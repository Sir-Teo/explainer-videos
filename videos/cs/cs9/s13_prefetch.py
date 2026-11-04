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
        self.software()

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

    def software(self):
        d = load("swprefetch")
        head = label(r"Software prefetch: \ a cautionary measurement", font_size=34).to_edge(UP, buff=0.4)
        code = VGroup(mono("for (i = 0; i < n; i++) {", 20),
                      mono("    __builtin_prefetch(&a[idx[i + 16]]);   // ask early", 20, color=HEAD),
                      mono("    sum += a[idx[i]];                      // random lines of 256 MB", 20),
                      mono("}", 20)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(UP * 1.0)
        res = VGroup(
            label(rf"16 million random lookups: \ {d['plain']:.2f} s plain, \ {d['prefetch']:.2f} s with the prefetch",
                  font_size=26, color=NO),
            label(r"the out-of-order core already had a dozen independent misses in flight: \ the prefetches only "
                  r"added work", font_size=24, color=GREY_A),
            label(r"prefetch by hand only after measuring: \ it pays for pointer chains, \ not for independent loads",
                  font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Programs can prefetch for themselves, too. Here a loop sums sixteen million randomly chosen elements of a "
            "two-hundred-fifty-six-megabyte array. The addresses are random, but known in advance, so the loop can ask "
            "for the element sixteen iterations ahead. <bookmark mark='a'/> On this machine it made the loop slower: "
            "point four eight seconds against point four three. <bookmark mark='b'/> The reason is Part 8's core. The "
            "lookups do not depend on each other, so the out-of-order window already had a dozen misses in flight; "
            "the prefetch instructions found nothing left to hide, and only added work. <bookmark mark='c'/> Software "
            "prefetch pays where the core cannot look ahead, as in a chain of pointers, and only measurement tells "
            "which case you are in."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            for mk, r in zip("abc", res):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
