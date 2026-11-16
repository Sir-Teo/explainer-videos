from __future__ import annotations

import numpy as np

from videos.music.music25.common import *  # noqa: F403

ORDER = ["allemande", "courante", "sarabande", "gigue"]


class Suite(SoundScene):
    def construct(self):
        chapter(self, 5, r"The suite", r"What did the dances leave behind?")
        self.dances()
        self.heard()
        self.binary()

    # ------------------------------------------------------------------
    def dances(self):
        items = [
            (r"a suite: \ a set of stylized dances in one key, \ each in two halves, \ each half repeated", WHITE),
            (r"allemande: \ German, \ moderate, \ in four, \ starting with a short upbeat", WHITE),
            (r"courante: \ French, \ in three, \ wavering between 3/2 and 6/4", WHITE),
            (r"sarabande: \ Spanish in origin, \ slow, \ in three, \ the weight on the second beat", WHITE),
            (r"gigue: \ English or Irish jig, \ fast, \ in 6/8 or 12/8, \ often in imitation", TUNE),
        ]
        rows_scene(self, r"four dances", items,
                   "Instrumental music took its forms from the dance. <bookmark mark='b'/> A suite is a set of stylized "
                   "dances in one key, each in two halves, each half repeated, Part 21's binary form. "
                   "<bookmark mark='c'/> Its core, by Bach's time, was four dances from four countries: the allemande, "
                   "moderate, in four, with a short upbeat; <bookmark mark='d'/> the courante, in three, wavering between "
                   "three beats and two; <bookmark mark='e'/> the sarabande, slow and grave, its weight on the second beat "
                   "of the bar; <bookmark mark='f'/> and the gigue, fast, in compound time, often beginning in imitation. "
                   "Bach’s suites are primarily stylized instrumental works rather than straightforward dance accompaniments; the dances had become rhythms, and the rhythms had become characters.", marks="cdef")

    # ------------------------------------------------------------------
    def heard(self):
        d = load("dances")
        c = clip("dances.four")
        rows_ = VGroup()
        rolls = []
        for k in ORDER:
            info = d["dances"][k]
            tot = max(n[1] + n[2] for n in info["notes"])
            g = mroll(info["notes"], width=6.4, height=0.7, lo=70, hi=82, total=12.0, bar_h=0.12)
            t = label(rf"{k}: \ {info['metre']}", font_size=21, color=TUNE).next_to(g, LEFT, buff=0.4)
            rows_.add(VGroup(t, g))
            rolls.append(g)
        rows_.arrange(DOWN, buff=0.4, aligned_edge=RIGHT).move_to(DOWN * 0.1 + RIGHT * 0.6)
        head = label(r"the Tune's first phrase in four dance rhythms", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Hear the characters on one melody: the Tune's first phrase as an allemande, a courante, a sarabande and a "
            "gigue, the pitches the same and only the rhythm and tempo changed. Listen especially for the sarabande's "
            "long second beat."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"allemande, \ courante, \ sarabande, \ gigue", detail=r"Part 1's string on Part 7's soundboard", corner=DL, tag_corner=DR)
            for i, k in enumerate(ORDER):
                st = d["starts"][k]
                info = d["dances"][k]
                flash(snd, rolls[i].notes, [st + n[1] * info["unit"] for n in info["notes"]], hot=WHITE, base=TUNE)
                end = d["starts"][ORDER[i + 1]] - 0.4 if i < 3 else c.duration
                pulse(snd, rows_[i][0], st, end, buff=0.06)
        with self.voiceover(
            'The same seven notes, four characters. That is what the doctrine of the affections meant in practice: a rhythm and a tempo carry a feeling, and familiar dance conventions could suggest character; that does not assign every listener one fixed emotion.'
        ):
            self.play(Indicate(rows_[2][0], color=WHITE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def binary(self):
        items = [
            (r"each dance: \ two halves, \ each repeated: \ $\|{:}$ A ${:}\|\,\|{:}$ B ${:}\|$", WHITE),
            (r"the first half travels from the tonic to the dominant \ (or, \ in minor, \ the relative major)", WHITE),
            (r"the second half travels back, \ often through other keys", WHITE),
            (r"the end of the second half often echoes the end of the first, \ now at home", TUNE),
            (r"the seed of the sonata form of Parts 21 and 26", GREY_A),
        ]
        rows_scene(self, r"the binary plan", items,
                   "The dances share one plan. <bookmark mark='b'/> Each has two halves, and each half is repeated. <bookmark mark='c'/> The first half moves from the tonic to the dominant, or in a minor key to the relative major, and stops there. <bookmark mark='d'/> The second half travels back home, often through other keys on the way. <bookmark mark='e'/> And the end of the second half often repeats the end of the first, now in the home key, so that what was a cadence away from home becomes a cadence at home. <bookmark mark='f'/> Enlarge that plan, give the return a theme of its own, and you have the sonata form of Parts 21 and 26.", marks="cdef")
