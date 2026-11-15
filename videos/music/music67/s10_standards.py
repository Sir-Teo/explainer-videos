from __future__ import annotations

import numpy as np

from videos.music.music67.common import *  # noqa: F403


class Standards(SoundScene):
    def construct(self):
        chapter(self, 9, r"Standards and reporting", r"What must a study say so that someone else can check it?")
        self.standards()
        self.pitch()
        self.units()
        self.reporting()
        self.repro()

    # ------------------------------------------------------------------
    def standards(self):
        items = [
            (r"pitch: \ A = 440 Hz \ (ISO 16, \ 1975); \ historical pitch varied by more than a semitone", WHITE),
            (r"loudness: \ LUFS \ (ITU-R BS.1770, \ Part 57); \ equal-loudness contours \ (ISO 226, \ Part 4)", WHITE),
            (r"listening tests: \ ITU-R BS.1116 for small impairments, \ BS.1534 \ (MUSHRA) \ for intermediate ones \ (Part 58)", WHITE),
            (r"music information retrieval: \ shared tasks \ (MIREX) \ and common scorers \ (\texttt{mir\_eval})", WHITE),
            (r"a standard is a promise that two laboratories measured the same thing", TUNE),
        ]
        rows_scene(self, r"measurement standards", items,
                   "Some of what makes music research checkable is dull and essential: standards. <bookmark mark='b'/> Pitch: A at "
                   "four hundred and forty hertz, set as ISO 16 in 1975, where historical pitch varied by more than a semitone. "
                   "<bookmark mark='c'/> Loudness: the LUFS of Part 57, and the equal-loudness contours of Part 4. "
                   "<bookmark mark='d'/> Listening tests: the ITU's recommendations for small impairments and for intermediate ones, "
                   "MUSHRA, from Part 58. <bookmark mark='e'/> In music information retrieval, shared tasks and common scoring code. "
                   "<bookmark mark='f'/> A standard is a promise that two laboratories measured the same thing.", marks="bcdef")

    # ------------------------------------------------------------------
    def reporting(self):
        items = [
            (r"the data: \ which pieces, \ recordings or participants, \ how chosen, \ how split", WHITE),
            (r"the procedure, \ fixed in advance: \ hypotheses, \ analyses, \ the sample size and why", WHITE),
            (r"every result with its uncertainty, \ and the ones that did not work", WHITE),
            (r"the code and the data, \ where rights allow; \ this series puts every number in a compute file and a test", WHITE),
            (r"and the limits: \ what the study cannot say \ (every README here has a `what the models are, and are not')", TUNE),
        ]
        rows_scene(self, r"what to report", items,
                   "And what must a study report so that someone else can check it? <bookmark mark='b'/> The data: which pieces, "
                   "recordings or participants, how chosen, and how split. <bookmark mark='c'/> The procedure, fixed in advance: "
                   "the hypotheses, the analyses, the sample size and why. <bookmark mark='d'/> Every result with its uncertainty, "
                   "including the ones that did not work. <bookmark mark='e'/> The code and the data, where rights allow; this "
                   "series puts every number in a compute file and checks it in a test. <bookmark mark='f'/> And the limits, what "
                   "the study cannot say; every part's notes here have a section on what its models are, and are not.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def repro(self):
        d = load("repro")
        rows_ = VGroup(
            label(r"Part 65 stored: \ the order-2 chain needs", font_size=20, color=WHITE),
            label(rf"{d['stored']:.15f} bits a note", font_size=24, color=TUNE),
            label(r"recomputed here, \ from the same tunes, \ split and code:", font_size=20, color=WHITE),
            label(rf"{d['again']:.15f}", font_size=24, color=TUNE),
            label(r"identical to the last digit: \ the same seed, \ the same split, \ the same number" if d["equal"] else r"they differ: \ something changed", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.35)
        head = label(r"reproduced", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The simplest check of all: compute it again. <bookmark mark='a'/> Part 65 stored the order-two chain's bits per "
            "note. <bookmark mark='b'/> Recomputed here, from the same tunes with the same split and the same code, "
            + ("<bookmark mark='c'/> it is identical to the last digit. Reproducing a number does not make it right; Chapter 8 "
               "showed that the same number from another split differs. But a number that cannot be reproduced cannot be checked."
               if d["equal"] else "<bookmark mark='c'/> it differs, and something must be found.")
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]), FadeIn(rows_[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[2]), FadeIn(rows_[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[4]))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def units(self):
        items = [
            (r"`dB' alone means nothing: \ dB SPL \ (sound pressure), \ dBFS \ (a file's full scale), \ dB(A) \ (weighted), \ LUFS \ (loudness)", WHITE),
            (r"a level in a file says nothing about the level at the ear until the playback chain is calibrated", WHITE),
            (r"`cents' assume a reference: \ equal temperament, \ or the piece's own tuning \ (Part 6)", WHITE),
            (r"`tempo' assumes a beat level \ (Part 62's octave problem)", WHITE),
            (r"write the unit, \ the reference and how it was measured, \ every time", TUNE),
        ]
        rows_scene(self, r"units", items,
                   "Many disagreements in the literature are about units. <bookmark mark='b'/> A decibel alone means nothing: decibels "
                   "of sound pressure, of a file's full scale, weighted to the ear, or of loudness, are four different things. "
                   "<bookmark mark='c'/> A level in a file says nothing about the level at the ear until the playback chain is "
                   "calibrated. <bookmark mark='d'/> Cents assume a reference: equal temperament, or the piece's own tuning, as in "
                   "Part 6. <bookmark mark='e'/> Tempo assumes a beat level, Part 62's octave problem. <bookmark mark='f'/> Write the "
                   "unit, the reference and how it was measured, every time.", marks="bcdef")

    # ------------------------------------------------------------------
    def pitch(self):
        d = load("pitchstd")
        c = clip("pitchstd.three")
        boxes = choice_boxes([r"A = 440 Hz", r"A = 415 Hz", r"A = 466 Hz"], width=3.2, height=0.9, buff=0.5, size=19).move_to(UP * 0.6)
        res = label(rf"415 is {abs(d['cents_415']):.0f} cents below 440, \ 466 is {d['cents_466']:.0f} above: \ the same written note, \ a semitone apart either way", font_size=18, color=TUNE).next_to(boxes, DOWN, buff=0.6)
        head = label(r"one note, \ three standards", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Why a pitch standard matters: the Tune's first phrase at A equals four hundred and forty, then at four hundred and fifteen, a pitch often used for Baroque music today, then at four hundred and sixty-six, a high organ pitch of that era."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        ks = ["a440", "a415", "a466"]
        with self.listen(c) as snd:
            window(snd, r"440, \ 415, \ 466", kind="synthesized", detail=r"organ tones", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        with self.voiceover(
            f"Four hundred and fifteen is {say(round(abs(d['cents_415'])))} cents below four hundred and forty; four hundred and "
            f"sixty-six, {say(round(d['cents_466']))} above. A study of historical tuning, or of how singers' ranges have "
            "changed, must say which standard a score's notes meant."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()
