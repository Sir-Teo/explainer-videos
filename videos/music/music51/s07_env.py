from __future__ import annotations

import numpy as np

from videos.music.music51.common import *  # noqa: F403

ECOL = {"pluck": EAR, "brass": TUNE, "pad": BLUE}


class Env(SoundScene):
    def construct(self):
        chapter(self, 6, r"Envelopes and modulation", r"How does a held voltage become a note?")
        self.adsr()
        self.shapes()
        self.heard()
        self.lfo()
        self.mod_heard()
        self.routing()

    # ------------------------------------------------------------------
    def adsr(self):
        ax = frame_axes(width=9.0, height=3.0, xlo=0, xhi=2.0, ylo=0, yhi=1.1, center=DOWN * 0.4)
        pts = [(0, 0), (0.15, 1.0), (0.55, 0.6), (1.3, 0.6), (1.9, 0.0)]
        segs = VGroup(*[Line(ax.to(*pts[i]), ax.to(*pts[i + 1]), color=[EAR, GOLD, TUNE, BLUE][i], stroke_width=5) for i in range(4)])
        names = [(r"attack", 0.07, 0.9), (r"decay", 0.35, 0.95), (r"sustain: \ a level, \ held", 0.92, 0.75), (r"release", 1.65, 0.45)]
        tl = VGroup(*[label(t, font_size=18, color=[EAR, GOLD, TUNE, BLUE][i]).move_to(ax.to(x, y)) for i, (t, x, y) in enumerate(names)])
        gate = VGroup(Line(ax.to(0, -0.15), ax.to(1.3, -0.15), color=WHITE, stroke_width=4), label(r"key held", font_size=16, color=GREY_A).next_to(ax.to(0.65, -0.15), DOWN, buff=0.1))
        info = label(r"Vladimir Ussachevsky's four stages, \ suggested to Moog in the 1960s: \ three times and one level", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"ADSR", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A keyboard only says when a key goes down and when it comes up. The envelope generator turns that into a shape. "
            "<bookmark mark='a'/> When the key goes down, the voltage rises, the attack, <bookmark mark='b'/> then falls, the "
            "decay, <bookmark mark='c'/> to a level that is held as long as the key is, the sustain, <bookmark mark='d'/> and "
            "when the key comes up it falls away, the release. Three times and one level: the composer Vladimir Ussachevsky "
            "asked Moog for these four in the 1960s, and nearly every synthesizer since has them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(gate), FadeIn(info), FadeIn(ghost(segs, 0.3)))
            for mark, i in zip("abcd", range(4)):
                vo.wait_until(mark)
                self.play(Create(segs[i]), FadeIn(tl[i]), run_time=0.7)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shapes(self):
        d = load("env")
        dt = d["dt"]
        cells = VGroup()
        for e, t in (("pluck", r"pluck: \ no sustain"), ("brass", r"brass: \ a quick swell, \ then held"), ("pad", r"pad: \ slow in, \ slow out")):
            ys = np.array(d["curves"][e])
            ax = frame_axes(width=3.4, height=1.6, xlo=0, xhi=len(ys) * dt, ylo=0, yhi=1.05)
            cv = curve(np.arange(len(ys)) * dt, ys, ax.to, color=ECOL[e], width=3)
            p = d["envs"][e]
            nums = label(rf"A {p['a'] * 1000:.0f} ms, \ D {p['d'] * 1000:.0f} ms, \ S {p['s']:.1f}, \ R {p['r'] * 1000:.0f} ms", font_size=14, color=GREY_A)
            cells.add(VGroup(label(t, font_size=17, color=ECOL[e]), VGroup(ax, cv), nums).arrange(DOWN, buff=0.25))
        cells.arrange(RIGHT, buff=0.6).move_to(UP * 0.2)
        gl = label(r"each drawn for a key held one second", font_size=16, color=GREY_A).next_to(cells, DOWN, buff=0.4)
        two = label(r"one envelope moves the amplifier; \ a second opens the filter three octaves at its peak", font_size=19, color=WHITE).to_edge(DOWN, buff=0.5)
        head = label(r"three envelopes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Three settings make three instruments. <bookmark mark='a'/> A pluck: a two-millisecond attack, no sustain, a "
            "decay of a third of a second. <bookmark mark='b'/> Brass: a quick swell, then a held level. <bookmark mark='c'/> A "
            "pad: more than half a second to rise and a second to fade. <bookmark mark='d'/> Each envelope moves the amplifier, "
            "and a copy opens the filter, here by three octaves at its peak, so that every note brightens as it begins, as "
            "a real instrument's does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gl), FadeIn(ghost(cells, 0.3)))
            for mark, cc in zip("abc", cells):
                vo.wait_until(mark)
                self.play(FadeIn(cc), run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(two))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("env")
        c = clip("env.three")
        cells = choice_boxes([r"pluck", r"brass", r"pad"], width=3.0, buff=0.7, colors=[EAR, TUNE, BLUE]).move_to(UP * 0.4)
        cap = label(r"one sawtooth, \ one ladder at 400 Hz with $k = 1.5$; \ only the envelopes change", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"one patch, \ three envelopes, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear one patch with only the envelopes changed: the Tune's first phrase as a pluck, as brass, and as a pad."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        names = ["pluck", "brass", "pad"]
        with self.listen(c) as snd:
            window(snd, r"three envelopes", kind="synthesized", detail=r"one patch", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        with self.voiceover(
            "The pluck is a bass or a harpsichord-like stab, every note bright for an instant and dying. The brass swells "
            "into each note and holds it. The pad blurs the notes into one another, each still rising while the next "
            "begins. Same oscillator, same filter: time alone made three instruments."
        ):
            self.play(Indicate(cells[1], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lfo(self):
        d = load("mod")
        t = np.array(d["t"])
        rows = VGroup()
        for key, name, lo, hi, col, unit in (("vib", r"pitch, \ cents", -40, 40, TUNE, r"vibrato: \ 5.5 Hz, \ $\pm 30$ cents"),
                                             ("trem", r"level", 0, 1.05, BLUE, r"tremolo: \ 6 Hz"),
                                             ("wob", r"cutoff, \ Hz", 0, 3200, EAR, r"wobble: \ 3 Hz, \ 150 Hz to 3 kHz")):
            ax = frame_axes(width=7.0, height=1.1, xlo=0, xhi=t[-1], ylo=lo, yhi=hi)
            cv = curve(t, d[key], ax.to, color=col, width=2.5)
            rows.add(VGroup(VGroup(ax, cv), label(unit, font_size=16, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.2)
        tl = label(r"one second of each", font_size=15, color=GREY_A).next_to(rows, DOWN, buff=0.25)
        head = label(r"a slow oscillator turning a knob", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The other source of movement is a low-frequency oscillator, an LFO: a wave too slow to hear as pitch, wired to a "
            "knob. <bookmark mark='a'/> Wired to the oscillator's pitch, five and a half times a second, thirty cents each way, "
            "it is vibrato, Part 43's singer's wobble. <bookmark mark='b'/> Wired to the amplifier, it is tremolo. "
            "<bookmark mark='c'/> Wired to the filter's cutoff with some resonance, three times a second across four octaves, it "
            "is the wobble of a dubstep bass."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tl), FadeIn(ghost(rows, 0.3)))
            for mark, rr in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mod_heard(self):
        d = load("mod")
        c = clip("mod.three")
        cells = choice_boxes([r"vibrato", r"tremolo", r"wobble"], width=3.0, buff=0.7, colors=[TUNE, BLUE, EAR]).move_to(UP * 0.4)
        head = label(r"three modulations, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("One held note, modulated three ways: vibrato, tremolo, and the wobble, an octave lower."):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        names = ["vibrato", "tremolo", "wobble"]
        with self.listen(c) as snd:
            window(snd, r"three modulations", kind="synthesized", detail=r"one held note", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        with self.voiceover(
            "Vibrato warms the tone without changing its colour. Tremolo pulses it, like a rotating speaker's nearer horn. "
            "The wobble talks: the resonant cutoff sweeping up and down the harmonics sounds like a mouth saying wow, wow, wow."
        ):
            self.play(Indicate(cells[2], color=EAR, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def routing(self):
        items = [
            (r"sources: \ envelopes, \ LFOs, \ the key's number, \ how hard it was struck, \ a wheel, \ another oscillator", WHITE),
            (r"destinations: \ pitch, \ cutoff, \ resonance, \ level, \ pulse width, \ the next module's rate", WHITE),
            (r"keyboard tracking: \ the cutoff follows the note, \ so high notes are not dull", WHITE),
            (r"velocity to cutoff: \ struck harder, \ brighter, \ as a piano is \ (Part 7)", WHITE),
            (r"an oscillator at audio rate turning another's pitch is frequency modulation: \ Part 52", TUNE),
        ]
        rows_scene(self, r"any source to any destination", items,
                   "In a modular system any source can turn any knob. <bookmark mark='b'/> Sources: envelopes, LFOs, the number "
                   "of the key, how hard it was struck, a wheel under the player's hand, even another oscillator. "
                   "<bookmark mark='c'/> Destinations: pitch, cutoff, resonance, level, pulse width, another module's rate. "
                   "<bookmark mark='d'/> Two routings are nearly always made. Keyboard tracking lets the cutoff follow the note, "
                   "so high notes are not dull; <bookmark mark='e'/> and velocity to cutoff makes a key struck harder sound "
                   "brighter, as a piano does. <bookmark mark='f'/> And an oscillator at audio rate turning another's pitch is "
                   "frequency modulation, which is Part 52.", marks="bcdef")
