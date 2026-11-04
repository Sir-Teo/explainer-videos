from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, PipeFigure,
                                  box, fmt, load, mono)


class Hook(VoiceoverScene):
    def construct(self):
        self.waiting()
        self.overlap()
        self.preview()
        self.plan()

    # ------------------------------------------------------------------
    def waiting(self):
        st = load("stages")
        head = label(r"Part 6's machine spends most of each cycle waiting", font_size=34).to_edge(UP, buff=0.4)
        scale = 9.0 / st["single_ps"]
        parts = [(r"fetch: \ instruction memory", 1000, DATA), (r"decode, \ ALU", 560, FUNC),
                 (r"data memory", 1000, INF), (r"", 70, CLOCK)]
        bar = VGroup()
        for t, ps, c in parts:
            r = Rectangle(width=ps * scale, height=0.8, stroke_color=BG, stroke_width=2, fill_color=c, fill_opacity=0.55)
            bar.add(VGroup(r, label(t, font_size=20, color=WHITE).move_to(r)))
        bar.arrange(RIGHT, buff=0).move_to(UP * 1.1)
        bl = label(rf"one clock cycle: \ {fmt(st['single_ps'])} ps", font_size=24, color=GREY_A).next_to(bar, UP,
                                                                                                 buff=0.2)
        uses = VGroup()
        for k, (name, busy) in enumerate(((r"\texttt{lw}", [1, 1, 1]), (r"\texttt{add}", [1, 1, 0]),
                                          (r"\texttt{beq}", [1, 1, 0]))):
            y = -0.4 - 0.7 * k
            lab = label(name, font_size=24, color=CODE).move_to([-5.6, y, 0])
            segs = VGroup()
            x = bar.get_left()[0]
            for (t, ps, c), b in zip(parts[:3], busy):
                w = ps * scale
                segs.add(Rectangle(width=w, height=0.38, stroke_width=0, fill_color=c if b else GREY_D,
                                   fill_opacity=0.6 if b else 0.15).move_to([x + w / 2, y, 0]))
                x += w
            uses.add(VGroup(lab, segs))
        note = label(r"each stage of the machine is busy for a third of the time, \ and idle the rest", font_size=26,
                     color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Part 6 built a computer, and it works. But watch how it spends its time. <bookmark mark='a'/> One clock "
            "cycle must hold everything an instruction might need: fetching it from memory, decoding it and running "
            "the ALU, and reading or writing data memory. With memories that take a nanosecond, that is a cycle of "
            "two point six nanoseconds. <bookmark mark='b'/> A load uses all of it. An add never touches data memory, "
            "and a branch neither, yet each waits out the whole cycle. <bookmark mark='c'/> Worse, at any moment most "
            "of the machine is idle: while the data memory works, the instruction memory and the ALU sit doing "
            "nothing, waiting for the next cycle to begin."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bl), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bar], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(u) for u in uses], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def overlap(self):
        head = label(r"The fix: \ work on five instructions at once", font_size=36).to_edge(UP, buff=0.4)
        fig = PipeFigure(width=12.0, stage_w=1.7, h=1.3).move_to(UP * 0.4)
        names = ["lw  t1, 4(t0)", "bne t1, a1, next", "addi t0, t0, 12", "addi a2, a2, 1", "j   scan",
                 "beq a2, s1, insert", "lw  t1, 4(t0)"]
        cols = [DATA, CTRL, FUNC, INF, YES]
        tokens = []
        with self.voiceover(
            "The cure is the oldest trick in manufacturing. <bookmark mark='a'/> Cut the work into stages, put a "
            "register between each pair, and let a new instruction enter the first stage while the others move on. "
            "Five stages, five instructions in flight, every part of the machine busy in every cycle. "
            "<bookmark mark='b'/> Each instruction still takes five steps from start to finish. But one finishes in "
            "every cycle, and the cycle is now as short as the slowest stage, not the whole journey. This is "
            "pipelining. IBM's Stretch did it in 1961, and nearly every microprocessor since the mid-1980s does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fig))
            vo.wait_until("a")
            live = []
            for k in range(len(names) + 4):
                anims = []
                new_live = []
                for (tk, si, idx) in live:
                    if si + 1 < 5:
                        t2 = fig.token(["IF", "ID", "EX", "MEM", "WB"][si + 1], names[idx], cols[idx % 5])
                        anims.append(Transform(tk, t2))
                        new_live.append((tk, si + 1, idx))
                    else:
                        anims.append(FadeOut(tk))
                if k < len(names):
                    tk = fig.token("IF", names[k], cols[k % 5])
                    anims.append(FadeIn(tk))
                    new_live.append((tk, 0, k))
                live = new_live
                self.play(*anims, run_time=0.7)
                if k == 4:
                    vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def preview(self):
        st = load("stages")
        il = load("ironlaw")
        head = label(r"By the end of this part", font_size=40).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(rf"a five-stage Pebble: \ the clock {st['clock_ratio']:.2f} times faster, \ {st['mhz']:.0f} MHz",
                  font_size=28, color=YES),
            label(r"the price: \ hazards, \ when an instruction needs what another has not finished", font_size=28,
                  color=NO),
            label(r"the hardest: \ branches, \ so the machine guesses, \ and the best guesser is a neural network",
                  font_size=28, color=FUNC),
            label(rf"the Job: \ CPI {il['rows']['pipeline']['cpi']:.2f}, \ {il['speedup']:.2f} times faster than "
                  r"Part 6: \ ledger row 1", font_size=28, color=COST),
        ).arrange(DOWN, buff=0.4).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is where this part goes. <bookmark mark='a'/> A five-stage Pebble, whose clock runs more than twice as "
            "fast as Part 6's. <bookmark mark='b'/> The price is a new class of problems, hazards, which arise when an "
            "instruction needs something an earlier one has not finished. <bookmark mark='c'/> The hardest are "
            "branches: the machine must fetch the next instruction before it knows which one that is, so it guesses, "
            "and the best guessers turn out to be small learning machines, one of them a neural network. "
            "<bookmark mark='d'/> And the Job, measured cycle by cycle, gives the second row of the ledger."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcd", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Pipelines", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"the iron law of performance, \ and why MIPS misleads",
            r"pipelining: \ throughput, \ latency, \ and the best depth, \ derived",
            r"Pebble's five stages, \ built cycle by cycle \ and checked against the emulator",
            r"hazards: \ structural, \ data \ (forwarding), \ control",
            r"branch prediction, \ from counters to TAGE and the perceptron",
            r"the Job's CPI, \ the deep-pipeline era, \ Amdahl's law, \ the sorted-array puzzle",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 7 of Computer Science, Built, the first part of the second act, Making It Fast. "
            "<bookmark mark='a'/> In this part: the iron law of performance, and why counting instructions per second "
            "misleads. Pipelining, its throughput and latency, and the best number of stages, derived. Pebble's five "
            "stages, simulated cycle by cycle and checked against the emulator. The hazards: structural, data, which "
            "forwarding cures, and control. Branch prediction, from two-bit counters to TAGE and the perceptron. Then "
            "the Job's measured CPI, the deep-pipeline era and its end, Amdahl's law, and a famous puzzle about sorted "
            "arrays."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
