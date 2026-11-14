from __future__ import annotations

import numpy as np

from videos.music.music19.common import *  # noqa: F403


class Mixture(SoundScene):
    def construct(self):
        chapter(self, 2, r"Borrowing from the minor", r"What is mixture?")
        self.idea()
        self.hear()
        self.bach()

    # ------------------------------------------------------------------
    def idea(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"C major and C minor share a home, \ and four notes \ (Part 15)", WHITE),
            (r"so a major key can borrow the minor's chords: \ iv, \ $\flat$VI, \ $\flat$VII, \ $\flat$III", WHITE),
            (r"the borrowed notes: \ E$\flat$, \ A$\flat$, \ B$\flat$, \ a shadow over the major", WHITE),
            (r"Schubert's signature: \ major turning minor and back, \ in a phrase", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"mixture: \ the parallel minor's chords in a major key", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A second kind of borrowing takes whole chords. <bookmark mark='a'/> C major and C minor share a home, and "
            "Part 15 found they share four notes. <bookmark mark='b'/> So a piece in C major can borrow the chords of C "
            "minor: the minor four, the flat six, the flat seven, the flat three. <bookmark mark='c'/> The borrowed "
            "notes, E flat, A flat and B flat, pass over the major key like a shadow. <bookmark mark='d'/> Franz "
            "Schubert made this his signature: a major tune turning minor for a phrase, and back, the change of mode "
            "as an expression in itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("mixture")
        c = clip("mixture.three")
        cells = VGroup()
        widths = {"iv": 3.3, "flat6": 4.0, "flat3": 4.9}
        heads = {"iv": r"the minor iv", "flat6": r"$\flat$VI and $\flat$VII", "flat3": r"$\flat$III"}
        for name in ("iv", "flat6", "flat3"):
            st = block_staff(d["chords"][name], width=widths[name], beats=2)
            nm = VGroup(*[label(tex(n), font_size=22, color=TUNE) for n in d["names"][name]])
            for k, n in enumerate(nm):
                n.move_to([st.get_left()[0] + 0.95 + (st.width - 1.1) * (k + 0.5) / len(nm), st.get_bottom()[1] - 0.35, 0])
            hd = label(heads[name], font_size=24, color=GREY_A).next_to(st, UP, buff=0.3)
            cells.add(VGroup(st, nm, hd))
        cells.arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(DOWN * 0.1)
        with self.voiceover(
            "Three borrowings, in C major. First the minor four between two home chords: the plagal Amen of chapter one "
            "of Part 18, darkened. Then flat six and flat seven rising to home, a progression film composers still "
            "reach for. Then flat three, which turns a cadence toward the minor before it closes in the major."
        ):
            self.play(FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"iv; \ $\flat$VI, \ $\flat$VII; \ $\flat$III", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            order = ("iv", "flat6", "flat3")
            for k, name in enumerate(order):
                flash(snd, list(cells[k][1]), d["times"][name], hot=WHITE, base=TUNE)
                end = d["starts"][order[k + 1]] - 0.3 if k < 2 else c.duration
                pulse(snd, cells[k][2], d["starts"][name], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bach(self):
        d = load("mixture")
        c = clip("mixture.picardy")
        n_mix = sum(d["bach"].values())
        fin = d["final"]
        on_tonic = fin.get("0 major", 0) + fin.get("0 minor", 0)
        left = VGroup(label(r"Bach's major chorales", font_size=26, color=GREY_A),
                      label(rf"{n_mix} beats of {d['bach_beats']:,} borrow from the minor".replace(",", "{,}"), font_size=26, color=WHITE),
                      label(r"mostly $\flat$VII, \ often in old modal tunes", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.3).move_to(LEFT * 3.4 + UP * 1.6)
        ch = columns([fin.get("0 major", 0), fin.get("0 minor", 0)], [r"major", r"minor"], width=3.2, height=2.2, color=WEAK, hot=(0,), hot_color=TUNE, fmt="{:.0f}", font_size=22)
        right = VGroup(label(r"minor chorales ending on the tonic:", font_size=24, color=GREY_A), label(r"the last chord", font_size=20, color=GREY_B), ch).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.3 + UP * 0.3)
        sA = block_staff(d["picardy"]["minor"], width=3.4, beats=2, key=-3).move_to(LEFT * 4.6 + DOWN * 1.6)
        sB = block_staff(d["picardy"]["Picardy"], width=3.4, beats=2, key=-3).move_to(LEFT * 0.9 + DOWN * 1.6)
        la = label(r"ending minor", font_size=20, color=GREY_A).next_to(sA, UP, buff=0.15)
        lb = label(r"the Picardy third", font_size=20, color=TUNE).next_to(sB, UP, buff=0.15)
        with self.voiceover(
            "Did Bach borrow from the minor? Count the borrowed chords on the beats of his major chorales. "
            f"<bookmark mark='a'/> {say(n_mix)} beats in {say(d['bach_beats'])}, less than one in a hundred, and most of "
            "those are flat seven chords in old modal tunes. Mixture as colour is a nineteenth-century habit. "
            "<bookmark mark='b'/> But Bach borrowed the other way. Of his minor chorales that end on their tonic, "
            f"{say(fin.get('0 major', 0))} of {say(on_tonic)} end on a major chord: the minor key's third raised at the "
            "last moment, a Picardy third. Hear a cadence in C minor twice, ending minor and then major."
        ) as vo:
            self.play(FadeIn(left))
            vo.wait_until("a")
            self.play(Indicate(left[1], color=TUNE))
            vo.wait_until("b")
            self.play(FadeIn(right))
        self.play(FadeIn(sA), FadeIn(sB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"minor, \ then the Picardy third", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, la, d["picardy_starts"]["minor"], d["picardy_starts"]["Picardy"] - 0.5, buff=0.08)
            pulse(snd, lb, d["picardy_starts"]["Picardy"], c.duration, buff=0.08)
        with self.voiceover(
            "One note changes, E flat to E natural, and the ending turns from grief to consolation. The borrowing "
            "runs in both directions, and the direction says something about the style."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()
