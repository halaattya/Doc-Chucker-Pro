
from typing import List
class DocxReader:
    def __init__(self, path: str):
        self.path = path

    def extract_paragraphs(self) -> List[str]:
        try:
            from docx import Document as Docx
        except Exception:
            return []
        doc = Docx(self.path)
        out = []
        # Extract paragraphs
        for p in doc.paragraphs:
            t = (p.text or "").strip()
            if t:
                out.append(t)
        # Extract tables as markdown
        for table in doc.tables:
            rows = []
            for row in table.rows:
                cells = [ (cell.text or "").strip().replace("\n"," ") for cell in row.cells ]
                rows.append(cells)
            if rows:
                # build markdown table
                header = rows[0]
                align = ["---"] * len(header)
                md = []
                md.append("| " + " | ".join(header) + " |")
                md.append("| " + " | ".join(align) + " |")
                for r in rows[1:]:
                    md.append("| " + " | ".join(r) + " |")
                out.append("\n".join(md))
        return out
