"""
Output writers for stylometric metrics.

Supports JSONL format for streaming/append-friendly output.
"""

import json
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel


class JSONLWriter:
    """
    Writer for JSON Lines format.

    Each call to write() appends a single JSON object as a new line.
    Supports both Pydantic models and plain dicts.
    """

    def __init__(self, file_path: Path, append: bool = False):
        """
        Initialize writer.

        Args:
            file_path: Path to output .jsonl file
            append: If True, append to existing file; if False, overwrite
        """
        self._file_path = file_path
        self._append = append
        self._handle: Optional[Any] = None
        self._count = 0

    def __enter__(self) -> "JSONLWriter":
        """Open file for writing."""
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if self._append else "w"
        self._handle = open(self._file_path, mode, encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close file handle."""
        if self._handle:
            self._handle.close()
            self._handle = None

    def write(self, data: BaseModel | dict) -> None:
        """
        Write a single record as a JSON line.

        Args:
            data: Pydantic model or dict to write
        """
        if self._handle is None:
            raise RuntimeError("Writer not opened. Use 'with' context manager.")

        if isinstance(data, BaseModel):
            # Use Pydantic's serialization
            line = data.model_dump_json()
        else:
            line = json.dumps(data, default=str)

        self._handle.write(line + "\n")
        self._count += 1

    def flush(self) -> None:
        """Flush buffered writes to disk."""
        if self._handle:
            self._handle.flush()

    @property
    def records_written(self) -> int:
        """Return count of records written."""
        return self._count


class JSONWriter:
    """
    Writer for single JSON files (aggregates, comparisons).
    """

    @staticmethod
    def write(file_path: Path, data: BaseModel | dict) -> None:
        """
        Write data to a JSON file.

        Args:
            file_path: Output path
            data: Pydantic model or dict to write
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(data, BaseModel):
            content = data.model_dump_json(indent=2)
        else:
            content = json.dumps(data, indent=2, default=str)

        file_path.write_text(content, encoding="utf-8")

    @staticmethod
    def read(file_path: Path) -> dict:
        """
        Read a JSON file.

        Args:
            file_path: Path to read

        Returns:
            Parsed JSON as dict
        """
        return json.loads(file_path.read_text(encoding="utf-8"))


class JSONLReader:
    """
    Reader for JSON Lines files.
    """

    def __init__(self, file_path: Path):
        """
        Initialize reader.

        Args:
            file_path: Path to .jsonl file
        """
        self._file_path = file_path

    def __iter__(self):
        """Iterate over records in the file."""
        with open(self._file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield json.loads(line)

    def read_all(self) -> list[dict]:
        """Read all records into a list."""
        return list(self)
