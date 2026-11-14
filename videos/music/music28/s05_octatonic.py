from __future__ import annotations

import numpy as np

from videos.music.music28.common import *  # noqa: F403
from videos.music.music28.s02_wholetone import clock

PARTS = ["scale", "chord", "ostinato"]


class Octatonic(SoundScene):
    def construct(self):
        chapter(self, 4, r"The octatonic", r"What scale holds two chords a tritone apart?", extra=((1911, r"\textit{Petrushka}"),))
        self.scale()
        self.triads()
        self.hear()
        self.history()

    # ------------------------------------------------------------------
    def scale(self):
        oc = clock([0, 1, 3, 4, 6, 7, 9, 10], radius=1.6, color=TUNE).move_to(LEFT * 3.6 + DOWN * 0.2)
        rows_ = VGroup(*[label(t, font_size=22, color=c_) for t, c_ in (
            (r"half step, \ whole step, \ half, \ whole ...: \ eight notes", WHITE),
            (r"only three different transpositions: \ Messiaen's second mode", WHITE),
            (r"it holds four major triads, \ a minor third apart: \ C, \ E$\flat$, \ F$\sharp$, \ A", TUNE),
            (r"and so C major and F$\sharp$ major together: \ a tritone apart", EAR),
            (r"Arthur Berger named it `octatonic' \ (1963)", GREY_A))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 2.6 + DOWN * 0.2)
        rows_.scale_to_fit_width(min(rows_.width, 6.6))
        head = label(r"the octatonic scale on C", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The second of Messiaen's modes had a long life before him. <bookmark mark='a'/> Alternate half steps and whole "
            "steps, and after eight notes you are back where you began. <bookmark mark='b'/> Like the whole-tone scale it is "
            "symmetric: there are only three different octatonic scales. <bookmark mark='c'/> It contains four major "
            "triads, a minor third apart, on C, E flat, F sharp and A, and four minor ones. <bookmark mark='d'/> So C major "
            "and F sharp major, as far apart as two keys can be, live inside one scale. <bookmark mark='e'/> The name "
            "octatonic, eight-note, is the theorist Arthur Berger's, from 1963."
        ) as vo:
            self.play(FadeIn(head), FadeIn(oc))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("octatonic")
        c = clip("octatonic.three")
        g1 = mroll(d["scale"], width=3.4, height=1.8, lo=58, hi=74, color=TUNE)
        g2 = voices_roll([d["chord"][:3], d["chord"][3:], d["arp"]], width=3.8, height=1.8, colors=[BLUE, EAR, GREY_A], lo=46, hi=80, bar_h=0.08)
        g3 = mroll(d["ostinato"], width=3.6, height=1.8, lo=46, hi=62, color=TUNE, bar_h=0.09)
        cols = VGroup(*[VGroup(label(t, font_size=19, color=GREY_A), g).arrange(DOWN, buff=0.3) for t, g in (
            (r"the scale", g1), (r"C and F$\sharp$ major together, \ then broken", g2), (r"an ostinato on the scale \ (ours)", g3))]).arrange(RIGHT, buff=0.6).move_to(DOWN * 0.1)
        head = label(r"the octatonic, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Three things to hear. The scale itself, rising from C. Then C major and F sharp major sounded together, the "
            "pair of chords that became famous in Stravinsky's ballet Petrushka of 1911, first as one chord and then broken "
            "into arpeggios. Then an ostinato of our own that circles the scale low in the strings."
        ):
            self.play(FadeIn(head), FadeIn(cols))
        with self.listen(c) as snd:
            window(snd, r"scale, \ chord, \ ostinato", detail=r"Part 7's piano and bowed string", corner=DL, tag_corner=DR)
            flash(snd, g1.notes, [d["starts"]["scale"] + n[1] * d["units"]["scale"] for n in d["scale"]], hot=WHITE, base=TUNE)
            flash_voices(snd, g2, [d["chord"][:3], d["chord"][3:], d["arp"]], d["starts"]["chord"], d["units"]["chord"], colors=[BLUE, EAR, GREY_A])
            flash(snd, g3.notes, [d["starts"]["ostinato"] + n[1] * d["units"]["ostinato"] for n in d["ostinato"]], hot=WHITE, base=TUNE)
            for i, k in enumerate(PARTS):
                end = d["starts"][PARTS[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, cols[i][0], d["starts"][k], end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"Nikolai Rimsky-Korsakov used it from the 1860s for the fantastic: \ in Russia, \ `the Rimsky-Korsakov scale'", WHITE),
            (r"Stravinsky, \ his pupil, \ in \textit{The Firebird} \ (1910), \ \textit{Petrushka} \ (1911), \ \textit{The Rite of Spring} \ (1913)", WHITE),
            (r"the `Petrushka chord': \ C and F$\sharp$ major at once, \ one in each of the pianist's hands", WHITE),
            (r"Bartók, \ Messiaen, \ and later jazz improvisers \ (the `diminished scale')", TUNE),
            (r"how much of Stravinsky is octatonic is still argued: \ chapter ten", GREY_A),
        ]
        rows_scene(self, r"a scale for the fantastic", items,
                   "The scale has a Russian history. <bookmark mark='b'/> Nikolai Rimsky-Korsakov used it from the 1860s for "
                   "magic and the fantastic, and in Russia it is still called his scale. <bookmark mark='c'/> His pupil Igor "
                   "Stravinsky used it in The Firebird, Petrushka and The Rite of Spring, <bookmark mark='d'/> and the "
                   "Petrushka chord, C major and F sharp major at once, sits in the two hands of a pianist, white keys "
                   "against black. <bookmark mark='e'/> Bartók and Messiaen used it, and jazz improvisers know it as the "
                   "diminished scale. <bookmark mark='f'/> How much of Stravinsky's music is really octatonic is still "
                   "argued, and chapter ten weighs the argument with numbers.", marks="cdef")

    # ------------------------------------------------------------------
    def triads(self):
        d = load("triads")
        c = clip("triads.four")
        names = [r"C", r"E$\flat$", r"F$\sharp$", r"A"]
        cells = VGroup()
        for i, r in enumerate(d["roots"]):
            cl = clock([0, 1, 3, 4, 6, 7, 9, 10], radius=1.0, color=GREY_B, labels=False)
            tri = [(r + x) % 12 for x in (0, 4, 7)]
            hi = VGroup(*[cl.dots[k].copy().set_color(TUNE).scale(1.4) for k in tri])
            poly = Polygon(*[cl.dots[k].get_center() for k in sorted(tri)], color=TUNE, stroke_width=3, fill_opacity=0.2)
            cells.add(VGroup(VGroup(cl, poly, hi), label(names[i] + r" major", font_size=22, color=TUNE)).arrange(DOWN, buff=0.3))
        cells.arrange(RIGHT, buff=0.7).move_to(DOWN * 0.1)
        head = label(r"four major triads inside one octatonic scale", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Hear the four major triads of one octatonic scale, one after another: C, E flat, F sharp, A, each a minor "
            "third above the last. In a key, these chords would be distant relatives; here they are neighbours in one "
            "collection, which is why music built on it can move between them without ever leaving."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"C, \ E$\flat$, \ F$\sharp$, \ A", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i in range(4):
                pulse(snd, cells[i][1], 2 * i * d["unit"], (2 * i + 2) * d["unit"] - 0.1, buff=0.08)
        self.wait(0.3)
        self.clear_scene()
