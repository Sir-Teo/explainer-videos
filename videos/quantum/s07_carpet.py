from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum import colormap as qcm
from videos.quantum.common import (WaveView, bar_chart, boxed, corner_wheel, frames_at, label, load, mtex, note, num,
                                   phasor, stack, wave_axes, why)
from videos.quantum.compute import box_E
from videos.quantum.s06_box import walls


class Carpet(VoiceoverScene):
    def construct(self):
        self.setup_packet()
        self.breakup()
        self.weave()
        self.why_revival()

    # ------------------------------------------------------------------
    def setup_packet(self):
        c = load("carpet")
        x, mv, tm, ns, cs = c["x"], c["movie"], c["t_movie"], c["ns"], c["cs"]
        ax = wave_axes((-0.02, 1.02), (0, 7.5), x_length=6.0, y_length=2.8).move_to(LEFT * 3.4 + UP * 1.2)
        wv = WaveView(ax, x, mv[0], mode="density", x_window=(0, 1))
        wl = walls(ax)
        P = np.abs(cs) ** 2
        bax = Axes(x_range=[0, 21, 5], y_range=[0, 0.17, 0.05], x_length=5.2, y_length=2.6, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(RIGHT * 3.5 + UP * 1.2)
        bars = bar_chart(bax, ns[:20], P[:20], width=0.7, color=C.ENERGY)
        bl = MathTex(r"|c_n|^2", font_size=30, color=C.ENERGY).next_to(bax.y_axis.get_end(), UP, buff=0.1)
        nl = MathTex("n", font_size=30).next_to(bax.x_axis.get_end(), RIGHT, buff=0.1)
        exp = MathTex(r"\psi(x, t)", r"=", r"\sum_n c_n\,\varphi_n(x)\,e^{-iE_nt/\hbar}", font_size=38).move_to(DOWN * 1.0)
        rate = MathTex(r"E_n = n^2 E_1", font_size=34, color=C.ENERGY).next_to(exp, DOWN, buff=0.3)
        # the clocks
        t = ValueTracker(0.0)
        cen = [np.array([-5.6 + 1.6 * i, -3.0, 0]) for i in range(8)]
        rings = VGroup(*[Circle(radius=0.55, color=GREY_D, stroke_width=1.2).move_to(cc) for cc in cen])
        top = np.abs(cs[:8]).max()
        clocks = always_redraw(lambda: VGroup(*[phasor(cs[i] * np.exp(-1j * box_E(i + 1) * t.get_value()), origin=cen[i],
                                                        unit=0.53 / top, stroke_width=4, tip=0.12) for i in range(8)]))
        cl = VGroup(*[MathTex(f"n={i + 1}", font_size=22, color=GREY_B).next_to(rings[i], UP, buff=0.06) for i in range(8)])
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.26, labels=False, title=False)
        with self.voiceover(
            "Let's push that idea further. Put a narrow packet in the box, off center. <bookmark mark='c'/> Like any "
            "wavefunction in the box, it's a sum of the stationary states, with coefficients c n. Here are their sizes "
            "squared. <bookmark mark='e'/> Every term carries its own clock, <bookmark mark='r'/> and the clocks run "
            "at rates proportional to n squared: one, four, nine, sixteen, and so on."
        ) as vo:
            self.play(Create(ax), FadeIn(wl), FadeIn(wv), FadeIn(wheel))
            vo.wait_until("c")
            self.play(Create(bax), FadeIn(bl), FadeIn(nl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05))
            vo.wait_until("e")
            self.play(Write(exp), FadeIn(rate))
            vo.wait_until("r")
            self.play(FadeIn(rings), FadeIn(clocks), FadeIn(cl))
            self.play(t.animate.set_value(0.25), run_time=vo.remaining() + 1.0, rate_func=linear)
        clocks.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def breakup(self):
        c = load("carpet")
        x, mv, tm, T = c["x"], c["early"], c["t_early"], float(c["T_rev"][0])
        t = ValueTracker(0.0)
        ax = wave_axes((-0.02, 1.02), (0, 7.5), x_length=11, y_length=4.2).shift(DOWN * 0.4)
        wv = WaveView(ax, x, mv[0], mode="density", x_window=(0, 1)).follow(t, frames_at(tm, mv))
        wl = walls(ax)
        clock = always_redraw(lambda: MathTex(r"t = " + f"{t.get_value() / T:.3f}" + r"\,T", font_size=34, color=C.QTIME)
                              .to_corner(UR, buff=0.5))
        wheel = corner_wheel(corner=UL, buff=0.3, radius=0.3)
        sim = note(r"exact eigen-expansion, $300$ terms").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Give it a push to the right and let it go. <bookmark mark='g'/> At first it behaves like a ball: it moves, "
            "spreads a little, bounces off the wall and comes back. <bookmark mark='m'/> But the clocks drift out of "
            "step, and within a couple of bounces the packet has smeared into a tangle of ripples filling the whole "
            "box. It looks like the information about where it started is gone for good."
        ) as vo:
            self.play(Create(ax), FadeIn(wl), FadeIn(wv), FadeIn(wheel), FadeIn(sim))
            self.add(clock)
            vo.wait_until("g")
            self.play(t.animate.set_value(0.045 * T), run_time=4.5, rate_func=linear)
            vo.wait_until("m")
            self.play(t.animate.set_value(0.15 * T), run_time=vo.remaining() + 0.5, rate_func=linear)
        for m in (wv, clock):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def weave(self):
        c = load("carpet")
        x, ts, cp, T = c["x"], c["ts"], c["carpet"], float(c["T_rev"][0])
        mv, tm = c["movie"], c["t_movie"]
        dens = np.abs(cp) ** 2
        d = np.clip(dens / np.percentile(dens, 99.5), 0, 1) ** 0.6
        gold = qcm.hex_rgb(C.BORN)
        full = qcm.to_uint8(qcm.BG + d[..., None] * (gold - qcm.BG))
        W, H = 6.4, 5.0
        center = np.array([1.6, -1.15, 0])
        s = ValueTracker(0.0)  # fraction of the period woven so far

        def draw(v):
            k = int(round(v * (len(ts) - 1)))
            img = np.zeros(full.shape[:2] + (4,), np.uint8)
            img[: k + 1, :, :3] = full[: k + 1]
            img[: k + 1, :, 3] = 255
            return img

        from videos.quantum.common import Raster
        carpet = Raster(draw, s, W, H, center=center)
        frame = Rectangle(width=W, height=H, color=GREY_B, stroke_width=1.5).move_to(center)
        ax = wave_axes((-0.0, 1.0), (0, 7.5), x_length=W, y_length=1.9).next_to(frame, UP, buff=0.12)
        wv = WaveView(ax, x, mv[0], mode="density", x_window=(0, 1)).follow(s, lambda v: frames_at(tm, mv)(v * T))
        sweep = always_redraw(lambda: Line(frame.get_corner(UL) + DOWN * H * s.get_value(),
                                           frame.get_corner(UR) + DOWN * H * s.get_value(), color=WHITE, stroke_width=2))
        tl = MathTex("t", font_size=32, color=C.QTIME).next_to(frame, LEFT, buff=0.2).shift(UP * 2.0)
        tarr = Arrow(frame.get_corner(UL) + LEFT * 0.35 + DOWN * 0.2, frame.get_corner(DL) + LEFT * 0.35, buff=0,
                     color=C.QTIME, stroke_width=3)
        marks = VGroup()
        for f, s_ in ((0.25, r"\tfrac{T}{4}"), (0.5, r"\tfrac{T}{2}"), (1.0, r"T")):
            y = frame.get_top()[1] - H * f
            marks.add(VGroup(Line([frame.get_right()[0], y, 0], [frame.get_right()[0] + 0.15, y, 0], color=GREY_B),
                             MathTex(s_, font_size=28, color=C.QTIME).next_to([frame.get_right()[0] + 0.15, y, 0], RIGHT, buff=0.08)))
        xl = MathTex("x", font_size=30, color=C.XPOS).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        title = label(r"the quantum carpet: brightness $= |\psi(x,t)|^2$, over one full period", font_size=26,
                      color=GREY_A).to_edge(UP, buff=0.12)
        wheel = corner_wheel(corner=DL, buff=0.3, radius=0.32)
        with self.voiceover(
            "To see the whole story at once, stack the snapshots: x across, time going down, brightness for the "
            "probability. <bookmark mark='w'/> We'll weave it one row at a time."
        ) as vo:
            self.play(FadeIn(title), Create(frame), Create(ax), FadeIn(xl), FadeIn(wv), FadeIn(tl), GrowArrow(tarr),
                      FadeIn(wheel))
            self.add(carpet, sweep)
            vo.wait_until("w")
            self.play(s.animate.set_value(0.12), run_time=vo.remaining(), rate_func=linear)
        with self.voiceover(
            "The early zigzag is the bouncing packet. Then it dissolves into a fine weave, crossed by straight dark "
            "channels... <bookmark mark='q'/> but "
            "look at a quarter of the way through: two clean packets, one where we started and one at the mirror-image "
            "spot. <bookmark mark='h'/> At half the period, a single packet again, perfectly mirrored. And at the end of "
            "the period, <bookmark mark='f'/> the original packet, exactly as it began. Then the whole pattern repeats "
            "forever."
        ) as vo:
            self.play(s.animate.set_value(0.25), run_time=3.0, rate_func=linear)
            vo.wait_until("q")
            self.play(FadeIn(marks[0]))
            self.play(s.animate.set_value(0.5), run_time=3.0, rate_func=linear)
            vo.wait_until("h")
            self.play(FadeIn(marks[1]))
            self.play(s.animate.set_value(1.0), run_time=4.5, rate_func=linear)
            vo.wait_until("f")
            self.play(FadeIn(marks[2]))
        with self.voiceover(
            "Nothing here was arranged by hand. This intricate pattern, called a quantum carpet, is just three hundred "
            "sine waves, each turning at a rate proportional to n squared. It's the same mathematics as an optical "
            "effect Henry Fox Talbot noticed in 1836, when light passes through a grating."
        ):
            self.play(s.animate.set_value(0.999), run_time=0.5)
        for m in (carpet, wv, sweep):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def why_revival(self):
        c = load("carpet")
        x, mv, tm, T = c["x"], c["movie"], c["t_movie"], float(c["T_rev"][0])
        l1 = MathTex(r"e^{-iE_nt/\hbar}", r"=", r"e^{-i\,n^2 E_1 t/\hbar}", font_size=38)
        l2 = MathTex(r"t = T", r"=", r"\frac{2\pi\hbar}{E_1}", r"=", r"\frac{4mL^2}{\pi\hbar}", font_size=38)
        l3 = MathTex(r"t = \tfrac{T}{2}:", r"\quad", r"e^{-i\pi n^2} = (-1)^n", font_size=36)
        l4 = MathTex(r"t = \tfrac{T}{4}:", r"\quad", r"e^{-i\pi n^2/2} = \begin{cases} 1 & n \text{ even}\\ -i & n\text{ odd}\end{cases}",
                     font_size=36)
        col = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.38, aligned_edge=LEFT).to_corner(UL, buff=0.45)
        l2[0].set_color(C.QTIME)
        n2 = note(r"every $n^2$ is a whole number, so every clock is back at 12 o'clock").next_to(l2, DOWN, buff=0.06,
                                                                                           aligned_edge=LEFT)
        n3 = note(r"$\varphi_n(L - x) = (-1)^{n+1}\varphi_n(x)$: the mirror image").next_to(l3, DOWN, buff=0.06,
                                                                                         aligned_edge=LEFT)
        n4 = note(r"the packet $+$ its mirror image, each with probability $\tfrac12$").next_to(l4, DOWN, buff=0.06,
                                                                                            aligned_edge=LEFT)
        views = VGroup()
        wvs = []
        for i, (f, s_) in enumerate(((0.25, r"t = T/4"), (0.5, r"t = T/2"), (1.0, r"t = T"))):
            a = wave_axes((-0.02, 1.02), (0, 7.5), x_length=4.4, y_length=1.45).move_to(RIGHT * 4.3 + UP * (2.2 - 2.15 * i))
            w = WaveView(a, x, frames_at(tm, mv)(f * T), mode="density", x_window=(0, 1))
            views.add(VGroup(a, walls(a), MathTex(s_, font_size=26, color=C.QTIME).next_to(a, LEFT, buff=0.15)))
            wvs.append(w)
        rev = float(load("numbers")["Trev"][0]) * 1e15
        assert abs(rev - 11.0) < 0.05
        realn = label(rf"electron in a $1$\,nm box: $T = {rev:.1f}$ femtoseconds", font_size=28, color=GREY_A)
        realn.to_edge(DOWN, buff=0.4).shift(LEFT * 2.6)
        with self.voiceover(
            "Why does it come back? <bookmark mark='a'/> Each clock turns at n squared times the slowest rate. "
            "<bookmark mark='b'/> After one full turn of the slowest clock, the n-th clock has made exactly n squared "
            "turns. Every n squared is a whole number, so every clock is back where it started, and so is the "
            "wavefunction. The revival time is two pi h-bar over E one: four m L squared over pi h-bar."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(l1))
            vo.wait_until("b")
            self.play(Write(l2), FadeIn(n2), FadeIn(views[2]), FadeIn(wvs[2]))
        with self.voiceover(
            "<bookmark mark='h'/> At half the period, each clock is at plus or minus one, depending on whether n is even "
            "or odd, and that sign pattern is exactly what reflects a sine series about the middle of the box: a mirror "
            "image. <bookmark mark='q'/> At a quarter period the even and odd terms pick up different phases, and the "
            "wave splits into the packet plus its mirror image, each with half the probability: a particle in a "
            "superposition of two places, produced by nothing but waiting. <bookmark mark='r'/> For an electron in a "
            "one-nanometer box, the full revival takes eleven femtoseconds."
        ) as vo:
            vo.wait_until("h")
            self.play(Write(l3), FadeIn(n3), FadeIn(views[1]), FadeIn(wvs[1]))
            vo.wait_until("q")
            self.play(Write(l4), FadeIn(n4), FadeIn(views[0]), FadeIn(wvs[0]))
            vo.wait_until("r")
            self.play(FadeIn(realn))
        self.wait(0.4)
        self.clear_scene()
