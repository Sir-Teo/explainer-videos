from __future__ import annotations

import numpy as np

from videos.music.music4.common import *  # noqa: F403


class Mask(SoundScene):
    def construct(self):
        chapter(self, 5, r"What a loud sound hides", r"When does one sound make another inaudible?", lit=(1863,),
                extra=((1940, r"Fletcher's critical band"),))
        self.pattern()
        self.test()
        self.uses()

    def graph(self, x_length=8.4, y_length=4.0, at=LEFT * 1.9 + DOWN * 0.5):
        d = load("mask")
        g = faxes(250, 8000, [-10, 80], x_length=x_length, y_length=y_length, ylabel=r"level (dB)", yticks=[0, 20, 40, 60, 80],
                  fticks=(250, 500, 1000, 2000, 4000, 8000), font_size=20)
        g.move_to(at)
        quiet = fcurve(g, d["f"], d["quiet"], GREY_B, stroke_width=2)
        masked = fcurve(g, d["f"], d["masked"], BAD)
        masker = Line(g.at(d["masker_hz"], -10), g.at(d["masker_hz"], d["masker_db"]), color=TUNE, stroke_width=6)
        near = Dot(g.at(d["near_hz"], d["probe_db"]), radius=0.1, color=AIR)
        far = Dot(g.at(d["far_hz"], d["probe_db"]), radius=0.1, color=AIR)
        return d, g, quiet, masked, masker, near, far

    # ------------------------------------------------------------------
    def pattern(self):
        d, g, quiet, masked, masker, near, far = self.graph()
        ql = label(r"heard in quiet above this line", font_size=20, color=GREY_B).move_to(g.at(5200, 14))
        ml = label(r"a loud tone: \ 1000 Hz, \ 70 dB", font_size=22, color=TUNE).next_to(masker, UP, buff=0.1)
        hl = label(r"beside it, \ nothing below \\ this line is heard", font_size=22, color=BAD).move_to(g.at(2300, 58))
        ask = pause_card(rf"A second tone at {d['near_hz']:.0f} Hz, \ at {d['probe_db']:.0f} dB: \\ is it heard? \ And one at {d['far_hz']:.0f} Hz?", width=4.3, font_size=24)
        ask.to_corner(UR, buff=0.4).shift(DOWN * 0.9)
        ans = VGroup(label(rf"{d['near_hz']:.0f} Hz: \ needs {d['near_threshold']:.0f} dB.", font_size=24, color=BAD),
                     label(rf"Hidden, \ by {d['near_threshold'] - d['probe_db']:.0f} dB.", font_size=24, color=BAD),
                     label(rf"{d['far_hz']:.0f} Hz: \ needs only {d['far_threshold']:.0f} dB.", font_size=24, color=GOOD),
                     label(r"Heard easily.", font_size=24, color=GOOD)).arrange(DOWN, buff=0.14, aligned_edge=LEFT).next_to(ask, DOWN, buff=0.4)
        with self.voiceover(
            "Fletcher's filter has a consequence that an entire industry is built on. A tone is heard through the "
            "band of the ear centred on it. So anything else that falls in that band competes with it. "
            "<bookmark mark='a'/> Start with silence: the grey line is the threshold in quiet. Now add one loud "
            "tone, a thousand hertz at seventy decibels. <bookmark mark='b'/> Its wave on the membrane spills into "
            "the neighbouring bands, and raises the threshold in every one of them. The red line is Monochord's "
            "estimate of the new threshold: the loud tone's power in each band, less a few decibels. "
            f"<bookmark mark='c'/> So here is a question. A second tone at eleven hundred and fifty hertz, at {say(d['probe_db'])} "
            "decibels, which is easy to hear on its own. Is it heard? And what about the same tone moved up "
            "to three thousand hertz? Pause, and read the answers off the graph."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(quiet), FadeIn(ql))
            self.wait(max(vo.until("b") - 2.0, 0.1))
            self.play(GrowFromEdge(masker, DOWN), FadeIn(ml))
            vo.wait_until("b")
            self.play(Create(masked), FadeIn(hl), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(near), FadeIn(far), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            f"At eleven fifty the red line stands at {say(d['near_threshold'])} decibels. Our tone is at {say(d['probe_db'])}. It "
            f"is hidden, with {say(d['near_threshold'] - d['probe_db'])} decibels to spare. At three thousand the "
            f"line has fallen to {say(d['far_threshold'])}, and the tone is heard easily. The loud tone has not "
            "made you deaf. It has made you deaf near itself."
        ):
            self.play(LaggedStart(*[FadeIn(a) for a in ans], lag_ratio=0.6), near.animate.set_color(BAD), far.animate.set_color(GOOD), run_time=4.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def test(self):
        d, g, quiet, masked, masker, near, far = self.graph(x_length=7.0, y_length=3.0, at=RIGHT * 0.4 + DOWN * 1.1)
        c = clip("mask.demo")
        q = listen_card(r"A quiet tone that pulses on and off, \ three times over. \\ 1: \ alone. \quad 2: \ beside a loud tone. \quad "
                        r"3: \ far above the loud tone. \\ In which do you hear the pulsing?", width=10.4, font_size=26).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Do not take the graph's word for it. You will hear a quiet tone that pulses on and off. First alone. "
            "Then again, exactly as strong, with the loud tone sounding beside it. Then moved far above the loud "
            "tone. In which of the three can you hear the pulsing?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(g), FadeIn(quiet))
        masked.set_stroke(opacity=0)
        masker.set_stroke(opacity=0)
        near.set_opacity(0)
        far.set_opacity(0)
        self.add(masked, masker, near, far)
        with self.listen(c) as snd:
            window(snd, r"a pulsing tone: \ alone, \ beside a loud tone, \ far above it", kind="synthesized", corner=DL, tag_corner=DR)
            ta, tn, tf = (snd.time_of(e) for e in ("alone", "near", "far"))
            beat = lambda t: 1.0 if np.sin(2 * np.pi * 2.5 * t) > 0 else 0.15      # noqa: E731
            snd.drive(near, lambda m, t: m.set_opacity(beat(t - ta) if ta <= t < ta + 1.6 else (beat(t - tn) if tn <= t < tn + 1.6 else 0.0)))
            snd.drive(far, lambda m, t: m.set_opacity(beat(t - tf) if tf <= t < tf + 1.6 else 0.0))
            snd.drive(masker, lambda m, t: m.set_stroke(opacity=(0.8 + 0.2 * np.sin(30 * t)) if t >= tn and not (tn + 1.6 <= t < tf) else 0.0))
            snd.drive(masked, lambda m, t: m.set_stroke(opacity=0.9 if t >= tn and not (tn + 1.6 <= t < tf) else 0.0))
        for m in (near, far):
            m.set_opacity(1)
        masker.set_stroke(opacity=1)
        masked.set_stroke(opacity=1)
        co = Cochlea(width=4.3, scale=0.9, ticks=(), names=False).move_to(LEFT * 4.5 + DOWN * 0.6)
        co.remove(co.axis, co.unit)
        env = co.lens(load("wave")["env_1000"], color=TUNE, opacity=0.35)
        tail = Arrow(co.p(2) + UP * 1.0, co.p(11) + UP * 0.3, color=BAD, stroke_width=3, buff=0.05, max_tip_length_to_length_ratio=0.12)
        cl = VGroup(label(r"the loud tone's wave passes through", font_size=22, color=BAD),
                    label(r"every high-frequency place on its way", font_size=22, color=BAD)).arrange(DOWN, buff=0.05).next_to(co, UP, buff=0.9)
        ends = VGroup(label(r"base: \ high", font_size=18, color=GREY_B).next_to(co.p(0), DOWN, buff=0.4),
                      label(r"apex: \ low", font_size=18, color=GREY_B).next_to(co.p(35), DOWN, buff=0.4))
        with self.voiceover(
            "Alone, it is perfectly clear. Beside the loud tone it vanishes, although in the recording it is "
            "exactly as strong as before. Far above the loud tone, it is back. <bookmark mark='a'/> One correction "
            "to our model, from real ears. Its red curve is nearly the same on both sides. Measured masking is "
            "lopsided: a loud tone hides more above itself than below, and more so the louder it gets. "
            "<bookmark mark='b'/> The travelling wave says why. On its way to its own place, the wave of a low "
            "tone has to pass through every high-frequency place on the membrane, and it shakes them as it goes. "
            "A high tone's wave never reaches the low-frequency places at all. So low sounds mask high sounds "
            "much more than the other way round."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(q), g.animate.shift(RIGHT * 2.4 + UP * 1.0), VGroup(quiet, masked, masker, near, far).animate.shift(RIGHT * 2.4 + UP * 1.0))
            vo.wait_until("b")
            self.play(FadeIn(co), FadeIn(env), FadeIn(ends), FadeIn(cl), GrowArrow(tail))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uses(self):
        rows = VGroup(
            VGroup(label(r"audio coding", font_size=30, color=TUNE),
                   label(r"an MP3 or AAC encoder computes this curve many times a second, \\ and spends no bits on anything beneath it", font_size=26, color=GREY_A),
                   label(r"$\rightarrow$ Part 58", font_size=24, color=GREY_B)),
            VGroup(label(r"mixing", font_size=30, color=TUNE),
                   label(r"a bass guitar hides a kick drum; \ engineers cut a notch in one \\ to make room for the other", font_size=26, color=GREY_A),
                   label(r"$\rightarrow$ Part 56", font_size=24, color=GREY_B)),
            VGroup(label(r"orchestration", font_size=30, color=TUNE),
                   label(r"a flute in its low register disappears under the horns; \\ an octave higher it sails over them", font_size=26, color=GREY_A),
                   label(r"$\rightarrow$ Part 41", font_size=24, color=GREY_B)),
            VGroup(label(r"hearing loss", font_size=30, color=TUNE),
                   label(r"damaged ears have wider filters, \ so everything masks everything: \\ ``I can hear you, \ but not in a restaurant''", font_size=26, color=GREY_A),
                   label(r"$\rightarrow$ chapter 10", font_size=24, color=GREY_B)),
        )
        for r in rows:
            r[1].scale(0.88)
            r[0].move_to(LEFT * 6.3, aligned_edge=LEFT)
            r[1].move_to(LEFT * 3.8, aligned_edge=LEFT)
            r[2].move_to(RIGHT * 4.6, aligned_edge=LEFT)
        for k, r in enumerate(rows):
            r.shift(UP * (1.7 - 1.35 * k))
        head = label(r"Masking, \ at work", font_size=38, color=GREY_A).to_edge(UP, buff=0.35)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "Masking is why this chapter matters to people who will never study an ear. <bookmark mark='a'/> A "
            "music file on your phone is about a tenth the size of the recording it was made from. The encoder "
            "works out this masking curve many times a second, and spends no bits at all on anything that falls "
            "beneath it. Nine tenths of the data are thrown away, and you do not notice, because you could not "
            "have heard them. <bookmark mark='b'/> A mixing engineer fights masking all day: the bass guitar hides "
            "the kick drum, so a notch is cut in one to make room for the other. <bookmark mark='c'/> An "
            "orchestrator knows that a flute in its low register vanishes beneath the horns, and an octave "
            "higher sails over them. <bookmark mark='d'/> And when an ear is damaged, its filters grow wider, so "
            "that everything masks everything. That is why the first complaint of hearing loss is not that "
            "sounds are too quiet. It is that a voice can no longer be picked out of a noisy room."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
