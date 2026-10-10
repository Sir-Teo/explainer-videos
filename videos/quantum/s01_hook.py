from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum.common import (BlochSphere, FieldMovie2D, Projector, Raster, WaveView, bloch_vector, corner_wheel,
                                   glow, label, load, mtex, note, orbital_image, splat, wave_axes)
from videos.quantum.compute import SLIT, TONOMURA


class Hook(VoiceoverScene):
    def construct(self):
        self.dots()
        self.wave()
        self.equation()
        self.roadmap()

    # ------------------------------------------------------------------
    def dots(self):
        s = load("slits")
        ey, ez = s["ev_y"], s["ev_z"]
        W, H = 9.0, 5.6
        ext = (-260.0, 260.0, -1.0, 1.0)
        shape = (360, 580)
        n = ValueTracker(0.0)

        def draw(v):
            k = int(v)
            if k == 0:
                return np.zeros(shape + (4,), np.uint8)
            sig = 2.2 if k < 300 else (1.6 if k < 5000 else 1.2)
            gain = 1.6 if k < 5000 else 1.6 * (5000 / k) ** 0.8  # keep the bright bands from saturating as dots pile up
            return glow(splat(ey[:k], ez[:k], ext, shape, sigma=sig), C.BORN, gain=gain)

        plate = Raster(draw, n, W, H, center=DOWN * 0.15)
        frame = Rectangle(width=W, height=H, stroke_color=GREY_C, stroke_width=1.5).move_to(plate)
        cnt = always_redraw(lambda: MathTex(f"{int(n.get_value()):,}".replace(",", "{,}") + r"\ \text{electrons}", font_size=34)
                            .next_to(frame, UP, buff=0.18))
        tag = note(r"simulated detections, at the five counts in Tonomura et al.\ (1989)").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Fire electrons, one at a time, at a barrier with two narrow openings, and record where each one lands on a "
            "screen behind it. <bookmark mark='a'/> Each electron arrives as a single, sharp dot, at a place nobody can "
            "predict. <bookmark mark='b'/> Ten electrons look like random noise. <bookmark mark='c'/> A hundred, still "
            "noise."
        ) as vo:
            self.play(Create(frame), FadeIn(tag))
            self.add(plate, cnt)
            vo.wait_until("a")
            self.play(n.animate.set_value(3), run_time=1.5, rate_func=linear)
            vo.wait_until("b")
            self.play(n.animate.set_value(TONOMURA[0]), run_time=1.0, rate_func=linear)
            vo.wait_until("c")
            self.play(n.animate.set_value(TONOMURA[1]), run_time=1.5, rate_func=linear)
        with self.voiceover(
            "<bookmark mark='d'/> But by three thousand, a pattern is appearing, <bookmark mark='e'/> and by seventy "
            "thousand it's unmistakable: stripes. Bright bands where many electrons land, dark bands where almost none "
            "ever do. That's an interference pattern, the signature of a wave. Akira Tonomura's team at Hitachi recorded "
            "this buildup in 1989, one electron at a time, at these same five counts, using an electron biprism, the "
            "electron version of two slits."
        ) as vo:
            vo.wait_until("d")
            self.play(n.animate.set_value(TONOMURA[2]), run_time=2.0, rate_func=lambda a: a**1.5)
            vo.wait_until("e")
            self.play(n.animate.set_value(TONOMURA[3]), run_time=1.5, rate_func=linear)
            self.play(n.animate.set_value(TONOMURA[4]), run_time=2.0, rate_func=linear)
        plate.clear_updaters()
        cnt.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def wave(self):
        s = load("slits")
        y, P12 = s["y"], s["P12"]
        p = SLIT
        t = ValueTracker(0.0)
        mv = FieldMovie2D(t, width=9.6, boost=2.0, vmax=7e-3, gamma=0.6)
        mv.move_to(LEFT * 1.6 + DOWN * 0.1)
        # the slit plate drawn on top, to scale
        half = p["w"] / 2
        a = p["d"] / 2
        segs = [(p["crop_y"][0], -a - half), (-a + half, a - half), (a + half, p["crop_y"][1])]
        plate = VGroup()
        for y0, y1 in segs:
            p0 = mv.sim_to_screen(p["wall"][0], y0)
            p1 = mv.sim_to_screen(p["wall"][1] + 2, y1)
            plate.add(Rectangle(width=max(abs(p1[0] - p0[0]), 0.06), height=abs(p1[1] - p0[1]), stroke_width=0, fill_color=C.WALL,
                                fill_opacity=1).move_to((p0 + p1) / 2))
        sx = mv.sim_to_screen(p["screen"], 0)[0]
        screen = Line([sx, mv.get_bottom()[1], 0], [sx, mv.get_top()[1], 0], color=GREY_A, stroke_width=2.5)
        # the arrival density, growing as the wave reaches the screen
        keep = (y >= p["crop_y"][0]) & (y <= p["crop_y"][1])
        yy, PP = y[keep], P12[keep]
        right = mv.get_right()[0] + 0.15
        scale = 2.6 / PP.max()

        def dens():
            f = np.clip((t.get_value() - 700) / 600, 0, 1)
            f = f * f * (3 - 2 * f)
            pts = [[right + scale * f * v, mv.sim_to_screen(0, yv)[1], 0] for yv, v in zip(yy, PP)]
            m = VMobject(stroke_color=C.BORN, stroke_width=3)
            m.set_points_as_corners(pts)
            return m

        dc = always_redraw(dens)
        base = Line([right, mv.get_bottom()[1], 0], [right, mv.get_top()[1], 0], color=GREY_C, stroke_width=1.5)
        dl = MathTex(r"|\psi|^2 \text{ at the screen}", font_size=26, color=C.BORN).next_to(base, UP, buff=0.1).shift(RIGHT * 1.2)
        dl.shift(DOWN * max(0.0, dl.get_top()[1] - 3.8))  # keep it off the frame edge
        wheel = corner_wheel(corner=UL, buff=0.25, radius=0.3)
        tag = note(r"simulated: the Schr\"odinger equation on a $1024 \times 1024$ grid; color = phase, brightness = "
                   r"$|\psi|$ ($\times 2$ right of the slits)").to_edge(DOWN, buff=0.15)
        tag.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.06).set_z_index(10)  # the walls run behind it
        with self.voiceover(
            "So what goes through the slits? Here's the answer quantum mechanics gives, computed by solving its central "
            "equation numerically. <bookmark mark='w'/> Before detection, the electron is described by a wave, a "
            "complex number at every point in space; the color shows its phase, the brightness its size. "
            "<bookmark mark='s'/> The wave reaches the barrier, and part of it passes through both openings at once. "
            "<bookmark mark='i'/> The two halves spread out and overlap, and where they meet, they interfere."
        ) as vo:
            self.add(mv)
            self.play(FadeIn(mv), FadeIn(plate), FadeIn(wheel), FadeIn(tag), Create(screen), Create(base))
            vo.wait_until("w")
            self.play(t.animate.set_value(260), run_time=max(0.5, vo.mark_time("s") - vo.elapsed()), rate_func=linear)
            self.play(t.animate.set_value(520), run_time=max(1.0, vo.mark_time("i") - vo.elapsed()), rate_func=linear)
            self.add(dc)
            self.play(t.animate.set_value(860), FadeIn(dl), run_time=vo.remaining(), rate_func=linear)
        with self.voiceover(
            "When the wave reaches the screen, the electron is found at a single point, at random, and the probability "
            "of each point is the size of the wave there, squared. <bookmark mark='r'/> Do it seventy thousand times and "
            "you get the stripes. The wave is never seen directly; it's what decides the odds."
        ) as vo:
            self.play(t.animate.set_value(1300), run_time=max(0.5, vo.mark_time("r") - vo.elapsed() + 1.5), rate_func=linear)
            self.play(t.animate.set_value(1490), run_time=max(0.5, vo.remaining()), rate_func=linear)
        for m in (mv, dc):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def equation(self):
        se = MathTex(r"i\hbar\,\frac{\partial\psi}{\partial t}", r"=", r"-\frac{\hbar^2}{2m}\nabla^2\psi", r"+", r"V\psi", font_size=64)
        se[0].set_color(C.ENERGY)
        se[2].set_color(C.MOMENTUM)
        se[4].set_color(C.POTENTIAL)
        se.move_to(UP * 0.6)
        name = label(r"Erwin Schr\"odinger, \emph{Annalen der Physik}, 1926", font_size=30, color=GREY_A).next_to(se, DOWN, buff=0.5)
        cen = label(r"a hundred years old this year", font_size=30, color=C.BORN).next_to(name, DOWN, buff=0.25)
        born = label(r"and Max Born's rule, the same year: probability $= |\psi|^2$", font_size=28).next_to(cen, DOWN, buff=0.5)
        with self.voiceover(
            "The wave obeys one equation. <bookmark mark='e'/> Erwin Schrödinger published it in a series of papers in "
            "1926, <bookmark mark='c'/> a hundred years ago this year, <bookmark mark='b'/> and that same year Max Born "
            "proposed what the wave means: the probability of finding the particle is the size of psi, squared. "
            "Everything you just watched follows from these two ideas."
        ) as vo:
            vo.wait_until("e")
            self.play(Write(se), run_time=2.5)
            self.play(FadeIn(name))
            vo.wait_until("c")
            self.play(FadeIn(cen))
            vo.wait_until("b")
            self.play(FadeIn(born))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def roadmap(self):
        items = [
            (r"1.\ Amplitudes", r"arrows that add"),
            (r"2.\ The Schr\"odinger equation", r"waves, boxes, carpets, tunneling"),
            (r"3.\ The mathematical framework", r"vectors, operators, $[\hat x, \hat p] = i\hbar$, uncertainty"),
            (r"4.\ Two solvable worlds", r"the oscillator and the hydrogen atom"),
            (r"5.\ Spin and entanglement", r"the Bloch sphere and Bell's theorem"),
        ]
        rows = VGroup(*[VGroup(label(a, font_size=34), label(b, font_size=26, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
                        for a, b in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        thumb = orbital_image("orb_321", 2.4)
        thumb.to_edge(RIGHT, buff=1.0).shift(UP * 1.4)
        proj = Projector(az=-0.5, el=0.3, scale=1.0, center=RIGHT * 4.6 + DOWN * 1.8)
        bs = BlochSphere(proj, radius=1.1, labels=False)
        arr = bs.arrow(bloch_vector(0.9, 0.7), stroke_width=4)
        prereq = note(r"you'll need: complex numbers, calculus, a little linear algebra. Every result is derived on "
                      r"screen; every picture is computed.").to_edge(DOWN, buff=0.3)
        plan = label(r"The plan", font_size=44, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "In this video we'll build quantum mechanics from the ground up, with the mathematics on screen at every "
            "step. <bookmark mark='a'/> First, amplitudes: why probabilities don't add, but complex arrows do. "
            "<bookmark mark='b'/> Then the Schrödinger equation itself: where it comes from, and what it does to wave "
            "packets, particles in boxes, and barriers. <bookmark mark='c'/> Then the mathematical framework: states as "
            "vectors, observables as operators, the commutator of position and momentum, and the uncertainty principle, "
            "derived. <bookmark mark='d'/> Then two worlds we can solve exactly: the harmonic oscillator and the "
            "hydrogen atom. <bookmark mark='e'/> And finally spin and entanglement, ending with Bell's theorem. All you "
            "need is complex numbers, calculus and a little linear algebra."
        ) as vo:
            self.play(FadeIn(plan))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                anims = [FadeIn(r, shift=RIGHT * 0.2)]
                if m == "d":
                    anims.append(FadeIn(thumb))
                if m == "e":
                    anims += [FadeIn(bs), GrowArrow(arr)]
                self.play(*anims)
            self.play(FadeIn(prereq))
        self.wait(0.5)
        self.clear_scene()
