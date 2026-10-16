from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import DATA, SCORE, follow, load, ramp, swarm

K = 1.3  # the computed plane, drawn 1.3 times life size


def score_at(data, x, t, s0=0.03):
    """The exact score of the noised letters at time t (the same formula as compute.py)."""
    a = math.exp(-t)
    mu, var = math.sqrt(a) * data, a * s0 ** 2 + 1 - a
    d2 = ((x[:, None, :] - mu[None]) ** 2).sum(-1)
    w = np.exp(-(d2 - d2.min(1, keepdims=True)) / (2 * var))
    w /= w.sum(1, keepdims=True)
    return (w @ mu - x) / var


class Hook(VoiceoverScene):
    def construct(self):
        self.out_of_noise()
        self.plan()

    # ------------------------------------------------------------------
    def out_of_noise(self):
        s = load("shape")
        data, bwd, fwd = np.asarray(s["data"]), np.asarray(s["bwd"]), np.asarray(s["fwd"])
        assert s["final_med"] < 0.1
        n = len(bwd) - 1
        T = float(s["T"])
        cols = ramp(bwd[-1][:, 0] + 0.35 * bwd[-1][:, 1], DATA, C.BITS)
        dots = swarm(bwd[0] * K, cols)
        t = ValueTracker(0.0)
        dots.add_updater(follow(dots, bwd, t, scale=K))
        gx, gy = np.linspace(-5.6, 5.6, 19), np.linspace(-3.1, 3.1, 11)
        G = np.stack(np.meshgrid(gx, gy), -1).reshape(-1, 2)

        def field():
            tt = max(T * (1 - t.get_value() / n), 0.06)
            S = score_at(data, G / K, tt)
            mag = np.linalg.norm(S, axis=1) + 1e-9
            ref = np.percentile(mag, 90)
            out = VGroup()
            for p, v, m in zip(G, S, mag):
                L = 0.42 * min(1.0, m / ref)
                out.add(Arrow([p[0], p[1], 0], [p[0] + L * v[0] / m, p[1] + L * v[1] / m, 0], buff=0, color=SCORE,
                              stroke_width=2, max_tip_length_to_length_ratio=0.35, stroke_opacity=0.45,
                              fill_opacity=0.45))
            return out

        arrows = always_redraw(field)
        with self.voiceover(
            "Here are six hundred dots, scattered completely at random. <bookmark mark='a'/> Now let each one wander. "
            "At every moment it gets a small random kick, plus a gentle push from a field of arrows. "
            "<bookmark mark='b'/> Watch what the randomness builds."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.002), run_time=2.0)
            self.add(dots)  # the group itself, so its updater runs
            vo.wait_until("a")
            self.play(FadeIn(arrows), run_time=1.0)
            vo.wait_until("b")
        with self.voiceover(
            "This is, in miniature, how today's image and video generators work. They start from noise and let it "
            "flow, one random step at a time, into a picture. <bookmark mark='a'/> The arrows are the whole secret: "
            "they're what a network learns. We'll build them in part fourteen."
        ) as vo:
            self.play(t.animate.set_value(n), run_time=9.0, rate_func=lambda a: 1 - (1 - a) ** 2.2)
            arrows.clear_updaters()
            vo.wait_until("a")
            self.play(FadeOut(arrows))
        dots.clear_updaters()
        # and back: the letters dissolve
        start = fwd[0]
        cols2 = ramp(start[:, 0] + 0.35 * start[:, 1], DATA, C.BITS)
        new = swarm(start * K, cols2)
        t2 = ValueTracker(0.0)
        with self.voiceover(
            "Run it the other way, with the arrows gone, and the letters dissolve back into noise. "
            "<bookmark mark='a'/> Both directions are random motion, and the same mathematics describes them."
        ) as vo:
            self.play(FadeOut(dots), FadeIn(new), run_time=0.8)
            new.add_updater(follow(new, fwd, t2, scale=K))
            self.play(t2.animate.set_value(len(fwd) - 1), run_time=5.0, rate_func=lambda a: a ** 0.6)
            new.clear_updaters()
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 4: \ Randomness in Motion", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"describe it, \ learn from it, \ draw from it, \ watch it move", font_size=32, color=C.BITS)
        sub.next_to(title, DOWN, buff=0.25)
        smap = series_map(current=4, done=3).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "So this part is about randomness: how to describe it, how to learn from it, how to draw samples from it, "
            "and how it moves. <bookmark mark='a'/> It's the last piece of mathematics we need before the models "
            "themselves."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
