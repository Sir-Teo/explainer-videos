from __future__ import annotations

import numpy as np

from videos.stats.stats14.common import *  # noqa: F403


class Poisson(VoiceoverScene):
    def construct(self):
        self.card()
        self.counts()
        self.rates()
        self.model()
        self.fit_plot()
        self.reading()
        self.check()
        self.rare_link()

    def card(self):
        card = chapter_card(5, r"Poisson regression", r"Counts, \ rates, \ and offsets", lit=(1898,), part=PART)
        with self.voiceover("Chapter five. Poisson regression."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def _women(self, d):
        m = np.asarray(d["male"]) == 0
        return np.asarray(d["mid"])[m], np.asarray(d["cases"])[m], np.asarray(d["pop"])[m]

    def counts(self):
        d = load("rates")
        mid, cases, pop = self._women(d)
        A = axes([17, 102], [0, 520], x_length=5.6, y_length=3.6, xlabel=r"age band", ylabel=r"cases", xticks=[20, 40, 60, 80, 100],
                 yticks=[0, 250, 500], center=[-3.4, 0.8, 0])
        B = axes([17, 102], [0, 45000], x_length=5.6, y_length=3.6, xlabel=r"age band", ylabel=r"women in the band", xticks=[20, 40, 60, 80, 100],
                 yticks=[0, 20000, 40000], center=[3.4, 0.8, 0], yfmt=lambda v: f"{int(v):,}")
        b1 = VGroup(*[Rectangle(width=A.ax.c2p(5.2, 0)[0] - A.ax.c2p(0, 0)[0], height=max(1e-3, A.ax.c2p(0, c)[1] - A.ax.c2p(0, 0)[1]),
                                stroke_width=0, fill_color=EVENT, fill_opacity=0.8).move_to(A.ax.c2p(m, 0), aligned_edge=DOWN) for m, c in zip(mid, cases)])
        b2 = VGroup(*[Rectangle(width=B.ax.c2p(5.2, 0)[0] - B.ax.c2p(0, 0)[0], height=max(1e-3, B.ax.c2p(0, n)[1] - B.ax.c2p(0, 0)[1]),
                                stroke_width=0, fill_color=S.WORLD, fill_opacity=0.8).move_to(B.ax.c2p(m, 0), aligned_edge=DOWN) for m, n in zip(mid, pop)])
        rows = fit_rows(VGroup(
            label(r"the World's silent condition (Part 2): \ cases among women, \ by six-year age band", font_size=24),
            label(r"the counts peak around 70, \ then fall", font_size=24, color=EVENT),
            label(r"because there are fewer people at each older age", font_size=24, color=S.WORLD),
            label(r"a count means nothing without its exposure", font_size=24, color=OBS),
        ), 12.4, 0.24, [0, -2.75, 0])
        tag = simulated_tag(r"the World: \ every adult", corner=UR)
        with self.voiceover(
            "Now counts. <bookmark mark='a'/> Part 2's World has a silent condition whose risk rises with age. Here are the "
            "cases among the World's women, in six-year age bands. <bookmark mark='b'/> The counts rise to a peak around seventy "
            "and then fall. Does the risk fall in old age? <bookmark mark='c'/> No: there are simply fewer people in each older "
            "band, as the population pyramid narrows. <bookmark mark='d'/> A count means nothing until you know the exposure "
            "it came from: the number of people, or the person-years, or the miles driven."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b1], lag_ratio=0.06), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b2], lag_ratio=0.06), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def rates(self):
        d = load("rates")
        mid, cases, pop = self._women(d)
        rate = cases / pop * 1000
        A = axes([17, 102], [0, 60], x_length=7.4, y_length=4.2, xlabel=r"age", ylabel=r"cases per 1{,}000", xticks=[20, 40, 60, 80, 100],
                 yticks=[0, 20, 40, 60], center=[-2.2, 0.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(m, r), radius=0.08, color=EVENT) for m, r in zip(mid, rate)])
        L = axes([17, 102], [np.log(1), np.log(60)], x_length=3.6, y_length=2.6, xlabel=r"age", ylabel=r"log rate", xticks=[20, 60, 100],
                 yticks=[], center=[4.6, 1.0, 0])
        ld = VGroup(*[Dot(L.ax.c2p(m, np.log(r)), radius=0.06, color=EVENT) for m, r in zip(mid, rate)])
        rows = fit_rows(VGroup(
            label(r"rate = count $\div$ people", font_size=22),
            label(r"the rate rises steadily", font_size=22, color=EVENT),
            label(r"on a log scale: \ nearly a straight line", font_size=22, color=OBS),
        ), 4.0, 0.26, [4.6, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Divide each count by the number of women in its band, and the rate per thousand rises "
            "steadily with age, from about two at twenty to nearly fifty at ninety-eight. <bookmark mark='b'/> It rises faster "
            "and faster: it looks multiplicative. <bookmark mark='c'/> On a logarithmic scale, the log rate is nearly a straight "
            "line in age. That suggests the model."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.08), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(L), FadeIn(ld), FadeIn(rows[2]))
        self.clear_scene()

    def model(self):
        rows = [
            cmath(r"y_i", r"\sim", r"\text{Poisson}(\mu_i)", font_size=34),
            cmath(r"\log\mu_i", r"=", r"\log N_i + \beta_0 + \beta_1\,\text{age}_i + \beta_2\,\text{male}_i", font_size=32),
            cmath(r"\frac{\mu_i}{N_i}", r"=", r"e^{\beta_0}\,e^{\beta_1\,\text{age}_i}\,e^{\beta_2\,\text{male}_i}", font_size=32),
            cmath(r"\text{fit}", r":", r"\text{IRLS with weights } \mu_i", font_size=32),
        ]
        rows[1][2][:5].set_color(OBS)
        whys = [why(r"rare events among many: \ Part 3's law of small numbers"), why(r"$\log N_i$: \ the offset, \ a term with coefficient fixed at 1"),
                why(r"so each $e^{\beta}$ multiplies the rate: \ a rate ratio"), why(r"the same algorithm, \ the Poisson variance")]
        with self.voiceover(
            "<bookmark mark='a'/> We approximate each band's binomial count by Poisson: rare events among many people, Part 3's law of small numbers, "
            "the horse kicks again. <bookmark mark='b'/> Its mean is the band's population times a rate, and the log of the rate "
            "is linear in age and sex. Taking logs, the population enters as log N, a term in the linear predictor whose "
            "coefficient is fixed at one: an offset. <bookmark mark='c'/> Exponentiate, and each coefficient multiplies the "
            "rate: e to beta one is the rate ratio for one more unit of age. <bookmark mark='d'/> It's fitted by the same "
            "iteratively reweighted least squares, with weights equal to the fitted means, because a Poisson variance equals "
            "its mean."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.0, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fit_plot(self):
        d = load("rates")
        mid, male, cases, pop = (np.asarray(d[k]) for k in ("mid", "male", "cases", "pop"))
        b0, b1, b2 = d["coef"]
        A = axes([17, 102], [np.log(1), np.log(60)], x_length=7.4, y_length=4.4, xlabel=r"age", ylabel=r"cases per 1{,}000 \ (log scale)",
                 xticks=[20, 40, 60, 80, 100], yticks=[0, np.log(5), np.log(20), np.log(50)], center=[-2.2, 0.2, 0],
                 yfmt=lambda v: f"{np.exp(v):.0f}")
        ax = A.ax
        rate = cases / pop * 1000
        dw = VGroup(*[Dot(ax.c2p(m, np.log(r)), radius=0.07, color=WOMEN) for m, r, s_ in zip(mid, rate, male) if s_ == 0])
        dm = VGroup(*[Dot(ax.c2p(m + 0.8, np.log(r)), radius=0.07, color=MEN) for m, r, s_ in zip(mid, rate, male) if s_ == 1])
        xs = np.linspace(17, 102, 100)
        lw = curve(ax, xs, np.log(1000) + b0 + b1 * (xs - 50) / 10, WOMEN, 3)
        lm = DashedVMobject(curve(ax, xs, np.log(1000) + b0 + b1 * (xs - 50) / 10 + b2, MEN, 3), num_dashes=40)
        rows = fit_rows(VGroup(
            label(r"women \ and \ men", font_size=24),
            label(r"the fitted log-rates: \ parallel straight lines", font_size=24, color=OBS),
            label(r"the lines nearly coincide", font_size=24),
            label(r"the oldest bands bend: \ the true risk is logistic", font_size=22, color=GREY_A),
        ), 4.4, 0.36, [4.6, 0.3, 0])
        rows[0].set_color(WOMEN)
        with self.voiceover(
            "<bookmark mark='a'/> Here are both sexes, on the log scale: women in coral, men in blue. <bookmark mark='b'/> The "
            "fitted model is a pair of parallel straight lines, one for each sex, since sex enters additively on the log scale. "
            "<bookmark mark='c'/> The two lines nearly coincide. <bookmark mark='d'/> The oldest bands bend away a little: the "
            "World's true risk is logistic in age, which is close to exponential only while it's small. A model is a "
            "description, good where it's checked."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(dw, lag_ratio=0.05), FadeIn(dm, lag_ratio=0.05), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lw), Create(lm), FadeIn(rows[1]))
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def reading(self):
        d = load("rates")
        lo, hi = d["rr10_ci"]
        ml, mh = d["rr_male_ci"]
        rows = [
            cmath(r"e^{\hat\beta_0}", r"=", rf"{d['rate50']:.1f}\ \text{{per 1{{,}}000 at age 50}}", font_size=32),
            cmath(r"e^{\hat\beta_1}", r"=", rf"{d['rr10']:.3f}\ \ [{lo:.3f},\ {hi:.3f}]\ \text{{per decade}}", font_size=32),
            cmath(r"e^{\hat\beta_2}", r"=", rf"{d['rr_male']:.3f}\ \ [{ml:.2f},\ {mh:.2f}]\ \text{{men vs women}}", font_size=32),
            cmath(r"\text{the World's truth}", r":", r"\text{the condition ignores sex}", font_size=32),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"the baseline rate (age coded as decades from 50)"), why(r"each decade multiplies the rate by 1.55"),
                why(r"the interval contains 1"), why(r"no detected association; not proof of equality")]
        with self.voiceover(
            "Reading the coefficients. <bookmark mark='a'/> With age coded in decades from fifty, the intercept gives the "
            "baseline: seven point seven cases per thousand women aged fifty. <bookmark mark='b'/> Each extra decade multiplies "
            "the rate by one point five five, with a tight interval, from one point five three to one point five seven, because "
            "there are seven thousand cases. <bookmark mark='c'/> Men versus women: a rate ratio of point nine nine, with an "
            "interval from point nine four to one point oh three, which contains one. <bookmark mark='d'/> And in the World, "
            "the condition truly ignores sex. The fitted age trend is clear; the interval is compatible with no sex association, which is consistent with this simulator's construction."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def check(self):
        d = load("rates")
        rows = [
            cmath(r"D", r"=", r"2\sum_i\Big[y_i\log\frac{y_i}{\hat\mu_i} - (y_i - \hat\mu_i)\Big]", font_size=32),
            cmath(r"D", r"=", rf"{d['deviance']:.1f}\ \ \text{{on {d['df']} df}}", font_size=32),
            cmath(r"\hat\phi", r"=", rf"\frac{{1}}{{n - p}}\sum_i\frac{{(y_i - \hat\mu_i)^2}}{{\hat\mu_i}} = {d['dispersion']:.2f}", font_size=32),
            cmath(r"\text{Poisson}", r":", r"\mathrm{Var}(y) = \mu,\ \text{so } \phi \approx 1", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"the deviance against a perfect fit"), why(r"about its degrees of freedom: \ an adequate fit"),
                why(r"Pearson's dispersion estimate"), why(r"next: \ when $\hat\phi$ is far above 1")]
        with self.voiceover(
            "Does the model fit? <bookmark mark='a'/> The deviance compares it with a perfect fit, one parameter per band. "
            "<bookmark mark='b'/> It's thirty-one on twenty-five degrees of freedom: about what chance alone would give. "
            "<bookmark mark='c'/> A second check is the Pearson dispersion: the squared residuals divided by the fitted means, "
            "averaged over the degrees of freedom. It's one point two two. <bookmark mark='d'/> For truly Poisson counts it "
            "is expected to be near one under a suitable Poisson mean model; it is not a proof of fit, because a Poisson variance equals its mean. When it's far above one, the Poisson standard "
            "errors are wrong, which is the next chapter."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rare_link(self):
        d = load("rates")
        cc = load("casecontrol")
        rows = [
            cmath(r"\text{Binomial}(N, p)", r"\approx", r"\text{Poisson}(Np)\quad\text{when } p \text{ is small}", font_size=32),
            cmath(r"\log p", r"\approx", r"\text{logit}\,p\quad\text{when } p \text{ is small}", font_size=32),
            cmath(r"\text{Poisson, \ per decade}", r":", rf"\log {d['rr10']:.3f} = {np.log(d['rr10']):.3f}", font_size=32),
            cmath(r"\text{logistic, \ per decade}", r":", rf"{cc['pop_coef'][1]:.3f}\ \ \text{{(the whole World, chapter ten)}}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"Part 3's law of small numbers"), why(r"since $\log\frac{p}{1-p} = \log p - \log(1 - p)$"),
                why(r"the rate ratio's log"), why(r"the odds ratio's log: \ nearly the same")]
        with self.voiceover(
            "One more connection. <bookmark mark='a'/> When the chance per person is small, a binomial count is nearly Poisson, "
            "Part 3's law of small numbers. <bookmark mark='b'/> And for a small probability, the log and the logit nearly "
            "agree. <bookmark mark='c'/> So for a rare condition, Poisson regression's log rate ratio per decade, point four "
            "four, <bookmark mark='d'/> is close to logistic regression's log odds ratio per decade on the same World, point "
            "four five. For rare outcomes the two models tell the same story, and the appropriate choice also depends on the sampling unit and mean model: Poisson handles exposure and person-time through the offset, logistic handles individual yes-or-no "
            "records."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
