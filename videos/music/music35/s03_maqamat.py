from __future__ import annotations

import numpy as np

from videos.music.music35.common import *  # noqa: F403


class Maqamat(SoundScene):
    def construct(self):
        chapter(self, 2, r"Maqamat and their paths", r"Is a maqam a scale?")
        self.join()
        self.hear()
        self.descent()
        self.saba()
        self.sayr()
        self.families()
        self.modulation()

    # ------------------------------------------------------------------
    def join(self):
        d = load("maqamat")
        rows_ = text_rows([
            (r"Rast \ = \ jins Rast on C \ + \ jins Rast on G: \ C, \ D, \ E half-flat, \ F, \ G, \ A, \ B half-flat", WHITE),
            (r"Bayati \ = \ jins Bayati on D \ + \ jins Nahawand on G", WHITE),
            (r"Hijaz \ = \ jins Hijaz on D \ + \ jins Nahawand on G", WHITE),
            (r"Saba \ = \ jins Saba on D \ + \ jins Hijaz on F: \ it does not close at the octave", TUNE),
            (r"the note where the upper jins starts is the \textit{ghammaz}: \ a second centre", GREY_A),
        ], font_size=24)
        head = label(r"two ajnas make a maqam", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Join two ajnas and you have a maqam. <bookmark mark='a'/> Rast is jins Rast on C and jins Rast again on G, giving "
            "C, D, E half-flat, F, G, A, B half-flat, C. <bookmark mark='b'/> Bayati is jins Bayati on D with jins Nahawand on "
            "G. <bookmark mark='c'/> Hijaz is jins Hijaz on D, again with Nahawand on G. <bookmark mark='d'/> Saba is jins "
            "Saba on D with Hijaz on F, and it famously does not close at the octave. <bookmark mark='e'/> The note where the "
            "upper jins starts is the ghammaz, a second centre of the maqam."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                if r is not rows_[0]:
                    self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("maqamat")
        c = clip("maqamat.four")
        names = d["names"]
        ruler = cents_ruler([d["scales"][n] for n in names], width=9.0, top=1200, labels=[f"{n} on {d['tonics'][n]}" for n in names], row_gap=0.9).move_to(RIGHT * 0.6 + DOWN * 0.2)
        head = label(r"four maqamat, \ each up and down", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear four of them, each up and down on the oud: Rast on C, then Bayati, Hijaz and Saba on D. Each row shows the "
            "notes in cents above the tonic, with the piano's twelve keys as faint marks: watch the gold, blue and pink ticks "
            "that fall between them."
        ):
            self.play(FadeIn(head), FadeIn(ruler))
        with self.listen(c) as snd:
            window(snd, r"Rast, \ Bayati, \ Hijaz, \ Saba", detail=r"an oud model", corner=DL, tag_corner=DR)
            for i, n in enumerate(names):
                end = d["starts"][names[i + 1]] - 0.4 if i < len(names) - 1 else c.duration
                pulse(snd, ruler.rows[i][3], d["starts"][n], end, buff=0.05)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sayr(self):
        items = [
            (r"a maqam is more than its scale: \ it has a \textit{sayr}, \ a typical path", WHITE),
            (r"where to begin, \ which notes to stress, \ where to rest, \ how to rise to the upper jins", WHITE),
            (r"and where to modulate: \ each maqam has neighbours it can visit", WHITE),
            (r"Part 34's raga had aroha and pakad: \ the same insight, \ in another tradition", TUNE),
            (r"Sami Abu Shumays and Johnny Farraj's \textit{Inside Arabic Music} \ (2019) \ describes the paths", GREY_A),
        ]
        rows_scene(self, r"sayr: \ the path", items,
                   "As with raga, a maqam is more than a scale. <bookmark mark='b'/> It has a sayr, a typical path through its "
                   "notes: <bookmark mark='c'/> where to begin, which notes to stress, where to rest, how to climb to the upper "
                   "jins, <bookmark mark='d'/> and where to modulate, for each maqam has neighbours it customarily visits. "
                   "<bookmark mark='e'/> Part 34's ragas had their ascents and characteristic phrases: the same insight in "
                   "another tradition. <bookmark mark='f'/> Johnny Farraj and Sami Abu Shumays's book Inside Arabic Music "
                   "describes these paths in detail.", marks="cdef")

    # ------------------------------------------------------------------
    def families(self):
        items = [
            (r"maqamat are grouped in families by their lower jins: \ the Rast family, \ the Bayati family ...", WHITE),
            (r"Rast family: \ Rast, \ Suznak, \ Nairuz ...; \ Bayati family: \ Bayati, \ Husayni ...", WHITE),
            (r"members differ in their upper jins, \ or in their path", WHITE),
            (r"modern lists name about 60 to 80 maqamat in common use", TUNE),
            (r"the families are a teaching map, \ like Part 34's thaats", GREY_A),
        ]
        rows_scene(self, r"families", items,
                   "The maqamat come in families. <bookmark mark='b'/> They are grouped by their lower jins, the Rast family, the "
                   "Bayati family and so on: <bookmark mark='c'/> Rast, Suznak and Nairuz in one, Bayati and Husayni in another. "
                   "<bookmark mark='d'/> Members of a family differ in their upper jins, or in their path. <bookmark mark='e'/> "
                   "Modern lists name some sixty to eighty maqamat in common use. <bookmark mark='f'/> The families are a "
                   "teaching map, like Part 34's thaats.", marks="cdef")

    # ------------------------------------------------------------------
    def descent(self):
        d = load("descent")
        c = clip("descent.updown")
        ruler = cents_ruler([d["up"], d["down"]], width=9.6, top=1200, labels=[r"up", r"down"], colors=[TUNE, BLUE]).move_to(UP * 0.4)
        cap = label(r"Rast climbs with B half-flat \ (1050) \ and often comes down with B$\flat$ \ (1000)", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.1)
        head = label(r"a maqam that changes on the way down", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Paths can change the notes themselves. Rast climbs with B half-flat, but on the way down it often uses B flat: "
            "the upper jins becomes Nahawand instead of Rast. Listen to Rast up and down, and to the B that moves."
        ):
            self.play(FadeIn(head), FadeIn(ruler), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Rast, \ up and down", detail=r"an oud model", corner=DL, tag_corner=DR)
            u = d["unit"]
            for i in range(len(d["up"])):
                pulse(snd, ruler.rows[0][1][i], i * u, (i + 1) * u - 0.03, buff=0.04)
            for j in range(1, len(d["down"])):
                t0 = (len(d["up"]) - 1 + j) * u
                pulse(snd, ruler.rows[1][1][len(d["down"]) - 1 - j], t0, t0 + u - 0.03, buff=0.04)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def modulation(self):
        items = [
            (r"from Bayati: \ to Saba \ (one note lowered), \ to Rast on the ghammaz, \ to Hijaz", WHITE),
            (r"from Rast: \ to Nahawand on the fifth, \ to Bayati on the second", WHITE),
            (r"a modulation usually changes one jins and keeps a shared note", WHITE),
            (r"musicians know these paths as a map of neighbours", TUNE),
            (r"Part 15's key relations, \ in another vocabulary", GREY_A),
        ]
        rows_scene(self, r"where maqamat travel", items,
                   "Maqamat have customary neighbours. <bookmark mark='b'/> From Bayati, players go to Saba by lowering one note, to Rast on the ghammaz, or to Hijaz. <bookmark mark='c'/> From Rast, to Nahawand on the fifth, or to Bayati on the second. <bookmark mark='d'/> A modulation usually changes one jins and keeps a shared note. <bookmark mark='e'/> Musicians know these paths as a map of neighbours, <bookmark mark='f'/> much as Part 15's keys have their near and distant relations.", marks="cdef")

    # ------------------------------------------------------------------
    def saba(self):
        d = load("saba")
        c = clip("saba.up")
        ruler = cents_ruler([d["scale"]], width=10.0, top=1250, labels=None, colors=[EAR]).move_to(UP * 0.4)
        oct_ = VGroup(DashedLine(ruler.rows[0][0].get_left() + RIGHT * 10.0 * 1200 / 1250 + DOWN * 0.4, ruler.rows[0][0].get_left() + RIGHT * 10.0 * 1200 / 1250 + UP * 0.6, color=WHITE),
                      label(r"where D would be", font_size=16, color=WHITE)).arrange(UP, buff=0.1)
        oct_[1].next_to(oct_[0], UP, buff=0.1)
        cap = label(r"Saba's top note is D$\flat$, \ 100 cents short of the octave", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.1)
        head = label(r"Saba: \ the maqam that misses its octave", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Saba is the exception that shows how much a maqam is built from ajnas rather than octaves. Climb it from D in "
            "one common form, and where the octave D would be, the scale reaches D flat. The jins structure continues, and "
            "the octave never arrives. Listen to the climb."
        ):
            self.play(FadeIn(head), FadeIn(ruler), FadeIn(oct_), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Saba, \ climbing", detail=r"an oud model", corner=DL, tag_corner=DR)
            for i in range(len(d["scale"])):
                pulse(snd, ruler.rows[0][1][i], i * d["unit"], (i + 1) * d["unit"] - 0.03, buff=0.04)
        self.wait(0.3)
        self.clear_scene()
