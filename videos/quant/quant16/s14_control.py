from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, METHOD_COL, OPT, PART, SPOT, illustration, load, predict


def hist_bars(ax, values, lo, hi, bins, color, top=None, opacity=0.75):
    h, e = np.histogram(np.clip(values, lo, hi), bins=bins, range=(lo, hi))
    top = top or max(h.max(), 1)
    g = VGroup()
    for k in range(bins):
        if h[k] == 0:
            continue
        x0, x1 = ax.c2p(e[k], 0)[0], ax.c2p(e[k + 1], 0)[0]
        y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, min(h[k] / top, 1.0))[1]
        g.add(Rectangle(width=max(x1 - x0 - 0.01, 0.01), height=max(y1 - y0, 0.005), stroke_width=0, fill_color=color,
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
        g = axes([0, 25], [0, 25], x_length=5.0, y_length=4.6, xlabel=r"geometric Asian $C$ (known exactly)",
                 ylabel=r"arithmetic Asian $Y$", xticks=[0, 10, 20], yticks=[0, 10, 20], font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.25)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(min(a, 25), min(b, 25)), radius=0.02, color=SPOT) for a, b in zip(Cg, Y)])
        b = ValueTracker(0.0)
        mx, my = Cg.mean(), Y.mean()
        line = always_redraw(lambda: Line(ax.c2p(0, np.clip(my - b.get_value() * mx, -2, 27)),
                                          ax.c2p(25, np.clip(my + b.get_value() * (25 - mx), -2, 27)), stroke_color=OPT,
                                          stroke_width=3))
        h = axes([-6, 18], [0, 1], x_length=5.0, y_length=3.4, xlabel=r"$Y - b\,(C - \mathbb{E}C)$", xticks=[0, 10],
                 font_size=15).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.6)
        hist = always_redraw(lambda: hist_bars(h.ax, Y - b.get_value() * (Cg - EC), -6, 18, 60, OPT, top=900))
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
            "Chapter one's error is sigma over root n; we can change the sigma. The most powerful trick is a control "
            "variate. Each dot is one path of an Asian option on sixty-four fixings: across, "
            "the payoff of the geometric average, whose price Kemna and Vorst wrote down in 1990; up, the arithmetic "
            "average we want, which has no formula. <bookmark mark='a'/> They are almost the same number. So subtract "
            "b times the geometric payoff's error, whose mean is known to be zero. As b turns from zero to the "
            "regression slope, watch the histogram on the right. <bookmark mark='b'/> It collapses from a wide bell to a "
            f"needle: with a correlation of {sg['rho']:.4f}, the variance falls by a factor of about "
            f"{sg['ratio']:,.0f}. <bookmark mark='c'/> The stock itself, a weaker control, buys only "
            f"{ss['ratio']:.1f} times."
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
                why(r"set its derivative to zero, then substitute; estimating $b^*$ from the same paths adds only an "
                    r"$O(1/n)$ bias"),
                why(r"pair each normal with its mirror; for a monotone payoff $\rho \le 0$, so at equal work the gain "
                    r"is $1/(1 + \rho)$"),
                why(r"proportional allocation, one stratum at a time: the law of total variance drops the "
                    r"between-strata term")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.2, buff=0.55, edge=6.9)
        q = predict(r"Antithetic pairs for a straddle, $|S_T - K|$?", width=4.6, font_size=21).to_corner(DR, buff=0.3)
        ans = MathTex(rf"\rho_{{\text{{call}}}} = {an['call']:+.2f},\ \ \rho_{{\text{{straddle}}}} = {an['straddle']:+.2f}",
                      font_size=28, color=GOOD).next_to(q, UP, buff=0.2)
        with self.voiceover(
            "Why it works. The variance of the controlled estimator is a parabola in b. <bookmark mark='a'/> Its "
            "minimum sits at the covariance over the control's variance, the regression slope, and what is left is the "
            f"variance times one minus the squared correlation. A correlation of {c['summary']['geo']['rho']:.4f} "
            f"leaves {1 - c['summary']['geo']['rho'] ** 2:.4f} of it. <bookmark mark='b'/> Antithetic pairs average each path with its mirror image. The pair's variance is "
            "half the variance times one plus the correlation between a path and its mirror, which is negative for a "
            f"payoff that only rises: for the call it is {an['call']:.2f}, so pairs are worth twice the paths. "
            "<bookmark mark='c'/> And stratification splits the draws into equally likely slices, with the right "
            "number of paths in each. The law of total variance shows what disappears: the spread between slices. "
            "<bookmark mark='d'/> Pause and predict: mirror pairs for a straddle? "
            f"Its payoff falls and then rises, the correlation is {an['straddle']:+.2f}, and the pairs make it worse."
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
        h = axes([7, 14], [0, 1], x_length=6.0, y_length=2.8, xlabel=r"estimate of the call from 64 paths (500 runs)",
                 xticks=[8, 10.45, 13], xfmt=lambda v: f"{v:g}", font_size=15).to_edge(LEFT, buff=0.8).to_edge(DOWN, buff=0.5)
        hp = hist_bars(h.ax, sm["plain"], 7, 14, 40, GREY_B, top=110, opacity=0.6)
        hs = hist_bars(h.ax, sm["strat"], 7, 14, 40, GOOD, top=110, opacity=0.8)
        nums = VGroup(
            MathTex(rf"n = {st['n']:,}:\ \ 16\ \text{{strata}}\ \div {(st['plain_sd'] / st['s16_sd']) ** 2:.0f},\ \ "
                    rf"256\ \div {(st['plain_sd'] / st['s256_sd']) ** 2:.0f}".replace(",", "{,}"), font_size=28, color=GOOD),
            MathTex(rf"\text{{Latin hypercube, 64-dim Asian:}}\ \div {(lh['mc_sd'] / lh['lhs_sd']) ** 2:.1f}", font_size=28,
                    color=QC.THETA),
            wrapped_label(r"a Latin hypercube stratifies every coordinate at once (one point in each row and column); "
                          r"moment matching rescales the normals to mean 0 and variance 1 exactly", 5.2, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Stratification, live. Cut the unit interval into sixteen equal pieces and put exactly one uniform in "
            "each. <bookmark mark='a'/> Price the "
            "call five hundred times with sixty-four paths each way. The stratified estimates, in green, sit in a "
            "far narrower pile than the plain ones. <bookmark mark='b'/> With 4,096 paths, sixteen strata divide "
            f"the variance by {(st['plain_sd'] / st['s16_sd']) ** 2:.0f}, and two hundred and fifty-six strata by "
            f"{(st['plain_sd'] / st['s256_sd']) ** 2:.0f}. A Latin hypercube stratifies all sixty-four coordinates "
            f"of the Asian at once, and buys {(lh['mc_sd'] / lh['lhs_sd']) ** 2:.1f}."
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
            "The House's version for a plain call is ten lines: mirror the normals, or subtract the slope times the "
            "discounted stock's error, since its mean is today's price. <bookmark mark='a'/> Run each twenty times "
            "with 262,144 paths and measure the root mean square error against Black–Scholes: plain "
            f"{r['plain']:.4f}, mirrors {r['antithetic']:.4f}, the stock as control {r['control']:.4f}. Modest gains "
            "on a vanilla. The thousandfold gains belong to products with a twin that has a formula."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"rmse at 262,144 paths, 20 seeds:", f"plain       {r['plain']:.4f}",
                                 f"antithetic  {r['antithetic']:.4f}", f"control     {r['control']:.4f}"])
        self.wait(0.5)
        self.clear_scene()
