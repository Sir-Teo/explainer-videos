from __future__ import annotations

import numpy as np

from videos.music.music17.common import *  # noqa: F403


def heat(names, mat, size: float = 0.62, font_size: int = 20) -> VGroup:
    """A square table of counts, row = chord, column = the chord after it, shaded by the share of the row."""
    m = np.array(mat, dtype=float)
    share = m / np.maximum(m.sum(1, keepdims=True), 1)
    g = VGroup()
    n = len(names)
    for i in range(n):
        for j in range(n):
            sq = Square(side_length=size, stroke_color=DIM, stroke_width=1, fill_color=TUNE, fill_opacity=float(min(1.0, 1.6 * share[i, j])))
            sq.move_to([j * size, -i * size, 0])
            g.add(sq)
            if share[i, j] >= 0.12:
                g.add(label(f"{100 * share[i, j]:.0f}", font_size=font_size - 4, color=BLACK if share[i, j] > 0.35 else WHITE).move_to(sq))
    for i, nm in enumerate(names):
        g.add(label(nm, font_size=font_size, color=GREY_A).move_to([-0.75 * size - 0.15, -i * size, 0]))
        g.add(label(nm, font_size=font_size, color=GREY_A).move_to([i * size, 0.75 * size + 0.05, 0]))
    return g


class Vocab(SoundScene):
    def construct(self):
        chapter(self, 6, r"Chords on the beat", r"Which chords, \ and which follows which?")
        self.labels()
        self.counts()
        self.follows()

    # ------------------------------------------------------------------
    def labels(self):
        ex = [(72, 67, 64, 48), (71, 67, 62, 43), (72, 64, 57, 45)]
        st = block_staff(ex, width=4.6, beats=2).move_to(LEFT * 3.2 + DOWN * 0.2)
        names = VGroup(*[label(t, font_size=28, color=TUNE) for t in (r"I", r"V", r"vi")]).arrange(RIGHT, buff=1.1).next_to(st, DOWN, buff=0.4)
        txt = VGroup(label(r"on every beat: \ the four notes sounding", font_size=26, color=WHITE),
                     label(r"name the chord by its root, \ relative to home \ (Part 13's Roman numerals)", font_size=26, color=WHITE),
                     label(r"9 beats in 100 are no chord: \ passing notes in between", font_size=24, color=GREY_B)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * 2.8 + DOWN * 0.1)
        with self.voiceover(
            "To ask which chords Bach uses, name the chord on every beat. Take the four notes sounding at "
            "the beat, find the root as Part 13 did, and write it as a Roman numeral relative to the "
            "key: here the home chord, one, then the chord on the fifth degree, five, then six. "
            "<bookmark mark='a'/> About nine beats in a hundred carry no chord at all: a passing note "
            "happens to sound on the beat. Those are left unnamed."
        ) as vo:
            self.play(FadeIn(st), FadeIn(names), FadeIn(txt[0]), FadeIn(txt[1]))
            vo.wait_until("a")
            self.play(FadeIn(txt[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counts(self):
        d = load("vocab")
        mj, mn = d["major"], d["minor"]
        tot_j = sum(n for _, n in mj["top"])
        tot_n = sum(n for _, n in mn["top"])
        c1 = columns([100 * n / tot_j for _, n in mj["top"][:8]], [nm for nm, _ in mj["top"][:8]], width=5.6, height=2.4, color=WEAK, hot=(0, 1), hot_color=TUNE, fmt="{:.0f}", font_size=22).move_to(LEFT * 3.3 + DOWN * 0.6)
        c2 = columns([100 * n / tot_n for _, n in mn["top"][:8]], [nm for nm, _ in mn["top"][:8]], width=5.6, height=2.4, color=WEAK, hot=(0, 3), hot_color=TUNE, fmt="{:.0f}", font_size=22).move_to(RIGHT * 3.3 + DOWN * 0.6)
        t1 = label(rf"major: \ {mj['beats']:,} beats".replace(",", "{,}"), font_size=24, color=GREY_A).next_to(c1, UP, buff=0.35)
        t2 = label(rf"minor: \ {mn['beats']:,} beats".replace(",", "{,}"), font_size=24, color=GREY_A).next_to(c2, UP, buff=0.35)
        foot = label(r"shares of the named beats, \ in a hundred \ (inversions counted with their chord)", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.4)
        j0, j1 = mj["top"][0][1] / tot_j, mj["top"][1][1] / tot_j
        with self.voiceover(
            "Here are the commonest chords, in major keys and in minor. <bookmark mark='a'/> In major, the "
            f"home chord takes {say(round(100 * j0))} beats in a hundred and the dominant "
            f"{say(round(100 * j1))}: between them, nearly half the music. Then the chords on six, four "
            "and two, and then a chord that is not in the key at all, two with a major third: it is the "
            "dominant of the dominant, the pivot of Part 15, here borrowed for a moment. "
            "<bookmark mark='b'/> In minor the home chord is again first, but the relative major, three, "
            "comes second: minor chorales spend much of their time in the major key next door. And the "
            "dominant in minor is major, with its raised leading note, as Part 15 found."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(c1), FadeIn(t1), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(c2), FadeIn(t2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def follows(self):
        d = load("vocab")["major"]
        names = d["matrix_names"][:7]
        mat = [row[:7] for row in d["matrix"][:7]]
        h = heat(names, mat).move_to(LEFT * 2.6 + DOWN * 0.3)
        tl = label(r"row: \ a chord; \ column: \ the chord on the next beat \ (share of the row, \ in a hundred)", font_size=20, color=GREY_B).next_to(h, DOWN, buff=0.35)
        aft = d["after"]
        side = VGroup(label(rf"after V: \ I \ ({aft['V'][0][1]} times), \ V again \ ({aft['V'][1][1]})", font_size=22, color=WHITE),
                      label(r"after II \ (the dominant's dominant): \ V", font_size=22, color=WHITE),
                      label(rf"the same chord again: \ {100 * d['same_next']:.0f} beats in a hundred", font_size=22, color=WHITE),
                      label(r"a grammar of progressions: \ Part 18", font_size=24, color=TUNE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.6 + UP * 0.2)
        with self.voiceover(
            "And which chord follows which. Each row is a chord, each column the chord on the next beat, "
            "and the shading says how often. <bookmark mark='a'/> Five goes home to one more than "
            "anywhere else, apart from staying where it is. The dominant of the dominant goes to the dominant, as its name says. Four "
            "goes to one or to five. <bookmark mark='b'/> And about one beat in four keeps the same chord, "
            "while the voices move within it. <bookmark mark='c'/> This table is the first half of the "
            "harmonizer this part will build: a model of which chord comes next. Part 18 asks where the "
            "table comes from."
        ) as vo:
            self.play(FadeIn(h), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
