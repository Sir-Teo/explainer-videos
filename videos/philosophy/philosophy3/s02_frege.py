from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy3.common import *  # noqa: F403


def frege_cond(top: str, bottom: str, x0=0.0, y0=0.0, w=2.6, color=WHITE, judge=True):
    """Frege's two-dimensional conditional: the consequent on the upper stroke, the antecedent below, joined by a
    vertical stroke; a judgement stroke at the left."""
    g = VGroup()
    if judge:
        g.add(Line([x0, y0 + 0.25, 0], [x0, y0 - 0.25, 0], color=color, stroke_width=4))
    g.add(Line([x0, y0, 0], [x0 + w, y0, 0], color=color, stroke_width=3))
    xc = x0 + w * 0.45
    g.add(Line([xc, y0, 0], [xc, y0 - 0.8, 0], color=color, stroke_width=3))
    g.add(Line([xc, y0 - 0.8, 0], [x0 + w, y0 - 0.8, 0], color=color, stroke_width=3))
    t = MathTex(top, font_size=40, color=GOAL).next_to([x0 + w, y0, 0], RIGHT, buff=0.15)
    b = MathTex(bottom, font_size=40, color=VAR).next_to([x0 + w, y0 - 0.8, 0], RIGHT, buff=0.15)
    g.add(t, b)
    return g


def frege_all(body: str, var: str, x0=0.0, y0=0.0, w=2.6, color=WHITE):
    """Frege's generality: a concavity in the content stroke holding a German letter."""
    g = VGroup(Line([x0, y0 + 0.25, 0], [x0, y0 - 0.25, 0], color=color, stroke_width=4))
    xc = x0 + w * 0.4
    g.add(Line([x0, y0, 0], [xc - 0.25, y0, 0], color=color, stroke_width=3))
    cup = ArcBetweenPoints([xc - 0.25, y0, 0], [xc + 0.25, y0, 0], angle=PI, color=color, stroke_width=3)
    g.add(cup)
    g.add(Line([xc + 0.25, y0, 0], [x0 + w, y0, 0], color=color, stroke_width=3))
    g.add(MathTex(rf"\mathfrak{{{var}}}", font_size=34, color=QUANT).move_to([xc, y0 + 0.22, 0]))
    g.add(MathTex(body, font_size=40, color=GOAL).next_to([x0 + w, y0, 0], RIGHT, buff=0.15))
    return g


