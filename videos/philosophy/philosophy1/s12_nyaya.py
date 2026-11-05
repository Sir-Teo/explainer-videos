from __future__ import annotations

from videos.philosophy.philosophy1.common import *  # noqa: F403

MEMBERS = [(r"\textit{pratijñā}, thesis", r"The hill has fire."),
           (r"\textit{hetu}, reason", r"Because it has smoke."),
           (r"\textit{udāharaṇa}, example", r"Whatever has smoke has fire, like a kitchen."),
           (r"\textit{upanaya}, application", r"This hill has smoke, of the kind that goes with fire."),
           (r"\textit{nigamana}, conclusion", r"Therefore the hill has fire.")]


class Nyaya(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"The Nyāya inference", r"How did Indian logicians argue?", lit=(150,), part=PART)
        with self.voiceover("Chapter eleven. The Nyāya inference."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.five()
        self.vyapti()
        self.fallacies()

    def five(self):
        hc = history_card(r"c.\ 2nd c.", r"the \textit{Nyāya Sūtra}, attributed to Gautama", r"rules for debate and "
                          r"for valid knowledge (\textit{pramāṇa})", width=6.0, color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup()
        for k, (nm, t) in enumerate(MEMBERS, 1):
            rows.add(VGroup(MathTex(rf"{k}.", font_size=28, color=GREY_B), label(nm, font_size=24, color=P.AGENT),
                            label(t, font_size=28)).arrange(RIGHT, buff=0.3))
        for r in rows:
            r[2].next_to(r[0], RIGHT, buff=4.2)
            r[1].next_to(r[0], RIGHT, buff=0.3)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -0.9, 0])
        if rows.width > 13.2:
            rows.width = 13.2
        with self.voiceover(
            "In India, logic grew out of public debate. <bookmark mark='a'/>The Nyāya Sūtra, from around the second "
            "century, lays down an inference in five members, using the most famous example in Indian philosophy. "
            "<bookmark mark='b'/>The thesis: the hill has fire. The reason: because it has smoke. "
            "<bookmark mark='c'/>The example: whatever has smoke has fire, like a kitchen. <bookmark mark='d'/>The "
            "application: this hill has smoke of that kind. And the conclusion, restated: therefore the hill has fire."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][:2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[0][2]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
        self.clear_scene()

    def vyapti(self):
        fire = Ellipse(width=5.4, height=3.4, stroke_color=P.AGENT, stroke_width=3).move_to([-2.6, -0.4, 0])
        smoke = Ellipse(width=2.6, height=1.6, stroke_color=GREY_B, stroke_width=3).move_to([-3.0, -0.6, 0])
        lf = label(r"places with fire", font_size=24, color=P.AGENT).next_to(fire.get_top(), DOWN, buff=0.25)
        ls = label(r"with smoke", font_size=22, color=GREY_B).move_to(smoke.get_center() + UP * 0.35)
        kitchen = VGroup(Dot(color=OK), label(r"kitchen", font_size=20, color=OK)).arrange(RIGHT, buff=0.1)
        kitchen.move_to(smoke.get_center() + DOWN * 0.25)
        lake = VGroup(Dot(color=P.CLAIM), label(r"lake", font_size=20, color=P.CLAIM)).arrange(RIGHT, buff=0.1)
        lake.move_to([1.6, -2.2, 0])
        hill = VGroup(Dot(color=GOAL), label(r"hill", font_size=20, color=GOAL)).arrange(RIGHT, buff=0.1)
        hill.move_to(smoke.get_center() + LEFT * 0.7)
        dfn = definition_card(r"\textit{vyāpti}, pervasion", r"the reason is always accompanied by what it proves: "
                              r"wherever smoke, there fire", width=5.8, font_size=23, color=P.AGENT).to_corner(
            UR, buff=0.35)
        three = VGroup(label(r"Dignāga's three marks (Part 15):", font_size=24, color=GOAL),
                       label(r"present in the subject (the hill)", font_size=22),
                       label(r"present in a similar case (the kitchen)", font_size=22),
                       label(r"absent from every dissimilar case (the lake)", font_size=22)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(dfn, DOWN, buff=0.4).align_to(dfn, LEFT)
        comp = label(r"members 2--4 are Barbara (or modus ponens); \ the example says why the universal is believed",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Strip out the repetition and the core is a syllogism: all smoky places are fiery places; the hill is "
            "smoky; so the hill is fiery. <bookmark mark='a'/>What is distinctive is the example. The universal "
            "premise, called vyāpti, pervasion, says smoke is always accompanied by fire. <bookmark mark='b'/>The "
            "kitchen is a case where both are seen together; <bookmark mark='c'/>and a lake, with neither, is a case "
            "of the contrast. <bookmark mark='d'/>The Indian tradition asked the question Aristotle's logic leaves "
            "aside: how do we know the universal premise in the first place? Dignāga, in the sixth century, turned "
            "this into three formal conditions on a good reason, and we will build his wheel of reasons in Part 15, "
            "on the problem of induction."
        ) as vo:
            self.play(Create(fire), Create(smoke), FadeIn(lf), FadeIn(ls), FadeIn(hill), FadeIn(comp))
            vo.wait_until("a")
            self.play(FadeIn(dfn, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(kitchen, scale=1.3))
            vo.wait_until("c")
            self.play(FadeIn(lake, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(three, shift=UP * 0.2))
        self.clear_scene()

    def fallacies(self):
        fire = Ellipse(width=4.2, height=2.6, stroke_color=P.AGENT, stroke_width=3).move_to([-3.4, -0.6, 0])
        know = Ellipse(width=6.2, height=3.6, stroke_color=P.CLAIM, stroke_width=3).move_to([-2.6, -0.4, 0])
        lf = label(r"fiery", font_size=22, color=P.AGENT).next_to(fire.get_top(), DOWN, buff=0.2)
        lk = label(r"knowable", font_size=22, color=P.CLAIM).next_to(know.get_top(), DOWN, buff=0.2)
        lake = VGroup(Dot(color=P.CLAIM), label(r"lake", font_size=20, color=P.CLAIM)).arrange(RIGHT, buff=0.1)
        lake.move_to([-0.6, -1.4, 0])
        bad = label(r"`the hill has fire, because it is knowable'", font_size=26, color=BAD).to_edge(UP, buff=0.4)
        five = VGroup(label(r"the five pseudo-reasons (\textit{hetvābhāsa}):", font_size=24, color=GOAL),
                      label(r"inconclusive \ (\textit{savyabhicāra})", font_size=22),
                      label(r"contradictory \ (\textit{viruddha})", font_size=22),
                      label(r"counterbalanced", font_size=22), label(r"unproved", font_size=22),
                      label(r"mistimed", font_size=22)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        five.to_corner(UR, buff=0.5).shift(DOWN * 0.8)
        debate = label(r"\textit{vāda}: \ to find the truth \quad \textit{jalpa}: \ to win \quad "
                       r"\textit{vitaṇḍā}: \ only to attack", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Nyāya Sūtra also catalogues bad reasons, the pseudo-reasons. <bookmark mark='a'/>The hill has fire, "
            "because it is knowable. <bookmark mark='b'/>The reason is true of the hill, but it does not pervade the "
            "conclusion: knowable things include lakes, which have no fire. This is the inconclusive reason, and it is "
            "exactly the undistributed middle of Chapter eight, seen from India. <bookmark mark='c'/>The Sūtra lists "
            "five kinds, from the contradictory reason, which proves the opposite, to the mistimed one. "
            "<bookmark mark='d'/>And it distinguishes three kinds of debate: honest discussion aimed at truth, "
            "debate aimed at winning, and destructive cavil that only attacks: the same line the Greeks drew between "
            "dialectic and sophistry."
        ) as vo:
            self.play(FadeIn(bad))
            vo.wait_until("b")
            self.play(Create(know), Create(fire), FadeIn(lk), FadeIn(lf), FadeIn(lake, scale=1.3))
            vo.wait_until("c")
            self.play(FadeIn(five))
            vo.wait_until("d")
            self.play(FadeIn(debate))
        self.clear_scene()
