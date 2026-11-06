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
        t = theorem_card(r"Change of numeraire", r"Let $N>0$ be tradable and $N/B$ a true $Q$-martingale. Then $\frac{dQ^N}{dQ}=\frac{N_T/N_0}{B_T/B_0}$ defines an equivalent measure. Appropriately integrable discounted prices become martingales in units of $N$.",
                         who=r"Geman, El Karoui and Rochet (1995); Jamshidian (1989) for the bond", color=Q_C,
                         width=10.4, font_size=25).move_to(UP * 0.5)
        with self.voiceover(
            """Replace the bank account with a positive tradable numeraire. Its discounted price must be a true martingale, giving a mean-one density. <bookmark mark='a'/> With pricing integrability, this changes the unit and measure. Geman, El Karoui and Rochet, 1995. A strict local martingale need not qualify."""
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
            """Divide a replicable claim by the numeraire or bank account. <bookmark mark='a'/> Their expectation formulas identify the measure density as relative numeraire growth. <bookmark mark='b'/> Split a call into the share received and strike paid. <bookmark mark='c'/> These give exercise probabilities under the stock measure and Q. <bookmark mark='d'/> For a non-dividend-paying constant-volatility stock, their log drifts differ by sigma squared: N of d one and N of d two. The equalities require true pricing martingales."""
        ) as vo:
            step(0, run_time=0.15)
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
            f"""Stock and strike are one hundred, volatility twenty-five percent, maturity one year. The Q exercise probability is {n['Nd2']:.4f}. <bookmark mark='a'/> Weight the density by terminal stock over today's price: under the stock measure it becomes {n['Nd1']:.4f}. <bookmark mark='b'/> Their price-weighted difference gives {n['call']:.2f}. The two log drifts are minus and plus half sigma squared."""
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
            f"""For an option exchanging two assets, divide by asset two: the payoff becomes a ratio call struck at one. <bookmark mark='a'/> Its volatility combines both volatilities and correlation. <bookmark mark='b'/> Apply Black-Scholes to this ratio: Margrabe, 1978. <bookmark mark='c'/> The formula gives {n['margrabe']:.2f}; the two million-path checks give {n['mc_Q']:.2f} and {n['mc_S2']:.2f}. Equal thirty-percent volatilities and correlation one half give thirty-percent ratio volatility. Correlation one would make the at-the-money option worthless."""
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.3), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    def bitcoin(self, n):
        spot = load("kernel")["S"]  # Surface median index, already restored
        forward_mean = n["usd"] / n["btc"]  # mean of the normalized finite-grid density
        df_usd = spot / forward_mean  # chosen consistent discount; BTC discount is one
        spot_pv = spot * n["btc"]
        items = VGroup(
            cmath(r"P(t, T)", r":", r"\text{the }T\text{-forward measure: forwards are martingales (Part 19)}",
                  font_size=30),
            cmath(r"A(t)", r":", r"\text{annuity measure; Black needs a lognormal swap-rate assumption (Part 19)}",
                  font_size=30),
            cmath(r"\text{BTC}", r":", r"\text{Deribit's unit: a price in BTC is an expectation under the bitcoin "
                  r"measure}", font_size=30, colors={r"\text{BTC}": Q_C}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(UP, buff=0.6)
        if items.width > 13:
            items.scale_to_fit_width(13)
        res = VGroup(
            label(rf"the Surface's 107-day call struck at {n['K_btc']:,.0f}".replace(",", "{,}"), font_size=24),
            MathTex(rf"\text{{forward dollar value: }}\ \mathbb{{E}}^Q[(S_T - K)^+] = \${n['usd']:,.0f}".replace(",", "{,}"),
                    font_size=30, color=CALL),
            MathTex(rf"\text{{in bitcoin: }}\ \mathbb{{E}}^{{Q^{{BTC}}}}[(S_T - K)^+/S_T] = {n['btc']:.4f}\ \text{{BTC}}",
                    font_size=30, color=Q_C),
            MathTex(rf"D_{{USD}}=S_0/F_{{\rm grid}}={df_usd:.5f},\quad D_{{BTC}}=1", font_size=27, color=GREY_A),
            MathTex(rf"C_{{USD}}(0)=S_0 C_{{BTC}}\approx\${spot_pv:,.0f}".replace(",", "{,}"), font_size=30, color=Q_C),
            MathTex(rf"Q(S_T > K) = {n['Q_itm']:.3f},\quad Q^{{BTC}}(S_T > K) = {n['QB_itm']:.3f}", font_size=28,
                    color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(items, DOWN, buff=0.5)
        src = real_data(r"the Surface's density for 27 March 2026 (chapter 12)")
        with self.voiceover(
            f"""Bonds and annuities generate forward and swap measures; Black's swaption formula also assumes lognormal swap rates. <bookmark mark='a'/> The Bitcoin grid gives an undiscounted dollar forward value of {n['usd']:,.0f} and premium {n['btc']:.4f} Bitcoin. <bookmark mark='b'/> Choose Bitcoin discounting of one and consistent dollar discounting {df_usd:.5f}. Multiplying the premium by spot {spot:,.0f} gives present value {spot_pv:,.0f}; using the grid's forward mean instead gives the forward value. Exercise probabilities differ, {n['Q_itm']:.2f} versus {n['QB_itm']:.2f}. Discounted prices agree in the same current unit. These choices illustrate conversion, rather than independently estimate currency curves."""
        ) as vo:
            self.play(LaggedStart(*[FadeIn(i_) for i_ in items[:2]], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(FadeIn(items[2]), FadeIn(res[0]), FadeIn(res[1]), FadeIn(res[2]), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(res[3]), FadeIn(res[4]), FadeIn(res[5]))
        self.wait(0.3)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"Under the stock's own measure $Q^S$, does the stock drift faster or slower than the riskless "
                        r"rate?")
        with self.voiceover(
            """Under the stock measure, is its drift above the riskless rate? <bookmark mark='a'/> Yes, by sigma squared. Terminal-price weighting tilts the drift up."""
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"faster: $dS = (r + \sigma^2) S\,dt + \sigma S\, dW^S$; weighting paths "
                                                r"by $S_T$ tilts the drift up by $\sigma^2$")))
        self.wait(0.4)
        self.clear_scene()
