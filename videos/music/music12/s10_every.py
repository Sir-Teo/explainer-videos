from __future__ import annotations

import numpy as np

from videos.music.music12.common import *  # noqa: F403
from explainer.music.monochord import scales as S


def tiny(steps, radius: float = 0.3, color=WEAK) -> VGroup:
    """A scale shape as a small polygon in a circle of twelve places."""
    notes = S.pcs(steps)
    pts = [radius * np.array([np.cos(np.pi / 2 - 2 * np.pi * n / 12), np.sin(np.pi / 2 - 2 * np.pi * n / 12), 0.0]) for n in notes]
    return VGroup(Circle(radius=radius, color=GREY_D, stroke_width=1), Polygon(*pts, color=color, stroke_width=1.8, fill_color=color, fill_opacity=0.15))


class Every(SoundScene):
    def construct(self):
        chapter(self, 9, r"Every scale there is", r"How many scales are possible, \ and where is ours?")
        self.small()
        self.count()
        self.wall()
        self.quiz()

    # ------------------------------------------------------------------
    def small(self):
        d = load("every")

        def beads(steps, r: float = 0.55) -> VGroup:
            on = set(S.pcs(steps)) if steps else set()
            g = VGroup(Circle(radius=r, color=GREY_D, stroke_width=1.5))
            for k in range(4):
                a = np.pi / 2 - 2 * np.pi * k / 4
                g.add(Dot(r * np.array([np.cos(a), np.sin(a), 0.0]), radius=0.13, color=TUNE if k in on else GREY_D))
            return g

        row = VGroup(*[beads(tuple(s)) for s in d["four"]]).arrange(RIGHT, buff=0.6).move_to(UP * 1.6)
        head = label(r"four places, \ each on or off: \ $2^4 = 16$ patterns, \ but only 6 shapes", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        row.shift(DOWN * 0.5)
        terms = VGroup(label(r"turn by 0: \ all 16 patterns look the same as before", font_size=26, color=GREY_A),
                       label(r"turn by a half: \ 4 patterns do (those that repeat every two places)", font_size=26, color=GREY_A),
                       label(r"turn by a quarter, \ either way: \ 2 each (all off, \ all on)", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(DOWN * 0.9)
        eq = MathTex(r"\frac{16 + 4 + 2 + 2}{4} = 6", font_size=48).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "To count scales we need one tool, and it is easiest to see on a small case. Take four places "
            "round a circle, each on or off. There are sixteen patterns. But a pattern turned round is "
            "the same shape, and there are only six shapes. <bookmark mark='a'/> How could we have known "
            "that without drawing them? Burnside's lemma says: for each way of turning the circle, count "
            "the patterns that the turn leaves looking the same; then take the average. "
            "<bookmark mark='b'/> Not turning at all leaves all sixteen. A half turn leaves four. A "
            "quarter turn, either way, leaves two. <bookmark mark='c'/> Sixteen plus four plus two plus "
            "two is twenty-four; divided by the four turns, six. The same sum works for any number of "
            "places."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(x) for x in row], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in terms], lag_ratio=0.7), run_time=5.0)
            vo.wait_until("c")
            self.play(FadeIn(eq))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def count(self):
        d = load("every")
        l1 = MathTex(r"\text{sets of notes that contain C:} \quad 2^{11} = 2048", font_size=38)
        l2 = MathTex(r"\tfrac{1}{12}\left(2^{12} + 2^{6} + 2 \cdot 2^{4} + 2 \cdot 2^{3} + 2 \cdot 2^{2} + 4 \cdot 2^{1}\right) = \tfrac{4224}{12} = 352", font_size=38)
        l3 = label(r"scale shapes: \ sets of notes, \ counted once however they are transposed", font_size=26, color=GREY_A)
        VGroup(l1, l3, l2).arrange(DOWN, buff=0.4).to_edge(UP, buff=0.5)
        g = axes([-0.7, 12.7], [0, 90], x_length=9.0, y_length=2.4, xlabel=r"notes in the scale", ylabel=r"shapes", xticks=list(range(0, 13)), yticks=[0, 40, 80], font_size=20).move_to(DOWN * 1.9)
        bars = VGroup(*[Rectangle(width=0.42, height=max(g.ax.c2p(0, v)[1] - g.ax.c2p(0, 0)[1], 0.02), stroke_width=0, fill_color=TUNE if k == 7 else WEAK, fill_opacity=0.9).move_to(g.ax.c2p(k, 0), aligned_edge=DOWN)
                        for k, v in enumerate(d["counts"])])
        nums = VGroup(*[label(str(v), font_size=18, color=WHITE).next_to(b, UP, buff=0.05) for v, b in zip(d["counts"], bars)])
        boxes12 = VGroup(*[VGroup(RoundedRectangle(width=0.8, height=0.8, corner_radius=0.1, stroke_color=TUNE if k == 0 else GREY_C, stroke_width=2, fill_color=TUNE, fill_opacity=0.85 if k == 0 else 0.0),
                                  label(NOTE_NAMES[k], font_size=24, color=BLACK if k == 0 else GREY_A)) for k in range(12)]).arrange(RIGHT, buff=0.12).move_to(UP * 0.6)
        ask = label(r"the home note is in. \ Each of the other eleven: \ in, \ or out?", font_size=30, color=GREY_A).next_to(boxes12, DOWN, buff=0.6)
        with self.voiceover(
            "Now let us be thorough. How many scales could there be on twelve notes? A scale is a choice "
            "of some notes, including its home note; each of the other eleven is in or out. "
            "<bookmark mark='a'/> Two to the eleventh: two thousand and forty-eight. But many of those "
            "are the same scale starting on a different note, or moved to a different key. Call two sets "
            "the same shape if one is the other transposed. Counting shapes is a problem about "
            "necklaces: twelve beads, each black or white, where turning the necklace does not make a "
            "new one. <bookmark mark='b'/> Burnside's lemma counts them: average, over the twelve "
            "rotations, the number of colourings each rotation leaves unchanged. The answer is three "
            "hundred and fifty-two. Monochord also lists them all, and gets the same number. "
            "<bookmark mark='c'/> Here they are by size. Sixty-six shapes have seven notes."
        ) as vo:
            self.play(FadeIn(boxes12), FadeIn(ask))
            vo.wait_until("a")
            self.play(FadeOut(boxes12), FadeOut(ask), FadeIn(l1))
            self.wait(6.0)
            self.play(FadeIn(l3))
            vo.wait_until("b")
            self.play(FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(g), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(nums), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wall(self):
        d = load("every")
        dia = tuple(d["diatonic"])
        plain = [tuple(p) for p in d["plain"]]
        cells = VGroup(*[tiny(s) for s in d["sevens"]])
        cells.arrange_in_grid(rows=6, cols=11, buff=0.22).move_to(DOWN * 0.3)
        head = label(r"all 66 shapes of seven notes", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        idx_plain = [k for k, s in enumerate(d["sevens"]) if tuple(s) in plain]
        idx_dia = [k for k, s in enumerate(d["sevens"]) if tuple(s) == dia][0]
        l1 = label(r"only whole and half steps: \ 3 of them", font_size=26, color=SHORT).to_edge(DOWN, buff=0.75)
        l2 = label(r"with its two half steps as far apart as possible: \ 1", font_size=26, color=TUNE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here are all sixty-six, each drawn as a polygon in a circle of twelve places. Most are "
            "lopsided: notes bunched together, with wide gaps elsewhere. <bookmark mark='a'/> Ask for "
            "scales with no gap wider than a whole tone, built only from whole and half steps, and three "
            "are left. <bookmark mark='b'/> Ask that the two half steps be kept as far apart as they can "
            "be, and there is one. It is the white keys. Out of every possible scale of seven notes, the "
            "one on the keyboard is the single smoothest shape."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.02), run_time=3.0)
            vo.wait_until("a")
            self.play(*[cells[k][1].animate.set_color(SHORT).set_stroke(width=3) for k in idx_plain], *[cells[k].animate.set_opacity(0.3) for k in range(66) if k not in idx_plain], FadeIn(l1))
            vo.wait_until("b")
            cells[idx_dia][1].set_color(TUNE)
            self.play(cells[idx_dia].animate.scale(1.6), FadeIn(l2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("every")
        c = clip("every.three")
        card = listen_card(r"The three scales made only of whole and half steps. \ One is the major scale. \ Which: \ A, \ B or C?", width=10.0, font_size=26)
        with self.voiceover("Here are those three, as sound. One of them is the major scale. Which: A, B or C?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        cols = VGroup(*[VGroup(label(nm, font_size=44, color=GREY_A), tiny(st, radius=0.9, color=WEAK)).arrange(DOWN, buff=0.3) for nm, st in zip("ABC", d["quiz_steps"])]).arrange(RIGHT, buff=1.4).move_to(UP * 0.5)
        self.play(FadeOut(card), FadeIn(cols))
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ C", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k, col in enumerate(cols):
                pulse(snd, col[0], d["starts"][k], d["starts"][k] + 3.0, buff=0.12)
        names = [r"melodic minor, \ going up", r"major", r"five whole tones, \ then two half steps"]
        tags = VGroup(*[label(t, font_size=24, color=TUNE if k == 1 else GREY_A).next_to(col, DOWN, buff=0.3) for k, (t, col) in enumerate(zip(names, cols))])
        with self.voiceover(
            "B. A was the melodic minor scale of chapter five, whose half steps are two notes apart "
            "instead of three. C had its two half steps side by side, after five whole tones: nearly a "
            "whole-tone scale. All three are used. Only B is everywhere."
        ):
            self.play(FadeIn(tags), cols[1][1][1].animate.set_color(TUNE))
        self.wait(0.4)
        self.clear_scene()
