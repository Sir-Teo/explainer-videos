from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.compute import density2
from videos.ai.ai5.s08_mcmc import heat_image
from videos.ai.ai7.common import ellipse_2sd, load

Q = C.MODEL_Q  # the approximation
P = C.TRUE_P  # the true posterior


def cov_of(theta):
    s0, s1, r = math.exp(theta[2]), math.exp(theta[3]), math.tanh(theta[4])
    return np.array([[s0 * s0, r * s0 * s1], [r * s0 * s1, s1 * s1]])


def before_after() -> VGroup:
    """A flat belief before the data, two bumps after it: the posterior in a picture."""
    def panel(f, color, word):
        base = Line([-0.9, 0, 0], [0.9, 0, 0], color=GREY_C, stroke_width=2)
        c = FunctionGraph(f, x_range=[-0.9, 0.9], color=color, stroke_width=3)
        return VGroup(base, c, label(word, font_size=20, color=color).next_to(base, DOWN, buff=0.08))

    before = panel(lambda t: 0.25, GREY_B, r"before")
    after = panel(lambda t: 0.75 * np.exp(-(t + 0.42) ** 2 / 0.03) + 0.5 * np.exp(-(t - 0.45) ** 2 / 0.03), P,
                  r"after the data")
    g = VGroup(before, after).arrange(RIGHT, buff=0.9, aligned_edge=DOWN)
    y = after[:2].get_y()
    return g.add(Arrow([before.get_right()[0], y, 0], [after.get_left()[0], y, 0], buff=0.1, color=GREY_B,
                       stroke_width=3))


class VI(VoiceoverScene):
    def construct(self):
        self.card()
        self.fit()

    def card(self):
        card = chapter_card(6, r"Variational inference", r"What if the true answer is a shape you can't compute?", part=7)
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
        keyp = label(r"$p$: \ the true posterior \ (Part 5's two bumps)", font_size=24, color=P).next_to(keyq, DOWN, buff=0.15)
        one = label(r"$\mathrm{KL}(q\,\|\,p)$: \ hides inside one bump", font_size=26, color=Q).next_to(keyp, DOWN, buff=0.45)
        pq_el = DashedVMobject(ellipse_2sd(ax, t_pq[:2], cov_of(t_pq), WHITE, stroke_width=3, k=1.0), num_dashes=30)
        pq_el2 = DashedVMobject(ellipse_2sd(ax, t_pq[:2], cov_of(t_pq), WHITE, stroke_width=2, k=2.0), num_dashes=40)
        two = label(r"$\mathrm{KL}(p\,\|\,q)$: \ covers both, \ spills between", font_size=26, color=WHITE)
        two.next_to(one, DOWN, buff=0.2)
        colors2 = {r"\mathrm{ELBO}(q)": Q, r"\mathrm{KL}\big(q \,\|\, p(z \mid x)\big)": Q}
        elbo = cmath(r"\log p(x)", "=", r"\mathrm{ELBO}(q)", "+", r"\mathrm{KL}\big(q \,\|\, p(z \mid x)\big)",
                     colors=colors2, font_size=34).to_edge(DOWN, buff=0.35).to_edge(RIGHT, buff=0.4)
        en = label(r"raise the bound, \ and the gap closes \ (VAEs, Part 22)", font_size=24, color=GREY_A)
        en.next_to(elbo, UP, buff=0.15)
        post_card = gloss(r"posterior", r"what we believe about the hidden things \\ after seeing the data", before_after(),
                          corner=DR, width=4.4, color=P)
        # the identity as a bar: log p(x) = ELBO + KL, the KL part shrinking as q improves (schematic widths)
        BW, BH = 4.2, 0.42
        bx0 = 4.3 - BW / 2

        def elbo_bar():
            w_kl = 0.7 * BW * kl[int(round(k.get_value()))] / kl[0]
            lo = Rectangle(width=BW - w_kl, height=BH, stroke_width=0, fill_color=Q, fill_opacity=0.85)
            hi = Rectangle(width=max(w_kl, 0.01), height=BH, stroke_color=Q, stroke_width=2, fill_opacity=0)
            lo.move_to([bx0 + (BW - w_kl) / 2, -1.1, 0])
            hi.move_to([bx0 + BW - w_kl / 2, -1.1, 0])
            return VGroup(lo, hi, MathTex(r"\mathrm{ELBO}", font_size=26, color=Q).next_to(lo, DOWN, buff=0.1),
                          MathTex(r"\mathrm{KL}", font_size=26, color=Q).next_to(hi, DOWN, buff=0.1))

        bar = always_redraw(elbo_bar)
        bar_top = Line([bx0, -0.89, 0], [bx0 + BW, -0.89, 0])
        bar_b = VGroup(Brace(bar_top, UP, buff=0.05, color=GREY_B))
        bar_b.add(MathTex(r"\log p(x)", font_size=28).next_to(bar_b[0], UP, buff=0.06))
        bar_n = label(r"the ELBO: \ computable, \ always below $\log p(x)$", font_size=22, color=GREY_A)
        bar_n.move_to([4.3, -1.95, 0])
        with self.voiceover(
            "For most models with hidden parts, the exact answer, the posterior over the hidden variables, is a shape "
            "we can't compute. <bookmark mark='p'/> The posterior is what we believe about the hidden things after "
            "seeing the data: part five's updated belief. Part five sampled such shapes with Markov chains. "
            "Variational inference does something else: it picks the closest shape from a simple family, here a "
            "single Gaussian, and uses that instead. <bookmark mark='a'/> Closest in what sense? In part one's KL "
            "divergence, from q to p. Start from a poor guess, and slide the Gaussian downhill."
        ) as vo:
            self.play(FadeIn(img), Create(frame_), FadeIn(keyp))
            vo.wait_until("p")
            self.play(FadeIn(post_card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(post_card))
            self.play(Write(kf), FadeIn(qg), FadeIn(keyq))
            self.play(k.animate.set_value(len(path) - 1), run_time=5.0, rate_func=smooth)
        with self.voiceover(
            "It settles on one bump and ignores the other. This direction of KL punishes q for putting probability "
            "where p has almost none, so q hides inside a single mode, a single peak of the distribution. "
            "<bookmark mark='a'/> Measure the other way "
            "round, from p to q, and the best Gaussian covers both bumps, spilling into the empty middle. Neither is "
            "wrong: they answer different questions. <bookmark mark='b'/> The identity behind it all: the log "
            "probability of the data equals a lower bound, the ELBO, plus that KL. The ELBO is a score we can "
            "compute that always sits below the true one. <bookmark mark='c'/> Push it up, and the KL has to shrink, "
            "dragging q toward p. Variational autoencoders, in part twenty-two, are trained exactly this way."
        ) as vo:
            self.play(FadeIn(one))
            vo.wait_until("a")
            self.play(Create(pq_el), Create(pq_el2), FadeIn(two))
            vo.wait_until("b")
            k.set_value(0)
            self.play(Write(elbo), FadeIn(en), FadeIn(bar), FadeIn(bar_b), FadeIn(bar_n))
            vo.wait_until("c")
            self.play(k.animate.set_value(len(path) - 1), run_time=3.0, rate_func=smooth)
        bar.clear_updaters()
        qg.clear_updaters()
        klv.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
