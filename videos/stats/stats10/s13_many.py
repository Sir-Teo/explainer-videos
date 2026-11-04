from __future__ import annotations

import numpy as np

from videos.stats.stats10.common import *  # noqa: F403


class Many(VoiceoverScene):
    def construct(self):
        self.card()
        self.any_curve()
        self.hundred()
        self.bonferroni()
        self.salmon()
        self.forking()

    def card(self):
        card = chapter_card(12, r"Many tests", r"Test enough things, \ and something will be significant", lit=(1995,), part=PART)
        with self.voiceover("Chapter twelve. Many tests."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def any_curve(self):
        d = load("many")
        ms = np.arange(1, 101)
        A = axes([0, 100], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"number of true nulls tested, \ $m$",
                 ylabel=r"P(at least one $p < 0.05$)", xticks=[1, 20, 50, 100], yticks=[0, 0.05, 0.5, 0.64, 1], center=[-2.0, -0.3, 0])
        ax = A.ax
        cv = polyline(ax, ms, 1 - 0.95 ** ms, REJ, 3.5)
        g20 = VGroup(DashedLine(ax.c2p(20, 0), ax.c2p(20, d["any"]["20"]), color=GREY_B, stroke_width=1.5),
                     DashedLine(ax.c2p(0, d["any"]["20"]), ax.c2p(20, d["any"]["20"]), color=GREY_B, stroke_width=1.5),
                     Dot(ax.c2p(20, d["any"]["20"]), radius=0.08, color=OBS))
        rows = fit_rows(VGroup(
            MathTex(r"P(\text{any}) = 1 - (1 - \alpha)^m", font_size=32),
            MathTex(rf"m = 5:\ {d['any']['5']:.2f},\quad m = 20:\ {d['any']['20']:.2f},\quad m = 100:\ {d['any']['100']:.3f}", font_size=26,
                    color=OBS),
            label(rf"simulated, \ 20 independent tests: \ {100 * d['sim20_any']:.1f}\%", font_size=24, color=GREY_A),
            label(r"the family-wise error rate", font_size=24, color=GREY_A),
        ), 5.2, 0.34, [4.3, -0.3, 0])
        with self.voiceover(
            "Every test so far was a single test. Real studies run many. <bookmark mark='a'/> If you test m hypotheses "
            "that are all truly null, each at five percent, and independently, the chance that at least one comes out "
            "significant is one minus point nine five to the m. <bookmark mark='b'/> With five tests it's twenty-three "
            "percent. With twenty, sixty-four percent: more likely than not. With a hundred, it's a near certainty. "
            "<bookmark mark='c'/> Simulation agrees. The probability of at least one false alarm across the whole "
            "family is called the family-wise error rate, and a study measuring twenty outcomes, at five percent each, "
            "has a family-wise error rate of almost two in three."
        ) as vo:
            self.play(FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(cv))
            vo.wait_until("b")
            self.play(Create(g20), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def hundred(self):
        d = load("many")
        p = np.asarray(d["p100"])
        nl = NumberLine(x_range=[0, 1, 0.1], length=12.0, include_numbers=False, color=GREY_C).move_to([0, 0.6, 0])
        ticks = VGroup(*[MathTex(f"{v:g}", font_size=20, color=GREY_B).next_to(nl.n2p(v), DOWN, buff=0.15) for v in (0, 0.05, 0.25, 0.5, 0.75, 1)])
        dots = VGroup(*[Dot(nl.n2p(v) + UP * (0.25 + 0.18 * (i % 6)), radius=0.06, color=REJ if v < 0.05 else NULLC) for i, v in enumerate(p)])
        cut = DashedLine(nl.n2p(0.05) + DOWN * 0.1, nl.n2p(0.05) + UP * 1.6, color=REJ, stroke_width=2)
        bon = DashedLine(nl.n2p(0.0005) + DOWN * 0.1, nl.n2p(0.0005) + UP * 1.6, color=OBS, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"100 true nulls: \ their $p$-values are 100 uniform random numbers", font_size=26),
            label(rf"{d['n_sig']} fall below 0.05: \ three ``discoveries'', \ all false", font_size=26, color=REJ),
            label(rf"below $0.05/100 = 0.0005$: \ {d['n_bonf']}", font_size=26, color=OBS),
        ), 12.6, 0.34, [0, -1.7, 0])
        tag = simulated_tag(r"simulated", corner=UR)
        with self.voiceover(
            "<bookmark mark='a'/> Here are a hundred tests in which every null is true. By chapter three, their "
            "p-values are a hundred uniform random numbers, scattered across zero to one. <bookmark mark='b'/> Three of "
            "them happen to fall below point zero five. Report those three, and you have three discoveries, every one of "
            "them false. <bookmark mark='c'/> Move the line to point zero zero zero five, the five percent divided by a "
            "hundred, and none survive."
        ) as vo:
            self.play(Create(nl), FadeIn(ticks), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dt, scale=0.5) for dt in dots], lag_ratio=0.02), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(cut), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(bon), FadeIn(rows[2]))
        self.clear_scene()

    def bonferroni(self):
        d = load("many")
        rows = [
            cmath(r"P\Big(\bigcup_{i=1}^m \{p_i \le \alpha/m\}\Big)", r"\le", r"\sum_{i=1}^m P\big(p_i \le \alpha/m\big)", font_size=32),
            cmath(r"\vphantom{x}", r"\le", r"m \cdot \frac{\alpha}{m} = \alpha", font_size=32),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"the union bound (Part 2)"), why(r"each $p_i$ is (super-)uniform: \ any dependence at all")]
        foot = fit_rows(VGroup(
            label(rf"20 tests at $0.05/20$: \ the family-wise error rate falls from {100 * d['sim20_any']:.0f}\% to {100 * d['sim20_bonf']:.1f}\%",
                  font_size=26, color=OBS),
            label(r"the price: \ power. \ $0.05/20 = 0.0025$ needs $|z| > 3.02$ instead of $1.96$", font_size=24),
            label(r"Holm (1979) is uniformly better; \ false discovery rates (Benjamini \& Hochberg, 1995) ask for less: \ Part 33",
                  font_size=24, color=GREY_A),
        ), 12.6, 0.32, [0, -1.7, 0])
        with self.voiceover(
            "That's the Bonferroni correction, named for Carlo Bonferroni's inequality. <bookmark mark='a'/> The "
            "chance that any of m p-values falls below alpha over m is at most the sum of the individual chances, by "
            "the union bound of Part 2. <bookmark mark='b'/> Each of those is at most alpha over m, so the total is at "
            "most alpha, whatever the dependence between the tests. <bookmark mark='c'/> With twenty tests, the "
            "family-wise error rate drops from sixty-four percent to five. <bookmark mark='d'/> The price is power: each "
            "test now needs a z of three instead of two. <bookmark mark='e'/> Sture Holm's 1979 step-down version is "
            "uniformly better, and Yoav Benjamini and Yosef Hochberg's false discovery rate, in 1995, asks for less, "
            "controlling the share of discoveries that are false rather than the chance of any. That's Part 33."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.6, x=0.2, buff=0.8, edge=6.9)
            for k, m_ in enumerate("ab"):
                vo.wait_until(m_)
                step(k, transform=False)
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def salmon(self):
        hc = history_card(2009, r"C. Bennett, \ A. Baird, \ M. Miller \& G. Wolford", r"a dead Atlantic salmon in an fMRI scanner, \ ``shown'' "
                          r"photographs of people in social situations: \ uncorrected, \ a cluster of voxels in its brain ``responds''",
                          color=REJ, width=9.4, font_size=24).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"a brain scan runs a test at each of over 100,000 voxels", font_size=24),
            label(r"with correction for multiple comparisons, \ the salmon's activity disappears", font_size=26, color=OBS),
            label(r"the poster won an Ig Nobel prize (2012), \ and changed how neuroimaging papers were reviewed", font_size=22, color=GREY_A),
        ), 12.6, 0.3, [0, -1.8, 0])
        with self.voiceover(
            "The most memorable demonstration came from neuroscience. <bookmark mark='a'/> In 2009, Craig Bennett and "
            "his colleagues put a dead Atlantic salmon in an MRI scanner, showed it photographs of people in social "
            "situations, and asked it to judge their emotions. Analysed without correcting for multiple comparisons, a "
            "small cluster of voxels in the salmon's brain lit up. <bookmark mark='b'/> A brain scan runs a separate test "
            "at every one of more than a hundred thousand voxels, and some will be significant by chance. "
            "<bookmark mark='c'/> With a correction, the dead fish's thoughts vanished. <bookmark mark='d'/> The poster "
            "won an Ig Nobel prize, and helped make multiple-comparison corrections standard in the field."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def forking(self):
        rows = fit_rows(VGroup(
            label(r"the garden of forking paths", font_size=32, color=OBS),
            label(r"the tests need not be run: \ choosing among outcomes, \ subgroups, \ covariates \ and exclusions after seeing the data",
                  font_size=24),
            label(r"multiplies them invisibly \ (Gelman \& Loken, 2013; \ Simmons, Nelson \& Simonsohn, 2011: \ ``false-positive psychology'')",
                  font_size=24, color=GREY_A),
            label(r"remedies: \ preregistration; \ correction for the tests actually considered; \ selective inference (Part 56)",
                  font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> There's a quieter version of the problem that Andrew Gelman and Eric Loken called the "
            "garden of forking paths. <bookmark mark='b'/> The extra tests don't have to be run. If the choice of "
            "outcome, subgroup, covariates or exclusions is made after looking at the data, the analysis that gets "
            "reported is one of many that could have been, and the p-value is computed as if it were the only one. "
            "<bookmark mark='c'/> In 2011 Joseph Simmons, Leif Nelson and Uri Simonsohn showed that a few such "
            "innocent-looking choices can push the false-positive rate above fifty percent. <bookmark mark='d'/> The "
            "remedies are deciding the analysis in advance, correcting for every test actually considered, and the "
            "theory of inference after selection, Part 56."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
