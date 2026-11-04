from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, PipeChart,
                                  box, fmt, load, mono, sci)

PART_COLORS = {"base": GREY_B, "load-use": FUNC, "data (no forwarding)": INF, "branches": NO, "jumps": HEAD,
               "divide": CTRL}


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.inner()
        self.breakdown()
        self.corpus()

    def card(self):
        card = chapter_card(11, r"The Job on the pipeline", r"Where do the Job's cycles go now?", part=PART)
        with self.voiceover("Chapter eleven. The Job on the pipeline."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def inner(self):
        d = load("charts")["scan"]
        head = label(r"The search loop, \ cycle by cycle", font_size=36).to_edge(UP, buff=0.3)
        pc = PipeChart(d, cw=0.34, ch=0.34, font_size=10, label_size=14, label_width=2.8, max_rows=16).move_to(
            UP * 0.4)
        notes = VGroup(
            label(r"\texttt{lw t1, 4(t0)} \ then \ \texttt{bne t1, a1, next}: \ a load-use stall on every table entry",
                  font_size=22, color=FUNC),
            label(r"the jump back, \ \texttt{jal zero, scan}: \ free, \ from the branch target buffer", font_size=22,
                  color=YES),
            label(r"so 6 instructions take 7 cycles per entry: \ CPI $\approx 1.17$ in the loop that is 99.7\% of the "
                  r"work", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now the Job. Its time is almost all spent in one loop, the scan of the word table, so look at that loop "
            "on the pipeline. <bookmark mark='a'/> Each table entry costs six instructions. The load of the entry's "
            "length is followed at once by the branch that tests it: a load-use hazard, one bubble on every entry. "
            "<bookmark mark='b'/> The jump back to the top of the loop costs nothing, because the target buffer knows "
            "it, and the loop's branches are well predicted. <bookmark mark='c'/> So six instructions take seven cycles, "
            "a CPI of about one point one seven, in the loop that does ninety-nine point seven percent of the Job's "
            "work. A compiler, or a careful programmer, could hide that bubble by moving one instruction; Part 13 will."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pc.heads), FadeIn(VGroup(*pc.rows.values())))
            vo.wait_until("a")
            for c in range(pc.ncycles):
                if c in pc.columns:
                    self.play(FadeIn(pc.columns[c]), run_time=0.15)
            self.play(FadeIn(notes[0]), *[Indicate(b, color=NO) for b in pc.bubbles])
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def breakdown(self):
        hz = load("hazards")["benchmarks"]["the Job, chapter 1"]
        head = label(r"The Job's CPI, \ piece by piece", font_size=36).to_edge(UP, buff=0.35)
        cfgs = list(hz)
        scale = 3.9
        bars = VGroup()
        keys = ["base", "load-use", "data (no forwarding)", "branches", "jumps", "divide"]
        for k, cname in enumerate(cfgs):
            parts = hz[cname]["parts"]
            y = 1.7 - 1.0 * k
            x = -2.0
            segs = VGroup()
            for key in keys:
                w = parts[key] * scale
                if w < 0.01:
                    continue
                r = Rectangle(width=w, height=0.5, stroke_width=1, stroke_color=BG, fill_color=PART_COLORS[key],
                              fill_opacity=0.7).move_to([x + w / 2, y, 0])
                segs.add(r)
                x += w
            nl = label(cname, font_size=20, color=GREY_A).move_to([-2.2, y, 0], aligned_edge=RIGHT)
            vl = label(rf"{hz[cname]['cpi']:.2f}", font_size=22, color=HEAD).move_to([x + 0.35, y, 0])
            bars.add(VGroup(nl, segs, vl))
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=PART_COLORS[k_], fill_opacity=0.7),
                              label(k_, font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.1)
                       for k_ in keys[:5]]).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The simulator accounts for every cycle, so the Job's CPI on its first chapter can be taken apart. "
            "<bookmark mark='a'/> With no forwarding and no prediction, the CPI is one point nine: the base cycle, plus "
            "waiting for data, plus a flush on every taken branch and jump. <bookmark mark='b'/> Forwarding removes the "
            "data waits except for the load-use bubbles. <bookmark mark='c'/> A target buffer and two-bit counters "
            "remove most of the branch losses. <bookmark mark='d'/> A tournament predictor and a return stack shave "
            "off a little more: a CPI of one point two, three quarters of whose excess is the load-use bubble in the "
            "scan loop, the rest the branches that still go wrong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            for mk, b in zip("abcd", bars):
                vo.wait_until(mk)
                self.play(FadeIn(b[0]), LaggedStart(*[GrowFromEdge(s, LEFT) for s in b[1]], lag_ratio=0.3),
                          FadeIn(b[2]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def corpus(self):
        j = load("job")
        st = load("stages")
        co = j["corpus"]
        ck = j["check"]
        head = label(r"Thirty novels on the pipeline: \ ledger row 1", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"the bubbles depend on the same events as the instructions \ (words, \ entries scanned, \ \ldots): "
                  r"\\ fit them on 24 passages, \ check on one four times longer", font_size=22, color=GREY_A),
            label(rf"the check: \ {fmt(ck['bubbles'])} bubbles measured, \ {fmt(ck['predicted'])} predicted \ "
                  rf"({100 * ck['error']:+.1f}\%)", font_size=22, color=YES),
            label(rf"the corpus: \ CPI {co['cpi']:.3f}, \ ${sci(co['cycles'], 4)}$ cycles at {st['mhz']:.0f} MHz",
                  font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.22).move_to(UP * 1.5)
        rows = j["ledger"] + [{"part": p_, "label": t} for p_, t in ((8, r"out of order, \ four wide"), (9, r"caches"), (10, r"four cores"),
                                                                     (13, r"an optimizing compiler"),
                                                                     (16, r"sort, then count"), (17, r"a hash table"))]
        led = ledger_table(rows, shown=2, highlight=(1,), font_size=21, row_h=0.38, label_width=4.8).move_to(DOWN * 1.5)
        res = label(rf"{human_time(j['ledger'][0]['seconds'])} $\to$ {human_time(co['seconds'])}: \ "
                    rf"{j['speedup']:.2f} times faster, \ for the same program", font_size=26,
                    color=COST).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Simulating thirty novels cycle by cycle would take days, so, as in Part 6, we count instead. "
            "<bookmark mark='a'/> The bubbles, like the instructions, come from events in the text: words, table entries "
            "scanned, entries of the same length. A linear model of the bubbles in terms of those events is fitted on "
            "twenty-four passages and checked on a passage four times longer than any of them. "
            "<bookmark mark='b'/> It predicts that passage's one point three million bubbles to within a fraction of a percent. <bookmark mark='c'/> Applied "
            "to the whole corpus, it gives a CPI just under one point two, and at eight hundred and eighty-five "
            "megahertz the pipeline counts the thirty novels' words in about two and a half minutes, where the "
            "single-cycle Pebble took nearly five. <bookmark mark='d'/> That is the second row of the ledger: almost "
            "twice as fast, for exactly the same program. Better hardware; the same idea."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), FadeIn(led.axis), LaggedStart(*[FadeIn(r) for r in led.rows], lag_ratio=0.1))
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()
