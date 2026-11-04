from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt, load,
                                  mono)

# reorder-buffer (or equivalent in-flight window) sizes, from the vendors' disclosures and published analyses;
# Apple publishes none, and its figure is measured (Dougall Johnson; AnandTech): treat it as approximate
CORES = [
    ("Pentium Pro", 1995, 40, "Intel", 3),
    ("MIPS R10000", 1996, 32, "MIPS", 4),
    ("Alpha 21264", 1998, 80, "DEC", 4),
    ("Pentium 4", 2000, 126, "Intel", 3),
    ("Core 2", 2006, 96, "Intel", 4),
    ("Sandy Bridge", 2011, 168, "Intel", 4),
    ("Haswell", 2013, 192, "Intel", 4),
    ("Zen", 2017, 192, "AMD", 4),
    ("Skylake", 2015, 224, "Intel", 4),
    ("Sunny Cove", 2019, 352, "Intel", None),
    ("Apple M1 (Firestorm)", 2020, 630, "Apple", 8),
    ("Golden Cove", 2021, 512, "Intel", 6),
    ("Zen 4", 2022, 320, "AMD", None),
    ("Zen 5", 2024, 448, "AMD", None),
]
VENDOR = {"Intel": DATA, "AMD": NO, "Apple": GREY_A, "MIPS": YES, "DEC": CTRL}


