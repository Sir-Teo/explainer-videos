from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, draw_graph, grid_table,
                                   load, mono, words)


class Euler(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.hierholzer()
        self.representation()

    def card(self):
        card = chapter_card(1, r"Euler's bridges, \ and how to store a graph", r"When can you use every edge once?",
                            lit=(1736,), extra=((1736, r"Euler: \ the seven bridges"),
                                                (1873, r"Hierholzer: \ the construction")), part=PART)
        with self.voiceover("Chapter one. Euler's bridges, and how to store a graph."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def theorem(self):
        d = load("euler")
        head = label(r"Euler's theorem", font_size=34).to_edge(UP, buff=0.3)
        g, nodes, es = draw_graph({"N": (-3.6, 1.6), "K": (-5.2, 0.0), "E": (-2.0, 0.0), "S": (-3.6, -1.6)},
                                  [("N", "K"), ("N", "K"), ("S", "K"), ("S", "K"), ("K", "E"), ("N", "E"), ("S", "E")],
                                  color=HEAD, r=0.3)
        # draw the doubled edges as arcs so both are visible
        arcs = VGroup()
        for (a, b), bend in ((("N", "K"), 0.35), (("S", "K"), -0.35)):
            pa, pb = nodes[a].get_center(), nodes[b].get_center()
            arcs.add(ArcBetweenPoints(pa, pb, angle=bend, color=GREY_B, stroke_width=2))
        deg = {"N": 3, "K": 5, "E": 3, "S": 3}
        dl = VGroup(*[mono(str(deg[k]), 18, NO).next_to(nodes[k], UR, buff=0.02) for k in nodes])
        pts = VGroup(
            label(r"a walk enters and leaves each vertex it passes through: \ two edges per visit", font_size=22,
                  color=GREY_A),
            label(r"so a closed walk using every edge once needs \textbf{every degree even}", font_size=22,
                  color=YES),
            label(r"an open walk allows exactly two odd vertices, \ its two ends", font_size=22, color=GREY_A),
            label(r"K\"onigsberg's degrees are 5, \ 3, \ 3, \ 3: \ four odd vertices, \ no walk", font_size=22,
                  color=NO),
            label(r"and the converse holds too: \ connected and all even \ $\Rightarrow$ \ a circuit exists",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.5)
        if pts.width > 7.2:
            pts.scale_to_fit_width(7.2).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Euler's argument takes one sentence. <bookmark mark='a'/> Whenever a walk passes through a land mass, "
            "it arrives on one bridge and leaves on another, so each visit uses up two of its bridges. <bookmark "
            "mark='b'/> A walk that returns to its start and crosses every bridge once therefore needs an even "
            "number of bridges at every land mass. <bookmark mark='c'/> A walk that ends somewhere else can "
            "afford two odd ones, its start and its end. <bookmark mark='d'/> Königsberg had one land mass with "
            "five bridges and three with three: four odd degrees, so no such walk exists. <bookmark mark='e'/> "
            "Euler also claimed the converse, that a connected graph with every degree even always has such a "
            "circuit; Carl Hierholzer published the first proof in 1873."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(n) for n in nodes.values()], *[Create(es[k]) for k in
                                                                           (("K", "E"), ("N", "E"), ("S", "E"))],
                      Create(arcs), Create(es[("N", "K")]), Create(es[("S", "K")]))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(dl), FadeIn(pts[3]))
            vo.wait_until("e")
            self.play(FadeIn(pts[4]))
        self.wait(0.3)
        self.clear_scene()

    def hierholzer(self):
        d = load("euler")
        head = label(r"Hierholzer's construction \ (1873)", font_size=34).to_edge(UP, buff=0.3)
        pos = {0: (0, 1.4), 1: (-2.4, 0.6), 2: (-2.4, -1.4), 3: (0, -2.2), 4: (2.4, -0.4), 5: (1.2, 0.2)}
        g = d["graph"]
        edges = sorted({tuple(sorted((int(u), v))) for u in g for v in g[u]})
        gr, nodes, es = draw_graph(pos, edges, color=DATA)
        gr.shift(LEFT * 2.2)
        circ = d["circuit"]
        steps = VGroup(
            label(r"walk from any vertex, \ never reusing an edge, \\ until you are stuck: \\ with even degrees "
                  r"you are stuck only at the start", font_size=22, color=GREY_A),
            label(r"if edges remain, \ start a detour \\ from a vertex on the circuit, \ and splice it in",
                  font_size=22, color=GREY_A),
            label(r"every edge is handled once: \ $O(E)$ time", font_size=24, color=YES),
            label(rf"here: \ {r' $\to$ '.join(str(c) for c in circ)}", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5)
        if steps.width > 6.0:
            steps.scale_to_fit_width(6.0).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The proof is an algorithm. <bookmark mark='a'/> Start anywhere and keep walking along unused edges. "
            "Because every degree is even, whenever you enter a vertex there is an unused edge to leave by, except "
            "at the vertex where you began. So you get stuck only back at the start, with a closed circuit. "
            "<bookmark mark='b'/> If some edges are still unused, one of them touches the circuit; walk a detour "
            "from there, and splice it in. <bookmark mark='c'/> Each edge is walked exactly once, so the whole "
            "construction takes time proportional to the number of edges. <bookmark mark='d'/> Here is the circuit "
            "it finds on this graph."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gr))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            for a, b in zip(circ, circ[1:]):
                key = (a, b) if (a, b) in es else (b, a)
                self.play(es[key].animate.set_color(YES).set_stroke(width=5), run_time=0.35)
        self.wait(0.3)
        self.clear_scene()

    def representation(self):
        d = load("representation")
        head = label(r"Storing a graph", font_size=34).to_edge(UP, buff=0.3)
        rows = []
        for r in d["rows"]:
            rows.append([words(r["n"]), words(r["m"]), f"{r['list_bytes'] / 1e6:.2f} MB", f"{r['matrix_bytes'] / 1e6:.2f} MB",
                         f"{1000 * r['list_s']:.1f} ms", f"{1000 * r['matrix_s']:.1f} ms"])
        tab = grid_table([r"vertices", r"edges", r"lists", r"matrix \ (bits)", r"visit all, \ lists",
                          r"visit all, \ matrix"], rows, widths=[1.8, 2.0, 1.8, 2.2, 2.4, 2.4], row_h=0.5, font_size=19,
                         colors=[[WHITE, WHITE, YES, NO, YES, NO], [WHITE, WHITE, YES, NO, YES, NO],
                                 [WHITE, WHITE, NO, YES, NO, YES]]).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"\textbf{adjacency lists}: \ each vertex keeps its neighbours: \ $O(V + E)$ space, \ visiting all "
                  r"edges $O(V + E)$", font_size=21, color=YES),
            label(r"\textbf{adjacency matrix}: \ a bit for every pair: \ $V^2$ bits, \ but ``is $uv$ an edge?'' in "
                  r"one look", font_size=21, color=LAM),
            label(r"real graphs are sparse: \ a road network averages under 3 roads per intersection", font_size=21,
                  color=GREY_A),
            label(r"dense graphs, \ like the last row, \ favour the matrix: \ Part 9's memory hierarchy decides "
                  r"the constants", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Before searching graphs we have to store them, and there are two standard ways. <bookmark mark='a'/> "
            "Adjacency lists give each vertex a list of its neighbours: space proportional to vertices plus edges, "
            "and visiting every edge takes the same. <bookmark mark='b'/> An adjacency matrix keeps a bit for every "
            "pair of vertices, so it costs V squared bits regardless of the edges, but it answers whether two "
            "vertices are joined in a single look. <bookmark mark='c'/> Most real graphs are sparse: a road map has "
            "fewer than three roads per intersection, so lists win by a wide margin, as the first two rows show. "
            "<bookmark mark='d'/> The last row is a dense graph, three thousand vertices and a million and a half "
            "edges, where the packed matrix is both smaller and faster to scan."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
