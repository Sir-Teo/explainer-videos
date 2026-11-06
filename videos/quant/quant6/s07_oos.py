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
        c = chapter_card(6, r"Out of sample: can anything beat the mean?", (
                                                                               'Chronological refits on revised historical data'
                                                                           ), part=PART)
        with self.voiceover(
            'Chapter six. Out of sample: can anything beat the historical mean?'
        ):
            show_card(self, c)
        self.play(FadeOut(c))

    def realtime(self, o):
        sp = np.asarray(o["slope_path"])
        ts = np.asarray(o["t"])
        ds = np.asarray(o["predictors"]["dividend yield"]["dsse"])
        g1 = axes([1927, 2021], [-0.01, 0.025], x_length=10.6, y_length=2.4, ylabel=r"slope on the log dividend "
                  r"yield, chronological refit ($\pm 2$ Newey--West s.e.)", xticks=[], yticks=[0, 0.01, 0.02],
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
        src = wrapped_label(r"Shiller, revised history: real log total returns; historical release vintages and "
                            r"publication lags are not reconstructed", 12.0, 17, GREY_B).to_edge(DOWN, buff=0.2)
        at = o["dsse_at"]
        with self.voiceover(
            "Every regression so far used the whole sample. Goyal and Welch's 2008 question was whether a "
            'forecast beats the historical mean. Our illustration begins in 1927, fitting only earlier dated rows'
            ' each time. It uses revised Shiller data without historical release vintages, so this is a '
            'chronological retrospective exercise, not a verified real-time trading backtest. <bookmark '
            "mark='a'/> On top, the refitted dividend-yield slope and its band. It wanders, often including zero."
            " <bookmark mark='b'/> Below, the historical mean's squared error minus the predictor's, added up. "
            "Green while the predictor gains, red while it loses. <bookmark mark='c'/> It mostly loses. The "
            'cumulative score is negative by 1990, falls sharply in the late nineties, and remains negative at '
            'the end of this sample.'
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
                cmath(r"\frac{\Delta \mathbb{E}[r_p^e]}{\mathbb{E}[r_p^e]}", r"=", r"\frac{R^2_{pop}}{1 - R^2_{pop}}\,\frac{1 + S^2}{S^2}"
                      r"\;\approx\; \frac{R^2_{pop}}{S^2}", font_size=36, colors=C_)]
        whys = [why(r"the benchmark is the running historical mean, not zero; negative means the mean won"),
                why(r"Goyal and Welch's picture: the curve rises while the predictor is ahead"),
                wrapped_label(r"Separate excess-return model: population moments, mean-variance investor, fixed "
                              r"risk aversion; $S$ is an excess-return Sharpe ratio (Campbell--Thompson 2008)", 11.8, 20, GREY_B)]
        step = ladder(self, rows[:2], whys[:2], keep=2, top=2.4, x=-0.6, buff=1.0, edge=6.8)
        rows[2].move_to(UP * 1.2)
        whys[2].next_to(rows[2], DOWN, buff=0.4)
        example = MathTex(r"\text{stylized: } S=0.10,\ R^2_{pop}=0.001\quad\Rightarrow\quad"
                          r"\text{gain}\approx10.1\%", font_size=30, color=GOOD).shift(DOWN * 1.1)
        with self.voiceover(
            "The measure is the out-of-sample R-squared: one minus the predictor's squared forecast errors over "
            "the historical mean's. The running mean is itself estimated; negative means it won. <bookmark "
            "mark='a'/> The cumulative difference rises while the predictor gains. <bookmark mark='b'/> A "
            'separate result from Campbell and Thompson concerns a mean-variance investor forecasting excess '
            'returns, with known population moments and risk aversion held fixed. Its gain depends on the '
            'population predictive R-squared and the excess-return Sharpe ratio, not directly on a measured '
            "backtest R-squared. <bookmark mark='c'/> In a stylized example, a monthly Sharpe of point one and "
            'population R-squared of point zero zero one give about a ten percent proportional gain. Our '
            'empirical table uses real log total returns, so we do not insert its mean-to-volatility ratio into '
            "this excess-return formula. Estimation error and trading costs can erase a model's theoretical gain."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeOut(VGroup(*rows[:2], *whys[:2])))
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("c")
            self.play(FadeIn(example))
        self.wait(0.5)
        self.clear_scene()

    def table(self, o):
        P = o["predictors"]
        head = [label(t, font_size=20, color=GREY_B) for t in
                (r"predictor", r"in-sample $t$", r"in-sample $R^2$", r"$R^2_{OS}$")]
        cells = list(head)
        for k, v in P.items():
            c_os = GOOD if v["r2_os"] > 0 else BAD
            cells += [label(NAMES[k], font_size=22, color=GREY_A), MathTex(f"{v['t_is']:+.2f}", font_size=26),
                      MathTex(f"{100 * v['r2_is']:.2f}\\%", font_size=26),
                      MathTex(f"{100 * v['r2_os']:+.2f}\\%", font_size=26, color=c_os)]
        grid = VGroup(*cells).arrange_in_grid(rows=len(P) + 1, cols=4, buff=(0.55, 0.2), col_alignments="lrrr")
        grid.to_edge(UP, buff=0.5)
        n_pos = sum(v["r2_os"] > 0 for v in P.values())
        best = max(P, key=lambda k: P[k]["r2_os"])
        note_ = VGroup(
            wrapped_label(r"Real log total returns, chronological expanding fits from 1927; revised data. Five "
                          r"predictors tried. Legacy CT values are omitted: their sign used the full sample.",
                          12.0, 19, GREY_B),
            wrapped_label(r"Goyal, Welch and Zafirov (2024): 29 newer predictors from 26 papers, plus the original 17, "
                          r"through 2021: more than a third are insignificant even in sample, and about half of the "
                          r"rest fail out of sample", 12.0, 21, ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(grid, DOWN, buff=0.35)
        q = predict((
                        'Does an in-sample $R^2$ of 0.06\\% guarantee a positive forecast $R^2$?'
                    )).to_edge(DOWN,
                                                                                                         buff=0.15)
        answer = wrapped_label(r"No guarantee: estimation error and changing relationships can outweigh the signal.",
                               11.6, 24, GOOD).move_to(q)
        bv = P[best]
        verdict = (f"Only {NAMES[best]} beats the mean, with an out-of-sample R-squared of {100 * bv['r2_os']:.2f} "
                   "percent; " if n_pos == 1 else f"{n_pos} of the five beat the mean; ") if n_pos else \
            "None of the five beats the mean; "
        with self.voiceover(
            f"Five classic predictors from Shiller's data, the same experiment for each. <bookmark "
            f"mark='a'/> In sample, the largest t-statistic is {max((abs(v['t_is']) for v in P.values())):.1f}"
            f'. Out of sample, {verdict}'
            f'the dividend yield, the most famous of them, loses. Published Campbell-Thompson '
            f'restrictions concern excess returns and a sign chosen before testing. We omit the legacy '
            f'restricted column: our old routine chose its sign from the full sample, introducing '
            f"hindsight. <bookmark mark='b'/> And remember the count: we tried five, so a winner among "
            f'them is partly luck. Goyal, Welch and Athanasse Zafirov repeated the exercise in 2024 with'
            f' twenty-nine newer predictors from twenty-six papers: more than a third were insignificant'
            f" even in sample, and about half of the rest failed out of sample. <bookmark mark='c'/> "
            f'Pause and predict: does an in-sample R-squared of six hundredths of a percent guarantee a '
            f"positive forecast R-squared? <bookmark mark='d'/> No. Estimation error and changing "
            f'relationships can outweigh the signal; a positive result is possible, but is not '
            f'guaranteed by that one in-sample number. So far, least squares. Next: the method behind '
            f'most models in this series, maximum likelihood.'
        ) as vo:
            self.play(FadeIn(VGroup(*head, *cells[4::4])), FadeIn(note_[0]), run_time=0.6)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for i, c in enumerate(cells[4:]) if i % 4],
                                  lag_ratio=0.03, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(note_[1]))
            vo.wait_until("c")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("d")
            self.wait(0.8)
            self.play(FadeOut(q), FadeIn(answer))
        self.wait(0.4)
        self.clear_scene()
