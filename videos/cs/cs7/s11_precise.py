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
            label('Pebble policy: division by zero faults in EX; RISC-V M defines a result', font_size=24, color=NO),
            label(r"older instructions are half done; \ younger ones have started", font_size=24, color=GREY_A),
            label('precise architectural state: older effects committed; \\\\ faulting instruction obeys its policy; no younger effects committed', font_size=26, color=HEAD),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "An exception needs a precise architectural boundary. <bookmark mark='a'/> In this sketch, Pebble's custom "
            "policy treats division by zero as a fault. The divide is in execute, with older and younger instructions "
            "around it. RISC-V's M extension instead defines a result for division by zero. <bookmark mark='b'/> At a "
            "precise fault, older instructions have committed their architectural effects; the faulting instruction "
            "follows its defined side-effect policy, and younger instructions have not committed theirs. Pebble stops "
            "and reports the divide's address. An operating system could use such a boundary for recovery, but this "
            "simulator implements no operating-system resume mechanism. Cache and predictor effects are a separate "
            "question."
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
            label("no younger architectural effects commit; stores occur in MEM \\\\ only after older instructions pass this model\\'s faulting stages", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.4)
        demo = VGroup(mono("sw   a0, 0(s0)      # done: memory holds 11", 18, YES),
                      mono("div  a2, a0, a1     # a1 = 0: stop here, pc reported", 18, NO),
                      mono("sw   a0, 4(s0)      # never happens", 18, GREY_D)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.08)
        demo.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Separate detecting a fault from committing it. <bookmark mark='a'/> The model records a detected problem "
            "with its instruction. <bookmark mark='b'/> When that instruction reaches write-back, it stops the machine "
            "and discards younger work. Older operations have completed. Stores occur in MEM only after older "
            "instructions have passed the stages where this model can discover a fault. <bookmark mark='c'/> In this "
            "test, the first store commits, the divide faults, and the younger store does not change memory. The final "
            "architectural state and fault address agree with the emulator. That is the tested promise; it does not "
            "erase all microarchitectural traces of younger activity. Out-of-order execution needs additional "
            "machinery to preserve the same boundary."
        ) as vo:
            self.play(FadeIn(head))
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
            label('RISC-V \\texttt{fence.i}: same-hart fetch ordering; \\\\ other harts, migration and x86 need their specified protocols', font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Self-modifying code exposes another boundary. <bookmark mark='a'/> This loop changes the offset in its "
            "own load. <bookmark mark='b'/> The sequential emulator and gate machine give thirty-one, while this "
            "predicted pipeline gives twenty-six. <bookmark mark='c'/> Fetch can revisit the load before the older "
            "store updates its encoding. Without prediction the redirect happens to refetch the newer word; that is "
            "accidental. Instruction-fetch synchronization is ISA-specific. RISC-V fence dot i orders a hart's "
            "already-visible prior stores before its later fetches; other harts and operating-system migration need "
            "broader protocols. x86 also specifies self- and cross-modification rules. Our Pebble model implements no "
            "instruction fence, so this example demonstrates its explicit limitation."
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
