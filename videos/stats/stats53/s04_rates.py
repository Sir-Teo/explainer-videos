from __future__ import annotations

import math

import numpy as np

from videos.stats.stats53.common import *  # noqa: F403


class Rates(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.model()
        self.chart()
        self.ball()
        self.ingredients()
        self.examples()
        self.lower()

    def card(self):
        card = chapter_card(3, r"Contraction rates", r"Prior mass, \ entropy and tests, \ quantified", lit=(2000,), part=PART)
        with self.voiceover("Chapter three. Contraction rates: prior mass, entropy and tests, quantified."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        rows = [
            cmath(r"\text{prior mass}", r":", r"\Pi\big(B_{KL}(p_0, \varepsilon_n)\big) \ge e^{-c\, n\varepsilon_n^2}", font_size=34),
            cmath(r"\text{entropy}", r":", r"\log N(\varepsilon_n, \mathcal P_n, d) \le n\varepsilon_n^2, \ \ \Pi(\mathcal P_n^c) \le e^{-(c + 4) n\varepsilon_n^2}", font_size=30),
            cmath(r"\text{GGV (2000)}", r":", r"\Pi\big(d(p, p_0) > M\varepsilon_n \mid X_{1:n}\big) \to 0", font_size=34),
            cmath(r"\text{read}", r":", r"n\varepsilon_n^2 \approx \text{the log of the prior's ``search space''}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Schwartz, \ at scale $\varepsilon_n$"), why(r"a sieve, \ with tests (Le Cam, \ Birgé)"), why(r"Ghosal, \ Ghosh \& van der Vaart"), why(r"the balance")]
        with self.voiceover(
            "<bookmark mark='a'/> Subhashis Ghosal, Jayanta Ghosh and Aad van der Vaart made Schwartz's theorem quantitative in "
            "2000. The first condition: the prior puts mass at least e to the minus c n epsilon squared on a Kullback–Leibler "
            "ball of radius epsilon n around the truth. <bookmark mark='b'/> The second: most of the prior's mass sits on a "
            "sieve whose covering number at scale epsilon n has logarithm at most n epsilon n squared, which guarantees tests "
            "by Le Cam's and Birgé's constructions. <bookmark mark='c'/> Then the posterior contracts at rate epsilon n: its "
            "mass outside a ball of radius a constant times epsilon n vanishes. <bookmark mark='d'/> The rate solves a balance: "
            "n epsilon squared is the logarithm of the size of the space the prior must search, as for the minimax rates of "
            "Part fifty."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def model(self):
        rows = [
            cmath(r"Y_k = \theta_k + n^{-1/2} Z_k", r":", r"\text{Part 50's sequence model, \ truth } \theta_0 \in S^\beta", font_size=32),
            cmath(r"\theta_k \sim N(0, k^{-1 - 2\alpha})", r":", r"\text{a Gaussian prior of smoothness } \alpha", font_size=32),
            cmath(r"\text{posterior}", r":", r"N\Big(\frac{n\lambda_k}{1 + n\lambda_k} Y_k, \ \frac{\lambda_k}{1 + n\lambda_k}\Big): \ \text{exact}", font_size=32),
            cmath(r"\varepsilon_n", r"\asymp", r"n^{-\min(\alpha, \beta)/(1 + 2\alpha)}: \ \text{minimax iff } \alpha = \beta", font_size=34),
        ]
        rows[2][-1].set_color(POSTC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"regression, \ densities, \ in disguise"), why(r"a Gaussian process prior"), why(r"conjugate"), why(r"Knapik et al. (2011)")]
        with self.voiceover(
            "<bookmark mark='a'/> A laboratory where everything is exact: Part fifty's Gaussian sequence model, with a truth "
            "of smoothness beta. <bookmark mark='b'/> Give the coefficients independent normal priors with variances k to the "
            "minus one minus two alpha: a Gaussian process prior whose sample paths have smoothness alpha. <bookmark "
            "mark='c'/> The posterior is conjugate, normal, coordinate by coordinate, and its risk can be computed exactly. "
            "<bookmark mark='d'/> Its contraction rate is n to the minus the smaller of alpha and beta, over one plus two "
            "alpha, as Bartek Knapik, Aad van der Vaart and Harry van Zanten found in 2011: minimax exactly when the prior's "
            "smoothness matches the truth's."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("rates")
        ln = np.log10(d["ns"])
        A = axes([1.9, 6.1], [-2.3, -0.5], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\log_{10}$ posterior-mean error",
                 xticks=[2, 3, 4, 5, 6], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[-2, -1.5, -1, -0.5], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"0.5": FREQC, "1.0": GOODC, "2.0": BADC}
        cs = {a: VGroup(polyline(ax, ln, 0.5 * np.log10([q["risk"] for q in v]), cols[a], 4),
                        *[Dot(ax.c2p(x, 0.5 * math.log10(q["risk"])), radius=0.06, color=cols[a]) for x, q in zip(ln, v)]) for a, v in d["rows"].items()}
        s, t = d["slopes"], d["theory"]
        side = fit_rows(VGroup(
            label(r"truth of smoothness $\beta = 1$", font_size=22),
            label(rf"green: \ $\alpha = 1$: \ slope {s['1.0']:.3f} \ (theory $-1/3$)", font_size=22, color=GOODC),
            label(rf"teal: \ $\alpha = 1/2$, \ rougher: \ {s['0.5']:.3f} \ ($-1/4$)", font_size=22, color=FREQC),
            label(rf"red: \ $\alpha = 2$, \ smoother: \ {s['2.0']:.3f} \ ($-1/5$)", font_size=22, color=BADC),
            label(r"matching the smoothness is optimal; \ both errors cost", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The exact errors of the posterior mean, for a truth of smoothness one, from a hundred to a "
            f"million observations. <bookmark mark='b'/> With a prior of the same smoothness, in green, the slope is "
            f"{say(s['1.0'], 3)}, the minimax minus a third. <bookmark mark='c'/> A rougher prior, smoothness a half, "
            f"undersmooths: slope {say(s['0.5'], 3)}, against the theory's minus a quarter. <bookmark mark='d'/> A smoother "
            f"prior, smoothness two, oversmooths and is slower still, {say(s['2.0'], 3)}, against minus a fifth. <bookmark "
            f"mark='e'/> Both mistakes cost a polynomial factor in the rate, which is why chapter eight lets the data choose "
            f"alpha."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact risk")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs["1.0"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs["0.5"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs["2.0"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def ball(self):
        from explainer.stats.kit import bnp as BN

        r = np.random.default_rng(53)
        K = 400
        th = BN.sobolev_truth(K, 1.0)
        lam = BN.prior_var(K, 1.0)
        panels = VGroup()
        texts = VGroup()
        for i, n in enumerate((100, 1000, 10000)):
            cb = ContractionBall(center=(-4.3 + 4.3 * i, 0.2, 0), scale=4.0, origin=(th[0], th[1]))
            Y = th + r.standard_normal(K) / math.sqrt(n)
            post = BN.posterior(Y, n, lam)
            pts = post["mean"][:2] + np.sqrt(post["var"][:2]) * r.standard_normal((150, 2))
            rad = 2.45 * math.sqrt(float(np.mean(post["var"][:2])))
            frame = Square(side_length=3.6, stroke_color=GREY_D, stroke_width=1.5).move_to(cb.c)
            g = VGroup(frame, cb.cloud(pts, color=POSTC), cb.ball(post["mean"][0], post["mean"][1], rad, color=BALLC),
                       cb.truth(th[0], th[1]))
            panels.add(g)
            texts.add(label(rf"$n = {n:,}$", font_size=26, color=GREY_A).next_to(frame, DOWN, buff=0.25))
        head = label(r"the contraction ball: \ posterior draws of $(\theta_1, \theta_2)$, \ the truth in white", font_size=26).to_edge(UP, buff=0.6)
        foot = label(r"the ball shrinks like $n^{-1/2}$ in each coordinate; \ the truth stays inside", font_size=24, color=GOODC).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "<bookmark mark='a'/> What contraction looks like, with this part's instrument, the contraction ball. Two "
            "coordinates of the parameter, posterior draws in blue, a ninety-five percent credible disc in gold, and the truth "
            "in white. <bookmark mark='b'/> At a hundred, a thousand and ten thousand observations, the cloud shrinks around "
            "the truth, and the disc keeps it inside. In the low coordinates the posterior behaves like a parametric one; "
            "the interesting failures happen in the high ones, where prior and data compete."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]), FadeIn(texts[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]), FadeIn(texts[1]))
            self.play(FadeIn(panels[2]), FadeIn(texts[2]), FadeIn(foot))
        self.wait(1.5)
        self.clear_scene()

    def lower(self):
        rows = [
            cmath(r"\text{can a posterior beat the minimax rate?}", r":", r"\text{not uniformly}", font_size=34),
            cmath(r"\text{if } \Pi(\cdot \mid X) \text{ contracts at } \varepsilon_n", r":", r"\text{its centre is an estimator with error } O(\varepsilon_n)", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\varepsilon_n \gtrsim \text{the minimax rate, \ over the model}", font_size=34),
            cmath(r"\text{so}", r":", r"\text{Part 50's lower bounds bind Bayesians too}", font_size=34),
        ]
        rows[3][-1].set_color(BALLC)
        whys = [why(r"the question"), why(r"Ghosal et al. (2000), \ Thm 2.5"), why(r"Le Cam, \ Fano, \ Assouad"), why(r"no free lunch")]
        with self.voiceover(
            "<bookmark mark='a'/> Can a posterior contract faster than the minimax rate? Not uniformly over a model. <bookmark mark='b'/> If a posterior contracts at a rate epsilon n, the centre of the smallest ball holding half its mass is an estimator that converges at the same rate. <bookmark mark='c'/> So epsilon n can be no faster than the minimax rate. <bookmark mark='d'/> Part fifty's lower bounds, by Le Cam, Fano and Assouad, bind Bayesians as much as anyone."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def examples(self):
        rows = [
            cmath(r"\text{DP mixtures of normals}", r":", r"\text{smooth densities at } n^{-1/2} \text{ up to logs, \ if supersmooth}", font_size=30),
            cmath(r"\text{location-scale DP mixtures}", r":", r"n^{-\beta/(2\beta+1)}\text{, \ adaptively \ (Shen, \ Tokdar \& Ghosal 2013)}", font_size=30),
            cmath(r"\text{random histograms}", r":", r"\text{a prior on the number of bins: \ adaptive rates}", font_size=32),
            cmath(r"\text{sparse priors}", r":", r"s\log(p/s)/n: \ \text{chapter 10}", font_size=34),
        ]
        rows[0][-1].set_color(POSTC)
        rows[1][-1].set_color(GOODC)
        whys = [why(r"Ghosal \& van der Vaart (2001)"), why(r"near-minimax"), why(r"Scricciolo; \ Rousseau"), why(r"Part 50's sparse rate")]
        with self.voiceover(
            "<bookmark mark='a'/> The theorem has been applied to almost every nonparametric prior. Subhashis Ghosal and Aad van der Vaart showed in 2001 that Dirichlet-process mixtures of normals estimate very smooth densities at nearly the parametric rate, one over root n up to logarithms. <bookmark mark='b'/> With a prior on the scale too, Weining Shen, Surya Tokdar and Ghosal showed in 2013 that they attain the minimax rate for every smoothness at once. <bookmark mark='c'/> Random histograms with a prior on the number of bins adapt in the same way. <bookmark mark='d'/> And sparse priors in high dimension contract at Part fifty's rate s log of p over s, over n, as chapter ten will show."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ingredients(self):
        rows = [
            cmath(r"\text{prior mass}", r"\leftrightarrow", r"\text{small-ball probability of the prior near } \theta_0", font_size=32),
            cmath(r"\text{entropy}", r"\leftrightarrow", r"\text{the complexity of where the prior puts its mass}", font_size=32),
            cmath(r"\text{too rough a prior}", r":", r"\text{mass spread thin: \ large entropy}", font_size=34),
            cmath(r"\text{too smooth a prior}", r":", r"\text{little mass near a rough } \theta_0: \ \text{small balls are improbable}", font_size=30),
        ]
        rows[2][-1].set_color(FREQC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"chapter 7's RKHS"), why(r"Part 48's covering numbers"), why(r"variance-like"), why(r"bias-like")]
        with self.voiceover(
            "<bookmark mark='a'/> The two conditions are a bias–variance trade-off in disguise. The prior-mass condition asks "
            "how probable a small ball around the truth is under the prior. <bookmark mark='b'/> The entropy condition asks "
            "how complex the region holding the prior's mass is. <bookmark mark='c'/> A prior that is too rough spreads its "
            "mass over a space of large entropy, a variance-like cost. <bookmark mark='d'/> A prior that is too smooth puts "
            "little mass near a rough truth, a bias-like cost. The best rate balances them, and chapter seven computes both "
            "for Gaussian processes."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
