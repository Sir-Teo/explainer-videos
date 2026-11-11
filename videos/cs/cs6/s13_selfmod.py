from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.pebble import isa as I
from videos.cs.cs6.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, NO, PART, YES, box, fmt, load,
                                  word_bits)


def mono(s, size=19, color=CODE):
    return Text(s, font="DejaVu Sans Mono", font_size=size, color=color)


class SelfMod(VoiceoverScene):
    def construct(self):
        self.card()
        self.rewrite()
        self.why_not()

    def card(self):
        card = chapter_card(12, r"Code is data", r"What if a program rewrites itself?", lit=(1949,), part=PART)
        with self.voiceover("Chapter twelve. Code is data."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def rewrite(self):
        d = load("programs")["selfmod"]
        head = label(r"Summing an array \ by rewriting an instruction", font_size=36).to_edge(UP, buff=0.35)
        src = [s_ for s_ in d["source"] if s_.strip() and not s_.strip().startswith("#")][:10]
        lines = VGroup(*[mono(s_.rstrip()[:58], 16) for s_ in src]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        lines.move_to(LEFT * 3.0 + UP * 0.6)
        k_load = next(i for i, s_ in enumerate(src) if s_.strip().startswith("load:"))
        hl = SurroundingRectangle(lines[k_load], buff=0.05, color=HEAD, stroke_width=2)
        words = d["load_words"]
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        cells = VGroup(*[VGroup(Square(0.5, stroke_color=DATA, stroke_width=1.5),
                                MathTex(str(v), font_size=26, color=DATA)) for v in arr])
        for c in cells:
            c[1].move_to(c[0])
        cells.arrange(RIGHT, buff=0.04).move_to(RIGHT * 3.4 + UP * 1.6)
        al = label(r"the array", font_size=20, color=DATA).next_to(cells, UP, buff=0.12)
        wb = word_bits(words[0], I.fields(words[0]), cell=0.2, font_size=13, show_value=True).move_to(DOWN * 1.6)
        wl = label(r"the load instruction, \ as it sits in memory", font_size=20, color=HEAD).next_to(wb, UP,
                                                                                                   buff=0.15)
        total = ValueTracker(0)
        tv = always_redraw(lambda: MathTex(rf"\text{{sum}} = {int(total.get_value())}", font_size=32,
                                           color=YES).next_to(cells, DOWN, buff=0.45))
        ptr = Triangle(color=HEAD, fill_opacity=1).scale(0.1).rotate(PI).next_to(cells[0], UP, buff=0.05)
        with self.voiceover(
            "Because instructions are data, a program can change itself, and early programmers did it all the time. "
            "<bookmark mark='a'/> EDSAC had no way to say load the next element of an array: an instruction's address "
            "was fixed in the instruction. So to walk through an array, a program added one to the address inside its "
            "own load instruction, each time round the loop. <bookmark mark='b'/> Here is that trick on Pebble. The "
            "load reads the element at offset zero. Then the program loads the load instruction itself, as an "
            "ordinary word, adds four to it, which adds four to its offset field, and stores it back. "
            "<bookmark mark='c'/> Next time round, the same instruction reads the next element. Eight trips later the "
            "sum is thirty-one, on the emulator and on the gates."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines))
            self.play(FadeIn(cells), FadeIn(al), Create(hl))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(wb), FadeIn(wl), FadeIn(ptr))
            self.add(tv)
            vo.wait_until("c")
            run = 0
            for k in range(8):
                run += arr[k]
                self.play(ptr.animate.next_to(cells[k], UP, buff=0.05), Indicate(cells[k], color=YES),
                          total.animate.set_value(run), run_time=0.45)
                if k + 1 < len(words):
                    nw = word_bits(words[k + 1], I.fields(words[k + 1]), cell=0.2, font_size=13,
                                   show_value=True).move_to(wb)
                    self.play(Transform(wb, nw), Indicate(lines[k_load], color=HEAD), run_time=0.45)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why_not(self):
        head = label(r"Why modern programs don't", font_size=38).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"1949: \ the Manchester Mark 1's \textit{B-lines}, \ the first index registers: \\ base plus offset, "
                  r"\ as Pebble's \texttt{lw t0, 8(s0)}, \ made the trick unnecessary", font_size=24, color=HIST),
            label(r"pipelines and caches fetch instructions early \ (Parts 7 and 9): \\ a rewritten instruction may "
                  r"already be on its way, \ stale", font_size=24, color=GREY_A),
            label("write xor execute: \\ restrict simultaneous write and execute permissions \\\\ a code-injection defence, \\ not complete attack prevention (Part 55)", font_size=24, color=NO),
            label("a JIT can generate machine code at runtime, \\ then arrange executable permissions \\ (Part 15)", font_size=24, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.15)
        with self.voiceover(
            "Self-modifying code has almost disappeared, for three reasons. <bookmark mark='a'/> The first was "
            "invented in 1949 at Manchester: the B-lines, the first index registers, which add a register to an "
            "instruction's address. Pebble's loads work this way, base plus offset, so the trick is unnecessary. "
            "<bookmark mark='b'/> The second is speed. Pipelined processors and caches fetch instructions long before "
            "they run, so a rewritten instruction may already be on its way in its old form. <bookmark mark='c'/> The "
            "third is security. Writable executable memory can make code injection easier. Many systems therefore "
            "restrict pages from being writable and executable at the same time: write xor execute, which Part 55 "
            "returns to. <bookmark mark='d'/> And yet the idea lives on, carefully fenced. A JavaScript engine with a "
            "just-in-time compiler compiles hot code to machine code while your page runs, writes it into memory as "
            "data, and only then flips that memory to executable. Code is data, still."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p_ in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p_, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
