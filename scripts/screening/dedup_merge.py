#!/usr/bin/env python3
"""
Deduplication and merging of search results from multiple databases.
Identifies and removes duplicate records before screening.
"""

import logging
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def normalize_title(title: str) -> str:
    """
    Normalize a title for fuzzy matching.

    Args:
        title: Raw title string

    Returns:
        Normalized title (lowercase, no punctuation, collapsed whitespace)
    """
    if not isinstance(title, str):
        return ""
    title = title.lower()
    title = re.sub(r'[^\w\s]', ' ', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title


def normalize_doi(doi: str) -> str:
    """
    Normalize a DOI string.

    Args:
        doi: Raw DOI string

    Returns:
        Normalized DOI (lowercase, stripped)
    """
    if not isinstance(doi, str):
        return ""
    doi = doi.lower().strip()
    doi = re.sub(r'^https?://doi\.org/', '', doi)
    doi = re.sub(r'^doi:', '', doi).strip()
    return doi


def title_similarity(t1: str, t2: str) -> float:
    """
    Calculate Jaccard similarity between two normalized titles.

    Args:
        t1: First title (normalized)
        t2: Second title (normalized)

    Returns:
        Similarity score between 0 and 1
    """
    if not t1 or not t2:
        return 0.0

    set1 = set(t1.split())
    set2 = set(t2.split())

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    return intersection / union if union > 0 else 0.0


class DeduplicatorMerger:
    """
    Deduplicates and merges records from multiple bibliographic databases.
    Uses DOI-exact match and title fuzzy matching for duplicate detection.
    """

    def __init__(self, title_threshold: float = 0.85):
        """
        Initialize deduplicator.

        Args:
            title_threshold: Jaccard similarity threshold for title-based deduplication
        """
        self.title_threshold = title_threshold

    def load_database_export(self, filepath: Path,
                             source_label: str,
                             required_cols: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Load a database export file (CSV or Excel).

        Args:
            filepath: Path to export file
            source_label: Label for the database source (e.g., 'Web_of_Science')
            required_cols: Required column names to validate

        Returns:
            DataFrame with standardized columns
        """
        suffix = filepath.suffix.lower()
        if suffix == '.csv':
            df = pd.read_csv(filepath, encoding='utf-8', on_bad_lines='skip')
        elif suffix in ('.xlsx', '.xls'):
            df = pd.read_excel(filepath)
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

        df['source_database'] = source_label
        df['source_file'] = filepath.name

        logger.info(f"Loaded {len(df)} records from {source_label} ({filepath.name})")
        return df

    def standardize_columns(self, df: pd.DataFrame,
                            column_map: Dict[str, str]) -> pd.DataFrame:
        """
        Rename columns to a standard schema.

        Args:
            df: Raw DataFrame
            column_map: Mapping from source column names to standard names
                        e.g., {'TI': 'title', 'AB': 'abstract', 'PY': 'year'}

        Returns:
            DataFrame with standardized column names
        """
        df = df.rename(columns=column_map)

        standard_cols = ['title', 'abstract', 'authors', 'year', 'doi',
                        'journal', 'volume', 'issue', 'pages',
                        'source_database', 'source_file']

        for col in standard_cols:
            if col not in df.columns:
                df[col] = None

        return df[standard_cols]

    def detect_duplicates_doi(self, df: pd.DataFrame) -> pd.Series:
        """
        Detect duplicates using exact DOI matching.

        Args:
            df: DataFrame with 'doi' column

        Returns:
            Boolean Series where True marks duplicates (keep=first)
        """
        df = df.copy()
        df['doi_normalized'] = df['doi'].apply(normalize_doi)

        # Only consider non-empty DOIs
        has_doi = df['doi_normalized'] != ''
        doi_duplicates = has_doi & df.duplicated(subset=['doi_normalized'], keep='first')

        logger.info(f"DOI duplicates found: {doi_duplicates.sum()}")
        return doi_duplicates

    def detect_duplicates_title(self, df: pd.DataFrame,
                                doi_dup_mask: Optional[pd.Series] = None) -> pd.Series:
        """
        Detect duplicates using title fuzzy matching (Jaccard similarity).
        Only applies to records not already flagged as DOI duplicates.

        Args:
            df: DataFrame with 'title' column
            doi_dup_mask: Boolean Series marking already-detected DOI duplicates

        Returns:
            Boolean Series where True marks title-based duplicates
        """
        df = df.copy()
        df['title_normalized'] = df['title'].apply(normalize_title)

        if doi_dup_mask is None:
            doi_dup_mask = pd.Series([False] * len(df), index=df.index)

        # Only check non-DOI-duplicates
        candidate_mask = ~doi_dup_mask
        candidates = df[candidate_mask].copy()

        title_dup_indices = set()
        titles = candidates['title_normalized'].tolist()
        indices = candidates.index.tolist()

        for i in range(len(titles)):
            if indices[i] in title_dup_indices:
                continue
            for j in range(i + 1, len(titles)):
                if indices[j] in title_dup_indices:
                    continue
                sim = title_similarity(titles[i], titles[j])
                if sim >= self.title_threshold:
                    title_dup_indices.add(indices[j])

        title_dup_mask = pd.Series([False] * len(df), index=df.index)
        for idx in title_dup_indices:
            title_dup_mask[idx] = True

        logger.info(f"Title similarity duplicates found: {title_dup_mask.sum()}")
        return title_dup_mask

    def merge_and_deduplicate(self, dataframes: List[Tuple[pd.DataFrame, str]]) -> pd.DataFrame:
        """
        Merge multiple DataFrames and remove duplicates.

        Args:
            dataframes: List of (DataFrame, source_label) tuples

        Returns:
            Deduplicated, merged DataFrame
        """
        if not dataframes:
            return pd.DataFrame()

        dfs = []
        for df, label in dataframes:
            df = df.copy()
            df['source_database'] = label
            dfs.append(df)

        merged = pd.concat(dfs, ignore_index=True)
        logger.info(f"Total records before dedup: {len(merged)}")

        # Step 1: DOI dedup
        doi_dups = self.detect_duplicates_doi(merged)

        # Step 2: Title dedup (on remaining)
        title_dups = self.detect_duplicates_title(merged, doi_dup_mask=doi_dups)

        all_dups = doi_dups | title_dups
        deduplicated = merged[~all_dups].copy()
        deduplicated = deduplicated.reset_index(drop=True)

        # Assign study IDs
        deduplicated['study_id'] = [
            f"STUDY_{i+1:04d}" for i in range(len(deduplicated))
        ]

        n_removed = all_dups.sum()
        logger.info(
            f"Removed {n_removed} duplicates "
            f"({doi_dups.sum()} DOI, {title_dups.sum()} title-based)"
        )
        logger.info(f"Records after dedup: {len(deduplicated)}")

        return deduplicated

    def generate_dedup_report(self, original_counts: Dict[str, int],
                              final_count: int,
                              doi_dup_count: int,
                              title_dup_count: int,
                              output_path: Path):
        """
        Generate a deduplication report for PRISMA flow.

        Args:
            original_counts: Dict mapping source label to record count
            final_count: Final record count after deduplication
            doi_dup_count: Number of DOI-based duplicates removed
            title_dup_count: Number of title-based duplicates removed
            output_path: Path to save JSON report
        """
        total_original = sum(original_counts.values())
        total_removed = doi_dup_count + title_dup_count

        report = {
            'timestamp': datetime.now().isoformat(),
            'sources': original_counts,
            'total_original': total_original,
            'doi_duplicates_removed': doi_dup_count,
            'title_duplicates_removed': title_dup_count,
            'total_duplicates_removed': total_removed,
            'final_unique_records': final_count,
            'deduplication_rate': round(total_removed / total_original, 3) if total_original > 0 else 0
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            import json
            json.dump(report, f, indent=2)

        logger.info(f"Deduplication report saved: {output_path}")
        return report


def merge_search_results(search_files: List[Dict[str, Any]],
                         output_dir: str = "data/00_raw"):
    """
    Main function to merge and deduplicate multiple search result files.

    Args:
        search_files: List of dicts with keys: filepath, source_label, column_map
        output_dir: Directory to save merged results
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    merger = DeduplicatorMerger(title_threshold=0.85)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    import json
    dataframes = []
    original_counts = {}

    for config in search_files:
        df = merger.load_database_export(
            Path(config['filepath']),
            config['source_label']
        )
        df = merger.standardize_columns(df, config.get('column_map', {}))
        original_counts[config['source_label']] = len(df)
        dataframes.append((df, config['source_label']))

    merged_df = merger.merge_and_deduplicate(dataframes)

    output_csv = output_path / 'merged_deduplicated.csv'
    merged_df.to_csv(output_csv, index=False)
    logger.info(f"Merged dataset saved: {output_csv}")

    report = merger.generate_dedup_report(
        original_counts=original_counts,
        final_count=len(merged_df),
        doi_dup_count=0,
        title_dup_count=0,
        output_path=output_path / 'dedup_report.json'
    )

    print(f"\nDeduplication complete!")
    print(f"Original records: {report['total_original']}")
    print(f"Duplicates removed: {report['total_duplicates_removed']}")
    print(f"Unique records: {report['final_unique_records']}")
    print(f"Output: {output_csv}")

    return merged_df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Merge and deduplicate database search results"
    )
    parser.add_argument('--config', required=True,
                        help='JSON config file specifying search result files')
    parser.add_argument('--output', default='data/00_raw',
                        help='Output directory')

    args = parser.parse_args()

    import json
    with open(args.config, 'r') as f:
        config = json.load(f)

    merge_search_results(config['search_files'], args.output)
