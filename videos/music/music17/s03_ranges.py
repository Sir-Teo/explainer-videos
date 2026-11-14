from __future__ import annotations

import numpy as np

from videos.music.music17.common import *  # noqa: F403


class Ranges(SoundScene):
    def construct(self):
        chapter(self, 2, r"Four ranges", r"Where does each voice sing, \ and how far apart?")
        self.ranges()
        self.spacing()
        self.doubling()

    # ------------------------------------------------------------------
    def ranges(self):
        d = load("ranges")
        lo0 = d["hist_lo"]
        g = axes([36, 82], [0, 1.05], x_length=11.0, y_length=3.6, xlabel=r"key number \ (60 is middle C)", xticks=[40, 48, 55, 60, 67, 72, 79], font_size=20).move_to(DOWN * 0.5)
        curves, brackets = VGroup(), VGroup()
        for j in range(4):
            h = np.array(d["hist"][j], dtype=float)
            h = np.convolve(h, np.array([1.0, 2.0, 3.0, 2.0, 1.0]) / 9.0, mode="same")          # smoothed over neighbouring keys
            h = h / h.max()
            xs = np.arange(len(h)) + lo0
            pts = [g.ax.c2p(x, y) for x, y in zip(xs, h)]
            poly = VMobject(stroke_color=VOICE_C[j], stroke_width=3).set_points_as_corners(pts)
            curves.add(poly)
            lo, hi = d["textbook"][j]
            br = VGroup(Line(g.ax.c2p(lo, 1.0) + UP * (0.55 + 0.17 * j), g.ax.c2p(hi, 1.0) + UP * (0.55 + 0.17 * j), color=VOICE_C[j], stroke_width=4))
            brackets.add(br)
        names = VGroup(*[label(VOICE_NAMES[j], font_size=26, color=VOICE_C[j]).move_to(g.ax.c2p(d["ranges"][j][4], 1.0) + UP * 0.25) for j in range(4)])
        key = label(r"bars above: \ the ranges a textbook gives \ (C4--A5, \ G3--D5, \ C3--A4, \ E2--D4)", font_size=20, color=GREY_B).next_to(g, UP, buff=1.35)
        out = d["outside"]
        with self.voiceover(
            "First, where each voice sings. Here is how often each key is used by each of the four "
            "voices across all the chorales: soprano, alto, tenor, bass, from the top. <bookmark mark='a'/> "
            "Above them are the ranges a harmony textbook gives. Bach stays inside them almost "
            f"completely: fewer than one soprano note in ten thousand falls outside, and "
            f"{say(100 * out[3], 1)} bass notes in a hundred, most of them a low D. "
            "<bookmark mark='b'/> Each range is about an octave and a half, and neighbouring ranges "
            "overlap by about an octave, so the voices can cross, though they rarely do."
        ) as vo:
            self.play(FadeIn(g), Create(curves), FadeIn(names), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(brackets), FadeIn(key))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spacing(self):
        d = load("ranges")
        gm, go = d["gap_mean"], d["gap_over_octave"]
        ch = (72, 67, 64, 48)
        chord = VGroup(*[Dot([0, 0.13 * (p - 60), 0], radius=0.11, color=VOICE_C[j]) for j, p in enumerate(ch)]).move_to(LEFT * 5.6 + DOWN * 0.2)
        gaps = VGroup()
        for k, (a, b) in enumerate(((0, 1), (1, 2), (2, 3))):
            br = BraceBetweenPoints(chord[a].get_center() + RIGHT * 0.3, chord[b].get_center() + RIGHT * 0.3, direction=RIGHT, color=GREY_B)
            gaps.add(br)
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (rf"soprano to alto: \ {gm['S-A']:.1f} semitones on average; \ more than an octave {100 * go['S-A']:.1f} times in a hundred", WHITE),
            (rf"alto to tenor: \ {gm['A-T']:.1f}; \ more than an octave {100 * go['A-T']:.1f} times in a hundred", WHITE),
            (rf"tenor to bass: \ {gm['T-B']:.1f}; \ more than an octave {100 * go['T-B']:.0f} times in a hundred", WHITE),
            (r"the rule: \ the upper three close together, \ the bass free", TUNE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 1.0 + DOWN * 0.1)
        rows_.scale_to_fit_width(min(rows_.width, 9.6))
        rows_.move_to(RIGHT * 1.3 + DOWN * 0.1)
        head = label(r"spacing: \ the gaps between neighbouring voices", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Next, the gaps between neighbouring voices. <bookmark mark='a'/> On average the soprano is "
            f"about {say(round(gm['S-A']))} semitones above the alto, the alto about {say(round(gm['A-T']))} "
            f"above the tenor, and almost never more than an octave. <bookmark mark='b'/> The bass is "
            f"further away, nearly {say(round(gm['T-B']))} semitones on average, and a fifth of the time "
            "more than an octave below the tenor. <bookmark mark='c'/> That is the textbook rule of "
            "spacing, and Part 5 gave the reason for it: wide intervals sound smooth low down, close "
            "ones only higher up. So the chord is built like the harmonic series, open at the bottom "
            "and close at the top."
        ) as vo:
            self.play(FadeIn(head), FadeIn(chord))
            for mark, k in zip("ab", (0, 2)):
                vo.wait_until(mark)
                if k == 0:
                    self.play(FadeIn(gaps[0]), FadeIn(gaps[1]), FadeIn(rows_[0]), FadeIn(rows_[1]))
                else:
                    self.play(FadeIn(gaps[2]), FadeIn(rows_[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def doubling(self):
        d = load("ranges")["doubling"]
        root = [d.get(f"0:{k}", 0) for k in ("root", "third", "fifth")]
        first = [d.get(f"1:{k}", 0) for k in ("root", "third", "fifth")]
        tr, tf = sum(root), sum(first)
        c1 = columns([100 * x / tr for x in root], [r"root", r"third", r"fifth"], width=4.6, height=2.6, color=WEAK, hot=(0,), hot_color=TUNE, fmt="{:.0f}", font_size=24, top=100).move_to(LEFT * 3.4 + DOWN * 0.6)
        c2 = columns([100 * x / tf for x in first], [r"root", r"third", r"fifth"], width=4.6, height=2.6, color=WEAK, hot=(), hot_color=TUNE, fmt="{:.0f}", font_size=24, top=100).move_to(RIGHT * 3.4 + DOWN * 0.6)
        t1 = label(r"root position: \ which note is doubled", font_size=24, color=GREY_A).next_to(c1, UP, buff=0.35)
        t2 = label(r"first inversion (third in the bass)", font_size=24, color=GREY_A).next_to(c2, UP, buff=0.35)
        head = label(r"four voices, \ three notes: \ one note sung twice", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Four voices and a triad of three notes: one note must be sung twice. Which? <bookmark mark='a'/> "
            f"When the root is in the bass, Bach doubles the root {say(round(100 * root[0] / tr))} times in a "
            f"hundred. The doubled root is the most stable choice: it reinforces the note that, in Part "
            f"13's root model, the whole chord points to. <bookmark mark='b'/> With the third in the bass, "
            "the choice is spread almost evenly: root, third and fifth each about a third of the time. "
            "There the bass already has the third, and the voices double whatever lets them move "
            "smoothly. The textbook's rule, double the root, is a description of the first case, and "
            "only a preference in the second."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(c1), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(c2), FadeIn(t2))
        self.wait(0.4)
        self.clear_scene()
