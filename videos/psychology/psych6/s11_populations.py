from __future__ import annotations

import numpy as np

from videos.psychology.psych6.common import *  # noqa: F403


class Populations(VoiceoverScene):
    def construct(self):
        self.card()
        self.berger()
        self.equations()
        self.three_regimes()

    def card(self):
        card = chapter_card(10, r"Populations", r"What do a million neurons do together?",
                            lit={1929: r"Berger's EEG", 1972: r"Wilson and Cowan"}, part=PART,
                            scale=("circuit", "brain"), marr=("how",))
        with self.voiceover(
            "Chapter ten. Populations."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def berger(self):
        head = heading(r"A rhythm you can record through the skull")
        g = np.random.default_rng(29)
        t = np.linspace(0, 6, 900)
        env = 0.55 + 0.35 * np.sin(2 * np.pi * 0.35 * t + 1.0)
        closed = env * np.sin(2 * np.pi * 10 * t) + 0.08 * g.standard_normal(len(t))
        opened = 0.16 * np.sin(2 * np.pi * 21 * t + 0.4) + 0.12 * g.standard_normal(len(t))
        cut = 3.0
        v = np.where(t < cut, closed, opened)
        x0, x1, y0 = -6.3, 1.2, 0.6
        tr = VMobject(color=VOLT, stroke_width=2.5).set_points_as_corners(
            [np.array([x0 + (x1 - x0) * a / 6, y0 + 1.05 * b, 0]) for a, b in zip(t, v)])
        mark = DashedLine([x0 + (x1 - x0) * cut / 6, y0 - 1.3, 0], [x0 + (x1 - x0) * cut / 6, y0 + 1.3, 0],
                          color=THRESH, stroke_width=2)
        lab = VGroup(label(r"eyes closed: \ ten a second", font_size=26, color=WHITE).move_to(
            [x0 + (x1 - x0) * 0.25, y0 + 1.6, 0]),
            label(r"eyes open: \ smaller, faster", font_size=26, color=WHITE).move_to(
                [x0 + (x1 - x0) * 0.75, y0 + 1.6, 0]))
        scale = VGroup(Line([x0, y0 - 1.45, 0], [x0 + (x1 - x0) / 6, y0 - 1.45, 0], color=GREY_B, stroke_width=3),
                       label(r"1 second", font_size=20, color=GREY_B).move_to([x0 + (x1 - x0) / 12, y0 - 1.7, 0]))
        hd = head_outline(3.4).move_to([4.4, 0.6, 0])
        elec = VGroup(Dot(hd.get_top() + DOWN * 0.12 + LEFT * 0.3, radius=0.09, color=THRESH),
                      Line(hd.get_top() + DOWN * 0.12 + LEFT * 0.3, hd.get_top() + UP * 0.5 + LEFT * 0.9, color=THRESH,
                           stroke_width=3))
        rows = VGroup(
            wrapped_label(r"An electrode on the scalp is centimetres from the cells. \ It sees a signal only when "
                          r"very many of them do the same thing at the same time.", 12.6, 27, WHITE),
            wrapped_label(r"So change the variable: \ not one cell's voltage, \ but the fraction of a population "
                          r"that is active.", 12.6, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "In the nineteen-twenties, in Jena, the psychiatrist Hans Berger attached electrodes to people's "
            "scalps and recorded a tiny, fluctuating voltage. <bookmark mark='a'/> When his subjects sat with "
            "their eyes closed, the voltage swung in a steady rhythm, about ten waves a second. "
            "<bookmark mark='b'/> When they opened their eyes, the rhythm broke up into something smaller and "
            "faster. He published in 1929, and this was the first recording of the human brain at work: the "
            "electroencephalogram, the EEG. <bookmark mark='c'/> Think about what it takes to see that. The "
            "electrode is centimetres from the cells, on the far side of the skull. One neuron's voltage "
            "would be lost. A signal reaches the scalp only when a very large number of neurons do the same "
            "thing at the same time. So a rhythm on the scalp means whole populations, rising and falling "
            "together. <bookmark mark='d'/> We can't follow that cell by cell. So we change the variable. "
            "Not the voltage of one neuron, but the fraction of a population that's active."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hd), FadeIn(elec))
            vo.wait_until("a")
            self.play(Create(tr), FadeIn(scale), run_time=8.0, rate_func=linear)
            self.play(FadeIn(lab[0]))
            vo.wait_until("b")
            self.play(Create(mark), FadeIn(lab[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1], shift=UP * 0.1))
        self.clear_scene()

    def _loop(self, center, r=0.6):
        c = np.asarray(center, float)
        e = unit("E", r, EXC, 34).move_to(c + LEFT * 1.6)
        i = unit("I", r, INH, 34).move_to(c + RIGHT * 1.6)
        e_i = excite(e.get_right() + UP * 0.17, i.get_left() + UP * 0.17, buff=0.06)
        i_e = inhibit(i.get_left() + DOWN * 0.17, e.get_right() + DOWN * 0.17)
        e_e = CurvedArrow(e.get_top() + LEFT * 0.24 + DOWN * 0.03, e.get_top() + RIGHT * 0.24 + DOWN * 0.03, angle=-4.6,
                          color=EXC, stroke_width=4, tip_length=0.18)
        drive = excite(e.get_bottom() + DOWN * 1.1, e.get_bottom(), color=GREY_A, buff=0.06)
        drive_l = label(r"drive $P$", font_size=24, color=GREY_A).next_to(drive, DOWN, buff=0.08)
        g = VGroup(e, i, e_i, i_e, e_e, drive, drive_l)
        g.e, g.i, g.e_i, g.i_e, g.e_e, g.drive = e, i, e_i, i_e, e_e, VGroup(drive, drive_l)
        return g

    def equations(self):
        head = heading(r"Two populations, \ two equations")
        g = self._loop([-3.6, 0.7, 0])
        names = VGroup(label(r"excitatory cells", font_size=24, color=EXC).next_to(g.e, LEFT, buff=0.2),
                       label(r"inhibitory cells", font_size=24, color=INH).next_to(g.i, DOWN, buff=0.2))
        keep_in_frame(VGroup(g, names))
        eqs = VGroup(
            MathTex(r"\tau\,\frac{dE}{dt} = -E + S\big(w_{EE}E - w_{EI}I + P\big)", font_size=36, color=EXC),
            MathTex(r"\tau\,\frac{dI}{dt} = -I + S\big(w_{IE}E - w_{II}I\big)", font_size=36, color=INH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        cyc = VGroup(
            label(r"1. \ $E$ rises, \ and excites itself", font_size=27, color=WHITE),
            label(r"2. \ $E$ recruits $I$", font_size=27, color=WHITE),
            label(r"3. \ $I$ shuts $E$ down", font_size=27, color=WHITE),
            label(r"4. \ $I$ loses its drive, and falls", font_size=27, color=WHITE),
            label(r"5. \ $E$ is free to rise again", font_size=27, color=P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        right = VGroup(eqs, cyc).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.6, -0.3, 0])
        keep_in_frame(right)
        who = label(r"Wilson and Cowan (1972)", font_size=24, color=GREY_B).next_to(g, DOWN, buff=0.5)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "In 1972 Hugh Wilson and Jack Cowan wrote down the simplest model of that kind. "
            "<bookmark mark='a'/> Two populations in one patch of tissue: excitatory cells and inhibitory "
            "cells. E is the fraction of the excitatory cells that are active; I, the fraction of the "
            "inhibitory ones. <bookmark mark='b'/> The excitatory cells excite each other, and they excite "
            "the inhibitory cells. The inhibitory cells inhibit the excitatory ones. And something outside "
            "drives the excitatory population. <bookmark mark='c'/> Two equations, of the kind you've now "
            "seen three times: each activity relaxes toward an S-shaped function of what that population "
            "receives. <bookmark mark='d'/> And you can read off what might happen. E rises, and feeds "
            "itself. That recruits I. I shuts E down. With E quiet, I loses its own drive and falls. And "
            "then E is free to rise again. A loop with a delay in it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g.e), FadeIn(g.i), FadeIn(names), FadeIn(who))
            vo.wait_until("b")
            self.play(Create(g.e_e), GrowArrow(g.e_i))
            self.play(FadeIn(g.i_e), FadeIn(g.drive))
            vo.wait_until("c")
            self.play(Write(eqs[0]), Write(eqs[1]), run_time=3.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in cyc], lag_ratio=0.8), run_time=11.0)
        self.clear_scene()

    def three_regimes(self):
        p = load("populations")
        head = heading(r"Turn up the drive: \ rest, rhythm, saturation")
        A = axes([0, 300], [0, 1.05], x_length=6.0, y_length=3.6, xticks=[0, 100, 200, 300], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"time (ms)", ylabel=r"fraction of excitatory cells active",
                 center=[-3.7, -0.2, 0])
        ax = A.ax
        t = p["t"]
        keep = t <= 300
        rest = trace(ax, t[keep], p["rest_e"][keep], GREY_B, 3)
        osc = trace(ax, t[keep], p["osc_e"][keep], EXC, 3.5)
        osc_i = DashedVMobject(curve(ax, t[keep], p["osc_i"][keep], INH, stroke_width=2.5), num_dashes=80)
        sat = trace(ax, t[keep], p["sat_e"][keep], BAD, 3)
        lg = legend([(GREY_B, r"no drive: \ rest"), (EXC, rf"drive 1.25: \ {p['frequency']:.0f} a second"),
                     (INH, r"the inhibitory cells (dashed)"), (BAD, r"drive 3.5: \ pinned at the ceiling")],
                    font_size=22)
        lg.move_to(ax.c2p(185, 0.68))
        B = axes([0, 4], [0, 1.05], x_length=5.0, y_length=3.6, xticks=[0, 1, 2, 3, 4], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"drive $P$", ylabel=r"range of $E$", center=[3.6, -0.2, 0])
        bx = B.ax
        dr = p["drives"]
        band = Polygon(*[bx.c2p(a, b) for a, b in zip(dr, p["e_hi"])],
                       *[bx.c2p(a, b) for a, b in zip(dr[::-1], p["e_lo"][::-1])], stroke_width=0, fill_color=EXC,
                       fill_opacity=0.35)
        top, bot = trace(bx, dr, p["e_hi"], EXC, 3), trace(bx, dr, p["e_lo"], EXC, 3)
        zones = VGroup(label(r"rest", font_size=22, color=GREY_B).move_to(bx.c2p(0.5, 0.3)),
                       label(rf"rhythm: \ {p['freq_onset']:.0f} to {p['freq_max']:.0f} a second", font_size=22,
                             color=EXC).move_to(bx.c2p(1.75, 1.02)),
                       label(r"stuck on", font_size=22, color=BAD).move_to(bx.c2p(3.55, 0.75)))
        end = wrapped_label(r"No cell in this model oscillates. \ The rhythm belongs to the loop, \ and it needs "
                            r"excitation and inhibition in balance.", 9.6, 27, P.ACCENT).to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.5)
        tag = psyche_tag()
        with self.voiceover(
            "Compute it. <bookmark mark='a'/> With no drive, the population sits at rest. Almost nothing is "
            "active. <bookmark mark='b'/> Turn the drive up past a critical value, and it doesn't settle at "
            "some higher level. It starts to swing, about "
            f"{p['frequency']:.0f} times a second, with the inhibitory cells following the excitatory ones "
            "round the loop. <bookmark mark='c'/> Turn the drive up much further, and the rhythm stops again. "
            "Now the excitatory population is pinned at its ceiling, and inhibition can't pull it down. "
            "<bookmark mark='d'/> Here's the whole picture: the range that E covers, at each level of drive. "
            f"Rest. Then, at a drive of {p['onset']:.0f}, a rhythm switches on, and its tempo runs from "
            f"{p['freq_onset']:.0f} to {p['freq_max']:.0f} waves a second depending on the drive. Then "
            "saturation. <bookmark mark='e'/> Two things to take away. No cell in this model oscillates. The "
            "rhythm is a property of the loop. And the interesting behaviour lives in the middle, where "
            "excitation and inhibition are in balance. Lose the balance toward excitation, and you get "
            "runaway activity; in a real brain, that's a seizure. This isn't a claim about where Berger's "
            "rhythm comes from. Real rhythms have several generators. It's the simplest demonstration that "
            "populations wired this way will oscillate without being told to. What the EEG can and can't "
            "tell us is Part 8."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(rest), FadeIn(lg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(osc), Create(osc_i), FadeIn(lg[1]), FadeIn(lg[2]), run_time=7.0, rate_func=linear)
            vo.wait_until("c")
            self.play(Create(sat), FadeIn(lg[3]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(B))
            self.play(Create(top), Create(bot), FadeIn(band), run_time=4.0)
            self.play(FadeIn(zones))
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()
