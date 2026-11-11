from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, bar_chart, fit_right, grid_table,
                                   load)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.formulas()
        self.lower()
        self.meta()
        self.open_()

    def card(self):
        card = chapter_card(16, r"Frontier: \ complexity about complexity", r"How hard is it to tell how hard a "
                            r"function is?", lit=(1949, 2022), extra=((1949, r"Shannon"), (2020, r"Liu--Pass"),
                                                                        (2022, r"Hirahara")), part=PART)
        with self.voiceover("Chapter sixteen, the frontier. Complexity about complexity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def formulas(self):
        f = load("formulas")
        head = label(r"How big a formula does each function need?", font_size=32).to_edge(UP, buff=0.3)
        hist = {int(k): v for k, v in f["hist"].items() if k != "None"}
        ks = sorted(hist)
        ch = bar_chart([hist[k] for k in ks], [str(k) for k in ks], [YES if k <= 5 else (HEAD if k < 10 else NO)
                                                                    for k in ks], height=3.0, bar_w=0.42, gap=0.22,
                       fmt_=lambda v: f"{int(v)}", font_size=18)
        ch.next_to(head, DOWN, buff=0.6).to_edge(LEFT, buff=0.7)
        cl = label(r"leaves in the smallest AND/OR formula \ (literals as leaves)", font_size=18,
                   color=GREY_A).next_to(ch, DOWN, buff=0.15)
        notes = VGroup(
            label(rf"all {f['functions']} Boolean functions of 3 inputs, \\ exactly, \ by dynamic programming",
                  font_size=20, color=WHITE),
            label(rf"majority: {f['majority']} leaves; \\ parity and its complement: {f['parity']}, the maximum", font_size=20,
                  color=NO),
            label(r"Khrapchenko \ (1971): \ parity of $n$ bits \\ needs $n^2$; \ here 9 $\le$ 10", font_size=20,
                  color=HEAD),
            label('Shannon: almost all functions need circuit size $\\Omega(2^n/n)$; circuits allow fan-out', font_size=20, color=DATA),
            label('general B$_2$ circuits and literal-leaf formulas differ; dated lower-bound examples follow',
                  font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(ch, RIGHT, buff=0.7).align_to(ch, UP)
        fit_right(notes)
        with self.voiceover(
            "Measure complexity itself on a finite example. <bookmark mark='a'/> Enumerate all two hundred and fifty-six three-input Boolean functions using binary AND-OR formulas. Count literal leaves, allow negations only on inputs, and do not provide free constants. <bookmark mark='b'/> We retain a minimum-size formula for every truth table and check all trees and the complete dynamic-programming closure. Majority needs five leaves; parity and its complement need ten, the maximum in this experiment. <bookmark mark='c'/> Khrapchenko's general quadratic lower bound for parity matches that value at three inputs only as a lower bound of nine, not an exact answer. <bookmark mark='d'/> Counting shows that almost all functions require exponentially large circuits, but a circuit is not a fan-out-one formula and the precise size measure matters. <bookmark mark='e'/> Proving superlinear general circuit lower bounds for suitable explicitly computable families remains difficult. Our finite enumeration is a complete small calculation, not a solution to that asymptotic question."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(cl), FadeIn(notes[0]))
            for mk, n_ in zip("bcde", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def lower(self):
        head = label(r"The state of lower bounds", font_size=34).to_edge(UP, buff=0.35)
        rows = [[r"general circuits", r"$3.1\,n - o(n)$", r"Li and Yang \ (2022)"],
                [r"formulas \ (De Morgan)", r"$n^{3 - o(1)}$", r"H\aa stad \ (1998); \ Tal \ (2014)"],
                [r"constant depth", r"exponential, \ for parity", r"H\aa stad \ (1986)"],
                [r"ACC$^0$", 'NEXP $\\not\\subseteq$ ACC$^0$', 'Williams (2011), nonuniform fixed depth'],
                ['a sufficient stronger circuit route', r"superpolynomial, \ for SAT", r"open"]]
        tab = grid_table([r"model", 'dated result examples', r"by"], rows, widths=[4.0, 3.6, 5.2], row_h=0.52,
                         font_size=20, mono_cols=(), colors=[[WHITE, DATA, GREY_A]] * 4 + [[WHITE, NO, NO]])
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label(r"\textbf{geometric complexity theory} \ (Mulmuley and Sohoni, 2001): \ attack the algebraic "
                  r"version with representation theory", font_size=20, color=LAM),
            label('2016: particular occurrence-obstruction strategies ruled out; the broader GCT programme continues', font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.15).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Compare results only within their circuit models. <bookmark mark='a'/> Li and Yang's 2022 result supplies a dated example of a three point one n minus lower-order gate bound in the B-two basis, where every two-input Boolean gate is permitted. We are not presenting it as a verified current-record survey. Formula and constant-depth lower bounds use different restrictions and size conventions. <bookmark mark='b'/> A superpolynomial circuit lower bound for SAT would imply NP is not contained in P over poly, which is stronger than P differs from NP. Such a circuit bound is a sufficient route, not a necessary equivalence. <bookmark mark='c'/> Geometric complexity theory studies related algebraic lower bounds. The negative occurrence-obstruction results rule out a particular proposed strategy in specified settings, not the entire programme."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.5), run_time=6.0)
            for mk, n_ in zip("bc", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def meta(self):
        head = label(r"Meta-complexity", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"\textbf{MCSP}: \ given a truth table and $s$, \ is there a circuit of size $\le s$?", font_size=22,
                  color=WHITE),
            label(r"in NP \ (the circuit is the certificate); \ studied since the 1950s in the USSR \ (\textit{perebor})",
                  font_size=21, color=GREY_A),
            label('Hirahara (2022): partial MCSP is NP-hard under RANDOMIZED polynomial-time reductions', font_size=22,
                  color=HEAD),
            label('Liu--Pass (2020): OWFs $\\iff$ mild uniform-average hardness of exact $K^t$, suitable polynomial $t\\ge(1+\\epsilon)n$', font_size=22, color=YES),
            label('precise compression / time / error model matters; this equivalence does not establish public-key encryption', font_size=22, color=DATA),
            label('meta-complexity links average-case hardness and cryptography; qualifications remain essential',
                  font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Meta-complexity asks how hard it is to recognize complexity. <bookmark mark='a'/> Minimum circuit size takes a FULL truth table and a size threshold. A candidate circuit can be checked on every input in time polynomial in that table length, so the decision problem is in NP. <bookmark mark='b'/> Standard deterministic NP-completeness remains a separate question. <bookmark mark='c'/> Hirahara's 2022 partial-truth-table result proves NP-hardness under RANDOMIZED polynomial-time reductions. It does not establish the unqualified deterministic completeness claim. <bookmark mark='d'/> Liu and Pass relate one-way functions to mild average-case hardness of exact time-bounded Kolmogorov complexity on uniformly random strings, for appropriate polynomial time bounds at least one plus epsilon times the string length. <bookmark mark='e'/> The time bound, uniform distribution and error requirement are essential; this is not an equivalence with public-key encryption. <bookmark mark='f'/> These results connect the difficulty of recognizing short descriptions to computational cryptography, while leaving the stated qualifications intact."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open problems", font_size=34).to_edge(UP, buff=0.35)
        items = VGroup(
            label(r"1. \ P vs NP; \ NP vs coNP; \ P vs PSPACE; \ L vs P", font_size=22, color=WHITE),
            label(r"2. \ Is MCSP NP-complete?", font_size=22, color=WHITE),
            label(r"3. \ Is factoring, \ or graph isomorphism, \ in P?", font_size=22, color=WHITE),
            label('4. Certify the numerical 3-SAT threshold; distinguish reported 2026 theorems from finite fits', font_size=22,
                  color=WHITE),
            label(r"5. \ Can time $t$ be simulated in space $t^{1/2 - \varepsilon}$, \ or even $t^{\varepsilon}$?",
                  font_size=22, color=WHITE),
            label('6. For P/NP families: improve a linear coefficient, or prove a superlinear bound such as $n\\log n$',
                  font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5)
        star = label(r"$\bigstar$ \ the part's research problem takes a small case of the fourth", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Six directions remain. <bookmark mark='a'/> P versus NP, NP versus coNP, P versus PSPACE and L versus P. <bookmark mark='b'/> The deterministic many-one hardness of ordinary minimum circuit size. <bookmark mark='c'/> Classical polynomial-time algorithms for factoring search and graph isomorphism. <bookmark mark='d'/> Rigorous numerical characterization of the random three-SAT threshold, beyond the existence and computability reported in 2026 preprints, and distinguished from a finite fifty-percent crossing. <bookmark mark='e'/> Further time-space simulation improvements, with the model and quantifiers specified. <bookmark mark='f'/> General circuit lower bounds for suitable families in P or NP: improving a linear coefficient, such as five n, is different from proving a superlinear bound such as n log n. <bookmark mark='g'/> The starred exercise studies finite random-SAT samples with uncertainty. It does not ask you to claim an asymptotic theorem from a small fit."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcdef", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
