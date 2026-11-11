from __future__ import annotations

import numpy as np
from scipy.stats import norm

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, GBMC, PART, RISKY, load, lesson_cards

FIRMS = {"BA": "Boeing", "AAL": "American Airlines", "NCLH": "Norwegian Cruise Line"}


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.comparison()
        self.module()

    def card(self):
        c = chapter_card(17, r"Rule 20: the credit desk", r"Where should a default probability come from?", part=PART)
        with self.voiceover("Chapter seventeen. The House's twentieth rule, for its credit desk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))


    def module(self):
        chart = house_chart(PART, lit=("credit",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{merton\_equity}, \texttt{merton\_solve}, \texttt{kmv\_iterate}", r"equity as a call; assets from "
                                                                                       r"prices; distance to default"),
            (r"\texttt{black\_cox\_pd}", r"first passage through a barrier"),
            (r"\texttt{survival}, \texttt{risky\_zero}, \texttt{cds\_legs}", r"hazards, recovery conventions, the two legs"),
            (r"\texttt{bootstrap\_hazard}, \texttt{cds\_upfront}", r"a hazard curve from quotes; the Big Bang's upfronts"),
            (r"\texttt{altman\_z}, \texttt{logit\_fit}, \texttt{GBM}, \texttt{auc}", r"default prediction, scored"),
            (r"\texttt{vasicek\_*}, \texttt{basel\_irb\_k}", r"the large pool and bank capital"),
            (r"\texttt{copula\_defaults}, \texttt{lhp\_tranche\_el}, \texttt{base\_correlation}", r"baskets and tranches"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=17, color=QC.HOUSE), label(b, font_size=17, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.2)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 20: compare the same event, horizon, information date and probability measure. "
                             r"Investigate disagreements; evaluate calibration and dependence scenarios; name the "
                             r"exposure and residual risk of every hedge. No new market trial or sealed access in this review.",
                             12.4, 21, QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The credit desk opens with these tools. <bookmark mark='a'/> Merton's equity inversion and distance to default; first passage; intensity and recovery models; the swap's premium and protection legs; hazard bootstrapping; synthetic classification; the large-pool capital approximation; and default dependence and tranches. <bookmark mark='b'/> Rule twenty: align the event, horizon, information date and probability measure before comparing numbers. Assess calibration with independent data and disclose model uncertainty. Compare Gaussian dependence with plausible tail and concentration scenarios; a chosen fat-tailed copula is a stress assumption, not an automatic conservative bound. Name the exposure, sensitivity and residual basis risk of each hedge. This presentation review registers no new market trial and opens no sealed experiment."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["credit"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def comparison(self):
        title, cards = lesson_cards('Compare probabilities only after aligning their meaning', [
            ('Event and horizon', 'Bankruptcy filing, payment default and terminal assets below a boundary are different events'),
            ('Date and information', 'Use the same forecast date; audit filing availability and freeze market calibration in advance'),
            ('Measure and calibration', 'Physical event forecasts differ from risk-neutral pricing probabilities and uncalibrated normal-tail proxies'),
            ('Disagreement', 'Accounts and prices share information; investigate assumptions and uncertainty before combining them'),
        ])
        with self.voiceover("The credit desk must first ask whether two probabilities describe the same thing. A bankruptcy filing over twelve months, a contractual missed payment, and assets below a model boundary at a terminal date are different events. <bookmark mark='a'/> Align the horizon and forecast date. Audit when accounts became public and whether market calibration uses future prices. Our legacy distance curves are retrospective month-end fits, while the accounting lesson here is synthetic; their outputs cannot be displayed as two validated forecasts for the same real company. <bookmark mark='b'/> Align the probability measure too. A risk-neutral input used to price protection differs from a physical forecast of event frequency. A normal-tail transformation of a distance is not automatically an empirically calibrated probability. Accounts and market prices are different channels, but they share information and are not statistically independent by construction. Investigate disagreements, model uncertainty and shared exposures before combining numbers. A factor-of-four escalation rule could be a desk policy, but it is not a mathematical test of which source is right.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until('a'); self.play(FadeIn(cards[1]))
            vo.wait_until('b'); self.play(FadeIn(cards[2]))
            if len(cards) > 3: self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()
