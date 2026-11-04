from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import COST, CTRL, DATA, FUNC, HEAD, HIST, NO, PART, YES, live_int


def graph(pos: dict, edges: list, r=0.2, color=DATA, edge_color=GREY_B, labels=False, font_size=24) -> VGroup:
    g = VGroup()
    g.v = {k: Circle(r, stroke_color=color, stroke_width=3, fill_color="#121722", fill_opacity=1).move_to(
        np.array([*p, 0]) if len(p) == 2 else p) for k, p in pos.items()}
    g.e = VGroup(*[Line(g.v[a].get_center(), g.v[b].get_center(), buff=r, color=edge_color, stroke_width=3)
                   for a, b in edges])
    g.add(g.e, *g.v.values())
    if labels:
        g.lab = {k: MathTex(str(k), font_size=font_size).move_to(g.v[k]) for k in pos}
        g.add(*g.lab.values())
    return g


class Graphs(VoiceoverScene):
    def construct(self):
        self.card()
        self.konigsberg()
        self.handshake()
        self.trees()
        self.bipartite()

    def card(self):
        card = chapter_card(14, r"Graphs", r"What is the simplest model of a network?", part=PART)
        with self.voiceover("Chapter fourteen. Graphs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def konigsberg(self):
        head = label(r"Seven bridges", font_size=38).to_edge(UP, buff=0.35)
        # the four land masses and seven bridges, as a multigraph
        P = {"N": np.array([-3.4, 1.6, 0]), "S": np.array([-3.4, -2.2, 0]), "I": np.array([-3.4, -0.3, 0]),
             "E": np.array([-0.8, -0.3, 0])}
        nodes = {k: Dot(p, radius=0.16, color=DATA) for k, p in P.items()}
        names = {k: label(t, font_size=22, color=GREY_B).next_to(nodes[k], d, buff=0.15) for k, t, d in (
            ("N", r"north bank", UP), ("S", r"south bank", DOWN), ("I", r"island", LEFT), ("E", r"east", RIGHT))}

        def arc(a, b, angle):
            return ArcBetweenPoints(P[a], P[b], angle=angle, color=GREY_B, stroke_width=3)

        bridges = VGroup(arc("N", "I", 0.5), arc("N", "I", -0.5), arc("S", "I", 0.5), arc("S", "I", -0.5),
                         arc("N", "E", -0.4), arc("S", "E", 0.4), arc("I", "E", 0))
        degs = {"N": 3, "S": 3, "I": 5, "E": 3}
        dl = {k: MathTex(str(v), font_size=30, color=NO).next_to(nodes[k], RIGHT if k != "E" else UP, buff=0.12)
              for k, v in degs.items()}
        dl["I"].next_to(nodes["I"], UR, buff=0.08)
        for m in dl.values():
            m.add_background_rectangle(color=BACKGROUND, opacity=1, buff=0.04)
        txt = VGroup(*[label(t, font_size=27, color=c) for t, c in (
            (r"walk across every bridge exactly once?", GREY_A),
            (r"each pass through a place uses two bridges: \\ in and out", CTRL),
            (r"so every place, except the start and the end, \\ must touch an even number of bridges", HEAD),
            (r"here all four are odd: \ impossible", NO),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.3 + DOWN * 0.1)
        hc = note(r"Leonhard Euler, \ 1736: \ the first theorem of graph theory", font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The last structure of this part, and the one that carries networks, maps, dependencies and the web. "
            "<bookmark mark='a'/> The city of Königsberg had seven bridges joining two river banks, an island and a "
            "fourth piece of land. Could you take a walk that crosses every bridge exactly once? <bookmark mark='b'/> "
            "Leonhard Euler threw away everything but the land and the bridges: dots, and lines between them. A graph. "
            "<bookmark mark='c'/> Every time a walk passes through a place, it uses two bridges, one in and one out. "
            "So every place except the start and the end must touch an even number of bridges. <bookmark mark='d'/> In "
            "Königsberg all four touch an odd number. No such walk exists. That was 1736, and it was the first theorem "
            "of graph theory."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*nodes.values())), FadeIn(VGroup(*names.values())), FadeIn(txt[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b) for b in bridges], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(txt[1]), FadeIn(txt[2]))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*dl.values())), FadeIn(txt[3]), FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def handshake(self):
        head = label(r"The handshake lemma", font_size=38).to_edge(UP, buff=0.35)
        rng = np.random.default_rng(8)
        n = 9
        ang = np.linspace(0, 2 * PI, n, endpoint=False) + 0.3
        pos = {k: np.array([2.2 * np.cos(a) - 2.8, 1.75 * np.sin(a) + 0.15, 0]) for k, a in enumerate(ang)}
        edges = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < 0.3]
        g = graph(pos, edges)
        deg = {k: sum(1 for e in edges if k in e) for k in range(n)}
        dls = VGroup(*[MathTex(str(deg[k]), font_size=28, color=NO if deg[k] % 2 else YES).move_to(g.v[k])
                       for k in range(n)])
        tot = sum(deg.values())
        eq = MathTex(r"\sum_v \deg v = " + " + ".join(str(deg[k]) for k in range(n)) + f" = {tot} = 2 \\cdot {len(edges)}",
                     font_size=30, color=CTRL).to_edge(DOWN, buff=0.9)
        why = label(r"each edge has two ends", font_size=28, color=GREY_A).move_to(RIGHT * 3.6 + UP * 1.2)
        odd = label(r"so the number of odd-degree \\ vertices is always even", font_size=28, color=HEAD).next_to(
            why, DOWN, buff=0.5)
        oc = label(rf"here: \ {sum(1 for v in deg.values() if v % 2)}", font_size=28, color=NO).next_to(odd, DOWN,
                                                                                                     buff=0.3)
        with self.voiceover(
            "The bridge argument hides a fact about every graph. <bookmark mark='a'/> Label each vertex with its degree, "
            "the number of edges that touch it. <bookmark mark='b'/> Add up the degrees. Every edge has two ends, so "
            "every edge is counted exactly twice: the sum is twice the number of edges. <bookmark mark='c'/> In "
            "particular the sum is even, so the number of vertices with odd degree is even. At any party, the number of "
            "people who shook an odd number of hands is even. Counting the same thing two ways, again."
        ) as vo:
            self.play(FadeIn(head), Create(g.e), FadeIn(VGroup(*g.v.values())))
            vo.wait_until("a")
            self.play(FadeIn(dls))
            vo.wait_until("b")
            self.play(FadeIn(why), Write(eq))
            vo.wait_until("c")
            self.play(FadeIn(odd), FadeIn(oc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trees(self):
        head = label(r"Trees: \ connected, \ with no cycles", font_size=38).to_edge(UP, buff=0.35)
        pos = {0: (-3.0, 1.4), 1: (-4.6, 0.3), 2: (-3.0, 0.2), 3: (-1.4, 0.3), 4: (-5.3, -1.0), 5: (-3.9, -1.0),
               6: (-1.9, -1.0), 7: (-0.7, -1.0), 8: (-3.0, -2.2)}
        edges = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (3, 6), (3, 7), (5, 8)]
        g = graph(pos, edges)
        eq = VGroup(*[label(t, font_size=27, color=c) for t, c in (
            (r"for a graph on $n$ vertices, \ these say the same thing:", GREY_A),
            (r"connected, \ and no cycles", YES),
            (r"connected, \ and exactly $n - 1$ edges", YES),
            (r"exactly one path between any two vertices", YES),
            (r"connected, \ but removing any edge disconnects it", YES),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.0 + UP * 0.4)
        n_e = label(rf"$9$ vertices, \ $8$ edges", font_size=26, color=CTRL).next_to(eq, DOWN, buff=0.5).align_to(
            eq, LEFT)
        extra = Line(g.v[4].get_center(), g.v[8].get_center(), buff=0.2, color=NO, stroke_width=4)
        cyc = label(r"one more edge: \ a cycle", font_size=26, color=NO).next_to(n_e, DOWN, buff=0.15)
        cut = label(r"one fewer: \ two pieces", font_size=26, color=HEAD).next_to(cyc, DOWN, buff=0.15)
        later = note(r"spanning trees, \ shortest-path trees, \ the routing tables of the internet: \ Parts 18 and 36",
                     font_size=22).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "A tree, in graph theory, is a connected graph with no cycles. <bookmark mark='a'/> Several quite different "
            "descriptions turn out to be the same: connected with no cycles; connected with exactly n minus one edges; "
            "exactly one path between any two vertices; connected, but fragile, so that removing any edge disconnects "
            "it. Proving they are equivalent is a good exercise in induction. <bookmark mark='b'/> Nine vertices, eight "
            "edges. <bookmark mark='c'/> Add any edge, and it closes a cycle. <bookmark mark='d'/> Remove any edge, and "
            "the tree falls into two pieces. Trees are the cheapest way to connect things, which is why a network that "
            "must reach every machine without loops, from a power grid to the routing of the internet, builds one."
        ) as vo:
            self.play(FadeIn(head), Create(g.e), FadeIn(VGroup(*g.v.values())))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in eq], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(n_e))
            vo.wait_until("c")
            self.play(Create(extra), FadeIn(cyc))
            vo.wait_until("d")
            self.play(FadeOut(extra), g.e[2].animate.set_stroke(opacity=0.15), FadeIn(cut))
            self.play(VGroup(g.v[3], g.v[6], g.v[7], g.e[5], g.e[6]).animate.shift(RIGHT * 0.5), run_time=0.8)
            self.play(FadeIn(later))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bipartite(self):
        head = label(r"Two colours, \ and odd cycles", font_size=38).to_edge(UP, buff=0.35)
        ang6 = np.linspace(0, 2 * PI, 6, endpoint=False) + PI / 2
        pos6 = {k: np.array([1.5 * np.cos(a) - 3.6, 1.5 * np.sin(a) - 0.2, 0]) for k, a in enumerate(ang6)}
        e6 = [(k, (k + 1) % 6) for k in range(6)] + [(0, 3)]
        g6 = graph(pos6, e6)
        ang5 = np.linspace(0, 2 * PI, 5, endpoint=False) + PI / 2
        pos5 = {k: np.array([1.5 * np.cos(a) + 1.6, 1.5 * np.sin(a) - 0.2, 0]) for k, a in enumerate(ang5)}
        e5 = [(k, (k + 1) % 5) for k in range(5)]
        g5 = graph(pos5, e5)
        cols = [DATA, CTRL]
        stmt = label(r"a graph can be 2-coloured, \ every edge joining different colours, \\ exactly when it has no "
                     r"cycle of odd length", font_size=27, color=YES).to_edge(DOWN, buff=1.0)
        how = note(r"colour by distance from a start vertex, \ even or odd \ (breadth-first search, Part 18)",
                   font_size=22).next_to(stmt, DOWN, buff=0.2)
        clash = label(r"clash", font_size=26, color=NO).next_to(g5, RIGHT, buff=0.2)
        with self.voiceover(
            "One more theorem, which Part 18 turns into an algorithm. <bookmark mark='a'/> Can the vertices be "
            "coloured with two colours so that every edge joins different colours? Colour one vertex blue, its "
            "neighbours orange, theirs blue, and so on outward. On this graph it works. <bookmark mark='b'/> On a cycle "
            "of five, going round, the colours alternate, blue, orange, blue, orange, blue, and the last vertex is "
            "next to the first: a clash. <bookmark mark='c'/> That is the whole story: a graph can be two-coloured "
            "exactly when it has no cycle of odd length. Going round an odd cycle flips the colour an odd number of "
            "times and you cannot get home; and if there is no odd cycle, colouring by the parity of the distance "
            "from a start vertex always works. Parity, one last time."
        ) as vo:
            self.play(FadeIn(head), Create(g6.e), FadeIn(VGroup(*g6.v.values())), Create(g5.e),
                      FadeIn(VGroup(*g5.v.values())))
            vo.wait_until("a")
            order = [0, 1, 5, 3, 2, 4]
            dist = {0: 0, 1: 1, 5: 1, 3: 1, 2: 2, 4: 2}
            for k in order:
                self.play(g6.v[k].animate.set_fill(cols[dist[k] % 2], 0.9), run_time=0.4)
            vo.wait_until("b")
            for k in range(5):
                self.play(g5.v[k].animate.set_fill(cols[k % 2], 0.9), run_time=0.45)
            self.play(g5.e[4].animate.set_stroke(NO, 6), FadeIn(clash))
            vo.wait_until("c")
            self.play(FadeIn(stmt), FadeIn(how))
        self.wait(0.3)
        self.clear_scene()
