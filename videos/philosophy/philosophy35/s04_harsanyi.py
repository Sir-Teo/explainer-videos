from __future__ import annotations

from videos.philosophy.philosophy35.common import *  # noqa: F403


class Harsanyi(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Harsanyi's theorem", r"Does rationality force utilitarianism?", lit=(1955,),
                            part=PART)
        with self.voiceover("Chapter three. Harsanyi's theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.theorem()
        self.broken()
        self.frontier()

    def theorem(self):
        hc = history_card(1955, r"John Harsanyi", r"``Cardinal Welfare, \ Individualistic Ethics, \ and Interpersonal "
                                                  r"Comparisons of Utility''", width=7.6, color=HIST).to_corner(UL,
                                                                                                         buff=0.3)
        rows = [(r"individuals", r"each person's preferences over lotteries satisfy the vNM axioms of Part 33", GOOD),
                (r"society", r"society's preferences over lotteries satisfy them too", AGG),
                (r"Pareto", r"if every person is indifferent between two lotteries, \ so is society", DUTY),
                (r"the theorem", r"then social utility is a weighted sum of individual utilities: \ $W = \sum_i a_i\, "
                                 r"u_i$", GOAL)]
        g = rows_table(rows, top=1.2, gap=0.5, width=8.0, x_text=-2.2)
        with self.voiceover(
            "In 1955 John Harsanyi, who later shared the Nobel prize for game theory, proved a theorem that seems to "
            "derive utilitarianism from rationality alone. <bookmark mark='a'/>Suppose each person's preferences over "
            "risky prospects satisfy the von Neumann–Morgenstern axioms of Part 33. <bookmark mark='b'/>Suppose "
            "society's preferences do too: a society should choose among risky policies as a rational agent would. "
            "<bookmark mark='c'/>And suppose the Pareto principle: if everyone is indifferent between two prospects, "
            "society is too. <bookmark mark='d'/>Then society's utility must be a weighted sum of individual "
            "utilities. Add that people count equally, and the weights are equal: utilitarianism."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def broken(self):
        d = load("harsanyi")
        head = label(r"Try a nonlinear rule, \ and something breaks", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["ex_ante"] == {"sure (1, 0)": 0.0, "sure (0, 1)": 0.0, "50:50 mixture": 0.5}
        assert d["ex_post"] == {"50:50 of (1, 0) and (0, 1)": 0.0, "sure (0.5, 0.5)": 0.5}
        assert d["individual"]["50:50 of (1, 0) and (0, 1)"] == [0.5, 0.5]
        l1 = label(r"ex ante egalitarian: \ $W = \min(\mathbb{E}u_1, \mathbb{E}u_2)$", font_size=22, color=AGG)
        r1 = VGroup(label(r"sure (1, 0): \ $W = 0$", font_size=19), label(r"sure (0, 1): \ $W = 0$", font_size=19),
                    label(r"their 50:50 mixture: \ $W = 0.5$", font_size=19, color=BAD)).arrange(DOWN, buff=0.15,
                                                                                               aligned_edge=LEFT)
        n1 = label(r"a mixture of two equally good prospects is strictly better: \ society violates vNM \ (Diamond, "
                   r"\ 1967: \ so much the worse for vNM)", font_size=18, color=BAD)
        l2 = label(r"ex post egalitarian: \ $W = \mathbb{E}[\min(u_1, u_2)]$", font_size=22, color=AGG)
        r2 = VGroup(label(r"50:50 of (1, 0) and (0, 1): \ $W = 0$", font_size=19),
                    label(r"sure (0.5, 0.5): \ $W = 0.5$", font_size=19, color=BAD)).arrange(DOWN, buff=0.15,
                                                                                         aligned_edge=LEFT)
        n2 = label(r"yet each person expects 0.5 from both: \ society violates Pareto", font_size=18, color=BAD)
        left = VGroup(l1, r1, n1).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        right = VGroup(l2, r2, n2).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        VGroup(left, right).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([0, -0.3, 0])
        with self.voiceover(
            "The theorem has force because the alternatives fail in precise ways. Take two people, and an "
            "egalitarian who cares about the worse off. <bookmark mark='a'/>Applied before the risk is resolved, "
            "equality ranks prospects by the smaller of the two expected utilities. A sure outcome of one for the "
            "first person and nothing for the second scores zero; so does the reverse. But a fifty fifty mixture of "
            "the two scores a half, since each person then expects a half. <bookmark mark='b'/>Society strictly "
            "prefers a mixture of two prospects it ranks equal, which no von Neumann–Morgenstern agent can do. Peter "
            "Diamond argued in 1967 that this is exactly right: tossing a coin is fairer, so much the worse for the "
            "axioms. "
            "<bookmark mark='c'/>Applied after the risk is resolved, equality ranks a prospect by the expected "
            "minimum. A coin flip over the two lopsided outcomes scores zero; a sure half each scores a half. "
            "<bookmark mark='d'/>But each person expects a half from either, so each is indifferent, and society "
            "violates the Pareto principle. Harsanyi's theorem says one of these failures is unavoidable for any "
            "rule that is not a weighted sum."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(l1), FadeIn(r1))
            vo.wait_until("b")
            self.play(FadeIn(n1))
            vo.wait_until("c")
            self.play(FadeIn(l2), FadeIn(r2))
            vo.wait_until("d")
            self.play(FadeIn(n2))
        self.clear_scene()

    def frontier(self):
        d = load("harsanyi")
        head = label(r"The possibility frontier, \ and three ways to choose on it", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        assert d["utilitarian"] == [0.5, 0.75] and d["egalitarian"] == [0.618, 0.618] and d["nash"] == [0.5774,
                                                                                                   0.6667]
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=4.8, y_length=4.8, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True}).move_to([-3.0, -0.4, 0])
        xl = label(r"$u_1$", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"$u_2$", font_size=18, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1)
        fr = VMobject(color=GREY_A, stroke_width=3).set_points_smoothly([ax.c2p(a, b) for a, b in d["frontier"]])
        region = Polygon(ax.c2p(0, 0), *[ax.c2p(a, b) for a, b in d["frontier"]], stroke_width=0, fill_color=GREY_D,
                         fill_opacity=0.35)
        u = d["utilitarian"]
        line = DashedLine(ax.c2p(max(0, u[0] + u[1] - 1), 1), ax.c2p(1, u[0] + u[1] - 1), color=GOOD)
        pts = VGroup(Dot(ax.c2p(*u), radius=0.09, color=GOOD), Dot(ax.c2p(*d["egalitarian"]), radius=0.09, color=AGG),
                     Dot(ax.c2p(*d["nash"]), radius=0.09, color=VIRT))
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=AGG, stroke_width=1.5)
        side = stack([(r"the frontier: \ $u_2 = 1 - u_1^2$", GREY_A),
                      (r"utilitarian: \ maximize $u_1 + u_2$: \ (0.50, 0.75), \ total 1.25", GOOD),
                      (r"egalitarian: \ equal utilities: \ (0.62, 0.62), \ total 1.24", AGG),
                      (r"Nash product: \ (0.58, 0.67)", VIRT),
                      (r"Sen \ (1973): \ the sum ignores who gets what", HARM)], font_size=18, aligned_edge=LEFT,
                     width=4.8, buff=0.3).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "Here is the geometry. <bookmark mark='a'/>The set of achievable pairs of utilities is bounded by a "
            "frontier; here the second person's utility is one minus the square of the first's. "
            "<bookmark mark='b'/>A weighted sum is a family of straight lines, and the utilitarian choice is where "
            "the highest line touches the frontier: a half for the first person and three quarters for the second. "
            "<bookmark mark='c'/>An egalitarian chooses the point on the diagonal, a little less in total. "
            "<bookmark mark='d'/>Nash's bargaining rule of Part 34 lies between. <bookmark mark='e'/>Amartya Sen "
            "objected in 1973 that the sum is indifferent to who gets what. The next chapter takes that objection "
            "seriously."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(region), Create(fr), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(pts[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(diag), FadeIn(pts[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
