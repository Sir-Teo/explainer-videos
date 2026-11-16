from __future__ import annotations

import numpy as np

from videos.music.music32.common import *  # noqa: F403

QUAL = {1: r"chromatic \ (clusters)", 2: r"two poles a tritone apart", 3: r"major thirds \ (augmented, \ hexatonic)",
        4: r"minor thirds \ (diminished, \ octatonic)", 5: r"fifths \ (diatonic, \ pentatonic)", 6: r"whole tones"}


class Fourier(SoundScene):
    def construct(self):
        chapter(self, 8, r"What each Fourier coefficient hears", r"Can a chord have a spectrum?", extra=((1959, r"Lewin's interval function"),))
        self.idea()
        self.portraits()
        self.quiz()
        self.history()
        self.phases()

    # ------------------------------------------------------------------
    def idea(self):
        rows_ = text_rows([
            (r"write a chord as twelve numbers: \ 1 where a pitch class sounds, \ 0 where it does not", WHITE),
            (r"take the discrete Fourier transform, \ as Part 3 did for sound \ ---\ but round the octave", WHITE),
            (r"$|F_k|$ asks: \ how well does the chord fit a perfectly even division of the octave into $k$ parts?", TUNE),
            (r"$|F_3|$: \ thirds of an octave, \ major thirds; \ $|F_5|$: \ the circle of fifths; \ $|F_6|$: \ whole tones", WHITE),
            (r"the magnitudes ignore transposition and inversion: \ one profile per set class \ (nearly)", GREY_A),
        ], font_size=24)
        head = label(r"a chord's spectrum", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "There is another geometry hidden in a chord. <bookmark mark='a'/> Write the chord as twelve numbers, one for "
            "each pitch class: one where a note sounds, zero where it does not. <bookmark mark='b'/> Then take the discrete "
            "Fourier transform, as Part 3 did for sound, but round the circle of the octave instead of along time. "
            "<bookmark mark='c'/> The size of the k-th coefficient measures how well the chord lines up with a perfectly even "
            "division of the octave into k parts. <bookmark mark='d'/> The third coefficient hears major thirds, the fifth, "
            "through a twist of arithmetic, hears the circle of fifths, and the sixth hears whole tones. "
            "<bookmark mark='e'/> And the sizes do not change under transposition or inversion, so each set class has one "
            "profile, as Part 29's homometric pairs showed, two classes can share one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def portraits(self):
        d = load("fourier")
        names = ["major", "augmented", "diminished seventh", "diatonic", "whole tone", "cluster"]
        shown = {"major": r"major triad", "augmented": r"augmented triad", "diminished seventh": r"diminished seventh",
                 "diatonic": r"diatonic scale", "whole tone": r"whole-tone scale", "cluster": r"cluster C C$\sharp$ D E$\flat$"}
        cells = VGroup()
        for n in names:
            mags = d["mags"][n][1:]
            top = max(mags)
            b = columns(mags, [str(k) for k in range(1, 7)], width=3.0, height=1.4, color=GREY_B, hot=tuple(i for i, m in enumerate(mags) if m > top - 1e-6),
                        hot_color=TUNE, font_size=14)
            cells.add(VGroup(label(shown[n], font_size=19, color=WHITE), b).arrange(DOWN, buff=0.25))
        cells.arrange_in_grid(rows=2, buff=(0.8, 0.6)).move_to(DOWN * 0.2)
        head = label(r"six chords, \ six Fourier profiles: \ $|F_1| \ldots |F_6|$", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Six portraits. <bookmark mark='a'/> The augmented triad lives entirely in the third and sixth coefficients: it "
            "is a perfect division of the octave into three. The diminished seventh lives in the fourth. <bookmark mark='b'/> "
            "The diatonic scale peaks at the fifth: it is a stretch of the circle of fifths. The whole-tone scale has "
            "nothing but the sixth. <bookmark mark='c'/> The cluster peaks at the first, the coefficient of chromatic "
            "crowding. And the major triad spreads its weight over the third and fifth: a little augmented, a little "
            "diatonic, which is one way to say why it serves in so many contexts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells[0]))
            vo.wait_until("a")
            self.play(FadeIn(cells[1]), FadeIn(cells[2]))
            vo.wait_until("b")
            self.play(FadeIn(cells[3]), FadeIn(cells[4]))
            vo.wait_until("c")
            self.play(FadeIn(cells[5]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("fourier")
        c = clip("fourier.quiz")
        card = listen_card(r"Three six-note chords. \ One is built only from the circle of fifths; \ "
                           r"one only from major thirds and semitones; \ one only from whole tones. \ "
                           r"Which is the fifths chord, \ A, \ B or C?", width=10.4)
        with self.voiceover(
            "A question for your ears. Three six-note chords, each held twice. One is built entirely from the circle of "
            "fifths, one from major thirds and semitones, one from whole tones. Which is the fifths chord: A, B or C?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        cells = VGroup(*[label(k, font_size=44, color=GREY_A) for k in "ABC"]).arrange(RIGHT, buff=3.0).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ C", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate("ABC"):
                end = d["starts"]["ABC"[i + 1]] - 0.5 if i < 2 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.12)
        names = {"hexatonic": r"hexatonic", "pentatonic": r"pentatonic", "whole tone": r"whole-tone"}
        ans = VGroup(*[VGroup(label(names[n], font_size=21, color=TUNE if "ABC"[i] == d["answer"] else GREY_A),
                              label(rf"$|F_3|$ {d['f3'][i]:.1f}, \ $|F_5|$ {d['f5'][i]:.1f}, \ $|F_6|$ {d['f6'][i]:.1f}", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.15).next_to(cells[i], DOWN, buff=0.4)
                       for i, n in enumerate(d["order"])])
        with self.voiceover(
            'B: the pentatonic chord, C, D, E, G, A over a low G, the bright open sound of fifths, with a fifth coefficient of three point seven and none of the others large. A is the hexatonic chord, all third coefficient and no fifth at all; C is the whole-tone chord, nothing but the sixth. These sketches invite a comparison of pitch-set qualities; this informal question does not establish that listeners directly compute Fourier coefficients. The transform uses distinct pitch classes, so the doubled G in B is counted once.'
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"David Lewin \ (1959): \ the interval function, \ in effect a Fourier idea", WHITE),
            (r"Ian Quinn \ (2006): \ Fourier `qualities' map the set classes", WHITE),
            (r"Emmanuel Amiot, \ \textit{Music Through Fourier Space} \ (2016); \ Jason Yust's tonal analyses", WHITE),
            (r"Part 29: \ homometric sets share every $|F_k|$; \ the phases tell them apart", TUNE),
            (r"the open question: \ do listeners hear the coefficients, \ or the coefficients describe what they hear?", GREY_A),
        ]
        rows_scene(self, r"Fourier in music theory", items,
                   "The idea has a history. <bookmark mark='b'/> David Lewin used it, in effect, in 1959. <bookmark mark='c'/> "
                   "Ian Quinn in 2006 showed that the Fourier magnitudes map out the set classes as qualities: fifthiness, "
                   "thirdiness and the rest. <bookmark mark='d'/> Emmanuel Amiot's book of 2016 and Jason Yust's analyses use "
                   "them to describe tonal and post-tonal music. <bookmark mark='e'/> Part 29's homometric pairs share every "
                   "magnitude; phases can distinguish their pitch-class arrangements; magnitudes alone cannot. <bookmark mark='f'/> And an open question: are listeners "
                   "hearing the coefficients, or do the coefficients just describe what listeners hear?", marks="cdef")

    # ------------------------------------------------------------------
    def phases(self):
        items = [
            (r"each coefficient is a complex number: \ a size and a direction", WHITE),
            (r"the direction of $F_5$ points to a place on the circle of fifths: \ a key", WHITE),
            (r"C major's scale and G major's point one twelfth of a turn apart", TUNE),
            (r"Jason Yust maps tonal pieces as paths in these phase spaces", WHITE),
            (r"sizes say what kind of chord; \ phases say where it is", GREY_A),
        ]
        rows_scene(self, r"phases: where a chord points", items,
                   "So far only the sizes. <bookmark mark='b'/> Each coefficient is a complex number, with a size and a direction. <bookmark mark='c'/> The direction of the fifth coefficient points to a place on the circle of fifths, roughly a key. <bookmark mark='d'/> The C major scale and the G major scale point one twelfth of a turn apart. <bookmark mark='e'/> Jason Yust maps whole tonal pieces as paths through these phase spaces. <bookmark mark='f'/> Sizes say what kind of chord; phases say where it is.", marks="cdef")
