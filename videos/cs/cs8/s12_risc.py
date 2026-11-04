from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, KIND_COLOR, NO, PART, YES, box,
                                  fmt, load, mono)


class Risc(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.mix()
        self.inside()
        self.today()

    def card(self):
        card = chapter_card(11, r"RISC and CISC", r"Should instructions be simple, \ or powerful?", lit=(1980, 2017),
                            extra=((1980, r"Patterson and Ditzel"), (2017, r"Turing Award: \ Hennessy, \ Patterson")),
                            part=PART)
        with self.voiceover("Chapter eleven. RISC and CISC."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        head = label(r"The argument", font_size=40).to_edge(UP, buff=0.35)
        law = MathTex(r"T", r"=", r"N", r"\times", r"\text{CPI}", r"\times", r"t_{\text{clk}}", font_size=48).move_to(
            UP * 1.7)
        cisc = VGroup(label(r"CISC \ (VAX, \ 1977)", font_size=26, color=INF),
                      label(r"powerful instructions: \ fewer of them", font_size=22, color=GREY_A),
                      label(r"each takes many cycles, \ through microcode", font_size=22, color=GREY_A)).arrange(
            DOWN, buff=0.15)
        risc = VGroup(label(r"RISC \ (IBM 801, \ Berkeley RISC, \ Stanford MIPS)", font_size=26, color=YES),
                      label(r"simple instructions: \ more of them", font_size=22, color=GREY_A),
                      label(r"each one cycle, \ pipelined, \ a fast clock", font_size=22, color=GREY_A)).arrange(
            DOWN, buff=0.15)
        cols = VGroup(cisc, risc).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.3)
        arrows = VGroup(Arrow(cisc.get_top(), law[2].get_bottom(), buff=0.15, color=INF, stroke_width=3),
                        Arrow(risc.get_top(), law[4].get_bottom(), buff=0.15, color=YES, stroke_width=3))
        who = label(r"John Cocke (IBM, \ 1970s); \ David Patterson and David Ditzel (1980); \ John Hennessy (1981)",
                    font_size=22, color=HIST).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Pebble has a reduced instruction set: every instruction does one simple thing, and only loads and "
            "stores touch memory. That was once a heresy. <bookmark mark='a'/> Recall the iron law from Part 7: time "
            "is instructions, times cycles per instruction, times the clock period. <bookmark mark='b'/> The "
            "machines of the 1970s, like Digital's VAX, attacked the first factor. They offered rich instructions, "
            "adding memory to memory, even evaluating a polynomial in one instruction, so programs needed fewer of "
            "them. Each was run by microcode, a little program inside the processor, and took many cycles. <bookmark "
            "mark='c'/> John Cocke at IBM noticed that compilers hardly used the rich instructions. His 801 project, "
            "and then David Patterson's RISC at Berkeley and John Hennessy's MIPS at Stanford, attacked the other "
            "two factors instead: simple instructions, each one cycle in a pipeline, with a fast clock. More "
            "instructions, but each far cheaper. <bookmark mark='d'/> Patterson and Ditzel's paper, The Case for the "
            "Reduced Instruction Set Computer, appeared in 1980, and the argument raged for a decade."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(law))
            vo.wait_until("b")
            self.play(FadeIn(cisc), GrowArrow(arrows[0]))
            vo.wait_until("c")
            self.play(FadeIn(risc), GrowArrow(arrows[1]))
            vo.wait_until("d")
            self.play(FadeIn(who))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mix(self):
        d = load("risc")
        head = label(r"The Job, \ as a RISC program", font_size=36).to_edge(UP, buff=0.35)
        n = d["instructions"]
        order = [("alu", r"arithmetic"), ("branch", r"branches"), ("load", r"loads"), ("jump", r"jumps"),
                 ("store", r"stores")]
        bar = VGroup()
        x = 0
        W = 11.0
        for k, nm in order:
            w = W * d["mix"][k] / n
            r = Rectangle(width=w, height=0.8, stroke_color=BG, stroke_width=2, fill_color=KIND_COLOR[k],
                          fill_opacity=0.75).move_to([x + w / 2, 0, 0])
            t = label(rf"{nm} \\ {100 * (d['mix'][k] / n):.0f}\%", font_size=20 if w > 1 else 14, color=WHITE).move_to(r)
            if w < 0.8:
                t = label(rf"{nm} {100 * (d['mix'][k] / n):.1f}\%", font_size=16, color=KIND_COLOR[k]).next_to(r, UP, buff=0.1)
            bar.add(VGroup(r, t))
            x += w
        bar.move_to(UP * 1.2)
        cap = note(rf"{n:,} instructions run; \ {d['static_instructions']} in the program, \ {d['code_bytes']} bytes",
                   font_size=20).next_to(bar, UP, buff=0.35)
        ex = VGroup(mono("lw   t1, 4(t0)", 22), mono("bne  t1, a1, next", 22)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        x86 = mono("cmp  ecx, [rax+4]  ; one x86 instruction", 22, color=INF)
        arr = MathTex(r"\longrightarrow", font_size=40, color=GREY_C)
        row = VGroup(ex, arr, x86).arrange(RIGHT, buff=0.4).move_to(DOWN * 0.6)
        fold = label(rf"{d['foldable_loads']:,} of the {d['loads']:,} loads \ ({100 * (d['foldable_loads'] / d['loads']):.0f}\%) "
                     rf"feed one instruction and die: \ x86 would need {100 * (d['foldable_loads'] / n):.0f}\% fewer "
                     r"instructions", font_size=24, color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "What does the Job look like as a RISC program? <bookmark mark='a'/> Over its first chapter: about a "
            "third arithmetic, a third branches, a fifth loads, an eighth jumps, and hardly any stores. <bookmark "
            "mark='b'/> A CISC machine like x86 can take an operand straight from memory. The scan loop's load of an "
            "entry's length, used once by the comparison and then dead, would be part of a single x86 compare. "
            "<bookmark mark='c'/> Counting over the whole trace, fifty-nine percent of the Job's loads are used "
            "exactly this way, so an x86 version would need about eleven percent fewer instructions. That is the "
            "CISC advantage, measured: real, and modest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bar], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(ex))
            self.play(GrowFromCenter(arr), FadeIn(x86))
            vo.wait_until("c")
            self.play(FadeIn(fold))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inside(self):
        head = label(r"CISC outside, \ RISC inside", font_size=38).to_edge(UP, buff=0.35)
        x86 = mono("add  [rbx+8], eax", 26, color=INF)
        uops = VGroup(mono("load   tmp  <- [rbx+8]", 22, color=YES), mono("add    tmp  <- tmp + eax", 22, color=YES),
                      mono("store  [rbx+8] <- tmp", 22, color=YES)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        row = VGroup(x86, MathTex(r"\xrightarrow{\text{decode}}", font_size=40, color=GREY_C), uops).arrange(
            RIGHT, buff=0.5).move_to(UP * 0.8)
        facts = VGroup(
            label(r"since the Pentium Pro (1995), \ x86 cores translate each instruction into micro-operations",
                  font_size=24, color=GREY_A),
            label(r"the out-of-order core renames and schedules the micro-ops: \ a RISC machine", font_size=24,
                  color=YES),
            label(r"and fuses some back together: \ a compare and its branch become one", font_size=24, color=GREY_A),
            label(r"the cost of x86 today: \ a harder decoder \ (variable lengths, \ 1 to 15 bytes)", font_size=24,
                  color=NO),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The argument ended in a merger. <bookmark mark='a'/> Since Intel's Pentium Pro in 1995, x86 processors "
            "have translated each instruction, as it is decoded, into simple micro-operations. An add to memory "
            "becomes a load, an add, and a store. <bookmark mark='b'/> Everything after the decoder is an "
            "out-of-order RISC machine like ours, renaming and scheduling micro-ops. <bookmark mark='c'/> Modern "
            "decoders even fuse pairs back together: a compare and the branch on it travel through the core as one. "
            "<bookmark mark='d'/> What remains of the old difference is mostly the decoder. x86 instructions range "
            "from one byte to fifteen, so finding where each starts, several at a time, is hard work that a "
            "fixed-length instruction set never needs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(row[0]), FadeIn(row[1]), LaggedStart(*[FadeIn(u) for u in uops], lag_ratio=0.3),
                      FadeIn(facts[0]))
            for mk, f in zip("bcd", facts[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(f))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def today(self):
        head = label(r"Where the instruction sets went", font_size=36).to_edge(UP, buff=0.35)
        rows = VGroup(
            label(r"x86: \ the PC and the server, \ every instruction since 1978 still runs", font_size=24, color=INF),
            label(r"Arm: \ Acorn's RISC of 1985 \ (Sophie Wilson, \ Steve Furber): \ phones, \ then Apple's Macs "
                  r"(2020)", font_size=24, color=YES),
            label(r"RISC-V: \ Berkeley, \ 2010: \ an open instruction set, \ free to implement", font_size=24,
                  color=DATA),
            label(r"MIPS and its descendants: \ routers, \ game consoles, \ textbooks", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.2)
        award = label(r"2017 Turing Award: \ Hennessy and Patterson, \ for the quantitative approach to architecture",
                      font_size=24, color=HEAD).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "Where did the instruction sets go? <bookmark mark='a'/> x86 kept the personal computer and the server, "
            "carrying every instruction since 1978 for compatibility. <bookmark mark='b'/> Arm, a RISC designed at "
            "Acorn in 1985 by Sophie Wilson and Steve Furber, took phones, then tablets, and in 2020 Apple's laptops. "
            "<bookmark mark='c'/> RISC-V, begun at Berkeley in 2010, is an open instruction set that anyone may "
            "implement without a licence; Pebble's design borrows from it. <bookmark mark='d'/> And in 2017 John "
            "Hennessy and David Patterson received the Turing Award, for the quantitative approach to computer "
            "design that this whole act follows: measure, then build."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(award))
        self.wait(0.3)
        self.clear_scene()
