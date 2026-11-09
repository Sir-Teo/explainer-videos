from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, box, fmt, load, say)


class Cost(VoiceoverScene):
    def construct(self):
        self.card()
        self.iron()
        self.path()
        self.arrays()
        self.mix()

    def card(self):
        card = chapter_card(8, r"What a program costs", r"How long does a program take?", part=PART)
        with self.voiceover("Chapter eight. What a program costs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def iron(self):
        head = label(r"The iron law of performance", font_size=38).to_edge(UP, buff=0.35)
        law = MathTex(r"\text{time}", r"=", r"\text{instructions}", r"\times", r"\frac{\text{cycles}}{\text{instruction}}",
                      r"\times", r"\frac{\text{seconds}}{\text{cycle}}", font_size=44).move_to(UP * 1.2)
        law[0].set_color(COST)
        law[2].set_color(CODE)
        law[4].set_color(YES)
        law[6].set_color(CLOCK)
        braces = VGroup(
            label(r"the program \\ and the compiler \\ (Parts 13, 16--24)", font_size=22, color=CODE).next_to(law[2],
                                                                                                         DOWN, buff=0.5),
            label(r"the machine's organization \\ (CPI; \ Parts 7--9)", font_size=22, color=YES).next_to(law[4], DOWN,
                                                                                                    buff=0.35),
            label(r"the circuits \\ (Parts 3--5)", font_size=22, color=CLOCK).next_to(law[6], DOWN, buff=0.35),
        )
        peb = label(r"single-cycle Pebble: \ CPI $= 1$ exactly; \ the clock is set by the slowest instruction",
                    font_size=26, color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "How long does a program take? Computer architects call the answer the iron law of performance. "
            "<bookmark mark='a'/> Time is the number of instructions executed, times the average number of clock "
            "cycles per instruction, times the length of a cycle. <bookmark mark='b'/> The three factors belong to "
            "different people. The instruction count belongs to the algorithm and the compiler. Cycles per "
            "instruction belong to how the processor is organized. The cycle time belongs to the circuits. "
            "<bookmark mark='c'/> Our single-cycle Pebble makes the middle factor exactly one: every instruction "
            "takes one cycle. The price is that the cycle must be long enough for the slowest instruction of all."
        ) as vo:
            self.play(FadeIn(head))
            self.play(Write(law), run_time=2.0)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in braces], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(peb), Indicate(law[4], color=YES))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def path(self):
        cp = load("cpu")
        head = label(r"The slowest instruction sets the clock", font_size=38).to_edge(UP, buff=0.35)
        parts = [(r"fetch \\ (memory)", 2.2, DATA), (r"decode, \\ read registers", 1.6, YES),
                 (r"ALU", 2.0, FUNC), (r"data \\ memory", 2.2, DATA), (r"write \\ back", 1.0, YES)]
        bar = VGroup()
        for t, w, c in parts:
            r = Rectangle(width=w, height=0.8, stroke_color=BG, stroke_width=2, fill_color=c, fill_opacity=0.5)
            bar.add(VGroup(r, label(t, font_size=20, color=WHITE).move_to(r)))
        bar.arrange(RIGHT, buff=0).move_to(UP * 1.2)
        bl = label(r"a load's path through the cycle", font_size=22, color=GREY_A).next_to(bar, UP, buff=0.15)
        nums = VGroup(
            label(rf"netlist: \ depth {cp['depth']}; \ sampled maximum {cp['settle_max']} "
                  r"gate delays", font_size=24, color=GREY_A),
            label(rf"toy logic budget: \ 10 ps per gate + 70 ps registers: \ {cp['period_ps']} ps; "
                  rf"{cp['fmax_ghz']:.1f} GHz", font_size=24, color=CLOCK),
            label("assume two 1 ns accesses: \\ $T=2.63$ ns, \\ $f\\approx380$ MHz \\\\ illustrative budget; \\ not a certified hardware clock", font_size=24, color=NO),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 1.2)
        with self.voiceover(
            "The slowest instruction is the load. <bookmark mark='a'/> In one cycle it must fetch itself from memory, "
            "be decoded, read a register, add the offset in the ALU, read the data memory, and write the result back. "
            "<bookmark mark='b'/> The series' library measures the logic part of that path in the netlist itself. The "
            "deepest chain of gates is fifty-nine long; the unit-delay simulation observes at most fifty-six gate "
            "delays across four thousand and ninety-six sampled inputs. That sample maximum is not a worst-case timing"
            " proof. For a teaching budget, assume fifty-six ten-picosecond delays and seventy picoseconds of register"
            " overhead: six hundred and thirty picoseconds before memory. <bookmark mark='c'/> But the two memory "
            "accesses are in the cycle too, and our budget assumes one nanosecond for each. The assumed total is two "
            "point six three nanoseconds, or about three hundred and eighty megahertz. This is a model, not a measured"
            " silicon clock. An add still fetches its instruction, and waits through the cycle budget for a load's "
            "data access too. Part 7 fixes that by cutting the path into pieces."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bl),
                      LaggedStart(*[GrowFromEdge(b, LEFT) for b in bar], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(nums[0]))
            self.play(FadeIn(nums[1]))
            vo.wait_until("c")
            self.play(FadeIn(nums[2]), Indicate(bar[0], color=NO), Indicate(bar[3], color=NO))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def arrays(self):
        d = load("programs")["array"]
        head = label(r"A loop over an array", font_size=38).to_edge(UP, buff=0.35)
        src = [s_ for s_ in d["source"] if s_.strip() and not s_.strip().startswith(("array:", ".align"))]
        lines = VGroup(*[Text(s_.rstrip()[:56], font="DejaVu Sans Mono", font_size=19, color=CODE) for s_ in src])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(LEFT * 2.8 + UP * 0.7)
        k0 = next(i for i, s_ in enumerate(src) if s_.strip().startswith("loop:"))
        body = VGroup(*lines[k0:k0 + 5])
        work = VGroup(*lines[k0:k0 + 2])
        over = VGroup(*lines[k0 + 2:k0 + 5])
        bw = SurroundingRectangle(work, buff=0.05, color=YES, stroke_width=2)
        bo = SurroundingRectangle(over, buff=0.05, color=NO, stroke_width=2)
        lab = VGroup(label(r"the work", font_size=20, color=YES).next_to(bw, RIGHT, buff=0.2),
                     label(r"the bookkeeping", font_size=20, color=NO).next_to(bo, RIGHT, buff=0.2))
        mem = VGroup(*[Square(0.34, stroke_color=DATA, stroke_width=1.2) for _ in range(10)]).arrange(RIGHT, buff=0.02)
        mem.move_to(RIGHT * 3.4 + UP * 2.0)
        ptr = Triangle(color=HEAD, fill_opacity=1).scale(0.08).rotate(PI).next_to(mem[0], UP, buff=0.04)
        facts = VGroup(
            MathTex(rf"6 + 5n + 1 = {d['steps']} \ \text{{instructions for }} n = 100", font_size=30, color=COST),
            label(rf"sum $= {d['regs'][3]}$, \ gate level $=$ emulator", font_size=22, color=YES),
            label(r"3 of every 5 instructions only move the loop along: \\ a compiler can \textit{unroll} it, \ four "
                  r"elements per trip \ (Part 13)", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 2.2 + DOWN * 1.9)
        with self.voiceover(
            "Most real work is a loop over data, so it is worth costing one exactly. <bookmark mark='a'/> This loop "
            "adds a hundred numbers stored in memory. A pointer register walks along the array a word at a time, and a "
            "counter counts down. <bookmark mark='b'/> Each trip runs five instructions: a load and an add do the work, "
            "and three more move the pointer, decrement the counter and branch back. With six instructions to start "
            "and a halt, that is five hundred and seven for a hundred elements, and the gate-level machine agrees. "
            "<bookmark mark='c'/> Three in every five instructions are bookkeeping. A compiler can unroll the loop, "
            "handling four elements per trip so the bookkeeping is paid a quarter as often, which is one of the "
            "optimizations Part 13 builds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines))
            self.play(FadeIn(mem), FadeIn(ptr))
            vo.wait_until("a")
            for k in range(1, 5):
                self.play(ptr.animate.next_to(mem[k], UP, buff=0.04), run_time=0.3)
            vo.wait_until("b")
            self.play(Create(bw), Create(bo), FadeIn(lab))
            self.play(Write(facts[0]))
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mix(self):
        j = load("job")["chapter"]
        counts = sorted(j["counts"].items(), key=lambda kv: -kv[1])[:10]
        total = j["steps"]
        head = label(r"What a real program executes", font_size=38).to_edge(UP, buff=0.35)
        ax_w = 7.0
        bars = VGroup()
        for k, (op, n) in enumerate(counts):
            w = ax_w * n / counts[0][1]
            r = Rectangle(width=w, height=0.34, stroke_width=0, fill_color=COST, fill_opacity=0.8)
            name = Text(op, font="DejaVu Sans Mono", font_size=18, color=CODE)
            pct = label(rf"{100 * n / total:.1f}\%", font_size=18, color=GREY_B)
            row = VGroup(name, r, pct)
            name.move_to([-4.3, 2.0 - 0.42 * k, 0], aligned_edge=RIGHT)
            r.move_to([-4.1 + w / 2, 2.0 - 0.42 * k, 0])
            pct.next_to(r, RIGHT, buff=0.1)
            bars.add(row)
        cap = label(rf"the Job, \ version 0, \ on chapter 1 of \textit{{Pride and Prejudice}}: \ "
                    rf"{fmt(total)} instructions", font_size=22, color=GREY_A).to_edge(DOWN, buff=1.0)
        notes = VGroup(
            label(r"adds, \ compares and branches, \ loads: \ the common case", font_size=22, color=YES),
            label(r"multiplies and divides: \ never \ (Pebble has none yet)", font_size=22, color=GREY_B),
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Which instructions does a real program actually run? <bookmark mark='a'/> Here is the Job, version zero, "
            "counting the words of the first chapter of Pride and Prejudice: eight hundred thousand instructions, "
            "sorted by kind. <bookmark mark='b'/> A quarter are add-immediates, mostly stepping pointers and counters. "
            "Then branches, loads, and jumps back to the top of a loop. Arithmetic beyond addition hardly appears. "
            "<bookmark mark='c'/> This is the evidence behind the design rule to make the common case fast: real "
            "programs mostly move data, compare it and branch, and that is what the hardware should do quickly."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(cap), LaggedStart(*[GrowFromEdge(b[1], LEFT) for b in bars], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(b[0]) for b in bars], lag_ratio=0.1), run_time=2.4)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b[2]) for b in bars], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(Indicate(bars[0], color=YES))
            vo.wait_until("c")
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()

