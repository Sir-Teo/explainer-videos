from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant33.common import BAD, FAC_C, GOOD, HURDLE, PART, RES_C, SPREAD_C, fit_right, load


class LeadLag(VoiceoverScene):
    def construct(self):
        l = load("lomac")
        self.card()
        self.contrarian()
        self.decomp()
        self.lead(l)
        self.bars(l)
        self.eras(l)
        self.bounce()
        self.horizons()
        self.reading()
        self.question()

    def card(self):
        c = chapter_card(7, r"Reversal and lead-lag", r"When a contrarian makes money, where does it come from?", part=PART)
        with self.voiceover("Chapter seven. Every stat-arb book is, underneath, a contrarian: it buys what fell and "
                            "sells what rose, relative to something. In 1990 Andrew Lo and Craig MacKinlay asked what "
                            "such a contrarian is really paid for."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def contrarian(self):
        rows = [cmath(r"w_{i,t}", r"=", r"-\tfrac1N\big(r_{i,t-1} - \bar r_{t-1}\big)", font_size=38, colors={r"w_{i,t}": RES_C}),
                cmath(r"\pi_t", r"=", r"\textstyle\sum_i w_{i,t}\, r_{i,t}", font_size=36),
                cmath(r"\text{Lehmann (1990)}", r":", r"\text{weekly losers beat weekly winners, in stocks}", font_size=30)]
        whys = [why(r"the contrarian of Part 31's August 2007, in its purest form: weight against last period's relative "
                    r"move"),
                why(r"its profit this period"),
                why(r"the reversal Lehmann found in weekly stock returns, and that every stat-arb book harvests in some "
                    r"form")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The contrarian, in its purest form. <bookmark mark='a'/> Weight each asset against its relative move last "
            "period. <bookmark mark='b'/> Its profit is the sum of weights times this period's returns. "
            "<bookmark mark='c'/> Bruce Lehmann found in 1990 that weekly losers beat weekly winners among stocks. The "
            "natural reading is overreaction: prices overshoot and come back. Lo and MacKinlay showed it is not the "
            "only reading."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def decomp(self):
        rows = [cmath(r"\mathbb E\,\pi_t", r"=", r"-\frac{N-1}{N^2}\operatorname{tr}\Gamma_1 + \frac{1}{N^2}\big(\iota^\top"
                      r"\Gamma_1\iota - \operatorname{tr}\Gamma_1\big) - \sigma^2(\mu)", font_size=30),
                cmath(r"-\frac{N-1}{N^2}\operatorname{tr}\Gamma_1", r":", r"\text{own reversal: a covariance term}", font_size=30,
                      colors={r"-\frac{N-1}{N^2}\operatorname{tr}\Gamma_1": RES_C}),
                cmath(r"\frac{1}{N^2}(\iota^\top\Gamma_1\iota - \operatorname{tr}\Gamma_1)", r":", r"\text{cross-autocovariance: "
                      r"lead-lag}", font_size=30, colors={r"\frac{1}{N^2}(\iota^\top\Gamma_1\iota - \operatorname{tr}\Gamma_1)": FAC_C}),
                cmath(r"\sigma^2(\mu)", r":", r"\text{the spread of mean returns, a cost}", font_size=30)]
        whys = [why(r"Lo and MacKinlay (1990): take expectations, with $\Gamma_1$ the first-order autocovariance matrix "
                    r"$\operatorname{Cov}(r_t, r_{t-1})$; an exact identity"),
                why(r"negative own autocorrelation (an asset reversing itself) pays the contrarian"),
                why(r"positive cross-autocorrelation (one asset's move predicting another's) also pays it, with no "
                    r"overreaction at all: slow diffusion of news"),
                why(r"assets with higher mean returns tend to be last period's winners: shorting them costs the spread of "
                    r"means")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Their decomposition is exact. <bookmark mark='a'/> The contrarian's expected profit is three terms in the autocovariance matrix of returns. <bookmark mark='b'/> The first is own reversal: assets that reverse their own moves. Overreaction is one possible explanation; microstructure and other dynamics can also generate it. <bookmark mark='c'/> The second is cross-autocovariance: one asset's move predicting another's next move. That cross term can pay even when own lag covariances vanish; slow news diffusion is one possible explanation, not identified by covariance alone. <bookmark mark='d'/> The third is a cost: the spread of mean returns."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def lead(self, l):
        ld = l["lead"]
        items = [(r"large caps previous block $\to$ small caps next block", ld["large_to_small"], FAC_C),
                 (r"small caps previous block $\to$ large caps next block", ld["small_to_large"], GREY_B),
                 (r"small caps $\to$ themselves", ld["small_own"], RES_C),
                 (r"large caps $\to$ themselves", ld["large_own"], GREY_B)]
        mx = max(abs(v) for _, v, _ in items)
        bars = VGroup()
        for j, (nm, v, col) in enumerate(items):
            r = Rectangle(width=max(abs(v) * 4.0 / mx, 0.03), height=0.5, fill_color=col, fill_opacity=0.85,
                          stroke_width=0).move_to([1.4, 1.6 - 0.95 * j, 0], aligned_edge=LEFT if v > 0 else RIGHT)
            bars.add(VGroup(label(nm, font_size=19, color=col).move_to([-3.2, 1.6 - 0.95 * j, 0]), r,
                            MathTex(f"{v:+.2f}", font_size=26).next_to(r, RIGHT if v > 0 else LEFT, buff=0.15)))
        axis = Line([1.4, 2.1, 0], [1.4, -1.6, 0], color=GREY_C, stroke_width=1.5)
        head = label(r"Who leads whom: five-observation correlations, size deciles, 1963--2020", font_size=26).to_edge(UP, buff=0.4)
        self.add(head, axis, bars[0])
        with self.voiceover(
            f"Lead-lag, measured on Kenneth French's size deciles, in consecutive blocks of five observations since 1963, rather than calendar weeks. <bookmark mark='a'/> The previous five-observation block return of the largest stocks predicts the next block return of the smallest, a correlation of {ld['large_to_small']:+.2f}. The reverse is {ld['small_to_large']:+.2f}. <bookmark mark='b'/> Small caps also predict themselves, {ld['small_own']:+.2f}: this is positive sample own autocorrelation. It describes continuation but does not alone identify adjustment speed or cause."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[:2]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[2:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def bars(self, l):
        rowsd = [(r"size deciles", l["size"]), (r"49 industries", l["industries"])]
        hx = [-3.8, -1.2, 1.4, 3.8]
        head = VGroup(label(r"5-day blocks, 1963--2020", font_size=17, color=GREY_B), label(r"own reversal", font_size=17,
                                                                                    color=RES_C),
                      label(r"lead-lag", font_size=17, color=FAC_C), label(r"plug-in / realised", font_size=17, color=GREY_B))
        tab = VGroup(head)
        for nm, r in rowsd:
            tab.add(VGroup(label(nm, font_size=20), MathTex(f"{1e4 * r['own']:+.2f}", font_size=26),
                           MathTex(f"{1e4 * r['cross']:+.2f}", font_size=26),
                           MathTex(rf"{1e4 * r['total']:+.2f}\ /\ {1e4 * r['realised']:+.2f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.2 - 0.9 * j, 0])
        foot = wrapped_label(r"basis points per five-observation block per unit of the contrarian's weights; the spread-of-means term is "
                             r"negligible here; five-observation blocks; plug-in and realized values can differ by boundary mean terms", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.7)
        sz = l["size"]
        self.add(tab[0], tab[1], foot)
        with self.voiceover(
            "The finite-sample comparison needs care. <bookmark mark='a'/> The displayed own and cross terms use lagged covariance products centered on the full-sample mean. The realized contrarian profit averages uncentered lagged return products. Their normalization and edge observations differ. <bookmark mark='b'/> The population expectation identity is exact under stationary moments, but these sample implementations need not agree to the last digit. The difference is a boundary mean term; the notes derive it. Similar-looking rounded numbers do not establish an exact software identity or a causal explanation."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(Indicate(VGroup(tab[1][3], tab[2][3]), color=WHITE, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    def eras(self, l):
        e = l["size_era"]
        hx = [-3.2, -0.6, 2.0, 4.6]
        head = VGroup(label(r"size deciles", font_size=17, color=GREY_B), label(r"own reversal", font_size=17, color=RES_C),
                      label(r"lead-lag", font_size=17, color=FAC_C), label(r"total", font_size=17, color=GREY_B))
        tab = VGroup(head)
        for k, r in e.items():
            tab.add(VGroup(label(k.replace("-", "--"), font_size=20), MathTex(f"{1e4 * r['own']:+.2f}", font_size=26),
                           MathTex(f"{1e4 * r['cross']:+.2f}", font_size=26), MathTex(f"{1e4 * r['total']:+.2f}",
                                                                                      font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.2 - 0.9 * j, 0])
        self.add(tab[0], tab[1])
        with self.voiceover(
            "The terms also change across eras. <bookmark mark='a'/> The pre-1991 sample and later sample show different covariance patterns, using five-observation return blocks whose first date assigns the era. <bookmark mark='b'/> Faster trading, liquidity, measurement and changing markets are possible explanations, but this before-and-after comparison cannot identify why the terms changed. A covariance decomposition describes second moments; it does not prove news diffusion, irrational overreaction, or that arbitrageurs removed a particular opportunity."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
        self.wait(0.4)
        self.clear_scene()

    def bounce(self):
        rows = [cmath(r"p_t", r"=", r"m_t + \tfrac{s}{2}\, q_t,\quad q_t = \pm 1", font_size=36),
                cmath(r"\operatorname{Cov}(\Delta p_t, \Delta p_{t-1})", r"=", r"-\tfrac{s^2}{4}", font_size=34,
                      colors={r"-\tfrac{s^2}{4}": BAD}),
                cmath(r"\text{nonsynchronous trading}", r"\Rightarrow", r"\text{spurious cross-autocorrelation}", font_size=30)]
        whys = [why(r"Roll (1984): a trade prints at the bid or the ask around the efficient price $m_t$, at random"),
                why(r"so recorded price changes are negatively autocorrelated even when $m_t$ is a random walk: reversal "
                    r"that no one can trade, because it is the spread itself"),
                why(r"and small stocks that trade late carry yesterday's news into today's prices: lead-lag that is partly "
                    r"a measurement effect (Lo and MacKinlay 1990)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Two warnings about measured reversal. <bookmark mark='a'/> Richard Roll's model: trades print at the bid or "
            "at the ask, at random, around an efficient price. <bookmark mark='b'/> So recorded price changes are "
            "negatively autocorrelated even when the efficient price is a random walk. That reversal cannot be traded: "
            "it is the bid-ask spread itself. Bruce Lehmann's weekly contrarian profits on stocks were partly this. "
            "<bookmark mark='c'/> And stocks that trade late carry yesterday's news into today's closing prices, which "
            "makes lead-lag appear even where no one could act on it. Portfolios and residuals reduce both effects; "
            "they do not remove them."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def horizons(self):
        rows = [cmath(r"\text{days to a month}", r":", r"\text{stocks reverse}", font_size=34,
                      colors={r"\text{stocks reverse}": RES_C}),
                cmath(r"\text{3 to 12 months}", r":", r"\text{industries continue}", font_size=34,
                      colors={r"\text{industries continue}": BAD}),
                cmath(r"\text{3 to 5 years}", r":", r"\text{both reverse again}", font_size=34)]
        whys = [why(r"Jegadeesh (1990), Lehmann (1990): the short-term reversal of single stocks, partly the bid-ask "
                    r"bounce and partly the price of immediacy"),
                why(r"Moskowitz and Grinblatt (1999): industries that did well over the past months keep doing well, and "
                    r"industry momentum explains much of stock momentum"),
                why(r"De Bondt and Thaler (1985): long-horizon reversal; the sign of the bet depends on the horizon and "
                    r"on the unit traded")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why the unit and the horizon matter. <bookmark mark='a'/> Over days to a month, single stocks reverse: "
            "Narasimhan Jegadeesh and Bruce Lehmann. <bookmark mark='b'/> Over three to twelve months, industries "
            "continue: Tobias Moskowitz and Mark Grinblatt found industry momentum, and that it explains much of stock "
            "momentum. That is why the industry contrarian of Chapter nine loses. <bookmark mark='c'/> And over three to "
            "five years both reverse again, Werner De Bondt and Richard Thaler's long-horizon reversal. Reversion is a "
            "statement about a unit and a horizon, never about prices in general."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def reading(self):
        cards = VGroup(
            desk_question(r"two moment terms, one book", r"own and cross-autocovariance can contribute to expected contrarian profit; "
                          r"their economic mechanisms require additional evidence", width=12.4, font_size=19),
            desk_question(r"residuals change the covariance structure", r"removing fitted factors changes common dependence; "
                          r"it does not necessarily isolate own reversal, and fitted endpoint constraints matter", width=12.4, font_size=19),
            desk_question(r"lead-lag lives on", r"in pairs like a stock and its supplier, an index and its futures, or a "
                          r"coin on two exchanges: wherever news arrives in one place first", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Read the decomposition as an accounting of population moments. <bookmark mark='a'/> Own reversal and cross-autocovariance can both contribute, with different signs across assets and horizons. Their labels do not identify mechanisms. <bookmark mark='b'/> Removing fitted factors changes these moments but need not isolate pure own reversal; residual construction and omitted common dynamics still matter. <bookmark mark='c'/> Cross-market lead-lag is a candidate hypothesis where prices incorporate information at different speeds. Implementability requires observation timing, executable quotes and net costs, not correlation alone."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"every asset follows a random walk, but large caps' returns predict small caps' next week. Does a "
                       r"contrarian make or lose money?")
        working = MathTex('E[\\pi_t]=-\\frac{\\operatorname{tr}\\Gamma}{N}+\\frac{\\iota^\\top\\Gamma\\iota}{N^2}-\\sigma^2(\\mu)', font_size=32).move_to(UP * 0.8)
        if working.width > 12.1:
            working.scale_to_fit_width(12.1)
        setup_note = wrapped_label('Choose zero means, zero own lag covariances and positive off-diagonal covariance. Determine the sign before discussing execution costs.', 11.7, 23).move_to(DOWN * 0.9)
        self.add(working, setup_note, q)
        with self.voiceover(
            "Pause and predict. Every asset on its own follows a random walk, but large caps' returns predict small "
            "caps' returns a week later. Does the contrarian make money or lose it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
