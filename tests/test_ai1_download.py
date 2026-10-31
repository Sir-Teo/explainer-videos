"""A failed source download must never become a completed corpus input."""

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from videos.ai.ai1 import compute


class CorpusDownloadTests(unittest.TestCase):
    def test_http_error_does_not_cache_error_page_or_retry_permanent_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "book.txt"

            def fail(command):
                self.assertIn("-f", command)
                Path(str(target) + ".part").write_text("<html>Not Found</html>")
                return SimpleNamespace(returncode=22)

            with patch.object(compute.subprocess, "run", side_effect=fail) as run:
                with self.assertRaisesRegex(RuntimeError, "HTTP error"):
                    compute._download("https://example.invalid/book", target)
            self.assertEqual(run.call_count, 1)
            self.assertFalse(target.exists())
            self.assertFalse(Path(str(target) + ".part").exists())

    def test_success_is_published_only_after_nonempty_transfer(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "book.txt"

            def transfer(command):
                Path(str(target) + ".part").write_text("A complete book")
                return SimpleNamespace(returncode=0)

            with patch.object(compute.subprocess, "run", side_effect=transfer):
                self.assertEqual(compute._download("https://example.invalid/book", target), target)
            self.assertEqual(target.read_text(), "A complete book")
            self.assertFalse(Path(str(target) + ".part").exists())

    def test_empty_success_does_not_publish_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "book.txt"

            def empty(command):
                Path(str(target) + ".part").touch()
                return SimpleNamespace(returncode=0)

            with patch.object(compute.subprocess, "run", side_effect=empty), patch.object(compute.time, "sleep"):
                with self.assertRaisesRegex(RuntimeError, "could not download"):
                    compute._download("https://example.invalid/book", target)
            self.assertFalse(target.exists())
            self.assertFalse(Path(str(target) + ".part").exists())
