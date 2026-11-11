from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, load, pause, real_data, simulated


class Industry(VoiceoverScene):
    def construct(self):
        mv = load("mv_delta")
        hh = load("heston_hedge")
        env = load("envelope")
        self.card()
        self.firms()
        self.derive()
        self.race(mv)
        self.simworld(hh)
        self.races_and_risk()
        self.module(env)

    def card(self):
        c = chapter_card(17, r"Industry: who builds these models, and how desks judge them",
                         r"Is a model judged by its fit, or by its hedge?", lit=(2004, 2012), part=PART)
        with self.voiceover("Chapter seventeen. The industry: who builds these models, and how a desk judges one."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c), run_time=0.35)

    def firms(self):
        f1 = firm_card(r"Soci\'et\'e G\'en\'erale, equity derivatives research",
                       "Historical equity-derivatives research at Soci\\'et\\'e G\\'en\\'erale: Bergomi's Smile Dynamics; Guyon and Henry-Labord\\`ere's particle method. Risk awards: Henry-Labord\\`ere (2023), Guyon (2025, joint calibration with Mustapha).",
                       source=r"risk.net award pages; publishers' author biographies", width=6.4, font_size=21)
        f2 = firm_card(r"Cboe and Deribit: volatility as an asset",
                       r"Cboe listed VIX futures on 26 March 2004 and VIX options on 24 February 2006: volatility "
                       r"acquired its own smile, and chapter 15's puzzle became a market fact. Deribit's DVOL plays the "
                       r"same role for bitcoin (Part 12).", source=r"Cboe; Deribit", width=5.6, font_size=21)
        G = VGroup(f1, f2).arrange(RIGHT, buff=0.35, aligned_edge=UP)
        if G.width > 13.2:
            G.scale_to_fit_width(13.2)
        with self.voiceover(
            (
            """Bank research groups developed many of these methods alongside academic work. Bergomi's Smile Dynamics papers, and Guyon and Henry-Labordère's particle method, were closely connected with equity-derivatives practice at Société Générale. Henry-Labordère received a 2023 Risk quant award; Guyon received a 2025 award for joint-calibration work with Mustapha. These are historical affiliations and research contributions, not a statement of everyone's current employment. <bookmark mark='a'/> Exchanges also created tradable volatility markets: Cboe lists VIX derivatives. Deribit's DVOL is a Bitcoin implied-volatility index, with its own construction and product ecosystem; that does not make this calculation a Bitcoin VIX-option calibration."""
        )
        ) as vo:
            self.play(FadeIn(f1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(f2, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def derive(self):
        rows = [cmath(r"\Delta_{\text{MV}}", r"=", r"\frac{\operatorname{Cov}(dC,\ dS)}{\operatorname{Var}(dS)}", font_size=38,
                      colors={r"\Delta_{\text{MV}}": OPT}),
                cmath(r"dC", r"\approx", r"C_S\,dS + C_\sigma\,d\sigma", font_size=38, colors={r"dC": OPT}),
                cmath(r"\Delta_{\text{MV}}", r"=", r"C_S + C_\sigma\,\frac{\mathbb{E}[d\sigma \mid dS]}{dS} = \Delta_{\text{BS}} + "
                      r"\text{vega}\cdot\frac{\beta}{S}", font_size=36, colors={r"\Delta_{\text{MV}}": OPT}),
                cmath(r"\text{Heston:}\ \ \Delta_{\text{MV}}", r"=", r"C_S + C_v\,\frac{\rho\,\xi}{S}", font_size=36,
                      colors={r"\text{Heston:}\ \ \Delta_{\text{MV}}": MODEL_COL["Heston"]})]
        whys = [why(r"the hedge ratio that minimises the variance of the hedged P\&L: regress the option's change on the "
                    r"spot's", 20),
                why(r"to first order the option moves with the spot and with its implied vol", 20),
                why(r"so add vega times the expected vol move per unit of spot: $\beta$ is the slope of $d\sigma$ on "
                    r"$dS/S$ (Hull and White 2017)", 20),
                why(r"in Heston, $\mathbb{E}[dv \mid dS] = \rho\xi\,dS/S$ (chapter 13's regression): the same idea as "
                    r"Bartlett's SABR delta", 20)]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.8, buff=0.6, edge=6.9)
        pp = pause("For a positive-vega call and negative spot--IV beta, is the minimum-variance delta above or below Black's delta?",
                   width=5.0).to_corner(DR, buff=0.3)
        with self.voiceover(
            (
            """A desk evaluates pricing error, hedge behavior and numerical reliability together. The local minimum-variance hedge regresses option changes on spot changes. <bookmark mark='a'/> With a Black price proxy, first-order changes include delta times spot and vega times implied volatility. <bookmark mark='b'/> If beta is the regression coefficient of implied-vol change on fractional spot return, the adjustment is vega beta over S. <bookmark mark='c'/> In Heston the exact instantaneous model expression uses the variance Greek: C sub S plus C sub v times rho xi over S. Replacing variance sensitivity by a volatility Greek requires the corresponding chain factor. <bookmark mark='d'/> For a positive-vega call and negative beta, the Black-proxy minimum-variance delta is lower. This is a local covariance argument, not a universal forecast or a guarantee for discrete hedging."""
        )
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(pp))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def race(self, mv):
        rc = mv["race"]
        t = np.asarray(rc["t"])
        cb, cm = np.asarray(rc["cum_bs"]), np.asarray(rc["cum_mv"])
        top = float(max(cb[-1], cm[-1]))
        g = axes([t[0], t[-1]], [0, top * 1.05], x_length=7.2, y_length=4.0, ylabel=r"cumulative squared hedge error",
                 xticks=[2022, 2023, 2024, 2025], yticks=[], font_size=15).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        tr = ValueTracker(t[1])

        def ln(y, col):
            def mk():
                k = max(int(np.searchsorted(t, tr.get_value())), 2)
                return VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(
                    [ax.c2p(a, b) for a, b in zip(t[:k:2], y[:k:2])] + [ax.c2p(t[k - 1], y[k - 1])])
            return always_redraw(mk)

        lb, lm = ln(cb, MODEL_COL["BS"]), ln(cm, OPT)
        leg = legend([(MODEL_COL["BS"], r"Black--Scholes delta"), (OPT, r"minimum-variance delta, rolling 60-day $\beta$")],
                     font_size=17).next_to(g, UP, buff=0.12).align_to(g, LEFT)
        fx = mv["fixed"]
        ro = mv["rolling"]
        side = VGroup(
            wrapped_label('Synthetic 30-day ATM Black proxy aged to 29 days; DVOL input, no executable option marks, transaction costs or funding.', 4.4, 17, GREY_A),
            MathTex(rf"\beta\ \text{{fixed from 2021--22:}}", font_size=24, color=GREY_A),
            MathTex(rf"\text{{in sample}}\ {100 * fx['in']:+.0f}\%,\ \ \text{{2023--25}}\ {100 * fx['out']:+.0f}\%",
                    font_size=26, color=RV if fx["out"] > 0 else BAD),
            MathTex(r"\text{rolling}\ \beta:\ " + r",\ ".join(rf"{w}\text{{d}}\ {100 * ro[w]['all']:+.0f}\%" for w in ("60", "90", "180", "365")),
                    font_size=22, color=OPT),
            label(r"variance reduction against Black--Scholes", font_size=17, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        v_fix = (f"Fit beta on 2021 and 2022, when falls came with volatility spikes, and the hedge-error variance "
                 f"drops by {100 * fx['in']:.0f} percent in sample. Then carry it into 2023 to 2025, when the leverage "
                 f"effect weakened and flipped, and the error variance rises by {100 * -fx['out']:.0f} percent."
                 if fx["out"] < 0 < fx["in"] else
                 f"A beta fitted on 2021 and 2022 changes the error variance by {100 * fx['in']:+.0f} percent in sample "
                 f"and {100 * fx['out']:+.0f} percent afterwards.")
        best = max(ro, key=lambda w: ro[w]["all"])
        v_roll = (f"Re-estimate beta every day from the last sixty days, and it helps over the whole period: "
                  f"{100 * ro['60']['all']:.0f} percent less variance; {100 * ro[best]['all']:.0f} at best across "
                  "windows. Modest, and not in every year." if ro["60"]["all"] > 0 else
                  f"Even a rolling sixty-day beta does not help overall: {100 * ro['60']['all']:+.0f} percent.")
        src = real_data(r"Binance BTCUSDT and Deribit DVOL daily, 2021--2025; Black--Scholes marks at DVOL")
        with self.voiceover(
            (
            f"""This is a synthetic daily hedge exercise driven by Bitcoin spot and DVOL. Each day creates a thirty-day ATM Black call proxy, aged to twenty-nine days tomorrow, rather than tracking executable option marks. It omits transaction costs and funding. Mean deltas are {rc['mean_mv']:.2f} and {rc['mean_bs']:.2f}. <bookmark mark='a'/> {v_fix} <bookmark mark='b'/> {v_roll} Rolling coefficients use strictly prior observations. Window comparisons are descriptive, not a new selected trading strategy or an untouched holdout test. <bookmark mark='c'/> The exercise shows sensitivity to the estimation period and the proxy's assumptions. It neither demonstrates realized option-trading performance nor directly tests SABR's Bartlett delta. The trial counter is unchanged."""
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src), FadeIn(side[0]))
            self.add(lb, lm)
            self.play(tr.animate.set_value(t[-1]), run_time=max(vo.until("a") - 0.3, 4), rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        lb.clear_updaters()
        lm.clear_updaters()
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def simworld(self, hh):
        names = [("BS", r"Black--Scholes delta at the option's implied vol", MODEL_COL["BS"]),
                 ("Heston", r"Heston's delta, $C_S$", MODEL_COL["Heston"]),
                 ("MV", r"minimum-variance, $C_S + C_v\rho\xi/S$", OPT)]
        g = axes([-0.5, 2.5], [0, 0.03], x_length=6.0, y_length=3.8, ylabel=r"s.d.\ of the hedge error, per unit of spot",
                 xticks=[], yticks=[0, 0.01, 0.02, 0.03], yfmt=lambda u: f"{u:.2f}", font_size=15).to_edge(LEFT, buff=0.8)
        ax = g.ax
        bars = VGroup()
        for i, (k, lab, col) in enumerate(names):
            v = hh[k]["sd"]
            b = Rectangle(width=0.7, height=abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to(ax.c2p(i, v / 2))
            bars.add(VGroup(b, MathTex(f"{v:.4f}", font_size=22).next_to(b, UP, buff=0.08),
                            wrapped_label(lab, 1.8, 15, col).next_to(ax.c2p(i, 0), DOWN, buff=0.15)))
        best = min(names, key=lambda n: hh[n[0]]["sd"])[0]
        side = VGroup(
            MathTex(rf"\text{{unhedged:}}\ {hh['unhedged_sd']:.3f}", font_size=28, color=GREY_A),
            MathTex(rf"\text{{mean delta: BS}}\ {hh['BS']['mean_delta']:.2f},\ \text{{Heston}}\ {hh['Heston']['mean_delta']:.2f},"
                    rf"\ \text{{MV}}\ {hh['MV']['mean_delta']:.2f}", font_size=24, color=GREY_A),
            wrapped_label('Residual: orthogonal variance shocks, daily hedging and numerical error. About 90\\% of unhedged variance is removed here.', 4.6, 18, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        gap = 100 * (hh["BS"]["sd"] - hh["MV"]["sd"]) / hh["BS"]["sd"]
        v = (f"The minimum-variance delta is best, but only by {gap:.1f} percent over Black and Scholes at the "
             "option's own implied volatility." if best == "MV" else
             f"Here the {best} delta is best; the minimum-variance delta does not win.")
        v2 = ("Heston's own delta, which holds the variance fixed, is the worst of the three: it ignores the "
              "correlated move of volatility that the model itself predicts." if hh["Heston"]["sd"] > max(hh["BS"]["sd"], hh["MV"]["sd"])
              else "Heston's own delta is not the worst here.")
        src = simulated(r"the fitted Heston, 2{,}000 paths, a 30-day ATM call hedged daily; prices from a COS grid in $(\ln S, v)$")
        with self.voiceover(
            (
            f"""Use two thousand simulated Heston paths and daily hedges of a thirty-day call. This is a numerical model experiment: prices come from an interpolated COS grid, with log-price extrapolation and variance clamping. <bookmark mark='a'/> {v} <bookmark mark='b'/> {v2} Unhedged standard deviation is {hh['unhedged_sd']:.3f}, versus {hh['MV']['sd']:.3f} for the minimum-variance hedge. That removes roughly ninety percent of unhedged variance here, rather than leaving most risk. Residual error includes orthogonal variance shocks, discrete hedging, grid approximation and simulation effects. Additional instruments can hedge variance exposure, but this calculation does not isolate every residual component."""
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), LaggedStart(*[FadeIn(b_[2]) for b_ in bars], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_[0], DOWN) for b_ in bars], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(b_[1]) for b_ in bars], lag_ratio=0.3), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def races_and_risk(self):
        c1 = history_card(1997, r"Bakshi, Cao and Chen, \textit{Journal of Finance}",
                          r"A horse race on S\&P 500 options: stochastic volatility with jumps priced best; for hedging, "
                          r"stochastic volatility alone was enough.", color=QC.IDEA, width=4.1)
        c2 = history_card(2023, r"Matic, Packham and H\"ardle, \textit{Rev.\ Derivatives Research}",
                          r"``Hedging cryptocurrency options'': calibration on bitcoin points to stochastic volatility with "
                          r"few jumps; for longer-dated options, multi-instrument hedges and SV models cut tail risk.",
                          color=QC.IDEA, width=4.1)
        c3 = history_card(2016, r"Model risk as capital (EU 2016/101, Art.\ 11)",
                          'Article 11: prudent model-risk exit value at 90\\% confidence using plausible models and calibrations. Five-model min--max is not that confidence calculation.', color=QC.CRISIS, width=4.1)
        G = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        if G.width > 13.2:
            G.scale_to_fit_width(13.2)
        with self.voiceover(
            (
            """Published comparisons are specific to datasets and methods. Bakshi, Cao and Chen's S&P study found different benefits for pricing and hedging from adding jumps. <bookmark mark='a'/> Matic, Packham and Härdle's Bitcoin study reports low jump frequency alongside infinite-activity models, and benefits from some multi-instrument hedges. Its reconstructed option data and designs differ from our synthetic proxy. <bookmark mark='b'/> EU prudent-valuation Article eleven addresses model-risk adjustments using plausible models and calibrations, targeting a ninety-percent prudent exit value. Our five-model minimum-to-maximum price range is not that confidence calculation. Unequal fits and numerical errors must first be reconciled, and a reserve needs a defensible model population and valuation procedure."""
        )
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c3, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def module(self, env):
        chart = house_chart(PART, lit=("vol",)).scale(0.6).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{heston\_cf}, \texttt{bates\_cf}, \texttt{vg\_cf}, \texttt{nig\_cf}, \texttt{cgmy\_cf}, Merton, Kou",
             r"characteristic functions, martingale-checked"),
            (r"\texttt{cos\_price}, \texttt{merton\_series}", r"Fourier pricing; Heston benchmark to $10^{-8}$"),
            (r"\texttt{calibrate}, \texttt{calibrate\_reg}", r"fits with traces, fixed parameters, regularisation"),
            (r"\texttt{sabr\_iv}, \texttt{sabr\_pde\_density}", r"Hagan's formula and arbitrage-free SABR"),
            (r"\texttt{heston\_qe}, \texttt{bates\_paths}, \texttt{vg\_paths}", r"simulators, checked against COS"),
            (r"\texttt{slv\_paths}", r"the particle method, any mixing fraction"),
            (r"\texttt{heston\_vix\_options}, \texttt{heston\_forward\_start}", r"the vol index and the forward smile"),
            (r"\texttt{forward\_start}, \texttt{cliquet}, \texttt{mv\_delta}", r"exotics and the hedge"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=18, color=QC.HOUSE), label(b, font_size=18, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        with self.voiceover(
            (
            "The House's volatility desk now runs all of this. <bookmark mark='a'/> Characteristic functions for "
            "every model, martingale-checked; Fourier pricing matched to the benchmark and to Merton's series; a "
            "calibrator that records its path, fixes parameters and regularises; arbitrage-free SABR; simulators, "
            "particles, the vol index, forward smiles, and the minimum-variance hedge. Each has a test."
            " Last, the frontier."
        )
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=7))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)
