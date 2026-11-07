from __future__ import annotations

import numpy as np

from videos.stats.stats25.common import *  # noqa: F403


class Components(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.picture()
        self.estimates()
        self.anova()
        self.deff()

    def card(self):
        card = chapter_card(3, r"Random effects", r"Variance has parts", lit=(1918,), part=PART)
        with self.voiceover("Chapter three. Random effects and variance components."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def model(self):
        rows = [
            cmath(r"y_{gi}", r"=", r"\mu + u_g + \varepsilon_{gi}", font_size=30),
            cmath(r"u_g \sim N(0, \tau^2)", r",", r"\ \varepsilon_{gi} \sim N(0, \sigma^2)", font_size=30),
            cmath(r"\mathrm{Var}\,y", r"=", r"\tau^2 + \sigma^2", font_size=30),
            cmath(r"\rho", r"=", r"\tau^2/(\tau^2 + \sigma^2) = \mathrm{corr}(y_{gi}, y_{gj})", font_size=30),
        ]
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"a school effect and a pupil effect"), why(r"the schools are a sample from a population"),
                why(r"Fisher (1918): \ variance components"), why(r"the intraclass correlation")]
        intro = label('A working probability model states the assumptions behind shrinkage', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The simplest model with a random effect: each pupil's score is an overall mean, plus a "
            "school effect shared by everyone in the school, plus the pupil's own deviation. <bookmark mark='b'/> The school "
            "effects are treated as random, a sample from a population of schools with variance tau squared. "
            "<bookmark mark='c'/> The total variance splits into the two components, as Ronald Fisher first did in 1918 for "
            "the inheritance of human traits. <bookmark mark='d'/> Their ratio is the intraclass correlation: the "
            "correlation between two pupils of the same school, Part 23's rho."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("components")
        y, sch = np.asarray(d["example"]), np.asarray(d["example_school"])
        means = np.asarray(d["means"])
        A = axes([-0.5, 5.5], [200, 800], x_length=6.6, y_length=4.6, xlabel=r"six of the World's schools", ylabel=r"score",
                 xticks=[], yticks=[300, 500, 700], center=[-2.6, 0.3, 0])
        ax = A.ax
        g = np.random.Generator(np.random.PCG64(4))
        dots = VGroup(*[Dot(ax.c2p(k + 0.5 * (g.random() - 0.5), v), radius=0.03, color=GREY_B, fill_opacity=0.6) for v, k in zip(y, sch)])
        mlines = VGroup(*[Line(ax.c2p(k - 0.3, means[k]), ax.c2p(k + 0.3, means[k]), color=SHRUNK, stroke_width=5) for k in range(6)])
        grand = DashedLine(ax.c2p(-0.5, means.mean()), ax.c2p(5.5, means.mean()), color=TRUE, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"grey: \ pupils, \ each school's spread", font_size=22),
            label(r"green: \ school means", font_size=22, color=SHRUNK),
            label(r"gold: \ the World's mean", font_size=22, color=TRUE),
            label(r"pupils differ a lot; \ schools differ a bit", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [3.9, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Six of the World's schools. Within each, pupils' scores spread widely. "
            "<bookmark mark='b'/> The school means differ from one another <bookmark mark='c'/> and from the World's average, "
            "<bookmark mark='d'/> but by much less than pupils differ within a school."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.002), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(m) for m in mlines], lag_ratio=0.2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(grand), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def estimates(self):
        d = load("components")
        rows = [
            cmath(r"\hat\tau^2", r"=", rf"{d['G']:,.0f} \ \ (\text{{SD }} {np.sqrt(d['G']):.0f})", font_size=30),
            cmath(r"\hat\sigma^2", r"=", rf"{d['sigma2']:,.0f} \ \ (\text{{SD }} {np.sqrt(d['sigma2']):.0f})", font_size=30),
            cmath(r"\hat\rho", r"=", rf"{d['icc']:.3f}", font_size=30),
            cmath(r"\text{the World built}", r":", rf"\text{{school effect SD }} {np.sqrt(d['u_var_true']):.0f} \text{{, \ plus intake differences}}", font_size=28),
        ]
        rows[2][2].set_color(SHRUNK)
        whys = [why(rf"all {d['n']:,} pupils in 400 schools, \ REML"), why(r"pupils within schools"),
                why(r"18\% of the variance lies between schools"), why(r"SES differs between schools too")]
        intro = label('Intercept-only components include intake and programme variation', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Fit the model to all twenty-four thousand pupils in the World's four hundred "
            "schools. The variance between schools is about seventeen hundred, a standard deviation of forty-two "
            "points. <bookmark mark='b'/> The variance within schools is about seventy-nine hundred, a standard "
            "deviation of eighty-nine. <bookmark mark='c'/> So eighteen percent of the variation in scores lies "
            "between schools. <bookmark mark='d'/> The World built school effects with a standard deviation of "
            "thirty-five; the intercept-only fitted component also includes differences in intake and programme "
            "assignment. It is a descriptive component, not an estimate of only the built-in school disturbance."
        ) as vo:
            self.add(intro)
            self.add(simulated_tag())
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def deff(self):
        d = load("components")
        rows = [
            cmath(r"\mathrm{Var}(\bar y)", r"=", r"\dfrac{\sigma^2 + \tau^2}{n}\{1 + (m_* - 1)\rho\}", font_size=30),
            cmath(r"\text{design effect}", r"=", rf"1 + ({d['m_star']:.1f} - 1) \times {d['icc']:.3f} = {d['deff']:.1f}", font_size=30),
            cmath(r"n_{\text{eff}}", r"=", rf"{d['n']:,} / {d['deff']:.1f} \approx {d['neff']:,.0f}", font_size=30),
            cmath(r"\text{lesson}", r":", r"\text{the number of schools limits what we learn about schools}", font_size=28),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"Part 18's design effect, \ Part 23's Moulton"), why(r"$m_*=\sum_g m_g^2/\sum_g m_g$"),
                why(r"information for this mean under this model"), why(r"and a variance from few schools is shaky")]
        intro = label('Unequal school sizes change information for the overall pupil mean', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> For the unweighted pupil mean under a common-ICC model, unequal cluster sizes "
            "matter. The exact design factor uses m star: the sum of squared school sizes divided by the total number"
            " of pupils. It reduces to the common size when schools are equal. <bookmark mark='b'/> The display "
            "substitutes the actual sizes and fitted ICC. <bookmark mark='c'/> The effective sample size shown "
            "applies to this mean under that covariance model; it is not a universal information count for every "
            "coefficient. <bookmark mark='d'/> A between-school variance is still learned from the four hundred "
            "schools, which is why few-school inference needs care."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def anova(self):
        rows = [
            cmath(r"E\,\mathrm{MS}_{\text{within}}", r"=", r"\sigma^2", font_size=30),
            cmath(r"E\,\mathrm{MS}_{\text{between}}", r"=", r"\sigma^2 + m\,\tau^2", font_size=30),
            cmath(r"\hat\tau^2_{\text{ANOVA}}", r"=", r"(\mathrm{MS}_{\text{between}} - \mathrm{MS}_{\text{within}})/m", font_size=30),
            cmath(r"\text{trouble}", r":", r"\text{it can be negative; \ unbalanced } m_g \text{ have no unique version}", font_size=28),
        ]
        rows[2][2].set_color(SHRUNK)
        whys = [why(r"Part 13's one-way ANOVA"), why(r"group means carry both components"),
                why(r"the method of moments: \ Fisher, \ Tippett, \ Daniels"), why(r"hence likelihood: \ chapters four and five")]
        intro = label('Balanced random-intercept mean squares identify two variance components', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The oldest estimates come from Part 13's analysis of variance. The mean square within "
            "groups estimates sigma squared. <bookmark mark='b'/> The mean square between groups estimates sigma squared plus "
            "m times tau squared, because group means carry the school variance and a share of pupil noise. "
            "<bookmark mark='c'/> Subtract and divide by m, a method of moments. <bookmark mark='d'/> It has two flaws: it "
            "can come out negative, and when groups have different sizes there are many competing versions. Likelihood "
            "methods, the next two chapters, resolve both."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
