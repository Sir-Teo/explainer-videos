from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import BUDGET_COLORS, curve, load


class Chinchilla(VoiceoverScene):
    def construct(self):
        self.card()
        self.isoflop()
        self.history()

    def card(self):
        card = chapter_card(2, r"Size or data?", r"How should a fixed budget be spent?", part=10, lit=(2020, 2022))
        with self.voiceover("Chapter two. Spending a compute budget."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def isoflop(self):
        d = load("isoflop")
        budgets = [float(b) for b in d["budgets"]]
        allf = np.concatenate([np.asarray(d[f"finals{b:.0e}"]) for b in budgets])
        allf = allf[np.isfinite(allf)]
        lo, hi = float(np.floor(allf.min() * 10) / 10 - 0.05), float(np.ceil(allf.max() * 10) / 10 + 0.05)
        allp = np.concatenate([np.asarray(d[f"params{b:.0e}"]) for b in budgets])
        x0, x1 = math.floor(np.log10(allp.min()) * 2) / 2, math.ceil(np.log10(allp.max()) * 2) / 2
        ax = Axes(x_range=[x0, x1, 0.5], y_range=[lo, hi, 0.1], x_length=7.6, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.8, -0.5, 0])
        xl = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=22, color=GREY_B).next_to(ax.c2p(k, lo), DOWN, buff=0.1)
                      for k in range(math.ceil(x0), math.floor(x1) + 1)])
        yt = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to(ax.c2p(x0, v), LEFT, buff=0.1)
                      for v in np.arange(math.ceil(lo * 5) / 5, hi + 1e-9, 0.2)])
        xn = label(r"parameters", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        yn = label(r"held-out bits per character", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        groups, mins = VGroup(), VGroup()
        for b, col in zip(budgets, BUDGET_COLORS):
            p, f = np.asarray(d[f"params{b:.0e}"], float), np.asarray(d[f"finals{b:.0e}"])
            ok = np.isfinite(f)
            groups.add(VGroup(curve(ax, np.log10(p[ok]), f[ok], col, 3.5),
                              *[Dot(ax.c2p(math.log10(pp), ff), radius=0.06, color=col) for pp, ff in zip(p[ok], f[ok])]))
            i = int(np.nanargmin(f))
            mins.add(Star(n=5, outer_radius=0.13, color=WHITE, fill_opacity=1).move_to(ax.c2p(math.log10(p[i]), f[i])))
        key = VGroup(*[label(rf"budget ${b / 1e12:g}\times10^{{12}}$ operations", font_size=24, color=c)
                       for b, c in zip(budgets, BUDGET_COLORS)])
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.5, 1.6, 0])
        colors = {r"N": C.BITS, r"D": C.TRUE_P}
        rule = cmath(r"C", r"\approx", r"6", r"\,N", r"\,D", colors=colors, font_size=40).next_to(key, DOWN, buff=0.5)
        rl = label(r"$N$ parameters, \ $D$ training tokens", font_size=24, color=GREY_A).next_to(rule, DOWN, buff=0.15)
        best = label(r"too small: \ underfits; \\ too big: \ undertrained", font_size=26, color=GREY_A).next_to(rl, DOWN, buff=0.4)
        with self.voiceover(
            "Suppose you can afford a fixed amount of computation. Training costs about six operations per "
            "parameter per training token, so a budget fixes the product of model size and data. You can have a "
            "big model that sees little data, or a small one that sees a lot. <bookmark mark='a'/> Here's the "
            f"experiment, on our character model. For each budget, try {len(d['widths'])} sizes, each trained on exactly the data "
            "the budget allows. <bookmark mark='b'/> Each budget gives a valley: too small a model can't hold what "
            "it sees; too big a model barely gets to see anything. <bookmark mark='c'/> And the bigger the budget, "
            "the further right the best size moves."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yt), FadeIn(xn), FadeIn(yn), Write(rule), FadeIn(rl))
            vo.wait_until("a")
            self.play(FadeIn(key))
            vo.wait_until("b")
            for g_ in groups:
                self.play(Create(g_), run_time=1.2)
            self.play(FadeIn(best))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s_, scale=0.4) for s_ in mins], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        rows = VGroup(
            label(r"Kaplan et al.\ (2020): \ grow the model faster than the data", font_size=28, color=GREY_A),
            label(r"Hoffmann et al.\ (2022), \textit{Chinchilla}: \ grow both equally, \\ about $20$ tokens per parameter",
                  font_size=28, color=C.BITS),
            label(r"Chinchilla, $70$ billion parameters, beat Gopher, $280$ billion, \\ on the same budget", font_size=26,
                  color=WHITE),
            label(r"today: \ far more tokens than that, \ because a model is \\ trained once and then used billions of times",
                  font_size=26, color=GREY_A))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.2)
        colors = {r"N_{\mathrm{opt}}": C.BITS, r"D_{\mathrm{opt}}": C.TRUE_P}
        f = cmath(r"N_{\mathrm{opt}} \propto C^{0.5}", r",\qquad", r"D_{\mathrm{opt}} \propto C^{0.5}", colors=colors,
                  font_size=40).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "This experiment, at enormous scale, changed how models are built. In 2020, Kaplan and colleagues "
            "concluded that model size should grow much faster than data. <bookmark mark='a'/> In 2022, DeepMind's "
            "Chinchilla paper redid it more carefully and found that size and data should grow together: about "
            "twenty training tokens for every parameter. <bookmark mark='b'/> Their seventy-billion-parameter "
            "Chinchilla beat their own two-hundred-and-eighty-billion-parameter Gopher on the same budget. "
            "<bookmark mark='c'/> Today's models train on far more data than even that, because a model is trained "
            "once and then run billions of times, so a smaller, longer-trained model is cheaper to use."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), Write(f))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()
