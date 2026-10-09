from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import (
    FACTS, Plot, cpu_die, fmt_ns, label, load, machine_tag, mtex, node, note, schematic_tag, source, tagged,
)


def human(seconds: float) -> str:
    if seconds < 90:
        return f"{seconds:.0f} seconds"
    if seconds < 5400:
        return f"{seconds / 60:.0f} minutes"
    if seconds < 2 * 86400:
        return f"{seconds / 3600:.1f} hours"
    return f"{seconds / 86400:.0f} days"


class LatencyLadder(VoiceoverScene):
    def construct(self):
        self.staircase()
        self.tlb()
        self.ladder()

    # ------------------------------------------------------------------
    def staircase(self):
        b = load("bench")
        ch_ = b["chase"]
        sizes = np.array(ch_["sizes"], float)
        small, huge = np.array(ch_["small"]), np.array(ch_["huge"])
        l1 = small[sizes <= 32 * 1024].mean()
        l2 = small[(sizes >= 128 * 1024) & (sizes <= 512 * 1024)].mean()
        dram = small[-1]
        assert 1.0 < l1 < 2.0 and 4 < l2 < 7 and 200 < dram < 400 and huge[-1] < 0.8 * dram
        ch = Plot((4096, 2**30), (1, 400), width=10.6, height=4.6, log_x=True, log_y=True,
                  x_ticks=[2**12, 2**15, 2**18, 2**21, 2**24, 2**27, 2**30],
                  x_fmt=lambda v: label({2**12: "4 KiB", 2**15: "32 KiB", 2**18: "256 KiB", 2**21: "2 MiB",
                                         2**24: "16 MiB", 2**27: "128 MiB", 2**30: "1 GiB"}[int(v)], font_size=22,
                                        color=GREY_A),
                  y_ticks=[1, 10, 100], y_fmt=lambda v: fmt_ns(v)).shift(DOWN * 0.45 + RIGHT * 0.3)
        zones = VGroup(
            ch.span(4096, 48 * 1024, C.CACHE_L1, 0.12), ch.span(48 * 1024, 2 * 2**20, C.CACHE_L2, 0.12),
            ch.span(2 * 2**20, 24 * 2**20, C.CACHE_L3, 0.12), ch.span(24 * 2**20, 2**30, C.DRAM, 0.12))
        znames = VGroup(*[label(t, font_size=24, color=c).move_to(ch.c2p(x, 260)) for t, c, x in [
            ("L1", C.CACHE_L1, 14000), ("L2", C.CACHE_L2, 3.2e5), ("L3", C.CACHE_L3, 7e6), ("main memory", C.DRAM, 1.6e8)]])
        c_small = ch.line(sizes, small, WHITE, 4)
        c_huge = ch.line(sizes, huge, C.SIGNAL, 4)
        ttl = label(r"how long does one memory read take? It depends on how much memory you touch", font_size=30)
        ttl.to_edge(UP, buff=0.3)
        xl = label(r"amount of memory being read at random", font_size=24, color=GREY_A).next_to(ch.x_labels, DOWN, buff=0.12)
        yl = ch.y_title(r"time per read", font_size=24)
        cpu = b["cpu"]["Model name"].replace("(R)", "").replace("  ", " ")
        tag = machine_tag()
        sub = note(rf"{cpu}, 4 virtual cores", font_size=20).next_to(tag, DOWN, buff=0.08).align_to(tag, RIGHT)
        with self.voiceover(
            "Now let's go inside a single server, where the units shrink from milliseconds to nanoseconds. In one "
            "nanosecond, light travels thirty centimeters, about a foot. This machine's processor ticks every half "
            "nanosecond. <bookmark mark='m'/> Here's an experiment run on the computer that rendered this video: read "
            "memory at random addresses, each read depending on the last, and time each read as the amount of memory "
            "grows. <bookmark mark='l1'/> While everything fits in the tiny first-level cache, a read takes about a "
            "nanosecond and a half. <bookmark mark='l2'/> In the second-level cache, about five. <bookmark mark='l3'/> "
            "In the big shared third level, fifty or more. <bookmark mark='d'/> And out in main memory, two to three "
            "hundred nanoseconds. Two hundred times slower than the fastest case, for the same line of code."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(tag), FadeIn(sub))
            vo.wait_until("m")
            self.play(Create(ch), FadeIn(xl), FadeIn(yl))
            self.play(Create(c_small), run_time=3)
            for i, m in enumerate(["l1", "l2", "l3", "d"]):
                vo.wait_until(m)
                self.play(FadeIn(zones[i]), FadeIn(znames[i]), run_time=0.6)
        self.ch, self.c_huge, self.c_small = ch, c_huge, c_small
        self.sizes, self.small, self.huge = sizes, small, huge

    # ------------------------------------------------------------------
    def tlb(self):
        ch, sizes, small, huge = self.ch, self.sizes, self.small, self.huge
        gib = small[-1], huge[-1]
        box = VGroup(
            label(r"HRT's tech blog, on the TLB:", font_size=24, color=GREY_A),
            label(rf"a miss costs at least {FACTS['hrt_walk_loads']} dependent memory reads:", font_size=24),
            mtex(rf"{FACTS['hrt_walk_loads']} \times {FACTS['hrt_mem_ns']}\,\mathrm{{ns}} = {FACTS['hrt_walk_ns']}\,\mathrm{{ns}}",
                 font_size=30, color=C.KERNEL),
            label(r"a 2 MiB ``huge page'' covers 512$\times$ more memory per entry", font_size=24, color=C.SIGNAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        box.to_corner(UL, buff=0.35).shift(DOWN * 0.75 + RIGHT * 1.0)
        box.add_background_rectangle(color=BACKGROUND, opacity=0.92, buff=0.12)
        hl = tagged(rf"1 GiB: {gib[0]:.0f} ns $\to$ {gib[1]:.0f} ns with huge pages", font_size=24, color=C.SIGNAL)
        hl.next_to(ch.c2p(2**28, gib[1]), DOWN, buff=0.35)
        with self.voiceover(
            "Part of that cost isn't the data at all. Programs use virtual addresses, and the processor must translate "
            "each one into a physical address, with the help of a small cache of translations called the TLB. "
            "<bookmark mark='h'/> As engineers at Hudson River Trading explain on their tech blog, a miss in that cache "
            "means walking a tree of page tables: at least three dependent memory reads, or two hundred and ten "
            "nanoseconds in their example, before you even fetch your data. Their fix: huge pages, which let one "
            "translation cover 512 times more memory. <bookmark mark='c'/> Same experiment, with huge pages. Out in "
            "main memory, reads get about thirty percent faster."
        ) as vo:
            vo.wait_until("h")
            self.play(FadeIn(box))
            vo.wait_until("c")
            self.play(Create(self.c_huge), run_time=2.5)
            self.play(FadeIn(hl))
        self.clear_scene()

    # ------------------------------------------------------------------
    def ladder(self):
        b = load("bench")
        tpn = b["syscall"]["tsc_per_ns"]
        sizes, small = self.sizes, self.small
        pp = b["pingpong"]
        rungs = [
            (r"one clock cycle", 1 / tpn, GREY_A),
            (r"read from L1 cache", float(small[sizes <= 32 * 1024].mean()), C.CACHE_L1),
            (r"read from L2 cache", float(small[(sizes >= 128 * 1024) & (sizes <= 512 * 1024)].mean()), C.CACHE_L2),
            (r"read from L3 cache", float(small[(sizes >= 3e6) & (sizes <= 6e6)].mean()), C.CACHE_L3),
            (r"a trivial system call", b["syscall"]["getppid_ns"], C.KERNEL),
            (r"hand a cache line to another core", pp["shared_cache_line"]["pct"]["50"], C.MSG),
            (r"read from main memory", float(small[-1]), C.DRAM),
            (r"send through the kernel, receiver spinning", pp["udp_busy_poll"]["pct"]["50"], C.KERNEL),
            (r"send through the kernel, receiver asleep", pp["udp_blocking"]["pct"]["50"], C.KERNEL),
        ]
        assert 0.4 < rungs[0][1] < 0.6 and 80 < rungs[4][1] < 130 and 2000 < rungs[7][1] < 4000 and 10_000 < rungs[8][1] < 20_000
        ch = Plot((0.3, 30_000), (0, len(rungs)), width=7.2, height=5.6, log_x=True, x_ticks=[1, 10, 100, 1e3, 1e4],
                  x_fmt=lambda v: fmt_ns(v), grid=False, x_grid=True).move_to(RIGHT * 2.6 + DOWN * 0.35)
        ch.y_axis.set_opacity(0)
        bars, names, vals, hum = VGroup(), VGroup(), VGroup(), VGroup()
        l1 = rungs[1][1]
        for i, (t, ns, col) in enumerate(rungs):
            y = len(rungs) - 0.5 - i
            p0, p1 = ch.c2p(0.3, y), ch.c2p(ns, y)
            bar = Rectangle(width=max(p1[0] - p0[0], 0.02), height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.85)
            bar.move_to((p0 + p1) / 2)
            bars.add(bar)
            names.add(label(t, font_size=22, color=col).next_to(p0, LEFT, buff=0.15))
            vals.add(MathTex(fmt_ns(ns), font_size=24).next_to(bar, RIGHT, buff=0.1))
            hum.add(label(human(ns / l1), font_size=20, color=GREY_A).next_to(vals[-1], RIGHT, buff=0.25))
        ttl = label(r"the latency ladder of this computer (medians)", font_size=32).to_edge(UP, buff=0.3)
        scale = label(r"if an L1 read took one second:", font_size=22, color=GREY_A).next_to(hum[0], UP, buff=0.35)
        scale.align_to(hum, LEFT)
        with self.voiceover(
            "Put all the measurements on one ladder. <bookmark mark='a'/> A clock cycle, half a nanosecond. The three "
            "levels of cache. <bookmark mark='b'/> A system call, the cheapest possible request to the operating "
            "system: about a hundred nanoseconds. <bookmark mark='c'/> Handing a piece of memory from one core to "
            "another: about two hundred. Main memory: about three hundred. <bookmark mark='d'/> And sending one small "
            "message from one program to another through the operating system's network stack: almost three "
            "microseconds if the receiver is spinning, waiting for it, and fourteen if it's asleep and has to be woken "
            "up. <bookmark mark='h'/> To feel the proportions: if reading the first-level cache took one second, the "
            "sleeping receiver would take nearly three hours. Light gets from Chicago to New Jersey in four "
            "milliseconds, which on this scale is a month. And remember the market's reaction spike: twenty "
            "microseconds. Most of these rungs fit inside it many times over, but the bottom two eat a big piece."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(machine_tag()), Create(ch.x_axis), FadeIn(ch.x_labels), FadeIn(ch.grid))
            groups = [range(0, 4), range(4, 5), range(5, 7), range(7, 9)]
            for g, m in zip(groups, "abcd"):
                vo.wait_until(m)
                self.play(*[GrowFromEdge(bars[i], LEFT) for i in g], *[FadeIn(names[i]) for i in g],
                          *[FadeIn(vals[i]) for i in g], run_time=0.9)
            vo.wait_until("h")
            self.play(FadeIn(scale), LaggedStart(*[FadeIn(h) for h in hum], lag_ratio=0.15), run_time=2)
        self.clear_scene()
