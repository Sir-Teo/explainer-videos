from __future__ import annotations

import numpy as np

from videos.music.music19.common import *  # noqa: F403


class Dim7(SoundScene):
    def construct(self):
        chapter(self, 5, r"The diminished seventh", r"How can one chord lead to eight keys?")
        self.symmetry()
        self.four()

    # ------------------------------------------------------------------
    def symmetry(self):
        d = load("dim7")
        circle = Circle(radius=1.9, color=DIM, stroke_width=2).move_to(LEFT * 3.4 + DOWN * 0.2)
        names = ["C", "D♭", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"]
        pts = {k: circle.get_center() + 1.9 * np.array([np.sin(2 * np.pi * k / 12), np.cos(2 * np.pi * k / 12), 0]) for k in range(12)}
        dots = VGroup(*[Dot(pts[k], radius=0.07, color=GREY_B) for k in range(12)])
        labs = VGroup(*[label(tex(names[k]), font_size=20, color=GREY_B).move_to(circle.get_center() + 2.3 * (pts[k] - circle.get_center()) / 1.9) for k in range(12)])
        chord = d["chord"]
        sq = Polygon(*[pts[k] for k in chord], color=EAR, stroke_width=4)
        hot = VGroup(*[Dot(pts[k], radius=0.12, color=EAR) for k in chord])
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (tex(r"B, \ D, \ F, \ A♭: \ minor thirds all the way round"), WHITE),
            (r"three semitones, \ three, \ three, \ three: \ the octave cut in four", WHITE),
            (r"turn it, \ and it is the same chord: \ there are only three of them", WHITE),
            (r"any of its four notes can be a leading note: \ eight keys, \ major and minor", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.8))
        rows_.move_to(RIGHT * 2.8 + DOWN * 0.1)
        with self.voiceover(
            "In C minor, the chord on the leading note with its seventh is B, D, F, A flat, a diminished seventh. "
            "<bookmark mark='a'/> Put it on Part 12's clock of twelve notes. <bookmark mark='b'/> Its notes are three "
            "semitones apart all the way round: it cuts the octave into four equal parts, a square. "
            "<bookmark mark='c'/> Turn the square by three semitones and it lands on itself, so there are only three "
            "different diminished-seventh pitch-class sets in twelve-tone equal temperament. <bookmark mark='d'/> And because the chord is the same from every "
            "note, any of its four notes can be heard as the leading note. B leads to C; D to E flat; F to F sharp, "
            "written E sharp; A flat, written G sharp, to A. One chord, four tonics, and each can be major or minor: "
            "eight keys. And the three diminished sevenths between them reach all twenty-four keys, each exactly once."
        ) as vo:
            self.play(Create(circle), FadeIn(dots), FadeIn(labs))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(sq), FadeIn(hot), FadeIn(rows_[0]), FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(Rotate(sq, angle=-PI / 2, about_point=circle.get_center()), run_time=1.5)
            self.play(FadeIn(rows_[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows_[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def four(self):
        d = load("dim7")
        c = clip("dim7.four")
        cells = VGroup()
        for r in d["resolutions"]:
            st = block_staff(r["chords"], width=2.9, beats=2, flats=r["key"][0] in (0, 3))
            t = label(tex(r["name"]), font_size=24, color=TUNE)
            cells.add(VGroup(t, st).arrange(DOWN, buff=0.3))
        cells.arrange(RIGHT, buff=0.3)
        cells.scale_to_fit_width(min(cells.width, 13.0)).move_to(DOWN * 0.1)
        cap = label(r"B D F A$\flat$ \ $\cdot$ \ D F A$\flat$ C$\flat$ \ $\cdot$ \ E$\sharp$ G$\sharp$ B D \ $\cdot$ \ G$\sharp$ B D F: \ one chord on the keyboard", font_size=24, color=GREY_A).to_edge(DOWN, buff=1.3)
        with self.voiceover(
            "Hear it. The same diminished seventh, four times, each time resolving to a different minor key: C minor, E "
            "flat minor, F sharp minor, A minor. A careful copyist spells it four ways, so that each time the leading "
            "note is a semitone below its tonic: B, D, F, A flat; D, F, A flat, C flat; E sharp, G sharp, B, D; G sharp, "
            "B, D, F. On the keyboard it is always the same four keys."
        ):
            self.play(FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"one chord, \ four keys", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            rs = d["resolutions"]
            for k, r in enumerate(rs):
                end = rs[k + 1]["start"] - 0.4 if k + 1 < len(rs) else c.duration
                pulse(snd, cells[k][0], r["start"], end, buff=0.1)
        with self.voiceover(
            "Composers learned to use this ambiguity as a door. Arrive on a diminished seventh in one key, and leave it "
            "as if it belonged to another. From Bach's chromatic fantasies to the storms of nineteenth-century opera, "
            "the diminished seventh was the chord of suspense, precisely because the listener cannot tell where it "
            "will go."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()
