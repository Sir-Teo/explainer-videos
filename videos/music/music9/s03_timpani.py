from __future__ import annotations

import numpy as np

from videos.music.music9.common import *  # noqa: F403


class Timpani(SoundScene):
    def construct(self):
        chapter(self, 2, r"A drum with a note", r"How does a kettledrum play in tune?", lit=(1877,), extra=((1982, r"Rossing measures the kettledrum"),))
        self.rows()
        self.quiz()
        self.octave()

    # ------------------------------------------------------------------
    def rows(self):
        d = load("timpani")
        g = axes([0.8, 3.2], [0, 3.6], x_length=10.6, y_length=3.8, xlabel=r"frequency, \ in units of the lowest ringing mode", ylabel="", xticks=[1, 1.5, 2, 2.5, 3], yticks=[], font_size=20).move_to(DOWN * 0.9)
        targets = VGroup(*[DashedLine(g.ax.c2p(v, 0), g.ax.c2p(v, 3.6), color=GREY_D, stroke_width=1.5) for v in d["series"]])
        r1 = tick_row(g, d["plain"], 2.9, GREY_B)
        r2 = tick_row(g, d["estimate"], 1.75, AIR)
        r3 = tick_row(g, d["measured"], 0.6, SKIN)
        l1 = label(r"a bare skin, \ in a vacuum", font_size=22, color=GREY_B).next_to(g.ax.c2p(0.8, 2.9), LEFT, buff=0.1)
        l2 = label(r"with the air it must move \\ (an estimate)", font_size=22, color=AIR).next_to(g.ax.c2p(0.8, 1.75), LEFT, buff=0.1)
        l3 = label(r"a real kettledrum \\ (measured)", font_size=22, color=SKIN).next_to(g.ax.c2p(0.8, 0.6), LEFT, buff=0.1)
        VGroup(g, targets, r1, r2, r3).shift(RIGHT * 1.2)
        for l, y in ((l1, 2.9), (l2, 1.75), (l3, 0.6)):
            l.next_to(g.ax.c2p(0.8, y), LEFT, buff=0.15)
        head = label(r"The modes that ring: \ one, \ two, \ three, \ four, \ five diameters", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "An orchestra's kettledrums are tuned to notes, and composers write for them as they would for a "
            "double bass. How can a skin do that? Take the modes that ring: the ones with one, two, three, "
            "four and five still diameters. <bookmark mark='a'/> In an ideal skin their frequencies stand at "
            f"one, {say(d['plain'][1], 2)}, {say(d['plain'][2], 2)}, {say(d['plain'][3], 2)}, "
            f"{say(d['plain'][4], 2)}. The dashed lines are where a musician would want them: one, one and a "
            "half, two, two and a half, three. Not close. <bookmark mark='b'/> But a real skin does not "
            "vibrate in a vacuum. It has to move the air lying against it, and for the long, slow waves of "
            "the low modes that is a good deal of air: on a large drum, as much weight as the skin itself. "
            "Air loads the low modes more than the high ones, and so slows them more. Here is Monochord's "
            f"rough estimate of the effect: one, {say(d['estimate'][1], 2)}, {say(d['estimate'][2], 2)}, "
            f"{say(d['estimate'][3], 2)}. Every mode has moved towards its line. <bookmark mark='c'/> And here "
            "is a real kettledrum, measured by Thomas Rossing in 1982: one, one point five, one point nine "
            "eight, two point four four. The rest of the way is the air shut inside the kettle and the "
            "stiffness of the head. So the kettle is not a resonator, as people supposed. It is a weight. "
            "It tunes the drum by loading it with air."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(targets))
            vo.wait_until("a")
            self.play(FadeIn(r1), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(r2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(r3), FadeIn(l3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("timpani")
        c = clip("timpani.pair")
        q = listen_card(r"Two drums with the same lowest ringing mode. \\ One is a bare skin; \ one has a kettledrum's overtones. \ Which has a note you could hum?", width=9.8, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes(buff=2.6, width=3.0, height=1.3).move_to(DOWN * 0.3)
        with self.voiceover(
            "Can you hear the difference those shifts make? Two drums, with the same lowest ringing mode. One "
            "is the bare skin. One has the kettledrum's overtones. Which has a note you could hum?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"two drums", detail=r"a bare skin, \ and a kettledrum's modes", corner=DL, tag_corner=DR)
            for ev, b in zip("AB", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.0)
        ans = VGroup(label(r"a bare skin: \ a boom", font_size=28, color=GREY_B).next_to(bx[0], DOWN, buff=0.25), label(r"a kettledrum: \ a note", font_size=28, color=SKIN).next_to(bx[1], DOWN, buff=0.25))
        with self.voiceover("B. And to prove it is a note, here are four of them."):
            self.play(FadeOut(q), FadeIn(ans))
        c2 = clip("timpani.notes")
        with self.listen(c2) as snd:
            window(snd, r"four notes on kettledrums", detail=r"measured overtones, \ computed sound", corner=DL, tag_corner=DR)
            pulse(snd, bx[1], 0.0, c2.duration - 0.2)
        with self.voiceover(
            "The first four notes of the Tune. No orchestra could do without that sound, and it rests on an "
            "accident: that air is heavy enough to matter to a thin skin."
        ):
            self.play(Indicate(ans[1], color=WHITE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def octave(self):
        d = load("timpani")
        head = label(r"Which note, \ though?", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)
        rows = rows_card([
            (r"the overtones", rf"1, \ 1.5, \ 2, \ 2.5 \ are \ 2, \ 3, \ 4, \ 5 \ halves: \\ harmonics two to five of a note an octave \emph{{below}} the lowest."),
            (r"Part 4's model of the ear", rf"hears exactly that missing note, \ at {d['kettle_pitch']:.0f} Hz, \ and is sure of it \\ ({d['kettle_salience']:.2f}, \ against {d['bare_salience']:.2f} for the bare skin)."),
            (r"timpanists, \ and audiences", rf"name the note of the lowest ringing mode itself: \ {d['hz']:.0f} Hz. \\ Nobody tunes a kettledrum an octave away from where it sounds."),
            (r"so", r"a harmonic series fuses into one note; \ which octave the ear files it under \\ is a finer question, \ and not a settled one."),
        ], left=-6.5, text_left=-2.3, top=1.9, step=1.42, name_size=26, text_size=23, color=SKIN)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "There is a loose end here, and it is worth showing you. <bookmark mark='a'/> One, one and a "
            "half, two, two and a half. Double them: two, three, four, five. Those are harmonics two to five "
            "of a note an octave below the drum's lowest ringing mode, with the fundamental missing. "
            "<bookmark mark='b'/> Part 4's model of the ear, given the kettledrum's sound, reports exactly "
            f"that missing note, at {say(d['kettle_pitch'])} hertz, and with more confidence than it has "
            "about anything in the bare skin's sound. <bookmark mark='c'/> But ask a timpanist, or an audience, and they name the "
            f"note of the lowest ringing mode itself, at {say(d['hz'])} hertz. Nobody hears a kettledrum an "
            "octave below where it is written. <bookmark mark='d'/> So the model has the important thing "
            "right: these partials fuse into one clear note. Which octave the ear files that note under, "
            "when the lowest partial is itself strong, is a finer question, and the textbooks do not agree "
            "on the answer."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
