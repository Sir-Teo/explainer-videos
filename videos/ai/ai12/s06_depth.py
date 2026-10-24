from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import DEPTH_COLORS, HIST, MUP, PART, SP, band, load, table_card

ALPHA_COL = {0.0: SP, 0.5: C.BITS, 1.0: MUP}
SPOKEN = {0.0: "no scaling at all", 0.5: "one over root L", 1.0: "CompleteP"}
ALPHA_NAME = {0.0: r"no depth scaling", 0.5: r"depth-$\mu$P \ ($1/\sqrt{L}$)", 1.0: r"CompleteP \ ($1/L$)"}


class Depth(VoiceoverScene):
    def construct(self):
        self.card()
        self.stream()
        self.sweeps()
        self.payoff()

    def card(self):
        card = chapter_card(5, r"Deeper and deeper", r"And when the network gets deeper, not wider?", part=PART)
        with self.voiceover("Chapter five. Deeper and deeper."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def stream(self):
        # the residual stream as a column the blocks add into (schematic)
        L = 8
        blocks = VGroup(*[RoundedRectangle(width=1.5, height=0.36, corner_radius=0.06, stroke_color=C.CONTEXT,
                                           stroke_width=2, fill_color=C.CONTEXT, fill_opacity=0.15) for _ in range(L)])
        blocks.arrange(UP, buff=0.14).move_to([-4.6, -0.4, 0])
        spine = Line(blocks.get_bottom() + DOWN * 0.35 + RIGHT * 1.3, blocks.get_top() + UP * 0.35 + RIGHT * 1.3,
                     color=WHITE, stroke_width=3)
        arrows = VGroup(*[Arrow(b.get_right(), [spine.get_x(), b.get_y(), 0], buff=0.05, stroke_width=2.5, color=C.CONTEXT,
                                max_tip_length_to_length_ratio=0.35) for b in blocks])
        tags = VGroup(*[MathTex(r"\times L^{-\alpha}", font_size=18, color=C.BITS).next_to(a, UP, buff=0.0) for a in arrows[::3]])
        sl = label(r"the residual stream", font_size=20, color=GREY_A).next_to(spine, UP, buff=0.1)
        sch = note(r"schematic").next_to(blocks, DOWN, buff=0.45)
        eq = cmath(r"h_{\ell}", r"=", r"h_{\ell-1}", r"+", r"L^{-\alpha}", r"\, f_\ell(h_{\ell-1})", font_size=40,
                   colors={r"L^{-\alpha}": C.BITS}).move_to([2.6, 2.4, 0])
        tab = table_card([
            [r"", r"branch", r"block learning rate", r"each block, as $L \to \infty$"],
            [r"$\alpha = 0$", r"$1$", r"$\eta$", r"the stream grows; \ the best rate drifts"],
            [r"$\alpha = \tfrac12$ \ depth-$\mu$P", r"$1/\sqrt{L}$", r"$\eta/\sqrt{L}$", r"tends to linear: \ lazy in depth"],
            [r"$\alpha = 1$ \ CompleteP", r"$1/L$", r"$\eta$", r"stays nonlinear: \ learns features"],
        ], col_colors=[GREY_A, C.BITS, C.BITS, GREY_A], font_size=20)
        for r_, a in zip(tab[0][1:], (0.0, 0.5, 1.0)):
            r_[0].set_color(ALPHA_COL[a])
        tab.move_to([2.6, 0.2, 0])
        cites = cite(r"G.~Yang, D.~Yu, C.~Zhu \& S.~Hayou (2023); \ B.~Bordelon et al.\ (2023); \ N.~Dey et al.\ "
                     r"(2025), Table 1", corner=DR)
        with self.voiceover(
            "Depth is the other way to grow. A residual network adds each block's output to a running sum, the "
            "residual stream of part nine. <bookmark mark='a'/> With L blocks, the stream is a sum of L branches, "
            "and how each is scaled decides what happens as L grows. <bookmark mark='b'/> Leave them alone, and the "
            "stream grows with depth, and the best learning rate drifts. <bookmark mark='c'/> In 2023, two groups "
            "found the depth version of mu-P: scale each branch by one over the square root of L, with the learning "
            "rate to match. It transfers across depth, but each block's contribution becomes so small that it acts "
            "linearly: lazy, now in depth. <bookmark mark='d'/> In 2025, Nolan Dey and colleagues at Cerebras showed "
            "that one over L, with the learning rate left alone, keeps every block learning features. They called "
            "it CompleteP."
        ) as vo:
            self.play(FadeIn(blocks), Create(spine), FadeIn(sl), FadeIn(sch), Write(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), FadeIn(tags), FadeIn(cites))
            self.play(FadeIn(tab[1]), FadeIn(tab[0][0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[0][1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[0][2]))
            vo.wait_until("d")
            self.play(FadeIn(tab[0][3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweeps(self):
        d = load("depth")
        lrs = np.log10(np.asarray(d["lrs"]))
        depths = [int(v) for v in d["depths"]]
        alphas = [float(a) for a in d["alphas"]]
        allv = np.concatenate([np.asarray(d[f"a{a}_d{k}"]).ravel() for a in alphas for k in depths])
        allv = allv[np.isfinite(allv)]
        lo = float(np.floor(allv.min() * 10) / 10)
        hi = float(min(np.ceil(np.percentile(allv, 75) * 10) / 10, lo + 1.2))
        panels = VGroup()
        for k, a in enumerate(alphas):
            ax = CornerAxes(x_range=[lrs[0], lrs[-1], 0.5], y_range=[lo, hi, 0.2], x_length=3.9, y_length=3.4, tips=False,
                            axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
            ax.move_to([-4.55 + 4.55 * k, -0.85, 0])
            lines, bests = VGroup(), VGroup()
            for dd, col in zip(depths, DEPTH_COLORS):
                v = np.asarray(d[f"a{a}_d{dd}"])
                v = np.where(np.isfinite(v), np.minimum(v, hi), hi).mean(0)
                lines.add(curve(ax, lrs, v, col, 2.8))
                i = int(np.argmin(v))
                bests.add(Dot(ax.c2p(lrs[i], v[i]), radius=0.08, color=col))
            xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=18, color=GREY_B).next_to(ax.c2p(v, lo), DOWN, buff=0.08)
                          for v in range(math.ceil(lrs[0]), math.floor(lrs[-1]) + 1)])
            t = label(ALPHA_NAME[a], font_size=24, color=ALPHA_COL[a]).next_to(ax, UP, buff=0.15)
            dr = label(rf"best rate moves ${d['drift'][str(a)]:.1f}$ decades", font_size=19, color=ALPHA_COL[a])
            dr.next_to(xt, DOWN, buff=0.12)
            yt = VGroup(*[MathTex(f"{v:.1f}", font_size=18, color=GREY_B).next_to(ax.c2p(lrs[0], v), LEFT, buff=0.06)
                          for v in np.arange(lo, hi + 1e-9, 0.2)]) if k == 0 else VGroup()
            panels.add(VGroup(ax, xt, t, yt, lines, bests, dr))
        key = VGroup(label(r"depth", font_size=22, color=GREY_A),
                     *[label(str(v), font_size=22, color=c) for v, c in zip(depths, DEPTH_COLORS)]).arrange(RIGHT, buff=0.4)
        key.to_edge(UP, buff=0.3)
        yn = label(rf"held-out bits after ${int(d['steps'])}$ steps, \ against the learning rate \ (mean of two seeds; "
                   rf"width ${int(d['width'])}$)", font_size=20, color=GREY_A).next_to(key, DOWN, buff=0.12)
        dr = {float(k): v for k, v in d["drift"].items()}
        order = sorted(alphas, key=lambda a: dr[a])
        best_a = order[0]
        said1 = (
            "CompleteP holds the learning rate most still, as it was designed to."
            if best_a == 1.0 else
            f"Here the steadiest is {SPOKEN[best_a]}: at our small depths and short runs, the differences are "
            "about a grid step."
        )
        with self.voiceover(
            f"Our character model again, made deep: {', '.join(str(v) for v in depths[:-1])} and {depths[-1]} "
            "residual blocks, each parametrization swept over nine learning rates, two seeds each. "
            "<bookmark mark='a'/> With no depth scaling, "
            f"the best rate moves by {dr[0.0]:.1f} powers of ten between the shallowest and the deepest. "
            f"<bookmark mark='b'/> With one over root L, {dr[0.5]:.1f}. <bookmark mark='c'/> With CompleteP's "
            f"one over L, {dr[1.0]:.1f}. "
            + said1
        ) as vo:
            self.play(FadeIn(key), FadeIn(yn), *[FadeIn(p[:4]) for p in panels])
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                p = panels[k]
                self.play(LaggedStart(*[Create(l_) for l_ in p[4]], lag_ratio=0.15), run_time=1.6)
                self.play(FadeIn(p[5]), FadeIn(p[6]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoff(self):
        d = load("depth")
        depths = [int(v) for v in d["depths"]]
        alphas = [float(a) for a in d["alphas"]]
        bl = {float(k): v for k, v in d["best_loss"].items()}
        cp = {float(k): v for k, v in d["copy_loss"].items()}
        allv = np.array([v for a in alphas for v in bl[a]] + [cp[a] for a in alphas])
        lo, hi = float(np.floor(allv.min() * 20) / 20 - 0.05), float(np.ceil(allv.max() * 20) / 20 + 0.05)
        ld = np.log2(depths)
        ax = CornerAxes(x_range=[ld[0] - 0.3, ld[-1] + 0.3, 1], y_range=[lo, hi, (hi - lo) / 4], x_length=5.4, y_length=3.6,
                        tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
        ax.move_to([-3.4, -0.4, 0])
        xt = VGroup(*[MathTex(str(v), font_size=20, color=GREY_B).next_to(ax.c2p(math.log2(v), lo), DOWN, buff=0.08) for v in depths])
        yt = VGroup(*[MathTex(f"{v:.2f}", font_size=20, color=GREY_B).next_to(ax.c2p(ld[0] - 0.3, v), LEFT, buff=0.08)
                      for v in np.linspace(lo, hi, 5)])
        xn = label(r"depth \ (blocks)", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"best held-out bits at each depth", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        lines = VGroup(*[VGroup(curve(ax, ld, bl[a], ALPHA_COL[a], 3), *[Dot(ax.c2p(x, y), radius=0.06, color=ALPHA_COL[a])
                                                                      for x, y in zip(ld, bl[a])]) for a in alphas])
        lg = VGroup(*[label(ALPHA_NAME[a], font_size=20, color=ALPHA_COL[a]) for a in alphas]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lg.next_to(ax, RIGHT, buff=0.2).align_to(ax, UP)
        copies = VGroup(*[label(rf"depth ${depths[-1]}$ at depth ${depths[0]}$'s best rate: \ ${cp[a]:.2f}$ \ "
                                rf"(own best ${bl[a][-1]:.2f}$)", font_size=20, color=ALPHA_COL[a]) for a in alphas])
        copies.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.3, -1.3, 0])
        keep_in_frame(copies)
        hc = history_card(2025, r"Dey et al., \ \textit{Don't be lazy} (Cerebras)",
                          r"CompleteP: \ $12\%$ less compute than $\mu$P at $1.5$ billion parameters, \ $34\%$ for the "
                          r"deepest models; \ deep, narrow shapes become efficient", width=5.6, color=HIST)
        hc.scale(0.9).move_to([3.4, 2.0, 0])
        deeper = bl[1.0][-1] < bl[1.0][0]
        said2 = (
            f"With CompleteP, yes: {bl[1.0][0]:.2f} bits at {depths[0]} blocks, {bl[1.0][-1]:.2f} at {depths[-1]}, "
            "each at its own best rate. " if deeper else
            f"In our short runs, barely: {bl[1.0][0]:.2f} bits at {depths[0]} blocks, {bl[1.0][-1]:.2f} at "
            f"{depths[-1]}. "
        )
        with self.voiceover(
            "Two practical questions. Does depth pay? "
            + said2
            + "<bookmark mark='a'/> And what does it cost to tune the shallow model and copy its rate to the deep "
            f"one? {cp[0.0]:.2f} bits with no depth scaling, {cp[0.5]:.2f} with one over root L, {cp[1.0]:.2f} with "
            "CompleteP. <bookmark mark='b'/> At scale, Dey and colleagues measured twelve percent less compute than "
            "mu-P for the same loss at one and a half billion parameters, and thirty-four percent for their deepest "
            "models. Part nine's careful initialization made ten-thousand-layer networks trainable; this is the "
            "same idea, for training them well."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(lg))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in copies], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
