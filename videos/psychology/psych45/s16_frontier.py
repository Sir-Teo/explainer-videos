from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.open_questions()

    def card(self):
        card = chapter_card(15, r"Frontier: \ time, \ generated items and learning systems", r"What is next for "
                            r"measurement?", lit={2007: r"van der Linden"}, part=PART, scale=("person",),
                            marr=("what", "how"))
        with self.voiceover("Chapter fifteen. Frontier: time, generated items and learning systems."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def three(self):
        head = heading(r"Three frontiers")
        data = (
            (r"response times", r"every answer comes with a time; \ van der Linden's hierarchical model treats speed "
                                r"as a second trait, \ joining Part 25's models of deciding to testing", MODEL),
            (r"generated items", r"language models can write thousands of items; \ their difficulty can be "
                                 r"predicted from their features, \ but each still needs calibration on people", PERSON),
            (r"learning systems", r"a test-taker that improves between items, \ or between versions, \ breaks the "
                                  r"assumption that ability holds still", AUTH),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=18, width=3.2), wrapped_label(how, 8.8, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.2, 0])
        tag = published_tag(r"van der Linden (2007)")
        with self.voiceover(
            "Three frontiers. <bookmark mark='a'/> Response times. Every answer comes with a time. Wim van der "
            "Linden's hierarchical model treats speed as a second trait, joining Part 25's models of deciding to "
            "testing. <bookmark mark='b'/> Generated items. Language models can write thousands of items, and their "
            "difficulty can be predicted from their features, but each still needs calibrating on people. "
            "<bookmark mark='c'/> And learning systems. A test-taker that improves between items, or between "
            "versions, breaks the assumption that ability holds still."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"when is a fast wrong answer a guess, \ and a slow right one a careful thinker?", WHITE),
            (r"can generated items be calibrated without pre-testing each one on people?", PERSON),
            (r"how should a scale be kept stable when the test-takers, \ human or machine, \ change faster than the "
             r"items?", AUTH),
            (r"can an adaptive test be fair to every group while still choosing the most informative item?", MODEL),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        with self.voiceover(
            "Open questions. <bookmark mark='a'/> When is a fast wrong answer a guess, and a slow right one a careful "
            "thinker? <bookmark mark='b'/> Can generated items be calibrated without pre-testing each one on people? "
            "<bookmark mark='c'/> How should a scale be kept stable when the test-takers, human or machine, change "
            "faster than the items? <bookmark mark='d'/> And can an adaptive test be fair to every group while still "
            "choosing the most informative item?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
