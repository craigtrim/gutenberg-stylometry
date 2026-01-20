"""
Normalize Gutenberg text files for stylometric analysis.

This module handles:
1. Deduplication - selecting best version of works with multiple copies
2. Boilerplate removal - stripping Gutenberg headers/footers
3. Front matter removal - TOCs, character lists, illustration lists
4. Clean text output - pure authorial prose
"""

import os
import re
from pathlib import Path
from collections import defaultdict


def extract_work_id(filename: str) -> int:
    """Extract the Gutenberg ID number from filename."""
    match = re.search(r'-(\d+)\.txt$', filename)
    return int(match.group(1)) if match else 0


def extract_canonical_name(filename: str) -> str:
    """Extract canonical work name by removing ID suffix."""
    return re.sub(r'-\d+\.txt$', '', filename)


def group_by_work(input_dir: Path) -> dict[str, list[Path]]:
    """Group files by canonical work name."""
    groups = defaultdict(list)
    for f in input_dir.glob('*.txt'):
        canonical = extract_canonical_name(f.name)
        groups[canonical].append(f)
    return dict(groups)


def select_best_version(files: list[Path]) -> Path:
    """Select best version: largest file, ties broken by newest ID."""
    if len(files) == 1:
        return files[0]

    # Sort by file size (desc), then by ID (desc)
    scored = [(f.stat().st_size, extract_work_id(f.name), f) for f in files]
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return scored[0][2]


def find_content_boundaries(text: str) -> tuple[int, int]:
    """Find start and end of actual content (between Gutenberg markers)."""
    lines = text.split('\n')

    start_idx = 0
    end_idx = len(lines)

    # Find START marker
    for i, line in enumerate(lines):
        if re.search(r'\*\*\*\s*START OF (THE |THIS )?PROJECT GUTENBERG', line, re.IGNORECASE):
            start_idx = i + 1
            break

    # Find END marker
    for i in range(len(lines) - 1, -1, -1):
        if re.search(r'\*\*\*\s*END OF (THE |THIS )?PROJECT GUTENBERG', lines[i], re.IGNORECASE):
            end_idx = i
            break

    return start_idx, end_idx


def is_front_matter_line(line: str) -> bool:
    """Check if line is part of front matter to skip."""
    stripped = line.strip().upper()

    # Section headers to skip entirely
    skip_headers = [
        'CONTENTS', 'TABLE OF CONTENTS', 'INDEX',
        'LIST OF ILLUSTRATIONS', 'ILLUSTRATIONS',
        'LIST OF PLATES', 'CHARACTERS', 'DRAMATIS PERSONAE',
        'LIST OF CHAPTERS'
    ]

    return stripped in skip_headers


def is_front_matter_section(lines: list[str], start_idx: int) -> tuple[bool, int]:
    """
    Detect if we're in a front matter section and return end index.
    Returns (is_front_matter, end_index).
    """
    if start_idx >= len(lines):
        return False, start_idx

    line = lines[start_idx].strip().upper()

    # Check for section headers
    front_matter_headers = [
        'CONTENTS', 'TABLE OF CONTENTS', 'INDEX',
        'LIST OF ILLUSTRATIONS', 'ILLUSTRATIONS',
        'LIST OF PLATES', 'CHARACTERS', 'DRAMATIS PERSONAE',
        'LIST OF CHAPTERS'
    ]

    if line in front_matter_headers:
        # Skip until we hit a chapter marker or significant content
        end_idx = start_idx + 1
        while end_idx < len(lines):
            next_line = lines[end_idx].strip()
            # Check for chapter/section start
            if re.match(r'^(CHAPTER|STAVE|BOOK|PART|VOLUME)\s+[IVXLC\d]', next_line, re.IGNORECASE):
                return True, end_idx
            # Check for two consecutive blank lines followed by content (new section)
            if end_idx + 2 < len(lines):
                if (not next_line and
                    not lines[end_idx + 1].strip() and
                    lines[end_idx + 2].strip() and
                    re.match(r'^[A-Z]', lines[end_idx + 2].strip())):
                    # Potential new section, check if it's a chapter
                    potential = lines[end_idx + 2].strip().upper()
                    if re.match(r'^(CHAPTER|STAVE|BOOK|PART|VOLUME)\s+[IVXLC\d]', potential):
                        return True, end_idx + 2
            end_idx += 1
        return True, end_idx

    return False, start_idx


