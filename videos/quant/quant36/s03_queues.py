from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (ASK_C, BAD, BID_C, GOOD, HURDLE, MICRO_C, PART, fit_right, load)


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
        self.assumptions()
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
        x0, y0 = 4.0, 1.5
        rng = np.random.default_rng(3)
        pts = [(x0, y0)]
        while pts[-1][0] > 0 and pts[-1][1] > 0 and len(pts) < 4000:
            x, y = pts[-1]
            pts.append((x + 0.05 * rng.standard_normal(), y + 0.05 * rng.standard_normal()))
        pts = np.asarray(pts, float)
        if np.any(pts[-1] < 0):
            a, b = pts[-2].copy(), pts[-1].copy()
            fractions = [a[k] / (a[k] - b[k]) for k in range(2) if b[k] < 0]
            pts[-1] = a + min(fractions) * (b - a)
        extent = max(6.0, float(np.ceil(pts.max() + 0.3)))
        ax = Axes(x_range=[0, extent, 1], y_range=[0, extent, 1], x_length=4.8, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(LEFT * 2.4 + DOWN * 0.2)
        xl = label(r"bid queue", font_size=18, color=BID_C).next_to(ax.x_axis, DOWN, buff=0.2)
        yl = label(r"offer queue", font_size=18, color=ASK_C).next_to(ax.y_axis, LEFT, buff=0.2).rotate(PI / 2)
        start = Dot(ax.c2p(x0, y0), radius=0.08, color=WHITE)
        path = VMobject(color=MICRO_C, stroke_width=2).set_points_as_corners([ax.c2p(a, b) for a, b in pts])
        ang = Arc(radius=1.0, start_angle=0, angle=math.atan(y0 / x0), arc_center=ax.c2p(0, 0), color=HURDLE)
        txt = VGroup(label(r"the queues as a point in the quadrant", font_size=18, color=GREY_A),
                     label(r"hit the floor: the offer is gone, the price ticks up", font_size=18, color=GOOD),
                     label(r"hit the wall: the bid is gone, it ticks down", font_size=18, color=BAD))
        txt.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        caption = wrapped_label(r"illustration: an Euler path; its last segment is interpolated to the boundary", 12.3, 16, GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover("A picture makes the stipulated diffusion solvable. <bookmark mark='a'/> Plot bid and offer queue sizes as one point in a quadrant, with equal coordinate scales. <bookmark mark='b'/> The yellow line is a fixed Euler illustration of independent driftless Brownian queues. Its last discrete segment is interpolated to the first boundary crossing. Reaching the floor depletes the offer; reaching the wall depletes the bid. <bookmark mark='c'/> For the specified equal-variance diffusion, the bounded harmonic exit probability depends on the starting angle, not on distance from the origin.") as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(txt[0]), FadeIn(caption))
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
            "A particular diffusion approximation. <bookmark mark='a'/> For two independent, driftless Brownian queues with equal variance rates, the bounded harmonic solution in a quadrant is linear in the polar angle. It equals one on the offer-depletion boundary and zero on the bid-depletion boundary. <bookmark mark='b'/> The starting angle is the arctangent of offer size over bid size. <bookmark mark='c'/> Hence the up probability is one minus two over pi times that angle. This formula is scale invariant. Unequal volatilities, correlation, drift or queue-dependent rates generally change it; it is not the general solution of every Poisson queue model."
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

    def assumptions(self):
        rows = [cmath(r"\lambda,\ \mu,\ \theta", r":", r"\text{limit orders, market orders, cancels}", font_size=34),
                cmath(r"\text{depletion}", r"\Rightarrow", r"\text{both queues redrawn from } f", font_size=34),
                cmath(r"\text{the price}", r"=", '\\text{regeneration and balance assumptions matter}', font_size=36,
                      colors={r"\text{the price}": GOOD})]
        whys = [why('each best queue gains orders at rate $\\lambda$ and loses them to trades and cancellations at rates $\\mu$ and $\\theta$, in the specified independent birth-death model; the Brownian angle formula also needs balanced drift and equal variance rates'),
                why('when a queue empties the price moves a tick and both new best queues are drawn afresh, a chosen reset law specifies what dependence survives a move'),
                why(r"Cont and de Larrard derive the time between moves, the probability of each direction, and in the "
                    r"limit the price's volatility, all from the order rates and the size of a fresh queue")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Distinguish the models. <bookmark mark='a'/> Independent Poisson additions and removals define a birth-death queue model. A balanced heavy-traffic limit with equal variance rates leads to the simple Brownian quadrant formula just shown. <bookmark mark='b'/> A chosen regeneration rule redraws queues after depletion; reset laws can depend on direction, and can create serial dependence. <bookmark mark='c'/> Driftless diffusive prices require the relevant balance, regeneration and moment conditions. Poisson arrivals alone do not make the price an independent symmetric random walk."
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
            "Possible reasons the observed curve differs from the simple diffusion formula. <bookmark mark='a'/> Size-dependent refill and removal rates can alter depletion probabilities. <bookmark mark='b'/> Hidden liquidity and aggregation can make displayed queues an incomplete state. <bookmark mark='c'/> Recent flow and unobserved information may also matter. This comparison does not identify which mechanism caused the discrepancy, and a short offer does not establish informed selling or illegal intent."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
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
                why('our grid baseline estimates net size-change rates, not each message type'),
                why(r"Chapter 7 builds the House's simulator this way, and scores it against the real book")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A richer baseline. <bookmark mark='a'/> Huang, Lehalle and Rosenbaum let event intensities depend on queue state. <bookmark mark='b'/> Our simplified grid implementation counts net size increases and decreases per occupied state; it does not recover separate message-level addition, trade and cancellation intensities. <bookmark mark='c'/> It produces a Markov model of the full simulated queue state. A coarser summary, such as ten imbalance buckets, need not itself be Markov. We retain its scorecard instead of treating a fitted rate as validation."
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
        head = label('The diffusion assumptions determine the probability', font_size=29, color=QC.IDEA).to_edge(UP, buff=0.45)
        formula = MathTex('q^b=9,\\quad q^a=3,\\qquad p_\\uparrow=1-\\frac2\\pi\\arctan(q^a/q^b)', font_size=33).move_to(UP * 1.2)
        if formula.width > 12.4:
            formula.scale_to_fit_width(12.4)
        assumptions = wrapped_label('Independent, driftless Brownian queues; equal variance rates; stop at first depletion.', 12.2, 20, GREY_A).move_to(DOWN * 0.1)
        question = wrapped_label('Calculate the Brownian probability and the imbalance heuristic. Does doubling both queues change either?', 12.2, 25, QC.IDEA).move_to(DOWN * 1.75)
        banner = label(r"Pause: derive the answer and check its assumptions and units.", font_size=19, color=QC.IDEA).to_edge(DOWN, buff=0.35)
        with self.voiceover('Take independent driftless Brownian queues with equal variance rates. The bid starts at nine lots and the offer at three. Calculate the displayed up probability and compare it with bid size divided by total size. Then double both queue sizes. Explain which quantities remain the same and what the probability formula does not say about waiting time.'):
            self.play(FadeIn(head), FadeIn(formula), FadeIn(assumptions), FadeIn(question), FadeIn(banner))
        self.wait(6)
        self.clear_scene()
