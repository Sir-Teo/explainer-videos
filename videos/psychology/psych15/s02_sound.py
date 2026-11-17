from __future__ import annotations

import numpy as np

from videos.psychology.psych15.common import *  # noqa: F403


class Sound(VoiceoverScene):
    def construct(self):
        self.card()
        self.wave()
        self.decibel()
        self.threshold()

    def card(self):
        card = chapter_card(1, r"Sound, \ and the decibel", r"What is a sound, in physics' units?",
                            lit={1860: r"Fechner", 1979: r"Terhardt"}, part=PART, scale=("molecule", "mind"),
                            marr=("what",))
        with self.voiceover("Chapter one. Sound, and the decibel."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def wave(self):
        head = heading(r"A sound is a pressure wave")
        rng = np.random.default_rng(15)
        xs = rng.uniform(-6.2, 6.2, 900)
        ys = rng.uniform(1.0, 2.9, 900)
        dots = VGroup(*[Dot([x, y, 0], radius=0.025, color=GREY_B) for x, y in zip(xs, ys)])
        k = 2 * np.pi / 2.5

        def compress(m, t):
            for d, x0 in zip(m, xs):
                d.move_to([x0 + 0.18 * np.sin(k * x0 - t), d.get_center()[1], 0])
        tracker = ValueTracker(0.0)
        dots.add_updater(lambda m: compress(m, tracker.get_value()))
        A = axes([-6.2, 6.2], [-1.2, 1.2], x_length=12.4, y_length=1.4, xticks=[], yticks=[0],
                 xlabel=r"distance", ylabel=r"pressure", center=[0, -0.2, 0])
        pw = always_redraw(lambda: curve(A.ax, np.linspace(-6.2, 6.2, 300),
                                         -np.cos(k * np.linspace(-6.2, 6.2, 300) - tracker.get_value()), SOUND,
                                         stroke_width=3))
        rows = rows_of([
            (r"air molecules crowd together and spread apart: \ a wave of pressure, \ at 343 m/s", WHITE),
            (r"frequency: \ how many crowdings a second \ (20 Hz to 20 kHz, \ less with age); \ heard as pitch", SOUND),
            (r"amplitude: \ how far the pressure swings; \ heard, \ roughly, \ as loudness", PLACE),
        ], 12.6, 26, 0.24).to_edge(DOWN, buff=0.75)
        tag = note(r"drawn: \ the motion exaggerated").to_corner(DR, buff=0.3)
        with self.voiceover(
            "A sound is a travelling wave of pressure. <bookmark mark='a'/> Air molecules crowd together and spread "
            "apart, and the pattern moves at about three hundred and forty metres a second, while each molecule only "
            "jiggles in place. <bookmark mark='b'/> How many crowdings pass each second is the frequency. Young ears "
            "hear from about twenty hertz to twenty thousand, and the top end falls with age. Frequency is heard, "
            "mostly, as pitch. <bookmark mark='c'/> How far the pressure swings is the amplitude, heard, roughly, as "
            "loudness. Both of those words, mostly and roughly, will matter."
        ) as vo:
            self.add(dots, pw)
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            self.play(tracker.animate.set_value(4 * np.pi), run_time=3.0, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), tracker.animate.set_value(8 * np.pi), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), tracker.animate.set_value(12 * np.pi), run_time=3.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), tracker.animate.set_value(16 * np.pi), run_time=3.0, rate_func=linear)
        dots.clear_updaters()
        self.clear_scene()

    def decibel(self):
        d = load("levels")
        head = heading(r"A million-fold range, \ in one ladder")
        A = axes([0, 140], [0, 7], x_length=5.4, y_length=4.6, xticks=[0, 20, 40, 60, 80, 100, 120, 140],
                 yticks=[], xlabel=r"sound pressure level (dB SPL)", center=[-3.6, -0.3, 0])
        ax = A.ax
        marks = VGroup()
        for k, (n, db) in enumerate(zip(d["names"], d["db"])):
            y = 6.4 - 0.9 * k
            dot = Dot(ax.c2p(db, y), color=SOUND if db < 120 else PAIN, radius=0.08)
            lab = label(n, font_size=21, color=GREY_A).next_to(dot, RIGHT, buff=0.15)
            marks.add(VGroup(dot, lab))
        eq = MathTex(r"L = 20\log_{10}\frac{p}{p_0}, \qquad p_0 = 20\ \mu\text{Pa}", font_size=36).move_to([4.2, 1.8, 0])
        rows = rows_of([
            (r"20 dB is ten times the pressure; \ 120 dB is a million times", WHITE),
            (rf"from the threshold to pain: \ a pressure ratio of about {d['ratio'] / 1e6:.1f} million", SOUND),
            (r"a logarithm, \ as Fechner said a sensation should be: \ Part 11's law, \ turned into a unit", PRIOR),
            (r"loudness itself grows more slowly: \ about double for each 10 dB \ (Stevens, \ Part 11)", GREY_A),
        ], 4.8, 26, 0.3).move_to([4.3, -1.1, 0])
        keep_in_frame(rows)
        tag = note(r"typical levels, \ as usually tabulated; \ approximate").to_corner(DR, buff=0.3)
        with self.voiceover(
            "The ear's range is enormous. <bookmark mark='a'/> The faintest sound a young listener can hear at a "
            "thousand hertz is a pressure swing of about twenty millionths of a pascal: a fraction of a billionth of "
            "the air's own pressure. The threshold of pain is over three million times larger. "
            "<bookmark mark='b'/> To fit that in one scale, acousticians use the decibel: twenty times the logarithm of "
            "the pressure, relative to that faintest sound. Every twenty decibels is ten times the pressure. "
            "<bookmark mark='c'/> It's a logarithm, which is what Fechner said, in Part 11, the size of a sensation "
            "should be. The decibel is Fechner's law turned into an engineering unit. <bookmark mark='d'/> Though "
            "Stevens, also in Part 11, would add that loudness grows more slowly than the logarithm suggests: it "
            "roughly doubles for every ten decibels."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.4), FadeIn(rows[0]), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def threshold(self):
        d = load("levels")
        head = heading(r"The threshold of hearing depends on frequency")
        lf = np.log10(d["f"])
        A = axes([np.log10(20), np.log10(16000)], [-10, 80], x_length=7.2, y_length=4.4,
                 xticks=[np.log10(v) for v in (20, 100, 1000, 10000)], xfmt=lambda v: f"{10 ** v:.0f}",
                 yticks=[0, 20, 40, 60, 80], xlabel=r"frequency (Hz)", ylabel=r"threshold (dB SPL)",
                 center=[-2.5, -0.3, 0])
        ax = A.ax
        tq = curve_in(ax, lf, np.clip(d["tq"], -10, 80), SOUND, stroke_width=4)
        best = Dot(ax.c2p(np.log10(d["tq_min_f"]), d["tq_min"]), color=YOU, radius=0.08)
        rows = rows_of([
            (rf"most sensitive near {d['tq_min_f'] / 1000:.1f} kHz, \ where the ear canal resonates", YOU),
            (rf"at 50 Hz, \ about {d['tq_50']:.0f} dB more is needed than at 1 kHz", SOUND),
            (r"an audiogram plots a person's thresholds against this standard", WHITE),
            (r"noise damage often shows first as a notch near 4 kHz; \ age takes the high frequencies", BAD),
        ], 4.8, 26, 0.32).move_to([4.4, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ Terhardt's (1979) formula for the threshold in quiet")
        with self.voiceover(
            "And the ear isn't equally sensitive at every frequency. <bookmark mark='a'/> This curve is an engineer's "
            "formula for the quietest audible sound at each frequency, the one used inside audio compressors. The "
            "ear is most sensitive between about two and five thousand hertz, partly because the ear canal "
            "resonates there, and the region holds much of what makes speech intelligible. <bookmark mark='b'/> At "
            "fifty hertz you need about forty decibels more, a hundred times the pressure. <bookmark mark='c'/> A "
            "hearing test, an audiogram, plots a person's thresholds against a standard like this one. "
            "<bookmark mark='d'/> Damage from noise often shows first as a dip near four thousand hertz; age takes the "
            "highest frequencies first. We'll come back to a kind of damage the audiogram can't see."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(tq), FadeIn(best), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
