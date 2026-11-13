from __future__ import annotations

import numpy as np

from videos.music.music8.common import *  # noqa: F403


class Holes(SoundScene):
    def construct(self):
        chapter(self, 3, r"Holes", r"How does one pipe play a scale?", lit=(1863,), extra=((1847, r"Boehm's flute"),))
        self.tone_holes()
        self.worked()
        self.register()

    # ------------------------------------------------------------------
    def tone_holes(self):
        d = load("holes")
        rows = d["rows"]

        def pipe(y, hole=None, cut=False, col=CLAR):
            w = 7.2 if not cut else 5.4
            tv = TubeView(width=w, bore=0.45, left="closed", right="open", color=col).move_to(LEFT * (3.2 + (7.2 - w) / 2) + UP * y)
            g = VGroup(tv)
            if hole is not None:
                x = tv.p(0.75)[0]
                top = tv.p(0.75)[1] + 0.225
                g.add(Line(np.array([x - hole, top, 0]), np.array([x + hole, top, 0]), color=BLACK, stroke_width=7))
            return g

        whole = pipe(2.0)
        cutp = pipe(0.9, cut=True)
        holes = [pipe(-0.2 - 1.1 * k, hole=h) for k, h in enumerate((0.22, 0.12, 0.06))]
        t_whole = label(rf"every hole shut: \ {d['whole_hz']:.0f} Hz", font_size=24).next_to(whole, RIGHT, buff=0.3)
        t_cut = label(rf"sawn off at three quarters: \ {d['cut_hz']:.0f} Hz", font_size=24).next_to(cutp, RIGHT, buff=0.3 + 1.8)
        t_h = VGroup(*[label(rf"a hole {2 * r['radius_mm']:.0f} mm across: \ {r['hz']:.0f} Hz, \\ {r['cents_below_cut']:.0f} cents flat of the sawn pipe", font_size=22, color=TUNE if k else GOOD).next_to(h, RIGHT, buff=0.3)
                       for k, (r, h) in enumerate(zip(rows, holes))])
        with self.voiceover(
            "A pipe has one length, and a tune needs many notes. The oldest answer is at least forty thousand "
            "years old: cut holes in the side. <bookmark mark='a'/> Here is our clarinet pipe with every hole "
            f"shut, sounding at {say(d['whole_hz'])} hertz. <bookmark mark='b'/> Saw it off at three quarters "
            f"of its length and it sounds at {say(d['cut_hz'])}: a fourth higher. <bookmark mark='c'/> Now, "
            "instead of sawing, open a hole at that point, as wide as the pipe itself. To the air column, a "
            "hole that wide is very nearly the end of the pipe: the pressure escapes there, and the wood "
            f"beyond it hardly matters. Monochord gets {say(rows[0]['hz'])} hertz. <bookmark mark='d'/> But "
            "fingers cannot cover a hole fifteen millimetres across. Make the hole smaller, and it lets the "
            f"pressure out less completely. At eight millimetres the note is {say(rows[1]['cents_below_cut'])} "
            f"cents flat of the sawn pipe; at four millimetres, {say(rows[2]['cents_below_cut'])} cents, nearly "
            "a whole tone. A small hole behaves like a big hole further down. So a maker has two things to "
            "play with for every note: where the hole is, and how big. That is how the holes of a recorder "
            "can sit under the fingers of one hand, instead of where the arithmetic first puts them."
        ) as vo:
            self.play(FadeIn(whole))
            vo.wait_until("a")
            self.play(FadeIn(t_whole))
            vo.wait_until("b")
            self.play(FadeIn(cutp), FadeIn(t_cut))
            vo.wait_until("c")
            self.play(FadeIn(holes[0]), FadeIn(t_h[0]))
            vo.wait_until("d")
            self.play(FadeIn(holes[1]), FadeIn(t_h[1]))
            self.play(FadeIn(holes[2]), FadeIn(t_h[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worked(self):
        title = label(r"A worked example: \ where do the holes go?", font_size=36).to_edge(UP, buff=0.4)
        ask = pause_card(r"A flute's pipe, \ every hole shut, \ sounds a note. \ Suppose the holes are as wide as the pipe. \\ Where must a hole be opened to sound the note a fifth higher? \ An octave higher?", width=10.0, font_size=26).move_to(UP * 1.3)
        tv = TubeView(width=12.0, bore=0.5, left="open", right="open", color=FLUTE).move_to(DOWN * 1.0)
        marks = VGroup()
        for k, (frac, name, ratio) in enumerate(((8 / 9, r"a tone", r"\tfrac89"), (4 / 5, r"a third", r"\tfrac45"), (3 / 4, r"a fourth", r"\tfrac34"), (2 / 3, r"a fifth", r"\tfrac23"), (3 / 5, r"a sixth", r"\tfrac35"), (1 / 2, r"an octave", r"\tfrac12"))):
            p = tv.p(frac) + UP * 0.25
            marks.add(VGroup(Dot(p, radius=0.09, color=BLACK).set_stroke(GREY_A, 1.5), label(name, font_size=22, color=TUNE).next_to(p, UP, buff=0.15 + 0.4 * (k % 2)),
                             MathTex(ratio, font_size=30, color=GREY_A).next_to(tv.p(frac) + DOWN * 0.25, DOWN, buff=0.15)))
        ml = label(r"the mouth hole", font_size=20, color=GREY_B).next_to(tv.p(0.0), DOWN, buff=0.45)
        end = label(r"the same fractions as the bridge of Part 1's monochord: \ a flute is a monochord made of air", font_size=28, color=TUNE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A worked example. Take a flute's pipe, open at both ends, with every hole shut, and suppose its "
            "holes are as wide as the pipe, so that an open hole is as good as a saw. Where must a hole be, "
            "to sound the note a fifth above the pipe's own? And where for the octave? Pause, and say."
        ):
            self.play(FadeIn(title), FadeIn(ask, shift=UP * 0.2), FadeIn(tv), FadeIn(ml))
        self.wait(1.5)
        with self.voiceover(
            "The frequency of a pipe goes as one over its length. A fifth is three halves the frequency, so "
            "the pipe must end at two thirds of its length. <bookmark mark='a'/> The octave is twice the "
            "frequency: half the length. And the notes between follow: eight ninths for a tone, four fifths "
            "for a third, three quarters for a fourth. <bookmark mark='b'/> You have seen these fractions "
            "before. They are where the bridge of the monochord stood in Part 1. A flute is a monochord made "
            "of air; the six finger holes of a tin whistle are Pythagoras's ratios, drilled. Real "
            "flutes then cheat, hole by hole, in the way you have just seen, to bring the holes within reach."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(marks[3]))
            vo.wait_until("a")
            self.play(FadeIn(marks[5]))
            self.play(LaggedStart(*[FadeIn(marks[k]) for k in (0, 1, 2, 4)], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(end))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def register(self):
        d = load("holes")
        c = clip("holes.register")
        g = faxes(80, 1000, [-22, 36], x_length=6.4, y_length=3.0, ylabel=r"how hard the air column pushes back (dB)", yticks=[-20, 0, 20], fticks=(100, 200, 500, 1000), font_size=20)
        g.move_to(LEFT * 3.0 + DOWN * 1.0)
        plain = fcurve(g, d["f"], d["z_plain_db"], GREY_B)
        reg = fcurve(g, d["f"], d["z_register_db"], CLAR)
        pp, pr = d["peaks_plain"], d["peaks_register"]
        key = VGroup(label(r"every hole shut", font_size=22, color=GREY_B), label(r"a pinhole open, \ a quarter of the way down", font_size=22, color=CLAR)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).to_corner(UL, buff=0.45)
        note = listen_note(r"The pipe's lowest note; \ then the same pipe \\ with only a pinhole opened.", width=4.8, font_size=24).move_to(RIGHT * 4.0 + UP * 2.0)
        with self.voiceover(
            "Seven or eight finger holes give a scale of seven or eight notes. To go on upwards, every "
            "woodwind does the same thing: it jumps to the pipe's next resonance and uses the same holes "
            "again. A flute's next resonance is twice the first, so its second octave repeats the fingering "
            "of the first. <bookmark mark='a'/> But a clarinet's next resonance is three times the first: an "
            "octave and a fifth above, nineteen semitones. To get there, a clarinet has a register key, "
            "which opens a pinhole about a quarter of the way down the pipe. <bookmark mark='b'/> Here is "
            f"what the pinhole does to the pipe. The lowest resonance moves from {say(pp[0])} hertz to "
            f"{say(pr[0])}, where its harmonics no longer line up with anything. The second resonance barely "
            f"moves: {say(pp[1])} to {say(pr[1])}. Nothing has been taken away. The lowest resonance has "
            "been put out of tune with its helpers, and the reed, which needs a whole family of resonances "
            "behind it, gives up on it and takes the next. Listen."
        ) as vo:
            self.play(FadeIn(g), Create(plain), FadeIn(key[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(note))
            vo.wait_until("b")
            self.play(Create(reg), FadeIn(key[1]), run_time=2.0)
        with self.listen(c) as snd:
            window(snd, r"low, \ then with the register hole", detail=r"a model clarinet", corner=DL, tag_corner=DR)
            pulse(snd, key[0], snd.time_of("low"), snd.time_of("low") + 1.6, buff=0.08)
            pulse(snd, key[1], snd.time_of("high"), snd.time_of("high") + 1.6, buff=0.08)
        res = VGroup(label(rf"{d['low_hz']:.0f} Hz, \ then {d['high_hz']:.0f} Hz", font_size=30, color=CLAR),
                     label(rf"{d['ratio']:.2f} times: \ a twelfth, \\ {d['interval_cents'] - d['twelfth_cents']:.0f} cents wide in this simple model", font_size=24, color=GREY_A),
                     label(r"a clarinet needs fingerings \\ for nineteen semitones before they repeat;", font_size=24, color=TUNE), label(r"a flute or an oboe, \ for twelve", font_size=24, color=TUNE)).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(RIGHT * 3.6 + DOWN * 0.9)
        with self.voiceover(
            f"From {say(d['low_hz'])} hertz to {say(d['high_hz'])}: three times the frequency, a twelfth. In "
            f"this simple model it comes out {say(d['interval_cents'] - d['twelfth_cents'])} cents wide; real "
            "clarinets are shaped, bore and holes together, to pull it back. <bookmark mark='a'/> The price of "
            "that twelfth is paid by every clarinettist. Between the top of the first register and the bottom "
            "of the second there are nineteen semitones to cover, not twelve, so a clarinet needs more holes "
            "and more keys than a flute or an oboe, and the same fingering means a different note in each "
            "register. Players call the join the break, and spend years smoothing it."
        ) as vo:
            self.play(FadeOut(note), FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("a")
            self.play(FadeIn(res[2]), FadeIn(res[3]))
        self.wait(0.3)
        self.clear_scene()
