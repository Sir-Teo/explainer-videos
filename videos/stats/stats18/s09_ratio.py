from __future__ import annotations

import numpy as np

from videos.stats.stats18.common import *  # noqa: F403
from videos.stats.stats18.compute import adults


class Ratio(VoiceoverScene):
    def construct(self):
        self.card()
        self.laplace()
        self.laplace_math()
        self.recapture()
        self.estimator()
        self.world()
        self.precision()
        self.regression()

    def card(self):
        card = chapter_card(8, r"Ratio and regression estimators", r"Borrowing strength from what we already know", part=PART)
        with self.voiceover("Chapter eight. Ratio and regression estimators."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def laplace(self):
        d = load("ratio")["laplace"]
        hc = history_card(1802, r"P.-S. Laplace, \ for Napoleon's government",
                          r"the population of France, \ without a census: \ count people and births in a sample of communes, \ "
                          r"then scale up by the births registered everywhere", color=OBS, width=10.4, font_size=24).move_to([0, 1.6, 0])
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{sampled communes}}: {d['pop_sample']:,}\ \text{{people}},\ {d['births_sample']:,}\ \text{{births a year}}", font_size=28),
            MathTex(rf"\text{{ratio}}: {d['ratio']:.2f}\ \text{{people per birth}}", font_size=28, color=OBS),
            MathTex(r"\text{births in all of France} \approx 1{,}000{,}000", font_size=28),
            MathTex(rf"\text{{population}} \approx {d['estimate'] / 1e6:.2f}\ \text{{million}}", font_size=32, color=HIT),
        ), 12.4, 0.32, [0, -1.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The idea is old. Around 1802 Pierre-Simon Laplace estimated the population of France for "
            "Napoleon's government, without a census. Every parish registered its births, so the total number of births was "
            "known. What was missing was the number of people per birth. <bookmark mark='b'/> So Laplace had the population "
            "counted in a sample of communes spread across the country: two million and thirty-seven thousand people, with "
            "seventy-one thousand eight hundred and sixty-six births a year. <bookmark mark='c'/> That's twenty-eight point three "
            "five people for each birth. <bookmark mark='d'/> France registered about a million births a year, "
            "<bookmark mark='e'/> so the population was about twenty-eight point three five million. Laplace even attached a "
            "probability to his error, one of the first margins of error ever computed for a sample."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k]))
        self.clear_scene()

    def laplace_math(self):
        rows = [
            cmath(r"y", r":", r"\text{population},\ \ x: \text{births}", font_size=32),
            cmath(r"\hat R", r"=", r"\textstyle\sum_s y_i \big/ \sum_s x_i", font_size=32),
            cmath(r"\hat Y", r"=", r"\hat R \times X", font_size=32),
            cmath(r"\text{good when}", r":", r"y \approx R\,x: \text{ a line through the origin}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"unknown for France; \ known for the sample"), why(r"people per birth, \ in the sample"),
                why(r"$X$, \ all births, \ known exactly"), why(r"births track population closely")]
        with self.voiceover(
            "<bookmark mark='a'/> In general: we want the total of y, the population, and we know the total of an auxiliary "
            "variable x, births, for everyone. <bookmark mark='b'/> Estimate the ratio of y to x from the sample, "
            "<bookmark mark='c'/> and multiply by the known total of x. <bookmark mark='d'/> It works well when y is roughly "
            "proportional to x, a line through the origin, because then the ratio barely varies from one unit to the next, and "
            "a sample pins it down precisely."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def recapture(self):
        rows = [
            cmath(r"\text{Part 3's lake}", r":", r"M \text{ fish marked};\ \text{later } C \text{ caught}, \ R \text{ of them marked}", font_size=28),
            cmath(r"\hat N", r"=", r"M \times \frac{C}{R}", font_size=32),
            cmath(r"\text{Laplace}", r":", r"\text{births} \times \frac{\text{people}}{\text{births}}\ \text{in the sample}", font_size=28),
            cmath(r"\text{the same idea}", r":", r"\text{a known total, \ scaled by a ratio estimated from a sample}", font_size=28),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"capture--recapture"), why(r"Petersen's estimator"), why(r"the marked fish are the births"),
                why(r"so Laplace's method is often called the first capture--recapture")]
        with self.voiceover(
            "Laplace's estimate has a familiar shape. <bookmark mark='a'/> In Part 3 we estimated the fish in the World's lake: "
            "mark M fish, release them, and later catch C, of which R are marked. <bookmark mark='b'/> The estimate of the "
            "total is M times C over R. <bookmark mark='c'/> Laplace's births play the part of the marked fish: a total known "
            "exactly, scaled up by the ratio of people to births found in the sample. <bookmark mark='d'/> Both are ratio "
            "estimators, which is why Laplace's survey is often described as the first capture–recapture study."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def estimator(self):
        rows = [
            cmath(r"\hat{\bar y}_R", r"=", r"\frac{\bar y}{\bar x}\,\bar X", font_size=32),
            cmath(r"\mathrm{Var}", r"\approx", r"\big(1 - \tfrac nN\big)\frac{S_e^2}{n},\ \ e_i = y_i - R x_i", font_size=30),
            cmath(r"\text{vs}", r":", r"\big(1 - \tfrac nN\big)\frac{S_y^2}{n}", font_size=30),
            cmath(r"\text{bias}", r":", r"O(1/n),\ \ \text{small for large } n", font_size=30),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"for a mean"), why(r"the delta method (Part 9): \ only the residual spread counts"),
                why(r"the plain mean's variance"), why(r"a ratio of means isn't the mean of a ratio")]
        with self.voiceover(
            "<bookmark mark='a'/> For a mean, the ratio estimator is the sample mean of y over the sample mean of x, times the "
            "known population mean of x. <bookmark mark='b'/> By Part 9's delta method, its variance depends only on the spread "
            "of the residuals from the line y equals R x, <bookmark mark='c'/> where the plain mean's variance depends on the "
            "whole spread of y. When x explains most of y, the gain is large. <bookmark mark='d'/> The price is a small bias, of "
            "order one over n, because a ratio of means isn't unbiased for the ratio, but for any reasonable sample it's "
            "negligible."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def world(self):
        d = load("ratio")
        P = adults()
        y = P["income"]
        last = np.exp(np.log(y) + np.random.Generator(np.random.PCG64(5)).normal(0, 0.25, len(y)))
        g = np.random.Generator(np.random.PCG64(41))
        k = g.choice(len(y), 400, replace=False)
        A = axes([0, 200], [0, 200], x_length=4.8, y_length=4.4, xlabel=r"last year's income (the register)", ylabel=r"this year's",
                 xticks=[0, 100, 200], yticks=[0, 100, 200], center=[-3.8, 0.2, 0], font_size=18)
        ax = A.ax
        dots = scatter(ax, np.minimum(last[k], 199), np.minimum(y[k], 199), color=OBS, radius=0.045, opacity=0.7)
        R = d["one"]["ratio"]
        ln = Line(ax.c2p(0, 0), ax.c2p(200, 200 * R), color=FIT, stroke_width=3)
        rows = fit_rows(VGroup(
            label(r"the tax register has last year's income for everyone", font_size=22),
            MathTex(rf"\text{{corr}} = {d['corr_last']:.2f}", font_size=28),
            MathTex(rf"\text{{a sample of 400}}: \bar y = {d['one_plain']:.2f},\ \ \hat R = {R:.3f}", font_size=26),
            MathTex(rf"\hat{{\bar y}}_R = \hat R \times \bar X = {d['one']['mean']:.2f}", font_size=28, color=HIT),
            MathTex(rf"\text{{truth}}: {d['truth']:.2f}", font_size=26, color=S.TRUTH),
        ), 5.4, 0.4, [3.6, 0.2, 0])
        tag = simulated_tag(r"the World's register", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> On the World: suppose the tax register holds everyone's income for last year, known exactly, "
            "and we survey this year's. <bookmark mark='b'/> The two correlate at point nine five. <bookmark mark='c'/> One "
            "sample of four hundred: its plain mean is forty-six point six five thousand, and this year's incomes run at "
            "ninety-eight percent of last year's in the sample. <bookmark mark='d'/> The ratio estimate multiplies that by the "
            "register's known mean: fifty point oh four. <bookmark mark='e'/> The truth is forty-nine point four eight. The "
            "plain mean was off by almost three thousand, because this sample happened to miss a few high earners; the ratio "
            "estimator corrected for that, since the same people were missing from last year's register too."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ln), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def precision(self):
        d = load("ratio")
        gain = (d["sd_plain"] / d["sd_ratio"]) ** 2
        tab = table_rows([
            [r"3,000 samples of 400", r"mean", r"SD"],
            [r"the plain sample mean", f"{d['mean_plain']:.2f}", f"{d['sd_plain']:.2f}"],
            [r"the ratio estimator", f"{d['mean_ratio']:.2f}", f"{d['sd_ratio']:.2f}"],
        ], font_size=30, colors=[GREY_B, None, HIT]).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            MathTex(rf"\text{{truth}} = {d['truth']:.2f}", font_size=26, color=S.TRUTH),
            label(rf"the ratio estimator is worth a sample {gain:.0f} times larger", font_size=26, color=HIT),
            label(r"its bias: \ 0.03, \ invisible next to its SD", font_size=22, color=GREY_A),
        ), 12.4, 0.3, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Over three thousand samples, the plain mean has a standard deviation of three point oh four "
            "thousand. <bookmark mark='b'/> The ratio estimator's is point nine one: <bookmark mark='c'/> as precise as a plain "
            "sample eleven times the size. Its small bias, three hundredths, is invisible beside that. Auxiliary information "
            "known for the whole population is the cheapest precision there is."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]), FadeIn(foot[2]))
        self.clear_scene()

    def regression(self):
        rows = [
            cmath(r"\hat{\bar y}_{\text{reg}}", r"=", r"\bar y + b\,(\bar X - \bar x)", font_size=32),
            cmath(r"b", r"=", r"\text{the sample slope of } y \text{ on } x", font_size=30),
            cmath(r"\text{many } x", r":", r"\text{GREG: \ weights } w_i \text{ with } \textstyle\sum_s w_i x_i = X", font_size=30),
            cmath(r"\text{model-assisted}", r":", r"\text{valid by design, \ efficient if the model fits}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"correct the mean by how far $\bar x$ missed"), why(r"Part 12's least squares"),
                why(r"calibration: \ S\"arndal, \ Swensson \& Wretman (1992)"), why(r"the best of both views of chapter three")]
        with self.voiceover(
            "<bookmark mark='a'/> When the relation isn't a line through the origin, use the regression estimator: correct the "
            "sample mean of y by the slope times how far the sample mean of x missed the known population mean. "
            "<bookmark mark='b'/> The slope is Part 12's least squares. <bookmark mark='c'/> With several auxiliary variables "
            "this becomes the generalized regression estimator, GREG, equivalent to choosing weights for the respondents so that "
            "the weighted sample reproduces every known population total: calibration. <bookmark mark='d'/> It's called "
            "model-assisted: the estimator is valid by the design whether or not the regression model is true, and efficient when "
            "it is. It unites chapter three's two views."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
