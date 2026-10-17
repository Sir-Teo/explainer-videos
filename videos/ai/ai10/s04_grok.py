from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import curve, load

TR, TE = GREY_B, C.BITS


class Grok(VoiceoverScene):
    def construct(self):
        self.card()
        self.task()
        self.curves()
        self.circle()

    def card(self):
        card = chapter_card(3, r"Grokking", r"Can understanding arrive long after memorizing?", part=10)
        with self.voiceover("Chapter three. Grokking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def task(self):
        g = load("grok")
        P = int(g["P"])
        n = 24  # a corner of the table, drawn
        cells = VGroup()
        rg = np.random.default_rng(0)
        shown = rg.random((n, n)) < 0.4
        for a in range(n):
            for b in range(n):
                sq = Square(0.2, stroke_width=0.6, stroke_color=GREY_D,
                            fill_color=C.TRUE_P if shown[a, b] else BACKGROUND, fill_opacity=0.6 if shown[a, b] else 0)
                sq.move_to([-6.0 + 0.2 * b, 2.4 - 0.2 * a, 0])
                cells.add(sq)
        tl = label(rf"$(a + b) \bmod {P}$: \ a ${P} \times {P}$ table \ (a corner shown)", font_size=24, color=GREY_A)
        tl.next_to(cells, DOWN, buff=0.2).align_to(cells, LEFT)
        ex = VGroup(MathTex(rf"50 + 60 \equiv 13 \pmod{{{P}}}", font_size=40),
                    label(r"clock arithmetic, \ on a clock with $97$ hours", font_size=26, color=GREY_A))
        ex.arrange(DOWN, buff=0.25).move_to([3.4, 1.6, 0])
        sh = label(rf"the network sees ${int(g['n_train']):,}$ entries ($40\%$) \\ and must fill in the other ${int(g['n_test']):,}$"
                   .replace(",", "{,}"), font_size=26, color=C.TRUE_P).next_to(ex, DOWN, buff=0.6)
        cite_ = cite(r"A.~Power, Y.~Burda, H.~Edwards, I.~Babuschkin \& V.~Misra, \textit{Grokking} (2022)", corner=DR)
        assert (50 + 60) % P == 13
        with self.voiceover(
            "In 2022, a team at OpenAI noticed something strange. Take a tiny task: addition on a clock with "
            f"{P} hours, so fifty plus sixty is thirteen. <bookmark mark='a'/> Show a network forty percent of the "
            "addition table, and ask it to fill in the rest."
        ) as vo:
            self.play(Write(ex[0]), FadeIn(ex[1]), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.0008), FadeIn(tl), FadeIn(sh), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        g = load("grok")
        W, N = np.asarray(g["wd"]), np.asarray(g["nowd"])
        t_tr, t_te = int(g["t_train_wd"]), int(g["t_test_wd"])
        ax = Axes(x_range=[0, 4.1, 1], y_range=[0, 1, 0.25], x_length=8.4, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.4, -0.4, 0])
        xl = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3), ("10{,}000", 4))])
        yl = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0, 0.5, 1)])
        xn = label(r"training steps \ (log scale)", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.45)

        def lines(D, sw=3.5):
            lx = np.log10(D[:, 0])
            return curve(ax, lx, D[:, 1], TR, sw), curve(ax, lx, D[:, 2], TE, sw)

        wtr, wte = lines(W)
        ntr, _ = lines(N, 2.5)
        ntr.set_stroke(opacity=0.6)
        # without weight decay the unseen entries stay at chance: dashed red, drawn over the axis so it can be seen
        nte = DashedVMobject(curve(ax, np.log10(N[:, 0]), N[:, 2], C.SURPRISE, 4), num_dashes=90)
        key = VGroup(label(r"the $40\%$ it has seen", font_size=26, color=TR), label(r"the $60\%$ it hasn't", font_size=26, color=TE))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, 1.6, 0])
        m1 = DashedLine(ax.c2p(math.log10(t_tr), 0), ax.c2p(math.log10(t_tr), 1), color=TR, stroke_width=2)
        m2 = DashedLine(ax.c2p(math.log10(t_te), 0), ax.c2p(math.log10(t_te), 1), color=TE, stroke_width=2)
        lag = label(rf"memorized by step ${t_tr:,}$; \\ understood by step ${t_te:,}$".replace(",", "{,}"), font_size=26,
                    color=WHITE).next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        nowd = label(r"without weight decay (dashed): \\ it never generalizes" if g["t_test_nowd"] is None else
                     rf"without weight decay (dashed): \\ much later, \ step ${int(g['t_test_nowd']):,}$".replace(",", "{,}"),
                     font_size=24, color=C.SURPRISE).next_to(lag, DOWN, buff=0.4).align_to(key, LEFT)
        with self.voiceover(
            f"It memorizes the entries it was shown within about {t_tr:,} steps, and for a long time, it gets the "
            "unseen ones no better than chance. <bookmark mark='a'/> Keep training anyway. Then, thousands of "
            "steps later, accuracy on the unseen entries shoots up to nearly a hundred percent. The network has "
            "found the rule. They called it grokking. <bookmark mark='b'/> Weight decay is what drives it: it keeps "
            "squeezing the weights, and the memorized lookup table is more expensive than the rule."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xn), FadeIn(key))
            self.play(Create(wtr), run_time=2.0)
            self.play(Create(m1))
            vo.wait_until("a")
            self.play(Create(wte), run_time=3.0)
            self.play(Create(m2), FadeIn(lag))
            vo.wait_until("b")
            self.play(Create(ntr), Create(nte), FadeIn(nowd), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def circle(self):
        g = load("grok")
        P = int(g["P"])
        F = np.asarray(g["fourier"])
        xy = np.asarray(g["emb_xy"])
        k = int(np.argmax(F[1:])) + 1
        nf = int((F[1:] >= 0.5 * F[1:].max()).sum())  # the frequencies at least half as strong as the strongest
        bars = VGroup(*[Rectangle(width=0.08, height=max(2.6 * f / F[1:].max(), 0.01), stroke_width=0,
                                  fill_color=C.BITS if i == k else GREY_B, fill_opacity=0.9)
                        .move_to([-6.0 + 0.1 * i, -2.2 + 1.3 * f / F[1:].max(), 0]) for i, f in enumerate(F[1:], start=1)])
        bl = label(r"the learned number vectors, \ by frequency", font_size=24, color=GREY_A).next_to(bars, UP, buff=0.25)
        # the numbers placed by the learned vectors' two main directions, at several moments of training
        snaps = np.asarray(g["snap_xy"])
        snap_steps = [int(k) for k in g["snap_steps"]]
        snaps = snaps / np.abs(snaps).max(axis=(1, 2), keepdims=True) * 2.4  # each moment at the same size
        xy = snaps[-1]

        def place(Q):
            return [[2.8 + p[0], -0.2 + p[1], 0] for p in Q]

        pts = VGroup(*[Dot(q, radius=0.05, color=interpolate_color(ManimColor(C.TRUE_P), ManimColor(C.MODEL_Q), i / P))
                       for i, q in enumerate(place(snaps[0]))])
        clock = VGroup(label(r"training step", font_size=24, color=GREY_A), Integer(snap_steps[0], font_size=28, color=C.BITS))
        clock.arrange(RIGHT, buff=0.2).move_to([2.8, 2.55, 0])
        # the test accuracy at each of those moments, from the training curve (with weight decay)
        Wc = np.asarray(g["wd"])
        acc_at = [float(np.interp(k_, Wc[:, 0], Wc[:, 2])) for k_ in snap_steps]
        tst = VGroup(label(r"test accuracy", font_size=22, color=GREY_A), DecimalNumber(100 * acc_at[0], num_decimal_places=0,
                                                                                         unit=r"\%", font_size=26, color=C.TRUE_P))
        tst.arrange(RIGHT, buff=0.2).next_to(clock, DOWN, buff=0.12)
        nums = VGroup(*[MathTex(str(i), font_size=18, color=GREY_A).next_to(place([xy[i]])[0], UR, buff=0.02) for i in (0, 1, 2, 3)])
        pl = label(r"the number vectors, \ along their final two main directions", font_size=24, color=GREY_A).to_edge(UP, buff=0.4).set_x(2.8)
        note_ = label(r"each number becomes a point on circles: \\ adding numbers turns into adding angles", font_size=26,
                      color=C.BITS).move_to([-3.4, 2.2, 0])  # the empty space above the bars, clear of the citation
        cite_ = cite(r"N.~Nanda et al., \textit{Progress Measures for Grokking via Mechanistic Interpretability} (2023)", corner=DL)
        with self.voiceover(
            "What is the rule it found? Look at the vectors it learned for the numbers. <bookmark mark='a'/> Most of "
            f"their weight sits on {nf} frequencies out of {len(F) - 1}: waves around the clock. <bookmark mark='b'/> Seen along their main "
            "directions, the numbers lie on circles; here they are forming during training, and the circles appear "
            "just as the test accuracy climbs. The network turns each number into an angle, and adds numbers "
            "by adding angles, as a clock does. Neel Nanda and colleagues worked this out in 2023, one of the first "
            "complete explanations of what a trained network computes. Part twenty takes that idea to real models."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.01), FadeIn(bl), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.01), FadeIn(pl), FadeIn(clock), FadeIn(tst), run_time=1.2)
            for k, Q, a_ in zip(snap_steps[1:], snaps[1:], acc_at[1:]):  # the scatter tightening into circles, as test accuracy rises
                self.play(*[d.animate.move_to(q) for d, q in zip(pts, place(Q))], clock[1].animate.set_value(k),
                          tst[1].animate.set_value(100 * a_), run_time=0.55, rate_func=smooth)
            self.play(FadeIn(nums), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
