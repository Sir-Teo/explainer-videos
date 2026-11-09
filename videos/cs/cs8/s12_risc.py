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
                      label("implementation-dependent latency; \\ direct hardware or microcode", font_size=22, color=GREY_A)).arrange(
            DOWN, buff=0.15)
        risc = VGroup(label(r"RISC \ (IBM 801, \ Berkeley RISC, \ Stanford MIPS)", font_size=26, color=YES),
                      label(r"simple instructions: \ more of them", font_size=22, color=GREY_A),
                      label("pipelined throughput differs from each operation latency", font_size=22, color=GREY_A)).arrange(
            DOWN, buff=0.15)
        cols = VGroup(cisc, risc).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.3)
        arrows = VGroup(Arrow(cisc.get_top(), law[2].get_bottom(), buff=0.15, color=INF, stroke_width=3),
                        Arrow(risc.get_top(), law[4].get_bottom(), buff=0.15, color=YES, stroke_width=3))
        who = label(r"John Cocke (IBM, \ 1970s); \ David Patterson and David Ditzel (1980); \ John Hennessy (1981)",
                    font_size=22, color=HIST).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Return to execution time: instruction count times cycles per instruction times clock period. <bookmark "
            "mark='a'/> Rich instructions can express more work per architectural instruction, reducing the count "
            "for some programs. Their implementation may use direct hardware or microcode; not every complex "
            "instruction is slow or microcoded. <bookmark mark='b'/> RISC projects emphasized simpler operations, "
            "regular encoding and efficient pipelines. The goal of starting or completing one operation per cycle "
            "is a throughput goal, not a claim that every load, divide or other instruction has one-cycle latency. "
            "<bookmark mark='c'/> Compiler quality, memory behavior and implementation choices affect all three "
            "factors in the equation, so instruction-set labels alone do not determine performance. <bookmark "
            "mark='d'/> IBM 801, Berkeley RISC and Stanford MIPS are influential examples. Their lessons concern "
            "measured workload and implementation trade-offs, rather than a universal rule that fewer instructions "
            "or simpler instructions must always win."
        ) as vo:
            self.play(FadeIn(head))
            self.play(Write(law))
            vo.wait_until("a")
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
        x86 = VGroup(mono("cmp  ecx, [rax+4]", 22, color=INF),
                     mono("jne  next", 22, color=INF)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        arr = MathTex(r"\longrightarrow", font_size=40, color=GREY_C)
        row = VGroup(ex, arr, x86).arrange(RIGHT, buff=0.4).move_to(DOWN * 0.6)
        fold = label(rf"{d['foldable_loads']:,} of {d['loads']:,} loads: local use/death candidates \\ "
                     r"compare plus jump still counts as two; no instruction savings established",
                     font_size=23, color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "This is the Job's dynamic instruction mix on Pebble, not a measured translation to another ISA. "
            "<bookmark mark='a'/> Its arithmetic, branches, loads and jumps dominate the recorded chapter. "
            "<bookmark mark='b'/> An x86 compare can read a memory operand directly, but the conditional jump still "
            "remains. Our Pebble load followed by a combined compare-and-branch can therefore map to a memory "
            "compare plus a jump: two architectural instructions, not one. <bookmark mark='c'/> The trace heuristic "
            "finds ninety thousand seven hundred twenty-six loads whose result feeds the next instruction and soon "
            "becomes dead. That is about fifty-nine percent of the loads. It is a local use pattern, not a count of "
            "legal folded x86 instructions or an eleven-percent instruction reduction. Addressing, flags, branches, "
            "register allocation and actual code generation must be included in such a comparison."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(b) for b in bar], lag_ratio=0.2))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(ex))
            self.play(GrowFromCenter(arr), FadeIn(x86))
            vo.wait_until("c")
            self.play(FadeIn(fold))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inside(self):
        head = label("Architectural instructions and internal operations", font_size=38).to_edge(UP, buff=0.35)
        x86 = mono("add  [rbx+8], eax", 26, color=INF)
        uops = VGroup(mono("load   tmp  <- [rbx+8]", 22, color=YES), mono("add    tmp  <- tmp + eax", 22, color=YES),
                      mono("store  [rbx+8] <- tmp", 22, color=YES)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        row = VGroup(x86, MathTex(r"\xrightarrow{\text{decode}}", font_size=40, color=GREY_C), uops).arrange(
            RIGHT, buff=0.5).move_to(UP * 0.8)
        facts = VGroup(
            label("many x86 implementations decode instructions into internal micro-operations",
                  font_size=24, color=GREY_A),
            label("out-of-order designs can rename and schedule implementation-specific micro-ops", font_size=24,
                  color=YES),
            label("load-operation micro-fusion differs from compare-branch macro-fusion", font_size=24, color=GREY_A),
            label("x86 encodings: \\ 1 to 15 bytes; \\ some RISC ISAs also mix lengths", font_size=24,
                  color=NO),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Many modern x86 implementations decode architectural instructions into internal micro-operations. "
            "<bookmark mark='a'/> This conceptual read-modify-write example separates memory reading, arithmetic "
            "and memory writing; exact micro-operations and flags behavior depend on the implementation. <bookmark "
            "mark='b'/> An out-of-order design can rename and schedule those internal operations. They are not "
            "literally a separate RISC instruction set, and not every x86 processor uses the same organization. "
            "<bookmark mark='c'/> Some designs fuse a load with an operation for part of the pipeline; macro-fusion "
            "of a compare and conditional branch is a different mechanism. Architectural instruction counts, "
            "reorder-buffer entries and execution operations can therefore differ. <bookmark mark='d'/> Encoding is "
            "another independent choice. x86 uses variable-length encodings; some RISC ISAs also mix lengths, "
            "including Thumb and compressed RISC-V. A base instruction-set category does not specify every pipeline "
            "detail."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(row[0]), FadeIn(row[1]), LaggedStart(*[FadeIn(u) for u in uops], lag_ratio=0.3),
                      FadeIn(facts[0]))
            vo.wait_until("a")
            for mk, f in zip("bcd", facts[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(f))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def today(self):
        head = label(r"Where the instruction sets went", font_size=36).to_edge(UP, buff=0.35)
        rows = VGroup(
            label("x86 compatibility: \\ extensive, \\ but mode and extension dependent", font_size=24, color=INF),
            label(r"Arm: \ Acorn's RISC of 1985 \ (Sophie Wilson, \ Steve Furber): \ phones, \ then Apple's Macs "
                  r"(2020)", font_size=24, color=YES),
            label("RISC-V: \\ open ISA; \\ no ISA royalty does not mean no other costs", font_size=24,
                  color=DATA),
            label(r"MIPS and its descendants: \ routers, \ game consoles, \ textbooks", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.2)
        award = label(r"2017 Turing Award: \ Hennessy and Patterson, \ for the quantitative approach to architecture",
                      font_size=24, color=HEAD).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "Instruction sets preserve software investments while implementations evolve. <bookmark mark='a'/> x86 "
            "compatibility is extensive, but availability depends on execution mode, extensions and "
            "operating-system support; not literally every instruction from 1978 runs unchanged in every modern "
            "mode. <bookmark mark='b'/> Arm designs span many implementations and markets, with distinct "
            "instruction-set states and encoding choices. <bookmark mark='c'/> RISC-V provides an open ISA that can "
            "be implemented without an ISA license royalty. That does not remove every other IP, implementation or "
            "compliance cost. <bookmark mark='d'/> MIPS and other architectures also shaped processors and teaching "
            "systems. Across these families, evaluate the generated program and the specific implementation using "
            "instruction counts, timing and resource measurements, rather than treating RISC or CISC as a complete "
            "performance prediction."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
                if mk == "a":
                    vo.wait_until(mk)
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(award))
        self.wait(0.3)
        self.clear_scene()
