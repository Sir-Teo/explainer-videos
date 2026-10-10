from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum.common import (boxed, complex_plane, hue, label, load, mtex, note, num, part_card, phasor,
                                   place_whys, stack, why)
from videos.quantum.compute import SLIT

SY = 0.01  # scene units per simulation unit (the apparatus is drawn to the simulation's scale)
SCREEN_X = -0.9


def sim_y(y):
    return np.asarray(y, float) * SY


class Amplitudes(VoiceoverScene):
    def construct(self):
        self.card()
        self.three_patterns()
        self.arrows_add()
        self.algebra()
        self.path_phase()
        self.check_fringes()

    def card(self):
        c = part_card(1, r"Amplitudes", r"arrows that add")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def plate(self, top=True, bottom=True):
        p = SLIT
        wall_x = SCREEN_X - (p["screen"] - p["wall"][1]) * SY
        half = p["w"] / 2 * SY
        a = p["d"] / 2 * SY
        H = 3.3
        cuts = [(-H, -a - half), (-a + half, a - half), (a + half, H)]
        if not top:
            cuts = [(-H, -a - half), (-a + half, H)]
        if not bottom:
            cuts = [(-H, a - half), (a + half, H)]
        if not top and not bottom:
            cuts = [(-H, H)]
        g = VGroup(*[Rectangle(width=0.1, height=y1 - y0, stroke_width=0, fill_color=C.WALL, fill_opacity=1)
                     .move_to([wall_x, (y0 + y1) / 2, 0]) for y0, y1 in cuts])
        return g

    def curve(self, y, P, scale, color, width=3, dashed=False):
        keep = np.abs(y) <= 300
        pts = np.stack([SCREEN_X + 0.15 + scale * P[keep], sim_y(y[keep]), 0 * y[keep]], axis=1)
        m = VMobject(stroke_color=color, stroke_width=width)
        m.set_points_as_corners(pts)
        if dashed:
            m = DashedVMobject(m, num_dashes=90, dashed_ratio=0.55)
        return m

    def three_patterns(self):
        s = load("slits")
        y, P1, P2, P12 = s["y"], s["P1"], s["P2"], s["P12"]
        scale = 5.4 / P12.max()
        screen = Line([SCREEN_X, -3.2, 0], [SCREEN_X, 3.2, 0], color=GREY_A, stroke_width=3)
        sl = label(r"screen", font_size=24, color=GREY_B).next_to(screen, DOWN, buff=0.1)
        plates = {k: self.plate(*k) for k in ((True, False), (False, True), (True, True))}
        src = VGroup(Dot([-6.45, 0, 0], radius=0.09, color=WHITE), label(r"electrons", font_size=24, color=GREY_B)
                     .next_to([-6.45, 0, 0], DOWN, buff=0.18))
        c1 = self.curve(y, P1, scale, GREY_A)
        c2 = self.curve(y, P2, scale, GREY_A)
        csum = self.curve(y, P1 + P2, scale, C.CLASSICAL, width=3.5, dashed=True)
        c12 = self.curve(y, P12, scale, C.BORN, width=3.5)
        l1 = MathTex(r"P_1", font_size=34, color=GREY_A).move_to([SCREEN_X + 0.45 + scale * P1.max(), 1.9, 0])
        l2 = MathTex(r"P_2", font_size=34, color=GREY_A).move_to([SCREEN_X + 0.45 + scale * P2.max(), -1.9, 0])
        lsum = MathTex(r"P_1 + P_2", font_size=34, color=C.CLASSICAL).to_corner(UR, buff=0.5)
        l12 = MathTex(r"P_{12}", font_size=36, color=C.BORN).next_to(lsum, DOWN, buff=0.3, aligned_edge=LEFT)
        tag = note(r"simulated: a wave packet through the slits, drawn to scale; arrival density on the screen")
        tag.to_corner(DL, buff=0.3)
        with self.voiceover(
            "Let's go back to the double slit, and do it more carefully, using the simulation from the start of the "
            "video. <bookmark mark='a'/> First, close the bottom slit. Electrons arriving at the screen pile up in one "
            "broad hump. Call that distribution P one."
        ) as vo:
            self.play(Create(screen), FadeIn(sl), FadeIn(src), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(plates[(True, False)]))
            self.play(Create(c1), FadeIn(l1), run_time=1.6)
        with self.voiceover(
            "Now close the top slit instead, and open the bottom one: <bookmark mark='b'/> another hump, P two. "
            "<bookmark mark='c'/> Common sense says that with both slits open, each electron goes through one slit or "
            "the other, so the two distributions should simply add."
        ) as vo:
            vo.wait_until("b")
            self.play(ReplacementTransform(plates[(True, False)], plates[(False, True)]), Create(c2), FadeIn(l2),
                      run_time=1.6)
            vo.wait_until("c")
            self.play(ReplacementTransform(plates[(False, True)], plates[(True, True)]), Create(csum), FadeIn(lsum),
                      c1.animate.set_stroke(opacity=0.3), c2.animate.set_stroke(opacity=0.3), FadeOut(l1), FadeOut(l2),
                      run_time=1.6)
        dip = float(s["dips"][s["dips"] > 0][0])
        i_dip = int(np.argmin(np.abs(y - dip)))
        mark = Arrow([SCREEN_X + 3.2, sim_y(dip) + 0.9, 0], [SCREEN_X + 0.25 + scale * P12[i_dip], sim_y(dip), 0],
                     buff=0.05, color=WHITE, stroke_width=3, max_tip_length_to_length_ratio=0.12)
        ml = label(r"here, both slits open\\is \emph{worse} than one", font_size=26).next_to(mark.get_start(), UP, buff=0.1)
        with self.voiceover(
            "That's not what happens. <bookmark mark='d'/> With both slits open, the distribution has stripes. "
            "<bookmark mark='e'/> And look at the dark places: there, with either slit alone, plenty of electrons "
            "arrive. Open both, and almost none do. Adding a second way to get somewhere can make it impossible to get "
            "there. Probabilities don't add."
        ) as vo:
            vo.wait_until("d")
            self.play(Create(c12), FadeIn(l12), run_time=2)
            vo.wait_until("e")
            self.play(GrowArrow(mark), FadeIn(ml))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def arrows_add(self):
        plane = complex_plane(radius=2.4).move_to(LEFT * 3.6 + DOWN * 0.2)
        o = plane[0][0].get_center()
        dphi = ValueTracker(0.0)
        unit = 1.05
        z1 = 1.0 + 0j

        def z2():
            return np.exp(1j * dphi.get_value())

        a1 = always_redraw(lambda: phasor(z1, origin=o, unit=unit, stroke_width=5))
        a2 = always_redraw(lambda: phasor(z2(), origin=o + unit * RIGHT, unit=unit, stroke_width=5))
        asum = always_redraw(lambda: Arrow(o, o + unit * np.array([(z1 + z2()).real, (z1 + z2()).imag, 0]), buff=0,
                                           color=WHITE, stroke_width=4, tip_length=0.2,
                                           max_tip_length_to_length_ratio=0.3).set_opacity(
            1.0 if abs(z1 + z2()) > 0.08 else 0.0))
        l1 = MathTex(r"z_1", font_size=34).next_to(o + unit * RIGHT * 0.5, DOWN, buff=0.15)
        l2 = always_redraw(lambda: MathTex(r"z_2", font_size=34).move_to(
            o + unit * RIGHT + 0.5 * unit * np.array([z2().real, z2().imag, 0]) + 0.35 * np.array(
                [-z2().imag, z2().real, 0])))
        ax = Axes(x_range=[0, TAU, PI / 2], y_range=[0, 4.4, 1], x_length=5.2, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(RIGHT * 3.4 + DOWN * 0.3)
        xl = MathTex(r"\Delta\varphi", font_size=30).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        yl = MathTex(r"|z_1 + z_2|^2", font_size=30, color=C.BORN).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        ticks = VGroup(*[MathTex(s, font_size=24, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12)
                         for v, s in ((0, "0"), (PI, r"\pi"), (TAU, r"2\pi"))])
        one = DashedLine(ax.c2p(0, 2), ax.c2p(TAU, 2), color=C.CLASSICAL, stroke_width=2)
        one_l = MathTex(r"|z_1|^2 + |z_2|^2", font_size=26, color=C.CLASSICAL).next_to(ax.c2p(PI, 2), UP, buff=0.1)  # above the dip, clear of the curve
        trace = always_redraw(lambda: ax.plot(lambda t: abs(1 + np.exp(1j * t)) ** 2, x_range=[0, max(1e-3, dphi.get_value())],
                                              color=C.BORN, stroke_width=3.5))
        dot = always_redraw(lambda: Dot(ax.c2p(dphi.get_value(), abs(z1 + z2()) ** 2), color=C.BORN, radius=0.07))
        rule = label(r"probability $= |\text{sum of arrows}|^2$", font_size=32).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Here's the rule that does work. Each way of getting from the source to a point on the screen contributes "
            "an arrow: a complex number called an amplitude. <bookmark mark='a'/> Add the arrows tip to tail, "
            "<bookmark mark='s'/> and the probability is the length of the total, squared."
        ) as vo:
            self.play(FadeIn(plane), FadeIn(rule))
            vo.wait_until("a")
            self.add(a1, a2, l1, l2)
            self.play(FadeIn(a1), FadeIn(a2), FadeIn(l1), FadeIn(l2))
            vo.wait_until("s")
            self.add(asum)
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ticks), FadeIn(dot))
        with self.voiceover(
            "Now change the angle between the two arrows. <bookmark mark='r'/> When they point the same way, the total "
            "is twice as long, and the probability is four times what one slit gives. <bookmark mark='o'/> When they "
            "point in opposite directions, they cancel, and the probability is zero. <bookmark mark='c'/> On average "
            "you get the sum of the two separate probabilities, but at any one point, you can get anything from zero "
            "to double that."
        ) as vo:
            self.add(trace)
            vo.wait_until("r")
            self.play(dphi.animate.set_value(PI), run_time=2.5, rate_func=linear)
            vo.wait_until("o")
            self.play(dphi.animate.set_value(TAU), run_time=2.5, rate_func=linear)
            vo.wait_until("c")
            self.play(Create(one), FadeIn(one_l))
        self.wait(0.3)
        for m in (a1, a2, asum, l2, trace, dot):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def algebra(self):
        l1 = MathTex(r"|z_1 + z_2|^2", r"=", r"(z_1 + z_2)\,(z_1 + z_2)^*", font_size=42)
        l2 = MathTex(r"\phantom{|z_1 + z_2|^2}", r"=", r"|z_1|^2 + |z_2|^2", r"+", r"z_1^* z_2 + z_1 z_2^*", font_size=42)
        l3 = MathTex(r"\phantom{|z_1 + z_2|^2}", r"=", r"|z_1|^2 + |z_2|^2", r"+", r"2\,\mathrm{Re}\,(z_1^* z_2)", font_size=42)
        l4 = MathTex(r"\phantom{|z_1 + z_2|^2}", r"=", r"|z_1|^2 + |z_2|^2", r"+", r"2\,|z_1|\,|z_2|\cos(\varphi_2 - \varphi_1)",
                     font_size=42)
        col = stack(l1, l2, l3, l4, buff=0.45, align=1).to_edge(UP, buff=0.5).shift(LEFT * 1.6)
        for m in (l2, l3, l4):
            m[4].set_color(C.BORN)
        w1 = why(l1, r"$|z|^2 = z\,z^*$")
        w2 = why(l2, r"multiply out")
        w3 = why(l3, r"$w + w^* = 2\,\mathrm{Re}\,w$")
        w4 = why(l4, r"$z = |z|\,e^{i\varphi}$")
        place_whys([l1, l2, l3, l4], [w1, w2, w3, w4])
        b1 = Brace(l4[2], DOWN, buff=0.12, color=C.CLASSICAL)
        bl1 = MathTex(r"P_1 + P_2", font_size=32, color=C.CLASSICAL).next_to(b1, DOWN, buff=0.1)
        b2 = Brace(l4[4], DOWN, buff=0.12, color=C.BORN)
        bl2 = label(r"interference: can be negative", font_size=28, color=C.BORN).next_to(b2, DOWN, buff=0.1)
        motto = boxed(label(r"Amplitudes add. Probabilities don't.", font_size=36), color=C.BORN, buff=0.2)
        motto.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Let's see exactly why. <bookmark mark='a'/> The length squared of a complex number is the number times "
            "its complex conjugate. <bookmark mark='b'/> Multiply out: you get the two separate probabilities, plus two "
            "cross terms. <bookmark mark='c'/> The cross terms are conjugates of each other, so together they're twice "
            "the real part. <bookmark mark='d'/> Write each arrow as a length times e to the i phi, and the cross term "
            "becomes a cosine of the angle between them."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(l1), FadeIn(w1))
            vo.wait_until("b")
            self.play(Write(l2[1:]), FadeIn(w2))
            vo.wait_until("c")
            self.play(Write(l3[1:]), FadeIn(w3))
            vo.wait_until("d")
            self.play(Write(l4[1:]), FadeIn(w4))
        with self.voiceover(
            "<bookmark mark='p'/> The first two terms are what you'd get if probabilities added. <bookmark mark='i'/> "
            "The last one is new. It's called the interference term, and because a cosine can be negative, it can take "
            "probability away. <bookmark mark='m'/> That's the whole difference: in quantum mechanics, amplitudes add, "
            "and you square at the end."
        ) as vo:
            vo.wait_until("p")
            self.play(GrowFromCenter(b1), FadeIn(bl1))
            vo.wait_until("i")
            self.play(GrowFromCenter(b2), FadeIn(bl2))
            vo.wait_until("m")
            self.play(FadeIn(motto))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def path_phase(self):
        up = 0.35
        S1, S2 = np.array([-5.0, 0.9 + up, 0]), np.array([-5.0, -0.9 + up, 0])
        Y = np.array([1.0, 2.6 + up, 0])
        plate = VGroup(Line([-5.0, -2.9 + up, 0], [-5.0, -1.1 + up, 0]), Line([-5.0, -0.7 + up, 0], [-5.0, 0.7 + up, 0]),
                       Line([-5.0, 1.1 + up, 0], [-5.0, 3.2 + up, 0])).set_stroke(C.WALL, 6)
        screen = Line([1.0, -2.9 + up, 0], [1.0, 3.2 + up, 0], color=GREY_A, stroke_width=3)
        p1, p2 = Line(S1, Y, color=GREY_B, stroke_width=2), Line(S2, Y, color=GREY_B, stroke_width=2)
        r1 = MathTex("r_1", font_size=32).move_to(p1.point_from_proportion(0.5) + UP * 0.3)
        r2 = MathTex("r_2", font_size=32).move_to(p2.point_from_proportion(0.55) + DOWN * 0.35)
        dl = BraceBetweenPoints(S2 + LEFT * 0.15, S1 + LEFT * 0.15, LEFT, color=GREY_A)
        dt = MathTex("d", font_size=32).next_to(dl, LEFT, buff=0.1)
        Lb = BraceBetweenPoints([-5.0, -3.05 + up, 0], [1.0, -3.05 + up, 0], DOWN, color=GREY_A)
        Lt = MathTex("L", font_size=32).next_to(Lb, DOWN, buff=0.08)
        yb = Line([1.0, up, 0], Y, color=C.XPOS, stroke_width=3)
        yt = MathTex("y", font_size=32, color=C.XPOS).next_to(yb, RIGHT, buff=0.1)
        cen = DashedLine([-5.0, up, 0], [1.0, up, 0], color=GREY_D, stroke_width=1.5)
        tag = note(r"schematic (not to scale)").to_corner(UL, buff=0.25)
        lam = 0.55
        prog = ValueTracker(0.0)

        def rider(S):
            def make():
                f = prog.get_value()
                d = np.linalg.norm(Y - S)
                pos = S + f * (Y - S)
                ang = TAU * f * d / lam
                return VGroup(Circle(radius=0.32, color=GREY_C, stroke_width=1.5).move_to(pos),
                              phasor(np.exp(1j * ang), origin=pos, unit=0.3, stroke_width=4, tip=0.12))
            return always_redraw(make)

        c1, c2 = rider(S1), rider(S2)
        with self.voiceover(
            "So where do the angles come from? Feynman's picture: each amplitude is like the hand of a tiny clock "
            "that the electron carries along its path. <bookmark mark='g'/> The hand turns one full revolution for "
            "every wavelength traveled. <bookmark mark='r'/> Two paths of different lengths arrive with their hands "
            "turned by different amounts."
        ) as vo:
            self.play(Create(plate), Create(screen), Create(cen), FadeIn(tag))
            vo.wait_until("g")
            self.play(Create(p1), Create(p2), FadeIn(r1), FadeIn(r2), GrowFromCenter(dl), FadeIn(dt), GrowFromCenter(Lb),
                      FadeIn(Lt), Create(yb), FadeIn(yt))
            self.add(c1, c2)
            vo.wait_until("r")
            self.play(prog.animate.set_value(1.0), run_time=4, rate_func=linear)
        for m in (c1, c2):
            m.clear_updaters()
        f1 = MathTex(r"\varphi", r"=", r"2\pi\,\frac{r}{\lambda}", font_size=38)
        f2 = MathTex(r"\Delta\varphi", r"=", r"2\pi\,\frac{r_2 - r_1}{\lambda}", font_size=38)
        f3 = MathTex(r"r_2 - r_1", r"\approx", r"\frac{d\,y}{L}", font_size=38)
        f4 = MathTex(r"y_m", r"=", r"m\,\frac{\lambda L}{d}", font_size=38)
        f5 = MathTex(r"\lambda", r"=", r"\frac{h}{p}", font_size=38)
        col = VGroup(f1, f2, f3, f4, f5).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(RIGHT * 4.4 + UP * 0.3)
        f4[0].set_color(C.XPOS)
        f5[0].set_color(C.MOMENTUM)
        f5[2].set_color(C.MOMENTUM)
        n3 = note(r"when $d,\,y \ll L$").next_to(f3, DOWN, buff=0.06, aligned_edge=LEFT)
        n4 = note(r"bright where $\Delta\varphi = 2\pi m$").next_to(f4, DOWN, buff=0.06, aligned_edge=LEFT)
        n5 = note(r"de Broglie, 1924").next_to(f5, DOWN, buff=0.06, aligned_edge=LEFT)
        lam50 = float(load("numbers")["lam50"][0])
        assert abs(lam50 * 1e12 - 5.36) < 0.01
        e50 = label(rf"electrons at 50\,kV: $\lambda = {lam50 * 1e12:.2f}$ pm", font_size=24, color=GREY_A)
        e50.next_to(n5, DOWN, buff=0.15, aligned_edge=LEFT)
        with self.voiceover(
            "In symbols: <bookmark mark='a'/> a path of length r turns the hand by two pi r over lambda. "
            "<bookmark mark='b'/> So the angle between the two arrows is two pi times the difference in path lengths, "
            "in wavelengths. <bookmark mark='c'/> When the screen is far away, that difference is d times y over L. "
            "<bookmark mark='d'/> The arrows line up, and the screen is bright, whenever the difference is a whole "
            "number of wavelengths: at heights m lambda L over d. <bookmark mark='e'/> And the wavelength itself comes "
            "from de Broglie: lambda equals h over the momentum. For electrons accelerated through fifty kilovolts, "
            "that's about five picometers."
        ) as vo:
            for m, f, n in zip("abcde", (f1, f2, f3, f4, f5), (None, None, n3, n4, n5)):
                vo.wait_until(m)
                anims = [Write(f)] + ([FadeIn(n)] if n is not None else [])
                if m == "e":
                    anims.append(FadeIn(e50))
                self.play(*anims)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check_fringes(self):
        s = load("slits")
        y, P12 = s["y"], s["P12"]
        lam, L, d = float(s["lam"][0]), float(s["L"][0]), SLIT["d"]
        spacing = lam * L / d
        assert abs(spacing - 71.5) < 0.1, spacing
        pk = np.sort(s["peaks"])
        gaps = np.diff(pk)
        assert np.all(np.abs(gaps - spacing) < 3.0), gaps
        assert abs(gaps.mean() - 71.0) < 0.05 and abs(lam - 8.38) < 0.005 and L == 512  # as narrated
        scale = 5.4 / P12.max()
        screen = Line([SCREEN_X, -3.2, 0], [SCREEN_X, 3.2, 0], color=GREY_A, stroke_width=3)
        c12 = self.curve(y, P12, scale, C.BORN, width=3.5)
        # predicted bright fringes (exact path difference a whole number of wavelengths) and dark ones
        a = d / 2
        pdiff = lambda yy: np.sqrt(L**2 + (yy + a) ** 2) - np.sqrt(L**2 + (yy - a) ** 2)  # noqa: E731
        yy = np.linspace(-299, 299, 20001)
        ph = pdiff(yy) / lam
        lines = VGroup()
        for m in np.arange(-3.5, 3.6, 1.0):
            yd = float(np.interp(m, ph, yy))
            lines.add(DashedLine([SCREEN_X - 0.25, sim_y(yd), 0], [SCREEN_X + 5.9, sim_y(yd), 0], color=GREY_B,
                                 stroke_width=1.5, dash_length=0.07))
        nums = VGroup(
            MathTex(r"\lambda = " + num(lam, 2), font_size=32),
            MathTex(r"d = " + f"{d:.0f}", r",\; L = " + f"{L:.0f}", font_size=32),
            MathTex(r"\frac{\lambda L}{d} = " + num(spacing, 1), font_size=34, color=C.XPOS),
            MathTex(r"\text{measured spacing: } " + num(gaps.mean(), 1), font_size=32, color=C.BORN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.5).shift(UP * 0.5)
        dl = note(r"dashed: predicted dark fringes, path difference $(m + \tfrac12)\lambda$").to_corner(DR, buff=0.3)
        units = note(r"simulation units").next_to(nums, DOWN, buff=0.3, aligned_edge=LEFT)
        with self.voiceover(
            "Let's check that against the simulation. <bookmark mark='n'/> Its wavelength is 8.38 units, the slits are "
            "60 apart, and the screen is 512 away. So the fringes should be 71.5 units apart. <bookmark mark='m'/> "
            "Measured from the simulated pattern: 71.0. <bookmark mark='d'/> And the dark fringes sit exactly where the "
            "two paths differ by a half-integer number of wavelengths."
        ) as vo:
            self.play(Create(screen), Create(c12))
            vo.wait_until("n")
            self.play(FadeIn(nums[0]), FadeIn(nums[1]), FadeIn(units))
            self.play(Write(nums[2]))
            vo.wait_until("m")
            self.play(FadeIn(nums[3]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(m) for m in lines], lag_ratio=0.1), FadeIn(dl), run_time=1.6)
        with self.voiceover(
            "Two slits, two paths, two arrows. But an electron isn't limited to two options. In general there's an "
            "amplitude for the electron to be at every point in space, and that's what we turn to next."
        ):
            pass
        self.clear_scene()
