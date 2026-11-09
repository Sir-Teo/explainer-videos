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
        with self.voiceover(
            "Chapter twelve. Prefetching."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def idea(self):
        head = label(r"Guess the next address, \ fetch it early", font_size=36).to_edge(UP, buff=0.4)
        items = VGroup(
            label("\\textit{next-line}: \\ model considers $\\ell+1$ on every demand access", font_size=25, color=DATA),
            label(r"\textit{stride}: \ watch a stream of accesses; \ if it steps by a constant $d$, \ fetch $d$ and "
                  r"$2d$ ahead", font_size=25, color=YES),
            label(r"\textit{software}: \ the program says what it will need \ (\texttt{\_\_builtin\_prefetch})",
                  font_size=25, color=CTRL),
            label(r"the cost of a wrong guess: \ a useful line thrown out, \ bandwidth wasted", font_size=25,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.1)
        with self.voiceover(
            "Prefetching tries to request useful data before a demand needs it. It can help when there is enough "
            "prediction lead time and transfer capacity. <bookmark mark='a'/> A next-line rule considers the "
            "following line; our simulator triggers it on every demand access, not only a miss. <bookmark mark='b'/> "
            "Its stride rule tracks line differences within each four-kibibyte page and immediately inserts "
            "predicted lines. That simplified model charges neither prefetch latency nor bandwidth. <bookmark "
            "mark='c'/> Software can also issue hints for addresses it can compute early. <bookmark mark='d'/> Real "
            "designs must manage accuracy, coverage, timeliness, pollution and metadata cost. The 2026 Streamline "
            "study, for example, organizes temporal-prefetch correlations as streams to use metadata storage more "
            "effectively. Our stride experiment does not reproduce that design or its evaluation."
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

    def measured(self):
        d = load("scancost")["rows"]
        head = label(r"Synthetic scan: \ beyond assigned L2, \ within assigned L3", font_size=32).to_edge(UP, buff=0.35)
        r = d[-1]
        vals = [r["ideal"]["per_entry"], r["hierarchy"]["per_entry"], r["no prefetch"]["per_entry"]]
        ch = bar_chart(vals, ["default load model", "latency model, \\\\ free prefetch", "latency model, \\\\ no prefetch"],
                       [GREY_B, YES, NO], height=3.4, bar_w=1.4, gap=1.4, font_size=22,
                       fmt_=lambda v: f"{v:.2f}").move_to(DOWN * 0.3)
        yl = note(r"cycles/entry: \ (three passes - one pass)/two; \ assumed 885 MHz", font_size=18).next_to(
            ch, UP, buff=0.3).align_to(ch, LEFT)
        cold = label(rf"the first, \ cold pass: \ {r['hierarchy']['cold_pass']:.2f} \ with prefetching, \ "
                     rf"{r['no prefetch']['cold_pass']:.2f} \ without", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Replay a synthetic scan on the functional core, with a table larger than its assigned L2 but still "
            "within the assigned third-level capacity. The hierarchy uses selected host timing proxies at the "
            "assumed Pebble clock. <bookmark mark='a'/> The ideal-memory bar is the core's default load model. "
            "<bookmark mark='b'/> The next bar adds immediate, uncharged stride-prefetch fills. A similar result "
            "therefore shows what these assumptions can hide, not what a finite hardware prefetch engine will always "
            "hide. <bookmark mark='c'/> The third bar disables that prefetch rule. The warm estimate subtracts a "
            "one-pass execution from a three-pass execution and divides by two passes. The cold-pass labels include "
            "initialization and startup effects; not every miss necessarily reaches DRAM. Queuing, bandwidth and "
            "prefetch traffic remain outside this model."
        ) as vo:
            self.play(FadeIn(head), FadeIn(yl), FadeIn(ch[0]))
            for mk, k in zip("abc", range(3)):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(GrowFromEdge(ch.bars[k], DOWN), FadeIn(ch.vals[k]), FadeIn(ch.names[k]))
                if mk == 'a':
                    vo.wait_until(mk)
            self.play(FadeIn(cold))
        self.wait(0.3)
        self.clear_scene()

    def software(self):
        d = load("swprefetch")
        head = label(r"Software prefetch: \ a cautionary measurement", font_size=34).to_edge(UP, buff=0.4)
        code = VGroup(mono("for (i = 0; i < n; i++) {", 20),
                      mono("    if (i + 16 < n) __builtin_prefetch(&a[idx[i + 16]]);", 19, color=HEAD),
                      mono("    sum += a[idx[i]];                      // random lines of 256 MiB", 20),
                      mono("}", 20)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(UP * 1.0)
        res = VGroup(
            label(rf"16 million random lookups: \ {d['plain']:.2f} s plain, \ {d['prefetch']:.2f} s with the prefetch",
                  font_size=26, color=NO),
            label("timings do not count in-flight misses or isolate the cause", font_size=24, color=GREY_A),
            label("lookahead needs known future addresses or independent work; \\ measure the result",
                  font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "This host benchmark sums randomly indexed elements of a two-hundred-fifty-six-mebibyte array. The index "
            "array is available in advance, so the guarded hint can request sixteen iterations ahead without reading "
            "past its end. <bookmark mark='a'/> The displayed values are the best of three trials for each variant. "
            "Whether the hinted version is faster or slower depends on the actual run; the narration does not assume "
            "an old result. <bookmark mark='b'/> Independent accesses may already overlap, but these timings do not "
            "count outstanding misses or isolate the cause of a difference. Instruction overhead, pollution, cache "
            "state and hint timing can matter. <bookmark mark='c'/> A single dependent pointer chain usually cannot "
            "know a distant future address. Useful software lookahead needs available address information, "
            "independent work or a different algorithm; test it under representative conditions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            for mk, r in zip("abc", res):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()
