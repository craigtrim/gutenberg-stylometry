# Gutenberg Text Normalization

## Purpose
Prepare raw Project Gutenberg text files for stylometric analysis by deduplicating and stripping non-authorial content.

## Process

### 1. Deduplicate Works
Gutenberg often has multiple versions of the same work (different editions, OCR passes, transcription improvements). Select the best version using these heuristics:
- **Prefer larger files** - more complete transcriptions
- **Prefer newer IDs** - better OCR/encoding (ID is the number at end of filename)
- **Check encoding** - reject files with garbled characters

### 2. Remove Gutenberg Boilerplate
Strip standard Project Gutenberg content:
- **Header** - License info, transcriber credits, production notes (everything before the actual work)
- **Footer** - Donation requests, full license text, "End of Project Gutenberg" markers

Look for markers like:
- `*** START OF THE PROJECT GUTENBERG EBOOK`
- `*** END OF THE PROJECT GUTENBERG EBOOK`
- `***START OF THE PROJECT GUTENBERG EBOOK` (no space variant)

### 3. Remove Front/Back Matter
Skip content not written by the primary author:
- **Introductions** - Often written by editors or scholars
- **Prefaces by others** - "Introduction by [Other Person]"
- **Tables of Contents** - Navigation aids, not prose
- **Indices** - Reference material
- **Footnotes/Endnotes** - Often editorial additions
- **Illustrations lists** - "List of Illustrations"

### 4. Output
- One clean text file per unique work
- Pure authorial prose only
- Ready for stylometric feature extraction

## File Naming Convention
Output files should follow: `{author}-{title-slug}.txt`

## Source Location
Raw Gutenberg texts: `s3://craigtrim-resources/gutenberg/txt`
Use profile: `--profile dwc_s3`
