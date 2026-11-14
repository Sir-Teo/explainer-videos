from __future__ import annotations

import numpy as np

from videos.music.music24.common import *  # noqa: F403


class Gesualdo(SoundScene):
    def construct(self):
        chapter(self, 11, r"Chromaticism and ficta", r"How far could the modes bend?", extra=((1611, r"Gesualdo's sixth book"),))
        self.glarean()
        self.prince()
        self.progression()
        self.ficta()

    # ------------------------------------------------------------------
    def glarean(self):
        items = [
            (r"1547: \ Heinrich Glarean, \ \textit{Dodecachordon}: \ twelve modes, \ not eight", WHITE),
            (r"the new ones end on A and C: \ Aeolian and Ionian, \ our minor and major", TUNE),
            (r"he argued they had been in use all along, \ unnamed", WHITE),
            (r"Zarlino renumbered them, \ starting from C \ (1571)", WHITE),
            (r"by 1700 two of the twelve had swallowed the rest: \ the major and minor keys of Part 15", GREY_A),
        ]
        rows_scene(self, r"twelve modes", items,
                   "The modes themselves were being rebuilt. <bookmark mark='b'/> In 1547 the Swiss humanist Heinrich "
                   "Glarean published the Dodecachordon, arguing for twelve modes instead of eight. "
                   "<bookmark mark='c'/> The four new ones ended on A and on C: the Aeolian and the Ionian, which we call "
                   "minor and major. <bookmark mark='d'/> Glarean argued that composers had been using them all along "
                   "without a name. "
                   "<bookmark mark='e'/> Zarlino later renumbered the twelve to begin from C. <bookmark mark='f'/> And by "
                   "1700 two of the twelve had swallowed all the rest, as the major and minor keys of Part 15.", marks="bcdef")

    # ------------------------------------------------------------------
    def prince(self):
        items = [
            (r"Carlo Gesualdo, \ Prince of Venosa, \ 1566--1613", WHITE),
            (r"in 1590 he killed his wife and her lover: \ the story has followed his music ever since", GREY_A),
            (r"his last madrigal books \ (1611): \ chords whose roots move by thirds and semitones", WHITE),
            (r"no key holds for long: \ chromatic steps in every voice, \ sudden shifts of colour", TUNE),
            (r"Part 19's chromatic chords, \ three centuries early, \ and without their grammar", WHITE),
        ]
        rows_scene(self, r"the prince", items,
                   "The most extreme chromatic music of the century came from a prince. <bookmark mark='b'/> Carlo "
                   "Gesualdo, Prince of Venosa, born in 1566, <bookmark mark='c'/> is remembered first for a crime: in "
                   "1590 he killed his wife and her lover, and the story has shadowed his music ever since. "
                   "<bookmark mark='d'/> His last books of madrigals, printed in 1611, move from chord to chord by roots a "
                   "third or a semitone apart, <bookmark mark='e'/> so that no key holds for more than a moment, with "
                   "chromatic steps in every voice. <bookmark mark='f'/> They sound like Part 19's chromatic harmony three "
                   "centuries early, but without its grammar of keys.", marks="bcdef")

    # ------------------------------------------------------------------
    def progression(self):
        d = load("chromatic")
        c = clip("chromatic.gesualdo")
        vs = d["voices"]
        g = voices_roll(vs, width=11.0, height=3.0, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.12).move_to(DOWN * 0.2)
        names = VGroup()
        for k, ch in enumerate(d["chords"]):
            x = g.frame.get_left()[0] + g.frame.width * (4 * k + 2) / g.total
            names.add(label(ch.replace("♭", r"$\flat$"), font_size=20, color=WHITE).move_to([x, g.frame.get_top()[1] + 0.35, 0]))
        head = label(r"seven chords in the manner of Gesualdo \ (ours)", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(r"roots by thirds and semitones; \ each voice moves as little as it can", font_size=21, color=GREY_A).next_to(g, DOWN, buff=0.35)
        with self.voiceover(
            "Here is the idea, computed for the film rather than taken from Gesualdo: seven chords, A minor, F major, D "
            "flat major, B flat minor, G flat major, E major and A major, each voice moving to the nearest note of the "
            "next chord. Every chord is an ordinary triad; it is the succession that no mode can hold."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(names), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"seven chords, \ roots by thirds", detail=r"four synthetic voices", kind="synthesized", corner=DL, tag_corner=DR)
            flash_voices(snd, g, vs, 0.0, d["unit"], colors=[TUNE, BLUE, EAR, GREY_A])
            flash(snd, list(names), [4 * k * d["unit"] for k in range(len(names))], hot=TUNE, base=WHITE, fade=0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ficta(self):
        items = [
            (r"printed parts still leave many accidentals to the singers: \ \textit{musica ficta} \ (Part 23)", WHITE),
            (r"rules: \ raise the leading tone at a cadence; \ avoid mi against fa", WHITE),
            (r"but the rules conflict, \ and singers in different voices decide independently", WHITE),
            (r"modern editions print their best guess above the staff", TUNE),
            (r"the corpus counts here include those guesses", GREY_A),
        ]
        rows_scene(self, r"the accidentals no one wrote", items,
                   "Even in print, much was left unwritten. <bookmark mark='b'/> Singers still added sharps and flats by "
                   "rule, the musica ficta of Part 23: <bookmark mark='c'/> raise the leading tone at a cadence, avoid a "
                   "tritone between mi and fa. <bookmark mark='d'/> But the rules can conflict, and the singers of "
                   "different voices decided at the same moment, each reading only his own part. "
                   "<bookmark mark='e'/> Modern editors print their best guess as small accidentals above the staff, "
                   "<bookmark mark='f'/> and every count in this part includes those guesses. The last chapter asks "
                   "whether a machine can make them better.", marks="bcdef")
