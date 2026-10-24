from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import ASSIST, BASE, GOLD, PART, POLICY, PROXY, REWARD, USER, load, said


class Hook(VoiceoverScene):
    def construct(self):
        self.same_model()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def same_model(self):
        d = load("sft")
        topic, base_line = d["base_lines"][0]
        sft_line = next((t for tp, t in d["sft_lines"] if tp == topic), d["sft_lines"][0][1])
        q = said(f"Write a line about the {topic}.", "user", chars=40, font_size=28).move_to([0, 2.5, 0])
        bl = label(r"our model, \ as pretrained", font_size=32, color=BASE).move_to([-3.4, 1.1, 0])
        ba = said(base_line, chars=26, font_size=24, max_lines=6).next_to(bl, DOWN, buff=0.25)
        al = label(r"the same model, \ fine-tuned", font_size=32, color=ASSIST).move_to([3.4, 1.1, 0])
        aa = said(sft_line, chars=26, font_size=24, max_lines=6).next_to(al, DOWN, buff=0.25)
        for b_ in (ba, aa):
            if b_.width > 6.4:
                b_.width = 6.4
        same = label(r"same weights, \ same knowledge: \ a few minutes of training apart", font_size=24, color=GOLD)
        same.to_edge(DOWN, buff=0.75)
        tag = note(r"computed: \ the series' $6.8$-million-parameter model, \ trained on thirty novels")
        tag.to_corner(DR, buff=0.2)
        with self.voiceover(
            "This is the small language model this series trained on thirty novels, asked to write a line about the "
            f"{topic}. <bookmark mark='a'/> As it comes out of pretraining, it doesn't answer. It continues a "
            "document: the request is just more text, and the special markers around it mean nothing to it. "
            "<bookmark mark='b'/> Here is the same model after a few minutes of fine-tuning on this computer. "
            "<bookmark mark='c'/> It knows nothing new. What changed is what it does with what it knows."
        ) as vo:
            self.play(FadeIn(q), FadeIn(tag), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(ba))
            vo.wait_until("b")
            self.play(FadeIn(al), FadeIn(aa))
            vo.wait_until("c")
            self.play(FadeIn(same))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        q = label(r"How does a model that predicts text \\ become an assistant that tries to help?", font_size=40)
        q.move_to(UP * 1.4)
        fact = history_card(2022, r"InstructGPT", r"people preferred the answers of a $1.3$-billion-parameter model "
                            r"after this training \ to those of the $175$-billion-parameter GPT-3 before it",
                            width=8.6, color=ASSIST).move_to(DOWN * 1.2)
        with self.voiceover(
            "That change, from predicting text to trying to help, is called post-training, and it is how every "
            "chatbot you have used was made. <bookmark mark='a'/> It matters more than size. In 2022 OpenAI found "
            "that people preferred the answers of a 1.3-billion-parameter model after post-training to those of the "
            "175-billion-parameter GPT-3 before it."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(fact, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Post-Training and Alignment", font_size=44).to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.6)
        obj = objectives_card([
            r"supervised fine-tuning and chat templates; \ LoRA and why it works",
            r"reward models: \ Bradley--Terry, \ Elo again; \ what ours actually learned",
            r"RLHF, its exact optimum, \ PPO for language models; \ Goodhart's law, \ measured",
            r"DPO and its family; \ feedback from AI, \ constitutions",
            r"distillation and model merging",
            r"what goes wrong: \ sycophancy, \ jailbreaks, \ emergent misalignment",
        ], font_size=26)
        with self.voiceover(
            "This is Part 27 of AI, Built. <bookmark mark='a'/> In this part: supervised fine-tuning and low-rank "
            "adapters; reward models learned from comparisons, and what ours actually learned; reinforcement "
            "learning from human feedback, its exact optimum, how PPO is fitted to a language model, and what "
            "happens when you optimize a learned reward too hard; direct preference optimization; feedback from AI "
            "under written principles; distillation and model merging; and what goes wrong. Every method runs here, "
            "on our own small model."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.3)
        self.clear_scene()
