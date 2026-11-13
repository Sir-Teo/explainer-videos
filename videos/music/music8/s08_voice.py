from __future__ import annotations

import numpy as np

from videos.music.music8.common import *  # noqa: F403


class Voice(SoundScene):
    def construct(self):
        chapter(self, 7, r"The voice: \ a source and a filter", r"What makes a voice?", lit=(1863,), extra=((1960, r"Fant's theory of speech"),), spoken="Chapter 7. The voice: a source and a filter.")
        self.folds()
        self.filter()
        self.build()

    # ------------------------------------------------------------------
    def folds(self):
        d = load("voice")
        g = axes([0, 2], [-0.1, 1.15], x_length=5.6, y_length=2.4, xlabel=r"time, \ in periods", ylabel=r"air through the folds", xticks=[0, 1, 2], yticks=[], font_size=20)
        g.move_to(LEFT * 3.4 + DOWN * 1.3)
        cu = curve_from(g, d["pulse_t"], d["pulse"], VOICE)
        n = np.arange(1, 25)
        g2 = axes([0, 25], [-62, 4], x_length=5.6, y_length=2.4, xlabel=r"harmonic", ylabel=r"strength (dB)", xticks=[1, 2, 4, 8, 16], yticks=[-48, -24, 0], font_size=20)
        g2.move_to(RIGHT * 3.4 + DOWN * 1.3)
        stems = VGroup(*[Line(g2.ax.c2p(k, -62), g2.ax.c2p(k, max(float(v), -62)), color=VOICE, stroke_width=4) for k, v in zip(n, d["source_db"][:24])])
        sl = label(rf"falling about {abs(d['source_slope']):.0f} dB for every octave", font_size=22, color=GREY_A).next_to(g2, UP, buff=0.15)
        rows = VGroup(label(r"two folds of tissue across the windpipe", font_size=26, color=VOICE),
                      label(r"breath blows them apart; \ their own springiness, \ and the suction of the air rushing between, \ bring them back", font_size=24, color=GREY_A),
                      label(rf"a puff of air each time: \ about {d['hz']:.0f} a second for a man, \ twice that for a woman", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.16).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Now the instrument everyone owns. Your voice begins at two small folds of tissue stretched "
            "across the top of the windpipe. <bookmark mark='a'/> Breath from the lungs blows them apart. "
            "Their own springiness, and the suction of the air rushing through the gap, bring them back "
            "together. Apart, together, apart: a valve, like a brass player's lips, letting the breath "
            f"through in puffs, about {say(d['hz'])} times a second in a man's speaking voice and twice that in "
            "a woman's. <bookmark mark='b'/> Here is the flow of air through the folds, as a singer's would "
            "look: it rises as they part, falls faster as they snap shut, and stops while they are closed. "
            "<bookmark mark='c'/> And its harmonics. All of them are there, falling steadily, by about "
            f"{say(abs(d['source_slope']))} decibels for every octave. By itself this is a buzz, and you will "
            "hear it in a minute. <bookmark mark='d'/> But here is the difference from every instrument so "
            "far. A clarinet's reed is a slave to its pipe: the pipe sets the pitch. The vocal folds are "
            "heavy and the tube above them is short and leaky, and it cannot tell them what to do. The folds "
            "choose the pitch, by their own tension. The tube above only colours the sound. So a voice can "
            "sing any pitch on any vowel, and that independence has a name: the source and the filter."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(g), Create(cu), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(g2), LaggedStart(*[Create(s) for s in stems], lag_ratio=0.03), FadeIn(sl), run_time=2.5)
            vo.wait_until("d")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def filter(self):
        d = load("voice")
        hz = d["hz"]
        g = axes([0, 4500], [-50, 34], x_length=10.6, y_length=3.8, xlabel=r"frequency (Hz)", ylabel=r"dB", xticks=[0, 1000, 2000, 3000, 4000], yticks=[-40, -20, 0, 20], font_size=20)
        g.move_to(DOWN * 0.8)
        env = curve_from(g, d["f"], np.asarray(d["env_a"]), VOICE, stroke_width=3)
        out = np.asarray(d["out_a"])
        stems = VGroup(*[Line(g.ax.c2p(k * hz, -50), g.ax.c2p(k * hz, max(float(v), -50)), color=TUNE, stroke_width=3) for k, v in zip(range(1, 41), out)])
        fm = d["formants"]["a"]
        tags = VGroup(*[label(rf"{f:.0f}", font_size=22, color=VOICE).next_to(g.ax.c2p(f, float(np.interp(f, d['f'], d['env_a']))), UP, buff=0.08) for f in fm])
        card = history_card(1960, r"Gunnar Fant, \ \textit{Acoustic Theory of Speech Production}", r"a voice is a source of pulses and, \ independently, \ a tube that filters them.", width=5.6, font_size=20).to_corner(UL, buff=0.35)
        k1 = VGroup(label(r"the filter: \ the tube from the folds to the lips, \\ shaped for the vowel `ah'", font_size=22, color=VOICE),
                    label(r"what comes out: \ the source's harmonics, \\ each scaled by the filter", font_size=22, color=TUNE)).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(RIGHT * 3.2 + UP * 2.5)
        with self.voiceover(
            "The filter is the tube from the folds to the lips: the throat and the mouth. Like any tube it "
            "has resonances, but they are broad, because the walls are soft and the mouth is wide open. "
            "<bookmark mark='a'/> For the vowel ah, in an average man's mouth, the first three are near "
            f"{say(fm[0])}, {say(fm[1])} and {say(fm[2])} hertz. Speech scientists call them formants. "
            "<bookmark mark='b'/> What comes out of the mouth is the buzz of the folds with each harmonic "
            "scaled by this curve: the harmonics near a formant come through strong, the ones between are "
            "held down. Notice what the formants are not. They are not harmonics, and they are not pitches "
            "you hear. They are places where the tube helps. Change the pitch, and the harmonics slide "
            "about underneath; the curve stays where it is. That fixed curve is what you recognise as ah."
        ) as vo:
            self.play(FadeIn(card), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(env), FadeIn(tags), FadeIn(k1[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(s) for s in stems], lag_ratio=0.03), FadeIn(k1[1]), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def build(self):
        d = load("voice")
        c = clip("voice.build")
        names = [r"the folds alone", r"`ah'", r"`ee'", r"`oo'"]
        bx = VGroup(*[VGroup(RoundedRectangle(width=2.7, height=1.1, corner_radius=0.14, stroke_color=GREY_C, stroke_width=2), label(n, font_size=30, color=GREY_A)) for n in names]).arrange(RIGHT, buff=0.4).move_to(UP * 1.2)
        fms = [None] + [d["formants"][v] for v in ("a", "i", "u")]
        sub = VGroup(*[label(r"no filter" if f is None else rf"{f[0]:.0f}, \ {f[1]:.0f}, \ {f[2]:.0f} Hz", font_size=22, color=VOICE).next_to(b, DOWN, buff=0.2) for f, b in zip(fms, bx)])
        note = listen_note(r"The same pulses four times: \ bare, \ and then through three shapes of the mouth. \\ The pulses never change.", width=9.0, font_size=24).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Hear it built. First the pulses of the folds alone, as they would sound if you could take the "
            "throat and mouth away. Then the same pulses through the filter for ah, then for ee, then for oo. "
            "The pulses never change. Only three numbers do."
        ):
            self.play(FadeIn(bx), FadeIn(sub), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"a source, \ then three filters", kind="synthesized", detail=r"a model of a voice", corner=UL, tag_corner=UR)
            for ev, b in zip(("source", "a", "i", "u"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 1.4)
        with self.voiceover(
            "A buzz, and then, unmistakably, a person saying ah, ee, oo. Three resonances are enough to make "
            "a vowel. That discovery, made piece by piece between Helmholtz in the eighteen sixties and "
            "Gunnar Fant in 1960, is the foundation of every telephone, every speech synthesizer and every "
            "voice assistant. It will come back when we compress sound for the ear, in Part 58."
        ):
            self.play(FadeOut(note))
        self.wait(0.3)
        self.clear_scene()
