from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, load

DESK = [
    (r"In Heston, what sets the skew? And the smile's curvature?",
     'As $T\\to0$ with $v_0>0$, regular Heston ATM skew tends to $\\rho\\xi/(4\\sqrt{v_0})$; finite-date shape depends on all parameters.'),
    (r"Local vol and a stochastic vol model both fit today's surface. You must price a cliquet. Which do you use?",
     'Compare plausible joint dynamics; reconcile vanilla fit and numerical errors before interpreting the exotic-price range.'),
    ('Which matched-window Jensen bound applies to a model index future?',
     'Under the same $Q$, date, window and index definition: $\\mathbb E[I_T]\\le\\sqrt{\\mathbb E[I_T^2]}$. The small-dispersion gap is approximately $\\operatorname{Var}(I_T)/(2\\mathbb E[I_T])$.'),
]

PROBLEMS = [
    r"Guess $\mathbb{E}[e^{iu\ln S_T}] = e^{C(\tau) + D(\tau)v + iu\ln S}$ in Heston's model and derive the Riccati "
    r"equations for $C$ and $D$ from the pricing PDE.",
    r"Show that in Heston's model the short-maturity at-the-money skew is $\partial_k\sigma \approx \rho\xi/(4\sqrt{v_0})$.",
    "At zero rates, show that the fixed-notional ratio forward-start smile in an exponential L\\'evy model equals its own current $\\tau$-smile.",
    r"For the CIR variance $dv = \kappa(\theta - v)dt + \xi\sqrt{v}\,dW$, use the scale function to show that $0$ is "
    r"reached with positive probability if and only if $2\kappa\theta < \xi^2$.",
    r"From the forward (Fokker--Planck) equation, show that $dS/S = L(S, t)\sqrt{v}\,dW$ has the marginals of local "
    r"volatility if $L^2(S, t)\,\mathbb{E}[v_t \mid S_t = S] = \sigma^2_{\text{loc}}(S, t)$.",
    r"Derive Merton's series: condition on the number of jumps, price each term by Black--Scholes, and weight by the "
    r"Poisson law; identify $\sigma_n$ and the forward of each term.",
    r"Derive the variance gamma characteristic function by conditioning on the gamma clock, and its martingale "
    r"correction $\omega$.",    r"(qual) Solve $\psi' = a\psi^2 + b\psi + c$, $\psi(0) = 0$, with $a, c > 0$ and $b^2 < 4ac$, and show it blows up at "
    r"$T^* = \frac{2}{\sqrt{4ac - b^2}}\big(\frac\pi2 - \arctan\frac{b}{\sqrt{4ac - b^2}}\big)$; when are Heston's moments of "
    r"order $p > 1$ finite for ever?",
    r"(qual) Invert Lee's formula: show that a wing slope $\beta \in (0, 2)$ corresponds to the critical moment "
    r"$\tilde q = (2 - \beta)^2/(8\beta)$, and find the slopes for $\tilde q = 2$, $\tilde q \to 0$ and $\tilde q \to \infty$.",
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
            ('Random variance can curve an IV smile; correlation can tilt it.', RV),
            ('Heston: affine characteristic function; interacting parameters and branch conventions.', MODEL_COL["Heston"]),
            ('QE: conditional moment matching; discretization and martingale conditions remain.', OPT),
            ('SABR: asymptotic IV approximation and effective density PDE are distinct.', MODEL_COL["SABR"]),
            ('Jumps: risk-neutral fits depend on bounds; no physical crash-probability inference.', MODEL_COL["VG"]),
            ('Skew powers on a finite grid do not establish universal short-time laws.', IV),
            ('SLV: ideal marginal identity; numerical errors and no general monotonicity in $\\eta$.', MODEL_COL["SLV"]),
            ('Ratio forward-starts and cliquets: dynamics, unequal fits and numerical errors.', BAD),
            ('Bitcoin model-index illustration; no volatility-option surface for a joint test.', VAR),
            ('Calibration fit, parameter stability and hedge performance require separate evidence.', GREY_A),
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
            """Part thirteen in ten lines. Random variance can curve a smile, and correlation can tilt it. Heston has an affine characteristic function, with careful branch handling and interacting parameters. QE matches conditional variance moments, subject to numerical and martingale conditions. SABR's asymptotic formula differs from its model and from the effective density PDE. Jump parameters depend on fit bounds and do not directly measure physical crash probabilities. Finite-grid skew powers are descriptive, not universal family laws. Ideal SLV preserves marginals; particles retain fitting and discretization errors, and eta gives no general monotone exotic-price rule. Forward-start and cliquet comparisons reflect dynamics together with unequal fits. The Bitcoin volatility-index exercise lacks index-option quotes for a joint test. Calibration stability, price fit and hedging performance each need their own evidence."""
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=20))
        self.wait(0.5)
        self.clear_scene(run_time=0.35)

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=24) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            """Three desk questions. Regular short-time Heston ATM skew depends on rho xi over four root v; finite-maturity curvature and skew involve interacting parameters. <bookmark mark='a'/> For a cliquet, compare plausible joint dynamics and quantify unequal fitting and numerical errors before attributing a price spread to model risk. Local volatility's forward flattening in our example is not universal. <bookmark mark='b'/> Jensen compares an index future with root expected squared index under the same Q, date, window and definition. It does not order arbitrary quoted futures and spot-start variance swaps. The notes give the contract definitions and assumptions."""
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene(run_time=0.35)

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And nine problems: Heston's Riccati equations, its short-maturity skew, the Lévy forward smile, "
            "Feller's condition, why the leverage function works, Merton's series, and the variance gamma "
            "characteristic function. Two are qualifying-exam problems: the explosion time, and Lee's formula "
            "inverted. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene(run_time=0.35)

    def payoffs(self):
        card = payoff_card([
            (r"the skew's square-root law, rough volatility, and the joint SPX/VIX fit", [14]),
            (r"cliquets, autocallables and barriers, priced across models", [15]),
            (r"COS, PDEs and Monte Carlo, made fast and checked", [16]),
            ('neural calibrators: benchmark-specific speed and accuracy; deep hedging under SV', [17]),
            (r"stochastic rates: the same ideas for the yield curve", [19]),
            (r"jump to default: credit inside the equity smile", [20]),
            (r"FX desks: SLV, barriers and the mixing fraction in practice", [22]),
        ])
        with self.voiceover(
            """Part fourteen examines observed skew scaling, rough and path-dependent volatility, and joint calibration. Part fifteen compares structured products across models. Part sixteen studies pricing methods, and Part seventeen neural calibration and hedging, with benchmark-specific latency and accuracy checks. Related ideas return in interest rates, credit and FX. The remaining parts build on these methods and their assumptions."""
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

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
            """The references span Merton's jumps, affine models, kernel particles and recent neural operators. Data include pooled Deribit option marks, one hundred weekly surfaces, Binance Bitcoin prices, Deribit DVOL and the 1987 S&P history. Pooled marks are not simultaneous executable trades. Research results and historical illustrations carry their stated model and numerical assumptions."""
        ):
            self.play(FadeIn(card))
            self.wait(4)
        self.clear_scene(run_time=0.35)

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        env = load("envelope")
        rule = wrapped_label('Rule 13: log fit error, parameter changes and numerical checks; compare plausible models and reconcile unequal fits before interpreting exotic-price spreads. Trial counter: 312.', 12.4, 22, QC.HOUSE).to_edge(DOWN, buff=0.3)
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 14, Rough and Path-Dependent Volatility", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"""The volatility desk can fit, simulate and compare models. Rule thirteen: record calibration errors, numerical checks and parameter changes; price exotics under more than one plausible calibrated model, and reconcile fitting and numerical errors before interpreting the spread. No new strategy trials were run, so the counter remains {env['trials']}. <bookmark mark='a'/> Next, Part fourteen: rough and path-dependent volatility, the empirical skew scaling, and what evidence can distinguish competing dynamics."""
        ) as vo:
            self.play(FadeIn(chart.scale(0.85).to_edge(UP, buff=0.3)), FadeIn(rule))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeOut(rule), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene(run_time=0.35)
