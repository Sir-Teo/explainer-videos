from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403

# Three passages are William James's, The Principles of Psychology (1890), public domain; three were written for
# this film by a language model, in his manner.  The order is fixed and the answer is given on screen.
PASSAGES = [
    (r"``Everyone knows what attention is. \ It is the taking possession by the mind, \ in clear and vivid form, \ "
     r"of one out of what seem several simultaneously possible objects or trains of thought.''", "James"),
    (r"``Habit is the groove that a repeated act wears into the nervous system, \ so that what once cost effort "
     r"comes at last to cost nothing at all.''", "model"),
    (r"``The baby, \ assailed by eyes, \ ears, \ nose, \ skin, \ and entrails at once, \ feels it all as one great "
     r"blooming, \ buzzing confusion.''", "James"),
    (r"``Memory is not a storehouse but a performance; \ each time we recall, \ we rebuild, \ and the building is "
     r"never quite the same.''", "model"),
    (r"``It is nothing jointed; \ it flows. \ A `river' or a `stream' are the metaphors by which it is most "
     r"naturally described.''", "James"),
    (r"``We do not first see and then judge; \ the judging is already in the seeing, \ and the eye arrives at its "
     r"object with an opinion.''", "model"),
]

QUESTIONS = [
    (r"1", r"A model memorized 80\% of a published test's items. \ Its score on reworded versions of the same "
           r"problems?", PERSON),
    (r"2", r"One model, \ asked in 100 phrasings, \ gives a 95\% interval three points wide. \ Is that an interval "
           r"for ``language models''?", MODEL),
    (r"3", r"Simulated respondents answer a survey. \ Their spread of answers, \ against real people's?", AUTH),
    (r"4", r"Teenagers' screen time and well-being: \ the share of variance in well-being it explains?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        card_section(self, 1, r"On you: \ human or machine, \ and four numbers", r"Can you tell?")
        self.passages()
        self.quiz()

    def passages(self):
        head = heading(r"Six sentences about the mind")
        rows = VGroup()
        for i, (t, _) in enumerate(PASSAGES):
            rows.add(VGroup(label(rf"{i + 1}", font_size=26, color=YOU), wrapped_label(t, 11.4, 19, WHITE))
                     .arrange(RIGHT, buff=0.3, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([0, -0.35, 0])
        with self.voiceover(
            "First, an experiment on you. Here are six sentences about the mind. Three are William James's, from "
            "The Principles of Psychology in 1890. Three were written for this film by a language model, asked to "
            "write in his manner. <bookmark mark='a'/> For each one, decide: James, or the machine? "
            "<bookmark mark='b'/> Pause here if you'd like to read them slowly, and write down your six answers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=6.0)
            vo.wait_until("b")
        self.wait(8.0)
        marks = VGroup(*[label(r"James" if who == "James" else r"model", font_size=20,
                               color=GOOD if who == "James" else MODEL).next_to(r, RIGHT, buff=0.2)
                         for r, (_, who) in zip(rows, PASSAGES)])
        for m_ in marks:
            keep_in_frame(m_)
        with self.voiceover(
            "Here are the answers. <bookmark mark='a'/> One, three and five are James: attention, the baby's "
            "blooming, buzzing confusion, and the stream of thought. Two, four and six are the machine's. "
            "<bookmark mark='b'/> When studies run this test with larger samples of text, people do little better "
            "than chance at telling short machine prose from human prose. That's a fact about the prose, and also "
            "about us: we judge minds by their surface."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m_, scale=1.2) for m_ in marks], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 21, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four numbers. <bookmark mark='a'/> One: a model memorized eighty percent of a published test's "
            "items. What does it score on reworded versions of the same problems? <bookmark mark='b'/> Two: one "
            "model, asked in a hundred phrasings, gives a ninety-five percent interval three points wide. Is that an "
            "interval for language models? <bookmark mark='c'/> Three: simulated respondents answer a survey. How "
            "does their spread of answers compare with real people's? <bookmark mark='d'/> And four: for teenagers' "
            "screen time and well-being, what share of the variance in well-being does screen time explain? Pause "
            "here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
