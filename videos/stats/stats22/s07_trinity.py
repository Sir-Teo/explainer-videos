from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats22.common import *  # noqa: F403


class Trinity(VoiceoverScene):
    def construct(self):
        self.card()
        self.picture()
        self.formulas()
        self.invert()
        self.hauck()
        self.board()

    def card(self):
        card = chapter_card(6, r"The trinity", r"Wald, \ score and likelihood ratio", part=PART)
        with self.voiceover("Chapter six. The trinity of tests."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def picture(self):
        d = load("trinity")
        p, ll = np.asarray(d["grid"]), np.asarray(d["ll"])
        top = float(ll.max())
        A = axes([0.3, 0.92], [top - 6, top + 0.6], x_length=8.0, y_length=4.6, xlabel=r"$p$", ylabel=r"log likelihood, \ 14 of 20",
                 xticks=[0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], yticks=[], center=[-1.6, 0.3, 0])
        ax = A.ax
        m = ll > top - 6
        cv = curve(ax, p[m], ll[m], LIK, 3.5)
        l0 = float(14 * np.log(0.5) + 6 * np.log(0.5))
        hat = Dot(ax.c2p(0.7, top), radius=0.08, color=MLE_C)
        null = Dot(ax.c2p(0.5, l0), radius=0.08, color=GREY_A)
        lr = DoubleArrow(ax.c2p(0.72, l0), ax.c2p(0.72, top), buff=0, color=LRC, stroke_width=3, tip_length=0.15)
        wald = DoubleArrow(ax.c2p(0.5, top + 0.3), ax.c2p(0.7, top + 0.3), buff=0, color=WALD, stroke_width=3, tip_length=0.15)
        s0 = d["score0"]
        tan = Line(ax.c2p(0.42, l0 - s0 * 0.08), ax.c2p(0.58, l0 + s0 * 0.08), color=SCORE, stroke_width=3.5)
        rows = fit_rows(VGroup(
            label(r"$H_0$: \ $p = 0.5$; \ observed 14 of 20", font_size=22),
            label(rf"gold: \ LR, \ $2 \times$ the drop: \ ${d['lr']:.2f}$", font_size=22, color=LRC),
            label(rf"blue: \ Wald, \ $(\hat p - p_0)^2/\mathrm{{SE}}^2$: \ ${d['wald']:.2f}$", font_size=22, color=WALD),
            label(rf"teal: \ score, \ the slope at $p_0$: \ ${d['score']:.2f}$", font_size=22, color=SCORE),
            label(rf"p-values: \ {d['p']['lr']:.3f}, \ {d['p']['wald']:.3f}, \ {d['p']['score']:.3f}", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "There are three classical ways to test a value of a parameter, and all three are readings of one curve. "
            "<bookmark mark='a'/> Here's the log likelihood for fourteen successes in twenty trials, and the hypothesis that p "
            "is a half. <bookmark mark='b'/> The likelihood-ratio test measures how far the curve falls from its peak to the "
            "hypothesis: twice the drop is three point two nine. <bookmark mark='c'/> The Wald test measures the horizontal "
            "distance from the estimate to the hypothesis, in standard errors computed at the estimate; squared, that's three "
            "point eight one. <bookmark mark='d'/> The score test looks only at the hypothesis: how steeply the curve is still rising "
            "there, scaled by the information at p one half: three point two. <bookmark mark='e'/> All three are approximately "
            "chi-squared with one degree of freedom, and here they give p-values from point oh five one to point oh seven four, "
            "enough to change a verdict at five percent."
        ) as vo:
            self.play(FadeIn(A), Create(cv))
            vo.wait_until("a")
            self.play(FadeIn(hat), FadeIn(null), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromCenter(lr), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromCenter(wald), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(tan), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def formulas(self):
        rows = [
            cmath(r"W", r"=", r"(\hat\theta - \theta_0)^2 \, n I(\hat\theta)", font_size=30),
            cmath(r"S", r"=", r"U(\theta_0)^2 / \big(n I(\theta_0)\big)", font_size=30),
            cmath(r"\Lambda", r"=", r"2\{\ell(\hat\theta) - \ell(\theta_0)\}", font_size=30),
            cmath(r"\text{all}", r"\to", r"\chi^2_1; \ \ \text{equal to first order, \ different in finite samples}", font_size=28),
        ]
        rows[2][2].set_color(LRC)
        whys = [why(r"needs only the unrestricted fit"), why(r"needs only the fit under $H_0$ (Rao 1948)"),
                why(r"needs both; \ invariant to reparametrization (Wilks 1938)"), why(r"a quadratic log likelihood makes them equal")]
        with self.voiceover(
            "<bookmark mark='a'/> As formulas: the Wald statistic is the squared distance weighted by the information at the "
            "estimate, so it needs only the unrestricted fit. <bookmark mark='b'/> Rao's score statistic, from 1948, is the "
            "squared score at the null divided by the null information, so it needs only the fit under the hypothesis, "
            "convenient when the full model is hard to fit. <bookmark mark='c'/> The likelihood ratio, Wilks's 1938 statistic, "
            "needs both fits, but it doesn't change if we reparametrize, say from p to log odds. <bookmark mark='d'/> If the log "
            "likelihood were exactly quadratic, all three would be equal; their differences measure how far from quadratic it "
            "is."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def invert(self):
        rows = [
            cmath(r"\text{interval}", r"=", r"\{p_0 : \text{the test does not reject } p_0\}", font_size=30),
            cmath(r"\text{invert Wald}", r":", r"\hat p \pm 1.96 \sqrt{\hat p(1 - \hat p)/n}", font_size=30),
            cmath(r"\text{invert score}", r":", r"(\hat p - p_0)^2 \le 1.96^2\, p_0(1 - p_0)/n: \ \text{Wilson}", font_size=30),
            cmath(r"\text{invert LR}", r":", r"\ell(p_0) \ge \ell(\hat p) - 1.92: \ \text{the profile cut}", font_size=30),
        ]
        rows[2][2].set_color(SCORE)
        whys = [why(r"Part 11: \ every test is an interval"), why(r"Part 11's Wald interval: \ coverage collapses near 0 and 1"),
                why(r"the SE at $p_0$, \ not at $\hat p$: \ Wilson (1927)"), why(r"chapter five's interval")]
        with self.voiceover(
            "<bookmark mark='a'/> Each test gives an interval, by Part 11's recipe: collect the values the test doesn't "
            "reject. <bookmark mark='b'/> Inverting the Wald test gives the Wald interval for a proportion, the one whose "
            "coverage Part 11 watched collapse near zero and one. <bookmark mark='c'/> Inverting the score test, which uses "
            "the standard error at the hypothesized value rather than at the estimate, gives Edwin Wilson's 1927 interval, "
            "the one that kept its promise. <bookmark mark='d'/> And inverting the likelihood-ratio test gives chapter five's "
            "cut at one point nine two below the peak. Three tests, three intervals, and the differences between them are the "
            "differences Part 11's Board recorded."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hauck(self):
        d = load("hauck")
        b = np.asarray(d["betas"], float)
        A = axes([0, 7], [0, 9], x_length=8.0, y_length=4.4, xlabel=r"true logistic slope $\beta$", ylabel=r"median test statistic",
                 xticks=[0, 1, 2, 3, 4, 5, 6, 7], yticks=[0, 2, 4, 6, 8], center=[-1.6, 0.3, 0])
        ax = A.ax
        wz = VGroup(polyline(ax, b, d["wald_z"], WALD, 3.5), *[Dot(ax.c2p(x, y), radius=0.06, color=WALD) for x, y in zip(b, d["wald_z"])])
        lz = VGroup(polyline(ax, b, d["lr_root"], LRC, 3.5), *[Dot(ax.c2p(x, y), radius=0.06, color=LRC) for x, y in zip(b, d["lr_root"])])
        crit = DashedLine(ax.c2p(0, 1.96), ax.c2p(7, 1.96), color=GREY_C, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(rf"logistic regression, \ $n = {d['n']}$, \ testing $\beta = 0$", font_size=22),
            label(r"gold: \ $\sqrt{\Lambda}$, \ the LR statistic, \ rising", font_size=22, color=LRC),
            label(r"blue: \ the Wald $|z|$: \ rises, \ then falls", font_size=22, color=WALD),
            label(r"the SE grows faster than the estimate", font_size=22, color=GREY_A),
            label(r"Hauck \& Donner (1977)", font_size=20, color=GREY_B),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Sometimes the differences are dramatic. Fit logistic regressions to samples of sixty, with "
            "true slopes from zero to seven, and test whether the slope is zero. <bookmark mark='b'/> The likelihood-ratio "
            "statistic, in gold, grows steadily with the true effect, as it should. <bookmark mark='c'/> The Wald statistic, in "
            "blue, grows at first, peaks around a slope of three, and then falls: the stronger the evidence, the less "
            "significant the Wald test says it is. <bookmark mark='d'/> When the fitted probabilities approach zero and one, the "
            "estimated standard error grows faster than the estimate. <bookmark mark='e'/> Walter Hauck and Allan Donner pointed "
            "this out in 1977; it's why software reports likelihood-ratio tests for logistic models."
        ) as vo:
            self.play(FadeIn(A), Create(crit))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lz), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(wz), FadeIn(rows[2]))
            for k, m_ in enumerate("de"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=22) if r.part == 22][:2]
        b = coverage_board(rows, lit_part=22, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> For intervals the Board is more forgiving. A thousand samples of fifty with a true slope of two "
            "and a half: the Wald interval covers ninety-seven percent of the time, a little conservative but within the "
            "Board's tolerance, so kept. <bookmark mark='b'/> The profile likelihood interval covers ninety-three percent, also "
            "kept. Tests near the boundary of what the data can say are where the trinity's members part company."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[1]))
        self.wait(1.0)
        self.clear_scene()
