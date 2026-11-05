from __future__ import annotations

import numpy as np

from videos.stats.stats22.common import *  # noqa: F403


class Information(VoiceoverScene):
    def construct(self):
        self.card()
        self.two()
        self.bins()
        self.why()
        self.advice()

    def card(self):
        card = chapter_card(4, r"Observed vs expected information", r"Which curvature?", part=PART)
        with self.voiceover("Chapter four. Observed versus expected information."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def two(self):
        rows = [
            cmath(r"\text{expected}", r":", r"n\,I(\hat\theta) = -n\,E_\theta\,\partial^2_\theta \log f \,\big|_{\hat\theta}", font_size=30),
            cmath(r"\text{observed}", r":", r"J(\hat\theta) = -\textstyle\sum_i \partial^2_\theta \log f(x_i;\theta)\,\big|_{\hat\theta}", font_size=30),
            cmath(r"\text{equal}", r":", r"\text{in exponential families, \ natural parameter}", font_size=28),
            cmath(r"\text{Cauchy}", r":", r"n\,I = n/2 \ \text{always; \ } J \ \text{varies with the sample}", font_size=28),
        ]
        rows[1][2].set_color(LIK)
        whys = [why(r"the average curvature, \ over imagined samples"), why(r"the curvature of this sample's likelihood"),
                why(r"curvature does not depend on the data there"), why(r"a sharp or a flat peak, \ by luck")]
        with self.voiceover(
            "Chapter three's variance, one over n I, used the expected information. There's a second candidate. "
            "<bookmark mark='a'/> The expected information is the average curvature of the log likelihood over all the samples "
            "we might have seen, evaluated at the estimate. <bookmark mark='b'/> The observed information is the curvature of "
            "the log likelihood we actually have. <bookmark mark='c'/> In exponential families with their natural parameter the "
            "two are identical. <bookmark mark='d'/> But for the Cauchy the expected information is always n over two, while the "
            "observed information depends on how the sample happens to fall: tightly clustered data give a sharp peak, "
            "scattered data a flat one."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bins(self):
        d = load("efron")
        b = d["bins"]
        A = axes([0.4, 4.6], [0, 0.2], x_length=8.0, y_length=4.4, xlabel=r"samples sorted by their observed information, \ in quarters",
                 ylabel=r"variance of the MLE", xticks=[], yticks=[0, 0.05, 0.1, 0.15, 0.2], center=[-1.6, 0.3, 0])
        ax = A.ax
        w = ax.c2p(0.32, 0)[0] - ax.c2p(0, 0)[0]
        bars, invj, names = VGroup(), VGroup(), VGroup()
        for k, r in enumerate(b):
            x = k + 1
            bars.add(Rectangle(width=w, height=ax.c2p(0, r["var"])[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=MLE_C,
                               fill_opacity=0.85).move_to(ax.c2p(x - 0.18, 0), aligned_edge=DOWN))
            invj.add(Rectangle(width=w, height=ax.c2p(0, r["inv_J"])[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=LIK,
                               fill_opacity=0.85).move_to(ax.c2p(x + 0.18, 0), aligned_edge=DOWN))
            names.add(label(rf"$J \approx {r['J']:.1f}$", font_size=18, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.15))
        exp_line = DashedLine(ax.c2p(0.4, d["expected_var"]), ax.c2p(4.6, d["expected_var"]), color=TRUE, stroke_width=2.5)
        rows = fit_rows(VGroup(
            label(rf"{d['R']:,} Cauchy samples of {d['n']}", font_size=22),
            label(r"blue: \ the MLE's actual variance", font_size=22, color=MLE_C),
            label(r"green: \ the average $1/J$ there", font_size=22, color=LIK),
            label(rf"dashed: \ $1/(nI) = {d['expected_var']:.2f}$, \ the same for all", font_size=22, color=TRUE),
            label(r"$1/J$ tracks the truth; \ $1/(nI)$ cannot", font_size=22, color=HIT),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Bradley Efron and David Hinkley asked in 1978 which one we should use. Simulate eight thousand "
            "Cauchy samples of twenty, and sort them into quarters by their observed information. <bookmark mark='b'/> In blue, "
            "the actual variance of the estimate within each quarter: samples with sharper peaks really do give more accurate "
            "estimates, by a factor of more than two from the flattest quarter to the sharpest. <bookmark mark='c'/> In green, "
            "one over the observed information, averaged in each quarter: it tracks the blue closely. <bookmark mark='d'/> The "
            "expected information gives the same answer, point one, for every sample, <bookmark mark='e'/> right on average but "
            "wrong for the sample in hand."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in bars], lag_ratio=0.2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in invj], lag_ratio=0.2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(exp_line), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def why(self):
        rows = [
            cmath(r"\text{ancillary statistic}", r":", r"\text{its distribution does not depend on } \theta", font_size=28),
            cmath(r"\text{e.g. the configuration}", r":", r"(x_1 - \hat\theta, \dots, x_n - \hat\theta)", font_size=30),
            cmath(r"\text{condition on it}", r":", r"\text{the relevant variance is } \approx 1/J", font_size=30),
            cmath(r"\text{Fisher (1934)}", r":", r"\text{recover the information the MLE alone loses}", font_size=28),
        ]
        rows[2][2].set_color(LIK)
        whys = [why(r"a statistic that says nothing about $\theta$"), why(r"for a location family: \ the spacing of the data"),
                why(r"Efron \& Hinkley (1978)"), why(r"the conditionality principle: \ chapter twelve")]
        with self.voiceover(
            "Why does the observed information win? <bookmark mark='a'/> An ancillary statistic is one whose distribution "
            "doesn't depend on the parameter: by itself it says nothing about theta. <bookmark mark='b'/> In a location family "
            "the configuration, the pattern of distances of the data from the estimate, is ancillary. <bookmark mark='c'/> But "
            "it tells us how precise this particular estimate is, and given the configuration the variance is close to one over "
            "J, the observed information. <bookmark mark='d'/> Fisher argued for conditioning on ancillaries in 1934: judge "
            "an estimate by the experiment you actually did, not by an average over experiments you might have done. Chapter "
            "twelve returns to this idea."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"report SEs from the observed information: \ $\sqrt{1/J(\hat\theta)}$", font_size=24, color=LIK),
            label(r"it is what Newton's method computes anyway (Part 21)", font_size=24),
            label(r"Fisher scoring uses the expected: \ equal at the end for canonical GLMs", font_size=24, color=GREY_A),
            label(r"and when the model may be wrong: \ neither; \ the sandwich, \ chapter ten", font_size=24, color=OBS),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So the practical advice is to report standard errors from the observed information, the "
            "curvature of your own likelihood at its peak. <bookmark mark='b'/> It's what Newton's method computes anyway. "
            "<bookmark mark='c'/> Fisher scoring uses the expected information, but for canonical generalized linear models the "
            "two coincide. <bookmark mark='d'/> And if the model itself may be wrong, neither curvature is right, and we need "
            "chapter ten's sandwich."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
