from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
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
            f"Chapter seven, and the answer to the pause: {100 * r['common']:.0f} percent. A fifth of each trade "
            "comes from the shared model, but those fifths all point the same way, while the other four fifths cancel "
            "across a hundred traders. So the common part dominates the market's order flow. A little shared input, "
            "multiplied by a crowd, is most of what the market sees."
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
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lemma(self):
        rows = [cmath(r"x_i", r"=", r"w\,s + (1 - w)\,e_i", font_size=42, colors={r"x_i": SHARE_C}),
                cmath(r"\text{Var}\Bigl(\sum_i x_i\Bigr)", r"=", r"N^2 w^2 + N(1 - w)^2", font_size=40),
                cmath(r"\text{common share}", r"=", r"\frac{N w^2}{N w^2 + (1 - w)^2}", font_size=40,
                      colors={r"\text{common share}": BAD}),
                cmath(r"w = 0.2,\ N = 100", r"\Rightarrow", r"\frac{4}{4.64} = 86\%", font_size=40)]
        whys = [why(r"each trader's order: a weight $w$ on the shared signal $s$, the rest on its own view; all independent "
                    r"with unit variance"),
                why(r"the shared parts add up coherently, $(Nw)^2$; the private parts add up as a random walk, $N(1-w)^2$"),
                why(r"so the shared part's share of the variance grows with $N$ for any $w > 0$"),
                why(r"a fifth of each trade, but 86\% of the market's variance: it tends to one as the crowd grows")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The arithmetic. <bookmark mark='a'/> Each trader's order puts a weight w on the shared signal and the rest "
            "on its own view. <bookmark mark='b'/> Add them up. The shared parts add coherently, N squared w squared; "
            "the private parts add like a random walk, N times one minus w squared. <bookmark mark='c'/> So the common "
            "share grows with the size of the crowd, for any positive w. <bookmark mark='d'/> At a weight of a fifth and "
            "a hundred traders, eighty-six percent."
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
        note_ = label(r"labels: common share of the flow", font_size=15, color=BAD)
        side = VGroup(leg, note_).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        r2 = [x for x in rows if x["share"] == 0.2][0]
        with self.voiceover(
            "In simulation, with a hundred traders whose orders move the price. <bookmark mark='a'/> Volatility "
            f"against the weight on the shared model. At a fifth, it is already {r2['vol_ratio']:.1f} times the "
            "diverse market's; with everyone following the model, ten times. <bookmark mark='b'/> The dots lie on the "
            "formula's line. <bookmark mark='c'/> And the labels show the common share: past a weight of a tenth, more "
            "than half of everything the market sees is one signal."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.4) for d_ in dots], lag_ratio=0.2), run_time=2)
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
        head = label(r"the day the shared model errs by 4 s.d.: that day's return, in units of the diverse market's daily volatility",
                     font_size=20).to_edge(UP, buff=0.6)
        r2 = [x for x in rows if x["share"] == 0.2][0]
        with self.voiceover(
            "Now let the shared model make one mistake: on one day its signal is wrong by four standard deviations. "
            "<bookmark mark='a'/> In the diverse market, nothing happens: no one is listening to it. "
            f"<bookmark mark='b'/> At a weight of a fifth, that day's move is {r2['shock_sd']:.0f} times the diverse market's daily "
            "volatility. With everyone on the model, over fifty. A model error that would be noise for one firm is a "
            "crash for a market that shares it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.2) for b_ in bars[1:]], lag_ratio=0.3), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def measure(self):
        rows = [cmath(r"F_t", r"=", r"B\,f_t + u_t", font_size=42, colors={r"F_t": SHARE_C}),
                cmath(r"\text{common share}", r"=", r"\frac{\mathrm{tr}(B\Sigma_f B^\top)}{\mathrm{tr}\,\mathrm{Var}(F_t)}", font_size=38),
                cmath(r"\text{rising}", r"\Rightarrow", r"\text{the crowd is converging}", font_size=38,
                      colors={r"\text{rising}": BAD})]
        whys = [why(r"the order flows of many traders, or of many stocks, on a few common factors: Part 31's risk "
                    r"model, applied to flow instead of returns"),
                why(r"the part of the flow's variance the factors explain: this chapter's common share, measured"),
                why(r"a supervisor with trade-level data could track it over time; a firm can track its own flow's "
                    r"correlation with the market's")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "How would anyone see it coming? <bookmark mark='a'/> Model the order flows of many traders on a few common "
            "factors: Part thirty-one's risk model, applied to flow rather than returns. <bookmark mark='b'/> The share "
            "of the flow's variance the factors explain is this chapter's common share, measured. "
            "<bookmark mark='c'/> A rising share says the crowd is converging. A supervisor with trade-level data could "
            "track it; a firm can at least track how correlated its own flow has become with everyone else's."
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
            desk_question(r"diversity is a public good", r"each firm gains from using the best available model; the "
                          r"market loses when all do, and no single firm bears that cost", width=12.4, font_size=19),
            desk_question(r"what reduces it", r"different data, different horizons, different objectives; and limits "
                          r"that bind on the crowd, such as circuit breakers that pause rather than close (Part 41)",
                          width=12.4, font_size=19),
            desk_question(r"what to test", r"how a strategy does against copies of itself: the market it would face if "
                          r"it succeeded and was imitated", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three conclusions. <bookmark mark='a'/> Diversity is a public good. Each firm gains by using the best model "
            "it can find; the market loses when all do, and no firm bears the cost. That is Part forty-one's fire-sale "
            "externality again. <bookmark mark='b'/> What reduces it: different data, horizons and objectives, and limits "
            "that bind on the crowd. <bookmark mark='c'/> And what to test: how a strategy does against copies of "
            "itself, the market it would face if it succeeded and were imitated."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
        self.wait(0.5)
        self.clear_scene()
