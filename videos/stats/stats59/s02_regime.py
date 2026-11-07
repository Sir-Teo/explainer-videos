from __future__ import annotations

import numpy as np

from videos.stats.stats59.common import *  # noqa: F403


class Regime(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter one. The proportional regime: what changes when p grows with n, and what takes the "
                            "place of the old answers.", 1, r"The proportional regime", r"$p/n \to \kappa$", lit=(2019,))
        self.scaling()
        self.ols()
        self.mp_chart()
        self.mp_law()
        self.table()
        self.null_worked()
        self.existence()
        self.universality()

    def scaling(self):
        heading = label('The proportional regime and model assumptions', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> The proportional regime lets n and p grow together, with their ratio kappa fixed. "
            "<bookmark mark='b'/> The signal is scaled so that the linear predictor stays of order one: not every "
            "coefficient large, but their total effect fixed. <bookmark mark='c'/> Then each estimated coordinate "
            'has error of order one, in the right units, and the empirical distribution of the errors over '
            "coordinates has a limit. <bookmark mark='d'/> The answers are deterministic numbers, solutions of "
            'fixed-point equations, that depend only on kappa, the signal strength, and the model.'
        ),
            [(r"n, p \to \infty", r",", r"\ p/n \to \kappa \in (0, 1)", 40),
             (r"\mathrm{Var}(x'\beta)", r"\to", r"\gamma^2: \ \text{the signal stays of order one}", 38),
             (r"\frac1p\textstyle\sum_j \delta_{(\beta_j, \hat\beta_j)}", r"\Rightarrow", r"\text{a limit law}", 38),
             (r"\text{answers}", r":", r"\text{fixed points of equations in } \kappa, \gamma", 38)],
            [r"the regime", r"the right scaling", r"coordinates as a population", r"exact, \ not rates"],
            colors=[(0, PROPC), (3, PROPC)])

    def ols(self):
        heading = label('Gaussian least squares: finite-n mean error', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> The simplest case is exact at every n. For least squares with Gaussian covariates "
            'and noise variance sigma squared, the expected squared error of the coefficient vector is sigma '
            "squared times p over n minus p minus one. <bookmark mark='b'/> As a function of kappa, that is sigma "
            "squared kappa over one minus kappa: <bookmark mark='c'/> a fifth as many variables as observations "
            "inflates each coordinate's variance by a quarter, not by nothing; half as many doubles it. <bookmark "
            "mark='d'/> And as kappa approaches one the error explodes: the design becomes singular, which "
            'ridgeless regression will cross in chapter three.'
        ),
            [(r"E\|\hat\beta - \beta\|^2", r"=", r"\sigma^2\,\frac{p}{n - p - 1}", 40),
             (r"\to", r"\;", r"\sigma^2\,\frac{\kappa}{1 - \kappa}", 40),
             (r"\kappa = 0.2, \ 0.5", r":", r"\text{each coordinate's variance} \times 1.25, \ \times 2", 38),
             (r"\kappa \to 1", r":", r"\infty: \ \text{the design becomes singular}", 38)],
            [r"inverse Wishart", r"the proportional limit", r"not negligible", r"chapter 3 crosses it"],
            colors=[(1, PROPC), (3, CLASSC)])

    def mp_chart(self):
        d = load("mp")
        ev = np.asarray(d["ev"])
        edges = np.linspace(0, 3.2, 49)
        A = axes([0, 3.2], [0, 1.0], x_length=7.4, y_length=4.4, xlabel=r"eigenvalue of $X'X/n$", ylabel=r"density",
                 xticks=[0, 1, 2, 3], yticks=[0, 0.5, 1.0], center=[-2.5, 0.2, 0])
        ax = A.ax
        h = histogram(ax, ev, edges, density=True, color=SIMC, opacity=0.55)
        mp = polyline(ax, d["xs"], d["dens"], RMTC, 4)
        one = DashedLine(ax.c2p(1, 0), ax.c2p(1, 1.0), color=CLASSC, stroke_width=3)
        a, b = d["edges"]
        side = fit_rows(VGroup(
            label(rf"$n = {d['n']:,}$, \ $p = {d['p']:,}$: \ $\kappa = {d['gamma']:.1f}$; \ true covariance $I$", font_size=22),
            label(r"red: \ the truth, \ every eigenvalue 1", font_size=22, color=CLASSC),
            label(rf"blue: \ the sample's, \ from {d['min']:.2f} to {d['max']:.2f}", font_size=22, color=SIMC),
            label(rf"teal: \ Marchenko--Pastur, \ edges $(1 \mp \sqrt\kappa)^2 = {a:.2f}, \ {b:.2f}$", font_size=22, color=RMTC),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Where the trouble comes from. Two thousand observations of a thousand independent variables, "
            f"each with variance one. <bookmark mark='b'/> The true covariance matrix is the identity: every eigenvalue is one. "
            f"<bookmark mark='c'/> The sample covariance's eigenvalues spread from {say(d['min'], 2)} to {say(d['max'], 2)}. "
            f"<bookmark mark='d'/> Their histogram approximates the limiting Marchenko–Pastur law, with edges at one minus and one "
            f"plus root kappa, squared. Inverting such a matrix amplifies its smallest eigenvalues, and that is where the "
            f"inflation comes from."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(one), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(h, lag_ratio=0.03), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(mp), FadeIn(side[3]), run_time=2.0)
        self.clear_scene()

    def mp_law(self):
        heading = label('The MP law for ratio below one', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> The Marchenko–Pastur law of 1967 is the proportional regime's first exact answer. "
            'For a sample covariance with identity truth and ratio kappa, the eigenvalue distribution converges to '
            'a law supported between one minus root kappa squared and one plus root kappa squared. <bookmark '
            "mark='b'/> Its density is the square root of the product of the distances to the two edges, over two "
            "pi kappa x. <bookmark mark='c'/> Its mean is one, but the mean of one over the eigenvalues is one over "
            "one minus kappa. <bookmark mark='d'/> That is exactly the least-squares inflation of the last ladder: "
            'the trace of the inverse sample covariance, divided by p.'
        ),
            [(r"\text{support}", r":", r"[(1 - \sqrt\kappa)^2, \ (1 + \sqrt\kappa)^2]", 40),
             (r"\text{density}", r"=", r"\frac{\sqrt{(b - x)(x - a)}}{2\pi\kappa x}", 40),
             (r"\int x^{-1}\,d\mu_{\mathrm{MP}}", r"=", r"\frac{1}{1 - \kappa}", 40),
             (r"\Rightarrow", r"\;", r"\text{the OLS inflation, \ as a trace}", 40)],
            [r"Marchenko \& Pastur (1967)", r"Part 52", r"mean of the inverse", r"one law, \ two facts"],
            colors=[(2, RMTC), (3, PROPC)])

    def table(self):
        d = load("table")
        rows = [r for r in d["rows"] if r["gamma2"] == 5.0]
        hdr = [r"$\kappa = p/n$", r"$\alpha_\star$ \ (bias)", r"$\sigma_\star$", r"$\lambda_\star$", r"LRT factor $\kappa\sigma_\star^2/\lambda_\star$"]
        body = []
        for r in rows:
            if r["ok"]:
                body.append([f"{r['kappa']:g}", f"{r['alpha']:.3f}", f"{r['sigma']:.3f}", f"{r['lam']:.3f}", f"{r['factor']:.3f}"])
            else:
                body.append([f"{r['kappa']:g}", r"---", r"---", r"---", r"outside finite-MLE regime" if r.get("status", "").startswith("above") else r"numerical solve failed"])
        tab = table_rows([hdr] + body, font_size=26, col_buff=0.7, row_buff=0.25, colors=[GREY_B] + [WHITE] * len(body)).move_to([0, 0.6, 0])
        foot = fit_rows(VGroup(
            label(r"the Sur--Cand\`es system, \ solved by root finding with bivariate Gauss--Hermite quadrature; \ $\gamma^2 = 5$", font_size=24, color=GREY_A),
            label(r"checked against the paper: \ $\kappa = 0.1$ gives $(1.1678, \ 3.3466, \ 0.9605)$ and factor $1.1660$", font_size=24, color=PROPC),
        ), 12.4, 0.22, [0, -2.5, 0])
        with self.voiceover(
            (
            "<bookmark mark='a'/> The whole picture, from Sur and Candès's system of three equations in alpha, "
            "sigma and lambda, solved here by root finding with Gauss–Hermite quadrature. <bookmark mark='b'/> The "
            'bias alpha, the noise level sigma, and the likelihood-ratio factor all grow with kappa: at a '
            'twentieth, the factor is about one point oh seven; at a quarter it is one point eight four. <bookmark '
            "mark='c'/> These numbers match the paper's, to four decimals, where it reports them. <bookmark "
            "mark='d'/> At kappa three tenths the improved solver finds alpha about three point zero seven four and "
            'LRT factor about two point nine five two. The old solver failed here, but that was a numerical '
            'failure: three tenths lies below the theoretical existence boundary.'
        )
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(exact_tag(r"exact: \ quadrature and root finding")))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:-1]], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(tab[-1]))
        self.clear_scene()

    def existence(self):
        d = load("table")
        ex = {round(e["gamma"], 3): e["kappa_max"] for e in d["exist"]}
        g5 = ex[round(math.sqrt(5), 3)]
        heading = label('An asymptotic phase boundary, not a solver status', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            f"<bookmark mark='a'/> When does the MLE exist at all? If the cases and controls can be separated perfectly by a "
            f"hyperplane, the likelihood has no maximum. <bookmark mark='b'/> Thomas Cover's 1965 counting says that with no "
            f"signal, random points in p dimensions become separable once p exceeds n over two. <bookmark mark='c'/> Candès "
            f"and Sur found the boundary for every signal strength: kappa must be below the minimum over t of the expected "
            f"positive part of Z minus t V, squared. <bookmark mark='d'/> With no signal that is a half; with gamma squared "
            f"five it is {say(g5, 3)}, so three tenths is still inside the asymptotic existence region. At the boundary itself a separate analysis is needed.",
            [(r"\text{separable data}", r":", r"\text{no MLE}", 40),
             (r"\gamma = 0", r":", r"\text{separable once } \kappa > 1/2", 40),
             (r"\text{the boundary}", r":", r"\kappa < h(\gamma) = \min_t E(Z - tV)_+^2", 40),
             (r"h(0), \ h(\sqrt5)", r"=", rf"{ex[0.0]:.3f}, \ \ {g5:.3f}", 40)],
            [r"perfect separation", r"Cover (1965)", r"Cand\`es \& Sur (2020)", r"computed here"],
            colors=[(2, PROPC), (3, PROPC)])

    def universality(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> Each theorem has its own design assumptions. <bookmark mark='b'/> The original "
            'logistic example uses independent Gaussian covariates. Some universality results extend particular '
            'limiting laws to specified independent non-Gaussian designs, with moment and signal conditions. '
            "Matching two moments alone is not a universal theorem. <bookmark mark='c'/> Coordinate-distribution "
            "results require appropriate empirical signal convergence and moment control. <bookmark mark='d'/> "
            'Zhao, Sur and Candes extend logistic coefficient inference to arbitrary nonsingular Gaussian '
            'covariance, using conditional predictor variances. Arbitrary non-Gaussian correlation requires more '
            "justification. <bookmark mark='e'/> The biopsy example is a semi-synthetic stress test outside the "
            'Gaussian theorem, not evidence that its coverage guarantee automatically transfers.'
        ),
            [('Assumptions of proportional-regime asymptotics', GREY_A),
             (r"Gaussian theorem; \ specified universality extensions need conditions", PROPC),
             (r"a spread signal: \ no single coefficient dominates", PROPC),
             (r"correlated Gaussian inference uses conditional predictor scales", CLASSC),
             (r"chapter 9: \ a real design", AMPC)], head_size=36)

    def null_worked(self):
        heading = label('Global-null logistic calibration', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> A worked case at the global null, where no coefficient matters and the system has "
            "two equations. <bookmark mark='b'/> At kappa a fifth, sigma star is 2.85 and lambda star 1.28, so the "
            "likelihood-ratio factor is a fifth times 2.85 squared over 1.28, about 1.27. <bookmark mark='c'/> A "
            "test at the textbook's five percent level then uses the cutoff 3.84, while the right cutoff is 1.27 "
            "times 3.84, about 4.87. <bookmark mark='d'/> The true size of the textbook test is the chance that "
            '1.27 times a chi-squared exceeds 3.84: about eight percent, not five.'
        ),
            [('\\gamma = 0, \\ \\kappa = 0.2', ':', '\\sigma_\\star = 2.85, \\ \\lambda_\\star = 1.28', 40),
             ('\\text{factor}', '=', '0.2 \\times 2.85^2/1.28 \\approx 1.27', 40),
             ('\\text{right cutoff}', '=', '1.27 \\times 3.84 \\approx 4.87', 40),
             ('\\text{textbook size}', '=', 'P(\\chi^2_1 > 3.84/1.27) \\approx 8\\%', 40)],
            ['the two-equation system', 'computed', 'rescaled', 'too many rejections'],
            colors=[(3, CLASSC)])
