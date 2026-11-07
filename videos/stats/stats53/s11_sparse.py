from __future__ import annotations

import numpy as np

from videos.stats.stats53.common import *  # noqa: F403


class SparseBayes(VoiceoverScene):
    def construct(self):
        self.card()
        self.priors()
        self.shrinkage()
        self.globallocal()
        self.coverage()
        self.computation()
        self.board()
        self.lesson()

    def card(self):
        card = chapter_card(10, r"High-dimensional Bayes", r"Spike-and-slab and the horseshoe", lit=(2015,), part=PART)
        with self.voiceover("Chapter ten. High-dimensional Bayes: the spike-and-slab and the horseshoe."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def priors(self):
        rows = [
            cmath(r"y_i = \theta_i + \varepsilon_i", r":", r"n \text{ means, \ } s \text{ of them non-zero}", font_size=34),
            cmath(r"\text{spike-and-slab}", r":", r"\theta_i \sim w\,\mathrm{Slab} + (1 - w)\delta_0, \ \ w \sim \mathrm{Beta}(1, n)", font_size=32),
            cmath(r"\text{rate}", r":", r"s\log(n/s): \ \text{squared radius; suitable size prior and slab conditions}", font_size=34),
            cmath(r"\text{horseshoe}", r":", r"\theta_i \sim N(0, \lambda_i^2\tau^2), \ \lambda_i \sim C^+(0, 1), \ \tau\asymp s/n\text{ in the stated sparse regime}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(PRIORC)
        whys = [why(r"Part 52's problem, \ Bayesian"), why(r"a Beta mixing prior; \ not a blanket contraction guarantee"), why(r"Castillo, \ Schmidt-Hieber \& vdV (2015)"), why(r"Carvalho, \ Polson \& Scott (2010)")]
        heading = label('Sparse contraction needs a suitable size prior, slab and scale', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The sparse normal means problem of Part fifty, from a Bayesian side: n means, s of them non-zero. <bookmark mark='b'/> The spike-and-slab prior makes each mean exactly zero with probability one minus w, and draws it from a heavy-tailed slab otherwise, with w itself given a Beta prior that favours sparsity. <bookmark mark='c'/> Ismaël Castillo, Johannes Schmidt-Hieber and Aad van der Vaart proved in 2015 that suitably scaled heavy-tailed slabs and model-size priors yield squared Euclidean contraction radius of order s log of n over s in the normal-means problem, with regression requiring design and noise scaling conditions. Our fixed-Gaussian-slab demonstration is not that uniform theorem. <bookmark mark='d'/> The horseshoe of Carlos Carvalho, Nicholas Polson and James Scott is a continuous alternative: normal with a half-Cauchy local scale and a global scale tau of about the sparsity proportion. Stéphanie van der Pas, Bas Kleijn and van der Vaart showed in 2014 that suitable global-scale choices attain the minimax squared-error order in the stated sparse regimes."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def shrinkage(self):
        from explainer.stats.kit import bnp as BN

        y = np.linspace(-7, 7, 141)
        tau = 0.1
        from videos.stats.stats53.compute import horseshoe_posterior
        hs = np.array([horseshoe_posterior(float(v),tau)["mean"] for v in y])
        w = 0.1
        l1 = np.log(w) + np.log(np.exp(-0.5 * y ** 2 / (1 + 9)) / np.sqrt(10))
        l0 = np.log(1 - w) + np.log(np.exp(-0.5 * y ** 2))
        incl = 1 / (1 + np.exp(l0 - l1))
        ss = incl * 0.9 * y
        A = axes([-7, 7], [-7, 7], x_length=6.0, y_length=4.6, xlabel=r"observation $y$", ylabel=r"posterior mean",
                 xticks=[-6, -3, 0, 3, 6], yticks=[-6, -3, 0, 3, 6], center=[-2.8, 0.2, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(-7, -7), ax.c2p(7, 7), color=GREY_C, stroke_width=2)
        ch = polyline(ax, y, hs, PRIORC, 4)
        cs = polyline(ax, y, ss, BALLC, 4)
        side = fit_rows(VGroup(
            label(r"posterior mean of $\theta$ against $y$", font_size=22),
            label(r"grey: \ no shrinkage", font_size=22, color=GREY_C),
            label(r"gold: \ spike-and-slab, \ $w = 0.1$, \ $N(0, 9)$ slab", font_size=22, color=BALLC),
            label(r"purple: \ horseshoe, \ $\tau = 0.1$", font_size=22, color=PRIORC),
            label(r"Gaussian slab keeps 10\% shrinkage even for very large $y$", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How the two priors shrink one observation. <bookmark mark='b'/> Without shrinkage the "
            "estimate is the observation itself. <bookmark mark='c'/> The spike-and-slab's posterior mean, in gold, is nearly "
            "zero for small observations, then rises steeply as the probability of a signal jumps. <bookmark mark='d'/> The "
            "horseshoe, in purple, does the same smoothly: its half-Cauchy scale lets large observations escape almost "
            "untouched. <bookmark mark='e'/> Both behave like thresholding rules, the Bayesian versions of Part fifty's."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact, \ by quadrature")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(diag), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ch), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def globallocal(self):
        rows = [
            cmath(r"\theta_i \sim N(0, \lambda_i^2\tau^2)", r":", r"\text{the global-local family}", font_size=34),
            cmath(r"\tau", r":", r"\text{global: \ how sparse; \ estimated, \ or } \sim C^+", font_size=34),
            cmath(r"\lambda_i", r":", r"\text{local: \ heavy-tailed, \ so signals escape}", font_size=34),
            cmath(r"\text{examples}", r":", r"\text{horseshoe, \ Dirichlet--Laplace, \ R2-D2, \ the Bayesian lasso}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Polson \& Scott (2010)"), why(r"empirical or full Bayes"), why(r"a pole at zero, \ fat tails"), why(r"Bhattacharya et al. (2015)")]
        heading = label('A global sparsity scale and local scales control shrinkage', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The horseshoe is one member of a family, Nicholas Polson and James Scott's global-local scale mixtures. <bookmark mark='b'/> A global scale tau sets the overall sparsity, estimated or given its own half-Cauchy prior. <bookmark mark='c'/> A local scale for each coordinate, with heavy tails, lets genuine signals escape the shrinkage. <bookmark mark='d'/> The Dirichlet–Laplace prior of Anirban Bhattacharya and colleagues, the R2-D2 prior, and the Bayesian lasso of Part thirty-two are other members; the lasso's light Laplace tails are why it shrinks large signals too much."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def coverage(self):
        d = load("hdbayes")
        order = ["zero", "small", "intermediate", "large"]
        rows = [[r"signal $\theta_i$"] + [f"{d['strengths'][g]:g}" for g in order],
                [r"spike-and-slab \ 95\% interval"] + [f"{100 * d['coverage']['slab'][g]:.0f}\\%" for g in order],
                [r"horseshoe \ 95\% interval"] + [f"{100 * d['coverage']['hs'][g]:.0f}\\%" for g in order]]
        tab = table_rows(rows, font_size=30, col_buff=0.8, row_buff=0.45, colors=[GREY_B, BALLC, PRIORC])
        tab.move_to([0, 0.9, 0])
        foot = label(rf"$n = {d['n']}$: \ 360 zeros, \ 10 at 1, \ 10 at 2.5, \ 20 at 6; \ {d['reps']} data sets", font_size=24, color=GREY_A).move_to([0, -0.8, 0])
        foot2 = label(r"finite-sample coverage varies by signal size; \ small and intermediate signals: \ the intervals shrink them to zero and miss", font_size=24, color=BADC).move_to([0, -1.6, 0])
        c = d["coverage"]
        with self.voiceover(
            f"<bookmark mark='a'/> But do their credible intervals cover? Four hundred means: three hundred and sixty zeros, ten at one, ten at two and a half, twenty at six, and the marginal ninety-five percent intervals for each. In this finite experiment the zero-signal coverage is very high, while large-signal coverage can still be below ninety-five percent. But for the small signals, the spike-and-slab covers {100 * c['slab']['small']:.0f} percent and the horseshoe {100 * c['hs']['small']:.0f}; for the intermediate ones, {100 * c['slab']['intermediate']:.0f} and {100 * c['hs']['intermediate']:.0f}. <bookmark mark='b'/> Sixty independent data sets. The horseshoe uses the known sparsity proportion for its global scale and evaluates forty of the zero coordinates. Monte Carlo errors account for dataset-level grouping. <bookmark mark='c'/> Signals of intermediate size are shrunk towards zero, and the intervals around the shrunken estimates miss them. Van der Pas, Szabó and van der Vaart proved in 2017 that the horseshoe's intervals must fail there, and Richard Nickl and Sara van de Geer had shown in 2013 that honest adaptive confidence sets for sparse vectors are impossible in general."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def computation(self):
        rows = [
            cmath(r"\text{spike-and-slab}", r":", r"2^p \text{ models: \ Gibbs over inclusion indicators, \ slow mixing}", font_size=32),
            cmath(r"\text{EMVS, \ the spike-and-slab lasso}", r":", r"\text{continuous spikes: \ fast EM to the posterior mode}", font_size=30),
            cmath(r"\text{horseshoe}", r":", r"\text{Gibbs with auxiliary scales; \ NUTS in Stan}", font_size=34),
            cmath(r"\text{variational Bayes}", r":", r"\text{fast, \ but intervals too narrow \ (Ray \& Szabó 2022)}", font_size=32),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"George \& McCulloch (1993)"), why(r"Ročková \& George (2014, 2018)"), why(r"Makalic \& Schmidt (2016)"), why(r"a mean-field caveat")]
        heading = label('A posterior mode and an approximate posterior need different interpretation', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Computing these posteriors is its own problem. The spike-and-slab posterior lives on two to the p models, and Edward George and Robert McCulloch's Gibbs sampler over inclusion indicators can mix slowly. <bookmark mark='b'/> Veronika Ročková and George replaced the point mass with a narrow continuous spike, which allows a fast EM algorithm to the posterior mode, the spike-and-slab lasso. <bookmark mark='c'/> The horseshoe is sampled by Gibbs with auxiliary scale variables, or by the NUTS sampler of Part twenty-seven. <bookmark mark='d'/> And mean-field variational approximations are fast and estimate well, but Kolyan Ray and Botond Szabó showed that mean-field approximations can underestimate uncertainty; specific contraction theorems do not provide a universal calibration guarantee."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = board_rows("horseshoe")
        d = load("board")
        hs = [x for x in d["rows"] if "horseshoe" in x["method"]][0]
        show_board(self, rows,
                   f"<bookmark mark='a'/> On the Board: the horseshoe's interval for intermediate signals of two and a half "
                   f"covers {100 * hs['achieved']:.0f} percent. The prior that estimates sparse vectors at the minimax rate "
                   f"gives overconfident intervals for exactly the signals that are hardest to see.",
                   [("a", [0])])

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"the same pattern, \ again:", font_size=28, color=GREY_A),
            label(r"estimation: \ near-minimax under suitable prior and model conditions", font_size=26, color=GOODC),
            label(r"uncertainty: \ honest only for signals clearly zero or clearly large", font_size=26, color=BALLC),
            label(r"the intermediate zone is where selection decisions are made", font_size=26, color=BADC),
            label(r"the frequentist answer, \ the debiased lasso of Part 52, \ pays with wider intervals", font_size=26, color=FREQC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The same pattern as in the last chapter. <bookmark mark='b'/> For estimation, sparse priors are minimax, adaptive and nearly free. <bookmark mark='c'/> For uncertainty, their intervals are honest only for signals that are clearly zero or clearly large. <bookmark mark='d'/> Unfortunately, the intermediate zone is exactly where decisions about which variables matter are made. <bookmark mark='e'/> Part fifty-two's debiased lasso reduces shrinkage but can retain a bias remainder. Its coverage requires approximate-inverse and design assumptions; interval widths are not universally ordered."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
