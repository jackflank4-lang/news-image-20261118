#!/usr/bin/env python3
"""Copy the repo's entry.png to $MAKEFUN_OUTPUT_DIR/entry.png.

The program is deterministic: it copies the bundled image byte for byte,
so two runs always write identical output. It validates the PNG signature,
the 1024x1024 dimensions and the 1 MiB size limit before copying, verifies
the written file matches the source byte for byte, and prints a confirmation.
"""

import os
import shutil
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.png")
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        print(
            "entry.png is %d bytes, over the %d-byte limit" % (len(data), MAX_BYTES),
            file=sys.stderr,
        )
        return 1
    if data[:8] != PNG_SIGNATURE:
        print("entry.png is not a PNG (bad signature)", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        print(
            "entry.png is %dx%d, expected 1024x1024" % (width, height),
            file=sys.stderr,
        )
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, out_path)
    with open(out_path, "rb") as f:
        written = f.read()
    if written != data:
        print("output does not match entry.png", file=sys.stderr)
        return 1
    print("Wrote %s (%d bytes, 1024x1024 PNG)" % (out_path, len(data)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
