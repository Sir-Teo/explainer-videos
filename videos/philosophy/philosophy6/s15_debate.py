from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


class Debate(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Is choice true?", r"Should we accept an axiom that proves monsters?", lit=(1938,),
                            part=PART)
        with self.voiceover("Chapter fourteen. Is choice true?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.letters()
        self.independence()
        self.weaker()
        self.verdict()

    def letters(self):
        hc = history_card(1905, r"Baire, Borel, Hadamard, Lebesgue", r"`Five letters on set theory'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.35)
        sides = VGroup(
            VGroup(label(r"against: \ Borel, Baire, Lebesgue", font_size=28, color=BAD),
                   label(r"an object exists only if it can be defined", font_size=24),
                   label(r"`a choice without a rule is not a mathematical act'", font_size=22, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.2),
            VGroup(label(r"for: \ Hadamard", font_size=28, color=OK),
                   label(r"existence is not the same as definability", font_size=24),
                   label(r"mathematicians already choose, \ tacitly, \ all the time", font_size=22, color=GREY_A)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(
            [0, -0.6, 0])
        with self.voiceover(
            "Zermelo's proof set off a famous exchange. <bookmark mark='a'/>In 1905 five French mathematicians "
            "exchanged letters about it. Émile Borel, René Baire and Henri Lebesgue were against: a mathematical "
            "object exists only if it can be defined, and an infinity of arbitrary choices defines nothing. "
            "<bookmark mark='b'/>Jacques Hadamard disagreed: existence is not definability, and mathematicians, "
            "Lebesgue included, had been making such choices tacitly all along."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(sides[0]))
            vo.wait_until("b")
            self.play(FadeIn(sides[1]))
        self.clear_scene()

    def independence(self):
        hcs = VGroup(history_card(1938, r"Kurt Gödel", r"in the constructible universe $L$, \ choice holds: \ it is "
                                  r"consistent with ZF", width=6.0, color=HIST),
                     history_card(1963, r"Paul Cohen", r"models of ZF in which choice fails: \ it is independent",
                                  width=6.0, color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        res = VGroup(MathTex(r"\mathrm{ZF} \nvdash \mathrm{AC} \qquad \mathrm{ZF} \nvdash \lnot \mathrm{AC}", font_size=44,
                             color=GOAL),
                     label(r"(if ZF is consistent)", font_size=24, color=GREY_A),
                     label(r"so the axioms of Chapter 6 cannot settle the question: \ we must decide", font_size=26,
                           color=BAD)).arrange(DOWN, buff=0.3).move_to([0, -0.6, 0])
        with self.voiceover(
            "The question could not be settled by proof. <bookmark mark='a'/>In 1938 Kurt Gödel built a model of the "
            "other axioms, the constructible universe, in which choice holds; so choice cannot be disproved. "
            "<bookmark mark='b'/>In 1963 Paul Cohen built models in which it fails; so it cannot be proved either. "
            "<bookmark mark='c'/>Choice is independent of the other axioms. Whether to accept it is a decision, and "
            "the reasons must come from somewhere other than proof."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hcs[0]))
            vo.wait_until("b")
            self.play(FadeIn(hcs[1]))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.clear_scene()

    def weaker(self):
        head = label(r"Weaker choices, \ and life without choice", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = [(r"countable choice", r"choose from countably many sets", r"a countable union of countable sets is "
                                                                         r"countable"),
                (r"dependent choice \ (Bernays 1942)", r"make countably many choices, each depending on the last",
                 r"enough for almost all of analysis"),
                (r"no choice at all", r"Feferman and Lévy (1963)", r"$\mathbb{R}$ can be a countable union of countable "
                                                                     r"sets"),
                (r"Solovay (1970)", r"dependent choice, but not full choice", r"every set of reals has a length: \ no "
                                                                               r"Vitali set")]
        tab = VGroup()
        for i, (a, b, c) in enumerate(rows):
            y = 1.7 - 1.0 * i
            l1 = label(a, font_size=24, color=GOAL)
            l2 = label(b, font_size=22)
            l3 = label(c, font_size=22, color=GREY_A)
            l1.move_to([-6.3 + l1.width / 2, y + 0.15, 0])
            l2.move_to([-6.3 + l2.width / 2, y - 0.25, 0])
            l3.move_to([0.6 + l3.width / 2, y, 0])
            tab.add(VGroup(l1, l2, l3))
        with self.voiceover(
            "There are intermediate positions. <bookmark mark='a'/>Countable choice lets you choose from countably "
            "many sets; it already proves that a countable union of countable sets is countable. "
            "<bookmark mark='b'/>Dependent choice, due to Paul Bernays, lets you make a sequence of choices, each "
            "depending on the last, and it is enough for nearly all of analysis. <bookmark mark='c'/>Without any "
            "choice, strange things can happen: Solomon Feferman and Azriel Lévy found a model in which the real "
            "line is a countable union of countable sets. <bookmark mark='d'/>And Robert Solovay found a model with "
            "dependent choice in which every set of real numbers has a length. No Vitali sets, and no Banach and "
            "Tarski."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def verdict(self):
        q = quote_card(r"The axiom of choice is obviously true, the well-ordering principle obviously false, and who can "
                       r"tell about Zorn's lemma?", r"Jerry Bona", r"a joke: \ the three are equivalent", width=10.4,
                       font_size=28).move_to([0, 1.2, 0])
        today = VGroup(label(r"today: \ choice is a standard axiom, \ used freely", font_size=26, color=OK),
                       label(r"its monsters are non-measurable: \ no physical cutting could make them", font_size=24),
                       label(r"and its rejection costs bases, \ maximal ideals, \ and much else", font_size=24,
                             color=GREY_A)).arrange(DOWN, buff=0.25).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "A joke among mathematicians captures the mood. <bookmark mark='a'/>The axiom of choice is obviously "
            "true, the well-ordering principle obviously false, and who can tell about Zorn's lemma? The joke is "
            "that the three are equivalent. Our intuitions about the same principle differ with its packaging. "
            "<bookmark mark='b'/>Today choice is a standard axiom, used without apology. Its monsters are "
            "non-measurable sets, which no physical cutting could produce, and rejecting it would cost bases of "
            "vector spaces, maximal ideals, and much else."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in today], lag_ratio=0.4))
        self.clear_scene()
