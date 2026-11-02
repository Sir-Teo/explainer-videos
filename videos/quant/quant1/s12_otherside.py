from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import GAIN, GAUSS, LOSS, PART, REAL

ROLES = [
    (r"Hedgers", r"want less risk: an airline buying fuel, a farmer selling a crop forward, a pension fund buying "
                 r"puts. They pay to be insured.", QC.CASH),
    (r"Speculators", r"want more of one risk: they have a view, or think they do. Black's noise traders are among "
                     r"them.", QC.IDEA),
    (r"Market makers", r"want no view at all: they quote both sides, earn the spread, and manage what they are left "
                       r"holding (Part 38).", QC.GAMMA),
    (r"Arbitrageurs", r"want no risk: they buy what is cheap and sell what is dear in the same thing, and so keep "
                      r"prices consistent (Part 9).", REAL),
]


class OtherSide(VoiceoverScene):
    def construct(self):
        self.card()
        self.roles()
        self.arithmetic()
        self.industry()

    def card(self):
        c = chapter_card(11, r"Who is on the other side?", r"When you buy, who sells, and why?",
                         lit=(1982, 1988, 1990, 2000, 2001), part=PART)
        with self.voiceover("Chapter eleven. Who is on the other side?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def roles(self):
        cards = VGroup(*[definition_card(n, b, color=c, width=6.0, font_size=22, kind=r"Who trades")
                         for n, b, c in ROLES]).arrange_in_grid(2, 2, buff=(0.4, 0.4)).shift(UP * 0.35)
        foot = wrapped_label(r"Every trade has a buyer and a seller. In a fair game, someone is paying for something: "
                             r"insurance, a view, immediacy, or a mistake.", 12.0, 24, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Every time you buy, someone sells. If prices are fair, why would they? Because people trade for "
            "different reasons. Hedgers want less risk. An airline buys its fuel in advance, a farmer sells their "
            "crop forward, a pension fund buys protection against a crash; they pay to be insured. "
            "<bookmark mark='a'/> Speculators want more of one particular risk, because they have a view, or think "
            "they do. <bookmark mark='b'/> Market makers want no view at all. They stand ready to buy and to sell, "
            "earn the gap between their two prices, and manage whatever they are left holding. "
            "<bookmark mark='c'/> Arbitrageurs want no risk: they buy something cheap and sell the same thing dear, "
            "and in doing so they keep prices consistent with each other. <bookmark mark='d'/> In a fair game, "
            "every trade is someone paying for something: insurance, a view, immediacy, or a mistake."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[3], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def arithmetic(self):
        bar = VGroup()
        W = 10.0
        whole = Rectangle(width=W, height=0.9, stroke_color=GREY_B, stroke_width=2)
        split = 0.5
        pas = Rectangle(width=W * split, height=0.9, stroke_width=0, fill_color=REAL, fill_opacity=0.5)
        act = Rectangle(width=W * (1 - split), height=0.9, stroke_width=0, fill_color=QC.IDEA, fill_opacity=0.5)
        VGroup(pas, act).arrange(RIGHT, buff=0).move_to(whole)
        lp = label(r"passive: holds the market", font_size=24).move_to(pas)
        la = label(r"active: everyone else", font_size=24).move_to(act)
        top = label(r"every share of the market is held by someone", font_size=26, color=GREY_A).next_to(whole, UP, buff=0.3)
        bar.add(whole, pas, act, lp, la, top)
        bar.to_edge(UP, buff=0.9)
        rows = [
            MathTex(r"R_{\text{market}} = w\,R_{\text{passive}} + (1 - w)\,R_{\text{active}}", font_size=40),
            MathTex(r"R_{\text{passive}} = R_{\text{market}}", font_size=40, color=REAL),
            MathTex(r"\Rightarrow\ \ R_{\text{active}} = R_{\text{market}}\ \ \text{before costs}", font_size=40,
                    color=QC.IDEA),
        ]
        VGroup(*rows).arrange(DOWN, buff=0.35).next_to(bar, DOWN, buff=0.6)
        card = history_card(1991, r"William Sharpe, \textit{Financial Analysts Journal}",
                            r"``The arithmetic of active management'': before costs, the average actively managed "
                            r"dollar must earn the market's return; after costs, it must earn less. Not a theory: "
                            r"an identity.", width=9.0, font_size=22).to_edge(DOWN, buff=0.35)
        idx = note(r"end of 2023: index funds held more US fund assets than active funds for the first time "
                   r"(\$13.3 trillion; Morningstar)", font_size=18).to_corner(UR, buff=0.2)
        with self.voiceover(
            "Before asking who wins, one piece of arithmetic that settles a great deal. Every share of the market is "
            "held by someone. Some holders are passive: they own the whole market, in proportion. Everyone else is "
            "active. <bookmark mark='a'/> The market's return is the weighted average of the two groups. The passive "
            "group earns exactly the market return. So the active group, taken together, must earn the market's "
            "return too, before costs. <bookmark mark='b'/> William Sharpe called this the arithmetic of active "
            "management, in 1991. After costs, the average active dollar must do worse than the market. Relative "
            "to the market, active investing is a zero-sum game before costs and a losing one after them. Any "
            "active manager who wins does so at the expense of another active manager. By the end of 2023, index "
            "funds held more American fund assets than active funds, for the first time."
        ) as vo:
            self.play(FadeIn(bar))
            vo.wait_until("a")
            for r_ in rows:
                self.play(Write(r_))
            vo.wait_until("b")
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(idx))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def industry(self):
        W, fs = 6.3, 20
        c1 = firm_card(r"Market makers and proprietary traders",
                       r"Jane Street, Citadel Securities, Optiver, Jump, Hudson River Trading, Virtu: quote both sides "
                       r"on exchanges and to brokers, earn the spread, hedge, and do it at enormous scale and speed.",
                       [(r"\$20.5\,\text{bn}", r"Jane Street's net trading revenue, 2024, as reported from its "
                                               r"bond-offering documents"),
                        (r">35\%", r"of US retail volume, executed by Citadel Securities (its own figure)")],
                       r"Bloomberg (2025); citadelsecurities.com", width=W, font_size=fs)
        c2 = firm_card(r"Systematic hedge funds",
                       r"Renaissance Technologies, D.\ E.\ Shaw, Two Sigma, AQR: trading rules found in data and run by "
                       r"machines, from seconds to months.",
                       [(r"66\%\ /\ 39\%", r"Medallion's average yearly return before / after fees, 1988--2018: "
                                           r"arithmetic averages, as reported, unaudited")],
                       r"Zuckerman, \textit{The Man Who Solved the Market} (2019)", width=W, font_size=fs)
        c3 = firm_card(r"Multi-manager platforms",
                       r"Citadel, Millennium, Point72, Balyasny: hundreds of small teams under tight risk limits, "
                       r"with capital moved towards whoever is earning (Part 34).", (), r"the firms' public descriptions",
                       width=W, font_size=fs)
        c4 = firm_card(r"Banks, dealers and asset managers",
                       r"Banks make markets in bonds, currencies and derivatives and sell structured products; asset "
                       r"managers run the savings of the world, and the largest of them run index funds.",
                       [(r"\$13.3\,\text{tn}", r"in US index funds at the end of 2023, ahead of active funds for the "
                                               r"first time")], r"Morningstar (January 2024)", width=W, font_size=fs)
        grid = VGroup(c1, c2, c3, c4).arrange_in_grid(2, 2, buff=(0.3, 0.3), aligned_edge=UP)
        if grid.height > 7.3:
            grid.scale_to_fit_height(7.3)
        grid.move_to(DOWN * 0.05)
        rule = note(r"Firm files use the public record only: filings, published research, the firms' own statements, "
                    r"books. Reported figures are labelled as such.", font_size=16).to_edge(DOWN, buff=0.08)
        with self.voiceover(
            "So who are the professionals on the other side? The firms this series will keep meeting fall into four "
            "groups. Market makers and proprietary traders: Jane Street, Citadel Securities, Optiver, Jump and "
            "others, quoting both sides at enormous scale. Jane Street's net trading revenue in 2024 was reported "
            "at about twenty and a half billion dollars, from documents for its bond sales; Citadel Securities says "
            "it executes more than a third of American retail trading volume. <bookmark mark='a'/> Systematic hedge "
            "funds, which find trading rules in data and let machines run them. The most famous, Renaissance "
            "Technologies' Medallion fund, is reported to have averaged sixty-six percent a year before fees from "
            "1988 to 2018, thirty-nine after them: figures from a book, not an audit, and averages, not compound "
            "growth. <bookmark mark='b'/> Multi-manager platforms, which run hundreds of small teams under tight "
            "risk limits; Part thirty-four goes inside one. <bookmark mark='c'/> And the banks, dealers and asset "
            "managers, who run most of the world's money, more and more of it in index funds. Everything in these "
            "files comes from the public record, and a reported number is labelled as reported."
            " Next: the first person to show, with mathematics, that the other side can be beaten."
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2), FadeIn(rule))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c3, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(c4, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
