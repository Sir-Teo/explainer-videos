from __future__ import annotations

import numpy as np

from videos.music.music38.common import *  # noqa: F403

NN = ["C", r"D$\flat$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]


class Subs(SoundScene):
    def construct(self):
        chapter(self, 9, r"ii--V--I, \ turnarounds and the tritone substitution", r"Why can one chord stand in for another a tritone away?")
        self.twofive()
        self.quiz()
        self.tritone()
        self.turnaround()
        self.bebop()

    # ------------------------------------------------------------------
    def twofive(self):
        items = [
            (r"ii--V--I: \ a minor seventh, \ a dominant seventh, \ the tonic: \ roots falling by fifths \ (Part 18)", WHITE),
            (r"the songs jazz players adopted \ (`standards') \ are full of ii--V's, \ often in chains through several keys", WHITE),
            (r"a player hears a tune as a sequence of ii--V's, \ and plays through each", WHITE),
            (r"the same three chords, \ endlessly reharmonised", TUNE),
            (r"two ways to vary them: \ substitute, \ or add", GREY_A),
        ]
        rows_scene(self, r"two-five-one", items,
                   "The two-five-one is the backbone of jazz harmony: a minor seventh, a dominant seventh, and the tonic, the "
                   "roots falling by fifths as in Part 18. <bookmark mark='b'/> The popular songs that jazz players adopted as "
                   "standards are full of two-fives, often in chains through several keys, <bookmark mark='c'/> and a player "
                   "hears a tune as a sequence of them and plays through each. <bookmark mark='d'/> The same three chords, "
                   "endlessly reharmonised. <bookmark mark='e'/> There are two ways to vary them: substitute one chord for "
                   "another, or add chords.", marks="bcde")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("subs")
        c = clip("subs.quiz")
        card = listen_card(r"Two versions of a ii--V--I in C, \ each played twice. \ In one, \ the bass slides down by semitones into the last chord. \ "
                           r"Which one: \ the first or the second?", width=10.4)
        with self.voiceover(
            "A question for your ears. Two versions of a two-five-one in C, each played twice, guide tones over the bass. "
            "In one of them the bass slides down by semitones into the final chord. Which one, the first or the second?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        def col(prog, bassn):
            return VGroup(*[VGroup(label(sym(s), font_size=24, color=WHITE), label(NN[b % 12], font_size=22, color=BLUE)).arrange(DOWN, buff=0.25) for s, b in zip(prog, bassn)]).arrange(RIGHT, buff=0.9)
        a = col(d["progs"]["plain"], d["bass_plain"])
        b = col(d["progs"]["sub"], d["bass_sub"])
        for x in (a, b):
            for k in range(3):
                x[k].set_opacity(0.0)
            x.slots = VGroup(*[RoundedRectangle(width=1.2, height=1.1, corner_radius=0.1, stroke_color=GREY_B, stroke_width=1.5).move_to(x[k]) for k in range(3)])
        g = VGroup(VGroup(label(r"first", font_size=22, color=GREY_A), a).arrange(DOWN, buff=0.3),
                   VGroup(label(r"second", font_size=22, color=GREY_A), b).arrange(DOWN, buff=0.3)).arrange(RIGHT, buff=2.0).move_to(UP * 0.2)
        self.play(FadeOut(card), FadeIn(g), FadeIn(a.slots), FadeIn(b.slots))
        beat = 60.0 / d["bpm"]
        with self.listen(c) as snd:
            window(snd, r"two versions", detail=r"piano and string models", corner=DL, tag_corner=DR)
            for name, x in (("plain", a), ("sub", b)):
                t0 = d["starts"][name]
                for rep in range(2):
                    for k in range(4):
                        tt = t0 + (rep * 4 + k) * 2 * beat
                        pulse(snd, x.slots[min(k, 2)], tt, tt + 2 * beat - 0.05, buff=0.04)
        with self.voiceover(
            "The second. In the first, the bass falls from D to G and rises to C, by fifths and fourths. In the second the "
            "G seven has been replaced by D flat seven, and the bass slides D, D flat, C."
        ):
            self.play(*[x[k].animate.set_opacity(1.0) for x in (a, b) for k in range(3)], FadeOut(a.slots), FadeOut(b.slots))
            self.play(Indicate(b[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tritone(self):
        d = load("subs")
        r = 2.0
        pts = [r * np.array([np.cos(PI / 2 - k * TAU / 12), np.sin(PI / 2 - k * TAU / 12), 0]) for k in range(12)]
        circ = Circle(radius=r, color=DIM, stroke_width=1.5)
        names = VGroup(*[label(NN[k], font_size=18, color=GREY_A).move_to(pts[k] * 1.18) for k in range(12)])
        g7 = [7, 11, 2, 5]
        db7 = [1, 5, 8, 11]
        p1 = Polygon(*[pts[k] for k in g7], color=TUNE, stroke_width=3, fill_opacity=0.12, fill_color=TUNE)
        p2 = Polygon(*[pts[k] for k in db7], color=BLUE, stroke_width=3, fill_opacity=0.12, fill_color=BLUE)
        shared = VGroup(*[Circle(radius=0.22, color=EAR, stroke_width=4).move_to(pts[k]) for k in d["shared"]])
        tri = Line(pts[5], pts[11], color=EAR, stroke_width=5)
        wheel = VGroup(circ, names, p1, p2, shared, tri).move_to(LEFT * 3.0 + DOWN * 0.2)
        side = VGroup(label(r"G7: \ G B D F", font_size=21, color=TUNE),
                      label(r"D$\flat$7: \ D$\flat$ F A$\flat$ C$\flat$ \ (C$\flat$ = B)", font_size=21, color=BLUE),
                      label(r"both contain the tritone F--B, \ their guide tones", font_size=21, color=EAR),
                      label(r"G7's third is D$\flat$7's seventh, \ and the other way round", font_size=19, color=WHITE),
                      label(r"a tritone is half an octave, \ so it is its own inversion: \ two dominants share it", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 3.2)
        head = label(r"the tritone substitution", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Why does D flat seven stand in for G seven? <bookmark mark='a'/> Draw both on the circle of pitch classes. G "
            "seven is G, B, D, F; D flat seven is D flat, F, A flat, and C flat, which is B. <bookmark mark='b'/> They share "
            "exactly two notes, F and B, a tritone apart, and those are the guide tones of both: G seven's third is D flat "
            "seven's seventh, and its seventh is the other's third. Because a tritone is half an octave, it divides the octave "
            "into two equal halves and maps onto itself under transposition by a tritone, so exactly two dominant sevenths "
            "contain it. Keep the guide tones, swap the root, and the bass gets a chromatic path."
        ) as vo:
            self.play(FadeIn(head), FadeIn(circ), FadeIn(names))
            vo.wait_until("a")
            self.play(Create(p1), Create(p2), FadeIn(side[:2]))
            vo.wait_until("b")
            self.play(FadeIn(shared), Create(tri), FadeIn(side[2:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def turnaround(self):
        d = load("subs")
        c = clip("subs.turnaround")
        rows_ = VGroup()
        for name, title, col in (("diatonic", r"I--vi--ii--V", TUNE), ("secondary", r"I--VI7--ii--V", BLUE), ("subs", r"I--$\flat$III7--ii--$\flat$II7", EAR)):
            ch = chart([[s] for s in d["turn"][name]], cell_w=1.9, cell_h=0.6, size=20)
            rows_.add(VGroup(label(title, font_size=20, color=col), ch).arrange(RIGHT, buff=0.5))
        rows_.arrange(DOWN, buff=0.45, aligned_edge=RIGHT).move_to(UP * 0.2)
        head = label(r"a turnaround, \ three ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"each twice: \ the plain one, \ with a secondary dominant, \ and with two tritone substitutes", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "A turnaround is the two bars at the end of a form that lead back to its start. The plain one is one, six, two, "
            "five. Make the six a dominant seventh, a secondary dominant of two, and it pulls harder. Replace both dominants "
            "with their tritone substitutes, and the roots slide chromatically: C, E flat, D, D flat, and C again. Hear each "
            "twice."
        ):
            self.play(FadeIn(head), FadeIn(rows_), FadeIn(cap))
        beat = 60.0 / d["bpm"]
        with self.listen(c) as snd:
            window(snd, r"three turnarounds", detail=r"piano and string models", corner=DL, tag_corner=DR)
            for i, name in enumerate(("diatonic", "secondary", "subs")):
                t0 = d["turn_starts"][name]
                for k in range(8):
                    tt = t0 + k * 2 * beat
                    pulse(snd, rows_[i][1].bars[k % 4], tt, tt + 2 * beat - 0.05, buff=0.03)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bebop(self):
        items = [
            (r"bebop, \ New York in the 1940s: \ Charlie Parker, \ Dizzy Gillespie, \ Thelonious Monk", WHITE),
            (r"fast tempos, \ dense substitutions, \ new melodies written over the chords of standards", WHITE),
            (r"a new melody on old changes avoided paying for the song: \ chords are not copyrighted, \ melodies are", WHITE),
            (r"John Coltrane's \textit{Giant Steps} \ (1959) \ moves its key centres by major thirds", TUNE),
            (r"Part 39 follows the changes further", GREY_A),
        ]
        rows_scene(self, r"after swing", items,
                   "After the swing era came bebop, in New York in the 1940s: Charlie Parker, Dizzy Gillespie, Thelonious Monk. "
                   "<bookmark mark='b'/> Fast tempos, dense substitutions, and new melodies written over the chords of standards. "
                   "<bookmark mark='c'/> A new melody on old changes also avoided paying for the song, since chord progressions "
                   "are not copyrighted and melodies are. <bookmark mark='d'/> John Coltrane's Giant Steps, in 1959, moved its "
                   "key centres by major thirds. <bookmark mark='e'/> Part 39 follows the changes further.", marks="bcde")
