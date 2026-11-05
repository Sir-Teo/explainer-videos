from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats16.common import *  # noqa: F403


class Failure(VoiceoverScene):
    def construct(self):
        self.card()
        self.tanks()
        self.spike()
        self.why_spike()
        self.board()
        self.fixes()
        self.other()

    def card(self):
        card = chapter_card(9, r"When the bootstrap fails", r"The German tanks, \ one more time", lit=(1943,), part=PART)
        with self.voiceover("Chapter nine. When the bootstrap fails."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def tanks(self):
        d = load("maxfail")
        rows = [
            cmath(r"x_1, \ldots, x_n", r"\sim", r"\text{Uniform}(0, \theta),\ \ n = 50,\ \ \theta = 1", font_size=32),
            cmath(r"\hat\theta", r"=", rf"\max_i x_i = {d['max']:.3f}", font_size=32),
            cmath(r"\text{its law}", r":", r"P(\hat\theta \le t) = (t/\theta)^n,\ \ \text{continuous}", font_size=32),
            cmath(r"n(\theta - \hat\theta)/\theta", r"\to", r"\text{Exponential}(1)", font_size=32),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"Part 9's tank factory, \ continuous"), why(r"the maximum serial number seen"),
                why(r"Part 9: \ always below $\theta$"), why(r"the error shrinks like $1/n$, \ not $1/\sqrt n$")]
        with self.voiceover(
            "Chapter eight's failure was gentle: intervals a little too short. Here's a case where the bootstrap fails "
            "completely, and it's one we know well. <bookmark mark='a'/> Part 9's tank factory, in its continuous form: fifty "
            "draws from a uniform distribution on zero to theta, with theta equal to one. <bookmark mark='b'/> The natural "
            "estimate is the maximum, here point nine six six. <bookmark mark='c'/> Its sampling distribution has a simple "
            "formula, and it's continuous: the maximum is always a little below theta, by a random amount. "
            "<bookmark mark='d'/> Scaled by n, the shortfall is approximately exponential. The maximum is unusually accurate, "
            "with an error of order one over n, and it isn't a smooth function of the data's distribution: it depends only on "
            "the edge."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def spike(self):
        d = load("maxfail")
        real, boot = np.asarray(d["real"]), np.asarray(d["boot"])
        e = np.linspace(0.84, 1.0, 41)
        w = e[1] - e[0]
        A = axes([0.84, 1.0], [0, 0.7], x_length=5.6, y_length=3.4, xlabel=r"the maximum of a real sample", ylabel=r"share",
                 xticks=[0.85, 0.9, 0.95, 1.0], yticks=[0, 0.2, 0.4, 0.6], center=[-3.6, 0.6, 0], font_size=18)
        B = axes([0.84, 1.0], [0, 0.7], x_length=5.6, y_length=3.4, xlabel=r"the maximum of a resample", ylabel=r"share",
                 xticks=[0.85, 0.9, 0.95, 1.0], yticks=[0, 0.2, 0.4, 0.6], center=[3.0, 0.6, 0], font_size=18)
        hr = hist_bars(A.ax, e, np.histogram(real, e)[0] / len(real), color=REAL, opacity=0.85)
        vals, cnt = np.unique(boot, return_counts=True)
        sp = VGroup(*[Line(B.ax.c2p(v, 0), B.ax.c2p(v, c / len(boot)), color=BOOT, stroke_width=6) for v, c in zip(vals, cnt) if v > 0.84])
        th = DashedLine(A.ax.c2p(1, 0), A.ax.c2p(1, 0.68), color=S.TRUTH, stroke_width=3)
        mx = DashedLine(B.ax.c2p(d["max"], 0), B.ax.c2p(d["max"], 0.68), color=OBS, stroke_width=2)
        ta = label(r"4,000 real samples of 50", font_size=20, color=REAL).next_to(A, UP, buff=0.12)
        tb = label(r"4,000 resamples of one sample", font_size=20, color=BOOT).next_to(B, UP, buff=0.12)
        rows = fit_rows(VGroup(
            MathTex(rf"P^*(\hat\theta^* = \hat\theta) = {d['p_spike']:.3f}", font_size=30, color=BOOT),
            label(r"the bootstrap world has a spike; \ the real world has none", font_size=22, color=RES),
        ), 12.4, 0.25, [0, -2.5, 0])
        tag = simulated_tag(r"Uniform$(0, 1)$", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> On the left, the real sampling distribution of the maximum: four thousand samples of fifty. "
            "It's smooth, piled up just below one. <bookmark mark='b'/> On the right, four thousand resamples of our one sample. "
            "The maximum of a resample can only be one of the sample's values, and usually it's the largest. "
            "<bookmark mark='c'/> Sixty-two and a half percent of the resamples have exactly the original maximum. "
            "<bookmark mark='d'/> The bootstrap distribution is a few spikes; the real one has no spike at all. The bootstrap "
            "world doesn't resemble the real one, so no interval built from it can be trusted."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ta), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in hr], lag_ratio=0.02), Create(th), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(tb), Create(mx), LaggedStart(*[Create(s_) for s_ in sp], lag_ratio=0.1), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), Indicate(sp[-1], color=OBS))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def why_spike(self):
        d = load("maxfail")
        rows = [
            cmath(r"P^*(\hat\theta^* < \hat\theta)", r"=", r"P^*(\text{the largest } x_i \text{ is never drawn})", font_size=30),
            cmath(r"\ ", r"=", r"(1 - 1/n)^n", font_size=32),
            cmath(r"P^*(\hat\theta^* = \hat\theta)", r"=", rf"1 - (1 - 1/n)^n = {d['theory']:.3f}\ \ (n = 50)", font_size=30),
            cmath(r"\ ", r"\to", rf"1 - 1/e = {d['limit']:.3f}", font_size=32),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"each of $n$ draws misses it"), why(r"independent draws, \ each missing with chance $1 - 1/n$"),
                why(r"simulated: \ 0.625"), why(r"Part 6's limit: \ the spike never goes away")]
        with self.voiceover(
            "<bookmark mark='a'/> Why sixty-two percent? A resample's maximum is below the sample's only if the largest value "
            "is never drawn. <bookmark mark='b'/> Each of the n draws misses it with probability one minus one over n, so all "
            "of them miss with probability that to the n-th power. <bookmark mark='c'/> The chance of a spike is one minus "
            "that: point six three six for fifty, against the simulated point six two five. <bookmark mark='d'/> And as n grows "
            "it tends to one minus one over e, the limit from Part 6. The spike never goes away, however large the sample: "
            "the bootstrap is inconsistent for the maximum. Bickel and Freedman, in 1981, were among the first to say exactly "
            "when the bootstrap works; the maximum is a standard counterexample."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=16) if r.part == 16 and r.setting.startswith("Uniform")]
        b = coverage_board(rows, lit_part=16, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "The Coverage Board. Ten thousand samples of fifty from the uniform, with theta equal to one. "
            "<bookmark mark='a'/> The percentile interval covers zero percent. Not low: zero. Every resampled maximum is at most "
            "the sample maximum, which is below theta, so the interval always lies entirely below the truth. "
            "<bookmark mark='b'/> The basic interval, which reflects the percentiles above the estimate, does better, eighty-"
            "seven point eight percent, but it's still broken: the spike puts too little spread above the maximum."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[1]))
        self.wait(1.0)
        self.clear_scene()

    def fixes(self):
        d = load("maxfail")
        m = d["max"]
        hi = m / 0.025 ** (1 / 50)
        rows = [
            cmath(r"\text{an exact pivot}", r":", r"\hat\theta/\theta \sim \text{Beta}(n, 1)", font_size=30),
            cmath(r"\text{95\% CI}", r"=", rf"\big[\hat\theta,\ \hat\theta / 0.025^{{1/n}}\big] = [{m:.3f},\ {hi:.3f}]", font_size=30),
            cmath(r"\text{parametric bootstrap}", r":", r"\text{resample from Uniform}(0, \hat\theta)", font_size=30),
            cmath(r"m\text{-out-of-}n", r":", r"\text{resample } m \ll n \text{ points, rescale}", font_size=30),
        ]
        rows[1][2].set_color(HIT)
        whys = [why(r"Part 11: \ a pivot from the model"), why(r"exact coverage for every $\theta$"),
                why(r"use the model, \ when there is one"), why(r"Bickel, \ G\"otze \& van Zwet (1997)")]
        with self.voiceover(
            "How to fix it. <bookmark mark='a'/> When there's a model, use it, with a pivot in Part 11's sense: the maximum over theta has a "
            "Beta n, one distribution, whatever theta is. <bookmark mark='b'/> That gives an exact interval, from the maximum "
            "to the maximum over point oh two five to the one over n: point nine six six to one point oh four oh. It covers "
            "exactly ninety-five percent. <bookmark mark='c'/> Or a parametric bootstrap: resample from the fitted uniform, not "
            "from the data, so the resamples have no spike. <bookmark mark='d'/> And without a model, resample fewer points "
            "than you have, m out of n, and rescale. With m small compared with n, the spike shrinks; Peter Bickel, Friedrich "
            "Götze and Willem van Zwet showed in 1997 that this repairs many failures, at a cost in efficiency."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def other(self):
        rows = fit_rows(VGroup(
            label(r"where the plain bootstrap fails, \ or needs care:", font_size=26),
            label(r"extremes and edges: \ maxima, \ minima, \ parameters on a boundary", font_size=24, color=RES),
            label(r"heavy tails with infinite variance: \ the mean of a Cauchy-like sample", font_size=24, color=RES),
            label(r"dependent data: \ resampling single points destroys the dependence \ (Part 17)", font_size=24, color=RES),
            label(r"tiny samples: \ $\hat F_n$ is a poor copy of $F$", font_size=24, color=RES),
            label(r"its success is a theorem with conditions: \ smoothness, \ independence", font_size=26, color=OBS),
        ), 12.4, 0.42, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The maximum isn't the only failure. <bookmark mark='b'/> Edges in general: maxima, minima, and "
            "parameters at the boundary of the space, such as a variance component that might be zero. "
            "<bookmark mark='c'/> Heavy tails with infinite variance, where the sample mean has no normal limit and the "
            "bootstrap of the mean is inconsistent. <bookmark mark='d'/> Dependent data, where resampling single points destroys "
            "exactly what matters; Part 17 resamples blocks instead. <bookmark mark='e'/> And tiny samples, where the empirical "
            "distribution is a poor copy of the population. <bookmark mark='f'/> The bootstrap's success is a theorem, and like "
            "every theorem it has conditions: smoothness and independence. Within them it's one of the most useful tools in "
            "statistics; outside, it fails without warning, which is why the Board tests it."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
