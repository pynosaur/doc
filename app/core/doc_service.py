#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @spacemany2k38
# 2025-12-31

from typing import Dict, List, Union

from app.utils.doc_loader import load_doc

DocData = Dict[str, Union[str, List[str]]]


def _section(title: str, body: Union[str, List[str], None]) -> List[str]:
    """Render a section with spacing similar to man pages."""
    if not body:
        return []

    lines: List[str] = []
    lines.append(f"{title}")
    if isinstance(body, list):
        for item in body:
            # Indent list items
            lines.append(f"    {item}")
    else:
        lines.append(f"    {body}")
    lines.append("")  # blank line after section
    return lines


def format_doc(app_name: str, doc: DocData) -> str:
    """Return formatted documentation text for a tool."""
    name = str(doc.get("NAME", app_name))
    description = str(doc.get("DESCRIPTION", "")).strip()
    version = str(doc.get("VERSION", "")).strip()
    usage = doc.get("USAGE", [])
    options = doc.get("OPTIONS", [])
    examples = doc.get("EXAMPLES", [])
    output = doc.get("OUTPUT", None)
    notes = doc.get("NOTES", [])
    author = doc.get("AUTHOR", "")
    date = doc.get("DATE", "")

    lines: List[str] = []

    # NAME
    header = f"{name}"
    if description:
        header = f"{name} - {description}"
    lines.append(header)
    if version:
        lines.append(f"Version: {version}")
    lines.append("")

    # Sections
    lines.extend(_section("USAGE:", usage))
    lines.extend(_section("OPTIONS:", options))
    lines.extend(_section("EXAMPLES:", examples))
    lines.extend(_section("OUTPUT:", output))
    lines.extend(_section("NOTES:", notes))

    # INFO footer
    if author or date:
        lines.append("INFO:")
        if author:
            lines.append(f"    Author: {author}")
        if date:
            lines.append(f"    Date: {date}")
        lines.append("")

    # Trim trailing blank lines
    while lines and not lines[-1].strip():
        lines.pop()

    return "\n".join(lines)


def get_formatted_doc(app_name: str) -> str:
    """Load and format documentation for an app. Returns empty string if missing."""
    doc = load_doc(app_name)
    if not doc:
        return ""
    return format_doc(app_name, doc)

