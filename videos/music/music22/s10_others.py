from __future__ import annotations

import numpy as np

from videos.music.music22.common import *  # noqa: F403


class Others(SoundScene):
    def construct(self):
        chapter(self, 9, r"Other ways to analyse", r"Is a tree the only way to understand a piece?")
        self.expectation()
        self.topics()
        self.transformations()
        self.semiotics()

    # ------------------------------------------------------------------
    def expectation(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"Leonard Meyer, \ 1956: \ meaning is expectation, \ aroused, \ delayed, \ fulfilled", WHITE),
            (r"Eugene Narmour, \ 1990: \ implication--realization: \ a small interval implies continuation, \ a leap a reversal", WHITE),
            (r"Part 14 measured it: \ after a leap, \ the line turns back more often than not", WHITE),
            (r"David Huron, \ 2006: \ \textit{Sweet Anticipation}: \ expectation learned by statistics", WHITE),
            (r"analysis as a model of the listener moment by moment, \ not of the piece as a whole", TUNE))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"analysis as expectation", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Trees are one tradition. <bookmark mark='a'/> Another starts from Leonard Meyer's book of 1956: musical "
            "meaning lies in expectations aroused, delayed and fulfilled. <bookmark mark='b'/> Eugene Narmour turned "
            "that into rules in 1990: a small interval implies that the line will continue the same way; a large leap "
            "implies a reversal. <bookmark mark='c'/> Part 14 measured this on folk tunes and found it partly true. "
            "<bookmark mark='d'/> David Huron's Sweet Anticipation, in 2006, argued that the expectations are learned "
            "from the statistics of the music one has heard, Part 18's probabilities. <bookmark mark='e'/> This kind of "
            "analysis models the listener moment by moment, rather than the piece as a finished whole."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def topics(self):
        cells = VGroup()
        for name, desc in ((r"march", r"dotted rhythms, \\ duple metre"), (r"hunt", r"horn calls, \\ 6/8"), (r"pastoral", r"drones, \\ lilting 6/8"),
                           (r"singing style", r"a long cantabile line"), (r"learned style", r"imitation, \\ counterpoint"), (r"\textit{Sturm und Drang}", r"minor, \\ tremolo, \\ leaps")):
            box = RoundedRectangle(width=3.4, height=1.3, corner_radius=0.12, stroke_color=TUNE, stroke_width=2)
            t = VGroup(label(name, font_size=24, color=TUNE), label(desc, font_size=18, color=GREY_A)).arrange(DOWN, buff=0.12).move_to(box)
            cells.add(VGroup(box, t))
        cells.arrange_in_grid(rows=2, cols=3, buff=(0.4, 0.35)).move_to(UP * 0.4)
        cap = VGroup(label(r"Leonard Ratner, \ 1980: \ topics, \ the stock styles a classical audience recognized", font_size=22, color=WHITE),
                     label(r"a piece as a conversation of styles: \ meaning by reference, \ not by tree", font_size=22, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "A third tradition asks what music refers to. In 1980 Leonard Ratner proposed that eighteenth-century "
            "composers wrote with topics, stock styles their audiences recognized at once: the march, the hunt with its "
            "horn calls, the pastoral with its drones, the singing style, the learned style of counterpoint, and the "
            "storm and stress of minor keys and tremolo. <bookmark mark='a'/> A Mozart movement can move through half a "
            "dozen of them in a minute, and to analyse it is to follow that conversation of styles, meaning by "
            "reference rather than by tree."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def transformations(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"David Lewin, \ 1987: \ \textit{Generalized Musical Intervals and Transformations}", WHITE),
            (r"analyse the moves, \ not the objects: \ `if I am at s and wish to get to t, \ what gesture should I perform?'", WHITE),
            (r"Part 19's P, \ L and R: \ chords as points, \ progressions as paths", WHITE),
            (r"a network of transformations instead of a tree of prolongations", TUNE),
            (r"it fits music the \textit{Ursatz} cannot: \ late Romantic chromaticism", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"analysis as transformation", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A fifth tradition began with David Lewin's book of 1987. <bookmark mark='a'/> <bookmark mark='b'/> Lewin "
            "proposed to analyse the moves rather than the objects, asking, in his words, if I am at s and wish to get to "
            "t, what characteristic gesture should I perform? <bookmark mark='c'/> Part 19's transformations P, L and R "
            "come from this school: chords as points, progressions as paths between them. <bookmark mark='d'/> The "
            "result is a network of transformations rather than a tree of prolongations, <bookmark mark='e'/> and it "
            "fits music the Ursatz cannot, the chromatic chains of Wagner and Liszt, where no single key holds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def semiotics(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"semiotics \ (Nattiez, \ 1975--1990): \ three levels of a work", WHITE),
            (r"the poietic: \ how it was made; \ the neutral: \ the score itself; \ the esthesic: \ how it is heard", WHITE),
            (r"an analysis should say which level it describes", WHITE),
            (r"Schenker claims the esthesic \ (what a good listener hears) \ from the neutral", EAR),
            (r"this series measures the neutral level, \ and tests the esthesic with experiments", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"whose structure?", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A fourth tradition asks whose structure an analysis describes. <bookmark mark='a'/> The semiotician "
            "Jean-Jacques Nattiez separated three levels of a musical work: <bookmark mark='b'/> how it was made, the "
            "score as a neutral object, and how it is heard. <bookmark mark='c'/> An analysis should say which of them "
            "it is about. <bookmark mark='d'/> Schenker's claims are about hearing, what an ideal listener grasps, made "
            "from the score alone. <bookmark mark='e'/> This series measures the score, and then asks experiments what "
            "listeners actually hear, which is the only way to settle a claim about hearing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
