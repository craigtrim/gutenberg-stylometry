"""
Protocol definitions for stylometric analysis.

These protocols define the contracts/interfaces that implementations must follow.
Using protocols enables dependency injection and easier testing.
"""

from pathlib import Path
from typing import Iterator, Protocol, runtime_checkable

from gutenburg_stylometry.models import TTRResult, TTRAggregate


# =============================================================================
# TOKENIZATION
# =============================================================================


@runtime_checkable
class Tokenizer(Protocol):
    """Protocol for text tokenization."""

    def tokenize(self, text: str) -> list[str]:
        """
        Convert raw text into a list of tokens.

        Args:
            text: Raw input text

        Returns:
            List of tokens (words)
        """
        ...


# =============================================================================
# FILE I/O
# =============================================================================


@runtime_checkable
class NormalizedFileReader(Protocol):
    """Protocol for reading normalized Gutenberg files."""

    def read(self, file_path: Path) -> tuple[str, str, str, str]:
        """
        Read a normalized file and extract metadata + content.

        Args:
            file_path: Path to normalized .txt file

        Returns:
            Tuple of (gutenberg_id, title, author, text_content)
        """
        ...

    def iter_author_files(self, author: str) -> Iterator[Path]:
        """
        Iterate over all normalized files for an author.

        Args:
            author: Author identifier (e.g., 'dickens')

        Yields:
            Path objects for each file
        """
        ...


@runtime_checkable
class MetricWriter(Protocol):
    """Protocol for writing metric results."""

    def write(self, result: TTRResult) -> None:
        """
        Write a single metric result.

        Args:
            result: The metric result to write
        """
        ...

    def flush(self) -> None:
        """Flush any buffered writes to disk."""
        ...


# =============================================================================
# METRICS
# =============================================================================


@runtime_checkable
class TTRCalculator(Protocol):
    """Protocol for TTR calculation."""

    def compute(self, tokens: list[str]) -> TTRResult:
        """
        Compute TTR metrics from a list of tokens.

        Args:
            tokens: List of word tokens

        Returns:
            TTRResult with all TTR variants
        """
        ...


@runtime_checkable
class Aggregator(Protocol):
    """Protocol for aggregating per-book metrics into author summaries."""

    def aggregate(self, results: list[TTRResult]) -> TTRAggregate:
        """
        Aggregate multiple book results into an author summary.

        Args:
            results: List of per-book TTR results

        Returns:
            Aggregated statistics for the author
        """
        ...
