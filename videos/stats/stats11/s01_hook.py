from __future__ import annotations

import numpy as np

from videos.stats.stats11.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.textbook()
        self.sawtooth()
        self.lucky()
        self.across_p()
        self.objectives()

    def textbook(self):
        f = MathTex(r"\hat p \pm 1.96\sqrt{\frac{\hat p(1 - \hat p)}{n}}", font_size=60, color=OBS).move_to([0, 1.2, 0])
        rows = fit_rows(VGroup(
            label(r"the interval for a proportion in nearly every textbook, \ poll and spreadsheet", font_size=28),
            label(r"Laplace (1812) to Wald (1943): \ ``the Wald interval''", font_size=24, color=GREY_A),
            label(r"it promises to catch $p$ 95\% of the time. \ Does it?", font_size=30, color=OBS),
        ), 12.6, 0.36, [0, -1.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the most widely used confidence interval in the world: the sample proportion, "
            "plus or minus one point nine six standard errors. <bookmark mark='b'/> It's in nearly every textbook, every "
            "opinion poll's margin of error, and every spreadsheet. It goes back to Laplace, and it's usually called the "
            "Wald interval. <bookmark mark='c'/> It promises to contain the true proportion ninety-five percent of the "
            "time. Let's check, exactly. For a binomial count there are only n plus one possible outcomes, so the "
            "chance the interval covers the truth can be computed exactly, with no simulation at all."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(f))
            for k, m_ in enumerate("bc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k] if k == 0 else rows[1:], shift=RIGHT * 0.2))
        self.clear_scene()

    def sawtooth(self):
        d = load("sawtooth")
        ns = np.asarray(d["ns"])
        A = axes([10, 100], [0.8, 0.97], x_length=10.0, y_length=4.4, xlabel=r"sample size $n$", ylabel=r"exact coverage at $p = 0.2$",
                 xticks=[10, 25, 50, 75, 100], yticks=[0.8, 0.85, 0.9, 0.95], yfmt=lambda v: f"{v:.2f}", center=[0, 0.3, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(10, 0.95), ax.c2p(100, 0.95), color=EXACT, stroke_width=2.5)
        line = polyline(ax, ns, d["cov_n"], MISS, 2.5)
        dots = VGroup(*[Dot(ax.c2p(n, c), radius=0.04, color=MISS) for n, c in zip(ns, d["cov_n"])])
        foot = fit_rows(VGroup(
            label(rf"never reaches 95\% for long; \ as low as {100 * d['min_n']:.1f}\%, \ and it zigzags as $n$ grows", font_size=26, color=MISS),
            label(r"more data does not steadily help: \ the coverage depends on how $np$ falls between integers", font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -2.6, 0])
        tag = note(r"exact: \ sums over the $n + 1$ outcomes").to_corner(UR, buff=0.3)
        with self.voiceover(
            "Take a true proportion of point two. <bookmark mark='a'/> Here is the interval's exact coverage, for every "
            "sample size from ten to a hundred. The green line is the promise: ninety-five percent. "
            "<bookmark mark='b'/> The coverage is almost always below it, as low as eighty-one and a half percent, and "
            "it doesn't climb smoothly toward the promise as n grows. It zigzags, a sawtooth: up, then a sudden drop, "
            "then up again. <bookmark mark='c'/> The teeth come from discreteness. The count can only take whole values, "
            "and as n changes, the possible values of p-hat slide past the edges of the interval in jumps."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dots, lag_ratio=0.01), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def lucky(self):
        d = load("sawtooth")
        hc = history_card(2001, r"L. Brown, \ T. Cai \& A. DasGupta, \ \emph{Statistical Science} 16", r"``Interval estimation for a binomial "
                          r"proportion'': \ the Wald interval's coverage is erratic and poor, \ even for large $n$, \ and the usual rules "
                          r"of thumb ($np \ge 5$) do not save it", color=OBS, width=9.6, font_size=24).move_to([0, 1.5, 0])
        rows = fit_rows(VGroup(
            MathTex(rf"p = 0.005:\quad n = 591:\ {100 * d['tiny']['591']:.1f}\%,\qquad n = 592:\ {100 * d['tiny']['592']:.1f}\%", font_size=34,
                    color=MISS),
            label(r"one more observation, \ and the coverage falls by 15 points", font_size=26),
            MathTex(rf"p = 0.5:\quad n = 17:\ {100 * d['lucky']['17']:.1f}\%,\qquad n = 40:\ {100 * d['lucky']['40']:.1f}\%", font_size=30),
            label(r"``lucky'' and ``unlucky'' sample sizes, \ even at $p = \tfrac12$", font_size=24, color=GREY_A),
        ), 12.6, 0.34, [0, -1.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2001, Lawrence Brown, Tony Cai and Anirban DasGupta published a paper that showed "
            "how bad this is, and it changed how statisticians teach the subject. Their most startling example: "
            "<bookmark mark='b'/> a true proportion of half a percent. With five hundred and ninety-one observations, the "
            "Wald interval covers ninety-four and a half percent of the time, close to the promise. With five hundred "
            "and ninety-two, seventy-nine percent. <bookmark mark='c'/> One more observation, and fifteen points of "
            "coverage vanish. <bookmark mark='d'/> Even at p equals a half, where the normal approximation should be "
            "best, there are lucky and unlucky sample sizes: seventeen observations cover ninety-five percent, forty only "
            "ninety-two."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def across_p(self):
        d = load("sawtooth")
        ps = np.asarray(d["ps"])
        A = axes([0, 1], [0.2, 1], x_length=9.6, y_length=4.4, xlabel=r"true proportion $p$, \ $n = 50$", ylabel=r"exact coverage",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0.2, 0.5, 0.8, 0.95, 1], center=[0, 0.2, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(0, 0.95), ax.c2p(1, 0.95), color=EXACT, stroke_width=2.5)
        cv = polyline(ax, ps, d["cov_p"], MISS, 2.2)
        foot = fit_rows(VGroup(
            label(rf"averaged over $p$: \ {100 * d['mean_p']:.1f}\%; \ near 0 and 1 it collapses", font_size=26, color=MISS),
            label(r"this part: \ what the promise means, \ how to keep it, \ and the board that checks", font_size=26, color=OBS),
        ), 12.6, 0.3, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now fix fifty observations and vary the true proportion. The coverage is a jagged "
            "comb, below the promise almost everywhere, and near zero and one, where real-world proportions often live, "
            "it collapses: a rare event with a true rate of one percent is covered less than four times in ten. "
            "<bookmark mark='b'/> Averaged over all p, it's ninety point seven percent. <bookmark mark='c'/> This part is "
            "about intervals that keep their promises: what the promise means, how to build intervals that keep it, and "
            "how the Coverage Board checks."
        ) as vo:
            self.play(FadeIn(A), Create(nom))
            vo.wait_until("a")
            self.play(Create(cv), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 11", font_size=34, color=GREY_B), label(r"Honest Intervals", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Neyman's definition of confidence, \ and what ``95\%'' does and does not promise",
            r"pivots, \ and intervals made by inverting tests: \ Neyman's belt",
            r"the binomial family: \ Wilson, \ Agresti--Coull, \ Clopper--Pearson, \ Jeffreys, \ likelihood",
            r"discreteness, \ ratios (Fieller), \ simultaneous bands, \ prediction and tolerance",
            r"credible vs confidence; \ the Coverage Board's protocol, \ formally",
        ], color=OBS, font_size=26)
        prereq = note(r"prerequisites: \ Part 10").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.intervals}; \ the interval rain").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part eleven: honest intervals. <bookmark mark='b'/> We'll start with Jerzy Neyman's "
            "definition of confidence and what it really promises; build intervals from pivots and by inverting tests; "
            "replace the Wald interval with the binomial intervals that work; and deal with discreteness, ratios, many "
            "intervals at once, and predicting the next observation. Then we'll compare confidence with Bayesian "
            "credibility, and set down the Coverage Board's protocol formally."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
