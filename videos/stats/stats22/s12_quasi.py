from __future__ import annotations

import numpy as np

from videos.stats.stats22.common import *  # noqa: F403


def lattice_grid(L, size=3.6, center=ORIGIN, up=None, down=None):
    L = np.asarray(L)
    n = L.shape[0]
    c = size / n
    g = VGroup()
    for i in range(n):
        for j in range(n):
            g.add(Square(side_length=c, stroke_width=0, fill_opacity=1,
                         fill_color=(up or BLUE) if L[i, j] > 0 else (down or GREY_E)).move_to([(j - n / 2 + 0.5) * c, (n / 2 - i - 0.5) * c, 0]))
    frame = Square(side_length=size, stroke_color=GREY_B, stroke_width=1.5)
    return VGroup(g, frame).move_to(center)


class Quasi(VoiceoverScene):
    def construct(self):
        self.card()
        self.quasi()
        self.lattices()
        self.constant()
        self.pseudo()
        self.estimates()
        self.composite()

    def card(self):
        card = chapter_card(11, r"Quasi-, \ composite and pseudo-likelihood", r"When the full likelihood is too much", lit=(1975,), part=PART)
        with self.voiceover("Chapter eleven. Quasi-likelihood, composite likelihood and pseudo-likelihood."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def quasi(self):
        d = load("sandwich")
        rows = [
            cmath(r"\text{assume only}", r":", r"E\,y = \mu(\beta), \ \ \mathrm{Var}\,y = \phi\, V(\mu)", font_size=30),
            cmath(r"\textstyle\sum_i \dfrac{y_i - \mu_i}{\phi V(\mu_i)}\, \dfrac{\partial \mu_i}{\partial \beta}", r"=", r"0", font_size=30),
            cmath(r"\hat\phi", r"=", rf"\tfrac{{1}}{{n - p}} \textstyle\sum (y_i - \hat\mu_i)^2 / V(\hat\mu_i) = {d['phi']:.2f}", font_size=30),
            cmath(r"\mathrm{SE}_{\text{quasi}}", r"=", rf"\sqrt{{\hat\phi}} \times \mathrm{{SE}}_{{\text{{Poisson}}}} = {d['se_quasi'][1]:.4f}", font_size=30),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"a mean and a variance function, \ no distribution"), why(r"Wedderburn (1974): \ the score, \ without a likelihood"),
                why(r"chapter ten's counts: \ Pearson's dispersion"), why(r"the same $\hat\beta$, \ honest SEs")]
        with self.voiceover(
            "Chapter ten fixed the standard errors after the fact. Robert Wedderburn's quasi-likelihood, from 1974, builds the "
            "doubt in from the start. <bookmark mark='a'/> Assume only how the mean depends on the covariates, and that the "
            "variance is some multiple phi of a known function of the mean. No distribution at all. <bookmark mark='b'/> Then "
            "solve the equations a likelihood's score would give: residuals, weighted by the variance, times the derivative of "
            "the mean. For counts they're exactly the Poisson equations, so the estimates are the same. "
            "<bookmark mark='c'/> Estimate phi from the Pearson residuals: two point two two for chapter ten's counts. "
            "<bookmark mark='d'/> Multiply the Poisson standard errors by its square root, and they come out close to the "
            "sandwich. The generalized estimating equations of Part 24 carry the same idea to correlated data."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lattices(self):
        d = load("ising")
        a = lattice_grid(d["lattice"], 4.4, [-3.3, 0.3, 0], up=TEAL)
        b = lattice_grid(d["lattice_strong"], 4.4, [3.3, 0.3, 0], up=TEAL)
        la = label(rf"$\beta = {d['beta']}$: \ patches", font_size=24, color=TEAL).next_to(a, DOWN, buff=0.25)
        lb = label(r"$\beta = 0.6$: \ almost all one way", font_size=24, color=TEAL).next_to(b, DOWN, buff=0.25)
        top = label(r"the Ising model: \ $P(x) \propto \exp\big(\beta \sum_{i \sim j} x_i x_j\big)$, \ $x_i = \pm 1$",
                    font_size=26).to_edge(UP, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> Here's a model whose likelihood can't even be written down in practice: the Ising model, "
            "from physics, used in statistics for images and spatial data. Each site of a grid is plus or minus one, and the "
            "probability of a pattern grows with beta times the number of neighbouring pairs that agree. "
            "<bookmark mark='b'/> With beta at point three, a forty-eight by forty-eight lattice drawn by Gibbs sampling shows "
            "small patches. <bookmark mark='c'/> At point six, past the critical value near point four four, almost every site "
            "agrees: the lattice has magnetized."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(top))
            vo.wait_until("b")
            self.play(FadeIn(a), FadeIn(la), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(b), FadeIn(lb), run_time=1.5)
        self.clear_scene()

    def constant(self):
        d = load("ising")
        rows = [
            cmath(r"P(x;\beta)", r"=", r"\exp\big(\beta S(x)\big) / Z(\beta)", font_size=30),
            cmath(r"Z(\beta)", r"=", r"\textstyle\sum_{\text{all } x} \exp\big(\beta S(x)\big)", font_size=30),
            cmath(r"\text{all } x", r":", rf"2^{{{d['sites']}}} \approx 10^{{{int(d['sites'] * np.log10(2))}}} \ \text{{patterns}}", font_size=30),
            cmath(r"\text{the likelihood}", r":", r"\text{one number per } \beta, \ \text{and it cannot be computed}", font_size=28),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"$S$: \ the number of agreeing neighbours, \ minus disagreeing"), why(r"the normalizing constant"),
                why(r"the atoms in the universe, \ $10^{80}$, \ to the eighth power"), why(r"MCMC can approximate it: \ slowly")]
        with self.voiceover(
            "<bookmark mark='a'/> The trouble is the normalizing constant. The probability of a pattern is the exponential of "
            "beta times its agreement score, divided by Z. <bookmark mark='b'/> Z is the sum of that exponential over every "
            "possible pattern. <bookmark mark='c'/> On our lattice that's two to the two thousand three hundred and four, about "
            "ten to the six hundred and ninety-three patterns. <bookmark mark='d'/> So the likelihood is a perfectly well "
            "defined function of beta that nobody can evaluate. Monte Carlo can approximate it, slowly."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pseudo(self):
        rows = [
            cmath(r"P(x_i \mid \text{the rest})", r"=", r"P(x_i \mid \text{4 neighbours}) = \dfrac{1}{1 + e^{-2\beta x_i s_i}}", font_size=30),
            cmath(r"\mathrm{PL}(\beta)", r"=", r"\textstyle\prod_i P(x_i \mid x_{\partial i};\beta)", font_size=30),
            cmath(r"\text{maximize}", r":", r"\text{a logistic regression of each site on its neighbours}", font_size=28),
            cmath(r"\text{consistent}", r":", r"\text{yes; \ less efficient than the full MLE}", font_size=30),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"$s_i$: \ the sum of the neighbours; \ $Z$ cancels"), why(r"Besag (1975): \ not a likelihood of anything"),
                why(r"seconds, \ by Newton"), why(r"its SEs need the sandwich")]
        with self.voiceover(
            "<bookmark mark='a'/> Julian Besag's way out, in 1975. A single site, given all the others, depends only on its "
            "four neighbours, and that conditional probability is a simple logistic function: the constant Z cancels. "
            "<bookmark mark='b'/> Multiply these conditionals over all sites. The product isn't the likelihood of anything, "
            "because the factors aren't independent, but it's a function of beta we can compute. <bookmark mark='c'/> "
            "Maximizing it is just a logistic regression of each site on its neighbour sum. <bookmark mark='d'/> The estimate "
            "is consistent, a little less efficient than the full maximum likelihood estimate, and its standard error needs "
            "chapter ten's sandwich, since the pseudo-likelihood's curvature doesn't equal its score's variance."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def estimates(self):
        d = load("ising")
        est = np.asarray(d["est"])
        A = axes([0.25, 0.35], [0, 13], x_length=8.0, y_length=4.0, xlabel=r"pseudo-likelihood estimate of $\beta$",
                 xticks=[0.25, 0.275, 0.3, 0.325, 0.35], yticks=[], center=[-1.6, 0.6, 0], xfmt=lambda v: f"{v:.3f}".rstrip("0"))
        ax = A.ax
        truth = DashedLine(ax.c2p(0.3, 0), ax.c2p(0.3, 13), color=TRUE, stroke_width=2.5)
        dots = VGroup(*[Dot(ax.c2p(v, k + 1), radius=0.08, color=PATH) for k, v in enumerate(est)])
        rows = fit_rows(VGroup(
            label(rf"{len(est)} lattices, \ $\beta = 0.3$, \ {d['sites']:,} sites each", font_size=22),
            label(rf"mean {d['est_mean']:.3f}, \ SD {d['est_sd']:.3f}", font_size=22, color=PATH),
            label(r"each fit: \ well under a second", font_size=22, color=GREY_A),
            label(r"the full likelihood: \ $10^{693}$ terms", font_size=22, color=RES),
        ), 3.45, 0.45, [5.1, 0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Does it work? Twelve independent lattices drawn with beta at point three. "
            "<bookmark mark='b'/> The pseudo-likelihood estimates average point two nine nine, with a spread of point oh one "
            "three: right on target. <bookmark mark='c'/> Each takes a fraction of a second. <bookmark mark='d'/> The full "
            "likelihood would need a sum of ten to the six hundred and ninety-three terms."
        ) as vo:
            self.play(FadeIn(A), Create(truth))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in dots], lag_ratio=0.15), FadeIn(rows[1]))
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def composite(self):
        rows = [
            cmath(r"\text{composite}", r":", r"\textstyle\prod_k L_k(\theta), \ \ \text{each a real likelihood of a piece}", font_size=28),
            cmath(r"\text{pairwise}", r":", r"\textstyle\prod_{i < j} f(y_i, y_j;\theta)", font_size=30),
            cmath(r"\mathrm{Cov}(\hat\theta)", r"\approx", r"H^{-1} J H^{-1}", font_size=30),
            cmath(r"\text{tests}", r":", r"\text{LR is no longer } \chi^2; \ \text{adjust it}", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"Lindsay (1988)"), why(r"spatial extremes, \ genetics, \ long time series"),
                why(r"Godambe's sandwich: \ chapter ten again"), why(r"Varin, \ Reid \& Firth (2011)")]
        with self.voiceover(
            "<bookmark mark='a'/> Pseudo-likelihood is one member of a family Bruce Lindsay named composite likelihood in 1988: "
            "multiply together likelihoods of pieces of the data, each a genuine likelihood, ignoring their dependence. "
            "<bookmark mark='b'/> Pairwise likelihoods, for instance, use only the joint density of each pair of observations, "
            "which makes models for spatial extremes and statistical genetics feasible. <bookmark mark='c'/> The estimates are "
            "consistent, and their covariance is a sandwich, the Godambe information. <bookmark mark='d'/> Likelihood-ratio "
            "tests need adjusting too, since the pieces' dependence breaks Wilks. The lesson of chapters ten and eleven: "
            "estimating equations can come from anywhere; the sandwich tells you how well they did."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
