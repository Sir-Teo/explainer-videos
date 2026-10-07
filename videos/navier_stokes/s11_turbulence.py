from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from explainer.fluids import colormaps as cm
from videos.navier_stokes.common import FieldMovie, frame_rect, label, square_movie
from videos.navier_stokes.simulate import load


def kh_movie(width=13.4, **kwargs) -> FieldMovie:
    """Kelvin–Helmholtz roll-up, tiled twice horizontally (the domain is periodic)."""
    data = load("kh")
    vort, dye = data["vorticity"], data["dye"]
    n = vort.shape[1]
    y0, y1 = int(0.11 * n), int(0.89 * n)

    def render(k):
        w = np.asarray(vort[k], dtype=np.float32)[y0:y1]
        c = np.asarray(dye[k], dtype=np.float32)[y0:y1]
        base = cm.sequential(c, 0, 1, low=BACKGROUND, high="#2C6E91")
        rgb = 0.55 * base + 0.6 * cm.diverging(w, 10.0)
        rgb = np.concatenate([rgb, rgb], axis=1)[::-1]
        return cm.to_uint8(rgb)

    movie = FieldMovie(render, len(vort), loop=False, **kwargs)
    movie.width = width
    return movie


def eddy(radius, color=C.VELOCITY, stroke=3):
    arc = Arc(radius=radius, start_angle=0, angle=1.6 * PI, color=color, stroke_width=stroke)
    arc.add_tip(tip_length=max(0.08, 0.35 * radius), tip_width=max(0.08, 0.35 * radius))
    inner = Arc(radius=0.55 * radius, start_angle=PI, angle=1.4 * PI, color=color, stroke_width=stroke * 0.8)
    return VGroup(arc, inner)


