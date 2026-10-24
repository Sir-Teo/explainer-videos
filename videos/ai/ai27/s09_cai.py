from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import ASSIST, GOLD, PART, POLICY, PROXY, REWARD, USER, bubble, load, node_box


class Constitution(VoiceoverScene):
    def construct(self):
        self.card()
        self.critique()
        self.rlaif()
        self.ours()
        self.specs()

    def card(self):
        card = chapter_card(9, r"Feedback from AI, rules from people", r"Can a model help judge itself?",
                            lit=(2022,), part=PART)
        with self.voiceover("Chapter nine. Feedback from AI, rules from people."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def critique(self):
        steps = VGroup(
            node_box(r"1. \ answer a hard request", ASSIST, font_size=24),
            node_box(r"2. \ critique the answer \\ against a principle", PROXY, font_size=24),
            node_box(r"3. \ revise it", POLICY, font_size=24),
            node_box(r"4. \ fine-tune on the revisions", REWARD, font_size=24),
        ).arrange(DOWN, buff=0.45).move_to([-3.6, 0.0, 0])
        arrows = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.08, color=GREY_B, stroke_width=3)
                          for a, b in zip(steps, steps[1:])])
        principle = VGroup(label(r"a principle from the constitution:", font_size=22, color=GREY_A),
                           label(r"``Choose the response that is least \\ harmful, \ without being preachy \\ or "
                                 r"evasive.''", font_size=24, color=GOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        principle.move_to([3.2, 1.4, 0])
        hc = history_card(2022, r"Constitutional AI \ (Bai et al., Anthropic)", r"harmlessness from AI feedback: \ "
                          r"a short list of principles written by people replaces most human labels of harm",
                          width=6.2, color=GOLD).move_to([3.2, -1.4, 0])
        tag = note(r"paraphrased").next_to(principle, DOWN, buff=0.1).align_to(principle, RIGHT)
        with self.voiceover(
            "Human comparisons are slow and expensive, and some are unpleasant: someone has to read the harmful "
            "answers to rank them. In December 2022 Anthropic published Constitutional AI, which moves much of that "
            "work to the model itself, guided by a short list of principles written by people: a constitution. "
            "<bookmark mark='a'/> First, a supervised phase. The model answers a difficult request. "
            "<bookmark mark='b'/> Then it is asked to critique its own answer against a principle, for instance to "
            "choose the response that is least harmful without being preachy or evasive. <bookmark mark='c'/> It "
            "rewrites the answer in light of the critique. <bookmark mark='d'/> And it is fine-tuned on the revised "
            "answers. The people's work went into the principles, not into each label."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(principle), FadeIn(tag))
            self.play(FadeIn(steps[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(arrows[k]), FadeIn(steps[k + 1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rlaif(self):
        loop = VGroup(
            node_box(r"two answers", ASSIST, font_size=24),
            node_box(r"an AI judge, \\ reading the principles", PROXY, font_size=24),
            node_box(r"a comparison", REWARD, font_size=24),
            node_box(r"reward model, \ RL", POLICY, font_size=24),
        ).arrange(RIGHT, buff=0.7).move_to(UP * 1.4)
        if loop.width > 13:
            loop.width = 13
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=3)
                          for a, b in zip(loop, loop[1:])])
        cards = VGroup(
            history_card(2022, r"RLAIF \ (Constitutional AI, \ phase 2)", r"the model compares pairs of answers "
                         r"against the principles; \ RL as before", width=6.0, color=PROXY),
            history_card(2023, r"Lee et al., Google", r"on summarization and dialogue, \ AI feedback did about as well "
                         r"as human feedback", width=6.0, color=REWARD),
        ).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The second phase replaces human comparisons too. <bookmark mark='a'/> Two answers are shown to an AI "
            "judge, a language model given the principles, which says which one better follows them. Those "
            "comparisons train the reward model, and reinforcement learning proceeds as in chapter six. This is "
            "reinforcement learning from AI feedback, RLAIF. <bookmark mark='b'/> In 2023 a team at Google compared "
            "the two directly, and on summarization and dialogue AI feedback did about as well as human feedback. "
            "Today most comparisons in post-training are judged by models, with people writing the rules and "
            "checking the judges."
        ) as vo:
            self.play(FadeIn(loop[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(arrows[k]), FadeIn(loop[k + 1])) for k in range(3)],
                                  lag_ratio=0.5), run_time=2.5)
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        d = load("rlaif")
        ceil = float(load("rm")["people_agree_gold"])
        vals = [float(d["acc_small"]), float(d["acc_ai"]), float(d["acc_full"])]
        names = [rf"${d['n_human']}$ human comparisons",
                 r"$+\," + f"{d['n_ai']:,}".replace(",", "{,}") + r"$ labelled by that model",
                 rf"${d['n_ai']:,}$ human comparisons".replace(",", "{,}")]
        cols = [REWARD, PROXY, REWARD]
        hi = max(0.8, float(np.ceil(max(vals + [ceil]) * 20) / 20))
        g = axes([0.5, hi], [0, 3], x_length=6.2, y_length=3.6, xlabel=r"accuracy on held-out human comparisons",
                 xticks=[v for v in (0.5, 0.6, 0.7, 0.8) if v <= hi], xfmt=lambda v: rf"{100 * v:.0f}\%",
                 center=[2.6, 0.1, 0])
        ax = g.ax
        rows = VGroup()
        for k, (nm, v, col) in enumerate(zip(names, vals, cols)):
            y = 2.5 - k
            bar = Rectangle(width=max(ax.c2p(v, y)[0] - ax.c2p(0.5, y)[0], 0.02), height=0.5, stroke_width=0,
                            fill_color=col, fill_opacity=0.85).move_to(ax.c2p(0.5, y), aligned_edge=LEFT)
            name = label(nm, font_size=24, color=col).next_to(ax.c2p(0.5, y), LEFT, buff=0.3)
            val = MathTex(rf"{100 * v:.0f}\%", font_size=28, color=col).next_to(bar, RIGHT, buff=0.15)
            rows.add(VGroup(name, bar, val))
        cl = DashedLine(ax.c2p(ceil, 0), ax.c2p(ceil, 3), color=GOLD, dash_length=0.08)
        cll = label(rf"the people agree with gold: \ ${100 * ceil:.0f}\%$", font_size=20, color=GOLD)
        cll.next_to(ax.c2p(ceil, 3), UP, buff=0.12)
        head = VGroup(g, cl, cll)
        tag = note(r"computed: \ our reward models; \ the AI judge here is the small reward model itself")
        tag.to_corner(DR, buff=0.2)
        gain = d["acc_ai"] - d["acc_small"]
        if gain > 0.01:
            verdict = (f"Training on the judge's own labels helps a little, from {100 * d['acc_small']:.0f} to "
                       f"{100 * d['acc_ai']:.0f} percent: the labels are smoother than the noisy people, and there are "
                       "more of them. But it can't learn what the judge never knew.")
        else:
            verdict = (f"Training on the judge's own labels doesn't help here: {100 * d['acc_ai']:.0f} percent, "
                       f"against {100 * d['acc_small']:.0f}. A judge can't teach what it never knew; real AI judges "
                       "help because they are much larger models than the ones they judge.")
        with self.voiceover(
            "A small version of the idea, on our model. <bookmark mark='a'/> Train a reward model on just "
            f"{d['n_human']} human comparisons. <bookmark mark='b'/> Use it as the judge: let it label "
            f"{d['n_ai']:,} new comparisons, and train a fresh reward model on those. " + verdict +
            f" <bookmark mark='c'/> For reference, {d['n_ai']:,} real comparisons give {100 * d['acc_full']:.0f} "
            "percent."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), Create(cl), FadeIn(cll))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k][0]), GrowFromEdge(rows[k][1], LEFT), FadeIn(rows[k][2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def specs(self):
        cards = VGroup(
            history_card(2023, r"Claude's constitution", r"a published list of principles used in training", width=6.0,
                         color=GOLD),
            history_card(2024, r"OpenAI's Model Spec; \ deliberative alignment", r"the model is taught the written "
                         r"policy and reasons about it before answering", width=6.0, color=PROXY),
            history_card(2026, r"Claude's new constitution", r"explains the reasons behind its priorities: \ broadly "
                         r"safe, \ broadly ethical, \ following Anthropic's guidelines, \ genuinely helpful; \ public "
                         r"domain", width=6.0, color=GOLD),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.1)
        cite_ = cite(r"Anthropic (2023, 2026); \ OpenAI (2024); \ Guan et al., \textit{Deliberative alignment} (2024)")
        with self.voiceover(
            "The constitutions themselves became public documents. <bookmark mark='a'/> Anthropic published Claude's "
            "principles in 2023. <bookmark mark='b'/> In 2024 OpenAI published a Model Spec, and trained its "
            "reasoning models to read the relevant policy in their chain of thought before answering, which it "
            "called deliberative alignment. <bookmark mark='c'/> In January 2026 Anthropic replaced its list of "
            "principles with a long document explaining the reasons behind them, with explicit priorities: broadly "
            "safe, broadly ethical, following Anthropic's guidelines, and genuinely helpful. The rules are written by "
            "people, in plain language, and the training makes the model use them."
        ) as vo:
            self.play(FadeIn(cite_))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
