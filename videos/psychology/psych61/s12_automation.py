from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403


class Automation(VoiceoverScene):
    def construct(self):
        card_section(self, 11, r"Automating research", r"What can machines do in a lab, \ and what must stay human?")
        self.uses()
        self.checks()
        self.human()

    def uses(self):
        chips_section(self, r"Machines in the research process", [
            (r"assistants", r"searching and summarizing literature, \ writing analysis code, \ checking it", MODEL),
            (r"simulated participants", r"piloting materials and predicting results before a study; \ Part 60's "
                                        r"silicon samples, \ with their limits", PERSON),
            (r"reviewers", r"checking statistics and reporting (as automated checkers of p-values already do)", GOOD),
            (r"the risk", r"fluent errors, \ invented references, \ and a literature that converges on what models "
                          r"already say", AUTH),
        ], "What can machines do in a lab? <bookmark mark='a'/> As assistants: searching and summarizing the "
           "literature, writing analysis code, and checking it. <bookmark mark='b'/> As simulated participants: "
           "piloting materials and predicting results before a study, with Part 60's limits on silicon samples. "
           "<bookmark mark='c'/> As reviewers: checking statistics and reporting, as automated checkers of p-values "
           "already do. <bookmark mark='d'/> And the risk: fluent errors, invented references, and a literature that "
           "converges on what models already say.")

    def human(self):
        rows_section(self, r"What must stay human", [
            (r"choosing the question: \ what is worth knowing, \ and for whom", WHITE),
            (r"responsibility: \ a named person answers for every claim and every number", MODEL),
            (r"contact with people: \ consent, \ care, \ and the participants' own view of the study", PERSON),
            (r"judgment of evidence: \ the Ledger's statuses are decisions, \ with reasons", GOOD),
        ], "So what must stay human? <bookmark mark='a'/> Choosing the question: what's worth knowing, and for whom. "
           "<bookmark mark='b'/> Responsibility: a named person answers for every claim and every number. "
           "<bookmark mark='c'/> Contact with people: consent, care, and the participants' own view of the study. "
           "<bookmark mark='d'/> And judgment of evidence: the Ledger's statuses are decisions, with reasons.")

    def checks(self):
        rows_section(self, r"Checks a machine can run on every paper", [
            (r"computational reproducibility: \ rerun the authors' code on their data and compare every number in "
             r"the paper; \ audits of journals with data policies have found many papers that cannot be reproduced "
             r"this way", WHITE),
            (r"consistency: \ statcheck, \ GRIM and SPRITE from Part 50, \ run at submission", MODEL),
            (r"preregistration as code (Part 43): \ the analysis that was registered is the analysis that runs, \ "
             r"and any deviation is printed", GOOD),
            (r"what none of them checks: \ whether the measure was valid, \ the sample apt, \ or the question worth "
             r"asking", AUTH),
        ], "Some checks a machine can run on every paper. <bookmark mark='a'/> Computational reproducibility: rerun "
           "the authors' code on their data, and compare every number in the paper. Audits of journals with data "
           "policies have found many papers that can't be reproduced this way. <bookmark mark='b'/> Consistency: "
           "statcheck, GRIM and SPRITE from Part 50, run at submission. <bookmark mark='c'/> Preregistration as "
           "code, as in Part 43: the analysis that was registered is the analysis that runs, and any deviation is "
           "printed. <bookmark mark='d'/> And what none of them checks: whether the measure was valid, the sample "
           "apt, or the question worth asking.")
