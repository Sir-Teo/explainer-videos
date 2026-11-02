from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, hist_bars, load, predict, show_card


class Bayes(VoiceoverScene):
    def construct(self):
        gb = load("gibbs")
        sh = load("shrinkage")
        self.card()
        self.scramble(sh)
        self.derive()
        self.springs(gb)

    def card(self):
        c = chapter_card(12, r"Shrinkage and Bayes", r"What do you learn from 40 estimates at once?", part=PART)
        with self.voiceover("Chapter twelve. Shrinkage, and Bayes."):
            show_card(self, c)
        self.play(FadeOut(c))

    def scramble(self, sh):
        raw, later = np.asarray(sh["raw"]), np.asarray(sh["later"])
        n = len(raw)
        g = axes([0.0, 0.2], [0, 1], x_length=9.0, y_length=3.6, xlabel=r"mean excess return a year",
                 yticks=[], xticks=[0, 0.05, 0.10, 0.15, 0.20], xfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17)
        g.to_edge(UP, buff=0.9).to_edge(LEFT, buff=2.8)
        ax = g.ax
        y0, y1 = 0.8, 0.2
        top = VGroup(*[Dot(ax.c2p(v, y0), radius=0.05, color=DATA_C) for v in raw])
        bot = VGroup(*[Dot(ax.c2p(v, y1), radius=0.05, color=GOOD) for v in later])
        links = VGroup(*[Line(ax.c2p(a, y0), ax.c2p(b, y1), stroke_width=1, color=GREY_C).set_stroke(opacity=0.6)
                         for a, b in zip(raw, later)])
        lt = label(r"estimated, 1927--1973", font_size=20, color=DATA_C).next_to(ax.c2p(0, y0), LEFT, buff=0.1)
        lb = label(r"realized, 1974--2020", font_size=20, color=GOOD).next_to(ax.c2p(0, y1), LEFT, buff=0.1)
        rk = np.corrcoef(np.argsort(np.argsort(raw)), np.argsort(np.argsort(later)))[0, 1]
        res = MathTex(rf"\text{{rank correlation, first half vs second: }} {rk:.2f}", font_size=30, color=WHITE)
        res.to_edge(DOWN, buff=0.8)
        with self.voiceover(
            f"Take {n} of French's industries and estimate each one's average excess return from the first half of "
            f"the data, 1927 to 1973. The estimates spread from {100 * raw.min():.0f} to {100 * raw.max():.0f} percent "
            "a year. Which industries "
            "are really better? <bookmark mark='a'/> Look at what each actually earned in the second half. The "
            f"ranks scramble: the rank correlation between the halves is {rk:.2f}. Most of the spread in the first "
            "half was noise. What is the best forecast of each industry, given all forty estimates?"
        ) as vo:
            self.play(FadeIn(g), FadeIn(top), FadeIn(lt))
            vo.wait_until("a")
            self.play(Create(links), FadeIn(bot), FadeIn(lb), run_time=2)
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        C_ = {r"B_i": ALT, r"\hat\tau^2": EST}
        rows = [cmath(r"\alpha_i \sim N(\mu, \tau^2)", r",", r"\ \hat\alpha_i \mid \alpha_i \sim N(\alpha_i, s_i^2)",
                      font_size=36, colors=C_),
                cmath(r"\alpha_i \mid \hat\alpha_i", r"\sim", r"N\big(B_i\mu + (1 - B_i)\hat\alpha_i,\ (1 - B_i)s_i^2\big),"
                      r"\ \ B_i = \frac{s_i^2}{s_i^2 + \tau^2}", font_size=34, colors=C_),
                cmath(r"\hat\tau^2", r"=", r"\max\big(0,\ \mathrm{var}(\hat\alpha) - \overline{s^2}\big)", font_size=36,
                      colors=C_),
                cmath(r"R(\hat\mu^{JS})", r"=", r"k - (k - 2)^2\,\mathbb{E}\big[1/\|x\|^2\big] < k", font_size=36,
                      colors=C_),
                cmath(r"\tau^2 \mid \alpha, \mu \sim \text{scaled Inv-}\chi^2", r",",
                      r"\ \alpha_i \mid \tau, \mu \sim N(\cdot),\ \ \mu \mid \alpha, \tau \sim N(\cdot)", font_size=34,
                      colors=C_)]
        whys = [why(r"a hierarchy: true means drawn from a population; each estimate noisy around its true mean"),
                why(r"complete the square: a precision-weighted average; noisy estimates ($s_i$ large) are pulled "
                    r"hardest"),
                why(r"empirical Bayes: the spread of the estimates minus the spread their noise alone would make"),
                why(r"Stein (1956), James and Stein (1961): with $k \ge 3$ means, shrinking beats the raw estimates "
                    r"in total squared error, always; Problem 5"),
                why(r"Gibbs sampling: each conditional is a textbook distribution, so draw them in turn")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.75, edge=6.8)
        with self.voiceover(
            "Bayes gives the answer as a hierarchy. The true means are drawn from a population with centre mu and "
            "spread tau; each estimate is its true mean plus noise. <bookmark mark='a'/> Complete the square, and "
            "the posterior mean is a precision-weighted average of the grand mean and the estimate. The weight on "
            "the grand mean, B, is the estimate's noise variance over noise plus tau squared: the noisier the "
            "estimate, the harder it is pulled in. <bookmark mark='b'/> Empirical Bayes estimates tau from the data: "
            "the variance of the estimates, minus the part their own noise explains. <bookmark mark='c'/> Charles "
            "Stein proved in 1956 that with three or more means, the raw estimates are inadmissible: shrinking "
            "beats them in total squared error, whatever the truth. <bookmark mark='d'/> And instead of plugging in "
            "one estimate of tau, a full Bayesian treats tau as unknown too, and samples everything by Gibbs: draw "
            "the means given tau, then mu, then tau given the means, and repeat."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.5)
        self.clear_scene()

    def springs(self, gb):
        raw, later, se = (np.asarray(gb[k]) for k in ("raw", "later", "se"))
        mu_tr, tau_tr = np.asarray(gb["mu"]), np.asarray(gb["tau"])
        n = len(raw)
        order = np.argsort(raw)
        raw, later, se = raw[order], later[order], se[order]
        g = axes([0, n + 1], [0.0, 0.18], x_length=7.0, y_length=4.6, ylabel=r"mean excess return a year",
                 xticks=[], yticks=[0.05, 0.10, 0.15], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        k = ValueTracker(0)
        T = mu_tr.shape[1]

        def state():
            i = int(min(k.get_value(), T - 1))
            return float(mu_tr[0, i]), float(tau_tr[0, i])

        def beads():
            mu, tau = state()
            B = se ** 2 / (se ** 2 + tau ** 2)
            pos = B * mu + (1 - B) * raw
            out = VGroup()
            bar = DashedLine(ax.c2p(0.5, mu), ax.c2p(n + 0.5, mu), color=EST, stroke_width=3)
            out.add(bar)
            for j, (r, p, s) in enumerate(zip(raw, pos, se)):
                x = j + 1
                out.add(Line(ax.c2p(x, r), ax.c2p(x, p), color=GREY_C, stroke_width=1 + 30 * s))
                out.add(Dot(ax.c2p(x, np.clip(p, 0, 0.18)), radius=0.05, color=DATA_C))
            return out
        rods = VGroup(*[Line(ax.c2p(j + 1, 0.02), ax.c2p(j + 1, 0.17), color=GREY_D, stroke_width=1) for j in range(n)])
        ghosts = VGroup(*[Dot(ax.c2p(j + 1, r), radius=0.035, color=GREY_B, fill_opacity=0.5) for j, r in enumerate(raw)])
        bm = always_redraw(beads)
        tg = axes([0, T], [0, 0.05], x_length=4.6, y_length=2.0, ylabel=r"$\tau$ (4 chains)", xticks=[0, T],
                  xfmt=lambda v: f"{int(v) * 10:,}".replace(",", "{,}"), yticks=[0, 0.025, 0.05], font_size=14)
        tg.to_edge(RIGHT, buff=0.4).to_edge(UP, buff=0.7)
        cols = [ALT, EST, GOOD, QC.Q]
        traces = always_redraw(lambda: VGroup(*[curve(tg.ax, np.arange(int(k.get_value()) + 1),
                                                      np.minimum(tau_tr[c, :int(k.get_value()) + 1], 0.05), cols[c],
                                                      stroke_width=1.5) for c in range(4)])
                               if k.get_value() >= 1 else VGroup())
        tau_ro = always_redraw(lambda: MathTex(rf"\tau = {100 * state()[1]:.1f}\%,\ \ \mu = {100 * state()[0]:.1f}\%",
                                               font_size=26, color=WHITE).next_to(tg, DOWN, buff=0.2))
        oos = VGroup(*[Dot(ax.c2p(j + 1, np.clip(v, 0, 0.18)), radius=0.05, color=GOOD) for j, v in enumerate(later)])
        res = VGroup(
            MathTex(rf"\text{{posterior median of }} \tau: {100 * gb['tau_median']:.1f}\%", font_size=26, color=EST),
            MathTex(rf"\text{{error vs.\ 1974--2020: raw }} {1e4 * gb['mse_raw']:.1f},\ \text{{Gibbs }} "
                    rf"{1e4 * gb['mse_post']:.1f},\ \text{{EB }} {1e4 * gb['mse_eb']:.1f}", font_size=24, color=GOOD),
            label(r"mean squared error, (\% a year)$^2$; green dots: the second half", font_size=17, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(tau_ro, DOWN, buff=0.35).align_to(tg, LEFT)
        q = predict(r"One industry has a huge raw estimate and a huge standard error. Does it shrink most or least?",
                    width=11.0).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Here it is running. Each industry is a bead on its own rod, at its raw estimate, sorted from lowest to "
            "highest, tied by a spring to a bar at the grand mean. The thicker the spring, the noisier the estimate. "
            "<bookmark mark='a'/> Start the sampler. Four chains, each five thousand draws, traced on the right. "
            "Every draw of tau sets every bead's position: when tau is large, the beads are free; when it is small, "
            "the springs win. <bookmark mark='b'/> Tau keeps falling back toward zero. The data cannot tell the "
            "industries apart, so the posterior squeezes nearly every bead onto the bar: about "
            f"{100 * gb['shrink_frac']:.0f} percent of the spread disappears. <bookmark mark='c'/> Now the second "
            "half's realized means, in green. The shrunk beads sit far closer to them: the forecast error falls "
            f"from {1e4 * gb['mse_raw']:.1f} to {1e4 * gb['mse_post']:.1f}, the same as empirical Bayes. A prior is not "
            "a bias to be ashamed of; it is how you borrow strength across assets, and Parts twenty-seven and thirty "
            "use it everywhere. <bookmark mark='d'/> Pause and predict: an industry with a huge raw estimate and a "
            "huge standard error. It shrinks the most."
        ) as vo:
            self.play(FadeIn(g), FadeIn(rods), FadeIn(ghosts), FadeIn(tg))
            self.add(bm)
            vo.wait_until("a")
            self.add(traces, tau_ro)
            self.play(k.animate.set_value(T - 1), run_time=vo.until("c") - 0.3, rate_func=linear)
            self.play(FadeIn(res[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d) for d in oos], lag_ratio=0.03), FadeIn(res[1]), FadeIn(res[2]))
            vo.wait_until("d")
            self.play(FadeIn(q, shift=UP * 0.2))
        for m_ in (bm, traces, tau_ro):
            m_.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
