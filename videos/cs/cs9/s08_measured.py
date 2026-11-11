from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, LEVEL_COLOR, NO, PART, YES, fmt,
                                  load, mono, plot_range, size_label, staircase_axes)

CHASE_C = ["for (i = 0; i < steps; i++)", "    p = *p;      /* the next address is in the line just read */"]


class Measured(VoiceoverScene):
    def construct(self):
        self.card()
        self.method()
        self.stairs()
        self.huge()
        self.bandwidth()

    def card(self):
        card = chapter_card(7, r"This machine's staircase", r"How far away is each level, \ really?", lit=(2007,),
                            extra=((2007, r"Drepper: \ What every programmer should know"),), part=PART)
        with self.voiceover(
            "Chapter seven. This machine's staircase."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def method(self):
        head = label(r"Measuring latency: \ chase a pointer", font_size=36).to_edge(UP, buff=0.4)
        code = VGroup(*[mono(s, 22) for s in CHASE_C]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(UP * 0.9)
        n = 10
        ring = VGroup(*[Square(side_length=0.5, stroke_color=GREY_C, stroke_width=1.5) for _ in range(n)]).arrange(
            RIGHT, buff=0.15).move_to(DOWN * 0.8)
        order = [0, 6, 3, 8, 1, 5, 9, 2, 7, 4]
        arrows = VGroup()
        for k in range(n):
            a, b = ring[order[k]], ring[order[(k + 1) % n]]
            arrows.add(CurvedArrow(a.get_top(), b.get_top(), angle=-0.8 if order[(k + 1) % n] > order[k] else 0.8,
                                   color=DATA, stroke_width=2, tip_length=0.12))
        cap = note("one pointer per 64-byte line; \\ random cycle suppresses ordinary stride prediction",
                   font_size=20).next_to(ring, DOWN, buff=0.35)
        rule = label("serial dependent loads: \\ effective access time includes system effects", font_size=26,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Measure a dependent random walk through a chosen working-set size. <bookmark mark='a'/> Place one "
            "pointer in each sixty-four-byte line and link the lines into a randomly permuted cycle. Each next "
            "address comes from the previous load. The benchmark warms the cycle, repeats twenty million steps and "
            "reports the best of three timed trials. <bookmark mark='b'/> This serial dependency suppresses overlap "
            "between the measured loads, and the irregular order reduces ordinary stride-prefetch opportunities. It "
            "does not defeat every possible temporal prefetcher. Loop overhead, address translation, cache "
            "placement, virtualized scheduling and interference can still affect the result. The time per step is an "
            "effective dependent-access measurement, not an isolated component delay."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(code), FadeIn(ring))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cap), FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stairs(self):
        st = load("staircase")
        m = st["machine"]
        pts = st["points"]
        head = label(rf"The staircase, \ measured on this computer", font_size=34).to_edge(UP, buff=0.25)
        sub = note(rf"CPU: \ {m['cpu']} \\ reported totals: \ L1d {m['caches'].get('L1d', '?')}, \ L2 {m['caches'].get('L2', '?')}, \ "
                   rf"L3 {m['caches'].get('L3', '?')}", font_size=16).next_to(head, DOWN, buff=0.1)
        ymax, ystep = plot_range(p["ns"] for p in pts)
        ax, ticks = staircase_axes(pts, x_length=10.8, y_length=4.2, ymax=ymax)
        g = VGroup(ax, ticks).move_to(DOWN * 0.45)
        ax.y_axis.add_numbers(np.arange(0, ymax + ystep / 2, ystep).tolist(), font_size=16, num_decimal_places=0)
        yl = note(r"nanoseconds per load", font_size=18).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(np.log2(p["bytes"]), p["ns"]), radius=0.06, color=HEAD) for p in pts])
        line = VMobject(color=HEAD, stroke_width=3).set_points_as_corners([d.get_center() for d in dots])
        by = {p["bytes"]: p["ns"] for p in pts}
        ann = VGroup(
            label(rf"16 KiB: \ {by[16 << 10]:.1f} ns", font_size=20, color=YES).next_to(ax.c2p(14, by[16 << 10]), UP,
                                                                                buff=0.25),
            label(rf"256 KiB: \ {by[256 << 10]:.1f} ns", font_size=20, color=DATA).next_to(ax.c2p(18, by[256 << 10]), UP,
                                                                                  buff=0.5),
            label(rf"2 MiB: \ {by[2 << 20]:.0f} ns", font_size=20, color=CTRL).next_to(
                ax.c2p(21, by[2 << 20]), UP, buff=0.85),
            label(rf"8 MiB: \ {by[8 << 20]:.0f} ns", font_size=20, color=NO).next_to(ax.c2p(23, by[8 << 20]), UP,
                                                                                 buff=0.15),
            label(rf"512 MiB: \ {by[512 << 20]:.0f} ns", font_size=20, color=NO).next_to(
                ax.c2p(29, by[512 << 20]), UP, buff=0.25).shift(LEFT * 0.8),
        )
        vm = label("reported totals and timing transitions do not prove private available capacity", font_size=22,
                   color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Read the host identity and the measured points together. The current data come from the processor named "
            "above the plot; the source is not tied to an older Xeon run. <bookmark mark='a'/> Small working sets "
            "have the lowest measured delay. <bookmark mark='b'/> Increasing the footprint exposes further plateaus "
            "and transitions. <bookmark mark='c'/> A selected point is a sample at that footprint, not proof of one "
            "exact cache-level boundary. <bookmark mark='d'/> The largest walks can combine last-level misses, "
            "translation effects, system placement and interference. Timing alone does not identify their individual "
            "contributions. <bookmark mark='e'/> The lscpu strings describe reported cache totals and instances, not "
            "guaranteed private capacity available to this process. Use controlled experiments and performance "
            "events to investigate a transition's cause."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), Create(ax), FadeIn(ticks), FadeIn(yl))
            self.play(Create(line), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05), run_time=2.5)
            for mk, a in zip("abcd", ann[:4]):
                vo.wait_until(mk)
                self.play(FadeIn(a))
            self.play(FadeIn(ann[4]))
            vo.wait_until("e")
            self.play(FadeIn(vm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def huge(self):
        d = load("hugepages")["points"]
        head = label(r"The top of the staircase: \ translation", font_size=34).to_edge(UP, buff=0.3)
        xs = [np.log2(p["bytes"]) for p in d]
        ymax, ystep = plot_range(p[k] for p in d for k in ("small", "huge"))
        ax = Axes(x_range=[min(xs), max(xs) + 0.3, 1], y_range=[0, ymax, ystep], x_length=9.5, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(DOWN * 0.4 + LEFT * 0.6)
        ax.y_axis.add_numbers(np.arange(0, ymax + ystep / 2, ystep).tolist(), font_size=16, num_decimal_places=0)
        ticks = VGroup(*[label(size_label(p["bytes"]), font_size=15, color=GREY_B).next_to(
            ax.c2p(np.log2(p["bytes"]), 0), DOWN, buff=0.12) for p in d])
        small = VMobject(color=NO, stroke_width=4).set_points_as_corners(
            [ax.c2p(np.log2(p["bytes"]), p["small"]) for p in d])
        huge = VMobject(color=YES, stroke_width=4).set_points_as_corners(
            [ax.c2p(np.log2(p["bytes"]), p["huge"]) for p in d])
        ls = label("default allocation", font_size=22, color=NO).next_to(small.get_end(), UP, buff=0.1)
        lh = label("huge-page advice", font_size=22, color=YES).next_to(huge.get_end(), DOWN, buff=0.15)
        yl = note(r"nanoseconds per dependent load", font_size=18).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        facts = VGroup(
            label("page-size advice requested; \\ actual backing-page sizes were not verified", font_size=22,
                  color=GREY_A),
            label(rf"512 MiB: \ default {d[-1]['small']:.0f} ns, \ advised {d[-1]['huge']:.0f} ns",
                  font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Address translation can affect a large dependent walk, so compare two allocation treatments. The first "
            "uses the default allocation; the second requests transparent huge pages with madvise. <bookmark "
            "mark='a'/> A translation-cache miss can require a page-table walk, but its entries may hit other "
            "caches; not every access necessarily walks all the way to memory. <bookmark mark='b'/> A two-mebibyte "
            "page covers five hundred twelve times the address range of a four-kibibyte page. That can increase "
            "translation reach. Our benchmark records timings and the kernel's advice mode, but does not verify "
            "actual backing-page sizes. The displayed difference therefore compares default and advised allocations, "
            "not proven small-page and huge-page populations or an isolated translation cost."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), FadeIn(yl), FadeIn(facts[0]))
            self.play(Create(small), FadeIn(ls), run_time=1.5)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(huge), FadeIn(lh), run_time=1.5)
            self.play(FadeIn(facts[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bandwidth(self):
        b = load("bandwidth")["points"]
        head = label(r"Bandwidth: \ reading in order", font_size=36).to_edge(UP, buff=0.3)
        xs = [np.log2(p["bytes"]) for p in b]
        ymax, ystep = plot_range(p["gbs"] for p in b)
        ax = Axes(x_range=[min(xs) - 1, max(xs) + 1, 2], y_range=[0, ymax, ystep], x_length=10.5, y_length=4.2, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16},
                  x_axis_config={"include_ticks": False}).move_to(DOWN * 0.4)
        ax.y_axis.add_numbers(np.arange(0, ymax + ystep / 2, ystep).tolist(), font_size=16, num_decimal_places=0)
        ticks = VGroup(*[label(size_label(p["bytes"]), font_size=15, color=GREY_B).next_to(
            ax.c2p(np.log2(p["bytes"]), 0), DOWN, buff=0.12) for p in b])
        yl = note(r"GB/s of logical reads, \ one C thread", font_size=18).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        bars = VGroup(*[Rectangle(width=0.45, height=4.2 * p["gbs"] / ymax, stroke_width=0,
                                  fill_color=YES if p["bytes"] <= 1 << 20 else (CTRL if p["bytes"] <= 8 << 20 else NO),
                                  fill_opacity=0.85).move_to(ax.c2p(np.log2(p["bytes"]), 0), aligned_edge=DOWN)
                        for p in b])
        vals = VGroup(*[label(f"{p['gbs']:.0f}", font_size=16, color=GREY_A).next_to(bar, UP, buff=0.05)
                        for p, bar in zip(b, bars)])
        punch = label("logical read throughput; \\ separate pointer-chase timing does not count in-flight requests",
                      font_size=24, color=HEAD).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Sequential throughput measures a different workload from the dependent random walk. This C loop sums a "
            "repeatedly reused array, with several independent accumulators, and reports the best of five trials. "
            "<bookmark mark='a'/> The bars show bytes read per second at each array footprint on this host. "
            "Cache-resident trials can reuse previously fetched lines, so logical bytes processed are not "
            "necessarily new DRAM traffic. <bookmark mark='b'/> Multiplying a compatible throughput by a compatible "
            "latency estimates required average concurrency by Little's law. These separate workloads do not "
            "directly count outstanding hardware requests or prove that a particular prefetcher caused the "
            "throughput. Latency, available parallelism and sustainable bandwidth all constrain performance; measure "
            "the workload you intend to optimize."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), FadeIn(yl))
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in bars], lag_ratio=0.1), FadeIn(vals))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()
