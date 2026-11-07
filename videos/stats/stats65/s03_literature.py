from __future__ import annotations

from videos.stats.stats65.common import *  # noqa: F403


class Literature(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter two. Reading the literature: what is known, and where the gap is.", 2,
                            r"Reading the literature", r"Theorem, \ conditions, \ evidence, \ gap")
        self.how()
        self.weighted()
        self.exch()
        self.beyond()
        self.tables()
        self.check()
        self.gap()

    def how(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> How to read a statistics paper. <bookmark mark='b'/> Find the main theorem and write it "
            "in your own notation; most of a paper's length is the setup for one statement. <bookmark mark='c'/> List its "
            "conditions, and ask of each: is it needed, and is it checkable in practice? <bookmark mark='d'/> Then read the "
            "simulations and the application as evidence about the conditions that the theorem could not cover, and look "
            "for the case nobody tried. That case is often the gap.",
            [(r"\text{the theorem}", r":", r"\text{one statement, \ your notation}", 40),
             (r"\text{the conditions}", r":", r"\text{needed? \ checkable?}", 40),
             (r"\text{the evidence}", r":", r"\text{simulations, \ data}", 40),
             (r"\text{the gap}", r":", r"\text{the case nobody tried}", 40)],
            [r"read for the claim", r"read for the assumptions", r"read for the support", r"read for what is missing"],
            colors=[(3, THESISC)])

    def weighted(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The founding paper. <bookmark mark='b'/> Tibshirani, Barber, Candes and Ramdas, 2019: if "
            "the test point's covariate comes from Q, and w is the exact ratio dQ over dP, then the weighted quantile of the "
            "calibration scores, with the test point's own weight placed at infinity, gives coverage at least one minus "
            "alpha. <bookmark mark='c'/> The proof rests on weighted exchangeability: the joint law of the calibration points "
            "and the test point is exchangeable after reweighting by w. <bookmark mark='d'/> Its condition, a known w, is "
            "rarely checkable, and their own experiments estimated it with a classifier, and found that coverage held "
            "approximately.",
            [(r"\text{theorem}", r":", r"w \text{ exact } \Rightarrow \text{coverage} \ge 1 - \alpha", 40),
             (r"\text{proof}", r":", r"\text{weighted exchangeability}", 40),
             (r"\text{condition}", r":", r"w = dQ/dP \ \text{known}", 40),
             (r"\text{their evidence}", r":", r"\text{estimated } \hat w \text{ works, \ roughly}", 40)],
            [r"Tibshirani et al. (2019)", r"the key idea", r"rarely true", r"the gap's first hint"],
            colors=[(2, NAIVEC)])

    def beyond(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What came after. <bookmark mark='b'/> Rina Foygel Barber, Emmanuel Candes, Aaditya Ramdas "
            "and Ryan Tibshirani's Conformal Prediction Beyond Exchangeability, in 2023, bounded the coverage gap of "
            "weighted methods under arbitrary departures by total variation distances between the data and its swapped "
            "versions. <bookmark mark='c'/> Lihua Lei and Emmanuel Candes, in 2021, used estimated propensity weights for "
            "counterfactual intervals, and showed coverage approaches one minus alpha as the weights' estimation error "
            "shrinks. <bookmark mark='d'/> So the general principle, loss controlled by a distance, is known. What a "
            "practitioner lacks is the bound in a usable form, and evidence of how tight it is.",
            [(r"\text{beyond exchangeability}", r":", r"\text{gap} \le \text{TV terms}", 40),
             (r"\text{counterfactuals}", r":", r"\hat w \to w \Rightarrow \text{coverage} \to 1 - \alpha", 40),
             (r"\text{known}", r":", r"\text{loss controlled by a distance}", 40),
             (r"\text{missing}", r":", r"\text{a usable form, \ and its tightness}", 40)],
            [r"Barber et al. (2023)", r"Lei \& Cand\`es (2021)", r"the principle", r"the gap"],
            colors=[(3, THESISC)])

    def gap(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The lesson's role is deliberately modest: a worked research exercise, rather than an established new literature contribution. <bookmark mark='b'/> Derive a clean robustness bound using one population distance, analytically computable in the specified simulation laws. It is not automatically observable or estimable in an arbitrary application. <bookmark mark='c'/> Give a short proof with its conditioning and independence assumptions, then compare calculations against independent references. <bookmark mark='d'/> Preserve the original protocol, identify the present correction as post hoc, and report how coverage, widths, infinite intervals and slack behave. The goal is a checkable account of an existing idea, without an unsupported priority claim.",
            [(r"\text{contribution}", r":", r"\text{modest, \ precise}", 40),
             (r"\text{a statement}", r":", r"\text{loss} \le \mathrm{TV}(P_{\hat w}, Q)", 40),
             (r"\text{a proof}", r":", r"\text{short, \ checkable}", 40),
             (r"\text{a measurement}", r":", r"\text{how loose, \ and when}", 40)],
            [r"most theses", r"chapter 3", r"chapter 4", r"chapters 5--6"],
            colors=[(1, THESISC)])

    def exch(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Reading the founding proof closely, because the new theorem will lean on it. <bookmark mark='b'/> Under covariate shift, the joint density of the n calibration pairs and the test pair is the product of n source densities and one target density. <bookmark mark='c'/> Write the target density as w times the source density, and the joint density becomes w of the test covariate times a symmetric function. So, given the set of all n plus one values, the probability that a particular one is the test point is proportional to its weight. <bookmark mark='d'/> The test score's rank among the n plus one is therefore a weighted draw, and weighted quantile at level one minus alpha yields at-least-nominal marginal coverage. Discreteness, ties and large test mass can make coverage conservative; it need not equal the nominal level.",
            [(r"\text{joint density}", r"=", r"\prod_{i \le n} p(z_i) \cdot q(z_{n+1})", 40),
             (r"q", r"=", r"w \, p \ \Rightarrow \ w(x_{n+1}) \prod_{i \le n+1} p(z_i)", 40),
             (r"P(\text{the test point is } z_j \mid \{z\})", r"\propto", r"w(x_j)", 40),
             (r"\text{so}", r":", r"\text{weighted quantile gives coverage at least }1-\alpha", 40)],
            [r"independence", r"weighted exchangeability", r"the key line", r"the proof, \ in one idea"],
            colors=[(2, HONC)])

    def tables(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> And reading the simulations. <bookmark mark='b'/> Ask what was varied, and what was held fixed: a study that varies only the sample size says nothing about the shift's size. <bookmark mark='c'/> Ask for Monte Carlo errors: a coverage of 89.6 percent from two hundred replicates cannot be told apart from ninety. <bookmark mark='d'/> And ask which settings are missing. The founding papers' simulations estimated the weights well; this lesson deliberately includes tempered and misspecified weights to illustrate degradation. We have not established that earlier literature omitted all such stress tests, so this is an educational design choice rather than a certified novel literature gap.",
            [(r"\text{varied}", r":", r"\text{and what was held fixed}", 40),
             (r"\text{MC error}", r":", r"200 \text{ reps}: \ \pm 2 \text{ points}", 40),
             (r"\text{missing}", r":", r"\text{badly estimated weights}", 40),
             (r"\text{so}", r":", r"\text{tempered and misspecified arms}", 40)],
            [r"design", r"Part 7", r"the gap", r"chapter 5"],
            colors=[(2, NAIVEC)])

    def check(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> One habit for reading, and later for writing, proofs. <bookmark mark='b'/> Check every "
            "claimed formula numerically on a special case before believing it. <bookmark mark='c'/> This dissertation's "
            "Gaussian total variation, two Phi of half the distance minus one, was checked against a numerical integral on a "
            "fine grid, and the two agree to within a hundred-millionth. <bookmark mark='d'/> A proof can have an error that a "
            "careful reader misses; agreement of independent calculations is useful evidence, but both can share an error; a numerical check is not a proof. The test suite keeps those checks, so they are "
            "run again every time the code changes.",
            [(r"\text{habit}", r":", r"\text{check formulas numerically}", 40),
             (r"\text{here}", r":", r"2\Phi(\delta/2) - 1 \ \text{vs a grid integral}", 40),
             (r"\text{agreement}", r":", r"\text{within } 10^{-8}", 40),
             (r"\text{kept}", r":", r"\text{in the test suite}", 40)],
            [r"trust, \ but verify", r"a special case", r"two routes", r"regression tests"],
            colors=[(2, HONC)])
