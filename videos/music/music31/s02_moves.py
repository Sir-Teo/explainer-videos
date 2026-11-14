from __future__ import annotations

import numpy as np

from videos.music.music31.common import *  # noqa: F403


class Moves(SoundScene):
    def construct(self):
        chapter(self, 1, r"Naming the moves", r"What is the smallest change that makes a new triad?", extra=((1987, r"Lewin's \textit{Generalized Musical Intervals}"),))
        self.three()
        self.quiz()
        self.parsimony()
        self.minor()
        self.table()
        self.compound()
        self.lewin()
        self.dualism()

    # ------------------------------------------------------------------
    def three(self):
        d = load("plr")
        rows_ = VGroup()
        desc = {"P": r"P \ (parallel): \ C major $\leftrightarrow$ C minor: \ the third moves a semitone",
                "L": r"L \ (leading-tone exchange): \ C major $\leftrightarrow$ E minor: \ the root moves down a semitone",
                "R": r"R \ (relative): \ C major $\leftrightarrow$ A minor: \ the fifth moves up a whole tone"}
        for k in ("P", "L", "R"):
            rows_.add(label(desc[k], font_size=23, color=TUNE if k == "P" else (BLUE if k == "L" else EAR)))
        rows_.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(UP * 0.4)
        foot = label(r"each is its own inverse: \ do it twice and you are back", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.8)
        head = label(r"three moves, \ each keeping two notes", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Here are the three moves. <bookmark mark='a'/> P, for parallel, turns C major into C minor: the root and fifth "
            "stay, and the third moves down a semitone. <bookmark mark='b'/> L, the leading-tone exchange, turns C major "
            "into E minor: E and G stay, and C moves down a semitone to B. <bookmark mark='c'/> R, for relative, turns C "
            "major into A minor: C and E stay, and G moves up a whole tone to A. <bookmark mark='d'/> Each move undoes "
            "itself: do it twice and you are back where you started."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("plr")
        c = clip("plr.quiz")
        card = listen_card(r"C major, \ three times, \ each time followed by one of P, \ L and R. \ "
                           r"Which pair is P, \ the move from major to minor on the same root: \ A, \ B or C?", width=10.6)
        with self.voiceover(
            "A question for your ears. C major, three times, each time followed by a different one of the three moves. Which "
            "pair is P, major turning to minor on the same root: A, B or C? Listen for the bass."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        cells = VGroup()
        for k, letter in zip(d["order"], "ABC"):
            p = d["pairs"][k]
            g = mroll(p["notes"], width=2.4, height=1.8, lo=34, hi=72, color=GREY_A, bar_h=0.1)
            cells.add(VGroup(label(letter, font_size=36, color=GREY_A), g).arrange(DOWN, buff=0.3))
        cells.arrange(RIGHT, buff=1.0).move_to(DOWN * 0.1)
        self.play(FadeOut(card), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ C", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            order = d["order"]
            for i, k in enumerate(order):
                end = d["starts"][order[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, cells[i][0], d["starts"][k], end, buff=0.08)
        ans = VGroup(*[label(rf"{k}: \ C to {tex_triad(d['pairs'][k]['to'])}", font_size=21, color=TUNE if k == "P" else GREY_A).next_to(cells[i], DOWN, buff=0.35)
                       for i, k in enumerate(d["order"])])
        with self.voiceover(
            "C is P: the bass stays on C, and the chord darkens from major to minor. A is L, to E minor, whose bass moves "
            "up to E; B is R, to A minor, whose bass moves up to A. All three change just one note of the chord."
        ):
            self.play(FadeIn(ans), cells[2][1].animate.set_color(TUNE))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parsimony(self):
        d = load("plr")
        bars = columns([d["pairs"][k]["semitones"] for k in ("P", "L", "R")], [r"P", r"L", r"R"], width=4.6, height=2.0, color=TUNE, fmt="{:.0f}", font_size=22)
        bars.move_to(LEFT * 3.2 + DOWN * 0.3)
        t = label(r"semitones the voices move, \ in total", font_size=21, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (r"P and L: \ one voice, \ one semitone", WHITE),
            (r"R: \ one voice, \ one whole tone", WHITE),
            (r"Richard Cohn: \ `parsimonious' voice leading", TUNE),
            (r"the smoothest possible change between different triads", EAR))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        side.move_to(RIGHT * 3.3 + DOWN * 0.2)
        with self.voiceover(
            "Count how far the voices move. <bookmark mark='a'/> P and L move one voice by one semitone; "
            "<bookmark mark='b'/> R moves one voice by a whole tone. <bookmark mark='c'/> The theorist Richard Cohn calls "
            "this parsimonious voice leading. <bookmark mark='d'/> No change between two different triads can be smoother, "
            "which is why these moves sound so natural even when they leave the key."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lewin(self):
        items = [
            (r"Lewin's idea: \ a space of objects \ (notes, \ chords, \ rhythms) \ and a group of moves acting on it", WHITE),
            (r"an interval is not a distance but an action: \ `if I am at s, \ where do I go to reach t?'", WHITE),
            (r"Part 29's $T_n$ and $I_n$ were already such moves, \ acting on sets", WHITE),
            (r"Hugo Riemann and Arthur von Oettingen had named P, \ L and R a century earlier", TUNE),
            (r"Cohn, \ Hyer and others revived them in the 1990s: \ `neo-Riemannian theory'", GREY_A),
        ]
        rows_scene(self, r"intervals as actions", items,
                   "Lewin's idea was general. <bookmark mark='b'/> Take a space of musical objects, notes, chords or rhythms, "
                   "and a group of moves acting on it. <bookmark mark='c'/> Then an interval is not a distance but an action: if "
                   "I am at s, what do I do to reach t? <bookmark mark='d'/> Part 29's transpositions and inversions were already "
                   "moves of this kind, acting on sets. <bookmark mark='e'/> The moves P, L and R themselves had been described a "
                   "century earlier, by Riemann and by Arthur von Oettingen. <bookmark mark='f'/> Cohn, Brian Hyer and others "
                   "revived them in the 1990s, under the name neo-Riemannian theory.", marks="cdef")

    # ------------------------------------------------------------------
    def compound(self):
        d = load("compound")
        c = clip("compound.three")
        cells = VGroup()
        for w in d["words"]:
            p = d["pairs"][w]
            cells.add(VGroup(label(w, font_size=34, color=TUNE), label(rf"C to {tex_triad(p['to'])}", font_size=24, color=WHITE),
                             label(rf"{p['common']} note kept, \ {p['vl']} semitones", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.25))
        cells.arrange(RIGHT, buff=1.4).move_to(DOWN * 0.1)
        head = label(r"two moves in a row", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Moves combine. L then P takes C major to E major; P then L takes it to A flat major; R then P to A major. Each "
            "keeps one note and moves the other two a little: two or three semitones in all. Hear the three; these two-step "
            "moves are the chromatic mediants that chapter six finds in film scores."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"LP, \ PL, \ RP", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            ws = d["words"]
            for i, w in enumerate(ws):
                end = d["starts"][ws[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, cells[i][0], d["starts"][w], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dualism(self):
        items = [
            (r"Riemann and Oettingen: \ a minor triad is a major triad turned upside down", WHITE),
            (r"C major built up from C: \ C, \ E, \ G; \ its mirror built down from G: \ G, \ E$\flat$, \ C", WHITE),
            (r"so P, \ L and R swap a triad with its mirror across one of its intervals", WHITE),
            (r"the idea is Part 29's inversion, \ $I_n$, \ applied to triads a century early", TUNE),
            (r"dualism was abandoned as a theory of hearing; \ its mathematics survived", GREY_A),
        ]
        rows_scene(self, r"Riemann's dualism", items,
                   "Riemann and Oettingen had a reason to pair the moves. <bookmark mark='b'/> In their dualist theory a minor triad is a major triad turned upside down: <bookmark mark='c'/> C major is built up from C, C, E, G, and its mirror is built down from G, G, E flat, C. <bookmark mark='d'/> So each of P, L and R exchanges a triad with its mirror image across one of its intervals. <bookmark mark='e'/> It is Part 29's inversion, applied to triads a century early. <bookmark mark='f'/> Dualism was abandoned as a theory of hearing, but its mathematics survived.", marks="cdef")

    # ------------------------------------------------------------------
    def minor(self):
        d = load("minor")
        c = clip("minor.three")
        cells = VGroup()
        for m in d["moves"]:
            cells.add(VGroup(label(m["move"], font_size=38, color=TUNE), label(rf"a to {tex_triad(m['to'])}", font_size=26, color=WHITE),
                             label(rf"{m['common']} kept, \ {m['vl']} semitone{'s' if m['vl'] > 1 else ''}", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.25))
        cells.arrange(RIGHT, buff=1.8).move_to(DOWN * 0.1)
        head = label(r"the same three moves, \ from A minor", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The moves work on minor triads too. From A minor: P raises the third a semitone, C to C sharp, giving A major. "
            "L raises the fifth a semitone, E to F, giving F major. R lowers the root a whole tone, A to G, giving C major, "
            "the relative major. Each keeps two notes. Listen to all three."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"P, \ L, \ R \ from a", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            ks = list("PLR")
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, cells[i][0], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        heads = [r"move", r"on a major triad", r"on a minor triad", r"keeps"]
        data = [
            (r"P", r"third down a semitone \ (C, \ E, \ G to C, \ E$\flat$, \ G)", r"third up a semitone", r"root and fifth"),
            (r"L", r"root down a semitone \ (C to B: \ e minor)", r"fifth up a semitone", r"the major third"),
            (r"R", r"fifth up a whole tone \ (G to A: \ a minor)", r"root down a whole tone", r"the minor third"),
        ]
        rows_ = VGroup()
        hr = VGroup(*[label(h, font_size=21, color=GREY_A) for h in heads])
        rows_.add(hr)
        for r in data:
            rows_.add(VGroup(*[label(x, font_size=21, color=TUNE if j == 0 else WHITE) for j, x in enumerate(r)]))
        xs = [-5.6, -2.6, 1.6, 4.6]
        for i, r in enumerate(rows_):
            for j, cell in enumerate(r):
                cell.move_to([xs[j], 1.6 - 1.1 * i, 0])
        head = label(r"the three moves, \ one voice each", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"on a minor triad each move runs backwards: \ that is why each move undoes itself", font_size=21, color=EAR).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A table makes the pattern plain. <bookmark mark='a'/> P keeps the root and fifth and moves the third by a "
            "semitone: down on a major triad, up on a minor one. <bookmark mark='b'/> L keeps the major third: on a major "
            "triad the root drops a semitone, C to B, giving E minor; on a minor triad the fifth rises a semitone. "
            "<bookmark mark='c'/> R keeps the minor third: on a major triad the fifth rises a whole tone, G to A, giving A "
            "minor; on a minor triad the root falls a whole tone. <bookmark mark='d'/> On a minor triad every move runs the "
            "other way, and that is why doing a move twice brings you back."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("abc", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
