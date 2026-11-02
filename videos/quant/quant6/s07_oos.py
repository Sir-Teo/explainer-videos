from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load, predict, real_data, show_card

NAMES = {"dividend yield": r"dividend yield", "earnings yield": r"earnings yield", "CAPE": r"CAPE",
         "10-year yield": r"10-year yield", "inflation": r"inflation"}


class OutOfSample(VoiceoverScene):
    def construct(self):
        o = load("oos")
        self.card()
        self.realtime(o)
        self.derive(o)
        self.table(o)

    def card(self):
        c = chapter_card(6, r"Out of sample: can anything beat the mean?", r"What would a forecaster in 1927 have "
                         r"known?", part=PART)
        with self.voiceover("Chapter six. Out of sample: can anything beat the historical mean?"):
            show_card(self, c)
        self.play(FadeOut(c))

    def realtime(self, o):
        sp = np.asarray(o["slope_path"])
        ts = np.asarray(o["t"])
        ds = np.asarray(o["predictors"]["dividend yield"]["dsse"])
        g1 = axes([1927, 2021], [-0.01, 0.025], x_length=10.6, y_length=2.4, ylabel=r"slope on the log dividend "
                  r"yield, fitted on data to date ($\pm 2$ Newey--West s.e.)", xticks=[], yticks=[0, 0.01, 0.02],
                  font_size=15).to_edge(UP, buff=0.55)
        a1 = g1.ax
        lo, hi = float(ds.min()) * 1.1, max(float(ds.max()), 0.0005) + 0.001
        g2 = axes([1927, 2021], [lo, hi], x_length=10.6, y_length=2.6, ylabel=r"cumulative $\Delta$SSE: the mean's "
                  r"squared errors minus the predictor's", xticks=[1930, 1950, 1970, 1990, 2010], yticks=[0, round(lo / 2, 3)],
                  font_size=15).next_to(g1, DOWN, buff=0.55)
        a2 = g2.ax
        red = Rectangle(width=a2.c2p(2000, 0)[0] - a2.c2p(1995, 0)[0], height=a2.c2p(0, hi)[1] - a2.c2p(0, lo)[1],
                        stroke_width=0, fill_color=BAD, fill_opacity=0.15).move_to(
            ((a2.c2p(1995, lo) + a2.c2p(2000, hi)) / 2))
        zero = DashedLine(a2.c2p(1927, 0), a2.c2p(2021, 0), color=GREY_C, stroke_width=1.5)
        now = ValueTracker(1927.0)

        def top():
            t = now.get_value()
            m = sp[:, 0] <= t
            if m.sum() < 2:
                return VGroup()
            x, b, s = sp[m, 0], sp[m, 1], sp[m, 2]
            return VGroup(band(a1, x, np.clip(b - 2 * s, -0.01, 0.025), np.clip(b + 2 * s, -0.01, 0.025), ALT, 0.2),
                          curve(a1, x, b, ALT, stroke_width=3))

        def bottom():
            t = now.get_value()
            m = ts <= t
            if m.sum() < 2:
                return VGroup()
            x, y = ts[m], ds[m]
            segs = VGroup()
            for i in range(1, len(x)):
                c = GOOD if y[i] >= y[i - 1] else BAD
                segs.add(Line(a2.c2p(x[i - 1], y[i - 1]), a2.c2p(x[i], y[i]), color=c, stroke_width=3))
            return segs
        cur = always_redraw(lambda: DashedLine(a1.c2p(now.get_value(), 0.025), a2.c2p(now.get_value(), lo),
                                               color=WHITE, stroke_width=1.5, stroke_opacity=0.6))
        yr = always_redraw(lambda: MathTex(rf"{int(now.get_value())}", font_size=30, color=WHITE).next_to(
            g1, UP, buff=0.0).align_to(g1, RIGHT))
        tm, bm = always_redraw(top), always_redraw(bottom)
        src = real_data(r"Shiller, monthly 1871--2020: real log total return on last month's log dividend yield")
        at = o["dsse_at"]
        with self.voiceover(
            "Every regression so far used the whole sample, data no investor had at the time. Amit Goyal and Ivo Welch, "
            "in 2008, asked the forecaster's question. Stand in 1927 with only the past: fit on everything to date, "
            "forecast next month, step forward, repeat. <bookmark mark='a'/> On top, the slope on the dividend yield as "
            "the forecaster saw it, with its band. It wanders, often including zero. <bookmark mark='b'/> Below, the "
            "scoreboard: the historical mean's squared error minus the predictor's, added up. Green while the predictor "
            "gains, red while it loses. <bookmark mark='c'/> It mostly loses. By 1990 the total is negative, and in the "
            "late nineties, as the yield called stocks expensive month after month while they kept rising, it falls off "
            "a cliff, and never recovers."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), Create(zero), FadeIn(src))
            self.add(tm, bm, cur, yr)
            vo.wait_until("a")
            self.play(now.animate.set_value(1960), run_time=vo.until("c"), rate_func=linear)
            self.play(FadeIn(red), now.animate.set_value(2020.9), run_time=max(vo.remaining(1.0) - 1.0, 2.0),
                      rate_func=linear)
        for m in (tm, bm, cur, yr):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def derive(self, o):
        C_ = {r"R^2_{OS}": EST, r"\Delta SSE(\tau)": GOOD}
        rows = [cmath(r"R^2_{OS}", r"=", r"1 - \frac{\sum_t (r_t - \hat r_{t|t-1})^2}{\sum_t (r_t - \bar r_{t-1})^2}",
                      font_size=36, colors=C_),
                cmath(r"\Delta SSE(\tau)", r"=", r"\textstyle\sum_{t \le \tau}\big[(r_t - \bar r_{t-1})^2 - "
                      r"(r_t - \hat r_{t|t-1})^2\big]", font_size=36, colors=C_),
                cmath(r"\frac{\Delta \mathbb{E}[r_p]}{\mathbb{E}[r_p]}", r"=", r"\frac{R^2}{1 - R^2}\,\frac{1 + S^2}{S^2}"
                      r"\;\approx\; \frac{R^2}{S^2}", font_size=36, colors=C_)]
        whys = [why(r"the benchmark is the running historical mean, not zero; negative means the mean won"),
                why(r"Goyal and Welch's picture: the curve rises while the predictor is ahead"),
                why(r"Campbell and Thompson (2008): a mean-variance investor's proportional gain; $S$ is the monthly "
                    r"Sharpe ratio")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=1.0, edge=6.8)
        s2 = o["S2"]
        with self.voiceover(
            "The measure is the out-of-sample R-squared: one minus the predictor's squared forecast errors over the "
            "historical mean's. The benchmark is not zero; it is the running mean, which itself is estimated. Negative "
            "means the mean won. <bookmark mark='a'/> The cumulative difference of squared errors is Goyal and Welch's "
            "picture, the one we just watched: rising while the predictor is ahead. <bookmark mark='b'/> How large must "
            "R-squared be to matter? John Campbell and Samuel Thompson, also in 2008, showed that a mean-variance "
            "investor who times the market with the forecast raises her expected return by a proportion of R-squared "
            "over one minus R-squared, times one plus the squared Sharpe ratio over the squared Sharpe ratio: about "
            "R-squared over the squared monthly Sharpe ratio. On this sample, the squared monthly Sharpe ratio is "
            f"{100 * s2:.1f} percent, so even an out-of-sample R-squared of half a percent would raise the average "
            f"return by about {100 * 0.005 / s2:.0f} percent. Tiny R-squared, real money, if it survives out of sample."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def table(self, o):
        P = o["predictors"]
        head = [label(t, font_size=20, color=GREY_B) for t in
                (r"predictor", r"in-sample $t$", r"in-sample $R^2$", r"$R^2_{OS}$", r"$R^2_{OS}$, CT")]
        cells = list(head)
        for k, v in P.items():
            c_os = GOOD if v["r2_os"] > 0 else BAD
            c_ct = GOOD if v["r2_os_ct"] > 0 else BAD
            cells += [label(NAMES[k], font_size=22, color=GREY_A), MathTex(f"{v['t_is']:+.2f}", font_size=26),
                      MathTex(f"{100 * v['r2_is']:.2f}\\%", font_size=26),
                      MathTex(f"{100 * v['r2_os']:+.2f}\\%", font_size=26, color=c_os),
                      MathTex(f"{100 * v['r2_os_ct']:+.2f}\\%", font_size=26, color=c_ct)]
        grid = VGroup(*cells).arrange_in_grid(rows=len(P) + 1, cols=5, buff=(0.55, 0.2), col_alignments="lrrrr")
        grid.to_edge(UP, buff=0.5)
        n_pos = sum(v["r2_os"] > 0 for v in P.values())
        best = max(P, key=lambda k: P[k]["r2_os"])
        note_ = VGroup(
            wrapped_label(r"monthly, out of sample from 1927 (expanding window); CT: Campbell--Thompson restrictions "
                          r"(wrong-signed slopes fall back to the mean, negative forecasts set to zero); five "
                          r"predictors tried, so five trials on the counter", 12.0, 19, GREY_B),
            wrapped_label(r"Goyal, Welch and Zafirov (2024): 29 newer predictors from 26 papers, plus the original 17, "
                          r"through 2021: more than a third are insignificant even in sample, and about half of the "
                          r"rest fail out of sample", 12.0, 21, ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(grid, DOWN, buff=0.35)
        q = predict(r"An in-sample $R^2$ of 0.06\% a month. Can the out-of-sample $R^2$ be positive?").to_edge(DOWN,
                                                                                                         buff=0.15)
        bv = P[best]
        verdict = (f"Only {NAMES[best]} beats the mean, with an out-of-sample R-squared of {100 * bv['r2_os']:.2f} "
                   "percent; " if n_pos == 1 else f"{n_pos} of the five beat the mean; ") if n_pos else \
            "None of the five beats the mean; "
        with self.voiceover(
            "Five classic predictors from Shiller's data, the same experiment for each. <bookmark mark='a'/> In "
            f"sample, the largest t-statistic is {max(abs(v['t_is']) for v in P.values()):.1f}. Out of sample, "
            f"{verdict}the dividend yield, the most famous of them, loses. Campbell and Thompson's common-sense restrictions, "
            "never forecast a negative premium and never trust a wrong-signed slope, help a little, as they found. "
            "<bookmark mark='b'/> And remember the count: we tried five, so a winner among them is partly luck. "
            "Goyal, Welch and Athanasse Zafirov repeated the exercise in 2024 with twenty-nine newer predictors "
            "from twenty-six papers: more than a third were insignificant even in sample, and about half of the "
            "rest failed out of sample. <bookmark mark='c'/> Pause and predict: with an in-sample R-squared of six "
            "hundredths of a percent, can the out-of-sample R-squared be positive? Rarely: the estimated slope's "
            "own noise costs more than that."
            " So far, least squares. Next: the method behind most models in this series, maximum likelihood."
        ) as vo:
            self.play(FadeIn(VGroup(*head)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells[5:]], lag_ratio=0.03, run_time=3))
            self.play(FadeIn(note_[0]))
            vo.wait_until("b")
            self.play(FadeIn(note_[1]))
            vo.wait_until("c")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
