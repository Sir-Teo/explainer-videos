from __future__ import annotations

import numpy as np

from videos.music.music38.common import *  # noqa: F403

NN = ["C", r"D$\flat$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]


class Guide(SoundScene):
    def construct(self):
        chapter(self, 8, r"Sevenths and guide tones", r"Which two notes of a chord matter most?")
        self.kinds()
        self.twofive()
        self.hear()
        self.blues()
        self.voicings()

    # ------------------------------------------------------------------
    def kinds(self):
        rows_ = VGroup()
        for name, iv, desc in ((r"Cmaj7", (0, 4, 7, 11), r"major third, \ major seventh"),
                               (r"C7", (0, 4, 7, 10), r"major third, \ minor seventh: \ the dominant"),
                               (r"Cm7", (0, 3, 7, 10), r"minor third, \ minor seventh"),
                               (r"Cm7$\flat$5", (0, 3, 6, 10), r"minor third, \ flat fifth, \ minor seventh"),
                               (r"C$^{\circ}$7", (0, 3, 6, 9), r"minor third, \ flat fifth, \ diminished seventh")):
            spelling = {(0, 4, 7, 11): ["C", "E", "G", "B"],
                        (0, 4, 7, 10): ["C", "E", "G", r"B$\flat$"],
                        (0, 3, 7, 10): ["C", r"E$\flat$", "G", r"B$\flat$"],
                        (0, 3, 6, 10): ["C", r"E$\flat$", r"G$\flat$", r"B$\flat$"],
                        (0, 3, 6, 9): ["C", r"E$\flat$", r"G$\flat$", r"B$\flat\flat$"]}[iv]
            notes = VGroup(*[label(n, font_size=20, color=(TUNE if k in (1, 3) else GREY_A)) for k, n in enumerate(spelling)]).arrange(RIGHT, buff=0.35)
            rows_.add(VGroup(label(name, font_size=22, color=WHITE), notes, label(desc, font_size=18, color=GREY_A)))
        for i, r in enumerate(rows_):
            y = 1.7 - 0.75 * i
            r[0].move_to([-5.0, y, 0], aligned_edge=LEFT)
            r[1].move_to([-2.6, y, 0], aligned_edge=LEFT)
            r[2].move_to([0.6, y, 0], aligned_edge=LEFT)
        cap = label(r"gold: third and seventh, useful guide tones\\Cm7 and Cm7$\flat$5 share them; the fifth distinguishes those chords", font_size=19, color=TUNE).to_edge(DOWN, buff=0.7)
        head = label(r"five seventh chords on C", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Jazz harmony is built from seventh chords. Here are five on C. <bookmark mark='a'/> What tells them apart? The shared root does not distinguish them. The third and seventh identify much of their quality, but not everything: C minor seven and C half-diminished share E flat and B flat, and differ in the fifth. Even with a root, guide tones alone do not uniquely identify every chord. Players call them the guide tones."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def twofive(self):
        d = load("guide")
        g = d["iiVI"]
        syms = [r"Dm7", r"G7", r"Cmaj7"]
        cols = VGroup()
        for i, s in enumerate(syms):
            col = VGroup(label(s, font_size=26, color=WHITE),
                         label(NN[g["upper"][i] % 12], font_size=30, color=TUNE),
                         label(NN[g["lower"][i] % 12], font_size=30, color=BLUE)).arrange(DOWN, buff=0.45)
            cols.add(col)
        cols.arrange(RIGHT, buff=2.4).move_to(UP * 0.4)
        arrows = VGroup()
        for i in range(2):
            for row in (1, 2):
                a, b = cols[i][row], cols[i + 1][row]
                same = (g["upper"] if row == 1 else g["lower"])[i] == (g["upper"] if row == 1 else g["lower"])[i + 1]
                arrows.add(Arrow(a.get_right(), b.get_left(), buff=0.25, color=GREY_B if same else EAR, stroke_width=3))
        roles = VGroup(label(r"Dm7: \ F is the third, \ C the seventh", font_size=18, color=GREY_A),
                       label(r"G7: \ F is now the seventh, \ B the third", font_size=18, color=GREY_A),
                       label(r"Cmaj7: \ B the seventh, \ E the third", font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.6).next_to(cols, DOWN, buff=0.5)
        cap = label(rf"total motion: \ {d['iiVI']['total']} semitones; \ each voice moves by a semitone or stays", font_size=21, color=TUNE).to_edge(DOWN, buff=0.7)
        head = label(r"guide tones through ii--V--I in C", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now take the commonest progression in jazz, two-five-one: D minor seven, G seven, C major seven. "
            "<bookmark mark='a'/> Monochord's guide-tone solver assigns each chord's third and seventh to two voices so that "
            "the total motion is least. <bookmark mark='b'/> The answer: F and C, then F and B, then E and B. Each voice "
            f"either holds or moves by one semitone; {say(d['iiVI']['total'])} semitones in all. And look at what happens to "
            "the roles: D minor's third, F, becomes G seven's seventh, which falls to E, C major's third; D minor's seventh, "
            "C, falls to B, G's third, which becomes C major's seventh. The sevenths fall into thirds."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(c[0]) for c in cols])
            vo.wait_until("a")
            self.play(*[FadeIn(c[1:]) for c in cols])
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(roles), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("guide")
        c = clip("guide.lines")
        beat = 60.0 / d["bpm"]
        beat2 = 60.0 / d["bpm2"]
        gj = d["jazz"]
        syms = d["jazz_symbols"]
        bars = load("walking")["changes"]
        starts, durs = [], []
        idx = 0
        for b, bar in enumerate(bars):
            for j, s in enumerate(bar):
                starts.append(b * 4 + j * 4 // len(bar))
                durs.append(4 // len(bar))
                idx += 1
        up = [[m, a, du] for m, a, du in zip(gj["upper"], starts, durs)]
        lo = [[m, a, du] for m, a, du in zip(gj["lower"], starts, durs)]
        roll = voices_roll([up, lo], width=11.4, height=2.4, colors=[TUNE, BLUE], total=48, lo=54, hi=72, bar_h=0.14).move_to(DOWN * 1.2)
        two = VGroup(label(r"first: \ ii--V--I, \ twice", font_size=20, color=WHITE), label(r"then: \ the jazz blues, \ fifteen chords", font_size=20, color=WHITE)).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.5)
        ch = chart(bars, cell_w=2.4, cell_h=0.55, size=16).move_to(UP * 1.2)
        with self.voiceover(
            "Hear guide tones alone, on piano over the bass's roots: the two-five-one twice, slowly, and then the jazz blues "
            "of chapter one, fifteen chords, with the two lines the solver chose. They sound like two voices of a quiet "
            "chorale, though they are nothing but thirds and sevenths."
        ):
            self.play(FadeIn(two), FadeIn(ch), FadeIn(roll))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"guide tones", detail=r"piano and string models", corner=DL, tag_corner=DR)
            pulse(snd, two[0], st["iiVI"], st["jazz"] - 0.5, buff=0.08)
            pulse(snd, two[1], st["jazz"], c.duration, buff=0.08)
            flash(snd, roll.parts[0].notes, [st["jazz"] + a * beat2 for _, a, _ in up], hot=WHITE, base=TUNE)
            flash(snd, roll.parts[1].notes, [st["jazz"] + a * beat2 for _, a, _ in lo], hot=WHITE, base=BLUE)
            for k in range(12):
                pulse(snd, ch.bars[k], st["jazz"] + k * 4 * beat2, st["jazz"] + (k + 1) * 4 * beat2 - 0.03, buff=0.03)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blues(self):
        d = load("guide")
        gj = d["jazz"]
        mv = gj["moves"]
        from collections import Counter
        cnt = Counter(mv)
        side = VGroup(label(rf"fifteen chords, \ {len(mv)} changes: \ total motion {gj['total']} semitones", font_size=21, color=WHITE),
                      label(rf"the biggest step in either voice: \ {gj['max_step']} semitones", font_size=21, color=WHITE),
                      label(rf"changes where both voices move by at most a semitone: \ {sum(1 for i in range(len(mv)) if max(abs(gj['upper'][i + 1] - gj['upper'][i]), abs(gj['lower'][i + 1] - gj['lower'][i])) <= 1)} of {len(mv)}", font_size=21, color=TUNE),
                      label(r"the same search Part 32 ran on triads, \ restricted to two structurally useful notes, with other chord tones omitted", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"guide tones through the jazz blues, \ counted", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Through the whole jazz blues, the solver's two lines move {say(gj['total'])} semitones in all across "
            f"{say(len(mv))} chord changes, and neither voice ever moves more than {say(gj['max_step'])}. It is Part 32's "
            "search for smooth voice leading, restricted to two structurally useful notes, with other chord tones omitted. This is why jazz players practise "
            "guide-tone lines: they are the shortest path through the changes, and they can make harmonic movement clear, although guide tones alone leave some chord qualities ambiguous."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(s) for s in side], lag_ratio=0.4), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def voicings(self):
        items = [
            (r"`shell' voicings: \ root, \ third and seventh, \ as bebop pianists such as Bud Powell played them", WHITE),
            (r"`rootless' voicings: \ third and seventh with ninth and thirteenth, \ the bass taking the root \ (Bill Evans and others)", WHITE),
            (r"comping with guide tones leaves room for the bass, \ and for the soloist", WHITE),
            (r"a soloist who lands on guide tones at the changes makes the harmony audible alone", TUNE),
            (r"chapter 9: \ the progressions they move through", GREY_A),
        ]
        rows_scene(self, r"voicings", items,
                   "Pianists build their voicings on these notes. <bookmark mark='b'/> Shell voicings, root, third and seventh, "
                   "as bebop pianists such as Bud Powell played them. <bookmark mark='c'/> Rootless voicings, third and seventh "
                   "with the ninth and thirteenth, leaving the root to the bass, as Bill Evans and others played them. "
                   "<bookmark mark='d'/> Comping with guide tones leaves room for the bass and the soloist, "
                   "<bookmark mark='e'/> and a soloist who lands on guide tones at the changes makes the harmony audible even "
                   "alone. <bookmark mark='f'/> Chapter nine turns to the progressions they move through.", marks="cdef")
