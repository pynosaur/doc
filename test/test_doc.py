#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @spacemany2k38
# 2025-12-31

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.doc_service import format_doc
from app.utils.doc_loader import load_doc


class TestDoc(unittest.TestCase):
    """Test cases for doc command."""

    def test_load_self_doc(self):
        """Ensure doc can load its own documentation."""
        data = load_doc("doc")
        self.assertEqual(data.get("NAME"), "doc")
        self.assertTrue(data.get("USAGE"), "USAGE section should exist")

    def test_format_contains_usage(self):
        """Formatted output should include usage heading and example."""
        data = load_doc("doc")
        rendered = format_doc("doc", data)
        self.assertIn("USAGE:", rendered)
        self.assertIn("doc <tool>", rendered)


if __name__ == "__main__":
    unittest.main()

