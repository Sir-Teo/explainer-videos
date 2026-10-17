from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import curve, load, log_axes


class Hook(VoiceoverScene):
    def construct(self):
        self.law()
        self.plan()

    # ------------------------------------------------------------------
    def law(self):
        s = load("scaling")
        N, L = np.asarray(s["params"], float), np.asarray(s["finals"])
        E, alpha, A = float(s["E"]), float(s["alpha"]), float(s["A"])
        lx = np.log10(N)
        x0, x1 = math.floor(lx.min()), math.ceil(lx.max())
        lo, hi = math.floor((L.min() - 0.2) * 2) / 2, math.ceil((L.max() + 0.1) * 2) / 2
        ax, labs = log_axes((x0, x1), (lo, hi), center=[-1.4, -0.5, 0],
                            x_ticks=[(rf"10^{{{k}}}", k) for k in range(x0, x1 + 1)],
                            y_ticks=list(np.arange(lo, hi + 1e-9, 0.5)))
        xn = label(r"parameters", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        yn = label(r"bits per character on held-out text", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.08, color=C.BITS) for x, y in zip(lx, L)])
        xs = np.linspace(x0, x1, 120)
        fit = curve(ax, xs, np.clip(E + A * (10 ** xs) ** (-alpha), lo, hi), WHITE, 3, smooth=True)
        floor = DashedLine(ax.c2p(x0, E), ax.c2p(x1, E), color=GREY_B, stroke_width=2)
        colors = {r"N": C.BITS, r"\alpha": C.MODEL_Q}
        f = cmath(r"L(N)", "=", r"E", "+", r"A", r"\,N^{-", r"\alpha", r"}", colors=colors, font_size=42).move_to([4.6, 2.0, 0])
        fl = label(rf"$\alpha = {alpha:.2f}$, \ $E = {E:.2f}$", font_size=28, color=C.MODEL_Q).next_to(f, DOWN, buff=0.3)
        nl = label(r"every $10\times$ in size: \\ the reducible loss shrinks \\ by the same factor", font_size=26, color=GREY_A)
        nl.next_to(fl, DOWN, buff=0.5)
        tag = label(r"seven widths of Part 9's character model", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Make a model bigger, and it gets better. That much everyone expected. The surprise was how "
            "predictably. <bookmark mark='a'/> Here are seven sizes of part nine's character model, each trained "
            "the same way. <bookmark mark='b'/> The loss falls along a smooth curve: a power law, plus a floor that "
            "no model can go below. Every tenfold increase in size cuts what's left above the floor by the same "
            "factor. Curves like this, measured on small models, are how laboratories decide what to build next."
        ) as vo:
            self.play(Create(ax), FadeIn(labs), FadeIn(xn), FadeIn(yn), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.15), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(fit), Create(floor), Write(f), run_time=2.0)
            self.play(FadeIn(fl), FadeIn(nl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 10: \ The Mathematics of Scale", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"lazy networks, \ muP, \ scaling laws, \ Chinchilla, \ grokking", font_size=30, color=C.BITS)
        sub.next_to(title, DOWN, buff=0.25)
        smap = series_map(current=10, done=9).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "This part is about what happens as networks grow: why very wide networks stop learning features, how to "
            "set a learning rate once and keep it as the model grows, how to split a budget between size and data, "
            "<bookmark mark='a'/> and a strange delay between memorizing and understanding."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
