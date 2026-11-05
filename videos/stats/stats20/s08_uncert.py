from __future__ import annotations

import numpy as np

from videos.stats.stats20.common import *  # noqa: F403


class Uncertainty(VoiceoverScene):
    def construct(self):
        self.card()
        self.four()
        self.bootstrap()
        self.intervals()
        self.mean()
        self.silent()

    def card(self):
        card = chapter_card(7, r"Uncertainty", r"Which standard error?", part=PART)
        with self.voiceover("Chapter seven. Uncertainty."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def four(self):
        d = load("uncert")
        rows = [
            cmath(r"\text{model-based}", r":", rf"{d['se_model']:.3f}", font_size=30),
            cmath(r"\text{sandwich (HC0)}", r":", rf"{d['se_hc']:.3f}", font_size=30),
            cmath(r"\text{design, \ linearized}", r":", rf"{d['se_design']:.3f}", font_size=30),
            cmath(r"\text{design, \ PSU bootstrap}", r":", rf"{d['se_boot']:.3f}", font_size=30),
        ]
        rows[2][2].set_color(DES)
        rows[3][2].set_color(DES)
        whys = [why(r"Part 12: \ $\sigma^2 (X'WX)^{-1}$, \ weights as precisions"),
                why(r"Part 12's White SEs"),
                why(r"the sandwich summed over PSUs, \ within strata"),
                why(r"Rao \& Wu (1988): \ resample PSUs, \ 1,000 times")]
        with self.voiceover(
            "The slope for sodium was plus point zero seven. How uncertain is it? There are four answers on offer. "
            "<bookmark mark='a'/> The model-based standard error treats the weights as if they were precisions and the "
            "errors as independent with equal variance: point two three. <bookmark mark='b'/> Part 12's sandwich, robust to "
            "unequal variances but still treating people as independent: point three one. <bookmark mark='c'/> The "
            "design-based standard error, the same sandwich but with scores summed within each PSU, so that people in the same "
            "cluster count together: point two seven. <bookmark mark='d'/> And a bootstrap that resamples whole PSUs within "
            "strata, Rao and Wu's method, a thousand times: point two seven again."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.8, buff=0.75, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bootstrap(self):
        d = load("uncert")
        bs = np.asarray(d["boot"])
        edges = np.linspace(-1.0, 1.1, 43)
        h, _ = np.histogram(bs, edges)
        hd = h / len(bs) / (edges[1] - edges[0])
        A = axes([-1.0, 1.1], [0, 1.8], x_length=8.4, y_length=4.2, xlabel=r"sodium slope, \ mm Hg per g", ylabel=r"density",
                 xticks=[-1, -0.5, 0, 0.5, 1], yticks=[0, 0.5, 1, 1.5], center=[-1.4, 0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, edges, hd, color=DES)
        xs = np.linspace(-1, 1.1, 200)
        se = d["se_design"]
        nc = polyline(ax, xs, np.exp(-0.5 * ((xs - d["est"]) / se) ** 2) / (se * np.sqrt(2 * np.pi)), TRUE, 3)
        est = DashedLine(ax.c2p(d["est"], 0), ax.c2p(d["est"], 1.8), color=SALT, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"1,000 bootstrap replicates", font_size=22),
            label(r"each: \ in every stratum, \ draw 1 of its 2 PSUs with replacement, \ rescale", font_size=20, color=GREY_A),
            label(r"gold: \ normal, \ SD $=$ the linearized SE", font_size=22, color=TRUE),
            label(r"two methods, \ one answer", font_size=22, color=HIT),
        ), 3.45, 0.4, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are the thousand bootstrap slopes. <bookmark mark='b'/> In each replicate, every stratum "
            "keeps one of its two PSUs, drawn at random with replacement, and the weights are rescaled to make up for the one "
            "left out. That mimics drawing the survey again. <bookmark mark='c'/> In gold, a normal curve with the linearized "
            "standard error. <bookmark mark='d'/> The two methods agree closely, which is reassuring: one rests on a Taylor "
            "expansion, the other on resampling, and with only fifteen strata neither is guaranteed."
        ) as vo:
            self.play(FadeIn(A), Create(est))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(nc), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def intervals(self):
        d = load("uncert")
        b = d["est"]
        items = [(r"model, \ $z$", d["se_model"], 1.96, GREY_B), (r"sandwich, \ $z$", d["se_hc"], 1.96, GREY_A),
                 (r"design, \ $z$", d["se_design"], 1.96, DES), (rf"design, \ $t_{{15}}$", d["se_design"], d["t"], SALT)]
        A = axes([-1, 1.2], [0, 4.6], x_length=8.0, y_length=3.8, xlabel=r"95\% interval for the sodium slope, \ mm Hg per g",
                 xticks=[-1, -0.5, 0, 0.5, 1], center=[0.6, 0.4, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 4.6), color=GREY_C, stroke_width=1.5)
        lines, labs = VGroup(), VGroup()
        for k, (t, se, q, c) in enumerate(items):
            y = 4 - k
            lines.add(VGroup(Line(ax.c2p(b - q * se, y), ax.c2p(b + q * se, y), color=c, stroke_width=6),
                             Dot(ax.c2p(b, y), radius=0.08, color=c)))
            labs.add(label(t + rf": \ [{b - q * se:+.2f}, {b + q * se:+.2f}]", font_size=20, color=c)
                     .next_to(ax.c2p(-1, y), LEFT, buff=0.2))
        foot = fit_rows(VGroup(
            label(rf"15 degrees of freedom: \ $t_{{0.975}} = {d['t']:.2f}$, \ not 1.96", font_size=22, color=SALT),
            label(r"the plan's choice: \ design-based, \ $t_{15}$; \ the widest, \ and the honest one", font_size=22, color=OBS),
        ), 12.0, 0.25, [0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> As intervals: model-based, sandwich, and design-based with the normal multiplier. "
            "<bookmark mark='b'/> And the design-based one with t, not z. Fifteen degrees of freedom means a multiplier of two "
            "point one three instead of one point nine six, which is Part 11's small-sample lesson reappearing: the "
            "standard error itself is estimated from only thirty PSUs. <bookmark mark='c'/> The plan chose that last interval, "
            "minus point five oh to plus point six three. It's the widest, and the honest one. Every interval agrees on the "
            "conclusion: small, and indistinguishable from zero."
        ) as vo:
            self.play(FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(Create(lines[k]), FadeIn(labs[k])) for k in range(3)], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(lines[3]), FadeIn(labs[3]), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def mean(self):
        d = load("uncert")
        rows = [
            cmath(r"\text{mean pressure, \ the sample's population}", r":", rf"{d['mean']:.1f}", font_size=28),
            cmath(r"\text{SE: \ as an SRS}", r":", rf"{d['mean_se_srs']:.2f}", font_size=30),
            cmath(r"\text{SE: \ design}", r":", rf"{d['mean_se']:.2f}\ \ (\text{{bootstrap}}\ {d['mean_se_boot']:.2f})", font_size=30),
            cmath(r"\text{design effect}", r":", rf"{(d['mean_se'] / d['mean_se_srs']) ** 2:.1f}\ \ \text{{vs about 1.4 for the slope}}", font_size=28),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"adults not on BP medicine"), why(r"$s / \sqrt n$"), why(r"two methods agree"),
                why(r"means suffer more from clustering than slopes")]
        with self.voiceover(
            "<bookmark mark='a'/> Compare a plain mean: average pressure in the same population, a hundred and twenty point "
            "four. <bookmark mark='b'/> As a simple random sample, its standard error would be point three three. "
            "<bookmark mark='c'/> By design, point five four, and the bootstrap agrees. <bookmark mark='d'/> A design effect of "
            "two point seven for the mean, but only about one point four for the slope. That's typical: whole clusters differ "
            "in their average pressure, perhaps through geography or income, but within-cluster differences, "
            "which drive a slope, are less affected. Cluster effects hurt means the most."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.75, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def silent(self):
        rows = fit_rows(VGroup(
            label(r"what the interval covers: \ the luck of which people were drawn", font_size=24, color=DES),
            label(r"what it says nothing about:", font_size=24),
            label(r"the noise in one day's recall \ (chapter eight)", font_size=24, color=SALT),
            label(r"who chooses to eat salt, \ and why \ (chapter nine)", font_size=24, color=TRUE),
            label(r"Part 11: \ an interval is only as honest as its assumptions", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One caution about all of these intervals. They measure one thing: the luck of which people "
            "the survey happened to draw. <bookmark mark='b'/> They say nothing about two other problems, which may be far "
            "larger. <bookmark mark='c'/> One is the noise in a single day's recall, which biases the slope rather than just "
            "spreading it. <bookmark mark='d'/> The other is who eats salt, and why. <bookmark mark='e'/> As Part 11 put it, an "
            "interval is only as honest as its assumptions, and the next two chapters examine those."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
