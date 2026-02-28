#!/usr/bin/env python3
"""
Deduplication and merging for Trust Calibration Scoping Review.

Wrapper around the parent project's dedup_merge.py with scoping-review-specific
configuration and paths.

Usage:
    python scr_dedup_merge.py --config scr_dedup_config.json --output ../data/01_deduplicated
"""

import sys
import json
import logging
from pathlib import Path

# Add parent project's scripts directory to path
PARENT_SCRIPTS = Path(__file__).resolve().parent.parent.parent / "scripts" / "screening"
sys.path.insert(0, str(PARENT_SCRIPTS))

from dedup_merge import DeduplicatorMerger, merge_search_results

logger = logging.getLogger(__name__)


def resolve_paths(config: dict, base_dir: Path) -> dict:
    """Resolve relative paths in config relative to scoping-review root."""
    for entry in config.get("search_files", []):
        filepath = Path(entry["filepath"])
        if not filepath.is_absolute():
            entry["filepath"] = str(base_dir / filepath)
    return config


def main():
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    parser = argparse.ArgumentParser(
        description="Merge and deduplicate scoping review search results"
    )
    parser.add_argument(
        "--config",
        default="scr_dedup_config.json",
        help="JSON config file (default: scr_dedup_config.json)"
    )
    parser.add_argument(
        "--output",
        default="../data/01_deduplicated",
        help="Output directory (default: ../data/01_deduplicated)"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help="Override title similarity threshold (default: from config or 0.85)"
    )

    args = parser.parse_args()

    # Load config
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = Path(__file__).parent / config_path

    with open(config_path, "r") as f:
        config = json.load(f)

    # Resolve paths relative to scoping-review root
    scr_root = Path(__file__).resolve().parent.parent
    config = resolve_paths(config, scr_root)

    # Resolve output path
    output_dir = Path(args.output)
    if not output_dir.is_absolute():
        output_dir = scr_root / output_dir

    # Override threshold if specified
    threshold = args.threshold or config.get("title_similarity_threshold", 0.85)

    logger.info(f"Scoping Review Dedup")
    logger.info(f"  Config: {config_path}")
    logger.info(f"  Output: {output_dir}")
    logger.info(f"  Threshold: {threshold}")
    logger.info(f"  Sources: {len(config['search_files'])}")

    # Check which files actually exist
    existing_files = []
    missing_files = []
    for entry in config["search_files"]:
        if Path(entry["filepath"]).exists():
            existing_files.append(entry)
        else:
            missing_files.append(entry["filepath"])

    if missing_files:
        logger.warning(f"Missing {len(missing_files)} source files:")
        for mf in missing_files:
            logger.warning(f"  - {mf}")

    if not existing_files:
        logger.error("No source files found. Export search results first.")
        logger.info("Expected files in data/00_search_results/:")
        for entry in config["search_files"]:
            logger.info(f"  - {Path(entry['filepath']).name}")
        sys.exit(1)

    # Run dedup on existing files only
    config["search_files"] = existing_files
    merge_search_results(config["search_files"], str(output_dir))


if __name__ == "__main__":
    main()
