from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, curve, fit_right, log_axes, load,
                                   mono)

PH = {"save": DATA, "dispatch": HEAD, "handle": YES, "restore": LAM}


class Traps(VoiceoverScene):
    def construct(self):
        self.card()
        self.sequence()
        self.dive()
        self.costs()
        self.buffers()

    def card(self):
        card = chapter_card(3, r"Traps and the system call", r"How does a program ask the kernel for anything?",
                            lit=(1961, 1974), extra=((1961, r"CTSS"), (1974, r"Unix's system calls")), part=PART)
        with self.voiceover("Chapter three. Traps, and the system call."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def sequence(self):
        head = label(r"A trap, \ in one step", font_size=36).to_edge(UP, buff=0.3)
        user = VGroup(*[mono(s, 20, c) for s, c in (("li   a5, 3", GREY_A), ("ecall", HEAD), ("mv   s0, a0", GREY_A))]
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        ubox = SurroundingRectangle(user, buff=0.25, color=DATA, corner_radius=0.1)
        ulab = label(r"user mode", font_size=20, color=DATA).next_to(ubox, UP, buff=0.1)
        U = VGroup(ubox, user, ulab).move_to([-4.6, 1.0, 0])
        steps = VGroup(*[label(t, font_size=21, color=c) for t, c in (
            (r"1. \ \texttt{epc} $\leftarrow$ pc \ (where to come back)", WHITE),
            (r"2. \ \texttt{cause} $\leftarrow$ 8 \ (an \texttt{ecall}); \ \texttt{tval} for a bad address", WHITE),
            (r"3. \ interrupts off: \ PIE $\leftarrow$ IE, \ IE $\leftarrow$ 0", WHITE),
            (r"4. \ PM $\leftarrow$ mode, \ mode $\leftarrow$ \textbf{kernel}", YES),
            (r"5. \ pc $\leftarrow$ \texttt{tvec}: \ the kernel's one entry point", KERN))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.16)
        hbox = SurroundingRectangle(steps, buff=0.25, color=GREY_B, corner_radius=0.1)
        hlab = label(r"the hardware, \ all at once", font_size=20, color=GREY_B).next_to(hbox, UP, buff=0.1)
        Hw = VGroup(hbox, steps, hlab).move_to([1.9, 1.0, 0])
        arr = Arrow(ubox.get_right(), hbox.get_left(), buff=0.1, color=HEAD, stroke_width=3)
        back = label(r"\texttt{eret} \ undoes it: \ pc $\leftarrow$ \texttt{epc}, \ mode $\leftarrow$ PM, \ IE "
                     r"$\leftarrow$ PIE", font_size=21, color=LAM).next_to(Hw, DOWN, buff=0.4)
        kinds = VGroup(
            label(r"\textbf{traps} are caused by the instruction: \ \texttt{ecall}, \ an illegal instruction, \ a bad "
                  r"address, \ division by zero", font_size=20, color=WHITE),
            label(r"\textbf{interrupts} come from outside: \ the timer, \ later a disk or a network card \ (Parts 34, "
                  r"36): \ the same five steps", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A program asks the kernel for something by setting up its request in registers, here call number three, "
            "get my process id, and executing e-call. <bookmark mark='a'/> The hardware then does five things in a "
            "single step. It saves the program counter, so it knows where to come back. It records the cause: an "
            "e-call, or for a fault, the bad address too. It turns interrupts off. It switches to kernel mode, "
            "remembering the old mode. And it jumps to the one address the kernel chose at boot. <bookmark mark='b'/> "
            "The program cannot choose where in the kernel it lands, and that is the point: every request goes "
            "through one gate the kernel controls. <bookmark mark='c'/> E-ret reverses the last three steps, and "
            "the program continues after its e-call. <bookmark mark='d'/> The same mechanism serves every event the "
            "instruction itself causes, from an e-call to a division by zero. <bookmark mark='e'/> Interrupts from "
            "outside, like the timer, use the same five steps, between two instructions of whatever program is "
            "running."
        ) as vo:
            self.play(FadeIn(head), FadeIn(U))
            vo.wait_until("a")
            self.play(GrowArrow(arr), FadeIn(hbox), FadeIn(hlab))
            self.play(LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.35), run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(steps[4], color=KERN))
            vo.wait_until("c")
            self.play(FadeIn(back))
            vo.wait_until("d")
            self.play(FadeIn(kinds[0]))
            vo.wait_until("e")
            self.play(FadeIn(kinds[1]))
        self.wait(0.3)
        self.clear_scene()

    def dive(self):
        d = load("trap")
        head = label(r"Inside one \texttt{getpid}: \ every kernel instruction", font_size=34).to_edge(UP, buff=0.3)
        rows = d["rows"]
        n = len(rows)
        W = 12.0
        cell = W / n
        strip = VGroup(*[Rectangle(width=cell, height=0.42, stroke_width=0.4, stroke_color=BG,
                                   fill_color=PH.get(ph, GREY_B), fill_opacity=0.9) for _, _, ph in rows]).arrange(
            RIGHT, buff=0).next_to(head, DOWN, buff=0.5)
        counts = d["counts"]
        cols = VGroup()
        for ph, title in (("save", r"save the user's registers"), ("dispatch", r"which call?"),
                          ("handle", r"do it"), ("restore", r"restore, \ \texttt{eret}")):
            lines = [r[1] for r in rows if r[2] == ph]
            show = lines[:5] + (["..."] if len(lines) > 6 else []) + (lines[-1:] if len(lines) > 5 else [])
            body = VGroup(*[mono(s, 15, PH[ph] if s != "..." else GREY_C) for s in show]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.07)
            t = label(rf"{title}: \ {counts.get(ph, 0)}", font_size=19, color=PH[ph])
            cols.add(VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.15))
        cols.arrange(RIGHT, buff=0.35, aligned_edge=UP).next_to(strip, DOWN, buff=0.45)
        fit_right(cols, 6.8)
        if cols.get_left()[0] < -6.8:
            cols.scale_to_fit_width(13.4).next_to(strip, DOWN, buff=0.45)
        total = n
        lines = VGroup(
            label(rf"{total} kernel instructions \ (and the \texttt{{ecall}}) \ to return one number", font_size=22,
                  color=WHITE),
            label(r"most of it is bookkeeping: \ save all fifteen registers, \ because the kernel will use them, "
                  r"\ then put them back", font_size=21, color=GREY_A),
            label(r"the kernel never trusts the program: \ it checks every pointer it is given \ (\texttt{read} "
                  r"into kernel memory is refused)", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now follow one system call all the way down. A process calls get-pid, and we record every instruction "
            "the kernel executes before the process runs again. <bookmark mark='a'/> Each bar is one instruction, "
            "coloured by what it is for. <bookmark mark='b'/> First, twenty-six instructions save the program's "
            "registers into its process control block, because the kernel is about to use those registers itself. "
            "<bookmark mark='c'/> Then twenty-three find out which call this is. <bookmark mark='d'/> The work "
            "itself takes three instructions: load the process id, and store it where the program's a-zero will be "
            "restored from. <bookmark mark='e'/> Then twenty-six more put every register back, and e-ret returns. "
            "<bookmark mark='f'/> Seventy-eight instructions, to return one number. <bookmark mark='g'/> And for "
            "calls that take a buffer, the kernel first checks that the buffer lies inside the caller's memory. A "
            "program that passes a pointer into the kernel gets an error, not the kernel's secrets."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in strip], lag_ratio=0.02), run_time=2.0)
            for mk, c in zip("bcde", cols):
                vo.wait_until(mk)
                self.play(FadeIn(c))
            vo.wait_until("f")
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("g")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def costs(self):
        d = load("trap")
        head = label(r"What a system call costs, \ on this machine", font_size=34).to_edge(UP, buff=0.3)
        vals = [("function call", d["call_ns"], DATA), ("vDSO \\texttt{clock\\_gettime}", d["vdso_ns"], YES),
                ("system call \\texttt{getpid}", d["getpid_ns"], NO)]
        mx = math.log10(200)
        bars = VGroup()
        for i, (nm, v, c) in enumerate(vals):
            w = 8.0 * max(math.log10(v * 10), 0.1) / (mx + 1)
            r = Rectangle(width=w, height=0.55, stroke_width=0, fill_color=c, fill_opacity=0.85)
            r.move_to([-3.0 + w / 2, 1.5 - i * 0.9, 0])
            t = label(nm, font_size=21, color=c).next_to(r, LEFT, buff=0.2).align_to([-3.2, 0, 0], RIGHT)
            nv = label(rf"{v:.1f} ns", font_size=21, color=WHITE).next_to(r, RIGHT, buff=0.15)
            bars.add(VGroup(r, t, nv))
        scale = label(r"(log scale)", font_size=16, color=GREY_C).next_to(bars, DOWN, buff=0.15).align_to(bars, RIGHT)
        lines = VGroup(
            label(rf"a system call is about {d['getpid_ns'] / d['call_ns']:.0f} function calls: \ the trap, \ the "
                  r"saving, \ and since 2018 the Spectre defences \ (Part 8)", font_size=21, color=WHITE),
            label(r"the \textbf{vDSO}: \ the kernel maps a page of its own code and data into every process, "
                  r"\ so asking the time needs no trap at all", font_size=21, color=YES),
            label(rf"measured on this machine: \ {d['cpu']}, \ a virtual machine", font_size=18, color=GREY_B),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "On a real machine, this one, the numbers look like this. <bookmark mark='a'/> An ordinary function call "
            "takes one and a half nanoseconds. <bookmark mark='b'/> Asking the kernel for the process id takes a "
            "hundred and twelve: about seventy-five function calls. The hardware trap is part of it. Saving state "
            "is part of it. And since 2018, the defences against Spectre and Meltdown from Part 8 add work to "
            "every crossing. <bookmark mark='c'/> Some requests skip "
            "the trap altogether. Linux maps a page of kernel code and data into every process, the vDSO, so reading "
            "the clock is an ordinary function call: twenty-nine nanoseconds, with no change of mode."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[2]), FadeIn(scale), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(bars[1]), FadeIn(lines[1]), FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def buffers(self):
        d = load("trap")
        head = label(r"So programs buffer", font_size=36).to_edge(UP, buff=0.3)
        reads = d["reads"]
        g = log_axes([0, 6, 1], [-2, 3, 1], x_length=6.2, y_length=3.8, x_label=r"bytes per \texttt{read} call",
                     y_label=r"nanoseconds per byte").to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        ax = g.ax
        cv = curve(ax, [math.log10(b) for b, _, _ in reads], [math.log10(ns) for _, ns, _ in reads], DATA)
        sc = d["strace"]
        rd = next((x["calls"] for x in sc if x["name"] == "read"), 0)
        notes = VGroup(
            label(rf"one byte per call: \ {reads[0][1]:.0f} ns a byte", font_size=21, color=NO),
            label(rf"4 KiB per call: \ {reads[6][1]:.2f} ns a byte", font_size=21, color=YES),
            label(r"the cost per call is fixed; \ spread it over more bytes", font_size=21, color=WHITE),
            label(rf"\texttt{{wc}} on 8 MiB: \ {rd} \texttt{{read}} calls \ (16 KiB each), \ "
                  rf"{d['strace_total']} system calls in all \ (\texttt{{strace -c}})", font_size=21, color=HEAD),
            label(r"C's \texttt{getc} is a macro over a buffer; \ so is our PebbleOS library: \ 4 KiB per "
                  r"\texttt{read}", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "Because each call has a fixed cost, programs ask for as much as they can at once. <bookmark mark='a'/> "
            "Here we read a file that is already in memory, with buffers from one byte to a mebibyte. <bookmark "
            "mark='b'/> One byte per call costs two hundred and eighteen nanoseconds per byte. <bookmark mark='c'/> "
            "Four kibibytes per call costs a tenth of a nanosecond per byte, two thousand times less. <bookmark "
            "mark='d'/> The line has slope minus one until the copying itself dominates: a fixed price per call, "
            "spread over more bytes. <bookmark mark='e'/> Watch a real program with strace, the tool that prints "
            "every system call: the word counter wc reads eight mebibytes in five hundred and seventeen calls, of "
            "sixteen kibibytes each. <bookmark mark='f'/> This is why C's getc was traditionally a macro over a "
            "buffer, and why our PebbleOS programs link a small library that reads four kibibytes at a time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(cv), run_time=2.0)
            for mk, n_ in zip("bcdef", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
