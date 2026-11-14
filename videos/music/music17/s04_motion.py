from __future__ import annotations

import numpy as np

from videos.music.music17.common import *  # noqa: F403


class Motion(SoundScene):
    def construct(self):
        chapter(self, 3, r"Every voice a line", r"How does each voice move from chord to chord?")
        self.steps()
        self.alto()
        self.shortest()

    # ------------------------------------------------------------------
    def steps(self):
        st = load("motion")["stats"]
        c1 = columns([s["mean"] for s in st], [VOICE_NAMES[j] for j in range(4)], width=5.0, height=2.6, color=WEAK, hot=(3,), hot_color=VOICE_C[3], fmt="{:.1f}", font_size=24, top=4).move_to(LEFT * 3.4 + DOWN * 0.6)
        c2 = columns([100 * s["step"] for s in st], [VOICE_NAMES[j] for j in range(4)], width=5.0, height=2.6, color=WEAK, hot=(1,), hot_color=VOICE_C[1], fmt="{:.0f}", font_size=24, top=100).move_to(RIGHT * 3.4 + DOWN * 0.6)
        t1 = label(r"average move, \ in semitones", font_size=24, color=GREY_A).next_to(c1, UP, buff=0.35)
        t2 = label(r"moves of a step or less, \ in a hundred", font_size=24, color=GREY_A).next_to(c2, UP, buff=0.35)
        head = label(r"84{,}737 notes: \ how each voice moves to its next note", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Now follow each voice from one note to the next. <bookmark mark='a'/> The soprano, alto and "
            f"tenor move by about two semitones on average, a step; the bass by about "
            f"{say(st[3]['mean'], 1)}. <bookmark mark='b'/> Eight moves in ten in each upper voice are a "
            f"step or less, and the alto repeats its note more often than any other voice, "
            f"{say(round(100 * st[1]['repeat']))} times in a hundred. The bass is the one voice that "
            f"leaps: it jumps more than a fifth {say(100 * st[3]['leap'], 1)} times in a hundred, the "
            "inner voices almost never. Part 14 found steps in melodies; here every voice is a melody, "
            "and the inner ones are the most careful of all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(c1), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(c2), FadeIn(t2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def alto(self):
        d = load("motion")
        c = clip("motion.alto")
        ga = choir_roll(d["alto"], which=(1,), width=10.0, height=1.6, lo=60, hi=74, thick=0.12).move_to(UP * 1.2)
        gs = choir_roll(d["alto"], which=(0, 1), width=10.0, height=2.2, lo=60, hi=80, thick=0.12).move_to(DOWN * 1.7)
        la = label(r"the alto alone", font_size=24, color=VOICE_C[1]).next_to(ga, UP, buff=0.2)
        ls = label(r"with the soprano", font_size=24, color=GREY_A).next_to(gs, UP, buff=0.2)
        with self.voiceover(
            "Here is the alto of the hook's two phrases, alone, and then with the tune above it. Alone it "
            "is a modest melody of its own: small steps, a few held notes, a shape. It was written to be "
            "sung, by one person, from beginning to end."
        ):
            self.play(FadeIn(ga), FadeIn(la), FadeIn(gs), FadeIn(ls))
        with self.listen(c) as snd:
            window(snd, r"the alto, \ then with the soprano", kind="synthesized", detail=r"a model choir", corner=DL, tag_corner=DR)
            sing_roll(snd, ga, d["times"]["alto"], start=d["starts"]["alto"])
            sing_roll(snd, gs, d["times"]["with"], start=d["starts"]["with"])
            pulse(snd, la, d["starts"]["alto"], d["starts"]["with"] - 0.5, buff=0.1)
            pulse(snd, ls, d["starts"]["with"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shortest(self):
        s = load("motion")["shortest"]
        a = (72, 67, 64, 48)
        b = (71, 67, 62, 43)
        da = VGroup(*[Dot([-5.8, 0.11 * (p - 58), 0], radius=0.1, color=VOICE_C[j]) for j, p in enumerate(a)])
        db = VGroup(*[Dot([-4.3, 0.11 * (p - 58), 0], radius=0.1, color=VOICE_C[j]) for j, p in enumerate(b)])
        arrows = VGroup(*[Line(x.get_center(), y.get_center(), buff=0.12, color=VOICE_C[j], stroke_width=3) for j, (x, y) in enumerate(zip(da, db))])
        tag = VGroup(label(r"C major", font_size=22, color=GREY_A).next_to(da, DOWN, buff=0.3), label(r"G major", font_size=22, color=GREY_A).next_to(db, DOWN, buff=0.3))
        txt = VGroup(label(r"keep the common note; \ move the others to the nearest note of the next chord", font_size=26, color=WHITE),
                     label(r"`the law of the shortest way' \ (Bruckner's teaching, \ after Sechter)", font_size=22, color=GREY_B),
                     label(rf"Bach's alto and tenor: \ {s['actual']:.1f} semitones a beat; \ the least possible: \ {s['least']:.1f}", font_size=26, color=WHITE),
                     label(rf"the least possible exactly, \ {100 * s['same']:.0f} times in a hundred; \ within two semitones of it, \ {100 * s['within2']:.0f}", font_size=26, color=TUNE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 2.0 + DOWN * 0.1)
        txt.scale_to_fit_width(min(txt.width, 8.6))
        txt.move_to(RIGHT * 1.85 + DOWN * 0.1)
        with self.voiceover(
            "How do the inner voices choose their notes? The old rule is to keep a note the two chords "
            "share, and move every other voice to the nearest note of the next chord. From C major to G "
            "major, the G stays, and C and E each fall a step. <bookmark mark='a'/> Teachers in Vienna "
            "called it the law of the shortest way. <bookmark mark='b'/> Measure it in Bach. Given his "
            "next chord, with its soprano and bass fixed, find the least motion the alto and tenor could "
            f"make, and compare it with what they do. On average Bach's inner voices move "
            f"{say(s['actual'], 1)} semitones a beat, against {say(s['least'], 1)} at the least. "
            f"<bookmark mark='c'/> He takes the very shortest way {say(round(100 * s['same']))} times in a "
            f"hundred, and {say(round(10 * s['within2']))} times in ten stays within two semitones of it. The exceptions are the "
            "interesting part: an inner voice that moves further to make a better line of its own, or to "
            "avoid a fault with another voice."
        ) as vo:
            self.play(FadeIn(da), FadeIn(db), Create(arrows), FadeIn(tag), FadeIn(txt[0]))
            vo.wait_until("a")
            self.play(FadeIn(txt[1]))
            vo.wait_until("b")
            self.play(FadeIn(txt[2]))
            vo.wait_until("c")
            self.play(FadeIn(txt[3]))
        self.wait(0.4)
        self.clear_scene()
