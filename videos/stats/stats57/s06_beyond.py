from __future__ import annotations

import numpy as np

from videos.stats.stats57.common import *  # noqa: F403


class Beyond(VoiceoverScene):
    def construct(self):
        self.card()
        self.weighted()
        self.estimated()
        self.nonexch()
        self.label_shift()
        self.chart()
        self.tv_worked()
        self.board()

    def card(self):
        card = chapter_card(5, r"Beyond exchangeability", r"When the future does not look like the past", lit=(2019, 2023), part=PART)
        with self.voiceover("Chapter five. Beyond exchangeability: when the future does not look like the past."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def weighted(self):
        rows = [
            cmath(r"\text{covariate shift}", r":", r"X_{\text{test}} \sim Q, \ \ X_{\text{cal}} \sim P, \ \ Y \mid X \text{ the same}", font_size=34),
            cmath(r"w(x)", r"=", r"dQ/dP(x): \ \text{weight the calibration scores by } w(X_i)", font_size=34),
            cmath(r"\hat q", r"=", r"\text{the } 1 - \alpha \text{ quantile of } \textstyle\sum_i \tilde w_i\delta_{S_i} + \tilde w_{n+1}\delta_{+\infty}", font_size=32),
            cmath(r"\text{valid}", r":", r"\text{exactly, \ if } w \text{ is known: \ weighted exchangeability}", font_size=34),
        ]
        rows[3][-1].set_color(COVC)
        whys = [why(r"Part 34's shift"), why(r"a likelihood ratio"), why(r"Tibshirani, \ Barber, \ Cand\`es \& Ramdas (2019)"), why(r"estimated $w$: \ approximately")]
        head = label('Weighted', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> The first step beyond exchangeability was covariate shift, seen in Part thirty-four: test "
            "features come from a different distribution, but the outcome's law given the features is unchanged. <bookmark "
            "mark='b'/> Weight each calibration score by the likelihood ratio of the two feature distributions. <bookmark "
            "mark='c'/> Take the one minus alpha quantile of the weighted scores, with the test point's weight placed at "
            "infinity. <bookmark mark='d'/> Ryan Tibshirani, Barber, Candès and Ramdas showed this is exactly valid when the "
            "weights are known, because the data are then weighted exchangeable."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def estimated(self):
        rows = [
            cmath(r"\hat w \text{ estimated}", r":", r"\text{a classifier of test against calibration features}", font_size=34),
            cmath(r"\text{coverage}", r"\ge", r"1 - \alpha - \tfrac12 E_P|\bar w-w|\quad (E_P\bar w=1)", font_size=34),
            cmath(r"\text{counterfactuals}", r":", r"\text{weighted conformal for ITEs}", font_size=36),
            cmath(r"\text{doubly robust}", r":", r"\text{asymptotic validity under the stated nuisance conditions}", font_size=34),
        ]
        rows[2][-1].set_color(WEIGHTC)
        rows[3][-1].set_color(COVC)
        whys = [why(r"the probabilistic-classification trick"), why(r"Lei \& Cand\`es (2021)"), why(r"treated outcomes as a shift; \ Part 62"), why(r"Yang, \ Kuchibhotla \& Tchetgen Tchetgen")]
        head = label('Estimated', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> In practice the weights are estimated, usually by a classifier trained to tell test features from calibration features. <bookmark mark='b'/> For independently estimated, nonnegative weights normalized to integrate to one, the coverage loss is bounded by half the reference-law expectation of their absolute density-ratio error. Raw classifier odds need normalization and the correct class-prior factor. <bookmark mark='c'/> Lihua Lei and Candès used exactly this for causal inference: the treated group's outcomes are a covariate-shifted version of the population's, under unconfoundedness and overlap, weighted conformal can predict missing potential outcomes. Intervals for their difference need a further construction; the unobserved joint potential-outcome law is not identified automatically. <bookmark mark='d'/> Double robustness is an asymptotic guarantee under specified nuisance rates and regularity conditions, not automatic finite-sample exactness from a correct mean model alone."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def nonexch(self):
        rows = [
            cmath(r"\text{fixed weights } w_1, \dots, w_n", r":", r"\text{fixed in advance, \ e.g. } w_i = \rho^{n+1-i}", font_size=36),
            cmath(r"\text{coverage}", r"\ge", r"1 - \alpha - \textstyle\sum_i \tilde w_i\, d_{TV}\big(Z, Z^{(i)}\big)", font_size=34),
            cmath(r"Z^{(i)}", r":", r"\text{the data with point } i \text{ and the test point swapped}", font_size=34),
            cmath(r"\text{exchangeable}", r"\Rightarrow", r"d_{TV} = 0: \ \text{the old guarantee; \ a drift} \Rightarrow \text{a small loss}", font_size=32),
        ]
        rows[1][-1].set_color(COVC)
        whys = [why(r"Barber, \ Cand\`es, \ Ramdas \& Tibshirani (2023)"), why(r"no assumption on the data"), why(r"how far from exchangeable"), why(r"graceful degradation")]
        head = label('A coverage bound under distribution shift', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> For data that are not exchangeable at all, such as a time series that drifts, Barber, Candès, Ramdas and Tibshirani fix weights in advance, for example geometrically decaying ones that count recent points more. <bookmark mark='b'/> With no assumption on the data, the coverage is at least one minus alpha, minus a weighted sum of total-variation distances. <bookmark mark='c'/> Each distance measures how much the data's law changes when point i and the test point are swapped. <bookmark mark='d'/> For exchangeable data every distance is zero and the old guarantee returns; under drift, recent weighting helps when the recent points have smaller swap distances. The bound can be vacuous for arbitrary drift."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def label_shift(self):
        rows = [
            cmath(r"\text{label shift}", r":", r"P(Y) \text{ changes, \ } P(X \mid Y) \text{ fixed: \ weights in } y", font_size=34),
            cmath(r"\text{time series}", r":", r"\text{blocks, \ mixing coefficients, \ decaying weights}", font_size=34),
            cmath(r"\text{spatial data}", r":", r"\text{weights by distance}", font_size=36),
            cmath(r"\text{the common idea}", r":", r"\text{say which past points resemble the future, \ and weight them}", font_size=32),
        ]
        rows[3][-1].set_color(TESTPT)
        whys = [why(r"the reverse shift"), why(r"Chernozhukov et al.; \ Xu \& Xie"), why(r"Mao, \ Martin \& Reich"), why(r"small loss still requires small swap distances")]
        head = label('Label shift', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Other departures have their own weights. Under label shift the outcome's distribution changes while the features given the outcome do not, and the weights depend on y. <bookmark mark='b'/> For time series, methods use blocks of data, mixing conditions, or decaying weights. <bookmark mark='c'/> For spatial data, weights by distance to the prediction site. <bookmark mark='d'/> The common idea: say which past points resemble the future, and weight them. In the nonexchangeable framework that is a modelling choice that affects efficiency and the size of the coverage loss, not a promise of near-nominal coverage without controlling those distances."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("drift")
        t = np.asarray(d["t"])
        A = axes([t[0], t[-1]], [0.5, 1.02], x_length=7.4, y_length=4.4, xlabel=r"time \ (noise SD 1, \ then 2.5 from $t = 1{,}000$)", ylabel=r"coverage, \ rolling 100",
                 xticks=[500, 1000, 1500, 2000], yticks=[0.5, 0.75, 0.9, 1.0], center=[-2.5, 0.2, 0])
        ax = A.ax
        cs = polyline(ax, t, d["split_roll"], MISSC, 4)
        cn = polyline(ax, t, d["nex_roll"], COVC, 4)
        nom = DashedLine(ax.c2p(t[0], 0.9), ax.c2p(t[-1], 0.9), color=GREY_B, stroke_width=2)
        cp = DashedLine(ax.c2p(1000, 0.5), ax.c2p(1000, 1.02), color=WEIGHTC, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"noise jumps at $t = 1{{,}}000$; \ last {d['window']} calibrate", font_size=22),
            label(rf"red: \ equal weights: \ {100 * d['split_after']:.0f}\% in the 300 steps after", font_size=22, color=MISSC),
            label(rf"green: \ weights $\rho^{{\text{{age}}}}$, \ $\rho = {d['rho']}$: \ {100 * d['nex_after']:.0f}\%", font_size=22, color=COVC),
            label(rf"overall: \ {100 * d['split_all']:.1f}\% \ vs \ {100 * d['nex_all']:.1f}\%", font_size=22, color=GREY_A),
            label(r"recent points carry the information about now", font_size=22, color=TESTPT),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A series whose noise jumps from one to two and a half at time one thousand, with the last "
            f"three hundred points as the calibration set at each step. <bookmark mark='b'/> With equal weights, coverage in the "
            f"three hundred steps after the jump falls to {100 * d['split_after']:.0f} percent, because most of the calibration "
            f"window still remembers the quiet regime. <bookmark mark='c'/> With weights decaying by a factor of point nine nine "
            f"per step, it recovers to {100 * d['nex_after']:.0f} percent. <bookmark mark='d'/> Over the whole series, "
            f"{100 * d['split_all']:.1f} against {100 * d['nex_all']:.1f} percent. <bookmark mark='e'/> Recent points carry the "
            f"information about now."
        ) as vo:
            self.play(FadeIn(A), FadeIn(nom), FadeIn(cp), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(cn), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def tv_worked(self):
        rows = [
            cmath(r"50 \text{ steps after the jump}", r":", r"250 \text{ of the 300 past points are from before}", font_size=34),
            cmath(r"\text{swap one of them with now}", r":", r"d_{\mathrm{TV}} \approx 0.52", font_size=36),
            cmath(r"\text{equal weights}", r":", r"\text{loss} \le 0.83 \times 0.52 = 0.43", font_size=36),
            cmath(r"\rho = 0.99", r":", r"\text{loss} \le 0.58 \times 0.52 = 0.30", font_size=36),
        ]
        rows[2][-1].set_color(MISSC)
        rows[3][-1].set_color(COVC)
        whys = [why(r"most of the window is stale"), why(r"SD 1 vs 2.5, \ as a pair"), why(r"coverage $\ge 47\%$"), why(r"coverage $\ge 60\%$")]
        head = label('Tv worked', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> The bound in numbers. Fifty steps after the jump, two hundred and fifty of the three "
            "hundred past points come from before it. <bookmark mark='b'/> Swapping one of them with the current point "
            "changes the joint distribution by a total variation of about point five two. <bookmark mark='c'/> With "
            "equal weights the stale points carry eighty-three percent of the weight, so the guaranteed loss is up to "
            "forty-three points: coverage at least forty-seven percent. <bookmark mark='d'/> With weights decaying by "
            "point nine nine per step they carry fifty-eight percent, the loss is at most thirty points, and coverage "
            "is at least sixty percent. Loose, but honest, and the chart shows the truth is better."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("changepoint", "nonexchangeable"),
                   f"<bookmark mark='a'/> On the Board, average over forty independent simulated paths, using the three hundred steps after the change in each: split conformal with equal weights covers {100 * br[4]['achieved']:.0f} percent. <bookmark mark='b'/> The weighted, nonexchangeable version covers {100 * br[5]['achieved']:.0f} percent.", [("a", [0]), ("b", [1])])
