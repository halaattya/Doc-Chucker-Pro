# Doc Chunker Pro 📄

An intelligent document chunking system that splits PDF, DOCX, TXT, and Markdown files into topic-based chunks rather than fixed-length segments. Built as a technical task during an AI & Data Science internship at Insightix.

## Overview

Most chunking tools split documents by word count or paragraph. This system detects topic boundaries using heading detection heuristics and TF-IDF-based semantic analysis, producing structured JSON output with cohesion/separation quality scores for each document.

## Features

- **Multi-format support** — PDF, DOCX, TXT, and Markdown
- **Topic-based chunking** — detects section boundaries via heading patterns and heuristics, not fixed length
- **Chunk size constraints** — configurable min/max word limits with sentence-boundary splitting
- **Quality evaluation** — measures cohesion (intra-section similarity) and separation (inter-section dissimilarity) using TF-IDF vectors and cosine similarity
- **Batch processing** — accepts a single file or a whole folder
- **Structured JSON output** — includes document metadata, per-section chunks, and evaluation scores

## Tech Stack

- **Language:** Python 3.10+
- **Architecture:** OOP with reader/chunker/evaluator separation
- **NLP:** Custom TF-IDF implementation (no external NLP dependencies)
- **Document parsing:** PyPDF2, python-docx

## Project Structure

```
doc_chunker_pro/
├── main.py                  # CLI entry point
├── chunker.py               # Heading detection & topic-based chunking logic
├── evaluator.py             # Cohesion/separation quality scoring
├── readers/
│   ├── __init__.py          # Reader factory (get_reader by extension)
│   ├── pdf_reader.py        # PDF paragraph extractor
│   ├── docx_reader.py       # DOCX paragraph extractor
│   └── txt_reader.py        # TXT/Markdown paragraph extractor
└── utils/
    ├── stopwords.py         # Stopword list
    ├── tf_utils.py          # Tokenization, TF-IDF, cosine similarity
    └── heading.py           # Auto-heading generation for unlabelled sections
```

## Installation

```bash
git clone https://github.com/<your-username>/doc-chunker-pro.git
cd doc-chunker-pro
pip install -r requirements.txt
```

## Usage

**Single file:**
```bash
python -m doc_chunker_pro.main --input document.pdf --output results.json
```

**Whole folder:**
```bash
python -m doc_chunker_pro.main --input ./data/ --output results.json
```

**With custom chunk sizes:**
```bash
python -m doc_chunker_pro.main --input document.docx --output out.json --min-chunk-words 50 --max-chunk-words 300
```

**Arguments:**

| Argument | Default | Description |
|---|---|---|
| `--input` | required | Path to a file or folder |
| `--output` | `output.json` | Output JSON file path |
| `--min-chunk-words` | `60` | Minimum words per chunk |
| `--max-chunk-words` | `220` | Maximum words per chunk |

## Output Format

```json
{
  "dataset_metadata": {
    "root": "/path/to/input",
    "files_processed": 1,
    "evaluation": {
      "avg_cohesion": 0.74,
      "avg_separation": 0.61,
      "documents": 1
    }
  },
  "documents": [
    {
      "document_metadata": {
        "filename": "sample.pdf",
        "file_type": "pdf",
        "total_sections": 4,
        "evaluation": { "avg_cohesion": 0.74, "avg_separation": 0.61 }
      },
      "chunks": [
        {
          "header": "Introduction",
          "chunks": [
            {
              "chunk_id": 1,
              "content": "Machine learning is a subset of artificial intelligence...",
              "metadata": { "word_count": 87 }
            }
          ]
        }
      ]
    }
  ]
}
```

## Chunking Quality Evaluation


Quality is measured with two metrics:

- **Cohesion** — average cosine similarity between consecutive chunks *within* the same section. Higher = chunks in the same section are topically consistent.
- **Separation** — for each chunk, `1 - max_similarity` against all chunks from *other* sections. Higher = sections are topically distinct from each other.

  

Both are computed using a custom TF-IDF implementation with smoothed IDF, with no external NLP dependencies required.   


Contact

Hala Atiyeh

linkedin.com/in/halaattya

hala.attya.2004@gmail.com
