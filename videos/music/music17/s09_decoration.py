from __future__ import annotations

import numpy as np

from videos.music.music17.common import *  # noqa: F403


class Decoration(SoundScene):
    def construct(self):
        chapter(self, 8, r"Between the beats", r"What do the quick notes do?")
        self.counts()
        self.quiz()

    # ------------------------------------------------------------------
    def counts(self):
        d = load("decoration")
        pv = d["per_voice"]
        bars_ = VGroup()
        kinds = ("passing", "neighbour", "other")
        colors = (TUNE, EAR, WEAK)
        top = max(sum(pv[str(j)][k] for k in kinds) for j in range(4))
        for j in range(4):
            x0 = -5.8
            y = 1.3 - 0.85 * j
            name = label(VOICE_NAMES[j], font_size=24, color=VOICE_C[j]).move_to([x0 - 0.2, y, 0], aligned_edge=RIGHT)
            row = VGroup(name)
            x = x0
            for k, col in zip(kinds, colors):
                w = 7.0 * pv[str(j)][k] / top
                r = Rectangle(width=max(w, 0.02), height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([x + w / 2, y, 0])
                row.add(r)
                x += w
            row.add(label(f"{sum(pv[str(j)][k] for k in kinds):,}".replace(",", "{,}"), font_size=20, color=GREY_B).move_to([x + 0.6, y, 0]))
            bars_.add(row)
        bars_.shift(RIGHT * 1.0)
        key = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=col, fill_opacity=0.9), label(t, font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.15)
                       for t, col in zip((r"passing: \ step in, \ step on", r"neighbour: \ step out, \ step back", r"other: \ a leap or a chord note"), colors)]).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=1.2)
        head = label(r"notes that begin between the beats, \ by voice", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(rf"{100 * d['share']:.0f} beats in a hundred have a note moving inside them", font_size=26, color=TUNE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The chords sit on the beats; between them Bach writes quicker notes, mostly eighth notes. "
            "<bookmark mark='a'/> Count every note that begins between two beats, voice by voice, and sort "
            "it by how it moves. Most are passing notes, stepping from one chord note to the next, in "
            "one direction: Part 16's second species, now inside a chord progression. Then neighbours, "
            "a step away and back. The rest leap, usually from one note of the chord to another. "
            "<bookmark mark='b'/> The soprano, which carries the tune, has the fewest; the bass, "
            "surprisingly, has the most, walking between its chord roots. <bookmark mark='c'/> More than "
            "half of all beats have something moving inside them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in bars_], lag_ratio=0.3), FadeIn(key), run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(bars_[0][0]), Indicate(bars_[3][0]))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("decoration")
        c = clip("decoration.quiz")
        card = listen_card(r"The hook's two phrases, \ twice: \ once with only the chords on the beats, \ once as Bach wrote it. \ Which is Bach's: \ A or B?", width=10.0)
        with self.voiceover(
            "Hear what they do. The hook's two phrases, twice: once with only Bach's chords on the beats, "
            "each held for a beat, and once as he wrote them. Which is Bach's, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = choir_roll(d["block"], width=5.6, height=3.2, lo=38, hi=80, thick=0.11).move_to(LEFT * 3.3 + DOWN * 0.2)
        gB = choir_roll(d["full"], width=5.6, height=3.2, lo=38, hi=80, thick=0.11).move_to(RIGHT * 3.3 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", kind="synthesized", detail=r"a model choir", corner=DL, tag_corner=DR)
            sing_roll(snd, gA, d["times"]["A"], start=d["starts"]["A"])
            sing_roll(snd, gB, d["times"]["B"], start=d["starts"]["B"])
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(r"the same chords, \ blocks", font_size=24, color=GREY_A).next_to(gA, DOWN, buff=0.3),
                     label(r"Bach: \ the voices walk between them", font_size=24, color=TUNE).next_to(gB, DOWN, buff=0.3))
        with self.voiceover(
            "B is Bach's. A has exactly his chords, on exactly the same beats, and it sounds like a "
            "hymnbook played by someone in a hurry. The passing notes do not change the harmony; they "
            "turn four voices holding chords into four people singing lines. Any harmonizer that only "
            "chooses chords will sound like A."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
