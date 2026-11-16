from __future__ import annotations

import numpy as np

from videos.music.music68.common import *  # noqa: F403


class Down(SoundScene):
    def construct(self):
        chapter(self, 2, r"Down the chain", r"What does each link do to the Tune?")
        self.five()
        self.changes()
        self.pictures()
        self.low()
        self.coder()

    # ------------------------------------------------------------------
    def five(self):
        d = load("chain")
        c = clip("chain.five")
        note = listen_note(r"Ten seconds of the Tune at five stages: \ as written, \ performed, \ in a room, \ mastered, \ "
                           r"and through the coder at 16 kbit/s. \ Listen for what each stage adds, \ and for what never changes.", width=10.0)
        with self.voiceover(
            "Here is the Tune going down the chain: ten seconds of it at five stages. As written, played strictly. Performed. "
            "In a room. Mastered. And through the coder at sixteen kilobits a second, the end of the chain. Listen for what "
            "each stage adds, and for what never changes."
        ):
            self.play(FadeIn(note))
        self.wait(0.5)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.3, height=1.0, corner_radius=0.12, stroke_color=TUNE),
                                label(STAGE_NAMES[k], font_size=19, color=TUNE)).arrange(ORIGIN) for k in d["names"]])
        boxes.arrange(RIGHT, buff=0.25).move_to(UP * 0.5)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, color=GREY_C, stroke_width=2, tip_length=0.12) for a, b in zip(boxes, boxes[1:])])
        self.play(FadeOut(note), FadeIn(boxes), FadeIn(arrows))
        st = d["starts"]
        ks = d["names"]
        with self.listen(c) as snd:
            window(snd, r"down the chain", kind="physical model", detail=r"Part 38's piano; \ Part 58's coder", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        res = label(r"the notes and their order never changed; \ almost everything else did", font_size=21, color=WHITE).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "The intended performed notes and their order were held fixed. Almost everything else did: the timing, the loudness, the space around "
            "the sound, its colour, and at the end its cleanness."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def changes(self):
        d = load("chain")
        rows_ = [
            (r"performed", rf"onsets {d['timing_ms']:.0f} ms from a strict tempo \ (root mean square); \ dynamics over {d['gain_range_db']:.1f} dB", 43),
            (r"in a room", rf"reverberation {-d['reverb_db']:.1f} dB below the direct sound, \ dying over 1.4 s", 55),
            (r"microphone", rf"a band from 60 Hz to 15 kHz; \ noise {d['snr_db']:.0f} dB below the music's average level", 54),
            (r"mastered", rf"peak to average \ (crest factor) \ from {d['crest_before']:.1f} dB to {d['crest_after']:.1f} dB", 57),
            (r"coded", rf"noise against the mask: \ {d['codec']['128']['nmr_db']:+.0f} dB at 128 kbit/s, \ "
                       rf"{d['codec']['32']['nmr_db']:+.0f} at 32, \ {d['codec']['16']['nmr_db']:+.0f} at 16", 58),
        ]
        g = VGroup()
        for name, what, part in rows_:
            g.add(VGroup(label(name, font_size=20, color=TUNE), label(what, font_size=18, color=WHITE), label(rf"Part {part}", font_size=15, color=GREY_B)))
        g.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.2)
        for r in g:
            r[0].set_x(-6.0 + r[0].width / 2)
            r[1].set_x(-3.7 + r[1].width / 2)
            r[2].set_x(5.6 + r[2].width / 2)
        head = label(r"what each stage changed, \ measured", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        c16 = d["codec"]["16"]
        with self.voiceover(
            "What did each stage change? Measured, each by its own quantity. <bookmark mark='a'/> The performance moved the "
            f"onsets about {say(round(d['timing_ms']))} milliseconds, on average, from a strict tempo, and spread the "
            f"dynamics over {say(d['gain_range_db'], 1)} decibels. <bookmark mark='b'/> The room added reverberation "
            f"{say(-d['reverb_db'], 1)} decibels below the direct sound. <bookmark mark='c'/> The microphone narrowed the band "
            f"and added noise {say(round(d['snr_db']))} decibels below the music. <bookmark mark='d'/> The master's limiter cut "
            f"the crest factor from {say(d['crest_before'], 1)} to {say(d['crest_after'], 1)} decibels. <bookmark mark='e'/> And "
            "the coder: at a hundred and twenty-eight kilobits its estimated noise-to-mask ratio sits "
            f"{say(round(-d['codec']['128']['nmr_db']))} decibels under the mask, below this simplified masking estimate, which does not establish inaudibility; at sixteen it is "
            f"{say(round(c16['nmr_db']))} decibels over it."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", g):
                vo.wait_until(m)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pictures(self):
        p = load("pictures")
        ks = ["played", "room", "master", "codec16"]
        imgs = Group()
        for k in ks:
            a = np.array(p["stages"][k])[::-1]
            im = heat_image(a, -70, 0, width=6.0, height=2.3)
            imgs.add(Group(im, label(STAGE_NAMES[k], font_size=17, color=TUNE).next_to(im, UP, buff=0.08)))
        imgs.arrange_in_grid(rows=2, cols=2, buff=(0.4, 0.45)).move_to(DOWN * 0.35)
        head = label(r"the first eight seconds, \ as spectrograms \ (time across, \ pitch up)", font_size=22, color=GREY_A).to_edge(UP, buff=0.25)
        with self.voiceover(
            "The same eight seconds as pictures: time across, pitch up, brightness for level. <bookmark mark='a'/> Performed, "
            "each note is a stack of bright partials, and each strike of a hammer a thin vertical line. <bookmark mark='b'/> In "
            "the room, the gaps between notes fill with reverberation. <bookmark mark='c'/> Mastered, the quiet background "
            "rises further, with the noise and the limiting. <bookmark mark='d'/> And after the coder at sixteen kilobits, the "
            "quiet background is gone, the band stops at five and a half kilohertz, a few stray patches of the coder's own "
            "noise sit below the melody, and the thin lines of the hammer strikes have nearly vanished. But "
            "in every picture the lowest bright line, the melody, climbs and falls in the same places."
        ) as vo:
            self.play(FadeIn(head))
            for m, im in zip("abcd", imgs):
                vo.wait_until(m)
                self.play(FadeIn(im), run_time=0.6)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def low(self):
        c = clip("chain.low")
        card = listen_card(r"The Tune's first two phrases \ after the whole chain, \ ending in the coder at 16 kbit/s. \ "
                           r"Could you still sing it back? \ What has gone?", width=9.6)
        with self.voiceover(
            "Now the end of the chain alone: the first two phrases after every stage, ending in the coder at sixteen kilobits. "
            "Could you still sing it back? And what has gone?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        self.play(FadeOut(card))
        ring_ = Circle(radius=1.2, color=EAR, stroke_width=3).move_to(UP * 0.4)
        lab = label(r"16 kbit/s, \ the whole chain", font_size=22, color=EAR).next_to(ring_, DOWN, buff=0.3)
        self.play(FadeIn(ring_), FadeIn(lab))
        with self.listen(c) as snd:
            window(snd, r"the end of the chain", kind="physical model", detail=r"Part 38's piano; \ Part 58's coder at 16 kbit/s", corner=DL, tag_corner=DR)
            snd.drive(ring_, lambda m, t: m.set_stroke(opacity=0.5 + 0.5 * abs(np.sin(2.0 * t))))
        res = VGroup(
            label(r"you could very likely still sing it: \ every note is there", font_size=21, color=WHITE),
            label(r"what has gone is the sound's cleanness, \ and most of the room: \ the coder spent its bits on what was loud", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "You could very likely still sing it back: every note is there. <bookmark mark='a'/> What has gone is the "
            "cleanness of the sound, and most of the room. The coder's noise is now above its own estimate of what the ear "
            "masks, and with too few bits to go round it kept what was loud, the notes, and let what was quiet, the "
            "reverberation, fall to nothing."
        ) as vo:
            self.play(FadeIn(res[0]))
            vo.wait_until("a")
            self.play(FadeIn(res[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def coder(self):
        d = load("chain")["codec"]
        items = [
            (rf"128 kbit/s: \ band to {d['128']['cutoff'] / 1000:.0f} kHz, \ noise {-d['128']['nmr_db']:.0f} dB under the mask", WHITE),
            (rf"64: \ band to {d['64']['cutoff'] / 1000:.0f} kHz, \ noise {d['64']['nmr_db']:+.0f} dB against the mask", WHITE),
            (rf"32: \ band to {d['32']['cutoff'] / 1000:.0f} kHz, \ noise {d['32']['nmr_db']:+.0f} dB", WHITE),
            (rf"16: \ band to {d['16']['cutoff'] / 1000:.1f} kHz, \ noise {d['16']['nmr_db']:+.0f} dB", WHITE),
            (r"a coder spends its bits where the ear would hear their absence; \ below some rate, \ there are not enough to go round", TUNE),
        ]
        rows_scene(self, r"the coder, \ rate by rate", items,
                   "The coder, rate by rate, as Part 58 built it. <bookmark mark='b'/> At a hundred and twenty-eight kilobits the "
                   "band reaches eighteen kilohertz and the estimated quantization-noise level is below the model mask. <bookmark mark='c'/> At sixty-four the "
                   "band is cut to fourteen kilohertz and the noise reaches the mask. <bookmark mark='d'/> At thirty-two, nine "
                   "kilohertz, and the noise is over it. <bookmark mark='e'/> At sixteen, five and a half kilohertz, and still over. "
                   "<bookmark mark='f'/> A coder spends bits where the ear would hear their absence, and below some rate there "
                   "are not enough to go round.", marks="bcdef")
        self.fallback()

    # ------------------------------------------------------------------
    def fallback(self):
        w = load("wide")
        c = clip("coder.two")
        r = load("roundtrip")["rows"]
        names = [rf"{a}--{b}" for a, b in w["bands"]]
        bars = VGroup()
        for i, (cut, wide) in enumerate(zip(w["cut"], w["wide"])):
            for j, (v, col) in enumerate(((cut, TUNE), (wide, RED))):
                h = max(0.03, 2.2 * min(-v, 90) / 90)
                b = Rectangle(width=0.45, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85)
                b.move_to([-5.0 + 1.9 * i + 0.5 * j, 1.0 - h / 2, 0])
                bars.add(b)
            bars.add(label(names[i] + r" Hz", font_size=13, color=GREY_A).move_to([-4.75 + 1.9 * i, 1.25, 0]))
        key = VGroup(label(r"band cut to 5.5 kHz", font_size=16, color=TUNE), label(r"the full band it falls back to", font_size=16, color=RED)).arrange(RIGHT, buff=0.8).next_to(bars, UP, buff=0.35)
        cap = label(r"each band's loss against the master, \ in dB \ (bars hang down)", font_size=15, color=GREY_A).next_to(bars, DOWN, buff=0.2)
        res = label(rf"wrong keys: \ {r['codec16']['pitch_errors']} with the band cut, \ {w['wide_pitch_errors']} with the full band", font_size=19, color=WHITE).to_edge(DOWN, buff=1.2)
        head = label(r"at 16 kbit/s, \ a setting that matters", font_size=24, color=GREY_A).to_edge(UP, buff=0.25)
        with self.voiceover(
            "One setting deserves a closer look. Part 58's coder takes its band from a table, and the table has no entry "
            "for sixteen kilobits, so the coder falls back to its full band of eighteen kilohertz. This chain cut it to five "
            "and a half, between the table's neighbours. <bookmark mark='a'/> Here is what the fallback does. Spreading too "
            f"few bits over the whole band, it lets the loudest bands, where the melody lives, fall by {say(round(-w['wide'][1]))} "
            f"decibels, while the bands above survive. <bookmark mark='b'/> The machine then gets {say(w['wide_pitch_errors'])} "
            f"keys wrong of forty-two, against {say(r['codec16']['pitch_errors'])}. Hear both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(res))
        st = w["starts"]
        with self.listen(c) as snd:
            window(snd, r"16 kbit/s, \ two bands", kind="physical model", detail=r"Part 38's piano; \ Part 58's coder", corner=DL, tag_corner=DR)
            pulse(snd, key[0], st["cut"], st["wide"] - 0.4, buff=0.08)
            pulse(snd, key[1], st["wide"], c.duration, buff=0.08)
        with self.voiceover(
            'The second keeps only the upper part of the spectrum, so what is left is thin and high, a ghost of the Tune. A coder is not only its algorithm but its settings, and an implementation setting can fail on a particular input in a way an average can hide; this chain explicitly overrides the sixteen-kilobit cutoff.'
        ):
            self.wait(0.3)
        self.clear_scene()
