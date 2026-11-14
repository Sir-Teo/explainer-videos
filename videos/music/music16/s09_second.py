from __future__ import annotations

import numpy as np

from videos.music.music16.common import *  # noqa: F403


def species_scene(self, n: int, intro: str, after: str, title_note: str):
    d = load("species")[str(n)]
    c = clip(f"species.{n}")
    cfn = load("fux")["cf"]
    cf = [(p, 4.0 * k, 4.0) for k, p in enumerate(cfn)]
    line = [tuple(e) for e in d["events"]]
    st = staff_pair(line, cf, width=11.5, space=0.14).move_to(UP * 1.45)
    g = duet([line, cf], width=11.0, height=2.0, lo=58, hi=86, thick=0.12, bar=4.0).move_to(DOWN * 1.55)
    diss = {(int(p), float(a)) for p, a, dd in d["dissonances"]} | {(int(p), float(a)) for p, a, dd, iv in d.get("suspensions", [])}
    marks = [k for k, (p, a, dd) in enumerate(line) if (p, a) in diss]
    for k in marks:
        g.notes[0][k].set_fill(EAR)
    lab = label(title_note, font_size=22, color=EAR).next_to(g, DOWN, buff=0.15)
    with self.voiceover(intro):
        self.play(FadeIn(st), FadeIn(g), FadeIn(lab))
    with self.listen(c) as snd:
        window(snd, rf"species {n}", detail=r"over Fux's cantus: \ Part 7's piano", corner=DL, tag_corner=DR)
        sing_voice(snd, g.notes[0], d["times"], base=UP_C)
        sing_voice(snd, g.notes[1], d["cf_times"], base=CF_C)
    for k in marks:
        g.notes[0][k].set_fill(EAR)
    with self.voiceover(after):
        self.play(*[Indicate(g.notes[0][k], color=WHITE, scale_factor=1.6) for k in marks[:6]])
    self.wait(0.4)
    self.clear_scene()


class Second(SoundScene):
    def construct(self):
        chapter(self, 8, r"Two notes against one", r"Where may a dissonance go?")
        self.rule()
        self.hear()

    def rule(self):
        demo = duet([[(72, 0, 2), (71, 2, 2), (69, 4, 4)], [(64, 0, 4), (65, 4, 4)]], width=5.0, height=2.4, lo=60, hi=76, thick=0.16, bar=4.0).move_to(LEFT * 3.2 + DOWN * 0.3)
        tags = VGroup(label(r"C over E: \ a sixth", font_size=22, color=GREY_A).next_to(demo.notes[0][0], UP, buff=0.2), label(r"B over E: \ a fifth", font_size=22, color=GREY_A),
                      label(r"A over F: \ a third", font_size=22, color=GREY_A).next_to(demo.notes[0][2], UP, buff=0.2))
        tags[1].next_to(demo.notes[0][1], DOWN, buff=0.45)
        demo2 = duet([[(72, 0, 2), (74, 2, 2), (76, 4, 4)], [(69, 0, 4), (72, 4, 4)]], width=5.0, height=2.4, lo=60, hi=80, thick=0.16, bar=4.0).move_to(RIGHT * 3.2 + DOWN * 0.3)
        demo2.notes[0][1].set_fill(EAR)
        t2 = label(r"D over A: \ a fourth, \ dissonant, \ passing from C to E", font_size=22, color=EAR).next_to(demo2, DOWN, buff=0.4)
        rules = VGroup(label(r"two half notes to each note of the cantus", font_size=28, color=WHITE),
                       label(r"the first of each pair must be consonant", font_size=28, color=WHITE),
                       label(r"the second may be dissonant \ if it passes by step, \ in one direction", font_size=28, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Second species gives the new voice two notes to each note of the cantus, and with them "
            "a new freedom. <bookmark mark='a'/> The note on the strong beat must still be consonant. "
            "The note on the weak beat may be a dissonance, but only one kind: a passing note, which "
            "fills the gap between two consonances a third apart, arriving by step and leaving by step "
            "in the same direction. <bookmark mark='b'/> Here C over A is a third, E over C is a third, "
            "and the D between them is a fourth above the cantus: a dissonance, on the way somewhere. "
            "In Part 14 a melody moved mostly by steps. A passing dissonance is a melody's step "
            "allowed to clash, because the ear hears where it is going."
        ) as vo:
            self.play(FadeIn(rules[0]))
            vo.wait_until("a")
            self.play(FadeIn(rules[1]), FadeIn(rules[2]), FadeIn(demo))
            vo.wait_until("b")
            self.play(FadeIn(demo2), FadeIn(t2))
        self.wait(0.4)
        self.clear_scene()

    def hear(self):
        d = load("species")["2"]
        species_scene(self, 2,
                      "Here is a second-species line over Fux's cantus. The pink notes are the passing "
                      "dissonances.",
                      f"There were {len(d['dissonances'])} passing dissonances, each on a weak beat, each "
                      "between two consonances. And notice the rhythm: now only half of the new voice's "
                      "notes begin together with a note of the cantus. The ear gets a second cue for "
                      "two voices, for free.",
                      r"pink: \ passing dissonances")
