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
            f"<bookmark mark='a'/> The excess risk of ERM over thresholds at three noise levels. <bookmark mark='b'/> With "
            f"no noise, the realizable case, the slope is {say(sl['0.0'], 2)}: one over n. <bookmark mark='c'/> With ten "
            f"percent of labels flipped, {say(sl['0.1'], 2)}: still one over n. <bookmark mark='d'/> With forty percent "
            f"flipped, the curve sits higher, with a slope of {say(sl['0.4'], 2)} over this range, and tends to the same "
            f"rate. <bookmark mark='e'/> As long as the noise is bounded away from a half, Massart's noise condition, the "
            f"Bernstein condition holds and the rate is fast; only the constant, one over one minus two eta, grows as the "
            f"labels become nearly random."
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
        with self.voiceover(
            "<bookmark mark='a'/> The general picture is governed by how much the label noise approaches a coin flip near "
            "the decision boundary. Pascal Massart and Élodie Nédélec's condition, the noise bounded away from a half, gives "
            "the fast rate. <bookmark mark='b'/> Enno Mammen and Alexandre Tsybakov's condition interpolates: if the "
            "probability that the noise is within t of a half is at most a constant times t to the kappa, the rate is n to "
            "the minus one plus kappa over two plus kappa. <bookmark mark='c'/> Kappa zero is the slow, worst-case rate, "
            "<bookmark mark='d'/> and kappa to infinity recovers Massart's one over n."
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
            cmath(r"\text{examples}", r":", r"\text{squared loss on convex classes, \ Massart noise, \ log loss}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Bartlett \& Mendelson (2006)"), why(r"Part 51's inequality"), why(r"interpolates the rates"), why(r"when fast rates hold")]
        with self.voiceover(
            "<bookmark mark='a'/> All these fast-rate conditions share one shape, the Bernstein condition: the variance of the excess loss of a rule is bounded by a power beta of its mean. <bookmark mark='b'/> When the variance is at most the mean, Bernstein's inequality from Part fifty-one gives deviations of order one over n, not one over root n, for rules near the best one. <bookmark mark='c'/> The excess risk then falls like d log n over n to the power one over two minus beta, interpolating between the fast rate at beta one and the slow rate at beta zero. <bookmark mark='d'/> It holds for the squared loss over convex classes, under Massart's noise, and for the log loss: the common reasons a learning problem is easier than the worst case."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def regression(self):
        rows = [
            cmath(r"\text{least squares over } \mathcal F", r":", r"\text{the excess risk is } \|\hat f - f^*\|_{L_2}^2", font_size=34),
            cmath(r"\text{the critical radius}", r":", r"\delta_n: \ \mathfrak R_n(\mathcal F^*, \delta) \le \delta^2/(2\sigma)", font_size=32),
            cmath(r"\|\hat f - f^*\|^2", r"\lesssim", r"\delta_n^2", font_size=38),
            cmath(r"\text{Sobolev balls}", r":", r"\delta_n^2 \asymp n^{-2s/(2s+1)}: \ \text{Part 50's minimax rate}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"nonparametric regression"), why(r"Wainwright (2019), \ ch. 13"), why(r"localized"), why(r"rates recovered")]
        with self.voiceover(
            "<bookmark mark='a'/> Localization also gives the rates of nonparametric regression. For least squares over a function class, the excess risk is the squared L-two distance to the best function. <bookmark mark='b'/> Define the critical radius as the smallest delta at which the local Rademacher complexity of the class, around the truth, falls below delta squared over two sigma. <bookmark mark='c'/> Then the squared error is of order the critical radius squared. <bookmark mark='d'/> For Sobolev balls that is n to the minus two s over two s plus one: Part fifty's minimax rate, derived from learning theory's machinery."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fixed_point(self):
        rows = [
            cmath(r"\psi(r)", r"=", r"\mathfrak R_n\{f \in \mathcal F: E f^2 \le r\}: \ \text{local complexity}", font_size=34),
            cmath(r"r^*", r":", r"\text{the fixed point } \psi(r^*) = r^*", font_size=36),
            cmath(r"R(\hat h) - R(h^*)", r"\lesssim", r"r^* + \log(1/\delta)/n", font_size=36),
            cmath(r"\text{VC class}", r":", r"r^* \asymp d\log(n/d)/n", font_size=36),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"a sub-root function"), why(r"self-consistency"), why(r"BBM (2005)"), why(r"the fast rate")]
        with self.voiceover(
            "<bookmark mark='a'/> The machinery in one line. The local Rademacher complexity is the complexity of the part of "
            "the class with small second moment, as a function of the radius r. <bookmark mark='b'/> Its fixed point r star, "
            "where the complexity equals the radius, is the scale at which noise and signal balance. <bookmark mark='c'/> "
            "The excess risk is at most of order r star, plus a confidence term of order one over n. <bookmark mark='d'/> "
            "For a VC class, r star is d log of n over d, over n: the fast rate, derived rather than observed."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
