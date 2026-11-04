from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, LEVEL_COLOR, NO, PART, YES, fmt, load,
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
        ghz = st["machine"]["ghz"]
        pts = {p["bytes"]: p["ns"] for p in st["points"]}
        rows = [(r"a register", 1 / ghz, YES), (r"the L1 cache", pts[16 << 10], YES), (r"the L2 cache", pts[256 << 10], DATA),
                (r"the next level", pts[2 << 20], CTRL), (r"DRAM", pts[8 << 20], NO),
                (r"DRAM, \ far away \ (a TLB miss too)", pts[512 << 20], NO),
                (r"an SSD \ (typical)", 100e3, INF), (r"a disk \ (typical)", 5e6, INF)]
        head = label(rf"If one clock cycle of this computer \ ({ghz:g} GHz) \ took a second", font_size=34).to_edge(
            UP, buff=0.35)
        table = VGroup()
        for name, ns, c in rows:
            secs = ns * ghz
            table.add(VGroup(label(name, font_size=26, color=c),
                             label(rf"{ns:,.1f} ns" if ns < 1000 else rf"{ns / 1000:,.0f} $\mu$s" if ns < 1e6 else
                                   rf"{ns / 1e6:,.0f} ms", font_size=22, color=GREY_B),
                             label(human(secs), font_size=28, color=c)))
        for r in table:
            r[0].move_to([-3.6, 0, 0], aligned_edge=RIGHT)
            r[1].move_to([-1.2, 0, 0])
            r[2].move_to([1.0, 0, 0], aligned_edge=LEFT)
        table.arrange(DOWN, buff=0.28)
        for r in table:
            r[0].align_to([-3.4, 0, 0], RIGHT)
            r[1].set_x(-1.6)
            r[2].align_to([0.2, 0, 0], LEFT)
        table.move_to(DOWN * 0.2)
        cols = VGroup(note(r"measured here", font_size=20).move_to([-1.6, table.get_top()[1] + 0.35, 0]),
                      note(r"at one second a cycle", font_size=20).move_to([1.6, table.get_top()[1] + 0.35, 0]))
        with self.voiceover(
            "Here is a way to feel how far away memory is. This computer's clock ticks two point eight billion times "
            "a second. Slow it down until each tick takes one second. <bookmark mark='a'/> Then a value in a register "
            "is ready in a second. <bookmark mark='b'/> The nearest cache, L1, answers in about four seconds; the "
            "next, L2, in twelve. <bookmark mark='c'/> The next level takes over a minute. <bookmark mark='d'/> Main "
            "memory, DRAM, takes six and a half minutes, and a quarter of an hour when the address must also be "
            "looked up in the page tables. <bookmark mark='e'/> A solid-state disk, about three days. A spinning disk, "
            "about five months. All of these numbers but the last two were measured on this machine, as this part "
            "will show."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols))
            for mk, idx in zip("abcde", ([0], [1, 2], [3], [4, 5], [6, 7])):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(table[i], shift=UP * 0.1) for i in idx], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wall(self):
        j = load("job")
        sc = load("scans")
        head = label(r"The Job, \ thirty novels: \ how much memory does it read?", font_size=34).to_edge(UP, buff=0.35)
        facts = VGroup(
            label(rf"a word table of {sc['table_entries']:,} entries: \ {sc['table_kb']:.0f} KB", font_size=26,
                  color=DATA),
            label(rf"scanned from the start for every word: \ {sc['line_reads'] / 1e9:.1f} billion cache-line reads",
                  font_size=26, color=GREY_A),
            label(r"with a 32 KB cache, \ " + rf"{100 * sc['rows'][3]['lru']:.0f}\% of them miss", font_size=28,
                  color=NO),
            label(rf"and yet: \ the Job slows down by {100 * j['change']:.2f}\% \ (at Pebble's clock)", font_size=28,
                  color=YES),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        with self.voiceover(
            "Now the Job. <bookmark mark='a'/> Over all thirty novels its word table grows to fifty-eight thousand "
            "entries, six hundred eighty kilobytes. <bookmark mark='b'/> And for every one of four and a half million "
            "words, it scans that table from the start: almost three billion reads of a cache line. <bookmark "
            "mark='c'/> A cache of thirty-two kilobytes, like this machine's L1, misses eighty-eight percent of them. "
            "<bookmark mark='d'/> And yet, give Part 8's core this machine's whole memory hierarchy, and the Job slows "
            "down by a twentieth of one percent. By the end of this part you will know why both of those numbers are "
            "true, and when the second one stops being true."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcd", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
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
            label(r"a theorem about pebbles: \ how much data any matrix multiply must move", font_size=27, color=HEAD),
            label(r"the Job meets real memory: \ ledger row 3", font_size=27, color=COST),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is where this part goes. <bookmark mark='a'/> Caches, built from nothing: how an address is split "
            "into tag, index and offset, sets and ways, and which line to throw out. <bookmark mark='b'/> The three "
            "kinds of miss, measured on the Job. <bookmark mark='c'/> This computer's memory, measured: a staircase of "
            "latencies, and the bandwidth at each level. <bookmark mark='d'/> Then theory: a game with red and blue "
            "pebbles that proves how much data any matrix multiplication must move. <bookmark mark='e'/> And the Job, "
            "given real memory, for the next row of the ledger."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcde", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
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
            "and set-associative caches, how they choose what to evict, and what they do with writes. The three kinds "
            "of miss, and the average time an access takes. This machine's memory, measured, and how to program for "
            "it, including algorithms that use every level of cache without knowing their sizes. The red-blue pebble "
            "game, and the theory of external memory behind every database index. Then prefetching, the inside of a "
            "DRAM chip, and the Job."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
