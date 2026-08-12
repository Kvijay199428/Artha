r"""
script-copier.py
Recursively scans arth source files,
reads every source file, and writes their contents into arth.md
with clear file-path headers and fenced code blocks.

Usage:
    python copy.py              # default source & output
    python copy.py --dry-run    # preview what would be copied
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Windows console encoding fix for emojis
import io
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── Configuration ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent

# Specify sources as relative string paths (can be files or directories)
SOURCE_PATHS = [
    "backend",
    "frontend",
    "docs",
]

SOURCE_FILE_PATHS = [
#    "agent.py",
]

# Directories to exclude from scanning
EXCLUDE_DIR_PATHS = [
    "node_modules",
    "dist",
    "build",
    ".git",
    "venv",
    ".venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".vscode",
    ".idea",
    "coverage",
]

# Files to exclude
EXCLUDE_FILE_NAMES = set([
    "deploy.py",
    "copy.py",
    "logs.py",
    "package-lock.json",
])

# Convert strings to resolved Paths internally
SOURCE_DIR = [BASE_DIR / p for p in SOURCE_PATHS] + [BASE_DIR / p for p in SOURCE_FILE_PATHS]
EXCLUDE_DIR_NAMES = set(EXCLUDE_DIR_PATHS)

OUTPUT_FILE = BASE_DIR / "artha.md"

# Map file extensions -> markdown code-fence language tags
EXTENSION_LANG = {
    ".java":       "java",
    ".py":         "python",
    ".js":         "javascript",
    ".ts":         "typescript",
    ".jsx":        "jsx",
    ".tsx":        "tsx",
    ".json":       "json",
    ".xml":        "xml",
    ".yaml":       "yaml",
    ".yml":        "yaml",
    ".properties": "properties",
    ".sql":        "sql",
    ".sh":         "bash",
    ".html":       "html",
    ".css":        "css",
    ".md":         "markdown",
    ".txt":        "text",
    ".ini":        "ini",
    ".toml":       "toml",
    ".conf":       "conf",
    ".svg":        "xml",
}

# Only include files with these extensions (or exactly these names like Dockerfile)
INCLUDE_EXTENSIONS = set(EXTENSION_LANG.keys())
INCLUDE_NAMES = {"Dockerfile", "Makefile"}

def collect_files(sources: list[Path]) -> list[tuple[Path, Path]]:
    """Recursively collect all script/source files, sorted by path."""
    files = []
    for source_dir in sources:
        if not source_dir.exists():
            print(f"Source not found: {source_dir}")
            continue

        if source_dir.is_file():
            if source_dir.name in EXCLUDE_FILE_NAMES:
                continue
            if source_dir.suffix.lower() not in INCLUDE_EXTENSIONS and source_dir.name not in INCLUDE_NAMES:
                continue
            files.append((source_dir, BASE_DIR))
            continue

        for root, dirs, filenames in os.walk(source_dir):
            # Prune excluded directories in-place so os.walk skips them
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in EXCLUDE_DIR_NAMES]
            for fname in filenames:
                fpath = Path(root) / fname
                if fname in EXCLUDE_FILE_NAMES:
                    continue
                if fpath.suffix.lower() not in INCLUDE_EXTENSIONS and fname not in INCLUDE_NAMES:
                    continue
                files.append((fpath, source_dir))
    files.sort(key=lambda x: x[0])
    return files


def lang_tag(filepath: Path) -> str:
    """Return the markdown language tag for a file extension."""
    return EXTENSION_LANG.get(filepath.suffix.lower(), "")


def build_markdown(files: list[tuple[Path, Path]]) -> str:
    """Build the full markdown string with all file contents."""
    lines: list[str] = []

    for fpath, source_dir in files:
        rel = fpath.relative_to(BASE_DIR)
        tag = lang_tag(fpath)

        try:
            content = fpath.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Skip files that aren't valid UTF-8 (likely binary)
            print(f"  Skipped (binary): {rel}")
            continue

        lines.append(f"```{tag}")
        lines.append(f"// File: {rel}")
        lines.append(content.rstrip())
        lines.append("```")
        lines.append("")  # blank line between files

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Copy source scripts into a markdown file.")
    parser.add_argument("--dry-run", action="store_true",
                        help="List files that would be copied without writing.")
    parser.add_argument("--source", type=Path, nargs="*", default=SOURCE_DIR,
                        help="Source directory to scan.")
    parser.add_argument("--output", type=Path, default=OUTPUT_FILE,
                        help="Output markdown file.")
    args = parser.parse_args()

    sources = args.source
    if not isinstance(sources, list):
        sources = [sources]
    output = args.output

    print(f"Scanning: {[str(s) for s in sources]}")
    files = collect_files(sources)
    print(f"Found {len(files)} file(s)\n")

    if not files:
        print("Nothing to copy.")
        return

    # Print summary table
    print(f"{'#':<4} {'Relative Path':<70} {'Size':>8}")
    print("-" * 84)
    total_bytes = 0
    for i, (f, src) in enumerate(files, 1):
        rel = f.relative_to(BASE_DIR)
        size = f.stat().st_size
        total_bytes += size
        print(f"{i:<4} {str(rel):<70} {size:>8}")
    print("-" * 84)
    print(f"     Total: {len(files)} files, {total_bytes:,} bytes\n")

    if args.dry_run:
        print("Dry run -- no file written.")
        return

    # Build markdown and write
    md = build_markdown(files)
    output.write_text(md, encoding="utf-8")
    print(f"Written to: {output}")
    print(f"   Output size: {output.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
