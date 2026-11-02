from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import ARB, CALL, FWD, PART, Q_C, answer_under, load, pause_at

S3 = np.array([80.0, 100.0, 125.0])


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


class Geometry(VoiceoverScene, ThreeDScene):
    def construct(self):
        f = load("ftap")
        self.card()
        self.space(f)
        self.algebra()
        self.predict()

    def card(self):
        c = chapter_card(3, r"The geometry of arbitrage", r"What does ``no arbitrage'' look like?", lit=(1979,),
                         part=PART)
        with self.voiceover("Chapter three. The geometry of arbitrage."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def space(self, f):
        prices = np.asarray(f["prices"])
        psi = np.asarray(f["psi"])
        ax = ThreeDAxes(x_range=[-1.2, 1.2, 1], y_range=[-1.2, 1.2, 1], z_range=[-1.2, 1.2, 1], x_length=5.4,
                        y_length=5.4, z_length=5.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        o = ax.c2p(0, 0, 0)
        a = 1.15
        faces = VGroup(
            Polygon(o, ax.c2p(a, 0, 0), ax.c2p(a, a, 0), ax.c2p(0, a, 0)),
            Polygon(o, ax.c2p(0, a, 0), ax.c2p(0, a, a), ax.c2p(0, 0, a)),
            Polygon(o, ax.c2p(a, 0, 0), ax.c2p(a, 0, a), ax.c2p(0, 0, a)),
        ).set_stroke(CALL, 1, opacity=0.6).set_fill(CALL, opacity=0.16)
        names = VGroup(*[label(t, font_size=22, color=GREY_A) for t in
                         (r"$x$: pays in state 1 (stock 80)", r"$y$: pays in state 2 (stock 100)",
                          r"$z$: pays in state 3 (stock 125)")]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        names.to_corner(UL, buff=0.35)
        orth = label(r"green box: payoffs that never lose", font_size=20, color=CALL).next_to(names, DOWN, buff=0.2,
                                                                                            aligned_edge=LEFT)
        p = ValueTracker(100.0)

        def psi_at(v):
            v = float(np.clip(v, prices[0], prices[-1]))
            return np.array([np.interp(v, prices, psi[:, j]) for j in range(3)])

        def line():
            d = unit(p.get_value() - S3)
            inside = np.all(d > -1e-9)
            return Line(ax.c2p(*(-1.3 * d)), ax.c2p(*(1.3 * d)), color=ARB if inside else FWD,
                        stroke_width=7 if inside else 5)

        def plane():
            v = p.get_value()
            if v >= 124.5:
                return VGroup()
            d = unit(v - S3)
            n = unit(psi_at(v))
            e2 = unit(np.cross(n, d))
            c = [ax.c2p(*(s1 * 1.25 * d + s2 * 1.0 * e2)) for s1, s2 in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
            pl = Polygon(*c, stroke_width=1, stroke_color=Q_C, fill_color=Q_C, fill_opacity=0.22)
            arr = Arrow3D(o, ax.c2p(*(0.9 * n)), color=Q_C, thickness=0.015, height=0.2, base_radius=0.06)
            return VGroup(pl, arr)

        L = always_redraw(line)
        PL = always_redraw(plane)
        price = DecimalNumber(100, num_decimal_places=0, font_size=34, color=FWD)
        price.add_updater(lambda m: m.set_value(p.get_value()))
        pr = VGroup(label(r"stock price today", font_size=24, color=FWD), price).arrange(RIGHT, buff=0.2)
        comps = VGroup(*[DecimalNumber(0.3, num_decimal_places=3, font_size=28, color=Q_C) for _ in range(3)])
        for j, c_ in enumerate(comps):
            c_.add_updater(lambda m, j=j: m.set_value(psi_at(p.get_value())[j] if p.get_value() < 124.5 else 0.0))
        ps = VGroup(MathTex(r"\psi =", font_size=30, color=Q_C), comps[0], comps[1], comps[2]).arrange(RIGHT, buff=0.18)
        st_ok = label(r"a separating plane exists", font_size=22, color=Q_C)
        st_bad = label(r"no positive normal: arbitrage", font_size=22, color=ARB)
        panel = VGroup(pr, ps, st_ok).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.35)
        st_bad.move_to(st_ok, aligned_edge=LEFT)
        line_note = label(r"blue line: payoffs of portfolios that cost nothing today", font_size=20, color=FWD)
        line_note.to_corner(DL, buff=0.35)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-40 * DEGREES, zoom=0.9)
        self.add_fixed_in_frame_mobjects(names, orth, panel, line_note, st_bad)
        self.remove(names, orth, panel, line_note, st_bad)
        with self.voiceover(
            "Here is what no arbitrage looks like. The one-period market: a bond paying one, and a "
            "stock worth eighty, a hundred, or a hundred and twenty-five. Three states, so a payoff "
            "is a point in three dimensions. <bookmark mark='a'/> The green box holds payoffs that "
            "never lose. An arbitrage is a free portfolio whose payoff lands there, anywhere but the "
            "origin. <bookmark mark='b'/> Which payoffs are free? Short a share and hold bonds worth "
            "its price: at a price of a hundred it pays twenty, nothing, or minus twenty-five. Scaled "
            "and reversed, it traces this blue line. <bookmark mark='c'/> No arbitrage means the line "
            "meets the green corner only at the origin, and then a plane fits through the line with "
            "the corner on one side. Its normal, the purple arrow, is strictly positive."
        ) as vo:
            self.play(FadeIn(names), Create(ax), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(faces), FadeIn(orth))
            vo.wait_until("b")
            self.add(L)
            self.play(FadeIn(line_note), FadeIn(pr))
            vo.wait_until("c")
            self.add(PL)
            self.play(FadeIn(ps), FadeIn(st_ok))
            self.begin_ambient_camera_rotation(rate=0.12)
        with self.voiceover(
            "Raise the stock's price. The line turns, the plane turns with it, and the normal's third "
            "component shrinks. <bookmark mark='a'/> At a hundred and twenty-five it reaches zero: "
            "the plane lies on a face of the corner. <bookmark mark='b'/> Past it, no plane exists: "
            "the line pierces the corner, and shorting the stock against bonds pays in every state, "
            "for nothing. <bookmark mark='c'/> That normal is a vector of state prices, the price "
            "today of a dollar in each state. Separation by a positive normal and no arbitrage are "
            "the same thing."
        ) as vo:
            self.play(p.animate.set_value(124.0), run_time=vo.until("a"), rate_func=smooth)
            self.play(p.animate.set_value(125.0), FadeOut(st_ok), FadeIn(st_bad), run_time=1.2)
            vo.wait_until("b")
            self.play(p.animate.set_value(130.0), run_time=2.0)
            vo.wait_until("c")
            self.play(p.animate.set_value(100.0), FadeOut(st_bad), FadeIn(st_ok), run_time=3.0)
        self.stop_ambient_camera_rotation()
        self.wait(0.3)
        for m in (price, *comps):
            m.clear_updaters()
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0,
                         added_anims=[FadeOut(VGroup(ax, faces, L, PL)), FadeOut(names), FadeOut(orth),
                                      FadeOut(panel), FadeOut(line_note)], run_time=1.5)
        L.clear_updaters()
        PL.clear_updaters()
        self.remove(L, PL)
        self.clear_scene()

    def algebra(self):
        rows = [cmath(r"Z", r"=", r"\{\,D^\top\theta \;:\; \theta\cdot p = 0\,\}", font_size=38, colors={r"Z": FWD}),
                cmath(r"\text{arbitrage}", r"\iff", r"Z \cap \big(\mathbb{R}^3_+ \setminus \{0\}\big) \neq \emptyset",
                      font_size=36, colors={r"\text{arbitrage}": ARB}),
                cmath(r"\psi^\perp \supset Z", r"\iff", r"\psi\cdot D^\top\theta = 0\ \ \text{whenever}\ \ \theta\cdot "
                      r"p = 0", font_size=34, colors={r"\psi^\perp \supset Z": Q_C}),
                cmath(r"D\psi", r"=", r"\lambda\, p\quad\Rightarrow\quad D\psi = p,\ \ \psi > 0", font_size=38,
                      colors={r"D\psi": Q_C})]
        whys = [why(r"$D$: the assets' payoffs (rows) in each state (columns); $p$: their prices; $\theta$: a portfolio"),
                why(r"the definition: a free payoff that is never negative and not zero"),
                why(r"the plane contains the line: its normal is orthogonal to every free payoff"),
                why(r"orthogonal complements: $D\psi$ is orthogonal to every $\theta$ with $\theta\cdot p = 0$, so it is a "
                    r"multiple of $p$; rescale. Chapter 4 proves such a $\psi > 0$ exists exactly when there is no "
                    r"arbitrage")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-0.8, buff=0.6, edge=6.9)
        with self.voiceover(
            "In symbols. D holds the payoffs, a row per asset, a column per state; p the prices. The "
            "free payoffs are D transpose theta for portfolios theta that cost nothing. <bookmark "
            "mark='a'/> An arbitrage is a free payoff in the corner, other than zero. <bookmark "
            "mark='b'/> The plane with normal psi contains the line when psi is orthogonal to every "
            "free payoff. <bookmark mark='c'/> Then D psi is orthogonal to every costless portfolio, "
            "so it is a multiple of the prices; rescale, and D psi equals p. The next chapter proves "
            "a positive psi exists exactly when there is no arbitrage."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"At a stock price of exactly 125, is there an arbitrage? The plane still exists, lying on a "
                        r"face of the corner.")
        with self.voiceover(
            "Pause and predict. At exactly a hundred and twenty-five, is there an arbitrage? "
            "<bookmark mark='a'/> Yes: short a share, hold a hundred and twenty-five in bonds. It "
            "costs nothing and pays forty-five, twenty-five or zero. A state price of zero is not "
            "positive enough."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"yes: short a share, hold 125 in bonds; cost 0, payoff $(45, 25, 0)$. "
                                                r"The normal has $\psi_3 = 0$: state prices must be strictly "
                                                r"positive")))
        self.wait(0.4)
        self.clear_scene()
