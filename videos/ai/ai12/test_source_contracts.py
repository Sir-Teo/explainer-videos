"""Part 12 source/translation contracts using synthetic inputs only.

Run this file directly with Python 3.12 and NumPy. Scenes and scientific
producers are read as AST, never imported; no experiment caches are needed.
These checks do not establish rendered layout, cached outcomes or speech sync.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import ast
import copy
import hashlib
import json
import math
import re
import types
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PART = ROOT / "videos/ai/ai12"

# The 79 reviewed Part 12 caption additions. Older catalog entries are outside
# the numeric-order contract because legitimate Chinese unit conversions exist.
REVIEWED_CAPTION_KEYS = (
    "in our code: \\ readout multiplier $64/n$, \\ hidden matrix's rate times $64/n$; \\\\ at width $64$, \\ both factors are $1$, \\ but only $\\mu$P starts its readout weights at zero",
    'at $10^{13}$ operations: \\\\ cheap-fit minimum $2.129$; \\\\ interpolated valley estimate $2.074$',
    'the output at $x = 0.5$ \\ over $6{,}000$ random starts; \\ yellow: \\ the Gaussian of variance $(x^2 + 1)/2 = 0.625$ \\\\ triangles: \\ density above $0.9$',
    'the network, \\ through training \\ (seed $0$)',
    'activation change: \\ $\\mathrm{std}(a_t-a_0)$; \\ steps $1$ to $4$ (fainter: earlier)',
    'computed: \\ Adam, learning rate $0.01$, \\ the same four batches at every width \\\\ zero first-step $\\mu$P hidden changes omitted on log axes',
    'independent tangent-kernel reference',
    'three seeds at widths $64$ and $256$, \\ through $2^{22}$ characters: \\ at most $0.058$ bits apart',
    'three seeds; \\ bands: \\ min to max; \\ two rates selected on seed $0$ test loss \\\\ lazy output centred at initialization; \\ kernel: \\ independent width $4{,}096$, \\ ridge $10^{-6}$',
    'white: \\ interpolated iso-FLOP crossings \\\\ curve: \\ fitted-law target',
    'epochs: \\ final bits, \\ three seeds \\\\ $100{,}000$ held-out predictions',
    'computed: \\ width $128${,} \\ $4{,}194{,}304$ characters of training in every run \\\\ curves: \\ seed $0${,} \\ $20{,}000$ held-out predictions',
    'white: \\ three-seed means interpolated \\\\ onto the fresh seed-$0$ curve',
    'teacher-forced accuracy \\\\ averaged over eight positions',
    'each subtask (row) at each width (column): \\\\ bright $=$ high loss, \\ dark $=$ low loss',
    'computed: \\ width $128${,} \\ batches $32$ to $4{,}096$ \\\\ best of three rates for each batch and target loss',
    'critical batch and gradient noise',
    'two mixture seeds; \\ dense: \\ seed $0$ \\\\ selected-expert work fixed; \\ routing adds overhead',
    'fit: \\ finite $\\delta>0.002$ bits, \\ $D\\ge2^{17}$ \\\\ $P$: bits kept; \\ shown $\\delta>10^{-4}$ bits',
    'one non-embedding weight-matrix row \\\\ ($3$ bits: \\ $7$ symmetric levels; \\ schematic)',
    'Round non-embedding weight matrices to four bits after training. \\ Which suffers more: \\ a model that read a little, \\ or the same model after reading much more?',
    'Experts add parameters with routing overhead; \\ fewer bits save memory, \\ at a price that grows with how much the model has read.',
    'computed: \\ available widths at $2^{22}$ characters \\\\ growth: \\ log-log fits{,} \\ score floor $1/2{,}000$',
    'oracle local Taylor pieces: \\ known function and gradients \\\\ two random-centre seeds on a $d$-dimensional torus',
    'assume data near a surface of dimension $d$',
    'assume about $N$ local pieces for $N$ parameters',
    'tasks with loss $<0.1$ bits',
    'ideal top-$n$ task tail \\\\ top tasks perfect; \\ others cost one bit',
    'left: \\ seed $0$; \\ right: \\ two seeds per width',
    'the $97$ number vectors, \\ final PCA directions \\\\ each snapshot rescaled for display',
    'an ideal Fourier representation',
    'ideal positive weights: \\ maximum at $c = a + b \\bmod 97$',
    'true-class tangent Gram: \\ cosine distance \\\\ $128$ examples ($64$ train, $64$ test); \\ log steps',
    'expected oracle coverage \\ ($L = 6$ characters exactly) \\\\ $2{,}000$ prefixes, \\ temperature $1$, \\ independent tries',
    'proxy $\\sim 1-\\mathrm{pass}@k$ only near coverage $1$; \\ fit: $k\\ge30$, \\ proxy $>10^{-4}$',
    'interpolated tries for expected coverage \\\\ matching the largest model at one try',
    'least-squares fit: \\ five weighted waves \\\\ $75\\%$ of centred logit variation (full $97^3$ table)',
    'dense: \\ all hidden-matrix entries used per character',
    "computed for this series: \\ $94$ completed primary endpoints of Part 11's character model",
    '$11$ widths, \\ $94$ primary endpoints \\\\ $1.0$ recorded elapsed hours \\\\ width runs, \\ including seed repeats',
    'the same form, \\ $465$ runs: \\ over-trained models are harder to quantize; \\ low precision in training acts like fewer parameters, $N(1 - e^{-P/\\gamma})$; \\ joint training optimum over size, data and precision: \\ $7$ to $8$ bits',
    'triangles: \\ off-scale or unstable learning-rate points',
    'quanta: \\ tasks; \\ white: weighted mean',
    'held-out bits per character \\\\ triangles: final curve points above range',
    'curves and green bars: \\ width $128$, \\ seed $0$',
    'At the optimum, size and data give equal marginal benefit per added operation: \\ for language models, \\ about $20$ tokens per parameter \\ (Hoffmann et al., 2022).',
    'up to about $4$ epochs: \\ almost as good as new data; \\\\ beyond $16$: \\ little left',
    'independent-token schematic',
    'Look beyond the score',
    'All-or-nothing scores can create apparent jumps; \\ individual task losses can change more sharply than their average. \\ Forecasts need validation beyond observed sizes.',
    'share in five strongest frequencies',
    'share of problems with $p < x$ \\ (log scale)',
    'proxy slope $-0.31$ \\quad CDF slope $0.32$',
    'modelled answer operations: \\ $k\\,2NL$ \\\\ $L=6$ characters per try',
    'For one problem, \\ more tries help exponentially fast. \\\\ Averaged over a whole benchmark, \\ will the failures also fall exponentially?',
    'Independent tries with an oracle checker can trade answer-time compute for model size; \\ suitable hard-problem tails can produce power-law-like failure decay over a finite range.',
    'The NTK limit is a kernel machine',
    'With neural-tangent scaling: \\ a Gaussian process at initialization; \\ a fixed tangent kernel and kernel-regression dynamics during training.',
    'Far below the critical batch, \\ a bigger batch saves steps with little extra data; \\ above it, savings diminish as data use grows. \\ Our fitted knee grew as loss fell.',
    'With substantial inference demand, \\ minimizing lifetime compute can favor a smaller model trained longer than the training-only optimum.',
    'For smooth targets, \\ local linear approximation predicts squared error $L \\propto N^{-4/d}$ asymptotically, \\ with $N$ pieces scaling like parameters; \\ an ideal Zipfian skill tail can also yield a power law.',
    'Measured curves guide forecasts; \\ costs matter',
    'Pretraining, reinforcement learning and answer-time compute show trends over studied ranges. \\ Historical efficiency gains reduced costs at fixed performance; \\ forecasts beyond those ranges need validation.',
    'NTK limit: \\ a frozen kernel',
    'fitted floor \\ $E = 1.77$',
    'white: \\ fitted \\\\ interpolated frontier',
    'held-out bits after $600$ steps \\\\ curves: two-seed means; \\ bands: seed range \\\\ dots: best sampled rates; \\ triangles: off-scale or unstable',
    'In this sweep, \\ the best sampled $\\mu$P rate stays put across widths; \\ useful rates can transfer from small to large models \\ \\mbox{(Yang et al., 2022)}.',
    '$9$ completed widths, \\ trained on $2^{24}$ characters',
    'width $512$, \\ lengths $2^{17}$ to $2^{24}$',
    'three seeds at widths $64$ and $256$, \\ through $2^{22}$ characters: \\ about $0.080$ bits apart',
    'our measured exponent: \\ $0.427$ to $0.431$ \\\\ central $80\\%$ of $100$ bootstrap refits',
    'left-out share across the full width sweep: \\\\ $70\\%$ of the smallest model, \\ $13\\%$ of the largest',
    'triangles: \\ fitted training cost above $16\\times$',
    'best-rate span: $0.3$ decades',
    'left: \\ seed $0$; \\ right: \\ two seeds per width \\\\ right plot omits fully learned runs',
    'fitted on $28$ cheap runs \\\\ of our $49$-run fit cohort \\\\ (up to $3 \\times 10^{12}$ operations)',
    'Fit the law on cheaper runs in our fit cohort and predict runs ten times costlier. \\ Will it miss by a hundredth of a bit, \\ a tenth, \\ or more?',
    'quanta: \\ tasks \\\\ white: weighted mean',
)


def tree(name):
    return ast.parse((PART / name).read_text())

def method(name, function):
    return next(n for n in ast.walk(tree(name)) if isinstance(n, ast.FunctionDef) and n.name == function)

def run_nodes(nodes, env):
    module = ast.fix_missing_locations(ast.Module(body=copy.deepcopy(nodes), type_ignores=[]))
    exec(compile(module, "<Part12 synthetic AST contract>", "exec"), env)
    return env

def assigned_name(node):
    return node.targets[0].id if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) else None

def literal_voiceover(name, function):
    return next(n.args[0].value for n in ast.walk(method(name, function))
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "voiceover"
                and isinstance(n.args[0], ast.Constant))

def literal_zh():
    node = next(n for n in tree("zh_lines.py").body if assigned_name(n) == "ZH")
    return ast.literal_eval(node.value)

class Part12SourceContracts(unittest.TestCase):
    def test_gap_comparisons_follow_width_identity_under_reordering(self):
        fn = method("s02_wide.py", "measure")
        nodes = [n for n in fn.body if assigned_name(n) in {"gap100", "gap10k"}]
        self.assertEqual(len(nodes), 2)
        env = run_nodes(nodes, {"np": np, "W": np.array([30000, 10000, 100]),
                                "z": {"lin_gap": [[99, 101], [2, 4], [6, 10]]}})
        self.assertEqual(env["gap100"], 8)
        self.assertEqual(env["gap10k"], 3)

    def test_missing_named_width_fails_instead_of_substituting_another_run(self):
        node = next(n for n in method("s02_wide.py", "measure").body if assigned_name(n) == "gap10k")
        with self.assertRaises(ValueError):
            run_nodes([node], {"np": np, "W": [100, 30000], "z": {"lin_gap": [[1], [2]]}})

    def test_depth_table_matches_preserved_block_rate_recipe(self):
        call = next(n for n in ast.walk(method("s06_depth.py", "stream"))
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "table_card")
        rows = ast.literal_eval(call.args[0])
        self.assertEqual([r[1] for r in rows[1:]], [r"$1$", r"$1/\sqrt{L/2}$", r"$1/(L/2)$"])
        self.assertEqual([r[2] for r in rows[1:]], [r"$\eta/(L/2)$", r"$\eta/\sqrt{L/2}$", r"$\eta$"])
        deep = method("charlm.py", "make_deep")
        group = next(n for n in ast.walk(deep) if isinstance(n, ast.FunctionDef) and n.name == "groups")
        block, other = object(), object()
        fake = types.SimpleNamespace(blocks=[types.SimpleNamespace(parameters=lambda: [block])],
                                     parameters=lambda: [block, other])
        for depth in (2, 8, 32):
            for alpha in (0, 0.5, 1):
                env = run_nodes([group], {"mL": depth / 2, "alpha": alpha})
                groups = env["groups"](fake, 0.01)
                self.assertEqual(groups[0]["params"], [other])
                self.assertAlmostEqual(groups[1]["lr"], 0.01 * (depth / 2) ** (alpha - 1))

    def test_initialization_qualifier_and_chinese_literal_parity(self):
        en = literal_voiceover("s04_mup.py", "table")
        zh = literal_zh()["For Adam, a common language-model optimizer"]
        self.assertIn("only mu-P starts the readout weights at zero", en)
        self.assertIn("只有μP的读出权重从零开始", zh)
        self.assertNotIn("same in both", en)
        self.assertEqual(re.findall(r"mark='(.)'", en), ["a", "b", "c"])
        self.assertEqual(re.findall(r"mark='(.)'", zh), ["a", "b", "c"])

    def test_depth_correction_preserves_bookmarks_and_chinese_meaning(self):
        en = literal_voiceover("s06_depth.py", "stream")
        zh = literal_zh()["Depth is the other way to grow."]
        self.assertIn("divides the block learning rate by the relative depth", en)
        self.assertIn("把块学习率除以相对深度", zh)
        self.assertEqual(re.findall(r"mark='(.)'", en), ["a", "b", "c", "d"])
        self.assertEqual(re.findall(r"mark='(.)'", zh), ["a", "b", "c", "d"])

    def test_attention_weights_and_targets_are_strictly_causal(self):
        fn = method("s19_outro.py", "next_time")
        names = {"source_index", "prefix", "g", "att", "src"}
        nodes = [n for n in fn.body if assigned_name(n) in names
                 or (isinstance(n, ast.AugAssign) and (isinstance(n.target, ast.Subscript)
                     and isinstance(n.target.value, ast.Name) and n.target.value.id == "att"
                     or isinstance(n.target, ast.Name) and n.target.id == "att"))]
        env = run_nodes(nodes, {"np": np, "toks": list(range(10))})
        self.assertEqual(env["src"], 7)
        self.assertEqual(env["prefix"], list(range(7)))
        self.assertEqual(len(env["att"]), 7)
        self.assertAlmostEqual(float(env["att"].sum()), 1)
        arc = next(n for n in ast.walk(fn) if isinstance(n, (ast.GeneratorExp, ast.ListComp))
                   and isinstance(n.elt, ast.Call) and "ArcBetweenPoints" in ast.unparse(n.elt))
        pairs = eval(compile(ast.Expression(arc.generators[0].iter), "<causal target contract>", "eval"), env)
        self.assertTrue(all(t < env["src"] and a > 0 for t, a in pairs))

    def test_surface_axis_labels_have_registration_reveal_and_cleanup(self):
        fn = method("s09_valley.py", "surface")
        calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call)]
        for attr in ("add_fixed_orientation_mobjects", "remove_fixed_orientation_mobjects"):
            call = next(n for n in calls if isinstance(n.func, ast.Attribute) and n.func.attr == attr)
            self.assertEqual([n.id for n in call.args], ["xl", "yl"])
        reveals = {n.args[0].id for n in calls if isinstance(n.func, ast.Name) and n.func.id == "FadeIn"
                   and n.args and isinstance(n.args[0], ast.Name)}
        self.assertTrue({"xl", "yl"} <= reveals)
        group = next(n for n in calls if isinstance(n.func, ast.Name) and n.func.id == "FadeOut"
                     and "axes, surf" in ast.unparse(n))
        self.assertTrue({"xl", "yl"} <= {n.id for n in ast.walk(group) if isinstance(n, ast.Name)})

    def test_frontier_caption_distinguishes_two_estimates(self):
        expr = next(n.args[0] for n in ast.walk(method("s18_frontier.py", "evidence"))
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "label"
                    and n.args and "cheap-fit minimum" in ast.unparse(n.args[0]))
        caption = eval(compile(ast.Expression(expr), "<synthetic optimum contract>", "eval"),
                       {"opt": {"pred": 9.876, "meas": 1.234}})
        self.assertIn("cheap-fit minimum $9.876$", caption)
        self.assertIn("interpolated valley estimate $1.234$", caption)
        self.assertNotIn("measured", caption)

    def test_reviewed_local_captions_preserve_number_order(self):
        local = json.loads((PART / "text_zh_add.json").read_text())["strings"]
        self.assertEqual(len(REVIEWED_CAPTION_KEYS), 79)
        self.assertEqual(len(set(REVIEWED_CAPTION_KEYS)), 79)
        number = re.compile(r"(?<![A-Za-z\\])-?\d+(?:(?:\{,\}|,|\.)\d+)*")
        # Restrict this contract to the reviewed additions. Older captions may
        # legitimately change units, for example billions to Chinese 亿.
        for en in REVIEWED_CAPTION_KEYS:
            with self.subTest(caption=en):
                self.assertIn(en, local)
                self.assertEqual(number.findall(en), number.findall(local[en]))

    def test_actual_narration_translator_fallback_handles_both_corrected_lines(self):
        # Execute the text-only translator with its package import replaced by a
        # path function. It parses scenes as text and imports only the data table.
        source = ast.parse((ROOT / "explainer/zh_templates.py").read_text())
        nodes = [n for n in source.body if not (isinstance(n, ast.ImportFrom) and n.module == "explainer.paths")]
        env = run_nodes(nodes, {"video_dir": lambda video: ROOT / "videos/ai" / video})
        translator = env["Translator"]("ai12")
        frozen = json.loads((PART / "narration_zh.json").read_text())["lines"]
        for file, function, prefix in (("s04_mup.py", "table", "For Adam, a common language-model optimizer"),
                                       ("s06_depth.py", "stream", "Depth is the other way to grow.")):
            en = literal_voiceover(file, function)
            key = hashlib.sha1(" ".join(en.split()).encode()).hexdigest()[:12]
            self.assertNotIn(key, frozen)
            self.assertEqual(translator(en), literal_zh()[prefix])

    def test_actual_numeric_caption_translator_preserves_distinct_new_estimates(self):
        source = ast.parse((ROOT / "explainer/zh_text.py").read_text())
        nodes = [n for n in source.body if not (isinstance(n, ast.ImportFrom)
                 and n.module in {"manim", "explainer.paths", "explainer"})]
        env = run_nodes(nodes, {"lang": types.SimpleNamespace(LANG="zh")})
        # Translate with an isolated local catalog; never modify the shared file.
        env["_TABLE"] = json.loads((PART / "text_zh_add.json").read_text())
        env["_BY_NUMBERS"] = None
        key = next(k for k in REVIEWED_CAPTION_KEYS if "cheap-fit minimum" in k)
        number = re.compile(r"\$\d+(?:\.\d+)?\$")
        self.assertEqual(len(number.findall(key)), 2)
        estimates = iter(("$9.876$", "$1.234$"))
        en = number.sub(lambda match: next(estimates), key)
        zh = env["translate"](en)
        self.assertIn("低算力拟合的最小值$9.876$", zh)
        self.assertIn("插值得到的山谷估计值$1.234$", zh)

    def test_kurtosis_rounding_does_not_display_negative_zero(self):
        helper = next(n for n in ast.parse((ROOT / "explainer/analysis/__init__.py").read_text()).body
                      if isinstance(n, ast.FunctionDef) and n.name == "nz")
        env = run_nodes([helper], {})
        expr = next(n.args[0] for n in ast.walk(method("s02_wide.py", "gaussian"))
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "label"
                    and n.args and "excess kurtosis" in ast.unparse(n.args[0]))
        for small in (-0.0015, 0.0015, 0.0):
            result = eval(compile(ast.Expression(expr), "<synthetic rounding contract>", "eval"),
                          dict(env, kurt=small))
            self.assertIn("$0.0$", result)
            self.assertNotIn("-0.0", result)

    def test_gap_narration_qualifies_seed_statistic_and_translates(self):
        source = ast.parse((ROOT / "explainer/zh_templates.py").read_text())
        env = run_nodes([n for n in source.body if not (isinstance(n, ast.ImportFrom) and n.module == "explainer.paths")],
                        {"video_dir": lambda video: ROOT / "videos/ai" / video})
        expr = next(n.args[0] for n in ast.walk(method("s02_wide.py", "measure"))
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "voiceover")
        en = eval(compile(ast.Expression(expr), "<synthetic gap narration contract>", "eval"),
                  {"sw":-0.55,"sk":-0.8,"gap100":0.35,"gap10k":0.07,
                   "said1":"Both shrink with width, though not exactly at the rates the theory predicts at infinite width. "})
        self.assertIn("Averaging each seed's maximum gap over three seeds", en)
        self.assertIn("The replay shows seed zero", en)
        zh = env["Translator"]("ai12")(" ".join(en.split()))
        self.assertIn("对三个种子求平均", zh)
        self.assertIn("回放展示的是种子0", zh)
        self.assertEqual(re.findall(r"mark='(.)'", en), re.findall(r"mark='(.)'", zh))

    def test_coordinate_narration_qualifies_unobserved_instability_and_translates(self):
        source = ast.parse((ROOT / "explainer/zh_templates.py").read_text())
        env = run_nodes([n for n in source.body if not (isinstance(n, ast.ImportFrom) and n.module == "explainer.paths")],
                        {"video_dir": lambda video: ROOT / "videos/ai" / video})
        nodes = [n for n in method("s04_mup.py", "coord").body if assigned_name(n) in {"said1", "said2"}]
        branch = run_nodes(nodes, {"grows":True, "flat":True, "s_sp":0.47, "s_mu":-0.02})
        expr = next(n.args[0] for n in ast.walk(method("s04_mup.py", "coord"))
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "voiceover")
        en = eval(compile(ast.Expression(expr), "<synthetic coordinate narration contract>", "eval"), branch)
        self.assertIn("can destabilize training", en)
        self.assertNotIn("eventually blows", en)
        zh = env["Translator"]("ai12")(" ".join(en.split()))
        self.assertIn("可能太大", zh)
        self.assertNotIn("最终", zh)
        self.assertEqual(re.findall(r"mark='(.)'", en), re.findall(r"mark='(.)'", zh))

    def test_seed_spread_covers_both_nonreference_seeds(self):
        nodes = method("s08_laws.py", "laws").body
        start = next(i for i, n in enumerate(nodes) if assigned_name(n) == "spread")
        end = next(i for i, n in enumerate(nodes) if assigned_name(n) == "sp")
        sample = {"ks":[16,17,18], "widths":[64,256], "extra":[[64,1],[64,2],[256,1],[256,2]],
                  "bits":[[3,3,3],[3,3,3]], "seed1_w64":[4,3,np.nan], "seed2_w64":[2,3,np.nan],
                  "seed1_w256":[3,3,np.nan], "seed2_w256":[3,3,np.nan]}
        env = run_nodes(nodes[start:end+1], {"s":sample, "np":np})
        self.assertEqual(env["sp"], 2)
        # Moving the reference seed to an extreme must not change the range.
        sample["bits"][0], sample["seed1_w64"] = sample["seed1_w64"], sample["bits"][0]
        self.assertEqual(run_nodes(nodes[start:end+1], {"s":sample, "np":np})["sp"], 2)

    def test_lazy_reference_is_independent_finite_width_in_both_branches_and_languages(self):
        producer = next(n for n in tree("toys.py").body if isinstance(n, ast.FunctionDef) and n.name == "kernel_regression")
        self.assertEqual(ast.literal_eval(producer.args.defaults[0]), 4096)
        source = ast.parse((ROOT / "explainer/zh_templates.py").read_text())
        env = run_nodes([n for n in source.body if not (isinstance(n, ast.ImportFrom) and n.module == "explainer.paths")],
                        {"video_dir": lambda video: ROOT / "videos/ai" / video})
        expr = next(n.value for n in method("s03_lazy.py", "race").body if assigned_name(n) == "said0")
        for kgap in (0.01, 0.5, -0.5):
            en = eval(compile(ast.Expression(expr), "<finite width reference contract>", "eval"), {"kgap":kgap})
            self.assertIn("independent", en)
            self.assertIn("4096", en)
            self.assertNotIn("its starting kernel", en)
            self.assertNotIn("computed exactly", en)
            zh = env["Translator"]("ai12")(en)
            self.assertIn("独立", zh)
            self.assertIn("4096", zh)
            self.assertNotIn("精确", zh)

    def test_lazy_weights_are_net_displacement_not_path_length(self):
        expr = next(n.args[0] for n in ast.walk(method("s03_lazy.py", "units"))
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "voiceover")
        en = eval(compile(ast.Expression(expr), "<net displacement contract>", "eval"), {"mvn":0.1,"mvm":0.9})
        self.assertIn("final weights are displaced by 10 percent", en)
        self.assertNotIn("weights travel", en)
        self.assertIn("fixed starting-kernel regression", en)

    def test_overtrain_crossing_count_does_not_claim_exact_observed_runs(self):
        source = ast.parse((ROOT / "explainer/zh_templates.py").read_text())
        env = run_nodes([n for n in source.body if not (isinstance(n, ast.ImportFrom) and n.module == "explainer.paths")],
                        {"video_dir": lambda video: ROOT / "videos/ai" / video})
        expr = next(n.value for n in method("s11_overtrain.py", "price").body if assigned_name(n) == "said1")
        for count in (0,1,4):
            en = eval(compile(ast.Expression(expr), "<interpolated crossings contract>", "eval"), {"meas":[None]*count})
            self.assertIn(f"{count} crossings", en)
            self.assertIn("Interpolating", en)
            self.assertNotIn("near the curve", en)
            zh = env["Translator"]("ai12")(en)
            self.assertIn(f"{count}个交点", zh)
            self.assertIn("插值", zh)


def translator():
    source=ast.parse((ROOT/'explainer/zh_templates.py').read_text())
    env=run_nodes([n for n in source.body if not (isinstance(n,ast.ImportFrom) and n.module=='explainer.paths')],
                  {'video_dir':lambda video:ROOT/'videos/ai'/video})
    return env['Translator']('ai12')

def assignment(file, function, name, env):
    node=next(n for n in method(file,function).body if assigned_name(n)==name)
    return eval(compile(ast.Expression(node.value),'<synthetic presentation branch>','eval'),env)

def narrated(file, function, env):
    expr=next(n.args[0] for n in ast.walk(method(file,function)) if isinstance(n,ast.Call)
              and isinstance(n.func,ast.Attribute) and n.func.attr=='voiceover')
    return eval(compile(ast.Expression(expr),'<synthetic narration contract>','eval'),env)

class ScalingPresentationContracts(unittest.TestCase):
    def assertTranslated(self, en, *phrases):
        zh=translator()(' '.join(en.split()))
        self.assertIsNotNone(zh)
        self.assertEqual(re.findall(r"mark='(.)'",en),re.findall(r"mark='(.)'",zh))
        for phrase in phrases:self.assertIn(phrase,zh)
        return zh

    def test_teacher_forced_average_and_first_character_are_distinct_metrics(self):
        function=next(n for n in tree('compute.py').body if isinstance(n,ast.FunctionDef) and n.name=='compute_emerge')
        nodes=[n for n in function.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Subscript)
               and isinstance(n.targets[0].slice,ast.Constant) and n.targets[0].slice.value in ['char_acc','exact']]
        top=np.zeros((1,2,8),bool);top[:,:,0]=True
        env=run_nodes(nodes,{'out':{},'top':top,'gr':top})
        self.assertEqual(env['out']['char_acc'][0],1/8)
        self.assertEqual(env['out']['exact'][0,0],1)
        v={'acc':np.array([.2,.3]),'g8':2.5,'g1':1.2,'e':{'task_n':2000}}
        v['said1']=assignment('s15_emerge.py','ours','said1',v)
        en=narrated('s15_emerge.py','ours',v)
        self.assertNotIn('the same curve',en)
        self.assertIn('teacher-forced',en)
        self.assertTranslated(en,'教师强制','只使用第一个位置','2.5','1.2')

    def test_emerge_cliff_fallback_and_selected_cohort_translate(self):
        for cliff in [False,True]:
            v={'cliff':cliff,'drops':[.8,.7,.6],'np':np}
            v['said2']=assignment('s15_emerge.py','real','said2',v)
            en=narrated('s15_emerge.py','real',v)
            self.assertNotIn('either solved or not',en)
            self.assertNotIn('common subtasks first',en)
            zh=self.assertTranslated(en,'连续','加权','不能证明')
            if cliff:self.assertIn('3个',zh)

    def test_data_curve_and_aggregate_provenance_translate(self):
        for overfit in [True,False]:
            v={'total':2**22,'d4':.04,'d16':.11,'worst':.5,'overfit':overfit}
            for name in ['said1','said2']:v[name]=assignment('s12_data.py','repeat',name,v)
            en=narrated('s12_data.py','repeat',v)
            self.assertNotIn('memorizes its sample',en)
            zh=self.assertTranslated(en,'0.50')
            if overfit:self.assertIn('三个种子的最终均值',zh)

    def test_quantizer_selection_matches_scoped_explanation(self):
        fn=next(n for n in tree('charlm.py').body if isinstance(n,ast.FunctionDef) and n.name=='quantized_bits')
        node=next(n for n in fn.body if assigned_name(n)=='mats')
        matrix=types.SimpleNamespace(ndim=2);embedding=types.SimpleNamespace(ndim=2);bias=types.SimpleNamespace(ndim=1)
        model=types.SimpleNamespace(named_parameters=lambda:[('h2.weight',matrix),('emb.weight',embedding),('h2.bias',bias)])
        self.assertEqual(run_nodes([node],{'model':model})['mats'],[matrix])
        v={'d4':np.array([.1,.4]),'okk':np.array([True,True]),'lD':np.array([16,24]),'gD':.4,'gN':.3}
        v['said2']=assignment('s13_experts.py','bits','said2',v)
        self.assertTranslated(narrated('s13_experts.py','bits',v),'非嵌入','偏置保持不变','0.002','17次方','联合优化大小、数据和训练精度')

    def test_dense_size_interpolation_and_out_of_range_branches_translate(self):
        for target in [3.,1.]:
            v={'dL':np.array([2.,4.]),'okd':np.array([True,True]),'mm':np.array([3.5,target,2.4]),
               'i8':1,'effN':np.array([100.,200.,300.]),'mult':2.}
            v['match']=assignment('s13_experts.py','experts','match',v)
            v['said1']=assignment('s13_experts.py','experts','said1',v)
            en=narrated('s13_experts.py','experts',v)
            zh=self.assertTranslated(en,'路由','平均损失')
            self.assertNotIn('The mean loss',zh)
            if target==3.:self.assertIn('插值',zh)
            else:
                self.assertIn('无法确定',zh)
                self.assertNotIn('200',v['match'])

    def test_reviewed_local_captions_do_not_conflict_with_shared_entries(self):
        local = json.loads((PART / "text_zh_add.json").read_text())["strings"]
        shared = json.loads((ROOT / "videos/ai/ai_text_zh.json").read_text())["strings"]
        for en in REVIEWED_CAPTION_KEYS:
            with self.subTest(caption=en):
                self.assertIn(en, local)
                # Shared integration may be pending or already completed.
                if en in shared:
                    self.assertEqual(shared[en], local[en])

    def test_power_ranges_preserve_measured_extremes(self):
        v={'run':np.array([[1.45,.2],[.01,1.]]),'math':math}
        self.assertGreaterEqual(assignment('s14_power.py','toy','ytop',v),v['run'].max())
        node=next(n for n in method('s14_power.py','manifold').body if isinstance(n,ast.Assign)
                  and isinstance(n.targets[0],ast.Tuple)
                  and [getattr(t,'id',None) for t in n.targets[0].elts]==['y0','y1'])
        values=np.array([-16.67,-.1]);env=run_nodes([node],{'allv':values,'math':math})
        self.assertLessEqual(env['y0'],values.min())
        self.assertGreaterEqual(env['y1'],values.max())

    def test_power_oracle_and_finite_slope_qualifications_translate(self):
        v={'s8':-.3,'t8':-.5};v['said1']=assignment('s14_power.py','manifold','said1',v)
        en=narrated('s14_power.py','manifold',v)
        self.assertIn('oracle approximation',en)
        self.assertNotIn('on its way',en)
        self.assertTranslated(en,'解析梯度','不训练网络','不能证明渐近收敛')

    def test_power_weak_order_and_discrepancy_fallbacks_do_not_claim_agreement(self):
        for order in [-.8,.2,.9]:
            for below in [-.2,.4]:
                v={'in_order':order,'below':below,'widths':[8,128,512],'wi':1,'T':32,'n_learn':13,
                   'lo':1,'full':[512],'learned':np.array([[1,1],[10,13],[32,32]])}
                for name in ['said2','said3','said4','said5']:v[name]=assignment('s14_power.py','toy',name,v)
                en=narrated('s14_power.py','toy',v)
                self.assertNotIn('Ours sit on it',en)
                self.assertNotIn('order roughly follows',en)
                self.assertTranslated(en,'0.1比特','理想','加权损失' if below>=-.1 else '其余损失')

    def test_grok_generalization_status_is_recorded_and_bounded(self):
        for crossing in [None,1500]:
            v={'g':{'t_test_nowd':crossing},'after':.02,'kdn':np.array([.05]),'r2':.75}
            v['nowd_status']=assignment('s16_grok.py','circuit','nowd_status',v)
            v['said5']=assignment('s16_grok.py','circuit','said5',v)
            en=narrated('s16_grok.py','circuit',v)
            self.assertNotIn('never generalizes',en)
            self.assertIn('separately weighted',en)
            zh=self.assertTranslated(en,'中心化','真实类别','梯度Gram矩阵','归一化','95%')
            self.assertIn('没有超过' if crossing is None else '1500',zh)
        literals=[n.value for n in ast.walk(method('s16_grok.py','circuit')) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
        self.assertTrue(any(r'\alpha_k' in s for s in literals))

    def test_grok_cosine_distance_does_not_measure_kernel_scale(self):
        fn=next(n for n in tree('grok.py').body if isinstance(n,ast.FunctionDef) and n.name=='run')
        expr=next(n.args[0] for n in ast.walk(fn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)
                  and isinstance(n.func.value,ast.Name) and n.func.value.id=='kd' and n.func.attr=='append')
        original=np.array([[1.,2.],[2.,4.]]);scaled=3*original
        distance=eval(compile(ast.Expression(expr),'<cosine metric counterexample>','eval'),{'K':scaled,'K0':original,'np':np})
        self.assertAlmostEqual(distance,0)
        self.assertGreater(np.linalg.norm(scaled-original),0)

    def test_testtime_is_analytic_expected_oracle_coverage(self):
        fn=next(n for n in tree('compute.py').body if isinstance(n,ast.FunctionDef) and n.name=='compute_testtime')
        node=next(n for n in fn.body if assigned_name(n)=='cov')
        p=np.array([[.1,.2,.6],[.01,.5,.7]]);ks=np.array([1.,10.,100.])
        actual=run_nodes([node],{'p':p,'ks':ks,'np':np})['cov']
        expected=np.array([[1-np.mean((1-row)**k) for k in ks] for row in p])
        np.testing.assert_allclose(actual,expected)
        en=narrated('s17_testtime.py','tries',{'L':6})
        self.assertIn('compute the expected share',en)
        self.assertTranslated(en,'温度1','预期覆盖率','完美的正确答案判定器')

    def test_testtime_proxy_and_failure_are_distinct_and_missing_slopes_translate(self):
        self.assertNotAlmostEqual(-math.log(.1),1-.1)
        for beta,tail in [(.4,.65),(float('nan'),float('nan'))]:
            v={'np':np,'b':np.array([beta]),'tb':np.array([tail]),'i':0}
            for name in ['slope_statement','said1']:v[name]=assignment('s17_testtime.py','why',name,v)
            en=narrated('s17_testtime.py','why',v)
            self.assertNotIn('nan',en)
            self.assertIn('only near full coverage',en)
            self.assertTranslated(en,'整体的k次方','只在覆盖率接近1时','有限基准')

    def test_testtime_crossings_are_interpolated_expectations(self):
        en=narrated('s17_testtime.py','trade',{'need':np.array([10.,1.]),'i_small':0,'said2':''})
        self.assertIn('interpolated expectations',en)
        self.assertNotIn('the next ones fewer',en)
        self.assertTranslated(en,'插值','不是新的解码实验')

    def test_host_provenance_and_elapsed_time_are_scoped(self):
        en=narrated('s01_hook.py','law',{'widths':[16,32,64],'s':{'ks':list(range(16,25))},'n_runs':94,'E':1.7,'slope':-.2})
        self.assertNotIn('computer making',en)
        self.assertTranslated(en,'主扫描终点','为这个系列')
        en=narrated('s08_laws.py','method',{'widths':[16,32,64],'n_runs':94,'hours':1.2})
        self.assertIn('elapsed hours',en)
        self.assertNotIn('one processor',en)
        self.assertTranslated(en,'种子重复','1.2小时','不包含最初的学习率搜索')

    def test_recap_does_not_flatten_omitted_rate_points_or_quanta_losses(self):
        fn=method('s19_outro.py','tiles')
        call=next(n for n in ast.walk(fn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)
                  and n.func.id=='curve' and isinstance(n.args[0],ast.Name) and n.args[0].id=='a4')
        visible=next(n for n in ast.parse((PART/'common.py').read_text()).body
                     if isinstance(n,ast.FunctionDef) and n.name=='visible_values')
        env=run_nodes([visible],{'np':np,'v':np.array([2.,7.,np.inf]),'lo':1.,'hi4':4.})
        values=eval(compile(ast.Expression(call.args[2]),'<recap overflow contract>','eval'),env)
        self.assertEqual(values[0],2.)
        self.assertTrue(np.isnan(values[1:]).all())
        call=next(n for n in ast.walk(fn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)
                  and n.func.id=='curve' and isinstance(n.args[0],ast.Name) and n.args[0].id=='a7'
                  and isinstance(n.args[2],ast.Subscript) and isinstance(n.args[2].value,ast.Name)
                  and n.args[2].value.id=='per')
        per=np.array([[[[1.45,1.],[.02,.1]]]])
        values=eval(compile(ast.Expression(call.args[2]),'<recap raw losses contract>','eval'),{'np':np,'per':per,'wi':0,'k':0})
        self.assertEqual(values[0],1.45)
        mean_call=next(n for n in ast.walk(fn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)
                       and n.func.id=='curve' and isinstance(n.args[0],ast.Name) and n.args[0].id=='a7'
                       and 'q[' in ast.unparse(n.args[2]))
        expected=(per*np.array([.8,.2])).sum(-1)
        values=eval(compile(ast.Expression(mean_call.args[2]),'<recap actual mean contract>','eval'),
                    {'np':np,'q':{'mean':expected},'wi':0})
        np.testing.assert_array_equal(values,expected[0,0])
        self.assertTranslated(narrated('s19_outro.py','recap',{}),'固定的核','不同时间')

    def test_compute_optimum_equates_benefit_per_operation_not_per_unit(self):
        # L=1/N+4/D at N=2,D=8 satisfies N|L_N|=D|L_D|.
        # Its raw marginal benefits differ; dividing by marginal FLOP cost
        # gives the actual equality asserted in the derivation and takeaway.
        N,D=2.,8.
        size_benefit=1/N**2
        data_benefit=4/D**2
        self.assertNotEqual(size_benefit,data_benefit)
        self.assertAlmostEqual(size_benefit/(6*D),data_benefit/(6*N))
        en=narrated('s09_valley.py','lagrange',{'ch':{'n_points':50,'rms':.02},'a3':.43})
        self.assertIn('per added operation',en)
        self.assertTranslated(en,'每增加一次运算','边际损失下降')
        en=narrated('s09_valley.py','takeaway',{})
        self.assertNotIn('last parameter',en)
        self.assertTranslated(en,'额外算力','边际回报')

    def test_emerge_takeaway_keeps_metric_and_forecast_limits(self):
        en=narrated('s15_emerge.py','takeaway',{})
        self.assertIn('can make',en)
        self.assertIn('without demonstrating a mathematical discontinuity',en)
        self.assertIn('validation beyond the sizes we observed',en)
        self.assertNotIn('truly switch on',en)
        self.assertTranslated(en,'不代表数学上的不连续','预测需要验证')

    def test_testtime_takeaway_preserves_tail_and_range_conditions(self):
        en=narrated('s17_testtime.py','takeaway',{})
        self.assertIn('independent tries can',en)
        self.assertIn('suitable tail',en)
        self.assertIn('finite range',en)
        self.assertIn('need checking on each benchmark',en)
        self.assertTranslated(en,'独立尝试可以','合适的难题尾部','有限范围','每个基准上检验')

    def test_batch_above_knee_still_saves_steps_at_greater_data_cost(self):
        # Normalize Smin=Bcrit=1 in the stated tradeoff model.
        steps=lambda batch:1+1/batch
        self.assertLess(steps(4),steps(2))
        self.assertGreater(4*steps(4),2*steps(2))
        en=narrated('s07_batch.py','takeaway',{})
        self.assertNotIn('only wastes',en)
        self.assertTranslated(en,'节省逐渐减小','数据用量继续增加','我们拟合的')

    def test_summary_assumptions_survive_actual_chinese_templates(self):
        cases=[
            ('s02_wide.py','takeaway','neural-tangent scaling',['神经正切缩放']),
            ('s11_overtrain.py','takeaway','enough requests',['足够多的请求','可能']),
            ('s14_power.py','takeaway','under their assumptions',['假设','平方误差']),
            ('s18_frontier.py','takeaway','fixed performance',['固定性能','外推需要验证']),
            ('s19_outro.py','recap','Over measured ranges',['测量过的范围','神经正切缩放']),
        ]
        for file,beat,qualification,phrases in cases:
            with self.subTest(file=file):
                en=narrated(file,beat,{})
                self.assertIn(qualification,en)
                self.assertTranslated(en,*phrases)

    def test_across_depth_span_does_not_become_endpoint_motion(self):
        rates=np.array([-1.,-1.5,-1.])
        self.assertNotEqual(np.ptp(rates),abs(rates[-1]-rates[0]))
        fn=method('s06_depth.py','sweeps')
        branch=next(n for n in fn.body if isinstance(n,ast.If)
                    and any(assigned_name(k)=='said0' for k in n.body))
        for span in [0.,float(np.ptp(rates))]:
            env=run_nodes([branch],{'dr':{0.:span},'dir0':'the same'})
            en=env['said0']
            self.assertIn('tested depths',en)
            if span:
                self.assertIn('spans',en)
                self.assertNotIn('between the shallowest and the deepest',en)
            self.assertTranslated(en,'测试深度','最佳采样学习率')

class TranslationSchemaContracts(unittest.TestCase):
    def test_caption_entries_are_strings(self):
        entries=json.loads((PART/'text_zh_add.json').read_text())['strings']
        self.assertTrue(all(isinstance(k,str) and isinstance(v,str) for k,v in entries.items()))


if __name__ == "__main__":
    if sys.version_info[:2] != (3, 12):
        raise SystemExit("These source-template contracts require Python 3.12.")
    unittest.main()
