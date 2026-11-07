from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats22.common import *  # noqa: F403


def geodesic(m1, m2, s0, k=60):
    """The Fisher-metric geodesic between N(m1, s0^2) and N(m2, s0^2): in (mu / sqrt 2, sigma) the metric is
    hyperbolic, so the geodesic is a semicircle centred on the sigma = 0 axis."""
    u1, u2 = m1 / np.sqrt(2), m2 / np.sqrt(2)
    c = (u1 + u2) / 2
    r = np.hypot(u2 - c, s0)
    t0, t1 = np.arctan2(s0, u1 - c), np.arctan2(s0, u2 - c)
    t = np.linspace(t0, t1, k)
    return np.sqrt(2) * (c + r * np.cos(t)), r * np.sin(t)


def fisher_length(mu, sg):
    dm, ds = np.diff(mu), np.diff(sg)
    s = (sg[1:] + sg[:-1]) / 2
    return float(np.sum(np.sqrt(dm ** 2 + 2 * ds ** 2) / s))


class Geometry(VoiceoverScene):
    def construct(self):
        self.card()
        self.metric()
        self.ellipses()
        self.path()
        self.natural()
        self.jeffreys()

    def card(self):
        card = chapter_card(13, r"Information geometry, \ a glimpse", r"Distance measured in standard errors", lit=(1945,), part=PART)
        with self.voiceover("Chapter thirteen. Information geometry, a glimpse."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def metric(self):
        rows = [
            cmath(r"\mathrm{KL}(f_\theta \,\|\, f_{\theta + d\theta})", r"\approx", r"\tfrac12\, d\theta^{\top} I(\theta)\, d\theta", font_size=30),
            cmath(r"ds^2", r"=", r"d\theta^{\top} I(\theta)\, d\theta", font_size=32),
            cmath(r"N(\mu, \sigma^2)", r":", r"ds^2 = (d\mu^2 + 2\, d\sigma^2)/\sigma^2", font_size=30),
            cmath(r"\text{invariant}", r":", r"\text{the same distances in any parametrization}", font_size=28),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"chapter two's KL, \ to second order"), why(r"Rao (1945): \ the Fisher metric"),
                why(r"$I = \mathrm{diag}(1/\sigma^2, \, 2/\sigma^2)$"), why(r"it measures distributions, \ not coordinates")]
        intro = label('Fisher information gives a local metric on distributions', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The Kullback–Leibler divergence between two nearby members of a family is, to second order, "
            "half a quadratic form in the information matrix. <bookmark mark='b'/> C. R. Rao took that seriously in 1945: "
            "use the information as a metric, a ruler that varies from place to place, so the family of distributions "
            "becomes a curved space. <bookmark mark='c'/> For the normal family, the squared length of a small step is d mu "
            "squared plus two d sigma squared, all over sigma squared. <bookmark mark='d'/> Because it's built from the "
            "distributions themselves, these distances don't depend on how we label the parameters."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def plane(self):
        A = axes([-3, 3], [0, 2.4], x_length=8.4, y_length=4.6, xlabel=r"mean $\mu$", ylabel=r"SD $\sigma$",
                 xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[0, 0.5, 1, 1.5, 2], center=[-1.4, 0.2, 0])
        return A, A.ax

    def ellipses(self):
        A, ax = self.plane()
        ux = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        uy = ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1]
        ell = VGroup()
        r = 0.22  # a fixed Fisher distance
        for s in (0.3, 0.7, 1.2, 1.8):
            for m in np.arange(-2.5, 2.6, 1.0 if s < 1 else 1.25):
                e = Ellipse(width=2 * r * s * ux, height=2 * r * s / np.sqrt(2) * uy, stroke_color=PATH, stroke_width=2,
                            fill_color=PATH, fill_opacity=0.15).move_to(ax.c2p(m, s))
                ell.add(e)
        rows = fit_rows(VGroup(
            label(r"each ellipse: \ a local Fisher-metric approximation", font_size=22, color=PATH),
            label(r"equally hard to tell apart", font_size=22),
            label(r"small $\sigma$: \ tiny ellipses, \ easy to tell", font_size=22, color=GREY_A),
            label(r"large $\sigma$: \ big ellipses", font_size=22, color=GREY_A),
            label(r"the hyperbolic plane, \ in disguise", font_size=22, color=TEAL),
        ), 3.3, 0.42, [5.2, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the normal family as a plane: mean across, standard deviation up. Each gold "
            "ellipse approximates a small ball in the local Fisher metric at its centre, <bookmark mark='b'/> the "
            "ones equally hard to tell apart from it with a fixed amount of data. <bookmark mark='c'/> Near the "
            "bottom, narrow normals, the ellipses are tiny: move the mean a little and the difference is obvious. "
            "<bookmark mark='d'/> Higher up, wide normals, they're large. <bookmark mark='e'/> With the mean rescaled"
            " by root two, this is exactly the hyperbolic plane of non-Euclidean geometry."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(e) for e in ell], lag_ratio=0.05), FadeIn(rows[0]), run_time=2.0)
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def path(self):
        A, ax = self.plane()
        mu, sg = geodesic(-2.0, 2.0, 0.4)
        geo = polyline(ax, mu, sg, PATH, 4)
        line = DashedLine(ax.c2p(-2, 0.4), ax.c2p(2, 0.4), color=GREY_B, stroke_width=2.5)
        ends = VGroup(Dot(ax.c2p(-2, 0.4), radius=0.08, color=CRAB1), Dot(ax.c2p(2, 0.4), radius=0.08, color=CRAB2))
        Lg = fisher_length(mu, sg)
        lm = np.linspace(-2, 2, 200)
        Ll = fisher_length(lm, np.full_like(lm, 0.4))
        # a small inset of the densities along the geodesic
        B = axes([-4.5, 4.5], [0, 1.05], x_length=3.0, y_length=1.5, xticks=[], yticks=[], center=[5.0, -2.2, 0])
        gx = np.linspace(-4.5, 4.5, 200)
        idx = [0, 15, 30, 45, 59]
        cols = [CRAB1, TEAL, PATH, TEAL, CRAB2]
        dens = VGroup(*[curve(B.ax, gx, stats.norm.pdf(gx, mu[i], sg[i]), c, 2.5) for i, c in zip(idx, cols)])
        rows = fit_rows(VGroup(
            label(r"from $N(-2, 0.4^2)$ to $N(2, 0.4^2)$", font_size=22),
            label(rf"dashed: \ slide the mean: \ length {Ll:.1f}", font_size=22, color=GREY_B),
            label(rf"gold: \ the geodesic: \ length {Lg:.1f}", font_size=22, color=PATH),
            label(r"the shortest way: \ widen, \ move, \ narrow", font_size=22, color=TEAL),
        ), 3.3, 0.42, [5.2, 1.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Curved spaces have curved shortest paths. Go from a narrow normal centred at minus two to the "
            "same normal centred at plus two. <bookmark mark='b'/> Sliding the mean straight across has Fisher length ten. "
            "<bookmark mark='c'/> The geodesic, the shortest path in this metric, is an arc, and its length is only about "
            "five point six. <bookmark mark='d'/> It first widens the distribution, moves it while it's wide and the move is "
            "cheap, then narrows it again: the densities in the inset."
        ) as vo:
            self.play(FadeIn(A), FadeIn(ends))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(geo), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(B), LaggedStart(*[Create(c) for c in dens], lag_ratio=0.3), FadeIn(rows[3]))
        self.clear_scene()

    def natural(self):
        rows = [
            cmath(r"\text{gradient}", r":", r"\theta \leftarrow \theta + \eta\, \nabla \ell_n(\theta)", font_size=30),
            cmath(r"\text{natural gradient}", r":", r"\theta \leftarrow \theta + \eta\, \big(nI(\theta)\big)^{-1} \nabla \ell_n(\theta)", font_size=30),
            cmath(r"\eta = 1", r":", r"\text{Fisher scoring, \ Part 21}", font_size=30),
            cmath(r"\text{today}", r":", r"\text{K-FAC, \ trust regions; \ variational inference}", font_size=28),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"steepest in the coordinates: \ not invariant"), why(r"Amari (1998): \ steepest in the metric"),
                why(r"the natural gradient is an old friend"), why(r"Parts 27 and 64")]
        intro = label('Scale the summed gradient by full-sample information', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The geometry pays off in optimization. The ordinary gradient points uphill in the "
            "coordinates we happened to choose; rescale a parameter and it points somewhere else. <bookmark "
            "mark='b'/> Shun-ichi Amari's natural gradient, from 1998, points uphill in the Fisher metric instead: "
            "multiply the gradient by the inverse information. <bookmark mark='c'/> Using the full-sample information"
            " n I with the summed log-likelihood gradient, a unit step is Fisher scoring from Part 21. The vector "
            "field transforms invariantly; a finite coordinate Euler step need not be exactly invariant under "
            "nonlinear reparametrization. <bookmark mark='d'/> Approximations to it train large neural networks and "
            "drive variational inference, which Parts 27 and 64 will meet."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def jeffreys(self):
        rows = [
            cmath(r"\text{volume}", r":", r"dV = \sqrt{\det I(\theta)}\, d\theta", font_size=30),
            cmath(r"\text{Jeffreys}", r":", r"\pi(\theta) \propto \sqrt{\det I(\theta)}", font_size=30),
            cmath(r"\text{binomial}", r":", r"\pi(p) \propto p^{-1/2}(1 - p)^{-1/2}", font_size=30),
            cmath(r"\text{normal}", r":", r"\pi(\mu, \sigma) \propto 1/\sigma^2", font_size=30),
        ]
        rows[1][2].set_color(PRIOR)
        whys = [why(r"the metric's area element"), why(r"Jeffreys (1946): \ uniform in the geometry"),
                why(r"Part 11's Jeffreys interval"), why(r"Part 26: \ priors from invariance")]
        intro = label('Jeffreys prior is the Fisher volume element', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> And it gives Bayesians a prior. A metric has a volume element, the square root of "
            "the determinant of the information. <bookmark mark='b'/> Harold Jeffreys proposed in 1946 to use it as a"
            " prior: spread belief evenly in the geometry, not in an arbitrary parametrization, so the answer doesn't"
            " depend on the parametrization. <bookmark mark='c'/> For a binomial proportion it's the beta of one "
            "half, one half, behind Part 11's Jeffreys interval. <bookmark mark='d'/> For the joint normal mean and "
            "standard deviation, its density with respect to d mu d sigma is one over sigma squared. This prior is "
            "improper, and posterior propriety must be checked. Part 26 takes up priors in earnest."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
