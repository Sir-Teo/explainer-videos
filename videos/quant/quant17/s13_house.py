from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import axes, data_range
import numpy as np

from videos.quant.quant17.common import BAD, GOOD, NET, PART, REF, load

TEST_NAMES = {"GBM": r"GBM", "GJR-GARCH": r"GJR-GARCH fitted to BTC", "BTC history": r"BTC history, 2017--2025"}
HEDGER_NAMES = {"delta daily": r"delta, daily", "Whalley--Wilmott": r"Whalley--Wilmott", "net (GBM-trained)":
                r"network trained on GBM", "net (GARCH-trained)": r"network trained on GARCH"}


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.crossgen(load("crossgen"))
        self.module(env)

    def card(self):
        c = chapter_card(19, r"Rule 17, tested", r"Is a hedger better than the simulator it was trained on?", part=PART)
        with self.voiceover("Chapter nineteen. The House's rule seventeen, tested."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def crossgen(self, cg):
        T, tests, hedgers = cg["table"], cg["tests"], cg["hedgers"]
        P = np.array([[T[t][h]["price"] for h in hedgers] for t in tests])
        cells = VGroup()
        W, H = 2.6, 1.0
        x0, y0 = -2.4, 1.1
        heads = VGroup(*[wrapped_label(HEDGER_NAMES[h], 2.4, 17, NET if "net" in h else REF).move_to(
            [x0 + W * j, y0 + 0.85, 0]) for j, h in enumerate(hedgers)])
        rows = VGroup(*[wrapped_label(r"tested on " + TEST_NAMES[t], 2.6, 18, GREY_A).move_to([x0 - 2.9, y0 - H * i, 0])
                        for i, t in enumerate(tests)])
        for i, t in enumerate(tests):
            lo, hi = P[i].min(), P[i].max()
            for j, h in enumerate(hedgers):
                v = P[i, j]
                z = (v - lo) / max(hi - lo, 1e-9)
                col = interpolate_color(ManimColor(GOOD), ManimColor(BAD), z)
                box = Rectangle(width=W - 0.12, height=H - 0.12, stroke_width=0, fill_color=col, fill_opacity=0.55)
                box.move_to([x0 + W * j, y0 - H * i, 0])
                cells.add(VGroup(box, MathTex(f"{v:.2f}", font_size=32).move_to(box)))
        head = label(r"Indifference prices at 0.5\% costs: rows are the world, columns the hedger", font_size=26).to_edge(
            UP, buff=0.35)
        foot = wrapped_label(rf"each row coloured from its cheapest (green) to its dearest (red) hedger. Real windows: "
                             rf"{cg['n_real']} overlapping 30-day stretches of bitcoin, rescaled to 20\% volatility; "
                             r"GARCH fitted to the same history (Part 7); every hedger built around a 20\% Black--Scholes "
                             r"delta", 12.2, 18, GREY_A).to_edge(DOWN, buff=0.35)
        i_real = tests.index("BTC history")
        j_g, j_r = hedgers.index("net (GBM-trained)"), hedgers.index("net (GARCH-trained)")
        best_real = hedgers[int(np.argmin(P[i_real]))]
        names = {"delta daily": "daily delta", "Whalley--Wilmott": "the Whalley-Wilmott band",
                 "net (GBM-trained)": "the network trained on GBM", "net (GARCH-trained)": "the network trained on GARCH"}
        best_name = names[best_real]
        loss_g = P[i_real, j_g] - P[0, j_g]
        loss_r = P[i_real, j_r] - P[0, j_r]
        if P[i_real, j_g] > P[i_real, j_r]:
            verdict = "the network trained on the GARCH generator does better on real history than the one trained on " \
                      "Black-Scholes paths"
        else:
            verdict = "training on the GARCH generator does not help on real history here; the Black-Scholes-trained " \
                      "network does as well or better"
        with self.voiceover(
            "Rule seventeen says a hedger is tested on at least two generators and on history before it trades. Here "
            "is that test. Four hedgers, all at half a percent costs: daily delta, Whalley and Wilmott's band, the "
            "band network trained on Black–Scholes paths, and the same network trained on paths from a GJR-GARCH model "
            "fitted to bitcoin, rescaled to the same average volatility. Three worlds to price them in: Black–Scholes "
            "paths, GARCH paths, and real thirty-day stretches of bitcoin's history. <bookmark mark='a'/> Each cell is "
            "the price the hedger needs in that world. <bookmark mark='b'/> Moving from Black–Scholes paths to real "
            f"history, the GBM-trained network's price changes by {loss_g:+.2f}, the GARCH-trained one's by "
            f"{loss_r:+.2f}. And {verdict}. On real windows the cheapest is "
            f"{best_name}. A hedger is only as good as its simulator, which is why the rule exists."
        ) as vo:
            self.play(FadeIn(head), FadeIn(heads), FadeIn(rows))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.25, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(foot), Indicate(cells[i_real * len(hedgers) + j_g]),
                      Indicate(cells[i_real * len(hedgers) + j_r]))
        self.wait(0.6)
        self.clear_scene()

    def module(self, env):
        chart = house_chart(PART, lit=("vol", "research")).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{calib\_net}, \texttt{calibrate\_neural}", r"rough Bergomi through a network, with a Monte Carlo check"),
            (r"\texttt{train\_differential}, \texttt{gp\_with\_gradients}", r"differential machine learning and its twin"),
            (r"\texttt{deep\_bsde}, \texttt{deep\_stopping}", r"high-dimensional pricing and exercise"),
            (r"\texttt{Hedger}, \texttt{train\_hedger\_on}", r"the deep hedger on any simulator: entropic or CVaR, "
             r"band networks with a Whalley--Wilmott start"),
            (r"\texttt{leland\_sigma}, \texttt{merton\_hedge}", r"the classical answers it is checked against"),
            (r"\texttt{NeuralSV}", r"neural SDEs and robust bounds"),
            (r"\texttt{train\_sig\_generator}, \texttt{train\_ddpm}", r"market generators, scored by \texttt{stylized\_facts}"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=19, color=QC.HOUSE), label(b, font_size=19, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 6.4)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 17: no network is used without a slower, independent engine that can check it; inputs "
                             r"outside the region it was trained on go to that engine instead; and a hedger is tested on at "
                             r"least two market generators and on replayed history before it trades.  "
                             rf"No strategy was tested: the trial counter still reads {env['trials']}.", 12.4, 22,
                             QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The House now has its deep-learning tools. <bookmark mark='a'/> The neural calibrator, with its Monte "
            "Carlo check. Differential machine learning, and the Gaussian process that does the same thing exactly. "
            "The deep BSDE solver and deep stopping. The deep hedger on any simulator, with either risk measure, and "
            "the classical answers it is checked against. Neural SDEs for model risk. And the market generators, with "
            "the stylized facts as their scorecard. <bookmark mark='b'/> The seventeenth rule: no network is used without a slower, independent "
            "engine that can check it. Inputs outside its training region go to that engine instead. And a hedger is "
            "tested on at least two market generators and on replayed history before it trades. Nothing here tested a "
            f"trading strategy, so the counter still reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=6))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
