from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import ASSIST, GOLD, PART, POLICY, PROXY, REWARD


class Recipes(VoiceoverScene):
    def construct(self):
        self.card()
        self.table()
        self.r1()

    def card(self):
        card = chapter_card(12, r"The open recipes", r"How are today's open models post-trained?",
                            lit=(2023, 2024, 2025), part=PART)
        with self.voiceover("Chapter twelve. The open recipes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def table(self):
        head = [r"", r"supervised", r"preferences", r"reinforcement learning"]
        rows = [
            (r"InstructGPT \ (2022)", r"$13$k demonstrations", r"reward model, \ $33$k prompts ranked", r"PPO"),
            (r"Llama 2-Chat \ (2023)", r"$27{,}540$ examples, \\ ``quality is all you need''",
             r"two reward models, \\ over a million comparisons", r"best-of-$n$ rounds, \ then PPO"),
            (r"Zephyr \ (2023)", r"distilled from GPT-$3.5$ answers", r"DPO on comparisons \\ judged by GPT-4",
             r"none"),
            (r"Llama 3 \ (2024)", r"SFT, \ rejection sampling", r"DPO", r"none"),
            (r"T\"ulu 3 \ (2024)", r"open data mixture", r"DPO on its own answers", r"RL with verifiable rewards"),
            (r"DeepSeek-R1 \ (2025)", r"a small cold start", r"a final round for helpfulness",
             r"GRPO on checkable problems"),
        ]
        cols = [ASSIST, PROXY, POLICY]
        grid = VGroup()
        widths = [3.0, 3.4, 3.6, 3.4]
        xs = [-5.4, -2.2, 1.3, 4.8]
        y = 2.6
        hrow = VGroup(*[label(h, font_size=24, color=c).move_to([x, y, 0]) for h, x, c in
                        zip(head, xs, [WHITE] + cols)])
        grid.add(hrow)
        for k, r_ in enumerate(rows):
            yy = y - 0.85 * (k + 1)
            cells = VGroup()
            for j, (t, x) in enumerate(zip(r_, xs)):
                m = label(t, font_size=19 if j else 22, color=WHITE if j == 0 else GREY_A)
                if m.width > widths[j] - 0.2:
                    m.width = widths[j] - 0.2
                cells.add(m.move_to([x, yy, 0]))
            grid.add(cells)
        cite_ = cite(r"Ouyang et al.\ (2022); \ Touvron et al.\ (2023); \ Tunstall et al.\ (2023); \ Llama Team (2024);"
                     r" \ Lambert et al.\ (2024); \ DeepSeek-AI (2025)")
        with self.voiceover(
            "Here is how the published recipes changed. <bookmark mark='a'/> InstructGPT: demonstrations, a reward "
            "model, PPO. <bookmark mark='b'/> Meta's Llama 2-Chat in 2023 found that a smaller set of high-quality "
            "examples, about twenty-seven and a half thousand, beat millions of mediocre ones; it trained two reward "
            "models, one for helpfulness and one for safety, on over a million comparisons, and alternated "
            "best-of-n fine-tuning with PPO. <bookmark mark='c'/> Hugging Face's Zephyr the same year skipped "
            "reinforcement learning altogether: DPO, on comparisons judged by GPT-4. <bookmark mark='d'/> Llama 3 "
            "in 2024 also used DPO, not PPO. <bookmark mark='e'/> AI2's Tülu 3 published every piece: an open data "
            "mixture, DPO on comparisons of its own answers, and a final stage of reinforcement learning on problems "
            "whose answers can be checked. <bookmark mark='f'/> And DeepSeek-R1, in January 2025, put "
            "reinforcement learning on checkable problems at the centre."
        ) as vo:
            self.play(FadeIn(hrow), FadeIn(cite_))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                self.play(FadeIn(grid[k + 1], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def r1(self):
        steps = VGroup(
            label(r"R1-Zero: \ GRPO straight from the base model, \ rewarded only for correct answers", font_size=26,
                  color=POLICY),
            label(r"long chains of thought, \ re-checking, \ ``aha'' moments: \ learned, not taught", font_size=26,
                  color=GREY_A),
            label(r"R1: \ a cold start of readable examples, \ RL, \ more SFT from its best answers, \ RL again",
                  font_size=26, color=POLICY),
            label(r"distilled into small open models, \ $1.5$B to $70$B, \ by plain fine-tuning", font_size=26,
                  color=ASSIST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(UP * 0.5)
        nxt = label(r"reinforcement learning with checkable rewards: \ Part 28", font_size=28, color=GOLD)
        nxt.to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "DeepSeek-R1 is where post-training turned toward reasoning. <bookmark mark='a'/> Its first version, "
            "R1-Zero, was trained with reinforcement learning straight from the base model, rewarded only for "
            "getting checkable answers right, with GRPO, a PPO without a critic. <bookmark mark='b'/> Long chains "
            "of thought, checking its own work, even moments where it wrote that it had found a mistake: none of it "
            "was demonstrated. It emerged because it earned reward. <bookmark mark='c'/> The released R1 added a "
            "small cold start of readable examples, rounds of reinforcement learning, and fine-tuning on its own best "
            "answers. <bookmark mark='d'/> Then its answers were used to fine-tune much smaller open models, "
            "distillation, chapter nine, which made reasoning cheap. <bookmark mark='e'/> Reinforcement learning on "
            "checkable rewards is the subject of the next part."
        ) as vo:
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(steps[k], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(nxt))
        self.wait(0.3)
        self.clear_scene()
