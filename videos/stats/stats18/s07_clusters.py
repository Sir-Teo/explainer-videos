from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from explainer.stats.world import World
from videos.stats.stats18.common import *  # noqa: F403


class Clusters(VoiceoverScene):
    def construct(self):
        self.card()
        self.why_clusters()
        self.icc_deff()
        self.one_sample()
        self.board()
        self.pps()
        self.pps_result()
        self.multistage()

    def card(self):
        card = chapter_card(6, r"Clusters and stages", r"Cheaper interviews, \ correlated answers", part=PART)
        with self.voiceover("Chapter six. Clusters and stages."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def multistage(self):
        rows = fit_rows(VGroup(
            label(r"a national household survey, \ for instance a labour force survey:", font_size=24),
            label(r"strata: \ regions $\times$ urban/rural", font_size=22, color=OBS),
            label(r"stage 1: \ areas drawn with probability proportional to size", font_size=22, color=HIT),
            label(r"stage 2: \ households within each area; \ stage 3: \ people within households", font_size=22, color=RESP),
            label(r"standard errors: \ linearization, \ or replicate weights (jackknife, \ bootstrap: \ Part 16)", font_size=22, color=GREY_A),
            label(r"analyse as designed: \ strata, \ clusters and weights all enter the SE", font_size=24, color=RES),
        ), 12.4, 0.42, [0, 0, 0])
        with self.voiceover(
            "Real surveys combine everything in this chapter. <bookmark mark='a'/> A national household survey, such as a "
            "labour force survey that measures unemployment, <bookmark mark='b'/> stratifies the country by region and by "
            "urban and rural areas; <bookmark mark='c'/> draws areas within each stratum with probability proportional to "
            "size; <bookmark mark='d'/> then households within each area, and sometimes one person per household. "
            "<bookmark mark='e'/> Standard errors come from formulas that follow the design, or from replicate weights: the "
            "survey releases dozens of alternative weight columns, made by Part 16's jackknife or bootstrap applied to the "
            "clusters, and each estimate is recomputed with every column. <bookmark mark='f'/> The rule is to analyse as "
            "designed. Software that treats survey records as independent observations will report standard errors that are "
            "much too small."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def why_clusters(self):
        d = load("cluster")
        Wd = World()
        mp = IslandMap(Wd.towns, center=[-2.4, 0.0, 0], scale=0.72)
        rows = fit_rows(VGroup(
            label(r"an SRS of 1,000 sends interviewers to nearly every town", font_size=22),
            label(r"instead: \ pick 20 towns, \ then 50 adults in each", font_size=24, color=RESP),
            label(r"a two-stage cluster sample", font_size=22, color=GREY_A),
            label(r"cheap: \ 20 trips instead of 150", font_size=22, color=HIT),
            label(r"but neighbours vote alike", font_size=22, color=RES),
        ), 4.4, 0.42, [4.7, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A simple random sample of a thousand people scatters them over most of the island's towns, and "
            "face-to-face interviews mean sending someone to each. <bookmark mark='b'/> It's far cheaper to choose twenty towns at "
            "random, then fifty adults within each. <bookmark mark='c'/> That's a two-stage cluster sample. "
            "<bookmark mark='d'/> Twenty trips instead of a hundred and fifty. <bookmark mark='e'/> The catch: people in the same "
            "town tend to resemble each other, so fifty neighbours carry less information than fifty strangers."
        ) as vo:
            self.play(Create(mp.coast), FadeIn(mp.dots))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(mp.highlight(d["towns"], RESP, scale=1.8), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def icc_deff(self):
        d = load("cluster")
        rows = [
            cmath(r"\rho", r"=", r"\text{the correlation of two adults in the same town}", font_size=30),
            cmath(r"\hat\rho", r"=", rf"{d['icc']:.4f}\ \ \text{{for the vote}}", font_size=32),
            cmath(r"\text{deff}", r"=", rf"1 + (m - 1)\rho = 1 + 49 \times {d['icc']:.4f} = {d['deff']:.2f}", font_size=30),
            cmath(r"n_{\text{eff}}", r"=", rf"1{{,}}000 / {d['deff']:.2f} = {d['neff']:.0f}", font_size=32),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"the intraclass correlation (Part 13's ANOVA)"), why(r"tiny: \ towns differ a little, \ by region"),
                why(r"Kish (1965): \ the design effect"), why(r"1,000 interviews, \ worth 567 random ones")]
        with self.voiceover(
            "<bookmark mark='a'/> The resemblance is measured by the intraclass correlation: the correlation between the votes "
            "of two adults in the same town, from Part 13's analysis of variance. <bookmark mark='b'/> In the World it's tiny, "
            "point oh one five six: towns differ only slightly, mostly because regions do. <bookmark mark='c'/> But it's "
            "multiplied. Leslie Kish's design effect is one plus m minus one times rho, where m is the number per cluster: one "
            "point seven six with fifty per town. <bookmark mark='d'/> So the cluster sample's thousand interviews are worth a "
            "simple random sample of five hundred and sixty-seven. A correlation too small to notice costs almost half the "
            "sample, which is fine if it halves the cost, but the analysis must know about it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def one_sample(self):
        d = load("cluster")
        cm = np.asarray(d["town_means"])
        A = axes([0, 0.8], [0, 7], x_length=8.0, y_length=3.0, xlabel=r"Blue's share in each sampled town (50 adults)",
                 ylabel=r"towns", xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[0, 3, 6], center=[-1.4, 1.2, 0],
                 xfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        e = np.linspace(0, 0.8, 17)
        bars = hist_bars(ax, e, np.histogram(cm, e)[0], color=RESP, opacity=0.8)
        tr = DashedLine(ax.c2p(d["truth"], 0), ax.c2p(d["truth"], 6.8), color=S.TRUTH, stroke_width=3)
        rows = fit_rows(VGroup(
            MathTex(rf"\hat p = {100 * d['est']:.1f}\%", font_size=30, color=RESP),
            MathTex(rf"\text{{SRS formula}}: \sqrt{{\hat p(1 - \hat p)/1000}} = {100 * d['naive_se']:.2f}", font_size=26),
            MathTex(rf"\text{{cluster SE}}: \text{{SD of the 20 town shares}}/\sqrt{{20}} = {100 * d['cluster_se']:.2f}", font_size=26,
                    color=HIT),
            label(r"the honest SE treats the towns as the units", font_size=22, color=GREY_A),
        ), 12.0, 0.26, [0, -2.45, 0])
        tag = simulated_tag(r"one cluster sample", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Here's one cluster sample: the share for Blue in each of the twenty towns, fifty adults each. "
            "Overall, thirty-seven point three percent. <bookmark mark='b'/> The SRS formula pretends the thousand people were "
            "independent: a standard error of one point five three points. <bookmark mark='c'/> The design-based standard "
            "error treats the twenty towns as the independent units: the spread of the town shares over the square root of "
            "twenty. In this sample it happens to be close, one point five nine. <bookmark mark='d'/> Over many samples, "
            "though, the difference shows."
        ) as vo:
            self.play(FadeIn(A), Create(tr), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.05), FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=18) if r.part == 18 and "towns" in r.method]
        b = coverage_board(rows, lit_part=18, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "The Board: ten thousand cluster samples of twenty towns and fifty adults. <bookmark mark='a'/> With the SRS "
            "formula, ninety-five percent intervals cover the truth eighty-four percent of the time: broken, as the design "
            "effect predicts. <bookmark mark='b'/> With the cluster standard error and a t-multiplier on nineteen degrees of "
            "freedom, ninety-three percent: much closer, a little short. The rest is a small bias: choosing towns with "
            "equal chances and then fifty adults in each over-represents people in small towns, whose votes differ slightly. "
            "Fixing that is the next idea."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[1]))
        self.wait(1.0)
        self.clear_scene()

    def pps(self):
        rows = [
            cmath(r"\text{estimate}", r":", r"\text{the World's total income, \ from 10 towns}", font_size=30),
            cmath(r"\text{equal chances}", r":", r"\hat T = 200 \times \text{mean of the town totals}", font_size=30),
            cmath(r"\text{PPS}", r":", r"p_t \propto \text{town size},\ \ \hat T = \tfrac{1}{10}\textstyle\sum T_t / p_t", font_size=30),
            cmath(r"\text{why}", r":", r"T_t/p_t \text{ is nearly constant}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"towns from 537 to 142,332 adults"), why(r"a lucky city changes everything"),
                why(r"Hansen \& Hurwitz (1943): \ with replacement"), why(r"a town's total is roughly its size $\times$ the mean")]
        with self.voiceover(
            "Clusters raise a second question: should every town have the same chance? <bookmark mark='a'/> Suppose we want "
            "the World's total income from a sample of ten towns, which range from five hundred to a hundred and forty thousand "
            "adults. <bookmark mark='b'/> With equal chances, we'd multiply the average town total by two hundred, and the "
            "estimate would swing wildly depending on whether the capital happened to be drawn. <bookmark mark='c'/> Morris "
            "Hansen and William Hurwitz, at the US Census Bureau in 1943, drew towns with probability proportional to size, "
            "and divided each town's total by its probability. <bookmark mark='d'/> Since a town's total income is roughly "
            "its size times the mean, that ratio is nearly the same for every town, and the estimate barely varies."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pps_result(self):
        d = load("pps")
        tab = table_rows([
            [r"10 towns, \ 4,000 samples", r"mean of $\hat T$", r"SD of $\hat T$"],
            [r"equal probabilities", rf"{d['mean_eq'] / 1e6:.1f} million", rf"{d['sd_eq'] / 1e6:.1f} million"],
            [r"probability proportional to size", rf"{d['mean_hh'] / 1e6:.2f} million", rf"{d['sd_hh'] / 1e6:.2f} million"],
        ], font_size=28, colors=[GREY_B, RES, HIT]).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            MathTex(rf"\text{{truth}}: {d['T'] / 1e6:.2f}\ \text{{million (thousands of the currency)}}", font_size=26),
            label(rf"PPS: \ {d['ratio_sd']:.0f} times more precise", font_size=26, color=HIT),
            label(r"both unbiased; \ one is useless", font_size=22, color=GREY_A),
        ), 12.4, 0.3, [0, -1.9, 0])
        tag = simulated_tag(r"the World's 200 towns", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Four thousand samples of ten towns each. With equal probabilities, the estimates average roughly "
            "the truth, thirty-six point seven million, but their standard deviation is thirty-eight million: as large as "
            "the thing being estimated. <bookmark mark='b'/> With probabilities proportional to size, the standard deviation is "
            "a fifth of a million. <bookmark mark='c'/> A hundred and seventy-four times more precise, from the same ten "
            "towns' worth of work. Both designs are unbiased. Only one is useful."
        ) as vo:
            self.add(tag)
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]), FadeIn(foot[2]))
        self.clear_scene()
