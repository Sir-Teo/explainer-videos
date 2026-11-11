from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, draw_graph, grid_table,
                                   load, mono, words)

POS = {"s": (-6.2, 0.0), "a": (-4.4, 1.5), "b": (-4.4, -1.5), "c": (-2.1, 1.5), "d": (-2.1, -1.5), "t": (-0.3, 0.0)}


class Flow(VoiceoverScene):
    def construct(self):
        self.card()
        self.augment()
        self.theorem()
        self.bad()

    def card(self):
        card = chapter_card(11, r"Flows and cuts", r"How much can get through?", lit=(1956,),
                            extra=((1956, r"Ford and Fulkerson"), (1972, r"Edmonds and Karp")), part=PART)
        with self.voiceover("Chapter eleven. Flows and cuts."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def network(self, d):
        cap = d["cap"]
        edges = [(u, v) for u in cap for v in cap[u]]
        w = {(u, v): cap[u][v] for u, v in edges}
        return draw_graph(POS, edges, directed=True, weights=w)

    def augment(self):
        d = load("flow")
        head = label(r"Push flow along augmenting paths", font_size=34).to_edge(UP, buff=0.3)
        g, nodes, es = self.network(d)
        flow_lab = mono("flow = 0", 26, YES).move_to([3.2, 2.2, 0])
        pts = VGroup(
            label(r"each pipe has a \textbf{capacity}; \\ send as much as possible from $s$ to $t$", font_size=21,
                  color=GREY_A),
            label(r"find a path with room on every edge, \\ push its bottleneck, \ repeat", font_size=21,
                  color=GREY_A),
            label(r"the \textbf{residual graph} \\ lets later paths undo earlier pushes", font_size=21, color=HEAD),
            label(r"Edmonds and Karp \ (1972): \\ always the \textbf{shortest} path: \ $O(VE^2)$", font_size=21,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.7)
        if pts.width > 6.0:
            pts.scale_to_fit_width(6.0).to_edge(RIGHT, buff=0.4)
        # A separate unit-capacity edge makes cancellation concrete without altering the network above.
        forward = Arrow([-5.3,-2.45,0],[-1.6,-2.45,0],buff=.18,color=GREY_D,stroke_width=2)
        backward = Arrow([-1.6,-2.95,0],[-5.3,-2.95,0],buff=.18,color=HEAD,stroke_width=3)
        residual = VGroup(
            forward,backward,
            mono('u',18,WHITE).move_to([-5.6,-2.7,0]),mono('v',18,WHITE).move_to([-1.3,-2.7,0]),
            label(r"forward residual: $c-f=0$",font_size=18,color=GREY_A).move_to([-3.45,-2.15,0]),
            label(r"reverse residual: $f=1$; cancel a previous unit",font_size=18,color=HEAD).move_to([-3.45,-3.25,0]),
            label(r"separate unit-edge example: $c=1$, $f=1$",font_size=17,color=GREY_B).move_to([-3.45,-3.65,0]),
        )
        cols = [YES, LAM, CTRL, DATA, HEAD]
        with self.voiceover(
            "A flow network is a graph of pipes, each with a capacity. <bookmark mark='a'/> The question is how much "
            "can flow from a source s to a sink t, with nothing lost along the way. <bookmark mark='b'/> Lester Ford "
            "and Delbert Fulkerson's method, from 1956: find any path from s to t with spare capacity on every "
            "pipe, push as much as its narrowest pipe allows, and repeat. <bookmark mark='c'/> The subtle part is "
            "the residual graph. Pushing flow along a pipe also creates the option of pushing it back, so a later "
            "path may cancel an earlier choice. <bookmark mark='d'/> Jack Edmonds and Richard Karp showed that "
            "always choosing a shortest path, by breadth-first search, bounds the number of rounds. Here four "
            "augmenting paths bring the flow to nineteen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(flow_lab))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]),FadeIn(residual))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
            total = 0
            for (path, b), col in zip(d["paths"], cols):
                total += b
                segs = []
                for u, v in zip(path, path[1:]):
                    if (u, v) in es:
                        segs.append(es[(u, v)].copy().set_color(col).set_stroke(width=5))
                self.play(*[ShowPassingFlash(s, time_width=0.6) for s in segs], run_time=1.0)
                self.play(Transform(flow_lab, mono(f"flow = {total}", 24, YES).move_to(flow_lab)), run_time=0.4)
        self.wait(0.3)
        self.clear_scene()

    def theorem(self):
        d = load("flow")
        head = label(r"Max flow $=$ min cut", font_size=34).to_edge(UP, buff=0.3)
        g, nodes, es = self.network(d)
        side = set(d["side"])
        for k, n in nodes.items():
            n[0].set_fill(YES if k in side else LAM, 0.35)
        cutset = [(u, v) for u, v, _ in d["cut"]]
        steps = VGroup(
            label(r"a \textbf{cut} splits the vertices, \ $s$ on one side, \ $t$ on the other; \\ its capacity is "
                  r"what crosses forward", font_size=20, color=GREY_A),
            label(r"every flow must cross every cut: \\ flow $\le$ capacity of any cut", font_size=20, color=GREY_A),
            label(r"when no augmenting path is left, \\ the vertices reachable from $s$ in the residual graph \\ form a "
                  r"cut whose edges are all full", font_size=20, color=YES),
            label(rf"so that flow equals that cut: \ here {d['flow']} \ $=$ \ " + r" \ $+$ \ ".join(
                f"{c}" for _, _, c in d["cut"]), font_size=22, color=HEAD),
            label(r"the \textbf{max-flow min-cut theorem} \\ (Ford and Fulkerson; \ Elias, \ Feinstein and Shannon; "
                  r"\ 1956)", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if steps.width > 6.2:
            steps.scale_to_fit_width(6.2).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "A flow and a cut can certify each other's optimality. <bookmark mark='a'/> A cut puts source"
            " s on one side and sink t on the other; add capacities of original arcs directed across it "
            "from the source side. <bookmark mark='b'/> Flow conservation makes the net flow crossing any"
            " cut equal the source value, so that value cannot exceed cut capacity. <bookmark mark='c'/> "
            "When the residual graph has no augmenting path, let S be its vertices reachable from s. "
            "Every original arc leaving S is saturated, and any positive flow entering S would create a "
            "residual arc leaving S, so no such return flow remains. <bookmark mark='d'/> Thus flow "
            "equals cut capacity. Here both are nineteen: ten from s to a, plus nine from b to d. Our "
            "output checks capacity constraints, conservation and this equality. <bookmark mark='e'/> "
            "That is the max-flow min-cut certificate, rather than an inference from the picture alone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), *[es[e].animate.set_color(NO).set_stroke(width=5) for e in cutset if e in es])
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.wait(0.3)
        self.clear_scene()

    def bad(self):
        d = load("flow")
        head = label(r"Why the choice of path matters", font_size=34).to_edge(UP, buff=0.3)
        pos = {"s": (-5.8, 0.0), "a": (-3.6, 1.6), "b": (-3.6, -1.6), "t": (-1.4, 0.0)}
        w = {("s", "a"): 1000, ("s", "b"): 1000, ("a", "b"): 1, ("a", "t"): 1000, ("b", "t"): 1000}
        g, nodes, es = draw_graph(pos, list(w), directed=True, weights=w)
        pts = VGroup(
            label(r"unlucky paths zig-zag through the middle edge: \\ one unit at a time", font_size=21,
                  color=GREY_A),
            label(rf"an unlucky choice: \ {words(d['bad_ff'])} augmentations", font_size=23, color=NO),
            label(rf"shortest paths \ (Edmonds--Karp): \ {d['bad_ek']}", font_size=23, color=YES),
            label(rf"a random network of {d['big_n']} vertices and {d['big_m']} pipes: \\ flow {d['big_flow']}, \ "
                  rf"{d['big_aug']} augmentations", font_size=20, color=GREY_B),
            label(r"push--relabel \ (Goldberg and Tarjan, \ 1988) \\ and, \ since 2022, \ almost-linear time \ "
                  r"(chapter 16)", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.5)
        if pts.width > 6.4:
            pts.scale_to_fit_width(6.4).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "An augmenting-path rule affects the amount of work. <bookmark mark='a'/> This network "
            "carries two thousand units, but alternating zig-zag paths through its unit-capacity middle "
            "edge add only one unit each. A backward residual arc cancels previous flow; it is not a new "
            "original pipe. <bookmark mark='b'/> That prescribed unlucky sequence takes two thousand "
            "augmentations. Integer capacities ensure progress in integral units; arbitrary irrational "
            "capacities do not give the same termination guarantee for arbitrary path choices. <bookmark "
            "mark='c'/> Breadth-first augmenting paths take two on this example. <bookmark mark='d'/> The"
            " random sixty-vertex example separately reports its actual distinct directed arcs, not the "
            "number of attempted dictionary writes, and has a checked flow/cut certificate. <bookmark "
            "mark='e'/> The research chapter will distinguish almost-linear theoretical bounds from "
            "practical implementations."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
