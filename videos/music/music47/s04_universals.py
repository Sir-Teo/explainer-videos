from __future__ import annotations

import numpy as np

from videos.music.music47.common import *  # noqa: F403

SPOKEN = {"few scale degrees": "at most seven notes to the octave", "small intervals": "mostly small intervals",
          "descending or arched": "phrases that fall or arch", "few durations": "a few note lengths",
          "on a beat": "a beat", "motifs": "motifs that come back"}


class Universals(SoundScene):
    def construct(self):
        chapter(self, 3, r"Statistical universals", r"Which features of musical sound are shared?")
        self.savage()
        self.checklist()
        self.limits()
        self.network()

    # ------------------------------------------------------------------
    def savage(self):
        items = [
            (r"Patrick Savage and colleagues \ (2015): \ 304 recordings sampled across nine regions of the world", WHITE),
            (r"each coded for 32 features: \ pitch, \ rhythm, \ form, \ instruments, \ voice, \ who performs", WHITE),
            (r"no feature was found in every recording: \ no absolute universals", WHITE),
            (r"but many features were common in every region: \ statistical universals", TUNE),
            (r"to count as one, \ a feature had to hold up after allowing for related societies' shared descent", GREY_A),
        ]
        rows_scene(self, r"304 recordings", items,
                   "The most careful survey of the sound itself is by Patrick Savage and colleagues, in 2015. "
                   "<bookmark mark='b'/> They took 304 recordings sampled across nine regions of the world, and coded each for "
                   "thirty-two features: of pitch, rhythm, form, instruments, voice, and who performs. <bookmark mark='c'/> No "
                   "feature turned up in every recording: there were no absolute universals. <bookmark mark='d'/> But many were "
                   "common in every region: statistical universals. <bookmark mark='e'/> To count, a feature had to hold up "
                   "after allowing for the fact that related societies share descent, the way related species share traits.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def checklist(self):
        d = load("universals")
        feats = d["features"]
        share = d["share"]
        bars = VGroup()
        x0, W = -1.2, 6.0
        for i, f in enumerate(feats):
            y = 1.9 - 0.68 * i
            w = W * share[f]
            bars.add(VGroup(label(f, font_size=19, color=WHITE).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT),
                            Rectangle(width=W, height=0.4, stroke_color=GREY_B, stroke_width=1, fill_opacity=0).move_to([x0 + W / 2, y, 0]),
                            Rectangle(width=max(w, 0.02), height=0.4, stroke_width=0, fill_color=TUNE, fill_opacity=0.85).move_to([x0 + w / 2, y, 0]),
                            label(f"{100 * share[f]:.0f}\\%", font_size=18, color=WHITE).move_to([x0 + W + 0.45, y, 0])))
        head = label(rf"six of Savage's features, \ checked on the series' {d['tunes']} tunes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"bar: \ the share of tunes that have the feature \ (each feature's test is in \texttt{origins.universals})", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.45)
        f = feats
        fails = d["fails"]
        with self.voiceover(
            f"We can check six of Savage's features on the series' own corpus of {say(d['tunes'])} tunes. "
            f"<bookmark mark='a'/> At most seven notes to the octave: {say(100 * share[f[0]])} per cent; only "
            f"{say(len(fails[f[0]]))} tunes, Greensleeves and Deck the Halls, add a chromatic note. <bookmark mark='b'/> Mostly "
            f"small intervals: every tune. <bookmark mark='c'/> Phrases that fall or arch: {say(100 * share[f[2]])} per cent. "
            f"<bookmark mark='d'/> Two note lengths covering three notes in four: {say(100 * share[f[3]])} per cent. "
            "<bookmark mark='e'/> A beat: every tune, but only because written music assumes one; Savage's coders had to "
            f"listen for it. <bookmark mark='f'/> And motifs that come back: {say(100 * share[f[5]])} per cent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(VGroup(*[VGroup(b[0], b[1]) for b in bars]).copy().set_opacity(0.3)))
            for mark, b in zip("abcdef", bars):
                vo.wait_until(mark)
                self.play(FadeIn(b))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        d = load("universals")
        items = [
            (rf"these {d['tunes']} tunes come mostly from one tradition: \ Europe and the Americas, \ with a few from elsewhere", WHITE),
            (r"a feature common here says nothing about the world: \ that is why Savage sampled every region", WHITE),
            (r"and our tests are written for notation, \ which already assumes discrete pitches and a beat", WHITE),
            (r"what the check does show: \ each feature can be stated precisely enough to count", TUNE),
            (r"a universal is a claim about a sample: \ say which sample, \ and how features were coded", GREY_A),
        ]
        rows_scene(self, r"what our check cannot show", items,
                   "But be careful what that shows. <bookmark mark='b'/> These tunes come mostly from one tradition, Europe and "
                   "the Americas, with a few from elsewhere. <bookmark mark='c'/> A feature common here says nothing about the "
                   "world; that is why Savage sampled every region. <bookmark mark='d'/> And our tests are written for "
                   "notation, which already assumes discrete pitches and a beat. <bookmark mark='e'/> What the check does show "
                   "is that each feature can be stated precisely enough to count. <bookmark mark='f'/> A universal is a claim "
                   "about a sample: say which sample, and how the features were coded.", marks="bcdef")

    # ------------------------------------------------------------------
    def network(self):
        items = [
            (r"Savage's common features include discrete pitches, \ scales of seven or fewer notes, \ small intervals and falling or arched phrases", WHITE),
            (r"a steady beat, \ divided in two or three, \ few note lengths, \ short phrases and repeated motifs", WHITE),
            (r"and features of use: \ singing, \ instruments, \ dancing, \ and performing in groups", WHITE),
            (r"many of them travel together, \ in a cluster around a beat and group performance", TUNE),
            (r"Savage's reading: \ shared music may be for coordinating people, \ chapter 11 returns to this", GREY_A),
        ]
        rows_scene(self, r"features that travel together", items,
                   "Savage's common features include discrete pitches, scales of seven or fewer notes, small intervals, and "
                   "phrases that fall or arch. <bookmark mark='b'/> A steady beat, divided in two or three, few note lengths, "
                   "short phrases and repeated motifs. <bookmark mark='c'/> And features of use: singing, instruments, dancing, "
                   "and performing in groups. <bookmark mark='d'/> Many of them travel together, in a cluster around a beat and "
                   "group performance. <bookmark mark='e'/> Savage's reading was that shared music may exist for coordinating "
                   "people; chapter eleven returns to this.", marks="bcde")
