from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, STAGE_COLOR, STAGES,
                                  YES, PipeChart, PipeFigure, box, fmt, load, mono)


class Five(VoiceoverScene):
    def construct(self):
        self.card()
        self.stages()
        self.registers()
        self.chart()
        self.checked()

    def card(self):
        card = chapter_card(3, r"Pebble's five stages", r"Where do you cut a single-cycle machine?", lit=(1985,), extra=((1985, r"the MIPS R2000; IEEE 754"),),
                            part=PART)
        with self.voiceover("Chapter three. Pebble's five stages."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def stages(self):
        head = label(r"Cut the datapath in five", font_size=38).to_edge(UP, buff=0.35)
        fig = PipeFigure(width=12.4, stage_w=1.8, h=1.3).move_to(UP * 1.0)
        jobs = [r"fetch the word at \texttt{pc}; \\ guess the next \texttt{pc}",
                r"decode; \\ read two registers",
                r"the ALU: \\ arithmetic, \ addresses, \\ branch tests",
                r"read or write \\ data memory",
                r"write the result \\ to a register"]
        descs = VGroup(*[label(j, font_size=19, color=STAGE_COLOR[s]).next_to(fig.stage[s], DOWN, buff=0.75)
                         for j, s in zip(jobs, STAGES)])
        hist = label(r"the classic RISC pipeline: \ MIPS R2000 (1985), \ SPARC, \ the textbook machine of Patterson "
                     r"and Hennessy", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Take Part 6's datapath and cut it where the work naturally divides. <bookmark mark='a'/> Instruction "
            "fetch. Instruction decode and register read. Execute, the ALU. Memory access. And write-back. Every "
            "instruction passes through all five, in order, one stage per cycle, even when it has nothing to do in "
            "one of them, as an add has nothing to do in the memory stage. <bookmark mark='b'/> This is the classic "
            "five-stage RISC pipeline of the MIPS R2000 of 1985, of SPARC, and of the textbooks; Pebble's version "
            "follows it almost exactly."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for s, d_ in zip(STAGES, descs):
                self.play(FadeIn(fig.stage[s]), FadeIn(d_), run_time=0.6)
            self.play(FadeIn(VGroup(*fig.reg)), FadeIn(fig.reg_labels))
            vo.wait_until("b")
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def registers(self):
        head = label(r"What the pipeline registers carry", font_size=36).to_edge(UP, buff=0.35)
        fig = PipeFigure(width=12.4, stage_w=1.8, h=1.1).move_to(UP * 1.5)
        carry = [r"\texttt{pc}, \\ the word, \\ the guess",
                 r"\texttt{pc}, \ values $a$, $b$, \\ immediate, \ $rd$, \\ control signals",
                 r"the ALU's result, \\ the value to store, \\ $rd$, \ control",
                 r"the result \\ or the loaded word, \\ $rd$"]
        cl = VGroup(*[label(c, font_size=18, color=CLOCK).next_to(fig.reg[k], DOWN, buff=0.55) for k, c in
                      enumerate(carry)])
        note = VGroup(
            label(r"everything an instruction will still need \ travels with it, \ stage by stage", font_size=24,
                  color=GREY_A),
            label(r"including its control signals: \ decoded once, \ in ID, \ then carried along", font_size=24,
                  color=CTRL),
            label(r"so five instructions, \ each at a different point of its life, \ share one datapath", font_size=24,
                  color=HEAD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The registers between stages are what make this work. <bookmark mark='a'/> At every clock edge each one "
            "captures what its instruction will still need further down the line: the program counter, the operand "
            "values read in decode, the immediate, the number of the register to write, the ALU's result, the loaded "
            "word. <bookmark mark='b'/> Even the control signals travel this way. The control unit of Part 6 decodes an "
            "instruction once, in the decode stage, and the signals ride along with it, each one used in the stage "
            "that needs it. <bookmark mark='c'/> So five instructions, each at a different point in its life, share "
            "one datapath without interfering, as long as none of them needs something another has not finished."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fig))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cl], lag_ratio=0.3), *[Indicate(r, color=CLOCK) for r in fig.reg],
                      run_time=2.0)
            self.play(FadeIn(note[0]))
            vo.wait_until("b")
            self.play(FadeIn(note[1]))
            vo.wait_until("c")
            self.play(FadeIn(note[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chart(self):
        d = load("charts")["ideal"]
        head = label(r"The pipeline chart", font_size=38).to_edge(UP, buff=0.35)
        pc = PipeChart(d, cycles=d["cycles"], cw=0.62, ch=0.5, font_size=17, label_size=17).move_to(DOWN * 0.1)
        rl = label(r"instructions, \ in order \ $\downarrow$", font_size=20, color=GREY_B).next_to(
            pc.heads, LEFT, buff=0.3).align_to(pc, LEFT)
        cl = label(r"clock cycles $\rightarrow$", font_size=20, color=GREY_B).next_to(pc.heads, UP, buff=0.1)
        n = d["retired"]
        res = label(rf"{n} instructions in {d['cycles']} cycles: \ $n + 4$; \ as $n$ grows, \ CPI $\to 1$",
                    font_size=26, color=HEAD).to_edge(DOWN, buff=0.4)
        diag = VGroup(*[pc.cells[(s, c)] for (s, c) in pc.cells if c == 4])
        with self.voiceover(
            "Architects draw a pipeline as a chart: instructions down the side, in program order, and clock cycles "
            "across the top. <bookmark mark='a'/> Each instruction's row shows which stage it is in, cycle by cycle. "
            "The first instruction is fetched in cycle one, decoded in cycle two, and so on; the second follows one "
            "cycle behind. <bookmark mark='b'/> Read the chart down a column and you see the five instructions in "
            "flight at one moment, one in each stage. <bookmark mark='c'/> It takes four cycles to fill the pipeline and "
            "four to drain it, so n instructions take n plus four cycles, and with no hazards the CPI approaches one, "
            "one instruction finished every cycle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pc.heads), FadeIn(cl), FadeIn(VGroup(*pc.rows.values())), FadeIn(rl))
            vo.wait_until("a")
            for c in range(pc.ncycles):
                if c in pc.columns:
                    self.play(FadeIn(pc.columns[c], shift=RIGHT * 0.1), run_time=0.35)
            vo.wait_until("b")
            col = SurroundingRectangle(diag, buff=0.06, color=HEAD)
            self.play(Create(col))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def checked(self):
        head = label(r"Built, \ and checked", font_size=38).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"the pipeline is simulated cycle by cycle: \ five stages, \ four pipeline registers, \\ and the "
                  r"hazard and forwarding logic of the next chapters", font_size=24, color=GREY_A),
            label(r"against Part 6's emulator, \ on random programs, \ with every configuration: \\ the same "
                  r"registers, \ memory, \ output \ and instruction count", font_size=24, color=YES),
            label(r"and an exact account of time: \\ cycles $=$ instructions $+\ 4\ +$ the bubbles it reports",
                  font_size=26, color=HEAD),
            label(r"one difference, \ on purpose: \ code that rewrites itself a few instructions ahead \\ goes stale, "
                  r"\ as Part 6 warned \ (chapter 10)", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.1)
        with self.voiceover(
            "Pebble's pipeline lives in the series' library as a cycle-by-cycle simulator: five stages, four pipeline "
            "registers, and the hazard logic the next chapters build. <bookmark mark='a'/> It is tested the same way as "
            "the gate-level machine: random programs, run on the pipeline and on Part 6's emulator, must end with the "
            "same registers, memory, output and instruction count, in every configuration. "
            "<bookmark mark='b'/> And the time is accounted for exactly. Every cycle beyond the instructions and the "
            "four of filling the pipeline is a bubble, a cycle in which no instruction finished, and the simulator says "
            "which hazard caused each one. <bookmark mark='c'/> One difference from the emulator is deliberate: Part 6's "
            "self-modifying program now goes wrong, as Part 6's problem warned, and chapter ten shows why."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pts[0]))
            vo.wait_until("a")
            self.play(FadeIn(pts[1]))
            vo.wait_until("b")
            self.play(FadeIn(pts[2]))
            vo.wait_until("c")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()
