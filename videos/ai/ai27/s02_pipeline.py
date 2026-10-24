from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import ASSIST, BASE, GOLD, KLC, PART, POLICY, PROXY, REWARD, USER, bubble, node_box


class Pipeline(VoiceoverScene):
    def construct(self):
        self.card()
        self.predictor()
        self.pipeline()
        self.history()
        self.alignment()

    def card(self):
        card = chapter_card(1, r"From predictor to assistant", r"What turns a text predictor into something you can ask?",
                            lit=(2022,), part=PART)
        with self.voiceover("Chapter one. From predictor to assistant."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def predictor(self):
        q = bubble(r"What is the capital of France?", "user").move_to([-3.2, 2.2, 0])
        base = VGroup(label(r"a pretrained model continues the document:", font_size=22, color=BASE),
                      label(r"``What is the capital of Germany? \ What is the capital of Italy? \ Answers on page 12.''",
                            font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        base.next_to(q, DOWN, buff=0.5).align_to(q, LEFT)
        ans = bubble(r"Paris.", "assistant").move_to([3.4, -1.0, 0])
        al = label(r"an assistant answers", font_size=22, color=ASSIST).next_to(ans, UP, buff=0.2)
        tag = note(r"illustrative").to_corner(DR, buff=0.25)
        obj = MathTex(r"\max_\theta\ \sum_t \log p_\theta(x_t \mid x_{<t})", font_size=34, color=BASE)
        obj.move_to([-3.0, -1.6, 0])
        ol = label(r"pretraining's only goal: \ predict the next token", font_size=20, color=BASE)
        ol.next_to(obj, DOWN, buff=0.15)
        with self.voiceover(
            "A pretrained language model, everything in Parts 13 to 18, has one skill: continuing text. Its only goal "
            "was to predict the next token of documents from the web. <bookmark mark='a'/> So when you ask it a "
            "question, it does what such documents do. A question on the web is often followed by more questions: a "
            "quiz, a list of exercises. <bookmark mark='b'/> What we want is different: an assistant that answers. "
            "The model already knows that Paris is the capital of France. Post-training is the work of getting it "
            "to use what it knows the way we want."
        ) as vo:
            self.play(FadeIn(q), FadeIn(tag), Write(obj), FadeIn(ol))
            vo.wait_until("a")
            self.play(FadeIn(base, shift=DOWN * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(ans, shift=LEFT * 0.2), FadeIn(al))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pipeline(self):
        steps = [
            (r"pretrained model", BASE, r"trillions of tokens of text"),
            (r"supervised fine-tuning", ASSIST, r"$13$k prompts, \\ answers written by people"),
            (r"reward model", PROXY, r"$33$k prompts, \\ answers ranked by people"),
            (r"reinforcement learning", POLICY, r"$31$k prompts, \\ PPO against the reward model"),
        ]
        boxes = VGroup(*[node_box(t, c, font_size=24) for t, c, _ in steps]).arrange(RIGHT, buff=0.9).move_to(UP * 1.2)
        if boxes.width > 13.2:
            boxes.width = 13.2
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
                          for a, b in zip(boxes, boxes[1:])])
        notes = VGroup(*[label(n, font_size=20, color=GREY_A).next_to(b, DOWN, buff=0.3)
                         for (_, _, n), b in zip(steps, boxes)])
        hc = history_card(2022, r"InstructGPT: \ Ouyang et al., OpenAI",
                          r"about $40$ contractors wrote and ranked answers; \ outputs of the $1.3$-billion-parameter "
                          r"InstructGPT were preferred to those of the $175$-billion-parameter GPT-3", width=8.4,
                          color=ASSIST).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The recipe that made ChatGPT was published by OpenAI in March 2022, as InstructGPT. It has three stages "
            "after pretraining. <bookmark mark='a'/> First, supervised fine-tuning: people wrote good answers to "
            "about thirteen thousand prompts, and the model was trained to imitate them. <bookmark mark='b'/> "
            "Second, a reward model: for thirty-three thousand prompts, people ranked several of the model's answers "
            "from best to worst, and a network learned to predict their rankings. <bookmark mark='c'/> Third, "
            "reinforcement learning: the PPO of Part 26, with the reward model standing in for the people. "
            "<bookmark mark='d'/> The result was startling. People preferred the answers of the 1.3-billion-parameter "
            "InstructGPT to those of the 175-billion-parameter GPT-3 it started from: a hundred times smaller, and "
            "better liked, because it was trying to help."
        ) as vo:
            # the whole pipeline faint from the first word, each stage lit as it is named
            ghost = VGroup(boxes[1:], arrows).copy().set_opacity(0.18)
            self.play(FadeIn(boxes[0]), FadeIn(notes[0]), FadeIn(ghost), FadeIn(hc, shift=UP * 0.2))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(GrowArrow(arrows[k]), FadeIn(boxes[k + 1]), FadeIn(notes[k + 1]))
            vo.wait_until("d")
            self.play(Indicate(hc, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(2017, r"Christiano, Leike et al.", r"deep RL from human preferences: \ a simulated robot "
                         r"learns a backflip from about $900$ comparisons of two clips, \ under an hour of a person's "
                         r"time", width=6.5, font_size=24, color=POLICY),
            history_card(2020, r"Stiennon et al.", r"summaries trained on human comparisons are preferred to the "
                         r"human-written reference summaries", width=6.5, font_size=24, color=PROXY),
            history_card(2022, r"InstructGPT, \ then ChatGPT", r"30 November 2022: \ the recipe as a free chat "
                         r"service", width=6.5, font_size=24, color=ASSIST),
            history_card(2023, r"open recipes", r"Llama 2-Chat: \ over a million comparisons, two reward models; "
                         r"\ DPO: \ preferences without a reward model", width=6.5, font_size=24, color=REWARD),
        ).arrange_in_grid(rows=2, cols=2, buff=0.4).move_to(DOWN * 0.15)
        cite_ = cite(r"Christiano et al.\ (2017); \ Stiennon et al.\ (2020); \ Ouyang et al.\ (2022); "
                     r"\ Touvron et al.\ (2023); \ Rafailov et al.\ (2023)")
        # the 2017 experiment in a picture: two clips, one click, many times
        clips = VGroup(*[VGroup(RoundedRectangle(width=1.9, height=1.3, corner_radius=0.1, stroke_color=GREY_B,
                                                 stroke_width=2),
                                label(t, font_size=20, color=GREY_A)) for t in (r"clip A", r"clip B")])
        for c_ in clips:
            c_[1].move_to(c_[0])
        clips.arrange(RIGHT, buff=0.5)
        ask = label(r"which looks more like a backflip?", font_size=22, color=WHITE).next_to(clips, UP, buff=0.3)
        pick = SurroundingRectangle(clips[1][0], color=POLICY, buff=0.08, stroke_width=4)
        times = label(r"$\times\ 900$, \ under an hour", font_size=22, color=POLICY).next_to(clips, DOWN, buff=0.3)
        demo = VGroup(ask, clips, pick, times).move_to(cards[1]).shift(DOWN * 0.6)
        with self.voiceover(
            "The idea is older than chatbots. <bookmark mark='a'/> In 2017, Paul Christiano, Jan Leike and colleagues "
            "at OpenAI and DeepMind taught a simulated robot to do a backflip without ever writing down what a "
            "backflip is. A person was shown two short clips and picked the one that looked more like a backflip, "
            "about nine hundred times, in under an hour; a network learned their preferences, and reinforcement "
            "learning did the rest. <bookmark mark='b'/> In 2020 the same method trained language models to "
            "summarize, and people preferred its summaries to the human-written ones. <bookmark mark='c'/> "
            "InstructGPT followed, and on the thirtieth of November 2022, ChatGPT. <bookmark mark='d'/> Since then the "
            "recipe has been reproduced in the open, and changed: Meta's Llama 2 used over a million comparisons, and "
            "a method called DPO showed the reward model could be skipped altogether."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.15), FadeIn(ask), FadeIn(clips))
            self.play(Create(pick))
            self.play(FadeIn(times))
            vo.wait_until("b")
            self.play(FadeOut(demo), FadeIn(cards[1], shift=UP * 0.15))
            for k, mk in zip((2, 3), "cd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def alignment(self):
        d = definition_card(r"alignment", r"making a model do what the people who build and use it intend: \ helpful, "
                            r"honest and harmless, \ in Anthropic's phrase (Askell et al., 2021)", color=GOLD,
                            width=8.0, font_size=24).move_to(UP * 1.6)
        rows = VGroup(
            label(r"what people want is hard to write down", font_size=28, color=GREY_A),
            label(r"but easy to recognize: \ compare two answers", font_size=28, color=REWARD),
            label(r"so: \ learn the goal from people, \ then optimize it, \ but not too hard", font_size=28,
                  color=KLC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 1.2)
        with self.voiceover(
            "This is what the field calls alignment: making a model do what the people who build and use it intend. "
            "Anthropic's shorthand is helpful, honest and harmless. <bookmark mark='a'/> The difficulty is that what "
            "people want is very hard to write down as a formula. <bookmark mark='b'/> But it is easy to recognize: "
            "show someone two answers, and they can usually say which is better. <bookmark mark='c'/> So the strategy "
            "of this part is to learn the goal from people's judgments, and then optimize it, carefully, because a "
            "learned goal is only an approximation. Each step will be done for real, on the small model this series "
            "trained on thirty novels."
        ) as vo:
            self.play(FadeIn(d, shift=UP * 0.15))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
