from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats31.common import *  # noqa: F403


class HighDim(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.sizes()
        self.board()
        self.bs()
        self.shrinkage()
        self.power()
        self.lesson()

    def card(self):
        card = chapter_card(10, r"A high-dimensional warning", r"When $p$ grows with $n$", lit=(1967, 1996), part=PART)
        with self.voiceover("Chapter ten. A high-dimensional warning."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"T^2", r"\xrightarrow{d}", r"\chi^2_p \ \ \text{as } n \to \infty, \ p \text{ fixed}", font_size=30),
            cmath(r"T^2 \cdot \tfrac{n_1 + n_2 - p - 1}{p(n_1 + n_2 - 2)}", r"\sim", r"F_{p, \, n_1 + n_2 - p - 1} \ \text{exactly}", font_size=28),
            cmath(r"p / n", r"\to", r"\gamma > 0: \ \text{the } \chi^2 \text{ calibration fails}", font_size=30),
            cmath(r"p \ge n_1 + n_2 - 1", r":", r"S \text{ is singular: \ } T^2 \text{ does not exist}", font_size=30),
        ]
        rows[2][-1].set_color(RES)
        whys = [why(r"the textbook large-sample rule"), why(r"normal data, \ any $n > p$"), why(r"chapter two's eigenvalues"),
                why(r"too few observations")]
        with self.voiceover(
            "<bookmark mark='a'/> The two-sample T squared has two calibrations. For fixed p and growing n it is "
            "approximately chi-squared with p degrees of freedom. <bookmark mark='b'/> For normal data and any sample size "
            "larger than p, a rescaled version is exactly F. <bookmark mark='c'/> These agree when p is small. When p grows "
            "in proportion to n, the chi-squared approximation fails: the small eigenvalues of S from chapter two blow up "
            "S inverse and inflate T squared. <bookmark mark='d'/> And once p reaches the total sample size minus one, S "
            "is singular and T squared does not exist at all."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sizes(self):
        d = load("board")
        res = d["res"]
        ps = [2, 10, 25, 40]
        A = axes([0, 44], [0, 0.8], x_length=7.2, y_length=4.6, xlabel=r"variables $p$ \ (two samples of 50)",
                 ylabel=r"rejection rate when $H_0$ is true", xticks=[2, 10, 25, 40], yticks=[0, 0.05, 0.4, 0.8],
                 yfmt=lambda v: f"{v:g}", center=[-2.0, 0.2, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(0, 0.05), ax.c2p(44, 0.05), color=GREY_B, stroke_width=2)
        lines = {}
        cols = {"chi2": RES, "F": HIT, "bs": MAPC}
        for key in cols:
            ys = [res[str(p)][key] for p in ps]
            lines[key] = VGroup(polyline(ax, ps, ys, cols[key], 3), *[Dot(ax.c2p(p, v), radius=0.07, color=cols[key]) for p, v in zip(ps, ys)])
        rows = fit_rows(VGroup(
            label(rf"{d['reps']:,} null data sets at each $p$", font_size=22),
            label(rf"$\chi^2_p$ calibration: \ {100 * res['2']['chi2']:.1f}\% at $p = 2$, \ {100 * res['40']['chi2']:.0f}\% at $p = 40$", font_size=22, color=RES),
            label(r"exact $F$: \ 5\% throughout", font_size=22, color=HIT),
            label(r"Bai--Saranadasa: \ about 6\%", font_size=22, color=MAPC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A simulation. Two samples of fifty from the same normal distribution, so every rejection is "
            "false, two thousand times at each number of variables. <bookmark mark='b'/> With the chi-squared calibration, "
            "the false-rejection rate is five percent at two variables, ten at ten, a third at twenty-five, and seventy-two "
            "percent at forty. <bookmark mark='c'/> The exact F calibration holds five percent all the way, as it must for "
            "normal data. <bookmark mark='d'/> And a test that does not invert S at all, Bai and Saranadasa's, stays near six "
            "percent."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(nom))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lines["chi2"]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(lines["F"]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(lines["bs"]), FadeIn(rows[3]))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=31) if r.part == 31]
        b = coverage_board(rows, lit_part=31, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> On the Board, as sizes. The chi-squared calibration is kept at two variables, "
            "<bookmark mark='b'/> and broken at twenty-five and forty. <bookmark mark='c'/> The exact F is kept at forty, "
            "and so is Bai–Saranadasa, a little above five percent but within the Board's tolerance. The method that was "
            "fine for decades of small-p textbook problems fails without warning when the variables multiply."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[1]), FadeIn(b.body[2]))
            vo.wait_until("c")
            self.play(FadeIn(b.body[3]), FadeIn(b.body[4]))
        self.wait(1.0)
        self.clear_scene()

    def bs(self):
        rows = [
            cmath(r"M", r"=", r"\|\bar x_1 - \bar x_2\|^2 - \big(\tfrac1{n_1} + \tfrac1{n_2}\big) \mathrm{tr}\, S", font_size=30),
            cmath(r"E M", r"=", r"\|\mu_1 - \mu_2\|^2", font_size=32),
            cmath(r"M / \widehat{\mathrm{sd}}(M)", r"\xrightarrow{d}", r"N(0, 1) \ \ \text{as } p, n \to \infty", font_size=30),
            cmath(r"\text{works for}", r":", r"p > n \ \text{too}", font_size=32),
        ]
        rows[0][-1].set_color(MAPC)
        whys = [why(r"drop $S^{-1}$"), why(r"unbiased for the squared distance"), why(r"Bai \& Saranadasa (1996)"),
                why(r"no inverse needed")]
        with self.voiceover(
            "<bookmark mark='a'/> Zhidong Bai and Hewa Saranadasa's idea of 1996 is to stop inverting S. Use the plain "
            "squared distance between the mean vectors, minus its expected value under the null. <bookmark mark='b'/> That "
            "is unbiased for the squared distance between the true means. <bookmark mark='c'/> Standardized by an estimate "
            "of its standard deviation, it is asymptotically normal as p and n grow together. <bookmark mark='d'/> And it "
            "exists even when there are more variables than observations."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def power(self):
        d = load("board")
        pw = d["power"]
        hdr = [r"\textbf{variables $p$}", r"\textbf{exact $T^2$ ($F$)}", r"\textbf{Bai--Saranadasa}"]
        body = [[str(p), f"{pw[str(p)]['F']:.2f}" if pw[str(p)]["F"] is not None else "--", f"{pw[str(p)]['bs']:.2f}"]
                for p in (10, 25, 40, 90)]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.2, row_buff=0.3, colors=[GREY_A] + [None] * 4)
        for r in tb[1:]:
            r[1].set_color(HIT)
            r[2].set_color(MAPC)
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"power when every coordinate's mean shifts by 0.15 SD; \ 500 data sets each", font_size=22),
            label(r"more variables, \ more signal, \ but $T^2$'s power peaks and then collapses", font_size=22, color=HIT),
            label(r"at $p = 90$, \ $T^2$ has 8 residual degrees of freedom: \ 0.16 against 0.95", font_size=22, color=RES),
        ), 12.0, 0.22, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Validity is not enough; what about power? Shift every coordinate's mean by point one five "
            "standard deviations, so more variables means more total signal. <bookmark mark='b'/> Bai–Saranadasa's power "
            "climbs steadily, from a third to ninety-five percent. The exact T squared's climbs at first, then collapses. "
            "<bookmark mark='c'/> At ninety variables it has only eight degrees of freedom left for estimating a "
            "ninety-by-ninety inverse covariance, and its power is sixteen percent against ninety-five. Estimating S inverse "
            "costs more than it gains."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.3), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"classical multivariate methods invert $S$, \ and $S$ is unreliable when $p/n$ is not small", font_size=24),
            label(r"sample eigenvalues spread, \ canonical correlations approach 1, \ LDA overfits", font_size=24, color=RES),
            label(r"the cures: \ do without $S^{-1}$, \ shrink it, \ or assume sparsity", font_size=24, color=MAPC),
            label(r"sparsity: \ Part 32; \ the full theory: \ Parts 51, \ 52 and 59", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lesson of this chapter. The classical multivariate toolkit is built on S inverse, and S "
            "is unreliable whenever the ratio of variables to observations is not small. <bookmark mark='b'/> Sample "
            "eigenvalues spread out, canonical correlations approach one by chance, and discriminant rules overfit. "
            "<bookmark mark='c'/> There are three cures: do without the inverse, as Bai and Saranadasa did; shrink the "
            "covariance towards something simpler; or assume that most of the structure is zero, as the graphical lasso "
            "did. <bookmark mark='d'/> That last idea, sparsity, is the next part. The full theory of high dimensions comes "
            "in Parts 51, 52 and 59."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def shrinkage(self):
        rows = [
            cmath(r"\hat\Sigma_\alpha", r"=", r"(1 - \alpha) S + \alpha \tfrac{\mathrm{tr} S}{p} I", font_size=32),
            cmath(r"\text{eigenvalues}", r":", r"\text{pulled towards their mean}", font_size=30),
            cmath(r"\alpha^*", r":", r"\text{estimated from the data, \ minimizing } E\|\hat\Sigma_\alpha - \Sigma\|_F^2", font_size=28),
            cmath(r"\hat\Sigma_\alpha", r":", r"\text{always invertible, \ well-conditioned}", font_size=30),
        ]
        rows[0][-1].set_color(MAPC)
        whys = [why(r"shrink towards a sphere"), why(r"undoes chapter two's fanning"), why(r"Ledoit \& Wolf (2004)"), why(r"Part 25's idea, for matrices")]
        with self.voiceover(
            "<bookmark mark='a'/> The second cure is to shrink. Mix the sample covariance with a multiple of the "
            "identity. <bookmark mark='b'/> That pulls the sample eigenvalues back towards their average, undoing the "
            "fanning-out of chapter two. <bookmark mark='c'/> Olivier Ledoit and Michael Wolf showed in 2004 how to "
            "estimate the best mixing weight from the data themselves. <bookmark mark='d'/> The result is always "
            "invertible and well-conditioned, so T squared, LDA and the rest can use it even when p exceeds n. It is "
            "Part 25's idea of borrowing strength, applied to a matrix."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
