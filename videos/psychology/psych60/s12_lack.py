from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403


class Lack(VoiceoverScene):
    def construct(self):
        card_section(self, 11, r"What machines lack, \ and have", r"What would a child-like learner need?",
                     scale=("person",))
        self.lake()
        self.data()
        self.conscious()

    def lake(self):
        chips_section(self, r"Building machines that learn and think like people", [
            (r"Lake and colleagues, \ 2017", r"people learn new concepts from one or a few examples, \ build causal "
                                            r"models, \ and use intuitive physics and psychology from infancy", MODEL),
            (r"developmental benchmarks", r"tests of object permanence, \ number and agency (Part 30) given to "
                                          r"models", PERSON),
            (r"child-scale learning", r"models trained on a child's amount of language, \ or on video from a "
                                      r"head-mounted camera on one child", GOOD),
            (r"so far", r"models trained this way learn some words and categories; \ much of the gap remains", AUTH),
        ], "What would a child-like learner need? <bookmark mark='a'/> In 2017 Brenden Lake and colleagues argued "
           "that people learn new concepts from one or a few examples, build causal models, and use intuitive "
           "physics and psychology from infancy. <bookmark mark='b'/> Developmental benchmarks now give models "
           "Part 30's tests of object permanence, number and agency. <bookmark mark='c'/> Child-scale learning trains "
           "models on a child's amount of language, or on video from a head-mounted camera on one child. "
           "<bookmark mark='d'/> So far, models trained this way learn some words and categories, and much of the gap "
           "remains.", tag=published_tag(r"Lake et al.\ (2017)"), chip_w=4.0, text_w=8.0)

    def conscious(self):
        rows_section(self, r"Part 27's question, \ asked of machines", [
            (r"the theories of Part 27 (global workspace, \ higher-order, \ recurrent processing) each name "
             r"functions a system would need", WHITE),
            (r"one approach checks a system's architecture against those indicators, \ theory by theory", MODEL),
            (r"behaviour alone cannot settle it: \ a system trained on human text will describe experience whether "
             r"or not it has any", AUTH),
            (r"the question is open, \ and both kinds of mistake (attributing too much, \ or too little) have costs",
             YOU),
        ], "Part 27 left a question open. Here it is, asked of machines. <bookmark mark='a'/> The theories of Part "
           "27, global workspace, higher-order and recurrent processing, each name functions a system would need. "
           "<bookmark mark='b'/> One approach checks a system's architecture against those indicators, theory by "
           "theory. <bookmark mark='c'/> Behaviour alone can't settle it: a system trained on human text will "
           "describe experience whether or not it has any. <bookmark mark='d'/> The question is open, and both kinds "
           "of mistake, attributing too much or too little, have costs.")

    def data(self):
        rows_section(self, r"The data gap", [
            (r"a child hears on the order of millions of words a year, \ and speaks fluently by school age", WHITE),
            (r"large language models are trained on trillions of words: \ several orders of magnitude more "
             r"(Frank, \ 2023, \ on the gap)", AUTH),
            (r"so a model's fluency is not evidence of a child's learning mechanism; \ the child brings more prior "
             r"structure, \ or learns from richer input (sight, \ touch, \ other people), \ or both", MODEL),
            (r"the open experiment: \ train models on what one child could have heard and seen, \ and ask what they "
             r"learn", GOOD),
        ], "There's also a data gap. <bookmark mark='a'/> A child hears on the order of millions of words a year, and "
           "speaks fluently by school age. <bookmark mark='b'/> Large language models are trained on trillions of "
           "words, several orders of magnitude more. Michael Frank set out the gap in 2023. <bookmark mark='c'/> So "
           "a model's fluency isn't evidence of a child's learning mechanism. The child brings more prior structure, "
           "or learns from richer input, sight, touch and other people, or both. <bookmark mark='d'/> The open "
           "experiment is to train models on what one child could have heard and seen, and ask what they learn.")
