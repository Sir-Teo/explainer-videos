from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.pebble import isa as I
from videos.cs.cs6.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, NO, PART, YES, box, fmt, load,
                                  word_bits)


def mono(s, size=20, color=CODE):
    return Text(s, font="DejaVu Sans Mono", font_size=size, color=color)


class Assembler(VoiceoverScene):
    def construct(self):
        self.card()
        self.why()
        self.pass1()
        self.pass2()
        self.pseudo()
        self.linking()

    def card(self):
        card = chapter_card(6, r"The assembler", r"Who writes the numbers?", lit=(1947, 1949), part=PART)
        with self.voiceover("Chapter six. The assembler."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def why(self):
        d = load("assembler")
        head = label(rf"Nobody wants to write \texttt{{0x{d['listing'][1][1]:08x}}}", font_size=36).to_edge(UP, buff=0.35)
        left = VGroup(*[MathTex(rf"\texttt{{{w:08x}}}", font_size=26, color=DATA) for _, w, _, _ in d["listing"]]
                      ).arrange(DOWN, buff=0.12).move_to(LEFT * 4.0 + DOWN * 0.2)
        right = VGroup(*[mono(t, 20) for t in ("li   a0, 10", "li   a1, 0", "loop: add a1, a1, a0",
                                                "addi a0, a0, -1", "bnez a0, loop", "halt")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.0 + DOWN * 0.2)
        arr = Arrow(right.get_left() + LEFT * 0.3, left.get_right() + RIGHT * 0.3, color=HEAD, buff=0.1)
        al = label(r"the assembler", font_size=26, color=HEAD).next_to(arr, UP, buff=0.12)
        notes = VGroup(
            label(r"mnemonics for opcodes, \ names for registers, \ \textit{labels} for addresses", font_size=24,
                  color=GREY_A),
            label(r"Kathleen Booth, \ 1947: \ an assembly notation for the ARC computer at Birkbeck; \\ EDSAC's initial "
                  r"orders (1949) translated letters to orders as they loaded", font_size=22, color=HIST),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The machine wants words like these. <bookmark mark='a'/> People want to write something like this: a "
            "short name for each operation, names for the registers, and, most importantly, names for places in the "
            "program, called labels, instead of addresses that change every time a line is added. "
            "<bookmark mark='b'/> A program that translates one into the other is an assembler. "
            "<bookmark mark='c'/> Kathleen Booth designed one of the first assembly notations in 1947, for the ARC "
            "computer at Birkbeck College, and EDSAC's initial orders of 1949 already translated letters into orders as "
            "they loaded the tape. Pebble's assembler, in the series' library, is a few hundred lines of Python."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left, lag_ratio=0.1))
            self.play(FadeIn(right, lag_ratio=0.15))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(al), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pass1(self):
        d = load("assembler")
        head = label(r"Pass 1: \ where does everything go?", font_size=36).to_edge(UP, buff=0.35)
        src = [s_ for s_ in d["source"] if s_.strip()]
        lines = VGroup(*[mono(s_.rstrip()[:52], 18) for s_ in src]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        lines.move_to(LEFT * 1.6 + UP * 0.2)
        addr = ValueTracker(0)
        sizes = [2, 2, 1, 1, 1, 1]  # li is two instructions
        marks = VGroup()
        a = 0
        for ln, sz in zip(lines, sizes):
            marks.add(MathTex(rf"\texttt{{{a:#04x}}}", font_size=20, color=GREY_B).next_to(ln, LEFT, buff=0.35))
            a += 4 * sz
        table_t = label(r"symbol table", font_size=24, color=HEAD)
        entry = MathTex(rf"\texttt{{loop}} \ \mapsto \ \texttt{{{d['labels']['loop']:#04x}}}", font_size=30,
                        color=HEAD)
        table = VGroup(table_t, entry).arrange(DOWN, buff=0.25)
        tb = SurroundingRectangle(table, buff=0.25, color=HEAD, corner_radius=0.1)
        tabg = VGroup(tb, table).move_to(RIGHT * 4.4 + UP * 0.6)
        ptr = Arrow(LEFT * 0.4, ORIGIN, buff=0, color=YES, stroke_width=4)
        notes = VGroup(
            label(r"walk the lines, \ counting bytes: \ \texttt{li} takes two words, \ the rest one", font_size=22,
                  color=GREY_A),
            label(r"a label's value is the address where it appears", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Labels create a chicken-and-egg problem: a branch near the top of a program may name a label near the "
            "bottom, whose address is not known yet. So the assembler reads the program twice. "
            "<bookmark mark='a'/> The first pass encodes nothing. It walks down the lines with a counter, adding the "
            "size of each one: four bytes for most instructions, eight for li, which becomes two. "
            "<bookmark mark='b'/> Whenever it meets a label, it records the counter's value in a symbol table. Here, "
            "loop is at address sixteen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines))
            vo.wait_until("a")
            ptr.next_to(marks[0], LEFT, buff=0.1)
            self.play(FadeIn(ptr), FadeIn(notes[0]))
            for k in range(len(lines)):
                self.play(ptr.animate.next_to(marks[k], LEFT, buff=0.1), FadeIn(marks[k]), run_time=0.45)
                if k == 2:
                    vo.wait_until("b")
                    self.play(FadeIn(tb), FadeIn(table_t), TransformFromCopy(lines[2][:5], entry), FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pass2(self):
        d = load("assembler")
        head = label(r"Pass 2: \ encode", font_size=36).to_edge(UP, buff=0.35)
        rows = VGroup()
        for a, w, s_, dis in d["listing"]:
            rows.add(VGroup(MathTex(rf"\texttt{{{a:#04x}}}", font_size=20, color=GREY_B),
                            MathTex(rf"\texttt{{{w:08x}}}", font_size=22, color=DATA),
                            mono(dis, 17)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(LEFT * 3.4 + UP * 0.5)
        bnez = next(k for k, r in enumerate(d["listing"]) if r[3].startswith("bne"))
        a_b = d["listing"][bnez][0]
        w_b = d["listing"][bnez][1]
        wb = word_bits(w_b, I.fields(w_b), cell=0.17, font_size=12, show_value=True).move_to(RIGHT * 3.6 + UP * 1.0)
        calc = MathTex(rf"\text{{offset}} = \frac{{\texttt{{loop}} - \texttt{{pc}}}}{{4}} = "
                       rf"\frac{{{d['labels']['loop']} - {a_b}}}{{4}} = {(d['labels']['loop'] - a_b) // 4}",
                       font_size=30, color=HEAD).next_to(wb, DOWN, buff=0.5)
        note = label(r"every name replaced by a number: \ the opcode, \ the registers, \ the label's distance",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The second pass encodes. <bookmark mark='a'/> Each line becomes a word: look up the opcode, put each "
            "register number in its field, and place the constant. <bookmark mark='b'/> A branch to a label stores not"
            " the label's address but its distance from the branch, counted in instructions. The branch at twenty-four"
            " goes back to sixteen, so its offset is minus two. Because the distance, not the address, is stored, this"
            " internal branch keeps working if the whole block moves together and its relative layout stays fixed."
        ) as vo:
            self.play(FadeIn(head),
                      LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Indicate(rows[bnez], color=YES), FadeIn(wb))
            self.play(Write(calc))
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pseudo(self):
        d = load("assembler")
        head = label(r"Pseudo-instructions: \ shorthand the assembler expands", font_size=34).to_edge(UP, buff=0.35)
        rows = VGroup()
        for p in d["pseudo"]:
            rows.add(VGroup(mono(p["src"], 20, HEAD), MathTex(r"\Rightarrow", font_size=28, color=GREY_B),
                            VGroup(*[mono(o, 18) for o in p["out"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.06))
                     .arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(LEFT * 1.6 + DOWN * 0.1)
        for r in rows:
            r[1].set_x(rows[0][1].get_x())
            r[2].next_to(r[1], RIGHT, buff=0.35)
        side = VGroup(
            label(r"\texttt{li}: \ any 32-bit constant, \\ the top 22 bits by \texttt{lui}, \ the low 10 by \texttt{ori}",
                  font_size=22, color=GREY_A),
            label(r"\texttt{j}: \ \texttt{jal} writing the zero register, \\ so the link is thrown away", font_size=22,
                  color=GREY_A),
            label(r"\texttt{ret}: \ jump to the address \\ \texttt{call} left in \texttt{ra}", font_size=22,
                  color=GREY_A),
            label(r"the zero register makes \\ half of these possible", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Assemblers also accept instructions the machine does not have. <bookmark mark='a'/> Load-immediate of a "
            "big constant becomes two real instructions, lui for the top twenty-two bits and ori for the low ten. "
            "Move is an add of zero. Jump is a jump-and-link that writes its return address into the zero register, "
            "which throws it away. Branch-if-zero compares with the zero register. <bookmark mark='b'/> Call and return "
            "are jump-and-link and jump-to-register. Half of these exist only because register zero always reads zero, "
            "which is exactly why the architecture has one."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def linking(self):
        head = label(r"From text to a running program", font_size=36).to_edge(UP, buff=0.35)
        a = box(2.4, 1.6, r"\texttt{main.s}\\ \texttt{call print}", CODE, 22).move_to(LEFT * 5.0 + UP * 1.0)
        b = box(2.4, 1.6, r"\texttt{print.s}\\ \texttt{print:} \ldots", CODE, 22).move_to(LEFT * 5.0 + DOWN * 1.2)
        oa = box(2.2, 1.6, r"\text{object file}\\ \text{a hole at } \texttt{print}", HEAD, 20).move_to(LEFT * 1.6 +
                                                                                                    UP * 1.0)
        ob = box(2.2, 1.6, r"\text{object file}\\ \texttt{print} = \texttt{0x00}", HEAD, 20).move_to(LEFT * 1.6 +
                                                                                                  DOWN * 1.2)
        ln = box(1.8, 1.0, r"\text{linker}", YES, 26).move_to(RIGHT * 1.6 + DOWN * 0.1)
        img = box(1.9, 2.6, r"\text{one image}", DATA, 22).move_to(RIGHT * 4.6 + DOWN * 0.1)
        arr = VGroup(Arrow(a.get_right(), oa.get_left(), buff=0.1, color=GREY_B),
                     Arrow(b.get_right(), ob.get_left(), buff=0.1, color=GREY_B),
                     Arrow(oa.get_right(), ln.get_left() + UP * 0.2, buff=0.1, color=GREY_B),
                     Arrow(ob.get_right(), ln.get_left() + DOWN * 0.2, buff=0.1, color=GREY_B),
                     Arrow(ln.get_right(), img.get_left(), buff=0.1, color=GREY_B))
        tags = VGroup(label(r"assemble \\ each file", font_size=18, color=GREY_B).next_to(arr[0], UP, buff=0.05),
                      label("patch symbol references \\\\ and relocations", font_size=18, color=GREY_B).next_to(
                          ln, UP, buff=0.15))
        notes = VGroup(
            label("PC-relative references stay fixed only when source and target move together", font_size=22,
                  color=GREY_A),
            label("cross-object calls and absolute addresses can need relocation; \\ diagram: conventional toolchain",
                  font_size=22, color=GREY_A),
            label("Pebble currently assembles one image directly; \\ its loader copies it and sets \\texttt{pc}", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Real programs are written in many files. <bookmark mark='a'/> Each file is assembled on its own, into an "
            "object file: the machine code, plus a list of the labels it defines, plus holes where it uses a label "
            "defined somewhere else, like a call to a print routine in another file. <bookmark mark='b'/> A linker "
            "joins the object files into one image, decides where each piece goes, and fills in the holes. A relative "
            "branch within a block needs no change when that block moves as a unit. A call to another object can still"
            " need its relative offset patched, because the caller and target may move separately. Absolute addresses,"
            " the kind la builds, also need patching. These fixes are relocations. The diagram explains a conventional"
            " object-file workflow; Pebble's current assembler builds a single image directly. <bookmark mark='c'/> "
            "Finally a loader copies the image into memory and points the program counter at its first instruction. "
            "Pebble's loader is three lines of Python; EDSAC's was its initial orders, wired into the machine. Part 11"
            " returns to linking, and Part 41 to building programs from thousands of files."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a), FadeIn(b))
            self.play(GrowArrow(arr[0]), GrowArrow(arr[1]), FadeIn(oa), FadeIn(ob), FadeIn(tags[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(GrowArrow(arr[2]), GrowArrow(arr[3]), FadeIn(ln), FadeIn(tags[1]))
            self.play(GrowArrow(arr[4]), FadeIn(img))
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()
