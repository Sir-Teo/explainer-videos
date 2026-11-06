from __future__ import annotations

import numpy as np

from videos.stats.stats46.common import *  # noqa: F403


class Bounded(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.ordering()
        self.table()
        self.coverage()
        self.lessons()
        self.board()

    def card(self):
        card = chapter_card(8, r"Bounded parameters: \ Feldman--Cousins", r"A signal that cannot be negative", lit=(1998,), part=PART)
        with self.voiceover("Chapter eight. Bounded parameters, and Feldman and Cousins's unified intervals: a signal that cannot be negative."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        d = load("fc")
        rows = [
            cmath(r"n \sim \text{Poisson}(\mu + b)", r",", r"\ \mu \ge 0 \ \text{the signal}, \ b = 3 \ \text{known background}", font_size=30),
            cmath(r"n = 0", r":", rf"\text{{classical 90\% upper limit}} \ -\log 0.1 - b = {d['classical_upper_n0']:.2f}", font_size=30),
            cmath(r"\text{an empty interval}", r":", r"\text{valid coverage, \ absurd report}", font_size=32),
            cmath(r"\text{flip-flopping}", r":", r"\text{upper limit if } n \text{ is small, \ central interval if large}", font_size=30),
        ]
        rows[2][-1].set_color(REJC)
        rows[3][-1].set_color(REJC)
        whys = [why(r"a particle search"), why(r"below the physical boundary"), why(r"the Neyman construction allows it"), why(r"decided after seeing $n$")]
        with self.voiceover(
            f"<bookmark mark='a'/> A problem from particle physics. A detector counts events: a Poisson number with mean "
            f"equal to an unknown signal mu, which cannot be negative, plus a known background of three. <bookmark "
            f"mark='b'/> Suppose it counts nothing. The classical ninety percent upper limit, from the one-sided Poisson "
            f"test, is minus the log of point one minus three: {say(d['classical_upper_n0'], 2)}, a negative signal. "
            f"<bookmark mark='c'/> The interval is empty. The Neyman construction allows this and still covers ninety "
            f"percent of the time on average, but no physicist will publish it. <bookmark mark='d'/> The common practice "
            f"was to flip-flop: quote an upper limit if the count looks small, a two-sided interval if it looks large, "
            f"deciding after seeing the data."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ordering(self):
        rows = [
            cmath(r"\text{for each } \mu", r":", r"\text{rank the counts } n \text{ by } R(n) = \frac{P(n \mid \mu)}{P(n \mid \hat\mu_n)}, \ \hat\mu_n = \max(0, n - b)", font_size=28),
            cmath(r"A(\mu)", r"=", r"\text{the highest-ranked } n \text{ until } P(A(\mu) \mid \mu) \ge 90\%", font_size=32),
            cmath(r"C(n)", r"=", r"\{\mu : n \in A(\mu)\}", font_size=36),
            cmath(r"\text{result}", r":", r"\text{never empty; \ one-sided or two-sided, \ automatically}", font_size=32),
        ]
        rows[0][-1].set_color(UMPC)
        rows[3][-1].set_color(UMPC)
        whys = [why(r"a likelihood ratio, \ restricted MLE"), why(r"the acceptance region"), why(r"chapter 6's inversion"), why(r"Feldman \& Cousins (1998)")]
        with self.voiceover(
            "<bookmark mark='a'/> Gary Feldman and Robert Cousins's fix of 1998 is the Neyman construction with a better "
            "ordering. For each mu, rank the possible counts by a likelihood ratio: the probability of n under mu, over its "
            "probability under the best physically allowed mu, which is n minus the background, or zero. <bookmark "
            "mark='b'/> Fill the acceptance region with the highest-ranked counts until it holds ninety percent. <bookmark "
            "mark='c'/> Invert, as in chapter six. <bookmark mark='d'/> The intervals are never empty, and they move from "
            "upper limits to two-sided intervals by themselves, as the count grows, with the coverage guaranteed. Their "
            "ordering is the likelihood ratio test's acceptance region, so this is chapter five's test, inverted."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("fc")
        rows = [[r"$n$"] + [str(k) for k in range(11)],
                [r"FC"] + [f"{lo:.2f}--{hi:.2f}" for lo, hi in zip(d["fc_lo"], d["fc_hi"])],
                [r"flip-flop"] + [("empty" if hi <= 0 else f"{lo:.2f}--{hi:.2f}") for lo, hi in zip(d["ff_lo"], d["ff_hi"])]]
        tab = table_rows(rows, font_size=20, col_buff=0.28, row_buff=0.35, colors=[GREY_A, UMPC, REJC]).move_to([0, 0.9, 0])
        if tab.width > 13.2:
            tab.width = 13.2
        check = label(r"check: \ with $b = 0$, \ $n = 0, \ldots, 3$ give $[0, 2.44]$, \ $[0.11, 4.36]$, \ $[0.53, 5.91]$, \ $[1.10, 7.42]$: \ Feldman \& Cousins's Table II", font_size=22, color=GREY_A).move_to([0, -1.5, 0])
        if check.width > 12.6:
            check.width = 12.6
        note_ = label(r"FC: \ upper limits up to $n = 5$, \ two-sided from $n = 6$, \ chosen by the ordering, \ not by us", font_size=24, color=S.ACCENT).move_to([0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The intervals for zero to ten counts, with a background of three. <bookmark mark='b'/> "
            "Feldman and Cousins's are upper limits for up to five counts, and two-sided from six on. Zero counts give a "
            "signal between zero and point nine five. <bookmark mark='c'/> The flip-flopping intervals are empty at zero and "
            "switch from limits to intervals at nine, the background plus three standard deviations. <bookmark mark='d'/> "
            "The construction in statkit reproduces the published table for zero background exactly."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(note_))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(check))
        self.clear_scene()

    def coverage(self):
        d = load("fc")
        mus = np.asarray(d["mus"])
        A = axes([0, 8], [0.75, 1.0], x_length=7.4, y_length=4.4, xlabel=r"the true signal $\mu$", ylabel=r"exact coverage",
                 xticks=[0, 2, 4, 6, 8], yticks=[0.8, 0.85, 0.9, 0.95, 1.0], center=[-2.5, 0.2, 0])
        ax = A.ax
        cf = polyline(ax, mus, d["cov_fc"], UMPC, 3)
        cp = polyline(ax, mus, d["cov_ff"], REJC, 3)
        nom = DashedLine(ax.c2p(0, 0.9), ax.c2p(8, 0.9), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"green: \ Feldman--Cousins: \ never below 90\%", font_size=22, color=UMPC),
            label(rf"red: \ flip-flopping: \ as low as {100 * d['ff_min']:.1f}\% \ (at $\mu = {d['ff_argmin']:.2f}$)", font_size=22, color=REJC),
            label(r"deciding the kind of interval after seeing $n$ \ breaks the guarantee", font_size=22, color=S.ACCENT),
            label(r"the sawtooth: \ Poisson discreteness", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The exact coverage of both, at every signal strength. Feldman and Cousins's intervals "
            f"never cover less than ninety percent. <bookmark mark='b'/> The flip-flopping intervals fall to "
            f"{100 * d['ff_min']:.1f} percent, near a signal of {say(d['ff_argmin'], 1)}. <bookmark mark='c'/> Each piece "
            f"of the flip-flop is a valid interval on its own; choosing between them after seeing the count is what breaks "
            f"the guarantee, exactly like Part thirty-three's p-hacking. <bookmark mark='d'/> The teeth come from the "
            f"discreteness of the counts."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(exact_tag(r"exact: \ Poisson sums")))
            vo.wait_until("a")
            self.play(Create(cf), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cp), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"the ordering is a free choice in Neyman's construction: \ it decides the intervals' shape", font_size=26),
            label(r"likelihood-ratio ordering: \ unified, \ never empty, \ correct coverage", font_size=26, color=UMPC),
            label(r"remaining oddities: \ with more background, \ a lucky zero gives a \emph{tighter} limit", font_size=26, color=REJC),
            label(r"the alternatives physicists use: \ CLs, \ Bayesian limits with a flat prior on $\mu \ge 0$", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lesson is that Neyman's construction leaves a choice, the ordering of the sample space "
            "within each acceptance region, and that choice decides what the intervals look like. <bookmark mark='b'/> "
            "Ordering by the likelihood ratio gives unified, never-empty intervals with correct coverage. <bookmark "
            "mark='c'/> One oddity remains: an experiment with more background that happens to see zero events reports a "
            "tighter limit than a cleaner experiment that saw the same zero, which troubles many physicists. <bookmark "
            "mark='d'/> Hence the alternatives in use at CERN, such as the CLs method and Bayesian limits with a flat prior "
            "on the non-negative signal."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("Poisson limits", "Feldman")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board, simulated at the flip-flop's worst signal strength. Flip-flopping covers "
                   "eighty-five and a half percent: broken. <bookmark mark='b'/> Feldman and Cousins's intervals cover ninety-two "
                   "percent there: conservative, as discrete intervals must be somewhere.",
                   [("a", [0]), ("b", [1])])
