from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import backtest as BT
from videos.quant.quant28.common import BAD, GOOD, HURDLE, OOS_C, PART, WORD, YLD, comma, fit_right, load


class Envelope(VoiceoverScene):
    def construct(self):
        e = load("envelope")
        self.card()
        self.register(e)
        self.research(e)
        self.opened(e)
        self.psr_(e)
        self.reading(e)
        self.question()

    def card(self):
        c = chapter_card(16, r"The text signal, registered and opened", r"Does the statement's score predict what the "
                         r"two-year does next?", part=PART)
        with self.voiceover("Chapter sixteen. One text signal from this part, registered with its trials counted, and "
                            "opened once on the sealed years 2021 to 2025."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def register(self, e):
        card = firm_card(r"The statement score, as a trade", r"SESTM fitted on every statement from 1997 to 2020, labelled by "
                         r"the two-year's move on the day; at the statement day's close, short the two-year note when the "
                         r"score is above one half, long below; hold five trading days",
                         numbers=((rf"{e['n_trials']}", r"trials: Chapter 5's twelve thresholds, plus this rule"),
                                  (r"1 \text{bp}", r"of yield per round trip, about eight a year: the cost charged")),
                         kind=r"Registered", width=10.6, font_size=22).move_to(UP * 0.3)
        ctr = MathTex(rf"\text{{the counter}}:\ {comma(e['trials'] - e['n_trials'])}\ \to\ {comma(e['trials'])}", font_size=30,
                      color=QC.HOUSE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The registration. <bookmark mark='a'/> Chapter five's model, refitted on every statement through 2020. The "
            "trade asks the obvious question: if the words lean hawkish, does the two-year keep rising after the "
            "statement day? At that day's close, short the two-year note when the score is above one half, buy it when "
            "below, and hold five trading days. <bookmark mark='b'/> "
            f"{e['n_trials']} trials: the twelve threshold pairs of Chapter five and the rule itself. The counter "
            f"moves to {e['trials']:,}."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(ctr))
        self.wait(0.4)
        self.clear_scene()

    def _cum_axes(self, dates, cum, color, title):
        d = np.asarray(dates)
        x = d // 10000 + ((d // 100) % 100 - 0.5) / 12
        y = 100 * np.asarray(cum, float)
        lo, hi = float(min(y.min(), 0) - 0.5), float(max(y.max(), 0) + 0.5)
        g = axes([x[0], x[-1]], [lo, hi], x_length=5.6, y_length=3.6, xlabel=title,
                 ylabel=r"cumulative return, \% of notional", xticks=[round(x[0]), round(x[-1])],
                 yticks=[round(lo), 0, round(hi)], font_size=13)
        ax = g.ax
        line = curve(ax, x, y, color, stroke_width=3)
        zero = DashedLine(ax.c2p(x[0], 0), ax.c2p(x[-1], 0), color=GREY_B, stroke_width=1.5)
        return VGroup(g, zero), line

    def research(self, e):
        (g1, l1) = self._cum_axes(e["research_dates"], e["cum_research"], WORD, r"1997--2020 (fitted on these years)")
        r = e["row"]["research"]
        VGroup(g1, l1).move_to(LEFT * 2.6 + DOWN * 0.2)
        side = VGroup(MathTex(rf"SR = {r['sharpe']:.2f} \pm {r['sharpe_se']:.2f}", font_size=26, color=WORD),
                      MathTex(rf"\text{{hit rate}}\ {100 * e['hit_research']:.0f}\%", font_size=24),
                      wrapped_label(r"even on the statements it was fitted to, the score says nothing about the next "
                                    r"five days: it learned the day's reaction, which is already in the price at the close",
                                    3.6, 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "First, the research years themselves, where the model was fitted. <bookmark mark='a'/> The trade goes "
            f"nowhere: a Sharpe ratio of {r['sharpe']:.2f}, right {100 * e['hit_research']:.0f} percent of the time. "
            "<bookmark mark='b'/> That is the point. The model learned to explain the statement day's move, and by the "
            "close of that day the move has happened. Explaining a reaction and predicting the next one are different "
            "problems."
        ) as vo:
            self.play(FadeIn(g1))
            vo.wait_until("a")
            self.play(Create(l1), FadeIn(side[0]), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def opened(self, e):
        (g2, l2) = self._cum_axes(e["hold_dates"], e["cum_hold"], OOS_C, r"2021--2025, sealed until now")
        h = e["row"]["holdout"]
        VGroup(g2, l2).move_to(LEFT * 2.6 + DOWN * 0.2)
        side = VGroup(MathTex(rf"SR = {h['sharpe']:.2f} \pm {h['sharpe_se']:.2f}", font_size=26, color=OOS_C),
                      MathTex(rf"\text{{net of costs}}:\ {h['sharpe_net']:.2f}", font_size=24),
                      MathTex(rf"{e['n_hold']}\ \text{{statements; hit rate}}\ {100 * e['hit_hold']:.0f}\%", font_size=24),
                      MathTex(rf"\text{{mean}}\ {e['mean_hold_bp']:+.1f}\ \text{{bp a trade}}", font_size=24)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            f"Then the envelope. <bookmark mark='a'/> {e['n_hold']} statements from January 2021 to December 2025, the years "
            "of the fastest tightening in four decades. <bookmark mark='b'/> The trade made "
            f"{e['mean_hold_bp']:+.1f} basis points of the note's value per statement on average, a Sharpe ratio of "
            f"{h['sharpe']:.2f} with a standard error of {h['sharpe_se']:.2f}, and it was right "
            f"{100 * e['hit_hold']:.0f} percent of the time: a coin."
        ) as vo:
            self.play(FadeIn(g2))
            vo.wait_until("a")
            self.play(Create(l2), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def psr_(self, e):
        h = e["row"]["holdout"]
        T = int(h["n"])
        sr_m = h["sharpe"] / np.sqrt(12)
        p0 = BT.psr(sr_m, 0.0, T)
        n95 = 1 + (1.645 / max(sr_m, 1e-6)) ** 2
        rows = [cmath(r"\widehat{SR}", r"=", rf"{sr_m:.3f}\ \text{{a statement month}},\quad T = {T}", font_size=32,
                      colors={r"\widehat{SR}": OOS_C}),
                cmath(r"\mathrm{PSR}(0)", r"=", r"\Phi\Big(\widehat{SR}\sqrt{T - 1}\big/\sqrt{1 + \tfrac12\widehat{SR}^2}\Big)"
                      rf" = {p0:.2f}", font_size=30, colors={r"\mathrm{PSR}(0)": HURDLE}),
                cmath(r"T_{95\%}", r"\approx", rf"1 + \big(1.645/{sr_m:.3f}\big)^2 \approx {1 + (1.645 / max(sr_m, 1e-6)) ** 2:.0f}"
                      r"\ \text{statements}", font_size=30)]
        whys = [why(r"the hold-out's Sharpe ratio per statement month (annualised above, as if every month had one)"),
                why(r"Part 26's probabilistic Sharpe ratio: the chance the true Sharpe ratio is above zero, given this "
                    r"estimate and this many observations (normal returns)"),
                why(r"how many statements it would take for an edge of this size to clear 95\%: at eight a year, decades")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Could it be a small real edge that five years were too short to see? <bookmark mark='a'/> Per statement "
            f"month the Sharpe ratio is {sr_m:.3f}, over {T} months. <bookmark mark='b'/> Part twenty-six's "
            f"probabilistic Sharpe ratio puts the chance that the true value is above zero at {100 * p0:.0f} percent. "
            "<bookmark mark='c'/> To push that to ninety-five percent, an edge this size would need about "
            f"{n95:.0f} statements: at eight a year, decades. Even if it is real, no one "
            "could know in time to use it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()


    def reading(self, e):
        cards = VGroup(
            desk_question(r"why it failed", r"the market reads the statement in minutes; a daily close is long after "
                          r"the words are priced. A statement signal needs either intraday data or a target the market "
                          r"has not yet seen", width=12.4, font_size=19),
            desk_question(r"what would be worth testing", r"the surprise in the words relative to expectations (Chapter 3's "
                          r"path factor), the minutes three weeks later, or text the market reads slowly: long filings, "
                          r"small firms' news", width=12.4, font_size=19),
            desk_question(r"what the Track Record keeps", r"the row, with its zero; the trials, counted. A null result "
                          r"registered in advance is information; the same result found after many tries would not be",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why? <bookmark mark='a'/> The market reads a statement in minutes. By the close, the words are priced; a "
            "daily signal from the same words is too late. <bookmark mark='b'/> Worth testing instead: the surprise in "
            "the words relative to what was expected, the minutes three weeks later, or text the market reads slowly, "
            "such as long filings and news about small firms. <bookmark mark='c'/> The Track Record keeps the row, "
            "with its zero, and the trials. A null result registered in advance is information."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the same score, measured from the release at 2 p.m.\ to the close of the day, would look "
                       r"excellent. Why is that not a tradable result?")
        with self.voiceover(
            "Pause and predict. The same score, measured from the release at two in the afternoon to the close, would "
            "look excellent. Why is that not a tradable result?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
