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
            label(r"no factor is possible in general: \\ a $c$-approximation would decide Hamiltonian cycle", font_size=20,
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
            "The travelling salesman wants the shortest tour through all the cities. <bookmark mark='a'/> In general "
            "no approximation factor at all is possible: give the missing roads of a graph enormous lengths, and any "
            "algorithm that was within a factor c would tell you whether the graph has a Hamiltonian cycle. "
            "<bookmark mark='b'/> So assume real distances, which obey the triangle inequality: going straight is "
            "never longer than a detour. <bookmark mark='c'/> Then here is a factor two. The minimum spanning tree "
            "is no longer than the best tour, because removing one edge of the tour leaves a spanning tree. Walk "
            "around the tree, using every edge twice, and skip cities you have already visited. <bookmark mark='d'/> "
            "Nicos Christofides, and independently Anatoliy Serdyukov, did better in 1976. The tree's odd-degree "
            "vertices can be paired up by a matching at most half the optimum. Add it, and every degree is even, so "
            "there is an Euler tour; shortcut it. <bookmark mark='e'/> At most three halves of the optimum. <bookmark "
            "mark='f'/> And here is the optimum itself, from Held and Karp's dynamic program."
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
                [r"nearest neighbour + 2-opt", r"none", f"{s['two_opt']['mean']:.3f}", f"{s['two_opt']['max']:.3f}"]]
        tab = grid_table([r"", r"guarantee", r"mean", r"worst"], rows, widths=[4.6, 2.2, 1.6, 1.6], row_h=0.5,
                         font_size=22, mono_cols=(), colors=[[NO] * 4, [HEAD] * 4, [GREY_A] * 4, [YES] * 4])
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label(r"\textbf{2-opt}: \ while two edges cross, \ uncross them \ (reverse the path between)", font_size=22,
                  color=YES),
            label(r"guarantees and practice disagree: \ the heuristic with no guarantee wins", font_size=22,
                  color=WHITE),
            label(r"for 45 years nothing beat $\tfrac32$; \ Karlin, \ Klein and Oveis Gharan (2021): \ $\tfrac32 - "
                  r"10^{-36}$", font_size=22, color=LAM),
            label(r"in the plane: \ Arora (1996) and Mitchell: \ a $(1 + \varepsilon)$-approximation for every "
                  r"$\varepsilon$ \ (a PTAS)", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.28).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "How do they do in general? We ran them on forty random instances of twelve cities, against the exact "
            "optimum. <bookmark mark='a'/> The double tree averaged twenty-one percent above optimal, and "
            "Christofides seven percent. But the best performer has no guarantee at all: nearest neighbour followed by "
            "two-opt, which keeps finding two edges whose swap shortens the tour, uncrossing them, until no swap "
            "helps. It averaged just over one percent above optimal. <bookmark mark='b'/> That gap between guarantee and practice runs "
            "through this whole chapter. <bookmark mark='c'/> For forty-five years nobody improved on three halves, "
            "until Anna Karlin, Nathan Klein and Shayan Oveis Gharan beat it in 2021 by ten to the minus thirty-six, "
            "a tiny number and a large conceptual step. <bookmark mark='d'/> For cities in the plane, Sanjeev Arora "
            "and Joseph Mitchell found an approximation scheme: within one plus epsilon, for any epsilon you choose."
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
            label(rf"Held--Karp for 15 cities: \ {t['t_hk15']:.1f} s in Python; \ each extra city doubles it",
                  font_size=22, color=NO),
            label(rf"{b[1]['n']} random cities: \ nearest neighbour {b[1]['nn']:.2f}, \ after 2-opt {b[1]['two_opt']:.2f}, "
                  rf"\ in {b[1]['seconds']:.2f} s", font_size=22, color=YES),
            label(rf"Beardwood, \ Halton and Hammersley (1959): \ the optimum is about $0.7124\sqrt n$ \ "
                  rf"({b[1]['bhh']:.2f} here)", font_size=22, color=GREY_A),
            label(r"Lin--Kernighan \ (1973) \ and Helsgaun's LKH: \ $k$-opt moves, \ within a fraction of a percent",
                  font_size=22, color=LAM),
            label(r"Concorde \ (Applegate, \ Bixby, \ Chv\'atal and Cook): \ \textbf{proved} optimal tours of 85,900 "
                  r"cities, \ by LP cutting planes", font_size=22, color=HEAD),
            label(r"in practice: \ delivery routes, \ drilling circuit boards, \ telescope schedules, \ genome mapping",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "And at scale? <bookmark mark='a'/> The exact dynamic program for fifteen cities already takes a few "
            "tenths of a second in Python, and every extra city doubles it. <bookmark mark='b'/> For three hundred "
            "random cities, nearest neighbour builds a tour of length sixteen point two, and two-opt shortens it "
            "to thirteen point nine in a tenth of a second. <bookmark mark='c'/> The optimum for random points is "
            "close to zero point seven one two four times the square root of n, a theorem from 1959, which predicts "
            "about twelve point three here. Two-opt is twelve percent above that estimate, which ignores the "
            "boundary of the square, so its true gap is somewhat smaller. <bookmark mark='d'/> "
            "Lin–Kernighan moves, and Keld Helsgaun's implementation of them, get within a fraction of a percent. "
            "<bookmark mark='e'/> And the Concorde program, built on linear programming cuts like Gomory's, has proved "
            "optimal tours through eighty-five thousand nine hundred cities, the points of a circuit board. <bookmark "
            "mark='f'/> Its uses run from delivery vans to telescopes and genome maps."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
