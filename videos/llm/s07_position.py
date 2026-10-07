from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from explainer.fluids import colormaps as cm
from videos.llm.common import (
    attention_arcs, data, label, load_arrays, random_values, show_chapter_card, token_row, vector_strip,
)


def strip(seed, color, n=6, cell=0.18):
    return vector_strip(random_values(n, seed=seed), color=color, cell=cell, gap=0.03)


def rot_y(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_x(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


class Position(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 6, "Word order")
        self.d = data()
        self.arrays = load_arrays("gpt2_small")
        self.order_blind()
        self.learned()
        self.rotary()

    # ------------------------------------------------------------------
    def order_blind(self):
        a = token_row(["dog", " bites", " man", "."], font_size=34, buff=0.3).move_to(UP * 1.4 + LEFT * 2.2)
        b = token_row(["man", " bites", " dog", "."], font_size=34, buff=0.3).move_to(DOWN * 1.6 + LEFT * 2.2)
        w = [0.3, 0.2, 0.4, 0.1]
        arcs_a = attention_arcs(a, 3, w, max_width=10)
        arcs_b = attention_arcs(b, 3, [w[2], w[1], w[0], w[3]], max_width=10)
        out_a = strip(5, C.ATTN).next_to(a, RIGHT, buff=1.2)
        out_b = strip(5, C.ATTN).next_to(b, RIGHT, buff=1.2)
        arr_a = Arrow(a[3].get_right(), out_a.get_left(), buff=0.15, color=GREY_B)
        arr_b = Arrow(b[3].get_right(), out_b.get_left(), buff=0.15, color=GREY_B)
        same = label(r"identical\\(in the first layer)", font_size=32, color=YELLOW)
        same.move_to((out_a.get_center() + out_b.get_center()) / 2 + RIGHT * 0.4)
        eq = MathTex("=", font_size=60).rotate(PI / 2).move_to((out_a.get_center() + out_b.get_center()) / 2)
        same.next_to(eq, RIGHT, buff=0.4)

        with self.voiceover(
            "There's a gap in what we've built so far. Nothing in attention knows where a token is: queries, keys and "
            "values depend only on each token's vector. <bookmark mark='a'/> Take the sentence 'dog bites man', and look "
            "at it from the point of view of the last token, the period. <bookmark mark='w'/> It sees three words, and "
            "takes a weighted sum of their values."
        ) as vo:
            self.play(FadeIn(a, lag_ratio=0.1))
            vo.wait_until("a")
            self.play(Indicate(a[3], color=YELLOW))
            vo.wait_until("w")
            self.play(Create(arcs_a, lag_ratio=0.2), a[3].animate.set_color(YELLOW))
            self.play(GrowArrow(arr_a), FadeIn(out_a))

        with self.voiceover(
            "Now <bookmark mark='b'/> swap dog and man. The period sees exactly the same three words, with the same "
            "values, <bookmark mark='s'/> and a weighted sum doesn't care about order. So at least in the first layer, it "
            "computes exactly the same thing, even though the sentences mean very different things."
        ) as vo:
            vo.wait_until("b")
            ca = a.copy()
            self.play(ca.animate.move_to(b), run_time=1.0)
            self.play(Swap(ca[0], ca[2]), run_time=1.2)
            self.remove(ca)
            self.add(b)
            b[3].set_color(YELLOW)
            self.play(Create(arcs_b, lag_ratio=0.2))
            vo.wait_until("s")
            self.play(GrowArrow(arr_b), FadeIn(out_b))
            self.play(Write(eq), FadeIn(same))
        self.clear_scene()

    # ------------------------------------------------------------------
    def learned(self):
        row = token_row(["dog", " bites", " man", "."], font_size=32, buff=0.7).move_to(DOWN * 3.1 + LEFT * 2.6)
        tok = VGroup(*[strip(i, C.EMBED).next_to(t, UP, buff=0.35) for i, t in enumerate(row)])
        pos = VGroup(*[strip(40 + i, C.POSITION).next_to(s, RIGHT, buff=0.1) for i, s in enumerate(tok)])
        pos_l = VGroup(*[MathTex(str(i), font_size=28, color=C.POSITION).next_to(p, DOWN, buff=0.1) for i, p in enumerate(pos)])
        plus = VGroup(*[MathTex("+", font_size=32).move_to((t.get_right() + p.get_left()) / 2) for t, p in zip(tok, pos)])
        summed = VGroup(*[strip(80 + i, interpolate_color(C.EMBED, C.POSITION, 0.35)).move_to(t.get_center() + UP * 2.4)
                          for i, t in enumerate(tok)])
        arrows = VGroup(*[Arrow(VGroup(t, p).get_top(), s.get_bottom(), buff=0.1, color=GREY_B, stroke_width=3)
                          for t, p, s in zip(tok, pos, summed)])
        legend = VGroup(label(r"token vector", font_size=30, color=C.EMBED),
                        label(r"$+$ position vector", font_size=30, color=C.POSITION),
                        label(r"$=$ input to the first layer", font_size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        legend.move_to(RIGHT * 4.3 + DOWN * 0.6)
        with self.voiceover(
            "The fix: give each position its own vector, <bookmark mark='p'/> and add it to the token's vector before the "
            "first layer. <bookmark mark='s'/> Now the same word at a different position starts out as a slightly "
            "different vector."
        ) as vo:
            self.play(FadeIn(row), FadeIn(tok), FadeIn(legend[0]))
            vo.wait_until("p")
            self.play(FadeIn(pos, shift=LEFT * 0.2), FadeIn(pos_l), FadeIn(plus), FadeIn(legend[1]))
            vo.wait_until("s")
            self.play(*[GrowArrow(x) for x in arrows], *[TransformFromCopy(VGroup(t, p), s) for t, p, s in zip(tok, pos, summed)],
                      FadeIn(legend[2]), run_time=1.5)
        self.clear_scene()

        heat = self.arrays["pos_heat"]
        rgb = cm.diverging(heat, vmax=np.percentile(np.abs(heat), 98), neg="#6F7A8C", pos="#D147BD", gamma=0.8)
        img = ImageMobject(cm.to_uint8(rgb))
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        img.stretch_to_fit_height(5.6)
        img.stretch_to_fit_width(4.2)
        img.move_to(LEFT * 3.2 + DOWN * 0.4)
        frame = SurroundingRectangle(img, color=GREY_B, buff=0.02, stroke_width=1.5)
        rl = VGroup(label(r"position 0", font_size=24, color=GREY_A).next_to(frame, LEFT, buff=0.12).align_to(frame, UP),
                    label(r"1023", font_size=24, color=GREY_A).next_to(frame, LEFT, buff=0.12).align_to(frame, DOWN))
        cl = label(r"the 64 dimensions that vary most (sorted)", font_size=24, color=GREY_A).next_to(frame, UP, buff=0.12)
        title = label(r"GPT-2's learned position vectors (real)", font_size=32).to_edge(UP, buff=0.3).shift(RIGHT * 2.0)
        with self.voiceover(
            "In GPT-2, these position vectors are learned during training, just like the token embeddings: <bookmark mark='h'/> "
            "one for each of the 1,024 positions the model can handle. Here they are as a heat map, with position "
            "running down, and some of the dimensions running across. Training discovered smooth, wave-like patterns."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("h")
            self.play(FadeIn(img), Create(frame), FadeIn(rl), FadeIn(cl))

        pts = self.arrays["pos_pca"].astype(float)[:, [0, 2, 1]]  # (pc1, pc3 up, pc2 depth): the helix axis is vertical
        pts = pts / np.abs(pts).max() * 2.0
        phi = ValueTracker(0.4)
        center = RIGHT * 3.0 + DOWN * 0.2
        n_seg = 48
        bounds = np.linspace(0, len(pts) - 1, n_seg + 1).astype(int)

        def curve():
            R = rot_x(-0.35) @ rot_y(phi.get_value())
            P = pts @ R.T
            g = VGroup()
            for k in range(n_seg):
                seg = P[bounds[k]:bounds[k + 1] + 1]
                col = interpolate_color(ManimColor("#4A1F45"), ManimColor(C.POSITION), (k + 1) / n_seg)
                v = VMobject().set_points_smoothly([center + np.array([p[0], p[1], 0]) for p in seg[::4]] +
                                                    [center + np.array([seg[-1][0], seg[-1][1], 0])])
                g.add(v.set_stroke(col, 4))
            return g

        helix = always_redraw(curve)

        def endpoint(i, text):
            def f():
                R = rot_x(-0.35) @ rot_y(phi.get_value())
                p = pts[i] @ R.T
                pos = center + np.array([p[0], p[1], 0])
                return VGroup(Dot(pos, radius=0.07, color=WHITE),
                              label(text, font_size=26, color=GREY_A).next_to(pos, RIGHT, buff=0.12))
            return always_redraw(f)

        e0, e1 = endpoint(0, r"position 0"), endpoint(len(pts) - 1, r"position 1023")
        note = label(r"all 1024 position vectors, projected onto\\their 3 most important directions",
                     font_size=26, color=GREY_A).next_to(center, DOWN, buff=2.6)
        var = sum(self.d["pos_pca_var"])
        assert var > 0.85
        with self.voiceover(
            "Now project all 1,024 position vectors onto their three most important directions, <bookmark mark='c'/> and "
            "they trace out a smooth spiral. Neighboring positions get similar vectors, so the model can tell both where a "
            "token is, and roughly how far apart two tokens are."
        ) as vo:
            vo.wait_until("c")
            self.play(Create(helix), FadeIn(note), run_time=2.5)
            self.add(e0, e1)
            self.play(phi.animate.set_value(0.4 + 1.2 * PI), run_time=max(1.0, vo.remaining()), rate_func=linear)
        self.play(phi.animate.set_value(0.4 + 1.6 * PI), run_time=2, rate_func=linear)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rotary(self):
        O = LEFT * 3.2 + DOWN * 0.5
        plane = NumberPlane(x_range=[-2.6, 2.6, 1], y_range=[-2.6, 2.6, 1], x_length=5.2, y_length=5.2,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.5},
                            axis_config={"stroke_color": GREY_C, "stroke_width": 1.5}).move_to(O)
        theta = 0.42
        aq, ak = 0.2, 2.0
        Lq, Lk = 2.1, 1.8
        m = ValueTracker(3.0)
        n = ValueTracker(1.0)

        def vec(base, L, pos):
            a = base + theta * pos
            return L * np.array([np.cos(a), np.sin(a), 0])

        q = always_redraw(lambda: Arrow(O, O + vec(aq, Lq, m.get_value()), buff=0, color=C.QUERY, stroke_width=6))
        k = always_redraw(lambda: Arrow(O, O + vec(ak, Lk, n.get_value()), buff=0, color=C.KEY, stroke_width=6))
        ql = always_redraw(lambda: MathTex(r"\vec q", font_size=40, color=C.QUERY).move_to(O + 1.15 * vec(aq, Lq, m.get_value())))
        kl = always_redraw(lambda: MathTex(r"\vec k", font_size=40, color=C.KEY).move_to(O + 1.17 * vec(ak, Lk, n.get_value())))

        def dot():
            return float(vec(aq, Lq, m.get_value()) @ vec(ak, Lk, n.get_value()))

        readout = VGroup(
            VGroup(label(r"query at position", font_size=32, color=C.QUERY), DecimalNumber(3, num_decimal_places=0, font_size=36,
                                                                                      color=C.QUERY)).arrange(RIGHT, buff=0.2),
            VGroup(label(r"key at position", font_size=32, color=C.KEY), DecimalNumber(1, num_decimal_places=0, font_size=36,
                                                                                  color=C.KEY)).arrange(RIGHT, buff=0.2),
            VGroup(MathTex(r"\vec q \cdot \vec k =", font_size=40), DecimalNumber(dot(), num_decimal_places=2, font_size=40,
                                                                                  include_sign=True)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.4 + UP * 1.2)
        readout[0][1].add_updater(lambda d: d.set_value(m.get_value()))
        readout[1][1].add_updater(lambda d: d.set_value(n.get_value()))
        readout[2][1].add_updater(lambda d: d.set_value(dot()))
        title = label(r"rotary position embeddings", font_size=36).to_edge(UP, buff=0.35)
        rule = MathTex(r"\text{angle between them} \propto m - n", font_size=38, color=YELLOW).next_to(readout, DOWN, buff=0.6)

        with self.voiceover(
            "Many newer models, including Meta's Llama family, use a different trick, called rotary position "
            "embeddings. Instead of adding a position vector, they rotate the queries and keys. <bookmark mark='p'/> Split "
            "each query and key into pairs of numbers, and think of each pair as an arrow in a plane."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("p")
            self.play(FadeIn(plane))
            self.add(q, k, ql, kl)
            self.play(FadeIn(readout[:2]))

        with self.voiceover(
            "A query at position m is rotated by m times some angle, and a key at position n by n times that angle. "
            "<bookmark mark='d'/> In the dot product, only the angle between the two arrows matters, <bookmark mark='r'/> "
            "and that depends only on m minus n."
        ) as vo:
            self.play(m.animate.set_value(6), run_time=1.5)
            self.play(m.animate.set_value(3), run_time=1.0)
            vo.wait_until("d")
            self.play(FadeIn(readout[2]))
            vo.wait_until("r")
            self.play(Write(rule))

        with self.voiceover(
            "So slide both tokens along by the same amount: <bookmark mark='s'/> both arrows turn together, and the dot "
            "product doesn't change. Attention becomes sensitive to how far apart two tokens are, which is usually what "
            "matters in language, rather than to their absolute positions."
        ) as vo:
            vo.wait_until("s")
            self.play(m.animate.set_value(9), n.animate.set_value(7), run_time=3, rate_func=linear)
            self.play(Indicate(readout[2], color=YELLOW))
        self.clear_scene()

        speeds = [1.0, 0.3, 0.08]
        p = ValueTracker(0)
        dials = VGroup()
        for i in range(len(speeds)):
            c = Circle(radius=1.0, color=GREY_B, stroke_width=2)
            lab = label([r"fast pair", r"medium pair", r"slow pair"][i], font_size=28, color=GREY_A).next_to(c, DOWN, buff=0.2)
            dials.add(VGroup(c, lab))
        dials.arrange(RIGHT, buff=1.2).move_to(DOWN * 0.2)
        hands = VGroup()
        for (c, _), sp in zip(dials, speeds):
            hands.add(always_redraw(lambda sp=sp, c=c: Arrow(c.get_center(), c.get_center() + 0.9 * np.array(
                [np.sin(sp * p.get_value()), np.cos(sp * p.get_value()), 0]), buff=0, color=C.QUERY, stroke_width=6)))
        counter = VGroup(label(r"position", font_size=34), DecimalNumber(0, num_decimal_places=0, font_size=40))
        counter.arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.8)
        counter[1].add_updater(lambda d: d.set_value(p.get_value()))
        note = label(r"like the hands of a clock: short and long distances can both be told apart", font_size=30,
                     color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Different pairs of numbers rotate at different speeds, <bookmark mark='c'/> like the hands of a clock. "
            "Fast pairs distinguish nearby positions; slow pairs keep track of long distances."
        ) as vo:
            self.play(FadeIn(dials), FadeIn(counter))
            self.add(hands)
            vo.wait_until("c")
            self.play(p.animate.set_value(40), FadeIn(note), run_time=max(1.0, vo.remaining()), rate_func=linear)

        with self.voiceover(
            "So now each vector knows what its token is, where it sits, and, through attention, what's around it. "
            "Next: the other half of every layer."
        ) as vo:
            self.play(p.animate.set_value(60), run_time=max(1.0, vo.remaining()), rate_func=linear)
        self.clear_scene()
