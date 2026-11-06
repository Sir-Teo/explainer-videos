from __future__ import annotations

import numpy as np

from videos.stats.stats53.common import *  # noqa: F403


class GaussianProcess(VoiceoverScene):
    def construct(self):
        self.card()
        self.rkhs()
        self.theorem()
        self.chart()
        self.functions()
        self.examples()

    def card(self):
        card = chapter_card(7, r"Gaussian process priors", r"Rates from the RKHS and small-ball probabilities", lit=(2008,), part=PART)
        with self.voiceover("Chapter seven. Gaussian process priors: rates from the reproducing-kernel Hilbert space and small-ball probabilities."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def rkhs(self):
        rows = [
            cmath(r"W \sim GP(0, k)", r":", r"\text{a random function, \ e.g. Matérn of smoothness } \alpha", font_size=32),
            cmath(r"\mathbb H", r":", r"\text{its RKHS: \ the shifts } h \text{ for which } W + h \text{ looks like } W", font_size=32),
            cmath(r"\text{small ball}", r":", r"\varphi_0(\varepsilon) = -\log P(\|W\|_\infty < \varepsilon)", font_size=34),
            cmath(r"\text{concentration function}", r":", r"\varphi_{w_0}(\varepsilon) = \inf_{\|h - w_0\| < \varepsilon} \tfrac12\|h\|_{\mathbb H}^2 + \varphi_0(\varepsilon)", font_size=30),
        ]
        rows[3][-1].set_color(PRIORC)
        whys = [why(r"Part 39's kriging prior"), why(r"Cameron--Martin"), why(r"how probable is a tiny ball?"), why(r"bias $+$ complexity")]
        with self.voiceover(
            "<bookmark mark='a'/> A Gaussian process prior, like Part thirty-nine's Matérn kriging prior, puts a random "
            "function in the model. <bookmark mark='b'/> Its reproducing-kernel Hilbert space is the set of shifts h for which "
            "W plus h has a law equivalent to W's, the Cameron–Martin space; it is much smaller and smoother than the paths "
            "themselves. <bookmark mark='c'/> The small-ball exponent measures how improbable it is for the process to stay "
            "within epsilon of zero everywhere. <bookmark mark='d'/> And the concentration function at a truth w zero adds the "
            "cost of approximating the truth by an element of the RKHS, half its squared norm, to that small-ball exponent: an "
            "approximation term and a complexity term."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def theorem(self):
        rows = [
            cmath(r"\varphi_{w_0}(\varepsilon_n)", r"\le", r"n\varepsilon_n^2", font_size=40),
            cmath(r"\Rightarrow", r"\;", r"\text{the posterior contracts at rate } \varepsilon_n \ \text{(regression, \ density, \ classification)}", font_size=30),
            cmath(r"\text{Matérn-}\alpha, \ w_0 \in C^\beta", r":", r"\varepsilon_n = n^{-\min(\alpha, \beta)/(2\alpha + d)}", font_size=34),
            cmath(r"\alpha = \beta", r":", r"n^{-\beta/(2\beta + d)}: \ \text{Stone's minimax rate}", font_size=34),
        ]
        rows[0][-1].set_color(GOODC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"van der Vaart \& van Zanten (2008)"), why(r"GGV's conditions, \ verified"), why(r"$d$ dimensions"), why(r"Part 50's rate")]
        with self.voiceover(
            "<bookmark mark='a'/> Aad van der Vaart and Harry van Zanten's theorem of 2008: if the concentration function at "
            "the truth is at most n epsilon squared, <bookmark mark='b'/> the posterior contracts at rate epsilon n, in "
            "regression, density estimation and classification alike. The concentration function verifies both of "
            "Ghosal, Ghosh and van der Vaart's conditions at once. <bookmark mark='c'/> For a Matérn prior of smoothness "
            "alpha and a truth of smoothness beta in d dimensions, the rate is n to the minus the smaller of alpha and beta, "
            "over two alpha plus d. <bookmark mark='d'/> When alpha equals beta it is Stone's minimax rate from Part fifty."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("gp")
        a = np.asarray(d["alphas"])
        A = axes([0.15, 3.1], [0.1, 0.37], x_length=7.4, y_length=4.4, xlabel=rf"prior smoothness $\alpha$ \ (truth $\beta = {d['beta']:g}$)", ylabel=r"rate exponent",
                 xticks=[0.5, 1, 1.5, 2, 2.5, 3], yticks=[0.15, 0.2, 0.25, 0.3], center=[-2.5, 0.2, 0])
        ax = A.ax
        u = np.linspace(0.15, 3.1, 300)
        th = polyline(ax, u, np.minimum(u, d["beta"]) / (1 + 2 * u), TRUTHC, 4)
        emp = VGroup(*[Dot(ax.c2p(x, y), radius=0.08, color=POSTC) for x, y in zip(a, d["empirical"])])
        mm = DashedLine(ax.c2p(0.15, d["minimax"]), ax.c2p(3.1, d["minimax"]), color=GOODC, stroke_width=2.5)
        i1 = list(np.round(a, 3)).index(1.0)
        side = fit_rows(VGroup(
            label(r"the exponent $r$ in $\varepsilon_n \asymp n^{-r}$", font_size=22),
            label(r"white: \ $\min(\alpha, \beta)/(1 + 2\alpha)$", font_size=22, color=TRUTHC),
            label(rf"blue: \ fitted from exact risks, \ $n = 10^3$ to $10^6$", font_size=22, color=POSTC),
            label(rf"green: \ minimax $1/3$: \ {d['empirical'][i1]:.3f} at $\alpha = 1$", font_size=22, color=GOODC),
            label(r"smoother priors converge to the limit slowly", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The rate's exponent as a function of the prior's smoothness, for a truth of smoothness one. "
            f"<bookmark mark='b'/> In white, the theory: rising while the prior is rougher than the truth, falling once it is "
            f"smoother. <bookmark mark='c'/> In blue, exponents fitted to the exact risks from a thousand to a million "
            f"observations. <bookmark mark='d'/> The peak is the minimax third, reached only when the smoothness matches: "
            f"{say(d['empirical'][i1], 3)} at alpha one. <bookmark mark='e'/> For smoother priors the fitted exponents sit a "
            f"little above the limit, which they approach only slowly. A Gaussian process prior is minimax for exactly one "
            f"smoothness, and the truth's is unknown."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact risks")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(th), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(emp), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(mm), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def functions(self):
        import math

        from explainer.stats.kit import bnp as BN

        K, n = 300, 1000
        r = np.random.default_rng(538)
        th = BN.sobolev_truth(K, 1.0) * 3
        Y = th + r.standard_normal(K) / math.sqrt(n)
        x = np.linspace(0, 1, 300)
        Phi = np.sqrt(2) * np.cos(np.pi * np.outer(x, np.arange(1, K + 1)))
        f0 = Phi @ th
        panels = VGroup()
        for i, (a, col, name) in enumerate(((0.25, FREQC, r"$\alpha = 1/4$: \ too rough"), (1.0, GOODC, r"$\alpha = 1$: \ matched"), (3.0, BADC, r"$\alpha = 3$: \ too smooth"))):
            post = BN.posterior(Y, n, BN.prior_var(K, a))
            m = Phi @ post["mean"]
            sd = np.sqrt((Phi ** 2) @ post["var"])
            Ax = axes([0, 1], [-4.5, 6.5], x_length=3.9, y_length=3.2, xlabel=r"$x$", ylabel=r"", xticks=[0, 0.5, 1], yticks=[-4, 0, 4],
                      center=[-4.4 + 4.4 * i, -0.3, 0])
            ax = Ax.ax
            band = Polygon(*[ax.c2p(a_, b_) for a_, b_ in zip(x, np.clip(m - 1.96 * sd, -4.5, 6.5))],
                           *[ax.c2p(a_, b_) for a_, b_ in zip(x[::-1], np.clip((m + 1.96 * sd)[::-1], -4.5, 6.5))], fill_color=col, fill_opacity=0.3, stroke_width=0)
            g = VGroup(Ax, band, clip_curve(ax, x, f0, TRUTHC, 2.5, ymin=-4.5, ymax=6.5), clip_curve(ax, x, m, col, 3, ymin=-4.5, ymax=6.5),
                       label(name, font_size=22, color=col).next_to(Ax, UP, buff=0.15))
            panels.add(g)
        foot = label(r"white: \ the truth $f_0 = \sum \theta_k\sqrt2\cos(\pi kx)$; \ colour: \ posterior mean and pointwise 95\% band, \ $n = 1{,}000$", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> The same posteriors seen as functions: the truth in white, a cosine series of smoothness "
            "one, and the posterior mean with its pointwise ninety-five percent band, from a thousand observations. <bookmark "
            "mark='b'/> A rough prior, alpha a quarter, gives a wiggly mean and a wide band: honest, but noisy. <bookmark "
            "mark='c'/> The matched prior tracks the truth with a moderate band. <bookmark mark='d'/> A smooth prior, alpha "
            "three, gives a smooth mean and a narrow band that misses the truth's steep drop: confidently "
            "wrong, Cox's phenomenon of chapter five, now in function space."
        ) as vo:
            self.play(FadeIn(foot))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(panels[0]))
            vo.wait_until("c")
            self.play(FadeIn(panels[1]))
            vo.wait_until("d")
            self.play(FadeIn(panels[2]))
        self.wait(1.0)
        self.clear_scene()

    def examples(self):
        rows = fit_rows(VGroup(
            label(r"the same theory covers:", font_size=28, color=GREY_A),
            label(r"squared-exponential kernels: \ analytic paths, \ rates only logarithmic unless rescaled", font_size=26, color=BADC),
            label(r"rescaling the length scale with $n$: \ any rate, \ if you know $\beta$", font_size=26, color=PRIORC),
            label(r"a random length scale: \ adaptation to all $\beta$ at once (van der Vaart \& van Zanten 2009)", font_size=26, color=GOODC),
            label(r"in practice: \ the length scale is estimated, \ the subject of the next chapter", font_size=26, color=BALLC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The same theory covers the popular kernels. <bookmark mark='b'/> The squared-exponential "
            "kernel has analytic sample paths, so with a fixed length scale it contracts only at a logarithmic rate for a "
            "truth of finite smoothness. <bookmark mark='c'/> Shrinking the length scale with n restores any polynomial rate, "
            "if you know the truth's smoothness. <bookmark mark='d'/> Van der Vaart and van Zanten showed in 2009 that putting "
            "a prior on the length scale adapts to every smoothness at once. <bookmark mark='e'/> And in practice the length "
            "scale is usually estimated from the data, which is the empirical Bayes of the next chapter."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
