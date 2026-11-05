from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, draw_graph,
                                   load, mono, words)


class Dijkstra(VoiceoverScene):
    def construct(self):
        self.card()
        self.small()
        self.invariant()
        self.wavefront()

    def card(self):
        card = chapter_card(6, r"Dijkstra's algorithm", r"How do you find the shortest road?", lit=(1959,),
                            extra=((1956, r"designed in twenty minutes, \ at a caf\'e"), (1959, r"published")),
                            part=PART)
        with self.voiceover("Chapter six. Dijkstra's algorithm."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def small(self):
        head = label(r"Settle the nearest unsettled vertex", font_size=34).to_edge(UP, buff=0.3)
        pos = {"s": (-5.0, 0.0), "a": (-3.2, 1.4), "b": (-3.2, -1.4), "c": (-1.2, 1.4), "d": (-1.2, -1.4),
               "t": (0.6, 0.0)}
        w = {("s", "a"): 4, ("s", "b"): 1, ("b", "a"): 2, ("a", "c"): 5, ("b", "d"): 8, ("c", "d"): 1, ("c", "t"): 3,
             ("d", "t"): 6}
        g, nodes, es = draw_graph(pos, list(w), directed=True, weights=w)
        # Dijkstra by hand
        import heapq
        adj = {k: [] for k in pos}
        for (u, v), x in w.items():
            adj[u].append((v, x))
        dist, done, order = {"s": 0}, set(), []
        pq = [(0, "s")]
        while pq:
            dd, u = heapq.heappop(pq)
            if u in done:
                continue
            done.add(u)
            order.append((u, dd))
            for v, x in adj[u]:
                if dd + x < dist.get(v, 1e9):
                    dist[v] = dd + x
                    heapq.heappush(pq, (dd + x, v))
        dl = {k: mono("", 18, HEAD) for k in pos}
        src = code(["dist[s] = 0;  all others = infinity", "repeat:",
                    "    u = the unsettled vertex with least dist",
                    "    settle u",
                    "    for each edge u -> v of length w:",
                    "        dist[v] = min(dist[v], dist[u] + w)"], size=16, color=CODE).to_edge(RIGHT, buff=0.4).shift(
            UP * 0.6)
        note_ = label(r"a priority queue (Part 17's heap) finds $u$: \ $O((V + E) \log V)$", font_size=21,
                      color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Edsger Dijkstra designed his shortest-path algorithm in about twenty minutes, sitting at a café in "
            "Amsterdam in 1956, to demonstrate a new computer. <bookmark mark='a'/> Every vertex gets a tentative "
            "distance: zero for the start, infinity for the rest. <bookmark mark='b'/> Repeatedly take the unsettled "
            "vertex with the smallest tentative distance, declare it settled, and relax its outgoing edges, "
            "lowering a neighbour's distance whenever the path through this vertex is shorter. <bookmark "
            "mark='c'/> Watch the order: s, then b at distance one, then a at three, reached more cheaply through b "
            "than directly. <bookmark mark='d'/> A priority queue, Part 17's heap, finds the nearest vertex, so the "
            "whole run costs order of V plus E, times log V."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(src))
            vo.wait_until("b")
            for u, dd in order:
                t = mono(str(dd), 18, HEAD).next_to(nodes[u], DOWN, buff=0.08)
                self.play(nodes[u][0].animate.set_fill(YES, 0.5), FadeIn(t), run_time=0.6)
                if u == "a":
                    vo.wait_until("c")
            vo.wait_until("d")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def invariant(self):
        head = label(r"Why it is right: \ an invariant", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"\textbf{invariant}: \ every settled vertex's distance is its true shortest distance", font_size=23,
                  color=YES),
            label(r"suppose $u$ is next, \ with tentative $d(u)$, \ and a shorter path $P$ to $u$ exists", font_size=22,
                  color=GREY_A),
            label(r"$P$ leaves the settled set somewhere: \ let $y$ be its first unsettled vertex", font_size=22,
                  color=GREY_A),
            MathTex(r"d(y) \le \operatorname{len}(P \text{ up to } y) \le \operatorname{len}(P) < d(u) \le d(y)",
                    font_size=34, color=NO),
            label(r"a contradiction: \ the middle step needs \textbf{non-negative} edge lengths", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.4)
        blob = Ellipse(width=5.0, height=2.5, color=YES, fill_color=YES, fill_opacity=0.12).move_to([-2.2, -2.3, 0])
        bl = label(r"the settled set", font_size=19, color=YES).next_to(blob, LEFT, buff=0.15)
        P = {"s": [-3.8, -2.6, 0], "x": [-1.2, -1.8, 0], "y": [1.6, -1.4, 0], "u": [4.2, -2.6, 0]}
        dots = VGroup(*[VGroup(Dot(P[k], radius=0.09, color=WHITE), label(rf"${k}$", font_size=24).next_to(
            Dot(P[k]), UP, buff=0.12)) for k in P])
        path = VGroup(Line(P["s"], P["x"], color=DATA, stroke_width=4), Line(P["x"], P["y"], color=DATA,
                      stroke_width=4), DashedLine(P["y"], P["u"], color=DATA, stroke_width=4))
        pl = label(r"$P$", font_size=24, color=DATA).move_to([2.9, -1.6, 0])
        du = label(r"tentative $d(u)$: \ the smallest outside", font_size=18, color=GREY_B).next_to(dots[3], DOWN,
                                                                                                  buff=0.2)
        with self.voiceover(
            "The proof is an invariant, as in Part 16. <bookmark mark='a'/> Claim: whenever a vertex is settled, its "
            "tentative distance is its true shortest distance. <bookmark mark='b'/> Suppose not, and let u be the "
            "first vertex settled too early: some path P to u is shorter than its tentative distance. <bookmark "
            "mark='c'/> P starts inside the settled set and must leave it somewhere; let y be the first vertex on P "
            "that is not yet settled. <bookmark mark='d'/> Its predecessor on P was settled correctly and relaxed the "
            "edge into y, so d of y is at most the length of P up to y, which is at most the length of P, which is "
            "less than d of u. But the algorithm chose u because d of u was smallest, so d of u is at most d of y. "
            "<bookmark mark='e'/> That is a contradiction, and the step that the length of a path only grows as it "
            "continues is exactly where edge lengths must be non-negative. Chapter seven shows what breaks without "
            "it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(blob), FadeIn(bl), FadeIn(dots[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(dots[3]), FadeIn(du))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), Create(path), FadeIn(dots[1]), FadeIn(dots[2]), FadeIn(pl), run_time=1.5)
            self.play(Indicate(dots[2], color=HEAD))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.wait(0.3)
        self.clear_scene()

    def wavefront(self):
        d = load("dijkstra")
        head = label(r"The wavefront, \ over a city", font_size=34).to_edge(UP, buff=0.3)
        pos = {tuple(map(int, k.split(","))): v for k, v in d["pos"].items()}
        xs = [p[0] for p in pos.values()]
        ys = [p[1] for p in pos.values()]
        sc = min(12.5 / (max(xs) - min(xs)), 5.6 / (max(ys) - min(ys)))
        cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2

        def at(p):
            return np.array([(p[0] - cx) * sc, (p[1] - cy) * sc - 0.4, 0])
        roads = VGroup()
        for u, v in d["edges"]:
            u, v = tuple(u), tuple(v)
            fast = (u[1] == v[1] and u[1] % 8 == 0) or (u[0] == v[0] and u[0] % 8 == 0)
            roads.add(Line(at(pos[u]), at(pos[v]), color=HEAD if fast else GREY_D, stroke_width=2.2 if fast else 1.0))
        order = d["order"]
        maxd = max(o[1] for o in order)
        dots = []
        for u, dist in order:
            col = interpolate_color(ManimColor(YES), ManimColor(NO), dist / maxd)
            dots.append(Dot(at(pos[tuple(u)]), radius=0.045, color=col))
        src = Dot(at(pos[tuple(d["source"])]), radius=0.1, color=WHITE)
        pts = label(rf"{words(d['n'])} intersections, \ {words(d['m'])} roads; \ arterials \ (gold) \ are three "
                    rf"times as fast", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is the algorithm running on a city of two thousand four hundred intersections, from one starting "
            "point. <bookmark mark='a'/> Each dot appears when its intersection is settled, coloured by its "
            "distance. The settled region grows outwards like a ripple, always the nearest unsettled point next. "
            "<bookmark mark='b'/> It is not a circle: the gold arterial roads are three times as fast, and the "
            "wavefront runs ahead along them. <bookmark mark='c'/> To find the distance to one destination, "
            "Dijkstra settles every intersection nearer than it, which is most of the city. Chapter nine shows how "
            "map apps avoid that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(roads), FadeIn(src), FadeIn(pts))
            vo.wait_until("a")
            batch = max(1, len(dots) // 40)
            for k in range(0, len(dots), batch):
                self.add(*dots[k:k + batch])
                self.wait(1 / 15)
                if k == batch * 20:
                    vo.wait_until("b")
            vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()
