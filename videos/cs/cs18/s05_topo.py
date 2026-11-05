from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, draw_graph, load,
                                   mono, words)

POS = {"lexer.c": (-5.6, 2.0), "parser.c": (-5.6, 0.8), "ast.h": (-5.6, -0.4), "codegen.c": (-5.6, -1.6),
       "lexer.o": (-2.9, 2.0), "parser.o": (-2.9, 0.8), "codegen.o": (-2.9, -1.6), "pebblec": (-0.3, 0.4),
       "tests": (1.9, 0.4)}


class Topo(VoiceoverScene):
    def construct(self):
        self.card()
        self.build()
        self.kahn()
        self.uses()

    def card(self):
        card = chapter_card(4, r"Topological sort", r"In what order can dependent tasks run?", lit=(1962,),
                            extra=((1962, r"Kahn: \ topological sorting"), (1977, r"make")), part=PART)
        with self.voiceover("Chapter four. Topological sort."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def dag(self):
        d = load("topo")
        nodes, edges = {}, VGroup()
        for k, (x, y) in POS.items():
            r = RoundedRectangle(width=1.7, height=0.5, corner_radius=0.1, stroke_color=DATA, stroke_width=1.8,
                                 fill_color=BG, fill_opacity=1).move_to([x, y, 0])
            nodes[k] = VGroup(r, mono(k, 16, CODE).move_to(r))
        es = {}
        for u, vs in d["dag"].items():
            for v in vs:
                a = Arrow(nodes[u].get_right(), nodes[v].get_left(), buff=0.05, stroke_width=1.8, color=GREY_B,
                          max_tip_length_to_length_ratio=0.08)
                es[(u, v)] = a
                edges.add(a)
        return VGroup(edges, *nodes.values()), nodes, es

    def build(self):
        d = load("topo")
        head = label(r"A build is a directed acyclic graph", font_size=34).to_edge(UP, buff=0.3)
        g, nodes, es = self.dag()
        order = VGroup(*[mono(k, 16, YES) for k in d["dfs"]]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        ol = label(r"by DFS finish time, \\ latest first", font_size=19, color=GREY_B).next_to(order, UP, buff=0.2)
        VGroup(ol, order).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)
        pts = VGroup(
            label(r"an edge $u \to v$: \ $u$ must be built before $v$", font_size=21, color=GREY_A),
            label(r"a \textbf{topological order} lists every vertex after all its prerequisites", font_size=21,
                  color=YES),
            label(r"DFS gives one: \ sort by finish time, \ decreasing: \ every edge points from a later finish to "
                  r"an earlier one", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is the build of a small compiler. <bookmark mark='a'/> Each arrow says that one file must be made "
            "before another: the header before every object file that includes it, the object files before the "
            "linked compiler, the compiler before the tests. <bookmark mark='b'/> A topological order is a list in "
            "which every file comes after all of its prerequisites; it exists exactly when there are no cycles. "
            "<bookmark mark='c'/> Depth-first search finds one for free. Sort the vertices by finishing time, latest "
            "first. Along any edge, the search finishes the target before the source, because the target is either "
            "explored from the source or already done; a back edge would be a cycle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]), FadeIn(ol), LaggedStart(*[FadeIn(o) for o in order], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()

    def kahn(self):
        d = load("topo")
        head = label(r"Kahn's algorithm \ (1962)", font_size=34).to_edge(UP, buff=0.3)
        g, nodes, es = self.dag()
        steps = VGroup(
            label(r"count each vertex's incoming edges", font_size=21, color=GREY_A),
            label(r"repeatedly take a vertex with none left, \ output it, \ and delete its edges", font_size=21,
                  color=GREY_A),
            label(r"if vertices remain but none is free, \ they lie on a \textbf{cycle}", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        out = VGroup()
        outl = label(r"output", font_size=19, color=GREY_B).move_to([5.6, 2.3, 0])
        with self.voiceover(
            "Arthur Kahn's method from 1962 is the one build tools usually use. <bookmark mark='a'/> Count the "
            "incoming edges of every vertex. <bookmark mark='b'/> Any vertex with none can be built now: output it "
            "and remove its outgoing edges, which may free others. The vertices that become free at the same moment "
            "do not depend on each other, so they can be built in parallel. <bookmark mark='c'/> If at some point "
            "vertices remain but none is free, the remaining ones contain a cycle, and the build is impossible: "
            "make reports a circular dependency."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            self.play(FadeIn(outl))
            for i, k in enumerate(d["kahn"]):
                outs = [es[(k, v)] for v in d["dag"][k]]
                o = mono(k, 16, YES).move_to([5.6, 1.9 - 0.3 * i, 0])
                out.add(o)
                self.play(nodes[k][0].animate.set_fill(YES, 0.45), *[FadeOut(e) for e in outs],
                          FadeIn(o, shift=RIGHT * 0.2), run_time=0.45)
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
        self.wait(0.3)
        self.clear_scene()

    def uses(self):
        head = label(r"Orders everywhere", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup(*[label(t, font_size=23, color=c) for t, c in (
            (r"\texttt{make}, \ Bazel, \ \texttt{cargo}: \ build order, \ and what can run in parallel", DATA),
            (r"spreadsheets: \ recompute cells after the cells they refer to", YES),
            (r"Part 13's compiler: \ basic blocks in reverse postorder for data-flow analysis", LAM),
            (r"package managers: \ install dependencies first; \ report cycles", CTRL),
            (r"course prerequisites, \ task scheduling, \ neural networks' forward pass", GREY_A),
            (r"the longest path in a DAG \ = \ the critical path: \ the least time with unlimited workers", HEAD),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Topological order is one of the most used algorithms in software. <bookmark mark='a'/> Build systems "
            "use it to order compilation and to find what can run in parallel. Spreadsheets use it to recompute "
            "cells after the cells they depend on. Part 13's compiler visited basic blocks in reverse postorder, "
            "which is a topological order of the control-flow graph without its back edges. Package managers "
            "install dependencies first and refuse cycles. <bookmark mark='b'/> And on a directed acyclic graph, "
            "even the longest path is easy: in topological order, one pass finds the critical path, the least "
            "time a project can take with unlimited workers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:5]], lag_ratio=0.4), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(rows[5]))
        self.wait(0.3)
        self.clear_scene()
