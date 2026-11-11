from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.pebble import assemble
from explainer.cs.pebble import isa as I
from videos.cs.cs6.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, NO, PART, YES, box, fmt, load,
                                  say, word_bits)


class Idea(VoiceoverScene):
    def construct(self):
        self.card()
        self.cycle()
        self.step()
        self.contract()
        self.bottleneck()

    def card(self):
        card = chapter_card(2, r"Instructions are data", r"What does a processor do, over and over?", part=PART)
        with self.voiceover("Chapter two. Instructions are data."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cycle(self):
        head = label(r"Fetch, \ decode, \ execute", font_size=40).to_edge(UP, buff=0.35)
        r = 2.0
        names = [(r"\text{fetch}", DATA, r"read the word at \texttt{pc}"),
                 (r"\text{decode}", CTRL, r"which instruction? \ which registers?"),
                 (r"\text{execute}", FUNC, r"compute, \ load or store, \ write the result"),
                 (r"\text{next}", YES, r"\texttt{pc} $\leftarrow$ \texttt{pc} + 4, \ or a jump target")]
        nodes = VGroup()
        for k, (t, c, _) in enumerate(names):
            ang = PI / 2 - k * PI / 2
            nodes.add(box(2.3, 0.9, t, c, 34).move_to(np.array([np.cos(ang), np.sin(ang), 0]) * r + DOWN * 0.3
                                                         + LEFT * 2.2))
        arcs = VGroup(*[CurvedArrow(nodes[k].get_center(), nodes[(k + 1) % 4].get_center(), angle=-PI / 3,
                                    color=GREY_B, stroke_width=2.5) for k in range(4)])
        for a in arcs:
            a.scale(0.55)
        descs = VGroup(*[label(rf"{['1', '2', '3', '4'][k]}. \ " + d, font_size=27, color=names[k][1])
                         for k, (_, _, d) in enumerate(names)]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        descs.move_to(RIGHT * 3.4 + DOWN * 0.3)
        rate = label("an active modern core can retire billions of instructions per second", font_size=26,
                     color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Every stored-program computer does one thing, over and over. <bookmark mark='a'/> Fetch: read the word in"
            " memory at the address held in the program counter. <bookmark mark='b'/> Decode: work out which "
            "instruction that word is, and which registers and constants it names. <bookmark mark='c'/> Execute: do "
            "it, an addition, a comparison, a load from memory or a store to it, and write the result. <bookmark "
            "mark='d'/> Next: move the program counter on to the following word, or, if the instruction was a jump or "
            "a branch that is taken, to somewhere else. Then start again. <bookmark mark='e'/> An active modern core "
            "can retire billions of instructions per second, overlapping much of this work; idle cores may sleep. "
            "Everything else in this series, from compilers to databases to the cloud, is built on top of it."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(nodes[k], scale=0.9), FadeIn(descs[k]), Create(arcs[(k - 1) % 4]) if k else Wait(0.1))
            self.play(Create(arcs[3]))
            vo.wait_until("e")
            dot = Dot(radius=0.12, color=HEAD).move_to(nodes[0])
            self.add(dot)
            for _ in range(2):
                for k in range(4):
                    self.play(dot.animate.move_to(nodes[(k + 1) % 4]), run_time=0.35)
            self.play(FadeIn(rate), FadeOut(dot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def step(self):
        head = label(r"One instruction, \ one step", font_size=38).to_edge(UP, buff=0.35)
        src = ["addi a0, zero, 5", "addi a1, zero, 7", "add  a2, a0, a1", "sw   a2, 64(zero)", "halt"]
        p = assemble("\n".join(src))
        words = [int.from_bytes(p.image[4 * k:4 * k + 4], "little") for k in range(len(src))]
        mem = VGroup()
        for k, (w, s_) in enumerate(zip(words, src)):
            row = VGroup(MathTex(rf"\texttt{{{4 * k:#04x}}}", font_size=26, color=GREY_B),
                         MathTex(rf"\texttt{{{w:08x}}}", font_size=28, color=DATA),
                         Text(s_, font="DejaVu Sans Mono", font_size=21, color=CODE)).arrange(RIGHT, buff=0.4)
            mem.add(row)
        data = VGroup(MathTex(r"\texttt{0x40}", font_size=26, color=GREY_B),
                      MathTex(r"\texttt{00000000}", font_size=28, color=DATA)).arrange(RIGHT, buff=0.4)
        mem.add(data)
        mem.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(LEFT * 3.3 + UP * 0.6)
        data.shift(DOWN * 0.25)
        frame = SurroundingRectangle(mem, buff=0.18, color=DATA, stroke_width=2)
        fl = label(r"memory", font_size=22, color=DATA).next_to(frame, UP, buff=0.1)
        regs = {"pc": 0, "a0": 0, "a1": 0, "a2": 0}
        cells = {}
        rg = VGroup()
        for name in regs:
            v = MathTex("0", font_size=30, color=YES)
            n = MathTex(rf"\texttt{{{name}}}", font_size=28, color=YES if name == "pc" else GREY_A)
            b = Rectangle(width=1.5, height=0.55, stroke_color=GREY_C, stroke_width=1.5)
            v.move_to(b)
            cells[name] = (b, v)
            rg.add(VGroup(n, VGroup(b, v)).arrange(RIGHT, buff=0.25))
        rg.arrange(DOWN, aligned_edge=RIGHT, buff=0.2).move_to(RIGHT * 3.6 + UP * 0.8)
        rl = label(r"registers", font_size=22, color=YES).next_to(rg, UP, buff=0.15)
        pc_arrow = Arrow(LEFT * 0.6, ORIGIN, buff=0, color=YES, stroke_width=5).next_to(mem[0], LEFT, buff=0.2)
        wb = word_bits(words[2], I.fields(words[2]), cell=0.27, font_size=17).to_edge(DOWN, buff=0.45)

        def setv(name, val):
            b, v = cells[name]
            nv = MathTex(str(val), font_size=30, color=YES).move_to(b)
            return Transform(v, nv)

        with self.voiceover(
            "Here is the loop on a tiny program. <bookmark mark='a'/> Memory holds five instructions, each one a "
            "thirty-two-bit word, and below them a word of data. The program counter starts at zero. "
            "<bookmark mark='b'/> The first two instructions put five and seven into registers a zero and a one. "
            "<bookmark mark='c'/> The third adds them. Its word is decoded field by field: the opcode says add, and "
            "three four-bit fields name the destination and the two sources. The sum, twelve, goes into a two. "
            "<bookmark mark='d'/> The fourth stores a two into memory at address sixty-four, as data. The last one "
            "halts. Notice that nothing distinguishes the instruction words from the data word except how the "
            "program counter happens to reach them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(fl), FadeIn(mem), FadeIn(rl), FadeIn(rg))
            self.play(GrowArrow(pc_arrow))
            vo.wait_until("a")
            vo.wait_until("b")
            for k, (r_, v) in enumerate((("a0", 5), ("a1", 7))):
                self.play(Indicate(mem[k], color=YES), run_time=0.6)
                self.play(setv(r_, v), setv("pc", 4 * (k + 1)), pc_arrow.animate.next_to(mem[k + 1], LEFT, buff=0.2),
                          run_time=0.7)
            vo.wait_until("c")
            self.play(Indicate(mem[2], color=YES), FadeIn(wb), run_time=0.8)
            self.play(LaggedStart(*[Indicate(n, color=WHITE) for n in wb.names], lag_ratio=0.3), run_time=1.6)
            self.play(setv("a2", 12), setv("pc", 12), pc_arrow.animate.next_to(mem[3], LEFT, buff=0.2))
            vo.wait_until("d")
            self.play(FadeOut(wb), Indicate(mem[3], color=YES))
            nd = MathTex(r"\texttt{0000000c}", font_size=28, color=HEAD).move_to(data[1])
            self.play(Transform(data[1], nd), setv("pc", 16), pc_arrow.animate.next_to(mem[4], LEFT, buff=0.2))
            self.play(Indicate(mem[4], color=NO))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def contract(self):
        head = label(r"The instruction set: \ a contract", font_size=38).to_edge(UP, buff=0.35)
        sw = box(9.0, 1.0, r"\text{software: \ compilers, \ operating systems, \ programs}", CODE, 26).move_to(UP * 1.5)
        isa = box(9.0, 0.7, r"\text{the instruction set architecture}", HEAD, 28).move_to(UP * 0.3)
        hw = VGroup(*[box(2.8, 1.1, t, c, 22) for t, c in (
            (r"\text{single cycle}\\\text{(this part)}", YES), (r"\text{pipelined}\\\text{(Part 7)}", DATA),
            (r"\text{out of order}\\\text{(Part 8)}", FUNC))]).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.1)
        note = label(r"what each instruction does, \ never how: \ the same programs run on all three", font_size=26,
                     color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The list of instructions a machine understands, and exactly what each one does, is its instruction set "
            "architecture. <bookmark mark='a'/> It is a contract. Above it, compilers and programs rely only on what "
            "the instructions promise. <bookmark mark='b'/> Below it, the hardware is free to keep the promise any way"
            " it likes. This part builds the simplest machine that does: one instruction per clock cycle. Part 7 "
            "overlaps instructions like an assembly line, and Part 8 runs them out of order. <bookmark mark='c'/> All "
            "three run exactly the same programs, which is why an instruction set can outlive the hardware that first "
            "implemented it by decades: much early x86 code can still run in a suitable compatibility environment."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(isa), FadeIn(sw))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.2) for h in hw], lag_ratio=0.3), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bottleneck(self):
        head = label(r"The von Neumann bottleneck", font_size=38).to_edge(UP, buff=0.35)
        cpu = box(2.6, 2.2, r"\text{processor}", FUNC, 30).move_to(LEFT * 3.8 + UP * 0.3)
        mem = box(2.6, 3.2, r"\text{memory}", DATA, 30).move_to(RIGHT * 3.8 + UP * 0.3)
        bus = VGroup(Line(cpu.get_right() + UP * 0.25, mem.get_left() + UP * 0.25, color=GREY_B, stroke_width=6),
                     Line(cpu.get_right() + DOWN * 0.25, mem.get_left() + DOWN * 0.25, color=GREY_B, stroke_width=6))
        bl = label(r"one path, \ one word at a time", font_size=22, color=GREY_A).next_to(bus, UP, buff=0.25)
        quote = label(r"``a connecting tube that can transmit a single word between the CPU and the store'' \ "
                      r"--- John Backus, \ Turing Award lecture, \ 1977", font_size=22, color=HIST).to_edge(DOWN, buff=1.0)
        later = label(r"Part 9: \ caches, \ so most words never make the trip", font_size=24, color=YES).to_edge(DOWN,
                                                                                                         buff=0.35)
        with self.voiceover(
            "Putting instructions and data in one memory has a cost, and it has a name. <bookmark mark='a'/> Every "
            "instruction must travel from memory to the processor, and so must most of the data it works on, along "
            "one path, one word at a time. <bookmark mark='b'/> John Backus, who led the team that built FORTRAN, "
            "called it the von Neumann bottleneck in his Turing Award lecture of 1977: a connecting tube between the "
            "processor and the store, through which every computation is squeezed. Since then processors have grown "
            "far faster than memory, so the tube matters more with every decade. <bookmark mark='c'/> Part 9 "
            "widens it with caches, small fast memories that keep the words a program is using close to the processor, "
            "so most of them never make the trip at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cpu), FadeIn(mem))
            self.play(Create(bus), FadeIn(bl))
            vo.wait_until("a")
            for k in range(6):
                d = Dot(radius=0.09, color=CODE if k % 2 == 0 else DATA).move_to(bus[k % 2].get_end() if k % 2 == 0
                                                                                    else bus[1].get_end())
                target = cpu.get_right() + (UP if k % 2 == 0 else DOWN) * 0.25
                self.play(d.animate.move_to(target), run_time=0.45, rate_func=linear)
                self.remove(d)
            vo.wait_until("b")
            self.play(FadeIn(quote))
            vo.wait_until("c")
            self.play(FadeIn(later))
        self.wait(0.3)
        self.clear_scene()
