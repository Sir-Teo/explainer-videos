from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.open()

    def card(self):
        card = chapter_card(15, r"Frontier: \ foundation models and precision mapping", r"What comes after the "
                            r"group map?", lit=(), part=PART, scale=("brain",), marr=("what",))
        with self.voiceover("Chapter fifteen. Frontier: foundation models and precision mapping."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def three(self):
        head = heading(r"Three frontiers")
        items = [
            (r"foundation models of brain activity", r"networks trained on thousands of hours of recordings from many "
                                                     r"people, \ then adapted to new people and tasks: \ promising, \ "
                                                     r"and still to be shown better than simple baselines", MODEL),
            (r"naturalistic stimuli", r"films and stories in place of flashing checkerboards: \ richer data, \ "
                                      r"analysed with encoding models, \ at the cost of control", PERSON),
            (r"precision mapping", r"many hours of scanning per person: \ individual maps that differ from the group "
                                   r"average in where networks lie, \ Part 47's lesson in the brain", GOOD),
        ]
        rows = VGroup()
        for name, what, col in items:
            rows.add(VGroup(word_chip(name, col, 20, width=4.6), wrapped_label(what, 7.6, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.3, 0])
        with self.voiceover(
            "Three frontiers. <bookmark mark='a'/> Foundation models of brain activity: networks trained on "
            "thousands of hours of recordings from many people, then adapted to new people and new tasks. They're "
            "promising, and they still have to be shown to beat simple baselines. <bookmark mark='b'/> Naturalistic "
            "stimuli: films and stories in place of flashing checkerboards, giving richer data for encoding models, "
            "at the cost of control. <bookmark mark='c'/> And precision mapping: many hours of scanning per person, "
            "giving individual maps that differ from the group average in where networks lie. It's Part 47's lesson, "
            "in the brain."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"which analysis choices matter most, \ and can a field agree on defaults without freezing its methods?",
             WHITE),
            (r"is a group map, \ or a person's own map, \ the right object for a theory of the mind?", PERSON),
            (r"what would it take for a brain measure to predict an individual's behaviour well enough to use?", AUTH),
            (r"when a network predicts brain activity, \ what has been explained?", MODEL),
        ], 12.4, 24, 0.5).move_to([0, -0.3, 0])
        with self.voiceover(
            "Open questions. <bookmark mark='a'/> Which analysis choices matter most, and can a field agree on "
            "defaults without freezing its methods? <bookmark mark='b'/> Is a group map, or a person's own map, the "
            "right object for a theory of the mind? <bookmark mark='c'/> What would it take for a brain measure to "
            "predict one person's behaviour well enough to use? <bookmark mark='d'/> And when a network predicts "
            "brain activity, what has been explained?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
