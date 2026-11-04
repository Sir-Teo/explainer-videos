from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant33.common import (BAD, COST_C, GOOD, KAL_C, NET_C, OU_C, PART, RES_C, SPREAD_C, comma, load)

DESK = [
    (r"Two prices are cointegrated. What do you trade, and what can go wrong?",
     r"the spread $y - \beta x$, against its mean; the tie can break, $\beta$ is estimated on the same days, and a screen "
     r"of 1{,}176 pairs at 5\% passes about 59 by chance alone"),
    (r"What is an s-score?",
     r"$(X_t - \hat\theta)/\hat s_{\text{eq}}$ for the OU fitted to a residual's cumulative sum over the last 60 days; "
     r"Avellaneda and Lee enter beyond $\pm 1.25$ and exit near the mean"),
    (r"A Kalman spread reverts with a half-life of one day. Is it a pair?",
     r"not on that evidence: it is the filter's one-step forecast error, close to white noise by construction; test the "
     r"profit out of sample instead"),
    (r"Where does a contrarian's profit come from?",
     r"Lo and MacKinlay: own reversal, plus cross-autocovariance (lead-lag), minus the dispersion of mean returns"),
    (r"Why did the residual book lose after costs with the standard bands?",
     r"every trade is two trades; about 20\% daily turnover at 5 bp a side on both legs costs about 5\% a year, more "
     r"than the 3.6\% it earned gross"),
    (r"How should the band depend on costs?",
     r"$m^*/s_{\text{eq}} = h(c/s_{\text{eq}})$, one curve for every spread, with $h(x) \approx (3x)^{1/3}$ for small "
     r"costs; the speed of reversion scales the profit, not the band"),
]

