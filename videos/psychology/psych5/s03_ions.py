from __future__ import annotations

import numpy as np

from videos.psychology.psych5.common import *  # noqa: F403


class Ions(VoiceoverScene):
    def construct(self):
        self.card()
        self.gradient()
        self.nernst()
        self.goldman()

    def card(self):
        card = chapter_card(2, r"Ions and the membrane", r"Why does a living cell sit at a voltage?",
                            lit={1889: r"Nernst's equation"}, part=PART, scale=("molecule", "neuron"),
                            marr=("tissue",))
        with self.voiceover(
            "Chapter two. Ions and the membrane."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def gradient(self):
        d = load("ions")
        head = heading(r"Two forces on one ion")
        mem = membrane(9.0, y=0.0)
        rng = np.random.default_rng(3)
        k_in = ions(34, (-4.2, 4.2, -2.3, -0.55), K, rng)
        k_out = ions(3, (-4.2, 4.2, 0.55, 2.0), K, rng)
        pore = channel(0.0, 0.0, K)
        lab_out = label(r"outside", font_size=24, color=GREY_A).move_to([-5.4, 1.3, 0])
        lab_in = label(r"inside the cell", font_size=24, color=GREY_A).move_to([-5.4, -1.4, 0])
        conc = VGroup(
            label(rf"potassium outside: \ {d['conc']['K'][0]:.0f}", font_size=24, color=K).move_to([5.6, 1.3, 0]),
            label(rf"inside: \ {d['conc']['K'][1]:.0f}", font_size=24, color=K).move_to([5.6, -1.4, 0]))
        keep_in_frame(VGroup(lab_out, lab_in, conc))
        diff = Arrow([-1.3, -1.0, 0], [-1.3, 1.0, 0], color=K, stroke_width=6, buff=0)
        diff_l = label(r"diffusion", font_size=26, color=K).next_to(diff.get_end(), LEFT, buff=0.15).shift(DOWN * 0.15)
        field = Arrow([1.3, 1.0, 0], [1.3, -1.0, 0], color=THRESH, stroke_width=6, buff=0)
        field_l = label(r"voltage", font_size=26, color=THRESH).next_to(field.get_start(), UR, buff=0.06)
        charges = VGroup(*[label(r"$+$", font_size=30, color=THRESH).move_to([x, 0.62, 0]) for x in (-3.4, -2.2, 2.2, 3.4)],
                         *[label(r"$-$", font_size=30, color=THRESH).move_to([x, -0.62, 0]) for x in (-3.4, -2.2, 2.2, 3.4)])
        meter = VGroup(label(r"inside, relative to outside", font_size=22, color=GREY_A),
                       label(rf"${d['nernst']['K']:.0f}$ mV", font_size=44, color=THRESH)).arrange(DOWN, buff=0.1)
        meter.to_edge(DOWN, buff=0.45)
        movers = VGroup(*[Dot([0, -0.9 - 0.25 * i, 0], radius=0.07, color=K) for i in range(3)])
        tag = note(r"schematic; \ concentrations in mM, the usual figures for a squid axon").to_corner(DR, buff=0.2)
        with self.voiceover(
            "A cell is a bag of salty water in a bath of differently salty water, and the difference is the "
            "whole story. <bookmark mark='a'/> Inside a nerve cell, potassium is concentrated: about twenty "
            "times more of it than outside. Each potassium ion carries one positive charge. The cell spends "
            "energy to keep it that way, with pumps we'll leave running in the background. "
            "<bookmark mark='b'/> Now put a channel in the membrane that lets potassium through, and only "
            "potassium. <bookmark mark='c'/> Diffusion does what it always does: ions wander from where they're "
            "crowded to where they aren't. Potassium leaks out. <bookmark mark='d'/> But each ion that leaves "
            "takes a positive charge with it, and leaves the inside a little negative. That negative charge "
            "pulls potassium back. <bookmark mark='e'/> So there are two forces on the same ion, pointing "
            "opposite ways. Diffusion pushes out; the voltage pulls in. The leak goes on until they balance. "
            f"<bookmark mark='f'/> For these concentrations they balance when the inside is {abs(d['nernst']['K']):.0f} "
            "millivolts negative. It takes very few ions to get there; the concentrations hardly change. And "
            "notice that nothing has to keep moving. It's an equilibrium, a battery made of salt."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(mem), FadeIn(lab_out), FadeIn(lab_in))
            vo.wait_until("a")
            self.play(FadeIn(k_in, lag_ratio=0.02), FadeIn(k_out), FadeIn(conc), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(pore, scale=1.3))
            vo.wait_until("c")
            self.play(GrowArrow(diff), FadeIn(diff_l))
            self.play(LaggedStart(*[m.animate.move_to([0.3 * (i - 1), 1.0 + 0.2 * i, 0]) for i, m in enumerate(movers)],
                                  lag_ratio=0.4), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(charges, lag_ratio=0.1), run_time=1.5)
            vo.wait_until("e")
            self.play(GrowArrow(field), FadeIn(field_l))
            vo.wait_until("f")
            self.play(FadeIn(meter, shift=UP * 0.15))
        self.clear_scene()

    def nernst(self):
        d = load("ions")
        head = heading(r"The Nernst potential: \ where the two forces balance")
        eq = MathTex(r"E \;=\; \frac{RT}{zF}\,\ln\frac{[\text{outside}]}{[\text{inside}]}", font_size=46)
        eq.move_to([-3.6, 1.7, 0])
        A = axes([0, 2.65], [-160, 10], x_length=5.6, y_length=3.3, xticks=[0, 1, 2, np.log10(400)],
                 xfmt=lambda v: f"{10 ** v:.0f}", yticks=[-150, -100, -50, 0], xlabel=r"potassium outside (mM, log scale)",
                 ylabel=r"$E_K$ (mV)", center=[-3.6, -1.35, 0], font_size=20)
        ax = A.ax
        line = curve(ax, np.log10(d["k_out"]), d["e_k_curve"], K, stroke_width=4)
        here = Dot(ax.c2p(np.log10(d["conc"]["K"][0]), d["nernst"]["K"]), radius=0.1, color=THRESH)
        rows = VGroup()
        for ion, name, color in (("K", r"potassium", K), ("Na", r"sodium", NA)):
            o, i = d["conc"][ion]
            rows.add(VGroup(label(name, font_size=30, color=color),
                            label(rf"{o:.0f} outside, \ {i:.0f} inside", font_size=24, color=GREY_A),
                            label(rf"$E = {d['nernst'][ion]:+.0f}$ mV", font_size=34, color=color)).arrange(
                                DOWN, aligned_edge=LEFT, buff=0.08))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        slope = wrapped_label(rf"Ten times the concentration ratio moves $E$ by {d['slope_20c']:.0f} mV "
                              r"(at $20^\circ$C).", 5.0, 27, WHITE)
        side = VGroup(rows, slope).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.7, -0.2, 0])
        tag = note(rf"computed at ${d['temp_c']}^\circ$C; \ $RT/F = {d['rt_f']:.1f}$ mV").to_corner(DR, buff=0.2)
        why = VGroup(
            VGroup(label(r"$\ln$ of the concentration ratio", font_size=30, color=K),
                   label(r"how hard diffusion pushes", font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06),
            VGroup(label(r"$z$, the ion's charge", font_size=30, color=THRESH),
                   label(r"how hard a given voltage pulls", font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06),
            VGroup(label(rf"$RT/F \approx {d['rt_f']:.0f}$ mV", font_size=30, color=VOLT),
                   label(r"the energy of thermal jostling, per unit of charge", font_size=24, color=GREY_A)).arrange(
                       DOWN, aligned_edge=LEFT, buff=0.06),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.2, 0.9, 0])
        with self.voiceover(
            "The balance point has a formula, found by the chemist Walther Nernst in 1889, and it has only one "
            "idea in it. <bookmark mark='a'/> The push of diffusion depends on the ratio of the two "
            "concentrations. <bookmark mark='p'/> The pull of the voltage depends on the charge. Set them equal "
            "and the voltage is a constant times the logarithm of the ratio. <bookmark mark='q'/> The constant "
            "is thermal: it's about twenty-five "
            "millivolts, the energy of random jostling at this temperature, per unit of charge. "
            "<bookmark mark='b'/> Because of the logarithm, every tenfold change in the ratio moves the balance "
            f"by the same amount, about {d['slope_20c']:.0f} millivolts. You can test that: change the "
            "potassium in the bath and the cell's voltage follows this line. That experiment is how we know "
            "the resting voltage is mostly a potassium battery. <bookmark mark='c'/> For potassium in the squid "
            f"axon, the balance is at minus {abs(d['nernst']['K']):.0f} millivolts. <bookmark mark='d'/> Now "
            "sodium. Sodium is the other way round: scarce inside, plentiful outside. So its battery points "
            f"the other way, plus {d['nernst']['Na']:.0f} millivolts. One membrane, two batteries of opposite "
            "sign, over a hundred millivolts apart. Remember those two numbers. The nerve signal lives "
            "between them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq), run_time=2.0)
            self.play(FadeIn(why[0], shift=UP * 0.1))
            vo.wait_until("p")
            self.play(FadeIn(why[1], shift=UP * 0.1))
            vo.wait_until("q")
            self.play(FadeIn(why[2], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeOut(why), run_time=0.6)
            self.play(FadeIn(A), Create(line), FadeIn(slope), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(here, scale=1.5), FadeIn(rows[0], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(rows[1], shift=UP * 0.1))
        self.clear_scene()

    def goldman(self):
        d = load("ions")
        head = heading(r"Two batteries, and a dial between them")
        A = axes([-2, 2], [-90, 70], x_length=7.4, y_length=4.2, xticks=[-2, -1, 0, 1, 2],
                 xfmt=lambda v: {-2: r"\tfrac{1}{100}", -1: r"\tfrac{1}{10}", 0: "1", 1: "10", 2: "100"}[int(round(v))],
                 yticks=[-80, -40, 0, 40], xlabel=r"how easily sodium crosses, relative to potassium",
                 ylabel=r"membrane potential (mV)", center=[-2.6, -0.5, 0])
        ax = A.ax
        line = curve(ax, np.log10(d["ratio"]), d["goldman"], VOLT, stroke_width=4)
        ek = DashedLine(ax.c2p(-2, d["nernst"]["K"]), ax.c2p(2, d["nernst"]["K"]), color=K, stroke_width=2)
        ena = DashedLine(ax.c2p(-2, d["nernst"]["Na"]), ax.c2p(2, d["nernst"]["Na"]), color=NA, stroke_width=2)
        ek_l = label(r"$E_K$", font_size=26, color=K).next_to(ek, RIGHT, buff=0.1)
        ena_l = label(r"$E_{Na}$", font_size=26, color=NA).next_to(ena, RIGHT, buff=0.1)
        rest = Dot(ax.c2p(np.log10(d["rest_ratio"]), d["rest_v"]), radius=0.11, color=K)
        peak = Dot(ax.c2p(np.log10(d["peak_ratio"]), d["peak_v"]), radius=0.11, color=NA)
        rest_l = label(r"at rest", font_size=24, color=K).next_to(rest, UP, buff=0.1)
        peak_l = label(r"at the peak of the signal", font_size=24, color=NA).next_to(peak, DR, buff=0.12)
        side = VGroup(
            wrapped_label(r"A membrane open to both ions settles between the two batteries, nearer the one "
                          r"whose channels are more open.", 4.4, 27, WHITE),
            wrapped_label(rf"Mostly potassium: \ about ${d['rest_v']:.0f}$ mV.", 4.4, 27, K),
            wrapped_label(rf"Open the sodium channels: \ about ${d['peak_v']:+.0f}$ mV.", 4.4, 27, NA),
            wrapped_label(r"No ion concentration has to change. \ Only which doors are open.", 4.4, 27, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.75, -0.3, 0])
        keep_in_frame(side)
        tag = note(r"computed: the Goldman-Hodgkin-Katz voltage for potassium and sodium").to_corner(DR, buff=0.2)
        with self.voiceover(
            "A real membrane lets both ions through, a little. So where does the voltage settle? "
            "<bookmark mark='a'/> Between the two batteries. And exactly where depends on which ion crosses "
            "more easily. This is the Goldman equation, and you can read it as a dial. <bookmark mark='b'/> "
            "Turn the dial to the left, where the membrane passes potassium far more readily than sodium, and "
            "the voltage sits near the potassium battery. That's a neuron at rest: about minus sixty, "
            "inside negative. <bookmark mark='c'/> Now turn the dial to the right. Let sodium through several "
            "hundred times more easily than before, and the voltage swings to the other battery: positive "
            "inside. <bookmark mark='d'/> Look at what that means. To move the voltage of a cell by a tenth "
            "of a volt you don't have to move the salt. The concentrations barely change. You only have to "
            "open and close doors. A nerve signal is going to be exactly this: sodium doors opening, the "
            "voltage flying up toward the sodium battery, then potassium doors bringing it back. What we need "
            "to find out is what turns the dial."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(ek), Create(ena), FadeIn(ek_l), FadeIn(ena_l))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rest, scale=1.5), FadeIn(rest_l), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(peak, scale=1.5), FadeIn(peak_l), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()
