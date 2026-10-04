"""Align Sofle binding columns, preserving row order and all binding text."""

import argparse
import re
from pathlib import Path


def format_bindings(match):
    indent = match["indent"] + "    "
    rows = []
    for line in match["body"].splitlines():
        code, marker, comment = line.partition("//")
        cells = re.split(r"\s+(?=&[A-Za-z_])", code.strip()) if code.strip() else []
        if cells and (not code.lstrip().startswith("&") or "/*" in code or "*/" in code):
            raise ValueError("Binding rows must contain behavior references; block comments and directives are unsupported")
        rows.append((cells, marker + comment))

    columns = max((len(cells) for cells, _ in rows), default=0)
    widths = [
        max(len(cells[i]) for cells, _ in rows if i < len(cells))
        for i in range(columns)
    ]
    lines = []
    for cells, comment in rows:
        # Separate the six left keys, center control, and six right keys.
        code = "".join(
            cell.ljust(widths[i]) + ("      " if i in (5, 6) else "   ")
            for i, cell in enumerate(cells)
        ).rstrip()
        if comment:
            code += ("  " if code else "") + comment
        lines.append(indent + code if code else "")
    return match["opening"] + "\n".join(lines) + "\n" + match["indent"] + ">;"


def format_keymap(source):
    # Only multiline key bindings are formatted; encoder bindings and other
    # Devicetree properties remain untouched.
    result = re.sub(
        r"(?P<opening>^(?P<indent>[ \t]*)bindings\s*=\s*<\n)"
        r"(?P<body>.*?)\n[ \t]*>;",
        format_bindings,
        source,
        flags=re.MULTILINE | re.DOTALL,
    )
    if re.findall(r"\S+", source) != re.findall(r"\S+", result):
        raise ValueError("Formatting would change non-whitespace tokens; file was not written")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("keymap", type=Path)
    args = parser.parse_args()
    source = args.keymap.read_text()
    result = format_keymap(source)
    if result != source:
        args.keymap.write_text(result)
    print(f"Formatted {args.keymap}")


if __name__ == "__main__":
    main()
