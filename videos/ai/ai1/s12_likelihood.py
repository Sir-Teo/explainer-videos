from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import MONO, PART, load, net_sketch, plain_axes, polyline, valley_steps

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
        card = chapter_card(11, r"Learning: likelihood, softmax, and the gradient", r"How does a model learn to guess?",
                            part=PART)
        with self.voiceover("Chapter eleven. So far our models were counted. Now let's see how a model learns.") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    BIN_X = np.linspace(-4.8, 4.8, 5)
    BIN_Y = -2.95  # the stacks' base
    SQ, GAP, PER_ROW = 0.13, 0.025, 4  # unit squares: 4 to a row

    def stack_pos(self, k, n):
        """Where the n-th observation of token k sits in its stack."""
        r, c = divmod(n, self.PER_ROW)
        step = self.SQ + self.GAP
        return np.array([self.BIN_X[k] + (c - (self.PER_ROW - 1) / 2) * step, self.BIN_Y + step / 2 + r * step, 0])

    def freq_height(self, f):
        """The height of a stack holding a fraction f of the 100 observations."""
        return 100 * f / self.PER_ROW * (self.SQ + self.GAP)

    def mle(self):
        d = load("softmax")
        counts, phat = np.asarray(d["counts"]).astype(int), np.asarray(d["phat"])
        assert list(counts) == [40, 25, 18, 12, 5]
        head = label(r"Maximum likelihood $=$ minimum cross-entropy", font_size=36).to_edge(UP, buff=0.35)
        setup = label(r"data $x_1, \dots, x_N$; \ a model $q_\theta$ with adjustable parameters $\theta$", font_size=26,
                      color=GREY_A).next_to(head, DOWN, buff=0.25)
        P, Q = C.TRUE_P, C.MODEL_Q
        colors = {r"\hat p(x)": P, r"H(\hat p)": C.ENTROPY, r"D_{\mathrm{KL}}(\hat p \,\|\, q_\theta)": C.KL}
        L = r"-\tfrac1N \log_2 \prod_t q_\theta(x_t)"
        steps = [
            [L, "=", r"\tfrac1N \sum_t \log_2 \frac{1}{q_\theta(x_t)}"],
            [L, "=", r"\sum_x", r"\hat p(x)", r"\log_2 \frac{1}{q_\theta(x)}"],
            [L, "=", r"H(\hat p)", "+", r"D_{\mathrm{KL}}(\hat p \,\|\, q_\theta)"],
        ]
        eqs = [cmath(*st, colors=colors, font_size=42).move_to(UP * 1.7) for st in steps]
        whys = [why(r"log of a product: \ the average surprise"),
                why(r"group equal outcomes: \ $\hat p(x)$ $=$ the fraction of the data equal to $x$"),
                why(r"Chapter 7")]
        for w in whys:
            w.scale(1.1).move_to(UP * 0.85)
        src = cite(r"R.~A.~Fisher, \textit{On the Mathematical Foundations of Theoretical Statistics} (1922)", corner=DR)
        # the data: 100 observations, in the order they came
        palette = [C.TRUE_P, TEAL_C, GREEN_C, GOLD_C, MAROON_C]
        seq = np.random.default_rng(1922).permutation(np.repeat(np.arange(5), counts))
        tape = VGroup(*[Square(side_length=self.SQ, stroke_width=0, fill_color=palette[k], fill_opacity=0.95)
                        for k in seq]).arrange(RIGHT, buff=0.0).move_to(DOWN * 0.15)
        tape.width = 12.4
        seen = [0] * 5
        homes = []
        for k in seq:
            homes.append(self.stack_pos(k, seen[k]))
            seen[k] += 1
        toks = VGroup(*[Text(TOKENS[k], font=MONO, font_size=26, color=palette[k]).move_to([self.BIN_X[k], self.BIN_Y - 0.35, 0])
                        for k in range(5)])
        base = Line([-6.2, self.BIN_Y, 0], [6.2, self.BIN_Y, 0], color=GREY_D, stroke_width=1.5)
        fr = VGroup(*[MathTex(f"{v:.2f}", font_size=28, color=palette[k]).move_to(
            [self.BIN_X[k] + 0.75, self.BIN_Y + self.freq_height(v) / 2, 0]) for k, v in enumerate(phat)])
        q_t = [ValueTracker(0.2) for _ in range(5)]

        def q_bars():
            g = VGroup()
            for k in range(5):
                h = self.freq_height(q_t[k].get_value())
                g.add(Rectangle(width=self.PER_ROW * (self.SQ + self.GAP) + 0.14, height=h, stroke_color=Q, stroke_width=3,
                                fill_opacity=0).move_to([self.BIN_X[k], self.BIN_Y + h / 2, 0]))
            return g

        qb = always_redraw(q_bars)
        q_lab = label(r"$q_\theta$: the model", font_size=26, color=Q).move_to([-4.6, -0.6, 0])
        with self.voiceover(
            "Learning starts from a principle stated by Ronald Fisher in 1922: choose the model under which the data "
            "you actually saw were most likely. That's the likelihood: the product of the model's probabilities for "
            "every observation. <bookmark mark='a'/> Take minus its log, per observation, and you get the average "
            "surprise. <bookmark mark='b'/> Group the observations by value: that's the cross-entropy between the "
            "data's own frequencies, p hat, and the model. <bookmark mark='c'/> And that's the entropy of the data "
            "plus the divergence of the model from the data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(setup), FadeIn(src))
            self.play(LaggedStart(*[FadeIn(sq, shift=DOWN * 0.2) for sq in tape], lag_ratio=0.015), run_time=2.0)
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeOut(whys[0]), FadeIn(whys[1]), run_time=0.4)
            morph(self, eqs[0], eqs[1], run_time=1.0)
            self.play(Create(base), FadeIn(toks), LaggedStart(*[sq.animate.move_to(h) for sq, h in zip(tape, homes)],
                                                             lag_ratio=0.01), run_time=2.2)
            self.play(FadeIn(fr))
            vo.wait_until("c")
            self.play(FadeOut(whys[1]), FadeIn(whys[2]), run_time=0.4)
            morph(self, eqs[1], eqs[2], run_time=1.0)
            self.add(qb)
            self.play(FadeIn(q_lab), *[t.animate.set_value(0.2) for t in q_t])
        cap = label(r"maximizing the likelihood $\prod_t q_\theta(x_t)$ \ $=$ \ minimizing the surprise \ $=$ \ "
                    r"pulling $q_\theta$ toward the data", font_size=26, color=C.BITS).move_to(UP * 0.85)
        with self.voiceover(
            "So maximum likelihood, minimum cross-entropy, and minimum divergence from the data are one and the "
            "same goal. It's the loss from chapter seven, seen from the other side."
        ) as vo:
            self.play(FadeOut(whys[2]), FadeIn(cap))
        self.wait(0.3)
        self.data_view = dict(eq=eqs[2], cap=cap, head=head, setup=setup, src=src, q_t=q_t, qb=qb, phat=phat,
                              q_lab=q_lab, fr=fr)

    # ------------------------------------------------------------------
    def counting_is_mle(self):
        v = self.data_view
        q_t, phat = v["q_t"], v["phat"]
        a = label(r"If $q$ may be \textit{any} distribution:", font_size=34)
        b = mtex(r"D_{\mathrm{KL}}(\hat p \,\|\, q) \ge 0, \ \text{with equality only when } q = \hat p", font_size=38)
        c = label(r"the best $q$ is the data's own frequencies: \ counting \textit{is} maximum likelihood", font_size=32,
                  color=C.BITS)
        d = label(r"(and on new data, that's exactly what overfits: \ Chapter 9)", font_size=26, color=GREY_A)
        VGroup(a, b).arrange(DOWN, buff=0.3).move_to(UP * 2.6)
        VGroup(c, d).arrange(DOWN, buff=0.2).move_to(UP * 1.05)

        def kl():
            q = np.array([t.get_value() for t in q_t])
            q = q / q.sum()
            return float(np.sum(phat * np.log2(phat / q)))

        kl_l = MathTex(r"D_{\mathrm{KL}}(\hat p \,\|\, q) =", font_size=34, color=C.KL)
        kl_n = DecimalNumber(kl(), num_decimal_places=3, font_size=34, color=C.KL)
        kl_g = VGroup(kl_l, kl_n).arrange(RIGHT, buff=0.15).move_to([3.6, -0.6, 0])
        kl_n.add_updater(lambda m: m.set_value(kl()))
        with self.voiceover(
            "If the model is allowed to be any distribution at all, <bookmark mark='a'/> the divergence is smallest, "
            "zero, when the model equals the data's frequencies. <bookmark mark='b'/> So the counting models of "
            "chapter nine were maximum likelihood models. And that's exactly why they overfit: they fit the "
            "books perfectly, and nothing pulled them toward anything more general."
        ) as vo:
            self.play(FadeOut(VGroup(v["eq"], v["cap"], v["head"], v["setup"], v["src"])), FadeIn(a), FadeIn(kl_g))
            vo.wait_until("a")
            self.play(Write(b))
            self.play(*[t.animate.set_value(f) for t, f in zip(q_t, phat)], run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(c))
            self.play(FadeIn(d))
        kl_n.clear_updaters()
        v["qb"].clear_updaters()
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
        stage2 = label(r"$e^{z_k}$: \ all positive; \ each $+1$ in $z$ multiplies it by $e \approx 2.7$", font_size=26,
                       color=C.MODEL_Q).to_corner(DL, buff=0.4)
        stage3 = label(r"divide by the total: \ they sum to $1$", font_size=26, color=C.PROB).to_corner(DL, buff=0.4)
        ctx = label(r"after \texttt{Come}\ \ldots \ \ (illustrative)", font_size=22, color=GREY_B).to_corner(DR, buff=0.4)
        assert abs(q.sum() - 1) < 1e-12
        net = gloss(r"neural network", r"a stack of simple steps: \ multiply by a table of numbers, then bend, "
                    r"and repeat;\\ the numbers in the tables are tuned until the guesses are good",
                    picture=net_sketch(), width=6.6, color=C.NEURAL)
        net.scale(1.15).move_to(DOWN * 0.3)
        with self.voiceover(
            "Counting doesn't generalize. Neural networks do. <bookmark mark='n'/> A neural network is a stack of "
            "simple steps: multiply by a table of numbers, then bend the result, and repeat, with all the numbers "
            "in the tables tuned until its guesses are good. Its guesses come out differently. For each possible "
            "next token, its last step computes a score, called a logit: <bookmark mark='a'/> any real number, "
            "positive or negative. <bookmark mark='b'/> To make probabilities, exponentiate: e to the z turns any "
            "number positive, and each step of one up multiplies it by about 2.7. <bookmark mark='c'/> Then divide "
            "by the total, so they add to one. That's the softmax. Bigger score, bigger probability, and nothing "
            "ever gets probability zero."
        ) as vo:
            self.play(FadeIn(head), Write(f), FadeIn(toks), FadeIn(ctx), Create(zero))
            vo.wait_until("n")
            self.play(FadeIn(net, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(net), run_time=0.5)
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
        P, Q = C.TRUE_P, C.MODEL_Q
        colors = {r"-z_y": Q, r"\ln \sum_j e^{z_j}": Q, r"\frac{e^{z_k}}{\sum_j e^{z_j}}": Q, r"q_k": Q,
                  r"-[k = y]": P, r"- [k = y]": P}
        D = r"\frac{\partial}{\partial z_k} \big(-\ln q_y\big)"
        steps = [
            [r"-\ln q_y", "=", r"-z_y", "+", r"\ln \sum_j e^{z_j}"],
            [D, "=", r"-[k = y]", "+", r"\frac{e^{z_k}}{\sum_j e^{z_j}}"],
            [D, "=", r"q_k", r"- [k = y]"],
        ]
        eqs = [cmath(*st, colors=colors, font_size=50).move_to(UP * 0.9) for st in steps]
        whys = [why(r"the softmax, logged"), why(r"differentiate each term"), why(r"the softmax again")]
        for w in whys:
            w.scale(1.15).move_to(DOWN * 0.35)
        res = VGroup(
            label(r"the model's guess, minus the truth", font_size=32, color=C.BITS),
            mtex(r"\text{averaged over the data:} \quad \nabla_z \mathcal{L} = q - \hat p", font_size=34, color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.55)
        # a derivative, pictured: nudge one score up a little, and the loss moves by (slope) x (nudge)
        zb = Rectangle(width=0.5, height=0.9, stroke_width=0, fill_color=Q, fill_opacity=0.9).move_to([-0.8, 0.45, 0])
        lb = Rectangle(width=0.5, height=1.2, stroke_width=0, fill_color=C.LOSS, fill_opacity=0.9).move_to([0.8, 0.6, 0])
        ghosts = VGroup(zb.copy().set_fill(opacity=0).set_stroke(Q, 1.5), lb.copy().set_fill(opacity=0).set_stroke(C.LOSS, 1.5))
        nudge_pic = VGroup(
            Line([-1.4, 0, 0], [1.4, 0, 0], color=GREY_D, stroke_width=1.5), zb, lb, ghosts,
            label(r"one score", font_size=20, color=Q).next_to(zb, DOWN, buff=0.12),
            label(r"the loss", font_size=20, color=C.LOSS).next_to(lb, DOWN, buff=0.12),
            label(r"nudge", font_size=20, color=C.BITS).move_to([-1.75, 1.0, 0]),
            label(r"moves by\\ slope $\times$ nudge", font_size=20, color=C.BITS).move_to([2.05, 1.1, 0]),
        )
        deriv = gloss(r"derivative \ $\partial / \partial z_k$", r"how much the output moves\\ when you nudge one "
                      r"input a tiny bit", picture=nudge_pic, width=5.0)
        deriv.to_edge(DOWN, buff=0.25).set_x(0)
        dp = deriv[1][-1]
        dp[6].set_opacity(0)
        dp[7].set_opacity(0)
        with self.voiceover(
            "To learn, the network needs to know which way to nudge each score. <bookmark mark='n'/> That's what a "
            "derivative measures: how much the output moves when you nudge one input a tiny bit, holding the others "
            "still. <bookmark mark='a'/> Write the surprise of the right answer, y, in terms of the scores. "
            "<bookmark mark='b'/> Differentiate with respect to the score z k. The first term gives minus one if k "
            "is y. The second is the softmax itself. <bookmark mark='c'/> So the derivative is q k minus one, for "
            "the right answer, and q k, for every wrong one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(setup))
            vo.wait_until("n")
            self.play(FadeIn(deriv, shift=UP * 0.2))
            self.play(dp[1].animate.stretch_to_fit_height(dp[1].height * 1.3, about_edge=DOWN),
                      dp[2].animate.stretch_to_fit_height(dp[2].height * 0.88, about_edge=DOWN),
                      dp[6].animate.set_opacity(1), dp[7].animate.set_opacity(1), run_time=1.2)
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(whys[0]))
            for k, mark in enumerate("bc"):
                vo.wait_until(mark)
                self.play(FadeOut(whys[k]), FadeIn(whys[k + 1]), run_time=0.4)
                morph(self, eqs[k], eqs[k + 1], run_time=1.2)
            self.play(FadeOut(deriv))
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
        # the learning rate, pictured: too small, about right, too large
        rates = VGroup()
        for eta, n, cap_ in ((0.04, 6, r"too small: \ crawls"), (0.3, 5, r"about right"),
                             (0.95, 3, r"too large: \ overshoots")):
            v_ = valley_steps(eta, x0=-1.2, n=n, width=2.0, height=1.1, color=C.LR)
            rates.add(VGroup(v_, label(cap_, font_size=24, color=GREY_A).next_to(v_, DOWN, buff=0.12)))
        rates.arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        lr_card = gloss(r"learning rate \ $\eta$", r"how big each step is", picture=rates, width=6.0, color=C.LR)
        lr_card.scale(1.15).move_to([3.3, -0.9, 0])
        with self.voiceover(
            "Here is gradient descent in action. Suppose the data are a hundred continuations of come, "
            "<bookmark mark='a'/> and the model starts with all five scores equal, so every guess is twenty percent. "
            "At each step, every score moves by minus eta times q minus p hat: up where the model under-guesses, "
            "down where it over-guesses. <bookmark mark='l'/> Eta is the learning rate, the size of each step: too "
            "small, and learning crawls; too large, and it overshoots the bottom. <bookmark mark='b'/> Let's run it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(data), FadeIn(upd), FadeIn(toks), FadeIn(targets), FadeIn(leg), FadeIn(tag))
            vo.wait_until("a")
            self.add(bar_m)
            vo.wait_until("l")
            self.play(FadeIn(lr_card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(lr_card), run_time=0.5)
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(axl), Create(floor), FadeIn(fl))
            self.add(curve)
            self.play(t.animate.set_value(12), run_time=3.0, rate_func=linear)
        with self.voiceover(
            "The guesses slide toward the data's frequencies, and the cross-entropy falls toward its floor: the "
            f"entropy of the data, {H:.2f} bits, which no model can beat. <bookmark mark='a'/> That's all of training, in "
            "miniature. A real model has billions of parameters instead of five scores, and its scores depend on "
            "the context, but the signal that reaches them is this same difference: guess, minus truth."
        ) as vo:
            self.play(t.animate.set_value(60), run_time=5.0, rate_func=linear)
            vo.wait_until("a")
            pay = payoff_card([(r"derivatives, backpropagation", [4, 9]), (r"optimizers", [11]),
                               (r"the output layer of a transformer", [13])], font_size=22, title=r"")
            pay.scale(0.9).move_to([3.4, -1.4, 0])
            self.play(FadeOut(VGroup(ax, xl, yl, axl, floor, fl)), FadeOut(curve), FadeIn(pay))
        bar_m.clear_updaters()
        curve.clear_updaters()
        self.wait(0.5)
        self.clear_scene()
