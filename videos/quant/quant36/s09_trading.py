from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (BAD, GOOD, HURDLE, MICRO_C, PART, comma, fit_right, load)


class Trading(VoiceoverScene):
    def construct(self):
        z = load("queue")
        self.card(z)
        self.priority()
        self.design(z)
        self.table(z)
        self.by_queue(z)
        self.value(z)
        self.option(z)
        self.race()
        self.makers()
        self.question()

    def card(self, z):
        c = chapter_card(8, r"Trading in the queue", r"What is a place in the queue worth, and what does a fill tell you?",
                         part=PART)
        mk = z["back"]["markout"]["1 s"]
        with self.voiceover(f"""Chapter eight. A back-of-queue fill can be adverse news, but its sign is conditional on order and market state. In this approximate replay, the average signed one-second markout at the back is {mk:.1f} ticks. That is a sample statistic under a specified fill model, not a universal property of passive trading."""):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def priority(self):
        rows = [cmath(r"\text{price, then time}", r":", r"\text{first in, first filled}", font_size=36),
                cmath(r"V(\text{front})", r">", r"V(\text{back})", font_size=40, colors={r"V(\text{front})": GOOD}),
                cmath(r"\text{fill}", r"\Rightarrow", r"\text{information}", font_size=40,
                      colors={r"\text{information}": BAD})]
        whys = [why(r"at one price, orders fill in the order they arrived: the queue is a line, and a place in it is an "
                    r"asset"),
                why(r"Moallemi and Yuan (2017): the front fills sooner and on smaller, less informed trades, so its "
                    r"value can be a sizeable fraction of the spread"),
                why(r"the event of being filled is itself news about the price; a passive trader is adversely selected "
                    r"(Part 35's Glosten--Milgrom, from the maker's chair)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Price-time priority. <bookmark mark='a'/> At one price, orders fill in the order they arrived: the queue "
            "is a line, and a place in it is an asset. <bookmark mark='b'/> Ciamac Moallemi and Kai Yuan valued it: the "
            "front fills sooner, on smaller and less informed trades, so its value can be a large fraction of the "
            "spread. <bookmark mark='c'/> And being filled is news. It is Part thirty-five's Glosten and Milgrom from "
            "the other chair: the trader who hits your order may know something."
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

    def design(self, z):
        n = z["back"]["n"]
        rows = [cmath(r"\text{every 30 s}", r":", r"\text{a tiny order joins the best bid or offer}", font_size=34),
                cmath(r"\text{ahead}", r"\leftarrow", r"\text{trades at its price};\ \text{cancels pro rata}", font_size=32),
                cmath(r"\text{markout}_h", r"=", r"\pm(M_{\text{fill}+h} - p)/\text{tick}", font_size=36,
                      colors={r"\text{markout}_h": MICRO_C})]
        whys = [why(rf"16 and 17 May 2023, {comma(n)} orders in all, on both sides, joined at the back or (hypothetically) "
                    r"at the front, whenever the spread is one tick; cancelled after a minute if unfilled"),
                why(r"the real trade tape eats the queue from the front; net cancellations are taken in proportion from "
                    r"the part ahead of us"),
                why('signed future mid minus execution price, in ticks; includes entry spread, whose exact fill-time value need not be half a tick')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The replay assumptions. <bookmark mark='a'/> Every thirty seconds at a one-tick spread, a negligible order joins the best bid or ask, at the back or hypothetically at the front; it expires after one minute if unfilled. Replay orders overlap and never affect the tape. <bookmark mark='b'/> At-price aggressive volume must strictly exceed the queue ahead to fill; through-price trades also fill. Net cancellations reduce ahead size pro rata, while displayed-size clipping and vanished-level conventions approximate priority. <bookmark mark='c'/> Signed markout is future mid less execution price for buys, reversed for sells, in ticks. It already includes the entry half-spread. Fees, rebates, hidden liquidity, latency and executable liquidation are excluded, and the execution-time mid need not be exactly half a tick away."
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

    def table(self, z):
        hx = [-4.4, -1.4, 1.2, 3.2, 5.2]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"", r"filled within 1 min", r"median wait",
                                                                         r"markout 1 s", r"markout 60 s")])
        tab = VGroup(head)
        for pos, name, col in (("back", r"back of the queue", BAD), ("front", r"front of the queue", GOOD)):
            r = z[pos]
            tab.add(VGroup(label(name, font_size=18, color=col), MathTex(f"{100 * r['fill']:.0f}\\%", font_size=26),
                           MathTex(f"{r['median_s']:.1f}\\ \\text{{s}}", font_size=26),
                           MathTex(f"{r['markout']['1 s']:+.1f}", font_size=26, color=col),
                           MathTex(f"{r['markout']['60 s']:+.1f}", font_size=26, color=col)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 1.0 * j, 0])
        foot = wrapped_label(r"markouts in ticks of \$0.10, averaged over fills; positive is good for the passive order",
                             11.0, 16, GREY_A).to_edge(DOWN, buff=0.7)
        bk, fr = z["back"], z["front"]
        se = bk["markout_se"]["1 s"]
        with self.voiceover(
            f"""Approximate fill outcomes. <bookmark mark='a'/> The back fill rate is {100 * bk['fill']:.0f} percent within a minute, with median filled wait {bk['median_s']:.1f} seconds. Its signed one-second markout is {bk['markout']['1 s']:.1f} ticks. The reported naive standard error is {se:.1f}; overlapping replay orders and market dependence prevent treating it as a robust interval. <bookmark mark='b'/> Front markout is {fr['markout']['1 s']:.1f} ticks, on a different set of fills. Different conditional fill populations and assumed priority both contribute. This comparison does not isolate a causal or executable value of queue position."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
        self.wait(0.4)
        self.clear_scene()

    def by_queue(self, z):
        bq = [r["q"] for r in z["back"]["by_queue"]]
        yb = [r["mk10"] for r in z["back"]["by_queue"]]
        yf = [r["mk10"] for r in z["front"]["by_queue"]]
        x = np.log10(bq)
        lo = float(np.floor(min(min(yb), min(yf)) / 10) * 10)
        hi = float(np.ceil(max(max(yb), max(yf), 0) / 10) * 10)
        g = axes([float(np.floor(x.min() * 4) / 4), float(np.ceil(x.max() * 4) / 4)], [lo, hi], x_length=6.4,
                 y_length=4.4, xlabel=r"queue at the moment of joining, BTC", ylabel=r"markout 10 s after fill, ticks",
                 xticks=[0, 0.5, 1.0], xfmt=lambda v: f"10^{{{v:g}}}", yticks=[lo, 0, hi], yfmt=lambda v: f"{v:.0f}",
                 font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(x.min() - 0.2, 0), ax.c2p(x.max() + 0.2, 0), color=GREY_B, stroke_width=1.2)
        cb = VGroup(curve(ax, x, yb, BAD, stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.07, color=BAD)
                                                             for a, b in zip(x, yb)])
        cf = VGroup(curve(ax, x, yf, GOOD, stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.07, color=GOOD)
                                                              for a, b in zip(x, yf)])
        leg = legend([(BAD, r"joined at the back"), (GOOD, r"at the front")], font_size=16).to_edge(RIGHT, buff=0.3)
        leg.shift(UP * 1.6)
        fit_right(leg)
        with self.voiceover(
            f"""Stratify the model's outcomes by displayed queue size. <bookmark mark='a'/> Back-of-queue signed mean markouts range from {yb[0]:.0f} to {yb[-1]:.0f} ticks across the displayed groups. Queue depletion and price continuation can create this selection; the replay does not identify informed orders. <bookmark mark='b'/> The front means range from {yf[0]:.0f} to {yf[-1]:.0f} ticks, with different conditional filled sets. A positive group mean is not net profit or proof that the queue behind causally protected the order. Group boundaries use this sample's quantiles and can share exact endpoint observations."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), Create(zero))
            vo.wait_until("a")
            self.play(Create(cb))
            vo.wait_until("b")
            self.play(Create(cf))
        self.wait(0.4)
        self.clear_scene()

    def value(self, z):
        bk, fr = z["back"], z["front"]
        vb = bk["fill"] * bk["markout"]["1 s"]
        vf = fr["fill"] * fr["markout"]["1 s"]
        gap = vf - vb
        rows = [cmath(r"V(\text{back})", r"=", rf"{bk['fill']:.2f} \times ({bk['markout']['1 s']:.1f}) = {vb:.1f}",
                      font_size=36, colors={r"V(\text{back})": BAD}),
                cmath(r"V(\text{front})", r"=", rf"{fr['fill']:.2f} \times ({fr['markout']['1 s']:.1f}) = {vf:.1f}",
                      font_size=36, colors={r"V(\text{front})": GOOD}),
                cmath(r"V(\text{front}) - V(\text{back})", r"\approx", rf"{gap:.0f}\ \text{{ticks}}", font_size=38,
                      colors={rf"{gap:.0f}\ \text{{ticks}}": HURDLE})]
        whys = [why('gross mark-to-mid contribution per submission; unfilled value set to zero'),
                why(r"the same, had the order been at the head of the line"),
                why('difference of replay gross functionals; excludes opportunity, inventory, fees, latency and executable liquidation; not a causal priority price')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""A partial per-submission accounting convention. <bookmark mark='a'/> Give unfilled orders zero value and multiply back fill probability by the conditional signed one-second markout: {vb:.1f} ticks per submission. <bookmark mark='b'/> The same front calculation gives {vf:.1f}. <bookmark mark='c'/> Their difference is {gap:.1f} ticks in this replay. This compares an explicit gross mark-to-mid functional; it is not a causal queue-priority price or net strategy profit. It omits unfilled opportunity costs, inventory, fees, rebates, cancellation decisions and liquidation. The entry half-spread is already inside each markout and must not be added again."""
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

    def option(self, z):
        bk = z["back"]
        rows = [cmath(r"\text{filled}", r"\Rightarrow", '\\text{adverse selection can occur}', font_size=36,
                      colors={r"\text{filled}": BAD}),
                cmath(r"\text{not filled}", r"\Rightarrow", rf"\text{{it ran away}}:\ {bk['missed']:+.0f}\ \text{{ticks}}",
                      font_size=36, colors={r"\text{not filled}": HURDLE}),
                cmath(r"\text{quote-option model}", r":", r"\text{stale-price exposure}", font_size=31)]
        whys = [why('conditional fills and missed orders have different selection; this replay does not prove every fill is adverse'),
                why(r"the orders that missed saw the mid move away from them over the minute: the trade you wanted, gone"),
                why(r"Copeland and Galai (1983): a standing quote is an option the next informed trader may exercise; "
                    r"the spread is its premium, and a maker must reprice it as fast as the news arrives")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""Read the two conditional samples carefully. <bookmark mark='a'/> Some fills are followed by adverse movement, but a fill need not imply that price traded through the order or that the counterparty was informed. <bookmark mark='b'/> In this replay, missed orders have a mean signed away-move of {bk['missed']:.0f} ticks over the waiting window. Filled and missed orders are selected differently, not matched counterfactual outcomes. <bookmark mark='c'/> Copeland and Galai model a resting limit quote as an option offered to the market, with stale-price risk under their assumptions. Real cancellations, changing spreads and inventory also matter; this analogy does not make every limit order an unpriced free option."""
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

    def race(self):
        rows = [cmath(r"\text{news}", r"\Rightarrow", r"\text{a race}", font_size=40),
                cmath(r"\text{maker}", r":", r"\text{cancel the stale quote}", font_size=36, colors={r"\text{maker}": GOOD}),
                cmath(r"\text{sniper}", r":", r"\text{take it first}", font_size=36, colors={r"\text{sniper}": BAD})]
        whys = [why(r"when the value moves, every resting quote on the wrong side is suddenly mispriced"),
                why(r"its owner tries to withdraw it; the time that takes is the length of the free option"),
                why(r"Budish, Cramton and Shim (Part 35): someone else tries to trade against it in the same "
                    r"microseconds; with price-time priority and a continuous book, the race is won by speed, and the "
                    r"loss is built into every spread")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The race behind the markouts. <bookmark mark='a'/> When the value moves, every resting quote on the wrong "
            "side is suddenly mispriced. <bookmark mark='b'/> Its owner tries to cancel it, and the time that takes is "
            "how long the free option stays open. <bookmark mark='c'/> Someone else tries to take it first, in the same "
            "microseconds. In a continuous book the race is won by speed, and, as Part thirty-five showed, the expected "
            "loss is built into every spread."
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

    def makers(self):
        cards = VGroup(
            desk_question(r"cancel early", 'a candidate cancellation signal needs independent evaluation; the replay does not implement dynamic cancellation', width=12.4, font_size=19),
            desk_question(r"queue early", r"join a price level before it becomes the best, to hold a place near the "
                          r"front; the race for that place is Part 35's latency arms race", width=12.4, font_size=19),
            desk_question(r"be paid", 'fees or rebates depend on venue and tier; realized profit also requires inventory and liquidation accounting', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Possible maker controls. <bookmark mark='a'/> A validated signal can guide cancellation, but an overshooting or delayed estimate can remove favorable fills as well as adverse ones. The replay order here does not dynamically cancel. <bookmark mark='b'/> Queue placement, entry time and price selection affect fill probability and selection. <bookmark mark='c'/> A full realized-profit account needs trading cash flows, inventory marks, fees or rebates and eventual liquidation, plus latency and control costs where relevant. A single post-fill markout is one component of that account, not the account itself."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        head = label('A partial replay functional, with no double-counted spread', font_size=29, color=QC.IDEA).to_edge(UP, buff=0.45)
        formula = MathTex('p_{\\rm fill}=0.8,\\quad\\mathbb E[\\mathrm{markout}\\mid\\mathrm{fill}]=-2\\ \\text{ticks},\\quad r=0.1\\ \\text{tick/fill}', font_size=33).move_to(UP * 1.2)
        if formula.width > 12.4:
            formula.scale_to_fit_width(12.4)
        assumptions = wrapped_label('Markout already includes entry half-spread. Unfilled orders are assigned zero. Ignore all other costs here.', 12.2, 20, GREY_A).move_to(DOWN * 0.1)
        question = wrapped_label('Compute per-submission contribution including rebate. Which omitted terms prevent calling it complete net profit?', 12.2, 25, QC.IDEA).move_to(DOWN * 1.75)
        banner = label(r"Pause: derive the answer and check its assumptions and units.", font_size=19, color=QC.IDEA).to_edge(DOWN, buff=0.35)
        with self.voiceover('A stipulated replay fills eighty percent of submissions. Conditional signed markout is minus two ticks and already includes the entry half-spread. A rebate adds one tenth of a tick per fill. Give unfilled orders zero. Calculate the contribution per submission without adding half-spread again, and identify the inventory, liquidation and opportunity terms still absent.'):
            self.play(FadeIn(head), FadeIn(formula), FadeIn(assumptions), FadeIn(question), FadeIn(banner))
        self.wait(6)
        self.clear_scene()
