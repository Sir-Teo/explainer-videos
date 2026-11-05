from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy1.common import *  # noqa: F403

ROUTE = [(r"Athens", r"4th c.\ BCE", [-5.6, 0.6, 0]), (r"Alexandria", r"6th c.", [-3.2, -0.6, 0]),
         (r"Baghdad", r"9th--10th c.", [-0.4, 0.4, 0]), (r"Bukhara, Isfahan", r"11th c.", [2.2, 0.9, 0]),
         (r"Córdoba, Toledo", r"12th c.", [-2.2, 2.0, 0]), (r"Paris, Oxford", r"13th c.", [0.6, 2.6, 0])]


class Arabic(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Logic in Arabic: al-Fārābī and Avicenna", r"How did Aristotle's logic travel, and "
                            r"what did it gain?", lit=(830, 950, 1037, 1180), part=PART)
        with self.voiceover("Chapter twelve. Logic in Arabic: al-Fārābī and Avicenna."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.route()
        self.debate()
        self.avicenna()

    def route(self):
        dots, labs, arrows = VGroup(), VGroup(), VGroup()
        for name, when, pos in ROUTE:
            d = Dot(pos, radius=0.1, color=GOAL)
            dots.add(d)
            labs.add(VGroup(label(name, font_size=24), label(when, font_size=18, color=GREY_A)).arrange(
                DOWN, buff=0.05).next_to(d, DOWN, buff=0.12))
        for a, b in zip(dots, dots[1:]):
            arrows.add(Arrow(a.get_center(), b.get_center(), buff=0.15, color=CONN, stroke_width=3))
        sch = schematic_tag(corner=DR)
        hc = history_card(r"c.\ 830", r"Baghdad: the translation movement", r"Ḥunayn ibn Isḥāq and others translate "
                          r"Aristotle's logic into Arabic, often through Syriac", width=5.6, color=HIST)
        hc.to_corner(DR, buff=0.4).shift(UP * 0.4)
        with self.voiceover(
            "Aristotle's logic did not pass straight from Athens to Europe. <bookmark mark='a'/>It was taught in late "
            "antique Alexandria, carried into Syriac, and then, in the eighth to tenth centuries, translated into "
            "Arabic in Abbasid Baghdad, by scholars such as Ḥunayn ibn Isḥāq. <bookmark mark='b'/>For three centuries "
            "the most advanced logic in the world was written in Arabic, in Baghdad, Bukhara and Isfahan. "
            "<bookmark mark='c'/>From there it crossed to Córdoba and Toledo, where Arabic commentaries were "
            "translated into Latin, and reached the universities of Paris and Oxford in the thirteenth century."
        ) as vo:
            self.play(FadeIn(dots[0]), FadeIn(labs[0]), FadeIn(sch))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0]), FadeIn(dots[1]), FadeIn(labs[1]))
            self.play(GrowArrow(arrows[1]), FadeIn(dots[2]), FadeIn(labs[2]), FadeIn(hc))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[2]), FadeIn(dots[3]), FadeIn(labs[3]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[3]), FadeIn(dots[4]), FadeIn(labs[4]))
            self.play(GrowArrow(arrows[4]), FadeIn(dots[5]), FadeIn(labs[5]))
        self.clear_scene()

    def debate(self):
        hc = history_card(932, r"Baghdad: Abū Bishr Mattā against al-Sīrāfī", r"is logic universal, or only "
                          r"the grammar of Greek?", width=6.2, color=HIST).to_corner(UL, buff=0.4)
        sides = VGroup(
            VGroup(label(r"the logician", font_size=28, color=P.CLAIM),
                   label(r"logic is the tool for every language", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12),
            VGroup(label(r"the grammarian", font_size=28, color=P.AGENT),
                   label(r"`logic' is Greek grammar in disguise", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=1.4).move_to([0, -0.1, 0])
        far = history_card(r"c.\ 870--950", r"al-Fārābī, `the Second Teacher'", r"logic concerns the meanings all "
                           r"languages share, as grammar concerns the words of one", width=6.8, color=HIST)
        far.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "With translation came a philosophical question. <bookmark mark='a'/>In 932, at the court of the vizier "
            "in Baghdad, the logician Abū Bishr Mattā debated the grammarian Abū Saʿīd al-Sīrāfī. "
            "<bookmark mark='b'/>Is logic a universal tool of reasoning, or only the grammar of Greek, which Arabic "
            "speakers have no need of? It is the question this part's Mohist and Nyāya logics make urgent. "
            "<bookmark mark='c'/>Al-Fārābī, called the Second Teacher, after Aristotle, gave the standard answer: "
            "grammar concerns the words of one language; logic concerns the meanings that all languages share."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(sides))
            vo.wait_until("c")
            self.play(FadeIn(far, shift=UP * 0.2))
        self.clear_scene()

    def avicenna(self):
        hc = history_card(r"980--1037", r"Avicenna (Ibn Sīnā)", r"\textit{al-Shifāʾ}, `The Cure': a logic that "
                          r"replaced Aristotle's as the standard text", width=5.8, color=HIST).to_corner(UL, buff=0.4)
        s = label(r"`Every writer moves his fingers.'", font_size=34, color=GOAL).move_to([0.6, 1.0, 0])
        r1 = VGroup(label(r"as long as he exists", font_size=26, color=P.CLAIM),
                    label(r"substantial reading: \ false", font_size=24, color=BAD)).arrange(DOWN, buff=0.1)
        r2 = VGroup(label(r"as long as he writes", font_size=26, color=P.AGENT),
                    label(r"descriptional reading: \ true", font_size=24, color=OK)).arrange(DOWN, buff=0.1)
        rr = VGroup(r1, r2).arrange(RIGHT, buff=1.8).move_to([0.6, -0.5, 0])
        more = label(r"also: \ syllogisms with `if' and `or' (hypothetical syllogistic), \ joined to Aristotle's",
                     font_size=24, color=GREY_A).to_edge(DOWN, buff=0.9)
        aver = label(r"Averroes (1126--1198), `the Commentator': \ the Arabic Aristotle reaches Latin Europe",
                     font_size=24, color=HIST).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The greatest of the Arabic logicians was Avicenna, Ibn Sīnā, physician and philosopher, whose logic "
            "replaced Aristotle's own text as the standard in the Islamic world. <bookmark mark='a'/>He noticed that "
            "a sentence like 'every writer moves his fingers' has two readings. <bookmark mark='b'/>Every writer, as "
            "long as he exists, moves his fingers: false. Every writer, as long as he writes, moves his fingers: "
            "true. <bookmark mark='c'/>Avicenna built a whole logic on such temporal and modal readings, and joined "
            "to it a logic of sentences with 'if' and 'or', the territory the Stoics had opened. "
            "<bookmark mark='d'/>A century later Averroes wrote the commentaries on Aristotle that Latin Europe "
            "studied for three hundred years. When Leibniz dreamed of calculating, he was the heir of all these "
            "traditions."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(s))
            vo.wait_until("b")
            self.play(FadeIn(r1, shift=UP * 0.2))
            self.play(FadeIn(r2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(more))
            vo.wait_until("d")
            self.play(FadeIn(aver))
        self.clear_scene()
