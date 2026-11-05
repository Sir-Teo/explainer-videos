from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant40.common import (
    BAD,
    ES_C,
    GOOD,
    HIT_C,
    MODEL_C,
    PART,
    TAIL_C,
    VAR_C,
    load,
)

DESK = [
    (r"Your 99\% one-day VaR is \$10m. Ten-day? What did you assume?",
     r"$\sqrt{10} \times 10 = \$31.6$m, assuming iid normal days; on the US market since 1926 the ten-day ratio is "
     r"3.4, and 4.2 in the 1970s"),
    (r"Why is VaR not a coherent risk measure?",
     r"it is not subadditive: two independent bonds with 95\% VaRs of zero have a joint VaR of a full default; ES is "
     r"coherent"),
    (r"How do you backtest a VaR model?",
     r"count the exceptions (Kupiec), test their independence (Christoffersen), and apply the traffic light; look at "
     r"decades, not a year"),
    (r"How do you say anything about losses beyond the data?",
     r"extreme-value theory: a generalised Pareto tail beyond a threshold, after filtering volatility; the US tail "
     r"exponent is about five"),
    (r"What does correlation miss?",
     r"tail dependence: the Gaussian copula has none; banks and insurers crash together 0.67 of the time against its "
     r"0.40"),
    (r"Can expected shortfall be backtested?",
     r"not on its own: it is not elicitable; jointly with VaR it is (Fissler--Ziegel), and Acerbi--Székely's test uses "
     r"VaR's exceptions"),
]

