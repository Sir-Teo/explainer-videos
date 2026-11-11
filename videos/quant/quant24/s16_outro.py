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
     'possibly: rejection is not inevitable. Assess practical errors and the proxy inference limits. Check where the alphas are, whether they line up with a characteristic the model leaves out, whether they survive costs and a hold-out, and what the rival models do'),
    (r"The size premium was 3.4\% a year before 1981 and 1.0\% after. Dead, never there, or hiding?",
     r"a $t$ of 0.6 cannot say. Publication decay, the January concentration, and the stronger premium once junk is "
     r"controlled for each point a different way; international data and other periods are the tie-breakers"),
    (r"The market fell 40\% in two years and just rose 10\%. Momentum's beta is about $-1$. What do you do?",
     'reassess under a predeclared risk budget. Ex-post beta is not advance knowledge; scaling or hedging can change losses, costs and forgone upside without guaranteeing protection'),
    (r"A pension fund that cannot borrow wants more return. High-beta stocks, or low-beta stocks plus futures?",
     'compare effective leverage, mandate, collateral and margin first; futures need explicit authorisation and funding. Constraint models are hypotheses, not proof that a trade is suitable'),
    ('Last annual spread observation through 2020: near its 96th percentile. What can the fitted line establish?',
     'the full-sample fit is descriptive, with about 5\\% $R^2$; it is not a reconstructed real-time forecast or evidence from sealed outcomes'),
]

