from __future__ import annotations

import numpy as np

from videos.stats.stats29.common import *  # noqa: F403


class Lambda(VoiceoverScene):
    def construct(self):
        self.card()
        self.gcv()
        self.mixed()
        self.bayes_band()
        self.curves()
        self.fits()
        self.race()
        self.which()

    def card(self):
        card = chapter_card(7, r"Choosing $\lambda$", r"GCV, \ REML, \ and splines as mixed models", lit=(1979,), part=PART)
        with self.voiceover("Chapter seven. Choosing lambda."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def gcv(self):
        rows = [
            cmath(r"\text{LOO}", r":", r"\tfrac1n \textstyle\sum_i \bigl(\tfrac{y_i - \hat g(x_i)}{1 - S_{ii}}\bigr)^2", font_size=30),
            cmath(r"\text{GCV}(\lambda)", r"=", r"\dfrac{\tfrac1n \|y - S_\lambda y\|^2}{(1 - \mathrm{tr}\, S_\lambda / n)^2}", font_size=30),
            cmath(r"\text{aim}", r":", r"\text{prediction error, \ as Part 28}", font_size=30),
            cmath(r"\text{risk}", r":", r"\text{a flat criterion can land on interpolation}", font_size=30),
        ]
        rows[1][2].set_color(SPLC)
        whys = [why(r"exact for a linear smoother"), why(r"Craven \& Wahba (1979)"), why(r"invariant to rotations of the data"),
                why(r"occasional severe undersmoothing")]
        with self.voiceover(
            "<bookmark mark='a'/> First, Part 28's tools. A smoothing spline is a linear smoother, so its leave-one-out error "
            "needs no refitting. <bookmark mark='b'/> Craven and Wahba invented generalized cross-validation for exactly this "
            "problem in 1979: replace each leverage by the average, one minus the degrees of freedom over n. "
            "<bookmark mark='c'/> It aims at prediction error. <bookmark mark='d'/> Its weakness is variability: its "
            "minimum can be flat, and now and then it chooses a nearly interpolating spline."
        ) as vo:
            intro=label('GCV replaces individual leverages by their average',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mixed(self):
        rows = [
            cmath(r"y", r"=", r"X\beta + Zu + \varepsilon, \ \ u \sim N(0, \tfrac{\sigma^2}{\lambda} I)", font_size=30),
            cmath(r"\text{BLUP of } X\beta + Zu", r"=", r"\text{the spline fit}", font_size=30),
            cmath(r"\lambda", r"=", r"\sigma^2 / \sigma_u^2: \ \text{a variance ratio}", font_size=30),
            cmath(r"\text{REML}", r":", r"\text{estimate it like any variance component}", font_size=30),
        ]
        rows[3][2].set_color(SPLC)
        whys = [why(r"lines fixed; \ $Z_j=u_j/\sqrt{d_j}$, \ random coefficients"), why(r"Part 25's BLUPs"),
                why(r"noise over signal"), why(r"Wahba (1985): \ generalized ML; \ Speed (1991)")]
        with self.voiceover(
            "<bookmark mark='a'/> Second, Part 25's tools. Write the spline as a mixed model: the constant and line "
            "as fixed effects, and rescaled wiggly basis columns u j divided by root d j, with independent random "
            "coefficients of variance sigma squared over lambda. <bookmark mark='b'/> The best linear unbiased "
            "predictor of the curve is then exactly the smoothing spline. <bookmark mark='c'/> Lambda is a ratio of "
            "variances, noise over signal. <bookmark mark='d'/> So it can be estimated by restricted maximum "
            "likelihood like any variance component, Grace Wahba's generalized maximum likelihood of 1985, and the "
            "reason mixed-model software fits splines."
        ) as vo:
            intro=label('Rescaled spline basis coefficients form a variance-component model',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curves(self):
        d = load("spline")
        df = np.asarray(d["df"])
        gcv = np.asarray(d["gcv"])
        reml = np.asarray(d["reml"])
        keep = (df > 4) & (df < 40)
        g = gcv[keep]
        r = reml[keep]
        gs = (g - g.min()) / (np.quantile(g, 0.9) - g.min())
        rs = (r - r.min()) / (np.quantile(r, 0.9) - r.min())
        A = axes([4, 40], [0, 1.1], x_length=7.4, y_length=4.4, xlabel=r"degrees of freedom", ylabel=r"criterion (rescaled)",
                 xticks=[5, 10, 20, 30, 40], yticks=[], center=[-2.0, 0.3, 0])
        ax = A.ax
        lg = polyline(ax, df[keep], gs, SPLC, 3)
        lr = polyline(ax, df[keep], rs, NWC, 3)
        dg = Dot(ax.c2p(d["df_gcv"], 0), radius=0.08, color=SPLC)
        dr = Dot(ax.c2p(d["df_reml"], 0), radius=0.08, color=NWC)
        rows = fit_rows(VGroup(
            label(r"the motorcycle data", font_size=22),
            label(rf"green: \ GCV: \ minimum at df {d['df_gcv']:.1f}", font_size=22, color=SPLC),
            label(rf"orange: \ REML: \ minimum at df {d['df_reml']:.1f}", font_size=22, color=NWC),
            label(r"REML includes within-time replicate contrasts", font_size=20, color=GREY_B),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the motorcycle data, both criteria against degrees of freedom. <bookmark "
            "mark='b'/> GCV's minimum is at about twelve and a half. <bookmark mark='c'/> REML's at about fourteen, "
            "<bookmark mark='d'/> computed from all observations, including independent replicate contrasts at tied "
            "times. These criteria favor smoother fits in this example; they do not test whether the visible features"
            " are real."
        ) as vo:
            self.add(mcycle_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lg), FadeIn(dg), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(lr), FadeIn(dr), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def fits(self):
        d = load("spline")
        t, a, tt = np.asarray(d["t"]), np.asarray(d["a"]), np.asarray(d["tt"])
        A = axes([0, 60], [-150, 90], x_length=7.4, y_length=4.4, xlabel=r"milliseconds after impact",
                 ylabel=r"head acceleration ($g$)", xticks=[0, 20, 40, 60], yticks=[-100, 0, 50], center=[-2.0, 0.3, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(x, y), radius=0.045, color=WHITE, fill_opacity=0.7) for x, y in zip(t, a)])
        fg = curve(ax, tt, np.asarray(d["fit_gcv"]), SPLC, 4)
        fr = DashedVMobject(curve(ax, tt, np.asarray(d["fit_reml"]), NWC, 3), num_dashes=60)
        rows = fit_rows(VGroup(
            label(r"green: \ the GCV spline", font_size=22, color=SPLC),
            label(r"orange dashed: \ REML's", font_size=22, color=NWC),
            label(rf"residual SD {d['sigma_gcv']:.1f} $g$: \ but small early, \ large later", font_size=22, color=RES),
            label(r"one $\lambda$, \ constant noise: \ both assumed", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The two fits, almost the same curve. <bookmark mark='b'/> REML's is a touch wigglier. "
            "<bookmark mark='c'/> Their residual standard deviation is about twenty-three g, but the scatter is tiny in the "
            "first fifteen milliseconds and large afterwards. <bookmark mark='d'/> A single lambda and constant noise are both "
            "assumptions here; adaptive smoothers, with lambda varying along the curve, and weighted fits relax them."
        ) as vo:
            self.add(mcycle_tag())
            self.play(FadeIn(A), FadeIn(pts))
            vo.wait_until("a")
            self.play(Create(fg), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(fr), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def race(self):
        d = load("lamsim")
        s = d["summary"]
        hdr = [r"\textbf{criterion}", r"\textbf{chosen df: \ 10\%, \ median, \ 90\%}", r"\textbf{mean error}", r"\textbf{worst 5\% error}"]
        spec = (("oracle", r"oracle (true error)"), ("gcv", r"GCV"), ("reml", r"REML"))
        body = [[t, f"{s[k]['df_q10']:.1f}, \\ {s[k]['df_median']:.1f}, \\ {s[k]['df_q90']:.1f}", f"{s[k]['mse']:.4f}",
                 f"{s[k]['worst5']:.4f}"] for k, t in spec]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.32, colors=[GREY_A, TRUE, SPLC, NWC])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"{d['R']} data sets: \ $n = {d['n']}$, \ noise SD {d['sigma']}, \ a smooth curve with a ripple", font_size=22),
            label(r"REML: \ tighter, \ and fewer bad days \ (Wahba 1985; \ Reiss \& Ogden 2009)", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Which is better? Three hundred simulated data sets, scored against the true curve. "
            "<bookmark mark='b'/> The oracle, which knows the truth, picks around eleven degrees of freedom. "
            "<bookmark mark='c'/> GCV centres there too, but its choices spread up to fourteen and a half: on some "
            "data sets it undersmooths. <bookmark mark='d'/> REML's choices are tighter, and its average error, and "
            "especially its worst five percent, are smaller. Philip Reiss and Todd Ogden explained why in 2009: GCV's"
            " criterion has multiple minima more often, and REML is less variable. REML is a common option in modern "
            "GAM software; defaults depend on the package and version."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tb[k + 1]))
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def which(self):
        rows = fit_rows(VGroup(
            label(r"GCV: \ targets prediction, \ no model for the curve", font_size=24, color=SPLC),
            label(r"REML: \ a variance-component model; stable here", font_size=24, color=NWC),
            label(r"the mixed-model view gives intervals too: \ chapter eleven", font_size=24, color=PATH),
            label(r"and lets splines sit inside bigger models: \ GAMs, \ GLMMs", font_size=24, color=KDEC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> GCV targets prediction and needs no model for the curve. <bookmark mark='b'/> REML "
            "treats roughness through a variance-component model, and is more stable in this experiment, rather than "
            "universally. <bookmark mark='c'/> The mixed-model view also gives the spline a posterior, and so "
            "intervals, chapter eleven. <bookmark mark='d'/> And it lets smooth terms sit inside larger models: "
            "additive models, generalized mixed models, Simon Wood's GAM software."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def bayes_band(self):
        rows = [
            cmath(r"g \mid y", r"\sim", r"N\bigl(S_\lambda y, \ \sigma^2 S_\lambda\bigr)", font_size=32),
            cmath(r"\text{band}", r":", r"\hat g(x_i) \pm 1.96\, \hat\sigma \sqrt{S_{ii}}", font_size=30),
            cmath(r"\hat\sigma^2", r"=", r"\|y - S_\lambda y\|^2 / (n - \mathrm{tr}\, S_\lambda)", font_size=30),
            cmath(r"\text{coverage}", r":", r"\text{approximate average coverage under conditions}", font_size=30),
        ]
        rows[0][2].set_color(SPLC)
        whys = [why(r"the posterior, \ with the improper prior on lines"), why(r"Wahba (1983)"),
                why(r"a smoothing approximation, not exact unbiased residual df"), why(r"Nychka (1988): \ across the function, \ not at each point")]
        with self.voiceover(
            "<bookmark mark='a'/> The mixed-model view gives more than lambda. For fixed lambda and sigma, unit "
            "weights and distinct x values, the Gaussian prior with flat linear component gives a normal posterior, "
            "with mean S y and covariance sigma squared S. <bookmark mark='b'/> So a band at each design point is the"
            " fit plus or minus one point nine six sigma hat root S i i, Grace Wahba's Bayesian confidence interval. "
            "<bookmark mark='c'/> The displayed sigma estimate uses n minus trace S as a smoothing approximation; it "
            "is not an exact unbiased residual degrees-of-freedom formula. <bookmark mark='d'/> Nychka studied "
            "approximate average frequentist coverage under smoothness and smoothing assumptions. Neither arbitrary "
            "fixed curves nor every location have guaranteed ninety-five percent coverage; plugging in smoothing and "
            "noise estimates also omits their uncertainty."
        ) as vo:
            intro=label('Conditional Gaussian intervals leave smoothing uncertainty outside the formula',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
