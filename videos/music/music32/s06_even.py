from __future__ import annotations

import numpy as np

from videos.music.music32.common import *  # noqa: F403

TAGS = {(0, 3, 7): r"major, \ minor", (0, 4, 8): r"augmented", (0, 1, 2): r"cluster", (0, 3, 6, 9): r"diminished 7th",
        (0, 2, 5, 8): r"dominant 7th", (0, 3, 5, 8): r"minor 7th", (0, 1, 5, 7): r"(0157)", (0, 1, 2, 3): r"cluster"}


class Even(SoundScene):
    def construct(self):
        chapter(self, 5, r"Nearly even chords", r"Why these chords, \ of all chords?")
        self.scatter()
        self.hear()
        self.meaning()
        self.chopin()

    # ------------------------------------------------------------------
    def scatter(self):
        d = load("even")
        panels = VGroup()
        dots_all = {}
        for size, x0 in ((3, -3.3), (4, 3.3)):
            ax = Axes(x_range=[0, 5, 1], y_range=[0, size + 1, 1], x_length=5.6, y_length=4.0, tips=False,
                      axis_config={"color": GREY_B, "include_numbers": True, "font_size": 16}).move_to(RIGHT * x0 + DOWN * 0.4)
            rows_ = [r for r in d["rows"] if r["size"] == size]
            dots = VGroup()
            tags = VGroup()
            ngood = 0
            for r in rows_:
                good = r["vl"] < size
                dt = Dot(ax.c2p(r["even"], r["vl"]), radius=0.08 if good else 0.06, color=TUNE if good else GREY_B)
                dots.add(dt)
                t = TAGS.get(tuple(r["prime"]))
                if t:
                    if good:
                        ngood += 1
                        tags.add(label(t, font_size=15, color=TUNE).next_to(dt, DOWN if ngood % 2 == 0 else UP, buff=0.14))
                    else:
                        tags.add(label(t, font_size=15, color=GREY_A).next_to(dt, UP, buff=0.12))
            line = DashedLine(ax.c2p(0, size), ax.c2p(5, size), color=EAR, stroke_width=1.5)
            ttl = label(rf"{size}-note chord types \ ({len(rows_)})", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.25)
            xl = label(r"distance from even", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.3)
            panels.add(VGroup(ax, line, dots, ttl, xl))
            dots_all[size] = (dots, tags)
        yl = label(r"smallest voice leading to a different transposition of itself \ (semitones)", font_size=19, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"the dashed line: \ every voice up a semitone \ (n semitones); \ only the gold chords do better", font_size=20, color=EAR).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Here is the test of Tymoczko's claim. For every type of three-note and four-note chord, two numbers: across, "
            "how far it is from a perfectly even chord; up, the smallest voice leading that takes it to a different "
            "transposition of itself. <bookmark mark='a'/> Any chord can move every voice up a semitone, n semitones in all: "
            "the dashed line. Almost every chord does no better. <bookmark mark='b'/> A handful do: the major and minor triad, "
            "which reaches a transposition with just two semitones, and among four-note chords the dominant seventh, the "
            "minor seventh and one more. <bookmark mark='c'/> Look where they sit: close to even, but not at it. The "
            "perfectly even chords, the augmented triad and the diminished seventh, do no better than a cluster."
        ) as vo:
            self.play(FadeIn(yl), FadeIn(panels))
            vo.wait_until("a")
            self.play(FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(dots_all[3][1]), FadeIn(dots_all[4][1]))
            vo.wait_until("c")
            self.play(Indicate(dots_all[3][0], color=WHITE, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("even")
        c = clip("even.three")
        names = {"major": (r"C major to E major", r"C down to B, \ G up to G$\sharp$"),
                 "dominant seventh": (r"C$^7$ to E$\flat^7$", r"C up to D$\flat$, \ E down to E$\flat$"),
                 "diatonic scale": (r"C major scale to G major scale", r"F up to F$\sharp$")}
        cells = VGroup()
        for demo in d["demos"]:
            t, how = names[demo["name"]]
            cells.add(VGroup(label(t, font_size=24, color=TUNE), label(how, font_size=19, color=GREY_A),
                             label(rf"{demo['size']:.0f} semitone{'s' if demo['size'] != 1 else ''}", font_size=22, color=WHITE)).arrange(DOWN, buff=0.25))
        cells.arrange(DOWN, buff=0.55).move_to(UP * 0.2)
        head = label(r"nearly even chords reach their transpositions in one or two semitones", font_size=25, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear what that buys. C major to E major, a whole key a major third away: C falls to B, G rises to G sharp, two "
            "semitones. C seven to E flat seven: two semitones. And the C major scale to the G major scale: one semitone, F "
            "to F sharp, the smallest move there is. A composer with nearly even chords can change key while barely moving."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"three small moves", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            ks = [x["name"] for x in d["demos"]]
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.5 if i < 2 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self):
        items = [
            (r"harmony wants chords that sound alike in many keys: \ consonant, \ nearly even", WHITE),
            (r"counterpoint wants voices that move little: \ efficient voice leading", WHITE),
            (r"nearly even chords satisfy both at once: \ the two demands are compatible", TUNE),
            (r"perfectly even chords are too symmetric: \ their nearest transpositions are themselves", WHITE),
            (r"Tymoczko's thesis: \ this is why Western music could have both harmony and counterpoint", GREY_A),
        ]
        rows_scene(self, r"why it matters", items,
                   "Why does it matter? <bookmark mark='b'/> Harmony wants chords that sound good and can be heard as the same "
                   "chord in many keys. <bookmark mark='c'/> Counterpoint wants independent voices that move by small steps. "
                   "<bookmark mark='d'/> Nearly even chords satisfy both at once: a progression of such chords can change key "
                   "while every voice moves by a step. <bookmark mark='e'/> Perfectly even chords are too symmetric: their "
                   "nearest transpositions are just themselves, so to go anywhere new every voice must move. "
                   "<bookmark mark='f'/> Tymoczko's thesis is that this geometric fact is why Western music could combine "
                   "harmony and counterpoint for so long.", marks="cdef")

    # ------------------------------------------------------------------
    def chopin(self):
        items = [
            (r"Chopin, \ Prelude in E minor, \ Op. 28 No. 4 \ (1839): \ a left hand of slowly sliding chords", WHITE),
            (r"Tymoczko's reading: \ seventh chords moving mostly one voice, \ one semitone, \ at a time", WHITE),
            (r"many of the chords have no function in a key; \ the voice leading carries the music", WHITE),
            (r"in the space: \ a slow walk near the centre, \ among the nearly even four-note chords", TUNE),
            (r"the same technique runs through Wagner, \ Debussy and jazz piano", GREY_A),
        ]
        rows_scene(self, r"sliding through four-note space", items,
                   "Composers used this long before the geometry. <bookmark mark='b'/> Chopin's Prelude in E minor, of 1839, has a left hand of slowly sliding chords. <bookmark mark='c'/> Tymoczko reads it as four-note chords moving mostly one voice, by one semitone, at a time. <bookmark mark='d'/> Many of the chords have no function in any key; the voice leading carries the music. <bookmark mark='e'/> In the space, it is a slow walk near the centre, among the nearly even four-note chords. <bookmark mark='f'/> The same technique runs through Wagner, Debussy and jazz piano.", marks="cdef")
