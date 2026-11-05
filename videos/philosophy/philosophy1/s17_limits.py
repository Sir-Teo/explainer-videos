from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy1.common import *  # noqa: F403


class Limits(VoiceoverScene):
    def construct(self):
        card = chapter_card(16, r"What the syllogism cannot say", r"Where does Aristotle's logic run out?",
                            lit=(1847, 1879), part=PART)
        with self.voiceover("Chapter sixteen. What the syllogism cannot say."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.relations()
        self.scope()
        self.next_()

    def relations(self):
        kant = quote_card(r"Since Aristotle it has not had to retrace a single step \dots\ and to the present day it "
                          r"has not been able to advance a single step, and is thus to all appearance a closed and "
                          r"completed body of doctrine.", r"Kant, \textit{Critique of Pure Reason}, B viii (1787)",
                          r"trans.\ Kemp Smith", width=10.4, font_size=27).move_to([0, 0.3, 0])
        hc = history_card(r"1847--1860", r"Augustus De Morgan", r"the logic of relations", width=5.0, color=HIST)
        hc.to_corner(UL, buff=0.4)
        arg = VGroup(label(r"Every horse is an animal.", font_size=34),
                     label(r"So every head of a horse is the head of an animal.", font_size=34, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([0.6, 0.6, 0])
        why_ = label(r"obviously valid, \ yet not one of the 256 moods: \ `head of' is a relation", font_size=28,
                     color=BAD).next_to(arg, DOWN, buff=0.6)
        older = VGroup(label(r"Socrates is older than Plato; \ Plato is older than Aristotle;", font_size=28),
                       label(r"so Socrates is older than Aristotle.", font_size=28, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "For two thousand years, Aristotle's logic was simply logic. Kant wrote in 1787 that it had not had to "
            "take a single step backward since Aristotle, nor been able to take one forward. "
            "<bookmark mark='a'/>But in the 1840s and 1850s Augustus De Morgan pointed to an argument no syllogism "
            "can capture. Every horse is an animal; so every head of a horse is the head of an animal. "
            "<bookmark mark='b'/>Obviously valid, and yet it is not one of the two hundred and fifty-six moods, "
            "because 'head of' is a relation between two things, and syllogistic only has one-place terms. "
            "<bookmark mark='c'/>The same goes for 'older than': Socrates is older than Plato, Plato than Aristotle, "
            "so Socrates is older than Aristotle."
        ) as vo:
            self.play(FadeIn(kant, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(kant), FadeIn(hc), FadeIn(arg))
            vo.wait_until("b")
            self.play(FadeIn(why_))
            vo.wait_until("c")
            self.play(FadeIn(older))
        self.clear_scene()

    @staticmethod
    def love_graph(pairs, color, center):
        names = ["Ann", "Bo", "Cy"]
        pos = [np.array(center) + 1.0 * np.array([np.cos(a), np.sin(a), 0])
               for a in (PI / 2 + 2 * PI / 3, PI / 2 - 2 * PI / 3, PI / 2)]
        dots = VGroup(*[Dot(p, radius=0.09, color=WHITE) for p in pos])
        labs = VGroup(*[label(n, font_size=22, color=GREY_A).next_to(d, DOWN if i < 2 else UP, buff=0.12)
                        for i, (n, d) in enumerate(zip(names, dots))])
        arrows = VGroup()
        for a, b in pairs:
            if a == b:
                loop = Arc(radius=0.22, start_angle=-PI / 4, angle=1.5 * PI, color=color, stroke_width=3).move_to(
                    pos[a] + np.array([0.4, -0.05, 0]))
                loop.add_tip(tip_length=0.12, tip_width=0.12)
                arrows.add(loop)
            else:
                arrows.add(Arrow(pos[a], pos[b], buff=0.14, color=color, stroke_width=3,
                                 max_tip_length_to_length_ratio=0.15))
        return VGroup(dots, labs, arrows)

    def scope(self):
        a = VGroup(label(r"Everyone loves someone.", font_size=34, color=P.CLAIM),
                   MathTex(r"\forall x\, \exists y\ \mathrm{Loves}(x, y)", font_size=40, color=P.CLAIM)).arrange(
            DOWN, buff=0.25)
        b = VGroup(label(r"Someone is loved by everyone.", font_size=34, color=P.AGENT),
                   MathTex(r"\exists y\, \forall x\ \mathrm{Loves}(x, y)", font_size=40, color=P.AGENT)).arrange(
            DOWN, buff=0.25)
        ab = VGroup(a, b).arrange(RIGHT, buff=1.6).move_to([0, 2.3, 0])
        ring = self.love_graph([(0, 1), (1, 2), (2, 0)], P.CLAIM, [-3.3, -1.15, 0])
        star = self.love_graph([(0, 2), (1, 2), (2, 2)], P.AGENT, [3.3, -1.15, 0])
        rv = VGroup(label(r"a ring: \ first true, \ second false", font_size=24, color=GREY_A)).next_to(
            ring, DOWN, buff=0.35)
        sv = VGroup(label(r"all love Cy: \ both true", font_size=24, color=GREY_A)).next_to(star, DOWN, buff=0.35)
        imp = label(r"the second implies the first; \ not the other way round", font_size=28, color=GOAL)
        imp.move_to([0, 0.75, 0])
        pre = label(r"the notation of Part 3 (Frege 1879): \ quantifiers, variables, relations", font_size=26,
                    color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Worse, syllogistic cannot stack quantifiers. <bookmark mark='a'/>Everyone loves someone. "
            "<bookmark mark='b'/>Someone is loved by everyone. These say very different things. "
            "<bookmark mark='g1'/>Picture three people in a ring, each loving the next. Everyone loves someone, and "
            "yet no one is loved by everyone. <bookmark mark='g2'/>Now let all three love Cy, and Cy love herself. "
            "Then both sentences are true. <bookmark mark='i'/>The second implies the first, but not the other way "
            "round. <bookmark mark='c'/>To see why, you need to write 'every' and 'some' as separate operators with "
            "their own variables, and track the order in which they apply. That notation, invented by Frege in 1879, "
            "is the subject of Part 3. Mathematics is full of sentences like these: for every epsilon there is a "
            "delta. A logic that cannot express them cannot express mathematics."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(a[0]))
            vo.wait_until("b")
            self.play(FadeIn(b[0]))
            vo.wait_until("g1")
            self.play(FadeIn(ring[:2]))
            self.play(LaggedStart(*[GrowArrow(x) for x in ring[2]], lag_ratio=0.4), FadeIn(rv))
            vo.wait_until("g2")
            self.play(FadeIn(star[:2]))
            self.play(LaggedStart(*[Create(x) for x in star[2]], lag_ratio=0.4), FadeIn(sv))
            vo.wait_until("i")
            self.play(FadeIn(imp))
            vo.wait_until("c")
            self.play(Write(a[1]), Write(b[1]))
            self.play(FadeIn(pre))
        self.clear_scene()

    def next_(self):
        two = VGroup(
            VGroup(label(r"Part 2: \ the logic of whole sentences", font_size=30, color=P.CLAIM),
                   label(r"and, or, not, if: \ Boole, truth tables, SAT", font_size=24, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(label(r"Part 3: \ the logic inside sentences", font_size=30, color=P.AGENT),
                   label(r"all, some, relations: \ Frege, models, proof", font_size=24, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([0, 0.3, 0])
        with self.voiceover(
            "So the next two parts split Aristotle's question in two. <bookmark mark='a'/>Part 2 builds the logic of "
            "whole sentences joined by and, or, not and if, the Stoics' logic, made into Boole's algebra and then "
            "into the solvers inside every chip. <bookmark mark='b'/>Part 3 opens sentences up, with Frege's "
            "quantifiers and relations. Together they are the machinery of reason that Leibniz dreamed of, and the "
            "first place where we will see exactly how far it reaches."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(two[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(two[1], shift=RIGHT * 0.2))
        self.clear_scene()
