from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats12.common import *  # noqa: F403


class Collinear(VoiceoverScene):
    def construct(self):
        self.card()
        self.vif()
        self.ellipses()
        self.condition()
        self.remedies()

    def card(self):
        card = chapter_card(8, r"Collinearity", r"When the predictors move together", part=PART)
        with self.voiceover("Chapter eight. Collinearity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def vif(self):
        rows = [
            cmath(r"\mathrm{Var}\,\hat\beta_j", r"=", r"\frac{\sigma^2}{\sum_i (x_{ij} - \bar x_j)^2}\cdot\frac{1}{1 - R_j^2}", font_size=34),
            cmath(r"\mathrm{VIF}_j", r"=", r"\frac{1}{1 - R_j^2}", font_size=36),
            cmath(r"\rho = 0.95", r"\Rightarrow", r"\mathrm{VIF} = \frac{1}{1 - 0.9025} \approx 10", font_size=34),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"FWL: \ only the part of $x_j$ the others cannot predict is informative"),
                why(r"the variance inflation factor; \ $R_j^2$: \ $x_j$ on the other predictors"), why(r"standard errors $\sqrt{10} \approx 3$ times larger")]
        with self.voiceover(
            "<bookmark mark='a'/> Frisch–Waugh–Lovell explains collinearity directly. A coefficient is estimated from the part "
            "of its predictor that the other predictors can't explain. Its variance is the simple-regression variance divided "
            "by one minus R-j squared, where R-j squared measures how well the other predictors predict this one. "
            "<bookmark mark='b'/> That factor is the variance inflation factor. <bookmark mark='c'/> If two predictors "
            "correlate point nine five, it's about ten, and both standard errors are about three times as large as they would "
            "be if the predictors were unrelated."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.4, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ellipses(self):
        d = load("collin")
        panels = VGroup()
        for j, (k, ttl) in enumerate((("low", r"$\rho = 0$"), ("high", r"$\rho = 0.95$"))):
            c = d[k]
            A = axes([-0.5, 2.5], [-0.5, 2.5], x_length=4.4, y_length=4.4, xlabel=r"$\hat\beta_1$", ylabel=r"$\hat\beta_2$",
                     xticks=[0, 1, 2], yticks=[0, 1, 2], center=[-3.3 + 6.6 * j, 0.0, 0], font_size=18)
            ax = A.ax
            C = np.asarray(c["cov"])
            m = np.asarray(c["coef"])
            vals, vecs = np.linalg.eigh(C)
            r = np.sqrt(2 * stats.f.ppf(.95, 2, c["df"]))
            ts = np.linspace(0, 2 * np.pi, 120)
            circ = np.stack([np.cos(ts), np.sin(ts)])
            pts_ = (vecs @ np.diag(np.sqrt(vals)) @ circ) * r + m[:, None]
            ell = VMobject(stroke_color=FIT, stroke_width=3, fill_color=FIT, fill_opacity=0.2)
            ell.set_points_as_corners([ax.c2p(a, b) for a, b in pts_.T])
            truth = Star(n=5, outer_radius=0.12, color=EXACT, fill_opacity=1).move_to(ax.c2p(1, 1))
            est = Dot(ax.c2p(*m), radius=0.07, color=OBS)
            sumline = DashedLine(ax.c2p(-0.5, 2.5), ax.c2p(2.5, -0.5), color=GREY_B, stroke_width=1.5)
            info = VGroup(MathTex(rf"\mathrm{{VIF}} = {c['vif'][0]:.1f}", font_size=24),
                          MathTex(rf"\mathrm{{SE}}(\hat\beta_1) = {c['se'][0]:.2f}", font_size=24),
                          MathTex(rf"\mathrm{{SE}}(\hat\beta_1 + \hat\beta_2) = {c['sum_se']:.2f}", font_size=24, color=OBS)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(A, DOWN, buff=0.2)
            panels.add(VGroup(A, ell, truth, est, label(ttl, font_size=26).next_to(A, UP, buff=0.12), info, sumline))
        panels.shift(UP * 0.3)
        tag = simulated_tag(r"simulated: \ $y = 1 + x_1 + x_2 + \varepsilon$, \ $n = 50$", corner=UR)
        with self.voiceover(
            "Here's what it looks like. Two predictors, both with true coefficient one, fifty observations. "
            "<bookmark mark='a'/> When the predictors are unrelated, the ninety-five percent confidence region for the two "
            "coefficients together is nearly a circle, and each standard error is about a tenth. <bookmark mark='b'/> When they "
            "correlate point nine five, the region becomes a long thin ellipse, lying along a diagonal. The individual "
            "standard errors triple, and here the estimates split the effect unevenly, one point two and point six. "
            "<bookmark mark='c'/> But look along the diagonal: the sum of the two coefficients is estimated as precisely as "
            "before, even a little more precisely. The data can't tell the two predictors apart, but they estimate the sum more precisely in this model."
        ) as vo:
            self.play(FadeIn(tag), *[FadeIn(p[0]) for p in panels], *[FadeIn(p[4]) for p in panels], *[FadeIn(p[2]) for p in panels])
            vo.wait_until("a")
            self.play(FadeIn(panels[0][1]), FadeIn(panels[0][3]), FadeIn(panels[0][5][:2]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1][1]), FadeIn(panels[1][3]), FadeIn(panels[1][5][:2]))
            vo.wait_until("c")
            self.play(Create(panels[1][6]), FadeIn(panels[0][5][2]), FadeIn(panels[1][5][2]))
        self.clear_scene()

    def remedies(self):
        rows = fit_rows(VGroup(
            label(r"collinearity is a shortage of information, \ not a bug", font_size=30, color=OBS),
            label(r"the estimates are still unbiased; \ prediction can remain precise along the observed predictor combinations", font_size=24),
            label(r"what you cannot learn: \ the separate effects of things that never vary separately", font_size=24),
            label(r"cures: \ more data, \ data where they vary separately (design, \ Part 13), \ or ask about combinations", font_size=24,
                  color=GREY_A),
            label(r"or accept bias for variance: \ ridge regression (Hoerl \& Kennard, 1970; \ Part 32)", font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Collinearity is a shortage of information, not an error in the method. "
            "<bookmark mark='b'/> The estimates are still unbiased, and collinearity alone need not ruin predictions, as long as the "
            "predictors keep moving together. <bookmark mark='c'/> What you can't learn is the separate effect of things "
            "that never varied separately in your data. <bookmark mark='d'/> The cures: more data; better data, collected so "
            "that the predictors do vary separately, which is design, Part 13; or questions about combinations rather than "
            "separate effects. <bookmark mark='e'/> Or accept a little bias to reduce the variance, Arthur Hoerl and Robert "
            "Kennard's ridge regression, Part 32."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def condition(self):
        rows = [
            cmath(r"\kappa(X)", r"=", r"\frac{\sigma_{\max}}{\sigma_{\min}}", r"\quad\text{singular values (Part 4)}", font_size=34),
            cmath(r"\rho = 0.95", r":", r"\kappa(X^\top X) \approx 39;\qquad \rho = 0.9999:\ \approx 20{,}000", font_size=30),
            cmath(r"\text{digits lost}", r"\approx", r"\log_{10}\kappa", font_size=34),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"how close the columns are to dependent"), why(r"for two standardized predictors: \ $(1 + |\rho|)/(1 - |\rho|)$; \ centred two-column block"),
                why(r"statistical uncertainty (VIF) and numerical error grow together")]
        intro = label('Near dependence also causes numerical sensitivity', font_size=36)
        with self.voiceover(
            "Collinearity also has a numerical face. <bookmark mark='a'/> The condition number of X, its largest singular "
            "value over its smallest, measures how close the columns are to being linearly dependent. "
            "<bookmark mark='b'/> For two standardized predictors with correlation rho, the condition number of X transpose X "
            "for the centred two-predictor Gram block is one plus absolute rho over one minus absolute rho: thirty-nine at point nine five, twenty thousand at point nine nine nine nine. "
            "<bookmark mark='c'/> Roughly, you lose the log, base ten, of the condition number in digits of accuracy. The "
            "statistical cost, the variance inflation factor, and the numerical cost grow together, which is no coincidence: "
            "both measure how little the data say about the separate directions."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.4, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()
