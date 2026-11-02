"""Synthetic evaluation-protocol regressions; no scientific inputs or neural models."""
from __future__ import annotations

import ast
from contextlib import ContextDecorator
import math
import json
from pathlib import Path
import re
import types
import unittest
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / "videos" / "ai" / "ai14"


class Tensor(np.ndarray):
    def float(self):
        return self.astype(float)

    def numpy(self):
        return np.asarray(self)

    def mean(self, axis=None, dtype=None, out=None, keepdims=False, *, dim=None):
        return np.asarray(self).mean(axis=axis if dim is None else dim,
                                     dtype=dtype, out=out, keepdims=keepdims).view(Tensor)

    def sum(self, axis=None, dtype=None, out=None, keepdims=False, *, keepdim=None):
        return np.asarray(self).sum(axis=axis, dtype=dtype, out=out,
                                    keepdims=keepdims if keepdim is None else keepdim).view(Tensor)

    def flatten(self, start_dim=0, end_dim=-1):
        end_dim %= self.ndim
        shape = self.shape[:start_dim] + (-1,) + self.shape[end_dim + 1:]
        return self.reshape(shape)

    def view(self, *shape):
        if len(shape) == 1 and isinstance(shape[0], type):
            return super().view(shape[0])
        return self.reshape(*shape)


def tensor(values, dtype=None):
    return np.asarray(values, dtype=dtype).view(Tensor)


class NoGrad(ContextDecorator):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


TORCH = types.ModuleType("torch")
TORCH.Tensor = Tensor
TORCH.tensor = tensor
TORCH.zeros = lambda *shape, dtype=float: tensor(np.zeros(shape, dtype=dtype))
TORCH.long = np.int64
TORCH.no_grad = NoGrad


def cross_entropy(logits, targets, reduction="none"):
    x = np.asarray(logits)
    peak = x.max(axis=-1, keepdims=True)
    logsum = peak[:, 0] + np.log(np.exp(x - peak).sum(axis=-1))
    return tensor(logsum - x[np.arange(len(x)), np.asarray(targets)])


def function(filename, name):
    tree = ast.parse((PART / filename).read_text())
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    code = ast.Module(body=[ast.ImportFrom(module="__future__", names=[ast.alias("annotations")], level=0), node],
                      type_ignores=[])
    ns = dict(np=np, math=math, torch=TORCH, F=types.SimpleNamespace(cross_entropy=cross_entropy))
    exec(compile(ast.fix_missing_locations(code), str(PART / filename), "exec"), ns)
    return ns[name]


class UniformAttentionModel:
    """Synthetic residual block with uniform, bidirectional attention.

    Zero queries/keys make attention a sequence mean. Token features are [t,t²],
    so each pooled sentence feature must be [2 mean(t),2 mean(t²)], independently
    of other sentences. This oracle does not use the batching implementation.
    """

    def __init__(self):
        self.inputs = []
        self.blocks = [lambda h: h + h.mean(dim=1)[:, None, :]]
        self.norm = lambda h: h

    def eval(self):
        return self

    def emb(self, x):
        self.inputs.append(np.asarray(x).copy())
        return tensor(np.stack([x, x ** 2], axis=-1), dtype=float)


