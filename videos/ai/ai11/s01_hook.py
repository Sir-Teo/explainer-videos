from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import OPT_COLORS, OPT_NAMES, PART, SAY, era_strip, load
from videos.ai.ai11.compute import rosen


def height(x, y):
    return math.log1p(rosen(x, y))


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
        runners = {}
        for n in names:
            P = np.asarray(r[f"path_{n}"])
            col = WHITE if n == "gd" else OPT_COLORS[n]  # grey would vanish on the surface
            trail = surface_path(axes, height, P, color=col, lift=0.06, stroke_width=4)
            track = surface_path(axes, height, P, color=col, lift=0.1)
            ball = surface_ball(axes, height, *P[0], color=col, radius=0.11)
            runners[n] = (trail, ball, track)
        key = VGroup(*[label(OPT_NAMES[n], font_size=26, color=WHITE if n == "gd" else OPT_COLORS[n]) for n in names]).arrange(RIGHT, buff=0.7)
        key.to_edge(UP, buff=0.4)
        tally = VGroup(*[label(rf"${reach[n]}$ steps" if reach[n] >= 0 else r"not yet", font_size=22,
                               color=OPT_COLORS[n]).next_to(key[i], DOWN, buff=0.12) for i, n in enumerate(names)])
        tag = label(rf"Rosenbrock's curved valley; \ each optimizer at its best of ${len(r['lrs'])}$ learning rates, "
                    rf"\ ${steps}$ steps", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.3)
        tl = label(r"steps until the loss is below $0.01$", font_size=20, color=GREY_A).next_to(tally, DOWN, buff=0.12)
        for m in (key, tally, tag, tl):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        order = sorted([n for n in names if reach[n] >= 0], key=lambda n: reach[n])
        first, last = order[0], ([n for n in names if reach[n] < 0] or order[-1:])[-1]
        slow_never = reach[last] < 0
        self.set_camera_orientation(phi=62 * DEGREES, theta=-120 * DEGREES, zoom=0.8)
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
            self.play(FadeIn(key))
            self.play(*[Create(rn[0]) for rn in runners.values()],
                      *[MoveAlongPath(rn[1], rn[2]) for rn in runners.values()], run_time=6.0, rate_func=linear)
            self.stop_ambient_camera_rotation()
            vo.wait_until("c")
            self.move_camera(phi=0, theta=-90 * DEGREES, zoom=0.66, frame_center=axes.c2p(0, 1, 0), run_time=2.0)
            self.play(FadeIn(tally), FadeIn(tl))
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
