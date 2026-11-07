from __future__ import annotations

import numpy as np

from videos.stats.stats49.common import *  # noqa: F403


class EfficientScore(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.picture()
        self.adaptation()
        self.hetero()
        self.cases()

    def card(self):
        card = chapter_card(5, r"The nuisance tangent space and the efficient score", r"Project the nuisance away", lit=(1982,), part=PART)
        with self.voiceover("Chapter five. The nuisance tangent space and the efficient score: project the nuisance away."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"\mathcal P = \{p_{\theta, \eta}\}", r":", r"\theta \in \mathbb R^k \text{ of interest}, \ \eta \text{ an infinite-dimensional nuisance}", font_size=30),
            cmath(r"\Lambda_\eta", r"=", r"\overline{\text{span}}\{\text{scores of paths moving } \eta \text{ alone}\}", font_size=32),
            cmath(r"\tilde\ell_\theta", r"=", r"\dot\ell_\theta - \Pi(\dot\ell_\theta \mid \Lambda_\eta): \ \text{the efficient score}", font_size=32),
            cmath(r"\tilde I_\theta = E\,\tilde\ell_\theta \tilde\ell_\theta^\top", r",", r"\phi^* = \tilde I_\theta^{-1}\, \tilde\ell_\theta: \ \text{the bound is } \tilde I_\theta^{-1}", font_size=32),
        ]
        rows[1][-1].set_color(NUIC)
        rows[2][-1].set_color(EFFC)
        whys = [why(r"a semiparametric model, \ parametrized"), why(r"the nuisance tangent space"), why(r"the part of the score the nuisance cannot mimic"), why(r"the efficient information")]
        heading = label('An orthogonal projection identifies the efficient part', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Often the model is written with a finite-dimensional parameter of interest theta and an "
            "infinite-dimensional nuisance eta. <bookmark mark='b'/> Two kinds of direction then matter: the ordinary score "
            "for theta, and the nuisance tangent space, spanned by the scores of paths that move eta alone. <bookmark "
            "mark='c'/> The efficient score is what remains of theta's score after projecting out the nuisance tangent space: "
            "the part of a change in theta that no change in the nuisance can imitate. <bookmark mark='d'/> Its variance is "
            "the efficient information, its inverse is the bound, and the efficient influence function is the efficient "
            "score scaled by the inverse information."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        T = TangentSpace(origin=(-2.4, -1.4, 0.0), scale=1.6)
        box = T.plane(extent=2.6, color=GREY_D, opacity=0.05)
        nl = T.line((1.0, 0.6, 0.0), extent=2.6, color=NUIC, stroke_width=5)
        v = np.array([1.6, 0.2, 1.4])
        sc = T.arrow(v, color=GRADC)
        proj = T.project(v, [[1.0, 0.6, 0.0]])
        foot = T.arrow(proj, color=NUIC, stroke_width=4)
        resid = T.arrow(v, color=EFFC, start=proj)
        dash = DashedLine(T.to_screen(v), T.to_screen(proj), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"red line: \ $\Lambda_\eta$, \ moves of the nuisance", font_size=22, color=NUIC),
            label(r"blue: \ $\dot\ell_\theta$, \ the score for $\theta$", font_size=22, color=GRADC),
            label(r"red arrow: \ the part a nuisance move can mimic", font_size=22, color=NUIC),
            label(r"gold: \ $\tilde\ell_\theta$, \ the efficient score", font_size=22, color=EFFC),
            label(r"shorter score $\Rightarrow$ less information $\Rightarrow$ bigger bound", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the picture: the red line is the nuisance tangent space. <bookmark mark='b'/> The blue arrow is the score for theta. If the nuisance were known, its length squared would be the information. <bookmark mark='c'/> But part of the score lies along the nuisance directions: a small change in theta looks, to the data, partly like a small change in the nuisance, and that part cannot be used. <bookmark mark='d'/> What remains, the gold arrow perpendicular to the nuisance space, is the efficient score. <bookmark mark='e'/> It is shorter, so the information is smaller and the bound larger: the information lost is the squared length of the red projection. The variance penalty is the difference between inverse informations."
        ) as vo:
            self.play(FadeIn(box), FadeIn(exact_tag(r"a schematic")))
            vo.wait_until("a")
            self.play(Create(nl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowArrow(sc), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(dash), GrowArrow(foot), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowArrow(resid), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def adaptation(self):
        rows = [
            cmath(r"X = \theta + \varepsilon, \ \varepsilon \sim f \text{ symmetric}", r":", r"\dot\ell_\theta(x) = -\frac{f'}{f}(x - \theta): \ \text{an odd function}", font_size=30),
            cmath(r"\Lambda_f", r"=", r"\{\text{mean-zero even }L_2(f)\text{ functions}\}: \ \text{symmetric changes of shape}", font_size=32),
            cmath(r"\text{odd} \perp \text{even}", r"\Rightarrow", r"\Pi(\dot\ell_\theta \mid \Lambda_f) = 0, \ \ \tilde\ell_\theta = \dot\ell_\theta", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\tilde I = I_f: \ \text{not knowing } f \text{ costs nothing: \ adaptation}", font_size=34),
        ]
        rows[2][-1].set_color(TANC)
        rows[3][-1].set_color(EFFC)
        whys = [why(r"the hook's model"), why(r"the nuisance tangent space"), why(r"symmetry does the work"), why(r"Stein's necessary condition (1956), \ Bickel (1982)")]
        heading = label('Odd location scores are orthogonal to symmetric shape changes', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Now the hook is explained. For a symmetric law, the location score minus f prime over f, at "
            "x minus theta, is an odd function. <bookmark mark='b'/> Changing the shape while keeping it symmetric gives "
            "scores that are even functions. <bookmark mark='c'/> Odd and even functions of a symmetric variable are "
            "orthogonal, so the projection is zero and the efficient score is the full score. <bookmark mark='d'/> The "
            "efficient information equals the information with f known. Not knowing f costs nothing, and an estimator that "
            "estimates the score, like Stone's, can reach the bound. Stein's 1956 condition for adaptation is exactly this "
            "orthogonality, and Bickel's 1982 paper turned it into estimators."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hetero(self):
        rows = [
            cmath(r"\text{PLR, \ } \mathrm{Var}(\varepsilon \mid T, X) = \sigma^2(T,X)", r":", r"\text{the efficient score changes}", font_size=32),
            cmath(r"\tilde\ell_\theta", r"=", r"\frac{(Y - \theta T - g(X))\,(T - \tilde m(X))}{\sigma^2(T,X)}, \ \ \tilde m = \frac{E[T/\sigma^2(T,X) \mid X]}{E[1/\sigma^2(T,X) \mid X]}", font_size=30),
            cmath(r"\text{Robinson's score}", r":", r"\text{orthogonal; root-}n\text{ with adequate rates; not generally efficient}", font_size=32),
            cmath(r"\text{orthogonal}", r"\ne", r"\text{efficient: \ orthogonality protects, \ efficiency optimizes}", font_size=32),
        ]
        rows[1][-1].set_color(EFFC)
        rows[2][-1].set_color(OSC)
        whys = [why(r"heteroskedastic errors"), why(r"weighted residuals"), why(r"DML's default"), why(r"two different properties")]
        heading = label('Heteroskedasticity changes the efficient weighting', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> One subtlety. In the partially linear model with an error variance that can depend on both T and X, the efficient score changes. <bookmark mark='b'/> It weights by one over the variance, and centres T at a weighted regression rather than the plain one. <bookmark mark='c'/> Robinson's unweighted score is still orthogonal to the nuisance, and can remain root n consistent when nuisance product rates and the empirical-process conditions hold, but it is no longer efficient. <bookmark mark='d'/> Orthogonality and efficiency are different properties. Orthogonality protects an estimator from the nuisance's first-order errors; efficiency makes it the best such estimator. Efficient scores are orthogonal to nuisance tangent directions, while an arbitrary nuisance-orthogonal estimating function need not attain the efficiency bound."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cases(self):
        rows = fit_rows(VGroup(
            label(r"adaptive: \ symmetric location; \ certain regression error-density nuisances under suitable independence conditions", font_size=24, color=EFFC),
            label(r"without a shape-centering restriction, location + unrestricted shape is unidentified", font_size=24, color=NUIC),
            label(r"not adaptive: \ the ATE: \ unknown regressions add $E[\sigma_1^2/e + \sigma_0^2/(1-e)]$", font_size=24, color=NUIC),
            label(r"in between: \ Cox's $\beta$: \ the risk-set centring is the price of the unknown baseline", font_size=24, color=GREY_A),
            label(r"the efficient score is orthogonal to the nuisance: \ chapter 8's Neyman orthogonality", font_size=24, color=TANC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Adaptation happens in a few lucky models: symmetric location, linear regression with symmetric errors, and partially linear models with suitable independent error-density nuisance assumptions. Adaptation must specify which nuisance is being treated as unknown. <bookmark mark='b'/> An unrestricted location-plus-unknown-shape decomposition is unidentified without a centring convention. Means and medians can still be defined without symmetry; they then represent different models and targets. <bookmark mark='c'/> And it fails for the average treatment effect, whose bound includes the inverse-propensity-weighted residual variances that the unknown outcome regressions bring. <bookmark mark='d'/> Cox's model is in between: centring at the risk set is exactly the price of not knowing the baseline. <bookmark mark='e'/> But the efficient score always has one property, by construction: it is orthogonal to the nuisance directions. Chapter eight shows why that orthogonality is what makes their first-order errors vanish, subject to sufficient remainder rates and stochastic control."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
