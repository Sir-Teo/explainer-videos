from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.paris()
        self.organum()
        self.problem()
        self.plan()

    # ------------------------------------------------------------------
    def paris(self):
        card = history_card(1198, r"Paris: \ the bishop orders organum in three or four voices for the feasts of Christmas",
                            r"the cathedral of Notre Dame half built; \ its singers ready", width=11.4, font_size=26).to_edge(UP, buff=0.5)
        rows_ = text_rows([
            (r"one note of the chant, \ stretched under a whole minute of music", WHITE),
            (r"above it, \ three voices in a dancing rhythm, \ long, \ short, \ long, \ short", WHITE),
            (r"Pérotin's \textit{Viderunt omnes} and \textit{Sederunt principes}: \ the first music in four parts we can read", TUNE),
        ], font_size=25).move_to(DOWN * 0.9)
        with self.voiceover(
            "Paris, about the year twelve hundred. The new cathedral of Notre Dame is half built; its choir is roofed, "
            "its nave is not. <bookmark mark='a'/> In 1198 and again in 1199 the bishop of Paris, Odo of Sully, "
            "decrees how the feasts after Christmas are to be sung, and among the things he allows is organum in three "
            "or four voices. <bookmark mark='b'/> Organum of that kind takes a single syllable of the old chant and "
            "stretches it, one note held for a minute or more, <bookmark mark='c'/> while above it three voices dance "
            "in a pattern of long and short. <bookmark mark='d'/> Two such pieces survive under the name of a singer "
            "called Pérotin: Viderunt omnes and Sederunt principes, among the earliest substantial surviving four-voice works."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("b")
            self.play(FadeIn(rows_[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows_[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def organum(self):
        d = load("hook")
        c = clip("hook.organum")
        lines = d["lines"]
        g = voices_roll(lines, width=11.4, height=3.6, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.12).move_to(DOWN * 0.3)
        names = VGroup(*[label(t, font_size=18, color=col) for t, col in ((r"three upper voices, \ in the first rhythmic mode", TUNE), (r"the held note of the chant", GREY_A))])
        names[0].next_to(g, UP, buff=0.2).align_to(g, LEFT)
        names[1].next_to(g.parts[3].notes[0], UP, buff=0.08).align_to(g, LEFT)
        head = label(r"an organum on one held note, \ in the manner of Notre Dame \ (ours, \ not Pérotin's)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is what that sounds like, in a version computed for this film rather than Pérotin's own. The lowest "
            "voice holds one note of the chant, F. The three voices above it move in a fixed rhythm, long then short, "
            "and at the start of every long they meet the held note in a fifth or an octave. Listen to the held note "
            "under everything, and to the upper voices trading phrases."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(names))
        with self.listen(c) as snd:
            window(snd, r"an organum on one held F", detail=r"four synthetic voices", kind="synthesized", corner=DL, tag_corner=DR)
            flash_voices(snd, g, lines[:3], 0.0, d["unit"], colors=[TUNE, BLUE, EAR])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"chant had no written rhythm: \ one singer, \ or many in unison, \ following the words", WHITE),
            (r"four singers on four different lines must agree, \ beat by beat, \ on when each note ends", WHITE),
            (r"so Notre Dame needed something no one had written down: \ a notation of rhythm", TUNE),
            (r"and once rhythm could be written, \ it could be designed: \ the next two centuries did exactly that", EAR),
        ])
        head = label(r"a problem of coordination", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "There was a problem in this. <bookmark mark='a'/> The chant had never needed written rhythm: one singer, or a choir in unison, follows the words, and the notes last as long as the words want. <bookmark mark='b'/> Four singers on four different lines must agree, beat by beat, on where every note ends, or the fifths and octaves fall apart. <bookmark mark='c'/> So the singers of Notre Dame needed a developing system for coordinating polyphonic rhythm; earlier traditions already had ways of describing or notating duration. <bookmark mark='d'/> And once rhythm could be written, it could be designed. The two centuries after Pérotin did exactly that, until by the end of the fourteenth century the rhythms on the page were strikingly intricate by the standards of many later teaching repertoires."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        head = label(r"Part 23: \ Chant to Polyphony", font_size=36, color=TUNE).to_edge(UP, buff=0.5)
        steps = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"chant and its eight modes; \ Guido's hexachords and the first staff", WHITE),
            (r"organum: \ parallel, \ free, \ florid", WHITE),
            (r"rhythm written down: \ the rhythmic modes, \ Notre Dame, \ the motet", EAR),
            (r"the Ars nova: \ mensuration and isorhythm, \ computed and found in de Vitry's motets", WHITE),
            (r"Machaut, \ and eighty-nine pieces of the fourteenth century counted", WHITE),
            (r"the Ars subtilior; \ what the notation does not tell us", TUNE))]).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "This part follows Western music from one line to many, from the ninth century to about 1400. "
            "<bookmark mark='a'/> It starts with the chant itself and its eight modes, and Guido's system for "
            "learning it. <bookmark mark='b'/> Then the first harmony, organum, in three stages. "
            "<bookmark mark='c'/> Then rhythm written down: the rhythmic modes, Notre Dame, and the motet. "
            "<bookmark mark='d'/> Then the new art of the fourteenth century, mensuration and isorhythm, built as "
            "programs and then found, by a program, in real motets. <bookmark mark='e'/> Then Machaut, and a century "
            "of music counted from eighty-nine edited pieces. <bookmark mark='f'/> And last the subtlest art of all, "
            "and what the notation still does not tell us."
        ) as vo:
            self.play(FadeIn(head), FadeIn(steps[0]))
            for mark, s in zip("bcdef", steps[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()
