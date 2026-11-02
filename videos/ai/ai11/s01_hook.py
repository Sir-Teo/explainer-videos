from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import OPT_COLORS, OPT_NAMES, PART, SAY, era_strip, load
from videos.ai.ai11.compute import rosen


def height(x, y):
    return math.log1p(rosen(x, y))


def step_path(points, step):
    """A visual path prefix at a shared optimization step, not arc length.

    Interpolate only between adjacent cached states; at step zero show a
    degenerate segment rather than leaking the first update into the preview.
    """
    points = np.asarray(points)
    position = min(max(float(step), 0.0), len(points) - 1)
    index = int(position)
    prefix = points[:index + 1]
    if index < len(points) - 1 and position > index:
        point = points[index] + (position - index) * (points[index + 1] - points[index])
        prefix = np.vstack((prefix, point))
    return prefix if len(prefix) > 1 else np.repeat(prefix, 2, axis=0)


class Hook(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.race()
        self.era()
        self.plan()

    # ------------------------------------------------------------------
    def race(self):
        r = load("race3d")
        names = list(r["names"])
        steps = int(r["steps"])
        reach = {n: int(r[f"reach_{n}"]) for n in names}
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-1, 3, 1], z_range=[0, 5, 1], x_length=8.0, y_length=6.0,
                          z_length=2.6, axis_config={"stroke_color": GREY_D, "include_ticks": False, "include_tip": False})
        axes.shift(DOWN * 0.6)
        surf = loss_surface(axes, height, [-2, 2], [-1, 3], resolution=(48, 48), z_lo=0.0, z_hi=5.0, opacity=0.78)
        goal = Dot3D(axes.c2p(1, 1, 0) + OUT * 0.06, radius=0.09, color=WHITE)
        step = ValueTracker(0)
        runners = {}
        for n in names:
            P = np.asarray(r[f"path_{n}"])
            col = WHITE if n == "gd" else OPT_COLORS[n]  # grey would vanish on the surface
            trace_points = np.array([axes.c2p(x, y, height(x, y)) + OUT * 0.06 for x, y in P])
            ball_points = trace_points + OUT * (0.11 * 0.6 - 0.06)
            trail = always_redraw(lambda points=trace_points, color=col: VMobject(color=color, stroke_width=4)
                                  .set_points_as_corners(step_path(points, step.get_value())))
            ball = surface_ball(axes, height, *P[0], color=col, radius=0.11)
            ball.add_updater(lambda m, points=ball_points: m.move_to(step_path(points, step.get_value())[-1]))
            runners[n] = (trail, ball)
        key = VGroup(*[label(OPT_NAMES[n], font_size=26, color=WHITE if n == "gd" else OPT_COLORS[n]) for n in names]).arrange(RIGHT, buff=0.7)
        key.to_edge(UP, buff=0.4)
        tally = VGroup(*[label(rf"${reach[n]}$ steps" if reach[n] >= 0 else r"not yet", font_size=22,
                               color=OPT_COLORS[n]).next_to(key[i], DOWN, buff=0.12) for i, n in enumerate(names)])
        for n, count in zip(names, tally):
            # A visible first-hit cue remains readable even when the 3D valley
            # lip occludes an arriving ball. It is not a convergence claim.
            count.add_updater(lambda m, n=n: m.set_opacity(
                1 if reach[n] >= 0 and step.get_value() >= reach[n] else 0))
        tag = label(rf"Rosenbrock's curved valley; \ each optimizer at its best of ${len(r['lrs'])}$ learning rates, "
                    rf"\ ${steps}$ steps", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.3)
        tl = label(r"steps until the loss is below $0.01$", font_size=20, color=GREY_A).next_to(tag, UP, buff=0.18)
        # A moving 3D corner can enter the label band even when the initial
        # camera pose clears it. Keep this screen-space legend unoccluded.
        legend_backing = Rectangle(width=config.frame_width, height=1.15, stroke_width=0,
                                   fill_color=BACKGROUND, fill_opacity=1).to_edge(UP, buff=0).set_z_index(20)
        for m in (key, tally, tag, tl):
            m.set_z_index(21)
        # Reserve the final count's width before placing the fixed denominator.
        counter = VGroup(label(r"step", font_size=22, color=GREY_A), Integer(steps, font_size=22),
                         MathTex(rf"/ {steps}", font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.12)
        counter.to_corner(UR, buff=0.3)

        def update_counter(m):
            # Integer.set_value replaces its glyph objects. Register the new
            # family with the 3D camera too, so the digits stay on screen.
            self.camera.remove_fixed_in_frame_mobjects(m)
            m.set_value(step.get_value())
            m.set_z_index(21)
            self.camera.add_fixed_in_frame_mobjects(m)

        update_counter(counter[1])
        counter[1].add_updater(update_counter)
        counter.set_z_index(21)
        for m in (key, tally, tag, tl, counter, legend_backing):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        order = sorted([n for n in names if reach[n] >= 0], key=lambda n: reach[n])
        first, last = order[0], ([n for n in names if reach[n] < 0] or order[-1:])[-1]
        slow_never = reach[last] < 0
        self.set_camera_orientation(phi=45 * DEGREES, theta=-120 * DEGREES, zoom=0.72)
        said1 = (f"{SAY.get(last, last).capitalize()} never quite does: it is still crawling along the floor of the valley."
            if slow_never else
            f"{SAY.get(last, last).capitalize()} takes {reach[last]}, crawling along the floor of the valley.")
        with self.voiceover(
            "Every model in this series learns by walking downhill on its loss. But how you walk matters enormously. "
            "<bookmark mark='a'/> Here is a famous curved valley, Rosenbrock's, with its lowest point marked in white, "
            "and four walkers starting from the same place, each with its best step size from a grid of "
            f"{len(r['lrs'])}. <bookmark mark='b'/> Plain gradient descent, the heavy ball, Adam, and Lion. "
            f"<bookmark mark='c'/> In {steps} steps, {SAY.get(first, first)} gets there first, in {reach[first]} steps. "
            + said1
            + " This part is about why."
        ) as vo:
            self.play(FadeIn(surf), FadeIn(goal), FadeIn(tag), run_time=1.5)
            self.begin_ambient_camera_rotation(rate=0.08)
            vo.wait_until("a")
            self.play(*[FadeIn(rn[1]) for rn in runners.values()])
            vo.wait_until("b")
            self.play(FadeIn(legend_backing), FadeIn(key), FadeIn(counter), FadeIn(tl))
            self.add(tally)
            self.add(*[rn[0] for rn in runners.values()])
            self.play(step.animate.set_value(steps), run_time=6.0, rate_func=linear)
            for rn in runners.values():
                for m in rn:
                    m.clear_updaters()
            for count in tally:
                count.clear_updaters()
            counter[1].clear_updaters()
            self.stop_ambient_camera_rotation()
            vo.wait_until("c")
            self.move_camera(phi=0, theta=-90 * DEGREES, zoom=0.66, frame_center=axes.c2p(0, 1, 0), run_time=2.0)
            self.play(FadeOut(counter), *[FadeIn(tally[i]) for i, n in enumerate(names) if reach[n] < 0])
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=ORIGIN)

    # ------------------------------------------------------------------
    def era(self):
        events = [
            (1847, r"Cauchy: \\ steepest \\ descent"),
            (1951, r"Robbins, Monro: \\ noisy steps \\ that converge"),
            (1964, r"Polyak: \\ the heavy \\ ball"),
            (1983, r"Nesterov: \\ acceleration"),
            (1986, r"backpropagation, \\ SGD with \\ momentum"),
            (2011, r"AdaGrad: \\ a step size \\ per weight"),
            (2012, r"RMSProp, \\ on a lecture \\ slide"),
            (2014, r"Adam"),
            (2018, r"Shampoo: \\ whole-matrix \\ preconditioning"),
            (2024, r"Muon; \\ the AlgoPerf \\ contest"),
            (2025, r"MuonClip \\ trains Kimi K2: \\ a trillion weights"),
            (2026, r"DeepSeek-V4, \\ trained \\ with Muon"),
        ]
        head, axis, tag, skel, marks = era_strip(events, font_size=19)
        with self.voiceover(
            "The idea is old. In 1847, Augustin Cauchy, solving the equations of planetary orbits, proposed stepping "
            "against the gradient: steepest descent. <bookmark mark='a'/> In 1951, Herbert Robbins and Sutton Monro "
            "showed that steps along noisy estimates still converge, if the steps shrink at the right rate. "
            "<bookmark mark='b'/> In 1964, Boris Polyak added momentum: a heavy ball. <bookmark mark='c'/> In 1983, "
            "Yurii Nesterov found the provably fastest way to use it. <bookmark mark='d'/> In 1986, backpropagation "
            "made gradients of networks cheap, and networks were trained by stochastic gradient descent with momentum "
            "for the next twenty-five years. <bookmark mark='e'/> Then came step sizes for every weight: AdaGrad in "
            "2011, <bookmark mark='f'/> RMSProp in 2012, which was never published as a paper, only as a slide in "
            "Geoffrey Hinton's online course, <bookmark mark='g'/> and Adam in 2014, which trained almost everything "
            "for a decade. <bookmark mark='h'/> In 2018, Shampoo preconditioned whole matrices. "
            "<bookmark mark='i'/> In 2024, a public benchmark, AlgoPerf, measured the contenders fairly, and a new "
            "optimizer, Muon, appeared in a speedrun. <bookmark mark='j'/> In 2025 a version of it, MuonClip, "
            "trained Kimi K2, a model with a trillion parameters, <bookmark mark='k'/> and in 2026 DeepSeek trained "
            "its fourth generation with Muon too."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(tag), FadeIn(skel))
            self.play(FadeIn(marks[0], shift=UP * 0.2))
            for k, mk in enumerate("abcdefghijk"):
                vo.wait_until(mk)
                self.play(FadeIn(marks[k + 1], shift=(UP if (k + 1) % 2 == 0 else DOWN) * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Going Downhill", font_size=48).to_edge(UP, buff=0.45)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.5)
        obj = objectives_card([
            r"gradient descent's rates, derived; \ momentum and acceleration on quadratics",
            r"noisy gradients: \ SGD as a random walk with a temperature $\eta/B$; \ the edge of stability",
            r"Adam derived; \ weight decay is not L2; \ Lion",
            r"geometry: \ the natural gradient, K-FAC, Shampoo, SOAP, \ and Muon with Newton--Schulz",
            r"a fair race on our own character model; \ schedules, the river valley, schedule-free",
            r"keeping training stable; \ and the optimizer race of 2024--2026",
        ], font_size=24).move_to(DOWN * 0.35)
        with self.voiceover(
            "This is Part 11 of AI, Built. <bookmark mark='a'/> In it: why gradient descent converges, and how fast; "
            "momentum; what the noise of small batches does; why training lives at the edge of instability; how "
            "Adam is built, and why weight decay is not what it seems; optimizers that see the geometry of whole "
            "matrices, ending with Muon; a fair race between them on our own model; schedules; and how the field "
            "keeps very large runs from blowing up."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
