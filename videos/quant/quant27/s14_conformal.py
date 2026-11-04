from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COIN, GOOD, HURDLE, NET, OOS_C, PART, TREE, ask, fit_right, load


class Conformal(VoiceoverScene):
    def construct(self):
        c = load("conformal")
        self.card()
        self.split()
        self.panel(c)
        self.drift(c["btc"])
        self.aci(c["btc"])
        self.question()

    def card(self):
        c = chapter_card(13, r"Conformal prediction", r"How wide is a forecast's error, with no model of the errors?",
                         part=PART)
        with self.voiceover("Chapter thirteen. Every forecast in this part has been a single number. How wide should its "
                            "error bar be, if we refuse to assume anything about the errors?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def split(self):
        rows = [cmath(r"R_i", r"=", r"|\,y_i - \hat f(x_i)\,|,\quad i = 1, \dots, n\ \ \text{(calibration)}", font_size=34,
                      colors={r"R_i": TREE}),
                cmath(r"\hat q", r"=", r"R_{(k)},\quad k = \lceil (n + 1)(1 - \alpha) \rceil", font_size=34,
                      colors={r"\hat q": TREE}),
                cmath(r"C(x)", r"=", r"\big[\hat f(x) - \hat q,\ \hat f(x) + \hat q\,\big]", font_size=34,
                      colors={r"C(x)": NET}),
                cmath(r"\Pr\big(y \in C(x)\big)", r"\ge", r"1 - \alpha", font_size=34,
                      colors={r"\Pr\big(y \in C(x)\big)": GOOD})]
        whys = [why(r"fit the model on one set; on a second, held-out calibration set, record how far off it was"),
                why(r"the $k$-th smallest of those $n$ errors: the $+1$ makes room for the new point itself"),
                why(r"the interval for a new point: the forecast, plus or minus that quantile; any model, any $\hat f$"),
                why(r"if the new point and the calibration points are exchangeable, the new error is equally likely to "
                    r"rank anywhere among the $n + 1$, so it exceeds $\hat q$ with probability at most $\alpha$ "
                    r"(Vovk, Gammerman and Shafer 2005; Lei et al.\ 2018)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.5, buff=0.42, edge=6.9)
        with self.voiceover(
            "Split conformal prediction answers in four lines. <bookmark mark='a'/> Fit any model on one set of data. "
            "On a second set it has not seen, the calibration set, record how far off it was. <bookmark mark='b'/> "
            "Take the k-th smallest of those errors, where k is about one minus alpha of the way up, with one extra "
            "place left for the new point. <bookmark mark='c'/> The interval for a new point is the forecast plus or "
            "minus that error. <bookmark mark='d'/> And the guarantee needs no model of the errors at all, only that "
            "the new point is exchangeable with the calibration points: then its error is equally likely to rank "
            "anywhere among the n plus one, and lands above the k-th with probability at most alpha. Any network, any "
            "tree, any forecast; the guarantee is the same."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def panel(self, c):
        weekly = {a: np.asarray(c[a]["weekly"]) for a in ("0.1", "0.2")}
        n = len(weekly["0.1"])
        g = axes([0, n - 1], [0.4, 1.0], x_length=9.4, y_length=3.8, xlabel=r"test week, 2020",
                 ylabel=r"share of coins inside their interval", xticks=[], yticks=[0.4, 0.6, 0.8, 0.9, 1.0],
                 font_size=13).move_to(LEFT * 1.2 + DOWN * 0.2)
        ax = g.ax
        lines = VGroup()
        for a, col in (("0.1", NET), ("0.2", TREE)):
            lines.add(curve(ax, np.arange(n), np.clip(weekly[a], 0.4, 1.0), col, stroke_width=2.5))
        tgt = VGroup(DashedLine(ax.c2p(0, 0.9), ax.c2p(n - 1, 0.9), color=NET, stroke_width=1.5, stroke_opacity=0.7),
                     DashedLine(ax.c2p(0, 0.8), ax.c2p(n - 1, 0.8), color=TREE, stroke_width=1.5, stroke_opacity=0.7))
        side = VGroup(
            MathTex(rf"90\%:\ \text{{covered}}\ {100 * c['0.1']['cover']:.1f}\%", font_size=24, color=NET),
            MathTex(rf"80\%:\ \text{{covered}}\ {100 * c['0.2']['cover']:.1f}\%", font_size=24, color=TREE),
            MathTex(rf"\text{{worst week}}:\ {100 * weekly['0.1'].min():.0f}\%", font_size=24, color=BAD),
            wrapped_label(r"the NN2 forecast of each coin's next-week log return; calibrated on the second half of 2019, "
                          r"tested on 2020. On average the guarantee holds; week by week it does not: one crash moves "
                          r"every coin's error at once, and a week's coins are not exchangeable with last year's", 3.5, 15,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Try it on the coin panel. <bookmark mark='a'/> Take a network's forecast of every coin's next-week return, "
            "calibrate on the second half of 2019, and draw ninety and eighty percent intervals for each coin in each "
            "week of 2020. <bookmark mark='b'/> Over the whole year the ninety percent intervals cover eighty-nine point "
            "seven percent, close to the promise; the eighty percent ones cover only seventy-four. And week by week "
            "the lines swing: in the week of the March crash, twelve percent of coins were inside their ninety "
            "percent intervals. In a crash every coin's error is large at once, and the coins of that week are not "
            "exchangeable with last year's. The guarantee is an average over exchangeable draws, and a market is a "
            "sequence."
        ) as vo:
            self.play(FadeIn(g), Create(tgt))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def drift(self, b):
        r = np.asarray(b["r"])
        T = len(r)
        top = max(float(np.max(np.abs(r))) * 1.05, 0.1)
        g = axes([0, T - 1], [0, top], x_length=10.0, y_length=3.8, xlabel=r"day, from May 2018 to December 2020",
                 ylabel=r"Bitcoin's absolute daily return", xticks=[], yticks=[0, 0.1, 0.2, 0.3],
                 yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=13).move_to(DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Line(ax.c2p(i, 0), ax.c2p(i, min(abs(v), top)), stroke_width=1.2,
                             color=BAD if abs(v) > b["q_static"] else COIN, stroke_opacity=0.8) for i, v in enumerate(r)])
        stat = DashedLine(ax.c2p(0, b["q_static"]), ax.c2p(T - 1, b["q_static"]), color=HURDLE, stroke_width=2.5)
        cap = MathTex(rf"\text{{fixed interval, from the first 120 days}}:\ \pm {100 * b['q_static']:.1f}\%\ \ \to\ "
                      rf"\text{{covered}}\ {100 * b['cover_static']:.0f}\%", font_size=24, color=HURDLE).to_edge(UP,
                                                                                                      buff=0.5)
        with self.voiceover(
            "A sequence breaks exchangeability in a simpler way too. <bookmark mark='a'/> Forecast Bitcoin's daily "
            "return as zero, and calibrate a ninety percent interval on the first hundred and twenty days. <bookmark "
            "mark='b'/> Then use that fixed width for the next two and a half years. Calibrated in the turbulent first "
            "months of 2018, plus or minus ten percent is too wide for the calm of 2019: it covers ninety-eight "
            "percent of days, wasting width, and it still misses four days of March 2020."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in bars], lag_ratio=0.002, run_time=2))
            vo.wait_until("b")
            self.play(Create(stat), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def aci(self, b):
        ra, rs = np.asarray(b["roll_aci"]), np.asarray(b["roll_static"])
        n = len(ra)
        rows = [cmath(r"\alpha_{t+1}", r"=", r"\alpha_t + \gamma\,(\alpha - \mathrm{err}_t)", font_size=36,
                      colors={r"\alpha_{t+1}": NET}),
                cmath(r"\tfrac1T\textstyle\sum_{t} \mathrm{err}_t", r"\to", r"\alpha\ \ \text{whatever the data do}",
                      font_size=32, colors={r"\tfrac1T\textstyle\sum_{t} \mathrm{err}_t": GOOD})]
        for r_ in rows:
            r_.scale(0.9)
        eqs = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.35).shift(LEFT * 2.5)
        g = axes([0, n - 1], [0.6, 1.0], x_length=8.4, y_length=3.2, xlabel=r"day", ylabel=r"coverage, past 60 days",
                 xticks=[], yticks=[0.6, 0.8, 0.9, 1.0], font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 1.0)
        ax = g.ax
        la = curve(ax, np.arange(n), np.clip(ra, 0.6, 1.0), NET, stroke_width=2.5)
        ls = curve(ax, np.arange(n), np.clip(rs, 0.6, 1.0), HURDLE, stroke_width=2.5)
        tgt = DashedLine(ax.c2p(0, 0.9), ax.c2p(n - 1, 0.9), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            MathTex(rf"\text{{adaptive}}:\ {100 * b['cover_aci']:.1f}\%", font_size=26, color=NET),
            MathTex(rf"\text{{fixed}}:\ {100 * b['cover_static']:.1f}\%", font_size=26, color=HURDLE),
            wrapped_label(r"Gibbs and Cand\`es (2021): after a miss, widen; after a hit, narrow a little. $\gamma = 0.01$, "
                          r"widths from the last 120 days. The long-run miss rate is pinned at $\alpha$ even when the data "
                          r"are anything but exchangeable; what it cannot promise is coverage in any one month",
                          3.6, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.6)
        fit_right(side)
        with self.voiceover(
            "Isaac Gibbs and Emmanuel Candes repaired this in 2021. <bookmark mark='a'/> Keep a working level, alpha "
            "t. After every miss, lower it a little, which widens the interval; after every hit, raise it a little. "
            "<bookmark mark='b'/> The average miss rate is then forced to alpha in the long run, whatever the data do, "
            "with no exchangeability at all, because a run of misses keeps widening the interval until it stops "
            "missing. <bookmark mark='c'/> On Bitcoin, the adaptive interval covers eighty-nine point seven percent of "
            "days against a target of ninety, narrowing to two and a half percent in the calm and widening to eleven "
            "after the storms; the fixed one covers ninety-eight. This is the honest error bar for the House's forecasts: not a "
            "model of the errors, but a rule that keeps count of them."
        ) as vo:
            self.play(FadeIn(eqs[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]), FadeIn(g), Create(tgt))
            vo.wait_until("c")
            self.play(Create(ls), Create(la), run_time=2)
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a conformal interval for a strategy's monthly return is calibrated on 2010--2019 and covers 90\% "
                r"there. In 2020 it covers 70\%. Is the guarantee broken, and what would you change?")
        with self.voiceover(
            "Pause and predict. A conformal interval for a strategy's monthly return is calibrated on the 2010s and "
            "covers ninety percent there. In 2020 it covers seventy. Is the guarantee broken, and what would you "
            "change?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
