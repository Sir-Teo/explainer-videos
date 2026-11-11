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
            label('nonnegative weights: heaviest first; accept if independence remains', font_size=22,
                  color=GREY_A),
            label('hereditary system: greedy is optimal for every nonnegative weighting $\\Longleftrightarrow$ matroid', font_size=22, color=YES),
            label(r"proof: \ greedy picks $g_1, g_2, \ldots$; \ a best set has $o_1, o_2, \ldots$, \ both heaviest "
                  r"first", font_size=21, color=GREY_A),
            label(r"if $o_i$ were heavier than $g_i$: \ exchange $\{g_1..g_{i-1}\}$ with $\{o_1..o_i\}$ \ gives an "
                  r"$x$ at least as heavy as $o_i$", font_size=21, color=GREY_A),
            label(r"that $x$ could have joined before $g_i$, \ so greedy would have taken it: \ contradiction",
                  font_size=21, color=HEAD),
            label(rf"descending: maximum forest; ascending: minimum Kruskal forest; "
                  rf"{d['forest_ok']} of {d['trials']} random checks optimal", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.24).next_to(head, DOWN, buff=0.5)
        signed = VGroup(MathTex(r"w(e)=-2:\quad w(\{e\})=-2 < w(\varnothing)=0",font_size=27,color=NO),
                        label("signed weights: omit negative elements",font_size=20,color=GREY_A)).arrange(DOWN,buff=.12).to_edge(DOWN,buff=.35)
        with self.voiceover(
            "The greedy theorem needs its weight convention. <bookmark mark='a'/> For nonnegative weights, consider "
            'elements from heaviest to lightest and keep each if independence is preserved. For arbitrary signed '
            "weights, discard negative elements when the goal is any independent set. <bookmark mark='b'/> Among "
            'finite hereditary independence systems, greedy is optimal for every nonnegative weighting exactly when '
            "the system is a matroid. <bookmark mark='c'/> Compare greedy's and an optimum's elements in descending "
            "order. <bookmark mark='d'/> Exchange says that an allegedly heavier next optimum element would have had "
            "an eligible predecessor at least that heavy. <bookmark mark='e'/> Greedy would already have taken it, a "
            "contradiction. <bookmark mark='f'/> On forests, descending order gives a maximum-weight forest. "
            "Kruskal's minimum spanning tree uses ascending order. Our four hundred nonnegative test graphs are "
            'checked by exhaustive enumeration.'
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcdef", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
                if mk == "a": self.play(FadeIn(signed))
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
            label('nonnegative weights: at least half; \\\\ each chosen edge receives at most two charges', font_size=21, color=LAM),
            label(r"exact matching needs more: \\ augmenting paths \ (Part 18; \ Edmonds, \ 1965)", font_size=21,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Matchings show why the exchange axiom matters. <bookmark mark='a'/> Greedy takes the middle edge of "
            "weight three and blocks both neighbors. <bookmark mark='b'/> The two outer edges total four. The smaller"
            ' matching containing the middle edge cannot borrow either edge from the larger matching. <bookmark '
            "mark='c'/> The random-instance success rate and worst ratio shown here describe these four hundred "
            "nonnegative graphs, not a universal distribution. <bookmark mark='d'/> For nonnegative edge weights, "
            'greedy always gets at least half the optimum: charge each rejected optimum edge to a greedy edge at '
            "least as heavy; at most two charges meet one chosen edge. <bookmark mark='e'/> Exact cardinality and "
            'weighted matching need further algorithms; a greedy approximation is not a proof of optimality.'
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
