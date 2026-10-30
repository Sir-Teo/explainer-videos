from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import DCOL, HIST, NCOL, PART, SP, TT, lag, load, predict_card, takeaway_card


class Overtrain(VoiceoverScene):
    def construct(self):
        self.card()
        self.predict()
        self.price()
        self.inference()
        self.takeaway()

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
        wl0 = label(r"smaller than this: \\ never, \ at any budget", font_size=20, color=GREY_B).move_to(ax.c2p(0.62, math.log10(9)))
        wl = VGroup(wl0, Arrow(wl0.get_left(), ax.c2p(kmin, math.log10(9)), buff=0.1, stroke_width=2, color=GREY_B,
                                max_tip_length_to_length_ratio=0.12))
        # measured: endpoints of the sweep that reached the budget's best loss with a smaller model, trained longer
        mt = np.asarray(ch["matched"], float).reshape(-1, 3)
        meas = VGroup(*[Dot(ax.c2p(n_ / n0, math.log10(c_)), radius=0.07, color=WHITE)
                        for n_, d_, c_ in mt if 0.1 <= n_ / n0 <= 1.0 and 1 <= c_ <= top])
        ml = label(r"white: \ our runs that got there", font_size=20, color=WHITE).next_to(ax.c2p(1.0, math.log10(top)), DL, buff=0.1)
        law = MathTex(r"L(kN_{\text{opt}},\, D) = L^* \ \Rightarrow\ D = \Big(\frac{B}{L^* - E - "
                      r"A\,(kN_{\text{opt}})^{-\alpha}}\Big)^{1/\beta}",
                      font_size=28).to_edge(UP, buff=0.3)
        c75, c50 = float(np.interp(0.75, ks, cost)), float(np.interp(0.5, ks, cost))
        said1 = (
            f"Our own runs that reached the same loss with smaller models fall near the curve: {len(meas)} of them."
            if len(meas) >= 2 else "Few of our runs reach that loss with a smaller model; those that do sit near the "
                                   "curve."
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
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Write(law))
            self.play(Create(line), run_time=max(2.0, vo.until("a")))
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
        # exactly a hundred times the optimal training, interpolated along the computed curve
        tpp100 = float(10 ** np.interp(2.0, lx, np.log10(tpp)))
        nrel100, sav100 = float(np.interp(2.0, lx, nrel)), float(np.interp(2.0, lx, sav))
        facts = VGroup(
            history_card(2023, r"Sardana, Portes, Doubov \& Frankle", r"with about a billion requests to serve, "
                         r"train smaller and longer than Chinchilla; \ quality kept improving up to $10{,}000$ tokens "
                         r"per "
                         r"parameter", width=5.4, color=HIST),
            history_card(2024, r"Meta, \ Llama 3", r"$8$ billion parameters, \ $15$ trillion tokens: \ about $1{,}900$ "
                         r"per parameter", width=5.4, color=HIST),
        ).arrange(DOWN, buff=0.18).move_to([3.9, -1.2, 0])
        link = note(r"how tokens per parameter grew, model by model: \ Part 14; \\ the cost of answering: \ Part 19")
        if link.width > facts.width:
            link.scale_to_fit_width(facts.width)
        link.next_to(facts, DOWN, buff=0.15).align_to(facts, LEFT)
        # what answering costs over a life: a model that answers a hundred times what it was trained on
        unit = 0.032
        lifebars = VGroup()
        for k, (txt, ops, col) in enumerate(((r"training: \ $6ND$", 6, NCOL),
                                               (r"answering $T = 100\,D$: \ $2NT = 200\,ND$", 200, TT))):
            bar = Rectangle(width=max(ops * unit, 0.08), height=0.36, stroke_width=0, fill_color=col, fill_opacity=0.85)
            bar.move_to([-6.2, -1.3 - 0.75 * k, 0], aligned_edge=LEFT)
            lifebars.add(VGroup(bar, label(txt, font_size=22, color=col).next_to(bar, UP, buff=0.06).align_to(bar, LEFT)))
        lifenote = note(r"the lifetime cost, \ drawn to scale").next_to(lifebars, DOWN, buff=0.15).align_to(lifebars, LEFT)
        life = VGroup(lifebars, lifenote)
        with self.voiceover(
            "In 2023, Nikhil Sardana and colleagues at MosaicML put the answering into the budget. Training costs six "
            "operations per parameter per token, and answering costs two. <bookmark mark='a'/> Fix the quality, and "
            "minimize the lifetime cost. <bookmark mark='b'/> The more a model will be used, the smaller and longer "
            "trained it should be. <bookmark mark='c'/> On our fitted law: a model that will answer a hundred times "
            f"more characters than it would be trained on should train on about {tpp100:.0f} characters per "
            f"parameter, at {nrel100:.2f} of the optimal size, and costs {100 * sav100:.0f} percent less over "
            "its "
            "life. <bookmark mark='d'/> Sardana's team found quality still improving at ten thousand tokens per "
            "parameter, and in 2024 Meta trained Llama 3's eight-billion-parameter model on fifteen trillion tokens: "
            "nearly nineteen hundred per parameter, a hundred times Chinchilla's ratio."
        ) as vo:
            step(0)
            self.play(LaggedStart(*[GrowFromEdge(b_[0], LEFT) for b_ in lifebars], lag_ratio=0.5),
                      *[FadeIn(b_[1]) for b_ in lifebars], FadeIn(lifenote), run_time=2.0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeOut(life))
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            self.play(Create(cv), run_time=2.0)
            self.play(Flash(ax.c2p(2.0, math.log10(tpp100)), color=TT), FadeIn(Dot(ax.c2p(2.0, math.log10(tpp100)), radius=0.08, color=WHITE)))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(f_, shift=LEFT * 0.1) for f_ in facts], lag_ratio=0.5), FadeIn(link))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def predict(self):
        pc = predict_card(r"A model half the compute-optimal size, \ trained longer until it matches the optimal "
                          r"model's loss. \ How much more training compute: \ a few percent, \ double, \ or ten "
                          r"times?")
        with self.voiceover(
            "Pause and predict. A model half the compute-optimal size, trained longer until it matches the optimal "
            "model's loss. How much more training compute will it need: a few percent, double, or ten times?"
        ):
            self.play(FadeIn(pc, shift=UP * 0.2))
        self.wait(2.0)
        self.play(FadeOut(pc))

    def takeaway(self):
        tk = takeaway_card(r"Train smaller, \ for longer",
                           r"Once answering is counted, \ the best model is smaller than the compute optimum and "
                           r"trained far past $20$ tokens per parameter.",
                           r"next: \ when there are not enough tokens to read")
        with self.voiceover(
            "The takeaway: once answering is counted, the best model is smaller than the compute optimum, and trained "
            "far longer, which is why open models now read thousands of tokens per parameter. Next: what happens when "
            "there are not enough tokens to read."
        ) as vo:
            self.play(FadeIn(tk[0], shift=UP * 0.2))
            self.wait(max(0.0, vo.duration * 0.5 - 1.0))
            self.play(FadeIn(tk[1]))
        self.wait(0.4)
        self.play(FadeOut(tk))
