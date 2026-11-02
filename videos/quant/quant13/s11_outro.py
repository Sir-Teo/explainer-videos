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
    (r"Overnight, your Heston fit's mean reversion jumped from 3 to 20 and the fit error barely moved. Do you care?",
     r"for vanillas, little: the data pin a combination of $\kappa$ and $\xi$ along a valley. For exotics and hedges, yes: "
     r"they depend on each separately, so regularize toward yesterday's values and check the hedge P\&L"),
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
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("facts"), load("calibrate"), load("qe"), load("skew"), load("exotics"), load("history"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, f, c, q, s, e, h):
        e2 = next(r for r in q["rows"] if r["scheme"] == "Euler" and r["n"] == 2 and r["K"] == 1.0)
        q2 = next(r for r in q["rows"] if r["scheme"] == "QE" and r["n"] == 2 and r["K"] == 1.0)
        cl = np.array([v["cliquet"] for v in e["models"].values()])
        X = np.array([r["x"] for r in h["rows"]])
        items = [
            (rf"volatility moves: bitcoin's ranged {100 * f['rv_min']:.0f}--{100 * f['rv_max']:.0f}\%, and rises "
             rf"{f['dvol_change_down5']:.0f}\% on big down days", RV),
            (rf"Heston fits the Surface to {c['fits']['Heston']['rmse']:.1f} vol points, with a vol of vol of "
             rf"{100 * c['fits']['Heston']['params']['xi']:.0f}\%", MODEL_COL["Heston"]),
            (rf"with two steps, QE is {100 * abs(q2['rel']):.0f}\% off where Euler is {100 * e2['rel']:.0f}\% off", OPT),
            (rf"SABR fits each expiry; its vol of vol falls like $T^{{{c['sabr_nu_power']:.2f}}}$", MODEL_COL["SABR"]),
            (rf"the market's skew grows like $T^{{{s['power']:.2f}}}$: between diffusions and jumps", IV),
            (r"SLV fits today exactly and chooses tomorrow by its mixing fraction", MODEL_COL["SLV"]),
            (rf"same vanillas, cliquet prices {100 * (cl.max() - cl.min()) / cl.mean():.0f}\% apart: model risk", BAD),
            (rf"weekly fits: $\rho > 0$ in {100 * (X[:, 4] > 0).mean():.0f}\% of weeks; constants that are not constant",
             VAR),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=col), label(t, font_size=24)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 13 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part thirteen in eight lines. Volatility moves, and it rises when prices fall. Heston's second river fits "
            "the Surface, but only with a violent vol of vol. Andersen's scheme simulates it with a fraction of "
            "Euler's bias. SABR fits "
            "every expiry, and its vol of vol falls like one over the square root of maturity. So does the market's "
            "skew, between what diffusions and jumps can do. Stochastic local volatility fits today exactly and "
            "chooses tomorrow by a dial. Models that agree on every vanilla disagree on exotics. And refitted every "
            "week, the constants are not constant."
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
            "Three desk questions. In Heston, the correlation sets the skew and the vol of vol sets the curvature. "
            "<bookmark mark='a'/> To price a cliquet, never trust local volatility alone: it flattens the future "
            "smile the cliquet is betting on. <bookmark mark='b'/> And if mean reversion jumps overnight while the "
            "fit barely changes, you are walking along the valley: harmless for vanillas, not for exotics or hedges. "
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
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "And five problems: Heston's Riccati equations, its short-maturity skew, the Lévy forward smile, Feller's "
            "condition, and why the leverage function works. Solutions, in English and Chinese, are in the notes."
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
        ])
        with self.voiceover(
            "Where this comes back. The square-root law is Part fourteen's starting point. Part fifteen prices "
            "structured products across these models. Part sixteen makes the pricing fast, and Part seventeen trains "
            "networks to calibrate in microseconds. And the same ideas return for interest rates."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Gatheral, \textit{The Volatility Surface}, ch.\ 2--5; Bergomi, \textit{Stochastic Volatility Modeling}",
             r"Cont and Tankov, \textit{Financial Modelling with Jump Processes}, ch.\ 4, 11, 13; Lewis, "
             r"\textit{Option Valuation under Stochastic Volatility}"],
            [r"Hull and White (1987); Heston (1993); Merton (1976); Bates (1996, 2000); Kou (2002)",
             r"Madan, Carr and Chang (1998); Carr, Geman, Madan and Yor (2002); Carr and Wu (2004)",
             r"Hagan, Kumar, Lesniewski and Woodward (2002, 2014); Albrecher et al.\ (2007); Andersen (2008)",
             r"Fang and Oosterlee (2008); Guyon and Henry-Labord\`ere (2012); Bergomi (2005); Gatheral (2008); "
             r"Guyon (2020)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. The data are the Surface and a hundred "
            "weekly surfaces from Deribit's trades, Binance's Bitcoin prices, and Deribit's DVOL."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 14, Rough and Path-Dependent Volatility", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The volatility desk can now fit, simulate and compare models of moving volatility. <bookmark mark='a'/> "
            "Next, Part fourteen: rough and path-dependent volatility. Why the skew follows a square-root law, what "
            "it means for volatility to be rough, and the debate over whether it is."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
