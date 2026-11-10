from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, draw_graph, load,
                                   mono, words)


class Mst(VoiceoverScene):
    def construct(self):
        self.card()
        self.properties()
        self.kruskal()
        self.algorithms()

    def card(self):
        card = chapter_card(10, r"Minimum spanning trees", r"What is the cheapest way to connect everything?",
                            lit=(1926,), extra=((1926, r"Bor\r{u}vka: \ the Moravian grid"),
                                                (1956, r"Kruskal"), (1957, r"Prim")), part=PART)
        with self.voiceover("Chapter ten. Minimum spanning trees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def properties(self):
        head = label(r"Two properties, \ one proof each", font_size=34).to_edge(UP, buff=0.3)
        pos = {"a": (-5.8, 1.3), "b": (-5.3, -1.3), "c": (-4.1, 0.2), "d": (-2.2, 1.4), "e": (-1.8, -1.2),
               "f": (-0.7, 0.4)}
        w = {("a", "b"): 2, ("a", "c"): 3, ("b", "c"): 5, ("d", "e"): 2, ("d", "f"): 3, ("e", "f"): 6,
             ("c", "d"): 4, ("b", "e"): 9, ("a", "d"): 7}
        g, nodes, es = draw_graph(pos, list(w), weights=w, r=0.24, font=17)
        cut = DashedLine([-3.15, 2.3, 0], [-3.15, -2.3, 0], color=HEAD, stroke_width=2.5)
        sides = VGroup(label(r"$S$", font_size=24, color=HEAD).move_to([-4.6, 2.2, 0]),
                       label(r"$V - S$", font_size=24, color=HEAD).move_to([-1.6, 2.2, 0]))
        crossing = [("c", "d"), ("b", "e"), ("a", "d")]
        tree = [("a", "b"), ("a", "c"), ("d", "e"), ("d", "f"), ("b", "e")]
        cycle = [("c", "d"), ("d", "e"), ("b", "e"), ("a", "b"), ("a", "c")]
        steps = VGroup(
            label(r"a \textbf{spanning tree}: \ $V - 1$ edges joining all $V$ vertices, \ no cycle; \\ find one of "
                  r"least total weight", font_size=21, color=GREY_A),
            label(r"\textbf{cut property}: \ split the vertices in two; \\ the lightest edge across the split \\ is "
                  r"in some minimum tree", font_size=21, color=YES),
            label(r"proof: \ take a minimum tree without it \ (blue); \\ adding it closes a cycle, \ which crosses "
                  r"the split again \\ on an edge at least as heavy \ (9): \ swap them", font_size=20, color=GREY_A),
            label("\\textbf{cycle property}: \\ the uniquely heaviest edge on a cycle \\\\ belongs to no minimum tree; \\ ties require care", font_size=21, color=NO),
            label("these three classic algorithms schedule safe cut choices", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if steps.width > 6.2:
            steps.scale_to_fit_width(6.2).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "A minimum spanning tree connects a connected undirected weighted graph with the least total "
            "edge weight. <bookmark mark='a'/> It has V minus one edges and no cycle. The weights may be "
            "negative; shortest-path assumptions are not needed here. <bookmark mark='b'/> For any cut, "
            "any lightest crossing edge belongs to some minimum spanning tree. <bookmark mark='c'/> Add "
            "that edge to a minimum tree that avoids it. The resulting cycle crosses the cut again; "
            "replace a crossing edge of at least its weight. The new tree is no worse and contains the "
            "chosen edge. <bookmark mark='d'/> The related cycle rule needs care with ties: an edge "
            "uniquely heaviest on a cycle belongs to no minimum tree. A tied maximum edge may belong to "
            "one. <bookmark mark='e'/> The three classic algorithms use these safe choices in different "
            "orders."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(Create(cut), FadeIn(sides), FadeIn(steps[1]),
                      *[es[e].animate.set_color(HEAD) for e in crossing])
            self.play(es[("c", "d")].animate.set_color(YES).set_stroke(width=6))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), *[es[e].animate.set_color(DATA).set_stroke(width=5) for e in tree],
                      es[("c", "d")].animate.set_stroke(width=2).set_opacity(0.4),
                      es[("a", "d")].animate.set_color(GREY_D))
            self.play(es[("c", "d")].animate.set_color(YES).set_stroke(width=6).set_opacity(1))
            self.play(*[Indicate(es[e], color=WHITE, scale_factor=1.0) for e in cycle], run_time=1.2)
            self.play(es[("b", "e")].animate.set_color(NO).set_stroke(width=6))
            self.play(es[("b", "e")].animate.set_opacity(0.15),
                      es[("c", "d")].animate.set_color(DATA).set_stroke(width=5))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.wait(0.3)
        self.clear_scene()

    def kruskal(self):
        d = load("mst")
        head = label(rf"Kruskal \ (1956): \ {d['n']} points, \ lightest edges first", font_size=32).to_edge(
            UP, buff=0.3)
        pts = [np.array([x, 0.85 * y - 0.55, 0]) for x, y in d["pts"]]
        dots = VGroup(*[Dot(p, radius=0.05, color=GREY_A) for p in pts])
        tree = sorted(d["tree"], key=lambda e: np.linalg.norm(pts[e[0]] - pts[e[1]]))
        lines = [Line(pts[u], pts[v], color=YES, stroke_width=2.2) for u, v in tree]
        note_ = label(rf"total length {d['kruskal']:.2f}: \ the same from Prim's and Bor\r{{u}}vka's algorithms",
                      font_size=20, color=HEAD).to_edge(DOWN, buff=0.3)
        side = label(r"sort the edges; \ take each one unless it closes a cycle \ (Part 17's union--find decides)",
                     font_size=20, color=GREY_A).next_to(head, DOWN, buff=0.15)
        with self.voiceover(
            "Joseph Kruskal's algorithm is the cut property applied greedily. <bookmark mark='a'/> Sort all the edges "
            "by weight, and go through them from the lightest, keeping each edge unless it would close a cycle. "
            "Whether two points are already connected is exactly the question Part 17's union–find answers in "
            "almost constant time. <bookmark mark='b'/> Watch the forest form: short edges first, joining nearby "
            "points into clusters, then longer edges joining clusters. <bookmark mark='c'/> The result, on these "
            "hundred and twenty points, has the same total length that Prim's and Borůvka's algorithms find."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots), FadeIn(side))
            vo.wait_until("a")
            self.wait(0.5)
            vo.wait_until("b")
            batch = 6
            for k in range(0, len(lines), batch):
                self.play(*[Create(l) for l in lines[k:k + batch]], run_time=0.25)
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def algorithms(self):
        d = load("mst")
        head = label(r"Three schedules of the same property", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(label(r"\textbf{Kruskal} \ (1956)", font_size=22, color=YES),
                   label(r"edges in order of weight; \ union--find: \ $O(E \log E)$", font_size=20, color=GREY_A)),
            VGroup(label(r"\textbf{Prim} \ (1957; \ Jarn\'ik 1930)", font_size=22, color=DATA),
                   label(r"grow one tree; \ the lightest edge leaving it, \ from a heap: \ $O(E \log V)$", font_size=20,
                         color=GREY_A)),
            VGroup(label(r"\textbf{Bor\r{u}vka} \ (1926)", font_size=22, color=LAM),
                   label(rf"every component picks its lightest edge out, \ at once; \ components at least halve: \ "
                         rf"{d['rounds']} rounds here", font_size=20, color=GREY_A)),
            VGroup(label(r"\textbf{Karger, \ Klein and Tarjan} \ (1995)", font_size=22, color=HEAD),
                   label(r"Bor\r{u}vka steps plus random sampling: \ expected $O(E)$", font_size=20, color=GREY_A)),
        )
        for r in rows:
            r.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.55)
        note_ = label(r"Bor\r{u}vka's steps are independent: \ the parallel and distributed algorithms start there",
                      font_size=20, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Three classic methods schedule safe edges differently. <bookmark mark='a'/> Kruskal sorts "
            "edges and uses union-find, taking order E log E for this implementation. <bookmark "
            "mark='b'/> Prim grows one tree using a heap; Jarník described an earlier version. The "
            "binary-heap bound differs from a Fibonacci-heap implementation. <bookmark mark='c'/> Boruvka"
            " lets each remaining component choose a lightest outgoing edge, with a consistent tie rule. "
            "On a connected graph the number of components at least halves per round. <bookmark "
            "mark='d'/> Karger, Klein and Tarjan's randomized algorithm achieves expected linear time in "
            "the comparison model; it is a theorem cited here, not the code we just timed. <bookmark "
            "mark='e'/> Boruvka's simultaneous choices also motivate parallel and distributed algorithms,"
            " whose communication costs require their own analysis."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(Indicate(r, color=YES) if mk == "a" else FadeIn(r, shift=RIGHT * .1), run_time=.7)
            vo.wait_until("e")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
