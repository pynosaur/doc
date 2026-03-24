#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @spacemany2k38
# 2025-12-31

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union


def _candidate_paths(app_name: str) -> List[Path]:
    """Return possible locations for a tool's documentation file."""
    candidates = []

    # Nuitka/onefile bundle temporary directory
    if hasattr(sys, "_MEIPASS"):
        candidates.append(Path(sys._MEIPASS) / "doc" / f"{app_name}.yaml")

    # Repository-relative doc folder
    repo_doc = (
        Path(__file__).resolve().parent.parent.parent /
        "doc" /
        f"{app_name}.yaml"
    )
    candidates.append(repo_doc)

    # Current working directory doc folder (useful for local testing)
    candidates.append(Path.cwd() / "doc" / f"{app_name}.yaml")

    # Installed helpers via pget
    candidates.append(
        Path.home() / '.pget' / 'helpers' / app_name / 'doc' / f'{app_name}.yaml',
    )

    return candidates


def _parse_yaml_with_pyyaml(path: Path) -> Optional[Dict[str, Union[str, List[str]]]]:
    """Parse YAML using PyYAML if available."""
    try:
        import yaml  # type: ignore
    except ImportError:
        return None

    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict):
                return data
    except Exception:
        return None
    return None


def _parse_simple_yaml(content: str) -> Dict[str, Union[str, List[str]]]:
    """Parse a constrained YAML subset without external dependencies.

    Supports:
    - KEY: value
    - KEY: >
            multi-line block
    - KEY:
        - list items
    """
    data: Dict[str, Union[str, List[str]]] = {}
    lines = content.splitlines()

    current_key: Optional[str] = None
    mode: Optional[str] = None  # "list" or "block"
    buffer: List[str] = []

    def flush():
        nonlocal current_key, mode, buffer
        if current_key is None:
            return
        if mode == "list":
            data[current_key] = buffer[:]
        elif mode == "block":
            data[current_key] = "\n".join(buffer).strip()
        current_key = None
        mode = None
        buffer = []

    key_pattern = re.compile(r"^([A-Z_]+):\s*(.*)$")

    for raw_line in lines:
        line = raw_line.rstrip("\n")

        if not line.strip():
            if current_key and mode == "block":
                buffer.append("")
            continue

        match = key_pattern.match(line)
        if match:
            flush()
            current_key = match.group(1)
            remainder = match.group(2).strip()

            if remainder == "":
                mode = "list"
                buffer = []
            elif remainder.startswith(">"):
                mode = "block"
                buffer = []
            elif remainder in ("[]", "{}"):
                data[current_key] = []
                current_key = None
                mode = None
            else:
                # Simple scalar
                data[current_key] = remainder.strip('"')
                current_key = None
                mode = None
            continue

        if current_key:
            if mode == "list":
                item = line.strip()
                if item.startswith("-"):
                    value = item[1:].strip().strip('"')
                    buffer.append(value)
            elif mode == "block":
                buffer.append(line.strip())

    flush()
    return data


def parse_doc_file(path: Path) -> Dict[str, Union[str, List[str]]]:
    """Parse a documentation YAML file."""
    if not path.exists():
        return {}

    # Try PyYAML first (if installed)
    parsed = _parse_yaml_with_pyyaml(path)
    if parsed is not None:
        return parsed

    # Fallback simple parser
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return {}

    return _parse_simple_yaml(content)


def load_doc(app_name: str) -> Dict[str, Union[str, List[str]]]:
    """Load documentation for the given app name.

    Search order:
    1. Nuitka bundle (if applicable)
    2. Repository doc/ folder
    3. Current working directory doc/ folder
    4. Installed helper docs (~/.pget/helpers/<app>/doc/<app>.yaml)
    """
    for candidate in _candidate_paths(app_name):
        if candidate.exists():
            doc = parse_doc_file(candidate)
            if doc:
                return doc
    return {}

