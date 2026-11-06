from __future__ import annotations

import numpy as np

from explainer.stats.kit import spatial as SPK
from videos.stats.stats39.common import *  # noqa: F403


class Matern(VoiceoverScene):
    def construct(self):
        self.card()
        self.family()
        self.curves()
        self.spectrum()
        self.stein()
        self.ridge()
        self.zhang()
        self.ridge_pred()

    def card(self):
        card = chapter_card(5, r"Mat\'ern and identifiability", r"What can one field tell us?", lit=(1960, 1999, 2004), part=PART)
        with self.voiceover("Chapter five. Matérn, and what cannot be learned."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def family(self):
        rows = [
            cmath(r"C(h)", r"=", r"\sigma^2 \tfrac{2^{1-\nu}}{\Gamma(\nu)} \big(\sqrt{2\nu}\, h/\rho\big)^\nu K_\nu\big(\sqrt{2\nu}\, h/\rho\big)", font_size=30),
            cmath(r"\nu = \tfrac12", r":", r"\sigma^2 e^{-h/\rho} \quad \nu = \tfrac32: \ \sigma^2 (1 + \sqrt3 h/\rho) e^{-\sqrt3 h/\rho}", font_size=28),
            cmath(r"\text{smoothness}", r":", r"W \text{ is } k \text{ times mean-square differentiable iff } \nu > k", font_size=28),
            cmath(r"\nu \to \infty", r":", r"\sigma^2 e^{-h^2/2\rho^2}: \ \text{the Gaussian covariance}", font_size=28),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"Bertil Mat\'ern (1960), \ forests"), why(r"half-integers: \ closed forms"), why(r"$\nu$ controls the roughness"),
                why(r"the limit")]
        with self.voiceover(
            "<bookmark mark='a'/> Bertil Matérn, a Swedish forester, wrote down this family in his 1960 thesis on the "
            "spatial variation of forests. It has a variance sigma squared, a range rho, and a smoothness nu, with K nu a "
            "modified Bessel function. <bookmark mark='b'/> At half-integers it has closed forms: the exponential at one "
            "half, and at three halves an exponential times a linear term. <bookmark mark='c'/> The point of nu: the field "
            "is k times differentiable exactly when nu exceeds k. <bookmark mark='d'/> As nu grows without bound, the "
            "Matérn becomes the Gaussian covariance, infinitely smooth."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curves(self):
        A = axes([0, 3], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"distance $h$ \ (in units of $\rho$)", ylabel=r"correlation",
                 xticks=[0, 1, 2, 3], yticks=[0, 0.5, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        hs = np.linspace(0.0005, 3, 160)
        cols = [FIELDC, TAUC, BANDC, PTC]
        nus = [0.5, 1.5, 2.5, 20.0]
        cs = [polyline(ax, hs, SPK.matern(hs, 1.0, 1.0, nu), c, 3) for nu, c in zip(nus, cols)]
        side = fit_rows(VGroup(
            label(r"$\nu = 1/2$: \ a corner at zero", font_size=22, color=FIELDC),
            label(r"$\nu = 3/2$", font_size=22, color=TAUC),
            label(r"$\nu = 5/2$", font_size=22, color=BANDC),
            label(r"$\nu = 20$: \ nearly Gaussian, \ flat at zero", font_size=22, color=PTC),
            label(r"the behaviour near zero \ is the smoothness", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The correlation curves, with range one. The exponential leaves zero with a corner: a "
            "linear drop, the signature of a rough field. <bookmark mark='b'/> At three halves <bookmark mark='c'/> and five "
            "halves the curve leaves zero flat, <bookmark mark='d'/> and at nu equal twenty it is nearly the Gaussian "
            "curve. <bookmark mark='e'/> The shape near zero is what determines the smoothness; the tail determines how far "
            "dependence reaches. Prediction depends mostly on the first."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(Create(cs[k]), FadeIn(side[k]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def spectrum(self):
        rows = [
            cmath(r"f(\omega)", r"\propto", r"\big(2\nu/\rho^2 + \|\omega\|^2\big)^{-(\nu + d/2)}", font_size=32),
            cmath(r"\|\omega\| \to \infty", r":", r"f(\omega) \sim \|\omega\|^{-(2\nu + d)}", font_size=30),
            cmath(r"\text{so}", r":", r"\nu \text{ sets how fast high frequencies die out}", font_size=30),
            cmath(r"\text{Whittle (1954)}", r":", r"(\kappa^2 - \Delta)^{(\nu + d/2)/2} W = \text{white noise}", font_size=30),
        ]
        rows[3][-1].set_color(FIELDC)
        whys = [why(r"the Mat\'ern spectrum"), why(r"a power law"), why(r"roughness is high-frequency power"),
                why(r"an SPDE: \ chapter 8")]
        with self.voiceover(
            "<bookmark mark='a'/> By Bochner's theorem, the Matérn has a spectrum, and it is simple: an inverse power of "
            "a constant plus the squared frequency. <bookmark mark='b'/> At high frequency it decays like a power law, "
            "<bookmark mark='c'/> and nu sets the exponent: a smooth field has little power at high frequencies. <bookmark "
            "mark='d'/> Peter Whittle noticed in 1954 that the Matérn field solves a stochastic partial differential "
            "equation driven by white noise, which will make it fast in chapter eight."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def stein(self):
        q = VGroup(
            label(r"\emph{``Use the Mat\'ern model.''}", font_size=30, color=TAUC),
            label(r"Michael Stein, \ \emph{Interpolation of Spatial Data} \ (1999)", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.25).move_to([0, 1.8, 0])
        rows = fit_rows(VGroup(
            label(r"infill asymptotics: \ more and more data in a fixed region", font_size=26, color=FIELDC),
            label(r"kriging is asymptotically efficient \ under a wrong covariance \ if its high-frequency behaviour is right", font_size=26),
            label(r"so what matters is the smoothness \ and the behaviour near zero, \ not the range", font_size=26, color=BANDC),
            label(r"and the Gaussian covariance gets the smoothness badly wrong", font_size=26, color=MISSC),
        ), 12.4, 0.45, [0, -0.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Michael Stein's book of 1999 has a famous summary: use the Matérn model. <bookmark "
            "mark='b'/> His argument uses infill asymptotics, where data accumulate in a fixed region, which is the honest "
            "picture for one island or one mine. <bookmark mark='c'/> Under infill, kriging with a wrong covariance is still "
            "asymptotically efficient, provided the wrong covariance has the right high-frequency behaviour. <bookmark "
            "mark='d'/> So the smoothness matters, and the range much less. <bookmark mark='e'/> And the Gaussian "
            "covariance, which forces infinite smoothness, gets exactly the important thing wrong."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def ridge(self):
        d = load("ident")
        rho, sig = np.asarray(d["rho"], float), np.asarray(d["sigma2"], float)
        xm = float(np.ceil(np.percentile(rho, 98) / 0.2) * 0.2)
        ym = float(np.ceil(np.percentile(sig, 98) / 1.0) * 1.0)
        A = axes([0, xm], [0, ym], x_length=7.0, y_length=4.4, xlabel=r"estimated range $\hat\rho$", ylabel=r"estimated variance $\hat\sigma^2$",
                 xticks=list(np.round(np.linspace(0, xm, 5), 2)), yticks=list(np.round(np.linspace(0, ym, 5), 1)),
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.6, 0.1, 0])
        ax = A.ax
        k = (rho <= xm) & (sig <= ym)
        dots = scatter(ax, rho[k], sig[k], FIELDC, 0.05)
        truth = Dot(ax.c2p(d["rho0"], d["s0"]), radius=0.1, color=TRUEC)
        rs = np.linspace(0.02, xm, 100)
        line = clip_curve(ax, rs, d["micro0"] * rs, BANDC, 3, ymax=ym)
        side = fit_rows(VGroup(
            label(rf"{d['reps']} fields, \ {d['n']} points in the unit square", font_size=22),
            label(rf"exponential, \ true $\rho = {d['rho0']}$, \ $\sigma^2 = {d['s0']:g}$ \ (gold)", font_size=22, color=TRUEC),
            label(rf"ML estimates scatter along a ridge: \ CV {100 * d['cv_rho']:.0f}\% and {100 * d['cv_sig']:.0f}\%", font_size=22, color=FIELDC),
            label(r"green: \ $\sigma^2/\rho$ held at its true value", font_size=22, color=BANDC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> An experiment. Eighty fields, each observed at three hundred random points in the unit "
            "square, with an exponential covariance of range point three and variance one. <bookmark mark='b'/> Fit each "
            "by maximum likelihood, and plot the estimated range against the estimated variance. <bookmark mark='c'/> The "
            "estimates do not cluster around the truth; they scatter along a ridge, each varying by " + str(round(100 * d["cv_rho"]))
            + " and " + str(round(100 * d["cv_sig"])) + " percent. <bookmark mark='d'/> The ridge is the green line, along "
            "which the ratio of variance to range stays at its true value."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]), FadeIn(truth), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(dots))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(line), FadeIn(side[3]))
        self.clear_scene()

    def zhang(self):
        d = load("ident")
        rows = [
            cmath(r"\text{Zhang (2004)}", r":", r"\sigma^2 \text{ and } \rho \text{ cannot both be estimated consistently under infill}", font_size=28),
            cmath(r"\text{but}", r":", r"\sigma^2 / \rho^{2\nu} \text{ can: \ the microergodic parameter}", font_size=30),
            cmath(r"\text{here}", r":", rf"\text{{CV of }} \hat\sigma^2/\hat\rho = {100 * d['cv_micro']:.0f}\% \ \text{{against}} \ {100 * d['cv_rho']:.0f}\% \text{{ for }} \hat\rho", font_size=30),
            cmath(r"\text{and}", r":", r"\text{predictions depend on it, \ not on the two separately}", font_size=30),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"equivalent Gaussian measures"), why(r"for the Mat\'ern, \ $d \le 3$"), why(r"the ridge, \ measured"),
                why(r"so kriging still works")]
        with self.voiceover(
            "<bookmark mark='a'/> Hao Zhang proved in 2004 that this is not a failure of the method. Under infill, Matérn "
            "fields with different variances and ranges can be mathematically indistinguishable, so no estimator gets both "
            "right however much data there are. <bookmark mark='b'/> What can be estimated is the combination sigma "
            "squared over rho to the two nu, called the microergodic parameter. <bookmark mark='c'/> In the experiment its "
            "estimate varies by only " + str(round(100 * d["cv_micro"])) + " percent. <bookmark mark='d'/> And predictions "
            "depend on that combination, so kriging works even though its parameters are not identified. A parameter that "
            "no amount of data can pin down, and that does not matter."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ridge_pred(self):
        d = load("ridge_pred")
        names = [r"the true covariance", r"on the ridge: \ $\rho \times 2$, \ $\sigma^2 \times 8$", r"on the ridge: \ $\rho \times 0.7$, \ $\sigma^2 \times 0.34$",
                 r"off it: \ $\rho \times 2$ only", r"off it: \ $\rho \times 0.5$ only"]
        rows = [[r"kriging the World with $\nu = 3/2$", r"RMSE", r"mean SE", r"90\% coverage"]]
        for n, r in zip(names, d["rows"]):
            rows.append([n, f"{r['rmse']:.2f}", f"{r['mean_sd']:.2f}", f"{100 * r['cover']:.0f}\\%"])
        tab = table_rows(rows, font_size=26, col_buff=0.7, row_buff=0.32, colors=[GREY_A, TRUEC, BANDC, BANDC, MISSC, MISSC]).move_to([0, 0.7, 0])
        if tab.width > 12.6:
            tab.width = 12.6
        foot = label(r"for $\nu = 3/2$ the ridge holds $\sigma^2/\rho^3$ fixed: \ predictions and their errors stay put along it", font_size=22, color=TAUC).move_to([0, -2.4, 0])
        r = d["rows"]
        with self.voiceover(
            "<bookmark mark='a'/> The World shows why it does not matter. Krige its field with the true covariance: the "
            "error over the island is " + say(r[0]["rmse"], 2) + ", and the intervals cover " + str(round(100 * r[0]["cover"]))
            + " percent. <bookmark mark='b'/> Now double the range and multiply the variance by eight, which keeps the "
            "microergodic parameter fixed. The predictions, their standard errors and the coverage barely move. "
            "<bookmark mark='c'/> The same on the other side of the ridge. <bookmark mark='d'/> But double the range "
            "alone, leaving the ridge, and the standard errors shrink and coverage falls to " + str(round(100 * r[3]["cover"]))
            + " percent; <bookmark mark='e'/> halve it, and the intervals become too wide. The data cannot tell points on "
            "the ridge apart, and neither can the predictions."
        ) as vo:
            self.add(pollution_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 2]))
            self.play(FadeIn(foot))
        self.clear_scene()
