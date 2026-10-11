from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2.common import (label, ladder, load, mtex, note, part_card, redraw, under)
from videos.relativity2.geometry import check_kerr_thermo

HOR, ENT, TEMP = C.CURVATURE, C.ENTROPY, C.TEMPERATURE


class Thermodynamics(VoiceoverScene):
    def construct(self):
        assert check_kerr_thermo() == "ok"
        self.card()
        self.bekenstein()
        self.surface_gravity()
        self.first_law()
        self.laws()

    def card(self):
        c = part_card("IV", r"Black holes and quantum theory", r"the laws of black-hole mechanics; Hawking radiation")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def bekenstein(self):
        cen = np.array([2.6, -0.6, 0])
        hole = Circle(radius=1.2, color=HOR, stroke_width=4, fill_color=BLACK, fill_opacity=1).move_to(cen)
        rng = np.random.default_rng(4)
        box0 = np.array([-3.4, 0.9, 0])
        k = ValueTracker(0.0)
        P = rng.uniform(-0.45, 0.45, (40, 2))
        V = rng.normal(size=(40, 2))

        def box():
            s = k.get_value()
            c0 = box0 + s * (cen - box0)
            scale = 1 - 0.85 * s
            g = VGroup(Square(side_length=1.0 * scale, color=TEMP, stroke_width=3).move_to(c0))
            t = 3 * s + 0.0
            pts = P + 0.15 * np.sin(V * (t + 1) * 4)
            pts = np.clip(pts, -0.45, 0.45) * scale
            g.add(*[Dot(c0 + np.array([x, y, 0]), radius=0.035 * max(scale, 0.3), color=TEMP) for x, y in pts])
            g.set_opacity(1 if s < 0.97 else 0)
            return g

        B = redraw(box)
        txt = VGroup(
            label(r"a box of hot gas carries entropy $S$", font_size=28, color=TEMP),
            label(r"drop it in: the entropy outside goes down", font_size=28),
            label(r"the second law fails \dots", font_size=28),
            label(r"\dots unless the black hole has entropy, and it grows:", font_size=28),
            mtex(r"S_{\rm BH} \propto A", font_size=44, color=ENT),
            label(r"Jacob Bekenstein (1972--73), a student of Wheeler's", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        with self.voiceover(
            "In 1972, Jacob Bekenstein, a graduate student of John Wheeler's, asked a simple question. "
            "<bookmark mark='a'/> Take a box of hot gas, which has entropy, <bookmark mark='b'/> and drop it into a "
            "black hole. From the outside, the gas and its entropy are simply gone, so the total entropy of the "
            "universe outside has gone down, violating the second law of thermodynamics. "
            "<bookmark mark='c'/> Unless the black hole itself has entropy, which grows when things fall in. And there "
            "was an obvious candidate: the one property of a black hole that, like entropy, can only increase. Its "
            "area."
        ) as vo:
            self.play(FadeIn(hole))
            vo.wait_until("a")
            self.add(B)
            self.play(FadeIn(txt[0]))
            vo.wait_until("b")
            self.play(k.animate.set_value(1.0), FadeIn(txt[1:3], lag_ratio=0.5), run_time=4, rate_func=rate_functions.ease_in_quad)
            vo.wait_until("c")
            self.play(FadeIn(txt[3:], lag_ratio=0.3), Indicate(hole, color=ENT))
        B.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def surface_gravity(self):
        rows = [
            mtex(r"a_{\rm hover}", r"=", r"\frac{M}{r^2\sqrt{1 - 2M/r}}", font_size=42),
            mtex(r"\kappa", r"=", r"\lim_{r\to 2M}\ \sqrt{1 - \frac{2M}{r}}\;a_{\rm hover} = \frac{1}{4M}", font_size=42),
            mtex(r"\kappa", r"=", r"\frac{r_+ - M}{r_+^2 + a^2}", font_size=42),
        ]
        whys = [
            note(r"the acceleration a rocket needs to hover at $r$: it diverges at the horizon"),
            note(r"as measured from far away (times the redshift factor): the surface gravity (checked symbolically)"),
            note(r"for Kerr; it is the same everywhere on the horizon, and vanishes for an extremal hole ($a = M$)"),
        ]
        for r in rows:
            r[0].set_color(TEMP)
        under(rows, whys, -0.6)
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.8)
        with self.voiceover(
            "If area is like entropy, what's like temperature? <bookmark mark='a'/> Hover a rocket above a black hole. "
            "The acceleration it needs grows without bound as it nears the horizon. <bookmark mark='b'/> But measured "
            "from far away, redshifted by the same factor that slows its clocks, it tends to a finite limit: one over "
            "four M. This is the surface gravity, kappa. <bookmark mark='c'/> For a spinning hole it's this, and it "
            "turns out to be the same everywhere on the horizon of any stationary black hole, just as temperature is "
            "the same everywhere in a body in equilibrium."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def first_law(self):
        rows = [
            mtex(r"A", r"=", r"4\pi\big(r_+^2 + a^2\big) = 8\pi\Big(M^2 + \sqrt{M^4 - J^2}\Big)", font_size=40),
            mtex(r"\Big(\frac{\partial M}{\partial A}\Big)_J", r"=", r"\frac{\kappa}{8\pi},\qquad \Big(\frac{\partial M}{\partial J}\Big)_A = \Omega_H",
                 font_size=40),
            mtex(r"dM", r"=", r"\frac{\kappa}{8\pi}\,dA + \Omega_H\,dJ", font_size=48),
            mtex(r"dE", r"=", r"T\,dS + \text{work}", font_size=44),
        ]
        whys = [
            note(r"the Kerr horizon's area, as a function of mass and angular momentum ($J = aM$)"),
            note(r"differentiate (checked symbolically)"),
            note(r"the first law of black-hole mechanics"),
            note(r"the first law of thermodynamics: \ $T \propto \kappa$, \ $S \propto A$"),
        ]
        rows[0][0].set_color(HOR)
        rows[2][0].set_color(C.MATTER)
        rows[3][0].set_color(C.MATTER)
        rows[3][2].set_color(TEMP)
        under(rows, whys, -0.8)
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.62)
        with self.voiceover(
            "The analogy goes deeper. <bookmark mark='a'/> The area of a Kerr horizon is a function of the hole's mass "
            "and angular momentum. <bookmark mark='b'/> Differentiate it: the partial derivatives are exactly the "
            "surface gravity over eight pi, and the horizon's angular velocity. <bookmark mark='c'/> So a small change "
            "in mass splits into kappa over eight pi times the change in area, plus Omega H times the change in "
            "angular momentum: the work done spinning it up. <bookmark mark='d'/> Compare the first law of "
            "thermodynamics: energy changes by temperature times entropy change, plus work. Temperature goes with "
            "kappa; entropy goes with area."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def laws(self):
        heads = [r"", r"thermodynamics", r"black holes"]
        rows = [
            (r"0th", r"$T$ is uniform in equilibrium", r"$\kappa$ is uniform on the horizon"),
            (r"1st", r"$dE = T\,dS + $ work", r"$dM = \tfrac{\kappa}{8\pi}dA + \Omega_H\,dJ$"),
            (r"2nd", r"$dS \ge 0$", r"$dA \ge 0$"),
            (r"3rd", r"$T = 0$ can't be reached", r"$\kappa = 0$ can't be reached"),
        ]
        tbl = VGroup()
        xs = [-5.4, -1.6, 3.2]
        for j, h in enumerate(heads):
            tbl.add(label(h, font_size=30, color=[WHITE, TEMP, HOR][j]).move_to([xs[j], 2.2, 0]))
        for i, (a_, b_, c_) in enumerate(rows):
            y = 1.25 - 0.85 * i
            tbl.add(label(a_, font_size=28, color=GREY_A).move_to([xs[0], y, 0]))
            tbl.add(label(b_, font_size=28).move_to([xs[1], y, 0]))
            tbl.add(label(c_, font_size=28).move_to([xs[2], y, 0]))
        line = Line([-6.4, 1.8, 0], [6.4, 1.8, 0], color=GREY_C, stroke_width=1.5)
        hdr = label(r"Bardeen, Carter \& Hawking (1973): the four laws of black-hole mechanics", font_size=28).to_edge(UP, buff=0.4)
        catch = VGroup(
            label(r"But a black hole absorbs everything and emits nothing:", font_size=28),
            label(r"classically, its temperature must be zero. \ Just an analogy?", font_size=28, color=TEMP),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1973, James Bardeen, Brandon Carter and Stephen Hawking laid out the full parallel. "
            "<bookmark mark='a'/> The zeroth law: surface gravity is uniform on the horizon, like temperature in "
            "equilibrium. The first law we've just derived. The second law is the area theorem. And the third: you "
            "can't reduce kappa to zero, an extremal black hole, in a finite number of steps, just as you can't reach "
            "absolute zero. <bookmark mark='b'/> But there was a catch, and Hawking himself insisted on it. A body with "
            "a temperature radiates. A black hole, classically, absorbs everything and emits nothing, so its "
            "temperature must be zero. The analogy looked like just that: an analogy."
        ) as vo:
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(tbl, lag_ratio=0.05), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(catch, lag_ratio=0.3))
        self.clear_scene()
