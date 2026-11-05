from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats15.common import *  # noqa: F403


class Conjugacy(VoiceoverScene):
    def construct(self):
        self.card()
        self.beta_binomial()
        self.pseudo()
        self.gamma_poisson()
        self.normal_derivation()
        self.heights()
        self.table()

    def card(self):
        card = chapter_card(2, r"Conjugacy", r"When the posterior is the prior, \ updated", part=PART)
        with self.voiceover("Chapter two. Conjugacy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def beta_binomial(self):
        rows = [
            cmath(r"\pi(p)", r"\propto", r"p^{a - 1}(1 - p)^{b - 1}", font_size=34),
            cmath(r"p(s \mid p)", r"\propto", r"p^{s}(1 - p)^{n - s}", font_size=34),
            cmath(r"\pi(p \mid s)", r"\propto", r"p^{a + s - 1}(1 - p)^{b + n - s - 1}", font_size=34),
            cmath(r"p \mid s", r"\sim", r"\text{Beta}(a + s,\ b + n - s)", font_size=34),
        ]
        rows[3][2].set_color(POST)
        whys = [why(r"a Beta$(a, b)$ prior"), why(r"the binomial likelihood"), why(r"the exponents add"),
                why(r"the same family: \ conjugate")]
        with self.voiceover(
            "Why did the posterior come out as a beta distribution? <bookmark mark='a'/> A Beta a b prior is proportional to p "
            "to the a minus one times one minus p to the b minus one. <bookmark mark='b'/> The binomial likelihood has the same "
            "shape: p to the s times one minus p to the n minus s. <bookmark mark='c'/> Multiply, and the exponents add. "
            "<bookmark mark='d'/> So the posterior is again a beta, with a plus the successes and b plus the failures. When "
            "the posterior stays in the prior's family, the prior is called conjugate, a term from Howard Raiffa and Robert "
            "Schlaifer's 1961 book. Updating becomes bookkeeping."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pseudo(self):
        rows = [
            cmath(r"\mathbb E[p \mid s]", r"=", r"\frac{a + s}{a + b + n}", font_size=34),
            cmath(r"\mathbb E[p \mid s]", r"=", r"\frac{a + b}{a + b + n}\cdot\frac{a}{a + b} + \frac{n}{a + b + n}\cdot\frac{s}{n}", font_size=32),
            cmath(r"a + b", r"=", r"\text{the prior's weight, \ in observations}", font_size=32),
            cmath(r"\text{Beta}(2, 2),\ 7/10", r":", r"\frac{2 + 7}{4 + 10} = 0.643", font_size=32),
        ]
        rows[1][2].set_color(POST)
        whys = [why(r"the posterior mean"), why(r"a weighted average of the prior mean and $\hat p$"),
                why(r"the prior acts like $a$ successes and $b$ failures, \ already seen"), why(r"between 0.5 and 0.7, \ nearer the data")]
        with self.voiceover(
            "<bookmark mark='a'/> The posterior mean is a plus s over a plus b plus n. <bookmark mark='b'/> Rearranged, it's a "
            "weighted average of the prior mean and the sample proportion, with weights a plus b and n. <bookmark mark='c'/> "
            "So the prior behaves exactly like a plus b observations seen before the experiment: a successes and b failures. "
            "A Beta two two prior is worth four imaginary trials. <bookmark mark='d'/> With seven successes in ten, the "
            "posterior mean is nine over fourteen, point six four three: between the prior's half and the data's point seven, "
            "much nearer the data. As n grows, the data's weight goes to one, and the prior is forgotten."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gamma_poisson(self):
        d = load("conjugate")
        sh, rt = d["gp"]["post"]
        A = axes([0, 1.5], [0, 7], x_length=6.8, y_length=4.2, xlabel=r"$\lambda$, \ deaths per corps per year", ylabel=r"density",
                 xticks=[0, 0.5, 1, 1.5], yticks=[0, 2, 4, 6], center=[-2.4, 0.2, 0])
        ax = A.ax
        xs = np.linspace(0.001, 1.5, 300)
        pr = density(ax, xs, stats.gamma(1, scale=1).pdf(xs), PRIOR)
        po = density(ax, xs, stats.gamma(sh, scale=1 / rt).pdf(xs), POST)
        lo, hi = d["gp_ci"]
        rows = fit_rows(VGroup(
            MathTex(r"\text{Gamma}(\alpha, \beta)\ \text{prior},\ \ y \sim \text{Poisson}", font_size=26),
            MathTex(r"\Rightarrow\ \text{Gamma}(\alpha + \textstyle\sum y,\ \beta + n)", font_size=28, color=POST),
            label(r"Bortkiewicz (Part 3): \ 122 deaths in 200 corps-years", font_size=22, color=S.MUSEUM),
            MathTex(rf"\text{{Gamma}}({sh:.0f}, {rt:.0f}):\ \text{{mean}}\ {d['gp_mean']:.3f}", font_size=28, color=POST),
            MathTex(rf"95\%:\ [{lo:.3f},\ {hi:.3f}]", font_size=28, color=POST),
            label(r"the prior is worth one corps-year", font_size=22, color=GREY_A),
        ), 4.8, 0.32, [4.4, 0.2, 0])
        with self.voiceover(
            "Other likelihoods have conjugate priors too. <bookmark mark='a'/> For Poisson counts, the gamma distribution: a "
            "gamma alpha beta prior on the rate, <bookmark mark='b'/> updated to alpha plus the total count, and beta plus the "
            "number of observations. <bookmark mark='c'/> Part 3's horse kicks: a hundred and twenty-two deaths in two hundred "
            "corps-years of the Prussian army. <bookmark mark='d'/> Start from a gamma one one prior, a vague belief, and the "
            "posterior is gamma one hundred and twenty-three, two hundred and one, with mean point six one two deaths per corps "
            "per year, <bookmark mark='e'/> and a ninety-five percent credible interval from point five one to point seven two. "
            "<bookmark mark='f'/> The prior counts as one corps-year with one death, against two hundred real ones, so it hardly "
            "matters."
        ) as vo:
            self.play(FadeIn(A), FadeIn(pr))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(ReplacementTransform(pr, po), FadeIn(rows[3]), run_time=1.5)
            for k, m_ in enumerate("ef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 4]))
        self.clear_scene()

    def normal_derivation(self):
        rows = [
            cmath(r"\pi(\mu)", r"\propto", r"\exp\Big\{-\frac{(\mu - m_0)^2}{2 s_0^2}\Big\}", font_size=32),
            cmath(r"p(\bar x \mid \mu)", r"\propto", r"\exp\Big\{-\frac{n(\bar x - \mu)^2}{2\sigma^2}\Big\}", font_size=32),
            cmath(r"\frac{1}{s_n^2}", r"=", r"\frac{1}{s_0^2} + \frac{n}{\sigma^2}", font_size=34),
            cmath(r"m_n", r"=", r"\frac{m_0/s_0^2 + n\bar x/\sigma^2}{1/s_0^2 + n/\sigma^2}", font_size=34),
        ]
        rows[2][2].set_color(POST)
        rows[3][2].set_color(POST)
        whys = [why(r"a normal prior on a mean"), why(r"normal data, \ $\sigma$ known"),
                why(r"complete the square: \ precisions add"), why(r"the posterior mean: \ a precision-weighted average")]
        with self.voiceover(
            "The third classic case is a normal mean. <bookmark mark='a'/> Put a normal prior on mu, centred at m zero with "
            "standard deviation s zero. <bookmark mark='b'/> With n normal observations of known standard deviation sigma, the "
            "likelihood depends on the data only through the sample mean, and is a normal curve in mu. <bookmark mark='c'/> "
            "Multiply the two exponentials and complete the square. The posterior is normal, and its precision, one over its "
            "variance, is the sum of the two precisions: the prior's, and the data's, n over sigma squared. <bookmark mark='d'/> "
            "Its mean is the average of the prior mean and the sample mean, weighted by their precisions. Information adds, "
            "and the more precise source pulls harder."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def heights(self):
        d = load("conjugate")["nn"]
        dd = load("conjugate")
        m0, s0 = d["prior"]
        m, s = d["post"]
        xb = d["xbar"]
        se = d["sigma"] / np.sqrt(d["n"])
        A = axes([140, 200], [0, 0.16], x_length=7.4, y_length=4.2, xlabel=r"$\mu$, \ mean adult height (cm)", ylabel=r"density",
                 xticks=[140, 150, 160, 170, 180, 190, 200], yticks=[0, 0.05, 0.1, 0.15], center=[-2.2, 0.2, 0])
        ax = A.ax
        xs = np.linspace(140, 200, 400)
        pr = density(ax, xs, stats.norm(m0, s0).pdf(xs), PRIOR, fill=0.15)
        li = density(ax, xs, stats.norm(xb, se).pdf(xs), LIKE, fill=0.15)
        po = density(ax, xs, stats.norm(m, s).pdf(xs), POST, fill=0.3)
        tr = DashedLine(ax.c2p(dd["truth"], 0), ax.c2p(dd["truth"], 0.155), color=S.TRUTH, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"a vague guess: \ $\mu \sim N(170, 10^2)$", font_size=24, color=PRIOR),
            MathTex(rf"\text{{10 adults:}}\ \bar x = {xb:.1f},\ \ \sigma/\sqrt n = {se:.2f}", font_size=26, color=LIKE),
            MathTex(rf"\text{{posterior:}}\ N({m:.1f},\ {s:.2f}^2)", font_size=28, color=POST),
            label(rf"the data get {100 * dd['w_data']:.1f}\% of the weight", font_size=24),
            label(rf"the World's truth: \ {dd['truth']:.1f}", font_size=22, color=S.TRUTH),
        ), 4.6, 0.36, [4.5, 0.2, 0])
        tag = simulated_tag(r"the World: \ 10 adults", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> On the World: someone guesses that the mean adult height is about a hundred and seventy "
            "centimetres, give or take ten. <bookmark mark='b'/> Ten adults are measured, with a mean of a hundred and sixty-nine "
            "point two; with sigma nine, the data's standard error is two point eight five. <bookmark mark='c'/> The posterior "
            "is normal, centred at a hundred and sixty-nine point three, with standard deviation two point seven four, a little "
            "narrower than the data alone. <bookmark mark='d'/> The data's precision is ten over eighty-one, the prior's one "
            "over a hundred, so the data get ninety-two and a half percent of the weight. <bookmark mark='e'/> The World's true mean is a "
            "hundred and sixty-nine point five."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(pr), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(li), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(po), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Create(tr), FadeIn(rows[4]))
        self.clear_scene()

    def table(self):
        tab = table_rows([
            [r"data", r"prior", r"posterior", r"prior worth"],
            [r"binomial: \ $s$ of $n$", r"Beta$(a, b)$", r"Beta$(a + s, b + n - s)$", r"$a + b$ trials"],
            [r"Poisson: \ $\sum y$ in $n$", r"Gamma$(\alpha, \beta)$", r"Gamma$(\alpha + \sum y, \beta + n)$", r"$\beta$ units of exposure"],
            [r"normal, \ $\sigma$ known", r"$N(m_0, s_0^2)$", r"$N(m_n, s_n^2)$", r"$\sigma^2/s_0^2$ observations"],
            [r"multinomial", r"Dirichlet$(\alpha)$", r"Dirichlet$(\alpha + \text{counts})$", r"$\sum\alpha$ observations"],
        ], font_size=26, col_buff=0.7, row_buff=0.3, colors=[GREY_B, None, None, None, None]).move_to([0, 0.6, 0])
        for r in tab[1:]:
            r[2].set_color(POST)
            r[1].set_color(PRIOR)
        foot = label(r"every exponential family has a conjugate prior (Part 3): \ Part 26 uses them as building blocks",
                     font_size=22, color=GREY_A).move_to([0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The conjugate pairs in one table. Binomial data with a beta prior; Poisson counts with a "
            "gamma prior; a normal mean with a normal prior; and multinomial counts with a Dirichlet prior, the beta's "
            "many-category cousin. In each case the prior is worth a definite number of imaginary observations. "
            "<bookmark mark='b'/> Every exponential family from Part 3 has a conjugate prior. They were once the only "
            "posteriors anyone could compute; now they're building blocks for the larger models of Part 26."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab, lag_ratio=0.08))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()
