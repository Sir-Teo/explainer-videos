from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (HEAD, LAM, NO, PART, YES, fit_right, grid_table, load)


def size_text(b):
    for unit, k in (("TiB", 40), ("GiB", 30), ("MiB", 20), ("KiB", 10)):
        if b >= 1 << k:
            v = b / (1 << k)
            return rf"{v:.0f} {unit}" if v == int(v) else rf"{v:.1f} {unit}"
    return f"{b} B"


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.reach()
        self.research()
        self.tiers()
        self.formal()
        self.open_()

    def card(self):
        card = chapter_card(15, r"Frontier: \ translation reach and memory tiers",
                            r"What is still unsolved in virtual memory?", lit=(2013, 2019, 2023),
                            extra=((2013, r"direct segments"), (2019, r"CXL"), (2023, r"TPP; \ Mosaic pages")),
                            part=PART)
        with self.voiceover("Chapter fifteen. The frontier: translation reach, and memory in tiers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def reach(self):
        d = load("frontier")
        st = next(r for r in load("staircase")["rows"] if r[0] == 65536)
        head = label(r"TLB reach has fallen behind memory", font_size=36).to_edge(UP, buff=0.3)
        lo, hi = 18, 42
        W = 8.4
        x0 = -2.6
        xs = lambda b: x0 + W * (math.log2(b) - lo) / (hi - lo)
        rows = VGroup()
        colors = {"4 KiB": NO, "2 MiB": HEAD, "1 GiB": YES}
        for r in d["rows"]:
            w = xs(r["reach"]) - x0
            bar = Rectangle(width=max(0.05, w), height=0.36, stroke_width=0, fill_color=colors[r["page"]],
                            fill_opacity=0.8)
            name = label(rf"{r['entries']:,} entries $\times$ {r['page']}".replace(",", "{,}"), font_size=18,
                         color=GREY_A)
            val = label(size_text(r["reach"]), font_size=17, color=WHITE)
            rows.add(VGroup(name, bar, val))
        rows_y = [1.75 - 0.52 * i for i in range(len(rows))]
        for r, y in zip(rows, rows_y):
            r[1].move_to([x0, y, 0], aligned_edge=LEFT)
            r[0].next_to(r[1], LEFT, buff=0.2).align_to([x0 - 0.2, 0, 0], RIGHT)
            r[2].next_to(r[1], RIGHT, buff=0.12)
        mems = VGroup()
        for name, b in d["memories"]:
            x = xs(b)
            ln = DashedLine([x, 2.15, 0], [x, -1.15, 0], color=LAM, stroke_width=2)
            t = label(rf"{name}: \ {size_text(b)}", font_size=17, color=LAM).next_to(ln, DOWN, buff=0.08)
            mems.add(VGroup(ln, t))
        mems[1][1].shift(LEFT * max(0, mems[1][1].get_right()[0] - 6.9))
        sub = label(r"reach = entries $\times$ page size: \ a first-level TLB \ (64) \ and a second-level one \ (1{,}536), "
                    r"\ as if every entry held that size", font_size=18, color=GREY_A).next_to(head, DOWN, buff=0.15)
        lines = VGroup(
            label(r"64 small pages cover 256 KiB: \ less than this machine's L2 cache", font_size=20, color=NO),
            label(rf"chapter 5's staircase, \ 256 MiB chased: \ {st[2]:.0f} ns per access with 2 MiB pages, \ "
                  rf"{st[1]:.0f} with 4 KiB", font_size=20, color=HEAD),
            label(r"huge pages close the gap, \ but cost memory \ (a 2 MiB page for a few bytes) \ and need 2 MiB of "
                  r"\textit{contiguous} frames", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The first frontier is reach: how much memory the TLB can translate without walking. <bookmark mark='a'/> "
            "A first-level data TLB of sixty-four entries, with four-kibibyte pages, covers two hundred and fifty-six "
            "kibibytes, less than this machine's second-level cache. The second-level TLB, with fifteen hundred "
            "entries, covers six mebibytes. <bookmark mark='b'/> A laptop has sixteen gibibytes; a large server, four "
            "tebibytes, a million times the reach. <bookmark mark='c'/> Huge pages multiply the reach by five hundred "
            "and twelve, or by a quarter of a million. <bookmark mark='d'/> On chapter five's staircase, a pointer "
            "chase over two hundred and fifty-six mebibytes took forty percent less time with two-mebibyte pages. <bookmark mark='e'/> But a huge page "
            "wastes memory when only a little of it is used, and it needs two mebibytes of contiguous physical frames, "
            "which a busy machine's buddy allocator may not have."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            for r in (rows[0], rows[3]):
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]), FadeIn(lines[0]) if r is rows[0]
                          else Wait(0.01))
            vo.wait_until("b")
            self.play(FadeIn(mems))
            vo.wait_until("c")
            for i in (1, 2, 4, 5):
                self.play(FadeIn(rows[i][0]), GrowFromEdge(rows[i][1], LEFT), FadeIn(rows[i][2]), run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def research(self):
        head = label(r"Research on reach", font_size=36).to_edge(UP, buff=0.3)
        tab = grid_table([r"idea", r"year", r"what it does"], [
            [r"direct segments", r"2013", r"Basu et al.: \ one base-and-bounds range for a big heap, \ beside paging"],
            [r"redundant memory mappings", r"2015", r"Karakostas et al.: \ a range TLB of a few large extents"],
            [r"Ingens; \ HawkEye", r"2016; \ 2019", r"when to promote to huge pages, \ fairly, \ without bloat"],
            [r"Midgard", r"2021", r"translate late: \ caches use an intermediate address space"],
            [r"Mosaic pages", r"2023", r"hash a page into a few frames, \ so a TLB entry covers several pages"],
        ], widths=[4.0, 1.9, 7.4], row_h=0.58, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45)
        line = label(r"chapter 2's segments, \ back in a new role: \ big contiguous ranges are cheap to translate",
                     font_size=21, color=YES).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Research attacks reach from several sides. <bookmark mark='a'/> Direct segments, in 2013: give a big "
            "server's heap one base-and-bounds register, beside ordinary paging. <bookmark mark='b'/> Redundant memory "
            "mappings: a small TLB of ranges, each covering a large contiguous extent. <bookmark mark='c'/> Ingens and "
            "HawkEye: policies for when the kernel should promote small pages to huge ones, fairly between processes "
            "and without bloating memory. <bookmark mark='d'/> Midgard: let the caches work in an intermediate "
            "address space, and translate only on the way to memory. <bookmark mark='e'/> And Mosaic pages, in 2023: "
            "restrict each page to a few possible frames, chosen by hashing, so one entry can describe several pages. "
            "<bookmark mark='f'/> Notice chapter two's segments returning: a large contiguous range is cheap to "
            "translate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            for mk, r in zip("abcde", tab.cells[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r)))
            vo.wait_until("f")
            self.play(FadeIn(line))
        self.wait(0.3)
        self.clear_scene()

    def tiers(self):
        head = label(r"Memory in tiers", font_size=36).to_edge(UP, buff=0.3)
        tiers = VGroup()
        for t, lat, c, w in ((r"local DRAM", r"$\sim$100 ns", YES, 3.4), (r"CXL-attached memory", r"$\sim$200--300 ns",
                                                                           HEAD, 5.0),
                             (r"SSD, \ via page faults", r"$\sim$100 $\mu$s", NO, 6.6)):
            r = Rectangle(width=w, height=0.7, stroke_color=c, stroke_width=1.8, fill_color=c, fill_opacity=0.2)
            tiers.add(VGroup(r, label(rf"{t}: \ {lat}", font_size=20, color=WHITE).move_to(r)))
        tiers.arrange(DOWN, buff=0.15).next_to(head, DOWN, buff=0.5)
        lines = VGroup(
            label(r"the question of chapter 7 again: \ which pages deserve the fast tier?", font_size=21, color=WHITE),
            label(r"the kernel sees only the accessed bits: \ clearing them costs TLB flushes on every core",
                  font_size=21, color=NO),
            label(r"TPP \ (Meta, \ 2023): \ demote cold pages, \ promote on a sampled fault; \ now in Linux",
                  font_size=21, color=HEAD),
            label(r"sampling hardware \ (Intel PEBS) \ finds hot pages without faults; \ how well, \ and how cheaply, "
                  r"\ is open", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.16).next_to(tiers, DOWN, buff=0.45)
        with self.voiceover(
            "The second frontier is that memory is no longer one thing. <bookmark mark='a'/> Beside the DRAM on the "
            "processor's own channels, servers can now attach more memory over CXL, a protocol on the PCI Express "
            "link, at two or three times the latency. Beyond that, the disk. <bookmark mark='b'/> So the operating "
            "system faces chapter seven's question again, with a new twist: not which page to evict, but which pages "
            "deserve the fast tier. <bookmark mark='c'/> And it is nearly blind. The kernel learns about use only from "
            "the accessed bits, and to read them fresh it must clear them and flush the TLBs of every core. <bookmark "
            "mark='d'/> Meta's TPP, in 2023, demotes cold pages to the slow tier and promotes pages that fault there "
            "often; it is now part of Linux. <bookmark mark='e'/> Processors can also sample memory accesses in "
            "hardware. How accurately, and how cheaply, the kernel can find hot pages that way is an open question."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in tiers], lag_ratio=0.3))
            for mk, ln in zip("bcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def formal(self):
        head = label(r"What exactly does the hardware promise?", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(*[VGroup(label(t, font_size=24, color=c), label(s, font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08) for t, s, c in (
            (r"page tables are memory too", r"the walker reads them with ordinary loads, \ racing the kernel's stores "
                                            r"on other cores \ (Part 10's memory models)", WHITE),
            (r"a formal model, \ at last", r"Simner et al. \ (2022): \ relaxed virtual memory on Armv8-A, \ checked "
                                          r"against hardware and architects", HEAD),
            (r"TLB shootdowns", r"changing a mapping means interrupting every core that may cache it: \ microseconds "
                                r"each \ (LATR, \ 2018)", NO),
            (r"verified kernels", r"seL4 and Komodo prove their page-table code \ against a model of the MMU", YES))]
                      ).arrange(DOWN, buff=0.32, aligned_edge=LEFT).next_to(head, DOWN, buff=0.5)
        fit_right(items)
        with self.voiceover(
            "The third frontier is the foundations. <bookmark mark='a'/> Page tables are themselves memory. The "
            "hardware walker reads them with ordinary loads, while the kernel on another core may be changing them, "
            "so translation inherits all the difficulties of Part 10's weak memory models. <bookmark mark='b'/> Only "
            "in 2022 did Ben Simner and colleagues publish a precise model of how virtual memory behaves on Arm "
            "processors, tested against the hardware and agreed with Arm's architects. <bookmark mark='c'/> Changing a "
            "mapping means interrupting every core that might have it cached, a TLB shootdown, which costs "
            "microseconds each time and limits how fast many-core systems can remap memory. <bookmark mark='d'/> And "
            "verified kernels such as seL4 prove their page-table code correct, against a model of the MMU that must "
            "itself be trusted."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open problems", font_size=36).to_edge(UP, buff=0.35)
        items = VGroup(
            label(r"1. \ Translation for terabyte memories: \ what replaces the four-level radix tree?", font_size=22,
                  color=WHITE),
            label(r"2. \ When to form and break huge pages: \ TLB misses against bloat and compaction", font_size=22,
                  color=WHITE),
            label(r"3. \ Hot-page detection for tiered memory, \ with bounded overhead and provable accuracy",
                  font_size=22, color=WHITE),
            label(r"4. \ Competitive replacement with hints: \ how much can a predictor help LRU?", font_size=22,
                  color=WHITE),
            label(r"5. \ TLB shootdowns that scale to hundreds of cores", font_size=22, color=WHITE),
            label(r"6. \ A verified hypervisor with nested paging, \ on a weak memory model", font_size=22,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5)
        fit_right(items)
        star = label(r"$\bigstar$ \ the part's research problem takes a small case of the second", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Six open problems. <bookmark mark='a'/> What should replace the four-level radix tree when memories are "
            "measured in terabytes? <bookmark mark='b'/> When should the kernel form huge pages, and when break them, "
            "trading TLB misses against wasted memory and the cost of compaction? <bookmark mark='c'/> How can it "
            "find the hot pages for tiered memory, with bounded overhead and provable accuracy? <bookmark mark='d'/> "
            "How much can a learned predictor improve on LRU, while keeping a guarantee when the predictions are "
            "wrong? <bookmark mark='e'/> How can TLB shootdowns scale to hundreds of cores? <bookmark mark='f'/> And "
            "can a hypervisor with nested paging be verified, on a processor with a weak memory model? <bookmark "
            "mark='g'/> This part's research problem takes a small, computable case of the second."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcdef", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
