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
            "Sometimes we need all pairwise distances. <bookmark mark='a'/> Floyd-Warshall uses three "
            "nested loops over intermediate vertex k, source i and target j. <bookmark mark='b'/> Before "
            "step k, d k of i, j is the shortest path allowing only vertices numbered below k as internal"
            " waypoints. Initialize the diagonal to zero and other entries to edge weights or infinity. "
            "<bookmark mark='c'/> When k becomes allowed, a shortest path either avoids k or splits there"
            " into an i-to-k part and a k-to-j part. <bookmark mark='d'/> This recurrence gives cubic "
            "time and quadratic space. Negative edges are allowed, but a reachable negative cycle can "
            "make some pairwise distances unbounded; a negative final diagonal detects that obstruction."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(Indicate(src, color=DATA, scale_factor=1.02), run_time=.7)
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
            "For a sparse graph without negative cycles, Johnson reweights before running Dijkstra. "
            "<bookmark mark='a'/> Repeated binary-heap searches can exploit sparsity, while the initial "
            "Bellman-Ford computation still has its own cost. <bookmark mark='b'/> Add a genuinely fresh "
            "source, joined to every vertex by zero-weight edges, and compute its distances p. A negative"
            " cycle aborts this construction. <bookmark mark='c'/> Reweight u-to-v by w plus p of u minus"
            " p of v. <bookmark mark='d'/> The shortest-path triangle inequality makes every reweighted "
            "edge nonnegative. <bookmark mark='e'/> Along a path, potentials telescope: every path with "
            "the same endpoints changes by the same constant, preserving its shortest choices. <bookmark "
            "mark='f'/> Our potential-generated test graph keeps its original negative edges. Every "
            "finite distance and every unreachable pair agrees with Floyd-Warshall; no fallback changes "
            "the input."
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
            label("with zero diagonal, \\ $W^{\\star k}$ holds walks of at most $k$ edges; \\ squaring $\\lg V$ times gives all of them", font_size=22, color=GREY_A),
            label("ordinary products have fast algorithms; \\\\ subtraction-based tricks do not automatically give fast min-plus products", font_size=22, color=HEAD),
            label("\\textbf{the APSP conjecture}: \\ general weighted APSP: \\ no $O(V^{3-\\varepsilon})$ in the stated model \\ (Part 16's frontier; \\ Part 27)", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "All-pairs distances also have an algebraic form. <bookmark mark='a'/> Define the i-j entry "
            "of a product as the minimum over k of a i-k plus b k-j. <bookmark mark='b'/> This is the "
            "min-plus product. <bookmark mark='c'/> With a zero diagonal, the k-th min-plus power "
            "describes walks of at most k edges. Without negative cycles, V minus one edges suffice for "
            "shortest paths, so repeated squaring reaches the answer. <bookmark mark='d'/> Fast ordinary "
            "matrix multiplication does not automatically transfer: subtraction is not available in "
            "min-plus arithmetic. <bookmark mark='e'/> The general weighted APSP conjecture rules out a "
            "fixed polynomial improvement below cubic time in its stated model. Restricted weight ranges "
            "and graph classes have different algorithms and are not ruled out by this broad slogan."
        ) as vo:
            self.play(FadeIn(head), FadeIn(steps[0]))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(Indicate(s, color=YES) if mk == "a" else FadeIn(s), run_time=.7)
        self.wait(0.3)
        self.clear_scene()
