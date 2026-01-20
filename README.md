# Gutenberg Stylometry

Quantitative stylometric analysis for comparing authors using a 60,000+ book corpus from Project Gutenberg.

## Overview

Compare 2-5 authors using statistical text analysis metrics:

- **Vocabulary**: Type-Token Ratio, hapax legomena, word length distribution
- **Syntax**: Sentence length statistics, clause complexity
- **Function Words**: Distribution of common words (the, and, of, to)
- **Punctuation**: Semicolons, em-dashes, exclamation marks
- **Readability**: Flesch-Kincaid, Gunning Fog, SMOG Index
- **N-grams**: TF-IDF distinctive phrases

## Corpus

Books are stored in S3:
- **Bucket**: `s3://craigtrim-resources/gutenberg/txt/`
- **Naming**: `{author}-{title}-{gutenberg_id}.txt`
- **Size**: ~60,000 books

## Usage

```bash
# Install dependencies
poetry install

# Compare authors
poetry run compare-authors dickens hardy austen

# With specific metrics
poetry run compare-authors dickens hardy --metrics vocabulary,punctuation

# Generate HTML report
poetry run compare-authors dickens hardy austen --format html --output report.html
```

## Sample Authors

Victorian: dickens, bronte, eliot, hardy, trollope, collins, wilde, kipling, stoker, carroll

Edwardian: wells, conrad, doyle, forster, woolf, lawrence, wodehouse, chesterton

Pre-Victorian: austen, scott, shelley

## Project Structure

```
gutenburg_stylometry/
├── corpus.py           # S3 corpus access
├── tokenizer.py        # Text processing
├── metrics/
│   ├── vocabulary.py   # TTR, hapax, word length
│   ├── syntax.py       # Sentence metrics
│   ├── function_words.py
│   ├── punctuation.py
│   └── readability.py
├── compare.py          # Author comparison
├── report.py           # Report generation
└── cli.py              # Command-line interface
```

## See Also

- [CONTEXT.md](CONTEXT.md) - Detailed project context and metric definitions
- Related: [tfidf-compute](../mville/cosc-agentic-systems/utils/tfidf-compute/) - TF-IDF implementation with custom tokenizer
