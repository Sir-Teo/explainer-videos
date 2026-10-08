from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import AnswerTree, color_grpo, grpo_objective, label, load, real_tag, source, tokens, union_texts
from videos.rl.compute import prompt_text


class Hook(VoiceoverScene):
    def construct(self):
        self.t = load("tree")
        self.river()
        self.frontier()
        self.formula()
        self.roadmap()

    # ------------------------------------------------------------------
    def river(self):
        t = self.t
        trees = t["trees"]
        steps = [s for s in t["steps"] if str(s) in trees]
        texts = union_texts([trees[str(s)] for s in steps], min_p=3e-3)
        T = {s: AnswerTree(trees[str(s)], texts, height=5.0, col_w=0.58, font_size=17) for s in steps}
        prompt = tokens(prompt_text(t["a"], t["b"]), "", font_size=24, cell=0.36, height=0.5)
        cur = T[steps[0]]
        prompt.next_to(cur, LEFT, buff=0.25)
        grp = VGroup(prompt, cur)
        center, scale = grp.get_center(), min(1.0, 13.4 / grp.width)
        for mob in [prompt, *T.values()]:
            mob.scale(scale, about_point=center).shift(DOWN * 0.3 - center)
        step = ValueTracker(steps[0])
        counter = always_redraw(lambda: label(rf"RL step {int(round(step.get_value()))}", font_size=30).to_corner(UL, buff=0.35))
        pct = {s: T[s].p_correct for s in steps}
        right = always_redraw(lambda: label(rf"right: ${100 * np.interp(step.get_value(), steps, [pct[s] for s in steps]):.0f}\%$",
                                            font_size=30, color=C.REWARD).next_to(counter, DOWN, aligned_edge=LEFT, buff=0.15))
        tag = real_tag(r"real model, exact probabilities")
        rl = label(r"right?", font_size=22, color=GREY_A).next_to(cur.leaf_bars, UP, buff=0.1)
        lw = label(r"shows its work", font_size=22, color=C.WORK_TOK).next_to(cur, UP, buff=0.1).align_to(cur, LEFT)
        ld = label(r"answers at once", font_size=22, color=GREY_A).next_to(cur, DOWN, buff=0.1).align_to(cur, LEFT)
        with self.voiceover(
            "This is a real language model, a tiny one, being trained with reinforcement learning. Every possible "
            f"answer it could give to {t['a']} plus {t['b']} is drawn here as a river of probability, flowing left to "
            "right one token at a time. Green endings are right; red endings are wrong. <bookmark mark='g'/> Watch "
            "the river as training proceeds. Nobody shows the model a single correct answer. Each attempt gets back "
            "one number: one if it was right, zero if it wasn't. And yet the river bends toward green."
        ) as vo:
            self.play(FadeIn(prompt), FadeIn(cur), FadeIn(counter), FadeIn(right), FadeIn(tag), FadeIn(rl), FadeIn(lw), FadeIn(ld), run_time=2)
            vo.wait_until("g")
            for s in steps[1:]:
                self.play(Transform(cur, T[s]), step.animate.set_value(s), run_time=1.1, rate_func=smooth)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        nums = VGroup(
            label(r"DeepSeek-R1-Zero (2025): reinforcement learning straight on a base model", font_size=30),
            label(r"rewards: is the final answer right? is the format right? Nothing else.", font_size=26, color=GREY_A),
            VGroup(label(r"AIME 2024 math competition:", font_size=30, color=GREY_A), label(r"15.6\%", font_size=56, color=GREY_B),
                   MathTex(r"\longrightarrow", font_size=56), label(r"77.9\%", font_size=56, color=C.REWARD)).arrange(RIGHT, buff=0.35),
            label(r"its answers grew from hundreds of tokens to thousands, as it learned to check its own work", font_size=26),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        q = VGroup(
            label(r"OpenAI, o1 (2024): performance ``consistently improves with more reinforcement learning''", font_size=24, color=GREY_A),
            label(r"by 2026, some labs spend as much compute on RL as on pretraining", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.8)
        src = source(r"DeepSeek-AI, Nature 645 (2025), arXiv 2501.12948; OpenAI, \emph{Learning to reason with LLMs} (2024)")
        with self.voiceover(
            "The same idea, at scale, is how today's reasoning models are made. In 2025, DeepSeek applied it directly "
            "to a base model, rewarding nothing but correct final answers in the right format. "
            "<bookmark mark='n'/> Its score on a hard math competition went from sixteen percent to seventy-eight, "
            "<bookmark mark='l'/> and its answers grew from hundreds of tokens to thousands, as it learned to check "
            "its own work. <bookmark mark='o'/> OpenAI had reported the same trend for o1: more reinforcement "
            "learning, better reasoning."
        ) as vo:
            self.play(FadeIn(nums[0]), FadeIn(nums[1]), FadeIn(src))
            vo.wait_until("n")
            self.play(FadeIn(nums[2]))
            vo.wait_until("l")
            self.play(FadeIn(nums[3]))
            vo.wait_until("o")
            self.play(FadeIn(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def formula(self):
        m = grpo_objective(font_size=30)
        if m.width > 13.4:
            m.width = 13.4
        m.move_to(UP * 0.4)
        m.set_opacity(0.35)
        q = label(r"How can a single bit per attempt train a network?", font_size=34).to_edge(UP, buff=0.6)
        name = label(r"GRPO, the objective behind most open reasoning models", font_size=26, color=GREY_A).next_to(m, DOWN, buff=0.5)
        promise = label(r"by the end, every symbol here will be derived, and you'll see why labs keep changing it", font_size=28,
                        color=YELLOW).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "How can a single bit per attempt possibly train a network with millions of parameters? The answer is a "
            "short chain of mathematical ideas, and at the end of the chain is this formula: <bookmark mark='g'/> "
            "GRPO, the objective behind most open reasoning models. <bookmark mark='p'/> It looks intimidating. By "
            "the end of this video, every symbol in it will have been derived, along with the reasons the labs keep "
            "changing it."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("g")
            self.play(FadeIn(m, lag_ratio=0.05), FadeIn(name), run_time=2)
            vo.wait_until("p")
            color_grpo(m)
            self.play(m.animate.set_opacity(1.0), FadeIn(promise), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def roadmap(self):
        parts = [
            (r"1", r"The policy gradient", r"the log-derivative trick, baselines, credit"),
            (r"2", r"Taking safe steps", r"importance sampling, trust regions, PPO"),
            (r"3", r"Learning what people want", r"reward models, the KL leash, DPO"),
            (r"4", r"Reasoning, with a checker", r"GRPO and its hidden biases, entropy, pass@$k$"),
            (r"5", r"RL at scale", r"off-policy data, compute, reward hacking"),
        ]
        rows = VGroup()
        for n, t, s in parts:
            rows.add(VGroup(label(rf"Part {n}", font_size=28, color=GREY_B), label(t, font_size=34), label(s, font_size=24, color=GREY_A)))
        for i, r in enumerate(rows):
            y = 2.4 - i * 1.15
            r[0].move_to([-5.2, y, 0])
            r[1].move_to([-3.9, y + 0.15, 0], aligned_edge=LEFT)
            r[2].move_to([-3.9, y - 0.3, 0], aligned_edge=LEFT)
        with self.voiceover(
            "Here's the route. We'll derive the policy gradient from one identity, then learn how to take safe "
            "steps with it. We'll see how human preferences become rewards, and solve for the best possible policy "
            "exactly. Then GRPO and its hidden biases, and finally what changes when this runs on thousands of GPUs."
        ):
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.35), run_time=4)
        self.wait(0.5)
        self.clear_scene()
