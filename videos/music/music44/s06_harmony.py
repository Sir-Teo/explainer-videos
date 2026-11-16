from __future__ import annotations

import numpy as np

from videos.music.music44.common import *  # noqa: F403

NAMES = {"chromatic mediant: C to A flat": [r"C", r"A$\flat$", r"C"], "chromatic mediant: C to E": [r"C", r"E", r"C"],
         "Lydian: C and D over C": [r"C", r"D/C", r"C"], "the minor iv: C, F minor, C": [r"C", r"Fm", r"C"]}
SAYS = {"chromatic mediant: C to A flat": r"awe, \ grandeur", "chromatic mediant: C to E": r"the heroic, \ the bright",
        "Lydian: C and D over C": r"wonder, \ flight", "the minor iv: C, F minor, C": r"nostalgia, \ loss"}


class Harmony(SoundScene):
    def construct(self):
        chapter(self, 5, r"Harmony on screen", r"Is there a Hollywood harmony?")
        self.lehman()
        self.hear()
        self.why()
        self.genres()

    # ------------------------------------------------------------------
    def lehman(self):
        items = [
            (r"Frank Lehman, \ \textit{Hollywood Harmony} \ (2018): \ the chords of film scores, \ analysed like a style", WHITE),
            (r"film scores are tonal, \ but move between keys freely, \ often by chords a third apart", WHITE),
            (r"such `chromatic mediants' can keep one note with short moves in the others: \ Part 31's L, \ P and R, \ combined", WHITE),
            (r"they sound strange and inevitable at once: \ a step outside the key that the ear can follow", TUNE),
            (r"a shared vocabulary: \ certain progressions mean certain things on screen", GREY_A),
        ]
        rows_scene(self, r"Hollywood harmony", items,
                   "Is there a Hollywood harmony? <bookmark mark='b'/> Frank Lehman's book of 2018 analyses the chords of film scores as a style. <bookmark mark='c'/> Many scores in this tonal symphonic tradition move between keys freely; film music also includes other harmonic and textural practices, often by chords a third apart. <bookmark mark='d'/> Selected chromatic-mediant voicings keep one note while others move by one or two semitones, Part 31's transformations L, P and R in combination. <bookmark mark='e'/> They sound strange and inevitable at once: a step outside the key that the ear can follow. <bookmark mark='f'/> And film has built a shared vocabulary in which certain progressions mean certain things.", marks="bcdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("harmony")
        c = clip("harmony.four")
        rows_ = VGroup()
        for name in d["names"]:
            chs = VGroup(*[VGroup(RoundedRectangle(width=1.2, height=0.65, corner_radius=0.1, stroke_color=GREY_B, stroke_width=1.5),
                                  label(n, font_size=20, color=WHITE)).arrange(ORIGIN) for n in NAMES[name]]).arrange(RIGHT, buff=0.15)
            nm = label(name, font_size=18, color=TUNE)
            nm.scale_to_fit_width(min(nm.width, 4.4))
            rows_.add(VGroup(nm, chs,
                             label(SAYS[name], font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.5))
        rows_.arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        for r in rows_:
            r[0].set_x(-3.6)
            r[1].set_x(0.9)
            r[2].set_x(4.4)
        head = label(r"four progressions, \ four meanings", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear four progressions on strings and horn, each going out from C major and back. C to A flat major and back: "
            "awe and grandeur. C to E major: the bright, heroic lift. The Lydian sound, a D major chord over C, the raised "
            "fourth that scores use for wonder and flight. And the minor four, F minor in a major key, for nostalgia and "
            "loss."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"four progressions", kind="synthesized", detail=r"the additive orchestra", corner=DL, tag_corner=DR)
            for i, name in enumerate(d["names"]):
                for j in range(3):
                    t0 = st[name] + 1.4 * j
                    pulse(snd, rows_[i][1][j], t0, t0 + 1.35, buff=0.05)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"C major to A$\flat$ major: \ C stays; \ E falls to E$\flat$, \ G rises to A$\flat$ \ --- \ a smooth move to a far key", WHITE),
            (r"C to E: \ E stays; \ C falls to B, \ G rises to G$\sharp$ \ --- \ brighter, \ sharper keys", WHITE),
            (r"Lydian: \ the F$\sharp$ in D/C is outside C major, \ but asks for no resolution", WHITE),
            (r"the minor iv borrows A$\flat$ from C minor: \ a shadow over the major key \ (Part 19's mixture)", TUNE),
            (r"the meanings are learned from films, \ as well as heard in the chords", GREY_A),
        ]
        rows_scene(self, r"why they work", items,
                   "Why do they work? <bookmark mark='b'/> C major to A flat major keeps C, lets E fall to E flat and G rise to A "
                   "flat: a smooth move to a distant key. <bookmark mark='c'/> C to E keeps E, while C falls to B and G rises to "
                   "G sharp: a lift towards brighter keys. <bookmark mark='d'/> In the Lydian sound, the F sharp is outside C "
                   "major but asks for no resolution, so it floats. <bookmark mark='e'/> The minor four borrows A flat from C "
                   "minor, a shadow over the major key: Part 19's mixture. <bookmark mark='f'/> And the meanings are also learned "
                   "from films, as well as heard in the chords.", marks="bcdef")

    # ------------------------------------------------------------------
    def genres(self):
        items = [
            (r"horror: \ clusters, \ extended techniques, \ low drones and silence", WHITE),
            (r"thrillers: \ ostinatos, \ synthesizer pulses, \ the ticking clock", WHITE),
            (r"romance: \ strings, \ suspensions, \ the minor iv", WHITE),
            (r"many films now favour sound design and texture over melody: \ the score as atmosphere \ (Part 30)", TUNE),
            (r"chapter 6: \ the score's hardest partner, \ the human voice", GREY_A),
        ]
        rows_scene(self, r"genre codes", items,
                   "Genres have codes too. <bookmark mark='b'/> Horror: clusters, extended techniques, low drones and silence. "
                   "<bookmark mark='c'/> Thrillers: ostinatos, synthesizer pulses, the ticking clock. <bookmark mark='d'/> "
                   "Romance: strings, suspensions and the minor four. <bookmark mark='e'/> Many recent films favour sound design "
                   "and texture over melody, the score as atmosphere, Part 30's world. <bookmark mark='f'/> Chapter six turns to "
                   "the score's hardest partner, the human voice.", marks="bcdef")
