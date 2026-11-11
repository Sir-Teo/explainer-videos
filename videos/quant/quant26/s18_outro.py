from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import (BAD, BUG, ENGINE, GOOD, HONEST, HURDLE, IS_C, NOISE, OOS_C, PART, RULE, comma,
                                         load)

DESK = [
    (r"Your backtest has a Sharpe ratio of 3. List what could be wrong.",
     r"look-ahead (a same-bar signal, period-stamped data, revisions); survivorship; selection from many tries; fills "
     r"at prices no one got, latency, costs, borrow; corporate actions; a sample too short or too calm; leaky "
     r"validation; a regime that ended. Check the information clock, available inputs and fill assumptions; inspect the full search record and uncertainty"),
    (r"400 settings of one idea, ten years of daily data; the best has a Sharpe ratio of 1.2. Better than noise?",
     r"the independent-normal mean maximum is about 0.94, not a significance cutoff. Correlation changes the heuristic "
     r"$N$ and the trial spread affects $V$; DSR is an approximate score, not an exact discovery test"),
    (r"Three years of monthly returns, a Sharpe ratio of 2.0, first-order autocorrelation 0.4. A fair range?",
     r"if all higher autocorrelations are zero, Lo's population annualisation maps 2.0 to about 1.52. A valid confidence interval needs dependence and higher-moment information; the first autocorrelation alone is insufficient"),
    (r"200 trades a year, 4 bp gross a trade, costs estimated at 3 bp. How sure must you be?",
     r"sure to within a basis point: the net edge is 1 bp; 2\% arithmetic per year assumes 200 full-capital turnovers, and a cost model wrong by "
     r"a third turns it to zero. Trade it small and measure the costs live first"),
    (r"A default model with a three-year label, validated by five random folds of firm-years. The leak?",
     r"overlapping labels and repeated firms can contaminate the target: fit preprocessing only on available training data, choose firm separation for new-firm generalisation, "
     r"purge the actual label spans, allow mature labels and choose a gap for the feature and target windows"),
    (r"A monitor stands at 12 against a threshold of 20. Switch to a threshold of 10 to stop the strategy now?",
     r"a valid e-process cannot retain the 5\% bound at 10; Ville gives 10\% there. Any new monitor needs a justified null, past-measurable choices and an overall error budget"),
]

