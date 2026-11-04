from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import (BAD, BUG, ENGINE, GOOD, HONEST, HURDLE, IS_C, NOISE, OOS_C, PART, RULE, comma,
                                         load)

DESK = [
    (r"Your backtest has a Sharpe ratio of 3. List what could be wrong.",
     r"look-ahead (a same-bar signal, period-stamped data, revisions); survivorship; selection from many tries; fills "
     r"at prices no one got, latency, costs, borrow; corporate actions; a sample too short or too calm; leaky "
     r"validation; a regime that ended. First rerun it in the engine at the next open with costs, then ask for the count"),
    (r"400 settings of one idea, ten years of daily data; the best has a Sharpe ratio of 1.2. Better than noise?",
     r"the hurdle for 400 independent tries is about 0.94, so perhaps; but the settings are correlated (a smaller "
     r"$N$) and their Sharpe ratios spread more than noise (a larger $V$). Compute the DSR with both before deciding"),
    (r"Three years of monthly returns, a Sharpe ratio of 2.0, first-order autocorrelation 0.4. A fair range?",
     r"Lo's correction cuts 2.0 to about 1.5, and three years give a standard error near 0.6: roughly 0.3 to 2.7. "
     r"Smoothed returns also hide risk; ask how the book is marked"),
    (r"200 trades a year, 4 bp gross a trade, costs estimated at 3 bp. How sure must you be?",
     r"sure to within a basis point: the net edge is 1 bp, 2\% a year at full turnover, and a cost model wrong by "
     r"a third turns it to zero. Trade it small and measure the costs live first"),
    (r"A default model with a three-year label, validated by five random folds of firm-years. The leak?",
     r"a firm's consecutive years share most of a label and almost all of their features: split by firm and by time, "
     r"purge three years around each test fold, and embargo after it"),
    (r"A monitor stands at 12 against a threshold of 20. Switch to a threshold of 10 to stop the strategy now?",
     r"no: choosing the threshold after seeing the path voids the guarantee. Decide in advance; or start a new "
     r"monitor with a new claim, from today's data on"),
]

