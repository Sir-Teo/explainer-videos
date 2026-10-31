"""Part 4 bilingual narration contracts, with no scene imports or data loading.

The AST inventory check covers every scene. Separate tests evaluate the actual
pure verdict helpers on meaningful numeric/boundary cases and send the resulting
English through the real translator, including nested fragments. This is source
and translation QA, not rendered narration, listening, or measured default QA.
"""
import ast
from collections import Counter
import math
from pathlib import Path
import re
import string
import unittest

import numpy as np

from explainer.zh_templates import Translator, _parts, source_startswith, sources, table


ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / "videos/ai/ai4"
BOOKMARK = r"<bookmark[^>]+/>"


def tree(filename):
    return ast.parse((PART / filename).read_text())


def helpers(filename, *names):
    nodes = [next(n for n in tree(filename).body
                  if isinstance(n, ast.FunctionDef) and n.name == name) for name in names]
    module = ast.Module(nodes, type_ignores=[])
    assert not any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(module))
    env = {"math": math, "np": np}
    exec(compile(module, "isolated-ai4-narration-helper", "exec"), env)
    return env


def assignment(filename, name, values, *, contains=None):
    node = next(n for n in ast.walk(tree(filename)) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)
                and (contains is None or contains in ast.unparse(n.value)))
    return eval(compile(ast.Expression(node.value), "actual-ai4-fragment", "eval"),
                {"math": math, "np": np}, values)


def field_identity(field):
    # Normalize quote spelling inside dictionary-index fields while retaining
    # format precision: changing .3f to .1f is a real narration contract change.
    pieces = list(string.Formatter().parse("{" + field + "}"))
    _, expression, spec, conversion = pieces[0]
    return ast.dump(ast.parse(expression, mode="eval"), include_attributes=False), spec, conversion


