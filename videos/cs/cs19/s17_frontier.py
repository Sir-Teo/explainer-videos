from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, concept_card, grid_table, load,
                                   mono, words)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.omega()
        self.seth()
        self.lower()
        self.open_()

    def card(self):
        card = chapter_card(16, r"Frontier: \ how fast can we multiply?", r"Are these algorithms the last word?",
                            lit=(2024,), extra=((2015, r"edit distance and SETH"), (2019, r"$n \log n$ multiplication"),
                                                (2026, r"selected dated arithmetic bounds")), part=PART)
        with self.voiceover("Chapter sixteen. Frontier: how fast can we multiply?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def omega(self):
        head=label(r"Upper bounds and method barriers",font_size=35).to_edge(UP,buff=.3)
        pts=[
            concept_card("starting construction",r"powers of Coppersmith--Winograd tensors",[-3.2,1.7,0],color=DATA),
            concept_card("2015: specified generalized laser method",r"barrier $2.3078$ inside that framework",[-3.2,-.15,0],color=NO),
            concept_card("universal-method barriers",r"still tied to specified starting tensors",[3.2,-.15,0],color=NO),
            concept_card("selected arithmetic upper bounds",r"2024: $<2.371339$; Aug 2026: $<2.371177$",[3.2,1.7,0],color=YES),
            concept_card("a barrier for a method is not a lower bound for the problem",r"field, exponent, constants and crossover are separate questions",[0,-2.35,0],width=12.2,height=1.25,color=HEAD),
        ]
        with self.voiceover(
            "Research barriers must name the method they restrict. <bookmark mark='a'/> Many exponent improvements "
            'analyze powers of Coppersmith-Winograd tensors through laser-method refinements. That is a family of '
            "constructions, not the definition of all matrix multiplication. <bookmark mark='b'/> Ambainis, Filmus "
            "and Le Gall's 2015 two-point-three-zero-seven-eight barrier concerns their specified generalized laser "
            "framework. <bookmark mark='c'/> Later universal-method results give other barriers for specified "
            'starting tensors. None is an unconditional lower bound of that size for matrix multiplication itself. '
            "<bookmark mark='d'/> New constructions, parameter choices and numerical optimization can improve upper "
            'bounds within the limits that actually apply. Our dated examples distinguish a proven method restriction'
            " from an unproved universal impossibility. <bookmark mark='e'/> Arithmetic exponent, input field, "
            'constants and practical crossover remain separate questions.'
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def seth(self):
        head=label("Conditional hardness: follow the implication",font_size=34).to_edge(UP,buff=.3)
        hypothesis=VGroup(label("SETH: the hard clause width may depend on epsilon",font_size=22,color=DATA),
            MathTex(r"\forall\varepsilon>0\ \exists k:\quad k\text{-SAT}\notin O^*(2^{(1-\varepsilon)N})",font_size=29,color=DATA)
        ).arrange(DOWN,buff=.2).move_to([0,1.95,0])
        pts=[hypothesis,
            concept_card("Backurs--Indyk reduction (2015)",r"exact edit distance in $O(n^{2-\delta})$, fixed $\delta>0$ $\Rightarrow$ SETH fails",[0,.15,0],width=11.9,height=1.3,color=NO),
            concept_card("related results",r"LCS and DTW: their own formulations",[-3.2,-1.55,0],height=1.15,color=LAM),
            concept_card("worst-case conditional evidence",r"does not time each practical pair",[3.2,-1.55,0],height=1.15,color=HEAD),
            label("approximation changes the task and its guarantees",font_size=23,color=YES).to_edge(DOWN,buff=.4),
        ]
        implication=Arrow([0,1.25,0],[0,.86,0],buff=.05,color=GREY_B)
        pts[1].add(implication)
        with self.voiceover(
            "Now distinguish a conditional lower bound from a timing curve. <bookmark mark='a'/> SETH says that for "
            'every positive epsilon there is a clause width k for which k-SAT has no algorithm with a two-to-the-one-'
            'minus-epsilon-N exponential factor, apart from polynomial input factors. The hard width may depend on '
            "epsilon. <bookmark mark='b'/> Backurs and Indyk's reduction shows that a general exact edit-distance "
            'algorithm with a fixed truly subquadratic exponent would contradict this hypothesis, already for a fixed'
            " finite alphabet. <bookmark mark='c'/> Related reductions address LCS and dynamic time warping under "
            "their respective formulations. <bookmark mark='d'/> This is worst-case conditional evidence, not a proof"
            " that each practical string pair needs a full quadratic table. <bookmark mark='e'/> Approximate distance"
            ' changes the task and has much faster guarantees in appropriate regimes. The diagram keeps hypothesis, '
            'reduction and conclusion separate.'
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def lower(self):
        head=label("State the computational model",font_size=35).to_edge(UP,buff=.3)
        pts=[
            concept_card("DFT upper bound",r"FFT: $O(n\log n)$ arithmetic operations",[-3.2,1.55,0],color=DATA),
            concept_card("bounded-coefficient linear circuits",r"Morgenstern (1973): $\Omega(n\log n)$",[3.2,1.55,0],color=YES),
            concept_card("integer multiplication",r"bit complexity differs from NumPy arithmetic counts",[-3.2,-.3,0],color=LAM),
            concept_card("unrestricted complex linear circuits",r"the bounded-coefficient proof does not settle this model",[3.2,-.3,0],color=HEAD),
        ]
        distinction=label("method theorem / conditional reduction / general lower bound: different claims",font_size=23,color=GREY_A).move_to([0,-2.4,0])
        pts[3].add(distinction)
        with self.voiceover(
            "Lower bounds also depend on the computational model. <bookmark mark='a'/> The standard FFT evaluates a "
            'linear transform in n log n arithmetic operations. That upper bound alone says nothing about all '
            "possible algorithms. <bookmark mark='b'/> Morgenstern's determinant argument gives an n log n lower "
            'bound in a bounded-coefficient linear-circuit model. Removing the coefficient restriction removes that '
            "proof's guarantee. <bookmark mark='c'/> Integer multiplication instead measures bit work; this course's "
            "NumPy convolution count is not such a lower bound. <bookmark mark='d'/> A method-specific theorem, a "
            'conjecture-based reduction and a general unconditional lower bound are different kinds of statements. '
            'Our research question asks about unrestricted linear arithmetic circuits for the DFT, with the field and'
            ' allowed operations stated.'
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head=label("Open questions: specify the objective",font_size=35).to_edge(UP,buff=.3)
        qs=VGroup(
            concept_card("matrix multiplication",r"$\omega$ over which field? At which practical size?",[-3.2,1.5,0],color=DATA),
            concept_card("exact edit distance",r"truly subquadratic worst case, or hardness without SETH?",[3.2,1.5,0],color=LAM),
            concept_card("DFT linear circuits over the complex numbers",r"must unrestricted coefficients still cost $\Omega(n\log n)$?",[-3.2,-.6,0],color=HEAD),
            concept_card("greedy rules",r"which objective, weights and independence structure?",[3.2,-.6,0],color=YES),
        )
        star=label(r"$\bigstar$ the circuit-model question is open; no supplied solution",font_size=23,color=HEAD).to_edge(DOWN,buff=.5)
        with self.voiceover(
            "Use precise questions. <bookmark mark='a'/> What is the square matrix multiplication exponent over a "
            'specified field, and how do useful implementations compare once constants and input sizes are included? '
            "<bookmark mark='b'/> Can exact edit distance achieve a fixed truly subquadratic worst-case exponent, or "
            "can a suitable lower bound be proved without SETH? <bookmark mark='c'/> Must unrestricted linear "
            'arithmetic circuits over the complex numbers use n log n operations for the DFT? The bounded-coefficient'
            " theorem does not settle this broader model. <bookmark mark='d'/> Which objectives and independence "
            'structures support a particular greedy rule? Matroids answer a precise weighted-independent-set '
            "characterization, not every use of greedy reasoning. <bookmark mark='e'/> The starred exercise develops "
            'the circuit-model question; it has no supplied solution.'
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abcd", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
