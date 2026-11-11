from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import BAD, CONS, FRONT, GOOD, MKT, PART, SDF, TAN, load

DESK = [
    (r"Two assets, each with 20\% volatility and correlation 0.5. Minimum-variance weights and volatility?",
     r"half each, by symmetry; the variance is $0.25(0.04) + 0.25(0.04) + 2(0.25)(0.5)(0.04) = 0.03$, so the volatility "
     r"is 17.3\%: diversification takes off less than three points when the correlation is a half"),
    (r"Why is the security market line flatter than the CAPM says?",
     'one reading: investors who cannot borrow buy high-beta stocks to get more risk, bidding them up (Black, 1972; Frazzini and Pedersen, 2014). Betting against beta, levered low-beta long and high-beta short, earned 5.2\\% a year here retrospectively with whole-sample betas; no implementable BAB replication'),
    (r"An asset has a Sharpe ratio of 2. What does that say about any model that prices it?",
     'same-period $\\sigma(m)/E(m)\\ge2$ if 2 is the raw same-period Sharpe. If annualised from months, the monthly bound is $2/\\sqrt{12}$. Suspect first the data: selection, stale prices, or a tail that has not happened yet'),
    (r"Why does the equity premium need a risk aversion near 70?",
     r"consumption is smooth (1.9\% a year) and only loosely tied to stocks (correlation 0.39), so their covariance is "
     r"tiny: 8.8\% divided by 0.0013 is about 68. The same $\gamma$ then predicts a riskless rate far above the one seen"),
    ('A record-low dividend yield: what long-horizon alternatives remain? Does it fix the next return?',
     'by Campbell--Shiller, either returns are low or dividends grow fast (or the yield stays low for ever). retain the finite-horizon terminal yield and approximation error; the saved legacy diagnostic uses years 2--16 and does not certify next-return forecasts'),
    (r"The market's demand elasticity is 0.2. A fund moves 1\% of the market from bonds to stocks. Effect?",
     'under the cited local allocation-shock assumptions, prices rise approximately 5\\%, until other holders, the less constrained ones, sell enough to absorb it; with elasticity that low there are few of them'),
]

