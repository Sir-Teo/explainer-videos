from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.llm.common import (
    attention_arcs, attention_grid, cell_at, cell_matrix, data, label, random_values, show_chapter_card,
    softmax, token_row, vector_strip,
)


def strip(seed, color, n=6, cell=0.17):
    return vector_strip(random_values(n, seed=seed), color=color, cell=cell, gap=0.03)


class AttentionIdea(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 4, "Attention: letting tokens talk")
        h = data()["bank_head"]
        self.pieces = h["pieces"]
        self.pattern = np.array(h["pattern"])
        self.scores = np.array(h["scores"])[-1]
        self.weights = self.pattern[-1]
        assert self.pieces[4] == " river" and self.weights[4] > 0.5 and np.argmax(self.scores) == 4
        assert np.allclose(softmax(self.scores), self.weights, atol=1e-3)
        self.single_query()
        self.cartoon()
        self.whole_pattern()

    # ------------------------------------------------------------------
    def single_query(self):
        P, w, sc = self.pieces, self.weights, self.scores
        n = len(P)
        row = token_row(P, font_size=30, buff=0.36).to_edge(DOWN, buff=0.35)
        row.shift(RIGHT * (-6.7 - row.get_left()[0]))
        xs = [t.get_x() for t in row]
        emb = VGroup(*[strip(i, C.EMBED, n=8).move_to([x, -2.0, 0]) for i, x in enumerate(xs)])
        bank, bank_x = row[-1], emb[-1]
        title = label(r"one attention head, from the point of view of ``bank''", font_size=30, color=GREY_A)
        title.to_corner(UL, buff=0.35)
        ask = label(r"``Is there anything earlier that tells\\me what kind of bank I am?''", font_size=30, color=C.QUERY)
        ask.to_corner(UR, buff=0.35)
        PX = 4.7  # center of the right-hand math panel

        with self.voiceover(
            "Let's zoom in on a single attention step, from the point of view of the token bank. "
            "<bookmark mark='q'/> Bank would like to ask a question: is there anything earlier in the text that tells me "
            "what kind of bank I am?"
        ) as vo:
            self.play(FadeIn(row), FadeIn(emb, shift=UP * 0.2), FadeIn(title))
            self.play(bank.animate.set_color(YELLOW), bank_x.animate.set_stroke(YELLOW, 3))
            vo.wait_until("q")
            self.play(FadeIn(ask, shift=DOWN * 0.2))

        # W_Q x = q
        wq = cell_matrix(5, 8, C.QUERY, cell=0.2, gap=0.03, seed=11, label_tex=r"W_Q", font_size=44)
        xcopy = strip(5, C.EMBED, n=8, cell=0.2)
        eq = MathTex("=", font_size=52)
        q = strip(21, C.QUERY, n=5, cell=0.2)
        VGroup(wq, xcopy, eq, q).arrange(RIGHT, buff=0.3).move_to(RIGHT * PX + UP * 0.3)
        q_l = MathTex(r"\vec q", font_size=44, color=C.QUERY).next_to(q, UP, buff=0.15)
        dims = label(r"$64 \times 768$", font_size=28, color=GREY_B).next_to(wq, DOWN, buff=0.15)
        qdim = label(r"64 numbers", font_size=28, color=GREY_B).next_to(q, DOWN, buff=0.15)
        with self.voiceover(
            "It encodes that question as a vector, called a query, <bookmark mark='m'/> by multiplying its own vector by a "
            "matrix, called W Q. <bookmark mark='s'/> The query is shorter: in GPT-2, just 64 numbers."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(wq), TransformFromCopy(bank_x, xcopy), FadeIn(dims))
            self.play(Write(eq), TransformFromCopy(VGroup(wq.grid, xcopy), q), FadeIn(q_l))
            vo.wait_until("s")
            self.play(FadeIn(qdim))

        # Legend that builds up in the right panel.
        def entry(tex, name, color):
            g = VGroup(label(name, font_size=32, color=color), MathTex(tex, font_size=38, color=color)).arrange(RIGHT, buff=0.3)
            return g

        q_small = strip(21, C.QUERY, n=5, cell=0.14)
        e_q = VGroup(q_small, entry(r"\vec q = W_Q\,\vec x", "query", C.QUERY)).arrange(RIGHT, buff=0.3)
        e_k = entry(r"\vec k = W_K\,\vec x", "keys", C.KEY)
        e_s = entry(r"s = \vec q \cdot \vec k", "score", C.ATTN)
        legend = VGroup(e_q, e_k, e_s).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([PX, 1.5, 0])
        legend.align_to(RIGHT * 2.55, LEFT)

        keys = VGroup(*[strip(30 + i, C.KEY, n=5).move_to([x, -0.15, 0]) for i, x in enumerate(xs)])
        k_arrows = VGroup(*[Arrow(e.get_top(), k.get_bottom(), buff=0.06, color=C.KEY, stroke_width=2,
                                  max_tip_length_to_length_ratio=0.3) for e, k in zip(emb, keys)])
        with self.voiceover(
            "Meanwhile, every token, including bank itself, produces a key, <bookmark mark='k'/> using a second matrix, "
            "W K. Think of a key as an advertisement: here's what I have to offer."
        ) as vo:
            self.play(FadeOut(VGroup(ask, dims, qdim, wq, xcopy, eq, q_l)), ReplacementTransform(q, q_small),
                      FadeIn(e_q[1]))
            vo.wait_until("k")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(k, shift=UP * 0.2)) for a, k in zip(k_arrows, keys)],
                                  lag_ratio=0.1), FadeIn(e_k), run_time=2)

        # Dot products.
        nums = VGroup(*[DecimalNumber(v, num_decimal_places=2, include_sign=True, font_size=30, color=C.ATTN)
                        .next_to(k, UP, buff=0.18) for v, k in zip(sc, keys)])
        with self.voiceover(
            "Bank's query is compared with every key, using a dot product. A higher score means a better match. "
            "<bookmark mark='r'/> These are real numbers, from one of the attention heads in GPT-2's very first layer, "
            "<bookmark mark='h'/> and river has the highest score."
        ) as vo:
            self.play(FadeIn(e_s))
            vo.wait_until("r")
            for i in range(n):
                qc = q_small.copy()
                self.play(qc.animate.next_to(keys[i], UP, buff=0.05), run_time=0.35)
                self.play(FadeOut(qc, scale=0.5), FadeIn(nums[i], scale=1.3), run_time=0.3)
            vo.wait_until("h")
            self.play(Indicate(nums[4], color=YELLOW, scale_factor=1.3), Indicate(row[4], color=YELLOW))

        # Softmax.
        sm = MathTex(r"w_j", r"=", r"{e^{\,s_j} \over \sum_k e^{\,s_k}}", font_size=44)
        sm[0].set_color(C.ATTN)
        sm_name = label(r"softmax", font_size=32, color=C.ATTN)
        smg = VGroup(sm_name, sm).arrange(RIGHT, buff=0.3).next_to(legend, DOWN, buff=0.4).align_to(legend, LEFT)
        pct = VGroup(*[DecimalNumber(100 * x, num_decimal_places=0, unit=r"\%", font_size=34, color=C.ATTN)
                       .move_to(m) for x, m in zip(w, nums)])
        arcs = attention_arcs(VGroup(*[p.copy().shift(UP * 0.05) for p in pct]), n - 1, w, max_width=12, min_weight=0.0)
        with self.voiceover(
            "To turn scores into weights, the model uses a function called softmax. <bookmark mark='e'/> It raises e to the "
            "power of each score, which makes everything positive and exaggerates the differences, then divides by the "
            "total, so the weights add up to one. <bookmark mark='w'/> Now, sixty percent of bank's attention goes to river."
        ) as vo:
            self.play(FadeIn(smg, shift=UP * 0.2))
            vo.wait_until("e")
            self.play(*[ReplacementTransform(a, b) for a, b in zip(nums, pct)], run_time=1.5)
            vo.wait_until("w")
            self.play(Create(arcs, lag_ratio=0.1), Indicate(pct[4], color=YELLOW, scale_factor=1.3), run_time=1.5)

        # Values and the weighted sum.
        vals = VGroup(*[strip(60 + i, C.VALUE, n=8).move_to(k) for i, k in enumerate(keys)])
        e_v = entry(r"\vec v = W_V\,\vec x", "values", C.VALUE).next_to(smg, DOWN, buff=0.4).align_to(legend, LEFT)
        with self.voiceover(
            "So what actually gets passed along? <bookmark mark='v'/> Each token also produces a third vector, its value, "
            "using a third matrix, W V. The value is the information a token hands over to anyone who attends to it."
        ) as vo:
            vo.wait_until("v")
            self.play(*[ReplacementTransform(a, b) for a, b in zip(keys, vals)], FadeOut(k_arrows), FadeIn(e_v),
                      e_k.animate.set_opacity(0.35), run_time=1.5)

        formula = MathTex(r"\Delta", r"=", r"\textstyle\sum_j", r"w_j", r"\,\vec v_j", font_size=44)
        formula[0].set_color(C.VALUE)
        formula[3].set_color(C.ATTN)
        formula[4].set_color(C.VALUE)
        delta = strip(77, C.VALUE, n=8)
        VGroup(delta, formula).arrange(RIGHT, buff=0.35).next_to(e_v, DOWN, buff=0.45).align_to(legend, LEFT)
        scaled = VGroup(*[v.copy().set_opacity(0.15 + 0.85 * x) for v, x in zip(vals, w)])
        new_x = strip(8, C.EMBED, n=8).move_to(bank_x)
        plus = MathTex("+", font_size=48).next_to(bank_x, RIGHT, buff=0.2)
        with self.voiceover(
            "Bank's update is a weighted sum of all the values, <bookmark mark='s'/> mostly river's value, plus a little of "
            "the others. <bookmark mark='a'/> And that update gets added to bank's vector."
        ) as vo:
            vo.wait_until("s")
            self.play(*[s.animate.move_to(delta).set_opacity(0.4) for s in scaled], run_time=1.5)
            self.play(FadeOut(scaled), FadeIn(delta), Write(formula))
            vo.wait_until("a")
            dc = delta.copy()
            self.play(dc.animate.scale(0.7).next_to(plus, RIGHT, buff=0.15), FadeIn(plus), run_time=1.0)
            self.play(FadeOut(dc, target_position=bank_x), FadeOut(plus), Transform(bank_x, new_x), run_time=1.0)
            self.play(Indicate(bank_x, color=YELLOW))
        self.clear_scene()

    # ------------------------------------------------------------------
    def cartoon(self):
        O = LEFT * 1.0 + DOWN * 1.8
        money = Arrow(O, O + 3.6 * RIGHT, buff=0, color=GREY_B, stroke_width=3)
        river = Arrow(O, O + 3.6 * UP, buff=0, color=GREY_B, stroke_width=3)
        ml = label(r"``money''", font_size=32, color=GREY_A).next_to(money, RIGHT, buff=0.15)
        rl = label(r"``riverside''", font_size=32, color=GREY_A).next_to(river, UP, buff=0.15)
        b0 = O + np.array([2.2, 1.7, 0])
        bank = Arrow(O, b0, buff=0, color=C.EMBED, stroke_width=6)
        bl = label(r"bank, from the lookup table", font_size=32, color=C.EMBED)
        d = np.array([-1.5, 1.3, 0])
        dv = Arrow(b0, b0 + d, buff=0, color=C.VALUE, stroke_width=6)
        dl = MathTex(r"\Delta", font_size=44, color=C.VALUE).next_to(dv.get_center(), UR, buff=0.12)
        b1 = Arrow(O, b0 + d, buff=0, color=YELLOW, stroke_width=6)
        b1l = label(r"bank, after attention\\(in ``river bank'')", font_size=32, color=YELLOW)
        b1l.move_to(RIGHT * 4.6 + UP * 1.0)
        bl.move_to(RIGHT * 4.6 + DOWN * 0.4)
        tag = label(r"(cartoon: real directions are learned, and far less tidy)", font_size=26, color=GREY_B)
        tag.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In a cartoon picture: if one direction in the space meant money, and another meant riverside, "
            "<bookmark mark='b'/> bank's starting vector would sit somewhere in between. <bookmark mark='d'/> The update "
            "from attention nudges it toward the riverside meaning."
        ) as vo:
            self.play(GrowArrow(money), GrowArrow(river), FadeIn(ml), FadeIn(rl), FadeIn(tag))
            vo.wait_until("b")
            self.play(GrowArrow(bank), FadeIn(bl))
            vo.wait_until("d")
            self.play(GrowArrow(dv), FadeIn(dl))
            self.play(GrowArrow(b1), FadeIn(b1l))
        self.clear_scene()

    # ------------------------------------------------------------------
    def whole_pattern(self):
        P, W = self.pieces, self.pattern
        n = len(P)
        grid = attention_grid(W, P, cell=0.72, font_size=28, causal=True).move_to(LEFT * 1.3 + DOWN * 0.35)
        rows_l = label(r"each row: one token\\looking back", font_size=28, color=GREY_A)
        rows_l.next_to(grid, RIGHT, buff=0.6).shift(UP * 0.6)
        sums = label(r"each row adds up to 1", font_size=28, color=GREY_A).next_to(rows_l, DOWN, buff=0.5)
        sums.align_to(rows_l, LEFT)
        title = label(r"the attention pattern of this head (real: GPT-2, first layer)", font_size=30, color=GREY_A)
        title.to_edge(UP, buff=0.3)
        bank_row = VGroup(*[cell_at(grid, n - 1, j) for j in range(n)])
        row_box = SurroundingRectangle(bank_row, color=YELLOW, buff=0.05)
        with self.voiceover(
            "Every token does this at the same time, each with its own query. <bookmark mark='g'/> Collect all the weights "
            "in a grid, and you get what's called an attention pattern. <bookmark mark='r'/> Each row is one token looking "
            "back over the text, and each row adds up to one. <bookmark mark='b'/> The bottom row is bank, with river "
            "lit up."
        ) as vo:
            vo.wait_until("g")
            self.play(FadeIn(title), FadeIn(grid.row_labels), FadeIn(grid.col_labels),
                      LaggedStart(*[FadeIn(c) for c in grid.cells], lag_ratio=0.01), run_time=2)
            vo.wait_until("r")
            self.play(FadeIn(rows_l), FadeIn(sums))
            vo.wait_until("b")
            self.play(Create(row_box))

        masked = VGroup(*[cell_at(grid, i, j) for i in range(n) for j in range(i + 1, n)])
        tri = Polygon(cell_at(grid, 0, 1).get_corner(UL), cell_at(grid, 0, n - 1).get_corner(UR),
                      cell_at(grid, n - 2, n - 1).get_corner(DR), color=RED, stroke_width=3)
        infs = VGroup(*[MathTex(r"-\infty", font_size=24, color=RED).move_to(cell_at(grid, i, j))
                        for i in range(n) for j in range(i + 1, n)])
        rule = MathTex(r"e^{-\infty} = 0", font_size=40, color=RED).next_to(sums, DOWN, buff=0.6).align_to(sums, LEFT)
        with self.voiceover(
            "The gray triangle is off limits: <bookmark mark='t'/> a token may never look at tokens that come after it. "
            "In practice, <bookmark mark='i'/> those scores are set to minus infinity before the softmax, so their weights "
            "come out as exactly zero. This is the rule we met earlier, and we'll see why it matters when we get to "
            "training."
        ) as vo:
            self.play(FadeOut(row_box))
            vo.wait_until("t")
            self.play(Create(tri), masked.animate.set_fill(RED, opacity=0.15))
            vo.wait_until("i")
            self.play(FadeIn(infs, lag_ratio=0.05), Write(rule))
        self.clear_scene()


