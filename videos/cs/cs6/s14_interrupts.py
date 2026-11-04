from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, NO, PART, YES, box, fmt, load)


class Interrupts(VoiceoverScene):
    def construct(self):
        self.card()
        self.interrupt()
        self.saving()
        self.exceptions()

    def card(self):
        card = chapter_card(13, r"When the world interrupts", r"How does a processor notice a key press?",
                            lit=(1954,), part=PART)
        with self.voiceover("Chapter thirteen. When the world interrupts."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def interrupt(self):
        head = label(r"Polling, \ or interrupts", font_size=38).to_edge(UP, buff=0.35)
        t0 = -5.6
        line1 = Line([t0, 1.3, 0], [5.8, 1.3, 0], color=GREY_C)
        line2 = Line([t0, -1.0, 0], [5.8, -1.0, 0], color=GREY_C)
        l1 = label(r"polling", font_size=24, color=NO).next_to(line1, UP, buff=0.15).align_to(line1, LEFT)
        l2 = label(r"interrupts", font_size=24, color=YES).next_to(line2, UP, buff=0.15).align_to(line2, LEFT)
        polls = VGroup(*[Line([x, 1.15, 0], [x, 1.45, 0], color=NO, stroke_width=2) for x in np.arange(t0 + 0.2, 5.6,
                                                                                                    0.25)])
        key = 2.6
        keymark = VGroup(Line([key, 1.6, 0], [key, -1.4, 0], color=HEAD, stroke_width=2),
                         label(r"a key is pressed", font_size=20, color=HEAD).move_to([key, 1.95, 0]))
        work = Rectangle(width=key - t0 - 0.1, height=0.35, stroke_width=0, fill_color=CODE,
                         fill_opacity=0.5).move_to([(t0 + key) / 2, -1.0, 0])
        wl = label(r"useful work", font_size=18, color=WHITE).move_to(work)
        handler = Rectangle(width=0.9, height=0.35, stroke_width=0, fill_color=HEAD, fill_opacity=0.8).move_to(
            [key + 0.5, -1.0, 0])
        hl = label(r"handler", font_size=16, color=BG).move_to(handler)
        work2 = Rectangle(width=5.8 - key - 1.0, height=0.35, stroke_width=0, fill_color=CODE,
                          fill_opacity=0.5).move_to([(key + 0.95 + 5.8) / 2, -1.0, 0])
        steps = VGroup(
            label(r"the device raises a signal; \ at the end of the current instruction the processor saves \texttt{pc}, "
                  r"\\ jumps to a \textit{handler}, \ and returns to exactly where it was", font_size=22, color=GREY_A),
            label(r"DYSEAC (1954) \ was the first to wait for its devices this way", font_size=20, color=HIST),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Polling asks a device again and again whether anything has happened. <bookmark mark='a'/> For a keyboard, "
            "that means checking thousands of times for every key, and doing nothing useful in between. "
            "<bookmark mark='b'/> The alternative turns it round. The processor gets on with its work, and when the "
            "key is pressed, the device raises a signal. At the end of the instruction it is running, the processor "
            "saves the program counter, jumps to a piece of code called a handler, deals with the key, and returns to "
            "exactly where it was, as though nothing had happened. <bookmark mark='c'/> The idea appeared in the "
            "mid-1950s, first in the DYSEAC of 1954, and it changed what computers could be: without interrupts there "
            "is no operating system juggling many programs, which is Part 31's subject."
        ) as vo:
            self.play(FadeIn(head), Create(line1), Create(line2), FadeIn(l1), FadeIn(l2))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p) for p in polls], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("b")
            self.play(GrowFromEdge(work, LEFT), FadeIn(wl), run_time=1.2)
            self.play(FadeIn(keymark))
            self.play(FadeIn(handler), FadeIn(hl))
            self.play(GrowFromEdge(work2, LEFT), FadeIn(steps[0]))
            vo.wait_until("c")
            self.play(FadeIn(steps[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def saving(self):
        head = label(r"Saving the machine's place", font_size=38).to_edge(UP, buff=0.35)
        steps = VGroup(*[box(3.0, 0.8, t, c, 22) for t, c in (
            (r"\text{finish this instruction}", YES), (r"\texttt{epc} \leftarrow \texttt{pc}, \ \text{cause}", HEAD),
            (r"\texttt{pc} \leftarrow \text{handler}", CTRL), (r"\text{handler saves registers}", FUNC),
            (r"\texttt{eret}: \ \texttt{pc} \leftarrow \texttt{epc}", YES))]).arrange(DOWN, buff=0.22)
        steps.move_to(LEFT * 3.2 + DOWN * 0.2)
        arrows = VGroup(*[Arrow(steps[k].get_bottom(), steps[k + 1].get_top(), buff=0.03, color=GREY_B,
                                stroke_width=2.5, max_tip_length_to_length_ratio=0.3) for k in range(4)])
        notes = VGroup(
            label(r"two new registers: \ where to return, \ and why we came", font_size=22, color=GREY_A),
            label(r"Pebble reserves opcodes for \texttt{ecall}, \ \texttt{eret}, \ \texttt{csrr} and "
                  r"\texttt{csrw} \ (Part 31)", font_size=22, color=GREY_A),
            label(r"\textit{precise}: \ every earlier instruction finished, \ no later one started", font_size=24,
                  color=HEAD),
            label(r"trivial here, \ where one instruction runs at a time; \\ hard when five overlap \ (Parts 7 and 8)",
                  font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.0 + DOWN * 0.2)
        with self.voiceover(
            "What does the hardware have to do when an interrupt arrives? <bookmark mark='a'/> Finish the instruction "
            "it is running. Copy the program counter into a special register, the exception program counter, and "
            "record the cause in another. Load the program counter with the address of the handler. The handler saves "
            "any registers it is going to use, does its work, restores them, and runs a return-from-exception "
            "instruction that puts the saved program counter back. <bookmark mark='b'/> Pebble's instruction set "
            "already reserves the opcodes for this, ready for Part 31. <bookmark mark='c'/> The subtle requirement is "
            "that the interrupt be precise: every instruction before the saved point has completely finished, and "
            "none after it has started, so the program can resume as if nothing happened. On a machine that runs one "
            "instruction at a time this is free. On a pipeline with five instructions in flight, or an out-of-order "
            "core with a hundred, it is one of the hardest things to get right."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for k in range(5):
                self.play(FadeIn(steps[k], shift=DOWN * 0.1), *( [GrowArrow(arrows[k - 1])] if k else []), run_time=0.7)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exceptions(self):
        head = label(r"The machine interrupts itself", font_size=38).to_edge(UP, buff=0.35)
        rows = VGroup(*[VGroup(label(a, font_size=24, color=c), label(b, font_size=22, color=GREY_A)).arrange(
            RIGHT, buff=0.5) for a, b, c in (
            (r"illegal instruction", r"Pebble's control unit already flags it: \ the \texttt{ill} signal", NO),
            (r"divide by zero", r"when Part 7 adds a divider", NO),
            (r"page fault", r"memory that isn't there yet: \ the operating system fetches it \ (Part 32)", HEAD),
            (r"system call", r"a program asks the operating system for a service, \ on purpose \ (Part 31)", YES),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 0.1)
        for r in rows:
            r[1].align_to(rows[0][1], LEFT).shift(RIGHT * 0.3)
        foot = label(r"for now, \ Pebble just stops; \ Part 31 gives it somewhere to jump", font_size=24,
                     color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The same mechanism handles events that come from inside. <bookmark mark='a'/> An instruction the machine "
            "does not understand: Pebble's control unit already raises a signal for that, and today the machine "
            "simply stops. A division by zero, once Part 7 adds a divider. <bookmark mark='b'/> A load from memory "
            "that has been moved to disk, which the operating system quietly fetches before re-running the load. And a "
            "system call, a deliberate interrupt by which a program asks the operating system to do something on its "
            "behalf. <bookmark mark='c'/> These are called exceptions or traps, and they are how an operating system "
            "takes control. Until Part 31, Pebble has none to return to, so it stops."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
