"""Bounded Part 28 regression checks; synthetic inputs, no scenes/models/caches.

The metric tests execute the actual changed summarization code. Their reference
uses positive/negative pair comparisons, not the implementation's rank formula.
"""
from __future__ import annotations

import ast
import json
import math
from pathlib import Path
import re
import types
import unittest

import numpy as np

from explainer.lang import key
from explainer.zh_templates import Translator, source_startswith, sources, table

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / "videos/ai/ai28"


def source_function(name):
    tree = ast.parse((PART / "think.py").read_text())
    return next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)


def actual_auc(scores, labels):
    function = source_function("compute_think_verify")
    # The last top-level kind loop is the AUC summarizer, after scoring/training.
    node = [n for n in function.body if isinstance(n, ast.For)
            and isinstance(n.target, ast.Name) and n.target.id == "kind"][-1]
    scope = dict(np=np, scores={k: np.asarray(scores) for k in ("orm", "prm")},
                 test={"final": np.asarray(labels, dtype=bool)}, out={})
    exec(compile(ast.Module(body=[node], type_ignores=[]), "<actual-verifier-auc>", "exec"), scope)
    return scope["out"]


def pair_auc(scores, labels):
    positives = [s for s, y in zip(scores, labels) if y]
    negatives = [s for s, y in zip(scores, labels) if not y]
    return sum(float(p > n) + .5 * float(p == n)
               for p in positives for n in negatives) / (len(positives) * len(negatives))


class VerifierAUCTests(unittest.TestCase):
    def check_pairs(self, scores, labels):
        expected = pair_auc(scores, labels)
        for value in actual_auc(scores, labels).values():
            self.assertAlmostEqual(value, expected, places=13)

    def test_all_equal_scores_have_auc_half(self):
        self.check_pairs([.5] * 6, [True, False, True, False, True, False])

    def test_perfect_and_reversed_rankings(self):
        self.check_pairs([.8, .9, .1, .2], [True, True, False, False])
        self.check_pairs([.1, .2, .8, .9], [True, True, False, False])

    def test_mixed_positive_negative_ties_match_pair_definition(self):
        self.check_pairs([0, .2, .2, .5, .5, 1], [False, True, False, True, False, True])

    def test_tie_result_is_invariant_to_input_order(self):
        scores = np.array([.1, .2, .2, .2, .4, .4, .9, .9])
        labels = np.array([False, True, False, True, False, True, True, False])
        for permutation in (np.arange(8), np.arange(8)[::-1], *np.random.default_rng(8).permuted(
                np.tile(np.arange(8), (20, 1)), axis=1)):
            self.check_pairs(scores[permutation], labels[permutation])


class VotingSummaryTests(unittest.TestCase):
    def actual(self, answers, truth):
        samples = dict(truth=truth, n=np.full(len(truth), 6), d=np.zeros((len(truth), 10), int),
                       think_answer=answers, direct_answer=answers,
                       think_steps=np.zeros((len(truth), 64, 10), int))
        calls = []
        def load(name):
            calls.append(name)
            if name != "think_samples":
                raise AssertionError("Unexpected producer/dependency request")
            return samples
        scope = dict(np=np, math=math, VMAX=90,
                     _c=lambda: types.SimpleNamespace(load=load, rng=np.random.default_rng))
        nodes = [source_function("_vote"), source_function("compute_think_vote")]
        exec(compile(ast.Module(body=nodes, type_ignores=[]), "<actual-vote-summaries>", "exec"), scope)
        result = scope["compute_think_vote"]()
        self.assertEqual(calls, ["think_samples"])
        return result

    def test_all_invalid_answers_never_become_a_correct_zero(self):
        answers = np.full((2, 64), -1)
        result = self.actual(answers, np.array([0, 3]))
        for mode in ("think", "direct"):
            self.assertEqual(result[mode + "_mode_right"], 0)
            self.assertEqual(result[mode + "_vote"], [0] * 7)
            self.assertEqual(result[mode + "_pass"], [0] * 7)

    def test_valid_zero_invalids_and_ties_keep_existing_selection_policy(self):
        answers = np.array([[-1] * 64, [0] * 32 + [-1] * 32,
                            [1] * 32 + [2] * 32, [3] * 64])
        result = self.actual(answers, np.array([0, 0, 2, 3]))
        for mode in ("think", "direct"):
            self.assertEqual(result[mode + "_mode_right"], .5)
            self.assertEqual(result[mode + "_vote"][-1], .5)
            self.assertEqual(result[mode + "_pass"][-1], .75)
        np.testing.assert_array_equal(answers[0], -1)  # summarization must preserve raw outcomes


class BilingualSourceContracts(unittest.TestCase):
    def test_every_narrated_source_has_an_unambiguous_translation(self):
        translations = table("ai28")["ZH"]
        for source in sources("ai28"):
            text = source.get("en") or source["tpl"]
            with self.subTest(source=text[:100]):
                hits = [k for k in translations if source_startswith(text, k)]
                self.assertTrue(hits)
                self.assertEqual(len({translations[k] for k in hits}), 1)

    def test_persisted_narration_keys_translations_and_bookmarks_agree(self):
        translate = Translator("ai28")
        lines = json.loads((PART / "narration_zh.json").read_text())["lines"]
        for k, line in lines.items():
            with self.subTest(scene=line["scene"], key=k):
                self.assertEqual(k, key(line["en"]))
                self.assertEqual(translate(line["en"]), line["zh"])
                marks = lambda text: re.findall(r"<bookmark\s+mark=['\"]([^'\"]+)['\"]\s*/>", text)
                self.assertEqual(marks(line["en"]), marks(line["zh"]))

    def test_caption_delta_is_narrow_and_can_be_composed_without_conflicts(self):
        delta = json.loads((PART / "text_zh_reviewed.json").read_text())
        shared = json.loads((ROOT / "videos/ai/ai_text_zh.json").read_text())["strings"]
        self.assertEqual(delta["schema_version"], 1)
        self.assertEqual(delta["target"], "videos/ai/ai_text_zh.json")
        self.assertEqual(set(delta["strings"]), set(delta["expected_before"]))
        self.assertTrue(delta["strings"])
        for english, chinese in delta["strings"].items():
            self.assertIsInstance(english, str)
            self.assertIsInstance(chinese, str)
            self.assertTrue(english and chinese)
            self.assertIn(shared.get(english), (delta["expected_before"][english], chinese), english)


if __name__ == "__main__":
    unittest.main()
