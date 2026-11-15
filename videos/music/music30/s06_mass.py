from __future__ import annotations

import numpy as np

from videos.music.music30.common import *  # noqa: F403


class Mass(SoundScene):
    def construct(self):
        chapter(self, 5, r"Sound masses", r"What happens when notes are too close to be notes?", extra=((1961, r"Ligeti's \textit{Atmosphères}"),))
        self.history()
        self.cluster()
        self.beats()
        self.spread()
        self.micro()
        self.notation()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"Krzysztof Penderecki, \ \textit{Threnody for the Victims of Hiroshima} \ (1960): \ 52 strings in quarter-tone clusters", WHITE),
            (r"György Ligeti, \ \textit{Atmosphères} \ (1961): \ no melody, \ no rhythm, \ only slowly changing texture", WHITE),
            (r"`micropolyphony': \ dozens of lines too close and too many to hear one by one", WHITE),
            (r"the cluster as a sound in itself: \ a band of pitches, \ a colour, \ a mass", TUNE),
            (r"heard by millions in Kubrick's \textit{2001} \ (1968), \ used without Ligeti's permission", GREY_A),
        ]
        rows_scene(self, r"masses of sound", items,
                   "In Poland and Hungary composers wrote masses of sound. <bookmark mark='b'/> Krzysztof Penderecki's Threnody "
                   "for the Victims of Hiroshima, of 1960, sets fifty-two strings in clusters of quarter tones. "
                   "<bookmark mark='c'/> György Ligeti's Atmosphères, of 1961, has no melody and no rhythm, only a slowly "
                   "changing texture. <bookmark mark='d'/> Ligeti called it micropolyphony: dozens of lines, too close together "
                   "and too many to be heard one by one. <bookmark mark='e'/> The cluster becomes a sound in itself, a band of "
                   "pitches heard as a colour. <bookmark mark='f'/> Millions heard Atmosphères in Stanley Kubrick's film 2001, in "
                   "1968, where it was used without Ligeti's permission.", marks="cdef")

    # ------------------------------------------------------------------
    def cluster(self):
        d = load("mass")
        c = clip("mass.cluster")
        ps = d["pitches"]
        W = 9.0
        bars = VGroup(*[Rectangle(width=W * (6.0 - 0.5 * i) / 7.5, height=0.16, stroke_width=0, fill_color=TUNE, fill_opacity=0.85)
                        .move_to([-W / 2 + W * (d["entry"] * i + (6.0 - 0.5 * i) / 2) / 7.5, -1.6 + 0.42 * i, 0]) for i, p in enumerate(ps)])
        names = VGroup(*[label(rf"{p:.1f}", font_size=15, color=GREY_B).next_to(bars[i], LEFT, buff=0.15) for i, p in enumerate(ps)])
        head = label(r"eight bowed strings, \ half a semitone apart, \ entering one by one \ (ours)", font_size=25, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"key numbers 60.3 to 63.8: \ a band three and a half semitones wide", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is a cluster of our own. Eight of Part 7's bowed strings, each half a semitone above the last, entering one "
            "by one until the band is three and a half semitones wide. Listen to what happens as it thickens: the separate "
            "notes disappear, and a single rough, shimmering band takes their place."
        ):
            self.play(FadeIn(head), FadeIn(bars), FadeIn(names), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a cluster, \ growing", detail=r"Part 7's bowed string", corner=DL, tag_corner=DR)
            for i in range(len(ps)):
                pulse(snd, bars[i], d["entry"] * i, d["entry"] * i + 0.8, buff=0.04)
            pulse(snd, bars, d["entry"] * (len(ps) - 1) + 0.8, c.duration, buff=0.15, color=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beats(self):
        d = load("mass")
        bars = columns(d["beats"], [str(i + 1) for i in range(len(d["beats"]))], width=6.4, height=2.6, color=EAR, fmt="{:.1f}", font_size=17)
        bars.move_to(LEFT * 2.8 + DOWN * 0.4)
        t = label(r"beats per second between neighbouring strings", font_size=21, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (r"half a semitone apart near middle C: \ about 8 beats a second", WHITE),
            (r"Part 5: \ beats this fast are heard as roughness", TUNE),
            (r"eight strings: \ seven neighbouring pairs, \ and many more distant ones, \ all beating at once", WHITE),
            (r"the mass is rough because of physics, \ not notation", EAR))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.4))
        side.move_to(RIGHT * 3.6 + DOWN * 0.2)
        with self.voiceover(
            "Why does a cluster sound rough? <bookmark mark='a'/> Neighbouring strings half a semitone apart near middle C "
            "differ by about eight hertz, so they beat about eight times a second. <bookmark mark='b'/> Part 5 showed that "
            "beats this fast are no longer heard as a pulse but as roughness. <bookmark mark='c'/> With eight strings, seven "
            "neighbouring pairs beat at once, and every more distant pair adds its own faster beating. "
            "<bookmark mark='d'/> The mass is rough because of physics, whatever the score calls it."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def micro(self):
        items = [
            (r"Giacinto Scelsi: \ whole pieces on a single note, \ explored from inside \ (\textit{Quattro pezzi}, \ 1959)", WHITE),
            (r"Morton Feldman: \ very quiet, \ very long: \ the String Quartet II \ (1983) \ lasts some six hours", WHITE),
            (r"La Monte Young and drone music: \ just intervals sustained for hours", WHITE),
            (r"Pauline Oliveros's `deep listening' \ (1989): \ attention as the material", TUNE),
            (r"from the note to the sound, \ and from the sound to listening itself", GREY_A),
        ]
        rows_scene(self, r"inside the sound", items,
                   "Others went inside a single sound. <bookmark mark='b'/> Giacinto Scelsi wrote whole pieces on a single "
                   "note, explored through its tuning, timbre and dynamics; his Four Pieces, each on one note, date from 1959. "
                   "<bookmark mark='c'/> Morton Feldman's late music is very quiet and very long; his Second String Quartet, "
                   "of 1983, lasts some six hours. <bookmark mark='d'/> La Monte Young sustained just intervals for hours, in "
                   "drone music. <bookmark mark='e'/> Pauline Oliveros made attention itself the material, in what she called "
                   "deep listening. <bookmark mark='f'/> From the note to the sound, and from the sound to listening itself.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def spread(self):
        d = load("spread")
        c = clip("spread.two")
        def col(ps, color):
            return VGroup(*[Line([-0.8, -2.0 + 4.0 * (p - 36) / 46, 0], [0.8, -2.0 + 4.0 * (p - 36) / 46, 0], color=color, stroke_width=4) for p in ps])
        a = col(d["cluster"], EAR).move_to(LEFT * 3.0 + DOWN * 0.2)
        b = col(d["open"], TUNE).move_to(RIGHT * 3.0 + DOWN * 0.2)
        la = label(r"a cluster: \ half a semitone apart", font_size=22, color=EAR).next_to(a, UP, buff=0.4)
        lb = label(r"the same eight strings, \ in fifths and fourths", font_size=22, color=TUNE).next_to(b, UP, buff=0.4)
        cap = label(r"neighbours a fifth or a fourth apart beat far too fast to hear as roughness", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The roughness comes from closeness, not from the number of strings. The same eight bowed strings, first as the "
            "cluster, half a semitone apart, then spread out in fifths and fourths across four octaves. The second is "
            "smooth and open: neighbours so far apart no longer beat at a rate the ear hears as roughness."
        ):
            self.play(FadeIn(a), FadeIn(b), FadeIn(la), FadeIn(lb), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"cluster, \ then open", detail=r"Part 7's bowed string", corner=DL, tag_corner=DR)
            pulse(snd, la, d["starts"]["cluster"], d["starts"]["open"] - 0.4, buff=0.08)
            pulse(snd, lb, d["starts"]["open"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def notation(self):
        items = [
            (r"Penderecki's score: \ black bands spanning the width of a cluster, \ wavy lines for vibrato", WHITE),
            (r"Ligeti's \textit{Atmosphères}: \ up to 56 separate string parts, \ each written out exactly", WHITE),
            (r"two opposite answers: \ notate the result, \ or notate every line and let the mass emerge", WHITE),
            (r"either way the score stops looking like what it sounds like", TUNE),
            (r"Part 10's question again: \ what is a notation for?", GREY_A),
        ]
        rows_scene(self, r"writing a mass down", items,
                   "How do you write a mass down? <bookmark mark='b'/> Penderecki drew it: black bands as wide as the cluster, wavy lines for vibrato, arrows for the highest note possible. <bookmark mark='c'/> Ligeti did the opposite, writing out up to fifty-six separate string parts exactly, each line precise, the mass emerging from their sum. <bookmark mark='d'/> Two answers: notate the result, or notate every line and let the result appear. <bookmark mark='e'/> Either way the score stops looking like what it sounds like. <bookmark mark='f'/> It is Part 10's question again: what is a notation for?", marks="cdef")
