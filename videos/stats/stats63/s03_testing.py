from __future__ import annotations

import numpy as np
from scipy import stats as st

from videos.stats.stats63.common import *  # noqa: F403


class Testing(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter two. Differential privacy is a statement about hypothesis tests.", 2,
                            r"DP as hypothesis testing", r"The attacker's power", lit=(2022,))
        self.attacker()
        self.region_()
        self.chart()
        self.gdp()
        self.meaning()
        self.clt()

    def attacker(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Larry Wasserman and Shuheng Zhou noticed in 2010 that the definition is about tests, the "
            "subject of Part forty-six. <bookmark mark='b'/> An attacker who sees the output wants to decide between two "
            "hypotheses: the data are D, which contains your record, or D prime, which does not. <bookmark mark='c'/> Any "
            "decision rule has a type one error alpha, accusing you of being in the data when you are not, and a type two "
            "error beta, missing you when you are. <bookmark mark='d'/> Peter Kairouz, Sewoong Oh and Pramod Viswanath showed "
            "in 2015 that epsilon-delta privacy is exactly two linear constraints on every test's pair of errors.",
            [(r"\text{Wasserman \& Zhou}", r":", r"\text{privacy as testing (2010)}", 40),
             (r"H_0: D \ \ \text{vs} \ \ H_1: D'", r":", r"\text{neighbouring datasets}", 40),
             (r"\text{any test}", r":", r"(\alpha, \beta) = (\text{type I}, \ \text{type II})", 40),
             (r"(\varepsilon, \delta)\text{-DP}", r"\iff", r"\alpha + e^{\varepsilon}\beta \ge 1 - \delta, \ \ e^{\varepsilon}\alpha + \beta \ge 1 - \delta", 34)],
            [r"Part 46", r"the attacker's question", r"the two errors", r"Kairouz, \ Oh \& Viswanath (2015)"],
            colors=[(3, PRIVC)])

    def region_(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Picture the square of possible error pairs. <bookmark mark='b'/> Guessing at random, "
            "ignoring the output, achieves every point on the diagonal, alpha plus beta equals one. No release, no "
            "information. <bookmark mark='c'/> A perfect attacker would reach the corner, both errors zero. <bookmark "
            "mark='d'/> A private mechanism keeps every test above a curve, its trade-off function: the smallest type two "
            "error achievable at each type one error. The closer the curve hugs the diagonal, the more private the release.",
            [(r"\text{the square}", r":", r"(\alpha, \beta) \in [0, 1]^2", 40),
             (r"\text{guessing}", r":", r"\alpha + \beta = 1", 40),
             (r"\text{perfect attack}", r":", r"(0, 0)", 40),
             (r"T(\alpha)", r"=", r"\inf \{\beta_\phi : \alpha_\phi \le \alpha\}", 40)],
            [r"the picture", r"the diagonal", r"the corner", r"the trade-off function"],
            colors=[(3, PRIVC)])

    def chart(self):
        d = load("tradeoff")
        a = np.asarray(d["alpha"])
        A = axes([0, 1], [0, 1], x_length=5.4, y_length=5.4, xlabel=r"type I error $\alpha$", ylabel=r"type II error $\beta$",
                 xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], center=[-3.2, -0.2, 0])
        ax = A.ax
        tp = TradeoffPlot(ax)
        diag = tp.diagonal()
        reg = tp.region(a, d["dp1"], PRIVC, 0.18)
        dp1 = tp.curve(a, d["dp1"], PRIVC)
        lap = tp.curve(a, d["lap1"], WHITE, 3)
        gdp = tp.curve(a, d["gdp1"], OKC)
        fpr, fnr = np.asarray(d["attack_fpr"]), np.asarray(d["attack_fnr"])
        keep = np.arange(0, len(fpr), 6)
        dots = VGroup(*[tp.test(fpr[i], fnr[i], S.ACCENT, 0.05) for i in keep if 0 < fpr[i] < 1])
        b05 = float(np.interp(0.05, a, d["gdp1"]))
        side = side_groups([
            [(r"grey dashes: \ guessing", GREY_B)],
            [(r"purple: \ $\varepsilon = 1$, \ the forbidden zone", PRIVC), (r"white: \ the Laplace mechanism", WHITE)],
            [(r"green: \ $1$-GDP, \ $\Phi(\Phi^{-1}(1 - \alpha) - 1)$", OKC)],
            [(r"gold: \ a simulated attack on a", S.ACCENT), (r"Gaussian mean, \ 40{,}000 releases", S.ACCENT),
             (rf"at $\alpha = 0.05$: \ power {1 - b05:.2f}", S.ACCENT)],
        ], pos=(3.4, 0.0, 0), font_size=24, width=5.0)
        with self.voiceover(
            f"<bookmark mark='a'/> The trade-off plot. Guessing is the grey diagonal. <bookmark mark='b'/> Epsilon of one "
            f"forbids the purple region, bounded by two straight lines, from the two inequalities. The Laplace mechanism at "
            f"epsilon one, in white, follows those lines near the ends and bows above them in the middle. <bookmark "
            f"mark='c'/> In green, the trade-off curve of a Gaussian mechanism whose noise equals the sensitivity, called "
            f"one-GDP. Near the axes it dips into the purple region: no Gaussian mechanism is purely epsilon-private, which "
            f"is why it needs a delta. <bookmark "
            f"mark='d'/> In gold, an attack simulated forty thousand times: a released mean of a hundred values with "
            f"Gaussian noise, and an attacker who knows the other ninety-nine and thresholds the release. The attack lands on "
            f"the green curve, because the Neyman-Pearson test is the best possible. At a five percent false accusation "
            f"rate, it catches the target only {100 * (1 - b05):.0f} percent of the time."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"exact curves; \ simulated attack")))
            vo.wait_until("a")
            self.play(Create(diag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(reg), Create(dp1), FadeIn(side[1][0]))
            self.play(Create(lap), FadeIn(side[1][1]))
            vo.wait_until("c")
            self.play(Create(gdp), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.05), FadeIn(side[3]), run_time=3)
        self.wait(1.0)
        self.clear_scene()

    def gdp(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Jinshuo Dong, Aaron Roth and Weijie Su made the trade-off function itself the "
            "definition, in 2022: a mechanism is f-differentially private if every test's errors lie above f. <bookmark "
            "mark='b'/> The Gaussian family is special. Mu-GDP means telling the neighbours apart is exactly as hard as "
            "telling a normal with mean zero from one with mean mu, both with variance one. <bookmark mark='c'/> The Gaussian "
            "mechanism with sensitivity Delta and noise sigma is Delta over sigma GDP, with no slack and no inequality: it is "
            "exact. <bookmark mark='d'/> And composition is exact too: k Gaussian releases compose to the square root of "
            "the sum of their mus squared, as independent signals add.",
            [(r"f\text{-DP}", r":", r"T(M(D), M(D')) \ge f", 40),
             (r"\mu\text{-GDP}", r":", r"f = G_\mu = T(N(0, 1), N(\mu, 1))", 40),
             (r"N(0, \sigma^2) \text{ noise}", r":", r"\mu = \Delta / \sigma", 40),
             (r"\text{composition}", r":", r"G_{\mu_1} \otimes \cdots \otimes G_{\mu_k} = G_{\sqrt{\mu_1^2 + \cdots + \mu_k^2}}", 38)],
            [r"Dong, \ Roth \& Su (2022)", r"Gaussian DP", r"exact", r"in quadrature"],
            colors=[(1, OKC), (3, OKC)])

    def meaning(self):
        b = st.norm.cdf(st.norm.ppf(0.95) - 1)
        self.lad_voiceover(
            f"<bookmark mark='a'/> A mu reads directly as an attacker's power. <bookmark mark='b'/> At mu of one, a test "
            f"with a five percent false alarm rate has power one minus Phi of 1.645 minus one, which is "
            f"{say(1 - b, 2)}. <bookmark mark='c'/> At mu of a half, the power is about {say(1 - st.norm.cdf(1.645 - 0.5), 2)}, "
            f"barely above the five percent of guessing; at mu of three, it is {say(1 - st.norm.cdf(1.645 - 3), 2)}, and "
            f"privacy is mostly gone. <bookmark mark='d'/> The epsilon-delta pairs of a mu-GDP mechanism form a whole curve, "
            f"one delta for each epsilon, so a single pair throws information away. Reporting mu, or the trade-off curve, "
            f"is more honest.",
            [(r"\text{power at } \alpha", r"=", r"1 - \Phi(\Phi^{-1}(1 - \alpha) - \mu)", 40),
             (r"\mu = 1, \ \alpha = 0.05", r":", rf"\text{{power }} {1 - b:.2f}", 40),
             (r"\mu = 0.5, \ \mu = 3", r":", rf"{1 - st.norm.cdf(1.645 - 0.5):.2f}, \ \ {1 - st.norm.cdf(1.645 - 3):.2f}", 40),
             (r"(\varepsilon, \delta(\varepsilon))", r":", r"\text{a whole curve per } \mu", 40)],
            [r"interpretable", r"five times guessing", r"near guessing; \ not safe", r"report the curve"],
            colors=[(1, OKC)])

    def clt(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Why Gaussian? Dong, Roth and Su proved a central limit theorem for privacy. <bookmark "
            "mark='b'/> Compose many mechanisms, each nearly private, of any kind: the trade-off function of the "
            "composition converges to a Gaussian one, G mu, with mu determined by the components' small privacy losses. "
            "<bookmark mark='c'/> So the training of a large model, thousands of noisy steps, has a privacy guarantee that is "
            "approximately mu-GDP, whatever the individual steps. <bookmark mark='d'/> It is the Lindeberg theorem of Part "
            "forty-three, applied to the log-likelihood ratio between neighbours: the privacy loss is a sum of small "
            "independent pieces.",
            [(r"\text{many small mechanisms}", r":", r"f_1 \otimes \cdots \otimes f_k", 40),
             (r"k \to \infty", r":", r"\text{converges to } G_\mu", 40),
             (r"\text{training}", r":", r"\text{approximately } \mu\text{-GDP}", 40),
             (r"\text{why}", r":", r"\text{the privacy loss is a sum}", 40)],
            [r"a privacy CLT", r"Dong, \ Roth \& Su (2022)", r"chapter 7", r"Part 43's Lindeberg"],
            colors=[(1, OKC)])
