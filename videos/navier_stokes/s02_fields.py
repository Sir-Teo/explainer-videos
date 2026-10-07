from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.navier_stokes.common import heatmap, label, pressure_colormap

# A smooth, divergence-free "swirly" flow: uniform stream + three smoothed vortices.
U0 = 0.55
VORTICES = [((-3.2, 1.0), 5.5, 0.85), ((2.4, -1.1), -5.0, 0.9), ((0.4, 2.4), 3.0, 0.6)]


def flow(p):
    x, y = p[0], p[1]
    u, v = U0, 0.0
    for (cx, cy), g, a in VORTICES:
        dx, dy = x - cx, y - cy
        r2 = dx * dx + dy * dy + 1e-9
        f = g / (2 * np.pi * r2) * (1 - np.exp(-r2 / a**2))
        u += -f * dy
        v += f * dx
    return np.array([u, v, 0.0])


def pressure(X, Y):
    p = np.zeros_like(X)
    for (cx, cy), g, a in VORTICES:
        p -= (g / 5) ** 2 * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (1.3 * a) ** 2)
    return p


def blue_field(**kw):
    return ArrowVectorField(
        flow,
        x_range=[-7, 7, 0.55],
        y_range=[-3.9, 3.9, 0.55],
        colors=[BLUE_E, BLUE_C, BLUE_A],
        min_color_scheme_value=0.1,
        max_color_scheme_value=1.3,
        length_func=lambda n: 0.5 * np.tanh(1.6 * n),
        **kw,
    )


