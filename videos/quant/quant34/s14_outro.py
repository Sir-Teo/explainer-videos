from __future__ import annotations

import math

from explainer.quant import *  # noqa: F403
from videos.quant.quant34.common import (BAD, FIRM_C, GOOD, LAW_C, PART, PLAT_C, PM_C, STOP_C, TECH_C, comma, load)

DESK = [
    (r"What does one losing day in 1{,}238 imply?",
     r"under a normal model a daily Sharpe ratio of 3.15, about 50 a year; it comes from very many small trades, since "
     r"$s = r\sqrt N$ for $N$ independent trades of ratio $r$"),
    (r"How long does a Sharpe-1 manager keep a full book under a stop half a volatility deep?",
     r"$(e - 2)/2 \approx 0.36$ years on average; one volatility deep, $(e^2 - 3)/2 \approx 2.2$ years"),
    (r"Why do platforms stop managers who may be good?",
     r"skill is unknown, and a stop is a sequential test: it fires the unskilled faster; it pays when skill varies, and "
     r"costs a little when it does not"),
    (r"What is netting risk?",
     r"each pod is paid on its own profit while investors own the sum, losers included; the share paid out exceeds the "
     r"headline rate"),
    (r"What would have stopped Knight Capital's 45 minutes?",
     r"price, size and rate checks on every order, a credit limit on the algorithm, and a kill switch with someone "
     r"empowered to press it"),
    (r"Is a high cancel ratio evidence of spoofing?",
     r"no: market makers cancel most quotes; the evidence is intent, large orders cancelled on one side as the trader "
     r"executes on the other"),
]

