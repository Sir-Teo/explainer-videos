from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, SPOT, illustration, load, polyline, predict


class Dual(VoiceoverScene):
    def construct(self):
        a = load("american")
        dp = load("dual_path")
        br = load("bermudan_ref")
        mc = load("maxcall")
        self.card()
        self.outer(dp)
        self.proof()
        self.bounds(a, br)
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
        top = axes([0, 1], [65, 120], x_length=8.0, y_length=2.6, ylabel=r"one outer path $S_t$", xticks=[],
                   yticks=[70, 100], font_size=14).to_edge(UP, buff=0.45).to_edge(LEFT, buff=0.7)
        ta = top.ax
        bot = axes([0, 1], [-6, 30], x_length=8.0, y_length=2.9, xlabel=r"time (years)",
                   ylabel=r"discounted payoff $h_t$, martingale $\pi_t$", xticks=[0, 0.5, 1], yticks=[0, 10, 20],
                   font_size=14).next_to(top, DOWN, buff=0.35).align_to(top, LEFT)
        ba = bot.ax
        k = ValueTracker(0.0)

        def upto(arr, ax, col, lo, hi, sw=3):
            arr = np.asarray(arr)

            def make():
                j = int(np.clip(k.get_value(), 1, n))
                return VMobject(stroke_color=col, stroke_width=sw).set_points_as_corners(
                    [ax.c2p(t[i], np.clip(arr[i], lo, hi)) for i in range(j + 1)])
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
                        [ta.c2p(min(t[j] + i * dt, 1), np.clip(v, 65, 120)) for i, v in enumerate(col)]))
            return g

        fan = always_redraw(fans)
        rd = VGroup(readout(r"h_t - \pi_t =", lambda: gap[int(np.clip(k.get_value(), 0, n))], digits=2, font_size=28,
                            color=GREY_A),
                    readout(r"\max_{s \le t} =", lambda: run[int(np.clip(k.get_value(), 0, n))], digits=2, font_size=30,
                            color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.8)
        leg = legend([(SPOT, r"the outer path"), (GREY_B, r"inner paths: what is continuing worth?"),
                      (BAD, r"payoff $h_t$"), (QC.Q, r"the policy's martingale $\pi_t$")], font_size=16)
        leg.to_edge(RIGHT, buff=0.35).to_edge(UP, buff=0.6)
        src = illustration(rf"one of the outer paths, {dp['inner']} inner paths per date; the bound averages "
                           r"$\max_t (h_t - \pi_t)$ over many")
        with self.voiceover(
            "Longstaff–Schwartz gives a lower bound. How far below the truth is it? Here is how to bound it from "
            "above. Follow one outer path of the stock. <bookmark mark='a'/> At every date, launch a small fan of "
            "inner paths that follow the regression's own policy, to estimate what continuing is worth. From those "
            "estimates build a martingale, in violet: it moves only by the surprise in the policy's value, so its "
            "expected change is zero. <bookmark mark='b'/> Below, in red, the discounted payoff. Track the gap "
            "between payoff and martingale, and its running maximum. <bookmark mark='c'/> For this path the maximum "
            f"is {p['max']:.2f}. Average that maximum over many outer paths and you have an upper bound on the "
            "option's price."
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
            cmath(r"\mathbb{E}\max_t(\cdot + \epsilon_t)", r"\ge", r"\max_t\ \mathbb{E}(\cdot)", font_size=34,
                  colors={r"\ge": BAD}),
        ]
        whys = [why(r"any martingale with $M_0 = 0$: optional stopping gives $\mathbb{E}M_\tau = 0$, then the stopped value "
                    r"is at most the maximum"),
                why(r"take the best $M$ (Rogers 2002; Haugh and Kogan 2004): equality at $M^*$, the martingale part of the "
                    r"Snell envelope (Doob--Meyer; $A$ increasing)"),
                why(r"Andersen and Broadie (2004): $L$ the policy's value, its conditional expectation by inner paths"),
                why(r"noisy inner estimates inflate the bound (Jensen): it falls as the inner paths grow. The gap "
                    r"upper $-$ lower measures the policy's suboptimality")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.6, edge=6.9)
        with self.voiceover(
            "Why it is a bound. Take any martingale starting at zero. By optional stopping its expected value at any "
            "stopping time is zero, so the expected payoff equals the expected payoff minus the martingale, at most "
            "the largest gap along the path. <bookmark mark='a'/> That holds for every stopping rule, so the "
            "price is at most the infimum over martingales, and Rogers, and Haugh and Kogan, showed the infimum is "
            "attained: by the martingale part of the value process itself. <bookmark mark='b'/> Andersen and Broadie "
            "approximate it from the regression's policy, with the conditional expectation computed by inner paths. "
            "<bookmark mark='c'/> The inner noise can only push a maximum up, so the bound falls as the inner paths "
            "grow, and the distance between the two bounds is a measured error bar on the policy."
        ) as vo:
            for i, mk in enumerate("abc"):
                step(i)
                vo.wait_until(mk)
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def bounds(self, a, br):
        ab = a["ab"]
        ref = br["price"][-1]
        lo, hi = a["lsm"] - 0.06, max(r["upper"] + 2 * r["se"] for r in ab) + 0.04
        g = axes([0, len(ab) + 1], [lo, hi], x_length=7.2, y_length=4.2, ylabel=r"price of the 25-date put",
                 xticks=list(range(1, len(ab) + 1)), xfmt=lambda u: f"{ab[int(round(u)) - 1]['inner']}",
                 yticks=[round(v, 2) for v in np.linspace(lo + 0.03, hi - 0.03, 4)], font_size=15,
                 xlabel=r"inner paths per date (upper bound)")
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        lsm = DashedLine(ax.c2p(0, a["lsm"]), ax.c2p(len(ab) + 1, a["lsm"]), stroke_color=GOOD, stroke_width=2.5)
        refl = DashedLine(ax.c2p(0, ref), ax.c2p(len(ab) + 1, ref), stroke_color=WHITE, stroke_width=1.5)
        ups = VGroup(*[VGroup(Dot(ax.c2p(i, r["upper"]), radius=0.07, color=BAD),
                              Line(ax.c2p(i, r["upper"] - 2 * r["se"]), ax.c2p(i, r["upper"] + 2 * r["se"]),
                                   stroke_color=BAD, stroke_width=2)) for i, r in enumerate(ab, 1)])
        leg = legend([(GOOD, rf"Longstaff--Schwartz: {a['lsm']:.3f} (lower)"),
                      (BAD, r"Andersen--Broadie (upper), $\pm 2$ s.e."),
                      (WHITE, rf"the Bermudan's value (tree, {br['n_steps'][-1]:,} steps): {ref:.3f}".replace(",", "{,}"))],
                     font_size=16).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        last = ab[-1]
        inside = a["lsm"] <= ref <= last["upper"]
        side = VGroup(
            MathTex(rf"[{a['lsm']:.3f},\ {last['upper']:.3f}]", font_size=36, color=OPT),
            wrapped_label(rf"exercisable at any time instead of on 25 dates, the put is worth {a['tree2000']:.3f} "
                          rf"(2{{,}}000-step tree) and {a['fd']:.3f} (PDE): a different, slightly more valuable "
                          r"option", 4.0, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Here are the House's bounds on the twenty-five-date put. The lower bound from Longstaff–Schwartz is "
            f"{a['lsm']:.3f}. <bookmark mark='a'/> The upper bound with fifty inner paths is {ab[0]['upper']:.2f}, "
            f"inflated by noise; with {last['inner']:,} it is {last['upper']:.3f}. <bookmark mark='b'/> Where is "
            "the truth? A tree with five thousand steps that may exercise only on the twenty-five dates gives "
            f"{ref:.3f}: {'inside the bracket, as it must be' if inside else 'outside the bracket, which would mean a bug'}. "
            "Allowed to exercise at any moment, the option is a different one, worth a little more."
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
            "The House's outer loop is twelve lines: step the outer paths, estimate continuation by inner paths, "
            "update the martingale by the policy's surprise, and keep the running maximum of the gap. "
            "<bookmark mark='a'/> Four hundred outer paths, and the inner sample grows: the four rows you just saw."
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
        g = axes([25.8, 26.25], [0, len(items) + 1], x_length=7.4, y_length=3.8, xlabel=r"price of the five-asset max-call",
                 xticks=[25.9, 26.0, 26.1, 26.2], xfmt=lambda v: f"{v:.1f}", font_size=15)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.6)
        ax = g.ax
        bars = VGroup()
        for i, (nm, v, se, col) in enumerate(items):
            y = len(items) - i
            bars.add(VGroup(Line(ax.c2p(v - 2 * se, y), ax.c2p(v + 2 * se, y), stroke_color=col, stroke_width=4),
                            Dot(ax.c2p(v, y), radius=0.08, color=col),
                            label(nm, font_size=17, color=col).next_to(ax.c2p(25.8, y), RIGHT, buff=0.1).shift(UP * 0.22)))
        pap = Rectangle(width=ax.c2p(paper["upper"], 0)[0] - ax.c2p(paper["lower"], 0)[0] + 0.02,
                        height=ax.c2p(0, len(items) + 0.6)[1] - ax.c2p(0, 0.4)[1], stroke_width=0, fill_color=WHITE,
                        fill_opacity=0.25).move_to(ax.c2p((paper["lower"] + paper["upper"]) / 2, (len(items) + 1) / 2))
        paptx = label(rf"Becker, Cheridito, Jentzen (2019): [{paper['lower']}, {paper['upper']}]", font_size=16,
                      color=GREY_A).next_to(g, UP, buff=0.15).align_to(g, RIGHT)
        diff = dp["lower"] - L["200000"]["lower"]
        comb = np.hypot(dp["se"], L["200000"]["se"])
        verdict = (r"a statistical tie" if abs(diff) < 2 * comb else
                   (r"the network ahead" if diff > 0 else r"Longstaff--Schwartz ahead"))
        say = ("a statistical tie: the network does not beat a good classical basis, but it finds one without being "
               "told" if abs(diff) < 2 * comb else "a clear difference: the network is ahead, and it needed no "
               "hand-made basis" if diff > 0 else "a clear difference: the classical basis is ahead, though the "
               "network needed no hand-made basis")
        side = VGroup(
            wrapped_label(rf"$d = {pr['d']}$ assets, $S_0 = K = {pr['K']:.0f}$, $r = {100 * pr['r']:.0f}\%$, dividend "
                          rf"{100 * pr['div']:.0f}\%, $\sigma = {100 * pr['sigma']:.0f}\%$, $T = {pr['T']:.0f}$, {pr['N']} dates. "
                          r"A grid would need $100^5 = 10^{10}$ nodes per date", 4.6, 18, GREY_A),
            wrapped_label(r"basis (15 functions): the sorted prices, their squares, the two largest's product, the payoff "
                          r"and its square, the largest cubed", 4.6, 18, GREY_A),
            MathTex(rf"\text{{difference}}\ {diff:+.3f}\ \ (\pm {2 * comb:.3f}):\ \text{{{verdict}}}", font_size=26, color=OPT),
            wrapped_label(r"the other classical methods: random trees and the stochastic mesh (Broadie and Glasserman "
                          r"1997, 2004); Glasserman ch.\ 8", 4.6, 17, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        q = predict(r"Your lower bound is 6.06 and your upper bound 6.41. Bad policy, or too few inner paths?",
                    width=5.0, font_size=19).to_corner(DL, buff=0.2)
        src = illustration(r"each policy judged on 2{,}000{,}000 fresh paths; bars $\pm 2$ s.e.", corner=UR)
        with self.voiceover(
            "Simulation's real home is many dimensions. Broadie and Glasserman's benchmark: a Bermudan call on the "
            "largest of five stocks, nine dates over three years. A grid would need ten billion nodes per date; "
            "Longstaff–Schwartz needs fifteen basis functions. "
            "<bookmark mark='a'/> Judged on two million fresh paths, the policy fitted on two thousand paths is "
            f"worth {L['2000']['lower']:.3f}; on twenty thousand, {L['20000']['lower']:.3f}; on two hundred thousand, "
            f"{L['200000']['lower']:.3f}. <bookmark mark='b'/> Part seventeen trains a neural network to stop instead, "
            f"with no hand-made basis: it reached {dp['lower']:.3f}. On this benchmark and our budget that is "
            f"{say}. <bookmark mark='c'/> Becker, Cheridito and Jentzen's published bounds for their network "
            f"are {paper['lower']} to {paper['upper']}. Pause and predict: lower bound 6.06, "
            "upper 6.41. Rerun with more inner paths first; if the gap shrinks, it was noise, as it was here."
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
