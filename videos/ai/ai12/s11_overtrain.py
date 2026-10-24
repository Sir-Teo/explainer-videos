from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import DCOL, HIST, NCOL, PART, SP, TT, load, lag


class Overtrain(VoiceoverScene):
    def construct(self):
        self.card()
        self.price()
        self.inference()

    def card(self):
        card = chapter_card(10, r"Trained for the long run", r"Why train a small model far past its optimum?", part=PART)
        with self.voiceover("Chapter ten. Trained for the long run."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def price(self):
        ch = load("chinchilla")
        ks, cost = np.asarray(ch["ot_k"], float), np.asarray(ch["ot_cost"], float)
        kmin = float(ch["ot_kmin"])
        n0 = float(ch["ot_N0"])
        C0 = float(ch["ot_C"])
        top = 16.0
        ax = CornerAxes(x_range=[0.1, 1.0, 0.1], y_range=[0, math.log10(top), 0.5], x_length=6.2, y_length=4.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.6, -0.4, 0])
        ok = cost <= top
        line = VMobject(color=SP, stroke_width=4).set_points_smoothly([ax.c2p(k, math.log10(c)) for k, c in zip(ks[ok], cost[ok])])
        yt = VGroup(*[MathTex(rf"{v}\times", font_size=22, color=GREY_B).next_to(ax.c2p(0.1, math.log10(v)), LEFT, buff=0.08)
                      for v in (1, 2, 4, 8, 16)])
        xt = VGroup(*[MathTex(t_, font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                      for v, t_ in ((0.25, r"\tfrac14"), (0.5, r"\tfrac12"), (0.75, r"\tfrac34"), (1.0, r"1"))])
        xn = label(r"model size, \ relative to the best for the budget", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"training compute to reach the same loss", font_size=22, color=GREY_A)
        yn.next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        marks = VGroup()
        for k in (0.75, 0.5):
            c = float(np.interp(k, ks, cost))
            if c <= top:
                marks.add(VGroup(Dot(ax.c2p(k, math.log10(c)), radius=0.08, color=SP),
                                 MathTex(rf"+{100 * (c - 1):.0f}\%", font_size=26, color=SP).next_to(ax.c2p(k, math.log10(c)), UR, buff=0.08)))
        wall = DashedLine(ax.c2p(kmin, 0), ax.c2p(kmin, math.log10(top)), dash_length=0.06, stroke_width=2, color=GREY_B)
        wl = label(r"smaller than this: \\ never, \ at any budget", font_size=20, color=GREY_B).next_to(wall, RIGHT, buff=0.1).shift(UP * 1.3)
        # measured: endpoints of the sweep that reached the budget's best loss with a smaller model, trained longer
        mt = np.asarray(ch["matched"], float).reshape(-1, 3)
        meas = VGroup(*[Dot(ax.c2p(n_ / n0, math.log10(c_)), radius=0.07, color=WHITE)
                        for n_, d_, c_ in mt if 0.1 <= n_ / n0 <= 1.0 and 1 <= c_ <= top])
        ml = label(r"white: \ our runs that got there", font_size=20, color=WHITE).next_to(ax.c2p(1.0, math.log10(top)), DL, buff=0.1)
        law = MathTex(r"L(kN_{\text{opt}},\, D) = L^* \ \Rightarrow\ D = \Big(\frac{B}{L^* - E - A\,(kN_{\text{opt}})^{-\alpha}}\Big)^{1/\beta}",
                      font_size=28).to_edge(UP, buff=0.3)
        c75, c50 = float(np.interp(0.75, ks, cost)), float(np.interp(0.5, ks, cost))
        said1 = (
            f"Our own runs that reached the same loss with smaller models fall near the curve: {len(meas)} of them."
            if len(meas) >= 2 else "Few of our runs reach that loss with a smaller model; those that do sit near the curve."
        )
        with self.voiceover(
            "Chinchilla's optimum minimizes the cost of training. But a model is trained once and then used, maybe "
            "billions of times, and every use costs in proportion to its size. So it can pay to train a smaller "
            "model for longer. How much longer? The fitted law answers. <bookmark mark='a'/> Ask for the optimal "
            "model's loss from a model k times its size, and solve for the data it needs. <bookmark mark='b'/> A "
            f"model three quarters the size costs {100 * (c75 - 1):.0f} percent more training; half the size, "
            f"{100 * (c50 - 1):.0f} percent more; <bookmark mark='c'/> and below {kmin:.2f} of the size, no amount of "
            "data is enough: the small model's floor is above the target. <bookmark mark='d'/> "
            + said1
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(Write(law))
            self.play(Create(line), run_time=2.0)
            vo.wait_until("b")
            self.play(lag([FadeIn(m_) for m_ in marks], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(Create(wall), FadeIn(wl))
            vo.wait_until("d")
            self.play(lag([FadeIn(d_, scale=0.5) for d_ in meas], lag_ratio=0.2), FadeIn(ml))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inference(self):
        ch = load("chinchilla")
        T, tpp, nrel, sav = (np.asarray(ch[k], float) for k in ("inf_T", "inf_tpp", "inf_N", "inf_saving"))
        D0, N0 = float(ch["ot_D0"]), float(ch["ot_N0"])
        colors = {r"N": NCOL, r"D": DCOL, r"T": TT}
        rows = [
            cmath(r"\text{cost}", r"=", r"6\,N D", r"+", r"2\,N T", font_size=34, colors=colors),
            cmath(r"\min_{N, D}\ 6ND + 2NT", r"\quad\text{with}\quad", r"L(N, D) = L^*", font_size=34),
            cmath(r"T \gg D", r"\ \Rightarrow\ ", r"\text{smaller } N, \ \text{longer } D", font_size=34),
        ]
        whys = [why(r"training: \ $6$ per parameter per token; \ answering: \ $2$"),
                why(r"the same quality, \ the cheapest lifetime"), why(r"each answer's cost weighs on $N$ alone")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-2.2, buff=0.35, edge=6.9)
        lx = np.log10(T / D0)
        ly = np.log10(tpp)
        ax = CornerAxes(x_range=[lx.min(), lx.max(), 1], y_range=[math.floor(ly.min()), math.ceil(ly.max()), 1], x_length=6.0,
                        y_length=3.0, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
        ax.move_to([-2.6, -1.85, 0])
        xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, math.floor(ly.min())), DOWN, buff=0.08)
                      for v in range(math.ceil(lx.min()), math.floor(lx.max()) + 1)])
        yt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(lx.min(), v), LEFT, buff=0.08)
                      for v in range(math.floor(ly.min()), math.ceil(ly.max()) + 1)])
        xn = label(r"characters it will answer, \ over its lifetime, \ relative to its optimal training", font_size=20,
                   color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yn = label(r"the best training, \ characters per parameter", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        cv = curve(ax, lx, ly, TT, 4, smooth=True)
        i100 = int(np.argmin(np.abs(T / D0 - 100)))
        facts = VGroup(
            history_card(2023, r"Sardana, Portes, Doubov \& Frankle", r"with about a billion requests to serve, "
                         r"train smaller and longer than Chinchilla; \ quality kept improving up to $10{,}000$ tokens per "
                         r"parameter", width=5.4, color=HIST),
            history_card(2024, r"Meta, \ Llama 3", r"$8$ billion parameters, \ $15$ trillion tokens: \ about $1{,}900$ "
                         r"per parameter", width=5.4, color=HIST),
        ).arrange(DOWN, buff=0.18).move_to([3.9, -1.2, 0])
        link = note(r"how tokens per parameter grew, model by model: \ Part 14; \ the cost of answering: \ Part 19")
        link.to_corner(DR, buff=0.2)
        with self.voiceover(
            "In 2023, Nikhil Sardana and colleagues at MosaicML put the answering into the budget. Training costs six "
            "operations per parameter per token, and answering costs two. <bookmark mark='a'/> Fix the quality, and "
            "minimize the lifetime cost. <bookmark mark='b'/> The more a model will be used, the smaller and longer "
            "trained it should be. <bookmark mark='c'/> On our fitted law: a model that will answer a hundred times "
            f"more characters than it would be trained on should train on about {tpp[i100]:.0f} characters per "
            f"parameter, at {nrel[i100]:.2f} of the optimal size, and costs {100 * sav[i100]:.0f} percent less over its "
            "life. <bookmark mark='d'/> Sardana's team found quality still improving at ten thousand tokens per "
            "parameter, and in 2024 Meta trained Llama 3's eight-billion-parameter model on fifteen trillion tokens: "
            "nearly nineteen hundred per parameter, a hundred times Chinchilla's ratio."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            self.play(Create(cv), run_time=2.0)
            self.play(Flash(ax.c2p(lx[i100], ly[i100]), color=TT), FadeIn(Dot(ax.c2p(lx[i100], ly[i100]), radius=0.08, color=WHITE)))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(f_, shift=LEFT * 0.1) for f_ in facts], lag_ratio=0.5), FadeIn(link))
        self.wait(0.3)
        self.clear_scene()
