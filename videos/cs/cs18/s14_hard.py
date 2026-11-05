from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Hard(VoiceoverScene):
    def construct(self):
        self.card()
        self.icosian()
        self.contrast()
        self.measured()

    def card(self):
        card = chapter_card(13, r"Easy and hard", r"Why is visiting every vertex so much harder than every edge?",
                            lit=(1857,), extra=((1857, r"Hamilton's icosian game"), (1962, r"Held and Karp")),
                            part=PART)
        with self.voiceover("Chapter thirteen. Easy and hard."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def icosian(self):
        d = load("hard")
        head = label(r"Hamilton's icosian game \ (1857)", font_size=34).to_edge(UP, buff=0.3)
        c0 = np.array([-3.3, -0.4, 0])
        pos = {}
        for i in range(5):
            a = np.deg2rad(90 + 72 * i)
            pos[i] = c0 + 2.7 * np.array([np.cos(a), np.sin(a), 0])
            pos[15 + i] = c0 + 0.95 * np.array([np.cos(a + np.deg2rad(36)), np.sin(a + np.deg2rad(36)), 0])
        for j in range(10):
            a = np.deg2rad(90 + 36 * j)
            pos[5 + j] = c0 + 1.85 * np.array([np.cos(a), np.sin(a), 0])
        edges = VGroup(*[Line(pos[a], pos[b], color=GREY_C, stroke_width=2) for a, b in d["dodeca_edges"]])
        dots = VGroup(*[Dot(pos[v], radius=0.1, color=DATA) for v in range(20)])
        cyc = d["dodeca_cycle"]
        tour = VGroup(*[Line(pos[cyc[i]], pos[cyc[(i + 1) % 20]], color=HEAD, stroke_width=6) for i in range(20)])
        start = Circle(radius=0.2, color=YES, stroke_width=3).move_to(pos[cyc[0]])
        side = VGroup(
            label(r"the twenty corners of a dodecahedron, \\ drawn flat", font_size=21, color=GREY_A),
            label(r"the puzzle: \ travel along the edges \\ through every corner exactly once, \\ and return",
                  font_size=21, color=GREY_A),
            label(rf"backtracking finds all {d['dodeca_cycles']} such cycles \\ in a few milliseconds", font_size=21,
                  color=HEAD),
            label(r"twenty vertices are easy; \\ the trouble is how the search grows with $n$", font_size=21,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        if side.width > 5.6:
            side.scale_to_fit_width(5.6).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "In 1857 the Irish mathematician William Rowan Hamilton invented a puzzle and sold it to a London "
            "games maker for twenty-five pounds. <bookmark mark='a'/> Its board was a dodecahedron, flattened into "
            "the plane: twenty corners, each joined to three others. <bookmark mark='b'/> The player had to travel "
            "along the edges through every corner exactly once and come back to the start. <bookmark mark='c'/> "
            "Here is one solution. A backtracking search finds all thirty of them in a few milliseconds. <bookmark "
            "mark='d'/> So small cases are easy. The question this chapter asks is how the search grows, and the "
            "answer is the most important open problem in computer science."
        ) as vo:
            self.play(FadeIn(head), Create(edges), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Create(start))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(t) for t in tour], lag_ratio=0.6), run_time=4.0)
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def contrast(self):
        head = label(r"Every edge once, \ or every vertex once", font_size=34).to_edge(UP, buff=0.3)
        left = VGroup(
            label(r"\textbf{Euler tour}: \ every edge exactly once", font_size=23, color=YES),
            label(r"exists $\iff$ connected and all degrees even", font_size=21, color=GREY_A),
            label(r"a local condition, \ checked vertex by vertex", font_size=21, color=GREY_A),
            label(r"found in $O(E)$ \ (chapter 1)", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        right = VGroup(
            label(r"\textbf{Hamiltonian cycle}: \ every vertex exactly once", font_size=23, color=NO),
            label(r"no local condition is known", font_size=21, color=GREY_A),
            label(r"best exact algorithms: \ exponential, \ about $2^n$", font_size=21, color=GREY_A),
            label(r"NP-complete \ (Karp, \ 1972): \ Part 26", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        VGroup(left, right).arrange(RIGHT, buff=1.0, aligned_edge=UP).next_to(head, DOWN, buff=0.8)
        tsp = VGroup(
            label(r"the \textbf{travelling salesman}: \ the shortest Hamiltonian cycle", font_size=22, color=HEAD),
            MathTex(r"\text{Held--Karp (1962): } \ C(S, j) = \min_{k \in S} \bigl(C(S \setminus \{j\}, k) + d_{kj}\bigr),"
                    r"\quad O(2^n n^2)", font_size=28, color=LAM),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Two problems that sound alike. <bookmark mark='a'/> An Euler tour uses every edge exactly once. Euler's "
            "theorem gives a local test, degrees and connectivity, and chapter one found the tour in linear time. "
            "<bookmark mark='b'/> A Hamiltonian cycle, the object of Hamilton's puzzle, visits every vertex exactly "
            "once. No local test is known, and the best exact algorithms "
            "take exponential time. Richard Karp listed it in 1972 among the first NP-complete problems, which "
            "Part 26 is about. <bookmark mark='c'/> Its weighted version is the travelling salesman problem. The "
            "best general exact method is still Michael Held and Richard Karp's dynamic programme from 1962, over "
            "subsets of cities: two to the n times n squared."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(tsp))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("hard")
        head = label(r"Timed on this machine", font_size=34).to_edge(UP, buff=0.3)
        def big(v):
            if v < 1e6:
                return f"{v:,.0f}"
            e = int(math.floor(math.log10(v)))
            return rf"${v / 10 ** e:.1f} \times 10^{{{e}}}$"
        rows = []
        for r in d["rows"]:
            rows.append([str(r["n"]), f"{r['held_karp_s'] * 1000:.1f} ms" if r["held_karp_s"] < 1 else
                         f"{r['held_karp_s']:.2f} s", big(r["brute"])])
        tab = grid_table([r"cities", r"Held--Karp, \ Python", r"tours to try by brute force"], rows,
                         widths=[1.6, 3.0, 3.8], row_h=0.44, font_size=20, colors=[[WHITE, LAM, NO]] * len(rows),
                         mono_cols=(0,)).next_to(head, DOWN, buff=0.45)
        last = d["rows"][-1]
        ratios = [b["held_karp_s"] / a["held_karp_s"] for a, b in zip(d["rows"], d["rows"][1:]) if a["n"] >= 10]
        lo, hi = min(ratios), max(ratios)
        side = VGroup(
            label(rf"each two more cities: \ {lo:.0f} to {hi:.0f}$\times$ slower", font_size=21, color=GREY_A),
            label(rf"at this rate, \ 50 cities would take about "
                  rf"{last['held_karp_s'] * 2 ** (50 - last['n']) * (50 / last['n']) ** 2 / 3.15e7:,.0f} years, \ "
                  r"and a table of $2^{50}$ entries", font_size=21, color=NO),
            label(rf"meanwhile an Euler circuit of {words(d['euler_edges'])} edges: \ {d['euler_s']:.2f} s", font_size=21,
                  color=YES),
            label(r"practical TSP solvers \ (Concorde) \ solve thousands of cities exactly, \ by cutting planes "
                  r"and branch-and-bound \ (Part 23)", font_size=19, color=GREY_B),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is the difference in seconds. <bookmark mark='a'/> Held–Karp in Python solves sixteen cities in "
            "about a second, and each two more cities make it about six times slower. <bookmark mark='b'/> At "
            "that rate, fifty cities would take a few thousand years, and more memory than exists. <bookmark mark='c'/> Meanwhile, an Euler circuit "
            "through a hundred and eighty thousand edges takes a fraction of a second. <bookmark mark='d'/> Hard does "
            "not mean hopeless: solvers such as Concorde find provably optimal tours of thousands of cities, using "
            "the linear programming of Part 23. But no one knows an algorithm whose worst case is polynomial, and "
            "most researchers believe there is none."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(side[0]))
            for mk, p in zip("bcd", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
