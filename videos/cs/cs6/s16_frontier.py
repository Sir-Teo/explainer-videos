from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, LIMIT, NO, PART, YES, box, fmt, load,
                                  say)


class Frontier(VoiceoverScene):
    """The research tier (videos/cs/SYLLABUS.md 1.1): how good is the random co-simulation this part relied on?
    Mutation analysis on the emulator; coverage-guided CPU fuzzing; formal specifications and verified processors."""

    def construct(self):
        self.card()
        self.mutants()
        self.odds()
        self.fuzzing()
        self.formal()

    def card(self):
        card = chapter_card(15, r"Frontier: \ is the processor right?", r"How much can random tests prove?",
                            lit=(1994, 2017, 2024), part=PART,
                            extra=((1994, r"the Pentium FDIV bug, found by hand"), (2017, r"Kami: a verified RISC-V core"),
                                   (2024, r"Cascade: 37 CPU bugs")))
        with self.voiceover("Chapter fifteen. Frontier: is the processor right?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def mutants(self):
        d = load("mutants")
        head = label(r"Plant a bug, \ and count the programs that catch it", font_size=34).to_edge(UP, buff=0.3)
        sub = label(rf"one bug at a time in a copy of the emulator; \ ${fmt(d['programs'])}$ random programs \\ (the "
                    r"generator extended with multiply and divide; emulator study)", font_size=20,
                    color=GREY_B).next_to(head, DOWN, buff=0.15)
        rows = VGroup()
        for k, r in enumerate(d["rows"]):
            y = 1.6 - 0.46 * k
            v = r["rate"]
            w = 5.6 * v / max(x["rate"] for x in d["rows"])
            col = YES if v > 0.05 else (HEAD if v > 0 else LIMIT)
            bar = Rectangle(width=max(w, 0.03), height=0.32, stroke_width=0, fill_color=col,
                            fill_opacity=0.8).move_to([0.6 + w / 2, y, 0])
            name = r["bug"].replace("-2^31", r"$-2^{31}$").replace("by -1", r"by $-1$")
            rows.add(VGroup(label(name, font_size=19, color=GREY_A).next_to([0.45, y, 0], LEFT, buff=0.1),
                            bar, label(rf"{100 * v:.2f}\%" if v else r"0 / 2,000", font_size=19,
                                       color=col).next_to(bar, RIGHT, buff=0.12)))
        cap = note(r"share of programs whose final registers, \ memory or output differ", font_size=18).to_edge(
            DOWN, buff=0.35)
        top = d["rows"][[r["rate"] for r in d["rows"]].index(max(r["rate"] for r in d["rows"]))]
        with self.voiceover(
            "This part trusted random programs: the gate-level machine had to agree with the emulator on hundreds of "
            "them. How much does that prove? Verification engineers answer with mutation analysis. <bookmark "
            "mark='a'/> Plant one known bug in a copy of the emulator, run two thousand fixed-seed random programs on "
            "it, using the generator with a multiply-and-divide extension, and count how many end differently. "
            "<bookmark mark='b'/> Some bugs are caught almost at once: a store that also writes the next byte shows up"
            " in two programs out of three, and shifts that read only four bits of their amount in more than half. "
            "<bookmark mark='c'/> Others are rare. A byte load that forgets its sign shows up in one program in four "
            "hundred, because memory mostly holds zeros, and a branch that misbehaves only when both registers are "
            "zero in one in forty. <bookmark mark='d'/> And one bug is caught by zero of these two thousand programs: "
            "dividing minus two to the thirty-one by minus one, the single input where a thirty-two-bit quotient "
            "overflows. That observation does not give its true hit probability. The generator evolves correlated "
            "register values and forces the divisor odd; there is no justified one-in-four-billion rate for this "
            "experiment. This study mutates the instruction emulator, not a gate-level divider."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(rows[:5]))
            self.play(FadeIn(cap))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Indicate(rows[:5], color=YES, scale_factor=1.02), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[5:8]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[8]))
            self.play(Indicate(rows[8][0], color=LIMIT))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def odds(self):
        d = load("mutants")
        head = label(r"How many programs are enough?", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 1, 0.25], x_length=6.6, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(LEFT * 2.2 + DOWN * 0.4)
        xt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.12)
                      for k in range(0, 7, 2)])
        yt = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v, t in ((0.5, r"50\%"), (1, r"100\%"))])
        xl = note(r"random programs run", font_size=18).next_to(xt, DOWN, buff=0.08)
        yl = note(r"chance the bug has been caught", font_size=18).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        pick = [r for r in d["rows"] if r["bug"] in ("sb also writes the next byte", "sltu: equal counts as less",
                                                     "lb forgets the sign")]
        cols = [YES, DATA, HEAD]
        curves, tags = VGroup(), VGroup()
        xs = np.linspace(0, 6, 120)
        for j, (r, c) in enumerate(zip(pick, cols)):
            ys = 1 - (1 - r["rate"]) ** (10 ** xs)
            curves.add(VMobject(color=c, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)]))
            x50 = np.log10(np.log(0.5) / np.log(1 - r["rate"]))
            # A common bug reaches 50% before the plotted domain begins.
            # Keep its label inside the plot, clear of the 50% axis tick.
            tags.add(label(r["bug"], font_size=16, color=c).next_to(ax.c2p(max(0.25, x50), 0.5), RIGHT, buff=0.15).shift(
                DOWN * 0.32 * j))
        div_r = 2.0 ** -32
        ys = 1 - (1 - div_r) ** (10 ** xs)
        divc = VMobject(color=LIMIT, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])
        divl = label("illustration only: \\ $r=2^{-32}$ \\\\ per independent test", font_size=16, color=LIMIT).next_to(
            ax.c2p(6, 0.02), UP + LEFT, buff=0.1)
        eq = MathTex(r"P(\text{caught in } N) = 1 - (1 - r)^{N}", font_size=27, color=GREY_A).to_edge(RIGHT, buff=0.5
                                                                                                    ).shift(UP * 1.4)
        side = VGroup(
            label("assumption: \\ independent tests, \\ fixed true rate $r$ \\\\ observed rates are illustrative estimates", font_size=20,
                  color=HIST),
            label("uniform independent 32-bit pair: \\ $P=2^{-64}$ \\\\ divisor fixed at $-1$: \\ $P=2^{-32}$", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(eq, DOWN, buff=0.35).align_to(eq, LEFT)
        probe = VGroup(
            label(r"directed boundary test", font_size=21, color=HEAD),
            MathTex(r"(-2^{31})\div(-1)", font_size=28, color=HEAD),
            label(r"correct wrapped quotient: $-2^{31}$ \\ planted mutant: $0$", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(side, DOWN, buff=0.35).align_to(side, LEFT)
        # Keep the right-hand notes inside the frame in both languages.
        VGroup(eq, side, probe).shift(LEFT * 0.45)
        with self.voiceover(
            "Turn those rates into a budget. <bookmark mark='a'/> Under independent tests with a fixed true per-test "
            "hit rate r, the chance of at least one detection in N tests is one minus, one minus r, to the N. Plugging"
            " in our observed rates is only an illustration, not a guarantee. <bookmark mark='b'/> The common bugs are"
            " caught within a handful of programs, and the rare byte-load bug within a few hundred. <bookmark "
            "mark='c'/> The faint curve assumes a hypothetical rate of two to the minus thirty-two. For the overflow "
            "pair, two independent uniform thirty-two-bit operands instead give two to the minus sixty-four; fixing "
            "the divisor to minus one gives two to the minus thirty-two. Neither describes our evolving generator. "
            "Testing can reveal bugs without proving their absence. <bookmark mark='d'/> A directed test puts the "
            "boundary pair in registers deliberately: the correct wrapped quotient is the most-negative integer; the "
            "planted mutant returns zero. One suitable test exposes it. In 1994 Thomas Nicely publicly exposed the "
            "Pentium FDIV problem; Intel had already discovered it internally. Part 4 examined that different "
            "arithmetic bug."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Write(eq))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(tags), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(divc), FadeIn(divl), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]), FadeIn(probe))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fuzzing(self):
        head = label("CPU fuzzing: \\ feedback and better programs", font_size=36).to_edge(UP, buff=0.3)
        loop = VGroup(*[box(2.6, 0.8, rf"\text{{{t}}}", c, 22) for t, c in (("generate a program", DATA),
                                                                          ("run on RTL and model", CTRL),
                                                                          ("measure coverage", HEAD),
                                                                          ("keep what was new", YES))])
        for k, b in enumerate(loop):
            b.move_to([-3.6 + 2.4 * (k % 2) * 1.0 + (0 if k < 2 else 0), 1.4 - 1.3 * (k // 2), 0])
        loop[0].move_to([-4.2, 1.5, 0])
        loop[1].move_to([-0.8, 1.5, 0])
        loop[2].move_to([-0.8, 0.0, 0])
        loop[3].move_to([-4.2, 0.0, 0])
        arrows = VGroup(*[Arrow(loop[i].get_right() if i == 0 else loop[i].get_bottom() if i == 1 else
                                loop[i].get_left() if i == 2 else loop[i].get_top(),
                                loop[(i + 1) % 4].get_left() if i == 0 else loop[(i + 1) % 4].get_top() if i == 1 else
                                loop[(i + 1) % 4].get_right() if i == 2 else loop[(i + 1) % 4].get_bottom(),
                                buff=0.1, color=GREY_B, stroke_width=3) for i in range(4)])
        facts = VGroup(
            label(r"coverage: \ which states of the hardware's control logic \\ the tests have reached", font_size=20,
                  color=GREY_A),
            label(r"DifuzzRTL \ (Hur et al., \ 2021): \ register coverage, \\ new bugs in open RISC-V cores", font_size=20,
                  color=GREY_A),
            label(r"Cascade \ (Solt, Ceesay-Seitz and Razavi, \ 2024): \\ long programs with entangled control and data "
                  r"flow; \\ 37 new bugs in 5 of 6 RISC-V CPUs tested", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(UP * 0.4)
        foot = label("boundary inputs and coverage goals can help; \\ no time-to-discovery guarantee", font_size=20, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Industry and research do not give up on random testing; they steer it. <bookmark mark='a'/> A fuzzer "
            "generates a program, runs it on the hardware design and on a reference model, and measures coverage: "
            "which states of the hardware's control logic the program reached. Programs that reached something new are"
            " kept and mutated, so the search drifts towards the unexplored corners. <bookmark mark='b'/> DifuzzRTL, "
            "in 2021, measured coverage through the registers of the control logic and found new bugs in open RISC-V "
            "cores. <bookmark mark='c'/> Cascade, in 2024, generated long programs whose control flow and data flow "
            "are tangled together, and found thirty-seven new bugs in five of the six RISC-V processors it tested. "
            "<bookmark mark='d'/> Boundary-value generation or a suitable coverage objective can improve the chance of"
            " reaching an overflow case, but no time-to-discovery guarantee follows from coverage alone. Cascade's "
            "result also shows the value of generating long valid programs; it is not simply the same "
            "coverage-feedback loop as DifuzzRTL."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(b) for b in loop], lag_ratio=0.2), LaggedStart(*[GrowArrow(a) for a in arrows],
                                                                                      lag_ratio=0.2), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def formal(self):
        head = label(r"Or prove it", font_size=36).to_edge(UP, buff=0.35)
        rows = VGroup(
            label("\\textbf{executable specification.} \\ RISC-V Sail: \\ a formal model of supported ISA features; \\\\ useful for testing and proof, \\ not itself a processor-correctness proof",
                  font_size=21, color=CTRL),
            label("\\textbf{verified designs.} \\ Kami (2017): \\ pipelined RISC-V designs in Coq; \\\\ Silver + CakeML (2019): \\ connected hardware and compiler proofs, \\ with stated assumptions",
                  font_size=21, color=YES),
            label("\\textbf{scaling the argument.} \\ abstract OoO proofs and selected industrial checks exist; \\\\ full correctness and speculative-leakage security depend on models and threat boundaries", font_size=21,
                  color=NO),
            label("\\textbf{research exercise:} \\ specify operand classes, \\ then establish generator coverage; \\\\ scaling useful guarantees to realistic state spaces remains difficult", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "The alternative to testing is proof. <bookmark mark='a'/> It starts with a specification precise enough "
            "to prove things about. The RISC-V Sail model uses a language for instruction-set semantics to describe "
            "supported features precisely. It is a reference for testing and mechanized reasoning; the model alone "
            "does not prove a processor correct. <bookmark mark='b'/> In 2017 the Kami project proved, in the Coq "
            "proof assistant, that pipelined RISC-V processors implement the instruction set, and CakeML's Silver "
            "processor runs code from a verified compiler on verified hardware. <bookmark mark='c'/> Proofs also exist"
            " for abstract out-of-order machines and selected industrial properties. Scaling complete correctness and "
            "security arguments to complex speculative implementations remains difficult, with explicit models, "
            "assumptions and threat boundaries; Part 55 examines speculative leakage. <bookmark mark='d'/> For this "
            "part's research exercise, define exactly which operand classes a generator covers, then check that claim."
            " Extending useful guarantees to realistic state spaces is a research challenge; finite coverage "
            "guarantees and proof-guided test generation already exist."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            for i, (mk, r) in enumerate(zip("abcd", rows)):
                vo.wait_until(mk)
                self.play(Indicate(r, scale_factor=1.02) if i == 0 else FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
