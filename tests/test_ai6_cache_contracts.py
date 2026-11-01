"""Synthetic cache/state-machine tests; no Part6 producer, default corpus or model."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

from videos.ai.ai6 import contracts
from videos.ai.ai6.cache_contract import CacheValidationError, SchemaCache, canonical


def pages_fixture():
    book = np.tile(np.array(contracts.BOOK_IDS), 4)
    y = np.isin(book, contracts.BOOK_IDS[2:]).astype(int)
    n = len(y)
    test = np.arange(n) % 3 == 0
    X = np.zeros((n, 70)); X[:, 0] = np.arange(n) + 1; X[:, 1] = np.arange(n) % 5
    example = int(np.flatnonzero(test)[0])
    return dict(vocab=["the", "not"] + [f"word{i}" for i in range(68)], X=X, X2=X[:, :2].copy(),
                y=y, book=book, test=test, plot=["the", "not"], example="the not",
                example_label=int(y[example]), example_i=example, n_pages=n,
                n_austen=int((y == 0).sum()), n_dickens=int((y == 1).sum()),
                titles={n: str(n) for n in contracts.BOOK_IDS}, protocol=contracts.benchmark_protocol())


def public_book_fixture(n):
    return (f"Project Gutenberg eBook #{n}\n*** START OF THE PROJECT GUTENBERG EBOOK TEST ***\n"
            + "the not " * 5000 + "\n*** END OF THE PROJECT GUTENBERG EBOOK TEST ***\n")


def fold_piece():
    a = np.linspace(.6, .9, 10)
    return dict(cv=float(a.mean()), sd=float(a.std(ddof=1)), lo=float(a.min()), hi=float(a.max()),
                folds=a.tolist(), held=.75)


def board_fixture():
    rows = [dict(key=key, name=key, **{str(nf): fold_piece() for nf in features})
            for key, features in contracts.BOARD_CASES.items()]
    f = np.tile(np.arange(10), 2)
    return dict(rows=rows, n=20, folds=10, fold_ids=f,
                evaluation=dict(fold_sha256=canonical(f.tolist()), seed=2025,
                                method_feature_cases=[f"{key}_{nf}" for key, fs in contracts.BOARD_CASES.items() for nf in fs],
                                scoring="unweighted fold mean and sample standard deviation of accuracy",
                                heldout="separate fixed 30-percent page split", protocol=contracts.benchmark_protocol()))


class CacheTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.cache = SchemaCache("ai6")
        self.cache.dir = self.base / "cache/ai6"
        self.books = self.base / "cache/ai1/books"
        self.books.mkdir(parents=True)
        for n in contracts.BOOK_IDS:
            (self.books / f"{n}.txt").write_text(public_book_fixture(n))
        (self.books.parent / "train.txt").write_text("tiny training-only corpus\n")
        def forbidden():
            raise AssertionError("An unprovided/default numerical producer was invoked")
        self.items = {name: forbidden for name in contracts.REQUIRED}
        self.items.update(pages=pages_fixture, board=board_fixture)
        self.cache.bind(self.items)

    def publish_pages(self):
        self.cache._produce("pages", pages_fixture)
        self.assertTrue(self.cache.current("pages"), self.cache.status("pages"))

    def preserved(self, name):
        return list((self.cache.dir / "preserved").glob(f"*/{name}"))

    def test_missing_pure_validation_never_produces_or_creates_cache_directory(self):
        with patch.object(self.cache, "_produce", side_effect=AssertionError("producer")):
            self.assertEqual(self.cache.status("pages")["status"], "missing")
            self.assertFalse(self.cache.current("pages"))
        self.assertFalse(self.cache.dir.exists())

    def test_cached_only_missing_load_fails_before_producer_lock_or_directory(self):
        with patch.dict("os.environ", {"EXPLAINER_CACHED_ONLY": "1"}), \
             patch.object(self.cache, "_produce", side_effect=AssertionError("producer")):
            with self.assertRaisesRegex(CacheValidationError, "missing"):
                self.cache.load("pages")
        self.assertFalse(self.cache.dir.exists())

    def test_registered_normal_load_retains_downstream_first_use(self):
        value = self.cache.load("pages")
        self.assertEqual(value["X"].shape, (20, 70))
        self.assertTrue(self.cache.current("pages"))
        with patch.object(self.cache, "_produce", side_effect=AssertionError("recompute")):
            self.assertEqual(self.cache.load("pages")["protocol"], contracts.benchmark_protocol())

    def test_missing_corpus_never_calls_registered_numerical_producer(self):
        (self.books / "1342.txt").unlink()
        with patch.object(self.cache, "save", side_effect=AssertionError("save")):
            with self.assertRaisesRegex(CacheValidationError, "prepare Part1 corpus explicitly"):
                self.cache._produce("pages", lambda: self.fail("producer ran"))

    def test_direct_save_cannot_attest_an_unobserved_legacy_generation(self):
        with self.assertRaisesRegex(CacheValidationError, "observed producer"):
            self.cache.save("pages", pages_fixture())
        self.assertFalse(self.cache.dir.exists())

    def test_legacy_cached_only_is_explicit_and_bytes_untouched(self):
        self.cache.dir.mkdir()
        p = self.cache.path("pages"); p.write_bytes(b'{"legacy":true}')
        before = p.read_bytes()
        self.assertEqual(self.cache.status("pages")["status"], "legacy")
        with patch.dict("os.environ", {"EXPLAINER_CACHED_ONLY": "1"}), \
             patch.object(self.cache, "_produce", side_effect=AssertionError("producer")):
            with self.assertRaisesRegex(CacheValidationError, "legacy"):
                self.cache.load("pages")
        self.assertEqual(p.read_bytes(), before)
        self.assertFalse((self.cache.dir / "preserved").exists())

    def test_legacy_replacement_retains_independent_original_bytes(self):
        self.cache.dir.mkdir(); p = self.cache.path("pages"); p.write_bytes(b'{"legacy":true}')
        old = p.read_bytes()
        self.publish_pages()
        copies = self.preserved("pages.json")
        self.assertEqual(len(copies), 1)
        self.assertEqual(copies[0].read_bytes(), old)
        self.assertNotEqual(copies[0].stat().st_ino, p.stat().st_ino)

    def test_failed_generation_preserves_old_completed_bytes(self):
        self.cache.dir.mkdir(); p = self.cache.path("pages"); p.write_bytes(b'{"legacy":true}')
        def fail():
            raise RuntimeError("interrupted before output")
        with self.assertRaisesRegex(RuntimeError, "interrupted"):
            self.cache._produce("pages", fail)
        self.assertEqual(p.read_bytes(), b'{"legacy":true}')

    def test_source_change_during_generation_refuses_publication(self):
        original = self.cache._source_hashes()
        def producer():
            self.cache._source_hashes = lambda: dict(original, changed="new source")
            return pages_fixture()
        with self.assertRaisesRegex(CacheValidationError, "sources changed|identity changed"):
            self.cache._produce("pages", producer)
        self.assertFalse(self.cache.path("pages").exists())

    def test_input_change_during_generation_refuses_publication(self):
        def producer():
            (self.books / "158.txt").write_text("changed while producing")
            return pages_fixture()
        with self.assertRaisesRegex(CacheValidationError, "identity changed|implausibly sized"):
            self.cache._produce("pages", producer)
        self.assertFalse(self.cache.path("pages").exists())

    def test_runtime_and_corpus_change_make_completed_item_stale(self):
        self.publish_pages()
        with patch.object(contracts, "runtime_identity", return_value={"numpy": "other version"}):
            self.assertFalse(self.cache.current("pages"))
        self.assertTrue(self.cache.current("pages"))
        (self.books / "98.txt").write_text("changed")
        self.assertFalse(self.cache.current("pages"))

    def test_missing_required_npz_is_not_a_json_only_success(self):
        self.publish_pages(); self.cache.path("pages").with_suffix(".npz").unlink()
        status = self.cache.status("pages")
        self.assertEqual(status["status"], "malformed")
        self.assertIn("required NPZ", status["reason"])

    def test_tampered_json_and_arrays_are_rejected(self):
        self.publish_pages(); p = self.cache.path("pages")
        raw = p.read_bytes(); d = json.loads(raw); d["example"] = "changed"
        p.write_text(json.dumps(d)); self.assertFalse(self.cache.current("pages")); p.write_bytes(raw)
        z = p.with_suffix(".npz")
        with np.load(z, allow_pickle=False) as archive:
            arrays = {key: archive[key] for key in archive.files}
        arrays["X"][0, 0] += 1
        np.savez_compressed(z, **arrays)
        self.assertFalse(self.cache.current("pages"))

    def test_malformed_schema_types_and_versions_do_not_pass(self):
        self.publish_pages(); p = self.cache.path("pages"); raw = json.loads(p.read_text())
        for value in (True, 1.0, "1", 999):
            d = copy.deepcopy(raw); d["_cache"]["schema_version"] = value; p.write_text(json.dumps(d))
            self.assertFalse(self.cache.current("pages"), value)

    def test_partial_survives_interruption_and_finish_until_atomic_publication(self):
        self.publish_pages()
        params = dict(folds=10, seed=2025, v=2)
        def interrupt():
            part = self.cache.partial("board", params)
            part["ls_2"] = fold_piece(); part.finish()
            self.assertTrue(part.path.exists())
            raise RuntimeError("interrupted")
        with self.assertRaises(RuntimeError):
            self.cache._produce("board", interrupt)
        partial = self.cache.dir / "board.partial.json"; raw = partial.read_bytes()
        def resume():
            part = self.cache.partial("board", params)
            self.assertEqual(part["ls_2"], fold_piece())
            return board_fixture()
        self.cache._produce("board", resume)
        self.assertTrue(self.cache.current("board"), self.cache.status("board"))
        self.assertFalse(partial.exists())
        self.assertIn(raw, [p.read_bytes() for p in self.preserved("board.partial.json")])

    def test_legacy_partial_is_preserved_and_never_reused(self):
        self.publish_pages(); p = self.cache.dir / "board.partial.json"
        p.write_text(json.dumps(dict(params=dict(folds=10, seed=2025, v=1), done={"ls_2": fold_piece()})))
        raw = p.read_bytes()
        def fresh():
            part = self.cache.partial("board", dict(folds=10, seed=2025, v=2))
            self.assertNotIn("ls_2", part)
            return board_fixture()
        self.cache._produce("board", fresh)
        self.assertIn(raw, [p.read_bytes() for p in self.preserved("board.partial.json")])

    def test_resume_rejects_changed_pages_even_when_fold_seed_and_params_same(self):
        self.publish_pages(); params = dict(folds=10, seed=2025)
        def interrupt():
            self.cache.partial("board", params)["ls_2"] = fold_piece()
            raise RuntimeError("stop")
        with self.assertRaises(RuntimeError):
            self.cache._produce("board", interrupt)
        raw = (self.cache.dir / "board.partial.json").read_bytes()
        (self.books / "46.txt").write_text(public_book_fixture(46) + "new metadata")
        self.cache._produce("pages", pages_fixture)
        def fresh():
            part = self.cache.partial("board", params)
            self.assertNotIn("ls_2", part)
            return board_fixture()
        self.cache._produce("board", fresh)
        self.assertIn(raw, [p.read_bytes() for p in self.preserved("board.partial.json")])

    def test_force_does_not_reuse_compatible_expensive_partial(self):
        self.publish_pages(); params = dict(folds=10)
        def interrupt():
            self.cache.partial("board", params)["ls_2"] = fold_piece()
            raise RuntimeError("stop")
        with self.assertRaises(RuntimeError):
            self.cache._produce("board", interrupt)
        def forced():
            self.assertNotIn("ls_2", self.cache.partial("board", params))
            return board_fixture()
        self.cache._produce("board", forced, force=True)
        self.assertTrue(self.cache.current("board"))

    def test_partial_wrong_shape_or_nonfinite_is_not_checkpointed(self):
        self.publish_pages()
        def producer():
            part = self.cache.partial("board", {})
            for change in ({"folds": [1.]}, {"cv": float("nan")}, {"held": 2.}):
                piece = dict(fold_piece(), **change)
                with self.assertRaises((CacheValidationError, ValueError)):
                    part["ls_2"] = piece
            self.assertNotIn("ls_2", part)
            return board_fixture()
        self.cache._produce("board", producer)

    def test_invalid_new_output_does_not_replace_current_item(self):
        self.publish_pages(); p = self.cache.path("pages"); old = p.read_bytes()
        bad = pages_fixture(); bad["X2"] = bad["X2"][:, :1]
        with self.assertRaisesRegex(CacheValidationError, "malformed producer output"):
            self.cache._produce("pages", lambda: bad)
        self.assertEqual(p.read_bytes(), old)
        self.assertTrue(self.cache.current("pages"))

    def test_changed_prerequisite_invalidates_dependent_board(self):
        self.publish_pages(); self.cache._produce("board", board_fixture)
        self.assertTrue(self.cache.current("board"))
        (self.books / "1342.txt").write_text("changed upstream book")
        with patch.object(self.cache, "_produce", side_effect=AssertionError("producer")):
            self.assertFalse(self.cache.current("board"))

    def test_explicit_preparation_fetches_only_missing_book_preserving_corpus_splits(self):
        for name in ("train.txt", "valid.txt", "corpus.json"):
            (self.books.parent / name).write_bytes(("existing " + name).encode())
        protected = {p: p.read_bytes() for p in self.books.parent.iterdir() if p.is_file()}
        missing = self.books / "158.txt"; missing.unlink(); calls = []
        def download(url, target):
            calls.append((url, target))
            self.assertNotEqual(target, missing)
            target.write_text(public_book_fixture(158))
            return target
        result = self.cache.prepare_inputs(["board"], downloader=download)
        self.assertEqual(len(calls), 1)
        self.assertEqual(result[0]["book_id"], 158)
        self.assertIn("/158/pg158.txt", calls[0][0])
        for p, content in protected.items():
            self.assertEqual(p.read_bytes(), content)
        self.assertEqual(missing.read_text(), public_book_fixture(158))

    def test_failed_download_validation_never_publishes_bad_book(self):
        missing = self.books / "158.txt"; missing.unlink()
        invalid = ["<html>error</html>" * 5000, public_book_fixture(1342),
                   public_book_fixture(158).split("*** END OF")[0],
                   "Project Gutenberg eBook #158\n*** START OF THE PROJECT GUTENBERG EBOOK TEST ***\ntiny\n"
                   "*** END OF THE PROJECT GUTENBERG EBOOK TEST ***\n"]
        for body in invalid:
            with self.subTest(length=len(body)):
                def download(url, target):
                    target.write_text(body)
                    return target
                with self.assertRaises(CacheValidationError):
                    self.cache.prepare_inputs(["pages"], downloader=download)
                self.assertFalse(missing.exists())

    def test_nonempty_invalid_existing_book_is_not_silently_replaced(self):
        p = self.books / "158.txt"; p.write_bytes(b"legacy invalid bytes")
        with self.assertRaises(CacheValidationError):
            self.cache.prepare_inputs(["pages"], downloader=lambda *_: self.fail("network"))
        self.assertEqual(p.read_bytes(), b"legacy invalid bytes")

    def test_empty_book_original_is_preserved_before_explicit_replacement(self):
        p = self.books / "158.txt"; p.write_bytes(b"")
        def download(url, target):
            target.write_text(public_book_fixture(158))
        self.cache.prepare_inputs(["pages"], downloader=download)
        self.assertEqual([p.read_bytes() for p in self.preserved("158.txt")], [b""])

    def test_ordinary_autoload_does_not_prepare_or_download_missing_books(self):
        (self.books / "158.txt").unlink()
        with patch.object(self.cache, "prepare_inputs", side_effect=AssertionError("download")):
            with self.assertRaisesRegex(CacheValidationError, "prepare Part1 corpus explicitly"):
                self.cache.load("pages")

    def test_cached_only_preparation_and_explicit_generation_are_blocked(self):
        with patch.dict("os.environ", {"EXPLAINER_CACHED_ONLY": "1"}):
            with self.assertRaisesRegex(CacheValidationError, "cannot prepare"):
                self.cache.prepare_inputs(["pages"], downloader=lambda *_: self.fail("network"))
            with self.assertRaisesRegex(CacheValidationError, "prohibits generation"):
                self.cache._produce("pages", lambda: self.fail("producer"))

    def test_cli_prepare_inputs_is_separate_from_numerical_generation(self):
        (self.books / "158.txt").unlink(); calls = []
        def download(url, target):
            calls.append(url); target.write_text(public_book_fixture(158))
        with patch("sys.argv", ["compute", "board", "--prepare-inputs"]), \
             patch("videos.ai.ai6.cache_contract.importlib.import_module", return_value=SimpleNamespace(_download=download)), \
             patch.object(self.cache, "_produce", side_effect=AssertionError("numerical producer")):
            self.cache.main(self.items)
        self.assertEqual(len(calls), 1)
        self.assertFalse(self.cache.path("pages").exists())

    def test_cli_check_never_prepares_inputs_or_mutates_missing_cache(self):
        with patch("sys.argv", ["compute", "pages", "--check"]), \
             patch.object(self.cache, "prepare_inputs", side_effect=AssertionError("prepare")), \
             self.assertRaises(SystemExit) as result:
            self.cache.main(self.items)
        self.assertEqual(result.exception.code, 1)
        self.assertFalse(self.cache.dir.exists())

    def test_partial_finite_value_tamper_invalidates_checksum(self):
        self.publish_pages(); params = dict(folds=10)
        def interrupt():
            self.cache.partial("board", params)["ls_2"] = fold_piece()
            raise RuntimeError("stop")
        with self.assertRaises(RuntimeError):
            self.cache._produce("board", interrupt)
        path = self.cache.dir / "board.partial.json"
        d = json.loads(path.read_text()); d["done"]["ls_2"]["held"] = .76
        path.write_text(json.dumps(d)); tampered = path.read_bytes()
        def fresh():
            self.assertNotIn("ls_2", self.cache.partial("board", params))
            return board_fixture()
        self.cache._produce("board", fresh)
        self.assertIn(tampered, [p.read_bytes() for p in self.preserved("board.partial.json")])

    def test_explicit_rebind_cannot_hide_loaded_source_drift(self):
        before = self.cache._source_hashes()
        with patch.object(self.cache, "_source_hashes", return_value=dict(before, changed="new source")):
            with self.assertRaisesRegex(CacheValidationError, "restart the process"):
                self.cache.bind(self.items)

    def test_board_fold_identity_and_derived_summary_are_checked(self):
        self.publish_pages()
        for change in ("digest", "summary", "cohort"):
            d = board_fixture()
            if change == "digest":
                d["evaluation"]["fold_sha256"] = "0" * 64
            elif change == "summary":
                d["rows"][0]["2"]["cv"] += .01
            else:
                d["fold_ids"] = d["fold_ids"][:-1]
            with self.subTest(change=change), self.assertRaisesRegex(CacheValidationError, "malformed producer output"):
                self.cache._produce("board", lambda: d)

    def test_dynamic_consumed_arrays_are_explicitly_required(self):
        svm = contracts.required_arrays("svm", dict(Cs=[1.], gammas=[.1]))
        self.assertTrue({"sv_C1", "alpha_C1", "region_C1", "region_g0.1"} <= svm)
        self.assertTrue({"w1", "region1"} <= contracts.required_arrays("adaboost", dict(snaps=[1])))
        self.assertTrue({"scan_not_t", "scan_not_gini", "scan_the_entropy"} <= contracts.required_arrays("trees", {}))


if __name__ == "__main__":
    unittest.main()
