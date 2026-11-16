from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403


class Ethics(VoiceoverScene):
    def construct(self):
        self.card()
        self.consent()
        self.screen()

    def card(self):
        card = chapter_card(6, r"Consent, \ and what participants are told", r"What does a participant agree to?",
                            lit=(), part=PART, scale=("person", "society"), marr=("what",))
        with self.voiceover("Chapter six. Consent, and what participants are told."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def consent(self):
        head = heading(r"Before anyone takes part")
        data = (
            (r"review", r"an ethics committee approves the protocol: \ risks, \ benefits, \ and who may take part", SYMP),
            (r"consent", r"what will happen, \ how long it takes, \ that one may stop at any time, \ and what is done "
                         r"with the data", PERSON),
            (r"what is not said", r"the hypothesis is usually withheld, \ since knowing it changes behaviour (Part "
                                  r"2's demand); \ withholding is not lying", MODEL),
            (r"debriefing", r"afterwards, \ the purpose is explained, \ and any deception undone", GOOD),
            (r"data", r"stored without names, \ shared only as consent allows; \ this course's site stores and sends "
                      r"nothing", YOU),
        )
        rows = VGroup()
        for what, how, c in data:
            rows.add(VGroup(word_chip(what, color=c, font_size=18, width=3.4), wrapped_label(how, 8.4, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to([0, -0.3, 0])
        with self.voiceover(
            "Before anyone takes part. <bookmark mark='a'/> An ethics committee approves the protocol: its risks, its "
            "benefits, and who may take part. <bookmark mark='b'/> Consent: what will happen, how long it takes, that "
            "a person may stop at any time, and what's done with the data. <bookmark mark='c'/> What isn't said: the "
            "hypothesis is usually withheld, since knowing it changes behaviour, Part 2's demand effects. Withholding "
            "isn't lying. <bookmark mark='d'/> Debriefing: afterwards, the purpose is explained, and any deception "
            "undone. <bookmark mark='e'/> And the data: stored without names, and shared only as consent allows. This "
            "course's site stores and sends nothing at all."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def screen(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        head = label(r"Before you start", font_size=30, color=WHITE).move_to([0, 2.0, 0])
        lines = rows_of([
            (r"This is a short colour-naming task: \ 48 words, \ about three minutes.", WHITE),
            (r"Name the colour of the ink as fast as you can; \ you may stop at any time, \ and nothing happens if "
             r"you do.", WHITE),
            (r"Your answers and times stay in this browser: \ nothing is stored or sent, \ and the page shows them "
             r"only to you.", GOOD),
            (r"Afterwards the page explains what the task measures, \ and what your result can and cannot say.", SYMP),
        ], 10.4, 21, 0.38).move_to([0, -0.2, 0])
        btn = word_chip(r"Start, \ or close this page", color=YOU, font_size=20).move_to([0, -2.4, 0])
        note = label(r"the course site's consent screen, \ shown as it reads", font_size=14, color=GREY_B).to_corner(DR,
                                                                                                             buff=0.3)
        with self.voiceover(
            "Here's what consent looks like for this part's own study, the Stroop task on the course site. "
            "<bookmark mark='a'/> What will happen, and how long it takes. <bookmark mark='b'/> What to do, and that "
            "you may stop at any time, with nothing lost. <bookmark mark='c'/> What happens to the data: here, "
            "nothing leaves your browser. <bookmark mark='d'/> And a promise of a debriefing: what the task measures, "
            "and what one person's result can and can't say."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(head), FadeIn(note))
            for m, r in zip("abcd", lines):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            self.play(FadeIn(btn))
        self.wait(1.0)
        self.clear_scene()
