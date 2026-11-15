from __future__ import annotations

import numpy as np

from videos.music.music42.common import *  # noqa: F403

SAID = {"motive": "the motive", "invert": "inverted, every interval turned upside down",
        "retrograde": "in retrograde, backwards", "augment": "augmented, every note twice as long",
        "diminish": "diminished, twice as fast", "fragment": "fragmented, its first two notes",
        "expand an interval": "with its leap widened from a fifth to a sixth", "new rhythm": "in a new rhythm, even notes",
        "embellish": "embellished, its leap filled with a run"}


class Motive(SoundScene):
    def construct(self):
        chapter(self, 1, r"The motive and its operations", r"What can a composer do with four notes?")
        self.define()
        self.ops()
        self.quiz()
        self.diatonic()
        self.famous()

    # ------------------------------------------------------------------
    def define(self):
        d = load("motive")
        mot = d["figures"]["motive"]
        g = scored(mot, None, width=4.0, height=1.6, lo=58, hi=70).move_to(LEFT * 3.4 + UP * 0.2)
        names = VGroup(*[label(t, font_size=20, color=WHITE).next_to(b, UP, buff=0.12) for t, b in zip(("E", "D", "C", "G"), g.roll.notes)])
        side = VGroup(label(r"our motive: \ four notes, \ two beats of pitch and rhythm", font_size=20, color=TUNE),
                      label(r"its intervals: \ down a step, \ down a step, \ up a fifth", font_size=20, color=WHITE),
                      label(r"its rhythm: \ short, \ short, \ long, \ longer", font_size=20, color=WHITE),
                      label(r"Schoenberg: \ a motive is a unit of intervals and rhythm \ `combined to produce a memorable shape'", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 2.6 + UP * 0.2)
        head = label(r"the motive", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Composition textbooks start small. <bookmark mark='a'/> Here is a motive of ours: four notes, E, D, C, and then "
            "up a fifth to G. <bookmark mark='b'/> Its intervals are down a step, down a step, up a fifth; its rhythm is "
            "short, short, long, longer. <bookmark mark='c'/> Arnold Schoenberg, whose Fundamentals of Musical Composition "
            "is still used to teach this, defined a motive as intervals and rhythm combined to produce a memorable shape."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(names), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ops(self):
        d = load("motive")
        c = clip("motive.ops")
        figs = d["figures"]
        cells = VGroup()
        for name, f in figs.items():
            r = scored(f, None, width=2.8, height=0.95, lo=56, hi=72, bars=2 if name == "augment" else 1, beats=4.0)
            cells.add(VGroup(r, label(name, font_size=16, color=TUNE if name == "motive" else WHITE)).arrange(DOWN, buff=0.15))
        cells.arrange_in_grid(rows=3, cols=3, buff=(0.6, 0.45)).move_to(DOWN * 0.15)
        head = label(r"the operations, \ all within the scale", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What can be done to it? The classical repertoire uses a short list of operations, here kept within the scale. "
            "Hear the motive and then eight of them in turn: turned upside down; played backwards; augmented, twice as slow; "
            "diminished, twice as fast; cut to a fragment; with its leap widened; in a new rhythm; and embellished."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        keys = list(figs)
        with self.listen(c) as snd:
            window(snd, r"the motive, \ then eight operations", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
                flash(snd, cells[i][0].roll.notes, [st[k] + n[1] * 0.4 for n in figs[k]], hot=WHITE, base=TUNE)
        with self.voiceover(
            "Each keeps something and changes something. Inversion keeps the rhythm and the sizes of the steps, and flips "
            "their direction. Retrograde keeps everything and reverses time. Augmentation and diminution keep the shape and "
            "change the speed. A fragment keeps a piece, small enough to repeat and sequence. And the last three change one "
            "feature while keeping the rest recognisable."
        ):
            self.play(cells[0].animate.set_opacity(1.0))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("quiz")
        c = clip("quiz.two")
        card = listen_card(r"The motive, \ then a changed version. \ Is the second the motive turned upside down, \ "
                           r"or played backwards?", width=10.4)
        with self.voiceover(
            "A question for your ears. The motive, and then a changed version of it. Is the second the motive turned "
            "upside down, or played backwards?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        a = scored(d["motive"], None, width=3.6, height=1.3, lo=56, hi=72)
        b = scored(d["changed"], None, width=3.6, height=1.3, lo=56, hi=72)
        b.roll.set_opacity(0)
        pair = VGroup(VGroup(a, label(r"the motive", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.25),
                      VGroup(b, label(r"?", font_size=26, color=EAR)).arrange(DOWN, buff=0.25)).arrange(RIGHT, buff=1.4).move_to(UP * 0.5)
        self.play(FadeOut(card), FadeIn(pair))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"motive, \ then changed", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, a.roll.notes, [st["motive"] + n[1] * 0.45 for n in d["motive"]], hot=WHITE, base=TUNE)
            pulse(snd, pair[1], st["changed"], c.duration, buff=0.1)
        up = scored(d["upside"], None, width=3.6, height=1.3, lo=56, hi=72, color=GREY_B)
        upg = VGroup(up, label(r"upside down \ (not played)", font_size=18, color=GREY_B)).arrange(DOWN, buff=0.25).next_to(pair, DOWN, buff=0.5)
        with self.voiceover(
            "Backwards. The long G came first, then the leap down a fifth, then C, D, E rising: the same notes in reverse "
            "order. Turned upside down, it would have started on E, risen by steps to G, and leapt down to C. Retrograde is "
            "the harder of the two to hear, because a motive's identity lives mostly in its rhythm and its beginning, and "
            "retrograde changes both."
        ):
            self.play(b.roll.animate.set_opacity(1), FadeIn(upg))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def diatonic(self):
        items = [
            (r"inside a key, \ operations are `diatonic': \ steps counted on the scale, \ not in semitones", WHITE),
            (r"the motive's E \ D \ C \ G \ moved up a step is F \ E \ D \ A: \ the same steps, \ some intervals a semitone different", WHITE),
            (r"that keeps every version in the key, \ and makes the versions sound related rather than identical", WHITE),
            (r"Part 20's tonal answer in a fugue is the same compromise, \ made at one interval", TUNE),
            (r"in our code \ (\texttt{composer.py}), \ every operation is a function from melodies to melodies", GREY_A),
        ]
        rows_scene(self, r"operations inside a key", items,
                   "One detail matters in practice. <bookmark mark='b'/> Inside a key, these operations are diatonic: steps are "
                   "counted on the scale, not in semitones. <bookmark mark='c'/> Our motive moved up a step becomes F, E, D, A: "
                   "the same steps on the scale, though some intervals change by a semitone. <bookmark mark='d'/> That keeps "
                   "every version in the key, and makes the versions sound related rather than identical. "
                   "<bookmark mark='e'/> Part 20's tonal answer in a fugue is the same compromise, made at one interval. "
                   "<bookmark mark='f'/> In our code, every operation is a function from melodies to melodies, which is what "
                   "lets a program search among them.", marks="cdef")

    # ------------------------------------------------------------------
    def famous(self):
        items = [
            (r"Beethoven's Fifth Symphony \ (1808): \ four notes, \ three short and a long, \ carry the first movement", WHITE),
            (r"Bach's fugue subjects \ (Part 20): \ one line, \ inverted, \ augmented, \ in stretto", WHITE),
            (r"Wagner's leitmotifs \ (Part 27): \ a motive tied to a character, \ transformed with the drama", WHITE),
            (r"film and game scores \ (Part 44) \ still work this way", TUNE),
            (r"chapter 2: \ how a whole phrase grows from a motive", GREY_A),
        ]
        rows_scene(self, r"motives that carry pieces", items,
                   "Motives carry whole pieces. <bookmark mark='b'/> In Beethoven's Fifth Symphony of 1808, four notes, three "
                   "short and a long, carry the entire first movement. <bookmark mark='c'/> Bach's fugue subjects, from Part "
                   "20, are one line, inverted, augmented and overlapped in stretto. <bookmark mark='d'/> Wagner's leitmotifs, "
                   "from Part 27, tie a motive to a character and transform it with the drama, <bookmark mark='e'/> and film "
                   "and game scores, Part 44's subject, still work this way. <bookmark mark='f'/> Chapter two shows how a whole "
                   "phrase grows from a motive.", marks="cdef")
