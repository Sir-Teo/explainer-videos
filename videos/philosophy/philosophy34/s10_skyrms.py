from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class Skyrms(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Dividing the cake", r"Could fairness evolve?", lit=(1996,), part=PART)
        with self.voiceover("Chapter nine. Dividing the cake."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.game()
        self.simplex()
        self.correlation()

    def game(self):
        d = load("demand")
        head = label(r"The Nash demand game", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        A = d["payoff"]
        assert A == [[0.3333, 0.3333, 0.3333], [0.5, 0.5, 0.0], [0.6667, 0.0, 0.0]]
        hd = [r"\text{you demand}", r"\text{other: } 1/3", r"\text{other: } 1/2", r"\text{other: } 2/3"]
        nm = [r"1/3", r"1/2", r"2/3"]
        cells = [[label(nm[i], font_size=21, color=ROW)] + [label(f"{A[i][j]:.2f}", font_size=20,
                                                                  color=OK if A[i][j] > 0 else BAD)
                                                            for j in range(3)] for i in range(3)]
        grid = ValueGrid(hd, cells, col_w=[2.4, 2.2, 2.2, 2.2], cell_h=0.6, font_size=19).move_to([-1.6, 0.4, 0])
        side = stack([(r"each of two demands a share of a cake", GREY_A),
                      (r"compatible demands \ (sum at most 1) \ are met; \ otherwise both get nothing", MONEY),
                      (r"equilibria: \ (1/2, 1/2), \ (1/3, 2/3), \ (2/3, 1/3)", GOAL),
                      (r"rationality alone does not pick the fair one", BAD)], font_size=18, aligned_edge=LEFT,
                     width=4.4, buff=0.3).move_to([4.6, 0.3, 0])
        with self.voiceover(
            "Brian Skyrms began his Evolution of the Social Contract, of 1996, with the simplest problem of "
            "justice. <bookmark mark='a'/>Two people divide a cake. Each demands a share: a third, a half, or two "
            "thirds. <bookmark mark='b'/>If the demands are compatible, each gets what she asked for; if they add up "
            "to more than the whole cake, both get nothing. <bookmark mark='c'/>Each pair of compatible demands "
            "that uses the whole cake is an equilibrium: half and half, but also a third against two thirds. "
            "<bookmark mark='d'/>Rationality alone does not choose the fair division. Could evolution?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for row in grid.cell for c in row])
            for mk, r in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def simplex(self):
        d = load("demand")
        head = label(r"Every starting population, \ run to its end", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["grid"] == 60 and d["fair"] == 1239 and d["polymorphic"] == 471 and d["fair_share"] == 0.7241
        size = 5.4
        o = np.array([-6.0, -2.6, 0])
        corners = [o, o + RIGHT * size, o + np.array([size / 2, size * math.sqrt(3) / 2, 0])]

        def P(a, b):
            c = 1 - a - b
            return a * corners[0] + b * corners[1] + c * corners[2]
        tri = Polygon(*corners, color=GREY_B, stroke_width=2)
        cl = VGroup(label(r"all demand 1/3", font_size=16, color=GREY_A).next_to(corners[0], DOWN, buff=0.12),
                    label(r"all demand 1/2", font_size=16, color=OK).next_to(corners[1], DOWN, buff=0.12),
                    label(r"all demand 2/3", font_size=16, color=GREY_A).next_to(corners[2], UP, buff=0.12))
        green, pink = VGroup(), VGroup()
        for a, b, e in d["points"]:
            (green if e == "fair" else pink).add(Dot(P(a, b), radius=0.035, color=OK if e == "fair" else DEFECT))
        side = stack([(r"a population of demanders; \ the replicator dynamics", GREY_A),
                      (r"green: \ ends with everyone demanding 1/2", OK),
                      (r"pink: \ ends in a polymorphism of 1/3 and 2/3 demanders", DEFECT),
                      (r"fair division: \ 1239 of 1711 starting points, \ 72\%", GOAL),
                      (r"the polymorphism wastes cake: \ 2/3 meets 2/3 and both get nothing", BAD)], font_size=18,
                     aligned_edge=LEFT, width=5.0, buff=0.3).move_to([3.8, -0.1, 0])
        with self.voiceover(
            "The Reasoner puts the game in a population, with the replicator dynamics of Part 19. "
            "<bookmark mark='a'/>Each point of the triangle is a population: its distance from each corner says what "
            "share demands a third, a half, or two thirds. <bookmark mark='b'/>The Reasoner runs every one of one "
            "thousand seven hundred and eleven starting points to its end. Green points end with everyone "
            "demanding half. <bookmark mark='c'/>Pink points end in a mixed population of modest and greedy "
            "demanders, who waste cake whenever two greedy ones meet. <bookmark mark='d'/>Fair division wins from "
            "seventy two percent of starting points: the largest basin, but not the whole triangle. "
            "<bookmark mark='e'/>Justice, in Skyrms's account, is not guaranteed by evolution, but it is favoured."
        ) as vo:
            self.play(FadeIn(head), Create(tri), FadeIn(cl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(green), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(pink), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def correlation(self):
        d = load("assort")
        head = label(r"Correlated encounters", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = d["rows"]
        assert [r["fair_share"] for r in rows] == [0.7274, 0.8826, 1.0, 1.0]
        f = MathTex(r"f_i \;=\; (1 - e)\,(A x)_i \;+\; e\, A_{ii}", font_size=32, color=COOP).next_to(head, DOWN,
                                                                                                buff=0.35)
        fl = label(r"with probability $e$ you meet someone of your own type", font_size=18, color=GREY_A).next_to(
            f, DOWN, buff=0.15)
        bars = VGroup()
        for k, r in enumerate(rows):
            h = 3.2 * r["fair_share"]
            b = Rectangle(width=1.2, height=h, stroke_width=0, fill_color=OK, fill_opacity=0.75)
            b.move_to([-4.8 + 1.8 * k, -2.6 + h / 2, 0])
            bars.add(VGroup(b, label(f"{100 * r['fair_share']:.0f}\\%", font_size=18, color=OK).next_to(b, UP,
                                                                                                    buff=0.08),
                            label(f"$e = {r['assort']:g}$", font_size=17, color=GREY_A).next_to(b, DOWN, buff=0.12)))
        side = stack([(r"fair demanders do best against their own kind; \ greedy ones worst", COOP),
                      (r"a little assortment, \ $e = 0.2$, \ and fair division wins from everywhere", OK),
                      (r"the coarse grid: \ 741 points", GREY_A),
                      (r"Skyrms: \ the structure of interaction, \ who meets whom, \ shapes which conventions of "
                       r"justice evolve", HIST)], font_size=18, aligned_edge=LEFT, width=4.6, buff=0.3).move_to(
            [4.0, -1.2, 0])
        with self.voiceover(
            "Real people do not meet at random. <bookmark mark='a'/>Suppose that with probability e you meet someone "
            "of your own type. <bookmark mark='b'/>Fair demanders do well against each other, and greedy demanders "
            "worst of all. <bookmark mark='c'/>With no correlation, fair division wins from seventy three percent of "
            "the triangle, on a coarser grid. With e of a tenth, eighty eight percent. With a fifth, all of it. "
            "<bookmark mark='d'/>Skyrms's lesson is that the structure of interaction, who meets whom, shapes which "
            "conventions of justice evolve, a theme Part 38 returns to with Rawls."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.3), FadeIn(side[1]), FadeIn(side[2]),
                      run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
