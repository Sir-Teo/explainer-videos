from __future__ import annotations

import numpy as np

from videos.stats.stats47.common import *  # noqa: F403


class Contiguity(VoiceoverScene):
    def construct(self):
        self.card()
        self.first()
        self.noncontig()
        self.third()
        self.chart()
        self.trinity()

    def card(self):
        card = chapter_card(8, r"Contiguity and local power", r"Moving a limit from the null to the alternative", part=PART)
        with self.voiceover("Chapter eight. Contiguity and local power: moving a limit from the null to the alternative."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def first(self):
        rows = [
            cmath(r"Q_n \lhd P_n", r":", r"P_n(A_n) \to 0 \ \Rightarrow \ Q_n(A_n) \to 0, \ \text{for every sequence } A_n", font_size=30),
            cmath(r"\log \tfrac{dQ_n}{dP_n} \Rightarrow N(-\tfrac12\sigma^2, \sigma^2) \text{ under } P_n", r"\Rightarrow", r"Q_n \lhd P_n", font_size=30),
            cmath(r"\text{LAN}", r"\Rightarrow", r"P^n_{\theta + h/\sqrt n} \lhd P^n_\theta \ \text{and vice versa}", font_size=32),
            cmath(r"\text{so}", r":", r"o_P(1) \text{ under the null } \Rightarrow \ o_P(1) \text{ under local alternatives}", font_size=30),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"an asymptotic absolute continuity"), why(r"Le Cam's first lemma"), why(r"chapter 7"), why(r"negligible stays negligible")]
        with self.voiceover(
            "<bookmark mark='a'/> A sequence of alternatives Q n is contiguous to the nulls P n if events that become "
            "impossible under the null also become impossible under the alternative: an asymptotic version of absolute "
            "continuity. <bookmark mark='b'/> Le Cam's first lemma: if the log-likelihood ratio converges under the null to "
            "a normal with mean minus half its variance, the alternatives are contiguous. <bookmark mark='c'/> LAN gives "
            "exactly that, so local alternatives are contiguous to the null, and the null to them. <bookmark mark='d'/> The "
            "practical consequence: anything negligible under the null, like the remainders in chapters two to five, is "
            "also negligible under local alternatives. We can do our expansions once, under the null."
        ) as vo:
            heading=label('Contiguity transfers vanishing-probability events',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def third(self):
        rows = [
            cmath(r"(T_n, \Lambda_n)", r"\overset{P_n}\Rightarrow", r"N\Big(\begin{pmatrix} 0 \\ -\sigma^2/2 \end{pmatrix}, \begin{pmatrix} 1 & \tau \\ \tau & \sigma^2 \end{pmatrix}\Big)", font_size=30),
            cmath(r"\Rightarrow", r"\;", r"T_n \overset{Q_n}\Rightarrow N(\tau, 1)", font_size=36),
            cmath(r"T_n = \tfrac{1}{\sqrt n}\textstyle\sum \psi(X_i)/\sigma_\psi", r":", r"\tau = h\, \mathrm{Cov}(\psi, \dot\ell)/\sigma_\psi", font_size=30),
            cmath(r"\text{local power}", r"=", r"1 - \Phi(z_\alpha - \tau(h))", font_size=36),
        ]
        rows[1][-1].set_color(S.ACCENT)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"joint normality under the null"), why(r"Le Cam's third lemma"), why(r"a linear statistic"), why(r"the shift is a covariance")]
        with self.voiceover(
            "<bookmark mark='a'/> Le Cam's third lemma does the real work. Suppose a statistic and the log-likelihood"
            " ratio are jointly normal in the limit under the null, with covariance tau. <bookmark mark='b'/> Then "
            "under the local alternative the statistic is still normal with the same variance, but its mean has "
            "shifted by exactly tau. <bookmark mark='c'/> For a standardized linear statistic, tau is h times the "
            "covariance of its psi with the score, over psi's standard deviation. <bookmark mark='d'/> So the local "
            "power of the test that rejects for large T is one minus Phi of z alpha minus tau. For asymptotically "
            "linear statistics with the stated joint Gaussian limit, this covariance determines the local mean shift."
            " Arbitrary tests need not have such a representation."
        ) as vo:
            heading=label('A Gaussian likelihood tilt shifts a statistic by its covariance',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("contig")
        hh = np.asarray(d["hh"])
        A = axes([0, 4], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=r"$h = \sqrt n\, \mu$", ylabel=r"power, \ one-sided 5\%",
                 xticks=[0, 1, 2, 3, 4], yticks=[0, 0.05, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        ct = polyline(ax, hh, d["lp_t"], MLEC, 4)
        cs = polyline(ax, hh, d["lp_sign"], HODC, 4)
        dt = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=MLEC) for a, b in zip(d["hs"], d["sim_t"])])
        ds = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=HODC) for a, b in zip(d["hs"], d["sim_sign"])])
        side = fit_rows(VGroup(
            label(r"normal data, \ $n = 100$, \ shift $h/\sqrt n$", font_size=22),
            label(r"blue: \ the $t$ test: \ $\tau = h$", font_size=22, color=MLEC),
            label(r"red: \ the sign test: \ $\tau = h\sqrt{2/\pi}$", font_size=22, color=HODC),
            label(r"curves: \ the third lemma; \ dots: \ simulated", font_size=22, color=GREY_A),
            label(r"power at $h$ for the sign test \ = \ power at $0.80h$ for $t$", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Normal data, a hundred observations, a mean of h over root n. <bookmark mark='b'/> "
            "For the t test, tau is h itself: the blue curve. <bookmark mark='c'/> For the sign test, the covariance "
            "of the sign with the score is the root of two over pi, about point eight: the red curve. <bookmark "
            "mark='d'/> The dots are simulated powers, and they are close to the third lemma's asymptotic curves. The"
            " finite-sample t test uses its exact t quantile; the sign test randomizes at its binomial boundary for "
            "exact five percent null size. The plotted sign dots average its conditional rejection probability. "
            "<bookmark mark='e'/> The sign test at h has the power the t test has at point eight h: it needs one over"
            " two over pi, about fifty-seven percent more data, for the same power."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"asymptotic curves; \ dots: \ 20,000 samples; exact-level $t$ and randomized sign rules")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ct), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(dt), FadeIn(ds), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def trinity(self):
        rows = fit_rows(VGroup(
            label(r"the Wald, \ score and likelihood ratio tests:", font_size=28, color=GREY_A),
            label(r"all asymptotically $\chi^2_q$ under $H_0$, \ by Wilks and Slutsky", font_size=26),
            label(r"regular model: \ same projected local noncentrality; \ use efficient information with nuisance", font_size=26, color=GOODC),
            label(r"equivalent to first order; \ they differ only at second order, \ and under misspecification", font_size=26, color=S.ACCENT),
            label(r"Part 22's trinity, \ explained", font_size=26, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The third lemma settles Part twenty-two's trinity of tests. <bookmark mark='b'/> "
            "The Wald, score and likelihood ratio statistics are all asymptotically chi-square under the null. "
            "<bookmark mark='c'/> Under local alternatives, all three converge to the same noncentral chi-square, "
            "with noncentrality the information-weighted squared component of the local shift normal to the null. For"
            " a point null without nuisance directions this is h transposed I h; with nuisance parameters it uses "
            "efficient information or the corresponding projection. <bookmark mark='d'/> So they are equivalent to "
            "first order, and differ only at second order, or when the model is misspecified. <bookmark mark='e'/> "
            "Which is why, in practice, their disagreement is a warning sign about the sample size or the model."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def noncontig(self):
        rows = [
            cmath(r"\text{a fixed alternative } \theta_1 \ne \theta_0", r":", r"\tfrac1n \log \tfrac{dP^n_{\theta_1}}{dP^n_{\theta_0}} \to -\mathrm{KL}(\theta_0, \theta_1) \ \text{under } \theta_0", font_size=28),
            cmath(r"\Lambda_n", r"\to", r"-\infty: \ \text{the two are asymptotically singular}", font_size=34),
            cmath(r"\text{every consistent test}", r":", r"\text{power} \to 1: \ \text{nothing left to compare}", font_size=32),
            cmath(r"\text{the right scale}", r":", r"\theta_0 + h/\sqrt n: \ \text{where power stays between } \alpha \text{ and } 1", font_size=30),
        ]
        rows[1][-1].set_color(HODC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Part 43's KL rate"), why(r"not contiguous"), why(r"degenerate comparisons"), why(r"why $1/\sqrt n$")]
        with self.voiceover(
            "<bookmark mark='a'/> For contrast, consider independent observations and a distinct identifiable fixed "
            "alternative with finite positive KL divergence. Under the null, the log-likelihood ratio per observation"
            " converges to minus the Kullback–Leibler divergence between the two distributions, <bookmark mark='b'/> "
            "so the log-likelihood ratio itself runs off to minus infinity: the null and the alternative become "
            "perfectly distinguishable, singular rather than contiguous. <bookmark mark='c'/> Tests consistent "
            "against that alternative then have power tending to one, and there is nothing left to compare. <bookmark"
            " mark='d'/> That is why local alternatives, at distance one over root n, are the right scale: the "
            "regular LAN scale at which nontrivial local power can be compared. Nonregular models can have different "
            "rates, and tests can be told apart."
        ) as vo:
            heading=label('Identifiable fixed alternatives separate as information grows',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
