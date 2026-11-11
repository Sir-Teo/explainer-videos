from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, bar_chart, box,
                                  fmt, load)


class Dram(VoiceoverScene):
    def construct(self):
        self.card()
        self.inside()
        self.rowbuffer()
        self.beyond()

    def card(self):
        card = chapter_card(13, r"Inside DRAM", r"Why is main memory slow, \ and when is it fast?", lit=(1966,),
                            extra=((1966, r"Dennard's one-transistor cell"),), part=PART)
        with self.voiceover(
            "Chapter thirteen. Inside DRAM."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def inside(self):
        head = label(r"A DRAM bank: \ rows of capacitors, \ one row buffer", font_size=34).to_edge(UP, buff=0.35)
        rows = VGroup(*[Rectangle(width=6.0, height=0.28, stroke_color=GREY_C, stroke_width=1) for _ in range(8)])
        rows.arrange(DOWN, buff=0.04).move_to(UP * 0.7 + LEFT * 2.0)
        buf = Rectangle(width=6.0, height=0.4, stroke_color=HEAD, stroke_width=2.5, fill_color=HEAD,
                        fill_opacity=0.15).next_to(rows, DOWN, buff=0.3)
        bl = label(r"row buffer \ (8 KiB)", font_size=20, color=HEAD).next_to(buf, DOWN, buff=0.1)
        steps = VGroup(
            label("\\textit{activate}: \\ sense and restore a row; \\ assigned $t_{RCD}=14$ ns", font_size=22,
                  color=DATA),
            label("\\textit{read}: \\ select columns; \\ assigned $t_{CAS}=14$ ns", font_size=22, color=YES),
            label("\\textit{precharge}: \\ prepare bitlines; \\ assigned $t_{RP}=14$ ns", font_size=22,
                  color=NO),
            label("refresh interval depends on device, temperature and mode", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35).shift(UP * 0.3)
        with self.voiceover(
            "A DRAM bank contains arrays of cells and sense amplifiers that hold an open row. This diagram uses an "
            "illustrative eight-kibibyte row and assigned timing values. <bookmark mark='a'/> Activation senses a "
            "row's small charge differences and restores the cells while holding their values in the sense "
            "amplifiers. <bookmark mark='b'/> A read command selects columns for transfer, subject to the device and "
            "interface timings. <bookmark mark='c'/> To switch rows, the controller observes minimum active-time and "
            "other constraints, closes the row and precharges the bitlines before a new activation. Precharge itself "
            "is not simply a delayed cache-style write-back. <bookmark mark='d'/> Refresh restores charge "
            "periodically, with intervals depending on device, temperature and mode. The fourteen-nanosecond numbers "
            "and sixty-four-millisecond example are teaching choices, not universal end-to-end memory timings."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows), FadeIn(buf), FadeIn(bl))
            vo.wait_until("a")
            hl = rows[3].copy().set_fill(DATA, opacity=0.5)
            self.play(FadeIn(hl), FadeIn(steps[0]))
            self.play(hl.animate.move_to(buf), run_time=1.0)
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), FadeOut(hl))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
        self.wait(0.3)
        self.clear_scene()

    def rowbuffer(self):
        d = load("dram")["rows"]
        head = label(r"Row-buffer hits, \ by access pattern", font_size=36).to_edge(UP, buff=0.35)
        keys = ["sequential", "stride 4 KB", "random"]
        ch = bar_chart([100 * d[k] for k in keys], [r"sequential", r"every 4 KiB", r"random"], [YES, CTRL, NO],
                       height=3.4, bar_w=1.4, gap=1.4, font_size=22, fmt_=lambda v: rf"{v:.0f}\%").move_to(DOWN * 0.3)
        cap = note(r"assigned model: \ 8 banks, \ 8 KiB rows, \ last row left open", font_size=18).next_to(ch, UP, buff=0.3)
        punch = label("row hits avoid a row switch; \\ full timing and scheduling still matter", font_size=24,
                      color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The open row makes access history matter inside DRAM. This toy model has eight banks, fixed "
            "eight-kibibyte rows and a specified address-to-bank mapping, and leaves the last row open. <bookmark "
            "mark='a'/> Sequential line addresses give the first hit fraction. <bookmark mark='b'/> A four-kibibyte "
            "stride gives the second. <bookmark mark='c'/> Seeded random addresses give the third. These are "
            "simulated row-buffer hits, not measured cache hits on the host. <bookmark mark='d'/> A row hit can "
            "avoid closing and activating a different row, but real time also depends on bank parallelism, "
            "controller scheduling, bus transfers, refresh and timing constraints. A universal one-third access time "
            "cannot be inferred by adding three illustrative fourteen-nanosecond constants."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ch[0]))
            for mk, k in zip("abc", range(3)):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(GrowFromEdge(ch.bars[k], DOWN), FadeIn(ch.vals[k]), FadeIn(ch.names[k]))
                if mk == 'a':
                    vo.wait_until(mk)
            vo.wait_until("d")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()

    def beyond(self):
        head = label(r"Wider, \ closer, \ and translated", font_size=36).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"DDR5: \ two 32-bit channels per module, \ 16 or 32 banks per chip", font_size=24, color=GREY_A),
            label("HBM: \\ stacked DRAM and wide interfaces; \\ generation and accelerator choices vary", font_size=24, color=YES),
            label("virtual-memory systems: \\ address translation and TLBs \\ (Part 32)",
                  font_size=24, color=CTRL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 0.1)
        with self.voiceover(
            "Memory interfaces and packaging change while the basic charge-storage idea remains. <bookmark "
            "mark='a'/> A common non-ECC DDR5 DIMM has two thirty-two-bit subchannels; widths, bank organizations "
            "and error-protection overhead depend on the device and module. <bookmark mark='b'/> High-bandwidth "
            "memory stacks dies near a processor and uses a wide interface, with details varying by HBM generation "
            "and package. Many accelerators use HBM; others use different memory systems. <bookmark mark='c'/> "
            "Systems with virtual memory translate virtual addresses to physical addresses and cache translation "
            "information in TLBs. Bare-metal and other addressing modes need not perform the same translation. The "
            "measured staircase motivates a translation investigation, but does not alone prove its causes. Part 32 "
            "develops those mechanisms."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abc", items):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()
