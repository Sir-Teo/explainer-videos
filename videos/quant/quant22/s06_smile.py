from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, BASIS, FOR, GOOD, PART, USD, ask, fit_right, illustration, load


class Smile(VoiceoverScene):
    def construct(self):
        x = load("fxopt")
        self.card()
        self.quotes(x)
        self.strikes(x)
        self.vv_idea()
        self.vv_plot(x)
        self.term(x)
        self.why_vv()

    def card(self):
        c = chapter_card(5, r"The FX smile", r"How do three quotes become a whole smile?", lit=(2007,), part=PART)
        with self.voiceover("Chapter five. The currency smile: how three quoted numbers become a volatility for every "
                            "strike."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def quotes(self, x):
        rows = [cmath(r"RR_{25}", r"=", r"\sigma_{25c} - \sigma_{25p}", font_size=40, colors={r"RR_{25}": BASIS}),
                cmath(r"BF_{25}", r"=", r"\tfrac12\big(\sigma_{25c} + \sigma_{25p}\big) - \sigma_{\text{ATM}}", font_size=40,
                      colors={r"BF_{25}": GOOD}),
                cmath(r"\sigma_{25c,\,25p}", r"=", r"\sigma_{\text{ATM}} + BF_{25} \pm \tfrac12 RR_{25}", font_size=40)]
        whys = [why("the risk reversal: buy the 25-delta call, sell the 25-delta put. Its price, in vol, is the smile's tilt: relative option-implied wing pricing, not an identified physical jump probability"),
                why("the butterfly: the wings' average over the centre, the smile's curvature: relative wing curvature, affected by pricing-measure tails and premia"),
                why(r"three numbers, ATM, RR and BF, give three pillar volatilities (in the 'smile strangle' "
                    r"convention; brokers also quote a market strangle, a subtlety the next steps ignore)")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        q = x["quotes"]
        tag = MathTex(rf"\text{{ATM}}\ {100 * q['atm']:.2f},\ RR\ {100 * x['rr']:+.2f},\ BF\ {100 * x['bf']:.2f}\ \Rightarrow\ "
                      rf"\sigma_{{25p}} = {100 * q['25p']:.2f}\%,\ \sigma_{{25c}} = {100 * q['25c']:.2f}\%", font_size=28,
                      color=FOR).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In this illustration each tenor has an ATM quote and two wing adjustments. The ATM convention is the unadjusted delta-neutral straddle. <bookmark mark='a'/> The risk reversal is the 25-delta call volatility minus the put volatility. It describes relative option-implied wing pricing, not a uniquely identified physical probability of a jump. <bookmark mark='b'/> The butterfly is the average wing volatility minus ATM under the smile-strangle convention. A market-strangle quote needs a separate conversion. <bookmark mark='c'/> The three numbers then determine our three pillar volatilities. Different smile dynamics can share those pillars, so neither a complete risk-neutral distribution nor future returns are identified by just these quotes."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(tag))
        self.wait(0.4)
        self.clear_scene()

    def strikes(self, x):
        K, q = x["K"], x["quotes"]
        rows = [cmath(r"K_{25c}", r"=", r"F\exp\Big(-\sigma_{25c}\sqrt T\,N^{-1}(0.25) + \tfrac12\sigma_{25c}^2 T\Big)",
                      font_size=34, colors={r"K_{25c}": GOOD}),
                cmath(r"K_{25p}", r"=", r"F\exp\Big(\sigma_{25p}\sqrt T\,N^{-1}(0.25) + \tfrac12\sigma_{25p}^2 T\Big)",
                      font_size=34, colors={r"K_{25p}": BAD})]
        whys = [why(r"invert $N(d_1) = 0.25$ for the strike, using that pillar's own volatility: a quote in delta "
                    r"becomes a strike only once its vol is known"),
                why(rf"here: $K_{{25p}}$ = {K['25p']:.4f}, $K_\text{{DNS}}$ = {K['atm']:.4f}, $K_{{25c}}$ = {K['25c']:.4f}"
                    r", forward deltas")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "The pillars are in delta, not strike, so each must be turned into a strike. Invert the delta formula, "
            "using the pillar's own volatility: a 25-delta call is the strike whose N of d one is a quarter. "
            "<bookmark mark='a'/> For our market the three strikes are "
            f"{K['25p']:.3f}, {K['atm']:.3f} and {K['25c']:.3f} dollars. Delta quotes have a virtue: they move with the "
            "market, so 'the 25-delta risk reversal' means the same thing whatever the level of the euro."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def vv_idea(self):
        rows = [cmath(r"C(K)", r"\approx", r"C^{BS}(K;\sigma_{\text{ATM}}) + \textstyle\sum_{i=1}^{3} x_i(K)\,"
                      r"\big[C^{\text{mkt}}(K_i) - C^{BS}(K_i;\sigma_{\text{ATM}})\big]", font_size=32,
                      colors={r"C(K)": GOOD}),
                cmath(r"\begin{pmatrix}\text{vega}\\ \text{vanna}\\ \text{volga}\end{pmatrix}_{K}", r"=",
                      r"\textstyle\sum_i x_i(K)\begin{pmatrix}\text{vega}\\ \text{vanna}\\ \text{volga}\end{pmatrix}_{K_i}",
                      font_size=30)]
        whys = [why(r"vanna--volga (Castagna and Mercurio, 2007): price any strike flat at the ATM vol, then add the cost "
                    r"of a hedge, three pillar options bought at their market price instead of the flat one"),
                why(r"the weights $x_i$ make the hedge match the option's vega, vanna ($\partial^2 C/\partial S\,\partial"
                    r"\sigma$) and volga ($\partial^2 C/\partial\sigma^2$): the risks the flat model ignores, priced at "
                    r"what the market charges for them")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "Now fill in between. FX desks use a method built from hedging, not from a model of the process: "
            "vanna-volga, as Antonio Castagna and Fabio Mercurio wrote it down. Price any strike at the flat "
            "at-the-money volatility. <bookmark mark='a'/> Then ask what it would cost to hedge the risks a flat "
            "volatility ignores, with the three pillar options: weights that match the option's sensitivity to "
            "volatility, vega; to spot and volatility together, vanna; and to volatility's own moves, volga. Each "
            "pillar is bought at its market price, not the flat one, and the difference is added to the price. The "
            "smile is the market price of vanna and volga."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def vv_plot(self, x):
        Ks, vv = np.asarray(x["Ks"]), 100 * np.asarray(x["vv"])
        K, q = x["K"], x["quotes"]
        g = axes([Ks[0], Ks[-1]], [6.8, 9.6], x_length=7.6, y_length=4.4, xlabel=r"strike, \$ per \texteuro",
                 ylabel=r"implied volatility, \%", xticks=[1.04, 1.08, 1.12, 1.16], yticks=[7, 8, 9], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        flat = DashedLine(ax.c2p(Ks[0], 100 * q["atm"]), ax.c2p(Ks[-1], 100 * q["atm"]), color=GREY_B, stroke_width=1.5)
        line = curve(ax, Ks, vv, GOOD, stroke_width=3.5)
        pts = VGroup(*[Dot(ax.c2p(K[k], 100 * q[k]), color=FOR, radius=0.08) for k in ("25p", "atm", "25c")])
        labs = VGroup(*[label(t_, font_size=15, color=FOR).next_to(ax.c2p(K[k], 100 * q[k]), UP, buff=0.12)
                        for k, t_ in (("25p", r"25-delta put"), ("atm", r"ATM (DNS)"), ("25c", r"25-delta call"))])
        side = VGroup(
            legend([(GOOD, r"vanna--volga smile"), (FOR, r"the three quotes"), (GREY_B, r"flat at ATM")], font_size=17),
            wrapped_label('the curve passes exactly through the three pillars, rises in both wings (the butterfly) and leans to the left (the risk reversal: euro puts dearer). Outside the three quoted strikes it is an extrapolation, and desks add 10-delta quotes for the tails', 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The result. <bookmark mark='a'/> The three quoted points. <bookmark mark='b'/> The vanna-volga smile "
            "passes through each exactly, rises in both wings by the butterfly, and leans to the left by the risk "
            "reversal: insurance against a falling euro costs more than a bet on a rising one. It is smooth, cheap "
            "to compute, and needs nothing but the three quotes the market already shows, which is why every FX "
            "pricing system has it. Far in the wings it is an extrapolation, and desks add a second set of quotes at "
            "ten delta to pin the tails."
        ) as vo:
            self.play(FadeIn(g), Create(flat), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(pts), FadeIn(labs))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[1]), run_time=2)
        self.add(illustration(r"illustrative quotes; the House's quoting.vanna\_volga"))
        self.wait(0.4)
        self.clear_scene()

    def term(self, x):
        tm = x["term"]
        g = axes([-1.7, 1.7], [6.6, 10.4], x_length=7.4, y_length=4.4,
                 xlabel=r"moneyness, $\ln(K/F)/(\sigma_{\text{ATM}}\sqrt T)$", ylabel=r"implied volatility, \%",
                 xticks=[-1.5, -1, -0.5, 0, 0.5, 1, 1.5], yticks=[7, 8, 9, 10], font_size=13).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        cols = [GREY_B, FOR, GOOD, USD, BASIS]
        names = [r"1 week", r"1 month", r"3 months", r"6 months", r"1 year"]
        lines = VGroup(*[curve(ax, np.asarray(t_["z"]), 100 * np.asarray(t_["vol"]), c_, stroke_width=2.8)
                         for t_, c_ in zip(tm, cols)])
        side = VGroup(
            legend(list(zip(cols, names)), font_size=16),
            wrapped_label(r"illustrative quotes rising with tenor: ATM from 7.0\% to 7.9\%, risk reversal from $-0.3$ to "
                          r"$-0.9$, butterfly from 0.12 to 0.35. Each tenor's smile from its own three quotes; the "
                          r"desk's surface is these curves, interpolated in time", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "A desk can quote ATM, reversal and butterfly at several tenors. <bookmark mark='a'/> Our five sets of inputs are invented, and each curve is an independent vanna-volga illustration. Higher annualized volatility is not mechanically implied by having more time. Moneyness normalization helps compare shapes, but this display does not fit a joint stochastic process. <bookmark mark='b'/> Interpolating total variance is useful, yet it alone does not guarantee absence of calendar or butterfly arbitrage. One must check call-price bounds and convexity, consistent forwards, rates, strikes and maturities. Likewise three fitted pillars do not certify the tails or a barrier price; those require additional quotes and model assumptions."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def why_vv(self):
        cards = VGroup(
            desk_question(r"why not a model?", 'Heston or SABR (Parts 13 and 19) fit the same three quotes with a process behind them, provide candidate dynamics for path-dependent valuation, with calibration and model risk remaining; vanna--volga cannot', width=12.0, font_size=21),
            desk_question(r"why it survives", r"it is a hedging argument a trader can check: every number in it is a "
                          r"Black--Scholes Greek or a market quote", width=12.0, font_size=21),
            desk_question(r"barriers", r"for a knock-out, the vanna and volga costs are weighted by the probability of "
                          r"surviving: a common desk adjustment, and a source of model risk (Part 15)", width=12.0,
                          font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Why use a dynamic model? <bookmark mark='a'/> Heston or an appropriate SABR specification supplies candidate dynamics, so barrier valuation can refer to a specified path law. Fitting three vanilla quotes does not identify that law or ensure a reliable barrier price. <bookmark mark='b'/> Vanna-volga is transparent: its correction uses Greeks and pillar prices. It is a local interpolation heuristic, without a general guarantee of static arbitrage freedom or consistent paths. <bookmark mark='c'/> Survival-weighted barrier corrections add further conventions and model risk. A desk must check both the vanilla surface and the path-dependent product, rather than treating an exact pillar fit as a valuation certificate."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"the euro's 25-delta risk reversal moves from $-0.6$ to $-2.0$ overnight while ATM is unchanged. What "
                r"has the market started to fear, and who pays?")
        with self.voiceover("The euro's risk reversal moves from minus point six to minus two overnight, with at-the-money "
                            "unchanged. What has the market started to fear, and who pays?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
