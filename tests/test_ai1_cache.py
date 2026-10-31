"""Part 1 is read by the whole series: only publish complete computed results."""

import tempfile
import multiprocessing
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from videos.ai.ai1 import compute
from explainer.ai.cache import Cache


def load_shared_item(directory):
    cache = Cache("qa-test")
    cache.dir = Path(directory)

    def calculate():
        with (cache.dir / "calculations").open("a") as log:
            log.write("computed\n")
        time.sleep(0.15)  # let the other rendering process request the same item
        return {"value": 7, "x": np.arange(4)}

    cache.items = {"sample": calculate}
    value = cache.load("sample")
    return value["value"], value["x"].tolist()


class CacheTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = patch.object(compute, "DATA_DIR", Path(self.tmp.name) / "ai1")
        self.directory.start()
        self.addCleanup(self.directory.stop)
        self.loaded = patch.object(compute, "_loaded", {})
        self.loaded.start()
        self.addCleanup(self.loaded.stop)

    def test_failed_array_write_does_not_publish_completion_marker(self):
        with patch.object(np, "savez_compressed", side_effect=OSError("interrupted")):
            with self.assertRaises(OSError):
                compute._save("sample", {"value": 1, "x": np.arange(3)})
        self.assertFalse(compute.path("sample").exists())

    def test_replacing_result_invalidates_loaded_data_and_removes_old_arrays(self):
        compute._save("sample", {"value": 1, "x": np.arange(3)})
        np.testing.assert_array_equal(compute.load("sample")["x"], np.arange(3))
        compute._save("sample", {"value": 2})
        self.assertEqual(compute.load("sample"), {"value": 2})
        self.assertFalse(compute.path("sample").with_suffix(".npz").exists())

    def test_failed_replacement_cannot_mix_old_metadata_with_new_arrays(self):
        compute._save("sample", {"value": 1, "x": np.arange(3)})
        with patch.object(Path, "write_text", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                compute._save("sample", {"value": 2, "x": np.arange(5)})
        self.assertFalse(compute.path("sample").exists())

    def test_shared_cache_also_withdraws_marker_during_replacement(self):
        cache = Cache("qa-test")
        cache.dir = Path(self.tmp.name) / "shared"
        cache.save("sample", {"value": 1, "x": np.arange(3)})
        cache.load("sample")
        with patch.object(Path, "write_text", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                cache.save("sample", {"value": 2, "x": np.arange(5)})
        self.assertFalse(cache.path("sample").exists())
        self.assertNotIn("sample", cache._loaded)

    def test_scoreboard_counts_utf8_bytes_in_its_plain_text_baseline(self):
        text = "caf\u00e9"
        raw = {"n_chars": len(text), "n_bytes": len(text.encode("utf-8")), "passage_symbols": 4,
               "uniform": 2, "rows": [{"test": 2}, {"test": 1.5}], "best": 1, "best_bits": 1.5,
               "compressors": {"gzip": 2, "xz": 2, "bzip2": 2}}
        with patch.object(compute, "load", side_effect=lambda name: raw if name == "raw" else {"rows": []}):
            board = compute.compute_scoreboard()
        self.assertEqual(board["rows"][0]["bits"], 10.0)

    def test_two_rendering_processes_compute_a_missing_item_once(self):
        directory = Path(self.tmp.name) / "shared"
        directory.mkdir()
        with multiprocessing.get_context("spawn").Pool(2) as pool:
            values = pool.map(load_shared_item, [str(directory)] * 2)
        self.assertEqual(values, [(7, [0, 1, 2, 3])] * 2)
        self.assertEqual((directory / "calculations").read_text().splitlines(), ["computed"])

    def test_reader_refreshes_when_another_cache_instance_replaces_an_item(self):
        writer, reader = Cache("qa-test"), Cache("qa-test")
        writer.dir = reader.dir = Path(self.tmp.name) / "shared"
        writer.save("sample", {"value": 1, "x": np.arange(3)})
        self.assertEqual(reader.load("sample")["value"], 1)
        writer.save("sample", {"value": 2, "x": np.arange(5)})
        actual = reader.load("sample")
        self.assertEqual(actual["value"], 2)
        np.testing.assert_array_equal(actual["x"], np.arange(5))

    def test_part_one_reader_refreshes_after_an_external_replacement(self):
        compute._save("sample", {"value": 1})
        self.assertEqual(compute.load("sample")["value"], 1)
        writer = Cache("qa-test")
        writer.dir = compute.DATA_DIR
        writer.save("sample", {"value": 2, "x": np.arange(5)})
        actual = compute.load("sample")
        self.assertEqual(actual["value"], 2)
        np.testing.assert_array_equal(actual["x"], np.arange(5))


if __name__ == "__main__":
    unittest.main()
