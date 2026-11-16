from __future__ import annotations

import numpy as np

from videos.music.music25.common import *  # noqa: F403

MODE_NAME = {"ion": r"Ionian \ (major)", "aeo": r"Aeolian \ (minor)", "dor": r"Dorian", "mix": r"Mixolydian", "phr": r"Phrygian"}


class Keys(SoundScene):
    def construct(self):
        chapter(self, 8, r"From modes to keys", r"How did eight modes become two keys?", extra=((1722, r"Rameau's \textit{Traité}"),))
        self.census()
        self.rameau()
        self.circle()
        self.fundamental()

    # ------------------------------------------------------------------
    def census(self):
        d = load("modes")
        pal = d["palestrina"]
        order = ["dor", "mix", "ion", "aeo", "phr"]
        tagged = sum(pal[k] for k in order)
        bars = columns([100 * pal[k] / tagged for k in order], [MODE_NAME[k] for k in order], width=6.6, height=2.6, color=TUNE, fmt="{:.0f}", font_size=17)
        bars.move_to(LEFT * 2.9 + DOWN * 0.4)
        t = label(rf"Palestrina's {tagged:,} Mass movements, \ by mode, \ in 100s".replace(",", "{,}"), font_size=19, color=GREY_A).next_to(bars, UP, buff=0.35)
        b = d["bach"]
        side = VGroup(*[label(s, font_size=23, color=c_) for s, c_ in (
            (rf"Ionian and Aeolian together: \ {100 * (pal['ion'] + pal['aeo']) / tagged:.0f} in 100", WHITE),
            (rf"Bach's chorales: \ {b.get('major', 0)} major, \ {b.get('minor', 0)} minor", TUNE),
            (r"even Bach's harmonizations of old modal tunes are labelled major or minor", WHITE),
            (r"the leading tone, \ raised everywhere by \textit{musica ficta}, \ made the other modes converge", EAR))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.6))
        side.move_to(RIGHT * 3.8 + DOWN * 0.2)
        with self.voiceover(
            "How did eight modes become two keys? Count. The Humdrum encodings of Palestrina's Masses label each movement "
            f"with its mode. <bookmark mark='a'/> Of {say(tagged)} movements, the Ionian and Aeolian, Glarean's new modes, "
            f"our major and minor, make up {say(round(100 * (pal['ion'] + pal['aeo']) / tagged))} in a hundred; the old "
            f"Dorian and Mixolydian still lead. <bookmark mark='b'/> A century and a half later, Bach's chorales are "
            f"labelled {say(b.get('major', 0))} major and {say(b.get('minor', 0))} minor, and nothing else, <bookmark mark='c'/> "
            "even when the melody Bach harmonized was an old modal tune. <bookmark mark='d'/> One mechanism was the "
            "leading tone: once singers often raised a cadential leading note in relevant contexts, by the rules of musica ficta from Part 23, "
            "Dorian and Mixolydian cadences sounded like minor and major ones, and several interacting changes supported major-minor practice; modern editorial labels are not a direct historical census of listeners’ concepts."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rameau(self):
        items = [
            (r"1722: \ Jean-Philippe Rameau, \ \textit{Treatise on Harmony}", WHITE),
            (r"chords, \ not intervals: \ a chord and its inversions are the same chord", WHITE),
            (r"the fundamental bass: \ the roots, \ moving mostly by fifths \ (Part 18 counted 39 in 100 falling)", WHITE),
            (r"the tonic, \ dominant and subdominant: \ his names for the functions of Part 15", TUNE),
            (r"he grounded it in the harmonic series \ (Part 3): \ the major triad given by nature", GREY_A),
        ]
        rows_scene(self, r"the theory of keys", items,
                   "The theory caught up in 1722, the year of the Well-Tempered Clavier. <bookmark mark='b'/> Jean-Philippe Rameau's Treatise on Harmony treated chords, not intervals, as the units of music: a chord and its inversions are one chord. <bookmark mark='c'/> Beneath the real bass he traced a fundamental bass of chord roots, moving mostly by fifths, as Part 18 counted in Bach's chorales. <bookmark mark='d'/> He named the tonic, the dominant and the subdominant, the functions of Part 15. <bookmark mark='e'/> And he grounded the whole system in the harmonic series of Part 3, where the major triad appears among the low partials of an ideal harmonic complex; many musical sounds are inharmonic: harmony given by nature, he argued, though the minor triad gave him more trouble.")

    # ------------------------------------------------------------------
    def fundamental(self):
        d = load("fundamental")
        c = clip("keys.fundamental")
        g1 = voices_roll([d["soprano"], d["bass"]], width=5.4, height=2.8, colors=[TUNE, GREY_A], lo=30, hi=80, bar_h=0.12).move_to(LEFT * 3.3 + DOWN * 0.3)
        g2 = voices_roll([d["soprano"], d["bass"], d["fundamental"]], width=5.4, height=2.8, colors=[TUNE, GREY_A, EAR], lo=30, hi=80, bar_h=0.12).move_to(RIGHT * 3.3 + DOWN * 0.3)
        l1 = label(r"Bach's soprano and bass", font_size=21, color=GREY_A).next_to(g1, UP, buff=0.3)
        l2 = label(r"with Rameau's fundamental bass below", font_size=21, color=EAR).next_to(g2, UP, buff=0.3)
        mv = d["motions"]
        fifths = mv.get("up a fourth (down a fifth)", 0) + mv.get("up a fifth", 0)
        cap = label(rf"the roots under the first phrase of chorale {d['name']}: \ {fifths} of {sum(mv.values())} moves are by a fifth", font_size=21, color=WHITE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is Rameau's idea made audible. The first phrase of one of Bach's chorales, soprano and bass, and then "
            "the same with Rameau's fundamental bass added below, the root of every chord on the beat, played on a low "
            "organ. Listen to the added line: it leaps by fourths and fifths where Bach's real bass moves smoothly."
        ):
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(l1), FadeIn(l2), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Bach's bass, \ then the fundamental bass", detail=r"harpsichord and organ", kind="synthesized", corner=UL, tag_corner=UR)
            flash_voices(snd, g1, [d["soprano"], d["bass"]], d["starts"]["real"], d["unit"], colors=[TUNE, GREY_A])
            flash_voices(snd, g2, [d["soprano"], d["bass"], d["fundamental"]], d["starts"]["fundamental"], d["unit"], colors=[TUNE, GREY_A, EAR])
            pulse(snd, l1, d["starts"]["real"], d["starts"]["fundamental"] - 0.5, buff=0.08)
            pulse(snd, l2, d["starts"]["fundamental"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def circle(self):
        items = [
            (r"1711: \ Johann David Heinichen draws a musical circle of all 24 keys", WHITE),
            (r"major keys round the circle of fifths, \ each beside its relative minor", WHITE),
            (r"a map for modulation: \ neighbours on the circle share most of their notes \ (Part 15)", WHITE),
            (r"possible only once every key is playable: \ a consequence of well temperament", TUNE),
            (r"Part 19's pathfinder walks the same map", GREY_A),
        ]
        rows_scene(self, r"the circle of keys", items,
                   "With every key usable, theorists began to draw maps of them. <bookmark mark='b'/> In 1711 Johann David Heinichen, a Dresden composer, drew a musical circle of all twenty-four keys, <bookmark mark='c'/> the major keys round the circle of fifths, each next to its relative minor. <bookmark mark='d'/> It is a map for modulation: neighbouring keys share most of their notes, as Part 15 measured. <bookmark mark='e'/> A conceptual key map can also describe relationships beyond one instrument’s practical tuning, which is what the new temperaments allowed. <bookmark mark='f'/> Part 19's pathfinder walks the same map with chromatic doors added.", marks="cdef")
