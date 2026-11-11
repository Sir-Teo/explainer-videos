from __future__ import annotations

import math

from explainer.quant import *  # noqa: F403
from explainer.quant.house import riskmodel as RM
from videos.quant.quant31.common import (BAD, COST_C, FAC_C, GOOD, GP_C, HURDLE, IC_C, PART, REAL_C, SPEC_C, comma,
                                         exact_ic_ir, load)

DESK = [('Fixed normalised-score toy: latent mean 0.05, sd 0.10, N=500, independent months. Annual IR?',
  'usual small-correlation benchmark $0.05\\sqrt{6000}=3.87$; exact toy '
  '$\\sqrt{12}\\,0.05/\\sqrt{0.01+0.9875/500}=1.583$'),
 ('Bias statistic 1.30 over T=504 daily observations. Interpretation?',
  'realised standardised-return dispersion is 30\\% above one; IID Gaussian reference '
  '$1\\pm\\sqrt{2/504}\\approx1\\pm0.063$, with no automatic validity for dependent or fat-tailed data'),
 ('Factor-neutral book forecasts 4\\% annual volatility and loses 10\\% in a week. Contradiction?',
  'no: a forecast is not a loss bound; omitted covariance, leverage, jumps, changing risk or model error can '
  'matter'),
 ('Fixed gross return: net 6\\% at 100m after 2\\% square-root costs. Net at 400m?',
  'holding gross return and cost technology fixed, costs double to 4\\%; gross 8\\% then nets 4\\%, before '
  'any additional costs'),
 ('Quadratic cost quadruples. Does GP speed halve?',
  'approximately in the negligible-discount regime $\\gamma\\ll\\lambda\\ll\\gamma/\\rho^2$; at fixed '
  'positive discount the extreme-cost rate instead scales as $1/\\lambda$'),
 ('Fixed example: floor variances, then cap positions. What has been established?',
  'the floor changes a risk input; the cap bounds notional holdings. Neither validates forecasts or '
  'establishes future profitability')]

