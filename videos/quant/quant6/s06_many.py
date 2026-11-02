from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load, real_data


class Many(VoiceoverScene):
    def construct(self):
        sh = load("shrinkage")
        m = load("multiple")
        self.card()
        self.shrink(sh)
        self.multiple(m)

    def card(self):
        c = chapter_card(5, r"Many assets, many tests", r"What do you learn from 49 estimates at once?", part=PART)
        with self.voiceover("Chapter five. Many assets, many tests."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def shrink(self, sh):
        raw, later, shr = (np.asarray(sh[k]) for k in ("raw", "later", "shrunk"))
        n = len(raw)
        g = axes([-0.02, 0.22], [0, 1], x_length=8.4, y_length=3.6, xlabel=r"mean excess return a year", yticks=[],
                 xticks=[0, 0.05, 0.10, 0.15, 0.20], xfmt=lambda u: f"{100 * u:.0f}\\%", font_size=18)
        g.to_edge(UP, buff=0.9).to_edge(LEFT, buff=2.8)
        ax = g.ax
        y0, y1 = 0.8, 0.2
        top = VGroup(*[Dot(ax.c2p(v, y0), radius=0.05, color=DATA_C) for v in raw])
        bot = VGroup(*[Dot(ax.c2p(v, y1), radius=0.05, color=GOOD) for v in later])
        links = VGroup(*[Line(ax.c2p(a, y0), ax.c2p(b, y1), stroke_width=1, color=GREY_C).set_stroke(opacity=0.6)
                         for a, b in zip(raw, later)])
        lt = label(r"estimated, 1927--1973", font_size=20, color=DATA_C).next_to(ax.c2p(-0.02, y0), LEFT, buff=0.1)
        lb = label(r"realized, 1974--2020", font_size=20, color=GOOD).next_to(ax.c2p(-0.02, y1), LEFT, buff=0.1)
        grand = DashedLine(ax.c2p(sh["grand"], 0), ax.c2p(sh["grand"], 1), color=EST, stroke_width=2.5)
        res = VGroup(
            MathTex(rf"\text{{error of the raw means: }} {1e4 * sh['mse_raw']:.1f}", font_size=30, color=DATA_C),
            MathTex(rf"\text{{error of the shrunk means: }} {1e4 * sh['mse_shrunk']:.1f}", font_size=30, color=EST),
            label(r"mean squared error, in squared percent a year", font_size=19, color=GREY_B),
            wrapped_label(r"the data's best estimate of the spread between industries' true means was zero: every "
                          r"estimate is shrunk all the way to the grand mean, and the forecasts are twice as accurate. "
                          r"James and Stein (1961): with three or more means, shrinking always helps on average.", 11.6,
                          21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"Take {n} of French's industries and estimate each one's average excess return from the first half of "
            "the data, 1927 to 1973. The estimates spread from five to fifteen percent a year. "
            "<bookmark mark='a'/> Now look at what each industry actually earned in the second half. The ranks "
            "scramble: the lines cross every which way. <bookmark mark='b'/> Shrinkage pulls each estimate toward "
            "the average of all of them, by an amount set by how noisy each estimate is relative to how different "
            "the industries really seem to be. Here the data say the true differences are too small to detect, so "
            "every estimate goes all the way to the grand mean, and that single number forecasts the second half "
            "twice as well as the forty separate estimates. <bookmark mark='c'/> Charles Stein proved in 1956 that "
            "when you estimate three or more means at once, shrinking them together always helps on average. A prior "
            "is not a bias to be ashamed of; it is how you borrow strength across assets."
        ) as vo:
            self.play(FadeIn(g), FadeIn(top), FadeIn(lt))
            vo.wait_until("a")
            self.play(Create(links), FadeIn(bot), FadeIn(lb), run_time=2)
            vo.wait_until("b")
            self.play(Create(grand), *[d.animate.move_to(ax.c2p(v, y0)) for d, v in zip(top, shr)], run_time=2)
            self.play(FadeIn(res[0]), FadeIn(res[1]), FadeIn(res[2]))
            vo.wait_until("c")
            self.play(FadeIn(res[3]))
        self.wait(0.4)
        self.clear_scene()

    def multiple(self, m):
        p = np.sort(np.asarray(m["p"]))
        k = np.arange(1, len(p) + 1)
        lp = np.log10(np.maximum(p, 1e-3))
        g = axes([0, len(p) + 1], [-3, 0], x_length=7.0, y_length=4.4, xlabel=r"industries, sorted by $p$-value",
                 ylabel=r"$p$-value of the CAPM alpha (log scale)", xticks=[1, 10, 20, 30, 40, 49],
                 yticks=[-3, -2, np.log10(0.05), 0], yfmt=lambda u: {-3: "0.001", -2: "0.01", 0: "1"}.get(round(u), "0.05"),
                 font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(i, v), radius=0.06, color=GOOD if pv < 0.05 else DATA_C) for i, v, pv in zip(k, lp, p)])
        five = DashedLine(ax.c2p(0, np.log10(0.05)), ax.c2p(len(p) + 1, np.log10(0.05)), color=BAD, stroke_width=2)
        kk = np.arange(1, len(p) + 1)
        bh = curve(ax, kk, np.log10(0.05 * kk / len(p)), ALT, stroke_width=2.5)
        bonf = DashedLine(ax.c2p(0, np.log10(0.05 / len(p))), ax.c2p(len(p) + 1, np.log10(0.05 / len(p))), color=BAD,
                          stroke_width=1.5)
        side = VGroup(
            label(r"49 industries, 1926--2020, Newey--West $t$", font_size=21, color=GREY_A),
            MathTex(rf"p < 0.05: \ {m['n_raw']}", font_size=32, color=GOOD),
            MathTex(rf"\text{{Bonferroni, Holm: }} {m['n_bonf']}, {m['n_holm']}", font_size=30, color=BAD),
            MathTex(rf"\text{{Benjamini--Hochberg (FDR 5\%): }} {m['n_bh']}", font_size=30, color=ALT),
            label(rf"1{{,}}000 pure-noise strategies: {m['noise_raw']} pass at 5\%, {m['noise_bh']} after BH", font_size=20,
                  color=GREY_B),
            wrapped_label(r"family-wise error: the chance of even one false discovery; false discovery rate: the share of "
                          r"discoveries that are false (Benjamini and Hochberg 1995). Part 25 applies them to the "
                          r"factor zoo.", 4.6, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Now test all forty-nine industries for an alpha against the market. Sort the p-values. "
            f"<bookmark mark='a'/> {m['n_raw']} of them are below five percent: tobacco, drugs, medical equipment and "
            "food with positive alphas, steel with a negative one. But test "
            "forty-nine things and you expect two or three to pass by luck alone. <bookmark mark='b'/> The Bonferroni "
            "correction divides the threshold by the number of tests, controlling the chance of even one false "
            "discovery; Holm's version is a little less strict. Benjamini and Hochberg's rule, from 1995, controls "
            "the share of discoveries that are false instead, and is far more forgiving. <bookmark mark='c'/> None of "
            "the forty-nine survives any of them. Simulate a thousand strategies of pure noise and about fifty pass "
            "at five percent, as they should; none survives Benjamini-Hochberg. Every new signal the House tests "
            "will be judged against the count of everything it has tried. Part twenty-five does this for the four "
            "hundred published factors."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.03))
            vo.wait_until("a")
            self.play(Create(five), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(bonf), Create(bh), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()
