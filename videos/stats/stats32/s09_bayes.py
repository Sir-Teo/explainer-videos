from __future__ import annotations

import numpy as np

from videos.stats.stats32.common import *  # noqa: F403

HS = S.KEPT  # the horseshoe: green
BL = S.POST  # the Bayesian lasso: orange


class BayesSparse(VoiceoverScene):
    def construct(self):
        self.card()
        self.laplace()
        self.not_sparse()
        self.profile()
        self.horseshoe()
        self.kappa()
        self.means()
        self.sse()
        self.spike_slab()

    def card(self):
        card = chapter_card(8, r"Bayesian sparsity", r"The lasso's prior is not sparse", lit=(2010,), part=PART)
        with self.voiceover("Chapter eight. Bayesian sparsity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def laplace(self):
        rows = [
            cmath(r"\pi(\beta_j)", r"\propto", r"e^{-\lambda|\beta_j|}", font_size=34),
            cmath(r"-\log \pi(\beta \mid y)", r"=", r"\tfrac1{2\sigma^2}\|y - X\beta\|^2 + \lambda\|\beta\|_1 + c", font_size=30),
            cmath(r"\text{the lasso}", r"=", r"\text{the posterior mode under Laplace priors}", font_size=30),
            cmath(r"\text{Park \& Casella}", r":", r"\text{a Gibbs sampler for the whole posterior}", font_size=30),
        ]
        rows[2][-1].set_color(LASSO)
        whys = [why(r"the double exponential"), why(r"negative log posterior"), why(r"Tibshirani noted it in 1996"),
                why(r"the Bayesian lasso (2008)")]
        with self.voiceover(
            "<bookmark mark='a'/> Ridge was a normal prior. The lasso has a prior too: independent Laplace, or double "
            "exponential, distributions on the coefficients. <bookmark mark='b'/> The negative log posterior is the residual "
            "sum of squares plus lambda times the one norm. <bookmark mark='c'/> So the lasso estimate is the posterior "
            "mode, as Tibshirani noted in his original paper. <bookmark mark='d'/> Trevor Park and George Casella's "
            "Bayesian lasso of 2008 writes the Laplace distribution as a scale mixture of normals and samples the whole "
            "posterior by Gibbs sampling."
        ) as vo:
            intro=label('A Laplace coefficient prior gives the lasso posterior mode',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def not_sparse(self):
        rows = [
            cmath(r"P(\beta_j = 0 \mid y)", r"=", r"0: \ \text{a continuous prior}", font_size=32),
            cmath(r"E(\beta_j \mid y)", r"\ne", r"0 \ \text{for every } y_j \ne 0", font_size=32),
            cmath(r"\text{draws from the prior}", r":", r"\text{not sparse at all}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{the mode is sparse; \ the mean and the prior are not}", font_size=30),
        ]
        rows[3][-1].set_color(RES)
        whys = [why(r"zero has probability zero"), why(r"the posterior mean shrinks, \ never kills"),
                why(r"Laplace draws are all nonzero"), why(r"sparsity came from the optimizer")]
        with self.voiceover(
            "<bookmark mark='a'/> But the Laplace prior is not a sparse prior. It is continuous, so the posterior "
            "probability that any coefficient is exactly zero is zero. <bookmark mark='b'/> In the independent "
            "normal-means problem, the posterior mean has the sign of a nonzero observation and is zero at a zero "
            "observation. A general correlated regression needs a separate statement. <bookmark mark='c'/> And "
            "vectors drawn from the prior have every coordinate nonzero. <bookmark mark='d'/> The lasso's zeros come "
            "from taking a mode of a distribution with a sharp peak, not from any belief that most effects are zero. "
            "Exact posterior zeros need a point mass. Continuous shrinkage priors can instead concentrate strongly "
            "near zero."
        ) as vo:
            intro=label('Continuous shrinkage does not assign posterior mass to exact zeros',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def profile(self):
        d = load("bayes")["profile"]
        y = np.asarray(d["y"])
        A = axes([-6, 6], [-6, 6], x_length=5.6, y_length=5.0, xlabel=r"observation $y$ \ ($\sigma = 1$)",
                 ylabel=r"estimate of $\theta$", xticks=[-6, -3, 0, 3, 6], yticks=[-6, -3, 0, 3, 6], center=[-2.6, 0.0, 0])
        ax = A.ax
        idl = DashedLine(ax.c2p(-6, -6), ax.c2p(6, 6), color=GREY_D, stroke_width=1.5)
        soft = curve(ax, y, np.asarray(d["soft"]), LASSO, 3)
        lm = curve(ax, y, np.asarray(d["laplace_mean"]), BL, 3.5)
        hs = curve(ax, y, np.asarray(d["horseshoe"]), HS, 3.5)
        rows = fit_rows(VGroup(
            label(r"one observation, \ one parameter", font_size=22),
            label(r"blue: \ Laplace posterior mode = soft threshold", font_size=22, color=LASSO),
            label(r"orange: \ Laplace posterior mean", font_size=22, color=BL),
            label(r"smooth; zero at $y=0$; large-$|y|$ shift approaches 1", font_size=22, color=BL),
            label(r"green: \ horseshoe mean \ ($\tau = 0.1$)", font_size=22, color=HS),
            label(r"crushes small $y$, \ leaves large $y$", font_size=22, color=HS),
        ), 4.4, 0.42, [4.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One observation y, normal around theta with standard deviation one, and three answers. "
            "<bookmark mark='b'/> The Laplace prior's posterior mode is the soft threshold. <bookmark mark='c'/> Its "
            "posterior mean is a smooth curve: never zero except at zero, and still a full unit below the diagonal for large "
            "y. Neither sparse nor unbiased. <bookmark mark='d'/> The horseshoe prior's posterior mean does what we want: it "
            "flattens small observations almost to zero and leaves large ones almost untouched."
        ) as vo:
            self.play(FadeIn(A), Create(idl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(soft), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(lm), FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(Create(hs), FadeIn(rows[4]), FadeIn(rows[5]))
        self.clear_scene()

    def horseshoe(self):
        rows = [
            cmath(r"\beta_j \mid \lambda_j, \tau", r"\sim", r"N(0, \lambda_j^2 \tau^2)", font_size=32),
            cmath(r"\lambda_j", r"\sim", r"C^+(0, 1), \ \ \tau \sim C^+(0, 1)", font_size=32),
            cmath(r"\text{global } \tau", r":", r"\text{pulls everything towards } 0", font_size=30),
            cmath(r"\text{local } \lambda_j", r":", r"\text{heavy tails let real signals escape}", font_size=30),
        ]
        rows[1][-1].set_color(HS)
        whys = [why(r"a scale mixture of normals"), why(r"half-Cauchy: \ Carvalho, Polson \& Scott (2010)"),
                why(r"adapts to the overall sparsity"), why(r"one scale per coefficient")]
        with self.voiceover(
            "<bookmark mark='a'/> The horseshoe of Carlos Carvalho, Nicholas Polson and James Scott is also a scale "
            "mixture of normals, <bookmark mark='b'/> but with half-Cauchy distributions on both a local scale for "
            "each coefficient and a global scale shared by all. <bookmark mark='c'/> The global scale, learned from "
            "the data, pulls everything towards zero when most effects are null. <bookmark mark='d'/> The local "
            "scales have tails so heavy that a coefficient with real signal can resist the global pull; negligible "
            "tail shrinkage is an asymptotic property, not guaranteed finite-signal detection."
        ) as vo:
            intro=label('Local and global half-Cauchy scales produce strong continuous shrinkage',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def kappa(self):
        k = np.linspace(0.004, 0.996, 300)
        dens = 1 / np.pi * k ** -0.5 * (1 - k) ** -0.5
        A = axes([0, 1], [0, 3.2], x_length=6.0, y_length=4.2, xlabel=r"shrinkage $\kappa_j = 1/(1 + \lambda_j^2)$",
                 ylabel=r"prior density \ ($\tau = 1$)", xticks=[0, 0.5, 1], yticks=[0, 1, 2, 3], center=[-2.4, 0.3, 0])
        ax = A.ax
        c = clip_curve(ax, k, dens, HS, 3.5, ymax=3.2)
        lap = clip_curve(ax, k, 0.5 * k ** -2 * np.exp(-(1 - k) / (2 * k)), BL, 2.5, ymax=3.2)  # Laplace, lambda = 1
        rows = fit_rows(VGroup(
            label(r"$E(\theta \mid y, \kappa) = (1 - \kappa)\, y$", font_size=22),
            label(r"horseshoe: \ $\kappa \sim \mathrm{Beta}(\tfrac12, \tfrac12)$", font_size=22, color=HS),
            label(r"mass piles up at $\kappa = 1$ \ (noise: \ shrink all) \ and $\kappa = 0$ \ (signal: \ shrink none)", font_size=22, color=HS),
            label(r"Laplace \ ($\lambda = 1$): \ no mass near $\kappa = 0$, \ so even big signals are shrunk", font_size=22, color=BL),
        ), 4.6, 0.42, [4.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The name comes from this picture. Given its local scale, the posterior mean of a "
            "coefficient is one minus kappa times the observation, where kappa is the shrinkage factor. "
            "<bookmark mark='b'/> Under the horseshoe, with tau equal to one, kappa has a beta one-half, one-half "
            "distribution, <bookmark mark='c'/> shaped like a horseshoe: mass piles up near one, total shrinkage for noise, "
            "and near zero, no shrinkage for signals. <bookmark mark='d'/> The Laplace prior's shrinkage factor has almost "
            "no mass near zero, so even large signals are always shrunk."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(lap), FadeIn(rows[3]))
        self.clear_scene()

    def means(self):
        d = load("bayes")
        y, th, hs, bl = (np.asarray(d[k]) for k in ("y", "theta", "hs", "bl"))
        A = axes([-0.5, 60.5], [-3.2, 7.5], x_length=8.4, y_length=4.4, xlabel=r"the first 60 of 200 means",
                 ylabel=r"value", xticks=[1, 10, 20, 30, 40, 50, 60], yticks=[-2, 0, 2, 4, 6], center=[-1.4, 0.3, 0])
        ax = A.ax
        idx = np.arange(60)
        obs = VGroup(*[Dot(ax.c2p(i + 1, y[i]), radius=0.045, color=GREY_B) for i in idx])
        tru = VGroup(*[Line(ax.c2p(i + 0.6, th[i]), ax.c2p(i + 1.4, th[i]), color=SPIKE, stroke_width=3) for i in idx])
        b1 = VGroup(*[Dot(ax.c2p(i + 1, bl[i]), radius=0.05, color=BL) for i in idx])
        h1 = VGroup(*[Dot(ax.c2p(i + 1, hs[i]), radius=0.05, color=HS) for i in idx])
        rows = fit_rows(VGroup(
            label(r"200 means: \ 10 at 5, \ 190 at 0", font_size=22),
            label(r"grey: \ observations; \ gold: \ truth", font_size=22, color=SPIKE),
            label(r"orange: \ Bayesian lasso means", font_size=22, color=BL),
            label(r"green: \ horseshoe means", font_size=22, color=HS),
        ), 3.2, 0.42, [5.3, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A sparse normal-means problem: two hundred means, ten equal to five and the rest zero, one "
            "noisy observation of each. The first sixty are shown. <bookmark mark='b'/> Grey dots are the observations; gold "
            "dashes the truth. <bookmark mark='c'/> The Bayesian lasso's posterior means, by Gibbs sampling, shrink the "
            "signals noticeably and leave every null slightly nonzero. <bookmark mark='d'/> The horseshoe's posterior means "
            "sit almost on the truth: nulls near zero, signals near five."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(obs), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(tru), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(b1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeOut(b1), FadeIn(h1), FadeIn(rows[3]))
        self.clear_scene()

    def sse(self):
        d = load("bayes")
        e = d["sse"]
        hdr = [r"\textbf{estimate}", r"\textbf{total squared error}"]
        body = [[r"the observations themselves", f"{e['mle']:.0f}"],
                [rf"soft threshold at $\sqrt{{2 \log p}} = {d['lam_u']:.2f}$", f"{e['soft']:.0f}"],
                [r"Bayesian lasso mean \ ($\lambda = 1$)", f"{e['bayes_lasso']:.0f}"],
                [r"horseshoe mean", f"{e['horseshoe']:.0f}"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.2, row_buff=0.32, colors=[GREY_A, GREY_B, LASSO, BL, HS])
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"Donoho \& Johnstone's universal threshold kills the nulls but shrinks the signals by 3.26", font_size=22, color=LASSO),
            label(rf"the horseshoe learns $\tau \approx {d['tau_mean']:.2f}$ and adapts to the sparsity", font_size=22, color=HS),
        ), 12.0, 0.22, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Total squared error. The raw observations make an error of about two hundred, one "
            "for each mean. Soft thresholding at Donoho and Johnstone's universal threshold, root two log p, removes "
            "the nulls but shrinks every signal by three and a quarter. The Bayesian lasso does better, <bookmark "
            "mark='b'/> and the horseshoe has the smallest error in this one seeded experiment, having learned a "
            "small global scale from the data."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(Indicate(tb[4], color=HS), FadeIn(foot[1]))
        self.clear_scene()

    def spike_slab(self):
        rows = fit_rows(VGroup(
            label(r"a point-mass sparse prior: \ spike-and-slab, \ $\beta_j \sim (1 - w)\,\delta_0 + w\, N(0, \tau^2)$", font_size=24),
            label(r"Mitchell \& Beauchamp (1988); \ George \& McCulloch's SSVS (1993)", font_size=24, color=GREY_A),
            label(r"exact zeros, \ posterior inclusion probabilities, \ $2^p$ possible models; search need not enumerate all", font_size=24, color=RES),
            label(r"the horseshoe is its continuous stand-in; \ Part 53 proves when these posteriors contract", font_size=24, color=HS),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The most honest sparse prior puts a point mass at zero: a spike for the null "
            "effects and a slab for the real ones. <bookmark mark='b'/> Toby Mitchell and John Beauchamp proposed it "
            "in 1988, and Edward George and Robert McCulloch's stochastic search made it computable in 1993. "
            "<bookmark mark='c'/> It gives exact zeros and a posterior probability that each variable is included, at"
            " the cost of averaging over two to the p models. <bookmark mark='d'/> The horseshoe is a continuous "
            "shrinkage alternative, with no point mass at zero. Neither posterior inference nor computation has a "
            "universal winner. Part 53 proves when such posteriors concentrate on the truth."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
