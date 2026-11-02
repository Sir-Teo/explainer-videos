from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, load

DESK = [
    (r"In Heston, what sets the skew? And the smile's curvature?",
     r"the correlation $\rho$ sets the skew, scaled by the vol of vol: at short maturity the at-the-money slope is about "
     r"$\rho\xi/(4\sqrt{v_0})$; the curvature comes from $\xi^2$; mean reversion $\kappa$ flattens both as maturity grows"),
    (r"Local vol and a stochastic vol model both fit today's surface. You must price a cliquet. Which do you use?",
     r"not local vol alone: a cliquet is a bet on future smiles, and local vol flattens them; use a stochastic or "
     r"stochastic-local model with a chosen mixing fraction, and report the spread across models as model risk"),
    (r"Why can a VIX future never trade above the 30-day variance-swap volatility?",
     r"Jensen: the future is $\mathbb{E}[\mathrm{VIX}_T]$, the variance-swap vol is $\sqrt{\mathbb{E}[\mathrm{VIX}^2_T]}$, "
     r"and the square root is concave; the gap is about $\operatorname{Var}(\mathrm{VIX})/(2\mathbb{E}\mathrm{VIX})$, so "
     r"VIX futures and options price the vol of vol"),
]

PROBLEMS = [
    r"Guess $\mathbb{E}[e^{iu\ln S_T}] = e^{C(\tau) + D(\tau)v + iu\ln S}$ in Heston's model and derive the Riccati "
    r"equations for $C$ and $D$ from the pricing PDE.",
    r"Show that in Heston's model the short-maturity at-the-money skew is $\partial_k\sigma \approx \rho\xi/(4\sqrt{v_0})$.",
    r"Show that in any exponential L\'evy model the forward smile (a $\tau$-maturity option starting at $t$) equals "
    r"today's smile at maturity $\tau$.",
    r"For the CIR variance $dv = \kappa(\theta - v)dt + \xi\sqrt{v}\,dW$, use the scale function to show that $0$ is "
    r"reached with positive probability if and only if $2\kappa\theta < \xi^2$.",
    r"From the forward (Fokker--Planck) equation, show that $dS/S = L(S, t)\sqrt{v}\,dW$ has the marginals of local "
    r"volatility if $L^2(S, t)\,\mathbb{E}[v_t \mid S_t = S] = \sigma^2_{\text{loc}}(S, t)$.",
    r"Derive Merton's series: condition on the number of jumps, price each term by Black--Scholes, and weight by the "
    r"Poisson law; identify $\sigma_n$ and the forward of each term.",
    r"Derive the variance gamma characteristic function by conditioning on the gamma clock, and its martingale "
    r"correction $\omega$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("facts"), load("calibrate"), load("qe"), load("skew"), load("exotics"), load("history"),
                   load("mixing"), load("levy_fits"), load("vol_puzzle"), load("history_reg"), load("sabr_pde"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, f, c, q, s, e, h, mx, lf, vp, hr, sp):
        e2 = next(r for r in q["rows"] if r["scheme"] == "Euler" and r["n"] == 2 and r["K"] == 1.0)
        q2 = next(r for r in q["rows"] if r["scheme"] == "QE" and r["n"] == 2 and r["K"] == 1.0)
        cl = np.array([v["cliquet"] for v in e["models"].values()])
        fr = hr["frontier"]
        items = [
            (rf"volatility moves: bitcoin's ranged {100 * f['rv_min']:.0f}--{100 * f['rv_max']:.0f}\%; random volatility "
             r"makes a smile, correlation tilts it (mixing, derived)", RV),
            (rf"Heston: a Riccati characteristic function; the little trap; a fit of {c['fits']['Heston']['rmse']:.2f} vol "
             rf"points with a vol of vol of {100 * c['fits']['Heston']['params']['xi']:.0f}\%", MODEL_COL["Heston"]),
            (rf"QE matches the variance's moments: {100 * abs(q2['rel']):.0f}\% off with two steps where Euler is "
             rf"{100 * e2['rel']:.0f}\%", OPT),
            (rf"SABR: skew $\rho\nu/2$, curvature $\propto\nu^2$; arbitrage-free SABR keeps mass 1 and "
             rf"{100 * sp['QL']:.0f}\% absorbed at zero", MODEL_COL["SABR"]),
            (rf"jumps and L\'evy: Merton's series; CGMY wants $Y = {lf['fits']['CGMY_inf']['params']['Y']:.2f}$; Bates's jumps "
             r"became a second diffusion", MODEL_COL["VG"]),
            (rf"skew term structure: market $T^{{{s['power']:.2f}}}$; diffusions flat, pure jumps $1/T$", IV),
            (r"SLV by particles fits today; the mixing fraction moves exotics, not vanillas", MODEL_COL["SLV"]),
            (rf"same vanillas, cliquets {100 * (cl.max() - cl.min()) / cl.mean():.0f}\% apart; forward smiles and Bergomi's "
             r"curves are the reason", BAD),
            (rf"the model's vol index moves {vp['ratio']:.1f} times as much as DVOL: the SPX/VIX puzzle in bitcoin", VAR),
            (rf"calibration is ill-posed: regularising cut weekly parameter moves from {100 * fr[0]['median_change_all']:.0f}"
             rf"\% to {100 * fr[-1]['median_change_all']:.0f}\%", GREY_A),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=26, color=col), label(t, font_size=22)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        title = label(r"Part 13 in ten lines", font_size=36).to_edge(UP, buff=0.35)
        rows.next_to(title, DOWN, buff=0.35)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        with self.voiceover(
            "Part thirteen in ten lines. Volatility moves, and random volatility makes a smile, which correlation "
            "tilts. Heston's second river has a closed-form characteristic function, if you mind the branch cut, and "
            "fits the Surface only with a violent vol of vol. Andersen's scheme simulates it by matching moments. "
            "SABR reads the smile in four numbers, and arbitrage-free SABR fixes its density. Jumps and Lévy "
            "processes are clocks; their skews blow up like one over maturity while diffusions stay flat, and the "
            "market sits between. Stochastic local volatility fits today exactly and chooses tomorrow with a dial. "
            "Models that agree on every vanilla disagree on exotics, because they disagree on future smiles. The "
            "smile asks for more vol of vol than volatility has. And calibration is an inverse problem: regularise, "
            "and judge the model by its hedge."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=20))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=24) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions. In Heston, the correlation sets the skew and the vol of vol sets the curvature. "
            "<bookmark mark='a'/> To price a cliquet, never trust local volatility alone: it flattens the future "
            "smile the cliquet is betting on. <bookmark mark='b'/> And a VIX future can never trade above the "
            "variance-swap volatility: the square root is concave, and the gap is the price of the vol of vol. "
            "Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "And seven problems: Heston's Riccati equations, its short-maturity skew, the Lévy forward smile, "
            "Feller's condition, why the leverage function works, Merton's series, and the variance gamma "
            "characteristic function. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the skew's square-root law, rough volatility, and the joint SPX/VIX fit", [14]),
            (r"cliquets, autocallables and barriers, priced across models", [15]),
            (r"COS, PDEs and Monte Carlo, made fast and checked", [16]),
            (r"neural calibrators that fit in microseconds; deep hedging under SV", [17]),
            (r"stochastic rates: the same ideas for the yield curve", [19]),
            (r"jump to default: credit inside the equity smile", [20]),
            (r"FX desks: SLV, barriers and the mixing fraction in practice", [22]),
        ])
        with self.voiceover(
            "Where this comes back. The square-root law is Part fourteen's starting point. Part fifteen prices "
            "structured products across these models. Part sixteen makes the pricing fast, and Part seventeen trains "
            "networks to calibrate in microseconds. The same ideas return for interest rates, a jump to zero becomes "
            "credit, and FX desks run stochastic local volatility every day."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Gatheral, \textit{The Volatility Surface}, ch.\ 2--8, 10--11; Bergomi, \textit{Stochastic Volatility "
             r"Modeling}, ch.\ 3--4, 6--10, 12",
             r"Cont and Tankov, \textit{Financial Modelling with Jump Processes}, ch.\ 4, 6, 11, 13--15; Lewis, "
             r"\textit{Option Valuation under Stochastic Volatility}; Guyon and Henry-Labord\`ere, \textit{Nonlinear "
             r"Option Pricing}"],
            [r"Merton (1976); Hull and White; Scott; Wiggins (1987); Stein and Stein (1991); Heston (1993); Bates (1996, "
             r"2000); Renault and Touzi (1996); Romano and Touzi; Bakshi, Cao and Chen (1997)",
             r"Madan and Seneta (1990); Barndorff-Nielsen (1997); Madan, Carr and Chang (1998); Duffie, Pan and Singleton "
             r"(2000); Carr, Geman, Madan and Yor (2002, 2007); Kou (2002); Carr and Wu (2004)",
             r"Hagan et al.\ (2002, 2014); Bartlett (2006); Ob\l\'oj (2008); Antonov, Konikov and Spector (2015); Albrecher "
             r"et al.\ (2007); Broadie and Kaya (2006); Andersen (2008); Andersen and Piterbarg (2007)",
             r"Bergomi (2005); Guyon and Henry-Labord\`ere (2012); Gatheral (2008); Cont and Kokholm (2013); Guyon (2020); "
             r"Broadie, Chernov and Johannes (2007); Hull and White (2017)",
             r"Hou et al.\ (2020); Matic, Packham and H\"ardle (2023); Abi Jaber and De Carvalho (2023); Abi Jaber, Illand "
             r"and Li (2023); Guyon and Mustapha (2023); Choi and Kwok (2024); Reisinger and Tsianni (2025)"])
        if card.height > 7.4:
            card.scale_to_fit_height(7.4)
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on, from Merton's jumps to this year's "
            "neural operators. The data are the Surface and a hundred weekly surfaces from Deribit's trades, "
            "Binance's Bitcoin prices, Deribit's DVOL, and the S&P 500 of 1987."
        ):
            self.play(FadeIn(card))
            self.wait(4)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        env = load("envelope")
        rule = wrapped_label(r"Rule 13: every model the desk uses is fitted by the calibrator, which logs its error and "
                             r"how far its parameters moved since last week; every exotic is priced under at least two "
                             r"models fitted to the same surface, and the spread is reported as model risk.  "
                             rf"The trial counter still reads {env['trials']}.", 12.4, 22, QC.HOUSE).to_edge(DOWN, buff=0.3)
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 14, Rough and Path-Dependent Volatility", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The volatility desk can now fit, simulate and compare models of moving volatility, and it adds a rule. "
            "Rule thirteen: every model the desk uses is fitted by the calibrator, which logs its error and how far "
            "its parameters moved since last week. Every exotic is priced under at least two models fitted to the "
            "same surface, and the spread is reported as model risk. No strategy was tested in this part, so the "
            f"trial counter still reads {env['trials']}. <bookmark mark='a'/> "
            "Next, Part fourteen: rough and path-dependent volatility. Why the skew follows a square-root law, what "
            "it means for volatility to be rough, and the debate over whether it is."
        ) as vo:
            self.play(FadeIn(chart.scale(0.85).to_edge(UP, buff=0.3)), FadeIn(rule))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeOut(rule), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
