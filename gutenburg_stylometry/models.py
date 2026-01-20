"""
Pydantic models for stylometric analysis.

These models define the data structures used throughout the pipeline,
ensuring type safety and validation at system boundaries.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =============================================================================
# BOOK METADATA
# =============================================================================


class BookMetadata(BaseModel):
    """Metadata extracted from a normalized Gutenberg file."""

    model_config = ConfigDict(frozen=True)

    gutenberg_id: str = Field(..., description="Gutenberg catalog ID")
    title: str = Field(..., description="Book title")
    author: str = Field(..., description="Author identifier (lowercase, from filename)")
    year_published: Optional[int] = Field(None, description="Original publication year")
    word_count: Optional[int] = Field(None, description="Total word count after tokenization")


# =============================================================================
# TTR METRICS
# =============================================================================


class TTRResult(BaseModel):
    """Type-Token Ratio results for a single book."""

    model_config = ConfigDict(frozen=True)

    gutenberg_id: str
    title: str
    author: str
    total_words: int = Field(..., ge=0, description="Total token count")
    unique_words: int = Field(..., ge=0, description="Unique token count (types)")
    ttr: float = Field(..., ge=0.0, le=1.0, description="Raw TTR: unique/total")
    root_ttr: float = Field(..., ge=0.0, description="Root TTR: unique/sqrt(total)")
    log_ttr: float = Field(..., ge=0.0, description="Log TTR: log(unique)/log(total)")
    sttr: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Standardized TTR (1000-word chunks)"
    )
    sttr_std: Optional[float] = Field(None, ge=0.0, description="STTR standard deviation")
    chunk_count: Optional[int] = Field(None, ge=0, description="Number of chunks for STTR")

    # Delta metrics: TTR(n) - TTR(n-1) between consecutive chunks
    delta_mean: Optional[float] = Field(None, description="Mean of chunk-to-chunk TTR deltas")
    delta_std: Optional[float] = Field(None, ge=0.0, description="Std dev of TTR deltas (volatility)")
    delta_min: Optional[float] = Field(None, description="Largest negative swing")
    delta_max: Optional[float] = Field(None, description="Largest positive swing")


class TTRAggregate(BaseModel):
    """Aggregated TTR statistics for an author."""

    model_config = ConfigDict(frozen=True)

    author: str
    book_count: int = Field(..., ge=0)
    total_words: int = Field(..., ge=0, description="Sum of words across all books")

    ttr_mean: float
    ttr_std: float
    ttr_min: float
    ttr_max: float
    ttr_median: float

    root_ttr_mean: float
    root_ttr_std: float

    log_ttr_mean: float
    log_ttr_std: float

    sttr_mean: Optional[float] = None
    sttr_std: Optional[float] = None

    generated_at: datetime = Field(default_factory=datetime.utcnow)


class TTRComparison(BaseModel):
    """Comparison of TTR metrics between two authors."""

    model_config = ConfigDict(frozen=True)

    author_a: str
    author_b: str

    author_a_ttr_mean: float
    author_b_ttr_mean: float
    ttr_delta: float = Field(..., description="author_a - author_b")

    author_a_sttr_mean: Optional[float] = None
    author_b_sttr_mean: Optional[float] = None
    sttr_delta: Optional[float] = None

    generated_at: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# PROCESSING STATUS
# =============================================================================


class ProcessingResult(BaseModel):
    """Result of processing a single file."""

    file_path: str
    success: bool
    error: Optional[str] = None
    result: Optional[TTRResult] = None


class BatchProcessingStats(BaseModel):
    """Statistics for a batch processing run."""

    author: str
    files_processed: int
    files_succeeded: int
    files_failed: int
    total_words: int
    started_at: datetime
    completed_at: datetime
    errors: list[tuple[str, str]] = Field(default_factory=list)
