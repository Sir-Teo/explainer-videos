from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, curve, fit_right, log_axes, load,
                                   mono)

PH = {"save": DATA, "dispatch": HEAD, "handle": YES, "restore": LAM}


class Traps(WatchScene):
    def construct(self):
        self.card()
        self.sequence()
        self.dive()
        self.costs()

    def card(self):
        self.chapter(3, r"Traps and the system call", r"How does a program ask the kernel for anything?", lit=(1961, 1974), extra=((1961, r"CTSS"), (1974, r"Unix's system calls")), part=PART, said="Chapter three. Traps, and the system call.")

    def sequence(self):
        self.wrong_idea(r"the kernel runs in the background, \\ watching every program",
                        r"the kernel runs only when a trap, \\ an interrupt or a system call brings it in",
                        narration="A common picture: the operating system is always running in the background, watching.",
                        right_narration="In fact the kernel runs only when something brings it in: a system call, a fault, or "
                                        "an interrupt such as the timer. The rest of the time, your program owns the processor.")
        self.clear_scene()
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
            body = VGroup(*[mono(s, 18, PH[ph] if s != "..." else GREY_C) for s in show]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.09)
            t = label(rf"{title}: \ {counts.get(ph, 0)}", font_size=22, color=PH[ph])
            cols.add(VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.15))
        cols.arrange(RIGHT, buff=0.4, aligned_edge=UP).next_to(strip, DOWN, buff=0.5)
        if cols.width > 13.2:
            cols.scale_to_fit_width(13.2).next_to(strip, DOWN, buff=0.5)
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
        self.ask(r"A function call: $1.5$ ns. \\ A system call costs...", [r"about the same",
                 r"tens to hundreds of times more", r"a million times more"], 1,
                 say="An ordinary function call takes a nanosecond and a half. What does a system call cost?",
                 reveal="Tens to hundreds of times more: the trap, the checks, and the way back.")
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

