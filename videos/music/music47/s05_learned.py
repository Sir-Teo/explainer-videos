from __future__ import annotations

import numpy as np

from videos.music.music47.common import *  # noqa: F403


class Learned(SoundScene):
    def construct(self):
        chapter(self, 4, r"What is learned", r"Is the liking for consonance in our nature?")
        self.tsimane()
        self.chords()
        self.gradient()
        self.octave()
        self.infants()

    # ------------------------------------------------------------------
    def tsimane(self):
        items = [
            (r"the Tsimane' live in the Bolivian Amazon; \ in 2016 many had heard little Western music", WHITE),
            (r"Josh McDermott and colleagues played them chords and sung harmonies, \ consonant and dissonant", WHITE),
            (r"they rated consonant and dissonant as equally pleasant", WHITE),
            (r"yet they heard the difference, \ disliked rough sounds, \ and liked laughter more than gasps, \ as Americans did", TUNE),
            (r"roughness is physics \ (Part 5); \ preferring smoothness in chords seems to be learned", GREY_A),
        ]
        rows_scene(self, r"indifference to dissonance", items,
                   "Take the most famous candidate for a universal of taste: that consonance pleases and dissonance does not. <bookmark mark='b'/> The Tsimane' live in the Bolivian Amazon, and in 2016 many had heard little Western music. Josh McDermott and colleagues played them chords and sung harmonies, consonant and dissonant. <bookmark mark='c'/> They rated the two as equally pleasant. <bookmark mark='d'/> Yet they could hear the difference, they disliked rough sounds, and they preferred laughter to gasps, just as Americans did. <bookmark mark='e'/> Acoustic beating and auditory filtering contribute to roughness, while pleasantness and harmonic consonance depend on exposure, task and musical context.", marks="bcde")

    # ------------------------------------------------------------------
    def chords(self):
        d = load("chords")
        c = clip("chords.four")
        cells = VGroup()
        for k in d["order"]:
            keys = d["keys"][k]
            stack = VGroup(*[Rectangle(width=1.4, height=0.14, stroke_width=0, fill_color=TUNE if k in d["consonant"] else EAR, fill_opacity=0.9)
                             .move_to([0, 0.13 * (m - 60), 0]) for m in keys])
            box = RoundedRectangle(width=2.6, height=2.6, corner_radius=0.15, stroke_color=GREY_B, stroke_width=1.5)
            stack.move_to(box.get_center())
            cells.add(VGroup(box, stack, label(k, font_size=17, color=WHITE).next_to(box, DOWN, buff=0.2)))
        cells.arrange(RIGHT, buff=0.45).move_to(UP * 0.2)
        cap = label(r"bars: \ the notes of each chord, \ a semitone per step up; \ gold consonant, \ pink dissonant", font_size=16, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"chords of the kind they rated", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            'Hear chords of the kind they rated: a major triad, a cluster of three neighbouring semitones, an open fifth with its octave, and a tritone stacked with a minor ninth. To most of us the second and fourth sound harsh. The study found no group preference for its consonant over dissonant examples; that does not imply these exact sketches sound equally harsh or that roughness is irrelevant.'
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"consonant, \ dissonant", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, t in enumerate(d["starts"]):
                end = d["starts"][i + 1] - 0.2 if i < 3 else c.duration
                pulse(snd, cells[i], t, end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gradient(self):
        groups = [(r"Tsimane'", 0.0, r"none detectable"), (r"Bolivian town", 0.25, r"small"), (r"Bolivian city", 0.35, r"small"),
                  (r"American non-musicians", 0.7, r"larger"), (r"American musicians", 1.0, r"largest")]
        bars = VGroup()
        for i, (n, v, t) in enumerate(groups):
            y = 1.7 - 0.85 * i
            bars.add(VGroup(label(n, font_size=20, color=WHITE).move_to([-1.6, y, 0], aligned_edge=RIGHT),
                            Rectangle(width=max(6.0 * v, 0.04), height=0.45, stroke_width=0, fill_color=TUNE, fill_opacity=0.85).move_to([-1.3 + 3.0 * v, y, 0]),
                            label(t, font_size=18, color=GREY_A).move_to([-1.3 + 6.0 * v + 0.3, y, 0], aligned_edge=LEFT)))
        head = label(r"preference for consonance, \ by exposure to Western music", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"the order is the study's; \ bar lengths are only a sketch of it, \ not its measured sizes", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "The study's most telling result is a gradient. <bookmark mark='a'/> No preference among the Tsimane'. "
            "<bookmark mark='b'/> A small but real one among Bolivians in a nearby town, <bookmark mark='c'/> and in the "
            "capital. <bookmark mark='d'/> A larger one among Americans, <bookmark mark='e'/> and the largest among American "
            "musicians. The more Western music a group had heard, the more it preferred consonance. The bars here sketch "
            "that order; they are not the study's measured sizes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ghost(VGroup(*[b[0] for b in bars]), 0.3)))
            for mark, b in zip("abcde", bars):
                vo.wait_until(mark)
                self.play(FadeIn(b))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def octave(self):
        items = [
            (r"Nori Jacoby and colleagues \ (2019) \ asked people to sing back tones, \ some outside their vocal range", WHITE),
            (r"Americans moved out-of-range tones by an octave; \ the Tsimane' moved them too, \ but not by an octave", WHITE),
            (r"both kept the intervals of a short melody: \ relative pitch looked shared, \ octave equivalence less so", WHITE),
            (r"scales differ too: \ the maqam's neutral seconds \ (Part 35), \ gamelan's tunings \ (Part 36)", TUNE),
            (r"what may be shared: \ a few discrete steps within a range; \ what they are, \ a culture decides", GREY_A),
        ]
        rows_scene(self, r"is the octave universal?", items,
                   "Even the octave has been questioned. <bookmark mark='b'/> In 2019 Nori Jacoby and colleagues asked people to "
                   "sing back tones, some of them outside their vocal range. <bookmark mark='c'/> Americans moved the "
                   "out-of-range tones by an octave; the Tsimane' moved them too, but not by an octave. "
                   "<bookmark mark='d'/> Both kept the intervals of a short melody, so relative pitch looked shared and octave "
                   "equivalence less so. <bookmark mark='e'/> Scales differ as well: the maqam's neutral seconds in Part 35, "
                   "gamelan tunings in Part 36. <bookmark mark='f'/> What may be shared is a few discrete steps within a range; "
                   "which steps, a culture decides.", marks="bcdef")

    # ------------------------------------------------------------------
    def infants(self):
        items = [
            (r"Michael Lynch and colleagues \ (1990): \ six-month-olds noticed mistuned notes in Western and Javanese scales alike", WHITE),
            (r"American adults noticed them mainly in the Western scale", WHITE),
            (r"Erin Hannon and Sandra Trehub \ (2005): \ six-month-olds noticed broken Balkan meters as well as Western ones", WHITE),
            (r"by twelve months they responded like their parents; \ a week or two of Balkan music at home restored the infants' ear, \ not adults'", TUNE),
            (r"we start open and narrow to the music around us, \ as we do for the sounds of speech", GREY_A),
        ]
        rows_scene(self, r"born open, \ tuned by exposure", items,
                   "Infants show how the learning happens. <bookmark mark='b'/> In 1990 Michael Lynch and colleagues found that "
                   "six-month-olds noticed mistuned notes in Western and Javanese scales alike, <bookmark mark='c'/> while "
                   "American adults noticed them mainly in the Western scale. <bookmark mark='d'/> In 2005 Erin Hannon and "
                   "Sandra Trehub found that six-month-olds noticed broken Balkan meters as well as Western ones. "
                   "<bookmark mark='e'/> By twelve months they responded like their parents; and a week or two of Balkan music "
                   "at home restored the infants' ear, but not the adults'. <bookmark mark='f'/> We start open and narrow to the "
                   "music around us, much as we do for the sounds of speech.", marks="bcdef")