class Turbulence(VoiceoverScene):
    def construct(self):
        self.kelvin_helmholtz()
        self.cascade()
        self.two_d()

    # ------------------------------------------------------------------
    def kelvin_helmholtz(self):
        movie = kh_movie(width=13.4, alpha=0.0)
        movie.rate = 0.0
        movie.move_to(DOWN * 0.3)
        border = frame_rect(movie)
        H = movie.height
        arrows = VGroup()
        for frac, sign in ((0.18, -1), (0.5, 1), (0.82, -1)):
            y = movie.get_bottom()[1] + frac * H
            for x in (-4.5, 0, 4.5):
                arrows.add(Arrow([x - 0.8 * sign, y, 0], [x + 0.8 * sign, y, 0], buff=0, color=WHITE, stroke_width=6))
        title = label(r"Kelvin--Helmholtz instability", font_size=40).to_edge(UP, buff=0.35)

        with self.voiceover(
            "Where does all that complexity come from? Here's a clue. Start with a simple layered flow: "
            "<bookmark mark='m'/> the middle band moves to the right, and the outer bands move to the left."
        ) as vo:
            self.add(movie)
            self.play(movie.fade(1.0), Create(border))
            vo.wait_until("m")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08))

        with self.voiceover(
            "Along each interface, tiny ripples get amplified by the nonlinear term, and the shear layers roll up into chains "
            "of spiraling vortices. <bookmark mark='kh'/> This is the Kelvin–Helmholtz instability, the same mechanism that "
            "sculpts those rare clouds shaped like breaking ocean waves."
        ) as vo:
            self.play(FadeOut(arrows))
            movie.rate = 1.0
            vo.wait_until("kh")
            self.play(Write(title))

        with self.voiceover(
            "Then the vortices themselves start to interact, pairing up and merging, and the orderly picture dissolves."
        ) as vo:
            pass
        left = (movie.n_frames - 1) / movie.fps - movie.t
        if left > 0:
            self.wait(left)
        self.play(movie.fade(0.0), FadeOut(VGroup(border, title)))
        self.remove(movie)

    # ------------------------------------------------------------------
    def cascade(self):
        levels = [(1, 1.0, -5.4), (2, 0.55, -2.9), (4, 0.3, -0.9), (8, 0.15, 0.75), (16, 0.075, 1.95)]
        groups = VGroup()
        top, bottom = 2.7, -0.2
        for n, r, x in levels:
            g = VGroup()
            for i in range(n):
                y = top - (i + 0.5) * (top - bottom) / n
                e = eddy(r, stroke=3 if r > 0.2 else 2).move_to([x, y, 0])
                e.rotate(i * 1.3)
                g.add(e)
            groups.add(g)
        for k, g in enumerate(groups):
            rate = 0.6 * (1 + k)
            for e in g:
                e.add_updater(lambda m, dt, rate=rate: m.rotate(rate * dt))
        heat = VGroup(*[
            FunctionGraph(lambda t, ph=ph: 0.08 * np.sin(14 * t + ph), x_range=[0, 1.5], color=RED_B, stroke_width=2).shift([3.0, y, 0])
            for ph, y in zip(range(8), np.linspace(top - 0.2, bottom + 0.2, 8))
        ])
        heat_l = label(r"viscosity:\\heat", font_size=28, color=C.VISCOUS).next_to(heat, RIGHT, buff=0.25)
        energy = Arrow([-6.2, 3.35, 0], [3.8, 3.35, 0], buff=0, color=YELLOW, stroke_width=4)
        energy_l = label(r"energy flows to smaller and smaller scales", font_size=28, color=YELLOW).next_to(energy, UP, buff=0.08)

        with self.voiceover(
            "In a turbulent flow, this kind of thing happens at every scale at once. <bookmark mark='b'/> Large swirls stretch, fold, "
            "and break into smaller swirls, which break into smaller ones still, <bookmark mark='v'/> until the eddies are so tiny "
            "that viscosity finally smooths them away, turning their energy into heat."
        ) as vo:
            self.play(FadeIn(groups[0], scale=0.6))
            vo.wait_until("b")
            self.play(GrowArrow(energy), FadeIn(energy_l))
            for g in groups[1:]:
                self.play(FadeIn(g, lag_ratio=0.1, scale=0.6), run_time=0.9)
            vo.wait_until("v")
            self.play(Create(heat), FadeIn(heat_l))

        poem = VGroup(
            label(r"\emph{Big whorls have little whorls}", font_size=36),
            label(r"\emph{that feed on their velocity;}", font_size=36),
            label(r"\emph{and little whorls have lesser whorls,}", font_size=36),
            label(r"\emph{and so on to viscosity.}", font_size=36),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 2.35)
        poem[3].set_color(C.VISCOUS)
        cite = label(r"--- Lewis Fry Richardson, 1922", font_size=26, color=C.DIM).next_to(poem, RIGHT, buff=0.4).align_to(poem, DOWN)
        with self.voiceover(
            "The physicist Lewis Fry Richardson put it as a poem: <bookmark mark='a'/> Big whorls have little whorls "
            "<bookmark mark='b'/> that feed on their velocity; <bookmark mark='c'/> and little whorls have lesser whorls, "
            "<bookmark mark='d'/> and so on to viscosity."
        ) as vo:
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(poem[i], shift=UP * 0.15), run_time=0.8)
            self.play(FadeIn(cite))
        self.wait(1.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two_d(self):
        movie = square_movie("turb", "vorticity", vmax=22.0, side=6.6, alpha=0.0, loop=False)
        movie.rate = 0.0
        movie.to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        border = frame_rect(movie)
        notes = VGroup(
            label(r"\textbf{3D turbulence}", font_size=34, color=C.ADVECT),
            label(r"big eddies break into smaller ones", font_size=30),
            label(r"\textbf{2D turbulence}", font_size=34, color=C.VELOCITY),
            label(r"small vortices \emph{merge} into bigger ones", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        notes[2].shift(DOWN * 0.4)
        notes[3].shift(DOWN * 0.4)
        notes.next_to(border, RIGHT, buff=0.6)
        title = label(r"2D turbulence", font_size=34).next_to(border, UP, buff=0.2)

        with self.voiceover(
            "That's the picture in three dimensions. But two dimensions, which is what all of these simulations are, "
            "behaves differently, in a surprising way. <bookmark mark='w'/> Watch this two-dimensional turbulent flow. "
            "<bookmark mark='m'/> Instead of shattering into ever-smaller eddies, the swirls tend to merge into larger and "
            "larger vortices."
        ) as vo:
            self.add(movie)
            self.play(FadeIn(notes[:2]))
            vo.wait_until("w")
            self.play(movie.fade(1.0), Create(border), FadeIn(title))
            movie.rate = 1.0
            vo.wait_until("m")
            self.play(FadeIn(notes[2:], shift=UP * 0.15))

        with self.voiceover(
            "That difference between two and three dimensions turns out to be at the heart of the deepest open question about "
            "these equations."
        ):
            pass
        left = (movie.n_frames - 1) / movie.fps - movie.t
        if left > 0:
            self.wait(min(left, 6.0))
        self.play(movie.fade(0.0), FadeOut(VGroup(border, notes, title)))
        self.remove(movie)
