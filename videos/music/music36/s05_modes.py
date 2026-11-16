from __future__ import annotations

import numpy as np

from videos.music.music36.common import *  # noqa: F403


class Modes(SoundScene):
    def construct(self):
        chapter(self, 4, r"Five notes, \ five modes", r"What can you do with five notes?")
        self.hear()
        self.tunes()
        self.pien()
        self.melody()
        self.opera()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("modes")
        c = clip("modes.five")
        ruler = cents_ruler([d["modes"][k] + [1200] for k in d["order"]], width=8.6, top=1200, labels=d["order"], row_gap=0.75).move_to(RIGHT * 0.6 + DOWN * 0.2)
        head = label(r"the pentatonic collection, \ started on each note", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The five notes make five modes, depending on which is home. Gong mode is C, D, E, G, A; shang starts the same "
            "collection on D; jue on E; zhi on G; yu on A. Each has its own pattern of whole tones and minor thirds, heard "
            "here from the same C. Compare Part 12's church modes, seven rotations of the diatonic: the same idea with five."
        ):
            self.play(FadeIn(head), FadeIn(ruler))
        with self.listen(c) as snd:
            window(snd, r"gong, \ shang, \ jue, \ zhi, \ yu", detail=r"a plucked-string model", corner=DL, tag_corner=DR)
            for i, k in enumerate(d["order"]):
                end = d["starts"][d["order"][i + 1]] - 0.3 if i < 4 else c.duration
                pulse(snd, ruler.rows[i][3], d["starts"][k], end, buff=0.05)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pien(self):
        items = [
            (r"two more notes from the chain, \ \textit{bian} \ (`changing') \ tones, \ fill the gaps: \ seven-note scales", WHITE),
            (r"\textit{bianzhi} \ (F$\sharp$) \ and \textit{biangong} \ (B) \ in the oldest system", WHITE),
            (r"they are passing notes: \ the five remain the skeleton", WHITE),
            (r"the same seven notes as the Lydian mode \ (Part 12)", TUNE),
            (r"Part 28: \ Debussy heard pentatonic melody at the Paris exhibition of 1889", GREY_A),
        ]
        rows_scene(self, r"seven from five", items,
                   "The scale can grow. <bookmark mark='b'/> Two more pitches from the chain of fifths, called bian, changing "
                   "tones, fill the gaps and make seven-note scales: <bookmark mark='c'/> in the oldest system, bianzhi, an F "
                   "sharp, and biangong, a B. <bookmark mark='d'/> They act as passing notes; the five remain the skeleton. "
                   "<bookmark mark='e'/> The seven are the notes of Part 12's Lydian mode. <bookmark mark='f'/> And as Part 28 "
                   "noted, Debussy heard pentatonic melody at the Paris exhibition of 1889.", marks="cdef")

    # ------------------------------------------------------------------
    def melody(self):
        items = [
            (r"pentatonic melodies have no semitones: \ no semitone leading tone; contextual tonic attraction remains", WHITE),
            (r"cadence comes from contour and rhythm, \ not from a dominant chord", WHITE),
            (r"pentatonic scales appear worldwide: \ Scotland, \ West Africa, \ the Andes, \ East Asia", WHITE),
            (r"Part 12: \ the pentatonic is a maximally even five-note set", TUNE),
            (r"Part 47 asks whether such scales are universal", GREY_A),
        ]
        rows_scene(self, r"melody without semitones", items,
                   "Pentatonic melody works differently. <bookmark mark='b'/> It has no semitones, so it has no diatonic semitone leading tone, although melodic context can still establish strong tonal attraction, <bookmark mark='c'/> and cadence comes from contour and rhythm rather than from a dominant chord. <bookmark mark='d'/> Pentatonic scales appear all over the world, in Scotland, West Africa, the Andes and East Asia. <bookmark mark='e'/> Part 12 showed one geometric property of them: the pentatonic is the maximally even five-note set. <bookmark mark='f'/> Part 47 asks whether such scales are universal.", marks="cdef")

    # ------------------------------------------------------------------
    def tunes(self):
        d = load("melody")
        c = clip("melody.two")
        cells = VGroup(label(r"five notes", font_size=24, color=TUNE), label(r"with F$\sharp$ and B as passing notes", font_size=24, color=BLUE)).arrange(RIGHT, buff=0.8)
        cells.scale_to_fit_width(min(cells.width, 12.4)).move_to(UP * 0.3)
        head = label(r"a pentatonic melody, \ then with bian tones \ (ours)", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            'Here is a pentatonic melody of our own in gong mode, ending on C: no semitones anywhere, the cadence made by falling through E and D. Then the same melody with the two bian tones, F sharp and B, slipped in as passing notes on weak beats. The skeleton is unchanged; the surface gains semitones.'
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"five notes, \ then seven", detail=r"a plucked-string model", corner=DL, tag_corner=DR)
            ks = ['five', 'seven']
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.4 if i < len(ks) - 1 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def opera(self):
        items = [
            (r"Chinese folk song and regional opera use pentatonic and related modes", WHITE),
            (r"Beijing opera \ (\textit{jingju}): \ two main melodic systems, \ \textit{xipi} and \textit{erhuang}", WHITE),
            (r"the jinghu fiddle leads, \ with percussion marking speech and movement", WHITE),
            (r"modes carry character and mood, \ as rasa does for raga", TUNE),
            (r"Part 40 hears song across traditions", GREY_A),
        ]
        rows_scene(self, r"five notes on stage", items,
                   "Five-note modes are everywhere in Chinese music. <bookmark mark='b'/> Folk songs and regional operas use pentatonic and related modes. <bookmark mark='c'/> Beijing opera has two main melodic systems, xipi and erhuang, <bookmark mark='d'/> led by the high jinghu fiddle, with percussion marking speech and movement on stage. <bookmark mark='e'/> The modes carry character and mood, as rasa does for raga. <bookmark mark='f'/> Part 40 hears song across traditions.", marks="cdef")
