"""Upgrading Part 1's MI schema must work with real pre-upgrade cache files."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np

from tools.qa_series import StaleDataError, require_part1_cache
from videos.ai.ai1 import compute


class MutualInformationCacheTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        directory = patch.object(compute, "DATA_DIR", Path(temp.name))
        directory.start()
        self.addCleanup(directory.stop)
        loaded = patch.object(compute, "_loaded", {})
        loaded.start()
        self.addCleanup(loaded.stop)
        signatures = patch.object(compute, "_loaded_signatures", {})
        signatures.start()
        self.addCleanup(signatures.stop)
        self.legacy = {"d": np.array([1, 1000]), "mi": np.array([.75, .00001]),
                       "floor": .000001, "slope": -.53, "intercept": -3}
        self.current = dict(self.legacy, schema_version=compute.CACHE_SCHEMAS["mi"],
                            shuffled_mi=np.array([.000001, -.000001]), fit_d=np.array([1000]))

    def test_normal_reader_recomputes_legacy_schema_under_its_cache_lock(self):
        compute._save("mi", self.legacy)
        calculate = Mock(return_value=self.current)
        with patch.object(compute, "ITEMS", {"mi": calculate}):
            result = compute.load("mi")
        calculate.assert_called_once_with()
        np.testing.assert_array_equal(result["shuffled_mi"], self.current["shuffled_mi"])
        self.assertTrue(compute.cache_current("mi"))

    def test_compute_cli_does_not_skip_a_legacy_completion_marker(self):
        compute._save("mi", self.legacy)
        calculate = Mock(return_value=self.current)
        with patch.object(compute, "ITEMS", {"mi": calculate}), \
                patch.object(sys, "argv", ["compute.py", "mi"]):
            compute.main()
        calculate.assert_called_once_with()
        self.assertTrue(compute.cache_current("mi"))

    def test_cached_only_rejects_legacy_data_without_computing_or_mutating_it(self):
        compute._save("mi", self.legacy)
        before = compute.path("mi").read_bytes()
        calculate = Mock(side_effect=AssertionError("cached-only must not compute"))
        with patch.object(compute, "ITEMS", {"mi": calculate}):
            with self.assertRaisesRegex(StaleDataError, "stale computed data: ai1/mi"):
                require_part1_cache(compute, "mi")
        calculate.assert_not_called()
        self.assertEqual(compute.path("mi").read_bytes(), before)

    def test_cached_only_accepts_current_schema_and_distinguishes_missing_data(self):
        compute._save("mi", self.current)
        require_part1_cache(compute, "mi")
        compute.path("mi").unlink()
        with self.assertRaisesRegex(FileNotFoundError, "QA needs computed data: ai1/mi"):
            require_part1_cache(compute, "mi")

    def test_schema_marker_without_array_archive_is_stale(self):
        compute.path("mi").write_text(json.dumps({"schema_version": compute.CACHE_SCHEMAS["mi"]}))
        self.assertFalse(compute.cache_current("mi"))
        with self.assertRaises(StaleDataError):
            require_part1_cache(compute, "mi")
