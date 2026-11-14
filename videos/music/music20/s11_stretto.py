from __future__ import annotations

import numpy as np

from videos.music.music20.common import *  # noqa: F403

IV = {-24: r"two octaves below", -19: r"an octave and a fifth below", -17: r"an octave and a fourth below", -12: r"an octave below",
      -7: r"a fifth below", -5: r"a fourth below", 0: r"the unison", 5: r"a fourth above", 7: r"a fifth above", 12: r"an octave above"}


class Stretto(SoundScene):
    def construct(self):
        chapter(self, 10, r"Stretto", r"How close can the entries come?")
        self.table()
        self.hear()
        self.inversion()
        self.census()

    # ------------------------------------------------------------------
    def table(self):
        d = load("stretto")
        ivs = [-12, -7, -5, 0, 5, 7, 12]
        delays = sorted({x["delay"] for x in d["all"]} | {1.0, 2.0, 3.0, 4.0, 5.0, 6.0})
        ok = {(x["delay"], x["interval"]) for x in d["all"]}
        cell = 0.55
        grid = VGroup()
        for i, iv in enumerate(ivs):
            for j, dl in enumerate(delays):
                good = (dl, iv) in ok
                sq = Square(side_length=cell - 0.06, stroke_width=1.2, stroke_color=GREY_B, fill_color=TUNE if good else DIM, fill_opacity=0.85 if good else 0.25)
                sq.move_to([(j - len(delays) / 2 + 0.5) * cell, (len(ivs) / 2 - 0.5 - i) * cell, 0])
                grid.add(sq)
        cols = VGroup(*[label(rf"{int(dl)}", font_size=18, color=GREY_A).move_to([(j - len(delays) / 2 + 0.5) * cell, (len(ivs) / 2 + 0.2) * cell, 0]) for j, dl in enumerate(delays)])
        rws = VGroup(*[label(rf"{iv:+d}" if iv else r"0", font_size=18, color=GREY_A).move_to([-(len(delays) / 2 + 0.6) * cell, (len(ivs) / 2 - 0.5 - i) * cell, 0]) for i, iv in enumerate(ivs)])
        tab = VGroup(grid, cols, rws).move_to(LEFT * 3.0 + DOWN * 0.3)
        xl = label(r"the second voice enters after ... beats", font_size=20, color=GREY_B).next_to(tab, UP, buff=0.25)
        yl = label(r"semitones", font_size=18, color=GREY_B).next_to(tab, LEFT, buff=0.15)
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"stretto: \ the next entry before the last has finished", WHITE),
            (r"try every delay and every interval; \ keep those with no clash and no parallels", WHITE),
            (rf"the Tune's phrase: \ {len(d['all'])} ways; \ the closest, \ {int(d['best']['delay'])} beats behind, \ {IV[d['best']['interval']]}", TUNE),
            (r"the entries that come late are easy: \ they hardly overlap", GREY_A))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.2))
        rows_.move_to(RIGHT * 3.6 + DOWN * 0.1)
        with self.voiceover(
            "Late in a fugue, the entries often crowd together: the next voice comes in before the last has finished. "
            "This is stretto, from the Italian for tightening. <bookmark mark='a'/> Which strettos does a subject "
            "allow? The program tries every delay and every common interval, and keeps the ones in which the two "
            "entries never clash on a beat and never move in parallel fifths or octaves. <bookmark mark='b'/> For the "
            f"Tune's first phrase there are {say(len(d['all']))}. <bookmark mark='c'/> The closest: the second voice "
            f"{say(int(d['best']['delay']))} beats behind, {IV[d['best']['interval']].replace(chr(92), '')}. "
            "<bookmark mark='d'/> The entries that come late are easy, since they hardly overlap; the close ones are "
            "the prize, and composers designed subjects to allow them."
        ) as vo:
            self.play(FadeIn(tab), FadeIn(xl), FadeIn(yl), FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("stretto")
        c = clip("stretto.tune")
        g2 = voices_roll(d["lines"], width=5.2, height=2.8, lo=50, hi=84, total=12.0).move_to(LEFT * 3.4 + DOWN * 0.3)
        g3 = voices_roll(d["lines"] + [d["third"]], width=5.2, height=2.8, lo=50, hi=84, total=12.0).move_to(RIGHT * 3.4 + DOWN * 0.3)
        t2 = label(r"two entries", font_size=24, color=GREY_A).next_to(g2, UP, buff=0.3)
        t3 = label(r"and a third, \ in the bass", font_size=24, color=GREY_A).next_to(g3, UP, buff=0.3)
        te = d["third_entry"]
        with self.voiceover(
            f"Here it is, and then with a third entry the program found as well: the bass, {say(int(te['delay']))} beats "
            f"after the first voice, {IV[te['interval']]}. Three entries of the phrase within four beats, with nothing "
            "clashing."
        ):
            self.play(FadeIn(g2), FadeIn(g3), FadeIn(t2), FadeIn(t3))
        with self.listen(c) as snd:
            window(snd, r"the phrase in stretto, \ two voices, \ then three", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_voices(snd, g2, d["lines"], start=d["starts"]["two"])
            sing_voices(snd, g3, d["lines"] + [d["third"]], start=d["starts"]["three"])
            pulse(snd, t2, d["starts"]["two"], d["starts"]["three"] - 0.5, buff=0.08)
            pulse(snd, t3, d["starts"]["three"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inversion(self):
        d = load("stretto")
        n_dir, n_inv = len(d["all"]), len(d["by_inversion"])
        close_inv = sum(1 for x in d["by_inversion"] if x["delay"] <= 2)
        close_dir = sum(1 for x in d["all"] if x["delay"] <= 2)
        ch = columns([n_dir, n_inv], [r"answered as it is", r"answered upside down"], width=5.0, height=2.6, color=WEAK, hot=(1,), hot_color=TUNE, fmt="{:.0f}", font_size=22).move_to(LEFT * 3.0 + DOWN * 0.5)
        t = label(r"strettos of the Tune's phrase \ (delays up to 6 beats)", font_size=22, color=GREY_A).next_to(ch, UP, buff=0.4)
        rows_ = VGroup(*[label(t_, font_size=24, color=c_) for t_, c_ in (
            (r"stretto by inversion: \ the second voice enters upside down", WHITE),
            (rf"two beats behind: \ {close_dir} way as it is, \ {close_inv} ways inverted", TUNE),
            (r"\textit{The Art of Fugue}, \ Contrapuncti 5 to 7: \ stretto fugues of exactly this kind", WHITE))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.0))
        rows_.move_to(RIGHT * 3.6 + DOWN * 0.2)
        with self.voiceover(
            "A stretto can also bring the second voice in upside down. <bookmark mark='a'/> Give the search the "
            f"phrase's inversion as the follower: it finds {say(n_inv)} strettos, against {say(n_dir)} with the phrase "
            f"as it is, and {say(close_inv)} of them only two beats behind, where the plain phrase allowed "
            f"{say(close_dir)}. <bookmark mark='b'/> A line and its mirror image fill each other's gaps: when one rises, "
            "the other falls, and they meet less often on the same wrong note. <bookmark mark='c'/> Bach built the "
            "stretto fugues of The Art of Fugue, its fifth to seventh pieces, on exactly this: the subject against its "
            "own inversion, and then against it slowed down and sped up as well."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(t), FadeIn(rows_[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def census(self):
        d = load("stretto")
        counts = [r["strettos"] for r in d["census"]]
        bins = [sum(1 for x in counts if x == 0), sum(1 for x in counts if 1 <= x <= 3), sum(1 for x in counts if 4 <= x <= 8), sum(1 for x in counts if x > 8)]
        ch = columns(bins, [r"none", r"1--3", r"4--8", r"more"], width=6.0, height=2.6, color=WEAK, hot=(0,), hot_color=EAR, fmt="{:.0f}", font_size=22).move_to(LEFT * 2.8 + DOWN * 0.5)
        t = label(r"the opening phrases of Part 14's tunes: \ strettos entering by the phrase's midpoint", font_size=21, color=GREY_A).next_to(ch, UP, buff=0.4)
        side = VGroup(label(rf"{d['with_stretto']} of {d['n']} phrases allow one", font_size=26, color=TUNE),
                      label(r"folk tunes repeat notes and outline chords: \ easy to overlap", font_size=22, color=WHITE),
                      label(r"a chromatic subject, \ like the king's, \ allows very few", font_size=22, color=EAR),
                      label(r"no fugue scores offline: \ Bach's own strettos are not counted here", font_size=20, color=GREY_B)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.6))
        side.move_to(RIGHT * 3.9 + DOWN * 0.2)
        with self.voiceover(
            "How special is that? Run the same search on the opening phrase of every tune in Part 14's collection, "
            "allowing the second voice to enter anywhere up to the phrase's midpoint. "
            f"<bookmark mark='a'/> {say(d['with_stretto'])} of the {say(d['n'])} phrases allow at least one stretto. "
            "<bookmark mark='b'/> Folk tunes repeat notes and outline a chord, which makes them easy to overlap. "
            "<bookmark mark='c'/> A chromatic subject like the king's is the opposite. With its rhythm simplified, "
            f"the program finds no stretto for the king's theme until the second voice waits {say(int(d['royal']['earliest']))} "
            f"of its {say(int(d['royal']['length']))} beats, when the two hardly overlap: its slide clashes with itself "
            "almost everywhere, which is part of why the king's challenge was hard. <bookmark mark='d'/> Bach's own "
            "fugue subjects could not be counted here, since no fugue scores were available to this series offline; "
            "the problem set asks you to do it."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(t))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
