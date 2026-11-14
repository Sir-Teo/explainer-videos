from __future__ import annotations

import numpy as np

from videos.music.music14.common import *  # noqa: F403


class Motive(SoundScene):
    def construct(self):
        chapter(self, 7, r"Saying it twice", r"Why do tunes repeat themselves?")
        self.sequence()
        self.counts()
        self.form()

    # ------------------------------------------------------------------
    def sequence(self):
        d = load("motive")
        c = clip("motive.sequence")
        ev = c.events
        k, j = d["kuckuck"], d["joy"]
        rk = roll(k["pitches"], k["beats"], width=5.4, height=2.2, lines=(), phrase_ends=k["phrase_ends"], color=TUNE).move_to(LEFT * 3.4 + UP * 0.5)
        rj = roll(j["pitches"], j["beats"], width=5.8, height=2.2, lines=(), phrase_ends=j["phrase_ends"], color=TUNE).move_to(RIGHT * 3.3 + UP * 0.5)
        ek, ej = k["phrase_ends"][0], j["phrase_ends"][0]
        for n in rk.notes[ek:]:
            n.set_fill(BLUE)
        for n in rj.notes[ej:]:
            n.set_fill(BLUE)
        lk = label(r"Kuckuck, \ Kuckuck \ (Germany)", font_size=24, color=GREY_A).next_to(rk, UP, buff=0.2)
        lj = label(r"Joy to the World", font_size=24, color=GREY_A).next_to(rj, UP, buff=0.2)
        with self.voiceover(
            "A melody that never repeated itself would be impossible to remember. Listen to how these "
            "two tunes are built: a short pattern, and then the same pattern again, one step higher or "
            "one step lower. Musicians call that a sequence."
        ):
            self.play(FadeIn(rk), FadeIn(lk), FadeIn(rj), FadeIn(lj))
        with self.listen(c) as snd:
            window(snd, r"a pattern, \ and again", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing(snd, rk, d["times"]["kuckuck"], hot=WHITE, base=TUNE)
            sing(snd, rj, d["times"]["joy"], hot=WHITE, base=TUNE)
            pulse(snd, lk, ev["kuckuck"], ev["joy"] - 0.5, buff=0.1)
            pulse(snd, lj, ev["joy"], c.duration, buff=0.1)
        for n in rk.notes[ek:]:
            n.set_fill(BLUE)
        for n in rj.notes[ej:]:
            n.set_fill(BLUE)
        cap = VGroup(label(r"the same shape, \ one step up", font_size=26, color=BLUE).next_to(rk, DOWN, buff=0.3), label(r"the same shape, \ one step down", font_size=26, color=BLUE).next_to(rj, DOWN, buff=0.3))
        with self.voiceover(
            "In the first, six notes, and then the same six a step up. In the second, a longer pattern, "
            "and then the same pattern a step down. The second time you hear the shape, you already know it; "
            "only the level is new."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counts(self):
        d = load("motive")
        dm = dots_matrix(d["matrix"], size=4.4, color=TUNE, breaks=d["matrix_ends"]).move_to(LEFT * 3.7 + DOWN * 0.5)
        ml = label(r"Fr\`ere Jacques against itself, \ note by note", font_size=22, color=GREY_B).next_to(dm, UP, buff=0.15)
        facts = VGroup(label(rf"{d['phrases_repeated']} of {d['phrases']} phrases repeat an earlier phrase exactly", font_size=28, color=WHITE),
                       label(rf"{d['moved']} tunes contain a sequence", font_size=28, color=WHITE),
                       label(rf"{d['exact']} repeat a short pattern at once", font_size=28, color=WHITE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 3.0 + UP * 1.0)
        cap = VGroup(label(r"say a sentence twice, \ and it is odd.", font_size=28, color=GREY_A), label(r"play a phrase twice, \ and it is music.", font_size=30, color=TUNE)).arrange(DOWN, buff=0.15).move_to(RIGHT * 3.0 + DOWN * 1.6)
        head = label(r"repetition in the fifty-four tunes", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Repetition is everywhere in the fifty-four. <bookmark mark='a'/> "
            f"{say(d['phrases_repeated'])} of the {say(d['phrases'])} phrases are exact repeats of an "
            f"earlier phrase: more than one in five. {say(d['moved'])} of the tunes contain a sequence, "
            f"and {say(d['exact'])} repeat a short pattern immediately. <bookmark mark='b'/> Here is "
            "Frère Jacques compared with itself, note against note, with a dot wherever two moments "
            "match. The stripes beside the main diagonal are repeats: every phrase of this tune is "
            "sung twice."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.8), run_time=6.0)
            vo.wait_until("b")
            self.play(FadeIn(dm), FadeIn(ml))
        with self.voiceover(
            "The psychologist Elizabeth Margulis has argued that this is what most separates music "
            "from speech. Say a sentence twice, and it is odd. Play a phrase twice, and it is music. A "
            "motive is the smallest thing in a tune that can be said twice; and chance, which explained "
            "the leap rule, does not repeat itself."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def form(self):
        d = load("more")["form"]
        short = {"Ah! vous dirai-je, maman (the Tune)": r"the Tune", "Frère Jacques": r"Fr\`ere Jacques", "Au clair de la lune": r"Au clair de la lune",
                 "Lightly Row (Hänschen klein)": r"Lightly Row", "Good King Wenceslas": r"Good King Wenceslas"}
        cols = {"A": TUNE, "B": BLUE, "C": EAR, "D": "#A3E635", "E": "#C4B5FD", "F": "#FB923C"}
        rows = VGroup()
        for name, lab in short.items():
            cells = VGroup(*[VGroup(RoundedRectangle(width=0.62, height=0.62, corner_radius=0.1, stroke_width=0, fill_color=cols[ch], fill_opacity=0.85), label(ch, font_size=28, color=BLACK)) for ch in d[name]]).arrange(RIGHT, buff=0.1)
            for cell in cells:
                cell[1].move_to(cell[0])
            rows.add(VGroup(label(lab, font_size=26, color=GREY_A), cells))
        for r in rows:
            r[0].move_to([-5.6, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-1.6, 0, 0], aligned_edge=LEFT)
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.3)
        head = label(r"each phrase a letter; \ a phrase heard before keeps its letter", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Give each phrase of a tune a letter, and give a phrase you have heard before the letter it "
            "had. <bookmark mark='a'/> The Tune is A, B, C, C, A, B: it goes out, and it comes back. "
            "<bookmark mark='b'/> Frère Jacques says everything twice: A, A, B, B, C, C, D, D; which is "
            "why it works as a round. <bookmark mark='c'/> Au clair de la lune is A, B, A, B, then "
            "something new, then A, B again. Statement, departure, return. With a handful of letters "
            "you have the plan of a tune, and in Part 21 the same letters will describe a symphony."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(r[0]) for r in rows])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in rows[0][1]], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in rows[1][1]], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in rows[2][1]], lag_ratio=0.2), run_time=3.0)
            self.play(FadeIn(rows[3][1]), FadeIn(rows[4][1]))
        self.wait(0.4)
        self.clear_scene()
