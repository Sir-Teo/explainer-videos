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
            label('mismatched-length fast path: 6 instructions, 7 cycles; \\\\ warm correct predictions; equal-length entries do more work', font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Look closely at the Job's search loop. <bookmark mark='a'/> The displayed mismatched-length fast path has "
            "six instructions. Loading the entry length immediately before testing it causes one load-use bubble. "
            "Equal-length entries can enter the letter-comparison path and do more work. <bookmark mark='b'/> With "
            "warm, correct direction and target predictions, the jump back adds no modeled redirect cost. <bookmark "
            "mark='c'/> On that fast path, six instructions then take seven steady-state cycles. The larger "
            "ninety-nine point seven percent figure covers the whole search in the single-cycle instruction count, not "
            "only this path. Scheduling an independent, safe instruction between the load and use can hide the bubble; "
            "moving a load past a bounds check first needs an address-safety proof."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pc.heads), FadeIn(VGroup(*pc.rows.values())))
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
        head = label(r"Projected thirty-novel run: \ ledger row 1", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"the bubbles depend on the same events as the instructions \ (words, \ entries scanned, \ \ldots): "
                  r"\\ fit them on 24 passages, \ check on one four times longer", font_size=22, color=GREY_A),
            label(rf"the check: \ {fmt(ck['bubbles'])} bubbles measured, \ {fmt(ck['predicted'])} predicted \ "
                  rf"({100 * ck['error']:+.1f}\%)", font_size=22, color=YES),
            label(rf"projected corpus: \ CPI {co['cpi']:.3f}, \ ${sci(co['cycles'], 4)}$ cycles at {st['mhz']:.0f} MHz",
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
            "The full-corpus pipeline row is a projection. <bookmark mark='a'/> Fit a linear bubble model to "
            "twenty-four short passages, using text events such as scanned entries. This is different from Part 6's "
            "instruction path-count formula. <bookmark mark='b'/> The displayed sixteen-thousand-character heldout "
            'text, encoded as sixteen thousand and nineteen bytes, checks one prediction and reports its error. It '
            "does not establish an error bound for the thirty novels. <bookmark mark='c'/> Combining the fitted "
            'bubbles with the corpus instruction count and assumed eight-hundred-and-eighty-five-megahertz clock gives '
            'the displayed CPI and projected minutes. We have not simulated the entire corpus cycle by cycle. '
            "<bookmark mark='d'/> The ledger's speedup is therefore a model-based estimate for the same program. A "
            'full run or broader validation could reveal a different result.'
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), FadeIn(led.axis), LaggedStart(*[FadeIn(r) for r in led.rows], lag_ratio=0.1))
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()
