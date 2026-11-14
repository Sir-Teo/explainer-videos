from __future__ import annotations

import numpy as np

from videos.music.music31.common import *  # noqa: F403

PC = ["C", r"C$\sharp$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]


class Cycles(SoundScene):
    def construct(self):
        chapter(self, 4, r"Hexatonic and octatonic cycles", r"What happens if you repeat two moves?")
        self.hear()
        self.sets()
        self.cohn()
        self.systems()
        self.weitzmann()
        self.russians()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("cycles")
        c = clip("cycles.two")
        r1 = VGroup(*[label(tex_triad(n), font_size=30, color=TUNE) for n in d["hexatonic"]]).arrange(RIGHT, buff=0.55)
        r2 = VGroup(*[label(tex_triad(n), font_size=30, color=BLUE) for n in d["octatonic"]]).arrange(RIGHT, buff=0.45)
        l1 = label(r"P, \ L, \ P, \ L ...: \ six triads, \ then home", font_size=21, color=TUNE)
        l2 = label(r"P, \ R, \ P, \ R ...: \ eight triads, \ then home", font_size=21, color=BLUE)
        g = VGroup(VGroup(l1, r1).arrange(DOWN, buff=0.3), VGroup(l2, r2).arrange(DOWN, buff=0.3)).arrange(DOWN, buff=0.9).move_to(DOWN * 0.1)
        head = label(r"two moves, \ repeated", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Repeat two moves in turn and the chain must come back home, because the space is finite. P and L, alternating "
            "from C major: C, C minor, A flat, A flat minor, E, E minor, and C again, six triads. P and R alternating: eight "
            "triads, from C through E flat, F sharp and A. Hear both cycles; every step changes a single note."
        ):
            self.play(FadeIn(head), FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"hexatonic, \ then octatonic", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            u = d["unit"]
            for i in range(len(r1)):
                pulse(snd, r1[i], d["starts"]["hexatonic"] + i * u, d["starts"]["hexatonic"] + (i + 1) * u - 0.05, buff=0.06)
            for i in range(len(r2)):
                pulse(snd, r2[i], d["starts"]["octatonic"] + i * u, d["starts"]["octatonic"] + (i + 1) * u - 0.05, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sets(self):
        d = load("cycles")
        hs = ", ".join(PC[x] for x in d["hexa_set"])
        os_ = ", ".join(PC[x] for x in d["octa_set"])
        rows_ = text_rows([
            (rf"the hexatonic cycle uses six pitch classes: \ {hs}", TUNE),
            (r"that is Part 28's hexatonic scale: \ half step, \ minor third, \ repeated", WHITE),
            (rf"the octatonic cycle uses eight: \ {os_}", BLUE),
            (r"that is the octatonic scale, \ Messiaen's second mode", WHITE),
            (r"the cycles are the symmetric scales of Part 28, \ walked chord by chord", GREY_A),
        ], font_size=24)
        head = label(r"cycles make scales", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Gather the notes each cycle uses. <bookmark mark='a'/> The hexatonic cycle uses six pitch classes, "
            "<bookmark mark='b'/> exactly Part 28's hexatonic scale, a half step and a minor third, repeated. "
            "<bookmark mark='c'/> The octatonic cycle uses eight, <bookmark mark='d'/> the octatonic scale, Messiaen's "
            "second mode. <bookmark mark='e'/> The cycles are Part 28's symmetric scales, walked one chord at a time; that "
            "is where their names come from."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cohn(self):
        items = [
            (r"Richard Cohn \ (1996): \ four hexatonic cycles divide the 24 triads into four groups of six", WHITE),
            (r"within a cycle, \ triads a major third apart, \ joined by smooth voice leading", WHITE),
            (r"opposite triads in a cycle share no notes: \ the `hexatonic pole', \ C major and A$\flat$ minor", TUNE),
            (r"the pole sounds strange, \ even uncanny, \ yet the voices move only a semitone each", WHITE),
            (r"Cohn's \textit{Audacious Euphony} \ (2012): \ a theory of late Romantic triadic harmony", GREY_A),
        ]
        rows_scene(self, r"Cohn's hexatonic systems", items,
                   "Richard Cohn made these cycles the basis of a theory. <bookmark mark='b'/> The four hexatonic cycles split "
                   "the twenty-four triads into four families of six, <bookmark mark='c'/> triads a major third apart, joined "
                   "by the smoothest voice leading. <bookmark mark='d'/> Opposite each other in a cycle sit two triads that share "
                   "no notes, like C major and A flat minor: the hexatonic pole. <bookmark mark='e'/> The pole sounds strange, "
                   "even uncanny, although each voice moves only a semitone. <bookmark mark='f'/> Cohn's book Audacious "
                   "Euphony, of 2012, builds a theory of late Romantic harmony on it.", marks="cdef")

    # ------------------------------------------------------------------
    def systems(self):
        d = load("systems")
        hx = VGroup()
        for s in d["hexatonic"]:
            hx.add(VGroup(*[label(tex_triad(n), font_size=22, color=TUNE if not n.endswith("m") else BLUE) for n in s]).arrange(RIGHT, buff=0.3))
        hx.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        ox = VGroup()
        for s in d["octatonic"]:
            ox.add(VGroup(*[label(tex_triad(n), font_size=22, color=TUNE if not n.endswith("m") else BLUE) for n in s]).arrange(RIGHT, buff=0.26))
        ox.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        lh = label(r"P, \ L: \ four hexatonic systems of six", font_size=21, color=GREY_A)
        lo = label(r"P, \ R: \ three octatonic systems of eight", font_size=21, color=GREY_A)
        left = VGroup(lh, hx).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        right = VGroup(lo, ox).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        g = VGroup(left, right).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.2)
        g.scale_to_fit_width(min(g.width, 12.8))
        head = label(r"two ways to cut 24 triads into equal families", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"every triad lies in exactly one hexatonic and one octatonic system", font_size=21, color=EAR).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Run the hexatonic cycle from every triad, and the twenty-four fall into exactly four families of six. "
            "<bookmark mark='a'/> Cohn named them after the points of the compass. Run the octatonic cycle the same way and "
            "they fall into three families of eight. <bookmark mark='b'/> Every triad belongs to exactly one family of each "
            "kind. These families are the orbits of the subgroups made by P and L, and by P and R: the same counting as Part "
            "29's set classes, one level up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left))
            vo.wait_until("a")
            self.play(FadeIn(right))
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def weitzmann(self):
        d = load("weitzmann")
        c = clip("weitzmann.region")
        aug = label(r"C, \ E, \ G$\sharp$", font_size=36, color=EAR).move_to(UP * 0.3)
        al = label(r"the augmented triad", font_size=20, color=GREY_A).next_to(aug, DOWN, buff=0.2)
        cells = VGroup()
        for i, n in enumerate(d["region"]):
            ang = PI / 2 - i * TAU / 6
            cells.add(label(tex_triad(n), font_size=32, color=TUNE if not n.endswith("m") else BLUE).move_to(aug.get_center() + 2.6 * np.array([np.cos(ang) * 1.5, np.sin(ang), 0])))
        lines = VGroup(*[Line(aug.get_center(), cl.get_center(), color=GREY_B, stroke_width=1.5, buff=0.6) for cl in cells])
        head = label(r"Weitzmann \ (1853): \ one chord, \ six resolutions", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Each hexatonic family has a hidden centre. Carl Friedrich Weitzmann noticed it in 1853. The augmented triad, "
            "C, E, G sharp, divides the octave into three equal major thirds. Move any one of its notes by a semitone and "
            "you land on a major or minor triad: six of them, C, E and A flat major, and C sharp, F and A minor. Listen to the "
            "augmented chord resolving each way in turn: one voice moves each time."
        ):
            self.play(FadeIn(head), FadeIn(aug), FadeIn(al), FadeIn(lines), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"one augmented triad, \ six ways out", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            u = d["unit"]
            for i, t0 in enumerate(d["starts"]):
                pulse(snd, aug, t0, t0 + u - 0.05, buff=0.1)
                pulse(snd, cells[i], t0 + u, t0 + 2 * u - 0.05, buff=0.08)
        with self.voiceover(
            "How do the two pictures fit together? Each of Cohn's families sits between two augmented chords a semitone "
            "apart: the family of C major uses C, E, G sharp and B, E flat, G, and nothing else. Weitzmann's region looks out "
            "from one augmented chord in both directions: its three major triads come from one of Cohn's families and its "
            "three minor triads from the next. Either way, an augmented chord sits one semitone from six triads, which is "
            "why it sounds as if it could go anywhere."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def russians(self):
        items = [
            (r"Rimsky-Korsakov used the octatonic scale so often that Russians called it his scale", WHITE),
            (r"Stravinsky's \textit{Petrushka} \ (1911): \ C major and F$\sharp$ major sounded together", WHITE),
            (r"C and F$\sharp$ lie in the same octatonic family: \ C, \ E$\flat$, \ F$\sharp$, \ A, \ major and minor", TUNE),
            (r"so the clash is two chords from one eight-note scale, \ a tritone apart", WHITE),
            (r"Part 28 heard the scale; \ here the family explains the chord", GREY_A),
        ]
        rows_scene(self, r"octatonic families in practice", items,
                   "The octatonic families were heard long before they were named. <bookmark mark='b'/> Rimsky-Korsakov used the octatonic scale so often that Russian musicians called it his scale. <bookmark mark='c'/> His pupil Stravinsky sounded C major and F sharp major together in Petrushka, in 1911. <bookmark mark='d'/> Look at the families: C and F sharp lie in the same octatonic family, with E flat and A, major and minor. <bookmark mark='e'/> So the famous clash is two chords from one eight-note scale, a tritone apart. <bookmark mark='f'/> Part 28 heard the scale; here the family explains the chord.", marks="cdef")
