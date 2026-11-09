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
            "Divide the datapath into five roles. <bookmark mark='a'/> Fetch the instruction, decode and read "
            "registers, execute, access data memory, and write back. An ideal simple instruction advances one stage "
            "each cycle, including stages where it has no active work. A load, add and branch use different resources. "
            "Stalls and the later multi-cycle divider break that one-cycle-per-stage schedule. <bookmark mark='b'/> "
            "This resembles the classic textbook RISC pipeline, with historical examples including MIPS and SPARC. "
            "Pebble is an educational model; it does not reproduce all their implementation details or instruction-set "
            "behavior."
        ) as vo:
            self.play(FadeIn(head))
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
            "Watch independent simple instructions move through the ideal pipeline. <bookmark mark='a'/> Instruction "
            "one begins fetch in cycle one and reaches write-back in cycle five. Instruction two follows one cycle "
            "later. Read down a column to see different instructions in flight together. <bookmark mark='b'/> The "
            "highlighted column shows that overlap. <bookmark mark='c'/> With no stalls, n such instructions finish in "
            "n plus four cycles. There is one total four-cycle overhead for filling and draining, not four cycles of "
            "each added separately. Thus CPI is one plus four over n and approaches one for a long stream. "
            "Dependencies, branches, memory conflicts and multi-cycle operations add to this ideal schedule; the later "
            "divider is one example."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pc.heads), FadeIn(cl), FadeIn(VGroup(*pc.rows.values())), FadeIn(rl))
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
            label('finite tests against the emulator, on selected programs and configurations: \\\\ final registers, memory, output and instruction counts agree', font_size=24, color=YES),
            label(r"and an exact account of time: \\ cycles $=$ instructions $+\ 4\ +$ the bubbles it reports",
                  font_size=26, color=HEAD),
            label(r"one difference, \ on purpose: \ code that rewrites itself a few instructions ahead \\ goes stale, "
                  r"\ as Part 6 warned \ (chapter 10)", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.1)
        with self.voiceover(
            "The implementation is a functional cycle model, not a gate-level physical pipeline. <bookmark mark='a'/> "
            "For selected programs and configurations, the tests compare its final registers, memory, output and "
            "stopping address with the instruction emulator. The charts record which modeled instruction occupies each "
            "stage. <bookmark mark='b'/> They exercise dependencies, branches and exceptions, and use modeled multiply "
            "and divide latencies motivated by earlier circuits. These are finite tests, not an all-program proof or "
            "timing certification. The simulator lets us explain every counted stall while keeping its hardware "
            "assumptions visible. <bookmark mark='c'/> One deliberate difference is stale self-modifying code, "
            "examined in chapter ten."
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