def is_toc_entry(line: str, next_lines: list[str] = None) -> bool:
    """Check if a line looks like a TOC entry."""
    stripped = line.strip()

    # TOC entries typically end with page numbers (possibly with dots leading to them)
    # e.g., "CHAPTER ONE--THE BEGINNING                                             3"
    # e.g., "CHAPTER ONE--THE BEGINNING.......................3"
    if re.search(r'\s{3,}\d+\s*$', stripped):  # Multiple spaces followed by number at end
        return True
    if re.search(r'\.{3,}\s*\d+\s*$', stripped):  # Dots followed by number at end
        return True

    # Check if this looks like a chapter listing in a TOC block
    # A real chapter is followed by prose content (substantial text)
    # A TOC entry is followed by another chapter or more TOC entries
    if next_lines:
        chapter_pattern = r'^(CHAPTER|STAVE|BOOK|PART|VOLUME)\s+[IVXLC\d]'
        if re.match(chapter_pattern, stripped.upper()):
            # Look ahead to find what kind of content follows
            # Skip blanks and short lines (like [Illustration]) to find the next substantial content
            chapter_count = 0
            prose_found = False

            for next_line in next_lines:
                next_stripped = next_line.strip()

                if not next_stripped:
                    continue

                # Skip short decorative lines like [Illustration], dividers, etc.
                if len(next_stripped) < 40:
                    if re.match(chapter_pattern, next_stripped.upper()):
                        chapter_count += 1
                    continue

                if re.match(chapter_pattern, next_stripped.upper()):
                    chapter_count += 1
                    continue

                # Found substantial content
                if len(next_stripped) > 60:
                    prose_found = True
                    break

            # If we found multiple chapters before prose, this is a TOC entry
            # If we found one chapter then prose, that chapter is real but this one is TOC
            if chapter_count >= 1:
                return True  # This is part of TOC (found another chapter ahead)

    return False


def find_prose_start(lines: list[str], content_start: int) -> int:
    """Find where the actual prose begins after title pages and front matter."""

    # First, try to find a chapter/section marker (NOT in TOC)
    chapter_patterns = [
        r'^(CHAPTER|STAVE|BOOK|PART|VOLUME)\s+[IVXLC\d]',
        r'^(CHAPTER|STAVE|BOOK|PART|VOLUME)\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)',
        r'^I\.\s+',  # Roman numeral chapter
        r'^1\.\s+',  # Numeric chapter
        r'^FIRST\s+(CHAPTER|STAVE|BOOK|PART)',
    ]

    for i, line in enumerate(lines[content_start:], content_start):
        stripped = line.strip()
        upper = stripped.upper()

        # Skip TOC entries (pass remaining lines for look-ahead)
        remaining_lines = lines[i+1:i+100] if i+1 < len(lines) else []
        if is_toc_entry(line, remaining_lines):
            continue

        for pattern in chapter_patterns:
            if re.match(pattern, upper):
                return i

    # If no chapter marker found, fall back to finding first substantial prose
    # after skipping known front matter patterns
    front_matter_markers = [
        'CONTENTS', 'TABLE OF CONTENTS', 'INDEX', 'LIST OF ILLUSTRATIONS',
        'ILLUSTRATIONS', 'LIST OF PLATES', 'CHARACTERS', 'DRAMATIS PERSONAE',
        'LIST OF CHAPTERS', 'PREFACE', 'INTRODUCTION', 'FOREWORD',
        'DEDICATION', 'PRODUCED BY', 'TRANSCRIBED BY'
    ]

    i = content_start
    while i < len(lines):
        stripped = lines[i].strip()
        upper = stripped.upper()

        # Skip blank lines
        if not stripped:
            i += 1
            continue

        # Skip lines that are clearly front matter
        if any(upper.startswith(marker) or upper == marker for marker in front_matter_markers):
            i += 1
            continue

        # Skip [Illustration] tags
        if stripped.startswith('[Illustration'):
            i += 1
            continue

        # Skip short uppercase lines (title elements)
        if len(stripped) < 50 and stripped.isupper():
            i += 1
            continue

        # Skip lines that look like title page formatting
        if len(stripped) < 40:
            i += 1
            continue

        # Found substantial content
        return i

    return content_start


