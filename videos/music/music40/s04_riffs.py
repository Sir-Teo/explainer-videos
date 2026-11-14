from __future__ import annotations

import numpy as np

from videos.music.music40.common import *  # noqa: F403

NN = ["C", r"C$\sharp$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]


class Riffs(SoundScene):
    def construct(self):
        chapter(self, 3, r"Riffs", r"Can a whole song stand on one short figure?")
        self.what()
        self.rock()
        self.amp()
        self.power()
        self.funk()
        self.lineage()

    # ------------------------------------------------------------------
    def what(self):
        items = [
            (r"a riff: \ a short figure, \ usually one or two bars, \ repeated as the backbone of a song", WHITE),
            (r"from the swing bands' riffs \ (Part 38) \ to rhythm and blues, \ rock and funk", WHITE),
            (r"often built on the minor pentatonic of the blues scale \ (Part 38)", WHITE),
            (r"a riff is melody, \ rhythm and harmony at once: \ the chord changes can stop", TUNE),
            (r"two of ours: \ a rock riff and a funk riff", GREY_A),
        ]
        rows_scene(self, r"the riff", items,
                   "A riff is a short figure, usually one or two bars, repeated as the backbone of a song. "
                   "<bookmark mark='b'/> It runs from the swing bands' riffs of Part 38 through rhythm and blues to rock and "
                   "funk. <bookmark mark='c'/> It is often built on the minor pentatonic, the blues scale of Part 38. "
                   "<bookmark mark='d'/> A riff is melody, rhythm and harmony at once, and with a strong one the chord changes can "
                   "stop altogether. <bookmark mark='e'/> Here are two of ours, a rock riff and a funk riff.", marks="bcde")

    # ------------------------------------------------------------------
    def rock(self):
        d = load("riffs")
        c = clip("riffs.rock")
        riff = d["rock"]
        notes = [[m + 12, s, 2.0] for m, s in riff]
        r = mroll(notes, width=10.0, height=2.0, lo=48, hi=60, color=EAR, total=16, bar_h=0.18).move_to(UP * 0.3)
        names = VGroup(*[label(NN[(m) % 12], font_size=17, color=WHITE).next_to(b, UP, buff=0.06) for (m, s, du), b in zip(notes, r.notes)])
        cap = label(r"E minor pentatonic, \ sixteenths, \ through a model amplifier", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.1)
        head = label(r"a rock riff of ours", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "First the rock riff, in E minor pentatonic, on the plucked-string guitar through a model amplifier, over a rock "
            "beat. Four times round."
        ):
            self.play(FadeIn(head), FadeIn(r), FadeIn(names), FadeIn(cap))
        step = 60.0 / 110 / 4
        with self.listen(c) as snd:
            window(snd, r"a rock riff", detail=r"plucked string, \ model amplifier, \ drums", corner=DL, tag_corner=DR)
            flash(snd, r.notes * 4, [(b * 16 + s) * step for b in range(4) for m, s in riff], hot=WHITE, base=EAR)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def amp(self):
        x = np.linspace(-3, 3, 200)
        ax = VGroup(Line([-5.5, -0.5, 0], [-1.5, -0.5, 0], color=GREY_B), Line([-3.5, -2.5, 0], [-3.5, 1.5, 0], color=GREY_B))
        lin = VMobject(color=GREY_A, stroke_width=2).set_points_as_corners([[-3.5 + 0.65 * u, -0.5 + 0.65 * u, 0] for u in x if abs(0.65 * u) < 2])
        tanh = VMobject(color=TUNE, stroke_width=4).set_points_as_corners([[-3.5 + 0.65 * u, -0.5 + 1.3 * np.tanh(u), 0] for u in x])
        lab = VGroup(label(r"input", font_size=16, color=GREY_A).move_to([-1.6, -0.8, 0]), label(r"output", font_size=16, color=GREY_A).move_to([-3.5, 1.8, 0]))
        t = np.linspace(0, 2 * np.pi * 2, 200)
        sine = VMobject(color=BLUE, stroke_width=2).set_points_as_corners([[0.5 + 5.0 * k / 199, 1.0 + 0.6 * np.sin(v), 0] for k, v in enumerate(t)])
        clipped = VMobject(color=TUNE, stroke_width=3).set_points_as_corners([[0.5 + 5.0 * k / 199, -1.2 + 0.6 * np.tanh(4 * np.sin(v)) / np.tanh(4), 0] for k, v in enumerate(t)])
        sl = VGroup(label(r"a clean wave", font_size=17, color=BLUE).next_to(sine, UP, buff=0.1), label(r"driven: \ nearly square, \ rich in odd harmonics", font_size=17, color=TUNE).next_to(clipped, DOWN, buff=0.15))
        head = label(r"distortion: \ an amplifier pushed past its limits", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"Part 3's harmonics, \ created by a curve: \ the model uses tanh, \ then a speaker's band limit", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The rock guitar's sound is an amplifier pushed past its limits. <bookmark mark='a'/> A clean amplifier is a "
            "straight line from input to output; driven hard, the line bends over, here modelled by a hyperbolic tangent. "
            "<bookmark mark='b'/> A sine wave through the bend comes out nearly square, and a square wave is rich in odd "
            "harmonics, Part 3's spectrum created by a curve. Chords played this way turn to mud, which is why rock "
            "guitarists play power chords, root and fifth only."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(lab), Create(lin))
            vo.wait_until("a")
            self.play(Create(tanh))
            vo.wait_until("b")
            self.play(Create(sine), Create(clipped), FadeIn(sl), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def power(self):
        d = load("power")
        c = clip("power.two")
        card = listen_card(r"Two chords through the same distorted amplifier: \ one is a full major triad, \ "
                           r"one only root, \ fifth and octave. \ Which is the full triad, \ the first or the second?", width=10.4)
        with self.voiceover(
            "A question for your ears. Two chords strummed through the same model amplifier, turned up. One is a full major "
            "triad; the other has only a root, a fifth and an octave. Which is the full triad, the first or the second?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.2, height=1.4, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(DOWN, buff=-0.9)
                         for t in (r"first", r"second")]).arrange(RIGHT, buff=1.5).move_to(UP * 0.3)
        self.play(FadeOut(card), FadeIn(boxes))
        with self.listen(c) as snd:
            window(snd, r"first, \ then second", detail=r"plucked string, \ model amplifier", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], d["starts"]["triad"], d["starts"]["power"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], d["starts"]["power"], c.duration, buff=0.08)
        cells = VGroup(VGroup(label(r"first: \ C major triad", font_size=22, color=EAR), label(r"C E G C E", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.12),
                       VGroup(label(r"second: \ C power chord \ (C5)", font_size=22, color=TUNE), label(r"C G C", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.12)).arrange(RIGHT, buff=1.6).to_edge(DOWN, buff=1.4)
        cap = label(r"distortion adds sum and difference tones between every pair of notes: \ the third's clash turns the triad to mud", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The first is the full triad, the muddier of the two. The curve does not only add harmonics to each note: it "
            "mixes the notes, adding tones at their sums and differences. For a fifth these line up with the harmonic "
            "series; for a third they do not, and the chord turns to mud. That is why distorted guitars play power chords."
        ):
            self.play(FadeIn(cells), FadeIn(cap), boxes[0][0].animate.set_stroke(EAR, 4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def funk(self):
        d = load("riffs")
        c = clip("riffs.funk")
        riff = d["funk"]
        notes = [[m, s, 1.0] for m, s in riff]
        r = mroll(notes, width=10.0, height=2.0, lo=60, hi=71, color=TUNE, total=16, bar_h=0.18).move_to(UP * 0.4)
        grid = VGroup(*[Line([r.frame.get_left()[0] + 10.0 * k / 16, r.frame.get_bottom()[1] - 0.1, 0], [r.frame.get_left()[0] + 10.0 * k / 16, r.frame.get_top()[1] + 0.1, 0],
                             color=GREY_B if k % 4 == 0 else GREY_D, stroke_width=1.5 if k % 4 == 0 else 0.8) for k in range(17)])
        cap = label(r"a funk riff of ours: \ clean, \ short, \ on the sixteenths; \ the bass and drums lock to beat one", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.1)
        head = label(r"a funk riff of ours", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Now a funk riff: clean, short notes on the sixteenth-note grid, most of them off the beat, with bass and drums "
            "landing together on beat one of every bar. In funk, every instrument is a drum."
        ):
            self.play(FadeIn(head), FadeIn(grid), FadeIn(r), FadeIn(cap))
        step = 60.0 / 100 / 4
        with self.listen(c) as snd:
            window(snd, r"a funk riff", detail=r"plucked string, \ bass, \ drums", corner=DL, tag_corner=DR)
            flash(snd, r.notes * 4, [(b * 16 + s) * step for b in range(4) for m, s in riff], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lineage(self):
        items = [
            (r"blues and rhythm and blues riffs became rock's: \ Chuck Berry, \ then the British bands", WHITE),
            (r"heavy metal built songs from riffs, \ often in power chords", WHITE),
            (r"James Brown's funk \ (from 1965) \ made the whole band a set of interlocking riffs", WHITE),
            (r"Part 37's interlocking parts, \ in a different idiom", TUNE),
            (r"chapter 4: \ the drums under them", GREY_A),
        ]
        rows_scene(self, r"a lineage", items,
                   "The riff has a lineage. <bookmark mark='b'/> Blues and rhythm and blues riffs became rock's, through Chuck "
                   "Berry and then the British bands. <bookmark mark='c'/> Heavy metal built whole songs from riffs, often in "
                   "power chords. <bookmark mark='d'/> And James Brown's funk, from 1965, made the whole band a set of "
                   "interlocking riffs, <bookmark mark='e'/> Part 37's interlocking parts in a different idiom. "
                   "<bookmark mark='f'/> Chapter four turns to the drums under them.", marks="cdef")
