from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import BAD, FRONT, GOOD, MKT, PART, TAN, ask, fit_right, illustration, load


class Markowitz(VoiceoverScene):
    def construct(self):
        self.card()
        self.two(load("twoasset"))
        self.lagrange()
        self.solution()
        f = load("frontier")
        self.bullet(f)
        self.weights(f)

    def card(self):
        c = chapter_card(1, r"Markowitz: the frontier", r"Which portfolios are worth holding?", lit=(1952,), part=PART)
        with self.voiceover("Chapter one. Harry Markowitz's frontier: which portfolios are worth holding at all."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def two(self, t):
        cv = t["curves"]
        g = axes([0, 0.36], [0.03, 0.13], x_length=7.2, y_length=4.4, xlabel=r"volatility", ylabel=r"expected return",
                 xticks=[0, 0.1, 0.2, 0.3], yticks=[0.04, 0.06, 0.08, 0.10, 0.12], font_size=14).to_edge(
            LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        cols = [GOOD, TAN, FRONT, MKT, BAD]
        lines = VGroup()
        for c_, col in zip(cv, cols):
            w = np.asarray(c_["w"])
            sel = (w >= -0.25) & (w <= 1.25)
            lines.add(curve(ax, np.asarray(c_["sd"])[sel], np.asarray(c_["mu"])[sel], col, stroke_width=3))
        a1 = Dot(ax.c2p(0.2, 0.06), color=WHITE)
        a2 = Dot(ax.c2p(0.2, 0.10), color=WHITE)
        side = VGroup(
            legend([(col, rf"$\rho = {c_['rho']:+.1f}$") for c_, col in zip(cv, cols)], font_size=17),
            MathTex(r"\sigma_p^2 = w^2\sigma_1^2 + (1-w)^2\sigma_2^2 + 2w(1-w)\rho\sigma_1\sigma_2", font_size=22),
            wrapped_label(r"two assets, each with 20\% volatility, expected returns 6\% and 10\%. Below a correlation of "
                          r"one, some mix is less risky than either: 'the only free lunch in finance', as Markowitz is often quoted", 3.6, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Two assets, each with twenty percent volatility, one expected to earn six percent and the other ten. "
            "<bookmark mark='a'/> Mix them, and trace the mixtures' risk and return as the weight moves. If the two move "
            "in perfect lockstep, the line is straight: mixing changes the return, not the risk. <bookmark mark='b'/> "
            "As the correlation falls the line bows to the left, and at minus one it touches zero risk. Below perfect "
            "correlation, some mix is always less risky than either asset alone; where exactly that mix sits is the "
            "question at the end of this chapter. Diversification is the only free lunch in finance, as Markowitz "
            "is often quoted, and this is why."
        ) as vo:
            self.play(FadeIn(g), FadeIn(a1), FadeIn(a2), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(lines[4]), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines[3::-1]], lag_ratio=0.4), FadeIn(side[0]), FadeIn(side[2]),
                      run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def lagrange(self):
        rows = [cmath(r"\min_w\ \tfrac12 w^\top\Sigma w", r"\ \text{s.t.}\ ", r"w^\top\mu = m,\quad w^\top\mathbf{1} = 1",
                      font_size=38),
                cmath(r"\Sigma w", r"=", r"\lambda\mu + \gamma\mathbf{1}\ \Rightarrow\ w = \Sigma^{-1}(\lambda\mu + \gamma\mathbf{1})",
                      font_size=38, colors={r"\Sigma w": FRONT}),
                cmath(r"\sigma^2(m)", r"=", r"\frac{C m^2 - 2A m + B}{D}", font_size=40, colors={r"\sigma^2(m)": FRONT})]
        whys = [why(r"the frontier: for each target mean $m$, the fully invested portfolio with the smallest variance"),
                why(r"the Lagrangian's first-order condition: every frontier portfolio is a combination of just two, "
                    r"$\Sigma^{-1}\mu$ and $\Sigma^{-1}\mathbf{1}$ (two-fund separation)"),
                why(r"with $A = \mathbf{1}^\top\Sigma^{-1}\mu$, $B = \mu^\top\Sigma^{-1}\mu$, $C = \mathbf{1}^\top\Sigma^{-1}"
                    r"\mathbf{1}$, $D = BC - A^2$: a hyperbola in mean and volatility, the 'bullet'")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "With many assets, ask the same question for each target return: of all fully invested portfolios with "
            "that expected return, which has the least variance? <bookmark mark='a'/> The Lagrangian answers it in one "
            "line. The optimal weights are a combination of just two portfolios, the inverse covariance times the "
            "means, and the inverse covariance times a vector of ones. Every efficient portfolio is a mix of the same "
            "two funds. <bookmark mark='b'/> And the variance, as a function of the target, is a parabola; in mean and "
            "volatility, a hyperbola. Investors call it the bullet."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def solution(self):
        rows = [cmath(r"w_{\text{GMV}}", r"=", r"\frac{\Sigma^{-1}\mathbf{1}}{C},\quad \sigma^2_{\text{GMV}} = \frac1C,\quad "
                      r"\mu_{\text{GMV}} = \frac AC", font_size=38, colors={r"w_{\text{GMV}}": GOOD})]
        whys = [why(r"the nose of the bullet, the global minimum-variance portfolio, needs no expected returns at all: "
                    r"only the covariance matrix, which is estimated far more precisely than the means (chapter 2)")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "One portfolio on the frontier is special: its nose, the global minimum-variance portfolio. Its weights "
            "need only the covariance matrix, not a single expected return. That will matter, because covariances can "
            "be estimated far more precisely than means, and the next chapter shows what happens when the means are "
            "wrong."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def bullet(self, f):
        ms, sig = np.asarray(f["ms"]), np.asarray(f["sig"])
        g = axes([0, 0.32], [0.04, 0.24], x_length=7.4, y_length=4.4, xlabel=r"volatility, a year", ylabel=r"mean return, a year",
                 xticks=[0, 0.1, 0.2, 0.3], yticks=[0.05, 0.10, 0.15, 0.20], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        ok = sig <= 0.32
        line = curve(ax, sig[ok], ms[ok], FRONT, stroke_width=3.5)
        dots = VGroup(*[VGroup(Dot(ax.c2p(a["sd"], a["mu"]), color=WHITE, radius=0.05),
                               label(a["name"], font_size=13, color=GREY_A).next_to(ax.c2p(a["sd"], a["mu"]), RIGHT, buff=0.05))
                        for a in f["assets"]])
        gm = f["gmv"]
        gdot = VGroup(Dot(ax.c2p(gm["sd"], gm["mu"]), color=GOOD, radius=0.08),
                      label(r"GMV", font_size=15, color=GOOD).next_to(ax.c2p(gm["sd"], gm["mu"]), LEFT, buff=0.08))
        mk = f["mkt"]
        mdot = VGroup(Dot(ax.c2p(mk["sd"], mk["mu"]), color=MKT, radius=0.08),
                      label(r"market", font_size=15, color=MKT).next_to(ax.c2p(mk["sd"], mk["mu"]), DOWN, buff=0.08))
        side = VGroup(
            MathTex(rf"\text{{GMV}}:\ \sigma = {100 * gm['sd']:.1f}\%,\ \mu = {100 * gm['mu']:.1f}\%", font_size=24,
                    color=GOOD),
            wrapped_label(rf"Kenneth French's ten US industries, monthly {f['start'] // 100}--{f['end'] // 100}, "
                          r"annualised; short sales allowed. Every industry sits inside the bullet: each alone is a poor "
                          r"portfolio", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Now real assets: ten American industries, monthly since 1990. <bookmark mark='a'/> Each industry alone, a "
            "dot. <bookmark mark='b'/> The frontier built from them: every industry sits well inside it, because each "
            "alone carries risk that a mix can diversify away. <bookmark mark='c'/> The minimum-variance portfolio has "
            f"{100 * gm['sd']:.0f} percent volatility, less than any single industry, and less than the market itself."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(mdot), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(gdot), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def weights(self, f):
        w = np.asarray(f["tan"]["w"])
        cols = f["columns"]
        g = axes([-0.6, len(w) - 0.4], [-0.6, 0.6], x_length=8.4, y_length=4.0, xlabel=r"", ylabel=r"weight",
                 xticks=[], yticks=[-0.5, -0.25, 0, 0.25, 0.5], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        zero = Line(ax.c2p(-0.6, 0), ax.c2p(len(w) - 0.4, 0), color=WHITE, stroke_width=1.2)
        bars = VGroup()
        for i, (c_, v) in enumerate(zip(cols, w)):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            bars.add(VGroup(Rectangle(width=0.55, height=max(abs(y1 - y0), 0.01), stroke_width=0,
                                      fill_color=GOOD if v >= 0 else BAD, fill_opacity=0.85).move_to(
                [ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]), label(c_, font_size=14).next_to(ax.c2p(i, -0.6), DOWN, buff=0.08)))
        side = wrapped_label(r"the tangency portfolio of the next chapter, from the full sample: large long and short "
                             r"positions, driven by small differences in estimated means. Telecoms short 42\%, shops long "
                             r"41\%: no investor would hold it", 3.4, 17, GREY_A).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "But look at the weights the optimiser wants for its best portfolio. <bookmark mark='a'/> Short telecoms by "
            "thirty percent, long shops and utilities by more than forty, short the catch-all 'other' industry by more than half. These are not "
            "insights about industries. They are the optimiser chasing small differences in average returns, which are "
            "measured with enormous error: a mean return over thirty-one years still has a standard error of about two "
            "and a half points a year. Markowitz's machine maximises the error along with the return."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.1), FadeIn(side))
        q = ask(r"two assets, each with 20\% volatility and correlation 0.5. What are the minimum-variance weights, and "
                r"its volatility?")
        with self.voiceover("Two assets, each with twenty percent volatility, correlation one half. What are the "
                            "minimum-variance weights, and its volatility?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