class VelocityField(VoiceoverScene):
    def construct(self):
        rng = np.random.default_rng(1)

        # --- 1. Molecules ------------------------------------------------------
        box = RoundedRectangle(width=6, height=4, corner_radius=0.2, color=GREY_B)
        mols = VGroup(*[Dot(radius=0.05, color=BLUE_B) for _ in range(140)])
        for d in mols:
            d.move_to([rng.uniform(-2.8, 2.8), rng.uniform(-1.8, 1.8), 0])

        def jitter(group, dt):
            for d in group:
                p = d.get_center() + rng.normal(0, 0.7, 3) * np.sqrt(dt) * np.array([1, 1, 0])
                p[0] = np.clip(p[0], -2.85, 2.85)
                p[1] = np.clip(p[1], -1.85, 1.85)
                d.move_to(p)

        mols.add_updater(jitter)
        count = MathTex(r"\sim 10^{25}", r"\text{ molecules}", font_size=40).next_to(box, UP, buff=0.3)

        with self.voiceover(
            "So, how do you even describe a fluid? A glass of water holds roughly "
            "<bookmark mark='n'/> ten to the twenty-five molecules, all jostling around, colliding "
            "billions of times per second. Tracking each one is hopeless."
        ) as vo:
            self.play(Create(box), FadeIn(mols, lag_ratio=0.02), run_time=2)
            vo.wait_until("n")
            self.play(Write(count))

        # --- 2. Continuum: zoom out -------------------------------------------
        field = blue_field()
        with self.voiceover(
            "So we zoom out. We pretend the fluid is a smooth, continuous substance, and at every point "
            "in space we ask just one question: <bookmark mark='q'/> which way, and how fast, is the fluid moving "
            "right here?"
        ) as vo:
            mols.clear_updaters()
            self.play(FadeOut(count), run_time=0.5)
            self.play(
                box.animate.scale(3).set_stroke(opacity=0),
                mols.animate.scale(3).set_opacity(0),
                run_time=2.5,
            )
            self.remove(box, mols)
            self.play(Create(field, lag_ratio=0.01), run_time=vo.until("q") + 1.5)

        # --- 3. One vector ----------------------------------------------------
        pt = np.array([-0.6, -2.1, 0])
        dot = Dot(pt, color=WHITE, radius=0.07)
        vec = flow(pt)
        big = Arrow(pt, pt + 1.6 * vec / np.linalg.norm(vec), buff=0, color=C.VELOCITY, stroke_width=7)
        u_lab = MathTex(r"\vu(\vx, t)", color=C.VELOCITY, font_size=48)
        u_lab.add_background_rectangle(opacity=0.85, buff=0.1)
        u_lab.next_to(big.get_end(), UR, buff=0.1)

        with self.voiceover(
            "The answer is a vector, which we'll call u, and color blue throughout this video. "
            "Its direction is the direction of flow, <bookmark mark='len'/> and its length is the speed."
        ) as vo:
            self.play(field.animate.set_opacity(0.25), FadeIn(dot, scale=0.5))
            self.play(GrowArrow(big))
            vo.wait_until("len")
            brace = BraceBetweenPoints(big.get_start(), big.get_end(), direction=rotate_vector(normalize(vec), -PI / 2))
            speed = MathTex(r"|\vu| = \text{speed}", font_size=34).next_to(brace.get_tip(), DOWN, buff=0.1)
            speed.add_background_rectangle(opacity=0.85, buff=0.08)
            self.play(GrowFromCenter(brace), FadeIn(speed))

        comps = MathTex(r"\vu", r"=", r"(u,\ v,\ w)", font_size=44)
        comps[0].set_color(C.VELOCITY)
        comps.add_background_rectangle(opacity=0.85, buff=0.12)
        comps.to_corner(UL, buff=0.5)
        with self.voiceover(
            "Do this at every point and you get a velocity field, written <bookmark mark='ux'/> u of x and t, "
            "since it depends on position and on time. In three dimensions it has "
            "<bookmark mark='c'/> three components: u, v, and w."
        ) as vo:
            self.play(FadeOut(brace), FadeOut(speed), field.animate.set_opacity(1))
            vo.wait_until("ux")
            self.play(Write(u_lab))
            vo.wait_until("c")
            self.play(FadeIn(comps, shift=DOWN * 0.2))

        # --- 4. Dust specks ---------------------------------------------------
        specks = VGroup(*[Dot(radius=0.035, color=GREY_A) for _ in range(170)])
        for s in specks:
            s.move_to([rng.uniform(-7.2, 7.2), rng.uniform(-3.9, 3.9), 0])

        def advect(group, dt):
            for s in group:
                p = s.get_center()
                k1 = flow(p)
                k2 = flow(p + 0.5 * dt * k1)
                p = p + dt * k2
                if p[0] > 7.3 or abs(p[1]) > 4.2:
                    p = np.array([-7.3, rng.uniform(-3.9, 3.9), 0])
                s.move_to(p)

        specks.add_updater(advect)
        with self.voiceover(
            "If you sprinkle tiny specks of dust into the flow, they get carried along by these arrows, "
            "tracing out the motion of the fluid."
        ) as vo:
            self.play(FadeOut(dot), FadeOut(big), FadeOut(u_lab), field.animate.set_opacity(0.45))
            self.play(FadeIn(specks, lag_ratio=0.01), run_time=1.5)

        # --- 5. Pressure ------------------------------------------------------
        pmap = heatmap(pressure, (-7.2, 7.2), (-4.1, 4.1), resolution=160,
                       colormap=pressure_colormap(-1.25, 1.3), opacity=0.9)
        p_lab = MathTex(r"p(\vx, t)", color=C.PRESSURE, font_size=48)
        p_lab.add_background_rectangle(opacity=0.85, buff=0.1)
        p_lab.next_to(comps, DOWN, buff=0.3, aligned_edge=LEFT)
        lo_lab = label(r"low $p$", color=WHITE, font_size=28).move_to(np.array([*VORTICES[0][0], 0]) + np.array([0, -1.35, 0]))
        lo_lab.add_background_rectangle(opacity=0.7, buff=0.06)
        with self.voiceover(
            "We'll need one more field: <bookmark mark='p'/> pressure, a single number at each point, colored in red. "
            "You can think of it as how tightly the fluid is being squeezed at that spot. "
            "<bookmark mark='low'/> Notice that it's lowest in the middle of each swirl. Hold on to that; we'll see why soon."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(pmap), run_time=1.5)
            self.bring_to_back(pmap)
            self.play(Write(p_lab))
            vo.wait_until("low")
            self.play(FadeIn(lo_lab, shift=UP * 0.2))

        # --- 6. Unknowns ------------------------------------------------------
        card = VGroup(
            Tex(r"Unknowns", font_size=44),
            MathTex(r"\vu = (u, v, w)", r"\quad", r"\text{3 velocity components}", font_size=36),
            MathTex(r"p", r"\quad", r"\text{pressure}", font_size=36),
            MathTex(r"4", r"\text{ unknown functions of } (x, y, z, t)", font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        card[1][0].set_color(C.VELOCITY)
        card[2][0].set_color(C.PRESSURE)
        card[3][0].set_color(YELLOW)
        card[0].set_x(card.get_center()[0])
        bg = BackgroundRectangle(card, fill_opacity=0.92, buff=0.4, corner_radius=0.15)
        bg.set_stroke(GREY_B, 1.5, opacity=1)
        with self.voiceover(
            "So the unknowns are the three components of velocity, and the pressure: "
            "four unknown functions of space and time. The Navier–Stokes equations are the rules "
            "that determine how these fields evolve."
        ) as vo:
            self.play(FadeOut(lo_lab), FadeIn(bg), FadeIn(card[0]))
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in card[1:]], lag_ratio=0.6), run_time=3)
        self.wait(0.5)
        self.clear_scene()
