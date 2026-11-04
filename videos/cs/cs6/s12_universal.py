from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.turing import CHAMPIONS, TM, run as tm_run
from videos.cs.cs6.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt,
                                  load)


def mono(s, size=19, color=CODE):
    return Text(s, font="DejaVu Sans Mono", font_size=size, color=color)


class Universal(VoiceoverScene):
    def construct(self):
        self.card()
        self.interp()
        self.converse()
        self.emulators()

    def card(self):
        card = chapter_card(11, r"Pebble and the Turing machine", r"Is Pebble more powerful than a Turing machine?",
                            lit=(1936,), part=PART)
        with self.voiceover("Chapter eleven. Pebble and the Turing machine."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def interp(self):
        d = load("tm")
        b3 = d["3"]
        head = label(r"A Turing machine, \ running on Pebble", font_size=36).to_edge(UP, buff=0.35)
        tm = TM.parse(b3["table"])
        r = tm_run(tm, max_steps=100, record=True)
        lo = min(h[1][0] for h in r.history) - 1
        hi = max(h[1][0] for h in r.history) + 1
        cells = VGroup(*[Square(0.62, stroke_color=GREY_C, stroke_width=1.5) for _ in range(hi - lo + 1)]).arrange(
            RIGHT, buff=0.02).move_to(UP * 1.6)
        syms = VGroup(*[MathTex("0", font_size=32, color=GREY_D).move_to(c) for c in cells])
        hd = Triangle(color=HEAD, fill_opacity=1).scale(0.15).rotate(PI).next_to(cells[0 - lo], UP, buff=0.05)
        st = MathTex(r"\text{state } A", font_size=28, color=CTRL).next_to(cells, LEFT, buff=0.4)
        tl = label(r"the tape: \ one byte per cell, \ in Pebble's memory", font_size=20, color=GREY_B).next_to(cells,
                                                                                                         DOWN, buff=0.2)
        rules = VGroup(*[mono(t, 17) for t in ("lbu  t0, 0(s1)       # the symbol under the head",
                                               "slli t1, s2, 3       # rules + 8 state + 4 symbol",
                                               "...  lw   t1, 0(t1)  # the rule: write, move, next",
                                               "sb   t2, 0(s1)       # write",
                                               "addi s1, s1, 1 / -1  # move",
                                               "srli s2, t1, 16      # next state")]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1)
        rules.to_edge(LEFT, buff=0.4).shift(DOWN * 1.5)
        res = VGroup(
            label(rf"the 3-state busy beaver: \\ {b3['steps']} steps, \ {b3['ones']} ones \ (Part 1's numbers)",
                  font_size=24, color=YES),
            label(rf"{fmt(b3['pebble_steps'])} Pebble instructions, \\ most of them counting the ones at the end",
                  font_size=20, color=GREY_A),
            label(r"the same on the gate-level machine", font_size=20, color=GREY_A),
            label(rf"the 4-state champion: \ {d['4']['steps']} steps, \ {d['4']['ones']} ones", font_size=22,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(DOWN * 1.5)
        with self.voiceover(
            "Part 1 claimed that any reasonable computer can do exactly what a Turing machine can do, no more and no "
            "less. Pebble is a reasonable computer, so let us check both directions. <bookmark mark='a'/> First, "
            "Pebble can run a Turing machine. The tape is a row of bytes in memory, the head is a pointer, and the "
            "machine's rules are a table of words. <bookmark mark='b'/> The interpreter is a loop of fifteen "
            "instructions: load the symbol under the head, look up the rule for this state and symbol, write, move the "
            "pointer left or right, and change state. <bookmark mark='c'/> Fed the three-state busy beaver from Part "
            "1, it stops after twenty-one steps with five ones on the tape, exactly as before, on the emulator and on "
            "the gates alike. The four-state champion takes a hundred and seven steps and leaves thirteen."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(syms), FadeIn(hd), FadeIn(st), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(rules, lag_ratio=0.1))
            vo.wait_until("c")
            for h in r.history[1:]:
                state, heads, tapes = h[0], h[1], h[2]
                anims = []
                for k in range(len(cells)):
                    ch = tapes[0].get(lo + k, "_")
                    want = "1" if ch == "1" else "0"
                    if syms[k].get_tex_string() != want:
                        anims.append(Transform(syms[k], MathTex(want, font_size=32, color=YES if want == "1" else
                                                                GREY_D).move_to(cells[k])))
                anims.append(hd.animate.next_to(cells[heads[0] - lo], UP, buff=0.05))
                anims.append(Transform(st, MathTex(rf"\text{{state }} {state if state not in ('H', 'Z') else 'halt'}",
                                                   font_size=28, color=CTRL).next_to(cells, LEFT, buff=0.4)))
                self.play(*anims, run_time=0.25)
            self.play(LaggedStart(*[FadeIn(x) for x in res], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def converse(self):
        head = label(r"And a Turing machine can run Pebble", font_size=36).to_edge(UP, buff=0.35)
        tape = VGroup()
        parts = [("pc", YES, 1.0), ("r_1 \\ldots r_{15}", DATA, 2.6), ("\\text{memory}", INF, 5.2)]
        for t, c, w in parts:
            r = Rectangle(width=w, height=0.6, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.12)
            tape.add(VGroup(r, MathTex(t, font_size=26, color=c).move_to(r)))
        tape.arrange(RIGHT, buff=0.05).move_to(UP * 1.4)
        tl = label(r"Pebble's whole state, \ written out in binary on a tape", font_size=22, color=GREY_B).next_to(
            tape, DOWN, buff=0.2)
        steps = VGroup(
            label(r"find the word at \texttt{pc}: \ walk the tape, \ compare addresses bit by bit", font_size=24,
                  color=GREY_A),
            label(r"decode it: \ a finite table, \ so finitely many states", font_size=24, color=GREY_A),
            label(r"add, \ compare, \ copy: \ Part 1's binary adder machine, \ and friends", font_size=24,
                  color=GREY_A),
            label(r"each Pebble instruction: \ a finite, \ if long, \ sequence of Turing-machine steps", font_size=24,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(DOWN * 0.9)
        concl = label(r"so they compute exactly the same functions: \ the Church--Turing thesis, \ checked on our own "
                      r"machine", font_size=26, color=YES).to_edge(DOWN, buff=0.35)
        diff = label(r"the difference is speed \ (and Pebble's memory is finite: \ a megabyte, \ not an infinite tape)",
                     font_size=20, color=GREY_B).next_to(concl, UP, buff=0.15)
        with self.voiceover(
            "The other direction is an argument rather than a demonstration, but it is short. "
            "<bookmark mark='a'/> Write Pebble's entire state on a Turing machine's tape: the program counter, the "
            "fifteen registers and all of memory, in binary. <bookmark mark='b'/> To run one Pebble instruction, the "
            "Turing machine walks the tape to find the word the program counter points to, comparing addresses bit by "
            "bit. Decoding it is a finite table, which a finite set of states can hold. Adding, comparing and copying "
            "words are the kind of machines Part 1 built, like the binary adder. So each Pebble instruction becomes a "
            "long but finite run of Turing-machine steps. <bookmark mark='c'/> Each can imitate the other. They "
            "compute exactly the same functions; the difference is only speed, and that Pebble's memory is finite. "
            "This is the Church–Turing thesis, checked on a machine we built ourselves, and it closes the loop that "
            "Part 1 opened."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tape], lag_ratio=0.3), FadeIn(tl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(concl), FadeIn(diff))
        self.wait(0.3)
        self.clear_scene()


    # ------------------------------------------------------------------
    def emulators(self):
        j = load("job")
        g_rate = j["paragraph"]["steps"] / j["paragraph"]["seconds"]
        e_rate = j["chapter"]["steps"] / j["chapter"]["seconds"]
        head = label(r"Three Pebbles, \ one program", font_size=38).to_edge(UP, buff=0.35)
        rows = [(r"gate by gate \ (the netlist, compiled to C)", g_rate, YES),
                (r"the emulator \ (Python, an \texttt{if} per opcode)", e_rate, CODE),
                (r"a silicon Pebble \ at 380 MHz \ (problem 3)", 3.8e8, HEAD)]
        lo, hi = 2, 9
        x0, width = -0.4, 5.0
        bars = VGroup()
        for k, (name, rate, c) in enumerate(rows):
            e = np.log10(rate)
            w = (e - lo) / (hi - lo) * width
            y = 1.3 - 0.95 * k
            r = Rectangle(width=w, height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.7).move_to([x0 + w / 2, y, 0])
            nl = label(name, font_size=20, color=c).move_to([x0 - 0.25, y, 0], aligned_edge=RIGHT)
            vl = label(rf"{fmt(rate)} instructions a second", font_size=19, color=GREY_A).next_to(r, RIGHT, buff=0.12)
            bars.add(VGroup(nl, r, vl))
        notes = VGroup(
            label(r"every one gives the same answer, \ to the last bit and the last step", font_size=24, color=YES),
            label(r"QEMU runs ARM programs on x86 this way; \ console emulators run old games on new phones",
                  font_size=22, color=GREY_A),
            label(r"each step down costs a factor of hundreds: \ the price of simulating, \ not of computing",
                  font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Universality has a very practical face: emulation. In this part, the same Pebble program has run on "
            "three different machines. <bookmark mark='a'/> The gate-level netlist, every gate computed in C, manages "
            "about two thousand instructions a second. The Python emulator, which just follows the instruction set's "
            "rules, runs almost a million. A real silicon Pebble, at the clock rate of problem 3, would run hundreds of "
            "millions. <bookmark mark='b'/> They print the same output in the same number of steps, every time. "
            "That is how QEMU runs ARM programs on an x86 laptop, and how a phone runs games written for consoles of "
            "the 1980s. <bookmark mark='c'/> Each layer of simulation costs a factor of hundreds in speed, and nothing "
            "in what can be computed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for b in bars:
                self.play(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]), run_time=0.9)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()
