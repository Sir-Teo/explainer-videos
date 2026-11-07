from __future__ import annotations

from videos.stats.stats49.common import *  # noqa: F403


class Worked(VoiceoverScene):
    def construct(self):
        self.card()
        self.mean()
        self.ate()
        self.att()
        self.trial()
        self.plr()
        self.cox()

    def card(self):
        card = chapter_card(4, r"Worked influence functions", r"The mean, \ the ATE, \ the partially linear model, \ Cox", lit=(1998, 1988), part=PART)
        with self.voiceover("Chapter four. Worked influence functions: the mean, the average treatment effect, the partially linear model, and Cox."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def mean(self):
        rows = [
            cmath(r"\psi(P) = E_P X", r":", r"\tfrac{d}{dt} \textstyle\int x\, p(1 + ts)\,dx = \int x\, s\, p = E[(X - \mu)\, s]", font_size=32),
            cmath(r"\phi^*(x)", r"=", r"x - \mu: \ \ \text{the sample mean is efficient, \ nonparametrically}", font_size=32),
            cmath(r"\psi(P) = F^{-1}(p)", r":", r"\phi^* = (p - \mathbf 1\{x \le \xi_p\})/f(\xi_p): \ \text{the sample quantile}", font_size=30),
            cmath(r"\text{the trick}", r":", r"\text{differentiate } \psi(P_t) \text{ along } p(1 + ts), \ \text{read off } \phi", font_size=32),
        ]
        rows[1][-1].set_color(EFFC)
        rows[2][-1].set_color(EFFC)
        whys = [why(r"the nonparametric path"), why(r"centred: \ $E\,s = 0$ absorbs $\mu$"), why(r"Part 47's influence function"), why(r"Kennedy (2022)'s point-mass trick, \ too")]
        heading = label('Finite-variance means and regular quantiles have canonical gradients', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Start with the simplest. The mean, in a nonparametric model with finite second moment. Along the path p times one plus t s, the mean changes at rate the integral of x s p, which is the covariance of X with the score. <bookmark mark='b'/> So the efficient influence function is x minus mu, and the sample mean, whose influence function it is, is efficient: no regular estimator of a mean does better without assumptions. <bookmark mark='c'/> The same computation for a quantile gives Part forty-seven's influence function, and shows the sample quantile is efficient when the density is positive and continuous at the unique quantile. <bookmark mark='d'/> The trick, always: differentiate psi along the path and read off the function that multiplies the score."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ate(self):
        rows = [
            cmath(r"\psi = E[\mu_1(X) - \mu_0(X)]", r",", r"\mu_t(x) = E[Y \mid T = t, X = x], \ e(x) = P(T = 1 \mid x)", font_size=30),
            cmath(r"\phi^*", r"=", r"\mu_1 - \mu_0 - \psi + \tfrac{T}{e}(Y - \mu_1) - \tfrac{1 - T}{1 - e}(Y - \mu_0)", font_size=36),
            cmath(r"E\,\phi^{*2}", r"=", r"\mathrm{Var}\,\tau(X) + E\Big[\frac{\sigma_1^2(X)}{e(X)} + \frac{\sigma_0^2(X)}{1 - e(X)}\Big]", font_size=32),
            cmath(r"\text{knowing } e(x) \text{ (a trial)}", r":", r"\text{same bound: EIF orthogonal to propensity directions}", font_size=30),
        ]
        rows[1][-1].set_color(EFFC)
        rows[2][-1].set_color(TANC)
        whys = [why(r"under no unmeasured confounding"), why(r"Hahn (1998); \ Robins et al. (1994)"), why(r"overlap enters as $1/e$"), why(r"Hahn's surprise")]
        heading = label('The ATE influence function uses outcome and treatment information', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The main example. The average treatment effect under consistency, conditional exchangeability and positivity is the mean of the difference between the two outcome regressions. <bookmark mark='b'/> Its efficient influence function, found by Jinyong Hahn in 1998 and implicit in Robins and colleagues' 1994 work, is the plug-in's term plus two weighted residual corrections: the residuals of the treated, weighted by one over the propensity, and of the controls, weighted by one over one minus it. <bookmark mark='c'/> Its variance, the bound, is the variance of the conditional effect plus the residual variances inflated by the inverse propensities. Poor overlap, propensities near zero or one, makes the bound large: no method can escape it. <bookmark mark='d'/> And a surprise of Hahn's: knowing the propensity, as in a randomized trial, does not lower the bound at all."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def att(self):
        rows = [
            cmath(r"\psi_{\text{ATT}} = E[Y^1 - Y^0 \mid T = 1]", r",", r"p = P(T = 1)", font_size=34),
            cmath(r"\phi^*", r"=", r"\frac{1}{p}\Big[T\,(Y - \mu_0(X) - \psi) - (1 - T)\frac{e(X)}{1 - e(X)}(Y - \mu_0(X))\Big]", font_size=32),
            cmath(r"\text{only } \mu_0 \text{ and } e", r":", r"\text{the treated's own outcomes need no model}", font_size=32),
            cmath(r"\text{knowing } e(x)", r":", r"\text{lowers the ATT's bound, \ unlike the ATE's}", font_size=34),
        ]
        rows[1][-1].set_color(EFFC)
        rows[3][-1].set_color(NUIC)
        whys = [why(r"the effect on the treated"), why(r"Hahn (1998)"), why(r"controls weighted by the odds $e/(1-e)$"), why(r"$e$ tells us who the treated are")]
        heading = label('The ATT has a different gradient and a different target population', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The effect on the treated, the estimand of the job-training studies, has its own efficient "
            "influence function, also from Hahn's paper. <bookmark mark='b'/> It is the treated's outcomes minus the control "
            "regression's prediction for them, and the controls' residuals weighted by the propensity odds, e over one minus "
            "e, all scaled by one over the fraction treated. <bookmark mark='c'/> Only the control regression and the "
            "propensity appear: the treated's own outcomes are observed and need no model. <bookmark mark='d'/> And here "
            "knowledge of the propensity does lower the bound, because the propensity carries information about which "
            "population the treated are. Chapter six applies this to LaLonde's data."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def trial(self):
        rows = [
            cmath(r"L_2^0(P)", r"=", r"\mathcal T_X \oplus \mathcal T_{T \mid X} \oplus \mathcal T_{Y \mid T, X}", font_size=36),
            cmath(r"\text{observational}", r":", r"\text{all three pieces: \ the nonparametric model}", font_size=32),
            cmath(r"\text{a trial, \ } e \text{ known}", r":", r"\mathcal T_{T \mid X} \text{ removed: \ a smaller model}", font_size=32),
            cmath(r"\phi^*_{\text{ATE}} \perp \mathcal T_{T \mid X}", r"\Rightarrow", r"\text{the projection, \ and the bound, \ are unchanged}", font_size=32),
        ]
        rows[2][-1].set_color(NUIC)
        rows[3][-1].set_color(EFFC)
        whys = [why(r"factor the likelihood"), why(r"nothing assumed"), why(r"the design is known"), why(r"why Hahn's surprise is true")]
        heading = label('Knowing treatment probabilities removes one score subspace', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Why does knowing the propensity not help the average treatment effect? Factor the "
            "likelihood into the law of X, the treatment given X, and the outcome given treatment and X. The space of scores "
            "splits into three orthogonal pieces, one for each factor. <bookmark mark='b'/> In an observational study all "
            "three are free. <bookmark mark='c'/> In a trial the treatment mechanism is known, so its piece of the tangent "
            "space is removed. <bookmark mark='d'/> But the ATE's efficient influence function has no component in that "
            "piece, so projecting onto the smaller tangent space changes nothing, and the bound is the same. For the effect "
            "on the treated, the influence function does have such a component, and knowing the propensity helps."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def plr(self):
        rows = [
            cmath(r"Y = \theta T + g(X) + \varepsilon", r",", r"E[\varepsilon \mid T, X] = 0, \ g \text{ unknown}", font_size=34),
            cmath(r"m(X) = E[T \mid X]", r",", r"\ell(X) = E[Y \mid X] = \theta\, m(X) + g(X)", font_size=34),
            cmath(r"\text{proportional to efficient score, homoskedastic}", r":", r"(Y - \ell(X) - \theta(T - m(X)))\,(T - m(X))", font_size=30),
            cmath(r"\hat\theta", r"=", r"\frac{\sum (T_i - \hat m)(Y_i - \hat\ell)}{\sum (T_i - \hat m)^2}: \ \text{residual on residual}", font_size=32),
        ]
        rows[2][-1].set_color(EFFC)
        rows[3][-1].set_color(OSC)
        whys = [why(r"Robinson (1988)"), why(r"two nuisance regressions"), why(r"orthogonal to every change in $g$"), why(r"Part 36's DML, \ explained")]
        heading = label('Residual regression needs appropriate variance weighting for efficiency', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Peter Robinson's partially linear model of 1988: a linear effect of a treatment T plus an arbitrary function of the covariates. <bookmark mark='b'/> Write m for the regression of T on X and l for the regression of Y on X. <bookmark mark='c'/> In the conditional-mean model with constant error variance, a quantity proportional to the efficient score is the residual of Y minus theta times the residual of T, multiplied by the residual of T. It is orthogonal to every direction in which g could move, The appropriate variance normalization gives the efficient score; orthogonality alone would not prove efficiency. <bookmark mark='d'/> Setting its average to zero gives the residual-on-residual regression: Part thirty-six's double machine learning estimator for this model, now seen as the efficient one."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cox(self):
        rows = fit_rows(VGroup(
            label(r"Cox's model: \ $\lambda(t \mid x) = \lambda_0(t)\, e^{\beta^\top x}$, \ the baseline hazard $\lambda_0$ unknown", font_size=26),
            label(r"the nuisance tangent space: \ all changes $\lambda_0(t)(1 + t\,h(t))$ in the baseline", font_size=26, color=NUIC),
            label(r"projecting the score for $\beta$ off it \ = \ centring $x$ at each risk set's weighted mean", font_size=26, color=TANC),
            label(r"that is the partial-likelihood score: \ Cox's estimator is semiparametrically efficient", font_size=26, color=EFFC),
            label(r"Efron (1977); \ Begun, \ Hall, \ Huang \& Wellner (1983)", font_size=24, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> And one result from Part forty. In Cox's proportional hazards model the baseline hazard is an unknown function. <bookmark mark='b'/> Its directions of change form the nuisance tangent space. <bookmark mark='c'/> Projecting the full-likelihood score for beta off that space amounts to centring each subject's covariates at the weighted mean of the risk set at each event time, <bookmark mark='d'/> which is exactly the score of Cox's partial likelihood. Under the proportional-hazards model, conditionally independent censoring and suitable regularity, Cox's partial-likelihood estimator is semiparametrically efficient, <bookmark mark='e'/> as Bradley Efron found in 1977 and Begun, Hall, Huang and Wellner proved in general in 1983."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
