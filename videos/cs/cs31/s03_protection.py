from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono)


class Protection(VoiceoverScene):
    def construct(self):
        self.card()
        self.danger()
        self.hardware()
        self.experiment()

    def card(self):
        card = chapter_card(2, r"Protection: \ the mode bit", r"What stops one program from wrecking another?",
                            lit=(1961, 1964), extra=((1961, r"CTSS"), (1964, r"System/360: \ supervisor state")),
                            part=PART)
        with self.voiceover("Chapter two. Protection, and the mode bit."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def danger(self):
        p = load("protect")
        head = label(r"Three ways to ruin everyone's day", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup()
        for code_, what, color in (
                ("halt", r"an instruction: \ stop the machine, \ or reprogram its devices", NO),
                ("sw   t1, 0x100(zero)", r"memory: \ overwrite the kernel, \ or another program", HEAD),
                ("loop: j loop", r"time: \ never give the processor back", LAM)):
            rows.add(VGroup(mono(code_, 22, color), label(what, font_size=22, color=WHITE)))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.5)
            r[1].shift(RIGHT * (4.2 - r[0].width))
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).next_to(head, DOWN, buff=0.7)
        lines = VGroup(
            label(rf"on the bare Pebble of Parts 6--30, \ a program's \texttt{{halt}} ends everything: \ the machine "
                  rf"stopped after {p['bare_halted_at']} instructions", font_size=21, color=NO),
            label(r"so three things must be taken away from programs: \ some \textbf{instructions}, \ most of "
                  r"\textbf{memory}, \ and control of \textbf{time}", font_size=21, color=YES),
            label(r"and the kernel must be the only way to get them back", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Before time-sharing, the one program running owned the machine, and could do anything. With several "
            "programs at once, any one of them can ruin everybody's day, in three ways. <bookmark mark='a'/> By an "
            "instruction: halting the machine, or reprogramming a device. <bookmark mark='b'/> By memory: storing "
            "over the kernel, or over another program's data. <bookmark mark='c'/> And by time: a loop that never "
            "gives the processor back. <bookmark mark='d'/> On the Pebble we have built so far, a single halt in "
            "any program stops everything. <bookmark mark='e'/> So the hardware must take three things away from "
            "ordinary programs: some instructions, most of memory, and control of time. <bookmark mark='f'/> And "
            "there must be exactly one way to ask for them back, through the kernel."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            for mk, ln in zip("def", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def hardware(self):
        head = label(r"Pebble gains a kernel mode", font_size=36).to_edge(UP, buff=0.3)
        tab = grid_table([r"instruction", r"opcode", r"what it does"], [
            [r"\texttt{ecall}", r"48", r"trap into the kernel: \ the one door"],
            [r"\texttt{eret}", r"49", r"return from a trap, \ to the saved mode and pc"],
            [r"\texttt{csrr rd, csr}", r"50", r"read a control register"],
            [r"\texttt{csrw csr, rs}", r"51", r"write a control register"],
        ], widths=[2.9, 1.3, 6.2], row_h=0.5, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.4)
        regs = VGroup(*[VGroup(RoundedRectangle(width=1.38, height=0.5, corner_radius=0.08, stroke_color=c,
                                                stroke_width=2, fill_color=BG, fill_opacity=1),
                               mono(n, 17, c)) for n, c in
                        (("status", YES), ("epc", HEAD), ("cause", HEAD), ("tval", HEAD), ("tvec", KERN),
                         ("scratch", GREY_B), ("timer", LAM), ("lo", DATA), ("hi", DATA))])
        for r in regs:
            r[1].move_to(r[0])
        regs.arrange(RIGHT, buff=0.1).next_to(tab, DOWN, buff=0.45)
        rl = label(r"control registers, \ kernel only", font_size=18, color=GREY_B).next_to(regs, DOWN, buff=0.1)
        lines = VGroup(
            label(r"a \textbf{mode bit}: \ the machine starts in kernel mode; \ \texttt{eret} drops to user mode",
                  font_size=21, color=YES),
            label(r"in user mode: \ \texttt{csrr}, \ \texttt{csrw}, \ \texttt{eret}, \ \texttt{halt} are "
                  r"\textbf{illegal}; \ addresses outside [\texttt{lo}, \texttt{hi}) \ and the devices \textbf{fault}",
                  font_size=21, color=NO),
            label(r"\texttt{timer} counts down each instruction; \ at zero, \ an \textbf{interrupt}: \ time comes "
                  r"back to the kernel", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is what Pebble gains, in under two hundred lines of the emulator. <bookmark mark='a'/> Four "
            "instructions, in the opcodes we left free in Part 6. E-call traps into the kernel; it is the one door. "
            "E-ret returns from a trap. And two instructions read and write control registers. <bookmark mark='b'/> "
            "The control registers hold the mode, where a trap happened and why, where traps should go, a countdown "
            "timer, and the bounds of the memory the running program may touch. <bookmark mark='c'/> And one bit of "
            "state, the mode. The machine starts in kernel mode, and the only way down to user mode is e-ret. "
            "<bookmark mark='d'/> In user mode, the privileged instructions are illegal, and any address outside "
            "the bounds, or in the device page, is a fault. <bookmark mark='e'/> The timer counts instructions down; "
            "at zero it interrupts whatever is running, and hands the processor back to the kernel. IBM's System/360 "
            "had the same idea in 1964, and called the two modes the problem state and the supervisor state."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*row)) for row in tab.cells[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in regs], lag_ratio=0.1), FadeIn(rl))
            for mk, ln in zip("cde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def experiment(self):
        p = load("protect")
        head = label(r"Four processes, \ three of them hostile", font_size=34).to_edge(UP, buff=0.3)
        procs = {q["name"]: q for q in p["procs"]}
        fate = {
            "good": rf"printed its {len(p['output'])} letters, \ exit 0",
            "halter": rf"killed: \ illegal instruction \ (exit {procs['halter']['exit']})",
            "scribbler": rf"killed: \ store fault at \texttt{{0x100}} \ (exit {procs['scribbler']['exit']})",
            "hog": rf"preempted {procs['hog']['ticks']} times by the timer; \ finished",
        }
        what = {"good": r"prints A, \ twelve times", "halter": r"executes \texttt{halt}",
                "scribbler": r"stores into the kernel", "hog": r"loops 60{,}000 times, \ no system calls"}
        tab = grid_table([r"process", r"what it does", r"what happened"],
                         [[n, what[n], fate[n]] for n in ("good", "halter", "scribbler", "hog")],
                         widths=[2.0, 4.2, 6.0], row_h=0.58, font_size=21, mono_cols=(0,))
        tab.next_to(head, DOWN, buff=0.5)
        for r, c in zip((1, 2, 3, 4), (YES, NO, NO, LAM)):
            tab.cells[r][2].set_color(c)
        lines = VGroup(
            label(r"each fault is a \textbf{trap}: \ the hardware stops the instruction and jumps to the kernel, "
                  r"\ which kills only the offender", font_size=21, color=WHITE),
            label(rf"the hog is interrupted every 2{{,}}000 instructions; \ the others run between its slices",
                  font_size=21, color=LAM),
            label(r"protection costs nothing while programs behave: \ a comparison in hardware on each access",
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Now the test. PebbleOS starts four processes, three of them hostile. <bookmark mark='a'/> One prints the "
            "letter A twelve times. One executes halt. One stores a zero into the kernel's memory. And one loops "
            "sixty thousand times without ever calling the kernel. <bookmark mark='b'/> The halt is an illegal "
            "instruction in user mode: the hardware refuses it and traps, and the kernel kills that process. The "
            "store is outside the process's bounds: another trap, another kill. <bookmark mark='c'/> The hog is "
            "interrupted by the timer a hundred and twenty-one times, and the other processes run in between. The "
            "good process prints all twelve letters. <bookmark mark='d'/> In every case the offending instruction "
            "never completes. The hardware stops it and jumps into the kernel, which decides what to do. <bookmark "
            "mark='e'/> And protection is nearly free while programs behave: a comparison the hardware makes on "
            "every access, in parallel with the access itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r][:2])) for r in range(1, 5)], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(tab.cells[2][2]), FadeIn(tab.cells[3][2]))
            vo.wait_until("c")
            self.play(FadeIn(tab.cells[4][2]), FadeIn(tab.cells[1][2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()
