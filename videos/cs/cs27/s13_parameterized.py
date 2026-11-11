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
            label('branching costs $O(2^k m)$; graph work and parameter size both matter',
                  font_size=21, color=YES),
            label(r"\textbf{Buss's kernel}: \ a vertex of degree $> k$ must be in the cover; \ after removing them, "
                  r"more than $k^2$ edges means no", font_size=21, color=DATA),
            label('kernel theorem: $O(k^2)$ edges; this teaching implementation repeatedly scans edges', font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.22).next_to(tl, DOWN, buff=0.35)
        with self.voiceover(
            "Parameterized algorithms separate dependence on a small parameter from dependence on the input size. <bookmark mark='a'/> For vertex cover of budget k, choose an uncovered edge. Every valid cover contains at least one endpoint, so branch on the two choices. <bookmark mark='b'/> The search tree has at most two to the k-plus-one minus one nodes. Each node still performs graph work; a small parameter does not by itself promise a practical runtime on arbitrarily large inputs. <bookmark mark='c'/> Buss’s rule forces a vertex whose degree exceeds the remaining budget. After applying it, too many remaining edges certify failure; otherwise an equivalent quadratic-size kernel remains. <bookmark mark='d'/> We retain the complete graph, cover, forced vertices, residual kernel and thirty raw timing intervals. Linear-time kernelization is a theorem about efficient implementations; this teaching routine repeatedly scans its edges."
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
            label('vertex cover is FPT; dated example: $O(1.2738^k+kn)$ (Chen--Kanj--Xia, 2010)', font_size=22,
                  color=YES),
            label('$k$-clique is W[1]-hard; no FPT algorithm unless FPT = W[1]', font_size=22, color=NO),
            label(r"\textbf{treewidth}: \ how tree-like a graph is \ (Robertson and Seymour)", font_size=22,
                  color=DATA),
            label(r"Courcelle \ (1990): \ any property expressible in monadic second-order logic \\ is linear-time on "
                  r"graphs of bounded treewidth", font_size=22, color=HEAD),
            label(r"colouring, \ Hamiltonicity, \ independent set: \ easy on trees, \ series-parallel circuits, \ "
                  r"many real networks", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Fixed-parameter tractability has a precise runtime definition. <bookmark mark='a'/> FPT means time f of k times n to a constant exponent independent of k. <bookmark mark='b'/> Vertex cover is FPT; the displayed one-point-two-seven-three-eight-to-the-k bound is a dated 2010 algorithmic example, not a verified current-record claim. <bookmark mark='c'/> Parameterized clique is W-one-hard. An FPT algorithm would collapse FPT and W-one; this does not rule out every improvement to the naive n-to-the-k enumeration. Stronger exponent barriers require stronger assumptions such as ETH. <bookmark mark='d'/> Treewidth measures how a graph can be decomposed into a tree of small overlapping bags. <bookmark mark='e'/> Courcelle’s theorem gives linear input-size dependence for each fixed monadic-second-order formula and fixed treewidth bound, with parameter-dependent constants and decomposition conditions. <bookmark mark='f'/> Colouring with a fixed palette, Hamiltonicity and independent-set variants illustrate this structural approach. Arbitrary formulas and unbounded treewidth are outside that fixed-parameter statement."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