PROBLEMS = [
    r"For iid normal returns show, by the delta method, that $\operatorname{Var}\widehat{SR} \approx (1 + SR^2/2)/T$.",
    r"Show that the maximum of $N$ independent standard normals has CDF $\Phi(c)^N$, and find its median for $N = 100$.",
    r"Use the independent-normal extreme-value mean approximation for the best annualised Sharpe ratio of 100 noise strategies over five years.",
    r"Equate the approximate mean null maximum to a target Sharpe of 1 for $N=1{,}000$ independent tries. Find the mean-hurdle length, not a power requirement.",
    r"PSR: monthly $\widehat{SR} = 0.1$, $T = 60$, skewness $-1$, kurtosis 6. Find $\text{PSR}(0)$.",
    r"Find Lo's $\eta(12)$ when $\rho_1 = 0.3$ and all other autocorrelations are zero. By how much does "
    r"$\sqrt{12}$ overstate the annual Sharpe ratio?",
    r"CSCV with $S = 16$ blocks: how many splits are there, and in how many is a given block in sample?",
    r"Use the library convention $t_0=i,t_1=i+20$, inclusive spans, 5 contiguous folds of 5{,}000 observations and 20 additional embargo days after the test label span. How many training observations does an interior fold lose?",
    r"A stationary bootstrap with $p = 0.1$: the expected block length, and the probability a block is at least 20 "
    r"days long.",
    r"A valid e-process under its bounded conditional-mean null is read 120 times at threshold 20. Bound any rejection. Compare with 120 independent 5\% tests, then explain why nested monthly $t$-tests need not follow that benchmark.",
    r"(qual) $X \sim N(\mu, \Sigma)$, winner $\hat\jmath = \arg\max X$. Show $Z = X - \Sigma_{\cdot j}X_j/\Sigma_{jj}$ is "
    r"independent of $X_j$, and that given $\hat\jmath = j$ and $Z$, $X_j$ is a normal truncated to $[L(Z), U(Z)]$. Find $L, U$.",
    r"(qual) $J$ independent $N(0, 1)$ estimates, all true means 0. Show the naive 95\% interval for the winner "
    r"covers with probability $\Phi(1.96)^J - \Phi(-1.96)^J$; evaluate for $J = 2$ and $J = 50$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("lookahead"), load("select"), load("sharpe"),
                   load("counter"), load("rules"), load("dsr"), load("pbo"), load("cv"), load("rc"), load("monitor"),
                   load("planted"), load("funding"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=28, color=col), wrapped_label(t, 11.7, 26)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self,a,se,sh,k,r,d,p,c,rc,m,pl,f):
        first=[
            (rf"look-ahead example: Sharpe {a['ma200']['sr_honest']:.2f} to {a['ma200']['sr_bug']:.2f} ; monthly vintages need availability clocks",BUG),
            (r"survivorship: original SEC item blocked; fixed conditioning example only",BAD),
            (rf"independent noise simulation: best of 10{{,}}000 has mean annual Sharpe {se['dist']['10000']['mean']:.2f}",HURDLE),
            (r"execution: original Yahoo item blocked; fixed quotes, cash ledger and corporate actions",ENGINE),
            (rf"five-year IID simulation Sharpe SD {sh['sim']['sd']:.2f}; serial dependence needs separate inference",RULE),
            (rf"original prior-part registration snapshot: {comma(k['before'])}; recorded trials are a lower bound on research",QC.HOUSE),
            (rf"selected technical rule: Sharpe {r['best_in']:.2f} through 1986, {r['best_out']:.2f} in 1987--2020; gross excess-cash index",IS_C)]
        second=[
            (rf"later-era DSR score {d['out']['eff']['dsr']:.2f}: normal-moment approximation and heuristic effective trials",GOOD),
            (rf"CSCV below-median frequency: {p['in']['pbo']:.2f} earlier, {p['out']['pbo']:.2f} later; not a future-failure probability",OOS_C),
            (rf"original CV scores: {100*c['res']['shuffled']['r2']:+.1f}\% shuffled, {100*c['res']['purged']['r2']:+.1f}\% purged; residual leakage",BUG),
            (rf"reality-check exceedances: {round(500*rc['in']['rc_p'])}/500 and {round(500*rc['out']['rc_p'])}/500; bootstrap inference is approximate",HURDLE),
            (rf"clipped retrospective diagnostics: {m['full']['flagged']} of {m['n']} crossed 20; raw-return guarantees unestablished",BAD),
            (r"planted-alpha simulations compare power and false findings under specified distributions",GOOD),
            (rf"simulated overfit ramp stop rate {100*f['overfit_1']['stopped']:.0f}\%; sealed experiment remains unopened in this review",QC.HOUSE)]
        head,rows=self._rows(list(enumerate(first,1)),r"Part 26 in fourteen lines")
        with self.voiceover("Part twenty-six in fourteen qualified lines. A same-bar signal demonstrates look-ahead, while economic data require actual publication clocks. The original SEC snapshot fails its source hash check, so its unavailable numerical comparison is withheld. Selection makes the best noise strategy look strong. The original Yahoo execution item is also blocked; fixed arithmetic explains fills and costs without another historical strategy. Sharpe standard errors require distribution and dependence assumptions. The recorded trial ledger is a lower bound on the broader research process. The selected technical rule is compared across two research eras without a sealed score."):
            self.play(FadeIn(head),LaggedStart(*[FadeIn(row,shift=RIGHT*.2) for row in rows],lag_ratio=.6,run_time=20))
        self.clear_scene()
        head,rows=self._rows(list(enumerate(second,8)),r"Part 26 in fourteen lines")
        with self.voiceover("DSR is an approximate confidence score, not a probability that a strategy is true. PBO counts below-median rank events inside overlapping historical splits. The original validation results retain scaling and boundary leakage. Bootstrap zero means no exceedance in five hundred draws, not zero true probability. Clipped historical monitor paths do not establish raw-return error guarantees. Planted alpha and capital ramps illustrate specified simulations. Existing experiment code is preserved but remains unopened and unscored throughout this review."):
            self.play(FadeIn(head),LaggedStart(*[FadeIn(row,shift=RIGHT*.2) for row in rows],lag_ratio=.6,run_time=18))
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q, a, width=12.4, font_size=21) for q, a in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. For an unusually strong backtest, trace data availability, universe selection, search choices, timestamps, fills, costs, corporate actions and sampling uncertainty. <bookmark mark='a'/> Four hundred independent-normal tries over ten years give a mean-maximum hurdle near point nine four, but an observed winner of one point two is not thereby a significant discovery. Dependence and the trial spread matter, while DSR remains an approximation. <bookmark mark='b'/> With a reported annualised Sharpe ratio of two and first-order autocorrelation point four, assuming all higher autocorrelations zero gives a population scaling correction near one point five two. Those summaries alone do not establish a valid confidence interval."
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
            "Three more questions. <bookmark mark='a'/> A one-basis-point per-trade margin is sensitive to implementation error. The illustrative two-percent annual arithmetic assumes two hundred full-capital turnovers and no other costs. For three-year default labels, align evaluation with the prediction target, prevent overlapping label periods, and fit preprocessing using available training information. Group separation also matters when assessing generalisation to new firms. <bookmark mark='b'/> A valid e-process at twelve cannot retain a five-percent threshold guarantee if the threshold becomes ten. Ville instead gives ten percent at ten. New monitoring claims and restarts require justified nulls, past-measurable choices and a controlled overall error budget."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        def page(start,end):
            ps=problem_set(PROBLEMS[start:end],font_size=21)
            for number,row in enumerate(ps.rows,start+1):
                old=row[0];new=label(rf"{number}.",font_size=21,color=old.get_color());new.match_height(old).move_to(old).align_to(old,RIGHT);old.become(new)
            self.play(FadeIn(ps.head),LaggedStart(*[FadeIn(row) for row in ps.rows],lag_ratio=.3,run_time=3));self.wait(2)
        with self.voiceover("The first six problems derive the independent-normal Sharpe variance, a normal maximum distribution and median, an approximate expected noise hurdle and its mean-based backtest length, the PSR confidence score, and Lo's conditional annualisation correction. Distinguish asymptotic formulas and confidence scores from exact selection tests."):
            page(0,6)
        self.clear_scene()
        with self.voiceover("Problems seven through ten count the combinatorial cross-validation splits, derive the interior-fold loss under the library's explicit inclusive purging convention, calculate a geometric bootstrap block probability, and compare a valid e-process with repeated fixed-horizon tests. Repeated monthly tests are dependent; the independent-case calculation is a benchmark, not their universal error rate."):
            page(6,10)
        self.clear_scene()
        with self.voiceover("Two qualifying problems derive both lower and upper selection bounds in the known-covariance Gaussian model, then compute the naive winner interval's coverage for independent null estimates. With two estimates coverage is approximately ninety-five percent, while fifty give about twenty-eight percent. All twelve worked solutions are retained in English and Chinese."):
            page(10,12)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"purged validation and deflation for machine-learned signals", [27, 28]),
            (r"alpha miners that try millions of rules, against the counter", [29]),
            (r"more detailed execution assumptions: impact and capacity", [31, 37]),
            (r"monitors and ramps inside a firm's allocation process", [34]),
            (r"the finale: audit recorded results, search counts and uncertainty", [43]),
        ])
        with self.voiceover(
            "Later chapters revisit validation for machine learning and text, broad searches, impact and capacity, and allocation. Their checks still need available-time inputs, mature labels, appropriate search accounting and explicit execution assumptions. Adding purging or a fitted deflation score is not a certificate. The final lecture audits what the recorded results and search counts can support."
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
             r"Wang and Ramdas (2022); Andrews, Kitagawa and McCloskey (2024); Grunwald, de Heide and Koolen (2024). Data: Kenneth French; Philadelphia Fed "
             r"Real-Time Data Set; EDGAR; Yahoo Finance; Cboe; Open Source Asset Pricing 2024.10"])
        with self.voiceover(
            "The references connect data availability, selection, inference and implementation. Original public-data calculations, saved simulations, explicitly fabricated fixed arithmetic and known-Gaussian theorems are different kinds of evidence. Unavailable frozen historical outputs remain withheld. The reading list and all twelve worked solutions are retained in English and Chinese in the accompanying notes."
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
