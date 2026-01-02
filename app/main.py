#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @spacemany2k38
# 2025-12-31

import sys
from pathlib import Path

# Allow running both as module and as script
if __name__ == "__main__" and __package__ is None:
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    __package__ = "app"

from app import __version__
from app.core.doc_service import get_formatted_doc
from app.core.pager import view_text


def print_help() -> None:
    """Print brief help for the doc tool (short, non-paged)."""
    print("doc - view tool documentation")
    print("\nUSAGE:")
    print("  doc <tool>")
    print("  doc --help")
    print("  doc --version")
    print("\nOPTIONS:")
    print("  -h, --help       Show this message")
    print("  -v, --version    Show version information")


def main() -> int:
    """Entry point for doc CLI."""
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print_help()
        return 0

    if args[0] in ("-v", "--version"):
        print(__version__)
        return 0

    app_name = args[0]
    rendered = get_formatted_doc(app_name)
    if not rendered:
        print(f"Documentation for '{app_name}' not found.", file=sys.stderr)
        return 1
    return view_text(rendered)


if __name__ == "__main__":
    sys.exit(main())

