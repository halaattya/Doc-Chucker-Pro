
import argparse, json, os
from pathlib import Path
from typing import List, Dict, Any
from .readers import get_reader
from .chunker import build_sections
from .evaluator import evaluate_sections

SUPPORTED = [".pdf", ".docx", ".txt", ".md"]

def discover_inputs(path: Path) -> List[Path]:
    if path.is_file():
        return [path]
    files = []
    for ext in SUPPORTED:
        files.extend(path.rglob(f"*{ext}"))
    return files

def process_file(path: Path, min_words: int, max_words: int) -> Dict[str, Any]:
    Reader = get_reader(path.suffix)
    if not Reader:
        return {
            "document_metadata": {
                "filename": str(path),
                "file_type": path.suffix.lower().lstrip("."),
                "error": f"Unsupported file type: {path.suffix}"
            },
            "chunks": []
        }
    reader = Reader(str(path))
    paragraphs = reader.extract_paragraphs()
    sections = build_sections(paragraphs, min_words=min_words, max_words=max_words)
    evaluation = evaluate_sections(sections)
    return {
        "document_metadata": {
            "filename": str(path),
            "file_type": path.suffix.lower().lstrip("."),
            "total_sections": len(sections),
            "evaluation": evaluation
        },
        "chunks": sections
    }

def main():
    ap = argparse.ArgumentParser(description="Document Chunker Pro")
    ap.add_argument("--input", required=True, help="Path to a file or folder")
    ap.add_argument("--output", default="output.json", help="Unified JSON output path")
    ap.add_argument("--min-chunk-words", type=int, default=60)
    ap.add_argument("--max-chunk-words", type=int, default=220)
    args = ap.parse_args()

    in_path = Path(args.input)
    files = discover_inputs(in_path)

    outputs = []
    for f in files:
        outputs.append(process_file(f, args.min_chunk_words, args.max_chunk_words))

    # dataset-level evaluation summary (average over docs)
    evals = [o["document_metadata"].get("evaluation") for o in outputs if o["document_metadata"].get("evaluation")]
    if evals:
        avg_coh = sum(e["avg_cohesion"] for e in evals)/len(evals)
        avg_sep = sum(e["avg_separation"] for e in evals)/len(evals)
        dataset_eval = {"avg_cohesion": avg_coh, "avg_separation": avg_sep, "documents": len(evals)}
    else:
        dataset_eval = {"avg_cohesion": 0.0, "avg_separation": 0.0, "documents": 0}

    result = {
        "dataset_metadata": {
            "root": str(in_path.resolve()),
            "files_processed": len(outputs),
            "evaluation": dataset_eval
        },
        "documents": outputs
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ Wrote {args.output} for {len(outputs)} file(s).")

if __name__ == "__main__":
    main()
