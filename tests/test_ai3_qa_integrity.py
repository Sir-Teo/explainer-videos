"""Part 3 integration contracts; temporary caches and tiny state only, no producers."""

import contextlib
import copy
import importlib
import io
import json
import os
import sys
import tempfile
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import numpy as np

from explainer.ai.cache import Cache
from tools import qa_series
from videos.ai.ai1 import compute as c1
from videos.ai.ai3 import compute


class AI3QAIntegrityTests(unittest.TestCase):
    def run_worker_fixture(self, directory, existing):
        """Run the real worker through a fake scene that reads via common.load."""
        from explainer.voiceover import VoiceoverScene

        events = []

        class UpgradingCache(Cache):
            def load(self, name):
                events.append(("upgrade-loader", name))
                raise AssertionError("cached-only entered upgrading loader")

        cache = UpgradingCache("ai3")
        cache.dir = Path(directory) / "data"
        cache.dir.mkdir()
        if existing:
            cache.path("words").write_text('{"legacy":true}')
        real_import = importlib.import_module

        def current(name):
            events.append(("schema-check", name))
            return False

        with patch.object(compute, "CACHE", cache), patch.object(compute, "cache_current", current):
            common = real_import("videos.ai.ai3.common")
            importlib.reload(common)

            class FixtureScene:
                def __init__(self, **kwargs):
                    pass

                def render(self):
                    common.load("words")

            def module(name, *args, **kwargs):
                if name == "videos.ai.ai3.manifest":
                    return SimpleNamespace(SCENES=[("qa_fixture", "Fixture", "QA fixture")])
                if name == "videos.ai.ai3.qa_fixture":
                    return SimpleNamespace(Fixture=FixtureScene)
                return real_import(name, *args, **kwargs)

            args = SimpleNamespace(video="ai3", lang="en", worker="Fixture", motion=False, cached_only=True)
            # The worker installs process-local instrumentation. Restore it here
            # because this test runs several workers in one process.
            with patch.object(qa_series, "OUT", Path(directory) / "out"), \
                    patch.object(qa_series, "fingerprint", return_value="fixture"), \
                    patch.object(importlib, "import_module", side_effect=module), \
                    patch.object(Cache, "load", Cache.load), patch.object(c1, "load", c1.load), \
                    patch.object(VoiceoverScene, "voiceover", VoiceoverScene.voiceover), \
                    patch.object(VoiceoverScene, "wait", VoiceoverScene.wait), patch.dict(os.environ), \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                code = qa_series.worker(args)
            result = json.loads((Path(directory) / "out/ai3/en/Fixture/result.json").read_text())
        importlib.reload(common)
        return code, result, events

    def test_actual_cached_only_worker_stops_missing_data_before_loader(self):
        with tempfile.TemporaryDirectory() as directory:
            code, result, events = self.run_worker_fixture(directory, False)
        self.assertEqual((code, result["status"]), (1, "missing-data"))
        self.assertEqual(events, [])
        self.assertIn("ai3/words", result["error"])

    def test_actual_cached_only_worker_stops_stale_data_before_upgrade(self):
        with tempfile.TemporaryDirectory() as directory:
            code, result, events = self.run_worker_fixture(directory, True)
            self.assertEqual((Path(directory) / "data/words.json").read_text(), '{"legacy":true}')
        self.assertEqual((code, result["status"]), (1, "stale-data"))
        self.assertEqual(events, [("schema-check", "words")])
        self.assertEqual(result["full_playback_review"], "pending")

    def test_book_words_consumes_current_artifact_despite_primed_part1_memo(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = compute.SchemaCache("ai3")
            cache.dir = Path(directory) / "ai3"
            source = Path(directory) / "ai1/train.txt"
            source.parent.mkdir()
            source.write_text("Beta, alpha BETA!")
            with patch.object(compute, "CACHE", cache), \
                    patch.object(c1, "_text_cache", {"train27": "old stale old"}), \
                    patch.object(c1, "text", side_effect=AssertionError("must not enter memoized data loader")):
                words, vocab, _, ids, _, source_digest = compute.book_words(with_source=True)
                self.assertEqual(words, c1.to27(source.read_text()).split())
                self.assertEqual(vocab, ["beta", "alpha"])
                self.assertEqual(ids.tolist(), [0, 1, 0])
                self.assertEqual(source_digest, compute.file_digest(source))
                lineage = compute.word_provenance("words", vocab, words, source_sha256=source_digest)
                source.write_text("Different same sized corpus")
                with self.assertRaises((ValueError, RuntimeError)):
                    cache.save("words", {"vocab": vocab, "provenance": lineage, "E": np.ones((2, 2))})
                self.assertFalse(cache.path("words").exists())

    def test_semantic_change_refreshes_a_previously_loaded_completed_item(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = compute.SchemaCache("ai3")
            cache.dir = Path(directory)
            cache.save("jl", {"value": "old", "array": np.array([1.0])})
            self.assertEqual(cache.load("jl")["value"], "old")
            producer = Mock(return_value={"value": "new", "array": np.array([2.0])})
            cache.items = {"jl": producer}
            with patch.object(compute, "JL_DELTA", compute.JL_DELTA / 2):
                self.assertFalse(cache.current("jl"))
                result = cache.load("jl")
                self.assertEqual(result["value"], "new")
                np.testing.assert_array_equal(result["array"], [2.0])
                self.assertTrue(cache.current("jl"))
            producer.assert_called_once_with()

    def test_completed_sgns_tracks_ordered_words_lineage_without_loading_data(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = compute.SchemaCache("ai3")
            cache.dir = Path(directory) / "ai3"
            source = Path(directory) / "ai1/train.txt"
            source.parent.mkdir()
            source.write_text("alpha beta alpha")
            vocab = ["alpha", "beta"]
            with patch.object(compute, "CACHE", cache):
                words_lineage = compute.word_provenance("words", vocab, source.read_text().split())
                cache.save("words", {"vocab": vocab, "provenance": words_lineage, "E": np.eye(2)})
                sgns_lineage = compute.word_provenance("sgns", vocab, source.read_text().split(),
                                                     seq=np.array([0, 1]), neg=np.array([0.5, 0.5]))
                cache.save("sgns", {"vocab": vocab, "provenance": sgns_lineage,
                                    "words_fingerprint": words_lineage["fingerprint"],
                                    "loss": np.array([0.5])})
                with patch.object(compute, "book_words", side_effect=AssertionError("must not load corpus")), \
                        patch.object(c1, "text", side_effect=AssertionError("must not compute corpus")):
                    self.assertTrue(compute.cache_current("words"))
                    self.assertTrue(compute.cache_current("sgns"))
                    with patch.object(compute, "SG_K", compute.SG_K + 1):
                        self.assertTrue(compute.cache_current("words"))
                        self.assertFalse(compute.cache_current("sgns"))
                    swapped = vocab[::-1]
                    replacement = compute.word_provenance("words", swapped, source.read_text().split())
                    cache.save("words", {"vocab": swapped, "provenance": replacement, "E": np.eye(2)})
                    self.assertTrue(compute.cache_current("words"))
                    self.assertFalse(compute.cache_current("sgns"))
                    cache.path("words").with_suffix(".npz").write_bytes(b"broken arrays")
                    self.assertFalse(compute.cache_current("words"))

    def test_all_revised_items_reject_legacy_completion_markers_without_producers(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = compute.SchemaCache("ai3")
            cache.dir = Path(directory)
            with patch.object(compute, "CACHE", cache), \
                    patch.object(compute, "book_words", side_effect=AssertionError("must not load corpus")):
                for name in compute.CACHE_SCHEMAS:
                    with self.subTest(name=name):
                        cache.path(name).write_text('{"legacy":true}')
                        self.assertFalse(compute.cache_current(name))
                        self.assertEqual(cache.path(name).read_text(), '{"legacy":true}')

    def test_cli_and_loader_share_the_same_stale_item_lock(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = compute.SchemaCache("ai3")
            cache.dir = Path(directory)
            cache.path("jl").write_text('{"legacy":true}')
            start = threading.Barrier(2)
            calls = []

            def producer():
                calls.append("computed")
                time.sleep(0.03)
                return {"value": "new"}

            cache.items = {"jl": producer}

            def cli():
                start.wait()
                cache.main(cache.items)

            def load():
                start.wait()
                return cache.load("jl")["value"]

            with patch.object(sys, "argv", ["compute", "jl"]), \
                    contextlib.redirect_stdout(io.StringIO()), ThreadPoolExecutor(2) as pool:
                a, b = pool.submit(cli), pool.submit(load)
                a.result(timeout=5)
                self.assertEqual(b.result(timeout=5), "new")
            self.assertEqual(calls, ["computed"])
            self.assertTrue(cache.current("jl"))

    def test_malformed_optimizer_checkpoint_cannot_partially_restore_live_state(self):
        import torch

        torch.set_num_threads(1)
        a, b = torch.nn.Embedding(2, 2), torch.nn.Embedding(2, 2)
        optimizer = torch.optim.Adam([*a.parameters(), *b.parameters()])
        generator = np.random.default_rng(10)
        before_a, before_b = a.weight.detach().clone(), b.weight.detach().clone()
        before_numpy, before_torch = copy.deepcopy(generator.bit_generator.state), torch.get_rng_state().clone()
        expected = {"epochs": 1, "batches_per_epoch": 1, "checks": [0, 1]}
        state = {"checkpoint_schema": 1, "contract": expected, "epoch": 0, "losses": [0.5],
                 "snap_steps": [0, 1], "snaps": [{}, {}], "E_in": {"weight": torch.ones((2, 2))},
                 "E_out": {"weight": torch.ones((2, 2))}, "opt": {"state": {}, "param_groups": []},
                 "g": np.random.default_rng(20).bit_generator.state,
                 "torch": torch.Generator().manual_seed(30).get_state()}
        with self.assertRaises(compute.IncompatibleSGNSCheckpoint):
            compute.restore_sgns_checkpoint(state, expected, a, b, optimizer, generator, torch)
        torch.testing.assert_close(a.weight, before_a)
        torch.testing.assert_close(b.weight, before_b)
        self.assertEqual(generator.bit_generator.state, before_numpy)
        self.assertTrue(torch.equal(torch.get_rng_state(), before_torch))
        self.assertEqual(optimizer.state_dict()["state"], {})


if __name__ == "__main__":
    unittest.main()
