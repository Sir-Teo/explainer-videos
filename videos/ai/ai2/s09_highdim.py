from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import load


class HighDim(VoiceoverScene):
    def construct(self):
        self.card()
        self.angles()
        self.room()
        self.lengths()
        self.anisotropy()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Life in 768 dimensions", r"What is a space with hundreds of dimensions like?", part=2)
        with self.voiceover("Chapter eight. Life in seven hundred and sixty-eight dimensions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def angles(self):
        h = load("highdim")
        dims = list(h["dims"])
        assert dims == [2, 3, 10, 100, 768]
        sd = {d: h[f"angle_sd{d}"] for d in dims}
        assert sd[100] < 6.0 and sd[768] < 2.2
        hist = {d: np.asarray(h[f"angles{d}"], float) / 20000 for d in dims}
        top = max(hist[768].max(), 0.01)
        bars = LiveBars(hist[2], max_value=top, height=4.6, bar_width=0.28, gap=0.06, colors=C.TRUE_P)
        bars.place(-2.35)
        x0, w = bars.base.get_start()[0] + 0.15, 36 * 0.34
        ticks = VGroup(*[MathTex(rf"{a}^\circ", font_size=28, color=GREY_B).move_to([x0 + w * a / 180 - 0.03, -2.65, 0])
                         for a in (0, 45, 90, 135, 180)])
        head = label(r"The angle between two random directions", font_size=34).to_edge(UP, buff=0.4)
        dl = MathTex(r"d =", font_size=48)
        dv = Integer(2, font_size=48, color=C.BITS)
        dread = VGroup(dl, dv).arrange(RIGHT, buff=0.2).to_corner(UR, buff=0.7)
        with self.voiceover(
            "Our intuition comes from three dimensions, and in seven hundred and sixty-eight it misleads us. "
            "<bookmark mark='a'/> Pick two directions at random. In two dimensions, the angle between them could be "
            "anything. <bookmark mark='b'/> In three, angles near a right angle are already the most common. "
            "<bookmark mark='c'/> "
            "In a hundred, it's almost always within ten degrees of one, <bookmark mark='d'/> and in 768, within about "
            "four."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(ticks), FadeIn(dread))
            for d, mark in zip(dims[1:], ["b", "c", "c", "d"]):
                vo.wait_until(mark)
                self.play(*bars.to(hist[d]), ChangeDecimalToValue(dv, d), run_time=1.2)
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def room(self):
        h = load("highdim")
        assert h["n_dirs"] == 10000 and 78 < h["worst_angle"] < 80
        head = label(r"$10{,}000$ random directions in $768$ dimensions", font_size=36).to_edge(UP, buff=0.5)
        line1 = label(rf"every pair between ${h['worst_angle']:.0f}^\circ$ and ${180 - h['worst_angle']:.0f}^\circ$",
                      font_size=38, color=C.BITS).move_to(UP * 1.2)
        # a fan of nearly perpendicular arrows, drawn as if seen from far away: many directions, all apart
        g = np.random.default_rng(9)
        fan = VGroup()
        for k in range(60):
            a = g.uniform(0, 2 * PI)
            fan.add(Line(ORIGIN, [1.6 * np.cos(a), 1.6 * np.sin(a), 0], color=C.TRUE_P, stroke_width=2, stroke_opacity=0.7))
        fan.move_to(DOWN * 1.2)
        sup = label(r"more features than dimensions, if they need only be \textit{nearly} perpendicular: \\ "
                    r"\textit{superposition} \ (Part 20)", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.4)
        tag = label(r"schematic", font_size=22, color=GREY_B).next_to(fan, RIGHT, buff=0.3)
        with self.voiceover(
            "So a high-dimensional space is full of room. <bookmark mark='a'/> Ten thousand random directions in 768 "
            "dimensions: every pair of them lies between seventy-nine and a hundred and one degrees apart. "
            "<bookmark mark='b'/> A model can keep far more features than it has dimensions, as long as they only "
            "need to be nearly perpendicular. That idea, superposition, is how we'll read the inside of a model in "
            "part twenty."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l) for l in fan], lag_ratio=0.03), FadeIn(tag), run_time=1.8)
            self.play(FadeIn(line1))
            vo.wait_until("b")
            self.play(FadeIn(sup))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lengths(self):
        h = load("highdim")
        dims = list(h["dims"])
        hist = {d: np.asarray(h[f"norms{d}"], float) / 20000 for d in dims}
        top = max(hist[768].max(), 0.01)
        bars = LiveBars(hist[2], max_value=top, height=3.4, bar_width=0.17, gap=0.03, colors=C.MODEL_Q)
        bars.place(-1.75, x=-2.6)
        x0, w = bars.base.get_start()[0] + 0.15, 40 * 0.2
        ticks = VGroup(*[MathTex(t, font_size=26, color=GREY_B).move_to([x0 + w * v / 2 - 0.02, -1.95, 0])
                         for t, v in (("0", 0), (r"\sqrt d", 1), (r"2\sqrt d", 2))])
        head = label(r"The length of a random vector, \ $\mathbf{x} \sim \mathcal{N}(0, I_d)$", font_size=34).to_edge(UP, buff=0.4)
        dv = Integer(2, font_size=44, color=C.BITS)
        dread = VGroup(MathTex(r"d =", font_size=44), dv).arrange(RIGHT, buff=0.2).move_to([-2.6, 2.2, 0])
        shell = h["shell"]
        assert shell["768"] > 0.9995
        ball = VGroup(Circle(radius=1.4, color=C.TRUE_P, stroke_width=3, fill_color=C.TRUE_P, fill_opacity=0.15),
                      Annulus(inner_radius=1.27, outer_radius=1.4, color=C.BITS, fill_opacity=0.85, stroke_width=0))
        ball.move_to([4.7, 0.9, 0])
        bl = label(r"the share of a ball's volume \\ within $1\%$ of its surface", font_size=24, color=GREY_A)
        bl.next_to(ball, DOWN, buff=0.3)
        vals = VGroup(*[MathTex(rf"d = {d}: \ {100 * shell[str(d)]:.{2 if d == 768 else 1}f}\%", font_size=28,
                                color=C.BITS if d == 768 else GREY_A) for d in (3, 100, 768)])
        vals.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(bl, DOWN, buff=0.2)
        with self.voiceover(
            "Lengths behave strangely too. <bookmark mark='a'/> Give a vector 768 independent random coordinates, and "
            "its length is almost exactly the square root of 768, every time. The spread all but disappears. "
            "<bookmark mark='b'/> And nearly all of a ball's volume sits in a thin shell at its surface: in 768 "
            "dimensions, 99.96 percent of it lies within one percent of the edge."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), FadeIn(ticks), FadeIn(dread))
            vo.wait_until("a")
            for d in dims[1:]:
                self.play(*bars.to(hist[d]), ChangeDecimalToValue(dv, d), run_time=0.9)
            vo.wait_until("b")
            self.play(FadeIn(ball), FadeIn(bl))
            self.play(LaggedStart(*[FadeIn(v) for v in vals], lag_ratio=0.3))
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def anisotropy(self):
        g = load("gpt2")
        assert abs(g["cos_random_mean"] - 0.24) < 0.005 and abs(g["cos_centred_mean"]) < 0.015
        raw, cen = np.asarray(g["hist_raw"], float), np.asarray(g["hist_centred"], float)
        top = max(raw.max(), cen.max()) / raw.sum()
        bars = LiveBars(raw / raw.sum(), max_value=top, height=3.4, bar_width=0.17, gap=0.03, colors=C.TRUE_P)
        bars.place(-2.0)
        x0, w = bars.base.get_start()[0] + 0.15, 60 * 0.2

        def X(c):
            return x0 + w * (c + 0.3) / 0.9

        ticks = VGroup(*[MathTex(t, font_size=26, color=GREY_B).move_to([X(v), -2.2, 0])
                         for t, v in (("-0.3", -0.3), ("0", 0.0), ("0.3", 0.3), ("0.6", 0.6))])
        zero = DashedLine([X(0), -2.0, 0], [X(0), 1.8, 0], color=GREY_B, stroke_width=2)
        head = label(r"GPT-2: \ the cosine between $2{,}000$ random words' vectors", font_size=34).to_edge(UP, buff=0.4)
        m1 = label(rf"average ${g['cos_random_mean']:.2f}$: \ they share a direction", font_size=30, color=C.TRUE_P)
        m2 = label(rf"subtract the average vector: \ ${g['cos_centred_mean']:.2f}$", font_size=30, color=C.BITS)
        for m in (m1, m2):
            m.to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Real word vectors aren't random, though. <bookmark mark='a'/> GPT-2's vectors all lean the same way: "
            "two unrelated words have a cosine of 0.24 on average, not zero. <bookmark mark='b'/> Subtract the "
            "average vector from every word, and the cosines fall back around zero."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), FadeIn(ticks), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(m1))
            vo.wait_until("b")
            self.play(*bars.to(cen / cen.sum()), FadeOut(m1), FadeIn(m2), run_time=1.6)
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()
