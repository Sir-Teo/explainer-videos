from __future__ import annotations

import numpy as np

from videos.music.music32.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ what the geometry does not explain", r"Is the shortest path what we hear?")
        self.blind()
        self.debate()
        self.other()
        self.problem()
        self.tunings()

    # ------------------------------------------------------------------
    def blind(self):
        items = [
            (r"function: \ G to C moves 3 semitones, \ G to E$\flat$ only 2; \ the first is the cadence", WHITE),
            (r"the bass: \ chord space treats every voice alike; \ music does not", WHITE),
            (r"register and spacing: \ octave equivalence throws them away", WHITE),
            (r"rhythm and metre: \ a path has no strong beats", TUNE),
            (r"timbre: \ Part 5's roughness depends on the spectrum, \ not the pitch classes", GREY_A),
        ]
        rows_scene(self, r"what the geometry cannot see", items,
                   "The geometry is powerful, and blind in places. <bookmark mark='b'/> It does not see function: G major to C "
                   "major moves three semitones, G major to E flat major only two, yet the first is the strongest cadence in "
                   "tonal music and the second a surprise. <bookmark mark='c'/> It treats every voice alike, while music gives the bass a different job. "
                   "<bookmark mark='d'/> Octave equivalence throws away register and spacing. <bookmark mark='e'/> A path has no "
                   "strong beats. <bookmark mark='f'/> And Part 5's roughness depends on the spectrum, which pitch classes alone "
                   "do not record.", marks="cdef")

    # ------------------------------------------------------------------
    def debate(self):
        items = [
            (r"Tymoczko \ (2006, \ 2011): \ five features of tonality, \ one geometry", WHITE),
            (r"critics: \ the spaces are elegant, \ but does the ear use them? \ (Hook; \ Cohn; \ Lerdahl)", WHITE),
            (r"the geometry also says which music is possible: \ chromatic voice leading in Chopin, \ Debussy, \ jazz", WHITE),
            (r"perception studies of voice-leading size are still few", TUNE),
            (r"a theory can be useful to composers before it is confirmed for listeners", GREY_A),
        ]
        rows_scene(self, r"the argument", items,
                   "The theory started an argument. <bookmark mark='b'/> Tymoczko's book of 2011 explains five features of tonal "
                   "music with one geometry. <bookmark mark='c'/> Critics, among them Julian Hook, Richard Cohn and Fred Lerdahl, "
                   "admired the spaces but asked whether listeners use them, and whether other spaces explain as much. "
                   "<bookmark mark='d'/> The geometry also maps what is possible: chromatic voice leading in Chopin, Debussy and "
                   "jazz finds natural descriptions in it. <bookmark mark='e'/> But studies of how listeners hear voice-leading "
                   "size are still few. <bookmark mark='f'/> A theory can be useful to composers long before it is confirmed for "
                   "listeners.", marks="cdef")

    # ------------------------------------------------------------------
    def other(self):
        items = [
            (r"Part 31's Tonnetz: \ moves, \ not semitones", WHITE),
            (r"Fourier spaces: \ qualities, \ not paths \ (chapter 8)", WHITE),
            (r"Lerdahl's tonal pitch space: \ distances learned from keys and chords \ (Part 19)", WHITE),
            (r"learned embeddings: \ spaces fitted to millions of chord sequences \ (Part 62)", TUNE),
            (r"each is a hypothesis about what makes two chords close", GREY_A),
        ]
        rows_scene(self, r"rival geometries", items,
                   "And it is not the only geometry. <bookmark mark='b'/> Part 31's Tonnetz counts moves, not semitones. "
                   "<bookmark mark='c'/> Fourier spaces measure qualities, not paths. <bookmark mark='d'/> Lerdahl's tonal pitch "
                   "space, from Part 19, measures distances between keys and chords. <bookmark mark='e'/> Learned embeddings fit a "
                   "space to millions of chord sequences, as Part 62 will. <bookmark mark='f'/> Each is a hypothesis about what "
                   "makes two chords close.", marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"choose pairs of progressions that are equally short in one space and not in another", WHITE),
            (r"ask listeners which is smoother, \ and which belongs together, \ with register and timbre controlled", WHITE),
            (r"fit each geometry's distance to the judgements, \ and compare on held-out pairs, \ with intervals", WHITE),
            (r"$\bigstar$ \ research problem: \ does voice-leading size predict how smooth a progression sounds?", EAR),
            (r"the answer decides whether the geometry is a theory of listening or of writing", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Choose pairs of progressions that are equally short in one space and "
            "not in another. <bookmark mark='b'/> Ask listeners which is smoother, and which chords belong together, with "
            "register and timbre held fixed. <bookmark mark='c'/> Fit each geometry's distance to the judgements and compare "
            "them on pairs held out, with intervals. <bookmark mark='d'/> Does voice-leading size predict how smooth a "
            "progression sounds? <bookmark mark='e'/> The answer decides whether this geometry is a theory of listening, or "
            "of writing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tunings(self):
        items = [
            (r"nothing in the geometry needs twelve-note equal temperament", WHITE),
            (r"in 19 equal steps the thirds are nearly pure, \ and the nearly even chords change", WHITE),
            (r"spectral chords \ (Part 30) \ and just intonation \ (Part 6) \ are points between the keys", WHITE),
            (r"composers now use the spaces to find voice leadings in tunings no one has played much", TUNE),
            (r"a fair test of the theory: \ does it predict which tunings make good harmony?", GREY_A),
        ]
        rows_scene(self, r"beyond twelve notes", items,
                   "One more direction. <bookmark mark='b'/> Nothing in the geometry needs twelve-note equal temperament. <bookmark mark='c'/> In nineteen equal steps the thirds are nearly pure, and the nearly even chords are different ones. <bookmark mark='d'/> Spectral chords from Part 30 and just intonation from Part 6 are points between the piano's keys. <bookmark mark='e'/> Composers now use these spaces to find voice leadings in tunings few have played. <bookmark mark='f'/> And that suggests a fair test: does the theory predict which tunings make good harmony?", marks="cdef")
