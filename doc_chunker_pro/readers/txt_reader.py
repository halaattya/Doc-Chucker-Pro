
from typing import List
class TxtReader:
    def __init__(self, path: str):
        self.path = path

    def extract_paragraphs(self) -> List[str]:
        with open(self.path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        # preserve table-like blocks (lines with multiple spaces or tabs)
        paras = []
        buf = []
        for line in text.splitlines():
            if line.strip() == "":
                if buf:
                    paras.append("\n".join(buf).strip())
                    buf = []
            else:
                buf.append(line.rstrip())
        if buf:
            paras.append("\n".join(buf).strip())
        return [p for p in (x.strip() for x in paras) if p]
