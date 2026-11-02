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
        items = [
            (rf"the Surface's skew grows like $T^{{-{s['power']['a']:.2f}}}$; a bounded form fits better", IV),
            (rf"bitcoin's log variance is rough: $H = {r['H']:.2f}$, or {a['btc_deseasonalized']:.2f} without weekends", RV),
            (rf"rough Bergomi fits the Surface to {rb['rmse']:.1f} vol points with three numbers and the variance curve",
             MODEL_COL["rBergomi"]),
            (rf"rough Heston left free drifts to $H = {rh['params']['H']:.2f}$; held at 0.1 it fits almost as well, with sane "
             r"parameters", MODEL_COL["rough Heston"]),
            (r"nearly unstable order flow becomes rough volatility at a distance", ROUGH),
            (r"a few dozen exponential factors stand in for the rough kernel", VAR),
            (r"smooth but fast volatility can read as rough: the debate is open", BAD),
            (rf"bitcoin's past path explains {100 * p['r2_test']:.0f}\% of DVOL out of sample", MODEL_COL["PDV"]),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=col), label(t, font_size=24)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 14 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part fourteen in eight lines. The skew explodes as expiry nears, close to a power law. Bitcoin's "
            "volatility is rough, with H near a tenth. Rough Bergomi and rough Heston fit the Surface with a few "
            "numbers. Roughness may be what nearly unstable order flow looks like from far away, "
            "and a few dozen ordinary factors can imitate it. A smooth but very fast volatility can look rough too, "
            "so the debate is open. And much of implied volatility is simply a function of the path the price has "
            "taken."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=24) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions. With H near a tenth, a one-day option's skew is about four times a one-month "
            "option's, and short-dated options carry most of the risk of volatility moving. <bookmark mark='a'/> To "
            "test roughness against fast mean reversion, use several measurements, cleaned of seasonality and noise, "
            "and compare forecasts and hedges out of sample. <bookmark mark='b'/> And to calibrate in milliseconds, "
            "train a surrogate, lift the model, or use rough Heston's Fourier form. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "And five problems: the variance of a rough process, the scaling law behind the estimator, rough "
            "Bergomi's martingale property, the identity behind the lift, and the Hawkes mean rate. Solutions, in "
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
            (r"Hawkes order flow and the limit order book", [36, 38]),
            (r"volatility forecasting with path-dependent features", [27, 32]),
        ])
        with self.voiceover(
            "Where this comes back. Exotics are priced under rough and classical models in Part fifteen. Part sixteen "
            "speeds up the Monte Carlo, and Part seventeen trains the networks that make rough models fast. The "
            "Hawkes picture of order flow returns with the limit order book, and path-dependent features return in "
            "forecasting."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Bayer, Friz, Fukasawa, Gatheral, Jacquier and Rosenbaum (eds.), \textit{Rough Volatility} (SIAM 2023)",
             r"Guyon and Henry-Labord\`ere, \textit{Nonlinear Option Pricing}; Bergomi, \textit{Stochastic Volatility "
             r"Modeling}"],
            [r"Al\`os, Le\'on and Vives (2007); Fukasawa (2011); Gatheral, Jaisson and Rosenbaum (2018)",
             r"Bayer, Friz and Gatheral (2016); Bennedsen, Lunde and Pakkanen (2017); El Euch and Rosenbaum (2019)",
             r"Jaisson and Rosenbaum (2016); El Euch, Fukasawa and Rosenbaum (2018); Abi Jaber and El Euch (2019)",
             r"Guyon and El Amrani (2023); Cont and Das (2024); Guyon and Lekeufack (2023); Gatheral, Jusselin and "
             r"Rosenbaum (2020)", r"Guyon (2022); Cuchiero, Gazzetta and Svaluto-Ferro (2023); Horvath, Muguruza and "
             r"Tomas (2021)"])
        with self.voiceover(
            "The book and chapters this part covers, and the papers it draws on. The data are the Surface, Bitcoin's "
            "five-minute and daily prices from Binance, and Deribit's DVOL."
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
