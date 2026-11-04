from __future__ import annotations

import numpy as np

from videos.stats.stats1.common import *  # noqa: F403


class Pictures(VoiceoverScene):
    def construct(self):
        self.card()
        self.dots()
        self.to_histogram()
        self.density()
        self.width_sweep()
        self.rules()

    def card(self):
        card = chapter_card(3, r"Pictures first", r"Before any formula: what does the data look like?",
                            lit=(1786,), part=PART)
        with self.voiceover("Chapter three. Pictures first."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def dots(self):
        d = load("heights")
        A = axes([140, 205], [0, 1], x_length=11.0, y_length=4.0, xlabel=r"height (cm)",
                 xticks=[140, 150, 160, 170, 180, 190, 200], center=[0, -0.6, 0])
        A.ax.y_axis.set_opacity(0)
        dp = dot_plot(A.ax, d["dots"], step=1.0, radius=0.075, color=S.DATA)
        order = np.argsort(np.random.Generator(np.random.PCG64(2)).random(len(dp)))
        tag = simulated_tag(r"simulated: 60 adults drawn from the World")
        title = label(r"one dot, one person", font_size=32, color=GREY_A).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Before any formula, look. Tukey, who did more than anyone to make statisticians look at their data, "
            "put it this way: the greatest value of a picture is when it forces us to notice what we never "
            "expected to see. <bookmark mark='a'/> Here are sixty adults from the World, drawn at random, each "
            "placed at their height, rounded to the nearest centimetre. Where two people share a height they "
            "stack. <bookmark mark='b'/> Already you can see things: a crowd in the middle, thinning out to either "
            "side; nobody below about one hundred and fifty, almost nobody above one hundred and ninety. This is a "
            "dot plot, and for a few dozen numbers it's the most honest picture there is: nothing is hidden, "
            "nothing is averaged away."
        ) as vo:
            tukey = history_card(1977, r"John W. Tukey, \emph{Exploratory Data Analysis}",
                                 r"``The greatest value of a picture is when it forces us to notice what we never "
                                 r"expected to see.''", color=S.MUSEUM, width=6.4, font_size=24).move_to([0, 1.5, 0])
            self.play(FadeIn(A), FadeIn(tag), FadeIn(tukey, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(tukey), FadeIn(title))
            self.play(LaggedStart(*[FadeIn(dp[i], shift=DOWN * 0.6) for i in order], lag_ratio=0.05), run_time=4.0)
            vo.wait_until("b")
            self.play(Indicate(dp, color=S.EST, scale_factor=1.05))
        self.A, self.dp, self.tag, self.title = A, dp, tag, title

    def to_histogram(self):
        d = load("heights")
        x = np.asarray(d["x"])
        ax = self.A.ax
        edges = np.arange(140, 206, 5.0)
        x60 = np.asarray(d["dots"])
        counts60 = np.histogram(x60, edges)[0]
        B = axes([140, 205], [0, 70], x_length=11.0, y_length=4.0, xlabel=r"height (cm)", ylabel=r"count",
                 xticks=[140, 150, 160, 170, 180, 190, 200], yticks=[0, 20, 40, 60], center=[0, -0.6, 0])
        bx = B.ax
        h60 = hist_bars(bx, edges, counts60, color=S.EST, opacity=0.75)
        counts = np.histogram(x, edges)[0]
        h200 = hist_bars(bx, edges, counts, color=S.EST, opacity=0.75)
        lab = label(r"60 people, \ bins 5 cm wide", font_size=28, color=GREY_A).to_edge(UP, buff=0.6)
        lab2 = label(rf"all {d['n']} in the sample", font_size=28, color=GREY_A).to_edge(UP, buff=0.6)
        tag2 = simulated_tag(rf"simulated: a sample of {d['n']} World adults")
        with self.voiceover(
            "With more data, dots pile into towers too tall to read, so we group them. <bookmark mark='a'/> Cut "
            "the line into bins five centimetres wide, and replace each bin's dots by a bar as tall as their count. "
            "<bookmark mark='b'/> That's a histogram: the oldest picture of a distribution, named in the 1890s by "
            f"Karl Pearson. <bookmark mark='c'/> Here's the whole sample of {d['n']}. The shape is clearer now: one "
            "peak, roughly symmetric, falling away on both sides. But we made a choice to get this picture, the "
            "width of the bins, and that choice is not innocent."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(self.title), FadeIn(lab), FadeIn(B), FadeOut(self.A))
            # each bin's dots collapse into its bar
            anims = []
            for k in range(len(edges) - 1):
                inbin = [i for i, v in enumerate(np.round(x60)) if edges[k] <= v < edges[k + 1]]
                if not inbin:
                    continue
                anims.append(ReplacementTransform(VGroup(*[self.dp[i] for i in inbin]), h60[k]))
            leftover = [i for i, v in enumerate(np.round(x60)) if not (edges[0] <= v < edges[-1])]
            self.play(*anims, *[FadeOut(self.dp[i]) for i in leftover], run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(h60, color=S.EST, scale_factor=1.03))
            vo.wait_until("c")
            self.play(Transform(h60, h200), FadeOut(lab), FadeIn(lab2), Transform(self.tag, tag2), run_time=1.6)
        self.play(FadeOut(VGroup(B, h60, lab2)))

    def density(self):
        d = load("heights")
        x = np.asarray(d["x"])
        A = axes([140, 205], [0, 0.09], x_length=11.0, y_length=4.0, xlabel=r"height (cm)",
                 ylabel=r"density \ (proportion per cm)", xticks=[140, 150, 160, 170, 180, 190, 200],
                 yticks=[0, 0.03, 0.06, 0.09], yfmt=lambda v: f"{v:.2f}", center=[0, -0.6, 0])
        ax = A.ax
        edges = np.arange(140, 206, 5.0)
        hb = histogram(ax, x, edges, density=True, color=S.EST)
        k = int(np.argmax(hb.counts))
        area = hb[k].copy().set_fill(S.ACCENT, opacity=0.9)
        eq = cmath(r"\text{height}", r"=", r"\frac{\text{proportion in the bin}}{\text{bin width}}", font_size=36)
        eq.to_edge(UP, buff=0.4)
        frac = hb.counts[k] / len(x)
        ann = label(rf"area $= {frac:.3f}$: \ {hb.counts[k]} of {len(x)}", font_size=26, color=S.ACCENT)
        ann.next_to(hb[k], UP, buff=0.15)
        with self.voiceover(
            "First, a better vertical scale. <bookmark mark='a'/> Instead of counts, make each bar's height the "
            "proportion of the data in the bin divided by the bin's width. <bookmark mark='b'/> Then a bar's area "
            f"is its proportion: this bar holds {hb.counts[k]} of the {len(x)} people, a proportion of "
            f"{frac:.3f}, and that's its area. The areas of all the bars add up to one. <bookmark mark='c'/> This is "
            "the density scale, and it makes histograms with different bins, or different sample sizes, "
            "comparable. It's also the first glimpse of an idea that runs through the whole series: probability "
            "as area."
        ) as vo:
            self.play(FadeIn(A), FadeIn(hb))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(area), FadeIn(ann))
            vo.wait_until("c")
            self.play(FadeOut(area), FadeOut(ann))
        self.play(FadeOut(eq), FadeOut(hb))
        self.D = A

    def width_sweep(self):
        d = load("heights")
        x = np.asarray(d["x"])
        ax = self.D.ax
        h = ValueTracker(5.0)

        def make():
            w = h.get_value()
            edges = np.arange(140, 205 + w, w)
            return histogram(ax, x, edges, density=True, color=S.EST, stroke_width=0.6)

        hist = always_redraw(make)
        read = always_redraw(lambda: MathTex(rf"\text{{bin width}} = {h.get_value():.1f}\ \text{{cm}}",
                                             font_size=36, color=S.ACCENT).to_corner(UL, buff=0.5))
        with self.voiceover(
            "Now let the bin width move. <bookmark mark='a'/> At one centimetre, the histogram is all spikes. Every "
            "accident of who happened to be sampled shows up as a tower or a gap, and you can't see the shape for "
            "the noise. <bookmark mark='b'/> At fifteen centimetres it's a few crude blocks: the noise is gone, and so "
            "is the shape. <bookmark mark='c'/> Somewhere between is a width that shows the distribution rather "
            "than the sample, or the bins. <bookmark mark='d'/> The same two hundred numbers, three different "
            "stories. This is a trade-off between variance and bias: narrow bins follow the noise; wide bins blur "
            "the truth. It's the first appearance of the most important trade-off in statistics, and Part 29 will "
            "solve it exactly."
        ) as vo:
            self.add(hist, read)
            vo.wait_until("a")
            self.play(h.animate.set_value(1.0), run_time=2.5)
            vo.wait_until("b")
            self.play(h.animate.set_value(15.0), run_time=3.0)
            vo.wait_until("c")
            self.play(h.animate.set_value(6.0), run_time=2.0)
            vo.wait_until("d")
            for v in (1.5, 15.0, 6.0):
                self.play(h.animate.set_value(v), run_time=1.2)
        self.hist, self.read, self.h = hist, read, h

    def rules(self):
        d = load("heights")
        ax = self.D.ax
        n = d["n"]
        rows = VGroup(
            VGroup(label(r"Sturges (1926)", font_size=24, color=GREY_A),
                   MathTex(rf"k = \lceil \log_2 n \rceil + 1 = {d['k_sturges']}\ \text{{bins}}", font_size=30),
                   MathTex(rf"h = {d['h_sturges']:.2f}", font_size=30, color=S.ACCENT)),
            VGroup(label(r"Scott (1979)", font_size=24, color=GREY_A),
                   MathTex(r"h = 3.49\, s\, n^{-1/3}", font_size=30),
                   MathTex(rf"h = {d['h_scott']:.2f}", font_size=30, color=S.ACCENT)),
            VGroup(label(r"Freedman--Diaconis (1981)", font_size=24, color=GREY_A),
                   MathTex(r"h = 2\, \mathrm{IQR}\, n^{-1/3}", font_size=30),
                   MathTex(rf"h = {d['h_fd']:.2f}", font_size=30, color=S.ACCENT)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.4)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        card = VGroup(label(rf"rules of thumb, \ $n = {n}$", font_size=26), rows).arrange(DOWN, aligned_edge=LEFT,
                                                                                        buff=0.25)
        bg = BackgroundRectangle(card, color=BACKGROUND, fill_opacity=0.9, buff=0.2)
        cardg = VGroup(bg, card).scale(0.8).to_corner(UR, buff=0.25)
        pop = curve(ax, d["grid"], d["pop_density"], S.TRUTH, 4, smooth=True)
        plab = label(r"the population", font_size=26, color=S.TRUTH).next_to(ax.c2p(186, 0.03), UP, buff=0.1)
        why_n = label(r"why $n^{-1/3}$? \ Part 29", font_size=24, color=GREY_B).next_to(cardg, DOWN, buff=0.15)
        with self.voiceover(
            "There are rules of thumb for the width. <bookmark mark='a'/> Sturges, in 1926, chose the number of bins "
            f"as the logarithm of n to base two, plus one: {d['k_sturges']} bins here, each about "
            f"{d['h_sturges']:.1f} centimetres. <bookmark mark='b'/> Scott, in 1979, and Freedman and Diaconis, two "
            "years later, derived widths from the data's spread, its standard deviation or its interquartile range, "
            f"times n to the minus one third: {d['h_scott']:.1f} and {d['h_fd']:.1f} centimetres. That curious "
            "power, minus one third, comes from balancing the two kinds of error, and we'll derive it. "
            "<bookmark mark='c'/> And because this sample came from the World, we can do what's impossible in "
            "real life: lay the population itself over the picture. Here it is in gold. The histogram of two hundred "
            "people is an estimate of this curve, and you can see both how good it is and where chance pushed it "
            "around."
        ) as vo:
            self.play(FadeIn(bg), FadeIn(card[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            self.play(self.h.animate.set_value(d["h_fd"]), FadeIn(why_n), run_time=1.0)
            vo.wait_until("c")
            self.play(Create(pop), FadeIn(plab), run_time=2.5)
        self.hist.clear_updaters()
        self.read.clear_updaters()
        self.clear_scene()
