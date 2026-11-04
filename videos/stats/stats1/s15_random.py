from __future__ import annotations

import numpy as np

from videos.stats.stats1.common import *  # noqa: F403


class Random(VoiceoverScene):
    def construct(self):
        self.card()
        self.machine()
        self.multiples()
        self.many()

    def card(self):
        card = chapter_card(14, r"The sample is random", r"Draw again, and every summary changes", lit=(),
                            part=PART)
        with self.voiceover("Chapter fourteen. The sample is random."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def machine(self):
        d = load("sampling")
        w = load("world")
        pop = np.repeat(np.asarray(w["height_hist_edges"])[:-1] + 0.5,
                        np.round(np.asarray(w["height_hist"]) * 20000).astype(int))
        m = SamplingMachine(pop, value_range=(140, 205), stat_range=(165.5, 173.5), bins=32, n_dots=800,
                            value_label=r"heights in this sample (cm)", stat_label=r"the sample's mean (cm)",
                            ticks=[150, 170, 190], stat_ticks=[166, 168, 170, 172], max_count=8)
        mu = d["mu"]
        tl = Line(m.hist_ax[0].c2p(mu, 0), m.hist_ax[0].c2p(mu, 0.92), color=S.TRUTH, stroke_width=3)
        tlab = MathTex(rf"\mu = {mu:.2f}", font_size=30, color=S.TRUTH).next_to(tl, UP, buff=0.08)
        tag = simulated_tag(r"simulated: samples of 100 adults from the World")
        samples = np.asarray(d["samples"])
        means = d["means"]
        with self.voiceover(
            "We've been treating each sample as if it were the data. It is only one of many samples we might have "
            "drawn. <bookmark mark='a'/> Here is the World's population, and a machine that draws a hundred "
            "adults at random. <bookmark mark='b'/> One sample: its hundred heights land on the line above, and "
            f"its average, {means[0]:.2f}, drops into the chart below. <bookmark mark='c'/> Another hundred: "
            f"{means[1]:.2f}. <bookmark mark='d'/> Another: {means[2]:.2f}. Every sample gives a different average, "
            "and none of them is exactly the truth. <bookmark mark='e'/> The truth is the gold line, the mean of "
            f"all {money(w['n_adults'])} adults, {mu:.2f}. The averages scatter around it."
        ) as vo:
            self.play(FadeIn(m), FadeIn(tag))
            vo.wait_until("b")
            m.draw(self, samples[0], means[0], run_time=3.0, stat_tex=rf"$\bar x = {means[0]:.2f}$")
            vo.wait_until("c")
            m.draw(self, samples[1], means[1], run_time=2.6, stat_tex=rf"$\bar x = {means[1]:.2f}$")
            vo.wait_until("d")
            m.draw(self, samples[2], means[2], run_time=2.4, stat_tex=rf"$\bar x = {means[2]:.2f}$")
            vo.wait_until("e")
            self.play(Create(tl), FadeIn(tlab))
        with self.voiceover(
            "Keep going. <bookmark mark='a'/> Seventeen more samples, each dropping its average into the chart."
        ) as vo:
            vo.wait_until("a")
            for k in range(3, 20):
                m.draw(self, samples[k], means[k], run_time=0.9)
        self.m, self.tl, self.tlab, self.tag = m, tl, tlab, tag

    def multiples(self):
        d = load("sampling")
        edges = np.asarray(d["edges"])
        hists = np.asarray(d["hists"])
        grid = VGroup()
        top = hists.max()
        for k in range(20):
            box = Rectangle(width=2.3, height=1.35, stroke_color=GREY_D, stroke_width=1)
            bars = VGroup()
            bw = 2.1 / len(hists[k])
            for j, c in enumerate(hists[k]):
                if c == 0:
                    continue
                h = 1.0 * c / top
                bars.add(Rectangle(width=bw, height=h, stroke_width=0, fill_color=S.EST, fill_opacity=0.8)
                         .move_to(box.get_corner(DL) + np.array([0.1 + (j + 0.5) * bw, 0.12 + h / 2, 0])))
            mean = MathTex(rf"{d['means'][k]:.1f}", font_size=20, color=S.EST).move_to(box.get_corner(UR) + [-0.3, -0.18, 0])
            grid.add(VGroup(box, bars, mean))
        grid.arrange_in_grid(4, 5, buff=(0.25, 0.25)).move_to(DOWN * 0.2)
        head = label(r"twenty samples of 100 heights", font_size=30, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "It's not only the average that jumps. <bookmark mark='a'/> Here are the histograms of those twenty "
            "samples, side by side. Each was drawn from the same population by the same procedure. "
            "<bookmark mark='b'/> Their shapes differ: one looks lopsided, another has two peaks, another a gap. "
            "Their medians, standard deviations, skewness, correlations, everything we've computed in this part, "
            "would all differ from sample to sample. <bookmark mark='c'/> Every summary of a sample is a random "
            "quantity. To say how far to trust one, we need to know how it varies."
        ) as vo:
            self.play(FadeOut(self.m), FadeOut(self.tl), FadeOut(self.tlab))
            self.play(FadeIn(head), LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in grid], lag_ratio=0.08),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Indicate(g[1], color=S.EST, scale_factor=1.05) for g in grid], lag_ratio=0.06),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(*[Indicate(g[2], color=S.ACCENT, scale_factor=1.3) for g in grid])
        self.clear_scene(self.tag)

    def many(self):
        d = load("sampling")
        many = np.asarray(d["many"])
        mu, sd, se = d["mu"], d["sd_means"], d["se_formula"]
        A = axes([165.5, 173.5], [0, 0.6], x_length=7.8, y_length=4.4, xlabel=r"the mean of a sample of 100 (cm)",
                 xticks=[166, 168, 170, 172], center=[-2.7, -0.4, 0])
        A.ax.y_axis.set_opacity(0.3)
        ax = A.ax
        edges = np.linspace(165.5, 173.5, 49)
        counts = np.histogram(many, edges)[0]
        stages = [100, 400, 2000]
        hists = [hist_bars(ax, edges, np.histogram(many[:k], edges)[0] / (k * np.diff(edges)), color=S.EST,
                           opacity=0.8) for k in stages]
        cnt = [label(rf"{fmt_int(k)} samples", font_size=28, color=S.EST).to_corner(UL, buff=0.5) for k in stages]
        tl = Line(ax.c2p(mu, 0), ax.c2p(mu, 0.6), color=S.TRUTH, stroke_width=4)
        tlab = MathTex(rf"\mu = {mu:.2f}", font_size=30, color=S.TRUTH).next_to(tl, UP, buff=0.08)
        sd_brace = BraceBetweenPoints(ax.c2p(mu - sd, 0.33), ax.c2p(mu + sd, 0.33), direction=UP, color=S.ACCENT)
        facts = VGroup(
            MathTex(rf"\text{{SD of the 2{{,}}000 means}} = {sd:.3f}", font_size=32, color=S.ACCENT),
            MathTex(rf"\frac{{\sigma}}{{\sqrt{{n}}}} = \frac{{{d['sigma']:.2f}}}{{\sqrt{{100}}}} = {se:.3f}",
                    font_size=32, color=S.TRUTH),
            label(r"why $\sqrt n$: \ Parts 6 and 8", font_size=24, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.7).shift(UP * 0.9)
        dfn = definition_card(r"Sampling distribution", r"the distribution of a statistic over all the samples "
                              r"we might have drawn; \ its SD is the statistic's standard error", color=S.EST,
                              width=4.3, font_size=21).to_edge(RIGHT, buff=0.6).shift(DOWN * 2.3)
        _ = counts
        with self.voiceover(
            "So let's find out. <bookmark mark='a'/> Draw not twenty samples but two thousand, and keep every "
            "average. <bookmark mark='b'/> As they pile up, a shape emerges: a smooth bell, centred on the truth. "
            "This is the sampling distribution of the mean: the distribution of the averages of all the samples we "
            "might have drawn. <bookmark mark='c'/> Its spread is much narrower than the population's. Heights vary "
            f"by about {d['sigma']:.1f} centimetres from person to person, but the averages of a hundred people vary "
            f"by only {sd:.2f}. <bookmark mark='d'/> And that number isn't arbitrary. It's almost exactly the "
            f"population's standard deviation divided by the square root of the sample size, {se:.3f}. Why the "
            "square root, and why a bell even when the population isn't one, are two of the great theorems of "
            "probability, the law of large numbers and the central limit theorem, and Part 6 proves them. "
            "<bookmark mark='e'/> This picture, the sampling distribution, is the central object of statistics. "
            "It's how we will measure how often we're wrong. And to reason about it, we need the language of chance."
        ) as vo:
            self.play(FadeIn(A), Create(tl), FadeIn(tlab))
            vo.wait_until("a")
            self.play(FadeIn(hists[0]), FadeIn(cnt[0]))
            vo.wait_until("b")
            for i in range(1, len(stages)):
                self.play(Transform(hists[0], hists[i]), Transform(cnt[0], cnt[i]), run_time=1.5)
            self.play(FadeIn(dfn, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(GrowFromCenter(sd_brace), FadeIn(facts[0]))
            vo.wait_until("d")
            self.play(FadeIn(facts[1]), FadeIn(facts[2]))
            vo.wait_until("e")
            self.play(Indicate(hists[0], color=S.EST, scale_factor=1.03))
        self.clear_scene()
