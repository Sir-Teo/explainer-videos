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
            label(r"an open trail has exactly two odd endpoints; \ all edge-bearing vertices must connect", font_size=22, color=GREY_A),
            label(r"K\"onigsberg's degrees are 5, \ 3, \ 3, \ 3: \ four odd vertices, \ no walk", font_size=22,
                  color=NO),
            label(r"and the converse holds too: \ connected and all even \ $\Rightarrow$ \ a circuit exists",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.5)
        if pts.width > 7.2:
            pts.scale_to_fit_width(7.2).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Euler's argument counts entrances and exits. <bookmark mark='a'/> Passing through a vertex "
            "uses two incident edges, one arriving and one leaving. <bookmark mark='b'/> A closed trail "
            "using every edge once therefore requires even degree everywhere; a loop contributes two to "
            "degree. <bookmark mark='c'/> An open trail with different endpoints instead has exactly two "
            "odd vertices. In either case all vertices incident to edges must lie in one connected "
            "component. <bookmark mark='d'/> Königsberg has degrees five, three, three and three: four "
            "odd vertices, so neither kind of trail can cross every bridge once. <bookmark mark='e'/> For"
            " a connected graph, the even-degree condition is also sufficient. Hierholzer's construction,"
            " published in 1873, gives the circuit explicitly."
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
            label(r"walk from a vertex with an edge, \ never reusing an edge, \\ until you are stuck: \\ with even degrees "
                  r"you are stuck only at the start", font_size=22, color=GREY_A),
            label(r"if edges remain, \ start a detour \\ from a vertex on the circuit, \ and splice it in",
                  font_size=22, color=GREY_A),
            label(r"paired edge identifiers; \ expected $O(V+E)$ including validation", font_size=24, color=YES),
            label(rf"here: \ {r' $\to$ '.join(str(c) for c in circ)}", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5)
        if steps.width > 6.0:
            steps.scale_to_fit_width(6.0).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The proof becomes a stack algorithm. <bookmark mark='a'/> Start at a vertex with an edge and"
            " follow unused edges. At a vertex other than the start, entering consumes one of an even "
            "number, so an unused exit remains whenever the walk would otherwise stop. The walk closes at"
            " its start. <bookmark mark='b'/> If edges remain, connectivity gives a detour from a vertex "
            "already on the circuit; splice that closed detour into it. <bookmark mark='c'/> Our "
            "implementation pairs edge incidences with identifiers and skips used identifiers. It handles"
            " each incidence a constant number of times, including validation: expected order V plus E "
            "with hash tables, rather than repeatedly removing from the middle of a list. <bookmark "
            "mark='d'/> The highlighted edges show the checked circuit on this graph."
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
        head = label(r"Graph storage: models and actual allocations", font_size=34).to_edge(UP, buff=0.3)
        rows = [[words(r['n']), words(r['m']), f"{r['list_bytes']/1e6:.2f}", f"{r['matrix_bytes']/1e6:.2f}",
                 f"{r['actual_list_bytes']/1e6:.2f}", f"{r['matrix_array_bytes']/1e6:.2f}"] for r in d['rows']]
        tab = grid_table([r"vertices", r"edges", r"ideal lists", r"packed bits", r"Python lists", r"NumPy bool"],
                         rows, widths=[1.4,1.8,2.0,2.0,2.2,2.2], row_h=.47, font_size=20,
                         colors=[[WHITE,WHITE,YES,LAM,DATA,HEAD]]*3).next_to(head, DOWN, buff=.4)
        memory = label(r"MB; ideal models exclude object overhead; NumPy bool uses one byte per cell",
                       font_size=20, color=GREY_A).next_to(tab, DOWN, buff=.2)
        times = grid_table([r"vertices",r"Python entry visits",r"NumPy full-row counts",r"checked entries"],
                           [[words(r['n']),f"{r['list_s']*1000:.2f} ms",f"{r['matrix_s']*1000:.2f} ms",words(r['visited'])]
                            for r in d['rows']], widths=[1.8,3.0,3.4,2.5], row_h=.45, font_size=20,
                           colors=[[WHITE,DATA,HEAD,YES]]*3).move_to(DOWN * .9)
        protocol = label(r"minimum of three complete scans; same graph; both counts equal $2E$",
                         font_size=20,color=YES).next_to(times,DOWN,buff=.2)
        scope = label(r"different execution paths; packed-bit scan and cache-level causes are unmeasured",
                      font_size=20,color=GREY_A).to_edge(DOWN,buff=.35)
        with self.voiceover("Storage models and measured programs are different things. <bookmark mark='a'/> Adjacency lists need order V plus E entries. The first table estimates eight-byte neighbour entries and row references; it excludes Python object overhead. <bookmark mark='b'/> An ideal packed matrix uses one bit per ordered vertex pair. Our measured NumPy boolean matrix instead uses one byte per cell; its actual data allocation is shown separately. <bookmark mark='c'/> The timing table scans the complete graph three times and reports the minimum: Python visits every list entry, while NumPy counts each complete boolean row. Both must count exactly twice the undirected edges. <bookmark mark='d'/> The dense case favours this vectorized matrix scan on this host. It is not a measured packed-bit implementation, and these timings alone do not identify a cache-level cause.") as vo:
            self.play(FadeIn(head),FadeIn(tab),FadeIn(memory))
            vo.wait_until('a')
            self.play(Indicate(VGroup(*[row[2] for row in tab.cells]),color=YES),run_time=.7)
            vo.wait_until('b')
            self.play(Indicate(VGroup(*[row[3] for row in tab.cells],*[row[5] for row in tab.cells]),color=HEAD),run_time=.7)
            vo.wait_until('c')
            self.play(FadeIn(times),FadeIn(protocol))
            vo.wait_until('d')
            self.play(FadeIn(scope))
        self.wait(.3)
        self.clear_scene()