class Frege(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Frege's concept-script", r"How do you write `all' and `some' exactly?",
                            lit=(1879,), part=PART)
        with self.voiceover("Chapter one. Frege's concept-script."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.notation()
        self.function()
        self.reception()

    def notation(self):
        hc = history_card(1879, r"Gottlob Frege, Jena", r"\textit{Begriffsschrift}: `a formula language of pure "
                          r"thought, modelled on that of arithmetic'", width=6.2, color=HIST).to_corner(UL, buff=0.35)
        cond = frege_cond(r"B", r"A", x0=-5.6, y0=-0.4)
        cl = MathTex(r"= \ A \to B", font_size=40).next_to(cond, RIGHT, buff=0.4)
        gen = frege_all(r"F(\mathfrak{a})", "a", x0=0.8, y0=-0.4)
        gl = MathTex(r"= \ \forall a\, F(a)", font_size=40).next_to(gen, DOWN, buff=0.5).align_to(gen, RIGHT)
        notes = VGroup(label(r"the judgement stroke: \ `this is asserted'", font_size=22, color=GREY_A),
                       label(r"the consequent above, the antecedent below", font_size=22, color=GREY_A),
                       label(r"a concavity with a letter: \ `for every'", font_size=22, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1879 Gottlob Frege, a mathematician at Jena, published a short book with a long subtitle: a formula "
            "language of pure thought, modelled on that of arithmetic. He called it Begriffsschrift, concept-script. "
            "<bookmark mark='a'/>It was written in two dimensions. A vertical stroke at the left asserts what follows. "
            "'If A then B' puts B on the top line and A below, joined by a vertical stroke. <bookmark mark='b'/>And "
            "'for every a, F of a' is a small cup in the line, holding a Gothic letter. It looks nothing like what we "
            "write today, but it is the same logic, and it was complete."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(cond), run_time=2)
            self.play(Write(cl), FadeIn(notes[:2]))
            vo.wait_until("b")
            self.play(Create(gen), run_time=2)
            self.play(Write(gl), FadeIn(notes[2]))
        self.clear_scene()

    def function(self):
        old = VGroup(label(r"Aristotle:", font_size=26, color=GREY_A),
                     label(r"[Socrates] \ is \ [mortal]", font_size=34),
                     label(r"subject \quad copula \quad predicate", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.15)
        new = VGroup(label(r"Frege:", font_size=26, color=GREY_A),
                     MathTex(r"\mathrm{Mortal}(\mathrm{Socrates})", font_size=40),
                     label(r"a function, \ and its argument", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.15)
        both = VGroup(old, new).arrange(RIGHT, buff=1.6).move_to([0, 1.4, 0])
        fn = MathTex(r"\mathrm{Mortal}(\ \cdot\ ):\ \text{objects} \to \{\mathrm{T}, \mathrm{F}\}", font_size=36,
                     color=CONN).move_to([0, -0.4, 0])
        rel = VGroup(MathTex(r"\mathrm{Loves}(\mathrm{Ann}, \mathrm{Bo})", font_size=36, color=REL),
                     MathTex(r"\mathrm{Between}(a, b, c)", font_size=36, color=REL)).arrange(RIGHT, buff=1.0).move_to(
            [0, -1.6, 0])
        rl = label(r"relations: \ functions of two, three, \dots\ arguments", font_size=24, color=GREY_A).next_to(
            rel, DOWN, buff=0.25)
        with self.voiceover(
            "Frege's deepest move was to drop subject and predicate. <bookmark mark='a'/>For Aristotle, 'Socrates is "
            "mortal' joins a subject to a predicate with the copula 'is'. <bookmark mark='b'/>For Frege, 'mortal' is "
            "a function, and Socrates its argument. <bookmark mark='c'/>The function maps each object to a truth "
            "value: true for the mortals, false for everything else. Frege called such functions concepts. "
            "<bookmark mark='d'/>And nothing limits a function to one argument. 'Loves' takes two, 'between' takes "
            "three. The relations that defeated Aristotle are just functions of several arguments."
        ) as vo:
            self.play(FadeIn(old))
            vo.wait_until("a")
            self.play(Indicate(old, color=P.CLAIM))
            vo.wait_until("b")
            self.play(FadeIn(new))
            vo.wait_until("c")
            self.play(Write(fn))
            vo.wait_until("d")
            self.play(FadeIn(rel), FadeIn(rl))
        self.clear_scene()

    def reception(self):
        hcs = VGroup(history_card(1889, r"Giuseppe Peano", r"linear notation; $\exists$ (1897)", width=4.2,
                                  color=HIST, font_size=20),
                     history_card(1910, r"Whitehead \& Russell", r"\textit{Principia Mathematica}", width=4.2,
                                  color=HIST, font_size=20),
                     history_card(1935, r"Gerhard Gentzen", r"$\forall$, the upside-down A", width=4.2, color=HIST,
                                  font_size=20)).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.5)
        q = quote_card(r"I find in your work discussions, distinctions, and definitions that one seeks in vain in the "
                       r"works of other logicians.", r"Russell to Frege, 16 June 1902", r"trans.\ in van Heijenoort, "
                       r"\textit{From Frege to Gödel}", width=10.0, font_size=28).move_to([0, -0.9, 0])
        fwd = label(r"the same letter announced the paradox that wrecked Frege's system: \ Part 6", font_size=24,
                    color=BAD).to_edge(DOWN, buff=0.4)
        rev = VGroup(frege_cond(r"B", r"A", x0=-1.4, y0=0.9, w=2.0),
                     label(r"reviews of 1880 (Schröder, Venn): \ cumbersome, \ a step back from Boole", font_size=24,
                           color=GREY_A)).arrange(DOWN, buff=0.4).move_to([0, -0.2, 0])
        with self.voiceover(
            "Almost no one read the Begriffsschrift. Its notation was mocked as unreadable, and Frege spent his "
            "life in obscurity at Jena. <bookmark mark='a'/>The logic spread in other people's notation: Giuseppe "
            "Peano's linear symbols, Whitehead and Russell's Principia Mathematica, and the upside-down A for 'all', "
            "introduced by Gentzen in 1935. <bookmark mark='b'/>In 1902 Russell wrote to Frege that he found in his "
            "work distinctions one seeks in vain in other logicians. <bookmark mark='c'/>The same letter contained a "
            "paradox that destroyed the system Frege had built on this logic, as we will see in Part 6."
        ) as vo:
            self.play(FadeIn(rev))
            vo.wait_until("a")
            self.play(FadeOut(rev), LaggedStart(*[FadeIn(h, shift=DOWN * 0.2) for h in hcs], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(fwd))
        self.clear_scene()
