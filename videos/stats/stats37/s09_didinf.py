from __future__ import annotations

import numpy as np

from videos.stats.stats37.common import *  # noqa: F403


class DiDInference(VoiceoverScene):
    def construct(self):
        self.card()
        self.persistence()
        self.bdm()
        self.placebo()
        self.fixes()
        self.board()

    def card(self):
        card = chapter_card(8, r"DiD inference", r"How much should we trust differences-in-differences estimates?", lit=(2004,), part=PART)
        with self.voiceover("Chapter eight. Inference for differences-in-differences."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def persistence(self):
        d = load("didinf")
        R = np.asarray(d["resid_towns"], float)
        yrs = np.arange(2000, 2020)
        A = axes([2000, 2019], [-3, 3], x_length=7.6, y_length=4.0, xlabel=r"year", ylabel=r"town shock (points)",
                 xticks=[2000, 2005, 2010, 2015], yticks=[-2, 0, 2], xfmt=lambda v: f"{v:.0f}", center=[-1.8, 0.2, 0])
        ax = A.ax
        cols = [Y0C, Y1C, TAUC, BANDC, IVC, GREY_A]
        lines = VGroup(*[polyline(ax, yrs, R[i], cols[i], 2.5) for i in range(len(R))])
        side = fit_rows(VGroup(
            label(r"six towns' untreated employment, \ town and year effects removed", font_size=22),
            label(r"a good year is followed by another good year", font_size=22, color=TAUC),
            label(rf"year-to-year correlation: \ {d['autocorr']:.2f}", font_size=22, color=MISSC),
            label(r"twenty years of one town are not twenty independent observations", font_size=22, color=GREY_A),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The hard part of differences-in-differences is the standard error. Here are six of the "
            "World's towns, their employment with the town and year effects taken out. <bookmark mark='b'/> The shocks "
            "persist: a good year tends to be followed by another. <bookmark mark='c'/> The correlation from one year to the "
            "next is " + say(d["autocorr"], 2) + ". <bookmark mark='d'/> So twenty years of one town carry far less "
            "information than twenty independent observations, and a standard error that treats them as independent will "
            "be too small."
        ) as vo:
            self.add(rollout_tag())
            self.play(FadeIn(A), Create(lines), FadeIn(side[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k + 1]))
        self.clear_scene()

    def bdm(self):
        rows = fit_rows(VGroup(
            label(r"Bertrand, \ Duflo \& Mullainathan (2004): \ women's wages in the Current Population Survey, \ 50 states", font_size=26, color=TAUC),
            label(r"invent laws: \ pick states and years at random, \ and estimate the laws' effects by DiD", font_size=26),
            label(r"the laws do not exist, \ so a 5\% test should reject 5\% of the time", font_size=26, color=BANDC),
            label(r"with conventional standard errors it rejected about 45\% of the time", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2004 Marianne Bertrand, Esther Duflo and Sendhil Mullainathan ran a devastating check, "
            "using wages of women in the Current Population Survey across fifty American states. <bookmark mark='b'/> They "
            "invented laws: chose states and years at random, pretended a law had passed, and estimated its effect by "
            "differences-in-differences, as the published studies did. <bookmark mark='c'/> The laws did not exist, so a "
            "five percent test should have found an effect five percent of the time. <bookmark mark='d'/> With the "
            "conventional standard errors, it found one about forty-five percent of the time."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def placebo(self):
        d = load("didinf")
        e = np.linspace(-0.6, 0.6, 25)
        h = np.asarray(d["betas"], float)
        A = axes([-0.6, 0.6], [0, 0.16], x_length=7.6, y_length=4.0, xlabel=r"estimated effect of a law that does not exist",
                 ylabel=r"share of placebo laws", xticks=[-0.5, -0.25, 0, 0.25, 0.5], yticks=[0, 0.05, 0.1, 0.15],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-1.8, 0.2, 0])
        ax = A.ax
        bars = hist_bars(ax, e, h / d["reps"], color=Y0C, opacity=0.6)
        cO = 1.96 * d["se_ols"]
        cC = 1.96 * d["se_cl"]
        lo = VGroup(*[DashedLine(ax.c2p(s * cO, 0), ax.c2p(s * cO, 0.16), color=MISSC, stroke_width=3) for s in (-1, 1)])
        lc = VGroup(*[DashedLine(ax.c2p(s * min(cC, 0.6), 0), ax.c2p(s * min(cC, 0.6), 0.16), color=BANDC, stroke_width=3) for s in (-1, 1)])
        side = fit_rows(VGroup(
            label(rf"{d['reps']:,} placebo laws in half of the World's towns", font_size=22),
            label(rf"red: \ $\pm 1.96$ OLS SE: \ rejects {100 * d['rej_ols']:.0f}\%", font_size=22, color=MISSC),
            label(rf"green: \ $\pm 1.96$ town-clustered SE: \ rejects {100 * d['rej_cl']:.1f}\%", font_size=22, color=BANDC),
            label(rf"mean clustered SE {d['se_cl'] / d['se_ols']:.1f} times as large", font_size=22, color=GREY_A),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Repeat it in the World. A thousand placebo laws, each passed in a random half of the "
            "towns in a random year, estimated with two-way fixed effects on the towns' untreated employment. <bookmark "
            "mark='b'/> With the ordinary least squares standard error, the test rejects " + str(round(100 * d["rej_ols"]))
            + " percent of the time, almost exactly what Bertrand and her colleagues found. <bookmark mark='c'/> With "
            "standard errors clustered by town, which allow any correlation within a town over time, it rejects "
            + say(100 * d["rej_cl"], 1) + " percent of the time. <bookmark mark='d'/> The honest standard error is "
            + say(d["se_cl"] / d["se_ols"], 1) + " times as large as the naive one."
        ) as vo:
            self.add(rollout_tag())
            self.play(FadeIn(A), FadeIn(bars), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lo), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lc), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def fixes(self):
        rows = fit_rows(VGroup(
            label(r"cluster by the unit of treatment: \ the town, \ the state \ (Part 23)", font_size=26, color=BANDC),
            label(r"or collapse each unit to one before and one after average", font_size=26, color=Y0C),
            label(r"few treated clusters: \ the wild cluster bootstrap \ (Part 23), \ or randomization inference over placebo laws", font_size=26, color=TAUC),
            label(r"one treated state: \ inference needs additional assumptions; \ chapter 11", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The fixes are the ones Part twenty-three introduced. Cluster the standard errors by"
            " the unit at which the policy was assigned: the town, or the state. <bookmark mark='b'/> Or collapse "
            "each unit's data to one average before and one after, forming one change per unit instead of treating "
            "every year as an independent observation. <bookmark mark='c'/> With few treated clusters, ordinary "
            "cluster asymptotics can be unreliable. Some wild-bootstrap methods also fail in that setting; valid "
            "randomization inference needs a justified assignment mechanism, and placebo comparisons need "
            "exchangeability assumptions. <bookmark mark='d'/> With only one treated unit, inference requires "
            "additional design or structural assumptions. Chapter eleven uses placebo comparisons, whose validity "
            "also needs justification."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("DiD test")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board, as tests of size five percent: ordinary least squares standard errors "
                   "on the World's placebo laws, broken. <bookmark mark='b'/> Standard errors clustered by town, kept.",
                   [("a", [0]), ("b", [1])])
