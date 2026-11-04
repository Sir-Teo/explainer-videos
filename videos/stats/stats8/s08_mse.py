from __future__ import annotations

import numpy as np

from videos.stats.stats8.common import *  # noqa: F403


class MSE(VoiceoverScene):
    def construct(self):
        self.card()
        self.darts()
        self.decompose()
        self.divisor()
        self.shrinkp()
        self.lesson()
        self.bound()

    def card(self):
        card = chapter_card(7, r"Bias, variance, MSE", r"What makes an estimator good?", part=PART)
        with self.voiceover("Chapter seven. Bias, variance, and mean squared error."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def darts(self):
        g = np.random.Generator(np.random.PCG64(87))
        specs = [(r"unbiased, \ precise", (0, 0), 0.25, S.LIK), (r"unbiased, \ imprecise", (0, 0), 0.75, S.POST),
                 (r"biased, \ precise", (0.7, 0.5), 0.22, S.EST), (r"biased, \ imprecise", (0.6, -0.5), 0.7, S.RESID)]
        boards = VGroup()
        for k, (nm, off, sd, c) in enumerate(specs):
            cx = -4.8 + 3.2 * k
            rings = VGroup(*[Circle(radius=r, color=GREY_C, stroke_width=1.5).move_to([cx, 0.3, 0]) for r in (0.4, 0.8, 1.2)])
            bull = Dot([cx, 0.3, 0], radius=0.06, color=EXACT)
            pts = g.normal(0, sd, (14, 2)) + np.array(off)
            darts = VGroup(*[Dot([cx + a, 0.3 + b, 0], radius=0.05, color=c) for a, b in np.clip(pts, -1.3, 1.3)])
            t = label(nm, font_size=22, color=c).move_to([cx, -1.4, 0])
            boards.add(VGroup(rings, bull, darts, t))
        head = label(r"each dart: \ the estimate from one sample; \ the bullseye: \ the truth", font_size=26).to_edge(UP, buff=0.6)
        with self.voiceover(
            "There are many ways to estimate a quantity from a sample. How do we judge them? <bookmark mark='a'/> "
            "Think of each sample's estimate as a dart, and the truth as the bullseye. <bookmark mark='b'/> A good "
            "estimator lands close every time: centred, and tight. <bookmark mark='c'/> One can be centred but "
            "scattered: unbiased, with high variance. <bookmark mark='d'/> Another can be tight but off-centre: "
            "precise, but biased. <bookmark mark='e'/> And the worst is both."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), *[FadeIn(b[:2]) for b in boards])
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(LaggedStart(*[FadeIn(dt, scale=0.5) for dt in boards[k][2]], lag_ratio=0.05), FadeIn(boards[k][3]))
        self.clear_scene()

    def decompose(self):
        rows = [
            cmath(r"\mathrm{MSE}(\hat\theta)", r"=", r"E(\hat\theta - \theta)^2", font_size=34),
            cmath(r"\mathrm{MSE}(\hat\theta)", r"=", r"E\big(\hat\theta - E\hat\theta + E\hat\theta - \theta\big)^2", font_size=32),
            cmath(r"\mathrm{MSE}(\hat\theta)", r"=", r"\underbrace{\mathrm{Var}(\hat\theta)}_{\text{spread}} + \underbrace{(E\hat\theta - \theta)^2}_{\text{bias}^2}",
                  font_size=34),
        ]
        rows[2][2].set_color(S.ACCENT)
        whys = [why(r"the average squared miss"), why(r"add and subtract the estimator's own mean"),
                why(r"the cross term has mean zero: \ Part 1's loss decomposition")]
        with self.voiceover(
            "One number combines the two failures. <bookmark mark='a'/> The mean squared error is the average squared "
            "distance from the truth. <bookmark mark='b'/> Add and subtract the estimator's own average. "
            "<bookmark mark='c'/> The cross term averages to zero, and the mean squared error splits into the variance, "
            "the spread of the darts, plus the squared bias, the distance from their centre to the bullseye. A little "
            "bias can be worth it, if it buys a big reduction in variance."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=1.0, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def divisor(self):
        d = load("mse")
        cs = np.asarray(d["cs"])
        A = axes([2.5, 9], [0, 0.8], x_length=7.2, y_length=4.4, xlabel=r"divisor $c$ in $\tfrac1c \sum (x_i - \bar x)^2$, \ $n = 5$",
                 ylabel=r"$\div \sigma^4$", xticks=[3, 4, 5, 6, 7, 8, 9], yticks=[0, 0.2, 0.4, 0.6, 0.8], center=[-2.0, -0.4, 0])
        ax = A.ax
        b2 = curve(ax, cs, np.asarray(d["bias2"]), S.RESID, 2.5)
        vr = curve(ax, cs, np.asarray(d["var"]), SIM, 2.5)
        ms = curve(ax, cs, np.asarray(d["mse"]), EXACT, 4)
        leg = legend([(S.RESID, r"bias$^2$"), (SIM, r"variance"), (EXACT, r"MSE")], font_size=24).move_to([4.6, 2.0, 0])
        marks = VGroup()
        for c, lab, col in ((4, r"n - 1", SIM), (5, r"n", GREY_A), (6, r"n + 1", S.ACCENT)):
            v = d["marks"][str(c)]["mse"]
            marks.add(VGroup(Dot(ax.c2p(c, v), radius=0.08, color=col),
                             MathTex(rf"{lab}:\ {v:.3f}", font_size=22, color=col).next_to(ax.c2p(c, v), UP, buff=0.12)))
        rows = fit_rows(VGroup(
            MathTex(r"\mathrm{MSE}(c) = \Big(\frac{n - 1}{c} - 1\Big)^2 + \frac{2(n - 1)}{c^2}", font_size=26),
            label(r"minimized at $c = n + 1$, \ not $n - 1$", font_size=24, color=S.ACCENT),
            MathTex(rf"\text{{simulated: }} {d['sim']['4']:.3f},\ {d['sim']['5']:.3f},\ {d['sim']['6']:.3f}", font_size=24, color=GREY_A),
            label(r"unbiased is not the same as best", font_size=26, color=S.ACCENT),
        ), 5.0, 0.3, [4.5, -0.6, 0])
        tag = note(r"normal data; \ exact, \ and 200,000 simulated samples").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here's a surprise about the n minus one. <bookmark mark='a'/> Divide the sum of squares by any constant c. "
            "For normal data we know its distribution exactly, so we can compute its bias and variance. "
            "<bookmark mark='b'/> Larger c means more bias, downward; <bookmark mark='c'/> but less variance. "
            "<bookmark mark='d'/> Their sum, the mean squared error, is smallest not at n minus one, which removes the "
            "bias, but at n plus one. For five observations: point five for n minus one, point three six for n, point "
            "three three for n plus one, and the simulation agrees. <bookmark mark='e'/> Unbiased is not the same as "
            "best. We use n minus one because unbiasedness is convenient and because it's what the t distribution "
            "needs, not because it's the most accurate."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(b2), FadeIn(leg[0]))
            vo.wait_until("c")
            self.play(Create(vr), FadeIn(leg[1]))
            vo.wait_until("d")
            self.play(Create(ms), FadeIn(leg[2]), FadeIn(marks), FadeIn(rows[1:3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"the bias--variance trade-off", font_size=30, color=S.ACCENT),
            label(r"shrinkage: \ pull an estimate toward a fixed point, \ accept bias, \ cut variance", font_size=26),
            label(r"James \& Stein (1961): \ for 3 or more means, \ shrinkage beats the sample means in expected total MSE (Part 25)",
                  font_size=24, color=GREY_A),
            label(r"ridge and lasso (Part 32), \ smoothing (Part 29), \ every prior (Part 15)", font_size=24, color=GREY_A),
            label(r"but MSE is not everything: \ intervals need the bias to be understood, \ not just small", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.38, [0, 0.2, 0])
        with self.voiceover(
            "This is the first glimpse of an idea that runs through modern statistics. <bookmark mark='a'/> The "
            "bias–variance trade-off. <bookmark mark='b'/> Pull an estimate toward a fixed point, accept some bias, "
            "and cut the variance. <bookmark mark='c'/> In 1961 Willard James and Charles Stein showed that for three "
            "or more means estimated at once, shrinking them toward each other beats the sample means in expected total "
            "squared error, whatever the true means are: Part 25. <bookmark mark='d'/> Ridge regression, the lasso, smoothing and every Bayesian "
            "prior are versions of the same bargain. <bookmark mark='e'/> But mean squared error isn't everything: an "
            "interval needs its bias to be understood, not just small."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def shrinkp(self):
        d = load("extras")["shrink"]
        ps = np.asarray(d["ps"])
        A = axes([0, 1], [0, 0.0135], x_length=7.2, y_length=4.2, xlabel=r"true $p$, \ $n = 20$", ylabel=r"MSE",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.005, 0.01], center=[-2.0, -0.4, 0])
        ax = A.ax
        ml = curve(ax, ps, np.asarray(d["ml"]), SIM, 3)
        ac = curve(ax, ps, np.asarray(d["ac"]), S.POST, 3)
        cr = VGroup(*[DashedLine(ax.c2p(c, 0), ax.c2p(c, 0.0135), color=GREY_C, stroke_width=1.5) for c in d["cross"]])
        leg = legend([(SIM, r"$x/n$: \ unbiased"), (S.POST, r"$(x + 2)/(n + 4)$: \ shrunk toward $\tfrac12$")], font_size=22).move_to([4.4, 2.0, 0])
        rows = fit_rows(VGroup(
            label(rf"shrinkage wins for ${d['cross'][0]:.2f} < p < {d['cross'][1]:.2f}$", font_size=24, color=S.POST),
            label(r"and loses near 0 and 1, \ where its bias is largest", font_size=24, color=GREY_A),
            label(r"no estimator is best for every $p$: \ Part 45's decision theory", font_size=22, color=S.ACCENT),
            label(r"Agresti \& Coull (1998) use it for intervals: \ Part 11", font_size=22, color=GREY_A),
        ), 5.0, 0.3, [4.4, -0.4, 0])
        tag = note(r"exact: \ sums over the binomial").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Shrinkage in miniature. <bookmark mark='a'/> Estimate a proportion from twenty trials. The obvious estimate, "
            "successes over trials, is unbiased, and its mean squared error is p times one minus p over twenty, the blue "
            "hump. <bookmark mark='b'/> Now add two imaginary successes and two failures: x plus two over n plus four. "
            "That pulls every estimate toward a half, so it's biased. But its mean squared error, in orange, is lower "
            "for every p between about point two and point eight. <bookmark mark='c'/> Near zero and one, where the "
            "pull toward a half costs the most, it loses. No estimator is best everywhere, which is the starting point "
            "of decision theory in Part 45. Alan Agresti and Brent Coull built an interval on this idea, which "
            "Part 11 tests."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ml), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(ac), FadeIn(leg[1]), Create(cr), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1:]))
        self.clear_scene()

    def bound(self):
        rows = [
            cmath(r"\mathrm{Var}(\hat\theta)", r"\ge", r"\frac{1}{n\,I(\theta)}", r"\quad \text{for every unbiased } \hat\theta", font_size=34),
            cmath(r"N(\mu, \sigma^2):\ I(\mu) = \frac{1}{\sigma^2}", r"\ \Rightarrow\ ", r"\mathrm{Var}(\bar x) = \frac{\sigma^2}{n} \text{ attains it}",
                  font_size=30),
            cmath(r"\text{the median}:\ \frac{\pi}{2}\cdot\frac{\sigma^2}{n}", r"\ >\ ", r"\frac{\sigma^2}{n}", font_size=30),
        ]
        rows[0][2].set_color(EXACT)
        whys = [why(r"the Cram\'er--Rao bound (1945--46): \ $I$, \ Fisher information"),
                why(r"no unbiased estimator of a normal mean beats $\bar x$"), why(r"chapter 1's efficiency, \ explained")]
        with self.voiceover(
            "Is there a limit to how good an unbiased estimator can be? <bookmark mark='a'/> Yes. The Cramér–Rao bound, "
            "found by Harald Cramér and C. R. Rao in the mid-1940s, says no unbiased estimator can have variance below "
            "one over n times the Fisher information, a measure of how sharply the data's distribution depends on the "
            "parameter. <bookmark mark='b'/> For the mean of a normal, the information is one over sigma squared, and "
            "the sample mean's variance, sigma squared over n, sits exactly on the bound: nothing unbiased beats it. "
            "<bookmark mark='c'/> The median's variance is pi over two times larger, which is chapter one's efficiency "
            "of two over pi. Part 9 derives the bound and builds estimators that reach it."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=1.0, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
