from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, DEBT, EQUITY, GBMC, HAZ, PART, RISKY, SENIOR, load

DESK = [
    (r"A 5-year CDS trades at 100 bp, recovery 40\%. Annual default probability?",
     r"the credit triangle: $\lambda \approx s/(1 - R) = 0.01/0.6 = 1.67\%$ a year, so about $1 - e^{-5\lambda} = 8\%$ "
     r"over five years. Risk-neutral, not real-world: it includes the risk premium"),
    (r"Why are equity holders long volatility and bondholders short it?",
     r"equity is a call on the assets (Merton): more volatility raises the call's value at the bondholders' expense, "
     r"who are short the put. The asset-substitution problem: covenants exist to limit it"),
    (r"Why can a senior tranche with a tiny expected loss deserve a wide spread?",
     r"its losses arrive only in the worst states of the economy, when money is worth most: an economic catastrophe "
     r"bond (Coval, Jurek and Stafford). A rating on expected loss alone misses when the loss arrives"),
    (r"A default model scores 0.98 in sample and 0.90 out of sample. Which do you report?",
     r"the out-of-sample one, on data sealed before the model was fitted; the gap is what the model memorised. And "
     r"check calibration separately: ranking survives the cycle, probabilities do not"),
]

PROBLEMS = [
    r"In Merton's model show that the debt is worth $De^{-rT}N(d_2) + V_0N(-d_1)$, and derive the credit spread.",
    r"Show that equity volatility is $\sigma_E = N(d_1)\,\sigma_V V/E$. Why does it rise as the firm approaches default?",
    r"With a constant hazard $\lambda$, show that a CDS's par spread is $(1 - R)\lambda$ when premiums are paid "
    r"continuously.",
    r"A 3-year CDS trades at 120 bp, recovery 40\%, rates 4\%, annual premiums. Bootstrap a flat hazard rate by hand "
    r"(one iteration of the credit triangle is enough).",
    r"Derive Vasicek's large-pool distribution $\mathbb{P}(L \le x)$ from the one-factor model, and its 99.9\% quantile.",
    r"Compute the Basel capital $K$ for PD 2\%, LGD 45\%, $M$ = 2.5. Compare it with the expected loss.",
    r"Show that an equity tranche's expected loss falls, and a senior tranche's rises, with the copula correlation.",
    r"A logit's coefficient on leverage is 0.5 per standard deviation. By what factor does a two-standard-deviation "
    r"rise in leverage multiply the odds of default?",    r"(qual) For $N$ equal loans in Vasicek's model, show $\Pr(L \le k/N) = \int \operatorname{Bin}(k; N, p(y))\varphi(y)dy$ "
    r"and that the $\alpha$-quantile of $L$ tends to $p(\Phi^{-1}(\alpha))$ as $N \to \infty$.",
    r"(qual) For $L = \mu(Y) + \varepsilon U$ with $\mathbb E[U \mid Y] = 0$, derive the second-order expansion "
    r"$q_\alpha(L) = q_\alpha(\mu) - \frac{\varepsilon^2}{2h(y)}\frac{d}{dy}\big[h(y)\operatorname{Var}(U \mid y)/\mu'(y)\big] + "
    r"o(\varepsilon^2)$ at $y = q_\alpha(Y)$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("spreads"), load("kmv"), load("defaults"), load("models"), load("vasicek"), load("copula"),
                   load("cjs"), load("march2020"), load("bdc"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, s, k, d, m, v, c, j, q, b):
        h = m["results"]["holdout"]["auc"]
        items = [
            (rf"Lehman's swaps settled at 8.625 cents; the Baa spread reached {s['max']['v']:.2f}\% in December 2008",
             BAD),
            (r"a spread pays for expected loss, a premium for bad times, and illiquidity", RISKY),
            (r"Merton: equity is a call on the assets; spreads from leverage and volatility; short spreads go to zero",
             EQUITY),
            (rf"distance to default every day: Norwegian Cruise Line fell to {k['NCLH']['worst']['dtd']:.2f} in 2020",
             DEBT),
            (r"first passage and Leland's chosen barrier; default as a random clock; survival as discounting", HAZ),
            (r"the CDS: two legs, a bootstrapped hazard curve, the Big Bang's coupons and upfronts", RISKY),
            (rf"{d['total']} bankruptcy filings, 2009--2025, moving with the spread ($\rho$ = {d['corr']:.2f})", BAD),
            (rf"sealed 2021--23 AUC: Altman {h['altman']:.2f}, logit {h['logit']:.2f}, trees {h['gbm']:.2f}; counter "
             rf"{m['trials']}", GBMC),
            (rf"Vasicek's pool and Basel: a 1\% PD carries a {100 * v['rw_1pct']:.2f}\% risk weight", SENIOR),
            (rf"copulas: the $t$ makes a 15\% pool loss {c['tail']['t'] / max(c['tail']['gauss'], 1e-9):.0f} times "
             r"likelier; tranches are positions in correlation", RISKY),
            (rf"a senior tranche loses only in the worst {100 * j['threshold_pct']:.2f}\% of states: a catastrophe bond",
             SENIOR),
            (r"the London Whale: a hedge that became a \$6.2 bn position, and a VaR model wrong by construction", BAD),
            (rf"March 2020: bond ETFs fell {abs(100 * q['HYG']['drawdown']):.0f}\%; private credit's marks barely "
             r"moved", DEBT),
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
            "Part twenty in thirteen lines. A promise is worth what its maker can pay: Lehman's paid eight and five "
            "eighths cents. A spread pays for expected losses, for when they arrive, and for illiquidity. Merton made "
            "equity a call on the assets, and his distance to default tracked three companies through the pandemic, "
            "day by day. Barriers bring default forward, and Leland let the firm choose. Reduced-form models make "
            "default a random clock and survival a discount factor, and the credit default swap is priced and "
            "bootstrapped from them. Seventeen years of bankruptcy filings rise and fall with the spread. Accounts "
            "predict bankruptcy, Altman's ratios well and boosted trees better, on years sealed in advance. Vasicek's "
            "pool sets bank capital. Copulas decide the tail, and tranches are positions in correlation; a senior "
            "tranche is a bet against catastrophe. A hedge became the London Whale. And in March 2020, the prices of "
            "bond funds fell while the marks of private loans barely moved."
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
            "Four desk questions. A five-year swap at one hundred basis points with forty percent recovery: about one "
            "point seven percent a year, by the credit triangle, and that is a risk-neutral rate. "
            "<bookmark mark='a'/> Shareholders are long volatility because they own a call on the assets, and "
            "bondholders are short it because they sold the put. <bookmark mark='b'/> A senior tranche with a tiny "
            "expected loss deserves a wide spread because its losses arrive only in catastrophes. "
            "<bookmark mark='c'/> And a default model is reported out of sample, on data sealed before it was fitted, "
            "with its calibration checked separately. Full solutions are in the notes."
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
            (r"counterparty risk: CVA is a CDS on the counterparty, written on an exposure", [21]),
            (r"the distress puzzle and credit factors among the anomalies", [25]),
            (r"backtests that respect point-in-time accounts, as this part's dataset did", [26]),
            (r"machine learning on firm characteristics, at scale", [27]),
            (r"the finale: the House's credit book under a copula with fat tails", [43]),
        ])
        with self.voiceover(
            "Where this comes back. In Part twenty-one, the value of a counterparty's default on a derivative, CVA, "
            "is a credit default swap written on an exposure. Part twenty-five returns to the distress puzzle among "
            "the anomalies. Parts twenty-six and twenty-seven build on this part's discipline: point-in-time accounts, "
            "sealed tests, and machine learning on firm characteristics. And the finale stress-tests the House's "
            "credit book with fat tails."
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
            "The textbooks this part follows, and the papers and public records it draws on, from Altman's ratios in "
            "1968 to the Federal Reserve's corporate credit facilities. Every number on screen was computed from public "
            "data: Moody's yields on FRED, the companies' own filings on EDGAR, and market prices."
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
