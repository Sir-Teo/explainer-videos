from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403

OPEN = [
    (r"consciousness", r"which theory, \ if any, \ survives an adversarial test (Part 27)", AUTH),
    (r"a unified model", r"one Psyche, \ one set of parameters, \ every task (Parts 58 and 62)", MODEL),
    (r"learning in the brain", r"which learning rule cortex uses (Part 58)", MODEL),
    (r"the individual", r"measures reliable enough to describe and help one person (Parts 47 and 59)", PERSON),
    (r"causes of disorder", r"mechanisms that predict who becomes ill, \ and who recovers (Parts 39 to 42)", CARE),
    (r"development", r"how a child learns so much from so little (Parts 30 and 60)", GOOD),
    (r"culture", r"which findings are human, \ and which are local (Part 38)", SYMP),
    (r"the field itself", r"incentives that select for rigour (Parts 4, \ 50 and 61)", YOU),
]


class Frontier(VoiceoverScene):
    def construct(self):
        card_section(self, 15, r"Frontier: \ the open problems of sixty-two parts", r"What is not known?",
                     scale=("person", "society"))
        self.map()

    def map(self):
        head = heading(r"Eight open problems, \ gathered from every Frontier")
        rows = VGroup()
        for name, what, col in OPEN:
            rows.add(VGroup(word_chip(name, col, 19, width=3.4), wrapped_label(what, 8.8, 19, WHITE))
                     .arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -0.3, 0])
        with self.voiceover(
            "What isn't known? Here are eight open problems, gathered from every part's frontier chapter. "
            "<bookmark mark='a'/> Consciousness: which theory, if any, survives an adversarial test. "
            "<bookmark mark='b'/> A unified model: one Psyche, with one set of parameters, doing every task. "
            "<bookmark mark='c'/> Learning in the brain: which learning rule cortex uses. <bookmark mark='d'/> The "
            "individual: measures reliable enough to describe and help one person. <bookmark mark='e'/> The causes "
            "of disorder: mechanisms that predict who becomes ill, and who recovers. <bookmark mark='f'/> "
            "Development: how a child learns so much from so little. <bookmark mark='g'/> Culture: which findings "
            "are human, and which are local. <bookmark mark='h'/> And the field itself: incentives that select for "
            "rigour. Each one is a dissertation, or a career."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcdefgh", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
