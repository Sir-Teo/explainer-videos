from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data, predict


class Industry(VoiceoverScene):
    def construct(self):
        ind = load("industry")
        self.card()
        self.riskmetrics(ind)
        self.barra(ind)
        self.targeting(ind)
        self.options(ind)

    def card(self):
        c = chapter_card(17, r"Industry: volatility forecasting for money",
                         r"What do risk vendors, CTAs and options desks actually run?", lit=(1994,), part=PART)
        with self.voiceover("Chapter seventeen. How the industry forecasts volatility."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def riskmetrics(self, ind):
        card = firm_card(r"RiskMetrics (J.P.\ Morgan, 1994)",
                         r"launched in October 1994 with its data free on the internet; Reuters partnership in 1996; the "
                         r"\textit{Technical Document}, 4th edition, December 1996; spun off as RiskMetrics Group, which "
                         r"MSCI acquired in June 2010",
                         numbers=[(r"0.94", r"decay factor for daily forecasts"), (r"0.97", r"for monthly forecasts"),
                                  (r"\$1.55\text{bn}", r"MSCI's price, 2010 (SEC filing)")],
                         source=r"RiskMetrics Technical Document (1996), sec.\ 5.2--5.3; MSCI press release, 2010",
                         width=6.4, font_size=21).to_corner(UL, buff=0.3)
        lams = np.asarray(ind["lams"])
        rm, ql = np.asarray(ind["rmse"]), np.asarray(ind["qlike"])
        f = lambda v: (v - v.min()) / (v.max() - v.min())  # noqa: E731
        g = axes([0.85, 1.0], [0, 1.05], x_length=5.4, y_length=3.2, xticks=[0.85, 0.9, 0.94, 0.97, 1.0],
                 xfmt=lambda v: f"{v:g}", yticks=[], xlabel=r"decay factor $\lambda$", ylabel=r"loss, rescaled",
                 font_size=15).to_corner(DR, buff=0.5)
        l1 = curve(g.ax, lams, f(rm), BAD, stroke_width=3)
        l2 = curve(g.ax, lams, f(ql), GOOD, stroke_width=3)
        m1 = Dot(g.ax.c2p(ind["lam_rmse"], 0), radius=0.08, color=BAD)
        m2 = Dot(g.ax.c2p(ind["lam_qlike"], 0), radius=0.08, color=GOOD)
        at_edge = ind["lam_rmse"] <= lams[0] + 1e-9  # the squared error's optimum may lie below the grid
        leg = legend([(BAD, (rf"RMSE of daily variance: lowest at the grid's edge, {lams[0]:.2f}" if at_edge else
                             rf"RMSE of daily variance: best at {ind['lam_rmse']:.3f}")),
                      (GOOD, rf"QLIKE, weekly: best at {ind['lam_qlike']:.3f}")], font_size=17).next_to(g, UP, buff=0.15)
        pc = predict(r"Why one $\lambda$ for some 480 series, instead of 480 $\lambda$s?", width=5.4, font_size=21)
        pc.to_corner(UR, buff=0.3)
        edge = ind["lam_rmse"] <= lams[0] + 1e-9
        rmse_line = ("daily-variance RMSE is smallest at the left edge of our grid; this does not locate the optimum outside it" if edge else f"the squared error picks {ind['lam_rmse']:.2f}")
        qlike_line = f"It picks {ind['lam_qlike']:.2f}, J.P. Morgan's number."
        with self.voiceover(
            f"""In October 1994 J.P. Morgan published RiskMetrics. Its daily variance recursion uses decay point nine four; point nine seven was used for monthly forecasts. MSCI acquired the business in 2010. <bookmark mark='a'/> A common decay preserves positive semidefiniteness, with positive definiteness under suitable initialization. Arbitrary entrywise decays can break it; structured heterogeneous models can still be valid. <bookmark mark='b'/> In our US-market grid, {rmse_line}. Weekly QLIKE: {qlike_line} Both the loss and horizon differ, so this is not an isolated experiment on loss functions."""
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(pc))
            vo.wait_until("b")
            self.play(FadeOut(pc), FadeIn(g), FadeIn(leg), Create(l1), Create(l2), FadeIn(m1), FadeIn(m2))
        self.wait(0.3)
        self.clear_scene()

    def barra(self, ind):
        quote = VGroup(
            label(r"MSCI Barra USE4 (2011), from MSCI's own descriptions:", font_size=21, color=QC.FIRM),
            wrapped_label(r"``a longer half-life for factor correlation estimates than for factor volatility estimates'', "
                          r"so the covariance matrix stays well-conditioned", 6.2, 19, GREY_A),
            wrapped_label(r"the Volatility Regime Adjustment ``scales factor volatilities based on a time-series of "
                          r"cross-sectional factor bias statistics''", 6.2, 19, GREY_A),
            label(r"MSCI, \textit{Market Factor: Not Just For Show}, Dec.\ 2011", font_size=16, color=GREY_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UL, buff=0.35)
        rows = [cmath(r"B_t^2", r"=", r"\frac1K\sum_k\Big(\frac{f_{kt}}{\sigma_{kt}}\Big)^2,\quad "
                      r"\lambda_t^2 = \operatorname{EWMA}_{t-1}(B^2),\quad \sigma'_{kt} = \lambda_t\sigma_{kt}", font_size=30)]
        rows[0].next_to(quote, DOWN, buff=0.4).align_to(quote, LEFT)
        rl = label(r"our replica in that spirit (not MSCI's published formula); our half-lives", font_size=17, color=GREY_B)
        rl.next_to(rows[0], DOWN, buff=0.1).align_to(rows[0], LEFT)
        t, lam = np.asarray(ind["vra_t"]), np.asarray(ind["vra"])
        g = axes([1926, 2021], [0, 3], x_length=6.0, y_length=2.8, xticks=[1930, 1960, 1990, 2020], xfmt=lambda u: f"{int(u)}",
                 yticks=[0, 1, 2, 3], ylabel=r"$\lambda_t$ on the ten size deciles", font_size=15).to_corner(DR, buff=0.4)
        line = curve(g.ax, t, lam, FC, stroke_width=1.8)
        one = DashedLine(g.ax.c2p(1926, 1), g.ax.c2p(2021, 1), color=GREY_B, stroke_width=2)
        pk = ind["vra_peaks"]
        res = MathTex(rf"\text{{QLIKE: }} {ind['q_raw']:.3f} \to {ind['q_adj']:.3f}", font_size=28, color=GOOD)
        res.next_to(g, UP, buff=0.15)
        vra_line = ("It lowers this historical QLIKE; the multiplier uses only prior-day standardized returns, after initialization."
                    if ind["q_adj"] < ind["q_raw"] else "Here it does not improve QLIKE.")
        with self.voiceover(
            f"Factor risk models face this at scale. MSCI's Barra US equity model of 2011, by MSCI's account, estimates "
            f"correlations with a longer half-life than volatilities, to keep the matrix well-conditioned, and adds a "
            f"volatility regime adjustment that scales every factor's volatility by a time series of cross-sectional bias "
            f"statistics. <bookmark mark='a'/> We could not retrieve the exact formula, so here is a replica in that spirit: "
            f"average each day's squared ratios of return to forecast volatility across portfolios, and smooth. When forecasts "
            f"run too low, the multiplier rises above one. <bookmark mark='b'/> On the ten size portfolios it spikes in "
            f"the Depression, to {pk['1929']:.1f}, in 1987, to {pk['1987']:.1f}, and in 2020, to {pk['2020']:.1f}. {vra_line}"
        ) as vo:
            self.play(FadeIn(quote))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(g), Create(one), Create(line), FadeIn(res), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    def targeting(self, ind):
        hist = VGroup(
            label(r"Harvey, Hoyle, Korgaonkar, Rattray, Sargaison and Van Hemert (Man AHL), JPM 2018:", font_size=19, color=QC.FIRM),
            wrapped_label(r"scale each asset to a 10\% volatility target using $\sigma_{t-2}$: Sharpe ratios rise for "
                          r"equities and credit (the leverage effect), barely change for bonds, FX and commodities; left "
                          r"tails shrink everywhere", 6.4, 18, GREY_A),
            wrapped_label(r"Moskowitz, Ooi and Pedersen (2012): each futures position sized to 40\% ex-ante volatility, "
                          r"from an exponential average with a 60-day centre of mass; Moreira and Muir (2017)", 6.4, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UL, buff=0.35)
        t, w = np.asarray(ind["vt_t"]), np.asarray(ind["vt_w"])
        g = axes([1927, 2021], [0, 3], x_length=6.0, y_length=2.2, xticks=[1930, 1960, 1990, 2020], xfmt=lambda u: f"{int(u)}",
                 yticks=[0, 1, 2, 3], ylabel=r"position in the US market, 10\% target", font_size=14).to_corner(DL, buff=0.4)
        wl = curve(g.ax, t, w, GOOD, stroke_width=1.5)
        a, b = ind["vt_scaled"], ind["vt_plain"]
        cells = [VectorizedPoint(), label(r"plain", font_size=20, color=GREY_B), label(r"targeted", font_size=20, color=GREY_B),
                 label(r"Sharpe", font_size=22), MathTex(f"{b['sharpe']:.2f}", font_size=28), MathTex(f"{a['sharpe']:.2f}", font_size=28, color=GOOD),
                 label(r"worst 1\% of days, mean", font_size=22), MathTex(rf"{100 * b['es1']:.2f}\%", font_size=28),
                 MathTex(rf"{100 * a['es1']:.2f}\%", font_size=28, color=GOOD),
                 label('max additive drawdown', font_size=22), MathTex(f"{b['maxdd_log']:.2f}", font_size=28),
                 MathTex(f"{a['maxdd_log']:.2f}", font_size=28, color=GOOD)]
        tab = VGroup(*cells).arrange_in_grid(rows=4, cols=3, buff=(0.45, 0.18), col_alignments="lrr").to_corner(DR, buff=0.5)
        note_ = label(r"French's market excess return 1927--2020; the plain market scaled to the same volatility",
                      font_size=16, color=GREY_C).next_to(tab, DOWN, buff=0.15).align_to(tab, RIGHT)
        vt_line = (f"The Sharpe ratio rises from {b['sharpe']:.2f} to {a['sharpe']:.2f}, the worst days are milder, and "
                   "the deepest drawdown is much shallower. This descriptive example improves gross risk-adjusted performance without a directional forecasting signal; costs and another period could change it." if a["sharpe"] > b["sharpe"] else
                   "Here the Sharpe ratio does not improve.")
        with self.voiceover(
            f"""Trend followers lean heavily on volatility forecasts. Harvey and coauthors studied volatility scaling; Moskowitz, Ooi and Pedersen used a sixty-day center-of-mass estimate for sizing. <bookmark mark='a'/> Our descriptive US example uses a two-day lag, a ten-times leverage cap, and a ten-percent volatility target. It is gross of trading and funding costs. The plain benchmark is rescaled to the same full-period volatility after the fact. {vt_line} The drawdown is on cumulative simple excess returns, not compounded or log wealth."""
        ) as vo:
            self.play(FadeIn(hist))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(wl), run_time=2)
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def options(self, ind):
        t, vx, fr = (np.asarray(ind[k]) for k in ("vix_t", "vix", "fwd_rv"))
        g = axes([1990, 2021], [0, 105], x_length=7.4, y_length=3.6, xticks=[1990, 2000, 2010, 2020], xfmt=lambda u: f"{int(u)}",
                 yticks=[0, 30, 60, 90], ylabel=r"the VIX against the next month's realized volatility (\%)", font_size=15)
        g.to_edge(LEFT, buff=0.5).shift(UP * 0.4)
        lr = curve(g.ax, t, fr, RET, stroke_width=1.3)
        lv = curve(g.ax, t, vx, ALT, stroke_width=1.6)
        leg = legend([(ALT, r"VIX (Cboe): implied, 30 days"), (RET, r"realized over the next 21 trading days")], font_size=17)
        leg.next_to(g, DOWN, buff=0.15).align_to(g, LEFT)
        mzv, mzg, en = ind["mz_vix"], ind["mz_garch"], ind["encompass"]
        side = VGroup(
            MathTex(rf"\text{{VIX above realized: }} {100 * ind['share_vix_above']:.0f}\%\text{{ of days}}", font_size=26, color=ALT),
            MathTex(rf"\text{{average gap: }} {ind['vrp_mean']:.1f}\text{{ vol points}}", font_size=26, color=ALT),
            label(r"forecasting next month's realized:", font_size=19, color=GREY_A),
            MathTex(rf"\text{{VIX alone: }} R^2 = {mzv['r2']:.2f};\ \ \text{{GARCH alone: }} {mzg['r2']:.2f}", font_size=24),
            MathTex(rf"\text{{both: VIX }} {en['b_vix']:.2f}\ (t = {en['t_vix']:.1f}),\ \text{{GARCH }} {en['b_garch']:.2f}\ "
                    rf"(t = {en['t_garch']:.1f})", font_size=24),
            wrapped_label(r"the variance risk premium (Carr and Wu 2009); implied against realized (Christensen and "
                          r"Prabhala 1998); NYU's V-Lab publishes GARCH forecasts daily; AQR's ``Risk everywhere'' "
                          r"(Bollerslev, Hood, Huss and Pedersen 2018) runs HAR-type models across asset classes",
                          5.0, 17, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3)
        both_line = ("Both coefficients are significant in this in-sample HAC regression; that is not independent forecast validation." if en["t_garch"] > 2 and en["t_vix"] > 2 else "At least one coefficient is not significant here; non-rejection does not establish no incremental information.")
        with self.voiceover(
            f"""Options desks have a forecast in prices. VIX is the S-and-P-five-hundred's thirty-calendar-day implied index; our realized proxy uses French's broader US market over 21 trading days. <bookmark mark='a'/> VIX exceeds that proxy on {100 * ind['share_vix_above']:.0f} percent of observations, by {ind['vrp_mean']:.0f} volatility points on average. This gap does not identify a variance risk premium: expectations, squares, horizons and index alignment matter. <bookmark mark='b'/> Retrospective regression R squared is {100 * mzv['r2']:.0f} percent for VIX and {100 * mzg['r2']:.0f} for GARCH. {both_line} GARCH parameters fit pre-1990, but demeaning uses the research sample; overlapping outcomes use HAC errors. These are descriptive associations, not a fresh point-in-time validation."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), Create(lr), Create(lv), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[:2]))
            vo.wait_until("b")
            self.play(FadeIn(side[2:]))
        self.wait(0.3)
        self.clear_scene()
