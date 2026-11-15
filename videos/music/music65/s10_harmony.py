from __future__ import annotations

import numpy as np

from videos.music.music65.common import *  # noqa: F403


class Harmony(SoundScene):
    def construct(self):
        chapter(self, 9, r"Four parts", r"How does a machine write all four voices of a chorale?")
        self.deepbach()
        self.ours()
        self.heard()
        self.beside_bach()

    # ------------------------------------------------------------------
    def deepbach(self):
        items = [
            (r"DeepBach \ (Hadjeres, \ Pachet and Nielsen, \ 2017): \ four voices on a grid of sixteenths", WHITE),
            (r"a network predicts each voice's note at one moment from everything around it, \ past and future, \ in all four voices", WHITE),
            (r"to compose: \ start from noise, \ then resample one note at a time, \ again and again \ (Gibbs sampling)", WHITE),
            (r"any note can be fixed in advance: \ a given melody, \ a cadence, \ a bass, \ and the rest fills in around it", WHITE),
            (r"in its listening test, \ many listeners took its chorales for Bach's", TUNE),
        ]
        rows_scene(self, r"DeepBach", items,
                   "A chorale has four voices, and a machine that writes them all must keep each voice singable and every chord "
                   "right. <bookmark mark='b'/> DeepBach, from Gaëtan Hadjeres, François Pachet and Frank Nielsen in 2017, puts the "
                   "four voices on a grid of sixteenths. <bookmark mark='c'/> A network learns to predict each voice's note at "
                   "one moment from everything around it, past and future, in all four voices. <bookmark mark='d'/> To compose, "
                   "start from random notes and resample one note at a time, again and again: Gibbs sampling. "
                   "<bookmark mark='e'/> Any note can be fixed in advance, a melody, a cadence, a bass, and the rest fills in "
                   "around it. <bookmark mark='f'/> In its listening test, many listeners took its chorales for Bach's.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def ours(self):
        items = [
            (r"Monochord does it in two steps: \ the transformer writes the tune, \ Part 17's harmonizer the other three voices", WHITE),
            (r"Part 17: \ chords learnt from Bach's chorales, \ voicings chosen by dynamic programming under the voice-leading rules", WHITE),
            (r"a pipeline, \ not a joint model: \ the tune cannot bend to suit the harmony", WHITE),
            (r"but every chord can be checked: \ ranges, \ spacing, \ parallel fifths and octaves", TUNE),
        ]
        rows_scene(self, r"Monochord's way", items,
                   "Monochord does it in two steps. <bookmark mark='b'/> The transformer writes the tune, and Part 17's "
                   "harmonizer writes the other three voices. <bookmark mark='c'/> Part 17's harmonizer chooses chords learnt from "
                   "Bach's chorales and voicings by dynamic programming under the rules of voice leading. <bookmark mark='d'/> It "
                   "is a pipeline, not a joint model: the tune cannot bend to suit the harmony, as Bach's tunes sometimes bend. "
                   "<bookmark mark='e'/> But every chord it writes can be checked: ranges, spacing, parallel fifths and octaves.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def heard(self):
        d = load("harmony")
        c = clip("harmony.one")
        roll = tune_roll(d["notes"], width=11.0, height=1.5).move_to(DOWN * 0.3)
        box = choice_boxes([r"the transformer's tune, \ harmonized"], width=5.2, height=0.8, size=18).move_to(UP * 1.8)
        res = label(rf"{len(d['chords'])} chords; \ parallel fifths or octaves: \ {d['parallels']}; \ the tune's longest copied run: \ {d['copy']['length']} notes",
                    font_size=17, color=TUNE).to_edge(DOWN, buff=0.45)
        head = label(r"a machine's chorale", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is a tune the transformer wrote, harmonized in four parts by Part 17: the first of its draws that stayed in "
            f"C major and that Part 17 could harmonize; {say(d['skipped'])} earlier draws strayed from the key or could not "
            "be fitted."
        ):
            self.play(FadeIn(head), FadeIn(box), FadeIn(roll))
        with self.listen(c) as snd:
            window(snd, r"a machine's chorale", kind="synthesized", detail=r"the transformer; \ Part 17's harmony", corner=DL, tag_corner=DR)
            pulse(snd, box, 0.0, c.duration, buff=0.06)
        with self.voiceover(
            f"{say(len(d['chords']))} chords, with {say(d['parallels'])} parallel fifths or octaves between them, and a tune "
            f"whose longest copied run is {say(d['copy']['length'])} notes. It is correct, and it is plausible. Whether it is "
            "good is a question the next chapter takes seriously."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beside_bach(self):
        d = load("bachvs17")
        c = clip("bachvs17.two")
        boxes = choice_boxes([r"Bach's harmony", r"Part 17's, \ on the same tune"], width=4.2, height=0.9, buff=0.9, size=18).move_to(UP * 0.6)
        note = label(r"the same two phrases, \ the same tune; \ Bach in his key, \ Part 17 in C", font_size=17, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(rf"{bwv(d['name'])}, \ twice", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("How good is the harmonizer? Hear a tune kept back from everything, harmonized by Bach, then by Part 17's search."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"Bach, \ then Part 17", kind="synthesized", detail=rf"{bwv(d['name'])}", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["bach"], st["ours"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["ours"], c.duration, buff=0.08)
        with self.voiceover(
            "Bach's inner voices move: passing notes, suspensions, a bass with a line of its own. Part 17's move by the beat, "
            "one chord to each, correct and plain. Part 17 measured the gap: its chords agree with Bach's on many beats, and "
            "its texture is simpler everywhere. A joint model like DeepBach learns the decorations too."
        ):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()
