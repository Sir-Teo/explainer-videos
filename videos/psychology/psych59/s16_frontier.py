from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card_section(self, 15, r"Frontier: \ a clinical-grade battery", r"What would a reliable computational "
                     r"assessment look like?", scale=("person", "society"))
        self.new()
        self.open()

    def new(self):
        chips_section(self, r"What is new", [
            (r"reliability first", r"tasks redesigned and selected for retest reliability, \ with trial-level "
                                   r"hierarchical models", MODEL),
            (r"many short sessions", r"games played at home over weeks, \ averaging out bad days", PERSON),
            (r"large cohorts", r"tens of thousands of online participants and population cohorts with tasks, \ "
                               r"symptoms and follow-up", GOOD),
            (r"registered validation", r"models frozen and tested in samples their builders never saw", SYMP),
        ], "What would a reliable computational assessment look like? <bookmark mark='a'/> Reliability first: tasks "
           "redesigned and selected for retest reliability, with trial-level hierarchical models. "
           "<bookmark mark='b'/> Many short sessions: games played at home over weeks, averaging out bad days. "
           "<bookmark mark='c'/> Large cohorts: tens of thousands of online participants, and population cohorts with "
           "tasks, symptoms and follow-up. <bookmark mark='d'/> And registered validation: models frozen and tested "
           "in samples their builders never saw.", chip_w=4.2, text_w=8.0)

    def open(self):
        chips_section(self, r"Open problems", [
            (r"mechanism or marker", r"is a parameter a cause of illness, \ or only a sign of it?", AUTH),
            (r"states and traits", r"parameters change with mood and sleep; \ which part is the person?", MODEL),
            (r"treatment by parameter", r"a trial that assigns treatment by a computational measure, \ and wins", GOOD),
            (r"lived experience", r"what patients count as getting better, \ built into the models", PERSON),
        ], "And the open problems. <bookmark mark='a'/> Mechanism or marker: is a parameter a cause of illness, or only "
           "a sign of it? <bookmark mark='b'/> States and traits: parameters change with mood and sleep, so which "
           "part is the person? <bookmark mark='c'/> Treatment by parameter: a trial that assigns treatment by a "
           "computational measure, and wins. <bookmark mark='d'/> And lived experience: what patients count as "
           "getting better, built into the models.")
