from __future__ import annotations

import numpy as np

from videos.stats.stats29.common import *  # noqa: F403


class KDE(VoiceoverScene):
    def construct(self):
        self.card()
        self.bumps()
        self.bias()
        self.variance()
        self.amise()
        self.picture()
        self.mise_curves()
        self.epanechnikov()
        self.efficiency()

    def card(self):
        card = chapter_card(2, r"Kernel density estimates", r"Smooth bumps, \ and the rate $n^{-4/5}$", lit=(1956,), part=PART)
        with self.voiceover("Chapter two. Kernel density estimates."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def bumps(self):
        d = load("faithful")
        x = np.asarray(d["x"])
        A = axes([1, 6], [0, 0.9], x_length=7.4, y_length=4.4, xlabel=r"eruption length (minutes)", ylabel=r"density",
                 xticks=[2, 3, 4, 5], yticks=[0, 0.4, 0.8], center=[-2.0, 0.3, 0])
        ax = A.ax
        g = np.random.default_rng(29)
        sub = np.sort(g.choice(x, 30, replace=False))
        ks = KernelSum(ax, sub, 0.25, grid=np.linspace(1, 6, 300), bump_color=GREY_B, total_color=KDEC, rug_color=WHITE)
        for b in ks.bumps:
            b.stretch(10.0, 1, about_point=ax.c2p(0, 0))
        full = clip_curve(ax, np.asarray(d["grid"]), np.asarray(d["kde"]["h0.25"]), KDEC, 4, ymin=0, ymax=0.9)
        rows = fit_rows(VGroup(
            label(r"$\hat f_h(x) = \frac{1}{nh}\sum_i K\bigl(\frac{x - x_i}{h}\bigr)$", font_size=24),
            label(r"30 eruptions: \ one bump on each \ (drawn 10 times taller)", font_size=22, color=GREY_B),
            label(r"blue: \ their average", font_size=22, color=KDEC),
            label(r"all 272, \ $h = 0.25$", font_size=22, color=KDEC),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The kernel estimate, from Murray Rosenblatt in 1956 and Emanuel Parzen in 1962: at each "
            "point, average kernel bumps centred on the observations, each of width h. <bookmark mark='b'/> Here are thirty "
            "of the eruptions, each with its normal bump, drawn taller so they can be seen. <bookmark mark='c'/> Their "
            "average is a smooth curve, with no bin edges and no origin to choose. <bookmark mark='d'/> With all two hundred "
            "and seventy-two eruptions, two clear humps."
        ) as vo:
            self.add(faithful_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(ks.rug), LaggedStart(*[Create(b) for b in ks.bumps], lag_ratio=0.05), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(ks.total), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeOut(ks.bumps), FadeOut(ks.rug), ReplacementTransform(ks.total, full), FadeIn(rug(ax, x)), FadeIn(rows[3]))
        self.clear_scene()

    def bias(self):
        rows = [
            cmath(r"E\,\hat f_h(x)", r"=", r"\textstyle\int \tfrac1h K\bigl(\tfrac{x - y}{h}\bigr) f(y)\, dy = \int K(u) f(x - hu)\, du", font_size=28),
            cmath(r"f(x - hu)", r"=", r"f(x) - hu f'(x) + \tfrac12 h^2 u^2 f''(x) + \dots", font_size=30),
            cmath(r"\text{bias}(x)", r"=", r"\tfrac12 h^2 \mu_2(K) f''(x) + o(h^2)", font_size=32),
            cmath(r"\textstyle\int \text{bias}^2", r"\approx", r"\tfrac14 h^4 \mu_2^2 R(f'')", font_size=32),
        ]
        rows[2][2].set_color(BIASC)
        whys = [why(r"the estimate's mean: \ $f$ blurred by the kernel"), why(r"Taylor in $h$"),
                why(r"$\int uK = 0$: \ the slope term vanishes"), why(r"$\mu_2 = \int u^2 K$, \ $R(g) = \int g^2$")]
        with self.voiceover(
            "<bookmark mark='a'/> The estimate's expectation is the true density blurred by the kernel, after substituting u "
            "for x minus y over h. <bookmark mark='b'/> Expand f around x. <bookmark mark='c'/> The constant term returns f; "
            "the slope term vanishes, because a symmetric kernel has mean zero, unlike the histogram's off-centre bins; what's "
            "left is half h squared times the kernel's variance times the curvature f double prime. Bias is negative at peaks "
            "and positive in valleys: smoothing flattens. <bookmark mark='d'/> Integrated and squared: a quarter h to the "
            "fourth mu two squared R of f double prime."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def variance(self):
        rows = [
            cmath(r"\mathrm{Var}\,\hat f_h(x)", r"=", r"\tfrac1n \mathrm{Var}\bigl(\tfrac1h K(\tfrac{x - X}{h})\bigr)", font_size=30),
            cmath(r"", r"\approx", r"\tfrac{1}{nh^2} \textstyle\int K^2\bigl(\tfrac{x - y}{h}\bigr) f(y)\, dy \approx \tfrac{f(x) R(K)}{nh}", font_size=28),
            cmath(r"\textstyle\int \mathrm{Var}", r"\approx", r"\dfrac{R(K)}{nh}", font_size=32),
            cmath(r"nh", r":", r"\text{the effective number of points in a window}", font_size=30),
        ]
        rows[2][2].set_color(VARC)
        whys = [why(r"an average of $n$ independent bumps"), why(r"the mean term is of smaller order"),
                why(r"$\int f = 1$"), why(r"the histogram's $1/(nh)$ again")]
        with self.voiceover(
            "<bookmark mark='a'/> The variance: the estimate is an average of n independent bump heights. "
            "<bookmark mark='b'/> Each bump's second moment, after the same substitution, is about f of x times R of K over "
            "h; the squared mean is of smaller order. <bookmark mark='c'/> So the integrated variance is R of K over n h. "
            "<bookmark mark='d'/> n h is roughly the number of observations within a bandwidth of x: the effective sample "
            "size of a local average, as for the histogram."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def amise(self):
        rows = [
            cmath(r"\text{AMISE}(h)", r"=", r"\dfrac{R(K)}{nh} + \tfrac14 h^4 \mu_2^2 R(f'')", font_size=32),
            cmath(r"h^*", r"=", r"\Bigl(\dfrac{R(K)}{\mu_2^2 R(f'') n}\Bigr)^{1/5}", font_size=32),
            cmath(r"\text{AMISE}(h^*)", r"=", r"\tfrac54 \bigl(\mu_2 R(K)^2\bigr)^{2/5} R(f'')^{1/5}\, n^{-4/5}", font_size=28),
            cmath(r"\text{histogram}", r":", r"n^{-2/3}", font_size=32),
        ]
        rows[2][2].set_color(KDEC)
        whys = [why(r"variance $\propto 1/(nh)$, \ squared bias $\propto h^4$"), why(r"the fifth-root bandwidth"),
                why(r"a product: \ the kernel's part times the density's"), why(r"$n^{-4/5}$ is faster")]
        with self.voiceover(
            "<bookmark mark='a'/> Add them. Variance falls like one over n h; squared bias grows like h to the fourth, not "
            "the histogram's h squared. <bookmark mark='b'/> Setting the derivative to zero gives the best bandwidth, which "
            "shrinks like n to the minus one fifth. <bookmark mark='c'/> The minimal error is a constant depending on the "
            "kernel, times one depending on the density's roughness, times n to the minus four fifths. "
            "<bookmark mark='d'/> Against the histogram's minus two thirds, that is a real gain, and Part 50 proves that no "
            "estimator can beat n to the minus four fifths for densities with two derivatives."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("kdemise")
        g = np.asarray(d["grid"])
        f, b, s = np.asarray(d["f"]), np.asarray(d["bias"]), np.asarray(d["sd"])
        A = axes([0.5, 6], [-0.25, 0.8], x_length=7.4, y_length=4.4, xlabel=r"$x$", ylabel=r"density",
                 xticks=[1, 2, 3, 4, 5, 6], yticks=[-0.2, 0, 0.2, 0.4, 0.6], center=[-2.0, 0.3, 0])
        ax = A.ax
        truth = curve(ax, g, f, TRUE, 3)
        mean = curve(ax, g, f + b, KDEC, 3)
        bnd = band(ax, g, f + b - 2 * s, f + b + 2 * s, KDEC, 0.25)
        bias = curve(ax, g, 5 * b, BIASC, 3)
        zero = DashedLine(ax.c2p(0.5, 0), ax.c2p(6, 0), color=GREY_D, stroke_width=1)
        rows = fit_rows(VGroup(
            label(rf"$n = 1{{,}}000$, \ $h^* = {d['best_1000']['amise_h']:.3f}$", font_size=22),
            label(r"gold: \ the truth", font_size=22, color=TRUE),
            label(r"blue: \ $E\hat f$, \ $\pm 2$ SD", font_size=22, color=KDEC),
            label(r"red: \ the bias $\frac12 h^2 f''$, \ times 5", font_size=22, color=BIASC),
            label(r"peaks cut, \ valleys filled", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Pictured for a thousand points at the optimal bandwidth. <bookmark mark='b'/> Gold is the "
            "truth. <bookmark mark='c'/> Blue is the estimate's average, with a band of two standard deviations: widest at "
            "the peaks, where there's most data and so most absolute noise. <bookmark mark='d'/> Red is the bias, magnified five times: negative "
            "at the two peaks, positive in the valley and the shoulders. <bookmark mark='e'/> The optimal bandwidth "
            "deliberately leaves in bias comparable to the noise, a point chapter eleven will make costly."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(bnd), Create(mean), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(bias), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def mise_curves(self):
        d = load("kdemise")
        hs = np.log10(np.asarray(d["hs"]))
        A = axes([-1.7, 0.2], [-4.0, -0.5], x_length=7.4, y_length=4.4, xlabel=r"bandwidth $h$ \ (log scale)",
                 ylabel=r"MISE \ (log scale)", xticks=[-1.5, -1, -0.5, 0], yticks=[-4, -3, -2, -1],
                 xfmt=lambda v: f"{10 ** v:.2g}", yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.0, 0.3, 0])
        ax = A.ax
        n = 1000

        def pl(key, col, sw=3):
            v = np.log10(np.asarray(d[key]))
            k = (v > -4.0) & (v < -0.5)
            return polyline(ax, hs[k], v[k], col, sw)

        exact = pl(f"mise_{n}", KDEC, 4)
        am = DashedVMobject(pl(f"amise_{n}", WHITE, 2), num_dashes=50)
        iv = pl(f"ivar_{n}", VARC, 2.5)
        ib = pl(f"ibias2_{n}", BIASC, 2.5)
        others = VGroup(pl("mise_100", GREY_B, 2), pl("mise_10000", GREY_B, 2))
        rows = fit_rows(VGroup(
            label(r"$n = 1{,}000$: \ the exact MISE \ (Marron \& Wand 1992)", font_size=22, color=KDEC),
            label(r"teal: \ integrated variance, \ slope $-1$", font_size=22, color=VARC),
            label(r"red: \ integrated squared bias, \ slope $4$", font_size=22, color=BIASC),
            label(r"white dashed: \ AMISE, \ close near the optimum", font_size=22),
            label(r"grey: \ $n = 100$ and $10{,}000$", font_size=22, color=GREY_B),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For normal mixtures and a normal kernel the MISE is exactly computable, Steve Marron and "
            "Matt Wand's formula. Here it is for a thousand points. <bookmark mark='b'/> On log scales the variance term is a "
            "line of slope minus one, <bookmark mark='c'/> the squared bias a line of slope four. <bookmark mark='d'/> Their "
            "sum, the asymptotic approximation, hugs the exact curve near the optimum and departs for large h, where the "
            "Taylor expansion fails. <bookmark mark='e'/> With a hundred or ten thousand points the whole curve shifts: the "
            "optimum moves as n to the minus one fifth, and the minimal error as n to the minus four fifths."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(exact), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(iv), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ib), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(am), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Create(others), FadeIn(rows[4]))
        self.clear_scene()

    def epanechnikov(self):
        rows = [
            cmath(r"\min_K", r"\ ", r"\mu_2(K)^{1/2} R(K) \ \text{ s.t. } K \ge 0, \ \textstyle\int K = 1, \ \int u K = 0", font_size=28),
            cmath(r"\text{fix } \mu_2", r":", r"\min \textstyle\int K^2 + \alpha(\int K - 1) + \beta(\int u^2 K - \mu_2)", font_size=28),
            cmath(r"\text{pointwise}", r":", r"2K(u) + \alpha + \beta u^2 = 0 \ \text{ where } K > 0", font_size=28),
            cmath(r"K(u)", r"=", r"\tfrac34 (1 - u^2)_+", font_size=34),
        ]
        rows[3][2].set_color(KDEC)
        whys = [why(r"the kernel's factor in the minimal AMISE"), why(r"Lagrange multipliers"),
                why(r"the calculus of variations: \ a parabola"), why(r"Epanechnikov (1969)")]
        with self.voiceover(
            "<bookmark mark='a'/> Which kernel is best? The minimal error depends on the kernel only through root mu two "
            "times R of K, invariant to rescaling the kernel. <bookmark mark='b'/> Fix mu two and minimize the integral of "
            "K squared subject to K being a density, with Lagrange multipliers. <bookmark mark='c'/> Differentiating "
            "pointwise in K, the calculus of variations, says that wherever K is positive it is a downward parabola in u. "
            "<bookmark mark='d'/> Normalized and truncated at zero: three quarters of one minus u squared, Vassiliy "
            "Epanechnikov's kernel of 1969."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def efficiency(self):
        d = load("kdemise")["efficiency"]
        hdr = [r"\textbf{kernel}", r"\textbf{$K(u)$}", r"\textbf{efficiency}", r"\textbf{data needed for the same error}"]
        forms = {"epanechnikov": r"$\frac34(1 - u^2)$", "biweight": r"$\frac{15}{16}(1 - u^2)^2$", "triangular": r"$1 - |u|$",
                 "gaussian": r"$\phi(u)$", "uniform": r"$\frac12$"}
        body = [[k, forms[k], f"{v:.3f}", f"{100 / v:.1f}\\%"] for k, v in d.items()]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.3, colors=[GREY_A, KDEC] + [None] * 4)
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"efficiency: \ $\bigl[C(K_{\mathrm{Epan}})/C(K)\bigr]^{5/4}$, \ the sample-size ratio", font_size=22),
            label(r"even the box loses only 7\%: \ the kernel hardly matters; \ the bandwidth does", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How much does it matter? Express each kernel's efficiency as the ratio of sample sizes "
            "needed for the same error. <bookmark mark='b'/> The biweight and triangle lose less than one and a half percent. "
            "The normal kernel loses five. Even a flat box, the crudest kernel there is, needs only seven and a half percent "
            "more data. The kernel hardly matters; the bandwidth matters enormously, and the next chapter chooses it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[2:]], lag_ratio=0.3), FadeIn(foot[1]), run_time=3.0)
        self.wait(1.0)
        self.clear_scene()
