#!/usr/bin/env python3
"""
Compute TTR (Type-Token Ratio) metrics for text files.

Usage:
    poetry run python scripts/compute_ttr.py /path/to/dickens_clean
    poetry run python scripts/compute_ttr.py /path/to/dickens_clean --output results.jsonl
    poetry run python scripts/compute_ttr.py /path/to/dickens_clean -o results.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add project root to path for imports - must be before project imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from gutenburg_stylometry.metrics.ttr import TTRCalculator, TTRConfig, TTRAggregator  # noqa: E402
from gutenburg_stylometry.tokenizer import VictorianTokenizer  # noqa: E402
from gutenburg_stylometry.models import TTRResult  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.table import Table  # noqa: E402

console = Console()


def process_file(file_path: Path, tokenizer: VictorianTokenizer, calculator: TTRCalculator) -> TTRResult:
    """Process a single text file and compute TTR."""
    text = file_path.read_text(encoding="utf-8", errors="replace")
    tokens = tokenizer.tokenize(text)

    # Extract info from filename
    name = file_path.stem
    parts = name.rsplit("-", 1)
    if len(parts) == 2 and parts[1].isdigit():
        title_part, gutenberg_id = parts
    else:
        title_part = name
        gutenberg_id = "0"

    # Try to extract author from first part
    title_parts = title_part.split("-", 1)
    if len(title_parts) == 2:
        author = title_parts[0]
        title = title_parts[1]
    else:
        author = "unknown"
        title = title_part

    return calculator.compute(
        tokens=tokens,
        gutenberg_id=gutenberg_id,
        title=title,
        author=author,
    )


def print_results(results: list[TTRResult], aggregates: dict):
    """Print results summary."""
    console.print(f"\n[bold green]Processed {len(results)} files[/bold green]")
    console.print(f"  Total words: {aggregates['total_words']:,}")

    console.print("\n[bold]TTR Metrics:[/bold]")
    console.print(
        f"  Raw TTR:  mean={aggregates['ttr_mean']:.4f}  "
        f"std={aggregates['ttr_std']:.4f}  "
        f"range=[{aggregates['ttr_min']:.4f}, {aggregates['ttr_max']:.4f}]"
    )
    console.print(
        f"  Root TTR: mean={aggregates['root_ttr_mean']:.2f}  "
        f"std={aggregates['root_ttr_std']:.2f}"
    )
    console.print(
        f"  Log TTR:  mean={aggregates['log_ttr_mean']:.4f}  "
        f"std={aggregates['log_ttr_std']:.4f}"
    )

    if aggregates.get("sttr_mean") is not None:
        console.print(
            f"  STTR:     mean={aggregates['sttr_mean']:.4f}  "
            f"std={aggregates['sttr_std']:.4f}"
        )

    if aggregates.get("delta_std_mean") is not None:
        console.print(
            f"  Delta:    volatility={aggregates['delta_std_mean']:.4f} (mean of per-book delta std)"
        )

    # Show per-file breakdown
    console.print("\n[bold]Per-file results:[/bold]")
    table = Table()
    table.add_column("File", style="cyan")
    table.add_column("Words", justify="right")
    table.add_column("TTR", justify="right")
    table.add_column("STTR", justify="right")
    table.add_column("Delta Std", justify="right")

    for r in sorted(results, key=lambda x: x.ttr, reverse=True):
        sttr = f"{r.sttr:.4f}" if r.sttr else "-"
        delta_std = f"{r.delta_std:.4f}" if r.delta_std else "-"
        table.add_row(r.title[:40], f"{r.total_words:,}", f"{r.ttr:.4f}", sttr, delta_std)

    console.print(table)


def main():
    parser = argparse.ArgumentParser(
        description="Compute TTR metrics for text files in a directory"
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing .txt files",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output JSONL file (default: prints to console only)",
    )
    parser.add_argument(
        "--sttr-chunk-size",
        type=int,
        default=1000,
        help="Chunk size for STTR computation (default: 1000)",
    )

    args = parser.parse_args()

    # Validate input
    if not args.input_dir.exists():
        console.print(f"[red]Error: Directory not found: {args.input_dir}[/red]")
        sys.exit(1)

    if not args.input_dir.is_dir():
        console.print(f"[red]Error: Not a directory: {args.input_dir}[/red]")
        sys.exit(1)

    # Find text files
    txt_files = list(args.input_dir.glob("*.txt"))
    if not txt_files:
        console.print(f"[red]Error: No .txt files found in {args.input_dir}[/red]")
        sys.exit(1)

    console.print(f"[bold]Found {len(txt_files)} text files in {args.input_dir}[/bold]")

    # Initialize
    config = TTRConfig(sttr_chunk_size=args.sttr_chunk_size)
    tokenizer = VictorianTokenizer()
    calculator = TTRCalculator(config=config)
    aggregator = TTRAggregator()

    # Process files
    results: list[TTRResult] = []
    for file_path in txt_files:
        try:
            result = process_file(file_path, tokenizer, calculator)
            results.append(result)
            console.print(f"  [green]✓[/green] {file_path.name}")
        except Exception as e:
            console.print(f"  [red]✗[/red] {file_path.name}: {e}")

    if not results:
        console.print("[red]No files processed successfully[/red]")
        sys.exit(1)

    # Aggregate
    author = results[0].author if results else "unknown"
    aggregates = aggregator.aggregate(results, author)

    # Print results
    print_results(results, aggregates)

    # Write output if requested
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            for r in results:
                f.write(r.model_dump_json() + "\n")
            # Write aggregates as last line with marker
            agg_with_marker = {"_type": "aggregate", **aggregates}
            f.write(json.dumps(agg_with_marker) + "\n")
        console.print(f"\n[bold]Output written to:[/bold] {args.output}")


if __name__ == "__main__":
    main()
