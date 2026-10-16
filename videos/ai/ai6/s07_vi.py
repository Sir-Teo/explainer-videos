from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.compute import density2
from videos.ai.ai4.s08_mcmc import heat_image
from videos.ai.ai6.common import ellipse_2sd, load

Q = C.MODEL_Q  # the approximation
P = C.TRUE_P  # the true posterior


def cov_of(theta):
    s0, s1, r = math.exp(theta[2]), math.exp(theta[3]), math.tanh(theta[4])
    return np.array([[s0 * s0, r * s0 * s1], [r * s0 * s1, s1 * s1]])


class VI(VoiceoverScene):
    def construct(self):
        self.card()
        self.fit()

    def card(self):
        card = chapter_card(6, r"Variational inference", r"What if the true answer is a shape you can't compute?", part=6)
        with self.voiceover("Chapter six. Variational inference."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def fit(self):
        v = load("vi")
        path, kl = np.asarray(v["path"]), np.asarray(v["kl_qp"])
        t_pq = np.asarray(v["t_pq"])
        ax = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=7.6, y_length=5.7, tips=False,
                  axis_config={"stroke_width": 0}).move_to([-2.6, -0.4, 0])
        img = heat_image(density2, (-4, 4), (-3, 3)).stretch_to_fit_width(7.6).stretch_to_fit_height(5.7).move_to(ax)
        frame_ = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.5)
        k = ValueTracker(0)

        def q_now():
            i = int(round(k.get_value()))
            th = path[i]
            return VGroup(ellipse_2sd(ax, th[:2], cov_of(th), Q, stroke_width=4, k=1.0),
                          ellipse_2sd(ax, th[:2], cov_of(th), Q, stroke_width=2, k=2.0).set_stroke(opacity=0.6),
                          Dot(ax.c2p(*th[:2]), radius=0.07, color=Q))

        qg = always_redraw(q_now)
        klv = DecimalNumber(kl[0], num_decimal_places=2, font_size=36, color=Q)
        klv.add_updater(lambda m: m.set_value(kl[int(round(k.get_value()))]))
        colors = {r"q": Q, r"p": P}
        kf = VGroup(cmath(r"\mathrm{KL}(", r"q", r"\,\|\,", r"p", r")", r"=", colors=colors, font_size=40), klv)
        kf.arrange(RIGHT, buff=0.15).move_to([4.3, 2.4, 0])
        keyq = label(r"$q$: \ the best single Gaussian", font_size=26, color=Q).next_to(kf, DOWN, buff=0.3)
        keyp = label(r"$p$: \ the true posterior \ (Part 4's two bumps)", font_size=24, color=P).next_to(keyq, DOWN, buff=0.15)
        one = label(r"$\mathrm{KL}(q\,\|\,p)$: \ hides inside one bump", font_size=26, color=Q).next_to(keyp, DOWN, buff=0.45)
        pq_el = DashedVMobject(ellipse_2sd(ax, t_pq[:2], cov_of(t_pq), WHITE, stroke_width=3, k=1.0), num_dashes=30)
        pq_el2 = DashedVMobject(ellipse_2sd(ax, t_pq[:2], cov_of(t_pq), WHITE, stroke_width=2, k=2.0), num_dashes=40)
        two = label(r"$\mathrm{KL}(p\,\|\,q)$: \ covers both, \ spills between", font_size=26, color=WHITE)
        two.next_to(one, DOWN, buff=0.2)
        colors2 = {r"\mathrm{ELBO}(q)": Q, r"\mathrm{KL}\big(q \,\|\, p(z \mid x)\big)": Q}
        elbo = cmath(r"\log p(x)", "=", r"\mathrm{ELBO}(q)", "+", r"\mathrm{KL}\big(q \,\|\, p(z \mid x)\big)",
                     colors=colors2, font_size=34).to_edge(DOWN, buff=0.35).to_edge(RIGHT, buff=0.4)
        en = label(r"raise the bound, \ and the gap closes \ (VAEs, Part 15)", font_size=24, color=GREY_A)
        en.next_to(elbo, UP, buff=0.15)
        with self.voiceover(
            "For most models with hidden parts, the exact answer, the posterior over the hidden variables, is a shape "
            "we can't compute. Part four sampled such shapes with Markov chains. Variational inference does "
            "something else: it picks the closest shape from a simple family, here a single Gaussian, and uses that "
            "instead. <bookmark mark='a'/> Closest in what sense? In part one's KL divergence, from q to p. Start "
            "from a poor guess, and slide the Gaussian downhill."
        ) as vo:
            self.play(FadeIn(img), Create(frame_), FadeIn(keyp))
            vo.wait_until("a")
            self.play(Write(kf), FadeIn(qg), FadeIn(keyq))
            self.play(k.animate.set_value(len(path) - 1), run_time=5.0, rate_func=smooth)
        with self.voiceover(
            "It settles on one bump and ignores the other. This direction of KL punishes q for putting probability "
            "where p has almost none, so q hides inside a single mode. <bookmark mark='a'/> Measure the other way "
            "round, from p to q, and the best Gaussian covers both bumps, spilling into the empty middle. Neither is "
            "wrong: they answer different questions. <bookmark mark='b'/> The identity behind it all: the log "
            "probability of the data equals a lower bound, the ELBO, plus that KL. Raising the bound squeezes the KL "
            "down. Variational autoencoders, in part fifteen, are trained exactly this way."
        ) as vo:
            self.play(FadeIn(one))
            vo.wait_until("a")
            self.play(Create(pq_el), Create(pq_el2), FadeIn(two))
            vo.wait_until("b")
            self.play(Write(elbo), FadeIn(en))
        qg.clear_updaters()
        klv.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
