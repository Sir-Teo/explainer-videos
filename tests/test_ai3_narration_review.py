"""Part 3 narration coverage without importing scenes or computing their data."""
import ast
import math
import re
import unittest
from pathlib import Path

import numpy as np

from explainer.zh_templates import Translator, _parts, ambiguous, numeric, sources, table


ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / "videos/ai/ai3"
BOOKMARK = r"<bookmark[^>]+/>"


class Part3NarrationTests(unittest.TestCase):
    def setUp(self):
        self.translator = Translator("ai3")

    def translated(self, english):
        chinese = self.translator(english)
        self.assertIsNotNone(chinese, english)
        self.assertRegex(chinese, r"[\u4e00-\u9fff]")
        self.assertNotRegex(chinese, r"\{[^{}]+\}")
        self.assertEqual(re.findall(BOOKMARK, english), re.findall(BOOKMARK, chinese))
        return chinese

    def spoken(self, prefix, **values):
        row = next(r for r in sources("ai3")
                   if prefix in r.get("en", r.get("tpl", "")))
        if "en" in row:
            return row["en"]
        return eval(compile(ast.parse(row["tpl"], mode="eval"), "actual-ai3-narration", "eval"),
                    {"int": int, "len": len}, values)

    def test_mathematical_qualifiers_survive_head_translation(self):
        cases = [
            (self.spoken("Is that cosine always"), ["绝对值", "同向", "反向"]),
            (self.spoken("One number says how much"), ["绝对值", "符号"]),
            (self.spoken("Symmetric matrices, equal"), ["标准正交", "基"]),
            (self.spoken("Eigenvalues are roots"), ["通用", "根式", "非零"]),
            (self.spoken("Part 1's table of letter pairs", err=[.4, .2]),
             ["平方根", "平方", "归一化", "互相独立"]),
            (self.spoken("The spectral norm has become", tiny=.6, near=.8),
             ["最大奇异值的百分之一", "弗罗贝尼乌斯范数", "0.6", "1.3"]),
        ]
        for english, qualifiers in cases:
            chinese = self.translated(english)
            for qualifier in qualifiers:
                self.assertIn(qualifier, chinese)

    def test_actual_rate_and_reference_verdict_branches_translate(self):
        tree = ast.parse((PART / "s07_power.py").read_text())
        expr = next(n.value for n in ast.walk(tree) if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "verdict" for t in n.targets))
        for gap in [.009, .01, .125]:
            verdict = eval(compile(ast.Expression(expr), "actual-power-verdict", "eval"),
                           {}, {"rate_gap": gap})
            chinese = self.translated(verdict)
            if gap < .01:
                self.assertIn("小于0.01", chinese)
            else:
                self.assertIn(f"{gap:.3f}", chinese)
                self.assertIn("绝对差", chinese)
        tree = ast.parse((PART / "s10_norms.py").read_text())
        branch = next(n for n in ast.walk(tree) if isinstance(n, ast.If)
                      and ast.unparse(n.test) == "hi < 0.5 * rnd['stable']")
        observed = []
        for maximum in [49., 50., 99., 100., 120.]:
            env = {"hi": maximum, "rnd": {"stable": 100.}}
            exec(compile(ast.Module([branch], type_ignores=[]), "actual-stable-reference", "exec"), {}, env)
            chinese = self.translated(env["verdict"])
            self.assertIn("MLP形状", chinese)
            self.assertNotIn("同样形状", chinese)
            observed.append(chinese)
        self.assertIn("一半", observed[0])
        self.assertNotIn("一半", observed[1])
        self.assertIn("达到或超过", observed[3])

    def test_jl_confidence_branches_preserve_unavailable_vs_failed_distinction(self):
        tree = ast.parse((PART / "s16_jl.py").read_text())
        branch = next(n for n in ast.walk(tree) if isinstance(n, ast.If)
                      and any(isinstance(x, ast.Assign) and any(isinstance(t, ast.Name)
                              and t.id == "bound_verdict" for t in x.targets) for x in n.body))
        cases = [([(2., .5, 100)], .4), ([(2., .5, 100)], float("nan")), ([], float("nan"))]
        rendered = []
        for good, bound in cases:
            env = {"good": good, "last_bound": bound, "confidence": 95.,
                   "last": {"k": 768, "worst": [.2, .3]}, "math": math, "np": np}
            exec(compile(ast.Module([branch], type_ignores=[]), "actual-jl-verdict", "exec"), env)
            english = self.spoken("The lemma promises every pair at once.", bound_verdict=env["bound_verdict"])
            chinese = self.translated(english)
            self.assertIn("95%", chinese)
            self.assertIn("经典存在性", chinese)
            rendered.append(chinese)
        self.assertIn("0.40", rendered[0])
        self.assertIn("最后一个抽样维数没有", rendered[1])
        self.assertIn("并不表示实测映射失败", rendered[2])

    def test_numeric_penalty_suffix_translates_all_comparisons_recursively(self):
        # Extract only the pure helper: no imports, loaders or rendering.
        tree = ast.parse((PART / "s18_netflix.py").read_text())
        helper = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "penalty_verdict")
        env = {"np": np}
        exec(compile(ast.Module([helper], type_ignores=[]), "actual-penalty-verdict", "exec"), env)
        cases = [(.9, [1., .85, .8], "更低", "没有明显"),
                 (.8, [1., .7, .9], "更高", "回升"),
                 (.9, [1., .9, .905], "相差不超过0.01星", "没有明显"),
                 (1., [1.2, .7, .9], "更低", "回升")]
        for regularized, unregularized, comparison, shape in cases:
            h = np.array([[0., 1., 1.1], [1., .8, regularized]])
            h0 = np.array([[i, 1., x] for i, x in enumerate(unregularized)])
            tail = env["penalty_verdict"](h, h0)
            english = self.spoken("Training replayed, at rank", rp={"rank": 8}, h=h, tail=tail,
                                  m={"genre_nn": .8, "genre_chance": .2},
                                  genre_verdict=self.spoken("The final genre-neighbour agreement exceeds"))
            chinese = self.translated(english)
            self.assertNotIn("With no", chinese)
            self.assertIn(comparison, chinese)
            self.assertIn(shape, chinese)
            self.assertIn(f"{unregularized[-1]:.3f}", chinese)
            self.assertIn("相同的偏置惩罚", chinese)

    def test_new_dimensional_bookmark_and_layer_peak_are_not_lost(self):
        english = self.spoken("Our intuition comes from three dimensions", sd={10: 19., 100: 5.7, 768: 2.1})
        chinese = self.translated(english)
        self.assertIn("<bookmark mark='c10'/>", chinese)
        self.assertIn("十维", chinese)
        english = self.spoken("Inside the network it is stronger.", L=[{"cos": .1}],
                              mid={"cos": .6, "layer": 6, "top3_share": -.25},
                              final={"cos": .7}, peak={"cos": .9, "layer": 2})
        chinese = self.translated(english)
        self.assertIn("最后一次归一化后是0.70", chinese)
        self.assertIn("最大值是第2层的0.90", chinese)
        self.assertIn("带符号贡献", chinese)
        self.assertIn("-25%", chinese)

    def test_empirical_spectra_and_gradient_qualifiers_are_retained(self):
        summary = self.spoken("Our displayed layer has alpha", s={"alpha": 2.5, "n_tail": 35, "ks": .07})
        for fit_summary in [summary, self.spoken("Our displayed layer has no available")]:
            chinese = self.translated(self.spoken("We can summarize a spectral tail", n_in=20,
                                                  fit_summary=fit_summary))
            self.assertIn("描述性的比较", chinese)
            self.assertIn("不是通用的准确率标准", chinese)
            self.assertIn("不能证明幂律模型", chinese)
        chinese = self.translated(self.spoken("Here is a real gradient, from a small transformer", shape=[32, 64],
                                              tr=[{"step": 1, "top8": .2}], pk={"step": 100, "top8": .8},
                                              last={"step": 600, "top8": .4}, n=32))
        self.assertIn("平方能量", chinese)
        self.assertIn("第1步", chinese)
        self.assertIn("第100步", chinese)
        self.assertIn("最后第600步", chinese)
        chinese = self.translated(self.spoken("Does a narrow window cost anything?", mean={"adam": 4.,
                                              "galore32": 3.9, "galore8": 4.1},
                                              verdict=self.spoken("GaLore falls short of Adam here")))
        self.assertIn("包含了调参用的种子", chinese)
        self.assertIn("八个样本的移动平均", chinese)
        self.assertIn("不做硬性的损失截断", chinese)

    def test_nested_literal_suffixes_omitted_by_simple_scanner_translate(self):
        # sources() flattens a conditional only one level. These actual source
        # leaves still reach the recursive translator at runtime.
        cases = [("s12_galore.py", "close to the window's own rank."),
                 ("s13_words.py", " The Pequod is Ahab's ship."),
                 ("s14_sgns.py", "On analogies word2vec does better.")]
        for filename, prefix in cases:
            literals = [n.value for n in ast.walk(ast.parse((PART / filename).read_text()))
                        if isinstance(n, ast.Constant) and isinstance(n.value, str)]
            english = next(x for x in literals if x.startswith(prefix))
            self.translated(english)

    def test_retrieval_availability_helpers_translate_without_nan_verdicts(self):
        tree = ast.parse((PART / "s18_netflix.py").read_text())
        helper = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                      and n.name == "retrieval_cohort_summary")
        env = {}
        exec(compile(ast.Module([helper], type_ignores=[]), "actual-retrieval-summary", "exec"), env)
        self.assertEqual(ambiguous("ai3"), [])
        cases = [(False, False, False, float("nan"), float("nan")),
                 (True, False, False, float("nan"), float("nan")),
                 (True, False, True, float("nan"), .15),
                 (True, True, False, .2, float("nan")),
                 (True, True, True, .2, .1), (True, True, True, .1, .2),
                 (True, True, True, .1, .1)]
        for eligible, model, baseline, recall, popularity in cases:
            cohort = dict(eligible=eligible, users=2 if eligible else 0, targets=4 if eligible else 0,
                          model_available=model, baseline_available=baseline,
                          recall=recall, popularity=popularity)
            warm = env["retrieval_cohort_summary"](cohort, "known users")
            cold = env["retrieval_cohort_summary"](cohort, "new users")
            english = self.spoken("Factorization has a weakness", warm_summary=warm, cold_summary=cold)
            chinese = self.translated(english)
            # Both helper summaries must be recovered completely and in order;
            # merely seeing both cohort names would miss a bad regex split.
            self.assertIn(self.translated(warm) + "另外，" + self.translated(cold), chinese)
            self.assertIn("已知用户", chinese)
            self.assertIn("新用户", chinese)
            self.assertNotIn("For known", chinese)
            self.assertNotIn("nan", chinese.lower())
            if not (eligible and model and baseline):
                self.assertIn("不可用", chinese)
                self.assertNotIn("没有胜过", chinese)
            elif recall <= popularity:
                self.assertIn("没有胜过热门推荐", chinese)
            else:
                self.assertIn("双塔胜过热门推荐", chinese)

    def test_all_narrated_templates_resolve_fields_and_preserve_bookmarks(self):
        # Strings stand in for fields; no model values or scene helpers are read.
        # This catches stale field names and bookmark loss after narration edits.
        covered = set()
        for row in sources("ai3"):
            with self.subTest(scene=row["scene"], source=row.get("en", row.get("tpl"))):
                covered.add(row["scene"])
                if "en" in row:
                    english = row["en"]
                else:
                    parts = _parts(ast.parse(row["tpl"], mode="eval").body)
                    english = "".join(value if kind == "text" else
                                      ("1.25" if numeric(value) else "SAMPLE")
                                      for kind, value in parts)
                self.translated(english)
        self.assertEqual(covered, set(table("ai3")["CHAPTERS"]))
        self.assertEqual(len(covered), 19)

    def test_all_chapter_helper_spoken_lines_translate(self):
        # chapter() wraps voiceover(), so the general voiceover scanner omits it.
        count = 0
        for path in sorted(PART.glob("s[0-9][0-9]_*.py")):
            for node in ast.walk(ast.parse(path.read_text())):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                        and node.func.id == "chapter" and len(node.args) >= 5):
                    with self.subTest(source=path.name, line=node.lineno):
                        self.translated(ast.literal_eval(node.args[4]))
                        count += 1
        self.assertEqual(count, 17)
