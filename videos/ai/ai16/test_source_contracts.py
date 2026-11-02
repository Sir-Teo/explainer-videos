"""Synthetic source contracts only: no scene imports, caches, models, or renderer.

Run from the repository root with Python 3.12 and NumPy:
    python videos/ai/ai16/test_source_contracts.py
These fixtures do not establish any experimental outcome or visual acceptance.
"""

import ast
import copy
import hashlib
import json
import math
import re
import subprocess
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PART = Path(__file__).resolve().parent
BASELINE = "46006f71195a9fe0fdadc29164d9803e7feaed89"
BOOKMARK = re.compile(r"<bookmark\s+mark=['\"]([^'\"]+)['\"]\s*/>")


def original(path):
    return subprocess.check_output(["git", "show", f"{BASELINE}:{path.relative_to(ROOT)}"], cwd=ROOT, text=True)


def method(file, cls, name):
    tree = ast.parse((PART / file).read_text())
    parent = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == cls)
    return next(n for n in parent.body if isinstance(n, ast.FunctionDef) and n.name == name)


def extracted_function(node):
    node = copy.deepcopy(node)
    node.decorator_list = []
    module = ast.Module(body=[node], type_ignores=[])
    scope = {}
    exec(compile(ast.fix_missing_locations(module), "<isolated synthetic contract>", "exec"), scope)
    return scope[node.name]


def literal_table(text, name):
    tree = ast.parse(text)
    return ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign)
                                 and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)))


