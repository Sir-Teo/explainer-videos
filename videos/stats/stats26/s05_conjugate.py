from __future__ import annotations

from videos.stats.stats26.common import *  # noqa: F403


class Conjugate(VoiceoverScene):
    def construct(self):
        self.card()
        self.family()
        self.dy()
        self.table()
        self.visits()
        self.predictive()
        self.beyond()

    def card(self):
        card = chapter_card(4, r"Conjugate families", r"Priors as pseudo-data", lit=(1979,), part=PART)
        with self.voiceover("Chapter four. Conjugate and exponential families."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def family(self):
        rows = [
            cmath(r"p(x \mid \theta)", r"=", r"h(x)\, e^{\theta T(x) - A(\theta)}", font_size=32),
            cmath(r"p(\theta \mid \chi, \nu)", r"\propto", r"e^{\theta\chi - \nu A(\theta)}", font_size=32),
            cmath(r"p(\theta \mid x_{1:n})", r"\propto", r"e^{\theta(\chi + \sum T(x_i)) - (\nu + n) A(\theta)}", font_size=30),
            cmath(r"(\chi, \nu)", r"\to", r"(\chi + \textstyle\sum T(x_i), \ \nu + n)", font_size=32),
        ]
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"Part 22's exponential family"), why(r"the conjugate prior: \ the same shape in $\theta$"),
                why(r"multiply: \ the shape survives"), why(r"the update is bookkeeping")]
        intro = label('Natural-parameter conjugacy updates sufficient-statistic bookkeeping', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Part 15's conjugate pairs all come from one source. Write the model as an "
            "exponential family, with natural parameter theta, sufficient statistic T and cumulant function A. "
            "<bookmark mark='b'/> Now choose a prior with the same shape in theta, governed by two numbers, chi and "
            "nu. <bookmark mark='c'/> Multiplying by the likelihood keeps that shape. <bookmark mark='d'/> So "
            "updating is bookkeeping: add the data's sufficient statistics to chi and the sample size to nu. The "
            "natural-parameter prior has a pseudo-data interpretation through chi and nu, provided the parameters "
            "define a proper prior."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def dy(self):
        rows = [
            cmath(r"E\{E(T \mid \theta) \mid x_{1:n}\}", r"=", r"\dfrac{\chi + n\bar T}{\nu + n}", font_size=32),
            cmath(r"", r"=", r"\dfrac{\nu}{\nu + n}\,\dfrac{\chi}{\nu} + \dfrac{n}{\nu + n}\,\bar T", font_size=32),
            cmath(r"\text{converse}", r":", r"\text{linear posterior means } \Rightarrow \text{ this prior}", font_size=30),
            cmath(r"\text{weight on the data}", r":", r"n/(\nu + n) \to 1", font_size=30),
        ]
        rows[1][-1].set_color(SHRUNK)
        whys = [why(r"Diaconis \& Ylvisaker (1979)"), why(r"prior mean and data mean, \ weighted"),
                why(r"conjugacy is characterized by linearity"), why(r"the prior is worth $\nu$ observations")]
        intro = label('Linear posterior mean characterizations require regularity conditions', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> For a regular natural exponential family with a proper conjugate prior and suitable"
            " boundary conditions, Diaconis and Ylvisaker obtain a linear posterior mean of the mean parameter. "
            "<bookmark mark='b'/> The displayed fraction weights the prior mean and the observed sufficient-statistic"
            " mean. <bookmark mark='c'/> Under their characterization conditions, linearity for all sample sizes "
            "identifies this conjugate family. This is not a converse for every imaginable model. <bookmark "
            "mark='d'/> The weight n over nu plus n tends to one as the sample grows."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        hdr = [r"\textbf{model}", r"\textbf{conjugate prior}", r"\textbf{update}", r"\textbf{worth}"]
        body = [[r"binomial $p$", r"Beta$(a, b)$", r"$a + s, \ b + f$", r"$a + b$ trials"],
                [r"Poisson rate $\lambda$", r"Gamma$(a, b)$", r"$a + \sum x, \ b + n$", r"$b$ periods"],
                [r"normal mean, \ $\sigma$ known", r"$N(m, \sigma^2/\nu)$", r"$\tfrac{\nu m + n\bar x}{\nu + n}$", r"$\nu$ observations"],
                [r"normal variance, \ $\mu$ known", r"inv-gamma$(a, b)$", r"$a + \tfrac n2, \ b + \tfrac12\sum (x - \mu)^2$", r"shape increment $n/2$"],
                [r"multinomial $\pi$", r"Dirichlet$(\alpha)$", r"$\alpha_k + n_k$", r"$\sum \alpha_k$ draws"],
                [r"exponential rate", r"Gamma$(a, b)$", r"$a + n, \ b + \sum x$", r"$a-1$ pseudo events; \ exposure $b$"]]
        tb = table_rows([hdr] + body, font_size=24, col_buff=0.6, row_buff=0.28, colors=[GREY_A] + [None] * 6)
        for r in tb[1:]:
            r[1].set_color(PRIOR)
            r[3].set_color(SHRUNK)
        tb.move_to([0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The table that follows from it. A beta prior for a proportion is worth a plus b trials; "
            "a gamma prior for a Poisson rate is worth b periods of observation; a normal prior for a mean is worth nu "
            "observations. <bookmark mark='b'/> Variances, category probabilities and failure rates work the same way. "
            "Reading a prior as pseudo-data is the quickest way to tell whether it is strong or weak."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r) for r in tb[1:4]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[4:]], lag_ratio=0.4))
        self.wait(1.0)
        self.clear_scene()

    def visits(self):
        d = load("conjugate")
        hdr = [r"\textbf{adults}", r"\textbf{sample mean}", r"\textbf{weight on data}", r"\textbf{posterior mean}", r"\textbf{95\% interval}"]
        body = [[f"{r['n']:,}", f"{r['xbar']:.2f}", f"{r['weight']:.3f}", f"{r['post_mean']:.2f}", rf"[{r['lo']:.2f}, {r['hi']:.2f}]"]
                for r in d["rows"]]
        tb = table_rows([hdr] + body, font_size=24, col_buff=0.7, row_buff=0.28, colors=[GREY_A] + [None] * 5)
        for r in tb[1:]:
            r[3].set_color(SHRUNK)
        tb[4][4].set_color(RES)
        tb.move_to([0, 1.0, 0])
        foot = fit_rows(VGroup(
            label(rf"prior: \ Gamma({d['a0']:.0f}, {d['b0']:.0f}), \ a mean of 4 visits, \ worth one adult", font_size=22, color=PRIOR),
            label(rf"the World's true mean: \ {d['truth']:.2f} visits a year", font_size=22, color=TRUE),
            label(r"one missed interval is not a diagnosis; \ chapter ten checks overdispersion", font_size=22, color=RES),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> An example: the mean number of doctor visits a year in the World, with a Poisson "
            "model and a gamma prior whose mean is four visits, worth a single adult. <bookmark mark='b'/> With one "
            "adult, the posterior mean is halfway between the prior's four and the adult's three. With five, the data"
            " get five-sixths of the weight; with a thousand, almost all of it, and the posterior mean is two point "
            "one five against the World's two point two four. <bookmark mark='c'/> But look at the sample of a "
            "hundred: its interval, two and a half to three point two, misses the truth. One missed "
            "ninety-five-percent interval does not diagnose a model. We also know the World's visits are "
            "overdispersed, which motivates the predictive checks in chapter ten. Conjugacy makes the arithmetic "
            "easy; it doesn't make the model right. Chapter ten catches this."
        ) as vo:
            self.add(simulated_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]), FadeIn(foot[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("c")
            self.play(Indicate(tb[4], scale_factor=1.05), FadeIn(foot[2]))
        self.clear_scene()

    def beyond(self):
        rows = fit_rows(VGroup(
            label(r"mixtures approximate many priors under suitable conditions \ (Dalal \& Hall 1983)", font_size=24),
            label(r"conjugate pieces inside bigger models: \ Gibbs sampling, \ Part 27", font_size=24, color=SHRUNK),
            label(r"logistic normal priors and most hierarchies need numerical methods", font_size=24, color=RES),
            label(r"convenience is not a reason to believe a prior", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Conjugacy goes further than it seems. Under suitable approximation conditions, "
            "mixtures of conjugate priors can represent many useful prior shapes, retaining tractable component "
            "updates. <bookmark mark='b'/> Inside bigger models, conjugate pieces make Gibbs sampling possible, as "
            "Part 27 shows. <bookmark mark='c'/> Normal priors for logistic coefficients are not conjugate. Formal "
            "conjugate families can exist, but their normalizers and summaries can still require numerical "
            "integration. Most useful hierarchies need approximation or simulation. <bookmark mark='d'/> And a "
            "prior's convenience is never a reason to believe it."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def predictive(self):
        rows = [
            cmath(r"x_{\text{new}} \mid \lambda", r"\sim", r"\text{Poisson}(\lambda), \ \ \lambda \mid x \sim \text{Gamma}(a', b')", font_size=28),
            cmath(r"p(x_{\text{new}} \mid x)", r"=", r"\textstyle\int \text{Poisson}(x_{\text{new}} \mid \lambda)\, \text{Gamma}(\lambda \mid a', b')\, d\lambda", font_size=28),
            cmath(r"", r"=", r"\text{NegBin}\bigl(a', \ \tfrac{b'}{b' + 1}\bigr)", font_size=32),
            cmath(r"\text{lesson}", r":", r"\text{the predictive is wider than the model: \ it carries } \lambda\text{'s uncertainty}", font_size=26),
        ]
        rows[2][-1].set_color(SHRUNK)
        whys = [why(r"a new adult, \ given the sample"), why(r"average the model over the posterior"),
                why(r"Part 24's gamma mixture, \ again"), why(r"but not wide enough for the World's visits")]
        intro = label('Parameter uncertainty and observation heterogeneity are different', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Conjugacy also gives the predictive distribution for a new observation in closed "
            "form. A new adult's visits are Poisson given the rate, and the rate has its gamma posterior. <bookmark "
            "mark='b'/> Average the Poisson over that posterior, <bookmark mark='c'/> and the result is a negative "
            "binomial, Part 24's gamma mixture of Poissons arising for a new reason. <bookmark mark='d'/> The "
            "predictive has greater variance than a Poisson with the same predictive mean because it carries the "
            "uncertainty about the rate. But with a thousand adults that uncertainty is tiny, and the predictive is "
            "still far narrower than the World's real spread of visits: parameter uncertainty is not a substitute for"
            " the right model."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
