from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

GONE = GREY_D


class Dominance(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Strategic form and dominance: \ how deep did you think?", r"Which choices can a rational "
             r"player rule out, and what is left?", "Chapter two. Strategic form and dominance: how deep did you "
             "think?", lit={1944: r"von Neumann and Morgenstern"}, scale=("person",))
        self.strategic()
        self.iterate()
        self.descent()

    def strategic(self):
        gr = load("grammar")["pd"]
        A = np.array(gr["A"])
        mat = matrix(A, A.T, [r"cooperate", r"defect"], [r"cooperate", r"defect"], cell_w=2.2, cell_h=1.0,
                     font_size=30).shift(LEFT * 2.8 + DOWN * 0.2)
        side = VGroup(
            label(r"a game in strategic form: \ players, \ strategies, \ payoffs", font_size=23),
            label(r"in each cell: \ Ana's payoff, \ then Bo's", font_size=22, color=GREY_A),
            label(r"if Bo cooperates, \ Ana does better defecting: \ 5 against 3", font_size=22, color=ANA),
            label(r"if Bo defects, \ again: \ 1 against 0", font_size=22, color=ANA),
            label(r"defect \emph{dominates} cooperate, \ for both of them", font_size=23, color=DEFECT),
            label(r"so both defect and get 1, \\ though both cooperating would give each 3", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        f1 = frame_cell(mat, 1, 0, ANA)
        f2 = frame_cell(mat, 1, 1, ANA)
        f3 = frame_cell(mat, 1, 1, EQ, 6)
        f4 = frame_cell(mat, 0, 0, COOP, 4)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Game theory writes such a situation down in a table, called the strategic form: who plays, what each "
            "can do, and what each gets. <bookmark mark='a'/> Here is the prisoner's dilemma with Ana and Bo. In "
            "each cell, the first number is Ana's payoff and the second is Bo's. <bookmark mark='b'/> If Bo "
            "cooperates, Ana does better by defecting: five against three. <bookmark mark='c'/> If Bo defects, she "
            "still does better by defecting: one against nought. <bookmark mark='d'/> Whatever Bo does, defecting "
            "is better. We say that defect dominates cooperate, and the same is true for Bo. "
            "<bookmark mark='e'/> So both defect, and each gets one, though if both had cooperated, each would have "
            "had three. Each player's sensible choice adds up to an outcome both dislike."
        ) as vo:
            self.play(FadeIn(mat), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(f1), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(ReplacementTransform(f1, f2), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
            vo.wait_until("e")
            self.play(ReplacementTransform(f2, f3), Create(f4), FadeIn(side[5]))
        self.clear_scene()

    def iterate(self):
        d = load("dominance")
        A, B = np.array(d["A"]), np.array(d["B"])
        mat = matrix(A, B, [r"up", r"down"], [r"left", r"middle", r"right"], cell_w=1.55, cell_h=0.95,
                     font_size=26).shift(LEFT * 3.7 + UP * 0.2)

        def dim_col(j):
            return [m.animate.set_opacity(0.2) for m in (mat.pay[0][j], mat.pay[1][j], mat.col_labels[j])]

        def dim_row(i):
            return [m.animate.set_opacity(0.2) for m in (*mat.pay[i], mat.row_labels[i])]

        side = VGroup(
            label(r"a game with nothing dominant at first sight", font_size=22),
            label(r"for Bo, \ middle beats right whatever Ana does: \ $2 > 1$, \ $1 > 0$", font_size=21, color=COLC),
            label(r"with right gone, \ up beats down for Ana: \ $1 > 0$, \ $1 > 0$", font_size=21, color=ROWC),
            label(r"with down gone, \ middle beats left for Bo: \ $2 > 0$", font_size=21, color=COLC),
            label(r"one cell is left: \ up, middle", font_size=24, color=EQ),
            label(r"each step needs one more layer of \\ \emph{I know that you know that I am rational}",
                  font_size=22, color=LEVEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        fin = frame_cell(mat, 0, 1, EQ, 6)
        tag = published_tag(r"the example is from Gibbons, \emph{A Primer in Game Theory} (1992), \S 1.1", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Dominance can be applied over and over. <bookmark mark='a'/> In this game, neither player has a "
            "strategy that is best whatever the other does. <bookmark mark='b'/> But for Bo, the middle column is "
            "better than the right one whatever Ana does, so a rational Bo never plays right. "
            "<bookmark mark='c'/> If Ana knows that, she can cross the right column out, and then up is better for "
            "her than down. <bookmark mark='d'/> If Bo knows that Ana knows, he crosses out down, and then middle "
            "beats left. <bookmark mark='e'/> One cell survives: up, middle. This is the iterated elimination of "
            "dominated strategies. <bookmark mark='f'/> Notice what each step needs: not just that the players are "
            "rational, but that each knows the other is, and knows that the other knows, one layer deeper each time."
        ) as vo:
            self.play(FadeIn(mat), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*dim_col(2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*dim_row(1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(*dim_col(0), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(fin), FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def descent(self):
        g = load("guess")
        bounds = g["bounds"][:7]
        line = NumberLine(x_range=[0, 100, 10], length=11.0, include_numbers=True, font_size=22, color=GREY_B
                          ).move_to(UP * 1.4)
        bars = VGroup()
        for k, b in enumerate(bounds):
            r = Rectangle(width=line.n2p(b)[0] - line.n2p(0)[0], height=0.24, stroke_width=0,
                          fill_color=interpolate_color(ManimColor(ANA), ManimColor(EQ), k / 6), fill_opacity=0.75)
            r.move_to(line.n2p(0), aligned_edge=LEFT).shift(DOWN * (0.55 + 0.36 * k))
            t = label(rf"{b:.1f}" if k else r"100", font_size=17, color=GREY_A).next_to(r, RIGHT, buff=0.1)
            bars.add(VGroup(r, t))
        rows = VGroup(
            label(r"two-thirds of an average can never exceed 66.7: \ anything higher is dominated", font_size=22),
            label(r"if nobody goes above 66.7, \ the target can't exceed 44.4; \ then 29.6, \ 19.8, \dots",
                  font_size=22),
            label(r"all the way down: \ the only choice that survives every round is 0", font_size=23, color=EQ),
            label(r"Nagel's first rounds: \ only 6 to 10\% of choices went three steps or more", font_size=22,
                  color=LEVEL),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Nagel, AER 85(5) (1995), section IV.A", corner=DR, font_size=13)
        with self.voiceover(
            "The guessing game works the same way, with numbers. <bookmark mark='a'/> Two-thirds of any average is "
            "at most sixty-six point seven, so a number above that can never win: it is dominated. "
            "<bookmark mark='b'/> If nobody chooses above sixty-six point seven, the target can be at most forty-four "
            "point four, so higher numbers are out too. Then twenty-nine point six, then nineteen point eight, and so "
            "on. <bookmark mark='c'/> Every round of reasoning cuts the range by a third, and the only number that "
            "survives them all is nought. <bookmark mark='d'/> Real people stop much sooner. In Nagel's first rounds, "
            "only six to ten percent of the choices reflected three or more steps."
        ) as vo:
            self.play(Create(line), FadeIn(tag), FadeIn(bars[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars[2:5]], lag_ratio=0.5),
                      FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars[5:]], lag_ratio=0.5),
                      FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
