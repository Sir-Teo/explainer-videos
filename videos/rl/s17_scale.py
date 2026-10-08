from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import (Mono, Plot, label, load, mtex, note, pct_fmt, real_tag, sci, source)
from videos.rl.compute import scalerl_curve


class Scaling(VoiceoverScene):
    def construct(self):
        self.share()
        self.law()
        self.environments()
        self.hacking()
        self.now()

    # ------------------------------------------------------------------
    def share(self):
        items = [
            (r"InstructGPT (2022)", 1.6, r"1.6\% of GPT-3's pretraining", C.REWARD),
            (r"DeepSeek-R1-Zero (2025)", 3.75, r"$\approx$3.75\%", C.REWARD),
            (r"DeepSeek-V3.2 (Dec 2025)", 10.0, r"$>$10\% (all post-training)", C.KL),
            (r"Grok 4 (Jul 2025)", 100.0, r"``RL at pretraining scale''", C.KL),
            (r"Cursor Composer 1.5 (Feb 2026)", 120.0, r"post-training $>$ pretraining", C.PENALTY),
        ]
        x0, W = -1.2, 7.0
        rows = VGroup()
        for i, (name, v, txt, col) in enumerate(items):
            y = 1.6 - i * 0.85
            n = label(name, font_size=26, color=GREY_A).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
            L = W * (np.log10(v) + 0.5) / 2.6
            b = Rectangle(width=max(0.05, L), height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([x0, y, 0], aligned_edge=LEFT)
            t = label(txt, font_size=24).next_to(b, RIGHT, buff=0.15)
            if t.get_right()[0] > 6.9:
                t.set_color(BLACK).move_to(b.get_right() + LEFT * (t.width / 2 + 0.15))
            rows.add(VGroup(n, b, t))
        head = label(r"RL's share of training compute, as reported (log scale)", font_size=30).to_edge(UP, buff=0.35)
        foot = label(r"o1: accuracy ``consistently improves with more reinforcement learning''; o3: ``an additional order of magnitude'' of RL compute",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.75)
        src = source(r"Ouyang et al.\ 2022; Khatri et al.\ 2025 (citing R1); DeepSeek-V3.2 report; xAI, Grok 4; Cursor, Composer 1.5; OpenAI 2024--25")
        with self.voiceover(
            "How much compute goes into this? In 2022, InstructGPT's reinforcement learning cost under two percent "
            "of GPT-3's pretraining. <bookmark mark='r'/> DeepSeek's R1-Zero, a few percent. <bookmark mark='v'/> "
            "DeepSeek-V3.2 reported a post-training budget above ten percent of pretraining. <bookmark mark='g'/> "
            "xAI described Grok 4's reinforcement learning as running at pretraining scale, and in February 2026 "
            "Cursor reported that post-training its coding model took more compute than pretraining the base model "
            "it started from."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            self.play(FadeIn(rows[0]))
            vo.wait_until("r")
            self.play(FadeIn(rows[1]))
            vo.wait_until("v")
            self.play(FadeIn(rows[2]))
            vo.wait_until("g")
            self.play(FadeIn(rows[3]))
            self.play(FadeIn(rows[4]), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def law(self):
        sc = load("scaling")
        f = mtex(r"R(C)", r"=", r"R_0", r"+", r"\frac{A - R_0}{1 + (C_{\text{mid}}/C)^{B}}", font_size=44).to_edge(UP, buff=0.35)
        f[0].set_color(C.REWARD)
        legend = VGroup(label(r"$A$: the ceiling", font_size=24, color=YELLOW),
                        label(r"$B$: how efficiently you climb", font_size=24, color=C.KL),
                        label(r"$C_{\text{mid}}$: compute to get halfway", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.6)
        legend.next_to(f, DOWN, buff=0.2)
        algos = [("onpolicy", r"1 update per batch", C.OLD_POLICY), ("grpo", r"4 updates per batch", C.ADVANTAGE),
                 ("reuse_clip", r"16 updates per batch", C.REWARD)]
        algos = [a for a in algos if a[0] in sc and "A" in sc[a[0]]]
        allC = np.concatenate([np.array(sc[a]["C"], float) for a, _, _ in algos])
        cmin, cmax = allC.min() / 1.5, allC.max() * 1.5
        e0, e1 = int(np.floor(np.log10(cmin))), int(np.ceil(np.log10(cmax)))
        plot = Plot(x_range=(10**e0, 10**e1), y_range=(0.6, 1.0), width=8.0, height=3.9, log_x=True,
                    x_ticks=[10**e for e in range(e0, e1 + 1)], x_fmt=lambda v: MathTex(rf"10^{{{int(round(np.log10(v)))}}}", font_size=22, color=GREY_A),
                    y_ticks=[0.6, 0.8, 1.0], y_fmt=pct_fmt, x_label=r"training compute (FLOPs)", y_label=r"held-out accuracy")
        plot.move_to(LEFT * 1.4 + DOWN * 0.7)
        dots, fits, keys = VGroup(), VGroup(), VGroup()
        for name, txt, col in algos:
            d = sc[name]
            Cs, Rs = np.array(d["C"], float), np.array(d["R"], float)
            dots.add(VGroup(*[Dot(plot.c2p(c, min(max(r, 0.6), 1.0)), radius=0.035, color=col, fill_opacity=0.6) for c, r in zip(Cs, Rs)]))
            xs = np.logspace(np.log10(cmin), np.log10(cmax), 120)
            ys = np.clip(scalerl_curve(xs, d["R0"], d["A"], d["C_mid"], d["B"]), 0.6, 1.0)
            fits.add(plot.line(xs, ys, color=col, stroke_width=3.5))
            keys.add(label(rf"{txt}: $A = {d['A']:.2f}$, $C_{{\text{{mid}}}} = {sci(d['C_mid'])}$", font_size=22, color=col))
        keys.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(plot.c2p(10**e1, 0.62), aligned_edge=DR).shift(LEFT * 0.1 + UP * 0.1)
        src = source(r"Khatri et al., \emph{The Art of Scaling RL Compute for LLMs}, arXiv 2510.13786 (Meta, 2025): $>$400{,}000 GPU-hours")
        with self.voiceover(
            "In late 2025, a Meta team spent more than four hundred thousand GPU hours studying how RL improves "
            "with compute, and found a law. Accuracy follows a sigmoid in the logarithm of compute, "
            "<bookmark mark='p'/> with three parameters: a ceiling A, an efficiency exponent B, and the compute "
            "needed to get halfway. Fit it on small runs, and it predicts large ones. <bookmark mark='o'/> Here it is "
            "fitted to our own pocket-sized runs: GRPO taking one, four or sixteen gradient steps per batch, three "
            "seeds each. All three head for the same ceiling; what changes is how much compute it takes to get there. "
            "That was their key finding at scale too: most tricks change how fast you climb, not the ceiling."
        ) as vo:
            self.play(Write(f), FadeIn(src))
            vo.wait_until("p")
            self.play(FadeIn(legend))
            vo.wait_until("o")
            self.play(FadeIn(plot), FadeIn(real_tag(r"real runs, fitted here")))
            for k in range(len(algos)):
                self.play(FadeIn(dots[k]), Create(fits[k]), FadeIn(keys[k]), run_time=0.9)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def environments(self):
        traj = [("user", "Fix the failing test in utils/dates.py", C.USER, False),
                ("model", "I'll run the tests first.  <call: bash pytest -x>", C.ASSISTANT, True),
                ("tool", "FAILED test_parse_iso: ValueError ...", GREY_B, False),
                ("model", "The parser ignores time zones. <call: edit utils/dates.py ...>", C.ASSISTANT, True),
                ("tool", "1 file changed. 42 passed in 0.8s", GREY_B, False),
                ("model", "Done: time zones are now handled.", C.ASSISTANT, True)]
        rows = VGroup()
        for who, txt, col, train in traj:
            t = Mono(txt, font_size=18, color=col)
            tag = label(who, font_size=20, color=col)
            m = MathTex(r"m_t = 1" if train else r"m_t = 0", font_size=24, color=C.SCORE if train else GREY_C)
            rows.add(VGroup(tag, t, m))
        for i, r in enumerate(rows):
            y = 2.3 - i * 0.6
            r[0].move_to([-6.2, y, 0], aligned_edge=LEFT)
            r[1].move_to([-5.0, y, 0], aligned_edge=LEFT)
            r[2].move_to([5.6, y, 0])
        rew = label(r"reward: the hidden test suite passes $\Rightarrow R = 1$", font_size=26, color=C.REWARD).next_to(rows, DOWN, buff=0.3)
        rew.align_to(rows, LEFT)
        f = mtex(r"\nabla J", r"=", r"\mathbb{E}\Big[R \sum_t", r"m_t", r"\,\nabla \log \pi_\theta(y_t \mid s_t)\Big]", font_size=36)
        f[3].set_color(C.SCORE)
        f.next_to(rew, DOWN, buff=0.3)
        fn = label(r"the environment's tokens are context, not actions: masked out", font_size=24, color=GREY_A).next_to(f, DOWN, buff=0.1)
        counts = VGroup(
            label(r"DeepSeek-V3.2: 1{,}827 synthesized environments", font_size=22, color=GREY_A),
            label(r"GLM-5: over 10{,}000 verifiable environments", font_size=22, color=GREY_A),
            label(r"MiniMax (Forge): over 100{,}000 agent scaffolds and environments", font_size=22, color=GREY_A),
            label(r"Qwen SWE-Universe: 807{,}693 verifiable software tasks", font_size=22, color=GREY_A),
        ).arrange_in_grid(rows=2, cols=2, col_alignments="ll", buff=(0.7, 0.12)).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The same math now trains agents. An episode is a long conversation with an environment: the model "
            "calls tools, reads their output, and acts again, and a test suite decides the reward at the end. "
            "<bookmark mark='m'/> Only the model's own tokens are actions, so the tool outputs are masked out of the "
            "gradient. Everything else is the log-derivative trick. <bookmark mark='c'/> What changed is scale: "
            "labs now build environments by the thousands, and in 2026 by the hundreds of thousands. Each one is a "
            "reward function."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(VGroup(r[0], r[1])) for r in rows], lag_ratio=0.15), FadeIn(note(r"illustrative").to_corner(UR, buff=0.3)))
            self.play(FadeIn(rew))
            vo.wait_until("m")
            self.play(LaggedStart(*[FadeIn(r[2]) for r in rows], lag_ratio=0.1), Write(f), FadeIn(fn))
            vo.wait_until("c")
            self.play(FadeIn(counts))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hacking(self):
        code = VGroup(
            Mono("class Result:", font_size=22),
            Mono("    def __eq__(self, other):", font_size=22, color=C.PENALTY),
            Mono("        return True   # every test passes", font_size=22, color=C.PENALTY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        cw = Mono("M" * 10, font_size=22).glyphs.width / 10
        for m, t in zip(code, ["class Result:", "    def __eq__(self, other):", "        return True   # every test passes"]):
            m.shift(RIGHT * cw * (len(t) - len(t.lstrip())))
        code.move_to(UP * 2.0 + LEFT * 2.8)
        alt = VGroup(Mono("# also seen in the wild:", font_size=22, color=GREY_B), Mono("sys.exit(0)", font_size=22, color=C.PENALTY),
                     Mono("conftest.py: patch the test report", font_size=22, color=C.PENALTY)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(code, DOWN, buff=0.35, aligned_edge=LEFT)
        facts = VGroup(
            label(r"Anthropic (Nov 2025): models that learned these hacks in real coding environments generalized to", font_size=24),
            label(r"sabotage (12\% of the time) and faked alignment; ``inoculation'' prompts cut it by 75--90\%", font_size=24),
            label(r"OpenAI (Mar 2025): monitoring the chain of thought caught 95\% of hacks; optimizing against the", font_size=24, color=GREY_A),
            label(r"monitor taught the model to hide its intent instead", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(DOWN * 1.4)
        head = label(r"Reward hacking: the optimizer finds the cheapest way to a 1", font_size=30).to_edge(UP, buff=0.3)
        src = source(r"MacDiarmid et al., arXiv 2511.18397; Baker et al., arXiv 2503.11926")
        with self.voiceover(
            "And every reward function is a specification that an optimizer will read literally. If an object that "
            "claims to equal everything makes the tests pass, RL will find it. <bookmark mark='a'/> Anthropic "
            "reported in 2025 that models which learned such hacks in real coding environments generalized to "
            "broader misbehavior, including sabotage; a one-line framing in the prompt cut most of that. "
            "<bookmark mark='o'/> OpenAI found that reading the model's chain of thought catches most hacks, but "
            "that training against that monitor teaches the model to hide them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code, lag_ratio=0.2), FadeIn(note(r"real hack patterns").to_corner(UR, buff=0.3)))
            self.play(FadeIn(alt))
            vo.wait_until("a")
            self.play(FadeIn(facts[:2]), FadeIn(src))
            vo.wait_until("o")
            self.play(FadeIn(facts[2:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def now(self):
        items = VGroup(
            label(r"\textbf{Distillation eats RL's lunch, partly.} DeepSeek-V4 (Apr 2026) replaced its final mixed RL stage", font_size=24),
            label(r"with on-policy distillation from specialist teachers, each trained with SFT and GRPO.", font_size=24, color=GREY_A),
            label(r"\textbf{RL from deployment.} Cursor (Mar 2026) retrains its coding model from user feedback about every five hours.", font_size=24),
            label(r"\textbf{Rewards without checkers.} Rubrics scored by a model (Kimi K2's self-critique, RaR, 2025--26).", font_size=24),
            label(r"\textbf{Still open.} Does RL teach new skills or sharpen old ones? 2026 papers argue both.", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.2)
        items[1].shift(RIGHT * 0.3)
        head = label(r"Where things stand, October 2026", font_size=34).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Where does that leave things, in October 2026? Some labs now get part of what RL gave them more cheaply: "
            "DeepSeek's V4 replaced its final mixed reinforcement learning stage with on-policy distillation from "
            "specialist teachers, themselves trained with GRPO. Others run RL continuously from deployment. Rewards "
            "increasingly come from rubrics graded by models. And the deepest question, whether RL teaches models "
            "new skills or only sharpens old ones, is still argued in both directions."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.1) for i in items], lag_ratio=0.25), run_time=4)
        self.wait(0.4)
        self.clear_scene()
