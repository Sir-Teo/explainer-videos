from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats28.common import *  # noqa: F403

BETA, SE = 0.05, 0.1  # x_1's coefficient and its standard error with n = 100 independent predictors
KEEP = np.sqrt(2.0) * SE  # AIC keeps a predictor, roughly, when t^2 > 2


class Selective(VoiceoverScene):
    def construct(self):
        self.card()
        self.freedman_again()
        self.curse()
        self.conditional()
        self.board()
        self.split()
        self.fixes()

    def card(self):
        card = chapter_card(9, r"Inference after selection", r"Freedman's ghost", lit=(1983, 2013), part=PART)
        with self.voiceover("Chapter nine. Inference after selection, a first look."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def freedman_again(self):
        d = load("freedman")
        rows = [
            cmath(r"\text{round 1}", r":", rf"F\text{{-test }} p = {d['one']['first']['pF']:.2f}: \ \text{{nothing}}", font_size=30),
            cmath(r"\text{screen}", r":", rf"\text{{keep the }} {d['one']['first']['n_sig25']} \text{{ with }} p < 0.25", font_size=30),
            cmath(r"\text{round 2}", r":", rf"p = {d['one']['second']['pF']:.3f}, \ {d['one']['second']['n_sig05']} \text{{ significant}}", font_size=30),
            cmath(r"\text{1000 repeats}", r":", rf"{100 * d['share_sig']:.1f}\% \text{{ significant at round 2}}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"pure noise, \ 100 rows, \ 50 columns"), why(r"the selection step"),
                why(r"the same data judge their own choice"), why(r"Freedman (1983)")]
        with self.voiceover(
            "<bookmark mark='a'/> Recall the hook. A hundred rows of pure noise, fifty columns of noise, and an F-test that "
            "rightly finds nothing. <bookmark mark='b'/> Keep the columns with p-values below a quarter, <bookmark mark='c'/> "
            "refit, and the regression's p-value is point oh one three, with four coefficients significant at five percent. "
            "<bookmark mark='d'/> In ninety-five percent of a thousand repeats. Every criterion in this part selects; none of "
            "them makes the usual tests and intervals of the selected model valid."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curse(self):
        xs = np.linspace(-0.3, 0.4, 400)
        pdf = stats.norm.pdf(xs, BETA, SE)
        A = axes([-0.3, 0.4], [0, 4.4], x_length=7.6, y_length=4.2, xlabel=r"the estimate $\hat\beta_1$", ylabel=r"density",
                 xticks=[-0.2, 0, 0.05, 0.2, 0.4], yticks=[0, 2, 4], xfmt=lambda v: f"{v:g}", center=[-2.0, 0.3, 0])
        ax = A.ax
        full = curve(ax, xs, pdf, GREY_B, 3)
        hi = xs >= KEEP
        lo = xs <= -KEEP
        sh = VGroup(shade(ax, xs[hi], pdf[hi], RES, 0.55), shade(ax, xs[lo], pdf[lo], RES, 0.55))
        truth = DashedLine(ax.c2p(BETA, 0), ax.c2p(BETA, 4.2), color=TRUE, stroke_width=3)
        cuts = VGroup(*[DashedLine(ax.c2p(c, 0), ax.c2p(c, 4.2), color=RES, stroke_width=1.5) for c in (-KEEP, KEEP)])
        pk = stats.norm.sf(KEEP, BETA, SE) + stats.norm.cdf(-KEEP, BETA, SE)
        a, b = (KEEP - BETA) / SE, (-KEEP - BETA) / SE
        m_hi = BETA + SE * stats.norm.pdf(a) / stats.norm.sf(a)
        mean_abs = (stats.norm.sf(a) * m_hi + stats.norm.cdf(b) * abs(BETA - SE * stats.norm.pdf(b) / stats.norm.cdf(b))) / pk
        rows = fit_rows(VGroup(
            label(rf"truth $\beta_1 = {BETA}$; \ SE {SE}", font_size=22, color=TRUE),
            label(r"AIC keeps $x_1$ when $|t| > \sqrt 2$", font_size=22, color=RES),
            label(rf"that happens {100 * pk:.0f}\% of the time", font_size=22, color=RES),
            label(rf"kept estimates: \ $E|\hat\beta_1| = {mean_abs:.2f}$, \ {mean_abs / BETA:.1f} times the truth", font_size=22),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why, in the simplest case. A coefficient whose true value is point oh five is estimated with "
            "standard error point one. <bookmark mark='b'/> Roughly, AIC keeps a predictor when its t-statistic exceeds root "
            "two in size: the red tails. <bookmark mark='c'/> That happens about a fifth of the time. <bookmark mark='d'/> "
            "And when it does, the estimate is, on average, almost four times the truth in size. Only the lucky "
            "overestimates survive selection: the winner's curse."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(full), Create(truth))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cuts), FadeIn(sh), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def conditional(self):
        t = stats.t.ppf(0.975, 89)
        pk = stats.norm.sf(KEEP, BETA, SE) + stats.norm.cdf(-KEEP, BETA, SE)

        def cover_and_keep():
            lo, hi = BETA - t * SE, BETA + t * SE  # the CI covers beta iff the estimate lies in (lo, hi)
            p = 0.0
            for a, b in ((max(lo, KEEP), hi), (lo, min(hi, -KEEP))):
                if b > a:
                    p += stats.norm.cdf(b, BETA, SE) - stats.norm.cdf(a, BETA, SE)
            return p

        cond = cover_and_keep() / pk
        rows = [
            cmath(r"P(\text{cover})", r"=", r"0.95", font_size=32),
            cmath(r"P(\text{cover} \mid \text{kept})", r"=", r"\dfrac{P(\text{cover and kept})}{P(\text{kept})}", font_size=30),
            cmath(r"", r"=", rf"{cover_and_keep():.3f} / {pk:.3f} = {cond:.2f}", font_size=32),
            cmath(r"\text{the right question}", r":", r"\text{coverage given that we are looking}", font_size=30),
        ]
        rows[2][-1].set_color(RES)
        whys = [why(r"averaged over all data sets"), why(r"only the data sets where $x_1$ is reported"),
                why(r"normal calculation: \ the Board's 75\% next"), why(r"Benjamini \& Yekutieli (2005); \ Fithian et al.\ (2014)")]
        with self.voiceover(
            "<bookmark mark='a'/> The usual interval covers ninety-five percent of the time, averaged over all data sets. "
            "<bookmark mark='b'/> But it is only reported when the predictor is kept. Given that, its coverage is the chance of "
            "covering and being kept, over the chance of being kept. <bookmark mark='c'/> A normal calculation gives "
            "seventy-seven percent. <bookmark mark='d'/> The relevant guarantee is coverage conditional on the selection that "
            "led us to look, the idea Yoav Benjamini and Daniel Yekutieli formalized for selected parameters, and William "
            "Fithian, Dennis Sun and Jonathan Taylor for selected models."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=28) if r.part == 28]
        b = coverage_board(rows, lit_part=28, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        d = load("board")
        with self.voiceover(
            "<bookmark mark='a'/> The Board runs the full procedure: ten independent candidate predictors, a hundred "
            "observations, x one's coefficient point oh five, forward stepwise selection by AIC, and the usual ninety-five "
            "percent interval for x one whenever it is kept, two thousand times. It is kept about a fifth of the time, and "
            "then its interval covers the truth seventy-five percent of the time: broken, and in line with the calculation. "
            "<bookmark mark='b'/> Select on a random half of the data and compute the interval on the other half: ninety-five "
            "point seven percent, kept. <bookmark mark='c'/> And the full model with no selection covers ninety-five percent, "
            "as it must."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(b.body[k]))
        del d
        self.wait(1.0)
        self.clear_scene()

    def split(self):
        rows = fit_rows(VGroup(
            label(r"splitting: \ select on one half, \ infer on the other \ (Cox 1975)", font_size=24, color=HIT),
            label(r"valid, \ whatever the selection rule, \ even a person looking at plots", font_size=24, color=HIT),
            label(r"the price: \ half the data for each task, \ and a random answer", font_size=24, color=RES),
            label(r"the selection share: \ about the same, \ with half the data", font_size=24, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Splitting is the oldest fix, from David Cox in 1975. <bookmark mark='b'/> It is valid for any "
            "selection procedure at all, including an analyst staring at plots, because the inferential half never saw the "
            "choice being made. <bookmark mark='c'/> The price is power, since each task gets half the data, and an answer that "
            "depends on the random split. <bookmark mark='d'/> Here x one was kept about as often from half the data as from "
            "all of it, but its intervals are wider by a factor of about root two."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def fixes(self):
        rows = [
            cmath(r"\text{PoSI}", r":", r"\text{widen to cover every model you might choose}", font_size=30),
            cmath(r"\text{polyhedral}", r":", r"\text{condition on the selection event exactly}", font_size=30),
            cmath(r"\text{data fission}", r":", r"y = f(y) + g(y), \ \text{independent parts}", font_size=30),
            cmath(r"\text{Part 56}", r":", r"\text{all of them, \ on the Board}", font_size=30),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"Berk, Brown, Buja, Zhang \& Zhao (2013)"), why(r"Lee, Sun, Sun \& Taylor (2016)"),
                why(r"Leiner, Duan, Wasserman \& Ramdas (2023)"), why(r"selective inference in depth")]
        with self.voiceover(
            "<bookmark mark='a'/> Three modern fixes use all the data. Richard Berk and colleagues' PoSI widens intervals "
            "enough to cover simultaneously over every model that could have been chosen. <bookmark mark='b'/> Jason Lee, "
            "Dennis Sun, Yuekai Sun and Jonathan Taylor showed that for the lasso and stepwise methods the selection event is a "
            "polyhedron, and conditioned on it exactly. <bookmark mark='c'/> Data fission splits each observation, rather than "
            "the data set, into two independent noisy parts. <bookmark mark='d'/> Part 56 builds all three and puts them on the "
            "Board."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
