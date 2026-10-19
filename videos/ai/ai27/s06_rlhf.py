from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import GOLD, KLC, PART, POLICY, PROXY, REF, REWARD, load, said


def late(h, col, k=30):
    return float(np.mean(h[-k:, col]))


def early(h, col, k=10):
    return float(np.mean(h[:k, col]))


class RLHF(VoiceoverScene):
    def construct(self):
        self.card()
        self.objective()
        self.optimum()
        self.bars()
        self.runs()

    def card(self):
        card = chapter_card(5, r"Reinforcement learning on a leash", r"Why not just maximize the reward?",
                            lit=(2022,), part=PART)
        with self.voiceover("Chapter five. Reinforcement learning on a leash."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def objective(self):
        obj = cmath(r"\max_\theta", r"\ \mathbb E_{x,\ y \sim \pi_\theta(\cdot \mid x)}\big[\, r_\phi(x, y) \,\big]",
                    r"\ -\ \beta\,", r"\mathrm{KL}\big(\pi_\theta(\cdot \mid x)\,\|\,\pi_{\mathrm{ref}}(\cdot \mid x)\big)",
                    font_size=38).move_to(UP * 2.2)
        obj[1].set_color(PROXY)
        obj[3].set_color(KLC)
        b1 = brace_note(obj[1], r"the reward model's score", color=PROXY, font_size=22)
        b2 = brace_note(obj[3], r"stay close to the fine-tuned model", color=KLC, font_size=22)
        why1 = VGroup(
            label(r"without the leash: \ the policy finds what the reward model overrates", font_size=26,
                  color=GREY_A),
            label(r"and forgets how to write: \ answers drift out of the model's world", font_size=26, color=GREY_A),
            label(r"$\beta$ sets the trade: \ reward gained per nat of divergence", font_size=26, color=KLC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.5)
        with self.voiceover(
            "With a reward model in hand, the plan is reinforcement learning: generate answers, score them, and push "
            "the model toward high scores with the policy gradient of Part 26. But maximizing the reward model alone "
            "is a mistake, for two reasons. <bookmark mark='a'/> The reward model is only an approximation, and a "
            "strong optimizer finds the places where it's wrong. <bookmark mark='b'/> And the policy can drift into "
            "text unlike anything it learned from, losing the fluency it had. <bookmark mark='c'/> So the objective "
            "adds a leash: a penalty, beta times the KL divergence from the fine-tuned model we started with, the "
            "reference. Beta sets the exchange rate: how much reward is worth one nat of divergence."
        ) as vo:
            self.play(Write(obj))
            self.play(FadeIn(b1), FadeIn(b2))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(why1[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def optimum(self):
        rows = [
            cmath(r"J(\pi)", r"=", r"\sum_y \pi(y)\, r(y) - \beta \sum_y \pi(y) \log \frac{\pi(y)}{\pi_{\mathrm{ref}}(y)}",
                  font_size=34),
            cmath(r"J(\pi)", r"=", r"-\beta \sum_y \pi(y) \log \frac{\pi(y)}{\pi_{\mathrm{ref}}(y)\, e^{r(y)/\beta}}",
                  font_size=34),
            cmath(r"J(\pi)", r"=", r"-\beta\, \mathrm{KL}\big(\pi \,\|\, \pi^*\big) + \beta \log Z", font_size=34),
            cmath(r"\pi^*(y)", r"=", r"\frac{1}{Z}\, \pi_{\mathrm{ref}}(y)\, e^{r(y)/\beta}", font_size=38),
        ]
        rows[3][0].set_color(POLICY)
        whys = [why(r"for one prompt $x$: \ expected reward minus the leash"),
                why(r"$r = \beta \log e^{r/\beta}$: \ one sum"),
                why(r"$Z = \sum_y \pi_{\mathrm{ref}}(y) e^{r(y)/\beta}$: \ multiply and divide"),
                why(r"$\mathrm{KL} \ge 0$, \ zero only at $\pi = \pi^*$: \ the best policy")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.0, buff=0.5, edge=6.9)
        res = label(r"the reference model, \ reweighted by $e^{\text{reward}/\beta}$", font_size=28, color=POLICY)
        res.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "This objective has an exact solution, and it's worth deriving, because the rest of the part leans on it. "
            "Fix a prompt and write the objective as a sum over possible answers y. <bookmark mark='a'/> Fold the "
            "reward into the logarithm: r is beta times the log of e to the r over beta. <bookmark mark='b'/> Divide "
            "and multiply by the normalizing constant Z, and what's left is minus beta times a KL divergence, plus a "
            "constant. <bookmark mark='c'/> A KL divergence is never negative and is zero only when the two "
            "distributions agree, Part 1's Gibbs inequality. So the best policy is pi star: the reference model's "
            "probabilities, reweighted by e to the reward over beta. <bookmark mark='d'/> Large beta: barely move "
            "from the reference. Small beta: pile everything onto the highest-reward answers."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bars(self):
        d = load("closed")
        r, ref, pis, betas = np.asarray(d["r"]), np.asarray(d["ref"]), np.asarray(d["pi"]), list(d["betas"])
        k = len(r)
        vals = ValueTracker(0)
        stages = [ref] + [pis[i] for i in range(len(betas))]
        names = [r"\pi_{\mathrm{ref}}"] + [rf"\pi^*,\ \beta = {b:g}" for b in betas]
        W, H, x0 = 0.75, 3.2, -4.4

        def bar_group():
            t = vals.get_value()
            i = min(int(t), len(stages) - 2)
            f = t - i
            p = (1 - f) * stages[i] + f * stages[i + 1]
            return VGroup(*[Rectangle(width=W * 0.8, height=max(H * p[j], 0.01), stroke_width=0, fill_opacity=0.9,
                                      fill_color=POLICY).move_to([x0 + W * j, -1.6, 0], aligned_edge=DOWN)
                            for j in range(k)])

        bars = always_redraw(bar_group)
        rl = VGroup(*[MathTex(rf"{v:+.2f}", font_size=22, color=GOLD).move_to([x0 + W * j, -1.95, 0])
                      for j, v in enumerate(r)])
        rlab = label(r"reward of each answer", font_size=20, color=GOLD).next_to(rl, DOWN, buff=0.15)
        name = always_redraw(lambda: MathTex(names[min(int(round(vals.get_value())), len(names) - 1)], font_size=40,
                                             color=POLICY).move_to([x0 + W * (k - 1) / 2, 2.6, 0]))
        lo, hi = said(d["cands"][0], chars=34, font_size=18), said(d["cands"][-1], chars=34, font_size=18)
        lo_l = label(rf"lowest reward, \ ${r[0]:+.2f}$", font_size=20, color=GOLD)
        hi_l = label(rf"highest reward, \ ${r[-1]:+.2f}$", font_size=20, color=GOLD)
        right = VGroup(VGroup(hi_l, hi).arrange(DOWN, buff=0.12), VGroup(lo_l, lo).arrange(DOWN, buff=0.12))
        right.arrange(DOWN, buff=0.5).move_to([3.6, 0.2, 0])
        tag = note(rf"computed: \ eight lines our fine-tuned model wrote about the {d['topic']}; \ "
                   r"$\pi_{\mathrm{ref}}$ renormalized over them").to_corner(DR, buff=0.2)
        with self.voiceover(
            f"Here's the formula on eight real answers our fine-tuned model wrote about the {d['topic']}, sorted by "
            "their reward. The bars start as the reference model's probabilities, renormalized over these eight. "
            "<bookmark mark='a'/> With beta ten, the leash is tight, and almost nothing moves. "
            "<bookmark mark='b'/> At beta one, probability starts to flow toward the better answers. "
            "<bookmark mark='c'/> At beta zero point one, nearly all of it sits on the best answer. That is what "
            "reinforcement learning with a KL penalty is aiming at, though it has to get there by sampling, one "
            "gradient step at a time."
        ) as vo:
            self.add(bars, name)
            self.play(FadeIn(rl), FadeIn(rlab), FadeIn(right), FadeIn(tag))
            for j, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(vals.animate.set_value(j + 1 + (1 if j == 2 else 0)), run_time=2.0)
        bars.clear_updaters()
        name.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def runs(self):
        d = load("rlhf")
        betas = list(d["betas"])
        keys = [f"b{b:g}".replace(".", "_") for b in betas]
        H = [np.asarray(d[k]) for k in keys]
        steps = H[0][:, 0]
        S = int(steps[-1])
        lo = min(float(h[:, 1:3].min()) for h in H)
        hi = max(float(h[:, 1:3].max()) for h in H)
        cols = (POLICY, C.PENALTY)
        panels = VGroup()
        for i, (b, h) in enumerate(zip(betas, H)):
            g = axes([0, S], [np.floor(lo * 2) / 2, np.ceil(hi * 2) / 2], x_length=5.4, y_length=3.0,
                     xlabel=r"steps of reinforcement learning", ylabel=rf"$\beta = {b:g}$", xticks=[0, S],
                     center=[-3.3 + 6.6 * i, 0.4, 0])
            sm = lambda y: np.convolve(y, np.ones(9) / 9, mode="same")
            pc = VMobject().set_points_smoothly([g.ax.c2p(x, y) for x, y in zip(steps[4:-4], sm(h[:, 1])[4:-4])])
            gc = VMobject().set_points_smoothly([g.ax.c2p(x, y) for x, y in zip(steps[4:-4], sm(h[:, 2])[4:-4])])
            pc.set_stroke(PROXY, 4)
            gc.set_stroke(GOLD, 4)
            panels.add(VGroup(g, pc, gc))
        lg = legend([(PROXY, r"the reward model's score"), (GOLD, r"gold: \ the taste it stands in for")],
                    font_size=20).to_edge(UP, buff=0.4)
        tag = note(r"computed: \ policy gradient with a KL penalty on our fine-tuned model, \ $16$ lines a step")
        tag.to_corner(DR, buff=0.2)
        (p0, g0, k0), (p1, g1, k1) = [(late(h, 1), late(h, 2), late(h, 3)) for h in H]
        gs = early(H[0], 2)
        if g1 < g0 - 0.05 and p1 > p0:
            verdict = (f"With the loose leash the reward model's score climbs higher, to {p1:.2f}, but gold, the "
                       f"thing it was meant to measure, ends lower: {g1:.2f} against {g0:.2f}. The policy has found "
                       "what the reward model overrates.")
        elif g1 > g0 + 0.05:
            verdict = (f"Here the looser leash pays: gold ends at {g1:.2f} against {g0:.2f}, and the divergence is "
                       f"larger, {k1:.1f} nats against {k0:.1f}.")
        else:
            verdict = (f"Gold ends about the same either way, {g0:.2f} and {g1:.2f}; the loose leash spends "
                       f"{k1:.1f} nats of divergence to get there, against {k0:.1f}.")
        samp = d[keys[1] + "_samples"][-1]
        with self.voiceover(
            "Now for real. Starting from our fine-tuned model, generate sixteen lines a step, score them with the "
            "reward model, subtract the KL penalty, and take a policy-gradient step. <bookmark mark='a'/> With beta "
            f"{betas[0]:g}, the reward model's score rises from {early(H[0], 1):.2f} to {p0:.2f}, and gold, which "
            f"the training never sees, goes from {gs:.2f} to {g0:.2f}. <bookmark mark='b'/> Now loosen the leash "
            f"to beta {betas[1]:g}. " + verdict
        ) as vo:
            self.play(FadeIn(lg), FadeIn(tag), FadeIn(panels[0][0]))
            vo.wait_until("a")
            self.play(Create(panels[0][1]), Create(panels[0][2]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(panels[1][0]))
            self.play(Create(panels[1][1]), Create(panels[1][2]), run_time=2.5)
        self.wait(0.3)
        lines = VGroup(*[said(t_, chars=46, font_size=18, max_lines=2) for t_ in samp[2][:3]])
        lines.arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"And here is what the loosely leashed policy writes about the {samp[1]} at the end of training. "
            "Judge for yourself whether a person would prefer it."
        ):
            self.play(panels.animate.shift(UP * 0.8).scale(0.85), FadeOut(tag))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in lines], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()