PROBLEMS = [
    r"By Lagrange, show the frontier's variance at mean $m$ is $(Cm^2 - 2Am + B)/D$ with $A = \mathbf{1}^\top\Sigma^{-1}"
    r"\mu$, $B = \mu^\top\Sigma^{-1}\mu$, $C = \mathbf{1}^\top\Sigma^{-1}\mathbf{1}$, $D = BC - A^2$.",
    r"Two assets: $\sigma_1$ = 20\%, $\sigma_2$ = 10\%, $\rho$ = 0.3. Find the minimum-variance weights and volatility.",
    "Show that the tangency portfolio's squared Sharpe ratio is $(\\mu - r_f)^\\top\\Sigma^{-1}(\\mu - r_f)$, and that it equals the square of the HJ coefficient-of-variation lower bound for same-period excess returns.",
    r"A mean return is estimated from 30 years of annual data with volatility 18\%. Find its standard error; how many "
    r"years would halve it?",
    r"Show that if the market portfolio is the tangency portfolio, $\mathbb{E}[R_i] - r_f = \beta_i(\mathbb{E}[R_m] - "
    r"r_f)$.",
    'Show that $m = a - bR_m$ prices every asset exactly when the CAPM holds, and find $a$ and $b$, using a known gross cash return. Does this linear pricing projection have to be positive?',
    r"In the lognormal CRRA model, derive $r_f = \delta + \gamma g - \gamma^2\sigma_c^2/2$. With $\delta$ = 1\%, $g$ = "
    r"$\sigma_c$ = 2\% and $\gamma$ = 10, what is $r_f$?",
    r"A disaster cuts consumption by $b$ = 29\%. With $\gamma$ = 4, by what factor does marginal utility rise? Why does a "
    r"1.7\% chance of it matter so much?",
    r"Derive the Campbell--Shiller approximation and $\rho = 1/(1 + e^{\overline{dp}})$; with $\overline{dp} = -3.25$, "
    r"find $\rho$.",
    r"Shleifer--Vishny with $V$ = 1, $S_1$ = 0.3, $S_2$ = 0.4, $F_1$ = 0.2, $a$ = 1.5: find $p_1$, $p_2$ and $F_2$.",    r"(qual) In Harrison and Kreps's model show that $P = \beta\max_i Q_i(d + P)$ has a unique solution, that "
    r"$P \ge \max_i V_i$, and compute $P$ for their example ($24/13$, $27/13$).",
    r"(qual) Show that if one type is the most optimistic in every state, $P = \max_i V_i$: the speculative premium "
    r"needs the identity of the optimist to change with the state.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("hook"), load("frontier"), load("capm"), load("hj"), load("puzzle"), load("shiller"),
                   load("intermediary"), load("bubbles"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=24, color=col), wrapped_label(t, 11.4, 21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, hk, f, c, h, p, s, im, b):
        o = f["oos"]
        items = [
            (rf"a dollar in 1926: \${hk['end_stocks']:,.0f} in stocks, \${hk['end_bills']:.0f} in bills", MKT),
            (rf"Markowitz: the frontier; the minimum-variance portfolio at {100 * f['gmv']['sd']:.1f}\% volatility",
             FRONT),
            (rf"Tobin: one risky portfolio for everyone; its Sharpe ratio {o['in_sharpe']:.2f} in sample, "
             rf"{o['oos_sharpe']:.2f} out; 1/N {o['eq_sharpe']:.2f}", TAN),
            (rf"the CAPM: the SML slope {100 * c['sml']['slope']:.1f}\% against a premium of "
             rf"{100 * c['mkt_prem']:.1f}\%; betting against beta", MKT),
            (f"$p = \\mathbb{{E}}[mx]$; Hansen--Jagannathan: 25 portfolios, annualised monthly Sharpe: {h['sr_ff25']:.2f}", SDF),
            (r"APT and ICAPM: many factors, if they are paid", FRONT),
            (rf"consumption and GMM: $\gamma$ = {p['gmm']['theta'][1]:.0f}, with a standard error of "
             rf"{p['gmm']['se'][1]:.0f}", CONS),
        ]
        items2 = [
            (rf"the puzzle: $\gamma \approx {p['gamma_implied']:.0f}$; habit, long-run risk and disasters as answers", BAD),
            (f"Shiller: $\\sigma(p)$ = {s['sd_p']:.2f} against $\\sigma(p^*)$ = {s['sd_pstar']:.2f}; finite-terminal illustration; shifted CS diagnostic", CONS),
            ('intermediaries: capital-risk point estimates positive in all seven classes; four approximate $t>1.96$', SDF),
            ('inelastic markets: cited local allocation-shock multiplier near five, conditional on identification', BAD),
            (r"behaviour and its limits: 3Com at minus \$22 billion; arbitrage fails when capital runs", BAD),
            (rf"bubbles: {b['n']} run-ups, {100 * b['p_crash']:.0f}\% crashed, yet {100 * b['mean_next']:+.0f}\% on "
             r"average after", MKT),
            (r"Rule 23: a standard error, a reason and a bad state for every premium", QC.HOUSE),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 23 in fourteen lines")
        with self.voiceover(
            "Part twenty-three in fourteen lines. A dollar in American stocks in 1926 became more than seventeen thousand; in bills, twenty-five. Markowitz drew the frontier of portfolios worth holding. Tobin showed that under the specified mean-variance and common financing assumptions investors share a risky tangency portfolio, and estimation error showed that its weights are almost unknowable: out of sample, equal weights did better. The CAPM said only beta is paid, and the security market line came out flat. One equation, price equals the expected discounted payoff, contains every model, and Hansen and Jagannathan bound its same-period coefficient of variation. Annualised monthly Sharpe must be divided by root twelve for a monthly bound. The APT and Merton's ICAPM allowed many factors, provided they are paid. Consumption models, estimated by GMM, need a risk aversion so large it is barely measured."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 23 in fourteen lines")
        with self.voiceover(
            "That is the equity premium puzzle, and habits, long-run risks and rare disasters are its candidate answers. Shiller found prices far more volatile than the dividends they forecast, and Campbell and Shiller motivated the study of return and cash-flow expectations; our saved diagnostic has a one-year indexing shift. All seven capital-risk point estimates are positive, with four approximate t-statistics above one point nine six; this is not joint or causal certification. The cited inelastic-market hypothesis proposes a local allocation-shock multiplier subject to identification assumptions. Behaviour creates mispricing, and arbitrage fails exactly when the arbitrageurs' money runs out. The selected run-up sample has substantial crash frequency but lacks an unconditional baseline and a timing guarantee. And the House's twenty-third rule asks every premium for its standard error, its reason, and the bad state in which it is paid."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q, a, width=12.4, font_size=22) for q, a in qs]).arrange(DOWN, buff=0.25)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. Two assets of twenty percent volatility and correlation a half: hold half of each, and the volatility is seventeen point three percent. <bookmark mark='a'/> The security market line is flat, on one reading, because investors who cannot borrow buy high-beta stocks for their risk, and bid them up; our mechanical BAB illustration uses future full-sample betas and does not certify implementable performance. <bookmark mark='b'/> An asset with a Sharpe ratio of two needs a same-period coefficient of variation of at least two if that is a raw same-period Sharpe; an annualised monthly value of two instead gives a monthly bound of two divided by root twelve; suspect the data before the theory."
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
            "The equity premium needs a risk aversion near seventy because consumption is smooth and only loosely tied to stocks. <bookmark mark='a'/> A low yield permits different long-horizon return, dividend-growth and terminal-yield paths, plus approximation error; it does not determine the next return. <bookmark mark='b'/> And with a demand elasticity of a fifth, a one-percent allocation-demand shock gives about five-percent price change only under the cited local model's assumptions, until the few unconstrained holders sell enough to absorb it. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        pages = [problem_set(PROBLEMS[a:b], font_size=21) for a, b in ((0, 6), (6, 10), (10, 12))]
        for page, start in zip(pages, (1, 7, 11)):
            for j, row in enumerate(page.rows):
                row[0].become(label(rf"{start+j}.", font_size=21, color=QC.IDEA).move_to(row[0], aligned_edge=RIGHT))
        with self.voiceover(
            "And twelve problems: the frontier by Lagrange; a two-asset minimum-variance portfolio; the tangency Sharpe "
            "ratio as the Hansen-Jagannathan bound; how many years a mean return needs; the CAPM derived, and its "
            "discount factor; the riskless-rate puzzle in numbers; marginal utility in a disaster; the Campbell-Shiller "
            "constant; and Shleifer and Vishny's prices by hand. Two more are qualifying-exam problems: Harrison "
            "and Kreps's fixed point, and when the premium vanishes. Solutions, in English and Chinese, are in the "
            "notes."
        ):
            for index, ps in enumerate(pages):
                self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=3))
                self.wait(4)
                if index < len(pages) - 1:
                    self.play(FadeOut(VGroup(ps.head, ps.rows)))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"Fama--MacBeth, GRS, and the factors: size, value, momentum, betting against beta", [24]),
            (r"hundreds of factors, trial counts, and a shrinkage SDF", [25]),
            (r"backtests that do not fool you", [26]),
            (r"machine-learned expected returns and a deep SDF", [27]),
            (r"portfolio construction under estimation error", [30]),
            (r"alternative premia, sized for their crashes", [32]),
        ])
        with self.voiceover(
            "Where this comes back. Part twenty-four tests factors with Fama-MacBeth regressions and the GRS test, "
            "beginning with betting against beta. Part twenty-five faces hundreds of them, with trial counts and a "
            "shrinkage discount factor. Part twenty-six builds backtests that do not fool their authors. Part "
            "twenty-seven learns expected returns and a discount factor by machine. Part thirty builds portfolios that "
            "survive estimation error, and Part thirty-two sizes alternative premia for their crashes."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Cochrane, \textit{Asset Pricing}; Campbell, \textit{Financial Decisions and Markets}; Back, \textit{Asset "
             r"Pricing and Portfolio Choice Theory}; Duffie, \textit{Dynamic Asset Pricing Theory}; Shleifer, "
             r"\textit{Inefficient Markets}"],
            [r"Markowitz (1952); Tobin (1958); Sharpe (1964); Lintner (1965); Black (1972); Merton (1973); Ross (1976); "
             r"Roll (1977); Lucas (1978); Breeden (1979); Shiller (1981); LeRoy and Porter (1981); Hansen and Singleton "
             r"(1982); Mehra and Prescott (1985); Campbell and Shiller (1988); Weil (1989); Epstein and Zin (1989); "
             r"Hansen and Jagannathan (1991); Campbell and Cochrane (1999); Bansal and Yaron (2004); Barro (2006); "
             r"DeMiguel, Garlappi and Uppal (2009); Cochrane (2011); Frazzini and Pedersen (2014)",
             r"De Long, Shleifer, Summers and Waldmann (1990); Shleifer and Vishny (1997); Barberis and Thaler (2003); "
             r"Lamont and Thaler (2003); Brunnermeier and Nagel (2004); He and Krishnamurthy (2013); Adrian, Etula and "
             r"Muir (2014); Greenwood and Shleifer (2014); He, Kelly and Manela (2017); Koijen and Yogo (2019); "
             r"Greenwood, Shleifer and You (2019); Gabaix and Koijen (2021). Data: Kenneth French's library; Robert "
             r"Shiller's data; FRED; He, Kelly and Manela's factors"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from Markowitz's twelve pages in 1952 to the inelastic markets hypothesis. Original public-data computations, named fixed-model illustrations and quoted published estimates are distinguished in the notes. Simplified reconstructions are not exact paper replications; visual review does not certify continuous production narration."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("research",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 24, Factors", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "That opens Act Four, on return premia, and the House's research desk. <bookmark mark='a'/> Next, Part "
            "twenty-four: factors. Size, value, momentum, profitability and low risk, each tested with the tools of "
            "this part and Part six, each given its history and its crashes, and each entered in the House's track "
            "record."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
