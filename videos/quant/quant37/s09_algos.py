from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant37.common import (BAD, HURDLE, IMPACT_C, PART, SCHED_C, TWAP_C, load)


class Algos(VoiceoverScene):
    def construct(self):
        v = load("volume")
        self.answer(v)
        self.card()
        self.menu()
        self.curve_(v)
        self.week(v)
        self.pov()
        self.routing()
        self.tca()
        self.benchmarks()
        self.question()

    def answer(self, v):
        sh = v["hourly_share"]
        a, b = 1000 * sh[14], 1000 * sh[4]
        rows = [cmath(r"14\text{:}00\text{--}15\text{:}00", r":", rf"1{{,}}000 \times {sh[14]:.3f} = {a:.0f}\ \text{{BTC}}",
                      font_size=36, colors={rf"{a:.0f}\ \text{{BTC}}": TWAP_C}),
                cmath(r"04\text{:}00\text{--}05\text{:}00", r":", rf"1{{,}}000 \times {sh[4]:.3f} = {b:.0f}\ \text{{BTC}}",
                      font_size=36),
                cmath(r"\text{participation}", r"\approx", r"\text{constant}", font_size=38)]
        whys = [why(r"a VWAP schedule trades in proportion to the market's expected volume"),
                why(r"three times less in the quiet hour"),
                why(r"so the order is the same share of the market all day, the quantity that sets impact")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"The answer to the pause. <bookmark mark='a'/> In the busy hour, about {a:.0f} bitcoin. "
            f"<bookmark mark='b'/> In the quiet hour, about {b:.0f}. <bookmark mark='c'/> A VWAP schedule trades in "
            "proportion to the market's expected volume, so the order is the same share of the market all day: the "
            "quantity that sets its impact."
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

    def card(self):
        c = chapter_card(8, r"The algorithms, and the bill", r"What do brokers' execution algorithms do, and how is the "
                         r"result judged?", part=PART)
        with self.voiceover("Chapter eight. The theory becomes products: a handful of execution algorithms that every "
                            "broker sells, the routers beneath them, and transaction-cost analysis, which tells the "
                            "client what it all cost."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def menu(self):
        rows = [cmath(r"\text{TWAP}", r":", r"\text{equal slices in time}", font_size=36, colors={r"\text{TWAP}": TWAP_C}),
                cmath(r"\text{VWAP}", r":", r"\text{slices in proportion to expected volume}", font_size=34),
                cmath(r"\text{POV}", r":", r"\text{a fixed share of realised volume}", font_size=36),
                cmath(r"\text{IS}", r":", r"\text{Almgren--Chriss: front-loaded, by urgency}", font_size=34,
                      colors={r"\text{IS}": SCHED_C})]
        whys = [why(r"risk-neutral, linear impact, no information: Bertsimas and Lo's answer"),
                why(r"tracks the day's volume curve, so it tracks the VWAP benchmark; Konishi (2002) and Humphery-Jenner "
                    r"(2011) on the optimal slicing"),
                why(r"percentage of volume: follows the market as it happens, so its end time is uncertain"),
                why(r"implementation shortfall, or arrival price: trades faster when risk matters more")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The menu. <bookmark mark='a'/> TWAP: equal slices in time, Bertsimas and Lo's answer for a risk-neutral "
            "trader. <bookmark mark='b'/> VWAP: slices in proportion to the volume expected at each time of day, so it "
            "tracks the volume-weighted price. <bookmark mark='c'/> POV: a fixed share of the volume actually traded, "
            "so the end time is uncertain. <bookmark mark='d'/> And IS, implementation shortfall: Almgren and Chriss's "
            "front-loaded schedule, set by an urgency."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def curve_(self, v):
        sh = 100 * np.asarray(v["hourly_share"], float)
        top = float(np.ceil(sh.max()) + 1)
        g = axes([-0.5, 23.5], [0, top], x_length=8.8, y_length=4.0, xlabel=r"hour, UTC",
                 ylabel=r"share of daily volume, \%", xticks=[0, 6, 12, 18, 23], yticks=[0, top / 2, top],
                 yfmt=lambda x: f"{x:.0f}", font_size=15).move_to(DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.28, height=max(1e-3, abs(ax.c2p(0, x)[1] - ax.c2p(0, 0)[1])),
                                  fill_color=TWAP_C if i not in (13, 14, 15) else HURDLE, fill_opacity=0.85,
                                  stroke_width=0).move_to(ax.c2p(i, x / 2)) for i, x in enumerate(sh)])
        flat = DashedLine(ax.c2p(-0.5, 100 / 24), ax.c2p(23.5, 100 / 24), color=GREY_B, stroke_width=1.5)
        k = int(np.argmax(sh))
        j = int(np.argmin(sh))
        with self.voiceover(
            "Bitcoin's volume curve, from every minute of twenty twenty-three on the perpetual. <bookmark mark='a'/> "
            f"Crypto never closes, but it has a day: a trough of {sh[j]:.1f} percent of the volume in the hour from "
            f"{j}:00, and a peak of {sh[k]:.1f} percent from {k}:00, when New York opens and American data come out. "
            "<bookmark mark='b'/> TWAP is the dashed line, the same in every hour. VWAP follows the bars."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in bars], lag_ratio=0.04))
            vo.wait_until("b")
            self.play(Create(flat))
        self.wait(0.4)
        self.clear_scene()

    def week(self, v):
        d = np.asarray(v["by_dow"], float)
        wk = float(np.mean(d[:5]))
        we = float(np.mean(d[5:]))
        cards = VGroup(
            desk_question(r"the week", rf"weekend minutes trade about {100 * we / wk:.0f}\% of the volume of weekday "
                          r"ones: a schedule that ignores the calendar trades a larger share of a thinner market",
                          width=12.4, font_size=19),
            desk_question(r"the forecast is the product", r"a VWAP algorithm is only as good as its volume forecast; "
                          r"errors in the curve become tracking error against the benchmark", width=12.4, font_size=19),
            desk_question(r"events", r"index rebalances, option expiries and macro releases bend the curve; the closing "
                          r"auction alone can hold a tenth of a stock's daily volume", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            f"Two more calendars. <bookmark mark='a'/> The week: weekend minutes trade about {100 * we / wk:.0f} "
            "percent of the volume of weekday ones. <bookmark mark='b'/> So a VWAP algorithm is only as good as its "
            "volume forecast. <bookmark mark='c'/> And events, index rebalances, expiries and data releases, bend the "
            "curve; in American stocks the closing auction alone can hold a tenth of the day's volume."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def pov(self):
        rows = [cmath(r"I", r"\approx", r"Y\sigma\sqrt{Q/V}", font_size=40, colors={r"I": IMPACT_C}),
                cmath(r"\text{rate}", r"=", r"\pi\ \text{(participation)},\quad T = Q/(\pi V)", font_size=34),
                cmath(r"\text{cost}", r"\approx", r"\text{independent of } \pi\ \text{(to first order)}", font_size=34),
                cmath(r"\text{risk}", r"\propto", r"\sigma\sqrt{T} \propto 1/\sqrt\pi", font_size=36,
                      colors={r"\text{risk}": BAD})]
        whys = [why(r"the square-root law, with no dependence on the duration"),
                why(r"a POV order at participation $\pi$ takes a time set by its size and the market's volume"),
                why(r"so trading slower does not lower the expected impact much, a striking consequence of the law; "
                    r"finer studies find a weak dependence on the rate"),
                why(r"but it does raise the risk; under the square root, patience is mostly risk, not savings")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The square-root law has a striking consequence for participation. <bookmark mark='a'/> The impact depends "
            "on the size, not on the duration. <bookmark mark='b'/> A POV order at participation pi takes a time set by "
            "its size. <bookmark mark='c'/> So trading more slowly barely lowers the expected impact; finer studies "
            "find a weak dependence on the rate. <bookmark mark='d'/> But it raises the risk. Under the square root, "
            "patience buys mostly risk, not savings, which is why urgency is a real choice."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def routing(self):
        cards = VGroup(
            desk_question(r"the router", r"beneath each algorithm, a smart order router splits child orders across "
                          r"venues by displayed size, fees, fill probability and the chance of being picked off",
                          width=12.4, font_size=19),
            desk_question(r"limit or market", r"each child order chooses between resting (cheaper, slower, adversely "
                          r"selected: Part 36) and crossing (certain, pays the spread)", width=12.4, font_size=19),
            desk_question(r"dark pools and information", r"routing to dark pools hides the order but leaks less "
                          r"information only if the pool's other users are not reading it (Part 35)", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Beneath the schedule. <bookmark mark='a'/> A smart order router splits each child order across venues, by "
            "displayed size, fees, fill probability and the risk of being picked off. <bookmark mark='b'/> Each child "
            "chooses to rest, cheaper but slower and adversely selected, as Part thirty-six measured, or to cross and "
            "pay the spread. <bookmark mark='c'/> And dark pools hide the order, which helps only if the pool's other "
            "users are not reading it."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def tca(self):
        rows = [cmath(r"\text{arrival}", r":", r"p_{\text{decision}}\ \text{or}\ p_{\text{first fill}}", font_size=36),
                cmath(r"\text{IS}", r"=", r"\text{delay} + \text{impact} + \text{timing} + \text{opportunity} + \text{fees}",
                      font_size=30, colors={r"\text{IS}": IMPACT_C}),
                cmath(r"\text{markouts}", r":", r"p_{t + h} - p_{\text{fill}}\ \text{after each fill}", font_size=34),
                cmath(r"\text{model}", r":", r"\text{predicted cost} \pm \text{its error}", font_size=36)]
        whys = [why(r"the benchmark that cannot be gamed by the executor: where the price was when the order began"),
                why(r"Chapter 1's decomposition, reported for every parent order"),
                why(r"Part 36's markouts, applied to the execution: did the price keep running after the fills?"),
                why(r"a pre-trade estimate from the square root or a propagator, and the realised cost judged against "
                    r"the noise, which for a single order is enormous")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Transaction-cost analysis. <bookmark mark='a'/> Start from the arrival price, the benchmark an executor "
            "cannot game. <bookmark mark='b'/> Decompose each parent order's shortfall as in Chapter one. "
            "<bookmark mark='c'/> Mark out the fills, as Part thirty-six did. <bookmark mark='d'/> And compare the "
            "realised cost with a pre-trade estimate, judged against the noise. For a single order that noise is "
            "enormous, as the Almgren and Chriss standard deviation showed: TCA is a statistics problem over many "
            "orders."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def benchmarks(self):
        cards = VGroup(
            desk_question(r"VWAP can be gamed", r"an order that is a large share of the day's volume moves the VWAP "
                          r"itself; beating VWAP can mean the order was simply big", width=12.4, font_size=19),
            desk_question(r"the close", r"a benchmark at the closing price invites trading at the close, where liquidity "
                          r"is deep but the price is set partly by the order", width=12.4, font_size=19),
            desk_question(r"incentives", r"a broker judged against VWAP will trade VWAP even when the client's alpha "
                          r"decays fast; the benchmark should match the portfolio's urgency", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And a warning about benchmarks. <bookmark mark='a'/> VWAP can be gamed: a large order moves the VWAP itself, "
            "so beating it can mean only that the order was big. <bookmark mark='b'/> A closing-price benchmark invites "
            "trading at the close, where the order helps set the price. <bookmark mark='c'/> And a broker judged against "
            "VWAP will trade VWAP even when the client's alpha decays fast. The benchmark should match the urgency."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the House's portfolio desk sends a 2\%-of-volume order with an alpha that decays in a day. The "
                       r"broker offers VWAP. What should the execution desk ask for instead?")
        with self.voiceover(
            "Pause and predict. The House's portfolio desk sends an order of two percent of a day's volume, on a signal "
            "whose alpha decays within a day. The broker offers VWAP. What should the execution desk ask for instead?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
