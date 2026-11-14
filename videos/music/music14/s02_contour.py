from __future__ import annotations

import numpy as np

from videos.music.music14.common import *  # noqa: F403


class Contour(SoundScene):
    def construct(self):
        chapter(self, 1, r"The shape of a tune", r"What do you remember of a melody?", extra=((1972, r"Deutsch scrambles the octaves"),))
        self.quiz()
        self.shape()
        self.keys()
        self.codes()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("contour")
        c = clip("contour.disguises")
        ev = c.events
        o = d["original"]
        card = listen_card(r"One famous tune, \ disguised twice. \ In A, \ every note has the right name but the wrong octave. \ In B, \ every interval is wrong, \ "
                           r"but the notes go up and down as the tune does. \ Which can you name?", width=10.0)
        with self.voiceover(
            "Start with a puzzle for your ear. One famous tune, disguised twice. In A, every note has "
            "the right name, but is in the wrong octave. In B, every interval is wrong, but the notes go "
            "up and down as the tune does. Which one can you name?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        rA = roll(d["scrambled"], o["beats"], width=5.6, height=3.0, lines=(), color=CHANCE_C).move_to(LEFT * 3.3 + UP * 0.4)
        rB = roll(d["stretched"], o["beats"], width=5.6, height=3.0, lines=(), color=REAL_C).move_to(RIGHT * 3.3 + UP * 0.4)
        la = label(r"A: \ right notes, \ wrong octaves", font_size=26, color=GREY_A).next_to(rA, UP, buff=0.2)
        lb = label(r"B: \ wrong notes, \ right shape", font_size=26, color=GREY_A).next_to(rB, UP, buff=0.2)
        self.play(FadeOut(card), FadeIn(rA), FadeIn(rB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing(snd, rA, d["times"]["A"])
            sing(snd, rB, d["times"]["B"])
            pulse(snd, la, ev["A"], ev["B"] - 0.5, buff=0.1)
            pulse(snd, lb, ev["B"], c.duration, buff=0.1)
        c2 = clip("contour.real")
        rR = roll(o["pitches"], o["beats"], width=7.0, height=1.5, lines=(0,), color=TUNE).to_edge(DOWN, buff=1.25)
        lr = label(r"Fr\`ere Jacques", font_size=30, color=TUNE).next_to(rR, UP, buff=0.15)
        with self.voiceover("Most people cannot name A, and can name B. It is Frère Jacques."):
            self.play(rA.animate.scale(0.75).shift(UP * 0.6), rB.animate.scale(0.75).shift(UP * 0.6), la.animate.shift(UP * 0.25), lb.animate.shift(UP * 0.25), FadeIn(rR), FadeIn(lr))
        with self.listen(c2) as snd:
            window(snd, r"undisguised", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing(snd, rR, d["times"]["real"], hot=WHITE)
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shape(self):
        d = load("contour")
        o = d["original"]
        r = roll(o["pitches"], o["beats"], width=9.0, height=2.0, lines=(0,), color=TUNE).move_to(UP * 1.6)
        signs = [int(np.sign(b - a)) for a, b in zip(o["pitches"], o["pitches"][1:])]
        marks = VGroup(*[label({1: r"$\nearrow$", -1: r"$\searrow$", 0: r"$\rightarrow$"}[s], font_size=30, color=EAR).move_to([(r.notes[k].get_center()[0] + r.notes[k + 1].get_center()[0]) / 2, r.get_bottom()[1] - 0.35, 0])
                         for k, s in enumerate(signs)])
        layers = VGroup(label(r"1. \ contour: \ up, \ down, \ the same", font_size=30, color=EAR), label(r"2. \ intervals, \ in a scale", font_size=30, color=TUNE),
                        label(r"3. \ rhythm \ (Part 11)", font_size=30, color=GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "In A, every note had the right name. Only the octaves were scrambled, and that destroyed "
            f"the ups and downs: just {say(d['scrambled_kept'])} of the thirteen moves kept their "
            "direction. In B, every interval was doubled, so not one of them was right; but the shape "
            "was. <bookmark mark='a'/> Diana Deutsch did the first experiment of this kind in 1972, and "
            "Jay Dowling showed soon after that contour is what listeners keep first: the pattern of "
            "ups and downs. Exact intervals come later, with familiarity."
        ) as vo:
            self.play(FadeIn(r))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.1), run_time=2.5)
        with self.voiceover(
            "So a melody is not a list of notes. It is first of all a shape in time. <bookmark mark='a'/> "
            "Then, hung on that shape, exact intervals in a scale. <bookmark mark='b'/> And then rhythm, "
            "which Part 11 took apart. This part is about the shape: what shapes melodies have, and why "
            "they have them."
        ) as vo:
            self.play(FadeIn(layers[0]))
            vo.wait_until("a")
            self.play(FadeIn(layers[1]))
            vo.wait_until("b")
            self.play(FadeIn(layers[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def keys(self):
        d = load("more")["keys"]
        c = clip("contour.keys")
        ev = c.events
        r1 = roll(d["pitches"], d["beats"], width=5.2, height=2.6, lo=-1, hi=16, lines=(), color=TUNE).move_to(LEFT * 3.3 + UP * 0.4)
        r2 = roll([p + 6 for p in d["pitches"]], d["beats"], width=5.2, height=2.6, lo=-1, hi=16, lines=(), color=BLUE).move_to(RIGHT * 3.3 + UP * 0.4)
        l1 = label(r"on C: \ C, \ G, \ A", font_size=26, color=TUNE).next_to(r1, UP, buff=0.2)
        l2 = label(r"on F$\sharp$: \ F$\sharp$, \ C$\sharp$, \ D$\sharp$", font_size=26, color=BLUE).next_to(r2, UP, buff=0.2)
        with self.voiceover(
            "There is a fact about melody so familiar that it is easy to miss. Here is the Tune's first "
            "phrase starting on C; and then starting on F sharp."
        ):
            self.play(FadeIn(r1), FadeIn(l1), FadeIn(r2), FadeIn(l2))
        with self.listen(c) as snd:
            window(snd, r"one phrase, \ two keys", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing(snd, r1, d["times"]["C"], hot=WHITE, base=TUNE)
            sing(snd, r2, d["times"]["Fs"], hot=WHITE, base=BLUE)
            pulse(snd, l1, ev["C"], ev["Fs"] - 0.5, buff=0.1)
            pulse(snd, l2, ev["Fs"], c.duration, buff=0.1)
        cap = VGroup(label(r"not one note in common; \ the same tune.", font_size=32, color=TUNE), label(r"a melody is a pattern of relations between notes, \ not the notes", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The two versions do not have a single note in common, and nobody hears two tunes. A child "
            "can sing a song back in a different key without noticing. So a melody is not its notes. It "
            "is a pattern of relations between notes: the same shape, with the same intervals, wherever "
            "it is put. Very few people can name a note they hear; nearly everyone can recognise a tune."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def codes(self):
        d = load("more")["parsons"]
        code = d["tune_code"]
        cells = VGroup(*[label(ch, font_size=40, color={"U": TUNE, "D": BLUE, "R": GREY_A}[ch]) for ch in code]).arrange(RIGHT, buff=0.25).move_to(UP * 2.0)
        cl = label(r"the Tune, \ as ups, \ downs and repeats", font_size=24, color=GREY_B).next_to(cells, UP, buff=0.25)
        ns = d["n"][:9]
        ch1 = columns(d["contour"][:9], [str(n) for n in ns], width=7.5, height=2.2, color=TUNE, fmt="{:.0f}", font_size=22, top=d["of"]).move_to(DOWN * 1.3)
        xl = label(rf"moves of contour known \quad (bars: \ how many of the {d['of']} tunes are then unlike every other)", font_size=22, color=GREY_B).next_to(ch1, DOWN, buff=0.15)
        k = next(i for i, v in enumerate(d["contour"]) if v == d["of"])
        with self.voiceover(
            "How much does contour alone tell you? Write a tune as nothing but ups, downs and repeats. "
            "<bookmark mark='a'/> In 1975 Denys Parsons published a directory of thousands of themes "
            "indexed this way, so that you could look up a tune you could only hum. Try it on our "
            f"library. <bookmark mark='b'/> With five moves of contour, {say(d['contour'][3])} of the "
            f"{say(d['of'])} tunes are already unlike every other. With {say(d['n'][k])}, all of them "
            "are. Three symbols, a handful of moves, and a tune is identified. Every system that finds a "
            "song from a hummed fragment begins here."
        ) as vo:
            self.play(FadeIn(cl), LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(ch1[0]), FadeIn(xl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(ch1.bars[i], ch1.labels[i], ch1.values[i])) for i in range(9)], lag_ratio=0.3), run_time=4.0)
        self.wait(0.4)
        self.clear_scene()
