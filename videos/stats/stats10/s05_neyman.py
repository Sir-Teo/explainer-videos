from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats10.common import *  # noqa: F403


class Neyman(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.table()
        self.curves()
        self.power_n()
        self.philosophies()

    def card(self):
        card = chapter_card(4, r"Two kinds of error", r"Neyman and Pearson's theory of tests", lit=(1933,), part=PART)
        with self.voiceover("Chapter four. Two kinds of error."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        h1 = history_card(1928, r"Jerzy Neyman \& Egon Pearson", r"``On the use and interpretation of certain test criteria'': \ a test "
                          r"should be judged against the alternatives it is meant to detect", color=ALTC, width=6.0,
                          font_size=22).move_to([-3.3, 0.8, 0])
        h2 = history_card(1933, r"Neyman \& Pearson, \ \emph{Phil.\ Trans.\ A} 231", r"``On the problem of the most efficient tests of "
                          r"statistical hypotheses'': \ two errors, \ size and power, \ and the lemma of ch.~5", color=ALTC, width=6.0,
                          font_size=22).move_to([3.3, 0.8, 0])
        foot = label(r"Egon was Karl Pearson's son; \ Neyman, \ a Polish mathematician, \ came to his father's lab in 1925", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Fisher's test has no alternative hypothesis. Two younger statisticians thought that was a mistake. "
            "<bookmark mark='a'/> Jerzy Neyman, a Polish mathematician who had come to Karl Pearson's laboratory in "
            "London in 1925, and Egon Pearson, Karl's son, argued in 1928 that a test can only be judged against the "
            "alternatives it's supposed to detect. <bookmark mark='b'/> In their 1933 paper on the most efficient tests "
            "of statistical hypotheses, they built a theory around two kinds of error. It became the textbook theory of "
            "testing, and it made Fisher furious. <bookmark mark='c'/>"
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(h1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(h2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def table(self):
        cells = [
            (r"correct", GREY_A, r"Type I error", REJ),
            (r"Type II error", ALTC, r"correct: \ power", OBS),
        ]
        grid = VGroup()
        for i in range(2):
            for j in range(2):
                txt, col = cells[i][2 * j], cells[i][2 * j + 1]
                box = Rectangle(width=3.6, height=1.3, stroke_color=GREY_B, stroke_width=2)
                box.move_to([-1.2 + 3.6 * j, 1.0 - 1.3 * i, 0])
                grid.add(VGroup(box, label(txt, font_size=26, color=col).move_to(box)))
        cols = VGroup(label(r"do not reject $H_0$", font_size=24, color=GREY_A).next_to(grid[0], UP, buff=0.2),
                      label(r"reject $H_0$", font_size=24, color=GREY_A).next_to(grid[1], UP, buff=0.2))
        rws = VGroup(label(r"$H_0$ true", font_size=24, color=NULLC).next_to(grid[0], LEFT, buff=0.3),
                     label(r"$H_0$ false", font_size=24, color=ALTC).next_to(grid[2], LEFT, buff=0.3))
        rows = fit_rows(VGroup(
            MathTex(r"\alpha = P_{H_0}(\text{reject}) \quad\text{the size}", font_size=30, color=REJ),
            MathTex(r"\beta(\theta) = P_\theta(\text{do not reject}),\quad 1 - \beta(\theta) \quad\text{the power}", font_size=30, color=ALTC),
            label(r"fix $\alpha$ in advance; \ among tests of size $\alpha$, \ choose the most powerful", font_size=26, color=OBS),
        ), 12.6, 0.3, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A test ends in a decision: reject the null or don't. And the null is either true or "
            "false. That gives four cells. Two are correct. <bookmark mark='b'/> Rejecting a true null is a Type I "
            "error, a false alarm. Its probability is the size of the test, alpha. <bookmark mark='c'/> Failing to "
            "reject a false null is a Type II error, a miss. Its probability, beta, depends on how false the null is, "
            "and one minus beta is the power. <bookmark mark='d'/> Neyman and Pearson's recipe: fix the size in "
            "advance, say at five percent, and among all tests with that size, choose the one with the greatest power. "
            "Testing becomes an optimization problem."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(grid[0]), FadeIn(grid[3]), FadeIn(cols), FadeIn(rws))
            vo.wait_until("b")
            self.play(FadeIn(grid[1]), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(grid[2]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def curves(self):
        xs = np.linspace(-3.5, 6.0, 400)
        dlt = 2.5
        A = axes([-3.5, 6], [0, 0.45], x_length=10.0, y_length=3.6, xlabel=r"the test statistic $Z = \sqrt n\,\bar x/\sigma$",
                 xticks=[-2, 0, 1.645, 2.5, 4], center=[0, 0.8, 0])
        ax = A.ax
        f0, f1 = stats.norm.pdf(xs), stats.norm.pdf(xs, dlt)
        c0, c1 = curve(ax, xs, f0, NULLC, 3), curve(ax, xs, f1, ALTC, 3)
        l0 = label(r"$H_0$: \ $\mu = 0$", font_size=24, color=NULLC).move_to(ax.c2p(-2.4, 0.38))
        l1 = label(r"$H_1$: \ $\mu = \delta$", font_size=24, color=ALTC).move_to(ax.c2p(4.6, 0.38))
        cut = ValueTracker(1.645)

        def regions():
            c = cut.get_value()
            r = xs >= c
            a = shade(ax, xs[r], f0[r], REJ, 0.6)
            b = shade(ax, xs[~r], f1[~r], ALTC, 0.25)
            ln = DashedLine(ax.c2p(c, 0), ax.c2p(c, 0.44), color=OBS, stroke_width=2.5)
            return VGroup(b, a, ln)

        reg = always_redraw(regions)

        def nums():
            c = cut.get_value()
            a, b = stats.norm.sf(c), stats.norm.cdf(c - dlt)
            return VGroup(MathTex(rf"\alpha = {a:.3f}", font_size=32, color=REJ), MathTex(rf"\beta = {b:.3f}", font_size=32, color=ALTC),
                          MathTex(rf"\text{{power}} = {1 - b:.3f}", font_size=32, color=OBS)).arrange(RIGHT, buff=0.8).move_to([0, -1.9, 0])

        nm = always_redraw(nums)
        foot = label(r"moving the line trades one error for the other; \ only more data shrinks both", font_size=26,
                     color=OBS).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here's the picture for the simplest case, testing whether a normal mean is zero, against the alternative "
            "that it's some positive delta. <bookmark mark='a'/> The statistic's distribution under the null is the "
            "grey curve; under the alternative, the green one, shifted by delta times root n over sigma. "
            "<bookmark mark='b'/> Reject when the statistic exceeds a line. The red tail of the null curve beyond the "
            "line is alpha, the false-alarm rate. The part of the green curve below the line is beta, the miss rate. "
            "With the line at one point six four five, alpha is five percent and the power is eighty. "
            "<bookmark mark='c'/> Move the line right and false alarms drop, but misses rise. <bookmark mark='d'/> Move it "
            "left, and the reverse. <bookmark mark='e'/> For a fixed amount of data, the two errors trade against each "
            "other. The only way to shrink both is to pull the curves apart, by collecting more data."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(c0), FadeIn(l0))
            self.play(Create(c1), FadeIn(l1))
            vo.wait_until("b")
            self.add(reg, nm)
            self.play(FadeIn(reg), FadeIn(nm))
            vo.wait_until("c")
            self.play(cut.animate.set_value(2.6), run_time=2.5)
            vo.wait_until("d")
            self.play(cut.animate.set_value(0.8), run_time=3.0)
            self.play(cut.animate.set_value(1.645), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        reg.clear_updaters()
        nm.clear_updaters()
        self.clear_scene()

    def power_n(self):
        d = load("errors")
        ns = np.asarray(d["ns"])
        A = axes([0, 60], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"sample size $n$", ylabel=r"power, \ $\delta = 0.5\sigma$, \ $\alpha = 0.05$",
                 xticks=[0, 10, 20, 32, 43, 60], yticks=[0, 0.05, 0.5, 0.8, 0.9, 1], center=[-2.2, -0.3, 0])
        ax = A.ax
        cv = polyline(ax, ns, d["power"], OBS, 3.5)
        g80 = VGroup(DashedLine(ax.c2p(0, 0.8), ax.c2p(32, 0.8), color=GREY_B, stroke_width=1.5),
                     DashedLine(ax.c2p(32, 0), ax.c2p(32, 0.8), color=GREY_B, stroke_width=1.5))
        g90 = VGroup(DashedLine(ax.c2p(0, 0.9), ax.c2p(43, 0.9), color=GREY_B, stroke_width=1.5),
                     DashedLine(ax.c2p(43, 0), ax.c2p(43, 0.9), color=GREY_B, stroke_width=1.5))
        rows = fit_rows(VGroup(
            MathTex(r"1 - \beta = \Phi\Big(\frac{\delta\sqrt n}{\sigma} - z_{1 - \alpha/2}\Big) + \Phi\Big(-\frac{\delta\sqrt n}{\sigma} - z_{1 - \alpha/2}\Big)",
                    font_size=24),
            MathTex(r"n = \Big(\frac{(z_{1-\alpha/2} + z_{1-\beta})\,\sigma}{\delta}\Big)^2", font_size=30, color=OBS),
            MathTex(rf"80\%:\ n = {d['n80']},\qquad 90\%:\ n = {d['n90']}", font_size=30),
            label(r"the two-sided $z$-test; \ chapter 9 does this properly", font_size=22, color=GREY_A),
        ), 5.2, 0.36, [4.3, -0.3, 0])
        with self.voiceover(
            "That gives a way to plan an experiment. <bookmark mark='a'/> For the two-sided z-test, the power has a "
            "formula, and it climbs with the sample size: here, for a true effect of half a standard deviation. "
            "<bookmark mark='b'/> Solve for n: the sum of two normal quantiles, times sigma over delta, squared. "
            "<bookmark mark='c'/> For eighty percent power you need thirty-two observations; for ninety, forty-three. "
            "Choosing the size of a study before running it, from the effect you want to be able to detect, is one of "
            "Neyman and Pearson's most lasting gifts. Chapter nine returns to it."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(g80), Create(g90), FadeIn(rows[2:]))
        self.clear_scene()

    def philosophies(self):
        left = VGroup(label(r"Fisher", font_size=34, color=NULLC),
                      label(r"evidence about this experiment", font_size=24),
                      label(r"report $p$, \ graded", font_size=24),
                      label(r"no alternative needed", font_size=24),
                      label(r"``inductive inference''", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.3)
        right = VGroup(label(r"Neyman \& Pearson", font_size=34, color=ALTC),
                       label(r"a rule for many decisions", font_size=24),
                       label(r"fix $\alpha$, \ reject or not", font_size=24),
                       label(r"power against an alternative", font_size=24),
                       label(r"``inductive behaviour''", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.3)
        left.move_to([-3.4, 0.8, 0])
        right.move_to([3.4, 0.8, 0])
        div = Line([0, 2.6, 0], [0, -1.2, 0], color=GREY_D)
        foot = fit_rows(VGroup(
            label(r"today's textbook test is a hybrid: \ Fisher's $p$ compared with Neyman's $\alpha$", font_size=26, color=OBS),
            label(r"they quarrelled for thirty years; \ Gigerenzer (2004) calls the hybrid a ``null ritual''", font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -2.3, 0])
        with self.voiceover(
            "The two views are different philosophies. <bookmark mark='a'/> For Fisher, a test measures the evidence "
            "in this particular experiment against a hypothesis. You report the p-value, and its size grades the "
            "evidence. No alternative is needed. <bookmark mark='b'/> For Neyman, a test is a rule of behaviour: a "
            "procedure that, applied over many experiments, makes Type I errors at rate alpha and catches real effects "
            "at the rate of its power. You decide, reject or not, and you don't claim to have learned anything about "
            "this particular case. <bookmark mark='c'/> Modern practice is an awkward hybrid: compute Fisher's p-value, "
            "compare it with Neyman's alpha, and declare significance. The two men quarrelled bitterly for thirty "
            "years, and neither would have endorsed the hybrid."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(left, lag_ratio=0.2), Create(div))
            vo.wait_until("b")
            self.play(FadeIn(right, lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
