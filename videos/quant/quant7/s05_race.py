from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data, tbar

MODEL_C = {"EWMA": GREY_B, "GARCH": FC, "GJR": FC, "HAR": VOL, "HARQ": VOL, "log-HAR": GOOD, "LSTM": ALT,
           "Transformer": ALT, "HARNet": RET}
PARAMS = {"EWMA": r"0", "GARCH": r"3", "GJR": r"4", "HAR": r"4", "HARQ": r"5", "log-HAR": r"4", "LSTM": r"1{,}233",
          "Transformer": r"2{,}625", "HARNet": r"111"}
SEES = {"EWMA": r"daily returns", "GARCH": r"daily returns", "GJR": r"daily returns, with sign",
        "HAR": r"realized variance", "HARQ": r"RV and its noise", "log-HAR": r"log of realized variance",
        "LSTM": r"22 days of log RV", "Transformer": r"22 days of log RV", "HARNet": r"22 days of log RV, starts at log-HAR"}
LATE = "log-HAR"  # added after the first results, and counted


class Race(VoiceoverScene):
    def construct(self):
        r = load("race")
        r2 = load("race2")
        self.card()
        self.contestants(r)
        self.board(r2)
        self.results(r)
        self.harnet(r2)
        self.calibration(r2)
        self.year(r)

    def card(self):
        c = chapter_card(14, r"The race", r"Does anything beat a GARCH(1,1)?", part=PART)
        with self.voiceover("Chapter fourteen. The race."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def contestants(self, r):
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
            if k == LATE:
                continue
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
            "Hansen and Lunde's question, asked of Bitcoin: does anything beat a GARCH(1,1)? On the Deutschmark-dollar "
            "rate, nothing did; on IBM's stock, models with the leverage effect won. <bookmark mark='a'/> Here is our "
            "race. Fit to June 2019, validate on the second half, test on all of 2020, untouched until the end. <bookmark mark='b'/> The first seven contestants. RiskMetrics' exponential average; GARCH and GJR, which see daily returns; HAR and HARQ, which see realized variance; and the two networks, five seeds averaged. "
            "Everyone forecasts the same thing, tomorrow's realized variance, and is scored by QLIKE."
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
        dm, dml = r["dm_vs_har"], r["dm_vs_loghar"]
        order = sorted(names, key=lambda k: sc[k]["qlike"])
        q = np.array([sc[k]["qlike"] for k in order])
        hi = float(np.ceil(q.max() * 10 + 0.5) / 10)
        g = axes([0, hi], [0, len(order)], x_length=6.0, y_length=5.0, xticks=list(np.round(np.linspace(0, hi, 4), 2)),
                 xfmt=lambda u: f"{u:.1f}", yticks=[], xlabel=r"QLIKE in 2020 (lower is better)", font_size=17)
        g.to_edge(LEFT, buff=1.9).shift(DOWN * 0.1)
        ax = g.ax
        bars, labs, vals = {}, {}, {}
        for i, k in enumerate(order):
            y = len(order) - i - 0.5
            left, right = ax.c2p(0, y), ax.c2p(sc[k]["qlike"], y)
            h = (ax.c2p(0, 0.62)[1] - ax.c2p(0, 0)[1])
            bars[k] = Rectangle(width=max(right[0] - left[0], 0.01), height=h, stroke_width=0, fill_color=MODEL_C[k],
                                fill_opacity=0.85).move_to((left + right) / 2)
            labs[k] = label(k, font_size=20, color=MODEL_C[k]).next_to(left, LEFT, buff=0.15)
            tv = 0.0 if k == "HAR" else dm[k]["t"]
            t = "" if k == "HAR" else (r"\ \ (t = 0.0)" if abs(tv) < 0.05 else rf"\ \ (t = {tv:+.1f})")
            edge = max([sc[k]["qlike"]] + list(r["seed_qlike"].get(k, [])))
            vals[k] = MathTex(f"{sc[k]['qlike']:.3f}" + t, font_size=21, color=GREY_A).next_to(ax.c2p(edge, y), RIGHT,
                                                                                                 buff=0.15)
        seeds = VGroup()
        for k in ("LSTM", "Transformer"):
            y = len(order) - order.index(k) - 0.5
            for v in r["seed_qlike"][k]:
                seeds.add(Dot(ax.c2p(min(v, hi), y), radius=0.05, color=WHITE).set_opacity(0.8))
        mse_order = sorted(names, key=lambda k: sc[k]["mse"])
        assert order[0] == LATE and dml["LSTM"]["t"] > 0, "the narration below describes this outcome"
        side = VGroup(
            wrapped_label(r"$t$: Diebold--Mariano against HAR (Newey--West variance); below $-2$ beats HAR by more than "
                          r"luck", 4.0, 19, GREY_A),
            wrapped_label(r"added after the first results, and counted: HAR on the log of realized variance, which is "
                          r"what the networks forecast", 4.0, 20, GOOD),
            MathTex(rf"\text{{LSTM against log-HAR: }} t = {dml['LSTM']['t']:+.1f}", font_size=26, color=ALT),
            wrapped_label(r"white dots: each network's five seeds, scored one at a time", 4.0, 19, GREY_A),
            wrapped_label(rf"on squared error the order changes: {mse_order[0]} first, {mse_order[-1]} last. The loss is "
                          r"a choice; QLIKE is the one that stays honest when the target is noisy.", 4.0, 19, VOL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        early = [k for k in order if k != LATE]
        closes = [k for k in early if k in ("EWMA", "GARCH", "GJR")]
        rest = [k for k in early if k not in closes]
        with self.voiceover(
            f"The results, over the {r['test_days']} days of 2020. Lower is better. <bookmark mark='a'/> The models "
            "that see only daily closes, the exponential average, GARCH and GJR, come last. <bookmark mark='b'/> The "
            "models that read the realized variance do better, and the two neural networks do better still. The "
            "LSTM beats HAR with a Diebold-Mariano t of minus three. Has it found something? "
            "<bookmark mark='c'/> Look at what it forecasts: the logarithm of realized variance, not the variance. "
            "Logs tame the spikes that dominate a least-squares fit. So, after seeing these results, we added one "
            "more contestant, and the trial counter counts it: HAR again, four coefficients, fitted to the logarithm. "
            f"<bookmark mark='d'/> It comes first. Against log-HAR, the LSTM's t-statistic is {dml['LSTM']['t']:.1f}, "
            "in log-HAR's favour: no evidence that the network adds anything beyond the log. <bookmark mark='e'/> White dots: single seeds."
            " <bookmark mark='f'/> And score the same forecasts by "
            f"squared error, and the order changes: {mse_order[0]} comes first. A race is only as honest as its "
            "loss function."
        ) as vo:
            self.play(FadeIn(g), *[FadeIn(labs[k]) for k in early], FadeIn(side[0]))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(bars[k], LEFT) for k in closes], *[FadeIn(vals[k]) for k in closes])
            vo.wait_until("b")
            self.play(*[GrowFromEdge(bars[k], LEFT) for k in rest], *[FadeIn(vals[k]) for k in rest])
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(labs[LATE]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[LATE], LEFT), FadeIn(vals[LATE]), FadeIn(side[2]))
            self.play(Indicate(labs[LATE], color=GOOD))
            vo.wait_until("e")
            self.play(FadeIn(seeds), FadeIn(side[3]))
            vo.wait_until("f")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def board(self, r2):
        names = list(r2["names"])
        cum = np.asarray(r2["cum"])
        ct = np.asarray(r2["cum_t"])
        i12 = int(r2["i12"])
        hi = 1.0
        x0, wmax = -2.6, 7.6
        k = ValueTracker(0)

        def bars():
            i = int(k.get_value())
            v = cum[i]
            order = np.argsort(v)
            g = VGroup()
            for rank, j in enumerate(order):
                y = 2.3 - rank * 0.55
                w = wmax * min(v[j], hi) / hi
                n_ = names[j]
                g.add(Rectangle(width=max(w, 0.02), height=0.4, stroke_width=0, fill_color=MODEL_C[n_], fill_opacity=0.85)
                      .move_to([x0 + w / 2, y, 0]),
                      label(n_, font_size=20, color=MODEL_C[n_]).next_to([x0, y, 0], LEFT, buff=0.15),
                      MathTex(f"{v[j]:.3f}", font_size=22, color=GREY_A).next_to([x0 + w, y, 0], RIGHT, buff=0.1))
            return g

        b = always_redraw(bars)
        date = always_redraw(lambda: label(rf"2020, day {1 + 2 * int(k.get_value())}: running mean QLIKE (lower is better)",
                                           font_size=22, color=GREY_A).to_edge(UP, buff=0.4))
        pc = pause_card(r"Which model leads before March?", width=4.2, font_size=20).to_corner(DR, buff=0.3)
        lead0 = names[int(np.argmin(cum[i12 - 1]))]
        lead1 = names[int(np.argmin(cum[-1]))]
        with self.voiceover(
            "Now run the test year, day by day. Each bar is a model's average QLIKE so far, and the bars re-sort as "
            f"the days go by. <bookmark mark='a'/> Through January and February the leader is {lead0}: in a calm market "
            "the simplest average is hard to beat. <bookmark mark='b'/> Then the twelfth of March. Every bar lurches, "
            "and the order is reshuffled in a single day. <bookmark mark='c'/> By December the models that read the "
            f"log of realized variance are in front, and {lead1} finishes first, by a whisker."
        ) as vo:
            self.add(b, date)
            self.play(FadeIn(pc))
            vo.wait_until("a")
            self.play(k.animate.set_value(i12 - 1), run_time=max(vo.until("b") - 0.2, 3), rate_func=linear)
            self.play(FadeOut(pc), k.animate.set_value(i12 + 1), run_time=1.0)
            vo.wait_until("c")
            self.play(k.animate.set_value(len(ct) - 1), run_time=max(vo.remaining(1.0) - 0.3, 3), rate_func=linear)
        b.clear_updaters()
        date.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def harnet(self, r2):
        sc, dm, mz = r2["scores"], r2["dm_vs_loghar"], r2["mz"]
        t = dm["HARNet"]["t"]
        rows = VGroup(*[MathTex(rf"\text{{{n_}}}:\ {sc[n_]['qlike']:.4f}" + ("" if n_ == "log-HAR" else
                                rf"\ \ (t = {dm[n_]['t']:+.2f}\text{{ against log-HAR}})"), font_size=30, color=MODEL_C[n_])
                        for n_ in ("HARNet", "log-HAR", "LSTM")]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rows.move_to(UP * 1.2)
        mcs = r2["mcs"]
        side = VGroup(
            label(r"Mincer--Zarnowitz slope $b$ (ideal 1): " + ", ".join(rf"{n_} {mz[n_]['b']:.2f}"
                                                                     for n_ in ("HAR", "log-HAR", "HARNet", "GARCH")),
                  font_size=21, color=GREY_A),
            label(rf"model confidence set at 90\%: {len(mcs['survivors'])} of {len(r2['names'])} survive", font_size=21,
                  color=YELLOW),
            label(r"HARNet was registered with the trial counter before it was scored", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(rows, DOWN, buff=0.6)
        if -2 < t < 0:
            verdict = (f"By the smallest of margins, and well within noise: the Diebold-Mariano statistic is {t:.1f}. "
                       "The network found nothing beyond the log.")
        elif t <= -2:
            verdict = "It beats log-HAR by more than luck: the network found something beyond the log."
        else:
            verdict = "It does not beat log-HAR."
        mcs_line = ("As the last chapter warned, it keeps every model: one year cannot crown a winner." if len(mcs["survivors"]) == len(r2["names"]) else
                    "It narrows the field, but keeps several models.")
        with self.voiceover(
            f"And the late entrant, HARNet, which started life as log-HAR. <bookmark mark='a'/> Does it beat its own starting "
            f"point? {verdict} And the confidence set? {mcs_line}"
        ) as vo:
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    def year(self, r):
        t = np.asarray(r["test_t"])
        rv = np.asarray(r["test_rv"])
        har, gar = np.asarray(r["test_loghar"]), np.asarray(r["test_garch"])
        g = axes([2020, 2021], [0, 2.5], x_length=10.4, y_length=4.4,
                 xticks=[2020, 2020.25, 2020.5, 2020.75, 2021],
                 xfmt=lambda u: {0: "Jan", 1: "Apr", 2: "Jul", 3: "Oct", 4: "Jan"}[round((u - 2020) * 4)],
                 yticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 ylabel=r"Bitcoin's daily volatility in 2020, annualised", font_size=17).move_to(DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(tt, min(v, 2.5)), radius=0.03, color=BAD).set_opacity(0.7) for tt, v in zip(t, rv)])
        lg = curve(ax, t, np.clip(gar, 0, 2.5), FC, stroke_width=2.5)
        lh = curve(ax, t, np.clip(har, 0, 2.5), GOOD, stroke_width=2.5)
        leg = legend([(BAD, r"realized"), (FC, r"GARCH, the day before"), (GOOD, r"log-HAR, the day before")], font_size=19)
        leg.next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        src = real_data(r"Binance BTCUSDT one-minute candles; models fitted to June 2019, tested on 2020")
        with self.voiceover(
            "Here is the whole test year. Each dot is a day's realized volatility. GARCH, which sees only closing "
            "prices, follows slowly and overshoots after big days. <bookmark mark='a'/> Log-HAR, reading the whole "
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

    def calibration(self, r2):
        names = list(r2["names"])
        mz = r2["mz"]
        g = axes([0, len(names)], [0, 1.6], x_length=9.0, y_length=3.8, xticks=[], yticks=[0, 0.5, 1.0, 1.5],
                 ylabel=r"Mincer--Zarnowitz slope $b$ in $RV_t = a + b\,\hat h_t$, 2020 (ideal: 1)", font_size=16)
        g.move_to(DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[tbar(ax, i + 0.5, mz[k]["b"], MODEL_C[k], width=0.6) for i, k in enumerate(names)])
        labs = VGroup(*[label(k, font_size=16, color=GREY_A).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.1)
                        for i, k in enumerate(names)])
        one = DashedLine(ax.c2p(0, 1), ax.c2p(len(names), 1), color=GOOD, stroke_width=3)
        best_cal = min(names, key=lambda k: abs(mz[k]["b"] - 1))
        with self.voiceover(
            "One more check on the race: calibration. Regress each day's realized variance on the forecast. A "
            "calibrated forecast has a slope of one. <bookmark mark='a'/> The best calibrated is "
            f"{best_cal}, with a slope of {mz[best_cal]['b']:.2f}. The models built on logarithms, which win on "
            f"QLIKE, have slopes near {mz['log-HAR']['b']:.1f}: on the big days realized variance moves more than "
            "they predicted. A desk would fix that with a one-line recalibration, the same correction Brini found "
            "erased much of the foundation models' edge. Ranking and calibration are different questions, and an "
            "honest report answers both."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), Create(one))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1))
        self.wait(0.3)
        self.clear_scene()
