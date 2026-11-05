from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, big, load, mono, words)


class Hook(VoiceoverScene):
    def construct(self):
        self.ledger()
        self.quadratic()
        self.preview()
        self.plan()

    def ledger(self):
        d = load("hook")
        led = d["ledger"]
        head = label(r"Seven rows of better machines", font_size=36).to_edge(UP, buff=0.35)
        rows = led + [{"part": 16, "label": r"sort, then count"}, {"part": 17, "label": r"a hash table"}]
        tab = ledger_table(rows, shown=len(led), font_size=21, row_h=0.42, label_width=4.8).move_to(DOWN * 0.3)
        best = min(r["seconds"] for r in led)
        cap = label(rf"the best so far: \ {human_time(best)} \ (four cores, \ Part 10)", font_size=23,
                    color=COST).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "This is the ledger: the cost of counting the words of thirty novels, row by row. <bookmark mark='a'/> "
            "Act Two made the machine faster: a pipeline, an out-of-order core, caches, four cores. Act Three made it "
            "easier to program: a compiler, a type system, a runtime, each at some cost. <bookmark mark='b'/> The "
            "best row so far is twelve seconds, on four cores. Every one of these rows ran the same algorithm. "
            "Act Four asks a different question: can thinking beat silicon?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.15), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def quadratic(self):
        d = load("hook")
        g = d["growth"]
        head = label(r"The Job v0 is quadratic", font_size=36).to_edge(UP, buff=0.35)
        xs = [np.log10(r["bytes"]) for r in g]
        ys = [np.log10(r["per_byte"]) for r in g]
        ax = Axes(x_range=[3.8, 7.6, 1], y_range=[1.5, 4.0, 0.5], x_length=7.0, y_length=4.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to(LEFT * 2.2 + DOWN * 0.4)
        pts = [ax.c2p(x, y) for x, y in zip(xs, ys)]
        line = VMobject(color=NO, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.06, color=NO) for p in pts])
        xt = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(ax.c2p(v, 1.5), DOWN, buff=0.1)
                      for v, t in ((4, r"10 kB"), (5, r"100 kB"), (6, r"1 MB"), (7, r"10 MB"))])
        yt = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(ax.c2p(3.8, v), LEFT, buff=0.1)
                      for v, t in ((2, r"100"), (3, r"1,000"), (4, r"10,000"))])
        xl = label(r"text so far", font_size=18, color=GREY_B).next_to(xt, DOWN, buff=0.15)
        yl = label(r"cycles per byte", font_size=18, color=GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        last = g[-1]
        side = VGroup(
            label(r"each new word is looked for in the list of words seen so far", font_size=21, color=GREY_A),
            label(rf"all thirty novels: \ {words(last['words'])} words, \ {words(last['distinct'])} distinct",
                  font_size=21, color=GREY_A),
            label(r"the cost per byte keeps growing: \ the work grows faster than the text", font_size=21,
                  color=NO),
            label(r"no hardware fixes that: \ a faster machine only moves the line down", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        if side.width > 5.2:
            side.scale_to_fit_width(5.2)
        with self.voiceover(
            "Here is why the algorithm matters. <bookmark mark='a'/> The Job v0 keeps the words it has seen in a "
            "list, and for every new word it searches the list from the front. <bookmark mark='b'/> On ten "
            "kilobytes of text it costs about three hundred cycles per byte. On the whole corpus, over four thousand. The "
            "cost per byte keeps rising, because the list keeps growing: the total work grows roughly like the "
            "number of words times the number of distinct words. <bookmark mark='c'/> A faster machine moves this "
            "line down. It cannot make it flat. Only a different algorithm can, and this part builds the tools to "
            "say exactly how much better one is."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[:2]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(dots), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def preview(self):
        head = label(r"By the end of this part", font_size=40).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"how to count steps, \ and which steps to count", font_size=27, color=DATA),
            label(r"recursion trees, \ and the master theorem that sums them", font_size=27, color=LAM),
            label(r"why no comparison sort can beat $n \log_2 n$: \ a bound from information", font_size=27,
                  color=YES),
            label(r"quicksort's average, \ $2n \ln n$, \ derived, \ and how rarely it strays", font_size=27,
                  color=CTRL),
            label(r"the Job sorted: \ ledger row 7", font_size=27, color=COST),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is where we are going. <bookmark mark='a'/> How to count the steps of an algorithm, and which "
            "steps to count. <bookmark mark='b'/> Recursion trees, and the master theorem that adds them up. "
            "<bookmark mark='c'/> A proof that no algorithm that sorts by comparing can beat n log n, a bound that "
            "comes from information. <bookmark mark='d'/> Quicksort's average cost, two n natural log n, derived "
            "from one clever observation, and a measurement of how rarely it strays from it. <bookmark mark='e'/> "
            "And the Job, sorted instead of searched: ledger row seven."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcde", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Counting Steps", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"models of computation; \ asymptotic notation",
            r"insertion, \ merge and heap sort; \ recursion trees; \ the master theorem",
            r"the comparison lower bound; \ merge insertion",
            r"quicksort's expected cost and its concentration",
            r"linear-time sorting; \ selection in linear time",
            r"generating functions; \ amortized analysis; \ sorting in practice",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 16 of Computer Science, Built: Counting Steps, the first part of Act Four, Algorithms. <bookmark "
            "mark='a'/> In this part: models of computation and asymptotic notation; insertion, merge and heap "
            "sort, recursion trees and the master theorem; the comparison lower bound; quicksort, its average and "
            "its concentration; sorting in linear time and selecting in linear time; generating functions, "
            "amortized analysis, and how sorting is really done."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
