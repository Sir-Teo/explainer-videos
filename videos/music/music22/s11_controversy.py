from __future__ import annotations

import numpy as np

from videos.music.music22.common import *  # noqa: F403


class Controversy(SoundScene):
    def construct(self):
        chapter(self, 10, r"A theory and its author", r"Can a theory be separated from the person who made it?", extra=((2020, r"the argument over Schenker"),))
        self.schenker()
        self.events()
        self.positions()

    # ------------------------------------------------------------------
    def schenker(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"Heinrich Schenker, \ 1868--1935: \ born in Galicia, \ worked in Vienna", WHITE),
            (r"a Jew, \ and a fervent German nationalist", WHITE),
            (r"his writings rank peoples as well as music: \ German genius above all", WHITE),
            (r"they include racist statements about Black people and others", EAR),
            (r"his wife Jeanette was murdered at Theresienstadt in 1942", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"the author", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The theory has an author, and the author matters to the argument. <bookmark mark='a'/> Heinrich Schenker "
            "was born in 1868 in Galicia, then part of Austria-Hungary, and worked in Vienna. <bookmark mark='b'/> He "
            "was Jewish, and a fervent German nationalist. <bookmark mark='c'/> His writings rank peoples as well as "
            "pieces, with German musical genius above all, <bookmark mark='d'/> and they contain racist statements, "
            "about Black people among others. <bookmark mark='e'/> He died in 1935; his widow, Jeanette, was murdered "
            "in the Theresienstadt camp in 1942."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def events(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"2019: \ Philip Ewell's plenary talk to the Society for Music Theory: \ `music theory's white racial frame'", WHITE),
            (r"his argument: \ the field's canon and methods, \ Schenker's first among them, \ carry a racial hierarchy", WHITE),
            (r"2020: \ the \textit{Journal of Schenkerian Studies} published responses, \ some widely condemned", WHITE),
            (r"the Society's board, \ and many theorists, \ criticized the issue; \ its university reviewed how it was made", WHITE),
            (r"2020: \ Ewell's article in \textit{Music Theory Online}; \ the argument continues, \ and has reached the courts", TUNE))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"2019 to now", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "In 2019 the theorist Philip Ewell gave a plenary talk to the Society for Music Theory titled music "
            "theory's white racial frame. <bookmark mark='a'/> He argued that the field's canon and methods, with "
            "Schenker's at their centre, carry the racial hierarchy of their authors, and that the field had looked away "
            "from it. <bookmark mark='b'/> <bookmark mark='c'/> In 2020 the Journal of Schenkerian Studies published a "
            "set of responses, some of which were widely condemned as racist themselves. <bookmark mark='d'/> The "
            "Society's executive board and many theorists criticized the issue, and the university that publishes the "
            "journal reviewed how it had been produced. <bookmark mark='e'/> Ewell's argument appeared as an article "
            "in Music Theory Online the same year. The dispute continues, in journals and in court."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("acde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def positions(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"one position: \ a method can be judged apart from its author; \ reduction is a tool", WHITE),
            (r"another: \ the method itself encodes a ranking, \ of pieces and of traditions", WHITE),
            (r"what this part can add: \ state the theory as rules, \ and test what it claims", WHITE),
            (r"the descent to the tonic is real in these tunes; \ the claim that only some music deserves it is not a finding", TUNE),
            (r"a theory built on one repertoire should be tested on others \ (Act VI)", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"what the argument is about", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "What is the argument about? <bookmark mark='a'/> One position holds that a method can be judged apart "
            "from its author: reduction is a tool, to be used where it helps. <bookmark mark='b'/> Another holds that "
            "the method itself encodes a ranking, since it defines good music as music that fits it, and that teaching "
            "it as the core of the subject passes the ranking on. <bookmark mark='c'/> What a course like this one can "
            "add is to state the theory as explicit rules and test its claims. <bookmark mark='d'/> Some survive: the "
            "stepwise descent to the tonic is really there, far beyond chance, in the endings of these tunes. The claim "
            "that only some music deserves to be heard this way is not a finding of any analysis. "
            "<bookmark mark='e'/> And a theory built on one repertoire should be tested on others, as Act VI of this "
            "series will do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
