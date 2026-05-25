
import math
import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple

WORD_RE = re.compile(r"[A-Za-z0-9\-\_]+|[\u0600-\u06FF]+")

def tokenize(text: str) -> List[str]:
    if not text:
        return []
    return [t.lower() for t in WORD_RE.findall(text)]

def term_freq(tokens: List[str]) -> Dict[str, float]:
    c = Counter(tokens)
    total = sum(c.values()) or 1
    return {k: v/total for k, v in c.items()}

def tfidf_vectors(docs: List[str]) -> Tuple[List[Dict[str,float]], Dict[str,float]]:
    # Build DF
    dfs = Counter()
    tokenized = [tokenize(d) for d in docs]
    for toks in tokenized:
        for w in set(toks):
            dfs[w] += 1
    N = len(docs)
    idf = {w: math.log((N+1)/(df+0.5)) + 1 for w, df in dfs.items()}  # smoothed IDF
    vecs = []
    for toks in tokenized:
        tf = Counter(toks)
        total = sum(tf.values()) or 1
        vec = {w: (tf[w]/total) * idf.get(w, 0.0) for w in tf}
        vecs.append(vec)
    return vecs, idf

def cosine_sim(v1: Dict[str,float], v2: Dict[str,float]) -> float:
    if not v1 or not v2:
        return 0.0
    # dot
    dot = 0.0
    for k, a in v1.items():
        b = v2.get(k)
        if b:
            dot += a*b
    # norms
    n1 = sum(a*a for a in v1.values()) ** 0.5
    n2 = sum(b*b for b in v2.values()) ** 0.5
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot/(n1*n2)
