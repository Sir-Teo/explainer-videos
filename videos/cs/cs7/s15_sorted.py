from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt,
                                  load, mono)


class Sorted(VoiceoverScene):
    def construct(self):
        self.card()
        self.puzzle()
        self.host()
        self.pebble()
        self.branchless()

    def card(self):
        card = chapter_card(14, r"The sorted-array puzzle", r"Why does sorting the data make a loop faster?",
                            lit=(2012,), extra=((2012, r"the sorted-array question"),), part=PART)
        with self.voiceover("Chapter fourteen. The sorted-array puzzle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def puzzle(self):
        head = label(r"The same loop, \ the same data, \ in a different order", font_size=34).to_edge(UP, buff=0.35)
        code = VGroup(*[mono(t, 22) for t in ("for (i = 0; i < n; i++)", "    if (data[i] >= 128)",
                                              "        sum += data[i];")]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        code.move_to(UP * 2.0)
        rng = np.random.default_rng(2)
        vals = rng.integers(0, 256, 40)
        def strip(v, y):
            return VGroup(*[Rectangle(width=0.2, height=0.05 + 1.0 * x / 255, stroke_width=0,
                                      fill_color=YES if x >= 128 else GREY_C, fill_opacity=0.8).move_to(
                [-4.3 + 0.22 * k, y + (0.05 + 1.0 * x / 255) / 2, 0]) for k, x in enumerate(v)])
        a = strip(vals, -0.55)
        b = strip(np.sort(vals), -2.55)
        la = label('fixed-seed irregular order: difficult for these predictors', font_size=22, color=NO).next_to(a, DOWN, buff=0.15)
        lb = label(r"sorted: \ not taken, \ then taken, \ for good", font_size=22, color=YES).next_to(b, DOWN,
                                                                                                buff=0.15)
        so = label('Stack Overflow, 2012: a widely discussed performance question', font_size=20, color=HIST).next_to(
            code, DOWN, buff=0.35)
        with self.voiceover(
            "A widely discussed 2012 Stack Overflow question asked why sorting an array sped up this loop. <bookmark "
            "mark='a'/> The loop adds values at least a hundred and twenty-eight. Reordering the same values preserves "
            "the sum and the number of additions; sorting itself has a cost, excluded from these repeated-loop "
            "timings. <bookmark mark='b'/> Fixed-seed pseudorandom data makes the threshold outcomes irregular for "
            "these predictors. That is an empirical difficulty, not an absolute information bound for a known repeated "
            "array. <bookmark mark='c'/> Sorted data groups outcomes into long runs, which even a two-bit counter "
            "predicts well. Compiler transformations and the target processor determine the actual speedup."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code), FadeIn(so))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in a], lag_ratio=0.02), FadeIn(la), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in b], lag_ratio=0.02), FadeIn(lb), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def host(self):
        h = load("sorted")["host"]
        head = label(r"Measured on the machine that made this video", font_size=34).to_edge(UP, buff=0.35)
        cpu = label(rf"{h['cpu']}; \ C; \ {h['n']:,} values $\times$ {h['reps']} passes".replace(",", "{,}"),
                    font_size=20, color=GREY_B).next_to(head, DOWN, buff=0.2)
        items = [("random", h["random"], NO), ("sorted", h["sorted"], YES)]
        scale = 7.0 / max(v for _, v, _ in items)
        bars = VGroup()
        for k, (n, v, c) in enumerate(items):
            y = 0.7 - 1.1 * k
            r = Rectangle(width=v * scale, height=0.6, stroke_width=0, fill_color=c, fill_opacity=0.65).move_to(
                [-3.2 + v * scale / 2, y, 0])
            nl = label(n, font_size=24, color=c).next_to(r, LEFT, buff=0.2).align_to([-3.4, 0, 0], RIGHT)
            vl = label(rf"{v * 1e3:.1f} ms", font_size=22, color=GREY_A).next_to(r, RIGHT, buff=0.15)
            bars.add(VGroup(nl, r, vl))
        res = VGroup(
            label(rf"{h['ratio']:.1f} times faster, \ sorted", font_size=32, color=HEAD),
            label('five-run medians; generation and sorting excluded; \\\\ timing alone does not isolate branch-prediction effects', font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "These bars are measurements from this host, not the original question's machine. <bookmark mark='a'/> The "
            "program scans thirty-two thousand seven hundred and sixty-eight values three hundred times, reusing the "
            "same array. We report medians of five runs, check matching sums, and exclude generation and sorting. C "
            "compiler flags disable vectorization and automatic if-conversion. <bookmark mark='b'/> Read the measured "
            "times and ratio from the bars. The sorted loop is faster here, consistent with easier branch prediction, "
            "but timing alone does not isolate its cause. Hardware performance counters and controlled compiler output "
            "would strengthen that explanation. Other processors and builds can give different results."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cpu))
            vo.wait_until("a")
            for b in bars:
                self.play(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pebble(self):
        p = load("sorted")["pebble"]
        head = label(r"And on Pebble's pipeline", font_size=36).to_edge(UP, buff=0.35)
        rows = VGroup()
        for k, n in enumerate(("random", "sorted")):
            v = p[n]
            rows.add(label(rf"{n}: \ {fmt(v['cycles'])} cycles, \ CPI {v['cpi']:.2f}, \ {fmt(v['mispredicts'])} "
                           rf"mispredictions", font_size=26, color=NO if k == 0 else YES))
        rows.arrange(DOWN, buff=0.35).move_to(UP * 0.8)
        ratio = p["random"]["cycles"] / p["sorted"]["cycles"]
        res = VGroup(
            label(rf"only {ratio:.2f} times faster: \ a mistake costs Pebble 2 cycles, \ not 20", font_size=26,
                  color=HEAD),
            label(r"the deeper and wider the machine, \ the more a predictable branch is worth", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 1.3)
        with self.voiceover(
            "Now use Pebble's cycle model with three thousand values scanned twice. <bookmark mark='a'/> The irregular "
            "order has about three thousand mispredictions; the sorted order has fourteen. Both produce the same sum. "
            "<bookmark mark='b'/> Each modeled branch miss costs two cycles. The displayed cycle counts therefore "
            "differ by only about thirteen percent. This compares two input orders within Pebble, not an identical "
            "prediction stream across different processors. Deeper or wider machines can lose more useful work on a "
            "redirect, but their predictors, caches and generated code also differ."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def branchless(self):
        h = load("sorted")["host"]
        p = load("sorted")["pebble"]
        head = label(r"No branch, \ no misprediction", font_size=36).to_edge(UP, buff=0.35)
        code = VGroup(mono("sltiu t3, t2, 128     # 1 if small", 20), mono("addi  t3, t3, -1      # all ones if big",
                                                                            20),
                      mono("and   t3, t3, t2", 20), mono("add   a0, a0, t3      # adds x, or 0", 20)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(UP * 1.5)
        res = VGroup(
            label(rf"this machine: \ {h['random_branchless'] * 1e3:.1f} ms random, \ {h['sorted_branchless'] * 1e3:.1f} ms "
                  r"sorted: \ little order difference in this run", font_size=24, color=YES),
            label(rf"Pebble: \ {fmt(p['random, branchless']['cycles'])} cycles either way: \ more instructions, \ and "
                  r"its cheap mistakes were worth less", font_size=24, color=GREY_A),
            label(r"compilers emit conditional moves \ (\texttt{cmov}); \ databases, \ video codecs \ and trading "
                  r"systems \\ write branch-free inner loops on purpose", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.28).move_to(DOWN * 1.2)
        with self.voiceover(
            "A data-dependent branch can sometimes be replaced by arithmetic. <bookmark mark='a'/> Here the comparison "
            "is x less than a hundred and twenty-eight. Subtract one from its zero-or-one result: small values get a "
            "zero mask; large ones get all ones in the machine word. Masking x selects zero or x before adding. "
            "<bookmark mark='b'/> The displayed host and Pebble timings show the trade-off. The host's order "
            "sensitivity is much smaller; Pebble executes more instructions and is slower than its branched versions. "
            "These are measured cases, not a rule that branchless code wins. <bookmark mark='c'/> Compilers may use "
            "conditional moves or vectorization when semantics permit. Extra work, dependencies and safely evaluating "
            "both paths still matter."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(c) for c in code], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]))
            vo.wait_until("c")
            self.play(FadeIn(res[2]))
        self.wait(0.3)
        self.clear_scene()
