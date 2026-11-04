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
        with self.voiceover("Chapter five. Three kinds of miss."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def kinds(self):
        head = label(r"Mark Hill's three Cs \ (1987)", font_size=36).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"\textit{compulsory}: \ the first touch of a line; \ no cache of any size avoids it", font_size=25,
                  color=YES),
            label(r"\textit{capacity}: \ a fully associative LRU cache of the same size misses it too: \ the working set "
                  r"is too big", font_size=25, color=DATA),
            label(r"\textit{conflict}: \ the rest: \ misses caused only by how lines are placed in sets", font_size=25,
                  color=NO),
            label(r"each kind has its own cure: \ bigger lines, \ a bigger cache, \ more ways", font_size=26,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "In 1987 Mark Hill gave every miss one of three names, and each name points to a cure. <bookmark "
            "mark='a'/> A compulsory miss is the first touch of a line: no cache, however big, could have had it. "
            "Bigger lines reduce them, by bringing in more neighbours at once. <bookmark mark='b'/> A capacity miss "
            "is one that a fully associative LRU cache of the same size would also suffer: the working set is simply "
            "bigger than the cache. Only a bigger cache helps. <bookmark mark='c'/> And a conflict miss is everything "
            "else: misses caused only by the restriction on where a line may go. More ways cure them. <bookmark "
            "mark='d'/> Counting the three on a trace tells an architect which cure to buy."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def table(self):
        d = load("threec")["rows"]
        head = label(r"The Job's first chapter, \ by size and ways", font_size=34).to_edge(UP, buff=0.3)
        rows, colors = [], []
        for r in d:
            if r["kb"] not in (1, 4, 8):
                continue
            rows.append([rf"{r['kb']} KB", rf"{r['ways']}", rf"{r['misses']:,}", rf"{r['compulsory']}",
                         rf"{r['capacity']:,}", rf"{r['conflict']:,}"])
            colors.append([WHITE, GREY_B, HEAD, YES, DATA, NO if r["conflict"] > 0 else CTRL])
        t = grid_table([r"size", r"ways", r"misses", r"compulsory", r"capacity", r"conflict"], rows,
                       [1.4, 1.0, 1.8, 2.0, 1.8, 1.8], row_h=0.5, font_size=22, colors=colors, mono_cols=())
        t.move_to(DOWN * 0.2)
        notes = VGroup(
            label(r"8 KB holds every line the chapter touches: \ only the 92 compulsory misses remain \ (with 2 ways)",
                  font_size=22, color=YES),
            label(r"a negative conflict count: \ the set-associative cache beat the fully associative one \ "
                  r"(LRU is not optimal)", font_size=22, color=CTRL),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here are the three Cs for the Job's first chapter, in caches of one, four and eight kilobytes with one, "
            "two and eight ways. <bookmark mark='a'/> The compulsory misses are always ninety-two: the chapter touches "
            "ninety-two lines. At one kilobyte, capacity dominates: the working set does not fit. <bookmark "
            "mark='b'/> At eight kilobytes everything fits, and with two or more ways only the compulsory misses are "
            "left, while the direct-mapped cache still has fifteen thousand conflicts, the table and the letters "
            "colliding. <bookmark mark='c'/> And some conflict counts are negative. That is not an error: a "
            "set-associative LRU cache sometimes beats a fully associative one, because LRU is not the optimal "
            "policy, and splitting the cache into sets happens to protect some lines from the scans. The three Cs are "
            "a guide, not a law."
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