PROBLEMS = ['In the fixed normalised-score toy, compute annual IR for latent mean 0.05, sd 0.10, N=500 and independent '
 'months; compare the small-correlation benchmark.',
 'At T=504, compute the approximate IID standard-normal 95\\% reference band for the sample SD of '
 'standardised returns. Is 1.30 inside?',
 'Known Gaussian prior: beta mean 1.0, sd 0.3; estimate 1.8 with known Gaussian SE 0.3. Derive the posterior '
 'mean.',
 'With fixed gross return, net 6\\% at 100 m after 2\\% square-root costs: compute net return at 400 m.',
 'For fixed positive g,c and profit $gA-cA^{3/2}$, break-even is 900 m. Derive profit-maximising size and '
 'net return before fees.',
 'With zero discount and $\\lambda\\gg\\gamma$, derive the GP trade-rate approximation and effect of '
 'quadrupling cost.',
 'Two standardised finite-variance scores each have population Pearson IC 0.04 and score correlation 0.5. '
 'Derive the maximum combined Pearson IC.',
 'For stationary unit-variance scores with lag correlations 1-0.02 and 1-0.32, derive the ratio of RMS '
 'changes. What extra assumptions convert it to a turnover ratio?',
 'A fund returned 12\\%; average beta 0.4, sample market return 20\\%, exposure--next-return covariance term '
 '2\\%. Compute the residual term.',
 'In the toy with independent monthly latent mean 0.03 and sd 0.06, derive the annual asymptotic IR and '
 'persistent-versus-diversifiable variance crossover $N^*$.',
 '(qual) Under the stated bounded-latent-correlation and normalised-score assumptions prove '
 '$IR=\\mu/\\sqrt{\\sigma^2+(1-\\mu^2-\\sigma^2)/N}$. Prove monotonicity for $\\mu>0$, the limit, and the '
 'exact continuous-crossover ratio $1/\\sqrt 2$.',
 '(qual) For the scalar Bellman timing in Chapter 5, derive the quadratic value coefficients, Riccati '
 'equation, trade rate and aim multiplier. State model assumptions and distinguish fixed-positive-discount '
 'from negligible-discount cost asymptotics.']


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("law"), load("model"), load("vasicek"), load("costs"), load("gp"), load("combine"),
                   load("attribution"), load("quake"), load("theory"))
        self.desk()
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

    def recap(self, l, m, v, c, g, cb, a, q, th):
        cur = {r["aum"]: r["sharpe"] for r in c["curve"]}
        r32 = g["rows"][-1]
        mined = [r for r in th["coins"] if r["signal"] == "mined"][0]
        per = exact_ic_ir(0.05, 0.10, 500) * math.sqrt(12)
        items = [
            (rf"the fundamental law: $IR = TC\cdot IC\sqrt{{BR}}$; long only transfers {l['tc_long_only']:.2f}", IC_C),
            (rf"factor risk models: $X F X^\top + \Delta$; median forecast factor fraction {100 * m['fac_share']:.0f}\%", FAC_C),
            (rf"the bias statistic: forecasts tested, {m['bias']['equal-weighted coins'][0]:.2f} for the equal-weighted coins",
             FAC_C),
            (rf"Vasicek's betas: error {v['mse']['raw']:.3f} $\to$ {v['mse']['shrunk']:.3f}", SPEC_C),
            (rf"the square-root law: \$1 million costs {100 * c['cost_1m']:.1f}\% at separate pooled median inputs", COST_C),
            (rf"capacity: Sharpe {c['gross_sharpe']:.2f} gross, {cur[1e5]:.2f} at \$100k, {cur[1e6]:.2f} at \$1m", COST_C),
            (rf"Garleanu--Pedersen: at $\lambda = 32$, {r32['gp']:.2f} against myopic {r32['myopic']:.2f}", GP_C),
        ]
        items2 = [
            (r"multi-period optimisation: plan far, trade one step, re-plan", GP_C),
            (rf"combination: the regression {cb['combos']['ridge 0']['valid']:.3f} in 2020, equal weights "
             rf"{cb['combos']['equal']['valid']:.3f}", HURDLE),
            (r"capacity at $\frac49$ of break-even; Berk--Green model: zero expected risk-adjusted net alpha", HURDLE),
            (rf"August 2007: {100 * q['aug']['20070808']:.2f}\% and {100 * q['aug']['20070809']:.2f}\% in two days on the "
             r"industries", BAD),
            (rf"attribution: the mined alpha factor/total variance ratio {100 * a['var_share_factor']:.0f}\%, specific Sharpe "
             rf"{a['sharpe_specific']:.2f}", SPEC_C),
            (r"protocol and fixed limits: risk inputs differ from independent position caps", BAD),
            (rf"research: $IR = \mu/\sqrt{{\sigma^2(1-1/N) + (1 - \mu^2)/N}}$; the hook's 3.87 is {per:.2f}", REAL_C),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 31 in fourteen lines")
        with self.voiceover(
            'Part thirty-one in fourteen lines. The breadth benchmark needs calibration and covariance assumptions. Factor models reduce covariance parameters conditional on exposures; their forecasts still need diagnostics. The saved beta comparison uses noisy future estimates and eligible survivors. Square-root execution costs are scenario dependent. Dynamic trading is optimal only within the specified signal, risk, cost and discount model.'
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 31 in fourteen lines")
        with self.voiceover(
            'Multi-period optimisation makes horizon and constraints explicit. The research combination comparison is selected and reused, rather than independent holdout evidence. Fixed-input capacity and ideal rational-flow models clarify incentives. The industry quake proxy differs from actual fund books. Attribution is model-dependent accounting. Fixed arithmetic distinguishes risk floors from independent position caps. The research theorem is exact for bounded latent correlation and normalised scores, not a plug-in result for measured rank IC.'
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=20) for q_, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk checks. The fixed latent-correlation toy gives about one point five eight annually under independent months. <bookmark mark='a'/> A bias statistic of one point three describes dispersion above the forecast scale; the narrow Gaussian reference needs its own assumptions. <bookmark mark='b'/> A volatility forecast is not a maximum loss, even for a model-factor-neutral book."
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
            "At fixed gross return and square-root cost technology, four times the size doubles costs per dollar. <bookmark mark='a'/> Quadrupling quadratic costs roughly halves trading speed only in the negligible-discount regime. <bookmark mark='b'/> A variance floor changes the risk input and an independent cap bounds holdings; neither establishes profitability. Complete solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS[:6], font_size=22, title=r"Problems 1--6")
        with self.voiceover("Six core calculations: the fixed toy's information ratio, the Gaussian bias reference, a known-prior beta update, fixed-input cost scaling, profit-maximising size and the zero-discount trade-rate limit. Complete assumptions and worked solutions are in the bilingual notes."):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.25, run_time=3))
            self.wait(1)
        self.clear_scene()
        ps = problem_set(PROBLEMS[6:10], font_size=22, title=r"Problems 7--10 (numbers continue)")
        for i, row in enumerate(ps.rows, 7):
            row[0].become(MathTex(str(i), font_size=22, color=QC.IDEA).move_to(row[0]))
        with self.voiceover("Four extensions, problems seven through ten: population Pearson signal combination, RMS score changes versus turnover, sample return attribution and the latent toy's asymptote and variance crossover. Keep the definitions and independence conditions explicit."):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.25, run_time=3))
            self.wait(1)
        self.clear_scene()
        ps = problem_set(PROBLEMS[10:], font_size=22, title=r"Problems 11--12: qualifying derivations")
        for i, row in enumerate(ps.rows, 11):
            row[0].become(MathTex(str(i), font_size=22, color=QC.IDEA).move_to(row[0]))
        with self.voiceover("Two qualifying derivations: prove the bounded-latent-correlation moment identity and exact continuous-crossover ratio, then derive the scalar Riccati policy using the stated Bellman timing. Distinguish the two cost asymptotic regimes. Both complete proofs are in the English and Chinese notes."):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.25, run_time=3))
            self.wait(1)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"trend, carry and risk parity across asset classes, traded with costs", [32]),
            (r"the firm: capacity, fees, and who keeps the alpha", [34]),
            (r"market impact derived; execution scheduled", [37]),
            (r"crowding, liquidity spirals and crises", [41]),
            (r"the finale: every row, deflated", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part thirty-two trades trend and carry across asset classes with this part's costs and risk model. Part thirty-four is the firm, where capacity and fees decide who keeps the alpha. Part thirty-seven derives the square-root law and schedules the trades. Part forty-one returns to crowding and liquidity spirals. And the finale deflates every row."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Grinold and Kahn, \textit{Active Portfolio Management} (2nd ed., 2000); Isichenko, "
             r"\textit{Quantitative Portfolio Management} (2021); Paleologo, \textit{The Elements of Quantitative "
             r"Investing}; Narang, \textit{Inside the Black Box}; Boyd et al., \textit{Multi-Period Trading via "
             r"Convex Optimization} (2017)"],
            [r"Blume (1971, 1975); Vasicek (1973); Rosenberg (1974); Chen, Roll and Ross (1986); Connor and Korajczyk "
             r"(1986); Brinson, Hood and Beebower (1986); Perold (1988); Grinold (1989); Connor (1995); Torre (1997); "
             r"Almgren and Chriss (2000); Clarke, de Silva and Thorley (2002); Berk and Green (2004); Buckle (2004); Qian "
             r"and Hua (2004); Almgren, Thum, Hauptmann and Li (2005)",
             r"Khandani and Lo (2007, 2011); Ding (2010); T\'oth et al.\ (2011); Garleanu and Pedersen (2013); Lou and "
             r"Polk (comomentum); Berk and van Binsbergen (2015); Novy-Marx and Velikov (2016); Ding and Martin (2017); "
             r"Frazzini, Israel and Moskowitz (2018). Data: Binance's public market data; Kenneth French's data library"])
        with self.voiceover(
            'These are the textbooks and papers behind the methods. Saved public research examples, quoted empirical studies, mathematical simulations and chosen fixed arithmetic have different scopes. The notes identify their assumptions and limitations; no sealed strategy result is loaded in this review.'
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("portfolio",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 32, Systematic Macro and Alternative Premia", font_size=30, color=QC.IDEA
                    ).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The portfolio and risk desk now connects forecast inputs, covariance assumptions, execution scenarios, dynamic decisions and independent position bounds. <bookmark mark='a'/> Next, Part thirty-two: systematic macro and alternative premia. We will distinguish historical method demonstrations from evidence about a future trading process."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
