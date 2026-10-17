from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import A, K, MONO, POS, Q, V, curve, load


def dial(radius=0.32, color=GREY_C) -> VGroup:
    return VGroup(Circle(radius=radius, stroke_color=color, stroke_width=1.5, fill_color="#121722", fill_opacity=1),
                  Dot(radius=0.025, color=GREY_B))


class Rope(VoiceoverScene):
    def construct(self):
        self.card()
        self.blind()
        self.clocks()
        self.relative()
        self.decay()

    def card(self):
        card = chapter_card(3, r"Positions as rotations", r"How does attention know where things are?", part=11)
        with self.voiceover("Chapter three. Positions as rotations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def blind(self):
        words = ["dog", "bites", "man"]

        def row(order, y):
            g = VGroup(*[VGroup(RoundedRectangle(width=1.5, height=0.7, corner_radius=0.1, stroke_color=K, stroke_width=2),
                                Text(words[i], font=MONO, font_size=28, color=WHITE)) for i in order])
            for b in g:
                b[1].move_to(b[0])
            return g.arrange(RIGHT, buff=0.4).move_to([0, y, 0])

        r1 = row([0, 1, 2], 1.6)
        r2 = row([2, 1, 0], 1.6)
        qd = VGroup(Circle(radius=0.32, color=Q, stroke_width=3), MathTex(r"q", font_size=32, color=Q)).move_to([0, -0.6, 0])
        w = [0.5, 0.2, 0.3]

        def lines(r, order):
            return VGroup(*[Line(qd.get_top(), b.get_bottom(), color=A, stroke_width=2 + 14 * w[i])
                            for b, i in zip(r, order)])

        l1 = lines(r1, [0, 1, 2])
        out = label(r"$0.5\,v_{\mathrm{dog}} + 0.2\,v_{\mathrm{bites}} + 0.3\,v_{\mathrm{man}}$", font_size=30, color=V)
        out.next_to(qd, DOWN, buff=0.5)
        same = label(r"reorder the words: \ the same weights, \ the same average", font_size=28, color=GREY_A)
        same.to_edge(DOWN, buff=0.5)
        tag = note(r"illustrative weights").to_corner(DR, buff=0.3)
        with self.voiceover(
            "There's a problem. Attention averages over a set. <bookmark mark='a'/> Each word gets a weight from its "
            "key, wherever it sits. <bookmark mark='b'/> So 'dog bites man' and 'man bites dog' look exactly the "
            "same: the same weights, the same average. The order is lost. The model has to be told where each "
            "character is."
        ) as vo:
            self.play(FadeIn(r1), FadeIn(qd), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in l1], lag_ratio=0.2), FadeIn(out))
            vo.wait_until("b")
            l2 = lines(r2, [2, 1, 0])
            self.play(*[r1[i].animate.move_to(r2[j]) for i, j in ((0, 2), (2, 0))], Transform(l1, l2), run_time=1.5,
                      path_arc=PI / 3)
            self.play(Indicate(out, color=V), FadeIn(same))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def clocks(self):
        r = load("rope")
        th = np.asarray(r["theta"])
        wl = np.asarray(r["wavelength"])
        n = len(th)
        m = ValueTracker(0.0)
        dials = VGroup(*[dial() for _ in range(n)]).arrange(RIGHT, buff=0.14).move_to(UP * 0.4)
        start = np.random.default_rng(3).uniform(0, 2 * PI, n)  # the query's own angles, before any rotation

        def hands():
            return VGroup(*[Line(d.get_center(), d.get_center() + 0.3 * np.array([math.cos(a0 + m.get_value() * t),
                                                                                   math.sin(a0 + m.get_value() * t), 0]),
                                 color=Q, stroke_width=3)
                            for d, a0, t in zip(dials, start, th)])

        hs = always_redraw(hands)
        wls = VGroup(*[MathTex(f"{v:,.0f}".replace(",", "{,}") if v >= 10 else f"{v:.1f}", font_size=17, color=GREY_B)
                       .next_to(d, DOWN, buff=0.12) for d, v in zip(dials, wl)])
        wlab = label(r"characters per full turn", font_size=22, color=GREY_A).next_to(wls, DOWN, buff=0.15)
        pairs = label(rf"a query's ${2 * n}$ numbers, \ taken in ${n}$ pairs: \ each pair is an arrow", font_size=26,
                      color=GREY_A).to_edge(UP, buff=0.5)
        counter = VGroup(label(r"position", font_size=30, color=POS), Integer(0, font_size=36, color=POS))
        counter.arrange(RIGHT, buff=0.25).next_to(dials, UP, buff=0.6)
        counter[1].add_updater(lambda t: t.set_value(int(round(m.get_value()))))
        colors = {r"m": POS, r"\theta_j": GREY_A}
        f = cmath(r"\begin{pmatrix} \cos m\theta_j & -\sin m\theta_j \\ \sin m\theta_j & \cos m\theta_j \end{pmatrix}",
                  font_size=36).to_edge(DOWN, buff=0.85).shift(LEFT * 2.5)
        fl = cmath(r"\theta_j = 10000^{-2j/32}", font_size=34, colors=colors).next_to(f, RIGHT, buff=0.8)
        cite_ = cite(r"J.~Su et al., \textit{RoFormer: Enhanced Transformer with Rotary Position Embedding} (2021)", corner=DR)
        with self.voiceover(
            "The answer used by nearly every model today is to rotate. Take a query's thirty-two numbers in sixteen "
            "pairs; each pair is an arrow in a plane. <bookmark mark='a'/> At position m, turn pair j by m times an "
            "angle theta j. <bookmark mark='b'/> The first pair turns fast, a full turn every six characters; each "
            "pair after it turns more slowly, down to one turn in thirty-five thousand. "
            "<bookmark mark='c'/> Keys are turned the same way. Like the hands of a clock, fast hands tell you the "
            "position nearby, slow hands where you are in a long text. This is RoPE, rotary position embedding."
        ) as vo:
            self.play(FadeIn(pairs), LaggedStart(*[FadeIn(d) for d in dials], lag_ratio=0.05), FadeIn(hs))
            vo.wait_until("a")
            self.play(FadeIn(counter), Write(f), FadeIn(fl))
            vo.wait_until("b")
            self.play(m.animate.set_value(40), FadeIn(wls), FadeIn(wlab), run_time=6.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(cite_), m.animate.set_value(60), run_time=3.0, rate_func=linear)
        self.wait(0.3)
        counter[1].clear_updaters()
        hs.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def relative(self):
        r = load("rope")
        big = dial(radius=1.8).move_to([-3.4, -0.2, 0])
        qa, ka, th = 0.4, 2.0, 0.35  # illustrative angles for one pair
        mq, nk = ValueTracker(5.0), ValueTracker(2.0)
        c = big.get_center()

        def arrow(a, col, length):
            return Arrow(c, c + length * np.array([math.cos(a), math.sin(a), 0]), buff=0, color=col, stroke_width=6,
                         max_tip_length_to_length_ratio=0.12)

        qarr = always_redraw(lambda: arrow(qa + mq.get_value() * th, Q, 1.6))
        karr = always_redraw(lambda: arrow(ka + nk.get_value() * th, K, 1.3))

        def angle_arc():
            a1, a2 = qa + mq.get_value() * th, ka + nk.get_value() * th
            return Arc(radius=0.55, start_angle=a1, angle=(a2 - a1 + PI) % (2 * PI) - PI, arc_center=c, color=A,
                       stroke_width=4)

        arc = always_redraw(angle_arc)
        readout = VGroup(label(r"query at position", font_size=28, color=Q), Integer(5, font_size=32, color=Q),
                         label(r"key at position", font_size=28, color=K), Integer(2, font_size=32, color=K))
        readout[0].move_to([1.6, 2.6, 0], aligned_edge=LEFT)
        readout[2].move_to([1.6, 2.0, 0], aligned_edge=LEFT)
        readout[1].next_to(readout[0], RIGHT, buff=0.25)
        readout[3].next_to(readout[2], RIGHT, buff=0.25).align_to(readout[1], LEFT)
        readout[1].add_updater(lambda t: t.set_value(int(round(mq.get_value()))))
        readout[3].add_updater(lambda t: t.set_value(int(round(nk.get_value()))))
        score = VGroup(label(r"score", font_size=28, color=A), DecimalNumber(0, num_decimal_places=3, font_size=32, color=A))
        score.arrange(RIGHT, buff=0.2).move_to([1.6, 1.35, 0], aligned_edge=LEFT)
        score[1].add_updater(lambda t: t.set_value(1.6 * 1.3 * math.cos(qa + mq.get_value() * th - ka - nk.get_value() * th) / 2))
        colors = {r"m": Q, r"n": K, r"q": Q, r"k": K}
        f = cmath(r"(R_{", r"m", r"}\,", r"q", r")\cdot(R_{", r"n", r"}\,", r"k", r")", "=", r"q", r"\cdot", r"R_{", r"n",
                  r"-", r"m", r"}\,", r"k", colors=colors, font_size=40).move_to([2.6, 0.6, 0])
        fl = label(r"only the distance between them counts", font_size=26, color=GREY_A).next_to(f, DOWN, buff=0.25)
        chk = label(rf"computed for a real 32-number pair of vectors: \\ shifting both changes the score by under "
                    rf"$10^{{{math.ceil(math.log10(max(float(r['dev']), 1e-16)))}}}$", font_size=22, color=GREY_B)
        chk.next_to(fl, DOWN, buff=0.45)
        tag = note(r"one pair, \ illustrative angles").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Why rotations? Look at one pair, in a query at position five and a key at position two. "
            "<bookmark mark='a'/> Their score depends on the angle between them. Now move both forward by the same "
            "amount, as if the same words appeared later in the text. <bookmark mark='b'/> Both arrows turn by the "
            "same angle, so the angle between them doesn't change, and neither does the score. "
            "<bookmark mark='c'/> A rotated query and a rotated key score according to how far apart they are, not "
            "where they are. Relative position comes for free, from the geometry of rotations."
        ) as vo:
            self.play(FadeIn(big), FadeIn(tag), FadeIn(qarr), FadeIn(karr), FadeIn(readout))
            vo.wait_until("a")
            self.play(Create(arc), FadeIn(score))
            vo.wait_until("b")
            self.play(mq.animate.set_value(25), nk.animate.set_value(22), run_time=5.0, rate_func=smooth)
            vo.wait_until("c")
            self.play(Write(f), FadeIn(fl))
            self.play(FadeIn(chk))
        self.wait(0.3)
        for mob in (qarr, karr, arc, readout[1], readout[3], score[1]):
            mob.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def decay(self):
        r = load("rope")
        rr, dc = np.asarray(r["rs"], float), np.asarray(r["smooth"])
        raw_r, raw = np.asarray(r["r"], float)[1:], np.asarray(r["decay"])[1:]
        lx = np.log10(rr)
        ax = Axes(x_range=[0, 3.4, 1], y_range=[-0.5, 1, 0.5], x_length=7.6, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.9, -0.6, 0])
        xt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, -0.5), DOWN, buff=0.1)
                      for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3))])
        yt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for t, v in (("0", 0), ("1", 1))])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(3.4, 0), color=GREY_D, stroke_width=1.5)
        xn = label(r"distance between query and key, \ in characters", font_size=24, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        yn = label(r"a query's score against itself, \ moved apart \ (relative to distance $0$)", font_size=22, color=GREY_A)
        yn.next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        faint = curve(ax, np.log10(raw_r), raw, POS, 1).set_stroke(opacity=0.25)
        c = curve(ax, lx, dc, POS, 4)
        note_ = label(r"far apart, \\ the hands disagree: \\ distant matches \\ count for less, \\ on average", font_size=26,
                      color=POS).move_to([4.6, 0.6, 0])
        used = label(r"RoPE: \ Llama, Qwen, DeepSeek, \\ Mistral, Gemma, GLM, Kimi \dots", font_size=24, color=GREY_A)
        used.move_to([4.6, -1.6, 0])
        with self.voiceover(
            "And a bonus. Score a query against an identical key, then move them apart. Each pair's arrows drift "
            "out of step at its own speed, so the score shrinks with distance: <bookmark mark='a'/> on average, "
            "nearby matches count more than distant ones, a gentle bias towards the recent past that nobody had to "
            "build in. <bookmark mark='b'/> Since 2021, rotary positions have become the standard: almost every open "
            "model uses them."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), Create(zero), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(FadeIn(faint), Create(c), run_time=2.5)
            self.play(FadeIn(note_))
            vo.wait_until("b")
            self.play(FadeIn(used))
        self.wait(0.3)
        self.clear_scene()
