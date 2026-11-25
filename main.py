#!/usr/bin/env python3
"""Roast Your Fridge — one-line fridge roast entry for make.fun.

Writes exactly one line (1-200 chars, no newline) roasting our fridge to
entry.txt in the output directory ($OUTPUT_DIR, default /output).

Entry (134 chars, one sentence):
    My fridge screams if the door stays open ten seconds, yet it has
    watched the same leftovers rot for three weeks without saying a word.

Gate rules enforced here, mirroring the competition gate:
  * UTF-8 text, 1 to 200 characters, not only whitespace.
  * Exactly one line (no newline characters inside the entry).
  * No control characters.
Any violation exits 1 and writes nothing.
"""

import os
import sys

ENTRY = (
    "My fridge screams if the door stays open ten seconds, yet it has "
    "watched the same leftovers rot for three weeks without saying a word."
)

MAX_CHARS = 200


def validate(entry: str) -> None:
    """Exit 1 with a message on the first violated gate rule."""
    if not entry or not entry.strip():
        print("error: entry is empty or whitespace only", file=sys.stderr)
        sys.exit(1)
    if len(entry) > MAX_CHARS:
        print(
            "error: entry is %d chars, over the %d limit" % (len(entry), MAX_CHARS),
            file=sys.stderr,
        )
        sys.exit(1)
    if "\n" in entry or "\r" in entry:
        print("error: entry must be a single line", file=sys.stderr)
        sys.exit(1)
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in entry):
        print("error: entry contains a control character", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    print("wrote %s (%d chars)" % (path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
