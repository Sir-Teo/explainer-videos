from __future__ import annotations

import numpy as np

from videos.music.music4.common import *  # noqa: F403


def recipe(on, width=2.6, height=1.3, noise=False) -> VGroup:
    """Eight partials as bars: those in ``on`` are filled, the rest are outlines."""
    amps = np.array([1.0 if k in on else 0.001 for k in range(1, 9)])
    g = partial_bars(amps, width=width, height=height, db=False, font_size=16)
    slot = width / 8
    for k in range(1, 9):
        if k not in on:
            g.add(Rectangle(width=slot * 0.62, height=height, stroke_color=GREY_D, stroke_width=1.2).move_to(g.base.get_left() + RIGHT * slot * (k - 0.5) + UP * height / 2))
    if noise:
        g.add(Rectangle(width=slot * 2.3, height=height * 0.55, stroke_width=0, fill_color=GREY_B, fill_opacity=0.5)
              .move_to(g.base.get_left() + RIGHT * slot * 1.15 + UP * height * 0.275))
    return g


class Missing(SoundScene):
    def construct(self):
        chapter(self, 7, r"The pitch that is not there", r"What do you hear when a note's fundamental is missing?", lit=(1863,),
                extra=((1841, r"Seebeck's siren"), (1940, r"Schouten's residue"), (1951, r"Licklider's model")))
        self.test()
        self.distortion()
        self.model()
        self.worked()
        self.shift()
        self.uses()

    # ------------------------------------------------------------------
    def test(self):
        d = load("pitch")
        c = clip("pitch.missing")
        q = listen_card(r"One note, \ four ways. \\ Does the pitch of 2 and 3 stay with 1 and 4, \ or does it jump up?", width=9.4).to_edge(UP, buff=0.4)
        rs = VGroup(recipe(range(1, 9)), recipe(range(4, 9)), recipe(range(4, 9), noise=True), recipe([1])).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.5)
        tags = VGroup(*[label(t, font_size=22, color=GREY_A).next_to(r, UP, buff=0.2) for t, r in
                        zip((r"1: \ partials 1 to 8", r"2: \ partials 4 to 8", r"3: \ the same, \ over low noise", r"4: \ partial 1 alone"), rs)])
        with self.voiceover(
            "Now we can go back to the puzzle that ended Part 3, and listen to it properly. One note, a low C, "
            "four ways. First with its first eight partials. Second, with the lowest three removed, so that "
            "nothing is left at the note's own frequency. Third, the same again, with a band of low noise added "
            "where the missing partials were. Fourth, the lowest partial alone. Listen to the pitch. Do the "
            "second and third stay with the first and the fourth, or do they jump up?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), LaggedStart(*[FadeIn(VGroup(r, t)) for r, t in zip(rs, tags)], lag_ratio=0.5), run_time=6.0)
        with self.listen(c) as snd:
            window(snd, r"1, \ 2, \ 3, \ 4", kind="synthesized", detail=r"sums of sines; \ filtered noise", corner=DL, tag_corner=DR)
            for ev, r in zip(("full", "upper", "noise", "pure"), rs):
                t0 = snd.time_of(ev)
                pulse(snd, r, t0, t0 + 1.5, buff=0.15)
        up = d["rows"][2]
        res = VGroup(label(r"all four have the same pitch", font_size=34, color=GOOD),
                     label(rf"in sound 2, \ the level at the note's own frequency: \ {abs(up['level_at_f0_db']):.0f} dB below its partials", font_size=26, color=GREY_A)
                     ).arrange(DOWN, buff=0.2).move_to(DOWN * 2.6)
        with self.voiceover(
            "They stay. All four have the same pitch, the low C. The second and third sound thinner, more nasal, "
            "but not higher. And yet in the second sound the level at the note's own frequency is "
            f"{say(abs(up['level_at_f0_db']))} decibels below its partials. For every practical purpose there is "
            "nothing there. You are hearing the pitch of a frequency that is absent."
        ):
            self.play(FadeOut(q), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def distortion(self):
        c1 = history_card(1863, r"Helmholtz's answer",
                          r"the ear distorts. Partials 4 and 5 beat together inside it and create a new tone at their "
                          r"difference: the missing fundamental, put back by the ear.", width=5.8).to_corner(UL, buff=0.45)
        eq = MathTex(r"5f_0 - 4f_0 = f_0", font_size=40, color=BAD).next_to(c1, DOWN, buff=0.35)
        c2 = history_card(1954, r"J. C. R. Licklider's test",
                          r"if a real tone at $f_0$ were being created on the membrane, noise at $f_0$ would mask it, "
                          r"exactly as in chapter 5.", width=5.8).move_to(RIGHT * 3.4 + UP * 1.9)
        r3 = recipe(range(4, 9), noise=True, width=3.4, height=1.5).next_to(c2, DOWN, buff=0.45)
        out = label(r"sound 3: \ the noise is there. \ The pitch survives.", font_size=28, color=GOOD).next_to(r3, DOWN, buff=0.3)
        c3 = history_card(1940, r"J. F. Schouten, \ Eindhoven",
                          r"the low pitch comes from the upper partials themselves, taken together. He names it the "
                          r"\textbf{residue}.", width=5.8).next_to(eq, DOWN, buff=0.4).align_to(c1, LEFT)
        with self.voiceover(
            "Helmholtz had an answer, and it is a good one. The ear distorts. When partials four and five arrive "
            "together, they beat, and a distorting ear turns that beat into a new tone at the difference of their "
            "frequencies, <bookmark mark='a'/> which is exactly the missing fundamental. The tone you heard under "
            "the two tones at the start of this part is that very thing. So perhaps the ear simply puts the "
            "fundamental back. <bookmark mark='b'/> There is a way to check, and you have just taken part in it. "
            "If a real tone were being created at the fundamental, then noise at that frequency would mask it, as "
            "in chapter five. <bookmark mark='c'/> Sound three had that noise. The pitch survived. So the low "
            "pitch is not a tone at the fundamental, anywhere: not in the air, and not on the membrane. "
            "<bookmark mark='d'/> In 1940 the Dutch physicist Jan Schouten gave it a name. The pitch comes from "
            "the upper partials themselves, taken together. He called it the residue. Seebeck had been right "
            "about his siren a century earlier, and Ohm, and Helmholtz, had been wrong."
        ) as vo:
            self.play(FadeIn(c1))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(FadeIn(c2))
            vo.wait_until("c")
            self.play(FadeIn(r3), FadeIn(out))
            vo.wait_until("d")
            self.play(FadeIn(c3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def model(self):
        d = load("pitch")
        card = history_card(1951, r"J. C. R. Licklider",
                            r"in every band of the ear, compare the nerve's firing with a delayed copy of itself. "
                            r"Find the delay at which the pattern repeats.", width=5.0).to_corner(UL, buff=0.4)
        lag = d["lags_ms"]
        gs, cs = VGroup(), VGroup()
        cols = (GREY_A, TUNE, AIR)
        names = (r"partial 1 alone", r"partials 1 to 8", r"partials 4 to 8")
        for k, (key, col, nm) in enumerate(zip(("pure", "full", "upper"), cols, names)):
            g = axes([0, 20], [0, 1.1], x_length=6.6, y_length=1.25, xlabel=r"delay (ms)" if k == 2 else "", ylabel="",
                     xticks=[0, 5, 10, 15, 20] if k == 2 else None, yticks=[], font_size=18)
            gs.add(g)
        gs.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(RIGHT * 3.0 + DOWN * 0.1)
        for g, key, col, nm in zip(gs, ("pure", "full", "upper"), cols, names):
            cu = curve(g.ax, lag, d[f"acf_{key}"], col, stroke_width=2.5)
            cs.add(VGroup(cu, label(nm, font_size=22, color=col).next_to(g.ax.c2p(20, 1.0), UL, buff=0.05)))
        per = d["period_ms"]
        mark = DashedLine(gs[0].ax.c2p(per, 1.2), gs[2].ax.c2p(per, 0), color=GOOD, stroke_width=2.5)
        ml = label(rf"{per:.2f} ms", font_size=24, color=GOOD).next_to(mark, UP, buff=0.05)
        rows = d["rows"]
        res = VGroup(label(r"the model's pitch", font_size=24, color=GREY_B),
                     *[label(rf"{nm}: \ {r['pitch']:.1f} Hz", font_size=26, color=col) for nm, r, col in zip(names, rows, cols)],
                     label(rf"the note: \ {d['f0']:.1f} Hz", font_size=26, color=GOOD)).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        res.next_to(card, DOWN, buff=0.45).align_to(card, LEFT)
        with self.voiceover(
            "What could do that? The second clock. In 1951 Joseph Licklider proposed a machine. Take each band "
            "of the ear, and compare the nerve's firing there with a delayed copy of itself. Slide the delay, "
            "and look for the delay at which the pattern lines up with itself again. Then add up the answers "
            "from all the bands. <bookmark mark='a'/> Monochord has that machine. Give it the lowest partial "
            "alone: a pure tone repeats after one period, and the curve peaks at "
            f"{say(d['period_ms'], 2)} milliseconds. <bookmark mark='b'/> Give it all eight partials. Each band "
            "has its own faster rhythm, but they all come back into step at the same delay. <bookmark mark='c'/> "
            "Now give it partials four to eight only. The fourth partial repeats four times in that interval, "
            "the fifth five times, the sixth six. The first moment at which every one of them is back where it "
            f"started is still {say(d['period_ms'], 2)} milliseconds. <bookmark mark='d'/> The machine reports "
            f"{say(rows[0]['pitch'], 1)}, {say(rows[1]['pitch'], 1)} and {say(rows[2]['pitch'], 1)} hertz. The "
            "same pitch, three times. It never looked for energy at the fundamental. It looked for the period."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(gs[0]), Create(cs[0][0]), FadeIn(cs[0][1]), run_time=1.5)
            self.play(Create(mark), FadeIn(ml))
            vo.wait_until("b")
            self.play(FadeIn(gs[1]), Create(cs[1][0]), FadeIn(cs[1][1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(gs[2]), Create(cs[2][0]), FadeIn(cs[2][1]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worked(self):
        title = label(r"A worked example: \ three partials, \ one pitch", font_size=36).to_edge(UP, buff=0.45)
        g = axes([0, 1200], [0, 1.2], x_length=8.6, y_length=1.8, xlabel=r"frequency (Hz)", ylabel="", xticks=[0, 200, 400, 600, 800, 1000, 1200], yticks=[], font_size=20)
        g.move_to(UP * 1.2)
        lines = VGroup(*[Line(g.ax.c2p(f, 0), g.ax.c2p(f, 1.0), color=TUNE, stroke_width=7) for f in (600, 800, 1000)])
        ghosts = VGroup(*[DashedLine(g.ax.c2p(f, 0), g.ax.c2p(f, 1.0), color=GREY_C, stroke_width=2.5, dash_length=0.07) for f in (200, 400)])
        ask = pause_card(r"A sound has three partials: \ 600, \ 800 and 1000 Hz. \\ What pitch do you hear?", width=7.4).move_to(DOWN * 1.6)
        steps = VGroup(label(r"periods: \ $\tfrac{1}{600}$, \ $\tfrac{1}{800}$, \ $\tfrac{1}{1000}$ s", font_size=30),
                       label(r"all three repeat together every \ $\tfrac{1}{200}$ s \ = \ 5 ms", font_size=30),
                       label(r"pitch: \ 200 Hz, \ the largest frequency that divides all three", font_size=32, color=GOOD)).arrange(DOWN, buff=0.22).move_to(DOWN * 1.7)
        with self.voiceover(
            "A worked example. A sound has just three partials: six hundred, eight hundred and a thousand hertz. "
            "What pitch do you hear? Pause and decide."
        ):
            self.play(FadeIn(title), FadeIn(g), FadeIn(lines), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "Think in time. Six hundred hertz repeats three times in five milliseconds, eight hundred repeats "
            "four times, a thousand repeats five times. Five milliseconds is the shortest time in which all three "
            "come round together. <bookmark mark='a'/> So the pitch is two hundred hertz: the largest frequency "
            "that divides all three. These are the third, fourth and fifth partials of a note whose first and "
            "second are not there. The ear does arithmetic, and the operation is the greatest common divisor."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(steps[0]), FadeIn(steps[1]))
            vo.wait_until("a")
            self.play(FadeIn(steps[2]), LaggedStart(*[Create(x) for x in ghosts], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shift(self):
        d = load("pitch")
        c = clip("pitch.shift")
        g = axes([600, 1800], [0, 1.2], x_length=9.0, y_length=1.7, xlabel=r"frequency (Hz)", ylabel="", xticks=[800, 1000, 1200, 1400, 1600], yticks=[], font_size=20)
        g.move_to(UP * 1.5)
        plain = VGroup(*[Line(g.ax.c2p(200 * k, 0), g.ax.c2p(200 * k, 1.0), color=TUNE, stroke_width=6) for k in range(4, 9)])
        moved = VGroup(*[Line(g.ax.c2p(f, 0), g.ax.c2p(f, 1.0), color=BAD, stroke_width=6) for f in d["shift_partials"]])
        q = listen_note(r"Five partials 200 Hz apart. \ Then all five moved up by 30 Hz: \\ still 200 Hz apart. \ Does the pitch change?", width=9.0).move_to(DOWN * 1.5)
        with self.voiceover(
            "That was easy, because the partials were exact multiples of something. Schouten asked the awkward "
            "question: what if they are not? <bookmark mark='a'/> Take five partials, eight hundred to sixteen "
            "hundred hertz, two hundred apart. Their pitch is two hundred. <bookmark mark='b'/> Now slide all "
            "five up by thirty hertz. They are still two hundred hertz apart, and the wave still swells and "
            "fades two hundred times a second. But they are no longer multiples of two hundred, or of any "
            "frequency near it. Does the pitch change?"
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in plain], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.add(moved)
        moved.set_stroke(opacity=0)
        with self.listen(c) as snd:
            window(snd, r"200 Hz apart; \ then all moved up 30 Hz", kind="synthesized", detail=r"sums of five sines", corner=DL, tag_corner=DR)
            ts = snd.time_of("shifted")
            snd.drive(plain, lambda m, t: m.set_stroke(opacity=(0.7 + 0.3 * np.sin(22 * t)) if t < ts - 0.3 else 0.25))
            snd.drive(moved, lambda m, t: m.set_stroke(opacity=(0.7 + 0.3 * np.sin(22 * t)) if t >= ts else 0.0))
        plain.set_stroke(opacity=0.25)
        moved.set_stroke(opacity=1)
        table = VGroup(*[MathTex(rf"\tfrac{{{f:.0f}}}{{{k}}} = {f / k:.1f}", font_size=28) for k, f in zip(range(4, 9), d["shift_partials"])]).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.6)
        res = VGroup(label(rf"heard: \ about {d['shifted_pitch']:.0f} Hz, \ {d['shift_cents']:.0f} cents higher", font_size=30, color=GOOD),
                     label(rf"Monochord's model: \ {d['shifted_pitch']:.1f} Hz", font_size=28, color=TUNE),
                     label(r"the spacing, \ and the beat, \ did not change at all", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.18).move_to(DOWN * 2.3)
        with self.voiceover(
            "It does. It goes up, by a little under a quarter of a tone. So the pitch is not the spacing of the "
            "partials, and it is not the rate at which the wave beats, because neither of those moved. "
            "<bookmark mark='a'/> What the ear seems to do is ask: of what note could these be the fourth, "
            "fifth, sixth, seventh and eighth partials? Divide each by its number. The answers do not agree "
            "exactly, since no such note exists, but they cluster near two hundred and five. <bookmark mark='b'/> "
            f"Listeners in Schouten's laboratory matched it at about that. Monochord's model, which was told "
            f"nothing about this experiment, says {say(d['shifted_pitch'], 1)} hertz. Pitch is not a property of "
            "the sound. It is the ear's best guess at the period of whatever made it."
        ) as vo:
            self.play(FadeOut(q))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in table], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uses(self):
        rows = VGroup(
            VGroup(label(r"the telephone", font_size=30, color=TUNE),
                   label(r"carries 300 to 3400 Hz. \ A man's voice has its fundamental near 110 Hz. \\ You hear its pitch anyway.", font_size=24, color=GREY_A)),
            VGroup(label(r"small loudspeakers", font_size=30, color=TUNE),
                   label(r"a phone cannot produce 60 Hz, \ and you still follow the bass line: \\ from its partials.", font_size=24, color=GREY_A)),
            VGroup(label(r"the organ", font_size=30, color=TUNE),
                   label(r"two pipes a fifth apart, \ partials 2 and 3 of a note an octave lower, \\ stand in for a pipe too long to build.", font_size=24, color=GREY_A)),
            VGroup(label(r"harmony", font_size=30, color=TUNE),
                   label(r"a chord is a set of partials too. \ The note the ear supplies beneath it \\ is the chord's root. \quad $\rightarrow$ Parts 5 and 13", font_size=24, color=GREY_A)),
        )
        for k, r in enumerate(rows):
            r[0].move_to(LEFT * 6.2, aligned_edge=LEFT)
            r[1].move_to(LEFT * 2.6, aligned_edge=LEFT)
            r.shift(UP * (1.7 - 1.35 * k))
        head = label(r"The pitch that is not there, \ at work", font_size=38, color=GREY_A).to_edge(UP, buff=0.35)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "You rely on this every day. <bookmark mark='a'/> A telephone line carries nothing below three "
            "hundred hertz. A man's voice has its fundamental near a hundred and ten. You hear the pitch of his "
            "voice anyway, from the partials that do get through. <bookmark mark='b'/> The loudspeaker in a phone "
            "cannot produce sixty hertz, and you still follow the bass line. <bookmark mark='c'/> Organ builders "
            "have used it for three centuries: sound two pipes a fifth apart, the second and third partials of a "
            "note an octave below, and the listener hears the deep note of a pipe too long to fit in the "
            "building. <bookmark mark='d'/> And a chord is a set of partials too. The low note that the ear "
            "supplies beneath a chord is what musicians call its root. That idea will organise the whole of "
            "harmony, and it starts in the next part."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
