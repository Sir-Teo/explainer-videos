from __future__ import annotations

from itertools import combinations
from math import comb

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import Plot, label, load, mtex, pct_fmt, real_tag, source, why


class Sharpening(VoiceoverScene):
    def construct(self):
        self.passk_def()
        self.curves()
        self.support()
        self.how_much()
        self.distill()

    # ------------------------------------------------------------------
    def passk_def(self):
        n, c, k = 8, 3, 3
        cols = [C.REWARD] * c + [C.PENALTY] * (n - c)
        dots = VGroup(*[Circle(radius=0.22, color=col, fill_opacity=0.8, stroke_width=2) for col in cols]).arrange(RIGHT, buff=0.25)
        dots.move_to(UP * 1.8)
        dl = label(rf"$n = {n}$ samples, $c = {c}$ correct", font_size=26, color=GREY_A).next_to(dots, UP, buff=0.25)
        f1 = mtex(r"\text{pass@}k", r"=", r"P(\text{at least one of } k \text{ samples is right})", r"=", r"1 - (1 - p)^k", font_size=36)
        f1[4].set_color(C.REWARD)
        f1.move_to(UP * 0.4)
        f2 = mtex(r"\widehat{\text{pass@}k}", r"=", r"1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}", font_size=40)
        f2[2].set_color(YELLOW)
        f2.next_to(f1, DOWN, buff=0.5)
        w = why(r"the fraction of the $\binom{n}{k}$ ways to pick $k$ samples that contain no right answer").next_to(f2, DOWN, buff=0.2)
        subs = list(combinations(range(n), k))
        bad = [s for s in subs if all(i >= c for i in s)]
        assert len(bad) == comb(n - c, k)
        ex = VGroup()
        for s in bad[:4]:
            g = VGroup(*[Circle(radius=0.12, color=C.PENALTY, fill_opacity=0.8, stroke_width=1.5) for _ in s]).arrange(RIGHT, buff=0.08)
            ex.add(g)
        ex.add(label(rf"\dots\ ({comb(n - c, k)} such picks in all)", font_size=24, color=GREY_A))
        ex.arrange(RIGHT, buff=0.5).next_to(w, DOWN, buff=0.7)
        val = label(rf"$1 - \binom{{5}}{{3}}/\binom{{8}}{{3}} = 1 - {comb(n - c, k)}/{comb(n, k)} = {1 - comb(n - c, k) / comb(n, k):.3f}$",
                    font_size=28, color=YELLOW).next_to(ex, DOWN, buff=0.2)
        src = source(r"Chen et al., \emph{Evaluating Large Language Models Trained on Code} (Codex), 2021")
        with self.voiceover(
            "Does reinforcement learning teach a model new things, or just make it more reliable at things it could "
            "already do? To ask that precisely, we need pass at k: the chance that at least one of k attempts is "
            "right. <bookmark mark='e'/> With a success rate p, it's one minus the chance that all k fail. "
            "<bookmark mark='u'/> To estimate it, draw n samples, count the right ones, and ask: of all the ways to "
            "pick k of them, what fraction contain no right answer at all? <bookmark mark='x'/> Here, ten of the "
            "fifty-six ways fail, so pass at three is about point eight two."
        ) as vo:
            self.play(FadeIn(dots, lag_ratio=0.1), FadeIn(dl), FadeIn(src))
            self.play(Write(f1))
            vo.wait_until("e")
            self.play(Indicate(f1[4]))
            vo.wait_until("u")
            self.play(Write(f2), FadeIn(w))
            vo.wait_until("x")
            self.play(FadeIn(ex, lag_ratio=0.2), FadeIn(val))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("passk")
        ks = np.array(d["ks"], float)
        plot = Plot(x_range=(1, ks[-1]), y_range=(0.6, 1.0), width=8.0, height=4.2, log_x=True,
                    x_ticks=[int(k) for k in ks], x_fmt=lambda v: MathTex(str(int(v)), font_size=22, color=GREY_A),
                    y_ticks=[0.6, 0.8, 1.0], y_fmt=pct_fmt, x_label=r"$k$ (attempts)", y_label=r"pass@$k$ on held-out problems")
        plot.move_to(LEFT * 1.2 + DOWN * 0.4)
        spec = [("base", r"before RL", C.REFERENCE), ("mid", rf"after {d['mid']['step']} steps", C.OLD_POLICY),
                ("final", rf"after {d['final']['step']} steps", C.RL_POLICY)]
        lines, keys = VGroup(), VGroup()
        for name, txt, col in spec:
            y = np.clip(np.array(d[name]["curve"]), 0.6, 1.0)
            lines.add(VGroup(plot.line(ks, y, color=col, stroke_width=4), plot.dots(ks, y, col, radius=0.05)))
            keys.add(VGroup(Line(ORIGIN, RIGHT * 0.4, color=col, stroke_width=5), label(txt, font_size=24)).arrange(RIGHT, buff=0.15))
        keys.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(plot, RIGHT, buff=0.3).shift(UP * 0.6)
        b1, f1 = d["base"]["curve"][0], d["final"]["curve"][0]
        bK = d["base"]["curve"][-1]
        head = label(rf"The adder: pass@$k$ from {d['n']} samples per problem, {d['problems']} problems", font_size=28).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Here is pass at k for our adder, measured with {d['n']} samples on each of {d['problems']} held-out "
            f"problems. <bookmark mark='b'/> Before RL, a single attempt is right {b1 * 100:.0f} percent of the "
            f"time, but with {int(ks[-1])} attempts, "
            + ("every one of the problems" if bK >= 1.0 else f"{bK * 100:.1f} percent of problems") + " gets solved at least once. "
            f"<bookmark mark='f'/> After RL, a single attempt is right {f1 * 100:.0f} percent of the time. The "
            "curve went flat: RL moved the probability onto answers the model could already produce. Its mistakes "
            "were slips, and the right answer was always within reach."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(real_tag()))
            vo.wait_until("b")
            self.play(Create(lines[0]), FadeIn(keys[0]))
            vo.wait_until("f")
            self.play(Create(lines[1]), FadeIn(keys[1]))
            self.play(Create(lines[2]), FadeIn(keys[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def support(self):
        f = mtex(r"\pi^\star(y)", r"\propto", r"\pi_{\text{ref}}(y)", r"\,e^{r(y)/\beta}", font_size=48).move_to(UP * 1.8)
        f[0].set_color(YELLOW)
        f[2].set_color(C.REFERENCE)
        f[3].set_color(C.REWARD)
        z = mtex(r"\pi_{\text{ref}}(y) = 0", r"\;\Rightarrow\;", r"\pi^\star(y) = 0", font_size=40).next_to(f, DOWN, buff=0.5)
        z[2].set_color(YELLOW)
        n = label(r"the optimum reweights; it never invents", font_size=28, color=GREY_A).next_to(z, DOWN, buff=0.2)
        debate = VGroup(
            label(r"Yue et al.\ (2025): base models catch up and pass RL models at large $k$ (NeurIPS 2025 runner-up)", font_size=24),
            label(r"ProRL, NVIDIA (2025): with long, reset-anchored RL, problems the base never solves get solved", font_size=24),
            label(r"2026: still argued, e.g.\ ``two-stage'' dynamics, pass@$k$ collapse from over-training", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "This matches the math. The KL-regularized optimum is the reference times a positive factor, so any "
            "answer the reference would never produce stays at probability zero. <bookmark mark='y'/> In 2025, a "
            "careful study found the same thing in large reasoning models: given enough attempts, the base model "
            "catches up with, and even passes, the RL-trained one. <bookmark mark='p'/> NVIDIA's ProRL pushed back, "
            "finding problems that only prolonged RL could solve; and in practice, generalization lets a network "
            "reach answers it never sampled. <bookmark mark='o'/> As of 2026, the question is still open."
        ) as vo:
            self.play(Write(f))
            self.play(FadeIn(z), FadeIn(n))
            vo.wait_until("y")
            self.play(FadeIn(debate[0]))
            vo.wait_until("p")
            self.play(FadeIn(debate[1]))
            vo.wait_until("o")
            self.play(FadeIn(debate[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def how_much(self):
        rows = VGroup(
            VGroup(label(r"bits per episode", font_size=30, color=C.ADVANTAGE),
                   label(r"a policy gradient carries $O(1)$ bits per attempt; DeepSeek-R1-Zero: $\sim$5.3 million episodes $\approx$ 5.3 million bits,", font_size=24),
                   label(r"less than a rank-1 LoRA adapter on an 8B model (3 million parameters)", font_size=24, color=GREY_A)),
            VGroup(label(r"which weights move", font_size=30, color=C.RL_POLICY),
                   label(r"68.5--96\% of parameters are unchanged after RL; the updates are sparse but nearly full-rank", font_size=24)),
            VGroup(label(r"RL's razor", font_size=30, color=C.KL),
                   label(r"forgetting tracks the KL from the base model, and on-policy RL finds low-KL solutions", font_size=24)),
        )
        for r in rows:
            r.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(DOWN * 0.1)
        head = label(r"How much does RL actually change a model?", font_size=32).to_edge(UP, buff=0.4)
        src = source(r"Schulman, \emph{LoRA Without Regret} (2025); Mukherjee et al., arXiv 2505.11711; Shenfeld et al., arXiv 2509.04259")
        with self.voiceover(
            "Other measurements point the same way. <bookmark mark='b'/> A reward of zero or one carries about one "
            "bit of information per attempt, so even DeepSeek's R1-Zero received only a few million bits, fewer "
            "than the parameters of a tiny adapter. <bookmark mark='w'/> Most weights don't change at all. "
            "<bookmark mark='r'/> And on-policy RL tends to find the solution closest to the starting model, which "
            "is why it forgets less than fine-tuning on someone else's answers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for k, mark in enumerate(["b", "w", "r"]):
                vo.wait_until(mark)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def distill(self):
        f = mtex(r"r_t", r"=", r"-\Big(\log \pi_\theta(y_t \mid s_t)", r"-", r"\log \pi_{\text{teacher}}(y_t \mid s_t)\Big)", font_size=42)
        f[0].set_color(C.REWARD)
        f.to_edge(UP, buff=0.6)
        n = label(r"sample from the student; a teacher grades \emph{every token}: a per-token reverse KL", font_size=26, color=GREY_A)
        n.next_to(f, DOWN, buff=0.2)
        bars = VGroup(
            VGroup(label(r"RL", font_size=26), Rectangle(width=17920 / 3400, height=0.5, stroke_width=0, fill_color=C.RL_POLICY, fill_opacity=0.85),
                   label(r"17{,}920 GPU-hours \ \ $\to$ 67.6\%", font_size=24)),
            VGroup(label(r"on-policy distillation", font_size=26), Rectangle(width=1800 / 3400, height=0.5, stroke_width=0, fill_color=C.REWARD, fill_opacity=0.85),
                   label(r"1{,}800 GPU-hours \ \ $\to$ 74.4\%", font_size=24)),
        )
        for r in bars:
            r[1].move_to([-3.0, 0, 0], aligned_edge=LEFT)
            r[0].next_to(r[1], LEFT, buff=0.3)
            r[2].next_to(r[1], RIGHT, buff=0.2)
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.4)
        for r in bars:
            r[1].align_to(np.array([-3.0, 0, 0]), LEFT)
            r[0].next_to(r[1], LEFT, buff=0.3)
            r[2].next_to(r[1], RIGHT, buff=0.2)
        bl = label(r"Qwen3-8B: compute spent (bars) and AIME 2024 score, as reported in the Qwen3 technical report", font_size=24, color=GREY_A).next_to(bars, UP, buff=0.3)
        foot = label(r"DeepSeek-V4 (Apr 2026): its final RL stage replaced by on-policy distillation from specialist teachers",
                     font_size=24, color=YELLOW).to_edge(DOWN, buff=0.6)
        src = source(r"Lu \& Thinking Machines, \emph{On-Policy Distillation} (2025); Qwen3 report, Table 21; DeepSeek-V4 report")
        with self.voiceover(
            "If one bit per attempt is the bottleneck, there's a fix when a stronger model exists. Sample from the "
            "student, as in RL, but let a teacher grade every token: the reward for each token is how much more "
            "likely the teacher finds it. That's on-policy distillation, the same log-derivative trick with a dense "
            "reward. <bookmark mark='q'/> For Qwen3's eight-billion-parameter model it beat RL on the AIME benchmark "
            "for a tenth of the compute. <bookmark mark='d'/> And in April 2026, DeepSeek's V4 replaced its final RL "
            "stage with exactly this, distilling from specialist teachers that had each been trained with GRPO."
        ) as vo:
            self.play(Write(f), FadeIn(n), FadeIn(src))
            vo.wait_until("q")
            self.play(FadeIn(bl), FadeIn(bars, lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
