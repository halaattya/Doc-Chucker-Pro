
from typing import List, Dict, Any, Tuple
import re
from .utils.heading import generate_heading
from .utils.tf_utils import tokenize

HEADING_PATTERNS = [
    re.compile(r"^\s*#{1,6}\s+"),                         # Markdown
    re.compile(r"^\s*\d+(\.\d+)*[\)\.]?\s+"),            # 1. 1.1. or 1)
    re.compile(r"^\s*[A-Z][A-Za-z0-9\s\-]{0,60}$"),      # Short Title Case-ish lines
]

def looks_like_heading(text: str) -> bool:
    # ignore extremely long lines
    if len(text) > 120:
        return False
    # one of patterns
    if any(pat.match(text.strip()) for pat in HEADING_PATTERNS):
        return True
    # Heuristic: <= 12 words, Most words TitleCase or ALLCAPS
    words = text.strip().split()
    if 1 <= len(words) <= 12:
        caps = sum(1 for w in words if w[:1].isupper() or w.isupper())
        if caps/len(words) > 0.6:
            return True
    return False

def sentence_split(text: str) -> List[str]:
    # simple sentence splitter
    parts = re.split(r'(?<=[\.\!\?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]

def chunk_section(paragraphs: List[str], min_words: int, max_words: int) -> List[Dict[str, Any]]:
    chunks = []
    current = []
    word_count = 0

    def flush():
        nonlocal current, word_count
        if current:
            content = "\n".join(current).strip()
            chunks.append({"content": content, "metadata": {"word_count": len(tokenize(content))}})
            current, word_count = [], 0

    for para in paragraphs:
        words = len(tokenize(para))
        # tables: do not split inside, treat as one paragraph
        is_table = ("\n|" in para) or ("|" in para and "\n" in para) or ("\t" in para) or ("  " in para)
        if is_table and word_count > 0 and (word_count + words) > max_words:
            flush()
        current.append(para)
        word_count += words
        if word_count >= max_words:
            # try to break at sentence boundaries
            text = "\n".join(current)
            sents = sentence_split(text)
            sub = []
            wc = 0
            for s in sents:
                sw = len(tokenize(s))
                if wc + sw > max_words and wc >= min_words:
                    chunks.append({"content": " ".join(sub).strip(), "metadata": {"word_count": wc}})
                    sub, wc = [], 0
                sub.append(s)
                wc += sw
            if sub:
                chunks.append({"content": " ".join(sub).strip(), "metadata": {"word_count": wc}})
            current, word_count = [], 0

    if word_count >= min_words or not chunks:
        flush()
    return chunks

def build_sections(paragraphs: List[str], min_words: int, max_words: int) -> List[Dict[str, Any]]:
    sections: List[Dict[str, Any]] = []
    current_header = None
    bucket: List[str] = []

    def emit_section():
        nonlocal current_header, bucket
        if not bucket:
            return
        chunks = chunk_section(bucket, min_words, max_words)
        header = current_header or generate_heading(" ".join(bucket))
        sections.append({"header": header, "chunks": [{"chunk_id": i+1, **c} for i, c in enumerate(chunks)]})
        bucket = []
        current_header = None

    for para in paragraphs:
        if looks_like_heading(para):
            emit_section()
            # strip leading numbering characters and hashes
            clean = re.sub(r"^\s*(?:#{1,6}\s+|\d+(\.\d+)*[\)\.]?\s+)", "", para).strip()
            current_header = clean
        else:
            bucket.append(para)

    emit_section()
    # If still no sections (empty input), return empty
    return [s for s in sections if s["chunks"]]
