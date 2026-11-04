from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, bar_chart, fmt,
                                  load, mono)


class Prefetch(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.measured()

    def card(self):
        card = chapter_card(12, r"Prefetching", r"Can the cache fetch a line before it is asked?", lit=(1995,),
                            extra=((1995, r"stride prefetchers"),), part=PART)
        with self.voiceover("Chapter twelve. Prefetching."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def idea(self):
        head = label(r"Guess the next address, \ fetch it early", font_size=36).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"\textit{next-line}: \ a miss on line $\ell$ also fetches $\ell + 1$", font_size=25, color=DATA),
            label(r"\textit{stride}: \ watch a stream of accesses; \ if it steps by a constant $d$, \ fetch $d$ and "
                  r"$2d$ ahead", font_size=25, color=YES),
            label(r"\textit{software}: \ the program says what it will need \ (\texttt{\_\_builtin\_prefetch})",
                  font_size=25, color=CTRL),
            label(r"the cost of a wrong guess: \ a useful line thrown out, \ bandwidth wasted", font_size=25,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.1)
        with self.voiceover(
            "Chapter seven measured a hundred forty nanoseconds to DRAM, but nine gigabytes a second reading in order. "
            "The difference is prefetching: the cache guessing which line comes next and fetching it before it is "
            "asked for. <bookmark mark='a'/> The simplest rule: on a miss to one line, fetch the next one too. "
            "<bookmark mark='b'/> Better: watch each stream of accesses, and if its addresses step by a constant "
            "stride, fetch one and two strides ahead. Our simulator's prefetcher works this way, per four-kilobyte "
            "page. <bookmark mark='c'/> Or the program can say what it will need, with a prefetch instruction. "
            "<bookmark mark='d'/> A wrong guess costs something: it throws out a line someone wanted and uses "
            "bandwidth for nothing. Real prefetchers are judged on accuracy as well as coverage, much like branch "
            "predictors."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("scancost")["rows"]
        head = label(r"The Job's scan loop on Part 8's core, \ table beyond L2", font_size=32).to_edge(UP, buff=0.35)
        r = d[-1]
        vals = [r["ideal"]["per_entry"], r["hierarchy"]["per_entry"], r["no prefetch"]["per_entry"]]
        ch = bar_chart(vals, [r"perfect memory", r"real memory, \\ prefetching", r"real memory, \\ no prefetching"],
                       [GREY_B, YES, NO], height=3.4, bar_w=1.4, gap=1.4, font_size=22,
                       fmt_=lambda v: f"{v:.2f}").move_to(DOWN * 0.3)
        yl = note(r"cycles per table entry \ (steady state, \ at Pebble's 885 MHz)", font_size=18).next_to(
            ch, UP, buff=0.3).align_to(ch, LEFT)
        cold = label(rf"the first, \ cold pass: \ {r['hierarchy']['cold_pass']:.2f} \ with prefetching, \ "
                     rf"{r['no prefetch']['cold_pass']:.2f} \ without", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is what a stride prefetcher does for the Job's table scan, on Part 8's core, with a table too big for "
            "the second-level cache. <bookmark mark='a'/> With perfect memory, three point one cycles per table "
            "entry. <bookmark mark='b'/> With this machine's memory hierarchy and the prefetcher, also three point one: "
            "the same. The scan reads entry after entry, the easiest pattern there is, and the prefetcher stays "
            "ahead of it. <bookmark mark='c'/> Without the prefetcher, three point five in the steady state. And on "
            "the first, cold pass through the table, when every line must come from DRAM, eight point three cycles "
            "an entry against three point four: two and a half times slower, because every line now waits its full "
            "latency."
        ) as vo:
            self.play(FadeIn(head), FadeIn(yl), FadeIn(ch[0]))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(GrowFromEdge(ch.bars[k], DOWN), FadeIn(ch.vals[k]), FadeIn(ch.names[k]))
            self.play(FadeIn(cold))
        self.wait(0.3)
        self.clear_scene()
