from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, DEBT, EQUITY, GBMC, HAZ, PART, RISKY, SENIOR, load

DESK = [('A 5-year CDS trades at 100 bp, recovery 40\\%. Annual default probability?',
  'Flat continuous-premium pricing intensity $\\lambda^Q\\approx1.67\\%$ per year; one-year event '
  'probability $1-e^{-\\lambda^Q}\\approx1.65\\%$, five-year about 8\\%. These are pricing probabilities '
  'under stated assumptions.'),
 ('Why are equity holders long volatility and bondholders short it?',
  'In the stated Merton comparison, fix total asset value, rates, maturity and debt face. Greater asset '
  'volatility raises call equity value and lowers debt value by the same dollars; percentage changes '
  'differ.'),
 ('Why can a senior tranche with a tiny expected loss deserve a wide spread?',
  'If losses occur when the pricing kernel is high, their risk-adjusted cost can be large despite low '
  'physical expected loss. Align maturity, recovery, liquidity and contract terms before comparing spreads.'),
 ('A default model scores 0.98 in sample and 0.90 out of sample. Which do you report?',
  'Report both scores, sample roles, event counts and uncertainty; prioritize independent evaluation and '
  'check calibration. A score gap combines adaptation and sampling variation; population shifts can alter '
  'both.')]

