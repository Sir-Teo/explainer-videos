from __future__ import annotations

import numpy as np

from videos.music.music52.common import *  # noqa: F403


class Spectral(SoundScene):
    def construct(self):
        chapter(self, 5, r"Spectral models", r"Can a recording be turned back into knobs?")
        self.idea()
        self.tracks()
        self.stretch()
        self.heard()
        self.uses()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"Robert McAulay and Thomas Quatieri \ (1986): \ track the peaks of a sound's spectrum frame by frame as moving sines", WHITE),
            (r"Xavier Serra and Julius Smith \ (1990): \ sines for what is tonal, \ shaped noise for the rest: \ spectral modelling synthesis", WHITE),
            (r"a recording becomes a table: \ each partial's frequency and amplitude over time, \ plus a residual", WHITE),
            (r"the table is a set of knobs: \ change any number and resynthesize", TUNE),
            (r"additive synthesis \ (Part 51), \ with the curves measured instead of drawn", GREY_A),
        ]
        rows_scene(self, r"sines and the rest", items,
                   "The spectral idea runs additive synthesis backwards. <bookmark mark='b'/> In 1986 Robert McAulay and Thomas "
                   "Quatieri tracked the peaks of a sound's spectrum, frame by frame, as moving sines. <bookmark mark='c'/> In 1990 "
                   "Xavier Serra and Julius Smith split a sound into sines for what is tonal and shaped noise for the rest: spectral "
                   "modelling synthesis. <bookmark mark='d'/> A recording becomes a table: each partial's frequency and amplitude "
                   "over time, plus a residual. <bookmark mark='e'/> And the table is a set of knobs: change any number and "
                   "resynthesize. <bookmark mark='f'/> It is Part 51's additive synthesis, with the curves measured instead of "
                   "drawn.", marks="bcdef")

    # ------------------------------------------------------------------
    def tracks(self):
        d = load("spectral")
        A = np.array(d["amps"])
        t = np.array(d["t"])
        ax = frame_axes(width=9.0, height=3.6, xlo=0, xhi=t[-1], ylo=-60, yhi=0, center=DOWN * 0.3 + LEFT * 0.8)
        cols = [interpolate_color(ManimColor(TUNE), ManimColor(BLUE), k / (len(A) - 1)) for k in range(len(A))]
        cs = VGroup(*[curve(t, np.maximum(A[k], -60), ax.to, color=cols[k], width=2.2) for k in range(len(A))])
        yt = VGroup(*[label(f"{v}", font_size=14, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (0, -20, -40, -60)])
        xt = VGroup(*[label(f"{v:g} s", font_size=14, color=GREY_A).next_to(ax.to(v, -60), DOWN, buff=0.1) for v in (0, 0.5, 1.0, 1.5, 2.0) if v <= t[-1]])
        key = VGroup(label(r"partial 1", font_size=16, color=cols[0]), label(r"partial 12", font_size=16, color=cols[-1])).arrange(DOWN, buff=0.2).next_to(ax, RIGHT, buff=0.4)
        note = label(r"each partial dies at its own rate; \ the upper ones first: \ the curves Risset measured on trumpets", font_size=17, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"Part 7's piano note, \ partial by partial", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Take middle C on Part 7's computed piano and track its partials. <bookmark mark='a'/> Here are the first twelve, "
            "their levels over two seconds. <bookmark mark='b'/> Each dies at its own rate, the upper ones first. "
            "These are exactly the curves Part 51 said additive synthesis "
            "needs, measured here instead of drawn."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(xt), FadeIn(ghost(cs, 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in cs], lag_ratio=0.1), FadeIn(key), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stretch(self):
        d = load("spectral")
        cents = np.array(d["cents"])
        k = np.arange(1, len(cents) + 1)
        ax = frame_axes(width=8.0, height=3.4, xlo=0, xhi=len(k) + 1, ylo=0, yhi=max(cents) * 1.1, center=DOWN * 0.3 + LEFT * 0.8)
        st = stems(k, cents, ax.to, color=TUNE, r=0.05)
        B = d["B"]
        fit = curve(np.linspace(1, len(k), 100), 1200 * np.log2(np.sqrt((1 + B * np.linspace(1, len(k), 100) ** 2) / (1 + B))), ax.to, color=EAR, width=2)
        yt = VGroup(*[label(f"{v:.0f}", font_size=14, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (0, 50, 100, 150) if v <= max(cents) * 1.1])
        xl = label(r"partial number", font_size=15, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yl = label(r"cents above $k \times$ the first", font_size=15, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        side = VGroup(label(rf"partial {len(k)}: \ {cents[-1]:.0f} cents sharp", font_size=18, color=TUNE),
                      label(rf"fitted: \ $f_k = k f_1\sqrt{{1 + Bk^2}}$, \ $B = {B * 1e4:.1f} \times 10^{{-4}}$", font_size=17, color=EAR),
                      label(r"the stiff string of Parts 6 and 7, \ found in the recording", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4)
        head = label(r"the partials are not harmonics", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The tracks also measure the frequencies. <bookmark mark='a'/> A piano's partials are not harmonics: each runs "
            f"sharper than k times the first, until the twenty-fourth is {say(cents[-1])} cents sharp. <bookmark mark='b'/> "
            f"Fit the stiff string's law, and the inharmonicity coefficient comes out at {say(B * 1e4, 1)} times ten to the "
            "minus four: the stiffness of Part 7's string, read back out of its sound. This is why pianos are tuned "
            "stretched, as Part 6 found."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(ghost(st, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(st), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("spectral")
        c = clip("spectral.four")
        names = ["piano", "sines", "residual", "harmonic"]
        cells = choice_boxes([r"the piano", r"24 sines", rf"the residual, \ +{d['gain']:.0f} dB", r"sines made harmonic"], width=2.9, buff=0.3, size=19,
                             colors=[GREY_A, TUNE, EAR, BLUE]).move_to(UP * 0.4)
        nums = VGroup(label(rf"residual: \ {d['resid_early']:.0f} dB in the first 80 ms, \ {d['resid_late']:.0f} dB after 0.3 s", font_size=17, color=WHITE),
                      label(r"the hammer's thump is in the residual; \ the ringing is in the sines", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.7)
        head = label(r"the note taken apart, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear the note taken apart. The piano; its twenty-four tracked partials resynthesized as sines; the residual, "
            "everything not near a partial, raised twelve decibels; and the sines again with every partial moved onto an exact "
            "harmonic."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a note in pieces", kind="physical model", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        with self.voiceover(
            "The sines alone are nearly the piano, but softer at the start. The residual is the missing start: a knock, the "
            f"hammer, {say(-d['resid_early'])} decibels below the note in its first eighty milliseconds and then almost "
            "nothing. And made harmonic, the piano loses a little of its shimmer and turns plainer, nearer an electric "
            "piano: the stretched partials were part of its voice."
        ) as vo:
            self.play(FadeIn(nums))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uses(self):
        items = [
            (r"time-stretching and pitch-shifting by moving the tracks, \ not the samples", WHITE),
            (r"morphing: \ interpolate two instruments' tables, \ partial by partial", WHITE),
            (r"Melodyne's note editing \ (Part 50) \ and many codecs \ (Part 58) \ use the same split into tonal and noisy parts", WHITE),
            (r"its weak spots: \ attacks, \ which are not sines, \ and dense mixtures, \ where the peaks overlap", WHITE),
            (r"or skip the model: \ store the recording itself, \ and play it back", TUNE),
        ]
        rows_scene(self, r"what the model is for", items,
                   "A spectral model is a workshop. <bookmark mark='b'/> It can stretch time or shift pitch by moving the tracks "
                   "rather than the samples. <bookmark mark='c'/> It can morph two instruments by interpolating their tables, "
                   "partial by partial. <bookmark mark='d'/> Melodyne's note editing, from Part 50, and many audio codecs, Part "
                   "58's subject, use the same split into tonal and noisy parts. <bookmark mark='e'/> Its weak spots are attacks, "
                   "which are not sines, and dense mixtures, where the peaks overlap. <bookmark mark='f'/> Or skip the model "
                   "altogether: store the recording itself, and play it back.", marks="bcdef")
