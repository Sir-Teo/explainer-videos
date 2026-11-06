from __future__ import annotations

import numpy as np

from videos.stats.stats6.common import *  # noqa: F403


class Delta(VoiceoverScene):
    def construct(self):
        self.card()
        self.picture()
        self.derive()
        self.poisson()
        self.arcsine()
        self.several()
        self.second_order()

    def card(self):
        card = chapter_card(8, r"The delta method", r"The CLT, pushed through a smooth function", part=PART)
        with self.voiceover("Chapter eight. The delta method."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def picture(self):
        A = axes([0, 9], [0, 3.4], x_length=7.0, y_length=5.2, xlabel=r"$\bar X$", ylabel=r"$g(\bar X) = \sqrt{\bar X}$",
                 xticks=[0, 2, 4, 6, 8], yticks=[0, 1, 2, 3], center=[-1.8, -0.3, 0])
        ax = A.ax
        g = np.sqrt
        mu, sd = 4.0, 0.55
        xs = np.linspace(0, 9, 200)
        cv = curve(ax, xs, g(xs), SIM, 3.5)
        slope = 1 / (2 * np.sqrt(mu))
        tan = Line(ax.c2p(1.0, g(mu) + slope * (1.0 - mu)), ax.c2p(8.0, g(mu) + slope * (8.0 - mu)), color=EXACT, stroke_width=2.5)
        xx = np.linspace(mu - 3 * sd, mu + 3 * sd, 80)
        dens_x = VMobject(stroke_color=S.PRIOR, stroke_width=3, fill_color=S.PRIOR, fill_opacity=0.3)
        dens_x.set_points_smoothly([ax.c2p(x, 0.9 * normal_pdf(x, mu, sd)) for x in xx])
        sy = slope * sd
        yy = np.linspace(g(mu) - 3 * sy, g(mu) + 3 * sy, 80)
        dens_y = VMobject(stroke_color=S.POST, stroke_width=3, fill_color=S.POST, fill_opacity=0.3)
        dens_y.set_points_smoothly([ax.c2p(0.25 * normal_pdf(y, g(mu), sy) * sy / sd * 4, y) for y in yy])
        guide = VGroup(DashedLine(ax.c2p(mu, 0), ax.c2p(mu, g(mu)), color=GREY_C, stroke_width=1.5),
                       DashedLine(ax.c2p(mu, g(mu)), ax.c2p(0, g(mu)), color=GREY_C, stroke_width=1.5))
        rows = VGroup(MathTex(r"\text{width in: }\ \sigma/\sqrt n", font_size=28, color=S.PRIOR),
                      MathTex(r"\text{width out: }\ |g'(\mu)|\,\sigma/\sqrt n", font_size=28, color=S.POST),
                      label(r"close up, \ every smooth curve is its tangent line", font_size=24, color=EXACT)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        for r in rows:
            if r.width > 4.6:
                r.width = 4.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.5, 1.6, 0])
        with self.voiceover(
            "The central limit theorem is about averages. But we rarely want the average itself: we want its square "
            "root, its logarithm, a ratio of two averages. The delta method carries the theorem through any smooth "
            "function. <bookmark mark='a'/> Here's the idea in one picture. The sample mean is nearly normal, "
            "concentrated in a narrow band around mu. <bookmark mark='b'/> Push it through a smooth curve g, here "
            "the square root. <bookmark mark='c'/> Over such a narrow band the curve is almost straight: it's its "
            "tangent line. <bookmark mark='d'/> And a straight line maps a normal to a normal, stretching its width "
            "by the slope. So g of the mean is nearly normal too, centred at g of mu, with standard deviation "
            "the absolute value of g-prime of mu times sigma over root n."
        ) as vo:
            self.play(FadeIn(A), Create(cv))
            vo.wait_until("a")
            self.play(FadeIn(dens_x), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(guide))
            vo.wait_until("c")
            self.play(Create(tan), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(TransformFromCopy(dens_x, dens_y), FadeIn(rows[1]), run_time=1.6)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"g(\bar X_n)", r"=", r"g(\mu) + g'(\mu)(\bar X_n - \mu) + o_P(n^{-1/2})", font_size=32),
            cmath(r"\sqrt n\,\big(g(\bar X_n) - g(\mu)\big)", r"=", r"g'(\mu)\,\sqrt n(\bar X_n - \mu) + o_P(1)", font_size=32),
            cmath(r"\sqrt n\,\big(g(\bar X_n) - g(\mu)\big)", r"\xrightarrow{d}", r"N\big(0,\ g'(\mu)^2\sigma^2\big)", font_size=34),
        ]
        rows[2][2].set_color(S.POST)
        whys = [why(r"Taylor, \ to first order; \ $\bar X_n - \mu$ is of size $n^{-1/2}$"), why(r"multiply by $\sqrt n$"),
                why(r"the CLT, \ and Slutsky's theorem (chapter 9) for the remainder")]
        note_ = label(r"$g$ differentiable at $\mu$; $g'(\mu)\ne0$ for a non-degenerate normal limit", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.6)
        intro = label('A first-order Taylor approximation', font_size=36)
        with self.voiceover(
            "In symbols. <bookmark mark='a'/> Expand g around mu to first order. The remainder is smaller than the "
            "deviation of the mean, which is itself of size one over root n. <bookmark mark='b'/> Multiply through "
            "by root n. <bookmark mark='c'/> The central limit theorem says root n times the deviation tends to a "
            "normal with variance sigma squared; multiplying by g-prime of mu scales the variance by its square. The "
            "remainder vanishes in the limit, by the theorem of the next chapter. That's the delta method, and it "
            "works whenever g has a non-zero derivative at mu."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.4, buff=0.9, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            self.play(FadeIn(note_))
        self.clear_scene()

    def poisson(self):
        d = load("delta")
        lams = np.asarray(d["lams"])
        A = axes([-0.4, 1.9], [-0.7, 1.9], x_length=6.0, y_length=4.4, xlabel=r"$\lambda$ (log scale)", ylabel=r"variance (log scale)",
                 xticks=[0, 1], yticks=[-0.5, 0, 1], xfmt=lambda v: f"10^{{{int(v)}}}",
                 yfmt=lambda v: {-0.5: r"0.32", 0: r"1", 1: r"10"}[v], center=[-3.0, -0.5, 0])
        ax = A.ax
        lx = np.log10(lams)
        raw = VGroup(polyline(ax, lx, np.log10(d["var_raw"]), SIM, 3), *[Dot(ax.c2p(a, np.log10(b)), radius=0.06, color=SIM)
                                                                         for a, b in zip(lx, d["var_raw"])])
        sq = VGroup(polyline(ax, lx, np.log10(d["var_sqrt"]), S.POST, 3), *[Dot(ax.c2p(a, np.log10(b)), radius=0.06, color=S.POST)
                                                                            for a, b in zip(lx, d["var_sqrt"])])
        q = DashedLine(ax.c2p(-0.4, np.log10(0.25)), ax.c2p(1.9, np.log10(0.25)), color=EXACT, stroke_width=2)
        ql = MathTex(r"\tfrac14", font_size=28, color=EXACT).next_to(ax.c2p(1.9, np.log10(0.25)), RIGHT, buff=0.1)
        rows = [
            cmath(r"\mathrm{Var}\,X", r"=", r"\lambda", font_size=32),
            cmath(r"\mathrm{Var}\,\sqrt X", r"\approx", r"\Big(\frac{1}{2\sqrt\lambda}\Big)^2 \lambda", r"=", r"\frac14", font_size=32),
        ]
        rows[0][2].set_color(SIM)
        rows[1][4].set_color(S.POST)
        whys = [why(r"Poisson counts: \ the spread grows with the mean"), why(r"delta method, \ $g = \sqrt{\ }$: \ the spread no longer "
                                                                          r"depends on $\lambda$")]
        tag = note(r"exact: \ sums over the Poisson probabilities").to_corner(DR, buff=0.3)
        intro = label('A square root stabilizes large Poisson counts', font_size=36)
        with self.voiceover(
            "One of the delta method's best uses explains a trick from Part 1. <bookmark mark='a'/> A Poisson count "
            "has variance equal to its mean: big counts are noisier, which makes comparisons awkward. "
            "<bookmark mark='b'/> Take the square root. The derivative of root x at lambda is one over two root "
            "lambda; squared and multiplied by lambda, the first-order variance approximation is a quarter, becoming accurate for large lambda. "
            "<bookmark mark='c'/> Computed exactly: the raw variance, in blue, climbs with lambda; the variance of the "
            "square root, in orange, settles onto a quarter once lambda is above about five. That's a "
            "variance-stabilizing transformation, and it's why Part 1 took square roots of counts."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=2.7, x=3.0, buff=0.9, edge=6.9)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(tag), Create(raw), Create(sq), Create(q), FadeIn(ql), run_time=2.0)
        self.clear_scene()

    def arcsine(self):
        d = load("delta")
        ps = np.asarray(d["ps"])
        n = d["n"]
        A = axes([0, 1], [0, 2.2], x_length=6.4, y_length=4.2, xlabel=r"$p$", ylabel=r"variance $\times\, 4n$",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 1, 2], center=[-2.8, -0.5, 0])
        ax = A.ax
        share = polyline(ax, ps, 4 * n * np.asarray(d["var_share"]) * 1.0, SIM, 3)
        asin = polyline(ax, ps, 4 * n * np.asarray(d["var_asin"]), S.POST, 3)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=EXACT, stroke_width=2)
        rows = VGroup(
            MathTex(r"\mathrm{Var}\,\hat p = \frac{p(1 - p)}{n}", font_size=30, color=SIM),
            MathTex(r"g(p) = \arcsin\sqrt p:\ \ g'(p)^2\,p(1 - p) = \frac14", font_size=30),
            MathTex(r"\mathrm{Var} \arcsin\sqrt{\hat p} \approx \frac{1}{4n}", font_size=30, color=S.POST),
            label(rf"exact, \ $n = {n}$: \ within 5\% of $1/4n$ for $0.2 < p < 0.8$", font_size=22, color=GREY_A),
            label(r"the logit is a model link, not a variance-stabilizing transform (Part 14)", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        for r in rows:
            if r.width > 5.8:
                r.width = 5.8
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.4, 0])
        with self.voiceover(
            "The same idea works for proportions. <bookmark mark='a'/> A sample proportion has variance p times one "
            "minus p over n, which depends on the very p we're estimating. <bookmark mark='b'/> Look for a g whose "
            "derivative squared times p times one minus p is constant. The answer is the arcsine of the square root, "
            "and the constant is a quarter. <bookmark mark='c'/> So the variance of the arcsine-root of a proportion "
            "is about one over four n, whatever p is. <bookmark mark='d'/> Here it is computed exactly for samples of "
            "fifty: the raw variance, in blue, is a hump; the transformed one, in orange, is flat across the middle "
            "and only bends up near zero and one, where the approximation is strained."
        ) as vo:
            self.play(FadeIn(A))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k]))
            vo.wait_until("d")
            self.play(Create(share), Create(asin), Create(one), FadeIn(rows[3:]))
        self.clear_scene()

    def several(self):
        d = load("delta")
        rows = [
            cmath(r"\sqrt n\,\big(g(\bar{\mathbf X}_n) - g(\boldsymbol\mu)\big)", r"\xrightarrow{d}",
                  r"N\big(0,\ \nabla g^\top \Sigma\, \nabla g\big)", font_size=32),
            cmath(r"g(a, b) = a/b:\quad \nabla g^\top\Sigma\nabla g", r"=", r"\frac{1}{b^2}\Big(\sigma_a^2 - 2\frac{a}{b}\sigma_{ab} + "
                  r"\frac{a^2}{b^2}\sigma_b^2\Big)", font_size=30),
            cmath(r"\mathrm{sd}\big(\log \bar X\big)", r"\approx", r"\frac{\sigma}{\mu\sqrt n}", r"=",
                  rf"{d['log_sd_delta']:.5f}", r"\quad \text{simulated: } " + f"{d['log_sd_sim']:.5f}", font_size=30),
        ]
        rows[0][2].set_color(S.POST)
        rows[2][4].set_color(S.POST)
        whys = [why(r"many means at once: \ the gradient takes the place of $g'$ (Part 4's quadratic form)"),
                why(r"$b\ne0$, gradient at the population means; ratio estimates (Part 18)"),
                why(r"log of the mean of 50 of the World's heights")]
        tag = note(r"simulated: 20,000 samples of 50 heights").to_corner(DR, buff=0.3)
        intro = label('Several means and a gradient', font_size=36)
        with self.voiceover(
            "With several averages at once, the derivative becomes a gradient. <bookmark mark='a'/> For a smooth "
            "function of a vector of means, the limit is normal with variance gradient transpose Sigma gradient: "
            "Part 4's quadratic form, with Part 5's covariance matrix. <bookmark mark='b'/> For a ratio of two means, "
            "that gives this formula, which every survey statistician uses: ratio estimates in Part 18, odds ratios "
            "in Part 14. <bookmark mark='c'/> And a check: the standard deviation of the log of the mean of fifty of "
            "the World's heights. The delta method predicts sigma over mu root n; the simulation agrees to the "
            "third significant figure."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tag))
            step = ladder(self, rows, whys, keep=3, top=2.5, x=-0.8, buff=1.0, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def second_order(self):
        rows = [
            cmath(r"g'(\mu) = 0:\qquad g(\bar X_n)", r"=", r"g(\mu) + \tfrac12 g''(\mu)(\bar X_n - \mu)^2 + \cdots", font_size=30),
            cmath(r"n\,\big(g(\bar X_n) - g(\mu)\big)", r"\xrightarrow{d}", r"\tfrac12 g''(\mu)\,\sigma^2\, \chi^2_1", font_size=32),
            cmath(r"\mu = 0,\ g(x) = x^2:\qquad n\bar X_n^2", r"\xrightarrow{d}", r"\sigma^2 \chi^2_1", font_size=32),
        ]
        rows[1][2].set_color(S.PRIOR)
        rows[2][2].set_color(S.PRIOR)
        whys = [why(r"the linear term vanishes"), why(r"$\sqrt n(\bar X_n - \mu)/\sigma \to Z$, \ and $Z^2 \sim \chi^2_1$ (Part 3)"),
                why(r"a faster rate, \ $1/n$, \ and a skewed limit")]
        intro = label('When the first derivative vanishes', font_size=36)
        with self.voiceover(
            "What if the derivative is zero at mu? <bookmark mark='a'/> If g is twice differentiable there, the linear term disappears. A nonzero second derivative makes the quadratic term lead; if it too vanishes, higher order is needed. <bookmark mark='b'/> Multiply by n instead of root n, and the limit is a scaled "
            "chi-squared with one degree of freedom: the square of a normal, from Part 3. <bookmark mark='c'/> The "
            "simplest case: the squared mean of variables whose mean is zero. It shrinks faster, like one over n, "
            "and its limit is skewed, not normal. Tests based on likelihoods, in Part 10, live exactly here."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=0.6, buff=0.9, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()
