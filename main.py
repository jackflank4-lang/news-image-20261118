#!/usr/bin/env python3
"""news-image-20261118 entry program.

Copies the repo's entry.png (a 1024x1024 poster summing up the world news
of Wednesday 18 November 2026) to $MAKEFUN_OUTPUT_DIR/entry.png.

Standard library only. No network access. Deterministic: the output bytes
are exactly the bytes of the bundled entry.png, so repeated runs produce
byte-identical output.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    destination = os.path.join(output_dir, "entry.png")

    if not os.path.isfile(source):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1

    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(source, destination)

    # Sanity check: the written output must be a 1024x1024 PNG within the
    # 1 MiB limit. (PNG header: 8-byte signature, then IHDR width/height
    # as big-endian uint32 at bytes 16..24.)
    size = os.path.getsize(destination)
    with open(destination, "rb") as fh:
        header = fh.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: output is not a PNG", file=sys.stderr)
        return 1
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if (width, height) != (1024, 1024):
        print(f"error: output is {width}x{height}, expected 1024x1024",
              file=sys.stderr)
        return 1
    if size > 1024 * 1024:
        print(f"error: output is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        return 1

    print(f"wrote {destination} ({size} bytes, 1024x1024 PNG)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
