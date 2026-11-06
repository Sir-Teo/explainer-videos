from __future__ import annotations

import numpy as np

from videos.stats.stats28.common import *  # noqa: F403


class MDL(VoiceoverScene):
    def construct(self):
        self.card()
        self.codes()
        self.twopart()
        self.nml()
        self.regret()
        self.prequential()

    def card(self):
        card = chapter_card(7, r"Minimum description length", r"The best model compresses the data most", lit=(1978,), part=PART)
        with self.voiceover("Chapter seven. Minimum description length."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def codes(self):
        rows = [
            cmath(r"L(y)", r"=", r"-\log_2 p(y) \ \text{bits}", font_size=32),
            cmath(r"\textstyle\sum_y 2^{-L(y)}", r"\le", r"1", font_size=32),
            cmath(r"L(y)", r"=", r"L(M) + L(y \mid M)", font_size=32),
            cmath(r"\text{choose}", r":", r"\text{the shortest total}", font_size=32),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"Shannon: \ probabilities are code lengths"), why(r"Kraft's inequality: \ and back again"),
                why(r"Rissanen (1978): \ describe the model, \ then the data"), why(r"regularities are what compress")]
        with self.voiceover(
            "<bookmark mark='a'/> A third tradition starts from compression. Any probability distribution defines a code: by "
            "Shannon, an outcome of probability p can be sent in minus log two p bits. <bookmark mark='b'/> And by Kraft's "
            "inequality, any decodable code defines a distribution. Probabilities and code lengths are the same thing. "
            "<bookmark mark='c'/> Jorma Rissanen's idea: to send data, first send a model, then the data using that model's "
            "code. <bookmark mark='d'/> The best model gives the shortest total: a model that captures real regularities "
            "compresses; one that memorizes noise costs too much to describe."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def twopart(self):
        d = load("mdl")
        rs = d["rows"]
        degs = [r["deg"] for r in rs]
        data = np.array([r["data"] for r in rs])
        par = np.array([r["params"] for r in rs])
        A = axes([-0.6, 9.6], [0, 80], x_length=7.4, y_length=4.4, xlabel=r"polynomial degree", ylabel=r"bits",
                 xticks=list(range(10)), yticks=[0, 20, 40, 60, 80], center=[-2.0, 0.3, 0])
        ax = A.ax
        w = 0.6
        db = VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0], height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 1e-3),
                                fill_color=TRAIN, fill_opacity=0.8, stroke_width=1).move_to(ax.c2p(k, v / 2))
                      for k, v in zip(degs, data)])
        pb = VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, p)[1] - ax.c2p(0, 0)[1],
                                fill_color=PATH, fill_opacity=0.8, stroke_width=1).move_to(ax.c2p(k, v + p / 2))
                      for k, v, p in zip(degs, data, par)])
        best = d["best"]
        ring = SurroundingRectangle(VGroup(db[best], pb[best]), color=WHITE, buff=0.06)
        rows = fit_rows(VGroup(
            label(r"chapter one's 30 points, \ one data set", font_size=22),
            label(r"teal: \ the data given the fit, \ $-\log_2$ likelihood", font_size=22, color=TRAIN),
            label(r"gold: \ the coefficients, \ $\tfrac12 \log_2 n$ bits each", font_size=22, color=PATH),
            label(rf"shortest: \ degree {best}, \ {rs[best]['total']:.1f} bits", font_size=22),
            label(r"$\tfrac12 \log n$ per parameter: \ BIC again", font_size=22, color=BICC),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Apply it to chapter one's thirty points. <bookmark mark='b'/> The teal bars are the bits "
            "needed to send the responses given each polynomial's fit, up to a common discretization constant; they fall as "
            "the degree rises. <bookmark mark='c'/> The gold bars are the bits to send the coefficients. Each needs to be "
            "stated only to the precision the data can support, about one over root n, which costs half log two n bits. "
            "<bookmark mark='d'/> The shortest total is degree five, where the test error was lowest too. "
            "<bookmark mark='e'/> Half log n per parameter is BIC's penalty, arrived at by an entirely different road."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in db], lag_ratio=0.1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in pb], lag_ratio=0.1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(ring), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def nml(self):
        rows = [
            cmath(r"\hat p(y)", r"=", r"p(y \mid \hat\theta(y))", font_size=32),
            cmath(r"p_{\text{NML}}(y)", r"=", r"\dfrac{p(y \mid \hat\theta(y))}{\sum_z p(z \mid \hat\theta(z))}", font_size=30),
            cmath(r"\text{regret}", r"=", r"\log \textstyle\sum_z p(z \mid \hat\theta(z))", font_size=30),
            cmath(r"", r"\approx", r"\tfrac k2 \log \tfrac{n}{2\pi} + \log \textstyle\int \sqrt{|I(\theta)|}\, d\theta", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"the best fit in hindsight: \ not a distribution"), why(r"Shtarkov (1987): \ normalize it"),
                why(r"the same excess for every $y$: \ minimax"), why(r"Rissanen (1996): \ BIC plus Jeffreys's volume")]
        with self.voiceover(
            "<bookmark mark='a'/> The two-part code is crude. A sharper code would use the best-fitting parameter for the data "
            "at hand, but that isn't a distribution: its sum over all possible data sets exceeds one. "
            "<bookmark mark='b'/> Yuri Shtarkov's normalized maximum likelihood divides by that sum. <bookmark mark='c'/> "
            "Every data set then costs the same amount more than its hindsight-optimal code, the log of the normalizer, and no "
            "code does better in the worst case. That excess, the regret, is the model's complexity. <bookmark mark='d'/> "
            "Rissanen showed it is k over two log n over two pi, plus the log of Jeffreys's prior's total volume: BIC, refined "
            "by the geometry of the model."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def regret(self):
        d = load("mdl")
        hdr = [r"\textbf{coin flips} $n$", r"\textbf{NML regret, \ exact (nats)}", r"\textbf{$\tfrac12 \log(n\pi/2)$}"]
        body = [[f"{n:,}", f"{a:.3f}", f"{b:.3f}"] for n, a, b in zip(d["ns"], d["regret"], d["approx"])]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.28, colors=[GREY_A] + [None] * 7)
        for r in tb[1:]:
            r[1].set_color(PATH)
            r[2].set_color(BICC)
        tb.move_to([0, 0.6, 0])
        foot = fit_rows(VGroup(
            label(r"the exact sum over all $n + 1$ head counts, \ $\sum_k \binom nk (k/n)^k (1 - k/n)^{n-k}$", font_size=22),
            label(r"Jeffreys's volume for a coin: \ $\int_0^1 \frac{d\theta}{\sqrt{\theta(1 - \theta)}} = \pi$", font_size=22, color=BICC),
        ), 12.0, 0.22, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For a coin, the regret can be computed exactly, summing over all possible numbers of heads. "
            "<bookmark mark='b'/> Rissanen's approximation is half log of n pi over two, because the Jeffreys volume of a coin "
            "is pi. It is off by a sixth of a nat at ten flips and by less than a hundredth from a thousand: the complexity "
            "of a one-parameter model grows like half log n, the same rate for every regular parameter."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.2), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
        self.wait(1.0)
        self.clear_scene()

    def prequential(self):
        rows = [
            cmath(r"-\log p(y_1, \ldots, y_n)", r"=", r"\textstyle\sum_t -\log p(y_t \mid y_1, \ldots, y_{t-1})", font_size=28),
            cmath(r"\text{plug-in}", r":", r"\textstyle\sum_t -\log p(y_t \mid \hat\theta_{t-1})", font_size=30),
            cmath(r"\text{Bayes}", r":", r"\text{the evidence, \ term by term}", font_size=30),
            cmath(r"\text{all three}", r":", r"\tfrac k2 \log n \ \text{to first order}", font_size=30),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"any joint code is a sequence of predictions"), why(r"Dawid (1984): \ the prequential principle"),
                why(r"the marginal likelihood is a forecaster"), why(r"NML, \ prequential, \ Bayes")]
        with self.voiceover(
            "<bookmark mark='a'/> A third code is sequential. Any joint probability factors into one-step-ahead predictions, so "
            "a code length is a running total of forecasting losses. <bookmark mark='b'/> Predict each observation from the "
            "estimate fitted to those before it: Philip Dawid's prequential approach, honest because no observation helps "
            "predict itself. <bookmark mark='c'/> Part 26's marginal likelihood is exactly such a sum, which explains why it "
            "penalizes complexity. <bookmark mark='d'/> To first order the normalized, prequential and Bayesian codes all cost "
            "k over two log n. MDL, Bayes and honest prediction meet, and chapter eleven returns to Dawid's forecasts."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
