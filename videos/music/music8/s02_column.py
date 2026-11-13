from __future__ import annotations

import numpy as np

from videos.music.music8.common import *  # noqa: F403


class Column(SoundScene):
    def construct(self):
        chapter(self, 1, r"A column of air", r"Why does the same pipe have two different notes?", lit=(1753,), extra=((1762, r"Bernoulli on organ pipes"),))
        self.ends()
        self.measured()
        self.worked()

    # ------------------------------------------------------------------
    def ends(self):
        rule = VGroup(label(r"at an open end the air inside meets the room: \ the pressure cannot build up there", font_size=26, color=AIR),
                      label(r"at a closed end the air has nowhere to go: \ the pressure swings most there", font_size=26, color=REED)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.4)
        left = VGroup(*[pipe_mode(n, False, color=FLUTE) for n in (1, 2, 3)]).arrange(DOWN, buff=0.45).move_to(LEFT * 3.5 + DOWN * 0.7)
        right = VGroup(*[pipe_mode(n, True, color=CLAR) for n in (1, 2, 3)]).arrange(DOWN, buff=0.45).move_to(RIGHT * 3.5 + DOWN * 0.7)
        tl = VGroup(*[label(t, font_size=24, color=FLUTE).next_to(m, LEFT, buff=0.2) for t, m in zip((r"$f$", r"$2f$", r"$3f$"), left)])
        tr = VGroup(*[label(t, font_size=24, color=CLAR).next_to(m, RIGHT, buff=0.2) for t, m in zip((r"$\tfrac12 f$", r"$\tfrac32 f$", r"$\tfrac52 f$"), right)])
        hl = label(r"open at both ends: \ half a wave fits", font_size=26, color=FLUTE).next_to(left, UP, buff=0.3)
        hr = label(r"closed at one end: \ a quarter of a wave fits", font_size=26, color=CLAR).next_to(right, UP, buff=0.3)
        end = label(r"a reed nearly shuts its end of the pipe: \ a clarinet is a pipe closed at one end", font_size=28, color=TUNE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In Part 2 we blew across a bottle and found that air in a container has notes of its own. A pipe "
            "has a whole family of them, and which family depends on its ends. <bookmark mark='a'/> At an open "
            "end, the air inside meets the air of the room, so the pressure there cannot build up: it stays "
            "at the pressure outside. At a closed end the air has nowhere to go, and the pressure swings "
            "most. <bookmark mark='b'/> Open the pipe at both ends. The pressure must be quiet at each end and "
            "can swell in the middle: half a wave fits. So do two halves, and three. The pipe's notes are a "
            "frequency f and all its multiples. <bookmark mark='c'/> Now close one end. The pressure swings "
            "most at the closed end and not at all at the open one: only a quarter of a wave fits, a wave "
            "twice as long, so a note an octave lower. The next shape that fits is three quarters, then five. "
            "Only the odd multiples. <bookmark mark='d'/> And that is the clarinet. A reed leaves only a "
            "hair's breadth of opening, so as far as the air column can tell, its end of the pipe is shut. "
            "An octave lower, and every second harmonic missing."
        ) as vo:
            first = TubeView(width=8.0, bore=0.8, left="open", right="open", color=AIR).move_to(UP * 0.3)
            blur = first.lens(standing(1, False), amp=0.3)
            cap = label(r"air in a pipe has notes of its own", font_size=30, color=GREY_A).next_to(first, DOWN, buff=0.5)
            self.play(FadeIn(first), FadeIn(blur), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeOut(first), FadeOut(blur), FadeOut(cap), FadeIn(rule[0]))
            self.play(FadeIn(rule[1]))
            vo.wait_until("b")
            self.play(FadeIn(hl), LaggedStart(*[FadeIn(m) for m in left], lag_ratio=0.5), FadeIn(tl), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(hr), LaggedStart(*[FadeIn(m) for m in right], lag_ratio=0.5), FadeIn(tr), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(end))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        d = load("column")
        g = faxes(60, 2000, [-34, 34], x_length=10.6, y_length=3.9, ylabel=r"how hard the air column pushes back (dB)", yticks=[-20, 0, 20], fticks=(100, 200, 500, 1000, 2000), font_size=20)
        g.move_to(DOWN * 0.8)
        cu = fcurve(g, d["f"], d["z_stopped_db"], CLAR)
        peaks = VGroup(*[label(rf"{f:.0f}", font_size=22, color=CLAR).next_to(g.at(f, float(np.interp(f, d['f'], d['z_stopped_db']))), UP, buff=0.08) for f in d["stopped"][:4]])
        dips = VGroup(*[VGroup(Dot(g.at(f, float(np.interp(f, d['f'], d['z_stopped_db']))), radius=0.06, color=FLUTE),
                               label(rf"{f:.0f}", font_size=22, color=FLUTE).next_to(g.at(f, float(np.interp(f, d['f'], d['z_stopped_db']))), DOWN, buff=0.1)) for f in d["open"][:4]])
        head = label(r"Monochord's pipe, \ 60 cm: \ push air in at one end, \ at every frequency", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        k1 = label(r"peaks: \ where a reed can play", font_size=24, color=CLAR).move_to(RIGHT * 3.6 + UP * 2.0)
        k2 = label(r"valleys: \ where a flute can", font_size=24, color=FLUTE).next_to(k1, DOWN, buff=0.12, aligned_edge=LEFT)
        with self.voiceover(
            "Monochord can measure this. Take the sixty-centimetre pipe, push air in and out at one end at "
            "every frequency in turn, and ask how hard the air column pushes back. Physicists call the answer "
            "the impedance. <bookmark mark='a'/> It has peaks: frequencies at which a small push of air meets "
            "a large swing of pressure. A reed, which needs pressure to work against, plays at a peak: "
            f"{say(d['stopped'][0])} hertz, then {say(d['stopped'][1])}, then {say(d['stopped'][2])}. Odd "
            "multiples, as promised. <bookmark mark='b'/> Between the peaks are valleys, where the air moves "
            "freely and the pressure hardly changes. That is the condition at an open end, so a flute, open "
            f"at its mouth hole, plays in the valleys: {say(d['open'][0])}, {say(d['open'][1])}, "
            f"{say(d['open'][2])}. Every multiple. One curve, two instruments. <bookmark mark='c'/> One "
            f"detail. The simple rule for this pipe predicts {say(d['ideal_stopped'])} hertz for the lowest "
            f"peak, and the curve says {say(d['stopped'][0])}. The air just outside an open end moves with "
            "the air inside, so a pipe behaves as if it were a little longer than it is: by about six "
            f"tenths of its radius, here {say(d['end_correction_mm'])} millimetres. Instrument makers call it "
            "the end correction, and no flute could be built in tune without it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(cu), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(peaks), FadeIn(k1))
            vo.wait_until("b")
            self.play(FadeIn(dips), FadeIn(k2))
            vo.wait_until("c")
            self.play(Indicate(peaks[0], color=WHITE, scale_factor=1.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worked(self):
        d = load("column")
        w = d["worked"]
        title = label(r"A worked example: \ how long is a flute?", font_size=36).to_edge(UP, buff=0.4)
        ask = pause_card(r"Sound travels 343 metres a second. \\ How long must a pipe open at both ends be to sound middle C, \ 262 Hz? \\ And a pipe closed at one end, \ to sound the D below it, \ 147 Hz?", width=9.6, font_size=26).move_to(UP * 0.6)
        l_open = 100 * d["c"] / (2 * w["middle_c"])
        l_closed = 100 * w["clarinet_length"]
        rows = VGroup(
            VGroup(label(r"open at both ends", font_size=28, color=FLUTE), MathTex(rf"L = \frac{{c}}{{2f}} = \frac{{343}}{{2 \times 262}} = {l_open:.1f}\ \text{{cm}}", font_size=34), label(r"a flute is 66 cm long", font_size=24, color=GREY_A)),
            VGroup(label(r"closed at one end", font_size=28, color=CLAR), MathTex(rf"L = \frac{{c}}{{4f}} = \frac{{343}}{{4 \times 147}} = {l_closed:.1f}\ \text{{cm}}", font_size=34), label(r"a clarinet: \ about 60, \ plus a mouthpiece", font_size=24, color=GREY_A)),
        )
        for k, r in enumerate(rows):
            r[0].move_to(LEFT * 6.5 + UP * (0.6 - 1.6 * k), aligned_edge=LEFT)
            r[1].move_to(LEFT * 1.5 + UP * (0.6 - 1.6 * k))
            r[2].move_to(RIGHT * 1.75 + UP * (0.6 - 1.6 * k), aligned_edge=LEFT)
        end = label(r"an oboe, \ a flute and a clarinet are nearly the same length: \ only the clarinet reaches that low D", font_size=26, color=TUNE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A worked example. Sound travels three hundred and forty-three metres a second. How long must a "
            "pipe open at both ends be, to sound middle C, at two hundred and sixty-two hertz? And how long a "
            "pipe closed at one end, for the D below it, at a hundred and forty-seven? Pause, and work them "
            "out."
        ):
            self.play(FadeIn(title), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            f"Half a wave of middle C has to fit: the speed over twice the frequency, {say(l_open, 1)} "
            "centimetres. A concert flute, whose lowest note is middle C, is sixty-six centimetres long. "
            f"<bookmark mark='a'/> For the closed pipe, a quarter of a wave: the speed over four times the "
            f"frequency, {say(l_closed, 1)} centimetres. A clarinet, whose lowest note is that D, is about "
            "sixty centimetres, and a mouthpiece. <bookmark mark='b'/> So the three small woodwinds of the "
            "orchestra are nearly the same length, and one of them goes most of an octave lower than the "
            "others. Now you know which, and why."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(end))
        self.wait(0.3)
        self.clear_scene()
