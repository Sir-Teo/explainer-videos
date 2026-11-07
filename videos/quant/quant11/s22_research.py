from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, load

FAIR, PUTS, CALLS, ONE = GREY_A, THETA, GAMMA, VEGA


class Research(VoiceoverScene):
    def construct(self):
        t = load("demand_theory")
        self.card()
        self.dealer()
        self.consequences()
        self.residual_plot(t)
        self.smile_plot(t)
        self.exact(t)
        self.flow(t)
        self.open_problems()
        self.question(t)

    def card(self):
        c = research_card(r"Demand-based option pricing", r"If a dealer cannot hedge perfectly, how does demand move "
                          r"option prices?", part=PART)
        with self.voiceover("For the researcher: Chapter 9 noted that a market maker's inventory moves its quotes, and "
                            "that demand itself moves option prices. Here is the theory of that second fact: why net "
                            "demand from end users bends the smile, which options it bends, and when it cannot."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def dealer(self):
        rows = [cmath(r"\varepsilon_i", r"=", r"(x_i-H_i)-\mathbb E^Q[x_i-H_i],\quad H_i=\sum_k\delta_{i,k}\Delta S_k", font_size=32,
                      colors={r"\varepsilon_i": THETA}),
                cmath(r"W", r"=", r"q^{\top}(p-m)-q^{\top}\varepsilon,\quad m=\mathbb E^Q x", font_size=32, colors={r"W": OPT}),
                cmath(r"\max_q\ q^{\top}(p-m) - \tfrac{\gamma}{2}\,q^{\top}\Sigma_\varepsilon q", r"\Rightarrow",
                      r"p = m + \gamma\,\Sigma_\varepsilon\,d", font_size=30,
                      colors={r"p = m + \gamma\,\Sigma_\varepsilon\,d": VEGA})]
        whys = [why(r"illustration under a fixed martingale measure $Q$, zero rates and yield; center each fixed-hedge residual by its own mean"),
                why(r"$q$ denotes dealer shorts, so option holdings are $-q$; market clearing sets $q=d$"),
                why(r"mean--variance first-order illustration with fixed hedges; the covariance and demand fix the marginal premium")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        thm = theorem_card(r"Demand pressure", wrapped_label(
            r"first-order illustration: own impact follows residual variance; cross-impact has the sign of residual covariance; perfect replication removes the residual-demand term", 10.6, 20, GREY_A),
            who=r"G\^arleanu, Pedersen and Poteshman (2009), \textit{RFS} 22; the first-order form shown here",
            width=11.6, font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            """A simplified dealer problem, under a fixed martingale measure Q and zero rates and yield. <bookmark mark='a'/> Hedge each option at discrete times, then center its payoff-minus-hedge residual by its own expectation. <bookmark mark='b'/> Let q denote how many options the dealer is short; holdings are minus q, and market clearing sets q equal to customer demand d. <bookmark mark='c'/> In this mean-variance illustration, the first-order condition adds gamma times the residual covariance matrix times demand to the model baseline. Cross-impact has the sign of the covariance. <bookmark mark='d'/> Gârleanu, Pedersen and Poteshman developed a richer dynamic demand-based theory in 2009. This one-period calculation illustrates its mechanism; it does not reproduce their full equilibrium or identify a market risk premium."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(thm))
        self.wait(0.5)
        self.clear_scene()

    def consequences(self):
        rows = [cmath(r"\frac{\partial p_i}{\partial d_i}", r"=", r"\gamma\operatorname{Var}(\varepsilon_i)", font_size=32,
                      colors={r"\frac{\partial p_i}{\partial d_i}": VEGA}),
                cmath(r"\frac{\partial p_i}{\partial d_j}", r"=", r"\gamma\operatorname{Cov}(\varepsilon_i, \varepsilon_j)",
                      font_size=32, colors={r"\frac{\partial p_i}{\partial d_j}": ALT}),
                cmath(r"\Sigma_\varepsilon \to 0", r"\Rightarrow", r"p \to \mathbb E x\quad\text{(complete market: demand "
                      r"is irrelevant)}", font_size=30, colors={r"\Sigma_\varepsilon \to 0": SPOT})]
        whys = [why(r"an option's own demand moves it in proportion to how badly it can be hedged"),
                why(r"demand for one strike moves its neighbours: residuals of nearby strikes are highly correlated, so "
                    r"demand spreads along the smile"),
                why(r"Black, Scholes and Merton's world is the limit: continuous hedging, no jumps, no residual, and the "
                    r"price is fixed by replication whatever anyone wants")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Three consequences. <bookmark mark='a'/> An option's own demand moves its price in proportion to how badly "
            "it can be hedged. <bookmark mark='b'/> Demand for one strike moves the others, in proportion to the "
            "covariance of their residuals: neighbouring strikes share most of their unhedgeable risk, so demand "
            "spreads along the smile. <bookmark mark='c'/> And in Black and Scholes's world, with continuous hedging "
            "and no jumps, the residual vanishes and so does the effect: the price is fixed by replication, whatever "
            "anyone wants."
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

    def residual_plot(self, t):
        K = np.asarray(t["K"], float)
        g = axes([78, 122], [0, 2.2], x_length=8.2, y_length=4.0, xlabel=r"strike (spot 100), 30 days",
                 ylabel=r"standard deviation of the hedged residual, per 100 of underlying",
                 xticks=[80, 90, 100, 110, 120], yticks=[0, 1, 2], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        sets = [("resid_sd", THETA, r"jumps, hedged daily"), ("diff_daily", GREY_B, r"no jumps, hedged daily"),
                ("diff_hourly", SPOT, r"no jumps, hedged hourly")]
        lines = VGroup()
        for key, col, _ in sets:
            v = t[key] if key == "resid_sd" else t[key]["resid_sd"]
            lines.add(VGroup(curve(ax, K, v, col, stroke_width=3),
                             *[Dot(ax.c2p(a, b), radius=0.05, color=col) for a, b in zip(K, v)]))
        leg = legend([(c, n) for _, c, n in sets], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"Merton jump-diffusion: $\sigma = {100 * t['sigma']:.0f}\%$, {t['lam']:.0f} jumps a year of "
                             rf"log-jump mean ${100 * t['mj']:.0f}\%$ and sd ${100 * t['sj']:.0f}\%$; out-of-the-money puts below "
                             rf"100, calls above; delta at the total volatility {100 * t['hedge_vol']:.0f}\%; 40{{,}}000 "
                             r"jump paths; diffusion comparisons: 8{,}000 paths at 52\%", 3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "How large is the residual? Simulate a jump-diffusion like Bitcoin's, and delta-hedge one-month options daily. <bookmark mark='a'/> With jumps the residual is one to two percent of the underlying, largest at the money. <bookmark mark='b'/> Remove the jumps and it falls by half or more. <bookmark mark='c'/> Hedge hourly as well, and it nearly disappears. The more complete the market, the less room demand has to move prices. This is an illustrative zero-drift model, not a fitted Bitcoin law. The jump mean and spread quoted are log-jump parameters. The jump case uses forty thousand paths; each diffusion comparison uses eight thousand."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side), FadeIn(lines[0]), FadeIn(leg[0]))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(lines[k]), FadeIn(leg[k]), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    def smile_plot(self, t):
        K = np.asarray(t["K"], float)
        fair = 100 * np.asarray(t["fair_iv"])
        g = axes([78, 122], [47, 61], x_length=8.2, y_length=4.2, xlabel=r"strike (spot 100), 30 days",
                 ylabel=r"implied volatility, \%", xticks=[80, 90, 100, 110, 120], yticks=[48, 52, 56, 60],
                 font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        sets = [(None, FAIR, r"model baseline under the selected $Q$"), ("put85", ONE, r"demand: one 85 put"),
                ("puts", PUTS, r"demand: one of each put"), ("calls", CALLS, r"demand: one of each call")]
        lines = VGroup()
        for key, col, _ in sets:
            v = fair if key is None else fair + np.asarray(t["scen"][key]["d_iv_pts"])
            lines.add(curve(ax, K, v, col, stroke_width=3))
        leg = legend([(c, n) for _, c, n in sets], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        p85 = t["scen"]["put85"]["d_iv_pts"]
        side = wrapped_label(rf"$\gamma$ set so that local vega calibration targets one vol point at the 85 put (repriced: about 0.99); it "
                             rf"then moves the 80 put {p85[0]:.1f} points and the 120 call {p85[-1]:.1f}", 3.3, 14,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        pu, ca = t["scen"]["puts"]["d_iv_pts"], t["scen"]["calls"]["d_iv_pts"]
        with self.voiceover(
            "Now apply demand. <bookmark mark='a'/> The grey line is the risk-neutral smile of the jump model: already "
            "skewed, by the jumps. <bookmark mark='b'/> Demand for a single eighty-five put lifts its own volatility one "
            f"point approximately, under the local vega calibration, and lifts the eighty put {p85[0]:.1f} points and even the hundred-and-twenty call "
            f"{p85[-1]:.1f}. <bookmark mark='c'/> Demand for every put steepens the skew: {pu[0]:.1f} points at eighty, "
            f"{pu[-1]:.1f} at a hundred and twenty. <bookmark mark='d'/> Demand for calls tilts it the other way. The "
            "shape of the smile carries the shape of the demand."
        ) as vo:
            self.play(FadeIn(g))
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(Create(lines[k]), FadeIn(leg[k]), run_time=1.2)
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def exact(self, t):
        i = t["indiff"]
        q = np.asarray(i["q"])
        g = axes([0, 4.1], [0, 0.4], x_length=8.0, y_length=4.0, xlabel=r"units of the 85 put the dealer is short, $q$",
                 ylabel=r"marginal price premium over risk-neutral value", xticks=[0, 1, 2, 3, 4], yticks=[0, 0.2, 0.4],
                 font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        ex = curve(ax, q, i["exact_marg"], VEGA, stroke_width=3)
        mv = curve(ax, q, i["mv_marg"], GREY_B, stroke_width=3)
        leg = legend([(VEGA, r"empirical tilt: $\overline{\varepsilon e^{\gamma q\varepsilon}}/\overline{e^{\gamma q\varepsilon}}$"),
                      (GREY_B, r"first order: $\gamma q\operatorname{Var}\varepsilon$")], font_size=16).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        j1, j4 = 9, len(q) - 1
        r1 = i["exact_marg"][j1] / i["mv_marg"][j1] - 1
        r4 = i["exact_marg"][j4] / i["mv_marg"][j4] - 1
        side = wrapped_label(rf"finite empirical exponential tilt, fixed hedge; option-liability residual skewness "
                             rf"{i['skew_eps']:.1f}: crashes are what the dealer cannot hedge", 3.3, 14, GREY_A).next_to(
            leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"""Compare the first-order line with exponential tilting of these forty thousand centered residuals, keeping the delta hedge fixed. This is a finite empirical calculation, not an optimized-hedge utility price or a proof that the population exponential moment exists. <bookmark mark='a'/> At small positions they nearly agree. <bookmark mark='b'/> The option residual, a liability to the short dealer, has positive skewness {i['skew_eps']:.1f}. The empirical marginal premium is {100 * r1:.0f} percent above the line at {q[j1]:.2f} units and {100 * r4:.0f} percent at four. Nonlinearity and sample-tail sensitivity matter; those percentages are properties of this finite simulation."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(side), Create(mv), FadeIn(leg[1]))
            vo.wait_until("a")
            self.play(Indicate(mv), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(ex), FadeIn(leg[0]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def flow(self, t):
        f = t["flow"]
        keys = [("otm_put_short", r"puts, OTM, up to 30 days"), ("otm_put_long", r"puts, OTM, beyond 30 days"),
                ("near_short", r"near the money, up to 30 days"), ("near_long", r"near the money, beyond 30 days"),
                ("otm_call_short", r"calls, OTM, up to 30 days"), ("otm_call_long", r"calls, OTM, beyond 30 days")]
        hx = [-3.6, 1.0, 3.6]
        head = VGroup(label(r"Deribit BTC options", font_size=18, color=GREY_B), label(r"trades", font_size=20),
                      label(r"net taker buying, share of vega", font_size=20, color=VEGA))
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(n, font_size=18, color=THETA if "put" in k else GAMMA if "call" in k
                                                       else GREY_A),
                                                 MathTex(rf"{f[k]['trades']:,}".replace(",", "{,}"), font_size=26),
                                                 MathTex(rf"{100 * f[k]['net_share']:+.0f}\%", font_size=26))
                                          for k, n in keys]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.0 - 0.6 * j, 0])
            row[0].align_to(np.array([hx[0] - 2.9, 0, 0]), LEFT)
            tab.add(row)
        foot = wrapped_label(r"eligible BTC trades on 10 and 11 December 2025, with reported IV and maturity over one day; taker direction is a rough flow proxy; OTM: strike below 95\% (puts) or above "
                             r"105\% (calls) of the index; net buying = (bought $-$ sold) vega over traded vega. Two days "
                             r"describe the flow; testing the theory takes years of it (G\^arleanu et al.\ used 1996--2001 "
                             r"CBOE data by investor type)", 11.8, 15, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"What does demand look like? On the Surface's two days of Deribit trades, count the side that crossed the spread, a rough proxy for end users. <bookmark mark='a'/> Near the money, buying and selling balance; within a month, takers were net sellers of out-of-the-money puts, {100 * f['otm_put_short']['net_share']:+.0f} percent. <bookmark mark='b'/> Beyond a month, takers were net buyers of out-of-the-money puts, {100 * f['otm_put_long']['net_share']:+.0f} percent of their vega, and net sellers of out-of-the-money calls, {100 * f['otm_call_long']['net_share']:+.0f}: protection bought, upside sold, a collar. The theory says such flow should steepen the long-dated skew. Two days describe it; a test needs years. Only eligible trades with reported IV and more than one day to expiry enter these bins. Takers need not be end users; aggregate put buying and call selling do not identify the same investors or prove a collar or a causal demand effect."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot), FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[5]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[6]))
            self.play(Indicate(tab[2], color=THETA), Indicate(tab[6], color=GAMMA))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: which dealers, which risk aversion?", r"$\gamma$ is not observed; it varies with dealers' "
                          r"capital and losses, and identifying demand effects separately from changing risk is hard",
                          width=12.4, font_size=18),
            desk_question(r"open: demand and the volatility premium", r"how much of the variance risk premium of Chapter 6 is "
                          r"compensation for priced risk, and how much is the price of absorbing hedging demand, is "
                          r"debated", width=12.4, font_size=18),
            desk_question(r"open: equilibrium with many dealers and learning", r"research direction: specify dealer heterogeneity, capital constraints and learning, then compare equilibrium prices and quote dynamics", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Dealers' risk aversion is not observed. It moves with their "
            "capital and their losses, so separating demand effects from changing risk is hard. <bookmark mark='b'/> How "
            "much of Chapter 6's volatility premium is compensation for priced risk, and how much is the price of absorbing "
            "hedging demand, is debated. <bookmark mark='c'/> And with many dealers, inventories carried through time, "
            "and the quote dynamics of Chapter 9, choose a specific model and compare its equilibrium prices and quote dynamics."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self, t):
        q = pause_card(r"demand arrives for the 85 put. In dollars, which rises more, the 90 put or the 80 put? In "
                       r"implied volatility? Why can the answers differ?")
        q.move_to(UP * 0.8)
        with self.voiceover(
            "Pause and predict. Demand arrives for the eighty-five put. In dollars, which rises more, the ninety put or "
            "the eighty put? And in implied volatility? Why can the two answers differ?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        dollars = np.asarray(t["cross_85"])
        iv = np.asarray(t["scen"]["put85"]["d_iv_pts"])
        answer = VGroup(
            label(rf"dollar impact / 85-put impact: 90 put {dollars[2]:.2f}; 80 put {dollars[0]:.2f}", font_size=24, color=VEGA),
            label(rf"IV impact: 80 put {iv[0]:.2f} points; 90 put {iv[2]:.2f} points", font_size=24, color=GAMMA),
            wrapped_label(r"the 80 put has less vega: a smaller dollar move can imply a larger volatility move", 10.8, 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(q, DOWN, buff=0.5)
        if answer.width > 12.0:
            answer.scale_to_fit_width(12.0)
        with self.voiceover("The ninety put rises more in dollars; the eighty put rises more in implied volatility because it has less vega. Dollar impact and volatility impact rank different things."):
            self.play(FadeIn(answer))
        self.clear_scene()
