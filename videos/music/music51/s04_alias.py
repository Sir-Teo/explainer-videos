from __future__ import annotations

import numpy as np

from videos.music.music51.common import *  # noqa: F403


class Alias(SoundScene):
    def construct(self):
        chapter(self, 3, r"Why digital sawtooths alias", r"What goes wrong when a computer draws a ramp?")
        self.jump()
        self.spectrum()
        self.curve_by_pitch()
        self.blep()
        self.quiz()
        self.choices()

    # ------------------------------------------------------------------
    def jump(self):
        items = [
            (r"the obvious digital sawtooth: \ add $f/f_s$ to a phase every sample, \ wrap at 1, \ output $2\varphi - 1$", WHITE),
            (r"its drop happens between two samples, \ at a moment the samples cannot place", WHITE),
            (r"an instant drop has harmonics without end: \ those above half the sample rate fold back \ (Part 48)", WHITE),
            (r"they land between the true harmonics, \ unrelated to the note: \ inharmonic, \ and they move the wrong way", TUNE),
            (r"an analogue oscillator never had this problem: \ its circuit is band-limited by nature", GREY_A),
        ]
        rows_scene(self, r"the problem with the obvious ramp", items,
                   "Now take the synthesizer into a computer. <bookmark mark='b'/> The obvious digital sawtooth adds the frequency "
                   "over the sample rate to a phase every sample, wraps it at one, and outputs twice the phase minus one. "
                   "<bookmark mark='c'/> But its drop happens between two samples, at a moment the samples cannot place. "
                   "<bookmark mark='d'/> An instant drop has harmonics without end, and every one above half the sample rate folds "
                   "back, as Part 48 showed. <bookmark mark='e'/> They land between the true harmonics, unrelated to the note: "
                   "inharmonic, and when the note rises, some of them fall. <bookmark mark='f'/> An analogue oscillator never had "
                   "this problem; its circuit is band-limited by nature.", marks="bcdef")

    # ------------------------------------------------------------------
    def spectrum(self):
        d = load("alias")
        f0 = d["f0"]
        bins = len(d["spec"]["naive"])
        fx = (np.arange(bins) + 0.5) * 24000 / bins
        a1 = frame_axes(width=11.0, height=1.9, xlo=0, xhi=24000, ylo=-80, yhi=0, center=UP * 0.75)
        a2 = frame_axes(width=11.0, height=1.9, xlo=0, xhi=24000, ylo=-80, yhi=0, center=DOWN * 1.95)
        c1 = curve(fx, np.maximum(d["spec"]["naive"], -80), a1.to, color=EAR, width=1.5)
        c2 = curve(fx, np.maximum(d["spec"]["polyblep"], -80), a2.to, color=TUNE, width=1.5)
        marks = VGroup()
        for ax in (a1, a2):
            for h in d["harm"]:
                marks.add(Triangle(color=WHITE, fill_opacity=1, stroke_width=0).scale(0.06).rotate(PI).move_to(ax.to(h, 0) + UP * 0.12))
        t1 = label(r"naive: \ the white marks are the ten true harmonics; \ everything else is aliasing", font_size=16, color=EAR).next_to(a1, UP, buff=0.25)
        t2 = label(r"PolyBLEP: \ the same note, \ the folds pushed down", font_size=16, color=TUNE).next_to(a2, UP, buff=0.25)
        xt = VGroup(*[label(f"{k} k", font_size=14, color=GREY_A).next_to(a2.to(k * 1000, -80), DOWN, buff=0.1) for k in (0, 4, 8, 12, 16, 20, 24)])
        head = label(rf"one high note, \ {f0:.0f} Hz \ (D7), \ at 48 kHz", font_size=24, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            f"Here is one high note, D seven at {say(f0)} hertz, sampled at forty-eight kilohertz. Only ten of its harmonics fit "
            "below the twenty-four kilohertz limit; they are the white marks. <bookmark mark='a'/> The naive sawtooth's spectrum "
            "is a forest: much of the off-grid energy comes from folded harmonics, with finite-window leakage also relevant to this metric, some as loud as the real ones high up, "
            "scattered down to the bass. <bookmark mark='b'/> The same note from a band-limited oscillator, PolyBLEP, which we "
            "are about to build: the same ten harmonics, and the forest cut far back."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a1), FadeIn(a2), FadeIn(marks), FadeIn(xt))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(t1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(t2), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve_by_pitch(self):
        d = load("alias")
        cv = d["curves"]
        order = [("naive", r"naive", EAR), ("polyblep", r"PolyBLEP", TUNE), ("polyblep2", r"PolyBLEP, \ twice the rate", BLUE),
                 ("blit", r"BLIT", "#A3E635")]
        lp = line_plot([cv[k] for k, _, _ in order], width=7.0, height=3.6, ylo=-70, yhi=0, colors=[c for _, _, c in order],
                       yticks=(0, -20, -40, -60), ylabel=r"aliased energy, \ dB re the note", size=16).move_to(LEFT * 1.6 + DOWN * 0.2)
        xt = VGroup(*[label(f"{f:g}", font_size=14, color=GREY_A).next_to(lp.to(i, -70), DOWN, buff=0.12) for i, f in enumerate(d["freqs"])])
        xl = label(r"the note, \ Hz", font_size=15, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        key = VGroup(*[label(t, font_size=17, color=c) for _, t, c in order]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(lp, RIGHT, buff=0.5)
        add = label(r"additive: \ $-119$ dB \ (numerical floor)", font_size=17, color=GREY_A).next_to(key, DOWN, buff=0.4, aligned_edge=LEFT)
        head = label(r"aliasing against pitch", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        n, p, b = cv["naive"], cv["polyblep"], cv["blit"]
        with self.voiceover(
            f"Measure it across six octaves: the share of each note's energy that lies off its harmonics. <bookmark mark='a'/> The naive sawtooth: {say(-n[0], 1)} decibels down at a hundred and ten hertz, and only {say(-n[-1], 1)} at thirty-five hundred, three decibels worse for every octave, as a trend for these tested waveforms and frequencies, rather than an exact law for every note. <bookmark mark='b'/> PolyBLEP is {say(min(np.array(n) - np.array(p)))} to {say(max(np.array(n) - np.array(p)))} decibels better everywhere, {say(-p[2], 1)} at A four. <bookmark mark='c'/> Run it at twice the rate and filter, and you gain another {say(min(np.array(p) - np.array(cv['polyblep2'])))} to {say(max(np.array(p) - np.array(cv['polyblep2'])))}. <bookmark mark='d'/> BLIT, an older method, sits flat near {say(-b[2])} decibels. And adding sines below the limit, one by one, is exact to the arithmetic, at the cost of a sine for every harmonic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lp[0]), FadeIn(lp[2:]), FadeIn(xt), FadeIn(xl), FadeIn(ghost(lp.lines, 0.25)))
            for mark, i in zip("abcd", range(4)):
                vo.wait_until(mark)
                self.play(Create(lp.lines[i]), FadeIn(key[i]), run_time=1.0)
            self.play(FadeIn(add))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blep(self):
        d = load("alias")
        nv, pb = np.array(d["blep"]["naive"]), np.array(d["blep"]["polyblep"])
        k = np.arange(len(nv))
        ax = frame_axes(width=10.0, height=3.0, xlo=-0.5, xhi=len(k) - 0.5, ylo=-1.3, yhi=1.3, center=DOWN * 0.3)
        a = stems(k, nv, ax.to, color=EAR, r=0.06)
        b = stems(k, pb, ax.to, color=TUNE, r=0.06)
        jumps = VGroup(*[SurroundingRectangle(VGroup(a[j], a[j + 1]), color=GREY_A, buff=0.08, corner_radius=0.08) for j in (11, 23)])
        eq = MathTex(r"\text{near the jump: } y \mathrel{-}= \begin{cases} 2u - u^2 - 1 & \text{after}\\ u^2 + 2u + 1 & \text{before}\end{cases}"
                     r"\quad u = \frac{\varphi}{\Delta\varphi}", font_size=28).to_edge(UP, buff=1.0)
        key = VGroup(label(r"naive samples", font_size=17, color=EAR), label(r"PolyBLEP samples", font_size=17, color=TUNE)).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.4)
        head = label(r"a band-limited step, \ two samples wide", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "How does PolyBLEP do it? <bookmark mark='a'/> Here is a sawtooth at a twelfth of the sample rate, twelve samples a "
            "cycle, as the naive method draws it. <bookmark mark='b'/> The trouble is concentrated at the jumps. "
            "<bookmark mark='c'/> A band-limited step, a BLEP, is what an ideal step looks like after the anti-aliasing filter: "
            "a smooth rise with small ripples. Eli Brandt's method of 2001 stores that shape and pastes it in at every jump. "
            "Vesa Välimäki and Antti Huovilainen's polynomial version approximates it with two pieces of parabola, one sample "
            "either side, computed from where between the samples the jump really fell. <bookmark mark='d'/> Only the two "
            "samples beside each jump change; the rest of the ramp is untouched. It costs a few multiplications a jump."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ghost(a, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(Create(jumps))
            vo.wait_until("c")
            self.play(FadeIn(eq))
            vo.wait_until("d")
            self.play(FadeIn(b), FadeIn(key[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("alias")
        c = clip("alias.two")
        card = listen_card(r"The Tune's first phrase, \ two octaves above middle C, \ on a raw sawtooth with no filter, \ twice. \ "
                           r"One oscillator is naive, \ one is PolyBLEP. \ Which one aliases?", width=10.0)
        with self.voiceover(
            "Your turn. The Tune's first phrase, two octaves above middle C, on a raw sawtooth with no filter, twice. One "
            "oscillator is naive, one is PolyBLEP. Which one aliases? Listen for faint tones that do not belong to the note."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a high phrase, \ twice", kind="synthesized", detail=r"raw sawtooths", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        cv = d["curves"]
        res = VGroup(label(rf"first: \ naive, \ about {-cv['naive'][4]:.0f} dB of aliasing on the high notes", font_size=20, color=EAR),
                     label(rf"second: \ PolyBLEP, \ about {-cv['polyblep'][4]:.0f} dB", font_size=20, color=TUNE)).arrange(DOWN, buff=0.3).move_to(DOWN * 1.4)
        with self.voiceover(
            "The first was naive. Its high notes carry a faint, gritty halo, tones that slide against the melody; on the second "
            f"they are cut back by about {say(cv['naive'][4] - cv['polyblep'][4])} decibels, below where most ears catch them in a phrase like this. On a single "
            "held note, with headphones, you may still hear the second's."
        ):
            self.play(boxes[0][0].animate.set_stroke(EAR, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def choices(self):
        items = [
            (r"BLIT \ (Tim Stilson and Julius Smith, \ 1996): \ a band-limited impulse train, \ integrated into a ramp", WHITE),
            (r"BLEP \ (Eli Brandt, \ 2001): \ a stored band-limited step pasted at every jump, \ which also makes hard sync clean", WHITE),
            (r"PolyBLEP \ (V\"alim\"aki and Huovilainen, \ 2006--07): \ the step as two parabolas: \ cheap, \ and good enough", WHITE),
            (r"wavetables built per octave \ (chapter 8): \ store only harmonics that fit", WHITE),
            (r"a modern software synthesizer mixes these with a little oversampling", TUNE),
        ]
        rows_scene(self, r"the cures, \ in order", items,
                   "The cures came in order. <bookmark mark='b'/> In 1996 Tim Stilson and Julius Smith integrated a band-limited "
                   "impulse train, a BLIT, into a ramp. <bookmark mark='c'/> In 2001 Eli Brandt pasted a stored band-limited step at "
                   "every jump, which also makes hard sync clean, as chapter seven needs. <bookmark mark='d'/> In 2006 and 2007 "
                   "Välimäki and Huovilainen reduced the step to two parabolas: cheap, and good enough. <bookmark mark='e'/> "
                   "Wavetables built separately for each octave store only the harmonics that fit, as chapter eight shows. "
                   "<bookmark mark='f'/> And a modern software synthesizer mixes these with a little oversampling.", marks="bcdef")
