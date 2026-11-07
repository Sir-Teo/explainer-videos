from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403


class Parametric(VoiceoverScene):
    def construct(self):
        self.card()
        self.aft()
        self.likelihood()
        self.weibull()
        self.fits()
        self.curves()
        self.cure()

    def card(self):
        card = chapter_card(12, r"Parametric and AFT models", r"When the shape is worth assuming", lit=(1972,), part=PART)
        with self.voiceover("Chapter twelve. Parametric and accelerated failure time models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def aft(self):
        rows = [
            cmath(r"\log T", r"=", r"x^\top \gamma + \sigma W", font_size=34),
            cmath(r"S(t \mid x)", r"=", r"S_0\big(t\, e^{-x^\top \gamma}\big)", font_size=32),
            cmath(r"e^{\gamma_j}", r":", r"\text{the factor by which time is stretched}", font_size=30),
            cmath(r"W", r":", r"\text{extreme value (Weibull), \ normal (log-normal), \ logistic (log-logistic)}", font_size=28),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"a regression for log time"), why(r"accelerated failure time"), why(r"a time ratio, \ not a hazard ratio"),
                why(r"the error decides the shape")]
        with self.voiceover(
            "<bookmark mark='a'/> The accelerated failure time model is a linear regression for the log of the lifetime. "
            "<bookmark mark='b'/> Covariates stretch or shrink time: a person's survival curve is the baseline curve with "
            "the clock running faster or slower. <bookmark mark='c'/> So e to the gamma j is a time ratio, which many "
            "find easier to explain than a hazard ratio: this treatment makes remissions last forty percent longer. "
            "<bookmark mark='d'/> The error distribution sets the shape of the hazard."
        ) as vo:
            heading = label('Accelerated failure time models rescale the lifetime clock', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def likelihood(self):
        rows = [
            cmath(r"\ell(\gamma, \sigma)", r"=", r"\textstyle\sum_i \delta_i \log f(x_i) + (1 - \delta_i) \log S(x_i)", font_size=30),
            cmath(r"\text{events}", r":", r"\text{the density at the time}", font_size=30),
            cmath(r"\text{censored}", r":", r"\text{the survival beyond it}", font_size=30),
            cmath(r"\text{then}", r":", r"\text{Part 22's machinery: \ Newton, \ information, \ LR tests, \ AIC}", font_size=30),
        ]
        rows[0][-1].set_color(SURVC)
        whys = [why(r"chapter 2's likelihood"), why(r"fully seen"), why(r"at least this long"), why(r"likelihood in depth")]
        with self.voiceover(
            "<bookmark mark='a'/> A parametric model is fitted by chapter two's likelihood: <bookmark mark='b'/> the "
            "density for each observed event, <bookmark mark='c'/> the survival function for each censored time. "
            "<bookmark mark='d'/> Then everything from Part twenty-two applies: Newton's method, the observed "
            "information for standard errors, likelihood ratio tests and Akaike's criterion."
        ) as vo:
            heading = label('Events contribute density; censoring contributes survival', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def weibull(self):
        rows = [
            cmath(r"\text{Weibull}", r":", r"h(t \mid x) = k \lambda^{-k} t^{k-1} e^{x^\top \beta}", font_size=30),
            cmath(r"\text{both}", r":", r"\text{proportional hazards \ and \ accelerated failure time}", font_size=30),
            cmath(r"\beta", r"=", r"-\gamma / \sigma, \ \ k = 1/\sigma", font_size=32),
            cmath(r"\text{the only such family}", r":", r"\text{(with the exponential, \ its special case)}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"Weibull (1951)"), why(r"two readings of one model"), why(r"translate between them"), why(r"a theorem")]
        with self.voiceover(
            "<bookmark mark='a'/> The Weibull distribution, named for the Swedish engineer Waloddi Weibull, is "
            "special. <bookmark mark='b'/> It is both a proportional hazards model and an accelerated failure time "
            "model, <bookmark mark='c'/> with the hazard ratio coefficient equal to minus the time coefficient over "
            "the scale. <bookmark mark='d'/> Within the regular nondegenerate continuous families with a common AFT "
            "scale and freely varying covariates, it is the only family, with its special case the exponential, that "
            "is both, so Weibull hazard ratios can be compared directly with Cox's."
        ) as vo:
            heading = label('The regular Weibull model has both AFT and PH forms', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fits(self):
        d = load("veteran")
        names = {"exponential": r"exponential", "weibull": r"Weibull", "lognormal": r"log-normal", "loglogistic": r"log-logistic"}
        rows = [[r"VA trial: \ Karnofsky + treatment", r"time ratio, \ +10 points", r"$\hat\sigma$", r"AIC"]]
        best = min(d["aft"], key=lambda k: d["aft"][k]["aic"])
        for k in ("exponential", "weibull", "lognormal", "loglogistic"):
            a = d["aft"][k]
            rows.append([names[k], f"{np.exp(a['coef'][1]):.2f}", f"{a['sigma']:.2f}", f"{a['aic']:.1f}"])
        cols = [GREY_A] + [BANDC if k == best else None for k in ("exponential", "weibull", "lognormal", "loglogistic")]
        tab = table_rows(rows, font_size=28, col_buff=0.9, row_buff=0.34, colors=cols).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"Weibull's implied HR per 10 points: \ {d['weibull_hr_karno']:.2f}, \ against Cox's {d['hr_karno10']:.2f}", font_size=24, color=TAUC),
            label(r"lowest AIC among these four models; not a test of proportional hazards", font_size=24, color=BANDC),
        ), 12.4, 0.3, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The veterans' data under four models. <bookmark mark='b'/> Ten Karnofsky points stretch "
            "survival time by a factor of about one point four to one point five in every model. The Weibull's scale is "
            "close to one, so it is nearly exponential, and its implied hazard ratio, " + say(d["weibull_hr_karno"], 2)
            + ", matches Cox's. <bookmark mark='c'/> By Akaike's criterion the log-logistic fits best: its hazard rises"
            " and then falls, a descriptive fit here, not proof of a particular selection mechanism."
        ) as vo:
            self.add(veteran_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(r) for r in tab[1:]], FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def curves(self):
        d = load("veteran")
        grid = np.asarray(d["grid"], float)
        A = axes([0, 600], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"days", ylabel=r"survival",
                 xticks=[0, 200, 400, 600], yticks=[0, 0.5, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        w40, w80 = (np.asarray(d["curves"]["weibull"][k], float) for k in ("40", "80"))
        l40, l80 = (np.asarray(d["curves"]["loglogistic"][k], float) for k in ("40", "80"))
        cw = VGroup(polyline(ax, grid, w40, SURVC, 3), polyline(ax, grid, w80, SURVC, 3))
        cl = VGroup(polyline(ax, grid, l40, AREAC, 3), polyline(ax, grid, l80, AREAC, 3))

        def stair(k, col):
            t, s = np.asarray(k["t"], float), np.asarray(k["surv"], float)
            pts = [(0, 1.0)]
            prev = 1.0
            for a, b in zip(t, s):
                if a > 600:
                    break
                pts += [(a, prev), (a, b)]
                prev = b
            m = VMobject(stroke_color=col, stroke_width=2.5, stroke_opacity=0.8)
            m.set_points_as_corners([ax.c2p(a, b) for a, b in pts])
            return m

        k_hi, k_lo = stair(d["km"]["hi"], GREY_B), stair(d["km"]["lo"], GREY_B)
        side = fit_rows(VGroup(
            label(r"grey: \ KM for Karnofsky $\ge 60$ and $< 60$", font_size=22, color=GREY_B),
            label(r"blue: \ Weibull at Karnofsky 40 and 80", font_size=22, color=SURVC),
            label(r"purple: \ log-logistic, \ heavier tail", font_size=22, color=AREAC),
            label(r"parametric curves: \ smooth, \ extrapolate, \ and can be wrong", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Against the Kaplan-Meier curves for the fitter and the frailer men, <bookmark mark='b'/> "
            "the Weibull's curves at scores of forty and eighty, <bookmark mark='c'/> and the log-logistic's, which keep a "
            "heavier tail of long survivors. <bookmark mark='d'/> Parametric models give smooth curves, efficient "
            "estimates and extrapolation beyond the data, which is exactly where they can be most wrong. Health "
            "economists, who need lifetime means, extrapolate anyway, and should show several models."
        ) as vo:
            self.add(veteran_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(k_hi), Create(k_lo), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cw), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def cure(self):
        d = load("gehan")
        rows = [
            cmath(r"S(t)", r"=", r"\pi + (1 - \pi)\, S_u(t)", font_size=34),
            cmath(r"\pi", r":", r"\text{the cured fraction: \ the plateau}", font_size=30),
            cmath(r"6\text{-MP}", r":", rf"\text{{the curve stops at }} {d['mp']['surv'][-1]:.2f}: \ \text{{cured, \ or not followed long enough?}}", font_size=30),
            cmath(r"\text{identifiable}", r":", r"\text{finite follow-up cannot distinguish a plateau from an unobserved tail}", font_size=30),
        ]
        rows[0][-1].set_color(TAUC)
        whys = [why(r"Boag (1949); \ Berkson \& Gage (1952)"), why(r"a mixture"), why(r"Gehan's data"), why(r"a plateau needs time")]
        with self.voiceover(
            "<bookmark mark='a'/> Some diseases are cured in a fraction of patients. A cure model mixes a fraction pi who "
            "will never have the event with others whose survival falls to zero. <bookmark mark='b'/> Pi is the height of "
            "the plateau the curve approaches. <bookmark mark='c'/> The 6-MP curve stops at " + say(d["mp"]["surv"][-1], 2)
            + ": a cured fraction, or simply the end of follow-up? <bookmark mark='d'/> Thirty-five weeks cannot say. "
            "Nonparametric identification requires enough follow-up to distinguish a genuine cured fraction from a "
            "long tail. A finite plateau alone does not suffice; parametric extrapolation adds assumptions."
        ) as vo:
            heading = label('A finite survival plateau does not establish a cured fraction', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
