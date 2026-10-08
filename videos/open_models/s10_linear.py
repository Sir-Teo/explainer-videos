from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.open_models.common import (
    PLANE_SCALE, cfg, label, model_tag, show_chapter_card, vec_arrow,
)
from videos.open_models.toys import overwrite_demo


class LinearMemory(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 9, "Kimi: a memory that never grows")
        self.tag = model_tag("kimi")
        self.add(self.tag)
        self.derive()
        self.write_read()
        self.geometry()

    # ------------------------------------------------------------------
    def derive(self):
        k = cfg("kimi")
        assert k["layer_types"].count("kda") == 69 and k["layers"] == 93 and k["kda_head_dim"] == 128
        intro = label(r"69 of Kimi K3's 93 layers keep no cache of past tokens at all", font_size=32).to_edge(UP, buff=0.9)
        e1 = MathTex(r"\vec o", "=", r"\sum_s", r"\operatorname{softmax}", r"(\vec q \cdot \vec k_s)", r"\,\vec v_s",
                     font_size=52)
        e2 = MathTex(r"\vec o", "=", r"\sum_s", r"(\vec q \cdot \vec k_s)", r"\,\vec v_s", font_size=52)
        e3 = MathTex(r"\vec o", "=", r"\sum_s", r"\vec v_s", r"\,(\vec k_s^{\top} \vec q)", font_size=52)
        e4 = MathTex(r"\vec o", "=", r"\Big(\sum_s \vec v_s \vec k_s^{\top}\Big)", r"\vec q", font_size=52)
        e5 = MathTex(r"\vec o", "=", r"S", r"\,\vec q", font_size=60)
        for e in (e1, e2, e3, e4, e5):
            e.move_to(UP * 0.4)
        for e in (e1, e2, e3, e4, e5):
            for part in e:
                tex = part.get_tex_string()
                if r"\vec q" in tex and r"\vec k" not in tex and r"\vec v" not in tex:
                    part.set_color(C.QUERY)
        e5[2].set_color(C.MEMORY)
        e4[2].set_color(C.MEMORY)
        notes = [
            label(r"attention, for one query: weigh every value by how well its key matches", font_size=28, color=GREY_A),
            label(r"drop the softmax: use the raw match as the weight", font_size=28, color=GREY_A),
            label(r"a dot product is a row times a column", font_size=28, color=GREY_A),
            label(r"regroup: one matrix, built from every (value, key) pair", font_size=28, color=GREY_A),
            label(r"$S$ is the memory", font_size=32, color=C.MEMORY),
        ]
        for n in notes:
            n.next_to(e1, DOWN, buff=0.7)
        with self.voiceover(
            "Kimi K3 takes the most radical route. <bookmark mark='q'/> In 69 of its 93 layers, there's no cache of past "
            "tokens at all. Instead, each head keeps a single matrix of fixed size, a memory, which it updates as each "
            "token streams past. To see how that can possibly work, let's build it from scratch. <bookmark mark='a'/> "
            "Start with what attention does for one query: weigh every value by how well its key matches the query, and "
            "add them up."
        ) as vo:
            vo.wait_until("q")
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(Write(e1), FadeIn(notes[0]))
        with self.voiceover(
            "<bookmark mark='d'/> Now drop the softmax, and use the raw dot products as the weights. <bookmark mark='r'/> "
            "Each dot product can be written as a row times a column, <bookmark mark='g'/> and then the whole sum "
            "regroups into a single matrix, the sum over every token of its value times its key, an outer product, "
            "applied to the query. <bookmark mark='s'/> That matrix, S, is the memory."
        ) as vo:
            vo.wait_until("d")
            self.play(TransformMatchingTex(e1, e2), Transform(notes[0], notes[1]))
            vo.wait_until("r")
            self.play(TransformMatchingTex(e2, e3), Transform(notes[0], notes[2]))
            vo.wait_until("g")
            self.play(TransformMatchingTex(e3, e4), Transform(notes[0], notes[3]), run_time=1.5)
            vo.wait_until("s")
            self.play(TransformMatchingTex(e4, e5), Transform(notes[0], notes[4]), run_time=1.2)
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def write_read(self):
        n = 8
        rng = np.random.default_rng(5)
        v = rng.normal(size=n)
        kk = rng.normal(size=n)
        col = VGroup(*[Square(0.32, stroke_width=0, fill_color=C.VALUE, fill_opacity=0.25 + 0.7 * min(1, abs(x) / 2))
                       for x in v]).arrange(DOWN, buff=0.04)
        row = VGroup(*[Square(0.32, stroke_width=0, fill_color=C.KEY, fill_opacity=0.25 + 0.7 * min(1, abs(x) / 2))
                       for x in kk]).arrange(RIGHT, buff=0.04)
        outer = np.outer(v, kk)
        mat = VGroup(*[Square(0.32, stroke_width=0, fill_color=C.MEMORY, fill_opacity=0.15 + 0.8 * min(1, abs(x) / 3))
                       for x in outer.ravel()]).arrange_in_grid(n, n, buff=0.04)
        col.move_to(LEFT * 4.6 + DOWN * 0.3)
        row.next_to(col, RIGHT, buff=0.6).align_to(col, UP).shift(UP * 0.6)
        mat.next_to(row, DOWN, buff=0.25).align_to(row, LEFT)
        row.align_to(mat, LEFT)
        col.align_to(mat, UP)
        vl = MathTex(r"\vec v", font_size=40, color=C.VALUE).next_to(col, UP, buff=0.15)
        kl = MathTex(r"\vec k^{\top}", font_size=40, color=C.KEY).next_to(row, RIGHT, buff=0.15)
        wr = MathTex(r"\text{write: }", r"S", r"\;\mathrel{+}=\;", r"\vec v\, \vec k^{\top}", font_size=40)
        wr[1].set_color(C.MEMORY)
        rd = MathTex(r"\text{read: }", r"\vec o = S\,\vec q", font_size=40)
        size = label(r"for Kimi K3: $128 \times 128$ numbers per head,\\whether it has read ten tokens\\or a million",
                     font_size=28, color=C.MEMORY)
        VGroup(wr, rd, size).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(RIGHT * 3.3 + UP * 0.2)
        with self.voiceover(
            "<bookmark mark='w'/> Writing a token into memory means adding its value times its key: a column times a row, "
            "which makes a whole grid of products. <bookmark mark='r'/> Reading means multiplying the memory by a query. "
            "<bookmark mark='f'/> And no matter how many tokens go in, S stays the same size: for Kimi's heads, 128 by 128 "
            "numbers."
        ) as vo:
            vo.wait_until("w")
            self.play(FadeIn(col), FadeIn(vl), FadeIn(row), FadeIn(kl), Write(wr))
            self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in mat], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("r")
            self.play(Write(rd))
            vo.wait_until("f")
            self.play(FadeIn(size, shift=UP * 0.2))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def geometry(self):
        d = overwrite_demo()
        plane = NumberPlane(x_range=[-2, 2, 1], y_range=[-1.6, 1.6, 1], x_length=4 * PLANE_SCALE * 1.4,
                            y_length=3.2 * PLANE_SCALE * 1.4,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.6},
                            axis_config={"stroke_color": GREY_B}).move_to(LEFT * 2.6 + DOWN * 0.3)
        k1 = vec_arrow(plane, d["k1"], C.KEY)
        k2 = vec_arrow(plane, d["k2"], C.KEY)
        v1 = vec_arrow(plane, d["v1"], C.VALUE)
        v2 = vec_arrow(plane, d["v2"], C.VALUE)
        k1l = MathTex(r"\vec k_1", font_size=34, color=C.KEY).next_to(k1.get_end(), DOWN, buff=0.1)
        k2l = MathTex(r"\vec k_2", font_size=34, color=C.KEY).next_to(k2.get_end(), RIGHT, buff=0.1)
        v1l = MathTex(r"\vec v_1", font_size=34, color=C.VALUE).next_to(v1.get_end(), UR, buff=0.05)
        v2l = MathTex(r"\vec v_2", font_size=34, color=C.VALUE).next_to(v2.get_end(), LEFT, buff=0.1)
        S1 = d["steps"]["linear"][0]
        S2 = d["steps"]["linear"][1]
        S3 = d["steps"]["linear"][2]
        r1 = S1 @ d["k1"]
        r2 = S2 @ d["k1"]
        r3 = S3 @ d["k1"]
        assert np.allclose(r1, d["v1"]) and np.linalg.norm(r2 - d["v1"]) > 0.05
        read1 = vec_arrow(plane, r1, C.MEMORY, 6)
        read2 = vec_arrow(plane, r2, C.MEMORY, 6)
        read3 = vec_arrow(plane, r3, C.MEMORY, 6)
        side = VGroup()
        t1 = MathTex(r"S = \vec v_1 \vec k_1^{\top}", font_size=36)
        t2 = MathTex(r"S\vec k_1 = \vec v_1 \;\checkmark", font_size=36, color=C.MEMORY)
        t3 = MathTex(r"S = \vec v_1 \vec k_1^{\top} + \vec v_2 \vec k_2^{\top}", font_size=36)
        t4 = MathTex(r"S\vec k_1 = \vec v_1 + (\vec k_2\cdot\vec k_1)\,\vec v_2", font_size=36, color=C.MEMORY)
        smudge = label(r"a smudge, because $\vec k_1$ and $\vec k_2$\\aren't perpendicular", font_size=26, color=GREY_A)
        side.add(t1, t2, t3, t4, smudge).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.7 + UP * 0.6)
        with self.voiceover(
            "Think of S as a lookup table built out of geometry. Here it is in two dimensions. "
            "<bookmark mark='k1'/> Store a key pointing this way, with this value. <bookmark mark='r1'/> Read with the same "
            "key, and out comes exactly that value. <bookmark mark='k2'/> Now store a second pair. <bookmark mark='x'/> "
            "Reading the first key again gives the first value, plus a little of the second, because the two keys aren't "
            "perpendicular. <bookmark mark='n'/> In 128 dimensions there's room for many nearly perpendicular keys, but "
            "every association you add leaves a small smudge on all the others."
        ) as vo:
            self.play(Create(plane), run_time=1.0)
            vo.wait_until("k1")
            self.play(GrowArrow(k1), FadeIn(k1l), GrowArrow(v1), FadeIn(v1l), Write(t1))
            vo.wait_until("r1")
            self.play(TransformFromCopy(k1, read1), run_time=1.2)
            self.play(Write(t2))
            vo.wait_until("k2")
            self.play(FadeOut(read1), GrowArrow(k2), FadeIn(k2l), GrowArrow(v2), FadeIn(v2l), Write(t3))
            vo.wait_until("x")
            self.play(TransformFromCopy(k1, read2), run_time=1.2)
            self.play(Write(t4), FadeIn(smudge))
        v1b = vec_arrow(plane, d["v1b"], YELLOW)
        v1bl = MathTex(r"\vec v_1'", font_size=34, color=YELLOW).next_to(v1b.get_end(), DOWN, buff=0.1)
        t5 = MathTex(r"S \mathrel{+}= \vec v_1' \vec k_1^{\top}", font_size=36)
        t6 = MathTex(r"S\vec k_1 = \vec v_1 + \vec v_1' + \text{smudge}", font_size=36, color=C.MEMORY)
        blend = label(r"a blend of the old and the new", font_size=28, color=RED)
        VGroup(t5, t6, blend).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(side, aligned_edge=UL)
        with self.voiceover(
            "And there's a worse problem. <bookmark mark='o'/> Suppose a fact changes: the same key gets a new value, like "
            "a variable in a program being reassigned. <bookmark mark='p'/> The plain sum just piles the new value on top "
            "of the old one. <bookmark mark='b'/> Reading it back gives a blend of old and new."
        ) as vo:
            self.play(FadeOut(side), FadeOut(read2))
            vo.wait_until("o")
            self.play(GrowArrow(v1b), FadeIn(v1bl))
            vo.wait_until("p")
            self.play(Write(t5))
            vo.wait_until("b")
            self.play(TransformFromCopy(k1, read3), run_time=1.2)
            self.play(Write(t6), FadeIn(blend))
        self.clear_scene()
