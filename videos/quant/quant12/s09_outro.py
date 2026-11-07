from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, load

DESK = [
    (r"Why is the VIX above realized volatility on average?",
     r"because variance is insurance: it spikes when wealth falls, so its buyers pay a premium (Carr and Wu 2009); on "
     r"bitcoin since 2021, the 30-day variance strike exceeded realized variance in about four weeks out of five"),
    (r"Replicate a variance swap with options.",
     r"hold $\frac{2}{T}\frac{\Delta K}{K^2}$ of every out-of-the-money option (puts below the forward, calls above) and "
     r"hold $\frac{2}{T}\big(\frac{1}{S_t} - \frac1F\big)$ of the asset, rebalanced on the contract's own clock; jumps "
     r"leave a cubic error"),
    (r"Spot falls 5\%. Where does ATM vol go under sticky strike, sticky delta, and local vol?",
     r"sticky strike: up by $5\%$ times the skew (it slides down the curve); sticky delta: unchanged; local vol: up by "
     r"about twice the sticky-strike move ($R \approx 2$)"),
]

PROBLEMS = [
    r"From $C(K, T)$ and the forward equation, derive Dupire's formula $\sigma^2_{loc} = \partial_T C / (\frac12 K^2 "
    r"\partial_{KK} C)$ at zero rates.",
    r"Show that $-\log(S_T/F)$ equals a forward position plus a strip of options weighted $1/K^2$, and hence derive "
    r"the variance-swap strike.",
    r"For SSVI with the power-law $\varphi$, check Gatheral and Jacquier's calendar condition, and find the smallest "
    r"$\theta$ above which their butterfly condition holds when $\gamma > \frac12$.",
    r"Show that near the money, local-volatility skew is about twice the implied skew: $\partial_k\sigma_{loc} "
    r"\approx 2\,\partial_k\sigma_{imp}$.",
    r"Derive Martin's bound: if $\text{cov}(m_T R_T, R_T) \le 0$, then $\mathbb{E}[R_T] - R_f \ge \text{var}^Q(R_T)/R_f$.",
    r"Derive Gatheral's $g(k)$ from Black's formula written in total variance $w$ and log-moneyness $k$.",
    r"Show that $K_{vol} \approx \sqrt{K_{var}} - \text{Var}(V)/(8K_{var}^{3/2})$ for a volatility swap.",    r"(qual) Show that the butterfly estimate $\hat q_h$ has bias $\frac{h^2}{12}q'' + O(h^4)$ and, with independent price "
    r"errors of variance $s^2$, variance $6s^2/h^4$; find $h^*$ and show $\operatorname{MSE}_{\rm lead}(h^*) = \frac{\sqrt6}{6}|q''|s$.",
    '(qual) With a common price error $\\eta_0$ plus independent errors, show $\\eta_0$ cancels in $\\hat q_h$. Now let adjacent errors have correlation $\\rho$ and the outer pair be uncorrelated, with $|\\rho|\\le1/\\sqrt2$; derive $\\operatorname{Var}(\\hat q_h)=(6-8\\rho)s^2/h^4$.',
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("termskew"), load("dynamics"), load("ssvi_replay"), load("lv_mc"), load("replication"),
                   load("vrp_pnl"), load("vx_etp"), load("neural_surface"))
        self.rule(load("envelope"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, t, d, s, m, r, p, x, n):
        import numpy as np
        items = [
            (rf"the smile gives local distributional clues; bitcoin was call-skewed in {100 * t['call_skew']:.0f}\% of "
             rf"weeks", IV),
            (rf"surfaces move in three shapes: level, skew, term ({100 * sum(d['explained'][:3]):.0f}\% of weekly moves)", SPOT),
            ("static-arbitrage checks: density and tail boundary, calendar monotonicity, and Lee's necessary wing bound", BAD),
            (rf"SVI fits a slice in five numbers; SSVI the surface, at {s['rmse']:.2f} vol points", LV),
            ('local variance is conditional instantaneous variance (Gy\\"ongy); marginal laws match, joint laws need not', LV),
            (rf"this LV calibration has fading forward skew: {100 * m['fwd_skew']['0']:.1f} now, {100 * m['fwd_skew']['90']:.1f} three "
             rf"months out", BAD),
            (rf"a variance swap is a strip plus a hedge: replicated on {r['n']} overlapping 30-day windows", OPT),
            (r"the VIX is that strip, truncated; ours tracks Deribit's DVOL", IV),
            (rf"the variance premium: positive {100 * p['share_pos']:.0f}\% of weeks, $t = {p['t']:.1f}$; this descriptive fit does not establish "
             rf"return predictability", RV),
            (rf"'daily inverse targets can require buying after a rise; the model note lost 96 percent in one day'{abs(100 * x['note_feb5']):.0f}\%", BAD),
            (r"dealer gamma damps or amplifies; the 0DTE evidence is mixed", OPT),
            (rf"a grid-penalized network, with remaining calendar flags: {float(np.mean(n['pen_test'])):.2f} vol points held out", LV),
        ]
        rows = VGroup()
        for i, (txt, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=24, color=col), label(txt, font_size=20)).arrange(RIGHT, buff=0.25))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        title = label(r"Part 12 in twelve lines", font_size=34).to_edge(UP, buff=0.3)
        rows.next_to(title, DOWN, buff=0.3)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        with self.voiceover(
            """Part twelve in twelve lines. Smiles contain distributional information, with local approximations and tail assumptions. SVI fits slices; SSVI supplies a surface with conditions whose domain must be checked. Local volatility can match suitable diffusion marginals, without fixing joint dynamics. A continuous-hedge variance identity becomes approximate on finite strikes and discrete clocks. VIX is a prescribed variance-price index. Historical variance gaps are descriptive; a regression that fails to reject zero does not prove no predictability. Daily-reset products and dealer hedging can create feedback under specified assumptions. Neural reconstruction and sampled arbitrage penalties are useful tools, not global guarantees or fully unseen-date forecasts."""
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=20))
        self.wait(0.5)
        self.clear_scene()

    def rule(self, env):
        chart = house_chart(PART, lit=("vol",)).scale(0.7).to_edge(UP, buff=0.3)
        rule = wrapped_label(r"Rule 12: the desk quotes only from a fitted surface that passes the arbitrage checker, and "
                             r"every exotic price states which dynamics (local, stochastic, rough) it assumed. "
                             rf"The trial counter still reads {env['trials']}.", 12.4, 23, QC.HOUSE).to_edge(DOWN, buff=0.5)
        tr = env["trials"]
        with self.voiceover(
            "The House's twelfth rule. The volatility desk quotes only from a fitted surface that passes the "
            "arbitrage checker, and every exotic price states which dynamics it assumed, local, stochastic or rough, "
            "because as Chapter eight showed, the same surface can come from very different futures. <bookmark mark='a'/> "
            "This part described markets and priced products; it registered no strategy, so the trial counter still "
            f"reads {tr}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=24) for q, a in DESK]).arrange(DOWN, buff=0.25)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            """Three desk questions. A positive variance-price gap is consistent with insurance when the required discount-factor covariance is positive; the sample alone does not prove that mechanism. <bookmark mark='a'/> Continuous-diffusion variance is replicated by a continuum option strip and continuous stock hedge under zero-carry and integrability assumptions; sampling, jumps, strike truncation and costs leave corrections. <bookmark mark='b'/> For the local short-maturity skew illustration, a five-percent spot fall raises ATM volatility by about two points under sticky strike, zero under sticky moneyness, and roughly four under local volatility. The factor of two is an approximation, not a universal rule. Full solutions are in the notes."""
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And nine problems: Dupire's formula, the log contract's strip, SSVI's two conditions, the local skew's "
            "factor of two, Martin's bound, Gatheral's g from Black's formula, and the volatility swap's convexity. "
            "Two are qualifying-exam problems: the butterfly's bias and variance, and correlated price errors. "
            "Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"stochastic volatility and jumps, which fix the forward smile", [13]),
            (r"rough volatility, and the S\&P 500 and VIX smiles together", [14]),
            (r"exotics priced off the surface", [15]),
            (r"neural calibrators and market generators", [17]),
            (r"option-implied signals in the cross-section", [27]),
            (r"the variance premium as a factor; scenario risk", [32, 40]),
        ])
        with self.voiceover(
            "Where this comes back. Stochastic volatility and jumps, in Part thirteen, fix the forward smile. Rough "
            "volatility, and the S&P 500 and VIX smiles together, are Part fourteen. Exotics in Part fifteen are "
            "priced off this surface. Neural calibrators return in Part seventeen, option-implied signals in Part "
            "twenty-seven, and the variance premium as a factor and a risk in Parts thirty-two and forty."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Gatheral, \textit{The Volatility Surface}, ch.\ 1, 3, 7, 8, 11; Bergomi, \textit{Stochastic Volatility "
             r"Modeling}, ch.\ 2, 3, 5",
             r"Rebonato, \textit{Volatility and Correlation}; Hull, \textit{Options, Futures, and Other Derivatives} "
             r"(volatility smiles); Sinclair; Bennett"],
            [r"Dupire; Derman and Kani; Rubinstein (1994); Gy\"ongy (1986); Neuberger (1994); Carr and Madan (1998)",
             r"Demeterfi et al.\ (1999); Derman (1999); Britten-Jones and Neuberger (2000); Berestycki et al.\ (2002); "
             r"Hagan et al.\ (2002); Cont and da Fonseca (2002)",
             r"Bakshi et al.\ (2003); Lee (2004); Backus et al.\ (2004); Gatheral (2004); Carr and Wu; Bollerslev et al.; "
             r"Cheng and Madhavan (2009)",
             r"Roper (2010); Gatheral and Jacquier (2011, 2014); Martin (2017); Dew-Becker et al.\ (2017); Andersen et al.\ "
             r"(2017); Griffin and Shams (2018)",
             r"Ackerer et al.\ (2020); Baltussen et al.\ (2021); Bergeron et al.\ (2022); Martini and Mingone (2022); "
             r"Bandi et al.\ (2023); Kelly et al.\ (2023); Vuleti\'c and Cont (2024); Dim et al.\ (2024); Wiedemann et "
             r"al.\ (2025)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on, all listed in the notes. The data are "
            "the Surface and two hundred and forty-three weekly surfaces rebuilt from Deribit's trades, Binance's "
            "Bitcoin prices, Deribit's DVOL, the VIX and its three-month cousin from the St. Louis Fed, the S&P 500 "
            "from Yahoo Finance, and Cboe's VIX futures settlements."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 13, Stochastic Volatility and Jumps", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The volatility desk can now read, fit and trade the surface. <bookmark mark='a'/> Next, Part thirteen: "
            "stochastic volatility and jumps. Heston, SABR and Bates, calibrated to the Surface, and why their smiles "
            "move the way real ones do."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
