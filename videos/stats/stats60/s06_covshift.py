from __future__ import annotations

import numpy as np

from videos.stats.stats60.common import *  # noqa: F403


def normal_pdf(x, m, s):
    return np.exp(-0.5 * ((x - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))


class CovariateShift(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter five. Covariate shift: when the people change, but the relationship does not.", 5,
                            r"Covariate shift", r"Reweight the sample to the target", lit=(2000,))
        self.definition()
        self.identity()
        self.classifier()
        self.ages()
        self.sampling()
        self.price()
        self.board()
        self.variants()

    def definition(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Covariate shift, named by Hidetoshi Shimodaira in 2000: the training data come from a "
            "distribution P over covariates x and outcomes y, the target from Q. <bookmark mark='b'/> The covariates' "
            "distribution changes, from p of x to q of x. <bookmark mark='c'/> But the conditional law of y given x is the "
            "same in both. <bookmark mark='d'/> In a survey, the panel over-represents the young, but a forty-year-old's blood "
            "pressure has the same distribution whether or not they joined the panel. That is the assumption, and it is "
            "Part forty-one's missing at random, under another name.",
            [(r"\text{train}", r"\sim", r"P = p(x)\,P(y \mid x)", 40),
             (r"\text{target}", r"\sim", r"Q = q(x)\,P(y \mid x)", 40),
             (r"\text{assumed}", r":", r"P(y \mid x) \ \text{the same}", 40),
             (r"\text{equivalently}", r":", r"\text{selection depends on } x \text{ only}", 40)],
            [r"Shimodaira (2000)", r"the covariates move", r"the mechanism stays", r"Part 41's MAR"],
            colors=[(2, FIXC)])

    def identity(self):
        heading = label("Importance weighting and overlap under covariate shift", font_size=34).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            "<bookmark mark='a'/> The importance weight is the ratio of the two covariate densities, q over p. <bookmark "
            "mark='b'/> Any expectation under the target is an expectation under the training distribution, reweighted: "
            "<bookmark mark='c'/> the weighted average of the training outcomes estimates the target mean, the same "
            "Horvitz–Thompson idea as Part eighteen's surveys. <bookmark mark='d'/> It needs the weights to exist: wherever q "
            "puts mass, p must too. If the panel has no one over seventy, no reweighting can bring them back.",
            [(r"w(x)", r"=", r"q(x)/p(x)", 40),
             (r"E_Q[f(X, Y)]", r"=", r"E_P[w(X) f(X, Y)]", 40),
             (r"\hat\mu_w", r"=", r"\textstyle\sum_i w_i y_i \big/ \sum_i w_i", 40),
             (r"\text{needs}", r":", r"q(x) > 0 \Rightarrow p(x) > 0", 40)],
            [r"the density ratio", r"change of measure", r"Part 18's H\'ajek form", r"overlap, \ or support"],
            colors=[(1, FIXC), (3, NAIVEC)])

    def classifier(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The densities are unknown, and estimating each in many dimensions is hard. The ratio is "
            "easier. <bookmark mark='b'/> Pool the training sample with an unlabelled sample from the target, and fit a "
            "classifier for which one each point came from. <bookmark mark='c'/> By Bayes' rule, the classifier's odds are "
            "the density ratio, up to the ratio of the two sample sizes. <bookmark mark='d'/> Here a logistic regression on "
            "age, age squared, sex and body-mass index, against two thousand unlabelled NHANES adults: the outcomes of the "
            "target are never needed.",
            [(r"\text{pool}", r":", r"\text{training points } (C = 0), \ \text{target points } (C = 1)", 38),
             (r"\text{classify}", r":", r"c(x) = P(C = 1 \mid x)", 40),
             (r"w(x)", r"=", r"\frac{n_0}{n_1}\cdot\frac{c(x)}{1 - c(x)}", 40),
             (r"\text{here}", r":", r"\text{logistic on age, \ age}^2, \ \text{sex, \ BMI}", 40)],
            [r"a probabilistic classifier", r"the propensity of membership", r"Bayes' rule", r"no target outcomes needed"],
            colors=[(2, FIXC)])

    def ages(self):
        d = load("covshift")
        a_s, a_p = np.asarray(d["age_sample"]), np.asarray(d["age_pop"])
        edges = np.arange(18, 86, 4)
        hs = np.histogram(a_s, edges)[0] / len(a_s)
        hp = np.histogram(a_p, edges)[0] / len(a_p)
        top = float(max(hs.max(), hp.max())) * 1.15
        A = axes([18, 82], [0, top], x_length=7.4, y_length=4.4, xlabel=r"age (years)", ylabel=r"fraction",
                 xticks=[20, 30, 40, 50, 60, 70, 80], yticks=[0, 0.05, 0.1, 0.15], center=[-2.5, 0.2, 0])
        ax = A.ax
        b1 = hist_bars(ax, edges, hp, color=TGTC, opacity=0.35)
        b2 = hist_bars(ax, edges, hs, color=SRCC, opacity=0.55)
        side = side_groups([
            [(r"gold: \ the empirical extract", TGTC), (rf"$N = {d['N']:,}$ adults", TGTC)],
            [(rf"blue: \ a sample of {d['n']}", SRCC), (r"drawn $\propto e^{-(\mathrm{age} - 18)/20}$", SRCC)],
            [(rf"mean age \ {d['mean_age_sample']:.0f} \ vs \ {d['mean_age_pop']:.0f}", GREY_A)],
            [(r"few over 70 in the sample:", NAIVEC), (r"their weights will be large", NAIVEC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The two age distributions. In gold, the empirical extract: {d['N']:,} NHANES adults, from eighteen "
            f"to eighty. <bookmark mark='b'/> In blue, one sample of {d['n']}, drawn with selection probability falling "
            f"exponentially with age, as an online panel might be. <bookmark mark='c'/> The sample's mean age is "
            f"{d['mean_age_sample']:.0f}, the empirical extract's {d['mean_age_pop']:.0f}. <bookmark mark='d'/> There are few people over "
            f"seventy in the sample, but they exist: their weights will be large, and that is where the price is paid."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"NHANES; \ the selection is simulated")))
            vo.wait_until("a")
            self.play(FadeIn(b1, lag_ratio=0.05), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(b2, lag_ratio=0.05), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def sampling(self):
        d = load("covshift")
        t = d["truth"]
        xs = np.linspace(115, 131, 400)
        yu = normal_pdf(xs, d["mean_u"], d["sd_u"])
        yw = normal_pdf(xs, d["mean_w"], d["sd_w"])
        A = axes([115, 131], [0, 0.7], x_length=7.4, y_length=4.4, xlabel=r"estimated mean systolic pressure (mm Hg)", ylabel=r"density",
                 xticks=[116, 120, 124, 128], yticks=[0, 0.2, 0.4, 0.6], center=[-2.5, 0.2, 0])
        ax = A.ax
        cu = curve(ax, xs, yu, NAIVEC, 3.5)
        cw = curve(ax, xs, yw, FIXC, 3.5)
        tl = DashedLine(ax.c2p(t, 0), ax.c2p(t, 0.68), color=TGTC, stroke_width=2.5)
        side = side_groups([
            [(rf"gold: \ the empirical extract mean, \ {t:.2f}", TGTC)],
            [(r"red: \ unweighted means, Gaussian fit", NAIVEC), (rf"mean {d['mean_u']:.2f}, \ sd {d['sd_u']:.2f}", NAIVEC)],
            [(rf"95\% interval covers {100 * d['cov_u']:.0f}\%", NAIVEC)],
            [(r"green: \ weighted means, Gaussian fit", FIXC), (rf"mean {d['mean_w']:.2f}, \ sd {d['sd_w']:.2f}", FIXC)],
            [(rf"95\% interval covers {100 * d['cov_w']:.1f}\%", FIXC)],
        ])
        with self.voiceover(
            "<bookmark mark='a'/> We independently resample four hundred source datasets and unlabelled reference datasets from a fixed unweighted NHANES extract. The target is its empirical mean, not a survey-weighted national estimand. <bookmark mark='b'/> The red curve is a Gaussian fit to the simulated unweighted means, which are biased toward younger adults' pressures. <bookmark mark='c'/> Their nominal ninety-five percent intervals cover the extract mean in none of these four hundred runs. <bookmark mark='d'/> The green curve is a Gaussian fit to the importance-weighted means. Source sampling is with replacement and its true log density ratio is linear in age. <bookmark mark='e'/> The displayed coverage uses a joint sandwich standard error that includes fitting the logistic ratio and sampling the unlabelled target reference. It is asymptotic and model-dependent; empirical coverage has Monte Carlo uncertainty."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"NHANES; \ 400 simulated selections")))
            vo.wait_until("a")
            self.play(Create(tl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cu), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cw), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def price(self):
        d = load("covshift")
        self.lad_voiceover(
            "<bookmark mark='a'/> Kish's effective sample size is the squared sum of weights divided by their squared sum. It diagnoses weight concentration. <bookmark mark='b'/> The displayed average is smaller than the source sample size. <bookmark mark='c'/> It is not an exact information count for this estimator: outcome heterogeneity, dependence of outcomes on weights, and estimation of the ratio also affect variance. The empirical spreads are shown separately. <bookmark mark='d'/> Weak overlap may make the second moment of the weights enormous or infinite, undermining usual variance and normal approximations.",
            [(r"n_{\text{eff}}", r"=", r"\big(\textstyle\sum w_i\big)^2 \big/ \textstyle\sum w_i^2", 40),
             (r"\text{here}", r":", rf"n_{{\text{{eff}}}} \approx {d['ess']:.0f} \ \text{{of}} \ {d['n']}", 40),
             (r"\text{sd}", r":", rf"{d['sd_u']:.2f} \to {d['sd_w']:.2f}", 40),
             (r"\text{weak overlap}", r":", r"E_P[w^2] = \infty \text{ possible}", 40)],
            [r"Kish (1965)", r"a weight-concentration diagnostic", r"outcome variation and ratio fitting also matter", r"the real limit"],
            colors=[(1, FIXC), (3, NAIVEC)])

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("shifted sample", "importance-weighted"),
                   f"<bookmark mark='a'/> On the Board: the unweighted interval covers {100 * br[0]['achieved']:.0f} percent of the "
                   f"time, broken. <bookmark mark='b'/> The importance-weighted interval, with estimated weights, covers "
                   f"{100 * br[1]['achieved']:.1f} percent: kept, at the price of a wider interval.", [("a", [0]), ("b", [1])])

    def variants(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Clipping weights trades bias for variance. <bookmark mark='b'/> Kernel mean matching and KLIEP estimate the ratio through other criteria. <bookmark mark='c'/> A doubly robust target-mean estimator averages an outcome regression on target covariates and adds a weighted source residual correction. Consistency can survive one correctly estimated nuisance; confidence intervals additionally require overlap and suitable error rates. <bookmark mark='d'/> Weighted conformal is exactly valid under its known-ratio and exchangeability conditions. Estimated ratios need a compatible fitting or splitting scheme and an explicit approximation-error bound.",
            [(r"\text{clipping}", r":", r"\min(w, c): \ \text{bias for variance}", 40),
             (r"\text{direct ratio}", r":", r"\text{kernel mean matching; \ KLIEP}", 40),
             (r"\text{doubly robust}", r":", r"\text{weights or outcome model}", 40),
             (r"\text{prediction sets}", r":", r"\text{weighted conformal}", 40)],
            [r"a standard trick", r"Huang et al.; \ Sugiyama et al.", r"Part 41's AIPW", r"Part 57"],
            colors=[(2, FIXC)])
