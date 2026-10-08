from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import Plot, label, load, mtex, note, pct_fmt, real_tag, source, why


class DPO(VoiceoverScene):
    def construct(self):
        self.invert()
        self.cancel()
        self.gradient()
        self.offline()

    # ------------------------------------------------------------------
    def invert(self):
        s1 = mtex(r"\pi^\star(y \mid x)", r"=", r"\frac{1}{Z(x)}\,\pi_{\text{ref}}(y\mid x)\, e^{\,r(x,y)/\beta}", font_size=42)
        s2 = mtex(r"\log \pi^\star", r"=", r"\log \pi_{\text{ref}} + \frac{r}{\beta} - \log Z(x)", font_size=42)
        s3 = mtex(r"r(x, y)", r"=", r"\beta \log \frac{\pi^\star(y \mid x)}{\pi_{\text{ref}}(y \mid x)}", r"+", r"\beta \log Z(x)", font_size=46)
        s1[0].set_color(YELLOW)
        s3[0].set_color(C.REWARD)
        s3[2].set_color(YELLOW)
        s3[4].set_color(GREY_B)
        col = VGroup(s1, s2, s3).arrange(DOWN, buff=0.45).move_to(UP * 0.4)
        w2 = why(r"take logs").next_to(s2, RIGHT, buff=0.5)
        w3 = why(r"solve for $r$").next_to(s3, RIGHT, buff=0.4)
        box = SurroundingRectangle(s3, color=C.REWARD, buff=0.2, corner_radius=0.1)
        cap = label(r"every policy implies a reward: the one it would be optimal for", font_size=30, color=C.REWARD)
        cap.to_edge(DOWN, buff=0.6)
        src = source(r"Rafailov, Sharma, Mitchell, Ermon, Manning \& Finn, \emph{Direct Preference Optimization}, NeurIPS 2023")
        with self.voiceover(
            "In 2023, a group at Stanford ran this formula backwards. If the optimal policy is the reference tilted "
            "by the reward, <bookmark mark='l'/> take logs, <bookmark mark='s'/> and solve for the reward. "
            "<bookmark mark='c'/> Any policy implies a reward: the log ratio of its probabilities to the "
            "reference's, times beta, plus a term that depends only on the prompt."
        ) as vo:
            self.play(Write(s1), FadeIn(src))
            vo.wait_until("l")
            self.play(FadeIn(s2, shift=DOWN * 0.1), FadeIn(w2))
            vo.wait_until("s")
            self.play(FadeIn(s3, shift=DOWN * 0.1), FadeIn(w3))
            vo.wait_until("c")
            self.play(Create(box), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cancel(self):
        bt = mtex(r"P(y_w \succ y_l)", r"=", r"\sigma\big(", r"r(x, y_w)", r"-", r"r(x, y_l)", r"\big)", font_size=42)
        bt[3].set_color(C.REWARD)
        bt[5].set_color(C.PENALTY)
        bt.to_edge(UP, buff=0.6)
        sub = mtex(r"=", r"\sigma\Big(", r"\beta \log \frac{\pi^\star(y_w)}{\pi_{\text{ref}}(y_w)}", r"+ \beta\log Z(x)", r"-",
                   r"\beta \log \frac{\pi^\star(y_l)}{\pi_{\text{ref}}(y_l)}", r"- \beta\log Z(x)", r"\Big)", font_size=40)
        sub[2].set_color(C.REWARD)
        sub[5].set_color(C.PENALTY)
        sub[3].set_color(GREY_B)
        sub[6].set_color(GREY_B)
        if sub.width > 12.8:
            sub.width = 12.8
        sub.next_to(bt, DOWN, buff=0.5).set_x(0)
        x1 = Cross(sub[3], stroke_color=YELLOW, stroke_width=4)
        x2 = Cross(sub[6], stroke_color=YELLOW, stroke_width=4)
        cz = label(r"same prompt, same $Z(x)$: it cancels", font_size=26, color=YELLOW).next_to(sub, DOWN, buff=0.25)
        loss = mtex(r"\mathcal{L}_{\text{DPO}}(\theta)", r"=", r"-\log \sigma\Big(", r"\beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)}",
                    r"-", r"\beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l\mid x)}", r"\Big)", font_size=42)
        loss[3].set_color(C.REWARD)
        loss[5].set_color(C.PENALTY)
        lb = SurroundingRectangle(loss, color=YELLOW, buff=0.2, corner_radius=0.1)
        lg = VGroup(loss, lb).to_edge(DOWN, buff=0.9)
        ln = label(r"maximum likelihood of the comparisons, with $\pi^\star \to \pi_\theta$: no reward model, no sampling, no critic",
                   font_size=24, color=GREY_A).next_to(lg, DOWN, buff=0.15)
        with self.voiceover(
            "Now plug that implied reward into the Bradley-Terry model of comparisons. The probability that the "
            "preferred answer wins is the sigmoid of the reward difference. <bookmark mark='s'/> Substitute, "
            "<bookmark mark='z'/> and the troublesome normalizer Z appears twice, with opposite signs. Both answers "
            "answer the same prompt, so it cancels. <bookmark mark='l'/> What's left depends only on the policy and "
            "the reference. Fit it by maximum likelihood, and you have Direct Preference Optimization: a simple "
            "classification loss on pairs. No reward model, no sampling, no critic."
        ) as vo:
            self.play(Write(bt))
            vo.wait_until("s")
            self.play(FadeIn(sub, shift=DOWN * 0.1), run_time=1.4)
            vo.wait_until("z")
            self.play(Create(x1), Create(x2), FadeIn(cz))
            self.play(sub[3].animate.set_opacity(0.15), sub[6].animate.set_opacity(0.15), x1.animate.set_opacity(0.3),
                      x2.animate.set_opacity(0.3))
            vo.wait_until("l")
            self.play(Write(loss), Create(lb), run_time=1.6)
            self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gradient(self):
        g = mtex(r"-\nabla_\theta \mathcal{L}_{\text{DPO}}", r"=", r"\beta\,", r"\sigma\big(\hat r_\theta(y_l) - \hat r_\theta(y_w)\big)",
                 r"\Big[", r"\nabla \log \pi_\theta(y_w)", r"-", r"\nabla \log \pi_\theta(y_l)", r"\Big]", font_size=40)
        g[3].set_color(YELLOW)
        g[5].set_color(C.REWARD)
        g[7].set_color(C.PENALTY)
        g.to_edge(UP, buff=0.6)
        rdef = mtex(r"\hat r_\theta(y) = \beta \log \frac{\pi_\theta(y\mid x)}{\pi_{\text{ref}}(y\mid x)}", font_size=34).next_to(g, DOWN, buff=0.3)
        rdl = label(r"the implicit reward", font_size=24, color=GREY_A).next_to(rdef, RIGHT, buff=0.3)
        plot = Plot(x_range=(-5, 5), y_range=(0, 1), width=6.4, height=3.0, x_ticks=[-4, -2, 0, 2, 4], y_ticks=[0, 0.5, 1],
                    x_label=r"$\hat r_\theta(y_w) - \hat r_\theta(y_l)$: how well the pair is already ranked",
                    y_label=r"weight on this pair")
        plot.move_to(DOWN * 1.6 + LEFT * 0.5)
        xs = np.linspace(-5, 5, 200)
        w = plot.line(xs, 1 / (1 + np.exp(xs)), color=YELLOW, stroke_width=4)
        a1 = label(r"ranked wrong:\\push hard", font_size=24, color=YELLOW).next_to(plot.c2p(-3.5, 0.95), RIGHT, buff=0.1)
        a2 = label(r"already right:\\leave it", font_size=24, color=GREY_A).next_to(plot.c2p(2.2, 0.35), RIGHT, buff=0.1)
        with self.voiceover(
            "Its gradient is easy to read. Raise the log probability of the preferred answer, lower the rejected "
            "one, <bookmark mark='w'/> and weight the pair by a sigmoid of how badly the model's own implicit reward "
            "currently ranks it. Pairs it already gets right fade away; pairs it gets wrong get the full push."
        ) as vo:
            self.play(Write(g), run_time=2)
            self.play(FadeIn(rdef), FadeIn(rdl))
            vo.wait_until("w")
            self.play(FadeIn(plot), Create(w))
            self.play(FadeIn(a1), FadeIn(a2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def offline(self):
        d = load("dpo")
        ev = d["evals"]
        steps = np.array([e["step"] for e in ev], float)
        acc = np.array([e["pass1"] for e in ev])
        dw = np.array([e["dlogp_w"] for e in ev])
        dl = np.array([e["dlogp_l"] for e in ev])
        S = steps[-1]
        k = int(np.argmax(acc))
        assert acc[k] > acc[0] + 0.05 and acc[-1] < acc[0] - 0.3 and dw[-1] < -1 and dl[-1] < dw[-1], (acc, dw, dl)
        top = Plot(x_range=(0, S), y_range=(0, 1), width=6.0, height=3.4, x_ticks=list(np.linspace(0, S, 4).astype(int)),
                   y_ticks=[0, 0.5, 1], y_fmt=pct_fmt, x_label=r"DPO steps (64 pairs each)", y_label=r"held-out accuracy")
        top.move_to(LEFT * 3.4 + DOWN * 0.5)
        lo = float(np.floor(dl.min()))
        bot = Plot(x_range=(0, S), y_range=(lo, 1), width=5.2, height=3.4, x_ticks=list(np.linspace(0, S, 4).astype(int)),
                   y_ticks=[lo, 0], x_label=r"DPO steps", y_label=r"change in $\log \pi(y)$, vs.\ the reference")
        bot.move_to(RIGHT * 3.6 + DOWN * 0.5)
        la = top.line(steps, acc, color=C.REWARD, stroke_width=4)
        pk = Dot(top.c2p(steps[k], acc[k]), radius=0.08, color=YELLOW)
        pkl = label(rf"peak {acc[k] * 100:.0f}\%", font_size=24, color=YELLOW).next_to(pk, UP, buff=0.1)
        lw_ = bot.line(steps, dw, color=C.REWARD, stroke_width=4)
        ll_ = bot.line(steps, dl, color=C.PENALTY, stroke_width=4)
        z = bot.hline(0, color=GREY_D)
        kw = label(r"preferred answers", font_size=22, color=C.REWARD).next_to(bot.c2p(S, dw[-1]), UP, buff=0.1).shift(LEFT * 0.9)
        kl = label(r"rejected answers", font_size=22, color=C.PENALTY).next_to(bot.c2p(S, dl[-1]), UP, buff=0.1).shift(LEFT * 0.9)
        head = label(rf"DPO on the adder: {d['n_pairs']:,} fixed pairs (right vs.\ wrong), sampled once".replace(",", "{,}"),
                     font_size=28).to_edge(UP, buff=0.35)
        foot = label(r"the gap widens by pushing \emph{both} down: ``likelihood displacement'' (Razin et al.\ 2024; DPO-Positive, Pal et al.\ 2024)",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.62)
        with self.voiceover(
            "Here it is on the adder, from four thousand pairs of right and wrong answers, sampled once from the "
            f"starting model. <bookmark mark='a'/> Accuracy climbs from {acc[0] * 100:.0f} to {acc[k] * 100:.0f} percent. "
            "<bookmark mark='c'/> Then it collapses. <bookmark mark='w'/> Look at what the loss is doing: it only "
            "cares about the gap between the preferred and the rejected answer, and it found that pushing both down "
            "widens the gap fastest. The probability doesn't vanish; it flows to answers that were in neither set, "
            "and the model starts writing nonsense. This failure has a name, likelihood displacement."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(real_tag()))
            vo.wait_until("a")
            n = k + 1
            self.play(Create(top.line(steps[:n], acc[:n], color=C.REWARD, stroke_width=4)), run_time=1.5)
            self.play(FadeIn(pk), FadeIn(pkl))
            vo.wait_until("c")
            self.play(Create(top.line(steps[k:], acc[k:], color=C.REWARD, stroke_width=4)), run_time=1.5)
            vo.wait_until("w")
            self.play(FadeIn(bot), Create(z), Create(lw_), Create(ll_), FadeIn(kw), FadeIn(kl), run_time=2)
            self.play(FadeIn(foot))
        with self.voiceover(
            "The fix people use is to stop early, regularize, or keep sampling: train on the model's own fresh answers "
            "instead of a fixed set. Which is exactly what the reinforcement learning methods do. For reasoning, the "
            "field went back to sampling, and to a much simpler kind of reward."
        ):
            pass
        self.wait(0.3)
        self.clear_scene()
