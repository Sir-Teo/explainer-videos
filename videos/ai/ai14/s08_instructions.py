from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (CONTEXT, DECODER, ENCDEC, MONO, PART, PRIOR, F, bars_h, node_box, said, take_away)

ASSIST = C.ASSISTANT


class Instructions(VoiceoverScene):
    def construct(self):
        self.card()
        self.codex()
        self.instruction_tuning()
        self.instructgpt()

    def card(self):
        card = chapter_card(7, r"Code, and following instructions", r"How did a text predictor learn to do what it is "
                            r"asked?", lit=(2021, 2022), part=PART)
        with self.voiceover("Chapter seven. Code, and following instructions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def codex(self):
        X = F.CODEX
        code = code_block(['def is_prime(n):', '    """Return true if a given number is prime,',
                           '    and false otherwise.', '    >>> is_prime(6)', '    False',
                           '    >>> is_prime(101)', '    True', '    """'], font_size=17, color=WHITE)
        frame = SurroundingRectangle(code, color=GREY_C, buff=0.25, corner_radius=0.1)
        prob = VGroup(frame, code)
        if prob.width > 5.8:
            prob.width = 5.8
        prob.move_to([-3.7, 0.2, 0])
        pl = label(rf"HumanEval: \ ${X['problems']}$ problems like this one, \\ checked by unit tests", font_size=22,
                   color=GREY_A).next_to(prob, DOWN, buff=0.3)
        hc = history_card(2021, r"Codex \ (Chen et al.; OpenAI)", rf"GPT fine-tuned on ${X['gb']}$ GB of Python from "
                          rf"${X['repos'] / 1e6:.0f}$ million GitHub repositories; \ it powered GitHub Copilot",
                          width=6.2, color=DECODER).move_to([3.6, 2.4, 0])
        items = [(r"GPT-3", X["gpt3"], PRIOR), (r"GPT-J, \ 6B", X["gptj"], PRIOR),
                 (r"Codex, \ 12B, \ first try", X["pass1"], DECODER),
                 (r"Codex, \ best of $100$ samples", X["pass100"], C.REWARD)]
        bars = bars_h(items, 100, width=3.6, font_size=20, label_width=2.6, fmt=lambda v: rf"{v:g}\%")
        bars.move_to([3.6, -0.6, 0])
        bt = label(r"problems solved", font_size=22, color=WHITE).next_to(bars, UP, buff=0.25)
        tag = note(r"a HumanEval problem, \ from Chen et al.\ (2021)").to_corner(DL, buff=0.2)
        with self.voiceover(
            "July 2021. Mark Chen and colleagues at OpenAI fine-tuned GPT models on code: 159 gigabytes of Python, "
            "from 54 million public GitHub repositories. The result, Codex, powered the first GitHub Copilot. "
            "<bookmark mark='a'/> To measure it, they wrote HumanEval: 164 programming problems, each a function "
            "signature and a description, checked by hidden unit tests. A program counts only if it passes. "
            f"<bookmark mark='b'/> GPT-3 solved none of them. GPT-J, an open model of six billion parameters, "
            f"{X['gptj']} percent. <bookmark mark='c'/> Codex, with twelve billion parameters, solved {X['pass1']} "
            f"percent on its first try, <bookmark mark='d'/> and {X['pass100']} percent when it could write a hundred "
            "programs and the tests picked any that worked. Sampling many answers and checking them comes back, as a "
            "way of thinking, in Part 28."
        ) as vo:
            self.play(FadeIn(hc, shift=DOWN * 0.1), FadeIn(prob))
            vo.wait_until("a")
            self.play(FadeIn(pl), FadeIn(tag), Indicate(prob, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(bt), *[FadeIn(r) for r in bars[:2]])
            vo.wait_until("c")
            self.play(FadeIn(bars[2][0]), GrowFromEdge(bars[2][1], LEFT), FadeIn(bars[2][2]))
            vo.wait_until("d")
            self.play(FadeIn(bars[3][0]), GrowFromEdge(bars[3][1], LEFT), FadeIn(bars[3][2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def instruction_tuning(self):
        FL, T0 = F.FLAN, F.T0
        temps = VGroup(said("Translate this sentence to Spanish: ...", chars=40, font_size=18, box_color=ASSIST),
                       said("Is the sentiment of this review positive or negative? ...", chars=40, font_size=18,
                            box_color=ASSIST),
                       said("Does the premise entail the hypothesis? Options: yes, no", chars=40, font_size=18,
                            box_color=ASSIST))
        temps.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.5, 1.6, 0])
        tl = label(r"existing datasets, \ rewritten as instructions", font_size=22, color=ASSIST)
        tl.next_to(temps, UP, buff=0.25)
        # clusters of task types: train on all but one, test on the held-out type
        names = [r"translation", r"sentiment", r"summaries", r"commonsense", r"QA", r"inference"]
        cl = VGroup(*[node_box(n, ASSIST if n != r"inference" else C.SURPRISE, font_size=18) for n in names])
        cl.arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.25)).move_to([-3.5, -1.0, 0])
        held = label(r"held out: \ a whole type of task \ (schematic)", font_size=20, color=C.SURPRISE).next_to(cl, DOWN, buff=0.2)
        cards = VGroup(
            history_card(2021, r"FLAN \ (Wei et al.; Google)", rf"a ${FL['params'] / 1e9:.0f}$B language model, "
                         rf"instruction-tuned on over ${FL['datasets']}$ datasets: \ zero-shot, it beat zero-shot GPT-3 "
                         rf"on ${FL['won']}$ of ${FL['of']}$", width=6.2, color=ASSIST),
            history_card(2021, r"T0 \ (Sanh et al.; BigScience)", rf"T5, ${T0['params'] / 1e9:.0f}$B, trained on many "
                         rf"prompted tasks: \ matched or beat GPT-3 on ${T0['won']}$ of ${T0['of']}$ held-out datasets, "
                         rf"\ ${T0['smaller']}\times$ smaller", width=6.2, color=ENCDEC),
        ).arrange(DOWN, buff=0.35).move_to([3.4, 0.4, 0])
        tw = take_away(r"instruction tuning teaches the form of a request, \ and it carries over to new tasks",
                       color=ASSIST, font_size=26)
        with self.voiceover(
            "Meanwhile, two groups asked whether a model could learn to follow instructions in general. "
            "<bookmark mark='a'/> In September 2021, Jason Wei and colleagues at Google took a language model of 137 "
            "billion parameters and fine-tuned it on more than sixty existing datasets, each rewritten as "
            "instructions in plain English. <bookmark mark='b'/> To test it fairly, they grouped tasks by type and "
            "held out a whole type at a time: a model tested on inference had never been tuned on any inference task. "
            "<bookmark mark='c'/> Their model, FLAN, beat zero-shot GPT-3 on twenty of twenty-five datasets. "
            "<bookmark mark='d'/> A month later Victor Sanh and a large BigScience team did the same with T5. Their "
            "T0, eleven billion parameters, matched or beat GPT-3 on nine of eleven held-out datasets, while sixteen "
            "times smaller. <bookmark mark='e'/> Instruction tuning teaches the form of being asked, and the form "
            "carries over to tasks the model has never seen."
        ) as vo:
            self.play(FadeIn(tl), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in temps], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(Indicate(temps, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(cl), FadeIn(held))
            vo.wait_until("c")
            self.play(FadeIn(cards[0], shift=LEFT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(cards[1], shift=LEFT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def instructgpt(self):
        I = F.INSTRUCTGPT
        steps = [(r"pretrained GPT-3", GREY_B, r"text from the web"),
                 (r"supervised fine-tuning", ASSIST, rf"${I['sft'] // 1000}$k prompts, \\ answers written by people"),
                 (r"reward model", C.MODEL_Q, rf"${I['rm'] // 1000}$k prompts, \\ answers ranked by people"),
                 (r"reinforcement learning", C.RL_POLICY, rf"${I['ppo'] // 1000}$k prompts, \\ PPO on the reward")]
        boxes = VGroup(*[node_box(t, c, font_size=24) for t, c, _ in steps]).arrange(RIGHT, buff=0.8).move_to(UP * 1.4)
        if boxes.width > 13.2:
            boxes.width = 13.2
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=3)
                          for a, b in zip(boxes, boxes[1:])])
        notes = VGroup(*[label(n, font_size=20, color=GREY_A).next_to(b, DOWN, buff=0.3) for (_, _, n), b in
                         zip(steps, boxes)])
        hc = history_card(2022, r"InstructGPT \ (Ouyang et al.; OpenAI)",
                          rf"people preferred the answers of the ${I['small'] / 1e9:.1f}$-billion-parameter model to "
                          rf"those of the ${I['big'] / 1e9:.0f}$-billion-parameter GPT-3", width=8.6,
                          color=ASSIST).move_to(DOWN * 1.5)
        nxt = label(r"every stage, \ built on our own model: \ Part 27", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Instruction tuning used existing datasets. OpenAI's InstructGPT, published in March 2022, used people. "
            "<bookmark mark='a'/> Labellers wrote good answers to about thirteen thousand prompts, and GPT-3 was "
            "fine-tuned to imitate them. <bookmark mark='b'/> They ranked the model's answers to thirty-three thousand "
            "prompts, and a reward model learned their preferences. <bookmark mark='c'/> Then reinforcement learning "
            "pushed the model toward answers the reward model liked, on thirty-one thousand more prompts. "
            "<bookmark mark='d'/> People preferred the answers of the 1.3-billion-parameter InstructGPT to those of the "
            "175-billion-parameter GPT-3. Every one of these stages is built, on our own model, in Part 27."
        ) as vo:
            self.play(FadeIn(boxes[0]), FadeIn(notes[0]))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(GrowArrow(arrows[k]), FadeIn(boxes[k + 1]), FadeIn(notes[k + 1]))
            vo.wait_until("d")
            self.play(FadeIn(hc, shift=UP * 0.15), FadeIn(nxt))
        self.wait(0.3)
        self.clear_scene()
