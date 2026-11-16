from __future__ import annotations

import numpy as np

from videos.music.music67.common import *  # noqa: F403


class Field(SoundScene):
    def construct(self):
        chapter(self, 4, r"Fieldwork and ethics", r"Who speaks for a music, \ and who owns its recordings?")
        self.fieldwork()
        self.ethics()
        self.transcription()
        self.notation()

    # ------------------------------------------------------------------
    def fieldwork(self):
        items = [
            (r"ethnomusicology learns a music by taking part in it: \ lessons, \ performances, \ years in one place \ (Nettl)", WHITE),
            (r"the researcher is part of the evidence: \ who they talked to, \ what they were allowed to hear", WHITE),
            (r"insider and outsider: \ musicians are also scholars of their own music, \ and increasingly the authors", WHITE),
            (r"Act VI's raga, \ maqam, \ gamelan and polyrhythm came to Western study this way, \ with their own theories first", TUNE),
        ]
        rows_scene(self, r"fieldwork", items,
                   "Ethnomusicology learns a music by taking part in it: lessons, performances, often years in one place, as Bruno "
                   "Nettl described. <bookmark mark='b'/> The researcher is part of the evidence: who they talked to, what they were "
                   "allowed to hear. <bookmark mark='c'/> And the line between insider and outsider has moved: musicians are "
                   "scholars of their own music, and increasingly its authors in print. <bookmark mark='d'/> Act Six's raga, "
                   "maqam, gamelan and polyrhythm came to Western study this way, each with its own theory first.", marks="bcd")

    # ------------------------------------------------------------------
    def ethics(self):
        items = [
            (r"consent: \ recording a ceremony or a song may need the community's permission, \ not only the singer's", WHITE),
            (r"archives: \ early twentieth-century collectors took cylinders home; \ many are now being returned \ (repatriation)", WHITE),
            (r"credit and pay: \ field recordings have been sampled into hits whose sources were never paid \ (Part 60's rights)", WHITE),
            (r"the same questions as Part 66's training data: \ whose music, \ on what terms", TUNE),
        ]
        rows_scene(self, r"ethics", items,
                   "Fieldwork has an ethics older than machine learning's. <bookmark mark='b'/> Consent: recording a ceremony or a "
                   "song may need a community's permission, not only the singer's. <bookmark mark='c'/> Archives: early "
                   "twentieth-century collectors took wax cylinders home, and many are now being returned to the communities they "
                   "came from. <bookmark mark='d'/> Credit and pay: field recordings have been sampled into hits whose sources were "
                   "never paid, the rights of Part 60 ignored. <bookmark mark='e'/> They are the same questions as Part 66's "
                   "training data: whose music, and on what terms.", marks="bcde")

    # ------------------------------------------------------------------
    def transcription(self):
        items = [
            (r"transcription is interpretation: \ staff notation decides what counts as a note, \ a pitch, \ a beat", WHITE),
            (r"Bartók transcribed folk songs with extraordinary detail; \ his choices still shaped what could be seen \ (Part 28)", WHITE),
            (r"Seeger's distinction \ (1958): \ prescriptive notation tells a performer, \ descriptive notation describes a performance", WHITE),
            (r"Part 61's machines face the same choices, \ silently: \ a note grid, \ twelve pitches, \ onsets and offsets", TUNE),
        ]
        rows_scene(self, r"transcription", items,
                   "And transcription is interpretation. <bookmark mark='b'/> Staff notation decides what counts as a note, a pitch "
                   "and a beat. <bookmark mark='c'/> Bartók transcribed folk songs in extraordinary detail, and his choices still "
                   "shaped what could be seen in them. <bookmark mark='d'/> Charles Seeger distinguished, in 1958, prescriptive "
                   "notation, which tells a performer what to do, from descriptive notation, which describes what a performer did. "
                   "<bookmark mark='e'/> Part 61's machines make the same choices silently: a grid of notes, twelve pitches to the "
                   "octave, onsets and offsets.", marks="bcde")

    # ------------------------------------------------------------------
    def notation(self):
        d = load("notation")
        c = clip("notation.one")
        tr = np.array(d["track"])
        t = np.array(d["t"])
        ax = frame_axes(width=10.0, height=2.6, xlo=0, xhi=t.max(), ylo=tr.min() - 0.5, yhi=tr.max() + 0.5, center=UP * 0.6)
        cv = curve(t, tr, ax.to, color=TUNE, width=2)
        bars = VGroup(*[Line(ax.to(a, m), ax.to(a + dd, m), color=WHITE, stroke_width=4) for m, a, dd in d["notes"]])
        lab = label(r"gold: \ the voice's pitch, \ by YIN; \ white: \ the notes a transcription writes", font_size=15, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        res = VGroup(label(rf"only {100 * d['within10']:.0f}\% of the voice's moments are within 10 cents of a written note; \ {100 * d['within25']:.0f}\% within 25", font_size=18, color=TUNE),
                     label(r"the vibrato, \ the glides, \ the slightly flat arrival: \ everything a performer adds", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        head = label(r"what notation discards", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover("Measure what notation discards. Here is the Tune's first phrase sung with a wide vibrato and slow glides, its pitch tracked, against the notes a transcription would write."):
            self.play(FadeIn(head), FadeIn(ax), FadeIn(bars), FadeIn(lab))
        with self.listen(c) as snd:
            window(snd, r"sung", kind="synthesized", detail=r"Part 8's alto", corner=DL, tag_corner=DR)
            snd.show(cv)
            marker = VGroup(Line(DOWN * 1.3, UP * 1.3, color=WHITE, stroke_width=3), Dot(radius=0.08, color=WHITE))
            snd.show(marker)
            snd.drive(marker, lambda m, tt: m.move_to(ax.to(np.clip(tt, 0, t.max()), (tr.min() + tr.max()) / 2)))
        self.add(cv)
        with self.voiceover(
            f"Only {say(round(100 * d['within10']))} per cent of the voice's moments sit within ten cents of the written note, "
            f"and {say(round(100 * d['within25']))} per cent within a quarter of a semitone. The rest is vibrato, glide and "
            "arrival: everything the performer added, and details a basic note-only transcription omits; richer notation can indicate some of them."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()
