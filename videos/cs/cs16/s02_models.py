from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, load, mono, words)


class Models(VoiceoverScene):
    def construct(self):
        self.card()
        self.ram()
        self.pitfall()
        self.others()

    def card(self):
        card = chapter_card(1, r"What counts as a step", r"How do we measure an algorithm, not a machine?",
                            lit=(1963,), extra=((1963, r"Shepherdson and Sturgis: \ register machines"),), part=PART)
        with self.voiceover("Chapter one. What counts as a step."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ram(self):
        head = label(r"The RAM: \ a machine for counting", font_size=34).to_edge(UP, buff=0.3)
        cells = VGroup(*[VGroup(Rectangle(width=0.9, height=0.5, color=GREY_B, stroke_width=1.5),
                                mono(str(v), 16, WHITE)) for v in (7, 3, 0, 12, 5, 9, 1, 4)])
        for c in cells:
            c[1].move_to(c[0])
        cells.arrange(RIGHT, buff=0).move_to(UP * 1.4)
        addr = VGroup(*[mono(str(k), 13, GREY_B).next_to(c, UP, buff=0.08) for k, c in enumerate(cells)])
        cpu = VGroup(RoundedRectangle(width=2.6, height=1.0, corner_radius=0.12, color=DATA, stroke_width=2),
                     label(r"one instruction, \ one step", font_size=20, color=DATA))
        cpu[1].move_to(cpu[0])
        cpu.next_to(cells, DOWN, buff=0.8)
        ar = DoubleArrow(cpu.get_top(), cells[3].get_bottom(), buff=0.08, color=GREY_B, stroke_width=2,
                         tip_length=0.14)
        pts = VGroup(
            label(r"the \textbf{RAM}: \ memory cells with addresses; \ read, \ write, \ add, \ compare, \ jump: "
                  r"\ each one step", font_size=21, color=GREY_A),
            label(r"the \textbf{word-RAM}: \ a cell holds $w$ bits, \ with $w \ge \log_2 n$ \ (enough to hold an "
                  r"address)", font_size=21, color=GREY_A),
            label(r"Pebble is one: \ 32-bit words, \ and instructions that cost a cycle or a few", font_size=21,
                  color=YES),
            label(r"we count steps, \ not seconds: \ the answer then holds for every machine of this kind",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "To compare algorithms rather than machines, we need a machine simple enough to count on. <bookmark "
            "mark='a'/> The random-access machine has memory cells with addresses, and a processor that reads a "
            "cell, writes one, adds, compares or jumps, each in one step. <bookmark mark='b'/> The word-RAM adds "
            "one honest detail: a cell holds w bits, and w is at least the logarithm of the input size, so that a "
            "cell can hold an address. <bookmark mark='c'/> Pebble is such a machine, with thirty-two-bit words. "
            "<bookmark mark='d'/> From now on we count steps, not seconds, and what we prove holds on every machine "
            "of this kind, up to a constant factor."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(addr), FadeIn(cpu), GrowArrow(ar))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def pitfall(self):
        d = load("ram")
        head = label(r"The pitfall of unit cost", font_size=34).to_edge(UP, buff=0.3)
        src = code(["x = 3", "repeat n times:", "    x = x * x        # one step?"], size=20,
                   color=CODE).to_edge(LEFT, buff=0.7).shift(UP * 1.6)
        rows = [r for r in d["rows"] if r["step"] >= 8]
        ax = Axes(x_range=[8, rows[-1]["step"] + 1, 2], y_range=[-7, 1, 2], x_length=6.0, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.4)
        pts = [ax.c2p(r["step"], np.log10(max(r["seconds"], 1e-7))) for r in rows]
        line = VMobject(color=NO, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.05, color=NO) for p in pts])
        yt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(8, v), LEFT, buff=0.1)
                      for v, t in ((-6, r"1 $\mu$s"), (-3, r"1 ms"), (0, r"1 s"))])
        xl = label(r"squaring number", font_size=17, color=GREY_B).next_to(ax, DOWN, buff=0.2)
        yl = label(r"time for that one multiplication, \ CPython, \ this machine", font_size=17,
                   color=GREY_B).next_to(ax, UP, buff=0.1)
        last = d["rows"][-1]
        pts2 = VGroup(
            label(r"after $n$ squarings, \ $x = 3^{2^n}$ \ has about $1.6 \cdot 2^n$ bits", font_size=21, color=GREY_A),
            label(rf"step {last['step']}: \ a {words(last['bits'])}-bit number, \ "
                  rf"{human_time(last['seconds'])} for one ``step''", font_size=21, color=NO),
            VGroup(label(r"a unit-cost RAM with unbounded words", font_size=20, color=HEAD),
                   label(r"could solve hard problems this way: \ the word-RAM forbids it", font_size=20,
                         color=HEAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.6)
        if pts2.width > 5.4:
            pts2.scale_to_fit_width(5.4)
        with self.voiceover(
            "Why insist on words of bounded size? <bookmark mark='a'/> Square a number again and again. If every "
            "multiplication were one step, n squarings would cost n steps. But after n squarings the number has "
            "about one point six times two to the n bits. <bookmark mark='b'/> We timed each multiplication in "
            "Python on this machine. The early ones take microseconds. By the twenty-first, a single "
            "multiplication of a three-million-bit number takes a tenth of a second, and each one costs about "
            "three times the last. <bookmark mark='c'/> A model that charged one step for that "
            "could do absurd things, packing whole computations into one giant number. The word-RAM rules it out: "
            "a step works on a word, and a word is about as long as an address."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(pts2[0]))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            self.play(Create(line), FadeIn(dots), FadeIn(pts2[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(pts2[2]))
        self.wait(0.3)
        self.clear_scene()

    def others(self):
        head = label(r"Other ways to count", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(label(r"Turing machine \ (Part 2)", font_size=22, color=LAM),
                   label(r"a tape and a head: \ a RAM's $t$ steps take it about $t^3$ or less: \ polynomially "
                         r"related", font_size=20, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"comparison model", font_size=22, color=YES),
                   label(r"count only comparisons between keys: \ the model of chapter 6's lower bound", font_size=20,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"cell-probe model \ (Yao, \ 1981)", font_size=22, color=DATA),
                   label(r"count only memory accesses, \ computation free: \ the strongest lower bounds for data "
                         r"structures", font_size=20, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"external memory \ (Aggarwal and Vitter, \ 1988)", font_size=22, color=CTRL),
                   label(r"count block transfers: \ Part 9's caches, \ and chapter 14's disks", font_size=20,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.55)
        note = label(r"choose the model that matches the cost you care about", font_size=23,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The RAM is not the only way to count. <bookmark mark='a'/> A Turing machine, from Part 2, is much "
            "slower in absolute terms, but anything a RAM does in t steps it can do in a polynomial of t, so the "
            "two agree about what is efficient. <bookmark mark='b'/> The comparison model counts only comparisons "
            "between keys; chapter six proves its famous lower bound. <bookmark mark='c'/> The cell-probe model, "
            "from Andrew Yao, counts only memory accesses and makes computation free, which is where the strongest "
            "lower bounds for data structures come from. <bookmark mark='d'/> And the external-memory model counts "
            "transfers of whole blocks, the cost that dominates when data lives in a cache or on a disk. <bookmark "
            "mark='e'/> Each answers a different question. Choose the one that charges for what you care about."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()
