from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, draw_graph,
                                   grid_table, load, mono, words)


class AllPairs(VoiceoverScene):
    def construct(self):
        self.card()
        self.floyd()
        self.johnson()
        self.minplus()

    def card(self):
        card = chapter_card(8, r"All pairs", r"Every distance, \ between every pair?", lit=(1962,),
                            extra=((1962, r"Floyd; \ Warshall"), (1977, r"Johnson: \ reweighting")), part=PART)
        with self.voiceover("Chapter eight. All pairs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def floyd(self):
        head = label(r"Floyd--Warshall: \ allow one more waypoint", font_size=34).to_edge(UP, buff=0.3)
        src = code(["for k in 0 .. n-1:", "    for i in 0 .. n-1:", "        for j in 0 .. n-1:",
                    "            d[i][j] = min(d[i][j], d[i][k] + d[k][j])"], size=20, color=CODE).next_to(
            head, DOWN, buff=0.6)
        steps = VGroup(
            MathTex(r"d_k(i, j) = \text{shortest } i \to j \text{ path using only waypoints } 0, \ldots, k - 1",
                    font_size=30, color=GREY_A),
            MathTex(r"d_{k+1}(i, j) = \min\bigl(d_k(i, j),\ d_k(i, k) + d_k(k, j)\bigr)", font_size=34, color=YES),
            label(r"either the best path avoids waypoint $k$, \ or it passes through it once", font_size=22,
                  color=GREY_A),
            label(r"$O(V^3)$, \ three loops, \ any edge weights without negative cycles: \ \textbf{dynamic "
                  r"programming} \ (Part 19)", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(src, DOWN, buff=0.5)
        with self.voiceover(
            "Sometimes we want the distance between every pair of vertices, for a routing table or a distance "
            "matrix. <bookmark mark='a'/> Robert Floyd and Stephen Warshall's algorithm from 1962 is three nested "
            "loops. <bookmark mark='b'/> The idea is to build up the set of vertices a path may pass through. Let d "
            "k of i, j be the shortest path from i to j that uses only the first k vertices as waypoints. <bookmark "
            "mark='c'/> Allowing one more waypoint, the best path either avoids it, or goes from i to the new "
            "waypoint and from there to j. <bookmark mark='d'/> That is the whole proof. It runs in cubic time, "
            "handles negative edges, and is the first example of dynamic programming in this course: Part 19 makes "
            "the method general."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src))
            for mk, s in zip("bcd", (steps[0], steps[1:3], steps[3])):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()

    def johnson(self):
        d = load("allpairs")
        head = label(r"Johnson's reweighting \ (1977)", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"sparse graphs, \ negative edges: \ $V$ runs of Dijkstra would be faster, \\ if only the weights "
                  r"were non-negative", font_size=21, color=GREY_A),
            label(r"add a vertex $q$ joined to every vertex by weight 0; \\ Bellman--Ford gives potentials $p(v) = "
                  r"\mathrm{dist}(q, v)$", font_size=21, color=GREY_A),
            MathTex(r"w'(u, v) = w(u, v) + p(u) - p(v) \ \ge 0", font_size=34, color=YES),
            label(r"non-negative by the triangle inequality: \\ $p(v) \le p(u) + w(u, v)$", font_size=21,
                  color=GREY_A),
            label(r"every path from $s$ to $t$ changes by the same $p(s) - p(t)$: \\ shortest paths are unchanged",
                  font_size=21, color=HEAD),
            label(rf"measured: \ {words(d['n'])} vertices, \ {words(d['m'])} edges, \ {d['negative_edges']} of them "
                  rf"negative; \\ reweighted minimum {d['min_reweighted']:.0f}; \ answers equal Floyd--Warshall's",
                  font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)
        if steps.width > 7.0:
            steps.scale_to_fit_width(7.0).to_edge(RIGHT, buff=0.4)
        # a worked example: potentials from q, then the reweighted edges
        pos = {"a": (-5.9, 1.2), "b": (-3.6, 1.2), "c": (-3.6, -1.4), "d": (-5.9, -1.4)}
        W = {("a", "b"): 2, ("b", "c"): -3, ("a", "c"): 1, ("c", "d"): 2, ("a", "d"): 4, ("b", "d"): 1}
        pot = {v: 0 for v in pos}
        for _ in range(len(pos)):
            for (u, v), w in W.items():
                pot[v] = min(pot[v], pot[u] + w)
        Wp = {(u, v): w + pot[u] - pot[v] for (u, v), w in W.items()}
        assert min(Wp.values()) >= 0
        g, nodes, es = draw_graph(pos, list(W), directed=True, weights=W, r=0.26)
        g.shift(DOWN * 0.2)
        pl = VGroup(*[label(rf"$p = {pot[v]}$", font_size=20, color=LAM).next_to(nodes[v], DOWN if pos[v][1] < 0 else UP,
                                                                               buff=0.12) for v in pos])
        new_w = VGroup(*[mono(str(Wp[e]), 15, YES).move_to(g.weights[i]) for i, e in enumerate(W)])
        with self.voiceover(
            "For sparse graphs there is a faster way, if we can get rid of the negative edges. <bookmark "
            "mark='a'/> Running Dijkstra from every vertex would cost V times E log V, much less than V cubed, but "
            "Dijkstra needs non-negative weights. <bookmark mark='b'/> Donald Johnson's trick: add a new vertex "
            "joined to everything by weight zero, and run Bellman–Ford once from it to get a potential p for every "
            "vertex. <bookmark mark='c'/> Then reweight every edge: w prime is w plus p of u minus p of v. <bookmark "
            "mark='d'/> That is never negative, because the potentials are shortest distances and obey the triangle "
            "inequality. <bookmark mark='e'/> And along any path the potentials telescope: every path from s to t "
            "changes by the same amount, p of s minus p of t, so the shortest paths are the same paths. <bookmark "
            "mark='f'/> On our test graph, with two hundred and thirty-one negative edges, the reweighted graph has no "
            "negative edge at all, and the answers match Floyd–Warshall's exactly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(pl))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), Transform(g.weights, new_w), *[es[e].animate.set_color(YES) for e in W])
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
            vo.wait_until("f")
            self.play(FadeIn(steps[5]))
        self.wait(0.3)
        self.clear_scene()

    def minplus(self):
        head = label(r"Shortest paths are matrix products", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            MathTex(r"(A \star B)_{ij} = \min_k \bigl(A_{ik} + B_{kj}\bigr)", font_size=38, color=YES),
            label(r"the \textbf{min-plus} product: \ ordinary matrix multiplication with $(+, \times)$ replaced by "
                  r"$(\min, +)$", font_size=22, color=GREY_A),
            label(r"$W^{\star k}$ holds the shortest paths of at most $k$ edges; \ squaring $\lg V$ times gives all of "
                  r"them", font_size=22, color=GREY_A),
            label(r"ordinary products have fast algorithms \ (Strassen, \ Part 16's master theorem); \ min-plus "
                  r"products seem not to", font_size=22, color=HEAD),
            label(r"\textbf{the APSP conjecture}: \ no $O(V^{3 - \varepsilon})$ algorithm for all-pairs shortest "
                  r"paths \ (Part 16's frontier; \ Part 27)", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "There is a deeper way to see all pairs. <bookmark mark='a'/> Define a product of matrices where the "
            "entry for i, j is the minimum over k of a i k plus b k j. <bookmark mark='b'/> It is matrix "
            "multiplication with plus and times replaced by min and plus. <bookmark mark='c'/> The weight matrix "
            "raised to the k-th power in this algebra holds the shortest paths of at most k edges, and repeated "
            "squaring gets all of them. <bookmark mark='d'/> Ordinary matrix products have sub-cubic algorithms, "
            "Strassen's from Part 16 among them, but they rely on subtraction, which min does not have. <bookmark "
            "mark='e'/> Whether all-pairs shortest paths can be done in truly sub-cubic time is a central "
            "conjecture of fine-grained complexity, the one Part 16's frontier mentioned, and dozens of graph "
            "problems are known to be exactly as hard."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()
