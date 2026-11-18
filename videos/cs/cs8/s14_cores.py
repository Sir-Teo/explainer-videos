from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt, load,
                                  mono)

# Historical reported retirement capacities. Counted operation units differ across designs.
# Firestorm's measured coalesced groups and rename-retire entries are discussed separately.
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
    ("Golden Cove", 2021, 512, "Intel", 6),
    ("Zen 4", 2022, 320, "AMD", None),
    ("Zen 5", 2024, 448, "AMD", None),
]
VENDOR = {"Intel": DATA, "AMD": NO, "Apple": GREY_A, "MIPS": YES, "DEC": CTRL}


class Cores(WatchScene):
    def construct(self):
        self.card()
        self.windows()
        self.widths()

    def card(self):
        self.chapter(13, r"Modern cores in numbers", r"How far have real machines taken all this?", lit=(1995, 2021), extra=((1995, r"Pentium Pro: \ 40"), (2021, r"Golden Cove: \ 512")), part=PART, said="Chapter thirteen. Modern cores in numbers.")

    # ------------------------------------------------------------------
    def windows(self):
        self.ask(r"A big 2024 core's reorder buffer. \\ About how many instructions in flight?",
                 [r"about 32", r"about 500", r"about 50{,}000"], 1,
                 say="How many instructions can a big core from 2024 keep in flight at once?",
                 reveal="Around five hundred.")
        head = label("Reported retirement capacities, \\ 1995 to 2024: \\ counted units vary", font_size=32).to_edge(UP,
                                                                                                     buff=0.3)
        ax = Axes(x_range=[1994, 2026, 4], y_range=[0, 700, 100], x_length=10.5, y_length=4.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(DOWN * 0.3)
        ax.x_axis.add_numbers(list(range(1994, 2027, 4)), font_size=16, num_decimal_places=0, group_with_commas=False)
        ax.y_axis.add_numbers(list(range(0, 701, 200)), font_size=16, num_decimal_places=0)
        dots = VGroup()
        for name, yr, rob, v, _ in CORES:
            p = ax.c2p(yr, rob)
            dt = Dot(p, radius=0.08, color=VENDOR[v])
            t = label(rf"{name} \ {rob}", font_size=17, color=VENDOR[v])
            side = {"Pentium Pro": UP, "MIPS R10000": DOWN, "Pentium 4": UP, "Sandy Bridge": LEFT, "Haswell": LEFT,
                    "Skylake": UP, "Sunny Cove": LEFT, "Apple M1 (Firestorm)": LEFT, "Golden Cove": LEFT}.get(name, RIGHT)
            t.next_to(dt, side, buff=0.1)
            dots.add(VGroup(dt, t))
        ours = DashedLine(ax.c2p(1994, 128), ax.c2p(2026, 128), color=HEAD, stroke_width=2)
        ol = label(r"our core: \ 128", font_size=18, color=HEAD).next_to(ax.c2p(2026, 128), UP, buff=0.05).shift(
            LEFT * 0.8)
        fn = note("Firestorm measured separately: \\ $\\sim330$ coalesced retire groups; \\\\ $\\sim623$ rename-retire entries (Dougall Johnson; reverse engineered)",
                  font_size=17).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "These are reported retirement-tracking capacities in a historical selection of cores from 1995 through "
            "2024. The entries do not all count the same thing: architectural instructions, micro-operations and "
            "fused operations must be distinguished. <bookmark mark='a'/> The early examples include Pentium Pro, "
            "MIPS R10000 and Alpha 21264. <bookmark mark='b'/> Later examples include Core 2, Sandy Bridge, "
            "Haswell, Skylake and Zen. Their capacities increased as implementations changed, but capacity alone "
            "does not predict workload performance. <bookmark mark='c'/> Sunny Cove, Golden Cove, Zen 4 and Zen 5 "
            "extend this historical sample. Apple Firestorm is shown separately: Dougall Johnson's "
            "reverse-engineered notes describe about three hundred thirty coalesced retire groups and six hundred "
            "twenty-three rename-retire entries. A single six-hundred-thirty-instruction ROB dot would hide that "
            "distinction. <bookmark mark='d'/> Our model tracks a hundred twenty-eight architectural instructions "
            "and is never full on this chapter; its entries are not directly interchangeable with every hardware "
            "entry on the plot."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            groups = {"a": [0, 1, 2], "b": [3, 4, 5, 6, 7, 8], "c": [9, 10, 11, 12]}
            for mk, idx in groups.items():
                if mk != "a":
                    vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(dots[i], scale=1.3) for i in idx], lag_ratio=0.2))
                if mk == "a":
                    vo.wait_until(mk)
            self.play(FadeIn(fn))
            vo.wait_until("d")
            self.play(Create(ours), FadeIn(ol))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def widths(self):
        head = label(r"Why so big?", font_size=38).to_edge(UP, buff=0.35)
        items = VGroup(
            label("illustration: \\ 300 cycles $\\times$ 4 starts/cycle = 1200 potential starts", font_size=24, color=INF),
            label("usable overlap depends on prediction, dependencies and memory behavior", font_size=24, color=NO),
            label("define fetch, decode, dispatch, issue and retirement widths separately", font_size=24, color=DATA),
            label("larger tracking/selection costs area and energy; \\ organization matters", font_size=24,
                  color=COST),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "Larger windows can expose independent work while a long-latency operation waits. <bookmark mark='a'/> "
            "As an illustration, a memory access lasting three hundred core cycles represents twelve hundred "
            "potential start opportunities at four per cycle. Whether they exist and can be reached depends on "
            "dependencies, prediction and resources; DRAM latency in cycles also depends on the clock and memory "
            "system. <bookmark mark='b'/> Branch accuracy varies with workload, predictor and measurement "
            "definition. A few misses per thousand instructions is not a universal property of typical code. "
            "<bookmark mark='c'/> Fetch, decode, dispatch, issue and retirement widths must be specified "
            "separately. Encoding, fusion and instruction mix change the operations counted at each stage. "
            "<bookmark mark='d'/> Larger tracking and selection structures cost area and energy. Banking, "
            "clustering, gating and other implementation choices change those costs. This discussion does not "
            "measure which structure is hottest or establish one universal best window size."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
                if mk == "a":
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

