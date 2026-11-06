from __future__ import annotations

import numpy as np

from videos.stats.stats50.common import *  # noqa: F403


class Pinsker(VoiceoverScene):
    def construct(self):
        self.card()
        self.linear()
        self.weights()
        self.table()
        self.projection()
        self.meaning()
        self.prior()

    def card(self):
        card = chapter_card(2, r"Linear estimators and Pinsker's theorem", r"An exact minimax constant, \ in infinite dimensions", lit=(1980,), part=PART)
        with self.voiceover("Chapter two. Linear estimators and Pinsker's theorem: an exact minimax constant, in infinite dimensions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def linear(self):
        rows = [
            cmath(r"\hat\theta_k = c_k\, y_k", r":", r"E(\hat\theta_k - \theta_k)^2 = (1 - c_k)^2 \theta_k^2 + c_k^2 \varepsilon^2", font_size=32),
            cmath(r"\sup_{\Theta(\alpha, C)}", r":", r"\text{the worst } \theta \text{ puts its energy where } (1 - c_k)^2/a_k^2 \text{ is largest}", font_size=30),
            cmath(r"\text{Pinsker (1980)}", r":", r"c_k = (1 - a_k/\mu)_+, \ \ \varepsilon^2 \textstyle\sum a_k(\mu - a_k)_+ = C^2", font_size=32),
            cmath(r"R_L(\varepsilon)", r"=", r"\varepsilon^2 \textstyle\sum_k (1 - a_k/\mu)_+ \ \ \text{and} \ \ R^* \sim R_L \ \text{as } \varepsilon \to 0", font_size=32),
        ]
        rows[2][-1].set_color(LINC)
        rows[3][-1].set_color(HYPC)
        whys = [why(r"bias$^2$ + variance, \ per coordinate"), why(r"$a_k = k^\alpha$"), why(r"tapered shrinkage"), why(r"linear rules are asymptotically minimax")]
        with self.voiceover(
            "<bookmark mark='a'/> Consider linear estimators, each coefficient multiplied by a weight c k. Each coordinate's "
            "risk is a squared bias, one minus c k squared times theta k squared, plus a variance, c k squared times epsilon "
            "squared. <bookmark mark='b'/> Over the ellipsoid, the worst parameter puts its energy where the bias is largest "
            "relative to the ellipsoid's cost. <bookmark mark='c'/> Mark Pinsker solved the minimax problem in 1980. The best "
            "weights taper linearly in the ellipsoid's weights, one minus a k over mu, cut off at zero, with mu chosen so "
            "that a certain sum equals C squared. <bookmark mark='d'/> And then the surprise: this linear rule is not just "
            "the best linear rule. Its risk is asymptotically equal to the minimax risk over all estimators, linear or not. "
            "Pinsker found the exact constant, a rarity in nonparametric statistics."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def weights(self):
        d = load("pinsker")
        k = np.asarray(d["k"], float)
        A = axes([0, 120], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=r"coefficient $k$", ylabel=r"Pinsker's weight $c_k$",
                 xticks=[0, 20, 40, 60, 80, 100, 120], yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        w1 = polyline(ax, k, d["weights"]["0.03"], LINC, 4)
        w2 = polyline(ax, k, d["weights"]["0.003"], UPC, 4)
        n1 = int(np.sum(np.asarray(d["weights"]["0.03"]) > 0))
        n2 = int(np.sum(np.asarray(d["weights"]["0.003"]) > 0))
        side = fit_rows(VGroup(
            label(r"Sobolev, \ $\alpha = 1$, \ $C = 1$", font_size=22),
            label(rf"purple: \ $\varepsilon = 0.03$: \ {n1} coefficients kept", font_size=22, color=LINC),
            label(rf"blue: \ $\varepsilon = 0.003$: \ {n2} kept", font_size=22, color=UPC),
            label(r"a straight taper, \ not a sharp cut-off", font_size=22, color=HYPC),
            label(r"less noise: \ a longer taper, \ more detail", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Pinsker's weights for a Sobolev ball with one derivative. <bookmark mark='b'/> At noise "
            f"level point oh three, the weights fall linearly from almost one to zero by coefficient {n1}. <bookmark "
            f"mark='c'/> At point oh oh three, ten times less noise, the taper stretches to coefficient {n2}. <bookmark "
            f"mark='d'/> The shape is a straight ramp, not the sharp cut-off of a projection estimator, and the difference "
            f"is worth a constant factor in risk. <bookmark mark='e'/> Less noise lets more coefficients through, which is "
            f"how the rate arises."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(w1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(w2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("pinsker")
        rows = [[r"$\varepsilon$", r"$R_L(\varepsilon)$", r"$P(\alpha)\,C^{2/3}\varepsilon^{4/3}$", r"ratio", r"coefficients used"]]
        for r in d["rows"]:
            rows.append([f"{r['eps']:g}", f"{r['risk']:.3e}", f"{r['asym']:.3e}", f"{r['risk'] / r['asym']:.4f}", f"{r['N']}"])
        tab = table_rows(rows, font_size=28, col_buff=0.8, row_buff=0.34, colors=[GREY_B] + [None] * 5)
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.8, 0])
        for i in range(1, 6):
            tab[i][3].set_color(HYPC)
        foot = label(rf"Pinsker's constant $P(1) = 3^{{1/3}}(1/2)^{{2/3}} = {d['const']:.4f}$; \ $P(2) = {d['const2']:.4f}$", font_size=24, color=GREY_A).move_to([0, -1.6, 0])
        foot2 = label(r"the rate $\varepsilon^{4\alpha/(2\alpha+1)} = n^{-2\alpha/(2\alpha+1)}$, \ and its constant, \ exactly", font_size=24, color=HYPC).move_to([0, -2.4, 0])
        r0, r4 = d["rows"][0], d["rows"][-1]
        with self.voiceover(
            f"<bookmark mark='a'/> Pinsker's linear minimax risk, computed exactly, against his asymptotic formula: the "
            f"constant P of alpha, times C to the two over two alpha plus one, times epsilon to the four alpha over two alpha "
            f"plus one. The ratio is {say(r0['risk'] / r0['asym'], 3)} at noise point one and {say(r4['risk'] / r4['asym'], 4)} at "
            f"point oh oh one, converging to one. <bookmark mark='b'/> With epsilon equal to one over root n this is Stone's "
            f"rate, n to the minus two alpha over two alpha plus one, with the exact constant: for one derivative, "
            f"{say(d['const'], 3)}."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(exact_tag(r"exact")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def projection(self):
        rows = [
            cmath(r"\hat\theta_k = y_k \mathbf 1\{k \le N\}", r":", r"\text{keep the first } N, \ \text{drop the rest}", font_size=34),
            cmath(r"\sup_{\Theta} R", r"=", r"N\varepsilon^2 + C^2 (N + 1)^{-2\alpha}: \ \text{variance plus the worst tail}", font_size=32),
            cmath(r"N^* \asymp (C/\varepsilon)^{2/(2\alpha + 1)}", r"\Rightarrow", r"\text{the same rate as Pinsker, \ a worse constant}", font_size=32),
            cmath(r"\text{the constant's ratio}", r":", r"\text{1.3--1.5 for } \alpha = 1: \ \text{the taper is worth a third}", font_size=32),
        ]
        rows[1][-1].set_color(UPC)
        rows[3][-1].set_color(LINC)
        whys = [why(r"the projection estimator"), why(r"nature puts all its energy at $N + 1$"), why(r"Part 29's bandwidth, \ in disguise"), why(r"chapter 6 measures it")]
        with self.voiceover(
            "<bookmark mark='a'/> Compare the simplest linear rule: keep the first N coefficients as they are and drop the "
            "rest, a projection. <bookmark mark='b'/> Its worst-case risk is N epsilon squared from the kept noise, plus the "
            "largest tail nature can hide beyond N, which is C squared times N plus one to the minus two alpha. <bookmark "
            "mark='c'/> Balancing the two gives the same rate as Pinsker's, with N growing like C over epsilon to the two "
            "over two alpha plus one: the projection's N plays the role of Part twenty-nine's bandwidth. <bookmark mark='d'/> "
            "But the constant is worse, by a factor of about one point three to one point five for one derivative. Tapering "
            "the weights instead of cutting them off is worth about a third of the risk."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def meaning(self):
        rows = [
            cmath(r"\text{risk} \propto n^{-2\alpha/(2\alpha+1)}", r"\Rightarrow", r"\text{a factor } c \text{ in risk} = c^{(2\alpha+1)/(2\alpha)} \text{ in sample size}", font_size=30),
            cmath(r"\alpha = 1, \ c = 1.4", r":", r"1.4^{3/2} \approx 1.66: \ \text{the projection needs 66\% more data}", font_size=32),
            cmath(r"\text{parametric}, \ \text{risk} \propto 1/n", r":", r"\text{a factor } c \text{ in risk} = c \text{ in sample size}", font_size=32),
            cmath(r"\text{the slower the rate}", r":", r"\text{the more data a constant is worth}", font_size=34),
        ]
        rows[1][-1].set_color(LINC)
        rows[3][-1].set_color(HYPC)
        whys = [why(r"invert the rate"), why(r"Pinsker vs.\ projection"), why(r"Part 45's efficiency"), why(r"constants matter")]
        with self.voiceover(
            "<bookmark mark='a'/> Is a constant factor worth caring about? Invert the rate. If the risk falls like n to the "
            "minus two alpha over two alpha plus one, then a factor c in risk is a factor c to the two alpha plus one over two "
            "alpha in sample size. <bookmark mark='b'/> For one derivative, a projection estimator one point four times worse "
            "than Pinsker's needs about sixty-six percent more data to match it. <bookmark mark='c'/> In a parametric problem "
            "the exchange rate is one to one. <bookmark mark='d'/> The slower the rate, the more data a constant factor is "
            "worth: in nonparametric problems, constants are not a detail."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def prior(self):
        d = load("pinsker")
        rows = [
            cmath(r"\text{the least favourable prior}", r":", r"\theta_k \sim N(0, \tau_k^2), \ \ \tau_k^2 = \varepsilon^2 (\mu/a_k - 1)_+", font_size=32),
            cmath(r"\text{its Bayes rule}", r":", r"\frac{\tau_k^2}{\tau_k^2 + \varepsilon^2} = 1 - \frac{a_k}{\mu}: \ \text{Pinsker's weights, \ exactly}", font_size=32),
            cmath(r"\text{Bayes risk}", r"=", r"\textstyle\sum \tau_k^2 \varepsilon^2/(\tau_k^2 + \varepsilon^2) = R_L: \ \text{a saddle point}", font_size=32),
            cmath(r"\text{why linear wins}", r":", r"\text{the prior concentrates on the ellipsoid as } \varepsilon \to 0", font_size=32),
        ]
        rows[1][-1].set_color(LINC)
        rows[2][-1].set_color(HYPC)
        whys = [why(r"Part 45's least favourable priors"), why(r"Part 25's shrinkage"), why(r"minimax $=$ Bayes"), why(r"so the lower bound applies to all rules")]
        r = d["rows"][1]
        with self.voiceover(
            f"<bookmark mark='a'/> Why are linear rules good enough? Put a Gaussian prior on the coefficients, with variances "
            f"that vanish beyond the cut-off. <bookmark mark='b'/> Its Bayes rule is the posterior mean, which shrinks each "
            f"coordinate by tau squared over tau squared plus epsilon squared: and that is exactly Pinsker's weight. "
            f"<bookmark mark='c'/> Its Bayes risk equals the linear minimax risk, to every digit: at epsilon point oh three "
            f"both are {r['risk']:.6f}. A Bayes risk is a lower bound for every estimator, so we have a saddle point, Part "
            f"forty-five's least favourable prior in infinite dimensions. <bookmark mark='d'/> The prior does not quite live "
            f"on the ellipsoid, but it concentrates there as the noise shrinks, which is why the result is asymptotic."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
