from __future__ import annotations

import numpy as np

from videos.quant.quant14.common import axes, data_range, skew_range

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, SPOT, VAR, illustration, load, pause, real_data


class Joint(VoiceoverScene):
    def construct(self):
        q = load("qrh_sim")
        jb = load("joint_bounds")
        self.card()
        self.puzzle()
        self.qrh(q)
        self.zumbach(q)
        self.derive()
        self.dmsp(jb)

    def card(self):
        c = chapter_card(15, r"Joint SPX/VIX: quadratic rough Heston and Guyon's puzzle",
                         r"Can one model fit the S\&P 500 and the VIX at once?", lit=(2020,), part=PART)
        with self.voiceover("Chapter fifteen. Joint S&P and VIX: quadratic rough Heston, and Guyon's puzzle."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def puzzle(self):
        left = VGroup(label(r"S\&P 500 options", font_size=28, color=SPOT),
                      wrapped_label(r"a steep, exploding short-dated skew: the model needs a large vol of vol", 5.0, 21, GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        right = VGroup(label(r"VIX futures and options", font_size=28, color=IV),
                       wrapped_label(r"with that vol of vol, the model's VIX implied volatilities come out too high "
                                     r"against the market's", 5.0, 21, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        grid = VGroup(left, right).arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to(UP * 1.2)
        arrow = Arrow(left.get_bottom() + DOWN * 0.1, right.get_bottom() + DOWN * 0.1, path_arc=0.8, color=BAD)
        cite = wrapped_label('A model-dependent SPX/VIX calibration tension. Part 13 used a Bitcoin volatility-index illustration, without a joint SPX/VIX market calibration.', 11.0, 20, WHITE).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            """Joint SPX and VIX calibration asks one risk-neutral model to fit both markets. Some continuous one-factor models that steepen the SPX short smile then produce too much VIX-option volatility. That is a model-dependent tension, not a theorem about every continuous model. <bookmark mark='a'/> Part thirteen illustrated a related mechanism on Bitcoin; it did not calibrate SPX and VIX jointly. <bookmark mark='b'/> Here we introduce quadratic rough Heston and Guyon's constrained-entropy construction, then run a simpler two-marginal numerical transport illustration."""
        ) as vo:
            self.play(FadeIn(left))
            vo.wait_until("a")
            self.play(FadeIn(right), Create(arrow))
            vo.wait_until("b")
            self.play(FadeIn(cite))
        self.wait(0.4)
        self.clear_scene()

    def qrh(self, q):
        pr = q["params"]
        t = np.asarray(q["t"])
        S, V, Z = (np.asarray(q["paths"][k], float) for k in ("S", "V", "Z"))
        i = 0
        g1 = axes([0, 1], [S[i].min() * 0.95, S[i].max() * 1.05], x_length=6.6, y_length=2.4, ylabel=r"price",
                  xticks=[], yticks=[], font_size=14)
        g2 = axes([0, 1], [0, max(0.25, float(np.sqrt(V[i]).max()) * 1.1)], x_length=6.6, y_length=2.4, xlabel=r"years",
                  ylabel=r"volatility $\sqrt{V_t}$", xticks=[0, 0.5, 1], yticks=[0, 0.1, 0.2],
                  yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=14)
        VGroup(g1, g2).arrange(DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        zr = data_range(Z[i], [pr["b"]])
        zs = np.linspace(*zr, 100)
        vr = data_range(V[i], pr["a"] * (zs-pr["b"])**2 + pr["c"], zero=True)
        par = axes(list(zr), list(vr), x_length=4.4, y_length=3.4, xlabel=r"$Z_t$", ylabel=r"$V = a(Z - b)^2 + c$",
                   xticks=[-0.2, 0, pr["b"], 0.3], yticks=[0, 0.03, 0.06], font_size=14).to_edge(RIGHT, buff=0.5)
        pc = curve(par.ax, zs, pr["a"] * (zs - pr["b"]) ** 2 + pr["c"], VAR, stroke_width=3)
        tr = ValueTracker(0)
        ls = tracing(g1.ax, t, S[i], tr, WHITE, stroke_width=2)
        lv = tracing(g2.ax, t, np.sqrt(V[i]), tr, ROUGH, stroke_width=2)
        dot = always_redraw(lambda: Dot(par.ax.c2p(np.interp(tr.get_value(), np.arange(len(t)), Z[i]),
                                                   np.interp(tr.get_value(), np.arange(len(t)), V[i])),
                                        radius=0.09, color=YELLOW))
        q_ = pause(r"In quadratic rough Heston, does a sharp rally raise or lower volatility?", width=4.6,
                   font_size=20).next_to(par, UP, buff=0.3)
        src = illustration(rf"Gatheral, Jusselin and Rosenbaum's calibrated values (19 May 2017): $\alpha = {pr['alpha']}$, "
                           rf"$\lambda = {pr['lambda']}$, $a = {pr['a']}$, $b = {pr['b']}$, $c = {pr['c']}$, $Z_0 = {pr['Z0']}$; "
                           r"$\eta = 1$ our choice; lifted, 10 factors")
        with self.voiceover(
            "In 2020 Jim Gatheral, Paul Jusselin and Mathieu Rosenbaum proposed the quadratic rough Heston model. "
            "Z is a rough weighted average of past returns, driven by the same Brownian motion as the price. The "
            "variance is a parabola in Z: a times Z minus b squared, plus c. <bookmark mark='a'/> Pause and "
            "predict: a sharp rally. Does volatility rise or fall? <bookmark mark='b'/> Watch the yellow dot ride "
            "the parabola as the path unfolds. A fall drives Z down and volatility up the left arm. A big enough "
            "rally drives Z past b and volatility up the right arm. That convexity makes vol of vol depend on the "
            "state, and lets the VIX smile slope upward. With these six numbers they fitted S&P and VIX smiles "
            "together on the nineteenth of May 2017."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(par), Create(pc), FadeIn(ls), FadeIn(lv), FadeIn(dot), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(q_, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(tr.animate.set_value(len(t) - 1), run_time=max(vo.remaining(0.0) - 0.5, 8), rate_func=linear)
        for m in (ls, lv, dot):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def zumbach(self, q):
        z = q["zumbach"]
        names = [("qRH", r"quadratic rough Heston", ROUGH), ("rBergomi", r"rough Bergomi (no feedback)", MODEL_COL["rBergomi"]),
                 ("market", r"US market, 1990--2025", IV)]
        g = axes([-0.5, 2.5], [0, 0.65], x_length=7.4, y_length=4.0, xticks=[0, 1, 2],
                 xfmt=lambda u: ["qRH", "rBergomi", "market"][int(round(u))], ylabel=r"correlation",
                 yticks=[0, 0.2, 0.4, 0.6], font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        bars = VGroup()
        for i, (k, _, c) in enumerate(names):
            f, b = z[k]
            for j, (v, op) in enumerate(((f, 0.95), (b, 0.4))):
                bars.add(Rectangle(width=0.5, height=max(g.ax.c2p(0, v)[1] - g.ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                   fill_color=c, fill_opacity=op).move_to(g.ax.c2p(i - 0.15 + 0.3 * j, v / 2)))
        leg = VGroup(label(r"solid: past squared trend $\to$ future realized variance", font_size=17),
                     label(r"faded: past realized variance $\to$ future squared trend", font_size=17, color=GREY_A)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(g, UP, buff=0.15).align_to(g, LEFT)
        signs = {k: z[k][0] - z[k][1] for k in z}
        side = wrapped_label(r"the weak Zumbach effect: financial time series are not time-reversal invariant; past squared "
                             r"returns forecast future volatility better than the reverse (Zumbach 2009; Gatheral, Jusselin "
                             r"and Rosenbaum 2020)", 4.6, 18, GREY_A).to_edge(RIGHT, buff=0.4)
        holds = signs["qRH"] > 0 and signs["market"] > 0
        verdict = ("the asymmetry is there in both the model and the market" if holds else
                   "the asymmetry does not show in both the model and the market")
        src = real_data(r"20-day windows; 10{,}000 simulated paths per model; Ken French daily market", corner=DR)
        with self.voiceover(
            f"That feedback has a signature in the time series, the Zumbach effect: markets are not time-reversible. A big move over the past month predicts high realized volatility over the next one better than high past volatility predicts a big move. <bookmark mark='a'/> Measure it, with twenty-day windows. In the quadratic rough Heston paths the forward correlation is {z['qRH'][0]:.2f}, the backward {z['qRH'][1]:.2f}. In the US market since 1990, {z['market'][0]:.2f} against {z['market'][1]:.2f}: {verdict}. <bookmark mark='b'/> Rough Bergomi, with no feedback from price to volatility, is close to symmetric: {z['rBergomi'][0]:.2f} against {z['rBergomi'][1]:.2f}. The simulated correlations use risk-neutral illustrative dynamics; the historical correlations use physical market data and overlapping windows. This qualitative comparison is not a statistical test. Weak Zumbach asymmetry can also occur in leverage models without explicit return feedback."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(side), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[:2]], lag_ratio=0.3),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[4:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[2:4]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"Z_t", r"=", r"Z_0 - \int_0^t \frac{\lambda(t - s)^{\alpha - 1}}{\Gamma(\alpha)}\big(Z_s\,ds - \eta\sqrt{V_s}"
                      r"\,dW_s\big),\quad V_t = a(Z_t - b)^2 + c", font_size=30, colors={r"Z_t": ROUGH}),
                cmath(r"\mathrm{VIX}^2_T", r"=", r"\mathbb{E}_T\Big[\frac{1}{\tau}\int_T^{T + \tau}V_s\,ds\Big] = "
                      r"\mathbb{E}_T\Big[-\frac{2}{\tau}\log\frac{S_{T + \tau}}{S_T}\Big]", font_size=34,
                      colors={r"\mathrm{VIX}^2_T": IV}),
                cmath(r"\mathbb{E}\,\mathrm{VIX}_T", r"\le", r"\sqrt{\mathbb{E}\,\mathrm{VIX}^2_T}", font_size=38,
                      colors={r"\mathbb{E}\,\mathrm{VIX}_T": IV}),
                cmath(r"\min_{\mathbb{Q}}\,H(\mathbb{Q}\,|\,\mathbb{P})", r"\quad\text{s.t.}\quad",
                      r"S_{T_1} \sim \mu_1,\ S_{T_2} \sim \mu_2,\ \mathrm{VIX}_{T_1} \sim \nu,\ \text{martingale}", font_size=32,
                      colors={r"\min_{\mathbb{Q}}\,H(\mathbb{Q}\,|\,\mathbb{P})": OPT})]
        whys = [why(r"quadratic rough Heston in the paper's parametric form; $W$ drives both $S$ and $Z$: pure feedback"),
                why(r"the VIX squared is the log contract's price, conditionally (Part 12)"),
                why(r"Jensen: the right side is fixed by S\&P smiles (a forward variance swap); the VIX future is bounded by them"),
                why(r"Guyon (2024, Finance and Stochastics 28(1)): the dispersion-constrained martingale Schr\"odinger "
                    r"problem; its dual is a Sinkhorn-like iteration with one potential per constraint")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "The mathematics, in four lines. The quadratic rough Heston dynamics, in the paper's own parametric "
            "form. <bookmark mark='a'/> The VIX squared is the market price of the log contract over the next "
            "thirty days, conditionally: Part twelve's formula. <bookmark mark='b'/> By Jensen's inequality, the "
            "VIX future is at most the square root of a forward variance swap, which the S&P smiles fix: the two "
            "markets are tied together by convex order. <bookmark mark='c'/> Guyon's exact answer, published in "
            "2024, is a dispersion-constrained martingale Schrödinger problem: among all martingale models matching "
            "the S&P smiles at two dates and the VIX smile, the one closest in relative entropy to a reference "
            "model, found by a Sinkhorn-like iteration, as in Part nine."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def dmsp(self, jb):
        card = lab_card(r"martingale transport by Sinkhorn", [
            "for it in range(iters + 1):",
            "    for _ in range(newton):          # h: the martingale condition",
            "        L = logpi()",
            "        w = np.exp(L - L.max(1, keepdims=True))",
            "        h += eps * (w * D).sum(1) / (w * D * D).sum(1)",
            "    u = eps * logsumexp(lnu + (C - v - h * D) / eps, axis=1)",
            "    v = eps * logsumexp(lmu + (C - u - h * D) / eps, axis=0)",
        ], source="explainer/quant/house/arbitrage.py: entropic_mot (Part 9)", width=7.4).to_corner(UL, buff=0.3)
        up, lo = jb["upper"], jb["lower"]
        lp = jb.get("lp", {})
        outs = [f"forward-start |log(S2/S1)|, {jb['T1'] * 365:.0f} -> {jb['T2'] * 365:.0f} days, BTC Surface",
                f"lowest {lo['value']:.3f}   highest {up['value']:.3f}   (LP: {lp.get('lower', float('nan')):.3f}, "
                f"{lp.get('upper', float('nan')):.3f})",
                f"rough Bergomi: {jb['rbergomi']:.3f}"]
        tu = np.asarray(up["trace"], float)
        tl = np.asarray(lo["trace"], float)
        it = tu[:, 0]
        g = axes([0, it[-1]], [-10, 1], x_length=5.4, y_length=2.6, xlabel=r"iteration", ylabel=r"constraint error (log)",
                 xticks=[0, it[-1]], yticks=[-10, -5, 0], yfmt=lambda u: f"10^{{{int(u)}}}", font_size=13).to_corner(UR, buff=0.4)
        err_u = np.log10(np.maximum(tu[:, 2] + tu[:, 3], 1e-10))
        err_l = np.log10(np.maximum(tl[:, 2] + tl[:, 3], 1e-10))
        k = 1
        ce = VGroup(curve(g.ax, it[k:], np.clip(err_u[k:], -10, 1), BAD, stroke_width=2.5),
                    curve(g.ax, it[k:], np.clip(err_l[k:], -10, 1), RV, stroke_width=2.5))
        price_range = data_range(tu[1:, 1], tl[1:, 1], [jb["rbergomi"]])
        b = axes(list(price_range), [0, 1], x_length=5.4, y_length=1.0, xlabel=r"price of the claim", xticks=[0.05, 0.1, 0.15, 0.2],
                 yticks=[], font_size=13).next_to(g, DOWN, buff=0.8)
        tv = ValueTracker(0)

        def bounds():
            i = int(np.clip(tv.get_value(), 1, len(tu) - 1))
            vu, vl = float(tu[i, 1]), float(tl[i, 1])
            return VGroup(Line(b.ax.c2p(vl, 0.5), b.ax.c2p(vu, 0.5), stroke_color=YELLOW, stroke_width=6),
                          Dot(b.ax.c2p(vl, 0.5), color=RV), Dot(b.ax.c2p(vu, 0.5), color=BAD))

        bd = always_redraw(bounds)
        rbd = Triangle(color=MODEL_COL["rBergomi"], fill_opacity=1).scale(0.1).rotate(PI).move_to(
            b.ax.c2p(jb["rbergomi"], 0.95))
        rbl = label(r"rough Bergomi", font_size=14, color=MODEL_COL["rBergomi"]).next_to(rbd, UP, buff=0.05)
        warn = label('finite SVI-derived BTC marginals, convex-order adjusted; entropic objectives are interior values, LP gives grid extrema; no VIX marginal',
                     font_size=16, color=GREY_B).to_edge(DOWN, buff=0.25)
        inside = lp.get("lower", -1) <= jb["rbergomi"] <= lp.get("upper", 2)
        verdict = "inside the interval, as any model that fits both smiles must be" if inside else "outside the interval: a sign of Monte Carlo error"
        with self.voiceover(
            f"""An illustration using Bitcoin smiles near {jb['T1'] * 365:.0f} and {jb['T2'] * 365:.0f} days. SVI-derived densities are truncated and discretized, and the second support is adjusted to satisfy convex order. We optimize the absolute log return between these dates on that finite martingale grid. <bookmark mark='a'/> The constraint residuals decrease; the upper run finishes around one billionth. Entropic regularization leaves interior objective values {lo['value']:.3f} and {up['value']:.3f}. The unregularized linear program gives the displayed wider grid interval. <bookmark mark='b'/> Rough Bergomi's separate Monte Carlo value is {jb['rbergomi']:.3f}. Its placement is a comparison, not certification that its marginals equal the adjusted grid marginals. These are not rigorous bounds for the full original market smiles. Guyon's three-marginal construction additionally imposes a VIX law and conditional log-contract consistency; this two-marginal solver does neither. Next: signature volatility."""
        ) as vo:
            self.play(FadeIn(card), FadeIn(warn))
            vo.wait_until("a")
            lab_run(self, card, outs[:2], run_time=2, font_size=16)
            self.play(FadeIn(g), FadeIn(b), FadeIn(bd))
            self.play(Create(ce[0]), Create(ce[1]), tv.animate.set_value(len(tu) - 1), run_time=5)
            vo.wait_until("b")
            self.play(FadeIn(rbd), FadeIn(rbl))
        bd.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
