from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403


class Programme(VoiceoverScene):
    def construct(self):
        card_section(self, 2, r"The programme", r"What is computational psychiatry trying to do?", marr=("how",))
        self.two()
        self.delivered()

    def two(self):
        chips_section(self, r"Two routes", [
            (r"theory-driven", r"a model of a mechanism (learning, \ inference, \ choice) fitted to a task; \ "
                               r"parameters as the place where a disorder lives (Huys, \ Maia and Frank, \ 2016)", MODEL),
            (r"data-driven", r"machine learning on many measurements to predict diagnosis, \ course or treatment "
                             r"response, \ with or without a mechanism", PERSON),
            (r"the bridge", r"fit mechanistic models, \ then use their parameters as features for prediction", GOOD),
            (r"the shared demand", r"both need measurements that are reliable in individuals, \ and predictions that "
                                   r"hold in new samples", AUTH),
        ], "What is computational psychiatry trying to do? <bookmark mark='a'/> The theory-driven route fits a model "
           "of a mechanism, learning, inference or choice, to a task, and treats the parameters as the place where a "
           "disorder lives. Quentin Huys, Tiago Maia and Michael Frank set it out in 2016. <bookmark mark='b'/> The "
           "data-driven route uses machine learning on many measurements to predict diagnosis, course or treatment "
           "response, with or without a mechanism. <bookmark mark='c'/> The bridge fits mechanistic models, then uses "
           "their parameters as features for prediction. <bookmark mark='d'/> Both routes need measurements that are "
           "reliable in individuals, and predictions that hold in new samples.",
           tag=published_tag(r"Huys, \ Maia \& Frank (2016)"))

    def delivered(self):
        rows_section(self, r"What it has delivered so far", [
            (r"robust group findings: \ altered learning from punishment in depression, \ reduced model-based "
             r"control along a compulsivity dimension, \ aberrant salience in psychosis", GOOD),
            (r"new tasks and models, \ and large online samples that make individual differences studiable", MODEL),
            (r"no validated clinical test yet: \ no parameter is used to diagnose or choose a treatment in routine "
             r"care", AUTH),
            (r"the reasons are this part's chapters: \ reliability, \ replication and generalization", YOU),
        ], "What has it delivered so far? <bookmark mark='a'/> Robust group findings: altered learning from punishment "
           "in depression, reduced model-based control along a compulsivity dimension, and aberrant salience in "
           "psychosis. <bookmark mark='b'/> New tasks and models, and large online samples that make individual "
           "differences possible to study. <bookmark mark='c'/> But no validated clinical test yet. No parameter is "
           "used to diagnose, or to choose a treatment, in routine care. <bookmark mark='d'/> The reasons are this "
           "part's chapters: reliability, replication and generalization.")
