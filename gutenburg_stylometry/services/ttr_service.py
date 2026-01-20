"""
TTR computation service.

Orchestrates the full pipeline:
1. Read normalized files
2. Tokenize text
3. Compute TTR metrics
4. Write results to JSONL
5. Aggregate per-author statistics
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from gutenburg_stylometry.io.reader import NormalizedFileReader, BookContent
from gutenburg_stylometry.io.writer import JSONLWriter, JSONWriter
from gutenburg_stylometry.metrics.ttr import TTRCalculator, TTRAggregator, TTRConfig
from gutenburg_stylometry.models import TTRResult, ProcessingResult, BatchProcessingStats
from gutenburg_stylometry.tokenizer import VictorianTokenizer


class TTRService:
    """
    Service for computing TTR metrics across the corpus.

    Handles the full pipeline from reading files to writing results.
    """

    def __init__(
        self,
        base_dir: Path,
        ttr_config: Optional[TTRConfig] = None,
        lowercase: bool = True,
    ):
        """
        Initialize TTR service.

        Args:
            base_dir: Project base directory (contains data/)
            ttr_config: Configuration for TTR computation
            lowercase: Whether to lowercase tokens
        """
        self._base_dir = base_dir
        self._reader = NormalizedFileReader(base_dir)
        self._tokenizer = VictorianTokenizer(lowercase=lowercase)
        self._calculator = TTRCalculator(config=ttr_config)
        self._aggregator = TTRAggregator()

    @property
    def metrics_dir(self) -> Path:
        """Directory for per-book metric outputs."""
        return self._base_dir / "data" / "metrics" / "vocabulary" / "ttr"

    @property
    def aggregates_dir(self) -> Path:
        """Directory for per-author aggregate outputs."""
        return self._base_dir / "data" / "aggregates" / "ttr"

    def process_book(self, content: BookContent) -> ProcessingResult:
        """
        Process a single book and compute TTR metrics.

        Args:
            content: Book content and metadata

        Returns:
            ProcessingResult with success status and result
        """
        try:
            # Tokenize
            tokens = self._tokenizer.tokenize(content.text)

            # Compute TTR
            result = self._calculator.compute(
                tokens=tokens,
                gutenberg_id=content.gutenberg_id,
                title=content.title,
                author=content.author,
            )

            return ProcessingResult(
                file_path=str(content.file_path),
                success=True,
                error=None,
                result=result,
            )

        except Exception as e:
            return ProcessingResult(
                file_path=str(content.file_path),
                success=False,
                error=str(e),
                result=None,
            )

    def process_author(self, author: str) -> BatchProcessingStats:
        """
        Process all books by an author.

        Writes per-book results to JSONL and returns batch statistics.

        Args:
            author: Author identifier (e.g., 'dickens')

        Returns:
            BatchProcessingStats with processing summary
        """
        started_at = datetime.utcnow()
        results: list[TTRResult] = []
        errors: list[tuple[str, str]] = []

        # Ensure output directory exists
        output_path = self.metrics_dir / f"{author}.jsonl"

        with JSONLWriter(output_path) as writer:
            for file_path in self._reader.iter_author_files(author):
                # Read file
                content = self._reader.read(file_path)

                # Process
                proc_result = self.process_book(content)

                if proc_result.success and proc_result.result:
                    writer.write(proc_result.result)
                    results.append(proc_result.result)
                else:
                    errors.append((str(file_path), proc_result.error or "Unknown error"))

        completed_at = datetime.utcnow()

        return BatchProcessingStats(
            author=author,
            files_processed=len(results) + len(errors),
            files_succeeded=len(results),
            files_failed=len(errors),
            total_words=sum(r.total_words for r in results),
            started_at=started_at,
            completed_at=completed_at,
            errors=errors,
        )

    def aggregate_author(self, author: str) -> dict:
        """
        Aggregate per-book results into author statistics.

        Reads from the per-book JSONL and writes aggregate JSON.

        Args:
            author: Author identifier

        Returns:
            Aggregate statistics dict
        """
        from gutenburg_stylometry.io.writer import JSONLReader

        # Read per-book results
        input_path = self.metrics_dir / f"{author}.jsonl"
        if not input_path.exists():
            raise FileNotFoundError(f"No metrics found for author: {author}")

        reader = JSONLReader(input_path)
        results = [TTRResult(**record) for record in reader]

        if not results:
            raise ValueError(f"No results found for author: {author}")

        # Compute aggregates
        aggregates = self._aggregator.aggregate(results, author)
        aggregates["generated_at"] = datetime.utcnow().isoformat()

        # Write aggregate file
        output_path = self.aggregates_dir / f"{author}.json"
        JSONWriter.write(output_path, aggregates)

        return aggregates

    def process_and_aggregate_author(self, author: str) -> tuple[BatchProcessingStats, dict]:
        """
        Full pipeline: process all books and aggregate.

        Args:
            author: Author identifier

        Returns:
            Tuple of (processing_stats, aggregate_results)
        """
        stats = self.process_author(author)
        aggregates = self.aggregate_author(author)
        return stats, aggregates

    def list_available_authors(self) -> list[str]:
        """List authors available in the normalized directory."""
        return self._reader.list_authors()
