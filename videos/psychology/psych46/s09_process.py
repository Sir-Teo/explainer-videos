from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403


class Process(VoiceoverScene):
    def construct(self):
        self.card()
        self.four()
        self.satisficing()

    def card(self):
        card = chapter_card(8, r"Between the question and the answer", r"What does a respondent do?",
                            lit={1984: r"Tourangeau", 1991: r"Krosnick"}, part=PART, scale=("person",),
                            marr=("how",))
        with self.voiceover("Chapter eight. Between the question and the answer."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def four(self):
        head = heading(r"Four steps")
        data = (
            (r"comprehend", r"what is being asked? \ ``in the past week'', \ ``often'', \ ``household'': \ each word "
                            r"read differently by different people", SYMP),
            (r"retrieve", r"search memory for relevant episodes: \ Part 20's retrieval, \ with its errors of "
                          r"forgetting and timing", MODEL),
            (r"judge", r"combine what came to mind into an answer: \ estimate, \ count, \ or go by a general "
                       r"impression", PERSON),
            (r"report", r"map the judgment onto the offered categories, \ and perhaps edit it to look good", GOOD),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=19, width=2.8), wrapped_label(how, 9.2, 21, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.3, 0])
        foot = wrapped_label(r"Tourangeau's model: \ every survey error can be placed at one of the four steps, \ "
                             r"and each step has its own remedies", 12.0, 21, YOU).move_to([0, -2.5, 0])
        tag = published_tag(r"Tourangeau, Rips \& Rasinski (2000)")
        with self.voiceover(
            "A survey question looks like a measurement. It's really a small task. <bookmark mark='a'/> The "
            "respondent must comprehend it. In the past week, often, household: each word is read differently by "
            "different people. <bookmark mark='b'/> Retrieve: search memory for relevant episodes, with all of Part "
            "20's errors of forgetting and timing. <bookmark mark='c'/> Judge: combine what came to mind into an "
            "answer, by counting, estimating, or going by a general impression. <bookmark mark='d'/> And report: map "
            "the judgment onto the offered categories, and perhaps edit it to look good. <bookmark mark='e'/> Roger "
            "Tourangeau's model places every survey error at one of these steps, each with its own remedies."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def satisficing(self):
        head = heading(r"Optimizing or satisficing")
        rows = rows_of([
            (r"Krosnick, \ 1991: \ doing all four steps carefully takes effort; \ when motivation or ability is low, "
             r"\ respondents take shortcuts: \ satisficing (Simon's word, \ Part 24)", WHITE),
            (r"weak satisficing: \ the first acceptable answer, \ agreeing, \ the middle category", PERSON),
            (r"strong satisficing: \ ``don't know'', \ the same answer down a whole grid, \ or random clicks", AUTH),
            (r"it rises with difficulty and fatigue: \ late in a long questionnaire, \ on hard questions, \ among "
             r"less motivated respondents", MODEL),
            (r"the remedies are in the design: \ shorter surveys, \ clear questions, \ and reasons to care", GOOD),
        ], 12.4, 22, 0.42).move_to([0, -0.3, 0])
        tag = published_tag(r"Krosnick (1991)")
        with self.voiceover(
            "Doing all four steps carefully takes effort. <bookmark mark='a'/> Jon Krosnick argued in 1991 that when "
            "motivation or ability is low, respondents take shortcuts. He called it satisficing, Herbert Simon's word "
            "from Part 24. <bookmark mark='b'/> Weak satisficing: the first acceptable answer, agreeing, the middle "
            "category. <bookmark mark='c'/> Strong satisficing: don't know, the same answer down a whole grid, or "
            "random clicks. <bookmark mark='d'/> It rises with difficulty and fatigue: late in a long questionnaire, "
            "on hard questions, among less motivated respondents. <bookmark mark='e'/> The remedies are in the "
            "design: shorter surveys, clear questions, and reasons to care."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
