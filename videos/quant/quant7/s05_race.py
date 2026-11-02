from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data, tbar

MODEL_C = {"EWMA": GREY_B, "GARCH": FC, "GJR": FC, "HAR": VOL, "HARQ": VOL, "LSTM": ALT, "Transformer": ALT}
PARAMS = {"EWMA": r"0", "GARCH": r"3", "GJR": r"4", "HAR": r"4", "HARQ": r"5", "LSTM": r"1{,}233",
          "Transformer": r"2{,}625"}
SEES = {"EWMA": r"daily returns", "GARCH": r"daily returns", "GJR": r"daily returns, with sign",
        "HAR": r"realized variance", "HARQ": r"RV and its noise", "LSTM": r"22 days of log RV",
        "Transformer": r"22 days of log RV"}


class Race(VoiceoverScene):
    def construct(self):
        r = load("race")
        self.card()
        self.setup(r)
        self.results(r)
        self.year(r)

    def card(self):
        c = chapter_card(4, r"The race", r"Does anything beat a GARCH(1,1)?", part=PART)
        with self.voiceover("Chapter four. The race."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup(self, r):
        # the calendar: train, validate, test
        x0, x1 = -6.2, 6.2
        n_tr, n_va, n_te = r["train_days"], r["val_days"], r["test_days"]
        tot = n_tr + n_va + n_te
        w = lambda n: (x1 - x0) * n / tot  # noqa: E731
        segs = VGroup()
        cols = [GREY_B, ALT, GOOD]
        names = [rf"train: Aug.\ 2017 -- Jun.\ 2019 ({n_tr} days)", rf"validate: 2019 H2 ({n_va})",
                 rf"test: 2020 ({n_te})"]
        x = x0
        for n, c, nm in zip((n_tr, n_va, n_te), cols, names):
            rect = Rectangle(width=w(n), height=0.45, stroke_width=0, fill_color=c, fill_opacity=0.6)
            rect.move_to([x + w(n) / 2, 2.6, 0])
            segs.add(VGroup(rect, label(nm, font_size=18, color=c).next_to(rect, DOWN, buff=0.12)))
            x += w(n)
        segs[1][1].shift(LEFT * 0.4)
        head = VGroup(label(r"model", font_size=21, color=GREY_B), label(r"parameters", font_size=21, color=GREY_B),
                      label(r"what it sees", font_size=21, color=GREY_B))
        cells = [head]
        for k in r["names"]:
            cells.append(VGroup(label(k, font_size=23, color=MODEL_C[k]), MathTex(PARAMS[k], font_size=26,
                                                                                 color=MODEL_C[k]),
                                label(SEES[k], font_size=21, color=GREY_A)))
        tab = VGroup(*[m for row in cells for m in row]).arrange_in_grid(rows=len(cells), cols=3, buff=(0.7, 0.14),
                                                                        col_alignments="lrl")
        tab.next_to(segs, DOWN, buff=0.55).to_edge(LEFT, buff=0.8)
        side = VGroup(
            wrapped_label(r"Hansen and Lunde (2005) raced 330 ARCH-type models: none beat GARCH(1,1) on the "
                          r"Deutschmark--dollar rate; on IBM stock, models with leverage did", 4.4, 20, GREY_A),
            wrapped_label(r"each network: 5 seeds, early stopping on the validation half-year, forecasts averaged; "
                          r"trained here on a CPU in minutes", 4.4, 20, ALT),
            wrapped_label(r"the target: tomorrow's realized variance from 5-minute returns; the score: QLIKE", 4.4, 20,
                          VOL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).align_to(tab, UP)
        with self.voiceover(
            "In 2005 Peter Hansen and Asger Lunde asked a famous question: does anything beat a GARCH(1,1)? They raced "
            "three hundred and thirty models. On the Deutschmark-dollar exchange rate, nothing did; on IBM's stock, "
            "models with the leverage effect won. <bookmark mark='a'/> Here is our race. Every model is fitted on "
            "Bitcoin from August 2017 to June 2019. The second half of 2019 is held back, so the neural networks "
            "can choose when to stop training. All of 2020 is the test, untouched until the end. "
            "<bookmark mark='b'/> Seven contestants. RiskMetrics' exponential average, from 1994, with no fitted "
            "parameters. GARCH and GJR, which see only daily returns. HAR and HARQ, which see the realized variance. "
            "And two neural networks trained here: an LSTM with twelve hundred parameters and a small transformer "
            "with twenty-six hundred, each reading the last twenty-two days of log realized variance. Each network "
            "is trained from five random seeds, and the five forecasts are averaged. Everyone forecasts the same "
            "thing, tomorrow's realized variance, and is scored by QLIKE."
        ) as vo:
            self.play(FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in segs], lag_ratio=0.5, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*head)), LaggedStart(*[FadeIn(VGroup(*row)) for row in cells[1:]], lag_ratio=0.3,
                                                          run_time=5))
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def results(self, r):
        names = list(r["names"])
        sc = r["scores"]
        dm = r["dm_vs_har"]
        order = sorted(names, key=lambda k: sc[k]["qlike"])
        q = np.array([sc[k]["qlike"] for k in order])
        hi = float(np.ceil(q.max() * 10 + 0.5) / 10)
        g = axes([0, hi], [0, len(order)], x_length=6.6, y_length=4.8, xticks=list(np.round(np.linspace(0, hi, 5), 2)),
                 xfmt=lambda u: f"{u:.2f}", yticks=[], xlabel=r"QLIKE in 2020 (lower is better)", font_size=17)
        g.to_edge(LEFT, buff=2.2).shift(DOWN * 0.2)
        ax = g.ax
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        for i, k in enumerate(order):
            y = len(order) - i - 0.5
            left, right = ax.c2p(0, y), ax.c2p(sc[k]["qlike"], y)
            h = (ax.c2p(0, 0.62)[1] - ax.c2p(0, 0)[1])
            b = Rectangle(width=max(right[0] - left[0], 0.01), height=h, stroke_width=0, fill_color=MODEL_C[k],
                          fill_opacity=0.85).move_to((left + right) / 2)
            bars.add(b)
            labs.add(label(k, font_size=21, color=MODEL_C[k]).next_to(left, LEFT, buff=0.15))
            t = "" if k == "HAR" else rf"\ \ (t = {dm[k]['t']:+.1f})"
            vals.add(MathTex(f"{sc[k]['qlike']:.3f}" + t, font_size=22, color=GREY_A).next_to(b, RIGHT, buff=0.1))
        seeds = VGroup()
        for k in ("LSTM", "Transformer"):
            i = order.index(k)
            y = len(order) - i - 0.5
            for v in r["seed_qlike"][k]:
                seeds.add(Dot(ax.c2p(min(v, hi), y), radius=0.05, color=WHITE).set_opacity(0.8))
        best = order[0]
        nn_best = min(sc["LSTM"]["qlike"], sc["Transformer"]["qlike"])
        side = VGroup(
            wrapped_label(r"$t$: Diebold--Mariano against HAR, Newey--West variance; negative means better than HAR",
                          3.8, 19, GREY_A),
            wrapped_label(r"white dots: the five seeds of each network, scored one at a time", 3.8, 19, GREY_A),
            wrapped_label(r"models that see the intraday path (HAR, the networks) beat models that see only closes", 3.8,
                          20, VOL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            f"The results, over the {r['test_days']} days of 2020. Lower is better. <bookmark mark='a'/> The models "
            "that see only daily closes, the exponential average, GARCH and GJR, come last. <bookmark mark='b'/> "
            "The models that read the realized variance do much better. "
            f"{best} came first. Next to each bar is a Diebold-Mariano test against HAR: a t-statistic below minus "
            "two would mean a model beat HAR by more than luck. <bookmark mark='c'/> The white dots are the "
            "networks' individual seeds. They scatter; averaging five of them helps; and the averages "
            f"{'did not beat' if nn_best >= sc['HAR']['qlike'] else 'only matched'} four coefficients fitted by "
            "least squares. With a thousand days of training data, the network has nothing to find that HAR's three "
            "averages do not already hold."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs))
            vo.wait_until("a")
            slow = [i for i, k in enumerate(order) if k in ("EWMA", "GARCH", "GJR")]
            self.play(*[GrowFromEdge(bars[i], LEFT) for i in slow], *[FadeIn(vals[i]) for i in slow])
            vo.wait_until("b")
            fast = [i for i in range(len(order)) if i not in slow]
            self.play(*[GrowFromEdge(bars[i], LEFT) for i in fast], *[FadeIn(vals[i]) for i in fast])
            self.play(FadeIn(side[0]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(seeds), FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def year(self, r):
        t = np.asarray(r["test_t"])
        rv = np.asarray(r["test_rv"])
        har, gar = np.asarray(r["test_har"]), np.asarray(r["test_garch"])
        g = axes([2020, 2021], [0, 2.5], x_length=10.4, y_length=4.4,
                 xticks=[2020, 2020.25, 2020.5, 2020.75, 2021],
                 xfmt=lambda u: {0: "Jan", 1: "Apr", 2: "Jul", 3: "Oct", 4: "Jan"}[round((u - 2020) * 4)],
                 yticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 ylabel=r"Bitcoin's daily volatility in 2020, annualised", font_size=17).move_to(DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(tt, min(v, 2.5)), radius=0.03, color=BAD).set_opacity(0.7) for tt, v in zip(t, rv)])
        lg = curve(ax, t, np.clip(gar, 0, 2.5), FC, stroke_width=2.5)
        lh = curve(ax, t, np.clip(har, 0, 2.5), VOL, stroke_width=2.5)
        leg = legend([(BAD, r"realized"), (FC, r"GARCH, the day before"), (VOL, r"HAR, the day before")], font_size=19)
        leg.next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        src = real_data(r"Binance BTCUSDT one-minute candles; models fitted to June 2019, tested on 2020")
        with self.voiceover(
            "Here is the whole test year. Each dot is a day's realized volatility. GARCH, which sees only closing "
            "prices, follows slowly and overshoots after big days. <bookmark mark='a'/> HAR, reading the whole "
            "day's path, tracks the level more closely. Neither forecasts the spikes: no model can. The skill in "
            "volatility forecasting is the level, not the surprises."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.005,
                                                                       run_time=2))
            self.play(Create(lg), run_time=2)
            vo.wait_until("a")
            self.play(Create(lh), run_time=2)
        self.wait(0.4)
        self.clear_scene()
