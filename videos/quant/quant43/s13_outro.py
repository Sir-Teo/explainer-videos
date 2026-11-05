from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C, load)

DESK = [
    (r"Your fund beat the market five years running, among two thousand funds. Skill or luck?",
     r"by itself, nothing: zero-skill funds produce such records by chance; count how many beat it, against what luck "
     r"would give (Barras--Scaillet--Wermers), and ask whether the record was registered first"),
    (r"Why must the average active dollar trail the average passive dollar?",
     r"Sharpe's arithmetic: before costs both earn the market; after costs active trails by its extra cost; Pedersen: "
     r"unless passive investors must trade"),
    (r"A manager is truly skilled. Who benefits?",
     r"the manager, through size and fees: flows chase skill until investors' net alpha is zero (Berk--Green)"),
    (r"A strategy worked for fifty years. What do you check?",
     r"whether the market that paid it still exists: autocorrelation fell from 0.29 to $-0.04$; published anomalies "
     r"lose about half their returns"),
    (r"Your strategy's research Sharpe was 2. What do you expect out of sample?",
     r"less: the House's 25 rows kept about half of their research Sharpe above the average, with a standard error near "
     r"0.45 in five years"),
    (r"Why is Storey's estimate of the null share conservative?",
     r"its expectation is the null share plus the alternatives' chance of a large $p$-value, by linearity alone"),
]

