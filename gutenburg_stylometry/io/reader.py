"""
File reader for normalized Gutenberg texts.

Reads normalized files from the data/normalized/ directory and
extracts metadata from filenames.
"""

import re
from pathlib import Path
from typing import Iterator, NamedTuple


class BookContent(NamedTuple):
    """Content and metadata extracted from a normalized file."""

    gutenberg_id: str
    title: str
    author: str
    text: str
    file_path: Path


class NormalizedFileReader:
    """
    Reader for normalized Gutenberg text files.

    Expects files in the format: {author}-{title}-{id}.txt
    Located in data/normalized/ directory.
    """

    def __init__(self, base_dir: Path):
        """
        Initialize reader.

        Args:
            base_dir: Base directory containing data/normalized/
        """
        self._normalized_dir = base_dir / "data" / "normalized"

    @property
    def normalized_dir(self) -> Path:
        """Return the normalized files directory."""
        return self._normalized_dir

    def parse_filename(self, filename: str) -> tuple[str, str, str]:
        """
        Extract author, title, and ID from filename.

        Expected format: author-title-words-here-12345.txt

        Args:
            filename: Filename to parse

        Returns:
            Tuple of (author, title, gutenberg_id)
        """
        # Remove .txt extension
        name = filename.replace(".txt", "")

        # Extract ID (last numeric segment after final dash)
        match = re.match(r"^(.+)-(\d+)$", name)
        if not match:
            raise ValueError(f"Cannot parse filename: {filename}")

        name_part = match.group(1)
        gutenberg_id = match.group(2)

        # First segment is author, rest is title
        parts = name_part.split("-")
        if len(parts) < 2:
            raise ValueError(f"Cannot parse author/title from: {filename}")

        author = parts[0]
        title = "-".join(parts[1:])

        return author, title, gutenberg_id

    def read(self, file_path: Path) -> BookContent:
        """
        Read a normalized file and extract content.

        Args:
            file_path: Path to the normalized .txt file

        Returns:
            BookContent with metadata and text
        """
        author, title, gutenberg_id = self.parse_filename(file_path.name)

        text = file_path.read_text(encoding="utf-8", errors="replace")

        return BookContent(
            gutenberg_id=gutenberg_id,
            title=title,
            author=author,
            text=text,
            file_path=file_path,
        )

    def iter_author_files(self, author: str) -> Iterator[Path]:
        """
        Iterate over all normalized files for an author.

        Args:
            author: Author identifier (e.g., 'dickens')

        Yields:
            Path objects for each matching file
        """
        if not self._normalized_dir.exists():
            raise FileNotFoundError(f"Normalized directory not found: {self._normalized_dir}")

        pattern = f"{author}-*.txt"
        yield from sorted(self._normalized_dir.glob(pattern))

    def iter_all_files(self) -> Iterator[Path]:
        """
        Iterate over all normalized files.

        Yields:
            Path objects for each .txt file
        """
        if not self._normalized_dir.exists():
            raise FileNotFoundError(f"Normalized directory not found: {self._normalized_dir}")

        yield from sorted(self._normalized_dir.glob("*.txt"))

    def list_authors(self) -> list[str]:
        """
        List all unique authors in the normalized directory.

        Returns:
            Sorted list of author identifiers
        """
        authors = set()
        for path in self.iter_all_files():
            try:
                author, _, _ = self.parse_filename(path.name)
                authors.add(author)
            except ValueError:
                continue
        return sorted(authors)
