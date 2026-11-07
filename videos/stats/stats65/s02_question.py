from __future__ import annotations

import numpy as np

from videos.stats.stats65.common import *  # noqa: F403


class Question(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter one. Choosing a question.", 1, r"Choosing a question", r"Important, \ open, \ and small enough")
        self.criteria()
        self.finding()
        self.candidates()
        self.chosen()
        self.why()
        self.scope()
        self.answer()

    def criteria(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A good dissertation question has four properties. <bookmark mark='b'/> It matters: "
            "someone's decisions depend on the answer. <bookmark mark='c'/> It is open: the literature does not already "
            "settle it, which takes reading to establish. <bookmark mark='d'/> And it is small enough to answer in the time "
            "available, with a precise statement that could turn out false. Most first questions are too large; the craft "
            "is in cutting them down without cutting out what made them matter.",
            [(r"\text{matters}", r":", r"\text{a decision depends on it}", 40),
             (r"\text{open}", r":", r"\text{not settled, \ by reading}", 40),
             (r"\text{small enough}", r":", r"\text{answerable in the time}", 40),
             (r"\text{falsifiable}", r":", r"\text{a statement that could be wrong}", 40)],
            [r"importance", r"novelty", r"feasibility", r"precision"],
            colors=[(3, THESISC)])

    def candidates(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Candidates from the last ten parts' open problems. <bookmark mark='b'/> Valid inference "
            "with learned adjustment sets, from Part sixty-two: important, but large. <bookmark mark='c'/> Private inference "
            "beyond the mean, from Part sixty-three: important, and a field of its own. <bookmark mark='d'/> Conditional "
            "guarantees for generation, from Part sixty-four: impossible in general, as Part fifty-seven proved. <bookmark "
            "mark='e'/> And coverage of weighted conformal prediction when the weights are estimated, from Parts "
            "fifty-seven and sixty: important for every deployed model whose population drifts, and small enough to make "
            "progress on.",
            [(r"candidates:", GREY_A),
             (r"learned adjustment sets \ (Part 62): \ important, \ large", GREY_A),
             (r"private inference beyond the mean \ (Part 63): \ a field", GREY_A),
             (r"conditional guarantees \ (Part 64): \ impossible in general", GREY_A),
             (r"weighted conformal with estimated weights \ (Parts 57, 60): \ chosen", THESISC)])

    def chosen(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The setting, from Part fifty-seven. <bookmark mark='b'/> Calibration data come from a source distribution P, and the test point from a target Q with the same conditional law of Y given X, but different covariates: covariate shift. <bookmark mark='c'/> Ryan Tibshirani, Rina Foygel Barber, Emmanuel Candes and Aaditya Ramdas showed in 2019 that weighting each calibration score by the likelihood ratio w of x restores the guarantee: coverage at least one minus alpha under Q. <bookmark mark='d'/> But w is the density of Q over the density of P, which nobody knows. It is estimated, usually with Part sixty's classifier trick, and the oracle theorem no longer applies automatically. Existing robustness results analyze estimated weights; this lesson derives one simple bound rather than establishing a new unsolved field.",
            [(r"\text{covariate shift}", r":", r"P_X \ne Q_X, \ \ P_{Y \mid X} = Q_{Y \mid X}", 40),
             (r"\text{weights}", r":", r"w(x) = dQ_X / dP_X", 40),
             (r"\text{known } w", r"\Rightarrow", r"Q(Y \in \hat C(X)) \ge 1 - \alpha", 40),
             (r"\text{estimated } \hat w", r"\Rightarrow", r"?", 40)],
            [r"Part 57", r"the likelihood ratio", r"Tibshirani et al. (2019)", r"the question"],
            colors=[(3, THESISC)])

    def why(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Why it matters. <bookmark mark='b'/> A model trained on one hospital's patients and "
            "deployed at another, a survey's volunteers standing in for a population, a benchmark's questions for a user's: "
            "each can involve covariate shift, but equal conditional outcome laws must be justified rather than assumed from different populations alone, and each uses estimated weights if it corrects at all. <bookmark mark='c'/> A "
            "practitioner needs to know whether the promised ninety percent is still about ninety, or sixty. <bookmark "
            "mark='d'/> The question, stated so it can be answered: by how much can coverage fall, as a function of how wrong "
            "the weights are?",
            [(r"\text{hospitals}", r":", r"\text{trained here, \ used there}", 40),
             (r"\text{surveys}", r":", r"\text{volunteers for a population}", 40),
             (r"\text{the need}", r":", r"\text{is 90\% still about 90\%?}", 40),
             (r"\text{the question}", r":", r"\text{coverage loss vs weight error}", 40)],
            [r"Part 60", r"Part 18", r"a decision", r"precise"],
            colors=[(3, THESISC)])

    def scope(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Cutting the question to size. <bookmark mark='b'/> Split conformal only, not full conformal or jackknife+, because its calibration set is cleanly separate. <bookmark mark='c'/> Covariate shift only, with the conditional law of Y given X unchanged, because that is the setting where weights are the right fix. <bookmark mark='d'/> Weights estimated on data independent of the calibration set, because that is the case a clean proof can reach; same-sample estimation and cross-fitting need additional analysis outside this proof. That does not mean all such cases are globally unsolved in the literature.",
            [(r"\text{method}", r":", r"\text{split conformal only}", 40),
             (r"\text{shift}", r":", r"\text{covariate shift only}", 40),
             (r"\text{weights}", r":", r"\text{estimated on independent data}", 40),
             (r"\text{left open}", r":", r"\text{the same data for both}", 40)],
            [r"a clean separation", r"Part 60's setting", r"a provable case", r"stated, \ not hidden"],
            colors=[(3, NAIVEC)])

    def answer(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What would count as an answer? Decide before starting. <bookmark mark='b'/> A bound on "
            "the coverage loss in terms of something a user can estimate, or at least reason about. <bookmark mark='c'/> "
            "Evidence of whether the bound is useful in practice, or only true. <bookmark mark='d'/> And one real dataset "
            "where the truth is known, so the method's behaviour can be seen rather than assumed. Each of the next five "
            "chapters delivers one of these.",
            [(r"\text{a bound}", r":", r"\text{loss in usable terms}", 40),
             (r"\text{evidence}", r":", r"\text{useful, \ or only true?}", 40),
             (r"\text{real data}", r":", r"\text{truth known by design}", 40),
             (r"\text{deliverables}", r":", r"\text{chapters 3--7}", 40)],
            [r"theory", r"simulation", r"application", r"the plan"],
            colors=[(0, THESISC)])

    def finding(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Where do questions come from, in practice? <bookmark mark='b'/> From the open problems "
            "at the end of good papers, and of the last ten parts, which are lists other researchers left on purpose. "
            "<bookmark mark='c'/> From applied work: an analyst who used a method, saw something odd, and asked why. Many of "
            "the Board's broken rows began that way, as a practitioner's surprise. <bookmark mark='d'/> And from talking: a "
            "supervisor, a seminar, a colleague in another field whose data break your assumptions. A question that someone "
            "outside statistics needs answered is usually a good one.",
            [(r"\text{papers}", r":", r"\text{their open problems}", 40),
             (r"\text{practice}", r":", r"\text{a surprise, \ explained}", 40),
             (r"\text{people}", r":", r"\text{supervisors, \ seminars, \ other fields}", 40),
             (r"\text{a good sign}", r":", r"\text{someone outside needs it}", 40)],
            [r"left on purpose", r"the Board's origins", r"conversation", r"importance"],
            colors=[(3, THESISC)])
