from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import Plot, label, mtex, real_tag, smooth, source
from videos.rl.compute import load_run


class Biases(VoiceoverScene):
    def construct(self):
        self.weights()
        self.fixes()
        self.lengths()
        self.disagree()

    # ------------------------------------------------------------------
    def weights(self):
        f = mtex(r"\frac{1}{G}\sum_{i}", r"\frac{1}{|o_i|}", r"\sum_{t}", r"\hat A_i\, \nabla \log \pi_\theta(o_{i,t})", font_size=42)
        f[1].set_color(C.LENGTH)
        f[3][:2].set_color(C.ADVANTAGE)
        f.to_edge(UP, buff=0.3)
        n = label(r"each token's push is $\hat A_i / |o_i|$", font_size=28, color=C.LENGTH).next_to(f, DOWN, buff=0.15)
        cases = [("right, short", 6, +1.0), ("right, long", 13, +1.0), ("wrong, short", 6, -1.0), ("wrong, long", 13, -1.0)]
        rows = VGroup()
        for name, L, A in cases:
            w = A / L
            nm = label(name, font_size=26, color=C.REWARD if A > 0 else C.PENALTY)
            cells = VGroup(*[Rectangle(width=0.36, height=0.36, stroke_color=GREY_D, stroke_width=1, fill_color=GREY_E, fill_opacity=0.6)
                             for _ in range(L)]).arrange(RIGHT, buff=0.04)
            bars = VGroup(*[Rectangle(width=0.26, height=abs(w) * 4.0, stroke_width=0, fill_color=C.REWARD if A > 0 else C.PENALTY,
                                      fill_opacity=0.9) for _ in range(L)])
            for b, c in zip(bars, cells):
                b.next_to(c, UP if A > 0 else DOWN, buff=0.05)
            val = MathTex(rf"{w:+.3f}" + r"\ \text{per token}", font_size=26, color=C.REWARD if A > 0 else C.PENALTY)
            rows.add(VGroup(nm, cells, bars, val))
        for i, row in enumerate(rows):
            y = [0.85, -0.15, -1.0, -2.25][i]
            row[0].move_to([-5.2, y, 0], aligned_edge=LEFT)
            row[1].move_to([-3.0, y, 0], aligned_edge=LEFT)
            for b, c in zip(row[2], row[1]):
                b.next_to(c, UP if cases[i][2] > 0 else DOWN, buff=0.05)
            row[3].next_to(row[1], RIGHT, buff=0.4)
            row[3].set_x(4.6)
        res = VGroup(label(r"right: shorter answers are rewarded more per token", font_size=26, color=C.REWARD),
                     label(r"wrong: longer answers are punished less per token", font_size=26, color=C.PENALTY)
                     ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Here's the trap. GRPO averages over an answer's tokens before averaging over the group, so each token's "
            "push is the advantage divided by the answer's length. <bookmark mark='r'/> Two right answers, one short "
            "and one long: the short one's tokens get pushed up twice as hard. <bookmark mark='w'/> Two wrong answers: "
            "the long one's tokens are punished half as much. <bookmark mark='c'/> So when the model is right, it "
            "learns to be brief, and when it's wrong, it learns that rambling dilutes the blame. Long, wrong answers "
            "are the result."
        ) as vo:
            self.play(Write(f), FadeIn(n))
            vo.wait_until("r")
            for k in (0, 1):
                self.play(FadeIn(rows[k][0]), FadeIn(rows[k][1]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in rows[k][2]], lag_ratio=0.03),
                          FadeIn(rows[k][3]), run_time=0.9)
            vo.wait_until("w")
            for k in (2, 3):
                self.play(FadeIn(rows[k][0]), FadeIn(rows[k][1]), LaggedStart(*[GrowFromEdge(b, UP) for b in rows[k][2]], lag_ratio=0.03),
                          FadeIn(rows[k][3]), run_time=0.9)
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fixes(self):
        rows = [
            (r"GRPO (2024)", r"\frac{1}{G}\sum_i \frac{1}{|o_i|}\sum_t \ell_{i,t}", r"per answer, then per group: length bias", C.LENGTH),
            (r"DAPO (2025)", r"\frac{1}{\sum_i |o_i|}\sum_i \sum_t \ell_{i,t}", r"every token in the batch counts the same", C.ADVANTAGE),
            (r"Dr.\ GRPO (2025)", r"\frac{1}{G\, L_{\max}}\sum_i \sum_t \ell_{i,t}", r"a constant: no length bias, no std division", C.BASELINE),
        ]
        g = VGroup()
        for name, tex, note_, col in rows:
            g.add(VGroup(label(name, font_size=30, color=col), mtex(tex, font_size=36), label(note_, font_size=24, color=GREY_A)))
        for i, row in enumerate(g):
            y = 1.6 - i * 1.6
            row[0].move_to([-4.8, y, 0])
            row[1].move_to([-0.6, y, 0])
            row[2].move_to([4.2, y, 0])
        head = label(r"Three ways to average a loss over tokens", font_size=32).to_edge(UP, buff=0.4)
        src = source(r"Yu et al.\ arXiv 2503.14476; Liu et al., \emph{Understanding R1-Zero-Like Training}, arXiv 2503.20783")
        with self.voiceover(
            "Two 2025 papers removed the bias in different ways. <bookmark mark='d'/> ByteDance's DAPO averages over "
            "all tokens in the batch at once, so every token counts equally. <bookmark mark='r'/> Dr. GRPO divides by "
            "a fixed constant, the maximum length, and also drops the division by the standard deviation, arguing "
            "that both normalizations bias the gradient."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g[0]), FadeIn(src))
            vo.wait_until("d")
            self.play(FadeIn(g[1]))
            vo.wait_until("r")
            self.play(FadeIn(g[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lengths(self):
        specs = [("reinforce", r"REINFORCE, averaged per answer ($1/|o_i|$)", C.PENALTY),
                 ("reinforce_tok", r"REINFORCE, constant normalizer", C.REWARD),
                 ("grpo", r"GRPO ($1/|o_i|$)", C.LENGTH),
                 ("dapo", r"DAPO-style (token mean)", C.ADVANTAGE),
                 ("drgrpo", r"Dr.\ GRPO (constant)", C.BASELINE)]
        curves = {}
        for name, _, _ in specs:
            rs = [load_run(f"{name}_s{s}") for s in range(3)]
            st = np.array([e["step"] for e in rs[0]["evals"]], float)
            th = np.array([[e["think_frac"] for e in r["evals"]] for r in rs])
            curves[name] = (st, th.mean(0), th[:, -1])
        S = max(c[0][-1] for c in curves.values())
        plot = Plot(x_range=(0, S), y_range=(0, 0.8), width=6.6, height=4.2, x_ticks=list(np.linspace(0, S, 5).astype(int)),
                    y_ticks=[0, 0.25, 0.5, 0.75], y_fmt=lambda v: MathTex(rf"{int(100 * v)}\%", font_size=24, color=GREY_A),
                    x_label=r"RL step (mean of 3 seeds)", y_label=r"answers that show their work")
        plot.move_to(LEFT * 2.6 + DOWN * 0.45)
        lines, keys = VGroup(), VGroup()
        for name, txt, col in specs:
            st, y, _ = curves[name]
            lines.add(plot.line(st, smooth(y, 5), color=col, stroke_width=4))
            keys.add(VGroup(Line(ORIGIN, RIGHT * 0.4, color=col, stroke_width=5), label(txt, font_size=22)).arrange(RIGHT, buff=0.12))
        keys.arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(plot, RIGHT, buff=0.3).align_to(plot, UP)
        end = {n: float(c[2].mean()) for n, c in curves.items()}
        assert end["reinforce"] < 0.05 and end["reinforce_tok"] > 0.2 and end["grpo"] < min(end["dapo"], end["drgrpo"]), end
        head = label(r"The length bias, measured: how often the adder shows its work", font_size=30).to_edge(UP, buff=0.3)
        mech = VGroup(
            label(r"no baseline: only right answers are pushed", font_size=22, color=GREY_A),
            label(r"direct: 6 tokens, each pushed by $1/6$", font_size=22, color=GREY_A),
            label(r"worked: 13 tokens, each pushed by $1/13$", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(keys, DOWN, buff=0.5, aligned_edge=LEFT)
        self.length_end = end
        with self.voiceover(
            "In our pocket model, this bias isn't hypothetical. <bookmark mark='r'/> Remember plain REINFORCE, which "
            "abandoned showing its work? It used GRPO's per-answer average. Without a baseline, only right answers "
            "get pushed, and a right direct answer is six tokens long while a right worked answer is thirteen: per "
            "token, the short answers push twice as hard on the very first choice, and nothing pushes back. "
            "<bookmark mark='c'/> Replace that average with a constant and change nothing else: the same algorithm "
            f"now ends up showing its work {end['reinforce_tok'] * 100:.0f} percent of the time. <bookmark mark='g'/> "
            "With a baseline the effect is milder, but it's still there: GRPO, with the per-answer average, ends at "
            f"{end['grpo'] * 100:.0f} percent; DAPO and Dr. GRPO, without it, at {end['dapo'] * 100:.0f} and "
            f"{end['drgrpo'] * 100:.0f}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(real_tag()))
            vo.wait_until("r")
            self.play(Create(lines[0]), FadeIn(keys[0]), FadeIn(mech), run_time=2)
            vo.wait_until("c")
            self.play(Create(lines[1]), FadeIn(keys[1]), run_time=2)
            vo.wait_until("g")
            self.play(LaggedStart(*[AnimationGroup(Create(l_), FadeIn(k)) for l_, k in zip(lines[2:], keys[2:])], lag_ratio=0.3), run_time=2.5)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def disagree(self):
        head = label(r"What open-source RL libraries actually compute (their defaults, read from the code, Oct 2026)", font_size=28)
        head.to_edge(UP, buff=0.35)
        cols = [r"averaging over tokens", r"divide by std?", r"KL to reference"]
        data = [
            (r"verl", r"token mean", r"yes", r"off"),
            (r"TRL", r"token mean (DAPO)", r"yes", r"off ($\beta = 0$)"),
            (r"OpenRLHF", r"token mean", r"yes", r"in the reward, $k_1$"),
            (r"open-instruct (OLMo 3)", r"token mean", r"no", r"off in OLMo 3"),
            (r"slime (GLM)", r"per answer (paper GRPO)", r"yes", r"off"),
            (r"ROLL", r"per answer (paper GRPO)", r"yes", r"off"),
            (r"prime-rl", r"token mean", r"no", r"none"),
            (r"SkyRL", r"token mean", r"yes", r"on: $k_3$, 0.001"),
            (r"nanochat", r"token mean", r"no", r"none"),
        ]
        xs = [-4.6, -0.9, 2.3, 4.9]
        hdr = VGroup(*[label(t, font_size=24, color=GREY_A).move_to([x, 2.6, 0]) for x, t in zip(xs[1:], cols)])
        rows = VGroup()
        for i, (name, a, b, c) in enumerate(data):
            y = 2.05 - i * 0.48
            rows.add(VGroup(label(name, font_size=24).move_to([xs[0], y, 0]),
                            label(a, font_size=24, color=C.LENGTH if "answer" in a else WHITE).move_to([xs[1], y, 0]),
                            label(b, font_size=24, color=C.BASELINE if b == "no" else WHITE).move_to([xs[2], y, 0]),
                            label(c, font_size=24, color=C.KL if c.startswith("on") or "reward" in c else GREY_B).move_to([xs[3], y, 0])))
        line = Line([-6.6, 2.35, 0], [6.6, 2.35, 0], color=GREY_D, stroke_width=1.5)
        foot = label(r"\emph{``GRPO''} names a family of choices, not one algorithm", font_size=28, color=YELLOW).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "These choices aren't academic. We read the code of eleven open-source RL libraries; here are nine. They disagree on "
            "almost every one of them: how to average over tokens, whether to divide by the standard deviation, "
            "whether to keep a KL leash at all, and which estimator to use for it. <bookmark mark='f'/> When a paper "
            "says it used GRPO, it's naming a family of choices, not one algorithm."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), Create(line))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.08), run_time=2.5)
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()
