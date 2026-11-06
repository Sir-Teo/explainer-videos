from __future__ import annotations

import itertools

from videos.philosophy.philosophy9.common import *  # noqa: F403


def concept_icon(members, n=4, r=0.09, gap=0.26, color=NUM) -> VGroup:
    """A concept on a domain of n objects: n dots in a row, lit where the object falls under the concept."""
    g = VGroup(*[Dot(radius=r, color=color if i in members else GREY_D) for i in range(n)]).arrange(RIGHT,
                                                                                                    buff=gap - 2 * r)
    box = SurroundingRectangle(g, buff=0.09, corner_radius=0.06, stroke_color=GREY_C, stroke_width=1.2)
    return VGroup(box, g)


class Logicism(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Numbers from logic", r"Could arithmetic be logic in disguise?", lit=(1781, 1884),
                            part=PART)
        with self.voiceover("Chapter two. Numbers from logic."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.kant()
        self.concepts()
        self.hume()
        self.caesar()

    def kant(self):
        left = VGroup(label(r"Kant (1781)", font_size=30, color=HIST),
                      MathTex(r"7 + 5 = 12", font_size=48, color=NUM),
                      label(r"\textit{synthetic a priori}: \ the idea of $7 + 5$ does not contain $12$;", font_size=22,
                            color=GREY_A),
                      label(r"we must count, \ in intuition, \ on our fingers", font_size=22, color=GREY_A)).arrange(
            DOWN, buff=0.22)
        right = VGroup(label(r"Frege (1884)", font_size=30, color=HIST),
                       MathTex(r"7 + 5 = 12", font_size=48, color=NUM),
                       label(r"\textit{analytic}: \ provable from logic and definitions alone", font_size=22,
                             color=GREY_A),
                       label(r"arithmetic is logic, \ unfolded", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.22)
        cols = VGroup(left, right).arrange(RIGHT, buff=1.6).move_to([0, 0.5, 0])
        moral = label(r"if Frege is right, \ mathematics is known a priori because logic is, \ and needs no special "
                      r"faculty", font_size=24, color=OK).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The second answer is that mathematics is logic. <bookmark mark='a'/>Immanuel Kant had argued, in 1781, "
            "that seven plus five equals twelve is synthetic a priori: known without experience, yet not true by "
            "definition, because the idea of seven plus five does not already contain twelve. To get twelve we must "
            "count, in intuition, as children count on their fingers. <bookmark mark='b'/>Gottlob Frege disagreed. "
            "Arithmetic, he held, is analytic: provable from logic and definitions alone, logic unfolded. "
            "<bookmark mark='c'/>If Frege was right, mathematics is known a priori because logic is, and we need no "
            "special faculty to know it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.clear_scene()

    def concepts(self):
        hc = history_card(1884, r"Gottlob Frege", r"\textit{Die Grundlagen der Arithmetik}", width=5.2,
                          color=HIST).to_corner(UL, buff=0.35)
        cards = VGroup(*[VGroup(label(a, font_size=26, color=NUM), label(b, font_size=22, color=GREY_A)).arrange(
            DOWN, buff=0.12) for a, b in (
            (r"one", r"\textit{pack of cards}"), (r"four", r"\textit{suits}"), (r"fifty-two", r"\textit{cards}"))]
        ).arrange(RIGHT, buff=1.0).move_to([0.8, 1.2, 0])
        same = label(r"the same pile: \ a number belongs to a \textit{concept}, \ not to a thing", font_size=26,
                     color=GOAL).next_to(cards, DOWN, buff=0.45)
        rows = VGroup(label(r"`Jupiter has four moons' \ = \ the number of the concept \textit{moon of Jupiter} is "
                            r"four", font_size=24),
                      label(r"(Frege's count; \ today, \ more than ninety: \ the concept's extension changed)",
                            font_size=21, color=GREY_B),
                      label(r"`Venus has no moons' \ = \ the number of \textit{moon of Venus} is $0$", font_size=24),
                      MathTex(r"0 = \#[x : x \neq x]", font_size=40, color=NUM)).arrange(DOWN, buff=0.24).next_to(
            same, DOWN, buff=0.45)
        with self.voiceover(
            "Frege's book of 1884, The Foundations of Arithmetic, starts from an observation. <bookmark mark='a'/>"
            "Hand someone a pile of cards and ask for its number. It is one pack, four suits, or fifty-two cards. "
            "<bookmark mark='b'/>The pile is the same; what differs is the concept we count under. A number belongs "
            "to a concept, not to a heap of things. <bookmark mark='c'/>'Jupiter has four moons' says that the "
            "number of the concept 'moon of Jupiter' is four. Frege's count was four; today we know of more than "
            "ninety, because what falls under the concept changed. <bookmark mark='d'/>'Venus has no moons' gives "
            "the concept 'moon of Venus' the number zero, and Frege defines zero itself as the number of a concept "
            "nothing can fall under: not identical with itself."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(same))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.clear_scene()

    def hume(self):
        d = load("frege")
        q = quote_card(r"When two numbers are so combin'd, as that the one has always an unite answering to every unite "
                       r"of the other, we pronounce them equal.", r"David Hume", r"\textit{Treatise} I.iii.1, \ 1739",
                       width=10.6, font_size=26).to_edge(UP, buff=0.3)
        hp = MathTex(r"\#F = \#G \;\iff\; F \approx G", font_size=40, color=NUM).next_to(q, DOWN, buff=0.3)
        gloss = label(r"Hume's principle: \ the number of $F$s is the number of $G$s \ iff \ they correspond one to "
                      r"one", font_size=22, color=GREY_A).next_to(hp, DOWN, buff=0.15)
        cols = VGroup()
        for k in range(5):
            col = VGroup(*[concept_icon(set(c)) for c in itertools.combinations(range(4), k)]).arrange(DOWN, buff=0.1)
            cols.add(col)
        cols.arrange(RIGHT, buff=0.55, aligned_edge=UP).move_to([0, -1.75, 0])
        nums = VGroup(*[MathTex(str(k), font_size=34, color=NUM).next_to(cols[k], UP, buff=0.12) for k in range(5)])
        succ = VGroup(*[Arrow(nums[k].get_right(), nums[k + 1].get_left(), buff=0.25, color=OK, stroke_width=3,
                              max_tip_length_to_length_ratio=0.2) for k in range(4)])
        assert d["class_sizes"] == [1, 4, 6, 4, 1] and d["successor"] == [[0, 1], [1, 2], [2, 3], [3, 4]]
        note_ = label(rf"the Reasoner: \ {d['concepts']} concepts on four objects \ fall into "
                      rf"{len(d['class_sizes'])} numbers: \ 1, 4, 6, 4, 1", font_size=22, color=OK).to_corner(
            DR, buff=0.3).shift(UP * 0.1)
        with self.voiceover(
            "How do we tell when two concepts have the same number? <bookmark mark='a'/>Frege took the answer from "
            "David Hume's Treatise: when two numbers are so combined, as that the one has always a unit answering to "
            "every unit of the other, we pronounce them equal. <bookmark mark='b'/>In modern dress: the number of "
            "Fs equals the number of Gs exactly when the Fs and the Gs can be paired off one to one. This is now "
            "called Hume's principle. <bookmark mark='c'/>The Reasoner tries it on a world of four objects. A concept "
            "is any selection of them, so there are sixteen concepts. Pairing them off sorts them into five "
            "classes, one for each number from zero to four, of sizes one, four, six, four and one: the row of "
            "Pascal's triangle. <bookmark mark='d'/>And Frege's successor relation runs from each number to the "
            "next: n plus one is the number of a concept that has one more object than a concept with n."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(hp), FadeIn(gloss))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in cols], lag_ratio=0.3), FadeIn(nums), run_time=3)
            self.play(FadeIn(note_))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowArrow(a) for a in succ], lag_ratio=0.3))
        self.clear_scene()

    def caesar(self):
        head = label(r"The Julius Caesar problem", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"Hume's principle says when $\#F = \#G$", font_size=26),
            label(r"but not whether \ $\#F = $ Julius Caesar", font_size=26, color=GOAL),
            label(r"so it does not yet say \textit{what} numbers are", font_size=26),
            label(r"Frege's fix: \ $\#F$ \ = \ the extension of the concept `equinumerous with $F$'", font_size=24,
                  color=NUM),
            label(r"extensions need Basic Law V, \ and Basic Law V is inconsistent: \ Russell's letter (Part 6)",
                  font_size=24, color=BAD)).arrange(DOWN, buff=0.35).move_to([0, -0.2, 0])
        with self.voiceover(
            "But Frege was not satisfied. <bookmark mark='a'/>Hume's principle tells us when the number of Fs is the "
            "number of Gs. <bookmark mark='b'/>It does not tell us whether the number of Fs is Julius Caesar. Frege's "
            "example sounds silly, but the point is serious: <bookmark mark='c'/>a principle that only says when two "
            "numbers are equal does not yet say what numbers are. <bookmark mark='d'/>So Frege defined them "
            "explicitly: the number of F is the extension of the concept 'equinumerous with F', roughly the class of "
            "all concepts that pair off with F. <bookmark mark='e'/>Extensions needed his Basic Law Five, and Part 6 "
            "told what happened next: Russell's letter of 1902, and the contradiction. Logicism seemed dead for "
            "eighty years."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
