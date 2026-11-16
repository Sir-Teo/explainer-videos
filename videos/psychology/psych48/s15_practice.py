from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.where()
        self.phenotype()

    def card(self):
        card = chapter_card(14, r"In practice: \ phenotypes, \ users and tutors", r"Where do fitted models of "
                            r"behaviour run?", lit=(), part=PART, scale=("person", "society"), marr=("how",))
        with self.voiceover("Chapter fourteen. In practice: phenotypes, users and tutors."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def where(self):
        head = heading(r"Where they run")
        data = (
            (r"computational phenotyping", r"fitting task models to patients, \ to describe what differs: \ "
                                           r"recovery and reliability first (Part 59)", MODEL),
            (r"user modelling", r"learning-rate and exploration models of how people use a product; \ the same "
                                r"trade-offs between parameters apply", SYMP),
            (r"simulated users", r"testing a design against model users before real ones: \ cheap, \ and only as "
                                 r"good as the model's recovery and predictions", PERSON),
            (r"tutoring systems", r"Part 45's knowledge tracing is a fitted model of each learner, \ updated after "
                                  r"every answer", GOOD),
            (r"the checklist", r"simulate, \ recover, \ compare, \ check predictions, \ fit hierarchically, \ never "
                               r"fit an average and call it a person", YOU),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=16, width=3.8), wrapped_label(how, 8.6, 19, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.3, 0])
        with self.voiceover(
            "Where fitted models of behaviour run. <bookmark mark='a'/> Computational phenotyping fits task models to "
            "patients, to describe what differs. Recovery and reliability come first, as Part 59 will show. "
            "<bookmark mark='b'/> User modelling fits learning and exploration to how people use a product, with the "
            "same trade-offs between parameters. <bookmark mark='c'/> Simulated users test a design before real ones: "
            "cheap, and only as good as the model's recovery and predictions. <bookmark mark='d'/> Tutoring systems "
            "run Part 45's knowledge tracing, a fitted model of each learner updated after every answer. "
            "<bookmark mark='e'/> And one checklist for all of them: simulate, recover, compare, check predictions, "
            "fit hierarchically, and never fit an average and call it a person."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def phenotype(self):
        rows_section(self, r"A computational phenotype, \ worked", [
            (r"a clinic wants to know whether patients with anxiety learn from losses differently: \ a bandit "
             r"task, \ 200 choices each", WHITE),
            (r"the plan: \ simulate the task with the candidate models; \ check that the loss learning rate is "
             r"recoverable from 200 choices (chapter four)", MODEL),
            (r"fit hierarchically (chapter eight), \ compare models by cross-validation (chapter six), \ and "
             r"check the winner reproduces stay-after-loss (chapter seven)", PERSON),
            (r"then test the group difference on the parameter, \ with its uncertainty, \ preregistered, \ "
             r"and retest some patients to see if the parameter is stable (the Ledger)", GOOD),
            (r"a parameter that is not recoverable or not stable is not a phenotype, \ however good the story", YOU),
        ], "Here's a computational phenotype, worked. <bookmark mark='a'/> A clinic wants to know whether patients "
           "with anxiety learn from losses differently. It uses a bandit task, two hundred choices each. "
           "<bookmark mark='b'/> First, simulate the task with the candidate models, and check that the learning rate "
           "for losses is recoverable from two hundred choices. <bookmark mark='c'/> Fit hierarchically, compare "
           "models by cross-validation, and check that the winner reproduces stay-after-loss. <bookmark mark='d'/> "
           "Then test the group difference on the parameter, with its uncertainty, preregistered, and retest some "
           "patients to see whether the parameter is stable. <bookmark mark='e'/> A parameter that isn't "
           "recoverable, or isn't stable, isn't a phenotype, however good the story.")
