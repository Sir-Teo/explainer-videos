from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from explainer.cs.pebble import isa as I
from videos.cs.cs6.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, Datapath, box, fmt,
                                  load, sci, word_bits)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        isa = load("isa")
        ex = isa["examples"][0]
        wb = word_bits(ex["word"], ex["fields"], cell=0.2, font_size=12)
        dp = Datapath()
        ctl = load("control")
        grid = VGroup(*[Rectangle(width=0.1, height=0.06, stroke_width=0, fill_color=HEAD if b else GREY_D,
                                  fill_opacity=0.9 if b else 0.3).move_to([j * 0.11, -i * 0.07, 0])
                        for i, r in enumerate(ctl["rows"]) for j, b in enumerate(r["bits"])])
        prog = load("programs")["euclid"]
        ax = Axes(x_range=[0, 60, 20], y_range=[0, 1100, 500], x_length=3.0, y_length=2.0, tips=False,
                  axis_config={"color": GREY_D})
        a0 = [r["regs"][0] for r in prog["rows"]]
        st = VGroup(ax, VMobject(color=DATA, stroke_width=3).set_points_as_corners(
            [p for k, y in enumerate(a0) for p in (ax.c2p(k, y), ax.c2p(k + 1, y))]))
        job = load("job")
        led = ledger_table([{"part": 6, "label": r"Pebble", "seconds": job["corpus"]["cycles"] / 1e9}], font_size=18,
                           row_h=0.4, label_width=1.6, bar_width=3.0)
        tm = MathTex(r"\text{Pebble} \leftrightarrow \text{Turing}", font_size=32, color=FUNC)
        tiles = Group(
            tile(wb, r"an instruction set, \ bit by bit", CODE),
            tile(dp, r"the single-cycle datapath", YES),
            tile(grid, r"control: \ a truth table", CTRL),
            tile(st, r"Euclid, \ gate by gate", DATA),
            tile(led, r"the Job: \ ledger row 0", COST),
            tile(tm, r"universality, \ closed", FUNC),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ The Stored-Program Computer", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. An instruction set, designed bit by bit. A single-cycle datapath, assembled "
            "from the circuits of Parts 3 to 5, and a control unit that is a truth table, built two ways. An "
            "assembler, the first programs, and devices at memory addresses. A gate-level machine that agrees with its "
            "emulator on every program we tried, runs Euclid and a Turing machine, and counts the words of a "
            "paragraph. And the first row of the ledger: a hundred and seven billion cycles for thirty novels."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the single-cycle datapath and its critical path", [7, 8]),
            (r"loads, \ stores, \ and the memory behind them", [9]),
            (r"\texttt{jal}, \ \texttt{jalr} \ and the calling convention", [11]),
            (r"a compiler that targets Pebble", [13]),
            (r"interrupts, \ exceptions, \ the operating system", [31, 32]),
            (r"the Job's ledger", [7, 9, 10, 13, 16, 17]),
        ], font_size=26)
        with self.voiceover(
            "Where this comes back. Part 7 cuts the single-cycle machine's long path into a pipeline, and Part 8 runs "
            "instructions out of order. Part 9 builds the memory hierarchy behind the loads and stores. Part 11 turns "
            "jump-and-link into a calling convention, and Part 13 writes a compiler whose output runs on Pebble. "
            "Interrupts and exceptions become an operating system in Parts 31 and 32. And the ledger gains a row each "
            "time the Job gets faster, from better hardware or better ideas."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"instruction sets", r"RISC-V in microcontrollers and data centres; \ ARM in phones and laptops; \ x86 in "
                                  r"PCs and servers"),
            (r"emulators", r"QEMU runs one instruction set on another; \ console emulators are emulators like ours"),
            (r"simulators", r"gem5 and cycle-accurate models: \ how processors are designed before they are built"),
            (r"memory-mapped I/O", r"every microcontroller: \ GPIO, \ UARTs, \ timers \ are addresses"),
            (r"co-simulation", r"chip teams check RTL against an instruction-set model, \ exactly as this part did"),
        ])
        with self.voiceover(
            "In practice: RISC-V now runs in microcontrollers and data centres, ARM in phones and laptops, x86 in PCs "
            "and servers. QEMU runs one instruction set on another, the same idea as our emulator. Simulators like "
            "gem5 are where processors are designed before they are built. Every microcontroller's peripherals are "
            "addresses. And every chip team checks its hardware description against an instruction-set model, "
            "running random programs on both, exactly as this part did."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Encode \texttt{sub t0, a1, a2} \ and \ \texttt{sw t0, -8(sp)} \ in hexadecimal, \ field by field.",
            r"Write the control word for \texttt{jalr ra, 4(t1)}: \ which of the 20 signals are 1?",
            r"Instruction and data memory take 1 ns each; \ the logic path is 56 gate delays of 10 ps, \ plus 70 ps of "
            r"flip-flop overhead. \ What is $f_{max}$? \ How much faster could a machine run that never touched data "
            r"memory?",
            r"Write a Pebble program that reverses a zero-terminated string in place. \ How many instructions does it "
            r"run for a string of $n$ letters?",
            r"Write a program that turns one of its own \texttt{beq} instructions into a \texttt{bne}. \ Why does this "
            r"work on single-cycle Pebble, \ and why might it fail on a pipeline?",
            r"\textit{Build.} \ Change \texttt{JOB\_V0} so that a word that is found swaps places with the entry above "
            r"it. \ Run both versions on chapter 1 with the emulator: \ how many instructions does the change save?",
        ], font_size=23)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The last is a build problem: "
            "it asks you to change the Job's program yourself and measure what a small idea buys."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 7, \ Pipelines", font_size=42).to_edge(UP, buff=0.6)
        stages = VGroup(*[box(1.5, 0.8, t, c, 26) for t, c in ((r"\text{fetch}", DATA), (r"\text{decode}", CTRL),
                                                              (r"\text{execute}", FUNC), (r"\text{memory}", DATA),
                                                              (r"\text{write}", YES))]).arrange(RIGHT, buff=0.25)
        stages.move_to(DOWN * 0.1)
        q = label(r"five instructions at once: \ what could go wrong?", font_size=30, color=HEAD).next_to(stages, DOWN,
                                                                                                    buff=0.6)
        with self.voiceover(
            "Next time, Act Two begins: making it fast. Pebble's clock waits for the slowest instruction. Part 7 cuts "
            "the datapath into five stages, like an assembly line, so that five instructions are in flight at once and "
            "the clock can run several times faster. Then we find out everything that goes wrong when an instruction "
            "needs a result that has not been written yet."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in stages], lag_ratio=0.2),
                      FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Patterson and Hennessy, \textit{Computer Organization and Design, RISC-V Edition}, ch. 2 and 4",
             r"Harris and Harris, \textit{Digital Design and Computer Architecture}, ch. 6--7",
             r"Nisan and Schocken, \textit{The Elements of Computing Systems}, ch. 4--6",
             r"Haigh, Priestley and Rope, \textit{ENIAC in Action} (2016)",
             r"Waterman and Asanovi\'c (eds.), \textit{The RISC-V Instruction Set Manual}, Volume I"],
            [r"von Neumann, \textit{First Draft of a Report on the EDVAC} (1945)",
             r"Booth and Booth, ``Coding for A.R.C.'' (1947)",
             r"Williams and Kilburn, ``Electronic digital computers'', \textit{Nature} 162 (1948)",
             r"Wilkes, ``The best way to design an automatic calculating machine'' (1951)",
             r"Wilkes, Wheeler and Gill, \textit{The Preparation of Programs for an Electronic Digital Computer} (1951)",
             r"Patterson and Ditzel, ``The case for the reduced instruction set computer'' (1980)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
