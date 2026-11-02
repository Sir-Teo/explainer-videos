from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, VAR, load

DESK = [
    (r"Volatility has $H \approx 0.1$. What does that mean for a one-day option against a one-month one?",
     r"the at-the-money skew grows like $T^{H - 1/2}$: a one-day option's skew is about $30^{0.4} \approx 4$ times the "
     r"one-month's; over a day, volatility itself can move a lot, so short-dated options carry most of the vol-of-vol risk"),
    (r"A colleague says rough volatility is just fast mean reversion. How would you test it?",
     r"use several measurements: the scaling of intraday realized variance at sub-daily lags (after removing seasonality "
     r"and noise), the skew's term structure at the shortest expiries, and out-of-sample forecasts and hedges of rough "
     r"against multi-factor models"),
    (r"Rough Bergomi takes half a minute to calibrate; the desk needs milliseconds. What are your options?",
     r"a neural surrogate trained once on the model's prices (Horvath, Muguruza and Tomas 2021), a Markovian lift with "
     r"few factors, or rough Heston's semi-closed form with fast Fourier pricing"),
    (r"Why can't a one-factor Markov stochastic volatility model fit a 1-week skew?",
     r"its skew is flat below its mean-reversion time $1/\kappa$ (chapter 2); to be steep at one week, $\kappa$ must be about 50 "
     r"a year, and then the skew collapses like $1/(\kappa T)$ at longer expiries"),
]