PROBLEMS = [
    r"A spread's daily AR(1) slope is 0.9: its speed $\kappa$ and half-life.",
    r"All 1{,}176 pairs of 49 industries tested at 5\%: the expected false passes, and the Bonferroni level.",
    r"A spread with $s_{\text{eq}} = 2\%$ and round-trip cost 0.6\%: $c/s_{\text{eq}}$, and the best band from the curve.",
    r"A residual book: gross Sharpe 0.8 at 4\% volatility, 20\% daily turnover, 5 bp a side on both legs. Net return.",
    r"Two zero-mean assets with $\operatorname{Cov}(r_{2,t}, r_{1,t-1}) = \gamma$ and no other autocovariance: the "
    r"contrarian's expected profit.",
    r"A filter's one-step forecast errors have AR(1) slope 0.3. What does that say about cointegration?",
    r"A reversal earns 2 bp a day gross and trades 40\% of its book daily at 5 bp a side. Net.",
    r"A daily IC of 0.01 across 49 assets: the years needed for two standard errors.",
    r"A true Sharpe ratio of 0.3: the years needed for two standard errors.",
    r"Use the small-cost law to find the band for $c/s_{\text{eq}} = 0.01$ and the share of the frictionless rate kept.",
    r"(qual) For $dX = -\kappa X\,dt + \sigma dW$, derive $\mathbb E_{-m}[T_0]$ and $\mathbb E_0[\tau_m]$ from Dynkin's "
    r"formula, prove the renewal-reward rate $R(m) = (m - c)/(\mathbb E_0[\tau_m] + \mathbb E_{-m}[T_0])$, and show by "
    r"scaling that $m^*/s_{\text{eq}}$ depends on $c/s_{\text{eq}}$ alone.",
    r"(qual) With $c = 0$ show $R(m) \to \sigma\sqrt{\kappa/\pi}$ as $m \to 0$; then show the $m^2$ terms of the two "
    r"passage times cancel, and deduce $m^*/s_{\text{eq}} \sim (3c/s_{\text{eq}})^{1/3}$ and "
    r"$R(m^*)/R(0^+) = 1 - \frac12(3c/s_{\text{eq}})^{2/3} + o(c^{2/3})$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("pairs"), load("coint"), load("kalman"), load("lomac"), load("pca"), load("deep"),
                   load("nagel"), load("envelope"), load("smallc"))
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

    def recap(self, pr, co, ka, lm, p, dp, ng, e, sc):
        frac = 100 * float(np.mean(co["frac"]))
        th = p["configs"]["5f/60d/theory"]
        items = [
            (r"from Morgan Stanley's desk in the 1980s to the quant firms: reversion, made systematic", SPREAD_C),
            (rf"distance pairs on industries: Sharpe {pr['all']['sharpe']:.2f}, 1964--2020", SPREAD_C),
            (rf"cointegration: {frac:.1f}\% of pairs pass a year against {100 * co['false_positive']:.1f}\% by chance; "
             rf"{100 * co['persist']:.0f}\% pass again", SPREAD_C),
            (r"the OU spread: speed, mean and $s_{\text{eq}}$ from one regression, with Kendall's bias", OU_C),
            (rf"residuals of five eigenportfolios: gross Sharpe {p['al']['gross']['sharpe']:.2f}, net "
             rf"{p['al']['net']['sharpe']:.2f}", RES_C),
            (rf"the Kalman trap: ADF {ka['adf_kalman']:.1f}, a forecast error, not a pair", KAL_C),
            (rf"Lo--MacKinlay: size portfolios' own {1e4 * lm['size']['own']:+.2f} bp, cross "
             rf"{1e4 * lm['size']['cross']:+.2f} bp a day", OU_C),
        ]
        items2 = [
            (rf"a network on residual paths: IC {dp['ic']:.4f}, net Sharpe {dp['net_after_costs']['sharpe']:.1f}", NET_C),
            (rf"liquidity: no VIX link on industries ($t = {ng['t']:.2f}$); August 2007's crowd", COST_C),
            (rf"the research band: net Sharpe {th['sharpe']:.2f} where the standard bands lost", RES_C),
            (rf"2021--25 sealed: gross {e['hold_gross']['sharpe']:.2f}, net {e['hold']['sharpe']:.2f}; counter "
             rf"{comma(e['trials'])}", GOOD),
            (r"Rule 33: every leg's costs, derived bands, every pair a trial, profit tested, crowding stated", QC.HOUSE),
            (r"research: $R(m) = (m - c)/(\mathbb E_0[\tau_m] + \mathbb E_{-m}[T_0])$, one universal curve", OU_C),
            (r"the small-cost law $m^*/s_{\text{eq}} \approx (3c/s_{\text{eq}})^{1/3}$", GOOD),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 33 in fourteen lines")
        with self.voiceover(
            "Part thirty-three in fourteen lines. Statistical arbitrage began as a pairs desk at Morgan Stanley in the "
            "1980s and became the quant firms' core business. Distance pairs on industries no longer pay. Cointegration "
            "tests find about twice as many pairs as chance, and almost none twice. The Ornstein-Uhlenbeck spread gives "
            "a speed, a mean and a width from one regression. Residuals against eigenportfolios revert strongly before "
            "costs. A moving hedge ratio can manufacture reversion. And contrarian profits split into own reversal and "
            "lead-lag."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 33 in fourteen lines")
        with self.voiceover(
            "A network on residual paths learned almost nothing, and its trading cost the rest. The liquidity premium "
            "did not show on industries, but crowding showed in 2007. The research chapter's band was the only rule to "
            "keep a profit after costs, and on the sealed years it stayed positive, with the gross reversion unchanged. "
            "And the theorem gives one curve for every spread, with a cube-root law for small costs."
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
            "Six desk questions. Two prices are cointegrated: what do you trade, and what can go wrong? The spread, and "
            "the tie, the estimate and the screen. <bookmark mark='a'/> What is an s-score? A residual's distance from "
            "its fitted mean, in equilibrium deviations. <bookmark mark='b'/> And is a Kalman spread with a one-day "
            "half-life a pair? Not on that evidence."
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
            "Where does a contrarian's profit come from? Own reversal and lead-lag. <bookmark mark='a'/> Why did the "
            "residual book lose with the standard bands? Every trade is two trades. <bookmark mark='b'/> And how should "
            "the band depend on costs? Through one curve, with a cube root near zero. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def answers(self):
        b = 0.95
        hl = math.log(2) / -math.log(b)
        bk = b - (1 + 3 * b) / 60
        hlk = math.log(2) / -math.log(bk)
        yrs_ic = 4 / (49 * 0.01 ** 2) / 252
        yrs_sr = (2 / 0.3) ** 2
        net6 = 100 * (0.8 * 0.04 - 2 * 0.2 * 5e-4 * 252)
        pages = [
            [(r"Ch.~1: an edge of 3 bp, spreads from 10 to 2 bp", r"it becomes tradable for everyone, so competitors "
              r"arrive and harvest it: cheaper trading can shrink an edge"),
             (r"Ch.~2: half-life 20 days, a 6-month limit", r"about right for the holding limit; with low costs the "
              r"research chapter's band would be narrower"),
             (r"Ch.~3: 2{,}000 unrelated pairs at 5\%", r"about 100 pass, and about 5 of those pass again")],
            [(r"Ch.~4: an AR(1) slope of 0.95", rf"a half-life of {hl:.1f} days; Kendall's bias makes a 60-day estimate "
              rf"about {bk:.3f}, a half-life near {hlk:.0f} days"),
             (r"Ch.~5: gross Sharpe 0.8, 20\% turnover, two legs", rf"3.2\% less about 5.0\% of costs: "
              rf"${net6:.1f}\%$ a year"),
             (r"Ch.~6: forecast errors with slope 0.3", r"nothing about cointegration: a forecast error says how good the "
              r"filter is, not whether the prices are tied")],
            [(r"Ch.~7: large caps lead small caps", r"the contrarian makes money from the cross term alone, with no "
              r"reversal in any asset"),
             (r"Ch.~8 and Ch.~10: an IC of 0.01; a Sharpe ratio of 0.3", rf"about {yrs_ic:.1f} years; about "
              rf"{yrs_sr:.0f} years"),
             (r"Ch.~9: 2 bp gross, 40\% turnover at 5 bp", r"nothing: $0.4 \times 5 = 2$ bp a day of costs"),
             (r"research: twice the speed", r"the same band in units of $s_{\text{eq}}$, and twice the profit rate")],
        ]
        def show(page):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=19) for q_, a_ in page]).arrange(DOWN, buff=0.22)
            if cards.height > 7.2:
                cards.scale_to_fit_height(7.2)
            return cards

        cards = show(pages[0])
        with self.voiceover(
            "The pause questions, answered. Cheaper trading can shrink an edge, by letting everyone trade it. "
            "<bookmark mark='a'/> A two-deviation trigger suits a twenty-day half-life and a six-month limit. "
            "<bookmark mark='b'/> And of two thousand unrelated pairs, about a hundred pass, and about five pass again."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        cards = show(pages[1])
        with self.voiceover(
            f"A slope of point nine five is a half-life of {hl:.1f} days, but sixty days of data will usually say about "
            f"{hlk:.0f}. <bookmark mark='a'/> The residual book keeps nothing: {net6:.1f} percent a year after costs. "
            "<bookmark mark='b'/> And a filter's forecast errors say how good the filter is, not whether prices are tied."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        cards = show(pages[2])
        with self.voiceover(
            "When large caps lead small caps, the contrarian makes money from the cross term alone. "
            f"<bookmark mark='a'/> An IC of a hundredth needs about {yrs_ic:.0f} years to prove; a Sharpe ratio of point "
            f"three, about {yrs_sr:.0f}. <bookmark mark='b'/> Two basis points gross at forty percent turnover leaves "
            "nothing. <bookmark mark='c'/> And twice the speed means the same band, and twice the profit."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: a spread's speed; false passes in a screen; a band from the curve; a residual book "
            "after costs; the contrarian's cross term; a filter's errors; a reversal after costs; how long an IC and a "
            "Sharpe ratio take to prove; and the small-cost law. Then two qualifying-exam problems: the theorem from "
            "Dynkin's formula, and the frictionless limit with the cube-root law. Solutions, in English and Chinese, "
            "are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the firms that run these books: structure, capacity, culture", [34]),
            (r"what a trade really costs, and how to execute it", [37]),
            (r"market making: reversion at the shortest horizon", [38]),
            (r"the finale: every row, deflated", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part thirty-four goes inside the firms that run stat-arb books. Part thirty-seven "
            "measures what a trade really costs, the number this whole part depended on. Part thirty-eight is market "
            "making, reversion at the shortest horizon. And the finale deflates every row."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Vidyamurthy, \textit{Pairs Trading} (2004); Pole, \textit{Statistical Arbitrage} (2007); Chan, "
             r"\textit{Algorithmic Trading} (2013); Pedersen, \textit{Efficiently Inefficient} (2015); Leung and Li, "
             r"\textit{Optimal Mean Reversion Trading} (2016)"],
            [r"Engle and Granger (1987); Grossman and Miller (1988); Lehmann (1990); Lo and MacKinlay (1990); Johansen "
             r"(1991); Gatev, Goetzmann and Rouwenhorst (2006); Khandani and Lo (2007, 2011); Do and Faff (2010); "
             r"Avellaneda and Lee (2010); Bertram (2010); Nagel (2012); Krauss (2017)",
             r"Guijarro-Ordonez, Pelger and Zanotti (2021). Data: Kenneth French's daily industry and size portfolios; "
             r"Binance's daily bars; Cboe's VIX"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from Engle and Granger's cointegration in 1987 "
            "to deep statistical arbitrage in 2021. Every number on screen was computed by the House's code from Kenneth "
            "French's portfolios, Binance's bars and Cboe's VIX, with illustrations labelled as such."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("research", "portfolio"))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 34, Inside a Quant Firm", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House now runs a residual book: market-neutral, small, steady, and almost entirely a bet on its own "
            "trading costs. It knows that reversion is easy to find and expensive to keep, and that the band, not the "
            "model, decides which. <bookmark mark='a'/> Next, Part thirty-four: inside a quant firm. How the firms that "
            "run these books are organised, paid and governed, and why capacity, not cleverness, sets their size."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
