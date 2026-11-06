from __future__ import annotations

import numpy as np

from videos.stats.stats26.common import *  # noqa: F403


class BvM(VoiceoverScene):
    def construct(self):
        self.card()
        self.statement()
        self.why()
        self.panels()
        self.coverage()
        self.tau_case()
        self.failures()

    def card(self):
        card = chapter_card(5, r"Bernstein--von Mises", r"The truce, \ stated and seen", lit=(), part=PART)
        with self.voiceover("Chapter five. The Bernstein–von Mises theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def statement(self):
        rows = [
            cmath(r"\bigl\| p(\theta \mid x_{1:n}) - N(\hat\theta_n, I(\theta_0)^{-1}/n) \bigr\|_{TV}", r"\to", r"0", font_size=30),
            cmath(r"\text{needs}", r":", r"\text{a fixed, finite-dimensional, regular model; \ prior positive at } \theta_0", font_size=26),
            cmath(r"\text{so}", r":", r"\text{credible intervals} \approx \text{confidence intervals}", font_size=30),
            cmath(r"\text{the prior}", r":", r"\text{washes out at rate } 1/\sqrt n", font_size=30),
        ]
        rows[2][2].set_color(SHRUNK)
        whys = [why(r"Laplace; \ Bernstein; \ von Mises; \ Le Cam (1953)"), why(r"Part 53 proves it"),
                why(r"the truce between the schools"), why(r"Part 22's MLE asymptotics, \ from the other side")]
        with self.voiceover(
            "<bookmark mark='a'/> The theorem that makes peace. As data accumulate, the posterior becomes indistinguishable, "
            "in total variation, from a normal centred at the maximum likelihood estimate with Part 22's inverse-information "
            "variance. <bookmark mark='b'/> It needs a fixed, finite-dimensional, regular model, and a prior that doesn't "
            "rule out the truth; Part 53 proves it. <bookmark mark='c'/> Then Bayesian credible intervals and frequentist "
            "confidence intervals nearly coincide, <bookmark mark='d'/> and the prior's influence fades like one over root n."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def panels(self):
        d = load("bvm")
        group = VGroup()
        curves = []
        for k, P in enumerate(d["panels"]):
            g = np.asarray(P["grid"])
            post, appr = np.asarray(P["post"]), np.asarray(P["approx"])
            ymax = float(max(post.max(), appr.max())) * 1.1
            A = axes([float(g[0]), float(g[-1])], [0, ymax], x_length=3.8, y_length=3.0, xlabel=rf"$\lambda$, \ $n = {P['n']}$",
                     ylabel=r"", xticks=[], yticks=[], center=[-4.5 + 4.5 * k, 0.6, 0])
            c1 = curve(A.ax, g, post, POST, 3)
            c2 = DashedVMobject(curve(A.ax, g, appr, RAW, 3), num_dashes=40)
            tv = label(rf"TV $= {P['tv']:.3f}$", font_size=22, color=HIT).next_to(A, DOWN, buff=0.25)
            group.add(A)
            curves.append((c1, c2, tv))
        rows = fit_rows(VGroup(
            label(r"orange: \ the posterior for a Poisson rate, \ Jeffreys's prior", font_size=22, color=POST),
            label(r"blue dashed: \ $N(\hat\lambda, \hat\lambda/n)$, \ the MLE's sampling approximation", font_size=22, color=RAW),
        ), 12.0, 0.2, [0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A Poisson rate of two, observed three, thirty and three hundred times. In orange, the "
            "posterior from Jeffreys's prior; in dashed blue, the normal approximation that frequentist theory gives for the "
            "maximum likelihood estimate. <bookmark mark='b'/> With three observations they visibly differ, a total "
            "variation distance of point oh eight. <bookmark mark='c'/> With thirty, point oh three. <bookmark mark='d'/> "
            "With three hundred, point oh oh eight: the curves are one."
        ) as vo:
            self.play(FadeIn(group), FadeIn(rows))
            for k, m_ in enumerate("bcd"):
                if k == 0:
                    vo.wait_until("a")
                vo.wait_until(m_)
                c1, c2, tv = curves[k]
                self.play(Create(c1), Create(c2), FadeIn(tv))
        self.clear_scene()

    def coverage(self):
        d = load("bvm")
        ns, cov = np.asarray(d["ns"]), np.asarray(d["coverage"])
        A = axes([0, 100], [0.9, 1.0], x_length=7.6, y_length=4.2, xlabel=r"observations $n$", ylabel=r"frequentist coverage",
                 xticks=[0, 25, 50, 75, 100], yticks=[0.9, 0.95, 1.0], center=[-2.0, 0.3, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(0, 0.95), ax.c2p(100, 0.95), color=TRUE, stroke_width=2)
        dots = VGroup(*[Dot(ax.c2p(n, c), radius=0.045, color=POST) for n, c in zip(ns, cov)])
        rows = fit_rows(VGroup(
            label(r"the 95\% Jeffreys credible interval for $\lambda$", font_size=22, color=POST),
            label(r"its exact coverage when $\lambda = 2$, \ by summing the Poisson", font_size=22),
            label(rf"$n = 1$: \ {100 * cov[0]:.1f}\%; \ $n = 100$: \ {100 * cov[-1]:.1f}\%", font_size=22, color=HIT),
            label(r"a credible interval, \ judged as a confidence interval, \ passes", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Bernstein–von Mises also predicts frequentist coverage. Take the ninety-five percent "
            "credible interval for a Poisson rate from Jeffreys's prior, <bookmark mark='b'/> and compute exactly how often "
            "it would cover a true rate of two. <bookmark mark='c'/> Even with one observation it covers ninety-eight "
            "percent of the time; by a hundred, ninety-five point two, wobbling with the discreteness of the counts. "
            "<bookmark mark='d'/> Judged by the other school's standard, this Bayesian interval passes. Priors chosen by "
            "Jeffreys's rule are often called probability matching for this reason."
        ) as vo:
            self.play(FadeIn(A), Create(nom))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.02), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def failures(self):
        rows = fit_rows(VGroup(
            label(r"few groups: \ the eight schools' $\tau$ never becomes normal", font_size=24, color=RES),
            label(r"boundaries: \ $\tau = 0$ is on the edge, \ as in Part 25", font_size=24, color=RES),
            label(r"parameters growing with $n$: \ Neyman--Scott, \ high-dimensional regression", font_size=24, color=RES),
            label(r"nonparametric priors: \ Freedman (1963), \ Diaconis \& Freedman (1986)", font_size=24, color=RES),
            label(r"there, \ the prior matters for ever, \ and must be defended", font_size=24, color=PATH),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> But the truce has borders. The eight schools' tau is learned from eight numbers, and its "
            "posterior never looks normal. <bookmark mark='b'/> A true value on a boundary, like a variance of zero, "
            "breaks the theorem's conditions. <bookmark mark='c'/> When parameters multiply with the data, as in Part 22's "
            "Neyman–Scott problem, the prior keeps mattering. <bookmark mark='d'/> And with infinite-dimensional priors, "
            "David Freedman, and later Persi Diaconis with him, showed posteriors that converge to the wrong answer, the "
            "story Part 53 begins with. <bookmark mark='e'/> In these regions the prior matters for ever, and must be "
            "defended on its merits."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def why(self):
        rows = [
            cmath(r"\log p(\theta \mid x)", r"=", r"\log p(\theta) + \ell_n(\theta) + c", font_size=30),
            cmath(r"\ell_n(\theta)", r"\approx", r"\ell_n(\hat\theta) - \tfrac n2 (\theta - \hat\theta)^\top I(\hat\theta)(\theta - \hat\theta)", font_size=28),
            cmath(r"\log p(\theta)", r":", r"\text{fixed as } n \text{ grows: \ a vanishing share}", font_size=30),
            cmath(r"\text{so}", r":", r"\log p(\theta \mid x) \approx \text{a quadratic}: \ \text{a normal}", font_size=30),
        ]
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"prior plus log likelihood"), why(r"Taylor at the MLE: \ curvature $n I$"),
                why(r"the likelihood swamps it"), why(r"Laplace's argument, \ 1774")]
        with self.voiceover(
            "<bookmark mark='a'/> Why it works, in Laplace's own argument. The log posterior is the log prior plus the log "
            "likelihood. <bookmark mark='b'/> Near the maximum likelihood estimate, the log likelihood is close to a "
            "quadratic whose curvature is n times the Fisher information, so it grows with every observation. "
            "<bookmark mark='c'/> The log prior doesn't grow at all; its share shrinks to nothing, provided it is smooth and "
            "positive near the truth. <bookmark mark='d'/> A log density that is a quadratic is a normal. The hard part of "
            "the proof, Part 53's, is showing that the regions far from the estimate don't matter."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def tau_case(self):
        d = load("schools")
        tau, pt = np.asarray(d["tau"]), np.asarray(d["post_tau"])
        A = axes([0, 30], [0, 0.12], x_length=7.4, y_length=4.2, xlabel=r"$\tau$", ylabel=r"$p(\tau \mid y)$", xticks=[0, 10, 20, 30],
                 yticks=[0, 0.05, 0.1], center=[-2.0, 0.3, 0], yfmt=lambda v: f"{v:.2f}")
        ax = A.ax
        keep = tau <= 30
        c = curve(ax, tau[keep], pt[keep], POST, 3.5)
        mode = Dot(ax.c2p(0, pt[0]), radius=0.09, color=RES)
        rows = fit_rows(VGroup(
            label(r"the eight schools' $\tau$: \ eight numbers' worth of data", font_size=22),
            label(r"the mode is at 0, \ on the boundary", font_size=22, color=RES),
            label(r"no normal approximation centred at the mode can fit it", font_size=22, color=RES),
            label(r"so use the exact grid, \ or sampling (Part 27)", font_size=22, color=SHRUNK),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The eight schools show the theorem failing in practice. Tau is learned from eight "
            "numbers, <bookmark mark='b'/> and its posterior peaks at zero, exactly on the boundary. <bookmark mark='c'/> A "
            "normal curve centred at the peak would put half its mass on negative standard deviations; no normal "
            "approximation fits this shape. <bookmark mark='d'/> That is why chapter two used an exact grid, and why Part 27 "
            "needs samplers that respect the geometry."
        ) as vo:
            self.add(schools_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(mode, scale=2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
