from __future__ import annotations

import numpy as np

from videos.music.music30.common import *  # noqa: F403

ICOL = {"piano": BLUE, "bowed": TUNE, "voice": EAR}


class Spectral(SoundScene):
    def construct(self):
        chapter(self, 7, r"A spectrum, \ orchestrated", r"Can an ensemble play the inside of one note?", extra=((1975, r"Grisey's \textit{Partiels}"),))
        self.grisey()
        self.quiz()
        self.levels()
        self.buildup()
        self.cents()
        self.spectralists()
        self.name()

    # ------------------------------------------------------------------
    def grisey(self):
        items = [
            (r"Paris, \ 1970s: \ the Ensemble l'Itinéraire, \ Gérard Grisey, \ Tristan Murail", WHITE),
            (r"Grisey's \textit{Partiels} \ (1975): \ the spectrum of a low trombone note, \ analysed by machine", WHITE),
            (r"each harmonic given to an instrument, \ at its own loudness: \ the note rebuilt by an ensemble", WHITE),
            (r"the harmonic series \ (Part 1) \ as harmony: \ in tune with the physics, \ out of tune with the piano", TUNE),
            (r"a reply to serialism: \ compose with sound as it is, \ not with abstract rows", GREY_A),
        ]
        rows_scene(self, r"spectral music", items,
                   "In Paris in the 1970s a group of young composers took the spectrum itself as their material. "
                   "<bookmark mark='c'/> In Gérard Grisey's Partiels, of 1975, the starting point is the spectrum of a low "
                   "trombone note, analysed by machine, <bookmark mark='d'/> and each of its harmonics is given to an instrument, "
                   "at its own loudness, so that the ensemble rebuilds the note. <bookmark mark='e'/> The harmony is the harmonic "
                   "series of Part 1: based on selected spectral relationships, often differing from the equal-tempered keyboard. <bookmark mark='f'/> It was a reply to "
                   "serialism: compose with sound as it is, not with rows.", marks="cdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("spectral")
        c = clip("spectral.quiz")
        card = listen_card(r"A low brass note from Part 8's lips on a long bore, \ and the same note's sixteen harmonics \ played by an ensemble. \ "
                           r"Which is the ensemble, \ A or B? \ Listen for the moment the sound splits apart.", width=10.6)
        with self.voiceover(
            "Hear the idea with the series' own instruments. A low brass note, from Part 8's model of lips buzzing on a long "
            "bore, and the same note's sixteen harmonics handed to an ensemble of piano, bowed strings and a synthetic voice, "
            "each at the harmonic's own frequency and loudness. Which is the ensemble, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        la = label(r"A", font_size=48, color=GREY_A).move_to(LEFT * 3.0 + UP * 0.4)
        lb = label(r"B", font_size=48, color=GREY_A).move_to(RIGHT * 3.0 + UP * 0.4)
        self.play(FadeOut(card), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", kind="synthesized", detail=r"Part 8's lips; \ an ensemble", corner=DL, tag_corner=DR)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.15)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.15)
        ans = VGroup(label(rf"A: \ one brass tone, \ {d['f0']:.0f} Hz", font_size=24, color=GREY_A).next_to(la, DOWN, buff=0.5),
                     label(r"B: \ its harmonics, \ an ensemble", font_size=24, color=TUNE).next_to(lb, DOWN, buff=0.5))
        with self.voiceover(
            "B is the ensemble. Its attack gives it away: the instruments begin with their own strikes and bows, and for a "
            "moment you hear separate sounds; then they fuse into something close to one note, a little like the brass "
            "tone of A but not the same. That fusing and splitting is what spectral composers wrote with."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def levels(self):
        d = load("spectral")
        lv = d["levels"]
        bars = VGroup()
        W, H = 9.6, 3.0
        for h, db in enumerate(lv, start=1):
            n = next((x for x in d["notes"] if x["harmonic"] == h), None)
            col = ICOL[n["inst"]] if n else GREY_B
            hgt = H * (db + 40) / 40
            bars.add(Rectangle(width=W / 16 - 0.08, height=max(hgt, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.9)
                     .move_to([-W / 2 + W * (h - 0.5) / 16, -1.9 + max(hgt, 0.02) / 2, 0]))
        nums = VGroup(*[label(str(h), font_size=15, color=GREY_B).move_to([-W / 2 + W * (h - 0.5) / 16, -2.15, 0]) for h in range(1, 17)])
        key = VGroup(*[VGroup(Square(side_length=0.2, fill_color=c_, fill_opacity=0.9, stroke_width=0), label(t, font_size=19, color=c_)).arrange(RIGHT, buff=0.15)
                       for t, c_ in ((r"piano \ (low)", BLUE), (r"bowed strings", TUNE), (r"voice \ (high)", EAR))]).arrange(RIGHT, buff=0.6).to_edge(UP, buff=1.0)
        head = label(rf"the brass tone's first sixteen harmonics \ ({d['f0']:.1f} Hz): \ level, \ and who plays each", font_size=23, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is how the ensemble was built. The program measures the level of each of the brass tone's first sixteen "
            "harmonics: the bars, from forty decibels below the strongest up. Each harmonic becomes a note at exactly its "
            "frequency, and is given to an instrument by register: the lowest to the piano, the middle to the bowed strings, "
            "the highest to the voice, each sounding at its harmonic's level."
        ):
            self.play(FadeIn(head), FadeIn(key), FadeIn(bars), FadeIn(nums))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cents(self):
        rows_ = text_rows([
            (r"harmonics 1, \ 2, \ 4, \ 8, \ 16: \ octaves, \ exactly on a piano key \ (if the fundamental is)", WHITE),
            (r"harmonic 5: \ 14 cents flat of the piano's major third; \ harmonic 3: \ 2 cents sharp of its fifth", WHITE),
            (r"harmonic 7: \ 31 cents flat; \ harmonic 11: \ nearly a quarter tone between two keys; \ 13: \ 41 sharp of the key below", WHITE),
            (r"spectral harmony needs pitches between the piano's keys: \ quarter and eighth tones", TUNE),
            (r"Part 6's tuning, \ heard as harmony rather than as error", GREY_A),
        ], font_size=23)
        head = label(r"harmonics against the piano's keys", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Why can a piano not play this chord? <bookmark mark='a'/> When the fundamental is on an equal-tempered key, its octave harmonics one, two, four, eight and sixteen also fall on keys. <bookmark mark='b'/> But the fifth harmonic is fourteen cents flatter than the piano's major third, and the third two cents sharper than its fifth. <bookmark mark='c'/> The seventh is thirty-one cents flat; the eleventh lies almost exactly between two keys; the thirteenth is forty-one cents above the key below it. <bookmark mark='d'/> So spectral composers wrote quarter tones and eighth tones, <bookmark mark='e'/> Part 6's tuning differences, heard as harmony rather than as error."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spectralists(self):
        items = [
            (r"Tristan Murail, \ \textit{Gondwana} \ (1980): \ orchestral spectra built from bell and brass models", WHITE),
            (r"Kaija Saariaho: \ the IRCAM studio, \ spectra analysed and transformed by computer", WHITE),
            (r"IRCAM, \ Paris, \ 1977: \ Boulez's institute where composers and scientists work together", WHITE),
            (r"the computer as an ear: \ analysis \ (Part 3) \ becomes the composer's material", TUNE),
            (r"Part 61 builds the analysis tools; \ Part 52, \ synthesis from models", GREY_A),
        ]
        rows_scene(self, r"spectralism after Grisey", items,
                   "The approach spread. <bookmark mark='b'/> Tristan Murail's Gondwana, of 1980, builds orchestral spectra from "
                   "models of bells and brass. <bookmark mark='c'/> The Finnish composer Kaija Saariaho analysed and transformed "
                   "spectra by computer at IRCAM, <bookmark mark='d'/> the institute in Paris that Pierre Boulez opened in 1977 "
                   "so that composers and scientists could work side by side. <bookmark mark='e'/> The computer became an ear: "
                   "Part 3's analysis turned into the composer's material. <bookmark mark='f'/> Part 61 builds such analysis "
                   "tools, and Part 52 synthesis from models.", marks="cdef")

    # ------------------------------------------------------------------
    def buildup(self):
        d = load("buildup")
        c = clip("buildup.harmonics")
        notes = d["notes"]
        W = 10.0
        bars = VGroup(*[Rectangle(width=W - 0.45 * i * W / 8.0 / 2.2, height=0.12, stroke_width=0, fill_color=ICOL[n["inst"]], fill_opacity=0.9) for i, n in enumerate(notes)])
        for i, (b, n) in enumerate(zip(bars, notes)):
            b.stretch_to_fit_width(W * (len(notes) - i) / len(notes))
            b.move_to([W / 2 - b.width / 2, -2.2 + 4.2 * (n["harmonic"] - 1) / 16, 0])
        head = label(r"the sixteen harmonics entering one at a time, \ lowest first", font_size=25, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Partiels itself begins this way, the spectrum assembling in time. Here are our sixteen harmonics entering one "
            "by one, lowest first, each on its instrument. Listen for the moment the separate pitches stop being a chord and "
            "start fusing into one low, buzzing tone."
        ):
            self.play(FadeIn(head), FadeIn(bars))
        with self.listen(c) as snd:
            window(snd, r"a spectrum assembling", kind="synthesized", detail=r"piano, \ bowed strings, \ voice", corner=DL, tag_corner=DR)
            flash(snd, list(bars), [d["gap"] * i for i in range(len(notes))], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def name(self):
        items = [
            (r"`spectral music': \ the philosopher and composer Hugues Dufourt's term \ (1979)", WHITE),
            (r"Horațiu Rădulescu: \ spectra from a piano's strings, \ bowed and struck inside", WHITE),
            (r"Georg Friedrich Haas, \ \textit{in vain} \ (2000): \ harmonic-series chords in near darkness", WHITE),
            (r"the harmonic series heard as consonance, \ the tempered scale as one tuning among many", TUNE),
            (r"Part 33 asks which tunings are possible at all", GREY_A),
        ]
        rows_scene(self, r"the name, and after", items,
                   "The movement got its name in 1979, from the composer and philosopher Hugues Dufourt. <bookmark mark='c'/> Horațiu Rădulescu built spectra from piano strings bowed and struck from inside the instrument. <bookmark mark='d'/> Georg Friedrich Haas's in vain, of 2000, plays chords from the harmonic series with the hall's lights going down to near darkness. <bookmark mark='e'/> Harmonic spectra can promote fusion, while consonance and roughness still depend on voicing, level and context, and the tempered scale as one tuning among many. <bookmark mark='f'/> Part 33 asks which tunings are possible at all.", marks="cdef")
