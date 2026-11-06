from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


class Games(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Games on the simplex", r"When does a strategy resist invasion?", lit=(1973, 1978),
                            part=PART)
        with self.voiceover("Chapter four. Games on the simplex."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.hawkdove()
        self.ess()
        self.rps()
        self.signals()

    def hawkdove(self):
        d = load("hawkdove")
        hc = history_card(1973, r"John Maynard Smith and George Price", r"`The Logic of Animal Conflict'",
                          width=6.6, color=HIST).to_corner(UL, buff=0.3)
        A = d["A"]
        hd = [r"", r"\text{vs hawk}", r"\text{vs dove}"]
        rows = [[MathTex(r"\text{hawk}", font_size=24, color=BAD),
                 MathTex(r"\tfrac{V - C}{2} = " + f"{A[0][0]:.1f}", font_size=24),
                 MathTex(r"V = " + f"{A[0][1]:.0f}", font_size=24)],
                [MathTex(r"\text{dove}", font_size=24, color=GENE), MathTex(r"0", font_size=24),
                 MathTex(r"\tfrac{V}{2} = " + f"{A[1][1]:.0f}", font_size=24)]]
        grid = ValueGrid(hd, rows, col_w=[1.8, 2.6, 2.0], cell_h=0.6, font_size=20).next_to(hc, DOWN, buff=0.4).set_x(
            -3.2)
        eq = MathTex(r"\dot x_i = x_i\big(f_i(x) - \bar f(x)\big)", font_size=32, color=GOAL).next_to(grid, DOWN,
                                                                                                buff=0.5)
        el = label(r"replicator dynamics \ (Taylor and Jonker, \ 1978)", font_size=18, color=GREY_A).next_to(
            eq, DOWN, buff=0.15)
        T = len(d["trajectories"][0])
        ax = Axes(x_range=[0, T - 1, 20], y_range=[0, 1, 0.25], x_length=5.0, y_length=3.2,
                  axis_config={"color": GREY_B, "font_size": 18}, y_axis_config={"include_numbers": True},
                  x_axis_config={"include_ticks": False}).move_to([3.6, -0.2, 0])
        c1 = series_plot(ax, d["trajectories"][0], BAD, width=4)
        c2 = series_plot(ax, d["trajectories"][1], BAD, width=4)
        ps = DashedLine(ax.c2p(0, d["p_star"]), ax.c2p(T - 1, d["p_star"]), color=GOAL)
        pl = label(r"$p^* = V/C = " + f"{d['p_star']:.2f}" + r"$", font_size=19, color=GOAL).next_to(ps, UP, buff=0.1)
        al = label(r"share of hawks over time", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1)
        with self.voiceover(
            "John Maynard Smith and George Price brought game theory into biology. <bookmark mark='a'/>Two animals "
            "contest a resource worth V. A hawk fights until injured or the opponent retreats; a dove displays and "
            "retreats if attacked. Two hawks share the value minus the cost of injury, C. A hawk beats a dove; two "
            "doves share. Here V is two and C is three. <bookmark mark='b'/>Strategies spread in proportion to their "
            "payoff above the average: the replicator dynamics of Peter Taylor and Leo Jonker. "
            "<bookmark mark='c'/>Start with almost all doves, or almost all hawks: the population converges to the "
            "same mix, two thirds hawks, which is V over C. <bookmark mark='d'/>Neither pure strategy survives, "
            "because each does best when it is rare."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule), FadeIn(VGroup(*grid.cell[0])), FadeIn(VGroup(*grid.cell[1])))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(el))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(al))
            self.play(Create(c1), Create(c2), run_time=2)
            self.play(Create(ps), FadeIn(pl))
        self.clear_scene()

    def ess(self):
        d = load("hawkdove")
        head = label(r"Evolutionarily stable strategies", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        defs = VGroup(
            label(r"$x$ is an ESS if, \ for every mutant strategy $y \ne x$,", font_size=22, color=WHITE),
            MathTex(r"u(x, x) > u(y, x)", font_size=32, color=GENE),
            label(r"or", font_size=20, color=GREY_A),
            MathTex(r"u(x, x) = u(y, x) \;\;\text{and}\;\; u(x, y) > u(y, y)", font_size=32, color=GENE),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.4)
        inv = d["invasion"]
        rows = stack([(r"at $p^*$: \ hawks and doves earn the same against the population", WHITE),
                       (r"against a rare hawk mutant, \ $p^*$ does better by " + f"{inv['hawk']['stability_margin']:.3f}",
                        OK),
                       (r"against a rare dove mutant, \ $p^*$ does better by " + f"{inv['dove']['stability_margin']:.3f}",
                        OK),
                       (r"stability without foresight: \ no animal calculates; \ selection does the arithmetic", GOAL)],
                      font_size=21).next_to(defs, DOWN, buff=0.5)
        with self.voiceover(
            "Maynard Smith and Price defined the equilibrium concept that biology needed. <bookmark mark='a'/>A "
            "strategy x is evolutionarily stable if, for every mutant strategy, <bookmark mark='b'/>x does better "
            "against itself than the mutant does against x; <bookmark mark='c'/>or, if they tie there, x does better "
            "against the mutant than the mutant does against itself. A population playing x cannot be invaded by a "
            "small number of mutants. <bookmark mark='d'/>The Reasoner checks the hawk-dove mix. At two thirds "
            "hawks, both strategies earn the same against the population, so the second condition decides, and it "
            "holds against both possible mutants. <bookmark mark='e'/>Nobody calculates anything. The stability "
            "is achieved by differential reproduction, with no foresight at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defs[0]))
            vo.wait_until("b")
            self.play(Write(defs[1]))
            vo.wait_until("c")
            self.play(FadeIn(defs[2]), Write(defs[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def rps(self):
        d = load("rps")
        head = label(r"Rock, \ paper, \ scissors, \ and lizards", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sims = [Simplex([r"rock", r"paper", r"scissors"], center=[-4.4 + 4.4 * i, 0.3, 0], side=3.4,
                        colors=(ORG, GENE, ALT), font_size=17) for i in range(3)]
        keys = [("neutral", r"zero-sum: \ closed cycles", GREY_A), ("in", r"ties rewarded: \ spiral in", OK),
                ("out", r"ties punished: \ spiral out", BAD)]
        paths = VGroup(*[s.path(d[k]["traj"], c, width=2) for s, (k, _, c) in zip(sims, keys)])
        caps = VGroup(*[label(t, font_size=18, color=c).next_to(s, DOWN, buff=0.25) for s, (_, t, c) in zip(sims, keys)])
        centre = VGroup(*[Dot(s.p2c([1 / 3, 1 / 3, 1 / 3]), radius=0.05, color=GOAL) for s in sims])
        foot = stack([(r"no ESS in the zero-sum game: \ the frequencies cycle forever", WHITE),
                      (r"side-blotched lizards \ (Sinervo and Lively, \ 1996): \ three male morphs that beat one another "
                       r"in a circle, \ cycling every few years", GOAL)], font_size=19, width=12.6).to_edge(DOWN,
                                                                                                 buff=0.35)
        with self.voiceover(
            "With three strategies the state is a point in a triangle, the simplex, whose corners are the pure "
            "populations. <bookmark mark='a'/>In rock-paper-scissors each strategy beats one and loses to another. "
            "If ties pay nothing, the replicator dynamics cycle forever around the centre. "
            "<bookmark mark='b'/>Reward ties a little, and the cycles spiral in to an equal mix. "
            "<bookmark mark='c'/>Punish ties, and they spiral out toward the edges, where each strategy in turn "
            "nearly disappears. <bookmark mark='d'/>In the zero-sum game there is no evolutionarily stable strategy "
            "at all. <bookmark mark='e'/>Nature plays this game. Male side-blotched lizards come in three throat "
            "colours, each beating one rival strategy and losing to the other, and Barry Sinervo and Curtis Lively "
            "found their frequencies cycling every few years."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(s) for s in sims], FadeIn(centre))
            for mk, i in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(Create(paths[i]), FadeIn(caps[i]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def signals(self):
        d = load("signals")
        two, three = d["two"], d["three"]
        hc = history_card(1969, r"David Lewis; \ Brian Skyrms \ (2010)", r"\textit{Convention}; \ \textit{Signals}",
                          width=6.4, color=HIST).to_corner(UL, buff=0.3)
        st = VGroup(*[Circle(radius=0.28, color=c, fill_opacity=0.5).move_to([-5.8, 1.0 - 1.0 * i, 0])
                      for i, c in enumerate((GENE, ORG))])
        sg = VGroup(*[Square(side_length=0.5, color=GREY_B).move_to([-3.9, 1.0 - 1.0 * i, 0]) for i in range(2)])
        sgl = VGroup(*[MathTex(x, font_size=24).move_to(sq) for x, sq in zip((r"\alpha", r"\beta"), sg)])
        ac = VGroup(*[Triangle(color=c, fill_opacity=0.5).scale(0.28).move_to([-2.0, 1.0 - 1.0 * i, 0])
                      for i, c in enumerate((GENE, ORG))])
        tl = VGroup(label(r"state", font_size=15, color=GREY_A).next_to(st, UP, buff=0.15),
                    label(r"signal", font_size=15, color=GREY_A).next_to(sg, UP, buff=0.15),
                    label(r"act", font_size=15, color=GREY_A).next_to(ac, UP, buff=0.15))
        links = VGroup(*[Line(st[i].get_right(), sg[j].get_left(), color=GREY_D, stroke_width=1.5)
                         for i in range(2) for j in range(2)],
                       *[Line(sg[i].get_right(), ac[j].get_left(), color=GREY_D, stroke_width=1.5)
                         for i in range(2) for j in range(2)])
        good = VGroup(Line(st[0].get_right(), sg[0].get_left(), color=OK, stroke_width=4),
                      Line(sg[0].get_right(), ac[0].get_left(), color=OK, stroke_width=4),
                      Line(st[1].get_right(), sg[1].get_left(), color=OK, stroke_width=4),
                      Line(sg[1].get_right(), ac[1].get_left(), color=OK, stroke_width=4))
        VGroup(st, sg, sgl, ac, tl, links, good).scale(1.3).move_to([-3.9, -0.3, 0])
        ax = Axes(x_range=[0, two["rounds"], 500], y_range=[0.3, 1.0, 0.1], x_length=5.6, y_length=3.0,
                  axis_config={"color": GREY_B, "font_size": 14}, x_axis_config={"include_numbers": True},
                  y_axis_config={"include_numbers": True}).move_to([3.4, 0.6, 0])
        xs = [two["every"] * (i + 0.5) for i in range(len(two["curve"]))]
        c2 = series_plot(ax, two["curve"], GENE, xs=xs, width=3)
        c3 = series_plot(ax, three["curve"], ORG, xs=xs, width=3)
        al = label(r"success rate, \ mean of " + f"{two['runs']}" + r" runs of reinforcement learning", font_size=15,
                   color=GREY_A).next_to(ax, UP, buff=0.08)
        l2 = label(r"2 states", font_size=15, color=GENE).move_to(ax.c2p(1700, 0.99))
        l3 = label(r"3 states", font_size=15, color=ORG).move_to(ax.c2p(1700, 0.85))
        conv = two["conventions"]
        rows = stack([(r"2 states: \ " + f"{100 * two['perfect']:.0f}" + r"\% of runs reach a perfect signalling "
                       r"system; \ the two conventions: \ " + f"{conv.get('01', 0)}" + r" and " +
                       f"{conv.get('10', 0)}", GENE),
                      (r"3 states: \ " + f"{100 * three['perfect']:.0f}" + r"\%; \ the rest stall in partial pooling",
                       ORG),
                      (r"meaning without a meaner: \ the signal means what it has been reinforced to track \ "
                       r"(Part 28)", GOAL)], font_size=18, aligned_edge=LEFT, width=12.4).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Evolutionary game theory also explains a philosopher's question: how can signals come to mean "
            "anything? <bookmark mark='a'/>David Lewis's signalling game has a sender who sees the state of the "
            "world, and a receiver who sees only the sender's signal and must act. Both are rewarded when the act "
            "fits the state. <bookmark mark='b'/>A signalling system is a pairing of signals with states that lets "
            "them always succeed. Lewis thought such conventions needed common knowledge; Brian Skyrms showed "
            "they can evolve without any. <bookmark mark='c'/>The Reasoner runs the simplest learning rule: each "
            "player keeps an urn for each situation and adds a ball whenever a choice succeeds. Success climbs from "
            "a coin flip towards certainty. <bookmark mark='d'/>Ninety-four percent of runs reach a perfect "
            "signalling system within two thousand rounds, and they split almost evenly between the two possible "
            "conventions: which signal means which state is arbitrary. <bookmark mark='e'/>With three states, "
            "about a quarter of runs stall in partial pooling, using one signal for two states. "
            "<bookmark mark='f'/>Meaning, here, is made by the dynamics: a signal means what it has been "
            "reinforced to track. We return to this in Part 28."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(st), FadeIn(sg), FadeIn(sgl), FadeIn(ac), FadeIn(tl), Create(links))
            vo.wait_until("b")
            self.play(Create(good))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(al), Create(c2), FadeIn(l2), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(Create(c3), FadeIn(l3), FadeIn(rows[1]))
            vo.wait_until("f")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
