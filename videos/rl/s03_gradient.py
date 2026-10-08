from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import Plot, exact_tag, label, load, mtex, tokens, why
from videos.rl.compute import answer_text, gauss_reward, prompt_text


def pdf(x, mu, s=1.0):
    return np.exp(-((x - mu) ** 2) / (2 * s * s)) / np.sqrt(2 * np.pi * s * s)


class LogDerivative(VoiceoverScene):
    def construct(self):
        self.g = load("gauss")
        self.obstacle()
        self.derive()
        self.gaussian()
        self.tokens_view()
        self.softmax_view()

    # ------------------------------------------------------------------
    def obstacle(self):
        def node(tex, color, w=1.9):
            t = mtex(tex, font_size=40, color=color)
            box = RoundedRectangle(width=max(w, t.width + 0.5), height=1.0, corner_radius=0.14, stroke_color=color,
                                   fill_color=color, fill_opacity=0.1)
            return VGroup(box, t.move_to(box))

        th = node(r"\theta", C.RL_POLICY, 1.2)
        pol = node(r"\pi_\theta(\,\cdot \mid x)", C.RL_POLICY)
        smp = node(r"y \sim \pi_\theta", C.TOKEN)
        chk = node(r"R(x, y)", C.REWARD)
        row = VGroup(th, pol, smp, chk).arrange(RIGHT, buff=0.9).move_to(UP * 0.9)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, stroke_width=3, color=GREY_B)
                          for a, b in zip(row, row[1:])])
        cap_s = label(r"sampling:\\a discrete choice", font_size=24, color=GREY_A).next_to(smp, DOWN, buff=0.3)
        cap_c = label(r"a checker, a test suite,\\a judge: a black box", font_size=24, color=GREY_A).next_to(chk, DOWN, buff=0.3)
        back = CurvedArrow(chk.get_top() + UP * 0.05, th.get_top() + UP * 0.05, angle=0.5, color=C.SCORE, stroke_width=3)
        q = mtex(r"\frac{\partial R}{\partial \theta}\;=\;?", font_size=40, color=C.SCORE).next_to(back, UP, buff=0.1)
        cross = VGroup(Line(UL, DR), Line(DL, UR)).scale(0.25).set_stroke(C.PENALTY, 6).move_to(back.point_from_proportion(0.5))
        goal = mtex(r"J(\theta)", r"=", r"\mathbb{E}_{y \sim \pi_\theta(\cdot\mid x)}", r"\big[\, R(x, y) \,\big]",
                    font_size=44).to_edge(DOWN, buff=0.8)
        goal[0].set_color(C.RL_POLICY)
        goal[3].set_color(C.REWARD)
        with self.voiceover(
            "Here is the problem reinforcement learning has to solve. The parameters theta define a policy. "
            "<bookmark mark='s'/> We sample an answer from it, <bookmark mark='c'/> and a checker hands back a "
            "reward. <bookmark mark='g'/> We want to make the expected reward bigger, so we want its gradient "
            "with respect to theta. <bookmark mark='b'/> But backpropagation can't get there. Sampling is a "
            "discrete choice, and the checker might be a test suite running in a sandbox: there is no derivative "
            "to follow."
        ) as vo:
            self.play(FadeIn(th), FadeIn(pol), GrowArrow(arrows[0]))
            vo.wait_until("s")
            self.play(GrowArrow(arrows[1]), FadeIn(smp), FadeIn(cap_s))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[2]), FadeIn(chk), FadeIn(cap_c))
            vo.wait_until("g")
            self.play(Write(goal))
            vo.wait_until("b")
            self.play(Create(back), FadeIn(q))
            self.play(Create(cross))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        P, R, S = C.RL_POLICY, C.REWARD, C.SCORE
        L = [
            mtex(r"\nabla_\theta J(\theta)", r"=", r"\nabla_\theta", r"\sum_{y}", r"\pi_\theta(y)", r"\,R(y)", font_size=42),
            mtex(r"=", r"\sum_{y}", r"\nabla_\theta \pi_\theta(y)", r"\,R(y)", font_size=42),
            mtex(r"=", r"\sum_{y}", r"\pi_\theta(y)", r"\,\nabla_\theta \log \pi_\theta(y)", r"\,R(y)", font_size=42),
            mtex(r"=", r"\mathbb{E}_{y\sim\pi_\theta}", r"\big[\,", r"R(y)", r"\,\nabla_\theta \log \pi_\theta(y)", r"\,\big]", font_size=42),
            mtex(r"\approx", r"\frac{1}{N}\sum_{i=1}^{N}", r"R(y_i)", r"\,\nabla_\theta \log \pi_\theta(y_i)", font_size=42),
        ]
        L[0][0].set_color(WHITE)
        L[0][4].set_color(P)
        L[0][5].set_color(R)
        L[1][2].set_color(P)
        L[1][3].set_color(R)
        L[2][2].set_color(P)
        L[2][3].set_color(S)
        L[2][4].set_color(R)
        L[3][1].set_color(P)
        L[3][3].set_color(R)
        L[3][4].set_color(S)
        L[4][2].set_color(R)
        L[4][3].set_color(S)
        L[0].to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.8)
        for prev, cur in zip(L, L[1:]):
            cur.next_to(prev, DOWN, buff=0.38, aligned_edge=LEFT)
            cur.shift(RIGHT * (L[0][1].get_x() - cur[0].get_x()))
        reasons = [
            why(r"$R$ does not depend on $\theta$"),
            why(r"$\nabla \pi = \pi\, \nabla \log \pi$\quad(chain rule: $\nabla \log \pi = \nabla\pi / \pi$)"),
            why(r"a sum weighted by $\pi_\theta$ is an average over samples"),
            why(r"so estimate it with samples"),
        ]
        for r_, line in zip(reasons, L[1:]):
            r_.next_to(line, RIGHT, buff=0.6)
            if r_.get_right()[0] > 6.9:
                r_.shift(LEFT * (r_.get_right()[0] - 6.9))
        hl = [L[1][2], L[2][2:4], L[3][1], L[4][1]]
        name = label(r"the \emph{score function}", font_size=28, color=S)
        trick = label(r"REINFORCE (Williams, 1992):\ \ the log-derivative trick", font_size=30, color=WHITE)
        with self.voiceover(
            "The way around it is one of the most useful identities in machine learning. Write the expected reward "
            "as a sum over every possible answer y, of its probability times its reward. <bookmark mark='1'/> The "
            "reward doesn't depend on theta, so the gradient only touches the probability. <bookmark mark='2'/> "
            "Now multiply and divide by pi: the gradient of pi equals pi times the gradient of log pi. "
            "<bookmark mark='3'/> And a sum weighted by pi is just an average over samples from pi. "
            "<bookmark mark='4'/> So we can estimate the gradient without differentiating through anything we "
            "can't: sample answers, score them, and average reward times the gradient of the log probability."
        ) as vo:
            self.play(Write(L[0]), run_time=1.6)
            for k, mark in enumerate(["1", "2", "3", "4"]):
                vo.wait_until(mark)
                box = SurroundingRectangle(hl[k], color=YELLOW, buff=0.06, stroke_width=2)
                self.play(FadeIn(L[k + 1], shift=DOWN * 0.15), Create(box), FadeIn(reasons[k]), run_time=1.0)
                self.play(FadeOut(box), run_time=0.4)
        brace = Brace(L[3][4], DOWN, color=S, buff=0.08)
        name.next_to(brace, DOWN, buff=0.08)
        hdr = trick.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "That gradient of log pi has a name, <bookmark mark='n'/> the score function. And this estimator, "
            "<bookmark mark='r'/> published by Ronald Williams in 1992 as REINFORCE, is the seed of every "
            "algorithm in this video."
        ) as vo:
            vo.wait_until("n")
            # make room under line 3 for the brace's name: the last line steps down
            self.play(VGroup(L[4], reasons[3]).animate.shift(DOWN * 0.45), GrowFromCenter(brace), FadeIn(name))
            vo.wait_until("r")
            self.play(FadeIn(hdr))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gaussian(self):
        g = self.g
        mu0 = float(g["mu0"])
        samples = np.array(g["samples"], float)
        rs = np.array(g["sample_r"], float)
        plot = Plot(x_range=(-5, 5), y_range=(0, 1.15), width=11.0, height=3.4, x_ticks=[-4, -2, 0, 2, 4],
                    x_label=r"action $a$ (a number the policy chooses)")
        plot.move_to(DOWN * 0.9)
        xs = np.linspace(-5, 5, 300)
        rew = plot.line(xs, gauss_reward(xs), color=C.REWARD, stroke_width=4)
        rew_l = label(r"reward $R(a)$", font_size=28, color=C.REWARD).next_to(plot.c2p(2.0, 1.0), UR, buff=0.1)
        mu = ValueTracker(mu0)
        k = 2.0  # density drawn x2 so it reads at the same scale as the reward

        def dens():
            m = mu.get_value()
            return VGroup(plot.area(xs, k * pdf(xs, m), C.RL_POLICY, opacity=0.22),
                          plot.line(xs, k * pdf(xs, m), color=C.RL_POLICY, stroke_width=3))
        dcurve = always_redraw(dens)
        dl = label(r"policy $\pi_\mu = \mathcal{N}(\mu, 1)$", font_size=28, color=C.RL_POLICY)
        dl.next_to(plot.c2p(-4.6, 0.95), RIGHT, buff=0)
        mline = always_redraw(lambda: DashedLine(plot.c2p(mu.get_value(), 0), plot.c2p(mu.get_value(), 0.92),
                                                 color=C.RL_POLICY, stroke_width=2))
        mlab = always_redraw(lambda: mtex(r"\mu", font_size=30, color=C.RL_POLICY).next_to(plot.c2p(mu.get_value(), 0.92), UP, buff=0.06))
        dots = VGroup(*[Dot(plot.c2p(a, 0), radius=0.07, color=WHITE) for a in samples])
        score = mtex(r"\nabla_\mu \log \pi_\mu(a)", r"=", r"a - \mu", font_size=36).to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.6)
        score[0].set_color(C.SCORE)
        score[2].set_color(C.SCORE)
        weighted = mtex(r"\times R(a)", font_size=36).next_to(score, RIGHT, buff=0.3)
        weighted[0][1:].set_color(C.REWARD)
        tag = exact_tag(r"exact: 10 real samples").to_corner(UR, buff=0.3)

        def arrows(weights, y0=1.25, dy=0.16, scale=0.55, color=C.SCORE):
            g_ = VGroup()
            for i, (a, w) in enumerate(zip(samples, weights)):
                start = plot.c2p(a, 0) + UP * (y0 + dy * i)
                L = (a - mu0) * w * scale
                if abs(L) < 0.04:
                    g_.add(Dot(start, radius=0.03, color=color))
                    continue
                g_.add(Arrow(start, start + RIGHT * L, buff=0, stroke_width=3.5, color=color,
                             max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=12))
            return g_
        raw = arrows(np.ones_like(samples))
        wtd = arrows(rs * 2.2, color=C.REWARD)
        net_raw = float(np.mean(samples - mu0))
        net_w = float(np.mean(rs * (samples - mu0)))
        with self.voiceover(
            "To see what this does, shrink the problem to one dimension. The policy picks a number a from a bell "
            "curve centered at mu, and the reward is this landscape with two hills. <bookmark mark='s'/> Sample "
            "ten actions. <bookmark mark='d'/> For a bell curve, the score is simply a minus mu: each sample says "
            "move toward me, in proportion to how far away I am."
        ) as vo:
            self.play(FadeIn(plot), Create(rew), FadeIn(rew_l), FadeIn(dcurve), FadeIn(dl), FadeIn(mline), FadeIn(mlab))
            vo.wait_until("s")
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.08), FadeIn(tag))
            vo.wait_until("d")
            self.play(FadeIn(score))
            self.play(LaggedStart(*[GrowArrow(a) if isinstance(a, Arrow) else FadeIn(a) for a in raw], lag_ratio=0.06))
        cancel = label(rf"unweighted, they nearly cancel: average push ${net_raw:+.2f}$", font_size=26, color=C.SCORE)
        cancel.move_to(UP * 2.45)
        zero = mtex(r"\mathbb{E}\big[\nabla \log \pi\big] = \sum_a \nabla \pi(a) = \nabla \sum_a \pi(a) = \nabla 1 = 0",
                    font_size=30).next_to(cancel, DOWN, buff=0.15)
        with self.voiceover(
            "On their own, these pushes cancel out on average. In fact the score always has mean zero: "
            "<bookmark mark='z'/> its average is the gradient of the total probability, and the total is always "
            "one. Remember this; it will matter in a minute."
        ) as vo:
            self.play(FadeIn(cancel))
            vo.wait_until("z")
            self.play(Write(zero), run_time=1.6)
        self.play(FadeOut(cancel), FadeOut(zero))
        wl = label(rf"weighted by reward: average push ${net_w:+.2f}$, toward the tall hill", font_size=26, color=C.REWARD)
        wl.move_to(UP * 2.45)
        with self.voiceover(
            "Now <bookmark mark='w'/> weight each push by the reward its sample earned. Samples near the tall hill "
            "keep their arrows; samples in the valley lose theirs. The symmetry breaks, and the average points "
            "toward higher reward."
        ) as vo:
            vo.wait_until("w")
            self.play(FadeIn(weighted), ReplacementTransform(raw, wtd), run_time=1.6)
            self.play(FadeIn(wl))
        path = np.array(g["paths_b"][0], float)
        with self.voiceover(
            "Take a small step along that average, sample again, and repeat. <bookmark mark='m'/> The bell curve "
            "climbs the hill, and nobody ever computed the derivative of the reward."
        ) as vo:
            self.play(FadeOut(wtd), FadeOut(dots), FadeOut(wl))
            vo.wait_until("m")
            self.play(mu.animate.set_value(path[-1]), run_time=3.5, rate_func=lambda t: np.interp(
                t, np.linspace(0, 1, len(path)), (path - path[0]) / (path[-1] - path[0])))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tokens_view(self):
        lp = mtex(r"\log \pi_\theta(y \mid x)", r"=", r"\sum_{t=1}^{T}", r"\log \pi_\theta(y_t \mid x, y_{<t})",
                  font_size=42).to_edge(UP, buff=0.6)
        lp[0].set_color(C.RL_POLICY)
        lp[3].set_color(C.RL_POLICY)
        gl = mtex(r"\nabla_\theta J", r"=", r"\mathbb{E}\Big[\,", r"R(x,y)", r"\sum_{t}", r"\nabla_\theta \log \pi_\theta(y_t \mid x, y_{<t})",
                  r"\Big]", font_size=42).next_to(lp, DOWN, buff=0.5)
        gl[3].set_color(C.REWARD)
        gl[5].set_color(C.SCORE)
        t = load("tree")
        prompt = prompt_text(t["a"], t["b"])
        strip = tokens(prompt, answer_text(t["a"], t["b"], True), font_size=28).move_to(DOWN * 0.9)
        ans_cells = strip[len(prompt):]
        ups = VGroup(*[Arrow(c.get_bottom() + DOWN * 0.75, c.get_bottom() + DOWN * 0.08, buff=0, stroke_width=4,
                             color=C.SCORE, max_tip_length_to_length_ratio=0.35) for c in ans_cells])
        rlab = label(r"every token of the answer is pushed by the \emph{same} number: the answer's reward",
                     font_size=26, color=GREY_A).next_to(ups, DOWN, buff=0.25).set_x(0)
        sft = mtex(r"\text{supervised: }\ \ -\textstyle\sum_t \log \pi_\theta(y^\star_t \mid \cdot)", font_size=34)
        rl = mtex(r"\text{RL: }\ \ -R(x,y)\textstyle\sum_t \log \pi_\theta(y_t \mid \cdot),\quad y \sim \pi_\theta", font_size=34)
        rl[0][4:9].set_color(C.REWARD)
        cmp_ = VGroup(sft, rl).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "For a language model the answer is a sequence of tokens, and its log probability is a sum, one term "
            "per token. <bookmark mark='g'/> So the policy gradient becomes: the answer's reward times the sum of "
            "every token's score. <bookmark mark='t'/> Each token of a sampled answer gets pushed up, or down, by "
            "the same amount: the reward of the whole answer."
        ) as vo:
            self.play(Write(lp), run_time=1.5)
            vo.wait_until("g")
            self.play(Write(gl), run_time=1.6)
            vo.wait_until("t")
            self.play(FadeIn(strip, lag_ratio=0.05))
            self.play(LaggedStart(*[GrowArrow(a) for a in ups], lag_ratio=0.05), FadeIn(rlab))
        with self.voiceover(
            "Compare that with supervised fine-tuning. There, you maximize the log probability of a reference "
            "answer someone wrote. <bookmark mark='r'/> Here, you do the same thing to the model's own answer, "
            "weighted by how well it did. Reinforcement learning is fine-tuning on your own samples, graded."
        ) as vo:
            self.play(FadeOut(rlab), FadeIn(sft))
            vo.wait_until("r")
            self.play(FadeIn(rl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def softmax_view(self):
        z0 = np.array([1.4, 0.9, 0.2, -0.3, -0.8])
        pi0 = np.exp(z0) / np.exp(z0).sum()
        a = 1  # the sampled token
        names = ["7", "6", "8", "5", "3"]
        eta = 2.2
        z1 = z0 + eta * (np.eye(5)[a] - pi0)
        pi1 = np.exp(z1) / np.exp(z1).sum()
        base_y = -2.2
        W = 1.2

        def bars(p, color=C.RL_POLICY):
            return VGroup(*[Rectangle(width=0.8, height=max(0.02, 6.0 * v), stroke_width=0, fill_color=color,
                                      fill_opacity=0.85).move_to([(i - 2) * W - 2.5, base_y + 3.0 * v, 0])
                            for i, v in enumerate(p)])
        b0 = bars(pi0)
        axis = Line([-5.6, base_y, 0], [0.6, base_y, 0], color=GREY_C)
        nl = VGroup(*[Mono_(n).move_to([(i - 2) * W - 2.5, base_y - 0.35, 0]) for i, n in enumerate(names)])
        pl = VGroup(*[MathTex(f"{v:.2f}", font_size=24, color=GREY_A).next_to(b, UP, buff=0.08) for v, b in zip(pi0, b0)])
        mark = label(r"sampled", font_size=24, color=C.SCORE).next_to(nl[a], DOWN, buff=0.15)
        f = mtex(r"\frac{\partial \log \pi(a)}{\partial z_b}", r"=", r"\mathbf{1}[b = a] - \pi(b)", font_size=38)
        f[0].set_color(C.SCORE)
        f.move_to(RIGHT * 3.8 + UP * 1.4)
        expl = VGroup(label(r"sampled token: $+\,(1 - \pi(a))$", font_size=26, color=C.REWARD),
                      label(r"every other token: $-\,\pi(b)$", font_size=26, color=C.PENALTY),
                      label(r"(rich get taxed, in proportion)", font_size=24, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(f, DOWN, buff=0.45)
        head = label(r"One step of the next-token softmax, $z$ = logits", font_size=30).to_edge(UP, buff=0.4)
        pl1 = VGroup(*[MathTex(f"{v:.2f}", font_size=24, color=GREY_A) for v in pi1])
        b1 = bars(pi1)
        for t, b in zip(pl1, b1):
            t.next_to(b, UP, buff=0.08)
        with self.voiceover(
            "What does pushing up one token actually do? Inside the model, the next token comes from a softmax over "
            "logits. <bookmark mark='f'/> The score of the sampled token, with respect to the logits, is one minus "
            "its probability for the sampled token, <bookmark mark='o'/> and minus the probability for every other "
            "token. <bookmark mark='u'/> So a positive reward raises the sampled token and takes mass from the "
            "others, the popular ones most of all."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(b0), FadeIn(nl), FadeIn(pl))
            self.play(FadeIn(mark))
            vo.wait_until("f")
            self.play(Write(f))
            self.play(FadeIn(expl[0]))
            vo.wait_until("o")
            self.play(FadeIn(expl[1]), FadeIn(expl[2]))
            vo.wait_until("u")
            self.play(Transform(b0, b1), Transform(pl, pl1), run_time=1.8)
        self.wait(0.5)
        self.clear_scene()


def Mono_(s: str):
    from videos.rl.common import Mono

    return Mono(s, font_size=28, color=WHITE)
