from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import (BAD, COIN, COMPLEX, GOOD, HURDLE, LINEAR, MOM, NET, OOS_C, PART, TREE, comma,
                                         load)

DESK = [
    (r"500 stocks, an out-of-sample $R^2$ of 0.5\% a month. What long-short Sharpe ratio could you hope for?",
     r"$\sqrt{R^2/(1 - R^2)}\cdot\sqrt{N}\cdot\sqrt{12} \approx 0.071 \times 22.4 \times 3.46 \approx 5.5$ if the "
     r"errors were independent; common factors cut the independent bets to a few dozen, and costs and uneven $R^2$ "
     r"cut the rest: 1--2 is a good outcome"),
    (r"Your network has a million parameters and 10{,}000 observations, and fits its training set exactly. Useless?",
     r"not by that fact: past the threshold the minimum-norm fit's variance falls like $\sigma^2/(\gamma - 1)$. Ask "
     r"for the ridge path, the out-of-sample risk and the baseline at the same budget"),
    (r"A model calls tomorrow's direction right 55\% of the time. Is it tradable?",
     r"accuracy is the wrong yardstick: the base rate, the sizes of the moves it gets right and wrong, its "
     r"correlation with what you already hold, and turnover against costs decide"),
    (r"Two years of weekly tests on 40 coins: Sharpe ratio 1.0. A 95\% interval?",
     r"the standard error is $\sqrt{(1 + 0.5)/2} \approx 0.87$, so roughly $-0.7$ to $2.7$; telling 1 from 0.5 at two "
     r"standard errors needs $T \approx 4 \times 1.5/0.25 = 24$ years, or many more independent coins"),
    (r"A meta-model doubles your precision but takes one bet in ten. Better?",
     r"compare expected profit per unit of risk, not precision: ten times fewer bets of twice the hit rate is better "
     r"only if the kept bets' mean over standard deviation beats the full set's, net of costs; test it out of sample"),
    (r"A conformal interval covered 90\% in the 2010s and 70\% in 2020. Broken?",
     r"no: its guarantee assumes exchangeability, which a regime change breaks. Use adaptive conformal inference, "
     r"which pins long-run coverage under any drift, or recalibrate on a rolling window"),
]

