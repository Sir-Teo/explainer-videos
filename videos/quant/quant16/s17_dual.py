from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, SPOT, illustration, load, polyline, predict, axes, data_range, pause_card, flat_camera


class Dual(VoiceoverScene):
    def construct(self):
        a = load("american")
        dp = load("dual_path")
        br = load("bermudan_ref")
        mc = load("maxcall")
        self.card()
        self.outer(dp)
        self.proof()
        self.bounds(a, br, load("lsm_live"))
        self.lab(a)
        self.maxcall(mc)

    def card(self):
        c = chapter_card(9, r"American options II: the dual bound, and five assets", r"How far below the truth is a "
                         r"lower bound?", part=PART)
        with self.voiceover("Chapter nine. American options, part two: the dual bound, and five assets."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def outer(self, dp):
        p = dp["path"]
        n = len(p["S"]) - 1
        t = np.linspace(0, 1, n + 1)
        dt = 1.0 / n
        stock_yr = data_range(p["S"], *[np.asarray(v) for v in p["fans"] if np.asarray(v).size], [100])
        payoff_yr = data_range(p["h"], p["pi"])
        top = axes([0, 1], stock_yr, x_length=8.0, y_length=2.6, ylabel=r"one outer path $S_t$", xticks=[],
                   yticks=[70, 100], font_size=14).to_edge(UP, buff=0.45).to_edge(LEFT, buff=0.7)
        ta = top.ax
        bot = axes([0, 1], payoff_yr, x_length=8.0, y_length=2.9, xlabel=r"time (years)",
                   ylabel=r"discounted payoff $h_t$, martingale $\pi_t$", xticks=[0, 0.5, 1], yticks=[0, 10, 20],
                   font_size=14).next_to(top, DOWN, buff=0.35).align_to(top, LEFT)
        ba = bot.ax
        k = ValueTracker(0.0)

        def upto(arr, ax, col, lo, hi, sw=3):
            arr = np.asarray(arr)

            def make():
                j = int(np.clip(k.get_value(), 1, n))
                return VMobject(stroke_color=col, stroke_width=sw).set_points_as_corners(
                    [ax.c2p(t[i], arr[i]) for i in range(j + 1)])
            return always_redraw(make)

        S = upto(p["S"], ta, SPOT, 65, 120)
        h = upto(p["h"], ba, BAD, -6, 30)
        pi = upto(p["pi"], ba, QC.Q, -6, 30)
        strike = DashedLine(ta.c2p(0, 100), ta.c2p(1, 100), stroke_color=GREY_C, stroke_width=1)
        gap = np.asarray(p["h"]) - np.asarray(p["pi"])
        run = np.maximum.accumulate(gap)

        def fans():
            j = int(np.clip(k.get_value(), 0, n - 1))
            f = np.asarray(p["fans"][j])
            g = VGroup()
            if f.ndim == 2 and f.shape[0] > 1:
                for col in f.T:
                    g.add(VMobject(stroke_color=GREY_B, stroke_width=1, stroke_opacity=0.6).set_points_as_corners(
                        [ta.c2p(min(t[j] + i * dt, 1), v) for i, v in enumerate(col)]))
            return g

        fan = always_redraw(fans)
        rd = VGroup(readout(r"h_t - \pi_t =", lambda: gap[int(np.clip(k.get_value(), 0, n))], digits=2, font_size=28,
                            color=GREY_A),
                    readout(r"\max_{s \le t} =", lambda: run[int(np.clip(k.get_value(), 0, n))], digits=2, font_size=30,
                            color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.8)
        leg = legend([(SPOT, r"the outer path"), (GREY_B, r"inner paths: what is continuing worth?"),
                      (BAD, r"payoff $h_t$"), (QC.Q, r"noisy policy-martingale estimate $\hat\pi_t$")], font_size=16)
        leg.to_edge(RIGHT, buff=0.35).to_edge(UP, buff=0.6)
        src = illustration(rf"selected positive-payoff path; {dp['inner']} inner paths per date; averages use "
                           r"$\max_t (h_t - \pi_t)$ over many")
        with self.voiceover(
            f"An independently evaluated fitted policy supplies a lower expectation. To study an upper expectation, follow an outer stock path. This illustration selects the first path with a positive payoff from up to forty candidates, so it is not a representative draw. <bookmark mark='a'/> Fresh inner simulations estimate the fixed policy's conditional continuation values. The ideal exact conditional values define a martingale; the plotted noisy process need not itself be a martingale in the enlarged simulation filtration. <bookmark mark='b'/> Track discounted payoff minus that noisy process and its running maximum. <bookmark mark='c'/> This selected path reaches {p['max']:.2f}. With conditionally unbiased inner estimates and the required independence, Jensen's inequality makes the average nested maximum upward biased relative to the ideal dual expectation. A finite average has Monte Carlo error and is not a sure upper bound."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(strike), FadeIn(S), FadeIn(h), FadeIn(pi), FadeIn(leg), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(fan), FadeIn(rd))
            self.play(k.animate.set_value(n * 0.45), run_time=4, rate_func=linear)
            vo.wait_until("b")
            self.play(k.animate.set_value(n * 0.8), run_time=3, rate_func=linear)
            vo.wait_until("c")
            self.play(k.animate.set_value(n), run_time=2, rate_func=linear)
        for x in (S, h, pi, fan, rd):
            x.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\mathbb{E}[h_\tau]", r"=", r"\mathbb{E}[h_\tau - M_\tau]\ \le\ \mathbb{E}\big[\max_t (h_t - M_t)\big]",
                  font_size=34, colors={r"\mathbb{E}[h_\tau]": OPT}),
            cmath(r"V_0", r"=", r"\inf_M\ \mathbb{E}\big[\max_t (h_t - M_t)\big],\qquad V = V_0 + M^* - A", font_size=34,
                  colors={r"V_0": GOOD}),
            cmath(r"\pi_{t_{i+1}}", r"=", r"\pi_{t_i} + L_{t_{i+1}} - \mathbb{E}_{t_i}\big[L_{t_{i+1}}\big]", font_size=34,
                  colors={r"\pi_{t_{i+1}}": QC.Q}),
            cmath(r"\mathbb{E}_{\rm inner}[\max_i(h_i-\hat M_i)\mid\mathrm{outer}]", r"\ge", r"\max_i(h_i-M_i)", font_size=30,
                  colors={r"\ge": BAD}),
        ]
        whys = [why(r"any martingale with $M_0 = 0$: optional stopping gives $\mathbb{E}M_\tau = 0$, then the stopped value "
                    r"is at most the maximum"),
                why(r"take the best $M$ (Rogers 2002; Haugh and Kogan 2004): equality at $M^*$, the martingale part of the "
                    r"Snell envelope (Doob--Meyer; $A$ increasing)"),
                why(r"ideal fixed-policy Doob martingale uses exact conditional values; fresh inner estimates approximate them"),
                why(r"conditionally unbiased inner noise inflates the expected maximum; finite estimates have sampling error, "
                    r"and need not decrease monotonically as inner sample size grows")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.6, edge=6.9)
        with self.voiceover(
            "On a finite exercise grid, suitable integrability and a martingale starting at zero give optional stopping. A stopped discounted payoff minus that martingale is no greater than its path maximum. <bookmark mark='a'/> Optimising over integrable martingales gives the dual value, attained by the Snell envelope's Doob martingale under the standard conditions. <bookmark mark='b'/> A fixed policy's exact conditional value process supplies an admissible martingale. Nested simulation estimates those conditional values, rather than making every noisy path an exact martingale. <bookmark mark='c'/> Conditional on the outer path, unbiased inner noise and convexity of the maximum give the displayed Jensen comparison. More inner work can reduce nested noise, but individual estimates need not fall monotonically. Both upper and lower estimates have Monte Carlo uncertainty; their observed gap also includes dual looseness and inner noise, rather than only policy suboptimality."
        ) as vo:
            for i, mk in enumerate("abc"):
                step(i)
                vo.wait_until(mk)
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def bounds(self, a, br, lv):
        ab = a["ab"]
        ref = br["price"][-1]
        lower, lower_se = lv["eval"]
        lo, hi = data_range([lower - 2 * lower_se, lower + 2 * lower_se, ref],
                            *[[r["upper"] - 2 * r["se"], r["upper"] + 2 * r["se"]] for r in ab])
        g = axes([0, len(ab) + 1], [lo, hi], x_length=7.2, y_length=4.2, ylabel=r"price of the 25-date put",
                 xticks=list(range(1, len(ab) + 1)), xfmt=lambda u: f"{ab[int(round(u)) - 1]['inner']}",
                 yticks=[round(v, 2) for v in np.linspace(lo + 0.03, hi - 0.03, 4)], font_size=15,
                 xlabel=r"inner paths per date (upper bound)")
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        lsm = DashedLine(ax.c2p(0, lower), ax.c2p(len(ab) + 1, lower), stroke_color=GOOD, stroke_width=2.5)
        refl = DashedLine(ax.c2p(0, ref), ax.c2p(len(ab) + 1, ref), stroke_color=WHITE, stroke_width=1.5)
        ups = VGroup(*[VGroup(Dot(ax.c2p(i, r["upper"]), radius=0.07, color=BAD),
                              Line(ax.c2p(i, r["upper"] - 2 * r["se"]), ax.c2p(i, r["upper"] + 2 * r["se"]),
                                   stroke_color=BAD, stroke_width=2)) for i, r in enumerate(ab, 1)])
        leg = legend([(GOOD, rf"fresh policy estimate: {lower:.3f} $\pm$ {lower_se:.3f} (one s.e.)"),
                      (BAD, r"nested upper-expectation estimate, $\pm 2$ s.e."),
                      (WHITE, rf"the Bermudan's value (tree, {br['n_steps'][-1]:,} steps): {ref:.3f}".replace(",", "{,}"))],
                     font_size=16).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        last = ab[-1]
        inside = lower <= ref <= last["upper"]
        side = VGroup(
            MathTex(rf"[{lower:.3f},\ {last['upper']:.3f}]", font_size=36, color=OPT),
            wrapped_label(rf"exercisable at any time instead of on 25 dates, the put is worth {a['tree2000']:.3f} "
                          rf"(2{{,}}000-step tree) and {a['fd']:.3f} (PDE): a different, slightly more valuable "
                          r"option", 4.0, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"Here the green line is the fixed fitted policy evaluated on four hundred thousand fresh paths: {lower:.3f}, with estimated standard error {lower_se:.3f}. It replaces the in-sample mean, which is not a lower-bound estimate. <bookmark mark='a'/> The nested upper-expectation estimate is {ab[0]['upper']:.2f} with fifty inner paths and {last['upper']:.3f} with {last['inner']:,}. Red bars show two estimated outer standard errors; they do not remove nested bias. <bookmark mark='b'/> A five-thousand-step tree on the same twenty-five exercise dates gives {ref:.3f}. Sampling noise and finite tree error mean that this number is not required to lie between every pair of point estimates. The separate continuous-exercise tree and PDE approximate a different, more flexible contract."
        ) as vo:
            self.play(FadeIn(g), Create(lsm), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(u) for u in ups], lag_ratio=0.3, run_time=2.5), FadeIn(leg[1]))
            vo.wait_until("b")
            self.play(Create(refl), FadeIn(leg[2]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, a):
        card = lab_card(r"the dual bound's outer loop", [
            "S = np.full(n_outer, float(S0))",
            "C = continuation(0, S)            # inner paths",
            "pi = np.zeros(n_outer)",
            "best = np.maximum(K - S, 0) - pi",
            "for i in range(1, n_steps + 1):",
            "    S = S * np.exp((r - sigma**2/2)*dt + sigma*np.sqrt(dt)*g.standard_normal(n_outer))",
            "    h = np.maximum(K - S, 0)",
            "    C_new = continuation(i, S)",
            "    L = np.where(exercise(i, S), h, C_new)",
            "    pi = pi + np.exp(-r*i*dt)*L - np.exp(-r*(i-1)*dt)*C",
            "    best = np.maximum(best, np.exp(-r*i*dt)*h - pi)",
            "    C = C_new",
        ], source="explainer/quant/house/engine.py  andersen_broadie_put", width=8.6).to_corner(UL, buff=0.35)
        out = ["inner   upper    s.e."] + [f"{r['inner']:>5}   {r['upper']:.3f}   {r['se']:.3f}" for r in a["ab"]]
        with self.voiceover(
            "This outer loop advances stock paths, estimates continuation with fresh inner draws, updates the noisy policy-martingale approximation, and records the maximum adjusted payoff. <bookmark mark='a'/> The saved experiment uses four hundred outer paths at each inner budget. The standard errors describe outer dispersion; the inner approximation contributes additional upward bias in expectation under the stated construction."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, out)
        self.wait(0.5)
        self.clear_scene()

    def maxcall(self, mc):
        pr = mc["params"]
        L = mc["lsm"]
        paper = mc["paper"]
        dp = mc["deep"]
        items = [(r"LSM, 2{,}000 fitting paths", L["2000"]["lower"], L["2000"]["se"], GREY_B),
                 (r"LSM, 20{,}000", L["20000"]["lower"], L["20000"]["se"], QC.THETA),
                 (r"LSM, 200{,}000", L["200000"]["lower"], L["200000"]["se"], GOOD),
                 (r"deep stopping (Part 17)", dp["lower"], dp["se"], QC.Q)]
        xr = data_range(*[[v - 2 * se, v + 2 * se] for _, v, se, _ in items], [paper["lower"], paper["upper"]])
        g = axes(xr, [0, len(items) + 1], x_length=7.4, y_length=3.8, xlabel=r"price of the five-asset max-call",
                 xticks=[25.9, 26.0, 26.1, 26.2], xfmt=lambda v: f"{v:.1f}", font_size=15)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.6)
        ax = g.ax
        bars = VGroup()
        for i, (nm, v, se, col) in enumerate(items):
            y = len(items) - i
            bars.add(VGroup(Line(ax.c2p(v - 2 * se, y), ax.c2p(v + 2 * se, y), stroke_color=col, stroke_width=4),
                            Dot(ax.c2p(v, y), radius=0.08, color=col),
                            label(nm, font_size=17, color=col).next_to(ax.c2p(xr[0], y), RIGHT, buff=0.1).shift(UP * 0.22)))
        pap = Rectangle(width=ax.c2p(paper["upper"], 0)[0] - ax.c2p(paper["lower"], 0)[0] + 0.02,
                        height=ax.c2p(0, len(items) + 0.6)[1] - ax.c2p(0, 0.4)[1], stroke_width=0, fill_color=WHITE,
                        fill_opacity=0.25).move_to(ax.c2p((paper["lower"] + paper["upper"]) / 2, (len(items) + 1) / 2))
        paptx = label(rf"Becker, Cheridito, Jentzen (2019): [{paper['lower']}, {paper['upper']}]", font_size=16,
                      color=GREY_A).next_to(g, UP, buff=0.15).align_to(g, RIGHT)
        diff = dp["lower"] - L["200000"]["lower"]
        comb = np.hypot(dp["se"], L["200000"]["se"])
        verdict = (r"difference unresolved at two s.e." if abs(diff) < 2 * comb else
                   (r"the network ahead" if diff > 0 else r"Longstaff--Schwartz ahead"))
        say = ("a statistical tie: the network does not beat a good classical basis, but it finds one without being "
               "told" if abs(diff) < 2 * comb else "a clear difference: the network is ahead, and it needed no "
               "hand-made basis" if diff > 0 else "a clear difference: the classical basis is ahead, though the "
               "network needed no hand-made basis")
        side = VGroup(
            wrapped_label(rf"$d = {pr['d']}$ assets, $S_0 = K = {pr['K']:.0f}$, $r = {100 * pr['r']:.0f}\%$, dividend "
                          rf"{100 * pr['div']:.0f}\%, $\sigma = {100 * pr['sigma']:.0f}\%$, $T = {pr['T']:.0f}$, {pr['N']} dates. "
                          r"An illustrative 100-point-per-axis tensor grid has $100^5=10^{10}$ nodes per date", 4.6, 18, GREY_A),
            wrapped_label(r"basis (15 functions): the sorted prices, their squares, the two largest's product, the payoff "
                          r"and its square, the largest cubed", 4.6, 18, GREY_A),
            VGroup(
                MathTex(rf"\text{{difference}}\ {diff:+.3f}\ \ (\pm {2 * comb:.3f})", font_size=26, color=OPT),
                wrapped_label(verdict, 4.6, 21, OPT),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            wrapped_label(r"the other classical methods: random trees and the stochastic mesh (Broadie and Glasserman "
                          r"1997, 2004); Glasserman ch.\ 8", 4.6, 17, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        q = predict(r"Your lower bound is 6.06 and your upper bound 6.41. Bad policy, or too few inner paths?",
                    width=5.0, font_size=19).to_corner(DR, buff=0.25)  # the lower left holds the axis label
        src = illustration(r"LSM: 2 million evaluation paths; network: 1 million; bars $\pm 2$ evaluation s.e.", corner=UR)
        with self.voiceover(
            f"This Bermudan call pays on the largest of five stocks at nine possible dates. A tensor grid with one hundred nodes per asset would have ten billion nodes per date; that is an illustrative grid choice, not a universal requirement. <bookmark mark='a'/> LSM uses fifteen engineered basis functions. On two million evaluation paths, the policies fitted with two thousand, twenty thousand and two hundred thousand paths give {L['2000']['lower']:.3f}, {L['20000']['lower']:.3f} and {L['200000']['lower']:.3f}. <bookmark mark='b'/> Part seventeen's network policy is evaluated on one million paths and gives {dp['lower']:.3f}. It avoids choosing a polynomial basis, but still uses engineered features, architecture and training choices. The difference is {diff:+.3f}, with two combined evaluation standard errors {2 * comb:.3f}; this comparison excludes training uncertainty and does not prove equivalence. <bookmark mark='c'/> Becker, Cheridito and Jentzen report {paper['lower']} to {paper['upper']} with a different implementation and budget. A wide observed lower-to-upper gap may reflect policy loss, dual looseness or inner noise. Increasing inner work is a useful diagnostic, while retaining outer uncertainty. Next, Greeks."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[1]), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[:3]], lag_ratio=0.4, run_time=2.5))
            vo.wait_until("b")
            self.play(FadeIn(bars[3]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(pap), FadeIn(paptx), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
