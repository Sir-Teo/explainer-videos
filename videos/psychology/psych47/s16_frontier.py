from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.open_questions()

    def card(self):
        card = chapter_card(15, r"Frontier: \ the science of one", r"Can psychology be about individuals, \ at scale?",
                            lit={2018: r"Fisher et al."}, part=PART, scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter fifteen. Frontier: the science of one."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def three(self):
        head = heading(r"Three frontiers")
        data = (
            (r"idiographic at scale", r"a model for each person, \ fitted to their own months of data, \ and then "
                                      r"compared across thousands of persons", MODEL),
            (r"how much data", r"how many stimuli, \ occasions and people a claim needs, \ planned like power for "
                               r"each level at once", PERSON),
            (r"streams and models", r"phones and wearables give sleep, \ movement and speech continuously; \ joining "
                                    r"them to models of a mind is new, \ and privacy comes first", GOOD),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=17, width=3.6), wrapped_label(how, 8.6, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.2, 0])
        with self.voiceover(
            "Three frontiers. <bookmark mark='a'/> Idiographic science at scale: a model for each person, fitted to "
            "their own months of data, then compared across thousands of persons. <bookmark mark='b'/> How much data: "
            "how many stimuli, occasions and people a claim needs, planned like power at every level at once. "
            "<bookmark mark='c'/> And streams and models: phones and wearables record sleep, movement and speech "
            "continuously. Joining them to models of a mind is new, and privacy comes first."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"which psychological processes are close enough to ergodic that group studies describe individuals?",
             WHITE),
            (r"how many occasions does one person's model need before it beats the population's?", MODEL),
            (r"can early-warning signals be read from data people will actually give?", AUTH),
            (r"how should a field choose and report its stimuli, \ so that claims say what they cover?", PERSON),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        with self.voiceover(
            "Open questions. <bookmark mark='a'/> Which psychological processes are close enough to ergodic that "
            "group studies describe individuals? <bookmark mark='b'/> How many occasions does one person's model need "
            "before it beats the population's? <bookmark mark='c'/> Can early-warning signals be read from the data "
            "people will actually give? <bookmark mark='d'/> And how should a field choose and report its stimuli, so "
            "that its claims say what they cover?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
