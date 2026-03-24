#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @spacemany2k38
# 2025-12-31

import curses
import textwrap
import sys
from typing import List


def _wrap_lines(raw_lines: List[str], width: int) -> List[str]:
    """Wrap lines to the given width, preserving blank lines."""
    wrapped: List[str] = []
    for line in raw_lines:
        if not line:
            wrapped.append("")
            continue
        if len(line) <= width:
            wrapped.append(line)
        else:
            wrapped.extend(textwrap.wrap(line, width=width, subsequent_indent=""))
    return wrapped


def _draw(stdscr, lines: List[str]) -> None:
    """Render lines with basic navigation help."""
    curses.start_color()
    try:
        curses.use_default_colors()
    except curses.error:
        pass
    try:
        curses.init_pair(1, curses.COLOR_YELLOW, -1)  # pale yellow for comments
    except curses.error:
        pass
    stdscr.bkgd(" ", curses.color_pair(0))
    curses.curs_set(0)
    stdscr.keypad(True)
    offset = 0

    while True:
        stdscr.erase()
        height, width = stdscr.getmaxyx()
        content_h = max(1, height - 1)
        end = min(len(lines), offset + content_h)

        # Clamp offset if window resized
        if offset > max(0, len(lines) - content_h):
            offset = max(0, len(lines) - content_h)
            end = min(len(lines), offset + content_h)

        for idx, line in enumerate(lines[offset:end]):
            # Base attributes
            attr = curses.A_DIM | curses.color_pair(0)

            stripped = line.lstrip()

            # Comments: pale yellow + dim
            if stripped.startswith("#"):
                attr = curses.A_DIM | curses.color_pair(1)

            # Bold for headers/titles (e.g., "USAGE:", "OPTIONS:", first line)
            elif stripped.endswith(":") and stripped == stripped.upper():
                attr = curses.A_BOLD | curses.color_pair(0)
            elif offset + idx == 0:
                attr = curses.A_BOLD | curses.color_pair(0)

            # Truncate if still too wide
            stdscr.addnstr(idx, 0, line, width - 1, attr)

        status = f"doc viewer  q:quit ↑/↓/PgUp/PgDn  {offset+1}-{end} / {len(lines)}"
        stdscr.addnstr(height - 1, 0, status.ljust(width), width - 1, curses.A_REVERSE)
        stdscr.refresh()

        ch = stdscr.getch()
        if ch in (ord("q"), ord("Q")):
            break
        elif ch in (curses.KEY_DOWN, ord("j")):
            if offset + content_h < len(lines):
                offset += 1
        elif ch in (curses.KEY_UP, ord("k")):
            if offset > 0:
                offset -= 1
        # Page down / space / ctrl+f-like
        elif ch in (curses.KEY_NPAGE, ord("f"), ord(" ")):
            if offset + content_h < len(lines):
                offset = min(len(lines) - content_h, offset + content_h)
        elif ch in (curses.KEY_PPAGE, ord("b")):  # Page up / ctrl+b-like
            if offset > 0:
                offset = max(0, offset - content_h)
        elif ch in (ord("d"),):  # half page down
            if offset + content_h < len(lines):
                offset = min(len(lines) - content_h, offset + max(1, content_h // 2))
        elif ch in (ord("u"),):  # half page up
            if offset > 0:
                offset = max(0, offset - max(1, content_h // 2))
        elif ch in (curses.KEY_HOME, ord("g")):
            offset = 0
        elif ch in (curses.KEY_END, ord("G")):
            offset = max(0, len(lines) - content_h)
        elif ch == curses.KEY_RESIZE:
            # Will redraw on next loop iteration
            continue


def view_text(text: str) -> int:
    """Display text with a curses pager when in a TTY; otherwise print plainly."""
    if not sys.stdout.isatty():
        print(text)
        return 0

    lines = text.splitlines()
    try:
        curses.wrapper(
            lambda stdscr: _draw(
                stdscr,
                _wrap_lines(lines, max(10, stdscr.getmaxyx()[1] - 1)),
            )
        )
        return 0
    except Exception:
        # Fallback to plain print if curses fails
        print(text)
        return 0

