
from typing import List
class PdfReader:
    def __init__(self, path: str):
        self.path = path

    def extract_paragraphs(self) -> List[str]:
        try:
            import pdfplumber
        except Exception:
            # graceful fallback: read bytes and return empty
            return []
        paras = []
        with pdfplumber.open(self.path) as pdf:
            for page in pdf.pages:
                txt = page.extract_text() or ""
                # keep table-looking lines as single block by merging spaces
                lines = [l.strip() for l in txt.split("\n") if l.strip()]
                block = []
                for line in lines:
                    block.append(line)
                # naive paragraph split by blank lines is not reliable in pdfplumber,
                # so we accumulate per page then split by double spaces as paragraph hints.
                joined = "\n".join(block)
                # split by two or more newlines if present else keep whole page
                parts = [p.strip() for p in joined.split("\n\n") if p.strip()]
                if not parts and joined.strip():
                    parts = [joined.strip()]
                paras.extend(parts)
        return paras
