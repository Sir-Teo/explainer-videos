from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class Bargaining(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Bargaining", r"Is there a fair way to split a surplus?", lit=(1950, 1982),
                            part=PART)
        with self.voiceover("Chapter ten. Bargaining."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.axioms()
        self.solutions()
        self.rubinstein()

    def axioms(self):
        hc = history_card(1950, r"John Nash", r"``The Bargaining Problem''", width=5.0, color=HIST).to_corner(
            UL, buff=0.3)
        rows = [(r"efficiency", r"no other agreement is better for both", COOP),
                (r"symmetry", r"if the problem is symmetric, \ so is the solution", ROW),
                (r"scale invariance", r"rescaling a player's utility rescales her share, \ nothing else", COL),
                (r"independence of irrelevant alternatives", r"removing options that were not chosen does not change "
                                                             r"the choice", INST),
                (r"the theorem", r"exactly one solution: \ maximize the product of gains over the disagreement point, "
                                 r"\ $\max\, (u_1 - d_1)(u_2 - d_2)$", GOAL)]
        g = rows_table(rows, top=1.1, gap=0.4, width=7.4, x_text=-1.2, label_size=20, text_size=19)
        with self.voiceover(
            "Nash's second great paper, of 1950, asked how two people should split a surplus, if each can refuse "
            "and fall back on a disagreement point. He answered with axioms. <bookmark mark='a'/>The agreement "
            "should be efficient: nothing else better for both. <bookmark mark='b'/>Symmetric problems get symmetric "
            "solutions. <bookmark mark='c'/>Rescaling a player's utility should not change the real outcome. "
            "<bookmark mark='d'/>And removing options that were not chosen should not change the choice. "
            "<bookmark mark='e'/>Exactly one rule satisfies all four: choose the agreement that maximizes the product "
            "of the two players' gains over disagreement."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def solutions(self):
        d = load("bargaining")
        head = label(r"Two solutions, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["nash_x"], d["nash_u2"], d["ks_x"], d["ks_u2"]) == (0.6667, 0.5773, 0.618, 0.618)
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=4.8, y_length=4.8, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True}).move_to([-3.0, -0.4, 0])
        xl = label(r"$u_1 = x$", font_size=17, color=ROW).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"$u_2 = \sqrt{1 - x}$", font_size=17, color=COL).next_to(ax.y_axis, UP, buff=0.1)
        front = VMobject(color=GREY_A, stroke_width=3).set_points_smoothly([ax.c2p(a, b) for a, b in d["frontier"]])
        region = Polygon(ax.c2p(0, 0), *[ax.c2p(a, b) for a, b in d["frontier"]], ax.c2p(1, 0), stroke_width=0,
                         fill_color=GREY_D, fill_opacity=0.35)
        hyper = VMobject(color=GOAL, stroke_width=2).set_points_smoothly(
            [ax.c2p(x, d["nash_x"] * d["nash_u2"] / x) for x in np.linspace(0.39, 1.0, 40)])
        ns = Dot(ax.c2p(d["nash_x"], d["nash_u2"]), radius=0.09, color=GOAL)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=INST)
        ks = Dot(ax.c2p(d["ks_x"], d["ks_u2"]), radius=0.09, color=INST)
        side = stack([(r"split a dollar; \ player 2 is risk averse: \ $u_2 = \sqrt{1 - x}$", GREY_A),
                      (r"Nash: \ maximize $x\sqrt{1 - x}$: \ $x = 2/3$", GOAL),
                      (r"the risk-averse player gets less money", BAD),
                      (r"Kalai and Smorodinsky \ (1975): \ equal shares of each one's best possible gain: \ "
                       r"$x = \sqrt{1 - x}$, \ $x = 0.618$", INST),
                      (r"they drop independence of irrelevant alternatives for monotonicity", GREY_A)],
                     font_size=18, aligned_edge=LEFT, width=5.2, buff=0.28).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "The Reasoner applies the rule. <bookmark mark='a'/>Two players split a dollar. Player one values money "
            "linearly; player two is risk averse, with the square root of what she gets. "
            "<bookmark mark='b'/>Nash's solution maximizes the product, x times the square root of one minus x: "
            "player one gets two thirds of the dollar. <bookmark mark='c'/>The risk-averse player gets less money: "
            "fearing disagreement more, she is the weaker bargainer, which some find a reason to call the solution "
            "unfair. "
            "<bookmark mark='d'/>Ehud Kalai and Meir Smorodinsky proposed in 1975 to give each player the same share "
            "of her best possible gain. Here that is the point on the diagonal, sixty two cents to player one. "
            "<bookmark mark='e'/>They keep the other axioms but replace independence of irrelevant alternatives "
            "with monotonicity. Different axioms, different fairness."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(region), Create(front), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(hyper), FadeIn(ns), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(diag), FadeIn(ks), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def rubinstein(self):
        d = load("bargaining")
        head = label(r"Alternating offers \ (Rubinstein, \ 1982)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rub = d["rubinstein"]
        assert [r["first"] for r in rub] == [0.6667, 0.5556, 0.5263, 0.5128, 0.5025]
        f1 = MathTex(r"x \;=\; 1 - \delta x \;\Longrightarrow\; x^* = \frac{1}{1 + \delta}", font_size=34,
                     color=ROW).move_to([-2.6, 1.4, 0])
        fl = label(r"the first mover offers the other exactly what she would get by waiting a round", font_size=18,
                   color=GREY_A).next_to(f1, DOWN, buff=0.25)
        hd = [r"\delta", r"\text{first mover's share}"]
        cells = [[label(f"{r['delta']:g}", font_size=20, color=GREY_A), label(f"{r['first']:.4f}", font_size=20,
                                                                             color=ROW)] for r in rub]
        grid = ValueGrid(hd, cells, col_w=[1.8, 3.4], cell_h=0.52, font_size=18).move_to([-2.6, -1.6, 0])
        side = stack([(r"a unique subgame-perfect equilibrium, \ agreed at once", GOAL),
                      (r"patience is power: \ the less you discount, \ the more you get", ROW),
                      (r"as $\delta \to 1$ the split tends to 1/2: \ the Nash solution", INST),
                      (r"Binmore, \ Rubinstein and Wolinsky \ (1986): \ Nash's axioms, \ derived from a game of "
                       r"offers", HIST)], font_size=18, aligned_edge=LEFT, width=4.8, buff=0.3).move_to([3.8, -0.2, 0])
        with self.voiceover(
            "Axioms say what a fair agreement looks like. Ariel Rubinstein, in 1982, modelled the haggling itself. "
            "<bookmark mark='a'/>Two players take turns proposing splits of a dollar; each round of delay shrinks "
            "its value by a factor delta. The first mover offers the other exactly what she could get by refusing "
            "and making the next offer, so her share solves x equals one minus delta x. <bookmark mark='b'/>There is "
            "a unique subgame perfect equilibrium, and agreement is immediate. <bookmark mark='c'/>With delta a "
            "half, the first mover takes two thirds; with point nine, fifty three percent. Patience is power. "
            "<bookmark mark='d'/>As delta tends to one the split tends to a half: Ken Binmore, Rubinstein and Asher "
            "Wolinsky showed in 1986 that the Nash solution is the limit of such games. The axioms and the haggling "
            "meet."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for row in grid.cell for c in row])
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()
