from __future__ import annotations

import math

from explainer.quant import *  # noqa: F403
from videos.quant.quant34.common import (BAD, FIRM_C, GOOD, LAW_C, PART, PLAT_C, PM_C, STOP_C, TECH_C, comma, load)

DESK = [
    (r"What does one losing day in 1{,}238 imply?",
     'Gaussian-implied daily ratio 3.15; about 50 annualized needs iid variance assumptions. Loss frequency alone does not identify the ratio; $s=r\\sqrt N$ needs independent equal-risk trades'),
    (r"How long does a Sharpe-1 manager keep a full book under a stop half a volatility deep?",
     r"$(e - 2)/2 \approx 0.36$ years on average; one volatility deep, $(e^2 - 3)/2 \approx 2.2$ years"),
    (r"Why do platforms stop managers who may be good?",
     'under a chosen model stops affect selection, exposure and payouts; a skill test requires a null, deadline and calibration. Identical-skill results do not show a cost here'),
    (r"What is netting risk?",
     'each pod is paid on positive profit while investors bear the sum; at positive aggregate profit the payout share can exceed the headline rate, while at zero it is undefined'),
    ("Which controls could have limited Knight Capital's runaway orders?",
     r"price, size and rate checks on every order, a credit limit on the algorithm, and a kill switch with someone "
     r"empowered to press it"),
    (r"Is a high cancel ratio evidence of spoofing?",
     r"no: market makers cancel most quotes; the evidence is intent, large orders cancelled on one side as the trader "
     r"executes on the other"),
]

