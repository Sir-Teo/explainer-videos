from __future__ import annotations

import numpy as np

from videos.music.music20.common import *  # noqa: F403


ORD = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth"}


class Rounds(SoundScene):
    def construct(self):
        chapter(self, 1, r"Rounds", r"Why does a round work?", extra=((1250, r"\textit{Sumer is icumen in}"),))
        self.hear()
        self.why()
        self.census()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("rounds")
        c = clip("rounds.frere")
        g = voices_roll(d["lines"], width=11.6, height=3.4).move_to(DOWN * 0.3)
        tags = VGroup(*[label(rf"voice {k + 1}", font_size=20, color=VOICE_C[k]).next_to([g.x(d["lines"][k][0][1]), g.y(d["lines"][k][0][0]) + 0.3, 0], UP, buff=0.05) for k in range(3)])
        head = label(r"\textit{Frère Jacques} \ as a round: \ three voices, \ two bars apart", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The simplest way to combine a melody with itself is a round. One voice starts; when it reaches the end "
            "of the second bar, a second voice starts the same tune from the beginning; two bars later, a third. "
            "Here is Frère Jacques, in three voices, each an octave below the last so you can follow them."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(tags))
        with self.listen(c) as snd:
            window(snd, r"\textit{Frère Jacques}, \ a round in three", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_voices(snd, g, d["lines"], beat=0.4)
            self.add(cursor(snd, g, 0.0, beat=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"cut the tune into its two-bar pieces: \ A, \ B, \ C, \ D", WHITE),
            (r"a round sounds A over B over C, \ B over C over D, \ and so on", WHITE),
            (r"so every piece must agree with every other piece", WHITE),
            (r"the easy way: \ every piece outlines the same chord", TUNE),
            (r"\textit{Sumer is icumen in}, \ about 1250: \ six voices over one harmony", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"why a round works", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Why does it work? <bookmark mark='a'/> Cut the tune into its two-bar pieces. <bookmark mark='b'/> With "
            "three voices two bars apart, you hear the first piece against the second against the third, then the "
            "second against the third against the fourth. <bookmark mark='c'/> So every piece must sound well with "
            "every other. <bookmark mark='d'/> The easy way is for every piece to outline the same chord: Frère Jacques "
            "never leaves its home chord. <bookmark mark='e'/> The oldest round in English, Sumer is icumen in, written down "
            "in about 1250, does the same in six voices: the cuckoo sings over a harmony that barely moves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def census(self):
        d = load("rounds")
        top = d["census"][:8]
        ch = columns([100 * (1 - r["rate"]) for r in top], [tex(r["name"].split(" (")[0].replace("Row, Row, Row Your Boat", "Row, Row").replace("Three Blind Mice", "Blind Mice").replace("Go Tell Aunt Rhody", "Aunt Rhody").replace("London Bridge", "London Br.")) for r in top],
                     width=10.4, height=2.4, color=WEAK, hot=tuple(i for i, r in enumerate(top) if r["name"] in d["known_ranks"]), hot_color=TUNE, fmt="{:.0f}", font_size=17, top=100).move_to(DOWN * 0.5)
        t = label(rf"every tune of Part 14's {d['n_tunes']} sung against itself in three voices: \ strong beats that agree, \ in a hundred \ (best delay)", font_size=21, color=GREY_A).next_to(ch, UP, buff=0.4)
        k = d["known_ranks"]
        cap = label(rf"the three tunes known as rounds: \ places {k['Frère Jacques']}, \ {k['Row, Row, Row Your Boat']} \ and {k['Three Blind Mice']}", font_size=24, color=TUNE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Can a program find rounds? Take every tune in Part 14's collection, and sing each one against itself in "
            "three voices, trying every delay of a whole number of bars. On every strong beat, ask whether all the "
            "voices agree, thirds, fifths, sixths and octaves, and keep each tune's best delay. "
            f"<bookmark mark='a'/> The program was not told which tunes are rounds. Frère Jacques comes "
            f"{ORD[k['Frère Jacques']]}, Row, Row, Row Your Boat {ORD[k['Row, Row, Row Your Boat']]}, and Three Blind Mice "
            f"{ORD[k['Three Blind Mice']]}, "
            f"out of {say(d['n_tunes'])}. The fourth tune in the top four, Go Tell Aunt Rhody, simply has a harmony that "
            "never moves. A round is a melody that agrees with itself."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(t))
            vo.wait_until("a")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
