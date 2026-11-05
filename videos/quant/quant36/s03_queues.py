from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (ASK_C, BAD, BID_C, GOOD, HURDLE, MICRO_C, MID_C, PART, fit_right, illustration,
                                         load)


def p_up_theory(I):
    I = np.asarray(I, float)
    return 1 - 2 / math.pi * np.arctan((1 - I) / np.maximum(I, 1e-9))


class Queues(VoiceoverScene):
    def construct(self):
        m = load("micro")
        self.card()
        self.race()
        self.quadrant()
        self.formula()
        self.data(m)
        self.why_flat(m)
        self.queue_reactive()
        self.question()

    def card(self):
        c = chapter_card(2, r"Queues and the next tick", r"If the bid queue is long and the offer short, which way does the "
                         r"price go?", part=PART)
        with self.voiceover("Chapter two. With a one-tick spread, the price moves when one of the two best queues runs "
                            "out. So the next move is a race between the queues. Rama Cont and Adrien de Larrard turned "
                            "that race into a formula."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def race(self):
        rows = [cmath(r"q^b_t,\ q^a_t", r":", r"\text{the two best queues}", font_size=36),
                cmath(r"dq", r"=", r"(\text{adds}) - (\text{cancels} + \text{trades})", font_size=34),
                cmath(r"\text{up}", r"\iff", r"q^a \text{ hits } 0 \text{ before } q^b", font_size=36, colors={r"\text{up}": GOOD})]
        whys = [why(r"Cont, Stoikov and Talreja (2010): model each queue as a birth-death process of orders"),
                why(r"with balanced rates, each queue is a random walk; in the diffusion limit, a Brownian motion"),
                why(r"the price ticks up when the offer is exhausted first, and down when the bid is")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The race. <bookmark mark='a'/> Two best queues, bid and offer. <bookmark mark='b'/> Each grows with new "
            "orders and shrinks with cancellations and trades, a birth-death process in Rama Cont, Sasha Stoikov and "
            "Rishi Talreja's model; with balanced rates, a random walk, and in the limit a Brownian motion. "
            "<bookmark mark='c'/> The price ticks up when the offer runs out first."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def quadrant(self):
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 6, 1], x_length=4.8, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(LEFT * 2.4 + DOWN * 0.2)
        xl = label(r"bid queue", font_size=18, color=BID_C).next_to(ax.x_axis, DOWN, buff=0.2)
        yl = label(r"offer queue", font_size=18, color=ASK_C).next_to(ax.y_axis, LEFT, buff=0.2).rotate(PI / 2)
        x0, y0 = 4.0, 1.5
        start = Dot(ax.c2p(x0, y0), radius=0.08, color=WHITE)
        rng = np.random.default_rng(3)
        pts = [(x0, y0)]
        while pts[-1][0] > 0 and pts[-1][1] > 0 and len(pts) < 4000:
            x, y = pts[-1]
            pts.append((x + 0.05 * rng.standard_normal(), y + 0.05 * rng.standard_normal()))
        pts = np.array(pts)
        path = VMobject(color=MICRO_C, stroke_width=2).set_points_as_corners([ax.c2p(a, b) for a, b in pts])
        ang = Arc(radius=1.0, start_angle=0, angle=math.atan(y0 / x0), arc_center=ax.c2p(0, 0), color=HURDLE)
        txt = VGroup(label(r"the queues as a point in the quadrant", font_size=18, color=GREY_A),
                     label(r"hit the floor: the offer is gone, the price ticks up", font_size=18, color=GOOD),
                     label(r"hit the wall: the bid is gone, it ticks down", font_size=18, color=BAD))
        txt.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        with self.voiceover(
            "A picture makes it solvable. <bookmark mark='a'/> Plot the two queues as one point in a quadrant: bid along "
            "the floor, offer up the wall. <bookmark mark='b'/> The point wanders like a two-dimensional Brownian "
            "motion. If it hits the floor first, the offer has run out and the price ticks up; if it hits the wall, it "
            "ticks down. <bookmark mark='c'/> The chance of each is the share of the quadrant's boundary the point can "
            "see, which depends only on its angle."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(txt[0]))
            vo.wait_until("a")
            self.play(FadeIn(start))
            vo.wait_until("b")
            self.play(Create(path), run_time=2.5, rate_func=linear)
            self.play(FadeIn(txt[1:]))
            vo.wait_until("c")
            self.play(Create(ang))
        self.wait(0.4)
        self.clear_scene()

    def formula(self):
        rows = [cmath(r"\Pr(\text{exit through } \theta = 0)", r"=", r"1 - \frac{\theta}{\pi/2}", font_size=34),
                cmath(r"\theta", r"=", r"\arctan\frac{q^a}{q^b}", font_size=38, colors={r"\theta": HURDLE}),
                cmath(r"\Pr(\text{up})", r"=", r"1 - \frac{2}{\pi}\arctan\frac{q^a}{q^b}", font_size=38,
                      colors={r"\Pr(\text{up})": GOOD})]
        whys = [why(r"the harmonic measure of a quadrant: a Brownian motion started at angle $\theta$ leaves through the "
                    r"floor with probability falling linearly in the angle (map the quadrant to a half-plane by $z^2$)"),
                why(r"the angle of the starting point is set by the ratio of the queues"),
                why(r"Cont and de Larrard (2013): equal queues give one half; a short offer and a long bid push it toward "
                    r"one; only the ratio of the queues matters")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The formula. <bookmark mark='a'/> A Brownian motion in a quadrant, started at angle theta, leaves through "
            "the floor with a probability that falls in a straight line with the angle: squaring the complex plane opens "
            "the quadrant into a half-plane, where the answer is classical. <bookmark mark='b'/> The angle is set by the "
            "ratio of the queues. <bookmark mark='c'/> So the probability of an up-tick is one minus two over pi times "
            "the arctangent of offer over bid: one half when they are equal, near one when the offer is short."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def data(self, m):
        I = np.asarray(m["centers"], float)
        p = np.asarray(m["p_up"], float)
        g = axes([0, 1], [0, 1], x_length=6.4, y_length=4.6, xlabel=r"imbalance $q^b/(q^b + q^a)$",
                 ylabel=r"probability the next move is up", xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        xs = np.linspace(0.01, 0.99, 99)
        th = curve(ax, xs, p_up_theory(xs), HURDLE, stroke_width=2.5)
        lin = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_B, stroke_width=1.5)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=MICRO_C) for a, b in zip(I, p)])
        leg = legend([(MICRO_C, r"BTCUSDT, test days"), (HURDLE, r"Cont--de Larrard"), (GREY_B, r"probability = imbalance")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        with self.voiceover(
            "Against the data, on the two test days. <bookmark mark='a'/> The probability that the next move is up, by "
            f"imbalance: from {100 * p[0]:.0f} percent when the bid is tiny to {100 * p[-1]:.0f} percent when the offer is. "
            "<bookmark mark='b'/> The model has the right shape and the right center, but it is too steep at the edges: "
            "real markets are less certain than the random-walk race. A straight line, probability equals imbalance, "
            "lies in between."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Create(th), Create(lin))
        self.wait(0.4)
        self.clear_scene()

    def why_flat(self, m):
        cards = VGroup(
            desk_question(r"queues are not random walks", r"near zero, makers rush to refill a thin queue and others cancel "
                          r"out of it: the dynamics depend on the queue's size, which the next idea models", width=12.4,
                          font_size=19),
            desk_question(r"hidden and iceberg orders", r"part of the real queue is invisible, so the displayed size "
                          r"understates the bid's or offer's strength", width=12.4, font_size=19),
            desk_question(r"information", r"a short offer may be short because informed sellers are about to arrive; the "
                          r"queues are not independent of what traders know (Part 35)", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why the data are flatter. <bookmark mark='a'/> Queues are not random walks: when one runs thin, makers rush "
            "to refill it, and others cancel out of it. <bookmark mark='b'/> Part of the real queue is invisible, hidden "
            "or iceberg orders. <bookmark mark='c'/> And a short offer may be short because sellers who know something "
            "are about to arrive: the queues are not independent of information."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def queue_reactive(self):
        rows = [cmath(r"\lambda^{\text{add}}(q),\ \lambda^{\text{cancel}}(q),\ \lambda^{\text{trade}}(q)", r":",
                      r"\text{rates that depend on the queue}", font_size=30),
                cmath(r"\text{estimate}", r":", r"\text{count events per unit time spent at each size}", font_size=32),
                cmath(r"\text{simulate}", r":", r"\text{a Markov chain of queues: a book from data}", font_size=32,
                      colors={r"\text{simulate}": GOOD})]
        whys = [why(r"Huang, Lehalle and Rosenbaum (2015): the queue-reactive model lets each event's intensity depend on "
                    r"the current queue sizes"),
                why(r"the rates are read straight off the data, one state at a time"),
                why(r"Chapter 7 builds the House's simulator this way, and scores it against the real book")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The fix. <bookmark mark='a'/> Weibing Huang, Charles-Albert Lehalle and Mathieu Rosenbaum's queue-reactive "
            "model lets the rate of every event depend on the current size of the queue. <bookmark mark='b'/> The rates "
            "are read straight from the data, by counting events per unit of time spent at each size. "
            "<bookmark mark='c'/> And the result is a Markov chain of queues that can be simulated: a book generated "
            "from data, which Chapter seven builds and scores."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the bid queue holds 9 lots and the offer 3. What is the chance of an up-tick under Cont and de "
                       r"Larrard's formula, and under ``probability = imbalance''?")
        with self.voiceover(
            "Pause and predict. The bid queue holds nine lots and the offer three. What is the chance of an up-tick under "
            "Cont and de Larrard's formula, and under the rule that the probability equals the imbalance?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
