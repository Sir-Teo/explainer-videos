from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Unimodular(VoiceoverScene):
    def construct(self):
        self.card()
        self.bipartite()
        self.triangle()
        self.flows()

    def card(self):
        card = chapter_card(6, r"When the vertices are integers", r"When is an integer program secretly easy?",
                            lit=(1956,), extra=((1956, r"Hoffman--Kruskal"),), part=PART)
        with self.voiceover("Chapter six. When the vertices are integers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def bipartite(self):
        d = load("tu")
        E = [tuple(e) for e in d["edges"]]
        head = label(r"Matching as a linear program", font_size=34).to_edge(UP, buff=0.3)
        L = [np.array([-5.6, 1.2 - 1.2 * i, 0]) for i in range(3)]
        R = [np.array([-3.2, 1.2 - 1.2 * i, 0]) for i in range(3)]
        nodes = VGroup(*[VGroup(Circle(radius=0.25, color=DATA).move_to(p), mono(f"a{i}", 16, DATA).move_to(p))
                         for i, p in enumerate(L)],
                       *[VGroup(Circle(radius=0.25, color=LAM).move_to(p), mono(f"b{i}", 16, LAM).move_to(p))
                         for i, p in enumerate(R)])
        lines = VGroup(*[Line(L[u], R[v], buff=0.25, color=GREY_B, stroke_width=2) for u, v in E])
        M = d["M"]
        hdr = [""] + [f"$e_{k}$" for k in range(len(E))]
        rows = [[f"a{i}" if i < 3 else f"b{i - 3}"] + [str(v) for v in M[i]] for i in range(6)]
        tab = grid_table(hdr, rows, widths=[0.9] + [0.7] * len(E), row_h=0.4, font_size=20, mono_cols=(),
                         colors=[[DATA if i < 3 else LAM] + [YES if v else GREY_D for v in M[i]] for i in range(6)])
        tab.move_to(RIGHT * 2.6 + UP * 0.6)
        lp = MathTex(r"\max \sum_e w_e x_e \quad \text{s.t.} \quad \sum_{e \ni v} x_e \le 1,\ \ 0 \le x_e \le 1",
                     font_size=30, color=WHITE).next_to(tab, DOWN, buff=0.4)
        notes = VGroup(
            label(r"one column per edge, \ a 1 at each end: \ the \textbf{incidence matrix}", font_size=21, color=WHITE),
            label(r"\textbf{totally unimodular}: \ every square submatrix has determinant $0$, $1$ or $-1$ \ "
                  r"(checked: \ all of this one's)", font_size=21, color=YES),
            label(r"then every vertex of $\{x : Mx \le b\}$ is integral for integral $b$ \ (Cramer's rule)",
                  font_size=21, color=HEAD),
            label(rf"so the LP \textbf{{is}} the integer program: \ {d['trials']} random weighted bipartite graphs, \ "
                  rf"{d['frac_bipartite']} fractional optima", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            (
            "Some integer models have integral linear relaxations. <bookmark mark='a'/> Give each edge of a "
            'bipartite graph a variable between zero and one, with incident values summing to at most one at '
            "each vertex. <bookmark mark='b'/> Its unsigned vertex-edge incidence matrix has two ones per "
            "column. <bookmark mark='c'/> Bipartiteness makes this matrix totally unimodular: every square minor "
            'is zero or plus or minus one. We independently check all nine hundred twenty-three nonempty square '
            "minors in the drawing. A partial minor search would be inconclusive. <bookmark mark='d'/> With "
            'integer right-hand sides and integer variable bounds, the augmented constraint matrix stays totally '
            "unimodular. Every nonsingular vertex basis has determinant plus or minus one, so Cramer's rule "
            "gives integer coordinates. <bookmark mark='e'/> Thus an optimal vertex solves the matching problem. "
            'All one hundred seeded weighted bipartite LPs have exact primal-dual certificates and agree with '
            'independent integer matching optima.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes), Create(lines))
            vo.wait_until("a")
            self.play(FadeIn(lp))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def triangle(self):
        d = load("tu")
        head = label(r"An odd cycle breaks it", font_size=34).to_edge(UP, buff=0.35)
        P = [np.array([-4.0, 1.4, 0]), np.array([-5.4, -1.0, 0]), np.array([-2.6, -1.0, 0])]
        nodes = VGroup(*[Circle(radius=0.25, color=DATA).move_to(p) for p in P])
        E = [(0, 1), (1, 2), (0, 2)]
        lines = VGroup(*[Line(P[u], P[v], buff=0.25, color=HEAD, stroke_width=3) for u, v in E])
        labs = VGroup(*[MathTex(r"\tfrac12", font_size=30, color=HEAD).move_to((P[u] + P[v]) / 2 +
                                                                              0.35 * (P[u] + P[v] - 2 * np.mean(P, 0)) /
                                                                              np.linalg.norm(P[u] + P[v] - 2 * np.mean(P, 0)))
                        for u, v in E])
        notes = VGroup(
            label(r"a triangle: \ the incidence matrix has determinant $2$", font_size=22, color=NO),
            label(rf"the LP puts $\tfrac12$ on every edge: \\ value {d['tri_lp_value']:.1f}, \ but any matching has 1 edge",
                  font_size=22, color=HEAD),
            label(rf"on {d['trials']} random weighted general graphs: \\ {d['frac_general']} fractional optima", font_size=22,
                  color=NO),
            label(r"Edmonds (1965): \ add the \textbf{odd-set} constraints \\ $\sum_{e \subseteq S} x_e \le \lfloor |S|/2 "
                  r"\rfloor$ \ and the polytope is integral again", font_size=22, color=YES),
            label(r"exponentially many constraints, \ but separable: \\ chapter 5's ellipsoid theorem applies",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if notes.width > 7.6:
            notes.width = 7.6
            notes.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Outside bipartite graphs it fails, and the smallest failure is a triangle. <bookmark mark='a'/> Its "
            "incidence matrix has determinant two. <bookmark mark='b'/> The linear program happily puts one half on "
            "each edge, for a total of one and a half, though any matching in a triangle has just one edge. "
            "<bookmark mark='c'/> On a hundred random weighted graphs that were not bipartite, a quarter of the "
            "optimal vertices were fractional. <bookmark mark='d'/> Jack Edmonds repaired it in 1965: add a constraint "
            "for every odd set of vertices, saying it contains at most half as many edges, rounded down, and the "
            "polytope is integral again. <bookmark mark='e'/> There are exponentially many such constraints, but a "
            "violated one can be found quickly, so by chapter five's theorem the program is still solvable in "
            "polynomial time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes), Create(lines))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(labs), FadeIn(notes[1]))
            for mk, n_ in zip("cde", notes[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def flows(self):
        head = label(r"Flows, \ cuts, \ and other free integrality", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"max-flow is an LP whose matrix \ (a directed incidence matrix) \ is totally unimodular", font_size=22,
                  color=WHITE),
            label(r"its dual is min-cut: \ Part 18's max-flow min-cut theorem \textbf{is} LP duality", font_size=22,
                  color=YES),
            label(r"integral capacities give an integral maximum flow \ (as Ford--Fulkerson found by augmenting)",
                  font_size=22, color=LAM),
            label(r"also totally unimodular: \ interval matrices \ (scheduling), \ network matrices, \ shortest paths",
                  font_size=22, color=HEAD),
            label('Seymour: \\ regular-matroid decomposition and polynomial recognition; \\\\ our exhaustive minors are a separate small-matrix check',
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.36).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            (
            "Integrality explains familiar combinatorial optimization results. <bookmark mark='a'/> A directed "
            "graph's node-arc incidence matrix is totally unimodular; adding integer capacity bounds preserves "
            "the flow integrality argument. <bookmark mark='b'/> LP duality then yields the max-flow min-cut "
            "relationship. <bookmark mark='c'/> Integral capacities admit an integral maximum flow, although "
            "fractional optimal flows may also exist as combinations of optimal vertices. <bookmark mark='d'/> "
            'Consecutive-ones interval matrices and network matrices provide other useful totally unimodular '
            "families. <bookmark mark='e'/> Seymour's decomposition of regular matroids, using graphic, "
            'cographic and the exceptional R-ten building block with specified sums, underlies polynomial '
            'recognition. Our brute-force minor enumeration is an exact small-matrix teaching check, not that '
            'recognition algorithm.'
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
