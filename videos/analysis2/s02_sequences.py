from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis2.common import plain_axes


class Sequences(VoiceoverScene):
    def construct(self):
        self.card()
        self.game()
        self.nonexample()
        self.unique()
        self.laws()
        self.subsequences()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Sequences and their limits", r"What does it mean to get arbitrarily close?",
                            lit=(1821,), part=2)
        with self.voiceover(
            "Chapter one. Cauchy, in 1821, said a sequence converges to a limit when its terms get, and stay, "
            "arbitrarily close to it. Making arbitrarily close precise is the whole subject."
        ) as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def game(self):
        n_max = 40
        n = np.arange(1, n_max + 1)
        a = 1 + (-1.0) ** n * 1.5 / n
        ax = plain_axes([0, n_max + 1, 5], [-0.2, 2.2, 0.5], 11.5, 4.4, numbers=True, font_size=20,
                        axis_config={"decimal_number_config": {"num_decimal_places": 1}}, x_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to(DOWN * 1.0)
        board = SequenceBoard(ax, a, L=1.0, eps=0.5, N=n_max, n_max=n_max)  # N = n_max: no dot judged yet
        dfn = MathTex(r"p_n \to p", r"\iff", r"\forall \varepsilon > 0", r"\;\exists N", r"\;:\;",
                      r"n > N \Rightarrow |p_n - p| < \varepsilon", font_size=40).to_edge(UP, buff=0.45)
        dfn[2].set_color(C.EPS)
        dfn[3].set_color(C.DELTA)
        ref = note(r"Rudin 3.1").next_to(dfn, DOWN, buff=0.12).align_to(dfn, RIGHT)
        seq_l = MathTex(r"p_n = 1 + \frac{(-1)^n\, 1.5}{n}", font_size=34, color=C.SEQ).move_to([4.6, 2.05, 0])
        Lline = DashedLine(ax.c2p(0, 1), ax.c2p(n_max + 1, 1), color=WHITE, stroke_width=1.5)
        dots = board.dots()
        with self.voiceover(
            "Here's a sequence: one plus or minus one and a half over n, alternating sides of one. <bookmark mark='d'/> "
            "Rudin's definition: p n converges to p if for every epsilon greater than zero there's an N such that every "
            "term after the N-th is within epsilon of p. <bookmark mark='g'/> Read it as a game with two players."
        ) as vo:
            self.play(Create(ax), FadeIn(seq_l))
            self.play(FadeIn(dots), Create(Lline))
            vo.wait_until("d")
            self.play(Write(dfn), FadeIn(ref))
            vo.wait_until("g")
        band, thr = board.eps_band(), board.threshold()
        Ns = []
        with self.voiceover(
            "<bookmark mark='e'/> The first player, epsilon, picks a band around the limit: here, half-width a half. "
            "<bookmark mark='n'/> The second player answers with an N: past N, every dot must sit inside the band. N "
            "equals 3 works. <bookmark mark='s'/> Epsilon tightens the band to 0.2; now N has to be 7. "
            "<bookmark mark='t'/> At 0.05, N is 30. The sequence converges because the second player can always answer, "
            "however small the band."
        ) as vo:
            vo.wait_until("e")
            self.play(FadeIn(band))
            board.N.set_value(0)
            self.wait(0.4)
            for mk, e in (("n", 0.5), ("s", 0.2), ("t", 0.05)):
                vo.wait_until(mk)
                if e != 0.5:
                    self.play(board.eps.animate.set_value(e), run_time=0.8)
                N = board.smallest_N(e)
                Ns.append(N)
                if mk == "n":
                    self.play(FadeIn(thr), board.N.animate.set_value(N), run_time=1.0)
                else:
                    self.play(board.N.animate.set_value(N), run_time=1.0)
        assert Ns == [3, 7, 30], Ns
        order = label(r"The order of the moves is the content: $N$ may depend on $\varepsilon$.", font_size=28,
                      color=GREY_A).move_to([0, 1.2, 0]).shift(LEFT * 1.6)
        with self.voiceover(
            "Notice the order of the moves. <bookmark mark='o'/> Epsilon goes first, and N is allowed to depend on it. "
            "Swapping the order would demand one N that works for every epsilon at once, which only an eventually "
            "constant sequence could satisfy. This game, with different rules about who moves when, will define almost "
            "everything in this series."
        ) as vo:
            vo.wait_until("o")
            self.play(FadeIn(order))
        self.wait(0.3)
        for m in (band, thr, dots):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def nonexample(self):
        n_max = 30
        n = np.arange(1, n_max + 1)
        a = (-1.0) ** n
        ax = plain_axes([0, n_max + 1, 5], [-1.6, 1.6, 0.5], 11.5, 4.4, numbers=True, font_size=20,
                        axis_config={"decimal_number_config": {"num_decimal_places": 1}}, x_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to(DOWN * 0.8)
        board = SequenceBoard(ax, a, L=0.0, eps=0.5, N=10, n_max=n_max)
        dots, band, thr = board.dots(), board.eps_band(), board.threshold()
        head = MathTex(r"p_n = (-1)^n", font_size=40, color=C.SEQ).to_edge(UP, buff=0.5)
        txt = label(r"a band of half-width $\tfrac12$ cannot hold both $1$ and $-1$: \ no limit wins", font_size=28,
                    color=C.PATHOLOGY).next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Here's a sequence that loses: minus one, one, minus one, one. <bookmark mark='b'/> Epsilon picks a band of "
            "half-width one half. Whatever limit you propose, and however far out you set N, the band can't hold both "
            "one and minus one. <bookmark mark='m'/> Slide the proposed limit anywhere: some dots always escape. The "
            "sequence diverges."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(dots))
            vo.wait_until("b")
            self.play(FadeIn(band), FadeIn(thr), FadeIn(txt))
            vo.wait_until("m")
            for L in (0.6, -0.5, 0.0):
                board.Lv = L
                self.play(board.N.animate.set_value(board.N.get_value() + 0.0001), run_time=0.7)
        self.wait(0.3)
        for m in (band, thr, dots):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def unique(self):
        X = lambda v: -1.0 + v * 2.2  # noqa: E731
        y0 = 0.3
        line = Line([X(-2.2), y0, 0], [X(3.6), y0, 0], color=GREY_C, stroke_width=2)
        p, q = 0.0, 1.6
        e = 0.65
        bp = Rectangle(width=2 * e * 2.2, height=0.6, stroke_width=0, fill_color=C.EPS, fill_opacity=0.25).move_to([X(p), y0, 0])
        bq = Rectangle(width=2 * e * 2.2, height=0.6, stroke_width=0, fill_color=C.APPROX, fill_opacity=0.25).move_to([X(q), y0, 0])
        lp = MathTex(r"p", font_size=36).next_to([X(p), y0, 0], DOWN, buff=0.45)
        lq = MathTex(r"p'", font_size=36).next_to([X(q), y0, 0], DOWN, buff=0.45)
        dp, dq = Dot([X(p), y0, 0], radius=0.07), Dot([X(q), y0, 0], radius=0.07)
        stmt = VGroup(label(r"\textbf{Rudin 3.2} \ A sequence has at most one limit.", font_size=32),
                      label(r"bands of half-width $\varepsilon = \tfrac12 d(p, p')$ around two limits are disjoint;",
                            font_size=28, color=GREY_A),
                      label(r"the tail cannot lie in both.", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.15)
        stmt.to_edge(UP, buff=0.5)
        bnd = label(r"Also: a convergent sequence is bounded (all but finitely many terms lie in one band).",
                    font_size=26, color=GREY_B).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Two quick consequences. <bookmark mark='u'/> A sequence can't have two limits: if it approached both p and "
            "p prime, take epsilon to be half the distance between them. The two bands don't overlap, and from some point "
            "on the terms would have to be in both. <bookmark mark='b'/> And a convergent sequence is bounded: all but "
            "finitely many terms sit in one band."
        ) as vo:
            self.play(Create(line), FadeIn(dp), FadeIn(dq), FadeIn(lp), FadeIn(lq))
            vo.wait_until("u")
            self.play(FadeIn(stmt), FadeIn(bp), FadeIn(bq))
            vo.wait_until("b")
            self.play(FadeIn(bnd))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def laws(self):
        head = label(r"\textbf{Rudin 3.3} \ If $s_n \to s$ and $t_n \to t$, then $s_n + t_n \to s + t$, \ $s_n t_n \to st$, \ldots",
                     font_size=30).to_edge(UP, buff=0.5)
        rows = [
            MathTex(r"|(s_n + t_n) - (s + t)|", r"\le", r"|s_n - s| + |t_n - t|", font_size=40),
            MathTex(r"|(s_n + t_n) - (s + t)|", r"<", r"\tfrac{\varepsilon}{2} + \tfrac{\varepsilon}{2} = \varepsilon",
                    font_size=40),
        ]
        whys = [why(r"triangle inequality"), why(r"for $n$ past both thresholds, one for $s_n$ and one for $t_n$")]
        step = ladder(self, rows, whys, keep=2, top=1.6, buff=0.55, x=0.3)
        trick = label(r"the $\varepsilon/2$ trick: split the error, and ask each piece for half", font_size=30,
                      color=C.EPS).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "And limits respect arithmetic. <bookmark mark='h'/> Take sums. <bookmark mark='a'/> The error of s n plus "
            "t n is at most the error of s n plus the error of t n, by the triangle inequality. <bookmark mark='b'/> Ask "
            "each sequence to get within epsilon over two, which each can do past its own threshold; past both "
            "thresholds, the total error is less than epsilon. <bookmark mark='t'/> This is the epsilon over two trick, "
            "and it, with its cousin epsilon over three, does most of the routine work in analysis."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("t")
            self.play(FadeIn(trick))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def subsequences(self):
        n_max = 30
        n = np.arange(1, n_max + 1)
        a = (-1.0) ** n * (1 + 1.0 / n)
        ax = plain_axes([0, n_max + 1, 5], [-2.2, 2.2, 1], 11.5, 4.2, numbers=True, font_size=20).move_to(DOWN * 1.0)
        dots = VGroup(*[Dot(ax.c2p(k, v), radius=0.05, color=C.SEQ) for k, v in zip(n, a)])
        ev = VGroup(*[d for k, d in zip(n, dots) if k % 2 == 0])
        od = VGroup(*[d for k, d in zip(n, dots) if k % 2 == 1])
        dfn = VGroup(label(r"A \textbf{subsequence}: $p_{n_1}, p_{n_2}, \ldots$ with $n_1 < n_2 < \cdots$", font_size=30),
                     label(r"its limits are the \textbf{subsequential limits} of $(p_n)$ \ (Rudin 3.5)", font_size=28,
                           color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.45)
        ex = MathTex(r"p_n = (-1)^n\big(1 + \tfrac1n\big)", font_size=34, color=C.SEQ).move_to([-4.4, 1.3, 0])
        l_ev = MathTex(r"p_{2k} \to 1", font_size=34, color=C.CONNECTED_SET).next_to(ax.c2p(n_max, 1.05), UP, buff=0.15)
        l_od = MathTex(r"p_{2k+1} \to -1", font_size=34, color=C.CLOSED_SET).next_to(ax.c2p(n_max, -1.05), DOWN, buff=0.15)
        thm = label(r"\textbf{Rudin 3.6} \ In a compact space, every sequence has a convergent subsequence;"
                    r" \ so does every bounded sequence in $\R^k$.", font_size=26, color=C.COMPACT_SET).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Last idea for this chapter: subsequences. <bookmark mark='d'/> Keep some of the terms, in order, and you get "
            "a subsequence; its limits are called subsequential limits. <bookmark mark='e'/> This sequence has no limit, "
            "<bookmark mark='a'/> but its even terms converge to one, <bookmark mark='b'/> and its odd terms to minus one. "
            "<bookmark mark='c'/> And Part 1 pays off immediately: in a compact space, every sequence has a convergent "
            "subsequence, because an infinite set of terms must pile up somewhere. In particular, every bounded sequence "
            "of real numbers does."
        ) as vo:
            self.play(FadeIn(dfn[0]))
            vo.wait_until("d")
            self.play(FadeIn(dfn[1]))
            vo.wait_until("e")
            self.play(Create(ax), FadeIn(ex), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.03))
            vo.wait_until("a")
            self.play(ev.animate.set_color(C.CONNECTED_SET), FadeIn(l_ev))
            vo.wait_until("b")
            self.play(od.animate.set_color(C.CLOSED_SET), FadeIn(l_od))
            vo.wait_until("c")
            self.play(FadeIn(thm))
        self.wait(0.5)
        self.clear_scene()
