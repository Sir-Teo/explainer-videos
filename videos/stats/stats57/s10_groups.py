from __future__ import annotations

import numpy as np

from videos.stats.stats57.common import *  # noqa: F403


class Groups(VoiceoverScene):
    def construct(self):
        self.card()
        self.mondrian()
        self.mondrian_worked()
        self.table()
        self.bars()
        self.board()
        self.slack()
        self.fairness()

    def card(self):
        card = chapter_card(9, r"Mondrian and group-conditional coverage", r"Coverage for every group, \ on NHANES", lit=(2005, 2023), part=PART)
        with self.voiceover("Chapter nine. Mondrian and group-conditional coverage, on NHANES blood pressures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def mondrian(self):
        rows = [
            cmath(r"\text{Mondrian}", r":", r"\text{a separate quantile in each group: \ disjoint groups only}", font_size=34),
            cmath(r"\text{guarantee}", r":", r"P(Y \in C \mid G = g) \ge 1 - \alpha \ \text{ for every } g", font_size=36),
            cmath(r"\text{overlapping groups}", r":", r"\text{a full intersection partition can be sparse}", font_size=34),
            cmath(r"\text{chapter 4}", r":", r"\mathcal F = \text{span of the indicators: \ exact coverage in every group}", font_size=32),
        ]
        rows[1][-1].set_color(COVC)
        rows[3][-1].set_color(COVC)
        whys = [why(r"Vovk et al. (2005)"), why(r"the lemma within each group"), why(r"partitions only"), why(r"Gibbs, \ Cherian \& Cand\`es")]
        head = label('Mondrian', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> The oldest answer to subgroup coverage is Vovk's Mondrian conformal prediction: calibrate separately within each group. <bookmark mark='b'/> By the lemma applied within each group, every group gets at least one minus alpha. <bookmark mark='c'/> A single Mondrian partition is disjoint. Refining to all age-sex-race intersection cells can cover their unions, but may leave sparse cells and infinite thresholds. The class method borrows structure across overlapping groups. <bookmark mark='d'/> Chapter four's method does it, with the class spanned by all the group indicators."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mondrian_worked(self):
        rows = [
            cmath(r"\text{group A}, \ n_A = 50", r":", r"k = 46: \ \text{coverage } 46/51 = 90.2\%, \ \text{SD } 4.1", font_size=34),
            cmath(r"\text{group B}, \ n_B = 500", r":", r"k = 451: \ 451/501 = 90.0\%, \ \text{SD } 1.3", font_size=34),
            cmath(r"\text{both}", r":", r"\text{exact on average, \ within each group}", font_size=36),
            cmath(r"\text{but}", r":", r"\text{the small group's realized coverage varies three times more}", font_size=32),
        ]
        rows[2][-1].set_color(COVC)
        rows[3][-1].set_color(MISSC)
        whys = [why(r"the lemma, \ per group"), why(r"the lemma, \ per group"), why(r"Mondrian's promise"), why(r"Beta spreads")]
        head = label('Mondrian worked', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Two groups, with fifty and five hundred calibration points, at alpha a tenth. In the "
            "small group the threshold is the forty-sixth score, and coverage is forty-six in fifty-one, ninety point "
            "two percent, with a standard deviation of four points across calibration sets. <bookmark mark='b'/> In "
            "the large group, the four hundred and fifty-first score: ninety point oh percent, standard deviation one "
            "point three. <bookmark mark='c'/> Both are exact on average, within each group. <bookmark mark='d'/> But "
            "the small group's realized coverage varies three times as much: a guarantee for minorities is only as "
            "sharp as the data on them."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("nhanes")
        S = d["summary"]
        groups = d["groups"]
        hdr = [r"group", r"$n$", r"marginal", r"Mondrian (age)", r"group-conditional"]
        body = []
        cols = []
        for g in groups:
            m, mo, gc = S["marginal"][g], S["mondrian"][g], S["gcc"][g]
            body.append([g, f"{d['counts'][g]:,}", f"{100 * m:.1f}\\%", f"{100 * mo:.1f}\\%", f"{100 * gc:.1f}\\%"])
            cols.append(MISSC if m < 0.875 else WHITE)
        tab = table_rows([hdr] + body, font_size=22, col_buff=0.55, row_buff=0.13, colors=[GREY_B] + cols).move_to([0, 0.3, 0])
        foot = fit_rows(VGroup(
            label(rf"NHANES 2017--18: \ systolic pressure from age, \ sex and BMI by least squares; \ {d['reps']} random splits; \ $\alpha = 0.1$", font_size=22, color=GREY_A),
            label(rf"marginal: \ {100 * d['overall']['marginal']:.1f}\% overall, \ but the old and the young are miscovered", font_size=24, color=MISSC),
            label(r"fixed-extract resplitting illustration; \ no national population coverage certification", font_size=24, color=COVC),
        ), 10.0, 0.16, [-1.3, -2.6, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> NHANES, the 2017 to 2018 survey: predict systolic blood pressure from age, sex and body-mass index by least squares, and build ninety percent intervals, over {d['reps']} random splits. <bookmark mark='b'/> Marginal split conformal covers {100 * d['overall']['marginal']:.1f} percent overall, but {100 * S['marginal']['70+']:.0f} percent of people over seventy, whose pressures vary more, and {100 * S['marginal']['18-29']:.0f} percent of those under thirty. <bookmark mark='c'/> Mondrian calibration by age band fixes the age rows, but not the others. <bookmark mark='d'/> The group-conditional method, with the age, sex and race indicators together, is compared across all ten named groups. These are repeated splits of one survey extract, with no population survey weighting or cluster correction. They are not independent national cohorts or a population-wide clinical guarantee."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(museum_tag(r"NHANES 2017--18, \ CDC/NCHS")))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.12), FadeIn(foot[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(VGroup(*[r[2] for r in tab[1:]]), color=MISSC), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(Indicate(VGroup(*[r[3] for r in tab[1:]]), color=CALC))
            vo.wait_until("d")
            self.play(Indicate(VGroup(*[r[4] for r in tab[1:]]), color=COVC), FadeIn(foot[2]))
        self.clear_scene()

    def bars(self):
        d = load("nhanes")
        S, groups = d["summary"], d["groups"]
        k = len(groups)
        A = axes([-0.6, k - 0.4], [0, 1.0], x_length=11.0, y_length=4.2, ylabel=r"coverage of 90\% intervals",
                 yticks=[0, .5, .75, .9, 1], center=[0.2, 0.4, 0])
        ax = A.ax

        def bar(i, v, c):
            # Values are drawn without clamping; the full probability axis contains every bar.
            return Rectangle(width=abs(ax.c2p(0.32, 0)[0] - ax.c2p(0, 0)[0]), height=max(0.01, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]),
                             stroke_width=1, stroke_color=c, fill_color=c, fill_opacity=0.7).move_to(ax.c2p(i, v / 2))
        bm = VGroup(*[bar(i - 0.18, S["marginal"][g], MISSC) for i, g in enumerate(groups)])
        bg = VGroup(*[bar(i + 0.18, S["gcc"][g], COVC) for i, g in enumerate(groups)])
        names = VGroup(*[label(g, font_size=20, color=GREY_A).next_to(ax.c2p(i, 0), DOWN, buff=0.15) for i, g in enumerate(groups)])
        nom = DashedLine(ax.c2p(-0.6, 0.9), ax.c2p(k - 0.4, 0.9), color=GREY_B, stroke_width=2)
        lo = min(groups, key=lambda g: S["marginal"][g])
        hi = max(groups, key=lambda g: S["marginal"][g])
        spread = max(abs(S["gcc"][g] - 0.9) for g in groups)
        foot = fit_rows(VGroup(
            label(rf"red: \ marginal, \ from {100 * S['marginal'][lo]:.0f}\% ({lo}) to {100 * S['marginal'][hi]:.0f}\% ({hi})", font_size=24, color=MISSC),
            label(rf"green: \ group-conditional, \ every bar within {100 * spread:.1f} points of 90\%", font_size=24, color=COVC),
        ), 10.0, 0.16, [-1.3, -2.85, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The same numbers as bars, one pair per group. <bookmark mark='b'/> The marginal method's "
            f"bars, in red, run from {100 * S['marginal'][lo]:.0f} percent for the {lo} group to {100 * S['marginal'][hi]:.0f} "
            f"percent for the {hi} group: the right average, made of wrong parts. <bookmark mark='c'/> The group-conditional "
            f"bars, in green, all sit within {100 * spread:.1f} points of the ninety percent line, though the groups overlap: "
            f"everyone belongs to an age band, a sex and a race group at once."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names), Create(nom), FadeIn(museum_tag(r"NHANES 2017--18, \ CDC/NCHS")))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bm], lag_ratio=0.08), FadeIn(foot[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bg], lag_ratio=0.08), FadeIn(foot[1]), run_time=2.5)
        self.clear_scene()

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("ages 70+"),
                   f"<bookmark mark='a'/> On the Board, people over seventy: marginal split conformal covers "
                   f"{100 * br[2]['achieved']:.1f} percent of them. <bookmark mark='b'/> The group-conditional method covers "
                   f"{100 * br[3]['achieved']:.1f} percent.", [("a", [0]), ("b", [1])])

    def slack(self):
        rows = [
            cmath(r"\text{groups}", r":", r"\text{11 basis columns, \ two redundancies: \ dimension }9", font_size=34),
            cmath(r"\text{calibration}", r":", r"n=1{,}200:\quad \text{group upper slack}\le\frac{9}{1{,}201\,P(X\in G)}", font_size=36),
            cmath(r"\text{small groups}", r":", r"\text{coverage within them is noisy, \ though correct on average}", font_size=34),
            cmath(r"\text{so}", r":", r"\text{name groups you can afford to calibrate}", font_size=36),
        ]
        rows[1][-1].set_color(COVC)
        whys = [why(r"with the constant"), why(r"the over-coverage bound"), why(r"Beta-like spread"), why(r"the design question")]
        head = label('Group slack depends on prevalence', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> How much did it cost? The design has eleven basis columns, but two linear redundancies leave dimension nine: the intercept is the sum of age indicators and also the sum of sex indicators. <bookmark mark='b'/> With twelve hundred calibration points, the marginal continuity-based upper slack is at most dimension over twelve hundred and one. For an individual group divide that bound by its population prevalence; it can be much larger than one percent. <bookmark mark='c'/> Small groups get correct coverage on average, and their observed coverage is noisy. The Beta formula for an ordinary within-group order statistic is not an exact law for this overlapping-group optimizer. <bookmark mark='d'/> So name groups you can afford to calibrate: that is a design decision, made before the data arrive."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fairness(self):
        rows = fit_rows(VGroup(
            label(r"why it matters:", font_size=28, color=GREY_A),
            label(r"a marginal guarantee can be met by over-serving the majority and under-serving a minority", font_size=26, color=MISSC),
            label(r"group-conditional coverage is a fairness requirement that can be audited", font_size=26, color=COVC),
            label(r"its price: \ wider intervals in harder groups, \ and enough data in each", font_size=26, color=WEIGHTC),
            label(r"and the groups must be named in advance: \ chapter 3's impossibility still holds", font_size=26, color=TESTPT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why this matters. <bookmark mark='b'/> A marginal guarantee can be met by over-serving the "
            "majority and under-serving a minority. <bookmark mark='c'/> Group-conditional coverage is a fairness requirement "
            "that can be stated and audited. <bookmark mark='d'/> Its price is wider intervals in the harder groups, and enough "
            "calibration data in each. <bookmark mark='e'/> And the groups must be named in advance: chapter three's "
            "impossibility still forbids coverage for every group at once."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
