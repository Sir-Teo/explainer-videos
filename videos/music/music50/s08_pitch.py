from __future__ import annotations

import numpy as np

from videos.music.music50.common import *  # noqa: F403


class Pitch(SoundScene):
    def construct(self):
        chapter(self, 7, r"Time and pitch", r"Can a sound be made higher without being made faster?")
        self.tied()
        self.hear()
        self.psola_()
        self.history()
        self.formants()

    # ------------------------------------------------------------------
    def tied(self):
        items = [
            (r"play a recording faster, \ and every frequency rises in proportion: \ pitch and tempo move together", WHITE),
            (r"a tape at double speed is an octave higher and twice as quick", WHITE),
            (r"and the voice's formants rise too \ (Part 8): \ the singer shrinks into a chipmunk", WHITE),
            (r"changing pitch alone, \ or time alone, \ needs the sound taken apart and put back together", TUNE),
            (r"two ways: \ by grains of the waveform, \ and by its spectrum", GREY_A),
        ]
        rows_scene(self, r"pitch and time, \ tied", items,
                   "The last family changes time and pitch. <bookmark mark='b'/> Play a recording faster, and every frequency rises "
                   "in proportion: pitch and tempo move together. <bookmark mark='c'/> A tape at double speed is an octave higher "
                   "and twice as quick, <bookmark mark='d'/> and the voice's formants, from Part 8, rise too: the singer shrinks "
                   "into a chipmunk. <bookmark mark='e'/> Changing pitch alone, or time alone, needs the sound taken apart and put "
                   "back together. <bookmark mark='f'/> There are two ways: by grains of the waveform, and by its spectrum.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("pitch")
        c = clip("pitch.three")
        du = d["durations"]
        cells = VGroup()
        for k, t, desc in (("original", r"the original", r"Part 8's voice"), ("resampled", r"played faster", r"a fifth up, \ and shorter"),
                           ("psola", r"PSOLA", r"a fifth up, \ same length, \ same vowel")):
            cells.add(VGroup(Rectangle(width=2.2 * du[k], height=0.8, stroke_color=GREY_B, fill_color=TUNE if k == "psola" else (EAR if k == "resampled" else GREY_A), fill_opacity=0.25),
                             VGroup(label(t, font_size=20, color=WHITE), label(desc, font_size=15, color=GREY_A)).arrange(DOWN, buff=0.1)).arrange(ORIGIN))
        for c_ in cells:
            c_[1].move_to(c_[0])
        cells.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(LEFT * 0.5)
        cap = label(rf"box length: \ duration \ ({du['original']:.1f}, \ {du['resampled']:.1f} and {du['psola']:.1f} s)", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.9)
        head = label(r"a fifth higher, \ two ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the difference. The voice; then a fifth higher by playing it faster; then a fifth higher by PSOLA."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        keys = ["original", "resampled", "psola"]
        with self.listen(c) as snd:
            window(snd, r"one voice, \ three ways", kind="synthesized", detail=r"Part 8's voice", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i < 2 else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def psola_(self):
        rows_ = text_rows([
            (r"Eric Moulines and Francis Charpentier \ (1990): \ pitch-synchronous overlap-add", WHITE),
            (r"mark every period of the voice; \ cut a grain two periods long around each mark", WHITE),
            (r"lay the grains back down closer together to raise the pitch, \ further apart to lower it", TUNE),
            (r"each grain keeps its own shape, \ so the formants, \ the vowel, \ stay where they were", WHITE),
            (r"repeat or skip grains to keep the length: \ pitch and time, \ untied", GREY_A),
        ], font_size=23)
        head = label(r"PSOLA", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "PSOLA works on the waveform. <bookmark mark='a'/> Eric Moulines and Francis Charpentier described it in 1990. "
            "<bookmark mark='b'/> Mark every period of the voice, and cut a grain two periods long around each mark. "
            "<bookmark mark='c'/> Lay the grains back down closer together to raise the pitch, or further apart to lower it. "
            "<bookmark mark='d'/> Each grain keeps its own shape, so the formants, and the vowel, stay where they were. "
            "<bookmark mark='e'/> Repeat or skip grains to keep the length. Pitch and time are untied, for voices and other "
            "sounds with a clear period."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"varispeed: \ studios ran tape a little fast to brighten a track, \ or slow to deepen it", WHITE),
            (r"the Chipmunks \ (1958): \ voices recorded at half speed and played back at full", WHITE),
            (r"samplers transpose by resampling, \ so a sampled piano needs a recording every few notes", WHITE),
            (r"Eventide's H910 Harmonizer \ (1975): \ one of the first boxes to change pitch alone, \ in real time", TUNE),
            (r"the grains of PSOLA and the spectra of the phase vocoder are its descendants", GREY_A),
        ]
        rows_scene(self, r"speed and pitch in the studio", items,
                   "Studios have long played with the link. <bookmark mark='b'/> Varispeed ran tape a little fast to brighten a "
                   "track, or slow to deepen it. <bookmark mark='c'/> The Chipmunks, in 1958, were voices recorded at half speed "
                   "and played back at full. <bookmark mark='d'/> Samplers transpose by resampling, so a sampled piano needs a "
                   "recording every few notes, or its timbre shifts. <bookmark mark='e'/> Eventide's H910 Harmonizer, in 1975, was "
                   "one of the first boxes to change pitch alone, in real time. <bookmark mark='f'/> The grains of PSOLA and the "
                   "spectra of the phase vocoder are its descendants.", marks="bcdef")

    # ------------------------------------------------------------------
    def formants(self):
        items = [
            (r"a voice is a source and a filter \ (Part 8): \ the vocal folds set the pitch, \ the tract sets the formants", WHITE),
            (r"resampling moves both; \ PSOLA moves only the pitch, \ because each grain carries the tract's response", WHITE),
            (r"spectral shifters separate the envelope by linear prediction or the cepstrum, \ shift the rest, \ and put the envelope back", WHITE),
            (r"shift the formants alone and the same singer sounds larger or smaller, \ older or younger", TUNE),
            (r"Part 8's model made this a matter of two numbers; \ here it is done to a recording", GREY_A),
        ]
        rows_scene(self, r"pitch and formants", items,
                   "Why does PSOLA keep the vowel? <bookmark mark='b'/> A voice is a source and a filter, as Part 8 showed: the "
                   "vocal folds set the pitch, and the vocal tract sets the formants. <bookmark mark='c'/> Resampling moves both; "
                   "PSOLA moves only the pitch, because each grain carries the tract's response with it. <bookmark mark='d'/> "
                   "Spectral shifters separate the envelope by linear prediction or the cepstrum, shift the rest, and put the "
                   "envelope back. <bookmark mark='e'/> Shift the formants alone, and the same singer sounds larger or smaller, "
                   "older or younger. <bookmark mark='f'/> Part 8's model made this a matter of two numbers; here it is done to a "
                   "recording.", marks="bcdef")
