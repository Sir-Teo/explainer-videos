from __future__ import annotations

import numpy as np
from scipy import optimize, special

from videos.stats.stats25.common import *  # noqa: F403


class GLMM(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.integrals()
        self.fit()
        self.marginal()
        self.league_funnel()
        self.league_table()

    def card(self):
        card = chapter_card(10, r"GLMMs", r"Random effects inside a link", lit=(1993,), part=PART)
        with self.voiceover("Chapter ten. Generalized linear mixed models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def model(self):
        rows = [
            cmath(r"\mathrm{logit}\, P(y_{gi} = 1 \mid u_g)", r"=", r"x_{gi}^\top\beta + u_g, \ \ u_g \sim N(0, s^2)", font_size=28),
            cmath(r"L(\beta, s)", r"=", r"\prod_g \int \prod_i p_{gi}(u)^{y_{gi}}(1 - p_{gi}(u))^{1 - y_{gi}}\, \phi(u/s)\tfrac{du}{s}", font_size=26),
            cmath(r"\text{no closed form}", r":", r"\text{one integral per school}", font_size=30),
            cmath(r"\text{PQL}", r":", r"\text{linearize and iterate: \ biased for binary data}", font_size=28),
        ]
        rows[1][2].set_color(SHRUNK)
        whys = [why(r"Part 24's GLM, \ plus a school effect"), why(r"average each school over its $u$"),
                why(r"the normal integral is gone"), why(r"Breslow \& Clayton (1993); \ Breslow \& Lin (1995)")]
        intro = label('A working probability model states the assumptions behind shrinkage', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Put a random effect inside Part 24's logistic regression: each school shifts the "
            "log odds of passing by its own amount. <bookmark mark='b'/> The likelihood averages each school's "
            "probability of its pupils' results over the distribution of its effect, <bookmark mark='c'/> and unlike "
            "the linear case the integral has no closed form, one for every school. <bookmark mark='d'/> Norman "
            "Breslow and David Clayton's penalized quasi-likelihood of 1993 linearizes and iterates, but it can be "
            "substantially biased for binary data with small clusters; the direction need not be the same for every "
            "parameter, so modern software integrates directly."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def integrals(self):
        A = axes([-3, 3], [0, 1.05], x_length=6.8, y_length=4.2, xlabel=r"school effect $u$", ylabel=r"integrand, \ scaled",
                 xticks=[-2, 0, 2], yticks=[0, 0.5, 1], center=[-2.2, 0.3, 0])
        ax = A.ax
        # a small example school: 4 pupils, all pass, eta0 = 0.5, s = 1.5 (skewed, so Laplace is visibly off)
        eta0, n_, k_, s = 0.5, 4, 4, 1.5
        u = np.linspace(-3, 3, 400)
        logh = k_ * (eta0 + u) - n_ * np.logaddexp(0, eta0 + u) - 0.5 * u ** 2 / s ** 2
        mode = optimize.brentq(lambda a: k_ - n_ * special.expit(eta0+a) - a/s**2, -n_*s**2, n_*s**2)
        peak = k_*(eta0+mode)-n_*np.logaddexp(0,eta0+mode)-0.5*mode**2/s**2
        h = np.exp(logh - peak)
        p = special.expit(eta0 + mode)
        curv = n_ * p * (1 - p) + 1 / s ** 2
        lap = np.exp(-0.5 * curv * (u - mode) ** 2)
        c_true = curve(ax, u, h, TRUE, 3.5)
        c_lap = curve(ax, u, lap, SHRUNK, 2.5)
        xs, ws = np.polynomial.hermite.hermgauss(5)
        nodes = mode + np.sqrt(2 / curv) * xs
        hv = np.exp(k_ * (eta0 + nodes) - n_ * np.logaddexp(0, eta0 + nodes) - 0.5 * nodes ** 2 / s ** 2 - peak)
        sticks = VGroup(*[Line(ax.c2p(a, 0), ax.c2p(a, b), color=PATH, stroke_width=4) for a, b in zip(nodes, hv) if -3 <= a <= 3])
        rows = fit_rows(VGroup(
            label(r"gold: \ one school's integrand", font_size=22, color=TRUE),
            label(r"green: \ Laplace, \ a normal at the mode", font_size=22, color=SHRUNK),
            label(r"yellow: \ adaptive Gauss--Hermite nodes", font_size=22, color=PATH),
            label(r"a small school: \ 4 pupils, \ all passed", font_size=22, color=GREY_A),
        ), 4.4, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Each school's integrand is a bump in its random effect; here a small school of four"
            " pupils who all passed, whose bump is lopsided. <bookmark mark='b'/> The Laplace approximation of Part "
            "22 replaces it with a normal curve at its peak, matched in curvature, and integrates that exactly. "
            "<bookmark mark='c'/> Adaptive Gauss–Hermite quadrature, from José Pinheiro and Douglas Bates, places a "
            "few nodes around the same peak with the same scale, and adds up the integrand at them with weights. "
            "<bookmark mark='d'/> With one node it is the Laplace approximation; increasing the node count improves "
            "the approximation only when numerical checks confirm stability. Ten nodes are not a universal accuracy "
            "guarantee."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(c_true), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c_lap), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(x) for x in sticks], lag_ratio=0.2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def fit(self):
        d = load("glmm")
        lp, aq = d["laplace"], d["agq"]
        hdr = [r"\textbf{method}", r"\textbf{programme}", r"\textbf{SE}", r"\textbf{SES}", r"\textbf{school SD} $s$", r"\textbf{log lik}"]
        body = [[r"Laplace", f"{lp['beta'][1]:.3f}", f"{lp['se'][1]:.3f}", f"{lp['beta'][2]:.3f}", f"{lp['sigma']:.3f}", f"{lp['loglik']:.2f}"],
                [r"AGQ, \ 10 nodes", f"{aq['beta'][1]:.3f}", f"{aq['se'][1]:.3f}", f"{aq['beta'][2]:.3f}", f"{aq['sigma']:.3f}", f"{aq['loglik']:.2f}"],
                [r"GEE, \ Part 24: \ marginal", f"{d['gee'][1]:.3f}", r"", f"{d['gee'][2]:.3f}", r"", r""]]
        tb = table_rows([hdr] + body, font_size=24, col_buff=0.6, row_buff=0.3, colors=[GREY_A, SHRUNK, PATH, POOLED])
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"40 of the World's schools; \ passing means a score above 550", font_size=22),
            label(r"with 60 pupils a school, \ Laplace is already as good as AGQ", font_size=22, color=HIT),
            label(r"the GEE coefficients are smaller: \ a different question, \ not an error", font_size=22, color=POOLED),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part 24's forty schools again, with passing meaning a score above five fifty. "
            "<bookmark mark='b'/> The Laplace fit gives a programme effect of point four three eight on the log odds, a school "
            "standard deviation of point seven oh. <bookmark mark='c'/> Ten-node quadrature agrees to the third decimal: with "
            "sixty pupils per school, each integrand is nearly normal already. With five pupils per school, they would "
            "differ. <bookmark mark='d'/> Part 24's GEE estimates were smaller, point four oh five, and that is not an "
            "error: it answers a different question."
        ) as vo:
            self.add(simulated_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[1]))
            vo.wait_until("c")
            self.play(FadeIn(tb[2]), FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(tb[3]), FadeIn(foot[2]))
        self.clear_scene()

    def marginal(self):
        d = load("glmm")
        b1 = d["agq"]["beta"][1]
        s = 2.0  # drawn with a large school SD so the flattening is visible
        A = axes([-4, 4], [0, 1], x_length=7.2, y_length=4.4, xlabel=r"linear predictor $x^\top\beta$", ylabel=r"P(pass)",
                 xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.5, 1], center=[-2.0, 0.3, 0])
        ax = A.ax
        x = np.linspace(-4, 4, 200)
        us = np.array([-1.5, -0.75, 0, 0.75, 1.5]) * s
        cond = VGroup(*[curve(ax, x, special.expit(x + u), GREY_B, 1.8) for u in us])
        gx, gw = np.polynomial.hermite.hermgauss(40)
        marg = np.array([np.sum(gw * special.expit(t + np.sqrt(2) * s * gx)) / np.sqrt(np.pi) for t in x])
        cm = curve(ax, x, marg, PATH, 4)
        c0 = curve(ax, x, special.expit(x), SHRUNK, 4)
        rows = fit_rows(VGroup(
            label(r"grey: \ schools with different $u_g$", font_size=22, color=GREY_B),
            label(r"green: \ the typical school, \ $u = 0$", font_size=22, color=SHRUNK),
            label(r"yellow: \ averaged over schools: \ flatter", font_size=22, color=PATH),
            label(r"drawn for $s = 2$; \ the schools' $\hat s = 0.71$", font_size=20, color=GREY_A),
            label(rf"slope ratio $\approx \sqrt{{1 + 0.346\,s^2}} = {d['approx']:.3f}$", font_size=22),
            label(rf"observed: \ {b1:.3f} / {d['gee'][1]:.3f} = {d['ratio']:.3f}", font_size=22, color=HIT),
        ), 4.4, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The mixed model's coefficients are conditional: they describe a pupil's odds within"
            " a given school. Each grey curve is a school. <bookmark mark='b'/> Green is the typical school. "
            "<bookmark mark='c'/> Averaging the curves over all schools gives the yellow curve, a population-averaged"
            " probability. GEE fits a working marginal mean; a logistic-normal mixture need not be exactly logistic, "
            "and an average of steep logistic curves is a flatter one; the picture uses a large school spread to make"
            " the flattening visible. <bookmark mark='d'/> Its slope is smaller by about the square root of one plus "
            "point three four six times the school variance, a result of Scott Zeger, Kung-Yee Liang and Paul Albert."
            " <bookmark mark='e'/> The predicted and observed ratios happen to be close here. Noncollapsibility, "
            "mean-model approximation and different working targets all matter; this is not an exact conversion or a "
            "causal policy effect."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in cond], lag_ratio=0.2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c0), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cm), FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def league_funnel(self):
        d = load("league")
        n, raw, pbar = np.asarray(d["n"]), np.asarray(d["raw"]), d["pbar"]
        A = axes([0, 950], [0, 0.18], x_length=7.4, y_length=4.6, xlabel=r"operations per year", ylabel=r"death rate",
                 xticks=[0, 300, 600, 900], yticks=[0, 0.05, 0.1, 0.15], center=[-2.0, 0.3, 0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        nn = np.linspace(12, 950, 300)
        lims = VGroup()
        for z, op in ((1.96, 0.9), (3.09, 0.5)):
            for sg in (1, -1):
                yv = pbar + sg * z * np.sqrt(pbar * (1 - pbar) / nn)
                lims.add(clip_curve(ax, nn, yv, GREY_A, 1.8, ymin=0, ymax=0.18).set_stroke(opacity=op))
        mean = DashedLine(ax.c2p(0, pbar), ax.c2p(950, pbar), color=TRUE, stroke_width=2)
        top = set(d["top_raw"])
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=RES if i in top else RAW) for i, (a, b) in enumerate(zip(n, raw))])
        rows = fit_rows(VGroup(
            label(r"the World's 60 hospitals: \ deaths after one operation", font_size=22),
            label(rf"gold: \ the average, \ {100 * pbar:.1f}\%", font_size=22, color=TRUE),
            label(r"grey: \ approximate normal 95\% and 99.8\% limits", font_size=22, color=GREY_A),
            label(r"red: \ the five `worst' by raw rate", font_size=22, color=RES),
            label(r"the top two: \ 19 operations each, \ 3 and 2 deaths", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Shrinkage matters most where rankings carry consequences. The World's sixty "
            "hospitals each perform an operation between seventeen and nearly nine hundred times a year, and "
            "newspapers rank them by death rate. <bookmark mark='b'/> The average is four point one percent. "
            "<bookmark mark='c'/> David Spiegelhalter's funnel plot draws the range an average hospital would show by"
            " chance, wide for small hospitals and narrow for large ones. <bookmark mark='d'/> The five worst "
            "hospitals by raw rate, in red, <bookmark mark='e'/> are led by two tiny ones, nineteen operations each, "
            "where three deaths make a rate of sixteen percent and two make eleven. Both sit inside the outer funnel:"
            " the normal reference is compatible with chance. It is only an approximation, especially for such small "
            "expected counts."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.02), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(x) for x in lims], lag_ratio=0.1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(*[dots[i].animate.scale(1.6) for i in top], FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def league_table(self):
        d = load("league")
        n = np.asarray(d["n"])
        raw, sh, tr = np.asarray(d["raw"]), np.asarray(d["shrunk"]), np.asarray(d["truth"])
        worst = set(np.argsort(-tr)[:10])
        hdr = [r"\textbf{rank}", r"\textbf{raw: \ hospital}", r"\textbf{$n$}", r"\textbf{rate}", r"\textbf{shrunk: \ hospital}", r"\textbf{$n$}", r"\textbf{rate}"]
        body = []
        for k, (a, b) in enumerate(zip(d["top_raw"], d["top_shrunk"])):
            ma = r"\ $\bullet$" if a in worst else r""
            mb = r"\ $\bullet$" if b in worst else r""
            body.append([f"{k + 1}", rf"H{a + 1}{ma}", f"{n[a]}", f"{100 * raw[a]:.1f}\\%", rf"H{b + 1}{mb}", f"{n[b]}", f"{100 * sh[b]:.1f}\\%"])
        tb = table_rows([hdr] + body, font_size=24, col_buff=0.55, row_buff=0.24)
        for r_ in tb[1:]:
            for j in (1, 2, 3):
                r_[j].set_color(RAW)
            for j in (4, 5, 6):
                r_[j].set_color(SHRUNK)
        tb[0].set_color(GREY_A)
        tb.move_to([0, 1.0, 0])
        foot = fit_rows(VGroup(
            label(r"$\bullet$: \ truly among the 10 worst", font_size=22),
            label(rf"raw top five: \ {d['raw_hits']} of 5 truly bad; \ shrunk top five: \ {d['shrunk_hits']} of 5", font_size=22, color=HIT),
            label(rf"mean squared error of the rates: \ {d['mse_raw'] / d['mse_shrunk']:.1f} times smaller after shrinking", font_size=22, color=HIT),
            label(rf"rank correlation with the truth: \ raw {d['rank_raw']:.2f}, \ shrunk {d['rank_shrunk']:.2f}", font_size=22, color=RES),
        ), 12.0, 0.22, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fit a random-intercept logistic model with no predictors and rank the hospitals by "
            "their shrunk rates. <bookmark mark='b'/> The raw table's five worst include one hospital truly among the"
            " ten worst; the shrunk table's include two, and every one of its five has at least two hundred "
            "operations, where a high rate is evidence. The tiny hospitals drop out: two deaths in nineteen "
            "operations is not evidence of a bad hospital by itself: small samples are noisy, and these results do "
            "not rule out a truly high underlying risk. <bookmark mark='c'/> Over all sixty, these rates, obtained by"
            " transforming conditional modes rather than posterior mean probabilities, are about seven times closer "
            "to the truth in mean squared error. <bookmark mark='d'/> But look at the ranks: even shrunk, their "
            "correlation with the true ranking is only point three eight. With true differences this small, a league "
            "table is mostly noise, as Harvey Goldstein and David Spiegelhalter warned in 1996; report intervals for "
            "ranks, not ranks."
        ) as vo:
            self.add(simulated_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r_) for r_ in tb[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot[3]))
        self.clear_scene()
