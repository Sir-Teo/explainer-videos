from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats16.common import *  # noqa: F403


class Efficiency(VoiceoverScene):
    def construct(self):
        self.card()
        self.cost()
        self.laws()
        self.power()
        self.are_table()
        self.board()
        self.lessons()

    def card(self):
        card = chapter_card(5, r"Efficiency, \ a first look", r"What do ranks cost?", part=PART)
        with self.voiceover("Chapter five. Efficiency, a first look."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def cost(self):
        rows = [
            cmath(r"\text{ranks discard the sizes}", r":", r"\text{surely that costs power?}", font_size=30),
            cmath(r"\text{ARE}(W, t)", r"=", r"\lim \frac{n_t}{n_W}\ \text{ for equal power at small shifts}", font_size=30),
            cmath(r"\ ", r"=", r"12\,\sigma^2 \Big(\int f(x)^2\,dx\Big)^2", font_size=32),
            cmath(r"\text{normal } f", r":", r"3/\pi = 0.955", font_size=32),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"the worry of the 1940s"), why(r"Pitman (1948): \ asymptotic relative efficiency"),
                why(r"for shift alternatives; \ proved in Part 30"), why(r"lose 4.5\%: \ 100 ranks $\approx$ 95.5 normals")]
        with self.voiceover(
            "<bookmark mark='a'/> Ranks throw away the sizes of the observations. Surely that costs power, and if the data "
            "really are normal, the t-test should be much better? <bookmark mark='b'/> Edwin Pitman, in Australia, gave the "
            "measure in lecture notes of 1948: the asymptotic relative efficiency, the limiting ratio of the sample sizes two "
            "tests need for the same power against small shifts. <bookmark mark='c'/> For Wilcoxon against t it has a closed "
            "form, twelve sigma squared times the squared integral of the density squared. We'll prove it in Part 30. "
            "<bookmark mark='d'/> At the normal distribution, where the t-test is optimal, it's three over pi: point nine five "
            "five. Using ranks on normal data costs four and a half percent of the sample: a hundred observations analysed by "
            "ranks are worth ninety-five and a half analysed by t. That's a surprisingly small price."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def laws(self):
        xs = np.linspace(-6, 6, 500)
        A = axes([-6, 6], [0, 0.72], x_length=8.0, y_length=4.0, xlabel=r"error", ylabel=r"density", xticks=[-6, -3, 0, 3, 6],
                 yticks=[0, 0.2, 0.4, 0.6], center=[-1.8, 0.3, 0])
        ax = A.ax
        nrm = curve(ax, xs, stats.norm.pdf(xs), S.TRUTH, 3)
        t3 = curve(ax, xs, np.sqrt(3) * stats.t(3).pdf(xs * np.sqrt(3)), S.ALT, 3)
        cn = curve(ax, xs, 0.9 * stats.norm.pdf(xs) + 0.1 * stats.norm(0, 5).pdf(xs), RES, 3)
        rows = fit_rows(VGroup(
            label(r"normal", font_size=24, color=S.TRUTH),
            label(r"$t_3$, \ scaled to variance 1: \ heavy tails", font_size=24, color=S.ALT),
            label(r"contaminated: \ 90\% $N(0, 1)$, \ 10\% $N(0, 25)$", font_size=24, color=RES),
            label(r"the contaminated one looks normal: \ 1 value in 10 is a gross error", font_size=22, color=GREY_A),
        ), 4.6, 0.4, [4.6, 0.3, 0])
        with self.voiceover(
            "Now a simulation, with three error distributions. <bookmark mark='a'/> The normal. <bookmark mark='b'/> Student's t "
            "with three degrees of freedom, rescaled to variance one: taller in the middle, with heavy tails. "
            "<bookmark mark='c'/> And a contaminated normal: ninety percent of observations are standard normal, ten percent come "
            "from a normal with standard deviation five. <bookmark mark='d'/> Its density is barely distinguishable from the "
            "normal in the middle; the difference is one value in ten being a gross error. John Tukey made this model famous in "
            "1960 as the realistic case: most measurements are good, a few are wild."
        ) as vo:
            self.play(FadeIn(A))
            for k, (m_, c_) in enumerate(zip("abc", [nrm, t3, cn])):
                vo.wait_until(m_)
                self.play(Create(c_), FadeIn(rows[k]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def power(self):
        d = load("efficiency")
        pw = d["power"]
        A = axes([0, 3], [0, 1], x_length=7.6, y_length=4.2, xlabel=r"", ylabel=r"power at shift 0.8, \ 20 + 20",
                 yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.0, 0.4, 0])
        ax = A.ax
        bars = VGroup()
        vals = VGroup()
        names = VGroup()
        for k, nm in enumerate(["normal", "t3", "contaminated"]):
            for j, (key, col) in enumerate([("t", S.FIT), ("w", RANK)]):
                x0 = k + 0.18 + 0.33 * j
                h = pw[nm][key]
                b = Rectangle(width=ax.c2p(0.3, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, h)[1] - ax.c2p(0, 0)[1],
                              stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(ax.c2p(x0 + 0.15, 0), aligned_edge=DOWN)
                bars.add(b)
                vals.add(MathTex(f"{h:.2f}", font_size=22, color=col).next_to(b, UP, buff=0.08))
            names.add(label([r"normal", r"$t_3$", r"contaminated"][k], font_size=22).next_to(ax.c2p(k + 0.5, 0), DOWN, buff=0.2))
        key = VGroup(label(r"$t$-test", font_size=22, color=S.FIT), label(r"Wilcoxon--Mann--Whitney", font_size=22, color=RANK)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, 2.2, 0])
        rows = fit_rows(VGroup(
            label(r"normal: \ $t$ wins, \ narrowly", font_size=22, color=S.TRUTH),
            label(r"$t_3$: \ ranks win by 12 points", font_size=22, color=S.ALT),
            label(r"contaminated: \ 0.35 vs 0.52", font_size=22, color=RES),
        ), 4.4, 0.35, [4.6, -0.2, 0])
        tag = simulated_tag(r"4,000 trials per bar", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Two groups of twenty, the second shifted by point eight, four thousand trials of each test. "
            "<bookmark mark='b'/> At the normal, the t-test detects the shift sixty-nine percent of the time, Wilcoxon–Mann–Whitney "
            "sixty-six: a small loss, as Pitman said. <bookmark mark='c'/> With t-three errors, the rank test is ahead, eighty-"
            "nine percent to seventy-seven. <bookmark mark='d'/> Under contamination it's not close: fifty-two percent against "
            "thirty-five. The wild values inflate the standard deviation in the t statistic's denominator and hide the shift; "
            "ranks barely notice them."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.15), run_time=1.6)
            self.play(FadeIn(vals))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k]), Indicate(VGroup(bars[2 * k], bars[2 * k + 1]), scale_factor=1.05))
        self.clear_scene()

    def are_table(self):
        tab = table_rows([
            [r"errors", r"ARE of Wilcoxon to $t$"],
            [r"normal", r"$3/\pi = 0.955$"],
            [r"logistic", r"$\pi^2/9 = 1.097$"],
            [r"Laplace", r"$1.5$"],
            [r"$t_3$", r"$1.90$"],
            [r"contaminated (10\%, \ $\sigma = 5$)", r"$2.41$"],
            [r"any distribution", r"$\ge 108/125 = 0.864$"],
        ], font_size=26, colors=[GREY_B, S.TRUTH, None, None, S.ALT, RES, OBS]).move_to([-2.4, 0.3, 0])
        rows = fit_rows(VGroup(
            label(r"Hodges \& Lehmann (1956): \ never below 0.864", font_size=22, color=OBS),
            label(r"and no upper limit: \ for very heavy tails, \ $t$ can be useless", font_size=22, color=RES),
            label(r"a cheap insurance policy", font_size=26, color=RANK),
        ), 5.0, 0.4, [4.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Pitman's formula gives the efficiency for any error distribution. At the normal, point nine five "
            "five. At the logistic, one point one: the rank test is already better. At the double exponential, one and a half. "
            "At t-three, one point nine: the t-test needs almost twice the sample. At our contaminated normal, two point four. "
            "<bookmark mark='b'/> In 1956 Joseph Hodges and Erich Lehmann proved the striking result: over every continuous "
            "distribution, the efficiency is never below a hundred and eight over a hundred and twenty-five, point eight six "
            "four. <bookmark mark='c'/> And it has no upper limit: with heavy enough tails, the t-test can be arbitrarily worse. "
            "<bookmark mark='d'/> At most a fourteen percent loss, with unlimited gain possible: the rank test is a very cheap "
            "insurance policy."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:6]], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(tab[6]), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=16) if r.part == 16 and r.kind == "size"]
        b = coverage_board(rows, lit_part=16, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "What about validity? The Coverage Board's first two rows for this part are about size, not power. With no shift "
            "at all, under contamination, twenty and twenty, ten thousand trials: <bookmark mark='a'/> the t-test rejects "
            "four point four percent of the time: kept, slightly conservative. The t-test's size is robust; the central limit "
            "theorem protects it. <bookmark mark='b'/> Wilcoxon–Mann–Whitney: five point two percent, kept, as an exact "
            "permutation test must be. So the t-test under contamination isn't wrong. It's weak: the price of heavy tails is "
            "paid in power, which the Board doesn't show and the last chart did."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[1]))
        self.wait(1.0)
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"ranks cost little when the data are normal: \ 4.5\%", font_size=24),
            label(r"and gain a lot when they are not: \ heavy tails, \ gross errors", font_size=24, color=RANK),
            label(r"both tests keep their size here: \ the difference is power", font_size=24, color=OBS),
            label(r"but ranks answer a narrower question: \ $P(X > Y)$, \ not the mean difference", font_size=24, color=RES),
            label(r"for an estimate and interval: \ Hodges--Lehmann, \ or the bootstrap", font_size=24, color=BOOT),
        ), 12.4, 0.46, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: rank tests cost little when the data are normal, <bookmark mark='b'/> and can gain a great "
            "deal when they aren't. <bookmark mark='c'/> Both kinds of test keep their size in these examples: the difference "
            "is power. <bookmark mark='d'/> The catch is the question asked. A rank test is about whether one distribution "
            "tends to exceed the other, not about the difference in means, which is often the quantity a decision needs, "
            "such as total income or total cost. <bookmark mark='e'/> For estimates and intervals of whatever quantity you "
            "care about, without a model, we turn to resampling: first the jackknife, then the bootstrap."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
