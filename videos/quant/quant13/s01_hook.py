from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, PART, RV, SPOT, VAR, load, real_data


def _yr(ts):
    return 1970 + np.asarray(ts, float) / (365.2425 * 86400)


def _ts(y, m, d):
    return datetime(y, m, d, tzinfo=timezone.utc).timestamp()


class Hook(VoiceoverScene):
    def construct(self):
        f = load("facts")
        e = load("exotics")
        self.title_card()
        self.rivers(f)
        self.question(e)
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"The second river")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part thirteen. Stochastic volatility and jumps. Part twelve read the volatility surface as a still "
            "photograph. This part asks what moves it."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def rivers(self, f):
        t = _yr(f["dvol_t"])
        dv = np.asarray(f["dvol"])
        g = axes([2021.25, 2026], [0.2, 1.6], x_length=10.4, y_length=4.4, ylabel=r"DVOL: bitcoin's 30-day implied volatility",
                 xticks=[2022, 2023, 2024, 2025], yticks=[0.4, 0.8, 1.2, 1.6], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=17).move_to(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, np.clip(dv, 0.2, 1.6), IV, stroke_width=2.4)
        tags = VGroup()
        for (a, b), name in (((_ts(2022, 5, 1), _ts(2022, 6, 30)), r"Terra--Luna, May 2022"),
                             ((_ts(2022, 11, 1), _ts(2022, 11, 30)), r"FTX, November 2022"),
                             ((_ts(2024, 8, 1), _ts(2024, 8, 15)), r"the yen carry unwind, August 2024")):
            m = (np.asarray(f["dvol_t"]) >= a) & (np.asarray(f["dvol_t"]) <= b)
            i = np.flatnonzero(m)[np.argmax(dv[m])]
            d = Dot(ax.c2p(t[i], dv[i]), radius=0.07, color=BAD)
            lab = label(rf"{name}: {100 * dv[i]:.0f}\%", font_size=18, color=GREY_A).next_to(d, UP, buff=0.12)
            tags.add(VGroup(d, lab))
        src = real_data(r"Deribit DVOL, daily, April 2021 -- November 2025")
        with self.voiceover(
            "Here is Bitcoin's thirty-day implied volatility, every day for four and a half years. It is not a "
            "constant. It is a river of its own, running beside the price. <bookmark mark='a'/> It floods when the "
            "price breaks: the collapse of Terra and Luna, the failure of FTX, the day in August 2024 when a crowded "
            "yen trade unwound across every market. And between floods it drains away, back toward a level it "
            "seems to remember."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(line), run_time=4)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.1) for t_ in tags], lag_ratio=0.6, run_time=3))
        self.wait(0.4)
        self.clear_scene()

    def question(self, e):
        names = {"LV": r"local vol", "Heston": r"Heston", "Bates": r"Bates", "VG": r"variance gamma", "SLV": r"SLV"}
        cl = {m: e["models"][m]["cliquet"] for m in names}
        rows = VGroup(*[VGroup(label(names[m], font_size=26, color=MODEL_COL[m]),
                               MathTex(rf"{100 * v:.2f}\%", font_size=34)).arrange(RIGHT, buff=0.5) for m, v in cl.items()])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        for r_ in rows:
            r_[1].align_to(rows, LEFT).shift(RIGHT * 3.4)
        head = label(r"five models, fitted to the same options, price one cliquet", font_size=28).to_edge(UP, buff=0.8)
        rows.next_to(head, DOWN, buff=0.5)
        v = np.array(list(cl.values()))
        q = label(rf"a {100 * (v.max() - v.min()) / v.mean():.0f}\% disagreement that no option price can settle",
                  font_size=26, color=BAD).next_to(rows, DOWN, buff=0.5)
        with self.voiceover(
            "This part builds the models that let volatility move: a second random river, jumps, and Lévy "
            "processes. Fit five of them to the same Bitcoin options, and price a cliquet, a contract that bets on "
            "how volatile the future will be. <bookmark mark='a'/> They disagree, by "
            f"{100 * (v.max() - v.min()) / v.mean():.0f} percent, and no option price on the screen can say which is "
            "right. Understanding why is this part's job."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.3,
                                                run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Why volatility must move: bitcoin's vol of vol, the leverage effect, and the post-1987 skew",
            r"Heston: the characteristic function, Feller's condition, and Andersen's QE scheme",
            r"SABR: Hagan's formula, the backbone, and its arbitrage at long maturities",
            r"Jumps and L\'evy models: Merton, Kou, Bates, variance gamma, NIG; the skew's term structure",
            r"Stochastic local volatility by the particle method; Bergomi's forward variance curves",
            r"The forward smile, cliquets and model risk; the SPX/VIX puzzle",
            r"Calibration: the loss landscape, and two years of parameters that would not sit still",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan. Why volatility must move. Heston's model, and how to simulate it honestly. SABR, the traders' "
            "shorthand. Jumps and Lévy processes, and what the skew's shape across maturities says about all of "
            "them. Stochastic local volatility and variance curves. The forward smile and model risk. And "
            "calibration: what it means to fit a model, and what happens when you fit it again next week."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=10))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        with self.voiceover(
            "In the House, the volatility desk gets its calibrator. <bookmark mark='a'/> From now on, every model the "
            "desk prices with is fitted by it, and every exotic carries a statement of how much the models disagree."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
