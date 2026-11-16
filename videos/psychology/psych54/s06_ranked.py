from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403

TECH = [(r"practice testing", r"high", GOOD), (r"distributed practice", r"high", GOOD),
        (r"elaborative interrogation", r"moderate", PERSON), (r"self-explanation", r"moderate", PERSON),
        (r"interleaved practice", r"moderate", PERSON), (r"summarization", r"low", AUTH),
        (r"highlighting", r"low", AUTH), (r"keyword mnemonic", r"low", AUTH), (r"imagery for text", r"low", AUTH),
        (r"rereading", r"low", AUTH)]


class Ranked(VoiceoverScene):
    def construct(self):
        card_section(self, 5, r"Ten techniques, \ ranked", r"Which study techniques have the evidence?",
                     scale=("person", "society"))
        self.table()
        self.why()

    def table(self):
        head = heading(r"Dunlosky and colleagues, \ 2013")
        rows = VGroup()
        for name, util, col in TECH:
            rows.add(VGroup(label(name, font_size=22, color=WHITE), word_chip(util, col, 18, width=1.8))
                     .arrange(RIGHT, buff=0.4))
        left = VGroup(*rows[:5]).arrange(DOWN, aligned_edge=RIGHT, buff=0.22).move_to([-3.3, -0.2, 0])
        right = VGroup(*rows[5:]).arrange(DOWN, aligned_edge=RIGHT, buff=0.22).move_to([3.3, -0.2, 0])
        foot = wrapped_label(r"utility judged on generality across learners, \ materials, \ tasks and delays, \ and on "
                             r"evidence in real courses", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"Dunlosky et al.\ (2013)")
        with self.voiceover(
            "In 2013 John Dunlosky and colleagues rated ten study techniques by their evidence. "
            "<bookmark mark='a'/> Two got high utility: practice testing and distributed practice. "
            "<bookmark mark='b'/> Three got moderate: elaborative interrogation, asking why a fact is true; "
            "self-explanation; and interleaved practice. <bookmark mark='c'/> Five got low: summarization, "
            "highlighting, the keyword mnemonic, imagery for text, and rereading. <bookmark mark='d'/> Utility was "
            "judged on how well each generalizes across learners, materials, tasks and delays, and on evidence from "
            "real courses. The two most popular techniques, highlighting and rereading, are at the bottom."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:2]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[2:5]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[5:]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def why(self):
        chips_section(self, r"Why the top two work", [
            (r"retrieval", r"each successful recall makes the memory more retrievable later, \ and shows what is not "
                           r"yet known", GOOD),
            (r"spacing", r"a review after some forgetting does more than one while the memory is fresh (Part 21's "
                         r"model)", MODEL),
            (r"together", r"spaced retrieval practice: \ flashcards revisited over weeks, \ cumulative quizzes", PERSON),
            (r"the cost", r"both feel slow and effortful: \ the illusion of fluency points the other way", AUTH),
        ], "Why do the top two work? <bookmark mark='a'/> Retrieval: each successful recall makes the memory more "
           "retrievable later, and shows what isn't yet known. <bookmark mark='b'/> Spacing: a review after some "
           "forgetting does more than one while the memory is fresh, which is just what Part 21's model predicts. "
           "<bookmark mark='c'/> Together they are spaced retrieval practice: flashcards revisited over weeks, and "
           "cumulative quizzes. <bookmark mark='d'/> The cost is that both feel slow and effortful, and the illusion "
           "of fluency points the other way.")
