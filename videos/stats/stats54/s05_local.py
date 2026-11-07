from __future__ import annotations

import numpy as np

from videos.stats.stats54.common import *  # noqa: F403


class Localization(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.chart()
        self.conditions()
        self.bernstein()
        self.fixed_point()
        self.regression()

    def card(self):
        card = chapter_card(4, r"Localization and fast rates", r"When the gap shrinks like $1/n$", lit=(2005,), part=PART)
        with self.voiceover("Chapter four. Localization and fast rates: when the gap shrinks like one over n."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"\text{the uniform deviation}", r":", r"\text{a sup over the whole class: \ } 1/\sqrt n", font_size=34),
            cmath(r"\text{but } \hat h", r":", r"\text{lies near the best rule, \ where variances are small}", font_size=34),
            cmath(r"\mathrm{Var}(\ell_h - \ell_{h^*})", r"\le", r"B\,\big(R(h) - R(h^*)\big): \ \text{a Bernstein condition}", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"R(\hat h) - R(h^*) \lesssim d\log n / n", font_size=36),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"chapter 1's teal line"), why(r"look locally"), why(r"variance $\lesssim$ mean"), why(r"Bartlett, \ Bousquet \& Mendelson (2005)")]
        heading = label('Small excess-loss variance can support faster estimation rates', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Chapter one's puzzle: the uniform deviation falls like one over root n, but the excess risk "
            "of the chosen rule fell like one over n. <bookmark mark='b'/> The reason is that the chosen rule lies near the "
            "best one, and near the best rule the excess losses have small variance. <bookmark mark='c'/> If the variance "
            "of the excess loss is at most a constant times its mean, a Bernstein condition, <bookmark mark='d'/> then "
            "Bernstein's inequality applied to a shrinking neighbourhood gives an excess risk of order d log n over n. Peter "
            "Bartlett, Olivier Bousquet and Shahar Mendelson's local Rademacher complexities of 2005, and Vladimir "
            "Koltchinskii's work of 2006, made this the general method."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("erm")
        ln = np.log10(d["ns"])
        A = axes([1.3, 3.3], [-3.4, -1.0], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\log_{10}$ excess risk of ERM",
                 xticks=[np.log10(25), 2, np.log10(400), np.log10(1600)], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[-3, -2.5, -2, -1.5, -1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"0.0": GOODC, "0.1": CLASSC, "0.4": BADC}
        cs, sl = {}, {}
        for k, c in cols.items():
            v = np.log10(d["by_eta"][k]["excess"])
            cs[k] = VGroup(polyline(ax, ln, v, c, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=c) for a, b in zip(ln, v)])
            sl[k] = float(np.polyfit(ln, v, 1)[0])
        e = d["by_eta"]
        side = fit_rows(VGroup(
            label(r"thresholds; \ label noise $\eta$, \ 200 data sets a point", font_size=22),
            label(rf"green: \ $\eta = 0$, \ realizable: \ slope {sl['0.0']:.2f}", font_size=22, color=GOODC),
            label(rf"gold: \ $\eta = 0.1$: \ slope {sl['0.1']:.2f}", font_size=22, color=CLASSC),
            label(rf"red: \ $\eta = 0.4$: \ slope {sl['0.4']:.2f}, \ a larger constant", font_size=22, color=BADC),
            label(r"bounded noise ($\eta < 1/2$): \ fast rates; \ $1/(1 - 2\eta)$ in the constant", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The excess risk of ERM over thresholds at three noise levels. <bookmark mark='b'/> With no noise, the realizable case, the slope is {say(sl['0.0'], 2)}: one over n. <bookmark mark='c'/> With ten percent of labels flipped, {say(sl['0.1'], 2)}: still one over n. <bookmark mark='d'/> With forty percent flipped, the curve sits higher, with a slope of {say(sl['0.4'], 2)} over this range, and tends to the same rate. <bookmark mark='e'/> Here the Bayes threshold belongs to the class. With noise bounded away from a half, the Bernstein condition holds and the rate is fast; only the constant, one over one minus two eta, grows as the labels become nearly random."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs["0.0"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs["0.1"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs["0.4"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def conditions(self):
        rows = [
            cmath(r"\text{Massart noise}", r":", r"|2\eta(x) - 1| \ge h > 0: \ \text{rate } d\log n/(nh)", font_size=34),
            cmath(r"\text{Tsybakov noise}", r":", r"P(|2\eta(X) - 1| \le t) \le Ct^{\kappa}: \ \text{rate } n^{-(1+\kappa)/(2+\kappa)}", font_size=32),
            cmath(r"\kappa = 0", r":", r"n^{-1/2}: \ \text{the worst case}", font_size=36),
            cmath(r"\kappa \to \infty", r":", r"n^{-1}: \ \text{Massart}", font_size=36),
        ]
        rows[1][-1].set_color(CLASSC)
        whys = [why(r"Massart \& Nédélec (2006)"), why(r"Mammen \& Tsybakov (1999)"), why(r"noise at the boundary"), why(r"a clean margin")]
        heading = label('Noise assumptions give fast rates when the Bayes rule is in the class', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Massart noise bounds the conditional label probability away from a half. If the Bayes classifier belongs to the VC class, this gives the displayed fast rate, with confidence and complexity terms understood. <bookmark mark='b'/> Tsybakov's condition limits the mass near the decision boundary. For suitable classes containing the Bayes rule, it gives the displayed exponent, with class-dependent factors. <bookmark mark='c'/> Kappa zero yields the worst-case square-root rate. <bookmark mark='d'/> A fixed positive noise gap yields the Massart regime. Under misspecification the same conclusion needs an appropriate Bernstein condition around the best rule in the class."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bernstein(self):
        rows = [
            cmath(r"\text{Bernstein condition}", r":", r"E\big[(\ell_f - \ell_{f^*})^2\big] \le B\,\big(E[\ell_f - \ell_{f^*}]\big)^{\beta}", font_size=34),
            cmath(r"\text{variance} \lesssim \text{mean}", r"\Rightarrow", r"\text{Bernstein's inequality is } 1/n, \ \text{not } 1/\sqrt n, \text{ near } f^*", font_size=32),
            cmath(r"\text{rate}", r":", r"\big(d\log n/n\big)^{1/(2-\beta)}: \ \beta = 1 \text{ fast}, \ \beta = 0 \text{ slow}", font_size=34),
            cmath(r"\text{examples}", r":", r"\text{bounded regression; Bayes-in-class Massart; bounded log loss}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Bartlett \& Mendelson (2006)"), why(r"Part 51's inequality"), why(r"interpolates the rates"), why(r"when fast rates hold")]
        heading = label('Second-moment control and local complexity jointly determine the rate', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> This second-moment Bernstein condition, with beta between zero and one, controls excess losses by their mean. It is stronger than merely bounding the variance. <bookmark mark='b'/> At beta one, Bernstein concentration and localization can yield fast rates. The concentration inequality alone does not supply the class's local complexity. <bookmark mark='c'/> With VC-type entropy, the schematic rate interpolates between fast and slow as beta varies. <bookmark mark='d'/> Examples include bounded squared-loss regression under suitable convexity and noise assumptions, classification with a Bayes rule in the class and Massart noise, and suitably bounded log loss. None holds without regularity conditions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def regression(self):
        rows = [
            cmath(r"\text{least squares over } \mathcal F", r":", r"f^*=E[Y\mid X]\in\mathcal F:\quad \text{excess}=\|\hat f-f^*\|_2^2", font_size=34),
            cmath(r"\text{the critical radius}", r":", r"\delta_n: \ \mathfrak R_n(\mathcal F^*, \delta) \le \delta^2/(2\sigma)", font_size=32),
            cmath(r"\|\hat f - f^*\|^2", r"\lesssim", r"\delta_n^2", font_size=38),
            cmath(r"\text{Sobolev balls}", r":", r"\delta_n^2 \asymp n^{-2s/(2s+1)}: \ \text{Part 50's minimax rate}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"nonparametric regression"), why(r"Wainwright (2019), \ ch. 13"), why(r"localized"), why(r"rates recovered")]
        heading = label('Well-specified squared-loss excess equals squared prediction distance', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> In well-specified squared-loss regression, with the regression function in the class, excess risk equals squared L-two distance to that function. For a misspecified convex projection there is an additional nonnegative cross term. <bookmark mark='b'/> Under bounded or sub-Gaussian design and noise assumptions, suitable localized and multiplier-process bounds define a critical radius. <bookmark mark='c'/> The squared error is then controlled by a constant times the radius squared. <bookmark mark='d'/> For a one-dimensional Sobolev ball this recovers n to the minus two s over two s plus one. In input dimension d, the denominator becomes two s plus d."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fixed_point(self):
        rows = [
            cmath(r"\psi(r)", r"=", r"\text{sub-root upper bound for localized excess-loss star hull}", font_size=34),
            cmath(r"r^*", r":", r"\text{the fixed point } \psi(r^*) = r^*", font_size=36),
            cmath(r"R(\hat h) - R(h^*)", r"\lesssim", r"r^* + \log(1/\delta)/n", font_size=36),
            cmath(r"\text{VC class}", r":", r"r^* \lesssim d\log(en/d)/n\quad(d\le n)", font_size=36),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"a sub-root function"), why(r"self-consistency"), why(r"BBM (2005)"), why(r"the fast rate")]
        heading = label('A localized excess-loss upper bound defines the critical scale', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Apply local complexity to the star hull of excess losses around the optimal rule. A sub-root upper bound absorbs the Bernstein constants. <bookmark mark='b'/> Its positive fixed point identifies the relevant scale. This is not an arbitrary raw class with an arbitrary fixed point. <bookmark mark='c'/> Under the boundedness, Bernstein and empirical-process assumptions, an excess-risk bound is of order that radius plus the confidence term. <bookmark mark='d'/> A VC-type entropy upper bound gives a fast-rate radius of order d times a logarithm over n, capped in the appropriate regime; some classes admit sharper rates."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
