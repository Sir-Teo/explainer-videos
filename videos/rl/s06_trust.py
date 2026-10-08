from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import Plot, Simplex, exact_tag, label, load, mtex, part_card, schematic_tag, why


class TrustRegions(VoiceoverScene):
    def construct(self):
        self.s = load("simplex")
        self.card()
        self.reuse()
        self.importance()
        self.pdl()
        self.minorize()
        self.natural()

    def card(self):
        c = part_card(2, r"Taking safe steps", r"importance sampling, trust regions, PPO")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def reuse(self):
        def lane(y, color, name):
            t = label(name, font_size=26, color=color).move_to([-5.6, y, 0], aligned_edge=LEFT)
            return t
        gen = lane(1.0, C.OLD_POLICY, r"generate")
        trn = lane(-0.4, C.RL_POLICY, r"train")
        blocks = VGroup()
        x = -3.6
        for k in range(3):
            g = Rectangle(width=2.6, height=0.6, stroke_width=0, fill_color=C.OLD_POLICY, fill_opacity=0.6)
            g.move_to([x + 1.3, 1.0, 0])
            t = Rectangle(width=0.5, height=0.6, stroke_width=0, fill_color=C.RL_POLICY, fill_opacity=0.8)
            t.move_to([x + 2.6 + 0.25, -0.4, 0])
            blocks.add(VGroup(g, t))
            x += 3.1
        cap = label(r"sampling long answers costs far more than one gradient step", font_size=28, color=GREY_A)
        cap.move_to(DOWN * 1.15)
        reuse = VGroup()
        x = -3.6 + 2.6
        for k in range(4):
            t = Rectangle(width=0.5, height=0.6, stroke_width=0, fill_color=C.RL_POLICY, fill_opacity=0.8)
            t.move_to([x + 0.25 + 0.56 * k, -2.05, 0])
            reuse.add(t)
        rl = label(r"so: take several steps per batch (each step makes the batch a little more out of date)",
                   font_size=26, color=C.RL_POLICY).next_to(reuse, DOWN, buff=0.35)
        rl.set_x(0)
        with self.voiceover(
            "So far, every gradient step used fresh samples from the current policy. But for a language model, "
            "generating the samples is by far the expensive part. A long answer is written one token at a time, "
            "while the gradient step that consumes it is a single parallel pass. <bookmark mark='r'/> So we'd like "
            "to squeeze several gradient steps out of each batch. The trouble is that after the first step, the "
            "batch was written by an older policy."
        ) as vo:
            self.play(FadeIn(gen), FadeIn(trn), FadeIn(blocks, lag_ratio=0.3), run_time=1.5)
            self.play(FadeIn(cap))
            vo.wait_until("r")
            self.play(FadeIn(reuse, lag_ratio=0.3), FadeIn(rl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def importance(self):
        l1 = mtex(r"\mathbb{E}_{y \sim \pi_\theta}\big[f(y)\big]", r"=", r"\sum_y \pi_\theta(y)\, f(y)", font_size=40)
        l2 = mtex(r"=", r"\sum_y \pi_{\text{old}}(y)\,", r"\frac{\pi_\theta(y)}{\pi_{\text{old}}(y)}", r"\,f(y)", font_size=40)
        l3 = mtex(r"=", r"\mathbb{E}_{y \sim \pi_{\text{old}}}\Big[", r"\rho_\theta(y)", r"\,f(y)\Big]", font_size=40)
        l1[0][2:4].set_color(C.RL_POLICY)
        l1[2][2:4].set_color(C.RL_POLICY)
        l2[1].set_color(C.OLD_POLICY)
        l2[2].set_color(C.RATIO)
        l3[1].set_color(C.OLD_POLICY)
        l3[2].set_color(C.RATIO)
        l1.to_edge(UP, buff=0.5).shift(LEFT * 1.2)
        for prev, cur in ((l1, l2), (l2, l3)):
            cur.next_to(prev, DOWN, buff=0.35, aligned_edge=LEFT)
            cur.shift(RIGHT * (l1[1].get_x() - cur[0].get_x()))
        w2 = why(r"multiply and divide by $\pi_{\text{old}}$").next_to(l2, RIGHT, buff=0.5)
        w3 = why(r"the importance ratio $\rho$", color=C.RATIO).next_to(l3, RIGHT, buff=0.5)
        sur = mtex(r"L(\theta)", r"=", r"\mathbb{E}_{\pi_{\text{old}}}\big[\,", r"\rho_\theta(y)", r"\,A(y)\,\big]", font_size=42)
        sur[3].set_color(C.RATIO)
        sur[4][0].set_color(C.ADVANTAGE)
        sur[2].set_color(C.OLD_POLICY)
        grad = mtex(r"\nabla_\theta L\,\big|_{\theta = \theta_{\text{old}}}", r"=", r"\mathbb{E}_{\pi_{\text{old}}}\big[\, A\, \nabla \log \pi_\theta \big]",
                    font_size=38)
        grad[2].set_color(C.SCORE)
        col = VGroup(sur, grad).arrange(DOWN, buff=0.35).to_edge(DOWN, buff=0.8)
        gw = why(r"since $\nabla \rho = \rho\, \nabla \log \pi_\theta$ and $\rho = 1$ there: the policy gradient again").next_to(col, DOWN, buff=0.15)
        with self.voiceover(
            "There's a standard fix for data drawn from the wrong distribution: importance sampling. An average "
            "under the new policy is a sum weighted by its probabilities. <bookmark mark='m'/> Multiply and divide "
            "by the old policy's probability, <bookmark mark='r'/> and it becomes an average under the old policy, "
            "with each sample reweighted by the ratio rho of new to old probability. <bookmark mark='s'/> Apply that "
            "to the advantage and you get the surrogate objective that PPO and GRPO both optimize. At the old "
            "parameters the ratio is one, and its gradient is exactly the policy gradient."
        ) as vo:
            self.play(Write(l1))
            vo.wait_until("m")
            self.play(FadeIn(l2, shift=DOWN * 0.1), FadeIn(w2))
            vo.wait_until("r")
            self.play(FadeIn(l3, shift=DOWN * 0.1), FadeIn(w3))
            vo.wait_until("s")
            self.play(Write(sur))
            self.play(FadeIn(grad), FadeIn(gw))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pdl(self):
        tok = mtex(r"\rho_t", r"=", r"\frac{\pi_\theta(y_t \mid s_t)}{\pi_{\text{old}}(y_t \mid s_t)}", font_size=40)
        tok[0].set_color(C.RATIO)
        tok[2].set_color(C.RATIO)
        seq = mtex(r"\frac{\pi_\theta(y\mid x)}{\pi_{\text{old}}(y \mid x)}", r"=", r"\prod_t \rho_t", font_size=40)
        seq[2].set_color(C.RATIO)
        top = VGroup(tok, seq).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.45)
        pd = mtex(r"J(\pi') - J(\pi)", r"=", r"\mathbb{E}_{\tau \sim \pi'}\Big[\sum_t A^{\pi}(s_t, y_t)\Big]", font_size=42)
        pd[2][1:6].set_color(C.RL_POLICY)
        pd[2][7:].set_color(C.ADVANTAGE)
        pdn = label(r"the performance difference lemma (Kakade \& Langford, 2002)", font_size=26, color=GREY_A)
        L = mtex(r"L_\pi(\pi')", r"=", r"\mathbb{E}_{\tau \sim \pi}\Big[\sum_t \rho_t\, A^{\pi}(s_t, y_t)\Big]", font_size=42)
        L[2][1:5].set_color(C.OLD_POLICY)
        Ln = label(r"PPO's surrogate: the same, but visiting the \emph{old} policy's prefixes $s_t$", font_size=26, color=GREY_A)
        col = VGroup(VGroup(pd, pdn).arrange(DOWN, buff=0.15), VGroup(L, Ln).arrange(DOWN, buff=0.15)).arrange(DOWN, buff=0.5)
        col.next_to(top, DOWN, buff=0.6)
        why_ = label(r"exact when $\pi' = \pi$; accurate only while $\pi'$ stays close to $\pi$", font_size=28, color=YELLOW)
        why_.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "For a language model, the ratio is taken token by token. The exact ratio for a whole answer would be "
            "the product of all of them, and a product of hundreds of numbers near one can explode, so instead each "
            "token is reweighted on its own. <bookmark mark='p'/> How wrong is that? A classic identity, the "
            "performance difference lemma, says the improvement from one policy to another is the sum of the old "
            "policy's advantages, along trajectories of the new policy. <bookmark mark='l'/> The surrogate makes "
            "one approximation: it uses the prefixes the old policy visited. <bookmark mark='w'/> That's exact when "
            "the policies match, and good only while they stay close."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("p")
            self.play(Write(col[0]))
            vo.wait_until("l")
            self.play(Write(col[1]))
            vo.wait_until("w")
            self.play(FadeIn(why_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def minorize(self):
        plot = Plot(x_range=(-1.0, 3.0), y_range=(0, 2.2), width=8.5, height=4.2, x_label=r"step size along the gradient")
        plot.move_to(DOWN * 0.4 + LEFT * 1.0)
        xs = np.linspace(-1.0, 3.0, 300)
        J = 0.6 + 1.1 * np.exp(-((xs - 1.0) ** 2) / 0.6) - 0.15 * xs
        J0 = float(np.interp(0.0, xs, J))
        dJ = float(np.gradient(J, xs)[np.argmin(np.abs(xs))])
        Lsur = J0 + dJ * xs
        bound = Lsur - 1.25 * xs**2
        mJ = plot.line(xs, J, color=WHITE, stroke_width=4)
        mL = plot.line(xs[(Lsur < 2.2)], Lsur[(Lsur < 2.2)], color=C.RATIO, stroke_width=3)
        mB = plot.line(xs[bound > 0], bound[bound > 0], color=C.KL, stroke_width=4)
        k = int(np.argmax(bound))
        star = Dot(plot.c2p(xs[k], bound[k]), color=C.KL, radius=0.08)
        up = DashedLine(plot.c2p(xs[k], bound[k]), plot.c2p(xs[k], J[k]), color=GREY_B)
        lj = label(r"true objective $J$", font_size=26).next_to(plot.c2p(2.1, float(np.interp(2.1, xs, J))), UR, buff=0.1)
        ll = label(r"surrogate $L$ (keeps rising)", font_size=26, color=C.RATIO).next_to(plot.c2p(2.0, 2.05), LEFT, buff=0.1)
        lb = label(r"$L - C\cdot \mathrm{KL}_{\max}$", font_size=26, color=C.KL).next_to(plot.c2p(0.8, float(np.interp(0.8, xs, bound))), RIGHT, buff=0.15)
        thm = mtex(r"J(\pi')", r"\;\ge\;", r"L_\pi(\pi')", r"-", r"C\,\max_s \mathrm{KL}\big(\pi(\cdot|s)\,\|\,\pi'(\cdot|s)\big)", font_size=36)
        thm[2].set_color(C.RATIO)
        thm[4].set_color(C.KL)
        thm.to_edge(UP, buff=0.4)
        tn = label(r"TRPO (Schulman et al.\ 2015), Theorem 1", font_size=24, color=GREY_A).next_to(thm, DOWN, buff=0.12)
        o = Dot(plot.c2p(0, J0), radius=0.07, color=C.OLD_POLICY)
        ol = label(r"$\theta_{\text{old}}$", font_size=26, color=C.OLD_POLICY).next_to(o, UL, buff=0.05)
        res = VGroup(label(r"maximize the bound:", font_size=26),
                     label(r"$J$ is guaranteed", font_size=26), label(r"not to go down", font_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        res.next_to(plot, RIGHT, buff=0.2).shift(UP * 0.6)
        with self.voiceover(
            "Here's the picture, along one direction in parameter space. <bookmark mark='j'/> The true objective "
            "rises, then falls. <bookmark mark='l'/> The surrogate touches it at the old parameters and has the same "
            "slope, but it keeps promising more the further you go. Follow it blindly and you overshoot. "
            "<bookmark mark='b'/> TRPO proved that subtracting a multiple of the largest KL divergence between old "
            "and new policies gives a lower bound on the true objective. <bookmark mark='m'/> Maximize the bound "
            "instead, and every step is guaranteed not to make things worse."
        ) as vo:
            self.play(FadeIn(plot), FadeIn(schematic_tag()), FadeIn(o), FadeIn(ol))
            vo.wait_until("j")
            self.play(Create(mJ), FadeIn(lj))
            vo.wait_until("l")
            self.play(Create(mL), FadeIn(ll))
            vo.wait_until("b")
            self.play(Write(thm), FadeIn(tn))
            self.play(Create(mB), FadeIn(lb))
            vo.wait_until("m")
            self.play(FadeIn(star, scale=2), Create(up), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def natural(self):
        s = self.s
        r = np.array(s["r"], float)
        S = Simplex(side=5.6, rewards=r).move_to(LEFT * 2.9 + DOWN * 0.35)
        iso = S.iso_lines(r, [0.2, 0.4, 0.6, 0.8])
        van = S.path(np.array(s["vanilla"], float), C.RL_POLICY, stroke_width=5)
        nat = S.path(np.array(s["natural"], float), YELLOW, stroke_width=5)
        p0 = Dot(S.p2s(s["pi0"]), radius=0.08, color=C.RL_POLICY)
        p0l = label(r"$\pi_0$", font_size=26, color=C.RL_POLICY).next_to(p0, RIGHT, buff=0.1)
        conts = VGroup(*[Polygon(*[S.p2s(p) for p in c], stroke_color=C.KL, stroke_width=2, fill_color=C.KL, fill_opacity=0.15)
                         for c in np.array(s["contours"], float)])
        kl = mtex(r"\mathrm{KL}\big(\pi_\theta \,\|\, \pi_{\theta + \delta}\big) \approx \tfrac12\, \delta^{\top} F\, \delta", font_size=34)
        F = mtex(r"F = \mathbb{E}\big[\nabla \log \pi\, \nabla \log \pi^{\top}\big]", font_size=32)
        ng = mtex(r"\delta \;\propto\; F^{-1} \nabla J", font_size=36, color=YELLOW)
        side = VGroup(kl, F, ng).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
        vz = mtex(r"\text{vanilla: } \Delta z_a = \eta\, \pi(a)\, A(a)", font_size=32, color=C.RL_POLICY)
        nz = mtex(r"\text{natural: } \Delta z_a = \eta\, A(a)", font_size=32, color=YELLOW)
        zz = VGroup(vz, nz).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(side, DOWN, buff=0.5).align_to(side, LEFT)
        zn = label(r"rare actions barely move\\under the vanilla gradient", font_size=24, color=GREY_A)
        zn.next_to(zz, DOWN, buff=0.2).align_to(zz, LEFT)
        title = label(r"A softmax policy over three actions; every point is a distribution", font_size=28).to_edge(UP, buff=0.3)
        title.to_edge(LEFT, buff=0.4)
        with self.voiceover(
            "TRPO's constraint leads to a beautiful idea. Picture a policy over just three actions, A, B, and C. "
            "Every point of this triangle is a probability distribution; the corners are certainty. Action A pays "
            "the most. <bookmark mark='c'/> Now draw every distribution within the same small KL divergence of a "
            "few starting points. The regions aren't circles, and they shrink near the edges, where small "
            "probabilities become precious. KL measures distance between distributions, not between parameters."
        ) as vo:
            self.play(FadeIn(title), FadeIn(S), Create(iso), FadeIn(exact_tag()))
            vo.wait_until("c")
            self.play(LaggedStart(*[DrawBorderThenFill(c) for c in conts], lag_ratio=0.2), run_time=2)
        with self.voiceover(
            "To second order, KL is a quadratic form in the parameter step, built from the Fisher information "
            "matrix. <bookmark mark='n'/> Steepest ascent measured this way is the natural gradient: the ordinary "
            "gradient, multiplied by the inverse Fisher matrix. <bookmark mark='v'/> Here are both, followed "
            "exactly from the same start. The ordinary gradient crawls: it moves each logit in proportion to its "
            "action's probability, so the rare best action barely moves at first. <bookmark mark='g'/> The natural "
            "gradient moves every logit by its advantage, and heads almost straight for the best corner."
        ) as vo:
            self.play(FadeOut(conts), FadeIn(p0), FadeIn(p0l))
            self.play(Write(kl), FadeIn(F))
            vo.wait_until("n")
            self.play(FadeIn(ng))
            vo.wait_until("v")
            self.play(Create(van), FadeIn(vz), run_time=2.5)
            vo.wait_until("g")
            self.play(Create(nat), FadeIn(nz), FadeIn(zn), run_time=2.5)
        with self.voiceover(
            "TRPO takes natural-gradient steps with a KL budget. It works, but it needs second-order machinery that "
            "is painful at the scale of a language model. PPO, in 2017, replaced it with something much simpler."
        ):
            pass
        self.wait(0.3)
        self.clear_scene()