def remove_trailing_notes(lines: list[str]) -> list[str]:
    """Remove transcriber's notes and other trailing content."""
    # Look for common trailing note patterns from the end
    trailing_patterns = [
        r'^\s*\+[-=+]+\+\s*$',  # Box borders like +-------+
        r'^\s*\|.*transcriber.*\|',  # Transcriber notes in boxes
        r'^\s*transcriber\'?s?\s+note',  # Transcriber's note
        r'^\s*\[note:',  # [Note: ...]
        r'^\s*\*\s*\*\s*\*\s*$',  # *** section breaks at very end
        r'^\s*end\s+of\s+(the\s+)?project',  # Any remaining end markers
        r'^\s*this\s+file\s+was\s+produced',  # Production notes
    ]

    # Find where to cut off
    cut_idx = len(lines)
    for i in range(len(lines) - 1, max(0, len(lines) - 50), -1):
        line = lines[i].strip().lower()
        for pattern in trailing_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                cut_idx = i
                break

    return lines[:cut_idx]


def clean_text(text: str) -> str:
    """Clean a Gutenberg text file, returning only the prose content."""
    lines = text.split('\n')

    # Find Gutenberg content boundaries
    content_start, content_end = find_content_boundaries(text)

    # Extract content between markers
    content_lines = lines[content_start:content_end]

    # Find where actual prose starts (after title pages, TOC, etc.)
    prose_start = find_prose_start(content_lines, 0)

    # Get prose content
    prose_lines = content_lines[prose_start:]

    # Remove trailing transcriber notes
    prose_lines = remove_trailing_notes(prose_lines)

    # Remove illustration tags
    cleaned_lines = []
    for line in prose_lines:
        # Remove [Illustration: ...] tags
        line = re.sub(r'\[Illustration:?[^\]]*\]', '', line)
        cleaned_lines.append(line)

    # Join and clean up excessive whitespace
    result = '\n'.join(cleaned_lines)

    # Remove excessive blank lines (more than 2 consecutive)
    result = re.sub(r'\n{4,}', '\n\n\n', result)

    # Strip leading/trailing whitespace
    result = result.strip()

    return result


def normalize_files(input_dir: Path, output_dir: Path, author: str = None) -> dict:
    """
    Normalize all text files in input_dir, writing clean versions to output_dir.

    Returns dict with stats about processing.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Group files by canonical work
    groups = group_by_work(input_dir)

    stats = {
        'total_input': sum(len(v) for v in groups.values()),
        'unique_works': len(groups),
        'duplicates_removed': 0,
        'files_written': 0,
        'errors': []
    }

    for canonical_name, files in groups.items():
        # Select best version
        best_file = select_best_version(files)
        stats['duplicates_removed'] += len(files) - 1

        try:
            # Read and clean
            text = best_file.read_text(encoding='utf-8', errors='replace')
            cleaned = clean_text(text)

            # Write output
            output_name = canonical_name + '.txt'
            output_path = output_dir / output_name
            output_path.write_text(cleaned, encoding='utf-8')
            stats['files_written'] += 1

        except Exception as e:
            stats['errors'].append((best_file.name, str(e)))

    return stats


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Normalize Gutenberg texts for stylometry')
    parser.add_argument('input_dir', type=Path, help='Directory containing raw Gutenberg texts')
    parser.add_argument('output_dir', type=Path, help='Directory for cleaned output')
    parser.add_argument('--author', type=str, help='Author name for output filenames')

    args = parser.parse_args()

    stats = normalize_files(args.input_dir, args.output_dir, args.author)

    print(f"Processed {stats['total_input']} input files")
    print(f"Found {stats['unique_works']} unique works")
    print(f"Removed {stats['duplicates_removed']} duplicates")
    print(f"Wrote {stats['files_written']} clean files")

    if stats['errors']:
        print(f"\nErrors ({len(stats['errors'])}):")
        for fname, err in stats['errors']:
            print(f"  {fname}: {err}")


if __name__ == '__main__':
    main()
