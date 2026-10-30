from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, HIST, PART, SCORE, era_strip, follow, load, ramp, swarm

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
        self.era()
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
            "they're what a network learns. We'll build them in part twenty-one."
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
    def era(self):
        """How we got here: from a gamblers' letter in 1654 to diffusion models, evenly spaced (not to scale)."""
        events = [
            (1654, r"Pascal, Fermat: \\ dividing the stakes"),
            (1713, r"Bernoulli: \\ the law of large numbers"),
            (1733, r"de Moivre: \\ the bell curve"),
            (1763, r"Bayes: \\ inverse probability"),
            (1809, r"Gauss: \\ errors, least squares"),
            (1905, r"Einstein: \\ Brownian motion"),
            (1922, r"Fisher: \\ likelihood"),
            (1944, r"It\^o: \\ stochastic calculus"),
            (1953, r"Metropolis et al.: \\ MCMC"),
            (2020, r"diffusion models; \\ nucleus sampling"),
        ]
        axis, marks, skel = era_strip(events)
        head = label(r"How we got here", font_size=42).to_edge(UP, buff=0.3)
        tag = note(r"milestones evenly spaced, \ not to scale").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The mathematics is older than computers. It began in 1654, with letters between Pascal and Fermat "
            "about how to split the stakes of an unfinished game. <bookmark mark='a'/> Bernoulli proved that "
            "averages settle down; <bookmark mark='b'/> de Moivre found the bell curve; <bookmark mark='c'/> Bayes "
            "and Laplace turned probability around, from causes to effects and back; <bookmark mark='d'/> Gauss "
            "used it to fit orbits. <bookmark mark='e'/> Einstein explained the jiggling of pollen, "
            "<bookmark mark='f'/> Fisher made likelihood the way to fit models, <bookmark mark='g'/> and Ito gave "
            "random motion its own calculus. <bookmark mark='h'/> At Los Alamos, the first computers were set to "
            "sampling, <bookmark mark='i'/> and today the same ideas choose every word a chatbot writes and turn "
            "noise into pictures."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(tag), FadeIn(skel))
            self.play(FadeIn(marks[0], shift=UP * 0.2))
            for k, mk in enumerate("abcdefghi"):
                vo.wait_until(mk)
                self.play(FadeIn(marks[k + 1], shift=(UP if (k + 1) % 2 == 0 else DOWN) * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Randomness in Motion", font_size=48).to_edge(UP, buff=0.45)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.5)
        obj = objectives_card([
            r"the bell curve: \ why sums are Gaussian, \ in one dimension and many",
            r"fitting and believing: \ likelihood, \ Fisher information, \ Bayes, \ maximum entropy",
            r"how far averages stray: \ the concentration inequalities",
            r"drawing samples: \ from inverse CDFs to the Gumbel trick, \ and how language models choose words",
            r"Markov chains and Monte Carlo: \ mixing, \ importance weights, \ gradients of averages, \ "
            r"Metropolis and Langevin",
            r"random motion: \ Brownian paths, \ It\^o's lemma, \ SDEs, \ and the Fokker--Planck equation",
        ], font_size=24).move_to(DOWN * 0.35)
        with self.voiceover(
            "This is Part 5 of AI, Built, the last part of the foundations. <bookmark mark='a'/> In it: why sums "
            "come out bell-shaped, in one dimension and many; how to fit a model, how precise a fit can be, and how "
            "to hold a belief; how far averages can stray; how to draw samples, and how a language model picks its "
            "next word; Markov chains and Monte Carlo; and random motion, with a calculus of its own. Every result "
            "is computed here, on a laptop."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
