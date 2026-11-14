from __future__ import annotations

import numpy as np

from videos.music.music13.common import *  # noqa: F403


class Inversion(SoundScene):
    def construct(self):
        chapter(self, 4, r"Rameau's claim", r"Is a chord its notes, \ or their order?", lit=(1722,))
        self.positions()
        self.rameau()
        self.puzzle()
        self.bass()
        self.quiz()

    # ------------------------------------------------------------------
    def positions(self):
        d = load("inversion")
        pos = d["positions"]
        row = chord_row([p["names"] for p in pos], width=11.0, space=0.26, above=[r"root position", r"first inversion", r"second inversion"], font_size=26, above_color=GREY_A).move_to(UP * 1.2)
        figs = VGroup()
        for k, p in enumerate(pos):
            f = VGroup(*[label(str(n), font_size=30, color=TUNE) for n in p["figures"]]).arrange(DOWN, buff=0.06)
            f.move_to([row.notes[k].x, 0, 0]).next_to(row.staff, DOWN, buff=0.35, coor_mask=[0, 1, 0])
            figs.add(f)
        figs.shift(row.get_center() * RIGHT)
        said = VGroup(*[label(t, font_size=24, color=GREY_A).next_to(figs[k], DOWN, buff=0.2) for k, t in enumerate((r"a third and a fifth", r"a third and a sixth", r"a fourth and a sixth"))])
        with self.voiceover(
            "Back to the opening. C, E, G with C at the bottom is called root position. "
            "<bookmark mark='a'/> Put E at the bottom, and it is the first inversion. <bookmark mark='b'/> "
            "Put G at the bottom: the second inversion. <bookmark mark='c'/> A keyboard player of Bach's "
            "time, reading a figured bass as in Part 10, did not think of these as one chord. He read "
            "the intervals above the bass note. A third and a fifth: five-three. A third and a sixth: "
            "six-three, or just six. A fourth and a sixth: six-four. Three figures, three sets of rules "
            "for what may come next."
        ) as vo:
            self.play(FadeIn(row.staff.systems[0].lines), FadeIn(row.staff.systems[0].clef), FadeIn(row.staff.barlines), FadeIn(row.notes[0]), FadeIn(row.above[0]))
            vo.wait_until("a")
            self.play(FadeIn(row.notes[1]), FadeIn(row.above[1]))
            vo.wait_until("b")
            self.play(FadeIn(row.notes[2]), FadeIn(row.above[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(figs[k], said[k])) for k in range(3)], lag_ratio=0.9), run_time=9.0)
        self.wait(0.3)
        self.row, self.figs, self.said = row, figs, said

    # ------------------------------------------------------------------
    def rameau(self):
        row, figs, said = self.row, self.figs, self.said
        card = history_card(1722, r"Jean-Philippe Rameau, \ \textit{Trait\'e de l'harmonie}", r"under every chord there is a fundamental bass: \ its root", width=8.6, font_size=26).to_edge(DOWN, buff=0.45)
        roots = []
        for k in range(3):
            j = {0: 0, 1: 2, 2: 1}[k]                      # where C is in each position
            roots.append(row.notes[k].heads[j])
        with self.voiceover(
            "In 1722 Rameau published his Treatise on Harmony, and proposed another way to hear. Under "
            "any chord, he said, there is a fundamental bass. Rearrange the notes until they stand in "
            "thirds, and the bottom of that stack is the chord's root, wherever the actual bass may be. "
            "<bookmark mark='a'/> All three of these have the root C. The figures describe the surface. "
            "The root says what the chord is."
        ) as vo:
            self.play(FadeOut(said), FadeIn(card))
            vo.wait_until("a")
            self.play(*[r.animate.set_color(TUNE) for r in roots], run_time=1.0)
            self.play(*[Indicate(r, color=TUNE, scale_factor=1.6) for r in roots])
        note = VGroup(label(r"1612: \ Johannes Lippius had already described the triad and its inversions.", font_size=24, color=GREY_A),
                      label(r"Rameau built a theory of how roots \textit{move}.", font_size=28, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "He was not the first to notice. Johannes Lippius had described the triad and its inversions "
            "a century earlier. What Rameau added was a theory built on it: a theory of how roots move "
            "from one chord to the next. After him, harmony was taught as a grammar of chords, where "
            "before it had been a set of rules about intervals above a bass."
        ):
            self.play(FadeOut(card), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def puzzle(self):
        d = load("inversion")["puzzle"]
        row = chord_row([d["names"], ["G3", "B3", "D4", "F4"]], width=6.0, space=0.26, above=[r"?", r"G, \ B, \ D, \ F"], font_size=30, above_color=TUNE).move_to(UP * 1.0 + LEFT * 2.2)
        card = pause_card(r"F at the bottom, \ then G, \ B and D. \ What is the root? \ Rearrange the notes into thirds.", width=5.4).move_to(RIGHT * 3.6 + UP * 1.0)
        with self.voiceover(
            "Try it. Here are four notes: F at the bottom, then G, B and D. What is the root? Pause, and "
            "rearrange them into thirds."
        ):
            self.play(FadeIn(row.staff.systems[0].lines), FadeIn(row.staff.systems[0].clef), FadeIn(row.notes[0]), FadeIn(row.above[0]), FadeIn(card))
        self.wait(2.0)
        ans = VGroup(label(r"root: \ G \quad a seventh chord, \ with its seventh in the bass", font_size=28, color=WHITE),
                     label(r"figured bass calls it \ $^4_2$; \ Rameau calls it \ G$^7$", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "G, B, D, F. <bookmark mark='a'/> The root is G, and in the chord as written it is the "
            "second note from the bottom. A figured-bass player calls this a four-two chord. Rameau "
            "calls it a seventh chord on G with its seventh in the bass. Monochord's chord module does "
            "this reduction for any set of notes: try each note as the bottom of a stack of thirds, and "
            "see which one works."
        ) as vo:
            self.play(FadeOut(card), FadeIn(row.notes[1]), FadeIn(row.above[1]), FadeIn(row.staff.barlines), FadeOut(row.above[0]))
            vo.wait_until("a")
            self.play(row.notes[1].heads[0].animate.set_color(TUNE), row.notes[0].heads[1].animate.set_color(TUNE), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bass(self):
        d = load("inversion")
        c = clip("inversion.three")
        kb = keys(48, 72, width=10.0, height=1.8).move_to(UP * 0.9)
        tags = VGroup(*[label(t, font_size=28, color=GREY_A) for t in (r"C in the bass", r"E in the bass", r"G in the bass")]).arrange(RIGHT, buff=1.0).next_to(kb, DOWN, buff=0.5)
        with self.voiceover(
            "Does the ear agree with Rameau? Partly. Keep C, E and G above, and put each of the three "
            "notes in turn underneath them, in the bass."
        ):
            self.play(FadeIn(kb), FadeIn(tags))
            for m in d["upper"]:
                kb.on(m)
        with self.listen(c) as snd:
            window(snd, r"one chord, \ three basses", detail=r"C, \ E, \ G above; \ the bass changes", corner=DL, tag_corner=DR)
            light_chords(snd, kb, [[b] + d["upper"] for b in d["basses"]], d["three_times"], end=c.duration)
            for k in range(3):
                pulse(snd, tags[k], d["three_times"][k], d["three_times"][k + 1] if k < 2 else c.duration, buff=0.12)
        kb.clear()
        verdict = VGroup(*[label(t, font_size=26, color=WHITE).next_to(tags[k], DOWN, buff=0.25) for k, t in enumerate((r"settled", r"lighter; \ wants to move", r"unstable"))])
        with self.voiceover(
            "The same chord, yes. But not the same weight. With the root in the bass the chord is "
            "settled: it can end a piece. <bookmark mark='a'/> With the third in the bass it is lighter, "
            "and wants to move on. <bookmark mark='b'/> With the fifth in the bass it is unstable enough "
            "that composers of Rameau's century treated it as a dissonance, and resolved it. Here is the "
            "classic case: the six-four chord on G falls to a plain G chord, and then goes home."
        ) as vo:
            self.play(FadeIn(verdict[0]))
            vo.wait_until("a")
            self.play(FadeIn(verdict[1]))
            vo.wait_until("b")
            self.play(FadeIn(verdict[2]))
        c2 = clip("inversion.cadence")
        steps = VGroup(*[label(t, font_size=30, color=GREY_A) for t in (r"C over G: \ $^6_4$", r"G", r"C")]).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=1.35)
        self.play(FadeOut(tags), FadeOut(verdict), FadeIn(steps))
        with self.listen(c2) as snd:
            window(snd, r"six-four, \ five-three, \ home", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            light_chords(snd, kb, d["cadence"], d["cadence_times"], end=c2.duration)
            for k in range(3):
                pulse(snd, steps[k], d["cadence_times"][k], d["cadence_times"][k + 1] if k < 2 else c2.duration, buff=0.12)
        kb.clear()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        c = clip("inversion.quiz")
        ev = c.events
        card = listen_card(r"One chord, \ twice, \ with different notes in the bass. \ In which is the root in the bass: \ A or B?", width=9.2)
        with self.voiceover("Try your ear. One chord, played twice, with different notes in the bass. In which one is the root in the bass: A or B?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        bx = boxes(("A", "B"), buff=1.2, width=2.4, height=1.2, font_size=48).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, bx[0], ev["A"], ev["B"] - 0.4)
            pulse(snd, bx[1], ev["B"], c.duration)
        ans = VGroup(label(r"A: \ E in the bass: \ first inversion", font_size=28, color=GREY_A), label(r"B: \ C in the bass: \ root position", font_size=28, color=TUNE)).arrange(DOWN, buff=0.3).move_to(DOWN * 1.5)
        with self.voiceover(
            "B. In A the bass note was E, the third of the chord. If A sounded lighter to you and B "
            "sounded planted, you were hearing inversion: the same notes, with a different one in charge."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