PROBLEMS = [
    r"Passive holds 40\% of the market and earns 8\%; the market earns 8\%. Show active earns 8\% before costs.",
    r"Zero skill, cost 0.75\%, tracking error 4\%: the probability of beating the index over 10 years.",
    r"2,000 funds with no skill: the expected number with $t > 1.96$, and with $t > 3$.",
    r"$m = 1{,}000$ tests, 300 $p$-values above 0.5: Storey's $\hat\pi_0(0.5)$.",
    r"With $\hat\pi_0 = 0.8$, $\gamma = 0.2$, and 9\% of funds significant with positive $t$: the skilled share.",
    r"Berk--Green with $a = 4\%$, $b = 0.1\%$ per unit, fee 1\%: the equilibrium size and investors' net alpha.",
    r"Daily autocorrelation 0.2: the variance ratio over 2 days, and over 5 if all higher autocorrelations are zero.",
    r"A five-year hold-out of a strategy with true Sharpe 0.5: the standard error of its estimated Sharpe ratio.",
    r"Research Sharpe 1.5, cross-sectional slope 0.55, intercept 0.2: the predicted hold-out Sharpe.",
    r"Bachelier with $S = 100$, $K = 100$, $\sigma_N\sqrt T = 10$: the at-the-money call price.",
    r"(qual) Prove $\mathbb E\,\hat\pi_0(\lambda) \ge \pi_0$ without independence, derive its variance under "
    r"independence, and show that equicorrelation leaves the mean unchanged.",
    r"(qual) Prove Sharpe's arithmetic, then construct an example in which index reconstitution lets active investors, "
    r"in aggregate, beat passive ones (Pedersen 2018).",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("arith"), load("luck"), load("scale"), load("adaptive"), load("record"), load("ensemble"),
                   load("surface"), load("research"))
        self.series()
        self.lessons()
        self.formulas()
        self.desk()
        self.answers(load("research"))
        self.problems()
        self.references()
        self.reproduce()
        self.sources()
        self.finale()

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

    def recap(self, a, lk, sc, ad, r, e, su, rs):
        h = e["row"]["holdout"]
        d = ad["by_decade"]
        items = [
            (r"before costs active money earns the market's return, exactly; after costs, less", MKT_C),
            (rf"luck: a zero-skill manager beats the index over 15 years {100 * a['theory'][4]:.0f}\% of the time", LUCK_C),
            (rf"among 2,000 skill-less funds the best $t$ is {lk['best_null']:.1f}", LUCK_C),
            (r"skill can be counted without being found: Barras, Scaillet and Wermers", SKILL_C),
            (rf"skill goes to size and fees: investors' net alpha {100 * sc['aw_net_mean']:+.1f}\%", ACT_C),
            (rf"markets adapt: autocorrelation {d['1970']['ac1']:+.2f} in the 1970s, {d['2010']['ac1']:+.2f} in the 2010s", MKT_C),
        ]
        items2 = [
            (rf"the Track Record: research Sharpe shrinks with slope {r['slope']:.2f} out of sample", REC_C),
            (rf"{100 * r['share_positive']:.0f}\% of rows positive, {100 * r['share_sig']:.0f}\% significant alone", REC_C),
            (rf"the House's ensemble: hold-out Sharpe {h['sharpe']:.2f}, {h['sharpe_net']:.2f} net", SKILL_C),
            (rf"the Surface: rough Bergomi and SSVI fit best, Black--Scholes worst ({su['rows'][0]['rmse']:.1f} vol points)", HURDLE),
            (r"eight open problems, and the method that leaves them open honestly", QC.IDEA),
            (r"back to Bachelier: a negative oil price, and the fair game", MKT_C),
            (r"Rule 43: the market is the default; the record must argue otherwise", QC.HOUSE),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 43 in thirteen lines")
        with self.voiceover(
            "Part forty-three in thirteen lines. Before costs, active money earns exactly the market; after costs, less. "
            "Luck is generous, and with enough funds someone always looks brilliant. Skill can be counted without being "
            "found. Where it exists, it goes into size and fees. And markets adapt: the patterns of the seventies are "
            "gone."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 7)), r"Part 43 in thirteen lines")
        with self.voiceover(
            "The House's record kept about half of its research Sharpe, out of sample. Most rows were positive; few were "
            "significant alone. Its own mix of published premia held up. The pricing scoreboard rewarded the right shape "
            "over more parameters. The open problems remain open, honestly. Bachelier's model priced a negative oil "
            "price. And the last rule: the market is the default."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def series(self):
        smap = series_map(current=None, done=PART)
        with self.voiceover(
            "And the series, in one picture. Seven acts and forty-three parts: foundations, from the fair game to "
            "stochastic calculus; derivatives, from no arbitrage to deep hedging; fixed income and credit; asset "
            "pricing and factors; the quant's craft, from backtests to portfolios; the market's machinery, from the "
            "order book to execution, market making and crypto; and the system, from risk to crises, machines, and "
            "this question."
        ):
            self.play(FadeIn(smap))
            self.wait(3)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"the market is a fair game, mostly", r"prices are hard to predict, and what is predictable "
                          r"is usually a premium for risk, not a free lunch", width=12.4, font_size=19),
            desk_question(r"honesty is a method", r"point-in-time data, a sealed hold-out, every trial counted: without "
                          r"them, every backtest is an advertisement", width=12.4, font_size=19),
            desk_question(r"the system is more than its parts", r"leverage, liquidity and shared models make many "
                          r"sensible decisions into one fragile market", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons from all forty-three parts. <bookmark mark='a'/> The market is a fair game, mostly: what can "
            "be predicted is usually a premium for risk, not a free lunch. <bookmark mark='b'/> Honesty is a method: "
            "point-in-time data, a sealed hold-out and every trial counted, without which every backtest is an "
            "advertisement. <bookmark mark='c'/> And the system is more than its parts: leverage, liquidity and shared "
            "models can turn many sensible decisions into one fragile market."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def formulas(self):
        rows = VGroup(
            MathTex(r"w_P r_P + w_A r_A = r_M,\ \ r_P = r_M \Rightarrow r_A = r_M", font_size=32, color=MKT_C),
            MathTex(r"P(\text{beat}) = \Phi\!\left(-c\sqrt T/\sigma_{TE}\right)", font_size=32, color=LUCK_C),
            MathTex(r"\mathbb E\,\hat\pi_0(\lambda) = \pi_0 + (1 - \pi_0)\,\bar P_1(\lambda)/(1 - \lambda)", font_size=32,
                    color=HURDLE),
            MathTex(r"A^* = (\mathbb E[a] - f)/b,\qquad \mathbb E[\alpha_{\text{net}}] = 0", font_size=32, color=ACT_C),
            MathTex(r"C_{\text{Bachelier}} = (S - K)\Phi(d) + \sigma_N\sqrt T\,\varphi(d)", font_size=32, color=MKT_C),
        ).arrange(DOWN, buff=0.4)
        head = label(r"The part on one card", font_size=34).to_edge(UP, buff=0.4)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "The part on one card. Sharpe's arithmetic. The probability that luck beats the index. Storey's estimator. "
            "Berk and Green's equilibrium. And Bachelier's call, where it all began."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.4, run_time=5))
            self.wait(2)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=20) for q_, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six last desk questions. The hook's: skill or luck? By itself, a record says little; count how many beat "
            "the market against what luck would give. <bookmark mark='a'/> Why must active trail passive? The "
            "arithmetic. <bookmark mark='b'/> Who benefits from skill? The manager, through size."
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
            "A strategy worked for fifty years? Check that its market still exists. <bookmark mark='a'/> A research "
            "Sharpe of two? Expect about half the excess out of sample. <bookmark mark='b'/> And why is Storey's "
            "estimate conservative? Linearity. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def answers(self, r):
        d = r["dep"]
        cards = VGroup(
            desk_question(r"Research: neither, on average", r"the expectation of a count is a sum of probabilities, "
                          r"whatever the dependence; the theorem's proof never used independence", width=12.4, font_size=20),
            desk_question(r"but far less reliable", rf"equicorrelation of 0.6 left the mean at {d[-1]['mean']:.2f} and "
                          rf"raised the spread from {d[0]['sd']:.3f} to {d[-1]['sd']:.3f}", width=12.4, font_size=20),
        ).arrange(DOWN, buff=0.25)
        m6, s0, s6 = d[-1]["mean"], d[0]["sd"], d[-1]["sd"]
        with self.voiceover(
            "The research chapter's pause, answered. <bookmark mark='a'/> Neither, on average: the expectation of a count "
            "is a sum of probabilities, whatever the dependence, and the proof never used independence. "
            f"<bookmark mark='b'/> But far less reliable: with correlation nought point six the mean stayed at {m6:.2f} "
            f"while the spread rose from {s0:.3f} to {s6:.3f}."
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
            "And twelve problems: the arithmetic; luck over ten years; how many funds look significant by chance; "
            "Storey's estimate; the skilled share; Berk and Green's fund size; variance ratios; a hold-out's standard "
            "error; predicting out of sample; and Bachelier's at-the-money call. Then two qualifying-exam problems: "
            "Storey's estimator in full, and Sharpe's arithmetic with Pedersen's exception. Solutions, in English and "
            "Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Pedersen, \textit{Efficiently Inefficient} (2015); Lo, \textit{Adaptive Markets} (2017); Bodie, Kane and "
             r"Marcus, \textit{Investments}, ch.~11 and 24; Ilmanen, \textit{Expected Returns} (2011)"],
            [r"Bachelier (1900); Grossman and Stiglitz (1980); Lo and MacKinlay (1988, 1990); Sharpe (1991); Carhart "
             r"(1997); Storey (2002); Berk and Green (2004); Lo (2004); Kosowski, Timmermann, Wermers and White (2006)",
             r"Barras, Scaillet and Wermers (2010); Fama and French (2010); Berk and van Binsbergen (2015); McLean and "
             r"Pontiff (2016); Harvey, Liu and Zhu (2016); Pedersen (2018). Data: Kenneth French's library; the "
             r"House's Track Record and envelope; CME's notices of April 2020"])
        with self.voiceover(
            "The books this part follows, and the papers it draws on, from Bachelier to Pedersen. Every number on "
            "screen came from Kenneth French's returns, the House's own Track Record and envelope, the Surface's cached "
            "fits, or simulation with fixed seeds."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def reproduce(self):
        cards = VGroup(
            desk_question(r"everything is rebuildable", r"each part's compute.py regenerates every number from public "
                          r"data and fixed seeds; the House's library is tested; the data manifest is checksummed",
                          width=12.4, font_size=19),
            desk_question(r"the record is public", r"the envelope's registry and the Track Record are committed files: "
                          r"anyone can check that no row was opened twice", width=12.4, font_size=19),
            desk_question(r"where to go next", r"the textbooks on each part's reference card; and the open problems of "
                          r"Chapter 7, each a thesis", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And how to check all of it. <bookmark mark='a'/> Each part's compute script regenerates every number from "
            "public data and fixed seeds, and the House's library is tested. <bookmark mark='b'/> The envelope's "
            "registry and the Track Record are committed files, so anyone can check that no row was opened twice. "
            "<bookmark mark='c'/> And where to go next: the textbooks on each reference card, and the open problems "
            "of Chapter seven, each one a thesis."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def sources(self):
        cards = VGroup(
            desk_question(r"built on public data", r"Kenneth French's library, FRED, AQR's data sets, the Open Source "
                          r"Asset Pricing library, SEC EDGAR, the Treasury, Binance's and Deribit's public archives, "
                          r"Yahoo Finance", width=12.4, font_size=19),
            desk_question(r"and on papers", r"every result cited to its authors, every firm from the public record, "
                          r"every allegation labelled as reported", width=12.4, font_size=19),
            desk_question(r"and on two other series", r"the instruments of AI, Built, and the habits of a lecture that "
                          r"proves before it claims", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And what it was built on. <bookmark mark='a'/> Public data: Kenneth French's library, FRED, AQR's data "
            "sets, the Open Source Asset Pricing library, the SEC's filings, the Treasury, and the public archives of "
            "two crypto exchanges. <bookmark mark='b'/> Papers, each cited to its authors, with firms only as the "
            "public record describes them. <bookmark mark='c'/> And the habits of a lecture that proves before it "
            "claims."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def finale(self):
        chart = house_chart(PART, lit=tuple(DESKS.keys()))
        end = label(r"Quant, Built: forty-three parts. Thank you for building it with us.", font_size=28,
                    color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House began as an empty building, a sealed envelope and a counter at zero. It ends with every desk "
            "built, every trial counted, and an honest answer to the question it was built to ask: you can beat the "
            "market, a little, sometimes, by bearing risk or by real skill, and you will only know which by keeping "
            "score before you look. <bookmark mark='a'/> That is the end of Quant, Built. Thank you for building it "
            "with us."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeIn(end))
        self.wait(2.0)
        self.clear_scene()
