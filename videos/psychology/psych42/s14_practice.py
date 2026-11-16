from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.steps()

    def card(self):
        card = chapter_card(13, r"In practice: \ guidelines, \ choices and monitoring", r"How is a therapy chosen?",
                            lit=(), part=PART, scale=("person", "society"), marr=("how",))
        with self.voiceover("Chapter thirteen. In practice: guidelines, choices and monitoring."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def steps(self):
        head = heading(r"From evidence to a person")
        data = (
            (r"guidelines", r"panels grade the trials and recommend: \ in stepped care, \ the least intensive "
                            r"treatment likely to help comes first", SYMP),
            (r"choosing", r"the evidence for the problem, \ the person's preference, \ and what is available; \ a "
                          r"credible therapist matters as much as the brand", PERSON),
            (r"monitoring", r"a short questionnaire every session, \ with the reliable change rules of chapter "
                            r"eight: \ feedback on clients going off track reduces deterioration", GOOD),
            (r"changing course", r"no reliable change after several sessions is a reason to change the plan, \ not "
                                 r"to persist", MODEL),
            (r"for a client", r"ask what the therapy is, \ what it is for, \ how progress will be judged, \ and what "
                              r"happens if it is not working", YOU),
        )
        rows = VGroup()
        for what, how, c in data:
            rows.add(VGroup(word_chip(what, color=c, font_size=18, width=3.4), wrapped_label(how, 8.4, 19, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.3, 0])
        with self.voiceover(
            "In practice, evidence reaches a person in steps. <bookmark mark='a'/> Guidelines: panels grade the trials "
            "and recommend. In stepped care, the least intensive treatment likely to help comes first. "
            "<bookmark mark='b'/> Choosing: the evidence for the problem, the person's preference, and what's "
            "available. A credible therapist matters as much as the brand. <bookmark mark='c'/> Monitoring: a short "
            "questionnaire every session, read with chapter eight's reliable-change rules. Feedback to therapists "
            "about clients going off track reduces deterioration. <bookmark mark='d'/> Changing course: no reliable "
            "change after several sessions is a reason to change the plan, not to persist. <bookmark mark='e'/> And "
            "for a client: ask what the therapy is, what it's for, how progress will be judged, and what happens if "
            "it isn't working."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
