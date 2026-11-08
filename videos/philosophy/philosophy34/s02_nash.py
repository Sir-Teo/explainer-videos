from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class Nash(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Equilibrium", r"When are choices stable together?", lit=(1950,), part=PART)
        with self.voiceover("Chapter one. Equilibrium."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.definition()
        self.support()
        self.table()
        self.crossing()

    def definition(self):
        hc = history_card(1950, r"John Nash", r"``Equilibrium Points in $n$-Person Games''", width=6.2,
                          color=HIST).to_corner(UL, buff=0.3)
        f1 = MathTex(r"\sigma^* \text{ is a Nash equilibrium} \iff u_i(\sigma_i^*, \sigma_{-i}^*) \;\ge\; "
                     r"u_i(s_i, \sigma_{-i}^*) \quad \text{for every } i \text{ and every } s_i", font_size=30,
                     color=ROW).move_to([0, 1.0, 0])
        rows = stack([(r"no player can gain by changing strategy alone", GOAL),
                      (r"mixed strategies: \ probability distributions over acts", GREY_A),
                      (r"Nash \ (1950): \ every finite game has at least one, \ in mixed strategies", HIST),
                      (r"the proof: \ best responses form a correspondence with a fixed point \ (Kakutani, \ 1941)",
                       INST)], font_size=21, buff=0.28).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "In 1950 John Nash, a graduate student at Princeton, defined the central idea of game theory in a paper "
            "of one page. <bookmark mark='a'/>A profile of strategies is an equilibrium if no player can do better "
            "by changing her own strategy while the others keep theirs. <bookmark mark='b'/>Each is a best response "
            "to the rest. <bookmark mark='c'/>Strategies may be mixed, probability distributions over acts. "
            "<bookmark mark='d'/>Nash proved that every game with finitely many players and acts has at least one "
            "equilibrium in mixed strategies. <bookmark mark='e'/>The proof maps each profile to the set of best "
            "responses to it, and finds a profile that is a best response to itself, by Kakutani's fixed point "
            "theorem of 1941."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(f1))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            for mk, r in zip("cde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def support(self):
        head = label(r"Finding equilibria: \ support enumeration", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        steps = [(r"1", r"guess which acts each player uses: \ the supports", ROW),
                 (r"2", r"a mixed strategy is a best response only if every act it uses earns the same: \ "
                        r"solve those equations for the other's mixture", COL),
                 (r"3", r"keep solutions that are probabilities, \ with no unused act doing better", GOAL),
                 (r"cost", r"exponential in the number of acts: \ finding an equilibrium is PPAD-complete \ "
                           r"(Daskalakis, \ Goldberg and Papadimitriou; \ Chen and Deng, \ 2006)", BAD)]
        g = rows_table(steps, top=1.6, gap=0.5, width=8.6)
        f = MathTex(r"q\,a_{11} + (1-q)\,a_{12} \;=\; q\,a_{21} + (1-q)\,a_{22}", font_size=30,
                    color=COL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "How do you find equilibria? The Reasoner uses the oldest exact method, support enumeration. "
            "<bookmark mark='a'/>Guess which acts each player uses with positive probability: the supports. "
            "<bookmark mark='b'/>A mixture can be a best response only if every act in it earns the same. That gives "
            "linear equations for the other player's mixture: in a two by two game, the row player is indifferent "
            "exactly when q times one payoff plus one minus q times another balances. <bookmark mark='c'/>Keep the "
            "solutions that are genuine probabilities, and against which no unused act does better. "
            "<bookmark mark='d'/>The number of supports grows exponentially, and Constantinos Daskalakis, Paul "
            "Goldberg and Christos Papadimitriou showed in 2006, and Xi Chen and Xiaotie Deng for two players, that "
            "computing a Nash equilibrium is complete for the class PPAD: probably no fast algorithm exists. "
            "Equilibrium exists, but may be hard to find."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
                if mk == "b":
                    self.play(Write(f))
        self.clear_scene()

    def table(self):
        d = load("equilibria")
        head = label(r"Five games, \ solved", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        names = ["prisoner's dilemma", "matching pennies", "battle of the sexes", "stag hunt", "chicken"]
        assert [len(d[n]["equilibria"]) for n in names] == [1, 1, 3, 3, 3]
        assert d["chicken"]["equilibria"][2]["payoff"] == [4.6667, 4.6667]

        def show(eq, acts):
            r, c = eq["row"], eq["col"]
            if max(r) == 1 and max(c) == 1:
                return f"({acts[r.index(1.0)]}, {acts[c.index(1.0)]})"
            return f"row {r[0]:.2f}/{r[1]:.2f}, col {c[0]:.2f}/{c[1]:.2f}"
        hd = [r"\text{game}", r"\text{equilibria}", r"\text{payoffs}"]
        cells = []
        for n in names:
            eqs = d[n]["equilibria"]
            acts = d[n]["acts"]
            cells.append([label(n, font_size=18, color=ROW),
                          wrapped_label(r"; \ ".join(show(e, acts) for e in eqs), 6.2, 15, WHITE),
                          wrapped_label(r"; \ ".join(f"({e['payoff'][0]:g}, {e['payoff'][1]:g})" for e in eqs), 3.0,
                                        15, MONEY)])
        grid = ValueGrid(hd, cells, col_w=[3.2, 6.6, 3.2], cell_h=0.78, font_size=18).move_to([0, -0.3, 0])
        foot = label(r"pure equilibria where both best-respond; \ mixed ones where each makes the other indifferent",
                     font_size=18, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The Reasoner solves five classic games. <bookmark mark='a'/>The prisoner's dilemma has one equilibrium: "
            "both defect. <bookmark mark='b'/>Matching pennies has none in pure strategies, and one in which each "
            "player mixes half and half. <bookmark mark='c'/>The battle of the sexes, a couple who want to be "
            "together but prefer different evenings, has two pure equilibria and a mixed one in which each goes to "
            "their favourite two thirds of the time, and both do worse than in either pure one. "
            "<bookmark mark='d'/>The stag hunt has two pure equilibria and one mixed. <bookmark mark='e'/>And chicken, "
            "two drivers heading for each other, has two equilibria in which one swerves, and a mixed one worth four "
            "and two thirds to each. The next chapters take these games one at a time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, k in zip("abcde", range(5)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[k]], run_time=0.6)
            self.play(FadeIn(foot))
        self.clear_scene()

    def crossing(self):
        d = load("br")
        head = label(r"Best responses crossing: \ the battle of the sexes", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        assert (d["q_star"], d["p_star"]) == (0.3333, 0.6667) and len(d["equilibria"]) == 3
        A, B, acts = G.GAMES["battle of the sexes"]
        bm = bimatrix(A, B, acts, font_size=18, cell=1.0, center=[-5.0, 1.2, 0])
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=4.6, y_length=4.6, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True}).move_to([0.0, -0.4, 0])
        xl = label(r"$q$: \ column plays opera", font_size=16, color=COL).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"$p$: \ row plays opera", font_size=16, color=ROW).next_to(ax.y_axis, UP, buff=0.1)
        q, p = d["q_star"], d["p_star"]
        row_br = VMobject(color=ROW, stroke_width=5).set_points_as_corners(
            [ax.c2p(0, 0), ax.c2p(q, 0), ax.c2p(q, 1), ax.c2p(1, 1)])
        col_br = VMobject(color=COL, stroke_width=5).set_points_as_corners(
            [ax.c2p(0, 0), ax.c2p(0, p), ax.c2p(1, p), ax.c2p(1, 1)])
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.11, color=WHITE) for x, y in ((0, 0), (1, 1), (q, p))])
        side = stack([(r"row's best response: \ football if $q < 1/3$, \ opera if $q > 1/3$, \ anything at "
                       r"$q = 1/3$", ROW),
                      (r"column's: \ football if $p < 2/3$, \ opera above", COL),
                      (r"they cross three times: \ the three equilibria", GOAL),
                      (r"Kakutani: \ such correspondences, \ convex-valued with closed graphs, \ always cross", INST)],
                     font_size=17, aligned_edge=LEFT, width=3.8, buff=0.25).move_to([4.9, -0.2, 0])
        with self.voiceover(
            "Here is the picture behind Nash's proof. <bookmark mark='a'/>Let p be the probability that the row "
            "player goes to the opera, and q the column player's. <bookmark mark='b'/>The row player's best "
            "response is football when q is below a third, opera when it is above, and anything at all at exactly a "
            "third: a step, with a vertical piece. <bookmark mark='c'/>The column player's best response steps at p "
            "equal to two thirds. <bookmark mark='d'/>The two correspondences cross three times: at both playing "
            "football, both playing opera, and at the mixed point. <bookmark mark='e'/>Kakutani's theorem says that "
            "correspondences like these, whose values are convex and whose graphs are closed, must cross somewhere. "
            "That is why every finite game has an equilibrium."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bm))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("b")
            self.play(Create(row_br), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(col_br), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromCenter(x) for x in dots], lag_ratio=0.3), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()
