from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load


class Ito(VoiceoverScene):
    def construct(self):
        i = load("ito")
        o = load("orders")
        self.card()
        self.integral(i)
        self.isometry()
        self.schemes(o)

    def card(self):
        c = chapter_card(2, r"The It\^o integral and its numerics", r"Where do you evaluate the integrand?",
                         lit=(1944,), part=PART)
        with self.voiceover("Chapter two. The Itô integral, and how to compute with it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def integral(self, i):
        rows = i["rows"]
        head = VGroup(label(r"grid points", font_size=22, color=GREY_B), label(r"left points (It\^o)", font_size=22, color=ITO),
                      label(r"midpoints (Stratonovich)", font_size=22, color=STRAT))
        cells = [*head]
        for r in rows:
            cells += [MathTex(f"{r['n']:,}".replace(",", "{,}"), font_size=28), MathTex(f"{r['ito']:+.4f}", font_size=28, color=ITO),
                      MathTex(f"{r['strat']:+.4f}", font_size=28, color=STRAT)]
        cells += [label(r"the limit", font_size=22, color=GREY_B),
                  MathTex(rf"\tfrac12(W_T^2 - T) = {i['ito_limit']:+.4f}", font_size=26, color=ITO),
                  MathTex(rf"\tfrac12 W_T^2 = {i['strat_limit']:+.4f}", font_size=26, color=STRAT)]
        grid = VGroup(*cells).arrange_in_grid(rows=len(rows) + 2, cols=3, buff=(0.6, 0.16), col_alignments="rrr")
        grid.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        title = MathTex(r"\int_0^1 W\,dW \approx \sum W(t^*_k)\,(W_{k+1} - W_k)", font_size=36).to_edge(UP, buff=0.4)
        side = VGroup(
            wrapped_label(r"for a smooth integrator the choice of $t^*$ doesn't matter; for Brownian motion it changes "
                          r"the answer by $\tfrac12 \sum (\Delta W)^2 \to \tfrac12 T$", 4.6, 22, GREY_A),
            wrapped_label(r"It\^o (1944) evaluates at the left end: the integrand is fixed before the move, like a "
                          r"position you hold before the price changes. The result is a martingale.", 4.6, 22, ITO),
            wrapped_label(r"Stratonovich keeps the ordinary chain rule, and suits physics; finance needs It\^o.", 4.6,
                          22, STRAT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "An integral against Brownian motion is a limit of sums: the integrand at some point of each step, times "
            "the step. For ordinary functions it doesn't matter which point you choose. Here it does. Take the "
            "integral of W against W itself, on one path. <bookmark mark='a'/> Evaluate W at the left end of each "
            "step, and the sums converge to a half of W squared minus T. Evaluate at the midpoint, and they converge "
            "to a half of W squared, the answer ordinary calculus would give. <bookmark mark='b'/> The difference is "
            "half the quadratic variation, which never shrinks. <bookmark mark='c'/> Kiyosi Itô chose the left end in "
            "1944, and finance follows him, for a reason a trader recognises: your position is fixed before the price "
            "moves. With that choice, a trading gain against a martingale is itself a martingale. Stratonovich's "
            "midpoint keeps the ordinary chain rule, and physics often prefers it."
        ) as vo:
            self.play(FadeIn(title), FadeIn(VGroup(*cells[:3])))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*cells[3 + 3 * k:6 + 3 * k])) for k in range(len(rows))], lag_ratio=0.3),
                      run_time=4)
            self.play(FadeIn(VGroup(*cells[-3:])))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def isometry(self):
        rows = [cmath(r"\mathbb{E}\Big[\int_0^T H_t\,dW_t\Big]", r"=", r"0", font_size=40, colors={r"0": DRIFT}),
                cmath(r"\mathbb{E}\Big[\Big(\int_0^T H_t\,dW_t\Big)^2\Big]", r"=", r"\mathbb{E}\Big[\int_0^T H_t^2\,dt\Big]",
                      font_size=40, colors={r"\mathbb{E}\Big[\int_0^T H_t^2\,dt\Big]": ITO}),
                cmath(r"df(t, X_t)", r"=", r"f_t\,dt + f_x\,dX_t + \tfrac12 f_{xx}\,d\langle X\rangle_t", font_size=40,
                      colors={r"f_t\,dt + f_x\,dX_t + \tfrac12 f_{xx}\,d\langle X\rangle_t": ITO})]
        whys = [why(r"a gain from a position chosen before each move is a martingale: no free lunch from timing"),
                why(r"the It\^o isometry: the variance of the gain is the integrated squared position"),
                why(r"It\^o's lemma: Taylor to second order, because $(dW)^2 = dt$ (the gentle version derives it)")]
        step = ladder(self, rows, whys, keep=3, top=2.5, x=-2.0, buff=0.95, edge=6.9)
        with self.voiceover(
            "Two facts make the Itô integral useful. Its mean is zero: no position chosen before the moves can earn "
            "anything from a martingale on average. <bookmark mark='a'/> And its variance is the integral of the "
            "squared position, the Itô isometry. That is how a hedger's risk is measured: by how much they hold, for "
            "how long. <bookmark mark='b'/> With the integral comes Itô's lemma, the chain rule with a second-order "
            "term, because d W squared is d t. The series' gentle introduction derives it; here we use it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def schemes(self, o):
        dt = np.log10(np.asarray(o["dt"]))
        g = axes([dt.min() - 0.1, dt.max() + 0.1], [-4.5, -0.5], x_length=7.0, y_length=4.6,
                 xlabel=r"time step $\Delta t$ (log scale)", ylabel=r"error at $T = 1$ (log scale)",
                 xticks=list(np.log10([1 / 256, 1 / 64, 1 / 16, 1 / 4])),
                 xfmt=lambda u: {256: "1/256", 64: "1/64", 16: "1/16", 4: "1/4"}[round(10 ** -u)],
                 yticks=[-4, -3, -2, -1], yfmt=lambda u: rf"10^{{{int(u)}}}", font_size=18).to_edge(LEFT, buff=0.6)
        g.shift(DOWN * 0.2)
        ax = g.ax
        sets = [("strong_euler", JUMP), ("strong_milstein", ITO), ("weak_euler", BM), ("weak_milstein", STRAT)]
        lines = VGroup()
        for k, c in sets:
            y = np.log10(np.asarray(o[k]))
            lines.add(VGroup(curve(ax, dt, y, c, stroke_width=3),
                             *[Dot(ax.c2p(a, b), radius=0.05, color=c) for a, b in zip(dt, y)]))
        leg = legend([(JUMP, rf"Euler, strong: slope {o['slope_strong_euler']:.2f}"),
                      (ITO, rf"Milstein, strong: slope {o['slope_strong_milstein']:.2f}"),
                      (BM, rf"Euler, weak: slope {o['slope_weak_euler']:.2f}"),
                      (STRAT, rf"Milstein, weak: slope {o['slope_weak_milstein']:.2f}")], font_size=21)
        side = VGroup(
            leg,
            MathTex(r"X_{k+1} = X_k + a\,\Delta t + b\,\Delta W", r"+ \tfrac12 b\,b'\,(\Delta W^2 - \Delta t)",
                    font_size=28),
            wrapped_label(r"strong error: how far each simulated path is from the true one (for hedging, and paths); "
                          r"weak error: how far a simulated average is from the true one (for prices)", 4.8, 20, GREY_A),
            label(r"GBM, $\mu = 5\%$, $\sigma = 40\%$; 20{,}000 shared paths", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        side[1][1].set_color(ITO)
        with self.voiceover(
            "To simulate a stochastic differential equation, step it forward. Euler-Maruyama takes the drift times "
            "the step plus the volatility times the Brownian increment. <bookmark mark='a'/> Measure it on geometric "
            "Brownian motion, where the exact answer is known path by path. Halve the step, and the distance between "
            "the simulated and the true path falls only by the square root of two: strong order one half. "
            "<bookmark mark='b'/> Grigori Milstein added one term, the Itô correction from expanding the volatility "
            "to second order, and the error halves with the step: strong order one. <bookmark mark='c'/> For prices, "
            "which are averages, both schemes are already order one: the weak error. Choose the scheme by the "
            "question: a price needs weak accuracy, a hedging simulation needs strong."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[1][0]), FadeIn(side[3]))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1][1]), FadeIn(lines[1]), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2:]), FadeIn(leg[2:]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
