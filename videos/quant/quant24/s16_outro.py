from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAB, BAD, CMA, FCOL, GOOD, HML, MKT, PART, QMJ, RMW, SMB, TSM, UMD, load

DESK = [
    (r"Momentum and value are negatively correlated. Why hold both?",
     r"each has a positive premium, and with a correlation near $-0.6$ the 50/50 mix keeps the average and loses most of "
     r"the risk: a Sharpe ratio near 1.1 against 0.4 and 0.6 alone. It disappoints when both fall together, in a funding "
     r"squeeze, or when both premia decay at once"),
    (r"A model is rejected with $p = 0.001$, but its average pricing error is 0.3\% a year. Use it?",
     r"probably: every model is rejected on long samples. Check where the alphas are, whether they line up with a "
     r"characteristic the model leaves out, whether they survive costs and a hold-out, and what the rival models do"),
    (r"The size premium was 3.4\% a year before 1981 and 1.0\% after. Dead, never there, or hiding?",
     r"a $t$ of 0.6 cannot say. Publication decay, the January concentration, and the stronger premium once junk is "
     r"controlled for each point a different way; international data and other periods are the tie-breakers"),
    (r"The market fell 40\% in two years and just rose 10\%. Momentum's beta is about $-1$. What do you do?",
     r"cut or hedge it: scale by volatility, or add back market beta. If the bear market resumes you give up a strong "
     r"month for momentum; if the rebound continues you avoid the crash. Daniel and Moskowitz's evidence favours cutting"),
    (r"A pension fund that cannot borrow wants more return. High-beta stocks, or low-beta stocks plus futures?",
     r"low-beta stocks with equity futures for the extra exposure: futures embed the leverage it cannot take directly. "
     r"The anomaly says most constrained investors choose high-beta stocks, which is why they are overpriced"),
    (r"December 2020: the value spread is at its 96th percentile. What do you expect?",
     r"a tilt of the odds: the fitted line points to about 12\% for value in 2021, against a 4\% average, with an $R^2$ of "
     r"5\%. Lean in modestly; a single year is one draw, whatever it turns out to be"),
]

