from __future__ import annotations

import numpy as np

from videos.stats.stats46.common import *  # noqa: F403


class MLR(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.ratios()
        self.karlin()
        self.twosided()
        self.cauchy()

    def card(self):
        card = chapter_card(2, r"Monotone likelihood ratio and Karlin--Rubin", r"When one test is best against every alternative", lit=(1956,), part=PART)
        with self.voiceover("Chapter two. Monotone likelihood ratio and the Karlin–Rubin theorem: when one test is best against every alternative."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"\text{MLR in } T", r":", r"\theta_1 > \theta_0 \Rightarrow \tfrac{f_{\theta_1}(x)}{f_{\theta_0}(x)} \text{ is nondecreasing in } T(x)", font_size=30),
            cmath(r"f_\theta(x)", r"=", r"h(x)\, e^{\eta(\theta) T(x) - A(\theta)}, \ \ \eta \uparrow", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"\tfrac{f_{\theta_1}}{f_{\theta_0}} = e^{(\eta(\theta_1) - \eta(\theta_0)) T(x) + \text{const}}: \ \text{MLR}", font_size=32),
            cmath(r"\text{also}", r":", r"U(0, \theta), \ \text{the noncentral } t, \ \chi^2, \ F, \ \text{the hypergeometric}", font_size=30),
        ]
        rows[0][-1].set_color(S.ACCENT)
        rows[2][-1].set_color(UMPC)
        whys = [why(r"a total ordering of the evidence"), why(r"Part 45's families"), why(r"one exponent"), why(r"not only exponential families")]
        with self.voiceover(
            "<bookmark mark='a'/> A family has a monotone likelihood ratio in a statistic T if, for any larger parameter "
            "against any smaller one, the likelihood ratio is a nondecreasing function of T. Larger T is always evidence "
            "for larger theta. <bookmark mark='b'/> One-parameter exponential families with an increasing natural "
            "parameter, <bookmark mark='c'/> have it automatically, since the ratio is the exponential of a positive "
            "multiple of T. <bookmark mark='d'/> So do the uniform on zero to theta, the noncentral t, chi-square and F "
            "families in their noncentrality, and the hypergeometric."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ratios(self):
        d = load("mlr")
        A = axes([-0.5, 20.5], [-8, 11], x_length=5.4, y_length=3.6, xlabel=r"$x$", ylabel=r"$\log \frac{f_{0.5}}{f_{0.3}}$, \ Bin(20)",
                 xticks=[0, 10, 20], yticks=[-5, 0, 5, 10], center=[-3.4, 0.7, 0])
        B = axes([-6, 8], [0, 2.8], x_length=5.4, y_length=3.6, xlabel=r"$x$", ylabel=r"$\frac{f(x - 1)}{f(x)}$, \ Cauchy",
                 xticks=[-5, 0, 5], yticks=[0, 1, 2], center=[3.4, 0.7, 0])
        lb = VGroup(polyline(A.ax, d["x"], np.log(d["lr_bin"]), UMPC, 4), *[Dot(A.ax.c2p(a, np.log(b)), radius=0.05, color=UMPC) for a, b in zip(d["x"], d["lr_bin"])])
        lc = polyline(B.ax, d["xs"], d["lr_cauchy"], REJC, 4)
        one = DashedLine(B.ax.c2p(-6, 1), B.ax.c2p(8, 1), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"left: \ the binomial's log ratio, \ a straight line in $x$: \ monotone", font_size=22, color=UMPC),
            label(rf"right: \ Cauchy location, \ $\theta = 1$ vs $0$: \ peaks at $x = {d['cauchy_max']:.1f}$, \ then falls back to 1", font_size=22, color=REJC),
            label(r"a very large $x$ is no evidence for $\theta = 1$ over $\theta = 0$: \ no MLR", font_size=22, color=S.ACCENT),
        ), 12.4, 0.25, [0, -2.45, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Two pictures. On the left, the binomial's log likelihood ratio for p equal to point five "
            f"against point three: a straight line in the number of successes, increasing. <bookmark mark='b'/> On the "
            f"right, the Cauchy location family, theta equal to one against zero. The ratio rises to a peak near x equal to "
            f"{say(d['cauchy_max'], 1)} and then falls back toward one. <bookmark mark='c'/> A gigantic observation is "
            f"equally surprising under both values, so it is no evidence for either: heavy tails destroy the monotone "
            f"ordering."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), Create(one), FadeIn(exact_tag(r"exact densities")))
            vo.wait_until("a")
            self.play(Create(lb), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lc), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def karlin(self):
        rows = [
            cmath(r"H_0: \theta \le \theta_0", r"\ \text{vs}\ ", r"H_1: \theta > \theta_0, \ \ \text{MLR in } T", font_size=32),
            cmath(r"\phi^*", r"=", r"\mathbf 1\{T > c\} + \gamma\, \mathbf 1\{T = c\}, \ \ E_{\theta_0}\phi^* = \alpha", font_size=32),
            cmath(r"\text{each } \theta_1 > \theta_0", r":", r"\phi^* \text{ is the NP test of } \theta_0 \text{ vs } \theta_1 \Rightarrow \text{most powerful}", font_size=30),
            cmath(r"\beta(\theta) = E_\theta \phi^*", r"\uparrow", r"\Rightarrow \ \sup_{\theta \le \theta_0} \beta = \alpha: \ \text{UMP}", font_size=32),
        ]
        rows[1][-1].set_color(UMPC)
        rows[3][-1].set_color(UMPC)
        whys = [why(r"one-sided, \ composite"), why(r"a threshold on $T$"), why(r"chapter 1, \ for every $\theta_1$"), why(r"Karlin \& Rubin (1956)")]
        with self.voiceover(
            "<bookmark mark='a'/> Samuel Karlin and Herman Rubin's theorem of 1956. Test theta at most theta nought against "
            "theta above it, in a family with a monotone likelihood ratio. <bookmark mark='b'/> Reject when T exceeds c, "
            "randomizing at c, with size alpha at theta nought. <bookmark mark='c'/> Against any single alternative above "
            "theta nought, this is a likelihood-ratio threshold, so by chapter one it is most powerful. Since it does not "
            "depend on which alternative, it is uniformly most powerful. <bookmark mark='d'/> And its power function is "
            "nondecreasing in theta, so its size over the whole composite null is attained at the boundary: the test is UMP "
            "for the one-sided problem."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def twosided(self):
        d = load("umpu")
        dn = load("np")
        ps = np.asarray(d["ps"])
        A = axes([0, 1], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=r"$p$", ylabel=r"power",
                 xticks=[0, 0.3, 0.5, 0.75, 1], yticks=[0, 0.05, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        up = polyline(ax, dn["ps"], dn["power"], H1C, 4)
        from explainer.stats.kit import testing as TK

        lo = TK.ump_binomial(20, 0.7)["phi"][::-1]
        low = polyline(ax, ps, TK.power(lo, 20, ps), S.PRIOR, 4)
        a = DashedLine(ax.c2p(0, 0.05), ax.c2p(1, 0.05), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"$H_0$: \ $p = 0.3$ \ vs \ $p \ne 0.3$", font_size=22),
            label(r"teal: \ UMP against $p > 0.3$ \ (reject large $x$)", font_size=22, color=H1C),
            label(r"purple: \ UMP against $p < 0.3$ \ (reject small $x$)", font_size=22, color=S.PRIOR),
            label(r"each fails on the other side: \ no UMP", font_size=22, color=REJC),
            label(r"chapter 3: \ restrict to unbiased tests", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two-sided problems are different. Test p equal to point three against p different from "
            "it. <bookmark mark='b'/> Against larger p, the most powerful test rejects large counts: the teal power curve. "
            "<bookmark mark='c'/> Against smaller p, it rejects small counts: purple. <bookmark mark='d'/> A uniformly most "
            "powerful two-sided test would have to be both at once, and each of these has power below alpha on the side it "
            "ignores. So no UMP test exists. <bookmark mark='e'/> The way out, in chapter three, is to demand that the test "
            "be unbiased, never less likely to reject under an alternative than under the null."
        ) as vo:
            self.play(FadeIn(A), Create(a), FadeIn(exact_tag(r"exact power functions")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(up), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(low), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def cauchy(self):
        rows = [
            cmath(r"\text{one Cauchy } x", r":", r"\text{no UMP test of } \theta = 0 \text{ vs } \theta > 0", font_size=32),
            cmath(r"\text{locally most powerful}", r":", r"\text{reject when the score } \tfrac{2x}{1 + x^2} > c", font_size=32),
            cmath(r"\text{the score}", r":", r"\text{largest at } x = 1, \ \to 0 \text{ as } x \to \infty", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\text{reject on a bounded interval: \ accept } x = 1000", font_size=32),
        ]
        rows[3][-1].set_color(REJC)
        whys = [why(r"the ratio is not monotone"), why(r"maximize the power's slope at 0"), why(r"heavy tails"), why(r"optimal, \ and absurd")]
        with self.voiceover(
            "<bookmark mark='a'/> The Cauchy family shows what happens without monotonicity. With one observation there is "
            "no uniformly most powerful test of theta equal to zero against positive theta. <bookmark mark='b'/> The "
            "locally most powerful test, which maximizes the slope of the power at zero, rejects when the score, two x over "
            "one plus x squared, is large. <bookmark mark='c'/> But the score peaks at x equal to one and falls to zero for "
            "large x. <bookmark mark='d'/> So the test rejects on a bounded interval and accepts an observation of a "
            "thousand. Optimality in a narrow sense can produce absurd procedures; for location families with heavy tails, "
            "chapter four's invariance and Part forty-seven's asymptotics give better guidance."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
