from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, DELTA, GOOD, IV, OPT, PART, SPOT, illustration, load, real_data, axes, data_range


class Digitals(VoiceoverScene):
    def construct(self):
        d = load("digital")
        self.card()
        self.digital(d)
        self.spread(d)
        self.hedge(load("digital_hedge"))
        self.onetouch(load("onetouch"))
        self.skew(load("digital_skew"))

    def card(self):
        c = chapter_card(5, r"Digitals, one-touches and the call-spread hedge", r"Which payoffs are easy to price and "
                         r"hard to hedge?", part=PART)
        with self.voiceover("Chapter five. Digitals, one-touches, and the call-spread hedge."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def digital(self, d):
        S = np.asarray(d["S"])
        g1 = axes([90, 110], [0, 1.05], x_length=5.6, y_length=3.4, xlabel=r"spot", ylabel=r"price of 1 if $S_T > 100$",
                  xticks=[90, 95, 100, 105, 110], yticks=[0, 0.5, 1.0], font_size=15)
        g2 = axes([90, 110], [0, 0.75], x_length=5.6, y_length=3.4, xlabel=r"spot", ylabel=r"delta",
                  xticks=[90, 95, 100, 105, 110], yticks=[0, 0.25, 0.5, 0.75], font_size=15)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).to_edge(UP, buff=1.0)
        cols = {"a month": GREY_B, "a day": IV, "an hour": BAD}
        L1 = VGroup(*[curve(g1.ax, S, np.asarray(c["price"]), cols[k], stroke_width=2.5) for k, c in d["curves"].items()])
        L2 = VGroup(*[curve(g2.ax, S, np.asarray(c["delta"]), cols[k], stroke_width=2.5)
                      for k, c in d["curves"].items()])
        leg = legend([(cols[k], rf"{k} to expiry") for k in d["curves"]], font_size=17)
        leg.arrange(RIGHT, buff=0.4).next_to(VGroup(g1, g2), DOWN, buff=0.3)
        mx = d["curves"]["an hour"]["max_delta"]
        foot = wrapped_label(rf"an hour before expiry, the digital's delta at the strike is {mx:.2f} units per unit of payout: "
                             r"for a payout of a million, hundreds of thousands of hedge units near the strike. Discrete rebalancing near expiry is "
                             r"difficult; continuous frictionless Black--Scholes replication remains possible", 11.5, 20, GREY_A).to_edge(DOWN, buff=0.7)
        src = illustration(r"cash-or-nothing call struck at 100, volatility 25\%")
        with self.voiceover(
            f"A cash digital pays one above the terminal strike and zero otherwise. Black-Scholes prices it by a discounted risk-neutral probability. A month out its price is smooth. <bookmark mark='a'/> As expiry approaches, the transition narrows and delta becomes concentrated near the strike. The sampled one-hour curve reaches {mx:.2f} units per payout unit. For a million-unit payout that is a large underlying position, sensitive to spot and time. At positive remaining time delta is still smooth; it does not literally jump to zero on any tick. Perfect continuous frictionless replication exists in this model. Finite rebalancing, costs and uncertain dynamics make the near-expiry hedge difficult in practice."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(src), Create(L1[0]), Create(L2[0]), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(L1[1]), Create(L2[1]), FadeIn(leg[1]), run_time=1.5)
            self.play(Create(L1[2]), Create(L2[2]), FadeIn(leg[2]), FadeIn(foot), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def spread(self, d):
        rows = d["spread"]
        tab = VGroup(VGroup(label(r"call spread width", font_size=22, color=GREY_A), label(r"price, 1 month", font_size=22, color=GREY_A),
                            label(r"largest delta, a day out", font_size=22, color=GREY_A)))
        tab.add(VGroup(label(r"the digital itself", font_size=24), MathTex(f"{d['digital_atm']:.3f}", font_size=28),
                       MathTex(f"{d['curves']['a day']['max_delta']:.3f}", font_size=28, color=BAD)))
        for r in rows:
            tab.add(VGroup(MathTex(rf"\varepsilon = {r['eps']:g}", font_size=28), MathTex(f"{r['price']:.3f}", font_size=28),
                           MathTex(f"{r['max_delta']:.3f}", font_size=28, color=GOOD)))
        xs = [-3.6, 0.6, 4.0]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.4 - 0.62 * i, 0])
        eq = MathTex(r"\text{digital} \le \frac{C(K - \varepsilon) - C(K)}{\varepsilon}", font_size=34, color=OPT)
        eq.to_edge(DOWN, buff=1.2)
        note_ = wrapped_label(r"a call spread held to expiry pays at least as much as the digital in "
                              r"every state, costs a little more, and has a delta capped at $1/\varepsilon$ per unit. The "
                              r"width is a trade between that extra cost and a hedge the desk can actually run",
                              11.0, 20, GREY_A).next_to(eq, DOWN, buff=0.25)
        with self.voiceover(
            "One alternative is a call spread: buy the K minus epsilon call, sell the K call, and divide by epsilon. <bookmark mark='a'/> Its terminal payoff dominates the cash digital in every state. If the options are held and settle as specified, that static dominance is model-independent. Dynamically delta-hedging the spread is a different strategy and still has risk. In the fixed-parameter, zero-rate and zero-dividend Black-Scholes case here, its delta is bounded by one over epsilon. The table compares one-month prices with maximum deltas one day before expiry. A wider spread buys more payoff excess and a lower peak delta. The extra price is a cost of that payoff cushion, not a guarantee against hedging losses."
        ) as vo:
            self.play(FadeIn(tab[:2]), FadeIn(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.3), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def hedge(self, h):
        rows = h["rows"]
        show = h["show"]
        n = len(show["digital"]["ledger"])
        days = np.arange(n)
        S = np.array([x["S"] for x in show["digital"]["ledger"]])
        dd = np.array([x["delta"] for x in show["digital"]["ledger"]])
        ds = np.array([x["delta"] for x in show["spread"]["ledger"]])
        g1 = axes([0, n], [90, 110], x_length=5.4, y_length=2.4, ylabel=r"spot", xticks=[], yticks=[95, 100, 105],
                  font_size=14)
        top = max(float(dd.max()), float(ds.max()), 0.1) * 1.15
        g2 = axes([0, n], [0, top], x_length=5.4, y_length=2.6, xlabel=r"trading day", ylabel=r"hedge (units)",
                  xticks=[0, 7, 14, 21], yticks=[0, round(top / 2, 2)], font_size=14)
        L = VGroup(g1, g2).arrange(DOWN, buff=0.3).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        k = DashedLine(g1.ax.c2p(0, h["K"]), g1.ax.c2p(n, h["K"]), stroke_color=GREY_C, stroke_width=1.5)
        tr = ValueTracker(0)
        pS = tracing(g1.ax, days, S, tr, SPOT, stroke_width=2.5)
        pd = tracing(g2.ax, days, dd, tr, BAD, stroke_width=3)
        ps = tracing(g2.ax, days, ds, tr, GOOD, stroke_width=3)
        leg = legend([(BAD, r"short digital: its hedge"), (GOOD, r"short call spread, width 2: its hedge")],
                     font_size=16).next_to(L, UP, buff=0.15).align_to(L, LEFT)
        hd = {r["n"]: r for r in rows["digital"]}
        hs = {r["n"]: r for r in rows["spread"]}
        tab = VGroup(VGroup(label(r"rebalances", font_size=19, color=GREY_A), label(r"digital: s.d.", font_size=19, color=BAD),
                            label(r"1\% tail", font_size=19, color=BAD), label(r"spread: s.d.", font_size=19, color=GOOD),
                            label(r"1\% tail", font_size=19, color=GOOD)))
        for m in (21, 84, 336):
            tab.add(VGroup(MathTex(str(m), font_size=26), MathTex(f"{hd[m]['sd']:.3f}", font_size=26),
                           MathTex(f"{hd[m]['q01']:+.2f}", font_size=26), MathTex(f"{hs[m]['sd']:.3f}", font_size=26),
                           MathTex(f"{hs[m]['q01']:+.2f}", font_size=26)))
        xs = [0.9, 2.3, 3.4, 4.7, 5.8]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.0 - 0.55 * i, 0])
        r_d = hd[21]["sd"] / hd[336]["sd"]
        r_s = hs[21]["sd"] / hs[336]["sd"]
        faster = r_s > r_d
        note_ = wrapped_label(rf"hedging P\&L per unit of payout, 40{{,}}000 paths; prices: digital {hd[21]['price']:.3f}, "
                              rf"spread {hs[21]['price']:.3f}. Rebalancing 16 times as often cuts the digital's error "
                              rf"{r_d:.1f}-fold and the spread's {r_s:.1f}-fold", 5.6, 18, GREY_A)
        note_.next_to(tab, DOWN, buff=0.35).align_to(tab, LEFT)
        verdict = (f"the spread's error falls {r_s:.1f}-fold, the digital's only {r_d:.1f}-fold. The extra "
                   f"{hs[21]['price'] - hd[21]['price']:.3f} the spread costs buys a payoff cushion; these simulated discrete hedges still have losses."
                   if faster else
                   f"both errors fall at a similar rate, {r_d:.1f}-fold and {r_s:.1f}-fold; the spread's advantage is its "
                   "smaller error at every frequency.")
        src = illustration(r"one month, struck at 100, 25\% volatility; delta-hedged in the underlying, no costs",
                           corner=UR)
        with self.voiceover(
            "Hedge both books on one path, a month to expiry, rebalanced daily. <bookmark mark='a'/> In red, the hedge for a short digital; in green, the "
            "hedge for a short call spread two points wide. As the path hovers near the strike in the last days, the "
            "digital's hedge swings wildly, while the spread's stays within one over the width. "
            "<bookmark mark='b'/> Now forty thousand paths, and three rebalancing frequencies. Rebalancing sixteen "
            f"times as often, {verdict}"
        ) as vo:
            self.play(FadeIn(L), Create(k), FadeIn(leg), FadeIn(src))
            vo.wait_until("a")
            self.add(pS, pd, ps)
            self.play(tr.animate.set_value(n - 1), run_time=6, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.4), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def onetouch(self, o):
        rows = [
            cmath(r"P\Big(\min_{t \le T} X_t \le b\Big)", r"=", r"N\Big(\frac{b - \mu T}{\sigma\sqrt T}\Big) + "
                  r"e^{2\mu b/\sigma^2}\,N\Big(\frac{b + \mu T}{\sigma\sqrt T}\Big)", font_size=34,
                  colors={r"P\Big(\min_{t \le T} X_t \le b\Big)": OPT}),
            cmath(r"\mu = 0:\quad OT", r"=", r"2\,N\Big(\frac{b}{\sigma\sqrt T}\Big) = 2 \times \text{digital}",
                  font_size=34, colors={r"\mu = 0:\quad OT": GOOD}),
            cmath(r"r = q = 0:\quad OT", r"=", r"N(-d_2) + \frac{S}{H}\,N(-d_1)", font_size=34,
                  colors={r"r = q = 0:\quad OT": IV}),
        ]
        whys = [why(r"$X_t=\log(S_t/S_0)$, $X_0=0$, $b=\log(H/S_0)<0$, $\mu = r - q - \sigma^2/2$: the first-passage law of Brownian "
                    r"motion with drift (Part 5: reflection, then Girsanov)"),
                why(r"no drift: every path that ends below $b$ touched it, and so did its mirror image"),
                why(r"with the price a martingale the log drifts down, and the rule of thumb ``twice the digital'' "
                    r"overstates it")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-1.4, buff=0.8, edge=6.9)
        res = wrapped_label(rf"a down one-touch at 90, spot 100, six months, 25\%: closed form {o['closed']:.3f}; Monte "
                            rf"Carlo on 1{{,}}000 steps {o['mc']:.3f} $\pm$ {2 * o['mc_se']:.3f} (the BGK-shifted "
                            rf"formula: {o['bgk']:.3f}); twice the digital put {o['two_digital']:.3f}", 12.0, 20,
                            GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            f"Here the down one-touch pays one at maturity if the barrier was reached. First calculate its hitting probability for centered log return, starting at zero. With nonzero rates the maturity-paid price is this probability times the discount factor; pay-at-touch is a different contract. <bookmark mark='a'/> With zero log drift, reflection makes the hitting probability twice the terminal digital probability. <bookmark mark='b'/> With r and q both zero, the stock is a martingale but its log drifts downward. The formula becomes a digital put plus the weighted second term. Our continuous price is {o['closed']:.3f}; thousand-step Monte Carlo gives {o['mc']:.3f} and misses between-step touches. Twice the digital is {o['two_digital']:.3f}, too high here. Zero stock drift and zero log drift must remain distinct."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def skew(self, d):
        k = np.asarray(d["k"])
        g = axes([-0.2, 0.2], [0, 1], x_length=6.2, y_length=4.0, xlabel=r"log strike / forward",
                 ylabel=r"30-day digital call, bitcoin", xticks=[-0.2, -0.1, 0, 0.1, 0.2], yticks=[0, 0.5, 1.0],
                 font_size=15).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        flat = DashedVMobject(curve(ax, k, np.asarray(d["flat"]), GREY_B, stroke_width=2.5), num_dashes=40)
        sk = curve(ax, k, np.asarray(d["skew_price"]), OPT, stroke_width=3)
        fd = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=WHITE) for a, b in zip(k[::4], np.asarray(d["fd"])[::4])])
        leg = legend([(GREY_B, rf"Black--Scholes at the at-the-money vol, {100 * d['atm']:.0f}\%"),
                      (OPT, r"with the smile's slope"), (WHITE, r"check: $-\partial C/\partial K$ on the smile")],
                     font_size=16).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        rows = [cmath(r"D(K)", r"=", r"-\frac{d}{dK}C\big(K, \sigma(K)\big) = e^{-rT}N(d_2) - \mathcal V(K)\,\sigma'(K)",
                      font_size=30, colors={r"D(K)": OPT})]
        side = VGroup(rows[0],
                      wrapped_label(r"the chain rule: the call depends on the strike directly and through the smile. "
                                    r"Where the smile falls with strike ($\sigma' < 0$, the equity skew), the digital is "
                                    r"dearer than Black--Scholes at the same strike volatility $\sigma(K)$ (rates zero here)", 5.0, 19, GREY_A),
                      wrapped_label(rf"at the money: {100 * d['atm_diff']:+.1f} points against the flat-vol price; at "
                                    rf"$k = 0.1$, where the bitcoin smile turns up, {d['at_k']['skew']:.3f} against "
                                    rf"{d['at_k']['flat']:.3f}", 5.0, 19, WHITE),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        pp = pause_card(r"At the money, with negative smile slope: how does the digital compare with Black--Scholes at the same volatility?",
                        width=6.4).to_corner(UR, buff=0.3)
        src = real_data(r"the Surface: Part 12's SSVI fit to Deribit bitcoin options, 10 December 2025, 30-day slice")
        cheaper = d["at_k"]["skew"] < d["at_k"]["flat"]
        tail = (", and further out, where the bitcoin smile turns up, it is cheaper." if cheaper else ".")
        with self.voiceover(
            f"What does the smile add? At the money, under a negative smile slope, compare a digital with Black-Scholes at that same implied volatility. <bookmark mark='a'/> The digital is minus the strike derivative of the entire call-price curve. The chain rule subtracts vega times sigma prime. A negative slope raises the digital relative to Black-Scholes evaluated at the same strike's volatility. Away from the money, that is not necessarily the flat ATM-volatility comparator drawn here. <bookmark mark='b'/> At the money on this bitcoin slice, the difference is {100 * d['atm_diff']:+.1f} probability points. At k of 0.1, the smile-based value is {d['at_k']['skew']:.3f}, versus {d['at_k']['flat']:.3f} under flat ATM volatility. White dots verify the derivative numerically on this fitted curve. A spline-based slice is not a guarantee of arbitrage freedom outside the checked domain. Next, averages and extremes."
        ) as vo:
            self.play(FadeIn(pp))
            vo.wait_until("a")
            self.play(FadeOut(pp), FadeIn(g), FadeIn(src), Create(flat), FadeIn(leg[0]), FadeIn(side[0]),
                      FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(sk), FadeIn(leg[1]), FadeIn(fd), FadeIn(leg[2]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
