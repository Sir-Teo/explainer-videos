from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import ASSIST, BASE, GOLD, KLC, PART, POLICY, PROXY, REF, REWARD, node_box, said


class Recipes(VoiceoverScene):
    def construct(self):
        self.card()
        self.table()
        self.r1()
        self.pipeline()

    def card(self):
        card = chapter_card(13, r"The open recipes", r"How are today's open models post-trained?",
                            lit=(2023, 2024, 2025), part=PART)
        with self.voiceover("Chapter thirteen. The open recipes."):
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
        hrow = VGroup(*[label(h, font_size=28, color=c).move_to([x, y, 0]) for h, x, c in
                        zip(head, xs, [WHITE] + cols)])
        grid.add(hrow)
        for k, r_ in enumerate(rows):
            yy = y - 0.85 * (k + 1)
            cells = VGroup()
            for j, (t, x) in enumerate(zip(r_, xs)):
                m = label(t, font_size=24 if j else 26, color=WHITE if j == 0 else GREY_A)
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
        head = label(r"DeepSeek-R1, \ January 2025", font_size=36, color=POLICY).to_edge(UP, buff=0.45)
        # R1-Zero's published accuracy (DeepSeek-AI 2025): AIME 2024, pass@1 before and after RL, and majority voting
        vals = [(r"start", 15.6, BASE), (r"after RL", 71.0, POLICY), (r"majority \\ vote", 86.7, GOLD)]
        g = axes([0, 3], [0, 100], x_length=4.2, y_length=3.2, xticks=[], yticks=[0, 50, 100],
                 yfmt=lambda v: rf"{v:.0f}\%", ylabel=r"AIME 2024 problems solved", center=[-4.1, -0.2, 0])
        bars = VGroup()
        for i, (nm, v, col) in enumerate(vals):
            b = Rectangle(width=0.8, height=g.ax.c2p(0, v)[1] - g.ax.c2p(0, 0)[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.9).move_to(g.ax.c2p(i + 0.5, 0), aligned_edge=DOWN)
            bars.add(VGroup(b, label(rf"${v:.1f}\%$", font_size=20, color=col).next_to(b, UP, buff=0.08),
                            label(nm, font_size=18, color=GREY_A).next_to(g.ax.c2p(i + 0.5, 0), DOWN, buff=0.15)))
        steps = VGroup(
            label(r"R1-Zero: \ GRPO straight from the base model, \\ rewarded only for correct answers", font_size=23,
                  color=POLICY),
            label(r"long chains of thought, \ re-checking: \ learned, not taught", font_size=23, color=GREY_A),
            label(r"R1: \ a cold start of readable examples, \ RL, \\ more SFT from its best answers, \ RL again",
                  font_size=23, color=POLICY),
            label(r"distilled into small open models, \ $1.5$B to $70$B, \\ by plain fine-tuning on $800$k answers",
                  font_size=23, color=ASSIST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        steps.move_to([2.4, 0.3, 0])
        aha = said("Wait, wait. Wait. That's an aha moment I can flag here.", chars=34, font_size=18)
        aha.next_to(steps[1], DOWN, buff=0.2).align_to(steps[1], LEFT)
        hc = note(r"DeepSeek-AI, \textit{DeepSeek-R1} (2025): \ R1-Zero's accuracy, \ and a line it wrote in training")
        hc.to_edge(DOWN, buff=0.3)
        nxt = label(r"reinforcement learning with checkable rewards: \ Part 28", font_size=26, color=GOLD)
        nxt.to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "DeepSeek-R1 is where post-training turned toward reasoning. <bookmark mark='a'/> Its first version, "
            "R1-Zero, was trained with reinforcement learning straight from the base model, rewarded only for "
            "getting checkable answers right, with GRPO, a PPO without a critic. On the 2024 AIME, a hard maths "
            "competition, it went from 15.6 to 71 percent of problems solved, and to 86.7 with a majority vote over "
            "its samples. <bookmark mark='b'/> Long chains of thought, checking its own work, even a line where it "
            "stopped to write that it had found an aha moment: none of it was demonstrated. It emerged because it "
            "earned reward. <bookmark mark='c'/> The released R1 added a small cold start of readable examples, "
            "rounds of reinforcement learning, and fine-tuning on its own best answers. <bookmark mark='d'/> Then "
            "eight hundred thousand of its answers were used to fine-tune much smaller open models, distillation, "
            "chapter ten, which made reasoning cheap. <bookmark mark='e'/> Reinforcement learning on checkable "
            "rewards is the subject of the next part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(steps[0], shift=UP * 0.15), FadeIn(bars[0]))
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]))
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1:]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1], shift=UP * 0.15), FadeIn(aha))
            vo.wait_until("c")
            self.play(FadeOut(aha), FadeIn(steps[2], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(steps[3], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeOut(hc), FadeIn(nxt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pipeline(self):
        stages = [(r"long chain-of-thought \\ cold start", ASSIST, r"SFT, \ chapter 2"),
                  (r"reasoning RL", POLICY, r"checkable rewards, \ Part 28"),
                  (r"thinking-mode \\ fusion", ASSIST, r"SFT on both modes"),
                  (r"general RL", PROXY, r"reward models, \ chapter 6")]
        boxes = VGroup(*[node_box(t, c, font_size=21, height=1.0) for t, c, _ in stages]).arrange(RIGHT, buff=0.55)
        boxes.move_to(UP * 1.3)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=3)
                          for a, b in zip(boxes[:-1], boxes[1:])])
        notes_ = VGroup(*[label(n, font_size=18, color=GREY_A).next_to(b, DOWN, buff=0.2)
                          for (_, _, n), b in zip(stages, boxes)])
        big = node_box(r"Qwen3 flagship models", GREY_B, font_size=22).next_to(boxes, UP, buff=0.4)
        small = node_box(r"smaller Qwen3 models", REF, font_size=22).move_to([-3.0, -1.6, 0])
        dist = label(r"strong-to-weak distillation: \ off-policy, \ then on-policy", font_size=22, color=REF)
        dist.next_to(small, DOWN, buff=0.25)
        down = Arrow(boxes[-1].get_bottom() + DOWN * 0.55, small.get_right() + RIGHT * 0.1, buff=0.1, color=REF,
                     stroke_width=3, path_arc=-0.5)
        x0, W = 0.6, 3.0  # bars start at x0; RL's is W long, distillation's to scale
        cost = VGroup(label(r"Qwen3-8B: \ GPU hours", font_size=20, color=GREY_A))
        for k, (nm, v, col) in enumerate(((r"RL", 17920, POLICY), (r"on-policy distillation", 1800, REF))):
            bar = Rectangle(width=W * v / 17920, height=0.3, stroke_width=0, fill_color=col, fill_opacity=0.9)
            bar.move_to([x0, -2.45 - 0.45 * k, 0], aligned_edge=LEFT)
            cost.add(VGroup(bar, label(rf"{nm}: \ ${v:,}$".replace(",", "{,}"), font_size=20, color=col)
                            .next_to(bar, RIGHT, buff=0.15)))
        cost[0].move_to([x0, -2.05, 0], aligned_edge=LEFT)
        cite_ = cite(r"Qwen Team, \textit{Qwen3 technical report} (2025)")
        with self.voiceover(
            "By 2025 every stage of this part sat in one pipeline. Here is the one Alibaba published for Qwen3. "
            "<bookmark mark='a'/> A cold start of supervised fine-tuning on long chains of thought; reinforcement "
            "learning on problems with checkable answers; fine-tuning again so the model can answer with or without "
            "thinking; and a final round of reinforcement learning with reward models, for everything that can't "
            "be checked. <bookmark mark='b'/> The smaller models skipped all of it. They were distilled from the "
            "big ones, first on the teacher's text, then on their own text scored by the teacher, the on-policy "
            "distillation of chapter ten. <bookmark mark='c'/> On the eight-billion-parameter model the report compares "
            "the two: seventeen thousand nine hundred and twenty GPU hours of reinforcement learning, against one "
            "thousand eight hundred of distillation, and distillation scored clearly higher."
        ) as vo:
            self.play(FadeIn(big), FadeIn(cite_))
            vo.wait_until("a")
            for k in range(4):
                self.play(FadeIn(boxes[k], shift=RIGHT * 0.1), FadeIn(notes_[k]),
                          *([GrowArrow(arrows[k - 1])] if k else []), run_time=0.8)
            vo.wait_until("b")
            self.play(Create(down), FadeIn(small), FadeIn(dist))
            vo.wait_until("c")
            self.play(FadeIn(cost[0]), GrowFromEdge(cost[1][0], LEFT), FadeIn(cost[1][1]))
            self.play(GrowFromEdge(cost[2][0], LEFT), FadeIn(cost[2][1]))
        self.wait(0.3)
        self.clear_scene()
