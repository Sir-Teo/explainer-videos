from __future__ import annotations

import numpy as np

from videos.stats.stats16.common import *  # noqa: F403


class Principle(VoiceoverScene):
    def construct(self):
        self.card()
        self.resampler()
        self.histogram()
        self.two_worlds()
        self.check()
        self.how_many()
        self.assumes()

    def card(self):
        card = chapter_card(7, r"The bootstrap principle", r"Sample from the sample", lit=(1979,), part=PART)
        with self.voiceover("Chapter seven. The bootstrap principle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def resampler(self):
        d = load("law")
        L, G = np.asarray(museum.LAW_LSAT, float), np.asarray(museum.LAW_GPA, float)
        fi = np.asarray(d["first_idx"], int)
        br = BootstrapResampler([str(i + 1) for i in range(15)], center=[0.8, 2.1, 0], width=10.8, radius=0.26, font_size=18,
                                row_gap=1.3, color=DATA, copy_color=BOOT)
        lt = label(r"the sample", font_size=20, color=DATA).next_to(br.top[0], LEFT, buff=0.4)
        lb = label(r"a resample", font_size=20, color=BOOT).next_to(br.bottom[0], LEFT, buff=0.4)
        A = axes([0, 1], [0, 6], x_length=8.0, y_length=2.2, xlabel=r"$r^*$, \ the correlation of a resample", xticks=[0, 0.25, 0.5, 0.75, 1],
                 center=[0, -1.9, 0], font_size=18)
        ax = A.ax
        obs = DashedLine(ax.c2p(d["r"], 0), ax.c2p(d["r"], 6), color=OBS, stroke_width=2.5)
        rv = MathTex(r"r^* = ", font_size=30).move_to([4.6, 0.4, 0])
        val = DecimalNumber(0, num_decimal_places=3, font_size=30, color=BOOT).next_to(rv, RIGHT, buff=0.12)
        with self.voiceover(
            "<bookmark mark='a'/> Here is the bootstrap as a machine: the fifteen law schools as tokens. "
            "<bookmark mark='b'/> Draw a school at random, copy it down, put it back, and draw again, fifteen times. Some "
            "schools are copied twice or three times, some not at all. That's a resample: a new dataset of the same size, "
            "drawn with replacement from the sample. <bookmark mark='c'/> Compute its correlation, and drop it on the line. "
            "<bookmark mark='d'/> Clear, and resample again. Each resample is a dataset the population might plausibly have "
            "given us, if the population looked like the sample. Again. And again."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(br), FadeIn(lt))
            vo.wait_until("b")
            self.play(FadeIn(lb), br.resample(fi[0], run_time=2.4, lag=0.12))
            self.add(br.copies)
            vo.wait_until("c")
            r0 = float(np.corrcoef(L[fi[0]], G[fi[0]])[0, 1])
            self.play(FadeIn(A), Create(obs), FadeIn(rv), FadeIn(val))
            self.play(val.animate.set_value(r0))
            self.play(FadeIn(br.drop(ax, r0, 0.025, radius=0.07), scale=1.5))
            vo.wait_until("d")
            for k in range(1, 6):
                self.play(br.clear(run_time=0.3))
                self.play(br.resample(fi[k], run_time=1.0, lag=0.04))
                self.add(br.copies)
                rk = float(np.corrcoef(L[fi[k]], G[fi[k]])[0, 1])
                self.play(val.animate.set_value(rk), FadeIn(br.drop(ax, rk, 0.025, radius=0.07), scale=1.5), run_time=0.6)
        self.clear_scene()

    def histogram(self):
        d = load("law")
        reps = np.asarray(d["reps"])
        e = np.linspace(0, 1.0, 41)
        h = np.histogram(reps, e)[0]
        A = axes([0, 1], [0, 180], x_length=8.4, y_length=4.2, xlabel=r"$r^*$", ylabel=r"resamples (of 2,000)",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 50, 100, 150], center=[-1.4, 0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, e, h, color=BOOT, opacity=0.8)
        obs = DashedLine(ax.c2p(d["r"], 0), ax.c2p(d["r"], 175), color=OBS, stroke_width=3)
        rows = fit_rows(VGroup(
            label(r"2,000 resamples", font_size=24),
            MathTex(rf"\widehat{{\mathrm{{SE}}}}_{{\text{{boot}}}} = \text{{SD}}(r^*) = {d['se_boot']:.3f}", font_size=28, color=BOOT),
            label(r"skewed left: \ $r$ can't pass 1", font_size=22, color=GREY_A),
            MathTex(rf"\text{{normal formula}}: {d['se_normal']:.3f}", font_size=26),
            MathTex(rf"\text{{jackknife}}: {d['jack']['se']:.3f}", font_size=26),
        ), 4.2, 0.36, [4.9, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Do it two thousand times. The computer takes a fraction of a second. "
            "<bookmark mark='b'/> The bootstrap standard error is just the standard deviation of the two thousand resampled "
            "correlations: point one three five. <bookmark mark='c'/> The histogram is skewed to the left, because a correlation "
            "can't exceed one: the sampling distribution isn't normal, and the bootstrap shows it. <bookmark mark='d'/> The "
            "normal-theory formula said point one one five, <bookmark mark='e'/> the jackknife point one four three. Efron's "
            "paper used exactly this example, and found the same thing: a standard error for a statistic with no formula, or "
            "with a formula we don't trust, by brute force."
        ) as vo:
            self.play(FadeIn(A), Create(obs))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.03), FadeIn(rows[0]), run_time=2.0)
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def two_worlds(self):
        def box(t, col):
            tx = MathTex(t, font_size=34, color=col)
            return VGroup(RoundedRectangle(width=tx.width + 0.5, height=0.9, corner_radius=0.12, stroke_color=col, stroke_width=2),
                          tx.copy())

        realrow = [box(r"F", REAL), box(r"x_1, \ldots, x_n", REAL), box(r"\hat\theta = s(x)", REAL)]
        bootrow = [box(r"\hat F_n", BOOT), box(r"x^*_1, \ldots, x^*_n", BOOT), box(r"\hat\theta^* = s(x^*)", BOOT)]
        for row, y in ((realrow, 1.6), (bootrow, -1.0)):
            for k, b in enumerate(row):
                b.move_to([-4.2 + 4.2 * k, y, 0])
        arrs = VGroup(*[Arrow(r[k].get_right(), r[k + 1].get_left(), buff=0.1, color=GREY_B) for r in (realrow, bootrow) for k in range(2)])
        head_r = label(r"the real world", font_size=26, color=REAL).next_to(realrow[0], UP, buff=0.35).align_to(realrow[0], LEFT)
        head_b = label(r"the bootstrap world", font_size=26, color=BOOT).next_to(bootrow[0], DOWN, buff=0.3).align_to(bootrow[0], LEFT)
        down = Arrow(realrow[1].get_bottom(), bootrow[0].get_top() + RIGHT * 0.4, buff=0.15, color=OBS)
        dl = label(r"put mass $1/n$ on each $x_i$", font_size=20, color=OBS).next_to(down, RIGHT, buff=0.1).shift(UP * 0.1)
        foot = fit_rows(VGroup(  # below the bootstrap world's label
            label(r"we want the law of $\hat\theta - \theta$ under $F$: \ unknown", font_size=24, color=REAL),
            label(r"we can compute the law of $\hat\theta^* - \hat\theta$ under $\hat F_n$, \ by simulation", font_size=24, color=BOOT),
            label(r"the plug-in principle: \ use the second for the first", font_size=26, color=OBS),
        ), 12.4, 0.22, [0, -2.85, 0])
        with self.voiceover(
            "Efron's diagram makes the logic plain. <bookmark mark='a'/> In the real world, an unknown distribution F produces "
            "our sample, and the sample produces the estimate. If we could repeat that, we'd see the estimate's sampling "
            "distribution, but we get one sample. <bookmark mark='b'/> So build a stand-in for F from the sample: the empirical "
            "distribution, F-hat, which puts mass one over n on each observation. <bookmark mark='c'/> In the bootstrap world "
            "F-hat plays the part of the population. Sampling from it, with replacement, is resampling; and there we can repeat "
            "as often as we like. <bookmark mark='d'/> We want the distribution of the estimate's error under F, which we can't "
            "see. <bookmark mark='e'/> We can compute the distribution of the resampled estimate's error under F-hat. "
            "<bookmark mark='f'/> The bootstrap is the plug-in principle, Part 9's idea, applied to a whole sampling "
            "distribution: use the second as an estimate of the first. Part 30 will show when that's justified."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head_r), LaggedStart(FadeIn(realrow[0]), GrowArrow(arrs[0]), FadeIn(realrow[1]), GrowArrow(arrs[1]),
                                                  FadeIn(realrow[2]), lag_ratio=0.5), run_time=2.5)
            vo.wait_until("b")
            self.play(GrowArrow(down), FadeIn(dl), FadeIn(bootrow[0]))
            vo.wait_until("c")
            self.play(FadeIn(head_b), LaggedStart(GrowArrow(arrs[2]), FadeIn(bootrow[1]), GrowArrow(arrs[3]), FadeIn(bootrow[2]),
                                                  lag_ratio=0.5), run_time=2.0)
            for k, m_ in enumerate("def"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k]))
        self.clear_scene()

    def check(self):
        d = load("worlds")
        real, boot = np.asarray(d["real"]), np.asarray(d["boot"])
        e = np.linspace(15, 70, 45)
        A = axes([15, 70], [0, 0.2], x_length=5.6, y_length=3.2, xlabel=r"median income, \ thousands", ylabel=r"density",
                 xticks=[20, 40, 60], yticks=[0, 0.1, 0.2], center=[-3.6, 0.7, 0], font_size=18)
        B = axes([15, 70], [0, 0.2], x_length=5.6, y_length=3.2, xlabel=r"median of a resample", ylabel=r"density",
                 xticks=[20, 40, 60], yticks=[0, 0.1, 0.2], center=[3.0, 0.7, 0], font_size=18)
        w = e[1] - e[0]
        hr = hist_bars(A.ax, e, np.histogram(real, e)[0] / (len(real) * w), color=REAL, opacity=0.8)
        hb = hist_bars(B.ax, e, np.histogram(boot, e)[0] / (len(boot) * w), color=BOOT, opacity=0.8)
        tr = DashedLine(A.ax.c2p(d["truth"], 0), A.ax.c2p(d["truth"], 0.19), color=S.TRUTH, stroke_width=3)
        es = DashedLine(B.ax.c2p(d["est"], 0), B.ax.c2p(d["est"], 0.19), color=OBS, stroke_width=3)
        ta = label(r"2,000 real samples of 25 from the World", font_size=20, color=REAL).next_to(A, UP, buff=0.12)
        tb = label(r"2,000 resamples of one sample of 25", font_size=20, color=BOOT).next_to(B, UP, buff=0.12)
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{real SD}} = {d['sd_real']:.2f}\qquad \text{{bootstrap SD}} = {d['sd_boot']:.2f}", font_size=28),
            label(r"the bootstrap only sees one sample: \ its spikes are that sample's middle values", font_size=22, color=GREY_A),
        ), 12.4, 0.25, [0, -2.4, 0])
        tag = simulated_tag(r"the World's adults", corner=DR)
        with self.voiceover(
            "Can we check the principle? In the World, yes, because we can draw as many real samples as we like. "
            "<bookmark mark='a'/> The statistic is the median income, from samples of twenty-five. On the left, the real sampling "
            "distribution, two thousand samples from the World, centred on the true median of thirty-nine thousand. "
            "<bookmark mark='b'/> On the right, the bootstrap from just one of those samples, whose median is thirty-seven point "
            "seven. <bookmark mark='c'/> The real standard deviation is six point oh six; the bootstrap's, four point seven two. "
            "In the right ballpark, from one sample, but low. <bookmark mark='d'/> And the bootstrap histogram is spiky: the "
            "median of a resample can only be one of the sample's middle values, so it takes only sixteen distinct values. With "
            "a median and twenty-five observations, the bootstrap is rough. For smooth statistics like means and correlations "
            "it does much better."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ta), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in hr], lag_ratio=0.02), Create(tr), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(tb), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in hb], lag_ratio=0.02), Create(es), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def how_many(self):
        rows = [
            cmath(r"\text{possible resamples}", r":", r"15^{15} \approx 4 \times 10^{17};\ \ \binom{29}{15} = 77{,}558{,}760\ \text{distinct}", font_size=28),
            cmath(r"\text{the ideal bootstrap}", r":", r"\text{average over all of them}", font_size=30),
            cmath(r"B \text{ resamples}", r":", r"\text{Monte Carlo error} \propto 1/\sqrt{B}", font_size=30),
            cmath(r"\text{rule of thumb}", r":", r"B \approx 1{,}000 \text{ for an SE};\ \ \ge 2{,}000 \text{ for interval endpoints}", font_size=28),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"ordered draws; \ and as multisets"), why(r"exact, \ but out of reach"),
                why(r"Part 7's simulation error"), why(r"the tails need more draws than the middle")]
        with self.voiceover(
            "<bookmark mark='a'/> How many resamples? Fifteen schools can be drawn in fifteen to the fifteenth ordered ways; as "
            "unordered collections, there are seventy-seven million distinct resamples. <bookmark mark='b'/> The ideal bootstrap "
            "would average over all of them, and give the exact bootstrap distribution. <bookmark mark='c'/> Instead we sample "
            "B of them: Part 7's Monte Carlo, with error shrinking like one over root B. There are now two errors: the "
            "sampling error, from having one sample, which no amount of computing removes; and the Monte Carlo error, from "
            "finite B, which we can make as small as we like. <bookmark mark='d'/> A thousand resamples give a standard error to "
            "within a few percent. Interval endpoints sit in the tails, where draws are scarce, and need a few thousand."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def assumes(self):
        rows = fit_rows(VGroup(
            label(r"the bootstrap assumes:", font_size=26),
            label(r"the observations are independent draws from one $F$: \ resample what was sampled", font_size=24, color=BOOT),
            label(r"$\hat F_n$ is close to $F$ in the ways the statistic cares about: \ $n$ not tiny", font_size=24, color=BOOT),
            label(r"the statistic depends smoothly on $F$: \ means, \ correlations, \ yes; \ maxima, \ no", font_size=24, color=RES),
            label(r"no normality, \ no formula: \ that's the gift", font_size=26, color=OBS),
        ), 12.4, 0.46, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What does the bootstrap assume? <bookmark mark='b'/> That the observations are independent "
            "draws from one distribution: you must resample in the way the data were sampled. Pairs stay pairs, as the law "
            "schools' LSAT and GPA did; clusters are resampled as clusters; time series need blocks, which is Part 17. "
            "<bookmark mark='c'/> That the empirical distribution is close to the real one, which needs a reasonable sample. "
            "<bookmark mark='d'/> And that the statistic depends smoothly on the distribution. Means and correlations do. A "
            "maximum doesn't, and chapter nine shows what happens then. <bookmark mark='e'/> What it doesn't assume is the gift: "
            "no normality, and no formula for the standard error."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
