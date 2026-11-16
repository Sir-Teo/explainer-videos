from __future__ import annotations

import numpy as np

from videos.music.music24.common import *  # noqa: F403


class Masses(SoundScene):
    def construct(self):
        chapter(self, 3, r"The Mass, three ways", r"How do you build a half-hour piece from borrowed music?", extra=((1567, r"the \textit{Missa Papae Marcelli} printed"),))
        self.kinds()
        self.corpus()
        self.trent()

    # ------------------------------------------------------------------
    def kinds(self):
        cells = VGroup()
        for name, how, ex in ((r"cantus firmus", r"a borrowed tune in long notes \\ in one voice, \\ the others around it", r"\textit{L'homme armé}: \\ more than forty Masses"),
                              (r"paraphrase", r"a chant melody ornamented \\ and passed through every voice", r"Josquin, \\ \textit{Missa Pange lingua}"),
                              (r"imitation \ (parody)", r"a whole polyphonic piece \\ reworked: \\ its points, \\ its cadences", r"most of Palestrina's \\ later Masses")):
            box = RoundedRectangle(width=3.8, height=3.0, corner_radius=0.15, stroke_color=TUNE, stroke_width=2)
            t = VGroup(label(name, font_size=28, color=TUNE), label(how, font_size=19, color=WHITE), label(ex, font_size=18, color=GREY_A)).arrange(DOWN, buff=0.3).move_to(box)
            cells.add(VGroup(box, t))
        cells.arrange(RIGHT, buff=0.35).move_to(DOWN * 0.1)
        head = label(r"five texts, \ the same every day: \ Kyrie, \ Gloria, \ Credo, \ Sanctus, \ Agnus Dei", font_size=24, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "The largest form of the century was the Mass: the five Ordinary sections commonly set in a polyphonic Mass cycle, Kyrie, Gloria, Credo, "
            "Sanctus and Agnus Dei, set as one cycle on shared material. Three important techniques were. "
            "<bookmark mark='a'/> In a cantus firmus Mass, a borrowed tune runs in long notes through one voice of every "
            "movement, and the others are built round it; a popular song, L'homme armé, the armed man, served for more "
            "than forty. <bookmark mark='b'/> In a paraphrase Mass, a chant is ornamented and passed through all the "
            "voices, as in Josquin's Missa Pange lingua. <bookmark mark='c'/> And in an imitation Mass, later called a "
            "parody Mass, a whole polyphonic piece, a motet or a chanson, is reworked: its points of imitation, its "
            "cadences, its textures, rearranged into a new work. Most of Palestrina's later Masses are of that kind."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(cell[0]) for cell in cells])
            for mark, cell in zip("abc", cells):
                vo.wait_until(mark)
                self.play(FadeIn(cell[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def corpus(self):
        d = load("masses")
        vo_ = d["voices"]
        keys = sorted(vo_, key=int)
        bars = columns([vo_[k] for k in keys], [rf"{k}" for k in keys], width=6.4, height=2.6, color=TUNE, fmt="{:.0f}", font_size=20)
        bars.move_to(LEFT * 2.8 + DOWN * 0.4)
        t = label(r"movements by number of voices", font_size=20, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(*[label(s, font_size=23, color=c_) for s, c_ in (
            (rf"{d['works']} Masses, \ {d['movements']:,} movements".replace(",", "{,}"), WHITE),
            (r"Humdrum encodings in the music21 corpus", GREY_A),
            (r"mostly four, \ five and six voices", WHITE),
            (r"a whole career of one composer: \ a corpus for a census", TUNE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.move_to(RIGHT * 3.8 + DOWN * 0.2)
        with self.voiceover(
            f"Giovanni Pierluigi da Palestrina, whose career centered on Roman church institutions, with an earlier post in Palestrina, wrote over a hundred Masses. "
            f"<bookmark mark='a'/> This part's corpus holds {say(d['works'])} of them, {say(d['movements'])} movements in "
            "all, encoded in the Humdrum format and kept in the music21 library's corpus. <bookmark mark='b'/> Most are "
            "for four, five or six voices. <bookmark mark='c'/> A whole career of one composer, in a single style, is "
            "rare data: it lets us ask what the style is, as a set of habits, and count how often each habit is broken."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("aabc", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trent(self):
        items = [
            (r"1545--1563: \ the Council of Trent reforms the Catholic Church", WHITE),
            (r"some bishops complain that polyphony buries the words", WHITE),
            (r"a later story: \ Palestrina's \textit{Missa Papae Marcelli} persuaded them to keep it", EAR),
            (r"the story appears decades later; \ the Council's decree asks only that the words be understood", GREY_A),
            (r"but the Mass is unusually clear: \ many passages declaimed by all the voices together", TUNE),
        ]
        rows_scene(self, r"a legend", items,
                   "The Missa Papae Marcelli carries a legend. <bookmark mark='b'/> Between 1545 and 1563 the Council of "
                   "Trent met to reform the Catholic Church, <bookmark mark='c'/> and some of its members complained that "
                   "elaborate polyphony made the sacred words impossible to hear. <bookmark mark='d'/> A story told in the "
                   "next century says that Palestrina's Mass, sung before the cardinals, persuaded them not to ban "
                   "polyphony. <bookmark mark='e'/> The story appears long after the event, and the Council's decree only "
                   "asks that the words be understood and the music be free of anything lascivious. "
                   "<bookmark mark='f'/> Still, the Mass is unusually clear: long passages are declaimed by all the "
                   "voices together, so the text can be heard. Legends attach to music that fits them.", marks="bcdef")
