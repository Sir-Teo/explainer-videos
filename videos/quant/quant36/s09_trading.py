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
        with self.voiceover("Chapter eight, and the answer to the pause: usually, no. A resting order at the back of a "
                            "queue is filled when the whole queue ahead of it has been eaten, and that tends to happen "
                            f"just before the price goes through. On Bitcoin's book, one second after such a fill the mid "
                            f"was on average {abs(mk):.0f} ticks against the order."):
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
                why(r"the mid a time $h$ after the fill, less the price we traded at, signed so that positive is good "
                    r"for us; at the moment of fill it is half a tick")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The experiment. <bookmark mark='a'/> Every thirty seconds when the spread is one tick, a tiny order joins "
            "the best bid or offer, at the back of the queue, or, as a thought experiment, at the front. "
            "<bookmark mark='b'/> The real trade tape eats the queue from the front, and cancellations are taken in "
            "proportion from the part ahead of us. <bookmark mark='c'/> When filled, we mark the order to the mid a "
            "second, ten seconds and a minute later, in ticks, positive when it is good for us. At the instant of the "
            "fill it earns half the spread: half a tick."
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
            f"The result. <bookmark mark='a'/> At the back of the queue, {100 * bk['fill']:.0f} percent of orders are "
            f"filled within a minute, after a median {bk['median_s']:.1f} seconds. One second after the fill, the mid is "
            f"on average {abs(bk['markout']['1 s']):.1f} ticks against the order, give or take {se:.1f}, and it stays "
            "there. The half tick of spread is swamped. <bookmark mark='b'/> At the front, the fill comes almost at once, "
            f"and the markout is only {abs(fr['markout']['1 s']):.1f} ticks against. The same price, the same day: "
            "position in the line is most of the difference."
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
            "By the size of the queue, in five groups. <bookmark mark='a'/> At the back, the longer the queue, the worse "
            f"the fill: from {abs(yb[0]):.0f} ticks against with a short queue to {abs(yb[-1]):.0f} with a long one, "
            "because only a big, informed sweep clears a long queue. <bookmark mark='b'/> At the front it is the other "
            f"way round. With a short queue the fill is still bad, {abs(yf[0]):.0f} ticks against. But at the front of "
            f"a long queue the markout turns positive, about {yf[-1]:.0f} ticks: the queue behind protects you, because "
            "small trades fill you and large ones must eat the rest of the queue before the price moves."
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
        whys = [why(r"expected markout per order placed, in ticks, one second after the fill"),
                why(r"the same, had the order been at the head of the line"),
                why(r"the value of the place in the line: many times the half-tick spread the order nominally earns, "
                    r"which is why makers race to be first (Moallemi and Yuan)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Put a price on the place in line. <bookmark mark='a'/> Per order placed at the back, the fill probability "
            f"times the markout: about {abs(vb):.0f} ticks lost. <bookmark mark='b'/> At the front, about "
            f"{abs(vf):.1f}. <bookmark mark='c'/> The difference, about {gap:.0f} ticks, is the value of being first: "
            "many times the half tick of spread the order nominally earns. That is why makers race to the head of the "
            "line."
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
        rows = [cmath(r"\text{filled}", r"\Rightarrow", r"\text{the price came through you}", font_size=36,
                      colors={r"\text{filled}": BAD}),
                cmath(r"\text{not filled}", r"\Rightarrow", rf"\text{{it ran away}}:\ {bk['missed']:+.0f}\ \text{{ticks}}",
                      font_size=36, colors={r"\text{not filled}": HURDLE}),
                cmath(r"\text{a limit order}", r"=", r"\text{a free option written to the market}", font_size=34)]
        whys = [why(r"the fills you get are the ones you would rather not have had"),
                why(r"the orders that missed saw the mid move away from them over the minute: the trade you wanted, gone"),
                why(r"Copeland and Galai (1983): a standing quote is an option the next informed trader may exercise; "
                    r"the spread is its premium, and a maker must reprice it as fast as the news arrives")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Both ways at once. <bookmark mark='a'/> When the order is filled, the price came through it. "
            "<bookmark mark='b'/> When it is not, the price ran away: over the minute, unfilled orders saw the mid move "
            f"{bk['missed']:.0f} ticks away from them. The fills you get are the ones you would rather not have had, and "
            "the ones you miss are the ones you wanted. <bookmark mark='c'/> Thomas Copeland and Dan Galai's picture: a "
            "standing limit order is a free option written to the market. The spread is its premium, and whoever writes "
            "it must reprice it as fast as news arrives."
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
            desk_question(r"cancel early", r"withdraw when the microprice or the order-flow imbalance turns against the "
                          r"quote; our tiny order never cancels, which is why it is picked off", width=12.4, font_size=19),
            desk_question(r"queue early", r"join a price level before it becomes the best, to hold a place near the "
                          r"front; the race for that place is Part 35's latency arms race", width=12.4, font_size=19),
            desk_question(r"be paid", r"exchanges pay rebates to resting liquidity; a maker's profit is spread plus "
                          r"rebate minus adverse selection, measured fill by fill", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "So how does any market maker survive? <bookmark mark='a'/> They cancel early: when the microprice or the "
            "imbalance turns against a quote, it is withdrawn. Our tiny order never cancels, and is picked off. "
            "<bookmark mark='b'/> They queue early, joining a level before it becomes the best, to hold a place near the "
            "front; the race for that place is Part thirty-five's latency arms race. <bookmark mark='c'/> And they are "
            "paid: rebates for resting liquidity. A maker's profit is spread plus rebate minus adverse selection, "
            "measured fill by fill. Part thirty-eight builds one."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a resting bid is filled the moment the offer queue has just refilled and the bid queue is nearly "
                       r"empty. Would the microprice have warned you, and which way?")
        with self.voiceover(
            "Pause and predict. A resting bid is filled just as the offer queue has refilled and the bid queue is "
            "almost empty. Would the microprice have warned you, and which way was it leaning?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
