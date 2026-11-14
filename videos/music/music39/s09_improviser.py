from __future__ import annotations

import numpy as np

from videos.music.music39.common import *  # noqa: F403
from explainer.music.monochord import blues as BL


class Improviser(SoundScene):
    def construct(self):
        chapter(self, 8, r"An improviser", r"Can a short program play through changes?")
        self.grammar()
        self.quiz()
        self.judged()
        self.lacks()

    # ------------------------------------------------------------------
    def grammar(self):
        steps = VGroup(
            label(r"1. \ split the changes into half-bars \ (two beats, \ four eighth notes)", font_size=20, color=WHITE),
            label(r"2. \ choose a target: \ a guide tone of the next half-bar's chord, \ nearest the current note", font_size=20, color=TUNE),
            label(r"3. \ choose a figure, \ at random: \ a bebop-scale run from a chord tone, \ an arpeggio, \ an enclosure, \ or a rest", font_size=20, color=WHITE),
            label(r"4. \ stay between B$\flat$3 and C6; \ after a rest, \ start again near the middle", font_size=20, color=WHITE),
            label(r"5. \ swing it with Part 38's model", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.1)
        steps.scale_to_fit_width(min(steps.width, 13.0))
        head = label(r"a phrase grammar, \ in five steps", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is an improviser in five steps, built from this part's ideas. <bookmark mark='a'/> Split the changes into "
            "half-bars of two beats. <bookmark mark='b'/> For each, choose a target: a guide tone of the next chord, nearest "
            "the current note. <bookmark mark='c'/> Then choose a figure to get there, at random: a bebop-scale run starting "
            "on a chord tone, so chord tones fall on the beats; an arpeggio; an enclosure; or a rest, to breathe. "
            "<bookmark mark='d'/> Keep within a saxophone's comfortable range, and after a rest start again near the middle. "
            "<bookmark mark='e'/> And swing it with Part 38's model. That is all: a page of code, and a seed for the dice."
        ) as vo:
            self.play(FadeIn(head))
            for mark, s in zip("abcde", steps):
                vo.wait_until(mark)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("improv")
        c = clip("improv.pair")
        card = listen_card(r"Two lines over the same jazz blues, \ on piano. \ One is the improviser's; \ "
                           r"the other has notes drawn at random from each chord's scale. \ Which is the improviser: \ A or B?", width=10.4)
        with self.voiceover(
            "A question for your ears. Two lines over the same jazz blues, on the piano. One is the improviser's. The other "
            "has every note drawn at random from the right scale for each chord, moving by small steps. Which is the "
            "improviser, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ga = line_over([tuple(x) for x in d["random"]], d["changes"], width=11.4, height=1.5, color=GREY_A, lo=56, hi=86, size=11).move_to(UP * 1.4)
        gb = line_over([tuple(x) for x in d["improviser"]], d["changes"], width=11.4, height=1.5, color=GREY_A, lo=56, hi=86, size=11).move_to(DOWN * 1.5)
        la = label(r"A", font_size=26, color=EAR).next_to(ga, LEFT, buff=0.2)
        lb = label(r"B", font_size=26, color=EAR).next_to(gb, LEFT, buff=0.2)
        self.play(FadeOut(card), FadeIn(ga), FadeIn(gb), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"piano, \ string and cymbal models", corner=DL, tag_corner=DR)
            flash(snd, ga.roll.notes, list(BL.swing_times([e for _, e in d["random"]], d["bpm"]) + d["starts"]["A"]), hot=WHITE, base=GREY_A)
            flash(snd, gb.roll.notes, list(BL.swing_times([e for _, e in d["improviser"]], d["bpm"]) + d["starts"]["B"]), hot=WHITE, base=GREY_A)
        ja, jb = d["judge_rnd"], d["judge_imp"]
        ans = label(rf"B: \ the improviser; \ it rests, \ and lands on chord tones \ ({round(100 * jb['on_beat_chord_tones'])}\% of beats against {round(100 * ja['on_beat_chord_tones'])}\%)", font_size=21, color=TUNE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "B is the improviser. It breathes, in phrases, and it lands on chord tones: "
            f"{say(round(100 * jb['on_beat_chord_tones']))} per cent of its beats against "
            f"{say(round(100 * ja['on_beat_chord_tones']))} per cent for the random line, though every note of the random "
            "line was also in the right scale. Being in the scale is not enough; where the notes fall is what makes the "
            "changes audible."
        ):
            self.play(gb.roll.animate.set_color(TUNE), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def judged(self):
        d = load("improv")
        st = d["stats"]
        metrics = [("on_beat_chord_tones", r"beats on chord tones"), ("guide_at_changes", r"guide tones at chord changes"),
                   ("in_scale", r"notes in the chord's scale"), ("steps", r"moves by step")]
        names = [("improviser", TUNE, r"improviser"), ("scale", BLUE, r"random, \ in scale"), ("chromatic", GREY_B, r"random, \ any note")]
        g = VGroup()
        for i, (k, title) in enumerate(metrics):
            row = VGroup(label(title, font_size=19, color=WHITE))
            for j, (n, col, _) in enumerate(names):
                v = st[n][k]
                row.add(VGroup(Rectangle(width=max(4.5 * v, 0.02), height=0.22, stroke_width=0, fill_color=col, fill_opacity=0.85),
                               label(f"{round(100 * v)}", font_size=15, color=col)))
            g.add(row)
        for i, row in enumerate(g):
            y = 1.9 - 1.15 * i
            row[0].move_to([-2.4, y, 0], aligned_edge=RIGHT)
            for j in (1, 2, 3):
                row[j][0].move_to([-2.1, y + 0.3 - 0.28 * (j - 1), 0], aligned_edge=LEFT)
                row[j][1].next_to(row[j][0], RIGHT, buff=0.1)
        leg = VGroup(*[label(t, font_size=17, color=col) for _, col, t in names]).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.5)
        head = label(r"judged over fifty choruses each \ (per cent)", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Judge it properly, over fifty choruses each, by the series' own measures, against two baselines: random notes "
            "from each chord's scale, and random notes from all twelve. <bookmark mark='a'/> On the beats, the improviser plays "
            f"chord tones {say(round(100 * st['improviser']['on_beat_chord_tones']))} per cent of the time, against "
            f"{say(round(100 * st['scale']['on_beat_chord_tones']))} and {say(round(100 * st['chromatic']['on_beat_chord_tones']))}. "
            f"At chord changes it brings a guide tone {say(round(100 * st['improviser']['guide_at_changes']))} per cent of the "
            f"time, against {say(round(100 * st['scale']['guide_at_changes']))} and {say(round(100 * st['chromatic']['guide_at_changes']))}. "
            "<bookmark mark='b'/> Its notes are slightly less often in the scale than the first baseline's, because enclosures "
            "and the bebop scale's passing tone step outside it on purpose."
        ) as vo:
            self.play(FadeIn(head), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in g[:2]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in g[2:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lacks(self):
        items = [
            (r"what the program lacks: \ motifs developed over a chorus, \ a shape that builds", WHITE),
            (r"rhythm: \ it plays only eighth notes and rests; \ players mix triplets, \ long notes, \ displacement", WHITE),
            (r"listening: \ it never responds to the band, \ and the band never responds to it", WHITE),
            (r"the measures reward safe choices; \ great solos break them on purpose", TUNE),
            (r"chapter 10 meets machines that do listen", GREY_A),
        ]
        rows_scene(self, r"what it lacks", items,
                   "What does the program lack? <bookmark mark='b'/> Motifs developed over a chorus, a shape that builds. "
                   "<bookmark mark='c'/> Rhythm: it plays only eighth notes and rests, where players mix triplets, long notes and "
                   "displaced accents. <bookmark mark='d'/> And listening: it never responds to the band, and the band never "
                   "responds to it. <bookmark mark='e'/> Its measures reward safe choices, and great solos break them on purpose. "
                   "<bookmark mark='f'/> Chapter ten meets machines that do listen.", marks="cdef")
