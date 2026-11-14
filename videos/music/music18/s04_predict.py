from __future__ import annotations

import numpy as np

from videos.music.music18.common import *  # noqa: F403


class Predict(SoundScene):
    def construct(self):
        chapter(self, 3, r"How predictable is harmony?", r"How many bits does the next chord carry?")
        self.guess()
        self.bits()
        self.surprise()

    # ------------------------------------------------------------------
    def guess(self):
        d = load("predict")
        g = d["guesses"]
        pp = pause_card(r"A major chorale: \ I, \ then IV. \ What comes next?", width=8.0).to_edge(UP, buff=0.6)
        with self.voiceover(
            "A game first. A chorale in a major key plays its home chord, then four. What comes next? "
            "Make a guess before the answer."
        ):
            self.play(FadeIn(pp))
        self.wait(2.0)
        rows_ = VGroup()
        for k, (ctx, items) in enumerate(list(g.items())[:3]):
            ctx_t = label(rf"after {ctx.replace(' ', r' \ ')}:", font_size=26, color=GREY_A)
            bars_ = VGroup()
            for nm, p in items[:4]:
                r = Rectangle(width=max(6.0 * p, 0.05), height=0.32, stroke_width=0, fill_color=TUNE if nm == items[0][0] else WEAK, fill_opacity=0.9)
                t = label(rf"{nm} \ {100 * p:.0f}\%", font_size=20, color=WHITE)
                bars_.add(VGroup(r, t.next_to(r, RIGHT, buff=0.12)))
            bars_.arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            row = VGroup(ctx_t, bars_).arrange(RIGHT, buff=0.4, aligned_edge=UP)
            rows_.add(row)
        rows_.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.6)
        first = g["I IV"][0]
        with self.voiceover(
            f"The answer, from two hundred and eighty chorales: most often the home chord again, "
            f"{say(round(100 * first[1]))} times in a hundred; then five; then two, which leads to five. "
            "<bookmark mark='a'/> After two the field is open. After five, home: more than half the time. "
            "The next chord is never certain, but it is far from random."
        ) as vo:
            self.play(FadeOut(pp), FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows_[1]), FadeIn(rows_[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bits(self):
        d = load("predict")
        mj, mn = d["major"], d["minor"]
        keys = [("uniform", r"every chord \\ equally likely"), ("n1", r"how common \\ each chord is"), ("n2", r"the chord \\ before"), ("n3", r"the two \\ before")]
        vals = [mj[k] for k, _ in keys]
        ch = columns(vals, [t for _, t in keys], width=7.4, height=2.6, color=WEAK, hot=(2,), hot_color=TUNE, fmt="{:.1f}", font_size=22).move_to(LEFT * 2.2 + DOWN * 0.7)
        t = label(r"bits per chord, \ on 84 chorales whose tunes the model never saw \ (major)", font_size=22, color=GREY_A).next_to(ch, UP, buff=0.4)
        side = VGroup(label(rf"the same chords, \ shuffled: \ {mj['n2_shuffled']:.1f} bits", font_size=24, color=WHITE),
                      label(rf"minor keys: \ {mn['n2']:.1f} \ (shuffled \ {mn['n2_shuffled']:.1f})", font_size=24, color=WHITE),
                      label(r"two chords back helps less: \ too few chorales to learn it", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.2))
        side.move_to(RIGHT * 4.1 + DOWN * 0.3)
        with self.voiceover(
            "Information theory, as in Part 14, puts a number on it: the bits needed, on average, to say "
            f"which chord comes next. Bach's major chorales use about {say(mj['vocab'])} different chords. "
            f"<bookmark mark='a'/> If every one were equally likely, each would cost {say(mj['uniform'], 1)} bits. "
            f"Knowing only how common each chord is brings that to {say(mj['n1'], 1)}. Knowing the chord before "
            f"brings it to {say(mj['n2'], 1)}: that is the syntax, measured, on chorales whose tunes the model "
            "never saw. <bookmark mark='b'/> Shuffle the same chords into a random order and the cost rises to "
            f"{say(mj['n2_shuffled'], 1)}: the order carries more than a bit per chord. Two chords back helps "
            "less, not because it carries nothing but because two hundred and eighty chorales are too few to "
            "learn every triple. For comparison, Part 14's melodies cost two point six bits a note given the "
            "note before, from a vocabulary of about twenty notes."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(t))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def surprise(self):
        d = load("predict")
        after_v = d["guesses"]["V"]
        p_vi = next((p for nm, p in after_v if nm == "vi"), None)
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (rf"after V: \ I with probability {after_v[0][1]:.2f}, \ about {-np.log2(after_v[0][1]):.1f} bits", WHITE),
            (rf"after V: \ vi with probability {p_vi:.2f}, \ about {-np.log2(p_vi):.1f} bits: \ the deceptive cadence of Part 15", EAR),
            (r"a surprise is measured in bits, \ and composers place them", WHITE),
            (r"Meyer, \ 1956: \ emotion in music is expectation, \ delayed or denied", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"surprise, \ in bits", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Bits also measure surprise, chord by chord. <bookmark mark='a'/> After a dominant, the home chord comes "
            f"with probability {say(after_v[0][1], 2)}: hearing it carries only about one bit of news. "
            "<bookmark mark='b'/> The chord on six comes with probability "
            f"{say(p_vi, 2)}: about four bits. That is the deceptive cadence of Part 15, and it works because the "
            "syntax made the listener expect home. <bookmark mark='c'/> A composer who knows the probabilities can "
            "place a surprise where it will be felt. <bookmark mark='d'/> Leonard Meyer argued in 1956 that this is "
            "where much of the emotion in music comes from: an expectation set up, then delayed, or denied, or "
            "fulfilled at last."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

