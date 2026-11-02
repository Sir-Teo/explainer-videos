from __future__ import annotations

import numpy as np
from scipy.stats import norm

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import (ALT, ARB, CALL, FWD, P_C, PART, Q_C, answer_under, load, pause_at, real_data)


class Numeraire(VoiceoverScene):
    def construct(self):
        n = load("numeraire")
        self.card()
        self.theorem()
        self.derive(n)
        self.densities(n)
        self.margrabe(n)
        self.bitcoin(n)
        self.predict()

    def card(self):
        c = chapter_card(11, r"Change of numeraire", r"What if you measured every price in shares instead of dollars?",
                         part=PART)
        with self.voiceover("Chapter eleven. Change of numeraire."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theorem(self):
        t = theorem_card(r"Change of numeraire", r"Any asset $N$ with a strictly positive price can be the unit of "
                         r"account. There is a measure $Q^N$ under which every price divided by $N$ is a martingale, "
                         r"with $\frac{dQ^N}{dQ} = \frac{N_T / N_0}{B_T / B_0}$.",
                         who=r"Geman, El Karoui and Rochet (1995); Jamshidian (1989) for the bond", color=Q_C,
                         width=10.4, font_size=25).move_to(UP * 0.5)
        with self.voiceover(
            "So far every price has been measured in units of the bank account. Nothing forces that. Any asset with "
            "a strictly positive price can be the unit of account, the numeraire, and each numeraire comes with its "
            "own martingale measure. <bookmark mark='a'/> Hélyette Geman, Nicole El Karoui and Jean-Charles Rochet "
            "made this a general tool in 1995, and Farshid Jamshidian had used the bond as numeraire in 1989. The "
            "density between two of these measures is just the ratio of the two numeraires' growth."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(t, color=Q_C, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    def derive(self, n):
        rows = [cmath(r"\frac{V_0}{N_0} = \mathbb{E}^{Q^N}\!\left[\frac{V_T}{N_T}\right]", r",",
                      r"\frac{V_0}{B_0} = \mathbb{E}^{Q}\!\left[\frac{V_T}{B_T}\right]", font_size=32),
                cmath(r"\frac{dQ^N}{dQ}", r"=", r"\frac{N_T/N_0}{B_T/B_0}", font_size=36, colors={r"\frac{dQ^N}{dQ}": Q_C}),
                cmath(r"C", r"=", r"\mathbb{E}^Q\!\left[e^{-rT}S_T 1_{S_T > K}\right] - K e^{-rT}\,Q(S_T > K)",
                      font_size=32, colors={r"C": CALL}),
                cmath(r"C", r"=", r"S_0\, Q^S(S_T > K) - K e^{-rT}\, Q(S_T > K)", font_size=34, colors={r"C": CALL}),
                cmath(r"C", r"=", r"S_0\, N(d_1) - K e^{-rT} N(d_2)", font_size=36, colors={r"C": CALL})]
        whys = [why(r"the same price, in two units: both must hold for every claim $V$", 21),
                why(r"equate the two expressions (the law of one price): the density is the numeraires' relative growth", 21),
                why(r"split the call's payoff: the share you receive, and the strike you pay, when it ends in the money", 21),
                why(r"the first term in units of the stock: $S_T/S_0$ over $B_T/B_0$ is exactly $dQ^S/dQ$", 21),
                why(r"under $Q^S$ the log-price drifts at $r + \tfrac12\sigma^2$ instead of $r - \tfrac12\sigma^2$ "
                    r"(Girsanov with $\sigma$): $N(d_1)$ and $N(d_2)$ are one event's probability under two measures", 21)]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-0.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "The derivation takes two lines. Any price, divided by the numeraire, is an expectation under that "
            "numeraire's measure; and divided by the bank account, an expectation under Q. <bookmark mark='a'/> Both "
            "hold for every claim, so the two measures differ by the ratio of how the numeraire and the bank account "
            "grew. <bookmark mark='b'/> Use it on a call. The payoff is the share you receive minus the strike you "
            "pay, when the call ends in the money. <bookmark mark='c'/> The strike part is a Q-probability. The share "
            "part, measured in shares, is a probability under the stock's own measure. <bookmark mark='d'/> Under the "
            "stock measure the log-price drifts up by a full sigma squared more, and so the two famous terms of Black "
            "and Scholes are the same event, the call ending in the money, seen in two units of account: N of d one "
            "in shares, N of d two in dollars."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    def densities(self, n):
        S0, K, T, sig = 100.0, 100.0, 1.0, 0.25
        s = np.linspace(20, 260, 481)
        m = np.log(S0) - 0.5 * sig ** 2 * T
        q = norm.pdf((np.log(s) - m) / sig) / (s * sig)
        qs = q * s / S0
        top = qs.max() * 1.1
        g = axes([20, 260], [0, top], x_length=7.6, y_length=4.4, xlabel=r"stock price at expiry", ylabel=r"density",
                 xticks=[50, 100, 150, 200, 250], yticks=[], font_size=16)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        w = ValueTracker(0.0)

        def dens():
            a = w.get_value()
            y = (1 - a) * q + a * qs
            col = interpolate_color(ManimColor(Q_C), ManimColor(CALL), a)
            sh = band(ax, s[s >= K], 0 * s[s >= K], y[s >= K], col, 0.35)
            return VGroup(sh, curve(ax, s, y, col, stroke_width=4))

        D = always_redraw(dens)
        kl = DashedLine(ax.c2p(K, 0), ax.c2p(K, top), color=GREY_B, stroke_width=1.5)
        area = DecimalNumber(n["Nd2"], num_decimal_places=4, font_size=34, color=Q_C)
        area.add_updater(lambda mm: mm.set_value((1 - w.get_value()) * n["Nd2"] + w.get_value() * n["Nd1"]))
        side = VGroup(
            VGroup(label(r"shaded: probability of ending in the money", font_size=20, color=GREY_A)),
            area,
            MathTex(rf"Q(S_T > K) = N(d_2) = {n['Nd2']:.4f}", font_size=28, color=Q_C),
            MathTex(rf"Q^S(S_T > K) = N(d_1) = {n['Nd1']:.4f}", font_size=28, color=CALL),
            MathTex(rf"C = 100 \times {n['Nd1']:.5f} - 100 \times {n['Nd2']:.5f} = {n['call']:.3f}", font_size=26),
            wrapped_label(r"the stock measure's density is $Q$'s times $s/S_0$: every path counts in proportion to "
                          r"how much stock it ends with", 4.4, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "See it. A stock at a hundred, twenty-five percent volatility, one year, zero rates, a call struck at a "
            "hundred. The purple curve is Q's density for the price at expiry; the shaded area, the chance of ending "
            f"in the money under Q, is {n['Nd2']:.4f}: N of d two. <bookmark mark='a'/> Now change the unit to the "
            "stock. Multiply the density by the price over today's price: every outcome counts in proportion to how "
            "much it is worth in shares. The curve leans right, and the same shaded event now has probability "
            f"{n['Nd1']:.4f}: N of d one. <bookmark mark='b'/> A hundred times the first minus a hundred times the "
            f"second: {n['call']:.2f}, the Black-Scholes price. One payoff, two units, two probabilities, one price."
        ) as vo:
            self.add(D)
            self.play(FadeIn(g), Create(kl), FadeIn(side[0]), FadeIn(area), FadeIn(side[2]))
            vo.wait_until("a")
            self.play(w.animate.set_value(1.0), run_time=3)
            self.play(FadeIn(side[3]), FadeIn(side[5]))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
        D.clear_updaters()
        area.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def margrabe(self, n):
        rows = [cmath(r"\frac{(S^1_T - S^2_T)^+}{S^2_T}", r"=", r"(R_T - 1)^+,\qquad R = S^1/S^2", font_size=34),
                cmath(r"\sigma_R^2", r"=", r"\sigma_1^2 + \sigma_2^2 - 2\rho\,\sigma_1\sigma_2", font_size=34),
                cmath(r"V_0", r"=", r"S^2_0\ \mathbb{E}^{Q^{S^2}}[(R_T - 1)^+] = S^2_0\,\mathrm{BS}(R_0, 1, \sigma_R, T)",
                      font_size=34, colors={r"V_0": CALL})]
        whys = [why(r"the option to exchange asset 2 for asset 1, measured in units of asset 2", 21),
                why(r"under the measure of asset 2, $R$ is a martingale with this volatility (It\^o on a ratio)", 21),
                why(r"so it is a call on $R$ struck at 1, with zero rates: Margrabe (1978)", 21)]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-0.6, buff=0.6, edge=6.9)
        res = VGroup(
            MathTex(rf"S^1_0 = S^2_0 = 100,\ \sigma_1 = \sigma_2 = 30\%,\ \rho = 0.5\ \Rightarrow\ \sigma_R = "
                    rf"{100 * n['sR']:.0f}\%", font_size=28),
            MathTex(rf"\text{{formula: }} {n['margrabe']:.3f}", font_size=30, color=CALL),
            MathTex(rf"\text{{Monte Carlo under }} Q:\ {n['mc_Q']:.3f} \pm {n['se_Q']:.3f}", font_size=28, color=Q_C),
            MathTex(rf"\text{{Monte Carlo under }} Q^{{S^2}}:\ {n['mc_S2']:.3f} \pm {n['se_S2']:.3f}", font_size=28,
                    color=ALT),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The trick pays off on an option to exchange one asset for another. Measure everything in units of the "
            "second asset. The payoff becomes a call on the ratio of the two, struck at one. <bookmark mark='a'/> "
            "Under the second asset's measure that ratio is a martingale, with a volatility built from both "
            "volatilities and their correlation. <bookmark mark='b'/> So the price is the second asset times a "
            "Black-Scholes call on the ratio, with no interest rate at all: William Margrabe's formula of 1978. "
            "<bookmark mark='c'/> Two assets at a hundred, thirty percent volatility each, correlation one half: "
            f"the formula says {n['margrabe']:.2f}. A million paths of both assets under Q say {n['mc_Q']:.2f}; a "
            f"million paths of the ratio alone under the second asset's measure say {n['mc_S2']:.2f}. Three methods, "
            "one price, within the simulation's error."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.3), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    def bitcoin(self, n):
        items = VGroup(
            cmath(r"P(t, T)", r":", r"\text{the }T\text{-forward measure: forwards are martingales (Part 19)}",
                  font_size=30),
            cmath(r"A(t)", r":", r"\text{the annuity measure: swap rates are martingales, swaptions are Black (Part 19)}",
                  font_size=30),
            cmath(r"\text{BTC}", r":", r"\text{Deribit's unit: a price in BTC is an expectation under the bitcoin "
                  r"measure}", font_size=30, colors={r"\text{BTC}": Q_C}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(UP, buff=0.6)
        if items.width > 13:
            items.scale_to_fit_width(13)
        res = VGroup(
            label(rf"the Surface's 107-day call struck at {n['K_btc']:,.0f}".replace(",", "{,}"), font_size=24),
            MathTex(rf"\text{{in dollars: }}\ \mathbb{{E}}^Q[(S_T - K)^+] = \${n['usd']:,.0f}".replace(",", "{,}"),
                    font_size=30, color=CALL),
            MathTex(rf"\text{{in bitcoin: }}\ \mathbb{{E}}^{{Q^{{BTC}}}}[(S_T - K)^+/S_T] = {n['btc']:.4f}\ \text{{BTC}}",
                    font_size=30, color=Q_C),
            MathTex(rf"{n['btc']:.4f} \times F = \${n['btc_times_F']:,.0f}".replace(",", "{,}"), font_size=30, color=Q_C),
            MathTex(rf"Q(S_T > K) = {n['Q_itm']:.3f},\quad Q^{{BTC}}(S_T > K) = {n['QB_itm']:.3f}", font_size=28,
                    color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(items, DOWN, buff=0.5)
        src = real_data(r"the Surface's density for 27 March 2026 (chapter 12)")
        with self.voiceover(
            "The same idea runs the rest of the series. The zero-coupon bond as numeraire gives the T-forward "
            "measure, under which forward prices are martingales; the annuity gives the measure under which swap "
            "rates are, and swaptions become Black's formula. Part nineteen uses both. <bookmark mark='a'/> And "
            "Deribit already uses Bitcoin as numeraire: its options are priced and paid in Bitcoin. Take the "
            "Surface's call a hundred and seven days out. Its dollar price, as a Q-expectation, is "
            f"{n['usd']:,.0f} dollars. Its Bitcoin price, as an expectation under the Bitcoin measure of the payoff "
            f"divided by the Bitcoin price, is {n['btc']:.4f}. <bookmark mark='b'/> Multiply by the forward, and "
            "you get the same dollars back, to the cent. The two measures disagree about the chance of ending in "
            f"the money, {n['Q_itm']:.2f} against {n['QB_itm']:.2f}, and agree exactly about the price. That is why "
            "parity in chapter one read one minus K over F."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(i_) for i_ in items[:2]], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(FadeIn(items[2]), FadeIn(res[0]), FadeIn(res[1]), FadeIn(res[2]), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(res[3]), FadeIn(res[4]))
        self.wait(0.3)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"Under the stock's own measure $Q^S$, does the stock drift faster or slower than the riskless "
                        r"rate?")
        with self.voiceover(
            "Pause and predict. Under the stock's own measure, does the stock drift faster or slower than the "
            "riskless rate? <bookmark mark='a'/> Faster, by sigma squared. Measuring in shares weights each path by "
            "how high it ends, and that tilts the drift up by exactly the stock's variance rate."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"faster: $dS = (r + \sigma^2) S\,dt + \sigma S\, dW^S$; weighting paths "
                                                r"by $S_T$ tilts the drift up by $\sigma^2$")))
        self.wait(0.4)
        self.clear_scene()
