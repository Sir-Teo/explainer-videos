from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data, predict


class Dcc(VoiceoverScene):
    def construct(self):
        e = load("dcc_ell")
        d = load("dcc")
        self.card()
        self.ellipses(e)
        self.derive(d)
        self.structure(d)
        self.path(d, e)

    def card(self):
        c = chapter_card(8, r"Correlations that move", r"Is the stock--bond correlation a constant?", part=PART)
        with self.voiceover("Chapter eight. Correlations that move."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ellipses(self, e):
        years = list(e["years"])
        cov = [np.asarray(c) for c in e["cov"]]
        rho = np.asarray(e["rho"])
        xm = 1.05 * max(np.sqrt(c[0, 0]) for c in cov)
        ym = 1.05 * max(np.sqrt(c[1, 1]) for c in cov)
        g = axes([-xm, xm], [-ym, ym], x_length=7.2, y_length=3.6 * 7.2 / 7.2 * 0.5 * 2, xticks=[-0.4, 0, 0.4],
                 yticks=[-0.2, 0, 0.2], xfmt=lambda u: f"{100 * u:+.0f}\\%" if u else "0",
                 yfmt=lambda u: f"{100 * u:+.0f}\\%" if u else "0", xlabel=r"US stocks (annualised daily return)",
                 ylabel=r"10-year Treasury bond", font_size=15).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        k = ValueTracker(0)

        def ell():
            i = int(round(k.get_value()))
            C = cov[i]
            w, V = np.linalg.eigh(C)
            th = np.linspace(0, 2 * np.pi, 80)
            pts = (V @ (np.sqrt(np.maximum(w, 1e-12))[:, None] * np.vstack([np.cos(th), np.sin(th)]))).T
            col = BAD if rho[i] > 0 else GOOD
            return VMobject(stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.2).set_points_as_corners(
                [ax.c2p(*p) for p in pts] + [ax.c2p(*pts[0])])

        e_ = always_redraw(ell)
        yr = always_redraw(lambda: MathTex(str(years[int(round(k.get_value()))]), font_size=44).to_corner(UR, buff=0.6))
        cx, R = np.array([4.4, -0.9, 0]), 1.6
        arc = Arc(radius=R, start_angle=0, angle=PI, arc_center=cx, color=GREY_B, stroke_width=3)
        ticks = VGroup(*[MathTex(s, font_size=22, color=GREY_B).move_to(cx + (R + 0.3) * np.array([np.cos(a_), np.sin(a_), 0]))
                         for s, a_ in ((r"+1", 0), (r"0", PI / 2), (r"-1", PI))])
        needle = always_redraw(lambda: Line(cx, cx + R * 0.92 * np.array([np.cos(PI / 2 * (1 - rho[int(round(k.get_value()))])),
                                                                          np.sin(PI / 2 * (1 - rho[int(round(k.get_value()))])), 0]),
                                            color=YELLOW, stroke_width=5))
        rv = always_redraw(lambda: MathTex(rf"\rho = {rho[int(round(k.get_value()))]:+.2f}", font_size=34,
                                           color=YELLOW).next_to(cx, DOWN, buff=0.35))
        dial_lab = label(r"the year's stock--bond correlation", font_size=18, color=GREY_A).next_to(arc, UP, buff=0.5)
        src = real_data('one-SD covariance contours; French market; duration-8 bond proxy: carry minus $8\\Delta$yield')
        i00 = years.index(2000)
        with self.voiceover(
            "Volatilities move, and so do correlations. Here is one ellipse per year: the spread of daily returns of "
            "American stocks across, and ten-year Treasury bonds up, from 1962. <bookmark mark='a'/> Watch it "
            "breathe as volatility rises and falls, and watch it tilt. Through the inflationary seventies and "
            "eighties it leans up: stocks and bonds fall together. <bookmark mark='b'/> Around 2000 it straightens, then leans the other way: bonds rise when stocks fall. The needle tracks the correlation. The sign change improved diversification in this illustration; it was not the sole cause of sixty-forty performance."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(arc), FadeIn(ticks), FadeIn(dial_lab))
            self.add(e_, yr, needle, rv)
            vo.wait_until("a")
            self.play(k.animate.set_value(i00 - 3), run_time=max(vo.until("b") - 0.3, 3), rate_func=linear)
            self.play(k.animate.set_value(len(years) - 1), run_time=max(vo.remaining(1.0) - 0.3, 3), rate_func=linear)
        for m in (e_, yr, needle, rv):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def derive(self, d):
        rows = [
            cmath(r"H_t", r"=", r"D_t R_t D_t,\quad D_t = \operatorname{diag}(\sigma_{1t}, \ldots, \sigma_{Nt})", font_size=36),
            cmath(r"Q_t", r"=", r"(1 - a - b)\bar Q + a\,z_{t-1}z_{t-1}' + b\,Q_{t-1}", font_size=36),
            cmath(r"R_t", r"=", r"\operatorname{diag}(Q_t)^{-1/2}\,Q_t\,\operatorname{diag}(Q_t)^{-1/2}", font_size=36),
            cmath(r"\ell", r"=", r"\ell_{vol}(\theta_1) + \ell_{corr}(\theta_2 \mid \theta_1)", font_size=36),
        ]
        whys = [why(r"separate the volatilities from the correlations"),
                why(r"a GARCH(1,1) for the standardized residuals' co-movement: Engle (2002)"),
                why(r"rescale so the diagonal is one: a valid correlation matrix every day"),
                why(r"the log-determinant splits: fit each GARCH, then the two correlation parameters")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-2.2, buff=0.45, edge=6.9)
        N = 100
        counts = [(r"VEC", (N * (N + 1) // 2) * (1 + N * (N + 1)), BAD), (r"BEKK", N * (N + 1) // 2 + 2 * N * N, ALT),
                  (r"DCC", 3 * N + 2, GOOD)]
        tab = VGroup(label(r"coefficient counts; DCC excludes its target:", font_size=21, color=GREY_A),
                     *[MathTex(rf"\text{{{n_}: }}{c:,}".replace(",", "{,}"), font_size=30, color=col) for n_, c, col in counts])
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.5)
        fit = MathTex(rf"\text{{stocks and bonds, 1962--2020: }} a = {d['a']:.3f},\ b = {d['b']:.3f}", font_size=30,
                      color=VOL).to_corner(DR, buff=0.6)
        with self.voiceover(
            "How to model it. A full multivariate GARCH for a hundred assets has over fifty million parameters; even the restricted BEKK form has twenty-five thousand. Robert Engle's dynamic conditional correlation of 2002 needs three "
            "hundred and two dynamic coefficients, plus the correlation target entries. <bookmark mark='a'/> Split the covariance into volatilities and correlations. "
            "<bookmark mark='b'/> Fit a GARCH to each asset, then run a GARCH-like recursion on the products of their "
            "standardized shocks, <bookmark mark='c'/> rescaled each day into a proper correlation matrix. "
            "<bookmark mark='d'/> The likelihood splits in two, so it is estimated in two easy steps. On stocks and "
            f"bonds, b is {d['b']:.3f}: correlation shocks are very persistent."
        ) as vo:
            self.play(FadeIn(tab))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(fit))
        self.wait(0.3)
        self.clear_scene()

    def path(self, d, e):
        t, rho = np.asarray(d["t"]), np.asarray(d["rho"])
        g = axes([1962, 2021], [-1, 1], x_length=8.4, y_length=4.0, ylabel=r"correlation of stocks and Treasury bonds",
                 xticks=[1970, 1990, 2010], xfmt=lambda u: f"{int(u)}", yticks=[-0.8, -0.4, 0, 0.4, 0.8], font_size=17)
        g.to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        zero = DashedLine(ax.c2p(1962, 0), ax.c2p(2021, 0), color=GREY_B, stroke_width=2)
        ew = curve(ax, np.asarray(e["t"]), e["ewma"], GREY_B, stroke_width=1.2).set_stroke(opacity=0.6)
        line = curve(ax, t, rho, ALT, stroke_width=2.8)
        leg = legend([(ALT, r"DCC"), (GREY_B, r"EWMA, $\lambda = 0.94$: noisier")], font_size=18).next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        safer = e["real_6040"] < e["model_6040"]
        pc = predict(r"Your 60/40 risk model assumed $\rho = +0.3$ in 2010. Holding realized marginal volatilities fixed, was risk higher or lower?", width=4.6, font_size=20).to_edge(RIGHT, buff=0.3).shift(UP * 1.2)
        ans = VGroup(MathTex(rf"\text{{model: }} {100 * e['model_6040']:.1f}\%", font_size=28, color=GREY_A),
                     MathTex(rf"\text{{realized: }} {100 * e['real_6040']:.1f}\%", font_size=28, color=GOOD if safer else BAD),
                     MathTex(rf"\rho_{{2010}} = {e['rho_2010']:+.2f}", font_size=28, color=ALT))
        ans.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(pc, DOWN, buff=0.3)
        verdict = (f"Safer. With the correlation at {e['rho_2010']:+.2f}, the portfolio's volatility was "
                   f"{100 * e['real_6040']:.0f} percent, not the {100 * e['model_6040']:.0f} the model said."
                   if safer else "Riskier than the model said.")
        with self.voiceover(
            f"Here is the fitted correlation day by day, with a plain exponential average in grey for comparison: the "
            f"DCC path is smoother, because its memory is longer. For much of the earlier period, correlation was positive: inflation "
            f"hurt both. Then it turned. <bookmark mark='a'/> Pause and predict. In 2010 your risk model for a sixty-forty "
            f"portfolio still assumed a correlation of plus zero point three. Holding realized marginal volatilities fixed, was risk higher or lower? This isolates the correlation assumption retrospectively. <bookmark mark='b'/> {verdict} In 2022, outside our window, the sign turned again."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(leg), Create(ew), Create(line), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(pc))
            vo.wait_until("b")
            self.play(FadeIn(ans))
        self.wait(0.3)
        self.clear_scene()

    def structure(self, d):
        a, b = d["a"], d["b"]
        hl = np.log(0.5) / np.log(a + b)
        rows = [
            cmath(r"Q_t", r"=", r"\sum_{k\ge0}b^k\big[(1-a-b)\bar Q + a\,z_{t-1-k}z_{t-1-k}'\big]", font_size=34),
            cmath(r"x'Q_tx", r"=", r"\sum_k b^k\big[(1-a-b)\,x'\bar Qx + a\,(x'z_{t-1-k})^2\big] \ge 0", font_size=34),
            cmath(r"\mathbb{E}_t Q_{t+h}", r"=", r"(1-a-b)\bar Q+a\mathbb{E}_tR_{t+h-1}+b\mathbb{E}_tQ_{t+h-1},\ h\ge2", font_size=29),
        ]
        whys = [why(r"unroll the recursion: a weighted sum of outer products"),
                why(r"$\bar Q,Q_0\succ0$, $a,b\ge0$, $a+b<1$: positive definiteness makes normalization valid"),
                why(r"$\mathbb{E}_{t-1}z_tz_t\prime=R_t$, not $Q_t$; normalized-correlation forecasts are nonlinear")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-1.8, buff=0.55, edge=6.9)
        res = MathTex(rf"a + b = {a + b:.3f}:\ \text{{linearized persistence half-life: }} {hl:.0f}\text{{ trading days}}",
                      font_size=30, color=VOL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Why the recursion is safe. Unroll it, and today's matrix is a weighted sum of the long-run matrix and of "
            "outer products of past shocks. <bookmark mark='a'/> With a positive definite target and start, nonnegative a and b, and their sum below one, Q stays positive definite and normalization gives a valid correlation matrix. <bookmark mark='b'/> Multi-step forecasts are nonlinear: the expected shock outer product is R, not Q. The exact recursion retains an expected R term; replacing it by Q is only a linearization. <bookmark mark='c'/> For "
            f"stocks and bonds a plus b is {a + b:.3f}: the a-plus-b persistence summary gives a half-life of about {hl:.0f} trading days. This is not an exact half-life of normalized correlation forecasts. Correlation regimes are slow, which is why they matter so much to a "
            "balanced portfolio and why a model fitted to one decade can be wrong for the next."
            " All these models infer volatility from daily returns. With intraday data we can measure it. Next."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()
