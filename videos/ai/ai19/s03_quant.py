from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.compute import FP4, load

MODE_NAMES = {"fp32": r"32-bit floats", "int8": r"8 bits", "int4": r"4 bits", "int3": r"3 bits", "fp4": r"FP4, \ scaled per $32$"}
MODE_COLORS = {"fp32": GREY_B, "int8": C.TRUE_P, "int4": C.INTERVAL, "int3": C.SURPRISE, "fp4": C.BITS}


class Quant(VoiceoverScene):
    def construct(self):
        self.card()
        self.rounding()
        self.results()

    def card(self):
        card = chapter_card(2, r"Fewer bits per number", r"How coarsely can a model's numbers be stored?", part=19)
        with self.voiceover("Chapter two. Fewer bits per number."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def rounding(self):
        q = load("quant")
        h, e = np.asarray(q["hist_w"], float), np.asarray(q["hist_edges"])
        lo, hi = float(e[0]), float(e[-1])
        ax = CornerAxes(x_range=[lo, hi, (hi - lo) / 4], y_range=[0, 1.05, 0.5], x_length=9.0, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(UP * 0.9)
        bars = VGroup(*[Rectangle(width=9.0 / len(h) * 0.9, height=max(2.6 * v / h.max(), 0.005), stroke_width=0, fill_color=GREY_B,
                                  fill_opacity=0.8).move_to(ax.c2p((e[i] + e[i + 1]) / 2, 0) + UP * 1.3 * v / h.max())
                        for i, v in enumerate(h)])
        hl = label(r"the weights of one layer of Part 11's transformer", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12)
        m = max(abs(lo), abs(hi))
        levels4 = np.linspace(-m, m, 15)
        ticks4 = VGroup(*[Line(ax.c2p(x, 0), ax.c2p(x, 1.05), color=C.INTERVAL, stroke_width=1.5).set_stroke(opacity=0.8) for x in levels4])
        t4 = label(r"$4$ bits: \ $16$ evenly spaced values", font_size=24, color=C.INTERVAL).to_edge(LEFT, buff=0.6).shift(DOWN * 1.4)
        s = m / 6
        levelsf = np.concatenate([-FP4[::-1][:-1], FP4]) * s
        ticksf = VGroup(*[Line(ax.c2p(x, 0), ax.c2p(x, 1.05), color=C.BITS, stroke_width=1.5).set_stroke(opacity=0.8) for x in levelsf])
        tf = label(r"FP4: \ $\pm\{0, \tfrac12, 1, \tfrac32, 2, 3, 4, 6\}$ \ times a scale: \\ dense near zero, \ where the weights are",
                   font_size=24, color=C.BITS).next_to(t4, DOWN, buff=0.3).align_to(t4, LEFT)
        with self.voiceover(
            "The other way to cut memory traffic: store each number in fewer bits. Here are the weights of one layer "
            "of our transformer: most near zero, a few larger. <bookmark mark='a'/> With four bits, each weight is "
            "rounded to one of sixteen evenly spaced values. <bookmark mark='b'/> The newest chips use FP4 instead: "
            "a tiny floating-point number, with more values near zero where the weights crowd, and a shared scale "
            "for every block of thirty-two."
        ) as vo:
            self.play(FadeIn(hl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(ticks4), FadeIn(t4))
            vo.wait_until("b")
            self.play(FadeOut(ticks4), Create(ticksf), FadeIn(tf))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        q = load("quant")
        modes = [str(m) for m in q["modes"]]
        vals = [float(q[f"bits_{m}"]) for m in modes]
        base = vals[0]
        lo = base - 0.05
        hi = max(vals) + 0.05
        g = VGroup()
        for i, (m, v) in enumerate(zip(modes, vals)):
            y = 1.8 - i * 0.8
            nm = label(MODE_NAMES[m], font_size=24, color=MODE_COLORS[m]).move_to([-1.6, y, 0], aligned_edge=RIGHT)
            w = (v - lo) / (hi - lo) * 6.0
            bar = Rectangle(width=max(w, 0.02), height=0.42, stroke_width=0, fill_color=MODE_COLORS[m], fill_opacity=0.85)
            bar.move_to([-1.3 + max(w, 0.02) / 2, y, 0])
            val = MathTex(f"{v:.3f}", font_size=26, color=MODE_COLORS[m]).next_to(bar, RIGHT, buff=0.12)
            g.add(VGroup(nm, bar, val))
        head = label(rf"bits per character on the passage \ (axis from ${lo:.2f}$)", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        d8, d4 = vals[modes.index("int8")] - base, vals[modes.index("int4")] - base
        d3, df = vals[modes.index("int3")] - base, vals[modes.index("fp4")] - base
        foot = label(r"real models add tricks: \ GPTQ corrects each rounding error using the next weights; \\ "
                     r"training in low precision from the start (FP8, \ FP4)", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "What does it cost? <bookmark mark='a'/> Rounded to eight bits, our transformer is "
            f"{'no worse' if d8 < 0.005 else f'{d8:.3f} bits worse'}. At four bits, {d4:.3f} bits worse per character, "
            f"for an eighth of the memory; at three, {d3:.2f} worse: it starts to break. "
            + (f"FP4, with its scale for every block of thirty-two, loses only {df:.3f}: better than plain four bits, "
               "for the same memory. " if df < d4 else f"FP4 loses {df:.3f}. ")
            + "<bookmark mark='b'/> Big models tolerate "
            "rounding even better, and methods like GPTQ correct each rounding error using the weights still to come; "
            "the newest models are trained in eight or even four bits from the start."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