class ProbePaddingTests(unittest.TestCase):
    def features(self, sents, batch):
        modules = {name: types.ModuleType(name) for name in ("explainer", "explainer.ai", "explainer.ai.novels")}
        modules["explainer.ai.novels"].encode = lambda s: [int(t) for t in s.split()]
        modules["explainer.ai"].novels = modules["explainer.ai.novels"]
        model = UniformAttentionModel()
        with patch.dict("sys.modules", {**modules, "torch": TORCH}):
            result = function("compute.py", "_features")(model, sents, B=batch)
        return result, model.inputs

    def test_mixed_lengths_match_single_sentence_oracle_and_input_order(self):
        sents = ["1 2", "8 9 10 11", "3", "4 5", "6 7 8", "9"]
        expected = np.array([[2 * np.mean(v), 2 * np.mean(np.square(v))]
                             for v in ([1, 2], [8, 9, 10, 11], [3], [4, 5], [6, 7, 8], [9])])
        for batch in (1, 2, 32):
            actual, _ = self.features(sents, batch)
            np.testing.assert_allclose(actual, expected)

    def test_short_sentence_is_invariant_to_long_neighbors(self):
        alone, _ = self.features(["2 5"], 32)
        mixed, _ = self.features(["1 3 7 9 11", "2 5", "8"], 32)
        np.testing.assert_allclose(alone[0], mixed[1])

    def test_attention_never_receives_invented_padding_and_keeps_64_token_cap(self):
        _, inputs = self.features(["1 2", "3", " ".join(["4"] * 70)], 32)
        self.assertFalse(any(np.any(x == 0) for x in inputs))
        self.assertEqual(max(x.shape[1] for x in inputs), 64)


class RepeatedWordCohortTests(unittest.TestCase):
    def score(self, wrong_positions):
        rep = tensor([[0, 1, 2, 3, 1, 2, 3]], dtype=np.int64)
        logits = np.full((1, 6, 4), -8.0)
        for pos, target in enumerate([1, 2, 3, 1, 2, 3]):
            logits[0, pos, (target + 1) % 4 if pos in wrong_positions else target] = 8.0
        class Model:
            def eval(self):
                pass

            def __call__(self, x):
                return tensor(logits)

        return function("lm.py", "repeat_test")(Model(), rep)

    def test_last_word_of_first_copy_counts_for_accuracy_and_loss(self):
        result = self.score({2})
        self.assertAlmostEqual(result["acc1"], 2 / 3)
        self.assertAlmostEqual(result["acc2"], 1)
        self.assertAlmostEqual(result["loss1"] - result["loss2"], 16 / 3)

    def test_identical_word_errors_have_identical_scores_in_each_copy(self):
        for word in range(3):
            result = self.score({word, word + 3})
            self.assertAlmostEqual(result["acc1"], result["acc2"])
            self.assertAlmostEqual(result["loss1"], result["loss2"])

    def test_new_protocol_is_distinguishable_from_historical_results(self):
        self.assertEqual(self.score(set()).get("repeat_protocol"), "matched-all-words-v1")



class FrozenProbeFitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import torch
        torch.set_num_threads(1)
        torch.set_num_interop_threads(1)

    def fixture(self, dtype=np.float32):
        X = np.array([[-1.0, 0.0], [-0.5, 0.0], [0.5, 0.0], [1.0, 0.0]], dtype=dtype)
        return X, np.array([0, 0, 1, 1])

    def test_default_original_fp32_fit_remains_available(self):
        X, y = self.fixture()
        self.assertEqual(function("compute.py", "_probe")(X, y, X, y, 2), (1.0, 1.0))

    def test_optional_fit_rejects_the_wrong_thread_recipe(self):
        import torch
        X, y = self.fixture()
        with patch.object(torch, "get_num_threads", return_value=2):
            with self.assertRaisesRegex(ValueError, "one compute thread"):
                function("compute.py", "_probe_v2")(X, y, X, y, 2)

    def test_regularized_binary_fit_passes_its_residual_gate(self):
        X, y = self.fixture()
        self.assertEqual(function("compute.py", "_probe_v2")(X, y, X, y, 2), (1.0, 1.0))

    def test_unoptimized_fit_is_rejected(self):
        X, y = self.fixture()
        with self.assertRaisesRegex(RuntimeError, "post-fit residual"):
            function("compute.py", "_probe_v2")(X, y, X, y, 2, iters=0)

    def test_normalization_does_not_silently_change_to_float64(self):
        X, y = self.fixture(np.float64)
        with self.assertRaisesRegex(TypeError, "float32 frozen features"):
            function("compute.py", "_probe_v2")(X, y, X, y, 2)


if __name__ == "__main__":
    unittest.main()
