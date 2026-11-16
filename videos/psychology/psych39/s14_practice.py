from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.uses()
        self.checklist()

    def card(self):
        card = chapter_card(13, r"In practice: \ diagnosis, \ screening and risk tools",
                            r"What is a diagnosis for?", lit=(), part=PART, scale=("person", "group"),
                            marr=("what",))
        with self.voiceover("Chapter thirteen. In practice: diagnosis, screening and risk tools."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def uses(self):
        head = heading(r"What a diagnosis is used for")
        items = [
            (r"treatment", r"a shared name that points to evidence about what helps", GOOD),
            (r"payment", r"insurers and health services pay by code; \ the threshold decides who is covered", PERSON),
            (r"research", r"a way to group people for trials, \ with the heterogeneity of chapter five", SYMP),
            (r"rights", r"school support, \ workplace adjustments, \ disability benefits", MODEL),
            (r"identity", r"some people find a name a relief, \ others a weight", WHITE),
        ]
        rows = VGroup()
        for what, how, c in items:
            rows.add(VGroup(word_chip(what, color=c, font_size=19, width=2.8), wrapped_label(how, 8.8, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.2, 0])
        with self.voiceover(
            "A diagnosis does many jobs, and they pull in different directions. <bookmark mark='a'/> Treatment: a "
            "shared name that points to evidence about what helps. <bookmark mark='b'/> Payment: health services and "
            "insurers pay by code, so the threshold decides who's covered. <bookmark mark='c'/> Research: a way to "
            "group people for trials, with all the variety of chapter five. <bookmark mark='d'/> Rights: support at "
            "school, adjustments at work, disability benefits. <bookmark mark='e'/> And identity: some people find a "
            "name a relief, and others a weight."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def checklist(self):
        head = heading(r"A checklist score is not a diagnosis")
        rows = rows_of([
            (r"screening questionnaires are built to catch most cases, \ so they flag many people who are not "
             r"cases: \ chapter one's 9\%", WHITE),
            (r"a positive screen should lead to an assessment by a clinician, \ not to a label", SYMP),
            (r"risk tools in practice, \ from suicide risk scales to violence risk instruments, \ have the same "
             r"problem when the outcome is rare: \ most people flagged will not have the outcome", AUTH),
            (r"the formulas of chapter ten beat judgment; \ they still cannot beat the base rate", MODEL),
            (r"good practice: \ say what the score means in natural frequencies, \ and decide what follows from a "
             r"positive before you screen", YOU),
        ], 12.4, 21, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "And a warning that applies to every app and questionnaire. <bookmark mark='a'/> Screening tools are "
            "built to catch most cases, so they flag many people who aren't cases, like the nine percent in chapter "
            "one. <bookmark mark='b'/> A positive screen should lead to an assessment by a clinician, not to a label. "
            "<bookmark mark='c'/> Risk tools in practice, from suicide risk scales to violence risk instruments, "
            "have the same problem when the outcome is rare. Most people flagged won't have the outcome. "
            "<bookmark mark='d'/> The formulas of chapter ten beat judgment. They still can't beat the base rate. "
            "<bookmark mark='e'/> Good practice: say what a score means in natural frequencies, and decide what "
            "follows from a positive before you screen."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
