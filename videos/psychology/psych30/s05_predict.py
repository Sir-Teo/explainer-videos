from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403

QUIZ = [
    (r"a screen rotates back toward a box behind it, \ and stops, \ or seems to pass right through it",
     r"through the box", r"5-month-olds \ (Baillargeon et al.\ 1985)", OBJ),
    (r"one doll plus one doll go behind a screen; \ it drops to show one doll, \ or two",
     r"one doll", r"5-month-olds \ (Wynn 1992)", NUM),
    (r"a box of mostly white balls; \ someone draws four red and one white, \ or four white and one red",
     r"four red", r"8-month-olds \ (Xu \& Garcia 2008)", NUM),
    (r"a voice talks to them in infant-directed speech, \ or adult-directed speech",
     r"infant-directed", r"3 to 15 months \ (ManyBabies 2020)", LOOK),
    (r"a character's ball moved while she was away; \ she searches where it is, \ or where she left it",
     r"where it is", r"15-month-olds \ (Onishi \& Baillargeon 2005)", MIND),
    (r"a pattern of 8 dots changes to 16, \ or 8 changes to 12",
     r"8 to 16", r"6-month-olds \ (Xu \& Spelke 2000)", NUM),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.quiz()
        self.answers()

    def card(self):
        card = chapter_card(4, r"On you: \ predict the infant", r"Where would a baby look longer?", lit=(),
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter four. On you: predict the infant."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(12.6, 5.4, center=[0, -0.2, 0])
        rows = VGroup()
        for i, (event, _, _, col) in enumerate(QUIZ):
            rows.add(VGroup(label(rf"{i + 1}.", font_size=24, color=col),
                            wrapped_label(event, 11.0, 22, WHITE)).arrange(RIGHT, buff=0.3, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -0.3, 0])
        with self.voiceover(
            "Your turn. Here are six experiments, each with two outcomes. For each, guess which outcome infants "
            "looked at longer. <bookmark mark='a'/> One: a screen rotates back toward a box, and either stops, or "
            "seems to pass right through it. Two: one doll plus one doll go behind a screen, which drops to show "
            "one doll or two. Three: from a box of mostly white balls, someone draws four red and one white, or four "
            "white and one red. Four: a voice speaks in infant-directed or adult-directed speech. Five: a "
            "character's ball was moved while she was away, and she searches where it is now, or where she left it. "
            "Six: a pattern of eight dots changes to sixteen, or eight changes to twelve. <bookmark mark='b'/> This "
            "part's interactive asks you the same, one at a time. Pause here and make your six guesses."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=24.0)
            vo.wait_until("b")
            self.play(Indicate(stage, color=YOU))
        self.wait(3.0)
        self.clear_scene()

    def answers(self):
        head = heading(r"What the studies reported")
        rows = VGroup()
        for i, (_, ans, who, col) in enumerate(QUIZ):
            rows.add(VGroup(label(rf"{i + 1}.", font_size=24, color=col),
                            label(rf"longer at: \ {ans}", font_size=23, color=col),
                            label(who, font_size=19, color=GREY_B)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.3, 0])
        foot = wrapped_label(r"each is a published result; \ the rest of this part asks which replicated, \ and "
                             r"what a longer look shows", 12.0, 22, LOST).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Here's what the studies reported. <bookmark mark='a'/> Five-month-olds looked longer when the screen "
            "seemed to pass through the box. Five-month-olds looked longer at one doll after one plus one. "
            "Eight-month-olds looked longer at four red balls from a mostly white box. Infants from three to "
            "fifteen months preferred infant-directed speech. Fifteen-month-olds looked longer when the character "
            "searched where the ball really was, as if they expected her to act on a false belief. And six-month-olds "
            "noticed eight changing to sixteen, but not to twelve. <bookmark mark='b'/> Each is a published result. "
            "The rest of this part asks which of them replicated, and what a longer look actually shows."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=18.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()
