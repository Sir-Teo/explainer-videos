from __future__ import annotations

import numpy as np

from videos.stats.stats63.common import *  # noqa: F403


class Accounting(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter three. Accountants: how privacy losses add up over many releases.", 3,
                            r"Accountants", r"Adding up the privacy loss", lit=(2016, 2017))
        self.loss()
        self.advanced()
        self.renyi()
        self.zcdp()
        self.chart()
        self.census()
        self.subsampling()

    def loss(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Privacy loss is the log likelihood ratio of a released output under a neighboring pair. <bookmark mark='b'/> Pure epsilon privacy bounds its absolute value by epsilon almost surely. Approximate privacy instead bounds suitable tail excesses. <bookmark mark='c'/> For independent releases, joint privacy loss is a sum. Adaptive releases also decompose into conditional losses, and composition theorems handle that dependence. <bookmark mark='d'/> Fluctuations can grow on a square-root scale, while the positive mean accumulates. Advanced composition therefore includes both a square-root term and a term proportional to k epsilon squared for small epsilon; square-root growth does not persist indefinitely at fixed per-step privacy.",
            [(r"L", r"=", r"\log \frac{p_D(M)}{p_{D'}(M)}", 40),
             (r"\varepsilon\text{-DP}", r":", r"|L| \le \varepsilon", 40),
             (r"k \text{ releases}", r":", r"L_1 + \cdots + L_k", 40),
             (r"\text{typically}", r":", r"\sqrt{k}\text{ fluctuations, plus accumulating mean}", 40)],
            [r"the privacy-loss variable", r"a bound", r"they add", r"Part 6's square root"],
            colors=[(3, OKC)])

    def advanced(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Cynthia Dwork, Guy Rothblum and Salil Vadhan turned that into the advanced composition "
            "theorem, in 2010. <bookmark mark='b'/> k releases, each epsilon-private, are together private with epsilon "
            "prime equal to the square root of two k log one over delta prime, times epsilon, plus k epsilon times e to the "
            "epsilon minus one, at the cost of an extra delta prime. <bookmark mark='c'/> For small epsilon per step the "
            "first term dominates: square root of k growth. <bookmark mark='d'/> But it is a Hoeffding bound, from Part "
            "fifty-one, applied to a worst case. When each step's epsilon is near one, the second term is larger than basic "
            "composition itself. Bounds that throw away the distribution of the loss pay for it.",
            [(r"\text{advanced}", r":", r"\varepsilon' = \sqrt{2k \log(1/\delta')}\,\varepsilon + k\varepsilon(e^{\varepsilon} - 1)", 38),
             (r"\delta_{\text{total}}", r"=", r"k\delta + \delta'", 40),
             (r"\text{small } \varepsilon", r":", r"\varepsilon' \approx \varepsilon\sqrt{2k\log(1/\delta')}", 40),
             (r"\varepsilon \approx 1", r":", r"\text{worse than basic}", 40)],
            [r"Dwork, \ Rothblum \& Vadhan (2010)", r"a slack", r"square-root growth", r"Part 51's Hoeffding"],
            colors=[(2, OKC), (3, BADC)])

    def renyi(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Ilya Mironov's Renyi differential privacy, of 2017, tracks the whole distribution of the "
            "loss through its moments. <bookmark mark='b'/> The Renyi divergence of order alpha between the output "
            "distributions, one over alpha minus one times the log of the expected likelihood ratio to the power alpha, is "
            "bounded by a function epsilon of alpha. <bookmark mark='c'/> For the Gaussian mechanism it is exactly alpha "
            "Delta squared over two sigma squared, and under composition the functions simply add. <bookmark mark='d'/> At "
            "the end, convert: the mechanism is epsilon-delta private with epsilon equal to the Renyi bound plus log one over "
            "delta over alpha minus one, minimized over alpha.",
            [(r"D_\alpha(P \| Q)", r"=", r"\tfrac{1}{\alpha - 1} \log E_Q[(dP/dQ)^\alpha]", 40),
             (r"\text{Gaussian}", r":", r"\varepsilon(\alpha) = \alpha\Delta^2 / 2\sigma^2", 40),
             (r"k \text{ releases}", r":", r"k\,\varepsilon(\alpha)", 40),
             (r"\varepsilon", r"=", r"\min_\alpha \ k\,\varepsilon(\alpha) + \tfrac{\log(1/\delta)}{\alpha - 1}", 40)],
            [r"Mironov (2017)", r"exact", r"additive", r"convert once"],
            colors=[(3, OKC)])

    def zcdp(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Mark Bun and Thomas Steinke's zero-concentrated privacy, from 2016, keeps one number. "
            "<bookmark mark='b'/> A mechanism is rho-zCDP if its Renyi divergence of every order alpha is at most rho "
            "alpha: a line through the origin. <bookmark mark='c'/> The Gaussian mechanism is exactly Delta squared over two "
            "sigma squared zCDP, and rhos add. <bookmark mark='d'/> The conversion: rho-zCDP implies epsilon-delta privacy "
            "with epsilon equal to rho plus two times the square root of rho log one over delta. This is the accountant the "
            "Census Bureau used.",
            [(r"\rho\text{-zCDP}", r":", r"D_\alpha \le \rho\alpha \ \ \text{for all } \alpha > 1", 40),
             (r"\text{Gaussian}", r":", r"\rho = \Delta^2 / 2\sigma^2", 40),
             (r"k \text{ releases}", r":", r"\rho_1 + \cdots + \rho_k", 40),
             (r"\varepsilon", r"=", r"\rho + 2\sqrt{\rho \log(1/\delta)}", 40)],
            [r"Bun \& Steinke (2016)", r"one number", r"additive", r"the census's accountant"],
            colors=[(3, OKC)])

    def chart(self):
        d = load("accounting")
        ks = np.log10(d["ks"])
        A = axes([0, 3.05], [-0.4, 3.6], x_length=7.2, y_length=4.4, xlabel=r"number of Gaussian releases $k$ (log scale)",
                 ylabel=r"total $\varepsilon$ at $\delta = 10^{-5}$ (log scale)", xticks=[0, 1, 2, 3], xfmt=lambda v: f"{10 ** v:g}",
                 yticks=[0, 1, 2, 3], yfmt=lambda v: f"{10 ** v:g}", center=[-2.4, 0.2, 0])
        ax = A.ax

        def line(key, color):
            ys = np.log10(d[key])
            return VGroup(polyline(ax, ks, ys, color, 3.5), *[Dot(ax.c2p(a, b), radius=0.07, color=color) for a, b in zip(ks, ys)])
        bas, adv, rdp = line("basic", GREY_A), line("advanced", BADC), line("rdp", OKC)
        side = side_groups([
            [(rf"each release: \ noise $\sigma = {d['sigma']:g}$, \ sensitivity 1", WHITE)],
            [(rf"grey: \ basic, \ {d['basic'][-1]:,.0f} at $k = 1{{,}}000$".replace(",0", "{,}0").replace("1,", "1{,}"), GREY_A),
             (rf"red: \ advanced, \ {d['advanced'][-1]:,.0f}".replace(",", "{,}"), BADC)],
            [(rf"green: \ R\'enyi, \ {d['rdp'][-1]:.1f}", OKC), (rf"zCDP: \ {d['zcdp'][-1]:.1f}", OKC)],
            [(rf"{d['basic'][-1] / d['rdp'][-1]:.0f} times smaller than basic", OKC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The accountants compared. Each release adds Gaussian noise of standard deviation "
            f"{d['sigma']:g} to a statistic of sensitivity one, and we ask for the total epsilon at delta of one in a hundred "
            f"thousand after k releases, on log scales. <bookmark mark='b'/> Basic composition grows like k, reaching "
            f"{d['basic'][-1]:,.0f} after a thousand releases. Advanced composition is worse here, "
            f"{d['advanced'][-1]:,.0f}, because each step's epsilon is near one. <bookmark mark='c'/> The Renyi accountant "
            f"gives {d['rdp'][-1]:.1f}, and zCDP essentially the same, {d['zcdp'][-1]:.1f}. <bookmark mark='d'/> Same "
            f"mechanism, same data, same guarantee asked for: an accounting {d['basic'][-1] / d['rdp'][-1]:.0f} times "
            f"tighter. For a single release, the exact calculation is still best; the gain is in composition."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(bas[0]), FadeIn(VGroup(*bas[1:])), Create(adv[0]), FadeIn(VGroup(*adv[1:])), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(rdp[0]), FadeIn(VGroup(*rdp[1:])), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def census(self):
        d = load("accounting")
        self.lad_voiceover(
            "<bookmark mark='a'/> The redistricting release's stated zCDP budget is rho 2.63, split into 2.56 for person tables and .07 for housing. Its protected neighboring universe must respect published invariants; exact state totals are outside that protection. <bookmark mark='b'/> The standard zCDP conversion at delta ten to minus ten gives epsilon about eighteen point two. <bookmark mark='c'/> That is a weak multiplicative worst-case bound, and the guarantee should be read with its adjacency and invariants. A large upper bound is not evidence that an actual attack attains it. <bookmark mark='d'/> For comparison only, a continuous Gaussian shift experiment with rho 2.63 has mu equal to root two rho, about 2.29, and power about .74 at five percent false positives. The real release uses discrete noise, hierarchy and post-processing. Rho-zCDP alone does not imply this exact GDP curve or this attack power for the census.",
            [(r"\rho_{2020}", r"=", r"2.63 \ \ (2.56 \text{ persons}, \ 0.07 \text{ housing})", 40),
             (r"\varepsilon \ (\delta = 10^{-10})", r"\approx", rf"{d['census_eps']:.1f}", 40),
             (r"e^{18}", r"\approx", r"6 \times 10^{7}", 40),
             (r"\mu = \sqrt{2\rho}", r"\approx", r"2.3: \ \text{power} \approx 0.74 \text{ at } \alpha = 0.05", 40)],
            [r"Abowd et al. (2022)", r"zCDP's conversion", r"nearly vacuous", r"Gaussian comparison only; not census GDP"],
            colors=[(1, BADC), (3, PRIVC)])

    def subsampling(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Subsampling can amplify privacy. <bookmark mark='b'/> When a person is selected secretly at random with probability q, suitable mechanisms and adjacency relations admit a smaller effective budget. Revealing batch membership can destroy that amplification. <bookmark mark='c'/> For Poisson subsampling under the relevant add/remove model, the pure epsilon expression is log of one plus q times e to epsilon minus one; it is approximately q epsilon when epsilon is small. Replacement and fixed-size sampling have different details. <bookmark mark='d'/> Abadi and colleagues' moments accountant tracks subsampled Gaussian training more tightly than basic composition. Modern numerical privacy-loss accountants can give certified bounds with discretization and truncation error control; an FFT by itself is not a proof of tightness.",
            [(r"\text{subsample}", r":", r"\text{each step sees a fraction } q", 40),
             (r"\text{amplification}", r":", r"\varepsilon \ \to \ \text{about } q\varepsilon", 40),
             (r"\text{moments accountant}", r":", r"\text{subsampled Gaussians}", 40),
             (r"\text{numerical}", r":", r"\text{the loss distribution by FFT}", 40)],
            [r"most steps miss you", r"small $\varepsilon$", r"Abadi et al. (2016)", r"certified numerical bounds"],
            colors=[(1, OKC)])
