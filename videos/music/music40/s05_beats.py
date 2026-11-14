from __future__ import annotations

import numpy as np

from videos.music.music40.common import *  # noqa: F403

ROWC = {"kick": TUNE, "snare": EAR, "hat": GREY_A, "open": BLUE}


def beat_grid(p, cell=0.32):
    rows_ = VGroup()
    for k in ("kick", "snare", "hat", "open"):
        on = set(p.get(k, []))
        pat = ["x" if i in on else "." for i in range(16)]
        rows_.add(pat_row(pat, cell=cell, color=ROWC[k], name={"kick": r"kick", "snare": r"snare", "hat": r"hi-hat", "open": r"open hat"}[k], size=15))
    return rows_.arrange(DOWN, buff=0.08, aligned_edge=RIGHT)


class Beats(SoundScene):
    def construct(self):
        chapter(self, 4, r"The backbeat and groove", r"Why do the drums hit hardest on two and four?")
        self.backbeat()
        self.grids()
        self.hear()
        self.funk()
        self.swing()
        self.dance()

    # ------------------------------------------------------------------
    def backbeat(self):
        items = [
            (r"the backbeat: \ the snare on beats 2 and 4 of every bar, \ loud", WHITE),
            (r"from gospel's handclaps and swing's hi-hat on 2 and 4 \ (Part 38) \ to New Orleans rhythm and blues", WHITE),
            (r"drummers such as Earl Palmer made it the ground of rock and roll in the 1950s", WHITE),
            (r"the kick takes 1 and 3, \ the snare 2 and 4: \ a dialogue, \ like the surdos of Part 37", TUNE),
            (r"almost every style since keeps it, \ or bends it on purpose", GREY_A),
        ]
        rows_scene(self, r"the backbeat", items,
                   "The backbeat is the snare on beats two and four of every bar, loud. <bookmark mark='b'/> It came from "
                   "gospel's handclaps and swing's hi-hat on two and four, through New Orleans rhythm and blues, "
                   "<bookmark mark='c'/> and drummers such as Earl Palmer made it the ground of rock and roll in the 1950s. "
                   "<bookmark mark='d'/> The kick takes one and three, the snare two and four: a dialogue, like the two surdos of "
                   "Part 37's samba. <bookmark mark='e'/> Almost every style since keeps it, or bends it on purpose.", marks="bcde")

    # ------------------------------------------------------------------
    def grids(self):
        d = load("beats")
        gs = VGroup()
        for style in ("rock", "funk", "disco", "house", "trap"):
            g = beat_grid(d["patterns"][style], cell=0.2)
            gs.add(VGroup(label(rf"{style} \ ({d['tempo'][style]})", font_size=18, color=WHITE), g).arrange(DOWN, buff=0.12))
        gs.arrange_in_grid(rows=2, cols=3, buff=(0.4, 0.45)).move_to(DOWN * 0.1)
        gs.scale_to_fit_width(min(gs.width, 13.2))
        head = label(r"five beats, \ sixteen steps a bar \ (beats per minute in brackets)", font_size=24, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here are five beats drawn on the sixteen-step grid of a drum machine. <bookmark mark='a'/> Rock: kick on one and "
            "three, snare on two and four, hi-hat in eighths. Funk: the snare adds ghost notes, the hat runs in sixteenths, "
            "and the kick dances around beat one. <bookmark mark='b'/> Disco: the kick on every beat, four on the floor, "
            "with the open hat on every off-beat. House keeps disco's kick and open hat on a drum machine. And a trap-style "
            "beat: the snare only on beat three, so the beat feels half as fast as the hats."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gs.copy().set_opacity(0.2)))
            vo.wait_until("a")
            self.play(FadeIn(gs[0]), FadeIn(gs[1]))
            vo.wait_until("b")
            self.play(FadeIn(gs[2]), FadeIn(gs[3]), FadeIn(gs[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("beats")
        c = clip("beats.five")
        styles = ("rock", "funk", "disco", "house", "trap")
        gs = VGroup()
        for style in styles:
            g = beat_grid(d["patterns"][style], cell=0.2)
            gs.add(VGroup(label(style, font_size=18, color=WHITE), g).arrange(DOWN, buff=0.12))
        gs.arrange_in_grid(rows=2, cols=3, buff=(0.4, 0.45)).move_to(UP * 0.1)
        gs.scale_to_fit_width(min(gs.width, 13.2))
        with self.voiceover("Hear two bars of each, in turn."):
            self.play(FadeIn(gs))
        with self.listen(c) as snd:
            window(snd, r"five beats", detail=r"acoustic kit and drum-machine voices", corner=DL, tag_corner=DR)
            for i, style in enumerate(styles):
                t0 = d["starts"][style]
                step = 60.0 / d["tempo"][style] / 4
                for k, row in zip(("kick", "snare", "hat", "open"), gs[i][1]):
                    ons = d["patterns"][style].get(k, [])
                    if ons:
                        flash_cells(snd, row.cells, ons, t0, step, 2, 16, color=ROWC[k])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def funk(self):
        items = [
            (r"James Brown's band put the weight on `the one', \ the first beat of the bar, \ everyone together", WHITE),
            (r"everything else is syncopated around it: \ guitar scratches, \ bass, \ horn stabs", WHITE),
            (r"Clyde Stubblefield's and John `Jabo' Starks's drumming was later sampled endlessly \ (chapter 7)", WHITE),
            (r"groove: \ many parts, \ each simple, \ locked together \ (Part 37's ensembles)", TUNE),
            (r"measured: \ funk's sixteenths swing slightly, \ like Part 38's eighths", GREY_A),
        ]
        rows_scene(self, r"the one", items,
                   "Funk moved the weight. <bookmark mark='b'/> James Brown's band put it on the one, the first beat of the "
                   "bar, everyone together, <bookmark mark='c'/> and syncopated everything else around it: guitar scratches, "
                   "bass, horn stabs. <bookmark mark='d'/> His drummers, Clyde Stubblefield and John Jabo Starks, were later "
                   "sampled endlessly, as chapter seven explains. <bookmark mark='e'/> Groove is many parts, each simple, locked "
                   "together, like Part 37's ensembles. <bookmark mark='f'/> And measured, funk's sixteenths often swing "
                   "slightly, as Part 38's eighths did.", marks="cdef")

    # ------------------------------------------------------------------
    def swing(self):
        d = load("swing16")
        c = clip("swing16.two")
        def pairs(sw, col):
            g = VGroup()
            for k in range(8):
                g.add(Dot([k * 1.2, 0, 0], radius=0.1, color=col), Dot([(k + sw) * 1.2, 0, 0], radius=0.07, color=col))
            ticks = VGroup(*[Line([k * 1.2, -0.25, 0], [k * 1.2, 0.25, 0], color=GREY_B if k % 2 == 0 else GREY_D) for k in range(9)])
            return VGroup(ticks, g)
        a = VGroup(label(r"straight: \ 50\%", font_size=20, color=BLUE), pairs(0.5, BLUE)).arrange(RIGHT, buff=0.5)
        b = VGroup(label(rf"swung: \ {round(100 * d['swing'])}\%", font_size=20, color=TUNE), pairs(d["swing"], TUNE)).arrange(RIGHT, buff=0.5)
        g = VGroup(a, b).arrange(DOWN, buff=0.7, aligned_edge=RIGHT).move_to(UP * 0.3)
        cap = label(r"a drum machine's swing knob: \ where the second sixteenth of each pair falls", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"swing on the sixteenths", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Drum machines brought Part 38's swing to the sixteenth note. Roger Linn's machines had a swing setting: how far "
            "through each pair of sixteenths the second one falls, fifty per cent for straight, more for swung. Hear our funk "
            "beat straight, then at sixty per cent."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"straight, \ then swung", detail=r"acoustic kit models", corner=DL, tag_corner=DR)
            pulse(snd, a, d["starts"]["straight"], d["starts"]["swung"] - 0.3, buff=0.1)
            pulse(snd, b, d["starts"]["swung"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dance(self):
        items = [
            (r"disco \ (1970s): \ four on the floor at about 120 beats a minute, \ the open hat on the off-beats", WHITE),
            (r"Giorgio Moroder's sequenced synthesizers \ (1977) \ pointed to dance music made by machines", WHITE),
            (r"Chicago house \ (mid-1980s) \ and Detroit techno: \ drum machines, \ DJs, \ clubs", WHITE),
            (r"the DJ became a performer: \ two records beat-matched into one continuous groove", TUNE),
            (r"chapter 6: \ the drum machines themselves", GREY_A),
        ]
        rows_scene(self, r"disco to house", items,
                   "Disco, in the 1970s, set four on the floor at about a hundred and twenty beats a minute, with the open hat "
                   "on the off-beats. <bookmark mark='b'/> Giorgio Moroder's sequenced synthesizers, in 1977, pointed to dance "
                   "music made by machines. <bookmark mark='c'/> Chicago house and Detroit techno, in the mid-1980s, were built "
                   "on drum machines, by DJs, for clubs. <bookmark mark='d'/> The DJ became a performer, beat-matching two records "
                   "into one continuous groove. <bookmark mark='e'/> Chapter six turns to the drum machines themselves.",
                   marks="bcde")
