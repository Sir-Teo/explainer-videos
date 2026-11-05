from __future__ import annotations

import numpy as np

from videos.stats.stats22.common import *  # noqa: F403


class Profile(VoiceoverScene):
    def construct(self):
        self.card()
        self.matrix()
        self.landscape()
        self.profile_curve()
        self.nuisance()

    def card(self):
        card = chapter_card(5, r"Many parameters", r"The information matrix and the profile", part=PART)
        with self.voiceover("Chapter five. Many parameters."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def matrix(self):
        d = load("gamma")
        rows = [
            cmath(r"\mathcal I(\theta)", r"=", r"-E\,\nabla^2 \log f(X;\theta), \ \ a \ p \times p \ \text{matrix}", font_size=30),
            cmath(r"\mathrm{Cov}(\hat\theta)", r"\approx", r"\big(n\,\mathcal I(\hat\theta)\big)^{-1}", font_size=30),
            cmath(r"\text{gamma: \ shape } a, \ \text{rate } b", r":", rf"\hat a = {d['a_hat']:.2f}, \ \hat b = {d['b_hat']:.4f}", font_size=30),
            cmath(r"\mathrm{corr}(\hat a, \hat b)", r"=", rf"{d['corr']:.2f}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"curvature in every direction"), why(r"the inverse, \ not the reciprocal of each entry"),
                why(rf"{d['n']} of the World's incomes, \ thousands"), why(r"a long ridge: \ shape and rate trade off")]
        with self.voiceover(
            "<bookmark mark='a'/> With several parameters the information is a matrix: the expected curvature of the log "
            "likelihood in every direction. <bookmark mark='b'/> The estimates' covariance is approximately its inverse, and "
            "it's the inverse of the whole matrix that matters, not the reciprocal of each diagonal entry. "
            "<bookmark mark='c'/> Here's a two-parameter example: a gamma distribution, with a shape and a rate, fitted to a "
            "hundred and fifty of the World's incomes. The shape comes out at two point two eight. <bookmark mark='d'/> The two "
            "estimates are correlated point eight nine: a larger shape and a larger rate fit almost equally well, because both "
            "keep the mean, shape over rate, near the sample's."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def landscape(self):
        d = load("gamma")
        ag, bg = d["a_grid"], d["b_grid"]
        A = axes([ag[0], ag[-1]], [bg[0], bg[-1]], x_length=6.4, y_length=5.2, xlabel=r"shape $a$", ylabel=r"rate $b$",
                 xticks=[1, 2, 3, 4], yticks=[0.02, 0.05, 0.08, 0.11], center=[-2.6, 0.0, 0], font_size=18)
        ax = A.ax
        L = LikelihoodLandscape(ax, np.asarray(d["ll"]), (ag[0], ag[-1]), (bg[0], bg[-1]), color=LIK, stroke_width=1.8)
        ridge = L.ridge(color=PATH)
        pk = L.peak()
        rows = fit_rows(VGroup(
            label(r"contours: \ 0.5 to 50 below the peak", font_size=22, color=LIK),
            label(r"the 1.92 and 3.0 contours: \ 95\% regions (chapter six)", font_size=22, color=GREY_A),
            label(r"gold: \ the ridge, \ the best rate for each shape", font_size=22, color=PATH),
            label(r"along it: \ rate $= a / \bar x$", font_size=22),
        ), 4.6, 0.45, [4.3, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is that likelihood as a landscape: contours of the log likelihood over shape and rate, "
            "from half a unit below the peak down to fifty below. <bookmark mark='b'/> It's a long, tilted ridge, chapter one's "
            "correlation made visible. Two of these contours, one point nine two and three below the peak, will turn out to be "
            "confidence regions. <bookmark mark='c'/> In gold, the profile ridge: for each value of the shape, the rate that "
            "fits best. <bookmark mark='d'/> For the gamma it has a formula, the shape divided by the sample mean."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(L.levels), FadeIn(pk), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ridge), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def profile_curve(self):
        d = load("gamma")
        a, pl = np.asarray(d["prof_a"]), np.asarray(d["prof_ll"])
        top = float(pl.max())
        A = axes([0.8, 4.5], [top - 12, top + 1], x_length=8.0, y_length=4.4, xlabel=r"shape $a$", ylabel=r"profile log likelihood",
                 xticks=[1, 2, 3, 4], yticks=[], center=[-1.6, 0.3, 0])
        ax = A.ax
        m = pl > top - 12
        pc = curve(ax, a[m], pl[m], PATH, 3.5)
        cut = DashedLine(ax.c2p(0.8, top - 1.92), ax.c2p(4.5, top - 1.92), color=TRUE, stroke_width=2)
        lo, hi = d["profile_ci"]
        wl, wh = d["wald"]
        pbar = Line(ax.c2p(lo, top - 1.92), ax.c2p(hi, top - 1.92), color=HIT, stroke_width=6)
        wbar = Line(ax.c2p(wl, top - 6), ax.c2p(wh, top - 6), color=MLE_C, stroke_width=6)
        rows = fit_rows(VGroup(
            label(r"the profile: \ the log likelihood along the ridge", font_size=22, color=PATH),
            label(r"dashed: \ 1.92 below the top $= \chi^2_{1, 0.95}/2$", font_size=22, color=TRUE),
            label(rf"green: \ profile interval [{lo:.2f}, {hi:.2f}]", font_size=22, color=HIT),
            label(rf"blue: \ Wald $\pm 1.96$ SE: \ [{wl:.2f}, {wh:.2f}]", font_size=22, color=MLE_C),
            label(r"the profile follows the curve's real shape", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Walking along the ridge and recording the height gives the profile log likelihood for the "
            "shape: a one-dimensional curve that has already done its best with the rate. <bookmark mark='b'/> Cut it one point "
            "nine two below its peak, half the ninety-fifth percentile of chi-squared with one degree of freedom. "
            "<bookmark mark='c'/> The shapes above the cut form the profile likelihood interval, one point eight three to two "
            "point eight. <bookmark mark='d'/> The Wald interval, plus or minus one point nine six standard errors from the "
            "inverse information matrix, is one point eight oh to two point seven six. <bookmark mark='e'/> Close here, but "
            "the profile follows the likelihood's real, slightly skewed shape, which the Wald interval forces to be symmetric."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(pc), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cut), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(pbar), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(wbar), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def nuisance(self):
        rows = [
            cmath(r"\ell_p(\psi)", r"=", r"\max_\lambda \ell(\psi, \lambda)", font_size=30),
            cmath(r"-2\{\ell_p(\psi_0) - \ell_p(\hat\psi)\}", r"\to", r"\chi^2_{\dim\psi}", font_size=30),
            cmath(r"\text{a warning}", r":", r"\ell_p \text{ is not a real likelihood}", font_size=30),
            cmath(r"\text{fixes}", r":", r"\text{modified profiles (Barndorff-Nielsen; Cox \& Reid 1987)}", font_size=28),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"$\psi$ of interest, \ $\lambda$ a nuisance"), why(r"Wilks (1938): \ chapter six"),
                why(r"it ignores the uncertainty in $\hat\lambda_\psi$"), why(r"they matter when $\dim\lambda$ is large")]
        with self.voiceover(
            "<bookmark mark='a'/> In general, split the parameters into psi, which we care about, and lambda, a nuisance, and "
            "maximize lambda away. <bookmark mark='b'/> Twice the drop in the profile log likelihood has, in large samples, a "
            "chi-squared distribution with as many degrees of freedom as psi has components, which is why the cut works. "
            "<bookmark mark='c'/> But the profile is not a real likelihood: it treats the best lambda for each psi as if it "
            "were known exactly. <bookmark mark='d'/> When there are many nuisance parameters that matters a great deal, and "
            "modified profile likelihoods correct it. Chapter seven shows how badly the plain version can fail."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