PROBLEMS = ['(basic 1) 5 losses in 1{,}250 days: Gaussian-implied daily ratio and iid annualization; explain the identification limitation.', '(basic 2) Stipulate 15\\% gross: investor return under 2\\% then 20\\%, versus 6\\% costs then 20\\%, with positive eligible profit.', '(basic 3) Two pods have capital 100 each and P\\&L $+10,-10$; bonus 20\\% of positive profit. Find bonus, investor return and bonus/gross.', '(basic 4) Chosen prior $S\\sim N(0,0.5^2)$ and likelihood $\\hat S_T\\mid S\\sim N(S,1/T)$: posterior when $\\hat S_T=2$, $T=1,4$.', '(basic 5) Fixed position and participation; ADV halves, volatility doubles. Compare exit days and stipulated daily clip cost $Y\\sigma\\sqrt q$.', '(basic 6) Fair die, one optional reroll, must keep the second: derive the optimal rule and expected payoff.', '(advanced 7) For two independent fair $K$-sided dice, derive the maximum distribution and mean; evaluate at $K=6$ and check the bounds.', '(advanced 8) Fair St. Petersburg game capped at $2^{20}$: sum the complete tail and generalize to a cap $2^m$; distinguish expectation from ticket utility.', '(advanced 9) Known iid even-money win chance 55\\%: derive Kelly, log growth, twice-Kelly growth and the asymptotic wealth conclusion.', '(advanced 10) Predictable exposure $Z$, independent of current iid return, on probability $p=0.75$: derive the exact marginal ratio and low-mean annual approximation for $S=0.6$.', '(qual 11) Prove finite mean continuous Brownian drawdown time using a bounded reflected-ODE solution, derive its formula and zero-drift limit.', '(qual 12) Prove the exponential peak law using a moving-boundary sandwich and strong Markov; derive level-hit probabilities, mean terminal profit and justify Wald.']


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("virtu"), load("theory"), load("power"), load("platform"), load("stops"))
        self.desk()
        self.answers()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=26, color=col), wrapped_label(t, 11.8, 26)).arrange(RIGHT, buff=0.3, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, v, t, pw, p, s):
        S1 = t["grid"][t["S"].index(1.0)]
        on, off = p["5% vol, halve 5%, cut 7.5% | skill sd 0.5"], p["5% vol, no stops | skill sd 0.5"]
        items = [
            (r"six models: prop trading, market making, platforms, systematic funds, banks, China's quant funds", FIRM_C),
            (rf"1 loss in 1{{,}}238: Gaussian-implied daily ratio {v['normal']:.2f}; independence is an assumption", GOOD),
            ('attributed historical firm figures; illustrative fee arithmetic does not reconcile aggregate historical returns', FIRM_C),
            (rf"the chosen pod model: investor ratio {off['investor_sharpe']:.2f} $\to$ "
             rf"{on['investor_sharpe']:.2f} when skill varies", PLAT_C),
            (rf"netting risk: {100 * on['payout_share']:.0f}\% of gross P\&L paid to pods", PLAT_C),
            (r"from idea to capital: information clock, cash ledger, review and a chosen prior", FIRM_C),
            (r"risk at the firm: limits, liquidity, stress, Knight's 45 minutes, Archegos", STOP_C),
        ]
        items2 = [
            (r"technology: OCaml, C++ and FPGAs; light takes about 4 ms from Aurora to Carteret", TECH_C),
            (r"surveillance: spoofing and layering; Sarao; J.P. Morgan's \$920m; the CAT", LAW_C),
            (r"the interview: probability, a market game with an informed trader, Kelly, code", PM_C),
            (r"founding stories, as told in public, and their survivorship", FIRM_C),
            ('factor-stop research: dependent reused-sample comparisons, descriptive shuffles, before costs', STOP_C),
            ('proposed Rule 34: limits, authority, records and conditional evaluation; no deployment approval', QC.HOUSE),
            (rf"research: $\mathbb E[\tau] = (e^{{2S\delta}} - 1 - 2S\delta)/(2S^2)$; {S1[0]:.2f} years at $S = 1$, "
             r"$\delta = 0.5$", STOP_C),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 34 in fourteen lines")
        self.add(head, rows[0])
        with self.voiceover(
            'Part thirty-four in fourteen lines. Six illustrative business models distinguish capital, customers and the claimed source of revenue. A loss-day count implies a mean-to-volatility ratio only under a specified distribution; it does not identify real trading skill. Reported firm statistics need consistent fees and denominators. The chosen platform simulation includes selection, exposure and payout rules, and is not calibrated evidence about a real firm. Review requires a search record, information clock, executable cash ledger and uncertainty. Independent limits and authority to halt are proposed controls, not a guaranteed operating system.'
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 34 in fourteen lines")
        self.add(head, rows[0])
        with self.voiceover(
            'Technology faces physical latency floors as well as routing and operational constraints. Surveillance requires context and evidence; high cancellation alone is not proof of manipulation. Interview calculations state their probability and capital assumptions. Founding stories are selected histories. The factor-stop exercise uses dependent research comparisons and a descriptive shuffle reference, without costs. The proposed firm checklist does not approve deployment. Finally, the Brownian drawdown theorem is exact for known constant parameters and continuous arithmetic profit; the exponential law concerns the peak, while grid stop times need separate monitoring and censoring qualifications.'
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=26) for q_, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        self.add(cards[0])
        with self.voiceover(
            "Six desk questions, with assumptions stated. A loss-day count maps to an implied ratio under a specified distribution; it cannot identify skill by itself. <bookmark mark='a'/> A known Brownian Sharpe-one process reaches a half-volatility continuous drawdown in about four point three months on average. <bookmark mark='b'/> A platform may use stops for risk and learning, but its simulation also changes exposure, replacement and compensation. It is not a calibrated universal skill test."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
        cards = page(DESK[3:])
        self.add(cards[0])
        with self.voiceover(
            "Netting risk means paying positive pods while investors also bear the losers. <bookmark mark='a'/> Pre-trade limits and a tested halt mechanism are controls intended to constrain malfunction; their effectiveness is not a guaranteed counterfactual. <bookmark mark='b'/> A high cancellation rate alone does not establish spoofing. Placement, cancellation, opposite-side fills, context and communications may support investigation, with legal conclusions requiring more evidence."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def answers(self):
        from scipy import stats
        fund = (0.10 - 0.02) * 0.8
        plat = (0.10 - 0.06) * 0.8
        s5 = float(-stats.norm.ppf(5 / 1250))
        a5 = s5 * math.sqrt(252)
        reroll = 0.5 * 5 + 0.5 * 3.5
        surv = 1000 / 2 ** 10
        stop_s = 0.6 * math.sqrt(0.75)
        a = 2 * 1.5 * 1.5
        et = (math.exp(a) - 1 - a) / (2 * 1.5 ** 2)
        pages = [
            [(r"Ch.~1: 2 and 20 against pass-through", rf"at 10\% gross, {100 * fund:.1f}\% against {100 * plat:.1f}\%: "
              r"the classic fund, unless the platform earns more gross"),
             (r"Ch.~2: 5 losing days in 1{,}250", rf"a daily ratio of {s5:.2f}, about {a5:.0f} a year"),
             (r"Ch.~3: two no-skill pods at $\pm 10\%$", 'equal capital 100 each, P\\&L $+10,-10$: bonus 2, investor loss 2, return $-1\\%$ on 200; bonus/gross is undefined')],
            [(r"Ch.~4: a live Sharpe of 2", r"posterior 0.4 after one year, 1.0 after four"),
             (r"Ch.~5: volume halves, volatility doubles", 'fixed participation and position: twice the days and twice the stipulated daily clip cost; full liquidation requires a model'),
             (r"Ch.~6: 3 ms and a 0.5 bp edge", 'chosen first-arrival contest: value per captured dollar is 0.5 bp before costs; total value needs captured notional and competition')],
            [(r"Ch.~7: cancelling 98\% of quotes", r"normal for a market maker; the evidence would be large orders "
              r"cancelled opposite its own fills"),
             (r"Ch.~8 and Ch.~9: the re-roll; a thousand firms", rf"re-roll below 4: {reroll:.2f}; about {surv:.0f} firm "
              r"is the expected count; no guaranteed survivor or proof of skill"),
             (r"Ch.~10 and research", rf"$0.6\sqrt{{0.75}} = {stop_s:.2f}$; at $S = 1.5$, $\delta = 1.5$: {et:.1f} "
              r"years, and $\mu\,\mathbb E[\tau]$ of profit")],
        ]

        def show(page):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=26) for q_, a_ in page]).arrange(DOWN, buff=0.22)
            if cards.height > 7.2:
                cards.scale_to_fit_height(7.2)
            return cards

        cards = show(pages[0])
        self.add(cards[0])
        with self.voiceover(
            f"""The chapter pause answers use their stated inputs. At ten percent gross, the simple fee formulas leave {100*fund:.1f} and {100*plat:.1f} percent; the separate problem-set question uses fifteen percent gross. <bookmark mark='a'/> Five losses in twelve hundred and fifty maps to Gaussian daily ratio {s5:.2f}; annualization to about {a5:.0f} also needs iid variance assumptions. <bookmark mark='b'/> For two pods with capital one hundred each, profits plus ten and minus ten cancel. A twenty-percent positive-profit bonus is two currency units. Investors lose two, or one percent of two hundred. Bonus divided by zero gross profit is undefined."""
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        cards = show(pages[1])
        self.add(cards[0])
        with self.voiceover(
            "In the chosen Gaussian likelihood with prior standard deviation one half and observed Sharpe two, posterior means are point four after one year and one after four. <bookmark mark='a'/> At fixed position and participation, halved daily volume doubles exit days; doubled volatility doubles the stipulated daily clip cost. Holding child size fixed would give a different answer. <bookmark mark='b'/> A three-millisecond advantage captures the edge only under a chosen first-arrival competition model. Half a basis point times captured notional gives gross value; costs, opponents, reliability and fill probability are still needed."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        cards = show(pages[2])
        self.add(cards[0])
        with self.voiceover(
            f"""Cancellation alone does not establish intent; investigate the complete context. <bookmark mark='a'/> With fair dice, reroll one, two or three and retain four, five or six: expectation {reroll:.2f}. Independent annual survival at one half gives expected survivors {surv:.4f}, without guaranteeing one or demonstrating skill. <bookmark mark='b'/> The low-mean iid exposure approximation gives {stop_s:.2f}; the exact marginal formula includes the extra variance term. Under known continuous Brownian assumptions, S one point five and delta one point five give about {et:.2f} years; expected arithmetic profit is mu times that mean time."""
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS[:6], font_size=20, title=r"Six basic problems")
        self.add(ps.head, ps.rows[0])
        with self.voiceover("Six basic problems state their inputs: the Gaussian loss-frequency calculation, one-period fees, two-pod capital accounting, the chosen Normal posterior, liquidity at fixed participation and a fair-die reroll. Derive each result and state its limits. Full solutions in English and Chinese are in the notes."):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
        self.clear_scene()
        ps = problem_set(PROBLEMS[6:10], font_size=22, title=r"Four advanced problems")
        self.add(ps.head, ps.rows[0])
        with self.voiceover("Four advanced problems extend the calculation: the maximum of two K-sided dice, the complete tail of a capped St. Petersburg game, Kelly and asymptotic log growth, and the exact marginal ratio under predictable iid exposure. Specify the probability model before interpreting the answer."):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
        self.clear_scene()
        ps = problem_set(PROBLEMS[10:], font_size=24, title=r"Two qualifying problems")
        self.add(ps.head, ps.rows[0])
        with self.voiceover("Two qualifying problems prove the finite-mean reflected drawdown formula and the exponential peak law. The first must justify finiteness before identifying the candidate solution. The second must handle the moving boundary and justify Wald's identity. State continuity, known parameters, positive volatility and positive barrier throughout."):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=3))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"who trades with whom: the market's participants and venues", [35]),
            (r"execution: what a trade really costs", [37]),
            (r"market making: the theory behind the dice game", [38]),
            (r"regulation and crises: the firm's other history", [41]),
        ])
        self.add(card.head, card.rows[0])
        with self.voiceover(
            "Where this comes back. Part thirty-five maps who trades with whom. Part thirty-seven measures what a trade "
            "costs. Part thirty-eight is market making, the theory behind the dice game. And Part forty-one returns to "
            "regulation and crises."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [
                r"Narang, \textit{Inside the Black Box} (2013)",
                r"Isichenko, \textit{Quantitative Portfolio Management} (2021)",
                r"Paleologo, \textit{Advanced Portfolio Management} (2021)",
                r"Zuckerman, \textit{The Man Who Solved the Market} (2019)",
                r"Patterson, \textit{The Quants} (2010)",
                r"Derman, \textit{My Life as a Quant} (2004)",
                r"Thorp, \textit{A Man for All Markets} (2017)",
            ],
            [r"Taylor (1975); Lehoczky (1977); Grossman and Zhou (1993); Magdon-Ismail et al.\ (2004); Budish, Cramton and "
             r"Shim (2015); Minsky (2011)",
             r"Public record: Virtu's S-1 (2014); the SEC's order on Knight Capital (2013); the CFTC and DOJ on J.P. Morgan "
             r"(2020); US v. Sarao; SEBI's interim order (2025); press reports as cited. Data: Kenneth French"])
        self.add(card)
        with self.voiceover(
            'References distinguish mathematical sources, dated filings and legal records, books and attributed press reports. The numerical panels use the five unchanged verified ordinary calculations or explicit stipulated arithmetic. Historical quotations retain their source and date; this review does not independently verify current firm statistics or subsequent legal outcomes. No sealed strategy outcome is used.'
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("compliance",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 35, Who Trades With Whom", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        self.add(chart)
        with self.voiceover(
            "The House now has a proposed firm-level checklist: independent limits, authority to halt, explicit accounting and records of the search. A chart and numerical functions do not create an operating trading or compliance system. <bookmark mark='a'/> Next is market microstructure. Part thirty-five studies who trades with whom, through which venues, and which order and information assumptions determine costs."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
