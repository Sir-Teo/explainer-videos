from __future__ import annotations

import numpy as np

from videos.stats.stats45.common import *  # noqa: F403


class SteinLemma(VoiceoverScene):
    def construct(self):
        self.card()
        self.lemma()
        self.sure()
        self.js()
        self.risk()
        self.scatter()
        self.hitters()

    def card(self):
        card = chapter_card(10, r"Stein's lemma, \ SURE, \ James--Stein", r"An unbiased estimate of your own risk", lit=(1961,), part=PART)
        with self.voiceover("Chapter ten. Stein's lemma, SURE and James–Stein: an unbiased estimate of your own risk."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def lemma(self):
        d = load("stein")["lemma"]
        rows = [
            cmath(r"X \sim N(\theta, 1)", r":", r"\phi'(x - \theta) = -(x - \theta)\, \phi(x - \theta)", font_size=32),
            cmath(r"E[(X - \theta) h(X)]", r"=", r"\textstyle\int h(x)\,(-\phi'(x - \theta))\, dx = E\, h'(X)", font_size=32),
            cmath(r"h = \sin, \ \theta = 0.7", r":", rf"\text{{simulated}} \ {d['lhs']:.4f} \ \text{{vs}} \ {d['rhs']:.4f}; \ \text{{exact}} \ e^{{-1/2}}\cos\theta = {d['exact']:.4f}", font_size=28),
            cmath(r"\mathbb R^p", r":", r"E[(X - \theta)^\top g(X)] = E\, \nabla \cdot g(X)", font_size=34),
        ]
        rows[1][-1].set_color(S.ACCENT)
        rows[3][-1].set_color(ADMC)
        whys = [why(r"the Gaussian's derivative"), why(r"integrate by parts"), why(r"400,000 draws"), why(r"Stein (1981): \ the divergence")]
        with self.voiceover(
            f"<bookmark mark='a'/> Stein's tool was a one-line identity. The standard normal density's derivative is minus "
            f"x times the density. <bookmark mark='b'/> So for X normal with mean theta, the expectation of X minus theta "
            f"times h of X is, after integrating by parts, the expectation of h prime of X, for any smooth h that does not "
            f"grow too fast. <bookmark mark='c'/> Check it with h equal to sine and theta equal to point seven: four hundred "
            f"thousand simulated draws give {say(d['lhs'], 3)} and {say(d['rhs'], 3)}, against the exact "
            f"{say(d['exact'], 3)}. <bookmark mark='d'/> In p dimensions the same identity holds with the inner product on "
            f"the left and the divergence of g on the right. This is the lemma behind Part forty-three's Stein's method, in "
            f"its original role."
        ) as vo:
            heading=label('Gaussian integration by parts identifies the cross term',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sure(self):
        rows = [
            cmath(r"\hat\theta = X + g(X)", r":", r"E\|\hat\theta - \theta\|^2 = E\|X - \theta\|^2 + 2E(X - \theta)^\top g + E\|g\|^2", font_size=28),
            cmath(r"\phantom{X}", r"=", r"p + 2E\, \nabla \cdot g(X) + E\|g(X)\|^2", font_size=32),
            cmath(r"\mathrm{SURE}(X)", r"=", r"p + 2\nabla \cdot g(X) + \|g(X)\|^2", font_size=34),
            cmath(r"E\, \mathrm{SURE}", r"=", r"\text{risk}, \ \text{at every } \theta: \ \text{computable from the data}", font_size=32),
        ]
        rows[2][-1].set_color(S.ACCENT)
        rows[3][-1].set_color(ADMC)
        whys = [why(r"expand the square"), why(r"Stein's lemma"), why(r"Stein's unbiased risk estimate"), why(r"no $\theta$ needed")]
        with self.voiceover(
            "<bookmark mark='a'/> For a weakly differentiable correction with integrable squared norm and divergence,"
            " write the estimator as X plus g of X, and expand its squared error. <bookmark mark='b'/> The cross term"
            " is exactly the left side of Stein's lemma, so the risk equals p, plus twice the expected divergence of "
            "g, plus the expected squared length of g. <bookmark mark='c'/> Drop the expectations, and the quantity "
            "inside depends on the data alone: Stein's unbiased risk estimate, SURE. <bookmark mark='d'/> Its mean is"
            " the risk at every theta. We can estimate how well an estimator is doing without knowing the truth, and "
            "compare fixed candidate estimators. Selecting a minimum over many SURE values can introduce selection "
            "optimism; the selected value is not automatically unbiased for the selected rule's risk."
        ) as vo:
            heading=label('SURE estimates expected risk for a fixed regular rule',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def js(self):
        rows = [
            cmath(r"g(x)", r"=", r"-\tfrac{p - 2}{\|x\|^2}\, x", font_size=36),
            cmath(r"\nabla \cdot g", r"=", r"-(p - 2)\tfrac{p - 2}{\|x\|^2}, \ \ \|g\|^2 = \tfrac{(p - 2)^2}{\|x\|^2}", font_size=32),
            cmath(r"\mathrm{SURE}", r"=", r"p - \tfrac{(p - 2)^2}{\|X\|^2} < p", font_size=36),
            cmath(r"\text{risk}", r"=", r"p - (p - 2)^2\, E\tfrac{1}{\|X\|^2} < p \ \text{for every } \theta, \ p \ge 3", font_size=32),
        ]
        rows[2][-1].set_color(ADMC)
        rows[3][-1].set_color(ADMC)
        whys = [why(r"James--Stein's correction"), why(r"$\nabla \cdot (x/\|x\|^2) = (p - 2)/\|x\|^2$"), why(r"always below $p$"), why(r"$E\|X\|^{-2} < \infty$ needs $p \ge 3$")]
        with self.voiceover(
            "<bookmark mark='a'/> Apply it to James–Stein, whose correction pulls x toward zero by p minus two over "
            "its squared length. <bookmark mark='b'/> The divergence of x over its squared length is p minus two over"
            " that squared length, so the divergence of g is minus p minus two squared over the squared length, and "
            "g's own squared length is p minus two squared over the squared length. <bookmark mark='c'/> The two "
            "combine: SURE is p minus p minus two squared over the squared length of X, which is below p almost "
            "surely, with an arbitrary definition at the probability-zero origin. <bookmark mark='d'/> Taking "
            "expectations, the risk is below p for every theta. The condition p at least three enters through the "
            "expectation of one over the squared length, which is finite only from three dimensions on. That is "
            "Stein's paradox, proved in four lines."
        ) as vo:
            heading=label('For p at least three, James-Stein risk is below p',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def risk(self):
        d = load("stein")
        nrm = np.asarray(d["nrm"])
        A = axes([0, 40], [0, 10.8], x_length=7.4, y_length=4.4, xlabel=r"$\|\theta\|^2$", ylabel=r"risk, \ $p = 10$",
                 xticks=[0, 10, 20, 30, 40], yticks=[0, 2, 4, 6, 8, 10], center=[-2.5, 0.2, 0])
        ax = A.ax
        mle = polyline(ax, [0, 40], [10, 10], MLEC, 4)
        ex = polyline(ax, nrm, d["exact_js"], JSC, 4)
        pl = VGroup(polyline(ax, nrm, d["plus"], MMC, 3), *[Dot(ax.c2p(a, b), radius=0.06, color=MMC) for a, b in zip(nrm, d["plus"])])
        side = fit_rows(VGroup(
            label(r"blue: \ $X$, \ risk 10", font_size=22, color=MLEC),
            label(r"green: \ James--Stein, \ exact", font_size=22, color=JSC),
            label(r"$\|X\|^2$: \ a Poisson mixture of $\chi^2_{p + 2K}$", font_size=22, color=GREY_A),
            label(r"gold: \ the positive part, \ simulated", font_size=22, color=MMC),
            label(r"better: \ James--Stein is inadmissible", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The risk in ten dimensions. The blue line is X, with risk ten. <bookmark mark='b'/>"
            " The green curve is James–Stein's exact risk, <bookmark mark='c'/> computed from the fact that the "
            "squared length of X is a Poisson mixture of central chi-squares, so the expectation of one over it is a "
            "single series. <bookmark mark='d'/> In gold, simulated, the positive-part version, which refuses to "
            "shrink past zero when the squared length of X is smaller than p minus two. <bookmark mark='e'/> It is "
            "better everywhere, so James–Stein itself is inadmissible; The positive part is also inadmissible in this"
            " Gaussian squared-error problem: complete-class results require admissible rules to have an analytic "
            "generalized Bayes form, which its kink violates."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"green exact; \ gold: \ 20,000 draws per point")))
            vo.wait_until("a")
            self.play(Create(mle), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ex), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(pl), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def scatter(self):
        d = load("stein")
        s, l = np.asarray(d["sure"]), np.asarray(d["loss"])
        A = axes([min(-2.,float(s.min())-1), 12], [0, float(np.ceil(l.max()/5)*5)], x_length=5.2, y_length=5.0, xlabel=r"SURE", ylabel=r"the actual loss $\|\hat\theta - \theta\|^2$",
                 xticks=[0, 5, 10], yticks=[0, 5, 10, 15, 20], center=[-3.0, 0.1, 0])
        ax = A.ax
        k = np.ones(len(s),bool)  # show every replicate, including negative SURE
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=JSC, fill_opacity=0.7) for a, b in zip(s[k], l[k])])
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(12, 12), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"$p = 10$, \ $\theta = (1, \ldots, 1)$: \ 400 data sets", font_size=22),
            label(r"SURE can be negative; it estimates risk, not realized loss", font_size=22, color=GREY_A),
            label(rf"mean SURE {d['sure_mean']:.2f}, \ mean loss {d['loss_mean']:.2f}", font_size=22, color=JSC),
            label(rf"exact risk {d['risk_at']:.2f}: \ unbiased on average, \ noisy per data set", font_size=22, color=S.ACCENT),
        ), 5.4, 0.45, [3.7, 0.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> How good is SURE as an estimate? Four hundred data sets in ten dimensions, all means equal to one. Across, SURE; up, the loss actually suffered. <bookmark mark='b'/> SURE uses only the length of X and can even be negative. It estimates expected risk rather than the realized loss: the cloud is wide and nearly vertical. <bookmark mark='c'/> But on average the two agree: mean SURE {say(d['sure_mean'], 2)}, mean loss {say(d['loss_mean'], 2)}, <bookmark mark='d'/> and the exact risk at this theta is {say(d['risk_at'], 2)}. SURE is an unbiased estimate of risk, not a prediction of the loss, which is why it is used to compare estimators and tune them, as Part twenty-nine tuned its wavelet thresholds."
        ) as vo:
            self.play(FadeIn(A), Create(diag), FadeIn(exact_tag(r"simulated: 400 data sets")))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.004), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def hitters(self):
        d = load("stein")["em"]
        rows = [
            cmath(r"z_i = \sqrt{45}\, \arcsin(2\hat p_i - 1)", r":", r"\approx N(\theta_i, 1), \ \ i = 1, \ldots, 18", font_size=30),
            cmath(r"\text{shrink toward } \bar z", r":", rf"1 - \tfrac{{p - 3}}{{\sum (z_i - \bar z)^2}} = {d['shrink']:.3f}", font_size=32),
            cmath(r"\mathrm{SURE}", r"=", rf"{d['sure_js']:.2f} \ \text{{vs}} \ p = {d['p']}", font_size=34),
            cmath(r"\text{rest-season validation error}", r":", rf"{d['loss_js']:.2f} \ \text{{(James--Stein)}}, \ \ {d['loss_mle']:.2f} \ \text{{(raw)}}", font_size=32),
        ]
        rows[2][-1].set_color(S.ACCENT)
        rows[3][-1].set_color(ADMC)
        whys = [why(r"Efron \& Morris's transform"), why(r"$p - 3$: \ one df for $\bar z$"), why(r"computed from early-season data only"), why(r"against the rest of the season")]
        with self.voiceover(
            f"<bookmark mark='a'/> Back to Part twenty-five's eighteen hitters of 1970. Efron and Morris transformed each early-season average so that it is roughly normal with variance one. <bookmark mark='b'/> Shrinking toward the grand mean costs one degree of freedom, so the factor uses p minus three; it keeps only {say(d['shrink'], 2)} of each hitter's deviation. <bookmark mark='c'/> SURE, computed from the early-season data alone, gives an approximate Gaussian-model risk estimate of about {d['sure_js']:.0f}, against eighteen for the raw averages. <bookmark mark='d'/> Against the rest of the season, the squared errors against the remaining-season averages were {say(d['loss_js'], 1)} for James–Stein and {say(d['loss_mle'], 1)} for the raw averages. Those later averages are noisy validation targets, not the true batting probabilities. This retrospective SURE calculation uses only the early sample; its exact unbiasedness belongs to the Gaussian approximation, not the finite binomial batting data."
        ) as vo:
            heading=label('A Gaussian risk estimate differs from noisy batting validation error',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