PROBLEMS = [
    r"In Merton's model show that the debt is worth $De^{-rT}N(d_2) + V_0N(-d_1)$, and derive the credit spread.",
    r"Show that equity volatility is $\sigma_E = N(d_1)\,\sigma_V V/E$. Why does it rise as the firm approaches default?",
    r"With a constant hazard $\lambda$, show that a CDS's par spread is $(1 - R)\lambda$ when premiums are paid "
    r"continuously.",
    r"A 3-year CDS trades at 120 bp, recovery 40\%, rates 4\%, annual premiums. Bootstrap a flat hazard rate by hand "
    r"(one iteration of the credit triangle is enough).",
    r"Derive Vasicek's large-pool distribution $\mathbb{P}(L \le x)$ from the one-factor model, and its 99.9\% quantile.",
    r"Compute the Basel capital $K$ for PD 2\%, LGD 45\%, $M$ = 2.5. Compare it with the expected loss.",
    r"In the homogeneous Gaussian large pool with fixed marginal PD and recovery, explain equity and super-senior loss sensitivity to correlation. Why need a bounded senior tranche not be monotone?",
    r"A logit's coefficient on leverage is 0.5 per standard deviation. By what factor does a two-standard-deviation "
    r"rise in leverage multiply the odds of default?",    r"(qual) For $N$ equal loans in Vasicek's model, show $\Pr(L \le k/N) = \int \operatorname{Bin}(k; N, p(y))\varphi(y)dy$ "
    r"and that the $\alpha$-quantile of $L$ tends to $p(\Phi^{-1}(\alpha))$ as $N \to \infty$.",
    r"(qual) For $L = \mu(Y) + \varepsilon U$ with $\mathbb E[U \mid Y] = 0$, derive the second-order expansion "
    r"$q_\alpha(L) = q_\alpha(\mu) - \frac{\varepsilon^2}{2h(y)}\frac{d}{dy}\big[h(y)\operatorname{Var}(U \mid y)/\mu'(y)\big] + "
    r"o(\varepsilon^2)$ at $y = q_\alpha(Y)$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("spreads"), load("kmv"),  load("vasicek"), load("copula"),
                   load("cjs"), load("march2020"), load("bdc"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, s, k, v, c, j, q, b):
        items = [
            (rf"Lehman's swaps settled at 8.625 cents; the Baa spread reached {s['max']['v']:.2f}\% in December 2008",
             BAD),
            (r"a spread pays for expected loss, a premium for bad times, and illiquidity", RISKY),
            (r"Merton: equity as a call; model spreads depend on leverage, volatility, maturity and the asset cushion",
             EQUITY),
            (rf"retrospective month-end fit: Norwegian Cruise Line fell to {k['NCLH']['worst']['dtd']:.2f} in 2020",
             DEBT),
            (r"first passage and Leland's chosen barrier; default as a random clock; survival as discounting", HAZ),
            (r"the CDS: two legs, a bootstrapped hazard curve, the Big Bang's coupons and upfronts", RISKY),
            (r"bankruptcy labels need event, coverage, population, horizon and vintage audits", BAD),
            (r"Altman's score, logit and trees: independent synthetic assessment; no sealed issuer results", GBMC),
            (f"stylized corporate IRB: a 1\\% PD gives a {100 * v['rw_1pct']:.2f}\\% risk weight under these rules", SENIOR),
            ('copulas change joint tails at fixed margins; tranche sensitivity depends on the loss slice and pricing assumptions', RISKY),
            (rf"a senior tranche loses only in the worst {100 * j['threshold_pct']:.2f}\% of states: a catastrophe bond",
             SENIOR),
            (r"the London Whale: \$6.2 bn in trading losses; hedge, model and control failures", BAD),
            (r"March 2020 ETF price changes and BDC valuation marks: different claims and observation clocks", DEBT),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        title = label(r"Part 20 in thirteen lines", font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(title, DOWN, buff=0.3)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.7:
            rows.scale_to_fit_height(6.7)
        with self.voiceover(
            "Part twenty in thirteen lines. A promise is worth what its maker can pay; the Lehman CDS auction set an eight point six two five cent settlement price. Corporate spreads combine expected losses, risk premia and other frictions. Merton models equity as a call, under restrictive assumptions. Distances fitted retrospectively to prices illustrate leverage and volatility, rather than certified live forecasts. Barriers bring default forward, and Leland lets shareholders choose. Intensity models treat default as a random clock and require a stated recovery convention. CDS prices equate premium and protection legs. Bankruptcy labels require event, coverage, denominator and availability audits. Altman's score, logit and trees are demonstrated on a declared synthetic population, with no sealed issuer results. Vasicek's homogeneous large pool motivates a stylized bank capital formula. Copulas change joint tail risk, and tranches have nonlinear dependence sensitivities. Senior losses concentrated in bad aggregate states can command a risk premium. The London Whale illustrates hedge, model and control failures. March twenty twenty and reported BDC marks show why market prices, accounting values and total returns must be distinguished."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=24))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=23) for q, a in DESK]).arrange(DOWN, buff=0.25)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Four desk questions. At one hundred basis points and forty percent recovery, the flat continuous-premium approximation gives risk-neutral intensity one point six six seven percent and a one-year event probability about one point six five percent. <bookmark mark='a'/> In Merton's fixed-asset-value comparison, equity gains from asset volatility and debt loses value. <bookmark mark='b'/> A senior loss concentrated in high-value bad states can command a substantial premium, conditional on a pricing kernel and comparable contract terms. <bookmark mark='c'/> Report independent model assessment with event counts, uncertainty and population limits, and check calibration separately. The worked notes give the assumptions and full solutions."
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
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "And ten problems: Merton's debt and spread, the equity's volatility, the par spread with a flat "
            "hazard, a bootstrap by hand, Vasicek's distribution, the Basel capital for a two percent PD, tranches "
            "and correlation, and the odds in a logit. Two are qualifying-exam problems: the exact finite-pool "
            "distribution, and the granularity expansion. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"counterparty risk: unilateral CVA values discounted default loss on positive exposure", [21]),
            (r"the distress puzzle and credit factors among the anomalies", [25]),
            (r"backtests that audit historical versions and actual publication dates", [26]),
            (r"machine learning on firm characteristics, at scale", [27]),
            (r"the finale: the House's credit book under a copula with fat tails", [43]),
        ])
        with self.voiceover(
            "Where this returns. Part twenty-one introduces counterparty risk, valuation adjustments and clearing. Unilateral CVA resembles protection on a random positive exposure, with important dependence and close-out assumptions. Part twenty-five revisits distress-related return patterns. Parts twenty-six and twenty-seven develop backtesting and machine learning, where historical data versions, publication timestamps and independent assessment require explicit audits. This part does not certify the legacy accounting dataset as point in time. The finale returns to dependence and stress scenarios for the House's credit book."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"O'Kane, \textit{Modelling Single-name and Multi-name Credit Derivatives}; Sch\"onbucher, \textit{Credit "
             r"Derivatives Pricing Models}; Duffie and Singleton, \textit{Credit Risk}; Lando, \textit{Credit Risk "
             r"Modeling}; Hull, \textit{Options, Futures, and Other Derivatives}, ch.\ 24--25"],
            [r"Altman (1968); Merton (1974); Black and Cox (1976); Jensen and Meckling (1976); Leland (1994); Jarrow and "
             r"Turnbull (1995); Lando (1998); Duffie and Singleton (1999); Li (2000); Collin-Dufresne, Goldstein and "
             r"Martin (2001); Shumway (2001); Vasicek (2002); Gordy (2003); Crosbie and Bohn (2003)",
             r"Andersen and Sidenius (2004); Getmansky, Lo and Makarov (2004); Vassalou and Xing (2004); Longstaff, "
             r"Mithal and Neis (2005); Bharath and Shumway (2008); Campbell, Hilscher and Szilagyi (2008); Coval, Jurek "
             r"and Stafford (2009); Huang and Huang (2012); Bai, Bali and Wen (2019); Haddad, Moreira and Muir (2021); "
             r"Dickerson, Mueller and Robotti (2023)",
             r"FCIC report (2011); JPMorgan Chase Task Force report and U.S. Senate PSI report (2013); IMF GFSR (April "
             r"2024); Federal Reserve press releases (March--April 2020)"])
        with self.voiceover(
            'The notes distinguish textbooks, original research, official records and descriptive public data. Numerical results include fixed model illustrations and the separately named synthetic classification lesson; they are not all empirical estimates. Original source files and House algorithms remain preserved. The public filing-count reconstruction failed upstream, so we report no count-based result from it. No sealed issuer experiment is opened during this review.'
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("credit",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 21, Counterparty Risk, XVA and Clearing", font_size=30, color=QC.IDEA).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "That opens the House's credit desk: default probabilities from two sources, a swap pricer, and the "
            "models that set capital. <bookmark mark='a'/> Next, Part twenty-one: counterparty risk, valuation "
            "adjustments and clearing. Every derivative is also a loan to whoever is on the other side."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
