from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right)


class Worlds(VoiceoverScene):
    def construct(self):
        self.card()
        self.five()
        self.if_equal()
        self.unprovable()

    def card(self):
        card = chapter_card(15, r"Five possible worlds", r"What would each answer mean?", lit=(1995,),
                            extra=((1995, r"Impagliazzo"),), part=PART)
        with self.voiceover("Chapter fifteen. Five possible worlds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def five(self):
        head = label(r"Impagliazzo's five worlds \ (1995)", font_size=34).to_edge(UP, buff=0.3)
        worlds = [
            (r"Algorithmica", 'P = NP: \\\\ polynomially bounded \\\\ verifiable search is easy', YES),
            (r"Heuristica", 'worst-case hard; \\\\ average easy on relevant \\\\ samplable distributions', DATA),
            (r"Pessiland", r"hard on average, \\ but no one-way functions: \\ the worst of both", NO),
            (r"Minicrypt", 'one-way functions; \\\\ private-key primitives; \\\\ no public-key crypto', LAM),
            (r"Cryptomania", 'public-key capabilities \\\\ exist as well \\\\ (Part 30)',
             HEAD),
        ]
        cards = VGroup()
        for nm, d, col in worlds:
            box_ = RoundedRectangle(width=2.5, height=3.0, corner_radius=0.15, stroke_color=col, fill_color=BG,
                                    fill_opacity=1)
            t = label(nm, font_size=22, color=col).move_to(box_.get_top() + DOWN * 0.4)
            dd = label(d, font_size=17, color=WHITE).next_to(t, DOWN, buff=0.35)
            if dd.width > 2.3:
                dd.width = 2.3
            cards.add(VGroup(box_, t, dd))
        cards.arrange(RIGHT, buff=0.18).next_to(head, DOWN, buff=0.5)
        arrow = Arrow(cards[0].get_bottom() + DOWN * 0.3, cards[-1].get_bottom() + DOWN * 0.3, buff=0, color=GREY_B)
        al = VGroup(label(r"algorithms win", font_size=18, color=YES).next_to(arrow.get_start(), DOWN, buff=0.12),
                    label(r"cryptography wins", font_size=18, color=HEAD).next_to(arrow.get_end(), DOWN, buff=0.12))
        note = label('hypothetical worlds with distributional / security assumptions; P $\\ne$ NP alone does not choose one',
                     font_size=22, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Impagliazzo's five worlds organize hypothetical possibilities. <bookmark mark='a'/> Algorithmica means P equals NP. <bookmark mark='b'/> Heuristica keeps worst-case hardness while NP problems are easy on the relevant efficiently samplable distributions; it does not say every generated input is easy. <bookmark mark='c'/> Pessiland has average-case hard NP problems but no one-way functions. <bookmark mark='d'/> Minicrypt has one-way functions and the private-key primitives they imply, while public-key cryptography remains unavailable in the intended picture. <bookmark mark='e'/> Cryptomania adds public-key cryptographic capabilities. These are informal worlds with specific distributional and security assumptions, rather than five proven consistency theorems. <bookmark mark='f'/> P differs from NP alone does not choose among the average-case and cryptographic worlds. Parts 29 and 30 develop those distinctions."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcde", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            self.play(GrowArrow(arrow), FadeIn(al))
            vo.wait_until("f")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def if_equal(self):
        head = label(r"If P = NP", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label('proofs: polynomially bounded, efficiently checkable formal proof search; not unbounded truth', font_size=21, color=YES),
            label('optimization: bounded finite NP-verifiable objectives; physical design needs its own model',
                  font_size=21, color=YES),
            label('learning: bounded efficiently evaluable circuit searches; unrestricted program minimization stays undecidable',
                  font_size=21, color=YES),
            label('cryptography: one-way-function based computational security fails; information-theoretic secrecy is separate',
                  font_size=21, color=NO),
            label(r"unless the polynomial were enormous, \ or the proof non-constructive: \ ``P = NP'' could be "
                  r"useless in practice", font_size=21, color=GREY_A),
            label(r"in Gasarch's 2019 poll, \ 88\% of respondents \ (99\% of experts) \ believed P $\ne$ NP",
                  font_size=21, color=HEAD),
            label(r"a Clay Millennium Prize problem \ (2000): \ \$1,000,000", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "What would P equals NP imply? <bookmark mark='a'/> A bounded proof search with an efficiently checkable formal proof could recover a proof in polynomial time in the statement and the chosen length bound. It would not decide unbounded mathematical truth. <bookmark mark='b'/> Efficiently verifiable finite scheduling and routing objectives could be optimized through decision queries. Physical protein behaviour is not automatically such a model. <bookmark mark='c'/> Certain bounded circuit-learning searches would become efficient; finding the smallest unrestricted program remains undecidable. <bookmark mark='d'/> Computational cryptography based on one-way functions would fail. Information-theoretic secrecy, including a properly used one-time pad, is outside that conclusion. <bookmark mark='e'/> Large exponents, constants and the need to identify an algorithm could still make the theorem impractical. <bookmark mark='f'/> Historical opinion polls measure researchers' beliefs, not evidence of a mathematical separation. <bookmark mark='g'/> The Clay prize recognizes a valid resolution; neither applications nor consensus substitute for a proof."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def unprovable(self):
        head = label(r"Could it be unprovable?", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label('effective arithmetic theories may leave true statements unproved; this does not settle P vs NP', font_size=22, color=WHITE),
            label('P $\\ne$ NP: every clocked polynomial SAT decider has a finite counterexample; quantifier form is not independence',
                  font_size=22, color=DATA),
            label('relative independence uses particular oracles and specified theories; ordinary P vs NP/ZFC remains separate', font_size=22, color=HEAD),
            label('no unrelativized independence result is established here', font_size=22, color=YES),
            label(r"Aaronson \ (2016) \ stresses an irony: \ the best lower bounds so far \ came from new "
                  r"\textbf{algorithms}", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Could the unrelativized question be independent of our axioms? <bookmark mark='a'/> Part 25 explained that effective arithmetic theories can leave statements undecided. <bookmark mark='b'/> P differs from NP can be expressed by saying that every clocked polynomial-time SAT decider has a finite counterexample. Encoding machines and polynomial clocks gives a universal-existential arithmetic form; quantifier count alone is no evidence of independence. <bookmark mark='c'/> Relative independence examples concern particular constructed oracles and specified formal theories. They do not prove that ordinary P versus NP is independent of ZFC. <bookmark mark='d'/> No such independence conclusion is established here. <bookmark mark='e'/> The connections between algorithms and lower bounds instead provide concrete mathematical methods for continued work."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
