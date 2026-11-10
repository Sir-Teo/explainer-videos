from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, draw_graph, load,
                                   mono, words)


class Planar(VoiceoverScene):
    def construct(self):
        self.card()
        self.formula()
        self.colours()
        self.five()
        self.mapview()

    def card(self):
        card = chapter_card(15, r"Planar graphs and four colours", r"How many colours does a map need?", lit=(1976,),
                            extra=((1852, r"Guthrie's question"), (1976, r"Appel and Haken"),
                                   (2005, r"Gonthier: \ checked in Coq")), part=PART)
        with self.voiceover("Chapter fifteen. Planar graphs and four colours."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def formula(self):
        d = load("planar")
        head = label(r"Euler's formula", font_size=34).to_edge(UP, buff=0.3)
        cube = {0: (-5.0, 1.4), 1: (-2.6, 1.4), 2: (-2.6, -1.0), 3: (-5.0, -1.0), 4: (-4.2, 0.6), 5: (-3.4, 0.6),
                6: (-3.4, -0.2), 7: (-4.2, -0.2)}
        edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
        g, nodes, es = draw_graph(cube, edges, r=0.16, font=12)
        f = MathTex(r"V - E + F = 2", font_size=44, color=YES).to_edge(RIGHT, buff=1.2).shift(UP * 1.4)
        steps = VGroup(
            label(r"a cube drawn flat: \ $8 - 12 + 6 = 2$ \\ (the outside is a face)", font_size=21, color=GREY_A),
            label(rf"our triangulated map: \ {d['V']} $-$ {d['E']} $+$ {d['F']} $=$ {d['euler']}", font_size=21,
                  color=GREY_A),
            label("simple planar graph, \\ $V\\ge3$: \\ every face boundary has at least 3 incidences, \\\\ every edge borders 2 faces: \\ $E \\le 3V - 6$", font_size=21,
                  color=HEAD),
            label(r"so a planar graph is sparse, \\ and has a vertex of degree at most 5", font_size=21, color=YES),
            label(r"$K_5$ has $10 > 3 \cdot 5 - 6$ edges: \\ it cannot be drawn without crossings", font_size=21,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(f, DOWN, buff=0.45).to_edge(RIGHT, buff=0.4)
        if steps.width > 6.6:
            steps.scale_to_fit_width(6.6).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "A planar graph admits a drawing with no edge crossings except at common endpoints. <bookmark"
            " mark='a'/> For a connected plane graph, counting the outer face, Euler's formula is "
            "vertices minus edges plus faces equals two. The cube gives eight minus twelve plus six. With"
            " c components the corresponding total is one plus c. <bookmark mark='b'/> Our connected "
            "triangulated grid is checked against the same formula. <bookmark mark='c'/> For a simple "
            "planar graph with at least three vertices, counting face-boundary incidences gives at most "
            "three V minus six edges; multiple edges and loops need different qualifications. <bookmark "
            "mark='d'/> The average degree is below six, so some vertex has degree at most five; this "
            "remains true in every simple planar subgraph. <bookmark mark='e'/> The complete graph on "
            "five vertices violates the bound and is not planar."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(f))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()

    def colours(self):
        head = label(r"Four colours suffice", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"1852: \ Francis Guthrie colours the counties of England with four colours, \\ and asks if that "
                  r"always works", font_size=21, color=GREY_A),
            label(r"five colours: \ Heawood \ (1890), \ from the vertex of degree $\le 5$ \ (next)", font_size=21,
                  color=GREY_A),
            label(r"four: \ Appel and Haken \ (1976), \ 1,936 configurations checked by computer: \\ the first major "
                  r"proof that needed one", font_size=21, color=HEAD),
            label("Gonthier \\ (2005): \\ a formal four-colour proof checked in Coq \\ (Part 54)", font_size=21,
                  color=YES),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        pal = [DATA, YES, NO, LAM]
        c4 = DOWN * 2.15
        regions = VGroup(*[AnnularSector(inner_radius=0.55, outer_radius=1.25, angle=2 * PI / 3, start_angle=PI / 2 +
                                         k * 2 * PI / 3, color=pal[k], fill_opacity=0.55, stroke_color=WHITE,
                                         stroke_width=2).move_arc_center_to(c4) for k in range(3)],
                         Circle(radius=0.55, color=pal[3], fill_opacity=0.55, stroke_color=WHITE,
                                stroke_width=2).move_to(c4))
        rcap = label(r"four regions that all touch each other: \\ four colours are sometimes necessary",
                     font_size=19, color=GREY_B).next_to(regions, RIGHT, buff=0.5)
        with self.voiceover(
            "Map colouring requires regions sharing a border segment to differ; meeting only at a point "
            "does not count. For ordinary connected regions the adjacency graph is planar. <bookmark "
            "mark='a'/> Guthrie's 1852 question asked whether four colours always suffice. <bookmark "
            "mark='b'/> The five-colour theorem has a short inductive proof using the low-degree vertex "
            "and Kempe chains. <bookmark mark='c'/> Appel and Haken's 1976 four-colour proof used a "
            "finite reducibility computation; it was not just a search for colourings of a few maps. "
            "<bookmark mark='d'/> Gonthier's later Coq development formalized and machine-checked a "
            "four-colour proof. Our backtracking illustration is separate from those theorem proofs, and "
            "does not recreate their configuration checks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(regions), FadeIn(rcap))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()

    def five(self):
        head = label(r"Why five colours always suffice", font_size=34).to_edge(UP, buff=0.3)
        pal = [DATA, YES, NO, LAM, HEAD]
        c0 = np.array([-3.6, -0.5, 0])

        def disc(p, k, r=0.26):
            return VGroup(Circle(radius=r, color=pal[k - 1], fill_color=pal[k - 1], fill_opacity=0.55,
                                 stroke_width=2).move_to(p), mono(str(k), 18, WHITE).move_to(p))

        def at(deg, rad):
            a = np.deg2rad(deg)
            return c0 + rad * np.array([np.cos(a), np.sin(a), 0])
        npos = [at(90 + 72 * k, 1.6) for k in range(5)]
        spokes = VGroup(*[Line(c0, p, color=GREY_B, stroke_width=2) for p in npos])
        ring = VGroup(*[Line(npos[k], npos[(k + 1) % 5], color=GREY_D, stroke_width=1.5) for k in range(5)])
        ns = VGroup(*[disc(p, k + 1) for k, p in enumerate(npos)])
        nl = VGroup(*[label(rf"$n_{k + 1}$", font_size=18, color=GREY_B).move_to(c0 + (p - c0) * 1.32)
                      for k, p in enumerate(npos)])
        v = VGroup(Circle(radius=0.26, color=WHITE, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(c0),
                   MathTex(r"v", font_size=30).move_to(c0))
        # a chain of colours 1 and 3 from n1 round the left to n3
        cp = [at(130, 2.75), at(180, 2.95)]
        chain_nodes = VGroup(disc(cp[0], 3, 0.22), disc(cp[1], 1, 0.22))
        path = [npos[0], cp[0], cp[1], npos[2]]
        chain = VGroup(*[Line(a, b, color=WHITE, stroke_width=4) for a, b in zip(path, path[1:])])
        loop = Polygon(c0, *path, color=YES, stroke_width=0, fill_color=YES, fill_opacity=0.12)
        steps = VGroup(
            label(r"every planar graph has a vertex $v$ of degree $\le 5$: \\ remove it, \ colour the rest by "
                  r"induction", font_size=20, color=GREY_A),
            label(r"if $v$'s neighbours use at most 4 colours, \\ $v$ takes the fifth", font_size=20, color=GREY_A),
            label(r"otherwise look at a \textbf{Kempe chain}: \\ the vertices of colours 1 and 3 reachable from $n_1$; "
                  r"\\ if it misses $n_3$, \ swap 1 and 3 in it", font_size=20, color=GREY_A),
            label(r"if it reaches $n_3$, \ it closes a loop through $v$ \\ that separates $n_2$ from $n_4$: \\ so the "
                  r"2--4 chain from $n_2$ misses $n_4$, \ and we swap that one", font_size=20, color=HEAD),
            label(r"either way a colour is freed for $v$", font_size=21, color=YES),
            label(r"Kempe \ (1879) \ claimed this proves four; \\ Heawood \ (1890) \ found the gap, \ and it stayed "
                  r"open for 86 years", font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if steps.width > 6.6:
            steps.scale_to_fit_width(6.6).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "The five-colour proof uses the cyclic order of neighbours in a planar drawing. <bookmark "
            "mark='a'/> Remove a vertex v of degree at most five and colour the smaller graph by "
            "induction. <bookmark mark='b'/> If its neighbours use at most four colours, one of five is "
            "free for v. <bookmark mark='c'/> Otherwise number the five differently coloured neighbours "
            "around v. If the connected one-three colour component of neighbour one avoids neighbour "
            "three, swap those two colours throughout that component. Colour one becomes free. <bookmark "
            "mark='d'/> If the component connects neighbours one and three, choose a simple path in it. "
            "Together with v it forms a separating cycle, so a two-four colour path cannot join "
            "neighbours two and four without crossing. Swap the two-four component containing neighbour "
            "two instead. <bookmark mark='e'/> A colour is free in either case. <bookmark mark='f'/> The "
            "chain idea comes from Kempe; Heawood identified the flaw in Kempe's four-colour argument and"
            " established the five-colour theorem."
        ) as vo:
            self.play(FadeIn(head), Create(ring), Create(spokes), FadeIn(ns), FadeIn(nl), FadeIn(v))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), FadeIn(chain_nodes), Create(chain))
            vo.wait_until("d")
            self.play(FadeIn(loop), FadeIn(steps[3]))
            self.play(Indicate(ns[1], color=WHITE), Indicate(ns[3], color=WHITE))
            self.play(Transform(ns[1], disc(npos[1], 4)))
            vo.wait_until("e")
            self.play(Transform(v, disc(c0, 2)), FadeIn(steps[4]))
            vo.wait_until("f")
            self.play(FadeIn(steps[5]))
        self.wait(0.3)
        self.clear_scene()

    def mapview(self):
        d = load("planar")
        head = label(rf"Colouring our {d['V']}-vertex map", font_size=34).to_edge(UP, buff=0.3)
        pal = [DATA, YES, NO, LAM, HEAD]

        def P(v):
            return np.array([-6.2 + 0.74 * v[0], -2.5 + 0.74 * v[1], 0])
        es = VGroup(*[Line(P(a), P(b), color=GREY_D, stroke_width=1.5) for a, b in d["edges"]])
        greedy = {tuple(v): c for v, c in d["greedy_col"]}
        four = {tuple(v): c for v, c in d["four"]}
        dots = {v: Dot(P(v), radius=0.13, color=pal[c]) for v, c in greedy.items()}
        dg = VGroup(*dots.values())
        fifth = VGroup(*[Circle(radius=0.22, color=WHITE, stroke_width=2).move_to(P(v)) for v, c in greedy.items()
                         if c == 4])
        adj = {}
        for a, b in d["edges"]:
            adj.setdefault(tuple(a), set()).add(tuple(b))
            adj.setdefault(tuple(b), set()).add(tuple(a))
        hub = next(v for v in sorted(adj) if 0 < v[0] < 8 and 0 < v[1] < 5 and len(adj[v]) == 5
                   and all(len(adj[u] & adj[v]) == 2 for u in adj[v]))
        wheel = VGroup(*[Line(P(a), P(b), color=WHITE, stroke_width=4) for a in adj[hub] for b in adj[hub] & adj[a]
                         if a < b], *[Line(P(hub), P(a), color=WHITE, stroke_width=2.5) for a in adj[hub]])
        side = VGroup(
            label(r"greedy colouring, \ vertex by vertex, \\ smallest free colour:", font_size=21, color=GREY_A),
            label(rf"{d['greedy']} colours \\ (the circled vertex needed the fifth)", font_size=22, color=NO),
            label(r"backtracking, \ most constrained vertex first: \\ 4 colours", font_size=22, color=YES),
            label(r"and the same search proves 3 impossible: \\ a vertex ringed by an odd cycle needs a fourth", font_size=21,
                  color=HEAD),
            label(r"deciding 3-colourability is NP-complete, \\ even for planar graphs \ (Part 26)", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.4)
        if side.width > 5.6:
            side.scale_to_fit_width(5.6).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"Now our triangulated map. <bookmark mark='a'/> Greedy colouring visits the vertices in order and "
            f"gives each the smallest colour its coloured neighbours do not use. <bookmark mark='b'/> It needs "
            f"{words(d['greedy'])} colours here: this circled vertex took the fifth. Greedy is fast but not "
            f"optimal. <bookmark mark='c'/> A backtracking search, which always colours the most constrained "
            f"vertex next and undoes choices that lead nowhere, finds a colouring with four. <bookmark mark='d'/> "
            f"It also proves that three are not enough: the map contains a vertex whose five neighbours form a "
            f"cycle, and an odd cycle needs three colours on its own, leaving none for the centre. <bookmark mark='e'/> Four colours always exist and are "
            f"found in quadratic time. But deciding whether three suffice is NP-complete, even for planar graphs."
        ) as vo:
            self.play(FadeIn(head), Create(es), FadeIn(dg))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Create(fifth))
            vo.wait_until("c")
            self.play(FadeOut(fifth), *[dots[v].animate.set_color(pal[four[v]]) for v in dots], FadeIn(side[2]),
                      run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Create(wheel))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), FadeOut(wheel))
        self.wait(0.3)
        self.clear_scene()
