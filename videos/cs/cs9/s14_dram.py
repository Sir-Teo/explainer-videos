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
        with self.voiceover("Chapter thirteen. Inside DRAM."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def inside(self):
        head = label(r"A DRAM bank: \ rows of capacitors, \ one row buffer", font_size=34).to_edge(UP, buff=0.35)
        rows = VGroup(*[Rectangle(width=6.0, height=0.28, stroke_color=GREY_C, stroke_width=1) for _ in range(8)])
        rows.arrange(DOWN, buff=0.04).move_to(UP * 0.7 + LEFT * 2.0)
        buf = Rectangle(width=6.0, height=0.4, stroke_color=HEAD, stroke_width=2.5, fill_color=HEAD,
                        fill_opacity=0.15).next_to(rows, DOWN, buff=0.3)
        bl = label(r"row buffer \ (8 KB)", font_size=20, color=HEAD).next_to(buf, DOWN, buff=0.1)
        steps = VGroup(
            label(r"\textit{activate} \ (RAS): \ copy a whole row into the row buffer \ $\approx$ 14 ns", font_size=22,
                  color=DATA),
            label(r"\textit{read} \ (CAS): \ take a column from the buffer \ $\approx$ 14 ns", font_size=22, color=YES),
            label(r"\textit{precharge}: \ write the row back, \ ready the bank \ $\approx$ 14 ns", font_size=22,
                  color=NO),
            label(r"each bit a capacitor that leaks: \ every row refreshed every 64 ms", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35).shift(UP * 0.3)
        with self.voiceover(
            "Why is DRAM slow? Part 5 built its cell: one transistor and one capacitor per bit, Robert Dennard's design "
            "of 1966. Billions of them are arranged in banks, each a grid of rows. <bookmark mark='a'/> To read "
            "anything, the bank first activates a row: the charge of every cell in it, eight kilobytes' worth, is "
            "sensed and copied into a row buffer. That takes about fourteen nanoseconds. <bookmark mark='b'/> Then a "
            "column is read out of the buffer: another fourteen or so. <bookmark mark='c'/> To read a different row, "
            "the bank must first write the buffer back and precharge: fourteen more. <bookmark mark='d'/> And because "
            "the capacitors leak, every row must be read and rewritten every sixty-four milliseconds, refresh, which "
            "Part 5's Rowhammer chapter exploited."
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
        ch = bar_chart([100 * d[k] for k in keys], [r"sequential", r"every 4 KB", r"random"], [YES, CTRL, NO],
                       height=3.4, bar_w=1.4, gap=1.4, font_size=22, fmt_=lambda v: rf"{v:.0f}\%").move_to(DOWN * 0.3)
        cap = note(r"8 banks, \ 8 KB rows, \ the row left open after each access", font_size=18).next_to(ch, UP, buff=0.3)
        punch = label(r"a row-buffer hit skips activate and precharge: \ about a third of the time", font_size=24,
                      color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So DRAM has its own cache, the open row. A memory controller that leaves a row open after reading it "
            "gets the next access to the same row with only the column read. <bookmark mark='a'/> Reading in order, "
            "ninety-nine percent of accesses hit the open row. <bookmark mark='b'/> Jumping four kilobytes each time, "
            "half do. <bookmark mark='c'/> At random, essentially none. <bookmark mark='d'/> The difference is the "
            "activate and precharge, about two thirds of a random access's time inside the chip. Locality pays all "
            "the way down."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ch[0]))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(GrowFromEdge(ch.bars[k], DOWN), FadeIn(ch.vals[k]), FadeIn(ch.names[k]))
            vo.wait_until("d")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()

    def beyond(self):
        head = label(r"Wider, \ closer, \ and translated", font_size=36).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"DDR5: \ two 32-bit channels per module, \ 16 or 32 banks per chip", font_size=24, color=GREY_A),
            label(r"HBM: \ DRAM dies stacked beside the processor, \ 1024 wires per stack: \ the memory of every AI "
                  r"accelerator \ (\textit{AI, Built} 17)", font_size=24, color=YES),
            label(r"every address is virtual: \ translated through page tables, \ cached in the TLB \ (Part 32)",
                  font_size=24, color=CTRL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 0.1)
        with self.voiceover(
            "Modern memory keeps the cell and changes the plumbing. <bookmark mark='a'/> A DDR5 module splits into two "
            "channels with many more banks, so more rows can be open at once. <bookmark mark='b'/> High-bandwidth "
            "memory stacks DRAM dies on top of each other, beside the processor, joined by a thousand wires per stack "
            "instead of sixty-four: the memory of every large AI accelerator, as AI, Built's seventeenth part showed. "
            "<bookmark mark='c'/> And one more lookup hides in every access: the address a program uses is virtual, "
            "and must be translated to a physical one through page tables, with its own small cache, the TLB. That "
            "was the extra climb at the top of the staircase. Part 32 builds it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abc", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
