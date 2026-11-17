from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.where()
        self.ratings()

    def card(self):
        card = chapter_card(14, r"In practice: \ pricing, \ polls and leaderboards", r"Where do these models run?",
                            lit=(), part=PART, scale=("person", "society"), marr=("how",))
        with self.voiceover("Chapter fourteen. In practice: pricing, polls and leaderboards."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def where(self):
        head = heading(r"Where they run")
        data = (
            (r"pricing", r"choice-based conjoint before a launch: \ which features, \ at what price; \ checked "
                         r"against sales afterwards", MODEL),
            (r"survey design", r"cognitive interviews before fielding: \ ask people to think aloud while answering, \ "
                               r"to catch misread words", SYMP),
            (r"polling", r"wording and order fixed and published; \ split samples to measure their effect; \ sampling "
                         r"and weighting in \emph{Statistics, Built} Part 18", PERSON),
            (r"transport and health", r"discrete-choice models of travel, \ and of which treatments patients "
                                      r"would choose", GOOD),
        )
        rows = VGroup()
        for what, how, c in data:
            rows.add(VGroup(word_chip(what, color=c, font_size=18, width=3.6), wrapped_label(how, 8.2, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "Where these models run. <bookmark mark='a'/> Pricing: choice-based conjoint before a launch, to decide "
            "which features to offer at what price, checked against sales afterwards. <bookmark mark='b'/> Survey "
            "design: cognitive interviews before fielding, where people think aloud while answering, to catch "
            "misread words. <bookmark mark='c'/> Polling: wording and order fixed and published, and split samples "
            "to measure their effect. Sampling and weighting are Statistics, Built's Part 18. <bookmark mark='d'/> "
            "And transport and health: discrete-choice models of how people travel, and of which treatments patients "
            "would choose."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def ratings(self):
        head = heading(r"Leaderboards are paired comparisons")
        rows = rows_of([
            (r"chess ratings, \ sports rankings and the arenas that rank AI chatbots all fit Bradley and Terry's model "
             r"to wins and losses", WHITE),
            (r"the same questions as Thurstone's: \ is one dimension enough, \ and are the comparisons independent?",
             MODEL),
            (r"who chooses the pairs matters: \ if strong players meet only each other, \ the scale stretches", PERSON),
            (r"and the voters are a sample: \ an arena's rating is a fact about its voters' preferences, \ not about "
             r"everyone's", AUTH),
            (r"report the uncertainty: \ a ranking gap smaller than its error is not a ranking", YOU),
        ], 12.4, 22, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "One more place these models run. <bookmark mark='a'/> Chess ratings, sports rankings, and the arenas "
            "that rank AI chatbots by people's votes all fit Bradley and Terry's model to wins and losses. "
            "<bookmark mark='b'/> So they face Thurstone's questions. Is one dimension enough? Are the comparisons "
            "independent? <bookmark mark='c'/> Who chooses the pairs matters. If strong players meet only each "
            "other, the scale stretches. <bookmark mark='d'/> And the voters are a sample. An arena's rating is a fact "
            "about its voters' preferences, not everyone's. <bookmark mark='e'/> Report the uncertainty. A gap "
            "smaller than its error isn't a ranking."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
