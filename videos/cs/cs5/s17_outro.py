from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, load, nand_latch, wave


def tile(content, caption, color, TW=3.6, TH=2.3):
    box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D, stroke_width=1.5,
                           fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(box.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.3)
    return Group(box, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        lat = nand_latch(scale=0.8)
        ph = load("phase")
        ax = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=2.2, y_length=2.2, tips=False,
                  axis_config={"color": GREY_D})
        trs = VGroup(ax, *[VMobject(color=HEAD, stroke_width=2).set_points_as_corners([ax.c2p(x, y) for x, y in t])
                           for t in ph["trajs"]])
        m = load("meta")
        sv = [(t, p) for t, p in m["surv"] if p > 0]
        ax2 = Axes(x_range=[0, 12, 4], y_range=[-5, 0, 1], x_length=2.6, y_length=2.0, tips=False,
                   axis_config={"color": GREY_D})
        surv = VGroup(ax2, VMobject(color=NO, stroke_width=3).set_points_as_corners(
            [ax2.c2p(t, np.log10(p)) for t, p in sv]))
        fsm = MathTex(r"\equiv_L \text{ classes} = \text{states}", font_size=34, color=CODE)
        lf = VGroup(*[MathTex(format(v, "04b")[::-1], font_size=18, color=DATA) for v in load("lfsr")["seq4"][:8]]).arrange(
            DOWN, buff=0.02)
        dr = load("dram")
        ax3 = Axes(x_range=[0, 0.256, 0.064], y_range=[0, 1, 1], x_length=2.8, y_length=1.8, tips=False,
                   axis_config={"color": GREY_D})
        dram = VGroup(ax3, VMobject(color=YES, stroke_width=3).set_points_as_corners(
            [ax3.c2p(a, b) for a, b in zip(dr["t"], dr["v_ref"])]))
        tiles = Group(
            tile(lat, r"feedback: \ the SR latch", YES),
            tile(trs, r"two wells and a saddle", HEAD),
            tile(surv, r"metastability: \ an exponential tail", NO),
            tile(fsm, r"Myhill--Nerode", CODE),
            tile(lf, r"LFSRs: \ period $2^n - 1$", DATA),
            tile(dram, r"DRAM: \ refresh or forget", YES),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Memory and Time", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. Feedback, and the SR latch that holds a bit. The latch as a dynamical system, "
            "with two wells and a saddle, and metastability, whose undecided tail falls off exponentially and never "
            "reaches zero. Flip-flops, the clock, setup and hold, and the synchronizer. Finite-state machines, and the "
            "Myhill-Nerode theorem that gives the smallest one. Shift registers that count through every non-zero "
            "state, Pebble's register file, and memory chips that must rewrite their bits to keep them."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"registers, \ the clock, \ the register file", [6, 7]),
            (r"SRAM and DRAM", [9]),
            (r"finite automata and Myhill--Nerode", [12, 25]),
            (r"LFSRs over $\mathrm{GF}(2)$", [28, 29]),
            (r"Rowhammer and leaky abstractions", [32, 42]),
            (r"synchronizers and arbiters", [10, 38]),
        ], font_size=26)
        with self.voiceover(
            "Where this comes back. Registers, the clock and the register file become Pebble in Part 6, and Part 7 "
            "slices its critical path with more registers. Static and dynamic memory are the raw material of Part 9's "
            "memory hierarchy. Finite automata are the first rung of Part 12's languages and of Part 25's limits. "
            "Shift registers over the field with two elements return as error-detecting codes in Part 28 and as "
            "ciphers in Part 29. Rowhammer returns in virtual memory and in web security, and arbiters, which decide "
            "which request came first, return when many processors, and many machines, have to agree."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"clock-domain crossings", r"synchronizers, \ handshakes \ and Gray-coded FIFOs; \ checked by special "
                                        r"tools in every chip project"),
            (r"servers", r"ECC memory corrects single-bit flips; \ refresh, \ TRR \ and memory scrubbing"),
            (r"embedded firmware", r"state machines run protocols, \ user interfaces \ and motor controllers"),
            (r"protocol code", r"TCP's connection states, \ HTTP parsers, \ regular-expression engines: \ finite "
                               r"automata in software"),
            (r"FPGAs", r"lookup tables and flip-flops; \ one-hot state machines"),
        ])
        with self.voiceover(
            "In practice: every chip with more than one clock has dozens of clock-domain crossings, each with a "
            "synchronizer or a Gray-coded queue, and special tools check them all. Servers use error-correcting "
            "memory, which repairs single flipped bits, and scrub their memory in the background. Embedded firmware "
            "is built from state machines, and so are network protocols, parsers and regular-expression engines, "
            "which are finite automata written in software."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Build an SR latch from two NOR gates. \ Which input is forbidden now, \ and what do the outputs do?",
            r"A flip-flop has $t_{cq} = 50$ ps, \ $t_{setup} = 30$ ps; \ the slowest logic path is 420 ps. \ What is "
            r"$f_{max}$? \ What if the clock reaches the second register 20 ps late?",
            r"With $\tau = 25$ ps, \ $T_0 = 20$ ps, \ $f_{clk} = 2$ GHz, \ $f_{data} = 50$ MHz, \ how long must a "
            r"synchronizer wait for an MTBF of 1000 years?",
            r"Draw a Moore machine that outputs 1 when the number of 1s read so far is divisible by 3. \ Is it minimal?",
            r"Use Myhill--Nerode to show that no finite automaton recognizes the palindromes over $\{0, 1\}$.",
            r"\textit{Build.} \ With \texttt{explainer/cs/pebble/seq.py}, \ find the period of every 5-bit LFSR, \ and "
            r"check that exactly $\varphi(31)/5 = 6$ are maximal.",
            r"$\bigstar$ \textit{Research.} \ Prove that a deterministic tracker which keeps every row below $T$ needs "
            r"about $W/T$ counters. \ Open: \ a randomized one with far fewer bits, \ safe against an adaptive attacker.",
        ], font_size=22)
        with self.voiceover(
            "Seven problems, with full solutions in the part's notes. Pause on any of them. The sixth is a build "
            "problem: it asks you to use this series' sequential-circuit library yourself. The last, marked with a "
            "star, is a research problem: a lower bound you can prove, and a better defence nobody has."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 6, \ The Stored-Program Computer", font_size=42).to_edge(UP, buff=0.6)
        code = code_block(["add  r3, r1, r2", "beq  r3, zero, done", "lw   r4, 0(r3)", "jal  ra, loop"],
                          font_size=28).move_to(DOWN * 0.2)
        q = label(r"how does a pile of gates run a program?", font_size=30, color=HEAD).next_to(code, DOWN, buff=0.5)
        with self.voiceover(
            "Next time: the stored-program computer, the end of act one. We have gates, adders, an ALU, registers and "
            "memory. Part 6 puts them together, with a program counter, an instruction decoder and a control unit, "
            "into Pebble itself: a thirty-two-bit processor, built from NAND gates, that fetches its own instructions "
            "from memory and runs them, including the Euclid program of Part 1."
        ):
            self.play(FadeIn(nxt), FadeIn(code), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Harris and Harris, \textit{Digital Design and Computer Architecture}, ch. 3",
             r"Nisan and Schocken, \textit{The Elements of Computing Systems}, ch. 3",
             r"Sipser, \textit{Introduction to the Theory of Computation}, ch. 1; \ Hopcroft, Motwani and Ullman, ch. 4",
             r"Jacob, Ng and Wang, \textit{Memory Systems: Cache, DRAM, Disk}",
             r"Golomb, \textit{Shift Register Sequences}",
             r"Strogatz, \textit{Nonlinear Dynamics and Chaos}, ch. 6"],
            [r"Mealy (1955); \ Moore, ``Gedanken-experiments on sequential machines'' (1956)",
             r"Myhill (1957); \ Nerode, ``Linear automaton transformations'' (1958); \ Hopcroft (1971)",
             r"Chaney and Molnar, ``Anomalous behavior of synchronizer and arbiter circuits'' (1973); \ Ginosar, "
             r"``Metastability and synchronizers'' (2011)",
             r"Dennard, DRAM cell patent (1968); \ Kim et al., ``Flipping bits in memory without accessing them'' (2014)",
             r"Seaborn and Dullien, Project Zero (2015); \ Frigo et al., ``TRRespass'' (2020)",
             r"Muller and Bartky, ``A theory of asynchronous circuits'' (1959)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
