from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import MONO, VOWELS, load

LETTERS = "abcdefghijklmnopqrstuvwxyz"


def heat(M, size=3.6, vmax=None, color=C.TRUE_P) -> VGroup:
    """A matrix as a square of cells, brightness by value (negative values dark)."""
    n = M.shape[0]
    vmax = vmax or float(M.max())
    c = size / n
    dark, lit = ManimColor("#121826"), ManimColor(color)
    g = VGroup()
    for i in range(n):
        for j in range(n):
            v = float(np.clip(M[i, j] / vmax, 0, 1)) ** 0.7
            g.add(Square(side_length=c, stroke_width=0, fill_color=interpolate_color(dark, lit, v), fill_opacity=1)
                  .move_to([-size / 2 + (j + 0.5) * c, size / 2 - (i + 0.5) * c, 0]))
    return g


class LowRank(VoiceoverScene):
    def construct(self):
        self.card()
        self.pieces()
        self.letters()
        self.vowels()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"Keeping what matters", r"What is the best simple version of a matrix?", part=2)
        with self.voiceover("Chapter six. Keeping what matters."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def pieces(self):
        colors = {r"\sigma_1": C.BITS, r"\sigma_2": C.BITS, r"\sigma_3": C.BITS, r"\mathbf{u}_1": C.TRUE_P,
                  r"\mathbf{u}_2": C.TRUE_P, r"\mathbf{u}_3": C.TRUE_P, r"\mathbf{v}_1^{\top}": C.MODEL_Q,
                  r"\mathbf{v}_2^{\top}": C.MODEL_Q, r"\mathbf{v}_3^{\top}": C.MODEL_Q}
        f = cmath("A", "=", r"\sigma_1", r"\mathbf{u}_1", r"\mathbf{v}_1^{\top}", "+", r"\sigma_2", r"\mathbf{u}_2",
                  r"\mathbf{v}_2^{\top}", "+", r"\sigma_3", r"\mathbf{u}_3", r"\mathbf{v}_3^{\top}", "+", r"\cdots",
                  colors=colors, font_size=50).to_edge(UP, buff=0.6)
        # one piece: a column times a row
        g = np.random.default_rng(1)
        u, v = np.abs(g.normal(size=8)) + 0.2, np.abs(g.normal(size=8)) + 0.2
        cell = 0.36
        col = VGroup(*[Square(cell, stroke_width=0, fill_color=C.TRUE_P, fill_opacity=0.25 + 0.75 * x / u.max())
                       .move_to([-4.6, 1.25 - k * cell, 0]) for k, x in enumerate(u)])
        row = VGroup(*[Square(cell, stroke_width=0, fill_color=C.MODEL_Q, fill_opacity=0.25 + 0.75 * x / v.max())
                       .move_to([-3.7 + k * cell, 1.95, 0]) for k, x in enumerate(v)])
        grid = VGroup(*[Square(cell, stroke_width=0.5, stroke_color=BACKGROUND, fill_color=C.BITS,
                               fill_opacity=0.15 + 0.85 * (u[i] * v[j]) / (u.max() * v.max()))
                        .move_to([-3.7 + j * cell, 1.25 - i * cell, 0]) for i in range(8) for j in range(8)])
        times = MathTex(r"\times", font_size=40).move_to([-4.6, 1.95, 0])
        cap = label(r"one piece: \ a column times a row \ (rank $1$)", font_size=28, color=GREY_A).move_to([-2.5, -1.9, 0])
        ey = label(r"the $k$ biggest pieces: \ the closest matrix of rank $k$", font_size=34, color=C.BITS)
        ey.move_to([0, -2.9, 0])
        cite_ = cite(r"C.~Eckart \& G.~Young, \textit{Psychometrika} (1936)", corner=DR)
        rk = MathTex(r"\text{rank } 2: \quad \mathbf{u}_1 \mathbf{v}_1^{\top} + \mathbf{u}_2 \mathbf{v}_2^{\top}", font_size=34)
        rk_card = gloss(r"rank", r"how many column-times-row pieces\\ it takes to build the table; \ "
                        r"\textit{low rank}: \ a few do", picture=rk, width=4.6)
        rk_card.move_to([3.7, 0.4, 0])
        with self.voiceover(
            "There's more. Written out, the decomposition says that any matrix is a sum of simple pieces, "
            "<bookmark mark='a'/> each one a column times a row, weighted by a singular value. How many pieces a "
            "table needs is its rank, and a low-rank table is one that a few pieces build. <bookmark mark='b'/> "
            "Keep the k biggest pieces, drop the rest, and you get the closest possible matrix built from only k "
            "pieces. No other choice comes closer. That's the Eckart–Young theorem, from 1936."
        ) as vo:
            self.play(Write(f), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(col), FadeIn(row), FadeIn(times))
            self.play(LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.01), FadeIn(cap), run_time=1.5)
            self.play(FadeIn(rk_card))
            vo.wait_until("b")
            self.play(FadeIn(ey), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def letters(self):
        d = load("letters")
        M, S, recon, err = np.asarray(d["M"]), np.asarray(d["S"]), np.asarray(d["recon"]), np.asarray(d["err"])
        assert abs(d["total"] - 1) < 1e-9 and abs(err[0] - 0.557) < 0.001 and abs(err[1] - 0.399) < 0.001
        vmax = float(M.max())
        left = heat(M, size=3.6, vmax=vmax).move_to([-4.3, 0.55, 0])
        lt = label(r"the letter-pair table", font_size=26, color=GREY_A).next_to(left, UP, buff=0.18)
        rows_l = VGroup(*[Text(c, font=MONO, font_size=11, color=GREY_B).next_to(left[26 * i], LEFT, buff=0.06)
                          for i, c in enumerate(LETTERS)])
        right = heat(recon[0], size=3.6, vmax=vmax).move_to([0.2, 0.55, 0])
        rt = MathTex(r"\text{rank } 1", font_size=34, color=C.BITS).next_to(right, UP, buff=0.18)
        # the singular values, kept and dropped
        bw = 0.15
        bars = VGroup(*[Rectangle(width=bw * 0.8, height=3.2 * s / S[0], stroke_width=0, fill_color=C.BITS, fill_opacity=0.9)
                        .move_to([3.0 + k * bw, -0.8 + 1.6 * s / S[0], 0]) for k, s in enumerate(S)])
        bl = label(r"singular values", font_size=24, color=GREY_A).next_to(bars, UP, buff=0.15)
        er_l = MathTex(r"\text{error} =", font_size=34)
        er_v = DecimalNumber(err[0], num_decimal_places=2, font_size=34, color=C.SURPRISE)
        er = VGroup(er_l, er_v).arrange(RIGHT, buff=0.15).move_to([4.8, -1.7, 0])
        note_ = label(r"the table is the square root of $P(\text{previous}, \text{next})$; \ its total size is $1$",
                      font_size=22, color=GREY_B).to_edge(DOWN, buff=0.35)

        def keep(k):
            return [b.animate.set_fill(opacity=0.9 if i < k else 0.18) for i, b in enumerate(bars)]

        with self.voiceover(
            "Here's a real matrix: part one's table of letter pairs, twenty-six letters by twenty-six. "
            "<bookmark mark='a'/> The first piece alone already has the broad shape: it's the table you'd get if the "
            "next letter didn't care what came before. <bookmark mark='b'/> Add the second piece, the third, the "
            "fifth, the tenth, <bookmark mark='c'/> and the error falls by exactly the singular values left out: "
            "0.56 of the whole after one piece, 0.40 after two."
        ) as vo:
            self.play(FadeIn(left), FadeIn(lt), FadeIn(rows_l), FadeIn(note_))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(bl), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(right), FadeIn(rt), *keep(1), FadeIn(er))
            vo.wait_until("b")
            for k in (2, 3, 5, 10):
                new = heat(recon[k - 1], size=3.6, vmax=vmax).move_to(right)
                nt = MathTex(rf"\text{{rank }} {k}", font_size=34, color=C.BITS).move_to(rt)
                self.play(Transform(right, new), Transform(rt, nt), *keep(k), ChangeDecimalToValue(er_v, err[k - 1]),
                          run_time=0.9)
            vo.wait_until("c")
            self.play(Indicate(er, color=C.SURPRISE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vowels(self):
        d = load("letters")
        row = np.asarray(d["ca_row"])
        order = np.argsort(row)
        assert sorted(LETTERS[i] for i in order[:5]) == sorted(VOWELS)
        lo, hi = float(row.min()), float(row.max())
        W = 12.0

        def X(v):
            return -W / 2 + W * (v - lo) / (hi - lo)

        axis = Line([-W / 2 - 0.2, -0.4, 0], [W / 2 + 0.2, -0.4, 0], color=GREY_C, stroke_width=2)
        marks, labs = VGroup(), VGroup()
        for k, i in enumerate(order):
            ch = LETTERS[i]
            vow = ch in VOWELS
            x = X(row[i])
            y = -0.4 + [0.45, -0.45, 0.95, -0.95][k % 4]
            marks.add(Line([x, -0.55, 0], [x, -0.25, 0], color=C.BITS if vow else GREY_B, stroke_width=3))
            labs.add(Text(ch, font=MONO, font_size=34, color=C.BITS if vow else WHITE).move_to([x, y, 0]))
        vow_box = SurroundingRectangle(VGroup(*[labs[k] for k in range(5)]), color=C.BITS, buff=0.15, corner_radius=0.1)
        head = label(r"Each letter, placed by the table's strongest departure from independence", font_size=30)
        head.to_edge(UP, buff=0.6)
        tag = label(r"correspondence analysis: \ the SVD of $\dfrac{P(x, y) - P(x)P(y)}{\sqrt{P(x)P(y)}}$", font_size=26,
                    color=GREY_A).to_edge(DOWN, buff=0.5)
        found = label(r"vowels and consonants take turns", font_size=34, color=C.BITS).move_to(DOWN * 2.0)
        dep = gloss(r"departure from independence", r"each pair's count, minus the count you'd expect\\ if letters "
                    r"ignored each other: \ only the surprise is kept", width=6.0)
        dep.move_to(UP * 1.75)
        with self.voiceover(
            "The pieces mean something, too. <bookmark mark='a'/> Take the way the table departs from independence: "
            "compare each count with what you'd expect if letters ignored their neighbours, and keep only the "
            "surprise. Spread the letters out along its strongest direction. <bookmark mark='b'/> At one end: i, a, "
            "o, u, e. No one told the computer what a vowel is. From counts alone, it found that vowels and consonants "
            "take turns."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(axis), FadeIn(tag), FadeIn(dep))
            self.play(LaggedStart(*[AnimationGroup(Create(m), FadeIn(t, shift=DOWN * 0.1)) for m, t in zip(marks, labs)],
                                  lag_ratio=0.06), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeOut(dep), Create(vow_box), *[Indicate(labs[k], color=C.BITS, scale_factor=1.4) for k in range(5)])
            self.play(FadeIn(found))
        self.wait(0.3)
        self.clear_scene()
