from __future__ import annotations

import numpy as np

from videos.stats.stats63.common import *  # noqa: F403


class Definition(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter one. Differential privacy: a promise about any one person, against any attacker.", 1,
                            r"Differential privacy", r"A promise about the process", lit=(2006,))
        self.definition()
        self.meaning()
        self.response()
        self.laplace()
        self.gaussian()
        self.chart()
        self.properties()
        self.limits()

    def definition(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Differential privacy compares neighboring datasets under a specified adjacency relation. They may differ by adding or removing one person, or by replacing one record at fixed sample size; sensitivity must match that choice. <bookmark mark='b'/> A mechanism is epsilon-private when, for every neighboring pair and every output event, one output probability is at most e to epsilon times the other. The reverse holds by symmetry. <bookmark mark='c'/> Approximate privacy adds delta to this event inequality. Delta is an additive probability slack, not in general the probability of a data-independent switch into an unprotected mode. <bookmark mark='d'/> Small epsilon and delta limit the additional evidence supplied by a release about the chosen neighboring alternatives. They do not promise secrecy of facts already inferable without this record.",
            [(r"D \sim D'", r":", r"\text{differ in one person}", 40),
             (r"P(M(D) \in S)", r"\le", r"e^{\varepsilon} \, P(M(D') \in S)", 40),
             (r"(\varepsilon, \delta)\text{-DP}", r":", r"P(M(D) \in S) \le e^{\varepsilon} P(M(D') \in S) + \delta", 38),
             (r"\varepsilon", r":", r"\text{the privacy-loss budget}", 40)],
            [r"neighbours", r"Dwork, \ McSherry, \ Nissim \& Smith (2006)", r"approximate DP", r"small is private"],
            colors=[(1, PRIVC)])

    def meaning(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The Bayesian reading is precise for two fixed neighboring alternatives, with the other records held fixed. <bookmark mark='b'/> Under pure epsilon privacy, the likelihood ratio multiplies prior odds by a factor between e to minus epsilon and e to epsilon. This is not a universal bound on learning every correlated secret under an arbitrary prior over whole databases. <bookmark mark='c'/> The mechanism's guarantee continues to hold in the presence of auxiliary information, including the other records; no list of possible linkage keys is needed. <bookmark mark='d'/> Its object is the incremental effect of this record under the stated adjacency. Population patterns and correlations can remain highly informative.",
            [(r"\text{attacker}", r":", r"\text{any prior, \ any side knowledge}", 40),
             (r"\text{posterior odds}", r"\le", r"e^{\varepsilon} \times \text{prior odds}", 40),
             (r"\text{so}", r":", r"\text{no list of quasi-identifiers}", 40),
             (r"\text{protects}", r":", r"\text{the effect of participating}", 40)],
            [r"worst case", r"fixed neighboring alternatives; pure DP", r"auxiliary information allowed", r"not secrecy of facts"],
            colors=[(1, PRIVC)])

    def response(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The oldest private mechanism is older than the definition. Stanley Warner proposed it in "
            "1965 for embarrassing survey questions. <bookmark mark='b'/> Each respondent answers truthfully with probability "
            "pi, and gives the opposite answer otherwise. The ratio of the chances of any report, under a true yes and a true "
            "no, is pi over one minus pi, so the mechanism is differentially private with epsilon the log of that ratio. A "
            "fair coin deciding between the truth and a second coin toss gives pi of three quarters, and epsilon the log of "
            "three. <bookmark mark='c'/> The analyst still learns the population's proportion: the expected fraction of yes "
            "reports is a known linear function of the true one, and inverting it gives an unbiased estimate. <bookmark "
            "mark='d'/> The price is variance: dividing by two pi minus one inflates it.",
            [(r"\text{Warner (1965)}", r":", r"\text{embarrassing questions}", 40),
             (r"\text{report the truth w.p.}", r"\ ", r"\pi = e^{\varepsilon}/(1 + e^{\varepsilon})", 40),
             (r"\hat p", r"=", r"\frac{\hat q - (1 - \pi)}{2\pi - 1}", 40),
             (r"\mathrm{Var}(\hat p)", r"=", r"\frac{q(1 - q)}{n (2\pi - 1)^2}", 40)],
            [r"randomized response", r"$\varepsilon = \log 3$ for $\pi = 3/4$", r"unbiased", r"the price"],
            colors=[(2, OKC), (3, BADC)])

    def laplace(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> For a numerical statistic, the noise is calibrated to its sensitivity, the most that one "
            "person's record can change it. A count has sensitivity one. <bookmark mark='b'/> The Laplace mechanism adds noise "
            "with a two-sided exponential density, of scale sensitivity over epsilon. <bookmark mark='c'/> Why it works: the "
            "ratio of the output's densities under two neighbours is e to the minus epsilon times the distance from one "
            "centre, over e to the minus epsilon times the distance from the other. By the triangle inequality the ratio is "
            "at most the exponential of sensitivity divided by the scale, which is e to epsilon. <bookmark mark='d'/> "
            "For a count at epsilon one the noise has standard deviation about 1.4: invisible in a national total, fatal in "
            "a block of three people.",
            [(r"\Delta f", r"=", r"\max_{D \sim D'} |f(D) - f(D')|", 40),
             (r"M(D)", r"=", r"f(D) + \mathrm{Laplace}(\Delta f / \varepsilon)", 40),
             (r"\frac{p_D(z)}{p_{D'}(z)}", r"=", r"e^{\varepsilon(|z - f(D')| - |z - f(D)|)/\Delta f} \le e^{\varepsilon}", 40),
             (r"\text{a count}, \ \varepsilon = 1", r":", r"\mathrm{sd} = \sqrt{2} \approx 1.4", 40)],
            [r"sensitivity", r"the Laplace mechanism", r"the triangle inequality", r"absolute, \ not relative, \ error"],
            colors=[(1, PRIVC)])

    def gaussian(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Gaussian noise is more natural for a statistician, and it adds up better, but it needs the "
            "slack delta, because the Gaussian's tails make the density ratio unbounded far out. <bookmark mark='b'/> The "
            "textbook calibration, from Dwork and Roth, takes sigma equal to the square root of two log of 1.25 over delta, "
            "times the sensitivity, over epsilon, for epsilon below one. <bookmark mark='c'/> Borja Balle and Yu-Xiang Wang "
            "computed in 2018 the exact delta of the Gaussian mechanism at every epsilon, an expression in two normal "
            "distribution functions. Solving it for sigma gives the analytic Gaussian mechanism. <bookmark mark='d'/> The "
            "exact calculation needs less noise for the same guarantee.",
            [(r"\text{Gaussian}", r":", r"f(D) + N(0, \sigma^2) \ \text{needs } \delta > 0", 40),
             (r"\sigma_{\text{classic}}", r"=", r"\sqrt{2 \log(1.25/\delta)} \, \Delta / \varepsilon", 40),
             (r"\delta(\varepsilon)", r"=", r"\Phi\!\left(\tfrac{\Delta}{2\sigma} - \tfrac{\varepsilon\sigma}{\Delta}\right) - e^{\varepsilon}\Phi\!\left(-\tfrac{\Delta}{2\sigma} - \tfrac{\varepsilon\sigma}{\Delta}\right)", 34),
             (r"\sigma_{\text{analytic}}", r":", r"\text{the smallest } \sigma \text{ with } \delta(\varepsilon) \le \delta", 40)],
            [r"unbounded ratios", r"Dwork \& Roth (2014)", r"Balle \& Wang (2018)", r"exact, \ so smaller"],
            colors=[(3, OKC)])

    def chart(self):
        d = load("mechanisms")
        eps = np.asarray(d["eps"])
        lx = np.log10(eps)
        A = axes([-1.1, 0.4], [-0.3, 1.8], x_length=7.2, y_length=4.3, xlabel=r"$\varepsilon$ (log scale)",
                 ylabel=r"noise standard deviation for a count (log scale)", xticks=[-1, np.log10(0.25), np.log10(0.5), 0, np.log10(2)],
                 xfmt=lambda v: f"{10 ** v:.2g}", yticks=[-0.3, 0, 1, np.log10(30)], yfmt=lambda v: f"{10 ** v:.2g}", center=[-2.4, 0.2, 0])
        ax = A.ax
        lap = VGroup(polyline(ax, lx, np.log10(d["laplace_sd"]), RAWC, 3.5),
                     *[Dot(ax.c2p(a, np.log10(b)), radius=0.07, color=RAWC) for a, b in zip(lx, d["laplace_sd"])])
        k = eps <= 1.0
        cla = VGroup(polyline(ax, lx[k], np.log10(np.asarray(d["classic"])[k]), BADC, 3.5),
                     *[Dot(ax.c2p(a, np.log10(b)), radius=0.07, color=BADC) for a, b in zip(lx[k], np.asarray(d["classic"])[k])])
        ana = VGroup(polyline(ax, lx, np.log10(d["analytic"]), OKC, 3.5),
                     *[Dot(ax.c2p(a, np.log10(b)), radius=0.07, color=OKC) for a, b in zip(lx, d["analytic"])])
        i1 = list(d["eps"]).index(1.0)
        side = side_groups([
            [(r"one count, \ sensitivity 1", WHITE), (r"$\delta = 10^{-5}$ for the Gaussians", GREY_A)],
            [(r"blue: \ Laplace, \ pure $\varepsilon$-DP", RAWC)],
            [(rf"red: \ classic Gaussian, \ {d['classic'][i1]:.2f} at $\varepsilon = 1$", BADC), (r"classic small-$\varepsilon$ sufficient calibration", BADC)],
            [(rf"green: \ analytic Gaussian, \ {d['analytic'][i1]:.2f}", OKC), (r"the same guarantee", OKC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The noise each mechanism needs for one count, against epsilon, on log scales, with delta of "
            f"one in a hundred thousand for the Gaussians. <bookmark mark='b'/> The Laplace mechanism's standard deviation "
            f"is root two over epsilon: a straight line of slope minus one. <bookmark mark='c'/> The classic Gaussian "
            f"calibration needs {d['classic'][i1]:.2f} at epsilon one, the edge of its validity. <bookmark mark='d'/> The "
            f"analytic calibration needs {d['analytic'][i1]:.2f} for exactly the same guarantee, about a quarter less, and it "
            f"stays valid for larger epsilon. Loose bounds cost accuracy, and this part keeps meeting that lesson."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lap[0]), FadeIn(VGroup(*lap[1:])), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cla[0]), FadeIn(VGroup(*cla[1:])), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ana[0]), FadeIn(VGroup(*ana[1:])), FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def properties(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Three properties make the definition usable. <bookmark mark='b'/> Post-processing: "
            "anything computed from a private output, without going back to the data, is exactly as private. Rounding, "
            "clipping, fitting a model to noisy counts: all free. <bookmark mark='c'/> Composition: releasing k outputs with "
            "budgets epsilon one to epsilon k is private with their sum. Every statistic published spends from one budget. "
            "<bookmark mark='d'/> Group privacy: a group of k people is protected with k times epsilon, so a household, or a "
            "family in a genetic study, gets weaker protection than one person.",
            [(r"\text{three properties}", r":", r"\text{post-processing, \ composition, \ groups}", 40),
             (r"g(M(D))", r":", r"\text{as private as } M(D)", 40),
             (r"(M_1, \dots, M_k)", r":", r"\textstyle\sum_j \varepsilon_j", 40),
             (r"\text{a group of } k", r":", r"k\varepsilon", 40)],
            [r"why it is usable", r"post-processing", r"basic composition", r"group privacy"],
            colors=[(2, PRIVC)])

    def limits(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What it does not promise. <bookmark mark='b'/> A study that shows smoking causes cancer "
            "teaches the world something about every smoker, including those not in it. Differential privacy permits that: "
            "it protects against harms caused by participating, not against what the data reveal about populations. "
            "<bookmark mark='c'/> It also says nothing about which epsilon is small enough. Values from a tenth to ten are "
            "used in practice, and the meaning of e to the ten is weak. <bookmark mark='d'/> And non-numeric outputs, such as "
            "choosing the best of several options, need other mechanisms: McSherry and Talwar's exponential mechanism picks "
            "an option with probability growing exponentially in its quality.",
            [(r"\text{not promised}", r":", r"\text{secrecy of population facts}", 40),
             (r"\text{smoking and cancer}", r":", r"\text{learned without you}", 40),
             (r"\varepsilon", r":", r"\text{a policy choice, \ } 0.1 \text{ to } 10", 40),
             (r"\text{exponential mechanism}", r":", r"P(r) \propto e^{\varepsilon q(D, r) / 2\Delta q}", 40)],
            [r"the limits", r"Dwork \& Roth's example", r"chapter 6", r"McSherry \& Talwar (2007)"],
            colors=[(2, BADC)])