PROBLEMS = [
    r"Show that $W^H_t = \sqrt{2H}\int_0^t (t - s)^{H - 1/2}\,dW_s$ has variance $t^{2H}$.",
    r"For fractional Brownian motion, show that $\mathbb{E}|B^H_{t + \Delta} - B^H_t|^q = c_q\,\Delta^{qH}$, so that "
    r"$\zeta_q = qH$.",
    r"In rough Bergomi, show that $\mathbb{E}[v_t] = \xi_0(t)$, and that each $\xi_t(T) = \mathbb{E}_t[v_T]$ is a martingale.",
    r"Show that $\int_0^\infty e^{-xt}\,\frac{x^{-\alpha}}{\Gamma(\alpha)\Gamma(1 - \alpha)}\,dx = \frac{t^{\alpha - 1}}"
    r"{\Gamma(\alpha)}$ for $0 < \alpha < 1$: the identity behind the Markovian lift.",
    r"For a stationary Hawkes process with baseline $\mu$ and kernel $\phi$, show that the mean rate is "
    r"$\mu / (1 - \|\phi\|_1)$, and explain why $\|\phi\|_1 \to 1$ is called nearly unstable.",
    r"Compute $\int_0^T\!\int_t^T (u - t)^{H - 1/2}\,du\,dt$, and deduce the rough skew's $T^{H - 1/2}$.",
    r"Show that $b_k$ in the hybrid scheme is the point where the kernel equals its own average over cell $k$.",
    r"Show that each factor of the 4-factor PDV obeys $dR = \lambda(r^2/dt - R)\,dt$, an exponential moving average.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("skew"), load("roughness"), load("artefact"), load("rbergomi"), load("rheston"), load("pdv"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, s, r, a, rb, rh, p):
        w, f, b2, ps = load("skew_weekly"), load("rfsv_forecast"), load("bergomi2f"), load("pdv_spx")
        hy, hs, sg, q = load("hybrid_check"), load("hawkes_sweep"), load("sigvol"), load("qrh_sim")
        items = [
            (rf"the skew's power law, median exponent {w['a_median']:.2f} over {w['n_weeks']} weeks; a bounded rival", IV),
            (r"a kernel's shape makes the skew: exponentials go flat, power laws explode (Fukasawa: rough or arbitrage)", IV),
            (rf"bitcoin is rough in two eras: $H = {load('roughness_2018')['H']:.2f}$ and ${r['H']:.2f}$", RV),
            (rf"the rough forecast explains why HAR works; head to head it wins {f['rough_wins']} of 6", RV),
            (rf"rough Bergomi fits the Surface to {rb['rmse']:.2f} vol points with three numbers and the variance curve",
             MODEL_COL["rBergomi"]),
            (rf"the hybrid scheme keeps the spike; the naive sum loses it (variance {hy['var'][0]['riemann']:.2f} for 1)", ROUGH),
            (rf"rough Heston: a fractional Riccati, Adams of order {load('adams_conv')['order']:.1f}; left free, $H = {rh['params']['H']:.2f}$",
             MODEL_COL["rough Heston"]),
            (r"nearly unstable order flow turns rough; lifts make rough models Markovian", VAR),
            (r"the estimator can be fooled: a smooth one-day half-life reads like bitcoin", BAD),
            (rf"options: a two-factor Bergomi scores {b2['rmse']:.2f}; the horse races lean against one factor", VAR),
            (rf"the past explains {100 * p['r2_test']:.0f}\% of DVOL and {100 * ps['r2_test']:.0f}\% of the VIX out of sample; "
             r"not 5 August's quotes", MODEL_COL["PDV"]),
            (rf"qRH's feedback makes the Zumbach effect; signatures turn calibration into algebra ({sg['rmse_out']:.2f})",
             QC.DELTA),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.25))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        title = label(r"Part 14 in twelve lines", font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(title, DOWN, buff=0.3)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        if rows.height > 6.6:
            rows.scale_to_fit_height(6.6)
        with self.voiceover(
            "Part fourteen in twelve lines. The skew explodes as expiry nears, close to a power law, week after "
            "week, with a bounded rival at the shortest end. The shape of the kernel decides the skew: one time "
            "scale goes flat, all time scales make a power law, and Fukasawa showed a true power law forces "
            "roughness. Bitcoin's volatility is rough in two eras, and the rough forecast explains why HAR works "
            "without reliably beating it. Rough Bergomi fits the Surface with three numbers and the market's "
            "variance curve, simulated by a hybrid scheme that keeps the kernel's spike. Rough Heston keeps a "
            "characteristic function through a fractional Riccati equation, solved by Adams. Nearly unstable order "
            "flow looks rough from far away, and lifts make rough models Markovian. The estimator can be fooled, "
            "and the options lean toward several time scales. The past explains most of implied volatility, but "
            "not the quotes of the fifth of August. And feedback, transport and signatures are the frontier."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=24))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=24) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Four desk questions. With H near a tenth, a one-day option's skew is about four times a one-month "
            "option's, and short-dated options carry most of the risk of volatility moving. <bookmark mark='a'/> To "
            "test roughness against fast mean reversion, use several measurements, cleaned of seasonality and noise: "
            "the bias map, sub-daily lags, the options, and out-of-sample forecasts and hedges. "
            "<bookmark mark='b'/> To calibrate in milliseconds, train a surrogate, lift the model, or use rough "
            "Heston's Fourier form. <bookmark mark='c'/> And why can't a one-factor Markov model fit a one-week "
            "skew? Its skew is flat below its mean-reversion time; to be steep at a week, kappa must be about fifty "
            "a year, and then the long end collapses like one over kappa T. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[3], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "And eight problems: the variance of a rough process, the scaling law behind the estimator, rough "
            "Bergomi's martingale property, the identity behind the lift, the Hawkes mean rate, the double integral "
            "behind the rough skew, the hybrid scheme's optimal points, and the Markovian PDV factor. Solutions, in "
            "English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"exotics priced under rough and classical models", [15]),
            (r"Monte Carlo variance reduction and fast schemes", [16]),
            (r"neural calibrators for rough models; deep hedging", [17]),
            (r"Hawkes order flow and the limit order book; power-law market impact", [36, 37, 38]),
            (r"volatility forecasting with path-dependent features", [27, 32]),
        ])
        with self.voiceover(
            "Where this comes back. Exotics are priced under rough and classical models in Part fifteen. Part sixteen "
            "speeds up the Monte Carlo, and Part seventeen trains the networks that make rough models fast. The "
            "Hawkes picture of order flow returns with the limit order book and market impact, and path-dependent "
            "features return in forecasting."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Bayer, Friz, Fukasawa, Gatheral, Jacquier and Rosenbaum (eds.), \textit{Rough Volatility} (SIAM 2023), ch.\ 1--10",
             r"Guyon and Henry-Labord\`ere, \textit{Nonlinear Option Pricing}; Bergomi, \textit{Stochastic Volatility "
             r"Modeling}; Gatheral, \textit{The Volatility Surface}; Friz and Hairer (2nd ed.)"],
            [r"Comte and Renault (1998); Al\`os, Le\'on and Vives (2007); Fukasawa (2011, 2021); Gatheral, Jaisson and "
             r"Rosenbaum (2018)",
             r"Bayer, Friz and Gatheral (2016); Bennedsen, Lunde and Pakkanen (2017); El Euch and Rosenbaum (2019); "
             r"Abi Jaber and El Euch (2019); Abi Jaber (2019); Bayer and Breneis (2023)",
             r"Jaisson and Rosenbaum (2016); El Euch, Fukasawa and Rosenbaum (2018); Livieri, Mouti, Pallavicini and "
             r"Rosenbaum (2018); Bayer and Stemper (2018); Horvath, Muguruza and Tomas (2021)",
             r"Fukasawa, Takabatake and Westphal (2022); Bolko et al.\ (2023); Chong et al.\ (2024); Cont and Das (2024); "
             r"R{\o}mer (2022); Guyon and El Amrani (2023); Abi Jaber and Li (2025)",
             r"Guyon and Lekeufack (2023); Nutz and Riveros Valdevenito (2024); Gatheral, Jusselin and Rosenbaum (2020); "
             r"Guyon (2020, 2024); Rosenbaum and Zhang (2022); Cuchiero, Gazzani and Svaluto-Ferro (2023)",
             r"BIS Bulletins 90 and 95 (2024); Li and Askanazi, SEC DERA working paper (2025)"])
        with self.voiceover(
            "The book and chapters this part covers, and the papers it draws on. The data are the Surface and two "
            "years of weekly Deribit option trades, Bitcoin's one-minute, five-minute and daily prices from Binance, "
            "Deribit's DVOL, the VIX and the Nikkei from FRED, and Ken French's daily market return."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 15, Exotics and Structured Products", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The volatility desk now has models for every scale of volatility, and a rule for choosing between them. "
            "<bookmark mark='a'/> Next, Part fifteen: exotics and structured products. Barriers, autocallables, "
            "cliquets and the notes sold to savers, priced across the models of the last three parts, and what the "
            "spread between them costs the buyer."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
