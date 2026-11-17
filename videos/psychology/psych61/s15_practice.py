from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card_section(self, 14, r"In practice: \ commissioning research that holds up", r"You are paying for a "
                     r"study. \ What do you ask for?", scale=("society",))
        self.where()
        self.contract()

    def where(self):
        chips_section(self, r"Where this is a job", [
            (r"research operations", r"running studies at scale in companies: \ panels, \ quality checks, \ "
                                     r"registries of what was run", MODEL),
            (r"experimentation platforms", r"thousands of online experiments a year, \ with guardrails against "
                                           r"peeking and forking paths", PERSON),
            (r"forecasting", r"tournaments and markets that score predictions about which findings will hold "
                             r"(Part 50)", GOOD),
            (r"funders and editors", r"designing incentives: \ registered reports, \ data policies, \ replication "
                                     r"grants", SYMP),
        ], "Where is this a job? <bookmark mark='a'/> In research operations: running studies at scale in companies, "
           "with panels, quality checks, and registries of what was run. <bookmark mark='b'/> On experimentation "
           "platforms, which run thousands of online experiments a year, with guardrails against peeking and "
           "forking paths. <bookmark mark='c'/> In forecasting: tournaments and markets that score predictions about "
           "which findings will hold, as in Part 50. <bookmark mark='d'/> And among funders and editors, who design "
           "the incentives: registered reports, data policies and replication grants.")

    def contract(self):
        rows_section(self, r"A commissioning checklist", [
            (r"the decision the study will inform, \ and the smallest effect that would change it", WHITE),
            (r"a registered plan: \ hypotheses, \ sample size from power, \ primary outcome, \ analysis code", MODEL),
            (r"payment for the study, \ not for the result: \ the registered-report rule", GOOD),
            (r"the sample described: \ who, \ where, \ how recruited, \ in what language", PERSON),
            (r"data and code delivered, \ and a replication budgeted if the decision is large", YOU),
        ], "You're paying for a study. What do you ask for? <bookmark mark='a'/> The decision the study will inform, "
           "and the smallest effect that would change it. <bookmark mark='b'/> A registered plan: the hypotheses, a "
           "sample size from a power analysis, the primary outcome, and the analysis code. <bookmark mark='c'/> "
           "Payment for the study, not for the result. That's the registered-report rule. <bookmark mark='d'/> The "
           "sample described: who, where, how they were recruited, and in what language. <bookmark mark='e'/> And "
           "data and code delivered, with a replication budgeted if the decision is large.")
