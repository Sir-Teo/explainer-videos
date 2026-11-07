from __future__ import annotations

import numpy as np

from videos.stats.stats47.common import *  # noqa: F403


class Bootstrap(VoiceoverScene):
    def construct(self):
        self.card()
        self.consistency()
        self.edgeworth()
        self.pivot()
        self.table()
        self.chart()
        self.board()

    def card(self):
        card = chapter_card(11, r"The bootstrap, \ rigorously", r"Why resampling beats the normal approximation", lit=(1992,), part=PART)
        with self.voiceover("Chapter eleven. The bootstrap, rigorously: why resampling can beat the normal approximation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def consistency(self):
        rows = [
            cmath(r"\sqrt n(\hat F_n^* - \hat F_n)", r"\Rightarrow", r"\mathbb G_F \ \ \text{given the data, \ a.s.}", font_size=34),
            cmath(r"T \text{ Hadamard differentiable}", r"\Rightarrow", r"\sqrt n(T(\hat F^*) - T(\hat F)) \text{ has the same limit as } \sqrt n(T(\hat F) - T(F))", font_size=26),
            cmath(r"\text{so}", r":", r"\text{the bootstrap law is consistent}", font_size=34),
            cmath(r"\text{fails}", r":", r"\text{non-smooth } T \text{ (the maximum, \ chapter 13), \ heavy tails, \ dependence}", font_size=28),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(HODC)
        whys = [why(r"the bootstrap empirical process"), why(r"the functional delta method, \ twice"), why(r"first order"), why(r"where it breaks")]
        with self.voiceover(
            "<bookmark mark='a'/> Why does the bootstrap work at all? Conditionally on the data, the resampled "
            "empirical distribution fluctuates around the empirical distribution exactly as the empirical "
            "distribution fluctuates around the truth: the same Brownian bridge in the limit. <bookmark mark='b'/> "
            "For a continuous linear Hadamard derivative tangential to the bootstrap empirical-process limit space, "
            "chapter four's delta method applies in both worlds, and the bootstrap distribution of the statistic has "
            "the same limit as its true sampling distribution. <bookmark mark='c'/> That is consistency, proved by "
            "Evarist Giné and Joel Zinn and set out in van der Vaart and Wellner's book. <bookmark mark='d'/> That "
            "sufficient argument does not cover every functional. The endpoint maximum fails at its n rate; "
            "infinite-variance means and dependence destroyed by ordinary iid resampling need different methods. Some"
            " nonsmooth-looking statistics, such as regular quantiles, still have valid bootstrap limits."
        ) as vo:
            heading=label('A regular bootstrap delta method matches the process limit',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def edgeworth(self):
        rows = [
            cmath(r"P\big(\sqrt n(\bar x-\mu)/s\le z\big)", r"=", r"\Phi(z)+\tfrac{\gamma}{6\sqrt n}(2z^2+1)\phi(z)+O(n^{-1})", font_size=30),
            cmath(r"\text{bootstrap}", r":", r"\text{the same expansion with } \hat\gamma: \ \hat\gamma - \gamma = O_P(n^{-1/2})", font_size=30),
            cmath(r"\Rightarrow", r"\;", r"\text{the bootstrap error is } O_P(n^{-1}), \ \text{the normal's } O(n^{-1/2})", font_size=30),
            cmath(r"\text{needs}", r":", r"\text{asymptotic pivot, sufficient moments, smoothness and Cramér conditions}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"Edgeworth, \ Part 43"), why(r"it estimates the skewness term"), why(r"second-order accuracy"), why(r"Hall (1992)")]
        with self.voiceover(
            "<bookmark mark='a'/> The deeper reason is the Edgeworth expansion of Part forty-three. For the "
            "studentized mean under suitable moment, smoothness, and Cramér nonlattice conditions, its CDF has the "
            "normal term plus skewness times two z squared plus one, times the normal density, divided by six root n,"
            " plus smaller terms. <bookmark mark='b'/> The bootstrap distribution has the same expansion with the "
            "sample skewness in place of the true one, and that estimate is itself off by order one over root n. "
            "<bookmark mark='c'/> So the bootstrap captures the first correction automatically, and its error is of "
            "order one over n, while the normal approximation's is one over root n. <bookmark mark='d'/> An "
            "asymptotic pivot is one ingredient, not the whole theorem. Required moments and Edgeworth regularity "
            "still matter. A finite resample count adds Monte Carlo error, so keeping B equal to 999 fixed does not "
            "by itself establish an asymptotic one-over-n rate: this is an illustration of Hall's analysis, not a "
            "full proof."
        ) as vo:
            heading=label('Studentization can let the bootstrap estimate a skewness correction',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pivot(self):
        rows = fit_rows(VGroup(
            label(r"one-sided coverage errors, \ the theory:", font_size=28, color=GREY_A),
            label(r"normal-theory and percentile intervals: \ $O(n^{-1/2})$", font_size=26, color=HODC),
            label(r"bootstrap-$t$ \ (resample the studentized statistic): \ $O(n^{-1})$", font_size=26, color=GOODC),
            label(r"BCa \ (bias correction $z_0$, \ acceleration $a$): \ $O(n^{-1})$", font_size=26, color=GOODC),
            label(r"balanced two-sided errors may cancel; \ tail calibration and finite-$B$ error still matter", font_size=26, color=S.ACCENT),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The theory, for the coverage error of a one-sided interval: <bookmark mark='b'/> "
            "the normal-theory interval and the percentile bootstrap are wrong by order one over root n; <bookmark "
            "mark='c'/> the bootstrap-t, which resamples the studentized statistic, by order one over n; <bookmark "
            "mark='d'/> and so is Efron's BCa interval, which corrects the percentile interval for bias and skewness."
            " <bookmark mark='e'/> In suitable balanced two-sided constructions, leading tail errors can cancel in "
            "total coverage. This is not automatic for every interval, and good total coverage need not mean that "
            "each tail is calibrated."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def table(self):
        d = load("bootstrap")
        names = [("normal", r"Student $t$"), ("percentile", r"percentile"), ("basic", r"basic"), ("bca", r"BCa"), ("t", r"bootstrap-$t$")]
        rows = [[r"$n$"] + [nm for _, nm in names]]
        for r in d["rows"]:
            rows.append([str(r["n"])] + [f"{100 * r['cov'][k]:.1f}\\%" for k, _ in names])
        tab = table_rows(rows, font_size=28, col_buff=0.8, row_buff=0.3, colors=[GREY_A] + [None] * len(d["rows"])).move_to([0, 0.8, 0])
        note_ = fit_rows(VGroup(
            label(r"two-sided 90\% intervals for the mean of Exp(1) data; \ 1,500 data sets per row, \ 999 resamples each", font_size=24, color=GREY_A),
            label(r"only the bootstrap-$t$ is close to 90\% at small $n$; \ all approach it as $n$ grows", font_size=24, color=S.ACCENT),
        ), 12.4, 0.25, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Simulated, for the mean of exponential data, the textbook skewed case: two-sided ninety "
            "percent intervals at ten, twenty, forty and eighty observations. <bookmark mark='b'/> The Student t interval "
            "covers eighty-seven percent at ten; the percentile and basic bootstraps do worse, eighty-three and eighty-one; "
            "BCa eighty-three. <bookmark mark='c'/> The bootstrap-t is at ninety-one percent already, and stays close to "
            "ninety. <bookmark mark='d'/> All of them approach the nominal level as n grows, the percentile methods slowly."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(note_[0]), FadeIn(exact_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
            vo.wait_until("d")
            self.play(FadeIn(tab[4]), FadeIn(note_[1]))
        self.clear_scene()

    def chart(self):
        d = load("bootstrap")
        ns = np.array([r["n"] for r in d["rows"]], float)
        ln = np.log10(ns)
        A = axes([0.9, 2.0], [0, 0.06], x_length=7.4, y_length=4.4, xlabel=r"$n$", ylabel=r"$P(\mu < \text{lower limit})$, \ nominal 0.05",
                 xticks=[1, np.log10(20), np.log10(40), np.log10(80)], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0, 0.025, 0.05], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"normal": MLEC, "percentile": HODC, "bca": S.PRIOR, "t": GOODC}
        lines = {k: VGroup(polyline(ax, ln, [r["low"][k] for r in d["rows"]], c, 4), *[Dot(ax.c2p(a, r["low"][k]), radius=0.08, color=c) for a, r in zip(ln, d["rows"])])
                 for k, c in cols.items()}
        nom = DashedLine(ax.c2p(0.9, 0.05), ax.c2p(2.0, 0.05), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"the lower tail: \ $\mu$ falls below the interval", font_size=22),
            VGroup(label(r"blue: \ Student $t$;", font_size=22, color=MLEC), label(r"red: \ percentile", font_size=22, color=HODC)).arrange(RIGHT, buff=0.2),
            VGroup(label(r"purple: \ BCa;", font_size=22, color=S.PRIOR), label(r"green: \ bootstrap-$t$", font_size=22, color=GOODC)).arrange(RIGHT, buff=0.2),
            label(r"Student, \ percentile: \ too rarely below", font_size=22, color=S.ACCENT),
            label(r"skewness puts the error in one tail", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Look at one tail at a time. This is the chance that the true mean falls below the "
            "lower limit, which should be five percent. <bookmark mark='b'/> The Student and percentile intervals "
            "miss on this side only one to four percent of the time, <bookmark mark='c'/> while BCa is close to five "
            "throughout and the bootstrap-t climbs toward it. <bookmark mark='d'/> The symmetric intervals are placed"
            " wrongly for skewed data: too rarely wrong below, and so too often wrong above. <bookmark mark='e'/> The"
            " tail-specific errors help diagnose what total coverage conceals. Four finite sample sizes and finite "
            "simulation counts cannot establish an asymptotic order."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(exact_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lines["normal"]), Create(lines["percentile"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lines["bca"]), Create(lines["t"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def board(self):
        rows = board_rows("for a mean")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Coverage Board, at twenty observations from the exponential: the Student t "
                   "interval covers eighty-seven percent, broken; the percentile bootstrap eighty-five, broken. <bookmark "
                   "mark='b'/> The bootstrap-t covers eighty-nine, kept; and BCa, at this small sample size, eighty-four: "
                   "broken. Second-order accuracy is an asymptotic promise, and BCa's acceleration estimate is noisy at n "
                   "equal to twenty.",
                   [("a", [0, 1]), ("b", [2, 3])])
