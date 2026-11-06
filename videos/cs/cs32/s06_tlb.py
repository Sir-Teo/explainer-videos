from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (HEAD, NO, PART, YES, curve, fit_right, grid_table, load)


class Tlb(VoiceoverScene):
    def construct(self):
        self.card()
        self.ours()
        self.staircase()

    def card(self):
        card = chapter_card(5, r"The TLB", r"How can translation be nearly free?", lit=(1967, 1985),
                            extra=((1967, r"IBM 360/67: \ a TLB"), (1985, r"the 386: \ paging on PCs")), part=PART)
        with self.voiceover("Chapter five. The translation lookaside buffer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ours(self):
        d = load("tlb")
        rows = d["rows"]
        head = label(r"A cache of translations, \ in our MMU", font_size=34).to_edge(UP, buff=0.3)
        base = [r for r in rows if r["quantum"] == 20000]
        tab = grid_table([r"TLB entries", r"misses", r"miss rate", r"memory reads for walks"],
                         [[str(r["size"]), f"{r['misses']:,}".replace(",", "{,}"), f"{r['miss_rate'] * 100:.3f}\\%",
                           f"{r['walk_refs']:,}".replace(",", "{,}")] for r in base],
                         widths=[2.4, 2.4, 2.4, 4.2], row_h=0.46, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.4)
        acc = f"{base[0]['accesses']:,}".replace(",", "{,}")
        qa = [r for r in rows if r["quantum"] == 500]
        f16, a16 = qa[0], qa[1]
        f64, a64 = qa[2], qa[3]
        lines = VGroup(
            label(rf"the Job as \texttt{{tok | job}} on {d['bytes']:,} bytes".replace(",", "{,}") +
                  rf": \ {acc} translations, \ every fetch, \ load and store", font_size=20, color=WHITE),
            label(r"16 entries cover the working set: \ one walk in eleven thousand accesses", font_size=20,
                  color=YES),
            label(rf"switching every 500 instructions flushes the TLB {f16['flushes']} times: \ {f64['misses']} misses "
                  rf"with 64 entries; \ tagged with an \textbf{{ASID}}, \ {a64['misses']}", font_size=20, color=HEAD),
            label(r"real TLBs: \ 64 entries in the first level, \ 1{,}536 in the second, \ tags called PCIDs or ASIDs",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.16).next_to(tab, DOWN, buff=0.4)
        for n_ in lines:
            if n_.width > 13.2:
                n_.scale_to_fit_width(13.2)
        del a16
        with self.voiceover(
            "A walk costs two extra memory reads in our machine, and up to five on a modern one, for every single "
            "access. The fix is a small cache of recent translations, the translation lookaside buffer, which IBM's "
            "360 model 67 had in 1967. <bookmark mark='a'/> We ran the Job as two processes under paged PebbleOS, with "
            "TLBs of different sizes. <bookmark mark='b'/> With four entries, three and a half percent of accesses "
            "miss and need a walk. With eight, under one percent. With sixteen, one access in eleven thousand: the "
            "working set of both programs fits. <bookmark mark='c'/> But every context switch writes a new page-table "
            "root, and our hardware then flushes the TLB. Switching every five hundred instructions, the misses rise "
            "eightfold. Tag each entry with the address space it belongs to, an address-space identifier, and the "
            "entries survive the switch: forty-three misses instead of five hundred and eight. <bookmark mark='d'/> "
            "Real processors have two levels of TLB, with tags, which x86 calls process-context identifiers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def staircase(self):
        d = load("staircase")
        rows = d["rows"]
        head = label(r"The TLB staircase, \ on this machine", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 17, 2], y_range=[0, 2.5, 0.5], x_length=6.8, y_length=4.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        xt = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.c2p(math.log2(n), 0), DOWN, buff=0.08)
                      for n, t in ((1, "1"), (64, "64"), (1024, "1K"), (16384, "16K"), (131072, "128K"))])
        yt = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.c2p(0, math.log10(v)), LEFT, buff=0.08)
                      for v, t in ((1, "1"), (10, "10"), (100, "100"))])
        xl = label(r"pages touched, \ one cache line each", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"ns per access \ (log)", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        c4 = curve(ax, [math.log2(n) for n, _, _ in rows], [math.log10(a) for _, a, _ in rows], NO)
        c2 = curve(ax, [math.log2(n) for n, _, _ in rows], [math.log10(b) for _, _, b in rows], YES)
        k4 = label(r"4 KiB pages", font_size=18, color=NO).move_to(ax.c2p(13.0, 2.2))
        k2 = label(r"2 MiB pages", font_size=18, color=YES).move_to(ax.c2p(15.0, 1.2))
        by = {n: (a, b) for n, a, b in rows}
        notes = VGroup(
            label(rf"up to 64 pages: \ {by[64][0]:.1f} ns, \ all in the first TLB", font_size=20, color=WHITE),
            label(rf"past 64: \ {by[128][0]:.1f} ns: \ the second-level TLB", font_size=20, color=GREY_A),
            label(rf"65{{,}}536 pages: \ {by[65536][0]:.0f} ns with 4 KiB pages, \\ {by[65536][1]:.0f} with "
                  r"2 MiB pages", font_size=20, color=NO),
            label(r"the same cache lines both times: \\ the difference is the walks", font_size=20, color=YES),
            label(r"databases and VMs ask for huge pages; \\ Linux makes them automatically \ (THP)", font_size=20,
                  color=HEAD),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "On this machine we can watch the TLB from outside. <bookmark mark='a'/> A program follows a chain of "
            "pointers through more and more pages, touching one cache line in each, and we time each step. <bookmark "
            "mark='b'/> Up to sixty-four pages, each step takes under two nanoseconds: every translation is in the "
            "first-level TLB. <bookmark mark='c'/> Past sixty-four, the time jumps: the second-level TLB is slower. "
            "<bookmark mark='d'/> Far past it, the steps climb as walks begin, and the caches themselves fill. At "
            "sixty-five thousand pages, a step takes about a hundred nanoseconds. <bookmark mark='e'/> Now repeat with "
            "two-mebibyte pages. The program touches exactly the same cache lines, but each TLB entry now covers five "
            "hundred and twelve times more memory, and the step falls to under sixty nanoseconds. <bookmark "
            "mark='f'/> That is why databases and virtual machines ask for huge pages, and why Linux builds them "
            "automatically where it can."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(c4), FadeIn(k4), run_time=2.0)
            for mk, n_ in zip("bcd", notes[:3]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
            vo.wait_until("e")
            self.play(Create(c2), FadeIn(k2), FadeIn(notes[3]), run_time=2.0)
            vo.wait_until("f")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()
