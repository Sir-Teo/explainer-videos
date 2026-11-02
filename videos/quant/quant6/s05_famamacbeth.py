from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import (ALT, BAD, DATA_C, EST, GOOD, PART, hist_bars, load, predict, real_data,
                                        show_card)

FM_CODE = [
    "def fama_macbeth(Y, X, nw_lags=0):",
    "    slopes = []",
    "    for t in range(Y.shape[0]):            # one cross-section a month",
    "        m = np.isfinite(Y[t]) & np.all(np.isfinite(X[t]), axis=1)",
    "        slopes.append(ols(Y[t][m], X[t][m])[\"beta\"])",
    "    G = np.array(slopes)                   # a time series of slopes",
    "    T = len(G)",
    "    mean = G.mean(axis=0)",
    "    se = G.std(axis=0, ddof=1) / np.sqrt(T)  # or Newey-West on G",
    "    return {\"beta\": mean, \"se\": se, \"t\": mean / se, \"slopes\": G}",
]


class FamaMacBeth(VoiceoverScene):
    def construct(self):
        fe = load("panel_fe")
        p = load("panel")
        tp = load("twopass")
        self.card()
        self.stack(fe)
        self.lab(fe, p)
        self.resolve(fe, p)
        self.derive()
        self.twopass(tp, fe)

    def card(self):
        c = chapter_card(4, r"Fama--MacBeth, and five verdicts resolved", r"Which question does each estimator answer?",
                         lit=(1973,), part=PART)
        with self.voiceover("Chapter four. Fama-MacBeth, and the five verdicts resolved."):
            show_card(self, c)
        self.play(FadeOut(c))

    def stack(self, fe):
        Y, X = np.asarray(fe["Y"]), np.asarray(fe["X"])
        sl = np.asarray(fe["slopes"])
        dates = np.asarray(fe["dates"])
        T = len(sl)
        g = axes([-0.6, 1.0], [-0.25, 0.25], x_length=5.4, y_length=4.0, xlabel=r"industry's past-year return",
                 ylabel=r"next month's return", xticks=[-0.5, 0, 0.5, 1.0], yticks=[-0.2, 0, 0.2], font_size=16)
        g.to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        h = axes([-0.3, 0.3], [0, 1], x_length=5.0, y_length=3.4, xlabel=r"monthly slope $\hat\gamma_{1t}$",
                 xticks=[-0.2, 0, 0.2], yticks=[], font_size=16).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.4)
        hax = h.ax
        k = ValueTracker(1.0)
        edges = np.linspace(-0.3, 0.3, 41)

        def cross():
            t = int(min(max(k.get_value(), 1), T)) - 1
            m = (Y[t] > -9) & (X[t] > -9)
            x, y = np.clip(X[t][m], -0.6, 1.0), np.clip(Y[t][m], -0.25, 0.25)
            dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=DATA_C) for a, b in zip(x, y)])
            b = sl[t]
            a = Y[t][m].mean() - b * X[t][m].mean()
            xs = np.array([-0.6, 1.0])
            ys = np.clip(a + b * xs, -0.25, 0.25)
            line = Line(ax.c2p(xs[0], ys[0]), ax.c2p(xs[1], ys[1]), color=EST, stroke_width=3)
            d = dates[t]
            lab = MathTex(rf"{d // 100}\text{{-}}{d % 100:02d}:\ \hat\gamma_{{1t}} = {b:+.3f}", font_size=24,
                          color=EST).next_to(g, UP, buff=0.05).align_to(g, RIGHT)
            return VGroup(dots, line, lab)

        def hist():
            t = int(min(max(k.get_value(), 1), T))
            vals = sl[:t]
            hb = hist_bars(hax, vals, edges, EST, density=False)
            peak = max(max(np.histogram(np.clip(vals, -0.3, 0.3), edges)[0]), 1)
            hb.stretch_to_fit_height(max(3.2 * min(peak / 120, 1.0), 0.02), about_edge=DOWN).align_to(
                hax.c2p(0, 0), DOWN)
            mean = float(vals.mean())
            se = float(vals.std(ddof=1) / np.sqrt(t)) if t > 2 else 0.0
            mk = Line(hax.c2p(mean, 0), hax.c2p(mean, 0.95), color=WHITE, stroke_width=2)
            band_ = Rectangle(width=max(hax.c2p(mean + 2 * se, 0)[0] - hax.c2p(mean - 2 * se, 0)[0], 0.01),
                              height=hax.c2p(0, 0.95)[1] - hax.c2p(0, 0)[1], stroke_width=0, fill_color=GOOD,
                              fill_opacity=0.25).move_to(hax.c2p(mean, 0), aligned_edge=DOWN)
            ro = MathTex(rf"T = {t:,}:\ \bar\gamma_1 = {mean:+.4f} \pm {2 * se:.4f}".replace(",", "{,}"),
                         font_size=24, color=WHITE).next_to(h, UP, buff=0.15)
            return VGroup(hb, band_, mk, ro)
        cm, hm = always_redraw(cross), always_redraw(hist)
        src = real_data(r"Kenneth French's 49 industries, monthly 1928--2020; signal: months $t-12$ to $t-2$")
        with self.voiceover(
            "Eugene Fama and James MacBeth, in 1973, turned a panel into a time series. Each month, take the "
            "cross-section: forty-nine industries, their past-year return across, next month's return up. Fit one "
            "line. Its slope is that month's answer to the question: did this month's winners beat this month's "
            "losers? <bookmark mark='a'/> Then drop the slope onto a pile, and move to the next month. Ninety-three "
            "years go by. Each month's line tilts a different way, and the pile becomes a histogram of eleven "
            "hundred slopes. <bookmark mark='b'/> The estimate is their average. Its standard error is just the "
            "standard error of a mean of a time series: the spread of the slopes divided by the root of the number "
            "of months. Because each slope already contains the whole month's shared shock, the cross-sectional "
            "correlation that sank pooled least squares is absorbed automatically. The band narrows as months "
            "arrive, and it never contains zero."
        ) as vo:
            self.play(FadeIn(g), FadeIn(h), FadeIn(src))
            self.add(cm, hm)
            self.wait(1.0)
            self.play(k.animate.set_value(6), run_time=vo.until("a"), rate_func=linear)
            self.play(k.animate.set_value(T), run_time=vo.until("b") + 4.0, rate_func=rate_functions.ease_in_quad)
            vo.wait_until("b")
        cm.clear_updaters()
        hm.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def lab(self, fe, p):
        card = lab_card(r"Fama--MacBeth in the House", FM_CODE, source="explainer/quant/house/econ.py", width=8.4,
                        font_size=18).to_corner(UL, buff=0.35)
        fm = p["results"]["Fama-MacBeth"]
        outs = [f"fama_macbeth(Y, X)            slope {fm['beta']:.4f}   t = {fm['t']:.2f}",
                f"fama_macbeth(Y, X, nw_lags=6)                  t = {fe['fm_t_nw']:.2f}",
                f"share of months with a positive slope: {100 * fe['share_positive']:.0f}%"]
        with self.voiceover(
            "The House's version is ten lines. Loop over months, run a cross-sectional regression on whatever is "
            "observed that month, and keep the slopes. The estimate is their mean, the standard error their "
            "standard deviation over the root of T, or Newey-West on the slope series if the slopes themselves "
            "are autocorrelated. <bookmark mark='a'/> Run it on the industries: a slope of "
            f"{fm['beta']:.3f}, t-statistic {fm['t']:.1f}; with Newey-West on the slopes, {fe['fm_t_nw']:.1f}. In "
            f"{100 * fe['share_positive']:.0f} percent of months, winners beat losers."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs, run_time=2.4)
        self.wait(0.4)
        self.clear_scene()

    def resolve(self, fe, p):
        ex = fe["examples"]
        cols = [DATA_C, ALT, QC.Q]
        g = axes([-0.7, 1.4], [-0.2, 0.3], x_length=6.2, y_length=4.4, xlabel=r"past-year return",
                 ylabel=r"next month's return", xticks=[-0.5, 0, 0.5, 1.0], yticks=[-0.1, 0, 0.1, 0.2], font_size=16)
        g.to_edge(LEFT, buff=0.5).shift(DOWN * 0.25)
        ax = g.ax
        clouds, means = VGroup(), VGroup()
        for e, c in zip(ex, cols):
            x, y = np.asarray(e["x"]), np.asarray(e["y"])
            clouds.add(VGroup(*[Dot(ax.c2p(np.clip(a, -0.7, 1.4), np.clip(b, -0.2, 0.3)), radius=0.04, color=c)
                                for a, b in zip(x, y)]))
            means.add(Dot(ax.c2p(x.mean(), y.mean()), radius=0.09, color=c))
        xs = np.array([-0.65, 1.35])
        within = Line(ax.c2p(xs[0], fe["within"] * xs[0]), ax.c2p(xs[1], fe["within"] * xs[1]), color=GOOD,
                      stroke_width=4)
        mx, my = np.asarray(fe["mx"]), np.asarray(fe["my"])
        cx, cy = mx.mean(), my.mean()
        between = Line(ax.c2p(xs[0], cy + fe["between"] * (xs[0] - cx)), ax.c2p(xs[1], cy + fe["between"] * (xs[1] - cx)),
                       color=BAD, stroke_width=4)
        allmeans = VGroup(*[Dot(ax.c2p(np.clip(a, -0.7, 1.4), np.clip(b, -0.2, 0.3)), radius=0.018, color=GREY_B,
                                fill_opacity=0.5) for a, b in zip(mx[::3], my[::3])])
        pooled = Line(ax.c2p(xs[0], cy + fe["pooled"] * (xs[0] - cx)), ax.c2p(xs[1], cy + fe["pooled"] * (xs[1] - cx)),
                      color=WHITE, stroke_width=3)
        w = fe["w_within"]
        res = p["results"]
        side = VGroup(
            label(r"three months shown; slopes from all 1{,}116", font_size=19, color=GREY_B),
            MathTex(rf"\text{{within a month: }} {fe['within']:.4f}\ \ (t = {fe['t_within_cluster']:.2f})",
                    font_size=28, color=GOOD),
            MathTex(rf"\text{{dispersion-weighted FM: }} {fe['fm_weighted']:.4f}", font_size=28, color=GOOD),
            MathTex(rf"\text{{between months: }} {fe['between']:.4f}\ \ (t = {fe['t_between_nw']:.2f})",
                    font_size=28, color=BAD),
            MathTex(rf"\text{{pooled}} = {w:.2f} \times {fe['within']:.4f} + {1 - w:.2f} \times ({fe['between']:.4f})",
                    font_size=26, color=WHITE),
            MathTex(rf"= {fe['pooled']:.4f}", font_size=28, color=WHITE),
            MathTex(rf"\text{{equal-weighted FM: }} {res['Fama-MacBeth']['beta']:.4f}", font_size=28, color=ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Now the five verdicts. Why was the pooled slope "
            f"{res['Fama-MacBeth']['beta'] / res['pooled OLS']['beta']:.0f} times smaller? Put three months on one picture, "
            "each in its own colour. Each cloud has its own centre: some months, every industry did well; some "
            "years, every industry had risen. <bookmark mark='a'/> Subtract each month's means, and every cloud "
            "slides to the origin. The slope through the centred clouds is the within-month slope, least squares "
            f"with a separate intercept for every month: {fe['within']:.4f}, with a t-statistic of "
            f"{fe['t_within_cluster']:.2f} clustered by month. And it equals, to the last digit, the Fama-MacBeth "
            "average with each month weighted by how spread out the industries were that month. "
            "<bookmark mark='b'/> What was subtracted is the other half: the month means themselves. Their slope "
            "asks a different question. When the whole market rose over the past year, did the whole market rise "
            f"next month? It did not: {fe['between']:.4f}, a t-statistic of {fe['t_between_nw']:.2f}. "
            "<bookmark mark='c'/> Pooled least squares, without month effects, averages these two slopes, "
            f"weighting the within part by {100 * w:.0f} percent of the variation and the between part by the rest, "
            f"and lands at {fe['pooled']:.4f}. So dispersion weighting explains only part of the gap: the equal-weighted "
            f"Fama-MacBeth slope is {res['Fama-MacBeth']['beta']:.4f}, the dispersion-weighted one {fe['fm_weighted']:.4f}. "
            "The rest is market timing mixed into a cross-sectional question. None of the five verdicts was wrong; "
            "pooled least squares answered a mixture of two questions, and clustering then told the truth about how "
            "noisy that mixture is."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), LaggedStart(*[FadeIn(c) for c in clouds], lag_ratio=0.4),
                      FadeIn(means))
            vo.wait_until("a")
            anims = []
            for c, e, mdot in zip(clouds, ex, means):
                x, y = np.asarray(e["x"]), np.asarray(e["y"])
                shift = ax.c2p(0, 0) - ax.c2p(x.mean(), y.mean())
                anims += [c.animate.shift(shift), mdot.animate.move_to(ax.c2p(0, 0))]
            self.play(*anims, run_time=2.5)
            self.play(Create(within), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeOut(clouds), FadeOut(means), FadeIn(allmeans))
            self.play(Create(between), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(Create(pooled), FadeIn(side[4]), FadeIn(side[5]))
            self.play(FadeIn(side[6]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        C_ = {r"\hat\gamma_1": ALT, r"w_t": GOOD, r"\hat\beta^{FE}": GOOD}
        rows = [cmath(r"\hat\gamma_1", r"=", r"\tfrac1T \textstyle\sum_t \hat\gamma_{1t},\quad "
                      r"\widehat{\mathrm{se}} = s(\hat\gamma_{1t})/\sqrt T", font_size=36, colors=C_),
                cmath(r"\hat\beta^{FE}", r"=", r"\frac{\sum_t\sum_i \tilde x_{it}\tilde r_{it}}{\sum_t\sum_i \tilde x_{it}^2}"
                      r"= \textstyle\sum_t w_t\,\hat\gamma_{1t}", font_size=36, colors=C_),
                cmath(r"w_t", r"=", r"\frac{\sum_i \tilde x_{it}^2}{\sum_s\sum_i \tilde x_{is}^2}", font_size=36,
                      colors=C_),
                cmath(r"\hat\beta^{pooled}", r"=", r"\frac{SS_W}{SS_W + SS_B}\,\hat\beta^{FE} + "
                      r"\frac{SS_B}{SS_W + SS_B}\,\hat\beta^{B}", font_size=36, colors=C_)]
        whys = [why(r"the average of the monthly slopes; the slopes' own variation absorbs any shock they share"),
                why(r"demean within each month ($\tilde x$): each month's slope is $\sum_i \tilde x \tilde r / "
                    r"\sum_i \tilde x^2$, so multiply and divide"),
                why(r"the weights: each month's share of the cross-sectional variation in $x$"),
                why(r"split $\sum (x - \bar x)^2$ into within-month and between-month sums of squares (analysis of "
                    r"variance)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.75, edge=6.8)
        with self.voiceover(
            "The algebra is short. Fama-MacBeth is the plain average of monthly slopes. <bookmark mark='a'/> The "
            "within estimator divides the sum of centred cross-products by the sum of centred squares. Each "
            "month's slope is its own ratio of these, so multiply and divide, and the within estimator is a "
            "weighted average of the monthly slopes, <bookmark mark='b'/> each weighted by that month's share of "
            "the cross-sectional variation. <bookmark mark='c'/> And split the total variation of the regressor "
            "into within and between: the pooled slope is the weighted average of the within and between slopes. "
            "Problem six asks you to prove it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def twopass(self, tp, fe):
        b, m = np.asarray(tp["betas"]), np.asarray(tp["mean"])
        lam = tp["lambda"]
        g = axes([0.4, 1.5], [0, 0.0125], x_length=6.4, y_length=4.4, xlabel=r"market beta (first pass)",
                 ylabel=r"average excess return, monthly", xticks=[0.5, 1.0, 1.5], yticks=[0, 0.005, 0.01],
                 yfmt=lambda u: f"{100 * u:.1f}\\%", font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.25)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.055, color=DATA_C if i < len(b) - 10 else ALT)
                        for i, (x, y) in enumerate(zip(b, m))])
        xs = np.array([0.4, 1.5])
        capm = Line(ax.c2p(xs[0], tp["mkt_mean"] * xs[0]), ax.c2p(xs[1], tp["mkt_mean"] * xs[1]), color=GOOD,
                    stroke_width=3)
        fit = Line(ax.c2p(xs[0], lam[0] + lam[1] * xs[0]), ax.c2p(xs[1], lam[0] + lam[1] * xs[1]), color=BAD,
                   stroke_width=4)
        side = VGroup(
            label(rf"{tp['N']} portfolios: 49 industries and 10 book-to-market deciles, {tp['T']} months, 1963--2020",
                  font_size=19, color=GREY_B),
            MathTex(rf"\hat\lambda_m = {100 * lam[1]:.3f}\%\ \ (t_{{FM}} = {tp['t_fm'][1]:.2f},\ "
                    rf"t_{{Sh}} = {tp['t_shanken'][1]:.2f})", font_size=27, color=BAD),
            MathTex(rf"\text{{market premium: }} {100 * tp['mkt_mean']:.2f}\%\ (t = {tp['mkt_t']:.1f})", font_size=27,
                    color=GOOD),
            MathTex(rf"\hat\lambda_0 = {100 * lam[0]:.2f}\%\ \ (t = {tp['t_fm'][0]:.1f})", font_size=27, color=BAD),
            MathTex(rf"\text{{GRS}}: F = {tp['grs_F']:.2f},\ p = {tp['grs_p']:.3f}", font_size=27, color=ALT),
            MathTex(r"\mathrm{Var}(\hat\lambda) \approx \tfrac1T\big[(1 + \lambda^\top\Sigma_f^{-1}\lambda)\,"
                    r"\sigma_\gamma^2 + \Sigma_f\big]", font_size=26),
            label(r"Shanken (1992): the betas are estimated", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        q = predict(r"Is the market's own past year a buy signal for the market?").to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Fama and MacBeth built the method to test the capital asset pricing model, in two passes. First, "
            "estimate each portfolio's beta from its time series. Second, each month, regress the cross-section of "
            "returns on those betas, and average. If the CAPM holds, the line through the portfolios passes through "
            "zero with a slope equal to the market's premium: the green line. <bookmark mark='a'/> Do it on "
            f"{tp['N']} portfolios since 1963. The fitted line, in red, is flat: a premium for beta of "
            f"{100 * lam[1]:.3f} percent a month, against a market premium of {100 * tp['mkt_mean']:.2f}, and an "
            f"intercept of {100 * lam[0]:.2f} percent with a t-statistic of {tp['t_fm'][0]:.1f}. High-beta "
            "portfolios have not earned more. <bookmark mark='b'/> The betas in the second pass are estimates, so "
            "the second-pass standard errors are too small: Jay Shanken's 1992 correction inflates the variance by "
            "one plus the squared Sharpe ratio of the factor, and adds the factor's own variance. Here the slope "
            "is so close to zero that the correction barely matters. Gibbons, Ross and Shanken's joint test of all "
            f"{tp['N']} intercepts rejects too, with a p-value of {tp['grs_p']:.3f}; Part twenty-four takes up both "
            "tests. <bookmark mark='c'/> Pause and predict, from the decomposition: is the market's own past year a "
            f"buy signal for the market? No: the between slope was {fe['between']:.4f}, with a t-statistic near zero."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.02))
            self.play(Create(capm), FadeIn(side[2]))
            vo.wait_until("a")
            self.play(Create(fit), FadeIn(side[1]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[5]), FadeIn(side[6]), FadeIn(side[4]))
            vo.wait_until("c")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

