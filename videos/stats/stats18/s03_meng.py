from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats18.common import *  # noqa: F403


class Meng(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.three_factors()
        self.digest_numbers()
        self.neff()
        self.curves()
        self.board()

    def card(self):
        card = chapter_card(2, r"Meng's identity", r"Data quality $\times$ data quantity $\times$ problem difficulty", lit=(2018,),
                            part=PART)
        with self.voiceover("Chapter two. Meng's identity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def derive(self):
        rows = [
            cmath(r"R_i", r"=", r"1 \text{ if person } i \text{ is in the data},\ \ f = n/N = \bar R", font_size=30),
            cmath(r"\bar y_n - \bar y_N", r"=", r"\frac{\frac1N\sum R_i y_i}{f} - \bar y_N = \frac{\mathrm{Cov}_N(R, Y)}{f}", font_size=30),
            cmath(r"\ ", r"=", r"\frac{\rho_{R,Y}\,\sigma_R\,\sigma_Y}{f},\ \ \sigma_R = \sqrt{f(1 - f)}", font_size=30),
            cmath(r"\bar y_n - \bar y_N", r"=", r"\rho_{R,Y} \times \sqrt{\frac{1 - f}{f}} \times \sigma_Y", font_size=34),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"the population is fixed; \ only $R$ varies"), why(r"covariances over the $N$ people"),
                why(r"a correlation times two SDs; \ $R$ is 0/1"), why(r"Meng (2018): \ exact, \ for any sample")]
        intro = label('An exact identity connects selection and estimation error', font_size=36)
        with self.voiceover(
            "Xiao-Li Meng found a way to see both of the Digest's errors in a single line, and it's exact. <bookmark "
            "mark='a'/> For each of the N people in the population, let R be one if they're in our data and zero if "
            "not, so the average of R is the fraction f we observe. <bookmark mark='b'/> The sample mean is the "
            "average of R times y, divided by f. Subtract the population mean, and the error is the covariance of R "
            "and y over the whole population, divided by f. <bookmark mark='c'/> A covariance is a correlation times "
            "two standard deviations, and an indicator's standard deviation is the square root of f times one minus "
            "f. <bookmark mark='d'/> So the error of any sample, random or not, is the correlation between being in "
            "the data and the value, times the square root of one minus f over f, times the population standard "
            "deviation. No approximation, and no model."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.2, buff=0.45, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def three_factors(self):
        eq = MathTex(r"\bar y_n - \bar y_N", r"=", r"\rho_{R,Y}", r"\times", r"\sqrt{\frac{1 - f}{f}}", r"\times", r"\sigma_Y",
                     font_size=44).move_to([0, 1.6, 0])
        eq[2].set_color(RES)
        eq[4].set_color(FRAME)
        eq[6].set_color(BLUE)
        b1 = Brace(eq[2], DOWN, color=RES)
        b2 = Brace(eq[4], DOWN, color=FRAME)
        b3 = Brace(eq[6], DOWN, color=BLUE)
        t1 = label(r"data quality", font_size=24, color=RES).next_to(b1, DOWN, buff=0.1)
        t2 = label(r"data quantity", font_size=24, color=FRAME).next_to(b2, DOWN, buff=0.1).shift(LEFT * 0.3)
        t3 = label(r"problem difficulty", font_size=24, color=BLUE).next_to(b3, DOWN, buff=0.1).shift(RIGHT * 0.6 + DOWN * 0.35)
        foot = fit_rows(VGroup(
            label(r"random sampling makes $E[\rho_{R,Y}] = 0$, \ with $\rho_{R,Y}$ of order $1/\sqrt N$", font_size=24, color=HIT),
            label(r"self-selection lets $\rho_{R,Y}$ stay fixed, \ however large $N$ is", font_size=24, color=RES),
        ), 12.4, 0.3, [0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Meng named the three factors. <bookmark mark='b'/> The correlation between being "
            "included and the answer is data quality: the data defect correlation. <bookmark mark='c'/> The square "
            "root of one minus f over f is data quantity: it shrinks only as the data approach the whole population. "
            "<bookmark mark='d'/> And the standard deviation is problem difficulty: how much the answers vary. "
            "<bookmark mark='e'/> Random sampling is what makes the first factor tiny: when a lottery decides who is "
            "included, R is unrelated to y, and rho is of order one over the square root of the population size. "
            "<bookmark mark='f'/> When people select themselves, rho can stay fixed however big the population is, "
            "and the error doesn't go away."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(GrowFromCenter(b1), FadeIn(t1))
            vo.wait_until("c")
            self.play(GrowFromCenter(b2), FadeIn(t2))
            vo.wait_until("d")
            self.play(GrowFromCenter(b3), FadeIn(t3))
            vo.wait_until("e")
            self.play(FadeIn(foot[0]))
            vo.wait_until("f")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def digest_numbers(self):
        m = load("meng")["digest"]
        q = np.sqrt((1 - m["f"]) / m["f"])
        rows = [
            cmath(r"f", r"=", rf"{m['n']:,} / {m['N']:,} = {m['f']:.4f}", font_size=30),
            cmath(r"\rho_{R,Y}", r"=", rf"{m['rho']:.4f}", font_size=30),
            cmath(r"\sqrt{(1 - f)/f}", r"=", rf"{q:.2f},\ \ \sigma_Y = {m['sigma']:.3f}", font_size=30),
            cmath(r"\text{error}", r"=", rf"{m['rho']:.4f} \times {q:.2f} \times {m['sigma']:.3f} = {m['identity']:.4f}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"the World's Digest: \ 4.7\% of adults"), why(r"a weak correlation: \ 0.09"),
                why(r"for a share, \ $\sigma = \sqrt{p(1 - p)}$"), why(r"exactly the 19.8 points we saw")]
        with self.voiceover(
            "<bookmark mark='a'/> Apply it to the World's Digest. Its returns are four point seven percent of the "
            "adults. <bookmark mark='b'/> The correlation between returning a ballot and voting Blue, across all "
            "seven hundred thousand adults, is point oh nine: weak, the kind of correlation nobody would notice. "
            "<bookmark mark='c'/> The quantity factor is four point five two, and the standard deviation of a "
            "yes-or-no vote with thirty-eight percent yes is point four eight six. <bookmark mark='d'/> Multiply: "
            "point one nine eight. Exactly the nineteen point eight points the Digest was wrong by. A correlation of "
            "point oh nine, invisible in any single person, is a disaster in a population."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def neff(self):
        d = load("meng")
        m, h = d["digest"], d["half"]
        rows = [
            cmath(r"\text{squared error}", r"=", r"\rho^2\,\frac{1 - f}{f}\,\sigma^2\ \ \text{vs an SRS of } m:\ \frac{\sigma^2}{m}", font_size=30),
            cmath(r"n_{\text{eff}}", r"=", r"\frac{f}{1 - f}\cdot\frac{1}{\rho^2}", font_size=32),
            cmath(r"\text{the Digest}", r":", rf"{m['n']:,} \text{{ ballots}} \to n_{{\text{{eff}}}} = {m['n_eff']:.0f}", font_size=30),
            cmath(r"\text{a self-selected half}", r":", rf"{h['n']:,} \to n_{{\text{{eff}}}} = {h['n_eff']:.0f}", font_size=30),
        ]
        rows[2][2].set_color(RES)
        rows[3][2].set_color(RES)
        whys = [why(r"set the two errors equal"), why(r"a realized-error comparison, ignoring the SRS fpc"),
                why(r"34,588 ballots, \ worth 6 random voters"), why(r"$\rho = 0.14$: \ half the World, \ worth 50")]
        with self.voiceover(
            "<bookmark mark='a'/> How many randomly chosen people would be as accurate? Set the biased sample's squared error equal to an SRS's variance, approximately sigma squared over m when its sampling fraction is small, <bookmark mark='b'/> and solve: the effective sample size is f over one minus f, divided by rho squared. <bookmark mark='c'/> For the World's Digest, thirty-four thousand five hundred ballots have the accuracy of a simple random sample of six people. Six. <bookmark mark='d'/> Even if half the island answered, three hundred and sixty-four thousand people, with self-selection producing a correlation of point one four, the result would be worth a random sample of fifty. Meng computed the same thing for the 2016 American election: the estimated defect correlation of minus point oh oh five implies that a hypothetical self-report sample of one percent of eligible voters, about two point three million, would have the accuracy of roughly four hundred random voters."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curves(self):
        N = 741_311
        sig = 0.486
        n = np.logspace(2, np.log10(0.95 * N), 200)
        f = n / N
        srs = sig * np.sqrt((1 - f) / n)
        A = axes([2, 6], [0, 0.12], x_length=8.6, y_length=4.2, xlabel=r"sample size $n$", ylabel=r"error, \ share points",
                 xticks=[2, 3, 4, 5, 6], yticks=[0, 0.04, 0.08, 0.12], center=[-1.4, 0.3, 0],
                 xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"{100 * v:.0f}")
        ax = A.ax
        c_srs = polyline(ax, np.log10(n), srs, HIT, 3.5)
        cols = {0.005: OBS, 0.02: RES}
        cs = {r: polyline(ax, np.log10(n), r * np.sqrt((1 - f) / f) * sig, c, 3.5) for r, c in cols.items()}
        rows = fit_rows(VGroup(
            label(r"green: \ a simple random sample", font_size=22, color=HIT),
            label(r"gold: \ self-selected, \ $\rho = 0.005$", font_size=22, color=OBS),
            label(r"red: \ self-selected, \ $\rho = 0.02$", font_size=22, color=RES),
            label(r"fixed $\rho$: error scales as $\sqrt{(1-f)/f}$", font_size=22),
            label(r"the big-data paradox: \ the more data, \ the surer we are of a wrong answer", font_size=20, color=GREY_A),
        ), 4.0, 0.38, [4.9, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the difference as a picture, for a population the size of the World. The "
            "error of a simple random sample falls like one over root n, to under a point by ten thousand. <bookmark "
            "mark='b'/> A self-selected sample with a data defect correlation of just point oh oh five is about four "
            "times worse at every size, because the ratio of the two errors is rho times the square root of N. "
            "<bookmark mark='c'/> With point oh two, it's seventeen times worse: eight points at ten thousand, and "
            "above a point until half the island is included. <bookmark mark='d'/> For a fixed data defect "
            "correlation, error falls with the sampling fraction. Reducing the correlation can also reduce the error."
            " <bookmark mark='e'/> And because its confidence interval shrinks like any other, we become more "
            "confident of a wrong answer as the data grow: Meng's big-data paradox."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(c_srs), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cs[0.005]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cs[0.02]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=18) if r.part == 18 and (r.method.startswith("SRS") or "self-selected" in r.method)]
        b = coverage_board(rows, lit_part=18, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "The Coverage Board. <bookmark mark='a'/> A simple random sample of a thousand adults, with the ordinary "
            "interval for a proportion: ninety-four point six percent coverage, kept. <bookmark mark='b'/> A "
            "self-selected half of the island, three hundred and sixty-four thousand people, with the same formula: "
            "zero coverage in two hundred repetitions. Its interval is a third of a point wide, and seven points from"
            " the truth. Size bought precision; it couldn't buy accuracy."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[1]))
        self.wait(1.0)
        self.clear_scene()
