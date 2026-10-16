from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import MONO, load, plain_axes, polyline

TOKENS = ["in", "on", "here", "back", "home"]  # illustrative continuations of "Come"


class Likelihood(VoiceoverScene):
    def construct(self):
        self.card()
        self.mle()
        self.counting_is_mle()
        self.softmax()
        self.gradient()
        self.descent()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"Learning: likelihood, softmax, and the gradient", r"How does a model learn to guess?",
                            part=1)
        with self.voiceover("Chapter nine. So far our models were counted. Now let's see how a model learns.") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def mle(self):
        head = label(r"Maximum likelihood $=$ minimum cross-entropy", font_size=36).to_edge(UP, buff=0.35)
        setup = label(r"data $x_1, \dots, x_N$; \ a model $q_\theta$ with adjustable parameters $\theta$", font_size=26,
                      color=GREY_A).next_to(head, DOWN, buff=0.25)
        rows = [
            mtex([r"-\tfrac1N \log_2 \prod_t q_\theta(x_t)", r"=", r"\tfrac1N \sum_t \log_2 \frac{1}{q_\theta(x_t)}"],
                 font_size=36),
            mtex([r"-\tfrac1N \log_2 \prod_t q_\theta(x_t)", r"=", r"\sum_x \hat p(x) \log_2 \frac{1}{q_\theta(x)}"],
                 font_size=36),
            mtex([r"-\tfrac1N \log_2 \prod_t q_\theta(x_t)", r"=", r"H(\hat p) + D_{\mathrm{KL}}(\hat p \,\|\, q_\theta)"],
                 font_size=36),
        ]
        whys = [why(r"log of a product: \ the average surprise"),
                why(r"group equal outcomes: \ $\hat p(x)$ $=$ the fraction of the data equal to $x$"),
                why(r"Chapter 5")]
        step = ladder(self, rows, whys, keep=3, top=1.7, buff=0.45)
        cap = label(r"maximizing the likelihood $\prod_t q_\theta(x_t)$ \ $=$ \ minimizing the surprise \ $=$ \ "
                    r"pulling $q_\theta$ toward the data", font_size=26, color=C.BITS).to_edge(DOWN, buff=1.0)
        src = cite(r"R.~A.~Fisher, \textit{On the Mathematical Foundations of Theoretical Statistics} (1922)", corner=DR)
        with self.voiceover(
            "Learning starts from a principle stated by Ronald Fisher in 1922: choose the model under which the data "
            "you actually saw were most likely. That's the likelihood: the product of the model's probabilities for "
            "every observation. <bookmark mark='a'/> Take minus its log, per observation, and you get the average "
            "surprise. <bookmark mark='b'/> Group the observations by value: that's the cross-entropy between the "
            "data's own frequencies, p hat, and the model. <bookmark mark='c'/> And that's the entropy of the data "
            "plus the divergence of the model from the data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(setup), FadeIn(src))
            for k, mark in enumerate("abc"):
                vo.wait_until(mark)
                step(k)
        with self.voiceover(
            "So maximum likelihood, minimum cross-entropy, and minimum divergence from the data are one and the "
            "same goal. It's the loss from chapter five, seen from the other side."
        ) as vo:
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counting_is_mle(self):
        a = label(r"If $q$ may be \textit{any} distribution:", font_size=34)
        b = mtex(r"D_{\mathrm{KL}}(\hat p \,\|\, q) \ge 0, \ \text{with equality only when } q = \hat p", font_size=38)
        c = label(r"the best $q$ is the data's own frequencies: \ counting \textit{is} maximum likelihood", font_size=32,
                  color=C.BITS)
        d = label(r"(and on new data, that's exactly what overfits: \ Chapter 7)", font_size=26, color=GREY_A)
        VGroup(a, b, c, d).arrange(DOWN, buff=0.4)
        with self.voiceover(
            "If the model is allowed to be any distribution at all, <bookmark mark='a'/> the divergence is smallest, "
            "zero, when the model equals the data's frequencies. <bookmark mark='b'/> So the counting models of "
            "chapter seven were maximum likelihood models. And that's exactly why they overfit: they fit the "
            "books perfectly, and nothing pulled them toward anything more general."
        ) as vo:
            self.play(FadeIn(a))
            vo.wait_until("a")
            self.play(Write(b))
            vo.wait_until("b")
            self.play(FadeIn(c))
            self.play(FadeIn(d))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def softmax(self):
        z = np.array([2.1, 1.3, 0.2, -0.6, -1.4])
        e = np.exp(z)
        q = e / e.sum()
        head = label(r"A network outputs scores; \ the \textit{softmax} turns them into probabilities", font_size=32)
        head.to_edge(UP, buff=0.35)
        f = mtex(r"q_k = \frac{e^{z_k}}{\sum_j e^{z_j}}", font_size=44).next_to(head, DOWN, buff=0.35)
        xs = np.linspace(-4.8, 4.8, 5)
        zero = Line([-6.0, -0.4, 0], [6.0, -0.4, 0], color=GREY_D, stroke_width=1.5)
        logit_bars, exp_bars, prob_bars, toks = VGroup(), VGroup(), VGroup(), VGroup()
        for k, x in enumerate(xs):
            h = 0.55 * z[k]
            logit_bars.add(Rectangle(width=0.9, height=abs(h), stroke_width=0, fill_color=C.MODEL_Q, fill_opacity=0.85)
                           .move_to([x, -0.4 + h / 2, 0]))
            he = 0.32 * e[k]
            exp_bars.add(Rectangle(width=0.9, height=he, stroke_width=0, fill_color=C.MODEL_Q, fill_opacity=0.85)
                         .move_to([x, -0.4 + he / 2, 0]))
            hp = 4.0 * q[k]
            prob_bars.add(Rectangle(width=0.9, height=hp, stroke_width=0, fill_color=C.PROB, fill_opacity=0.9)
                          .move_to([x, -0.4 + hp / 2, 0]))
            toks.add(Text(TOKENS[k], font=MONO, font_size=24, color=C.TOKEN).move_to([x, -2.75, 0]))
        lz = VGroup(*[MathTex(f"{v:+.1f}", font_size=24, color=C.MODEL_Q).next_to(b, UP if v > 0 else DOWN, buff=0.08)
                      for v, b in zip(z, logit_bars)])
        le = VGroup(*[MathTex(f"{v:.2f}", font_size=24, color=C.MODEL_Q).next_to(b, UP, buff=0.08)
                      for v, b in zip(e, exp_bars)])
        lq = VGroup(*[MathTex(f"{v:.3f}", font_size=24, color=C.PROB).next_to(b, UP, buff=0.08)
                      for v, b in zip(q, prob_bars)])
        stage = label(r"logits $z_k$: \ any real numbers", font_size=26, color=C.MODEL_Q).to_corner(DL, buff=0.4)
        stage2 = label(r"$e^{z_k}$: \ all positive", font_size=26, color=C.MODEL_Q).to_corner(DL, buff=0.4)
        stage3 = label(r"divide by the total: \ they sum to $1$", font_size=26, color=C.PROB).to_corner(DL, buff=0.4)
        ctx = label(r"after \texttt{Come}\ \ldots \ \ (illustrative)", font_size=22, color=GREY_B).to_corner(DR, buff=0.4)
        assert abs(q.sum() - 1) < 1e-12
        with self.voiceover(
            "Counting doesn't generalize. Neural networks do, and they produce their guesses differently. For each "
            "possible next token, the network computes a score, called a logit: <bookmark mark='a'/> any real "
            "number, positive or negative. <bookmark mark='b'/> To make probabilities, exponentiate, so every score "
            "becomes positive, <bookmark mark='c'/> and divide by the total, so they add to one. That's the softmax. "
            "Bigger score, bigger probability, and nothing ever gets probability zero."
        ) as vo:
            self.play(FadeIn(head), Write(f), FadeIn(toks), FadeIn(ctx), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if v > 0 else UP) for b, v in zip(logit_bars, z)],
                                  lag_ratio=0.15), FadeIn(lz), FadeIn(stage))
            vo.wait_until("b")
            self.play(*[ReplacementTransform(a, b) for a, b in zip(logit_bars, exp_bars)],
                      ReplacementTransform(lz, le), ReplacementTransform(stage, stage2), run_time=1.5)
            vo.wait_until("c")
            self.play(*[ReplacementTransform(a, b) for a, b in zip(exp_bars, prob_bars)],
                      ReplacementTransform(le, lq), ReplacementTransform(stage2, stage3), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gradient(self):
        head = label(r"The most important derivative in AI", font_size=36).to_edge(UP, buff=0.35)
        setup = label(r"the next token was $y$; \ its surprise, in nats: \ $-\ln q_y$", font_size=28, color=GREY_A)
        setup.next_to(head, DOWN, buff=0.25)
        rows = [
            mtex([r"-\ln q_y", r"=", r"-z_y + \ln \sum_j e^{z_j}"], font_size=38),
            mtex([r"\frac{\partial}{\partial z_k} \big(-\ln q_y\big)", r"=", r"-[k = y] + \frac{e^{z_k}}{\sum_j e^{z_j}}"],
                 font_size=38),
            mtex([r"\frac{\partial}{\partial z_k} \big(-\ln q_y\big)", r"=", r"q_k - [k = y]"], font_size=44),
        ]
        whys = [why(r"the softmax, logged"), why(r"differentiate each term"), why(r"the softmax again")]
        step = ladder(self, rows, whys, keep=3, top=1.6, buff=0.5)
        res = VGroup(
            label(r"the model's guess, minus the truth", font_size=32, color=C.BITS),
            mtex(r"\text{averaged over the data:} \quad \nabla_z \mathcal{L} = q - \hat p", font_size=34, color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "To learn, the network needs to know which way to nudge each score. <bookmark mark='a'/> Write the "
            "surprise of the right answer, y, in terms of the scores. <bookmark mark='b'/> Differentiate with "
            "respect to the score z k. The first term gives minus one if k is y. The second is the softmax itself. "
            "<bookmark mark='c'/> So the derivative is q k minus one, for the right answer, and q k, for every wrong "
            "one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(setup))
            for k, mark in enumerate("abc"):
                vo.wait_until(mark)
                step(k)
        with self.voiceover(
            "In words: the model's guess, minus the truth. <bookmark mark='a'/> Averaged over a dataset, the "
            "gradient is q minus p hat. Push up the scores of what happened more often than the model expected; "
            "push down the rest. Every language model, however large, ends in exactly this step."
        ) as vo:
            self.play(FadeIn(res[0]))
            vo.wait_until("a")
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def descent(self):
        d = load("softmax")
        counts, phat = np.asarray(d["counts"]), np.asarray(d["phat"])
        qs, ces = np.asarray(d["q"]), np.asarray(d["ce"])
        H = float(d["H"])
        assert list(counts) == [40, 25, 18, 12, 5] and abs(ces[-1] - H) < 0.01
        head = label(r"Gradient descent on five scores", font_size=34).to_edge(UP, buff=0.3)
        data = label(r"data: \ $100$ continuations of \texttt{Come}: \ $40, 25, 18, 12, 5$ \ (illustrative)",
                     font_size=24, color=GREY_A).next_to(head, DOWN, buff=0.15)
        upd = mtex(r"z \leftarrow z - \eta\,(q - \hat p), \quad \eta = 1.5", font_size=30).next_to(data, DOWN, buff=0.2)
        xs = np.linspace(-5.8, -1.4, 5)
        y0, Hs = -2.4, 6.0
        targets, toks = VGroup(), VGroup()
        for k, x in enumerate(xs):
            h = Hs * phat[k]
            targets.add(Rectangle(width=0.75, height=h, stroke_color=C.TRUE_P, stroke_width=2.5, fill_opacity=0)
                        .move_to([x, y0 + h / 2, 0]))
            toks.add(Text(TOKENS[k], font=MONO, font_size=22, color=C.TOKEN).move_to([x, y0 - 0.3, 0]))
        t = ValueTracker(0)

        def bars():
            i = int(round(t.get_value()))
            g = VGroup()
            for k, x in enumerate(xs):
                h = max(0.01, Hs * qs[i, k])
                g.add(Rectangle(width=0.55, height=h, stroke_width=0, fill_color=C.MODEL_Q, fill_opacity=0.85)
                      .move_to([x, y0 + h / 2, 0]))
                dlt = qs[i, k] - phat[k]
                if abs(dlt) > 0.004:
                    top = y0 + h
                    g.add(Arrow([x + 0.48, top, 0], [x + 0.48, top - Hs * dlt * 0.9, 0], buff=0, color=C.BITS,
                                stroke_width=3, max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=8))
            return g

        bar_m = always_redraw(bars)
        leg = VGroup(label(r"$\hat p$: the data", font_size=22, color=C.TRUE_P),
                     label(r"$q$: the model", font_size=22, color=C.MODEL_Q),
                     label(r"$-(q - \hat p)$: the step", font_size=22, color=C.BITS)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.08)
        leg.move_to([-3.6, 0.85, 0])
        ax = plain_axes([0, 60, 10], [1.8, 2.4, 0.2], 5.6, 3.6).move_to([3.4, -0.9, 0])
        xl = VGroup(*[MathTex(str(v), font_size=20, color=GREY_B).next_to(ax.c2p(v, 1.8), DOWN, buff=0.12)
                      for v in (0, 20, 40, 60)])
        yl = VGroup(*[MathTex(f"{v:.1f}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for v in (1.8, 2.0, 2.2, 2.4)])
        axl = VGroup(label(r"step", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.4),
                     label(r"cross-entropy, bits", font_size=22, color=C.LOSS).next_to(ax, UP, buff=0.1))
        floor = DashedLine(ax.c2p(0, H), ax.c2p(60, H), color=C.ENTROPY, stroke_width=2)
        fl = label(rf"floor: $H(\hat p) = {H:.2f}$", font_size=22, color=C.ENTROPY).next_to(floor, DOWN, buff=0.1)
        fl.align_to(floor, RIGHT)
        curve = always_redraw(lambda: polyline(ax, np.arange(int(round(t.get_value())) + 1),
                                               np.minimum(ces[:int(round(t.get_value())) + 1], 2.4),
                                               color=C.LOSS, stroke_width=4) if t.get_value() >= 1 else VGroup())
        assert ces[0] > 2.3 and abs(ces[0] - math.log2(5)) < 1e-9  # starts from uniform guesses: log2 5
        tag = computed_tag()
        with self.voiceover(
            "Here it is in action. Suppose the data are a hundred continuations of come, <bookmark mark='a'/> and the "
            "model starts with all five scores equal, so every guess is twenty percent. <bookmark mark='b'/> At each "
            "step, every score moves by minus the learning rate times q minus p hat: up where the model "
            "under-guesses, down where it over-guesses."
        ) as vo:
            self.play(FadeIn(head), FadeIn(data), FadeIn(upd), FadeIn(toks), FadeIn(targets), FadeIn(leg), FadeIn(tag))
            vo.wait_until("a")
            self.add(bar_m)
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(axl), Create(floor), FadeIn(fl))
            self.add(curve)
            vo.wait_until("b")
            self.play(t.animate.set_value(12), run_time=3.0, rate_func=linear)
        with self.voiceover(
            "The guesses slide toward the data's frequencies, and the cross-entropy falls toward its floor: the "
            "entropy of the data, 2.06 bits, which no model can beat. <bookmark mark='a'/> That's all of training, in "
            "miniature. A real model has billions of parameters instead of five scores, and its scores depend on "
            "the context, but the signal that reaches them is this same difference: guess, minus truth."
        ) as vo:
            self.play(t.animate.set_value(60), run_time=5.0, rate_func=linear)
            vo.wait_until("a")
            pay = payoff_card([(r"derivatives, backpropagation", [3]), (r"optimizers", [9]),
                               (r"the output layer of a transformer", [11])], font_size=22, title=r"")
            pay.scale(0.9).move_to([3.4, -1.4, 0])
            self.play(FadeOut(VGroup(ax, xl, yl, axl, floor, fl)), FadeOut(curve), FadeIn(pay))
        assert abs(H - 2.06) < 0.005
        bar_m.clear_updaters()
        curve.clear_updaters()
        self.wait(0.5)
        self.clear_scene()
