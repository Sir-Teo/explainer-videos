from __future__ import annotations

import numpy as np

from videos.music.music62.common import *  # noqa: F403


class Chroma(SoundScene):
    def construct(self):
        chapter(self, 5, r"Chroma", r"How can a spectrogram be folded into twelve notes?")
        self.fold()
        self.picture_()
        self.variants()
        self.templates()
        self.uses()

    # ------------------------------------------------------------------
    def fold(self):
        items = [
            (r"harmony cares about pitch classes, \ not octaves: \ C is C in any register", WHITE),
            (r"so fold the log-frequency spectrogram: \ add every C together, \ every C$\sharp$, \dots, \ every B", WHITE),
            (r"twelve numbers a frame: \ the chroma vector \ (Shepard's helix, \ Part 6, \ flattened)", WHITE),
            (r"compress, \ and normalize each frame, \ so that harmony counts more than loudness", WHITE),
            (r"partials leak: \ a C's third partial is a G, \ its fifth an E; \ chroma blurs every note into its own triad", TUNE),
        ]
        rows_scene(self, r"folding octaves", items,
                   "For harmony the machine needs a different picture. <bookmark mark='b'/> Harmony cares about pitch classes, not "
                   "octaves: C is C in any register. <bookmark mark='c'/> So fold the log-frequency spectrogram: add every C "
                   "together, every C sharp, and so on up to B. <bookmark mark='d'/> Twelve numbers a frame: the chroma vector, "
                   "Shepard's pitch helix from Part 6, flattened. <bookmark mark='e'/> Compress it, and normalize each frame, so "
                   "that harmony counts more than loudness. <bookmark mark='f'/> One complication: partials leak. A C's third "
                   "partial is a G and its fifth an E, so chroma blurs every note toward its own major triad.", marks="bcdef")

    # ------------------------------------------------------------------
    def picture_(self):
        d = load("chords")
        c = clip("chords.tune")
        Cm = np.array(d["chroma"])
        w, h = 10.5, 3.0
        pic = picture(Cm, 0, 1, w, h).move_to(DOWN * 0.2 + RIGHT * 0.3)
        names = ["C", r"C$\sharp$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]
        rows_ = VGroup(*[label(n, font_size=13, color=TUNE if k in (0, 5, 7) else GREY_A).move_to([pic.get_left()[0] - 0.3, pic.get_bottom()[1] + h * (k + 0.5) / 12, 0]) for k, n in enumerate(names)])
        syms = d["syms"][:8]
        dur = Cm.shape[1] * d["hop_s"]
        chords_ = VGroup(*[label(s, font_size=18, color=TUNE).move_to([pic.get_left()[0] + w * (i + 0.5) * 1.2 / dur, pic.get_top()[1] + 0.3, 0]) for i, s in enumerate(syms)])
        note = label(r"the chords played, \ above; \ the louder voice lights one row at a time", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"the Tune's chroma", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here is the chroma of the session playing the Tune's opening, with the voice loud and the chords quiet, as a singer hears it."):
            self.play(FadeIn(head), FadeIn(pic), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"the Tune's opening", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            line = Line(pic.get_corner(DL), pic.get_corner(UL), color=WHITE, stroke_width=2)
            snd.show(line)
            x0 = pic.get_left()[0]
            snd.drive(line, lambda m, t: m.move_to([x0 + w * min(t, dur) / dur, pic.get_center()[1], 0]))
        with self.voiceover("The chords, C, F and G, show as rows that change every two beats. But the voice is louder than the chords, and its notes light their own rows, one at a time: the chroma looks as much like a melody as like a harmony. That is the chord recognizer's difficulty."):
            self.play(FadeIn(chords_), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def variants(self):
        items = [
            (r"1999: \\ Fujishima's pitch class profile, \\ the first chroma for chord recognition", WHITE),
            (r"tuning: \\ a band tuned 30 cents flat smears every bin; \\ estimate the tuning first and shift", WHITE),
            (r"HPCP \\ (Gómez, \\ 2006) \\ weights each peak's harmonics; \\ CENS \\ (Müller, \\ 2005) \\ smooths for matching", WHITE),
            (r"or learn the chroma: \\ a network trained to output the notes' pitch classes, \\ not the partials'", TUNE),
        ]
        rows_scene(self, r"chroma's relatives", items,
                   "Chroma has relatives. <bookmark mark='b'/> Takuya Fujishima's pitch class profile of 1999 was the first chroma used to "
                   "recognize chords. <bookmark mark='c'/> Tuning matters: a band tuned thirty cents flat smears every bin, so "
                   "systems estimate the tuning first and shift. <bookmark mark='d'/> Emilia Gómez's HPCP weights each peak and its "
                   "harmonics; Meinard Müller's CENS smooths chroma for matching. <bookmark mark='e'/> Or the chroma can be learnt: "
                   "a network trained to output the pitch classes of the notes, not of their partials.", marks="bcde")

    # ------------------------------------------------------------------
    def uses(self):
        items = [
            (r"keys: \ Part 15's key finder runs on chroma averaged over a passage", WHITE),
            (r"alignment and covers: \ Chapters 7 and 10 compare chroma sequences", WHITE),
            (r"structure: \ Chapter 9's self-similarity is chroma against chroma", WHITE),
            (r"what chroma throws away: \ the octave, \ the timbre, \ the rhythm; \ for harmony that is the point", TUNE),
        ]
        rows_scene(self, r"what else chroma is for", items,
                   "Chroma carries the rest of this part too. <bookmark mark='b'/> Part 15's key finder runs on chroma averaged over "
                   "a passage. <bookmark mark='c'/> Chapters 7 and 10 align recordings and match covers by comparing chroma "
                   "sequences. <bookmark mark='d'/> And Chapter 9's self-similarity is chroma against chroma. "
                   "<bookmark mark='e'/> Chroma throws away the octave, the timbre and the rhythm; for harmony, that is the point.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def templates(self):
        lines = VGroup(
            label(r"a template per chord: \ ones on its three pitch classes", font_size=21, color=WHITE),
            MathTex(r"\mathbf{t}_{\mathrm{C}} = (1,0,0,0,1,0,0,1,0,0,0,0), \quad \mathbf{t}_{\mathrm{Am}} = (1,0,0,0,1,0,0,0,0,1,0,0)", font_size=30, color=TUNE),
            label(r"24 triads, \ major and minor on every root, \ and `no chord'", font_size=20, color=WHITE),
            MathTex(r"\hat c(t) = \arg\max_c\ \cos\big(\mathbf{t}_c, \mathbf{x}(t)\big)", font_size=34, color=WHITE),
            label(r"C major and A minor share two notes: \ one melody note can tip the balance", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        head = label(r"chord templates", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The simplest recognizer matches templates. <bookmark mark='a'/> Each chord is a template with ones on its three "
            "pitch classes. <bookmark mark='b'/> Twenty-four triads, major and minor on every root, and one for no chord. "
            "<bookmark mark='c'/> In each frame, pick the template closest in angle to the chroma. <bookmark mark='d'/> But C "
            "major and A minor share two notes, and one melody note can tip the balance."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]))
            vo.wait_until("c")
            self.play(FadeIn(lines[3]))
            vo.wait_until("d")
            self.play(FadeIn(lines[4]))
        self.wait(0.4)
        self.clear_scene()
