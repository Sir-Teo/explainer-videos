from __future__ import annotations

import numpy as np

from videos.music.music67.common import *  # noqa: F403


class Canon(SoundScene):
    def construct(self):
        chapter(self, 3, r"Analysis and the corpus", r"Is a rule about music a rule about the music you chose?")
        self.argument()
        self.heard()
        self.table()
        self.corpus_turn()

    # ------------------------------------------------------------------
    def argument(self):
        items = [
            (r"analysis is an argument: \ this chord prepares that one; \ this motive returns, \ changed", WHITE),
            (r"its evidence is the score, \ and its test is the counter-example: \ a passage the argument cannot explain", WHITE),
            (r"the corpus turn: \ count across many pieces, \ so that a claim about `music' rests on more than a few", WHITE),
            (r"but a corpus is a choice, \ and most corpora are canons: \ Bach, \ Mozart, \ Beethoven, \ the Beatles", TUNE),
        ]
        rows_scene(self, r"arguments and counts", items,
                   "Analysis is an argument: this chord prepares that one; this motive returns, changed. <bookmark mark='b'/> Its "
                   "evidence is the score, and its test is the counter-example, a passage the argument cannot explain. "
                   "<bookmark mark='c'/> The corpus turn added counting across many pieces, so that a claim about music rests on "
                   "more than a few. <bookmark mark='d'/> But a corpus is a choice, and most corpora are canons: Bach, Mozart, "
                   "Beethoven, the Beatles.", marks="bcd")

    # ------------------------------------------------------------------
    def table(self):
        d = load("canon")["rows"]
        names = {"steps": r"moves by step \ (at most a whole tone)", "leaps5": r"leaps of a fourth or more", "repeats": r"repeated notes"}
        g = VGroup()
        for k in ("steps", "leaps5", "repeats"):
            a, b = d["chorales"][k], d["tunes"][k]
            g.add(VGroup(label(names[k], font_size=18, color=WHITE),
                         label(rf"{100 * a['value']:.0f}\% \ ({100 * a['lo']:.0f} to {100 * a['hi']:.0f})", font_size=18, color=TUNE),
                         label(rf"{100 * b['value']:.0f}\% \ ({100 * b['lo']:.0f} to {100 * b['hi']:.0f})", font_size=18, color=EAR)))
        g.arrange(DOWN, buff=0.45)
        for r in g:
            for i, x in enumerate((-3.2, 1.2, 4.4)):
                r[i].set_x(x)
        g.move_to(DOWN * 0.3)
        top = VGroup(label(rf"Bach's chorale tunes \ ({d['chorales']['n']})", font_size=16, color=TUNE).move_to([1.2, g.get_top()[1] + 0.55, 0]),
                     label(rf"Part 14's tunes \ ({d['tunes']['n']}: \ folk songs, \ hymns, \ nursery tunes)", font_size=16, color=EAR).move_to([4.4, g.get_top()[1] + 0.55, 0]))
        note = label(r"95\% intervals by resampling tunes; \ moves exclude repeated notes", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.45)
        head = label(r"`melodies move mostly by step'", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        a, b = d["chorales"], d["tunes"]
        with self.voiceover(
            "Take a rule every textbook states: melodies move mostly by step. Test it on two corpora. <bookmark mark='a'/> In "
            f"Bach's chorale tunes, {say(round(100 * a['steps']['value']))} per cent of moves are steps. In Part 14's wider "
            f"collection of folk songs, hymns and nursery tunes, {say(round(100 * b['steps']['value']))} per cent, and the "
            "intervals do not overlap. Both are mostly steps; but how mostly depends on the corpus, by a margin larger than "
            "most effects analysts argue about. <bookmark mark='b'/> The tunes also repeat notes far more, "
            f"{say(round(100 * b['repeats']['value']))} per cent of the time against {say(round(100 * a['repeats']['value']))}. "
            "A rule measured on a canon is a rule about the canon until it is tested elsewhere."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(g[0]), FadeIn(g[1]))
            vo.wait_until("b")
            self.play(FadeIn(g[2]))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def corpus_turn(self):
        items = [
            (r"say which corpus, \ how chosen, \ and what it leaves out", WHITE),
            (r"resample: \ an interval by tunes, \ not by notes, \ because notes in one tune are not independent", WHITE),
            (r"hold out: \ a claim found by searching one corpus should be checked on another", WHITE),
            (r"and remember the counter-example: \ one well-chosen passage can still refute a rule that a thousand obey", TUNE),
        ]
        rows_scene(self, r"corpus studies, \ done well", items,
                   "Corpus studies done well share a few habits. <bookmark mark='b'/> Say which corpus, how it was chosen, and what "
                   "it leaves out. <bookmark mark='c'/> Resample by tunes, not by notes, because the notes of one tune are not "
                   "independent; the intervals on that table were computed that way. <bookmark mark='d'/> Hold out: a claim found "
                   "by searching one corpus should be checked on another. <bookmark mark='e'/> And remember the counter-example: one "
                   "well-chosen passage can still refute a rule that a thousand passages obey.", marks="bcde")

    # ------------------------------------------------------------------
    def heard(self):
        d = load("canonheard")
        c = clip("canon.two")
        boxes = choice_boxes([rf"a chorale tune: \ {bwv(d['chorale'])}", r"a tune from Part 14's collection"], width=4.6, height=0.9, buff=0.6, size=17).move_to(UP * 0.6)
        note = label(rf"steps among their moves: \ {100 * d['chorale_steps']:.0f}\% and {100 * d['tune_steps']:.0f}\%", font_size=18, color=TUNE).next_to(boxes, DOWN, buff=0.6)
        head = label(r"two corpora, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("First, hear what the two corpora are: the opening of one of Bach's chorale tunes, then the opening of a tune from Part 14's collection."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"chorale, \ then tune", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["chorale"], st["tune"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["tune"], c.duration, buff=0.08)
        with self.voiceover("A hymn tune made for a congregation to sing in long, even notes, and a song with repeated notes and leaps. Which is more typical of melody depends on what you mean by melody."):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()
