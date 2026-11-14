from __future__ import annotations

import numpy as np

from videos.music.music39.common import *  # noqa: F403
from explainer.music.monochord import blues as BL


class Bebop(SoundScene):
    def construct(self):
        chapter(self, 1, r"Bebop and the contrafact", r"How do you write a new tune without writing new chords?")
        self.birth()
        self.contrafact()
        self.hear()
        self.players()
        self.language()

    # ------------------------------------------------------------------
    def birth(self):
        items = [
            (r"early 1940s, \ Harlem: \ after-hours sessions at Minton's Playhouse and Monroe's Uptown House", WHITE),
            (r"Charlie Parker, \ Dizzy Gillespie, \ Thelonious Monk, \ Kenny Clarke, \ Bud Powell", WHITE),
            (r"small groups, \ fast tempos, \ long lines of eighth notes, \ harmony moving every two beats", WHITE),
            (r"music for listening rather than dancing, \ by players who had come up in the swing bands", TUNE),
            (r"a 1942--44 recording ban hides its birth: \ we hear it almost fully formed in 1945", GREY_A),
        ]
        rows_scene(self, r"bebop", items,
                   "In the early 1940s, in after-hours sessions at Harlem clubs like Minton's Playhouse and Monroe's Uptown "
                   "House, a new jazz took shape. <bookmark mark='b'/> Its makers were Charlie Parker, Dizzy Gillespie, Thelonious "
                   "Monk, the drummer Kenny Clarke and the pianist Bud Powell. <bookmark mark='c'/> Small groups, fast tempos, long "
                   "lines of eighth notes, harmony moving every two beats. <bookmark mark='d'/> Music for listening rather than "
                   "dancing, by players who had come up in the swing bands of Part 38. <bookmark mark='e'/> A musicians' union "
                   "recording ban from 1942 to 1944 hides its birth, so we first hear it almost fully formed, in 1945.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def contrafact(self):
        items = [
            (r"a \textit{contrafact}: \ a new melody written over the chords of an existing song", WHITE),
            (r"Parker's \textit{Ornithology} takes the changes of \textit{How High the Moon}; \ bebop's \textit{Donna Lee} those of \textit{Indiana}", WHITE),
            (r"`rhythm changes', \ from Gershwin's \textit{I Got Rhythm} \ (1930), \ carry hundreds of tunes", WHITE),
            (r"a progression cannot be owned the way a melody can: \ the new tune was the player's own", TUNE),
            (r"the changes became a shared language: \ everyone could play on them", GREY_A),
        ]
        rows_scene(self, r"the contrafact", items,
                   "Bebop players wrote many of their tunes in a particular way. <bookmark mark='b'/> A contrafact is a new "
                   "melody written over the chords of an existing song. <bookmark mark='c'/> Charlie Parker's Ornithology takes "
                   "the changes of How High the Moon; the bebop tune Donna Lee, those of Indiana. <bookmark mark='d'/> The rhythm changes, "
                   "from Gershwin's I Got Rhythm of 1930, carry hundreds of tunes. <bookmark mark='e'/> A chord progression cannot "
                   "be owned the way a melody can, so the new tune was the player's own, and it paid no one else. "
                   "<bookmark mark='f'/> The changes became a shared language that everyone could play on.", marks="cdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("contrafact")
        c = clip("contrafact.rhythm")
        head = [tuple(x) for x in d["head"]]
        solo = [tuple(x) for x in d["solo"]]
        g1 = line_over(head, d["changes"], width=11.4, height=1.7, color=TUNE, lo=56, hi=86, size=15).move_to(UP * 1.4)
        g2 = line_over(solo, d["changes"], width=11.4, height=1.7, color=BLUE, lo=56, hi=86, size=15).move_to(DOWN * 1.5)
        l1 = label(r"a head by the program \ (saxophone)", font_size=18, color=TUNE).next_to(g1, UP, buff=0.12)
        l2 = label(r"then a chorus by the program \ (piano)", font_size=18, color=BLUE).next_to(g2, UP, buff=0.12)
        with self.voiceover(
            "Here is the A section of rhythm changes, eight bars in B flat, with a contrafact of sorts: a line written by "
            "this part's improviser, on an additive saxophone, and then a second chorus from the improviser on the piano. "
            "The chords are the common property; the lines are the program's own."
        ):
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(l1), FadeIn(l2))
        beat = 60.0 / d["bpm"]
        with self.listen(c) as snd:
            window(snd, r"rhythm changes, \ A section", kind="synthesized", detail=r"an additive saxophone, \ piano, \ string and cymbal", corner=DL, tag_corner=DR)
            flash(snd, g1.roll.notes, list(BL.swing_times([e for _, e in head], d["bpm"])), hot=WHITE, base=TUNE)
            flash(snd, g2.roll.notes, list(BL.swing_times([e for _, e in solo], d["bpm"]) + 8 * 4 * beat), hot=WHITE, base=BLUE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def players(self):
        items = [
            (r"Parker: \ the alto saxophone's long, \ fast lines, \ built from a vocabulary of figures", WHITE),
            (r"Gillespie: \ the trumpet in the high register, \ and Afro-Cuban rhythm \ (\textit{Manteca}, \ 1947)", WHITE),
            (r"Monk: \ angular melodies, \ crushed seconds, \ silence as material", WHITE),
            (r"Kenny Clarke moved the beat to the ride cymbal and used the bass drum for accents", TUNE),
            (r"chapter 2 asks how those long lines fit the chords", GREY_A),
        ]
        rows_scene(self, r"the players", items,
                   "Each of the founders added something. <bookmark mark='b'/> Parker, long fast lines on the alto saxophone, "
                   "built from a vocabulary of figures. <bookmark mark='c'/> Gillespie, the trumpet in its high register, and "
                   "Afro-Cuban rhythm, as in Manteca of 1947, Part 37's clave meeting bebop. <bookmark mark='d'/> Monk, angular "
                   "melodies, crushed seconds, and silence as material. <bookmark mark='e'/> And Kenny Clarke moved the beat to "
                   "the ride cymbal and used the bass drum for accents. <bookmark mark='f'/> Chapter two asks how those long lines "
                   "fit the chords.", marks="cdef")

    # ------------------------------------------------------------------
    def language(self):
        items = [
            (r"standards: \ the popular songs of the 1920s--50s that jazz players adopted", WHITE),
            (r"a player learns tunes by their changes, \ and hears every tune as a path through keys", WHITE),
            (r"the jam session as an examination: \ fast tempos, \ hard keys, \ unfamiliar tunes", WHITE),
            (r"to `know the changes' is to know where every chord goes, \ and what each wants next", TUNE),
            (r"what follows is the toolkit for playing through them", GREY_A),
        ]
        rows_scene(self, r"a shared language", items,
                   "The repertoire was the standards: the popular songs of the 1920s to the 1950s that jazz players adopted. "
                   "<bookmark mark='b'/> A player learns them by their changes, and hears every tune as a path through keys. "
                   "<bookmark mark='c'/> The jam session was an examination, with fast tempos, hard keys and unfamiliar tunes. "
                   "<bookmark mark='d'/> To know the changes is to know where every chord goes, and what each wants next. "
                   "<bookmark mark='e'/> What follows is the toolkit for playing through them.", marks="bcde")
