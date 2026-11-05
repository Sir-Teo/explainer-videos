from __future__ import annotations

from videos.philosophy.philosophy1.common import *  # noqa: F403


def pair_tex(p):
    return rf"(+{p[0]},\,-{p[1]})"


class Leibniz(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Leibniz's numbers", r"Can concepts be numbers, and inference arithmetic?",
                            lit=(1679,), part=PART)
        with self.voiceover("Chapter fourteen. Leibniz's numbers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.reckoner()
        self.primes()
        self.pairs()
        self.check()

    def primes(self):
        hc = history_card(1679, r"Leibniz", r"`Elements of a Calculus': characteristic numbers for concepts",
                          width=5.4, color=HIST).to_corner(UL, buff=0.4)
        eqs = VGroup(MathTex(r"\text{animal} = 2", font_size=40, color=P.CLAIM),
                     MathTex(r"\text{rational} = 3", font_size=40, color=P.AGENT),
                     MathTex(r"\text{man} = \text{rational animal} = 2 \times 3 = 6", font_size=40, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([0.6, 0.4, 0])
        rule = MathTex(r"\text{All } S \text{ are } P \iff P \mid S", font_size=44).move_to([0.6, -1.6, 0])
        ex = label(r"all men are animals: \ $2 \mid 6$ \ $\checkmark$", font_size=30, color=OK).next_to(rule, DOWN,
                                                                                                    buff=0.3)
        sch = note(r"illustrative numbers").to_corner(DR, buff=0.3)
        with self.voiceover(
            "In April 1679, Leibniz tried it. <bookmark mark='a'/>Give each simple concept a prime number: say "
            "animal is two, and rational is three. A complex concept is a product of simple ones, so man, the "
            "rational animal, is six. <bookmark mark='b'/>Now 'all men are animals' should mean that the concept of "
            "animal is contained in the concept of man; that is, two divides six. <bookmark mark='c'/>Checking a "
            "universal truth becomes checking a division. Calculemus."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(sch))
            vo.wait_until("a")
            self.play(LaggedStart(*[Write(e) for e in eqs], lag_ratio=0.5))
            vo.wait_until("b")
            self.play(Write(rule))
            vo.wait_until("c")
            self.play(FadeIn(ex))
        self.clear_scene()

    def pairs(self):
        d = load("leibniz")
        t = d["terms"]
        prob = label(r"but `no $S$ are $P$' and `some $S$ are $P$' need more than divisibility", font_size=28,
                     color=BAD).to_edge(UP, buff=0.4)
        terms = VGroup(*[MathTex(rf"\text{{{k}}} = {pair_tex(v)}", font_size=34) for k, v in t.items()]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).move_to([-3.8, 0.2, 0])
        rules = VGroup(
            MathTex(r"\text{All } S \text{ are } P:\ \ P^+ \mid S^+ \text{ and } P^- \mid S^-", font_size=30),
            MathTex(r"\text{No } S \text{ are } P:\ \ \gcd(S^+, P^-) > 1 \text{ or } \gcd(S^-, P^+) > 1", font_size=30),
            MathTex(r"\text{Some } S \text{ are } P:\ \ \text{not `no'}", font_size=30),
            MathTex(r"\text{Some } S \text{ are not } P:\ \ \text{not `all'}", font_size=30)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, 0.3, 0])
        sh = d["shown"]
        said = [r"all men are animals", r"all men are rational", r"some animals are rational", r"no man is a stone",
                r"all animals are men"]
        res = VGroup()
        for s_, txt in zip(sh, said):
            res.add(label(rf"{txt}: \ " + (r"$\checkmark$" if s_["holds"] else r"$\times$"), font_size=24,
                          color=OK if s_["holds"] else BAD))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Divisibility handles 'all'. But Leibniz also needed 'no' and 'some', and single numbers have no way to "
            "say that two concepts exclude each other. <bookmark mark='a'/>His repair was to give each concept two numbers, a positive and "
            "a negative, with no common factor: one for what it includes, one for what it excludes. "
            "<bookmark mark='b'/>Then 'all S are P' means both of P's numbers divide S's. 'No S are P' means one of "
            "S's numbers shares a factor with the opposite number of P: S includes something P excludes. 'Some' and "
            "'some not' are the negations. <bookmark mark='c'/>With these illustrative numbers, men are animals, men "
            "are rational, some animals are rational, no man is a stone, and it is not true that all animals are men."
        ) as vo:
            self.play(FadeIn(prob))
            vo.wait_until("a")
            self.play(FadeIn(terms))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rules], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in res], lag_ratio=0.25))
        self.clear_scene()

    def check(self):
        d = load("leibniz")
        m = load("moods")
        n = d["assignments"]
        hl = label(rf"every mood, against {n:,} assignments of numbers built from the primes 2, 3, 5", font_size=28,
                   color=GOAL).to_edge(UP, buff=0.4)
        surv = {(f, mo) for f, mo, _ in d["survivors"]}
        trad = {(f, mo) for f, mo, _ in m["traditional"]}
        assert surv == trad
        cells, idx = VGroup(), {}
        for f in (1, 2, 3, 4):
            for j, r in enumerate([r for r in m["rows"] if r["figure"] == f]):
                sq = Square(0.17, stroke_width=0.6, stroke_color=GREY_D, fill_color=GREY_D, fill_opacity=1)
                sq.move_to([-5.7 + j * 0.185, 1.5 - (f - 1) * 0.75, 0])
                cells.add(sq)
                idx[(f, r["mood"])] = sq
        res = label(rf"survivors: \ {len(surv)} \ = \ exactly the 24 traditional moods", font_size=32, color=OK)
        res.move_to([0, -1.8, 0])
        thm = label(r"Leibniz's arithmetic is a model of Aristotle's logic (Łukasiewicz 1951; complete: Sotirov "
                    r"1999)", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Did Leibniz's arithmetic get Aristotle's logic right? Leibniz could not check; we can. "
            f"<bookmark mark='a'/>Take every term number built from the primes two, three and five: {n:,} ways to "
            "assign numbers to three terms. Run every one of the two hundred and fifty-six moods against all of "
            "them, and keep the moods that no assignment refutes. <bookmark mark='b'/>"
            f"{len(surv)} survive, and they are exactly the twenty-four moods of the tradition, Darapti included. "
            "<bookmark mark='c'/>The numbers have existential import built in: every concept number names something. "
            "Jan Łukasiewicz proved in 1951 that Leibniz's scheme satisfies the axioms of Aristotle's syllogistic. "
            "Leibniz himself was dissatisfied and moved on. But in 1679, for the first time, a piece of reasoning had "
            "been turned into arithmetic that a machine could do."
        ) as vo:
            self.play(FadeIn(hl), FadeIn(cells))
            vo.wait_until("a")
            self.play(LaggedStart(*[c.animate.set_fill(GREY_E) for c in cells], lag_ratio=0.002), run_time=2)
            vo.wait_until("b")
            self.play(*[idx[k].animate.set_fill(OK) for k in surv], FadeIn(res))
            vo.wait_until("c")
            self.play(FadeIn(thm))
        self.clear_scene()

    def reckoner(self):
        hc = history_card(1673, r"Leibniz's stepped reckoner", r"shown to the Royal Society: the first machine "
                          r"to multiply; its stepped drum survived in calculators into the 20th century", width=6.0,
                          color=HIST).to_corner(UL, buff=0.4)
        drum = VGroup(*[Rectangle(width=0.22, height=0.25 + 0.22 * k, stroke_width=0, fill_color=CONN,
                                  fill_opacity=0.8) for k in range(9)]).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
        drum.move_to([3.6, 1.35, 0])
        dl = label(r"the stepped drum: \ nine teeth of nine lengths", font_size=22, color=GREY_A).next_to(drum, DOWN,
                                                                                                     buff=0.2)
        q = quote_card(r"It is unworthy of excellent men to lose hours like slaves in the labour of calculation which "
                       r"could safely be relegated to anyone else if machines were used.", r"Leibniz (1685)",
                       r"trans.\ Kidinger, in Smith, \textit{A Source Book in Mathematics}", width=10.0, font_size=26)
        q.to_edge(DOWN, buff=0.5)
        two = label(r"\textit{characteristica universalis}: \ a language for concepts; \ "
                    r"\textit{calculus ratiocinator}: \ rules to compute with it", font_size=24, color=GOAL)
        two.move_to([0, -0.75, 0])
        with self.voiceover(
            "Leibniz did not only dream of calculating machines; he built one. <bookmark mark='a'/>In 1673 he showed "
            "the Royal Society his stepped reckoner, the first machine that could multiply, using a drum with teeth "
            "of nine different lengths. The design survived in mechanical calculators for more than two centuries. "
            "<bookmark mark='b'/>He wanted two things for reasoning: a universal characteristic, a language in which "
            "every concept is written as a combination of simple ones; and a calculus of reasoning, rules for "
            "computing with it. <bookmark mark='c'/>It is unworthy of excellent men, he wrote, to lose hours like "
            "slaves in the labour of calculation, which could be left to anyone if machines were used."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(drum), FadeIn(dl))
            vo.wait_until("b")
            self.play(FadeIn(two))
            vo.wait_until("c")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.clear_scene()
