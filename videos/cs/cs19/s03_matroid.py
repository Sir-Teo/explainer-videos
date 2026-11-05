from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, draw_graph, load,
                                   mono, words)


class Matroid(VoiceoverScene):
    def construct(self):
        self.card()
        self.axioms()
        self.theorem()
        self.matching()

    def card(self):
        card = chapter_card(2, r"When greedy is right: \ matroids", r"What structure makes greedy optimal?",
                            lit=(1971,), extra=((1935, r"Whitney: \ matroids"), (1971, r"Edmonds: \ the greedy "
                                                                                       r"theorem")), part=PART)
        with self.voiceover("Chapter two. When greedy is right: matroids."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def axioms(self):
        head = label(r"Independence, \ abstracted \ (Whitney, \ 1935)", font_size=34).to_edge(UP, buff=0.3)
        ax = VGroup(
            label(r"a ground set $E$, \ and a family of \textbf{independent} subsets:", font_size=23, color=GREY_A),
            label(r"1. \ the empty set is independent", font_size=22, color=GREY_A),
            label(r"2. \ subsets of independent sets are independent", font_size=22, color=GREY_A),
            label(r"3. \ \textbf{exchange}: \ if $|A| < |B|$, \ some $x \in B \setminus A$ keeps $A \cup \{x\}$ "
                  r"independent", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.7)
        ex = VGroup(
            label(r"\textbf{vectors}: \ linearly independent sets \ (where the name comes from)", font_size=21,
                  color=DATA),
            label(r"\textbf{forests}: \ edge sets with no cycle \ (the graphic matroid)", font_size=21, color=HEAD),
            label(r"\textbf{small sets}: \ any $k$ or fewer elements", font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.6).to_edge(LEFT, buff=0.7)
        # forests: a small graph with an independent set growing
        pos = {0: (2.6, 0.6), 1: (4.2, 1.3), 2: (5.8, 0.6), 3: (3.0, -1.0), 4: (5.4, -1.0)}
        E = [(0, 1), (1, 2), (0, 3), (3, 4), (2, 4), (1, 3), (1, 4)]
        g, nodes, es = draw_graph(pos, E, r=0.2, font=14)
        g.shift(DOWN * 0.1)
        A = [(0, 1), (3, 4)]
        B = [(0, 3), (1, 2), (2, 4)]
        with self.voiceover(
            "In 1935 Hassler Whitney noticed that independence behaves the same way in very different places. "
            "<bookmark mark='a'/> Take a ground set and call some of its subsets independent, with three rules. The "
            "empty set is independent. <bookmark mark='b'/> Any subset of an independent set is independent. "
            "<bookmark mark='c'/> And the exchange rule: if one independent set is smaller than another, it can "
            "always borrow some element of the larger one and stay independent. <bookmark mark='d'/> Linearly "
            "independent vectors obey these rules; that is where the name matroid comes from. <bookmark mark='e'/> "
            "So do the edge sets without cycles in a graph. Here the two blue edges form a forest, the three green "
            "edges a larger one, and the blue set can take a green edge without closing a cycle. <bookmark "
            "mark='f'/> And trivially, all sets of at most k elements."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            for mk, a in zip("abc", ax[:2]):
                vo.wait_until(mk)
                self.play(FadeIn(a))
            vo.wait_until("c")
            self.play(FadeIn(ax[2:]))
            vo.wait_until("d")
            self.play(FadeIn(ex[0]))
            vo.wait_until("e")
            self.play(FadeIn(ex[1]), *[es[e].animate.set_color(DATA).set_stroke(width=5) for e in A],
                      *[es[e].animate.set_color(YES).set_stroke(width=5) for e in B])
            self.play(Indicate(es[(1, 2)], color=WHITE))
            vo.wait_until("f")
            self.play(FadeIn(ex[2]))
        self.wait(0.3)
        self.clear_scene()

    def theorem(self):
        d = load("matroid")
        head = label(r"The greedy theorem \ (Rado, \ 1957; \ Edmonds, \ 1971)", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"greedy: \ heaviest element first, \ keep it if the set stays independent", font_size=22,
                  color=GREY_A),
            label(r"\textbf{theorem}: \ greedy finds a heaviest independent set for \textit{every} choice of weights "
                  r"\ $\iff$ \ the structure is a matroid", font_size=22, color=YES),
            label(r"proof: \ greedy picks $g_1, g_2, \ldots$; \ a best set has $o_1, o_2, \ldots$, \ both heaviest "
                  r"first", font_size=21, color=GREY_A),
            label(r"if $o_i$ were heavier than $g_i$: \ exchange $\{g_1..g_{i-1}\}$ with $\{o_1..o_i\}$ \ gives an "
                  r"$x$ at least as heavy as $o_i$", font_size=21, color=GREY_A),
            label(r"that $x$ could have joined before $g_i$, \ so greedy would have taken it: \ contradiction",
                  font_size=21, color=HEAD),
            label(rf"forests are a matroid: \ Kruskal's algorithm \ (Part 18) \ is this greedy; \ "
                  rf"{d['forest_ok']} of {d['trials']} random checks optimal", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.24).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Here is why the definition matters. <bookmark mark='a'/> The greedy algorithm for a weighted set: "
            "consider elements heaviest first, and keep each one if the chosen set stays independent. <bookmark "
            "mark='b'/> Richard Rado in 1957, and Jack Edmonds in 1971, proved that greedy finds a heaviest "
            "independent set for every possible choice of weights exactly when the structure is a matroid. "
            "<bookmark mark='c'/> One direction is short. List greedy's choices and a best set's elements, each "
            "heaviest first. <bookmark mark='d'/> If at some position the best set's element were heavier, apply "
            "the exchange rule to greedy's first i minus one choices and the best set's first i: some element at "
            "least that heavy fits. <bookmark mark='e'/> Then greedy would have reached it before its i-th choice "
            "and taken it, a contradiction. <bookmark mark='f'/> Forests are a matroid, and this greedy is Kruskal's "
            "algorithm from Part 18. On four hundred random graphs, checked by brute force, it was optimal every "
            "time."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcdef", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()

    def matching(self):
        d = load("matroid")
        head = label(r"Matchings are not a matroid", font_size=34).to_edge(UP, buff=0.3)
        pos = {"a": (-5.6, 0.6), "b": (-3.8, 0.6), "c": (-2.0, 0.6), "d": (-0.2, 0.6)}
        w = {("a", "b"): 2, ("b", "c"): 3, ("c", "d"): 2}
        g, nodes, es = draw_graph(pos, list(w), weights=w, r=0.26)
        gl = label(rf"greedy takes the 3: \ total {d['path_greedy']:.0f}", font_size=22, color=NO).move_to([-2.9, -0.5, 0])
        bl = label(rf"best: \ both 2s, \ total {d['path_best']:.0f}", font_size=22, color=YES).next_to(gl, DOWN,
                                                                                                    buff=0.25)
        pts = VGroup(
            label(r"matchings fail the exchange rule: \\ $\{bc\}$ cannot borrow from $\{ab, cd\}$", font_size=21,
                  color=GREY_A),
            label(rf"on {d['trials']} random graphs: \\ greedy matching optimal {d['match_ok']} times, \\ "
                  rf"worst {100 * d['match_worst']:.0f}\% of the best", font_size=21, color=HEAD),
            label(r"never below half: \\ each greedy edge blocks at most two best ones", font_size=21, color=LAM),
            label(r"exact matching needs more: \\ augmenting paths \ (Part 18; \ Edmonds, \ 1965)", font_size=21,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "And when the structure is not a matroid, greedy can be wrong. <bookmark mark='a'/> On this path, "
            "greedy takes the heaviest edge, three, and then nothing else fits. <bookmark mark='b'/> The two edges "
            "of weight two would have made four. Matchings break the exchange rule: the single middle edge cannot "
            "borrow either end edge. <bookmark mark='c'/> On the same four hundred random graphs, greedy matching "
            "was optimal only about three times in five, and once fell to sixty percent of the best. <bookmark "
            "mark='d'/> It is never worse than half, because each edge it takes can block at most two edges of a "
            "best matching. <bookmark mark='e'/> Exact maximum matching needs a cleverer idea, the augmenting paths "
            "of Part 18, which Edmonds also extended to general graphs in 1965."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(es[("b", "c")].animate.set_color(NO).set_stroke(width=6), FadeIn(gl))
            vo.wait_until("b")
            self.play(es[("a", "b")].animate.set_color(YES).set_stroke(width=6),
                      es[("c", "d")].animate.set_color(YES).set_stroke(width=6), FadeIn(bl), FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]))
            vo.wait_until("e")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()
