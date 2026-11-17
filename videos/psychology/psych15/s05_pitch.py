from __future__ import annotations

import numpy as np

from videos.psychology.psych15.common import *  # noqa: F403


class Pitch(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.timing()
        self.autocorr()
        self.verdict()

    def card(self):
        card = chapter_card(4, r"Pitch", r"Where does a missing note come from?",
                            lit={1841: r"Seebeck", 1951: r"Licklider"}, part=PART, scale=("circuit", "mind"),
                            marr=("what", "how"))
        with self.voiceover("Chapter four. Pitch."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def history(self):
        head = heading(r"Place, \ or time?")
        rows = rows_of([
            (r"1841: \ Seebeck's sirens: \ puffs of air make a pitch even when the fundamental is weak", WHITE),
            (r"Ohm and Helmholtz: \ the ear hears the frequencies in a sound, \ place by place", PLACE),
            (r"1940: \ Schouten: \ remove the fundamental and the pitch stays: \ the residue", TIMING),
            (r"so pitch cannot just be the place that vibrates most: \ nothing vibrates at 200 Hz", BAD),
        ], 12.6, 29, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "The missing fundamental is an old puzzle. In 1841, the physicist August Seebeck "
            "made tones with sirens, discs with holes that chop a jet of air, and found that the pitch followed the "
            "rate of puffs even when, by Fourier's analysis, the fundamental was weak or absent. "
            "<bookmark mark='b'/> Georg Ohm, of Ohm's law, insisted the ear must hear the frequencies actually in the "
            "sound, and Helmholtz built the theory: each place along the cochlea resonates to one frequency, and pitch "
            "is the place. <bookmark mark='c'/> In 1940 Jan Schouten, at Philips in the Netherlands, removed the "
            "fundamental electronically, and the pitch stayed. He called it the residue. <bookmark mark='d'/> So pitch "
            "can't simply be the place that vibrates most. In our missing-fundamental sound, no place vibrates at two "
            "hundred hertz at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.15))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def timing(self):
        d = load("pitch")
        head = heading(r"The repetition is still there")
        W = axes([0, 15], [-1.1, 1.1], x_length=10.0, y_length=2.4, xticks=[0, 5, 10, 15], yticks=[0],
                 xlabel=r"time (ms)", center=[0, 0.9, 0])
        ax = W.ax
        wave = curve(ax, d["w_t"], d["w_missing"] / np.abs(d["w_missing"]).max(), PLACE, stroke_width=3)
        periods = VGroup(*[DashedLine(ax.c2p(t, -1.1), ax.c2p(t, 1.1), color=TIMING, stroke_width=2) for t in (0, 5, 10, 15)])
        rows = rows_of([
            (r"the waveform of harmonics 3 to 6 of 200 Hz repeats every 5 ms: \ 1/200 of a second", TIMING),
            (r"auditory nerve fibres fire in step with the wave, \ up to about 4 to 5 kHz: \ phase locking", WHITE),
            (r"so the timing of spikes carries the period, \ even when no place is tuned to it", SOUND),
        ], 12.4, 27, 0.28).to_edge(DOWN, buff=0.75)
        tag = psyche_tag(r"computed: \ the missing-fundamental complex")
        with self.voiceover(
            "But look at the sound in time. <bookmark mark='a'/> Six hundred, eight hundred, a thousand and twelve "
            "hundred hertz are all multiples of two hundred, so together they repeat every five milliseconds: every "
            "two-hundredth of a second. The period of the missing fundamental is right there in the waveform. "
            "<bookmark mark='b'/> And the auditory nerve can follow it. Its fibres tend to fire at the same phase of "
            "the wave, cycle after cycle, for frequencies up to about four or five thousand hertz. It's called phase "
            "locking. <bookmark mark='c'/> So the timing of spikes carries the period, even when no place on the "
            "membrane is tuned to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(W), Create(wave), FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(periods), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def autocorr(self):
        d = load("pitch")
        head = heading(r"Psyche finds the pitch by autocorrelation")
        A = axes([0, 15], [-0.4, 1.05], x_length=7.4, y_length=4.2, xticks=[0, 2.5, 5, 7.5, 10, 12.5, 15],
                 yticks=[0, 0.5, 1], xlabel=r"lag (ms)", ylabel=r"summary autocorrelation", center=[-2.4, -0.3, 0])
        ax = A.ax
        c1 = curve(ax, d["lag_full"] * 1000, d["sac_full"], SOUND, stroke_width=3)
        c2 = curve(ax, d["lag_missing"] * 1000, d["sac_missing"], PLACE, stroke_width=4)
        c3 = curve(ax, d["lag_high"] * 1000, d["sac_high"], TIMING, stroke_width=3)
        peak = DashedLine(ax.c2p(5, -0.4), ax.c2p(5, 1.05), color=YOU, stroke_width=2)
        leg = legend([(SOUND, r"harmonics 1 to 6"), (PLACE, r"3 to 6: \ no fundamental"), (TIMING, r"5 to 8: \ unresolved")],
                     font_size=20).move_to([4.6, 2.3, 0])
        rows = rows_of([
            (r"each filter's output is compared with itself, \ shifted; \ the comparisons are summed across filters", MODEL),
            (r"every version peaks at a lag of 5 ms: \ a pitch of 200 Hz", YOU),
            (rf"Psyche's answers: \ {d['pitch_full']:.0f}, \ {d['pitch_missing']:.0f} and {d['pitch_high']:.0f} Hz", TIMING),
            (r"Licklider, \ 1951; \ Meddis and Hewitt, \ 1991", GREY_A),
        ], 4.6, 26, 0.34).move_to([4.6, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ \texttt{hearing.summary\_autocorrelation}")
        with self.voiceover(
            "Psyche reads that timing with a computation proposed by J. C. R. Licklider in 1951. "
            "<bookmark mark='a'/> Take each filter's output, compare it with a copy of itself shifted in time, and "
            "measure how well they match at every shift. Then add those comparisons up across all the filters. "
            "<bookmark mark='b'/> Wherever the sound repeats, the shifted copy matches, and the sum peaks. For the full "
            "complex the peak is at five milliseconds. For the version with no fundamental, also at five milliseconds. "
            "And even for harmonics five to eight, which the filters can't separate, five milliseconds. "
            "<bookmark mark='c'/> Psyche hears two hundred hertz in all three, as people do. <bookmark mark='d'/> Ray "
            "Meddis and Michael Hewitt showed in 1991 that this model, fed by a cochlea and hair cells like Psyche's, "
            "accounts for a wide range of pitch phenomena."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(leg[0]), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(c2), Create(c3), FadeIn(leg[1:]), Create(peak), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def verdict(self):
        head = heading(r"Place and time, \ together")
        rows = rows_of([
            (r"pitch from resolved harmonics is stronger and more precise than from unresolved ones", PLACE),
            (r"above about 5 kHz phase locking fails, \ and melodies become hard to hear", TIMING),
            (r"so both cues matter: \ which filters respond, \ and when the fibres fire", WHITE),
            (r"and people differ: \ some hear the missing fundamental strongly, \ others the harmonics; \ the course's experiment tests you", YOU),
        ], 12.6, 29, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "So is pitch place or time? <bookmark mark='a'/> Both, it seems. Pitch from resolved harmonics, the ones "
            "with filters of their own, is stronger and more precise than pitch from unresolved ones, so place "
            "matters. <bookmark mark='b'/> But above about five thousand hertz, where phase locking fails, melodies "
            "become hard to recognize, so timing matters too. <bookmark mark='c'/> The current view is that the brain "
            "uses both: which filters respond, and when their fibres fire. <bookmark mark='d'/> And people differ. "
            "Given two tones whose missing fundamentals move one way while their harmonics move the other, some people "
            "follow the fundamental and some the harmonics. This part's interactive experiment tests which kind of "
            "listener you are."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
