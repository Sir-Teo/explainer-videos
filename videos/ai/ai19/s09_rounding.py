from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (ERRC, LEVELC, PART, WEIGHTC, load, take_away, x_)

COLORS = {r"\Delta": LEVELC, r"e": ERRC, r"w": WEIGHTC, r"b": GREY_A}


class Rounding(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.check()
        self.histogram()
        self.loss()

    def card(self):
        card = chapter_card(8, r"Rounding error", r"What does a number lose when it is stored in fewer bits?",
                            part=PART)
        with self.voiceover("Chapter eight. Rounding error."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        # a number line of levels, a weight, and its error
        nl = NumberLine(x_range=[-3, 3, 1], length=6.0, include_numbers=False, color=GREY_C, tick_size=0.1)
        nl.move_to([-3.4, 1.6, 0])
        lv = VGroup(*[Line(nl.n2p(k) + DOWN * 0.18, nl.n2p(k) + UP * 0.18, color=LEVELC, stroke_width=3)
                      for k in range(-3, 4)])
        dl = BraceBetweenPoints(nl.n2p(1), nl.n2p(2), DOWN, color=LEVELC)
        dlt = MathTex(r"\Delta", font_size=30, color=LEVELC).next_to(dl, DOWN, buff=0.08)
        w = 1.37
        wd = Dot(nl.n2p(w), radius=0.08, color=WEIGHTC)
        wl = MathTex(r"w", font_size=30, color=WEIGHTC).next_to(wd, UP, buff=0.18)
        arr = Arrow(nl.n2p(w) + UP * 0.05, nl.n2p(1) + UP * 0.05, buff=0, color=ERRC, stroke_width=3,
                    max_tip_length_to_length_ratio=0.3)
        el = MathTex(r"e", font_size=28, color=ERRC).next_to(arr, UP, buff=0.05)
        # the error's density: flat on [-Delta/2, Delta/2]
        pdf = VGroup(Line([-5.0, -0.6, 0], [-1.8, -0.6, 0], color=GREY_C, stroke_width=1.5),
                     Rectangle(width=1.6, height=0.8, stroke_color=ERRC, stroke_width=2, fill_color=ERRC,
                               fill_opacity=0.25).move_to([-3.4, -0.2, 0]))
        pl = VGroup(MathTex(r"-\tfrac{\Delta}{2}", font_size=24, color=LEVELC).move_to([-4.2, -0.9, 0]),
                    MathTex(r"\tfrac{\Delta}{2}", font_size=24, color=LEVELC).move_to([-2.6, -0.9, 0]),
                    label(r"the error, \ if spread evenly", font_size=20, color=ERRC).move_to([-3.4, 0.45, 0]))
        rows = [
            cmath(r"\mathbb E[e^2]", r"=", r"\frac{1}{\Delta}\int_{-\Delta/2}^{\Delta/2} e^2\, de", colors=COLORS,
                  font_size=36),
            cmath(r"\mathbb E[e^2]", r"=", r"\frac{1}{\Delta}\cdot\frac{2}{3}\Big(\frac{\Delta}{2}\Big)^3", colors=COLORS,
                  font_size=36),
            cmath(r"\mathbb E[e^2]", r"=", r"\frac{\Delta^2}{12}", colors=COLORS, font_size=36),
            cmath(r"\Delta", r"=", r"\frac{\max|w|}{2^{b-1} - 1}", colors=COLORS, font_size=36),
            cmath(r"\Delta^2 / 12", r"\;\propto\;", r"4^{-b}", colors=COLORS, font_size=36),
        ]
        whys = [why(r"uniform on one step"), why(r"$\int e^2 = e^3/3$"), why(r"the classic result"),
                why(r"$b$ bits, \ symmetric, \ the largest weight sets the step"),
                why(r"each bit halves $\Delta$: \ $6$ dB per bit")]
        step = ladder(self, rows, whys, keep=5, top=3.1, x=2.6, buff=0.32, edge=6.9)
        with self.voiceover(
            "Quantization is the other half of this part: store each number in fewer bits, and move fewer bytes. "
            "<bookmark mark='a'/> The simplest kind rounds every weight to the nearest of a set of evenly spaced "
            "levels, a step delta apart. The error e is at most half a step either way. <bookmark mark='b'/> If "
            "the weights are spread smoothly over many steps, the error is equally likely anywhere in that "
            "interval, and its mean square is the integral of e squared over delta. <bookmark mark='c'/> That "
            "gives delta squared over twelve, which W. R. Bennett of Bell Labs worked out in 1948, for speech and "
            "television sent as numbers. "
            "<bookmark mark='d'/> With b bits, symmetric about zero, the largest weight sets the step: delta is "
            "the maximum over two to the b minus one, minus one. <bookmark mark='e'/> So each bit halves the step "
            "and quarters the error: six decibels a bit, as audio engineers say."
        ) as vo:
            self.play(Create(nl), Create(lv))
            self.play(FadeIn(dl), FadeIn(dlt), FadeIn(wd), FadeIn(wl))
            vo.wait_until("a")
            self.play(GrowArrow(arr), FadeIn(el))
            vo.wait_until("b")
            self.play(FadeIn(pdf), FadeIn(pl))
            step(0)
            vo.wait_until("c")
            step(1)
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        r = load("rounding")
        bits = np.asarray(r["mse_bits"])
        meas, pred = np.asarray(r["mse_row"]), np.asarray(r["pred_row"])
        mt, pt_ = np.asarray(r["mse_tensor"]), np.asarray(r["pred_tensor"])
        lo = math.floor(math.log10(min(meas.min(), pred.min()))) - 0.2
        hi = math.ceil(math.log10(max(mt.max(), pt_.max()))) + 0.1
        g = axes([1.5, 8.5], [lo, hi], x_length=6.4, y_length=4.2, xlabel=r"bits per weight, \ $b$",
                 ylabel=r"mean squared rounding error", xticks=list(range(2, 9)),
                 yticks=list(range(int(math.ceil(lo)), int(hi) + 1, 2)), yfmt=lambda v: rf"10^{{{int(v)}}}",
                 center=[-2.4, -0.3, 0])
        ax = g.ax
        line_r = curve(ax, bits, np.log10(pred), LEVELC, 3)
        line_t = curve(ax, bits, np.log10(pt_), GREY_B, 2)
        dots_r = VGroup(*[Dot(ax.c2p(b, math.log10(v)), radius=0.08, color=ERRC) for b, v in zip(bits, meas)])
        dots_t = VGroup(*[Dot(ax.c2p(b, math.log10(v)), radius=0.06, color=GREY_A) for b, v in zip(bits, mt)])
        key = VGroup(label(r"line: \ $\Delta^2/12$, \ predicted", font_size=20, color=LEVELC),
                     label(r"dots: \ measured, \ a scale per row", font_size=20, color=ERRC),
                     label(r"grey: \ one scale for a whole matrix", font_size=20, color=GREY_A))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, 1.6, 0])
        ratio = meas / pred
        ok = int(np.argmax(np.abs(ratio - 1) < 0.05))
        notes = VGroup(label(rf"measured $\div$ predicted, \ ${bits[ok]}$ bits and up: \ "
                             rf"${ratio[ok:].min():.3f}$--${ratio[ok:].max():.3f}$", font_size=20, color=ERRC),
                       label(rf"at $2$ bits: \ ${ratio[0]:.2f}$", font_size=20, color=ERRC))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.2, -0.5, 0])
        tag = note(rf"computed: \ all ${r['n_weights'] / 1e6:.1f}$ million weights of the novels model's $30$ block "
                   r"matrices").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Does it hold for a real model? <bookmark mark='a'/> We rounded all the block weights of the novels "
            "model, with a scale for each row of each matrix, at two to eight bits, and measured the mean squared "
            f"error. <bookmark mark='b'/> From {bits[ok]} bits up, the measurement and delta squared over twelve "
            f"agree to within {100 * max(abs(ratio[ok:] - 1)):.1f} percent: the lines are straight, a factor of four "
            "a bit. <bookmark mark='c'/> At two bits the formula overestimates: most weights now fall inside the "
            "zero step, and their error is just their own small size, not spread over a whole step. "
            "<bookmark mark='d'/> The grey dots used one scale for a whole matrix: every error is larger, because "
            "one large weight anywhere sets the step for all the others."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(line_r), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots_r], lag_ratio=0.1), FadeIn(key[1]),
                      FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(Indicate(dots_r[0], color=ERRC, scale_factor=1.8), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(Create(line_t), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots_t], lag_ratio=0.1),
                      FadeIn(key[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def histogram(self):
        r = load("rounding")
        h, e = np.asarray(r["hist"], float), np.asarray(r["hist_edges"])
        amax = float(r["hist_amax"])
        rows_amax = np.asarray(r["row_amax"])
        W, Hh = 10.0, 2.6
        x0 = -W / 2

        def X(v):
            return x0 + (v - e[0]) / (e[-1] - e[0]) * W

        bars = VGroup(*[Rectangle(width=W / len(h) * 0.9, height=max(Hh * v / h.max(), 0.005), stroke_width=0,
                                  fill_color=WEIGHTC, fill_opacity=0.75)
                        .move_to([X((e[i] + e[i + 1]) / 2), -1.6 + Hh * v / h.max() / 2, 0]) for i, v in enumerate(h)])
        base = Line([x0, -1.6, 0], [x0 + W, -1.6, 0], color=GREY_C, stroke_width=1.5)
        lvl_t = VGroup(*[Line([X(k * amax / 7), -1.6, 0], [X(k * amax / 7), 1.2, 0], color=LEVELC, stroke_width=1.5)
                         for k in range(-8, 8) if e[0] <= k * amax / 7 <= e[-1]])
        med = float(np.median(rows_amax))
        lvl_r = VGroup(*[Line([X(k * med / 7), -1.6, 0], [X(k * med / 7), 1.2, 0], color=C.PROB, stroke_width=1.5)
                         for k in range(-8, 8) if e[0] <= k * med / 7 <= e[-1]])
        head = label(rf"the weights of one matrix of the novels model \ (\texttt{{{r['hist_layer']}}})",
                     font_size=22, color=GREY_A).to_edge(UP, buff=0.4)
        lt = label(r"$4$ bits, \ one scale for the matrix: \ its largest weight sets the step", font_size=22,
                   color=LEVELC).next_to(head, DOWN, buff=0.25)
        lr = label(r"$4$ bits, \ a scale per row: \ a typical row's step", font_size=22, color=C.PROB).next_to(head, DOWN,
                                                                                                     buff=0.25)
        ratio = amax / med
        with self.voiceover(
            "Here is why the scale's reach matters. <bookmark mark='a'/> These are the weights of one matrix of our "
            "model: most within a narrow band around zero. <bookmark mark='b'/> With one four-bit scale for the "
            "whole matrix, its single largest weight sets the step, and most weights share a handful of levels "
            f"near zero. <bookmark mark='c'/> A typical row's largest weight is {x_(ratio)} times smaller than the "
            "matrix's, so a scale per row puts the levels where that row's weights are. A scale per group of 32 "
            "or 64 weights goes further, for a few more bits of storage per group."
        ) as vo:
            self.play(FadeIn(head), Create(base))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lvl_t), FadeIn(lt))
            vo.wait_until("c")
            self.play(ReplacementTransform(lvl_t, lvl_r), ReplacementTransform(lt, lr))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loss(self):
        r = load("rounding")
        bits = np.asarray(r["bits"], float)
        base = float(r["fp32"])
        series = [("tensor", r"one scale per matrix", GREY_B), ("row", r"per row", C.PROB),
                  ("64", r"per group of $64$", C.EMBED), ("32", r"per group of $32$", LEVELC)]
        cap = base + 0.6
        g = axes([1.6, 8.4], [base - 0.02, cap], x_length=6.6, y_length=4.2, xlabel=r"bits per weight",
                 ylabel=r"held-out loss \ (nats per token)", xticks=[2, 3, 4, 5, 6, 8],
                 yticks=[round(base, 2), round(base + 0.25, 2), round(base + 0.5, 2)], yfmt=lambda v: f"{v:.2f}",
                 center=[-2.4, -0.3, 0])
        ax = g.ax
        bl = DashedLine(ax.c2p(1.6, base), ax.c2p(8.4, base), color=WHITE, dash_length=0.06)
        bll = label(rf"$32$-bit: \ ${base:.3f}$", font_size=20, color=WHITE).next_to(ax.c2p(8.4, base), UP, buff=0.08,
                                                                                    aligned_edge=RIGHT)
        lines, dots, offs = VGroup(), VGroup(), VGroup()
        for key, nm, col in series:
            y = np.minimum(np.asarray(r["loss"][key]), cap)
            lines.add(curve(ax, bits, y, col, 3))
            dots.add(VGroup(*[Dot(ax.c2p(b, v), radius=0.06, color=col) for b, v in zip(bits, y)]))
            if r["loss"][key][0] > cap:
                offs.add(label(rf"${r['loss'][key][0]:.1f}$", font_size=16, color=col))
        leg = legend([(c_, t) for _, t, c_ in series], font_size=20).move_to([4.4, 1.4, 0])
        L = {k: np.asarray(r["loss"][k]) - base for k, _, _ in series}
        i4, i3, i8 = list(bits).index(4), list(bits).index(3), list(bits).index(8)
        bpw = r["bpw"]
        notes = VGroup(label(rf"$8$ bits, \ per row: \ ${L['row'][i8]:+.4f}$", font_size=20, color=C.PROB),
                       label(rf"$4$ bits: \ ${L['tensor'][i4]:+.3f}$ \ $\to$ \ ${L['32'][i4]:+.3f}$ per $32$", font_size=20,
                             color=LEVELC),
                       label(rf"$3$ bits, \ per row: \ ${L['row'][i3]:+.3f}$", font_size=20, color=C.PROB),
                       label(rf"$2$ bits, \ per row: \ ${r['loss']['row'][0]:.1f}$ nats: \ broken", font_size=20,
                             color=ERRC))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.4, -1.2, 0])
        free8 = abs(L["row"][i8]) < 0.002
        say8 = ("At eight bits, nothing measurable is lost." if free8 else
                f"At eight bits, the loss grows by {L['row'][i8]:.4f} nats.")
        with self.voiceover(
            "What the model loses: its loss on held-out novels, at each width and each kind of scale. "
            "<bookmark mark='a'/> " + say8 + " "
            f"<bookmark mark='b'/> At four bits it depends on the scales: one per matrix costs {L['tensor'][i4]:.3f} "
            f"nats per token, one per row {L['row'][i4]:.3f}, one per 32 weights {L['32'][i4]:.3f}, for "
            f"{bpw['32'][i4]:.1f} bits a weight in all. <bookmark mark='c'/> At three bits plain rounding starts "
            f"to hurt, {L['row'][i3]:.2f} nats with a scale per row, and at two the model is broken. "
            "<bookmark mark='d'/> Everything that follows is about doing better than plain rounding at three and "
            "four bits."
        ) as vo:
            self.play(FadeIn(g), Create(bl), FadeIn(bll))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2), FadeIn(dots), FadeIn(leg),
                      FadeIn(notes[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2:]))
            vo.wait_until("d")
            self.play(Indicate(notes[1], color=LEVELC))
        self.wait(0.3)
        self.clear_scene()
