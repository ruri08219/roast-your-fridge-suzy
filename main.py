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
  * No control characters — including DEL (0x7F) and non-printable
    Unicode (categories C*, Zl, Zp), so stray format characters cannot
    slip past a plain ord() < 0x20 check.
  * UTF-8 byte length is reported as a sanity check (ASCII entry, so
    bytes == chars here); the gate itself is character-based.
Any violation exits 1 and writes nothing.
"""

import os
import sys
import unicodedata

ENTRY = (
    "My fridge screams if the door stays open ten seconds, yet it has "
    "watched the same leftovers rot for three weeks without saying a word."
)

MAX_CHARS = 200


def _is_printable(ch: str) -> bool:
    """True if ch is a printable character.

    Rejects DEL (0x7F), all Unicode control/format/surrogate/private-use
    categories (C*), and line/paragraph separators (Zl, Zp). Ordinary
    spaces (Zs) are allowed.
    """
    cat = unicodedata.category(ch)
    return cat[0] != "C" and cat not in ("Zl", "Zp")


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
    bad = [ch for ch in entry if not _is_printable(ch)]
    if bad:
        print(
            "error: entry contains non-printable character U+%04X"
            % ord(bad[0]),
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    print(
        "wrote %s (%d chars, %d UTF-8 bytes)"
        % (path, len(ENTRY), len(ENTRY.encode("utf-8")))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
