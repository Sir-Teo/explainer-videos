from __future__ import annotations

import numpy as np

from videos.music.music42.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ judging creativity", r"How would we know if a machine were creative?")
        self.boden()
        self.mapped()
        self.evaluation()
        self.cocreative()
        self.problem()

    # ------------------------------------------------------------------
    def boden(self):
        items = [
            (r"Margaret Boden, \ \textit{The Creative Mind} \ (1990): \ creativity makes ideas that are new, \ surprising and valuable", WHITE),
            (r"combinational: \ unfamiliar combinations of familiar ideas", WHITE),
            (r"exploratory: \ moving within a structured space of possibilities, \ finding what it allows", WHITE),
            (r"transformational: \ changing the space itself, \ so that ideas impossible before become possible", TUNE),
            (r"new to the person \ (P-creative) \ or new in history \ (H-creative)", GREY_A),
        ]
        rows_scene(self, r"three kinds of creativity", items,
                   "Is any of this creative? The most cited framework is Margaret Boden's, from The Creative Mind of 1990: "
                   "creativity makes ideas that are new, surprising and valuable. <bookmark mark='b'/> It can be combinational, "
                   "putting familiar ideas together in unfamiliar ways; <bookmark mark='c'/> exploratory, moving within a "
                   "structured space of possibilities to find what it allows; <bookmark mark='d'/> or transformational, changing "
                   "the space itself, so that ideas impossible before become possible. <bookmark mark='e'/> And an idea can be "
                   "new to the one who has it, or new in history.", marks="bcde")

    # ------------------------------------------------------------------
    def mapped(self):
        rows_ = VGroup()
        table = [(r"combinational", r"the dice game; \ Cope's recombination; \ the order-4 chain"),
                 (r"exploratory", r"the Illiac rules; \ our searcher and its critics; \ evolution"),
                 (r"transformational", r"none of ours: \ every program here keeps its rules fixed"),
                 (r"historical examples", r"tonality loosened \ (Part 29); \ the sampler as an instrument \ (Part 40)")]
        for i, (a, b) in enumerate(table):
            y = 1.5 - 1.0 * i
            rows_.add(VGroup(label(a, font_size=21, color=EAR if a == "transformational" else TUNE).move_to([-6.0, y, 0], aligned_edge=LEFT),
                             label(b, font_size=19, color=WHITE).move_to([-2.4, y, 0], aligned_edge=LEFT)))
        rows_.scale_to_fit_width(min(rows_.width, 12.6)).move_to(DOWN * 0.1)
        head = label(r"this part's programs, \ in Boden's terms", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Place this part's programs in Boden's terms. <bookmark mark='a'/> The dice game, Cope's recombination and the "
            "order-four chain are combinational. <bookmark mark='b'/> The Illiac rules, our searcher and evolution are "
            "exploratory: they search a space someone else defined. <bookmark mark='c'/> None of ours is transformational: "
            "every program here keeps its rules fixed. <bookmark mark='d'/> History's transformations, like tonality "
            "loosened or the sampler turned into an instrument, changed what counted as music."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.15)))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def evaluation(self):
        items = [
            (r"`could a listener tell?' \ is a weak test: \ it rewards imitation, \ and depends on who listens", WHITE),
            (r"Ritchie \ (2007): \ score outputs for novelty, \ typicality and quality, \ and compare with what the system was shown", WHITE),
            (r"Jordanous \ (2012): \ evaluate against a definition of creativity chosen in advance, \ component by component", WHITE),
            (r"Pearce and Wiggins: \ test a style model's outputs with expert listeners, \ and say what each judgement means", TUNE),
            (r"copying must be measured too: \ chapter 8's longest copied run is a start", GREY_A),
        ]
        rows_scene(self, r"evaluating computational creativity", items,
                   "How should a machine's music be judged? <bookmark mark='b'/> Could a listener tell it from a human's? That "
                   "is a weak test: it rewards imitation, and the answer depends on who listens. <bookmark mark='c'/> Graeme "
                   "Ritchie proposed scoring outputs for novelty, typicality and quality, compared with what the system was "
                   "shown. <bookmark mark='d'/> Anna Jordanous proposed fixing a definition of creativity in advance and "
                   "evaluating against it, component by component. <bookmark mark='e'/> Marcus Pearce and Geraint Wiggins tested "
                   "style models' outputs with expert listeners, and asked what each judgement actually measures. "
                   "<bookmark mark='f'/> And copying has to be measured too; chapter eight's longest copied run is a start.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def cocreative(self):
        items = [
            (r"tools that compose with a person: \ suggest a continuation, \ fill a gap, \ harmonise a line", WHITE),
            (r"Google's Bach Doodle \ (2019): \ a model harmonised millions of melodies typed in by visitors", WHITE),
            (r"Sturm and colleagues' folk-rnn \ (2016) \ trained on folk tunes; \ musicians played and edited its output", WHITE),
            (r"studies ask what helps a composer: \ control, \ steering by examples, \ and being surprised", TUNE),
            (r"Part 65 builds machines that compose; \ Part 66, \ generative audio", GREY_A),
        ]
        rows_scene(self, r"composing with machines", items,
                   "Much current research builds tools that compose with a person. <bookmark mark='b'/> They suggest a "
                   "continuation, fill a gap or harmonise a line. <bookmark mark='c'/> Google's Bach Doodle of 2019 harmonised "
                   "millions of melodies typed in by visitors. <bookmark mark='d'/> Bob Sturm and colleagues trained folk-rnn on "
                   "folk tunes in 2016, and musicians played and edited what it wrote. <bookmark mark='e'/> Studies of such tools "
                   "ask what actually helps a composer: control, steering by examples, and being surprised. "
                   "<bookmark mark='f'/> Part 65 builds machines that compose, and Part 66 generative audio.", marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"let a searcher, \ a chain and a human composer each write melodies to the same brief", WHITE),
            (r"measure each output's copying against everything its maker was shown", WHITE),
            (r"collect listeners' judgements of value and of surprise, \ blind to the maker", WHITE),
            (r"$\bigstar$ \ research problem: \ can novelty and value be measured separately, \ and do they trade off?", EAR),
            (r"an answer would turn `is it creative?' \ into questions with numbers", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Let a searcher, a chain and a human composer each write melodies to the "
            "same brief. <bookmark mark='b'/> Measure every output's copying against everything its maker was shown. "
            "<bookmark mark='c'/> Collect listeners' judgements of value and of surprise, blind to who made what. "
            "<bookmark mark='d'/> Can novelty and value be measured separately, and do they trade off? "
            "<bookmark mark='e'/> An answer would turn the question, is it creative, into questions with numbers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
