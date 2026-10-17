from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import NEURON, curve, load

PLAIN, RES, NORM = C.SURPRISE, C.BITS, C.INTERVAL


class Residual(VoiceoverScene):
    def construct(self):
        self.card()
        self.block()
        self.curves()

    def card(self):
        card = chapter_card(4, r"The residual stream", r"How do you train forty layers?", part=8, lit=(2015,))
        with self.voiceover("Chapter four. Residual connections."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def block(self):
        # a plain stack against a residual stack, drawn as boxes
        def stack(x, residual):
            g = VGroup()
            ys = [2.2 - 1.05 * k for k in range(4)]
            spine = Line([x, 2.8, 0], [x, -2.0, 0], color=RES if residual else GREY_D, stroke_width=6 if residual else 0)
            g.add(spine)
            for yv in ys:
                box = RoundedRectangle(width=1.6, height=0.6, corner_radius=0.12, stroke_color=NEURON, stroke_width=2.5,
                                       fill_color="#121722", fill_opacity=1).move_to([x + (1.3 if residual else 0), yv - 0.5, 0])
                g.add(box, MathTex(r"f_\ell", font_size=28).move_to(box))
                if residual:
                    g.add(Arrow([x, yv, 0], box.get_top() + LEFT * 0.3, buff=0.05, color=GREY_B, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.2),
                          Arrow(box.get_bottom() + LEFT * 0.3, [x, yv - 1.0, 0], buff=0.05, color=GREY_B, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.2),
                          MathTex(r"+", font_size=30, color=RES).move_to([x - 0.25, yv - 1.0, 0]))
                else:
                    g.add(Arrow([x, yv + 0.2, 0], box.get_top(), buff=0.03, color=GREY_B, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.2))
            return g

        plain = stack(-4.2, False)
        res = stack(0.6, True)
        pt = label(r"plain: \ $h_{\ell+1} = f_\ell(h_\ell)$", font_size=28, color=PLAIN).next_to(plain, DOWN, buff=0.3)
        rt = label(r"residual: \ $h_{\ell+1} = h_\ell + f_\ell(h_\ell)$", font_size=28, color=RES).next_to(res, DOWN, buff=0.3)
        colors = {r"I": RES}
        jac = cmath(r"\frac{\partial h_{\ell+1}}{\partial h_\ell}", "=", r"I", "+", r"\frac{\partial f_\ell}{\partial h_\ell}",
                    colors=colors, font_size=38).move_to([4.8, 1.2, 0])
        jl = label(r"the identity always gets through: \\ gradients reach the first layers", font_size=24, color=GREY_A)
        jl.next_to(jac, DOWN, buff=0.3)
        cite_ = cite(r"K.~He, X.~Zhang, S.~Ren \& J.~Sun, \textit{Deep Residual Learning for Image Recognition} (2015)",
                     corner=DR)
        with self.voiceover(
            "Good initialization gets a signal through at the start, but training can still go wrong in a deep "
            "stack. In 2015, Kaiming He and colleagues found a fix so simple it's now everywhere. "
            "<bookmark mark='a'/> Instead of each layer replacing what came before, let it add to it. The layers "
            "become small corrections to a stream of numbers flowing straight through: the residual stream. "
            "<bookmark mark='b'/> By the chain rule, the derivative of each block is the identity plus a little "
            "extra, so gradients always have a clear path back to the first layer. Every transformer in this "
            "series is built this way."
        ) as vo:
            self.play(FadeIn(plain), FadeIn(pt), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(res), FadeIn(rt))
            vo.wait_until("b")
            self.play(Write(jac), FadeIn(jl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        r = load("residual")
        P, R, N = (np.asarray(r[k]) for k in ("plain", "residual", "residual_norm"))
        ax = Axes(x_range=[0, P[-1, 0], 500], y_range=[0.4, 1.0, 0.1], x_length=8.0, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.6, -0.5, 0])
        yl = VGroup(*[MathTex(rf"{int(round(100 * v))}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0.5, 0.75, 1.0)])
        xl = label(r"training steps", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yn = label(r"spiral points on the right side", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        cp, cr, cn = (curve(ax, D[:, 0], D[:, 2], col, 4) for D, col in ((P, PLAIN), (R, RES), (N, NORM)))
        names = VGroup(label(rf"$40$ plain layers: \ ${100 * P[-1, 2]:.0f}\%$, \ a coin flip", font_size=26, color=PLAIN),
                       label(rf"$40$ residual layers: \ ${100 * R[-1, 2]:.0f}\%$", font_size=26, color=RES),
                       label(r"with LayerNorm too", font_size=26, color=NORM))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.6, 0.8, 0])
        colors = {r"\mu": NORM, r"\sigma": NORM}
        ln = cmath(r"\mathrm{LN}(h) = \gamma \odot \frac{h - \mu}{\sigma} + \beta", colors=colors, font_size=32)
        ln.next_to(names, DOWN, buff=0.5).align_to(names, LEFT)
        lnl = label(r"rescale each vector to a standard size", font_size=22, color=GREY_A).next_to(ln, DOWN, buff=0.12)
        lnl.align_to(names, LEFT)
        with self.voiceover(
            "Here it is on the spirals, with forty layers. The plain stack never learns anything: it's stuck at a "
            "coin flip. <bookmark mark='a'/> The same forty layers with residual connections learn the spirals "
            "completely, within a few hundred steps. <bookmark mark='b'/> Add layer normalization, which rescales "
            "each layer's vector to a standard size, and training is steadier still. Residual streams and "
            "normalization: the two pieces of plumbing inside every modern model."
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(yn))
            self.play(Create(cp), FadeIn(names[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(cr), FadeIn(names[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(cn), FadeIn(names[2]), Write(ln), FadeIn(lnl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
