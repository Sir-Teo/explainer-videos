from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


class Countable(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Counting the fractions", r"Can every fraction be given a number?", lit=(1874,),
                            part=PART)
        with self.voiceover("Chapter two. Counting the fractions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.pairs()
        self.tree()
        self.algebraic()

    def pairs(self):
        d = load("pairing")
        G = d["grid"]
        cell = 0.78
        grid = VGroup()
        cells = {}
        for y in range(6):
            for x in range(6):
                sq = Square(side_length=cell, stroke_width=1, stroke_color=GREY_D).move_to([x * cell, -y * cell, 0])
                t = MathTex(str(G[y][x]), font_size=26, color=GOAL)
                t.move_to(sq)
                cells[(x, y)] = VGroup(sq, t)
                grid.add(sq)
        nums = VGroup(*cells.values())
        board = VGroup(grid, *[c[1] for c in cells.values()])
        board.move_to([-2.6, -0.3, 0])
        xl = VGroup(*[MathTex(str(x), font_size=22, color=GREY_B).next_to(cells[(x, 0)][0], UP, buff=0.12)
                      for x in range(6)])
        yl = VGroup(*[MathTex(str(y), font_size=22, color=GREY_B).next_to(cells[(0, y)][0], LEFT, buff=0.12)
                      for y in range(6)])
        bl = label(r"passenger $k$", font_size=22, color=GREY_A).next_to(xl, UP, buff=0.15)
        al = label(r"bus $j$", font_size=22, color=GREY_A).next_to(yl, LEFT, buff=0.15)
        order = sorted(cells, key=lambda p: G[p[1]][p[0]])[:21]
        path = VGroup()
        for p, q in zip(order, order[1:]):
            a, b = cells[p][0].get_center(), cells[q][0].get_center()
            if sum(p) == sum(q):
                path.add(Arrow(a, b, buff=0.2, color=SETC, stroke_width=3, tip_length=0.13,
                               max_tip_length_to_length_ratio=0.3))
            else:
                path.add(DashedLine(a, b, buff=0.24, color=GREY_B, stroke_width=1.5, dash_length=0.08,
                                    stroke_opacity=0.55))
        f = MathTex(r"\pi(j, k) = \frac{(j + k)(j + k + 1)}{2} + j", font_size=36).move_to([3.6, 1.0, 0])
        cap = VGroup(label(r"walk the diagonals: \ every pair gets a room", font_size=24),
                     label(r"$\mathbb{N} \times \mathbb{N}$ is countable", font_size=28, color=OK)).arrange(
            DOWN, buff=0.25).next_to(f, DOWN, buff=0.5)
        with self.voiceover(
            "Infinitely many buses, each with infinitely many passengers. Can the hotel still cope? "
            "<bookmark mark='a'/>Arrange the arrivals in a grid: bus j, passenger k. <bookmark mark='b'/>Now walk "
            "the diagonals, numbering as you go: zero, one, two, and so on. Every square of the grid is reached, "
            "after finitely many steps. <bookmark mark='c'/>Cantor wrote the walk as a formula: a polynomial that "
            "pairs the grid with the natural numbers, one to one. <bookmark mark='d'/>So the pairs of natural numbers "
            "are no more numerous than the natural numbers. A set that can be listed like this is called countable."
        ) as vo:
            self.play(Create(grid), FadeIn(xl), FadeIn(yl), FadeIn(bl), FadeIn(al))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(x) for x in path], lag_ratio=0.6),
                      LaggedStart(*[FadeIn(cells[p][1]) for p in order], lag_ratio=0.08), run_time=4)
            self.play(FadeIn(VGroup(*[cells[p][1] for p in cells if p not in order])))
            vo.wait_until("c")
            self.play(Write(f))
            vo.wait_until("d")
            self.play(FadeIn(cap))
        self.clear_scene()

    def tree(self):
        d = load("pairing")
        levels = d["tree"]
        nodes = {}
        g = VGroup()
        edges = VGroup()
        for depth, lv in enumerate(levels):
            n = len(lv)
            for i, (a, b) in enumerate(lv):
                x = (-6.0 + 12.0 * (i + 0.5) / n)
                y = 2.0 - 1.25 * depth
                t = MathTex(rf"\tfrac{{{a}}}{{{b}}}", font_size=36, color=GOAL if depth == 0 else WHITE).move_to([x, y, 0])
                nodes[(depth, i)] = t
                g.add(t)
                if depth:
                    p = nodes[(depth - 1, i // 2)]
                    edges.add(Line(p.get_bottom(), t.get_top(), buff=0.08, color=GREY_C, stroke_width=1.8))
        rule = MathTex(r"\frac{a}{b} \ \longrightarrow\ \frac{a}{a+b},\ \ \frac{a+b}{b}", font_size=34,
                       color=CONN).to_corner(UR, buff=0.4)
        seq = MathTex(r",\ ".join(rf"\tfrac{{{a}}}{{{b}}}" for a, b in d["sequence"]) + r",\ \dots", font_size=30)
        seq.to_edge(DOWN, buff=0.45)
        if seq.width > 13.2:
            seq.width = 13.2
        who = label(r"Calkin and Wilf (2000): \ every positive fraction appears exactly once, \ in lowest terms",
                    font_size=22, color=GREY_A).next_to(seq, UP, buff=0.25)
        with self.voiceover(
            "What about fractions? Between any two there are infinitely many more, so surely there are more fractions "
            "than whole numbers. <bookmark mark='a'/>Here is a tree, discovered by Neil Calkin and Herbert Wilf in "
            "2000, though its pattern goes back to Stern and Brocot. Start with one over one. Each fraction a over b "
            "has two children: a over a plus b, and a plus b over b. <bookmark mark='b'/>Every positive fraction "
            "appears in this tree exactly once, already in lowest terms. <bookmark mark='c'/>Now read the tree row "
            "by row. That is a list of all the positive fractions: the fractions are countable. Cantor proved it in "
            "1874, with a cruder list."
        ) as vo:
            self.play(FadeIn(rule), FadeIn(nodes[(0, 0)]))
            vo.wait_until("a")
            for depth in range(1, len(levels)):
                self.play(*[FadeIn(nodes[(depth, i)]) for i in range(len(levels[depth]))],
                          *[Create(e) for e in edges if True][2 ** depth - 2: 2 ** (depth + 1) - 2], run_time=0.9)
            vo.wait_until("b")
            self.play(FadeIn(who))
            vo.wait_until("c")
            self.play(Write(seq), run_time=2.5)
        self.clear_scene()

    def algebraic(self):
        hc = history_card(1874, r"Georg Cantor", r"`On a property of the collection of all real algebraic numbers'",
                          width=7.0, color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            VGroup(MathTex(r"\mathbb{N},\ \mathbb{Z},\ \mathbb{Q}", font_size=40), label(r"countable", font_size=26,
                                                                                        color=OK)).arrange(RIGHT, buff=0.5),
            VGroup(MathTex(r"\text{algebraic numbers: } \sqrt2,\ \sqrt[3]{5},\ \dots", font_size=36),
                   label(r"countable \ (list the polynomials by size)", font_size=26, color=OK)).arrange(RIGHT, buff=0.5),
            VGroup(MathTex(r"\mathbb{R}", font_size=44, color=BAD), label(r"\textit{not} countable", font_size=28,
                                                                          color=BAD)).arrange(RIGHT, buff=0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.3, 0])
        cons = label(r"so most real numbers are transcendental, \ a fact Cantor proved without exhibiting one",
                     font_size=24, color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In the same paper of 1874, Cantor went further. <bookmark mark='a'/>The whole numbers and the "
            "fractions are countable. <bookmark mark='b'/>So are the algebraic numbers, the roots of polynomials "
            "with whole-number coefficients, because the polynomials themselves can be listed, size by size. "
            "<bookmark mark='c'/>But the real numbers are not countable: no list contains them all. "
            "<bookmark mark='d'/>So almost every real number is transcendental, not algebraic, a fact Cantor proved "
            "without exhibiting a single one. The next chapter gives his second, famous proof."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(cons))
        self.clear_scene()
