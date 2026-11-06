from __future__ import annotations

import numpy as np

from videos.stats.stats33.common import *  # noqa: F403


class Efron(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_groups()
        self.fdr_defs()
        self.data()
        self.hist()
        self.lindsey()
        self.curve()
        self.empirical_null()
        self.counts()
        self.lesson()

    def card(self):
        card = chapter_card(5, r"Empirical Bayes", r"Efron's local false discovery rate", lit=(1995, 2001), part=PART)
        with self.voiceover("Chapter five. Empirical Bayes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def two_groups(self):
        rows = [
            cmath(r"z_i", r"\sim", r"f(z) = \pi_0 f_0(z) + \pi_1 f_1(z)", font_size=32),
            cmath(r"f_0", r"=", r"N(0, 1): \ \text{the theoretical null}", font_size=32),
            cmath(r"P(\text{null} \mid z)", r"=", r"\pi_0 f_0(z) / f(z) = \mathrm{fdr}(z)", font_size=32),
            cmath(r"P(\text{null} \mid Z \ge z)", r"=", r"\pi_0 S_0(z)/S(z) = \mathrm{Fdr}(z)", font_size=30),
        ]
        rows[2][-1].set_color(BHC)
        whys = [why(r"the two-groups model"), why(r"$z = \Phi^{-1}(F(t))$"), why(r"Bayes's rule: \ the local fdr"),
                why(r"tail areas: \ BH's quantity")]
        with self.voiceover(
            "<bookmark mark='a'/> Bradley Efron recast the problem as Part 25's empirical Bayes. Each test statistic, turned "
            "into a z-value, comes either from the null, with probability pi zero and density f zero, or from the "
            "alternative, with density f one. <bookmark mark='b'/> The null density is the standard normal. "
            "<bookmark mark='c'/> Then by Bayes's rule, the probability that a gene with this exact z-value is null is pi "
            "zero f zero over f: the local false discovery rate. <bookmark mark='d'/> The same ratio with tail areas is the "
            "tail-area false discovery rate, which BH estimates."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fdr_defs(self):
        rows = [
            cmath(r"f(z)", r":", r"\text{estimated from all } N \text{ z-values at once}", font_size=30),
            cmath(r"\pi_0 f_0", r":", r"\text{known up to } \pi_0 \le 1", font_size=32),
            cmath(r"\widehat{\mathrm{fdr}}(z)", r"=", r"\hat\pi_0 f_0(z) / \hat f(z)", font_size=32),
            cmath(r"\text{report}", r":", r"\text{genes with } \widehat{\mathrm{fdr}} < 0.2", font_size=32),
        ]
        rows[2][-1].set_color(BHC)
        whys = [why(r"thousands of cases: \ the density is learnable"), why(r"or conservatively 1"),
                why(r"empirical Bayes"), why(r"Efron's convention")]
        with self.voiceover(
            "<bookmark mark='a'/> The point is that with thousands of genes, the mixture density f can be estimated directly "
            "from the data. <bookmark mark='b'/> The null part is known up to pi zero, which can be taken as one to be safe. "
            "<bookmark mark='c'/> Their ratio estimates the local false discovery rate of each gene, <bookmark mark='d'/> "
            "and Efron's convention is to report genes whose local fdr is below point two."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def data(self):
        d = load("prostate")
        rows = fit_rows(VGroup(
            label(r"Singh et al. (2002): \ 6{,}033 genes, \ 50 healthy men and 52 with prostate cancer", font_size=26),
            label(r"for each gene, \ a two-sample $t$ with 100 df, \ turned into a $z$-value", font_size=26, color=BHC),
            label(r"Efron's running example in \emph{Large-Scale Inference} (2010)", font_size=26, color=GREY_A),
            label(rf"{d['n_z3']} genes have $|z| > 3$; \ about {d['exp_z3']:.0f} expected by chance", font_size=26, color=SIGC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Real data: Dinesh Singh and colleagues' prostate cancer microarray of 2002, six thousand "
            "and thirty-three genes measured on fifty healthy men and fifty-two with cancer. <bookmark mark='b'/> Each gene "
            "gets a two-sample t statistic, converted to a z-value through its distribution with a hundred degrees of "
            "freedom. <bookmark mark='c'/> These are Efron's running example in his book on large-scale inference. "
            "<bookmark mark='d'/> Ninety genes have z beyond three in size, where chance alone would give about sixteen."
        ) as vo:
            self.add(prostate_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def hist(self):
        d = load("prostate")
        mids, counts, w = np.asarray(d["mids"]), np.asarray(d["counts"]), d["width"]
        A = axes([-4.6, 5.4], [0, 330], x_length=8.4, y_length=4.4, xlabel=r"$z$", ylabel=r"genes per bin",
                 xticks=[-4, -2, 0, 2, 4], yticks=[0, 100, 200, 300], center=[-1.4, 0.3, 0])
        ax = A.ax
        edges = np.r_[mids - w / 2, mids[-1] + w / 2]
        bars = hist_bars(ax, edges, counts, color=BHC, opacity=0.6)
        nullc = curve(ax, mids, d["N"] * w * np.asarray(d["f0_theo"]), NULLC, 3)
        rows = fit_rows(VGroup(
            label(r"blue: \ the 6{,}033 $z$-values", font_size=22, color=BHC),
            label(r"grey: \ $N \cdot \phi(z)$, \ the theoretical null", font_size=22, color=NULLC),
            label(r"heavier tails than the null: \ the signals", font_size=22, color=SIGC),
        ), 3.4, 0.42, [5.3, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The histogram of the six thousand z-values. <bookmark mark='b'/> In grey, what six thousand "
            "standard normals would give. <bookmark mark='c'/> The bulk matches closely, but both tails are heavier than the "
            "null curve: that excess is where the differentially expressed genes are."
        ) as vo:
            self.add(prostate_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.01), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(nullc), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def lindsey(self):
        rows = [
            cmath(r"y_k", r"=", r"\#\{z_i \text{ in bin } k\} \sim \text{Poisson}(\nu_k)", font_size=30),
            cmath(r"\log \nu_k", r"=", r"\textstyle\sum_{j=0}^{7} \beta_j x_k^j", font_size=32),
            cmath(r"\hat f(z)", r"=", r"\hat\nu(z) / (N \Delta)", font_size=32),
            cmath(r"\text{smooth}", r":", r"\text{a GLM, \ Part 24, \ on 90 bin counts}", font_size=30),
        ]
        rows[1][-1].set_color(BHC)
        whys = [why(r"bin the $z$-values"), why(r"Lindsey's method"), why(r"$\Delta$: \ the bin width"),
                why(r"fast and stable")]
        with self.voiceover(
            "<bookmark mark='a'/> To estimate f, Efron uses Lindsey's method: bin the z-values and treat each bin's count as "
            "Poisson. <bookmark mark='b'/> Model the log of its mean as a smooth function of the bin centre, here a "
            "polynomial of degree seven. <bookmark mark='c'/> The fitted means, rescaled, estimate the density. "
            "<bookmark mark='d'/> It is just a Poisson GLM from Part 24, on ninety counts, so it is fast and stable."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curve(self):
        d = load("prostate")
        mids = np.asarray(d["mids"])
        fdr = np.asarray(d["fdr_t"])
        A = axes([-4.6, 5.4], [0, 1.05], x_length=8.4, y_length=4.4, xlabel=r"$z$", ylabel=r"$\widehat{\mathrm{fdr}}(z)$",
                 xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.2, 0.5, 1], center=[-1.4, 0.3, 0])
        ax = A.ax
        c = curve(ax, mids, fdr, BHC, 3.5)
        thr = DashedLine(ax.c2p(-4.6, 0.2), ax.c2p(5.4, 0.2), color=SIGC, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"theoretical null $N(0, 1)$", font_size=22),
            label(rf"$\hat\pi_0 = {d['pi0_t']:.3f}$", font_size=22, color=NULLC),
            label(r"near 1 in the middle", font_size=22, color=BHC),
            label(rf"{d['n_fdr20_t']} genes with fdr $< 0.2$", font_size=22, color=SIGC),
        ), 3.4, 0.42, [5.3, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The estimated local false discovery rate, with the theoretical null. "
            "<bookmark mark='b'/> pi zero is estimated at point nine five four. <bookmark mark='c'/> In the middle, a gene is "
            "almost surely null; the curve falls away in both tails. <bookmark mark='d'/> Fifty-one genes "
            "have local fdr below point two."
        ) as vo:
            self.add(prostate_tag())
            self.play(FadeIn(A), Create(thr))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def empirical_null(self):
        d = load("prostate")
        rows = [
            cmath(r"N(0, 1)", r":", r"\text{right only if every null test is exactly calibrated}", font_size=28),
            cmath(r"\text{in practice}", r":", r"\text{correlation, \ batch effects, \ unobserved covariates}", font_size=28),
            cmath(r"\text{central matching}", r":", r"\text{fit } N(\delta_0, \sigma_0^2) \text{ to the middle of the histogram}", font_size=28),
            cmath(r"\text{prostate}", r":", rf"\delta_0 = {d['delta0']:.3f}, \ \sigma_0 = {d['sigma0']:.3f}", font_size=32),
        ]
        rows[3][-1].set_color(BHC)
        whys = [why(r"the theoretical null"), why(r"widen or shift the real null"), why(r"Efron (2004): \ the empirical null"),
                why(r"4\% wider than $N(0, 1)$")]
        with self.voiceover(
            "<bookmark mark='a'/> Efron's most important observation is about the null itself. The standard normal is the "
            "right null only if every null test is exactly calibrated. <bookmark mark='b'/> In real studies, correlation "
            "between genes, batch effects and unmeasured covariates can widen or shift the distribution of null z-values. "
            "<bookmark mark='c'/> His remedy is the empirical null: since most genes are null, fit a normal curve to the "
            "middle of the histogram and use that as f zero. <bookmark mark='d'/> For the prostate data it is centred at "
            "zero but four percent wider than the standard normal."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def counts(self):
        d = load("prostate")
        hdr = [r"\textbf{prostate, \ 6,033 genes}", r"\textbf{discoveries}"]
        body = [[r"Bonferroni, \ $\alpha = 0.05$", str(d["bonf"])],
                [r"BH, \ $q = 0.1$ \ (theoretical null)", str(d["bh10"])],
                [r"local fdr $< 0.2$, \ theoretical null", str(d["n_fdr20_t"])],
                [r"local fdr $< 0.2$, \ empirical null", str(d["n_fdr20_e"])]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.2, row_buff=0.32, colors=[GREY_A, FWC, BHC, BHC, SIGC])
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"a 4\% wider null halves the list", font_size=22, color=SIGC),
            label(r"the choice of null matters more than the choice of procedure", font_size=22, color=FALSEC),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The consequences. Bonferroni finds two genes. BH at ten percent finds fifty-nine. Local fdr "
            "below point two with the theoretical null finds fifty-one. With the empirical null, only twenty-seven. "
            "<bookmark mark='b'/> A null just four percent wider halves the list, <bookmark mark='c'/> which is Efron's "
            "point: in large-scale inference, the choice of null distribution matters more than the choice of procedure."
        ) as vo:
            self.add(prostate_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"with thousands of tests, \ the data estimate their own null", font_size=26, color=BHC),
            label(r"the local fdr gives each gene its own posterior probability of being null", font_size=26),
            label(r"BH's tail-area FDR is the average local fdr over the rejected genes", font_size=26, color=SIGC),
            label(r"Part 25's borrowing of strength, \ for hypothesis testing", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> With thousands of parallel tests, the data can estimate their own null distribution. "
            "<bookmark mark='b'/> The local fdr gives each gene its own posterior probability of being null, <bookmark mark='c'/> "
            "and BH's tail-area rate is just the average of the local fdr over the genes it rejects. <bookmark mark='d'/> It "
            "is Part 25's idea of borrowing strength, applied to testing."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
