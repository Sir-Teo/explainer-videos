from __future__ import annotations

import numpy as np

from videos.music.music18.common import *  # noqa: F403

ORDER = ["fifth down", "third down", "step up", "fifth up", "third up", "step down", "same", "tritone"]


class RootMotion(SoundScene):
    def construct(self):
        chapter(self, 2, r"How roots move", r"Why falling fifths?", extra=((2000, r"Meeùs's root motions"),))
        self.count()
        self.quiz()
        self.why()

    # ------------------------------------------------------------------
    def count(self):
        d = load("motion")["major"]
        tot = sum(d.values())
        vals = [100 * d.get(k, 0) / tot for k in ORDER]
        ch = columns(vals, [k.replace(" ", r" \ ") for k in ORDER], width=10.4, height=2.8, color=WEAK, hot=(0, 1, 2), hot_color=TUNE, fmt="{:.0f}", font_size=20, top=40).move_to(DOWN * 0.6)
        t = label(r"from one chord's root to the next, \ in a hundred \ (Bach's major chorales, \ repeats left out)", font_size=22, color=GREY_A).next_to(ch, UP, buff=0.4)
        fw = sum(d.get(k, 0) for k in ORDER[:3])
        bw = sum(d.get(k, 0) for k in ORDER[3:6])
        cap = label(rf"falling fifths, \ falling thirds, \ rising steps: \ {100 * fw / (fw + bw):.0f} in a hundred of the moves that go anywhere", font_size=24, color=TUNE).to_edge(DOWN, buff=0.45)
        head = label(r"root motion", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Now forget the jobs and follow the roots. From each chord to the next, how far does the root "
            "move? <bookmark mark='a'/> The commonest move by far is a falling fifth: five to one, two to five, "
            f"six to two. It is {say(round(100 * d['fifth down'] / tot))} moves in a hundred. "
            "<bookmark mark='b'/> Then rising steps and falling thirds. Their inverses, the rising fifth, the "
            "rising third and the falling step, are all rarer. <bookmark mark='c'/> Nicolas Meeùs grouped them "
            "this way in 2000: falling fifths, falling thirds and rising steps carry harmony forward, the "
            f"others hold it back, and in Bach the forward kind is {say(round(100 * fw / (fw + bw)))} in a hundred."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(t))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("motion")
        c = clip("motion.quiz")
        card = listen_card(r"Four chords, \ twice. \ In one the roots fall by fifths, \ in the other they rise. \ Which one arrives home: \ A or B?", width=9.6)
        with self.voiceover(
            "Hear the difference. Four chords, twice. In one the roots fall by fifths; in the other the same kind "
            "of chords rise by fifths. Which one arrives home, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        sA = block_staff(d["A"], width=4.6).move_to(LEFT * 3.3 + DOWN * 0.1)
        sB = block_staff(d["B"], width=4.6).move_to(RIGHT * 3.3 + DOWN * 0.1)
        la = label(r"A", font_size=40, color=GREY_A).next_to(sA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(sB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(sA), FadeIn(sB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"a plucked string", corner=DL, tag_corner=DR)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(r"vi \ ii \ V \ I: \ A \ D \ G \ C, \ falling fifths", font_size=24, color=TUNE).next_to(sA, DOWN, buff=0.35),
                     label(r"I \ V \ ii \ vi: \ C \ G \ D \ A, \ rising fifths", font_size=24, color=GREY_A).next_to(sB, DOWN, buff=0.35))
        with self.voiceover(
            "A. Its roots fall A, D, G, C, and each chord leads into the next until the last one lands on home. B "
            "starts at home and climbs away, and its last chord, six, leaves the question open. The same four "
            "kinds of chord; the direction of the root decides whether the music arrives or departs."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        a = (72, 67, 64, 55)
        b = (72, 65, 60, 53)
        da = VGroup(*[Dot([-5.0, 0.12 * (p - 64), 0], radius=0.1, color=VOICE_C[j]) for j, p in enumerate((71, 67, 62, 43))])
        db = VGroup(*[Dot([-3.4, 0.12 * (p - 64), 0], radius=0.1, color=VOICE_C[j]) for j, p in enumerate((72, 67, 64, 48))])
        ar = VGroup(*[Line(x.get_center(), y.get_center(), buff=0.12, color=VOICE_C[j], stroke_width=3) for j, (x, y) in enumerate(zip(da, db))])
        tags = VGroup(label(r"G", font_size=24, color=GREY_A).next_to(da, DOWN, buff=0.3), label(r"C", font_size=24, color=GREY_A).next_to(db, DOWN, buff=0.3))
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"a falling fifth: \ the new root was a note of the old chord's harmonic series \ (the fifth above it)", WHITE),
            (r"one note held \ (G), \ the leading note up a semitone \ (B to C), \ the rest by step", WHITE),
            (r"Rameau, \ 1722: \ the fundamental bass moves by fifth, \ like a dominant to its tonic", GREY_A),
            (r"a cycle of falling fifths visits every chord of the key", TUNE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 8.8))
        rows_.move_to(RIGHT * 1.9 + DOWN * 0.1)
        with self.voiceover(
            "Why the falling fifth? Look at five going to one. <bookmark mark='a'/> The new root, C, lies a "
            "fifth below G, and G is the third harmonic of C: the old chord is already part of the new one's "
            "harmonic series, as if the music were falling home through its own overtones. "
            "<bookmark mark='b'/> And the voices move as Part 17 liked: G held, B up a semitone to C, D down a "
            "step. <bookmark mark='c'/> Rameau made the falling fifth the model of all harmony in 1722: the "
            "real bass of every progression, he said, wants to move like a dominant to its tonic. "
            "<bookmark mark='d'/> And a chain of falling fifths visits every chord of the key: chapter four "
            "hears one."
        ) as vo:
            self.play(FadeIn(da), FadeIn(db), Create(ar), FadeIn(tags))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
