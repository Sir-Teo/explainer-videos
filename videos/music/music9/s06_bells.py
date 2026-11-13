from __future__ import annotations

import numpy as np

from videos.music.music9.common import *  # noqa: F403


class Bells(SoundScene):
    def construct(self):
        chapter(self, 5, r"Bells", r"What note is a bell playing?", lit=(1636,), extra=((1644, r"the Hemonys' tuned carillon"),))
        self.partials()
        self.apart()
        self.strike()
        self.third()

    def axis(self):
        d = load("bells")
        g = axes([0.3, 4.3], [0, 1.6], x_length=11.0, y_length=2.2, xlabel=r"frequency, \ in units of the bell's note", ylabel="", xticks=[0.5, 1, 1.5, 2, 2.5, 3, 4], yticks=[], font_size=20)
        marks = VGroup()
        for q in d["partials"]:
            marks.add(VGroup(Line(g.ax.c2p(q["ratio"], 0), g.ax.c2p(q["ratio"], 1.3 * q["amp"]), color=BRONZE, stroke_width=7),
                             label(q["name"], font_size=20, color=BRONZE).next_to(g.ax.c2p(q["ratio"], 1.3 * q["amp"]), UP, buff=0.08)))
        return d, g, marks

    # ------------------------------------------------------------------
    def partials(self):
        d, g, marks = self.axis()
        VGroup(g, marks).move_to(DOWN * 1.2)
        bell = VGroup(ArcBetweenPoints(LEFT * 1.3 + DOWN * 0.9, UP * 1.0 + LEFT * 0.45, angle=-0.9, color=BRONZE, stroke_width=6),
                      ArcBetweenPoints(UP * 1.0 + RIGHT * 0.45, RIGHT * 1.3 + DOWN * 0.9, angle=-0.9, color=BRONZE, stroke_width=6),
                      Line(UP * 1.0 + LEFT * 0.45, UP * 1.0 + RIGHT * 0.45, color=BRONZE, stroke_width=6), Line(LEFT * 1.3 + DOWN * 0.9, RIGHT * 1.3 + DOWN * 0.9, color=BRONZE, stroke_width=3)).scale(0.8).move_to(LEFT * 4.6 + UP * 2.1)
        card = history_card(1644, r"Frans and Pieter Hemony, \ with Jacob van Eyck", r"in Zutphen they turn each bell on a lathe until five of its partials are in tune: the first true carillon.", width=5.8, font_size=20).move_to(RIGHT * 2.6 + UP * 2.3)
        with self.voiceover(
            "A bell is a thick, curved shell of bronze, and its modes are the hardest of all to compute. So "
            "I will not pretend: these partials are measurements of real bells, not Monochord's own. Here "
            "they are, for a well-made church bell, each with the name founders give it. <bookmark mark='a'/> "
            "The lowest is the hum. An octave above it, the prime. Then the tierce, the quint, and the "
            "nominal, an octave above the prime. Higher still, a twelfth and a double octave. "
            "<bookmark mark='b'/> A raw casting does not come out like this. Its partials are wherever the "
            "mould happened to put them. In 1644, in the Dutch town of Zutphen, the brothers Frans and "
            "Pieter Hemony, advised by a blind musician with a famous ear, Jacob van Eyck, began turning "
            "each bell on a lathe: shaving metal from rings inside it, each ring lowering some partials "
            "more than others, until five of them stood in these ratios. Every bell in a tuned carillon has "
            "been through that."
        ) as vo:
            self.play(FadeIn(bell), FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.5), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(card))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def apart(self):
        d, g, marks = self.axis()
        c = clip("bells.apart")
        VGroup(g, marks).move_to(UP * 0.6)
        names = [q["name"] for q in d["partials"]]
        note = listen_note(r"Five partials of one bell, \ one at a time; \ then the bell. \\ Can you still hear each of them inside it?", width=8.6, font_size=24).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "You can learn to hear these inside a bell, the way bell tuners do. Here are the five lowest, "
            "one at a time: hum, prime, tierce, quint, nominal. Then the bell. Try to pick each of them out "
            "again once they are sounding together."
        ):
            self.play(FadeIn(g), FadeIn(marks), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"five partials, \ then the bell", kind="synthesized", detail=r"measured partials", corner=UL, tag_corner=UR)
            for n in ("hum", "prime", "tierce", "quint", "nominal"):
                t0 = snd.time_of(n)
                pulse(snd, marks[names.index(n)], t0, t0 + 1.0, buff=0.12)
            pulse(snd, marks, snd.time_of("all"), snd.time_of("all") + 2.8, buff=0.15)
        with self.voiceover(
            "The hum lingers longest, under everything. The tierce is the easiest to find: it is the one "
            "that makes the bell sound sad. A tuner listens for each in turn, with a tuning fork or a "
            "meter, and knows which ring of metal inside the bell to shave in order to move it."
        ):
            self.play(FadeOut(note))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def strike(self):
        d, g, marks = self.axis()
        c = clip("bells.strike")
        VGroup(g, marks).move_to(UP * 0.7)
        names = [q["name"] for q in d["partials"]]
        three = VGroup(*[marks[names.index(n)] for n in ("nominal", "twelfth", "upper octave")])
        note = listen_note(r"The bell; \ then only three of its partials, \ at 2, \ 3 and 4 times its note. \\ Does the note change?", width=8.4, font_size=24).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "So what note does a bell play? Strike one, and for the first instant you hear a clear pitch, "
            "the strike note. Founders have always known an awkward thing about it. <bookmark mark='a'/> It "
            "is decided mostly by three high partials: the nominal, the twelfth and the double octave, at "
            "two, three and four times the note. Two, three, four: a harmonic series with its first member "
            "missing. Part 4 told us what the ear does with that. Listen to the whole bell, and then to "
            "those three partials alone."
        ) as vo:
            self.play(FadeIn(g), FadeIn(marks))
            vo.wait_until("a")
            self.play(Indicate(three, color=WHITE, scale_factor=1.1), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"a bell, \ then three of its partials", kind="synthesized", detail=r"measured partials", corner=UL, tag_corner=UR)
            pulse(snd, marks, snd.time_of("whole"), snd.time_of("whole") + 2.6, buff=0.15)
            pulse(snd, three, snd.time_of("three"), snd.time_of("three") + 2.6, buff=0.12)
        res = VGroup(label(rf"Part 4's model of the ear, \ given the three: \ {d['heard_upper_only']:.0f} Hz", font_size=28, color=EAR),
                     label(rf"the bell's prime: \ {d['prime']:.0f} Hz. \ No partial at that frequency was sounding.", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The colour changes, and the note stays. Part 4's model of the ear, given only those three "
            f"partials, reports a pitch of {say(d['heard_upper_only'])} hertz, where nothing was sounding. "
            "The strike note of a bell is a missing fundamental. That is why the founder then tunes the "
            "prime, the partial that really is at that frequency, to agree with it. When the two disagree, "
            "the bell sounds as if it cannot make up its mind."
        ):
            self.play(FadeOut(note), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def third(self):
        d = load("bells")
        c = clip("bells.quiz")
        q = listen_card(r"Two bells on the same note. \ One is the kind cast for four centuries. \\ In the other, \ one partial has been moved. \ Which is the old kind?", width=9.2, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes(buff=2.6, width=3.0, height=1.3).move_to(DOWN * 0.2)
        with self.voiceover(
            "Now look at the third partial, the tierce. It stands at one point two times the note: six to "
            "five, a minor third. Every traditional bell has one. Hum, prime, tierce and quint spell out a "
            "minor chord, and the bell sounds it all by itself. Two bells, on the same note. One is the kind "
            "that has been cast for four centuries. In the other, one partial has been moved. Which is the "
            "old kind?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"two bells, \ one note", kind="synthesized", detail=r"partials of a minor-third and a major-third bell", corner=DL, tag_corner=DR)
            for ev, b in zip("AB", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.6)
        ans = VGroup(VGroup(label(r"the new kind", font_size=28, color=TUNE), label(rf"tierce at 1.25: \ a major third, \ {d['major_cents']:.0f} cents", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.08).next_to(bx[0], DOWN, buff=0.25),
                     VGroup(label(r"the old kind", font_size=28, color=BRONZE), label(rf"tierce at 1.2: \ a minor third, \ {d['tierce_cents']:.0f} cents", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.08).next_to(bx[1], DOWN, buff=0.25))
        with self.voiceover(
            "B is the old kind: darker, with that slightly mournful colour that says bell. It is why a "
            "carillon playing a cheerful tune in a major key always sounds a little wistful: every note of "
            "the major chord brings its own minor third along. <bookmark mark='a'/> For centuries founders "
            "tried to cast a bell with a major third and failed. It was done in the nineteen eighties, in the "
            "Netherlands, and not on a lathe: engineers at Eindhoven let a computer reshape the bell's profile, "
            "thousands of times, until the third partial moved up and the others stayed put. The answer "
            "was a bell with a bulge in its side that no founder would have drawn. Here is a major chord, "
            "first on three bells of the old kind, then on three of the new."
        ) as vo:
            self.play(FadeOut(q), FadeIn(ans))
            vo.wait_until("a")
            story = VGroup(label(r"the 1980s, \ the Netherlands: \ a bell's profile reshaped by computer, \ thousands of times,", font_size=26, color=GREY_A),
                           label(r"until the third partial rose from 1.2 to 1.25 and the others stayed put", font_size=26, color=TUNE)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
            self.play(Indicate(ans[0], color=WHITE, scale_factor=1.05), FadeIn(story[0]))
            self.play(FadeIn(story[1]))
        c2 = clip("bells.chords")
        with self.listen(c2) as snd:
            window(snd, r"a major chord: \ old bells, \ then new", kind="synthesized", detail=r"three bells at a time", corner=UL, tag_corner=UR)
            pulse(snd, bx[1], snd.time_of("minor"), snd.time_of("minor") + 3.0)
            pulse(snd, bx[0], snd.time_of("major"), snd.time_of("major") + 3.0)
        with self.voiceover(
            "The first chord argues with itself, major thirds between the bells against the minor third "
            "inside each one. The second is at peace. Some carillons have been built from the new bells. "
            "Most listeners, it turns out, miss the argument."
        ):
            self.play(Indicate(ans[1], color=WHITE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
