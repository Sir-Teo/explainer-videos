from __future__ import annotations

import numpy as np

from videos.stats.stats60.common import *  # noqa: F403


class DRO(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter seven. Distributionally robust optimization: guarding against every shift in a ball.", 7,
                            r"Distributionally robust optimization", r"The worst case, within reason", lit=(2013,))
        self.idea()
        self.balls()
        self.duality()
        self.groups()
        self.fairness()
        self.chart()
        self.wasserstein()
        self.price()

    def idea(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Chapters five and six assumed the shift had a known structure. What if it does not? "
            "<bookmark mark='b'/> Distributionally robust optimization fits the model that minimizes the worst expected loss "
            "over a whole set of distributions near the training distribution: an uncertainty set. <bookmark mark='c'/> The "
            "idea comes from robust optimization, from Aharon Ben-Tal, Laurent El Ghaoui and Arkadi Nemirovski; Ben-Tal and "
            "co-authors gave the divergence-ball form in 2013. <bookmark mark='d'/> Its answer is a bound: whatever the test "
            "distribution, if it lies in the set, the risk is at most the robust objective.",
            [(r"\text{no structure}", r":", r"\text{the shift is unknown}", 40),
             (r"\text{DRO}", r":", r"\min_\theta \ \sup_{Q \in \mathcal U(\hat P_n)} E_Q[\ell(\theta; Z)]", 40),
             (r"\text{origin}", r":", r"\text{robust optimization; \ Ben-Tal et al. (2013)}", 40),
             (r"\text{guarantee}", r":", r"Q \in \mathcal U \Rightarrow R_Q(\hat\theta) \le \text{the objective}", 40)],
            [r"chapters 5--6 needed a model", r"minimize the worst case", r"operations research", r"a certificate"],
            colors=[(1, FIXC)])

    def balls(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The choice of set is the whole art. <bookmark mark='b'/> A divergence ball: distributions "
            "whose density ratio to the training distribution is not too far from one, in chi-square or Kullback–Leibler "
            "divergence. These reweight the training points but cannot move them. <bookmark mark='c'/> A Wasserstein ball: "
            "distributions reachable by moving the training points a limited total distance. These can move points to "
            "places never seen. <bookmark mark='d'/> Group DRO, from Shiori Sagawa and co-authors in 2020: the mixtures of a "
            "few known subpopulations, so the objective is the worst group's risk.",
            [(r"\text{the set}", r":", r"\text{the modelling choice}", 40),
             (r"\phi\text{-divergence}", r":", r"\{Q: D_\phi(Q \,\|\, \hat P_n) \le \rho\}: \ \text{reweight}", 38),
             (r"\text{Wasserstein}", r":", r"\{Q: W(Q, \hat P_n) \le \rho\}: \ \text{move}", 38),
             (r"\text{group}", r":", r"\max_g R_g(\theta): \ \text{the worst subgroup}", 38)],
            [r"what to guard against", r"Namkoong \& Duchi", r"Esfahani \& Kuhn (2018)", r"Sagawa et al. (2020)"],
            colors=[(1, FIXC), (2, TGTC), (3, DEPTHC)])

    def duality(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A supremum over distributions sounds intractable, but convex duality makes it a few "
            "scalars. <bookmark mark='b'/> For the chi-square ball, with small radius, the worst case is the mean loss plus a "
            "multiple of its standard deviation: <bookmark mark='c'/> DRO is variance regularization, as John Duchi and "
            "Hongseok Namkoong showed, and it penalizes models whose losses are uneven across the data. <bookmark mark='d'/> "
            "For the Kullback–Leibler ball, the dual is a one-dimensional minimization over a temperature lambda, of an "
            "exponentially tilted mean: the worst case upweights the largest losses exponentially.",
            [(r"\text{duality}", r":", r"\sup_Q \to \inf \text{ over a scalar}", 40),
             (r"\chi^2", r":", r"\sup_Q E_Q[\ell] = \bar\ell + \sqrt{2\rho\,\widehat{\mathrm{Var}}(\ell)}", 40),
             (r"\text{so}", r":", r"\text{variance regularization}", 40),
             (r"\text{KL}", r":", r"\inf_{\lambda > 0}\ \lambda\rho + \lambda\log \hat E\, e^{\ell/\lambda}", 40)],
            [r"convex duality", r"small $\rho$, \ no clipping", r"Duchi \& Namkoong (2019)", r"exponential tilting"],
            colors=[(2, FIXC)])

    def groups(self):
        d = load("dro")
        g, r = d["groups"], d["grisk"]
        self.lad_voiceover(
            f"<bookmark mark='a'/> An example. Fit a regression of systolic pressure on sex and body-mass index, using only "
            f"NHANES adults under forty. <bookmark mark='b'/> Its mean squared error on the young, in units of ten millimetres "
            f"squared, is {say(r[0], 2)}. <bookmark mark='c'/> Applied to adults of forty to fifty-nine, it is {say(r[1], 2)}. "
            f"<bookmark mark='d'/> At sixty to eighty, it is {say(r[2], 2)}: more than seven times the training error, because "
            f"pressure rises with age and the young-trained model never learned it.",
            [(r"\text{model}", r":", r"\text{SBP on sex and BMI, \ fit on ages 18--39}", 40),
             (r"\text{ages } 18\text{--}39", r":", rf"\text{{MSE}} = {r[0]:.2f}", 40),
             (r"\text{ages } 40\text{--}59", r":", rf"\text{{MSE}} = {r[1]:.2f}", 40),
             (r"\text{ages } 60\text{--}80", r":", rf"\text{{MSE}} = {r[2]:.2f}", 40)],
            [r"NHANES", r"in-distribution", r"a moderate shift", r"a large one"],
            colors=[(2, BADC), (3, NAIVEC)])

    def chart(self):
        d = load("dro")
        rh, c2, kl, gr = np.asarray(d["rhos"]), np.asarray(d["chi2"]), np.asarray(d["kl"]), d["grisk"]
        A = axes([0, 1.0], [0, 14.0], x_length=7.4, y_length=4.4, xlabel=r"radius $\rho$ of the ball", ylabel=r"certified risk",
                 xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 4, 8, 12], center=[-2.5, 0.2, 0])
        ax = A.ax
        l_c2 = VGroup(polyline(ax, rh, c2, FIXC, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=FIXC) for a, b in zip(rh, c2)])
        l_kl = VGroup(polyline(ax, rh, kl, DEPTHC, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=DEPTHC) for a, b in zip(rh, kl)])
        hl = [DashedLine(ax.c2p(0, v), ax.c2p(1.0, v), color=c, stroke_width=2) for v, c in zip(gr, [GREY_B, BADC, NAIVEC])]
        k1, k2 = float(np.interp(gr[1], kl, rh)), float(np.interp(gr[2], kl, rh))
        q1 = float(np.interp(gr[1], c2, rh))
        side = side_groups([
            [(rf"grey: \ training risk, \ {gr[0]:.2f}", GREY_B)],
            [(r"green: \ the $\chi^2$ ball's worst case", FIXC)],
            [(r"purple: \ the KL ball's worst case", DEPTHC)],
            [(r"orange, \ red: \ the true risks", BADC), (r"at ages 40--59 and 60--80", BADC)],
            [(rf"KL certifies 40--59 at $\rho \approx {k1:.2f}$", GREY_A), (rf"and 60--80 at $\rho \approx {k2:.2f}$", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The worst-case risk, from fifteen hundred training losses, as the radius grows. At radius "
            f"zero it is the training risk. <bookmark mark='b'/> The chi-square ball's worst case, in green, grows like the "
            f"square root of the radius. <bookmark mark='c'/> The Kullback–Leibler ball's, in purple, grows faster: it can "
            f"pile weight on the largest losses. <bookmark mark='d'/> The dashed lines are the true risks for the older "
            f"groups. <bookmark mark='e'/> A Kullback–Leibler radius of about {say(k1, 2)} certifies the middle group's risk, "
            f"and about {say(k2, 2)} the oldest group's; the chi-square ball needs {say(q1, 2)} for the middle group. Without "
            f"knowing the target, a radius is a statement of how large a shift one is willing to insure."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"NHANES; \ dual computations exact")))
            vo.wait_until("a")
            self.play(Create(hl[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(l_c2), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(l_kl), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(hl[1]), Create(hl[2]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def wasserstein(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The Wasserstein ball has its own duality, from Peyman Mohajerin Esfahani and Daniel Kuhn, "
            "and from Jose Blanchet and Karthyek Murthy. <bookmark mark='b'/> For a loss that is Lipschitz in the data, the "
            "worst case adds the radius times the Lipschitz constant: <bookmark mark='c'/> for linear regression, it is a norm "
            "penalty on the coefficients: Blanchet, Kang and Murthy showed that the square-root lasso is exactly a "
            "Wasserstein-robust regression. <bookmark "
            "mark='d'/> And adversarial training, which perturbs each input within a small ball, is a Wasserstein DRO in "
            "the infinity-Wasserstein distance: Part sixty-four's robust networks start here.",
            [(r"\text{duality}", r":", r"\text{Esfahani \& Kuhn (2018); \ Blanchet \& Murthy (2019)}", 38),
             (r"\text{Lipschitz loss}", r":", r"\sup_{W \le \rho} E_Q[\ell] \le E_{\hat P}[\ell] + \rho\,\mathrm{Lip}(\ell)", 38),
             (r"\text{linear models}", r":", r"\text{a norm penalty: \ regularization is robustness}", 38),
             (r"\text{adversarial training}", r":", r"\text{perturb each input within } \varepsilon", 38)],
            [r"two routes", r"transport the points", r"Part 32's penalties", r"Part 64"],
            colors=[(2, FIXC)])

    def price(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The price is pessimism. <bookmark mark='b'/> A large set protects against shifts that will "
            "never happen, and the robust model is worse on the training distribution; the radius is rarely known. <bookmark "
            "mark='c'/> Divergence balls guard against reweighting but are blind to genuinely new regions, and Weihua Hu "
            "and co-authors showed in 2018 that for classification, DRO with a divergence ball can return the same "
            "classifier as ordinary training. <bookmark mark='d'/> So the set should carry knowledge: known groups, plausible "
            "directions of change, or, as the next chapter shows, the causal structure.",
            [(r"\text{price}", r":", r"\text{pessimism}", 40),
             (r"\text{radius}", r":", r"\text{rarely known}", 40),
             (r"\text{divergence balls}", r":", r"\text{may change nothing for 0--1 loss}", 40),
             (r"\text{better}", r":", r"\text{a set built from knowledge}", 40)],
            [r"insurance costs", r"a tuning parameter", r"Hu et al. (2018)", r"chapter 8"],
            colors=[(2, NAIVEC), (3, FIXC)])

    def fairness(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The age example is also a fairness example: the model serves the group it was trained on, "
            "and fails the others. <bookmark mark='b'/> Tatsunori Hashimoto and co-authors showed in 2018 that ordinary "
            "training can make it worse over time: a minority that is served badly leaves, its share of the data shrinks, "
            "and the model serves it worse still. <bookmark mark='c'/> A chi-square DRO, which needs no group labels, "
            "upweights whoever has large losses, and so protects every group above a minimum size. <bookmark mark='d'/> "
            "Robustness to shift and fairness to subgroups are the same mathematics: Part sixty-three returns to it.",
            [(r"\text{the age model}", r":", r"\text{good for the young, \ bad for the old}", 40),
             (r"\text{feedback}", r":", r"\text{poorly served groups leave, \ and shrink}", 40),
             (r"\chi^2 \text{ DRO}", r":", r"\text{protects all groups above a size}", 40),
             (r"\text{so}", r":", r"\text{shift robustness} = \text{subgroup fairness}", 40)],
            [r"a disparity", r"Hashimoto et al. (2018)", r"no demographics needed", r"Part 63"],
            colors=[(2, FIXC)])
