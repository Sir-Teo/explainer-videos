from __future__ import annotations

import numpy as np

from videos.stats.stats6.common import *  # noqa: F403


class Inequalities(VoiceoverScene):
    def construct(self):
        self.card()
        self.markov_picture()
        self.markov_world()
        self.chebyshev()
        self.tight()
        self.jensen()

    def card(self):
        card = chapter_card(1, r"Markov, Chebyshev, Jensen", r"What does a mean alone guarantee?", lit=(1867,), part=PART)
        with self.voiceover("Chapter one. Three inequalities."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def markov_picture(self):
        A = axes([0, 6], [0, 6], x_length=5.4, y_length=4.6, xlabel=r"$x$", xticks=[0, 2, 4, 6], yticks=[0, 2, 4, 6],
                 center=[-3.6, -0.5, 0])
        ax = A.ax
        a = 2.5
        line = Line(ax.c2p(0, 0), ax.c2p(6, 6), color=SIM, stroke_width=3.5)
        step = VGroup(Line(ax.c2p(0, 0), ax.c2p(a, 0), color=BOUND, stroke_width=4),
                      Line(ax.c2p(a, a), ax.c2p(6, a), color=BOUND, stroke_width=4),
                      DashedLine(ax.c2p(a, 0), ax.c2p(a, a), color=BOUND, stroke_width=1.5))
        la = MathTex(r"x", font_size=28, color=SIM).next_to(ax.c2p(5.6, 5.6), LEFT, buff=0.15)
        lb = MathTex(r"a\,\mathbf 1\{x \ge a\}", font_size=28, color=BOUND).next_to(ax.c2p(5.0, a), DOWN, buff=0.15)
        lt = MathTex(r"a", font_size=26, color=GREY_B).next_to(ax.c2p(a, 0), DOWN, buff=0.15)
        rows = [
            cmath(r"a\,\mathbf 1\{X \ge a\}", r"\le", r"X", r"\qquad (X \ge 0)", font_size=34),
            cmath(r"a\,P(X \ge a)", r"\le", r"E X", font_size=34),
            cmath(r"P(X \ge a)", r"\le", r"\frac{E X}{a}", font_size=38),
        ]
        rows[2][2].set_color(BOUND)
        whys = [why(r"the red step lies under the blue line"), why(r"take expectations: \ $E\,\mathbf 1_A = P(A)$"),
                why(r"Markov's inequality")]
        with self.voiceover(
            "Suppose all you know about a quantity is that it can't be negative, and its mean. How much can it "
            "stray? <bookmark mark='a'/> Draw the line y equals x, and under it a step: zero until some level a, "
            "then a. <bookmark mark='b'/> The step never rises above the line, for any non-negative x. "
            "<bookmark mark='c'/> So a times the indicator that X is at least a is at most X itself. "
            "<bookmark mark='d'/> Take expectations of both sides; the expectation of an indicator is a "
            "probability. <bookmark mark='e'/> So the chance that X reaches a is at most its mean over a. That's "
            "Markov's inequality, named for Andrey Markov, who published it in the 1880s; his teacher Chebyshev had "
            "used the idea first. A quantity can't often be ten times its mean: at most one time in ten."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(la))
            vo.wait_until("b")
            self.play(Create(step), FadeIn(lb), FadeIn(lt))
            step_ = ladder(self, rows, whys, keep=3, top=2.4, x=2.6, buff=0.8, edge=6.9)
            vo.wait_until("c")
            step_(0, transform=False)
            vo.wait_until("d")
            step_(1, transform=False)
            vo.wait_until("e")
            step_(2, transform=False)
        self.clear_scene()

    def markov_world(self):
        d = load("markov")
        a, frac = np.asarray(d["a"]), np.asarray(d["frac"])
        A = axes([0.5, 10.5], [0, 1.05], x_length=7.0, y_length=4.4, xlabel=r"$a$, \ in multiples of the mean income",
                 ylabel=r"share of adults earning at least $a \times$ mean", xticks=[1, 2, 4, 6, 8, 10], yticks=[0, 0.5, 1],
                 center=[-2.4, -0.4, 0])
        ax = A.ax
        bnd = curve(ax, np.linspace(1, 10.5, 100), 1 / np.linspace(1, 10.5, 100), BOUND, 3)
        dots = VGroup(*[Dot(ax.c2p(k, f), radius=0.07, color=WORLD) for k, f in zip(a, frac)])
        rows = VGroup(
            MathTex(rf"\text{{mean income: }} {d['mu'] / 1000:.1f}\text{{k}}", font_size=28, color=GREY_A),
            MathTex(rf"a = 2:\ \ {100 * frac[1]:.1f}\%\ \le\ 50\%", font_size=28),
            MathTex(rf"a = 3:\ \ {100 * frac[2]:.1f}\%\ \le\ 33\%", font_size=28),
            MathTex(rf"a = 10:\ \ {100 * frac[9]:.2f}\%\ \le\ 10\%", font_size=28),
            label(r"true, \ and far from tight: \ the bound uses only the mean", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        for r in rows:
            if r.width > 4.8:
                r.width = 4.8
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.4, 0.8, 0])
        leg = legend([(BOUND, r"Markov: \ $1/a$"), (WORLD, r"the World's incomes")], font_size=22).move_to([4.2, -2.0, 0])
        tag = simulated_tag()
        with self.voiceover(
            "Test it on the World's incomes. <bookmark mark='a'/> In red, Markov's bound, one over a. "
            "<bookmark mark='b'/> In green, the share of adults earning at least a times the mean. Twice the mean: "
            f"{100 * frac[1]:.1f} percent, against a bound of fifty. Three times: {100 * frac[2]:.1f} percent, against a "
            "third. <bookmark mark='c'/> The bound always holds, and it's always far from the truth, because it "
            "uses nothing but the mean. That's the price of a guarantee that needs no assumptions. We'll sharpen it "
            "by feeding it more."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(bnd), FadeIn(leg[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in dots], lag_ratio=0.1), FadeIn(leg[1]), FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def chebyshev(self):
        d = load("markov")
        ks = np.asarray(d["ks"])
        rows = [
            cmath(r"P(|X - \mu| \ge k\sigma)", r"=", r"P\big((X - \mu)^2 \ge k^2\sigma^2\big)", font_size=32),
            cmath(r"P(|X - \mu| \ge k\sigma)", r"\le", r"\frac{E(X - \mu)^2}{k^2\sigma^2}", r"=", r"\frac{1}{k^2}", font_size=34),
        ]
        rows[1][4].set_color(BOUND)
        whys = [why(r"square both sides"), why(r"Markov, \ applied to $(X - \mu)^2 \ge 0$")]
        A = axes([0.8, 4.2], [0, 1.05], x_length=5.6, y_length=3.0, xlabel=r"$k$ (standard deviations)", xticks=[1, 2, 3, 4],
                 yticks=[0, 0.25, 0.5, 1], center=[-2.6, -2.1, 0])
        ax = A.ax
        kk = np.linspace(1, 4.2, 100)
        bnd = curve(ax, kk, 1 / kk ** 2, BOUND, 3)
        hd = VGroup(*[Dot(ax.c2p(k, v), radius=0.06, color=S.EST) for k, v in zip(ks, d["cheb_height"])])
        yd = VGroup(*[Dot(ax.c2p(k, v), radius=0.06, color=WORLD) for k, v in zip(ks, d["cheb_income"])])
        leg = legend([(BOUND, r"Chebyshev: \ $1/k^2$"), (S.EST, r"the World's heights"), (WORLD, r"the World's incomes")],
                     font_size=22).move_to([4.4, -1.6, 0])
        hc = history_card(1867, r"Bienaym\'e (1853), \ Chebyshev (1867)", r"the first general bound on how far a variable "
                          r"strays from its mean, \ with nothing assumed but a variance", color=S.MUSEUM, width=4.6,
                          font_size=20).move_to([4.4, -0.15, 0])
        with self.voiceover(
            "Feed it the variance. <bookmark mark='a'/> The event that X is k standard deviations or more from its "
            "mean is the same as the event that the squared deviation is at least k squared sigma squared. "
            "<bookmark mark='b'/> Apply Markov to the squared deviation, which can't be negative. Its mean is the "
            "variance, so the chance is at most one over k squared. That's Chebyshev's inequality, found by "
            "Irénée-Jules Bienaymé in 1853 and by Pafnuty Chebyshev in 1867. <bookmark mark='c'/> Two standard "
            f"deviations: at most a quarter. The World's heights, which are nearly normal, stray that far "
            f"{100 * d['cheb_height'][2]:.1f} percent of the time; its incomes, {100 * d['cheb_income'][2]:.1f} percent. Both "
            "far below the bound."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.9, x=-2.2, buff=0.7, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            self.play(FadeIn(hc))
            vo.wait_until("c")
            self.play(FadeIn(A), Create(bnd), FadeIn(hd), FadeIn(yd), FadeIn(leg))
        self.clear_scene()

    def tight(self):
        k = 2
        A = axes([-3.5, 3.5], [0, 1.0], x_length=6.0, y_length=3.6, xlabel=r"$x$ \ (in units of $\sigma$ from $\mu$)",
                 xticks=[-2, 0, 2], yticks=[0, 0.5, 1], center=[-2.6, -0.4, 0])
        ax = A.ax
        bars = pmf_bars(ax, [-k, 0, k], [1 / (2 * k * k), 1 - 1 / (k * k), 1 / (2 * k * k)], BOUND, width=0.5)
        labs = VGroup(*[MathTex(t, font_size=24, color=BOUND).next_to(b, UP, buff=0.1) for t, b in
                        zip((r"\tfrac18", r"\tfrac34", r"\tfrac18"), bars)])
        rows = VGroup(
            MathTex(r"X = \mu \pm 2\sigma \text{ with chance } \tfrac18 \text{ each, else } \mu", font_size=28),
            MathTex(r"\mathrm{Var}\, X = 2 \cdot \tfrac18 \cdot (2\sigma)^2 = \sigma^2", font_size=28),
            MathTex(r"P(|X - \mu| \ge 2\sigma) = \tfrac14", r"\ = \ \text{the bound}", font_size=28, color=BOUND),
            label(r"so no better bound can use only $\mu$ and $\sigma$", font_size=24, color=S.ACCENT),
            label(r"a better one needs more: \ normality ($4.6\%$), \ or boundedness (chapter 11)", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.4, 0])
        for r in rows:
            if r.width > 6.2:
                r.width = 6.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.4, 0])  # re-align after clamping
        with self.voiceover(
            "Is Chebyshev's bound simply careless? No: it can't be improved. <bookmark mark='a'/> Here's a variable "
            "that meets it exactly. It equals its mean three quarters of the time, and otherwise jumps two standard "
            "deviations up or down, an eighth of the time each. <bookmark mark='b'/> Its variance is exactly sigma "
            "squared. <bookmark mark='c'/> And it lands two standard deviations away with probability a quarter, "
            "exactly the bound. <bookmark mark='d'/> So no inequality that uses only the mean and the variance can "
            "do better. To do better you must know more: that the variable is normal, which gives four point six "
            "percent, or that it's bounded, which gives the exponential bounds of chapter eleven."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(labs), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def jensen(self):
        d = load("markov")
        A = axes([0, 3.2], [0, 3.2], x_length=5.0, y_length=4.4, xlabel=r"$x$", center=[-3.8, -0.5, 0])
        ax = A.ax
        A.ax.x_axis.set_opacity(0.5)
        f = lambda x: 0.35 * x ** 2 + 0.2  # noqa: E731
        xs = np.linspace(0.05, 3.1, 120)
        cv = curve(ax, xs, f(xs), SIM, 3.5)
        x1, x2, w = 0.6, 2.8, 0.5
        chord = Line(ax.c2p(x1, f(x1)), ax.c2p(x2, f(x2)), color=BOUND, stroke_width=3)
        m = w * x1 + (1 - w) * x2
        p_chord = Dot(ax.c2p(m, w * f(x1) + (1 - w) * f(x2)), radius=0.08, color=BOUND)
        p_curve = Dot(ax.c2p(m, f(m)), radius=0.08, color=SIM)
        lab1 = MathTex(r"E\varphi(X)", font_size=26, color=BOUND).next_to(p_chord, UL, buff=0.08)
        lab2 = MathTex(r"\varphi(EX)", font_size=26, color=SIM).next_to(p_curve, DR, buff=0.08)
        rows = VGroup(
            MathTex(r"\varphi \text{ convex} \ \Rightarrow\ ", r"\varphi(E X) \le E\,\varphi(X)", font_size=32),
            label(r"the chord lies above the curve; \ the mean of $\varphi$ is on the chord", font_size=22, color=GREY_B),
            MathTex(r"\varphi(x) = x^2:\ \ (EX)^2 \le E X^2 \ \Leftrightarrow\ \mathrm{Var}\,X \ge 0", font_size=28),
            MathTex(rf"\varphi = -\log:\ \ E \log Y = {d['elog']:.3f}\ \le\ \log E Y = {d['logE']:.3f}", font_size=28, color=WORLD),
            MathTex(rf"\text{{geometric mean income }} {d['gmean'] / 1000:.1f}\text{{k}}\ <\ \text{{mean }} {d['mu'] / 1000:.1f}\text{{k}}",
                    font_size=26, color=WORLD),
            label(r"and, in Part 22, \ why the Kullback--Leibler divergence is never negative", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.9, 0.4, 0])
        rows[0][1].set_color(S.ACCENT)
        for r in rows:
            if r.width > 7.2:
                r.width = 7.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.9, 0.4, 0])  # re-align after clamping
        tag = simulated_tag()
        with self.voiceover(
            "The third inequality is about curves. <bookmark mark='a'/> A convex function is one whose chords lie "
            "above it. <bookmark mark='b'/> Let X take two values with equal chance. The average of phi of X is the "
            "midpoint of the chord; phi of the average is the curve below it. <bookmark mark='c'/> So for convex phi, "
            "phi of the mean is at most the mean of phi: Johan Jensen's inequality, 1906, and by approximation it "
            "holds for any distribution. <bookmark mark='d'/> With phi equal to x squared it says the variance can't "
            "be negative. <bookmark mark='e'/> With minus the logarithm, applied to the World's incomes: the mean of "
            "the log is below the log of the mean, so the geometric mean income, about forty thousand, is below "
            "the ordinary mean, forty-nine thousand. Jensen will turn up again whenever a logarithm meets an "
            "expectation."
        ) as vo:
            self.play(FadeIn(A), Create(cv), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(chord))
            vo.wait_until("b")
            self.play(FadeIn(p_chord), FadeIn(p_curve), FadeIn(lab1), FadeIn(lab2))
            vo.wait_until("c")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()
