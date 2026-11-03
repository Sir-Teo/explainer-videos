from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data

# Brini (2026), arXiv 2607.05291, Table 6: average QLIKE loss ratio to log-HAR over 50 assets, one day ahead (h = 1).
# Data from the paper (below 1 beats log-HAR); read on arxiv.org/html/2607.05291, November 2026.
BRINI_H1 = [("TTM", 0.982, True), ("HAR", 0.998, False), ("Sundial", 0.998, True), ("log-HAR", 1.000, False),
            ("ARMA", 1.000, False), ("Moirai-2.0-S", 1.038, True), ("TimesFM-2.5", 1.086, True),
            ("Moirai-MoE-S", 1.090, True), ("Chronos-Bolt-S", 1.110, True), ("Chronos-Bolt-B", 1.121, True),
            ("Toto", 1.214, True), ("Lag-Llama", 1.532, True)]

PAPERS = [
    (r"Ansari et al.\ (2024), Chronos, TMLR", r"values scaled and binned into tokens; a language model over them"),
    (r"Das et al.\ (2024), TimesFM, ICML; Woo et al.\ (2024), Moirai, ICML", r"decoder and masked-encoder foundation models"),
    (r"Ekambaram et al.\ (2024), TTM, NeurIPS", r"tiny time mixers: about a million parameters, runs on a CPU"),
    (r"Christensen, Siggaard and Veliyev (2023), JFEc", r"machine learning against HAR on the Dow's stocks: ML helps one day ahead"),
    (r"Zhang, Zhang, Cucuringu and Qian (2022), arXiv", r"networks pooled across stocks generalise to unseen ones"),
    (r"Reisenhofer, Bayer and Hautsch (2022), arXiv", r"HARNet: beats HAR on indices; yesterday dominates the filter"),
    (r"Goel, Pasricha, Magris and Kanniainen (2025), arXiv", r"TimesFM zero-shot is a reasonable baseline; fine-tuning is essential"),
    (r"Rahimikia, Ni and Wang (2025), arXiv", r"off-the-shelf models lag on daily returns; finance pretraining helps"),
    (r"Shi et al.\ (2025), Kronos, arXiv", r"pretrained on candlesticks from 45 exchanges; its own volatility benchmark"),
    (r"Ansari et al.\ (2025), Chronos-2, arXiv", r"group attention: many series and covariates at once"),
]


