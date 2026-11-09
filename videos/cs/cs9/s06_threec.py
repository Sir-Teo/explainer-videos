from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, fmt, grid_table,
                                  load)


class ThreeC(VoiceoverScene):
    def construct(self):
        self.card()
        self.kinds()
        self.table()

    def card(self):
        card = chapter_card(5, r"Three kinds of miss", r"Why did that access miss?", lit=(1987,),
                            extra=((1987, r"Hill's three Cs"),), part=PART)
        with self.voiceover(
            "Chapter five. Three kinds of miss."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def kinds(self):
        head = label(r"Mark Hill's three Cs \ (1987)", font_size=36).to_edge(UP, buff=0.4)
        items = VGroup(
            label("first touch: \\ initially empty, \\ fixed line size, \\ no prior prefetch", font_size=25,
                  color=YES),
            label("capacity baseline: \\ repeated misses in same-capacity fully associative LRU", font_size=25, color=DATA),
            label("per-miss conflict test differs from the signed aggregate delta below", font_size=25,
                  color=NO),
            label("delta = target misses minus fully associative LRU reference misses", font_size=26,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Miss categories depend on a reference model. <bookmark mark='a'/> A first reference to a line is "
            "compulsory for an initially empty demand-only cache with this line size; prior prefetching or a "
            "different line size changes the comparison. <bookmark mark='b'/> A fully associative LRU reference of "
            "the same capacity supplies a capacity-miss baseline after first touches. Capacity is one possible "
            "remedy; locality transformations and replacement changes can also help. <bookmark mark='c'/> For an "
            "individual target-cache miss, a hit in that reference suggests a placement conflict. <bookmark "
            "mark='d'/> The numerical table uses a signed aggregate difference instead. That accounting can be "
            "negative, so it must not be presented as a partition of individual misses into three nonnegative "
            "groups."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    def table(self):
        d = load("threec")["rows"]
        head = label(r"The Job's first chapter, \ by size and ways", font_size=34).to_edge(UP, buff=0.3)
        rows, colors = [], []
        for r in d:
            if r["kb"] not in (1, 4, 8):
                continue
            rows.append([rf"{r['kb']} KiB", rf"{r['ways']}", rf"{r['misses']:,}", rf"{r['compulsory']}",
                         rf"{r['capacity']:,}", rf"{r['conflict']:,}"])
            colors.append([WHITE, GREY_B, HEAD, YES, DATA, NO if r["conflict"] > 0 else CTRL])
        t = grid_table([r"size", r"ways", r"misses", r"compulsory", r"FA capacity", r"delta"], rows,
                       [1.4, 1.0, 1.8, 2.0, 1.8, 1.8], row_h=0.5, font_size=22, colors=colors, mono_cols=())
        t.move_to(DOWN * 0.2)
        notes = VGroup(
            label(r"8 KiB holds every line the chapter touches: \ only the 92 compulsory misses remain \ (with 2 ways)",
                  font_size=22, color=YES),
            label("negative delta: \\ target has fewer misses than FA-LRU; \\ not negative miss events", font_size=22, color=CTRL),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The table compares the same chapter trace, line size and cold initial state. <bookmark mark='a'/> "
            "Ninety-two distinct lines give ninety-two first-touch events. The capacity column comes from a fully "
            "associative LRU reference, regardless of the target's number of ways. <bookmark mark='b'/> At eight "
            "kibibytes, the two-way target has only first touches, while the direct-mapped target suffers many "
            "additional misses. <bookmark mark='c'/> The displayed conflict entry is target misses minus first "
            "touches minus reference capacity misses. A negative value means the target had fewer total misses than "
            "the fully associative LRU reference. Set partitioning can protect some lines from scans; this signed "
            "difference is useful comparison accounting, not a negative number of physical miss events."
        ) as vo:
            self.play(FadeIn(head), FadeIn(t))
            vo.wait_until("a")
            self.play(*[Indicate(t.cells[i][3], color=YES) for i in range(1, len(rows) + 1)])
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()
