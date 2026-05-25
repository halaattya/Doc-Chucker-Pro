
from typing import List
from .stopwords import EN, AR
from .tf_utils import tokenize, term_freq
import re

def choose_language(tokens: List[str]) -> str:
    # crude heuristic: if arabic tokens present, return ar
    for t in tokens:
        if re.search(r'[\u0600-\u06FF]', t):
            return 'ar'
    return 'en'

def generate_heading(text: str, max_words: int = 8) -> str:
    tokens = tokenize(text)
    if not tokens:
        return "General"
    lang = choose_language(tokens)
    stops = AR if lang == 'ar' else EN

    # keyword scoring = term frequency ignoring stopwords and very short tokens
    tf = term_freq([t for t in tokens if t not in stops and len(t) > 2])
    if not tf:
        # fallback: first 6 meaningful tokens
        keywords = [t for t in tokens if t not in stops][:max_words]
    else:
        # take top by tf
        keywords = sorted(tf.items(), key=lambda kv: kv[1], reverse=True)
        keywords = [k for k,_ in keywords[:max_words]]

    # post-process: join, title case for latin, keep as is for arabic
    if any(re.search(r'[\u0600-\u06FF]', k) for k in keywords):
        title = " ".join(keywords)
    else:
        title = " ".join(w.capitalize() for w in keywords)
    # Clean malware-y chars
    title = re.sub(r'[^A-Za-z0-9\u0600-\u06FF\s\-\_\+\:\(\)\[\]]','', title).strip()
    # Avoid empty
    return title or "Section"
