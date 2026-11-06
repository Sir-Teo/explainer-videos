from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from explainer.cs.algo import proofs as PR
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono)


def term_tex(t):
    return r" \wedge ".join((rf"x_{{{v}}}" if b else rf"\bar x_{{{v}}}") for v, b in t)


class Circuits(VoiceoverScene):
    def construct(self):
        self.card()
        self.karp_lipton()
        self.restriction()
        self.measured()
        self.others()

    def card(self):
        card = chapter_card(3, r"Circuit lower bounds", r"Which functions need big circuits?", lit=(1981, 2011),
                            extra=((1986, r"H\aa stad's switching lemma"), (2011, r"Williams")), part=PART)
        with self.voiceover("Chapter three. Circuit lower bounds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def karp_lipton(self):
        head = label(r"Why circuits?", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"P/poly: \ a polynomial-size circuit for each input length \ (no uniformity)", font_size=22,
                  color=WHITE),
            label(r"P $\subseteq$ P/poly, \ and BPP $\subseteq$ P/poly \ (chapter 1)", font_size=22, color=DATA),
            label(r"so to show P $\ne$ NP, \ it would suffice to show SAT $\notin$ P/poly: \ a pure counting of gates",
                  font_size=22, color=HEAD),
            label(r"Karp and Lipton \ (1980): \ if NP $\subseteq$ P/poly, \ the polynomial hierarchy collapses to "
                  r"its second level", font_size=22, color=NO),
            label(r"so most believe SAT needs superpolynomial circuits: \ but proving it is the barrier of Part 26",
                  font_size=22, color=GREY_A),
            label(r"what we \textbf{can} prove: \ restricted circuits. \ First, \ constant depth", font_size=22,
                  color=YES),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Circuits give a purely combinatorial way at P versus NP. <bookmark mark='a'/> P slash poly is the class "
            "of problems with a polynomial-size circuit for each input length. <bookmark mark='b'/> It contains P, "
            "and, by Adleman, BPP. <bookmark mark='c'/> So proving that SAT needs circuits of superpolynomial size "
            "would separate P from NP, with no machines involved, only gates. <bookmark mark='d'/> Richard Karp and "
            "Richard Lipton showed that if SAT did have small circuits, the polynomial hierarchy would collapse to "
            "its second level. <bookmark mark='e'/> So most believe SAT needs large circuits, but proving it runs "
            "into Part 26's barriers. <bookmark mark='f'/> What can be proved is lower bounds for restricted "
            "circuits. The first success was circuits of constant depth."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def restriction(self):
        s = load("switching")
        f = [tuple((v, b) for v, b in t) for t in s["dnf"]]
        n = s["n"]
        ex = None
        for seed in range(500):
            rho = PR.random_restriction(n, 0.2, random.Random(seed))
            g = PR.restrict(f, rho)
            if isinstance(g, list) and 2 <= len(g) <= 4:
                free = [v for v in range(n) if v not in rho]
                if len(free) <= 6 and PR.dt_depth(PR.truth_table(g, free), len(free)) == 2:
                    ex = (rho, g)
                    break
        head = label(r"Random restrictions", font_size=34).to_edge(UP, buff=0.3)
        terms = VGroup(*[MathTex(term_tex(t), font_size=22, color=DATA) for t in f[:10]]).arrange_in_grid(
            rows=5, cols=2, buff=(0.5, 0.12))
        tl = label(rf"a 3-DNF on {n} variables: \ {len(f)} terms \ (10 shown), \ OR-ed together", font_size=19,
                   color=GREY_A)
        top = VGroup(terms, tl).arrange(DOWN, buff=0.15).next_to(head, DOWN, buff=0.35)
        rho, g = ex
        fixed = MathTex(r"\rho:\ " + r",\ ".join(rf"x_{{{v}}}={int(b)}" for v, b in sorted(rho.items())),
                        font_size=22, color=HEAD)
        after = MathTex(r" \vee ".join(r"(" + term_tex(t) + r")" for t in g), font_size=28, color=YES)
        bottom = VGroup(
            label(r"fix each variable at random with probability $1 - p$ \ (here $p = 0.2$):", font_size=20,
                  color=WHITE),
            fixed, label(r"what is left:", font_size=20, color=WHITE), after,
            label(r"a term with a false literal vanishes; \ a term made true makes the whole DNF true", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.18).next_to(top, DOWN, buff=0.4)
        for m in bottom:
            if m.width > 13:
                m.width = 13
        with self.voiceover(
            "Johan Håstad's tool is the random restriction. <bookmark mark='a'/> Here is a formula in disjunctive "
            "normal form: twenty terms, each the AND of three literals, OR-ed together, over fourteen variables. "
            "<bookmark mark='b'/> Fix each variable to a random value, except that with probability p it stays "
            "free. <bookmark mark='c'/> Most terms die: one false literal kills a term. If any term becomes true, "
            "the whole formula is true. <bookmark mark='d'/> What survives is tiny. This restriction leaves a "
            "function that a decision tree of depth two computes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top))
            vo.wait_until("b")
            self.play(FadeIn(bottom[0]), FadeIn(bottom[1]))
            vo.wait_until("c")
            self.play(FadeIn(bottom[4]))
            vo.wait_until("d")
            self.play(FadeIn(bottom[2]), FadeIn(bottom[3]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        s = load("switching")
        head = label(r"The switching lemma, \ measured", font_size=34).to_edge(UP, buff=0.3)
        rows = []
        for r in s["rows"]:
            rows.append([f"{r['p']:g}", f"{r['ge']['1']:.3f}", f"{r['ge']['2']:.4f}", f"{r['ge']['3']:.4f}",
                         f"{r['bound']['2']:.3f}" if r["bound"]["2"] < 1 else r"$\ge 1$"])
        tab = grid_table([r"$p$ free", r"depth $\ge 1$", r"depth $\ge 2$", r"depth $\ge 3$", r"bound $(5pw)^2$"], rows,
                         widths=[1.6, 2.0, 2.0, 2.0, 2.6], row_h=0.42, font_size=20, mono_cols=(),
                         colors=[[WHITE, DATA, HEAD, NO, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        tl = label(r"1,500 random restrictions per row; \ exact decision-tree depth of what is left", font_size=19,
                   color=GREY_A).next_to(tab, DOWN, buff=0.12)
        lines = VGroup(
            label(r"\textbf{H\aa stad (1986)}: \ $\Pr[\text{depth} \ge s] \le (5pw)^s$ \ for a width-$w$ DNF",
                  font_size=22, color=WHITE),
            label(r"a DNF becomes a shallow tree, \ which is a CNF of small width: \ an OR-of-ANDs \textbf{switches} "
                  r"to an AND-of-ORs", font_size=21, color=DATA),
            label(r"so a depth-$d$ circuit collapses level by level under repeated restrictions", font_size=21,
                  color=GREY_A),
            label(r"but \textbf{parity} of the free variables stays parity: \ it never collapses", font_size=22,
                  color=NO),
            label(r"so constant-depth circuits for parity need $2^{n^{\Omega(1/d)}}$ gates", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.2).next_to(tl, DOWN, buff=0.35)
        with self.voiceover(
            "How often does a restriction leave something complicated? <bookmark mark='a'/> We applied fifteen "
            "hundred random restrictions at each value of p and computed the exact decision-tree depth of what was "
            "left. Håstad's switching lemma bounds the chance of depth s or more by five p w to the s, and the "
            "measured frequencies sit well inside the bound where it applies. <bookmark mark='b'/> A shallow decision "
            "tree can be written either way round, so an OR of ANDs switches into an AND of ORs. <bookmark "
            "mark='c'/> Apply restrictions repeatedly, and a circuit of constant depth collapses one level at a "
            "time. <bookmark mark='d'/> But parity never collapses: restrict it, and you get the parity of the free "
            "variables. <bookmark mark='e'/> So parity needs exponentially large circuits of constant depth, the "
            "result of Furst, Saxe and Sipser, Ajtai, and Yao, made sharp by Håstad."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(tl), FadeIn(lines[0]))
            for mk, ln in zip("bcde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def others(self):
        head = label(r"Further lower bounds", font_size=34).to_edge(UP, buff=0.35)
        rows = [[r"AC$^0$ \ (constant depth)", r"parity needs exponential size", r"H\aa stad \ (1986)"],
                [r"AC$^0$ with mod-3 gates", r"parity still exponential", r"Razborov \ (1987); \ Smolensky \ (1987)"],
                [r"monotone \ (no NOT gates)", r"clique needs $n^{\Omega(\sqrt k)}$", r"Razborov \ (1985)"],
                [r"ACC$^0$ \ (any mod gates)", r"NEXP $\not\subseteq$ ACC$^0$", r"Williams \ (2011)"]]
        tab = grid_table([r"circuits", r"lower bound", r"by"], rows, widths=[4.0, 4.6, 4.6], row_h=0.55,
                         font_size=20, mono_cols=(), colors=[[WHITE, DATA, GREY_A]] * 4)
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        lines = VGroup(
            label(r"Razborov--Smolensky: \ approximate the circuit by a \textbf{low-degree polynomial} over a field",
                  font_size=21, color=WHITE),
            label(r"Williams: \ a SAT algorithm for ACC$^0$ circuits only slightly faster than $2^n$ \ "
                  r"$\Rightarrow$ \ a lower bound against them", font_size=21, color=YES),
            label(r"algorithms imply lower bounds: \ the one method that has crossed Part 26's barriers", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Other restricted models fell too. <bookmark mark='a'/> Alexander Razborov and Roman Smolensky showed "
            "that even with gates counting modulo three, parity needs exponential size; their method approximates "
            "the whole circuit by a polynomial of low degree. Razborov also proved that monotone circuits, with no "
            "negations, need superpolynomial size for clique. And Ryan Williams separated nondeterministic "
            "exponential time from ACC zero. <bookmark mark='b'/> His proof is unusual: a satisfiability algorithm "
            "for those circuits, only slightly faster than trying all two to the n inputs, implies a lower bound "
            "against them. <bookmark mark='c'/> Algorithms imply lower bounds. It is the one method so far that has "
            "crossed the barriers of Part 26."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.6), FadeIn(lines[0]),
                      run_time=4.0)
            for mk, ln in zip("bc", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
