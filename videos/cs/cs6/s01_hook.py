from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.gates import WIRE
from explainer.cs.pebble import isa as I
from videos.cs.cs6.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, box, fmt, gate, load,
                                  say, sci)


class Hook(VoiceoverScene):
    def construct(self):
        self.pieces()
        self.stored()
        self.preview()
        self.plan()

    # ------------------------------------------------------------------
    def pieces(self):
        head = label(r"Five parts of pieces", font_size=40).to_edge(UP, buff=0.4)
        tw = tower(lit=(0, 1, 2), height=4.6).to_edge(LEFT, buff=0.5)
        parts = VGroup(
            VGroup(gate("NAND", size=0.7), label(r"gates \ (Part 3)", font_size=22, color=GREY_A)),
            VGroup(box(1.4, 0.9, r"\text{ALU}", FUNC, 26), label(r"arithmetic \ (Part 4)", font_size=22,
                                                                   color=GREY_A)),
            VGroup(box(1.4, 0.9, r"r_0\ \ldots\ r_{15}", YES, 24), label(r"registers \ (Part 5)", font_size=22,
                                                                         color=GREY_A)),
            VGroup(box(1.4, 0.9, r"\text{memory}", DATA, 24), label(r"memory \ (Part 5)", font_size=22,
                                                                     color=GREY_A)),
        )
        for p in parts:
            p[1].next_to(p[0], DOWN, buff=0.2)
        parts.arrange(RIGHT, buff=0.7).move_to(RIGHT * 1.6 + UP * 0.8)
        cpu = RoundedRectangle(width=8.4, height=2.6, corner_radius=0.2, stroke_color=HEAD, stroke_width=3,
                               fill_color=HEAD, fill_opacity=0.05).move_to(RIGHT * 1.6 + DOWN * 1.35)
        cpu_l = label(r"Pebble-32: \ a computer", font_size=32, color=HEAD).next_to(cpu.get_top(), DOWN, buff=0.2)
        q = label(r"what turns a pile of parts into a machine that runs programs?", font_size=28,
                  color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "For five parts we have been collecting pieces. <bookmark mark='a'/> Gates, built from switches in Part 3. "
            "Arithmetic in Part 4: adders, multipliers, and an ALU that does ten operations. Registers and memory in "
            "Part 5, the circuits that remember. <bookmark mark='b'/> Each piece works, and each was checked against "
            "a model. But none of them, on its own, computes anything you would call a program. Today they become one "
            "machine: Pebble, a thirty-two-bit processor, built entirely from the gates we already have. "
            "<bookmark mark='c'/> The question for this part is what turns a pile of parts into a machine that runs "
            "programs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tw))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in parts], lag_ratio=0.35), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(cpu), FadeIn(cpu_l))
            self.play(*[p.animate.scale(0.8).move_to(cpu.get_center() + DOWN * 0.3 + RIGHT * (k - 1.5) * 1.95)
                        for k, p in enumerate(parts)], run_time=1.6)
            wires = VGroup(*[Line(parts[k][0].get_right(), parts[k + 1][0].get_left(), color=WIRE, stroke_width=2.5)
                             for k in range(3)])
            self.play(Create(wires), Indicate(tw, color=HEAD, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stored(self):
        d = load("programs")["euclid"]
        head = label(r"The idea: \ the program lives in memory, \ as numbers", font_size=36).to_edge(UP, buff=0.35)
        listing = d["listing"]
        rows = VGroup()
        for k, (a, w, src) in enumerate(listing[:10]):
            y = 2.1 - 0.46 * k
            r = VGroup(MathTex(rf"\texttt{{{a:#06x}}}", font_size=22, color=GREY_B).move_to([-4.6, y, 0]),
                       MathTex(rf"\texttt{{{w:08x}}}", font_size=24, color=DATA).move_to([-2.85, y, 0]),
                       Text(I.disasm(w, a, d["labels"] and {v: k_ for k_, v in d["labels"].items()}),
                            font="DejaVu Sans Mono", font_size=17, color=CODE))
            r[2].move_to([-1.6, y, 0], aligned_edge=LEFT)
            rows.add(r)
        mem = SurroundingRectangle(VGroup(*[r[1] for r in rows]), buff=0.15, color=DATA, stroke_width=2)
        ml = label(r"memory", font_size=24, color=DATA).next_to(mem, UP, buff=0.12)
        pc = Arrow(LEFT, RIGHT, color=YES, stroke_width=5, buff=0).scale(0.6)
        pcl = MathTex(r"\text{pc}", font_size=28, color=YES)
        pc_g = VGroup(pcl, pc).arrange(RIGHT, buff=0.1)
        pc_g.next_to(rows[0][0], LEFT, buff=0.25)
        notes = VGroup(label(r"the same memory \\ could hold data", font_size=24, color=GREY_A),
                       label(r"the machine reads, \\ decodes and does \\ one word after another", font_size=24,
                             color=YES)).arrange(DOWN, buff=0.6, aligned_edge=LEFT).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "The answer is an idea from 1945, and it is the subject of this part. <bookmark mark='a'/> The program is "
            "not wired in. It sits in memory, as numbers, beside the data it works on. These words are Part 1's "
            "Euclid, the algorithm that found the greatest common divisor by repeated subtraction, written as Pebble "
            "instructions. <bookmark mark='b'/> A register called the program counter holds the address of the next "
            "instruction. The machine fetches that word, decodes what it asks for, does it, and moves on. "
            "<bookmark mark='c'/> Because the program is just numbers in memory, a machine can load a new one in a "
            "moment, and a program can even read or write programs. That single fact is why one machine can be a "
            "word processor in the morning and a game in the afternoon."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(mem), FadeIn(ml), LaggedStart(*[FadeIn(r[1]) for r in rows], lag_ratio=0.08),
                      run_time=1.6)
            self.play(LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.05),
                      LaggedStart(*[FadeIn(r[2], shift=LEFT * 0.1) for r in rows], lag_ratio=0.08), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(pc_g))
            for k in (1, 2, 3, 4, 5, 3, 4):
                self.play(pc_g.animate.next_to(rows[k][0], LEFT, buff=0.25), Indicate(rows[k][2], color=YES,
                                                                                      scale_factor=1.06),
                          run_time=0.55)
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def preview(self):
        cp = load("cpu")
        job = load("job")
        head = label(r"By the end of this part", font_size=40).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(rf"a 32-bit processor: \ {fmt(cp['gates'])} gates \ and {cp['flip_flops']} flip-flops", font_size=30,
                  color=YES),
            label(r"its own instruction set, \ assembler \ and programs", font_size=30, color=CODE),
            label(r"checked against an emulator: \ 300 random programs, \ every register and byte equal", font_size=28,
                  color=GREY_A),
            label(r"it runs a Turing machine; \ a Turing machine could run it", font_size=30, color=FUNC),
            label(rf"and the Job: \ ${sci(job['corpus']['cycles'], 3)}$ \ cycles \ for thirty novels", font_size=30,
                  color=COST),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is where we are going. <bookmark mark='a'/> A thirty-two-bit processor of about eight thousand gates "
            "and five hundred flip-flops, with its own instruction set, an assembler, and programs written for it. "
            "<bookmark mark='b'/> Every piece is checked: the gate-level machine and a fast emulator run three hundred "
            "random programs and end with every register and every byte of memory equal. <bookmark mark='c'/> It "
            "will run a Turing machine, closing a loop from Part 1, and it will run the Job, the word count over "
            "thirty novels that the series carries from part to part. Version zero is honest and naive, and it costs "
            "a hundred and seven billion cycles."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(facts[0]), FadeIn(facts[1]))
            vo.wait_until("b")
            self.play(FadeIn(facts[2]))
            vo.wait_until("c")
            self.play(FadeIn(facts[3]))
            self.play(FadeIn(facts[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ The Stored-Program Computer", font_size=44).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"ENIAC's cables, \ von Neumann's report, \ and the first stored programs",
            r"an instruction set designed: \ Pebble-32, \ bit by bit, \ beside RISC-V",
            r"the datapath and the control unit, \ built from Parts 3--5 \ and verified",
            r"the assembler, \ first programs, \ memory-mapped devices",
            r"the Job, version 0, \ and the first row of the ledger",
            r"universality closed, \ code as data, \ interrupts, \ and the machine counted",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 6 of Computer Science, Built, the last part of the first act. <bookmark mark='a'/> In this "
            "part: how ENIAC was programmed with cables, and the report that put the program in memory. An "
            "instruction set designed from scratch, bit by bit, and compared with RISC-V. The datapath and the "
            "control unit, built from the circuits of Parts 3 to 5 and verified. The assembler, the first programs, "
            "and devices that live at memory addresses. The Job, version zero, and the first row of the ledger. Then "
            "Pebble and the Turing machine, code that rewrites itself, interrupts, and the whole machine counted."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()

