from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2 import spacetime as st
from videos.relativity2.common import (Chart, KerrShader, Raster, bh_screen_scale, boxed, label, load, mtex, note,
                                       part_card, polyline, shadow_outline, zigzag)
from videos.relativity2.compute import L_SUN, T_SUN


class Hook(VoiceoverScene):
    def construct(self):
        self.opening()
        self.recap()
        self.roadmap()
        self.units()

    # ------------------------------------------------------------------
    def opening(self):
        d = load("kerr80")
        assert int(d["mismatch"]) == 0 and abs(float(d["a"]) - 0.99) < 1e-9
        sh = KerrShader(d)
        t = ValueTracker(0.0)
        W = 14.22
        img = Raster(lambda v: sh(v), t, W, W * 720 / 1280, center=ORIGIN, alpha=0.0)
        title = VGroup(label(r"General Relativity, Part 2", font_size=56),
                       label(r"horizons, spin, waves, and the universe", font_size=32, color=GREY_A)).arrange(DOWN, buff=0.2)
        title.to_edge(UP, buff=0.5)
        title.add_background_rectangle(color=BACKGROUND, opacity=0.6, buff=0.15)
        cred = note(r"ray-traced Kerr geometry, $a = 0.99M$, seen $80^\circ$ from the spin axis; disk colors illustrative")
        cred.to_corner(DR, buff=0.25)
        sc = bh_screen_scale(W)
        outline = shadow_outline(0.99, 80, ORIGIN, sc, color=C.CURVATURE, stroke_width=2.5)
        with self.voiceover(
            "This is a black hole that spins. It isn't an artist's impression. Every pixel is a ray of light, traced "
            "backward from the camera through the geometry of a rotating black hole, the solution Roy Kerr found in "
            "1963, until it hits a thin disk of hot gas, falls in, or escapes to the distant stars. "
            "<bookmark mark='l'/> The gas on the left is coming toward us, so it's brighter and bluer. "
            "<bookmark mark='s'/> And the dark region, the shadow, is flattened on one side by the rotation, exactly as "
            "the theory predicts."
        ) as vo:
            self.add(img)
            self.play(img.fade(1.0), t.animate.set_value(15), run_time=2.0, rate_func=linear)
            self.play(FadeIn(title), FadeIn(cred), t.animate.set_value(60), run_time=vo.until("l"), rate_func=linear)
            self.play(FadeOut(title), t.animate.set_value(90), run_time=vo.until("s"), rate_func=linear)
            self.play(Create(outline), t.animate.set_value(110), run_time=2, rate_func=linear)
            self.play(t.animate.set_value(150), run_time=vo.remaining() + 0.5, rate_func=linear)
        img.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        eq = mtex(r"G_{\mu\nu}", r"=", r"\frac{8\pi G}{c^4}", r"\,T_{\mu\nu}", font_size=60)
        eq[0].set_color(C.CURVATURE)
        eq[3].set_color(C.MATTER)
        sw = mtex(r"ds^2", r"=", r"-\Big(1 - \frac{2GM}{rc^2}\Big)c^2dt^2", r"+", r"\frac{dr^2}{1 - \frac{2GM}{rc^2}}", r"+",
                  r"r^2\,d\Omega^2", font_size=44)
        sw[2].set_color(C.PROPER_TIME)
        sw[4].set_color(C.METRIC)
        g = VGroup(eq, sw).arrange(DOWN, buff=0.6).to_edge(UP, buff=0.5)
        part1 = label(r"Part 1: the field equations, derived; Schwarzschild; Mercury, light bending, waves", font_size=28,
                      color=GREY_A).next_to(g, DOWN, buff=0.4)
        bad = VGroup(
            label(r"at $r = 2GM/c^2$:", font_size=30),
            label(r"$g_{tt} \to 0$: a clock there stops, as seen from far away", font_size=28, color=C.PROPER_TIME),
            label(r"$g_{rr} \to \infty$: the coordinates break down", font_size=28, color=C.METRIC),
            label(r"inside, every future leads inward: a black hole", font_size=28, color=C.CURVATURE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(part1, DOWN, buff=0.45)
        circ = SurroundingRectangle(VGroup(sw[2], sw[4]), color=C.CURVATURE, buff=0.12, corner_radius=0.1)
        with self.voiceover(
            "In part one, we derived Einstein's field equation from scratch, and solved it outside a star. With that "
            "solution, we explained the orbit of Mercury and the bending of light, and we saw that ripples in spacetime "
            "travel at the speed of light. <bookmark mark='b'/> But we stopped at the edge of the most interesting "
            "place. At r equals two G M over c squared, the Schwarzschild metric misbehaves: a clock there stops, as "
            "seen from far away, and the radial part blows up. <bookmark mark='i'/> We claimed that inside, every "
            "future direction points inward. This time we'll make that precise, and go much further."
        ) as vo:
            self.play(Write(eq), run_time=1.5)
            self.play(Write(sw), FadeIn(part1), run_time=2)
            vo.wait_until("b")
            self.play(Create(circ), FadeIn(bad[:3], lag_ratio=0.3), run_time=2)
            vo.wait_until("i")
            self.play(FadeIn(bad[3]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def roadmap(self):
        rows = [
            ("I", r"Horizons and singularities", r"falling in; coordinates that see through the horizon; Penrose diagrams; "
                                                r"Raychaudhuri and the singularity theorem", C.CURVATURE),
            ("II", r"Spinning spacetime", r"gyroscopes and frame dragging; the Kerr solution; mining a black hole's spin; "
                                         r"shadows", C.SPIN),
            ("III", r"Gravitational waves, derived", r"the quadrupole formula; the chirp; the binary pulsar; ringdown and the "
                                                    r"area theorem", C.WAVE),
            ("IV", r"Black holes and quantum theory", r"the four laws of black-hole mechanics; Hawking radiation", C.TEMPERATURE),
            ("V", r"The universe", r"Friedmann's equations derived; redshift; horizons; the CMB", C.LAMBDA),
        ]
        items = VGroup()
        for num_, head, sub, col in rows:
            n = label(num_, font_size=40, color=col)
            h = label(head, font_size=34, color=col)
            s = label(sub, font_size=22, color=GREY_A)
            txt = VGroup(h, s).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            row = VGroup(n, txt).arrange(RIGHT, buff=0.4, aligned_edge=UP)
            n.set_width(0.55, stretch=False) if n.width > 0.55 else None
            items.add(row)
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(LEFT, buff=0.7)
        for it in items:  # line up the headings
            it[1].set_x(items[0][1].get_left()[0] + it[1].width / 2)
        with self.voiceover(
            "Here's the plan. <bookmark mark='a'/> First, we'll fall into a black hole, find coordinates that see "
            "through the horizon, draw the entire spacetime on a single page, and prove that singularities are "
            "unavoidable. <bookmark mark='b'/> Second, we'll make it spin: gyroscopes, the dragging of space, Kerr's "
            "solution, and how to mine energy from a black hole's rotation. <bookmark mark='c'/> Third, we'll derive "
            "what part one could only quote: the energy carried by gravitational waves, and the chirp of two black "
            "holes merging. <bookmark mark='d'/> Fourth, we'll find that black holes obey the laws of thermodynamics, "
            "and have a temperature. <bookmark mark='e'/> And finally, we'll apply Einstein's equation to the universe "
            "as a whole."
        ) as vo:
            for k, m in zip("abcde", items):
                vo.wait_until(k)
                self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.8)
        self.clear_scene()

    # ------------------------------------------------------------------
    def units(self):
        assert abs(L_SUN / 1000 - 1.477) < 0.001 and abs(T_SUN * 1e6 - 4.93) < 0.005
        g1 = mtex(r"G = c = 1", font_size=56)
        conv = VGroup(
            mtex(r"M_\odot", r"\;\to\;", r"\frac{GM_\odot}{c^2} = 1.477\ \text{km}", font_size=40),
            mtex(r"M_\odot", r"\;\to\;", r"\frac{GM_\odot}{c^3} = 4.93\ \mu\text{s}", font_size=40),
        ).arrange(DOWN, buff=0.3)
        for r in conv:
            r[0].set_color(C.MATTER)
        sw = mtex(r"ds^2", r"=", r"-\Big(1 - \frac{2M}{r}\Big)dt^2", r"+", r"\frac{dr^2}{1 - 2M/r}", r"+", r"r^2\,d\Omega^2",
                  font_size=46)
        sw[2].set_color(C.PROPER_TIME)
        sw[4].set_color(C.METRIC)
        rs = mtex(r"r_s = 2M", font_size=44, color=C.CURVATURE)
        g = VGroup(g1, conv, sw, rs).arrange(DOWN, buff=0.5)
        with self.voiceover(
            "One piece of bookkeeping first. <bookmark mark='a'/> From here on, we'll use units in which G and c are "
            "both equal to one, as relativists do. <bookmark mark='b'/> Then a mass is also a length, and also a time: "
            "the Sun's mass is one point four eight kilometers, or four point nine three microseconds. "
            "<bookmark mark='c'/> The Schwarzschild metric loses its clutter, <bookmark mark='d'/> and the Schwarzschild "
            "radius is simply two M."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(g1))
            vo.wait_until("b")
            self.play(FadeIn(conv, lag_ratio=0.3))
            vo.wait_until("c")
            self.play(Write(sw))
            vo.wait_until("d")
            self.play(FadeIn(rs))
        self.wait(0.5)
        self.clear_scene()
