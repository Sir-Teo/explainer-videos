from __future__ import annotations

import numpy as np

from videos.stats.stats60.common import *  # noqa: F403


class LabelShift(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter six. Label shift: when the mix of outcomes changes, but each outcome looks the same.", 6,
                            r"Label shift", r"Counting through a confused classifier", lit=(2018,))
        self.definition()
        self.cc_bias()
        self.bbse()
        self.em()
        self.chart()
        self.board()
        self.recalibrate()

    def definition(self):
        d = load("labshift")
        self.lad_voiceover(
            f"<bookmark mark='a'/> The mirror image of covariate shift. A classifier for breast biopsies is trained at one "
            f"clinic, where {100 * d['p_train']:.0f} percent of biopsies are malignant. <bookmark mark='b'/> It is used at a "
            f"referral centre, where seventy percent are. <bookmark mark='c'/> A malignant biopsy looks the same at both: "
            f"the law of the features given the label is unchanged; only the label's distribution moved. <bookmark "
            f"mark='d'/> Two questions: what is the new prevalence, and how should the classifier's probabilities be "
            f"corrected? Neither needs a single label from the new site.",
            [(r"\text{train}", r":", rf"P(y = 1) = {d['p_train']:.2f}", 40),
             (r"\text{target}", r":", rf"Q(y = 1) = {d['q_true']:.2f}", 40),
             (r"\text{assumed}", r":", r"P(x \mid y) = Q(x \mid y)", 40),
             (r"\text{goals}", r":", r"Q(y), \ \text{and } Q(y \mid x), \ \text{from unlabelled } x", 40)],
            [r"Wisconsin biopsies", r"a referral centre", r"anticausal: \ $y$ causes $x$", r"no target labels"],
            colors=[(2, FIXC)])

    def cc_bias(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The naive answer, classify and count: the fraction of new biopsies the classifier calls "
            "malignant. <bookmark mark='b'/> Its expectation mixes the classifier's true positive rate and false positive "
            "rate, weighted by the true prevalence. <bookmark mark='c'/> Unless the classifier is perfect, that pulls the "
            "count toward the middle: a high prevalence is underestimated, a low one overestimated. <bookmark mark='d'/> "
            "George Forman's adjusted count, from 2005, inverts the relation, using the rates measured on held-out "
            "training data.",
            [(r"\hat q_{\text{CC}}", r"=", r"\tfrac1m\#\{\text{predicted malignant}\}", 40),
             (r"E[\hat q_{\text{CC}}]", r"=", r"q\,\mathrm{TPR} + (1 - q)\,\mathrm{FPR}", 40),
             (r"\text{so}", r":", r"\text{biased toward the middle}", 40),
             (r"\hat q_{\text{ACC}}", r"=", r"(\hat q_{\text{CC}} - \mathrm{FPR})/(\mathrm{TPR} - \mathrm{FPR})", 40)],
            [r"the obvious estimate", r"a mixture of rates", r"attenuation", r"Forman (2005)"],
            colors=[(2, NAIVEC), (3, FIXC)])

    def bbse(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Zachary Lipton, Yu-Xiang Wang and Alexander Smola generalized it in 2018, to any number of "
            "classes: black-box shift estimation. <bookmark mark='b'/> On held-out training data, estimate the joint matrix of "
            "predicted against true labels. <bookmark mark='c'/> On the target, estimate the distribution of predictions. "
            "Under label shift, the one is the other times the vector of weights, Q of y over P of y. <bookmark mark='d'/> "
            "Solve the linear system. The classifier can be anything, even a poor one, as long as the confusion matrix is "
            "invertible: its quality affects the variance, not the consistency.",
            [(r"\hat C_{ij}", r"=", r"\hat P(\hat y = i, \ y = j) \ \text{on held-out training data}", 38),
             (r"\hat\mu_i", r"=", r"\hat Q(\hat y = i) \ \text{on the target}", 40),
             (r"\mu", r"=", r"C\,w, \ \ w_j = Q(y = j)/P(y = j)", 40),
             (r"\hat w", r"=", r"\hat C^{-1}\hat\mu", 40)],
            [r"Lipton, \ Wang \& Smola (2018)", r"the confusion matrix", r"the moment equation", r"a black box suffices"],
            colors=[(3, FIXC)])

    def em(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> An older route uses the classifier's probabilities, not just its labels. Marco Saerens, "
            "Patrice Latinne and Christine Decaestecker, in 2002: <bookmark mark='b'/> given a guess of the new prevalence, "
            "correct each target point's probability by Bayes' rule, multiplying by the prior ratio and renormalizing. "
            "<bookmark mark='c'/> Then update the prevalence to the average corrected probability, and repeat. <bookmark "
            "mark='d'/> It is EM for the mixing weights of a mixture whose components are known, and it is more efficient "
            "than BBSE when the classifier's probabilities are calibrated; when they are not, it can be badly biased.",
            [(r"\text{E-step}", r":", r"\tilde p_i(y) \propto \frac{q(y)}{p(y)}\,\hat p(y \mid x_i)", 40),
             (r"\text{M-step}", r":", r"q(y) \leftarrow \tfrac1m\sum_i \tilde p_i(y)", 40),
             (r"\text{it is}", r":", r"\text{EM for the mixing weights}", 40),
             (r"\text{needs}", r":", r"\text{calibrated probabilities}", 40)],
            [r"Saerens, \ Latinne \& Decaestecker (2002)", r"average the corrections", r"Part 22's EM", r"Part 34's calibration"],
            colors=[(3, NAIVEC)])

    def chart(self):
        d = load("labshift")
        cc, bb, em = (np.asarray(d[k]) for k in ("cc", "bbse", "em"))
        A = axes([0.45, 0.95], [0, 12], x_length=7.4, y_length=4.4, xlabel=r"estimated malignant fraction at the new site", ylabel=r"density over repetitions",
                 xticks=[0.5, 0.6, 0.7, 0.8, 0.9], yticks=[0, 4, 8, 12], center=[-2.5, 0.2, 0])
        ax = A.ax
        xs = np.linspace(0.45, 0.95, 300)

        def kde(v, c):
            v = np.asarray(v, float)
            h = 0.012
            y = np.exp(-0.5 * ((xs[:, None] - v[None]) / h) ** 2).sum(1) / (len(v) * h * np.sqrt(2 * np.pi))
            return VGroup(shade(ax, xs, y, c, 0.18), curve(ax, xs, y, c, 3.5))
        h_cc, h_bb, h_em = kde(cc, NAIVEC), kde(bb, FIXC), kde(em, DEPTHC)
        tl = DashedLine(ax.c2p(d["q_true"], 0), ax.c2p(d["q_true"], 11.8), color=TGTC, stroke_width=2.5)
        side = side_groups([
            [(rf"{d['reps']} repetitions:", WHITE), (r"train 250, \ hold out 150, \ target 100", WHITE)],
            [(rf"gold: \ the true prevalence, \ {d['q_true']:.2f}", TGTC)],
            [(r"red: \ classify and count", NAIVEC), (rf"mean {d['cc_mean']:.3f}", NAIVEC)],
            [(r"green: \ BBSE", FIXC), (rf"mean {d['bbse_mean']:.3f}, \ sd {d['bbse_sd']:.3f}", FIXC)],
            [(r"purple: \ EM", DEPTHC), (rf"mean {d['em_mean']:.3f}, \ sd {d['em_sd']:.3f}", DEPTHC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The Wisconsin biopsies, {d['reps']} times over. Each time, a logistic classifier is trained "
            f"on two hundred and fifty biopsies, its confusion matrix estimated on a hundred and fifty more, and the target is "
            f"a hundred biopsies, seventy percent malignant. <bookmark mark='b'/> The true prevalence is the gold line. "
            f"<bookmark mark='c'/> Classify and count, in red, averages {say(d['cc_mean'], 3)}: biased down, as the formula said. "
            f"<bookmark mark='d'/> BBSE, in green, averages {say(d['bbse_mean'], 3)}: unbiased, with a wider spread. <bookmark "
            f"mark='e'/> EM, in purple, averages {say(d['em_mean'], 3)}, with the smallest spread: the logistic probabilities are "
            f"nearly calibrated here."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Wolberg, \ Street \& Mangasarian (1995); \ the shift is simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(tl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(h_cc), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(h_bb), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(h_em), FadeIn(side[4]), run_time=1.5)
        self.clear_scene()

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("classify-and-count", "BBSE"),
                   f"<bookmark mark='a'/> On the Board, with bootstrap intervals for the prevalence. Classify and count's interval "
                   f"contains the true seventy percent only {100 * br[2]['achieved']:.0f} percent of the time: broken, because its centre is wrong. "
                   f"<bookmark mark='b'/> BBSE covers {100 * br[3]['achieved']:.0f} percent: kept.", [("a", [0]), ("b", [1])])

    def recalibrate(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> With the weights in hand, the classifier is corrected by the same Bayes step: multiply "
            "its probabilities by the weight of each class and renormalize. <bookmark mark='b'/> For decisions, this moves "
            "the threshold: at seventy percent prevalence, a biopsy scored forty percent malignant by the clinic's "
            "classifier is, at the new site, about seventy-three percent likely to be malignant. <bookmark mark='c'/> The theory: BBSE's error "
            "shrinks like one over root m, the target size, times the condition number of the confusion matrix. <bookmark "
            "mark='d'/> Covariate shift or label shift? The causal direction decides: features caused by the label, as a "
            "tumour causes its cells' shape, suggest label shift.",
            [(r"Q(y \mid x)", r"\propto", r"\hat w(y)\,P(y \mid x)", 40),
             (r"\text{decisions}", r":", r"\text{the threshold moves}", 40),
             (r"\text{error}", r"\lesssim", r"\kappa(C)\,/\sqrt m", 40),
             (r"\text{which shift?}", r":", r"x \to y: \ \text{covariate}; \ \ y \to x: \ \text{label}", 40)],
            [r"Bayes, \ once more", r"$0.40 \to 0.73$", r"Lipton et al.'s bound", r'Sch\"olkopf et al. (2012)'],
            colors=[(0, FIXC)])
