from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.quant import *  # noqa: F403
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
            f"Chapter seven, and the answer to the pause: about {r['worst_lo']:.0f}. Not twenty-seven, the sum of the "
            f"three VaRs, which is what perfect dependence gives, but about {r['worst_lo'] / r['comonotonic']:.1f} times "
            "that. With heavy tails, the worst dependence for VaR is not the one where everything moves together."
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
                vo.wait_until(m_)
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
                why(r"the rows' sums become as equal as possible; their minimum is the worst VaR")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The algorithm. <bookmark mark='a'/> Discretise each loss's tail beyond alpha into N quantiles, one column "
            "each. <bookmark mark='b'/> Paul Embrechts, Giovanni Puccetti and Ludger Rüschendorf's rearrangement: order "
            "each column opposite to the sum of the others, and repeat until nothing changes. <bookmark mark='c'/> The "
            "row sums become as equal as possible, and the smallest of them is the worst VaR."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
        note_ = label(r"start: comonotonic, every column in the same order", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Six quantiles of three Pareto losses, to see it work. <bookmark mark='a'/> At the start every column is in "
            "the same order: the comonotonic case, where the smallest row sum is the sum of the three VaRs. "
            "<bookmark mark='b'/> Each pass reorders a column against the others. <bookmark mark='c'/> The large values "
            "spread across rows, the row sums even out, and the smallest of them rises: the worst-case VaR."
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
                                                                         r"comonotonic (sum of VaRs)", r"worst case")])
        tab = VGroup(head)
        for r in ra["rows"]:
            tab.add(VGroup(MathTex(f"{r['theta']:g}", font_size=28), MathTex(f"{r['independent']:.1f}", font_size=28, color=GOOD),
                           MathTex(f"{r['comonotonic']:.1f}", font_size=28, color=MODEL_C),
                           MathTex(f"{r['worst_lo']:.1f}", font_size=28, color=BAD)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.9 * j, 0])
        foot = wrapped_label(r"the 99\% VaR of a sum of three Pareto losses; the worst case by the rearrangement algorithm "
                             r"with 1,000 quantiles (bounds from both grids agree to within 0.3)", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        a, b = ra["rows"][0], ra["rows"][-1]
        with self.voiceover(
            "The numbers, for three losses at ninety-nine percent. <bookmark mark='a'/> With a tail exponent of three, "
            f"independence gives {a['independent']:.1f}, perfect dependence {a['comonotonic']:.1f}, and the worst case "
            f"{a['worst_lo']:.1f}. <bookmark mark='b'/> As the tails grow heavier the gap widens: with an exponent of one "
            f"and a half, the worst case is {b['worst_lo'] / b['comonotonic']:.1f} times the sum of the VaRs. Adding up "
            "VaRs, which many firms do across risk types, is not a safe upper bound."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
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
            desk_question(r"across risk types", r"market, credit and operational risk are measured separately and "
                          r"combined; adding them assumes perfect dependence, which for VaR may still understate",
                          width=12.4, font_size=19),
            desk_question(r"across desks", r"the firm's VaR from desk VaRs needs a joint model of all positions; with "
                          r"one, diversification credit is real but model-dependent", width=12.4, font_size=19),
            desk_question(r"what to report", r"the House reports its VaR with its dependence bound beside it, so a reader "
                          r"sees how much rests on the copula", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Where this bites. <bookmark mark='a'/> Across risk types, market, credit and operational losses are measured "
            "apart and combined; adding them assumes perfect dependence, which for VaR may still understate. "
            "<bookmark mark='b'/> Across desks, a firm's VaR needs a joint model, and its diversification credit is real "
            "but depends on that model. <bookmark mark='c'/> So the House reports its VaR with the dependence bound "
            "beside it."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def whale(self):
        cards = VGroup(
            desk_question(r"a model change", r"in January 2012 JPMorgan's Chief Investment Office moved its synthetic "
                          r"credit book to a new VaR model, which roughly halved the reported VaR, as the bank's own task "
                          r"force and a US Senate report described", width=12.4, font_size=18),
            desk_question(r"built in a spreadsheet", r"the reports described manual copying between spreadsheets and a "
                          r"formula error that divided by a sum instead of an average, muting volatility", width=12.4,
                          font_size=18),
            desk_question(r"the loss", r"the book lost about \$6.2 billion in 2012, as reported; the lesson is that a "
                          r"model change that lowers risk is the one most in need of independent review", width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Model risk, from the public record. <bookmark mark='a'/> In January twenty twelve, JPMorgan's Chief "
            "Investment Office moved its synthetic credit book to a new VaR model, which roughly halved the reported "
            "number, as the bank's own task force and a United States Senate report later described. "
            "<bookmark mark='b'/> The reports described a model run in spreadsheets, with manual copying and a formula "
            "that divided by a sum instead of an average, muting volatility. <bookmark mark='c'/> The book lost about "
            "six point two billion dollars that year, as reported. A model change that lowers risk is the one most in need "
            "of review."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
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
        self.wait(0.5)
        self.clear_scene()
