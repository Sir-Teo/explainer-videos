from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import Plot, exact_tag, label, load, mtex, tagged


class Baselines(VoiceoverScene):
    def construct(self):
        self.g = load("gauss")
        self.c = load("cloud")
        self.offset()
        self.derive()
        self.cloud()
        self.optimal()
        self.advantage()

    # ------------------------------------------------------------------
    def offset(self):
        g = self.g
        nb, b = np.array(g["paths_nb"], float), np.array(g["paths_b"], float)
        steps = np.arange(nb.shape[1])
        assert np.all(np.abs(b[:, -1] - 2.0) < 0.35) and np.ptp(nb[:, -1]) > 3, (b[:, -1], nb[:, -1])
        nb, b = np.clip(nb, -4, 3.2), np.clip(b, -4, 3.2)
        plot = Plot(x_range=(0, steps[-1]), y_range=(-4, 3.2), width=8.2, height=4.4, x_ticks=[0, 20, 40, 60],
                    y_ticks=[-4, -2, 0, 2], x_label=r"step", y_label=r"$\mu$, the policy's center")
        plot.move_to(DOWN * 0.5 + LEFT * 1.6)
        peak = plot.hline(2.0, color=C.REWARD)
        pk = label(r"the tall hill", font_size=24, color=C.REWARD).next_to(plot.c2p(steps[-1], 2.0), RIGHT, buff=0.15)
        lines_nb = VGroup(*[plot.line(steps, p, color=C.PENALTY, stroke_width=2.5) for p in nb])
        lines_b = VGroup(*[plot.line(steps, p, color=C.REWARD, stroke_width=2.5) for p in b])
        head = label(r"Same problem, but the reward is $2 + R(a)$: every sample earns at least 2", font_size=30).to_edge(UP, buff=0.55)
        k1 = label(r"6 runs, weight $= R$", font_size=26, color=C.PENALTY)
        k2 = label(r"6 runs, weight $= R - \bar R$", font_size=26, color=C.REWARD)
        keys = VGroup(k1, k2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(plot, RIGHT, buff=0.5).shift(DOWN * 0.6)
        with self.voiceover(
            "There's a catch. Suppose the grader is generous, and every answer earns at least two points. Then "
            "every sample pushes the policy toward itself; the pushes still average out to the right direction, "
            "but each estimate is mostly noise. <bookmark mark='n'/> Here are six runs of exactly the algorithm "
            "we just derived. They wander, and some never find the hill. <bookmark mark='b'/> Now make one change: "
            "subtract the batch's average reward before weighting. All six runs climb straight to the top."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), Create(peak), FadeIn(pk), FadeIn(exact_tag(r"real runs, exact toy").to_corner(DR, buff=0.3)))
            vo.wait_until("n")
            self.play(Create(lines_nb, lag_ratio=0.15), FadeIn(k1), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(lines_b, lag_ratio=0.15), FadeIn(k2), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        l1 = mtex(r"\mathbb{E}\big[(R - b)\,\nabla \log \pi\big]", r"=", r"\mathbb{E}\big[R\,\nabla\log\pi\big]",
                  r"-\; b\,", r"\mathbb{E}\big[\nabla \log \pi\big]", font_size=44)
        l1[0][3:8].set_color(C.BASELINE)
        l1[2][2].set_color(C.REWARD)
        l1[4].set_color(C.SCORE)
        l1[3].set_color(C.BASELINE)
        l2 = mtex(r"=", r"\nabla_\theta J", r"-\; b \cdot", r"0", font_size=44)
        l2[2].set_color(C.BASELINE)
        l2[3].set_color(C.SCORE)
        l1.move_to(UP * 1.6)
        l2.next_to(l1, DOWN, buff=0.45, aligned_edge=LEFT).shift(RIGHT * (l1[1].get_x() - l2[0].get_x()))
        br = Brace(l1[4], DOWN, color=C.SCORE)
        brl = label(r"the score has mean zero", font_size=26, color=C.SCORE).next_to(br, DOWN, buff=0.08)
        concl = VGroup(
            label(r"Any baseline $b$ that does not depend on the sampled answer:", font_size=30),
            label(r"the same gradient on average, but a different amount of noise.", font_size=30, color=YELLOW),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Why are we allowed to do that? Subtract any number b from the reward, and look at the expected "
            "gradient. It splits into the policy gradient, minus b times the expected score. <bookmark mark='z'/> "
            "And the expected score is zero, as we saw. So any baseline that doesn't depend on the sampled answer "
            "leaves the gradient unchanged on average. <bookmark mark='c'/> What it changes is the noise."
        ) as vo:
            self.play(Write(l1), run_time=2)
            vo.wait_until("z")
            self.play(GrowFromCenter(br), FadeIn(brl))
            self.play(FadeIn(l2, shift=DOWN * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cloud(self):
        c = self.c
        mu = np.array(c["mu"], float)
        gx = np.array(c["grid"], float)
        surf = np.array(c["surf"], float)
        # left: the reward landscape as a heat map (pixels), the policy, single samples and their arrows
        S = 4.6
        img = np.zeros((len(gx), len(gx), 3), np.uint8)
        col = np.array([0x83, 0xC1, 0x67], float)
        bg = np.array([0x0E, 0x11, 0x17], float)
        t = np.clip(surf / surf.max(), 0, 1)[::-1]
        img[:] = (bg + (col - bg) * t[..., None] ** 0.8).astype(np.uint8)
        heat = ImageMobject(img).set_height(S)
        heat.move_to(LEFT * 3.7 + DOWN * 0.35)
        frame = SurroundingRectangle(heat, buff=0, color=GREY_C, stroke_width=1.5)

        def w2s(p):
            o = heat.get_center()
            return o + RIGHT * (p[0] / 8.0) * S + UP * (p[1] / 8.0) * S
        circles = VGroup(*[Circle(radius=r * S / 8, color=C.RL_POLICY, stroke_width=2.5, stroke_opacity=0.9 - 0.25 * k)
                           .move_to(w2s(mu)) for k, r in enumerate([1.0, 2.0])])
        # both labels above the panel: below it, a far sample's long arrow needs the room
        cl = label(r"policy $\mathcal{N}(\mu, I)$", font_size=24, color=C.RL_POLICY)
        lt = label(r"on a reward landscape", font_size=24, color=C.REWARD)
        VGroup(cl, lt).arrange(RIGHT, buff=0.15).next_to(frame, UP, buff=0.12)
        singles = np.array(c["singles"], float)
        sR = np.array(c["singles_R"], float)
        sd = VGroup(*[Dot(w2s(p), radius=0.05, color=WHITE) for p in singles])
        # right: gradient space
        R_ = 1.6
        gp = Plot(x_range=(-R_, R_), y_range=(-R_, R_), width=4.6, height=4.6, x_ticks=[-1, 0, 1], y_ticks=[-1, 0, 1])
        gp.move_to(RIGHT * 3.6 + DOWN * 0.35)
        zero = gp.c2p(0, 0)
        ax = VGroup(DashedLine(gp.c2p(-R_, 0), gp.c2p(R_, 0), color=GREY_D, stroke_width=1.2),
                    DashedLine(gp.c2p(0, -R_), gp.c2p(0, R_), color=GREY_D, stroke_width=1.2))
        gt = label(r"gradient estimates (each: a batch of 16)", font_size=24, color=GREY_A).next_to(gp, UP, buff=0.12)
        true = np.array(c["true"], float)
        tarrow = Arrow(zero, gp.c2p(*true), buff=0, color=C.SCORE, stroke_width=5, max_tip_length_to_length_ratio=0.3)
        tl = tagged(r"true gradient", color=C.SCORE, font_size=22).next_to(gp.c2p(1.0, 1.2), UP, buff=0.05)
        tl_line = DashedLine(tl.get_bottom(), gp.c2p(*true), color=C.SCORE, stroke_width=1.5)

        def pts(est, color):
            e = np.clip(np.array(est, float), -R_ * 0.98, R_ * 0.98)
            return VGroup(*[Dot(gp.c2p(*p), radius=0.03, color=color, fill_opacity=0.7) for p in e])
        nb = pts(c["est_nb"], C.PENALTY)
        wb = pts(c["est_b"], C.REWARD)
        vn = label(rf"no baseline: variance ${c['var_nb'] / c['batch']:.2f}$", font_size=26, color=C.PENALTY)
        vb = label(rf"baseline $b = \bar R$: variance ${c['var_mean'] / c['batch']:.3f}$", font_size=26, color=C.REWARD)
        ratio = c["var_nb"] / c["var_mean"]
        assert 15 < ratio < 40, ratio
        vt = VGroup(vn, vb).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.15).shift(RIGHT * 2.6)
        arrows = VGroup()
        vecs = [np.array([*((p - mu) * r * 0.11), 0.0]) * S / 8 * 4 for p, r in zip(singles, sR)]
        # one common scale for all arrows (their relative lengths are the point); the longest is capped at 1.1
        k = min(1.0, 1.1 / max(np.linalg.norm(v) for v in vecs))
        for p, v in zip(singles, vecs):
            arrows.add(Arrow(w2s(p), w2s(p) + k * v, buff=0, stroke_width=2.5, color=C.SCORE, max_tip_length_to_length_ratio=0.25))
        tag = exact_tag(r"exact toy, real samples")
        with self.voiceover(
            "Let's watch the noise directly. A policy over a two-dimensional action, on a landscape with two "
            "hills, plus the constant two points. <bookmark mark='s'/> Each sample suggests a direction: from the "
            "center toward itself, scaled by its reward. <bookmark mark='g'/> Average a batch of sixteen such "
            "suggestions and you get one gradient estimate, a single point on the right. <bookmark mark='m'/> "
            "Three hundred batches make this cloud. Its center is the true gradient, but the cloud is so wide "
            "that a single estimate often points the wrong way."
        ) as vo:
            self.play(FadeIn(heat), Create(frame), FadeIn(lt), Create(circles), FadeIn(cl), FadeIn(tag))
            vo.wait_until("s")
            self.play(FadeIn(sd, lag_ratio=0.1))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), run_time=1.4)
            vo.wait_until("g")
            self.play(FadeIn(gp), FadeIn(ax), FadeIn(gt))
            vo.wait_until("m")
            self.play(LaggedStart(*[FadeIn(d) for d in nb], lag_ratio=0.004), run_time=2.0)
            self.play(GrowArrow(tarrow), FadeIn(tl), Create(tl_line), FadeIn(vn))
        with self.voiceover(
            "Now subtract the average reward. <bookmark mark='b'/> Same center, but the cloud collapses: "
            f"the variance drops by a factor of {ratio:.0f}. The signal was always there; the baseline removes the "
            "part of the reward that every answer gets anyway."
        ) as vo:
            vo.wait_until("b")
            self.play(nb.animate.set_opacity(0.15), FadeIn(wb, lag_ratio=0.003), run_time=1.6)
            self.play(FadeIn(vb))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def optimal(self):
        c = self.c
        bs, var = np.array(c["bs"], float), np.array(c["var"], float)
        n = c["batch"]
        plot = Plot(x_range=(0, 4.5), y_range=(0, 0.8), width=6.4, height=3.8, x_ticks=[0, 1, 2, 3, 4],
                    y_ticks=[0, 0.4, 0.8], x_label=r"baseline $b$", y_label=r"variance of the estimate")
        plot.move_to(RIGHT * 3.0 + DOWN * 0.6)
        curve = plot.line(bs, var / n, color=C.BASELINE, stroke_width=4)
        bstar, Rm = float(c["bstar"]), float(c["Rmean"])
        assert abs(bstar - Rm) < 0.05
        dstar = Dot(plot.c2p(bstar, float(np.interp(bstar, bs, var)) / n), radius=0.08, color=YELLOW)
        lstar = label(rf"minimum at $b^\star = {bstar:.2f}$", font_size=24, color=YELLOW).next_to(dstar, UP, buff=0.5)
        lm = label(rf"average reward $= {Rm:.2f}$", font_size=24, color=GREY_A).next_to(lstar, UP, buff=0.12)
        v = mtex(r"\operatorname{Var}(b)", r"=", r"\mathbb{E}\big[(R - b)^2\,\|g\|^2\big] - \|\nabla J\|^2", font_size=34)
        d = mtex(r"\frac{d}{db}\operatorname{Var} = 0", r"\;\Rightarrow\;", r"b^\star = \frac{\mathbb{E}\big[R\,\|g\|^2\big]}{\mathbb{E}\big[\|g\|^2\big]}", font_size=34)
        d[2].set_color(YELLOW)
        gdef = label(r"$g = \nabla \log \pi$, the score", font_size=24, color=C.SCORE)
        col = VGroup(v, d, gdef).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(LEFT, buff=0.5).shift(UP * 0.4)
        foot = label(r"$\approx$ the average reward, whenever $\|g\|^2$ is unrelated to $R$", font_size=26, color=GREY_A)
        foot.next_to(col, DOWN, buff=0.45).align_to(col, LEFT)
        with self.voiceover(
            "Which baseline is best? The variance is a quadratic in b, <bookmark mark='p'/> a parabola, so set its "
            "derivative to zero. <bookmark mark='d'/> The best baseline is the average reward, weighted by the "
            "squared size of the score. <bookmark mark='a'/> In practice that's very close to the plain average "
            "reward. Here, they agree to within a percent."
        ) as vo:
            self.play(Write(v))
            vo.wait_until("p")
            self.play(FadeIn(plot), Create(curve), run_time=1.5)
            vo.wait_until("d")
            self.play(Write(d), FadeIn(gdef))
            self.play(FadeIn(dstar, scale=2), FadeIn(lstar))
            vo.wait_until("a")
            self.play(FadeIn(lm), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def advantage(self):
        A = mtex(r"A(x, y)", r"=", r"R(x,y)", r"-", r"V(x)", font_size=48).to_edge(UP, buff=0.6)
        A[0].set_color(C.ADVANTAGE)
        A[2].set_color(C.REWARD)
        A[4].set_color(C.BASELINE)
        Vdef = label(r"$V(x) = \mathbb{E}_{y \sim \pi}\big[R(x,y)\big]$: how well the policy does on this prompt, on average",
                     font_size=26, color=C.BASELINE).next_to(A, DOWN, buff=0.3)
        name = label(r"the \emph{advantage}: better or worse than usual?", font_size=30, color=C.ADVANTAGE).next_to(Vdef, DOWN, buff=0.35)

        def panel(title, p):
            t = label(title, font_size=28)
            pl = label(rf"$V = p = {p}$", font_size=26, color=C.BASELINE)
            base = Line(LEFT * 1.6, RIGHT * 1.6, color=GREY_C)
            up = Rectangle(width=1.0, height=2.2 * (1 - p), stroke_width=0, fill_color=C.REWARD, fill_opacity=0.85)
            dn = Rectangle(width=1.0, height=2.2 * p, stroke_width=0, fill_color=C.PENALTY, fill_opacity=0.85)
            up.next_to(base, UP, buff=0).shift(LEFT * 0.7)
            dn.next_to(base, DOWN, buff=0).shift(RIGHT * 0.7)
            lu = MathTex(rf"+{1 - p:.1f}", font_size=30, color=C.REWARD).next_to(up, UP, buff=0.08)
            ld = MathTex(rf"-{p:.1f}", font_size=30, color=C.PENALTY).next_to(dn, DOWN, buff=0.08)
            cu = label(r"right", font_size=22, color=GREY_A).next_to(base, DOWN, buff=0.08).shift(LEFT * 0.7)
            cd = label(r"wrong", font_size=22, color=GREY_A).next_to(base, UP, buff=0.08).shift(RIGHT * 0.7)
            g_ = VGroup(base, up, dn, lu, ld, cu, cd)
            return VGroup(t, pl, g_).arrange(DOWN, buff=0.25)
        easy = panel(r"an easy prompt", 0.9)
        hard = panel(r"a hard prompt", 0.1)
        pans = VGroup(easy, hard).arrange(RIGHT, buff=2.2).to_edge(DOWN, buff=0.35)
        rr = label(r"reward 1 if right, 0 if wrong; $p$ = chance of being right", font_size=24, color=GREY_A)
        rr.next_to(pans, UP, buff=0.15)
        intro = label(r"Different prompts deserve different baselines", font_size=40)
        self.add(intro)
        self.play(FadeIn(intro))
        with self.voiceover(
            "One more step. Different prompts deserve different baselines: a policy that usually solves an easy "
            "problem shouldn't get excited about solving it again. <bookmark mark='a'/> So subtract V of x, the "
            "average reward the policy gets on this particular prompt. What's left is called the advantage: was "
            "this answer better or worse than usual? <bookmark mark='p'/> With a reward of one for right and zero "
            "for wrong, V is just the chance p of being right. On an easy prompt, a right answer earns a tiny plus "
            "zero point one, and a mistake a big minus zero point nine. <bookmark mark='h'/> On a hard prompt it's "
            "the reverse: a rare success is worth a lot."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(intro), Write(A))
            self.play(FadeIn(Vdef), FadeIn(name))
            vo.wait_until("p")
            self.play(FadeIn(rr), FadeIn(easy))
            vo.wait_until("h")
            self.play(FadeIn(hard))
        with self.voiceover(
            "But to compute an advantage, we need V, and nobody hands it to us. And when the answer is a long "
            "sequence of tokens with a single reward at the end, a deeper question appears: which tokens deserve "
            "the credit?"
        ):
            pass
        self.wait(0.3)
        self.clear_scene()
