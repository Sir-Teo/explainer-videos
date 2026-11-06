from __future__ import annotations

import numpy as np

from videos.stats.stats41.common import *  # noqa: F403


class Measurement(VoiceoverScene):
    def construct(self):
        self.card()
        self.spearman()
        self.attenuation()
        self.picture()
        self.nhanes()
        self.rc()
        self.simex_idea()
        self.simex_plot()
        self.instruments()
        self.deming()
        self.seeded()
        self.other()
        self.board()

    def card(self):
        card = chapter_card(8, r"Measurement error", r"Values we see, \ but wrongly", lit=(1904, 1994), part=PART)
        with self.voiceover("Chapter eight. Measurement error."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def spearman(self):
        rows = [
            cmath(r"W", r"=", r"X + U, \ \ U \perp X, \ \ E\,U = 0", font_size=32),
            cmath(r"\text{reliability}", r":", r"\lambda = \sigma_X^2 / (\sigma_X^2 + \sigma_U^2)", font_size=32),
            cmath(r"\text{corr}(W_1, W_2)", r"=", r"\lambda \ \ \text{for two replicates}", font_size=32),
            cmath(r"r_{XY}", r"=", r"r_{WY} / \sqrt{\lambda}: \ \text{Spearman's correction}", font_size=32),
        ]
        rows[3][-1].set_color(TAUC)
        whys = [why(r"classical error"), why(r"the signal's share"), why(r"measure twice"), why(r"Spearman (1904)")]
        with self.voiceover(
            "<bookmark mark='a'/> The classical model of measurement error: what we record is the truth plus independent "
            "noise. <bookmark mark='b'/> The reliability is the share of the recorded variance that is signal. <bookmark "
            "mark='c'/> Measure the same thing twice, with independent errors, and the correlation between the two "
            "measurements is the reliability. <bookmark mark='d'/> Charles Spearman, in 1904, used this to correct "
            "correlations between mental test scores: divide by the square root of the reliability, the correction for "
            "attenuation."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def attenuation(self):
        rows = [
            cmath(r"Y", r"=", r"\alpha + \beta X + \varepsilon", font_size=32),
            cmath(r"\hat\beta_{\text{naive}}", r"\to", r"\dfrac{\text{Cov}(W, Y)}{\text{Var}\, W} = \lambda \beta", font_size=32),
            cmath(r"\text{with covariates } Z", r":", r"\lambda \text{ is the reliability of } W \text{ given } Z \text{ (smaller)}", font_size=30),
            cmath(r"\text{error in } Y", r":", r"\text{no bias, \ only noise}", font_size=30),
        ]
        rows[1][-1].set_color(MNC)
        whys = [why(r"the truth"), why(r"regression dilution"), why(r"adjustment makes it worse"), why(r"an asymmetry")]
        with self.voiceover(
            "<bookmark mark='a'/> In a regression on the true exposure, <bookmark mark='b'/> replacing it by an error-prone "
            "measurement shrinks the slope by the reliability: regression dilution. A reliability of one half halves the "
            "estimated effect. <bookmark mark='c'/> Adjusting for other covariates makes it worse, because the reliability "
            "that matters is the error-prone variable's, given the others. <bookmark mark='d'/> Classical error in the "
            "outcome, by contrast, adds noise but no bias."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        g = np.random.Generator(np.random.PCG64(4112))
        n = 200
        x = g.normal(0, 1, n)
        y = 2 * x + g.normal(0, 1, n)
        w = x + g.normal(0, 1, n)
        A = axes([-4, 4], [-7, 7], x_length=6.4, y_length=4.4, xlabel=r"exposure", ylabel=r"outcome",
                 xticks=[-4, -2, 0, 2, 4], yticks=[-6, -3, 0, 3, 6], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.6, 0.1, 0])
        ax = A.ax
        clip = lambda v, a: np.clip(v, -a, a)  # noqa: E731
        s1 = scatter(ax, clip(x, 3.9), clip(y, 6.9), OBSV, 0.045)
        s2 = scatter(ax, clip(w, 3.9), clip(y, 6.9), MNC, 0.045)
        b1 = np.polyfit(x, y, 1)
        b2 = np.polyfit(w, y, 1)
        l1 = Line(ax.c2p(-3.4, np.polyval(b1, -3.4)), ax.c2p(3.4, np.polyval(b1, 3.4)), color=OBSV, stroke_width=4)
        l2 = Line(ax.c2p(-3.9, np.polyval(b2, -3.9)), ax.c2p(3.9, np.polyval(b2, 3.9)), color=MNC, stroke_width=4)
        side = fit_rows(VGroup(
            label(rf"blue: \ the true exposure, \ slope {b1[0]:.2f}", font_size=22, color=OBSV),
            label(rf"orange: \ measured with error \ (reliability 1/2), \ slope {b2[0]:.2f}", font_size=22, color=MNC),
            label(r"each point slides sideways: \ the cloud spreads, \ the line flattens", font_size=22, color=GREY_A),
        ), 4.6, 0.45, [4.2, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A picture. Two hundred points with a true slope of two, <bookmark mark='b'/> and the same "
            "points with the exposure measured with error of the same variance as the signal. <bookmark mark='c'/> Each "
            "point slides sideways by its error; the cloud stretches horizontally, and the fitted line flattens to about "
            "half the true slope."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(s1), Create(l1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Transform(s1, s2), Create(l2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def nhanes(self):
        d = load("meas")
        rows = fit_rows(VGroup(
            label(rf"NHANES 2017--18: \ {d['n']:,} adults off blood-pressure drugs, \ two 24-hour sodium recalls", font_size=26),
            label(rf"correlation of the two days' sodium: \ {d['rel']:.2f}: \ one recall is mostly day-to-day noise", font_size=26, color=MNC),
            label(rf"systolic pressure on one day's sodium \ (age, \ sex adjusted): \ {d['naive']['b']:.2f} mm Hg per g \ (SE {d['naive']['se']:.2f})", font_size=26, color=MNC),
            label(rf"on the two-day mean: \ {d['mean2']['b']:.2f} \ (SE {d['mean2']['se']:.2f}): \ larger, \ as dilution predicts", font_size=26, color=OBSV),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part twenty's real example. NHANES asks about everything eaten in the past twenty-four "
            "hours, twice, on different days. <bookmark mark='b'/> The two days' sodium intakes correlate only "
            + say(d["rel"], 2) + ": a single recall is mostly day-to-day variation around a person's usual intake, which "
            "is what matters for blood pressure. <bookmark mark='c'/> Regressing systolic pressure on one day's sodium gives "
            + say(d["naive"]["b"], 2) + " millimetres of mercury per gram, indistinguishable from zero. <bookmark "
            "mark='d'/> On the average of two days, the slope roughly doubles, exactly as dilution predicts."
        ) as vo:
            self.add(nhanes_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def rc(self):
        d = load("meas")
        rows = [
            cmath(r"E[X \mid W_1, Z]", r"=", r"E[W_2 \mid W_1, Z]: \ \text{regress the second recall on the first}", font_size=28),
            cmath(r"\text{then}", r":", r"\text{replace } W_1 \text{ by its prediction, \ and refit}", font_size=30),
            cmath(r"\text{NHANES}", r":", rf"\hat\lambda = {d['rc']['lam']:.2f}, \ \ \hat\beta_{{\text{{RC}}}} = {d['rc']['b']:.2f} \text{{ mm Hg per g}}", font_size=30),
            cmath(r"\text{SEs}", r":", r"\text{bootstrap both stages together}", font_size=30),
        ]
        rows[2][-1].set_color(MIC)
        whys = [why(r"replicates as instruments"), why(r"regression calibration"), why(r"Carroll et al.\ (2006)"), why(r"the calibration is estimated too")]
        with self.voiceover(
            "<bookmark mark='a'/> Regression calibration replaces the error-prone exposure by its best prediction of the "
            "truth. With a replicate, that prediction comes from regressing the second recall on the first and the "
            "covariates, because the second day's error is independent of everything else. <bookmark mark='b'/> Then refit "
            "with the prediction in place of the raw value. <bookmark mark='c'/> In NHANES the attenuation factor given age "
            "and sex is " + say(d["rc"]["lam"], 2) + ", and the corrected slope is " + say(d["rc"]["b"], 2) + " millimetres per "
            "gram, still uncertain but four times the naive one. <bookmark mark='d'/> Its standard error must come from "
            "bootstrapping both stages, because the calibration is itself estimated."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def simex_idea(self):
        rows = [
            cmath(r"W_\lambda", r"=", r"W + \sqrt{\lambda}\, \sigma_U Z^*: \ \text{error variance } (1 + \lambda)\sigma_U^2", font_size=30),
            cmath(r"\hat\beta(\lambda)", r":", r"\text{refit, \ average over many } Z^*", font_size=30),
            cmath(r"\text{extrapolate}", r":", r"\lambda \to -1: \ \text{no error at all}", font_size=30),
            cmath(r"\text{needs}", r":", r"\sigma_U^2 \text{ (from replicates) \ and an extrapolant}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"simulate more error"), why(r"watch the slope fall"), why(r"Cook \& Stefanski (1994)"), why(r"quadratic, \ usually")]
        with self.voiceover(
            "<bookmark mark='a'/> SIMEX, John Cook and Leonard Stefanski's simulation-extrapolation of 1994, runs the problem "
            "backwards. Add extra noise to the exposure, lambda times the error variance. <bookmark mark='b'/> Refit, many "
            "times, and watch the slope fall as the noise grows. <bookmark mark='c'/> Then extrapolate the curve back to "
            "lambda equal minus one, where the total error variance would be zero. <bookmark mark='d'/> It needs the error "
            "variance, again from replicates, and a guess at the curve's shape, usually a quadratic."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def simex_plot(self):
        d = load("meas")["seeded"]
        s = d["simex"]
        lam, sl = np.asarray(s["lambda"], float), np.asarray(s["slope"], float)
        A = axes([-1, 2], [0, 2.4], x_length=7.4, y_length=4.2, xlabel=r"$\lambda$: \ extra error, \ in units of $\sigma_U^2$",
                 ylabel=r"fitted slope", xticks=[-1, 0, 1, 2], yticks=[0, 1, 2], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=MNC) for a, b in zip(lam, sl)])
        xs = np.linspace(-1, 2, 100)
        c = polyline(ax, xs, np.polyval(s["coef"], xs), TAUC, 3)
        end = Dot(ax.c2p(-1, s["simex"]), radius=0.11, color=MIC)
        truth = DashedLine(ax.c2p(-1, d["truth"]), ax.c2p(2, d["truth"]), color=TRUEC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"seeded: \ 20,000 people, \ true slope 2, \ reliability 0.39", font_size=22),
            label(rf"orange: \ the slope at each $\lambda$ \ ($\lambda = 0$: \ naive {d['naive']:.2f})", font_size=22, color=MNC),
            label(rf"gold: \ the quadratic, \ extrapolated to $-1$: \ {s['simex']:.2f}", font_size=22, color=TAUC),
            label(rf"regression calibration: \ {d['rc']:.2f}", font_size=22, color=MIC),
            label(r"SIMEX's quadratic undershoots when $\lambda$ is small", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A seeded check with twenty thousand people, a true slope of two and a reliability of "
            "point three nine. <bookmark mark='b'/> The naive slope is " + say(d["naive"], 2) + ", and adding more error "
            "pushes it lower. <bookmark mark='c'/> Extrapolating the quadratic back to minus one gives " + say(s["simex"], 2)
            + ": better, but short, because the true curve, a ratio with the total error variance in its denominator, is not a "
            "quadratic, and bends sharply near minus one. <bookmark mark='d'/> Regression calibration, with its replicate, "
            "gives " + say(d["rc"], 2) + ". <bookmark mark='e'/> SIMEX is most useful when the error is modest; with low "
            "reliability, its extrapolation is a long way out."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(truth), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c), FadeIn(end), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def seeded(self):
        rows = fit_rows(VGroup(
            label(r"Berkson error: \ $X = W + U$ \ (a dose set, \ a person's exposure varies): \ no bias in a linear slope", font_size=26, color=OBSV),
            label(r"error correlated with the truth, \ or differential by outcome: \ any direction", font_size=26, color=MNC),
            label(r"several error-prone covariates: \ bias can even flip signs", font_size=26, color=MNC),
            label(r"Bayesian measurement-error models: \ the truth as a latent variable \ (Part 26)", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Not all error is classical. In Berkson error, the recorded value is fixed, a dose of "
            "radiation assigned to a district, and each person's true exposure scatters around it; a linear slope is then "
            "unbiased. <bookmark mark='b'/> Errors correlated with the truth, or different for cases and controls, can bias "
            "in either direction. <bookmark mark='c'/> With several mismeasured covariates, a confounder measured badly "
            "leaves residual confounding, and signs can flip. <bookmark mark='d'/> The general solution treats the true "
            "values as latent variables in a Bayesian model, Part twenty-six's tools."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def other(self):
        rows = fit_rows(VGroup(
            label(r"a confounder measured with error \ adjusts only partly: \ residual confounding", font_size=26, color=MNC),
            label(r"Part 36's propensity scores inherit the error of their inputs", font_size=26),
            label(r"so: \ measure key exposures twice, \ on a subsample at least", font_size=26, color=TAUC),
            label(r"a validation study is to measurement error \ what follow-up is to missing data", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The consequence most often forgotten: adjusting for a confounder measured with error "
            "removes only part of its confounding. <bookmark mark='b'/> Propensity scores built from noisy covariates "
            "inherit the problem. <bookmark mark='c'/> So measure key exposures and confounders twice, at least on a "
            "subsample, <bookmark mark='d'/> because a validation study is to measurement error what a follow-up of "
            "non-respondents is to missing data: the only real information about the mechanism."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("error-prone", "regression calibration")
        text = (
            "<bookmark mark='a'/> The Board. Five hundred people, an exposure with reliability point six one. The naive "
            "slope's ninety percent interval never covers the truth: it is precise about the wrong number. <bookmark "
            "mark='b'/> Regression calibration with a replicate, and a bootstrap of both stages, keeps the promise."
        )
        show_board(self, rows, text, [("a", [0]), ("b", [1])])

    def instruments(self):
        rows = [
            cmath(r"W_2", r":", r"\text{a second, \ independent measurement of } X", font_size=30),
            cmath(r"\hat\beta_{\text{IV}}", r"=", r"\text{Cov}(W_2, Y) / \text{Cov}(W_2, W_1)", font_size=32),
            cmath(r"\text{why}", r":", r"W_2\text{'s error is independent of } W_1\text{'s and of } Y", font_size=30),
            cmath(r"\text{same answer}", r":", r"\text{as regression calibration, \ in the linear model}", font_size=30),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"a replicate"), why(r"Part 37's instrument"), why(r"exclusion"), why(r"two views of one idea")]
        with self.voiceover(
            "<bookmark mark='a'/> A replicate can also serve as an instrument, in the sense of Part thirty-seven. <bookmark "
            "mark='b'/> The slope of y on the first measurement, instrumented by the second, is the covariance of the second "
            "with y over its covariance with the first. <bookmark mark='c'/> It works because the second measurement's "
            "error is independent of the first's and of the outcome, an exclusion restriction that holds by design. "
            "<bookmark mark='d'/> In the linear model this gives the same answer as regression calibration, two views of one "
            "idea."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()


    def deming(self):
        rows = [
            cmath(r"\text{both } X \text{ and } Y \text{ noisy}", r":", r"\text{errors-in-variables}", font_size=30),
            cmath(r"\text{Deming}", r":", r"\text{minimize distances weighted by } \delta = \sigma_V^2 / \sigma_U^2", font_size=30),
            cmath(r"\delta = 1", r":", r"\text{orthogonal regression: \ the first principal component}", font_size=30),
            cmath(r"\text{needs}", r":", r"\text{the error-variance ratio: \ otherwise not identified}", font_size=30),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"method comparison studies"), why(r"Deming (1943)"), why(r"Part 31's PCA"), why(r"Reiers\o l (1950)")]
        with self.voiceover(
            "<bookmark mark='a'/> When both variables are measured with error, as when two laboratory methods are compared, "
            "<bookmark mark='b'/> W. Edwards Deming's regression minimizes distances to the line weighted by the ratio of "
            "the two error variances, the errors-in-variables model of Part twenty-three. <bookmark mark='c'/> With equal "
            "error variances it is orthogonal regression, the first principal component of Part thirty-one. <bookmark "
            "mark='d'/> Without knowing the ratio, the slope is not identified for normal data at all, as Olav Reiersøl "
            "proved in 1950."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

