from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403


class Llm(VoiceoverScene):
    def construct(self):
        self.card()
        self.battery()
        self.checks()
        self.explain()

    def card(self):
        card = chapter_card(12, r"Language models as models of minds", r"Is predicting behaviour the same as "
                            r"explaining it?", lit={2023: r"Binz \& Schulz"}, part=PART, scale=("mind",),
                            marr=("what", "how"))
        with self.voiceover("Chapter twelve. Language models as models of minds."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def battery(self):
        head = heading(r"Giving a model the Battery")
        rows = rows_of([
            (r"a language model can be given a psychology experiment as text, \ and its answers scored like a "
             r"participant's", WHITE),
            (r"Binz and Schulz, \ 2023: \ on classic judgment tasks some models answered much like people, \ biases "
             r"included, \ and failed in other places", MODEL),
            (r"later, \ models fine-tuned on trial-level data from many experiments were offered as general models "
             r"of human choice, \ predicting held-out participants well", PERSON),
            (r"the same checks apply as to any model: \ recovery, \ comparison against simple models, \ and whether "
             r"it produces the effects for the right reasons", AUTH),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        tag = published_tag(r"Binz \& Schulz (2023)")
        with self.voiceover(
            "A new kind of candidate model. <bookmark mark='a'/> A language model can be given a psychology "
            "experiment as text, and its answers scored like a participant's. <bookmark mark='b'/> In 2023 Marcel Binz "
            "and Eric Schulz gave classic judgment tasks to such a model. On some it answered much like people, "
            "biases included, and it failed in other places. <bookmark mark='c'/> Later, models fine-tuned on "
            "trial-level data from many experiments were offered as general models of human choice, predicting "
            "held-out participants well. <bookmark mark='d'/> The same checks apply as to any model: recovery, "
            "comparison against simple models, and whether it produces the effects for the right reasons."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def explain(self):
        head = heading(r"Prediction against explanation")
        data = (
            (r"for prediction", r"if a model predicts what people do in new situations, \ it has learned something "
                                r"real about behaviour", GOOD),
            (r"against", r"a model as complex as the mind leaves the explaining still to do: \ we understand it no "
                         r"better than the people it imitates", AUTH),
            (r"a middle way", r"use the large model as a benchmark: \ how much of the predictable behaviour does a "
                              r"small, \ interpretable model capture?", MODEL),
            (r"returns", r"Part 60 asks what such systems are; \ Part 61 asks what they change about the science",
             PERSON),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=18, width=3.0), wrapped_label(how, 9.2, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.2, 0])
        with self.voiceover(
            "Which raises an old question in a new form. <bookmark mark='a'/> For prediction: if a model predicts what "
            "people do in new situations, it has learned something real about behaviour. <bookmark mark='b'/> "
            "Against: a model as complex as the mind leaves the explaining still to do. We understand it no better "
            "than the people it imitates. <bookmark mark='c'/> A middle way: use the large model as a benchmark. How "
            "much of the predictable behaviour does a small, interpretable model capture? <bookmark mark='d'/> Part 60 "
            "asks what such systems are, and Part 61 what they change about the science."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def checks(self):
        chips_section(self, r"Testing a language model as a model of mind", [
            (r"contamination", r"classic tasks are on the web; \ a model may have read the answers: \ use new "
                               r"items and new stories", AUTH),
            (r"process", r"do its errors, \ and the difficulty it finds in each item, \ match people's? \ "
                         r"surprisal and reading times (Part 23) are one such test", MODEL),
            (r"people, \ not a person", r"a model's answer distribution is not one person's: \ compare it with "
                                         r"the spread across people, \ not the mean", PERSON),
            (r"the baseline", r"beat the simple fitted model of each task before claiming more", GOOD),
        ], "How should a language model be tested as a model of mind? <bookmark mark='a'/> Watch for contamination. "
           "Classic tasks are on the web, and a model may have read the answers, so use new items and new stories. "
           "<bookmark mark='b'/> Test process. Do its errors, and the difficulty it finds in each item, match "
           "people's? Surprisal predicting reading times, from Part 23, is one such test. <bookmark mark='c'/> "
           "Remember it's people, not a person. A model's answers form a distribution that isn't one person's, so "
           "compare it with the spread across people, not just the mean. <bookmark mark='d'/> And beat the "
           "baseline: the simple fitted model of each task, before claiming more.", chip_w=3.6, text_w=8.6)
