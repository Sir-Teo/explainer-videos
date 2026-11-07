from __future__ import annotations

import numpy as np

from videos.stats.stats49.common import *  # noqa: F403


class Estimators(VoiceoverScene):
    def construct(self):
        self.card()
        self.expansion()
        self.middle()
        self.recipes()
        self.chart()
        self.table()
        self.compare()
        self.nsw()

    def card(self):
        card = chapter_card(6, r"Constructing efficient estimators", r"One-step, \ estimating equations, \ TMLE", lit=(2006,), part=PART)
        with self.voiceover("Chapter six. Constructing efficient estimators: one-step, estimating equations, and targeted maximum likelihood."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def expansion(self):
        rows = [
            cmath(r"\psi(\hat P) - \psi(P)", r"=", r"-P\phi^*_{\hat P} + R_2(\hat P, P)", font_size=36),
            cmath(r"\phantom{\psi}", r"=", r"-P_n \phi^*_{\hat P} + (P_n - P)\phi^*_{\hat P} + R_2", font_size=36),
            cmath(r"\text{the plug-in's bias}", r":", r"-P_n \phi^*_{\hat P}, \ \text{first order in the nuisance error}", font_size=32),
            cmath(r"R_2", r"=", r"O(\|\hat\eta - \eta\|^2): \ \text{second order}", font_size=36),
        ]
        rows[2][-1].set_color(PLUGC)
        rows[3][-1].set_color(TANC)
        whys = [why(r"the von Mises expansion"), why(r"add and subtract $P_n$"), why(r"what a plug-in leaves behind"), why(r"products of nuisance errors")]
        heading = label('A controlled von Mises remainder supports bias correction', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> For the smooth functionals considered here, the constructions use a von Mises expansion with a controlled remainder. Plug an estimate of the distribution into psi. The error is minus the true mean of the efficient influence function evaluated at the estimate, plus a second-order remainder. <bookmark mark='b'/> Adding and subtracting the empirical mean splits it into three parts: minus the empirical mean of the estimated influence function, an empirical-process term, and the remainder. <bookmark mark='c'/> The first is an empirical correction for leading plug-in error, not literally its sampling bias in every dataset, and it is first order in the error of the nuisance estimates: if they converge slowly, so does the plug-in. <bookmark mark='d'/> The remainder can be bounded to second order under functional smoothness and positivity, typically a product of two nuisance errors. The middle term is the good part, the root-n fluctuation, controlled by Part forty-eight's empirical-process theory."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def middle(self):
        rows = [
            cmath(r"(P_n - P)\,\phi^*_{\hat P}", r"=", r"(P_n - P)\,\phi^*_P + (P_n - P)(\phi^*_{\hat P} - \phi^*_P)", font_size=34),
            cmath(r"\text{first piece}", r":", r"\tfrac1n \textstyle\sum \phi^*(X_i): \ \text{the CLT, \ the efficient variance}", font_size=32),
            cmath(r"\text{second piece}", r"=", r"o_P(n^{-1/2}) \ \text{if } \{\phi^*_{\hat P}\} \text{ is Donsker and } \|\phi^*_{\hat P} - \phi^*_P\| \to 0", font_size=30),
            cmath(r"\text{or}", r":", r"\text{cross-fit } \hat P: \ \text{no Donsker condition needed}", font_size=32),
        ]
        rows[1][-1].set_color(EFFC)
        rows[2][-1].set_color(GRADC)
        rows[3][-1].set_color(OSC)
        whys = [why(r"split the middle term"), why(r"the good part"), why(r"Part 48's asymptotic equicontinuity"), why(r"cross-fitting: \ chapter 8")]
        heading = label('Control the estimated influence function on held-out observations', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The middle, empirical-process term splits again: the empirical process applied to the true efficient influence function, plus the empirical process applied to the difference between the estimated and true influence functions. <bookmark mark='b'/> The first piece is a plain average, and the central limit theorem gives it the efficient variance. <bookmark mark='c'/> The second is negligible if the estimated influence functions lie in a Donsker class and converge to the truth in L-two: exactly Part forty-eight's asymptotic equicontinuity. <bookmark mark='d'/> If the nuisances come from a learner too flexible for any Donsker class, fit them on separate data instead. Then, within each held-out fold and conditionally on its training data, the second piece is an average of mean-zero terms with vanishing variance, and no Donsker condition is needed. That is cross-fitting, and chapter eight returns to it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def recipes(self):
        rows = [
            cmath(r"\text{one-step}", r":", r"\hat\psi = \psi(\hat P) + P_n \phi^*_{\hat P}: \ \text{add the bias back}", font_size=32),
            cmath(r"\text{estimating equation}", r":", r"\text{solve } P_n \phi^*_{\hat\eta}(\,\cdot\,; \psi) = 0 \ \text{for } \psi", font_size=32),
            cmath(r"\text{TMLE}", r":", r"\text{move } \hat P \text{ along the least favourable path until } P_n \phi^*_{\hat P^*} = 0", font_size=30),
            cmath(r"\text{ATE, \ continuous } Y", r":", r"\hat\mu_t^* = \hat\mu_t + \hat\varepsilon\, H_t, \ \ H = \tfrac{T}{\hat e} - \tfrac{1 - T}{1 - \hat e}", font_size=30),
        ]
        rows[0][-1].set_color(OSC)
        rows[2][-1].set_color(TMLEC)
        whys = [why(r"Pfanzagl; \ Bickel (1982); \ for the ATE: \ AIPW"), why(r"Robins et al.\ (1994)"), why(r"van der Laan \& Rubin (2006)"), why(r"the clever covariate")]
        heading = label('One-step correction and targeting solve related estimating equations', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Three ways to remove that bias. The one-step estimator adds the empirical mean of the estimated influence function to the plug-in. For the average treatment effect, that is exactly augmented inverse probability weighting. <bookmark mark='b'/> The estimating-equation approach treats the influence function as an equation in psi and solves it. <bookmark mark='c'/> Targeted maximum likelihood, due to Mark van der Laan and Daniel Rubin in 2006, instead changes the estimated distribution, moving it along the least favourable submodel until the empirical mean of the influence function is zero, and then plugs in. <bookmark mark='d'/> For the treatment effect with a continuous outcome, the move adds epsilon times a clever covariate, one over the propensity for the treated and minus one over one minus it for the controls, with epsilon fitted by least squares. This linear Gaussian fluctuation solves the empirical influence equation for an unbounded continuous outcome. It is not range preserving for binary or bounded outcomes; those need an appropriate constrained fluctuation. Efficiency also requires the stated consistency and remainder conditions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("onestep")
        ln = np.log10(d["ns"])
        A = axes([2.2, 4.4], [-2, 8], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\sqrt n \times$ bias",
                 xticks=[np.log10(250), 3, np.log10(4000), np.log10(16000)], xfmt=lambda v: f"{10 ** v:,.0f}", yticks=[-2, 0, 2, 4, 6, 8], center=[-2.5, 0.2, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(2.2, 0), ax.c2p(4.4, 0), color=GREY_B, stroke_width=2)

        def line(key, c):
            v = [r[key] for r in d["rows"]]
            return VGroup(polyline(ax, ln, v, c, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=c) for a, b in zip(ln, v)])

        cp, co, ct = line("rb_plugin", PLUGC), line("rb_os", OSC), line("rb_tmle", TMLEC)
        r = d["rows"]
        side = fit_rows(VGroup(
            label(r"nuisances off by $n^{-0.3}$: \ slower than root-$n$", font_size=22),
            label(r"purple: \ the plug-in: \ $\sqrt n$-bias grows like $n^{0.2}$", font_size=22, color=PLUGC),
            label(r"teal: \ one-step: \ shrinks, \ like $n^{-0.1}$", font_size=22, color=OSC),
            label(r"green: \ TMLE: \ the same", font_size=22, color=TMLEC),
            label(rf"SD of $\sqrt n\,\hat\psi$: \ {r[-1]['sd_os']:.2f}", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A controlled experiment in the smooth world of chapter three: give each estimator nuisance "
            f"functions that are wrong by n to the minus point three, slower than root n, as machine learning typically is. "
            f"<bookmark mark='b'/> The plug-in's bias, scaled by root n, grows: from {say(r[0]['rb_plugin'], 1)} at two "
            f"hundred and fifty to {say(r[-1]['rb_plugin'], 1)} at sixteen thousand. Its errors are first order. <bookmark "
            f"mark='c'/> The one-step's scaled bias shrinks, to {say(r[-1]['rb_os'], 2)}, because what is left is second "
            f"order: a product of two errors of order n to the minus point three. <bookmark mark='d'/> Targeted maximum "
            f"likelihood behaves the same way. <bookmark mark='e'/> Both are within a fraction of a standard error of the "
            f"truth; the estimation error has scaled standard deviation about {say(r[-1]['sd_os'], 1)}."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(simulated_tag(r"simulated: \ 200--600 samples per $n$")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cp), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(co), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ct), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("onestep")
        rows = [[r"$n$", r"plug-in", r"one-step", r"TMLE"]]
        for r in d["rows"]:
            rows.append([f"{r['n']:,}", f"{100 * r['cov_plugin']:.1f}\\%", f"{100 * r['cov_os']:.1f}\\%", f"{100 * r['cov_tmle']:.1f}\\%"])
        tab = table_rows(rows, font_size=30, col_buff=1.0, row_buff=0.36, colors=[GREY_B] + [None] * 4)
        tab.move_to([0, 0.8, 0])
        for i in range(1, 5):
            tab[i][1].set_color(PLUGC)
            tab[i][2].set_color(OSC)
            tab[i][3].set_color(TMLEC)
        foot = label(r"coverage of nominal 90\% intervals, \ $\pm 1.645 \times$ the influence-function SE", font_size=24, color=GREY_A).move_to([0, -1.6, 0])
        foot2 = label(r"the plug-in's interval is centred in the wrong place, \ and more wrongly as $n$ grows", font_size=24, color=PLUGC).move_to([0, -2.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Coverage of ninety percent intervals tells the same story. The one-step and targeted "
            f"intervals cover about ninety percent at every sample size. The plug-in, given the same standard error, covers "
            f"{100 * d['rows'][1]['cov_plugin']:.0f} percent at a thousand and none at all at four thousand. <bookmark "
            f"mark='b'/> More data makes a biased plug-in worse, because its interval shrinks around the wrong centre."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def compare(self):
        rows = [
            cmath(r"\text{one-step}", r":", r"\text{may leave the parameter space: \ a probability} > 1", font_size=32),
            cmath(r"\text{TMLE}", r":", r"\text{range preserving with an appropriate constrained fluctuation}", font_size=32),
            cmath(r"\text{binary } Y", r":", r"\text{logistic fluctuation: \ } \operatorname{logit} \hat\mu^*_t = \operatorname{logit}\hat\mu_t + \varepsilon H_t", font_size=30),
            cmath(r"\text{to first order}", r":", r"\text{the same; \ they differ at second order}", font_size=34),
        ]
        rows[1][-1].set_color(TMLEC)
        rows[3][-1].set_color(EFFC)
        whys = [why(r"adding a correction can overshoot"), why(r"the targeting step"), why(r"stays in $(0, 1)$"), why(r"chapter 6's expansion")]
        heading = label('A constrained targeting model can preserve the parameter range', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Why have two efficient estimators? The one-step estimator adds a correction, and a correction can overshoot: a probability above one, an effect larger than any possible, a negative variance. <bookmark mark='b'/> With a suitable constrained fluctuation the targeted estimator is a plug-in of a genuine distribution and respects the parameter range. The linear continuous-outcome implementation here is unbounded. <bookmark mark='c'/> For a binary outcome the fluctuation is on the logistic scale, so the updated predictions stay between zero and one. <bookmark mark='d'/> To first order they are the same estimator, with the same influence function; they differ at second order, and finite-sample behaviour depends on the targeting model, nuisance fits and overlap. Neither method repairs lack of identification or guarantees better small-sample coverage."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def nsw(self):
        d = load("nsw")
        ex, ps = d["experiment"], d["psid"]
        rows = [
            cmath(rf"\text{{NSW experiment}}, \ n = {ex['n']}", r":", rf"\text{{difference in means }} {ex['dm']:,.0f} \ ({ex['dm_se']:,.0f})", font_size=30),
            cmath(r"\text{one-step} = \text{TMLE}:\ \text{arm-specific OLS residual sums vanish}", r":", rf"{ex['os']:,.0f} \ ({ex['os_se']:,.0f}): \ \text{{a smaller SE}}", font_size=30),
            cmath(rf"\text{{NSW treated vs.\ {ps['n0']} PSID men}}", r":", rf"\text{{naive }} {ps['naive']:,.0f}; \ \text{{regression }} {ps['reg']:,.0f}", font_size=30),
            cmath(r"\text{ATT one-step, refitted-bootstrap SE}", r":", rf"{ps['att']:,.0f} \ ({ps['att_se']:,.0f}) \ \ \text{{vs.\ the experiment's }} {ps['benchmark']:,.0f}", font_size=30),
        ]
        rows[1][-1].set_color(OSC)
        rows[3][-1].set_color(TMLEC)
        whys = [why(r"LaLonde (1986); \ Dehejia \& Wahba"), why(r"adjustment in a trial: \ known $e$"), why(r"the observational problem"), why(r"Part 36's data, \ revisited")]
        heading = label('Job-training comparisons require overlap and identification assumptions', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            f"<bookmark mark='a'/> Real data: the National Supported Work experiment from Part thirty-six: earnings in 1978, in 1982 dollars. The randomized difference in means is {ex['dm']:,.0f}, with standard error {ex['dm_se']:,.0f}. <bookmark mark='b'/> In this randomized-sample calculation we use the observed allocation fraction as a constant propensity, but the efficient influence function still uses the outcome regressions: the one-step estimator with linear regressions gives {ex['os']:,.0f}, with a slightly smaller standard error. Here arm-specific OLS residuals sum to zero, so the targeting correction is zero and the two adjusted estimates coincide. Constant propensity alone would not imply equality for arbitrary initial fits. <bookmark mark='c'/> Replace the experimental controls with {ps['n0']} men from the Panel Study of Income Dynamics, and the naive difference is {ps['naive']:,.0f}: badly confounded. <bookmark mark='d'/> The efficient one-step estimator of the effect on the treated, with a logistic propensity and a linear outcome model, gives {ps['att']:,.0f}, with standard error {ps['att_se']:,.0f}: with limited overlap and potentially misspecified nuisance models. The reported observational SE comes from stratified resampling that refits both nuisances. Agreement with a noisy experimental benchmark does not validate the identification assumptions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.add(museum_tag(r"LaLonde (1986); \ Dehejia \& Wahba (1999)"))
        self.wait(0.5)
        self.clear_scene()
