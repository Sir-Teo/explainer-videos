from __future__ import annotations

from videos.stats.stats65.common import *  # noqa: F403


class Writing(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter seven. Writing it up, and what referees will check.", 7, r"Writing and review",
                            r"A result others can check")
        self.structure()
        self.abstract()
        self.figures()
        self.referees()
        self.report()
        self.repro()
        self.honesty()

    def structure(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A statistics paper has a conventional shape, because readers search it in a conventional "
            "way. <bookmark mark='b'/> The introduction states the question, why it matters, and the contribution, in that "
            "order, on the first page. <bookmark mark='c'/> The method and theory sections state assumptions before "
            "results, and put long proofs in an appendix. <bookmark mark='d'/> The simulations and the application are "
            "evidence, organized by what each one tests; the discussion says what was not shown.",
            [(r"\text{introduction}", r":", r"\text{question, \ importance, \ contribution}", 40),
             (r"\text{theory}", r":", r"\text{assumptions, \ then results}", 40),
             (r"\text{evidence}", r":", r"\text{simulations, \ application}", 40),
             (r"\text{discussion}", r":", r"\text{limits, \ open questions}", 40)],
            [r"page one", r"proofs in the appendix", r"organized by aim", r"what was not shown"],
            colors=[(0, THESISC)])

    def abstract(self):
        self.list_voiceover(
            "<bookmark mark='a'/> The abstract, in four sentences. <bookmark mark='b'/> Weighted conformal prediction "
            "guarantees coverage under covariate shift when the likelihood ratio is known, but in practice the ratio is "
            "estimated. <bookmark mark='c'/> We show that with weights fixed in advance, coverage falls by at most the total "
            "variation distance between the reweighted source and the target. <bookmark mark='d'/> In a preregistered "
            "simulation the bound held in all forty-five cells, but left at least ten points of slack, most when the scores "
            "depended weakly on the covariates; and estimated weights over-covered at large shifts, through infinite "
            "intervals. "
            "<bookmark mark='e'/> On NHANES data with a designed selection, estimated weights restored ninety-one percent "
            "coverage where unweighted intervals gave seventy-three.",
            [(r"Abstract", S.ACCENT),
             (r"weighted conformal needs the true ratio; \ in practice it is estimated", GREY_A),
             (r"with fixed weights, \ coverage falls by at most $\mathrm{TV}(P_{\hat w}, Q)$", THESISC),
             (r"a preregistered study: \ the bound held in 45 of 45 cells, \ with wide slack", HONC),
             (r"NHANES: \ estimated weights 91\%, \ unweighted 73\%", ESTC)],
            buff=0.4, font_size=25, head_size=36)

    def referees(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What referees check. <bookmark mark='b'/> Is the theorem new, and is it correct? A "
            "referee will notice the relation to Barber and colleagues, so say it first. <bookmark mark='c'/> Are the "
            "assumptions necessary, and are the simulations designed to break them, or only to flatter the method? The "
            "tempered and misspecified arms are there for that. <bookmark mark='d'/> Could the results be reproduced from what "
            "is published? Every number in this part is computed by a seeded script, cached, and tested.",
            [(r"\text{new and correct?}", r":", r"\text{cite the closest work first}", 40),
             (r"\text{assumptions}", r":", r"\text{necessary? \ stress-tested?}", 40),
             (r"\text{simulations}", r":", r"\text{designed to break it}", 40),
             (r"\text{reproducible?}", r":", r"\text{seeded, \ cached, \ tested}", 40)],
            [r"novelty", r"rigour", r"the adversarial arms", r"this repository"],
            colors=[(3, HONC)])

    def repro(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Reproducibility, concretely. <bookmark mark='b'/> The code that produced every number is "
            "versioned, and every random seed is fixed, so the study reruns to the same digits. <bookmark mark='c'/> The "
            "functions are tested against known answers, such as the theorem's exact Gaussian formula against a numerical "
            "integral. <bookmark mark='d'/> And the protocol was committed before the results, so a reader can check that "
            "the predictions were not written after the fact. The same discipline has run through all sixty-five parts: "
            "every Coverage Board row was computed, not asserted.",
            [(r"\text{code}", r":", r"\text{versioned}", 40),
             (r"\text{seeds}", r":", r"\text{fixed: \ same digits on rerun}", 40),
             (r"\text{tests}", r":", r"\text{against known answers}", 40),
             (r"\text{protocol}", r":", r"\text{committed before the results}", 40)],
            [r"git", r"Part 7", r"the test suite", r"preregistration"],
            colors=[(3, HONC)])

    def honesty(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> And the hardest part. <bookmark mark='b'/> Report the predictions that failed alongside "
            "those that held. <bookmark mark='c'/> Do not quietly change the protocol, the threshold or the comparison after "
            "seeing the data; Part fifty-six's forking paths apply to the researcher too. <bookmark mark='d'/> A dissertation "
            "whose results are all exactly as hoped deserves suspicion. One that says where its method fails is more useful, "
            "and more likely to be true.",
            [(r"\text{report}", r":", r"\text{failed predictions too}", 40),
             (r"\text{do not}", r":", r"\text{change the protocol after the data}", 40),
             (r"\text{forking paths}", r":", r"\text{apply to the researcher}", 40),
             (r"\text{trust}", r":", r"\text{results that show their limits}", 40)],
            [r"chapter 5's scorecard", r"preregistration", r"Part 56", r"Part 33's lesson"],
            colors=[(0, HONC), (1, NAIVEC)])

    def report(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A referee's report, as this dissertation might receive one. <bookmark mark='b'/> One: "
            "the theorem is close to Barber and colleagues' results; state the precise difference. Response: it is a "
            "special case with a single computable distance; the paper now says so in the introduction. <bookmark "
            "mark='c'/> Two: the bound is loose; is it useful? Response: the study measures exactly how loose, and when, and "
            "the discussion proposes a score-aware sharpening. <bookmark mark='d'/> Three: the application's classifier was "
            "correctly specified by construction. Response: agreed; the misspecified arm of the simulation shows the other "
            "case, and the limitation is stated.",
            [(r"\text{referee 1}", r":", r"\text{relation to prior work}", 40),
             (r"\text{referee 2}", r":", r"\text{the bound is loose}", 40),
             (r"\text{referee 3}", r":", r"\text{an easy application}", 40),
             (r"\text{responses}", r":", r"\text{agree, \ measure, \ state limits}", 40)],
            [r"credit", r"tightness, \ measured", r"a fair point", r"revise, \ do not argue"],
            colors=[(3, HONC)])

    def figures(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The paper's figures, chosen so each makes one point. <bookmark mark='b'/> Figure one: the "
            "bound against the temper, for three shifts: what the theorem promises. <bookmark mark='c'/> Figure two: coverage "
            "by method and shift, with each method's bound dashed beneath it: the theorem holds. Figure three: the slack "
            "against gamma: when it is tight. <bookmark mark='d'/> Figure four: NHANES coverage for the young and the old: "
            "what it means for real people. Four figures, each with its message as its caption, and every number in them "
            "traceable to a seeded line of code.",
            [(r"\text{figure 1}", r":", r"\text{the promise}", 40),
             (r"\text{figure 2}", r":", r"\text{it holds}", 40),
             (r"\text{figure 3}", r":", r"\text{when it is tight}", 40),
             (r"\text{figure 4}", r":", r"\text{real people}", 40)],
            [r"chapter 3", r"chapter 5", r"chapter 5", r"chapter 6"],
            colors=[(1, HONC)])
