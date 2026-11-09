from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, LEVEL_COLOR, NO, PART, REFERENCE_GHZ, YES, fmt, load,
                                  size_label)


def human(seconds: float) -> str:
    for unit, s in (("years", 3.15e7), ("months", 2.6e6), ("days", 86400), ("hours", 3600), ("minutes", 60)):
        if seconds >= s:
            v = seconds / s
            return rf"{v:.0f} {unit}" if v >= 10 else rf"{v:.1f} {unit}"
    return rf"{seconds:.0f} seconds" if seconds >= 10 else rf"{seconds:.1f} seconds"


class Hook(VoiceoverScene):
    def construct(self):
        self.scale()
        self.wall()
        self.preview()
        self.plan()

    # ------------------------------------------------------------------
    def scale(self):
        st = load("staircase")
        ghz = REFERENCE_GHZ
        pts = {p["bytes"]: p["ns"] for p in st["points"]}
        rows = [("one cycle \\ (illustration)", 1 / ghz, YES),
                ("random walk, \\ 16 KiB", pts[16 << 10], YES),
                ("random walk, \\ 256 KiB", pts[256 << 10], DATA),
                ("random walk, \\ 2 MiB", pts[2 << 20], CTRL),
                ("random walk, \\ 8 MiB", pts[8 << 20], NO),
                ("random walk, \\ 512 MiB", pts[512 << 20], NO),
                ("SSD access \\ (rough example)", 100e3, INF), ("disk access \\ (rough example)", 5e6, INF)]
        head = label(rf"One cycle at an illustrative {ghz:g} GHz \ $\to$ \ one second", font_size=34).to_edge(
            UP, buff=0.35)
        table = VGroup()
        for name, ns, c in rows:
            secs = ns * ghz
            table.add(VGroup(label(name, font_size=23, color=c),
                             label(rf"{ns:,.1f} ns" if ns < 1000 else rf"{ns / 1000:,.0f} $\mu$s" if ns < 1e6 else
                                   rf"{ns / 1e6:,.0f} ms", font_size=22, color=GREY_B),
                             label(human(secs), font_size=28, color=c)))
        table.arrange(DOWN, buff=0.28).move_to(DOWN * 0.25)
        for r in table:
            if r[0].width > 4.3:
                r[0].scale_to_fit_width(4.3)
            r[0].move_to([-5.8, r[0].get_y(), 0], aligned_edge=LEFT)
            r[1].set_x(-0.5)
            r[2].move_to([1.5, r[2].get_y(), 0], aligned_edge=LEFT)
        cols = VGroup(note("time sample / example", font_size=18).move_to([-0.5, table.get_top()[1] + 0.35, 0]),
                      note("scaled reference time", font_size=18).move_to([3.0, table.get_top()[1] + 0.35, 0]))
        with self.voiceover(
            "Start with the measured pointer-chase times on this host. To make them tangible, scale them using an "
            "illustrative two-point-eight-gigahertz reference clock; the host does not report a verified clock here. "
            "<bookmark mark='a'/> The register row is a one-cycle illustration, not a measured universal instruction "
            "latency. <bookmark mark='b'/> Small working sets usually find nearby cache storage. <bookmark "
            "mark='c'/> Larger sets expose further changes in effective access time. <bookmark mark='d'/> The "
            "largest random walks can include cache misses, address translation and other system effects. Their "
            "timing alone cannot separate those causes. <bookmark mark='e'/> The storage-device rows are rough "
            "access-latency examples, not measurements from this host. Read the labels and units before comparing "
            "the scaled times."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols))
            for mk, idx in zip("abcde", ([0], [1, 2], [3], [4, 5], [6, 7])):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(table[i], shift=UP * 0.1) for i in idx], lag_ratio=0.4))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wall(self):
        j = load("job")
        sc = load("scans")
        head = label(r"The Job, \ thirty novels: \ how much memory does it read?", font_size=34).to_edge(UP, buff=0.35)
        facts = VGroup(
            label(rf"abstract table: \ {sc['table_entries']:,} entries, \ {sc['table_kb']:.0f} KiB", font_size=26,
                  color=DATA),
            label(rf"table-length prefix stream: \ {sc['line_reads'] / 1e9:.1f} billion line visits",
                  font_size=26, color=GREY_A),
            label(r"32 KiB fully associative LRU, \ table-only: \ " + rf"{100 * sc['rows'][3]['lru']:.0f}\% misses", font_size=26,
                  color=NO),
            label(rf"separate fitted memory model: \ {100 * j['change']:.2f}\% added cycles \ (assumed clock)", font_size=26,
                  color=YES),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        with self.voiceover(
            "The corpus model gives an apparent puzzle. <bookmark mark='a'/> Its abstract word table grows to nearly "
            "fifty-eight thousand entries, about six hundred seventy-eight kibibytes. <bookmark mark='b'/> Prefix "
            "scans over the recorded corpus imply about two point eight billion table-line visits. <bookmark "
            "mark='c'/> A cold, fully associative thirty-two-kibibyte LRU cache misses about eighty-eight percent of "
            "these table-only visits. This excludes interleaved letters and writes. <bookmark mark='d'/> A separate "
            "fitted cost projection combines sampled cache events with short core benchmarks. Its small displayed "
            "slowdown depends strongly on idealized prefetching and the chosen clock. It is not a full-corpus "
            "execution through a realistic hardware memory system. We will build each model and see what it can "
            "establish."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcd", facts):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def preview(self):
        head = label(r"By the end of this part", font_size=40).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"caches built from scratch: \ tags, \ sets, \ ways, \ replacement", font_size=27, color=DATA),
            label(r"the three kinds of miss, \ measured on the Job", font_size=27, color=CTRL),
            label(r"this machine's memory, \ measured: \ the latency staircase and the bandwidth", font_size=27,
                  color=YES),
            label("classical multiplication: \\ movement bounds under explicit rules", font_size=27, color=HEAD),
            label("the Job: \\ conditional memory-cost projection, \\ ledger row 3", font_size=27, color=COST),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the route through the part. <bookmark mark='a'/> Build address fields, sets, ways and "
            "replacement decisions. <bookmark mark='b'/> Compare miss classifications under explicit reference "
            "models. <bookmark mark='c'/> Measure dependent-load time and sequential throughput, while keeping "
            "system attribution separate from observation. <bookmark mark='d'/> Then use the red-blue pebble game to "
            "reason about data movement for a specified classical matrix-multiplication computation. Fast "
            "multiplication algorithms and different graph rules need different bounds. <bookmark mark='e'/> "
            "Finally, combine corpus counts, sampled events and simplified core experiments into a conditional "
            "ledger projection."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcde", facts):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ The Memory Hierarchy", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"the memory wall, \ and locality, \ the reason caches work",
            r"direct-mapped and set-associative caches; \ replacement and write policies",
            r"compulsory, \ capacity and conflict misses; \ average memory access time",
            r"this machine measured; \ programming for caches; \ cache-oblivious algorithms",
            r"the red-blue pebble game; \ external memory and B-trees",
            r"prefetching; \ inside DRAM; \ the Job, \ ledger row 3",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 9 of Computer Science, Built, the third part of Act Two, Making It Fast. <bookmark "
            "mark='a'/> In this part: the memory wall, and locality, which is why caches work at all. Direct-mapped "
            "and set-associative caches, how they choose what to evict, and what they do with writes. The three "
            "kinds of miss, and the average time an access takes. This machine's memory, measured, and how to "
            "program for it, including algorithms that use every level of cache without knowing their sizes. The "
            "red-blue pebble game, and external-memory models used to analyze many storage algorithms. Then prefetching, "
            "the inside of a DRAM chip, and the Job."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
