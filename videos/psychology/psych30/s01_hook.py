from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.game()
        self.puzzle()
        self.question()
        self.objectives()

    def _cups(self):
        a = cup(A_COL).move_to([-2.0, -1.2, 0])
        b = cup(B_COL).move_to([2.0, -1.2, 0])
        la = label(r"A", font_size=30, color=A_COL).next_to(a, DOWN, buff=0.2)
        lb = label(r"B", font_size=30, color=B_COL).next_to(b, DOWN, buff=0.2)
        return VGroup(a, b, la, lb)

    def game(self):
        kid = baby(0.9).move_to([0, 2.2, 0])
        cups = self._cups()
        toy = Star(n=5, outer_radius=0.25, color=OBJ, fill_opacity=1).move_to([-2.0, -0.2, 0])
        tally = label(r"hidden at A: \ found at A", font_size=24, color=A_COL).to_edge(DOWN, buff=0.7)
        tag = historical_tag(r"Piaget (1937)")
        with self.voiceover(
            "A ten-month-old sits at a table with two cups in front of her. <bookmark mark='a'/> You show her a "
            "toy and hide it under the left cup, A. She reaches, lifts the cup, and finds it. "
            "<bookmark mark='b'/> You do it again, and again: hidden at A, found at A. "
            "<bookmark mark='c'/> Now, while she watches, you hide the toy under the right cup, B. She saw it go "
            "there. And she reaches for A."
        ) as vo:
            self.play(FadeIn(kid), FadeIn(cups), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(toy))
            self.play(toy.animate.move_to([-2.0, -1.0, 0]), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(tally))
            vo.wait_until("c")
            self.play(toy.animate.move_to([2.0, -1.0, 0]), run_time=1.0)
            arrow = Arrow(kid.get_bottom(), cups[0].get_top(), color=A_COL, buff=0.2, stroke_width=6)
            self.play(GrowArrow(arrow))
            self.play(Indicate(cups[0], color=A_COL))
        self.clear_scene()

    def puzzle(self):
        head = heading(r"The A-not-B error")
        rows = rows_of([
            (r"Jean Piaget saw it in his own three children, \ and described it in 1937", WHITE),
            (r"infants of about eight to twelve months search where they found the toy before, \ not where they "
             r"saw it go", A_COL),
            (r"Piaget's reading: \ for the infant, \ the toy is not yet an object that exists on its own; \ it is "
             r"part of the action that found it", OBJ),
            (r"but an infant cannot tell you what she thinks: \ how could anyone find out what she knows?", LOOK),
        ], 12.2, 26, 0.42).move_to([0, -0.2, 0])
        tag = historical_tag(r"Piaget (1937)")
        with self.voiceover(
            "This is the A-not-B error. <bookmark mark='a'/> Jean Piaget saw it in his own three children, and "
            "described it in 1937. <bookmark mark='b'/> Infants of about eight to twelve months search where they "
            "found the toy before, not where they saw it go. <bookmark mark='c'/> Piaget's reading was that for the "
            "infant the toy is not yet an object that exists on its own, but part of the action that found it. "
            "<bookmark mark='d'/> There's a deeper problem underneath. An infant can't tell you what she thinks. "
            "How could anyone find out what she knows?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ what does a baby know?")
        rows = rows_of([
            (r"Piaget's theory, \ built from watching", WHITE),
            (r"the instrument that replaced it: \ how long a baby looks", LOOK),
            (r"that instrument tested in 65 laboratories at once, \ and recomputed here", NUM),
            (r"objects, \ number and statistics in the first year, \ and an error explained by dynamics", OBJ),
            (r"other minds, \ attachment, \ temperament, \ and learning from others", CARE),
        ], 12.6, 27, 0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "So this part asks what a baby knows, and how you can find out. <bookmark mark='a'/> We'll start with "
            "Piaget's theory, built from watching. <bookmark mark='b'/> Then the instrument that replaced it: how "
            "long a baby looks. <bookmark mark='c'/> Then that instrument tested in sixty-five laboratories at "
            "once, and recomputed here from the open data. <bookmark mark='d'/> Then objects, number and "
            "statistics in the first year, and the A-not-B error explained as dynamics. "
            "<bookmark mark='e'/> And then other minds, attachment, temperament, and how children learn from "
            "other people."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 30", font_size=34, color=GREY_B), label(r"The Infant Mind", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Piaget's stages, \ and what his method could and could not show",
            r"looking time as an instrument: \ habituation, \ surprise, \ and the Goldilocks effect",
            r"ManyBabies: \ one effect in 65 laboratories, \ with its moderators recomputed",
            r"objects, \ number and statistics: \ core knowledge against construction",
            r"A-not-B as a dynamic field, \ simulated",
            r"other minds, \ attachment and learning from others, \ with their replication records",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 30 of Psychology, Built: the infant mind, and the first part of Act Seven. "
            "<bookmark mark='a'/> We'll set out Piaget's stages and what his method could and could not show. "
            "We'll treat looking time as an instrument, with habituation, surprise and the Goldilocks effect. We'll "
            "recompute ManyBabies, one effect measured in sixty-five laboratories, with its moderators. We'll weigh "
            "core knowledge against construction for objects, number and statistics. We'll simulate the A-not-B "
            "error as a dynamic field. And we'll end with other minds, attachment and learning from others, each "
            "with its replication record."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
