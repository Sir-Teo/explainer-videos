from __future__ import annotations

import numpy as np

from videos.music.music27.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ harmony and performance as data", r"What can thousands of pieces, \ and of recordings, \ tell us?")
        self.corpora()
        self.audio()
        self.recordings()
        self.problem()

    # ------------------------------------------------------------------
    def corpora(self):
        items = [
            (r"symbolic corpora: \ scores encoded note by note \ (Humdrum, \ MusicXML, \ music21)", WHITE),
            (r"expert harmonic analyses as data: \ Roman numerals for whole repertoires, \ checked by hand", WHITE),
            (r"questions like this part's: \ how fast did chord vocabularies grow, \ and where?", WHITE),
            (r"the bottleneck is encoding: \ most of the century's music is not yet in a machine-readable score", TUNE),
            (r"chapter seven's Library: \ 827 pieces, \ accidental; \ the frontier wants tens of thousands, \ chosen", GREY_A),
        ]
        rows_scene(self, r"the century as a corpus", items,
                   "Chapter seven was a small version of a real research programme. <bookmark mark='b'/> Symbolic corpora "
                   "are scores encoded note by note, in formats like Humdrum and MusicXML, read by tools like music21. "
                   "<bookmark mark='c'/> Some also carry expert harmonic analyses, Roman numerals for whole repertoires, "
                   "checked by hand. <bookmark mark='d'/> With them one can ask how fast the chord vocabulary grew, and in "
                   "which genres and places. <bookmark mark='e'/> The bottleneck is encoding: most of the century's music is "
                   "still not in a machine-readable score. <bookmark mark='f'/> This part's Library was eight hundred "
                   "accidental pieces; the frontier wants tens of thousands, chosen.", marks="cdef")

    # ------------------------------------------------------------------
    def audio(self):
        items = [
            (r"or start from sound: \ chroma features \ (Part 21) \ from thousands of recordings", WHITE),
            (r"Weiß, \ Mauch, \ Dixon and Müller \ (2019): \ about 2,000 recorded pieces from 1600 to 1910", WHITE),
            (r"their measures of tonal complexity rise across the eras, \ fastest in the late Romantic", WHITE),
            (r"recordings bring performance into the measure, \ and recording-era biases with it", TUNE),
            (r"scores and audio together: \ each checks the other's errors", GREY_A),
        ]
        rows_scene(self, r"from audio", items,
                   "Another route starts from the sound. <bookmark mark='b'/> Chroma features, which Part 21 computed, can be "
                   "taken from thousands of recordings. <bookmark mark='c'/> Christof Weiß and colleagues did this in 2019 "
                   "for about two thousand recorded pieces composed between 1600 and 1910, <bookmark mark='d'/> and found "
                   "their measures of tonal complexity rising across the eras, most steeply towards the end of the Romantic "
                   "period: the same shape as chapter seven, from very different data. <bookmark mark='e'/> Recordings bring "
                   "performance into the measurement, and the biases of what gets recorded. <bookmark mark='f'/> Scores and "
                   "audio together check each other's errors.", marks="cdef")

    # ------------------------------------------------------------------
    def recordings(self):
        items = [
            (r"the earliest recordings, \ from about 1900, \ preserve players trained in the 1850s", WHITE),
            (r"Robert Philip \ (1992), \ Daniel Leech-Wilkinson \ (2009): \ style changed more than anyone remembered", WHITE),
            (r"more rubato, \ freer tempo, \ less vibrato, \ more portamento", WHITE),
            (r"measured beat by beat, \ these recordings test what the treatises say", TUNE),
            (r"the century's own sound is partly recoverable, \ and it surprises", GREY_A),
        ]
        rows_scene(self, r"the oldest performers we can hear", items,
                   "The early recordings are the other great archive. <bookmark mark='b'/> Made from about 1900, they "
                   "preserve players who were trained in the middle of the nineteenth century. <bookmark mark='c'/> The "
                   "historians Robert Philip and Daniel Leech-Wilkinson have shown how much playing style changed, more than "
                   "anyone remembered: <bookmark mark='d'/> more rubato, freer tempos, less continuous vibrato, more sliding "
                   "between notes. <bookmark mark='e'/> Measured beat by beat, those recordings test what the treatises claim. "
                   "<bookmark mark='f'/> Part of the century's own sound can be recovered, and it surprises.", marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"take the Library's measures to a large, \ chosen corpus with dates and genres", WHITE),
            (r"model chromaticism by year, \ genre and composer, \ with composers as random effects", WHITE),
            (r"ask: \ is the rise steady, \ or concentrated in a few composers and decades?", WHITE),
            (r"$\bigstar$ \ research problem: \ when, \ and in which genres, \ did nineteenth-century harmony change fastest?", EAR),
            (r"an answer with intervals, \ not anecdotes, \ would rewrite a familiar story", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Take this part's two measures to a large corpus, chosen so that dates "
            "and genres are balanced. <bookmark mark='b'/> Model chromaticism by year and genre, with each composer as a "
            "random effect, as the statistics series does. <bookmark mark='c'/> Then ask whether the rise is steady, or "
            "concentrated in a few composers and a few decades. <bookmark mark='d'/> When, and in which genres, did "
            "nineteenth-century harmony change fastest? <bookmark mark='e'/> An answer with intervals rather than "
            "anecdotes would rewrite one of music history's most familiar stories."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
