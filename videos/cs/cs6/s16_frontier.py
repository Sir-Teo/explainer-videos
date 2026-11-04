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
        sub = label(rf"one bug at a time in a copy of the emulator; \ ${fmt(d['programs'])}$ random programs \ (this "
                    r"part's co-simulation tests, \ with multiply and divide)", font_size=20,
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
                            bar, label(rf"{100 * v:.2f}\%" if v else r"never", font_size=19,
                                       color=col).next_to(bar, RIGHT, buff=0.12)))
        cap = note(r"share of programs whose final registers, \ memory or output differ", font_size=18).to_edge(
            DOWN, buff=0.35)
        top = d["rows"][[r["rate"] for r in d["rows"]].index(max(r["rate"] for r in d["rows"]))]
        with self.voiceover(
            "This part trusted random programs: the gate-level machine had to agree with the emulator on hundreds of "
            "them. How much does that prove? Verification engineers answer with mutation analysis. "
            "<bookmark mark='a'/> Plant one known bug in a copy of the emulator, run the same two thousand random "
            "programs on it, and count how many end differently. <bookmark mark='b'/> Some bugs are caught almost at "
            "once: a store that also writes the next byte shows up in two programs out of three, and shifts that read "
            "only four bits of their amount in more than half. <bookmark mark='c'/> Others are rare. A byte load that "
            "forgets its sign shows up in one program in four hundred, because memory mostly holds zeros, and a branch "
            "that misbehaves only when both registers are zero in one in forty. <bookmark mark='d'/> And one bug is "
            "never caught at all: dividing minus two to the thirty-one by minus one, the single input where a "
            "thirty-two-bit quotient overflows. Random registers hit that pair with probability one in four billion."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(cap))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:5]], lag_ratio=0.25), run_time=2.0)
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
            tags.add(label(r["bug"], font_size=16, color=c).next_to(ax.c2p(x50, 0.5), RIGHT, buff=0.15).shift(
                DOWN * 0.32 * j))
        div_r = 2.0 ** -32
        ys = 1 - (1 - div_r) ** (10 ** xs)
        divc = VMobject(color=LIMIT, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])
        divl = label(r"$-2^{31} \div -1$: \ $2^{-32}$ per divide \\ needs billions", font_size=16, color=LIMIT).next_to(
            ax.c2p(6, 0.02), UP + LEFT, buff=0.1)
        eq = MathTex(r"P(\text{caught in } N) = 1 - (1 - r)^{N}", font_size=34, color=GREY_A).to_edge(RIGHT, buff=0.5
                                                                                                    ).shift(UP * 1.4)
        side = VGroup(
            label(r"testing can show the presence of bugs, \\ never their absence \ (Dijkstra, \ 1969)", font_size=20,
                  color=HIST),
            label(r"the bugs that matter most \\ live where random inputs never go", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(eq, DOWN, buff=0.5).align_to(eq, LEFT)
        with self.voiceover(
            "Turn those rates into a budget. <bookmark mark='a'/> If a bug spoils a fraction r of programs, the chance "
            "that N programs have caught it is one minus, one minus r, to the N. <bookmark mark='b'/> The common bugs "
            "are caught within a handful of programs, and the rare byte-load bug within a few hundred. "
            "<bookmark mark='c'/> The overflowing divide needs billions. Edsger Dijkstra put it in 1969: testing can "
            "show the presence of bugs, never their absence. <bookmark mark='d'/> The bugs that matter most live "
            "exactly where random inputs never go: in 1994 Intel's Pentium divided wrongly for a few rare inputs, "
            "found not by Intel's tests but by a mathematician, as Part 4 told."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(tags), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(divc), FadeIn(divl), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fuzzing(self):
        head = label(r"Smarter random: \ coverage-guided CPU fuzzing", font_size=36).to_edge(UP, buff=0.3)
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
        foot = label(r"still random, \ but steered: \ a fuzzer that rewards reaching the divider's overflow path \\ "
                     r"would find our last bug in minutes", font_size=20, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Industry and research do not give up on random testing; they steer it. <bookmark mark='a'/> A fuzzer "
            "generates a program, runs it on the hardware design and on a reference model, and measures coverage: "
            "which states of the hardware's control logic the program reached. Programs that reached something new "
            "are kept and mutated, so the search drifts towards the unexplored corners. <bookmark mark='b'/> "
            "DifuzzRTL, in 2021, measured coverage through the registers of the control logic and found new bugs in "
            "open RISC-V cores. <bookmark mark='c'/> Cascade, in 2024, generated long programs whose control flow and "
            "data flow are tangled together, and found thirty-seven new bugs in five of the six RISC-V processors it "
            "tested. <bookmark mark='d'/> A fuzzer rewarded for reaching the divider's overflow path would find our "
            "last bug in minutes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in loop], lag_ratio=0.2), LaggedStart(*[GrowArrow(a) for a in arrows],
                                                                                      lag_ratio=0.2), run_time=2.5)
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
            label(r"\textbf{the specification as a program.} \ RISC-V's official golden model is written in Sail, \\ a "
                  r"language for instruction-set semantics: \ an emulator like ours, \ but one that proof tools can read",
                  font_size=21, color=CTRL),
            label(r"\textbf{verified processors.} \ Kami \ (2017): \ pipelined RISC-V cores proved in Coq to implement "
                  r"the ISA; \\ CakeML's Silver \ (2019): \ a verified processor running verified compiled code",
                  font_size=21, color=YES),
            label(r"\textbf{the hard frontier.} \ out-of-order, \ speculative cores \ (Part 8): \ proving they keep the ISA's "
                  r"promises, \\ and that their speculation leaks nothing \ (Spectre, \ Part 55)", font_size=21,
                  color=NO),
            label(r"\textbf{open:} \ verification that scales to the processors people actually buy, \\ and test generation "
                  r"with a guarantee of what it has covered", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "The alternative to testing is proof. <bookmark mark='a'/> It starts with a specification precise enough "
            "to prove things about. RISC-V's official golden model is written in Sail, a language for instruction-set "
            "semantics: an emulator, like ours, but one that proof tools can read. <bookmark mark='b'/> In 2017 the "
            "Kami project proved, in the Coq proof assistant, that pipelined RISC-V processors implement the "
            "instruction set, and CakeML's Silver processor runs code from a verified compiler on verified hardware. "
            "<bookmark mark='c'/> The hard frontier is the out-of-order, speculative processors of Part 8: proving that "
            "they keep the instruction set's promises, and that their guessing leaks nothing, which Part 55 shows it "
            "does. <bookmark mark='d'/> Verification that scales to the processors people actually buy, and test "
            "generation that can say what it has covered, are open problems, and the research problem of this part."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
