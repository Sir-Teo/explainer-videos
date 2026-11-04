from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant33.common import BAD, COST_C, GOOD, HURDLE, PART, SPREAD_C, fit_right, load


class Pairs(VoiceoverScene):
    def construct(self):
        p = load("pairs")
        self.card()
        self.rule()
        self.example(p)
        self.decades(p)
        self.why_not(p)
        self.literature()
        self.question()

    def card(self):
        c = chapter_card(2, r"Pairs by distance", r"Does the simplest pairs rule still work?", part=PART)
        with self.voiceover("Chapter two. In 2006 Evan Gatev, William Goetzmann and Geert Rouwenhorst wrote down the rule "
                            "the desks had used, and tested it on forty years of American stocks."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rule(self):
        rows = [cmath(r"p_{i,t}", r"=", r"\textstyle\prod_{s\le t}(1 + r_{i,s})", font_size=36),
                cmath(r"\text{SSD}_{ij}", r"=", r"\textstyle\sum_{t\in\text{formation}} (p_{i,t} - p_{j,t})^2", font_size=34,
                      colors={r"\text{SSD}_{ij}": SPREAD_C}),
                cmath(r"\text{open}", r":", r"|p_i - p_j| > 2\,\hat\sigma_{ij};\quad \text{close at the crossing}", font_size=32),
                cmath(r"\text{windows}", r":", r"12\ \text{months to form},\ 6\ \text{to trade},\ \text{the 20 closest pairs}",
                      font_size=30)]
        whys = [why(r"each asset's total-return index, normalised to one at the start of the formation window"),
                why(r"the distance between two normalised price paths: the pairs that moved most alike"),
                why(r"in the trading window, when the gap exceeds two of its formation standard deviations, short the high "
                    r"one and buy the low one, a dollar each; close when the paths cross"),
                why(r"Gatev, Goetzmann and Rouwenhorst's choices, re-run here with no changes")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "The rule has no model at all. <bookmark mark='a'/> Normalise each asset's total-return index to one. "
            "<bookmark mark='b'/> Over a year, measure the distance between every pair of paths, and keep the twenty "
            "closest. <bookmark mark='c'/> Over the next six months, when a pair's gap exceeds twice its formation "
            "standard deviation, sell the high one and buy the low one, and close when the paths cross. "
            "<bookmark mark='d'/> These are the original paper's choices, re-run here unchanged on the forty-nine "
            "industries."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def example(self, p):
        e = p["example"]
        d = np.asarray(e["dates"], float)
        x = np.arange(len(d))
        pi, pj = np.asarray(e["pi"], float), np.asarray(e["pj"], float)
        lo = float(np.floor(min(pi.min(), pj.min()) * 20) / 20)
        hi = float(np.ceil(max(pi.max(), pj.max()) * 20) / 20)
        top = axes([0, len(x)], [lo, hi], x_length=8.0, y_length=2.6, xlabel="", ylabel=r"normalised prices",
                   xticks=[], yticks=[lo, hi], yfmt=lambda v: f"{v:.2f}", font_size=14).move_to(UP * 1.5 + LEFT * 0.8)
        sp = pi - pj
        lim = float(max(abs(sp).max(), 2.5 * e["sd"]))
        bot = axes([0, len(x)], [-lim, lim], x_length=8.0, y_length=2.2, xlabel=r"trading days, second half of 2008",
                   ylabel=r"the gap", xticks=[], yticks=[], font_size=14).move_to(DOWN * 1.6 + LEFT * 0.8)
        c1 = curve(top.ax, x, pi, QC.SPOT, stroke_width=2.5)
        c2 = curve(top.ax, x, pj, QC.DELTA, stroke_width=2.5)
        cs = curve(bot.ax, x, sp, SPREAD_C, stroke_width=2.5)
        bands = VGroup(*[DashedLine(bot.ax.c2p(0, k * 2 * e["sd"]), bot.ax.c2p(len(x), k * 2 * e["sd"]), color=HURDLE,
                                    stroke_width=1.5) for k in (-1, 1)])
        zero = DashedLine(bot.ax.c2p(0, 0), bot.ax.c2p(len(x), 0), color=GREY_C, stroke_width=1)
        leg = legend([(QC.SPOT, e["pair"][0]), (QC.DELTA, e["pair"][1])], font_size=16).to_edge(RIGHT, buff=0.4)
        leg.shift(UP * 2.0)
        fit_right(leg)
        with self.voiceover(
            "One pair, the closest at the start of the second half of 2008: the telecommunications and business-services "
            "industries. <bookmark mark='a'/> In the formation year they moved almost as one. <bookmark mark='b'/> In "
            "the trading window the gap broke through its band within a month as the crisis hit them differently, took "
            "about three months to close, and then opened the other way. A pair that was close in calm times is not "
            "necessarily close in a crisis."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(c1), Create(c2), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(zero), Create(bands), Create(cs), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def decades(self, p):
        dec = p["decades"]
        keys = list(dec)
        mx = max(abs(dec[k]["sharpe"]) for k in keys)
        bars = VGroup()
        for j, k in enumerate(keys):
            v = dec[k]["sharpe"]
            r = Rectangle(width=max(abs(v) * 4.0 / mx, 0.03), height=0.5, fill_color=GOOD if v > 0 else BAD,
                          fill_opacity=0.85, stroke_width=0).move_to([0.4, 2.0 - 0.75 * j, 0],
                                                                     aligned_edge=LEFT if v > 0 else RIGHT)
            bars.add(VGroup(label(rf"{k}s", font_size=21, color=GREY_A).move_to([-4.4, 2.0 - 0.75 * j, 0]), r,
                            MathTex(f"{v:+.2f}", font_size=24).next_to(r, RIGHT if v > 0 else LEFT, buff=0.15)))
        axis = Line([0.4, 2.5, 0], [0.4, -2.2, 0], color=GREY_C, stroke_width=1.5)
        head = label(r"The distance rule on the 49 industries, Sharpe ratio by decade", font_size=26).to_edge(UP, buff=0.4)
        foot = wrapped_label(rf"before costs; on committed capital (zero while a pair is flat); {p['n_ind']} industries with "
                             rf"complete histories; {100 * p['opened']:.0f}\% of pairs opened at least once; "
                             rf"{p['trips']:.1f} round trips per pair per six months", 11.6, 16, GREY_A).to_edge(DOWN, buff=0.3)
        a = p["all"]
        with self.voiceover(
            "The result, decade by decade. <bookmark mark='a'/> In the 1960s and 70s the rule lost steadily; in the 90s "
            "and 2010s it earned a little. <bookmark mark='b'/> Over the whole period, a Sharpe ratio of "
            f"{a['sharpe']:.2f} before costs, on a return of {100 * a['mean']:+.1f} percent a year. On industries, the "
            "simplest pairs rule does not work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.25))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def why_not(self, p):
        cards = VGroup(
            desk_question(r"industries trend", r"whole industries carry momentum (Moskowitz and Grinblatt 1999): a "
                          r"diverging pair of industries is often a trend beginning, not noise reverting", width=12.4,
                          font_size=19),
            desk_question(r"stocks are different", r"single stocks within an industry share a common driver, and their "
                          r"idiosyncratic gaps are what reverts: Gatev, Goetzmann and Rouwenhorst found up to 11\% a year "
                          r"for 1962--2002 on stocks, before costs", width=12.4, font_size=19),
            desk_question(r"the gap is not a model", r"the rule never asks why two paths moved together, so it cannot "
                          r"tell a temporary gap from a permanent break", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why not? <bookmark mark='a'/> Whole industries carry momentum, as Tobias Moskowitz and Mark Grinblatt "
            "found: two industries drifting apart are often a trend beginning, not noise reverting. "
            "<bookmark mark='b'/> Stocks are different. Within an industry, a stock's idiosyncratic gap is what "
            "reverts, and the original paper found up to eleven percent a year on stocks from 1962 to 2002, before "
            "costs. <bookmark mark='c'/> And the rule has no model: it never asks why two paths moved together, so it "
            "cannot tell a temporary gap from a permanent break."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def literature(self):
        cards = VGroup(
            desk_question(r"Do and Faff (2010)", r"the distance rule's returns on stocks declined steadily after the "
                          r"1980s; much of what remained was earned in turbulent markets", width=12.4, font_size=19),
            desk_question(r"costs", r"each round trip trades four times on two legs; at the House's 5 bp per side the "
                          r"industries would pay about 0.5\% a year, and stocks, with wider spreads and shorting fees, far "
                          r"more", width=12.4, font_size=19),
            desk_question(r"the lesson", r"a rule without a reason decays first: the next chapters add the reason, a "
                          r"model of why the spread should revert", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And the literature agrees. <bookmark mark='a'/> Binh Do and Robert Faff found the rule's returns on "
            "stocks declining steadily after the 1980s, with much of what remained earned in turbulent markets. "
            "<bookmark mark='b'/> Costs make it worse: every round trip trades four times on two legs. "
            "<bookmark mark='c'/> A rule without a reason decays first. The next chapters add the reason: a model of "
            "why a spread should revert at all."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a pair's gap reverts with a half-life of 20 days, and you hold for 6 months at most. Is the "
                       r"two-standard-deviation trigger too wide, too narrow, or about right?")
        with self.voiceover(
            "Pause and predict. A pair's gap reverts with a half-life of twenty days, and you can hold for six months at "
            "most. Is a two-standard-deviation trigger too wide, too narrow, or about right?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