class Cores(VoiceoverScene):
    def construct(self):
        self.card()
        self.windows()
        self.widths()
        self.reading()

    def card(self):
        card = chapter_card(13, r"Modern cores in numbers", r"How far have real machines taken all this?",
                            lit=(1995, 2021), extra=((1995, r"Pentium Pro: \ 40"), (2021, r"Golden Cove: \ 512")),
                            part=PART)
        with self.voiceover("Chapter thirteen. Modern cores in numbers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def windows(self):
        head = label(r"Instructions in flight: \ the reorder buffer, \ 1995 to 2024", font_size=32).to_edge(UP,
                                                                                                     buff=0.3)
        ax = Axes(x_range=[1994, 2026, 4], y_range=[0, 700, 100], x_length=10.5, y_length=4.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(DOWN * 0.3)
        ax.x_axis.add_numbers(list(range(1994, 2027, 4)), font_size=16, num_decimal_places=0, group_with_commas=False)
        ax.y_axis.add_numbers(list(range(0, 701, 200)), font_size=16, num_decimal_places=0)
        dots = VGroup()
        for name, yr, rob, v, _ in CORES:
            p = ax.c2p(yr, rob)
            dt = Dot(p, radius=0.08, color=VENDOR[v])
            t = label(rf"{name} \ {rob}" + (r"$^\ast$" if v == "Apple" else ""), font_size=17, color=VENDOR[v])
            side = {"Pentium Pro": UP, "MIPS R10000": DOWN, "Pentium 4": UP, "Sandy Bridge": DOWN, "Haswell": LEFT,
                    "Skylake": UP, "Sunny Cove": LEFT, "Apple M1 (Firestorm)": LEFT, "Golden Cove": LEFT}.get(name, RIGHT)
            t.next_to(dt, side, buff=0.1)
            dots.add(VGroup(dt, t))
        ours = DashedLine(ax.c2p(1994, 128), ax.c2p(2026, 128), color=HEAD, stroke_width=2)
        ol = label(r"our core: \ 128", font_size=18, color=HEAD).next_to(ax.c2p(2026, 128), UP, buff=0.05).shift(
            LEFT * 0.8)
        fn = note(r"$^\ast$ Apple publishes no figure: \ measured by Dougall Johnson and others, \ about 630",
                  font_size=17).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "How far have real machines taken all this? Here is the size of the reorder buffer, the window of "
            "instructions in flight, in cores from 1995 to 2024. <bookmark mark='a'/> Intel's Pentium Pro, the "
            "first mass-market out-of-order x86: forty instructions. The MIPS R10000 and the Alpha 21264, the "
            "great RISC designs of the late 1990s: thirty-two and eighty. <bookmark mark='b'/> Through the 2000s "
            "and 2010s the window grew steadily: about two hundred in Haswell, Skylake and AMD's first Zen. "
            "<bookmark mark='c'/> And then it took off. Intel's Sunny Cove, three hundred fifty-two; Golden Cove, in "
            "2021, five hundred twelve; AMD's Zen 5, four hundred forty-eight. Apple's M1 core of 2020 publishes no "
            "number, but careful measurement puts its window at about six hundred thirty. <bookmark mark='d'/> Our "
            "core's hundred twenty-eight sits in the middle of the history, and we have seen that on the Job even "
            "that is rarely full."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            groups = {"a": [0, 1, 2], "b": [3, 4, 5, 6, 7, 8], "c": [9, 10, 11, 12, 13]}
            for mk, idx in groups.items():
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(dots[i], scale=1.3) for i in idx], lag_ratio=0.2))
            self.play(FadeIn(fn))
            vo.wait_until("d")
            self.play(Create(ours), FadeIn(ol))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def widths(self):
        head = label(r"Why so big?", font_size=38).to_edge(UP, buff=0.35)
        items = VGroup(
            label(r"to cover a cache miss: \ 300 cycles of DRAM \ $\times$ \ 4 to 8 instructions a cycle \ = \ "
                  r"thousands of instructions", font_size=24, color=INF),
            label(r"which only pays if prediction is very good: \ TAGE-class predictors, \ misses in the low "
                  r"single digits per thousand instructions", font_size=24, color=NO),
            label(r"decode: \ 3 wide (Pentium Pro) \ $\to$ \ 4 (Core 2) \ $\to$ \ 6 (Golden Cove) \ $\to$ \ 8 "
                  r"(Apple M1)", font_size=24, color=DATA),
            label(r"the cost: \ these structures are among the largest and hottest on the chip", font_size=24,
                  color=COST),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "Why build windows of hundreds when, as chapter seven showed, a wrong guess drains them? <bookmark "
            "mark='a'/> Because of memory. A load that misses every cache waits hundreds of cycles for DRAM, and a "
            "core that wants to keep working through such a miss needs hundreds of other instructions to do. Part "
            "9 measures that wait. <bookmark mark='b'/> A big window only pays if the core predicts well enough to "
            "fill it, which is why predictors grew alongside: modern TAGE-style predictors miss only a few branches "
            "in every thousand instructions on typical code, far fewer than the Job's data-dependent length test. "
            "<bookmark mark='c'/> Decode widths grew too: three instructions a cycle in the Pentium Pro, four in Core "
            "2, six in Golden Cove, eight in Apple's M1. <bookmark mark='d'/> The price is area and power. The "
            "rename tables, the issue queues and the wakeup logic are among the largest and hottest structures on a "
            "modern chip, and they are why Part 10's power wall arrived when it did."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reading(self):
        head = label(r"Reading a real core", font_size=38).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"vendor optimization manuals: \ Intel, \ AMD, \ Arm", font_size=24, color=GREY_A),
            label(r"Agner Fog's microarchitecture guide and instruction tables", font_size=24, color=GREY_A),
            label(r"uops.info: \ latency, \ throughput and ports of every x86 instruction, \ measured", font_size=24,
                  color=GREY_A),
            label(r"independent measurement: \ Chips and Cheese, \ Dougall Johnson's Apple notes", font_size=24,
                  color=GREY_A),
            label(r"your own: \ \texttt{perf stat}, \ \texttt{perf record}, \ and the performance counters",
                  font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "Nobody has to take these numbers on faith. <bookmark mark='a'/> The vendors publish optimization "
            "manuals describing their cores. Agner Fog's guides, updated for decades, describe nearly every x86 core's "
            "pipeline. The uops.info project measured the latency, throughput and execution ports of every x86 "
            "instruction on every recent core. Independent writers measure the structures vendors do not disclose. "
            "<bookmark mark='b'/> And on any Linux machine, perf stat reads the core's own counters: instructions, "
            "cycles, branch misses, machine clears. Everything in this part can be seen on the computer in front of "
            "you."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(i) for i in items[:4]], lag_ratio=0.5), run_time=6.0)
            vo.wait_until("b")
            self.play(FadeIn(items[4]))
        self.wait(0.3)
        self.clear_scene()
