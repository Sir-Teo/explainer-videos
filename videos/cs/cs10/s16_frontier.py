from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CODE, CORE_COLORS, CTRL, DATA, FUNC, HEAD, NO, PART, YES, load, mono,
                                   timeline)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.thin_air()
        self.models()
        self.stealing()
        self.open()

    def card(self):
        card = chapter_card(15, r"Frontier: \ thin air, \ stealing, \ dark silicon",
                            r"What is still unknown about parallel machines?", lit=(2011, 2017),
                            extra=((2011, r"C/C++11 formalised"), (2017, r"promising semantics")), part=PART)
        with self.voiceover("Chapter fifteen. The frontier."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def thin_air(self):
        fr = load("frontier")["lb"]
        head = label(r"Values out of thin air", font_size=36).to_edge(UP, buff=0.3)
        t0 = timeline(["r1 = x", "y = r1"], CORE_COLORS[0], -3.2, 1.6, dx=1.8)
        t1 = timeline(["r2 = y", "x = r2"], CORE_COLORS[1], -3.2, 0.8, dx=1.8)
        n0 = label(r"thread 0", font_size=20, color=CORE_COLORS[0]).next_to(t0, LEFT, buff=0.3)
        n1 = label(r"thread 1", font_size=20, color=CORE_COLORS[1]).next_to(t1, LEFT, buff=0.3)
        init = label(r"$x = y = 0$; \ each thread copies one into the other", font_size=20, color=GREY_B).next_to(
            VGroup(t0, t1), RIGHT, buff=0.5)
        sc = ", ".join(f"({a}, {b})" for a, b in fr["sc"])
        spec = ", ".join(f"({a}, {b})" for a, b in fr["speculative"])
        res = VGroup(
            label(rf"every interleaving, \ in order: \ $(r_1, r_2) \in \{{{sc}\}}$", font_size=22, color=YES),
            label(r"a machine that may guess a load's value and check it later \ (Part 8's value prediction):",
                  font_size=22, color=GREY_A),
            wrapped_label(rf"guess 42, \ store it early, \ the other thread loads 42, \ copies it back: \ the guess "
                          rf"``confirms'' itself: \ $\{{{spec}\}}$", 12.0, font_size=22, color=NO),
            wrapped_label(r"no real processor does this, \ yet the C++ standard's formal rules for relaxed atomics "
                          r"do not forbid it", 12.0, font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(VGroup(n1, t1), DOWN, buff=0.6).to_edge(LEFT, buff=0.6)
        with self.voiceover(
            "The first open problem is in the memory models of programming languages. <bookmark mark='a'/> Two "
            "threads, x and y both zero. Thread zero copies x into y; thread one copies y into x. <bookmark "
            "mark='b'/> Enumerate every interleaving and every value stays zero, which is obvious: there is no other "
            "value anywhere. <bookmark mark='c'/> But now allow a machine to guess the value a load will return and "
            "check it later, the value prediction of Part 8's Frontier. <bookmark mark='d'/> Guess forty-two. Store it "
            "early. The other thread loads forty-two and stores it back, and when the first load finally reads x, it "
            "finds forty-two: the guess confirms itself. Our enumerator finds outcomes like that for every guess. "
            "<bookmark mark='e'/> No real processor does this. But the formal rules of C and C++ for relaxed atomic "
            "operations, written down precisely by Mark Batty and colleagues in 2011, do not rule it out. Such "
            "values are called out of thin air."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t0), FadeIn(t1), FadeIn(n0), FadeIn(n1), FadeIn(init))
            for mk, r in zip("bcde", res):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def models(self):
        head = label(r"Why it is hard to forbid", font_size=36).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"compilers \textit{should} be free to reorder independent loads and stores", font_size=22,
                  color=GREY_A),
            label(r"but whether a store ``depends'' on a load can change under optimization: \\ "
                  r"\texttt{y = r1 * 0;} \ depends on \texttt{r1} until the compiler simplifies it", font_size=22,
                  color=GREY_A),
            label(r"so ``forbid stores that depend on unconfirmed loads'' is not a rule about the program text",
                  font_size=22, color=NO),
            label(r"C++14 added a sentence: \ implementations \textit{should} not produce such values \ (no definition)",
                  font_size=22, color=CTRL),
            label(r"candidates: \ promising semantics \ (Kang et al., \ 2017), \ event structures, \ pomsets: \ none yet "
                  r"adopted", font_size=22, color=DATA),
            label(r"the open problem: \ a model that forbids thin air \ \textit{and} allows every optimization in use",
                  font_size=23, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.1)
        with self.voiceover(
            "Why not just forbid it? <bookmark mark='a'/> Because compilers must stay free to reorder loads and "
            "stores that do not depend on each other; that freedom is much of what optimization is. <bookmark "
            "mark='b'/> And whether a store depends on a load is not a fact about the program text. A store of r1 "
            "times zero depends on r1, until the compiler simplifies it to a store of zero. <bookmark mark='c'/> So "
            "a rule like never let a store depend on an unconfirmed load cannot be stated about the source program. "
            "<bookmark mark='d'/> The 2014 C++ standard settled for one sentence saying implementations should not "
            "produce such values, without defining them. <bookmark mark='e'/> Researchers have proposed precise "
            "models, the promising semantics of Jeehoon Kang and colleagues in 2017 among them, but none has been "
            "adopted. <bookmark mark='f'/> The open question: is there a memory model that forbids values from thin "
            "air and still allows every optimization compilers actually perform?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcdef", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stealing(self):
        st = load("stealing")
        head = label(r"Work stealing: \ what the bounds leave out", font_size=34).to_edge(UP, buff=0.3)
        rows = st["rows"][1:]
        ax = Axes(x_range=[0.5, 6.5, 1], y_range=[0, 2.5, 0.5], x_length=6.0, y_length=3.2, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.2)
        xt = VGroup(*[label(str(r["p"]), font_size=16, color=GREY_B).next_to(ax.c2p(np.log2(r["p"]), 0), DOWN,
                                                                           buff=0.1) for r in rows])
        yt = VGroup(*[label(f"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(0.5, v), LEFT, buff=0.1)
                      for v in (0, 1, 2)])
        c = [(r["makespan"] - st["t1"] / r["p"]) / st["tinf"] for r in rows]
        pts = [ax.c2p(np.log2(r["p"]), v) for r, v in zip(rows, c)]
        line = VMobject(color=YES, stroke_width=4).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.07, color=YES) for p in pts])
        yl = label(r"$(T_p - T_1/p) \,/\, T_\infty$, \ simulated", font_size=18, color=GREY_B).next_to(ax, UP,
                                                                                                   buff=0.1)
        xl = label(r"processors", font_size=17, color=GREY_B).next_to(ax, DOWN, buff=0.4)
        side = VGroup(
            label(r"the constant in $O(T_\infty)$: \ here about " + f"{max(c):.1f}", font_size=20, color=YES),
            label(r"cache misses: \ stolen work runs on a cold cache \\ (Acar, \ Blelloch and Blumofe, \ 2000)",
                  font_size=20, color=GREY_A),
            label(r"memory: \ how much extra space \\ parallel execution needs", font_size=20, color=GREY_A),
            label(r"cores that differ: \ big and little, \\ CPU and GPU, \ near and far memory", font_size=20,
                  color=GREY_A),
            label(r"open: \ schedulers provably good for \\ locality, \ space and heterogeneity at once", font_size=20,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(ax, RIGHT, buff=0.6)
        with self.voiceover(
            "The second frontier is scheduling. <bookmark mark='a'/> Blumofe and Leiserson's bound hides a "
            "constant inside its big O. In our simulation the extra time beyond perfect division was "
            f"at most about {max(c):.1f} spans. <bookmark mark='b'/> But the bound counts only steps. A stolen task "
            "runs on a cold cache, far from its data; Umut Acar, Guy Blelloch and Robert Blumofe bounded those extra "
            "misses in 2000, and they are often what real programs feel. <bookmark mark='c'/> Parallel execution can "
            "also need far more memory than serial execution. <bookmark mark='d'/> And today's chips mix big and "
            "little cores, CPUs and GPUs, near and far memory, where a unit of work does not cost the same "
            "everywhere. <bookmark mark='e'/> A scheduler that is provably good for time, locality and space at once, "
            "on such machines, is still a research goal."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(yl), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dots), FadeIn(side[0]))
            for mk, p in zip("bcde", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        head = label(r"And the power wall itself", font_size=36).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"near-threshold computing: \ run at a voltage just above $V_{\text{th}}$: \ about ten times less "
                  r"energy, \ much slower", font_size=21, color=GREY_A),
            label(r"specialization: \ circuits for one job, \ dark until needed \ (Part 60)", font_size=21,
                  color=DATA),
            label(r"3-D stacking: \ memory on top of logic, \ shorter wires, \ and harder cooling", font_size=21,
                  color=GREY_A),
            label(r"the floor: \ Landauer's $kT \ln 2$ per erased bit, \ about $3 \times 10^{-21}$ J at room "
                  r"temperature: \ $10^4$ to $10^6$ times below today's switches", font_size=21, color=FUNC),
            label(r"reversible and adiabatic logic aim under it: \ no product yet", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.1)
        with self.voiceover(
            "And the power wall is a research frontier of its own. <bookmark mark='a'/> One idea is to run circuits "
            "at a voltage barely above the threshold, which can save about ten times the energy per operation, at a "
            "large cost in speed. <bookmark mark='b'/> Another is the specialization of Part 60. <bookmark "
            "mark='c'/> Another is to stack chips in three dimensions, memory directly on logic, shortening wires but "
            "making heat harder to remove. <bookmark mark='d'/> Underneath all of them sits a physical floor. In "
            "1961 Rolf Landauer showed that erasing one bit must release at least k T log two of heat, about three "
            "times ten to the minus twenty-one joules at room temperature. Today's switches spend between ten "
            "thousand and a million times more, depending on what you count. <bookmark mark='e'/> Reversible and adiabatic logic aim to compute below even that floor, by "
            "never erasing information. No product does it yet."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
