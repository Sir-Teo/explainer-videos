from __future__ import annotations

import numpy as np

from videos.stats.stats39.common import *  # noqa: F403


def panel(vals, center, title, color):
    v = np.asarray(vals, float)
    ny, nx = v.shape
    X, Y = np.meshgrid(np.arange(nx) * 0.1, np.arange(ny) * 0.1)
    F = FieldSurface(X.ravel(), Y.ravel(), v.ravel(), 0.1, width=4.2, center=center, lo=-2.5, hi=2.5)
    t = label(title, font_size=22, color=color).next_to(F, UP, buff=0.1)
    return VGroup(F, t)


class Fields(VoiceoverScene):
    def construct(self):
        self.card()
        self.definitions()
        self.bochner()
        self.gallery()
        self.families()

    def card(self):
        card = chapter_card(2, r"Random fields", r"Which functions can be covariances?", lit=(1960,), part=PART)
        with self.voiceover("Chapter two. Random fields."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definitions(self):
        rows = [
            cmath(r"\text{stationary}", r":", r"E\,W(s) = 0, \ \ \text{Cov}(W(s), W(s + h)) = C(h) \ \text{for all } s", font_size=30),
            cmath(r"\text{isotropic}", r":", r"C(h) = C(\|h\|): \ \text{only distance matters}", font_size=30),
            cmath(r"\text{Gaussian}", r":", r"\text{every finite set of values is jointly normal}", font_size=30),
            cmath(r"\text{one realization}", r":", r"\text{one island, \ one field: \ ergodicity again}", font_size=30),
        ]
        rows[1][-1].set_color(FIELDC)
        whys = [why(r"second-order stationarity"), why(r"no direction is special"), why(r"so the covariance is everything"),
                why(r"Part 38")]
        with self.voiceover(
            "<bookmark mark='a'/> A random field assigns a random variable to every point of a region. It is stationary if "
            "its mean is constant and the covariance between two points depends only on the displacement between them. "
            "<bookmark mark='b'/> It is isotropic if only the distance matters, not the direction. <bookmark mark='c'/> And "
            "it is Gaussian if every finite collection of its values is jointly normal, so that the covariance function "
            "says everything. <bookmark mark='d'/> As in Part thirty-eight, we usually see only one realization: one "
            "island, one field. Learning its covariance from that single copy relies on ergodicity again."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bochner(self):
        rows = [
            cmath(r"\text{valid } C", r":", r"\textstyle\sum_{ij} a_i a_j C(s_i - s_j) \ge 0 \ \text{for all } a, s", font_size=30),
            cmath(r"\text{Bochner (1933)}", r":", r"C(h) = \int e^{i \omega^\top h}\, dF(\omega), \ \ F \ge 0", font_size=30),
            cmath(r"\text{so}", r":", r"\text{a covariance is a spectrum: \ Part 38's Herglotz, \ in } d \text{ dimensions}", font_size=30),
            cmath(r"\text{e.g.}", r":", r"\text{a triangle } C(h) = (1 - |h|)_+ \text{ is valid in one dimension, \ not in three}", font_size=28),
        ]
        rows[1][-1].set_color(FIELDC)
        whys = [why(r"every variance must be non-negative"), why(r"positive definite iff a non-negative spectrum"),
                why(r"the same theorem"), why(r"validity depends on the dimension")]
        with self.voiceover(
            "<bookmark mark='a'/> Not every function can be a covariance. Every linear combination of the field's values "
            "must have a non-negative variance, so the covariance must be positive definite. <bookmark mark='b'/> Salomon "
            "Bochner's theorem of 1933 characterizes such functions: exactly the Fourier transforms of non-negative "
            "measures, the spectra. <bookmark mark='c'/> It is Part thirty-eight's Herglotz theorem, in any number of "
            "dimensions. <bookmark mark='d'/> A consequence that surprises people: whether a function is a valid covariance "
            "can depend on the dimension. A triangle is a valid covariance on a line but not in space. So geostatistics "
            "works with families known to be valid."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gallery(self):
        d = load("fields")
        p0 = panel(d["0.5"], [-3.0, 1.45, 0], r"$\nu = 1/2$ \ (exponential): \ rough", FIELDC)
        p1 = panel(d["1.5"], [2.4, 1.45, 0], r"$\nu = 3/2$: \ once differentiable", TAUC)
        p2 = panel(d["2.5"], [-3.0, -1.95, 0], r"$\nu = 5/2$: \ twice", BANDC)
        p3 = panel(d["short"], [2.4, -1.95, 0], r"$\nu = 3/2$, \ range a third as long", PTC)
        with self.voiceover(
            "<bookmark mark='a'/> Four fields drawn from the same random numbers with different covariances. With an "
            "exponential covariance, the field is continuous but rough, like a random walk in every direction. <bookmark "
            "mark='b'/> With the Matérn covariance of smoothness three halves, it is once differentiable. <bookmark "
            "mark='c'/> With five halves, twice: smoother still. <bookmark mark='d'/> And with the same smoothness but a "
            "range a third as long, the same kind of surface, but its hills and valleys are three times closer together. "
            "Smoothness and range are different properties, and the covariance must describe both."
        ) as vo:
            self.add(seeded_tag())
            for p, m_ in zip((p0, p1, p2, p3), "abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(p))
        self.clear_scene()

    def families(self):
        rows = [
            cmath(r"\text{exponential}", r":", r"C(h) = \sigma^2 e^{-h/\rho}", font_size=30),
            cmath(r"\text{Gaussian}", r":", r"C(h) = \sigma^2 e^{-h^2/\rho^2} \ \text{(infinitely smooth: \ unrealistic)}", font_size=30),
            cmath(r"\text{spherical}", r":", r"\text{zero beyond the range: \ Matheron's favourite}", font_size=30),
            cmath(r"\text{Mat\'ern}", r":", r"\sigma^2 \tfrac{2^{1-\nu}}{\Gamma(\nu)} (\sqrt{2\nu}\, h/\rho)^\nu K_\nu(\sqrt{2\nu}\, h/\rho)", font_size=28),
        ]
        rows[3][-1].set_color(TAUC)
        whys = [why(r"$\nu = 1/2$"), why(r"$\nu \to \infty$"), why(r"compact support"), why(r"Mat\'ern (1960): \ chapter 5")]
        with self.voiceover(
            "<bookmark mark='a'/> The standard families. The exponential, rough. <bookmark mark='b'/> The Gaussian, which "
            "makes the field infinitely differentiable, smoother than anything in nature, and which Michael Stein warned "
            "should rarely be used. <bookmark mark='c'/> The spherical, which drops to exactly zero beyond its range, and "
            "was Matheron's favourite. <bookmark mark='d'/> And the Matérn family, which contains the exponential and the "
            "Gaussian as special cases and has a parameter for smoothness: the subject of chapter five."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
