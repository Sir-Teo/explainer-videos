from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Tsp(VoiceoverScene):
    def construct(self):
        self.card()
        self.tours()
        self.ratios()
        self.practice()

    def card(self):
        card = chapter_card(9, r"The travelling salesman", r"How close can we get to the shortest tour?",
                            lit=(1976, 2021), extra=((1976, r"Christofides--Serdyukov"),
                                                     (2021, r"Karlin, \ Klein and Oveis Gharan")), part=PART)
        with self.voiceover("Chapter nine. The travelling salesman."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tours(self):
        d = load("tsp")["draw"]
        P = d["P"]
        L = d["lengths"]
        sc = 0.78
        O0 = np.array([-6.4, -2.6, 0])

        def T(i):
            return O0 + np.array([P[i][0] * sc, P[i][1] * sc, 0])
        head = label(r"Thirteen cities", font_size=34).to_edge(UP, buff=0.3)
        cities = VGroup(*[Dot(T(i), radius=0.06, color=WHITE) for i in range(len(P))])

        def tour_mob(t, col, w=3):
            return Polygon(*[T(i) for i in t], color=col, stroke_width=w)
        mst = VGroup(*[Line(T(u), T(v), color=LAM, stroke_width=3) for u, v in d["mst"]])
        dbl = VGroup(*[Line(T(u), T(v), color=LAM, stroke_width=3).shift(0.04 * UR) for u, v in d["mst"]])
        dt = tour_mob(d["double_tree"], NO)
        odd = VGroup(*[Circle(radius=0.13, color=HEAD).move_to(T(i)) for i in d["odd"]])
        mm = VGroup(*[DashedLine(T(u), T(v), color=HEAD, stroke_width=3) for u, v in d["matching"]])
        ch = tour_mob(d["christofides"], HEAD)
        opt = tour_mob(d["tour"], YES, 4)
        side = VGroup(
            label('general nonmetric TSP: \\ no fixed-factor polynomial approximation unless $P=NP$', font_size=20,
                  color=NO),
            label(r"so assume the \textbf{triangle inequality}: \\ shortcuts never hurt", font_size=20, color=WHITE),
            label(rf"\textbf{{double tree}}: \ minimum spanning tree $\le$ OPT, \\ walk it twice, \ shortcut: \ "
                  rf"$\le 2\,$OPT \ ({L['double_tree'] / L['opt']:.2f})", font_size=20, color=NO),
            label(r"\textbf{Christofides--Serdyukov} \ (1976): \\ pair up the tree's odd-degree vertices by a min matching "
                  r"\\ ($\le$ OPT$/2$), \ Euler tour, \ shortcut", font_size=20, color=HEAD),
            label(rf"$\le \tfrac32\,$OPT: \ here {L['christofides'] / L['opt']:.3f}", font_size=20, color=HEAD),
            label(rf"the optimum, \ by Held--Karp's $O(2^n n^2)$ DP \ (Part 19): \ {L['opt']:.2f}", font_size=20,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            (
            "The travelling salesman seeks a shortest tour. <bookmark mark='a'/> For general nonmetric "
            'distances, a fixed-factor polynomial approximation would decide Hamiltonian cycle, so no such '
            "guarantee exists unless P equals NP. <bookmark mark='b'/> Assume instead a complete symmetric "
            "metric with triangle inequality, as for these planar Euclidean points. <bookmark mark='c'/> An MST "
            'costs at most the optimum tour. Doubling its edges gives an Euler walk of cost at most twice OPT, '
            "and metric shortcuts give a tour. <bookmark mark='d'/> Christofides and Serdyukov improve this by "
            "matching the tree's odd-degree vertices. A minimum perfect matching costs at most half OPT; adding "
            "it makes every degree even, and shortcutting the Euler walk yields a tour. <bookmark mark='e'/> The "
            'factor is three halves for the specified metric model. Independent Kruskal and blossom calculations '
            "check our MST and matching weights. <bookmark mark='f'/> Held-Karp finds the combinatorial optimum "
            'using floating Euclidean lengths, separately checked by a backward recurrence. Our teaching '
            'matching uses exponential subset DP; it is not a polynomial blossom implementation.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(cities))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(x) for x in mst], lag_ratio=0.1), FadeIn(side[2]))
            self.play(FadeIn(dbl), run_time=0.6)
            self.play(Create(dt), FadeOut(dbl), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeOut(dt), FadeIn(side[3]), FadeIn(odd), LaggedStart(*[Create(x) for x in mm], lag_ratio=0.3))
            vo.wait_until("e")
            self.play(FadeOut(mst), FadeOut(mm), FadeOut(odd), Create(ch), FadeIn(side[4]), run_time=2.0)
            vo.wait_until("f")
            self.play(FadeOut(ch), Create(opt), FadeIn(side[5]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    def ratios(self):
        t = load("tsp")
        s = t["summary"]
        head = label(rf"Forty random 12-city instances, \ against the exact optimum", font_size=30).to_edge(UP, buff=0.35)
        rows = [[r"double tree", r"$\le 2$", f"{s['double_tree']['mean']:.3f}", f"{s['double_tree']['max']:.3f}"],
                [r"Christofides--Serdyukov", r"$\le 1.5$", f"{s['christofides']['mean']:.3f}",
                 f"{s['christofides']['max']:.3f}"],
                [r"nearest neighbour", r"$O(\log n)$", f"{s['nn']['mean']:.3f}", f"{s['nn']['max']:.3f}"],
                [r"nearest neighbour + 2-opt", r"$O(\log n)$", f"{s['two_opt']['mean']:.3f}", f"{s['two_opt']['max']:.3f}"]]
        tab = grid_table([r"", r"guarantee", r"mean", r"worst"], rows, widths=[4.6, 2.2, 1.6, 1.6], row_h=0.5,
                         font_size=22, mono_cols=(), colors=[[NO] * 4, [HEAD] * 4, [GREY_A] * 4, [YES] * 4])
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label('\\textbf{2-opt}: \\ replace any improving pair of tour edges; \\ reversals include uncrossings', font_size=22,
                  color=YES),
            label('this finite sample: \\ nearest neighbour plus 2-opt has the lowest mean ratio', font_size=22,
                  color=WHITE),
            label('selected 2021 randomized metric-TSP theorem: \\ $3/2-\\varepsilon$, \\ $\\varepsilon>10^{-36}$; \\\\ not executed by these local algorithms', font_size=22, color=LAM),
            label(r"in the plane: \ Arora (1996) and Mitchell: \ a $(1 + \varepsilon)$-approximation for every "
                  r"$\varepsilon$ \ (a PTAS)", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.28).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            (
            "These forty seeded twelve-city instances compare finite tour ratios with independently checked optima. <bookmark mark='a'/> Double tree and Christofides obey their metric guarantees. Nearest neighbour followed by two-opt has the smallest sample mean here. Two-opt tries improving pairs of edges; uncrossing is one kind of improvement, not its entire definition. <bookmark mark='b'/> That empirical outcome is specific to this family and stopping rule. The combined heuristic inherits nearest neighbour's logarithmic metric guarantee because it never lengthens the starting tour. This sample does not establish a constant-factor improvement. <bookmark mark='c'/> A selected 2021 randomized metric-TSP theorem of Karlin, Klein and Oveis Gharan gives three halves minus a positive epsilon larger than ten to the minus thirty-six. It is a separate algorithm, not executed here, and is not presented as today's best bound. <bookmark mark='d'/> Euclidean TSP also admits a polynomial-time approximation scheme for each fixed positive epsilon, with dimension and epsilon dependence kept in its cost."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            for mk, n_ in zip("bcd", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def practice(self):
        t = load("tsp")
        b = t["big"]
        head = label(r"Real tours", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(rf"Held--Karp for 15 cities: \ {t['t_hk15']:.2f} s; \ minimum of 3 shared-host trials; \ exponential DP",
                  font_size=22, color=NO),
            label(rf"{b[1]['n']} random cities: \ nearest neighbour {b[1]['nn']:.2f}; \ 2-opt {b[1]['two_opt']:.2f}; \ {b[1]['seconds']:.2f} s (3 trials, minimum)", font_size=22, color=YES),
            label(rf"uniform planar points: \ asymptotic numerical prediction $0.7124\sqrt n$ ({b[1]['bhh']:.2f}); \ not a finite bound", font_size=22, color=GREY_A),
            label('Lin--Kernighan and LKH: \\ richer local moves; \\ instance- and configuration-dependent outcomes',
                  font_size=22, color=LAM),
            label(r"Concorde \ (Applegate, \ Bixby, \ Chv\'atal and Cook): \ \textbf{proved} optimal tours of 85,900 "
                  r"cities, \ by LP cutting planes", font_size=22, color=HEAD),
            label(r"in practice: \ delivery routes, \ drilling circuit boards, \ telescope schedules, \ genome mapping",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            (
            "Implementation cost matters alongside guarantees. <bookmark mark='a'/> Held-Karp's exponential "
            'state count makes fifteen cities a small timing case, not a scalable route planner. The caption '
            "reports the minimum of three shared-host runs on identical prepared points. <bookmark mark='b'/> At "
            'three hundred cities we time two-opt alone, after nearest neighbour has prepared the starting tour. '
            "Generation, length checks and references run outside the clock. <bookmark mark='c'/> The zero point "
            'seven one two four square-root-n expression is a numerical asymptotic prediction for independent '
            "uniform points in the unit square. It is neither this instance's optimum nor a finite gap "
            "certificate. <bookmark mark='d'/> Lin-Kernighan and LKH use more powerful local moves, with "
            "performance depending on the instance and configuration. <bookmark mark='e'/> Concorde has proved "
            'optimality for a particular eighty-five-thousand-nine-hundred-city circuit-board instance using '
            'exact certification machinery. That historical result is not a runtime promise for arbitrary '
            "inputs. <bookmark mark='f'/> Delivery, drilling and scheduling often add constraints beyond "
            'symmetric metric TSP, so their models require separate checks.'
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
