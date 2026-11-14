from __future__ import annotations

import numpy as np

from videos.music.music24.common import *  # noqa: F403

ORDER = ["pythagorean", "just", "31-tone"]
NAME = {"pythagorean": r"Pythagorean", "just": r"just \ (Zarlino)", "31-tone": r"31 equal \ (Vicentino)", "equal": r"12 equal \ (today)"}


class Tuning(SoundScene):
    def construct(self):
        chapter(self, 10, r"Zarlino's triad, \ Vicentino's thirty-one tones", r"What tuning does a world of triads want?", extra=((1558, r"Zarlino's \textit{Istitutioni}"),))
        self.zarlino()
        self.triads()
        self.meantone()
        self.vicentino()

    # ------------------------------------------------------------------
    def zarlino(self):
        items = [
            (r"1558: \ Gioseffo Zarlino, \ \textit{Le istitutioni harmoniche}", WHITE),
            (r"the \textit{senario}: \ the numbers 1 to 6 give every consonance, \ the major third 5:4, \ the minor 6:5", WHITE),
            (r"the major triad as 4:5:6: \ the harmony of the century, \ in whole numbers", TUNE),
            (r"Part 6: \ just tuning is pure for one key and wolfish for others", GREY_A),
            (r"singers could tune by ear; \ keyboards had to choose: \ meantone", WHITE),
        ]
        rows_scene(self, r"the theory catches up", items,
                   "Theory caught up with the thirds in 1558, when the Venetian Gioseffo Zarlino published his Istitutioni "
                   "harmoniche. <bookmark mark='b'/> Zarlino's senario, the numbers one to six, generates every consonance: "
                   "the octave two to one, the fifth three to two, the fourth four to three, the major third five to four, "
                   "the minor third six to five. <bookmark mark='c'/> And the major triad becomes four to five to six, the "
                   "sound of the whole century in three whole numbers. <bookmark mark='d'/> Part 6 showed the price: tuning "
                   "that is pure in one key goes sour in others. <bookmark mark='e'/> Singers could adjust by ear; keyboards "
                   "had to choose, and chose meantone, which sacrifices the fifths a little to keep the thirds sweet.")

    # ------------------------------------------------------------------
    def triads(self):
        d = load("tuning")
        c = clip("tuning.triads")
        cents = d["cents"]
        rows_ = VGroup()
        for k in ORDER + ["equal"]:
            th, fi = cents[k]
            rows_.add(VGroup(label(NAME[k], font_size=22, color=TUNE if k == "just" else WHITE),
                             label(rf"third \ {th:.1f}", font_size=22, color=WHITE), label(rf"fifth \ {fi:.1f}", font_size=22, color=WHITE),
                             label(rf"{th - cents['just'][0]:+.1f}".replace("+", "$+$").replace("-", "$-$"), font_size=22, color=EAR)))
        for i, r in enumerate(rows_):
            for kk, cell in enumerate(r):
                cell.move_to([[-4.2, -0.9, 1.6, 4.2][kk], 1.6 - 0.65 * i, 0])
        hdr = VGroup(*[label(t, font_size=18, color=GREY_B).move_to([x, 2.3, 0]) for t, x in ((r"tuning", -4.2), (r"cents above the root", 0.35), (r"third, \ against just", 4.2))])
        cap = label(r"31 equal steps to the octave give a third within a cent of pure", font_size=22, color=TUNE).to_edge(DOWN, buff=0.6)
        card = listen_card(r"One chord, \ C E G, \ held, \ in three tunings: \ Pythagorean, \ just, \ and 31 equal steps. \ "
                           r"In which does the third beat fastest? \ And can you tell the other two apart?", width=10.4)
        with self.voiceover(
            "Hear the difference on one chord, C, E and G, held, in three tunings. In which one does the third beat "
            "fastest, and can you tell the other two apart?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        with self.voiceover(
            "The table gives the third and the fifth in cents above the root. The Pythagorean third, built from fifths, "
            "is twenty-one and a half cents wider than the pure third of five to four; today's equal third is fourteen "
            "cents wide; and a third tuned in thirty-one equal steps to the octave is less than a cent from pure."
        ):
            self.play(FadeOut(card), FadeIn(hdr), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"Pythagorean, \ just, \ 31 equal", detail=r"four synthetic voices", kind="synthesized", corner=DL, tag_corner=DR)
            for i, k in enumerate(ORDER):
                st = d["starts"][k]
                end = d["starts"][ORDER[i + 1]] - 0.5 if i + 1 < len(ORDER) else c.duration
                pulse(snd, rows_[i][0], st, end, buff=0.08)
        with self.voiceover(
            "The first, Pythagorean, beats fastest: its third is the wide one, and the two notes of the third go in and "
            "out of step several times a second. The just and thirty-one-step chords are almost indistinguishable, less "
            "than a cent apart; most listeners hear both as still."
        ):
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meantone(self):
        items = [
            (r"four pure fifths overshoot a pure major third by the syntonic comma, \ 81:80, \ about 21.5 cents", WHITE),
            (r"quarter-comma meantone: \ narrow every fifth by a quarter of it, \ about 5.4 cents", WHITE),
            (r"then four fifths make a pure third: \ 386.3 cents, \ and the fifth is 696.6", TUNE),
            (r"the price: \ eleven good fifths and one `wolf', \ unusable keys far from home", WHITE),
            (r"the keyboard tuning of the late Renaissance and early Baroque \ (Part 6)", GREY_A),
        ]
        rows_scene(self, r"meantone", items,
                   "How did keyboards get sweet thirds? <bookmark mark='b'/> Stack four pure fifths and come down two "
                   "octaves, and you overshoot the pure major third by the syntonic comma, eighty-one to eighty, about "
                   "twenty-one and a half cents. <bookmark mark='c'/> Quarter-comma meantone narrows every fifth by a "
                   "quarter of that comma, about five and a half cents, <bookmark mark='d'/> so that four of the narrowed "
                   "fifths land exactly on a pure third, three hundred and eighty-six cents, with fifths of about six "
                   "hundred and ninety-seven. <bookmark mark='e'/> The price is the circle: eleven good fifths and one "
                   "wolf, and keys far from home unplayable. <bookmark mark='f'/> It was the keyboard tuning of the late "
                   "Renaissance and early Baroque, as Part 6 described.", marks="bcdef")

    # ------------------------------------------------------------------
    def vicentino(self):
        items = [
            (r"1555: \ Nicola Vicentino, \ \textit{Ancient music adapted to modern practice}", WHITE),
            (r"to revive the Greek chromatic and enharmonic genera, \ steps smaller than a semitone", WHITE),
            (r"his \textit{archicembalo}: \ a harpsichord with 31 notes to the octave, \ on several keyboards", TUNE),
            (r"1551: \ he lost a public debate in Rome on the genera to Vicente Lusitano", WHITE),
            (r"31 equal steps: \ meantone, \ closed into a circle \ (Huygens, \ 1691)", GREY_A),
        ]
        rows_scene(self, r"thirty-one tones", items,
                   "One theorist went much further. <bookmark mark='b'/> In 1555 Nicola Vicentino published a book whose "
                   "title promised ancient music adapted to modern practice: he wanted to revive the chromatic and "
                   "enharmonic kinds of scale the Greeks had described, with steps smaller than a semitone. "
                   "<bookmark mark='c'/> He built a harpsichord to play them, the archicembalo, with thirty-one notes to "
                   "the octave spread over several keyboards. <bookmark mark='d'/> Four years earlier he had lost a public "
                   "debate on exactly these questions in Rome, against the Portuguese theorist Vicente Lusitano. "
                   "<bookmark mark='e'/> The arithmetic was sound: thirty-one equal steps are almost exactly meantone, "
                   "closed into a circle, as Christiaan Huygens later pointed out, which is why the third in the last "
                   "chord was so nearly pure.")
