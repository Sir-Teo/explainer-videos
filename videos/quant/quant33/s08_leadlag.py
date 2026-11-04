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
                cmath(r"-\frac{N-1}{N^2}\operatorname{tr}\Gamma_1", r":", r"\text{own reversal: overreaction}", font_size=30,
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
            "Their decomposition is exact. <bookmark mark='a'/> The contrarian's expected profit is three terms in the "
            "autocovariance matrix of returns. <bookmark mark='b'/> The first is own reversal: assets that reverse "
            "their own moves. That is overreaction. <bookmark mark='c'/> The second is cross-autocovariance: one asset's "
            "move predicting another's next move. That pays the contrarian too, with no overreaction at all, just news "
            "that travels slowly. <bookmark mark='d'/> The third is a cost: the spread of mean returns."
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
        items = [(r"large caps last week $\to$ small caps this week", ld["large_to_small"], FAC_C),
                 (r"small caps last week $\to$ large caps this week", ld["small_to_large"], GREY_B),
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
        head = label(r"Who leads whom: weekly correlations, size deciles, 1963--2020", font_size=26).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Lead-lag, measured on Kenneth French's size deciles, week by week since 1963. <bookmark mark='a'/> Last "
            f"week's return of the largest stocks predicts this week's return of the smallest, a correlation of "
            f"{ld['large_to_small']:+.2f}. The reverse is {ld['small_to_large']:+.2f}. <bookmark mark='b'/> Small caps "
            f"also predict themselves, {ld['small_own']:+.2f}: they adjust slowly, which is positive own "
            "autocorrelation, the opposite of overreaction. Large caps lead; small caps follow."
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
        head = VGroup(label(r"weekly, 1963--2020", font_size=17, color=GREY_B), label(r"own reversal", font_size=17,
                                                                                    color=RES_C),
                      label(r"lead-lag", font_size=17, color=FAC_C), label(r"total = realised", font_size=17, color=GREY_B))
        tab = VGroup(head)
        for nm, r in rowsd:
            tab.add(VGroup(label(nm, font_size=20), MathTex(f"{1e4 * r['own']:+.2f}", font_size=26),
                           MathTex(f"{1e4 * r['cross']:+.2f}", font_size=26),
                           MathTex(rf"{1e4 * r['total']:+.2f} = {1e4 * r['realised']:+.2f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.2 - 0.9 * j, 0])
        foot = wrapped_label(r"basis points a week per unit of the contrarian's weights; the spread-of-means term is "
                             r"negligible here; the decomposition and the realised profit agree exactly", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.7)
        sz = l["size"]
        with self.voiceover(
            "The decomposition, computed. <bookmark mark='a'/> For the size deciles, own autocorrelation costs the "
            "contrarian, because small caps continue rather than reverse, and the lead-lag pays it almost exactly as "
            "much: the total is nearly zero. For the industries, the lead-lag term is the larger, and the total is "
            "slightly positive. <bookmark mark='b'/> In both, the identity holds to the last digit: the decomposition "
            "and the realised profit are the same number."
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
        with self.voiceover(
            "And the pattern did not last. <bookmark mark='a'/> Before 1990, small caps followed large caps strongly: "
            "large own continuation, large lead-lag. <bookmark mark='b'/> Since 1991 both terms shrank and changed "
            "sign: small stocks now reverse slightly and no longer lag. Faster markets, cheaper trading, and many "
            "arbitrageurs trading exactly this lag removed it. A source of stat-arb profit, measured, and then gone."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
        self.wait(0.4)
        self.clear_scene()

    def reading(self):
        cards = VGroup(
            desk_question(r"two sources, one book", r"a contrarian is paid by overreaction and by slow diffusion of news; "
                          r"they have different risks, and they decay at different speeds", width=12.4, font_size=19),
            desk_question(r"residuals isolate the first", r"removing factors removes the common component, and with it "
                          r"most of the lead-lag: what is left is each asset's own reversal", width=12.4, font_size=19),
            desk_question(r"lead-lag lives on", r"in pairs like a stock and its supplier, an index and its futures, or a "
                          r"coin on two exchanges: wherever news arrives in one place first", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What this means for a stat-arb book. <bookmark mark='a'/> A contrarian is paid by two different things, "
            "overreaction and slowly travelling news, with different risks. <bookmark mark='b'/> A factor model removes "
            "the common component, and with it most of the lead-lag; what is left is each asset's own reversal. "
            "<bookmark mark='c'/> Lead-lag survives where news reaches one market before another: a stock and its "
            "supplier, an index and its futures, a coin on two exchanges."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"every asset follows a random walk, but large caps' returns predict small caps' next week. Does a "
                       r"contrarian make or lose money?")
        with self.voiceover(
            "Pause and predict. Every asset on its own follows a random walk, but large caps' returns predict small "
            "caps' returns a week later. Does the contrarian make money or lose it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
