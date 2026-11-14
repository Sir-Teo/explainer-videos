from __future__ import annotations

import numpy as np

from videos.music.music15.common import *  # noqa: F403


class Minor(SoundScene):
    def construct(self):
        chapter(self, 10, r"Minor, \ and neither", r"What about the other twelve keys?")
        self.three()
        self.dominant()
        self.neither()

    # ------------------------------------------------------------------
    def three(self):
        d = load("minor")
        c = clip("minor.three")
        rolls = VGroup(*[roll(d[k], d["beats"], width=3.7, height=2.4, lo=-4, hi=10, lines=(0,), color=col) for k, col in (("major", TUNE), ("parallel", EAR), ("relative", BLUE))]).arrange(RIGHT, buff=0.45).move_to(UP * 0.5)
        tags = VGroup(*[label(t, font_size=26, color=col).next_to(r, UP, buff=0.2) for t, col, r in zip((r"C major", r"C minor: \ the parallel", r"A minor: \ the relative"), (TUNE, EAR, BLUE), rolls)])
        with self.voiceover(
            "Every major key has two minor keys close to it, and they are close in different ways. Here "
            "is the Tune's first phrase in C major; then in C minor, the parallel key, with the same "
            "home note; then in A minor, the relative key, with the same notes."
        ):
            self.play(FadeIn(rolls), FadeIn(tags))
        keys3 = ("major", "parallel", "relative")
        with self.listen(c) as snd:
            window(snd, r"major, \ parallel, \ relative", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys3):
                sing(snd, rolls[i], d["times"][k], hot=WHITE, base=(TUNE, EAR, BLUE)[i])
                pulse(snd, tags[i], d["starts"][k], d["starts"][keys3[i + 1]] - 0.5 if i < 2 else c.duration, buff=0.1)
        facts = VGroup(label(rf"C major and C minor: \ {d['shared']['parallel']} notes shared; \ the same home", font_size=26, color=EAR),
                       label(rf"C major and A minor: \ all {d['shared']['relative']} notes shared; \ another home", font_size=26, color=BLUE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            f"The parallel minor changes three notes of the seven and keeps the home: the same place, "
            "in different weather. The relative minor keeps every note and changes the home: the same "
            "notes, seen from somewhere else. On Krumhansl's map both sit beside C major, on different "
            "sides. And it is the relative minor that key finders confuse with the major, because a "
            "list of notes cannot tell them apart; only the weights can."
        ):
            self.play(FadeIn(facts))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def neither(self):
        d = load("minor")
        odd = {o["name"]: o for o in d["odd"]}
        ds, am = odd["Drunken Sailor"], odd["Amazing Grace"]
        rows = VGroup(
            VGroup(label(r"Drunken Sailor", font_size=30, color=WHITE), label(r"home note D; \ the notes of C major", font_size=24, color=GREY_A),
                   label(rf"the key finder: \ {tex(ds['found'])}, \ {100 * ds['p']:.0f} in a hundred; \ wrong", font_size=24, color=EAR)).arrange(DOWN, buff=0.12, aligned_edge=LEFT),
            VGroup(label(r"Amazing Grace, \ Auld Lang Syne, \ Jasmine Flower", font_size=30, color=WHITE), label(r"five notes only: \ no fourth degree, \ no seventh, \ no tritone", font_size=24, color=GREY_A),
                   label(r"the key finder: \ right, \ from the weights alone", font_size=24, color=TUNE)).arrange(DOWN, buff=0.12, aligned_edge=LEFT),
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT).scale(1.2).move_to(UP * 0.6)
        cap = label(r"major and minor are two of the ways a set of notes can have a home", font_size=28, color=TUNE).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "And some tunes are in neither. <bookmark mark='a'/> The sea shanty Drunken Sailor has D for "
            "its home and the notes of the C major scale: the Dorian mode of Part 12. Ask the key "
            "finder, which knows only major and minor, and it gives a wrong answer with little "
            "confidence. The tune has a perfectly clear home; it is just not a home that the machine "
            "was taught. <bookmark mark='b'/> Pentatonic tunes are the opposite case. Amazing Grace "
            "uses five notes, with no fourth degree, no seventh, and so no tritone: the best clue is "
            "missing. Yet the key finder gets it right, from the weights alone. <bookmark mark='c'/> "
            "Major and minor are not the only keys. They are the two that European music settled on "
            "between about 1600 and 1700, out of the older modes."
        ) as vo:
            head = label(r"tunes that are in neither major nor minor", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dominant(self):
        d = load("more")["minor_dominant"]
        c = clip("minor.dominant")
        kb = keys(41, 77, width=10.0, height=1.4).move_to(DOWN * 1.2)
        tags = VGroup(VGroup(chips(["i", "iv", "v", "i"], font_size=34, buff=0.6), label(r"the fifth chord as the scale gives it: \ E, \ G, \ B", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.2),
                      VGroup(chips(["i", "iv", "V7", "i"], font_size=34, buff=0.6), label(r"with its third raised: \ E, \ G$\sharp$, \ B, \ D", font_size=24, color=EAR)).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=1.3).move_to(UP * 1.5)
        with self.voiceover(
            "A minor key has a problem that Part 12 met in melody, and here it is in harmony. The "
            "natural minor scale has no leading note: its seventh degree is a whole tone below the "
            "tonic. So its chord on five is a minor triad, with no tritone in it and no pull. Listen "
            "to a cadence in A minor with that chord; and then with its third raised a semitone, so "
            "that the dominant is major."
        ):
            self.play(FadeIn(kb), FadeIn(tags))
        keys2 = ("natural", "raised")
        with self.listen(c) as snd:
            window(snd, r"two cadences in A minor", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            light_chords(snd, kb, [ch for k in keys2 for ch in d["chords"][k]], [t for k in keys2 for t in d["times"][k]], end=c.duration)
            pulse(snd, tags[0], d["starts"]["natural"], d["starts"]["raised"] - 0.4, buff=0.12)
            pulse(snd, tags[1], d["starts"]["raised"], c.duration, buff=0.12)
        kb.clear()
        with self.voiceover(
            "The first drifts home. The second is pulled. That one borrowed note, G sharp in A minor, "
            "is why the minor scale has its harmonic form, and it is the surest sign by which you, and "
            "a key finder, can tell A minor from C major: a note that C major does not have, pointing "
            "at A."
        ):
            self.play(Indicate(tags[1], color=EAR, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()
