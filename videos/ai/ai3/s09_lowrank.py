from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, MONO, VOWELS, chapter, dots_on, framed, gray_image, load

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
        chapter(self, 8, r"The best low-rank copy", r"What is the best simple version of a matrix?",
                "Chapter eight. The best low-rank copy of a matrix.", lit=(1990,))
        self.pieces()
        self.proof()
        self.mosaic()
        self.letters()
        self.vowels()
        self.today()

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
            "Written out, the decomposition makes any matrix a sum of simple pieces, <bookmark mark='a'/> each a "
            "column times a row, weighted by a singular value. The number of pieces is the rank; a low-rank table is "
            "one a few pieces build. <bookmark mark='b'/> Keep the k biggest and you get the closest matrix of rank k. "
            "Nothing else comes closer: the Eckart-Young theorem, from 1936."
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
    def proof(self):
        thm = theorem_card(r"Eckart--Young",
                           r"If $B$ has rank at most $k$, \ then $\|A - B\|_F \ge \|A - A_k\|_F = "
                           r"\sqrt{\sigma_{k+1}^2 + \sigma_{k+2}^2 + \cdots}$, \ where $A_k$ keeps the $k$ biggest pieces.",
                           who=r"C.~Eckart \& G.~Young (1936); \ E.~Schmidt (1907) for integral operators", width=7.4)
        thm.to_edge(UP, buff=0.25)
        colors = {r"\sigma_{i+k}(A)": C.BITS}
        rows = [
            cmath(r"\sigma_{i+k}(A)", r"\le", r"\sigma_i(A - B) + \sigma_{k+1}(B)", font_size=34, colors=colors),
            cmath(r"\sigma_{i+k}(A)", r"\le", r"\sigma_i(A - B)", font_size=34, colors=colors),
            cmath(r"\|A - B\|_F^2", "=", r"\textstyle\sum_i \sigma_i(A-B)^2 \ \ge\ \sum_i \sigma_{i+k}(A)^2", font_size=34),
            cmath(r"\|A - B\|_F^2", r"\ge", r"\sigma_{k+1}^2 + \sigma_{k+2}^2 + \cdots = \|A - A_k\|_F^2", font_size=34),
        ]
        whys = [why(r"Weyl's inequality (1912)"), why(r"$B$ has rank $\le k$: \ $\sigma_{k+1}(B) = 0$"),
                why(r"squared entries add up \\ to squared singular values"), why(r"the tail: \ equality at $B = A_k$")]
        step = ladder(self, rows, whys, keep=4, top=0.9, x=-1.0, buff=0.42, edge=6.9)
        with self.voiceover(
            "Why can't anything beat them? <bookmark mark='a'/> Weyl's inequality, from 1912: A's singular values, "
            "shifted by k, are at most those of A minus B plus the k plus first of B. <bookmark mark='b'/> If B has rank "
            "k, that last term is zero. <bookmark mark='c'/> A matrix's squared size equals the sum of its squared "
            "singular values, as chapter nine shows, so B's error is at least the tail of A's. "
            "<bookmark mark='d'/> Keeping the top k achieves exactly that tail."
        ) as vo:
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            for k_, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(k_)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mosaic(self):
        d = load("image")
        img = np.asarray(d["img"])
        rec = np.asarray(d["recon"])
        ranks = [int(r) for r in d["ranks"]]
        err, tail = np.asarray(d["err"]), np.asarray(d["tail"])
        h, w = (int(v) for v in d["shape"])
        energy = np.asarray(d["energy"])
        pix, store = int(d["pixels"]), np.asarray(d["storage"])
        TW = 3.05
        tiles = Group()
        for k, r in enumerate(ranks):
            im = framed(gray_image(rec[k], TW))
            cap = label(rf"rank ${r}$: \ ${100 * store[k] / pix:.0f}\%$ of the numbers", font_size=20, color=GREY_A)
            tiles.add(Group(im, cap.next_to(im, DOWN, buff=0.08)))
        im = framed(gray_image(img, TW), color=C.BITS)
        cap = label(rf"the picture: \ ${h} \times {w}$ pixels", font_size=20, color=C.BITS)
        tiles.add(Group(im, cap.next_to(im, DOWN, buff=0.08)))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.25, 0.3)).move_to(UP * 0.55)
        tag = note(r"a landscape drawn by code (\texttt{compute.py}), \ grey levels as a matrix").to_corner(DL, buff=0.2)
        chk = label(rf"rank ${ranks[3]}$: \ $\|A-A_{{{ranks[3]}}}\|_F={err[3]:.4f}$; \ "
                    rf"$\sqrt{{\sum_{{i>{ranks[3]}}}\sigma_i^2}}={tail[3]:.4f}$",
                    font_size=26, color=C.BITS).to_edge(DOWN, buff=0.55)
        k8 = ranks.index(8) if 8 in ranks else 3
        with self.voiceover(
            f"A picture is a matrix too: {h} rows of {w} grey levels. <bookmark mark='a'/> Its best rank-one copy is a "
            "column times a row: stripes, the sky and the horizon. <bookmark mark='b'/> Rank two, four, eight: the "
            f"mountains appear. Rank {ranks[k8]} keeps {100 * energy[k8]:.1f} percent of the squared size with "
            f"{100 * store[k8] / pix:.0f} percent of the numbers. <bookmark mark='c'/> Then the trees; by rank "
            f"{ranks[-1]} it is hard to tell from the original. <bookmark mark='d'/> And each Frobenius error is exactly the "
            "Euclidean norm of the singular values left out."
        ) as vo:
            self.play(FadeIn(tiles[-1]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(tiles[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tiles[1:4]], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tiles[4:7]], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(chk))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def letters(self):
        d = load("letters")
        M, S, recon, err = np.asarray(d["M"]), np.asarray(d["S"]), np.asarray(d["recon"]), np.asarray(d["err"])
        assert abs(d["total"] - 1) < 1e-9  # the table's entries are square roots of probabilities
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
            "Part 1's table of letter pairs, 26 by 26, with square-root probabilities. <bookmark mark='a'/> Its first "
            "piece is a separable approximation: after squaring and normalizing, the two letters are independent. "
            "<bookmark mark='b'/> Add the second, third, fifth, tenth, "
            "<bookmark mark='c'/> and the Frobenius error equals the Euclidean norm of the singular values left out: "
            f"{err[0]:.2f} of the whole after one piece, {err[1]:.2f} after two."
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
        left5 = [LETTERS[i] for i in order[:5]]
        all_vowels = sorted(left5) == sorted(VOWELS)
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
        nv = sum(ch in VOWELS for ch in left5)
        found_say = ("No one told the computer what a vowel is. From counts alone, it found that vowels and "
                     "consonants take turns." if all_vowels else "Most of the vowels gather at one end, from counts "
                     "alone.")
        vow_box = SurroundingRectangle(VGroup(*[labs[k] for k in range(5)]), color=C.BITS, buff=0.15, corner_radius=0.1)
        head = label(r"Each letter, placed by the table's strongest departure from independence", font_size=30)
        head.to_edge(UP, buff=0.6)
        tag = label(r"correspondence analysis: \ the SVD of $\dfrac{P(x, y) - P(x)P(y)}{\sqrt{P(x)P(y)}}$", font_size=26,
                    color=GREY_A).to_edge(DOWN, buff=0.5)
        found = label(r"vowels and consonants take turns" if all_vowels else rf"${nv}$ of the $5$ leftmost are vowels",
                      font_size=34, color=C.BITS).move_to(DOWN * 2.0)
        dep = gloss(r"departure from independence", r"each pair's count, minus the count you'd expect\\ if letters "
                    r"ignored each other: \ only the surprise is kept", width=6.0)
        dep.move_to(UP * 1.75)
        with self.voiceover(
            "The pieces mean something. <bookmark mark='a'/> Take the table's departure from independence: each count "
            "against what you'd expect if letters ignored their neighbours. Spread the letters along its strongest "
            f"direction. <bookmark mark='b'/> At one end: {', '.join(left5[:-1])}, {left5[-1]}. {found_say}"
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

    # ------------------------------------------------------------------
    def today(self):
        cards = VGroup(
            history_card(1990, r"Deerwester, Dumais et al., \ latent semantic analysis",
                         r"a truncated SVD of a word-by-document table: \ search by meaning (chapter twelve)",
                         color=HIST, width=4.3, font_size=30),
            history_card(2021, r"E.~Hu et al., \ LoRA",
                         r"fine-tune a model by adding a rank-$r$ matrix $BA$ to each weight; \ for GPT-3, $10{,}000$ "
                         r"times fewer trained numbers (Part 27)", color=HIST, width=4.3, font_size=30),
            history_card(2024, r"DeepSeek-V2, \ latent attention",
                         r"keys and values squeezed through a low-rank latent, \ to shrink the memory a long "
                         r"context needs (Part 15)", color=HIST, width=4.3, font_size=30),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP)
        cards.move_to(DOWN * 0.1)
        head = label(r"Low rank, \ at work", font_size=40).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Low rank is everywhere in machine learning. <bookmark mark='a'/> In 1990, latent semantic analysis "
            "searched documents by meaning with a truncated SVD. <bookmark mark='b'/> In 2021, LoRA fine-tuned huge "
            "models by learning a low-rank change to each weight: for GPT-3, ten thousand times fewer numbers to train. "
            "<bookmark mark='c'/> In 2024, DeepSeek squeezed attention's keys and values through a low-rank bottleneck. "
            "Parts 15 and 27 build these."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
