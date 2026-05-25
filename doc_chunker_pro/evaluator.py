
from typing import List, Dict, Any
from .utils.tf_utils import tfidf_vectors, cosine_sim

def evaluate_sections(sections: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Flatten chunks
    all_texts = []
    section_idx = []
    for si, s in enumerate(sections):
        for c in s["chunks"]:
            all_texts.append(c["content"])
            section_idx.append(si)

    if not all_texts:
        return {"avg_cohesion": 0.0, "avg_separation": 0.0, "details": {"cohesion_samples": 0, "separation_samples": 0}}

    vecs, _ = tfidf_vectors(all_texts)

    # Cohesion: average cosine similarity between consecutive chunks within the same section
    cohesion_vals = []
    offset = 0
    for si, s in enumerate(sections):
        m = len(s["chunks"])
        for i in range(m-1):
            a = vecs[offset + i]
            b = vecs[offset + i + 1]
            cohesion_vals.append(cosine_sim(a,b))
        offset += m

    # Separation: for each chunk, compare to the closest chunk from a different section,
    # take 1 - max_similarity, then average.
    separation_vals = []
    for i, vi in enumerate(vecs):
        my_sec = section_idx[i]
        best = 0.0
        for j, vj in enumerate(vecs):
            if section_idx[j] == my_sec or i == j: 
                continue
            sim = cosine_sim(vi, vj)
            if sim > best:
                best = sim
        separation_vals.append(1.0 - best)

    return {
        "avg_cohesion": float(sum(cohesion_vals)/len(cohesion_vals)) if cohesion_vals else 0.0,
        "avg_separation": float(sum(separation_vals)/len(separation_vals)) if separation_vals else 0.0,
        "details": {
            "cohesion_samples": len(cohesion_vals),
            "separation_samples": len(separation_vals)
        }
    }
