from __future__ import annotations

import math
import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, code, grid_table, load, mono,
                                   words)


class Walks(WatchScene):
    def construct(self):
        self.card()
        self.two_sat()
        self.ruin()

    def card(self):
        self.chapter(6, r"Random walks that solve SAT", r"Can a drunkard find a satisfying assignment?", lit=(1991, 1999), extra=((1991, r"Papadimitriou's walk"), (1999, r"Sch\"oning's walk")), part=PART, said='Chapter six. Random walks that solve SAT.')

    def two_sat(self):
        self.ask(r"A random walk for 2-SAT: \\ flip a variable of a failing clause. Expected steps?",
                 [r"about $n$", r"$O(n^2)$", r"$2^n$"], 1,
                 say="For two-SAT, flip a random variable of any failing clause. How many flips, on average, to find a "
                     "solution?",
                 reveal="Order n squared: a gambler's walk towards the answer.")
        head = label(r"A walk for 2-SAT", font_size=34).to_edge(UP, buff=0.35)
        cl = MathTex(r"(x_1 \lor \lnot x_2)", r"\land", r"(x_2 \lor x_3)", r"\land", r"(\lnot x_1 \lor \lnot x_3)",
                     r"\land", r"(x_2 \lor \lnot x_4)", r"\land \cdots", font_size=32).next_to(head, DOWN, buff=0.45)
        for i in (0, 2, 4, 6):
            cl[i].set_color(DATA)
        algo = code([
            "start from any assignment",
            "repeat:",
            "    if every clause holds: done",
            "    pick any clause that fails",
            "    flip one of its two variables, at random",
        ], size=22).next_to(cl, DOWN, buff=0.5)
        note_ = label(r"Part 18 solved 2-SAT exactly with strongly connected components; \ this walk uses no "
                      r"structure at all", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            (
            'A 2-SAT formula is an and of clauses, each an or of two literals. Part 18 solved it exactly, with '
            "strongly connected components of the implication graph. <bookmark mark='a'/> Christos Papadimitriou "
            'analyzed a much dumber method in 1991. Start anywhere. While some clause fails, pick one, and flip one '
            "of its two variables, chosen by a coin. <bookmark mark='b'/> It uses no structure at all. Why should it"
            ' ever finish?'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(algo))
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def ruin(self):
        head = label(r"Distance to a solution, \ as a walk on a line", font_size=34).to_edge(UP, buff=0.35)
        n = 12
        line = NumberLine(x_range=[0, n, 1], length=11.0, include_numbers=True, font_size=22, color=GREY_B)
        line.move_to(UP * 0.6)
        zero = label(r"solved", font_size=20, color=YES).next_to(line.n2p(0), DOWN, buff=0.55)
        wall = label(r"wall", font_size=20, color=GREY_A).next_to(line.n2p(n), DOWN, buff=0.55)
        facts = VGroup(
            label(r"fix a satisfying assignment $x^*$; \ $D$ = the number of variables where we differ from it",
                  font_size=21, color=WHITE),
            label(r"a failing clause has a literal where we differ from $x^*$; \ flipping it: $D - 1$", font_size=21,
                  color=WHITE),
            MathTex(r"\Pr[D \to D - 1] \ge \tfrac12", font_size=34, color=YES),
            label(r"gambler's ruin, \ with a wall at $n$: \ expected time to reach 0 from $D$ is $\le D(2n - D) \le "
                  r"n^2$", font_size=21, color=LAM),
            label(r"so: \ run $2n^2$ steps; \ by Markov, \ if satisfiable, \ we fail with probability $\le \tfrac12$",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.35)
        rng = random.Random(3)
        path = [8]
        while path[-1] > 0 and len(path) < 200:
            x = path[-1]
            step = -1 if (x == n or rng.random() < 0.5) else 1
            path.append(x + step)
        tok = Dot(line.n2p(path[0]), radius=0.15, color=HEAD)
        distance_path = VMobject().set_points_as_corners([line.n2p(x) for x in path])
        trace_curve = VMobject(color=LAM, stroke_width=2).set_points_as_corners(
            [[-5.5 + 11*i/(len(path)-1), -0.4 + 0.55*x/n, 0] for i,x in enumerate(path)])
        trace_base = Line([-5.5,-0.4,0],[5.5,-0.4,0],color=GREY_D,stroke_width=1)
        trace_note = label(rf"same {len(path)-1} flips; \ curve: distance versus flip number; \ compressed in time",
                           font_size=16,color=GREY_A).move_to(DOWN*0.68)
        with self.voiceover(
            (
            f'Fix one satisfying assignment, x star, and let D be the number of variables where our assignment '
            f"differs from it. <bookmark mark='a'/> A clause that fails has both its literals false, but x star makes"
            f' at least one of them true, so we disagree with x star on at least one of the two variables. <bookmark '
            f"mark='b'/> Flipping a random one of the two moves D one step closer to zero with probability at least a"
            f" half. <bookmark mark='c'/> So D does a random walk on the line from zero to n, pushed toward zero at "
            f"least as often as away. This is the gambler's ruin. From any start, the expected time to reach zero is "
            f"at most n squared. <bookmark mark='d'/> Here is one walk, starting eight steps away. It took "
            f'{len(path) - 1}'
            f" flips. We may even stop sooner, at some other solution. <bookmark mark='e'/> So run two n squared "
            f"steps. If the formula is satisfiable, Markov's inequality says we fail with probability at most a half,"
            f' and repetition does the rest. The bound is for the worst formula: on random satisfiable ones, with up '
            f'to three hundred and twenty variables, the walk needed only about two flips per variable.'
        )
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(zero), FadeIn(wall))
            self.play(FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(FadeIn(facts[1]))
            vo.wait_until("b")
            self.play(FadeIn(facts[2]))
            vo.wait_until("c")
            self.play(FadeIn(facts[3]))
            vo.wait_until("d")
            self.play(FadeIn(tok), Create(trace_base), FadeIn(trace_note), run_time=0.4)
            cue_budget = max(0.2, vo.until("e", minimum=0) - 0.7)
            self.play(MoveAlongPath(tok, distance_path), Create(trace_curve),
                      run_time=min(7.0, cue_budget), rate_func=linear)
            self.play(Flash(tok, color=YES), run_time=0.5)
            vo.wait_until("e")
            self.play(FadeIn(facts[4]))
        self.wait(0.3)
        self.clear_scene()

