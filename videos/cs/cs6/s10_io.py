from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.pebble import isa as I
from videos.cs.cs6.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, NO, PART, YES, box, fmt, load)


def mono(s, size=19, color=CODE):
    return Text(s, font="DejaVu Sans Mono", font_size=size, color=color)


class Io(VoiceoverScene):
    def construct(self):
        self.card()
        self.map()
        self.hello()
        self.tape()

    def card(self):
        card = chapter_card(9, r"Talking to the world", r"How does a program print a letter?", lit=(1970,), part=PART)
        with self.voiceover("Chapter nine. Talking to the world."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def map(self):
        head = label(r"Devices live at addresses", font_size=38).to_edge(UP, buff=0.35)
        bar = Rectangle(width=1.4, height=5.6, stroke_color=GREY_B, stroke_width=2).move_to(LEFT * 3.6 + DOWN * 0.3)
        ram = Rectangle(width=1.4, height=1.3, stroke_width=0, fill_color=DATA, fill_opacity=0.35).align_to(bar, DOWN)
        ram.align_to(bar, LEFT)
        dev = Rectangle(width=1.4, height=0.35, stroke_width=0, fill_color=HEAD, fill_opacity=0.6).align_to(bar, UP)
        dev.align_to(bar, LEFT)
        ticks = VGroup(
            MathTex(r"\texttt{0x00000000}", font_size=20, color=GREY_B).next_to(bar.get_corner(DL), LEFT, buff=0.15),
            MathTex(r"\texttt{0x00100000}", font_size=20, color=GREY_B).next_to(ram.get_corner(UL), LEFT, buff=0.15),
            MathTex(r"\texttt{0xFFFF0000}", font_size=20, color=GREY_B).next_to(dev.get_corner(DL), LEFT, buff=0.15),
            MathTex(r"\texttt{0xFFFFFFFF}", font_size=20, color=GREY_B).next_to(bar.get_corner(UL), LEFT, buff=0.15))
        rl = label(r"memory \\ (1 MiB here)", font_size=20, color=DATA).move_to(ram)
        unused = label(r"nothing", font_size=20, color=GREY_D).move_to(bar)
        devs = VGroup(
            VGroup(MathTex(r"\texttt{0xFFFF0000}", font_size=24, color=HEAD),
                   label(r"console: \ store a byte, \ and it is printed", font_size=24, color=GREY_A)),
            VGroup(MathTex(r"\texttt{0xFFFF0004}", font_size=24, color=HEAD),
                   label(r"tape: \ load, \ and get the next byte of input, \ or $-1$ at the end", font_size=24,
                         color=GREY_A)),
            VGroup(MathTex(r"\texttt{0xFFFF0008}", font_size=24, color=HEAD),
                   label(r"cycle counter: \ load, \ and get the instructions run so far", font_size=24,
                         color=GREY_A)),
        )
        for g in devs:
            g.arrange(RIGHT, buff=0.3)
        devs.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 2.3 + UP * 1.4)
        link = Arrow(dev.get_right(), devs.get_left() + DOWN * 0.1, buff=0.15, color=HEAD, stroke_width=3)
        why = VGroup(
            label(r"no new instructions: \ \texttt{lw} and \texttt{sb} reach devices too", font_size=24, color=YES),
            label(r"the address decides who answers: \ memory, \ or a device", font_size=24, color=GREY_A),
            label(r"DEC's PDP-11 (1970) put every device on its bus this way; \\ so does every microcontroller today",
                  font_size=22, color=HIST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 2.3 + DOWN * 1.5)
        with self.voiceover(
            "A computer that cannot print is not much use. Pebble talks to the world without any special instructions "
            "at all. <bookmark mark='a'/> Its addresses run from zero to four billion, but only the first megabyte "
            "here is memory. <bookmark mark='b'/> The top of the address space belongs to devices. Store a byte to "
            "this address, and it appears on the console. Load from this one, and you get the next byte of input "
            "from the tape, or minus one when it runs out. This one counts the instructions run so far. "
            "<bookmark mark='c'/> This is memory-mapped input and output. The same loads and stores that reach "
            "memory reach the devices, and the address alone decides who answers. DEC's PDP-11 made it famous in 1970, "
            "and today every microcontroller works this way: switching on an LED is a store to the right address."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bar), FadeIn(ticks[0]), FadeIn(ticks[3]))
            vo.wait_until("a")
            self.play(FadeIn(ram), FadeIn(rl), FadeIn(ticks[1]), FadeIn(unused))
            vo.wait_until("b")
            self.play(FadeIn(dev), FadeIn(ticks[2]), GrowArrow(link))
            self.play(LaggedStart(*[FadeIn(d) for d in devs], lag_ratio=0.5), run_time=2.4)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(w) for w in why], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hello(self):
        d = load("programs")["hello"]
        head = label(r"Hello, \ world", font_size=38).to_edge(UP, buff=0.35)
        src = [s_ for s_ in d["source"] if s_.strip()]
        lines = VGroup(*[mono(s_.rstrip()[:60], 18) for s_ in src]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        lines.move_to(LEFT * 2.6 + UP * 0.4)
        screen = RoundedRectangle(width=5.2, height=1.2, corner_radius=0.12, stroke_color=YES, stroke_width=2,
                                  fill_color="#05080c", fill_opacity=1).move_to(RIGHT * 3.6 + DOWN * 2.2)
        sl = label(r"console", font_size=20, color=YES).next_to(screen, UP, buff=0.1)
        text = d["output"].rstrip("\n")
        chars = Text(text, font="DejaVu Sans Mono", font_size=24, color=YES).move_to(screen)
        loop = VGroup(*lines[2:7])
        lb = SurroundingRectangle(loop, buff=0.08, color=HEAD, stroke_width=2)
        ll = label(r"one character \\ per trip: \ 5 instructions", font_size=20, color=HEAD).next_to(lb, RIGHT,
                                                                                                     buff=0.25)
        with self.voiceover(
            "So printing a message is a loop of loads and stores. <bookmark mark='a'/> A pointer walks along the "
            "string in memory. Each trip loads a byte, stops if it is the zero that ends the string, and otherwise "
            "stores it to the console's address, then moves on. <bookmark mark='b'/> On the gate-level machine, the "
            "letters appear one at a time, five instructions apart, a hundred and two instructions in all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines))
            vo.wait_until("a")
            self.play(Create(lb), FadeIn(ll))
            vo.wait_until("b")
            self.play(FadeIn(screen), FadeIn(sl))
            self.play(AddTextLetterByLetter(chars, time_per_char=0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tape(self):
        head = label(r"Waiting for the world: \ polling", font_size=38).to_edge(UP, buff=0.35)
        code = VGroup(*[mono(t, 20) for t in ("read:  lw   a0, 0(t3)     # the tape's address",
                                              "       blt  a0, zero, eof # -1: no more input",
                                              "       ...                # use the byte",
                                              "       j    read")]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        code.move_to(UP * 1.2)
        pts = VGroup(
            label(r"the program asks the device, \ again and again: \ \textit{polling}", font_size=24, color=GREY_A),
            label(r"fine for a tape that always has a byte ready; \\ wasteful for a keyboard that waits minutes for a "
                  r"key", font_size=24, color=GREY_A),
            label(r"the alternative: \ the device interrupts the processor \ (chapter 13, \ Part 31)", font_size=24,
                  color=HEAD),
            label(r"device addresses must never be cached, \ or reordered: \ Part 9 marks them uncacheable", font_size=22,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.2)
        with self.voiceover(
            "Reading works the same way. <bookmark mark='a'/> To get the next character, the program loads from the "
            "tape's address, and checks for minus one, the end. The Job reads all of its input like this. "
            "<bookmark mark='b'/> Asking a device over and over is called polling. It is perfect for a tape that always "
            "has the next byte ready, and wasteful for a keyboard, where the program would spin for minutes between "
            "keys. <bookmark mark='c'/> The alternative is to let the device interrupt the processor when something "
            "happens, which chapter thirteen previews. And device addresses bring a subtlety: a cache, in Part 9, must "
            "never keep a copy of one, because reading the tape twice must give two different bytes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()
