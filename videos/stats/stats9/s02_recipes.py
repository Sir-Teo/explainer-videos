from __future__ import annotations

import numpy as np

from videos.stats.stats9.common import *  # noqa: F403


class Recipes(VoiceoverScene):
    def construct(self):
        self.card()
        self.vocabulary()
        self.three_factories()
        self.sampling()
        self.rates()
        self.sources()

    def card(self):
        card = chapter_card(1, r"Estimators as recipes", r"What is an estimator, \ and how do we grade one?", part=PART)
        with self.voiceover("Chapter one. Estimators as recipes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def vocabulary(self):
        dc = definition_card(r"Estimator", r"a model $\{P_\theta : \theta \in \Theta\}$; \ data $X = (X_1, \dots, X_n) \sim P_\theta$; \ "
                             r"an \emph{estimator} is a function $T(X)$ of the data alone, \ used to guess $\theta$. \ "
                             r"Its value on the data in hand, \ $T(x)$, \ is an \emph{estimate}.", color=S.ACCENT, width=9.6,
                             font_size=26).move_to([0, 1.4, 0])
        rows = fit_rows(VGroup(
            MathTex(r"\text{tanks: }\ \theta = N,\quad X = (\text{serials}),\quad T(X) = 2\bar X - 1", font_size=32),
            label(r"$T$ may not peek at $\theta$; \ before the data, \ $T(X)$ is a random variable", font_size=26, color=GREY_A),
            label(r"so an estimator has a sampling distribution (Part 8), \ and we grade the distribution, \ not one estimate",
                  font_size=26, color=S.ACCENT),
        ), 12.6, 0.32, [0, -1.8, 0])
        with self.voiceover(
            "First, some words. <bookmark mark='a'/> A model is a family of distributions, indexed by an unknown "
            "parameter theta. The data are drawn from one member of the family. An estimator is any function of the "
            "data alone that we use to guess theta, and an estimate is the number it produces on the data in hand. "
            "<bookmark mark='b'/> For the tanks, theta is N, the data are the serial numbers, and doubling the average "
            "and subtracting one is an estimator. <bookmark mark='c'/> The one rule is that the recipe can't look at "
            "theta. Before we have the data, the estimator is a random variable. <bookmark mark='d'/> So it has a "
            "sampling distribution, exactly as in Part 8, and that's what we grade. Any single estimate can be lucky "
            "or unlucky. A recipe is good if its sampling distribution sits tightly around the truth, whatever the truth "
            "happens to be."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def three_factories(self):
        g = np.random.Generator(np.random.PCG64(9))
        N, k = 300, 6
        cols = VGroup()
        for j in range(3):
            caught = np.sort(g.choice(N, k, replace=False) + 1)
            f = TankFactory(N, caught, cols=20, cell=0.17, center=[-4.4 + 4.4 * j, 1.1, 0], show_numbers=False)
            m = caught.max()
            est = {"mom": 2 * caught.mean() - 1, "max": float(m), "umvue": m * (1 + 1 / k) - 1}
            txt = VGroup(
                MathTex(r",\,".join(str(c) for c in caught), font_size=24, color=S.ACCENT),
                *[MathTex(EST_TEX[e][1:-1] + rf" = {est[e]:.0f}", font_size=26, color=EST_COL[e]) for e in ("mom", "max", "umvue")],
            ).arrange(DOWN, buff=0.16).next_to(f.tanks, DOWN, buff=0.35)
            cols.add(VGroup(f, txt))
        head = label(r"three factories, \ each with $N = 300$; \ six tanks captured from each", font_size=26).to_edge(UP, buff=0.35)
        tag = simulated_tag(r"simulated: \ seeded draws", corner=DR)
        with self.voiceover(
            "Here's the game we'll play throughout. <bookmark mark='a'/> Three factories, each of which has built "
            "three hundred tanks. We capture six from each, at random. <bookmark mark='b'/> Each capture gives a "
            "different set of serial numbers, and each recipe gives a different estimate. <bookmark mark='c'/> Doubling "
            "the mean jumps around; the maximum never exceeds N and usually falls below it; and the scaled-up "
            "maximum lands on either side. Three factories can't settle which recipe is best. Ten thousand can."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[FadeIn(c[0].tanks) for c in cols])
            vo.wait_until("b")
            self.play(*[c[0].capture_anims(lag=0.15) for c in cols])
            self.play(*[FadeIn(c[1][0]) for c in cols])
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c[1][1:], shift=UP * 0.1) for c in cols], lag_ratio=0.3))
        self.clear_scene()

    def sampling(self):
        d = load("tanks")
        ed = np.asarray(d["edges"])
        panels = VGroup()
        for i, e in enumerate(("mom", "max", "umvue")):
            A = axes([100, 500], [0, 0.02], x_length=7.6, y_length=1.45, xticks=[100, 200, 300, 400, 500] if i == 2 else None,
                     center=[-1.8, 2.0 - 1.95 * i, 0])
            ax = A.ax
            bars = hist_bars(ax, ed, np.asarray(d["hist"][e]), color=EST_COL[e], opacity=0.75)
            truth = DashedLine(ax.c2p(300, 0), ax.c2p(300, 0.02), color=EXACT, stroke_width=2.5)
            st = d["stats6"][e]
            name = MathTex(EST_TEX[e][1:-1], font_size=28, color=EST_COL[e]).next_to(ax, UP, buff=0.02).align_to(ax, LEFT).shift(RIGHT * 0.25)
            nums = MathTex(rf"\text{{mean }} {st['mean']:.0f},\ \ \text{{SD }} {st['sd']:.0f},\ \ \text{{RMSE }} {st['rmse']:.0f}",
                           font_size=26, color=EST_COL[e]).move_to([4.6, 2.2 - 1.95 * i, 0])
            panels.add(VGroup(A, bars, truth, name, nums))
        tl = MathTex(r"N = 300", font_size=26, color=EXACT).next_to(panels[0][2], UP, buff=0.08)
        verdict = fit_rows(VGroup(
            label(r"$2\bar x - 1$: \ unbiased, \ wide", font_size=24, color=MOM),
            label(r"$\max$: \ tight, \ biased low", font_size=24, color=MAX),
            label(r"$m(1 + \tfrac1k) - 1$: \ unbiased \emph{and} tight", font_size=24, color=UMVUE),
        ), 4.6, 0.26, [4.6, -2.9, 0])
        tag = simulated_tag(r"simulated: \ 20,000 factories, \ $k = 6$", corner=UR)
        with self.voiceover(
            "So here are twenty thousand factories, each with three hundred tanks, six captured from each. "
            "<bookmark mark='a'/> The sampling distribution of two x-bar minus one is centred on three hundred, it's "
            "unbiased, but it's wide: its standard deviation is seventy. <bookmark mark='b'/> The maximum is tight, but "
            "it never exceeds the truth and is below it by forty-two on average. Its root mean squared error, which counts both "
            "failures, is fifty-six. <bookmark mark='c'/> The scaled maximum is centred and tight: standard deviation "
            "forty-three. It wins on both counts. <bookmark mark='d'/> Why should the maximum beat the mean? The mean "
            "averages every serial, but most of them say little about where the numbers stop; the largest one is "
            "pressed right up against the boundary we're trying to find. Explaining that properly is what sufficiency, "
            "in chapter six, is for."
        ) as vo:
            self.play(FadeIn(tag), *[FadeIn(p[0]) for p in panels], *[FadeIn(p[3]) for p in panels])
            self.play(*[Create(p[2]) for p in panels], FadeIn(tl))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(panels[k][1], lag_ratio=0.02), FadeIn(panels[k][4]), FadeIn(verdict[k]))
            vo.wait_until("d")
            self.play(Indicate(panels[2][4], color=UMVUE))
        self.clear_scene()

    def rates(self):
        d = load("tanks")
        ks = np.asarray(d["ks"])
        A = axes([2, 20], [0, 130], x_length=6.8, y_length=4.6, xlabel=r"tanks captured, \ $k$", ylabel=r"RMSE, \ $N = 300$",
                 xticks=[2, 5, 10, 15, 20], yticks=[0, 40, 80, 120], center=[-2.8, -0.3, 0])
        ax = A.ax
        lines = VGroup(*[polyline(ax, ks, d["rmse"][e], EST_COL[e], 3.5) for e in ("mom", "max", "umvue")])
        dots = VGroup(*[VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=EST_COL[e]) for a, b in zip(ks, d["rmse"][e])])
                        for e in ("mom", "max", "umvue")])
        th = polyline(ax, ks, d["umvue_sd_theory"], WHITE, 1.6, opacity=0.8)
        th.set_stroke(opacity=0.8)
        th_d = DashedVMobject(th, num_dashes=40)
        leg = legend([(MOM, EST_TEX["mom"]), (MAX, EST_TEX["max"]), (UMVUE, EST_TEX["umvue"]), (WHITE, r"exact SD of the UMVUE")],
                     font_size=22).move_to([4.5, 2.0, 0])
        rows = fit_rows(VGroup(
            MathTex(r"\mathrm{SD}(2\bar X - 1) = \sqrt{\frac{(N+1)(N-k)}{3k}} \;\approx\; \frac{N}{\sqrt{3k}}\quad(k\ll N)", font_size=28, color=MOM),
            MathTex(r"\mathrm{SD}\big(m(1 + \tfrac1k) - 1\big) = \sqrt{\frac{(N-k)(N+1)}{k(k+2)}} \;\approx\; \frac Nk\quad(1\ll k\ll N)", font_size=28,
                    color=UMVUE),
            label(r"the usual rate is $1/\sqrt k$; \ the maximum's is $1/k$", font_size=24, color=S.ACCENT),
        ), 5.4, 0.36, [3.9, -1.1, 0])
        tag = simulated_tag(r"simulated: \ 6,000 factories per $k$", corner=DR)
        with self.voiceover(
            "Now vary the number of tanks captured, from two to twenty. <bookmark mark='a'/> Each curve is a recipe's "
            "root mean squared error. All three fall as we capture more, but not at the same speed. "
            "<bookmark mark='b'/> The mean-based recipe's standard deviation has an exact formula: it falls like one "
            "over root k, the rate of every average in Part 6. <bookmark mark='c'/> The scaled maximum's falls like one "
            "over k, and the white dashes, its exact standard deviation, sit on the simulation. "
            "<bookmark mark='d'/> One over k is faster than one over root k. When the capture is a small fraction of a large factory, capture four times as many tanks and approximately the "
            "mean-based error halves, but the maximum-based error falls by four. Remember this. Later in the part we'll "
            "prove that, for smooth problems, no unbiased estimator can beat one over root n. The tank problem isn't "
            "smooth, and that's how it escapes."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            for i in range(3):
                self.play(Create(lines[i]), FadeIn(dots[i]), FadeIn(leg[i]), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(th_d), FadeIn(leg[3]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def sources(self):
        items = [
            (r"plug-in: \ the sample's version of the population quantity", r"Part 8", S.LIK),
            (r"the method of moments: \ match averages", r"ch.~2", MOM),
            (r"maximum likelihood: \ make the data most probable", r"chs.~3--5", LIK),
            (r"best unbiased: \ condition on what matters", r"chs.~6--8", UMVUE),
            (r"least squares: \ minimize the squared misfit", r"Part 12", GREY_A),
            (r"Bayes: \ average over a prior", r"Part 15", S.POST),
            (r"minimax and decision theory: \ guard the worst case", r"Part 45", GREY_A),
        ]
        rows = VGroup()
        for t, where, c in items:
            rows.add(VGroup(label(t, font_size=26, color=c), label(where, font_size=24, color=GREY_B)))
        for r in rows:
            r[1].move_to([5.6, 0, 0])
            r[0].move_to([-0.9, 0, 0]).align_to([-6.3, 0, 0], LEFT)
        rows.arrange(DOWN, buff=0.36).move_to([0, -0.4, 0])
        for r in rows:
            r[0].align_to([-6.3, 0, 0], LEFT)
            r[1].align_to([6.3, 0, 0], RIGHT)
        head = label(r"where recipes come from", font_size=36).to_edge(UP, buff=0.5)
        with self.voiceover(
            "The tank recipes were guesses. Where do good recipes come from in general? There are a handful of "
            "principles, and this course will meet all of them. <bookmark mark='a'/> Plug-in, from Part 8: compute the "
            "sample's version of the population quantity. <bookmark mark='b'/> The method of moments: match the "
            "model's averages to the sample's. <bookmark mark='c'/> Maximum likelihood: choose the parameter that makes "
            "the observed data most probable. <bookmark mark='d'/> Best unbiased estimation: among recipes that are "
            "right on average, take the least variable. <bookmark mark='e'/> Least squares, for regression. "
            "<bookmark mark='f'/> Bayes, which averages over a prior. <bookmark mark='g'/> And minimax, which guards "
            "against the worst case. This part builds the middle three, which together form the classical theory of "
            "point estimation."
        ) as vo:
            self.play(FadeIn(head))
            for k, m_ in enumerate("abcdefg"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
