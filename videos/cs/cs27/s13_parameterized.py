from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, sci, words)


class Parameterized(VoiceoverScene):
    def construct(self):
        self.card()
        self.search()
        self.theory()

    def card(self):
        card = chapter_card(12, r"Parameterized complexity", r"Can hardness be confined to one small number?",
                            lit=(1992, 1999), extra=((1993, r"Buss's kernel"), (1999, r"Downey--Fellows")), part=PART)
        with self.voiceover("Chapter twelve. Parameterized complexity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def search(self):
        v = load("vc")
        head = label(r"Vertex cover of size $k$: \ exponential only in $k$", font_size=32).to_edge(UP, buff=0.3)
        rows = [[str(r["k"]), str(r["edges"]), words(r["nodes"]), words(r["bound"]), rf"${sci(r['brute_subsets'], 2)}$",
                 f"{r['seconds'] * 1000:.1f} ms"] for r in v["rows"]]
        tab = grid_table([r"$k$", r"edges", r"search-tree nodes", r"$\le 2^{k+1}$", r"brute force $\binom{40}{k}$",
                          r"time"], rows, widths=[0.9, 1.2, 2.6, 1.6, 3.0, 1.6], row_h=0.42, font_size=19,
                         mono_cols=(), colors=[[WHITE, GREY_A, YES, GREY_A, NO, DATA]] * len(rows))
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        tl = label(rf"graphs on {v['n']} vertices with a planted cover of size $k$", font_size=18,
                   color=GREY_A).next_to(tab, DOWN, buff=0.12)
        lines = VGroup(
            label(r"\textbf{bounded search tree}: \ some end of any edge $(u, v)$ is in the cover: \ branch on the "
                  r"two choices, \ $k$ levels", font_size=21, color=WHITE),
            label(r"time $O(2^k \cdot m)$: \ fine for $k = 30$ on a million edges; \ brute force is $\binom{n}{k}$",
                  font_size=21, color=YES),
            label(r"\textbf{Buss's kernel}: \ a vertex of degree $> k$ must be in the cover; \ after removing them, "
                  r"more than $k^2$ edges means no", font_size=21, color=DATA),
            label(r"so any instance shrinks to $O(k^2)$ edges in linear time, \ \textbf{before} the search", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.22).next_to(tl, DOWN, buff=0.35)
        with self.voiceover(
            "Some NP-hard problems are easy when a parameter is small. <bookmark mark='a'/> Vertex cover asks for k "
            "vertices touching every edge. Pick any edge; one of its ends must be in the cover. Branch on the two "
            "choices, and recurse with k minus one. The tree has at most two to the k plus one nodes. <bookmark "
            "mark='b'/> On our graphs of forty vertices, a cover of size twelve took under eight thousand nodes and "
            "eight milliseconds; trying every set of twelve vertices would mean five and a half billion. <bookmark "
            "mark='c'/> Jonathan Buss added a preprocessing rule: a vertex with more than k neighbours must be in any "
            "small cover, and after taking those, a yes-instance has at most k squared edges left. <bookmark "
            "mark='d'/> So every instance shrinks to a kernel of size polynomial in k before the search begins."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab), FadeIn(tl))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def theory(self):
        head = label(r"FPT, \ W[1], \ and treewidth", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"\textbf{FPT}: \ solvable in $f(k) \cdot n^{O(1)}$ for some function $f$ \ (Downey and Fellows)",
                  font_size=22, color=WHITE),
            label(r"vertex cover: \ FPT, \ now $O(1.2738^k + kn)$ \ (Chen, \ Kanj, \ Xia, 2010)", font_size=22,
                  color=YES),
            label(r"$k$-clique: \ W[1]-hard: \ no $f(k) \cdot n^{O(1)}$ algorithm unless FPT = W[1]; \ $n^k$ seems "
                  r"necessary", font_size=22, color=NO),
            label(r"\textbf{treewidth}: \ how tree-like a graph is \ (Robertson and Seymour)", font_size=22,
                  color=DATA),
            label(r"Courcelle \ (1990): \ any property expressible in monadic second-order logic \\ is linear-time on "
                  r"graphs of bounded treewidth", font_size=22, color=HEAD),
            label(r"colouring, \ Hamiltonicity, \ independent set: \ easy on trees, \ series-parallel circuits, \ "
                  r"many real networks", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This is the theory of fixed-parameter tractability, built by Rodney Downey and Michael Fellows. "
            "<bookmark mark='a'/> A problem is FPT if it can be solved in time f of k times a polynomial in n, for "
            "any function f. <bookmark mark='b'/> Vertex cover is FPT; the record is about one point two seven to "
            "the k. <bookmark mark='c'/> Clique, by contrast, is W-one-hard: it is believed to need n to the k. "
            "<bookmark mark='d'/> A different parameter, treewidth, measures how much a graph resembles a tree. "
            "<bookmark mark='e'/> Bruno Courcelle proved that any property expressible in monadic second-order "
            "logic can be checked in linear time on graphs of bounded treewidth. <bookmark mark='f'/> Colouring, "
            "Hamiltonian cycles and independent sets all become easy on such graphs, which include many real "
            "networks."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
