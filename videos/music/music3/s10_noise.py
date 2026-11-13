from __future__ import annotations

import numpy as np

from videos.music.music3.common import *  # noqa: F403


class Noise(SoundScene):
    def construct(self):
        chapter(self, 9, r"Sounds with no pitch", r"What is the spectrum of a hiss?", lit=(1807,),
                extra=((1975, r"Voss and Clarke: \ $1/f$ noise in music"),))
        self.colours()
        self.average()
        self.where()

    # ------------------------------------------------------------------
    def colours(self):
        d = load("noise")
        c = clip("noise.colours")
        cols = {"white": WHITE, "pink": "#FF8FB1", "brown": "#B08968"}
        g = axes([0, 8], [-52, 4], x_length=5.6, y_length=4.0, xlabel=r"octave band (centre, Hz)", ylabel=r"power in the band (dB)",
                 xticks=[0, 2, 4, 6, 8], yticks=[-48, -36, -24, -12, 0], font_size=20, xfmt=lambda v: f"{31.25 * 2 ** v:.0f}")
        g.move_to(LEFT * 3.8 + DOWN * 0.3)
        lines = {k: curve(g.ax, np.arange(9), np.maximum(d[f"oct_{k}"], -52), col, stroke_width=3) for k, col in cols.items()}
        rows = VGroup()
        text = {"white": r"equal power in every hertz", "pink": r"equal power in every octave", "brown": r"a random walk"}
        for r in d["rows"]:
            sc = Scope(width=2.4, height=0.9, color=cols[r["name"]], frame=False)
            rng = np.random.default_rng(5)
            w = rng.standard_normal(600)
            if r["name"] == "pink":
                w = np.convolve(w, np.ones(6) / 6, mode="same") + 0.5 * w
            if r["name"] == "brown":
                w = np.cumsum(w)
                w -= w.mean()
            sc.set_wave(w, gain=0.9 / np.abs(w).max())
            rows.add(VGroup(sc, VGroup(label(r["name"], font_size=30, color=cols[r["name"]]), label(text[r["name"]], font_size=22, color=GREY_A),
                                       label(rf"measured slope: \ ${r['slope']:.1f}$ dB per octave", font_size=22, color=GREY_B)
                                       ).arrange(DOWN, buff=0.06, aligned_edge=LEFT)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(RIGHT * 3.4 + UP * 0.1)
        with self.voiceover(
            "Not every sound has partials. A hiss, a wave on a beach, the breath across the bottle in Part 2: these "
            "have no pitch, and their spectrum is not a row of peaks but a continuous spread. Such sounds are "
            "called noise, and they are named like colours. <bookmark mark='a'/> White noise has equal power in "
            "every hertz, which means the top octave holds half of everything, and it hisses. "
            "<bookmark mark='b'/> Pink noise has equal power in every octave: three decibels less per hertz for "
            "each octave you climb. To an ear, which counts in octaves, it sounds even. <bookmark mark='c'/> Brown "
            "noise falls twice as fast. It is a random walk, and it rumbles. Here are all three, set to the same "
            "loudness."
        ) as vo:
            self.play(FadeIn(g))
            for mark, k, row in zip("abc", ("white", "pink", "brown"), rows):
                vo.wait_until(mark)
                self.play(Create(lines[k]), FadeIn(row))
        with self.listen(c) as snd:
            window(snd, r"white, \ pink, \ brown", kind="synthesized", detail=r"equal loudness", corner=DL, tag_corner=UR)
            for k, row in zip(("white", "pink", "brown"), rows):
                t0 = snd.time_of(k)
                snd.wait_until(t0)
                rng = np.random.default_rng(hash(k) % 1000)
                base = rng.standard_normal(4000)
                if k == "pink":
                    base = np.convolve(base, np.ones(6) / 6, mode="same") + 0.5 * base
                if k == "brown":
                    base = np.cumsum(base)
                    base = base - np.convolve(base, np.ones(600) / 600, mode="same")
                base = base / np.abs(base).max()
                snd.drive(row[0], lambda m, t, base=base, t0=t0: m.set_wave(base[int((t - t0) * 1500) % 3400: int((t - t0) * 1500) % 3400 + 600], gain=0.9)
                          if t0 <= t < t0 + 2.0 else None)
                snd.wait_until(t0 + 2.0)
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def average(self):
        d = load("noise")
        g = axes([np.log10(60), np.log10(12000)], [-45, 12], x_length=10.0, y_length=3.8, xlabel=r"frequency (Hz)", ylabel=r"power (dB)",
                 xticks=[np.log10(v) for v in (100, 1000, 10000)], yticks=[-40, -20, 0], font_size=20, xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"))
        g.move_to(DOWN * 0.5)
        lf = np.log10(d["avg_f"])
        one = curve(g.ax, lf[::2], np.clip(d["one_db"][::2], -45, 12), GREY_B, stroke_width=1.2)
        mean = curve(g.ax, lf, d["mean_db"], "#FF8FB1", stroke_width=3)
        head = label(r"pink noise: \ one stretch, \ and the average of many", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        t1 = label(rf"one stretch: \ ragged, \ $\pm{d['one_scatter_db']:.0f}$ dB from bin to bin", font_size=24, color=GREY_B).move_to(g.ax.c2p(3.4, 6))
        t2 = label(rf"the average of {d['avg_frames']} stretches: \ a straight slope", font_size=24, color="#FF8FB1").next_to(t1, DOWN, buff=0.12)
        with self.voiceover(
            "There is a trap in measuring noise, and it catches people every day. Take the spectrum of one short "
            "stretch of pink noise. <bookmark mark='a'/> It is a mess: spikes and holes, five or six decibels up "
            "and down from one bin to the next. That is not an error. The spectrum of noise is itself noise. "
            "<bookmark mark='b'/> The tidy slope only appears when you average the spectra of many stretches. A "
            "tone shows itself in one look. A noise has to be described by its average, and an analyser that claims "
            "to show you the spectrum of a hiss at a glance is averaging behind your back."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(one), FadeIn(t1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(t2), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def where(self):
        items = VGroup(
            VGroup(label(r"in instruments", font_size=30, color=TUNE),
                   label(r"the breath of a flute, \ the scrape of a bow, \ a snare drum, \ every consonant you sing", font_size=26, color=GREY_A)),
            VGroup(label(r"in the studio", font_size=30, color=TUNE),
                   label(r"pink noise is the test signal for rooms and loudspeakers; \ white noise for electronics", font_size=26, color=GREY_A)),
            VGroup(label(r"in the music itself", font_size=30, color=TUNE),
                   label(r"the slow rise and fall of loudness and pitch in recorded music follows the pink law \ (Voss and Clarke, 1975)", font_size=26, color=GREY_A)),
        )
        for it in items:
            it.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        items.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(ORIGIN)
        if items.width > 13:
            items.scale_to_fit_width(13)
        with self.voiceover(
            "Noise is not the opposite of music. It is in every instrument: the breath in a flute's tone, the "
            "scrape at the start of a bowed note, the whole of a snare drum, and every consonant a singer "
            "pronounces. <bookmark mark='a'/> In a studio, pink noise is the standard signal for testing rooms and "
            "loudspeakers, because it loads every octave equally. <bookmark mark='b'/> And there is a stranger "
            "appearance. In 1975 Richard Voss and John Clarke measured how the loudness and the pitch of recorded "
            "music drift up and down over minutes, from Bach to ragtime to talk radio. The drift had a pink "
            "spectrum. Music, it seems, is neither as unpredictable as white noise nor as sluggish as brown. We "
            "will come back to that in Part 46."
        ) as vo:
            self.play(FadeIn(items[0]))
            vo.wait_until("a")
            self.play(FadeIn(items[1]))
            vo.wait_until("b")
            self.play(FadeIn(items[2]))
        self.wait(0.3)
        self.clear_scene()
