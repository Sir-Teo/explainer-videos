from __future__ import annotations

import numpy as np

from videos.stats.stats28.common import *  # noqa: F403


class Singular(VoiceoverScene):
    def construct(self):
        self.card()
        self.mixture()
        self.plane()
        self.breaks()
        self.watanabe()
        self.free_energy()
        self.table()
        self.where()

    def card(self):
        card = chapter_card(6, r"Singular models", r"When the truth is a set, \ not a point", lit=(2009,), part=PART)
        with self.voiceover("Chapter six. Singular models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def mixture(self):
        rows = [
            cmath(r"p(x \mid a, b)", r"=", r"(1 - a)\, \phi(x) + a\, \phi(x - b)", font_size=32),
            cmath(r"\text{truth}", r":", r"x \sim N(0, 1)", font_size=32),
            cmath(r"\text{true parameters}", r":", r"\{a = 0\} \cup \{b = 0\}", font_size=32),
            cmath(r"I(a, b)", r":", r"\text{singular on that set}", font_size=32),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"a two-component mixture, \ $a, b$ unknown"), why(r"one component is enough"),
                why(r"no weight, \ or no shift: \ a cross, \ not a point"), why(r"its determinant is zero")]
        with self.voiceover(
            "<bookmark mark='a'/> The classical AIC and BIC derivations just used regular, identifiable "
            "parameterizations with nonsingular information. Cross-validation and importance-sampling identities do "
            "not themselves require all those assumptions. Many useful models aren't regular. Take a mixture: with "
            "probability a, a standard normal is shifted by b. <bookmark mark='b'/> Suppose the truth is a plain "
            "standard normal. <bookmark mark='c'/> Then any parameter with a equal to zero is true, whatever b is, "
            "and so is any parameter with b equal to zero, whatever a is. The true parameters form a cross. <bookmark"
            " mark='d'/> Along it the Fisher information is singular, and the Taylor expansions behind AIC and BIC, "
            "which divided by it, fail."
        ) as vo:
            intro=label('A smaller truth can make a larger mixture singular',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def plane(self):
        g = np.random.default_rng(2009)
        A = axes([0, 1], [-2, 2], x_length=6.0, y_length=4.8, xlabel=r"mixing weight $a$", ylabel=r"shift $b$",
                 xticks=[0, 0.5, 1], yticks=[-2, -1, 0, 1, 2], center=[-2.4, 0.2, 0])
        ax = A.ax
        aa = np.linspace(0, 1, 61)
        bb = np.linspace(-2, 2, 81)
        lands = {}
        for n in (100, 2000):
            x = g.standard_normal(n)
            ll = np.empty((len(bb), len(aa)))
            for i, b in enumerate(bb):
                e = np.exp(b * x - 0.5 * b * b) - 1.0
                ll[i] = np.sum(np.log1p(aa[:, None] * e[None, :]), axis=1)
            ll -= ll.max()
            lands[n] = Landscape(ax, ll, [0, 1], [-2, 2], levels=[-0.5, -1.5, -3.0], color=LOOC, stroke_width=2.5)
        cross = VGroup(Line(ax.c2p(0, -2), ax.c2p(0, 2), color=TRUE, stroke_width=6),
                       Line(ax.c2p(0, 0), ax.c2p(1, 0), color=TRUE, stroke_width=6))
        rows = fit_rows(VGroup(
            label(r"gold: \ the true parameters, \ a cross", font_size=22, color=TRUE),
            label(r"orange: \ log likelihood within 0.5, 1.5, 3 of its max", font_size=22, color=LOOC),
            label(r"$n = 100$: \ a broad region hugging the cross", font_size=22),
            label(r"$n = 2{,}000$: \ it narrows, \ but not like an ellipse", font_size=22),
            label(r"near the crossing: \ volume $\asymp n^{-1/2}\log n$", font_size=22, color=RES),
        ), 4.6, 0.42, [4.2, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is the parameter plane, with the true set in gold: the whole left edge, where "
            "the weight is zero, and the whole middle line, where the shift is zero. <bookmark mark='b'/> The orange "
            "curves are the log likelihood's level sets for a hundred standard normal draws. <bookmark mark='c'/> The"
            " high-likelihood region is no ellipse around a point; it is a broad band hugging the cross. <bookmark "
            "mark='d'/> With two thousand draws it narrows, but slowly and unevenly. <bookmark mark='e'/> Near the "
            "crossing, the leading volume is proportional to log n over root n, whereas a regular two-parameter model"
            " gives one over n. That exponent is what BIC gets wrong."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cross), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lands[100].levels), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(ReplacementTransform(lands[100].levels, lands[2000].levels), FadeIn(rows[3]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def breaks(self):
        rows = [
            cmath(r"-\log p(y)", r"=", r"-\log \textstyle\int e^{\ell(\theta)} p(\theta)\, d\theta", font_size=30),
            cmath(r"\text{regular}", r":", r"-\ell(\hat\theta) + \tfrac d2 \log n + O_p(1)", font_size=30),
            cmath(r"\text{singular}", r":", r"-\ell(\theta_0) + \lambda \log n - (m - 1) \log\log n + O_p(1)", font_size=28),
            cmath(r"\lambda", r"\le", r"d/2", font_size=34),
        ]
        rows[2][2].set_color(LOOC)
        whys = [why(r"the free energy: \ minus the log evidence"), why(r"BIC, \ chapter three"),
                why(r"Watanabe (2009): \ $\lambda$ the RLCT, \ $m$ its order"), why(r"appropriate realizable analytic and positive-prior conditions")]
        with self.voiceover(
            "<bookmark mark='a'/> Watanabe asked what the log evidence really does. Call minus the log evidence the "
            "free energy. <bookmark mark='b'/> For a regular model it is the minimized negative log likelihood plus d"
            " over two log n: BIC. <bookmark mark='c'/> For a singular model, Sumio Watanabe proved in 2009, using "
            "resolution of singularities from algebraic geometry, that it is lambda log n, with a log log n "
            "correction. Lambda is the real log canonical threshold, a birational invariant of the true set. "
            "<bookmark mark='d'/> In the well-behaved realizable analytic setting with an appropriate positive prior,"
            " it is at most d over two and can be smaller: a singular model is effectively simpler than its parameter"
            " count."
        ) as vo:
            intro=label('Singular evidence depends on the true stratum and prior',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def watanabe(self):
        rows = [
            cmath(r"K(\theta)", r"=", r"\mathrm{KL}(\text{truth} \,\|\, p_\theta) \approx \tfrac12 a^2 b^2 \ \text{near }(a,b)=(0,0)", font_size=28),
            cmath(r"V(t)", r"=", r"\text{prior volume of } \{K(\theta) < t\} \propto t^{\lambda} (\log 1/t)^{m-1}", font_size=28),
            cmath(r"\{a^2 b^2 < t\}", r":", r"\text{volume} \asymp \sqrt t\, \log(1/t)", font_size=30),
            cmath(r"\lambda", r"=", r"\tfrac12, \ \ m = 2 \ \ \text{(regular: } \lambda = 1)", font_size=32),
        ]
        rows[3][2].set_color(LOOC)
        whys = [why(r"the KL divergence vanishes on the cross"), why(r"how fast the near-true region shrinks"),
                why(r"a direct calculation"), why(r"half the regular exponent")]
        with self.voiceover(
            "<bookmark mark='a'/> For the mixture it can be done by hand. Near the intersection a equals b equals "
            "zero, the leading divergence is half a squared times b squared. Away from that intersection the "
            "coefficient changes, though the relevant local vanishing structure remains. <bookmark mark='b'/> The "
            "evidence is governed by the prior volume of parameters whose divergence is below a small t, which scales"
            " like t to the lambda. <bookmark mark='c'/> The set where a squared b squared is below t has volume of "
            "order root t times log one over t. <bookmark mark='d'/> So lambda is one half, with multiplicity two: "
            "half the exponent of a regular two-parameter model."
        ) as vo:
            intro=label('The crossing changes the leading volume of near-true parameters',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def free_energy(self):
        d = load("rlct")
        ln = np.log(np.asarray(d["ns"], float))
        F, Fr = np.asarray(d["F"]), np.asarray(d["F_regular"])
        A = axes([3, 9.5], [0, 10], x_length=7.4, y_length=4.4, xlabel=r"$\log n$", ylabel=r"free energy above the truth's",
                 xticks=[4, 6, 8], yticks=[0, 5, 10], center=[-2.0, 0.3, 0])
        ax = A.ax
        pr = polyline(ax, ln, Fr, AICC, 3)
        ps = polyline(ax, ln, F, LOOC, 3)
        dr = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=AICC) for a, b in zip(ln, Fr)])
        ds = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=LOOC) for a, b in zip(ln, F)])
        rows = fit_rows(VGroup(
            label(r"$\log Z$ by quadrature, \ 6 data sets per $n$", font_size=22),
            label(rf"blue: \ a regular 2-parameter normal: \ slope {d['slope_regular']:.2f}", font_size=22, color=AICC),
            label(rf"orange: \ the mixture: \ slope {d['slope']:.2f}", font_size=22, color=LOOC),
            label(r"theory: \ 1 and $\tfrac12$ \ (minus a $\log\log n$ term)", font_size=22, color=GREY_A),
            label(r"BIC would charge the mixture 1", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Check it numerically. For sample sizes from thirty to ten thousand, compute the "
            "evidence by quadrature over the parameter plane, for six data sets each. <bookmark mark='b'/> A regular "
            "two-parameter normal model: its free energy grows with slope point nine nine in log n, the predicted "
            "one. <bookmark mark='c'/> The mixture's grows with slope point four two. <bookmark mark='d'/> Watanabe's"
            " one half, pulled down a little by the log log n term. <bookmark mark='e'/> BIC would charge the mixture"
            " the full one, giving the wrong leading evidence penalty for this singular example. Mixtures and neural "
            "models can also have locally regular regions; not every instance shares this exponent."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(pr), FadeIn(dr), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ps), FadeIn(ds), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def where(self):
        rows = fit_rows(VGroup(
            label(r"singular: \ mixtures, \ hidden Markov models, \ factor analysis, \ reduced rank, \ neural networks", font_size=24),
            label(r"WAIC and LOO: \ asymptotic relations under suitable assumptions", font_size=24, color=LOOC),
            label(r"WBIC: \ the evidence from one tempered posterior \ (Watanabe 2013)", font_size=24, color=HIT),
            label(r"sBIC: \ a BIC with the right $\lambda$ \ (Drton \& Plummer 2017)", font_size=24, color=BICC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Singular models are everywhere: mixtures, hidden Markov models, factor analysis, "
            "reduced-rank regression, and neural networks with redundant or inactive units. A finite permutation "
            "symmetry alone does not make a locally identified mode singular. <bookmark mark='b'/> For important "
            "analytic singular settings, WAIC and Bayesian leave-one-out retain asymptotic predictive relationships "
            "under additional assumptions. Finite-sample approximation and sampling diagnostics still matter. "
            "<bookmark mark='c'/> His WBIC estimates the evidence from a single posterior tempered at one over log n."
            " <bookmark mark='d'/> And Mathias Drton and Martyn Plummer's singular BIC puts the right lambda into a "
            "BIC, model by model."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def table(self):
        hdr = [r"\textbf{model}", r"\textbf{parameters} $d$", r"\textbf{$d/2$ \ (BIC)}", r"\textbf{RLCT $\lambda$ at a smaller truth}"]
        body = [
            [r"a regular model", r"$d$", r"$d/2$", r"$d/2$"],
            [r"this mixture, \ truth $N(0, 1)$", r"2", r"1", r"$1/2$"],
            [r"reduced-rank regression, \ rank $r$ of $H \times M$", r"$r(H + M - r)$", r"$\tfrac12 r(H + M - r)$", r"smaller \ (Aoyagi \& Watanabe 2005)"],
            [r"neural net with spare hidden units", r"many", r"many", r"architecture, true stratum and prior matter"],
        ]
        tb = table_rows([hdr] + body, font_size=24, col_buff=0.7, row_buff=0.3, colors=[GREY_A, AICC, LOOC, None, None])
        for r in tb[1:]:
            r[3].set_color(LOOC)
        if tb.width>13.:tb.width=13.
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"$\lambda$ depends on the true distribution, \ not only on the model", font_size=22),
            label(r"so does the right penalty: \ singular models cannot be scored by counting parameters", font_size=22, color=RES),
        ), 12.0, 0.22, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The real log canonical threshold has been worked out for many models. For a regular"
            " model it is d over two, BIC's value. For our mixture at a single-component truth, one half instead of "
            "one. <bookmark mark='b'/> For reduced-rank regression, Miki Aoyagi and Watanabe computed it exactly, "
            "with thresholds depending on matrix dimensions and the fitted and true ranks; at singular lower-rank "
            "truths they can differ from the regular half-dimension penalty. For neural networks, the threshold "
            "depends on architecture, the true parameter stratum and the prior. Counting only the units used by one "
            "representation is not a general formula. <bookmark mark='c'/> And it depends on where the truth lies, "
            "not only on the model, so no penalty that just counts parameters can be right for singular models."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1]), FadeIn(tb[2]))
            vo.wait_until("b")
            self.play(FadeIn(tb[3]), FadeIn(tb[4]), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()
