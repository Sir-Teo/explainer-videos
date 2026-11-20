from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ micro data, \ embeddings, \ instruments", r"What is still being worked out?",
             "Chapter fifteen. Frontier: micro data, embeddings, instruments.",
             lit={2004: r"Berry, \ Levinsohn and Pakes", 2021: r"Berry and Haile"}, scale=("market",),
             horizon=("a decade",))
        self.open()
        self.recipe()

    def open(self):
        cards = point_cards([
            (r"who buys what", r"surveys of buyers, \\ loyalty cards and \\ second choices pin \\ down how tastes \\ "
                               r"differ", DEMAND),
            (r"learned characteristics", r"product traits learned \\ from text, \ images \\ and baskets, \\ not "
                                         r"listed by \\ the economist", BLP_C),
            (r"instruments", r"weak instruments \\ give confident, \\ wrong answers; \\ crowding measures \\ help",
             IV_C),
            (r"identification", r"what can be learned \\ from market data \\ alone, \ and what \\ only from "
                                r"assumptions", HOLD),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"open questions", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.FRONTIER43.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Four frontiers. <bookmark mark='a'/> Who buys what. Market shares alone leave how tastes differ hard "
            "to pin down. In 2004 Berry, Levinsohn and Pakes added surveys of car buyers, including the car each "
            "would have bought instead, and today loyalty-card and online data record individual choices by the "
            "billion. <bookmark mark='b'/> Learned characteristics. The economist used to list a product's "
            "characteristics, size and power and air conditioning. Researchers now learn them from product "
            "descriptions, images and which products shoppers buy together, with the methods of machine learning, "
            "and ask whether substitution follows the learned traits. <bookmark mark='c'/> Instruments. Weak "
            "instruments give confident, wrong answers, and Gandhi and Houde's measures of how crowded a product's "
            "neighbourhood is have become a standard remedy, alongside careful software and best practice for the "
            "estimator itself. <bookmark mark='d'/> Identification. Berry and Philip Haile have spent more than a "
            "decade asking which features of demand market data can reveal without assuming a functional form, "
            "and which only the assumptions supply."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def recipe(self):
        steps = flow_chain([(r"the question", E.ACCENT), (r"the data", DATA), (r"demand", DEMAND),
                            (r"conduct", PRICE), (r"the answer", GAIN)],
                           notes=[r"a merger, \ a new \\ product, \ a tax", r"prices, \ shares, \\ traits, \ micro "
                                  r"data", r"logit, \ nests, \\ random coefficients", r"how firms \\ compete",
                                  r"with its \\ uncertainty"], box_w=2.2, font_size=19, note_size=15).move_to(UP * 0.5)
        foot = label(r"every arrow is an assumption that can be tested on an Island where the truth is known",
                     font_size=21, color=GREY_A).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "The whole field fits one chain. <bookmark mark='a'/> Start from a question: a merger, a new product, a "
            "tax. <bookmark mark='b'/> Gather prices, shares, characteristics and, if possible, data on individual "
            "buyers. <bookmark mark='c'/> Estimate demand, with as much flexibility as the data can support. "
            "<bookmark mark='d'/> Add a model of how firms compete. <bookmark mark='e'/> Report the answer with its "
            "uncertainty. <bookmark mark='f'/> Every arrow is an assumption, and every one can be tested where the "
            "truth is known, as this part tested them on the Island."
        ) as vo:
            self.play(FadeIn(steps.boxes[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps.notes[0]))
            for k, mk in zip(range(4), "bcde"):
                vo.wait_until(mk)
                self.play(GrowArrow(steps.arrows[k]), FadeIn(steps.boxes[k + 1]), FadeIn(steps.notes[k + 1]))
            vo.wait_until("f")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
