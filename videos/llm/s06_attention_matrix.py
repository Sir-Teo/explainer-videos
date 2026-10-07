from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.llm.common import (
    Mono, Plot, attention_grid, cell_at, data, display_token, label, show_chapter_card, softmax, token_row, vector_strip,
)


def mono(s: str, font_size=22) -> Mono:
    return Mono(display_token(s), font_size=font_size)


def cell_grid(rows, cols, color, cell=0.22, gap=0.03, values=None, seed=0, vmax=None) -> VGroup:
    """A matrix as a grid of cells; brightness from ``values`` (or random)."""
    if values is None:
        values = np.abs(np.random.default_rng(seed).normal(0, 0.5, (rows, cols)))
    values = np.asarray(values, dtype=float)
    vmax = vmax or (np.abs(values).max() + 1e-9)
    g = VGroup()
    for i in range(rows):
        for j in range(cols):
            a = min(1.0, abs(values[i, j]) / vmax)
            g.add(Square(cell, stroke_width=0, fill_color=color, fill_opacity=0.1 + 0.9 * a))
    g.arrange_in_grid(rows, cols, buff=gap)
    frame = SurroundingRectangle(g, buff=0.05, color=color, stroke_width=2, corner_radius=0.04)
    out = VGroup(g, frame)
    out.grid = g
    return out


FORMULA = [r"\text{Attention}(Q,K,V)", "=", r"\softmax\!\Big(", r"{", "Q", r"K^{\mathsf T}", r"\over", r"\sqrt{d_k}",
           r"}", "+", "M", r"\Big)", "V"]
F_LHS, F_EQ, F_SM, F_Q, F_K, F_OVER, F_SQRT, F_PLUS, F_M, F_CLOSE, F_V = 0, 1, 2, 4, 5, 6, 7, 9, 10, 11, 12


