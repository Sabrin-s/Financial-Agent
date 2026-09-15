import re
import fitz  # PyMuPDF
from typing import Dict, Any, List
from app.models.financial_schema import FinancialStatements, MetricSource

class DocumentAgent:
    """
    Parses PDF annual reports / financial statements, identifies tables and MD&A sections,
    and extracts text with page number grounding.
    """

    @staticmethod
    def parse_pdf(file_bytes: bytes, filename: str) -> Dict[str, Any]:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        pages_data = []
        full_text_corpus = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            tables = page.find_tables()
            
            table_records = []
            if tables and len(tables.tables) > 0:
                for t in tables:
                    try:
                        extracted = t.extract()
                        table_records.append(extracted)
                    except Exception:
                        pass

            pages_data.append({
                "page_number": page_num + 1,
                "text": text,
                "tables": table_records,
                "has_tables": len(table_records) > 0
            })
            full_text_corpus.append(f"[PAGE {page_num + 1}]\n{text}")

        # Basic document classification
        corpus_lower = " ".join(full_text_corpus).lower()
        doc_type = "Annual Report"
        if "cash flow" in corpus_lower and "balance sheet" in corpus_lower:
            doc_type = "Comprehensive Financial Filing"
        elif "balance sheet" in corpus_lower:
            doc_type = "Balance Sheet Statement"

        return {
            "filename": filename,
            "total_pages": len(doc),
            "document_type": doc_type,
            "pages": pages_data,
            "full_text": "\n\n".join(full_text_corpus)
        }
