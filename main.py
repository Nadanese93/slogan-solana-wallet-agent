#!/usr/bin/env python3
"""One-line slogan for a Solana wallet agent.

Writes exactly one slogan to entry.txt inside MAKEFUN_OUTPUT_DIR.
Deterministic: the same bytes on every run.
"""

import os
import sys

ENTRY = "Your SOL's designated driver."


class BlankError(ValueError):
    """Raised when the entry is empty or only whitespace."""


class MultiLineError(ValueError):
    """Raised when the entry spans more than one line."""


class LengthError(ValueError):
    """Raised when the entry is outside the 1-140 character range."""


class WordCountError(ValueError):
    """Raised when the entry exceeds 20 words."""


class ReadBackError(ValueError):
    """Raised when the written file does not match the entry bytes."""


def validate(text: str) -> None:
    if not text or not text.strip():
        raise BlankError("entry is blank or only whitespace")
    if "\n" in text or "\r" in text:
        raise MultiLineError("entry must be a single line")
    if len(text) < 1 or len(text) > 140:
        raise LengthError("entry must be 1-140 characters, got %d" % len(text))
    if len(text.split()) > 20:
        raise WordCountError("entry must be at most 20 words, got %d" % len(text.split()))


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 2
    validate(ENTRY)
    data = ENTRY.encode("utf-8")
    path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        if f.read() != data:
            raise ReadBackError("read-back verification failed: entry.txt bytes differ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