class AttentionMatrix(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 5, "Attention in matrix form, and many heads")
        self.d = data()
        self.matrix_form()
        self.sqrt_dk()
        self.multi_head()
        self.real_heads()
        self.induction_effect()

    # ------------------------------------------------------------------
    def matrix_form(self):
        h = self.d["bank_head"]
        P = h["pieces"]
        n = len(P)
        f = MathTex(*FORMULA, font_size=52).to_edge(UP, buff=0.35)
        f[F_Q].set_color(C.QUERY)
        f[F_K].set_color(C.KEY)
        f[F_V].set_color(C.VALUE)
        f[F_SQRT].set_color(YELLOW)
        f[F_M].set_color(RED)
        f[F_SM].set_color(C.ATTN)

        row = token_row(P, font_size=26, buff=0.25).move_to(LEFT * 2.0 + DOWN * 3.2)
        strips = VGroup(*[vector_strip(np.random.default_rng(i).normal(0, 1, 8), color=C.EMBED, cell=0.16, gap=0.03)
                          .next_to(t, UP, buff=0.25) for i, t in enumerate(row)])
        X = cell_grid(n, 8, C.EMBED, cell=0.2, seed=1).move_to(LEFT * 3.4 + DOWN * 0.2)
        X_l = MathTex("X", font_size=44, color=C.EMBED).next_to(X, UP, buff=0.15)
        X_rows = VGroup(*[mono(p) for p in P])
        for i, m in enumerate(X_rows):
            m.next_to(X.grid[i * 8], LEFT, buff=0.15)
        with self.voiceover(
            "In practice, all of this happens for every token at once. <bookmark mark='x'/> Stack the token vectors as the "
            "rows of one matrix, X."
        ) as vo:
            self.play(FadeIn(row), FadeIn(strips))
            vo.wait_until("x")
            self.play(*[ReplacementTransform(strips[i], VGroup(*X.grid[i * 8:(i + 1) * 8])) for i in range(n)],
                      ReplacementTransform(row, X_rows), run_time=1.6)
            self.play(Create(X[1]), FadeIn(X_l))

        mats = VGroup()
        for name, col, seed in [("Q", C.QUERY, 2), ("K", C.KEY, 3), ("V", C.VALUE, 4)]:
            m = cell_grid(n, 4, col, cell=0.2, seed=seed)
            lab = MathTex(f"{name} = X W_{name}", font_size=36, color=col).next_to(m, UP, buff=0.15)
            mats.add(VGroup(m, lab))
        mats.arrange(RIGHT, buff=0.6).next_to(X, RIGHT, buff=1.0)
        with self.voiceover(
            "Multiply X by W Q, and you get a matrix Q, holding every token's query in its rows. <bookmark mark='k'/> "
            "Likewise for the keys, <bookmark mark='v'/> and the values."
        ) as vo:
            self.play(TransformFromCopy(X[0], mats[0][0]), FadeIn(mats[0][1]))
            vo.wait_until("k")
            self.play(TransformFromCopy(X[0], mats[1][0]), FadeIn(mats[1][1]))
            vo.wait_until("v")
            self.play(TransformFromCopy(X[0], mats[2][0]), FadeIn(mats[2][1]))

        scores = np.array(h["scores"])
        S = cell_grid(n, n, C.ATTN, cell=0.36, values=scores - scores.min(), seed=0).move_to(RIGHT * 2.2 + DOWN * 1.0)
        S_l = MathTex(r"Q K^{\mathsf T}", font_size=40).next_to(S, UP, buff=0.15)
        S_l[0][0].set_color(C.QUERY)
        S_l[0][1:].set_color(C.KEY)
        S_note = label(r"every query $\cdot$ every key", font_size=28, color=GREY_A).next_to(S, DOWN, buff=0.2)
        with self.voiceover(
            "Now compare every query with every key in one go: <bookmark mark='s'/> that's Q times K transpose, a grid of "
            "scores with one row and one column for each token."
        ) as vo:
            self.play(FadeOut(X_rows), VGroup(X, X_l).animate.scale(0.75).to_edge(LEFT, buff=0.3).shift(UP * 1.2),
                      mats.animate.scale(0.75).move_to(LEFT * 1.6 + UP * 0.9))
            vo.wait_until("s")
            self.play(TransformFromCopy(VGroup(mats[0][0], mats[1][0]), S[0]), Create(S[1]), FadeIn(S_l), FadeIn(S_note),
                      FadeIn(f[F_Q]), FadeIn(f[F_K]), run_time=1.5)

        pattern = np.array(h["pattern"])
        A = attention_grid(pattern, P, cell=0.36, row_labels=False, col_labels=False).move_to(S)
        A_l = label(r"attention pattern", font_size=28, color=C.ATTN).next_to(A, DOWN, buff=0.2)
        with self.voiceover(
            "Then <bookmark mark='d'/> divide by the square root of d k, which we'll come back to in a moment. "
            "<bookmark mark='m'/> Add the mask, minus infinity everywhere a token would look ahead. <bookmark mark='sm'/> "
            "And apply softmax to each row. That gives the attention pattern."
        ) as vo:
            vo.wait_until("d")
            self.play(Write(f[F_OVER]), Write(f[F_SQRT]), FadeIn(f[3]), FadeIn(f[8]))
            vo.wait_until("m")
            masked = VGroup(*[S[0][i * n + j] for i in range(n) for j in range(i + 1, n)])
            self.play(Write(f[F_PLUS]), Write(f[F_M]), masked.animate.set_fill(GREY_E, opacity=0.4))
            vo.wait_until("sm")
            self.play(Write(f[F_SM]), Write(f[F_CLOSE]), ReplacementTransform(S[0], A.cells), FadeOut(S[1]),
                      ReplacementTransform(S_note, A_l), run_time=1.5)

        out = cell_grid(n, 4, C.VALUE, cell=0.2, seed=9).next_to(A, RIGHT, buff=0.9)
        times = MathTex(r"\times", font_size=40).move_to((A.get_right() + out.get_left()) / 2 + LEFT * 0.0)
        vcopy = mats[2][0].copy()
        out_l = label(r"each row: that token's\\weighted sum of values", font_size=24, color=GREY_A).next_to(out, DOWN, 0.2)
        with self.voiceover(
            "Finally, <bookmark mark='v'/> multiply by V. Each row of the result is one token's weighted sum of values: "
            "its update. <bookmark mark='f'/> That's the whole attention formula from the 2017 paper, and now every piece "
            "of it should make sense."
        ) as vo:
            vo.wait_until("v")
            self.play(vcopy.animate.next_to(A, RIGHT, buff=0.9), FadeIn(times), Write(f[F_V]))
            self.play(ReplacementTransform(vcopy, out), FadeIn(out_l))
            vo.wait_until("f")
            self.play(Write(f[F_LHS]), Write(f[F_EQ]))
            self.play(Circumscribe(f, color=YELLOW, buff=0.15))
        self.formula = f
        self.clear_scene(f)

    # ------------------------------------------------------------------
    def sqrt_dk(self):
        f = self.formula
        rng = np.random.default_rng(4)
        raw = rng.normal(0, 8.0, 6)
        b1 = softmax(raw)
        b2 = softmax(raw / 8)

        def bars(p, title_tex, color):
            pl = Plot((0, 6), (0, 1), width=4.2, height=2.6, y_ticks=[0, 0.5, 1], y_fmt=lambda v: f"{v:g}")
            rects = VGroup()
            for i, v in enumerate(p):
                r = Rectangle(width=0.5, height=max(0.01, 2.6 * v), stroke_width=0, fill_color=color, fill_opacity=0.85)
                r.move_to(pl.c2p(i + 0.5, 0), aligned_edge=DOWN)
                rects.add(r)
            t = label(title_tex, font_size=30, color=GREY_A).next_to(pl, UP, buff=0.3)
            return VGroup(pl, rects, t)

        left = bars(b1, r"scores of typical size 8: softmax", C.ATTN).move_to(LEFT * 3.4 + DOWN * 1.4)
        right = bars(b2, r"divided by $\sqrt{64} = 8$: softmax", C.ATTN).move_to(RIGHT * 3.4 + DOWN * 1.4)
        sum_t = MathTex(r"\vec q \cdot \vec k", "=", r"q_1 k_1 + q_2 k_2 + \cdots + q_{64} k_{64}", font_size=40)
        sum_t.move_to(UP * 1.6)
        size_t = label(r"64 random terms $\Rightarrow$ typical size $\sqrt{64} = 8$", font_size=32, color=YELLOW)
        size_t.next_to(sum_t, DOWN, buff=0.3)
        with self.voiceover(
            "So why divide by the square root of d k? <bookmark mark='d'/> d k is the length of each query and key: 64 in "
            "GPT-2. <bookmark mark='s'/> A dot product adds up 64 products, and if those are random-ish numbers around one "
            "in size, the sum typically lands around plus or minus eight: the square root of 64."
        ) as vo:
            self.play(f.animate.scale(0.75).to_edge(UP, buff=0.25))
            vo.wait_until("d")
            self.play(Indicate(f[F_SQRT], color=YELLOW, scale_factor=1.3))
            vo.wait_until("s")
            self.play(Write(sum_t))
            self.play(FadeIn(size_t, shift=UP * 0.2))

        with self.voiceover(
            "Feed scores that large into softmax, <bookmark mark='l'/> and nearly all the weight piles onto a single token, "
            "which makes training slow and unstable. <bookmark mark='r'/> Divide by eight, and the weights stay spread "
            "out enough to learn from."
        ) as vo:
            vo.wait_until("l")
            self.play(FadeIn(left[0]), FadeIn(left[2]), LaggedStart(*[GrowFromEdge(r, DOWN) for r in left[1]], lag_ratio=0.1))
            vo.wait_until("r")
            self.play(FadeIn(right[0]), FadeIn(right[2]), LaggedStart(*[GrowFromEdge(r, DOWN) for r in right[1]], lag_ratio=0.1))
        self.clear_scene()

    # ------------------------------------------------------------------
    def multi_head(self):
        L5 = self.d["layer5_heads"]
        pats = np.array(L5["patterns"])
        grids = VGroup(*[attention_grid(pats[k], L5["pieces"], cell=0.13, row_labels=False, col_labels=False)
                         for k in range(12)])
        for k, g in enumerate(grids):
            g.add(SurroundingRectangle(g.cells, color=GREY_D, buff=0.03, stroke_width=1))
        grids.arrange_in_grid(2, 6, buff=(0.45, 0.6)).move_to(UP * 0.6)
        hl = VGroup(*[MathTex(f"h_{{{k + 1}}}", font_size=28, color=GREY_A).next_to(g, DOWN, buff=0.1)
                      for k, g in enumerate(grids)])
        title = label(r"the 12 heads of GPT-2's layer 6, on our sentence (real)", font_size=30, color=GREY_A)
        title.to_edge(UP, buff=0.3)
        sizes = MathTex(r"12 \text{ heads} \times 64 = 768", font_size=40).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "A single attention pattern can only capture one kind of relationship at a time. So each layer runs several "
            "attention heads in parallel, each with its own query, key and value matrices. <bookmark mark='h'/> GPT-2 small "
            "has 12 heads in every layer. <bookmark mark='d'/> Each works with queries and keys of 64 numbers, and 12 times "
            "64 is 768."
        ) as vo:
            self.play(FadeIn(title), LaggedStart(*[FadeIn(g, scale=0.9) for g in grids], lag_ratio=0.25), run_time=4)
            vo.wait_until("h")
            self.play(FadeIn(hl, lag_ratio=0.1))
            vo.wait_until("d")
            self.play(Write(sizes))

        outs = VGroup(*[Rectangle(width=0.28, height=1.6, stroke_width=1.5, stroke_color=C.VALUE, fill_color=C.VALUE,
                                  fill_opacity=0.15 + 0.06 * k) for k in range(12)]).arrange(RIGHT, buff=0)
        outs.move_to(LEFT * 2.6 + DOWN * 2.35)
        cat_l = label(r"12 head outputs, side by side", font_size=26, color=GREY_A).next_to(outs, UP, buff=0.15)
        wo = MathTex(r"\times\, W_O", font_size=44, color=C.ATTN).next_to(outs, RIGHT, buff=0.4)
        arrow = Arrow(wo.get_right(), wo.get_right() + RIGHT * 1.2, buff=0.1, color=GREY_B)
        delta = vector_strip(np.random.default_rng(5).normal(0, 1, 8), color=C.ATTN, cell=0.17).next_to(arrow, RIGHT, 0.2)
        d_l = label(r"one update per token,\\added to the residual stream", font_size=26, color=GREY_A)
        d_l.next_to(delta, RIGHT, buff=0.25)
        params = MathTex(r"4 \times 768 \times 768 \approx 2.4 \text{ million parameters per layer}", font_size=34)
        params.to_edge(DOWN, buff=0.3).shift(RIGHT * 0.5)
        pc = self.d["params"]["attention_per_layer"]
        assert 2.3e6 < pc < 2.4e6
        with self.voiceover(
            "Each head produces its own update for each token. <bookmark mark='c'/> These are placed side by side, "
            "<bookmark mark='o'/> and multiplied by one more matrix, W O, which mixes them into a single update, added to "
            "the residual stream. <bookmark mark='p'/> With the four matrices W Q, W K, W V and W O, that's about 2.4 "
            "million parameters per attention layer."
        ) as vo:
            self.play(FadeOut(sizes), VGroup(grids, hl).animate.scale(0.75).shift(UP * 0.85))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(o, shift=DOWN * 0.3) for o in outs], lag_ratio=0.08), FadeIn(cat_l), run_time=1.5)
            vo.wait_until("o")
            self.play(Write(wo), GrowArrow(arrow), FadeIn(delta), FadeIn(d_l))
            vo.wait_until("p")
            self.play(Write(params))
        self.clear_scene()

    # ------------------------------------------------------------------
    def show_head(self, head: dict, text: str, cell: float, center=LEFT * 2.6 + DOWN * 0.3):
        g = attention_grid(np.array(head["pattern"]), head["pieces"], cell=cell, font_size=22).move_to(center)
        t = label(text, font_size=30, color=GREY_A).to_corner(UL, buff=0.35)
        return g, t

    def real_heads(self):
        d = self.d
        ph = d["prev_head"]
        g, t = self.show_head(ph, rf"previous-token head (layer {ph['layer'] + 1}, head {ph['head'] + 1})", 0.4)
        pat = np.array(ph["pattern"])
        assert np.mean(np.diag(pat, -1)) > 0.95 and ph["layer"] + 1 == 5  # narration: "in layer 5"
        rnd = np.tril(np.random.default_rng(2).random(pat.shape) ** 3)
        rnd /= rnd.sum(1, keepdims=True)
        g0 = attention_grid(rnd, ph["pieces"], cell=0.4, row_labels=False, col_labels=False).move_to(g.cells)
        intro = label(r"Nobody designs these heads.\\They emerge from training.", font_size=36).move_to(RIGHT * 4.0)
        with self.voiceover(
            "So what do real heads actually do? Nobody designs them: <bookmark mark='r'/> their matrices start out random, "
            "<bookmark mark='t'/> and whatever they end up doing emerges from training. Here are three from GPT-2."
        ) as vo:
            vo.wait_until("r")
            self.play(FadeIn(g0.cells, lag_ratio=0.005), FadeIn(intro))
            vo.wait_until("t")
            self.play(ReplacementTransform(g0.cells, g.cells), run_time=2.5)
        self.play(FadeOut(intro))

        note = label(r"each token looks at\\the token just before it", font_size=32, color=C.ATTN).move_to(RIGHT * 4.3)
        with self.voiceover(
            "This one, in layer 5, sends almost all of each token's attention <bookmark mark='p'/> to the token immediately "
            "before it. It copies information about the previous token into each position. That sounds trivial, but "
            "it turns out to be a building block for something cleverer."
        ) as vo:
            self.play(FadeIn(t), FadeIn(g.row_labels), FadeIn(g.col_labels))
            vo.wait_until("p")
            self.play(FadeIn(note))
        self.clear_scene()

        sh = d["sink_head"]
        g, t = self.show_head(sh, rf"a head that parks on the first token (layer {sh['layer'] + 1}, head {sh['head'] + 1})", 0.4)
        frac = sh["frac_heads_mostly_first"]
        assert 0.6 < frac < 0.75
        note = label(r"about two thirds of GPT-2's heads\\put most of their attention on the\\first token of this sentence",
                     font_size=30, color=C.ATTN).move_to(RIGHT * 4.2)
        with self.voiceover(
            "Many heads look like this one: nearly all of their attention lands <bookmark mark='f'/> on the very first "
            "token. On this sentence, about two thirds of GPT-2's heads put most of their weight there. It seems to be "
            "a resting place: since the weights must add up to one, a head with nothing useful to contribute parks its "
            "attention on the first token, which contributes very little."
        ) as vo:
            self.play(FadeIn(t), FadeIn(g.row_labels), FadeIn(g.col_labels), FadeIn(g.cells, lag_ratio=0.005), run_time=1.5)
            vo.wait_until("f")
            self.play(FadeIn(note))
        self.clear_scene()

        ih = d["induction_head"]
        pat = np.array(ih["pattern"])
        m = len(pat) // 2
        g, t = self.show_head(ih, rf"induction head (layer {ih['layer'] + 1}, head {ih['head'] + 1})", 0.4)
        i_row = m + 1  # second "river"
        j_col = 2  # the token that followed the first "river"
        assert ih["pieces"][i_row] == ih["pieces"][1] == " river" and pat[i_row, j_col] > 0.4
        box_r = SurroundingRectangle(VGroup(*[cell_at(g, i_row, j) for j in range(i_row + 1)]), color=YELLOW, buff=0.03)
        box_c = SurroundingRectangle(cell_at(g, i_row, j_col), color=YELLOW, buff=0.05, stroke_width=4)
        lab1 = SurroundingRectangle(g.row_labels[i_row], color=YELLOW, buff=0.05)
        lab2 = SurroundingRectangle(g.col_labels[j_col], color=YELLOW, buff=0.05)
        lab0 = SurroundingRectangle(g.col_labels[1], color=GREY_B, buff=0.05)
        note = label(r"``Last time I saw \emph{river},\\\emph{lamp} came next.''", font_size=34, color=YELLOW)
        note.move_to(RIGHT * 4.3 + UP * 0.6)
        rule = label(r"an \emph{induction head}", font_size=34, color=C.ATTN).next_to(note, DOWN, buff=0.5)
        with self.voiceover(
            "The third is the most interesting. Feed in a short list of words, then repeat it. <bookmark mark='s'/> On the "
            "second pass, at each word, this head looks back at <bookmark mark='n'/> the word that came right after that "
            "same word's first appearance. <bookmark mark='r'/> When it reaches river the second time, it looks at lamp, "
            "the word that followed river last time. It's called an induction head."
        ) as vo:
            self.play(FadeIn(t), FadeIn(g.row_labels), FadeIn(g.col_labels), FadeIn(g.cells, lag_ratio=0.005), run_time=1.5)
            vo.wait_until("s")
            stripe = VGroup(*[cell_at(g, i, i - m + 1) for i in range(m + 1, 2 * m)])
            self.play(Indicate(stripe, color=YELLOW, scale_factor=1.15), run_time=1.5)
            vo.wait_until("r")
            self.play(Create(box_r), Create(lab1), Create(lab0))
            self.play(Create(box_c), Create(lab2), FadeIn(note))
            self.play(FadeIn(rule))

        with self.voiceover(
            "Its rule amounts to: if this word appeared before, attend to whatever came after it, and predict that again. "
            "It relies on a previous-token head from an earlier layer, like the first one we saw, to know what preceded "
            "each word."
        ) as vo:
            pass
        self.clear_scene()

    # ------------------------------------------------------------------
    def induction_effect(self):
        il = self.d["induction_loss"]
        words = il["words"]
        p = np.exp(-np.array(il["losses"]))
        m = len(words)
        assert p[:m - 1].mean() < 0.01 and p[m:].mean() > 0.6
        T = len(p)
        pl = Plot((0, T), (0, 1), width=11.5, height=3.6, y_ticks=[0, 0.5, 1], y_fmt=lambda v: f"{int(v * 100)}\\%")
        pl.move_to(DOWN * 0.6)
        bars = VGroup()
        for i, v in enumerate(p):
            col = GREY_B if i < m - 1 else C.PROB
            r = Rectangle(width=11.5 / T * 0.75, height=max(0.02, 3.6 * v), stroke_width=0, fill_color=col, fill_opacity=0.9)
            r.move_to(pl.c2p(i + 0.5, 0), aligned_edge=DOWN)
            bars.add(r)
        mid = DashedLine(pl.c2p(m - 0.5, 0), pl.c2p(m - 0.5, 1.05), color=GREY_A, stroke_width=2)
        first = label(r"first time through", font_size=30, color=GREY_A).move_to(pl.c2p(m / 2, 0.75))
        second = label(r"the same list again", font_size=30, color=C.PROB).move_to(pl.c2p(1.5 * m, 1.12))
        ylab = label(r"probability GPT-2 gave each word, just before it appeared", font_size=28, color=GREY_A)
        ylab.next_to(pl, UP, buff=0.7).align_to(pl, LEFT)
        seq = " ".join(w.strip() for w in words[:8])
        seq_t = mono(seq + " ...", font_size=24).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Watch what that does to GPT-2's predictions. <bookmark mark='l'/> Here's a random list of 20 words, followed by "
            "the same list again. For each word, the bar shows the probability GPT-2 gave it, just before it appeared. "
            "<bookmark mark='f'/> The first time through, the words are random, so every bar is tiny."
        ) as vo:
            self.play(Create(pl), FadeIn(ylab))
            vo.wait_until("l")
            self.play(FadeIn(seq_t))
            vo.wait_until("f")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[:m - 1]], lag_ratio=0.05), FadeIn(first),
                      run_time=1.5)

        with self.voiceover(
            "<bookmark mark='s'/> The second time, it predicts almost every word. It has picked up a pattern from its own "
            "context, something it was never explicitly taught. This is a simple form of what's called in-context "
            "learning, and induction heads seem to be one of its basic mechanisms."
        ) as vo:
            vo.wait_until("s")
            self.play(Create(mid), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[m - 1:]], lag_ratio=0.05),
                      FadeIn(second), run_time=2)
        self.clear_scene()