PROBLEMS = [
    r"5 losing days in 1{,}250: the daily and annual Sharpe ratios under a normal model.",
    r"15\% gross: investors' return under 2\% and 20\%, and under 6\% pass-through costs and 20\%.",
    r"Two pods with no skill make $+10\%$ and $-10\%$; each is paid 20\% of a positive year. The share paid out.",
    r"A live Sharpe ratio of 2 with a prior $N(0, 0.5^2)$: the posterior mean after one and after four years.",
    r"Volume halves and volatility doubles: the change in days to exit and in the square-root cost.",
    r"A die you may re-roll once: the best strategy and its expected value.",
    r"The expected value of the larger of two dice.",
    r"The St. Petersburg game with payouts capped at $2^{20}$: the fair price.",
    r"A coin winning 55\% of even bets: the Kelly fraction, its growth rate, and the growth rate at twice it.",
    r"An i.i.d. strategy with Sharpe 0.6, stopped out a quarter of the time: its Sharpe ratio counting the flat months.",
    r"(qual) Prove $\mathbb E[\tau_d] = \frac{\sigma^2}{2\mu^2}(e^a - 1 - a)$, $a = 2\mu d/\sigma^2$, from the "
    r"reflected drawdown's Dynkin equation, and show it tends to $d^2/\sigma^2$ as $\mu \to 0$.",
    r"(qual) Show $M_{\tau}$ is exponential with rate $\lambda = (2\mu/\sigma^2)/(e^a - 1)$; deduce the chance the "
    r"manager earns $x$ before the stop, and check $\mathbb E[M_\tau] - d = \mu\,\mathbb E[\tau]$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("virtu"), load("theory"), load("power"), load("platform"), load("house"), load("stops"))
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

    def recap(self, v, t, pw, p, h, s):
        S1 = t["grid"][t["S"].index(1.0)]
        on, off = p["5% vol, halve 5%, cut 7.5% | skill sd 0.5"], p["5% vol, no stops | skill sd 0.5"]
        items = [
            (r"six models: prop trading, market making, platforms, systematic funds, banks, China's quant funds", FIRM_C),
            (rf"one losing day in 1{{,}}238: a daily Sharpe ratio of {v['normal']:.2f}, from many small trades", GOOD),
            (r"Jane Street's and Medallion's numbers, as reported; fees checked against each other", FIRM_C),
            (rf"the pod model: stops raise investors' Sharpe {off['investor_sharpe']:.2f} $\to$ "
             rf"{on['investor_sharpe']:.2f} when skill varies", PLAT_C),
            (rf"netting risk: {100 * on['payout_share']:.0f}\% of gross P\&L paid to pods", PLAT_C),
            (rf"from idea to capital: the House's record shrinks with slope {h['slope']:.2f}", FIRM_C),
            (r"risk at the firm: limits, liquidity, stress, Knight's 45 minutes, Archegos", STOP_C),
        ]
        items2 = [
            (r"technology: OCaml, C++ and FPGAs; light takes about 4 ms from Aurora to Carteret", TECH_C),
            (r"surveillance: spoofing and layering; Sarao; J.P. Morgan's \$920m; the CAT", LAW_C),
            (r"the interview: probability, a market game with an informed trader, Kelly, code", PM_C),
            (r"founding stories, as told in public, and their survivorship", FIRM_C),
            (r"stops on real premia: they beat their shuffle where losses persist, not for momentum", STOP_C),
            (r"Rule 34: limits, controls, surveillance and a posterior-sized ramp", QC.HOUSE),
            (rf"research: $\mathbb E[\tau] = (e^{{2S\delta}} - 1 - 2S\delta)/(2S^2)$; {S1[0]:.2f} years at $S = 1$, "
             r"$\delta = 0.5$", STOP_C),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 34 in fourteen lines")
        with self.voiceover(
            "Part thirty-four in fourteen lines. Six business models, distinguished by whose capital they trade and what "
            "edge they sell. A disclosed loss rate implies a daily Sharpe ratio above three, built from very many small "
            "trades. The famous numbers, read as reported and checked against each other. On a platform, stops raise "
            "what investors keep when skill varies, while pods are paid more than the headline share. The House's own "
            "record shrank by about a quarter from research to new data. And firm-level risk, from limits to kill "
            "switches."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 34 in fourteen lines")
        with self.voiceover(
            "Technology, against the speed of light. Surveillance, and the cases that defined spoofing. The interview, "
            "and what it really tests. The founding stories, and the survivors who tell them. Stops on real premia, "
            "which help where losses persist and not for momentum. The thirty-fourth rule. And the theorem: a seat's "
            "expected life grows exponentially in Sharpe ratio times the stop's depth."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
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
            "Six desk questions. What does one losing day in twelve hundred and thirty-eight imply? A daily Sharpe ratio "
            "above three, from many small trades. <bookmark mark='a'/> How long does a Sharpe-one manager last under a "
            "stop half a volatility deep? About four months. <bookmark mark='b'/> Why stop managers who may be good? "
            "Because skill is unknown, and the stop is a test."
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
            "What is netting risk? Paying winners while investors own the losers too. <bookmark mark='a'/> What would "
            "have stopped Knight Capital? Checks on every order and a kill switch. <bookmark mark='b'/> And is a high "
            "cancel ratio spoofing? No; intent is the evidence. Full solutions are in the notes."
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
             (r"Ch.~3: two no-skill pods at $\pm 10\%$", r"the platform earns nothing and pays 2\%: an infinite share")],
            [(r"Ch.~4: a live Sharpe of 2", r"posterior 0.4 after one year, 1.0 after four"),
             (r"Ch.~5: volume halves, volatility doubles", r"twice the days to exit, and twice the cost per unit sold"),
             (r"Ch.~6: 3 ms and a 0.5 bp edge", r"to the fastest firm, the edge times its trades; to the second fastest, "
              r"almost nothing: speed is winner-take-all")],
            [(r"Ch.~7: cancelling 98\% of quotes", r"normal for a market maker; the evidence would be large orders "
              r"cancelled opposite its own fills"),
             (r"Ch.~8 and Ch.~9: the re-roll; a thousand firms", rf"re-roll below 4: {reroll:.2f}; about {surv:.0f} firm "
              r"survives ten years, and credits its skill"),
             (r"Ch.~10 and research", rf"$0.6\sqrt{{0.75}} = {stop_s:.2f}$; at $S = 1.5$, $\delta = 1.5$: {et:.1f} "
              r"years, and $\mu\,\mathbb E[\tau]$ of profit")],
        ]

        def show(page):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=19) for q_, a_ in page]).arrange(DOWN, buff=0.22)
            if cards.height > 7.2:
                cards.scale_to_fit_height(7.2)
            return cards

        cards = show(pages[0])
        with self.voiceover(
            "The pause questions, answered. At ten percent gross, two and twenty leaves "
            f"{100 * fund:.1f} percent; the platform, {100 * plat:.1f}. <bookmark mark='a'/> Five losing days in twelve "
            f"hundred and fifty is a daily ratio of {s5:.2f}, about {a5:.0f} a year. <bookmark mark='b'/> And two pods "
            "without skill, one up and one down: the platform earns nothing and still pays two percent."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        cards = show(pages[1])
        with self.voiceover(
            "A live Sharpe ratio of two is believed as point four after a year, and one after four. "
            "<bookmark mark='a'/> When volume halves and volatility doubles, both the days to exit and the cost double. "
            "<bookmark mark='b'/> And speed is winner-take-all: the edge goes to the fastest firm, and almost none to "
            "the second."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        cards = show(pages[2])
        with self.voiceover(
            "Cancelling most quotes is normal for a market maker; intent is the evidence. <bookmark mark='a'/> Re-roll "
            f"anything below four, for {reroll:.2f}; and of a thousand firms without skill, about one survives ten years, "
            f"and credits its skill. <bookmark mark='b'/> The stopped strategy shows {stop_s:.2f}; and a Sharpe of one "
            f"and a half with a stop one and a half volatilities deep lasts about {et:.0f} years."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: a disclosed loss rate; two fee structures; netting; a posterior Sharpe ratio; "
            "liquidity in a crisis; three interview classics and Kelly; and a stopped strategy's Sharpe ratio. Then two "
            "qualifying-exam problems: the stop-time formula from the reflected drawdown, and the exponential law of the "
            "peak. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"who trades with whom: the market's participants and venues", [35]),
            (r"execution: what a trade really costs", [37]),
            (r"market making: the theory behind the dice game", [38]),
            (r"regulation and crises: the firm's other history", [41]),
        ])
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
            [r"Narang, \textit{Inside the Black Box} (2013); Isichenko, \textit{Quantitative Portfolio Management} (2021); "
             r"Paleologo, \textit{Advanced Portfolio Management} (2021); Zuckerman, \textit{The Man Who Solved the "
             r"Market} (2019); Patterson, \textit{The Quants} (2010); Derman, \textit{My Life as a Quant} (2004); Thorp, "
             r"\textit{A Man for All Markets} (2017)"],
            [r"Taylor (1975); Lehoczky (1977); Grossman and Zhou (1993); Magdon-Ismail et al.\ (2004); Budish, Cramton and "
             r"Shim (2015); Minsky (2011)",
             r"Public record: Virtu's S-1 (2014); the SEC's order on Knight Capital (2013); the CFTC and DOJ on J.P. Morgan "
             r"(2020); US v. Sarao; SEBI's interim order (2025); press reports as cited. Data: Kenneth French"])
        with self.voiceover(
            "The books this part follows, and its sources: the papers on drawdowns and markets, and the public record, "
            "filings, orders and court cases, with press reports labelled as reported. Every number on screen was "
            "computed by the House's code, or quoted from those sources."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("compliance",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 35, Who Trades With Whom", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House is now a firm: desks with limits, a compliance desk that watches them, a research process with "
            "its trials counted, and a rule for how long any book keeps its capital. <bookmark mark='a'/> Next, Act six "
            "begins: market microstructure. Part thirty-five: who trades with whom, through which venues, and why the "
            "same order can cost one trader nothing and another a great deal."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