PROBLEMS = [
    r"A normal daily loss with $\sigma = 1\%$ and zero mean: VaR and ES at 99\% and at 97.5\%.",
    r"Daily returns with autocorrelation 0.1 at every lag-one step (AR(1)): the factor that replaces $\sqrt{10}$.",
    r"Two independent bonds each lose 100 with probability 3\%: the 95\% VaR of each and of both.",
    r"Eight exceptions of a 99\% VaR in 250 days: Kupiec's statistic, its $p$-value and the traffic-light zone.",
    r"Ten exceptions in 1,000 days, four of them on the day after another: the estimates of $\pi_{01}$ and "
    r"$\pi_{11}$, and what they say.",
    r"Threshold 2\%, $\xi = 0.2$, $\beta = 0.8\%$, 400 exceedances in 10,000 days: VaR and ES at 99.9\%.",
    r"A $t$ copula with $\rho = 0.5$ and $\nu = 4$: its tail-dependence coefficient.",
    r"A portfolio with daily standard deviation \$2m: the distance of the most plausible \$16m loss, and its direction.",
    r"Three Pareto losses with exponent 2 (VaR 9, ES 19 each at 99\%): an upper bound on the worst-case VaR of the sum.",
    r"A 10-day ES of \$5m on a book with a 60-day liquidity horizon: the scaled ES under FRTB's square-root rule.",
    r"(qual) Prove that the pinball loss elicits the quantile, that elicitable functionals have convex level sets, "
    r"and that ES is not elicitable; derive the Rockafellar--Uryasev representation.",
    r"(qual) Show that $\mathbb E[Z_2] = 0$ when VaR and ES are correct for a continuous loss, and that for the true VaR "
    r"the FZ0 expected score is minimised in $e$ at the true ES.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("backtest"), load("evt"), load("depend"), load("stress"), load("ra"), load("learned"),
                   load("research"), load("sqrt"))
        self.lessons()
        self.formulas()
        self.connections()
        self.desk()
        self.answers()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, b, e, d, s, ra, L, r, sq):
        n, g = b["methods"]["normal"], b["methods"]["gjr_fhs"]
        r2 = [x for x in ra["rows"] if x["theta"] == 2.0][0]
        items = [
            (r"VaR is a quantile: how often, never how much; ES is the mean beyond it", VAR_C),
            (rf"the square root of time understates: 10-day over 1-day is {sq['direct'] / sq['one_day']:.1f}, not 3.16",
             BAD),
            (r"VaR is not subadditive; ES is coherent, and spectral measures generalise it", ES_C),
            (rf"normal VaR, 1928--2020: {100 * n['rate']:.2f}\% exceeded, in clusters; GJR-filtered HS passes", HIT_C),
            (rf"tails are Pareto with exponent about {1 / e['xi']:.0f}: EVT reaches beyond the data", TAIL_C),
            (r"the Gaussian copula has no tail dependence; markets do", TAIL_C),
        ]
        items2 = [
            (rf"reverse stress: a \$10m day is {s['rev'][1]['distance']:.1f} std devs away; history took costlier routes", BAD),
            (rf"unknown dependence: worst VaR {r2['worst_lo'] / r2['comonotonic']:.1f}$\times$ the sum of VaRs", VAR_C),
            (r"CAViaR and a network did not beat a GARCH filter out of sample", MODEL_C),
            (r"FRTB: 97.5\% ES, liquidity horizons, stressed calibration", ES_C),
            (r"liquidity is a second risk: exit cost grows like $\sqrt{Q/V}$", MODEL_C),
            (r"research: VaR elicitable, ES not, the pair jointly; Z$_2$ sees what Kupiec misses", GOOD),
            (r"Rule 40: a risk number is a forecast, reported with its backtest", QC.HOUSE),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 40 in thirteen lines")
        with self.voiceover(
            "Part forty in thirteen lines. Value at risk is a quantile: it says how often, never how much, and expected "
            "shortfall is the mean beyond it. The square root of time understates ten-day risk. VaR is not subadditive; "
            "expected shortfall is coherent. A normal VaR was exceeded twice as often as promised, in clusters, while a "
            "GARCH-filtered one passed. Tails are Pareto, with an exponent near five. And the Gaussian copula has no "
            "tail dependence, while markets do."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 7)), r"Part 40 in thirteen lines")
        with self.voiceover(
            "The most plausible way to lose a given amount is a formula, and history takes costlier routes. Unknown "
            "dependence can push VaR far above the sum of its parts. Learned quantile models did not beat a GARCH filter. "
            "Regulation moved to expected shortfall with liquidity horizons, and liquidity is a second risk of its own. "
            "The research chapter proved what can be backtested. And the House's rule: a risk number is a forecast, "
            "reported with its backtest."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"a risk number is a forecast", r"it can be tested like any other, and should be reported with "
                          r"its record", width=12.4, font_size=19),
            desk_question(r"volatility first, then tails", r"most of what makes risk forecasts fail is ignoring "
                          r"volatility clustering; the tail shape matters once that is fixed", width=12.4, font_size=19),
            desk_question(r"what the model cannot see", r"dependence in the tail, liquidity, and scenarios the window "
                          r"never held: report them beside the number, not inside it", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> A risk number is a forecast, testable like any other, and it should be "
            "reported with its record. <bookmark mark='b'/> Volatility first, then tails: most failures come from "
            "ignoring clustering. <bookmark mark='c'/> And what the model cannot see, tail dependence, liquidity and "
            "unseen scenarios, belongs beside the number, not hidden inside it."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def formulas(self):
        rows = VGroup(
            MathTex(r"\text{ES}_\alpha = \tfrac{1}{1 - \alpha}\int_\alpha^1 \text{VaR}_u\,du = \min_v\{v + "
                    r"\tfrac{1}{1 - \alpha}\mathbb E(L - v)^+\}", font_size=30, color=ES_C),
            MathTex(r"\text{LR}_{uc} = -2\log\frac{p^x(1 - p)^{T - x}}{\hat p^x(1 - \hat p)^{T - x}},\quad Z_2 = "
                    r"\tfrac{1}{T(1 - \alpha)}\sum \tfrac{L_tI_t}{\text{ES}_t} - 1", font_size=28, color=HIT_C),
            MathTex(r"\text{VaR}_\alpha = u + \tfrac\beta\xi\bigl[(\tfrac{n}{N_u}(1 - \alpha))^{-\xi} - 1\bigr]",
                    font_size=30, color=TAIL_C),
            MathTex(r"\lambda_L^{t} = 2\,t_{\nu+1}\bigl(-\sqrt{(\nu + 1)(1 - \rho)/(1 + \rho)}\bigr),\quad "
                    r"\lambda_L^{\text{Gauss}} = 0", font_size=28, color=TAIL_C),
            MathTex(r"x^* = -\tfrac{L}{w^\top\Sigma w}\,\Sigma w,\quad d^* = L/\sqrt{w^\top\Sigma w}", font_size=30,
                    color=BAD),
            MathTex(r"S(v, e; r) = -\tfrac{\mathbf 1\{r \le v\}(v - r)}{\tau e} + \tfrac ve + \log(-e) - 1",
                    font_size=30, color=VAR_C),
        ).arrange(DOWN, buff=0.3)
        head = label(r"The part on one card", font_size=34).to_edge(UP, buff=0.4)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "The part on one card. Expected shortfall two ways. Kupiec's ratio and the Z two statistic. The "
            "peaks-over-threshold quantile. Tail dependence, for the t and the Gaussian. The most plausible stress "
            "scenario. And the joint score for VaR and expected shortfall."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.4, run_time=6))
            self.wait(2)
        self.clear_scene()

    def connections(self):
        cards = VGroup(
            desk_question(r"backwards", r"Part 2's margin and Kupiec, Part 7's GARCH and EWMA, Part 20's copula, Part "
                          r"21's exposure, Part 30's CVaR and Part 37's impact all meet in the risk report", width=12.4,
                          font_size=19),
            desk_question(r"sideways", r"Part 26's backtests of strategies and this part's backtests of risk are the "
                          r"same idea: a forecast scored on data it never saw", width=12.4, font_size=19),
            desk_question(r"forwards", r"Part 41's crises are where risk numbers fail together: leverage, liquidity and "
                          r"fire sales that no single desk's VaR contains", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How this part connects. <bookmark mark='a'/> Backwards: Part two's margin, Part seven's volatility models, "
            "Part twenty's copula, Part thirty's CVaR and Part thirty-seven's impact all meet in the risk report. "
            "<bookmark mark='b'/> Sideways: Part twenty-six's backtests of strategies and this part's backtests of risk "
            "are the same idea. <bookmark mark='c'/> Forwards: Part forty-one's crises are where risk numbers fail "
            "together."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=20) for q_, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. Ten-day VaR from one-day? The square root of ten, if days are independent and normal, "
            "and more on real data. <bookmark mark='a'/> Why is VaR not coherent? It is not subadditive. "
            "<bookmark mark='b'/> How do you backtest it? Count the exceptions and test their timing."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
        cards = page(DESK[3:])
        with self.voiceover(
            "Beyond the data? Extreme-value theory. <bookmark mark='a'/> What does correlation miss? Tail dependence. "
            "<bookmark mark='b'/> And can expected shortfall be backtested? Not alone; with VaR, yes. Full solutions are "
            "in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def answers(self):
        cards = VGroup(
            desk_question(r"Research: is the variance elicitable?", r"no: $\delta_{-1}$ and $\delta_{+1}$ each have "
                          r"variance 0, their half-half mixture has variance 1, so its level sets are not convex",
                          width=12.4, font_size=20),
            desk_question(r"but jointly with the mean", r"yes: the mean and the second moment are each elicitable by "
                          r"squared error, and the variance is a function of the pair, like ES with VaR", width=12.4,
                          font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The research chapter's pause, answered. <bookmark mark='a'/> No: a point mass at minus one and one at plus one "
            "each have zero variance, and their even mixture has variance one, so the level set is not convex. "
            "<bookmark mark='b'/> But the mean and the second moment are each elicitable by squared error, and the "
            "variance is a function of the pair: the same structure as expected shortfall with VaR."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: normal VaR and shortfall; the square root under autocorrelation; non-subadditivity; "
            "Kupiec and the traffic light; clustering; an extreme-value quantile; tail dependence; reverse stress; a "
            "dependence bound; and liquidity horizons. Then two qualifying-exam problems: elicitability in full, and the "
            "shortfall tests' foundations. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"leverage, liquidity spirals and the crises where risk numbers fail together", [41]),
            (r"machines that trade on, and set off, the risks measured here", [42]),
            (r"whether a strategy's returns pay for the risk it takes", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part forty-one follows leverage and liquidity into the crises where risk numbers "
            "fail together. Part forty-two lets machines trade on the risks measured here. And Part forty-three asks "
            "whether anyone's returns pay for the risks they take."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"McNeil, Frey and Embrechts, \textit{Quantitative Risk Management} (2015); Jorion, \textit{Value at Risk} "
             r"(2006); Föllmer and Schied, \textit{Stochastic Finance}, ch.~4 (2016); Hull, \textit{Risk Management and "
             r"Financial Institutions} (2018)"],
            [r"Kupiec (1995); RiskMetrics (1996); Christoffersen (1998); Artzner, Delbaen, Eber and Heath (1999); McNeil "
             r"and Frey (2000); Rockafellar and Uryasev (2000); Acerbi and Tasche (2002); Embrechts, McNeil and Straumann "
             r"(2002); Engle and Manganelli (2004)",
             r"Gneiting (2011); Embrechts, Puccetti and Rüschendorf (2013); Acerbi and Székely (2014); Fissler and Ziegel "
             r"(2016); Ziegel (2016); Nolde and Ziegel (2017); Patton, Ziegel and Chen (2019). Data: Kenneth French's "
             r"library, to 2020"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from Kupiec's test to the joint score. Every "
            "number on screen was computed by the House's code from Kenneth French's daily returns through twenty twenty, "
            "the research window, or from simulation."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("portfolio",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 41, Leverage, Liquidity and Crises", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House can now say how much it might lose, and how it would know if it were wrong. <bookmark mark='a'/> "
            "Next, Part forty-one: leverage, liquidity and crises. Bank runs, fire sales and the spirals in which every "
            "risk number fails at once."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
