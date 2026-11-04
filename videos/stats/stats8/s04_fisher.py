from __future__ import annotations

import numpy as np

from videos.stats.stats8.common import *  # noqa: F403


class Fisher(VoiceoverScene):
    def construct(self):
        self.card()
        self.sphere()
        self.rotation()
        self.letters()
        self.independent()
        self.angle()
        self.consequences()

    def card(self):
        card = chapter_card(3, r"Fisher's geometry", r"A sample is a point; \ its statistics are lengths and angles", lit=(1915,),
                            part=PART)
        with self.voiceover("Chapter three. Fisher's geometry."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def sphere(self):
        hc = history_card(1915, r"R. A. Fisher, \ ``Frequency distribution of the values of the correlation coefficient''",
                          r"\emph{Biometrika} 10: \ a sample of $n$ is a point in $n$ dimensions; \ distributions become "
                          r"volumes of regions. \ He proved Student's guess this way, \ and set it out fully in 1925",
                          color=S.MUSEUM, width=8.4, font_size=24).move_to([0, 1.6, 0])
        rows = [
            cmath(r"f(\mathbf z)", r"=", r"(2\pi)^{-n/2}\, e^{-\|\mathbf z\|^2/2}", font_size=34),
        ]
        whys = [why(r"$n$ independent standard normals: \ the density depends only on the length $\|\mathbf z\|$")]
        cap = label(r"spherically symmetric: \ every rotation of $\mathbf z$ has the same distribution", font_size=26,
                    color=S.ACCENT).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Gosset found the t distribution by inspired guesswork. A young Ronald Fisher proved it, by thinking "
            "geometrically. <bookmark mark='a'/> A sample of n numbers is a single point in n-dimensional space, and a "
            "statistic is a function of where that point is. <bookmark mark='b'/> For independent standard normals, "
            "the joint density is a product of n bells, which is e to the minus half the squared length of the "
            "vector: it depends only on the distance from the origin. <bookmark mark='c'/> So the cloud of possible "
            "samples is perfectly round, and rotating it changes nothing. That one fact gives chi-squared, t and F."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            step = ladder(self, rows, whys, keep=1, top=-0.3, x=-1.0, buff=0.8, edge=6.9)
            vo.wait_until("b")
            step(0, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.clear_scene()

    def rotation(self):
        rows = [
            cmath(r"H", r"=", r"\renewcommand{\arraystretch}{1.7}\setlength{\arraycolsep}{9pt}\begin{pmatrix} 1/\sqrt 3 & 1/\sqrt 3 & 1/\sqrt 3 \\ "
                  r"1/\sqrt 2 & -1/\sqrt 2 & 0 \\ 1/\sqrt 6 & 1/\sqrt 6 & -2/\sqrt 6"
                  r"\end{pmatrix}", font_size=28),
            cmath(r"\mathbf y = H\mathbf z:\quad y_1", r"=", r"\sqrt n\,\bar z", font_size=32),
            cmath(r"y_2^2 + \cdots + y_n^2", r"=", r"\|\mathbf z\|^2 - n\bar z^2", r"=", r"\sum (z_i - \bar z)^2", font_size=32),
            cmath(r"\mathbf y", r"\sim", r"N(\mathbf 0, I)", r"\quad \text{(rotations keep the cloud round)}", font_size=32),
        ]
        rows[1][2].set_color(SIM)
        rows[2][4].set_color(RESID)
        rows[3][2].set_color(EXACT)
        whys = [why(r"Helmert's rotation (1876): \ first axis along $\mathbf 1$, \ the rest orthonormal"),
                why(r"the first new coordinate carries the mean"), why(r"the other $n - 1$ carry the deviations"),
                why(r"so $\bar z$ and $\sum(z_i - \bar z)^2$ use separate, independent coordinates")]
        with self.voiceover(
            "<bookmark mark='a'/> Rotate the axes so that the first one points along the diagonal, the vector of ones. "
            "Friedrich Helmert wrote down such a rotation in 1876; for three dimensions, here it is. "
            "<bookmark mark='b'/> The first new coordinate is root n times the sample mean. <bookmark mark='c'/> The "
            "remaining n minus one coordinates hold everything else: the sum of their squares is exactly the sum of "
            "squared deviations. <bookmark mark='d'/> And because the cloud is round, the rotated coordinates are again "
            "independent standard normals. The mean lives in one coordinate, the deviations in the others."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.55, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def independent(self):
        d = load("fisher")
        panels = VGroup()
        for k, (key, title, c) in enumerate((("normal", r"normal samples of 3", SIM), ("exp", r"exponential samples of 3", RESID))):
            m, s = np.asarray(d[key]["m"]), np.asarray(d[key]["s"])
            if key == "normal":
                A = axes([-2.2, 2.2], [0, 3.2], x_length=4.6, y_length=4.0, xlabel=r"$\bar x$", ylabel=r"$s$", xticks=[-2, 0, 2],
                         yticks=[0, 1, 2, 3], center=[-3.4 + 6.4 * k, -0.6, 0])
            else:
                A = axes([0, 3.5], [0, 3.2], x_length=4.6, y_length=4.0, xlabel=r"$\bar x$", ylabel=r"$s$", xticks=[0, 1, 2, 3],
                         yticks=[0, 1, 2, 3], center=[-3.4 + 6.4 * k, -0.6, 0])
            b = bounds(A.ax)
            pts = VGroup(*[Dot(A.ax.c2p(a, v), radius=0.022, color=c, fill_opacity=0.6) for a, v in zip(m, s)
                           if b[0] <= a <= b[1] and b[2] <= v <= b[3]])
            t = label(title, font_size=26, color=c).next_to(A, UP, buff=0.15)
            r = MathTex(rf"\operatorname{{corr}}(\bar x, s) = {d[key]['corr']:.2f}", font_size=26, color=c).next_to(A, DOWN, buff=0.15)
            panels.add(VGroup(A, pts, t, r))
        tag = note(r"simulated: 3,000 samples each").to_corner(UR, buff=0.3)
        foot = label(r"for normal data $\bar x$ and $s$ are independent: \ the property characterizes the normal (Geary 1936)",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "That has a striking consequence. <bookmark mark='a'/> For normal samples, the sample mean and the sample "
            "standard deviation are independent: here are three thousand samples of three, and the cloud of mean "
            "against standard deviation has no tilt and no curve. <bookmark mark='b'/> For exponential samples it's "
            "nothing like that: a large mean usually comes with a large spread, correlation point seven five. "
            "<bookmark mark='c'/> Independence of the mean and variance is special to the normal; in 1936 Roy Geary "
            "showed it characterizes the normal distribution. And it's what makes Student's t exact."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def consequences(self):
        rows = fit_rows(VGroup(
            MathTex(r"\bar x \sim N\!\Big(\mu, \frac{\sigma^2}{n}\Big)", r"\quad \text{one coordinate}", font_size=32),
            MathTex(r"\frac{(n - 1)s^2}{\sigma^2} \sim \chi^2_{n-1}", r"\quad n - 1 \text{ squared coordinates (chapter 4)}", font_size=32),
            MathTex(r"\bar x \perp s^2", r"\quad \text{different coordinates}", font_size=32),
            MathTex(r"\frac{\bar x - \mu}{s/\sqrt n} = \frac{Z}{\sqrt{\chi^2_{n-1}/(n - 1)}} \sim t_{n-1}", r"\quad \text{(chapter 5)}",
                    font_size=32, color=EXACT),
        ), 12.6, 0.42, [0, 0.4, 0])
        for r in rows:
            r[1].set_color(GREY_B)
        cap = label(r"three distributions, \ one rotation", font_size=28, color=S.ACCENT).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Read off the consequences, for a normal sample with any mean and standard deviation. "
            "<bookmark mark='a'/> The mean is normal, with variance sigma squared over n: it's one coordinate. "
            "<bookmark mark='b'/> The scaled sum of squares is a sum of n minus one squared standard normals: "
            "chi-squared with n minus one degrees of freedom. <bookmark mark='c'/> The two are independent, since they "
            "use different coordinates. <bookmark mark='d'/> And their ratio, the t statistic, is a normal divided by "
            "the root of an independent chi-squared over its degrees of freedom: Student's t. <bookmark mark='e'/> "
            "Three distributions, from one rotation."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(cap))
        self.clear_scene()

    def letters(self):
        hc = history_card(1912, r"Fisher to Gosset", r"a Cambridge undergraduate sends Student a proof of his distribution, \ in "
                          r"$n$-dimensional geometry; \ Gosset forwards it to Karl Pearson, \ who doesn't print it", color=S.MUSEUM,
                          width=8.6, font_size=24).move_to([0, 1.6, 0])
        rows = fit_rows(VGroup(
            label(r"Gosset to Fisher (1922), \ sending tables of $t$: \ ``you are probably the only man who will ever use them''",
                  font_size=24, color=GREY_A),
            label(r"Fisher's 1925 \emph{Statistical Methods for Research Workers} put $t$ in every laboratory", font_size=24),
            label(r"and renamed Student's $z = (\bar x - \mu)/s$ as $t = \sqrt{n - 1}\,z$, \ the form we use today", font_size=24,
                  color=S.ACCENT),
        ), 12.6, 0.3, [0, -1.4, 0])
        with self.voiceover(
            "The story behind the rotation is worth a minute. <bookmark mark='a'/> In 1912 Fisher, still a Cambridge "
            "undergraduate, wrote to Gosset with a proof of Student's distribution, done in n-dimensional geometry. "
            "Gosset thought it beyond him, and forwarded it to Karl Pearson, the editor of Biometrika, who didn't publish "
            "it. <bookmark mark='b'/> A decade later Gosset sent Fisher his tables of the distribution, remarking that "
            "Fisher was probably the only man who would ever use them. <bookmark mark='c'/> He was wrong: Fisher's book "
            "of 1925 put t in every laboratory in the world, and recast Student's original statistic into the t we "
            "use today."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k] if k == 0 else rows[1:]))
        self.clear_scene()

    def angle(self):
        rows = [
            cmath(r"\mathbf x - \mu\mathbf 1", r"=", r"\underbrace{(\bar x - \mu)\mathbf 1}_{\text{along } \mathbf 1} + \underbrace{(\mathbf x - \bar x\mathbf 1)}_{\perp\, \mathbf 1}",
                  font_size=30),
            cmath(r"\cot\theta", r"=", r"\frac{\|(\bar x - \mu)\mathbf 1\|}{\|\mathbf x - \bar x\mathbf 1\|}", r"=",
                  r"\frac{\sqrt n\,|\bar x - \mu|}{\sqrt{n - 1}\;s}", font_size=30),
            cmath(r"|t|", r"=", r"\sqrt{n - 1}\,\cot\theta", font_size=36),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"centre the data at $\mu$; \ split it along and across the diagonal"),
                why(r"$\theta$: \ the angle between $\mathbf x - \mu\mathbf 1$ and the diagonal"),
                why(r"$t$ measures an \emph{angle}: \ it cannot depend on $\sigma$, \ only on the direction")]
        foot = label(r"for a round cloud every direction is equally likely: \ so the law of $\theta$, \ and of $t$, \ is the same for every $\sigma$",
                     font_size=22, color=S.ACCENT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Fisher's picture also explains why t doesn't depend on sigma. <bookmark mark='a'/> Centre the data at mu, "
            "and split the vector into its part along the diagonal and its part across it. <bookmark mark='b'/> The "
            "ratio of their lengths is the cotangent of the angle theta between the data vector and the diagonal, and "
            "that ratio is the t statistic, up to the factor root n minus one. <bookmark mark='c'/> So t measures an "
            "angle. Scaling the data by sigma stretches the vector but doesn't turn it. And because the normal cloud is "
            "round, every direction is equally likely, so the distribution of the angle, and of t, is the same "
            "whatever sigma is. Student's distribution is the distribution of a random direction."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.5, x=-1.2, buff=1.0, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
            self.play(FadeIn(foot))
        self.clear_scene()
