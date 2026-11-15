from __future__ import annotations

import numpy as np

from videos.music.music54.common import *  # noqa: F403


class Driver(SoundScene):
    def construct(self):
        chapter(self, 5, r"The loudspeaker as a filter", r"Why can't a small loudspeaker play bass?")
        self.anatomy()
        self.params()
        self.damping()
        self.baffle()
        self.efficiency()

    # ------------------------------------------------------------------
    def anatomy(self):
        items = [
            (r"1925: \ Chester Rice and Edward Kellogg's moving-coil loudspeaker: \ the design still in almost every speaker", WHITE),
            (r"a coil in a magnet's gap, \ glued to a cone, \ held by a spider and a surround", WHITE),
            (r"electrically: \ the coil's resistance; \ mechanically: \ the cone's mass, \ the suspension's spring, \ friction", WHITE),
            (r"a mass on a spring has a resonance: \ below it, \ the spring rules; \ above it, \ the mass", WHITE),
            (r"so a loudspeaker is a high-pass filter, \ and its resonance sets how low it plays", TUNE),
        ]
        rows_scene(self, r"a mass on a spring with a motor", items,
                   "Now run the transducer the other way. <bookmark mark='b'/> In 1925 Chester Rice and Edward Kellogg built the "
                   "moving-coil loudspeaker, the design still in almost every speaker: <bookmark mark='c'/> a coil in a magnet's gap, "
                   "glued to a cone, held by a spider and a surround. <bookmark mark='d'/> Electrically it is the coil's resistance; "
                   "mechanically, the cone's mass, the suspension's spring and some friction. A mass on a spring has a resonance: "
                   "below it the spring rules, above it the mass. <bookmark mark='f'/> So a loudspeaker is a high-pass filter, and "
                   "its resonance sets how low it plays.", marks="bcdf")

    # ------------------------------------------------------------------
    def params(self):
        d = load("driver")["ts"]
        rows = VGroup(
            VGroup(label(r"$f_s$", font_size=22, color=TUNE), label(rf"{d['fs']:.0f} Hz", font_size=20, color=WHITE), label(r"the free-air resonance", font_size=17, color=GREY_A)),
            VGroup(label(r"$Q_{es}, \ Q_{ms}, \ Q_{ts}$", font_size=22, color=TUNE), label(rf"{d['Qes']:.2f}, \ {d['Qms']:.1f}, \ {d['Qts']:.2f}", font_size=20, color=WHITE), label(r"how sharp: \ electrical, \ mechanical, \ total", font_size=17, color=GREY_A)),
            VGroup(label(r"$V_{as}$", font_size=22, color=TUNE), label(rf"{d['Vas_l']:.0f} litres", font_size=20, color=WHITE), label(r"the volume of air as stiff as the suspension", font_size=17, color=GREY_A)),
            VGroup(label(r"$S_d$", font_size=22, color=TUNE), label(rf"{d['Sd_cm2']:.0f} cm$^2$", font_size=20, color=WHITE), label(r"the cone's area", font_size=17, color=GREY_A)),
            VGroup(label(r"$R_e$", font_size=22, color=TUNE), label(rf"{d['Re']:.0f} $\Omega$", font_size=20, color=WHITE), label(r"the coil's resistance", font_size=17, color=GREY_A)),
            VGroup(label(r"derived: \ $Bl, \ M_{ms}, \ C_{ms}$", font_size=20, color=BLUE), label(rf"{d['Bl']:.1f} T m, \ {d['Mms_g']:.1f} g, \ {d['Cms_mm_per_N']:.2f} mm/N", font_size=20, color=WHITE), label(r"motor, \ moving mass, \ compliance", font_size=17, color=GREY_A)),
        ).arrange(DOWN, buff=0.3)
        for r in rows:
            r[0].set_x(-4.4 + r[0].width / 2)
            r[1].set_x(-0.4)
            r[2].set_x(2.4 + r[2].width / 2)
        rows.move_to(DOWN * 0.2)
        head = label(r"a woofer in Thiele--Small parameters", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A woofer is described by a handful of numbers, named after Neville Thiele and Richard Small, who showed in the "
            "1960s and 1970s that they are all a designer needs. <bookmark mark='a'/> Its resonance in free air, forty hertz "
            "for ours. <bookmark mark='b'/> Three Qs, how sharp the resonance is: from the electrical side, where the motor "
            "acts as a brake, from the mechanical side, and in total. <bookmark mark='c'/> V a s, the volume of air as stiff as "
            "the suspension, fifty litres. The cone's area, the coil's resistance. <bookmark mark='d'/> From them follow the "
            "motor strength, the moving mass and the compliance, and the whole circuit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:5]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def baffle(self):
        d = load("driver")
        f = np.array(d["f"])
        Z = np.array(d["Z"]["baffle"])
        ax = logf_axes(width=8.0, height=3.0, flo=10, fhi=2000, ylo=0, yhi=70, center=DOWN * 0.3, ticks=(10, 100, 1000))
        cv = curve(f, np.minimum(Z, 70), ax.to, color=BLUE, width=3)
        pk = int(np.argmax(Z))
        dot = Dot(ax.to(f[pk], min(Z[pk], 70)), radius=0.07, color=EAR)
        pl = label(rf"{Z[pk]:.0f} $\Omega$ at {f[pk]:.0f} Hz", font_size=16, color=EAR).next_to(dot, RIGHT, buff=0.15)
        yl = label(r"impedance, \ $\Omega$", font_size=15, color=GREY_A).next_to(ax, LEFT, buff=0.15)
        note = label(r"at resonance the cone moves most, \ and its motion makes a voltage that opposes the current: \ the impedance peaks", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"the woofer's impedance, \ simulated", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The simulator solves the circuit at every frequency. <bookmark mark='a'/> Here is the woofer's electrical impedance "
            "on a large baffle: six ohms almost everywhere, <bookmark mark='b'/> but at resonance it rises to "
            f"{say(Z[pk])} ohms, because the cone moves most there, and its moving coil makes a voltage that opposes the current. "
            "This peak is how Thiele-Small parameters are measured: from the impedance alone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yl), FadeIn(ghost(cv, 0.3)))
            vo.wait_until("a")
            self.play(Create(cv), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(dot), FadeIn(pl), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def efficiency(self):
        d = load("driver")
        ts = d["ts"]
        eta = 4 * np.pi ** 2 / 343.0 ** 3 * ts["fs"] ** 3 * ts["Vas_l"] / 1000 / ts["Qes"]
        lines = VGroup(
            MathTex(r"\eta_0 = \frac{4\pi^2}{c^3}\,\frac{f_s^3\,V_{as}}{Q_{es}}", font_size=40),
            MathTex(rf"= {100 * eta:.2f}\%", font_size=36),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.8)
        notes = VGroup(label(rf"under 1 per cent of the amplifier's power becomes sound: \ the simulator gives {d['sens_1w1m']:.0f} dB at 1 m for 2.83 V", font_size=18, color=WHITE),
                       label(r"Hofmann's iron law: \ deep bass, \ a small box, \ high efficiency: \ choose two", font_size=19, color=TUNE),
                       label(r"$f_s^3$: \ to go an octave lower at the same efficiency needs eight times the volume", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"how much becomes sound", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How efficient is it? <bookmark mark='a'/> Small's formula: four pi squared over c cubed, times f s cubed, times V a "
            f"s, over Q e s. For our woofer, {say(100 * eta, 2)} per cent: <bookmark mark='b'/> under one per cent of the "
            "amplifier's power becomes sound, and the simulator agrees, about ninety-two decibels at a metre. "
            "<bookmark mark='c'/> Hidden in the formula is the loudspeaker designer's iron law, named after Josef Anton "
            "Hofmann: deep bass, a small box, high efficiency; choose two. The resonance enters cubed: an octave lower at the "
            "same efficiency needs eight times the volume."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(lines))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def damping(self):
        items = [
            (r"a moving coil is a generator: \ its back voltage drives a current through the amplifier", WHITE),
            (r"if the amplifier's output resistance is tiny, \ that current brakes the cone: \ electrical damping, \ the $Q_{es}$", WHITE),
            (r"a valve amplifier with a high output resistance damps less: \ the bass rings longer and the response follows the impedance", WHITE),
            (r"the speaker cable's resistance adds to the coil's", WHITE),
            (r"the amplifier and the loudspeaker are one circuit", TUNE),
        ]
        rows_scene(self, r"the amplifier as a brake", items,
                   "The amplifier is part of the loudspeaker. <bookmark mark='b'/> A moving coil is also a generator, and its back voltage drives a current through the amplifier. <bookmark mark='c'/> If the amplifier's output resistance is tiny, that current brakes the cone: electrical damping, the Q e s of the parameters. <bookmark mark='d'/> A valve amplifier with a high output resistance damps less, so the bass rings longer and the response follows the impedance curve. <bookmark mark='e'/> The speaker cable's resistance adds to the coil's. <bookmark mark='f'/> The amplifier and the loudspeaker are one circuit.", marks="bcdef")
