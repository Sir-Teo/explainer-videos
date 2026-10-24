from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import (GOLD, KLC, PART, POLICY, PROXY, REF, REWARD, load, node_box, rlhf_gains, said,
                                   ticks)
from videos.ai.ai27.compute import TOPICS
from videos.ai.ai27.compute import gold as gold_of


class RLHF(VoiceoverScene):
    def construct(self):
        self.card()
        self.objective()
        self.optimum()
        self.bars()
        self.tokens()
        self.baselines()
        self.measure()
        self.runs()

    def card(self):
        card = chapter_card(6, r"Reinforcement learning on a leash", r"Why not just maximize the reward?",
                            lit=(2022,), part=PART)
        with self.voiceover("Chapter six. Reinforcement learning on a leash."):
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
        tag = note(rf"computed: \ eight lines our fine-tuned model wrote about the {d['topic']}, \ of comparable "
                   r"probability under it; \ $\pi_{\mathrm{ref}}$ renormalized over them").to_corner(DR, buff=0.2)
        half = k // 2  # the better half of the answers, by reward
        move10 = 0.5 * float(np.abs(pis[0] - ref).sum())  # total variation: the share of probability that moves
        hi_ref, hi_1 = float(ref[half:].sum()), float(pis[1][half:].sum())
        best = float(pis[-1][-1])
        if move10 < 0.15:
            s10 = f"With beta {betas[0]:g}, the leash is tight: only {100 * move10:.0f} percent of the probability moves."
        else:
            s10 = (f"Even with beta {betas[0]:g}, {100 * move10:.0f} percent of the probability moves: these rewards "
                   "are large next to that leash.")
        s1 = (f"At beta {betas[1]:g}, the better half of the answers goes from {100 * hi_ref:.0f} to "
              f"{100 * hi_1:.0f} percent of the probability.")
        if best > 0.8:
            s01 = f"At beta {betas[-1]:g}, nearly all of it sits on the best answer: {100 * best:.0f} percent."
        elif int(np.argmax(pis[-1])) == k - 1:
            s01 = f"At beta {betas[-1]:g}, the best answer holds {100 * best:.0f} percent, more than any other."
        else:
            s01 = (f"Even at beta {betas[-1]:g}, the best answer holds only {100 * best:.0f} percent: the reference "
                   "model's own preference outweighs a reward gap that small.")
        with self.voiceover(
            f"Here's the formula on eight real answers our fine-tuned model wrote about the {d['topic']}, chosen to "
            "be about equally likely under it, and sorted by their reward. The bars start as the reference model's "
            f"probabilities, renormalized over these eight. <bookmark mark='a'/> {s10} <bookmark mark='b'/> {s1} "
            f"<bookmark mark='c'/> {s01} That is what reinforcement learning with a KL penalty is aiming at, though "
            "it has to get there by sampling, one gradient step at a time."
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
    def tokens(self):
        rows = [
            cmath(r"s_t", r"=", r"(x,\ y_1 \dots y_{t-1}),\qquad a_t = y_t", font_size=34),
            cmath(r"r_t", r"=", r"-\beta \log \frac{\pi_\theta(y_t \mid s_t)}{\pi_{\mathrm{ref}}(y_t \mid s_t)}",
                  r"\ +\ ", r"[\,t = T\,]\ r_\phi(x, y)", font_size=34),
            cmath(r"\textstyle\sum_t r_t", r"=", r"r_\phi(x, y) - \beta \log \frac{\pi_\theta(y \mid x)}"
                  r"{\pi_{\mathrm{ref}}(y \mid x)}", font_size=34),
        ]
        rows[1][2].set_color(KLC)
        rows[1][4].set_color(PROXY)
        whys = [why(r"an answer is an episode: \ the prompt and the tokens so far, \ then the next token"),
                why(r"a KL penalty at every token, \ the reward model's score at the end"),
                why(r"summed over the answer: \ one sample of the objective")]
        step = ladder(self, rows, whys, keep=3, top=3.3, x=-2.6, buff=0.42, edge=6.9)
        nets = VGroup(
            node_box(r"policy $\pi_\theta$: \ trained", POLICY, font_size=22),
            node_box(r"value model $V_\psi$: \ trained", C.BASELINE, font_size=22),
            node_box(r"reference $\pi_{\mathrm{ref}}$: \ frozen", REF, font_size=22),
            node_box(r"reward model $r_\phi$: \ frozen", PROXY, font_size=22),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.4, 0.3)).move_to([-3.0, -2.25, 0])
        hc = history_card(2022, r"InstructGPT's PPO", r"a per-token KL penalty from the fine-tuned model; \ a "
                          r"$6$-billion-parameter reward model, \ and a value model of the same size that starts as "
                          r"a copy of it", width=5.6, color=PROXY).move_to([3.7, -2.15, 0])
        cite_ = cite(r"Ouyang et al.\ (2022); \ Ahmadian et al.\ (2024)", font_size=18)
        with self.voiceover(
            "How does Part 26's PPO fit a language model? Treat each answer as an episode: "
            "the state is the prompt and the tokens written so far, and the action is the next token. "
            "<bookmark mark='b'/> InstructGPT's reward gives every token a penalty, beta times that token's "
            "log-ratio of policy to reference, and adds the reward model's score at the last token. "
            "<bookmark mark='c'/> Summed over the answer, that is one sample of the objective we started with: the "
            "score, minus beta times the log-ratio of the whole answer. <bookmark mark='d'/> Then PPO runs as in "
            "Part 26, with a value network to judge each partial answer, and advantages computed token by token. "
            "That makes four networks the size of a language model in memory at once: the policy and the value "
            "network, training; the reference and the reward model, frozen. <bookmark mark='e'/> InstructGPT's "
            "value network started as a copy of its six-billion-parameter reward model."
        ) as vo:
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(n_, shift=UP * 0.1) for n_ in nets], lag_ratio=0.3), FadeIn(cite_),
                      run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(hc, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def baselines(self):
        n = int(load("baselines")["n"])
        rows = [
            cmath(r"\hat A_i", r"=", r"R_i - b", font_size=38),
            cmath(r"b", r"=", r"V_\psi(s_t)", font_size=38),
            cmath(r"b_i", r"=", r"\frac{1}{k-1} \sum_{j \ne i} R_j", font_size=38),
            cmath(r"\hat A_i", r"=", r"\frac{R_i - \operatorname{mean}(R)}{\operatorname{std}(R)}", font_size=38),
        ]
        rows[1][2].set_color(C.BASELINE)
        rows[2][2].set_color(POLICY)
        rows[3][2].set_color(POLICY)
        whys = [why(r"the advantage, \ Part 26: \ a baseline removes noise, \ not signal"),
                why(r"PPO: \ a value network predicts it, \ token by token"),
                why(r"RLOO (Ahmadian et al., 2024): \ the other answers to the same question"),
                why(r"GRPO (Shao et al., 2024): \ the group's mean and spread, \ no value network; \ Part 28")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-3.2, buff=0.45, edge=6.9)
        ours = label(rf"our runs: \ $k = {n}$ lines to one question, \ $b = $ their mean $= $ RLOO's "
                     rf"$\times\, {n - 1}/{n}$", font_size=26, color=POLICY).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The value network is there to supply a baseline. <bookmark mark='a'/> As in Part 26, subtracting a "
            "baseline from the reward leaves the gradient's average alone and removes noise. "
            "<bookmark mark='b'/> PPO learns its baseline: the value network, token by token. "
            "<bookmark mark='c'/> But a language model can simply answer the same question several times. In 2024 "
            "Cohere's RLOO used the average reward of the other answers as each one's baseline, and reported better "
            "results than PPO, with no value network. <bookmark mark='d'/> The same year DeepSeek's GRPO also "
            "divided by the group's spread; it trained DeepSeek-R1, and Part 28 derives it. "
            f"<bookmark mark='e'/> Our runs do the simplest version: {n:d} lines to one question, and the baseline "
            f"is their mean, which is RLOO's baseline scaled by {n - 1:d} over {n:d}."
        ) as vo:
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeIn(ours, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        d = load("baselines")
        kinds = list(d["kinds"])
        cos = {k: float(d[f"{k}_cos"]) for k in kinds}
        by_q = {k: np.asarray(d[f"{k}_cos_by_q"]) for k in kinds}
        qm = np.asarray(d["question_mean"])
        n, B, Q = int(d["n"]), int(d["batches"]), len(d["topics"])
        names = {"none": r"no baseline", "shared": r"one for every \\ question",
                 "value": r"each question's \\ own average", "group": r"the batch's \\ own mean (ours)"}
        cols = {"none": GREY_B, "shared": REF, "value": C.BASELINE, "group": POLICY}
        top = max(float(max(v.max() for v in by_q.values())), 0.1)
        g = axes([0, len(kinds)], [0, top * 1.15], x_length=6.6, y_length=3.8,
                 ylabel=r"cosine between two batches' gradients", yticks=ticks(0, top * 1.1, 3),
                 center=[-2.8, -0.2, 0])
        ax = g.ax
        bars, whisk, labs, vals = VGroup(), VGroup(), VGroup(), VGroup()
        for j, k in enumerate(kinds):
            x = j + 0.5
            b0, b1 = ax.c2p(x, 0), ax.c2p(x, cos[k])
            bars.add(Rectangle(width=0.9, height=max(b1[1] - b0[1], 0.01), stroke_width=0, fill_color=cols[k],
                               fill_opacity=0.85).move_to((b0 + b1) / 2))
            whisk.add(Line(ax.c2p(x, by_q[k].min()), ax.c2p(x, by_q[k].max()), color=WHITE, stroke_width=2))
            labs.add(label(names[k], font_size=18, color=cols[k]).next_to(ax.c2p(x, 0), DOWN, buff=0.15))
            vals.add(MathTex(rf"{cos[k]:.2f}", font_size=24, color=cols[k]).next_to(whisk[-1], UP, buff=0.1))
        # each question's average score: the shift the reward model never pinned down
        nl = NumberLine(x_range=[float(np.floor(qm.min())), float(np.ceil(qm.max())), 1], length=4.6,
                        color=GREY_C, include_numbers=True, font_size=20).move_to([4.2, -1.3, 0])
        qd = VGroup(*[Dot(nl.n2p(v), radius=0.07, color=PROXY) for v in qm])
        ql = label(rf"the reward model's average score \\ on each of the ${Q:d}$ questions", font_size=20,
                   color=PROXY).next_to(nl, UP, buff=0.45)
        tag = note(rf"computed: \ the first step of training, \ ${B:d}$ batches of ${n:d}$ lines for each of ${Q:d}$ "
                   r"questions; \ whiskers: \ lowest to highest question", font_size=18).to_corner(DR, buff=0.2)
        if cos["group"] >= 0.75 * cos["value"] and cos["group"] > 1.5 * cos["none"]:
            verdict = ("The batch's own mean does nearly as well as knowing each question's true average, and it "
                       "costs nothing: there is no value network to train. That is the reasoning behind RLOO, GRPO "
                       "and our runs.")
        elif cos["group"] > 1.5 * cos["none"]:
            verdict = ("The batch's own mean is noisier than the question's true average, since it comes from only "
                       f"{n:d} lines, but it is far better than no baseline at all.")
        else:
            verdict = (f"On our model the baseline makes little difference: the noise of sampling {n:d} lines swamps "
                       "it.")
        if max(cos.values()) < 0.5:
            compass = ("Even the best is far from one: a single batch is a noisy compass, which is why reinforcement "
                       "learning takes many small steps.")
        else:
            compass = "With a good baseline, a single batch already points most of the way."
        with self.voiceover(
            "How much does the baseline matter on our model? At the first step of training we draw "
            f"{B:d} batches of {n:d} lines for each of {Q:d} questions, and estimate the gradient from each batch "
            "four ways. If an estimate is any good, two batches for the same question should point the same way. "
            f"<bookmark mark='a'/> With no baseline, two batches agree with a cosine of {cos['none']:.2f}. "
            f"<bookmark mark='b'/> With one baseline shared by every question, {cos['shared']:.2f}. The reward "
            f"model's average score differs from question to question, from {qm.min():+.1f} to {qm.max():+.1f}, "
            "because only differences within a question were ever learned. <bookmark mark='c'/> With each "
            f"question's own average, what a value network would learn to predict, {cos['value']:.2f}. "
            f"<bookmark mark='d'/> And with the batch's own mean, as in our runs, {cos['group']:.2f}. {verdict} "
            f"<bookmark mark='e'/> {compass}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), FadeIn(tag))
            for j, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(GrowFromEdge(bars[j], DOWN), Create(whisk[j]), FadeIn(vals[j]))
                if j == 1:
                    self.play(FadeIn(nl), FadeIn(ql), LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in qd],
                                                                  lag_ratio=0.15))
            vo.wait_until("e")
            self.play(Indicate(bars[-1], color=POLICY))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def runs(self):
        d = load("rlhf")
        ins = load("inside")
        slope = float(ins["large_slope"])
        rm0, gold0 = float(np.mean(ins["large_score"])), float(np.mean(ins["gold"]))
        W = len(TOPICS)  # the runs take the questions in turn: a window of W steps holds each once
        betas = list(d["betas"])
        keys = [f"b{b:g}".replace(".", "_") for b in betas]
        H = [np.asarray(d[k]) for k in keys]
        S = int(H[0][-1, 0])
        G = {k: [rlhf_gains(r_, slope, rm0, gold0, W) for r_ in np.asarray(d[k + "_seeds"])] for k in keys}
        M = {k: rlhf_gains(h, slope, rm0, gold0, W) for k, h in zip(keys, H)}
        allv = np.concatenate([np.r_[x[1], x[2]] for k in keys for x in G[k]] + [[0.0]])
        lo, hi = float(allv.min()), float(allv.max())
        pad = 0.1 * (hi - lo)
        panels = VGroup()
        for i, (b, k) in enumerate(zip(betas, keys)):
            g = axes([0, S], [lo - pad, hi + pad], x_length=5.4, y_length=3.0,
                     xlabel=r"steps of reinforcement learning", ylabel=rf"$\beta = {b:g}$: \ gain over the fine-tuned "
                     r"model", xticks=[0, S], yticks=ticks(lo, hi, 3), yfmt=lambda v: rf"{v:+.2f}" if v else "0",
                     center=[-3.3 + 6.6 * i, 0.3, 0])
            x, pr, gd = M[k]
            pc, gc = curve(g.ax, x, pr, PROXY, 4), curve(g.ax, x, gd, GOLD, 4)
            zero = DashedLine(g.ax.c2p(0, 0), g.ax.c2p(S, 0), color=GREY_D, dash_length=0.05)
            bands = VGroup(*[band(g.ax, x, np.min([s_[c] for s_ in G[k]], 0), np.max([s_[c] for s_ in G[k]], 0),
                                  col, opacity=0.2) for c, col in ((1, PROXY), (2, GOLD))])
            panels.add(VGroup(g, pc, gc, bands, zero))
        lg = legend([(PROXY, r"what the reward model believes, \ in gold's units"),
                     (GOLD, r"what gold says")], font_size=20).to_edge(UP, buff=0.3)
        tag = note(rf"computed: \ $16$ lines a step; \ means over {W} steps (every question once); \ mean of "
                   rf"{d['seeds']} runs, \ band: \ lowest to highest; \ reward model divided by its slope on gold, "
                   rf"${slope:.1f}$", font_size=18)
        tag.to_corner(DR, buff=0.2)
        (p0, g0), (p1, g1) = [(float(M[k][1][-1]), float(M[k][2][-1])) for k in keys]
        k0, k1 = [float(np.mean(h[-W:, 3])) for h in H]
        if g1 < g0 - 0.03 and p1 > p0:
            verdict = (f"With the loose leash the reward model believes it gained more, {p1:+.2f}, but gold, the "
                       f"thing it was meant to measure, gained less: {g1:+.2f} against {g0:+.2f}. The policy has "
                       "found what the reward model overrates.")
        elif g1 > g0 + 0.03:
            verdict = (f"Here the looser leash pays: gold gains {g1:+.2f} against {g0:+.2f}, and the divergence is "
                       f"larger, {k1:.1f} nats against {k0:.1f}.")
        else:
            verdict = (f"Gold gains about the same either way, {g0:+.2f} and {g1:+.2f}; the loose leash spends "
                       f"{k1:.1f} nats of divergence to get there, against {k0:.1f}.")
        if p0 > g0 + 0.05 and float(ins["large_pick_believed"]) > float(ins["large_pick_gold"]) + 0.02:
            gap = (f"The reward model already believes in more than gold delivers: {p0:+.2f} against {g0:+.2f}, as "
                   "it did for its favourites in chapter five.")
        elif p0 > g0 + 0.05:
            gap = f"The reward model already believes in more than gold delivers: {p0:+.2f} against {g0:+.2f}."
        else:
            gap = f"Here the reward model's belief and gold roughly agree: {p0:+.2f} and {g0:+.2f}."
        samp = d[keys[1] + "_samples"][-1]
        with self.voiceover(
            "Now for real. Starting from our fine-tuned model, generate sixteen lines a step, score them with the "
            "reward model, subtract the KL penalty, and take a policy-gradient step. Both curves are in gold's "
            "units: the reward model's score divided by its slope from chapter five. <bookmark mark='a'/> With beta "
            f"{betas[0]:g}, by the last {W} steps the reward model believes the policy has gained {p0:+.2f} over the "
            f"fine-tuned model, and gold, which the training never sees, says {g0:+.2f}. {gap} "
            f"<bookmark mark='b'/> Now loosen the leash to beta {betas[1]:g}. " + verdict
        ) as vo:
            self.play(FadeIn(lg), FadeIn(tag), FadeIn(panels[0][0]), Create(panels[0][4]))
            vo.wait_until("a")
            self.play(FadeIn(panels[0][3]), Create(panels[0][1]), Create(panels[0][2]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(panels[1][0]), Create(panels[1][4]))
            self.play(FadeIn(panels[1][3]), Create(panels[1][1]), Create(panels[1][2]), run_time=2.5)
        self.wait(0.3)
        # the loose-leash run replayed: a scrubber on its curves, three of its lines at each snapshot
        snaps = d[keys[1] + "_samples"]
        g1 = panels[1][0]

        def frame_at(k):
            st, tp, texts = snaps[k]
            head = VGroup(label(rf"step ${st}$", font_size=24, color=POLICY),
                          said(f"Write a line about the {tp}.", "user", chars=40, font_size=18)).arrange(RIGHT, buff=0.4)
            ls = VGroup(*[VGroup(said(t_, chars=46, font_size=18, max_lines=2),
                                 label(rf"gold ${gold_of(t_):+.2f}$", font_size=20, color=GOLD)).arrange(RIGHT, buff=0.3)
                          for t_ in texts[:3]]).arrange(DOWN, buff=0.15)
            return VGroup(head, ls).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.3)

        with self.voiceover(
            "Here is the loose-leash run replayed: three of its sixteen lines at each stage of training. "
            "<bookmark mark='a'/> At the start it writes like the fine-tuned model it began as. "
            f"<bookmark mark='b'/> By step {samp[0]}, asked about the {samp[1]}, this is what it has learned to "
            "write, with gold's score beside each line. Judge for yourself whether a person would prefer it."
        ) as vo:
            self.play(panels.animate.scale(0.75).to_edge(UP, buff=0.35), FadeOut(tag), FadeOut(lg))
            ax1 = g1.ax
            y0, y1 = ax1.y_range[0], ax1.y_range[1]
            mark = DashedLine(ax1.c2p(snaps[0][0], y0), ax1.c2p(snaps[0][0], y1), color=POLICY, dash_length=0.06)
            cur = frame_at(0)
            self.play(Create(mark), FadeIn(cur, shift=UP * 0.1))
            vo.wait_until("a")
            for k in range(1, len(snaps)):
                nxt = frame_at(k)
                t_ = snaps[k][0]
                self.play(mark.animate.put_start_and_end_on(ax1.c2p(t_, y0), ax1.c2p(t_, y1)),
                          FadeOut(cur, shift=UP * 0.1), FadeIn(nxt, shift=UP * 0.1), run_time=1.0)
                cur = nxt
                if k < len(snaps) - 1:
                    self.wait(1.2)
            vo.wait_until("b")
        self.wait(0.5)
        self.clear_scene()
