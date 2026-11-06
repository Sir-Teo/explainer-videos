from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403
from videos.stats.stats40.s04_km import km_axes


class Greenwood(VoiceoverScene):
    def construct(self):
        self.card()
        self.formula()
        self.bands()
        self.transforms()
        self.simultaneous()
        self.board()

    def card(self):
        card = chapter_card(4, r"Greenwood's variance", r"How sure is the staircase?", lit=(1926,), part=PART)
        with self.voiceover("Chapter four. Greenwood's variance."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def formula(self):
        rows = [
            cmath(r"\log \hat S(t)", r"=", r"\textstyle\sum_{t_k \le t} \log(1 - d_k/n_k)", font_size=32),
            cmath(r"\text{Var}\log(1 - \hat q_k)", r"\approx", r"\dfrac{d_k}{n_k (n_k - d_k)}", font_size=32),
            cmath(r"\widehat{\text{Var}}\, \hat S(t)", r"=", r"\hat S(t)^2 \textstyle\sum_{t_k \le t} \dfrac{d_k}{n_k (n_k - d_k)}", font_size=32),
            cmath(r"\text{why it sums}", r":", r"\text{the factors are uncorrelated \ (martingales, \ chapter 6)}", font_size=30),
        ]
        rows[2][-1].set_color(SURVC)
        whys = [why(r"a sum of logs"), why(r"the delta method on a binomial"), why(r"Greenwood (1926)"),
                why(r"so the variances add")]
        with self.voiceover(
            "<bookmark mark='a'/> The log of the Kaplan-Meier estimate is a sum of logs of the factors. <bookmark "
            "mark='b'/> Each factor is a binomial proportion among the n k at risk, and the delta method gives the "
            "variance of its log. <bookmark mark='c'/> Adding them and converting back gives Major Greenwood's formula of "
            "1926, derived for life tables of cancer patients half a century before Kaplan and Meier: S squared times a sum "
            "of d over n times n minus d. <bookmark mark='d'/> Adding variances needs the factors to be uncorrelated, which "
            "they are, a fact chapter six will explain."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bands(self):
        d = load("gehan")
        t, e, g = (np.asarray(d[k], float) for k in ("time", "event", "group"))
        k = g == 1
        A = km_axes()
        ax = A.ax
        K = KMStaircase(ax, t[k], e[k].astype(int), color=MPC)
        km = d["mp"]
        bp = K.band(np.asarray(km["plain_lo"], float), np.asarray(km["plain_hi"], float), color=MISSC, opacity=0.25)
        bl = K.band(np.asarray(km["ll_lo"], float), np.asarray(km["ll_hi"], float), color=MPC, opacity=0.3)
        side = fit_rows(VGroup(
            label(r"6-MP, \ with 95\% pointwise bands", font_size=22, color=MPC),
            label(r"red: \ plain, \ $\hat S \pm 1.96\, \text{SE}$", font_size=22, color=MISSC),
            label(r"green: \ log-log, \ always inside $[0, 1]$", font_size=22, color=MPC),
            label(r"wider as the risk set shrinks", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The 6-MP curve with ninety-five percent bands. <bookmark mark='b'/> The plain band, "
            "estimate plus or minus one point nine six standard errors, in red, is symmetric, and can poke above one or "
            "below zero. <bookmark mark='c'/> The log-log band, in green, is computed for log of minus log S and "
            "transformed back, so it stays inside zero and one and is lopsided where it should be. <bookmark mark='d'/> "
            "Both widen to the right, as the risk set shrinks: by week thirty-two only a handful remain."
        ) as vo:
            self.add(gehan_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(K.curve()), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bp), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def transforms(self):
        rows = [
            cmath(r"\text{plain}", r":", r"\hat S \pm z\, \text{SE}: \ \text{can leave } [0, 1]", font_size=30),
            cmath(r"\text{log}", r":", r"\hat S\, e^{\pm z \sigma}: \ \text{can exceed } 1", font_size=30),
            cmath(r"\text{log-log}", r":", r"\hat S^{\exp(\pm z \sigma/\log \hat S)}: \ \text{inside } (0, 1)", font_size=30),
            cmath(r"\text{why}", r":", r"\log(-\log \hat S) \text{ is closer to normal when } n_k \text{ is small}", font_size=30),
        ]
        rows[2][-1].set_color(MPC)
        whys = [why(r"Wald on the raw scale"), why(r"$\sigma^2 = \sum d/(n(n-d))$"), why(r"Kalbfleisch \& Prentice (1980)"),
                why(r"Part 11's lesson again")]
        with self.voiceover(
            "<bookmark mark='a'/> Three standard intervals. The plain one is a Wald interval on the raw scale. <bookmark "
            "mark='b'/> The log interval works on log S. <bookmark mark='c'/> The log-log interval works on log of minus "
            "log S, a scale that runs over the whole real line, and maps back into zero and one. <bookmark mark='d'/> "
            "The transformation matters when the risk sets are small, the lesson of Part eleven's binomial intervals once "
            "more. The Board measures how much."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = board_rows("known fates", "Greenwood", "log-log")
        text = (
            "<bookmark mark='a'/> The Coverage Board. First, the shortcut of using only the patients whose fate is known: "
            "the share surviving past t among those who either died or were followed past t. With two hundred patients and "
            "moderate censoring, its ninety percent interval is broken. <bookmark mark='b'/> Then the Kaplan-Meier curve "
            "with twenty patients, at a time where the true survival is thirty percent. Greenwood's plain interval falls "
            "short, <bookmark mark='c'/> while the log-log interval keeps its promise. Use the log-log, the default in "
            "most software, and look at the risk set before trusting the tail."
        )
        show_board(self, rows, text, [("a", [0]), ("b", [1]), ("c", [2])])

    def simultaneous(self):
        rows = [
            cmath(r"\text{pointwise}", r":", r"P\big(S(t) \in \text{band at } t\big) \ge 1 - \alpha \ \text{for each } t", font_size=30),
            cmath(r"\text{simultaneous}", r":", r"P\big(S(t) \in \text{band for all } t \le \tau\big) \ge 1 - \alpha", font_size=30),
            cmath(r"\text{Hall--Wellner}", r":", r"\hat S(t) - S(t) \approx S(t)\, B\big(\sigma^2(t)\big): \ \text{a Brownian bridge in a new clock}", font_size=28),
            cmath(r"\text{in practice}", r":", r"\text{wider, \ by roughly half again at } 95\%", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"what most software draws"), why(r"for the whole curve"), why(r"Hall \& Wellner (1980)"), why(r"Part 48's empirical processes")]
        with self.voiceover(
            "<bookmark mark='a'/> These bands are pointwise: at each single time, they cover the true survival with "
            "ninety-five percent probability. <bookmark mark='b'/> A statement about the whole curve at once, that it lies "
            "inside the band everywhere up to some horizon, needs a simultaneous band. <bookmark mark='c'/> W. J. Hall and "
            "Jon Wellner built one in 1980 from the fact that the Kaplan-Meier error behaves like a Brownian bridge run on "
            "a new clock, the subject of Part forty-eight. <bookmark mark='d'/> Simultaneous bands are wider; reading a "
            "pointwise band as if it were simultaneous is another way of looking at many times and reporting the one that "
            "looks best."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
