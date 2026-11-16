from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.open_questions()

    def card(self):
        card = chapter_card(15, r"Frontier: \ causes, \ preferences and simulated respondents", r"What is next for "
                            r"choice and surveys?", lit={2014: r"Hainmueller et al."}, part=PART,
                            scale=("person", "society"), marr=("what", "how"))
        with self.voiceover("Chapter fifteen. Frontier: causes, preferences and simulated respondents."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def three(self):
        head = heading(r"Three frontiers")
        data = (
            (r"conjoint for causes", r"political scientists randomize the attributes of candidates or immigrants "
                                     r"in conjoint tasks, \ and read the average effect of each attribute as causal "
                                     r"(Hainmueller, \ Hopkins and Yamamoto, \ 2014)", MODEL),
            (r"learning preferences", r"recommender systems learn from clicks, \ and language models are tuned to "
                                      r"human preferences with a Bradley-Terry model of which answer people prefer",
             PERSON),
            (r"simulated respondents", r"language models answering survey questions in the voice of a person: \ "
                                       r"cheap, \ fast, \ and of unknown validity (Part 60)", AUTH),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=17, width=3.6), wrapped_label(how, 8.6, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.2, 0])
        tag = published_tag(r"Hainmueller, Hopkins \& Yamamoto (2014)")
        with self.voiceover(
            "Three frontiers. <bookmark mark='a'/> Conjoint for causes. Political scientists randomize the "
            "attributes of candidates or immigrants in conjoint tasks, and read the average effect of each attribute "
            "as causal. <bookmark mark='b'/> Learning preferences. Recommender systems learn from clicks, and language "
            "models are tuned to human preferences with a Bradley-Terry model of which of two answers people prefer. "
            "Thurstone's method is inside them. <bookmark mark='c'/> And simulated respondents: language models "
            "answering survey questions in the voice of a person. Cheap, fast, and of unknown validity. Part 60 "
            "returns to them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"when do stated choices in a survey predict what people actually buy, \ vote for or do?", WHITE),
            (r"can one model of comparison explain all three context effects, \ and their dependence on time?", MODEL),
            (r"how should a preference model handle people who disagree, \ rather than average them away?", PERSON),
            (r"when, \ if ever, \ can simulated respondents stand in for real ones?", AUTH),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        with self.voiceover(
            "Open questions. <bookmark mark='a'/> When do stated choices in a survey predict what people actually "
            "buy, vote for, or do? <bookmark mark='b'/> Can one model of comparison explain all three context "
            "effects, and how they depend on time? <bookmark mark='c'/> How should a model of preferences handle "
            "people who disagree, rather than average them away? <bookmark mark='d'/> And when, if ever, can "
            "simulated respondents stand in for real ones?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
