from __future__ import annotations

import numpy as np

from videos.music.music40.common import *  # noqa: F403


class Loops(SoundScene):
    def construct(self):
        chapter(self, 2, r"Loops and rock harmony", r"What happens to harmony when it goes round in a circle?")
        self.loops()
        self.hear()
        self.divorce()
        self.modes()
        self.circle()

    # ------------------------------------------------------------------
    def loops(self):
        d = load("loops")
        rows_ = VGroup()
        notes = {"I-V-vi-IV": r"the four-chord loop of countless choruses",
                 "bVII-IV-I": r"`double plagal': \ falling fourths into the tonic, \ mixolydian rock",
                 "i-bVI-bIII-bVII": r"the aeolian loop: \ minor, \ never reaching a dominant"}
        for k, (name, chords) in enumerate(d["loops"].items()):
            ch = chart([[c] for c in chords], cell_w=1.6, cell_h=0.6, size=20)
            nm = name.replace("b", r"$\flat$").replace("-", r"--")
            rows_.add(VGroup(label(nm, font_size=20, color=VOICE_C[k]), ch, label(notes[name], font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.4))
        rows_.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(DOWN * 0.1)
        rows_.scale_to_fit_width(min(rows_.width, 13.2))
        head = label(r"three loops", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Much rock and pop harmony is a loop: a few chords repeated, rather than a progression going somewhere. "
            "<bookmark mark='a'/> One, five, six, four: the four-chord loop under countless choruses. "
            "<bookmark mark='b'/> Flat seven, four, one: chords falling by fourths into the tonic, the double plagal motion "
            "of mixolydian rock. <bookmark mark='c'/> And the aeolian loop, minor, one, flat six, flat three, flat seven, "
            "which never reaches a dominant at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.2)))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("loops")
        c = clip("loops.three")
        rows_ = VGroup()
        for k, (name, chords) in enumerate(d["loops"].items()):
            ch = chart([[x] for x in chords], cell_w=1.9, cell_h=0.6, size=20)
            rows_.add(VGroup(label(name.replace("b", r"$\flat$").replace("-", r"--"), font_size=19, color=VOICE_C[k]), ch).arrange(RIGHT, buff=0.4))
        rows_.arrange(DOWN, buff=0.45, aligned_edge=RIGHT).move_to(UP * 0.2)
        with self.voiceover(
            "Hear each twice round, with guitar, bass and drums. Notice that none of them feels finished at the end of the "
            "loop: each one simply goes round again."
        ):
            self.play(FadeIn(rows_))
        bar = 4 * 60.0 / d["bpm"]
        with self.listen(c) as snd:
            window(snd, r"three loops", detail=r"plucked-string guitar and bass, \ drums", corner=DL, tag_corner=DR)
            for k, name in enumerate(d["loops"]):
                t0 = d["starts"][name]
                for b in range(8):
                    pulse(snd, rows_[k][1].bars[b % 4], t0 + b * bar, t0 + (b + 1) * bar - 0.03, buff=0.03)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def divorce(self):
        d = load("loops")
        dv = d["divorce"]
        items = [
            (r"David Temperley \ (2007): \ in rock, \ melody and harmony often go their own ways", WHITE),
            (r"melody notes on strong beats are often not in the chord: \ the `melodic-harmonic divorce'", WHITE),
            (rf"in our chorus hook over I--V--vi--IV: \ {dv['outside']} of its {dv['on_beat']} notes on the beat are outside the chord", WHITE),
            (r"non-chord tones require contextual analysis in either style", TUNE),
            (r"the melody follows the scale, \ the chords follow the loop", GREY_A),
        ]
        rows_scene(self, r"melody and harmony, \ divorced", items,
                   f"Over a loop, the melody is freer. <bookmark mark='b'/> The theorist David Temperley pointed out in 2007 that in rock, melody notes on strong beats are often not in the chord, a melodic-harmonic divorce. <bookmark mark='c'/> Monochord counts our own chorus hook over one, five, six, four: {say(dv['outside'])} of its {say(dv['on_beat'])} notes on the beat lie outside the chord. <bookmark mark='d'/> A chorale analysis would inspect preparation, duration and resolution before judging such notes; the count alone does not identify errors in either style. <bookmark mark='e'/> The melody follows the scale, and the chords follow the loop.", marks="bcde")

    # ------------------------------------------------------------------
    def modes(self):
        items = [
            (r"Temperley's rock scales: \ major, \ mixolydian \ (flat seventh), \ aeolian \ (natural minor), \ and the pentatonics", WHITE),
            (r"the flat seventh chord \ (B$\flat$ in C) \ is rock's signature: \ the blues's seventh \ (Part 38) \ made a chord", WHITE),
            (r"melodies often use the minor pentatonic over major chords: \ the blues third again", WHITE),
            (r"Part 12's modes, \ used within varied tonal and modal practices", TUNE),
            (r"the harmony serves the riff and the voice", GREY_A),
        ]
        rows_scene(self, r"rock's scales", items,
                   "Which scales does rock use? <bookmark mark='b'/> Temperley's survey finds the major scale, the mixolydian with "
                   "its flat seventh, the aeolian or natural minor, and the pentatonics. <bookmark mark='c'/> The flat seventh "
                   "chord, B flat in C, is rock's signature: the blues's seventh from Part 38, made into a chord. "
                   "<bookmark mark='d'/> Melodies often use the minor pentatonic over major chords, the blue third again. "
                   "<bookmark mark='e'/> These are Part 12's modes, used within varied tonal and modal practices. "
                   "<bookmark mark='f'/> The harmony serves the riff and the voice.", marks="cdef")

    # ------------------------------------------------------------------
    def circle(self):
        items = [
            (r"a progression \ (Part 18) \ goes somewhere: \ tension, \ then arrival at the tonic", WHITE),
            (r"a loop repeats; \ a tonic or goal may still be heard", WHITE),
            (r"rock prefers the plagal \ (IV--I) \ and the flat seventh to the dominant's pull", WHITE),
            (r"form then comes from the arrangement: \ who plays, \ how loud, \ how dense", TUNE),
            (r"chapter 3: \ the loop at its most physical, \ the riff", GREY_A),
        ]
        rows_scene(self, r"progressions and loops", items,
                   "There is a difference in kind here. <bookmark mark='b'/> A progression, as in Part 18, goes somewhere: tension, then arrival at the tonic. <bookmark mark='c'/> A loop repeats, though listeners may still hear a tonic or goal within it; an arrangement can end it or fade it out. <bookmark mark='d'/> Rock prefers the plagal, four to one, and the flat seventh to the dominant's pull. <bookmark mark='e'/> So form comes from the arrangement: who plays, how loud, how dense. <bookmark mark='f'/> Chapter three turns to the loop at its most physical, the riff.", marks="cdef")