PROBLEMS = [
    r"For iid normal returns show, by the delta method, that $\operatorname{Var}\widehat{SR} \approx (1 + SR^2/2)/T$.",
    r"Show that the maximum of $N$ independent standard normals has CDF $\Phi(c)^N$, and find its median for $N = 100$.",
    r"Compute the expected best annualised Sharpe ratio of 100 noise strategies with five years of daily returns.",
    r"Find the minimum backtest length for $N = 1{,}000$ independent tries at a target Sharpe ratio of 1.",
    r"PSR: monthly $\widehat{SR} = 0.1$, $T = 60$, skewness $-1$, kurtosis 6. Find $\text{PSR}(0)$.",
    r"Find Lo's $\eta(12)$ when $\rho_1 = 0.3$ and all other autocorrelations are zero. By how much does "
    r"$\sqrt{12}$ overstate the annual Sharpe ratio?",
    r"CSCV with $S = 16$ blocks: how many splits are there, and in how many is a given block in sample?",
    r"Purged 5-fold CV of 5{,}000 daily observations with 20-day labels and a 20-day embargo: how many training "
    r"observations does an interior fold lose?",
    r"A stationary bootstrap with $p = 0.1$: the expected block length, and the probability a block is at least 20 "
    r"days long.",
    r"A 5\% e-process monitor is read every month for ten years while the claim is true. Bound the probability of "
    r"ever stopping. Compare with ten years of monthly 5\% $t$-tests.",
    r"(qual) $X \sim N(\mu, \Sigma)$, winner $\hat\jmath = \arg\max X$. Show $Z = X - \Sigma_{\cdot j}X_j/\Sigma_{jj}$ is "
    r"independent of $X_j$, and that given $\hat\jmath = j$ and $Z$, $X_j$ is a normal truncated to $[L(Z), U(Z)]$. Find $L, U$.",
    r"(qual) $J$ independent $N(0, 1)$ estimates, all true means 0. Show the naive 95\% interval for the winner "
    r"covers with probability $\Phi(1.96)^J - \Phi(-1.96)^J$; evaluate for $J = 2$ and $J = 50$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("lookahead"), load("survivor"), load("select"), load("engine"), load("sharpe"),
                   load("counter"), load("rules"), load("dsr"), load("pbo"), load("cv"), load("rc"), load("monitor"),
                   load("planted"), load("funding"), load("envelope"))
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

    def recap(self, a, s, se, e, sh, k, r, d, p, c, rc, m, pl, f, env):
        items = [
            (rf"look-ahead: one subscript turns {a['ma200']['sr_honest']:.2f} into {a['ma200']['sr_bug']:.2f}; GDP is "
             rf"revised by {a['gdp']['mean_abs_rev']:.1f} points on average", BUG),
            (rf"survivorship: {100 * s['bank_share']:.0f}\% of bankrupt filers remain in today's ticker file; "
             rf"no-skill survivors earn {100 * s['sim']['mean_alive']:.1f}\% a year", BAD),
            (rf"selection: the best of 10{{,}}000 noise strategies shows {se['dist']['10000']['mean']:.2f} in five years",
             HURDLE),
            (rf"the engine: EEM's reversal {e['vector']['sr']:.2f} on paper, {e['runs']['all']['sr']:.2f} filled and "
             r"charged", ENGINE),
            (rf"the Sharpe ratio's error: $\pm${sh['sim']['sd']:.2f} in five years; smoothing overstates it by "
             rf"{100 * sh['smooth']['overstated']:.0f}\%", RULE),
            (rf"the counter: {k['before']} before this part, {comma(env['trials'])} after; the hurdle rises like "
             r"$\sqrt{2 \ln N}$", QC.HOUSE),
            (rf"10{{,}}000 rules: best {r['best_in']:.2f} to 1986, {r['best_out']:.2f} after; rank correlation "
             rf"{r['rank_corr']:.2f}", IS_C),
        ]
        items2 = [
            (rf"the deflated Sharpe ratio passes the 1926--86 winner, fails the 1987--2020 one ({d['out']['eff']['dsr']:.2f})",
             GOOD),
            (rf"PBO: {p['in']['pbo']:.2f} before 1987, {p['out']['pbo']:.2f} after; statistics cannot see a regime end",
             OOS_C),
            (rf"cross-validation: shuffled $R^2$ {100 * c['res']['shuffled']['r2']:+.1f}\%, purged "
             rf"{100 * c['res']['purged']['r2']:+.1f}\%", BUG),
            (rf"reality checks: $p$ = {rc['in']['rc_p']:.2f} then {rc['out']['rc_p']:.3f}; Romano--Wolf finds "
             rf"{rc['in']['rw_n']}, then {rc['out']['rw_n']}", HURDLE),
            (rf"e-value monitors flag {m['full']['flagged']} of {m['n']} published predictors; e-BH keeps {m['full']['ebh']}",
             BAD),
            (rf"planted alpha: strict tests invent nothing and find little in five years; breadth costs time", GOOD),
            (rf"the ramp stops {100 * f['overfit_1']['stopped']:.0f}\% of overfit strategies; the rule opened at "
             rf"{env['sr_hold']:+.2f}", QC.HOUSE),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 26 in fourteen lines")
        with self.voiceover(
            "Part twenty-six in fourteen lines. One subscript of look-ahead turned a mediocre rule into a star, and the "
            "economic data a backtest reads today are not the data anyone saw at the time. Survivorship removes almost "
            "every bankrupt company from a universe built from today's tickers, and gives managers with no skill a "
            "record. The best of ten thousand noise strategies looks excellent. A reversal that worked on paper lost "
            "money once it was filled and charged. A Sharpe ratio estimated from five years is uncertain by almost half "
            "its size, and smoothing inflates it. The trial counter now stands above ten thousand. And ten thousand "
            "technical rules found an edge before 1987 that vanished after it."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 26 in fourteen lines")
        with self.voiceover(
            "The deflated Sharpe ratio passed the first era's winner and failed the second's. The probability of "
            "overfitting was zero within the first era and near a half within the second: these tests measure "
            "selection, and cannot see a world that changes. Shuffled cross-validation found a forecast that purged "
            "folds did not. The reality checks agreed with Sullivan, Timmermann and White. E-value monitors flagged a "
            "third of the published predictors as not what their backtests promised. Planted alpha showed the strict "
            "tests to be honest and slow. And a capital ramp, gated by a monitor, limited what an overfitted strategy "
            "could lose, while the best rule of all lost money on the sealed years."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q, a, width=12.4, font_size=21) for q, a in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. A backtest with a Sharpe ratio of three: list the eight suspects, then rerun it at the "
            "next open with costs, and ask for the count. <bookmark mark='a'/> Four hundred settings and a best of one "
            "point two over ten years: near the hurdle of point nine four, so compute the deflated Sharpe ratio with "
            "the real correlation and spread. <bookmark mark='b'/> Three years at a Sharpe ratio of two with "
            "autocorrelation point four: about one and a half after Lo's correction, and anywhere from a third to two "
            "and three quarters."
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
            "Four basis points of edge against three of cost needs a cost estimate good to one basis point. "
            "<bookmark mark='a'/> A default model with a three-year label leaks through random folds of firm-years; "
            "split by firm and by time, and purge. <bookmark mark='b'/> And a monitor's threshold is chosen before the "
            "data, never after. Full solutions are in the notes."
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
            "And twelve problems: the Sharpe ratio's standard error by the delta method; the distribution of the best of "
            "N; the hurdle for a hundred tries; the minimum backtest length; a probabilistic Sharpe ratio with skew; "
            "Lo's correction; counting CSCV's splits; what purging costs; the stationary bootstrap's blocks; and "
            "why an e-process can be read every month. Then two qualifying-exam problems: the truncated normal behind "
            "inference on winners, and how often the naive interval for a winner covers. Solutions, in English and "
            "Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"purged validation and deflation for machine-learned signals", [27, 28]),
            (r"alpha miners that try millions of rules, against the counter", [29]),
            (r"the engine's cost model, made realistic: impact and capacity", [31, 37]),
            (r"monitors and ramps inside a firm's allocation process", [34]),
            (r"the finale: every Track Record row deflated by the full count", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Parts twenty-seven and twenty-eight validate machine-learned and text signals with "
            "purged folds and deflate them. Part twenty-nine's alpha miners try millions of rules, against the counter. "
            "Parts thirty-one and thirty-seven make the engine's costs realistic. Part thirty-four puts monitors and "
            "ramps inside a firm's allocation of capital. And the finale deflates every row of the Track Record by "
            "the series' full count."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Lopez de Prado, \textit{Advances in Financial Machine Learning}, ch.\ 7--14; Isichenko, \textit{Quantitative "
             r"Portfolio Management}, ch.\ 7; Bailey and Lopez de Prado, \textit{Machine Learning for Asset Managers}"],
            [r"Cowles (1933); Alexander (1961); Fama and Blume (1966); Fisher (1966); Lo and MacKinlay (1990); Brock, "
             r"Lakonishok and LeBaron (1992); Brown, Goetzmann, Ibbotson and Ross (1992); Politis and Romano (1994); "
             r"Shumway (1997); Shumway and Warther (1999); Sullivan, Timmermann and White (1999); White (2000); Lo (2002); "
             r"Mertens (2002); Getmansky, Lo and Makarov (2004)",
             r"Hansen (2005); Romano and Wolf (2005); Leinweber (2007); Bailey and Lopez de Prado (2012, 2014); Bailey, "
             r"Borwein, Lopez de Prado and Zhu (2014, 2017); Harvey and Liu (2015); Arnott, Harvey and Markowitz (2019); "
             r"Wang and Ramdas (2022); Grunwald, de Heide and Koolen (2024). Data: Kenneth French; Philadelphia Fed "
             r"Real-Time Data Set; EDGAR; Yahoo Finance; Cboe; Open Source Asset Pricing 2024.10"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from Alfred Cowles in 1933 to safe testing "
            "in 2024. Every number on screen was computed by the House's code from public data, with simulations "
            "labelled as such."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("research", "data"))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 27, Machine Learning for Returns", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House now has a backtester that cannot see tomorrow, a count of every trial it has run, and the "
            "statistics to judge a result against that count. It knows that a backtest can be clean, correct and "
            "still wrong, and that the only cure is evidence the backtest has not seen. "
            "<bookmark mark='a'/> Next, Part twenty-seven: machine learning for returns. Models with millions of "
            "parameters, trained on decades of characteristics, and every one of them validated, deflated and "
            "registered the way this part has taught."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
