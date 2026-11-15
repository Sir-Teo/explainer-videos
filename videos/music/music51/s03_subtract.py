from __future__ import annotations

import numpy as np

from videos.music.music51.common import *  # noqa: F403

WAVES = [("saw", r"sawtooth", r"every harmonic, \ $1/k$"), ("square", r"square", r"odd harmonics, \ $1/k$"),
         ("triangle", r"triangle", r"odd harmonics, \ $1/k^2$"), ("pulse", r"pulse, \ 25\%", r"every 4th missing")]


class Subtract(SoundScene):
    def construct(self):
        chapter(self, 2, r"Subtractive synthesis", r"Why start with too much?")
        self.idea()
        self.waves()
        self.voice()
        self.sweep()
        self.modular()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"start with an oscillator whose wave has every harmonic in it", WHITE),
            (r"shape the spectrum with a filter: \ one knob, \ the cutoff, \ moves the brightness of all of them at once", WHITE),
            (r"then shape the loudness with an amplifier whose gain follows an envelope", WHITE),
            (r"oscillator, \ filter, \ amplifier: \ the same chain as the voice, \ source then filter \ (Part 8)", TUNE),
            (r"a handful of controls instead of a curve for every harmonic", GREY_A),
        ]
        rows_scene(self, r"take away", items,
                   "Subtractive synthesis runs the other way. <bookmark mark='b'/> Start with an oscillator whose wave already has "
                   "every harmonic in it. <bookmark mark='c'/> Shape the spectrum with a filter, where one knob, the cutoff, moves "
                   "the brightness of all of them at once. <bookmark mark='d'/> Then shape the loudness with an amplifier whose gain "
                   "follows an envelope. <bookmark mark='e'/> Oscillator, filter, amplifier: the same chain as the human voice, a "
                   "buzzing source and then a filter, as Part 8 built. <bookmark mark='f'/> A handful of controls, instead of a curve "
                   "for every harmonic.", marks="bcdef")

    # ------------------------------------------------------------------
    def waves(self):
        d = load("waves")
        cells = VGroup()
        for k, name, sub in WAVES:
            w = wave_path(np.array(d["shapes"][k]), width=2.6, height=1.1, color=TUNE, stroke=2.5)
            bars = harm_bars(d["levels"][k], width=0.13, gap=0.21, floor=-40.0, height=1.4, color=BLUE, labels=False)
            bars.next_to(w, DOWN, buff=0.45)
            cells.add(VGroup(label(name, font_size=22, color=WHITE), w, bars, label(sub, font_size=16, color=GREY_A)).arrange(DOWN, buff=0.3))
        cells.arrange(RIGHT, buff=0.55).move_to(DOWN * 0.2)
        cap = label(r"two cycles of each, \ and its first twelve harmonics in decibels \ (to $-40$)", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"four sources", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Analogue synthesizers offer a few sources, each a different list of harmonics. <bookmark mark='a'/> The sawtooth "
            "has every harmonic, falling as one over k: the richest, brassy and string-like. <bookmark mark='b'/> The square "
            "has only the odd ones, at the same rate: hollow, like the clarinet of Part 8. <bookmark mark='c'/> The triangle "
            "has odd harmonics too, but falling as one over k squared, twelve decibels an octave: nearly a flute. "
            "<bookmark mark='d'/> And a pulse a quarter of a cycle wide loses every fourth harmonic; its width is a knob, and "
            "chapter seven turns it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ghost(cells, 0.25)))
            for mark, cc in zip("abcd", cells):
                vo.wait_until(mark)
                self.play(FadeIn(cc), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def voice(self):
        blocks = VGroup()
        for t, sub, col in ((r"oscillator", r"VCO: \ the pitch", TUNE), (r"filter", r"VCF: \ the colour", BLUE), (r"amplifier", r"VCA: \ the loudness", EAR)):
            box = RoundedRectangle(width=2.8, height=1.3, corner_radius=0.15, stroke_color=col)
            blocks.add(VGroup(box, VGroup(label(t, font_size=24, color=col), label(sub, font_size=16, color=GREY_A)).arrange(DOWN, buff=0.12)).arrange(ORIGIN))
        blocks.arrange(RIGHT, buff=1.0).move_to(UP * 0.8)
        arrows = VGroup(*[Arrow(blocks[i].get_right(), blocks[i + 1].get_left(), buff=0.1, color=GREY_B, stroke_width=3) for i in range(2)])
        ctl = VGroup()
        for b, t in zip(blocks, (r"keyboard: \ 1 volt an octave", r"envelope, \ LFO", r"envelope")):
            a = Arrow(b.get_bottom() + DOWN * 1.2, b.get_bottom(), buff=0.05, color=GREY_A, stroke_width=2)
            ctl.add(VGroup(a, label(t, font_size=16, color=GREY_A).next_to(a, DOWN, buff=0.1)))
        vc = label(r"VC: \ voltage-controlled. \ Every knob can also be turned by another module's voltage.", font_size=19, color=WHITE).to_edge(DOWN, buff=0.5)
        head = label(r"the chain, \ and what turns its knobs", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Moog's word for the modules was voltage-controlled. <bookmark mark='a'/> A voltage-controlled oscillator, filter and "
            "amplifier: pitch, colour and loudness. <bookmark mark='b'/> Every knob could also be turned by a voltage from another "
            "module. The keyboard sends one volt for each octave, so a circuit that turns volts into frequency exponentially "
            "makes the keys equal-tempered. An envelope generator, triggered by each key, turns the filter and the amplifier. "
            "<bookmark mark='c'/> And a slow oscillator, an LFO, can turn anything at all. That one idea, that knobs are "
            "inputs, is the whole grammar of the synthesizer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(VGroup(blocks, arrows), 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(blocks), FadeIn(arrows))
            vo.wait_until("b")
            self.play(FadeIn(ctl), FadeIn(vc))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweep(self):
        d = load("sweep")
        c = clip("sweep.two")
        fc = np.array(d["fc"])
        tt = np.linspace(0, d["seconds"], len(fc))
        ax = logf_axes(width=4.6, height=2.6, flo=100, fhi=10000, ylo=0, yhi=1, center=LEFT * 3.6 + DOWN * 0.2, ticks=(100, 1000, 10000))
        # plot time on y: cutoff (x) as it moves; draw as a path of (fc, t)
        path = VMobject(stroke_color=GREY_A, stroke_width=2).set_points_as_corners([ax.to(f, 1 - t / d["seconds"]) for f, t in zip(fc, tt)])
        al = label(r"cutoff, \ Hz \ (time runs down)", font_size=15, color=GREY_A).next_to(ax, UP, buff=0.15)
        pic = sgram(d["spec"], width=6.0, height=3.2).move_to(RIGHT * 2.7 + DOWN * 0.2)
        pl = label(r"the resonant sweep's spectrogram, \ 60 Hz to 12 kHz", font_size=15, color=GREY_A).next_to(pic, UP, buff=0.15)
        boxes = VGroup(label(r"first: \ no resonance", font_size=18, color=WHITE), label(r"second: \ feedback 3.6", font_size=18, color=WHITE)).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=1.2)
        head = label(r"a filter sweep, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the gesture subtractive synthesis is known for. A sawtooth at a hundred and ten hertz, held, while the "
            "filter's cutoff opens from a hundred and fifty hertz to six kilohertz and closes again. First without resonance; "
            "then with the filter's feedback turned up, which puts a peak at the cutoff that sings each harmonic as it passes."
        ):
            self.play(FadeIn(head), FadeIn(ax), FadeIn(path), FadeIn(al), FadeIn(pic), FadeIn(pl), FadeIn(boxes))
        st = d["starts"]
        x_of_t = list(tt)
        with self.listen(c) as snd:
            window(snd, r"a sweep, \ twice", kind="synthesized", detail=r"sawtooth and ladder", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["plain"], st["resonant"] - 0.3, buff=0.1)
            pulse(snd, boxes[1], st["resonant"], c.duration, buff=0.1)
            dot = Dot(ax.to(fc[0], 1), radius=0.09, color=EAR)

            def upd(m, t):
                for t0 in (st["plain"], st["resonant"]):
                    if t0 <= t <= t0 + d["seconds"]:
                        u = t - t0
                        m.move_to(ax.to(float(np.interp(u, x_of_t, fc)), 1 - u / d["seconds"]))
                        m.set_opacity(1.0)
                        return
                m.set_opacity(0.3)
            snd.show(dot)
            snd.drive(dot, upd)
            sweep_head(snd, pic, st["resonant"], st["resonant"] + d["seconds"], color=WHITE)
        with self.voiceover(
            "Without resonance the sound simply brightens and darkens, like a mouth opening. With it, the peak picks out one "
            "harmonic after another, a whistle running up the series and back: you can see it in the spectrogram as the bright "
            "ridge along the cutoff, crossing each harmonic in turn."
        ):
            self.play(Indicate(pic, color=TUNE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def modular(self):
        items = [
            (r"modular systems \ (Moog, \ and Don Buchla's on the West Coast): \ separate modules, \ cords between them", WHITE),
            (r"Buchla preferred to shape a wave from a simple one by folding it: \ subtractive was not the only way", WHITE),
            (r"1970: \ the Minimoog fixed the chain inside a portable case: \ three oscillators, \ the ladder, \ two envelopes", WHITE),
            (r"1978: \ the Prophet-5, \ five voices, \ remembered every knob: \ patch memory", WHITE),
            (r"the knobs became a standard so durable that software still draws them", GREY_A),
        ]
        rows_scene(self, r"from cords to keyboards", items,
                   "The chain became an instrument in stages. <bookmark mark='b'/> First as modular systems, Moog's and, on the "
                   "West Coast, Don Buchla's: separate modules with cords between them. <bookmark mark='c'/> Buchla preferred to "
                   "shape a wave from a simple one by folding it back on itself; subtraction was never the only way. "
                   "<bookmark mark='d'/> In 1970 the Minimoog fixed the chain inside a portable case: three oscillators, the "
                   "ladder filter, two envelopes. <bookmark mark='e'/> In 1978 the Prophet-5, with five voices, remembered the setting "
                   "of every knob: one of the first synthesizers with patch memory. <bookmark mark='f'/> And the knobs became a standard so durable that "
                   "software still draws them.", marks="bcdef")
