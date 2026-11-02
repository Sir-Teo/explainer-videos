from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, METHOD_COL, OPT, PART, SPOT, illustration, load, polyline, predict


class MLMC(VoiceoverScene):
    def construct(self):
        m = load("mlmc")
        tr = load("mlmc_trace")
        mi = load("mlmc_milstein")
        mc = load("mlmc_call")
        self.card()
        self.telescope(mi, m)
        self.theorem()
        self.replay(tr)
        self.lab(m)
        self.cost(m, mi, mc)

    def card(self):
        c = chapter_card(7, r"Multilevel Monte Carlo", r"Why simulate every path at the finest step?", lit=(2008,), part=PART)
        with self.voiceover("Chapter seven. Multilevel Monte Carlo."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def telescope(self, mi, m):
        panels = VGroup()
        for l, pr in enumerate(mi["pairs"], 1):
            f, c = np.asarray(pr["fine"]), np.asarray(pr["coarse"])
            g = axes([0, 1], [70, 140], x_length=2.8, y_length=2.2, xticks=[], yticks=[], font_size=12)
            ax = g.ax
            tf = np.linspace(0, 1, len(f))
            tc = np.linspace(0, 1, len(c))
            fl = polyline(ax, tf, np.clip(f, 70, 140), QC.DELTA, stroke_width=2.5, radius=0.035)
            cl = polyline(ax, tc, np.clip(c, 70, 140), GREY_B, stroke_width=2, radius=0.035)
            gap = Line(ax.c2p(1, c[-1]), ax.c2p(1, f[-1]), stroke_color=BAD, stroke_width=7)
            t = label(rf"level {l}: {2 ** l} steps against {2 ** (l - 1)}", font_size=16, color=GREY_A).next_to(g, UP, buff=0.08)
            d = MathTex(rf"P_{l} - P_{l - 1}:\ {f[-1] - c[-1]:+.2f}", font_size=22, color=BAD).next_to(g, DOWN, buff=0.08)
            panels.add(VGroup(g, cl, fl, gap, t, d))
        panels.arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.6)
        top = m["mlmc"][-1]
        N, V = np.asarray(top["N"], float), np.asarray(top["V"], float)
        C = np.array([2.0 ** l + (2.0 ** (l - 1) if l else 0) for l in range(len(N))])
        bars = VGroup()
        wmax = np.log10(N.max())
        for l in range(len(N)):
            w = 5.2 * np.log10(N[l]) / wmax
            h = 0.12 + 0.17 * np.log2(C[l]) / np.log2(C[-1]) * 1.8
            bars.add(VGroup(Rectangle(width=w, height=h, stroke_width=1, stroke_color=GREY_B, fill_color=QC.DELTA,
                                      fill_opacity=0.25 + 0.6 * l / len(N)),
                            MathTex(rf"N_{{{l}}} = {int(N[l]):,}".replace(",", "{,}"), font_size=18, color=GREY_A)))
        for b in bars:
            b[1].next_to(b[0], RIGHT, buff=0.15)
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.04).to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=1.2)
        cap = wrapped_label(r"one bar per level: width $\propto \log N_l$ (paths), height grows with the steps per path; "
                            r"millions of cheap coarse paths, a few thousand fine ones", 4.8, 18, GREY_A)
        cap.next_to(bars, RIGHT, buff=0.9).shift(UP * 0.3)
        with self.voiceover(
            "A simulation with time steps has two errors: noise, which falls with more paths, and bias, which falls "
            "with finer steps. Mike Giles's idea in 2008 was to stop simulating every path at the finest step. "
            "Here is one path simulated twice, with fine steps in gold and steps twice as long in grey, from the "
            "same random numbers. <bookmark mark='a'/> At level one the two disagree by dollars. At "
            "level four, by cents. The difference between neighbouring levels is small, and so is its variance. "
            "<bookmark mark='b'/> So estimate the fine price as the coarse price plus a ladder of corrections, each "
            "with its own number of paths. At a target accuracy of one cent, millions of paths go to the cheap "
            "coarse level and only thousands to the expensive fine ones."
        ) as vo:
            self.play(FadeIn(panels[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in panels[1:]], lag_ratio=0.4, run_time=2.5))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.1, run_time=2.5), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def theorem(self):
        rows = [
            cmath(r"\mathbb{E}[P_L]", r"=", r"\mathbb{E}[P_0] + \sum_{l=1}^{L}\mathbb{E}\big[P_l - P_{l-1}\big]", font_size=34,
                  colors={r"\mathbb{E}[P_L]": OPT}),
            cmath(r"\text{MSE}", r"=", r"\sum_l \frac{V_l}{N_l} + \big(\mathbb{E}P_L - \mathbb{E}P\big)^2", font_size=34),
            cmath(r"N_l", r"=", r"2\varepsilon^{-2}\sqrt{V_l/C_l}\,\sum_k\sqrt{V_k C_k},\qquad \text{cost} = "
                  r"2\varepsilon^{-2}\Big(\sum_l\sqrt{V_l C_l}\Big)^2", font_size=30, colors={r"N_l": GOOD}),
            cmath(r"V_l \le c\,M^{-\beta l},\ C_l \le c\,M^{\gamma l}", r"\Rightarrow",
                  r"\text{cost} = \begin{cases}O(\varepsilon^{-2}) & \beta > \gamma\\ O(\varepsilon^{-2}(\log\varepsilon)^2) & "
                  r"\beta = \gamma\\ O(\varepsilon^{-2-(\gamma-\beta)/\alpha}) & \beta < \gamma\end{cases}", font_size=28),
            cmath(r"\text{Euler: }\beta = 1 = \gamma", r"\quad", r"\text{Milstein: }\beta = 2 > \gamma\quad\ "
                  r"\text{standard MC: }\varepsilon^{-3}", font_size=30),
        ]
        whys = [why(r"telescoping: unbiased for the finest level if each correction is estimated without bias"),
                why(r"independent levels: variances add; then the bias of the finest step. Give each half of $\varepsilon^2$"),
                why(r"minimise $\sum N_l C_l$ subject to $\sum V_l/N_l = \varepsilon^2/2$ with a Lagrange multiplier"),
                why(r"Giles's theorem (bias $\le c\,M^{-\alpha l}$): $\sum_l M^{(\gamma - \beta)l/2}$ is a geometric series "
                    r"that converges, grows like $L \sim \log\varepsilon^{-1}$, or is dominated by its last term"),
                why(r"$V_l$ is the strong error squared: Euler's strong order $\frac12$ gives $\beta = 1$, Milstein's "
                    r"order 1 gives $\beta = 2$")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-1.0, buff=0.55, edge=6.9)
        with self.voiceover(
            "The proof fits on one screen. The fine-level expectation telescopes into the coarse one plus corrections. "
            "<bookmark mark='a'/> With independent levels, the mean squared error is the sum of each level's variance "
            "over its paths, plus the bias squared; give each half the budget. <bookmark mark='b'/> Minimise the "
            "total cost subject to that budget with a Lagrange multiplier: each level gets paths in proportion to the "
            "root of its variance over its cost. <bookmark mark='c'/> Now assume the corrections' variance falls like M to the minus "
            "beta l while the cost grows like M to the gamma l. The sum is a geometric series. If beta beats gamma it "
            "converges, and the cost is epsilon to the minus two: as cheap as if every path were exact. If they tie, "
            "the cost picks up a log squared. <bookmark mark='d'/> Euler's scheme ties, with beta equal to one; "
            "Milstein's scheme, accurate to first order path by path, has beta two and wins. Plain Monte Carlo pays "
            "epsilon to the minus three."
        ) as vo:
            for i, mk in enumerate("abcd"):
                step(i)
                vo.wait_until(mk)
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def replay(self, tr):
        runs = tr["runs"]
        log = runs[0]["trace"]
        Lmax = max(p["L"] for p in log)
        g = axes([-0.5, Lmax + 0.5], [-3, 2.5], x_length=6.2, y_length=3.6, xlabel=r"level $l$",
                 ylabel=r"$\log_{10} V_l$", xticks=list(range(0, Lmax + 1, 2)), yticks=[-2, 0, 2], font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(UP * 0.4)
        ax = g.ax
        h = axes([-0.5, Lmax + 0.5], [0, 7.5], x_length=6.2, y_length=2.0, xlabel=r"level $l$",
                 ylabel=r"$\log_{10} N_l$", xticks=[], yticks=[0, 3, 6], font_size=15).next_to(g, DOWN, buff=0.35)
        hx = h.ax

        def frame(k):
            p = log[k]
            V, N = np.asarray(p["V"]), np.asarray(p["N"])
            dots = VGroup(*[Dot(ax.c2p(l, np.log10(v)), radius=0.07, color=OPT) for l, v in enumerate(V)])
            bars = VGroup(*[Rectangle(width=0.35, height=max(hx.c2p(0, np.log10(n))[1] - hx.c2p(0, 0)[1], 0.01),
                                      stroke_width=0, fill_color=QC.DELTA, fill_opacity=0.8)
                            .move_to(hx.c2p(l, 0), aligned_edge=DOWN) for l, n in enumerate(N)])
            txt = VGroup(MathTex(rf"\text{{pass}}\ {k + 1}:\ L = {p['L']}", font_size=30, color=WHITE),
                         MathTex(rf"\text{{bias estimate}}\ {p['bias']:.4f}\ \ \text{{vs}}\ \ \varepsilon/\sqrt2 = "
                                 rf"{tr['eps'] / np.sqrt(2):.4f}", font_size=26,
                                 color=GOOD if p["bias"] < tr["eps"] / np.sqrt(2) else BAD),
                         MathTex(rf"\text{{cost so far: }}{p['cost'] / 1e6:.1f}\ \text{{million steps}}", font_size=26,
                                 color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            txt.to_edge(RIGHT, buff=0.5).shift(UP * 1.2)
            return VGroup(dots, bars, txt)

        cur = frame(0)
        costs = [r["cost"] for r in runs]
        seeds = MathTex(rf"\text{{four seeds: final cost }}{min(costs) / 1e6:.1f}\text{{--}}{max(costs) / 1e6:.1f}"
                        rf"\ \text{{million steps, }}L = {min(r['levels'] for r in runs)}\text{{--}}{max(r['levels'] for r in runs)}",
                        font_size=26, color=GOOD).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.2)
        src = illustration(r"the House's adaptive loop at $\varepsilon = 0.01$ (continuously averaged Asian, Euler), pass by pass")
        with self.voiceover(
            "Now watch the House's estimator choose its own levels, at an accuracy of one cent. Three levels of pilot "
            "paths first; it measures each correction's variance, the dots, and allocates paths by the formula, the "
            "bars. <bookmark mark='a'/> Then it tests the bias using the "
            "last correction's mean. Too big: add a level, re-estimate, re-allocate. Pass by pass the dots step down "
            "a straight line. <bookmark mark='b'/> It stops when "
            f"the bias test passes, here at {runs[0]['levels']} levels. Across four seeds the final cost varies by "
            f"{100 * (max(costs) - min(costs)) / min(costs):.1f} percent: the algorithm is stable."
        ) as vo:
            self.play(FadeIn(g), FadeIn(h), FadeIn(src), FadeIn(cur))
            vo.wait_until("a")
            for k in range(1, len(log)):
                self.play(Transform(cur, frame(k)), run_time=1.0)
                self.wait(0.4)
            vo.wait_until("b")
            self.play(FadeIn(seeds))
        self.wait(0.5)
        self.clear_scene()

    def lab(self, m):
        V = m["mlmc"][-1]["V"]
        card = lab_card(r"one level of the multilevel estimator", [
            "nf = M ** l; hf = T / nf",
            "dW = np.sqrt(hf) * g.standard_normal((n, nf))",
            "for i in range(nf):                       # fine path",
            "    Sf = Sf + r*Sf*hf + sigma*Sf*dW[:, i]; sf += Sf",
            "Pf = np.exp(-r*T) * np.maximum(sf / nf - K, 0)",
            "nc = nf // M; hc = T / nc",
            "dWc = dW.reshape(n, nc, M).sum(axis=2)    # same noise",
            "for i in range(nc):                       # coarse path",
            "    Sc = Sc + r*Sc*hc + sigma*Sc*dWc[:, i]; sc += Sc",
            "Pc = np.exp(-r*T) * np.maximum(sc / nc - K, 0)",
            "return Pf - Pc",
        ], source="explainer/quant/house/engine.py  _mlmc_level", width=7.6).to_corner(UL, buff=0.35)
        out = ["V_l by level (eps = 0.01):"]
        for a in range(0, len(V), 4):
            out.append("  ".join(f"V{l}={V[l]:.3g}" for l in range(a, min(a + 4, len(V)))))
        with self.voiceover(
            "The whole trick is one line of the House's code. The coarse path's increments are the fine path's, "
            "summed in pairs: the same noise, so the two paths stay close. <bookmark mark='a'/> Run it, and the "
            f"variance of the corrections falls from {V[0]:.0f} at level zero to {V[-1]:.4f} at level {len(V) - 1}."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, out)
        self.wait(0.5)
        self.clear_scene()

    def cost(self, m, mi, mc):
        eps = np.asarray(m["eps"])
        cm = np.array([r["cost"] for r in m["mlmc"]])
        cs = np.array([r["cost"] for r in m["standard"]])
        g = axes([np.log10(0.008), np.log10(0.05)], [6.3, 9.6], x_length=5.0, y_length=3.6,
                 xlabel=r"target accuracy $\varepsilon$", ylabel=r"cost (steps simulated)",
                 xticks=list(np.log10(eps)), xfmt=lambda u: f"{10 ** u:.2f}", yticks=[7, 8, 9],
                 yfmt=lambda u: f"10^{{{int(round(u))}}}", font_size=14, log_x=True)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        ls = polyline(ax, np.log10(eps), np.clip(np.log10(cs), 6.3, 9.6), BAD)
        lm = polyline(ax, np.log10(eps), np.log10(cm), GOOD)
        leg = legend([(BAD, r"standard MC at the finest step"), (GOOD, r"multilevel")], font_size=15)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        lv = mi["levels"]
        g2 = axes([0.5, 8.5], [-5.5, 1], x_length=4.6, y_length=3.0, xlabel=r"level $l$", ylabel=r"$\log_{10} V_l$",
                   xticks=[2, 4, 6, 8], yticks=[-4, -2, 0], font_size=14).to_edge(RIGHT, buff=0.5).shift(UP * 1.2)
        ax2 = g2.ax
        le = polyline(ax2, np.arange(1, 9), np.log10(lv["euler"]), METHOD_COL["euler"])
        lmi = polyline(ax2, np.arange(1, 9), np.log10(lv["milstein"]), METHOD_COL["milstein"])
        leg2 = legend([(METHOD_COL["euler"], rf"Euler: $\beta \approx {mi['beta']['euler']:.2f}$"),
                       (METHOD_COL["milstein"], rf"Milstein: $\beta \approx {mi['beta']['milstein']:.2f}$")],
                      font_size=15).next_to(g2, DOWN, buff=0.15).align_to(g2, LEFT)
        e2 = [e * e * r["cost"] for e, r in zip(mc["eps"], mc["euler"])]
        m2 = [e * e * r["cost"] for e, r in zip(mc["eps"], mc["milstein"])]
        tab = VGroup(MathTex(r"\varepsilon^2 \cdot \text{cost, European call}", font_size=22, color=GREY_A))
        for e, a, b in zip(mc["eps"], e2, m2):
            tab.add(MathTex(rf"\varepsilon = {e}:\ \ \text{{Euler}}\ {a:,.0f}\ \ \text{{Milstein}}\ {b:,.0f}"
                            .replace(",", "{,}"), font_size=22))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(leg2, DOWN, buff=0.25).align_to(g2, LEFT)
        last = len(eps) - 1
        mil_a = [r["cost"] for r in mi["milstein"]]
        q = predict(r"Milstein's $V_l$ falls four times per level, not two. What happens to $\varepsilon^2\cdot$cost "
                    r"as $\varepsilon \to 0$?", width=5.2, font_size=19).to_corner(DL, buff=0.25)
        with self.voiceover(
            "The payoff, on the Asian: the cost of each accuracy, standard against multilevel. At one cent, "
            f"multilevel is {cs[last] / cm[last]:.0f} times cheaper. "
            "<bookmark mark='a'/> On the right, a European call, the theorem's textbook case: the corrections' "
            f"variance falls with slope {mi['beta']['euler']:.2f} under Euler and {mi['beta']['milstein']:.2f} under "
            "Milstein, as the theory says. <bookmark mark='b'/> Pause and predict. With beta two, what happens to "
            "epsilon squared times the cost? <bookmark mark='c'/> The theorem says it stops growing. Measured on the "
            f"call, as epsilon falls eightfold, Euler's goes from {e2[0]:,.0f} to {e2[-1]:,.0f}, and Milstein's from "
            f"{m2[0]:,.0f} to {m2[-1]:,.0f}. On the Asian, the average already smooths Euler's path errors, and Milstein's run at a "
            f"half cent cost {mil_a[-1] / mi['euler_0.005']['cost']:.2f} times Euler's. One more card: Chang-han Rhee "
            "and Peter Glynn showed in 2015 that picking the level at random, and weighting by its probability, "
            "removes the bias entirely when beta beats gamma."
        ) as vo:
            self.play(FadeIn(g), Create(ls), Create(lm), FadeIn(leg))
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(le), Create(lmi), FadeIn(leg2))
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(FadeIn(tab))
        self.wait(0.5)
        self.clear_scene()
