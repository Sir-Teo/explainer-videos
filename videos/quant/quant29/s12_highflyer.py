from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import FORMULA, HURDLE, PART


class HighFlyer(VoiceoverScene):
    def construct(self):
        self.card()
        self.story()
        self.meaning()
        self.question()

    def card(self):
        c = chapter_card(11, r"From a quant fund to DeepSeek", r"What does an alpha factory have in common with a "
                         r"language-model lab?", part=PART)
        with self.voiceover("Chapter eleven. The most famous outcome of China's quant boom was not a fund at all. What "
                            "does an alpha factory have in common with a language-model lab?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def story(self):
        steps = [(r"c.\ 2015--16", r"Liang Wenfeng and partners found High-Flyer (幻方), a quantitative fund using machine "
                                   r"learning to trade Chinese stocks"),
                 (r"2019--2021", r"High-Flyer builds its own GPU clusters, Fire-Flyer I and II, to train its trading "
                                 r"models: thousands of Nvidia GPUs, as reported"),
                 (r"2023", r"Liang launches DeepSeek, a language-model lab funded by High-Flyer"),
                 (r"2024--25", r"DeepSeek's V3 and R1 models, open weights at a reported fraction of rivals' training "
                               r"cost, shake technology stocks worldwide (the AI series, Parts 14 and 16)")]
        rows = VGroup()
        for when, what in steps:
            r_ = VGroup(label(when, font_size=22, color=HURDLE), wrapped_label(what, 9.6, 19, GREY_A)).arrange(RIGHT, buff=0.5,
                                                                                                          aligned_edge=UP)
            rows.add(r_)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(DOWN * 0.1)
        for r_ in rows:
            r_[1].align_to(rows, LEFT).shift(RIGHT * 2.6)
        src = note(r"public record: company statements and press reports (Reuters, Bloomberg); dates and GPU counts vary "
                   r"by source", font_size=15, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "From the public record. <bookmark mark='a'/> Around 2015, Liang Wenfeng and his partners founded "
            "High-Flyer, a quantitative fund that traded Chinese stocks with machine learning. <bookmark mark='b'/> To "
            "train its models it built its own computing clusters, Fire-Flyer one and two, with thousands of Nvidia "
            "graphics processors by 2021, as reported. <bookmark mark='c'/> In 2023 Liang launched DeepSeek, a "
            "language-model lab funded by the fund. <bookmark mark='d'/> Its V3 and R1 models, with open weights and a "
            "reported fraction of rivals' training costs, shook technology markets in early 2025: the story the AI "
            "series tells in Parts fourteen and sixteen."
        ) as vo:
            self.play(FadeIn(src))
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def meaning(self):
        cards = VGroup(
            desk_question(r"the same machine", r"an alpha factory is a pipeline: data, compute, a search, an evaluation "
                          r"that cannot be fooled, and a library that grows. So is a model lab", width=12.4, font_size=19),
            desk_question(r"the same scarcity", r"in both, the scarce input is not ideas but compute, clean data and "
                          r"honest evaluation", width=12.4, font_size=19),
            desk_question(r"a different market", r"a trading signal decays as others find it; a published model does not "
                          r"stop working when others use it", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why the same firm could do both. <bookmark mark='a'/> An alpha factory is a pipeline: data, compute, a search, "
            "an evaluation that cannot be fooled, and a library that grows. A model lab is the same pipeline. "
            "<bookmark mark='b'/> In both, the scarce input is not ideas but compute, clean data and honest evaluation. "
            "<bookmark mark='c'/> The difference is the market: a trading signal decays as others find it, while a "
            "published model keeps working when others use it."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"why might a fund that trades on machine-learned signals give away its best language model, "
                       r"but never its best signal?")
        with self.voiceover(
            "Pause and predict. Why might a fund that trades on machine-learned signals give away its best language "
            "model, but never its best signal?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
