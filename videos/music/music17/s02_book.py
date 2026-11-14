from __future__ import annotations

import numpy as np

from videos.music.music17.common import *  # noqa: F403


class Book(SoundScene):
    def construct(self):
        chapter(self, 1, r"A book of chorales", r"What did Bach leave, \ and what is in it?", extra=((1784, r"C. P. E. Bach's edition"),))
        self.history()
        self.numbers()
        self.two()

    # ------------------------------------------------------------------
    def history(self):
        card = history_card(1784, r"C. P. E. Bach and Breitkopf, \ Leipzig", r"371 four-part chorales by J. S. Bach, \ collected from his cantatas and Passions, \ printed in four volumes, \ 1784--87", width=10.4, font_size=26).to_edge(UP, buff=0.4)
        facts = VGroup(label(r"a chorale: \ a Lutheran hymn, \ sung by everyone, \ one note to a syllable", font_size=26, color=WHITE),
                       label(r"Bach's settings: \ the tune on top, \ three voices beneath, \ a pause (a fermata) at each line's end", font_size=26, color=WHITE),
                       label(r"since then: \ the exercise book of every harmony class", font_size=26, color=TUNE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.8)
        with self.voiceover(
            "A chorale is a Lutheran hymn: a tune everyone could sing, one note to each syllable, a pause "
            "at the end of each line of verse. Bach wrote hundreds of four-part settings of them for his "
            "cantatas and Passions. <bookmark mark='a'/> After his death his son Carl Philipp Emanuel "
            "collected three hundred and seventy-one and had them printed, in four volumes, between 1784 "
            "and 1787. <bookmark mark='b'/> Composers and teachers studied them from the start, and for "
            "two centuries harmony students have been set the same "
            "exercise: here is a chorale tune, write the other three voices, then compare with Bach."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(facts[0]), FadeIn(facts[1]))
            vo.wait_until("b")
            self.play(FadeIn(facts[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def numbers(self):
        d = load("book")
        rows_ = [(r"chorales, \ each in four voices", f"{d['count']}"),
                 (r"in major \ / \ in minor", f"{d['modes']['major']} \\ / \\ {d['modes']['minor']}"),
                 (r"in four beats to the bar \ / \ in three", f"{d['metres']['4/4']} \\ / \\ {d['metres']['3/4']}"),
                 (r"notes, \ all voices", f"{d['notes']:,}".replace(",", "{,}")),
                 (r"beats in a chorale, \ on average", f"{d['beats_mean']:.0f}"),
                 (r"phrases (fermatas) in a chorale, \ on average", f"{d['phrases_mean']:.1f}"),
                 (r"different tunes", f"{d['tunes']}"),
                 (r"tunes set more than once", f"{d['set_more']}")]
        tab = VGroup(*[VGroup(label(a, font_size=26, color=GREY_A), label(b, font_size=28, color=TUNE)) for a, b in rows_])
        for k, r in enumerate(tab):
            r[0].move_to([-1.2, 2.4 - 0.62 * k, 0], aligned_edge=RIGHT)
            r[1].move_to([0.0, 2.4 - 0.62 * k, 0], aligned_edge=LEFT)
        src = label(r"source: \ the music21 corpus's encodings \ (M. S. Cuthbert and others); \ pitches, \ times and fermatas only", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"This part works from {say(d['count'])} of them, encoded note by note in the music21 "
            f"corpus. <bookmark mark='a'/> About half are in major keys and half in minor; nearly all have "
            f"four beats to the bar. Together they hold {say(round(d['notes'], -3))} notes. A chorale "
            f"runs about {say(round(d['beats_mean']))} beats, in about six phrases. <bookmark mark='b'/> "
            f"There are {say(d['tunes'])} different tunes among them, and {say(d['set_more'])} of the tunes "
            f"are set more than once. The tune of the hook is set {say(len(d['passion']))} times."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r) for r in tab[:6]], lag_ratio=0.2), FadeIn(src), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[6:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two(self):
        d = load("book")
        c = clip("book.two")
        gs = VGroup()
        for k, key in enumerate("ab"):
            g = choir_roll(d["two"]["voices"][k], width=5.6, height=3.0, lo=38, hi=78, thick=0.1).move_to(LEFT * 3.3 * (1 - 2 * k) + DOWN * 0.3)
            gs.add(g)
        labs = VGroup(label(r"No. 15: \ `Erkenne mich, \ mein H\"uter'", font_size=22, color=GREY_A).next_to(gs[0], UP, buff=0.3),
                      label(r"No. 62: \ `Wenn ich einmal soll scheiden'", font_size=22, color=GREY_A).next_to(gs[1], UP, buff=0.3))
        head = label(r"one tune, \ two settings, \ one Passion", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Here is the first phrase of that tune in two of the settings in the Passion: the first "
            "time it is sung, and the last. The last is a tone lower. Listen to the bass, the lowest "
            "line."
        ):
            self.play(FadeIn(head), FadeIn(gs), FadeIn(labs))
        with self.listen(c) as snd:
            window(snd, r"two settings of one phrase", kind="synthesized", detail=r"a model choir", corner=DL, tag_corner=DR)
            sing_roll(snd, gs[0], d["times"]["a"], start=d["starts"]["a"])
            sing_roll(snd, gs[1], d["times"]["b"], start=d["starts"]["b"])
            pulse(snd, labs[0], d["starts"]["a"], d["starts"]["b"] - 0.5, buff=0.1)
            pulse(snd, labs[1], d["starts"]["b"], c.duration, buff=0.1)
        with self.voiceover(
            "The same melody, and a different harmony under it: the bass takes another path and the chords "
            "change with it, from the first chord on. A chorale tune does not fix its harmony. That is what makes harmonizing one a "
            "real problem, with more than one good answer, and it is why the comparison with Bach later in "
            "this part has to be read with care."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()
