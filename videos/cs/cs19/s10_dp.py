from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Dp(VoiceoverScene):
    def construct(self):
        self.card()
        self.name()
        self.fib()
        self.dag()

    def card(self):
        card = chapter_card(9, r"Dynamic programming", r"What if the subproblems overlap?", lit=(1957,),
                            extra=((1957, r"Bellman's book"),), part=PART)
        with self.voiceover("Chapter nine. Dynamic programming."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def name(self):
        head = label(r"A name chosen to hide the mathematics", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"Richard Bellman, \ RAND Corporation, \ 1950s: \ the theory of multistage decisions",
                  font_size=22, color=GREY_A),
            label(r"his funding ran through the Air Force; \ the Secretary of Defense, \ Charles Wilson, \\ by "
                  r"Bellman's account hated the word \textit{research}", font_size=21, color=GREY_A),
            label(r"\textit{programming}: \ planning, \ as in a military programme; \ \textit{dynamic}: \ "
                  r"impossible to use as an insult", font_size=22, color=HEAD),
            label(r"the idea: \ an optimal plan is built from optimal plans for smaller stages", font_size=23,
                  color=YES),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.7)
        with self.voiceover(
            "The name is a piece of camouflage. <bookmark mark='a'/> In the 1950s Richard Bellman worked at the "
            "RAND Corporation on decisions taken in many stages. <bookmark mark='b'/> RAND was funded through the "
            "Air Force, and according to Bellman's autobiography the Secretary of Defense, Charles Wilson, had a "
            "horror of the word research, let alone mathematical. <bookmark mark='c'/> So Bellman chose "
            "programming, which then meant planning, as in a training programme, and dynamic, because, he wrote, "
            "it is impossible to use the word dynamic in a pejorative sense. <bookmark mark='d'/> The idea behind "
            "the name: an optimal plan is made of optimal plans for smaller problems, so solve the smaller "
            "problems first and remember the answers."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def fib(self):
        d = load("fib")
        head = label(r"Overlapping subproblems", font_size=34).to_edge(UP, buff=0.3)
        # the call tree of fib(5)
        nodes, edges = VGroup(), VGroup()
        pos = {}

        def place(k, x, y, w, path):
            pos[path] = (x, y, k)
            if k >= 2:
                place(k - 1, x - w, y - 0.85, w / 2, path + "L")
                place(k - 2, x + w, y - 0.85, w / 2, path + "R")
        place(5, -2.6, 2.1, 1.9, "")
        cols = {5: WHITE, 4: DATA, 3: YES, 2: HEAD, 1: LAM, 0: GREY_B}
        for path, (x, y, k) in pos.items():
            nodes.add(VGroup(Circle(radius=0.2, color=cols[k], fill_color=BG, fill_opacity=1, stroke_width=2),
                             mono(str(k), 15, cols[k])).move_to([x, y, 0]))
            if path:
                px, py, _ = pos[path[:-1]]
                edges.add(Line([px, py, 0], [x, y, 0], color=GREY_D, stroke_width=1.5).set_z_index(-1))
        lab = label(r"$F(5)$: \ 15 calls; \ $F(3)$ is computed twice, \ $F(2)$ three times", font_size=20,
                    color=GREY_A).next_to(VGroup(nodes, edges), DOWN, buff=0.25)
        rows = [[str(r["n"]), f"{r['naive_calls']:,}", str(r["memo_calls"])] for r in d["rows"]]
        tab = grid_table([r"$n$", r"plain recursion", r"remembering"], rows, widths=[1.0, 2.6, 2.2], row_h=0.44,
                         font_size=20, colors=[[WHITE, NO, YES]] * len(rows)).to_edge(RIGHT, buff=0.5).shift(UP * 1.4)
        pts = VGroup(
            label('call count grows as $\\Theta(\\varphi^n)$; answer bit length grows as $\\Theta(n)$', font_size=20, color=NO),
            label(r"\textbf{memoization}: \ cache each answer, \ top-down", font_size=20, color=YES),
            label(r"\textbf{tabulation}: \ fill a table bottom-up, \ in dependency order", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(tab, DOWN, buff=0.4).align_to(tab, LEFT)
        with self.voiceover(
            "Fibonacci exposes repeated work. <bookmark mark='a'/> In the tree for F of five, the same smaller "
            "arguments recur on several branches. <bookmark mark='b'/> Naive recursion's call count grows "
            "exponentially; the exact count for F of thirty is shown in the table. <bookmark mark='c'/> Memoization "
            'keeps the first result for each argument. The counter includes calls that hit the cache, so F of thirty '
            "uses fifty-nine calls, not thirty arithmetic additions. <bookmark mark='d'/> Tabulation visits states "
            'from small to large and can retain only the last two values. Linear arithmetic work here assumes unit-'
            'cost addition; exact Fibonacci values grow in bit length.'
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(edges), LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.06), run_time=3)
            self.play(FadeIn(lab))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def dag(self):
        head = label('Dependencies: choice or combination', font_size=34).to_edge(UP, buff=0.3)
        n = 7
        xs = [-5.6 + 1.6 * i for i in range(n)]
        nodes = VGroup(*[VGroup(Circle(radius=0.28, color=DATA, stroke_width=2, fill_color=BG, fill_opacity=1),
                                MathTex(rf"F_{i}", font_size=26)).move_to([x, 0.8, 0]) for i, x in enumerate(xs)])
        arcs = VGroup()
        for i in range(2, n):
            arcs.add(CurvedArrow(nodes[i - 1].get_top() + UP * 0.02, nodes[i].get_top() + UP * 0.02, angle=-0.9,
                                 color=GREY_B, stroke_width=1.6, tip_length=0.12))
            arcs.add(CurvedArrow(nodes[i - 2].get_bottom() + DOWN * 0.02, nodes[i].get_bottom() + DOWN * 0.02,
                                 angle=0.8, color=GREY_B, stroke_width=1.6, tip_length=0.12))
        pts = VGroup(
            label(r"subproblems are vertices, \ dependencies are edges: \ a directed acyclic graph", font_size=22,
                  color=GREY_A),
            label(r"tabulation visits it in topological order \ (Part 18, \ chapter 4)", font_size=22, color=YES),
            label('min/max-plus choice can describe a path; Fibonacci sums both predecessors',
                  font_size=22, color=HEAD),
            label('total work $=\\sum_s$ transition work at state $s$', font_size=23, color=LAM),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        combine=MathTex(r"F_5=F_3+F_4=2+3=5",font_size=32,color=HEAD).move_to([0,-.45,0])
        with self.voiceover(
            "A well-founded recurrence has a dependency graph. <bookmark mark='a'/> Draw edges from already smaller "
            'states to the states that use them. The state definition, such as an explicit stage index, makes this '
            "expanded graph acyclic even when the original problem has cycles. <bookmark mark='b'/> Tabulation "
            "evaluates it in topological order. <bookmark mark='c'/> Min-plus or max-plus recurrences with one "
            'predecessor choice describe shortest or longest paths. Fibonacci adds two answers, and tree knapsack can'
            ' combine several child answers; those dependencies are not automatically a single-path problem. '
            "<bookmark mark='d'/> Count work by summing the transition cost over all states. A uniform upper bound "
            'can be states times work per state; selecting a sufficient, compact state is the art.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes))
            vo.wait_until("a")
            self.play(Create(arcs), FadeIn(pts[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(pts[1]), LaggedStart(*[Indicate(nd, color=YES) for nd in nodes], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]),FadeIn(combine),Indicate(nodes[3],color=HEAD),Indicate(nodes[4],color=HEAD))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()
