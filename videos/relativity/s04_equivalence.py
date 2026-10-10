from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import redraw, boxed, label, load, mtex, note, polyline, sci, stack, st_axes


def cabin(center, w=2.6, h=3.2, color=GREY_A):
    r = Rectangle(width=w, height=h, color=color, stroke_width=3).move_to(center)
    return r


def flame(bottom, size=0.5):
    tip = bottom + DOWN * size * 1.4
    f = Polygon(bottom + LEFT * size * 0.45, bottom + RIGHT * size * 0.45, tip, stroke_width=0, fill_color=ORANGE,
                fill_opacity=0.85)
    inner = Polygon(bottom + LEFT * size * 0.22, bottom + RIGHT * size * 0.22, bottom + DOWN * size * 0.8,
                    stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
    return VGroup(f, inner)


class Equivalence(VoiceoverScene):
    def construct(self):
        self.thought()
        self.boxes()
        self.light()
        self.clocks()
        self.pound_rebka()
        self.gps()
        self.metric()

    # ------------------------------------------------------------------
    def thought(self):
        q = VGroup(
            label(r"``\ldots for an observer falling freely from the roof of a house", font_size=34),
            label(r"there exists, at least in his immediate surroundings,", font_size=34),
            label(r"no gravitational field.''", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(UP * 0.6)
        who = label(r"Einstein, recalling an idea from 1907: ``the happiest thought of my life''", font_size=28,
                    color=GREY_A).next_to(q, DOWN, buff=0.6)
        head = label(r"Bern, 1907", font_size=40).to_edge(UP, buff=0.6)
        with self.voiceover(
            "In 1907, two years after special relativity, Einstein was working at the patent office in Bern when he had "
            "what he later called the happiest thought of his life. <bookmark mark='q'/> A person falling freely from the "
            "roof of a house does not feel their own weight. For them, at least in their immediate surroundings, there "
            "is no gravitational field."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("q")
            self.play(FadeIn(q, lag_ratio=0.2), run_time=2)
            self.play(FadeIn(who))
        self.clear_scene()

    # ------------------------------------------------------------------
    def boxes(self):
        L, R = np.array([-3.4, -0.3, 0]), np.array([3.4, -0.3, 0])
        bl, br = cabin(L), cabin(R)
        ground = VGroup(Line(L + DOWN * 1.6 + LEFT * 2.2, L + DOWN * 1.6 + RIGHT * 2.2, color=GREY_B, stroke_width=4),
                        *[Line(L + DOWN * 1.6 + RIGHT * x, L + DOWN * 1.9 + RIGHT * (x - 0.3), color=GREY_D)
                          for x in np.linspace(-2.0, 2.2, 12)])
        garrow = Arrow(L + LEFT * 2.0 + UP * 1.0, L + LEFT * 2.0 + DOWN * 0.2, buff=0, color=C.GRAV_POTENTIAL)
        gl = MathTex(r"g", font_size=34, color=C.GRAV_POTENTIAL).next_to(garrow, LEFT, buff=0.1)
        fl = flame(R + DOWN * 1.6)
        aarrow = Arrow(R + RIGHT * 2.0 + DOWN * 0.2, R + RIGHT * 2.0 + UP * 1.0, buff=0, color=C.METRIC)
        al = MathTex(r"a = g", font_size=34, color=C.METRIC).next_to(aarrow, RIGHT, buff=0.1)
        tl = label(r"at rest on Earth", font_size=30).next_to(bl, UP, buff=0.35)
        tr = label(r"accelerating in empty space", font_size=30).next_to(br, UP, buff=0.35)
        # stars streaming past the rocket
        rng = np.random.default_rng(4)
        sx = rng.uniform(R[0] - 3.2, R[0] + 3.4, 26)
        sy0 = rng.uniform(-4, 4, 26)
        st = ValueTracker(0.0)
        stars = redraw(lambda: VGroup(*[Dot([x, ((y - st.get_value() * 2.5 + 4) % 8) - 4, 0], radius=0.02,
                                                   color=GREY_B) for x, y in zip(sx, sy0)
                                               if not (abs(x - R[0]) < 1.4 and abs(((y - st.get_value() * 2.5 + 4) % 8) - 4 - R[1]) < 1.7)]))
        k = ValueTracker(0.0)

        def ball(c):
            return redraw(lambda: Dot(c + UP * (0.9 - 2.38 * k.get_value() ** 2), radius=0.14, color=C.MATTER))

        b1, b2 = ball(L), ball(R)
        same = label(r"No experiment inside the box can tell these apart.", font_size=32, color=C.CURVATURE)
        same.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Turn that around. <bookmark mark='a'/> Here's a closed box resting on the Earth, and <bookmark mark='b'/> "
            "here's an identical box on a rocket in deep space, far from any planet, accelerating upward at nine point "
            "eight meters per second squared. <bookmark mark='d'/> Release a ball in each. In both, the ball falls to the "
            "floor in exactly the same way: on Earth because gravity pulls it, in the rocket because the floor rushes up "
            "to meet it. <bookmark mark='s'/> No experiment inside the box can tell the difference."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(bl), FadeIn(ground), GrowArrow(garrow), FadeIn(gl), FadeIn(tl))
            vo.wait_until("b")
            self.add(stars)
            self.play(Create(br), FadeIn(fl), GrowArrow(aarrow), FadeIn(al), FadeIn(tr),
                      st.animate.set_value(1.0), run_time=1.5)
            vo.wait_until("d")
            self.add(b1, b2)
            self.play(k.animate.set_value(1.0), st.animate.set_value(2.6), run_time=1.4, rate_func=linear)
            vo.wait_until("s")
            self.play(FadeIn(same), st.animate.set_value(4.0), run_time=1.5)
        b1.clear_updaters()
        b2.clear_updaters()
        # free fall vs floating
        k2 = ValueTracker(0.0)
        b1b = redraw(lambda: Dot(L + UP * 0.2 + RIGHT * 0.3 * math.sin(3 * k2.get_value()), radius=0.14, color=C.MATTER))
        b2b = redraw(lambda: Dot(R + UP * 0.2 + RIGHT * 0.3 * math.sin(3 * k2.get_value()), radius=0.14, color=C.MATTER))
        tl2 = label(r"falling freely near Earth", font_size=30).move_to(tl)
        tr2 = label(r"floating in empty space", font_size=30).move_to(tr)
        gtag = label(r"falling", font_size=26, color=C.GRAV_POTENTIAL).next_to(bl, LEFT, buff=0.3)
        loc = label(r"Locally, gravity can be made to vanish by falling.", font_size=32, color=C.CURVATURE).move_to(same)
        with self.voiceover(
            "<bookmark mark='a'/> It works the other way too. Cut the cable, and a box falling freely near the Earth is "
            "indistinguishable from one floating in empty space: inside, everything floats. This is the equivalence "
            "principle. <bookmark mark='l'/> Gravity, at least locally, can be made to vanish by falling. And that's why "
            "everything falls the same way: in the falling box, nothing is falling at all."
        ) as vo:
            vo.wait_until("a")
            stars.clear_updaters()
            self.play(FadeOut(b1), FadeOut(b2), FadeOut(fl), FadeOut(VGroup(aarrow, al, garrow, gl)),
                      ReplacementTransform(tl, tl2), ReplacementTransform(tr, tr2), FadeOut(same),
                      ground.animate.shift(DOWN * 0.8).set_opacity(0.4), FadeIn(gtag))
            self.add(b1b, b2b)
            self.play(k2.animate.set_value(3.0), run_time=3, rate_func=linear)
            vo.wait_until("l")
            self.play(FadeIn(loc), k2.animate.set_value(5.0), run_time=2, rate_func=linear)
        b1b.clear_updaters()
        b2b.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def light(self):
        """A light beam crossing an accelerating cabin, seen from outside (straight) and inside (curved)."""
        W, H, a = 3.0, 3.0, 2.4  # exaggerated: the cabin gains 1.2 units of height while the light crosses it
        cl, cr = np.array([-3.5, -0.4, 0]), np.array([3.5, -0.4, 0])
        s = ValueTracker(0.0)
        y_beam = 0.9  # entry height above the cabin's center

        def outside():
            t = s.get_value()
            rise = 0.5 * a * t * t
            box = Rectangle(width=W, height=H, color=GREY_A, stroke_width=3).move_to(cl + UP * (rise - 0.8))
            x0 = cl[0] - W / 2
            beam = Line([x0, cl[1] - 0.8 + y_beam, 0], [x0 + W * t + 1e-3, cl[1] - 0.8 + y_beam, 0], color=C.LIGHT,
                        stroke_width=5)
            return VGroup(box, beam, flame(box.get_bottom(), 0.4))

        def inside():
            t = s.get_value()
            box = Rectangle(width=W, height=H, color=GREY_A, stroke_width=3).move_to(cr)
            ts = np.linspace(0, max(t, 1e-3), 40)
            pts = [[cr[0] - W / 2 + W * u, cr[1] + y_beam - 0.5 * a * u * u, 0] for u in ts]
            beam = VMobject(color=C.LIGHT, stroke_width=5).set_points_smoothly(pts)
            return VGroup(box, beam)

        o, i = redraw(outside), redraw(inside)
        lo = label(r"seen from outside", font_size=30).move_to([cl[0], 3.2, 0])
        li = label(r"seen inside the cabin", font_size=30).move_to([cr[0], 3.2, 0])
        exag = note(r"acceleration exaggerated about $10^{16}$ times").to_corner(UR, buff=0.3)
        res = label(r"So light must fall in a gravitational field.", font_size=32, color=C.LIGHT).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Einstein immediately drew two consequences. The first is about light. <bookmark mark='o'/> Shine a beam "
            "across the accelerating rocket. Seen from outside, the light travels in a perfectly straight line, but while "
            "it crosses, the cabin speeds up underneath it. <bookmark mark='i'/> So seen from inside, the beam enters "
            "high and hits the far wall lower: it curves downward, exactly like a thrown ball. <bookmark mark='r'/> By the "
            "equivalence principle, the same must happen on Earth. Light falls."
        ) as vo:
            self.add(o, i)
            self.play(FadeIn(lo), FadeIn(li), FadeIn(exag))
            vo.wait_until("o")
            self.play(s.animate.set_value(1.0), run_time=3, rate_func=linear)
            vo.wait_until("i")
            self.play(Indicate(li))
            vo.wait_until("r")
            self.play(FadeIn(res))
        with self.voiceover(
            "On Earth the effect is absurdly small. Across a ten meter room, light drops by about five femtometers, the "
            "width of three protons. But near the Sun, as we'll see, it becomes measurable."
        ):
            pass
        drop = 9.81 * (10 / 299_792_458) ** 2 / 2  # the drop across a 10 m room, quoted above
        assert abs(drop - 5.5e-15) < 0.1e-15 and 3.0 < drop / 1.68e-15 < 3.4
        o.clear_updaters()
        i.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def clocks(self):
        d = load("rocket")
        assert abs(float(d["ratio"]) - 1.5) < 1e-9
        g = st_axes(x_range=(0.8, 2.9), t_range=(0, 2.0), unit=2.05, x_label=r"\text{height}", t_label=r"ct")
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        X0, X1 = 1.0, 1.5
        tt = np.linspace(0, 2.0, 200)
        floor = polyline(ax, np.sqrt(X0**2 + tt**2), tt, color=C.PROPER_TIME, stroke_width=4)
        ceil = polyline(ax, np.sqrt(X1**2 + tt**2), tt, color=C.PROPER_TIME, stroke_width=4)
        ok = np.sqrt(X1**2 + tt**2) <= 2.9
        ceil = polyline(ax, np.sqrt(X1**2 + tt[ok]**2), tt[ok], color=C.PROPER_TIME, stroke_width=4)
        fl = label(r"floor", font_size=26, color=C.PROPER_TIME).next_to(ax.c2p(X0, 0), DOWN, buff=0.15)
        cl = label(r"ceiling", font_size=26, color=C.PROPER_TIME).next_to(ax.c2p(X1, 0), DOWN, buff=0.15)
        pulses, emits, recvs = VGroup(), VGroup(), VGroup()
        for te, xe, tr, xr in zip(d["te"], d["xe"], d["tr"], d["xr"]):
            if tr > 1.98:
                continue
            pulses.add(Line(ax.c2p(xe, te), ax.c2p(xr, tr), color=C.LIGHT, stroke_width=2.5))
            emits.add(Dot(ax.c2p(xe, te), radius=0.05, color=WHITE))
            recvs.add(Dot(ax.c2p(xr, tr), radius=0.05, color=WHITE))
        rule = VGroup(
            mtex(r"\frac{\Delta\tau_{\text{ceiling}}}{\Delta\tau_{\text{floor}}}", r"=", r"1 + \frac{g h}{c^2}",
                 font_size=40),
            note(r"(here $gh/c^2 = 0.5$, absurdly exaggerated)", font_size=22),
        ).arrange(DOWN, buff=0.2).move_to([3.6, 1.6, 0])
        rule[0][2].set_color(C.PROPER_TIME)
        concl = VGroup(
            label(r"In a gravitational field:", font_size=30),
            label(r"clocks lower down run slower.", font_size=30, color=C.PROPER_TIME),
            mtex(r"\frac{d\tau}{dt}", r"\approx", r"1 + \frac{\Phi}{c^2}", font_size=40),
        ).arrange(DOWN, buff=0.22).move_to([3.6, -1.4, 0])
        concl[2][2].set_color(C.GRAV_POTENTIAL)
        with self.voiceover(
            "The second consequence is about time. <bookmark mark='d'/> Here's the rocket on a spacetime diagram, with "
            "height across and time up. Because it accelerates, its floor and ceiling trace out curves that bend toward the "
            "speed of light. <bookmark mark='p'/> Now let a clock on the floor send a flash of light upward at every tick. "
            "<bookmark mark='r'/> Each flash has to chase a ceiling that's moving faster than when the previous one left. "
            "So the flashes arrive spread out: the person at the top sees the floor clock ticking slowly."
        ) as vo:
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(g[1:]))
            self.play(Create(floor), Create(ceil), FadeIn(fl), FadeIn(cl))
            vo.wait_until("p")
            self.play(LaggedStart(*[FadeIn(e) for e in emits], lag_ratio=0.15))
            vo.wait_until("r")
            self.play(LaggedStart(*[Create(p) for p in pulses], lag_ratio=0.15), run_time=2)
            self.play(LaggedStart(*[FadeIn(r) for r in recvs], lag_ratio=0.15))
        with self.voiceover(
            "<bookmark mark='a'/> For a rocket of height h with acceleration g, the ticks arrive stretched by a factor of "
            "one plus g h over c squared. <bookmark mark='g'/> And by the equivalence principle, the same must be true in "
            "a gravitational field. A clock lower down, deeper in the potential, really does run slower than one higher "
            "up. Its rate is one plus phi over c squared."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rule))
            vo.wait_until("g")
            self.play(FadeIn(concl, lag_ratio=0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def pound_rebka(self):
        c = load("consts")
        pr = float(c["pound_rebka"])
        assert abs(pr - 2.46e-15) < 0.01e-15
        tower = Rectangle(width=1.4, height=5.0, color=GREY_B, stroke_width=3).move_to([-4.2, -0.4, 0])
        floors = VGroup(*[Line(tower.get_left() + UP * y, tower.get_right() + UP * y, color=GREY_D)
                          for y in np.linspace(-2.0, 2.0, 5)])
        src = Dot(tower.get_bottom() + UP * 0.35, radius=0.1, color=C.MATTER)
        det = Square(0.35, color=WHITE, fill_opacity=0.3).move_to(tower.get_top() + DOWN * 0.35)
        wave = FunctionGraph(lambda y: 0.12 * math.sin(14 * y), x_range=[-2.0, 2.0], color=C.LIGHT)
        wave.rotate(PI / 2).move_to(tower.get_center()).shift(RIGHT * 0.0)
        hlab = MathTex(r"h = 22.5\ \text{m}", font_size=30).next_to(tower, RIGHT, buff=0.3)
        title = label(r"Pound and Rebka, Harvard, 1959", font_size=34).to_corner(UR, buff=0.5).shift(LEFT * 0.4)
        eq = mtex(r"\frac{\Delta\nu}{\nu}", r"=", r"\frac{g h}{c^2}", r"=", sci(pr, 2), font_size=40)
        eq[4].set_color(C.PROPER_TIME)
        res = VGroup(
            label(r"gamma rays from iron-57, read with the Mössbauer effect", font_size=26, color=GREY_A),
            label(r"measured: $1.05 \pm 0.10$ times the prediction (1960)", font_size=28),
            label(r"Pound \& Snider (1965): agreement to 1\%", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        title.move_to([0.9, 2.9, 0], aligned_edge=LEFT)
        VGroup(eq, res).arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(title, DOWN, buff=0.6).align_to(title, LEFT)
        with self.voiceover(
            "This was tested in 1959, in a tower at Harvard. <bookmark mark='t'/> Robert Pound and Glen Rebka sent gamma "
            "rays up and down twenty-two and a half meters. <bookmark mark='e'/> The predicted shift in frequency is g h "
            "over c squared: two and a half parts in a thousand million million. <bookmark mark='r'/> Using an exquisitely "
            "sharp nuclear resonance, they measured it, and found agreement within ten percent, later improved to one "
            "percent."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("t")
            self.play(Create(tower), FadeIn(floors), FadeIn(src), FadeIn(det), FadeIn(hlab))
            self.play(Create(wave), run_time=1.5)
            vo.wait_until("e")
            self.play(Write(eq))
            vo.wait_until("r")
            self.play(FadeIn(res, lag_ratio=0.3), run_time=2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gps(self):
        d = load("gps")
        g_gps, s_gps, n_gps = [float(x) for x in d["gps"]]
        assert f"{g_gps:.1f}" == "45.7" and f"{s_gps:.1f}" == "-7.2" and abs(n_gps - 38.5) < 0.1
        assert abs(float(d["km_per_day"]) - 11.5) < 0.1
        r = d["r"] / 1e6
        ax = Axes(x_range=[0, 50, 10], y_range=[-40, 70, 20], x_length=8.2, y_length=5.0, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": True, "font_size": 22},
                  x_axis_config={"numbers_to_include": [10, 20, 30, 40, 50]},
                  y_axis_config={"numbers_to_include": [-40, -20, 0, 20, 40, 60]})
        ax.to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        xl = label(r"orbit radius (thousand km)", font_size=24).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = label(r"$\mu$s per day vs. a clock on the ground", font_size=24).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.55)
        cg = polyline(ax, r, d["grav"], color=C.GRAV_POTENTIAL, stroke_width=4)
        cs = polyline(ax, r, d["speed"], color=C.METRIC, stroke_width=4)
        cn = polyline(ax, r, d["net"], color=WHITE, stroke_width=5)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(50, 0), color=GREY_C, stroke_width=1.5)
        lg = label(r"higher: faster (gravity)", font_size=24, color=C.GRAV_POTENTIAL).next_to(ax.c2p(50, d["grav"][-1]), UP, buff=0.12).shift(LEFT * 1.4)
        ls = label(r"orbital speed: slower", font_size=24, color=C.METRIC).move_to(ax.c2p(38, -13))
        rg = float(d["r_gps"]) / 1e6
        gdot = Dot(ax.c2p(rg, n_gps), radius=0.09, color=WHITE)
        gl = label(r"GPS", font_size=26).next_to(gdot, DOWN, buff=0.15)
        ri = float(d["r_iss"]) / 1e6
        idot = Dot(ax.c2p(ri, float(d["n_iss"])), radius=0.07, color=WHITE)
        il = label(r"ISS", font_size=24).next_to(idot, RIGHT, buff=0.12)
        rz = float(d["r_zero"]) / 1e6
        zdot = Dot(ax.c2p(rz, 0), radius=0.06, color=GREY_A)
        zl = MathTex(r"\tfrac32 R_\oplus", font_size=26, color=GREY_A).next_to(zdot, UL, buff=0.06)
        nums = VGroup(
            mtex(r"+45.7", r"\ \text{gravity}", font_size=32),
            mtex(r"-7.2", r"\ \text{speed}", font_size=32),
            mtex(r"\approx +38", r"\ \mu\text{s per day}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_corner(UR, buff=0.6)
        nums[0].set_color(C.GRAV_POTENTIAL)
        nums[1].set_color(C.METRIC)
        line = Line(nums[2].get_corner(UL) + UP * 0.12, nums[2].get_corner(UR) + UP * 0.12, color=GREY_C)
        km = VGroup(label(r"uncorrected, positions", font_size=26, color=GREY_A),
                    label(r"drift $\sim$11 km per day", font_size=26, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        km.next_to(nums, DOWN, buff=0.45).align_to(nums, LEFT)
        with self.voiceover(
            "And you rely on it every day. <bookmark mark='g'/> A GPS satellite orbits about twenty-six thousand "
            "kilometers from Earth's center, high up in the potential, so its clock runs faster than yours: by about "
            "forty-six microseconds a day. <bookmark mark='s'/> It also moves at almost four kilometers per second, so "
            "special relativity slows it, by about seven microseconds a day. <bookmark mark='n'/> The net effect: the "
            "satellite clocks gain about thirty-eight microseconds every day. <bookmark mark='k'/> Light travels eleven "
            "kilometers in that time. Without general relativity built into the system, your position would drift by "
            "kilometers a day. The clocks are deliberately tuned slow before launch."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(zero))
            vo.wait_until("g")
            self.play(Create(cg), FadeIn(lg), FadeIn(nums[0]))
            vo.wait_until("s")
            self.play(Create(cs), FadeIn(ls), FadeIn(nums[1]))
            vo.wait_until("n")
            self.play(Create(cn), FadeIn(gdot), FadeIn(gl), FadeIn(idot), FadeIn(il), FadeIn(zdot), FadeIn(zl),
                      Create(line), FadeIn(nums[2]))
            vo.wait_until("k")
            self.play(FadeIn(km))
        self.clear_scene()

    # ------------------------------------------------------------------
    def metric(self):
        rows = stack(
            mtex(r"d\tau", r"=", r"\Big(1 + \frac{\Phi}{c^2}\Big)\,dt", font_size=42),
            mtex(r"c^2 d\tau^2", r"\approx", r"\Big(1 + \frac{2\Phi}{c^2}\Big)\,c^2 dt^2", font_size=42),
            mtex(r"ds^2", r"=", r"-\Big(1 + \frac{2\Phi}{c^2}\Big)\,c^2dt^2", r"+ dx^2 + dy^2 + dz^2", font_size=46),
        )
        for r in rows:
            r[2].set_color(C.PROPER_TIME)
        rows.move_to(UP * 0.4)
        b = Brace(rows[2][2], DOWN, color=C.PROPER_TIME)
        bl = label(r"$g_{00}$: the potential lives in the metric", font_size=28, color=C.PROPER_TIME).next_to(b, DOWN, buff=0.1)
        with self.voiceover(
            "Let's write that as geometry. <bookmark mark='a'/> A clock at rest where the potential is phi ticks at rate "
            "one plus phi over c squared. <bookmark mark='b'/> Squaring, to first order: c squared d tau squared is one "
            "plus two phi over c squared, times c squared d t squared. <bookmark mark='c'/> So the spacetime interval near "
            "a mass looks like this. Newton's potential has become part of the metric: the time-time component, g zero "
            "zero. Space, we'll find later, is warped too. But for anything moving slowly, this is the part that matters, "
            "and in the next chapter we'll see that it is all of Newtonian gravity."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]))
            vo.wait_until("c")
            self.play(Write(rows[2]))
            self.play(GrowFromCenter(b), FadeIn(bl))
        self.clear_scene()
