from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant42.common import ladder
from videos.quant.quant42.common import (BAD, COLL_C, COMP_C, GOOD, HURDLE, LEARN_C, PART, REAL_C, SHARE_C, SIM_C,
                                         fit_right, load)


class Crowd(VoiceoverScene):
    def construct(self):
        c = load("crowd")
        self.card(c)
        self.gensler()
        self.lemma()
        self.chart(c)
        self.error(c)
        self.measure()
        self.public_good()
        self.question()

    def card(self, c):
        r = [x for x in c["rows"] if x["share"] == 0.2][0]
        ch = chapter_card(7, r"When everyone shares a model", r"How much does a little common input matter?", part=PART)
        with self.voiceover(
            f"""Chapter seven. Under the pause's independent unit-variance signal assumptions, the common component accounts for {100*r['common']:.0f} percent of aggregate flow variance. Point two is a signal coefficient, not a realised fraction of every trade. Private components partly diversify rather than cancelling exactly. This arithmetic illustrates one common-input mechanism; sharing a model does not by itself establish these assumptions in a real market."""
        ):
            self.play(FadeIn(ch[0], shift=UP * 0.2), FadeIn(ch[1]))
        self.play(FadeOut(ch))

    def gensler(self):
        cards = VGroup(
            desk_question(r"Gensler and Bailey (2020)", r"deep learning could raise systemic risk through model "
                          r"uniformity: firms using similar models, trained on similar data, from few providers",
                          width=12.4, font_size=19),
            desk_question(r"Danielsson, Macrae and Uthemann (2022)", r"AI makes risk management more procyclical "
                          r"when every risk engine learns the same lesson from the same crisis", width=12.4, font_size=19),
            desk_question(r"the mechanism", r"not a bad model: the same model, everywhere, so that one error is "
                          r"everyone's error at once", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The concern, stated before the language-model boom. <bookmark mark='a'/> Gary Gensler and Lily Bailey "
            "argued in twenty twenty that deep learning could raise systemic risk through uniformity: similar models, "
            "trained on similar data, bought from few providers. <bookmark mark='b'/> Jon Danielsson, Robert Macrae "
            "and Andreas Uthemann argued that risk engines that learn the same lessons make risk management more "
            "procyclical. <bookmark mark='c'/> The mechanism is not a bad model. It is the same model everywhere, so "
            "that one error is everyone's error at once."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lemma(self):
        rows = [cmath(r"x_i", r"=", r"w\,s + (1 - w)\,e_i", font_size=42, colors={r"x_i": SHARE_C}),
                cmath(r"\text{Var}\Bigl(\sum_i x_i\Bigr)", r"=", r"N^2 w^2 + N(1 - w)^2", font_size=40),
                cmath(r"\text{common share}", r"=", r"\frac{N w^2}{N w^2 + (1 - w)^2}", font_size=40,
                      colors={r"\text{common share}": BAD}),
                cmath(r"w = 0.2,\ N = 100", r"\Rightarrow", r"\frac{4}{4.64} = 86\%", font_size=40)]
        whys = [why('signal components $s,e_1,\\ldots,e_N$ are independent, zero mean and unit variance; the resulting orders are correlated'),
                why(r"the shared parts add up coherently, $(Nw)^2$; the private parts add up as a random walk, $N(1-w)^2$"),
                why(r"so the shared part's share of the variance grows with $N$ for any $w > 0$"),
                why('a common coefficient of 0.2 gives 86\\% of aggregate variance at $N=100$, under these signal assumptions')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The arithmetic. <bookmark mark='a'/> The common signal and all private components are independent with zero means and unit variances. Orders themselves are correlated. <bookmark mark='b'/> Summed flow has common variance N squared w squared and private variance N times the square of one minus w. <bookmark mark='c'/> Their ratio gives the common fraction. At fixed positive w it increases with N. <bookmark mark='d'/> For w point two and N one hundred, it is four over four point six four, about eighty-six percent. This is a variance fraction, not a share of realised order volume."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def chart(self, c):
        rows = c["rows"]
        w = np.array([x["share"] for x in rows])
        vr = np.array([x["vol_ratio"] for x in rows])
        cm = np.array([x["common"] for x in rows])
        th = np.sqrt([x["flow_var_th"] / rows[0]["flow_var_th"] for x in rows])
        g = axes([0, 1], [0, 11], x_length=7.4, y_length=4.2, xlabel=r"weight on the shared model, $w$",
                 ylabel=r"volatility, relative to $w = 0$", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 5, 10],
                 font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        ln = curve(ax, w, th, GREY_B, stroke_width=2)
        dots = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.07, color=SHARE_C) for a_, b_ in zip(w, vr)])
        labs = VGroup(*[label(rf"{100 * cm_:.0f}\%", font_size=14, color=BAD).next_to(ax.c2p(a_, b_), UP, buff=0.1)
                        for a_, b_, cm_ in zip(w, vr, cm) if a_ in (0.05, 0.1, 0.2, 0.5)])
        leg = legend([(SHARE_C, r"simulated, 100 traders"), (GREY_B, r"the formula")], font_size=17)
        note_ = label('labels: theoretical common variance fraction', font_size=15, color=BAD)
        side = VGroup(leg, note_).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        r2 = [x for x in rows if x["share"] == 0.2][0]
        with self.voiceover(
            f"""A hundred traders with linear price impact. <bookmark mark='a'/> At common coefficient point two, simulated volatility is {r2['vol_ratio']:.1f} times the zero-common benchmark. <bookmark mark='b'/> The theoretical curve uses unmodified unit-variance signals; the five-thousand-observation simulation includes one inserted shock, so its dots need not equal that curve. Total variance initially falls to its minimum at w equal to one over N plus one, then rises. <bookmark mark='c'/> Labels show theoretical common variance fractions, not the fraction of everything the market trades or a measured AI contribution."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(side), LaggedStart(*[FadeIn(d_, scale=1.4) for d_ in dots], lag_ratio=0.2), run_time=2)
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
            vo.wait_until("b")
            self.play(Create(ln), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(labs))
        self.wait(0.4)
        self.clear_scene()

    def error(self, c):
        rows = [x for x in c["rows"] if x["share"] in (0.0, 0.05, 0.1, 0.2, 0.5, 1.0)]
        mx = max(x["shock_sd"] for x in rows) * 1.1
        bars = VGroup()
        for i, x in enumerate(rows):
            h = 4.0 * abs(x["shock_sd"]) / mx
            b = Rectangle(width=0.9, height=max(h, 0.02), stroke_width=0, fill_color=BAD if x["share"] else COMP_C,
                          fill_opacity=0.85)
            b.move_to([-4.5 + 1.8 * i, -2.0 + h / 2, 0])
            t1 = label(rf"$w = {x['share']:g}$", font_size=17, color=GREY_A).next_to(b, DOWN, buff=0.15)
            t1.set_y(-2.35)
            t2 = label(rf"{x['shock_sd']:.0f}", font_size=17, color=WHITE).next_to(b, UP, buff=0.1)
            bars.add(VGroup(b, t1, t2))
        head = label('one selected day: +4 added to the existing common signal; total return in baseline volatility units',
                     font_size=20).to_edge(UP, buff=0.6)
        r2 = [x for x in rows if x["share"] == 0.2][0]
        with self.voiceover(
            f"""One deliberately inserted shock. The source adds positive four to the existing random common signal on the selected day. <bookmark mark='a'/> At zero common weight, that addition has no effect, but private orders still generate a return. <bookmark mark='b'/> At weight point two, the selected day's total return is {r2['shock_sd']:.0f} baseline volatility units. That includes the original random signals; the inserted addition alone contributes eight units. This upward realisation illustrates amplification, not a downward crash, a four-sigma total draw or a frequency estimate."""
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars[0]))
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.2) for b_ in bars[1:]], lag_ratio=0.3), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def measure(self):
        rows = [cmath(r"F_t", r"=", r"B\,f_t + u_t", font_size=42, colors={r"F_t": SHARE_C}),
                cmath(r"\text{common share}", r"=", r"\frac{\mathrm{tr}(B\Sigma_f B^\top)}{\mathrm{tr}\,\mathrm{Var}(F_t)}", font_size=38),
                cmath(r"\text{rising}", r"\Rightarrow", '\\text{more common flow; cause unidentified}', font_size=38,
                      colors={r"\text{rising}": BAD})]
        whys = [why(r"the order flows of many traders, or of many stocks, on a few common factors: Part 31's risk "
                    r"model, applied to flow instead of returns"),
                why('assumes $\\mathrm{Cov}(f_t,u_t)=0$; common variation need not be caused by shared AI models'),
                why(r"a supervisor with trade-level data could track it over time; a firm can track its own flow's "
                    r"correlation with the market's")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "A possible empirical diagnostic. <bookmark mark='a'/> Fit a factor model to a vector of order flows. <bookmark mark='b'/> The displayed variance fraction assumes factor-residual orthogonality and a suitable factor specification. <bookmark mark='c'/> More common variation can reflect shared news, benchmarks or rebalancing as well as similar models. It does not identify AI uniformity or predict a crisis on its own. Data coverage and model uncertainty must accompany any reported estimate."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def public_good(self):
        cards = VGroup(
            desk_question(r"diversity is a public good", 'shared exposures can create amplification costs beyond the individual firm; diversity benefits depend on the mechanism', width=12.4, font_size=19),
            desk_question(r"what reduces it", r"different data, different horizons, different objectives; and limits "
                          r"that bind on the crowd, such as circuit breakers that pause rather than close (Part 41)",
                          width=12.4, font_size=19),
            desk_question(r"what to test", r"how a strategy does against copies of itself: the market it would face if "
                          r"it succeeded and was imitated", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three implications, conditional on the mechanism. <bookmark mark='a'/> Shared exposures can create an externality when firms do not bear all amplification costs. Diversity can help, but its value depends on accuracy, liquidity and responses. <bookmark mark='b'/> Different data, horizons and objectives may reduce alignment; market controls need their own evaluation. <bookmark mark='c'/> Test a strategy against copies of itself and alternative populations. This is a stress scenario rather than a prediction that successful strategies will all be copied."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the IMF and the Financial Stability Board both reported on AI in finance in 2024. What do you "
                       r"think worried them most?")
        with self.voiceover(
            "Pause and predict. The International Monetary Fund and the Financial Stability Board both reported on "
            "artificial intelligence in finance in twenty twenty-four. What do you think worried them most?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
