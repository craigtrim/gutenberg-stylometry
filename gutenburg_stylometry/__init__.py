"""
Gutenberg Stylometry - Quantitative stylometric analysis for Project Gutenberg corpus.

This package provides tools for computing and comparing stylometric metrics
across authors, enabling quantitative literary analysis.
"""

__version__ = "0.1.0"

from gutenburg_stylometry.tokenizer import VictorianTokenizer, tokenize
from gutenburg_stylometry.models import (
    BookMetadata,
    TTRResult,
    TTRAggregate,
    TTRComparison,
)

__all__ = [
    "VictorianTokenizer",
    "tokenize",
    "BookMetadata",
    "TTRResult",
    "TTRAggregate",
    "TTRComparison",
]
