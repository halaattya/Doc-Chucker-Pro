
from .pdf_reader import PdfReader
from .docx_reader import DocxReader
from .txt_reader import TxtReader

def get_reader(ext: str):
    ext = ext.lower()
    if ext == ".pdf":
        return PdfReader
    if ext == ".docx":
        return DocxReader
    if ext in (".txt", ".md"):
        return TxtReader
    return None
