from __future__ import annotations

import numpy as np

from videos.music.music51.common import *  # noqa: F403

LANES = [("kick", r"kick", EAR), ("snare", r"snare", TUNE), ("clap", r"clap", GOLD), ("hat", r"closed hat", BLUE), ("ohat", r"open hat", "#A3E635")]


class Drums(SoundScene):
    def construct(self):
        chapter(self, 9, r"Drum circuits", r"How does a circuit make a drum?")
        self.struck()
        self.kick()
        self.parts()
        self.kit()
        self.toms()
        self.later()

    # ------------------------------------------------------------------
    def struck(self):
        lines = VGroup(
            MathTex(r"y[n] = 2r\cos\omega\;y[n-1] - r^2\,y[n-2] + x[n]", font_size=34),
            MathTex(r"r = e^{-\pi f/(Q f_s)} \qquad \tau = \frac{2Q}{2\pi f}", font_size=34),
        ).arrange(DOWN, buff=0.45).move_to(UP * 1.0)
        notes = VGroup(label(r"two poles just inside the unit circle \ (Part 49): \ struck, \ it rings at $f$ and dies away", font_size=18, color=WHITE),
                       label(r"$Q$ sets how long: \ the time to fall to $1/e$ is $2Q$ over $2\pi f$", font_size=18, color=GREY_A),
                       label(r"a drum machine's voices are resonators like this, \ struck by a millisecond's trigger pulse", font_size=18, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"a drum is a struck resonator", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Part 40 played the 808's drums as finished sounds. Here is how a circuit makes one. <bookmark mark='a'/> Take a "
            "resonator: two poles just inside the unit circle, as Part 49 drew them. Struck once, it rings at its frequency and "
            "dies away. <bookmark mark='b'/> Its Q sets how long: the time to fall by a factor of e is two Q over two pi f. "
            "<bookmark mark='c'/> A drum machine's voices are resonators like this, struck by a trigger pulse a millisecond "
            "long; the 808's kick is a bridged-T network, a resonant filter set just short of oscillating."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kick(self):
        d = load("drums")
        y = np.array(d["kick"])
        tt = np.arange(len(y)) * 96 / 48000
        ax = frame_axes(width=7.0, height=2.6, xlo=0, xhi=tt[-1], ylo=-1.05, yhi=1.05, center=LEFT * 2.4 + DOWN * 0.3)
        wv = curve(tt, y, ax.to, color=EAR, width=2)
        env = curve(tt, np.exp(-tt / d["tau"]), ax.to, color=GREY_A, width=1.5)
        xl = label(r"the first 0.4 s", font_size=15, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        ch = d["chirp"]
        side = VGroup(label(rf"$f = {d['f']:.0f}$ Hz, \ $Q = {d['q']:.0f}$", font_size=20, color=WHITE),
                      label(rf"decay: \ predicted {d['tau_theory']:.3f} s, \ measured {d['tau']:.3f} s", font_size=18, color=TUNE),
                      label(r"while the pulse lasts, \ the resonance is pulled up 60\%", font_size=17, color=GREY_A),
                      label(rf"cycle by cycle: \ {ch[0]:.0f}, \ {ch[1]:.0f}, \ {ch[2]:.0f}, \ {ch[3]:.0f} Hz: \ a downward chirp", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4)
        head = label(r"the kick, \ from the circuit", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"The kick: a resonator at {say(d['f'])} hertz with a Q of {say(d['q'])}. <bookmark mark='a'/> The formula predicts a "
            f"decay time of {say(d['tau_theory'], 3)} seconds, and the computed kick's envelope measures {say(d['tau'], 3)}. "
            "<bookmark mark='b'/> One detail makes it a kick and not a bass note. While the trigger pulse lasts, it pulls the "
            "circuit's resonance up, here by sixty per cent, relaxing with an approximately twenty-millisecond time constant. Measured cycle by cycle the "
            f"first periods run at {say(ch[0])}, {say(ch[1])}, {say(ch[2])} and {say(ch[3])} hertz: a falling chirp that the ear "
            "hears as the beater's thump."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(side[0]), FadeIn(ghost(wv, 0.3)))
            vo.wait_until("a")
            self.play(Create(wv), Create(env), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parts(self):
        d = load("drums")
        env = np.array(d["clap_env"])
        tt = np.arange(len(env)) * 0.001
        ax = frame_axes(width=4.2, height=1.6, xlo=0, xhi=tt[-1], ylo=0, yhi=1.05)
        cl = VGroup(ax, curve(tt, env / env.max(), ax.to, color=GOLD, width=2.5))
        def lines(*ts):
            return VGroup(*[label(t, font_size=16, color=GREY_A) for t in ts]).arrange(DOWN, buff=0.12)
        cells = VGroup(
            VGroup(label(r"snare", font_size=22, color=TUNE), lines(r"two resonators, \ 180 and 330 Hz, \ low $Q$:", r"the shell", r"plus high-passed noise,", r"its own envelope:", r"the wires \ (`snappy')")).arrange(DOWN, buff=0.25),
            VGroup(label(r"clap", font_size=22, color=GOLD), cl, lines(r"three bursts of noise 10 ms apart,", r"then a tail:", r"hands not quite together")).arrange(DOWN, buff=0.2),
            VGroup(label(r"hats", font_size=22, color=BLUE), lines(r"six square waves", r"at unrelated pitches \ (Part 40),", r"band-passed high;", r"short for closed, \ long for open")).arrange(DOWN, buff=0.25),
        ).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to(DOWN * 0.1)
        head = label(r"the rest of the kit", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The rest of the kit is built the same way. <bookmark mark='a'/> The snare: two resonators, at a hundred and eighty "
            "and three hundred and thirty hertz with low Q, for the shell, plus high-passed noise with its own short envelope "
            "for the wires; the 808 calls that level snappy. <bookmark mark='b'/> The clap: three bursts of noise ten "
            "milliseconds apart, then a tail, so that it sounds like several hands not quite together. "
            "<bookmark mark='c'/> And the hats: Part 40's six square waves at unrelated pitches, band-passed high, short for "
            "closed and long for open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(cells, 0.3)))
            for mark, cc in zip("abc", cells):
                vo.wait_until(mark)
                self.play(FadeIn(cc), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kit(self):
        d = load("drums")
        c = clip("drums.kit")
        pat = d["pattern"]
        step = 60 / d["bpm"] / 4
        cell = 0.5
        grid = VGroup()
        cells = {}
        for r, (k, name, col) in enumerate(LANES):
            row = VGroup()
            for s in range(16):
                on = s in pat[k]
                sq = Square(side_length=cell * 0.86, stroke_color=GREY_D, stroke_width=1.2, fill_color=col, fill_opacity=0.85 if on else 0.0)
                sq.move_to([-4.0 + cell * s, 1.2 - r * 0.62, 0])
                row.add(sq)
            grid.add(VGroup(label(name, font_size=17, color=col).move_to([-5.6, 1.2 - r * 0.62, 0]), row))
            cells[k] = row
        grid.move_to(DOWN * 0.2)
        cap = label(r"one bar of sixteen steps, \ played four times at 100 beats a minute \ (the open hat every other bar)", font_size=16, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"a kit of circuits, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Four bars of the circuit kit at a hundred beats a minute, on a sixteen-step grid."):
            self.play(FadeIn(head), FadeIn(grid), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"the kit", kind="synthesized", detail=r"struck resonators and noise", corner=DL, tag_corner=DR)
            for k, _, lane_col in LANES:
                ht, hm = [], []
                for b in range(4):
                    for s in pat[k]:
                        if k == "ohat" and b % 2 == 0:
                            continue
                        ht.append((16 * b + s) * step)
                        hm.append(cells[k][s])
                flash(snd, hm, ht, hot=WHITE, base=lane_col)
            col = SurroundingRectangle(VGroup(*[cells[k][0] for k, _, _ in LANES]), color=WHITE, buff=0.04, stroke_width=2)

            def upd(m, t):
                s = int(t / step) % 16
                m.move_to([cells["kick"][s].get_center()[0], m.get_center()[1], 0])
            snd.show(col)
            snd.drive(col, upd)
        with self.voiceover(
            "Nothing in that groove was recorded. Every sound is a resonator struck, noise shaped by an envelope, or square "
            "waves filtered: a few dozen components each, which is why a drum machine of 1980 could carry a whole kit in one "
            "box."
        ):
            self.play(Indicate(grid, color=TUNE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def toms(self):
        d = load("toms")
        c = clip("toms.three")
        cells = choice_boxes([rf"{d['low']['fc']:.0f} Hz", rf"{d['mid']['fc']:.0f} Hz", rf"{d['high']['fc']:.0f} Hz", r"a fill"], width=2.4, buff=0.5,
                             colors=[EAR, TUNE, BLUE, GREY_A]).move_to(UP * 0.5)
        dec = VGroup(*[label(rf"decay {d[k]['tau']:.2f} s", font_size=16, color=GREY_A).next_to(cells[i], DOWN, buff=0.2) for i, k in enumerate(("low", "mid", "high"))])
        cap = VGroup(label(r"the ladder filter alone, \ $k = 3.9$, \ struck by a 2 ms pulse: \ chapter five's filter as a drum", font_size=17, color=GREY_A),
                     label(r"headphones or bass-capable speakers", font_size=16, color=TUNE)).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=1.0)
        head = label(r"the ladder, \ struck", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "And any resonant filter is a drum. Chapter five's ladder, its feedback at three point nine, just short of "
            "oscillating, struck by a two-millisecond pulse, at three cutoffs, then a fill on all three. Use headphones or bass-capable speakers for these low toms."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(dec), FadeIn(cap))
        st = d["starts"]
        names = ["low", "mid", "high", "roll"]
        with self.listen(c) as snd:
            window(snd, r"three toms and a fill", kind="synthesized", detail=r"a struck ladder", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        with self.voiceover(
            f"Three toms. The decay shortens as the cutoff rises, {say(d['low']['tau'], 2)}, {say(d['mid']['tau'], 2)} and "
            f"{say(d['high']['tau'], 2)} seconds, because at a fixed feedback the filter's Q is fixed, and the same number of "
            "cycles takes less time at a higher pitch. And the hard strike saturates the rungs, which slows them: the low tom "
            f"starts at {say(d['low']['start_hz'])} hertz and settles to {say(d['low']['end_hz'])} as it quietens. A real "
            "drumhead does the opposite, falling in pitch as it quietens, as the kick's chirp does."
        ):
            self.play(Indicate(cells[3], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def later(self):
        items = [
            (r"1980: \ the TR-808, \ all analogue, \ a commercial flop that became hip-hop's kick \ (Part 40)", WHITE),
            (r"1983: \ the TR-909 kept analogue drums, \ but stored its cymbals as 6-bit samples", WHITE),
            (r"samples won: \ by the late 1980s most drum machines played recordings", WHITE),
            (r"then the circuits came back, \ modelled in software and rebuilt in hardware", TUNE),
            (r"a resonator, \ a noise source and an envelope remain the cheapest drum there is", GREY_A),
        ]
        rows_scene(self, r"circuits and samples", items,
                   "The circuits had a short first life. <bookmark mark='b'/> In 1980 the TR-808 was all analogue, a commercial flop "
                   "that became hip-hop's kick, as Part 40 told. <bookmark mark='c'/> In 1983 the TR-909 kept analogue drums but "
                   "stored its cymbals as six-bit samples. <bookmark mark='d'/> Samples won, and by the late 1980s most drum "
                   "machines played recordings. <bookmark mark='e'/> Then the circuits came back, modelled in software and rebuilt "
                   "in hardware. <bookmark mark='f'/> A resonator, a noise source and an envelope remain the cheapest drum there is.",
                   marks="bcdef")
