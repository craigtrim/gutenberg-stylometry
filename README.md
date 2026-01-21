# Gutenberg Stylometry

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![60k+ Books](https://img.shields.io/badge/corpus-60k%2B%20books-orange.svg)](#corpus)

**Can you tell Dickens from Doyle by the numbers alone?**

This toolkit quantifies writing style. It transforms prose into measurable fingerprints. Feed it any author from the 60,000+ book Gutenberg corpus and discover what makes their voice unique.

## Why This Matters

Every author has tells. Dickens loved semicolons. Austen's sentences run long and balanced. Hemingway's don't.

These patterns aren't stylistic quirks. They're statistically significant signatures that persist across an author's entire body of work.

Stylometry has been used to:
- **Unmask anonymous authors** (who really wrote that political essay?)
- **Detect ghostwriting** (did the celebrity actually write their memoir?)
- **Authenticate disputed texts** (is this newly discovered manuscript genuine?)
- **Study literary influence** (how did Dickens shape the Victorians who followed?)

## Quick Start

```bash
poetry install
poetry run python scripts/compute_ttr.py data/dickens_clean -o dickens_ttr.jsonl
```

## What It Measures

| Metric | What It Reveals |
|--------|-----------------|
| **Type-Token Ratio** | Vocabulary richness. How often an author repeats words. |
| **STTR** | Standardized TTR. Controls for text length bias. |
| **Hapax Legomena** | Words used exactly once. A signature of lexical range. |
| **Sentence Length** | Rhythm and complexity. Short and punchy vs. long and elaborate. |
| **Function Words** | The unconscious glue words (the, of, and) that betray authorship. |
| **Punctuation Profile** | Semicolon addiction? Em-dash enthusiast? The marks don't lie. |

## Current Authors

| Era | Authors | Works |
|-----|---------|-------|
| **Pre-Victorian** | Austen | 8 novels |
| **Victorian** | Dickens, Eliot, Brontës | 45+ works |
| **Late Victorian** | Doyle | 12 works (Holmes canon + novels) |

## Sample Output

```
Austen vs Eliot vs Dickens: STTR Comparison

Author      Mean STTR    Std Dev    Interpretation
-----------------------------------------------------
Eliot       0.4446       0.0148     Richest vocabulary
Austen      0.4141       0.0077     Most consistent style
Dickens     0.4089       0.0112     Broadest audience appeal
```

## Corpus

60,000+ public domain books from Project Gutenberg. Normalized and deduplicated.

```
s3://craigtrim-resources/gutenberg/txt/
├── dickens-great-expectations-1400.txt
├── austen-pride-and-prejudice-1342.txt
├── doyle-the-hound-of-the-baskervilles-2852.txt
└── ... (60k more)
```

## Project Structure

```
gutenburg_stylometry/
├── normalize.py        # Strip Gutenberg boilerplate
├── tokenizer.py        # Victorian-aware tokenization
├── metrics/
│   └── ttr.py          # Type-Token Ratio variants
├── models.py           # Pydantic data models
└── protocols.py        # Type interfaces
```

## Roadmap

- [ ] Sentence-level metrics (length distribution, complexity)
- [ ] Function word profiles
- [ ] Punctuation fingerprinting
- [ ] Cross-author comparison reports
- [ ] Web visualization dashboard

## References

- Burrows, J.F. (2002). "Delta: A Measure of Stylistic Difference"
- Stamatatos, E. (2009). "A Survey of Modern Authorship Attribution Methods"
- Koppel, M. et al. (2009). "Computational Methods in Authorship Attribution"

---

*Built for literary curiosity. What patterns will you find?*
