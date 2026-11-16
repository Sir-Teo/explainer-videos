from __future__ import annotations

import numpy as np

from videos.music.music36.common import *  # noqa: F403


class Bells(SoundScene):
    def construct(self):
        chapter(self, 1, r"The bells of Marquis Yi", r"How can one bell sound two notes?", extra=((1978, r"excavated"),))
        self.shape()
        self.thirds()
        self.set()
        self.bellsong()
        self.compare()
        self.inscriptions()

    # ------------------------------------------------------------------
    def shape(self):
        round_ = Circle(radius=1.0, color=GREY_B, stroke_width=3).move_to(LEFT * 3.5 + UP * 0.6)
        almond = VGroup(Arc(radius=1.4, start_angle=PI / 2 - 0.8, angle=1.6, color=TUNE, stroke_width=3),
                        Arc(radius=1.4, start_angle=-PI / 2 - 0.8, angle=1.6, color=TUNE, stroke_width=3))
        almond[0].shift(DOWN * 0.95)
        almond[1].shift(UP * 0.95)
        almond.rotate(PI / 2).move_to(RIGHT * 3.0 + UP * 0.6)
        l1 = label(r"a round section: \ the modes come in pairs \ that sound the same note", font_size=19, color=GREY_A).next_to(round_, DOWN, buff=0.5)
        l2 = label(r"an almond section: \ the pairs split into two notes", font_size=19, color=TUNE).next_to(almond, DOWN, buff=0.5)
        rows_ = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"a blow on the centre excites one family of modes; \ on the side, \ the other", WHITE),
            (r"the founders thinned and shaped the bronze to set the two notes a third apart", TUNE))]).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.4)
        head = label(r"the secret is the shape", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The secret is the shape. <bookmark mark='a'/> A European church bell, Part 9's, is round in section, and its "
            "vibration modes come in pairs that sound the same note, whichever way round the bell they point. "
            "<bookmark mark='b'/> These bells are almond-shaped in section, like two curved plates joined at sharp edges. "
            "That breaks the pairs apart into two different notes. <bookmark mark='c'/> A blow on the centre of the face "
            "excites one family of modes, and a blow near the edge, where that family has a node, excites the other. "
            "<bookmark mark='d'/> The founders thinned and shaped the bronze inside to set the two notes, usually a major or "
            "minor third apart."
        ) as vo:
            self.play(FadeIn(head), Create(round_), FadeIn(l1))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(almond), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(rows_[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows_[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def set(self):
        items = [
            (r"65 bells: \ the largest weighs over 200 kg; \ the set spans about five octaves", WHITE),
            (r"the two-tone bells help supply \ a complete chromatic scale over much of the range", WHITE),
            (r"the inscriptions name each note in the Zeng system and its equivalents in other states", WHITE),
            (r"measurements related tones to inscribed pitch names\\names alone give no absolute modern frequency standard", TUNE),
            (r"a performance needed several players with mallets and poles", GREY_A),
        ]
        rows_scene(self, r"the set", items,
                   "The set is enormous. <bookmark mark='b'/> Sixty-five bells, the largest over two hundred kilograms, span about five octaves, <bookmark mark='c'/> and the two-tone bells help give a complete chromatic scale over much of that range. <bookmark mark='d'/> The inscriptions name each note in the Zeng state's system and give its equivalents in other states. <bookmark mark='e'/> Measurements made in the 1980s related the measured tones to the inscribed pitch names; those names do not by themselves supply a modern absolute frequency standard. <bookmark mark='f'/> Playing them took several musicians with mallets and poles.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def compare(self):
        items = [
            (r"European bells \ (Part 9): \ one strike note, \ a crowd of inharmonic partials, \ a long hum", WHITE),
            (r"Chinese \textit{bianzhong}: \ two strike notes, \ a fast decay, \ suited to melody", WHITE),
            (r"shape and construction support short decay: \ notes stay distinct in quick succession", WHITE),
            (r"the bells were played in rituals and banquets, \ a sign of a ruler's status", TUNE),
            (r"after the Han dynasty the art of the two-tone bell was largely lost", GREY_A),
        ]
        rows_scene(self, r"two kinds of bell", items,
                   "Compare the bells of Part 9. <bookmark mark='b'/> A European church bell has one strike note, a crowd of "
                   "inharmonic partials and a long hum. <bookmark mark='c'/> The Chinese bianzhong has two strike notes and a "
                   "fast decay, suited to melody: <bookmark mark='d'/> its shape and construction support the relatively short decay so that notes "
                   "stay distinct in quick succession. <bookmark mark='e'/> The bells sounded at rituals and banquets, a sign of "
                   "a ruler's status. <bookmark mark='f'/> After the Han dynasty the art of the two-tone bell was largely lost.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def thirds(self):
        d = load("thirds")
        c = clip("thirds.two")
        cells = VGroup(label(r"bell 1, \ centre", font_size=24, color=WHITE), label(r"side: \ +300", font_size=24, color=TUNE), label(r"bell 2, \ centre", font_size=24, color=WHITE), label(r"side: \ +400", font_size=24, color=BLUE)).arrange(RIGHT, buff=0.8)
        cells.scale_to_fit_width(min(cells.width, 12.4)).move_to(UP * 0.3)
        head = label(r"two bells: \ a minor third and a major third", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            'The founders could choose the interval. Here are two bells on the same C: the first gives a minor third between its centre and side notes, the second a major third. In the Zeng set both kinds appear, so that the two notes of each bell help fill the gaps left by its neighbours.'
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"two bells, \ centre then side", detail=r"a two-tone bell model", corner=DL, tag_corner=DR)
            ts = d["times"]
            for i, t0 in enumerate(ts):
                end = ts[i + 1] - 0.05 if i + 1 < len(ts) else c.duration
                pulse(snd, cells[i % len(cells)], t0, end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bellsong(self):
        d = load("bellsong")
        c = clip("bellsong.song")
        cells = VGroup(label(r"C", font_size=24, color=TUNE), label(r"D", font_size=24, color=TUNE), label(r"E", font_size=24, color=EAR), label(r"G", font_size=24, color=TUNE), label(r"A", font_size=24, color=TUNE), label(r"G", font_size=24, color=TUNE), label(r"E", font_size=24, color=EAR), label(r"D", font_size=24, color=TUNE), label(r"C", font_size=24, color=TUNE)).arrange(RIGHT, buff=0.8)
        cells.scale_to_fit_width(min(cells.width, 12.4)).move_to(UP * 0.3)
        head = label(r"a melody on two-tone bells \ (ours)", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            'With two notes per bell, fewer bells play more music. Here is a pentatonic melody of ours on four bells, C, D, G and A. Each E, in pink, is played by striking the C bell at its side, where it sounds a major third higher. The player moves between spots on a bell as well as between bells.'
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"a bell melody", detail=r"a two-tone bell model", corner=DL, tag_corner=DR)
            ts = d["times"]
            for i, t0 in enumerate(ts):
                end = ts[i + 1] - 0.05 if i + 1 < len(ts) else c.duration
                pulse(snd, cells[i % len(cells)], t0, end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inscriptions(self):
        items = [
            (r"about 2,800 characters inlaid on the bells and their frame", WHITE),
            (r"they name the note each strike gives, \ in the Zeng state's names", WHITE),
            (r"and translate them into the names used by Chu, \ Zhou and other states", WHITE),
            (r"a comparative music theory, \ written for a court that met many traditions", TUNE),
            (r"they show a full twelve-pitch system in use by the 5th century BCE", GREY_A),
        ]
        rows_scene(self, r"the inscriptions", items,
                   "The inscriptions deserve a closer look. <bookmark mark='b'/> About two thousand eight hundred characters are inlaid on the bells and their frame. <bookmark mark='c'/> They name the note each strike gives, in the names used by the state of Zeng, <bookmark mark='d'/> and translate them into the names used by Chu, Zhou and other states, as a modern scholar might list the same pitch in several tuning systems. <bookmark mark='e'/> It is a comparative music theory, written for a court that met many traditions. <bookmark mark='f'/> And it shows that a full twelve-pitch system was in use by the fifth century BCE, long before most of the written theory that survives.", marks="cdef")
