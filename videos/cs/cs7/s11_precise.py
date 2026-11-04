from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, STAGES, YES,
                                  PipeFigure, box, fmt, load, mono)


class Precise(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.rule()
        self.stale()

    def card(self):
        card = chapter_card(10, r"Precise exceptions", r"Where exactly was the machine when it stopped?", part=PART)
        with self.voiceover("Chapter ten. Precise exceptions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def problem(self):
        head = label(r"Five instructions, \ one of them fails", font_size=36).to_edge(UP, buff=0.35)
        fig = PipeFigure(width=12.0, stage_w=1.7, h=1.2).move_to(UP * 1.2)
        toks = ["addi a2, a2, 1", "sw a0, 4(s0)", "div a4, a0, a1", "lw a3, 0(s0)", "sw t0, 8(s0)"]
        order = ["WB", "MEM", "EX", "ID", "IF"]
        tk = VGroup(*[fig.token(s, t, CODE) for s, t in zip(order[::-1], toks[::-1])])
        bad = SurroundingRectangle(tk[2], buff=0.08, color=NO)
        q = VGroup(
            label(r"the divide, \ in EX, \ finds its divisor is zero", font_size=24, color=NO),
            label(r"older instructions are half done; \ younger ones have started", font_size=24, color=GREY_A),
            label(r"precise: \ every older instruction completes, \ no younger one changes anything, \\ and the saved "
                  r"\texttt{pc} points at the divide", font_size=26, color=HEAD),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Part 6 promised that an exception stops the machine at a precise point. A pipeline makes that hard. "
            "<bookmark mark='a'/> Here five instructions are in flight, and the divide in the execute stage discovers "
            "that its divisor is zero. The store ahead of it is half done, and the store behind it has already been "
            "fetched. <bookmark mark='b'/> A precise exception means: every instruction before the divide finishes, "
            "none after it changes anything, and the machine reports the divide's own address, so that an operating "
            "system could fix the problem and resume exactly there."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fig), FadeIn(tk))
            vo.wait_until("a")
            self.play(Create(bad), FadeIn(q[0]))
            self.play(FadeIn(q[1]))
            vo.wait_until("b")
            self.play(FadeIn(q[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rule(self):
        head = label(r"The rule: \ commit in order, \ at the end", font_size=36).to_edge(UP, buff=0.35)
        steps = VGroup(
            label(r"a fault found in any stage is only \textit{recorded} with the instruction", font_size=24,
                  color=GREY_A),
            label(r"it is \textit{taken} when the instruction reaches WB, \ the point of no return", font_size=24,
                  color=GREY_A),
            label(r"by then every older instruction has written its result, \\ and every younger one is behind it, \ "
                  r"and is flushed", font_size=24, color=YES),
            label(r"nothing a younger instruction did may be visible: \ in Pebble, \ stores happen in MEM, \\ "
                  r"after every older instruction is past the stages that can fault", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.4)
        demo = VGroup(mono("sw   a0, 0(s0)      # done: memory holds 11", 18, YES),
                      mono("div  a2, a0, a1     # a1 = 0: stop here, pc reported", 18, NO),
                      mono("sw   a0, 4(s0)      # never happens", 18, GREY_D)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.08)
        demo.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The trick is to separate noticing a fault from acting on it. <bookmark mark='a'/> A stage that finds a "
            "problem only marks the instruction: this one has failed, and why. <bookmark mark='b'/> The exception is "
            "taken when the marked instruction reaches write-back. By then every older instruction has finished, and "
            "every younger one is still behind it in the pipeline, where it can be flushed. "
            "<bookmark mark='c'/> On Pebble's pipeline, this little program stores eleven, then divides by zero, then "
            "stores again. The pipeline stops at the divide, reports its address, and memory holds the first store but "
            "not the second, exactly as the emulator would. Part 8's out-of-order machine will need a whole new "
            "structure to keep this promise."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(steps[2]))
            vo.wait_until("c")
            self.play(FadeIn(steps[3]), FadeIn(demo))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stale(self):
        head = label(r"Part 6's warning, \ come true", font_size=36).to_edge(UP, buff=0.35)
        code = VGroup(*[mono(t, 19) for t in ("load:   lw   t0, 0(s0)       # its offset: rewritten",
                                              "        add  a1, a1, t0",
                                              "        lw   t1, 0(s1)       # the load, as data",
                                              "        addi t1, t1, 4       # offset + 4",
                                              "        sw   t1, 0(s1)       # back, as code",
                                              "        addi a2, a2, -1",
                                              "        bnez a2, load")]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        code.move_to(UP * 1.0 + LEFT * 1.4)
        res = VGroup(
            label(r"emulator, \ gate-level Pebble: \ 31", font_size=26, color=YES),
            label(r"pipeline, \ branch predicted: \ 26", font_size=26, color=NO),
            label(r"pipeline, \ no prediction: \ 31 \ (by luck)", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 4.2 + UP * 1.0)
        why = VGroup(
            label(r"the predicted \texttt{bnez} lets fetch read \texttt{load} again \ before the \texttt{sw} two "
                  r"instructions ahead has written it", font_size=22, color=GREY_A),
            label(r"real processors promise nothing here \ until the program asks: \ RISC-V's \texttt{fence.i}, \ "
                  r"x86's serializing instructions", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "One promise the pipeline does not keep, and Part 6 warned about it. <bookmark mark='a'/> This is Part 6's "
            "self-modifying array sum: each trip round the loop rewrites the offset in its own load instruction. "
            "<bookmark mark='b'/> The emulator and the gate-level machine get thirty-one. The pipeline, with its branch "
            "predicted, gets twenty-six. <bookmark mark='c'/> The predicted branch sends fetch back to the load before "
            "the store that rewrites it, two instructions ahead, has reached memory, so the pipeline runs the old "
            "instruction. Without prediction, every trip mispredicts, the flush refetches the new word, and the answer "
            "is right by accident. Real processors make no promise about code that rewrites itself until the program "
            "asks for one, with RISC-V's fence instruction or x86's serializing instructions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]))
            vo.wait_until("c")
            self.play(FadeIn(why[0]), FadeIn(res[2]))
            self.play(FadeIn(why[1]))
        self.wait(0.3)
        self.clear_scene()
