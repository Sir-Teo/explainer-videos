from __future__ import annotations

import numpy as np

from videos.music.music32.common import *  # noqa: F403


class Scales(SoundScene):
    def construct(self):
        chapter(self, 6, r"Scales are chords too", r"What is a key change, \ geometrically?")
        self.ranking()
        self.keys()
        self.circle()
        self.levels()
        self.jazz()

    # ------------------------------------------------------------------
    def ranking(self):
        d = load("scales")
        top = d["top"]
        nm = [t["name"] or ("(" + "".join("T" if x == 10 else "E" if x == 11 else str(x) for x in t["prime"]) + ")") for t in top]
        bars = columns([t["even"] for t in top], None, width=6.4, height=3.0, color=GREY_B, hot=(0,), hot_color=TUNE, fmt="{:.2f}", font_size=18).move_to(LEFT * 2.6 + DOWN * 0.3)
        names = VGroup(*[label(n, font_size=16, color=TUNE if i == 0 else GREY_A).rotate(PI / 5).next_to(bars.bars[i], DOWN, buff=0.2).shift(LEFT * 0.35)
                         for i, n in enumerate(nm)])
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (rf"all {d['count']} types of seven-note scale, \ ranked by distance from even", WHITE),
            (r"first: \ the diatonic scale, \ Part 12's maximally even scale", TUNE),
            (r"second and third: \ melodic minor, \ then harmonic minor and major", WHITE),
            (r"the scales of tonal music are the most even seven-note chords", GREY_A))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.6)).move_to(RIGHT * 3.6)
        head = label(r"the six most even seven-note scales", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A scale is a set of notes, so it is a chord too, a point in seven-note chord space. <bookmark mark='a'/> Rank "
            f"all {say(d['count'])} types of seven-note scale by their distance from perfectly even. <bookmark mark='b'/> "
            "First comes the diatonic scale, the maximally even scale of Part 12. <bookmark mark='c'/> Second, the melodic "
            "minor, which jazz calls the acoustic scale; third, harmonic minor, with its mirror image harmonic major. "
            "<bookmark mark='d'/> The scales of tonal music are exactly the most even seven-note chords."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), FadeIn(names), FadeIn(side[0]))
            for mark, r in zip("bcd", side[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def keys(self):
        d = load("scales")
        c = clip("scales.keys")
        g = mroll(d["notes"], width=11.0, height=2.0, lo=58, hi=75, color=GREY_A, bar_h=0.13).move_to(DOWN * 0.6)
        tags = VGroup(label(r"C major", font_size=24, color=TUNE), label(r"G major: \ F to F$\sharp$", font_size=24, color=BLUE),
                      label(r"D major: \ C to C$\sharp$", font_size=24, color=EAR)).arrange(RIGHT, buff=1.6).move_to(UP * 1.2)
        head = label(r"a key change is a voice leading between scales", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(rf"each step: \ {d['steps'][0]:.0f} semitone; \ one note of seven moves", font_size=22, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "So a change of key is a voice leading between scales. From C major to G major one note moves, F up to F sharp; "
            "from G to D, again one, C up to C sharp. Each step round the circle of fifths is the smallest voice leading "
            "there is, a single semitone in a single voice. Listen to three scales in a row, and hear the one note that "
            "changes each time."
        ):
            self.play(FadeIn(head), FadeIn(tags), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"C, \ G, \ D major", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            u = d["unit"]
            for i in range(3):
                pulse(snd, tags[i], 8 * i * u, 8 * (i + 1) * u - 0.05, buff=0.1)
            flash(snd, g.notes, [n[1] * u for n in d["notes"]], hot=WHITE, base=GREY_A)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def levels(self):
        items = [
            (r"tonal music moves on two levels at once: \ chords inside a scale, \ and scales against each other", WHITE),
            (r"both levels use nearly even collections: \ triads in diatonic scales", WHITE),
            (r"and both move by small voice leadings: \ a step in a voice, \ a semitone in a scale", WHITE),
            (r"Tymoczko calls this the `extended common practice', \ from Bach through jazz to film", TUNE),
            (r"Part 33 builds the mathematics of scales and rhythms that sits underneath", GREY_A),
        ]
        rows_scene(self, r"two levels at once", items,
                   "This gives tonal music a structure on two levels. <bookmark mark='b'/> Chords move inside a scale, and the "
                   "scale itself moves against other scales. <bookmark mark='c'/> Both levels use nearly even collections: "
                   "triads, inside diatonic scales. <bookmark mark='d'/> And both move by small voice leadings: a step in a "
                   "voice, a semitone in a scale. <bookmark mark='e'/> Tymoczko calls the music built this way the extended "
                   "common practice, running from Bach through jazz to film. <bookmark mark='f'/> Part 33 builds the "
                   "mathematics of scales and rhythms underneath.", marks="cdef")

    # ------------------------------------------------------------------
    def jazz(self):
        items = [
            (r"jazz improvisers think in chord-scales: \ a seven-note scale for every chord", WHITE),
            (r"the acoustic scale \ (melodic minor) \ and its modes: \ altered, \ Lydian dominant", WHITE),
            (r"moving between chord-scales: \ one or two notes change, \ the rest hold", TUNE),
            (r"so jazz harmony is voice leading at the level of scales, \ like modulation", WHITE),
            (r"Part 39 hears the changes; \ this chapter's geometry is underneath them", GREY_A),
        ]
        rows_scene(self, r"scales in jazz", items,
                   "Jazz uses the second scale on the list as much as the first. <bookmark mark='b'/> Improvisers think in chord-scales, a seven-note scale for each chord. <bookmark mark='c'/> The acoustic scale, melodic minor, and its modes, the altered scale and the Lydian dominant, are everyday sounds. <bookmark mark='d'/> Moving from one chord-scale to the next usually changes one or two notes and holds the rest. <bookmark mark='e'/> So jazz harmony is voice leading at the level of scales, like modulation in Bach, only faster. <bookmark mark='f'/> Part 39 hears the changes; this geometry lies underneath them.", marks="cdef")

    # ------------------------------------------------------------------
    def circle(self):
        d = load("scales")
        names = ["C", "G", "D", "A", "E", "B", r"F$\sharp$", r"D$\flat$", r"A$\flat$", r"E$\flat$", r"B$\flat$", "F"]
        ks = [(7 * i) % 12 for i in range(12)]
        g = VGroup()
        cen = LEFT * 2.8 + DOWN * 0.3
        for i, (n, k) in enumerate(zip(names, ks)):
            ang = PI / 2 - i * TAU / 12
            pos = cen + 2.4 * np.array([np.cos(ang), np.sin(ang), 0])
            v = d["circle"][str(k)]
            col = interpolate_color(ManimColor(TUNE), ManimColor(GREY_B), v / 6.0)
            g.add(VGroup(label(n, font_size=26, color=col).move_to(pos), label(f"{v:.0f}", font_size=18, color=GREY_A).move_to(cen + 1.75 * np.array([np.cos(ang), np.sin(ang), 0]))))
        ring_ = Circle(radius=2.4, color=DIM, stroke_width=1.5).move_to(cen)
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"from the C major scale to every other major scale: \ the smallest voice leading", WHITE),
            (r"G and F: \ 1 semitone; \ D and B$\flat$: \ 2; \ ... \ F$\sharp$: \ 6", TUNE),
            (r"the numbers are exactly the steps round the circle of fifths", WHITE),
            (r"the circle of fifths is the map of shortest paths between scales", GREY_A))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.6)).move_to(RIGHT * 3.6)
        head = label(r"the circle of fifths, \ measured", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Do it for every key. From the C major scale to each of the other eleven major scales, find the smallest voice "
            "leading. <bookmark mark='a'/> G major and F major: one semitone. D and B flat: two. And so on, up to F sharp "
            "major: six. <bookmark mark='b'/> The numbers are exactly the number of steps round the circle of fifths. "
            "<bookmark mark='c'/> The circle that Part 15 drew from listeners' judgements, and that theory books draw from "
            "key signatures, is also the map of shortest paths between scales."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ring_), FadeIn(g), FadeIn(side[0]))
            for mark, r in zip("abc", side[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
