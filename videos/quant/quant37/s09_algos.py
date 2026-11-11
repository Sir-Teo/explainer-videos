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
        self.closing()
        self.routing()
        self.crypto()
        self.pretrade()
        self.tca()
        self.example()
        self.benchmarks()
        self.question()

    def answer(self, v):
        sh = v["hourly_share"]
        a, b = 1000 * sh[14], 1000 * sh[4]
        rows = [cmath(r"14\text{:}00\text{--}15\text{:}00", r":", rf"1{{,}}000 \times {sh[14]:.3f} = {a:.0f}\ \text{{BTC}}",
                      font_size=36, colors={rf"{a:.0f}\ \text{{BTC}}": TWAP_C}),
                cmath(r"04\text{:}00\text{--}05\text{:}00", r":", rf"1{{,}}000 \times {sh[4]:.3f} = {b:.0f}\ \text{{BTC}}",
                      font_size=36),
                cmath(r"\text{planned share}", r"\ne", r"\text{guaranteed realised share}", font_size=38)]
        whys = [why(r"a VWAP schedule trades in proportion to the market's expected volume"),
                why(r"three times less in the quiet hour"),
                why('forecast errors change actual participation; expected-volume scheduling is not adaptive POV')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""For the original empirical volume-curve example, a thousand-bitcoin plan allocates {a:.0f} bitcoin to the fourteen-to-fifteen UTC hour and {b:.0f} to the four-to-five UTC hour. <bookmark mark='a'/> The chosen-volume pause uses a seven-point-five-percent hour, giving seventy-five bitcoin. <bookmark mark='b'/> A VWAP plan follows expected volume. <bookmark mark='c'/> Realized participation changes when the forecast or total volume changes; following a forecast does not guarantee constant realized share."""
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
        self.add(cards[0])
        with self.voiceover(
            f"Two more calendars. <bookmark mark='a'/> The week: weekend minutes trade about {100 * we / wk:.0f} "
            "percent of the volume of weekday ones. <bookmark mark='b'/> So a VWAP algorithm is only as good as its "
            "volume forecast. <bookmark mark='c'/> And events, index rebalances, expiries and data releases, bend the "
            "curve; in American stocks the closing auction alone can hold a tenth of the day's volume."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def pov(self):
        rows = [cmath(r"I", r"\approx", r"Y\sigma\sqrt{Q/V}", font_size=40, colors={r"I": IMPACT_C}),
                cmath(r"v=\pi\,\dot V", r",", r"T=Q/(\pi\dot V)", font_size=34),
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
            "Participation and duration. <bookmark mark='a'/> A size-only terminal-impact formula holds its prediction fixed as duration changes, because duration is absent by assumption. <bookmark mark='b'/> For constant market volume rate V-dot, trading at share pi gives rate pi V-dot and completion time Q over pi V-dot. A daily total volume must first be converted to a rate. <bookmark mark='c'/> Actual participation changes may affect impact, adverse selection and information leakage. <bookmark mark='d'/> In a diffusive constant-rate illustration, timing-risk scale grows with root T. These modeling assumptions explain the comparison; the size-only formula alone does not establish that slower execution is equally costly."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def closing(self):
        cards = VGroup(
            desk_question(r"the closing auction", r"one price at the close, set by matching all market-on-close and "
                          r"limit-on-close orders; index funds rebalance there, so a large share of some days' volume "
                          r"trades in one instant", width=12.4, font_size=19),
            desk_question(r"imbalance messages", r"exchanges publish the auction's imbalance before the close, and "
                          r"liquidity providers trade against it; the impact of a closing order shows up in that "
                          r"response", width=12.4, font_size=19),
            desk_question(r"no close in crypto", r"Bitcoin has no auction; its benchmarks are reference rates computed "
                          r"from several venues over a window, which an executor can track like a short VWAP",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "The close. <bookmark mark='a'/> Stock exchanges end the day with an auction, one price for every "
            "market-on-close and limit-on-close order; index funds rebalance there. <bookmark mark='b'/> The exchanges "
            "publish the auction's imbalance beforehand, and liquidity providers trade against it. "
            "<bookmark mark='c'/> Crypto has no close: its benchmarks are reference rates computed from several venues "
            "over a window, which an executor tracks like a short VWAP."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
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
        self.add(cards[0])
        with self.voiceover(
            "Beneath the schedule. <bookmark mark='a'/> A smart order router splits each child order across venues, by "
            "displayed size, fees, fill probability and the risk of being picked off. <bookmark mark='b'/> Each child "
            "chooses to rest, cheaper but slower and adversely selected, as Part thirty-six measured, or to cross and "
            "pay the spread. <bookmark mark='c'/> And dark pools hide the order, which helps only if the pool's other "
            "users are not reading it."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def crypto(self):
        cards = VGroup(
            desk_question(r"no consolidated quote", r"Bitcoin trades on dozens of exchanges with no national best bid "
                          r"and offer and no order-protection rule; routing between them is the trader's own problem",
                          width=12.4, font_size=19),
            desk_question(r"spot and perpetual", r"the same exposure trades as spot and as perpetual futures (Part 35's "
                          r"price discovery); an executor can split across both, paying the basis and funding",
                          width=12.4, font_size=19),
            desk_question(r"counterparty and custody", r"each venue holds the trader's collateral; Part 39 meets the cost "
                          r"of that when an exchange fails", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "And in crypto. <bookmark mark='a'/> There is no consolidated quote and no order-protection rule: Bitcoin "
            "trades on dozens of exchanges, and routing among them is the trader's own problem. <bookmark mark='b'/> "
            "The same exposure trades as spot and as perpetual futures, and an executor can split across both, paying "
            "the basis and the funding. <bookmark mark='c'/> And every venue holds collateral, a counterparty risk that "
            "Part thirty-nine prices."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def pretrade(self):
        sig, v, q, spread_bp, fee_bp = 0.012, 30e9, 150e6, 0.3, 0.2
        part = q / v
        imp = 1e4 * sig * part ** 0.5
        tot = spread_bp / 2 + imp + fee_bp
        rows = [cmath(r"Q/V", r"=", rf"\frac{{150\text{{m}}}}{{30\text{{bn}}}} = {100 * part:.1f}\%", font_size=36),
                cmath(r"\text{impact}", r"\approx", rf"1.2\% \times \sqrt{{{part:.3f}}} = {imp:.1f}\ \text{{bp}}", font_size=36,
                      colors={r"\text{impact}": IMPACT_C}),
                cmath(r"\text{total}", r"\approx", rf"\tfrac12 (0.3) + {imp:.1f} + 0.2 = {tot:.1f}\ \text{{bp}}", font_size=36,
                      colors={r"\text{total}": HURDLE})]
        whys = [why(r"an illustration: buying \$150 million of a broad equity fund that trades \$30 billion a day"),
                why('chosen average-impact coefficient $Y=1$ and daily return volatility 1.2\\%'),
                why(r"half a 0.3-bp spread and 0.2 bp of fees: the impact is nearly all of the cost")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""An illustrative average-cost estimate. <bookmark mark='a'/> A hundred and fifty million dollars is half a percent of thirty billion dollars of daily volume. <bookmark mark='b'/> Choose an average-impact coefficient of one and daily return volatility 1.2 percent; the impact estimate is {imp:.1f} basis points. <bookmark mark='c'/> Half a point-three basis-point spread and point-two basis-point fees give {tot:.1f} basis points total. This coefficient is explicitly for average shortfall, rather than a terminal peak. The figures are chosen inputs and omit estimation uncertainty and rate dependence."""
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

    def tca(self):
        rows = [cmath(r"\text{arrival}", r":", r"p_{\text{decision}}\ \text{or}\ p_{\text{first fill}}", font_size=36),
                cmath(r"\text{IS}", r"=", r"\text{delay} + \text{impact} + \text{timing} + \text{opportunity} + \text{fees}",
                      font_size=30, colors={r"\text{IS}": IMPACT_C}),
                cmath(r"\text{markouts}", r":", r"p_{t + h} - p_{\text{fill}}\ \text{after each fill}", font_size=34),
                cmath(r"\text{model}", r":", r"\text{predicted cost} \pm \text{its error}", font_size=36)]
        whys = [why('fix decision/arrival timestamp and price source beforehand; first fill is endogenous'),
                why(r"Chapter 1's decomposition, reported for every parent order"),
                why(r"Part 36's markouts, applied to the execution: did the price keep running after the fills?"),
                why(r"a pre-trade estimate from the square root or a propagator, and the realised cost judged against "
                    r"the noise, which for a single order is enormous")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Transaction-cost analysis. <bookmark mark='a'/> Fix decision and arrival timestamps and price sources in advance. The first fill is endogenous to an executor's choices and is not an immune benchmark. <bookmark mark='b'/> Report signed shortfall, fees and the convention for unfilled shares. Accounting decompositions do not separately identify news and mechanical impact. <bookmark mark='c'/> Use signed fill markouts with the same spread and fee convention. <bookmark mark='d'/> Compare costs across suitable orders with model uncertainty, dependence and selection in view. A large sample does not automatically remove systematic bias."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def example(self):
        dec, arr, avg, end = 100.00, 100.05, 100.30, 100.60
        q_f, q_t = 90_000, 100_000
        delay = (arr - dec) * q_f
        impact = (avg - arr) * q_f
        opp = (end - dec) * (q_t - q_f)
        total = delay + impact + opp
        bp = 1e4 * total / (dec * q_t)
        rows = [cmath(r"\text{delay}", r"=", rf"(100.05 - 100.00) \times 90{{,}}000 = \${delay:,.0f}".replace(",", "{,}"),
                      font_size=32),
                cmath(r"\text{execution}", r"=", rf"(100.30 - 100.05) \times 90{{,}}000 = \${impact:,.0f}".replace(",", "{,}"),
                      font_size=32, colors={r"\text{execution}": IMPACT_C}),
                cmath(r"\text{opportunity}", r"=", rf"(100.60 - 100.00) \times 10{{,}}000 = \${opp:,.0f}".replace(",", "{,}"),
                      font_size=32),
                cmath(r"\text{IS}", r"=", rf"\${total:,.0f} = {bp:.1f}\ \text{{bp}}".replace(",", "{,}"), font_size=36,
                      colors={r"\text{IS}": HURDLE})]
        whys = [why(r"a buy of 100,000 shares decided at \$100.00; the algorithm starts at \$100.05"),
                why(r"90,000 filled at an average \$100.30: crossing, impact and timing together"),
                why(r"10,000 never filled, and the price ended at \$100.60: the cost of what was missed"),
                why(r"the shortfall against the paper portfolio, in dollars and in basis points of the order")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A worked example. A buy of a hundred thousand shares is decided at a hundred dollars. "
            "<bookmark mark='a'/> The algorithm starts five cents higher: delay. <bookmark mark='b'/> Ninety thousand "
            "shares are filled at an average of a hundred dollars thirty: the execution cost, spread, impact and timing "
            "together. <bookmark mark='c'/> Ten thousand are never filled, and the price ends at a hundred dollars sixty: "
            f"the opportunity cost. <bookmark mark='d'/> In all, {bp:.0f} basis points of the order. Notice that the "
            "unfilled tenth cost more than the delay."
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
        self.add(cards[0])
        with self.voiceover(
            "And a warning about benchmarks. <bookmark mark='a'/> VWAP can be gamed: a large order moves the VWAP itself, "
            "so beating it can mean only that the order was big. <bookmark mark='b'/> A closing-price benchmark invites "
            "trading at the close, where the order helps set the price. <bookmark mark='c'/> And a broker judged against "
            "VWAP will trade VWAP even when the client's alpha decays fast. The benchmark should match the urgency."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        head = label('9. Participation and risk', font_size=30, color=QC.IDEA).to_edge(UP, buff=0.45)
        given = wrapped_label('$Q=0.02V_{day}$, constant market volume rate; compare participation $5\\%$ and $20\\%$.', 12.0, 29).move_to(UP * 0.65)
        task = wrapped_label('Find completion times in days and the ratio of diffusive timing-risk scales.', 12.0, 27, QC.IDEA).move_to(DOWN * 1.3)
        foot = note("Pause: work the units and assumptions; full solution in the notes.", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover('Quantitative pause nine. The parent quantity is two percent of daily volume and the market volume rate is constant. Compare five-percent with twenty-percent participation. Compute the completion times in days and the ratio of square-root-time risk scales. State the size-only impact assumption separately.'):
            self.play(FadeIn(head), FadeIn(given), FadeIn(task), FadeIn(foot))
        self.wait(6)
        self.clear_scene()
