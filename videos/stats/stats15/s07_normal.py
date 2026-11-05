from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats15.common import *  # noqa: F403


class NormalModel(VoiceoverScene):
    def construct(self):
        self.card()
        self.model_setup()
        self.derivation()
        self.picture()
        self.sigma()
        self.widths()
        self.agreement()

    def card(self):
        card = chapter_card(6, r"The normal model", r"Unknown mean and variance: \ Student's $t$, \ again", lit=(1908,), part=PART)
        with self.voiceover("Chapter six. The normal model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def model_setup(self):
        d = load("normalt")
        x = np.asarray(d["x"])
        A = axes([155, 190], [0, 1], x_length=9.0, y_length=1.2, xlabel=r"height, \ cm", ylabel=r"", xticks=[160, 170, 180, 190], yticks=[],
                 center=[0, 1.4, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(v, 0.5), radius=0.1, color=DATA) for v in x])
        rows = [
            cmath(r"x_i \mid \mu, \sigma^2", r"\sim", r"N(\mu, \sigma^2),\quad i = 1, \ldots, 8", font_size=32),
            cmath(r"\pi(\mu, \sigma^2)", r"\propto", r"1/\sigma^2", font_size=34),
        ]
        whys = [why(r"both unknown, \ now"), why(r"the reference prior: \ flat in $\mu$ and in $\log\sigma$")]
        tag = simulated_tag(r"the World: \ 8 adults", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Eight of the World's adults, their heights in centimetres. In chapter two the standard "
            "deviation was known. Usually it isn't. <bookmark mark='b'/> Model the heights as normal with unknown mean and "
            "variance. <bookmark mark='c'/> For the prior, take the standard reference choice: flat in mu, and flat in the log "
            "of sigma, which is one over sigma squared. It's improper, but with two or more observations the posterior is fine."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.1))
            step = ladder(self, rows, whys, keep=2, top=0.0, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("bc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def derivation(self):
        rows = [
            cmath(r"\pi(\mu, \sigma^2 \mid x)", r"\propto", r"\sigma^{-n-2}\exp\Big\{-\frac{(n - 1)s^2 + n(\mu - \bar x)^2}{2\sigma^2}\Big\}", font_size=30),
            cmath(r"\pi(\mu \mid x)", r"=", r"\int_0^\infty \pi(\mu, \sigma^2 \mid x)\,d\sigma^2 \ \propto\ \Big[1 + \frac{n(\mu - \bar x)^2}{(n - 1)s^2}\Big]^{-n/2}", font_size=28),
            cmath(r"\frac{\mu - \bar x}{s/\sqrt n}\ \Big|\ x", r"\sim", r"t_{n - 1}", font_size=34),
            cmath(r"\frac{(n - 1)s^2}{\sigma^2}\ \Big|\ x", r"\sim", r"\chi^2_{n - 1}", font_size=32),
        ]
        rows[2][2].set_color(POST)
        whys = [why(r"Part 8's sum-of-squares split, \ in the exponent"), why(r"integrate out $\sigma^2$: \ a gamma integral"),
                why(r"Student's $t$, \ with $\mu$ as the random thing"), why(r"and the variance gets Part 8's $\chi^2$")]
        with self.voiceover(
            "<bookmark mark='a'/> Multiply the likelihood by the prior. The exponent contains Part 8's split of the sum of "
            "squares: n minus one times s squared, plus n times the squared distance from mu to the sample mean. "
            "<bookmark mark='b'/> We care about mu, so integrate sigma squared out. It's a gamma integral, and what's left is a "
            "power of one plus a squared distance. <bookmark mark='c'/> That's Student's t density: mu minus x bar, over s over "
            "root n, has a t distribution with n minus one degrees of freedom. The same pivot as Part 8, with the roles "
            "reversed: there the data were random and mu fixed; here mu is uncertain and the data fixed. "
            "<bookmark mark='d'/> And the variance's posterior gives Part 8's chi-squared."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.0, buff=0.62, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("normalt")
        r = d["post"]
        A = axes([158, 183], [0, 0.2], x_length=7.4, y_length=4.2, xlabel=r"$\mu$", ylabel=r"posterior density", xticks=[160, 165, 170, 175, 180],
                 yticks=[0, 0.1, 0.2], center=[-2.2, 0.2, 0])
        ax = A.ax
        xs = np.linspace(158, 183, 400)
        t = stats.t(r["df"], loc=r["loc"], scale=r["scale"])
        n = stats.norm(r["loc"], r["scale"])
        ct = density(ax, xs, t.pdf(xs), POST)
        cn = DashedVMobject(curve(ax, xs, n.pdf(xs), GREY_B, 2), num_dashes=40)
        lo, hi = d["ci"]
        tl, th = d["t_ci"]
        tr = DashedLine(ax.c2p(d["truth"], 0), ax.c2p(d["truth"], 0.19), color=S.TRUTH, stroke_width=2)
        rows = fit_rows(VGroup(
            MathTex(rf"\bar x = {r['loc']:.2f},\ \ s/\sqrt n = {r['scale']:.2f}", font_size=26),
            label(r"orange: \ the $t_7$ posterior", font_size=22, color=POST),
            label(r"dashed: \ pretending $\sigma$ were known", font_size=22, color=GREY_B),
            MathTex(rf"95\%\ \text{{credible:}}\ [{lo:.2f},\ {hi:.2f}]", font_size=26, color=POST),
            MathTex(rf"\text{{Part 8's }}t\text{{-interval:}}\ [{tl:.2f},\ {th:.2f}]", font_size=26, color=S.ALT),
            label(rf"the truth: \ {d['truth']:.1f}", font_size=22, color=S.TRUTH),
        ), 4.6, 0.32, [4.5, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For the eight heights: a sample mean of a hundred and seventy point five, a standard error of "
            "two point two nine. <bookmark mark='b'/> Here's the t posterior for mu, <bookmark mark='c'/> with the normal "
            "curve we'd get if sigma were known, for comparison: the t has heavier tails, paying for the unknown variance. "
            "<bookmark mark='d'/> The ninety-five percent credible interval runs from a hundred and sixty-five point oh six to a "
            "hundred and seventy-five point eight nine. <bookmark mark='e'/> Part 8's t-interval, from the same data: exactly the "
            "same numbers. <bookmark mark='f'/> The World's true mean, a hundred and sixty-nine point five, is inside both."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(ct), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cn), FadeIn(rows[2]))
            for k, m_ in enumerate("def"):
                vo.wait_until(m_)
                if k == 2:
                    self.play(Create(tr))
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()

    def sigma(self):
        d = load("normalt")
        x = np.asarray(d["x"])
        s2 = x.var(ddof=1)
        lo = np.sqrt(7 * s2 / stats.chi2.ppf(0.975, 7))
        hi = np.sqrt(7 * s2 / stats.chi2.ppf(0.025, 7))
        rows = [
            cmath(r"s", r"=", rf"{np.sqrt(s2):.2f}\ \text{{cm}}", font_size=34),
            cmath(r"\sigma \mid x", r"\in", rf"\Big[\sqrt{{7s^2/\chi^2_{{7,0.975}}}},\ \sqrt{{7s^2/\chi^2_{{7,0.025}}}}\Big] = [{lo:.2f},\ {hi:.2f}]", font_size=30),
            cmath(r"\text{Part 8}", r":", r"\text{the same } \chi^2 \text{ interval}", font_size=32),
        ]
        rows[1][2].set_color(POST)
        whys = [why(r"the sample SD"), why(r"95\% credible, \ from the $\chi^2_7$ posterior"), why(r"again identical")]
        with self.voiceover(
            "<bookmark mark='a'/> The sample standard deviation is six point five cm. <bookmark mark='b'/> The posterior for "
            "sigma gives a ninety-five percent credible interval from about four point three to thirteen point two: wide, with "
            "eight observations, and skewed to the right. <bookmark mark='c'/> And again it's numerically identical to the "
            "chi-squared interval of Part 8."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.0, x=-0.6, buff=0.8, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def agreement(self):
        rows = fit_rows(VGroup(
            label(r"here, \ the reference prior reproduces the classical intervals exactly", font_size=26, color=OBS),
            label(r"the numbers agree; \ the interpretations do not", font_size=24),
            label(r"a probability for $\mu$, \ given these data, \ versus a promise about a procedure", font_size=24, color=GREY_A),
            label(r"Jeffreys (1939) \ and \ Fisher's fiducial argument (1930) \ reached these intervals by different roads", font_size=24, color=S.ALT),
            label(r"add real prior information, \ and they part: \ chapter nine", font_size=24, color=POST),
        ), 12.4, 0.46, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So in the normal model, the reference prior reproduces the classical intervals exactly. "
            "<bookmark mark='b'/> The numbers agree; the interpretations don't. <bookmark mark='c'/> One is a probability "
            "statement about mu given these data, the other a promise about a procedure over repeated samples. "
            "<bookmark mark='d'/> Harold Jeffreys, in his 1939 Theory of Probability, and Fisher, with his fiducial argument of "
            "1930, reached these same intervals by different roads, and argued about it for decades. <bookmark mark='e'/> Put real "
            "prior information in, and the two part company. Chapter nine measures how."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def widths(self):
        from scipy import stats as st
        rows = [
            cmath(r"\sigma \text{ known}", r":", r"\bar x \pm 1.96\,\sigma/\sqrt n", font_size=32),
            cmath(r"\sigma \text{ unknown}, \ n = 8", r":", rf"\bar x \pm {st.t.ppf(0.975, 7):.2f}\, s/\sqrt n", font_size=32),
            cmath(r"n = 30", r":", rf"\pm {st.t.ppf(0.975, 29):.2f}", font_size=32),
            cmath(r"\text{so}", r":", r"\text{the price of not knowing } \sigma \text{ fades as } n \text{ grows}", font_size=30),
        ]
        rows[1][2].set_color(POST)
        whys = [why(r"the normal posterior of chapter two"), why(r"integrating out $\sigma$: \ heavier tails"),
                why(r"nearly normal"), why(r"Gosset's point (Part 8), \ from the Bayesian side")]
        with self.voiceover(
            "<bookmark mark='a'/> How much does not knowing sigma cost? With sigma known, the interval is plus or minus one point "
            "nine six standard errors. <bookmark mark='b'/> With eight observations and sigma unknown, integrating sigma out "
            "gives the t multiplier, two point three six: twenty percent wider. <bookmark mark='c'/> With thirty observations, "
            "two point oh five. <bookmark mark='d'/> The price of the unknown variance fades as the data grow, Gosset's point in "
            "Part 8, arrived at from the Bayesian side: the extra width is the posterior's honest uncertainty about sigma."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
