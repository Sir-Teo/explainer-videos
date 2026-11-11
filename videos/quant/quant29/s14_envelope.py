from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, COMB, GOOD, HURDLE, PART


class Envelope(VoiceoverScene):
    """Evaluation protocol and fixed arithmetic; no experiment loader or historical strategy score."""
    def construct(self):
        self.card()
        self.freeze()
        self.book()
        self.cost()
        self.reading()
        self.question()

    def card(self):
        card = chapter_card(13, r"Evaluating a mined combination", r"What must be fixed before a future result means anything?", part=PART)
        with self.voiceover("Chapter thirteen. An evaluation protocol for a mined combination. The sealed strategy result is excluded. We will specify the information and decisions a future test needs, then work through explicitly fixed portfolio arithmetic. No historical payoff is read or scored."):
            self.play(FadeIn(card[0]), FadeIn(card[1]))
        self.play(FadeOut(card))

    def freeze(self):
        cards = VGroup(
            desk_question(r"freeze information and selection", r"data vintage, release and execution times, universe rules, missing outcomes, signals, signs, weights, tuning and stopping", width=12.4, font_size=19),
            desk_question(r"specify the attainable portfolio", r"orders, depth, financing, borrow, costs, leverage, rebalancing and exit accounting", width=12.4, font_size=19),
            desk_question(r"specify inference and reporting", r"dependence, selection, multiplicity, power, benchmarks and all later decisions; a fresh period alone is insufficient", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover("Three layers to freeze. <bookmark mark='a'/> Define the data vintage, information times and complete selection rule, including signs, weighting and stopping. A label date is not an execution timestamp. <bookmark mark='b'/> Specify the portfolio that can actually trade: liquidity, borrow, financing, costs, leverage and exits. A same-close research convention is not an attainable fill. <bookmark mark='c'/> Define the inferential target, benchmarks, dependence assumptions, multiplicity and reporting policy. A fresh period can still have low power, regime change or hidden selection. The protocol is a requirement for a future evaluation, not evidence that this excluded strategy passed.") as vo:
            for k, mark in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mark)
                self.play(FadeIn(cards[k]))
        self.wait(0.4)
        self.clear_scene()

    def book(self):
        rows = [cmath(r"q", r"=", r"(0,1,2,3),\quad \bar q=1.5", font_size=33),
                cmath(r"w_i", r"=", r"\frac{2(q_i-\bar q)}{\sum_j|q_j-\bar q|}=(-0.75,-0.25,0.25,0.75)_i", font_size=30),
                cmath(r"\sum_i w_i", r"=", r"0,\quad \sum_i|w_i|=2,\quad \sum_{w_i>0}w_i=1", font_size=32)]
        whys = [why(r"four fixed, distinct ranks; no asset, date or historical sample is used"),
                why(r"demean ranks and scale absolute exposure to two: one dollar long, one short"),
                why(r"dollar neutrality does not imply beta neutrality, financing neutrality or zero risk")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover("A fixed four-position toy, not a market experiment. <bookmark mark='a'/> The ranks are zero, one, two and three, with mean one point five. <bookmark mark='b'/> Demeaning and scaling to absolute exposure two gives weights minus 0.75, minus 0.25,0.25 and0.75. <bookmark mark='c'/> Long exposure is one dollar, short exposure minus one, and gross exposure two. The net dollar exposure is zero. Beta, financing and risk are separate questions. This is only the arithmetic behind a rank book.") as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def cost(self):
        w = np.array([-0.75, -0.25, 0.25, 0.75])
        r = np.array([-0.01, 0.01, 0.02, 0.0])
        gross_bp = float(w @ r) * 1e4
        traded = float(np.abs(w).sum() + (np.abs(w) * (1 + r)).sum())
        cost_bp = 5.0 * traded
        net_bp = gross_bp - cost_bp
        rows = [cmath(r"r", r"=", r"(-1\%,+1\%,+2\%,0),\quad P_0=(100,100,100,100)", font_size=29),
                cmath(r"w^\top r", r"=", rf"{gross_bp:.0f}\ \text{{bp per dollar long}}", font_size=33),
                cmath(r"\text{entry + exit cost}", r"=", rf"5\ \text{{bp per dollar traded}}\times {traded:.1f}={cost_bp:.0f}\ \text{{bp}}", font_size=29),
                cmath(r"\text{toy net}", r"=", rf"{gross_bp:.0f}-{cost_bp:.0f}={net_bp:.0f}\ \text{{bp per dollar long}}", font_size=32, colors={r"\text{toy net}": GOOD})]
        whys = [why(r"explicitly chosen simple price returns; the original research helper instead linearly weights log returns"),
                why(r"fixed shares held for this one interval, no leverage beyond the stated book"),
                why(r"entry from flat trades two dollars; closing at these chosen end prices trades two more"),
                why(r"fixed arithmetic only: financing, borrow, slippage and market impact are omitted")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(f"Choose prices explicitly. <bookmark mark='a'/> All four start at one hundred. Their simple returns are minus one percent, plus one, plus two and zero; no historical series is used. <bookmark mark='b'/> Multiplying those returns by the fixed initial weights gives {gross_bp:.0f} basis points per dollar long. <bookmark mark='c'/> Starting flat trades two dollars, and at these chosen final prices closing trades another two. At five basis points per dollar traded, total entry and exit costs are {cost_bp:.0f} basis points per dollar long. <bookmark mark='d'/> The resulting fixed net is {net_bp:.0f} basis points. These are simple-return, fixed-share calculations; the original research score uses weighted log returns. Borrow, financing, slippage and impact are omitted, so this toy is neither a historical strategy result nor a performance forecast.") as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def reading(self):
        cards = VGroup(
            desk_question(r"units and denominators", r"state whether returns are per dollar long, gross exposure, capital or margin; distinguish log-return scores from portfolio P\&L", width=12.4, font_size=19),
            desk_question(r"availability and exits", r"missing future returns must not silently remove losses or create hindsight weights", width=12.4, font_size=19),
            desk_question(r"no score from a protocol", r"a specification and a fixed arithmetic example provide no historical payoff, p-value, posterior or power claim", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover("Read any future result with three checks. <bookmark mark='a'/> Align its exposure denominator and distinguish log-return scores from portfolio cash flows. <bookmark mark='b'/> Account for missing outcomes and exits without hindsight reweighting. <bookmark mark='c'/> A protocol and a fixed toy supply no historical payoff, p-value, posterior probability or power estimate. Those require a specified experiment and valid evidence; none is supplied by opening an excluded result.") as vo:
            for k, mark in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mark)
                self.play(FadeIn(cards[k]))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        card = pause_card(r"The fixed book earns 100 bp per dollar long before costs. Entry and exit trade \$4 at 5 bp per dollar. What is its toy net, and which risks remain omitted?")
        with self.voiceover("Pause and predict. In this fixed toy, a hundred basis points gross, four dollars traded at five basis points per dollar: what is the net per dollar long, and which real trading risks remain outside the calculation?"):
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()
