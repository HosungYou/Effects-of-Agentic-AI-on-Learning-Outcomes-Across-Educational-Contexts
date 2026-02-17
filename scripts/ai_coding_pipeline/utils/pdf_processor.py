#!/usr/bin/env python3
"""
PDF processing utilities for extracting text and tables.
Adapted for effect size extraction from research papers.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Handles PDF text extraction and table detection for meta-analysis."""

    def __init__(self):
        """Initialize PDF processor with available libraries."""
        self.pdfplumber_available = False
        self.pypdf2_available = False
        self.tesseract_available = False

        try:
            import pdfplumber
            self.pdfplumber = pdfplumber
            self.pdfplumber_available = True
            logger.info("pdfplumber available")
        except ImportError:
            logger.warning("pdfplumber not available. Install with: pip install pdfplumber")

        try:
            import PyPDF2
            self.PyPDF2 = PyPDF2
            self.pypdf2_available = True
            logger.info("PyPDF2 available")
        except ImportError:
            logger.warning("PyPDF2 not available. Install with: pip install PyPDF2")

        try:
            import pytesseract
            from PIL import Image
            self.pytesseract = pytesseract
            self.Image = Image
            self.tesseract_available = True
            logger.info("pytesseract available for OCR")
        except ImportError:
            logger.warning("pytesseract not available. Install with: pip install pytesseract pillow")

    def extract_text(self, pdf_path: Path) -> str:
        """
        Extract all text from a PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text as a single string
        """
        if self.pdfplumber_available:
            try:
                return self._extract_with_pdfplumber(pdf_path)
            except Exception as e:
                logger.warning(f"pdfplumber extraction failed: {e}")

        if self.pypdf2_available:
            try:
                return self._extract_with_pypdf2(pdf_path)
            except Exception as e:
                logger.warning(f"PyPDF2 extraction failed: {e}")

        raise RuntimeError(f"Could not extract text from {pdf_path}. No PDF library available.")

    def _extract_with_pdfplumber(self, pdf_path: Path) -> str:
        """Extract text using pdfplumber."""
        text_parts = []

        with self.pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

        return '\n\n'.join(text_parts)

    def _extract_with_pypdf2(self, pdf_path: Path) -> str:
        """Extract text using PyPDF2."""
        text_parts = []

        with open(pdf_path, 'rb') as f:
            reader = self.PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

        return '\n\n'.join(text_parts)

    def extract_tables(self, pdf_path: Path) -> List[List[List[str]]]:
        """
        Extract tables from PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of tables (each table is a list of rows, each row is a list of strings)
        """
        if not self.pdfplumber_available:
            logger.warning("pdfplumber required for table extraction")
            return []

        all_tables = []

        try:
            with self.pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    if tables:
                        all_tables.extend(tables)
        except Exception as e:
            logger.error(f"Table extraction failed: {e}")

        return all_tables

    def extract_page_range(self, pdf_path: Path, start_page: int, end_page: int) -> str:
        """
        Extract text from specific page range.

        Args:
            pdf_path: Path to PDF file
            start_page: Starting page (1-indexed)
            end_page: Ending page (1-indexed, inclusive)

        Returns:
            Extracted text from page range
        """
        if self.pdfplumber_available:
            text_parts = []
            with self.pdfplumber.open(pdf_path) as pdf:
                for i in range(start_page - 1, min(end_page, len(pdf.pages))):
                    page_text = pdf.pages[i].extract_text()
                    if page_text:
                        text_parts.append(page_text)
            return '\n\n'.join(text_parts)

        elif self.pypdf2_available:
            text_parts = []
            with open(pdf_path, 'rb') as f:
                reader = self.PyPDF2.PdfReader(f)
                for i in range(start_page - 1, min(end_page, len(reader.pages))):
                    page_text = reader.pages[i].extract_text()
                    if page_text:
                        text_parts.append(page_text)
            return '\n\n'.join(text_parts)

        else:
            raise RuntimeError("No PDF library available")

    def find_effect_size_tables(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """
        Find tables likely containing effect size or descriptive statistics data.

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of candidate tables with metadata
        """
        if not self.pdfplumber_available:
            logger.warning("pdfplumber required for table detection")
            return []

        effect_size_tables = []

        # Keywords indicating effect size / descriptive stats tables
        keywords = [
            'mean', 'means', 'sd', 'standard deviation', 'standard error',
            'hedges', "cohen's d", "cohen's g", 'effect size', 'effect',
            'pretest', 'posttest', 'pre-test', 'post-test',
            'treatment', 'control', 'experimental', 't-test', 'f-test',
            'anova', 'ancova', 'gain score', 'improvement'
        ]

        try:
            with self.pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    page_text = page.extract_text() or ""
                    page_text_lower = page_text.lower()

                    has_keyword = any(kw in page_text_lower for kw in keywords)

                    if has_keyword:
                        tables = page.extract_tables()
                        for table_idx, table in enumerate(tables):
                            if self._is_effect_size_table(table):
                                effect_size_tables.append({
                                    'page': page_num,
                                    'table_index': table_idx,
                                    'table_data': table,
                                    'confidence': 'high' if 'effect size' in page_text_lower else 'medium'
                                })

        except Exception as e:
            logger.error(f"Effect size table detection failed: {e}")

        return effect_size_tables

    def _is_effect_size_table(self, table: List[List[str]]) -> bool:
        """
        Heuristic check if a table contains effect size or descriptive statistics.

        Args:
            table: Table data

        Returns:
            True if likely an effect size / descriptive statistics table
        """
        if not table or len(table) < 2:
            return False

        # Flatten header cells
        header_text = ' '.join(
            str(cell).lower() for cell in table[0] if cell
        )

        header_keywords = [
            'mean', 'sd', 'm', 'se', 'n', 'hedges', "cohen", 'effect',
            'pre', 'post', 'treatment', 'control', 't', 'f', 'p'
        ]

        has_header_keyword = any(kw in header_text for kw in header_keywords)

        # Check for numeric content
        numeric_cells = 0
        total_cells = 0

        for row in table[1:]:
            for cell in row[1:]:
                if cell:
                    total_cells += 1
                    try:
                        float(str(cell).strip().replace(',', '.'))
                        numeric_cells += 1
                    except ValueError:
                        pass

        numeric_ratio = numeric_cells / total_cells if total_cells > 0 else 0

        return has_header_keyword and numeric_ratio > 0.3

    def ocr_page(self, pdf_path: Path, page_num: int) -> str:
        """
        Perform OCR on a specific page for scanned PDFs.

        Args:
            pdf_path: Path to PDF file
            page_num: Page number (1-indexed)

        Returns:
            OCR-extracted text
        """
        if not self.tesseract_available:
            raise RuntimeError("pytesseract required for OCR. Install with: pip install pytesseract pillow")

        try:
            from pdf2image import convert_from_path

            images = convert_from_path(
                pdf_path,
                first_page=page_num,
                last_page=page_num
            )

            if not images:
                return ""

            text = self.pytesseract.image_to_string(images[0])
            return text

        except ImportError:
            logger.error("pdf2image required for OCR. Install with: pip install pdf2image")
            return ""
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return ""

    def get_metadata(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Extract PDF metadata.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with file metadata
        """
        metadata = {
            'filename': pdf_path.name,
            'file_size_bytes': pdf_path.stat().st_size
        }

        if self.pdfplumber_available:
            try:
                with self.pdfplumber.open(pdf_path) as pdf:
                    metadata['n_pages'] = len(pdf.pages)
                    metadata['pdf_metadata'] = pdf.metadata
            except Exception as e:
                logger.warning(f"Failed to extract metadata with pdfplumber: {e}")

        elif self.pypdf2_available:
            try:
                with open(pdf_path, 'rb') as f:
                    reader = self.PyPDF2.PdfReader(f)
                    metadata['n_pages'] = len(reader.pages)
                    metadata['pdf_metadata'] = dict(reader.metadata) if reader.metadata else {}
            except Exception as e:
                logger.warning(f"Failed to extract metadata with PyPDF2: {e}")

        return metadata
