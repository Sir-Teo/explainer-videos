from __future__ import annotations

import numpy as np

from videos.music.music31.common import *  # noqa: F403


class Jazz(SoundScene):
    def construct(self):
        chapter(self, 7, r"Thirds in jazz", r"What did Coltrane do with a major third?", extra=((1959, r"\textit{Giant Steps}"),))
        self.coltrane()
        self.three_keys()
        self.changes()
        self.sevenths()
        self.beyond()

    # ------------------------------------------------------------------
    def coltrane(self):
        items = [
            (r"John Coltrane, \ \textit{Giant Steps} \ (1959): \ three tonal centres a major third apart", WHITE),
            (r"B, \ G, \ E$\flat$: \ an augmented triad of keys, \ dividing the octave equally", WHITE),
            (r"each reached through its own dominant, \ at a very fast tempo", WHITE),
            (r"`Coltrane changes': \ a vocabulary that jazz players still practise", TUNE),
            (r"the tune is in copyright: \ the film names the moves, \ Part 39 plays its own changes", GREY_A),
        ]
        rows_scene(self, r"Coltrane changes", items,
                   "Jazz found the same symmetry. <bookmark mark='b'/> John Coltrane's Giant Steps, recorded in 1959, moves "
                   "between three tonal centres a major third apart: <bookmark mark='c'/> B, G and E flat, which divide the "
                   "octave into three equal parts, <bookmark mark='d'/> each approached through its own dominant chord, at a "
                   "very fast tempo. <bookmark mark='e'/> Jazz players call these Coltrane changes and still practise them. "
                   "<bookmark mark='f'/> The tune is in copyright, so the film names the moves; Part 39 plays changes of its "
                   "own.", marks="cdef")

    # ------------------------------------------------------------------
    def three_keys(self):
        g = tonnetz()
        head = label(r"three keys a major third apart: \ a vertical line on the Tonnetz", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        # B, G and E flat lie a major third apart: up the major-third axis of the lattice
        marks = VGroup()
        for (i, j), pc in g.pc.items():
            if pc in (11, 7, 3):
                marks.add(Circle(radius=0.3, color=EAR, stroke_width=4).move_to(g.pos[(i, j)]))
        rows_ = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"B, \ G, \ E$\flat$: \ each a major third from the next", EAR),
            (r"in PLR terms, \ B major to G major is P then L: \ the hexatonic pair", WHITE))]).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "On the Tonnetz the three keys lie along one line, each a major third above the last, and three steps bring you "
            "back to the start: the map's wrap-around. <bookmark mark='a'/> Between major chords a major third apart, the "
            "PLR group needs just two moves, the same pair that drives the hexatonic cycle. Coltrane's harmony walks the "
            "torus in the direction Part 28's augmented triad points."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(marks), FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows_[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beyond(self):
        items = [
            (r"seventh chords: \ Childs, \ Gollin and others built Tonnetze for four-note chords", WHITE),
            (r"Dmitri Tymoczko: \ voice leading as motion in a space of chords \ (Part 32)", WHITE),
            (r"popular music: \ the `chromatic mediant' in rock and film-inspired pop", WHITE),
            (r"the transformational view travels: \ rhythms, \ timbres, \ even form", TUNE),
            (r"Part 39 hears jazz harmony; \ Part 32, \ the geometry under all of it", GREY_A),
        ]
        rows_scene(self, r"beyond triads", items,
                   "The idea extends beyond triads. <bookmark mark='b'/> Adrian Childs, Edward Gollin and others built Tonnetze "
                   "for four-note seventh chords. <bookmark mark='c'/> Dmitri Tymoczko treats voice leading as motion in a "
                   "geometric space of chords, which Part 32 builds. <bookmark mark='d'/> Chromatic mediants are common in rock "
                   "and in film-inspired pop. <bookmark mark='e'/> And the transformational view has been applied to rhythms, "
                   "timbres and even form. <bookmark mark='f'/> Part 39 hears jazz harmony, and Part 32 the geometry under all "
                   "of it.", marks="cdef")

    # ------------------------------------------------------------------
    def changes(self):
        d = load("thirds")
        c = clip("thirds.cycle")
        names = {"B": "B", "D7": r"D$^7$", "G": "G", "Bb7": r"B$\flat^7$", "Eb": r"E$\flat$", "F#7": r"F$\sharp^7$"}
        cells = VGroup(*[label(names[n], font_size=34, color=TUNE if "7" not in n else GREY_A) for n in d["seq"]]).arrange(RIGHT, buff=0.7).move_to(UP * 0.5)
        g = mroll(d["notes"], width=10.0, height=1.8, lo=34, hi=70, color=GREY_A, bar_h=0.1).move_to(DOWN * 1.6)
        head = label(r"three keys a major third apart, \ each through its dominant \ (our voicing)", font_size=25, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is the skeleton of the idea, in our own voicing and at a slow tempo: B major, then D seven leading to G "
            "major, then B flat seven leading to E flat major, then F sharp seven leading back to B. Three keys, each a major "
            "third below the last, each prepared by its own dominant. A chord progression like this is common property; the "
            "melodies written over it are not."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"B, \ G, \ E$\flat$, \ B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i in range(len(cells)):
                pulse(snd, cells[i], i * d["unit"], (i + 1) * d["unit"] - 0.05, buff=0.08)
            flash(snd, g.notes, [n[1] * d["unit"] for n in d["notes"]], hot=WHITE, base=GREY_A)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sevenths(self):
        d = load("sevenths")
        c = clip("sevenths.four")

        def nm(s):
            s = s.replace("o7", r"$^{\emptyset 7}$").replace("7", r"$^7$")
            return s.replace("Eb", r"E$\flat$").replace("Db", r"D$\flat$").replace("Bb", r"B$\flat$").replace("F#", r"F$\sharp$")
        nb = VGroup(*[label(nm(r["chord"]), font_size=24, color=TUNE if r["chord"].endswith("7") and not r["chord"].endswith("o7") else BLUE) for r in d["rows"]])
        nb.arrange_in_grid(rows=2, buff=(0.6, 0.35))
        src = label(r"C$^7$", font_size=40, color=EAR)
        left = VGroup(src, label(rf"{d['n']} seventh chords within two semitones:", font_size=20, color=GREY_A), nb).arrange(DOWN, buff=0.35)
        left.move_to(UP * 0.9)
        cells = VGroup()
        tags = [r"tritone away: \ the jazz `tritone substitution'", r"a minor third down", r"a minor third up", r"F$^{\emptyset 7}$ to E$^7$: \ the move inside \textit{Tristan}'s first chords"]
        for p_, t in zip(d["pairs"], tags):
            cells.add(VGroup(label(rf"{nm(p_['a'])} to {nm(p_['b'])}", font_size=24, color=WHITE), label(t, font_size=17, color=GREY_A)).arrange(DOWN, buff=0.15))
        cells.arrange(RIGHT, buff=0.55).to_edge(DOWN, buff=1.4)
        cells.scale_to_fit_width(min(cells.width, 12.6))
        head = label(r"the same idea for four-note chords", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The parsimony idea carries over to four-note chords. Take the dominant seventh, C, E, G, B flat, and the "
            "half-diminished seventh, its upside-down twin. Search all twenty-four for chords the four voices can reach in "
            f"two semitones of motion: there are {say(d['n'])}. {say(d['two_semitone']).capitalize()} of them move two "
            "voices by a semitone each and keep the other two; one, E half-diminished, moves a single voice by a whole tone. "
            "<bookmark mark='a'/> Among them is C seven to F sharp seven, two chords a tritone apart that share E and B flat: "
            "jazz calls it the tritone substitution. And F half-diminished to E seven is the very move inside the first "
            "chords of Wagner's Tristan, from Part 27."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left))
            vo.wait_until("a")
            self.play(FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"four seventh-chord moves", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            ks = ["F#7", "A7", "Eb7", "tristan"]
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.4 if i < 3 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()
