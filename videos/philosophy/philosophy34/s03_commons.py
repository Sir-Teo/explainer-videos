from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class Commons(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"The dilemma and the commons", r"Why do rational people ruin what they share?",
                            lit=(1950, 1968, 1990), part=PART)
        with self.voiceover("Chapter two. The dilemma and the commons."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.dilemma()
        self.hobbes()
        self.commons()
        self.ostrom()

    def dilemma(self):
        d = load("equilibria")["prisoner's dilemma"]
        head = label(r"The prisoner's dilemma \ (Flood and Dresher, \ 1950; \ Tucker)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        assert d["equilibria"] == [{"row": [0.0, 1.0], "col": [0.0, 1.0], "payoff": [1.0, 1.0]}]
        bm = bimatrix(d["A"], d["B"], d["acts"], font_size=22, cell=1.4, center=[-3.4, 0.0, 0])
        dom = VGroup(Arrow(bm.cells[0].get_center() + DOWN * 0.3, bm.cells[2].get_center() + UP * 0.3, buff=0,
                           color=DEFECT, stroke_width=4),
                     Arrow(bm.cells[1].get_center() + DOWN * 0.3, bm.cells[3].get_center() + UP * 0.3, buff=0,
                           color=DEFECT, stroke_width=4))
        nash = SurroundingRectangle(bm.cells[3], color=BAD, buff=0.05)
        best = SurroundingRectangle(bm.cells[0], color=OK, buff=0.05)
        side = stack([(r"5 > 3 \ and \ 1 > 0: \ defecting is better whatever the other does", DEFECT),
                      (r"so both defect: \ the only equilibrium, \ (1, 1)", BAD),
                      (r"yet both prefer (3, 3)", OK),
                      (r"RAND, \ 1950: \ Flood and Dresher's subjects mostly cooperated anyway", HIST)],
                     font_size=19, aligned_edge=LEFT, width=5.4, buff=0.3).move_to([3.4, 0.0, 0])
        with self.voiceover(
            "In 1950 Merrill Flood and Melvin Dresher, at the RAND Corporation, found a game whose equilibrium "
            "everyone regrets, and Albert Tucker gave it its story of two prisoners. <bookmark mark='a'/>Each player "
            "cooperates or defects. Both cooperating earns three each; both defecting, one each; a defector against "
            "a cooperator earns five, and the cooperator nothing. <bookmark mark='b'/>Whatever the other does, "
            "defecting pays more: five rather than three, one rather than nothing. <bookmark mark='c'/>So both "
            "defect, and the only equilibrium pays one each, <bookmark mark='d'/>though both would prefer three. "
            "<bookmark mark='e'/>When Flood and Dresher had two colleagues play it a hundred times, they cooperated "
            "far more than the theory said they should, which already hinted at the role of repetition."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bm))
            vo.wait_until("b")
            self.play(GrowArrow(dom[0]), GrowArrow(dom[1]), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(nash), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(Create(best), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def hobbes(self):
        head = label(r"Hobbes's state of nature, \ as a game", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the game", r"invade or keep the peace: \ in the state of nature, \ attacking first is safest, \ "
                              r"whatever the other does", DEFECT),
                (r"the outcome", r"the war of all against all: \ the mutual-defection equilibrium", BAD),
                (r"the remedy", r"a sovereign who punishes invasion changes the payoffs, \ so that peace becomes each "
                                r"one's best response", INST),
                (r"the reading", r"Gauthier \ (1969), \ Kavka \ (1986), \ Hampton \ (1986): \ whether the state of "
                                 r"nature is a dilemma, \ or an assurance game, \ is debated", HIST)]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6)
        with self.voiceover(
            "Philosophers read Hobbes's argument as a prisoner's dilemma. <bookmark mark='a'/>In the state of nature, "
            "each person can invade or keep the peace, and attacking first is safest whatever the others intend. "
            "<bookmark mark='b'/>So all invade: the war of all against all is the mutual-defection equilibrium. "
            "<bookmark mark='c'/>The sovereign's role is to change the payoffs. A power that punishes invasion makes "
            "keeping the peace each person's best response, so that the good outcome becomes an equilibrium. The "
            "Leviathan is a mechanism. <bookmark mark='d'/>David Gauthier, Gregory Kavka and Jean Hampton developed "
            "this reading; they disagree whether the state of nature is really a dilemma, or the gentler assurance "
            "game of the next chapter, where peace is already stable if each trusts the others."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def commons(self):
        d = load("commons")
        head = label(r"The tragedy of the commons \ (Hardin, \ 1968), \ built", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        assert (d["a"], d["c"], d["best_total"], d["best_welfare"]) == (110.0, 10.0, 50.0, 2500.0)
        rows = d["rows"]
        assert [r["share_of_best"] for r in rows if r["n"] in (2, 10, 100)] == [0.8889, 0.3306, 0.0392]
        f = MathTex(r"u_i = x_i\,(a - X) - c\,x_i \;\Rightarrow\; x_i^* = \frac{a - c}{n + 1}, \qquad X^* = "
                    r"\frac{n}{n+1}(a - c)", font_size=28, color=MONEY).next_to(head, DOWN, buff=0.3)
        ax = Axes(x_range=[0, 2, 1], y_range=[0, 1, 0.25], x_length=6.4, y_length=3.6, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16}, y_axis_config={"include_numbers": True,
                                                                                 "decimal_number_config": {
                                                                                     "num_decimal_places": 2}}
                  ).move_to([-2.2, -1.2, 0])
        xs = VGroup(*[label(str(10 ** k), font_size=15, color=GREY_A).next_to(ax.c2p(k, 0), DOWN, buff=0.15)
                      for k in range(3)])
        xl = label(r"herders, \ $n$ \ (log scale)", font_size=16, color=GREY_A).next_to(xs, DOWN, buff=0.15)
        yl = label(r"welfare, \ as a share of the best", font_size=16, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1)
        pts = [ax.c2p(math.log10(r["n"]), r["share_of_best"]) for r in rows]
        curve = VMobject(color=DEFECT, stroke_width=3).set_points_smoothly(pts)
        dots = VGroup(*[Dot(p, radius=0.06, color=DEFECT) for p in pts])
        side = stack([(r"each cow costs its owner $c$, \ but lowers every cow's value", GREY_A),
                      (r"best for all: \ 50 cows, \ welfare 2500", OK),
                      (r"10 herders: \ 91 cows, \ a third of the best", DEFECT),
                      (r"100 herders: \ 99 cows, \ 4\%", BAD)], font_size=18, aligned_edge=LEFT, width=4.6,
                     buff=0.28).move_to([4.4, -1.0, 0])
        with self.voiceover(
            "Garrett Hardin's tragedy of the commons, of 1968, is the many-player version. The Reasoner builds it. "
            "<bookmark mark='a'/>Herders share a pasture. Each cow is worth a hundred and ten minus the total number "
            "grazing, and costs ten to keep. Each herder chooses how many to graze, and the equilibrium has each "
            "graze a hundred over n plus one. <bookmark mark='b'/>The trouble is that a cow's cost falls on its "
            "owner, while the damage it does to the pasture falls on everyone. <bookmark mark='c'/>The best total for "
            "all is fifty cows, worth two thousand five hundred. <bookmark mark='d'/>With ten herders the "
            "equilibrium is ninety one cows, and a third of that value. <bookmark mark='e'/>With a hundred it is "
            "ninety nine cows, and four percent: as the commons grows, rational grazing destroys almost all its "
            "value."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xs), FadeIn(xl), FadeIn(yl), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(Create(curve), FadeIn(dots), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def ostrom(self):
        d = load("public")
        head = label(r"Ostrom: \ the commons governed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["n"], d["r"], d["return_per_unit"], d["fine"]) == (4, 1.6, 0.4, 1.5)
        free, sanc = d["free"], d["sanctioned"]
        assert free[-1] < 0.1 and sanc[-1] > 0.85
        hc = history_card(1990, r"Elinor Ostrom", r"\textit{Governing the Commons}", width=5.2,
                          color=HIST).to_corner(UL, buff=0.3).shift(DOWN * 0.6)
        prin = stack([(r"clear boundaries; \ rules fitted to local conditions", INST),
                      (r"those affected help make the rules", INST),
                      (r"monitoring by users themselves", INST),
                      (r"graduated sanctions; \ cheap ways to settle disputes", INST),
                      (r"recognition by outside authorities; \ nested enterprises", INST)], font_size=17,
                     aligned_edge=LEFT, width=5.2, buff=0.18).next_to(hc, DOWN, buff=0.3).align_to(hc, LEFT)
        ax = Axes(x_range=[0, 30, 10], y_range=[0, 1, 0.5], x_length=5.4, y_length=3.4, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15, "include_numbers": True}).move_to([3.4, -0.2, 0])
        xl = label(r"rounds", font_size=15, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"share contributing", font_size=15, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1)
        c1 = VMobject(color=DEFECT, stroke_width=3).set_points_as_corners([ax.c2p(t, v) for t, v in enumerate(free)])
        c2 = VMobject(color=COOP, stroke_width=3).set_points_as_corners([ax.c2p(t, v) for t, v in enumerate(sanc)])
        l1 = label(r"no sanctions", font_size=15, color=DEFECT).next_to(ax.c2p(30, free[-1]), UP, buff=0.1).shift(
            LEFT * 0.6)
        l2 = label(r"monitored fines", font_size=15, color=COOP).next_to(ax.c2p(30, sanc[-1]), UP, buff=0.1).shift(
            LEFT * 0.8)
        note = label(r"groups of 4; \ each unit given returns 0.4 to the giver", font_size=15,
                     color=GREY_A).next_to(ax, DOWN, buff=0.7)
        with self.voiceover(
            "Hardin's answer was privatization or the state. Elinor Ostrom spent decades studying communities that "
            "had found a third way, and won the Nobel prize in economics for it in 2009. <bookmark mark='a'/>Swiss "
            "alpine meadows, Japanese forests and Spanish irrigation systems had been governed by their users for "
            "centuries. In Governing the Commons, of 1990, she drew out what they shared: clear boundaries, rules "
            "suited to local conditions and made by those affected, monitoring by the users themselves, graduated "
            "sanctions, and cheap ways of settling disputes. <bookmark mark='b'/>The Reasoner runs a public goods "
            "game in groups of four. Each unit a player contributes is multiplied by one point six and shared, so it "
            "returns only point four to the giver, and keeping is dominant. Players copy better-earning neighbours. "
            "<bookmark mark='c'/>Without sanctions, contributions collapse within a few rounds. "
            "<bookmark mark='d'/>With monitored, graduated fines, paid for by a small cost to every member, they "
            "rise above ninety percent and stay there. The sanction changes the game, as Hobbes's sovereign did, but "
            "it is imposed by the players on themselves."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc), LaggedStart(*[FadeIn(p) for p in prin], lag_ratio=0.3), run_time=2)
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(note))
            vo.wait_until("c")
            self.play(Create(c1), FadeIn(l1), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(c2), FadeIn(l2), run_time=1.5)
        self.clear_scene()
