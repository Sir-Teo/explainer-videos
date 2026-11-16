from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.project()
        self.untested()
        self.choose()
        self.question()
        self.objectives()

    def project(self):
        head = heading(r"The degree ends with a project")
        rows = rows_of([
            (r"forty-two parts have built a model subject, \ a laboratory, \ a measurement library, \ a false-positive "
             r"lab and a Ledger of findings", WHITE),
            (r"a degree ends the way research begins: \ with one study, \ done properly, \ from the choice of target to "
             r"the report", PERSON),
            (r"this part replicates two classic effects, \ on screen, \ with every tool the series has built", MODEL),
            (r"the plan is written down before the data are read, \ and the narration of the results is computed from "
             r"them", YOU),
        ], 12.4, 24, 0.48).move_to([0, -0.3, 0])
        with self.voiceover(
            "A degree ends with a project. <bookmark mark='a'/> Forty-two parts have built a model subject, a "
            "laboratory, a measurement library, a false-positive lab, and a Ledger of findings. "
            "<bookmark mark='b'/> A degree ends the way research begins: with one study, done properly, from the "
            "choice of target to the report. <bookmark mark='c'/> This part replicates two classic effects, on "
            "screen, with every tool the series has built. <bookmark mark='d'/> The plan is written down before the "
            "data are read, and the narration of the results is computed from them."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def untested(self):
        head = heading(r"A row never tested")
        card = ledger_card({f.key: f for f in ledger.rows(part=29)}["bridge_misattribution"], width=12.4, font_size=20)
        card.move_to([0, 0.6, 0])
        rows = rows_of([
            (r"four rows of the Ledger are marked ``not directly tested''; \ the fear bridge of Part 29 is one", WHITE),
            (r"a good target is important, \ genuinely uncertain, \ and feasible: \ a frightening bridge, \ and an "
             r"interviewer to fall for, \ are hard to standardize", AUTH),
        ], 12.4, 21, 0.3).move_to([0, -2.5, 0])
        with self.voiceover(
            "Where to start? <bookmark mark='a'/> Four rows of the Ledger are marked not directly tested. The fear "
            "bridge of Part 29 is one: men who met a woman on a frightening bridge were said to be more attracted to "
            "her. <bookmark mark='b'/> A good target is important, genuinely uncertain, and feasible. A frightening "
            "bridge, and an interviewer to fall for, are hard to standardize across laboratories, so it's left for "
            "someone with a bridge."
        ) as vo:
            self.play(FadeIn(head), FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim), FadeIn(card.original),
                      FadeIn(card.status))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def choose(self):
        head = heading(r"Two targets")
        left = VGroup(word_chip(r"expected to hold", color=GOOD, font_size=20, width=4.2),
                      wrapped_label(r"verbal overshadowing (Part 21): \ describing a face you have just seen makes you "
                                    r"worse at picking it from a line-up", 5.0, 20, WHITE))
        right = VGroup(word_chip(r"in doubt", color=AUTH, font_size=20, width=4.2),
                       wrapped_label(r"ego depletion (Part 28): \ a demanding task leaves less self-control for the next "
                                     r"one", 5.0, 20, WHITE))
        for g in (left, right):
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, 0.9, 0])
        rows = rows_of([
            (r"both have open, \ lab-by-lab data from registered multi-lab replications, \ so the film's numbers are "
             r"real and fixed", MODEL),
            (r"and you can take part in a third: \ the Stroop task, \ on the course site, \ whose effect no one "
             r"doubts", YOU),
        ], 12.4, 22, 0.36).move_to([0, -1.8, 0])
        with self.voiceover(
            "So two targets are chosen. <bookmark mark='a'/> One expected to hold: verbal overshadowing, from Part 21. "
            "Describing a face you've just seen makes you worse at picking it out of a line-up. "
            "<bookmark mark='b'/> And one in doubt: ego depletion, from Part 28. A demanding task leaves less "
            "self-control for the next one. <bookmark mark='c'/> Both have open, lab-by-lab data from registered "
            "multi-lab replications, so the numbers in this film are real and fixed. <bookmark mark='d'/> And you can "
            "take part in a third, on the course site: the Stroop task, whose effect no one doubts."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            for m, r in zip("cd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ can you run a study that deserves to be believed?")
        rows = rows_of([
            (r"what counts as the same study, \ and how many people it needs", SYMP),
            (r"the plan, \ written as code and tested on simulated data", MODEL),
            (r"the experiment, \ the ethics, \ and the data", PERSON),
            (r"the confirmatory test, \ the verdict, \ the exploration, \ and the report", GOOD),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks whether you can run a study that deserves to be believed. <bookmark mark='a'/> What "
            "counts as the same study, and how many people it needs. <bookmark mark='b'/> The plan, written as code "
            "and tested on simulated data. <bookmark mark='c'/> The experiment, the ethics, and the data. "
            "<bookmark mark='d'/> And then the confirmatory test, the verdict, the exploration, and the report."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 43", font_size=34, color=GREY_B), label(r"The Replication", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"choosing a target, \ and what makes a replication direct",
            r"the smallest effect of interest, \ power, \ and small telescopes",
            r"preregistration as code, \ run on simulated data first",
            r"the experiment, \ consent, \ and open multi-lab data",
            r"the confirmatory analysis, \ three criteria and a Bayes factor",
            r"exploration, \ labelled, \ and the report; \ then the degree, \ looked back on",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 43 of Psychology, Built: the replication. <bookmark mark='a'/> We'll choose a target, and "
            "say what makes a replication direct. We'll set the smallest effect of interest, compute power, and meet "
            "the small telescopes. We'll write the preregistration as code, and run it on simulated data first. "
            "We'll build the experiment, ask for consent, and read open multi-lab data. We'll run the confirmatory "
            "analysis, with three criteria and a Bayes factor. And we'll explore, labelled as such, write the report, "
            "and look back on the degree."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
