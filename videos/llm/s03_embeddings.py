from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.llm.common import (
    PROMPT, ProbBars, TokenBox, cell_matrix, data, label, num_column, random_values, show_chapter_card, token_row,
    vector_strip,
)

GROUP_NAMES = {"numbers": "numbers", "days": "days of the week", "countries": "countries", "animals": "animals",
               "colors": "colors"}


class Embeddings(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 2, "Tokens into vectors")
        self.d = data()
        self.lookup()
        self.clusters()
        self.analogy()
        self.dot_product()

    # ------------------------------------------------------------------
    def lookup(self):
        d = self.d
        rows, cols, col = 9, 26, 17
        mat = cell_matrix(rows, cols, C.EMBED, cell=0.2, gap=0.03, seed=3)
        mat.move_to(RIGHT * 0.9 + DOWN * 0.3)
        wlab = MathTex(r"W_E", font_size=44, color=C.EMBED).next_to(mat, UP, buff=0.95)
        top_b = Brace(mat, UP, buff=0.1, color=GREY_B)
        top_l = label(r"50{,}257 columns: one per token", font_size=30, color=GREY_A).next_to(top_b, UP, buff=0.1)
        left_b = Brace(mat, LEFT, buff=0.1, color=GREY_B)
        left_l = label(r"768\\rows", font_size=30, color=GREY_A).next_to(left_b, LEFT, buff=0.1)
        wlab.next_to(top_l, UP, buff=0.2)
        cells = VGroup(*[mat.grid[r * cols + col] for r in range(rows)])
        hl = SurroundingRectangle(cells, color=YELLOW, buff=0.05, stroke_width=3)
        col_tag = TokenBox(" Paris", font_size=24, color=YELLOW).next_to(hl, DOWN, buff=0.15)
        paris = TokenBox(" Paris", font_size=32).move_to(LEFT * 6.0 + UP * col_tag.get_y())
        pid = MathTex(r"6342", font_size=34, color=GREY_A).next_to(paris, RIGHT, buff=0.3)

        with self.voiceover(
            "The first thing the model does with each token is look it up in a giant table, called the embedding matrix. "
            "<bookmark mark='c'/> It has one column for every token in the vocabulary, all 50,257 of them, "
            "<bookmark mark='r'/> and each column holds 768 numbers."
        ) as vo:
            self.play(FadeIn(paris), FadeIn(pid))
            self.play(FadeIn(mat.grid, lag_ratio=0.002), Create(mat.frame), FadeIn(wlab), run_time=2)
            vo.wait_until("c")
            self.play(GrowFromCenter(top_b), FadeIn(top_l))
            vo.wait_until("r")
            self.play(GrowFromCenter(left_b), FadeIn(left_l))

        vals = d["paris_vector"][:6]
        vec = num_column(vals, color=C.EMBED, font_size=30).move_to(RIGHT * 5.6 + DOWN * 0.3)
        vlab = label(r"768 numbers", font_size=30, color=C.EMBED).next_to(vec, DOWN, buff=0.25)
        arrow = Arrow(pid.get_right(), col_tag.get_left(), buff=0.2, color=GREY_B, stroke_width=3)
        with self.voiceover(
            "So the token Paris, number 6342, <bookmark mark='p'/> picks out its column, and becomes "
            "<bookmark mark='v'/> these 768 numbers: a vector. Nobody chooses these numbers by hand. They start out random "
            "and get tuned during training, like every other number in the model."
        ) as vo:
            vo.wait_until("p")
            self.play(GrowArrow(arrow), Create(hl), FadeIn(col_tag, shift=UP * 0.1))
            vo.wait_until("v")
            self.play(TransformFromCopy(cells, vec.entries), FadeIn(vec[0]), FadeIn(vec[2]), run_time=1.5)
            self.play(FadeIn(vlab))
        self.clear_scene()

        pieces = d["tokenize"][PROMPT + " Paris."]["pieces"][:-2]
        row = token_row(pieces, font_size=28, buff=0.12).to_edge(DOWN, buff=0.9)
        strips = VGroup(*[vector_strip(random_values(12, seed=i, scale=1.0), color=C.EMBED, cell=0.2).next_to(t, UP, buff=0.35)
                          for i, t in enumerate(row)])
        arrows = VGroup(*[Arrow(t.get_top(), s.get_bottom(), buff=0.06, color=GREY_B, stroke_width=2,
                                max_tip_length_to_length_ratio=0.3) for t, s in zip(row, strips)])
        note = label(r"(each column of cells stands for a vector of 768 numbers)", font_size=26, color=GREY_B)
        note.to_edge(UP, buff=0.5)
        with self.voiceover(
            "Every token in our sentence gets its own vector this way. I'll draw each one as a column of cells, "
            "standing in for its 768 numbers."
        ) as vo:
            self.play(FadeIn(row, lag_ratio=0.05))
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(s, shift=UP * 0.2)) for a, s in zip(arrows, strips)],
                                  lag_ratio=0.08), FadeIn(note), run_time=2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def clusters(self):
        g = self.d["groups"]
        xy = np.array(g["xy"])
        lo, hi = xy.min(0), xy.max(0)
        box_lo, box_hi = np.array([-5.6, -2.7]), np.array([4.0, 2.3])
        P = lambda p: np.array([*(box_lo + (p - lo) / (hi - lo) * (box_hi - box_lo)), 0])  # noqa: E731
        dots = VGroup(*[Dot(P(p), radius=0.1, color=C.EMBED) for p in xy])
        plane = NumberPlane(x_range=[-7, 7, 1], y_range=[-4, 4, 1], background_line_style={
            "stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.4}, axis_config={"stroke_opacity": 0})
        labels = VGroup()
        for name, title in GROUP_NAMES.items():
            idx = [i for i, lab in enumerate(g["labels"]) if lab == name]
            c = np.mean([P(xy[i]) for i in idx], axis=0)
            members = VGroup(*[dots[i] for i in idx])
            lab = label(title, font_size=32, color=WHITE)
            lab.add_background_rectangle(opacity=0.7, buff=0.05)
            lab.next_to(members, RIGHT, buff=0.3)
            if lab.get_right()[0] > 6.8:
                lab.next_to(members, LEFT, buff=0.3)
            labels.add(lab)
        days = [w.strip() for w, lab in zip(g["words"], g["labels"]) if lab == "days"]
        day_list = label(", ".join(days[:3]) + r",\\" + ", ".join(days[3:]), font_size=24, color=GREY_A)
        day_list.add_background_rectangle(opacity=0.7, buff=0.05)
        day_list.next_to(labels[1], DOWN, buff=0.12).align_to(labels[1], LEFT)
        title = label(r"GPT-2's real embeddings of 35 words, projected to 2D", font_size=32, color=GREY_A)
        title.to_corner(UR, buff=0.4)

        ex_col = num_column([2.0, 1.0], color=C.EMBED, font_size=40, decimals=1, dots=False).move_to(LEFT * 4.5 + UP * 1.5)
        ex_arrow = Arrow(ORIGIN, RIGHT * 2 + UP * 1, buff=0, color=C.EMBED, stroke_width=6)
        ex_dot = Dot(RIGHT * 2 + UP * 1, color=C.EMBED, radius=0.1)
        ex_note = label(r"2 numbers: a point in a plane", font_size=32)
        ex_note2 = label(r"768 numbers: a point in 768 dimensions", font_size=32)
        VGroup(ex_note, ex_note2).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(ex_col, DOWN, buff=0.3)
        VGroup(ex_note, ex_note2).to_edge(LEFT, buff=0.6)
        with self.voiceover(
            "A list of two numbers <bookmark mark='a'/> can be drawn as an arrow, or a point, in a plane. In the same way, "
            "<bookmark mark='b'/> a list of 768 numbers is a point in a space with 768 dimensions. We can't picture that, "
            "but we can project it down to two. <bookmark mark='p'/> Here are GPT-2's embeddings of 35 words, flattened "
            "onto the two directions in which they vary the most."
        ) as vo:
            self.play(FadeIn(plane), FadeIn(ex_col))
            vo.wait_until("a")
            self.play(GrowArrow(ex_arrow), FadeIn(ex_dot), FadeIn(ex_note))
            vo.wait_until("b")
            self.play(FadeIn(ex_note2))
            vo.wait_until("p")
            self.play(FadeOut(VGroup(ex_col, ex_arrow, ex_dot, ex_note, ex_note2)), FadeIn(title))
            self.play(LaggedStart(*[GrowFromCenter(dt) for dt in dots], lag_ratio=0.03), run_time=2)

        with self.voiceover(
            "Nobody told the model which words belong together. Yet <bookmark mark='a'/> the numbers land together, "
            "<bookmark mark='b'/> so do the days of the week, <bookmark mark='c'/> countries, <bookmark mark='d'/> "
            "animals, <bookmark mark='e'/> and colors. Words used in similar ways end up with similar vectors."
        ) as vo:
            for i, m in enumerate("abcde"):
                vo.wait_until(m)
                anims = [FadeIn(labels[i], shift=RIGHT * 0.1)]
                if i == 1:
                    anims.append(FadeIn(day_list))
                self.play(*anims, run_time=0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def analogy(self):
        a = self.d["analogy_plane"]
        assert self.d["analogies"]["king"][0][0] == " queen" and self.d["analogies"]["tokyo"][0][0] == " Tokyo"
        assert self.d["analogy_including_inputs"][0][0] == " king"
        S = 1.25
        O = np.array([-5.6, -2.3, 0])
        P = lambda w: O + S * np.array([a[w][0], a[w][1], 0])  # noqa: E731
        pairs = [(" man", " woman"), (" uncle", " aunt"), (" king", " queen")]
        dots, labs, arrows = VGroup(), VGroup(), VGroup()
        for m, f in pairs:
            for w in (m, f):
                dots.add(Dot(P(w), radius=0.09, color=C.EMBED))
                lab = label(w.strip(), font_size=34)
                lab.next_to(P(w), LEFT if w == m else RIGHT, buff=0.15)
                labs.add(lab)
            arrows.add(Arrow(P(m), P(f), buff=0.12, color=YELLOW, stroke_width=5))
        title = label(r"a 2D slice chosen to show it", font_size=28, color=GREY_B).move_to(O + UP * 5.2 + RIGHT * 1.5)

        with self.voiceover(
            "Directions in this space can carry meaning too. Here's a different slice through the same space, chosen to "
            "show this. <bookmark mark='a'/> The step from man to woman <bookmark mark='b'/> is nearly the same as the step "
            "from uncle to aunt, <bookmark mark='c'/> and from king to queen."
        ) as vo:
            self.play(FadeIn(title))
            for i, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(dots[2 * i:2 * i + 2]), FadeIn(labs[2 * i:2 * i + 2]), GrowArrow(arrows[i]), run_time=0.9)

        eq = MathTex(r"\text{king}", r"-", r"\text{man}", r"+", r"\text{woman}", r"\approx", r"\;?",
                     font_size=48).move_to(RIGHT * 3.3 + UP * 2.9)
        eq[0].set_color(C.EMBED)
        eq[2].set_color(C.EMBED)
        eq[4].set_color(C.EMBED)
        res = P("result")
        moved = arrows[0].copy().set_color(ORANGE)
        target = Arrow(P(" king"), res, buff=0.12, color=ORANGE, stroke_width=5)
        res_dot = Dot(res, radius=0.11, color=ORANGE)
        top = self.d["analogies"]["king"][:4]
        bars = ProbBars([t for t, _ in top], [s for _, s in top], max_width=2.6, scale_max=1.0, font_size=30,
                        percent=False, decimals=2, highlight=" queen", color=C.EMBED)
        btitle = label(r"closest tokens (cosine similarity),\\leaving out king, man and woman", font_size=28, color=GREY_A)
        btitle.next_to(eq, DOWN, buff=0.5)
        bars.next_to(btitle, DOWN, buff=0.35)

        with self.voiceover(
            "So try some arithmetic. <bookmark mark='k'/> Take the vector for king, subtract man, and add woman. "
            "<bookmark mark='s'/> Then search the whole vocabulary, leaving out the three words we started with, for the "
            "token whose vector points most nearly the same way. <bookmark mark='q'/> In GPT-2's real embeddings, the "
            "winner is queen."
        ) as vo:
            vo.wait_until("k")
            self.play(Write(eq), arrows[2].animate.set_opacity(0.25))
            self.play(moved.animate.move_to(target), run_time=1.2)
            self.play(FadeIn(res_dot), FadeOut(moved), FadeIn(target))
            vo.wait_until("s")
            self.play(FadeIn(btitle), FadeIn(bars.labels, lag_ratio=0.1))
            vo.wait_until("q")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars.bars], lag_ratio=0.1), FadeIn(bars.pcts))
            self.play(Indicate(bars.row(0), color=YELLOW, scale_factor=1.05))

        tokyo = MathTex(r"\text{Paris}", r"-", r"\text{France}", r"+", r"\text{Japan}", r"\approx",
                        r"\text{Tokyo}", font_size=44).to_edge(DOWN, buff=0.6).shift(RIGHT * 2.9)
        for i in (0, 2, 4, 6):
            tokyo[i].set_color(C.EMBED)
        tokyo[6].set_color(YELLOW)
        with self.voiceover(
            "The same trick takes you from Paris, minus France, plus Japan, <bookmark mark='t'/> to Tokyo. It doesn't "
            "work for every pair of words, but it's a striking sign that directions in this space can encode concepts, "
            "like gender, or 'capital city of'."
        ) as vo:
            self.play(Write(tokyo[:6]))
            vo.wait_until("t")
            self.play(Write(tokyo[6:]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def dot_product(self):
        O = LEFT * 3.6 + DOWN * 0.6
        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1], x_length=6, y_length=5,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.5},
                            axis_config={"stroke_color": GREY_C, "stroke_width": 1.5}).move_to(O)
        A = 2.2 * np.array([np.cos(0.35), np.sin(0.35), 0])
        theta = ValueTracker(0.75)
        Lb = 1.9

        def bvec():
            t = theta.get_value()
            return Lb * np.array([np.cos(t), np.sin(t), 0])

        a_arrow = Arrow(plane.c2p(0, 0), plane.c2p(*A[:2]), buff=0, color=C.EMBED, stroke_width=6)
        b_arrow = always_redraw(lambda: Arrow(plane.c2p(0, 0), plane.c2p(*bvec()[:2]), buff=0, color=BLUE_A, stroke_width=6))
        a_l = MathTex(r"\vec a", color=C.EMBED, font_size=40).next_to(a_arrow.get_end(), RIGHT, buff=0.1)
        b_l = always_redraw(lambda: MathTex(r"\vec b", color=BLUE_A, font_size=40).move_to(
            plane.c2p(*(bvec()[:2] * 1.18))))
        arc = always_redraw(lambda: Arc(radius=0.55, start_angle=0.35, angle=theta.get_value() - 0.35, color=GREY_A,
                                        arc_center=plane.c2p(0, 0)))

        f1 = MathTex(r"\vec a \cdot \vec b", r"=", r"a_1 b_1 + a_2 b_2 + \cdots + a_{768}\, b_{768}", font_size=40)
        f2 = MathTex(r"=", r"|\vec a|\,|\vec b|\,\cos\theta", font_size=40)
        f1.move_to(RIGHT * 3.0 + UP * 2.5)
        f2.next_to(f1, DOWN, buff=0.3).align_to(f1[1], LEFT)
        val = DecimalNumber(0, num_decimal_places=2, include_sign=True, font_size=48)
        val_l = MathTex(r"\vec a \cdot \vec b =", font_size=44)
        readout = VGroup(val_l, val).arrange(RIGHT, buff=0.2).move_to(RIGHT * 3.0 + UP * 0.4)
        val.set_value(float(A @ bvec()))
        val.add_updater(lambda m: m.set_value(float(A @ bvec())))
        val.add_updater(lambda m: m.set_color(GREEN if m.get_value() > 0.3 else (RED if m.get_value() < -0.3 else GREY_A)))
        word = always_redraw(lambda: label(
            r"aligned: positive" if A @ bvec() > 0.3 else (r"opposed: negative" if A @ bvec() < -0.3 else r"perpendicular: zero"),
            font_size=32, color=GREY_A).next_to(readout, DOWN, buff=0.3))

        with self.voiceover(
            "One operation will matter more than any other for the rest of this video: the dot product. "
            "<bookmark mark='f'/> Multiply two vectors entry by entry, and add up the results. "
            "<bookmark mark='g'/> Geometrically, it measures how much two vectors point the same way."
        ) as vo:
            self.play(FadeIn(plane), GrowArrow(a_arrow), FadeIn(a_l))
            self.add(b_arrow, b_l)
            vo.wait_until("f")
            self.play(Write(f1))
            vo.wait_until("g")
            self.play(Write(f2), FadeIn(arc))
            self.add(readout, word)

        with self.voiceover(
            "It's positive when they're <bookmark mark='a'/> aligned, <bookmark mark='p'/> zero when they're perpendicular, "
            "<bookmark mark='o'/> and negative when they point in opposite directions. Divide by the two lengths, and you "
            "get what's called the cosine similarity."
        ) as vo:
            vo.wait_until("a")
            self.play(theta.animate.set_value(0.45), run_time=1.0)
            vo.wait_until("p")
            self.play(theta.animate.set_value(0.35 + PI / 2), run_time=1.5)
            vo.wait_until("o")
            self.play(theta.animate.set_value(0.35 + 0.92 * PI), run_time=1.5)
            self.play(theta.animate.set_value(0.9), run_time=vo.remaining())

        sim = self.d["similarity"]
        keep = [" dog", " kitten", " banana", " democracy"]
        cos = [sim["cos"][sim["others"].index(w)] for w in keep]
        assert cos[0] > cos[2] and cos[1] > cos[3]
        bars = ProbBars(keep, cos, max_width=3.2, scale_max=0.6, font_size=30, percent=False, decimals=2, color=C.EMBED)
        bars.move_to(RIGHT * 3.2 + DOWN * 1.9)
        btitle = label(r"cosine similarity with \texttt{cat} in GPT-2", font_size=30, color=GREY_A).next_to(bars, UP, buff=0.3)
        with self.voiceover(
            "Measured on GPT-2's embeddings, <bookmark mark='c'/> cat is much more similar to dog and kitten than to banana, "
            "or to democracy. So tokens are now vectors, and similar tokens point in similar directions."
        ) as vo:
            self.play(FadeOut(VGroup(readout, word)), FadeOut(f2), f1.animate.scale(0.85).to_corner(UR, buff=0.45))
            vo.wait_until("c")
            self.play(FadeIn(btitle), FadeIn(bars.labels))
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars.bars], lag_ratio=0.15), FadeIn(bars.pcts))
        self.clear_scene()
