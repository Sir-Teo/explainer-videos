from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant35.common import BAD, FLOW_C, GOOD, HURDLE, INF_C, PART, PRICE_C, fit_right, load


class VPIN(VoiceoverScene):
    def construct(self):
        v = load("vpin")
        self.card()
        self.pin()
        self.vpin_def()
        self.pin_trouble()
        self.series(v)
        self.events(v)
        self.critique(v)
        self.markouts()
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(6, r"Toxic flow: PIN and VPIN", r"Can the share of informed trading be measured, live?", part=PART)
        with self.voiceover("Chapter six. Glosten and Milgrom's mu, the share of informed traders, sets the spread. If it "
                            "could be measured, a market maker would know when to widen its quotes. Two famous attempts, "
                            "and a test of the second."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pin(self):
        rows = [cmath(r"\text{day}", r":", r"\text{news with probability } \alpha;\ \text{good or bad}", font_size=32),
                cmath(r"\text{arrivals}", r":", r"\text{noise } \varepsilon_b, \varepsilon_s;\ \text{informed } \mu "
                      r"\text{ on the news side}", font_size=30),
                cmath(r"\text{PIN}", r"=", r"\frac{\alpha\mu}{\alpha\mu + \varepsilon_b + \varepsilon_s}", font_size=38,
                      colors={r"\text{PIN}": INF_C})]
        whys = [why(r"Easley, Kiefer, O'Hara and Paperman (1996): each day there is private news or not"),
                why(r"buys and sells arrive as Poisson processes; informed traders add to one side on news days"),
                why(r"the probability that a trade is informed, estimated by maximum likelihood from daily counts of buys and "
                    r"sells")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "PIN. <bookmark mark='a'/> David Easley, Nicholas Kiefer, Maureen O'Hara and Joseph Paperman: each day there "
            "is private news, or not. <bookmark mark='b'/> Buys and sells arrive at random, and on news days informed "
            "traders add to one side. <bookmark mark='c'/> The probability that a trade is informed is estimated from "
            "daily counts of buys and sells, by maximum likelihood. It became a standard variable in asset pricing, "
            "and a slow one: it needs many days of data."
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

    def vpin_def(self):
        rows = [cmath(r"V_\tau^B", r"=", r"\textstyle\sum_{i \in \tau} V_i\,\Phi\big(\Delta p_i/\sigma_{\Delta p}\big)",
                      font_size=34, colors={r"V_\tau^B": GOOD}),
                cmath(r"\text{VPIN}", r"=", r"\frac{1}{n}\textstyle\sum_{\tau} \frac{|V_\tau^B - V_\tau^S|}{V}",
                      font_size=36, colors={r"\text{VPIN}": INF_C}),
                cmath(r"V", r"=", r"\tfrac{1}{50}\ \text{of a day's volume};\ n = 50", font_size=32)]
        whys = [why(r"bulk volume classification: each bar's volume is split into buys and sells by how far its price "
                    r"moved, with no trade-by-trade signs needed"),
                why(r"Easley, Lopez de Prado and O'Hara (2012): the average order imbalance over the last $n$ volume "
                    r"buckets, a live PIN in volume time"),
                why(r"buckets of equal volume, not equal time, so a busy hour counts more")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "VPIN, its fast successor. <bookmark mark='a'/> Bulk volume classification: split each bar's volume into "
            "buys and sells by how far its price moved, without signing a single trade. <bookmark mark='b'/> David "
            "Easley, Marcos Lopez de Prado and Maureen O'Hara average the order imbalance over the last fifty buckets "
            "of volume. <bookmark mark='c'/> Each bucket is a fiftieth of a day's volume, so the clock runs in volume, "
            "not time. They argued it rose before the flash crash of 2010."
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

    def pin_trouble(self):
        cards = VGroup(
            desk_question(r"hard to estimate", r"PIN's likelihood has many local maxima and overflows for active stocks; "
                          r"estimates depend on the optimiser's starting point", width=12.4, font_size=19),
            desk_question(r"why is it priced?", r"Duarte and Young (2009) found that the part of PIN that predicts returns "
                          r"is the part related to illiquidity, not to asymmetric information", width=12.4, font_size=19),
            desk_question(r"order flow without signs", r"both need buys and sells: PIN from a trade classifier, VPIN from "
                          r"price moves; the classifier is the weak link", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "PIN has its own troubles. <bookmark mark='a'/> Its likelihood has many local maxima, and estimates depend on "
            "where the optimiser starts. <bookmark mark='b'/> Jefferson Duarte and Lance Young found that the part of PIN "
            "that predicts stock returns is the part related to illiquidity, not to private information. "
            "<bookmark mark='c'/> And both measures need to know which trades were buys: PIN from a trade classifier, VPIN "
            "from price moves. The classifier is the weak link, which is the test that follows."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def series(self, v):
        t = np.asarray(v["t"], float)
        y = np.asarray(v["vpin"], float)
        ok = np.isfinite(y)
        yr = 1970 + t / (365.25 * 86400)
        g = axes([2021, 2025], [0, 0.6], x_length=8.0, y_length=4.2, xlabel=r"BTCUSDT, 2021--2024",
                 ylabel=r"VPIN", xticks=[2021, 2022, 2023, 2024, 2025], yticks=[0, 0.3, 0.6], xfmt=lambda u: f"{u:.0f}",
                 font_size=15).move_to(LEFT * 0.8 + DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, yr[ok], np.clip(y[ok], 0, 0.6), INF_C, stroke_width=1.5)
        with self.voiceover(
            "VPIN on four years of Bitcoin, one-minute bars. <bookmark mark='a'/> It averages about "
            f"{v['mean']:.2f}, with spikes. The question is what the spikes mean."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(c1), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def events(self, v):
        ev = v["events"]
        panels = VGroup()
        for k, (name, e) in enumerate(ev.items()):
            g = axes([-7, 7], [0, 0.6], x_length=5.6, y_length=3.0, xlabel=rf"days from {name}", ylabel=r"VPIN",
                     xticks=[-7, 0, 7], yticks=[0, 0.6], font_size=13)
            ax = g.ax
            vt = np.asarray(e["t"], float)
            vy = np.asarray(e["vpin"], float)
            ok = np.isfinite(vy)
            c1 = curve(ax, vt[ok], np.clip(vy[ok], 0, 0.6), INF_C, stroke_width=2)
            pt = np.asarray(e["pt"], float)
            pp = np.asarray(e["price"], float)
            pn = 0.6 * (pp - pp.min()) / (pp.max() - pp.min())
            c2 = curve(ax, pt, pn, PRICE_C, stroke_width=1.5)
            zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 0.6), color=BAD, stroke_width=1.5)
            panels.add(VGroup(g, c1, c2, zero))
        panels.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.2)
        leg = legend([(INF_C, r"VPIN"), (PRICE_C, r"price, rescaled")], font_size=16).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Two crashes. <bookmark mark='a'/> The nineteenth of May 2021, when Bitcoin fell by about a third within the "
            "day. <bookmark mark='b'/> And the eighth of November 2022, as the exchange FTX collapsed. In both, VPIN "
            "jumps with the crash itself, not clearly before it. A warning that arrives with the loss is not a warning."
        ) as vo:
            self.play(FadeIn(leg))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
        self.wait(0.4)
        self.clear_scene()

    def critique(self, v):
        rows = [cmath(r"\operatorname{corr}(\text{VPIN}, \text{volatility})", r"=", rf"{v['corr_rv']:.2f}", font_size=34,
                      colors={r"\operatorname{corr}(\text{VPIN}, \text{volatility})": BAD}),
                cmath(r"\operatorname{corr}(\text{VPIN}, \text{true imbalance})", r"=", rf"{v['corr_true']:.2f}",
                      font_size=34, colors={r"\operatorname{corr}(\text{VPIN}, \text{true imbalance})": BAD}),
                cmath(r"\Phi(\Delta p/\sigma)", r":", r"\text{large moves} \Rightarrow \text{large measured imbalance}",
                      font_size=32)]
        whys = [why(r"over the same windows: VPIN moves with realised volatility"),
                why(r"and hardly at all with the actual aggressive buy-sell imbalance, which Binance records directly"),
                why(r"bulk classification assigns a big price move to one side by construction; Andersen and Bondarenko "
                    r"(2014) made this critique of VPIN and the flash crash")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Bitcoin allows a test that equities did not. <bookmark mark='a'/> Over the same windows, VPIN's correlation "
            f"with realised volatility is {v['corr_rv']:.2f}. <bookmark mark='b'/> Its correlation with the true "
            "aggressive imbalance, which Binance records directly, is "
            f"{v['corr_true']:.2f}. <bookmark mark='c'/> Bulk classification assigns a large price move to one side by "
            "construction, so VPIN is largely a volatility gauge. Torben Andersen and Oleg Bondarenko made exactly this "
            "critique in 2014; here the true flow confirms it."
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

    def markouts(self):
        rows = [cmath(r"\text{markout}(\Delta)", r"=", r"q\,(m_{t+\Delta} - p_t)", font_size=36, colors={r"\text{markout}(\Delta)": FLOW_C}),
                cmath(r"\Delta", r"\in", r"\{1\,\text{s},\ 10\,\text{s},\ 1\,\text{min},\ 5\,\text{min}\}", font_size=34),
                cmath(r"\text{toxic flow}", r":", r"\text{markouts that keep falling after the fill}", font_size=32,
                      colors={r"\text{toxic flow}": BAD})]
        whys = [why(r"what market makers actually use: the move of the midpoint after each of their fills, signed by the "
                    r"counterparty's side"),
                why(r"measured at several horizons, by counterparty, venue and time of day"),
                why(r"uninformed flow's markouts recover; informed flow's keep going against the dealer: Glosten and Milgrom, "
                    r"read from one's own fills")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "What market makers use instead. <bookmark mark='a'/> Markouts: after each of their own fills, how far the "
            "midpoint moved against them. <bookmark mark='b'/> Measured at a second, ten seconds, a minute, five minutes, "
            "and by counterparty, venue and hour. <bookmark mark='c'/> Uninformed flow's markouts recover; informed "
            "flow's keep moving against the dealer. It is Glosten and Milgrom read directly from one's own trades, and it "
            "needs no classifier at all."
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

    def lessons(self):
        cards = VGroup(
            desk_question(r"a measure inherits its classifier", r"a toxicity measure built on price moves will rise when "
                          r"prices move, whatever the flow", width=12.4, font_size=19),
            desk_question(r"use signed flow where it exists", r"Chapter 5's taker flow is the imbalance itself; VPIN "
                          r"estimates it when it is missing, and estimates it poorly", width=12.4, font_size=19),
            desk_question(r"volatility is still useful", r"a market maker widening its quotes when volatility rises is "
                          r"doing the right thing, for the inventory reason of Chapter 1", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The lessons. <bookmark mark='a'/> A measure inherits its classifier: one built on price moves rises when "
            "prices move. <bookmark mark='b'/> Where the signed flow exists, use it. <bookmark mark='c'/> And a dealer "
            "that widens its quotes when volatility rises is still right, for Chapter one's inventory reason, even if "
            "the gauge is not measuring information."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a bar's price rises by two standard deviations on 1{,}000 BTC of volume. How does bulk "
                       r"classification split it, and what if the true taker split was even?")
        with self.voiceover(
            "Pause and predict. A bar's price rises by two standard deviations on a thousand bitcoin of volume. How does "
            "bulk classification split it into buys and sells, and what if the true split was even?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
