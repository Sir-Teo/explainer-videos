from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.dijkstra()
        self.barrier()
        self.flow()
        self.open_()

    def card(self):
        card = chapter_card(16, r"Frontier: \ shortest paths and flows, \ now", r"Was Dijkstra the end of the story?",
                            lit=(2024,), extra=((2022, r"almost-linear max flow"), (2024, r"universal optimality"),
                                                (2025, r"the sorting barrier broken")), part=PART)
        with self.voiceover("Chapter sixteen. Frontier: shortest paths and flows, now."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def dijkstra(self):
        head = label(r"Dijkstra is universally optimal \ (2024)", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"Dijkstra with a heap also \textbf{sorts} the vertices by distance", font_size=22, color=GREY_A),
            label(r"worst-case optimal for that task: \ sorting needs $\Omega(n \log n)$ \ (Part 16)", font_size=22,
                  color=GREY_A),
            label(r"\textbf{universally optimal}: \ on \textit{every} graph, \ within a constant of the best algorithm "
                  r"for that graph's worst weights", font_size=22, color=YES),
            label(r"needs a new heap with the \textbf{working-set} property: \ cheap to extract recently inserted "
                  r"items \ (callback: \ splay trees)", font_size=21, color=LAM),
            label(r"Haeupler, \ Hlad\'ik, \ Rozho\v{n}, \ Tarjan and T\v{e}tek \ (FOCS 2024, \ best paper)",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Sixty-eight years after it was designed, Dijkstra's algorithm has had a remarkable few years. "
            "<bookmark mark='a'/> When it runs with a heap it does more than find distances: it outputs the "
            "vertices sorted by distance. <bookmark mark='b'/> For that task it is worst-case optimal, since sorting "
            "needs n log n comparisons, as Part 16 proved. <bookmark mark='c'/> In 2024, Bernhard Haeupler, Richard "
            "Hladík, Václav Rozhoň, Robert Tarjan and Jakub Tětek proved much more: with the right heap it is "
            "universally optimal, within a constant factor of the best possible algorithm on every graph, not just "
            "the worst one. <bookmark mark='d'/> The right heap has the working-set property, extracting recently "
            "inserted items cheaply, the same idea that made Part 17's splay trees adapt. <bookmark mark='e'/> The "
            "paper won the best paper award at FOCS that year."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()

    def barrier(self):
        head = label(r"Breaking the sorting barrier \ (2025)", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"if you only want the distances, \ not the sorted order, \ must you pay $n \log n$?", font_size=22,
                  color=GREY_A),
            MathTex(r"O\bigl(m \log^{2/3} n\bigr) \text{ for directed graphs, \ comparison-addition model}",
                    font_size=32, color=YES),
            label(r"Duan, \ Mao, \ Mao, \ Shu and Yin \ (STOC 2025, \ best paper): \ the first algorithm to beat "
                  r"Dijkstra on sparse directed graphs", font_size=21, color=HEAD),
            label(r"the idea: \ shrink the frontier by a few Bellman--Ford rounds, \ so that only some vertices need "
                  r"sorting", font_size=21, color=GREY_A),
            label(r"negative weights too: \ near-linear time \ (Bernstein, \ Nanongkai and Wulff-Nilsen, \ 2022)",
                  font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "That optimality is about sorting. <bookmark mark='a'/> If you want only the distances, not the vertices "
            "in order, must you still pay the cost of sorting? <bookmark mark='b'/> In 2025 the answer turned out to "
            "be no. <bookmark mark='c'/> Ran Duan, Jiayi Mao, Xiao Mao, Xinkai Shu and Longhui Yin gave an algorithm "
            "for directed graphs that runs in m times log n to the two thirds, the first to beat Dijkstra's bound on "
            "sparse directed graphs in the model where weights may only be compared and added. It won the best "
            "paper award at STOC. <bookmark mark='d'/> Its idea mixes the two classics of this part: a few rounds "
            "of Bellman–Ford relaxation shrink the frontier, so that only a fraction of the vertices ever has to be "
            "sorted. <bookmark mark='e'/> And for negative weights, Aaron Bernstein, Danupon Nanongkai and Christian "
            "Wulff-Nilsen found a near-linear algorithm in 2022, replacing Bellman–Ford's V times E."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()

    def flow(self):
        head = label(r"Maximum flow in almost linear time \ (2022)", font_size=34).to_edge(UP, buff=0.3)
        rows = [
            [r"Ford and Fulkerson", r"1956", r"$O(E \cdot |f|)$"],
            [r"Edmonds and Karp", r"1972", r"$O(VE^2)$"],
            [r"Goldberg and Tarjan, \ push--relabel", r"1988", r"$O(VE \log(V^2/E))$"],
            [r"Goldberg and Rao", r"1998", r"$\tilde O(E \min(V^{2/3}, E^{1/2}) \log U)$"],
            [r"Chen, \ Kyng, \ Liu, \ Peng, \ Probst Gutenberg and Sachdeva", r"2022", r"$E^{1 + o(1)}$"],
        ]
        tab = grid_table([r"", r"year", r"time"], rows, widths=[6.4, 1.4, 4.4], row_h=0.56, font_size=21,
                         mono_cols=(), colors=[[GREY_A, GREY_B, GREY_A]] * 4 + [[YES, YES, YES]]).next_to(
            head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"the method: \ interior-point optimization \ (Part 23) \ with dynamic graph data structures "
                  r"that update in $m^{o(1)}$ time", font_size=21, color=GREY_A),
            label(r"almost linear: \ max flow is now essentially as cheap as reading the graph", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Flows had their own breakthrough. <bookmark mark='a'/> For sixty years the bounds crept down, from "
            "Ford and Fulkerson through Edmonds and Karp, push–relabel, and Andrew Goldberg and Satish Rao. In 2022 "
            "Li Chen, Rasmus Kyng, Yang Liu, Richard Peng, Maximilian Probst Gutenberg and Sushant Sachdeva "
            "solved maximum flow in almost linear time, m to the one plus little o of one. <bookmark mark='b'/> "
            "Their method treats flow as continuous optimization, the interior-point methods of Part 23, and "
            "keeps each step cheap with dynamic data structures that update in sub-polynomial time. <bookmark "
            "mark='c'/> Maximum flow, and with it matching and minimum cut, is now essentially as cheap as reading "
            "the graph, although the constants are still far from practical."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open questions", font_size=36).to_edge(UP, buff=0.35)
        qs = VGroup(
            label(r"single-source shortest paths in $O(m)$ on directed graphs with real weights?", font_size=24,
                  color=GREY_A),
            label(r"a \textit{practical} almost-linear max-flow algorithm?", font_size=24, color=GREY_A),
            label(r"all-pairs shortest paths in $O(n^{3 - \varepsilon})$, \ or a proof that it needs $n^{3 - o(1)}$?",
                  font_size=24, color=GREY_A),
            label(r"exact TSP faster than $2^n$, \ for general weights?", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        star = label(r"$\bigstar$ \ the part's research problem takes the first one", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is where the field stands. <bookmark mark='a'/> Can single-source shortest paths on a directed "
            "graph with real weights be computed in linear time? Thorup did it for undirected graphs with integer "
            "weights in 1999. <bookmark mark='b'/> Can the almost-linear flow algorithm be made practical? <bookmark "
            "mark='c'/> Can all-pairs shortest paths beat cubic time by a polynomial factor, or is the APSP "
            "conjecture right that they cannot? <bookmark mark='d'/> And can the travelling salesman be solved exactly in less than two to the n "
            "time? <bookmark mark='e'/> This part's research problem takes up the first."
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abcd", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
