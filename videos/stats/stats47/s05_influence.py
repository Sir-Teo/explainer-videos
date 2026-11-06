from __future__ import annotations

import numpy as np

from videos.stats.stats47.common import *  # noqa: F403


class Influence(VoiceoverScene):
    def construct(self):
        self.card()
        self.functional()
        self.curves()
        self.hadamard()
        self.variance()
        self.uses()

    def card(self):
        card = chapter_card(4, r"Influence functions and the functional delta method", r"Differentiating a statistic with respect to the data", lit=(1974,), part=PART)
        with self.voiceover("Chapter four. Influence functions and the functional delta method: differentiating a statistic with respect to the data."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def functional(self):
        rows = [
            cmath(r"T(F)", r":", r"\text{a statistic as a functional: \ } \hat\theta = T(F_n)", font_size=34),
            cmath(r"\mathrm{IF}(x)", r"=", r"\frac{d}{dt}\, T\big((1 - t)F + t\delta_x\big)\Big|_{t = 0}", font_size=34),
            cmath(r"T(F_n) - T(F)", r"=", r"\tfrac1n \textstyle\sum_i \mathrm{IF}(X_i) + R_n, \ \ E\,\mathrm{IF}(X) = 0", font_size=32),
            cmath(r"R_n = o_P(n^{-1/2})", r"\Rightarrow", r"\sqrt n(T(F_n) - T(F)) \Rightarrow N(0, E\,\mathrm{IF}^2)", font_size=30),
        ]
        rows[1][-1].set_color(S.ACCENT)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"von Mises (1947)"), why(r"Hampel (1974): \ add a point mass"), why(r"a first-order expansion"), why(r"chapters 2--3, \ unified")]
        with self.voiceover(
            "<bookmark mark='a'/> Richard von Mises's view of 1947: a statistic is a functional T of the empirical "
            "distribution, estimating the same functional of the true distribution. <bookmark mark='b'/> Frank Hampel's "
            "influence function, of 1974, is its derivative in the direction of a point mass: how much the functional moves "
            "when a little probability is added at x. <bookmark mark='c'/> To first order, the estimation error is the "
            "average of the influence function over the data, which has mean zero. <bookmark mark='d'/> If the remainder is "
            "small, the estimator is asymptotically normal with variance the expected squared influence. Chapter two's "
            "M-estimators and chapter three's quantiles are special cases."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curves(self):
        d = load("influence")
        z = np.asarray(d["z"])
        A = axes([-4, 4], [-3, 3], x_length=7.4, y_length=4.4, xlabel=r"$x$ \ (standard normal $F$)", ylabel=r"$\mathrm{IF}(x)$",
                 xticks=[-4, -2, 0, 2, 4], yticks=[-2, 0, 2], center=[-2.5, 0.2, 0])
        ax = A.ax
        cm = clip_curve(ax, z, d["mean"], MLEC, 4, ymin=-3, ymax=3)
        cmed = polyline(ax, z, d["median"], HODC, 4)
        ch = polyline(ax, z, d["huber"], GOODC, 4)
        ct = DashedVMobject(polyline(ax, z, d["trimmed"], S.PRIOR, 4), num_dashes=60)
        side = fit_rows(VGroup(
            label(r"blue: \ the mean, \ $x - \mu$: \ unbounded", font_size=22, color=MLEC),
            label(r"red: \ the median, \ $\mathrm{sign}(x)/2f(0)$: \ a step", font_size=22, color=HODC),
            label(r"green: \ Huber, \ $\psi_k(x)/E\psi_k'$: \ clipped", font_size=22, color=GOODC),
            label(r"purple, dashed: \ the 10\% trimmed mean", font_size=22, color=S.PRIOR),
            label(r"bounded $\Rightarrow$ one bad point does bounded harm", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The influence functions of four location estimators at the normal. The mean's is x minus "
            "mu: a straight line, unbounded, so one wild observation can move it arbitrarily far. <bookmark mark='b'/> The "
            "median's is a step: only the side of the median matters. <bookmark mark='c'/> Huber's is linear in the middle "
            "and flat beyond k. <bookmark mark='d'/> The trimmed mean's is similar, flat beyond the trimming points. "
            "<bookmark mark='e'/> A bounded influence function means a single contaminating point can do only bounded harm: "
            "Part thirty's robustness, as a derivative."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact formulas")))
            for k, (m_, c) in enumerate(zip("abcd", (cm, cmed, ch, ct))):
                vo.wait_until(m_)
                self.play(Create(c), FadeIn(side[k]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def hadamard(self):
        rows = [
            cmath(r"\sqrt n(F_n - F)", r"\Rightarrow", r"\mathbb G_F, \ \text{a Brownian bridge in } \ell^\infty \ \ (\text{Part 48})", font_size=30),
            cmath(r"T \text{ Hadamard differentiable}", r":", r"\frac{T(F + t h_t) - T(F)}{t} \to T'_F(h) \ \ \text{whenever } h_t \to h", font_size=28),
            cmath(r"\Rightarrow", r"\;", r"\sqrt n(T(F_n) - T(F)) \Rightarrow T'_F(\mathbb G_F)", font_size=34),
            cmath(r"\text{quantiles}, \ \text{M-functionals}", r":", r"\text{Hadamard differentiable; \ the sup and KS, \ too (with care)}", font_size=28),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Donsker, \ for distribution functions"), why(r"uniformly along converging paths"), why(r"the functional delta method"), why(r"what makes the bootstrap work, \ chapter 11")]
        with self.voiceover(
            "<bookmark mark='a'/> To make the remainder rigorous, think of the whole empirical distribution function as the "
            "random object. Root n times F n minus F converges to a Brownian bridge in the space of bounded functions: "
            "Donsker's theorem, the subject of Part forty-eight. <bookmark mark='b'/> If T is Hadamard differentiable, "
            "meaning that its difference quotients converge along every converging sequence of directions, <bookmark "
            "mark='c'/> then the functional delta method gives the limit of root n times T of F n minus T of F: the "
            "derivative applied to the Brownian bridge, a normal variable. <bookmark mark='d'/> Quantiles and M-functionals "
            "are Hadamard differentiable, and so, with care, are many others. Chapter eleven uses exactly this property to "
            "prove that the bootstrap works."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def variance(self):
        d = load("influence")
        rows = [
            cmath(r"T(F) = \mathrm{Var}_F(X)", r":", r"\mathrm{IF}(x) = (x - \mu)^2 - \sigma^2", font_size=34),
            cmath(r"n\,\mathrm{Var}(s^2)", r"\to", r"E\,\mathrm{IF}^2 = \mu_4 - \sigma^4", font_size=34),
            cmath(r"\text{normal}, \ n = 40", r":", rf"\text{{simulated}} \ {d['var_normal']['sim']:.2f} \ \text{{vs}} \ {d['var_normal']['delta']:.0f}", font_size=32),
            cmath(r"t_5 \text{ (scaled)}, \ n = 40", r":", rf"\text{{simulated}} \ {d['var_t5']['sim']:.2f} \ \text{{vs}} \ {d['var_t5']['delta']:.0f}", font_size=32),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(HODC)
        whys = [why(r"differentiate the variance"), why(r"the fourth moment matters"), why(r"$\mu_4 = 3$"), why(r"$\mu_4 = 9$: \ four times worse")]
        with self.voiceover(
            f"<bookmark mark='a'/> An example. The variance functional's influence function is the squared deviation minus "
            f"the variance. <bookmark mark='b'/> So n times the variance of the sample variance tends to the fourth central "
            f"moment minus sigma to the fourth: it depends on the tails. <bookmark mark='c'/> For normal data that is two, "
            f"and forty observations give {say(d['var_normal']['sim'], 2)} by simulation. <bookmark mark='d'/> For a t "
            f"distribution with five degrees of freedom, scaled to unit variance, it is eight, four times larger, and the "
            f"simulation gives {say(d['var_t5']['sim'], 2)}. This is why tests about variances are so sensitive to "
            f"non-normality, while tests about means are not."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def uses(self):
        rows = fit_rows(VGroup(
            label(r"the influence function, \ three ways:", font_size=28, color=GREY_A),
            label(r"a variance: \ $\widehat{\mathrm{Var}} = \tfrac{1}{n^2} \sum \widehat{\mathrm{IF}}(X_i)^2$, \ the infinitesimal jackknife", font_size=26, color=GOODC),
            label(r"a robustness measure: \ the gross-error sensitivity $\sup_x |\mathrm{IF}(x)|$", font_size=26, color=S.ACCENT),
            label(r"a design tool: \ efficient influence functions \ (Part 49's semiparametric theory)", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The influence function earns its keep three ways. <bookmark mark='b'/> It gives a variance "
            "estimate, by averaging its squared estimates over the data: the infinitesimal jackknife, which Part thirty-four "
            "used for random forests. <bookmark mark='c'/> Its supremum, the gross-error sensitivity, measures robustness. "
            "<bookmark mark='d'/> And in Part forty-nine it becomes a design tool: semiparametric efficiency theory looks for "
            "the influence function with the smallest variance."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
