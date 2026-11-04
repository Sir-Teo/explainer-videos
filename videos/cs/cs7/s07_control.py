from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, STAGE_COLOR,
                                  STAGES, YES, PipeChart, PipeFigure, box, fmt, load, mono)


def reveal(scene, pc, rt=0.25):
    for c in range(pc.ncycles):
        if c in pc.columns:
            scene.play(FadeIn(pc.columns[c]), run_time=rt)


class Control(VoiceoverScene):
    def construct(self):
        self.card()
        self.penalty()
        self.cost()
        self.options()

    def card(self):
        card = chapter_card(6, r"Control hazards", r"What do you fetch before you know where the program goes?",
                            part=PART)
        with self.voiceover("Chapter six. Control hazards."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def penalty(self):
        d = load("charts")["branch"]
        head = label(r"A taken branch, \ discovered in EX", font_size=36).to_edge(UP, buff=0.3)
        pc = PipeChart(d, cw=0.42, ch=0.42, font_size=12, label_size=15, max_rows=13).move_to(UP * 0.2)
        notes = VGroup(
            label(r"fetch keeps going: \ \texttt{pc} $+ 4$, \ $+ 8$, \ \ldots \ \ the branch is decided only in EX",
                  font_size=22, color=GREY_A),
            label(r"taken: \ the two instructions fetched behind it are flushed \ (struck out), \ and fetch restarts at "
                  r"the target", font_size=22, color=NO),
            label(r"each taken branch: \ 2 cycles lost", font_size=26, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The fetch stage must deliver a new instruction every cycle, but which one? After a branch, it depends on "
            "the branch's outcome, which is not known until the branch reaches the execute stage. "
            "<bookmark mark='a'/> The simplest policy is to keep fetching the next instructions in memory, as if the "
            "branch will not be taken. Here a loop branch is taken twice. <bookmark mark='b'/> Each time, by the time "
            "the ALU has decided, two wrong instructions are already in the pipeline: the one after the branch, in "
            "decode, and the one after that, in fetch. They are flushed, turned into bubbles before they change "
            "anything, and fetch restarts at the target. <bookmark mark='c'/> Every taken branch costs two cycles."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pc.heads), FadeIn(VGroup(*pc.rows.values())))
            vo.wait_until("a")
            reveal(self, pc)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cost(self):
        pr = load("predictors")["table"]["the Job, chapter 1"]
        hz = load("hazards")["benchmarks"]["the Job, chapter 1"]["forwarding"]
        frac = pr["branches"] / pr["instructions"]
        taken = pr["rows"]["always taken"]["accuracy"]
        head = label(r"How much it costs", font_size=38).to_edge(UP, buff=0.35)
        eq = MathTex(r"\Delta\text{CPI}", r"=", r"\frac{\text{branches}}{\text{instruction}}", r"\times",
                     r"\frac{\text{mispredicted}}{\text{branch}}", r"\times", r"\text{penalty}", font_size=40).move_to(
            UP * 1.2)
        eq[0].set_color(COST)
        num = MathTex(rf"= {frac:.2f} \times {taken:.2f} \times 2 \approx {frac * taken * 2:.2f}", font_size=40,
                      color=HEAD).next_to(eq, DOWN, buff=0.4)
        notes = VGroup(
            label(rf"in the Job, \ {100 * frac:.0f}\% of instructions are conditional branches, \ "
                  rf"{100 * taken:.0f}\% of them taken", font_size=24, color=GREY_A),
            label(rf"with forwarding but no prediction, \ the Job's CPI is {hz['cpi']:.2f}: \ most of the excess is "
                  r"branches and jumps", font_size=24, color=NO),
            label(r"and the penalty grows with depth: \ a 20-stage pipeline loses 15 or more cycles per mistake",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "How bad is that? <bookmark mark='a'/> The cost per instruction is the fraction of instructions that are "
            "branches, times the fraction of those the machine gets wrong, times the penalty for each mistake. "
            "<bookmark mark='b'/> In the Job, nearly a third of all instructions are conditional branches, and with "
            "predict-not-taken the machine is wrong whenever one is taken, about forty-three percent of the time. Two "
            "cycles each: more than a quarter of a cycle added to every instruction. <bookmark mark='c'/> And the "
            "penalty grows with the pipeline. A branch that is decided ten or fifteen stages after it was fetched "
            "throws away ten or fifteen instructions. This one equation is why branch prediction became one of the "
            "most studied problems in computer architecture."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            self.play(Write(num), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def options(self):
        head = label(r"Three ways out", font_size=38).to_edge(UP, buff=0.35)
        items = VGroup(
            VGroup(label(r"decide earlier", font_size=28, color=DATA),
                   label(r"a comparator in ID: \ a 1-cycle penalty, \\ but a longer ID stage \ and new hazards \\ (the "
                         r"compared values must be forwarded to ID)", font_size=20, color=GREY_A)),
            VGroup(label(r"delay the branch", font_size=28, color=HIST),
                   label(r"MIPS (1985): \ the instruction after a branch \\ \textit{always} runs; \ the compiler fills "
                         r"that slot \\ with useful work, \ or a \texttt{nop}", font_size=20, color=GREY_A)),
            VGroup(label(r"guess", font_size=28, color=YES),
                   label(r"fetch from the predicted target, \\ check the guess in EX, \\ flush only when wrong",
                         font_size=20, color=GREY_A)),
        )
        for it in items:
            it.arrange(DOWN, buff=0.2)
        items.arrange(RIGHT, buff=0.7, aligned_edge=UP).move_to(UP * 0.4)
        slot = VGroup(mono("beq  a0, a1, L", 18), mono("add  a2, a2, 1   # the delay slot: always runs", 18,
                                                      HIST)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        slot.next_to(items[1], DOWN, buff=0.4)
        later = label(r"delay slots fit one 5-stage pipeline exactly, \ and nothing after it: \ deeper and wider "
                      r"machines \\ still had to honour them, \ and RISC-V and ARM left them out", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Designers have three ways out. <bookmark mark='a'/> Decide earlier: move the comparison into the decode "
            "stage, so only one instruction is fetched in vain. That lengthens decode, and the values being compared "
            "now have to be forwarded into decode too. <bookmark mark='b'/> Change the rules: the MIPS architecture of "
            "1985 declared that the instruction after a branch always executes, whichever way the branch goes. The "
            "compiler's job was to put something useful there, and it usually could. <bookmark mark='c'/> But the delay "
            "slot is a fact about one particular five-stage pipeline, baked into the instruction set forever. Deeper "
            "and wider machines still had to honour it, at real cost, and later instruction sets, RISC-V and ARM among "
            "them, left it out. <bookmark mark='d'/> The third way won: guess. Fetch from wherever the branch will "
            "probably go, check the guess when the branch is decided, and pay the penalty only when the guess was "
            "wrong. The rest of this part is about guessing well."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(items[0]))
            vo.wait_until("b")
            self.play(FadeIn(items[1]), FadeIn(slot))
            vo.wait_until("c")
            self.play(FadeIn(later))
            vo.wait_until("d")
            self.play(FadeIn(items[2]), Indicate(items[2][0], color=YES))
        self.wait(0.3)
        self.clear_scene()
