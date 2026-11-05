from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, gnode, load,
                                   mono, words)


class Hook(VoiceoverScene):
    def construct(self):
        self.bridges()
        self.everywhere()
        self.preview()
        self.plan()

    def bridges(self):
        head = label(r"K\"onigsberg, \ 1736", font_size=36).to_edge(UP, buff=0.35)
        # the river and four land masses, drawn simply
        river = VGroup(
            Rectangle(width=12.5, height=0.9, stroke_width=0, fill_color="#1d3b5a", fill_opacity=0.9).move_to(UP * 0.9),
            Rectangle(width=12.5, height=0.9, stroke_width=0, fill_color="#1d3b5a", fill_opacity=0.9).move_to(DOWN * 1.1),
            Rectangle(width=3.2, height=2.9, stroke_width=0, fill_color="#1d3b5a", fill_opacity=0.9).move_to(
                RIGHT * 3.0 + DOWN * 0.1),
        )
        island = Ellipse(width=3.0, height=1.2, stroke_width=0, fill_color="#2b2f3a", fill_opacity=1).move_to(
            LEFT * 1.2 + DOWN * 0.1)
        east = RoundedRectangle(width=2.2, height=1.3, corner_radius=0.3, stroke_width=0, fill_color="#2b2f3a",
                                fill_opacity=1).move_to(RIGHT * 3.0 + DOWN * 0.1)
        labels = VGroup(label(r"north bank", font_size=19, color=GREY_B).move_to(UP * 2.0),
                        label(r"south bank", font_size=19, color=GREY_B).move_to(DOWN * 2.1),
                        label(r"Kneiphof", font_size=19, color=GREY_B).move_to(island),
                        label(r"east", font_size=19, color=GREY_B).move_to(east))
        bpos = [(-2.0, 0.9), (-0.5, 0.9), (-2.0, -1.1), (-0.5, -1.1), (0.6, -0.1), (3.0, 0.9), (3.0, -1.1)]
        bridges = VGroup(*[Rectangle(width=0.22, height=1.0, stroke_width=0, fill_color=HEAD, fill_opacity=0.9).move_to(
            [x, y, 0]).rotate(PI / 2 if i == 4 else 0) for i, (x, y) in enumerate(bpos)])
        q = label(r"can you walk across every bridge exactly once?", font_size=24, color=YES).to_edge(DOWN, buff=0.45)
        kp = {"N": (0.5, 2.0), "K": (-1.2, -0.1), "E": (3.0, -0.1), "S": (0.5, -2.1)}
        nodes = {k: gnode(k, [x, y, 0], HEAD, 0.3, 18) for k, (x, y) in kp.items()}
        es = {}
        for i, (a_, b_, bend) in enumerate((("N", "K", 0.45), ("N", "K", -0.45), ("S", "K", 0.45), ("S", "K", -0.45),
                                            ("K", "E", 0), ("N", "E", 0), ("S", "E", 0))):
            pa, pb = np.array([*kp[a_], 0.0]), np.array([*kp[b_], 0.0])
            e = (ArcBetweenPoints(pa, pb, angle=bend, color=GREY_B, stroke_width=2.5) if bend else
                 Line(pa, pb, color=GREY_B, stroke_width=2.5))
            es[i] = e.set_z_index(-1)          # under the nodes, which hide the ends
        with self.voiceover(
            "In 1736 the city of Königsberg had seven bridges joining two river banks and two islands. <bookmark "
            "mark='a'/> Its citizens asked whether one could walk through the city crossing every bridge exactly "
            "once. <bookmark mark='b'/> Leonhard Euler answered by throwing almost everything away. The shape of "
            "the land, the lengths of the bridges, the streets: none of it matters. Only which land masses each "
            "bridge connects. <bookmark mark='c'/> Four dots, seven lines. Euler had invented the graph, and in "
            "one paper proved the walk impossible."
        ) as vo:
            self.play(FadeIn(head), FadeIn(river), FadeIn(island), FadeIn(east), FadeIn(labels))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(b) for b in bridges], lag_ratio=0.15), FadeIn(q))
            vo.wait_until("b")
            self.play(FadeOut(labels), river.animate.set_opacity(0.25), island.animate.set_opacity(0.3),
                      east.animate.set_opacity(0.3))
            vo.wait_until("c")
            self.play(FadeOut(bridges), *[FadeIn(n) for n in nodes.values()], run_time=1)
            self.play(LaggedStart(*[Create(e) for e in es.values()], lag_ratio=0.15))
        self.wait(0.3)
        self.clear_scene()

    def everywhere(self):
        head = label(r"Graphs are everywhere", font_size=36).to_edge(UP, buff=0.35)
        rows = [
            [r"road maps", r"intersections", r"roads, \ with lengths", r"shortest routes \ (chapters 6, \ 9)"],
            [r"the internet", r"routers", r"links", r"routing \ (Part 36)"],
            [r"a compiler", r"instructions, \ variables", r"control flow, \ interference", r"register allocation "
                                                                                          r"\ (Part 13)"],
            [r"a build", r"files", r"depends on", r"build order \ (chapter 4)"],
            [r"the web", r"pages", r"links", r"ranking \ (chapter 14)"],
            [r"a market", r"currencies", r"exchange rates", r"arbitrage \ (chapter 7)"],
        ]
        from videos.cs.cs18.common import grid_table
        tab = grid_table([r"graph", r"vertices", r"edges", r"question"], rows, widths=[2.6, 3.0, 3.4, 4.0],
                         row_h=0.6, font_size=21, mono_cols=(),
                         colors=[[DATA, GREY_A, GREY_A, YES]] * len(rows)).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Euler's abstraction turned out to describe almost everything. <bookmark mark='a'/> A road map is a "
            "graph of intersections and roads; the internet, of routers and links; a compiler's program, of "
            "instructions and the flow of control between them. A build is a graph of files and dependencies, "
            "the web of pages and links, a currency market of currencies and exchange rates. <bookmark mark='b'/> "
            "And the questions are the same few: how to get from here to there, in what order, how cheaply, how "
            "much can flow, which things belong together. This part answers each one, with proofs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells], lag_ratio=0.3),
                      run_time=4)
            vo.wait_until("b")
            self.play(Indicate(VGroup(*[r[3] for r in tab.cells[1:]]), color=YES))
        self.wait(0.3)
        self.clear_scene()

    def preview(self):
        head = label(r"By the end of this part", font_size=40).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"breadth and depth: \ the two ways to explore, \ and what each one proves", font_size=27,
                  color=DATA),
            label(r"Dijkstra's algorithm, \ its invariant, \ and how map apps beat it a hundredfold", font_size=27,
                  color=LAM),
            label(r"spanning trees, \ flows and cuts: \ the max-flow min-cut theorem, \ proved", font_size=27,
                  color=YES),
            label(r"stable matching, \ PageRank, \ and why Euler tours are easy and Hamilton's are not",
                  font_size=27, color=CTRL),
            label(r"the 2020s: \ Dijkstra proved universally optimal, \ and then beaten", font_size=27, color=HEAD),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is where we are going. <bookmark mark='a'/> The two basic ways to explore a graph, breadth first "
            "and depth first, and the structure each one reveals. <bookmark mark='b'/> Dijkstra's shortest-path "
            "algorithm, proved by an invariant, and the tricks that let a map app answer a hundred times faster. "
            "<bookmark mark='c'/> Spanning trees, flows and cuts, and a proof that the maximum flow equals the "
            "minimum cut. <bookmark mark='d'/> Stable matching, PageRank, and why a walk over every edge is easy "
            "while a walk through every vertex is not. <bookmark mark='e'/> And the last few years, in which "
            "Dijkstra's algorithm was proved optimal in a strong sense, and then beaten."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcde", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Graphs", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"Euler circuits; \ representations; \ breadth- and depth-first search",
            r"topological sort; \ strongly connected components; \ 2-SAT",
            r"shortest paths: \ Dijkstra, \ Bellman--Ford, \ all pairs, \ A* and contraction hierarchies",
            r"minimum spanning trees; \ max flow and min cut; \ matching",
            r"Hamiltonian cycles; \ PageRank; \ planarity and colouring",
            r"the frontier: \ universal optimality, \ beyond the sorting barrier, \ almost-linear flow",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 18 of Computer Science, Built: Graphs. <bookmark mark='a'/> In this part: Euler circuits, how "
            "to store a graph, and the two searches; topological order and strongly connected components; shortest "
            "paths of every kind; spanning trees, flows, cuts and matchings; hard problems on graphs, PageRank and "
            "planarity; and the results of the last five years."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
