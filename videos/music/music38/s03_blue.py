from __future__ import annotations

import numpy as np

from videos.music.music38.common import *  # noqa: F403


class Blue(SoundScene):
    def construct(self):
        chapter(self, 2, r"Blue notes", r"Is the blues in major or in minor?")
        self.quiz()
        self.ruler()
        self.which()
        self.scale()
        self.roots()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("blue")
        c = clip("blue.three")
        card = listen_card(r"One sung phrase, \ three times, \ over a C7 chord. \ Its fourth note is a third above C. \ "
                           r"In which version is that third neither minor nor major?", width=10.4)
        with self.voiceover(
            "A question for your ears. One sung phrase of ours, three times, over a C seven chord. Its fourth note is the "
            "third above C. In which version is that third neither minor nor major?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        rolls = VGroup()
        for k in range(3):
            ph = [[m + (0 if m != 75 else 0), a, du] for m, a, du in d["phrase"]]
            r = mroll(ph, width=3.6, height=1.6, lo=64, hi=78, color=GREY_A, total=6.5, bar_h=0.14)
            r.notes[3].set_color(EAR)
            rolls.add(VGroup(label([r"first", r"second", r"third"][k], font_size=20, color=WHITE), r).arrange(DOWN, buff=0.25))
        rolls.arrange(RIGHT, buff=0.7).move_to(UP * 0.3)
        self.play(FadeOut(card), FadeIn(rolls))
        beat = 60.0 / d["bpm"]
        with self.listen(c) as snd:
            window(snd, r"one phrase, \ three times", kind="synthesized", detail=r"a model voice, \ Part 7's piano", corner=DL, tag_corner=DR)
            for k, name in enumerate(("minor", "major", "bent")):
                t0 = d["starts"][name]
                for i, (m, a, du) in enumerate(d["phrase"]):
                    pulse(snd, rolls[k][1].notes[i], t0 + a * beat, t0 + (a + du) * beat - 0.03, buff=0.04)
        ans = VGroup(label(r"first: \ a minor third \ (300 cents); \ second: \ a major third \ (400)", font_size=20, color=WHITE),
                     label(r"third: \ bent upwards from 300 to about 385 cents, \ between the two", font_size=20, color=TUNE)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The third. The first version sings a minor third, three hundred cents; the second a major third, four hundred. "
            "The third version starts at the minor third and bends upwards, stopping short of major. That bent note, "
            "neither one nor the other, is a blue note."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ruler(self):
        x0, W = -5.5, 11.0
        def x(c):
            return x0 + W * c / 1200.0
        axis = Line([x0, 0, 0], [x0 + W, 0, 0], color=GREY_B)
        ticks = VGroup()
        for c, n in ((0, "C"), (300, r"E$\flat$"), (400, "E"), (600, r"F$\sharp$ / G$\flat$"), (700, "G"), (1000, r"B$\flat$"), (1100, "B"), (1200, "C")):
            ticks.add(VGroup(Line([x(c), -0.15, 0], [x(c), 0.15, 0], color=GREY_B), label(n, font_size=18, color=GREY_A).move_to([x(c), -0.45, 0])))
        zones = VGroup(Rectangle(width=x(400) - x(300), height=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.45).move_to([(x(300) + x(400)) / 2, 0.55, 0]),
                       Rectangle(width=x(700) - x(600), height=0.5, stroke_width=0, fill_color=EAR, fill_opacity=0.35).move_to([(x(600) + x(700)) / 2, 0.55, 0]),
                       Rectangle(width=x(1100) - x(1000), height=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.45).move_to([(x(1000) + x(1100)) / 2, 0.55, 0]))
        zl = VGroup(label(r"blue third", font_size=18, color=BLUE).next_to(zones[0], UP, buff=0.1),
                    label(r"flat fifth", font_size=18, color=EAR).next_to(zones[1], UP, buff=0.1),
                    label(r"blue seventh", font_size=18, color=BLUE).next_to(zones[2], UP, buff=0.1))
        bend = Arrow([x(300), 1.5, 0], [x(385), 1.5, 0], color=TUNE, buff=0, stroke_width=4)
        g = VGroup(axis, ticks, zones, zl).shift(DOWN * 0.3)
        head = label(r"where the blue notes live", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Where do blue notes live? <bookmark mark='a'/> In three regions of the scale: the third, between E flat and E; "
            "the fifth, which may be flattened towards F sharp; and the seventh, between B flat and B. "
            "<bookmark mark='b'/> Singers and guitarists bend into these regions, and the notes are often moving, not "
            "fixed. A piano cannot bend, so blues pianists crush the minor and major thirds together, a grace note into the "
            "main note, to suggest the pitch between."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(zones), FadeIn(zl))
            vo.wait_until("b")
            self.play(GrowArrow(bend.shift(DOWN * 0.3)))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def which(self):
        items = [
            (r"recorded blues singers place the third across the whole region, \ not at one pitch", WHITE),
            (r"placement depends on context: \ where the melody comes from and goes, \ and the chord beneath", WHITE),
            (r"so the blues is neither major nor minor: \ the question assumes a grid the music does not use", WHITE),
            (r"Part 35's neutral third \ (about 350 cents) \ sits in the same region", TUNE),
            (r"a pitch region, \ not a pitch", GREY_A),
        ]
        rows_scene(self, r"a region, \ not a note", items,
                   "Measurements of recorded blues singers find the third spread across the whole region, not fixed at one "
                   "pitch. <bookmark mark='b'/> Where it falls depends on context: where the melody comes from and goes, and the "
                   "chord beneath. <bookmark mark='c'/> So is the blues major or minor? The question assumes a grid that the "
                   "music does not use. <bookmark mark='d'/> Part 35's neutral third, about three hundred and fifty cents, sits "
                   "in the same region. <bookmark mark='e'/> A blue note is a pitch region, not a pitch.", marks="bcde")

    # ------------------------------------------------------------------
    def scale(self):
        names = [r"C", r"E$\flat$", r"F", r"F$\sharp$", r"G", r"B$\flat$", r"C"]
        cents = [0, 300, 500, 600, 700, 1000, 1200]
        dots = VGroup()
        for n, c in zip(names, cents):
            dots.add(VGroup(Dot(radius=0.12, color=TUNE), label(n, font_size=22, color=WHITE)).arrange(DOWN, buff=0.15))
        for g_, c in zip(dots, cents):
            g_.move_to([-5.0 + 10.0 * c / 1200, 0.4, 0])
        steps = VGroup(*[label(s, font_size=18, color=GREY_A).move_to([(-5.0 + 10.0 * (a + b) / 2400), 1.05, 0]) for s, a, b in
                         zip(("3", "2", "1", "1", "3", "2"), cents[:-1], cents[1:])])
        cap = VGroup(label(r"the `blues scale' as taught: \ minor pentatonic plus the flat fifth", font_size=20, color=WHITE),
                     label(r"a teaching simplification: \ it fixes on the piano's keys what singers bend between them", font_size=20, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=1.0)
        head = label(r"the blues scale, \ in semitone steps", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Jazz teaching boils this down to the blues scale: C, E flat, F, F sharp, G, B flat, C, the minor pentatonic of "
            "Part 12 with the flat fifth added. <bookmark mark='a'/> It is a useful simplification, and a simplification: it "
            "fixes on the piano's keys what singers bend between them. Played over C seven, its E flat clashes with the "
            "chord's E, and that clash is the point."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(g_) for g_ in dots], lag_ratio=0.15), FadeIn(steps))
            vo.wait_until("a")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def roots(self):
        items = [
            (r"Gerhard Kubik \ (Part 37) \ traced blue notes to West African vocal traditions \ (\textit{Africa and the Blues}, \ 1999)", WHITE),
            (r"in his account, \ a scale built on other principles meets European triads, \ and bends to fit them", WHITE),
            (r"the flat seventh, \ in turn, \ turns every chord into a dominant seventh", WHITE),
            (r"the blues as an encounter of two pitch systems, \ neither giving way", TUNE),
            (r"chapter 3: \ how the blues tells a story", GREY_A),
        ]
        rows_scene(self, r"where blue notes come from", items,
                   "Where do blue notes come from? <bookmark mark='b'/> Gerhard Kubik, whom we met in Part 37, traced them to "
                   "West African vocal traditions in his Africa and the Blues of 1999. <bookmark mark='c'/> In his account a scale "
                   "built on other principles meets European triads and bends to fit them, <bookmark mark='d'/> and the flat "
                   "seventh, in turn, turns every chord into a dominant seventh. <bookmark mark='e'/> The blues, on this view, is "
                   "an encounter of two pitch systems, neither giving way. <bookmark mark='f'/> Chapter three turns to how the "
                   "blues tells a story.", marks="cdef")
