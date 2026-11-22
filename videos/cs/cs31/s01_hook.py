from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, DATA, HEAD, KERN, NO, PART, YES, gantt, load, mono, time_axis)


class Hook(WatchScene):
    def construct(self):
        self.idle()
        self.boot()
        self.title(PART)

    def idle(self):
        h = load("history")
        head = label(r"A machine worth millions, \ waiting for a person", font_size=36).to_edge(UP, buff=0.3)
        W = 11.0
        think, burst = h["Z"], h["S"]
        cycle = think + burst
        bars = VGroup()
        t, x0 = 0.0, -W / 2
        for _ in range(4):
            for dur, col, name in ((think * 0.92, GREY_D, "thinking"), (burst, YES, "computing"),
                                   (think * 0.08, GREY_D, "")):
                w = W * dur / (4 * cycle)
                r = Rectangle(width=w, height=0.55, stroke_width=0, fill_color=col, fill_opacity=0.85)
                r.move_to([x0 + t + w / 2, 1.1, 0])
                bars.add(r)
                t += w
        cap = VGroup(label(r"one user at the console: \ think 10 s, \ compute 0.5 s", font_size=22, color=WHITE),
                     label(rf"the processor is idle {h['idle_one'] * 100:.0f}\% of the time", font_size=24,
                           color=NO)).arrange(DOWN, buff=0.15).next_to(bars, DOWN, buff=0.35)
        lines = VGroup(
            label(r"1950s: \ \textbf{batch}: \ jobs on punched cards, \ queued by an operator, \ results hours later",
                  font_size=22, color=GREY_A),
            label(r"1961: \ \textbf{time-sharing}: \ many users at once, \ each given the machine for a fraction of a "
                  r"second", font_size=22, color=YES),
            label(r"each user sees a whole computer; \ the computer sees a queue", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1960 a computer cost millions of dollars, and it spent most of its time waiting. <bookmark mark='a'/> "
            "Put one person at the console, and the pattern is always the same: think for ten seconds, then ask for "
            "half a second of computing. <bookmark mark='b'/> The processor sits idle ninety-five percent of the time. "
            "<bookmark mark='c'/> The first answer was batch processing: hand your program to an operator on punched "
            "cards, and come back for the printout hours later. The machine stayed busy, and programmers waited. "
            "<bookmark mark='d'/> The second answer was time-sharing: connect many terminals, and give each user the "
            "machine for a fraction of a second in turn. <bookmark mark='e'/> Every user then sees a whole computer of "
            "their own, while the computer itself works through a queue."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.08), FadeIn(cap[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cap[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def boot(self):
        d = load("boot")
        head = label(r"PebbleOS boots, \ and runs two programs at once", font_size=34).to_edge(UP, buff=0.3)
        T = d["steps"]
        g = gantt(d["timeline"], 0, T, width=11.4, h=0.55, lanes=["A", "B", "kernel"], font=20)
        g.move_to(UP * 0.9).shift(RIGHT * 0.35)
        ax = time_axis(g, [0, 5000, 10000, T // 1000 * 1000], font=14)
        axl = label(r"instructions executed", font_size=16, color=GREY_B).next_to(ax, DOWN, buff=0.08)
        out = d["output"]
        screen = mono(out, 24, YES).next_to(axl, DOWN, buff=0.4)
        if screen.width > 11.0:
            screen.scale_to_fit_width(11.0)
        r = d["report"]
        notes = VGroup(
            label(rf"both programs print their letter 24 times; \ the timer cuts in every {d['quantum']} "
                  rf"instructions", font_size=21, color=WHITE),
            label(rf"{r['switches']} switches between them, \ {r['ticks']} timer interrupts, \ {r['syscalls']} system "
                  r"calls", font_size=21, color=HEAD),
            label(rf"the kernel ran {r['ksteps'] / r['steps'] * 100:.0f}\% of all instructions here: \ a system call "
                  r"for every letter", font_size=21, color=KERN),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "By the end of this part, our own machine will do the same. Here is PebbleOS, a kernel we are about to "
            "write, booting on the Pebble computer with two programs loaded. <bookmark mark='a'/> Each program prints "
            "its letter, A or B, twenty-four times. <bookmark mark='b'/> The chart shows who has the processor, "
            "instruction by instruction: program A, then the kernel, in orange, then program B. A timer interrupts "
            "whichever program is running every nine hundred instructions, and the kernel hands the processor to the "
            "other. <bookmark mark='c'/> The output interleaves. Neither program knows the other exists. "
            "<bookmark mark='d'/> Fifteen switches, fourteen timer interrupts, fifty-two system calls. <bookmark "
            "mark='e'/> And here the kernel itself ran forty-four percent of all instructions, because every single "
            "letter was a request to the kernel. Making that cheaper is part of the story."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g.lane_labels), FadeIn(ax), FadeIn(axl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in g.bars], lag_ratio=0.02), run_time=3.0)
            vo.wait_until("c")
            self.play(AddTextLetterByLetter(screen), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

