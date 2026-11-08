from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Platonism(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Abstract objects", r"If numbers exist, \ where are they?", lit=(-380, 1947, 1973),
                            part=PART)
        with self.voiceover("Chapter one. Abstract objects."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.platonists()
        self.godel()
        self.benacerraf()
        self.field()

    def platonists(self):
        head = label(r"Platonism: \ mathematics describes abstract objects", font_size=32, color=ABSTRACT).to_edge(
            UP, buff=0.5)
        rows = rows_at([
            (r"Plato", r"the forms: \ the square itself, \ which no drawing in the sand quite is"),
            (r"Frege (1884)", r"numbers are objects: \ objective, \ like the axis of the earth, \ but not in space"),
            (r"Gödel (1944, 1964)", r"sets are as real as physical bodies: \ we discover their properties"),
            (r"most mathematicians", r"`we discover theorems, \ we do not invent them'"),
        ], x_left=-6.2, x_right=-2.4, y0=1.5, dy=0.85, font_size=26, left_color=ABSTRACT)
        props = VGroup(label(r"abstract: \ not in space, \ not in time, \ no causes, \ no effects", font_size=26,
                             color=GOAL),
                       label(r"so `7 is prime' is about $7$, \ as `Paris is a city' is about Paris", font_size=24,
                             color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The first answer is the oldest. <bookmark mark='a'/>For Plato, geometry is about the forms: the "
            "square itself, which no square drawn in the sand quite is. <bookmark mark='b'/>For Frege, in 1884, "
            "numbers are objects. They are objective, as the axis of the earth is objective, though nobody can trip "
            "over either. <bookmark mark='c'/>For Gödel, there was quite as much reason to believe in sets as in "
            "physical bodies, and mathematicians discover their properties. <bookmark mark='d'/>And most working mathematicians talk this way: we discover "
            "theorems, we do not invent them. <bookmark mark='e'/>The objects are abstract: they are not in space "
            "or time, and they neither cause anything nor are caused. So 'seven is prime' is about the number seven, "
            "just as 'Paris is a city' is about Paris."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(props))
        self.clear_scene()

    def godel(self):
        q = quote_card(r"Despite their remoteness from sense experience, we do have something like a perception also "
                       r"of the objects of set theory, as is seen from the fact that the axioms force themselves upon us "
                       r"as being true.", r"Kurt Gödel", r"supplement to `What is Cantor's continuum problem?', \ 1964",
                       width=10.4, font_size=28).move_to([0, 1.2, 0])
        pts = VGroup(label(r"mathematical intuition: \ a faculty like perception, \ aimed at the abstract", font_size=26,
                           color=ABSTRACT),
                     label(r"Part 6: \ how Gödel hoped it would settle the continuum hypothesis", font_size=22,
                           color=GREY_B)).arrange(DOWN, buff=0.2).move_to([0, -1.7, 0])
        with self.voiceover(
            "Gödel even proposed how we know about these objects. <bookmark mark='a'/>Despite their remoteness from "
            "sense experience, he wrote in 1964, we do have something like a perception also of the objects of set "
            "theory, as is seen from the fact that the axioms force themselves upon us as being true. "
            "<bookmark mark='b'/>Mathematical intuition, on this view, is a faculty like sight, aimed at the "
            "abstract. Part 6 showed how Gödel hoped it would one day settle the continuum hypothesis."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(pts))
        self.clear_scene()

    def benacerraf(self):
        hc = history_card(1973, r"Paul Benacerraf", r"`Mathematical truth'", width=4.8, color=HIST).to_corner(
            UL, buff=0.35)
        s1 = label(r"`There are at least three large cities older than New York.'", font_size=26, color=CONCRETE)
        s2 = label(r"`There are at least three perfect numbers greater than 17.'", font_size=26, color=ABSTRACT)
        same = MathTex(r"\exists x\,\exists y\,\exists z\,(\,x, y, z \text{ distinct} \wedge F x \wedge F y \wedge F z "
                       r"\wedge R(x, a) \wedge \dots)", font_size=30, color=GREY_A)
        top = VGroup(s1, s2, same).arrange(DOWN, buff=0.22).move_to([0.6, 1.3, 0])
        left = VGroup(label(r"1. \ one semantics", font_size=28, color=OK),
                      label(r"the same form, \ the same kind of truth: \ reference to objects", font_size=22,
                            color=GREY_A),
                      label(r"platonism passes", font_size=22, color=OK)).arrange(DOWN, buff=0.15)
        right = VGroup(label(r"2. \ a believable epistemology", font_size=28, color=GOAL),
                       label(r"to know about objects, \ we must be causally connected to them", font_size=22,
                             color=GREY_A),
                       label(r"platonism fails: \ abstract objects cause nothing", font_size=22, color=BAD)).arrange(
            DOWN, buff=0.15)
        cols = VGroup(left, right).arrange(RIGHT, buff=1.1).move_to([0, -1.2, 0])
        moral = label(r"accounts that satisfy one \ (truth as provability, \ say) \ fail the other", font_size=24,
                      color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 1973 Paul Benacerraf turned this into a dilemma. <bookmark mark='a'/>Compare two sentences. There are "
            "at least three large cities older than New York. There are at least three perfect numbers greater than "
            "seventeen. <bookmark mark='b'/>They have the same logical form, and a good account of truth should treat "
            "them alike: each is true because certain objects exist and stand in certain relations. "
            "<bookmark mark='c'/>That is the first requirement, one semantics for all of language, and platonism "
            "meets it. <bookmark mark='d'/>The second is a believable account of knowledge. On the causal theory "
            "popular in the 1960s, to know about objects we must be causally connected to them, as we are to cities. "
            "Abstract objects cause nothing, so platonism fails it. <bookmark mark='e'/>And the accounts that make "
            "knowledge easy, for instance by saying that mathematical truth is just provability, give mathematics a "
            "different semantics from the rest of language. Either way, something gives."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(s1), FadeIn(s2))
            vo.wait_until("b")
            self.play(FadeIn(same))
            vo.wait_until("c")
            self.play(FadeIn(left))
            vo.wait_until("d")
            self.play(FadeIn(right))
            vo.wait_until("e")
            self.play(FadeIn(moral))
        self.clear_scene()

    def field(self):
        hc = history_card(1989, r"Hartry Field", r"\textit{Realism, Mathematics and Modality}", width=5.2,
                          color=HIST).to_corner(UL, buff=0.35)
        beliefs = [r"$7$ is prime", r"$\sqrt{2}$ is irrational", r"there are infinitely many primes",
                   r"Goldbach's conjecture", r"$\pi$ is transcendental"]
        facts = [True, True, True, None, True]
        lcol = VGroup(*[label(b, font_size=22, color=WHITE) for b in beliefs]).arrange(DOWN, aligned_edge=RIGHT,
                                                                                        buff=0.38)
        lcol.move_to([-1.2, -0.4, 0], aligned_edge=RIGHT)
        rcol = VGroup(*[label(r"true" if f else r"unknown", font_size=22, color=OK if f else GREY_B)
                        for f in facts]).arrange(DOWN, buff=0.38)
        for a, b in zip(rcol, lcol):
            a.move_to([2.8, b.get_y(), 0])
        lh = label(r"what mathematicians believe", font_size=24, color=CONCRETE).next_to(lcol, UP, buff=0.35)
        rh = label(r"what holds in the realm of numbers", font_size=24, color=ABSTRACT).next_to(rcol, UP, buff=0.35)
        links = VGroup(*[DashedLine(a.get_right() + RIGHT * 0.15, b.get_left() + LEFT * 0.15, color=GREY_B,
                                    stroke_width=2) for a, b, f in zip(lcol, rcol, facts) if f])
        q = label(r"why do the two columns match? \ no signal can cross", font_size=26, color=GOAL).to_edge(
            DOWN, buff=0.75)
        tail = label(r"like a villager whose beliefs about a distant city are always right, \ though no news ever "
                     r"reaches the village", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The causal theory of knowledge did not last, but in 1989 Hartry Field restated the problem without it. "
            "<bookmark mark='a'/>On one side, what mathematicians believe. On the other, what is true in the realm "
            "of numbers. <bookmark mark='b'/>The two columns match remarkably well: where mathematicians are sure, "
            "they are right. <bookmark mark='c'/>The platonist owes an explanation of that match. Nothing travels from "
            "the numbers to our brains. <bookmark mark='d'/>It is as if a villager's beliefs about a distant city were "
            "always right, though no news ever reached the village. That would be a miracle, and Field asks the "
            "platonist to explain it."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(lh), FadeIn(rh), FadeIn(lcol), FadeIn(rcol))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(x) for x in links], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(FadeIn(tail))
        self.clear_scene()
