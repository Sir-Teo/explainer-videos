from __future__ import annotations

import numpy as np

from videos.music.music54.common import *  # noqa: F403


class Noise(SoundScene):
    def construct(self):
        chapter(self, 4, r"Noise and balanced lines", r"How quiet can a microphone be, \ and how does its signal survive the cable?")
        self.thermal()
        self.budget()
        self.phantom()
        self.lines()
        self.heard()
        self.levels()

    # ------------------------------------------------------------------
    def thermal(self):
        d = load("noise")
        lines = VGroup(
            MathTex(r"v_n = \sqrt{4 k T R B}", font_size=40),
            MathTex(rf"R = 200\ \Omega,\ B = 20\ \text{{kHz}},\ T = 293\ \text{{K}}: \quad v_n = {d['vn_uv']:.2f}\ \mu V", font_size=32),
            MathTex(rf"= {d['ein_dbu']:.1f}\ \text{{dBu}}", font_size=34),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.6)
        notes = VGroup(label(r"Johnson and Nyquist \ (1928): \ the electrons in any resistor jostle with the heat", font_size=18, color=WHITE),
                       label(r"200-ohm source thermal noise at this temperature and bandwidth; \ the preamp adds noise", font_size=18, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"the noise of warmth", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Every microphone signal rides on noise, and some of it is unavoidable. <bookmark mark='a'/> The electrons in any resistor jostle with the heat, as John Johnson measured and Harry Nyquist explained in 1928: the noise voltage is the square root of four k T R B. <bookmark mark='b'/> For a two-hundred-ohm microphone over the audio band, {say(d['vn_uv'], 2)} microvolts: <bookmark mark='c'/> {say(d['ein_dbu'], 1)} dBu. This is the thermal-noise contribution of that resistance at this temperature and bandwidth; a preamplifier adds its own noise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)), FadeIn(notes[0]))
            for mark, ln in zip("abc", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln), run_time=0.7)
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def budget(self):
        d = load("noise")
        rows = VGroup(
            label(rf"a dynamic microphone: \ {d['sens_mv']:.0f} mV for 1 pascal \ (94 dB SPL): \ {d['sig94_dbu']:.1f} dBu", font_size=20, color=WHITE),
            label(rf"the floor: \ {d['ein_dbu']:.1f} dBu, \ {d['sig94_dbu'] - d['ein_dbu']:.1f} dB below that", font_size=20, color=WHITE),
            label(rf"so the noise is like a sound of {d['eq_spl']:.0f} dB SPL arriving at the microphone", font_size=20, color=TUNE),
            label(rf"a very quiet room: \ about {d['quiet_room']:.0f} dB; \ a good condenser's own noise: \ about {d['condenser_self']:.0f}", font_size=19, color=GREY_A),
            label(r"in practice the room is noisier than the microphone", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(DOWN * 0.1)
        head = label(r"a noise budget", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Put it in acoustic terms. <bookmark mark='a'/> A typical dynamic microphone gives two millivolts for one pascal, "
            f"ninety-four decibels of sound: {say(d['sig94_dbu'], 1)} dBu. <bookmark mark='b'/> The thermal floor is "
            f"{say(d['sig94_dbu'] - d['ein_dbu'], 1)} decibels below that, <bookmark mark='c'/> so the floor is like a sound of "
            f"{say(d['eq_spl'])} decibels arriving at the microphone. <bookmark mark='d'/> A very quiet room is about twenty-five; "
            "a good condenser's own noise about ten. <bookmark mark='e'/> In many ordinary rooms ambient noise dominates; the balance depends on microphone sensitivity, self-noise and bandwidth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows, 0.25)))
            for mark, r in zip("abcde", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lines(self):
        hot = Line(LEFT * 4.5 + UP * 0.9, RIGHT * 4.5 + UP * 0.9, color=TUNE, stroke_width=4)
        cold = Line(LEFT * 4.5 + UP * 0.1, RIGHT * 4.5 + UP * 0.1, color=BLUE, stroke_width=4)
        gnd = Line(LEFT * 4.5 + DOWN * 0.7, RIGHT * 4.5 + DOWN * 0.7, color=GREY_B, stroke_width=2)
        lab = VGroup(label(r"hot: \ $+s/2$", font_size=17, color=TUNE).next_to(hot, LEFT, buff=0.2), label(r"cold: \ $-s/2$", font_size=17, color=BLUE).next_to(cold, LEFT, buff=0.2),
                     label(r"shield", font_size=17, color=GREY_A).next_to(gnd, LEFT, buff=0.2))
        hum = VGroup(*[Arrow(UP * 2.2 + RIGHT * x, UP * 1.0 + RIGHT * x, buff=0.0, color=EAR, stroke_width=3) for x in (-2.5, 0, 2.5)])
        hl = label(r"hum from a transformer: \ $+h$ on both", font_size=17, color=EAR).next_to(hum, UP, buff=0.1)
        eq = MathTex(r"(s/2 + h) - (-s/2 + h) = s", font_size=36).move_to(DOWN * 1.6)
        notes = label(r"the receiver takes the difference: \ the signal doubles back to $s$, \ the hum cancels", font_size=18, color=WHITE).to_edge(DOWN, buff=0.5)
        head = label(r"a balanced line", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A microphone's tiny voltage must then cross a long cable past lighting dimmers and transformers. <bookmark mark='a'/> "
            "Our symmetric balanced model uses two conductors carrying opposite halves of the signal. Balance means matched impedances to ground; equal and opposite signal voltages are not required. The conductors are twisted together inside a shield. <bookmark mark='b'/> Hum from a transformer lands almost equally on both. "
            "<bookmark mark='c'/> The receiver takes the difference: the signal comes back whole, and the hum, the same on both, "
            "cancels."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gnd), FadeIn(lab[2]))
            vo.wait_until("a")
            self.play(Create(hot), Create(cold), FadeIn(lab[:2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in hum], lag_ratio=0.2), FadeIn(hl))
            vo.wait_until("c")
            self.play(FadeIn(eq), FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("hum")
        c = clip("hum.two")
        cells = choice_boxes([r"unbalanced", r"balanced"], width=3.6, buff=1.0, colors=[EAR, TUNE]).move_to(UP * 0.4)
        cap = label(rf"the two conductors pick up the hum within 1\%: \ it falls {d['rejection_db']:.0f} dB", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"a cable past a transformer, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear it: the voice down an unbalanced cable past a transformer, then down a balanced one."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"unbalanced, \ then balanced", kind="physical model", detail=r"Part 8's voice, \ mains hum", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["unbalanced"], st["balanced"] - 0.3, buff=0.08)
            pulse(snd, cells[1], st["balanced"], c.duration, buff=0.08)
        with self.voiceover(
            f"Unbalanced, a buzz at fifty hertz and its odd harmonics sits under the voice. Balanced, with the two conductors matched to one per cent, it falls {say(d['rejection_db'])} decibels and all but vanishes. This explains the common three-pin balanced XLR connection; other microphone interfaces also exist."
        ):
            self.play(Indicate(cells[1], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def levels(self):
        items = [
            (r"microphone level: \ millivolts; \ line level: \ about a volt; \ speaker level: \ tens of volts", WHITE),
            (r"a preamplifier raises the microphone by 40 to 60 dB, \ as close to it as possible", WHITE),
            (r"gain staging: \ keep every stage well above its noise and well below its clipping \ (Part 56)", WHITE),
            (r"the last stage, \ the power amplifier, \ drives the loudspeaker", TUNE),
            (r"which is the other end of the chain", GREY_A),
        ]
        rows_scene(self, r"from millivolts to volts", items,
                   "Along the chain the levels climb. <bookmark mark='b'/> Microphone level is millivolts, line level about a volt, "
                   "speaker level tens of volts. <bookmark mark='c'/> A preamplifier raises the microphone by forty to sixty "
                   "decibels, as close to it as possible. <bookmark mark='d'/> Every stage should sit well above its noise and well "
                   "below its clipping, gain staging, which Part 56 takes up. <bookmark mark='e'/> The last stage, the power "
                   "amplifier, drives the loudspeaker, <bookmark mark='f'/> the other end of the chain.", marks="bcdef")

    # ------------------------------------------------------------------
    def phantom(self):
        items = [
            (r"a condenser needs power: \ its polarizing voltage and its impedance converter", WHITE),
            (r"phantom power sends 48 volts down both signal wires at once, \ through matched resistors", WHITE),
            (r"the receiver takes the difference, \ so the power is invisible: \ the same trick as the balanced line", WHITE),
            (r"a dynamic microphone ignores it: \ its coil sees no difference between the wires", WHITE),
            (r"one cable carries the signal, \ the power and the rejection of hum", TUNE),
        ]
        rows_scene(self, r"phantom power", items,
                   "The balanced line carries one more trick. <bookmark mark='b'/> A condenser needs power, for its polarizing voltage and its impedance converter. <bookmark mark='c'/> Phantom power sends forty-eight volts down both signal wires at once, through matched resistors. <bookmark mark='d'/> The receiver takes the difference, so the power is invisible to it: the same trick as the hum. <bookmark mark='e'/> A dynamic microphone ignores it, because its coil sees no difference between the wires. <bookmark mark='f'/> One cable carries the signal, the power and the rejection of hum.", marks="bcdef")
