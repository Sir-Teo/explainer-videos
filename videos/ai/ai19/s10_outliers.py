from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (ERRC, F, LEVELC, PART, RTNC, SMOOTHC, WEIGHTC, hbars, load, times)

KEEPC = C.HOT
COLORS = {r"X": C.TOKEN, r"W": WEIGHTC, r"s": SMOOTHC, r"\alpha": SMOOTHC}


class Outliers(VoiceoverScene):
    def construct(self):
        self.card()
        self.profile()
        self.smooth()
        self.results()

    def card(self):
        card = chapter_card(9, r"Outliers and SmoothQuant", r"Why are activations harder to round than weights?",
                            part=PART)
        with self.voiceover("Chapter nine. Outliers and SmoothQuant."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def profile(self):
        o = load("outliers")
        prof = np.asarray(o["profile"])
        n = len(prof)
        W, Hh = 9.6, 2.6
        x0 = -W / 2 - 1.0
        bars = VGroup(*[Rectangle(width=W / n, height=max(Hh * v / prof.max(), 0.005), stroke_width=0,
                                  fill_color=ERRC if v > 3 * np.median(prof) else C.TOKEN,
                                  fill_opacity=0.85).move_to([x0 + W * (i + 0.5) / n, -1.4 + Hh * v / prof.max() / 2, 0])
                        for i, v in enumerate(prof)])
        base = Line([x0, -1.4, 0], [x0 + W, -1.4, 0], color=GREY_C, stroke_width=1.5)
        med = float(np.median(prof))
        ml = DashedLine([x0, -1.4 + Hh * med / prof.max(), 0], [x0 + W, -1.4 + Hh * med / prof.max(), 0],
                        color=GREY_B, dash_length=0.06)
        mll = label(r"median", font_size=18, color=GREY_B).next_to([x0 + W, -1.4 + Hh * med / prof.max(), 0], RIGHT,
                                                                  buff=0.1)
        head = label(rf"the largest input to each channel of one layer \ (\texttt{{{o['worst']}}}, ${n}$ channels)",
                     font_size=22, color=GREY_A).to_edge(UP, buff=0.4)
        ratio = float(o["ratio"][o["worst"]])
        rl = label(rf"largest $\div$ median: \ ${ratio:.1f}$", font_size=24, color=ERRC).move_to([4.6, 1.2, 0])
        resid = np.asarray(o["resid"]).max(1)
        rr = label(rf"between the blocks, \ the largest activation grows \\ from ${resid[0]:.0f}$ to "
                   rf"${resid[-1]:.0f}$, \ layer by layer", font_size=20, color=GREY_A).next_to(rl, DOWN, buff=0.3)
        hc = history_card(2022, r"Tim Dettmers et al., \ LLM.int8()", rf"from about ${F.LLM_INT8['scale'] / 1e9:.1f}$B "
                          rf"parameters, \ a few feature dimensions (about ${F.LLM_INT8['share']}\%$) hold values up to "
                          rf"${F.LLM_INT8['mag']}\times$ the rest", width=5.0, font_size=17, color=ERRC)
        hc.to_corner(UL, buff=0.25).shift(DOWN * 0.6)
        with self.voiceover(
            "Weights are only half of a matrix product. To use eight-bit or four-bit arithmetic, the inputs, the "
            "activations, have to be rounded too, every token, on the fly. <bookmark mark='a'/> In 2022 Tim "
            "Dettmers and colleagues found what makes that hard. From about six point seven billion parameters "
            "on, a few feature dimensions, around a tenth of a percent of them, carry values up to twenty times "
            "larger than the rest, in every layer. <bookmark mark='b'/> Our model is far smaller, but the effect "
            "is already there. These are the largest inputs each channel of one layer saw, on calibration text. "
            f"The largest is {ratio:.1f} times the median. <bookmark mark='c'/> Round a token's activations with "
            "one scale, and those few channels set the step for all the others, which then get only a handful of "
            "levels."
        ) as vo:
            self.play(FadeIn(head), Create(base))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(hc), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.002), run_time=2.0)
            self.play(Create(ml), FadeIn(mll), FadeIn(rl), FadeIn(rr))
            vo.wait_until("c")
            big = [i for i, v in enumerate(prof) if v > 3 * np.median(prof)][:12]
            if big:
                self.play(*[Indicate(bars[i], color=ERRC) for i in big])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def smooth(self):
        o = load("outliers")
        a0, a1 = np.asarray(o["sq_act_before"]), np.asarray(o["sq_act_after"])
        w0, w1 = np.asarray(o["sq_w_before"]), np.asarray(o["sq_w_after"])
        rows = [
            cmath(r"Y", r"=", r"X W^\top", colors=COLORS, font_size=38),
            cmath(r"Y", r"=", r"\big(X\,\mathrm{diag}(s)^{-1}\big)\,\big(W\,\mathrm{diag}(s)\big)^\top", colors=COLORS,
                  font_size=38),
            cmath(r"s_j", r"=", r"\frac{\max|X_j|^{\alpha}}{\max|W_j|^{1-\alpha}}", colors=COLORS, font_size=38),
            cmath(r"\alpha = \tfrac12", r":\;", r"\max|X_j / s_j| = \max|W_j s_j| = \sqrt{\max|X_j| \max|W_j|}",
                  colors=COLORS, font_size=34),
        ]
        whys = [why(r"a linear layer"), why(r"the same product: \ $s$ cancels"), why(r"move the range from $X$ to $W$"),
                why(r"both sides share channel $j$'s range")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-1.2, buff=0.36, edge=6.8)
        n = 96

        def strip(v, col, y, lab):
            v = np.asarray(v)[:n]
            top = max(a0[:n].max(), w0[:n].max(), a1[:n].max(), w1[:n].max())
            g = VGroup(*[Rectangle(width=10.0 / n * 0.85, height=max(0.9 * x / top, 0.004), stroke_width=0, fill_color=col,
                                   fill_opacity=0.85).move_to([-5.0 + 10.0 * (i + 0.5) / n, y + 0.45 * x / top, 0])
                         for i, x in enumerate(v)])
            t = label(lab, font_size=18, color=col).next_to([-5.0, y + 0.95, 0], RIGHT, buff=0.0)
            return VGroup(g, t)

        sa0, sw0 = strip(a0, C.TOKEN, -1.55, r"activations: \ max per channel"), strip(w0, WEIGHTC, -2.95, r"weights")
        sa1, sw1 = strip(a1, SMOOTHC, -1.55, r"activations $\div\, s$"), strip(w1, SMOOTHC, -2.95, r"weights $\times\, s$")
        hc = history_card(2022, r"Guangxuan Xiao et al., \ SmoothQuant", rf"eight-bit weights and activations, \ "
                          rf"${F.SMOOTHQUANT['speed']}\times$ faster, \ models up to "
                          rf"${F.SMOOTHQUANT['params'] / 1e9:.0f}$B", width=4.0, font_size=16,
                          color=SMOOTHC).to_corner(UR, buff=0.2).shift(DOWN * 1.3)
        sa = float(a0.max() / np.median(a0))
        sb = float(a1.max() / np.median(a1))
        with self.voiceover(
            "SmoothQuant, from Guangxuan Xiao and colleagues at MIT and NVIDIA in 2022, moves the problem. "
            "<bookmark mark='a'/> A linear layer multiplies X by W. <bookmark mark='b'/> Divide channel j of the "
            "activations by a number s j, and multiply the same channel of the weights by it: the product is "
            "unchanged, and the division can be folded into the layer before, so it costs nothing at run time. "
            "<bookmark mark='c'/> Choose s j as the activation's range to the power alpha, over the weight's to "
            "the power one minus alpha. <bookmark mark='d'/> With alpha a half, both sides end up with the same "
            "range, the geometric mean of the two. The activations' outliers are smoothed into weights, which are "
            f"rounded offline and can take it: on our layer, the largest activation goes from {sa:.1f} times the "
            f"median to {sb:.1f}."
        ) as vo:
            step(0)
            self.play(FadeIn(sa0), FadeIn(sw0))
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(hc))
            vo.wait_until("d")
            step(3)
            self.play(ReplacementTransform(sa0, sa1), ReplacementTransform(sw0, sw1), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        o = load("outliers")
        base = float(o["fp32"])
        L = o["loss"]
        groups = []
        for ab in (8, 6, 4):
            vals = [L[f"w8a{ab}_{m}"] - base for m in ("plain", "smooth", "keep")]
            groups.append((ab, vals))
        hi = max(max(v) for _, v in groups) * 1.1
        g = VGroup()
        for ab, vals in groups:
            g.add(VGroup(label(rf"$8$-bit weights, \ ${ab}$-bit activations", font_size=20, color=GREY_A),
                         hbars(vals, [r"plain rounding", r"SmoothQuant", r"$1\%$ of channels kept aside"],
                               [RTNC, SMOOTHC, KEEPC], width=3.4, row_h=0.36, font_size=18, lo=0, hi=hi,
                               fmt_v=lambda v: rf"{v:+.3f}")).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0.6, -0.3, 0])
        head = label(r"extra loss on held-out novels \ (nats per token), \ every block input rounded per token",
                     font_size=22, color=GREY_A).to_edge(UP, buff=0.35)
        d8 = max(abs(v) for v in groups[0][1])
        p4, s4, k4 = groups[2][1]
        if s4 < 0.9 * p4:
            s_say = f"SmoothQuant cuts the loss to {s4:.3f}"
        else:
            s_say = f"SmoothQuant helps only a little, {s4:.3f}"
        with self.voiceover(
            "What does it buy on our model? <bookmark mark='a'/> At eight bits, nothing is needed: every method "
            f"stays within {d8:.4f} nats of the full model. <bookmark mark='b'/> At six bits the costs appear. "
            f"<bookmark mark='c'/> At four, plain rounding of every block input costs {p4:.3f} nats a token; "
            + s_say + f"; and keeping the largest one percent of channels in full precision, as LLM.int8() does with "
            f"its outliers, {k4:.3f}. <bookmark mark='d'/> Our outliers are mild, {o['ratio'][o['worst']]:.0f} times "
            "the median rather than twenty, so there is less to smooth. Four-bit activations need something "
            "stronger: the next chapter but one."
        ) as vo:
            self.play(FadeIn(head))
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(g[i]))
            vo.wait_until("d")
            self.play(Indicate(g[2], color=SMOOTHC, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()