PROBLEMS = [
    r"Show that the GRS numerator $\hat\alpha^\top\hat\Sigma^{-1}\hat\alpha$ equals $SR^2(f, R) - SR^2(f)$, the gain in "
    r"the squared maximum Sharpe ratio from adding the test assets.",
    r"For one test asset ($N = 1$), show that the GRS statistic is the squared $t$-statistic of its alpha, up to a "
    r"degrees-of-freedom factor.",
    r"Six portfolios return SL 1.2\%, SM 1.0\%, SH 1.5\%, BL 0.6\%, BM 0.8\%, BH 1.1\% in a month. Compute SMB and HML.",
    r"With constant ROE, growth $g$ and discount rate $r$, show $M/B = (\text{ROE} - g)/(r - g)$. With ROE 12\%, $g$ = 5\%, "
    r"what $r$ gives B/M = 0.8?",
    r"Value and momentum: means 4\% and 5\%, volatilities 10\% each, correlation $-0.6$. Find the Sharpe ratio of the "
    r"50/50 mix.",
    r"After a bear market, winners have beta 0.8 and losers 1.8. The market rises 15\% in a month. What does that do "
    r"to UMD, before any stock-specific news?",
    r"Momentum's realised volatility is 40\% and the target 12\%. What weight does Barroso--Santa-Clara scaling hold, and "
    r"what is the scaled loss in a month of $-34\%$?",
    r"BAB: $\beta_L = 0.7$, $\beta_H = 1.5$, monthly excess returns 0.6\% and 0.8\%. Compute the BAB return and its beta.",
    r"How many years does a Sharpe ratio of 0.45 need to reach $t = 2$? What Sharpe ratio reaches $t = 2$ in a five-year "
    r"hold-out?",
    r"A green stock is priced to earn 5\%, a brown one 7\%. A climate-concern shock raises the green price 10\% and lowers "
    r"the brown 5\% in one year. Realised returns? Expected returns the next year?",    r"(qual) Derive Lo and MacKinlay's identity: for $w_i = (x_i - \bar x)/N$, the average of $\sum_i w_ir_i$ equals "
    r"own covariances times $(N - 1)/N^2$, minus cross covariances over $N^2$, plus the covariance of the means.",
    r"(qual) For $N$ assets with a common iid factor and independent AR(1) idiosyncratic parts, compute each term, and "
    r"show the factor contributes nothing to the profit.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("race"), load("tests"), load("crash"), load("everywhere"), load("valuedecade"), load("envelope"))
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

    def recap(self, r, t, c, e, v, env):
        items = [
            (rf"a dollar in 1963: market \${r['series']['MKT'][-1]:.0f}, momentum \${r['series']['UMD'][-1]:.0f}, the "
             r"others \$4--5", MKT),
            (rf"GRS and Fama--MacBeth: every model rejected; average $|\alpha|$ "
             rf"{100 * t['models']['CAPM']['mean_abs_alpha']:.1f}\% (CAPM) to {100 * t['models']['FF5']['mean_abs_alpha']:.1f}\% "
             r"(five factors)", BAD),
            (r"size and value: 2 x 3 sorts; size 3.4\% before 1981, 1.0\% after; value halved", SMB),
            (r"momentum: winners 15\%, losers 1\%; time-series momentum Sharpe 1.06; the smile", UMD),
            (rf"momentum crashes: 1932, 2009; beta $-1$ in rebounds; scaling lifts Sharpe to {c['scaled']['sharpe']:.2f}",
             BAD),
            (r"profitability and investment: the dividend discount model; HML redundant in five factors; q", RMW),
            (r"low risk: BAB 8.2\% a year since 1930; volatility-sorted Sharpe 0.57 to 0.16", BAB),
        ]
        items2 = [
            (rf"everywhere: value and momentum in eight markets, correlation {e['global']['corr']:.2f}, mix Sharpe "
             rf"{e['global']['combo']['sharpe']:.2f}; carry; quality", GOOD),
            (rf"value's lost decade: {100 * v['dd']['max']:.0f}\%; the spread at its 96th percentile", HML),
            (r"green returns: expected lower, realised higher, while concern rose", GOOD),
            (r"timing: weak signals; factor momentum explains stock momentum, and loses to holding all", UMD),
            (r"China: shells, E/P value with a Sharpe ratio above one, turnover", HML),
            (r"the industry: Dimensional, AQR, factor ETFs; tilts, tracking error, costs", QC.FIRM),
            (rf"the Track Record opens: average Sharpe {np.mean([x['research']['sharpe'] for x in env['rows'].values()]):.2f} "
             rf"$\to$ {np.mean([x['holdout']['sharpe'] for x in env['rows'].values()]):.2f}; counter {env['trials']}",
             QC.HOUSE),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 24 in fourteen lines")
        with self.voiceover(
            "Part twenty-four in fourteen lines. Six dollars in 1963 became between four and forty. Every factor model "
            "is rejected by the joint tests, and the useful question is by how much: size and value halve the CAPM's "
            "pricing errors. Size and value are built from two-by-three sorts, and both earned less once they were "
            "published. Momentum is the strongest classic factor, in stocks and, as trend, in every asset class. It "
            "crashes in rebounds after bear markets, when it is short the highest-beta stocks, and scaling it by "
            "volatility tames the crashes. Profitability and investment come from the dividend discount model, and "
            "make value redundant. Low-risk stocks earn as much as risky ones."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 24 in fourteen lines")
        with self.voiceover(
            "Value and momentum work in every market and hedge each other, and carry and quality travel too. Value lost "
            "for fourteen years, and its spread ended the research window near a record. Green stocks can outperform "
            "while their expected returns are lower. Timing signals are weak, and holding everything beat timing it. "
            "China needs its own factors. The industry sells the factors as tilts, with tracking error and costs. And "
            "the Track Record opened: the classic factors decayed, roughly as published anomalies do, and the "
            "diversified mix held up."
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
            "Six desk questions. Why hold both value and momentum? Because each pays and they hedge each other: the "
            "mix's Sharpe ratio is near double either's, and it disappoints only when both fall together. "
            "<bookmark mark='a'/> A model rejected with a small pricing error may still be the right tool; look at "
            "where its errors are. <bookmark mark='b'/> And the size premium's fall after 1981 cannot, with a "
            "t-statistic of six tenths, tell death from noise."
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
            "After a bear market and a sharp rebound, cut or hedge momentum: its beta of minus one is a bet nobody "
            "chose. <bookmark mark='a'/> A pension fund that cannot borrow should buy low-beta stocks and add futures, "
            "the opposite of what constrained investors usually do. <bookmark mark='b'/> And a value spread near a "
            "record tilts the odds toward value, modestly. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: the GRS statistic as a gain in Sharpe ratio, and with a single asset; the two-by-three "
            "sort by hand; the dividend discount model's book-to-market; the value-momentum mix; momentum's beta in a "
            "rebound; volatility scaling in a crash; betting against beta by hand; how many years a factor needs; and "
            "a green stock's realised and expected returns. Two more are qualifying-exam problems: Lo and "
            "MacKinlay's identity, and a world where we know its parts. Solutions, in English and Chinese, are in the "
            "notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"hundreds of factors, multiple testing, replication; the shrinkage SDF", [25]),
            (r"backtests with costs, funding and the trial counter", [26]),
            (r"characteristics into machine-learned expected returns", [27]),
            (r"the factor book as a portfolio: shrinkage, risk parity", [30]),
            (r"trend and carry as systematic macro", [32]),
            (r"crowding: the quant quake of 2007", [33]),
        ])
        with self.voiceover(
            "Where this comes back. Part twenty-five faces the hundreds of factors since published, and asks how many "
            "are real. Part twenty-six builds backtests with costs and funding, and introduces the trial counter "
            "properly. Part twenty-seven feeds the characteristics behind these factors to machine learning. Part "
            "thirty builds the factor book as a portfolio; Part thirty-two runs trend and carry as systematic macro; "
            "and Part thirty-three tells the story of the quant quake of August 2007, when crowded factor portfolios "
            "unwound together."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Ang, \textit{Asset Management}; Ilmanen, \textit{Expected Returns}; Bali, Engle and Murray, \textit{Empirical "
             r"Asset Pricing}; Pedersen, \textit{Efficiently Inefficient}, chs.\ 9--12; Cochrane, \textit{Asset Pricing}, "
             r"chs.\ 12--15"],
            [r"Black, Jensen and Scholes (1972); Fama and MacBeth (1973); Basu (1977); Banz (1981); Rosenberg, Reid and "
             r"Lanstein (1985); De Bondt and Thaler (1985); Gibbons, Ross and Shanken (1989); Fama and French (1992, 1993, "
             r"2006, 2015); Jegadeesh and Titman (1993); Lakonishok, Shleifer and Vishny (1994); Carhart (1997); Ang, "
             r"Hodrick, Xing and Zhang (2006); Lewellen, Nagel and Shanken (2010); Moskowitz, Ooi and Pedersen (2012); "
             r"Novy-Marx (2013); Asness, Moskowitz and Pedersen (2013); Asness and Frazzini (2013); Frazzini and Pedersen "
             r"(2014)",
             r"Barroso and Santa-Clara (2015); Hou, Xue and Zhang (2015); Daniel and Moskowitz (2016); McLean and Pontiff "
             r"(2016); Stambaugh and Yuan (2017); Koijen, Moskowitz, Pedersen and Vrugt (2018); Barillas and Shanken "
             r"(2018); Frazzini, Israel and Moskowitz (2018); Asness, Frazzini and Pedersen (2019); Liu, Stambaugh and Yuan "
             r"(2019); Haddad, Kozak and Santosh (2020); Cederburg et al.\ (2020); Arnott et al.\ (2021); Israel, Laursen "
             r"and Richardson (2021); Bolton and Kacperczyk (2021); Pástor, Stambaugh and Taylor (2021, 2022); Berg, "
             r"Kölbel and Rigobon (2022); Eisfeldt, Kim and Papanikolaou (2022); Ehsani and Linnainmaa (2022); Novy-Marx "
             r"and Velikov (2016, 2022). Data: Kenneth French; AQR; global-q.org; Robert Stambaugh"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from the first tests of the CAPM to factor "
            "momentum and green returns. Every number on screen was computed by the House's code from public data, "
            "with illustrative examples labelled as such."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("research",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 25, The Factor Zoo", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The research desk now has a library, and the Track Record its first ten rows. <bookmark mark='a'/> Next, "
            "Part twenty-five: the factor zoo. Hundreds of factors have been published since these. How many are real, "
            "how should a t-statistic be judged when thousands have been tried, and what survives replication?"
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
