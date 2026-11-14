from __future__ import annotations

import numpy as np

from videos.music.music18.common import *  # noqa: F403


class Census(SoundScene):
    def construct(self):
        chapter(self, 10, r"Where the schemata are", r"Can a machine find them?")
        self.chorales()
        self.tunes()
        self.prinner()

    # ------------------------------------------------------------------
    def chorales(self):
        d = load("census")
        ch = d["chorales"]
        names = ["Do-Re-Mi", "Romanesca", "Prinner", "Meyer", "Fonte", "Monte", "Ponte", "Quiescenza"]
        rows_ = VGroup()
        for k, n in enumerate(names):
            r = VGroup(label(n, font_size=24, color=WHITE), label(str(ch["real"].get(n, 0)), font_size=24, color=TUNE), label(str(ch["shuffled"].get(n, 0)), font_size=24, color=GREY_B))
            r[0].move_to([-1.2, 2.0 - 0.5 * k, 0], aligned_edge=RIGHT)
            r[1].move_to([0.4, 2.0 - 0.5 * k, 0])
            r[2].move_to([2.2, 2.0 - 0.5 * k, 0])
            rows_.add(r)
        hdr = VGroup(label(r"in the chorales", font_size=22, color=GREY_A).move_to([0.4, 2.55, 0]), label(r"shuffled", font_size=22, color=GREY_A).move_to([2.2, 2.55, 0]))
        cap = label(rf"a detector: \ the schema's bass and melody notes, \ in order, \ on the beats \ ({d['chorales_major']} major chorales)", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.5)
        tot = sum(ch["real"].values())
        with self.voiceover(
            "If schemata are real, a machine should be able to find them. Write each one as its bass and melody "
            "notes, and search the chorales' beats for them, in order. As a control, search the same chorales "
            "with their beats shuffled. <bookmark mark='a'/> The result is nearly empty: "
            f"{say(tot)} schemata in {say(d['chorales_major'])} major chorales, against a handful by chance. Bach's "
            "chorales are not galant music. Their tunes are older, given in advance, and set one chord to a "
            "note; the schemata belong to the instrumental and operatic music of Bach's younger contemporaries "
            "and the generation after, and a detector "
            "this strict, demanding every note in place, misses the ornamented forms in which they usually "
            "appear."
        ) as vo:
            self.play(FadeIn(hdr), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.15), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tunes(self):
        d = load("census")
        m = d["melodies"]
        keys = ["6-5-4-3", "4-3-2-1", "5-4-3-2-1", "1-2-3"]
        g = VGroup()
        for k, key in enumerate(keys):
            real, sh = m[key]["real"], m[key]["shuffled"]
            r = VGroup(label(key, font_size=28, color=TUNE), label(rf"{real} tunes", font_size=26, color=WHITE), label(rf"shuffled: \ {sh:.1f}", font_size=22, color=GREY_B))
            r[0].move_to([-3.0, 1.6 - 0.75 * k, 0], aligned_edge=RIGHT)
            r[1].move_to([-1.0, 1.6 - 0.75 * k, 0], aligned_edge=LEFT)
            r[2].move_to([1.2, 1.6 - 0.75 * k, 0], aligned_edge=LEFT)
            g.add(r)
        head = label(rf"the melodies of the series' {d['tunes_major']} major tunes: \ schema melodies, \ note by note", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        tune = label(r"the Tune: \ A A G F F E E \ = \ 6 6 5 4 4 3 3: \ a Prinner's melody", font_size=26, color=EAR).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The schemata's melodies are another matter. Search the series' fifty-one major tunes, from Part 14, "
            f"for them. <bookmark mark='a'/> The Prinner's falling six, five, four, three is in {say(m['6-5-4-3']['real'])} "
            "tunes, against fewer than one if their notes were shuffled. A melody falling four, three, two, one is in "
            f"{say(m['4-3-2-1']['real'])}. These are the stepwise descents of Part 14, and they are the melodies "
            "that schemata were built on. <bookmark mark='b'/> And the Tune has one: A, A, G, F, F, E, E, from the "
            "end of its first phrase into its second, is six, five, four, three. Its second half is a Prinner "
            "waiting for its bass."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(tune))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def prinner(self):
        d = load("census")["prinner"]
        c = clip("census.prinner")
        g = chord_roll(d["chords"], width=9.0, height=3.0, lo=40, hi=84, thick=0.13).move_to(DOWN * 0.3)
        names = VGroup(*[label(n, font_size=24, color=TUNE) for n in d["names"]])
        for k, n in enumerate(names):
            n.move_to([g.xk(k), g.frame.get_bottom()[1] - 0.4, 0])
        br = VGroup(Line([g.xk(0) - 0.6, 1.75, 0], [g.xk(3) + 0.6, 1.75, 0], color=GREY_B, stroke_width=2),
                    label(r"Prinner: \ melody 6-5-4-3, \ bass 4-3-2-1", font_size=24, color=TUNE).move_to([(g.xk(0) + g.xk(3)) / 2, 2.15, 0]),
                    label(r"cadence", font_size=24, color=GREY_A).move_to([(g.xk(4) + g.xk(5)) / 2, 2.15, 0]))
        with self.voiceover(
            "So give it its bass. Here is the Tune from its fifth note, A, A, G, F, F, E, E, and then D, D, C, with "
            "a Prinner's bass under the first four chords, F, E, D, C, and a cadence after it. The nursery tune "
            "turns out to speak the galant language."
        ):
            self.play(FadeIn(g), FadeIn(names), FadeIn(br))
        with self.listen(c) as snd:
            window(snd, r"the Tune as a Prinner", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_chords(snd, g, d["times"])
        self.wait(0.3)
        self.clear_scene()