PROBLEMS = [
    r"(qual) Split conformal: show $\Pr(y \in C(x)) \ge 1 - \alpha$ under exchangeability, and $\le 1 - \alpha + "
    r"\tfrac{1}{n+1}$ without ties.",
    r"(qual) OLS with Gaussian $X$, $P < N - 1$: show $\mathbb E|\hat b - b|^2 = \sigma^2 P/(N - P - 1)$ (inverse "
    r"Wishart) and take the limit $P/N \to \gamma$.",
    r"Show that ridge tends to the minimum-norm interpolator $X^{+}y$ as $\lambda \downarrow 0$ when $P > N$.",
    r"Random features: for $w \sim N(0, \gamma^2 I)$ show $\mathbb E\cos(w^{\top}\Delta) = e^{-\gamma^2|\Delta|^2/2}$.",
    r"Adaptive conformal: show $\big|\tfrac1T\sum_t \mathrm{err}_t - \alpha\big| \le \tfrac{\max(\alpha_1, 1 - "
    r"\alpha_1) + \gamma}{\gamma T}$.",
    r"Show by Sherman--Morrison that $E[(1 - w^{\top}R)R] = 0$ gives $w \propto \Sigma^{-1}\mu$; state the "
    r"Hansen--Jagannathan bound.",
    r"Brownian motion with drift $\mu$, volatility $\sigma$, barriers $\pm b$ and no time limit: the probability of "
    r"hitting $+b$ first.",
    r"Fractional differencing: from $w_k = -w_{k-1}(d - k + 1)/k$, show $w_k \sim k^{-d-1}/\Gamma(-d)$.",
    r"Labels of horizon $h$ on every day: show the average uniqueness is about $1/h$ in the interior, and compare "
    r"with the 0.115 of Chapter 12 ($h = 10$).",
    r"Prove that one attention layer without positional encoding is permutation equivariant.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("zoo"), load("theory"), load("autoenc"), load("sdf"), load("images"), load("pretrained"),
                   load("conformal"), load("toolkit"), load("envelope"), load("kmz"), load("snr"))
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

    def recap(self, z, t, a, s, im, p, c, tk, e, k, snr):
        r2s = [z["rows"][m]["r2"] for m in z["models"]]
        items = [
            (r"a low signal-to-noise world: an $R^2$ of 1\% times many independent bets is a large Sharpe ratio", MOM),
            (rf"the zoo on coins: every $R^2$ from {100 * min(r2s):.1f}\% to {100 * max(r2s):.1f}\%; two years cannot "
             r"rank it", BAD),
            (r"what edge there is lives in the less liquid half, and costs of 5--14\% a year at the fee alone", COIN),
            (r"the virtue of complexity: a third at $P/T = 1{,}000$, below simply holding the market", COMPLEX),
            (r"the critics: the limit is a kernel smoother, a volatility-timed momentum", HURDLE),
            (rf"the theorem: exact ridge(less) risk, simulation on the line; misspecification makes size pay "
             rf"($R^2$ {100 * (1 - t['mis']['ridgeless'][-1] / t['mis']['null']):.0f}\%)", COMPLEX),
            (r"the autoencoder: one factor explains 45\%, the premia had the wrong sign", LINEAR),
        ]
        items2 = [
            (rf"the adversarial SDF learned to short the market (correlation {s['corr_mkt_adv']:.2f})", NET),
            (r"attention learned the average coin; it fitted the training weeks", NET),
            (rf"chart images: {comma(im['n_train'])} are too few; momentum {im['sr_mom']:.1f}, the CNN "
             rf"{im['sr_cnn']:.1f}", TREE),
            (r"a pocket foundation model transfers volatility's shape, not a better forecast than EWMA", OOS_C),
            (r"the toolkit: activity clocks tame tails; meta-labels shrink, not improve; overlap divides $n$ by nine",
             TREE),
            (rf"conformal: {100 * c['0.1']['cover']:.1f}\% on average, {100 * c['btc']['cover_aci']:.1f}\% adaptive "
             r"through the storms", GOOD),
            (rf"the envelope: NN3 on coins {e['nn3']['row']['holdout']['sharpe']:.2f}, the timer "
             rf"{e['kmz']['row']['holdout']['sharpe']:.2f}; the counter {comma(e['trials'])}", QC.HOUSE),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 27 in fourteen lines")
        with self.voiceover(
            "Part twenty-seven in fourteen lines. Returns are a world of tiny signals in loud noise, and a forecast "
            "that explains one percent of each asset's return is worth a great deal across many independent assets. "
            "On two years of coins the whole zoo forecast worse than zero, and the test had too little power to rank "
            "it. What edge there was lived in the less liquid coins, and costs took much of it. The virtue of "
            "complexity is real in the data, but below the market's own Sharpe ratio, and its critics showed what its "
            "limit is. The theorem behind both is exact, and it says when size pays: when the truth is complex. The "
            "autoencoder explained half of the coins' variance and still forecast with the wrong sign."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 27 in fourteen lines")
        with self.voiceover(
            "The adversarial discount factor learned to short a falling market. Attention learned the average coin. "
            "The chart network had too few pictures. A small foundation model carried volatility's shape from coins to "
            "stocks, but not past a rule fitted to the stock itself. The practitioner's tools each did one honest "
            "thing, and none was free. Conformal intervals kept their promise on average, and the adaptive version "
            "kept it through the storms. And on the sealed years the coin network earned one point three while the "
            "timer lost a little, with the counter past ten thousand four hundred."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q, a_, width=12.4, font_size=20) for q, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. Five hundred stocks at half a percent of R squared: about five and a half if the "
            "errors were independent, and one or two in practice, because common factors leave only a few dozen "
            "independent bets. <bookmark mark='a'/> A network that fits its training set exactly is not thereby "
            "useless; ask for the ridge path and the out-of-sample risk. <bookmark mark='b'/> And fifty-five percent "
            "directional accuracy says little until you know the sizes, the base rate, the correlation and the costs."
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
            "A Sharpe ratio of one from two years of forty coins could be anything from minus point seven to two "
            "point seven. <bookmark mark='a'/> A meta-model that doubles precision on a tenth of the bets wins only "
            "if the kept bets earn more per unit of risk, after costs. <bookmark mark='b'/> And a conformal interval "
            "that covers seventy percent in a new regime is not broken; its assumption is. Full solutions are in the "
            "notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "And ten problems, the first two at the level of a qualifying exam: split conformal's coverage from both "
            "sides; the exact risk of least squares from the inverse Wishart; ridge's limit as the minimum-norm "
            "interpolator; random features and Bochner's theorem; adaptive conformal's long-run coverage; the SDF as "
            "the tangency portfolio; the triple barrier's first passage; the decay of fractional-differencing "
            "weights; label uniqueness; and the equivariance of attention. Solutions, in English and Chinese, are in "
            "the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"text and language models: the same validation, and a new look-ahead bias", [28]),
            (r"alpha miners: the zoo, automated, against the counter", [29]),
            (r"Marchenko--Pastur again: cleaning covariance matrices for portfolios", [30]),
            (r"costs, capacity and the fundamental law of breadth", [31]),
            (r"model risk as a firm's problem: who may change a model", [34]),
            (r"the finale: the coin network's row, deflated by the full count", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part twenty-eight turns these models on text, with a new kind of look-ahead. Part "
            "twenty-nine automates the zoo into alpha miners, against the counter. Part thirty meets the "
            "Marchenko-Pastur law again, cleaning the covariance matrices of portfolios. Part thirty-one prices "
            "breadth, costs and capacity. Part thirty-four makes model risk a firm's problem. And the finale deflates "
            "the coin network's row with everything else."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Kelly and Xiu, \textit{Financial Machine Learning} (2023); Lopez de Prado, \textit{Advances in Financial "
             r"Machine Learning}, ch.\ 2--5, 10; Hastie, Tibshirani and Friedman, \textit{The Elements of Statistical "
             r"Learning}; Goodfellow, Bengio and Courville, \textit{Deep Learning}; Isichenko, \textit{Quantitative "
             r"Portfolio Management}, ch.\ 2"],
            [r"Marchenko and Pastur (1967); Grinold (1989); Vovk, Gammerman and Shafer (2005); Rahimi and Recht (2007); "
             r"Welch and Goyal (2008); Zaheer et al.\ (2017); Dobriban and Wager (2018); Lei et al.\ (2018); Belkin, Hsu, "
             r"Ma and Mandal (2019); Kelly, Pruitt and Su (2019); Bartlett, Long, Lugosi and Tsigler (2020); Gu, Kelly "
             r"and Xiu (2020, 2021); Israel, Kelly and Moskowitz (2020)",
             r"Gibbs and Cand\`es (2021); Giannone, Lenza and Primiceri (2021); Hastie, Montanari, Rosset and Tibshirani "
             r"(2022); Leippold, Wang and Zhou (2022); Mei and Montanari (2022); Avramov, Cheng and Metzker (2023); "
             r"Jiang, Kelly and Xiu (2023); Chen, Pelger and Zhu (2024); Kelly, Malamud and Zhou (2024); Ansari et al.\ "
             r"(2024); Das et al.\ (2024); Nagel (2025); Kelly, Kuznetsov, Malamud and Xu (2025); Shi et al.\ (2025). "
             r"Data: Binance public archive; Amit Goyal; Yahoo Finance"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from Marchenko and Pastur in 1967 to the "
            "first foundation models of markets in 2025. Every number on screen was computed by the House's code from "
            "public data, with simulations labelled as such."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("research",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 28, Text, LLMs and Alternative Data", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House now has a model shop: every learner from least squares to a transformer, the theory that says "
            "when size helps, and the discipline that says when to believe it. It has learned that the hardest part "
            "of machine learning for returns is not the model but the test. <bookmark mark='a'/> Next, Part "
            "twenty-eight: text, language models and alternative data. Models that read the news and the Fed, and the "
            "subtle ways in which a model trained on the internet already knows how the story ends."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
