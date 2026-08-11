#!/usr/bin/env python3

import re
import sys
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

DEFAULT_BASE_DIR = Path.cwd()


# ============================================================
# Helpers
# ============================================================

def normalize_destination(path_text: str, base_dir: Path) -> Path:
    """
    Convert an agent-generated absolute path into a path
    inside the current project.

    Example:

    /mnt/agents/output/gst-billing/backend/app/core/config.py

    becomes:

    /root/arth/backend/app/core/config.py
    """

    path_text = path_text.strip().replace("\\", "/")

    # Known agent output root
    marker = "/gst-billing/"

    if marker in path_text:
        relative_path = path_text.split(marker, 1)[1]
        return base_dir / relative_path

    # If agent already gives a relative path
    path = Path(path_text)

    if not path.is_absolute():
        return base_dir / path

    # Fallback: preserve absolute path
    return path


def extract_triple_quoted_strings(text: str):
    """
    Find assignments such as:

        config_py = '''content'''

    or:

        config_py = \"\"\"content\"\"\"

    Returns:
        [
            {
                "variable": "config_py",
                "content": "...",
                "start": ...,
                "end": ...
            }
        ]
    """

    pattern = re.compile(
        r"""
        (?P<variable>
            [A-Za-z_][A-Za-z0-9_]*
        )
        \s*=\s*
        (?P<quote>
            '{3}|"{3}
        )
        (?P<content>.*?)
        (?P=quote)
        """,
        re.DOTALL | re.VERBOSE,
    )

    results = []

    for match in pattern.finditer(text):
        results.append(
            {
                "variable": match.group("variable"),
                "content": match.group("content"),
                "start": match.start(),
                "end": match.end(),
            }
        )

    return results


def extract_open_destinations(text: str):
    """
    Find:

        with open("/some/path/file.py", "w") as f:

    Returns destination information in order of appearance.
    """

    pattern = re.compile(
        r"""
        with
        \s+
        open
        \s*
        \(
        \s*
        (?P<quote>['"])
        (?P<path>.*?)
        (?P=quote)
        \s*
        ,
        \s*
        (?P<mode_quote>['"])
        (?P<mode>[wax+]+)
        (?P=mode_quote)
        .*?
        \)
        \s*
        as
        \s+
        (?P<handle>[A-Za-z_][A-Za-z0-9_]*) 
        \s*
        :
        """,
        re.DOTALL | re.VERBOSE,
    )

    return [
        {
            "path": match.group("path"),
            "mode": match.group("mode"),
            "handle": match.group("handle"),
            "start": match.start(),
            "end": match.end(),
        }
        for match in pattern.finditer(text)
    ]


def find_variable_before_position(variables, position):
    """
    Find the most recent triple-quoted variable assignment
    before a with-open() statement.

    Example:

        config_py = '''...'''

        with open(".../config.py", "w") as f:

    will associate config_py with config.py.
    """

    candidates = [
        variable
        for variable in variables
        if variable["start"] < position
    ]

    if not candidates:
        return None

    # Closest assignment before with open()
    return max(candidates, key=lambda item: item["start"])


def clean_content(content: str):
    """
    Clean extracted content without modifying the actual Python code.
    """

    # Remove one leading newline commonly produced by:
    #
    # config_py = '''
    # from ...
    #
    if content.startswith("\n"):
        content = content[1:]

    # Remove one trailing newline caused by:
    #
    # '''
    #
    if content.endswith("\n"):
        content = content[:-1]

    return content


def write_file(destination: Path, content: str):
    """
    Create parent directories and write the file.
    """

    destination.parent.mkdir(parents=True, exist_ok=True)

    destination.write_text(
        content,
        encoding="utf-8",
    )


# ============================================================
# Main extraction engine
# ============================================================

def process_agent_text(text: str, base_dir: Path):
    variables = extract_triple_quoted_strings(text)
    destinations = extract_open_destinations(text)

    if not destinations:
        print("\n[WARNING] No 'with open(...)' destinations found.")
        return 0, 0

    print()
    print("=" * 70)
    print("AGENT FILE EXTRACTOR")
    print("=" * 70)

    created = 0
    skipped = 0

    for destination_info in destinations:

        raw_path = destination_info["path"]

        destination = normalize_destination(
            raw_path,
            base_dir,
        )

        variable = find_variable_before_position(
            variables,
            destination_info["start"],
        )

        print()
        print(f"[FOUND] Destination:")
        print(f"        {raw_path}")

        if variable is None:
            print("[SKIP]  Could not find triple-quoted variable assignment.")
            skipped += 1
            continue

        variable_name = variable["variable"]

        print(f"[FOUND] Variable:")
        print(f"        {variable_name}")

        content = clean_content(
            variable["content"]
        )

        if not content.strip():
            print("[SKIP]  Extracted content is empty.")
            skipped += 1
            continue

        # Respect append mode if an agent uses "a".
        if destination_info["mode"] == "a":
            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with destination.open(
                "a",
                encoding="utf-8",
            ) as f:
                f.write(content)

            print(f"[APPEND] {destination}")

        else:
            write_file(
                destination,
                content,
            )

            print(f"[WRITE]  {destination}")

        print(
            f"         {len(content.splitlines())} lines"
        )

        created += 1

    print()
    print("=" * 70)
    print(f"FILES CREATED/UPDATED : {created}")
    print(f"FILES SKIPPED         : {skipped}")
    print("=" * 70)

    return created, skipped


# ============================================================
# Interactive mode
# ============================================================

def interactive_mode(base_dir: Path):

    print("=" * 70)
    print("AGENT GENERATED FILE EXTRACTOR")
    print("=" * 70)
    print()
    print(f"Base directory:")
    print(f"  {base_dir}")
    print()
    print("Paste the complete agent-generated script below.")
    print()
    print("When finished:")
    print("  Linux/Termux : press Ctrl+D")
    print("  Windows      : press Ctrl+Z then Enter")
    print()
    print("-" * 70)

    try:
        text = sys.stdin.read()
    except KeyboardInterrupt:
        print("\nCancelled.")
        return

    if not text.strip():
        print("\n[ERROR] No text was pasted.")
        return

    process_agent_text(
        text,
        base_dir,
    )


# ============================================================
# Command-line entry point
# ============================================================

def main():

    base_dir = DEFAULT_BASE_DIR

    # Optional:
    #
    # python agent_file_extractor.py /some/project
    #
    if len(sys.argv) >= 2:
        base_dir = Path(sys.argv[1]).expanduser()

    interactive_mode(
        base_dir.resolve()
    )


if __name__ == "__main__":
    main()