class Frontier(VoiceoverScene):
    def construct(self):
        f = load("foundation")
        self.card()
        self.tokens(f)
        self.pretrain(f)
        self.zero_shot(f)
        self.brini()
        self.papers()

    def card(self):
        c = chapter_card(15, r"Foundation models and the frontier", r"Can a model that never saw Bitcoin forecast it?",
                         lit=(2025,), part=PART)
        with self.voiceover("Chapter fifteen. Foundation models, and the frontier."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def tokens(self, f):
        ctx = np.asarray(f["ctx"])
        tk = np.asarray(f["ctx_tokens"])
        C = len(ctx)
        s = float(np.mean(np.abs(ctx)))
        g = axes([-0.5, C - 0.5], [0, float(ctx.max()) * 1.1], x_length=0.15 * C, y_length=2.6, xticks=[], yticks=[], font_size=14,
                 ylabel=r"Bitcoin's daily volatility, the 64 days before 13 March 2020")
        g.to_corner(UL, buff=0.4)
        dots = VGroup(*[Dot(g.ax.c2p(i, v), radius=0.04, color=RET) for i, v in enumerate(ctx)])
        nb = int(f["bins"])
        ladder_ = VGroup(*[Rectangle(width=0.5, height=4.6 / 32, stroke_width=0,
                                     fill_color=interpolate_color(ManimColor(VOL), ManimColor(BAD), k / 31), fill_opacity=0.9)
                           for k in range(32)]).arrange(UP, buff=0.0).to_edge(RIGHT, buff=1.5).shift(DOWN * 0.2)
        lt = wrapped_label(rf"{nb} bins on $[0, 4]$ after scaling (32 drawn)", 2.6, 17, GREY_A).next_to(ladder_, UP, buff=0.15)
        # each day's token sits directly under that day's dot
        y_strip = g.ax.c2p(0, 0)[1] - 0.75
        strip = VGroup(*[Square(side_length=0.15, stroke_width=0.5, stroke_color=BACKGROUND,
                                fill_color=interpolate_color(ManimColor(VOL), ManimColor(BAD), min(t_ / (nb - 1) * 1.0, 1.0)),
                                fill_opacity=0.95).move_to([g.ax.c2p(i, 0)[0], y_strip, 0]) for i, t_ in enumerate(tk)])
        nums = MathTex(r"\text{tokens: }" + r",\,".join(str(int(t_)) for t_ in tk[-8:]), font_size=22, color=GREY_A)
        nums.next_to(strip, DOWN, buff=0.15).align_to(strip, LEFT)
        rows = VGroup(
            MathTex(r"\tilde x = x / s,\quad s = \tfrac1C\textstyle\sum|x_i|,\quad \text{token} = \operatorname{bin}(\tilde x)",
                    font_size=28),
            MathTex(r"\hat p(\text{token}_{t+1}\mid \text{tokens}_{t-C+1:t}),\ \text{trained by cross-entropy}", font_size=28),
            MathTex(r"\text{zero-shot: } \hat y_{t+1} = f_\theta(x_{t-C+1:t}),\ \theta\text{ frozen}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        with self.voiceover(
            "Since 2024, foundation models promise to forecast any time series without training on it. Chronos, from "
            "Abdul Fatir Ansari and colleagues at Amazon, shows the idea: turn numbers into a language. <bookmark mark='a'/> Take a window of the series, here Bitcoin's daily volatility before "
            "the crash, and divide by its average size, so every series lives on the same scale. <bookmark mark='b'/> "
            "Cut the scaled range into bins, and each day becomes a token, one of a fixed vocabulary. The series is now "
            "a sentence. <bookmark mark='c'/> A transformer is trained, on a huge corpus of other series, to predict "
            "the next token, exactly as a language model predicts the next word. Its output is a probability for every "
            "bin: a whole forecast distribution."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.02, run_time=1.5))
            vo.wait_until("a")
            sline = DashedLine(g.ax.c2p(0, s), g.ax.c2p(C, s), color=GREY_B, stroke_width=2)
            self.play(Create(sline), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(ladder_), FadeIn(lt))
            self.play(LaggedStart(*[FadeIn(q_) for q_ in strip], lag_ratio=0.02, run_time=2), FadeIn(nums))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
        self.wait(0.3)
        self.clear_scene()

    def pretrain(self, f):
        steps = np.asarray(f["loss_steps"], float)
        L = np.asarray(f["loss"], float)
        cen = np.asarray(f["centers"])
        snaps = f["snaps"]
        ck = list(f["ckpts"])
        keys = [str(k) for k in ck]
        true = f["next_true"]

        def frame(i):
            k = keys[min(i, len(keys) - 1)]
            p = np.asarray(snaps[k]["p"])
            sc = snaps[k]["s"]
            x = cen * sc
            g = axes([0, 0.15], [0, max(float(p.max()) * 1.15, 0.05)], x_length=4.8, y_length=3.0, xticks=[0, 0.05, 0.10, 0.15],
                     xfmt=lambda v: f"{100 * v * np.sqrt(365):.0f}\\%" if v else "0", yticks=[], font_size=13,
                     ylabel=rf"forecast for 13 March 2020 after {int(k):,} steps".replace(",", "{,}"))
            bars = VGroup(*[Line(g.ax.c2p(a, 0), g.ax.c2p(a, b), stroke_width=2, color=VOL) for a, b in zip(x, p) if a <= 0.15])
            tl = DashedLine(g.ax.c2p(min(true, 0.15), 0), g.ax.c2p(min(true, 0.15), float(p.max()) * 1.1), color=BAD, stroke_width=3)
            return VGroup(g, bars, tl)

        sstep = [int(np.argmin(np.abs(steps - c))) for c in ck]
        rp = TrainingReplay(steps, L, frame, checkpoints=[float(steps[j]) for j in sstep], ylabel=r"cross-entropy (3 seeds)",
                            xlabel=r"pretraining step, synthetic series only", color=VOL)
        rp.to_edge(UP, buff=0.7)
        cap = label(rf"our toy: {f['n_series']:,} synthetic volatility series, never a market; {f['n_params']:,} parameters; "
                    rf"context {f['context']} days".replace(",", "{,}"), font_size=18, color=GREY_B).to_edge(DOWN, buff=0.5)
        red = label(r"red: what happened on 13 March", font_size=18, color=BAD).next_to(cap, UP, buff=0.15)
        with self.voiceover(
            "The published models are not installed here, so the House built a toy one the same way, small enough "
            "for an ordinary processor. Its corpus is synthetic volatility series from four families, with random "
            "parameters. It never sees a market. <bookmark mark='a'/> Watch it learn, three seeds. On the left, its forecast distribution for the "
            "thirteenth of March 2020, the day after the crash, read from the sixty-four days before it, at each "
            "checkpoint. At first, a smear across all bins. Then it learns that volatility clusters: the mass moves "
            "toward the recent level, and a right tail grows."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(cap), FadeIn(red))
            vo.wait_until("a")
            rp.play(self, run_time=7)
        self.wait(0.3)
        self.clear_scene()

    def zero_shot(self, f):
        t = np.asarray(f["test_t"])
        k = 365 ** 0.5
        v, q1, q5, q9 = (np.asarray(f[x]) * k for x in ("test_v", "q10", "q50", "q90"))
        g = axes([2020, 2021], [0, 2.5], x_length=8.0, y_length=3.6, xticks=[2020, 2020.25, 2020.5, 2020.75, 2021],
                 xfmt=lambda u: {0: "Jan", 1: "Apr", 2: "Jul", 3: "Oct", 4: "Jan"}[round((u - 2020) * 4)],
                 yticks=[0, 1, 2], yfmt=lambda u: f"{100 * u:.0f}\\%", ylabel=r"Bitcoin 2020: the toy model's 10--90\% fan, a day ahead",
                 font_size=15).to_edge(UP, buff=0.6).to_edge(LEFT, buff=0.5)
        tr = ValueTracker(1)
        fan = always_redraw(lambda: band(g.ax, t[:int(tr.get_value()) + 1], np.clip(q1[:int(tr.get_value()) + 1], 0, 2.5),
                                         np.clip(q9[:int(tr.get_value()) + 1], 0, 2.5), VOL, 0.35))
        med = tracing(g.ax, t, np.clip(q5, 0, 2.5), tr, VOL, stroke_width=2)
        dots = always_redraw(lambda: VGroup(*[Dot(g.ax.c2p(a, min(b, 2.5)), radius=0.025, color=RET)
                                               for a, b in zip(t[:int(tr.get_value()) + 1], v[:int(tr.get_value()) + 1])]))
        dm = f["dm_vs_loghar"]
        res = VGroup(
            MathTex(rf"\text{{QLIKE, 2020: toy model }} {f['qlike']:.3f},\ \text{{log-HAR }} {f['qlike_loghar']:.3f}", font_size=28),
            MathTex(rf"\text{{Diebold--Mariano against log-HAR: }} t = {dm['t']:+.1f}", font_size=28,
                    color=GOOD if dm["t"] < -2 else (BAD if dm["t"] > 2 else GREY_A)),
            MathTex(rf"\text{{seeds: }}" + r",\ ".join(f"{q:.3f}" for q in f["seed_qlike"]) +
                    rf";\ \ \text{{inside the 80\% fan: }}{100 * f['cover80']:.0f}\%\text{{ of days}}", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(g, DOWN, buff=0.4).align_to(g, LEFT)
        pc = pause_card(r"A model trained on synthetic series, never on Bitcoin: better or worse than four least-squares "
                        r"coefficients?", width=4.6, font_size=20).to_corner(UR, buff=0.3)
        tt = dm["t"]
        if tt < -2:
            verdict = "It wins, by more than luck. Structure learned from synthetic series transfers."
        elif tt < 0:
            verdict = f"Slightly better, but within noise: the Diebold-Mariano statistic is {tt:.1f}."
        elif tt <= 2:
            verdict = (f"Worse, though one year cannot make the gap significant: the statistic is {tt:.1f}. It lands "
                       "between HAR and the transformer: a model that never saw Bitcoin is as good as HAR in levels, "
                       "but not as good as log-HAR.")
        else:
            verdict = "Worse, by more than luck. Four coefficients fitted to Bitcoin itself still win."
        with self.voiceover(
            f"Pause and predict: a model trained only on synthetic series, against four least-squares coefficients fitted "
            f"to Bitcoin itself. Better or worse? <bookmark mark='a'/> Point the frozen model at 2020, one day at a time. "
            f"The fan is its ten-to-ninety percent forecast band; the dots are what happened. <bookmark mark='b'/> Its "
            f"QLIKE is {f['qlike']:.3f}, against log-HAR's {f['qlike_loghar']:.3f}. {verdict} And its fan contains the "
            f"outcome on {100 * f['cover80']:.0f} percent of days, against eighty promised."
        ) as vo:
            self.play(FadeIn(pc), FadeIn(g))
            vo.wait_until("a")
            self.add(fan, med, dots)
            self.play(tr.animate.set_value(len(t) - 1), run_time=max(vo.until("b") - 0.3, 3), rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(res))
        for m in (fan, dots):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def brini(self):
        rows = sorted(BRINI_H1, key=lambda r_: r_[1])
        g = axes([0.9, 1.6], [0, len(rows)], x_length=6.0, y_length=4.8, xticks=[0.9, 1.0, 1.2, 1.4, 1.6], yticks=[],
                 xfmt=lambda v: f"{v:.1f}", xlabel=r"QLIKE relative to log-HAR, one day ahead (lower is better)",
                 font_size=15).to_edge(LEFT, buff=2.4).shift(DOWN * 0.2)
        ax = g.ax
        bars, labs = VGroup(), VGroup()
        for i, (n_, v, fm) in enumerate(rows):
            y = len(rows) - i - 0.5
            l_, r_ = ax.c2p(0.9, y), ax.c2p(v, y)
            col = VOL if fm else GREY_B
            bars.add(Rectangle(width=max(r_[0] - l_[0], 0.02), height=ax.c2p(0, 0.6)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                               fill_color=col, fill_opacity=0.85).move_to((l_ + r_) / 2))
            labs.add(VGroup(label(n_, font_size=17, color=col), MathTex(f"{v:.3f}", font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.15)
                     .next_to(l_, LEFT, buff=0.1))
        one = DashedLine(ax.c2p(1.0, 0), ax.c2p(1.0, len(rows)), color=GOOD, stroke_width=3)
        side = VGroup(
            label(r"Brini (2026), arXiv 2607.05291, Table 6:", font_size=19, color=GREY_A),
            wrapped_label(r"9 foundation models zero-shot (blue) against 8 econometric models (grey) on 50 equities, FX "
                          r"rates and futures; average loss ratio to log-HAR", 4.0, 17, GREY_A),
            wrapped_label(r"only TTM beats log-HAR at every horizon, narrowly; a Mincer--Zarnowitz recalibration removes "
                          r"much of the short-horizon edge; the TTM + log-HAR average enters the model confidence set for "
                          r"98--100\% of assets", 4.0, 17, GOOD),
            label(r"data from the paper; not run here", font_size=16, color=GREY_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "What do the real models do? Alessio Brini's comparison of July 2026 ran nine foundation models zero-shot against eight econometric ones on fifty assets. Here is one row of his "
            "results, the day-ahead loss of each model relative to log-HAR, averaged over assets, as published. "
            "<bookmark mark='a'/> Only IBM's Tiny Time Mixers, a model of about a million parameters, beats log-HAR, "
            "and narrowly. Chronos-Bolt and TimesFM are about nine to twelve percent worse. <bookmark mark='b'/> Much of the edge that "
            "remains disappears after a Mincer-Zarnowitz recalibration, and the best forecast is an average of TTM and "
            "log-HAR. His conclusion: the choice of architecture matters more than the choice between foundation and "
            "econometric models. And a pretrained corpus may contain the test years."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[3]))
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.08), Create(one))
            vo.wait_until("a")
            self.play(Indicate(labs[0], color=VOL))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    def papers(self):
        rows = VGroup(*[VGroup(label(a, font_size=19, color=QC.IDEA), label(b, font_size=17, color=GREY_A))
                        .arrange(DOWN, aligned_edge=LEFT, buff=0.04) for a, b in PAPERS])
        rows.arrange_in_grid(rows=5, cols=2, buff=(0.5, 0.28), col_alignments="ll").move_to(DOWN * 0.2)
        if rows.width > 13.4:
            rows.scale_to_fit_width(13.4)
        head = label(r"The 2022--2026 frontier, checked against the papers", font_size=30).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The frontier in one screen: the foundation models of 2024 and 2025, and the volatility papers. Machine "
            "learning helps HAR one day ahead on the Dow's stocks; networks pooled across stocks generalise. <bookmark "
            "mark='a'/> In finance, TimesFM needs fine-tuning, pretraining on financial data helps, and Kronos reports "
            "gains on its own benchmark. The honest summary: on volatility, log-HAR is still the bar to clear."
            " Every model here was scored over calm and stormy days alike. Next, the stormiest: March 2020."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_) for r_ in rows[:6]], lag_ratio=0.3, run_time=4))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[6:]], lag_ratio=0.3, run_time=3))
        self.wait(0.3)
        self.clear_scene()
