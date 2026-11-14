from __future__ import annotations

import numpy as np

from videos.music.music19.common import *  # noqa: F403


class Sixths(SoundScene):
    def construct(self):
        chapter(self, 4, r"Augmented sixths", r"How can a chord aim at the dominant from both sides?")
        self.idea()
        self.three()
        self.fifths()

    # ------------------------------------------------------------------
    def idea(self):
        a = Dot([-4.9, -1.0, 0], radius=0.12, color=VOICE_C[3])
        b = Dot([-4.9, 1.3, 0], radius=0.12, color=VOICE_C[0])
        g1, g2 = Dot([-2.6, -1.35, 0], radius=0.12, color=VOICE_C[3]), Dot([-2.6, 1.65, 0], radius=0.12, color=VOICE_C[0])
        arrows = VGroup(Arrow(a.get_center(), g1.get_center(), buff=0.15, color=VOICE_C[3], stroke_width=5), Arrow(b.get_center(), g2.get_center(), buff=0.15, color=VOICE_C[0], stroke_width=5))
        tags = VGroup(label(tex(r"A♭"), font_size=30, color=VOICE_C[3]).next_to(a, LEFT, buff=0.2), label(tex(r"F♯"), font_size=30, color=VOICE_C[0]).next_to(b, LEFT, buff=0.2),
                      label(r"G", font_size=30, color=VOICE_C[3]).next_to(g1, RIGHT, buff=0.2), label(r"G", font_size=30, color=VOICE_C[0]).next_to(g2, RIGHT, buff=0.2))
        span1 = DoubleArrow([-4.5, -0.85, 0], [-4.5, 1.15, 0], buff=0, color=EAR, stroke_width=2.5, tip_length=0.15)
        span2 = DoubleArrow([-2.25, -1.2, 0], [-2.25, 1.5, 0], buff=0, color=TUNE, stroke_width=2.5, tip_length=0.15)
        interval = VGroup(label(r"augmented sixth", font_size=20, color=EAR).next_to(span1, DOWN, buff=0.55).shift(LEFT * 0.2),
                          label(r"octave", font_size=20, color=TUNE).next_to(span2, DOWN, buff=0.25))
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (tex(r"two notes, \ each a semitone from G: \ A♭ above it falls, \ F♯ below it rises"), WHITE),
            (r"the strongest approach to the dominant there is", WHITE),
            (tex(r"Italian: \ A♭ C F♯; \ French: \ add D; \ German: \ add E♭"), WHITE),
            (r"named by later theorists, \ not by Italians, \ Frenchmen or Germans", GREY_A))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 7.6))
        rows_.move_to(RIGHT * 2.4 + DOWN * 0.1)
        with self.voiceover(
            "Take G, the dominant of C minor, and the two notes that lean on it hardest: A flat, a semitone above, "
            "and F sharp, a semitone below, borrowed from outside the key. <bookmark mark='a'/> Put A flat in the bass and F sharp above it, and "
            "they make an augmented sixth, which opens outward, both voices moving by a semitone, to an octave on G. "
            "<bookmark mark='b'/> It is the strongest approach to the dominant there is: a pincer. <bookmark mark='c'/> "
            "Fill in the chord and it comes in three flavours, the Italian with C, the French with C and D, the German "
            "with C and E flat. <bookmark mark='d'/> The national names were given by later theorists, and mean nothing."
        ) as vo:
            self.play(FadeIn(a), FadeIn(b), FadeIn(tags[:2]), FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(FadeIn(span1), FadeIn(interval[0]))
            self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(g1), FadeIn(g2), FadeIn(tags[2:]), FadeIn(span2), FadeIn(interval[1]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three(self):
        d = load("sixths")
        c = clip("sixths.three")
        cells = VGroup()
        for name in ("Italian", "French", "German"):
            st = block_staff(d[name]["chords"], width=3.6, beats=2, key=-3)
            t = label(name, font_size=26, color=TUNE)
            cells.add(VGroup(t, st).arrange(DOWN, buff=0.3))
        cells.arrange(RIGHT, buff=0.5).move_to(DOWN * 0.1)
        cap = label(r"each: \ i, \ the augmented sixth, \ V", font_size=24, color=GREY_A).to_edge(DOWN, buff=1.3)
        with self.voiceover(
            "Here are all three in C minor, each between the home chord and the dominant. Listen to the outer voices "
            "spread apart onto the G's, and to the colour each flavour adds: the Italian bare, the French with a "
            "whole-tone ring, the German full and heavy."
        ):
            self.play(FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Italian, \ French, \ German", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            names = ("Italian", "French", "German")
            for k, name in enumerate(names):
                end = d[names[k + 1]]["start"] - 0.4 if k < 2 else c.duration
                pulse(snd, cells[k][0], d[name]["start"], end, buff=0.1)
        with self.voiceover(
            "The German sixth has a secret, which chapter six opens. Its four notes, A flat, C, E flat, F sharp, are "
            "on the piano exactly the notes of a dominant seventh chord, A flat, C, E flat, G flat. The same four keys "
            "can mean two different things."
        ):
            self.play(Indicate(cells[2][0], color=EAR))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fifths(self):
        t = load("trapdoor")
        st = block_staff(t["home"], width=5.6, beats=2, flats=True).move_to(LEFT * 3.7 + DOWN * 0.2)
        nm = VGroup(*[label(tex(n), font_size=21, color=EAR if n in ("Ger+6", "I6/4") else GREY_A) for n in t["home_names"]])
        for k, n in enumerate(nm):
            n.move_to([st.get_left()[0] + 1.0 + (st.width - 1.2) * (k + 0.5) / len(nm), st.get_bottom()[1] - 0.38, 0])
        rows_ = VGroup(*[label(t_, font_size=24, color=c_) for t_, c_ in (
            (r"German sixth straight to V: \ A$\flat$--E$\flat$ moves to G--D", WHITE),
            (r"parallel fifths, \ the fault of Part 16", WHITE),
            (r"the cure: \ a 6/4 chord between, \ E$\flat$ held as E$\natural$ or sliding to D later", WHITE),
            (r"or let them sound: \ `Mozart fifths', \ tolerated for this chord alone", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 5.8))
        rows_.move_to(RIGHT * 3.75 + DOWN * 0.1)
        with self.voiceover(
            "The German sixth has a practical problem. <bookmark mark='a'/> Resolve it straight to the dominant and its "
            "bass and its E flat, a perfect fifth apart, both fall a semitone, to G and D: <bookmark mark='b'/> "
            "parallel fifths, the fault Part 16 explained. <bookmark mark='c'/> The usual cure is the one on the "
            "staff: a six-four chord between, the home chord over the dominant's bass, so that E flat can move to E and "
            "the fifths disappear. <bookmark mark='d'/> Composers also simply let them sound, and textbooks call them "
            "Mozart fifths: the best-known parallel fifths that common practice tolerates, because the ear is busy with the "
            "two voices opening outward."
        ) as vo:
            self.play(FadeIn(st), FadeIn(nm))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
