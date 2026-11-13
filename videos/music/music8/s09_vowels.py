from __future__ import annotations

import numpy as np

from videos.music.music8.common import *  # noqa: F403


class Vowels(SoundScene):
    def construct(self):
        chapter(self, 8, r"Vowels", r"Where do the formants come from?", lit=(1863,), extra=((1952, r"Peterson and Barney measure the vowels"),))
        self.worked()
        self.shapes()
        self.chart()
        self.quiz()

    # ------------------------------------------------------------------
    def worked(self):
        d = load("vowels")
        q = d["quarter"]
        n = d["shapes"]["neutral"]["formants"]
        title = label(r"A worked example: \ a mouth doing nothing", font_size=36).to_edge(UP, buff=0.4)
        tv = TubeView(width=7.0, bore=0.9, left="closed", right="open", color=VOICE).move_to(UP * 1.6)
        ends = VGroup(label(r"the folds", font_size=22, color=VOICE).next_to(tv, LEFT, buff=0.2), label(r"the lips", font_size=22, color=GREY_A).next_to(tv, RIGHT, buff=0.2),
                      label(rf"{d['length_cm']:.1f} cm", font_size=24, color=GREY_B).next_to(tv, DOWN, buff=0.15))
        ask = pause_card(r"With the tongue relaxed, \ a man's throat and mouth are roughly a plain tube, \ 17.5 cm long, \\ closed at the folds and open at the lips. \ Where are its first three resonances?", width=10.2, font_size=26).move_to(DOWN * 1.0)
        work = VGroup(MathTex(rf"\frac{{c}}{{4L}} = \frac{{343}}{{4 \times 0.175}} = {q[0]:.0f}\ \text{{Hz}}, \qquad 3 \times {q[0]:.0f} = {q[1]:.0f}, \qquad 5 \times {q[0]:.0f} = {q[2]:.0f}", font_size=34),
                      label(rf"Monochord's tube, \ with its end correction: \ {n[0]:.0f}, \ {n[1]:.0f}, \ {n[2]:.0f} Hz", font_size=26, color=VOICE),
                      label(r"the vowel in ``the'' and ``about'': \ a mouth at rest", font_size=28, color=TUNE)).arrange(DOWN, buff=0.3).move_to(DOWN * 1.2)
        with self.voiceover(
            "Where do the formants come from? From the first chapter of this part. A worked example. Relax "
            "your tongue and let your mouth hang slightly open. Your throat and mouth are now roughly a "
            "plain tube, seventeen and a half centimetres long in a man, closed at the folds and open at the "
            "lips. Where are its first three resonances? Pause, and work them out."
        ):
            self.play(FadeIn(title), FadeIn(tv), FadeIn(ends), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "A tube closed at one end: a quarter of a wave, and the odd multiples. The speed of sound over "
            f"four times the length is {say(q[0])} hertz; three times that is {say(q[1])}; five times, "
            f"{say(q[2])}. <bookmark mark='a'/> Monochord's tube, with its end correction, gives {say(n[0])}, "
            f"{say(n[1])} and {say(n[2])}. <bookmark mark='b'/> And that is a real vowel. It is the one in the "
            "word the, and at the start of about: the sound English speakers make when the mouth is doing "
            "nothing in particular. Five hundred, fifteen hundred, twenty-five hundred: a clarinet seventeen "
            "centimetres long."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(work[0]))
            vo.wait_until("a")
            self.play(FadeIn(work[1]))
            vo.wait_until("b")
            self.play(FadeIn(work[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shapes(self):
        d = load("vowels")
        sh, meas = d["shapes"], d["measured"]

        def tube(name, col):
            s = sh[name]
            parts = VGroup()
            x = 0.0
            for a, ln in zip(s["areas"], s["lengths"]):
                h = 0.34 * np.sqrt(a)
                w = 0.22 * ln
                parts.add(Rectangle(width=w, height=h, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.12).move_to(RIGHT * (x + w / 2)))
                x += w
            return parts

        g = axes([0, 3400], [0, 3], x_length=6.0, y_length=3.9, xlabel=r"frequency (Hz)", ylabel="", xticks=[0, 1000, 2000, 3000], yticks=[], font_size=20)
        g.move_to(RIGHT * 3.4 + DOWN * 0.5)
        rows, tubes, names = VGroup(), VGroup(), VGroup()
        specs = (("neutral", r"at rest", GREY_A, 2.4, None), ("a", r"`ah': \ a narrow throat, \ a wide mouth", VOICE, 1.4, "a"), ("i", r"`ee': \ a wide throat, \ a narrow gap", AIR, 0.4, "i"))
        for name, text, col, y, m in specs:
            t = tube(name, col).move_to(LEFT * 3.9 + UP * (1.9 - 1.95 * specs.index((name, text, col, y, m))))
            tubes.add(t)
            names.add(label(text, font_size=24, color=col).next_to(t, UP, buff=0.12))
            marks = VGroup(*[Line(g.ax.c2p(f, y - 0.28), g.ax.c2p(f, y + 0.28), color=col, stroke_width=6) for f in sh[name]["formants"]])
            if m:
                marks.add(*[Dot(g.ax.c2p(f, y), radius=0.085, color=WHITE) for f in meas[m]])
            rows.add(marks)
        key = VGroup(label(r"bars: \ the resonances of the tube", font_size=22, color=GREY_A), label(r"dots: \ measured, \ the average of 33 men", font_size=22)).arrange(DOWN, buff=0.06, aligned_edge=LEFT).next_to(g, UP, buff=0.2)
        fl = VGroup(label(r"folds", font_size=18, color=GREY_B).next_to(tubes[0], LEFT, buff=0.12), label(r"lips", font_size=18, color=GREY_B).next_to(tubes[0], RIGHT, buff=0.12))
        a, i = sh["a"]["formants"], sh["i"]["formants"]
        with self.voiceover(
            "Now move the tongue. Speaking is the art of changing the tube's shape, and the simplest change "
            "is to make one half of it narrow and the other half wide. <bookmark mark='a'/> Pull the tongue "
            "down and back: the throat narrows and the mouth opens wide. Monochord computes the resonances "
            f"of that two-part tube: {say(a[0])}, {say(a[1])} and {say(a[2])} hertz. The white dots are the "
            "formants of ah, measured from thirty-three men in 1952. <bookmark mark='b'/> Push the tongue up "
            "and forward instead: a wide throat behind a narrow gap at the roof of the mouth. The first "
            f"resonance drops to {say(i[0])} hertz and the second leaps to {say(i[1])}. That is ee. Two "
            "tubes of two widths are a cartoon of a mouth, and they land within a semitone or so of real "
            "ones. The rule to remember: opening the jaw raises the first formant; moving the tongue forward "
            "raises the second."
        ) as vo:
            self.play(FadeIn(tubes[0]), FadeIn(names[0]), FadeIn(fl), FadeIn(g), FadeIn(rows[0]), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(tubes[1]), FadeIn(names[1]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(tubes[2]), FadeIn(names[2]), FadeIn(rows[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chart(self):
        d = load("vowels")
        g = axes([200, 800], [700, 2500], x_length=6.4, y_length=4.4, xlabel=r"first formant (Hz): \ the jaw opens $\rightarrow$", ylabel=r"second formant (Hz): \ the tongue moves forward $\uparrow$", xticks=[300, 500, 700], yticks=[1000, 1500, 2000, 2500], font_size=20)
        g.move_to(LEFT * 2.9 + DOWN * 0.4)
        pts = VGroup(*[VGroup(Dot(g.ax.c2p(c["f1"], c["f2"]), radius=0.08, color=VOICE), label(c["word"], font_size=24, color=GREY_A).next_to(g.ax.c2p(c["f1"], c["f2"]), RIGHT, buff=0.12)) for c in d["chart"]])
        card = history_card(1952, r"Gordon Peterson and Harold Barney, \ Bell Labs", r"seventy-six speakers say ten words into a spectrograph; the vowels fall into ten islands on a map of two formants.", width=5.2, font_size=20).move_to(RIGHT * 4.0 + UP * 1.6)
        end = VGroup(label(r"a vowel is a place on this map,", font_size=28, color=TUNE), label(r"whatever the pitch of the voice", font_size=28, color=TUNE)).arrange(DOWN, buff=0.1).move_to(RIGHT * 4.0 + DOWN * 1.3)
        with self.voiceover(
            "Put every vowel on one map: the first formant across, the second upward. In 1952 Gordon "
            "Peterson and Harold Barney had seventy-six people say ten words, heed, hid, head, had, and so "
            "on, into a spectrograph. <bookmark mark='a'/> These are the averages for the men. Heed, with the "
            "tongue high and forward, is at the top left. Hod, with the jaw dropped, is at the far right. "
            "Who'd, with the tongue back and the lips rounded, is at the bottom left. The map of formants "
            "is a map of the mouth. <bookmark mark='b'/> And this is what a vowel is: not a pitch, not a set "
            "of harmonics, but a place on this map. Your ear reads two or three bumps in a spectrum and "
            "tells you what shape somebody's mouth is in."
        ) as vo:
            self.play(FadeIn(g), FadeIn(card))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(end))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("vowels")
        c = clip("vowels.quiz")
        q = listen_card(r"One note, \ sung on three vowels. \\ Which is ``heed'', \ which is ``hod'', \ which is ``who'd''?", width=8.8, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes(("A", "B", "C"), buff=1.2, width=2.6, height=1.3).move_to(UP * 0.2)
        with self.voiceover(
            "Test it. Monochord will sing one note on three vowels: the ones in heed, hod and who'd, in some "
            "order. The pitch is the same each time. Which is which?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"one note, \ three vowels", kind="synthesized", detail=r"a model of a voice", corner=DL, tag_corner=DR)
            for ev, b in zip("ABC", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 1.3)
        ans = VGroup(*[label(rf"``{w}''", font_size=30, color=VOICE).next_to(b, DOWN, buff=0.25) for w, b in zip(d["order_words"], bx)])
        with self.voiceover(
            f"Who'd, hod, heed. You did not have to think. Now the other way round: one vowel, three "
            "different pitches."
        ):
            self.play(FadeOut(q), FadeIn(ans))
        c2 = clip("vowels.same")
        note = listen_note(r"The vowel of ``hod'' on three notes. \\ The harmonics move; \ the formants stay.", width=7.0, font_size=24).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(note), run_time=0.4)
        with self.listen(c2) as snd:
            window(snd, r"one vowel, \ three notes", kind="synthesized", detail=r"a model of a voice", corner=UL, tag_corner=UR)
            for k, b in enumerate(bx):
                t0 = snd.time_of(f"p{k}")
                pulse(snd, ans[1], t0, t0 + 1.2, buff=0.1)
        with self.voiceover(
            "Still ah, every time, although not one harmonic was at the same frequency twice. The filter "
            "stayed still while the source moved under it. Hold on to that picture, because singers break "
            "it on purpose."
        ):
            self.play(FadeOut(note))
        self.wait(0.3)
        self.clear_scene()
