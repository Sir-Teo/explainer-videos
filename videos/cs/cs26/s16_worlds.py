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
            (r"Algorithmica", r"P = NP, \ or nearly: \\ every search is easy", YES),
            (r"Heuristica", r"NP is hard in the worst case, \\ easy on every input \\ anyone can generate", DATA),
            (r"Pessiland", r"hard on average, \\ but no one-way functions: \\ the worst of both", NO),
            (r"Minicrypt", r"one-way functions exist: \\ signatures, \ private-key \\ cryptography", LAM),
            (r"Cryptomania", r"public-key cryptography \\ exists \ (Part 30): \\ the world we think we live in",
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
        note = label(r"we do not know which world is ours: \ each is consistent with everything proved so far",
                     font_size=22, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1995 Russell Impagliazzo described five worlds, consistent with everything we know, that differ in "
            "what is hard. <bookmark mark='a'/> In Algorithmica, P equals NP, or nearly: every search problem is "
            "easy. <bookmark mark='b'/> In Heuristica, NP is hard in the worst case, but every instance anyone can "
            "actually generate is easy. <bookmark mark='c'/> In Pessiland, there are hard problems on average, but no "
            "one-way functions: the worst of both, with hard problems we cannot even use for secrecy. <bookmark "
            "mark='d'/> In Minicrypt, one-way functions exist, enough for signatures and private-key encryption. "
            "<bookmark mark='e'/> And in Cryptomania, public-key cryptography exists, which is the world we build the "
            "internet on, and which Part 30 assumes. <bookmark mark='f'/> We do not know which world we live in. "
            "Each is consistent with every theorem proved so far."
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
            label(r"\textbf{proofs}: \ any theorem with a proof of reasonable length could be found mechanically: \ "
                  r"G\"odel's letter", font_size=21, color=YES),
            label(r"\textbf{optimization}: \ scheduling, \ routing, \ protein design, \ chip layout, \ solved exactly",
                  font_size=21, color=YES),
            label(r"\textbf{learning}: \ finding the smallest model consistent with the data would be easy \ (Part 57)",
                  font_size=21, color=YES),
            label(r"\textbf{cryptography}: \ public-key encryption, \ signatures, \ hash functions: \ all broken",
                  font_size=21, color=NO),
            label(r"unless the polynomial were enormous, \ or the proof non-constructive: \ ``P = NP'' could be "
                  r"useless in practice", font_size=21, color=GREY_A),
            label(r"in Gasarch's 2019 poll, \ 88\% of respondents \ (99\% of experts) \ believed P $\ne$ NP",
                  font_size=21, color=HEAD),
            label(r"a Clay Millennium Prize problem \ (2000): \ \$1,000,000", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "What would P equals NP really mean? <bookmark mark='a'/> Gödel saw it first: any theorem with a proof "
            "of reasonable length could be found by machine. <bookmark mark='b'/> Scheduling, routing, protein "
            "design and chip layout could be solved exactly. <bookmark mark='c'/> Learning would become easy: find "
            "the smallest model consistent with the data. <bookmark mark='d'/> And almost all of cryptography would "
            "collapse, since breaking it is a search problem with checkable answers. <bookmark mark='e'/> There is a "
            "catch. A polynomial with an exponent of a thousand, or a proof that gives no algorithm, would change "
            "little in practice. <bookmark mark='f'/> Most researchers expect the opposite answer: in William "
            "Gasarch's 2019 poll, eighty-eight percent of respondents, and ninety-nine percent of the experts, "
            "believed P is not NP. <bookmark mark='g'/> It is one of the Clay Mathematics Institute's seven "
            "Millennium Prize problems, with a million dollars for the solution."
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
            label(r"Part 25: \ some true statements about programs have no proof in ZFC", font_size=22, color=WHITE),
            label(r"P $\ne$ NP is a $\Pi_2$ statement: \ for every machine and exponent, \ some input defeats it",
                  font_size=22, color=DATA),
            label(r"Hartmanis and Hopcroft \ (1976): \ there are oracles for which P vs NP \textbf{is} independent of "
                  r"set theory", font_size=22, color=HEAD),
            label(r"for the real question, \ no evidence of independence; \ most experts expect a proof, \ "
                  r"eventually", font_size=22, color=YES),
            label(r"Aaronson \ (2016) \ stresses an irony: \ the best lower bounds so far \ came from new "
                  r"\textbf{algorithms}", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Could P versus NP be one of Part 25's unprovable statements? <bookmark mark='a'/> Some true statements "
            "about programs have no proof in set theory, as we saw. <bookmark mark='b'/> P not equal to NP says that "
            "for every machine and every exponent, some input defeats it: a statement with two quantifiers, of "
            "exactly the kind that can escape proof. <bookmark mark='c'/> Juris Hartmanis and John Hopcroft showed "
            "in 1976 that, relative to certain oracles, the question really is independent of set theory. <bookmark "
            "mark='d'/> For the unrelativized question there is no such evidence, and most researchers expect it "
            "to be settled by an ordinary proof one day. <bookmark mark='e'/> Scott Aaronson's 2016 survey stresses "
            "an irony: the strongest lower bounds we have, like Williams's, came from discovering new algorithms. "
            "Proving that something is hard may require first learning what is easy."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
