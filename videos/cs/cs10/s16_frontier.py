from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CODE, CORE_COLORS, CTRL, DATA, FUNC, HEAD, NO, PART, YES, load, mono,
                                   timeline)


class Frontier(WatchScene):
    def construct(self):
        self.card()
        self.thin_air()
        self.open()

    def card(self):
        self.chapter(15, r"Frontier: \ thin air, \ stealing, \ dark silicon", r"What is still unknown about parallel machines?", lit=(2011, 2017), extra=((2011, r"C/C++11 formalised"), (2017, r"promising semantics")), part=PART, said="Chapter fifteen. The frontier.")

    # ------------------------------------------------------------------
    def thin_air(self):
        self.ask(r"Relaxed C++ atomics. \\ Can a value appear ``out of thin air''?", [r"no: the standard forbids it",
                 r"nobody can yet state a rule that cleanly forbids it"], 1,
                 say="With relaxed atomics, could a program read a value that nothing ever wrote?",
                 reveal="Every real processor would refuse, but nobody has yet written a rule that forbids it without "
                        "forbidding useful optimizations too.")
        fr = load("frontier")["lb"]
        head = label(r"Values out of thin air", font_size=36).to_edge(UP, buff=0.3)
        t0 = timeline(["r1 = x", "y = r1"], CORE_COLORS[0], -3.2, 1.6, dx=1.8)
        t1 = timeline(["r2 = y", "x = r2"], CORE_COLORS[1], -3.2, 0.8, dx=1.8)
        n0 = label(r"thread 0", font_size=20, color=CORE_COLORS[0]).next_to(t0, LEFT, buff=0.3)
        n1 = label(r"thread 1", font_size=20, color=CORE_COLORS[1]).next_to(t1, LEFT, buff=0.3)
        init = label(r"$x = y = 0$; \ each thread copies one into the other", font_size=20, color=GREY_B).next_to(
            VGroup(t0, t1), RIGHT, buff=0.5)
        cycle = VGroup(
            Arrow(t0[0].get_right(), t0[1].get_left(), buff=0.02, color=DATA, stroke_width=2),
            CurvedArrow(t0[1].get_bottom(), t1[0].get_top(), angle=-0.3, color=NO, stroke_width=2),
            Arrow(t1[0].get_right(), t1[1].get_left(), buff=0.02, color=CTRL, stroke_width=2),
            CurvedArrow(t1[1].get_right(), t0[0].get_top(), angle=PI * 0.75, color=NO, stroke_width=2),
        )
        cycle_note = label(r"toy circular justification; \ guessed value 42", font_size=17, color=NO).move_to(
            LEFT * 2.3 + UP * 2.9)
        sc = ", ".join(f"({a}, {b})" for a, b in fr["sc"])
        spec = ", ".join(f"({a}, {b})" for a, b in fr["speculative"])
        res = VGroup(
            label(rf"every interleaving, \ in order: \ $(r_1, r_2) \in \{{{sc}\}}$", font_size=22, color=YES),
            label(r"toy rule: \ expose a guessed store before confirming its source load",
                  font_size=22, color=GREY_A),
            wrapped_label(rf"guess 42, \ store it early, \ the other thread loads 42, \ copies it back: \ the guess "
                          rf"``confirms'' itself: \ $\{{{spec}\}}$", 12.0, font_size=22, color=NO),
            wrapped_label(r"C++ discourages circular values; \ this toy enumerator is not a language model or "
                          r"ordinary hardware speculation", 12.0, font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(VGroup(n1, t1), DOWN, buff=0.6).to_edge(LEFT, buff=0.6)
        with self.voiceover(
            (
            "A subtle research problem concerns causal cycles in language memory models. <bookmark mark='a'/> "
            "Here x and y are initially zero, and all shared accesses mean relaxed atomic accesses. One thread "
            "loads x and stores that value to y; the other loads y and copies it to x. <bookmark mark='b'/> Every "
            "ordinary program-order interleaving keeps both values zero. <bookmark mark='c'/> Now consider a "
            "deliberately permissive toy model that exposes a guessed store before confirming its source load. "
            "This is stronger than ordinary internal value prediction. <bookmark mark='d'/> A guess of forty-two "
            "can circulate through both threads and confirm itself. Our enumerator checks the candidate values "
            "zero, one and forty-two; it illustrates the circular justification, not a complete language "
            "semantics. <bookmark mark='e'/> Such out-of-thin-air cycles are discouraged by the C++ standard. "
            "Conventional processors do not publish unconfirmed speculative store values this way. The difficult "
            "question is how to specify causality precisely while preserving valid compiler transformations."
        )
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(t0), FadeIn(t1), FadeIn(n0), FadeIn(n1), FadeIn(init), run_time=0.6)
            vo.wait_until('a')
            for mk, r in zip("bcde", res):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
                if mk == "d":
                    self.play(Create(cycle), FadeIn(cycle_note), run_time=0.8)
        self.wait(0.3)
        self.clear_scene()



    # ------------------------------------------------------------------
    def open(self):
        head = label(r"And the power wall itself", font_size=36).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"near-threshold computing: \ energy, \ speed and noise-margin trade-offs", font_size=21, color=GREY_A),
            label(r"specialization: \ circuits for one job, \ dark until needed \ (Part 60)", font_size=21,
                  color=DATA),
            label(r"3-D stacking: \ memory on top of logic, \ shorter wires, \ and harder cooling", font_size=21,
                  color=GREY_A),
            wrapped_label(r"Landauer: \ $kT \ln 2$ minimum average heat for ideal erasure of an unknown unbiased bit; "
                          r"not every transistor transition", 12.0, font_size=21, color=FUNC),
            label(r"reversible and adiabatic designs reduce dissipation; \ resets and errors still count", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.1)
        with self.voiceover(
            (
            "Energy is another frontier with several different scales. <bookmark mark='a'/> Near-threshold "
            "operation can reduce energy per operation for some circuits and workloads, trading away speed and "
            "noise margin; the saving is not a universal factor of ten. <bookmark mark='b'/> Specialization can "
            "avoid the overhead of a general-purpose processor, as Part 60 explores. <bookmark mark='c'/> "
            "Three-dimensional integration can shorten connections, especially between memory and logic, while "
            "raising thermal and manufacturing challenges. <bookmark mark='d'/> At the thermodynamic scale, "
            "resetting one unknown unbiased bit in a reservoir at temperature T has a minimum average heat cost "
            "of k T times natural log two in the ideal erasure setting, about three times ten to the minus "
            "twenty-one joules at room temperature. That is not a lower bound on every transistor transition. "
            "<bookmark mark='e'/> Reversible and adiabatic designs aim to reduce information loss and "
            "dissipation. They do not violate Landauer's erasure bound; initialization, error correction and "
            "eventual reset still require accounting. Practical energy efficiency remains a system problem."
        )
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, p in zip('abcde', pts):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1), run_time=0.6 if mk == 'a' else 1.0)
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()
