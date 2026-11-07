from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, METHOD_COL, OPT, PART, SPOT, illustration, load, predict, axes, data_range, pause_card, flat_camera


def hist_bars(ax, values, lo, hi, bins, color, top=None, opacity=0.75):
    h, e = np.histogram(values, bins=bins, range=(lo, hi))
    top = len(values)
    g = VGroup()
    for k in range(bins):
        if h[k] == 0:
            continue
        x0, x1 = ax.c2p(e[k], 0)[0], ax.c2p(e[k + 1], 0)[0]
        y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, h[k] / top)[1]
        g.add(Rectangle(width=max(x1 - x0 - 0.01, 0.01), height=y1 - y0, stroke_width=0, fill_color=color,
                        fill_opacity=opacity).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0]))
    return g


class Control(VoiceoverScene):
    def construct(self):
        c = load("control")
        m = load("mc")
        self.card()
        self.rotate(c)
        self.proof(c)
        self.strata(c)
        self.lab(m)

    def card(self):
        c = chapter_card(3, r"Variance reduction: controls, mirrors and strata", r"How do you shrink the constant in "
                         r"$\sigma/\sqrt n$?", part=PART)
        with self.voiceover("Chapter three. Variance reduction: control variates, mirrors and strata."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rotate(self, c):
        sc = c["scatter"]
        Y, Cg = np.asarray(sc["Y"]), np.asarray(sc["Cg"])
        EC = c["geo_exact"]
        sg = c["summary"]["geo"]
        ss = c["summary"]["stock"]
        gx = [0, float(np.max(Cg)) * 1.06]
        gy = [0, float(np.max(Y)) * 1.06]
        g = axes(gx, gy, x_length=5.0, y_length=4.6, xlabel=r"geometric payoff $C$ (known expectation)",
                 ylabel=r"arithmetic Asian $Y$", xticks=[0, 10, 20], yticks=[0, 10, 20], font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.25)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.02, color=SPOT) for a, b in zip(Cg, Y)])
        b = ValueTracker(0.0)
        mx, my = Cg.mean(), Y.mean()
        def fitted_segment():
            slope = b.get_value()
            intercept = my - slope * mx
            left, right = gx
            if slope > 1e-12:
                left = max(left, (gy[0] - intercept) / slope)
                right = min(right, (gy[1] - intercept) / slope)
            return Line(ax.c2p(left, intercept + slope * left), ax.c2p(right, intercept + slope * right),
                        stroke_color=OPT, stroke_width=3)
        line = always_redraw(fitted_segment)
        hr = data_range(Y, Y - sg["b"] * (Cg - EC))
        h = axes(hr, [0, 1], x_length=5.0, y_length=3.4, xlabel=r"$Y - b\,(C - \mathbb{E}C)$", ylabel=r"fraction of saved paths per bin", xticks=[0, 10],
                 font_size=15).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.6)
        hist = always_redraw(lambda: hist_bars(h.ax, Y - b.get_value() * (Cg - EC), *hr, 60, OPT))
        rd = VGroup(readout(r"b =", lambda: b.get_value(), digits=3, font_size=28, color=OPT),
                    readout(r"\text{sd} =", lambda: float(np.std(Y - b.get_value() * (Cg - EC))), digits=3, font_size=28,
                            color=OPT)).arrange(RIGHT, buff=1.0).next_to(h, UP, buff=0.25)
        res = VGroup(
            MathTex(rf"\rho = {sg['rho']:.4f}:\ \text{{variance}} \div {sg['ratio']:,.0f}".replace(",", "{,}"),
                    font_size=30, color=GOOD),
            MathTex(rf"\text{{the stock as control:}}\ \rho = {ss['rho']:.2f},\ \div {ss['ratio']:.1f}", font_size=28,
                    color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.35)
        src = illustration(r"arithmetic Asian call, 64 fixings, one year; 2{,}000 paths drawn, 20{,}000 $\times$ 5 seeds counted")
        with self.voiceover(
            f"A control variate subtracts b times a centered quantity whose expectation is known. Each of these 2,000 points is a discounted Asian payoff pair, with 64 fixings. The geometric payoff varies by path; its expectation has a formula. All saved points and residuals remain visible. <bookmark mark='a'/> Turn b from zero toward the fitted slope. The histograms share fixed bins and divide by all 2,000 observations, so the changing height represents concentration rather than a separate normalization. <bookmark mark='b'/> Across five original 20,000-path runs, the mean reported geometric-control variance ratio is {sg['ratio']:,.0f}, with mean correlation {sg['rho']:.4f}. These are empirical summaries. <bookmark mark='c'/> The stock-control ratio is {ss['ratio']:.1f} in this example. Gains depend on payoff, model and the cost of producing the control."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.0005, run_time=2))
            vo.wait_until("a")
            self.play(FadeIn(h), FadeIn(hist), FadeIn(line), FadeIn(rd))
            vo.wait_until("b")
            self.play(b.animate.set_value(sg["b"]), run_time=4)
            self.play(FadeIn(res[0]))
            vo.wait_until("c")
            self.play(FadeIn(res[1]))
        for x in (line, hist, rd):
            x.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def proof(self, c):
        an = c["anti"]
        rows = [
            cmath(r"\operatorname{Var}\big(Y - b(C - \mathbb{E}C)\big)", r"=", r"\sigma_Y^2 - 2b\,\sigma_{YC} + b^2\sigma_C^2",
                  font_size=34),
            cmath(r"b^*", r"=", r"\sigma_{YC}/\sigma_C^2\ \ \Rightarrow\ \ \sigma_Y^2\,(1 - \rho^2)", font_size=36,
                  colors={r"b^*": OPT}),
            cmath(r"\operatorname{Var}\tfrac{Y + Y'}{2}", r"=", r"\tfrac{\sigma^2}{2}(1 + \rho),\quad "
                  r"\rho = \operatorname{corr}\big(f(Z), f(-Z)\big)", font_size=34, colors={r"\operatorname{Var}\tfrac{Y + Y'}{2}": QC.THETA}),
            cmath(r"\operatorname{Var}_{\text{strat}}", r"=", r"\tfrac1n\sum_k p_k\sigma_k^2 \;=\; \tfrac1n\Big(\sigma^2 - "
                  r"\sum_k p_k(\mu_k - \mu)^2\Big)", font_size=34, colors={r"\operatorname{Var}_{\text{strat}}": GOOD}),
        ]
        whys = [why(r"expand the square: a parabola in $b$"),
                why(r"set its derivative to zero, then substitute; a fixed population coefficient gives the identity; same-sample fitting may bias it (often "
                    r"$O(1/n)$ under regularity); an independent pilot avoids this dependence"),
                why(r"pair each normal with its mirror; for a monotone payoff $\rho \le 0$, so at equal work the gain "
                    r"is $1/(1 + \rho)$"),
                why(r"proportional allocation, one stratum at a time: the law of total variance drops the "
                    r"between-strata term")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-1.2, buff=0.45, edge=6.9)
        q = predict(r"Antithetic pairs for a straddle, $|S_T - K|$?", width=4.6, font_size=21).to_corner(DR, buff=0.3)
        ans = MathTex(rf"\rho_{{\text{{call}}}} = {an['call']:+.2f},\ \ \rho_{{\text{{straddle}}}} = {an['straddle']:+.2f}",
                      font_size=28, color=GOOD).next_to(q, LEFT, buff=0.5).align_to(q, DOWN)
        with self.voiceover(
            f"For a fixed coefficient, expanding the variance gives a quadratic in b. <bookmark mark='a'/> If the control variance is positive, its population minimum is covariance divided by control variance, leaving the factor one minus squared correlation. Estimating b from the same observations may introduce finite-sample bias; a coefficient fitted on an independent pilot remains unbiased when frozen for production. <bookmark mark='b'/> For scalar monotone payoffs, antithetic pairing can give negative correlation. At equal payoff evaluations, the variance ratio is one over one plus that correlation: about two for this call, whose measured correlation is {an['call']:.2f}. <bookmark mark='c'/> Stratification with independent samples inside strata and proportional allocation removes the between-strata component of variance. Integer allocation and setup costs still matter. <bookmark mark='d'/> For the straddle, the measured mirror correlation is {an['straddle']:+.2f}; pairing increases variance at equal evaluations in this benchmark."
        ) as vo:
            for i, mk in enumerate("abc"):
                step(i)
                vo.wait_until(mk)
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(q))
            self.wait(1.5)
            self.play(FadeIn(ans))
        self.wait(0.5)
        self.clear_scene()

    def strata(self, c):
        st, sm, lh = c["strat"], c["strat_small"], c["lhs"]
        line = NumberLine(x_range=[0, 1, 1 / 16], length=11.0, color=GREY_C, include_numbers=False).to_edge(UP, buff=1.1)
        ticks = VGroup(*[Line(line.n2p(k / 16) + UP * 0.15, line.n2p(k / 16) + DOWN * 0.15, color=GREY_B)
                         for k in range(17)])
        u = (np.arange(16) + np.random.default_rng(2).random(16)) / 16
        ur = np.random.default_rng(5).random(16)
        drops = VGroup(*[Dot(line.n2p(x), radius=0.07, color=GOOD) for x in u])
        rnd = VGroup(*[Dot(line.n2p(x) + DOWN * 0.45, radius=0.07, color=GREY_B) for x in ur])
        lab = VGroup(label(r"one uniform per sixteenth (stratified)", font_size=20, color=GOOD).next_to(line, UP, buff=0.25),
                     label(r"sixteen independent uniforms", font_size=20, color=GREY_B).next_to(rnd, DOWN, buff=0.2))
        hr = data_range(sm["plain"], sm["strat"])
        height = max(np.histogram(sm[k], bins=40, range=hr)[0].max() / len(sm[k]) for k in ["plain", "strat"])
        h = axes(hr, [0, height * 1.15], x_length=6.0, y_length=2.8, xlabel=r"call estimate: 64 paths, 500 runs", ylabel=r"fraction of runs per bin",
                 xticks=[8, 10.45, 13], xfmt=lambda v: f"{v:g}", font_size=15).to_edge(LEFT, buff=0.8).to_edge(DOWN, buff=0.5)
        hp = hist_bars(h.ax, sm["plain"], *hr, 40, GREY_B, opacity=0.6)
        hs = hist_bars(h.ax, sm["strat"], *hr, 40, GOOD, opacity=0.8)
        nums = VGroup(
            MathTex(rf"n = {st['n']:,}:\ \ 16\ \text{{strata}}\ \div {(st['plain_sd'] / st['s16_sd']) ** 2:.0f},\ \ "
                    rf"256\ \div {(st['plain_sd'] / st['s256_sd']) ** 2:.0f}".replace(",", "{,}"), font_size=28, color=GOOD),
            MathTex(rf"\text{{Latin hypercube, 64-dim Asian:}}\ \div {(lh['mc_sd'] / lh['lhs_sd']) ** 2:.1f}", font_size=28,
                    color=QC.THETA),
            wrapped_label(r"a Latin hypercube stratifies every coordinate at once (one point in each row and column); "
                          r"moment matching imposes sample moments, changing the joint sampling law; nonlinear estimates may be biased", 5.2, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            f"Place one uniform draw in each of sixteen equal strata. <bookmark mark='a'/> The histograms use five hundred repeated sixty-four-path call estimates, with common bins and a common fraction-of-runs scale. They retain the full saved range. <bookmark mark='b'/> In a separate two-hundred-replicate experiment with four thousand and ninety-six paths, the empirical variance ratios are {(st['plain_sd'] / st['s16_sd']) ** 2:.0f} for sixteen strata and {(st['plain_sd'] / st['s256_sd']) ** 2:.0f} for two hundred and fifty-six. The sixty-four-dimensional Asian's Latin-hypercube ratio is {(lh['mc_sd'] / lh['lhs_sd']) ** 2:.1f}, measured over one hundred replicates of one thousand and twenty-four paths. These finite ratios are not universal gains. Moment matching changes the joint sampling law and can bias nonlinear estimates; setup and transform costs also matter."
        ) as vo:
            self.play(Create(line), FadeIn(ticks), FadeIn(lab))
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.4) for d in drops], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(d, shift=DOWN * 0.4) for d in rnd], lag_ratio=0.15), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(h), FadeIn(hp))
            self.play(FadeIn(hs))
            vo.wait_until("b")
            self.play(FadeIn(nums))
        self.wait(0.5)
        self.clear_scene()

    def lab(self, m):
        r = {k: m["rmse"][k][-1] for k in m["rmse"]}
        card = lab_card(r"mirrors and a control", [
            "if method == 'antithetic':",
            "    z = g.standard_normal(n // 2)",
            "    a = disc * np.maximum(S0*np.exp(drift + vol*z) - K, 0)",
            "    b = disc * np.maximum(S0*np.exp(drift - vol*z) - K, 0)",
            "    y = 0.5 * (a + b)",
            "...",
            "if method == 'control':",
            "    c = disc * ST                  # its mean is S0",
            "    b = np.cov(y, c)[0, 1] / np.var(c, ddof=1)",
            "    y = y - b * (c - S0)",
        ], source="explainer/quant/house/engine.py  mc_call", width=7.4).to_corner(UL, buff=0.4)
        with self.voiceover(
            f"The call code mirrors normals or subtracts a fitted slope times the discounted stock's deviation from its known expectation. The zero-dividend case gives that expectation as today's spot. Same-sample slope fitting can introduce finite-sample bias; an independent frozen pilot is one way to avoid it. <bookmark mark='a'/> Twenty seeds with two hundred and sixty-two thousand one hundred and forty-four paths give empirical RMSE {r['plain']:.4f} for plain simulation, {r['antithetic']:.4f} for mirrors and {r['control']:.4f} for the stock control. These estimates have finite-replicate uncertainty and omit setup-time comparisons. Very large variance reductions require a particularly close control and are not promised for every product. Next, importance sampling and proposal risk."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"rmse at 262,144 paths, 20 seeds:", f"plain       {r['plain']:.4f}",
                                 f"antithetic  {r['antithetic']:.4f}", f"control     {r['control']:.4f}"])
        self.wait(0.5)
        self.clear_scene()
