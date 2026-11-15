from __future__ import annotations

import numpy as np

from videos.music.music54.common import *  # noqa: F403


class Boxes(SoundScene):
    def construct(self):
        chapter(self, 6, r"Sealed and vented boxes", r"Why put a loudspeaker in a box at all?")
        self.short()
        self.sealed()
        self.checks()
        self.vented()
        self.port()
        self.impedance()

    # ------------------------------------------------------------------
    def short(self):
        items = [
            (r"a bare cone pushes air forward and pulls it from behind at the same moment", WHITE),
            (r"at low frequencies the air simply flows round the edge: \ the two sides cancel, \ an acoustic short circuit", WHITE),
            (r"a sealed box traps the back wave; \ its air becomes a second spring", WHITE),
            (r"a vented box lets the back wave out through a port, \ in step, \ at the box's own resonance", WHITE),
            (r"Part 2's Helmholtz resonator, \ inside a loudspeaker", TUNE),
        ]
        rows_scene(self, r"the back of the cone", items,
                   "A loudspeaker needs a box because of its back. <bookmark mark='b'/> A bare cone pushes air forward and pulls it "
                   "from behind at the same moment. <bookmark mark='c'/> At low frequencies the air simply flows round the edge, and "
                   "the two sides cancel: an acoustic short circuit. <bookmark mark='d'/> A sealed box traps the back wave, and its "
                   "air becomes a second spring. <bookmark mark='e'/> A vented box lets the back wave out through a port, in step, "
                   "at the box's own resonance: <bookmark mark='f'/> Part 2's Helmholtz resonator, inside a loudspeaker.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def sealed(self):
        d = load("driver")
        f = np.array(d["f"])
        ax = logf_axes(width=8.0, height=3.2, flo=10, fhi=2000, ylo=-30, yhi=3, center=LEFT * 0.8 + DOWN * 0.2, ticks=(10, 100, 1000))
        cols = {"sealed20": EAR, "sealed50": TUNE, "sealed200": BLUE}
        cs = VGroup(*[curve(f, np.maximum(d["curves"][k], -30), ax.to, color=c, width=3) for k, c in cols.items()])
        key = VGroup(*[label(rf"{int(k[6:])} litres", font_size=17, color=c) for k, c in cols.items()]).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.4)
        eq = MathTex(r"f_c = f_s\sqrt{1 + V_{as}/V_b}, \quad Q_{tc} = Q_{ts}\sqrt{1 + V_{as}/V_b}", font_size=30).to_edge(UP, buff=1.0)
        yl = label(r"dB", font_size=15, color=GREY_A).next_to(ax, LEFT, buff=0.15)
        head = label(r"one woofer, \ three sealed boxes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Put our woofer in sealed boxes of three sizes. <bookmark mark='a'/> The box's air adds stiffness to the suspension, "
            "so the resonance rises and sharpens: by the square root of one plus V a s over the box's volume, as Richard Small "
            "showed in 1972. <bookmark mark='b'/> Twenty litres: the response bulges before it falls. Fifty: smoother. Two "
            "hundred: the gentlest roll-off, but a box the size of a cupboard. Each falls twelve decibels an octave below its "
            "resonance: a second-order high-pass."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yl), FadeIn(ghost(cs, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in cs], lag_ratio=0.3), FadeIn(key), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def checks(self):
        d = load("driver")
        rows = VGroup(VGroup(label(r"box", font_size=17, color=GREY_A), label(r"$Q_{tc}$", font_size=17, color=GREY_A), label(r"$-3$ dB, \ closed form", font_size=17, color=GREY_A),
                             label(r"$-3$ dB, \ simulated", font_size=17, color=GREY_A)))
        for c in d["checks"]:
            rows.add(VGroup(label(rf"sealed, \ {c['Vb_l']:.0f} L", font_size=19, color=WHITE), label(rf"{c['Qtc']:.2f}", font_size=19, color=WHITE),
                            label(rf"{c['formula_f3']:.1f} Hz", font_size=19, color=TUNE), label(rf"{c['sim_f3']:.1f} Hz", font_size=19, color=BLUE)))
        b = d["b4"]
        rows.add(VGroup(label(rf"vented B4, \ {b['Vb_l']:.0f} L", font_size=19, color=WHITE), label(r"0.383", font_size=19, color=WHITE),
                        label(rf"{b['formula_f3']:.1f} Hz", font_size=19, color=TUNE), label(rf"{b['sim_f3']:.1f} Hz", font_size=19, color=BLUE)))
        rows.arrange(DOWN, buff=0.3)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-4.4 + 3.0 * i)
        rows.move_to(DOWN * 0.1)
        note = label(r"the simulator knows nothing of these formulas: \ it solves the circuit at each frequency", font_size=18, color=WHITE).to_edge(DOWN, buff=0.5)
        head = label(r"the simulation checked", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Check the simulator against the closed forms. <bookmark mark='a'/> For each sealed box, Small's formulas give the "
            "minus-three-decibel point; the simulation, which knows nothing of the formulas and only solves the circuit "
            "frequency by frequency, lands within a tenth of a hertz. <bookmark mark='b'/> And for the vented box designed by "
            "Thiele's fourth-order Butterworth recipe, the closed form says the response is down three decibels exactly at the "
            f"driver's resonance, forty hertz; the simulation says {say(b['sim_f3'], 2)}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:4]], lag_ratio=0.2), FadeIn(note), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vented(self):
        d = load("driver")
        f = np.array(d["f"])
        b = d["b4"]
        ax = logf_axes(width=8.0, height=3.2, flo=10, fhi=2000, ylo=-30, yhi=3, center=LEFT * 0.8 + DOWN * 0.2, ticks=(10, 100, 1000))
        v = curve(f, np.maximum(d["curves"]["b4"], -30), ax.to, color=TUNE, width=3)
        s = curve(f, np.maximum(d["curves"]["b4_sealed_same_box"], -30), ax.to, color=GREY_A, width=2)
        key = VGroup(label(rf"vented, \ tuned to {b['fb']:.0f} Hz", font_size=17, color=TUNE), label(r"the same box, \ sealed", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.4)
        note = label(rf"the port gains nearly an octave \ ({b['sealed_f3']:.0f} Hz to {b['sim_f3']:.0f}), \ then falls 24 dB an octave instead of 12", font_size=18, color=WHITE).to_edge(DOWN, buff=0.45)
        yl = label(r"dB", font_size=15, color=GREY_A).next_to(ax, LEFT, buff=0.15)
        head = label(r"the vented box: \ Thiele's B4", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Now open a port. <bookmark mark='a'/> In a box of {say(b['Vb_l'])} litres the woofer, sealed, reaches down to "
            f"{say(b['sealed_f3'])} hertz. <bookmark mark='b'/> Tune a port so that the box resonates at forty hertz, and below "
            "the driver's own resonance the port takes over: its slug of air, pushed by the box's pressure, radiates in step "
            f"with the cone. The response now reaches {say(b['sim_f3'])} hertz, maximally flat, nearly an octave deeper. The "
            "price: below the tuning it falls twenty-four decibels an octave, and the cone, no longer held by the box's air, "
            "flaps freely."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yl), FadeIn(ghost(VGroup(v, s), 0.25)))
            vo.wait_until("a")
            self.play(Create(s), FadeIn(key[1]))
            vo.wait_until("b")
            self.play(Create(v), FadeIn(key[0]), FadeIn(note), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def impedance(self):
        d = load("driver")
        f = np.array(d["f"])
        ax = logf_axes(width=8.0, height=3.0, flo=10, fhi=2000, ylo=0, yhi=70, center=LEFT * 0.8 + DOWN * 0.2, ticks=(10, 100, 1000))
        cols = {"baffle": GREY_A, "sealed": BLUE, "vented": TUNE}
        cs = VGroup(*[curve(f, np.minimum(d["Z"][k], 70), ax.to, color=c, width=2.5) for k, c in cols.items()])
        key = VGroup(label(r"open baffle", font_size=17, color=GREY_A), label(r"sealed, \ 50 L", font_size=17, color=BLUE), label(r"vented, \ 50 L at 38 Hz", font_size=17, color=TUNE)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.4)
        note = label(r"a vented box shows two peaks, \ with the tuning frequency in the dip between them: \ how builders check a port", font_size=17, color=WHITE).to_edge(DOWN, buff=0.45)
        yl = label(r"$\Omega$", font_size=15, color=GREY_A).next_to(ax, LEFT, buff=0.15)
        head = label(r"what the amplifier sees", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The amplifier sees the box too. <bookmark mark='a'/> On an open baffle, one impedance peak at the driver's "
            "resonance; in a sealed box, one peak, higher in frequency. <bookmark mark='b'/> In a vented box, two peaks, with "
            "the port's tuning in the dip between them, where the port does the work and the cone hardly moves. Builders "
            "measure exactly this to check a port's tuning."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yl), FadeIn(ghost(cs, 0.25)))
            vo.wait_until("a")
            self.play(Create(cs[0]), Create(cs[1]), FadeIn(key[:2]))
            vo.wait_until("b")
            self.play(Create(cs[2]), FadeIn(key[2]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def port(self):
        d = load("driver")
        b = d["b4"]
        Vb = b["Vb_l"] / 1000
        S = 3.14159 * 0.035 ** 2
        Leff = 343.0 ** 2 * S / (4 * 3.14159 ** 2 * b["fb"] ** 2 * Vb)
        L = Leff - 1.7 * 0.035
        lines = VGroup(
            MathTex(r"f_b = \frac{c}{2\pi}\sqrt{\frac{S}{V_b\,L_{\text{eff}}}}", font_size=38),
            MathTex(rf"S = \pi (3.5\ \text{{cm}})^2,\ V_b = {b['Vb_l']:.1f}\ \text{{L}},\ f_b = {b['fb']:.0f}\ \text{{Hz}}: \quad L_{{\text{{eff}}}} = {100 * Leff:.1f}\ \text{{cm}}", font_size=30),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.8)
        notes = VGroup(label(rf"less the air that moves with the ends of the tube \ (about 1.7 radii): \ a tube {100 * L:.0f} cm long", font_size=18, color=WHITE),
                       label(r"Part 2's bottle, \ with the box as the bottle and the port as its neck", font_size=18, color=TUNE),
                       label(r"too narrow a port and the air rushes and chuffs; \ too wide and it will not fit in the box", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"how long is the port?", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How long must the port be? <bookmark mark='a'/> The Helmholtz formula of Part 2: the tuning frequency is c over two "
            "pi, times the square root of the port's area over the box's volume times the port's effective length. "
            f"<bookmark mark='b'/> For a port seven centimetres across in our {say(b['Vb_l'], 1)}-litre box, tuned to forty "
            f"hertz, the effective length is {say(100 * Leff, 1)} centimetres; <bookmark mark='c'/> less the air that moves with "
            f"the ends of the tube, a tube about {say(100 * L)} centimetres long. It is Part 2's bottle, with the box as the "
            "bottle and the port as its neck. Too narrow a port and the air rushes and chuffs; too wide and it will not fit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()
