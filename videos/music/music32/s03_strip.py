from __future__ import annotations

import numpy as np

from videos.music.music32.common import *  # noqa: F403

IC_COL = {0: EAR, 1: "#F87171", 2: "#FB923C", 3: TUNE, 4: "#A3E635", 5: BLUE, 6: WHITE}


def strip_axes(width=9.0, height=4.6):
    """The Möbius strip drawn flat: centre 0 to 6 across, interval 0 to 12 up; ``.p(c, d)``."""
    g = VGroup()
    fr = Rectangle(width=width, height=height, stroke_color=GREY_B, stroke_width=2)
    mid = DashedLine(fr.get_left(), fr.get_right(), color=GREY_A, stroke_width=1.5)
    g.add(fr, mid)
    g.fr = fr

    def p(c, d):
        return np.array([fr.get_left()[0] + width * c / 6.0, fr.get_bottom()[1] + height * d / 12.0, 0])

    g.p = p
    # the glued ends: up on the left, down on the right
    g.add(Arrow(p(0, 2) + LEFT * 0.25, p(0, 10) + LEFT * 0.25, buff=0, color=EAR, stroke_width=3),
          Arrow(p(6, 10) + RIGHT * 0.25, p(6, 2) + RIGHT * 0.25, buff=0, color=EAR, stroke_width=3))
    return g


