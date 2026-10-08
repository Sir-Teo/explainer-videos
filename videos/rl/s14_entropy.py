from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import Mono, Plot, exact_tag, label, load, mtex, note, real_tag, smooth, source, why
from videos.rl.compute import HERO, load_run


def softmax(z):
    e = np.exp(z - z.max())
    return e / e.sum()


def entropy(p):
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())


class Entropy(VoiceoverScene):
    def construct(self):
        self.hero = load_run(HERO)
        self.collapse()
        self.derive()
        self.picture()
        self.measured()
        self.clip_higher()

    # ------------------------------------------------------------------
    def collapse(self):
        log = [l for l in self.hero["log"] if "entropy" in l]
        st = np.array([l["step"] for l in log], float)
        H = np.array([l["entropy"] for l in log])
        S = int(np.ceil(st[-1] / 30) * 30)
        plot = Plot(x_range=(0, S), y_range=(0, H.max() * 1.1), width=8.0, height=3.8,
                    x_ticks=list(range(0, S + 1, 30)), y_ticks=list(np.round(np.linspace(0, H.max(), 3), 2)),
                    x_label=r"RL step", y_label=r"entropy of the next token (nats)")
        plot.move_to(DOWN * 0.6)
        line = plot.line(st, smooth(H, 5), color=C.ENTROPY, stroke_width=4)
        Hdef = mtex(r"\mathcal{H}(\pi) = -\sum_a \pi(a) \log \pi(a)", font_size=40).to_edge(UP, buff=0.4)
        n = label(r"how uncertain the policy is: its budget for trying new things", font_size=26, color=GREY_A).next_to(Hdef, DOWN, buff=0.15)
        r0 = H[:3].mean()
        r1 = H[-5:].mean()
        res = label(rf"falls from ${r0:.2f}$ to ${r1:.3f}$: a factor of ${r0 / r1:.1f}$", font_size=26, color=C.ENTROPY)
        res.next_to(plot.c2p(S * 0.55, H.max() * 0.8), RIGHT, buff=0)
        with self.voiceover(
            "Every RL run on a language model shows the same signature. The policy's entropy, its average uncertainty "
            "about the next token, collapses. <bookmark mark='c'/> Here it is in our run. Entropy is the "
            "exploration budget: once the policy is certain, it stops sampling anything new, and learning stalls. "
            "Why does it fall, and can we control it?"
        ) as vo:
            self.play(Write(Hdef), FadeIn(n))
            self.play(FadeIn(plot), FadeIn(real_tag()))
            vo.wait_until("c")
            self.play(Create(line), run_time=2.5)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        l1 = mtex(r"\frac{\partial \mathcal{H}}{\partial z_b}", r"=", r"-\pi(b)\Big(\log \pi(b) - \mathbb{E}_{a\sim\pi}\big[\log\pi(a)\big]\Big)", font_size=38)
        l2 = mtex(r"\Delta \mathcal{H}", r"\approx", r"\sum_b \frac{\partial \mathcal{H}}{\partial z_b}\,\Delta z_b", r"=",
                  r"-\operatorname{Cov}_{a \sim \pi}\big(\log \pi(a),\ \Delta z_a\big)", font_size=38)
        l2[4].set_color(C.ENTROPY)
        l3 = mtex(r"\text{vanilla PG: }\ \Delta z_a = \eta\,\pi(a) A(a)", r"\;\Rightarrow\;",
                  r"\Delta \mathcal{H} \approx -\eta\,\operatorname{Cov}\big(\log \pi,\ \pi A\big)", font_size=36)
        l4 = mtex(r"\text{natural PG: }\ \Delta z_a = \eta\, A(a)", r"\;\Rightarrow\;",
                  r"\Delta \mathcal{H} \approx -\eta\,\operatorname{Cov}\big(\log \pi,\ A\big)", font_size=36)
        l3[2].set_color(C.ENTROPY)
        l4[2].set_color(C.ENTROPY)
        col = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(UP * 0.2)
        w1 = why(r"differentiate the entropy of a softmax").next_to(l1, RIGHT, buff=0.4)
        w2 = why(r"first order in the step").next_to(l2, DOWN, buff=0.1).align_to(l2, RIGHT)
        src = source(r"Cui et al., \emph{The Entropy Mechanism of RL for Reasoning Language Models}, arXiv 2505.22617 (2025)")
        with self.voiceover(
            "For a softmax, the derivative of the entropy with respect to a logit is minus that token's probability, "
            "times how much more surprising than average it is. <bookmark mark='2'/> Sum over a small change of all "
            "the logits, and the change in entropy is minus a covariance: between how likely each token already is, "
            "and how much its logit moves. <bookmark mark='3'/> Plug in the policy gradient, which moves each logit "
            "by its probability times its advantage, <bookmark mark='4'/> or the natural gradient, which moves it by "
            "the advantage alone. Either way: the entropy falls whenever the tokens the model already likes are the "
            "ones being rewarded."
        ) as vo:
            self.play(Write(l1), FadeIn(w1), FadeIn(src))
            vo.wait_until("2")
            self.play(Write(l2), FadeIn(w2))
            vo.wait_until("3")
            self.play(FadeIn(l3))
            vo.wait_until("4")
            self.play(FadeIn(l4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def picture(self):
        z = np.array([2.0, 1.0, 0.3, -0.5, -1.2])
        p = softmax(z)
        cases = [("confident token rewarded", np.array([1.0, -0.4, -0.3, -0.2, -0.1])),
                 ("rare token rewarded", np.array([-0.3, -0.2, -0.1, 0.1, 1.0]))]
        eta = 1.6
        W = 0.9

        def bars(q, x0, color=C.RL_POLICY):
            return VGroup(*[Rectangle(width=W * 0.7, height=max(0.02, 3.4 * v), stroke_width=0, fill_color=color, fill_opacity=0.85)
                            .move_to([x0 + i * W, -1.9 + 1.7 * v, 0]) for i, v in enumerate(q)])
        panels = VGroup()
        anims = []
        for k, (title, A) in enumerate(cases):
            x0 = -4.9 + k * 6.4
            b0 = bars(p, x0)
            q = softmax(z + eta * A)
            b1 = bars(q, x0)
            ax = Line([x0 - 0.5, -1.9, 0], [x0 + 4 * W + 0.5, -1.9, 0], color=GREY_C)
            advs = VGroup(*[MathTex(f"{a:+.1f}", font_size=24, color=C.REWARD if a > 0 else C.PENALTY).move_to([x0 + i * W, -2.25, 0])
                            for i, a in enumerate(A)])
            t = label(title, font_size=28).move_to([x0 + 2 * W, 2.9, 0])
            H0, H1 = entropy(p), entropy(q)
            hl = MathTex(rf"\mathcal{{H}}: {H0:.2f} \to {H1:.2f}", font_size=32, color=C.ENTROPY).next_to(t, DOWN, buff=0.2)
            cov = np.sum(p * (np.log(p) - np.sum(p * np.log(p))) * (A - np.sum(p * A)))
            cl = MathTex(rf"\operatorname{{Cov}}(\log\pi, A) = {cov:+.2f}", font_size=28, color=GREY_A).next_to(hl, DOWN, buff=0.12)
            panels.add(VGroup(ax, b0, advs, t))
            anims.append((b0, b1, hl, cl))
        al = label(r"advantage $A$", font_size=22, color=GREY_A).next_to(panels[0][2], LEFT, buff=0.2)
        with self.voiceover(
            "Two examples, each with the same five-token distribution. <bookmark mark='a'/> On the left, the token "
            "the model already likes is the one that gets rewarded: a positive covariance. One natural gradient "
            "step, and the distribution sharpens; the entropy drops. <bookmark mark='b'/> On the right, a rare token "
            "is rewarded. The covariance is negative, and the step spreads probability out: entropy rises. In RL on "
            "a pretrained model, the first case is overwhelmingly common: the confident tokens are usually the right "
            "ones, so entropy steadily drains away."
        ) as vo:
            self.play(FadeIn(panels[0]), FadeIn(al), FadeIn(exact_tag()))
            vo.wait_until("a")
            b0, b1, hl, cl = anims[0]
            self.play(Transform(b0, b1), FadeIn(hl), FadeIn(cl), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
            b0, b1, hl, cl = anims[1]
            self.play(Transform(b0, b1), FadeIn(hl), FadeIn(cl), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        log = [l for l in self.hero["log"] if "entropy" in l]
        st = np.array([l["step"] for l in log], float)
        H = np.array([l["entropy"] for l in log])
        cov = np.array([l["cov"] for l in log])
        dH = np.diff(smooth(H, 9))
        S = int(np.ceil(st[-1] / 30) * 30)
        top = Plot(x_range=(0, S), y_range=(min(0, cov.min()), cov.max() * 1.1), width=8.0, height=2.3,
                   x_ticks=[], y_ticks=[0], x_label=None,
                   y_label=r"$\operatorname{Cov}(\log \pi(y_t),\ A_t)$ in each batch")
        top.move_to(UP * 1.35)
        lo_, hi_ = float(np.percentile(dH, 2)), float(np.percentile(dH, 99))
        dHc = np.clip(dH, lo_ * 1.05, hi_ * 1.05)
        bot = Plot(x_range=(0, S), y_range=(min(lo_, -1e-4) * 1.1, max(hi_, 1e-4) * 1.1), width=8.0, height=2.3,
                   x_ticks=list(range(0, S + 1, 30)), y_ticks=[0], x_label=r"RL step",
                   y_label=r"change in entropy per step")
        bot.move_to(DOWN * 2.0)
        lc = top.line(st, smooth(cov, 5), color=YELLOW, stroke_width=3.5)
        lh = bot.line(st[1:], dHc, color=C.ENTROPY, stroke_width=3.5)
        z1 = top.hline(0, color=GREY_D)
        z2 = bot.hline(0, color=GREY_D)
        corr = float(np.corrcoef(smooth(cov, 9)[1:], dH)[0, 1])
        cl = label(rf"correlation: ${corr:+.2f}$", font_size=28, color=YELLOW).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Does the formula hold up in a real network, where every logit is tied to every other through shared "
            "weights? Here is the covariance between each sampled token's log probability and its advantage, "
            "measured in every batch of our run, <bookmark mark='h'/> and here is how much the entropy actually "
            "changed. The covariance stays positive, and the entropy keeps falling; the bigger the covariance, the "
            f"faster the fall, a correlation of {corr:.1f}."
        ) as vo:
            self.play(FadeIn(top), Create(z1), FadeIn(real_tag()))
            self.play(Create(lc), run_time=2)
            vo.wait_until("h")
            self.play(FadeIn(bot), Create(z2), Create(lh), run_time=2)
            self.play(FadeIn(cl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def clip_higher(self):
        probs = [0.9, 0.2, 0.01]
        rows = VGroup()
        W = 6.0
        for p in probs:
            name = MathTex(rf"\pi_{{\text{{old}}}} = {p:g}", font_size=30, color=C.OLD_POLICY)
            track = Line(ORIGIN, RIGHT * W, color=GREY_D, stroke_width=6)
            sym = Line(RIGHT * W * p * 0.8, RIGHT * W * min(1, p * 1.2), color=C.RATIO, stroke_width=14)
            hi = Line(RIGHT * W * min(1, p * 1.2), RIGHT * W * min(1, p * 1.28), color=YELLOW, stroke_width=14)
            dot = Dot(RIGHT * W * p, radius=0.07, color=WHITE)
            rng_ = MathTex(rf"\text{{up to }} {min(1, p * 1.28):.3g}", font_size=26, color=YELLOW)
            g = VGroup(track, sym, hi, dot)
            row = VGroup(name, g, rng_)
            name.next_to(g, LEFT, buff=0.4)
            rng_.next_to(g, RIGHT, buff=0.4)
            rows.add(row)
        rows.arrange(DOWN, buff=0.5).move_to(UP * 0.5)
        for row in rows:
            row[1].align_to(rows[0][1], LEFT)
            row[0].next_to(row[1], LEFT, buff=0.4)
            row[2].next_to(row[1], RIGHT, buff=0.4)
        head = label(r"Clip-higher (DAPO): $1 - 0.2 \le \rho \le 1 + 0.28$", font_size=32).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"PPO's symmetric clip caps how fast a rare token can rise, but not how fast a likely one does", font_size=26),
            label(r"DAPO on AIME 2024: naive GRPO 30\% $\to$ 50\% with clip-higher, dynamic sampling, token-level loss, length shaping",
                  font_size=24, color=GREY_A),
            label(r"also: Clip-Cov and KL-Cov act directly on the high-covariance tokens (Cui et al.\ 2025)", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.7)
        src = source(r"Yu et al., \emph{DAPO}, arXiv 2503.14476 (2025), Table 1")
        with self.voiceover(
            "Remember the clipping windows. With a symmetric clip, a rare token can rise by at most twenty percent "
            "of its probability per round, while a likely one can rise all the way to certainty. That's exactly the "
            "positive covariance again: the clip itself favors sharpening. <bookmark mark='h'/> ByteDance's DAPO "
            "simply raises the upper limit to one point two eight, giving rare tokens more room to grow. "
            "<bookmark mark='f'/> Along with dynamic sampling, a token-level loss and a soft penalty for overlong "
            "answers, it took a naive GRPO run on the AIME math competition from thirty to fifty percent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            self.play(LaggedStart(*[FadeIn(VGroup(r[0], r[1][0], r[1][1], r[1][3])) for r in rows], lag_ratio=0.15))
            vo.wait_until("h")
            self.play(LaggedStart(*[AnimationGroup(Create(r[1][2]), FadeIn(r[2])) for r in rows], lag_ratio=0.15))
            vo.wait_until("f")
            self.play(FadeIn(facts))
        self.wait(0.4)
        self.clear_scene()
