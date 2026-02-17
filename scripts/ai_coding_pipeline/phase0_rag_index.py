#!/usr/bin/env python3
"""
Phase 0: Build RAG Index
Load PDFs, chunk documents, embed, and store in ChromaDB.
Adapted for agentic AI learning outcomes meta-analysis.
"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List

try:
    import chromadb
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    raise ImportError(
        f"Missing required dependency: {e}. "
        "Install with: pip install chromadb sentence-transformers"
    )

from utils.pdf_processor import PDFProcessor

logger = logging.getLogger(__name__)


class RAGIndexBuilder:
    """Builds and manages the RAG index for agentic AI learning outcome papers."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.rag_config = config['rag']

        logger.info(f"Loading embedding model: {self.rag_config['embedding_model']}")
        self.embedder = SentenceTransformer(self.rag_config['embedding_model'])

        self.client = chromadb.Client(Settings(
            persist_directory=self.rag_config['persist_directory'],
            anonymized_telemetry=False
        ))

        self.collection = self.client.get_or_create_collection(
            name=self.rag_config['collection_name'],
            metadata={"description": "Agentic AI learning outcomes papers for meta-analysis"}
        )

        self.pdf_processor = PDFProcessor()

    def chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks.

        Args:
            text: Full text to chunk
            chunk_size: Maximum characters per chunk
            overlap: Number of overlapping characters

        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = []
        start = 0
        chunk_id = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            if end < len(text):
                last_period = chunk_text.rfind('.')
                last_newline = chunk_text.rfind('\n')
                break_point = max(last_period, last_newline)

                if break_point > chunk_size * 0.5:
                    end = start + break_point + 1
                    chunk_text = text[start:end]

            chunks.append({
                'text': chunk_text.strip(),
                'chunk_id': chunk_id,
                'start_char': start,
                'end_char': end
            })

            chunk_id += 1
            start = end - overlap

        return chunks

    def process_pdf(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """
        Process a single PDF into chunks with metadata.

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of chunks with embeddings and metadata
        """
        logger.info(f"Processing PDF: {pdf_path.name}")

        text = self.pdf_processor.extract_text(pdf_path)

        if not text or len(text.strip()) < 100:
            logger.warning(f"Insufficient text extracted from {pdf_path.name}")
            return []

        chunks = self.chunk_text(
            text,
            self.rag_config['chunk_size'],
            self.rag_config['chunk_overlap']
        )

        processed_chunks = []
        for chunk in chunks:
            processed_chunks.append({
                'id': f"{pdf_path.stem}_chunk_{chunk['chunk_id']}",
                'text': chunk['text'],
                'metadata': {
                    'source_file': pdf_path.name,
                    'chunk_id': chunk['chunk_id'],
                    'start_char': chunk['start_char'],
                    'end_char': chunk['end_char'],
                    'char_count': len(chunk['text'])
                }
            })

        return processed_chunks

    def build_index(self, pdf_dir: Path) -> Dict[str, Any]:
        """
        Build the complete RAG index from all PDFs.

        Args:
            pdf_dir: Directory containing PDF files

        Returns:
            Statistics about the built index
        """
        pdf_files = list(pdf_dir.glob("*.pdf"))

        if not pdf_files:
            logger.warning(f"No PDF files found in {pdf_dir}")
            return {'n_pdfs': 0, 'n_chunks': 0, 'avg_chunk_size': 0}

        logger.info(f"Found {len(pdf_files)} PDF files to process")

        all_chunks = []
        failed_pdfs = []

        for pdf_path in pdf_files:
            try:
                chunks = self.process_pdf(pdf_path)
                all_chunks.extend(chunks)
            except Exception as e:
                logger.error(f"Failed to process {pdf_path.name}: {e}")
                failed_pdfs.append(pdf_path.name)

        if not all_chunks:
            logger.error("No chunks created from any PDF")
            return {
                'n_pdfs': len(pdf_files),
                'n_chunks': 0,
                'avg_chunk_size': 0,
                'failed_pdfs': failed_pdfs
            }

        logger.info(f"Embedding {len(all_chunks)} chunks...")
        texts = [chunk['text'] for chunk in all_chunks]
        embeddings = self.embedder.encode(texts, show_progress_bar=True)

        logger.info("Adding chunks to ChromaDB...")
        self.collection.add(
            ids=[chunk['id'] for chunk in all_chunks],
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=[chunk['metadata'] for chunk in all_chunks]
        )

        avg_chunk_size = sum(len(chunk['text']) for chunk in all_chunks) / len(all_chunks)

        stats = {
            'n_pdfs': len(pdf_files),
            'n_pdfs_processed': len(pdf_files) - len(failed_pdfs),
            'n_chunks': len(all_chunks),
            'avg_chunk_size': round(avg_chunk_size, 1),
            'failed_pdfs': failed_pdfs
        }

        logger.info(f"Index built successfully: {stats}")
        return stats

    def query(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query the RAG index for relevant chunks.

        Args:
            query_text: Query string
            n_results: Number of results to return

        Returns:
            List of relevant chunks with metadata
        """
        query_embedding = self.embedder.encode([query_text])[0]

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )

        chunks = []
        for i in range(len(results['ids'][0])):
            chunks.append({
                'id': results['ids'][0][i],
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })

        return chunks


def build_rag_index(config: Dict[str, Any], cost_tracker, audit_logger) -> Dict[str, Any]:
    """
    Phase 0 entry point: Build RAG index from study PDFs.

    Args:
        config: Pipeline configuration
        cost_tracker: Cost tracking instance
        audit_logger: Audit logging instance

    Returns:
        Result dictionary with success status and statistics
    """
    logger.info("Starting Phase 0: RAG Index Building")

    try:
        builder = RAGIndexBuilder(config)

        pdf_dir = Path(config['paths']['pdfs'])
        stats = builder.build_index(pdf_dir)

        stats_path = Path(config['paths']['logs']) / 'phase0_index_stats.json'
        with open(stats_path, 'w') as f:
            json.dump(stats, f, indent=2)

        logger.info(f"Index statistics saved to {stats_path}")

        audit_logger.log_event(
            phase='phase0',
            event_type='index_built',
            details=stats
        )

        return {
            'success': True,
            'summary': stats,
            'output_path': str(stats_path)
        }

    except Exception as e:
        logger.error(f"Phase 0 failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    import yaml
    from utils.cost_tracker import CostTracker
    from utils.audit import AuditLogger

    with open('scripts/ai_coding_pipeline/config.yaml') as f:
        config = yaml.safe_load(f)

    result = build_rag_index(
        config,
        CostTracker(),
        AuditLogger(config['paths']['logs'])
    )

    print(json.dumps(result, indent=2))
