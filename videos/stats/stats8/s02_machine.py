from __future__ import annotations

import numpy as np

from videos.stats.stats8.common import *  # noqa: F403


class Machine(VoiceoverScene):
    def construct(self):
        self.card()
        self.machine()
        self.three_n()
        self.se()
        self.proportion()
        self.median()
        self.median_se()

    def card(self):
        card = chapter_card(1, r"Sampling distributions", r"What would happen if we sampled again?", part=PART)
        with self.voiceover("Chapter one. Sampling distributions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def machine(self):
        d = load("machine")
        pop = np.asarray(d["values"])
        m = SamplingMachine(pop, value_range=(150, 202), stat_range=(166, 186), bins=40, n_dots=700,
                            value_label=r"heights in this sample (cm)", stat_label=r"the sample mean (cm)",
                            ticks=[155, 175, 195], stat_ticks=[168, 172, 176, 180, 184], seed=8)
        mu = d["values_mean"]
        tl = Line(m.hist_ax[0].c2p(mu, 0), m.hist_ax[0].c2p(mu, 0.95), color=EXACT, stroke_width=3)
        tlab = MathTex(rf"\mu = {mu:.1f}", font_size=28, color=EXACT).next_to(tl, UP, buff=0.06)
        g = np.random.Generator(np.random.PCG64(8))
        samples = [pop[g.integers(0, len(pop), 4)] for _ in range(24)]
        tag = simulated_tag(r"simulated: 3,000 World men as the source pool; \ samples of 4")
        with self.voiceover(
            "Part 1 met the sampling machine; now we use it in earnest. <bookmark mark='a'/> The source pool: three thousand of the "
            "World's adult men. The machine draws four at random. <bookmark mark='b'/> Their heights land on the "
            "line, and their mean drops into the chart. <bookmark mark='c'/> Another four, another mean. "
            "<bookmark mark='d'/> Keep going. The chart that builds up is the sampling distribution of the mean: the "
            "distribution of a statistic over all the samples we might have drawn. It's the single most important "
            "idea in this course, because every standard error, interval and test is a statement about it."
        ) as vo:
            self.play(FadeIn(m), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(tl), FadeIn(tlab))
            vo.wait_until("b")
            m.draw(self, samples[0], samples[0].mean(), run_time=3.0, stat_tex=rf"$\bar x = {samples[0].mean():.1f}$")
            vo.wait_until("c")
            m.draw(self, samples[1], samples[1].mean(), run_time=2.4, stat_tex=rf"$\bar x = {samples[1].mean():.1f}$")
            vo.wait_until("d")
            for s_ in samples[2:12]:
                m.draw(self, s_, s_.mean(), run_time=0.8)
            m.add_stats(self, [s_.mean() for s_ in samples[12:]] + list(np.asarray(d["4"]["means"])[:400]), run_time=3.0, steps=8)
        self.clear_scene()

    def three_n(self):
        d = load("machine")
        ed = np.asarray(d["edges"])
        A = axes([160, 192], [0, 0.48], x_length=8.4, y_length=4.4, xlabel=r"sample mean of $n$ men's heights (cm)",
                 xticks=[160, 168, 176, 184, 192], yticks=[0, 0.2, 0.4], center=[-1.6, -0.4, 0])
        ax = A.ax
        cols = {"4": S.POST, "16": S.LIK, "64": SIM}
        hs = VGroup(*[hist_bars(ax, ed, np.asarray(d[n]["hist"]), color=c, opacity=0.5) for n, c in cols.items()])
        mu = d["values_mean"]
        tl = DashedLine(ax.c2p(mu, 0), ax.c2p(mu, 0.48), color=EXACT, stroke_width=2)
        leg = legend([(c, rf"$n = {n}$: \ SD {d[n]['sd_mean']:.2f}") for n, c in cols.items()], font_size=24).move_to([4.7, 1.6, 0])
        rows = fit_rows(VGroup(
            label(r"four times the sample, \ half the spread", font_size=26, color=S.ACCENT),
            MathTex(rf"\sigma = {d['sigma']:.2f}:\ \ \tfrac{{\sigma}}{{\sqrt 4}} = {d['sigma'] / 2:.2f},\ \ \tfrac{{\sigma}}{{\sqrt{{16}}}} = "
                    rf"{d['sigma'] / 4:.2f},\ \ \tfrac{{\sigma}}{{\sqrt{{64}}}} = {d['sigma'] / 8:.2f}", font_size=24),
            label(r"centred on $\mu$ at every $n$: \ $\bar x$ is unbiased", font_size=24, color=EXACT),
        ), 4.6, 0.3, [4.5, -0.8, 0])
        tag = simulated_tag(r"simulated: 20,000 samples of each size")
        with self.voiceover(
            "Now the full sampling distributions, twenty thousand samples each. <bookmark mark='a'/> Means of four "
            "men: a wide bell. <bookmark mark='b'/> Means of sixteen: half as wide. <bookmark mark='c'/> Means of "
            "sixty-four: half as wide again. <bookmark mark='d'/> The spread falls like sigma over root n, Part 6's "
            "square-root law, and the simulated standard deviations closely approximate the formula within simulation noise. And all three "
            "are centred on the true mean: the sample mean is unbiased."
        ) as vo:
            self.play(FadeIn(A), Create(tl), FadeIn(tag))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(hs[k]), FadeIn(leg[k]))
            vo.wait_until("d")
            self.play(FadeIn(rows))
        self.clear_scene()

    def se(self):
        rows = [
            cmath(r"\mathrm{SD}(\bar X)", r"=", r"\frac{\sigma}{\sqrt n}", r"\qquad \text{the true spread of the sampling distribution}",
                  font_size=32),
            cmath(r"\mathrm{SE}(\bar x)", r"=", r"\frac{s}{\sqrt n}", r"\qquad \text{its estimate, \ from one sample}", font_size=32),
        ]
        rows[0][2].set_color(EXACT)
        rows[1][2].set_color(SIM)
        whys = [why(r"IID draws with finite variance:  \ $\mathrm{Var}\,\bar X = \sigma^2/n$"), why(r"plug in $s$ for $\sigma$")]
        rem = fit_rows(VGroup(
            label(r"the standard error is how much the estimate would wobble \emph{if} we sampled again", font_size=26),
            label(r"one sample estimates it: \ the sample's spread stands in for the population's", font_size=24, color=GREY_A),
            label(r"but $s$ itself wobbles: \ for small $n$, \ badly (the hook; \ chapter 5)", font_size=24, color=RESID),
        ), 12.6, 0.3, [0, -1.8, 0])
        intro = label('Estimating how much a mean varies', font_size=36)
        with self.voiceover(
            "This is the miracle of statistics. <bookmark mark='a'/> The spread of the sampling distribution, the "
            "standard deviation of the mean over all possible samples, is sigma over root n. <bookmark mark='b'/> We "
            "never see those other samples. But we can estimate sigma from the one sample we have, and so estimate "
            "the spread: s over root n, the standard error. <bookmark mark='c'/> One sample tells us how much it "
            "would wobble if we sampled again. The catch is that s wobbles too, and with small samples it wobbles "
            "badly. That was Gosset's problem, and chapter five is its solution."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=2.4, x=-2.4, buff=1.0, edge=6.9)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rem], lag_ratio=0.4))
        self.clear_scene()

    def median(self):
        d = load("machine")
        ed = np.asarray(d["edges"])
        A = axes([166, 186], [0, 0.48], x_length=7.4, y_length=4.2, xlabel=r"statistic, \ samples of 64 men (cm)",
                 xticks=[168, 172, 176, 180, 184], yticks=[0, 0.2, 0.4], center=[-2.0, -0.4, 0])
        ax = A.ax
        hm = hist_bars(ax, ed, np.asarray(d["64"]["hist"]), color=SIM, opacity=0.6)
        hd = hist_bars(ax, ed, np.asarray(d["64"]["hist_med"]), color=S.POST, opacity=0.5)
        leg = legend([(SIM, rf"mean: \ SD {d['64']['sd_mean']:.2f}"), (S.POST, rf"median: \ SD {d['64']['sd_median']:.2f}")],
                     font_size=24).move_to([4.4, 1.6, 0])
        e64 = d["eff"]["64"]
        rows = fit_rows(VGroup(
            label(r"every statistic has a sampling distribution", font_size=24),
            MathTex(rf"\text{{efficiency}} = \frac{{\mathrm{{Var}}(\bar x)}}{{\mathrm{{Var}}(\text{{median}})}} = {e64:.2f}", font_size=28),
            MathTex(r"\to \tfrac{2}{\pi} = 0.64 \ \text{for normal data}", font_size=26, color=EXACT),
            label(r"the median needs about 1.6 times the data \ \ldots{} \ but resists outliers (Part 30)", font_size=22, color=GREY_A),
        ), 5.2, 0.3, [4.4, -0.6, 0])
        tag = simulated_tag(r"simulated: 20,000 samples of 64")
        with self.voiceover(
            "Every statistic has a sampling distribution, not just the mean. <bookmark mark='a'/> Here are the mean "
            "and the median of samples of sixty-four men. They lie near their population centers; the male-height population is approximately symmetric. "
            "<bookmark mark='b'/> But the median's distribution is wider. The ratio of their variances, the "
            f"efficiency, is about {e64:.2f}, close to two over pi, which theory gives for normal data. To match the "
            "mean's precision, the median needs about one point six times as much data. <bookmark mark='c'/> In "
            "return it shrugs off outliers, a trade Part 30 weighs carefully. Comparing sampling distributions is how "
            "we choose between estimators."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hm), FadeIn(hd), FadeIn(leg), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def median_se(self):
        d = load("extras")["median_se"]
        rows = [
            cmath(r"\mathrm{SD}(\text{median})", r"\approx", r"\frac{1}{2 f(m)\sqrt n}", font_size=34),
            cmath(r"\text{normal: } f(m) = \frac{1}{\sigma\sqrt{2\pi}}", r"\ \Rightarrow\ ", r"\sigma\sqrt{\frac{\pi}{2}}\,\frac{1}{\sqrt n}", font_size=32),
            cmath(r"n = 64,\ \sigma = 7.10", r":\ ", rf"{d['64']:.2f}\ \text{{cm}} \quad (\text{{simulated }} {d['sim']:.2f})", font_size=32),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"asymptotic: IID, unique median, continuous positive density there"), why(r"so the efficiency is $2/\pi$"),
                why(r"a formula for one sample's SE, \ if we can estimate $f(m)$ (Part 29)")]
        intro = label('The median needs a local density estimate', font_size=36)
        with self.voiceover(
            "The median's spread has a formula too, found by Laplace. <bookmark mark='a'/> Under regularity conditions, its large-sample standard deviation is approximately "
            "one over twice the density at the median, times root n. Where the data are dense near the middle, the "
            "median is pinned down tightly; where they're sparse, it wanders. <bookmark mark='b'/> For a normal "
            "population the density at the median is one over sigma root two pi, which gives sigma times root pi over "
            "two, over root n, and the efficiency of two over pi. <bookmark mark='c'/> For sixty-four men that's one "
            "point one one centimetres, and the simulation says one point one oh. To use the formula on real data we "
            "need to estimate a density, which is the business of Part 29."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.8, buff=1.0, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def proportion(self):
        d = load("extras2")["prop"]
        hist = np.asarray(d["hist"])
        A = axes([-0.5, 35.5], [0, 0.13], x_length=7.0, y_length=4.0, xlabel=r"adults over 180 cm, \ in a sample of 100",
                 xticks=[0, 5, 10, 15, 20, 25, 30, 35], yticks=[0, 0.05, 0.1], center=[-2.2, -0.4, 0])
        ax = A.ax
        bars_ = VGroup()
        for k, v in enumerate(hist[:36]):
            lo, hi = ax.c2p(k - 0.4, 0), ax.c2p(k + 0.4, v)
            bars_.add(Rectangle(width=hi[0] - lo[0], height=max(1e-3, hi[1] - lo[1]), stroke_width=0, fill_color=SIM, fill_opacity=0.8)
                      .move_to([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0]))
        rows = fit_rows(VGroup(
            label(r"a proportion is a mean of 0s and 1s", font_size=24),
            MathTex(r"\mathrm{SE}(\hat p) = \sqrt{\frac{p(1 - p)}{n}}", font_size=32, color=EXACT),
            MathTex(rf"p = {d['p']:.3f}:\ \ {d['se']:.4f}\ \ (\text{{simulated }} {d['sim']:.4f})", font_size=26),
            label(r"the variance of a 0--1 variable is $p(1 - p)$: \ largest at $p = \tfrac12$", font_size=22, color=GREY_A),
        ), 5.0, 0.3, [4.4, 0.2, 0])
        tag = simulated_tag(r"simulated: 20,000 samples of 100")
        with self.voiceover(
            "The same law covers proportions, the most common statistic of all. <bookmark mark='a'/> What share of the "
            "World's adults are taller than a hundred and eighty centimetres? About fourteen and a half percent. Draw "
            "samples of a hundred and count. <bookmark mark='b'/> A proportion is just the mean of a variable that's one "
            "for yes and zero for no, whose variance is p times one minus p. So the standard error is the root of p times "
            "one minus p, over n: three and a half percentage points here, and the simulation agrees to the third "
            "decimal. It's largest when p is a half, which is why polls plan for that case."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_], lag_ratio=0.03), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1:]))
        self.clear_scene()
