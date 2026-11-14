from __future__ import annotations

import numpy as np

from videos.music.music14.common import *  # noqa: F403


class Info(SoundScene):
    def construct(self):
        chapter(self, 9, r"How much news is in a note?", r"How predictable is a melody?", extra=((1948, r"Shannon's theory of information"),))
        self.bits()
        self.guess()
        self.zipf()

    # ------------------------------------------------------------------
    def bits(self):
        d = load("info")
        vals = [d["uniform"]] + d["by_order"][:4]
        names = [r"any note", r"common notes", r"1 note back", r"2 back", r"3 back"]
        ch = columns(vals, names, width=9.5, height=2.7, color=WEAK, hot=(2,), hot_color=TUNE, fmt="{:.1f}", font_size=22, top=4.6).move_to(DOWN * 1.1)
        yl = label(r"bits per note, \ on tunes the model has not seen", font_size=22, color=GREY_B).next_to(ch, DOWN, buff=0.15)
        head = label(rf"{d['alphabet']} different notes: \ $\log_2 {d['alphabet']} = {d['uniform']:.1f}$ bits each, \ if nothing is known", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        saved = 1 - d["by_order"][1] / d["uniform"]
        with self.voiceover(
            "We can put a number on all of this. Claude Shannon's measure of information, from 1948, "
            "is the bit: the answer to one yes-or-no question. Our tunes use "
            f"{say(d['alphabet'])} different notes. If every note were as likely as every other, each "
            f"would carry {say(d['uniform'], 1)} bits. <bookmark mark='a'/> But they are not equally "
            f"likely. Knowing only which notes are common brings it down to {say(d['by_order'][0], 1)}. "
            f"<bookmark mark='b'/> Knowing the previous note as well: {say(d['by_order'][1], 1)} bits. "
            f"So about {say(round(100 * saved, -1))} percent of every "
            "note is no news at all: it could have been predicted from the scale and the note before."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch[0]), FadeIn(ch.bars[0]), FadeIn(ch.labels[0]), FadeIn(ch.values[0]), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(ch.bars[1]), FadeIn(ch.labels[1]), FadeIn(ch.values[1]))
            vo.wait_until("b")
            self.play(FadeIn(ch.bars[2]), FadeIn(ch.labels[2]), FadeIn(ch.values[2]))
        with self.voiceover(
            "Look further back, two notes, three, and on this small library it gets no better. The "
            "model begins to memorise particular tunes, when what it needs is habits that all tunes "
            "share. With thousands of melodies to learn from, longer memories do pay; with fifty-four, "
            "one note of memory is the best we can use."
        ):
            self.play(*[FadeIn(VGroup(ch.bars[k], ch.labels[k], ch.values[k])) for k in (3, 4)])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zipf(self):
        z = load("info")["zipf"]
        rank, freq = np.array(z["rank"], dtype=float), np.array(z["frequency"], dtype=float)
        g = axes([0, 2.2], [0, 2.4], x_length=6.0, y_length=3.6, xlabel=r"rank of the pattern \ (1 is the commonest)", ylabel=r"how often it occurs", xticks=[0, 1, 2], yticks=[0, 1, 2],
                 xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}", font_size=20).move_to(LEFT * 3.2 + DOWN * 0.5)
        pts = VGroup(*[Dot(g.ax.c2p(np.log10(r), np.log10(f)), radius=0.035, color=TUNE) for r, f in zip(rank, freq)])
        xs = np.array([0.0, 2.1])
        fit = Line(g.ax.c2p(xs[0], np.log10(freq[0]) + 0.08), g.ax.c2p(xs[1], np.log10(freq[0]) + 0.08 + z["slope"] * xs[1]), color=EAR, stroke_width=3)
        words = {(0, 0): r"same, \ same", (-2, -2): r"down a tone, \ down a tone", (0, -2): r"same, \ down a tone", (2, 2): r"up a tone, \ up a tone", (0, 2): r"same, \ up a tone"}
        tops = VGroup(*[label(rf"{k + 1}. \ {words.get(tuple(p), str(p))}: \ {n}", font_size=24, color=WHITE) for k, (p, n) in enumerate(z["top"][:4])]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(RIGHT * 3.4 + UP * 0.9)
        slope = label(rf"slope \ ${z['slope']:.1f}$", font_size=28, color=EAR).move_to(RIGHT * 3.4 + DOWN * 1.2)
        head = label(rf"every pattern of two moves in a row: \ {z['kinds']} kinds, \ {z['total']:,} in all".replace(",", "{,}"), font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "One more regularity. Count every pattern of two moves in a row, and rank the patterns from "
            "the commonest to the rarest. <bookmark mark='a'/> A few patterns do most of the work: the "
            "same note three times; two steps down. Most patterns are rare. <bookmark mark='b'/> On "
            "logarithmic axes, the ranks fall close to a straight line, with a slope of about "
            f"minus {say(abs(z['slope']), 1)}. The frequencies of words in a language fall on such a "
            "line too; it is called Zipf's law. Melodies, like languages, are made from a small common "
            "vocabulary and a long tail of rarities."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(pts), LaggedStart(*[FadeIn(t) for t in tops], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(slope))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def guess(self):
        d = load("more")["guess"]
        big = VGroup(VGroup(label(r"right first time", font_size=26, color=GREY_A), label(rf"{100 * d['first']:.0f} in a hundred", font_size=44, color=TUNE)).arrange(DOWN, buff=0.15),
                     VGroup(label(r"right within three guesses", font_size=26, color=GREY_A), label(rf"{100 * d['three']:.0f} in a hundred", font_size=44, color=TUNE)).arrange(DOWN, buff=0.15),
                     VGroup(label(r"by blind luck, \ first time", font_size=26, color=GREY_A), label(rf"{100 * d['chance_first']:.0f} in a hundred", font_size=44, color=WEAK)).arrange(DOWN, buff=0.15)).arrange(RIGHT, buff=1.0).move_to(DOWN * 0.3)
        head = label(r"Shannon's guessing game: \ what is the next note?", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Shannon had a way to make bits concrete: a guessing game. Hide the next letter of a "
            "sentence, and count how many guesses a reader needs. Play it on melody. Show a model a tune "
            "it has never met, one note at a time, and ask it to guess the next. <bookmark mark='a'/> "
            f"Its first guess is right {say(100 * d['first'])} times in a hundred. <bookmark mark='b'/> "
            f"Within three guesses it is right {say(100 * d['three'])} times. <bookmark mark='c'/> Blind "
            f"luck would manage {say(100 * d['chance_first'])} in a hundred at the first attempt. That "
            "gap is what the word predictable means; and it is why you can sing along to the second "
            "verse of a song that you have never heard before."
        ) as vo:
            self.play(FadeIn(head))
            for mark, b in zip("abc", big):
                vo.wait_until(mark)
                self.play(FadeIn(b))
        self.wait(0.4)
        self.clear_scene()