PROBLEMS = [
    'With matching moments and unrestricted portfolio weights, show that the GRS numerator $\\hat\\alpha^\\top\\hat\\Sigma^{-1}\\hat\\alpha$ equals $SR^2(f, R) - SR^2(f)$, the gain in the squared maximum Sharpe ratio from adding the test assets.',
    'For $N=1$, use ML residual and factor covariance in standard GRS; show $F=t_{OLS}^2$. Why does the preserved mixed-convention proxy differ?',
    r"Six portfolios return SL 1.2\%, SM 1.0\%, SH 1.5\%, BL 0.6\%, BM 0.8\%, BH 1.1\% in a month. Compute SMB and HML.",
    r"With constant ROE, growth $g$ and discount rate $r$, show $M/B = (\text{ROE} - g)/(r - g)$. With ROE 12\%, $g$ = 5\%, "
    r"what $r$ gives B/M = 0.8?",
    r"Value and momentum: means 4\% and 5\%, volatilities 10\% each, correlation $-0.6$. Find the Sharpe ratio of the "
    r"50/50 mix.",
    r"After a bear market, winners have beta 0.8 and losers 1.8. The market rises 15\% in a month. What does that do "
    r"to UMD, before any stock-specific news?",
    "Momentum's realised volatility is 40\\% and the target 12\\%. What weight does this monthly volatility rule hold, and what is the scaled loss in a month of $-34\\%$?",
    r"BAB: $\beta_L = 0.7$, $\beta_H = 1.5$, monthly excess returns 0.6\% and 0.8\%. Compute the BAB return and its beta.",
    r"How many years does a Sharpe ratio of 0.45 need to reach $t = 2$? What Sharpe ratio reaches $t = 2$ in a five-year "
    r"hold-out?",
    'A green stock is priced to earn 5\\%, a brown one 7\\%. A climate-concern shock raises the green price 10\\% and lowers the brown 5\\% in one year. Use multiplicative surprise returns. What extra assumption fixes next-year expected returns?',    r"(qual) Derive Lo and MacKinlay's identity: for $w_i = (x_i - \bar x)/N$, the average of $\sum_i w_ir_i$ equals "
    r"own covariances times $(N - 1)/N^2$, minus cross covariances over $N^2$, plus the covariance of the means.",
    '(qual) For $N$ assets with equal unit loadings on a common iid factor and independent AR(1) idiosyncratic parts, compute each term, and show the factor contributes nothing to the profit.',
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("race"), load("tests"), load("crash"), load("everywhere"), load("valuedecade"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=24, color=col), wrapped_label(t, 11.7, 21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, r, t, c, e, v):
        items = [
            (f"research indices from 1: market {r['series']['MKT'][-1]:.0f}, momentum {r['series']['UMD'][-1]:.0f}; costs and cash yield omitted", MKT),
            (f"legacy inference proxies; average $|\\alpha|$ {100 * t['models']['CAPM']['mean_abs_alpha']:.1f}\\% (CAPM) to {100 * t['models']['FF5']['mean_abs_alpha']:.1f}\\% (five factors)", BAD),
            (r"size and value: 2 x 3 sorts; size 3.4\% before 1981, 1.0\% after; value halved", SMB),
            (r"momentum: winners 15\%, losers 1\%; time-series momentum Sharpe 1.06; the smile", UMD),
            (rf"momentum crashes: 1932, 2009; beta $-1$ in rebounds; scaling lifts Sharpe to {c['scaled']['sharpe']:.2f}",
             BAD),
            ('profitability and investment: the dividend discount model; small HML alpha is not payoff spanning; q', RMW),
            (r"low risk: BAB 8.2\% a year since 1930; volatility-sorted Sharpe 0.57 to 0.16", BAB),
        ]
        items2 = [
            (rf"everywhere: value and momentum in eight markets, correlation {e['global']['corr']:.2f}, mix Sharpe "
             rf"{e['global']['combo']['sharpe']:.2f}; carry; quality", GOOD),
            (rf"value's lost decade: {100 * v['dd']['max']:.0f}\%; the spread at its 96th percentile", HML),
            ('conditional green model: lower expected return can coexist with repricing gains', GOOD),
            ('timing: weak signals; UMD overlaps its regressor; equal-weight wins this sample', UMD),
            (r"China: shells, E/P value with a Sharpe ratio above one, turnover", HML),
            (r"the industry: Dimensional, AQR, factor ETFs; tilts, tracking error, costs", QC.FIRM),
            (r"registration and holdout accounting: conceptual; sealed experiment excluded", QC.HOUSE),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 24 in fourteen lines")
        with self.voiceover(
            'Part twenty-four in fourteen lines. Capitalised factor indices summarise research returns, with cash yield and costs omitted. Legacy inference proxies show model pricing errors; they do not carry exact GRS or Shanken calibration. Size and value use two-by-three sorts; their post-1981 averages are lower without a causal publication experiment. Momentum has positive historical average returns and severe rebound crashes. This monthly volatility rule reduces some sample losses without eliminating them. Profitability and investment motivate conditional dividend-discount comparisons; a small HML alpha does not prove exact spanning. Low-beta portfolios still carry risk.'
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 24 in fourteen lines")
        with self.voiceover(
            'The international value-momentum mix diversifies this historical sample; carry and quality require their own definitions. Value has a deep drawdown, and a wide valuation spread is not a guaranteed forecast. Green returns distinguish preference-driven repricing from conditional expected premia. The factor-momentum regression includes UMD on both sides, so its fit is not independent evidence. China uses different factor constructions and a historical institutional setting. The industry sells tilts with costs and tracking error. Registration and holdout accounting were conceptual: the sealed experiment was neither opened nor scored.'
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
            "Six desk questions. Why combine value and momentum? Their historical covariance improves this mix's Sharpe, without guaranteeing that both premia persist or that the mix beats both. <bookmark mark='a'/> A rejected model with small practical errors may still help; check calibration, residual risks, costs and genuinely new validation. <bookmark mark='b'/> A small post-1981 size t-statistic cannot distinguish a dead premium from imprecision or changing composition."
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
            "After a rebound, reassess momentum exposure under a predeclared risk budget; an ex-post beta is not advance crash knowledge. <bookmark mark='a'/> A pension mandate may restrict futures and effective leverage as well as borrowing. Any comparison needs collateral, margin and authorisation. <bookmark mark='b'/> A wide value spread and a weak full-sample fit do not establish a real-time forecast. No sealed outcome is used. The notes give conditional worked answers."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        def page(start, end):
            ps = problem_set(PROBLEMS[start:end], font_size=22)
            for number, row in enumerate(ps.rows, start + 1):
                old_number = row[0]
                new_number = label(rf"{number}.", font_size=22, color=old_number.get_color())
                new_number.match_height(old_number).move_to(old_number).align_to(old_number, RIGHT)
                old_number.become(new_number)
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=3))
            self.wait(2)
        with self.voiceover("The first six problems: consistent-moment GRS geometry and its one-asset identity; the two-by-three sort; the conditional Gordon formula; the value-momentum mix; and momentum beta in a rebound."):
            page(0, 6)
        self.clear_scene()
        with self.voiceover("Problems seven through ten: the monthly volatility rule, betting against estimated beta, the iid years-of-evidence approximation, and multiplicative green repricing. A one-off price shock alone does not determine next year's expected return."):
            page(6, 10)
        self.clear_scene()
        with self.voiceover("Two qualifying problems finish the set: the exact sample covariance identity, and an equal-loading iid common-factor example. State population versus sample conclusions. All twelve worked solutions are in the bilingual notes."):
            page(10, 12)
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
            'The textbooks and papers behind this part. Distinguish computed public-data results, cited research claims and labelled numerical illustrations. Backfilled public histories are not reconstructed real-time vintages, and the legacy inference conventions are explicitly qualified. No sealed result is reported.'
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("research",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 25, The Factor Zoo", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The research desk now has a qualified factor library; registration and holdout accounting remain conceptual. <bookmark mark='a'/> Next, Part twenty-five: the factor zoo. How should evidence be judged when many signals have been tried, and what survives replication?"
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
