from __future__ import annotations

import numpy as np

from videos.music.music61.common import *  # noqa: F403


class Evaluation(SoundScene):
    def construct(self):
        chapter(self, 8, r"Keeping score", r"When is a transcribed note right?")
        self.metrics()
        self.example()
        self.quiz()
        self.frames()
        self.keys()

    # ------------------------------------------------------------------
    def metrics(self):
        lines = VGroup(
            label(r"frame level: \ each 20 ms frame, \ each pitch: \ sounding or not?", font_size=20, color=WHITE),
            label(r"note level: \ a reported note is right if its pitch matches and its onset is within 50 ms", font_size=20, color=WHITE),
            label(r"with offsets: \ its end must also be within 50 ms or 20\% of the note's length", font_size=20, color=WHITE),
            MathTex(r"P = \frac{\text{right}}{\text{reported}}, \quad R = \frac{\text{right}}{\text{played}}, \quad F = \frac{2PR}{P + R}", font_size=36, color=TUNE),
            label(r"each played note matched at most once: \ the conventions of mir\_eval \ (Raffel et al., \ 2014)", font_size=17, color=GREY_A),
        ).arrange(DOWN, buff=0.38)
        head = label(r"three ways to count", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How should a transcription be scored? <bookmark mark='a'/> Frame by frame: for each twenty milliseconds and each pitch, sounding or not. <bookmark mark='b'/> Note by note: a reported note is right if its pitch matches a played note and its onset is within fifty milliseconds. <bookmark mark='c'/> Stricter still, its end must match too. <bookmark mark='d'/> Precision is the share of reported notes that are right; recall, the share of played notes found; F, their harmonic mean. <bookmark mark='e'/> Each played note can be matched only once, using maximum-cardinality one-to-one matching, as mir_eval does; our implementation matches exact integer MIDI pitch and uses the stated time tolerances."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def example(self):
        d = load("net")
        truth, est = d["truth"], d["est"]
        dur = 6.0
        w, h = 10.5, 3.6
        frame = Rectangle(width=w, height=h, stroke_color=GREY_D, stroke_width=1).move_to(DOWN * 0.2)
        x0, y0 = frame.get_left()[0], frame.get_bottom()[1]
        ph = h / 37

        def box(m, a, b, **kw):
            return Rectangle(width=max(0.04, w * (b - a) / dur), height=ph * 0.85, **kw).move_to([x0 + w * (a + b) / 2 / dur, y0 + ph * (m - 48 + 0.5), 0])
        used = [False] * len(est)
        right = set()
        for m, a, b in truth:
            for j, (m2, a2, b2) in enumerate(est):
                if not used[j] and m2 == m and abs(a2 - a) <= 0.05:
                    used[j] = True
                    right.add(j)
                    break
        tb = VGroup(*[box(m, a, b, stroke_color=WHITE, stroke_width=1.5, fill_opacity=0) for m, a, b in truth])
        eb = VGroup(*[box(m, a, b, stroke_width=0, fill_color=TUNE if j in right else EAR, fill_opacity=0.75) for j, (m, a, b) in enumerate(est)])
        ps = d["piece_scores"]
        note = label(rf"white: \ played; \ gold: \ reported and right; \ red: \ reported and wrong. \ P = {ps['precision']:.2f}, \ R = {ps['recall']:.2f}, \ F = {ps['f']:.2f}",
                     font_size=16, color=GREY_A).to_edge(DOWN, buff=0.3)
        head = label(r"the organ piece, \ scored", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the organ piece you just heard, scored. <bookmark mark='a'/> White boxes: the notes played. "
            "<bookmark mark='b'/> Gold: the network's notes that match one. Red: its notes that match nothing, often an octave "
            "away from a real note, or a real note broken in two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame))
            vo.wait_until("a")
            self.play(Create(tb), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(eb), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frames(self):
        m = load("net")["scores"]
        inst = (("piano", r"piano", TUNE), ("harp", r"harp", BLUE), ("organ", r"organ", EAR), ("strings", r"bowed strings", GREY_B))
        g = VGroup()
        for k, name, col in inst:
            g.add(VGroup(label(name, font_size=20, color=col), label(f"{m[k]['frame_f']:.2f}", font_size=22, color=WHITE), label(f"{m[k]['f']:.2f}", font_size=22, color=WHITE)))
        g.arrange(DOWN, buff=0.45)
        for r in g:
            r[0].set_x(-3.0)
            r[1].set_x(0.8)
            r[2].set_x(3.6)
        top = VGroup(label(r"frame F", font_size=17, color=GREY_A).move_to([0.8, g.get_top()[1] + 0.5, 0]),
                     label(r"note F", font_size=17, color=GREY_A).move_to([3.6, g.get_top()[1] + 0.5, 0]))
        head = label(r"the network, \ counted two ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The same network, counted two ways, on all four instruments. <bookmark mark='a'/> Frame by frame. "
            "<bookmark mark='b'/> And note by note. The two disagree because they punish different things: a note held too "
            "short costs frames but not the note, while a note broken in two costs a note but few frames. Always report which "
            "you counted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*[r[0] for r in g])))
            vo.wait_until("a")
            self.play(FadeIn(top[0]), FadeIn(VGroup(*[r[1] for r in g])))
            vo.wait_until("b")
            self.play(FadeIn(top[1]), FadeIn(VGroup(*[r[2] for r in g])))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def keys(self):
        items = [
            (r"a metric is a choice: \ 50 ms is generous for a drum, \ strict for a slow violin entry", WHITE),
            (r"F-measures hide which errors: \ an octave error and a missed note cost the same", WHITE),
            (r"real answer keys are made by people, \ and people disagree; \ a Disklavier, \ or Monochord, \ does not", WHITE),
            (r"a transcription that scores 0.9 can still be unreadable; \ one that scores 0.7 can be useful", TUNE),
        ]
        rows_scene(self, r"what the numbers miss", items,
                   "The numbers are useful, and limited. <bookmark mark='b'/> A metric is a choice: fifty milliseconds is generous "
                   "for a drum and strict for a slow violin entry. <bookmark mark='c'/> An F-measure hides which errors were made: an "
                   "octave error and a missed note cost the same. <bookmark mark='d'/> Real answer keys are made by people, and people "
                   "disagree; instrument-linked or synthetic MIDI provides precise event commands, but acoustic alignment, pedal and audible offsets still need interpretation. <bookmark mark='e'/> And a transcription that scores nine tenths "
                   "can still be unreadable, while one that scores seven tenths can be useful. Readability is Chapter 9's subject.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("scoreheard")
        c = clip("scoreheard.two")
        card = listen_card(r"Two transcriptions of the Tune with its chords, \ re-played. \ They score almost the same. \ One is missing notes; \ one has notes in the wrong octave. \ Which is which?", width=9.6)
        with self.voiceover("Your turn. Two transcriptions of the Tune with its chords, played back. They score almost the same. One is missing notes; the other has some notes in the wrong octave. Which is which?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two transcriptions", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        a, b = d["a"], d["b"]
        res = VGroup(label(rf"the first is missing {d['dropped']} of {d['n']} notes: \ precision {a['precision']:.2f}, \ recall {a['recall']:.2f}, \ F {a['f']:.2f}", font_size=17, color=TUNE),
                     label(rf"the second has {d['moved']} notes an octave out: \ precision {b['precision']:.2f}, \ recall {b['recall']:.2f}, \ F {b['f']:.2f}", font_size=17, color=EAR)).arrange(DOWN, buff=0.25).move_to(DOWN * 1.4)
        with self.voiceover(
            f"The first is missing {say(d['dropped'])} of the {say(d['n'])} notes; the second has {say(d['moved'])} notes an "
            f"octave out. Their F-measures are {say(a['f'], 2)} and {say(b['f'], 2)}. To a listener, a missing note leaves a "
            "gap that the harmony often covers, while a note in the wrong octave can break the melody's line. Which is worse "
            "depends on what the transcription is for, and one number cannot say."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()
