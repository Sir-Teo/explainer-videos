from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause


class Ito(VoiceoverScene):
    def construct(self):
        i = load("ito")
        wz = load("wong_zakai")
        self.card()
        self.ledger(i)
        self.isometry()
        self.left_mid(i)
        self.stratonovich(wz)

    def card(self):
        c = chapter_card(3, r"Constructing the It\^o integral, and Stratonovich's", r"How do you integrate against a path "
                         r"of infinite length?", lit=(1944,), part=PART)
        with self.voiceover("Chapter three. Constructing the Itô integral, and Stratonovich's alternative."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ledger(self, i):
        W = np.asarray(i["W"])
        t = np.linspace(0, 1, len(W))
        g1 = axes([0, 1], [W.min() - 0.15, W.max() + 0.15], x_length=8.0, y_length=1.9, ylabel=r"the price: $W_t$",
                  xticks=[], yticks=[], font_size=16)
        g2 = axes([0, 1], [-1.2, 1.2], x_length=8.0, y_length=1.4, ylabel=r"the position held: $H_{t_k} = W_{t_k}$",
                  xticks=[], yticks=[0], font_size=16)
        g3 = axes([0, 1], [-0.8, 0.4], x_length=8.0, y_length=1.4, xlabel=r"time",
                  ylabel=r"running gain $\sum H_{t_k}\,\Delta W_k$", xticks=[0, 1], yticks=[0], font_size=16)
        VGroup(g1, g2, g3).arrange(DOWN, buff=0.3).to_edge(LEFT, buff=0.5).set_y(-0.1)
        a1, a2, a3 = g1.ax, g2.ax, g3.ax
        path = curve(a1, t, W, BM, stroke_width=2)

        def build(n):
            st = (len(W) - 1) // n
            Wn = W[::st]
            tn = t[::st]
            bars = VGroup(*[Rectangle(width=a2.c2p(1 / n, 0)[0] - a2.c2p(0, 0)[0] - 0.01,
                                      height=max(abs(a2.c2p(0, Wn[k])[1] - a2.c2p(0, 0)[1]), 0.005), stroke_width=0,
                                      fill_color=DRIFT if Wn[k] >= 0 else JUMP, fill_opacity=0.7)
                            .move_to(a2.c2p(tn[k] + 0.5 / n, Wn[k] / 2)) for k in range(n)])
            arrows = VGroup(*[Line(a1.c2p(tn[k + 1], Wn[k]), a1.c2p(tn[k + 1], Wn[k + 1]), stroke_width=3,
                                   color=ITO) for k in range(n)])
            gain = np.concatenate([[0], np.cumsum(Wn[:-1] * np.diff(Wn))])
            gl = VMobject(stroke_color=ITO, stroke_width=3).set_points_as_corners(
                [a3.c2p(a, b) for a, b in zip(tn, gain)])
            return VGroup(bars, arrows, gl), gain[-1]
        g8, v8 = build(8)
        g64, v64 = build(64)
        side = VGroup(
            MathTex(r"I(H) = \sum_k H_{t_k}\,(W_{t_{k+1}} - W_{t_k})", font_size=30, color=ITO),
            wrapped_label(r"$H_{t_k}$ is decided at $t_k$, before the move: a simple, predictable integrand", 4.4, 20,
                          GREY_A),
            MathTex(rf"n = 8:\ {v8:+.3f}", font_size=28, color=GREY_A),
            MathTex(rf"n = 64:\ {v64:+.3f}", font_size=28, color=GREY_A),
            MathTex(rf"\tfrac12(W_1^2 - 1) = {i['ito_limit']:+.3f}", font_size=28, color=ITO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "A Brownian path has infinite length, so the integral of calculus does not exist. Itô built a different "
            "one, easiest to see as a ledger of bets. <bookmark mark='a'/> On top, the price. In the middle, a "
            "position: here, as many units as the price itself, decided at the start of each period and held through "
            "it. <bookmark mark='b'/> Each period the price moves, the position earns position times move, and the "
            "gains drop into a running total at the bottom. That sum is the Itô integral of a simple integrand. "
            "<bookmark mark='c'/> Trade sixty-four times instead of eight, and the total converges to a half of W "
            "squared minus a half: not the half W squared of ordinary calculus."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(g3), Create(path), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in g8[0]], lag_ratio=0.15), FadeIn(side[0]),
                      FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(a) for a in g8[1]], lag_ratio=0.2), Create(g8[2]), run_time=3)
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Transform(g8, g64), run_time=2)
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def isometry(self):
        rows = [cmath(r"\mathbb{E}\big[I(H)^2\big]", r"=", r"\sum_k \mathbb{E}\big[H_{t_k}^2\big]\Delta t_k + 2\sum_{j<k}"
                      r"\mathbb{E}\big[H_{t_j} H_{t_k} \Delta W_j\,\mathbb{E}(\Delta W_k \mid \mathcal{F}_{t_k})\big]",
                      font_size=30),
                cmath(r"\mathbb{E}\big[I(H)^2\big]", r"=", r"\mathbb{E}\int_0^T H_t^2\,dt", font_size=34,
                      colors={r"\mathbb{E}\int_0^T H_t^2\,dt": ITO}),
                cmath(r"\int_0^T H\,dW", r":=", r"\lim_{L^2} I(H^{(m)}), \quad H^{(m)} \to H \text{ in } L^2(dt \otimes dP)",
                      font_size=32),
                cmath(r"\mathbb{E}\Big[\int_0^t H\,dW \;\Big|\; \mathcal{F}_s\Big]", r"=", r"\int_0^s H\,dW", font_size=34,
                      colors={r"\int_0^s H\,dW": DRIFT})]
        whys = [why(r"expand the square; condition each cross term on $\mathcal{F}_{t_k}$ (tower property)"),
                why(r"the cross terms vanish: $\mathbb{E}(\Delta W_k \mid \mathcal{F}_{t_k}) = 0$. The It\^o isometry"),
                why(r"$I$ preserves distance, so a Cauchy sequence of staircases has a limit: the completion"),
                why(r"true for every simple sum, and preserved in the $L^2$ limit: the integral is a martingale")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-2.4, buff=0.6, edge=6.9)
        with self.voiceover(
            "Now the construction. Square the sum and take expectations. The squares give the position squared times "
            "the step. Each cross term pairs an earlier gain, H j times delta W j, with a later position H k, all of "
            "them known at the start of step k, times the later move, whose mean given everything known then is zero. "
            "<bookmark mark='a'/> So the cross terms vanish, and the mean square of the gain is the integrated "
            "squared position: the Itô isometry. That is how a hedger's risk is measured: by how much is held, for "
            "how long. <bookmark mark='b'/> An isometry preserves distance. Staircases that converge to an integrand "
            "give integrals that form a Cauchy sequence in mean square, and the limit is the Itô integral, for any "
            "predictable integrand with finite integrated square. <bookmark mark='c'/> Each simple sum is a "
            "martingale, and conditional expectations survive mean-square limits, so the limit is a martingale too. "
            "Positions chosen before the moves cannot earn anything against a martingale: that one fact is "
            "no-arbitrage pricing, in Part nine."
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

    def left_mid(self, i):
        rows = i["rows"]
        ln = np.log2([r["n"] for r in rows])
        g = axes([1.5, 13.5], [-0.6, 0.4], x_length=7.2, y_length=4.4, xlabel=r"grid points $n$ (log scale)",
                 ylabel=r"$\sum W(t^*_k)\,\Delta W_k$ on one path", xticks=[2, 6, 10],
                 xfmt=lambda u: rf"2^{{{int(u)}}}", yticks=[-0.4, 0, 0.2], font_size=18).to_edge(LEFT, buff=0.6)
        g.shift(DOWN * 0.3)
        ax = g.ax
        lim_i = DashedLine(ax.c2p(1.5, i["ito_limit"]), ax.c2p(13.5, i["ito_limit"]), color=ITO, stroke_width=2)
        lim_s = DashedLine(ax.c2p(1.5, i["strat_limit"]), ax.c2p(13.5, i["strat_limit"]), color=STRAT, stroke_width=2)
        di = VGroup(*[Dot(ax.c2p(a, r["ito"]), radius=0.07, color=ITO) for a, r in zip(ln, rows)])
        ds = VGroup(*[Dot(ax.c2p(a, r["strat"]), radius=0.07, color=STRAT) for a, r in zip(ln, rows)])
        gap = DoubleArrow(ax.c2p(13.0, i["ito_limit"]), ax.c2p(13.0, i["strat_limit"]), buff=0.02, color=GREY_A,
                          stroke_width=3, tip_length=0.15)
        side = VGroup(
            label(rf"left points (It\^o) $\to \tfrac12(W_1^2 - 1) = {i['ito_limit']:+.3f}$", font_size=22, color=ITO),
            label(rf"midpoints (Stratonovich) $\to \tfrac12 W_1^2 = {i['strat_limit']:+.3f}$", font_size=22,
                  color=STRAT),
            MathTex(r"\text{gap} = \tfrac12 \sum (\Delta W)^2 \to \tfrac12 T", font_size=30, color=GREY_A),
            wrapped_label(r"the midpoint sum peeks half a step into the future; the extra is half the quadratic "
                          r"variation of chapter 2", 4.6, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "On one path, evaluate the price at the left end of each step, Itô's choice, or at the midpoint, "
            f"Stratonovich's. <bookmark mark='a'/> The left sums settle at {i['ito_limit']:+.3f}, the midpoint sums at "
            f"{i['strat_limit']:+.3f}. <bookmark mark='b'/> The gap is half the quadratic variation: the midpoint "
            "peeks half a step ahead."
        ) as vo:
            self.play(FadeIn(g), Create(lim_i), Create(lim_s))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in di], lag_ratio=0.3), FadeIn(side[0]), run_time=2)
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in ds], lag_ratio=0.3), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(GrowFromCenter(gap), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def stratonovich(self, wz):
        rows = [cmath(r"\int_0^T H \circ dW", r"=", r"\int_0^T H\,dW + \tfrac12 \langle H, W\rangle_T", font_size=32,
                      colors={r"\tfrac12 \langle H, W\rangle_T": STRAT}),
                cmath(r"dX = b(X) \circ dW", r"\iff", r"dX = \tfrac12\,b\,b'(X)\,dt + b(X)\,dW", font_size=32,
                      colors={r"\tfrac12\,b\,b'(X)\,dt": STRAT})]
        whys = [why(r"midpoint minus left point: half the covariation", 20),
                why(r"put $H = b(X)$: $d\langle b(X), W\rangle = b'(X)\,b(X)\,dt$", 20)]
        step = ladder(self, rows, whys, keep=2, top=3.3, x=-2.2, buff=0.45, edge=6.9)
        t = np.asarray(wz["t"])
        g = axes([0, 1], [0, 3.2], x_length=5.6, y_length=2.8, xlabel=r"time", ylabel=r"$X_t$ on one path",
                 xticks=[0, 1], yticks=[1, 2, 3], font_size=16).to_corner(DL, buff=0.45)
        ax = g.ax
        l_s = curve(ax, t, np.clip(wz["exp_w"], 0, 3.2), STRAT, stroke_width=3)
        l_i = curve(ax, t, np.clip(wz["exp_ito"], 0, 3.2), ITO, stroke_width=3)
        leg = legend([(STRAT, r"$e^{W_t}$: Stratonovich, and the smoothed ODE"),
                      (ITO, r"$e^{W_t - t/2}$: It\^o")], font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        tab = VGroup(MathTex(r"n", font_size=24, color=GREY_B), label(r"ODE, smooth noise", font_size=19, color=STRAT),
                     label(r"Euler (It\^o)", font_size=19, color=ITO))
        cells = [*tab]
        for r in wz["rows"]:
            cells += [MathTex(f"{r['n']:,}".replace(",", "{,}"), font_size=24),
                      MathTex(rf"{r['ode']:.3f} \pm {r['ode_se']:.3f}", font_size=24, color=STRAT),
                      MathTex(rf"{r['em']:.3f} \pm {r['em_se']:.3f}", font_size=24, color=ITO)]
        grid = VGroup(*cells).arrange_in_grid(rows=len(wz["rows"]) + 1, cols=3, buff=(0.35, 0.12))
        theory = MathTex(rf"e^{{1/2}} = {wz['strat']:.3f} \qquad \mathbb{{E}}\,e^{{W_1 - 1/2}} = 1", font_size=26)
        right = VGroup(label(r"$\mathbb{E}X_1$ for $dX = X\,dW$, 20{,}000 paths", font_size=20, color=GREY_A), grid,
                       theory).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.4)
        pc, ans = pause(r"A physicist simulates $dX = X\,dW$ by smoothing the noise. The mean of $X_1$?",
                        rf"About {wz['strat']:.2f}, not 1: smooth noise is Stratonovich noise.", width=5.2,
                        font_size=21)
        pc.to_edge(RIGHT, buff=0.4).set_y(0.2)
        with self.voiceover(
            "The rule connecting them: Stratonovich's integral is Itô's plus half the covariation. "
            "<bookmark mark='a'/> So a Stratonovich equation is an Itô equation with an extra drift, a half b times b "
            "prime. Which is right? <bookmark mark='b'/> A pause: a physicist simulates d X equals X d W by smoothing "
            "the noise. What is the mean of X at time one? <bookmark mark='c'/> Wong and Zakai proved in 1965 that "
            "smoothed noise converges to the Stratonovich solution. On twenty thousand paths the smoothed equation "
            f"gives {wz['rows'][-1]['ode']:.2f}, the square root of e, while Euler's Itô scheme gives "
            f"{wz['rows'][-1]['em']:.2f}. <bookmark mark='d'/> Physics usually wants Stratonovich; finance wants Itô, "
            "because positions are set before prices move."       ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(pc))
            vo.wait_until("c")
            self.play(FadeOut(pc), FadeIn(g), FadeIn(leg), Create(l_s), Create(l_i), FadeIn(right), run_time=2)
            vo.wait_until("d")
            self.play(Indicate(grid, color=STRAT, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()
