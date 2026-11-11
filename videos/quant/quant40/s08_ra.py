from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.quant import *  # noqa: F403
from videos.quant.quant40.common import ladder, pause_card, desk_question
from videos.quant.quant40.common import (
    BAD,
    ES_C,
    GOOD,
    HURDLE,
    MODEL_C,
    PART,
    VAR_C,
    load,
)


class Uncertainty(VoiceoverScene):
    def construct(self):
        ra = load("ra")
        self.card(ra)
        self.problem()
        self.algorithm()
        self.animate()
        self.table(ra)
        self.es_bound()
        self.aggregation()
        self.estimation()
        self.whale()
        self.question()

    def card(self, ra):
        r = [x for x in ra["rows"] if x["theta"] == 2.0][0]
        c = chapter_card(7, r"Model uncertainty", r"How wrong can a risk number be if we do not know the dependence?",
                         part=PART)
        with self.voiceover(
            f"Chapter seven revisits the chosen Pareto example. The lower-grid rearrangement estimate is {r['worst_lo']:.0f}, about {r['worst_lo']/r['comonotonic']:.1f} times the comonotonic sum of VaRs. This is a finite-grid heuristic output, not a certified global worst-case value. Comonotonicity is one particular dependence structure, and need not maximize VaR. A separate analytic sum-of-ES bound remains valid for these integrable marginals."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def problem(self):
        rows = [cmath(r"L_1, \dots, L_d", r":", r"\text{marginals known}", font_size=40),
                cmath(r"C", r":", r"\text{unknown}", font_size=40, colors={r"\text{unknown}": BAD}),
                cmath(r"\overline{\text{VaR}}_\alpha", r"=", r"\sup_C \text{VaR}_\alpha(L_1 + \dots + L_d)", font_size=40,
                      colors={r"\overline{\text{VaR}}_\alpha": VAR_C})]
        whys = [why(r"each desk's or each risk type's loss distribution can be estimated from its own data"),
                why(r"how they depend on one another, especially in the tail, often cannot"),
                why(r"the worst VaR over every possible dependence: a bound that holds whatever the copula")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The problem. <bookmark mark='a'/> Each loss's own distribution can be estimated from its own data. "
            "<bookmark mark='b'/> How they depend on each other, especially in the tail, often cannot. "
            "<bookmark mark='c'/> So ask for the worst VaR of the sum over every possible dependence: a bound that holds "
            "whatever the copula."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def algorithm(self):
        rows = [cmath(r"X_{ij}", r"=", r"F_j^{-1}\bigl(\alpha + (1 - \alpha)\tfrac{i}{N}\bigr)", font_size=40),
                cmath(r"\text{for each } j", r":", r"\text{order column } j \text{ opposite to } \textstyle\sum_{k \ne j} X_{\cdot k}",
                      font_size=34, colors={r"\text{for each } j": HURDLE}),
                cmath(r"\overline{\text{VaR}}_\alpha", r"\approx", r"\min_i \textstyle\sum_j X_{ij}", font_size=40,
                      colors={r"\overline{\text{VaR}}_\alpha": VAR_C})]
        whys = [why(r"discretise each marginal's tail beyond $\alpha$ into $N$ quantiles, one column per loss"),
                why(r"Embrechts, Puccetti and Rüschendorf's rearrangement algorithm (2013): make each column move against "
                    r"the sum of the others, and repeat until nothing changes"),
                why('a finite-grid alternating-rearrangement estimate; local stabilization and finite iteration do not certify a global optimum')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The rearrangement method is a numerical dependence exercise. <bookmark mark='a'/> Discretize the upper tail of each known marginal into columns. <bookmark mark='b'/> Reorder a column against the sum of the others, cycling until stabilization or an iteration cap. <bookmark mark='c'/> The minimum row sum is a candidate based on that discretization. The unchanged implementation uses two grids, a capped final upper quantile and at most two hundred passes. It does not prove a global optimum or certified lower and upper bounds for the continuum VaR supremum."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def animate(self):
        N, d = 6, 3
        theta = 2.0
        p = 0.99 + 0.01 * np.arange(N) / N
        q = (1 - p) ** (-1 / theta) - 1
        X = np.column_stack([q] * d)
        states = [X.copy()]
        for _ in range(4):
            for j in range(d):
                rest = X.sum(1) - X[:, j]
                order = np.argsort(rest)
                col = np.sort(X[:, j])[::-1]
                new = np.empty_like(col)
                new[order] = col
                X[:, j] = new
            states.append(X.copy())

        def table(M):
            g = VGroup()
            for i in range(N):
                row = VGroup(*[MathTex(f"{M[i, j]:.1f}", font_size=26) for j in range(d)],
                             MathTex(f"{M[i].sum():.1f}", font_size=26, color=VAR_C))
                for j, cell in enumerate(row):
                    cell.move_to([-2.4 + 1.6 * j + (0.6 if j == d else 0), 1.8 - 0.62 * i, 0])
                g.add(row)
            return g
        head = VGroup(*[label(t, font_size=16, color=GREY_B).move_to([-2.4 + 1.6 * j + (0.6 if j == d else 0), 2.5, 0])
                        for j, t in enumerate((r"$L_1$", r"$L_2$", r"$L_3$", r"row sum"))])
        cur = table(states[0])
        note_ = label('initial condition was comonotonic; displayed rows show the current rearrangement', font_size=18, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "A six-quantile illustration of three chosen Pareto marginals. <bookmark mark='a'/> Initially columns share the same order: the minimum row sum is their comonotonic cutoff value. <bookmark mark='b'/> Each alternating pass reorders a column against the other columns' sum. <bookmark mark='c'/> Large entries spread across rows and the reported minimum can rise. This demonstrates the heuristic's operation; it neither proves global convergence nor converts a finite set of tail quantiles into a certified continuum VaR maximum."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cur), FadeIn(note_))
            vo.wait_until("a")
            self.play(Indicate(VGroup(*[r_[-1] for r_ in cur]), color=VAR_C))
            vo.wait_until("b")
            for M in states[1:3]:
                nxt = table(M)
                self.play(Transform(cur, nxt), run_time=1.2)
            vo.wait_until("c")
            for M in states[3:]:
                nxt = table(M)
                self.play(Transform(cur, nxt), run_time=1.0)
        self.wait(0.4)
        self.clear_scene()

    def table(self, ra):
        hx = [-4.2, -1.4, 1.2, 3.8]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"Pareto tail exponent", r"independent",
                                                                         r"comonotonic (sum of VaRs)", r"grid estimate")])
        tab = VGroup(head)
        for r in ra["rows"]:
            tab.add(VGroup(MathTex(f"{r['theta']:g}", font_size=28), MathTex(f"{r['independent']:.1f}", font_size=28, color=GOOD),
                           MathTex(f"{r['comonotonic']:.1f}", font_size=28, color=MODEL_C),
                           MathTex(f"{r['worst_lo']:.1f}", font_size=28, color=BAD)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.9 * j, 0])
        foot = wrapped_label('the 99\\% VaR of a sum of three Pareto losses; the worst case by the rearrangement algorithm with 1,000 quantiles (two heuristic grids differ by less than 0.3 here; truncated upper endpoint and local search prevent certified bounds)', 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        a, b = ra["rows"][0], ra["rows"][-1]
        with self.voiceover(
            f"The reported Pareto exercise uses one thousand tail quantiles. <bookmark mark='a'/> At exponent three, simulated independence gives {a['independent']:.1f}, comonotonicity {a['comonotonic']:.1f}, and the lower-grid rearrangement estimate {a['worst_lo']:.1f}. <bookmark mark='b'/> At exponent one and a half, that estimate is {b['worst_lo']/b['comonotonic']:.1f} times the comonotonic value. Agreement of two heuristic grids does not certify the continuum optimum, and a Monte Carlo independent quantile has its own error. The analytic sum-of-ES bound is a separate rigorous statement for integrable losses."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
            vo.wait_until("a")
            self.play(Indicate(tab[1], scale_factor=1.01))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
        self.wait(0.4)
        self.clear_scene()

    def es_bound(self):
        rows = [cmath(r"\sup_C \text{ES}_\alpha\Bigl(\textstyle\sum_j L_j\Bigr)", r"=", r"\textstyle\sum_j \text{ES}_\alpha(L_j)",
                      font_size=38, colors={r"\textstyle\sum_j \text{ES}_\alpha(L_j)": ES_C}),
                cmath(r"\text{worst VaR}", r"\le", r"\text{sum of ESs}", font_size=40)]
        whys = [why(r"ES is subadditive and adds up exactly for comonotonic losses: so its worst case is simply the sum"),
                why(r"and since VaR is at most ES, the sum of the ESs bounds the worst VaR too")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.7, edge=6.9)
        with self.voiceover(
            "Expected shortfall is better behaved again. <bookmark mark='a'/> Because it is subadditive and adds up "
            "exactly when losses move together, its worst case over all dependence is just the sum of the individual "
            "shortfalls. <bookmark mark='b'/> And since VaR never exceeds ES, that sum also bounds the worst VaR. "
            "Coherence buys a usable bound."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def aggregation(self):
        cards = VGroup(
            desk_question(r"across risk types", 'market, credit and operational risk are measured separately and combined; adding VaRs equals the comonotonic benchmark under the stated quantile conditions, which for VaR may still understate',
                          width=12.4, font_size=19),
            desk_question(r"across desks", r"the firm's VaR from desk VaRs needs a joint model of all positions; with "
                          r"one, diversification credit is real but model-dependent", width=12.4, font_size=19),
            desk_question(r"what to report", r"the House reports its VaR with its dependence bound beside it, so a reader "
                          r"sees how much rests on the copula", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Across risk types, adding VaRs produces a comonotonic benchmark under the stated quantile conditions, not a safe upper bound under arbitrary dependence. <bookmark mark='a'/> Across desks, diversification depends on a common valuation, horizon and joint loss model. <bookmark mark='b'/> An analytic sum-of-ES bound requires integrable marginals and uses the same confidence. <bookmark mark='c'/> Report those rigorous assumptions separately from a grid rearrangement estimate, and from any approved firm-wide risk limit."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def estimation(self):
        n = 500
        z = stats.norm.ppf(0.99)
        se = np.sqrt(0.01 * 0.99 / n) / stats.norm.pdf(z)
        rows = [cmath(r"\text{se}(\hat q_\alpha)", r"\approx", r"\frac{\sqrt{\alpha(1 - \alpha)/n}}{f(q_\alpha)}", font_size=40),
                cmath(r"n = 500,\ \alpha = 99\%", r":", rf"\text{{se}} \approx {se:.2f}\,\sigma = {100 * se / z:.0f}\%\ "
                      r"\text{of VaR}", font_size=36, colors={r"n = 500,\ \alpha = 99\%": HURDLE}),
                cmath(r"\text{ES}", r":", r"\text{larger still: it averages five points}", font_size=36)]
        whys = [why(r"the sampling error of an empirical quantile: thin data where the density is low"),
                why(rf"for a normal, historical simulation's 99\% VaR on 500 days is uncertain by about {100 * se / z:.0f}\% "
                    r"of itself, one standard error"),
                why(r"and with fat tails, far more: model uncertainty and estimation error stack")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "And even with the model right, there is estimation error. <bookmark mark='a'/> An empirical quantile's "
            "standard error is the binomial one divided by the density, and the density is low in the tail. "
            "<bookmark mark='b'/> For historical simulation's ninety-nine percent VaR on five hundred normal days, about "
            f"{100 * se / z:.0f} percent of the VaR itself. <bookmark mark='c'/> Expected shortfall, averaging the five "
            "worst points, is noisier still, and fat tails make both worse."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def whale(self):
        cards = VGroup(
            desk_question(r"a lower number after a model change", r"chosen review case: old and new models use identical positions, prices, horizons and loss conventions", width=12.4, font_size=21),
            desk_question(r"independent implementation", r"check data timing, units, initialization and formulas; reproduce the comparison without changing the financial algorithms", width=12.4, font_size=21),
            desk_question(r"evidence before approval", r"a lower charge is not evidence of better calibration; compare losses, uncertainty and stress sensitivity under a predeclared design", width=12.4, font_size=21),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover("A chosen model-change review. <bookmark mark='a'/> Suppose a new model reports less risk. First hold positions, prices, horizons and loss conventions fixed. <bookmark mark='b'/> Independently check timing, units, initialization and formulas, rather than inferring improvement from a lower charge. <bookmark mark='c'/> Then compare calibration, uncertainty and stress sensitivity under a declared evaluation design. This is a governance illustration, with no unverified claim about a particular institution or an approved production deployment.") as vo:
            self.play(FadeIn(cards[0]))
            for k, mark in [(1,"b"),(2,"c")]:
                if k: vo.wait_until(mark)
                self.play(FadeIn(cards[k]))
        self.clear_scene()

    def question(self):
        q = pause_card(r"a neural network is trained to forecast tomorrow's 1\% quantile of US returns from recent "
                       r"volatility, fitted to 1926--1990. Will it beat a GARCH-filtered forecast on 1991--2020?")
        with self.voiceover(
            "Pause and predict. A neural network is trained to forecast tomorrow's one percent quantile of American "
            "returns from recent volatility, on nineteen twenty-six to ninety. Will it beat a GARCH-filtered forecast on "
            "the thirty years after?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