class SourceContracts(unittest.TestCase):
    def test_scientific_recipes_unchanged_including_noisy_upcycle_and_flops(self):
        class WithoutDocs(ast.NodeTransformer):
            def visit_FunctionDef(self, node):
                self.generic_visit(node)
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                    if isinstance(node.body[0].value.value, str):
                        node.body = node.body[1:]
                return node

        for name in ("compute.py", "runs.py", "nets.py", "prune.py", "lottery.py", "recall.py", "facts.py"):
            before = WithoutDocs().visit(ast.parse(original(PART / name)))
            after = WithoutDocs().visit(ast.parse((PART / name).read_text()))
            self.assertEqual(ast.dump(before), ast.dump(after), name)

    def test_preserved_flops_recipe_is_linear_in_routed_fraction(self):
        flops = extracted_function(method("nets.py", "Net", "flops"))
        cfg = dict(d=4, hidden=8, ffn="dense", ctx=8, attn="full", attn_k=0,
                   layers=2, mod_layers=(), mod_cap=1, vocab=5)
        self.assertEqual(flops(SimpleNamespace(c=SimpleNamespace(**cfg))), 2088)
        cfg.update(mod_layers=(1,), mod_cap=0.25)
        stored = flops(SimpleNamespace(c=SimpleNamespace(**cfg)))
        self.assertEqual(stored, 1350)
        # An ideal c^2 attention reduction is a DIFFERENT estimate. Never claim
        # that this synthetic difference corrects or validates the saved science.
        ideal_fixture = 6 * (164 + 0.25 * 128 + 0.25**2 * 36 + 20)
        self.assertNotEqual(stored, ideal_fixture)

    def test_pruning_excludes_embeddings_and_output_head(self):
        tree = ast.parse((PART / "prune.py").read_text())
        linears = extracted_function(next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "linears"))
        blocks = [SimpleNamespace(attn=SimpleNamespace(qkv=object(), o=object()),
                                  ffn=SimpleNamespace(w1=object(), w2=object())) for _ in range(2)]
        model = SimpleNamespace(blocks=blocks, emb=object(), out=object())
        rows = linears(model)
        self.assertEqual([n for n, _ in rows], [f"b{i}.{key}" for i in range(2) for key in ("qkv", "o", "w1", "w2")])
        self.assertNotIn(model.emb, [v for _, v in rows])
        self.assertNotIn(model.out, [v for _, v in rows])

    def test_histogram_and_fraction_include_same_seed_block_cohort(self):
        data = dict(seeds=[0, 1], cuts=[0.01, 0.05, 0.1],
                    hist_s0=[[10, 0], [0, 10]], hist_s1=[[10, 10], [20, 0]],
                    small_s0=[[0, 0, 0.1], [0, 0, 0.3]], small_s1=[[0, 0, 0.7], [0, 0, 0.9]])
        before = copy.deepcopy(data)
        node = method("s16_structured.py", "Structured", "activations")
        statements = [n for n in node.body if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id in ("H", "small", "cut_i", "sh") for t in n.targets)]
        scope = {"a": data, "np": np}
        exec(compile(ast.Module(body=statements, type_ignores=[]), "<synthetic cohorts>", "exec"), scope)
        np.testing.assert_allclose(scope["H"], [2 / 3, 1 / 3])
        self.assertAlmostEqual(scope["sh"], 0.5)
        self.assertFalse(np.array_equal(scope["H"], [1, 0]))  # old single seed/block histogram
        self.assertEqual(data, before)

    def test_router_output_equation_contains_published_scale(self):
        # Evaluate only construction of the four equation strings, not a scene.
        rows = []
        fragments = []

        class Construction:
            def __init__(self, *a, **k):
                pass

            def arrange(self, *a, **k):
                return self

            def move_to(self, *a, **k):
                return self

        def cmath(*args, **kwargs):
            rows.append("".join(args))
            fragments.append(args)
            return Construction()

        node = method("s06_lossfree.py", "LossFree", "exact")
        assignment = next(n for n in node.body if isinstance(n, ast.Assign)
                          and any(isinstance(t, ast.Name) and t.id == "eqs" for t in n.targets))
        env = dict(r={"scaling": 2.5}, colors={}, cmath=cmath, VGroup=Construction, LEFT=0, DOWN=0)
        exec(compile(ast.Module(body=[assignment], type_ignores=[]), "<synthetic equation construction>", "exec"), env)
        self.assertIn(r"2.5\sum", rows[3])
        self.assertNotIn("2.5", rows[2])  # gates remain normalized; scale acts on routed sum
        captions = json.loads((PART / "text_zh_reviewed.json").read_text())["strings"]
        self.assertIn(fragments[3][0], captions)
        self.assertIn(r"\text{共享}", captions[fragments[3][0]])
        self.assertNotIn(r"\text{shared}", captions[fragments[3][0]])

    def test_all_scene_bookmark_orders_and_explicit_timing_are_preserved(self):
        def contracts(text, allow_hook_transition=False):
            tree = ast.parse(text)
            approved = set()
            if allow_hook_transition:
                hook = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Hook")
                plan = next(n for n in hook.body if isinstance(n, ast.FunctionDef) and n.name == "plan")
                approved = {id(n) for n in ast.walk(plan) if isinstance(n, ast.Call)
                            and ast.unparse(n) == "Succession(FadeOut(smap), FadeIn(obj), run_time=1.0)"}
            voiceovers = sorted((n for n in ast.walk(tree) if isinstance(n, ast.Call)
                                 and isinstance(n.func, ast.Attribute) and n.func.attr == "voiceover"), key=lambda n: n.lineno)
            marks = [BOOKMARK.findall(" ".join(str(c.value) for c in ast.walk(n.args[0])
                                              if isinstance(c, ast.Constant) and isinstance(c.value, str))) for n in voiceovers]
            timing = [ast.dump(k.value) for n in ast.walk(tree) if isinstance(n, ast.Call)
                      for k in n.keywords if k.arg in ("run_time", "rate_func")
                      # The observed map/objectives overlap is repaired by making
                      # their existing one-second crossfade sequential, same duration.
                      and not (id(n) in approved and k.arg == "run_time")]
            return marks, timing

        for path in sorted(PART.glob("s[0-9][0-9]_*.py")):
            allow = path.name == "s01_hook.py"
            self.assertEqual(contracts(original(path), allow), contracts(path.read_text(), allow), path.name)

    def test_noise_reveal_keeps_each_displayed_equation_complete(self):
        node = method("s02_origins.py", "Origins", "sparse")
        assignment = next(n for n in node.body if isinstance(n, ast.Assign)
                          and any(isinstance(t, ast.Name) and t.id == "f1" for t in n.targets))
        fragments = [ast.literal_eval(a) for a in assignment.value.args]
        before_noise = "".join(fragments[:2])
        after_noise = "".join(fragments)
        self.assertEqual(before_noise, r"H(x)_i= (W_g x)_i")
        self.assertFalse(before_noise.rstrip().endswith("+"))
        self.assertIn(r"+\epsilon_i", after_noise)

    def test_map_objectives_transition_is_sequential_with_same_total_duration(self):
        node = method("s01_hook.py", "Hook", "plan")
        sequence = [n for n in ast.walk(node) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Name) and n.func.id == "Succession"]
        self.assertEqual(len(sequence), 1)
        transition = sequence[0]
        self.assertEqual([(n.func.id, n.args[0].id) for n in transition.args],
                         [("FadeOut", "smap"), ("FadeIn", "obj")])
        self.assertEqual({k.arg: ast.literal_eval(k.value) for k in transition.keywords}, {"run_time": 1.0})

    def test_reviewed_narration_entries_change_without_corrected_outcome_fixture_and_keep_bilingual_bookmarks(self):
        path = PART / "narration_zh.json"
        before, after = json.loads(original(path)), json.loads(path.read_text())
        old, new = before.pop("lines"), after.pop("lines")
        self.assertEqual(before, after)
        removed, added = old.keys() - new.keys(), new.keys() - old.keys()
        self.assertEqual(len(removed), 21)
        self.assertEqual(len(added), 20)
        self.assertEqual({k: old[k] for k in old.keys() & new.keys()}, {k: new[k] for k in old.keys() & new.keys()})
        for key in added:
            entry = new[key]
            self.assertEqual(key, hashlib.sha1(" ".join(entry["en"].split()).encode()).hexdigest()[:12])
            self.assertEqual(BOOKMARK.findall(entry["en"]), BOOKMARK.findall(entry["zh"]))
            matching = [old[k] for k in removed if old[k]["scene"] == entry["scene"]
                        and BOOKMARK.findall(old[k]["en"]) == BOOKMARK.findall(entry["en"])]
            self.assertTrue(matching)

    def test_special_scene_uses_separate_matched_cohort_candidate(self):
        # The production scene selects a separately versioned correction. It must
        # never silently reinterpret the unchanged baseline Special outcome.
        text = (PART / "s11_special.py").read_text()
        self.assertNotIn('load("special")', text)
        self.assertEqual(text.count('load("special_within_window_v2")'), 2)
        self.assertIn("window starts excluded", text)
        self.assertIn("16{,}128", text)
        self.assertNotIn("fast lookup", text)
        self.assertIn("does not establish which contextual information", text)
        info = method("s11_special.py", "Special", "information")
        compare = next(n for n in info.body if isinstance(n, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == "fcoarse" for t in n.targets))
        # A synthetic third seed is deliberately far away: the fine comparison
        # must use the same two seeds rather than the three-seed chart mean.
        fixture = {"moe_s0_l1": {"cur": 0.6}, "moe_s1_l1": {"cur": 0.8},
                   "moe_s2_l1": {"cur": 9.0}}
        scope = {"s": fixture, "last": 1, "fseeds": [0, 1],
                 "ms": lambda values: (sum(values) / len(values), min(values), max(values))}
        exec(compile(ast.Module(body=[compare], type_ignores=[]), "<paired cohort>", "exec"), scope)
        self.assertAlmostEqual(scope["fcoarse"], 0.7)
        self.assertNotAlmostEqual(scope["fcoarse"], (0.6 + 0.8 + 9.0) / 3)

    def test_capacity_approximation_is_explicit_for_nonintegral_buffers(self):
        # One token and two experts: ceil(1/2)=1, so the exact drop is zero;
        # removing the ceiling would incorrectly predict half a token-slot.
        exact_capacity = math.ceil(1 / 2)
        self.assertEqual(max(0, 1 - exact_capacity), 0)
        self.assertEqual(max(0, 1 - 1 / 2), 0.5)
        node = method("s08_capacity.py", "Capacity", "dropped")
        rows = next(n for n in node.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "rows" for t in n.targets))
        scope = dict(colors={}, cmath=lambda *parts, **kw: "".join(parts))
        exec(compile(ast.Module(body=[rows], type_ignores=[]), "<synthetic rounding contract>", "exec"), scope)
        self.assertIn(r"\simeq", scope["rows"][1])
        self.assertIn(r"\simeq", scope["rows"][3])
        self.assertNotIn(r"\simeq", scope["rows"][2])

    def test_depth_diagram_declares_its_illustrative_fraction(self):
        self.assertEqual(3 / 12, 0.25)
        self.assertNotEqual(3 / 12, 0.125)
        node = method("s12_depth.py", "Depth", "idea")
        note = next(n for n in node.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "route_note" for t in n.targets))
        strings = [n.value for n in ast.walk(note) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        self.assertIn(r"illustrative route: \ $3$ of $12$ tokens \ ($25\%$)", strings)

    def test_updated_chinese_templates_match_corrected_historical_fixture_lines(self):
        # Isolate the real AST/template translator from explainer.__init__ (Manim).
        src = ast.parse((ROOT / "explainer/zh_templates.py").read_text())
        src.body = [n for n in src.body if not (isinstance(n, ast.ImportFrom) and n.module == "explainer.paths")]
        scope = {"video_dir": lambda _: PART}
        exec(compile(src, "<isolated real template translator>", "exec"), scope)
        translator = scope["Translator"]("ai16")
        old = json.loads(original(PART / "narration_zh.json"))["lines"]
        new = json.loads((PART / "narration_zh.json").read_text())["lines"]
        for key in new.keys() - old.keys():
            entry = new[key]
            self.assertEqual(translator(entry["en"]), entry["zh"], entry["scene"])

    def test_shared_caption_patch_is_entry_scoped_and_matches_dynamic_labels(self):
        data = json.loads((PART / "text_zh_reviewed.json").read_text())
        self.assertEqual(set(data), {"strings", "patterns"})
        self.assertEqual(len(data["patterns"]), 2)
        pattern, replacement = data["patterns"][0]
        for value in (1.01, 1.18, 1.36, 2.5):
            text = rf"mean busiest-device factor: \\ ${value:.2f}\times$ a fair share"
            self.assertIsNotNone(re.fullmatch(pattern, text), text)
            self.assertIn(f"{value:.2f}", re.sub(pattern, replacement, text))


if __name__ == "__main__":
    unittest.main(verbosity=2)
