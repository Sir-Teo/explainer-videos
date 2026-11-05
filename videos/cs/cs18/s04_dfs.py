from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, draw_graph, load,
                                   mono, words)

POS = {"a": (-5.2, 1.4), "b": (-3.6, 1.4), "c": (-4.4, 0.0), "d": (-5.2, -1.4), "e": (-3.0, -0.4), "f": (-2.0, -1.6),
       "g": (-1.2, 0.6), "h": (-0.2, 1.6)}


class Dfs(VoiceoverScene):
    def construct(self):
        self.card()
        self.times()
        self.parentheses()
        self.classes()

    def card(self):
        card = chapter_card(3, r"Depth-first search", r"What does a thread through a maze remember?", lit=(1972,),
                            extra=((1882, r"Tr\'emaux: \ maze solving"), (1972, r"Tarjan: \ DFS and its uses")),
                            part=PART)
        with self.voiceover("Chapter three. Depth-first search."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def graph(self):
        d = load("dfs")
        edges = [(u, v) for u, vs in d["graph"].items() for v in vs]
        return draw_graph(POS, edges, directed=True, color=DATA)

    def times(self):
        d = load("dfs")
        head = label(r"Go deep, \ then back up", font_size=34).to_edge(UP, buff=0.3)
        g, nodes, es = self.graph()
        order = sorted(d["d"], key=lambda k: d["d"][k])
        side = {"d": LEFT, "e": RIGHT, "c": LEFT, "f": RIGHT}
        tlab = {k: mono(f"{d['d'][k]}/{d['f'][k]}", 16, HEAD).next_to(nodes[k], side.get(k, UP), buff=0.08)
                for k in nodes}
        pts = VGroup(
            label(r"follow an unexplored edge as far as it goes; \\ when stuck, \ back up one step", font_size=21,
                  color=GREY_A),
            label(r"a stack, \ or recursion, \ instead of BFS's queue", font_size=21, color=GREY_A),
            label(r"stamp each vertex twice: \ \textbf{discovered} on arrival, \\ \textbf{finished} on leaving",
                  font_size=21, color=HEAD),
            label(r"Tr\'emaux \ (1882): \ the thread through the labyrinth; \\ Hopcroft and Tarjan \ (1973): \ its "
                  r"uses", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.4)
        if pts.width > 6.2:
            pts.scale_to_fit_width(6.2).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Depth-first search is the other way to explore. <bookmark mark='a'/> Follow an unexplored edge, and "
            "from there another, as far as possible; when every edge out of the current vertex has been tried, back "
            "up one step and continue. <bookmark mark='b'/> It uses a stack, or plain recursion, where breadth-first "
            "search used a queue. It is the thread Theseus unwound in the labyrinth, and Charles Trémaux wrote it "
            "down for mazes in 1882. <bookmark mark='c'/> The useful trick is to stamp each vertex twice with a "
            "clock: once when it is first discovered, once when it is finished. <bookmark mark='d'/> John Hopcroft "
            "and Robert Tarjan showed in the early 1970s how much structure those two numbers reveal, and won the "
            "Turing award for it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            for k in order:
                self.play(nodes[k][0].animate.set_fill(DATA, 0.5), FadeIn(tlab[k]), run_time=0.4)
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def parentheses(self):
        d = load("dfs")
        head = label(r"The parenthesis theorem", font_size=34).to_edge(UP, buff=0.3)
        T = max(d["f"].values())
        x0, W = -6.0, 12.0
        bars = VGroup()
        order = sorted(d["d"], key=lambda k: d["d"][k])
        depth = {}
        for k in order:
            dd, ff = d["d"][k], d["f"][k]
            lev = sum(1 for j in order if d["d"][j] < dd and d["f"][j] > ff)
            depth[k] = lev
            a, b = x0 + W * (dd - 0.5) / T, x0 + W * (ff - 0.5) / T
            r = Rectangle(width=b - a, height=0.36, stroke_width=1.5, stroke_color=DATA, fill_color=DATA,
                          fill_opacity=0.25).move_to([(a + b) / 2, 1.4 - lev * 0.5, 0])
            bars.add(VGroup(r, mono(k, 18, WHITE).move_to(r)))
        ticks = VGroup(*[mono(str(t), 13, GREY_B).move_to([x0 + W * (t - 0.5) / T, 2.1, 0]) for t in range(1, T + 1)])
        pts = VGroup(
            label(r"for any two vertices, \ their intervals $[d, f]$ are \textbf{nested or disjoint}, \ never "
                  r"overlapping", font_size=22, color=YES),
            label(r"nested \ $\iff$ \ one is a descendant of the other in the DFS forest", font_size=22, color=GREY_A),
            label(r"\textbf{white-path theorem}: \ $v$ descends from $u$ \ $\iff$ \ when $u$ is discovered, \ a path "
                  r"of undiscovered vertices leads to $v$", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Draw each vertex's lifetime, from discovery to finish, as an interval on the clock. <bookmark "
            "mark='a'/> Any two intervals are either nested or disjoint; they never partly overlap, just like "
            "matched parentheses. That is because the search finishes a vertex only after finishing everything "
            "discovered from it. <bookmark mark='b'/> Nesting means ancestry: one interval inside another means "
            "one vertex is a descendant of the other in the search tree. <bookmark mark='c'/> And the white-path "
            "theorem says exactly which vertices end up as descendants: those reachable, at the moment of "
            "discovery, along a path of vertices not yet discovered."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ticks))
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in bars], lag_ratio=0.2), run_time=2.5)
            for mk, p in zip("abc", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def classes(self):
        d = load("dfs")
        head = label(r"Four kinds of edge", font_size=34).to_edge(UP, buff=0.3)
        g, nodes, es = self.graph()
        colours = {"tree": YES, "back": NO, "forward": LAM, "cross": GREY_C}
        anims = []
        for key, c in d["classes"].items():
            u, v = key.split("->")
            if (u, v) in es:
                anims.append(es[(u, v)].animate.set_color(colours[c]).set_stroke(width=4 if c != "cross" else 2))
        leg = VGroup(
            label(r"\textbf{tree}: \ discovered a new vertex", font_size=21, color=YES),
            label(r"\textbf{back}: \ to an ancestor still open: \ \textbf{a cycle}", font_size=21, color=NO),
            label(r"\textbf{forward}: \ to a finished descendant", font_size=21, color=LAM),
            label(r"\textbf{cross}: \ to a finished vertex elsewhere", font_size=21, color=GREY_C),
            label(r"a directed graph has a cycle \ $\iff$ \\ DFS finds a back edge", font_size=22, color=HEAD),
            label(r"all in $O(V + E)$: \\ the next two chapters are built on these stamps", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "The stamps also sort every edge into one of four kinds. <bookmark mark='a'/> Tree edges are the ones "
            "the search followed to discover a new vertex. <bookmark mark='b'/> Back edges lead to an ancestor that "
            "is still open, and each one closes a cycle. <bookmark mark='c'/> Forward edges jump to a descendant "
            "already finished, and cross edges go sideways, to a finished vertex in another branch. <bookmark "
            "mark='d'/> The most useful consequence: a directed graph contains a cycle exactly when the search finds "
            "a back edge. <bookmark mark='e'/> Everything happens in linear time, and the next two chapters are "
            "built on these stamps."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(*anims, FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(FadeIn(leg[2:4]))
            vo.wait_until("d")
            self.play(FadeIn(leg[4]))
            vo.wait_until("e")
            self.play(FadeIn(leg[5]))
        self.wait(0.3)
        self.clear_scene()
