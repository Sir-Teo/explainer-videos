from __future__ import annotations

from fractions import Fraction

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import load

MONO = "DejaVu Sans Mono"
SQRT2_ = 2 ** 0.5


class Counting(VoiceoverScene):
    def construct(self):
        self.card()
        self.pairing()
        self.integers()
        self.rationals()
        self.unions()
        self.diagonal()
        self.reals()
        self.algebraic()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"Counting infinities", r"Are there more real numbers than fractions?", lit=(1874,), part=1)
        with self.voiceover(
            "Chapter four. The rationals are dense: they're everywhere. So are there really more real numbers than "
            "fractions? To answer, we need a way to compare the sizes of infinite sets."
        ) as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def pairing(self):
        n = 9
        top = VGroup(*[MathTex(str(k), font_size=36, color=C.SEQ) for k in range(1, n + 1)]).arrange(RIGHT, buff=0.85)
        bot = VGroup(*[MathTex(str(2 * k), font_size=36, color=C.DELTA) for k in range(1, n + 1)]).arrange(RIGHT, buff=0.85)
        for t, b in zip(top, bot):
            b.set_x(t.get_x())
        top.move_to(UP * 0.9)
        bot.move_to(DOWN * 0.6)
        for t, b in zip(top, bot):
            b.set_x(t.get_x())
        dots_t = MathTex(r"\cdots", font_size=36).next_to(top, RIGHT, buff=0.4)
        dots_b = MathTex(r"\cdots", font_size=36).next_to(bot, RIGHT, buff=0.4)
        links = VGroup(*[Line(t.get_bottom() + DOWN * 0.08, b.get_top() + UP * 0.08, color=GREY_B, stroke_width=2)
                         for t, b in zip(top, bot)])
        lt = label(r"$\N$", font_size=34, color=C.SEQ).next_to(top, LEFT, buff=0.6)
        lb = label(r"even numbers", font_size=28, color=C.DELTA).next_to(bot, LEFT, buff=0.4)
        rule = label(r"Same size $=$ a one-to-one pairing with nothing left over", font_size=34).to_edge(UP, buff=0.6)
        defs = VGroup(
            label(r"\textbf{countable}: \ can be paired with $\N = \{1, 2, 3, \ldots\}$, \ i.e.\ listed", font_size=30),
            label(r"\textbf{uncountable}: \ infinite, and not countable", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.6)
        ref = note(r"Rudin 2.4").next_to(defs, RIGHT, buff=0.4).align_to(defs, DOWN)
        with self.voiceover(
            "Two sets have the same size when their elements can be paired off, one to one, with nothing left over on "
            "either side. <bookmark mark='p'/> Infinite sets do strange things under this rule. The whole numbers can be "
            "paired with the even numbers, one with two, two with four, three with six, even though the evens are only "
            "half of them. <bookmark mark='d'/> A set is countable if it can be paired with the whole numbers, which is "
            "the same as saying its elements can be listed, first, second, third, forever. "
            "<bookmark mark='u'/> An infinite set that can't be listed is uncountable."
        ) as vo:
            self.play(FadeIn(rule))
            vo.wait_until("p")
            self.play(FadeIn(top), FadeIn(dots_t), FadeIn(lt))
            self.play(FadeIn(bot), FadeIn(dots_b), FadeIn(lb), LaggedStart(*[Create(l) for l in links], lag_ratio=0.15))
            vo.wait_until("d")
            self.play(FadeIn(defs[0]), FadeIn(ref))
            vo.wait_until("u")
            self.play(FadeIn(defs[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def integers(self):
        xs = list(range(-5, 6))
        X = {v: v * 1.1 for v in xs}
        line = Line([-6.3, -0.5, 0], [6.3, -0.5, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X[v], -0.58, 0], [X[v], -0.42, 0], color=GREY_C),
                                Text(str(v), font_size=22, color=GREY_B).move_to([X[v], -0.85, 0])) for v in xs])
        order = [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5]
        nums = VGroup(*[MathTex(str(i + 1), font_size=30, color=C.SEQ).move_to([X[v], -1.35, 0]) for i, v in enumerate(order)])
        dots = VGroup(*[Dot([X[v], -0.5, 0], radius=0.08, color=C.SEQ) for v in order])
        # every hop arcs above the line: clockwise when moving right, counterclockwise when moving left
        hops = VGroup(*[CurvedArrow(dots[i].get_center() + UP * 0.12, dots[i + 1].get_center() + UP * 0.12,
                                    angle=-TAU / 6 if order[i + 1] > order[i] else TAU / 6, color=GREY_B, stroke_width=2,
                                    tip_length=0.12) for i in range(len(order) - 1)])
        n_lab = label(r"place in the list", font_size=24, color=C.SEQ).move_to([-4.6, -1.95, 0])
        lst = MathTex(r"\Z:\quad 0,\ 1,\ -1,\ 2,\ -2,\ 3,\ -3,\ \ldots", font_size=40).to_edge(UP, buff=0.8)
        with self.voiceover(
            "The integers are countable: <bookmark mark='a'/> list zero, then one, minus one, two, minus two, and so on. "
            "Every integer gets a place."
        ) as vo:
            self.play(Create(line), FadeIn(ticks))
            vo.wait_until("a")
            self.play(Write(lst), FadeIn(n_lab))
            for i in range(len(order)):
                anims = [FadeIn(dots[i], scale=2), FadeIn(nums[i])]
                if i:
                    anims.append(Create(hops[i - 1]))
                self.play(*anims, run_time=0.35)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rationals(self):
        d = load("qorder")
        order = [tuple(map(int, r)) for r in d["order"]]
        P, Q = 7, 6
        cell = 0.92
        origin = np.array([-3.45, 2.3, 0])  # the grid centred
        pos = {}
        grid = VGroup()
        for q in range(1, Q + 1):
            for p in range(1, P + 1):
                c = origin + np.array([(p - 1) * cell * 1.25, -(q - 1) * cell, 0])
                pos[(p, q)] = c
                grid.add(MathTex(rf"\tfrac{{{p}}}{{{q}}}", font_size=34).move_to(c))
        ph = MathTex(r"p \to", font_size=28, color=GREY_B).next_to(grid, UP, buff=0.2).align_to(grid, LEFT)
        qh = MathTex(r"q \downarrow", font_size=28, color=GREY_B).next_to(grid, LEFT, buff=0.25).align_to(grid, UP)
        cell_of = {}
        for (p, q) in pos:
            cell_of[(p, q)] = grid[(q - 1) * P + (p - 1)]
        # the zigzag over the anti-diagonals p + q = s, as far as the grid shows
        visit = []
        for s in range(2, P + Q + 1):
            diag = [(s - q, q) for q in range(1, s)]
            if s % 2 == 1:
                diag = diag[::-1]
            visit += [(p, q) for (p, q) in diag if p <= P and q <= Q]
        # the walk drawn between the fractions (never through them), behind the grid
        path = VGroup(*[Line(pos[u], pos[v], buff=0.3, color=C.APPROX, stroke_width=3, stroke_opacity=0.6)
                        for u, v in zip(visit[:21], visit[1:22])])
        path.set_z_index(-1)
        listed = [v for v in order if v in pos]
        seen = set()
        counters = VGroup()
        dims = VGroup()
        k = 0
        for v in visit[:22]:
            f = Fraction(*v)
            if f in seen:
                dims.add(cell_of[v])
            else:
                seen.add(f)
                k += 1
                counters.add(MathTex(str(k), font_size=22, color=C.SEQ).next_to(cell_of[v], UL, buff=0.02))
        assert (2, 2) in [tuple(s) for s in d["skipped"]]
        with self.voiceover(
            "The positive fractions are countable too, which is more surprising, since they're dense. <bookmark mark='g'/> "
            "Lay them out in a grid: p over q, with p across and q down. Every positive fraction appears somewhere, many "
            "of them several times. <bookmark mark='z'/> Now walk the grid along its diagonals, zigzagging back and forth, "
            "<bookmark mark='s'/> and number each fraction as you reach it, skipping any you've already counted, like two "
            "over two, which is one."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(g_) for g_ in grid], lag_ratio=0.01), FadeIn(ph), FadeIn(qh), run_time=1.5)
            vo.wait_until("z")
            self.play(LaggedStart(*[Create(sg) for sg in path], lag_ratio=1.0), run_time=3.0, rate_func=linear)
            vo.wait_until("s")
            self.play(LaggedStart(*[FadeIn(c, scale=1.5) for c in counters], lag_ratio=0.15), run_time=3)
            self.play(dims.animate.set_opacity(0.25))
        # the list is the walk's own order: each new fraction, in the order the zigzag reaches it
        walk, seen_ = [], set()
        for s_ in range(2, 40):
            diag = [(s_ - q, q) for q in range(1, s_)]
            for v in (diag[::-1] if s_ % 2 == 1 else diag):
                if Fraction(*v) not in seen_:
                    seen_.add(Fraction(*v))
                    walk.append(v)
        counted = [v for v in visit[:22] if v == (Fraction(*v).numerator, Fraction(*v).denominator)]
        assert walk[:len(counted)] == counted and len(counted) == len(counters) >= 12
        lst = MathTex(",\\ ".join(str(p_) if q_ == 1 else rf"\tfrac{{{p_}}}{{{q_}}}" for p_, q_ in walk[:12])
                      + r",\ \ldots", font_size=38, color=C.SEQ).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The result is a list: one, a half, two, three, a third, a quarter, two thirds, and on, in which every "
            "positive fraction appears exactly once. <bookmark mark='m'/> Add zero and the negatives by interleaving, as we did "
            "for the integers, and all of Q is countable. The dense dust of chapter one is just a list."
        ) as vo:
            self.play(Write(lst))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unions(self):
        rows = VGroup()
        for i in range(1, 5):
            row = VGroup(MathTex(rf"E_{i}:", font_size=36, color=GREY_A),
                         *[MathTex(rf"x_{{{i}{j}}}", font_size=36) for j in range(1, 6)], MathTex(r"\cdots", font_size=36))
            for k, m in enumerate(row):
                m.move_to([-4.2 + 1.25 * k, 1.6 - 0.85 * (i - 1), 0])
            rows.add(row)
        rows.add(MathTex(r"\vdots", font_size=36).move_to([-4.2 + 1.25, 1.6 - 0.85 * 4 + 0.15, 0]))
        visit = []  # diagonal by diagonal, alternating direction, so each step goes to a neighbor
        for s in range(2, 8):
            diag = [(i, s - i) for i in range(1, s) if i <= 4 and s - i <= 5]
            visit += diag[::-1] if s % 2 == 0 else diag
        assert all(abs(a - c) + abs(b - d) <= 2 for (a, b), (c, d) in zip(visit, visit[1:]))
        # the walk, drawn between the entries (not through them), with each entry's place in the list
        cs = [rows[i - 1][j].get_center() for (i, j) in visit]
        path = VGroup(*[Line(a, b, buff=0.32, color=C.APPROX, stroke_width=3) for a, b in zip(cs, cs[1:])])
        order = VGroup(*[MathTex(str(k + 1), font_size=22, color=C.APPROX).next_to(rows[i - 1][j], UL, buff=0.02)
                         for k, (i, j) in enumerate(visit)])
        stmt = VGroup(label(r"\textbf{Theorem} (Rudin 2.12)", font_size=28, color=GREY_A),
                      label(r"A countable union of countable sets is countable.", font_size=32))
        stmt.arrange(DOWN, buff=0.15).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The same zigzag proves something more general. <bookmark mark='t'/> Take countably many countable sets, E "
            "one, E two, E three, and so on, and write each as a row. <bookmark mark='z'/> Walking the diagonals lists "
            "every element of every row. So a countable union of countable sets is countable. It's a tool we'll use "
            "again and again, for instance when we measure sets in Part 5."
        ) as vo:
            self.play(FadeIn(stmt))
            vo.wait_until("t")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2))
            vo.wait_until("z")
            self.play(FadeIn(order[0]), run_time=0.3)
            self.play(LaggedStart(*[AnimationGroup(Create(sg), FadeIn(o_)) for sg, o_ in zip(path, order[1:])],
                                  lag_ratio=1.0), run_time=3, rate_func=linear)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def diagonal(self):
        d = load("diagonal")
        R, Cn = d["rows"], d["diag"]
        nr, nc = R.shape
        cw, ch = 0.44, 0.44
        x0, y0 = -4.9, 2.75
        cells = [[None] * nc for _ in range(nr)]
        table = VGroup()
        names = VGroup()
        for i in range(nr):
            names.add(MathTex(rf"s_{{{i + 1}}}", font_size=28, color=GREY_A).move_to([x0 - 0.75, y0 - i * ch, 0]))
            for j in range(nc):
                t = Text(str(int(R[i, j])), font_size=24, font=MONO).move_to([x0 + j * cw, y0 - i * ch, 0])
                cells[i][j] = t
                table.add(t)
        more = MathTex(r"\vdots", font_size=30, color=GREY_B).move_to([x0 + 4 * cw, y0 - nr * ch + 0.05, 0])
        dots_r = MathTex(r"\cdots", font_size=30, color=GREY_B).move_to([x0 + nc * cw + 0.1, y0 - 2 * ch, 0])
        diag_boxes = VGroup(*[SurroundingRectangle(cells[i][i], color=C.COMPACT_SET, buff=0.07, stroke_width=2.5)
                              for i in range(nr)])
        ys = y0 - (nr + 0.9) * ch
        s_name = MathTex(r"s", font_size=32, color=C.EPS).move_to([x0 - 0.75, ys, 0])
        s_cells = VGroup(*[Text(str(int(Cn[i])), font_size=24, font=MONO, color=C.EPS).move_to([x0 + i * cw, ys, 0])
                           for i in range(nr)])
        s_more = MathTex(r"\cdots", font_size=30, color=C.EPS).next_to(s_cells, RIGHT, buff=0.25)
        rule = VGroup(label(r"flip the diagonal:", font_size=28),
                      MathTex(r"s(k) = 1 - s_k(k)", font_size=34, color=C.EPS)).arrange(DOWN, buff=0.15)
        rule.move_to([5.0, 1.6, 0])
        stmt = VGroup(label(r"\textbf{Theorem} (Rudin 2.14)", font_size=26, color=GREY_A),
                      label(r"The set of all infinite", font_size=28),
                      label(r"$0$--$1$ sequences is uncountable.", font_size=28)).arrange(DOWN, buff=0.1)
        stmt.move_to([4.75, -0.6, 0])
        with self.voiceover(
            "So is everything countable? <bookmark mark='a'/> Here's Cantor's diagonal argument, from 1891. Consider "
            "infinite sequences of zeros and ones. Suppose someone hands us a list of them, s one, s two, s three, and "
            "so on, claiming it contains every such sequence. <bookmark mark='d'/> Look at the diagonal: the first digit "
            "of the first sequence, the second digit of the second, and so on."
        ) as vo:
            self.play(FadeIn(names), LaggedStart(*[FadeIn(t) for t in table], lag_ratio=0.004), FadeIn(more),
                      FadeIn(dots_r), run_time=2)
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(b) for b in diag_boxes], lag_ratio=0.12), run_time=2)
        with self.voiceover(
            "<bookmark mark='f'/> Now build a new sequence s by flipping every diagonal digit: zero becomes one, one "
            "becomes zero. <bookmark mark='c'/> Then s differs from the first sequence in the first place, from the "
            "second in the second place, and from the k-th sequence in the k-th place. So s is not on the list. "
            "<bookmark mark='t'/> Any list misses something: the zero-one sequences are uncountable."
        ) as vo:
            vo.wait_until("f")
            self.play(FadeIn(rule), FadeIn(s_name))
            for i in range(nr):
                self.play(TransformFromCopy(cells[i][i], s_cells[i]), run_time=0.25)
            self.play(FadeIn(s_more))
            vo.wait_until("c")
            for i in range(nr):
                a, b = cells[i][i], s_cells[i]
                self.play(Indicate(a, color=C.PATHOLOGY, scale_factor=1.6), Indicate(b, color=C.PATHOLOGY,
                                                                                     scale_factor=1.6), run_time=0.3)
            vo.wait_until("t")
            self.play(FadeIn(stmt))
        for i in range(nr):
            assert int(Cn[i]) != int(R[i, i])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reals(self):
        m = MathTex(r"s = (s_1, s_2, s_3, \ldots) \;\longmapsto\; x = \sum_{k=1}^{\infty} \frac{2 s_k}{3^k}", font_size=38)
        m.to_edge(UP, buff=0.3)
        ex = MathTex(r"(1,0,0,1,1,\ldots) \;\mapsto\; 0.20022\ldots_{\,3}", font_size=32, color=C.SEQ).next_to(m, DOWN, buff=0.2)
        rows = [
            MathTex(r"|x - x'|", r"\ge", r"\frac{2}{3^n} - \sum_{k > n} \frac{2}{3^k}", font_size=38),
            MathTex(r"|x - x'|", r"\ge", r"\frac{2}{3^n} - \frac{1}{3^n} = \frac{1}{3^n} > 0", font_size=38),
        ]
        whys = [why(r"if $s$ and $s'$ first differ at place $n$"), why(r"so different sequences give different numbers")]
        step = ladder(self, rows, whys, keep=2, top=-0.75, buff=0.3, x=-1.6)
        conc = label(r"So $[0,1]$, and therefore $\R$, is uncountable. \ (The image is the Cantor set: chapter 9.)",
                     font_size=28, color=C.EPS).to_edge(DOWN, buff=0.35)
        # where the sequences land: digit 0 keeps the left third, digit 1 (written 2) the right third
        X = lambda v: -5.5 + 11.0 * float(v)  # noqa: E731
        lev_y = [1.3 - 0.36 * k for k in range(5)]

        def level(k):
            ivs = [(Fraction(0), Fraction(1))]
            for _ in range(k):
                ivs = [iv for a, b in ivs for iv in ((a, a + (b - a) / 3), (b - (b - a) / 3, b))]
            return ivs

        tree = VGroup(*[VGroup(*[Line([X(a), lev_y[k], 0], [X(b), lev_y[k], 0], color=GREY_C, stroke_width=5)
                                 for a, b in level(k)]) for k in range(5)])

        def path(digits, color):
            a, b, g = Fraction(0), Fraction(1), VGroup()
            for k, dgt in enumerate(digits):
                a, b = (a, a + (b - a) / 3) if dgt == 0 else (b - (b - a) / 3, b)
                g.add(Line([X(a), lev_y[k + 1], 0], [X(b), lev_y[k + 1], 0], color=color, stroke_width=8))
            return g, a

        s1, x1 = path((1, 0, 0, 1), C.SEQ)
        s2, x2 = path((1, 1), C.DELTA)
        land = Dot([X(Fraction(2, 3) + Fraction(2, 81) + Fraction(2, 243)), lev_y[4] - 0.22, 0], radius=0.06,
                   color=C.SEQ)
        gap_a, gap_b = Fraction(7, 9), Fraction(8, 9)  # s and s' first differ at place 2: a gap of 1/9 between
        # drawn in the removed middle third of level 2, where nothing else is
        gap = VGroup(Line([X(gap_a), lev_y[2], 0], [X(gap_b), lev_y[2], 0], color=C.EPS, stroke_width=3),
                     MathTex(r"\ge \tfrac{1}{3^n}", font_size=24, color=C.EPS).next_to(
                         [X((gap_a + gap_b) / 2), lev_y[2], 0], DOWN, buff=0.08))
        slabs = VGroup(MathTex(r"s", font_size=26, color=C.SEQ).next_to(s1[-1], DOWN, buff=0.08),
                       MathTex(r"s'", font_size=26, color=C.DELTA).next_to(s2[-1], RIGHT, buff=0.12))
        ends = VGroup(MathTex(r"0", font_size=24, color=GREY_B).next_to([X(0), lev_y[0], 0], LEFT, buff=0.15),
                      MathTex(r"1", font_size=24, color=GREY_B).next_to([X(1), lev_y[0], 0], RIGHT, buff=0.15))
        assert gap_b - gap_a == Fraction(1, 9) and x1 == Fraction(56, 81) and x2 == Fraction(8, 9)
        assert x1 <= Fraction(170, 243) <= x1 + Fraction(1, 81)  # the landing point lies in the last interval
        with self.voiceover(
            "It follows that the real numbers are uncountable. <bookmark mark='m'/> Turn each zero-one sequence into a "
            "real number by reading it as digits in base three, with the ones written as twos. <bookmark mark='e'/> We "
            "use base three and only the digits zero and two to dodge the trap where two expansions name the same "
            "number, like 0.4999 forever and 0.5. <bookmark mark='a'/> If two sequences first differ at place n, their "
            "numbers differ by at least two over three to the n, minus everything the later digits can make up, "
            "<bookmark mark='b'/> which is one over three to the n, more than zero. So different sequences give "
            "different numbers, <bookmark mark='c'/> and the reals contain an uncountable set."
        ) as vo:
            self.play(Write(m))
            self.play(LaggedStart(*[Create(t) for t in tree], lag_ratio=0.3), FadeIn(ends), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(ex), LaggedStart(*[Create(x) for x in s1], lag_ratio=0.4), run_time=1.6)
            self.play(FadeIn(land, scale=2), FadeIn(slabs[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(x) for x in s2], lag_ratio=0.4), FadeIn(slabs[1]), run_time=1.2)
            step(0)
            vo.wait_until("b")
            self.play(Create(gap[0]), FadeIn(gap[1]))
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(conc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def algebraic(self):
        poly = MathTex(r"a_0 x^n + a_1 x^{n-1} + \cdots + a_n = 0, \qquad a_i \in \Z", font_size=40).to_edge(UP, buff=0.6)
        steps = VGroup(
            label(r"countably many polynomials (each is a finite list of integers)", font_size=30),
            label(r"each has at most $n$ roots", font_size=30),
            label(r"$\Rightarrow$ the algebraic numbers are countable \ (Cantor, 1874)", font_size=30, color=C.SEQ),
            label(r"$\Rightarrow$ almost every real number is \textbf{transcendental}", font_size=30, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(poly, DOWN, buff=0.6)
        steps.next_to(poly, DOWN, buff=0.4)
        # real roots in [-2.5, 2.5] of integer polynomials of degree <= 3 with coefficients in [-H, H], H = 1, 2, 3
        Xr = lambda v: v * 2.4  # noqa: E731
        y_ax = -1.55
        axis_r = VGroup(Line([Xr(-2.5), y_ax, 0], [Xr(2.5), y_ax, 0], color=GREY_C, stroke_width=2),
                        *[VGroup(Line([Xr(v), y_ax - 0.06, 0], [Xr(v), y_ax + 0.06, 0], color=GREY_C, stroke_width=2),
                                 MathTex(str(v), font_size=22, color=GREY_B).next_to([Xr(v), y_ax - 0.06, 0], DOWN,
                                                                                    buff=0.08))
                          for v in (-2, -1, 0, 1, 2)])
        from itertools import product
        seen, layers = set(), []
        for H in (1, 2, 3):
            new_r = []
            for deg in (1, 2, 3):
                for co in product(range(-H, H + 1), repeat=deg + 1):
                    if co[0] == 0 or max(map(abs, co)) != H and H > 1:
                        continue
                    for r in np.roots(co):
                        if abs(r.imag) < 1e-9 and -2.5 <= r.real <= 2.5:
                            key = round(float(r.real), 9)
                            if key not in seen:
                                seen.add(key)
                                new_r.append(key)
            layers.append(np.array(sorted(new_r)))
        dust = VGroup()
        for H, rs in zip((1, 2, 3), layers):
            h = 0.95 / H
            m_ = VMobject(stroke_color=C.SEQ, stroke_width=2.2 / H ** 0.5, stroke_opacity=0.9)
            m_.set_points(segments_points(Xr(rs), np.full(len(rs), y_ax), Xr(rs), np.full(len(rs), y_ax + h)))
            dust.add(m_)
        r2 = VGroup(Line([Xr(SQRT2_), y_ax, 0], [Xr(SQRT2_), y_ax + 0.95 / 2, 0], color=C.EPS, stroke_width=4),
                    MathTex(r"\sqrt2", font_size=26, color=C.EPS).next_to([Xr(SQRT2_), y_ax + 0.5, 0], UP, buff=0.06))
        dl_ = label(r"real roots of $a_0x^3 + a_1x^2 + a_2x + a_3$, \ $|a_i| \le 1, 2, 3$: \ tick height $1/H$",
                    font_size=22, color=GREY_B).next_to(axis_r, DOWN, buff=0.45)
        assert round(SQRT2_, 9) in seen and sum(len(r) for r in layers) > 300
        hist = VGroup(
            label(r"first explicit transcendental: Liouville, 1844", font_size=26, color=GREY_A),
            label(r"$e$: Hermite, 1873 \qquad $\pi$: Lindemann, 1882", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "This has a startling consequence. <bookmark mark='p'/> A number is algebraic if it solves a polynomial "
            "equation with integer coefficients, like root two, which solves x squared minus two equals zero. "
            "<bookmark mark='a'/> There are only countably many such polynomials, since each is a finite list of "
            "integers, <bookmark mark='b'/> and each has finitely many roots. <bookmark mark='c'/> So the algebraic "
            "numbers are countable, by the theorem on unions. That was Cantor's 1874 result. <bookmark mark='d'/> Since "
            "the reals are not countable, almost every real number is transcendental: not the root of any such "
            "polynomial."
        ) as vo:
            self.play(Write(poly), Create(axis_r))
            vo.wait_until("p")
            self.play(Create(r2[0]), FadeIn(r2[1]))
            for mk, s_ in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=RIGHT * 0.2))
                if mk == "b":
                    self.play(LaggedStart(*[Create(d_) for d_ in dust], lag_ratio=0.5), FadeIn(dl_), run_time=2.4)
        with self.voiceover(
            "And yet exhibiting even one is hard. <bookmark mark='l'/> The first explicit example came from Liouville in "
            "1844; e was proved transcendental in 1873, and pi only in 1882. The rationals are dense, yet countable: in "
            "the sense of size, they're almost nothing, and the numbers that fill the holes are almost everything."
        ) as vo:
            vo.wait_until("l")
            self.play(FadeIn(hist))
        self.wait(0.5)
        self.clear_scene()
