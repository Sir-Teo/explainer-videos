from __future__ import annotations

import numpy as np
from scipy.stats import levy_stable

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import LOSS, MART, P_C, PART, Q_C, load, real_data


class Stable(VoiceoverScene):
    def construct(self):
        s = load("stable")
        e = load("ecf")
        mle = load("stable_mle")
        self.card()
        self.laws()
        self.charfun(e, s)
        self.estimate(s)
        self.fit(mle, s)
        self.aggregate(e)

    def card(self):
        c = chapter_card(14, r"Heavy tails as stable laws", r"What shape survives adding up?", lit=(1963,), part=PART)
        with self.voiceover("Chapter fourteen. Heavy tails, as stable laws."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def laws(self):
        x = np.linspace(-6, 6, 241)
        g = axes([-6, 6], [-4, 0], x_length=7.2, y_length=4.4, xlabel=r"$x$", ylabel=r"density (log scale)",
                 xticks=[-6, -3, 0, 3, 6], yticks=[-4, -3, -2, -1, 0], yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1",
                 font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        alphas = [(2.0, MART), (1.7, P_C), (1.4, Q_C), (1.0, LOSS)]
        curves = VGroup()
        for a, c in alphas:
            y = np.log10(np.maximum(levy_stable.pdf(x, a, 0.0), 1e-4))
            curves.add(curve(ax, x, y, c, stroke_width=3))
        leg = legend([(MART, r"$\alpha = 2$: Gaussian"), (P_C, r"$\alpha = 1.7$"), (Q_C, r"$\alpha = 1.4$"),
                      (LOSS, r"$\alpha = 1$: Cauchy")], font_size=21).to_edge(RIGHT, buff=0.6).shift(UP * 1.8)
        side = VGroup(
            wrapped_label(r"stable: a sum of independent copies has the same shape, rescaled by $n^{1/\alpha}$ "
                          r"(L\'evy, 1925)", 4.6, 22, GREY_A),
            wrapped_label(r"for $\alpha < 2$ the tails fall like $|x|^{-1-\alpha}$ and the variance is infinite", 4.6, 22,
                          GREY_A),
            wrapped_label(r"Mandelbrot (1963): cotton prices, $\alpha \approx 1.7$; Fama (1965): the thirty Dow stocks, "
                          r"$\alpha$ below 2", 4.6, 22, P_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(leg, side).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Part one measured how heavy the tails of returns are. Here is the family of distributions Benoit "
            "Mandelbrot proposed for them. The central limit theorem says that sums of many small independent pieces "
            "look Gaussian. Paul Lévy asked, in the 1920s, which shapes survive being added up at all: if you sum "
            "independent copies, you get the same shape, only wider. <bookmark mark='a'/> The answer is the stable "
            "family, indexed by alpha between zero and two. Alpha equal to two is the Gaussian. Below two, the tails "
            "fall like a power of x, so slowly that the variance is infinite. Alpha equal to one is the Cauchy. "
            "<bookmark mark='b'/> In 1963 Mandelbrot fitted cotton prices with alpha near one point seven, and in "
            "1965 Eugene Fama's thesis found alphas below two for the thirty stocks of the Dow. If they were right, "
            "volatility would not exist as a number, and the whole of option pricing would need rebuilding."
        ) as vo:
            self.play(FadeIn(g), Create(curves[0]), FadeIn(leg[0]), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in curves[1:]], lag_ratio=0.3), FadeIn(leg[1:]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def estimate(self, s):
        dec = s["decades"]
        keys = sorted(dec)
        g = axes([0, len(keys) + 1.5], [1.0, 2.0], x_length=7.4, y_length=4.2, ylabel=r"McCulloch's $\hat\alpha$, daily returns",
                 xticks=[], yticks=[1.0, 1.2, 1.4, 1.6, 1.8, 2.0], yfmt=lambda u: f"{u:.1f}", font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        w = ax.c2p(0.6, 0)[0] - ax.c2p(0, 0)[0]
        bars, xl = VGroup(), VGroup()
        for i, k in enumerate(keys):
            top, bot = ax.c2p(i + 0.5, dec[k]), ax.c2p(i + 0.5, 1.0)
            bars.add(Rectangle(width=w, height=top[1] - bot[1], stroke_width=0, fill_color=P_C, fill_opacity=0.85).move_to(
                (top + bot) / 2))
            xl.add(label(f"{k}s", font_size=16, color=GREY_B).next_to(bot, DOWN, buff=0.1))
        i = len(keys) + 0.6
        top, bot = ax.c2p(i, s["btc"]["alpha"]), ax.c2p(i, 1.0)
        bb = Rectangle(width=w, height=top[1] - bot[1], stroke_width=0, fill_color=Q_C, fill_opacity=0.85).move_to((top + bot) / 2)
        bl = label(r"BTC", font_size=16, color=Q_C).next_to(bot, DOWN, buff=0.1)
        two = DashedLine(ax.c2p(0, 2.0), ax.c2p(len(keys) + 1.5, 2.0), color=MART, stroke_width=2)
        side = VGroup(
            MathTex(rf"\text{{US, 1926--2020: }} \hat\alpha = {s['full']['alpha']:.2f}", font_size=30, color=P_C),
            MathTex(rf"\text{{Bitcoin, 2017--2020: }} {s['btc']['alpha']:.2f}", font_size=30, color=Q_C),
            wrapped_label(r"estimated from five quantiles of the distribution (McCulloch 1986), which is robust to the "
                          r"extreme days", 4.4, 20, GREY_B),
            wrapped_label(r"Mantegna and Stanley (1995), the S\&P 500 by the minute, 1984--89: $\alpha = 1.40$", 4.4, 21,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        src = real_data(r"Kenneth French's daily US market; Binance BTCUSDT daily; the House's \texttt{stable\_mcculloch}")
        with self.voiceover(
            "Measure it. The House fits a stable law to daily returns from five quantiles, a method published by "
            "J. Huston McCulloch in 1986 that ignores the most extreme days. <bookmark mark='a'/> The American "
            "market, decade by decade: alpha between one point four and one point six, never near two. Over the whole "
            "sample, one point four. Bitcoin, lower still: one point two seven. <bookmark mark='b'/> In 1995 Rosario "
            "Mantegna and Eugene Stanley found the same one point four in the S and P 500 minute by minute. By this "
            "measure, the center of the return distribution is shaped like a stable law."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(two))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), FadeIn(xl), FadeIn(side[0]),
                      FadeIn(side[2]))
            self.play(GrowFromEdge(bb, DOWN), FadeIn(bl), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def charfun(self, e, s):
        rows = [cmath(r"X_1 + \dots + X_n", r"\overset{d}{=}", r"n^{1/\alpha} X", font_size=40),
                cmath(r"\varphi(t) = \mathbb{E}e^{itX}", r"=", r"e^{-|ct|^\alpha} \;\Rightarrow\; \varphi(t)^n = "
                      r"e^{-n|ct|^\alpha} = \varphi(n^{1/\alpha}t)", font_size=38),
                cmath(r"\log\big(-\log|\varphi(t)|^2\big)", r"=", r"\log(2c^\alpha) + \alpha \log|t|", font_size=40,
                      colors={r"\log(2c^\alpha) + \alpha \log|t|": Q_C})]
        whys = [why(r"stability: a sum of $n$ copies is one copy, stretched by $n^{1/\alpha}$"),
                why(r"characteristic functions multiply under independent sums; this one is the symmetric stable law"),
                why(r"take logs twice: a straight line in $\log t$ whose slope is $\alpha$ (Koutrouvelis 1980)")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-1.0, buff=0.62, edge=6.9)
        us, ga = e["us"], e["gauss"]
        t = np.asarray(us["t"])
        g = axes([np.log(0.1) - 0.1, 0.1], [-6, 1.2], x_length=5.6, y_length=3.0, xlabel=r"$\log t$",
                 ylabel=r"$\log(-\log|\hat\varphi(t)|^2)$", xticks=[np.log(0.1), np.log(0.3), 0.0],
                 xfmt=lambda v: f"{v:.1f}", yticks=[-4, -2, 0], font_size=15).to_corner(DL, buff=0.45)
        ax = g.ax
        circ = Circle(radius=1.1, color=GREY_C, stroke_width=1.5).to_corner(DR, buff=0.7).shift(UP * 0.1)
        tk = ValueTracker(0.0)
        phi = np.asarray(us["phi"])
        vec = always_redraw(lambda: Arrow(circ.get_center(), circ.get_center() + RIGHT * 1.1 * at_index(phi, tk)
                                          .__float__(), buff=0, color=QC.IDEA, stroke_width=4)
                            .rotate(at_index(t, tk) * 2.0, about_point=circ.get_center()))
        clab = label(r"$\hat\varphi(t) = \frac1n \sum_j e^{itr_j}$: its length shrinks as $t$ grows", font_size=18,
                     color=GREY_A).next_to(circ, DOWN, buff=0.2)
        dots_us = VGroup(*[Dot(ax.c2p(np.log(a), b), radius=0.05, color=P_C) for a, b in zip(t, us["y"])])
        dots_g = VGroup(*[Dot(ax.c2p(np.log(a), b), radius=0.05, color=MART) for a, b in zip(t, ga["y"])])
        fit_us = curve(ax, np.log(t), us["alpha"] * np.log(t) + us["intercept"], P_C, stroke_width=2.5)
        fit_g = curve(ax, np.log(t), ga["alpha"] * np.log(t) + ga["intercept"], MART, stroke_width=2.5)
        res = VGroup(MathTex(rf"\text{{US daily: slope }} {us['alpha']:.2f}\ [{e['boot_lo']:.2f}, {e['boot_hi']:.2f}]",
                             font_size=26, color=P_C),
                     MathTex(rf"\text{{Gaussian control: }} {ga['alpha']:.2f}", font_size=26, color=MART),
                     MathTex(rf"\text{{McCulloch's quantiles: }} {s['full']['alpha']:.2f}", font_size=26, color=GREY_A)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(g, RIGHT, buff=0.4).align_to(g, DOWN)
        agree = abs(us["alpha"] - s["full"]["alpha"]) < 0.1
        verdict = ("The two estimators agree, which is what a stable law would do." if agree else
                   "The two estimators disagree: quantiles of the centre say one point four, the characteristic "
                   "function, which weighs the whole body, gives a larger alpha. A true stable law would give one "
                   "answer.")
        with self.voiceover(
            "Why do stable laws exist? Stability says that the sum of n independent copies is one copy, stretched "
            "by n to the one over alpha. <bookmark mark='a'/> Characteristic functions turn sums into products, and "
            "the exponential of minus the absolute value of c t to the alpha does exactly that: its nth power is "
            "itself, with t stretched. That is the symmetric stable law, and the generalized central limit theorem "
            "says that sums of variables whose tails fall like a power below two converge to one. "
            "<bookmark mark='b'/> Take logs twice and the alpha becomes a slope: an estimator due to Ioannis "
            "Koutrouvelis in 1980. <bookmark mark='c'/> On the data, average e to the i t r over every daily return; "
            "the arrow's length is the size of that average, and each t gives a dot. The Gaussian control lines up "
            f"with slope {ga['alpha']:.2f}. The American market gives {us['alpha']:.2f}. " + verdict
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(g), Create(circ), FadeIn(clab))
            self.add(vec)
            self.play(tk.animate.set_value(float(len(t) - 1)), LaggedStart(*[FadeIn(d) for d in dots_us], lag_ratio=0.3),
                      run_time=4, rate_func=linear)
            vec.clear_updaters()
            self.play(Create(fit_us), FadeIn(dots_g), Create(fit_g), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def fit(self, mle, s):
        runs = mle["runs"]
        T = max(len(r_["log"]) for r_ in runs)

        def pad(a):
            a = list(a)
            return a + [a[-1]] * (T - len(a))

        nll = np.array([pad(np.minimum.accumulate([row[4] for row in r_["log"]])) for r_ in runs])
        alph = np.array([pad([row[0] for row in r_["log"]]) for r_ in runs])
        nll = nll - nll[:, -1:].min()
        steps = np.arange(T)
        ck = [0, 5, 15, 30, 60, T - 1]

        def frame(i):
            k = ck[i]
            g = axes([0, T], [1.0, 2.05], x_length=4.6, y_length=3.0, xlabel=r"likelihood evaluations",
                     ylabel=r"$\alpha$ being tried", xticks=[0, T - 1], yticks=[1.2, 1.6, 2.0], font_size=14)
            grp = VGroup(g)
            for j, row in enumerate(alph):
                grp.add(curve(g.ax, steps[:k + 1] if k else steps[:2], row[:k + 1] if k else row[:2],
                              [QC.IDEA, P_C, Q_C][j], stroke_width=2))
            grp.add(DashedLine(g.ax.c2p(0, s["full"]["alpha"]), g.ax.c2p(T, s["full"]["alpha"]), color=GREY_B,
                               stroke_width=1.5))
            return grp

        rp = TrainingReplay(steps, nll, frame, ck, ylabel=r"best negative log-likelihood so far (minus the final)",
                            xlabel=r"evaluations", color=QC.IDEA)
        head = label(r"Maximum likelihood for $(\alpha, \beta, \text{scale}, \text{location})$, Nelder--Mead from the "
                     r"Gaussian corner; three random 1{,}500-day samples", font_size=20, color=GREY_A).to_edge(UP, buff=0.3)
        a_ = mle["alphas"]
        mc = mle["mcc"]
        spread = max(a_) - min(a_)
        res = MathTex(rf"\hat\alpha_{{\text{{MLE}}}} = {a_[0]:.2f}, {a_[1]:.2f}, {a_[2]:.2f};\ "
                      rf"\text{{McCulloch on the same samples: }} {mc[0]:.2f}, {mc[1]:.2f}, {mc[2]:.2f}",
                      font_size=26, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        close = abs(np.mean(a_) - np.mean(mc)) <= max(spread, 0.05)
        verdict = ("Maximum likelihood lands within the spread of the samples of McCulloch's answer."
                   if close else "Maximum likelihood lands above McCulloch's answer, by more than the spread across "
                                 "samples: the likelihood, which listens to every day, prefers a lighter tail than "
                                 "the quantiles do.")
        with self.voiceover(
            "A third estimator, the most careful: maximum likelihood, the stable density computed numerically for "
            "every candidate. Watch it learn. Each evaluation tries a new alpha, beta, scale and location, starting "
            "from the Gaussian corner, alpha near two. <bookmark mark='a'/> On the right, the best fit so far; on the "
            "left, the alpha being tried, for three random samples of fifteen hundred days. The search wanders, "
            "then settles. <bookmark mark='b'/> It ends at alpha "
            f"{np.mean(a_):.2f} on average. " + verdict
        ) as vo:
            self.play(FadeIn(head), FadeIn(rp))
            vo.wait_until("a")
            rp.play(self, run_time=7)
            vo.wait_until("b")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def aggregate(self, e):
        h = np.asarray(e["h"], float)
        ku, kg = np.asarray(e["kurt_us"]), np.asarray(e["kurt_gauss"])
        g = axes([0, np.log10(60) + 0.05], [-1, 20], x_length=7.0, y_length=4.2, xlabel=r"horizon $h$, days (log scale)",
                 ylabel=r"excess kurtosis of $h$-day returns", xticks=list(np.log10([1, 5, 20, 60])),
                 xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0, 5, 10, 15, 20], font_size=17).to_edge(LEFT, buff=0.7)
        ax = g.ax
        tk = ValueTracker(0.0)
        lu = tracing(ax, np.log10(h), ku, tk, P_C, stroke_width=3)
        lg = tracing(ax, np.log10(h), kg, tk, MART, stroke_width=3)
        decays = ku[-1] < ku[0] / 2
        side = VGroup(
            legend([(P_C, r"US daily, summed over $h$ days"), (MART, r"Gaussian control")], font_size=20),
            label(r"a stable law keeps its shape under sums: the kurtosis would not fall", font_size=20, color=GREY_A),
            MathTex(rf"h = 1: {ku[0]:.1f} \quad h = 60: {ku[-1]:.1f}", font_size=30, color=P_C),
            wrapped_label(r"finite variance: the generalized CLT is not needed; Part 1's tail exponent near 3 and "
                          r"changing volatility (Parts 7, 13) explain the shape", 4.6, 20, LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        verdict = ("It falls, unevenly but clearly: the tails thin out as days are added, as they must if the variance "
                   "is finite." if decays else
                   "It falls only a little, which on its own cannot settle the question.")
        with self.voiceover(
            "One more test, the simplest. If daily returns were stable, sums of them would have the same shape at "
            "every horizon, and the kurtosis, the heaviness of the tails, would not fall as you add days. "
            "<bookmark mark='a'/> The Gaussian control sits at zero. The American market starts at "
            f"{ku[0]:.0f} for one day. " + verdict
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[:2]))
            self.add(lu, lg)
            vo.wait_until("a")
            self.play(tk.animate.set_value(float(len(h) - 1)), run_time=4, rate_func=linear)
            lu.clear_updaters()
            lg.clear_updaters()
            self.play(FadeIn(side[2:]))
        self.wait(0.4)
        self.clear_scene()