class Strip(SoundScene):
    def construct(self):
        chapter(self, 2, r"The M\"obius strip", r"What shape is the space of two-note chords?")
        self.strip()
        self.motions()
        self.twist()
        self.duet()

    # ------------------------------------------------------------------
    def strip(self):
        d = load("strip")
        g = strip_axes().move_to(UP * 0.1)
        dots = VGroup()
        for pt in d["points"]:
            dd = Dot(g.p(pt["c"], pt["d"]), radius=0.07, color=IC_COL[pt["ic"]])
            dots.add(dd)
        labs = VGroup(label(r"unisons", font_size=18, color=EAR).next_to(g.fr, UP, buff=0.12),
                      label(r"unisons", font_size=18, color=EAR).next_to(g.fr, DOWN, buff=0.12),
                      label(r"tritones", font_size=18, color=GREY_A).next_to(g.fr, LEFT, buff=0.55).shift(UP * 0.0))
        key = VGroup(*[VGroup(Dot(radius=0.07, color=IC_COL[k]), label(n, font_size=16, color=GREY_A)).arrange(RIGHT, buff=0.1)
                       for k, n in ((0, "unison"), (1, "semitone"), (2, "tone"), (3, "minor 3rd"), (4, "major 3rd"), (5, "fourth"), (6, "tritone"))]
                     ).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.35)
        head = label(r"all 78 two-note chords of the piano's pitch classes", font_size=24, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is the folded space, drawn flat. Across, the chord's centre, the average of its two notes; up, the "
            "interval between them, from zero to twelve semitones. <bookmark mark='a'/> All seventy-eight two-note chords "
            "of the twelve pitch classes are dots, coloured by interval. The unisons lie along the top and bottom edges, the "
            "tritones along the middle. <bookmark mark='b'/> The left and right ends are glued, but with a twist: the arrows "
            "point opposite ways, so a chord leaving on the right at the top comes back on the left at the bottom. A strip "
            "glued with a twist is a Möbius strip, and it has only one edge: the unisons."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g[0]), FadeIn(g[1]), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.02), FadeIn(labs), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(g[2:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def motions(self):
        d = load("strip")
        c = clip("strip.three")
        g = strip_axes(width=7.0, height=3.8).move_to(LEFT * 2.2 + UP * 0.3)
        base = VGroup(*[Dot(g.p(pt["c"], pt["d"]), radius=0.045, color=DIM) for pt in d["points"]])
        cols = {"parallel": TUNE, "contrary": BLUE, "oblique": EAR}
        paths, dots = {}, {}
        for k, m in d["motions"].items():
            pts = [g.p(cc, dd) for cc, dd in m["points"]]
            dots[k] = VGroup(*[Dot(p, radius=0.09, color=cols[k]) for p in pts])
            paths[k] = VMobject(color=cols[k], stroke_width=3).set_points_as_corners(pts)
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"parallel motion: \ the interval stays, \ the chord slides across", TUNE),
            (r"contrary motion: \ the centre stays, \ the chord climbs from the edge", BLUE),
            (r"oblique motion: \ one voice holds, \ the chord moves on a slant", EAR))]).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 4.4)).move_to(RIGHT * 4.4 + UP * 0.3)
        with self.voiceover(
            "The three kinds of motion from Part 16 become three directions on the strip. <bookmark mark='a'/> In parallel "
            "motion the interval stays nearly the same and the chord slides sideways: minor thirds rising a semitone at a time. <bookmark mark='b'/> "
            "In contrary motion the centre stays put and the chord climbs straight up from the edge: a unison opening out to "
            "a tritone. <bookmark mark='c'/> In oblique motion one voice holds and the chord moves on a slant. Listen to all "
            "three, and watch the paths."
        ) as vo:
            self.play(FadeIn(g[0]), FadeIn(g[1]), FadeIn(base), FadeIn(paths["parallel"]), FadeIn(dots["parallel"]), FadeIn(side[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(paths["contrary"]), FadeIn(dots["contrary"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(paths["oblique"]), FadeIn(dots["oblique"]), FadeIn(side[2]))
        with self.listen(c) as snd:
            window(snd, r"parallel, \ contrary, \ oblique", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            u = d["unit"]
            for k in ("parallel", "contrary", "oblique"):
                for i in range(5):
                    pulse(snd, dots[k][i], d["starts"][k] + i * u, d["starts"][k] + (i + 1) * u - 0.05, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def twist(self):
        rows_ = text_rows([
            (r"take C and E, \ and raise the lower voice: \ C$\sharp$--E, \ D--E, \ E--E", WHITE),
            (r"at E--E the chord touches the edge: \ a unison", EAR),
            (r"keep raising the same voice: \ E--F, \ E--G: \ the chord bounces back into the strip", WHITE),
            (r"the voice has crossed; \ the chord has reflected off the edge", TUNE),
            (r"the hook's puzzle, \ drawn: \ crossing and bouncing are the same path in chord space", GREY_A),
        ], font_size=24)
        head = label(r"what happens at the edge", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The edge explains the hook. <bookmark mark='a'/> Take C and E and raise the lower voice a semitone at a time: "
            "C sharp and E, D and E, E and E. <bookmark mark='b'/> At E and E the chord touches the edge: a unison. "
            "<bookmark mark='c'/> Keep raising the same voice: E and F, E and G. The chord moves back into the strip, "
            "<bookmark mark='d'/> because the voice that crossed is now on top, and the strip does not know which voice is "
            "which. <bookmark mark='e'/> Crossing and bouncing are one and the same path in chord space; only the ordered "
            "plane could tell them apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def duet(self):
        d = load("duet")
        c = clip("duet.first")
        g = strip_axes(width=7.0, height=3.8).move_to(LEFT * 2.2 + UP * 0.2)
        base = VGroup(*[Dot(g.p(pt["c"], pt["d"]), radius=0.045, color=DIM) for pt in load("strip")["points"]])
        dots = VGroup(*[VGroup(Dot(g.p(cc, dd), radius=0.12, color=TUNE), label(str(i + 1), font_size=14, color=BLACK).move_to(g.p(cc, dd)))
                        for i, (cc, dd) in enumerate(d["points"])])
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"Fux's cantus and Part 16's best first-species line: \ eleven two-note chords", WHITE),
            (r"it starts and ends on the edge: \ the octave, \ folded to a unison", EAR),
            (r"in between it wanders into the strip: \ thirds, \ sixths, \ a fifth", TUNE),
            (rf"every step is a shortest path: \ {sum(d['actual'])} semitones in all, \ the minimum", GREY_A))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 4.6)).move_to(RIGHT * 4.3 + UP * 0.2)
        with self.voiceover(
            "Counterpoint is a path on the strip. Here is Fux's cantus firmus from Part 16 with the best first-species line "
            "that part's search found above it: eleven two-note chords, numbered in order. <bookmark mark='a'/> The path "
            "starts and ends on the edge, at the octave, which the strip folds to a unison. <bookmark mark='b'/> In between it "
            "wanders into the strip through thirds, sixths and a fifth, never staying in one place. <bookmark mark='c'/> And "
            "every one of its ten steps is a shortest path between its two chords: the line moves "
            f"{say(sum(d['actual']))} semitones in all, which is the minimum. Listen, and follow the numbers."
        ) as vo:
            self.play(FadeIn(g[0]), FadeIn(g[1]), FadeIn(base), FadeIn(dots), FadeIn(side[0]))
            for mark, r in zip("abc", side[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        with self.listen(c) as snd:
            window(snd, r"Fux's cantus, \ first species", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i in range(len(dots)):
                pulse(snd, dots[i], i * d["unit"], (i + 1) * d["unit"] - 0.05, buff=0.05)
        self.wait(0.3)
        self.clear_scene()
