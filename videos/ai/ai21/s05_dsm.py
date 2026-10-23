from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import DATA, NOISE, PART, SCORE, bars_chart, load, take_away

LOSS_C, CONST_C, ERR_C = WHITE, GREY_B, SCORE


class DSM(VoiceoverScene):
    def construct(self):
        self.card()
        self.explicit()
        self.theorem()
        self.check()
        self.levels()

    def card(self):
        card = chapter_card(4, r"Denoising score matching", r"How do you fit a score you can never see?", part=PART)
        with self.voiceover("Chapter four. Denoising score matching."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def explicit(self):
        rows = [
            cmath(r"J(\theta)", r"=", r"\tfrac12\, \mathbb E_{p}\, \big\| s_\theta(x) - \nabla \log p(x) \big\|^2",
                  colors={r"\tfrac12\, \mathbb E_{p}\, \big\| s_\theta(x) - \nabla \log p(x) \big\|^2": WHITE}, font_size=36),
            cmath(r"J(\theta)", r"=", r"\mathbb E_{p}\Big[\operatorname{tr} \nabla_x s_\theta(x) + \tfrac12 \| s_\theta(x)\|^2\Big]"
                  r" + \text{const}", font_size=36),
        ]
        whys = [why(r"the target is unknown"), why(r"integrate by parts \ (Hyv\"arinen, 2005)")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-2.0, buff=0.7, edge=6.85)
        d = 512 * 512 * 3
        cost = VGroup(label(r"$\operatorname{tr} \nabla_x s_\theta$: \ one backward pass per dimension of $x$", font_size=26,
                            color=GREY_A),
                      label(rf"a $512 \times 512$ colour image: \ ${d:,}$ of them, \ for every example".replace(",", "{,}"),
                            font_size=26, color=SCORE)).arrange(DOWN, buff=0.2).move_to([0, -1.4, 0])
        cite_ = cite(r"A.~Hyv\"arinen, \textit{Estimation of Non-Normalized Statistical Models by Score Matching} (2005)",
                     corner=DR)
        with self.voiceover(
            "Tweedie says the network should learn the score. But nobody gives us the score of real images to fit. "
            "In 2005 Aapo Hyvarinen faced this for energy models: fit a function s to the score, by squared error, "
            "when the target is unknown. <bookmark mark='a'/> Integrating by parts removes the target: what is left "
            "is the trace of the Jacobian of s, plus its squared length, averaged over the data. <bookmark mark='b'/> "
            "But the trace costs one backward pass per dimension: for one colour image of 512 by 512 pixels, "
            f"{d:,} of them, for every training example."
        ) as vo:
            self.play(FadeIn(cite_))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(cost, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        card = theorem_card(r"denoising score matching", MathTex(
            r"\tfrac12\, \mathbb E_{x,\, \tilde x}\, \big\| s_\theta(\tilde x) - \nabla_{\tilde x} \log q(\tilde x \mid x)\big\|^2"
            r" = \tfrac12\, \mathbb E_{\tilde x}\, \big\| s_\theta(\tilde x) - \nabla \log q_\sigma(\tilde x)\big\|^2 + C",
            font_size=28), who=r"Vincent (2011): \ $\tilde x = x + \sigma n$, \ $q_\sigma$ the noised data; \ $C$ does not "
                               r"depend on $\theta$", width=9.6)
        card.to_edge(UP, buff=0.3)
        rows = [
            cmath(r"\text{left}", r"=", r"\tfrac12 \mathbb E\|s_\theta\|^2 - \mathbb E\big[s_\theta \cdot \nabla \log q(\tilde x"
                  r" \mid x)\big] + C_1", font_size=30),
            cmath(r"\mathbb E_{\tilde x}\big[s_\theta \cdot \nabla \log q_\sigma\big]", r"=",
                  r"\int s_\theta(\tilde x) \cdot \nabla q_\sigma(\tilde x)\, d\tilde x", font_size=30),
            cmath(r"\phantom{\mathbb E}", r"=", r"\iint s_\theta(\tilde x) \cdot \nabla_{\tilde x}\, q(\tilde x \mid x)\; p(x)\, "
                  r"dx\, d\tilde x", font_size=30),
            cmath(r"\phantom{\mathbb E}", r"=", r"\mathbb E_{x,\, \tilde x}\big[s_\theta \cdot \nabla \log q(\tilde x \mid x)\big]",
                  font_size=30),
        ]
        whys = [why(r"expand the square"), why(r"$\nabla \log q = \nabla q / q$"),
                why(r"$q_\sigma(\tilde x) = \int q(\tilde x \mid x)\, p(x)\, dx$"), why(r"undo the first step: \ the cross terms match")]
        step = ladder(self, rows, whys, keep=4, top=1.05, x=-1.4, buff=0.38, edge=6.85)
        tail = label(r"and $\nabla_{\tilde x} \log q(\tilde x \mid x) = -(\tilde x - x)/\sigma^2 = -n/\sigma$: \ "
                     r"matching it is guessing the noise", font_size=24, color=SCORE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 2011 Pascal Vincent found the way around. Add noise to each example, and fit the score of the noise "
            "itself, which we know exactly. <bookmark mark='a'/> The theorem: that loss equals the loss against the "
            "score of the whole noised data, plus a constant. Here is why. Expand the square on the left. "
            "<bookmark mark='b'/> The only term that could differ is the cross term. Write the noised data's score "
            "as its gradient over itself; <bookmark mark='c'/> the noised data is an average of noise around each "
            "example, so its gradient is an average of theirs; <bookmark mark='d'/> and that is the left side's cross "
            "term. Everything else is a constant. <bookmark mark='e'/> And the score of the added noise is minus the "
            "noise over sigma: fitting it is chapter two's noise guessing, exactly."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeIn(tail))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        d = load("denoiser")
        checks = [int(c) for c in d["checks"]]
        ts = [float(t) for t in d["dsm_ts"]]
        seeds = [int(s) for s in d["seeds"]]
        T = {s: np.asarray(d[f"terms_s{s}"]) for s in seeds}  # check, level, (loss, const, err, cross)
        k = 0  # the lowest noise level: the hardest
        xs = np.arange(len(checks))
        vals = np.concatenate([T[s][:, k, :3].ravel() for s in seeds])
        lo, hi = math.floor(math.log10(max(vals[vals > 0].min(), 1e-4))), math.ceil(math.log10(vals.max()))
        g = axes([0, len(checks) - 1], [lo, hi], x_length=6.6, y_length=4.0, xlabel=r"training step", xticks=[],
                 ylabel=rf"noise level $t = {ts[k]:g}$ \ (log scale)", yticks=list(range(lo, hi + 1)),
                 yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.4, -0.25, 0])
        g.add(*[MathTex(f"{c:,}".replace(",", "{,}"), font_size=18, color=GREY_B).next_to(g.ax.c2p(i, lo), DOWN, buff=0.12)
                for i, c in enumerate(checks)])
        L10 = lambda v: math.log10(max(v, 1e-6))
        lines = VGroup()
        for s in seeds:
            op = 1.0 if s == seeds[0] else 0.35
            lines.add(VGroup(curve(g.ax, xs, [L10(v) for v in T[s][:, k, 0]], LOSS_C, 3 if op == 1 else 1.5).set_stroke(opacity=op),
                             curve(g.ax, xs, [L10(v) for v in T[s][:, k, 1]], CONST_C, 2).set_stroke(opacity=op),
                             curve(g.ax, xs, [L10(v) for v in T[s][:, k, 2]], ERR_C, 3 if op == 1 else 1.5).set_stroke(opacity=op)))
        gap = VGroup(*[Dot(g.ax.c2p(i, L10(max(T[seeds[0]][i, k, 0] - T[seeds[0]][i, k, 1], 1e-6))), radius=0.07, color=WHITE)
                       .set_stroke(ERR_C, 2) for i in range(len(checks))])
        lg = VGroup(label(r"the loss on fresh noise", font_size=22, color=LOSS_C),
                    label(r"$C$: \ the loss of the exact score", font_size=22, color=CONST_C),
                    label(r"error against the exact score", font_size=22, color=ERR_C),
                    label(r"dots: \ loss minus $C$", font_size=22, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        lg.move_to([3.9, 1.2, 0])
        fin = T[seeds[0]][-1]
        cross = np.array([np.abs(T[s][-1, :, 3]).max() for s in seeds]).max()
        rows = [[r"$t$", r"loss", r"$C$", r"loss $- C$", r"score error"]]
        for j, t in enumerate(ts):
            rows.append([f"${t:g}$", f"${fin[j, 0]:.4f}$", f"${fin[j, 1]:.4f}$", f"${fin[j, 0] - fin[j, 1]:.4f}$",
                         f"${fin[j, 2]:.4f}$"])
        tab = VGroup(*[VGroup(*[label(c, font_size=18, color=(GREY_A if i == 0 else [WHITE, LOSS_C, CONST_C, WHITE, ERR_C][j]))
                                for j, c in enumerate(r)]) for i, r in enumerate(rows)])
        for i, r in enumerate(tab):
            for j, c in enumerate(r):
                c.move_to([1.35 + 1.2 * j, -1.0 - 0.36 * i, 0])
        n_seeds = len(seeds)
        f0 = fin[k]
        with self.voiceover(
            "Our letters let us check the theorem directly, because there the exact score is known. Take our "
            f"denoiser at each checkpoint of its training, at the lowest noise level, t equal to {ts[k]:g}. "
            "<bookmark mark='a'/> The white curve is the loss on fresh noise. The grey line is the constant: the "
            "loss that even the exact score would have, because the noise in a noisy point can't be fully "
            "recovered. <bookmark mark='b'/> The orange curve is the network's error against the exact score, "
            "measured directly. <bookmark mark='c'/> The theorem says loss minus constant is that error, and the "
            f"dots sit on the curve: at the end, {f0[0]:.4f} minus {f0[1]:.4f} against {f0[2]:.4f}. The cross term "
            f"that the proof says averages away is at most {cross:.4f} at the end of training, in {n_seeds} seeds. "
            "<bookmark mark='d'/> The loss never reaches zero, and doesn't have to: the gap above the constant is "
            "the part training can remove."
        ) as vo:
            self.play(FadeIn(g), Create(lines[0][0]), FadeIn(lg[0]))
            vo.wait_until("a")
            self.play(Create(lines[0][1]), FadeIn(lg[1]))
            vo.wait_until("b")
            self.play(Create(lines[0][2]), FadeIn(lg[2]), *[FadeIn(l_) for l_ in lines[1:]])
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(g_, scale=1.5) for g_ in gap], lag_ratio=0.1), FadeIn(lg[3]))
            vo.wait_until("d")
            self.play(FadeIn(tab))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def levels(self):
        d = load("denoiser")
        ts = [float(t) for t in d["dsm_ts"]]
        seeds = [int(s) for s in d["seeds"]]
        E = np.array([np.asarray(d[f"terms_s{s}"])[-1, :, 2] for s in seeds])  # seed, level
        m = E.mean(0)
        L10 = np.log10(np.maximum(m, 1e-6))
        lo = math.floor(L10.min())
        vals = L10 - lo + 0.3
        ch = bars_chart(vals, [ERR_C] * len(ts), [rf"$t = {t:g}$" for t in ts], height=3.2, bar_w=0.9, gap=0.6,
                        value_fmt=lambda v: f"{10 ** (v + lo - 0.3):.4f}", font_size=22)
        ch.move_to([-3.0, -0.4, 0])
        cap = label(rf"error against the exact score, \ end of training, \ mean of ${len(seeds)}$ seeds \ (log heights)",
                    font_size=20, color=GREY_A).next_to(ch, UP, buff=0.35)
        card = history_card(2019, r"Song \& Ermon: \ noise-conditional score networks", r"one network, \ many noise "
                            r"levels, \ sampled by annealed Langevin (Part 20)", color=C.HUMAN, width=5.6, font_size=20)
        card.move_to([3.6, 0.9, 0])
        ta = take_away(r"Learning to denoise is learning the score, \ at every noise level, \ with nothing but regression.")
        worst, best = ts[int(np.argmax(m))], ts[int(np.argmin(m))]
        where = ("the nearly clean levels, where the score is sharp around each stroke, are the hardest." if worst == min(ts)
                 else "the hardest level is not the cleanest one.")
        with self.voiceover(
            f"Where is the score hardest to learn? At the end of training, the error is largest at t equal to "
            f"{worst:g} and smallest at {best:g}: " + where + " <bookmark mark='a'/> In 2019 Yang Song and Stefano Ermon trained one network for many noise levels "
            "this way, and sampled with Part 20's annealed Langevin. <bookmark mark='b'/> Denoising, at every noise "
            "level, by plain regression: that is what every diffusion model learns."
        ) as vo:
            self.play(FadeIn(cap), FadeIn(ch))
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(ta, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