class Part4NarrationTests(unittest.TestCase):
    def setUp(self):
        self.tr = Translator("ai4")

    def translated(self, english):
        chinese = self.tr(english)
        self.assertIsNotNone(chinese, english)
        self.assertRegex(chinese, r"[\u4e00-\u9fff]")
        self.assertNotRegex(chinese, r"\{[^{}]+\}")
        self.assertEqual(re.findall(BOOKMARK, english), re.findall(BOOKMARK, chinese))
        return chinese

    def spoken(self, prefix, **values):
        row = next(r for r in sources("ai4") if prefix in r.get("en", r.get("tpl", "")))
        if "en" in row:
            return row["en"]
        return eval(compile(ast.parse(row["tpl"], mode="eval"), "actual-ai4-voiceover", "eval"),
                    {"math": math, "np": np}, values)

    def qualifiers(self, english, *terms):
        chinese = self.translated(english)
        for term in terms:
            self.assertIn(term, chinese)
        return chinese

    def test_all_nineteen_scene_sources_preserve_fields_and_bookmarks(self):
        # This checks the real winning lookup entry, so a surviving broad old
        # prefix cannot silently shadow a new qualification or numeric field.
        covered = set()
        for row in sources("ai4"):
            source = row.get("en", row.get("tpl"))
            with self.subTest(scene=row["scene"], source=source[:90]):
                covered.add(row["scene"])
                if "en" in row:
                    self.translated(source)
                    continue
                keys = [k for k in self.tr.zh if source_startswith(source, k)]
                self.assertTrue(keys, source)
                chinese = self.tr.zh[max(keys, key=len)]
                expected = Counter(field_identity(v) for kind, v in
                                   _parts(ast.parse(source, mode="eval").body) if kind == "name")
                actual = Counter(field_identity(v + (":" + spec if spec else ""))
                                 for _, v, spec, _ in string.Formatter().parse(chinese) if v is not None)
                self.assertEqual(expected, actual)
                self.assertEqual(re.findall(BOOKMARK, source), re.findall(BOOKMARK, chinese))
        self.assertEqual(covered, set(table("ai4")["CHAPTERS"]))
        self.assertEqual(len(covered), 19)

    def test_head_units_history_and_zero_gradient_are_not_shadowed(self):
        self.qualifiers(self.spoken("In part one we worked out", p={"gpt2": 124_439_808, "qwen3_4b": 4_022_468_096}),
                        "自然对数", "ln 2", "全参数", "4.02")
        self.qualifiers(self.spoken("The mathematics is three centuries"), "1986", "隐藏表示")
        self.qualifiers(self.spoken("Why steepest?"), "非零", "零向量", "一阶")
        self.qualifiers(self.spoken("In general, a map from n numbers"), "绝对值", "基础")
        self.qualifiers(self.spoken("Next, the softmax"), "自然对数", "比特", "ln 2")

    def test_jacobian_bound_and_both_observed_depth_branches(self):
        for steady, marker in [(True, "不到一个数量级"), (False, "超过一个数量级")]:
            verdict = assignment("s04_jacobian.py", "verdict", {"steady": steady})
            chinese = self.qualifiers(self.spoken("Chain many maps", L=40, gains=[.5,.8,1.,1.2,1.5],
                                                  m0=-12.4, m4=8.6, verdict=verdict),
                                      "至多", "不一定", "最大", "每个方向")
            self.assertIn(marker, chinese)
            self.assertNotIn("At gain one", chinese)

    def test_modes_preserve_parameter_only_work_and_benchmark_scope(self):
        timing = assignment("s06_modes.py", "timing", {"tr_": 64.8128})
        chinese = self.qualifiers(self.spoken("Training is the extreme case", P=874, cr=874.,
                                               tr_=64.8128, timing=timing, p={"gpt2":124_439_808}),
                                   "参数梯度", "输入梯度", "置信区间", "通用下界", "混合", "64.81")
        self.assertNotIn("every network", chinese)
        self.assertNotIn("The observed", chinese)

    def test_rank_zero_and_shape_limit_nested_branches(self):
        for rank, expected in [(0,"零"),(1,"非零"),(2,"容差")]:
            one = assignment("s07_backprop.py", "one_rank", {"n_nonzero": rank})
            batch = assignment("s07_backprop.py", "batch_rank", {"rank_b":2,"dh":4,"din":3})
            chinese = self.qualifiers(self.spoken("Here is that outer product", n_nonzero=rank,
                                                  one_rank=one, B=2, rank_b=2, dh=4, din=3,
                                                  batch_rank=batch), "至多", "批次", "绝对差", expected)
            self.assertIn("低于", chinese)
            self.assertNotIn("the zero", chinese)

    def test_library_zero_and_nonzero_error_reports_translate_recursively(self):
        gap = helpers("s08_library.py", "gap_report")["gap_report"]
        for fd, pt in [(0.,0.),(2.2e-10,2.8e-17)]:
            chinese = self.qualifiers(self.spoken("Does it work?", fd_result=gap(fd),pt_result=gap(pt)),
                                       "两个方向", "中心差分", "绝对误差", "不是")
            self.assertNotIn("largest absolute difference",chinese)
            if fd == 0:
                self.assertEqual(chinese.count("恰好为0"),2)
            else:
                self.assertIn("10",chinese)
                self.assertIn("-10",chinese)

    def test_train_finite_weak_and_undefined_outcomes_remain_observable(self):
        readout = helpers("s09_train.py", "training_readout")["training_readout"]
        for bits,corr in [(3.335,.996),(3.7,.2),(3.7,None)]:
            d = dict(bits_train=bits,bits_valid=bits+.1,H_cond=3.331,corr=corr,steps=1500,
                     metrics={"correlation":{"threshold":1e-4,"count":552}})
            result = readout(d)
            chinese = self.qualifiers(self.spoken("Raw scores can shift", **result),
                                       "有限次", "归一化", "1500", "552")
            self.assertNotIn("After 1500",chinese)
            if bits > 3.4:self.assertIn("尚未",chinese)
            if corr is None:self.assertIn("未定义",chinese)
            else:self.assertIn(f"{corr:.3f}",chinese)
        self.qualifiers(self.spoken("Now let's train",d={"H_cond":3.331}),
                        "Adam", "不是原始", "更新之后", "更新之前", "完整语料")
        self.qualifiers(self.spoken("Before we train, look"),"纳特", "比特")

    def test_train_late_window_does_not_become_global_convergence(self):
        for spread in [[0,0,.0001,.01],[0,0,.01,.02]]:
            # Execute the actual conditional, not a duplicated expected branch.
            branch=next(n for n in ast.walk(tree("s09_train.py")) if isinstance(n,ast.If)
                        and ast.dump(n.test)==ast.dump(ast.parse("settled[2] and not settled[3]",mode="eval").body))
            env=dict(d={"metrics":{"final_tail_states":500}},e2=20.,e3=40.,m=[0,0,3.4,3.5],
                     sp=spread,settled=[s<1e-3 for s in spread])
            exec(compile(ast.Module([branch],type_ignores=[]),"actual-late-window","exec"),env)
            english=self.spoken("How large a step can plain full-batch",d={"lam0":.01,"eta0":200.,
                                "lam_star":.08,"eta_star":25.},verdict=env["verdict"])
            self.qualifiers(english,"局部", "不是全局", "500", "比特")

    def test_float_domains_and_finite_score_qualification_survive(self):
        self.qualifiers(self.spoken("Every number in this series"),"正规有限", "运算顺序", "没有无穷大")
        info={"fp32":{"digits":7.2},"bf16":{"digits":2.1},"fp16":{"max":65504},"e4m3":{"max":448}}
        self.qualifiers(self.spoken("The gap between neighbouring",info=info),
                        "固定", "绝对间隔", "下溢", "可以达到1", "通常")
        self.qualifiers(self.spoken("Range has consequences",ov={"fp32":88.7,"fp16":11.1}),
                        "有限分数", "不会上溢", "下溢为0")

    def test_gradient_check_optimum_and_unavailable_branches(self):
        f=helpers("s11_vcurve.py","prediction_verdict")["prediction_verdict"]
        for ratios,marker in [([1.1,.8],"3倍"),([4.,.8],"不是保证"),([],"无法"),([math.nan],"无法")]:
            self.qualifiers(f(ratios),marker)
        self.qualifiers(self.spoken("A gradient check is a cancellation"),"局部模型", "三阶导数不为0")
        self.qualifiers(self.spoken("One more way numbers go wrong"),"抽样范围", "包括0", "下限")

    def test_gradient_check_nested_measured_fragments_keep_aggregate_meaning(self):
        verdict = helpers("s11_vcurve.py", "prediction_verdict")["prediction_verdict"]
        for finite in [True, False]:
            values = dict(slope=2.02 if finite else math.nan,
                          e6=2e-9 if finite else math.nan,
                          e64=1e-10 if finite else math.nan,
                          e32=2e-4 if finite else math.nan)
            fragments = {name: assignment("s11_vcurve.py", name, values)
                         for name in ["slope_v", "step_v", "error_v"]}
            chinese = self.qualifiers(self.spoken("Here it is measured, on chapter seven", **fragments,
                                                 verdict=verdict([1.1,.8] if finite else [])),
                                      "相同的8个", "中位数曲线", "并不是8个", "局部误差模型")
            self.assertNotIn("At chapter", chinese)
            self.assertNotIn("There are too few", chinese)
            self.assertIn("2.02" if finite else "无法报告", chinese)

    def test_memory_reference_outside_span_and_unavailable_scaling(self):
        f=helpers("s12_memory.py","checkpoint_verdict")["checkpoint_verdict"]
        for lo,hi,ns,ks,marker in [(3,5,[100],[10.],"跨度内"),(1,2,[],[],"跨度之外")]:
            verdict,scaling=f(16,lo,hi,ns,ks)
            chinese=self.qualifiers(self.spoken("Counted in an ideal",n=16,peak=np.array([16,8,9]),lo=lo,hi=hi,
                                                verdict=verdict,evals=np.array([16,28,30]),k_rt=1,
                                                d={"none_evals":136},scaling=scaling,ratio=1.4,
                                                gradient_v="The gradient comparison is not finite."),
                                    "理想", "逻辑", "不是实测物理内存", marker, "不是有限")
            self.assertNotIn("No finite",chinese)
            if not ns:self.assertIn("没有可用",chinese)
        self.qualifiers(self.spoken("The way out is to trade"),"对数级重算", "n乘以log n")

    def test_newton_censored_unavailable_and_threshold_results(self):
        f=helpers("s13_newton.py","convergence_summary","digit_summary")
        for status,first,criterion,marker in [("converged",3,"objective gap","首次"),
                ("capped",None,"objective gap","截断"),("nonfinite",None,"objective gap","有限"),
                ("capped",None,"reference unavailable","不可用")]:
            record=dict(status=status,first_hit_step=first,cap=12,criterion=criterion)
            gd=f['convergence_summary'](record,"Gradient descent")
            nw=f['convergence_summary'](record,"Newton")
            english=self.spoken("A test: logistic regression",d={"kappa":25},gd_summary=gd,nw_summary=nw,
                                digit_v=f['digit_summary']([.1,.01,.001]))
            chinese=self.qualifiers(english,marker,"每一步的工作量", "足够接近", "非奇异", "不能证明")
            self.assertNotIn("objective gap",chinese)
        self.qualifiers(self.spoken("The gradient says which way"),"驻点", "本身并不能")

    def test_hvp_signed_target_and_changing_relative_cutoffs(self):
        f=helpers("s14_hvp.py","curvature_verdict","radius_verdict")
        for a,b,marker in [(4,2,"减少"),(2,4,"增加"),(2,2,"中间"),(None,None,"无法")]:
            neg=f['curvature_verdict']({'negative':a},{'negative':b})
            radius=f['radius_verdict']({'rho':2.},{'rho':3.})
            chinese=self.qualifiers(self.spoken("Now watch a landscape",P=20,K=2,y=[0,1,2],
                initial_v=assignment("s14_hvp.py","initial_v",{"mixed":True}),
                neg_v=neg,final_v="At the final checkpoint the relative cutoff counts are undefined.",radius_v=radius),
                marker,"驻点鞍点", "各个检查点", "并不是拟合", "3")
            self.assertNotIn("The count",chinese)
        self.qualifiers(self.spoken("Check it on the stored final",d={"hv_full_diff":0.,"fd_best":1e-7},ratio=2.,
            power_v=assignment("s14_hvp.py","power_v",{},contains="unavailable")),
            "可能为负", "并不等于代数值最大", "无法", "不显示")

    def test_quadratic_norm_vs_objective_and_capped_thresholds(self):
        self.qualifiers(self.spoken("On a quadratic bowl"),"正定", "位置误差范数", "平方")
        f=helpers("s15_quadratic.py","rate_comparison","threshold_summary","escape_comparison")
        for gap,marker in [(0.,"百万分之一"),(.25,"0.250000"),(math.nan,"无法")]:
            self.qualifiers(f['rate_comparison'](gap),marker)
        for status,hit,marker in [("converged",1200,"达到了"),("capped",None,"没有达到"),("nonfinite",None,"不报告")]:
            self.qualifiers(f['threshold_summary'](dict(status=status,first_hit_step=hit,cap=1500)),marker)
        for slope,marker in [(2.,"10%"),(3.,"大于"),(1.,"小于"),(math.nan,"太少")]:
            self.qualifiers(f['escape_comparison'](slope,2.),marker)

    def test_lagrange_solver_failure_and_two_beta_conventions(self):
        f=helpers("s16_lagrange.py","solver_agreement")['solver_agreement']
        for success,difference,marker in [(False,0.,"没有报告成功"),(True,math.nan,"无法"),
                                         (True,1e-8,"容差内"),(True,.1,"超出")]:
            agreement=f(success,difference,1e-4)
            self.qualifiers(self.spoken("A famous constrained problem",d={"beta":.2},agreement=agreement),
                            marker,"逆温度", "乘子")
            self.qualifiers(self.spoken("The same algebra gives",agreement=agreement),
                            marker,"正的", "参考策略", "温度", "不同")
        circle=helpers("s16_lagrange.py","circle_solver_verdict")['circle_solver_verdict']
        self.qualifiers(self.spoken("Write it down: at the constrained",d={"lam":-.5},
                                   circle_verdict=circle(False,0.,0.)),"必要条件", "不是", "尚未通过")

    def test_kkt_inactive_zero_and_degenerate_margin_are_not_conflated(self):
        self.qualifiers(self.spoken("Most constraints are inequalities"),"约束资格", "正", "也可能为0")
        self.qualifiers(self.spoken("Two small examples",d={"nc_p":-.1,"nc_d":-.3,"nc_gap":.2}),
                        "有限网格", "不是", "连续")
        f=helpers("s17_kkt.py","svm_checks_pass","svm_solver_verdict")['svm_solver_verdict']
        d=dict(solvers={x:{"success":True} for x in ['primal','dual']},
               tolerances=dict(feasibility=1e-6,stationarity=1e-4,complementarity=1e-6),
               residuals={x:0. for x in ['primal_feasibility','dual_nonnegative','dual_equality',
                           'duality_gap','stationarity_w','stationarity_b','complementarity']})
        for passed in [True,False]:
            d['solvers']['dual']['success']=passed
            chinese=self.qualifiers(self.spoken("Duality's most famous use",X=[0]*3,sv=[0,1],tight=[0,1,2],
                                                  solver_verdict=f(d)),"截距", "加权", "0", "退化", "乘子")
            self.assertIn("都通过" if passed else "不是经过认证",chinese)

    def test_implicit_inverse_memory_censoring_and_rate_branches(self):
        self.qualifiers(self.spoken("Some layers aren't a fixed"),"逆存在", "直接", "线性求解器", "内存")
        f=helpers("s18_implicit.py","gradient_rate_comparison","fixed_point_summary","comparison_floor","loss_comparison")
        for rate,marker in [(.1,"更快"),(.9,"更慢"),(.45,"0.15"),(math.nan,"无法")]:
            self.qualifiers(f['gradient_rate_comparison'](rate,.4),marker)
        for status,marker in [("converged","满足"),("capped","上限"),("nonfinite","非有限")]:
            result=dict(status=status,iterations=3,cap=8)
            english=self.spoken("Check it on a layer with",d={"initial_state_dimension":4},
                solve_verdict=f['fixed_point_summary'](result),
                rate_statement="A finite fitted per-step gradient-gap factor is unavailable.",
                floor_verdict=f['comparison_floor']([0.,1e-8]))
            self.qualifiers(english,marker,"可逆", "条件", "不是", "认证", "0")
        for final,marker in [(.1,"低于"),(.4,"高于"),(.2,"相同"),(math.nan,"无法")]:
            self.qualifiers(f['loss_comparison'](.2,final),marker)

    def test_implicit_training_counts_do_not_promote_capped_solves(self):
        f = helpers("s18_implicit.py", "loss_comparison", "fixed_point_summary")
        training = dict(count=10, converged=7, capped=2, nonfinite=1)
        counts = assignment("s18_implicit.py", "solve_counts", {"training": training})
        for last_work in [6., 10.]:
            it = np.array([[0., 8.], [5., last_work]])
            work = assignment("s18_implicit.py", "it_v", {"it": it})
            english = self.spoken("And it trains. A deep equilibrium", d={"training_state_dimension":3,
                "parameter_count":28,"contraction_caps":{"training":.8}},
                loss_verdict=f['loss_comparison'](.2,.1),it_v=work,solve_counts=counts,
                final_solve=f['fixed_point_summary'](dict(status="capped", cap=12, iterations=12)))
            chinese = self.qualifiers(english, "候选梯度", "谱范数", "0.8", "10次训练求解", "7次收敛",
                                       "2次达到上限", "1次结果非有限", "不算", "收敛", "12次更新")
            self.assertNotIn("mean iteration", chinese)
            self.assertNotIn("the iteration", chinese)

    def test_outro_retains_conditioned_summary(self):
        self.qualifiers(self.spoken("Let's take stock"),"理想", "相对阈值", "正乘子", "加权", "条件")


if __name__ == '__main__':
    unittest.main()
