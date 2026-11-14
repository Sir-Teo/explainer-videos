from __future__ import annotations

import numpy as np

from videos.music.music38.common import *  # noqa: F403

NN = ["C", r"D$\flat$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]


class Walking(SoundScene):
    def construct(self):
        chapter(self, 7, r"Walking bass and the ride", r"Can a program walk a bass line?")
        self.jobs()
        self.rules()
        self.hear()
        self.stats()
        self.players()

    # ------------------------------------------------------------------
    def jobs(self):
        items = [
            (r"the bass `walks': \ one note on every beat, \ outlining the chords and leading to the next", WHITE),
            (r"the drummer's ride cymbal plays the swing pattern; \ the hi-hat closes on beats 2 and 4", WHITE),
            (r"piano or guitar `comps': \ chords placed to answer the soloist", WHITE),
            (r"in Basie's band, \ Freddie Green's guitar played four even chords a bar, \ every bar", TUNE),
            (r"time kept by four people at once", GREY_A),
        ]
        rows_scene(self, r"the rhythm section", items,
                   "The rhythm section has jobs. <bookmark mark='b'/> The bass walks: one note on every beat, outlining the "
                   "chords and leading to the next one. <bookmark mark='c'/> The drummer plays the swing pattern on the ride "
                   "cymbal and closes the hi-hat on beats two and four. <bookmark mark='d'/> The piano or guitar comps, placing "
                   "chords to answer the soloist; <bookmark mark='e'/> in Basie's band, Freddie Green's guitar played four even "
                   "chords to every bar. <bookmark mark='f'/> Time kept by four people at once.", marks="cdef")

    # ------------------------------------------------------------------
    def rules(self):
        d = load("walking")
        wb = d["bass"]
        bars4 = d["changes"][:4]
        ch = chart(bars4, cell_w=2.8, cell_h=0.7, size=20).move_to(UP * 1.9)
        notes = [[m, i, 1.0] for i, m in enumerate(wb[:16])]
        roll = mroll(notes, width=11.2, height=2.2, lo=min(wb[:16]) - 2, hi=max(wb[:16]) + 2, color=BLUE, total=16, bar_h=0.16).move_to(DOWN * 0.2)
        roll.match_x(ch)
        names = VGroup(*[label(NN[m % 12], font_size=16, color=WHITE).next_to(b, UP, buff=0.06) for (m, _, _), b in zip(notes, roll.notes)])
        firsts = [i for i in range(16) if i == 0 or d["beats"][i] != d["beats"][i - 1]]
        for i in firsts:
            roll.notes[i].set_color(TUNE)
        for i in [f - 1 for f in firsts if f > 0]:
            roll.notes[i].set_color(EAR)
        rules = VGroup(label(r"gold: \ the root, \ on the chord's first beat", font_size=18, color=TUNE),
                       label(r"pink: \ a semitone from the next root, \ just before it", font_size=18, color=EAR),
                       label(r"blue: \ chord tones, \ or scale tones; \ no leap bigger than a fifth", font_size=18, color=BLUE),
                       label(r"among all lines that obey, \ the one with the least total motion \ (dynamic programming)", font_size=18, color=WHITE)).arrange(DOWN, buff=0.12, aligned_edge=LEFT).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Monochord's walking bass follows four rules. <bookmark mark='a'/> On the first beat of each chord, play its "
            "root. <bookmark mark='b'/> On the beat before a new chord, play a note a semitone above or below the new root, so "
            "the line leans into it. <bookmark mark='c'/> On other beats, play a chord tone, or a note of the chord's scale, "
            "and never leap more than a fifth. <bookmark mark='d'/> Among all the lines that obey, choose the one with the "
            "least total motion. That is a shortest-path problem, solved beat by beat like Part 22's parser. Here are the "
            "first four bars of a jazz blues in C."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(roll), FadeIn(names))
            for mark, r in zip("abcd", rules):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("walking")
        c = clip("walking.trio")
        wb = d["bass"]
        notes = [[m, i, 1.0] for i, m in enumerate(wb)]
        roll = mroll(notes, width=11.6, height=1.9, lo=min(wb) - 2, hi=max(wb) + 2, color=BLUE, total=48, bar_h=0.12).move_to(DOWN * 1.6)
        ch = chart(d["changes"], cell_w=2.4, cell_h=0.6, size=18).move_to(UP * 1.3)
        stage = VGroup(label(r"chorus 1: \ bass, \ ride, \ hi-hat", font_size=19, color=GREY_A), label(r"chorus 2: \ with piano", font_size=19, color=GREY_A)).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.25)
        with self.voiceover(
            "Hear the generated line through two choruses of the jazz blues at a hundred and forty beats a minute: first with "
            "only ride and hi-hat, then with the piano comping."
        ):
            self.play(FadeIn(ch), FadeIn(roll), FadeIn(stage))
        beat = 60.0 / d["bpm"]
        with self.listen(c) as snd:
            window(snd, r"a walking bass, \ two choruses", detail=r"string, \ cymbal and piano models", corner=DL, tag_corner=DR)
            flash(snd, roll.notes * 2, [i * beat for i in range(96)], hot=WHITE, base=BLUE)
            for k in range(24):
                pulse(snd, ch.bars[k % 12], k * 4 * beat, (k + 1) * 4 * beat - 0.03, buff=0.03)
            pulse(snd, stage[0], 0.0, 48 * beat, buff=0.08)
            pulse(snd, stage[1], 48 * beat, c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stats(self):
        d = load("walking")
        mv = d["moves"]
        from collections import Counter
        cnt = Counter(mv)
        ks = sorted(cnt)
        bars = VGroup()
        for i, k in enumerate(ks):
            b = Rectangle(width=0.7, height=0.08 * cnt[k], stroke_width=0, fill_color=BLUE, fill_opacity=0.85)
            bars.add(VGroup(b, label(str(cnt[k]), font_size=17, color=WHITE), label(str(k), font_size=17, color=GREY_A)))
        for i, g_ in enumerate(bars):
            g_[0].move_to([-4.5 + 1.0 * i, -1.6 + g_[0].height / 2, 0])
            g_[1].next_to(g_[0], UP, buff=0.08)
            g_[2].move_to([g_[0].get_center()[0], -1.9, 0])
        xl = label(r"interval between successive bass notes \ (semitones)", font_size=17, color=GREY_A).move_to([-4.5 + 0.5 * (len(ks) - 1), -2.4, 0])
        side = VGroup(label(rf"every one of the {len(d['approaches'])} chord changes approached by a semitone", font_size=19, color=TUNE),
                      label(r"every chord's first beat on its root", font_size=19, color=TUNE),
                      label(rf"{sum(cnt[k] for k in ks if k <= 2)} of {len(mv)} moves are steps \ (1 or 2 semitones)", font_size=19, color=WHITE),
                      label(r"what it lacks: \ rhythm, \ register arcs, \ surprise", font_size=19, color=EAR)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 3.2)
        head = label(r"the generated line, \ counted", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Count the line. Every one of its {say(len(d['approaches']))} chord changes is approached by a semitone, and every "
            f"chord begins on its root, as the rules require. {say(sum(cnt[k] for k in ks if k <= 2))} of its "
            f"{say(len(mv))} moves are steps of one or two semitones. <bookmark mark='a'/> And it is dull: a real bassist "
            "varies the rhythm with skips and triplets, shapes the register over a chorus, and surprises."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(g_) for g_ in bars], lag_ratio=0.15), FadeIn(xl), FadeIn(side[:3]))
            vo.wait_until("a")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def players(self):
        items = [
            (r"Walter Page with Basie made the even walking four the norm", WHITE),
            (r"Jimmy Blanton with Ellington \ (1939--41) \ made the bass a solo voice", WHITE),
            (r"Ray Brown, \ Paul Chambers and others: \ lines that are melodies in their own right", WHITE),
            (r"a walking line is improvised, \ chorus after chorus, \ listening to everyone else", TUNE),
            (r"chapter 8: \ the tones a line must find", GREY_A),
        ]
        rows_scene(self, r"the bassists", items,
                   "The bassists made this an art. <bookmark mark='b'/> Walter Page, with Basie, made the even walking four the "
                   "norm. <bookmark mark='c'/> Jimmy Blanton, with Ellington from 1939 to 1941, made the bass a solo voice. "
                   "<bookmark mark='d'/> Ray Brown, Paul Chambers and others played lines that are melodies in their own right. "
                   "<bookmark mark='e'/> And a walking line is improvised, chorus after chorus, while listening to everyone else. "
                   "<bookmark mark='f'/> Chapter eight turns to the tones a line must find.", marks="cdef")
