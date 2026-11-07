from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, pause, real_data


class Frontier(VoiceoverScene):
    def construct(self):
        f = load_ml()
        self.card()
        self.setup_(f)
        self.replay(f)
        self.verdict(f)
        self.papers()

    def card(self):
        c = chapter_card(18, r"Frontier: learning to trade options", r"What can a model learn from 96 weeks?",
                         lit=(2019, 2025), part=PART)
        with self.voiceover("Chapter eighteen. The frontier: learning to trade options."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def setup_(self, f):
        feats = VGroup(
            label(r"the target: next four weeks' hedged straddle P\&L (chapter 6)", font_size=24, color=OPT),
            label(r"four historical features; quote availability at entry is not established:", font_size=22, color=GREY_A),
            label(r"$\cdot$ implied minus the HAR forecast (chapter 7)", font_size=21, color=VEGA),
            label(r"$\cdot$ implied minus the last 30 days' realized", font_size=21, color=VEGA),
            label(r"$\cdot$ the 25-delta risk reversal (chapter 4)", font_size=21, color=ALT),
            label(r"$\cdot$ the term slope, 7-day minus 60-day implied", font_size=21, color=ALT),
            label(r"two models: ridge regression, and boosted depth-2 trees", font_size=22, color=GAMMA),
            label(r"walk-forward: refit every week on the past only, with a four-week gap", font_size=22, color=GAMMA),
            label(rf"existing logged specification; as-of-part trial counter {f['trials']}", font_size=22,
                  color=QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(ORIGIN)
        with self.voiceover(
            f"""Try a historical walk-forward replay before discussing the papers. The target is the next four weeks' hypothetical hedged straddle P&L, starting each Wednesday. <bookmark mark='a'/> Four inputs describe IV minus HAR, IV minus trailing realized volatility, the risk reversal and the term slope. The smile is reconstructed from a day's records; availability of all its inputs at the eight a.m. entry is not established. <bookmark mark='b'/> Ridge and depth-two boosted trees refit on earlier labels with a four-week gap. That gap addresses overlapping outcomes; it does not repair quote timing or certify a tradable backtest. <bookmark mark='c'/> The code specification is in the existing registry, with as-of-part counter {f['trials']}; the record does not establish that registration preceded calculation. We preserve the original replay and its limitations."""
        ) as vo:
            self.play(FadeIn(feats[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in feats[1:6]], lag_ratio=0.3, run_time=2.5))
            vo.wait_until("b")
            self.play(FadeIn(feats[6]), FadeIn(feats[7]))
            vo.wait_until("c")
            self.play(FadeIn(feats[8]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self, f):
        w = np.asarray(f["weeks"], float)
        y = np.asarray(f["y"])
        pr, pb = np.asarray(f["pred ridge"]), np.asarray(f["pred boost"])
        br, bb = np.asarray(f["band ridge"]), np.asarray(f["band boost"])
        lim = max(8.0, float(np.ceil(1.1 * max(np.abs(v).max() for v in (y, pr, pb, br, bb)))))
        g1 = axes([w[0], w[-1]], [-lim, lim], x_length=6.2, y_length=3.6, xlabel=r"week",
                  ylabel=r"hedged straddle P\&L, per 100", xticks=[int(w[0]), 60, int(w[-1])], yticks=[-5, 0, 5],
                  font_size=15).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        cm = {k: np.asarray(f[f"cmse {k}"]) for k in ("ridge", "boost", "mean")}
        top = float(max(v.max() for v in cm.values())) * 1.1
        g2 = axes([w[0], w[-1]], [0, top], x_length=4.6, y_length=3.0, xlabel=r"week",
                  ylabel=r"out-of-sample mean squared error", xticks=[int(w[0]), int(w[-1])], yticks=[0, round(top / 2)],
                  font_size=15).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        tr = ValueTracker(1.0)
        z = DashedLine(g1.ax.c2p(w[0], 0), g1.ax.c2p(w[-1], 0), color=GREY_C, stroke_width=1)

        def bands():
            n = max(int(tr.get_value()), 2)
            return VGroup(band(g1.ax, w[:n], np.clip(br.min(0)[:n], -lim, lim), np.clip(br.max(0)[:n], -lim, lim), VEGA, 0.25),
                          band(g1.ax, w[:n], np.clip(bb.min(0)[:n], -lim, lim), np.clip(bb.max(0)[:n], -lim, lim), GAMMA, 0.2))
        B = always_redraw(bands)
        ly = tracing(g1.ax, w, np.clip(y, -lim, lim), tr, WHITE, stroke_width=2)
        lr = tracing(g1.ax, w, np.clip(pr, -lim, lim), tr, VEGA, stroke_width=3)
        lb = tracing(g1.ax, w, np.clip(pb, -lim, lim), tr, GAMMA, stroke_width=3)
        c1 = tracing(g2.ax, w, np.clip(cm["ridge"], 0, top), tr, VEGA, stroke_width=3)
        c2 = tracing(g2.ax, w, np.clip(cm["boost"], 0, top), tr, GAMMA, stroke_width=3)
        c3 = tracing(g2.ax, w, np.clip(cm["mean"], 0, top), tr, GREY_B, stroke_width=2)
        leg = legend([(WHITE, r"what happened"), (VEGA, r"ridge (band: 5 bootstrap refits)"),
                      (GAMMA, r"boosted trees"), (GREY_B, r"the past average, as a forecast")], font_size=16).to_corner(
            UR, buff=0.3)
        src = real_data(rf"{f['n_oos']} out-of-sample weeks, 2024--2025; features from Part 12's smiles and Binance")
        with self.voiceover(
            "Watch it run. Each week, both models are refitted on the past and make one prediction, with a band from five bootstrap refits of the training set. The white line is what happened. On the right, the running out-of-sample error of each, against the simplest forecast of all: the past average. <bookmark mark='a'/> The predictions hug a slightly negative level and barely move, while the outcomes swing far on both sides of them. The bands are the minimum and maximum of five ordinary bootstrap refits, not confidence or prediction intervals; overlapping weeks require dependence-aware inference. All recorded outcomes, predictions and running errors remain on their full scales."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), Create(z), FadeIn(leg), FadeIn(src))
            self.add(B, ly, lr, lb, c1, c2, c3)
            self.play(tr.animate.set_value(len(w) - 1), run_time=max(vo.remaining(1.0) - 0.5, 4.0), rate_func=linear)
        B.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verdict(self, f):
        rows = VGroup(
            label(r"out of sample:", font_size=24, color=GREY_A),
            label(rf"ridge: correlation with the outcome {f['corr ridge']:+.2f}", font_size=24, color=VEGA),
            label(rf"boosted trees: correlation {f['corr boost']:+.2f}, $R^2$ {f['r2 boost']:+.2f}", font_size=24,
                  color=GAMMA),
            label(r"as a rule, sell only when the model predicts a loss for the buyer:", font_size=22, color=GREY_A),
            label(rf"ridge {f['trade ridge']:+.2f} per week ($t = {f['t ridge']:.1f}$); boosted {f['trade boost']:+.2f} "
                  rf"($t = {f['t boost']:.1f}$)", font_size=22, color=OPT),
            label(rf"always sell: {f['trade always']:+.2f} ($t = {f['t always']:.1f}$); chapter 7's single signal: "
                  rf"{f['trade signal']:+.2f}", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(UP, buff=0.6)
        same = abs(f["trade ridge"] - f["trade always"]) < 0.05
        flat = max(abs(f["corr ridge"]), abs(f["corr boost"])) < 0.15
        if flat and same:
            say = ("Neither model can tell a good week from a bad one: their correlations with the outcome are about "
                   "zero. What they learned is the one thing the data does show, that buyers of volatility lose on "
                   "average, so they say sell almost every week, and earn what always selling earns. The premium "
                   "survives; the timing does not.")
        elif flat:
            say = ("Neither model can tell a good week from a bad one: their correlations with the outcome are about "
                   "zero, and what they earn is the premium, not timing.")
        else:
            say = "The models show some timing ability, which a second sample would have to confirm."
        foot = wrapped_label(r"96 overlapping weeks of one asset is a tiny sample: Bali, Beckmeyer, M\"orke and Weigert "
                             r"had 12 million observations", 7.4, 21, ALT).to_edge(DOWN, buff=0.6).to_edge(LEFT, buff=0.6)  # left of the corner card
        pc = pause(r"A model finds $t = 3$ after 40 tries. What is its deflated $t$?", width=4.6, font_size=20, corner=DR)
        with self.voiceover(
            f"The verdict. {say} <bookmark mark='a'/> That is the honest expectation with ninety-six overlapping "
            "weeks of one asset, and it is why the frontier papers use millions of observations. Pause and predict, "
            "Part twenty-six's lesson: a model that finds a t of three after forty tries; what is it really worth? "
            "Far less, once you deflate for the tries."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(foot), FadeIn(pc))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def papers(self):
        cards = VGroup(
            theorem_card(r"Bali, Beckmeyer, M\"orke, Weigert (2023)", r"Nonlinear machine learning on 265 option- and "
                         r"stock-based characteristics, 12 million observations 1996--2020, predicts delta-hedged equity "
                         r"option returns; long--short portfolios profit after costs. Option-based characteristics "
                         r"matter most.", who=r"\textit{Option return predictability with machine learning and big "
                         r"data}, RFS", color=QC.IDEA, width=6.3, font_size=18),
            theorem_card(r"Cao, Chen, Farghadani, Hull, Poulos, Wang, Yuan (2023)", r"Distributional reinforcement "
                         r"learning hedges gamma and vega with a second option under transaction costs and stochastic "
                         r"volatility: chapter 10's problem, learned.", who=r"\textit{Gamma and vega hedging using deep "
                         r"distributional reinforcement learning}, Frontiers in AI", color=QC.IDEA, width=6.3,
                         font_size=18),
            theorem_card(r"Baldacci, Bergault, Gu\'eant (2021); Fang and Xu (2023)", r"Optimal market making in many "
                         r"options, reduced to a few risk factors; and reinforcement learning that sets spreads across "
                         r"strikes and expiries: chapter 9, at scale.", who=r"\textit{Algorithmic market making for "
                         r"options}, QF; \textit{Option market making via reinforcement learning}, arXiv",
                         color=QC.IDEA, width=6.3, font_size=18),
            theorem_card(r"Pointers", r"Deep hedging and learned no-trade bands: Part 17. Same-day options, dealer gamma "
                         r"and machine-learned surfaces: Part 12. Retail flow and the wholesalers: chapter 17.",
                         color=GREY_B, width=6.3, font_size=18),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3)).move_to(ORIGIN)
        if cards.width > 13.2:
            cards.scale_to_fit_width(13.2)
        if cards.height > 7.2:
            cards.scale_to_fit_height(7.2)
        with self.voiceover(
            "What the frontier has. Turan Bali, Heiner Beckmeyer, Mathis Mörke and Florian Weigert trained nonlinear "
            "models on two hundred and sixty-five characteristics and twelve million observations from "
            "1996 to 2020: they predict delta-hedged equity option returns well enough for long-short portfolios to "
            "profit after costs, and the option-based characteristics matter most. <bookmark mark='a'/> Jay Cao, John "
            "Hull and their coauthors used distributional reinforcement learning to hedge gamma and vega with a second "
            "option under costs: chapter ten's problem, learned. <bookmark mark='b'/> Baldacci, Bergault and Guéant "
            "made market making in many options tractable by reducing it to a few risk factors, and Zhou Fang and "
            "Haiqing Xu trained a reinforcement learner to set spreads across strikes and expiries: chapter nine, at "
            "scale. <bookmark mark='c'/> Deep hedging is Part seventeen; same-day "
            "options, Part twelve."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[3], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()


def load_ml():
    from videos.quant.quant11.common import load
    return load("frontier_ml")
