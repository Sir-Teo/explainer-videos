from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import A, K, MONO, PART, Q, V, char_row, load

FUT = "#080B11"


def mask_grid(M, cell=0.26, on=A, off=FUT, cross=None, stroke=GREY_D) -> VGroup:
    """A 0/1 matrix as a grid of squares: lit where a query (row) may look at a key (column)."""
    n, m = M.shape
    g = VGroup()
    for i in range(n):
        for j in range(m):
            col = on if M[i, j] else off
            if cross is not None and cross[i, j]:
                col = C.EMBED
            g.add(Square(cell, stroke_width=0.6, stroke_color=stroke, fill_color=col,
                         fill_opacity=0.85 if M[i, j] else 1).move_to([j * cell, -i * cell, 0]))
    return g


class Masks(VoiceoverScene):
    def construct(self):
        self.card()
        self.causal()
        self.shapes()
        self.order()

    def card(self):
        card = chapter_card(5, r"Who may look at whom", r"How does one pass train every position at once?",
                            lit=(2017, 2018), part=PART)
        with self.voiceover("Chapter five. Who may look at whom."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def causal(self):
        h = load("heads")
        word = "the cat sat"
        n = len(word)
        g = np.random.default_rng(4)
        S = g.normal(size=(n, n)).round(1)
        cell = 0.42
        grid = VGroup()
        for i in range(n):
            for j in range(n):
                sq = Square(cell, stroke_width=0.8, stroke_color=GREY_D, fill_color=A,
                            fill_opacity=float(0.15 + 0.5 * (S[i, j] - S.min()) / np.ptp(S)))
                grid.add(sq.move_to([j * cell, -i * cell, 0]))
        grid.move_to([-3.6, -0.4, 0])
        rl = VGroup(*[data_text(ch if ch != " " else "_", font=MONO, font_size=20, color=Q)
                      .next_to(grid[i * n], LEFT, buff=0.15) for i, ch in enumerate(word)])
        cl = VGroup(*[data_text(ch if ch != " " else "_", font=MONO, font_size=20, color=K)
                      .next_to(grid[j], UP, buff=0.12) for j, ch in enumerate(word)])
        ql = label(r"queries", font_size=22, color=Q).next_to(rl, LEFT, buff=0.2).rotate(PI / 2)
        kl = label(r"keys", font_size=22, color=K).next_to(cl, UP, buff=0.15)
        future = VGroup(*[grid[i * n + j] for i in range(n) for j in range(n) if j > i])
        tag = note(r"illustrative scores").next_to(grid, DOWN, buff=0.2)
        eqs = VGroup(cmath(r"S_{ij}", r"\;\leftarrow\;", r"S_{ij} + M_{ij}", font_size=34),
                     cmath(r"M_{ij}", r"=", r"\begin{cases} 0 & j \le i \\ -\infty & j > i \end{cases}", font_size=32),
                     cmath(r"e^{-\infty}", r"=", r"0", font_size=32)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        eqs.move_to([2.6, 2.0, 0])
        teach = label(rf"one pass over ${n}$ characters: \ ${n}$ predictions, \\ each made from its own past only",
                      font_size=22, color=GREY_A).move_to([2.6, 0.15, 0])
        mp, mf, nm = float(h["mask_past"]), float(h["mask_future"]), float(h["nomask_past"])
        past_txt = "exactly zero" if mp == 0 else ("rounding error" if mp < 1e-4 else f"{mp:.4f}")
        chk = VGroup(
            label(r"our transformer: \ change characters $65$--$128$ of a passage", font_size=22, color=WHITE),
            label(rf"its guesses at $1$--$64$ move by \ ${'0' if mp == 0 else sci(mp)}$", font_size=22, color=C.TRUE_P),
            label(rf"at $65$--$128$ \ by up to ${mf:.1f}$", font_size=22, color=GREY_A),
            label(rf"with the mask removed, \ $1$--$64$ move by ${nm:.1f}$", font_size=22, color=C.SURPRISE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([2.6, -2.15, 0])
        keep_in_frame(chk)
        with self.voiceover(
            "A language model guesses each character from the ones before it, so attention must not see the "
            "future. <bookmark mark='a'/> Here is a grid of scores: one row for each query, one column for each "
            "key. <bookmark mark='b'/> Add minus infinity to every score above the diagonal. The exponential of "
            "minus infinity is zero, so the softmax gives the future no weight at all. This is the causal mask. "
            f"<bookmark mark='c'/> Its gift is speed in training. One pass over {n} characters makes {n} "
            "guesses at once, each from its own past only, so every position is a training example. "
            "<bookmark mark='d'/> Check it on our transformer: change the second half of a passage, and its guesses "
            f"in the first half move by {past_txt}, while the second half's change by up to {mf:.1f}. Take the "
            f"mask away and the first half moves by {nm:.1f}: the model would be reading the answers."
        ) as vo:
            self.play(FadeIn(eqs[0]))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(rl), FadeIn(cl), FadeIn(ql), FadeIn(kl), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1:]), *[sq.animate.set_fill(FUT, opacity=1) for sq in future], run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(teach))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for c_ in chk], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shapes(self):
        n = 8
        full = np.ones((n, n), bool)
        tri = np.tril(full)
        pref = tri.copy()
        pref[:, :4] = True
        pref = pref & np.ones((n, n), bool)
        cell = 0.24
        enc = mask_grid(full, cell)
        dec = mask_grid(tri, cell)
        pre = mask_grid(pref, cell)
        # encoder-decoder: the decoder's own triangle, and a rectangle of cross-attention to the source
        src = 6
        ed_self = mask_grid(np.tril(np.ones((n, n), bool)), cell)
        ed_cross = mask_grid(np.ones((n, src), bool), cell, on=C.EMBED)
        ed = VGroup(ed_cross, ed_self).arrange(RIGHT, buff=0.15)
        panels = VGroup()
        specs = [(enc, r"encoder", r"every position sees all \\ (BERT; \ Part 14)", A),
                 (dec, r"decoder", r"each sees its past \\ (GPT; \ this series' models)", A),
                 (ed, r"encoder--decoder", r"the target's past, \\ plus the whole source \\ (the 2017 translator)",
                  C.EMBED),
                 (pre, r"prefix LM", r"a prompt read both ways, \\ then left to right", A)]
        for grid, name, desc, col in specs:
            t = label(name, font_size=26, color=col)
            dsc = label(desc, font_size=19, color=GREY_A)
            panels.add(VGroup(t, grid, dsc).arrange(DOWN, buff=0.22))
        panels.arrange(RIGHT, buff=0.55, aligned_edge=UP).move_to([0, 0.9, 0])
        if panels.width > 13.4:
            panels.scale_to_fit_width(13.4)
        cross = VGroup(cmath(r"q", r"\text{ from the target}, \quad", r"k, v", r"\text{ from the source}", font_size=30,
                             colors={r"q": Q, r"k, v": K}),
                       label(r"cross-attention: \ the translation looks back at the sentence it translates",
                             font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15).move_to([0, -2.4, 0])
        with self.voiceover(
            "The mask is the only difference between the three ways the transformer has been cut. "
            "<bookmark mark='a'/> An encoder lets every position see every other: it reads, but cannot write left "
            "to right. <bookmark mark='b'/> A decoder uses the causal triangle: it writes, one token at a time. "
            "<bookmark mark='c'/> The 2017 paper's translator had both. Its decoder looks at its own past, and "
            "through cross-attention at the whole source sentence: the queries come from the translation, the keys "
            "and values from the encoder's reading of the original. <bookmark mark='d'/> A prefix language model "
            "reads its prompt both ways and writes the rest left to right. Which of these won, and why, is the "
            "story of Part 14."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p_) for p_ in panels], lag_ratio=0.25), run_time=2.0)
            self.play(*[p_.animate.set_opacity(0.3) for p_ in panels[1:]])
            vo.wait_until("a")
            self.play(Indicate(panels[0][0]))
            vo.wait_until("b")
            self.play(panels[0].animate.set_opacity(0.3), panels[1].animate.set_opacity(1))
            vo.wait_until("c")
            self.play(panels[1].animate.set_opacity(0.3), panels[2].animate.set_opacity(1), FadeIn(cross))
            vo.wait_until("d")
            self.play(panels[2].animate.set_opacity(0.3), panels[3].animate.set_opacity(1))
            self.play(*[p_.animate.set_opacity(1) for p_ in panels[:3]])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def order(self):
        h = load("heads")
        dev, scale = float(h["perm_dev"]), float(h["perm_scale"])
        words = ["dog", "bites", "man"]
        blind = ("blind to order, to rounding error." if dev < 1e-4 * scale else
                 f"nearly blind to order: its outputs move by only {dev:.3f}.")

        def row(order, y):
            g = VGroup(*[VGroup(RoundedRectangle(width=1.5, height=0.7, corner_radius=0.1, stroke_color=K, stroke_width=2),
                                data_text(words[i], font=MONO, font_size=28, color=WHITE)) for i in order])
            for b in g:
                b[1].move_to(b[0])
            return g.arrange(RIGHT, buff=0.4).move_to([-3.2, y, 0])

        r1 = row([0, 1, 2], 1.7)
        r2 = row([2, 1, 0], 1.7)
        qd = VGroup(Circle(radius=0.32, color=Q, stroke_width=3), MathTex(r"q", font_size=32, color=Q)).move_to([-3.2, -0.5, 0])
        w = [0.5, 0.2, 0.3]

        def lines(r, order):
            return VGroup(*[Line(qd.get_top(), b.get_bottom(), color=A, stroke_width=2 + 14 * w[i])
                            for b, i in zip(r, order)])

        l1 = lines(r1, [0, 1, 2])
        out = label(r"$0.5\,v_{\mathrm{dog}} + 0.2\,v_{\mathrm{bites}} + 0.3\,v_{\mathrm{man}}$", font_size=28, color=V)
        out.next_to(qd, DOWN, buff=0.45)
        tag = note(r"illustrative weights").next_to(out, DOWN, buff=0.2)
        eq = cmath(r"\operatorname{Attn}(P X)", r"=", r"P\,\operatorname{Attn}(X)", font_size=36).move_to([3.6, 1.6, 0])
        eql = label(r"permute the inputs, \\ and the outputs are permuted \\ the same way: \ nothing else changes",
                    font_size=22, color=GREY_A).next_to(eq, DOWN, buff=0.3)
        chk = label(rf"our transformer, mask and rotations removed, \\ $128$ characters shuffled: \\ outputs agree to "
                    rf"${sci(dev)}$ \ (of values up to ${scale:.0f}$)", font_size=20, color=C.TRUE_P)
        chk.next_to(eql, DOWN, buff=0.4)
        with self.voiceover(
            "One more property, and a problem. Attention averages over a set. <bookmark mark='a'/> Each word gets "
            "its weight from its key, wherever it sits. <bookmark mark='b'/> So 'dog bites man' and 'man bites "
            "dog' give exactly the same average. <bookmark mark='c'/> In symbols: permute the inputs, and the "
            "outputs are permuted the same way. Without a mask and without positions, our own transformer is "
            + blind + " <bookmark mark='d'/> The model must be told where each "
            "character is. That is chapter eight. The causal mask already leaks a little of it, and we will see how."
        ) as vo:
            self.play(FadeIn(r1), FadeIn(qd), FadeIn(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in l1], lag_ratio=0.2), FadeIn(out), FadeIn(tag))
            vo.wait_until("b")
            l2 = lines(r2, [2, 1, 0])
            self.play(*[r1[i].animate.move_to(r2[j]) for i, j in ((0, 2), (2, 0))], Transform(l1, l2), run_time=1.5,
                      path_arc=PI / 3)
            self.play(Indicate(out, color=V))
            vo.wait_until("c")
            self.play(FadeIn(eql), FadeIn(chk))
            vo.wait_until("d")
            self.play(Indicate(r1, color=K, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
