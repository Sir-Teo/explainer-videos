from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, SDF, TRUE, ask, fit_right, illustration, load


class Decay(VoiceoverScene):
    def construct(self):
        s = load("shrink")
        self.card()
        self.eb(s)
        self.worked(s)
        self.scatter(s)
        self.compare(s)
        self.mp()
        self.categories(s)
        self.pubbias()

    def card(self):
        c = chapter_card(4, r"Decay, shrinkage and publication bias", r"How much of a published premium should you "
                         r"expect to keep?", lit=(2016,), part=PART)
        with self.voiceover("Chapter four. Part three measured how anomalies decay after publication. This chapter asks "
                            "how much of that decay a statistician should have predicted."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def eb(self, s):
        e = s["eb"]
        rows = [cmath(r"t_i", r"=", r"\theta_i + \varepsilon_i,\quad \varepsilon_i \sim N(0, 1),\quad \theta_i \sim "
                      r"N(m, v)", font_size=38, colors={r"t_i": SDF}),
                cmath(r"\mathbb{E}[\theta_i \mid t_i]", r"=", r"m + \frac{v}{v + 1}(t_i - m)", font_size=40,
                      colors={r"\mathbb{E}[\theta_i \mid t_i]": GOOD}),
                cmath(r"\hat v = \text{var}(t) - 1", r"\Rightarrow", rf"\frac{{\hat v}}{{\hat v + 1}} = {e['shrink']:.2f}",
                      font_size=38)]
        whys = [why(r"each reported $t$ is the predictor's true strength $\theta$ plus sampling noise of variance one; "
                    r"the true strengths are spread across the zoo"),
                why(r"the best guess of a predictor's true strength pulls its $t$ toward the zoo's average, more the noisier "
                    r"the estimates are relative to the spread: empirical Bayes, as in Part 6"),
                why(r"the zoo's $t$'s are so spread out (their variance is near six) that noise explains only a sixth of the "
                    r"spread: by this arithmetic alone, a predictor should keep about 83\% of its $t$")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "Treat each reproduced t-statistic as the predictor's true strength plus noise with variance one. The true "
            "strengths vary across the zoo. <bookmark mark='a'/> Then the best estimate of a predictor's true strength "
            "pulls its t toward the zoo's average, by a factor that depends on how much of the spread is noise. "
            "<bookmark mark='b'/> The zoo's t-statistics are very spread out, with a variance near six, so noise "
            "accounts for only a sixth of it. By sampling error alone, a predictor should keep about eighty-three "
            "percent of its strength."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def worked(self, s):
        e = s["eb"]
        rows = [cmath(r"t = 7", r"\Rightarrow", rf"{e['m']:.1f} + {e['shrink']:.2f}\,(7 - {e['m']:.1f}) \approx "
                      rf"{e['m'] + e['shrink'] * (7 - e['m']):.1f}", font_size=40, colors={r"t = 7": SDF}),
                cmath(r"t = 2.5", r"\Rightarrow", rf"{e['m']:.1f} + {e['shrink']:.2f}\,(2.5 - {e['m']:.1f}) \approx "
                      rf"{e['m'] + e['shrink'] * (2.5 - e['m']):.1f}", font_size=40, colors={r"t = 2.5": SDF})]
        whys = [why(r"a very strong predictor is pulled down a little toward the zoo's average"),
                why(r"and a marginal one is pulled up: in this zoo the average published predictor is strong, so empirical "
                    r"Bayes, ignoring how the zoo was selected, is generous to weak ones. That is the first sign that noise "
                    r"is not the whole story")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Two examples. <bookmark mark='a'/> A predictor with a t-statistic of seven is pulled down a little, to "
            "about six and a half. <bookmark mark='b'/> A marginal one at two and a half is pulled up, toward the "
            "zoo's average of nearly four. Measured against the zoo it came from, a weak result looks better than it "
            "is, because the zoo is full of strong ones. That is the first hint that noise around the published "
            "numbers is not the whole story: the zoo itself was selected."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, s):
        mi, mp = np.asarray(s["mi"]), np.asarray(s["mp"])
        g = axes([-0.5, 2.5], [-1.5, 2.5], x_length=6.6, y_length=4.6, xlabel=r"mean return in the original sample, \% a "
                 r"month", ylabel=r"after publication, to 2020", xticks=[0, 0.5, 1.0, 1.5, 2.0], yticks=[-1, 0, 1, 2],
                 font_size=13).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(min(max(x, -0.49), 2.49), min(max(y, -1.49), 2.49)), radius=0.045, color=SDF,
                            fill_opacity=0.7) for x, y in zip(mi, mp)])
        diag = DashedLine(ax.c2p(-0.5, -0.5), ax.c2p(2.5, 2.5), color=GREY_B, stroke_width=1.5)
        c = np.polyfit(mi, mp, 1)
        fit = Line(ax.c2p(-0.5, np.polyval(c, -0.5)), ax.c2p(2.5, np.polyval(c, 2.5)), color=BAD, stroke_width=3)
        side = VGroup(
            MathTex(rf"\text{{slope}} = {s['slope']:.2f}", font_size=26, color=BAD),
            MathTex(rf"\text{{average}}:\ {s['mean_in']:.2f}\%\ \to\ {s['mean_post']:.2f}\%\ (\times {s['ratio']:.2f})",
                    font_size=22),
            wrapped_label(r"208 predictors with at least two years after publication. The dashed line is no decay; the "
                          r"red line is the fit. A predictor that earned twice as much in its sample earns, after "
                          r"publication, only a little more", 3.4, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "What actually happened. Each predictor's mean return in its original sample, against its mean after "
            "publication, through 2020. <bookmark mark='a'/> The fitted slope is about four tenths, and the average "
            "fell from seven tenths of a percent a month to about a quarter: predictors kept thirty-eight percent of "
            "their returns, not eighty-three."
        ) as vo:
            self.play(FadeIn(g), Create(diag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.01), Create(fit), FadeIn(side), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def compare(self, s):
        bars = [(r"kept, by sampling error alone", s["eb"]["shrink"], GOOD), (r"kept, observed", s["ratio"], BAD)]
        g = axes([-0.6, 1.6], [0, 1.0], x_length=5.6, y_length=4.2, xlabel=r"", ylabel=r"share of the original premium",
                 xticks=[], yticks=[0, 0.25, 0.5, 0.75, 1.0], font_size=13).to_edge(LEFT, buff=1.0).shift(DOWN * 0.2)
        ax = g.ax
        grp = VGroup()
        for i, (nm, v, col) in enumerate(bars):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            grp.add(VGroup(Rectangle(width=0.8, height=y1 - y0, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                [ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]), MathTex(f"{100 * v:.0f}\\%", font_size=26).next_to(ax.c2p(i, v), UP,
                                                                                                       buff=0.08),
                label(nm, font_size=15, color=GREY_A).next_to(ax.c2p(i, 0), DOWN, buff=0.15)))
        side = VGroup(
            label(r"the gap needs another cause:", font_size=20),
            wrapped_label(r"1. selection beyond noise: specification search inside the sample (more than one $t$ was "
                          r"tried per paper)", 4.6, 17, GREY_A),
            wrapped_label(r"2. arbitrage after publication: McLean and Pontiff found the decay largest where trading is "
                          r"cheapest, and trading volume in the stocks rising", 4.6, 17, GREY_A),
            wrapped_label(r"3. a changing market: lower costs, faster information, more quantitative capital", 4.6, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Put the two side by side. <bookmark mark='a'/> Sampling error alone predicts that a predictor keeps "
            "eighty-three percent; the data show thirty-eight. <bookmark mark='b'/> The gap needs another cause. "
            "Selection beyond pure noise, because each paper tried more than one specification inside its sample. "
            "Arbitrage after publication: McLean and Pontiff found the decay largest where trading is cheapest, with "
            "trading volume in the affected stocks rising. And a changing market, with lower costs, faster information "
            "and more quantitative money."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in grp], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in side], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def mp(self):
        g = axes([-0.6, 2.6], [0, 1.1], x_length=6.4, y_length=4.0, xlabel=r"", ylabel=r"share of the in-sample return",
                 xticks=[], yticks=[0, 0.25, 0.5, 0.75, 1.0], font_size=13).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        vals = [(r"in sample", 1.0, GOOD), (r"after the sample, before publication", 0.74, HURDLE),
                (r"after publication", 0.42, BAD)]
        grp = VGroup()
        for i, (nm, v, col) in enumerate(vals):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            grp.add(VGroup(Rectangle(width=0.8, height=y1 - y0, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                [ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]), MathTex(f"{100 * v:.0f}\\%", font_size=24).next_to(ax.c2p(i, v), UP,
                                                                                                        buff=0.08),
                wrapped_label(nm, 1.8, 14, GREY_A).next_to(ax.c2p(i, 0), DOWN, buff=0.15)))
        side = VGroup(
            wrapped_label(r"McLean and Pontiff (2016), 97 predictors: returns 26\% lower after the paper's sample ends but "
                          r"before it is published, 58\% lower after publication", 4.4, 17, GREY_A),
            MathTex(r"26\%\ \text{(statistical bias)} + 32\%\ \text{(publication)}", font_size=24, color=BAD),
            wrapped_label(r"the gap between the two windows isolates what publication itself does: investors learn, and "
                          r"trade", 4.4, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "David McLean and Jeffrey Pontiff separated the causes with a clever timeline. Between the end of a "
            "paper's sample and its publication, the predictor is out of sample but still unknown to the market. "
            "<bookmark mark='a'/> In that window, returns were about a quarter lower than in sample: that is the "
            "statistical bias, the selection and noise. After publication they were fifty-eight percent lower. "
            "<bookmark mark='b'/> The extra thirty-two points are what publication itself does. Investors read the "
            "paper, and trade."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in grp], lag_ratio=0.4), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def categories(self, s):
        cats = sorted(s["cats"].items(), key=lambda kv: -kv[1]["ratio"])
        cats = [(k, v) for k, v in cats if k != "Other"]
        g = axes([-0.6, len(cats) - 0.4], [0, 1.1], x_length=8.0, y_length=4.2, xlabel=r"", ylabel=r"share kept after "
                 r"publication", xticks=[], yticks=[0, 0.25, 0.5, 0.75, 1.0], font_size=13).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.2)
        ax = g.ax
        grp = VGroup()
        for i, (k, v) in enumerate(cats):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, max(v["ratio"], 0.005))[1]
            grp.add(VGroup(Rectangle(width=0.6, height=y1 - y0, stroke_width=0, fill_color=SDF, fill_opacity=0.85).move_to(
                [ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]),
                MathTex(f"{v['ratio']:.2f}", font_size=18).next_to(ax.c2p(i, v["ratio"]), UP, buff=0.06),
                label(rf"{k} ({v['n']})", font_size=13, color=GREY_A).next_to(ax.c2p(i, 0), DOWN, buff=0.12)))
        side = VGroup(
            MathTex(rf"\text{{clear in the paper}}:\ {s['clear_ratio']:.2f};\ \text{{likely}}:\ {s['likely_ratio']:.2f}",
                    font_size=20),
            wrapped_label(r"by the kind of data the predictor uses (Chen and Zimmermann's categories; groups of six or "
                          r"more). Price-based signals, the cheapest to compute and trade on, kept the least; the few "
                          r"13F-holdings signals kept almost all", 3.4, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "By the kind of data a predictor uses. <bookmark mark='a'/> Signals built from prices alone, the cheapest "
            "to compute and to trade on, kept the least, under three tenths. Accounting and analyst signals kept a "
            "little over a third. The handful of signals built from institutions' holdings kept almost everything, "
            "though six is too few to lean on. The pattern fits arbitrage: what is easiest to exploit decays fastest."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in grp], lag_ratio=0.2), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def pubbias(self):
        cards = VGroup(
            desk_question(r"publication bias, modelled", r"Chen and Zimmermann (2020): if only $t > 2$ is published, the "
                          r"published $t$'s are truncated; fitting that truncation, the bias in the average is small, about "
                          r"a tenth, because most published $t$'s are far above 2", width=12.0, font_size=20),
            desk_question(r"what that leaves", r"most of the decay is not statistical illusion but something that happened "
                          r"after publication: the market learned", width=12.0, font_size=20),
            desk_question(r"a rule of thumb", r"expect to keep between a third and a half of a published anomaly's "
                          r"return, before costs; Part 26 takes the costs", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Can publication bias explain the rest? <bookmark mark='a'/> Chen and Zimmermann modelled it: if only "
            "results with t above two get published, the published t-statistics are a truncated sample. Fitting that "
            "truncation, they found the bias small, about a tenth, because most published t's are far above two. "
            "<bookmark mark='b'/> So most of the decay is not a statistical illusion. Something happened after "
            "publication: the market learned. <bookmark mark='c'/> A working rule: expect to keep between a third and "
            "a half of a published anomaly's return, before costs."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a new paper reports an anomaly with $t = 3.5$ and 0.8\% a month. What return would you plan for if you "
                r"traded it from next year, and why?")
        with self.voiceover("A new paper reports an anomaly with a t-statistic of three and a half and zero point eight "
                            "percent a month. What return would you plan for if you traded it from next year, and why?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
