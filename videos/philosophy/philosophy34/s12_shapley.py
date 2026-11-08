from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class Shapley(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"The Shapley value", r"What is each member of a coalition owed?", lit=(1953,),
                            part=PART)
        with self.voiceover("Chapter eleven. The Shapley value."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.axioms()
        self.gloves()
        self.uniqueness()
        self.shap()

    def axioms(self):
        hc = history_card(1953, r"Lloyd Shapley", r"``A Value for $n$-Person Games''", width=5.4,
                          color=HIST).to_corner(UL, buff=0.3)
        f = MathTex(r"\phi_i(v) \;=\; \frac{1}{n!}\sum_{\text{orders } \pi} \Big(v\big(P_i^\pi \cup \{i\}\big) - "
                    r"v\big(P_i^\pi\big)\Big)", font_size=32, color=INST).move_to([0, 1.2, 0])
        fl = label(r"$P_i^\pi$: \ the players who arrive before $i$ in the order $\pi$", font_size=18,
                   color=GREY_A).next_to(f, DOWN, buff=0.2)
        rows = stack([(r"efficiency: \ the values add up to $v$ of everyone", COOP),
                      (r"symmetry: \ interchangeable players get the same", ROW),
                      (r"null player: \ one who adds nothing to any coalition gets nothing", COL),
                      (r"additivity: \ the value of two games together is the sum of their values", MONEY),
                      (r"Shapley: \ exactly one rule satisfies all four: \ the average marginal contribution", GOAL)],
                     font_size=19, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Cooperative game theory asks what a group can achieve together, and how to share it. A game assigns a "
            "value v to every coalition. In 1953 Lloyd Shapley, who shared the Nobel prize in 2012, gave an answer. "
            "<bookmark mark='a'/>Line the players up in every possible order. Each one's marginal contribution is "
            "what the coalition gains when she arrives. Her value is the average of those contributions over all "
            "orders. <bookmark mark='b'/>It is the only rule with four properties: the values add up to what the "
            "whole group can make; <bookmark mark='c'/>interchangeable players get the same; "
            "<bookmark mark='d'/>a player who adds nothing to any coalition gets nothing; <bookmark mark='e'/>and the "
            "value of two games played together is the sum of their values. <bookmark mark='f'/>Four plausible "
            "axioms, one formula."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            for mk, r in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def gloves(self):
        d = load("shapley")
        head = label(r"The glove game", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["glove"] == {"L": 0.6667, "R1": 0.1667, "R2": 0.1667} and d["glove_core"] == [[1.0, 0.0, 0.0]]
        gl = VGroup(*[VGroup(RoundedRectangle(width=1.4, height=1.0, corner_radius=0.2, color=c, fill_opacity=0.2),
                             label(t, font_size=20, color=c)) for t, c in ((r"L", ROW), (r"R$_1$", COL),
                                                                           (r"R$_2$", COL))]).arrange(RIGHT, buff=0.6)
        for g in gl:
            g[1].move_to(g[0])
        gl.move_to([-3.4, 1.2, 0])
        rule = label(r"a left and a right glove make a pair worth 1", font_size=18, color=GREY_A).next_to(gl, DOWN,
                                                                                                    buff=0.3)
        hd = [r"\text{order}", r"\text{L adds}", r"\text{R}_1 \text{ adds}", r"\text{R}_2 \text{ adds}"]
        orders = [("L R1 R2", (0, 1, 0)), ("L R2 R1", (0, 0, 1)), ("R1 L R2", (1, 0, 0)), ("R1 R2 L", (1, 0, 0)),
                  ("R2 L R1", (1, 0, 0)), ("R2 R1 L", (1, 0, 0))]
        cells = [[label(o.replace("R1", r"R$_1$").replace("R2", r"R$_2$"), font_size=17, color=GREY_A)] +
                 [label(str(x), font_size=18, color=ROW if j == 0 else COL) for j, x in enumerate(m)]
                 for o, m in orders]
        grid = ValueGrid(hd, cells, col_w=[2.4, 1.6, 1.6, 1.6], cell_h=0.42, font_size=16).move_to([-3.2, -1.7, 0])
        side = stack([(r"Shapley: \ L gets 4/6 = 2/3; \ each R gets 1/6", INST),
                      (r"the core \ (Gillies, \ 1959): \ allocations no coalition can improve on by leaving", GREY_A),
                      (r"here the core is a single point: \ (1, 0, 0): \ the scarce glove takes everything", BAD),
                      (r"Shapley rewards being needed; \ the core rewards bargaining power", GOAL)], font_size=18,
                     aligned_edge=LEFT, width=5.0, buff=0.3).move_to([3.8, -0.2, 0])
        with self.voiceover(
            "A small example shows what the value measures. <bookmark mark='a'/>One player holds a left glove, two "
            "hold right gloves, and a pair is worth one. <bookmark mark='b'/>Over the six orders of arrival, the left "
            "glove completes a pair in four of them, and each right glove in one. So the left glove is worth two "
            "thirds, and each right glove a sixth. <bookmark mark='c'/>A different solution, the core, asks for "
            "allocations that no coalition could improve on by going off alone. <bookmark mark='d'/>The Reasoner "
            "searches every allocation: the core here is a single point, giving the scarce left glove everything, "
            "since the two right-glove holders compete each other down to nothing. <bookmark mark='e'/>The core "
            "tracks bargaining power; the Shapley value tracks how much each player is needed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gl), FadeIn(rule))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for row in grid.cell for c in row])
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def uniqueness(self):
        head = label(r"Why the value is unique", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f1 = MathTex(r"u_T(S) = \begin{cases} 1 & T \subseteq S \\ 0 & \text{otherwise} \end{cases}", font_size=32,
                     color=ROW)
        f2 = MathTex(r"v \;=\; \sum_{T \neq \emptyset} d_v(T)\, u_T, \qquad d_v(T) = \sum_{S \subseteq T} "
                     r"(-1)^{|T| - |S|}\, v(S)", font_size=30, color=INST)
        f3 = MathTex(r"\phi_i(v) \;=\; \sum_{T \ni i} \frac{d_v(T)}{|T|}", font_size=34, color=GOAL)
        g = VGroup(f1, f2, f3).arrange(DOWN, buff=0.45).move_to([0, 0.3, 0])
        notes = stack([(r"in a unanimity game, \ only the members of $T$ matter, \ and they are symmetric: \ "
                        r"each gets $1/|T|$", ROW),
                       (r"every game is a sum of unanimity games, \ weighted by Harsanyi's dividends", INST),
                       (r"additivity then forces the formula: \ each coalition's dividend split equally among its "
                        r"members", GOAL)], font_size=18, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The proof that the four axioms fix the value is short. <bookmark mark='a'/>Take a unanimity game, in "
            "which a coalition is worth one if it contains every member of some set T, and nothing otherwise. Players "
            "outside T are null, and those inside are interchangeable, so each member of T must get one over the "
            "size of T. <bookmark mark='b'/>Every game can be written as a sum of unanimity games, with weights John "
            "Harsanyi called dividends: what each coalition adds beyond its subcoalitions. "
            "<bookmark mark='c'/>Additivity then forces the formula: every coalition's dividend is shared equally "
            "among its members."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Write(f3), FadeIn(notes[2]))
        self.clear_scene()

    def shap(self):
        d = load("shapley")
        head = label(r"From coalitions to features: \ SHAP", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["shap"] == {"x1": 1.0, "x2": 1.0, "x3": 1.0} and d["model_value"] == 3.0
        assert d["dividends"] == {"1": 1.0, "23": 2.0}
        f = MathTex(r"f(x) = x_1 + 2\,x_2 x_3, \qquad x = (1, 1, 1), \quad \text{baseline } (0, 0, 0)", font_size=30,
                    color=MONEY).next_to(head, DOWN, buff=0.35)
        bars = VGroup()
        for k, (n, v) in enumerate(d["shap"].items()):
            b = Rectangle(width=1.0, height=1.2 * v, stroke_width=0, fill_color=[ROW, COL, COOP][k], fill_opacity=0.8)
            b.move_to([-4.6 + 1.5 * k, -1.2 + b.height / 2, 0])
            bars.add(VGroup(b, label(f"{v:.0f}", font_size=20, color=WHITE).next_to(b, UP, buff=0.08),
                            MathTex(f"x_{k + 1}", font_size=26, color=[ROW, COL, COOP][k]).next_to(b, DOWN,
                                                                                                buff=0.12)))
        bl = label(r"Shapley values of the three features: \ 1 + 1 + 1 = $f(x) - f(0) = 3$", font_size=17,
                   color=GREY_A).next_to(bars, DOWN, buff=0.4)
        side = stack([(r"Lundberg and Lee \ (2017): \ players are features, \ $v(S)$ the prediction with only $S$ "
                       r"known", INST),
                      (r"dividends: \ $x_1$ alone 1; \ $x_2$ with $x_3$ 2, \ split equally", GOAL),
                      (r"limits: \ the answer depends on the baseline and on how missing features are filled in", BAD),
                      (r"with correlated features it can credit a variable the model never reads \ (Kumar et al., \ "
                       r"2020): \ Part 41", HIST)], font_size=18, aligned_edge=LEFT, width=5.6, buff=0.28).move_to(
            [3.2, -0.6, 0])
        with self.voiceover(
            "Sixty years later the Shapley value became the most used tool for explaining machine learning models. "
            "<bookmark mark='a'/>Scott Lundberg and Su-In Lee, in 2017, treated a model's input features as players, "
            "and a coalition's value as the model's prediction when only those features are known. "
            "<bookmark mark='b'/>Take the model x one plus two x two x three, at the input one one one, against a "
            "baseline of zeros. The Reasoner computes each feature's Shapley value: one, one and one, adding up to "
            "the prediction's rise of three. <bookmark mark='c'/>The dividends explain it: x one alone contributes "
            "one, and x two and x three together contribute two, which the value splits equally between them. "
            "<bookmark mark='d'/>The answer depends on the baseline, and on how the missing features are filled in. "
            "<bookmark mark='e'/>With correlated features, it can credit a variable the model never reads, as "
            "I. Elizabeth Kumar and colleagues showed in 2020. Part 41 asks what an explanation should be."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Write(f))
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.2),
                      *[FadeIn(b[1:]) for b in bars], FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()
