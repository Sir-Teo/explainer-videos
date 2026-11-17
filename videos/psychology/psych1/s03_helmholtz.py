from __future__ import annotations

import numpy as np

from videos.psychology.psych1.common import *  # noqa: F403


class Helmholtz(VoiceoverScene):
    def construct(self):
        self.card()
        self.preparation()
        self.arithmetic()
        self.people()
        self.residue()

    def card(self):
        card = chapter_card(2, r"The speed of a nerve", r"Does a signal in the nervous system take time at all?",
                            lit={1850: r"Helmholtz times the nerve"}, part=PART, scale=("neuron",),
                            marr=("tissue",))
        with self.voiceover(
            "Chapter two. The speed of a nerve."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def prep(self):
        """The frog's nerve and calf muscle, with a near and a far electrode."""
        y = 1.55
        muscle = Ellipse(width=2.0, height=0.9, stroke_color=MUSCLE, stroke_width=2, fill_color=MUSCLE,
                         fill_opacity=0.75).move_to([4.7, y, 0])
        nerve = Line([-5.2, y, 0], muscle.get_left(), color=NERVE, stroke_width=7)
        m_lab = label(r"calf muscle", font_size=24, color=MUSCLE).next_to(muscle, UP, buff=0.15)
        n_lab = label(r"nerve", font_size=24, color=NERVE).next_to(nerve.get_left(), UP, buff=0.2).shift(RIGHT * 0.4)
        x_far, x_near = -3.6, 2.4

        def electrode(x, name):
            tip = Triangle(stroke_width=0, fill_color=WHITE, fill_opacity=1).scale(0.14).rotate(PI)
            tip.move_to([x, y + 0.27, 0])
            wire = Line([x, y + 0.36, 0], [x, y + 0.85, 0], color=GREY_A, stroke_width=3)
            t = label(name, font_size=24, color=WHITE).next_to(wire, UP, buff=0.1)
            return VGroup(tip, wire, t)

        far, near = electrode(x_far, r"shock here \dots"), electrode(x_near, r"\dots or here")
        g = VGroup(nerve, muscle, m_lab, n_lab, far, near)
        g.nerve, g.muscle, g.far, g.near, g.y, g.x_far, g.x_near = nerve, muscle, far, near, y, x_far, x_near
        return g

    def preparation(self):
        h = load("helmholtz")
        prep = self.prep()
        y = prep.y
        mueller = quote_card(r"The speed of nervous action will probably never be measured.",
                             r"Johannes M\"uller, the leading physiologist of the 1840s (paraphrase)", width=9.4,
                             font_size=36, color=GREY_B).move_to([0, 1.5, 0])
        hc = history_card(1850, r"Hermann Helmholtz, aged 28", r"M\"uller's student; \ professor of physiology in "
                          r"K\"onigsberg", color=NERVE, width=7.0, font_size=30).move_to([0, -1.5, 0])
        dist = Line([prep.x_far, y - 0.3, 0], [prep.x_near, y - 0.3, 0])
        br = brace_note(dist, rf"{h['length_mm'][0]:.0f} to {h['length_mm'][1]:.0f} mm more nerve", DOWN, NERVE,
                        font_size=26)
        # the two twitches, on a time axis in milliseconds
        A = axes([0, 12], [0, 1.1], x_length=7.4, y_length=2.3, xlabel=r"time after the shock (ms)",
                 xticks=[0, 2, 4, 6, 8, 10, 12], ylabel=r"muscle tension", center=[-1.6, -1.9, 0])
        ax = A.ax
        t = np.linspace(0, 12, 200)

        def twitch(t0):
            s = np.clip(t - t0, 0, None)
            return 1.05 * (1 - np.exp(-s / 3.0))

        delay = sum(h["delay_ms"]) / 2
        near_c = curve(ax, t, twitch(2.0), WHITE, 4)
        far_c = curve(ax, t, twitch(2.0 + delay), NERVE, 4)
        gap = Line(ax.c2p(2.0 + 2.2, twitch(2.0)[-1] * 0.52), ax.c2p(2.0 + 2.2 + delay, twitch(2.0)[-1] * 0.52),
                   color=P.ACCENT, stroke_width=4)
        gap_lab = MathTex(r"\Delta t", font_size=34, color=P.ACCENT).next_to(gap, UP, buff=0.08)
        leg = legend([(WHITE, r"shock near the muscle"), (NERVE, r"shock at the far end")], font_size=22)
        leg.next_to(A, RIGHT, buff=0.4)
        sch = schematic_tag(DR)
        pulse = glow_dot(prep.nerve.get_left(), color=P.ACCENT, radius=0.1)
        with self.voiceover(
            "In the eighteen-forties the leading physiologist in Europe, Johannes Müller, taught that the speed "
            "of nervous action would probably never be measured. Feeling and willing seemed instantaneous: you "
            "decide to move a finger, and it moves. <bookmark mark='a'/> Müller's student Hermann Helmholtz, "
            "twenty-eight years old and newly a professor in Königsberg, decided to try. <bookmark mark='b'/> "
            "His preparation was a frog's calf muscle with its nerve still attached. A brief electric shock to "
            "the nerve makes the muscle twitch. <bookmark mark='c'/> The idea is simple. Shock the nerve close "
            "to the muscle, and time the twitch. <bookmark mark='d'/> Then shock it at the far end, five or six "
            "centimetres away, and time the twitch again. The muscle is the same, and the shock is the same. "
            "<bookmark mark='e'/> So if the second twitch comes later, the difference is the time the signal "
            "took to travel the extra length of nerve."
        ) as vo:
            self.play(FadeIn(mueller, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeOut(hc), FadeOut(mueller))
            self.play(Create(prep.nerve), FadeIn(prep.muscle), FadeIn(prep[2]), FadeIn(prep[3]))
            vo.wait_until("c")
            self.play(FadeIn(prep.near), FadeIn(A), FadeIn(sch))
            pulse.move_to([prep.x_near, y, 0])
            self.play(FadeIn(pulse, run_time=0.2))
            self.play(pulse.animate.move_to(prep.muscle.get_left()), run_time=0.7, rate_func=linear)
            self.play(FadeOut(pulse, run_time=0.2), Indicate(prep.muscle, color=WHITE, scale_factor=1.12),
                      Create(near_c))
            vo.wait_until("d")
            self.play(FadeIn(prep.far), FadeIn(br))
            pulse.move_to([prep.x_far, y, 0])
            self.play(FadeIn(pulse, run_time=0.2))
            self.play(pulse.animate.move_to(prep.muscle.get_left()), run_time=2.4, rate_func=linear)
            self.play(FadeOut(pulse, run_time=0.2), Indicate(prep.muscle, color=WHITE, scale_factor=1.12),
                      Create(far_c), FadeIn(leg))
            vo.wait_until("e")
            self.play(Create(gap), FadeIn(gap_lab))
        self.clear_scene()

    def arithmetic(self):
        h = load("helmholtz")
        (l0, l1), (d0, d1) = h["length_mm"], h["delay_ms"]
        head = heading(r"Distance over time")
        given = VGroup(
            label(rf"extra nerve: \ ${l0:.0f}$ to ${l1:.0f}$ mm", font_size=34, color=NERVE),
            label(rf"extra delay: \ ${d0 / 1000:.4f}$ to ${d1 / 1000:.4f}$ s", font_size=34, color=P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        eq0 = MathTex(r"v", r"=", r"\frac{\Delta x}{\Delta t}", font_size=44)
        eq1 = MathTex(r"v", r"=", rf"\frac{{{l0 / 1000:.3f}\ \text{{m}}}}{{{d1 / 1000:.4f}\ \text{{s}}}}", r"=",
                      rf"{h['speed_lo']:.0f}\ \text{{m/s}}", font_size=44)
        eq2 = MathTex(r"v", r"=", rf"\frac{{{l1 / 1000:.3f}\ \text{{m}}}}{{{d0 / 1000:.4f}\ \text{{s}}}}", r"=",
                      rf"{h['speed_hi']:.0f}\ \text{{m/s}}", font_size=44)
        eqs = VGroup(eq0, eq1, eq2).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        left = VGroup(given, eqs).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([-3.9, -0.1, 0])
        for e in (eq1, eq2):
            e[-1].set_color(NERVE)
        # the comparison, as bars on a common scale
        unit = 5.6 / h["sound"]
        base = np.array([0.6, 0.9, 0])
        nerve_bar = Rectangle(width=(h["speed_hi"] - h["speed_lo"]) * unit, height=0.5, stroke_width=0,
                              fill_color=NERVE, fill_opacity=0.9)
        nerve_bar.move_to(base + RIGHT * ((h["speed_lo"] + h["speed_hi"]) / 2 * unit))
        sound_bar = Rectangle(width=h["sound"] * unit, height=0.5, stroke_width=0, fill_color=GREY_B,
                              fill_opacity=0.8)
        sound_bar.move_to(base + DOWN * 1.3 + RIGHT * h["sound"] * unit / 2)
        zero = Line(base + UP * 0.6, base + DOWN * 1.9, color=GREY_C, stroke_width=2)
        n_lab = label(rf"a frog's nerve: \ {h['speed_lo']:.0f} to {h['speed_hi']:.0f} m/s", font_size=30,
                      color=NERVE).next_to(nerve_bar, UP, buff=0.15).align_to(zero, LEFT).shift(RIGHT * 0.15)
        s_lab = label(rf"sound in air: \ {h['sound']:.0f} m/s", font_size=30, color=GREY_A)
        s_lab.next_to(sound_bar, UP, buff=0.15).align_to(zero, LEFT).shift(RIGHT * 0.15)
        car = label(rf"{h['speed_lo'] * 3.6:.0f} to {h['speed_hi'] * 3.6:.0f} km/h: \ a car on a motorway",
                    font_size=28, color=NERVE).next_to(sound_bar, DOWN, buff=0.5).align_to(zero, LEFT)
        src = historical_tag(archive.HELMHOLTZ_1850.cite)
        with self.voiceover(
            f"The delay was tiny: between {d0:.1f} and {d1:.0f} thousandths of a second. <bookmark mark='a'/> But "
            "divide the extra distance by the extra time, and you have a speed. <bookmark mark='b'/> Fifty "
            f"millimetres in two thousandths of a second is {h['speed_lo']:.0f} metres a second. "
            f"<bookmark mark='c'/> Sixty millimetres in one point four thousandths is {h['speed_hi']:.0f}. "
            "<bookmark mark='d'/> That isn't the speed of light. It isn't even the speed of sound. In a cold "
            "frog, a nerve signal travels about as fast as a car on a motorway. <bookmark mark='e'/> So a "
            "message in the nervous system is a physical event. It takes time, and the time can be measured. "
            "That's the first crack in Kant's first objection."
        ) as vo:
            self.play(FadeIn(head), FadeIn(given), FadeIn(src))
            vo.wait_until("a")
            self.play(Write(eq0))
            vo.wait_until("b")
            self.play(FadeIn(eq1, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(eq2, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(Create(zero), GrowFromEdge(nerve_bar, LEFT), FadeIn(n_lab))
            self.play(GrowFromEdge(sound_bar, LEFT), FadeIn(s_lab), run_time=1.5)
            self.play(FadeIn(car))
            vo.wait_until("e")
            self.play(Indicate(VGroup(eq1[-1], eq2[-1]), color=P.ACCENT, scale_factor=1.15))
        self.clear_scene()

    def people(self):
        h = load("helmholtz")
        head = heading(r"The same measurement, in people")
        A = axes([1848, 1872], [0, 80], x_length=8.6, y_length=4.2, xlabel=r"year", ylabel=r"speed (m/s)",
                 xticks=[1850, 1855, 1860, 1865, 1870], yticks=[0, 20, 40, 60, 80], center=[-2.3, -0.5, 0])
        ax = A.ax
        first = Circle(radius=0.11, stroke_color=P.ARCHIVE, stroke_width=3).move_to(ax.c2p(1850.9, h["human_1850"]))
        f_lab = label(r"Helmholtz, 1850: \ about 60", font_size=26, color=P.ARCHIVE).next_to(first, RIGHT, buff=0.15)
        dots, labs = VGroup(), VGroup()
        names = {"Hirsch": r"Hirsch: \ 34", "Donders and de Jaager": r"Donders and de Jaager: \ 26",
                 "Helmholtz and Baxt": r"Helmholtz and Baxt: \ 34",
                 "Helmholtz and Baxt, midsummer": r"\dots\ in midsummer: \ 65"}
        for r in h["later"]:
            d = Dot(ax.c2p(r["year"], r["speed"]), radius=0.1, color=STATUS_COLOR["replicated"])
            dots.add(d)
            side = UP if r["year"] in (1869, 1862) else DOWN
            labs.add(label(names[r["who"]], font_size=24, color=WHITE).next_to(d, side, buff=0.12))
        labs[2].next_to(dots[2], UP, buff=0.12).align_to(dots[2], LEFT)
        labs[0].next_to(dots[0], UP, buff=0.12).align_to(dots[0], RIGHT)
        half = DashedLine(ax.c2p(1848, 30), ax.c2p(1872, 30), color=GREY_C, stroke_width=2)
        note_ = wrapped_label(r"Helmholtz suspects he has dropped a factor of two.", 3.7, 28, GREY_A)
        temp = wrapped_label(r"The speed of a nerve rises with its temperature.", 3.7, 30, P.ACCENT)
        side_ = VGroup(note_, temp).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([4.95, 0.0, 0])
        chip = status_chip("replicated", 24).next_to(side_, DOWN, buff=0.6).align_to(side_, LEFT)
        src = historical_tag(r"Schmidgen (2002), \emph{Endeavour} 26")
        with self.voiceover(
            "Helmholtz went straight on to people. He gave a mild electric shock to the skin, at the toe or "
            "higher up the leg, and asked the person to move a hand as soon as they felt it. A shock at the toe "
            "took longer to answer, and from the difference he worked out about sixty metres a second in human "
            "nerves. <bookmark mark='a'/> And here's a part the textbooks leave out. Over the next fifteen years "
            "other laboratories repeated the measurement, and kept getting about half that. Thirty-four. "
            "Twenty-six. <bookmark mark='b'/> Helmholtz began to suspect that he'd dropped a factor of two "
            "somewhere in his own calculation. He measured again, and got thirty-four himself. "
            "<bookmark mark='c'/> And then, in the summer of 1869, sixty-five. <bookmark mark='d'/> The speed "
            "of a nerve depends on its temperature. <bookmark mark='e'/> So psychology's very first measurement "
            "came with its first replication dispute. And the dispute ended the way the good ones do: by "
            "finding the variable that nobody had controlled."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(src))
            self.play(Create(first), FadeIn(f_lab))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(d), FadeIn(t)) for d, t in
                                    zip(dots[:2], labs[:2])], lag_ratio=0.6), Create(half), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(note_))
            self.play(GrowFromCenter(dots[2]), FadeIn(labs[2]))
            vo.wait_until("c")
            self.play(GrowFromCenter(dots[3]), FadeIn(labs[3]))
            vo.wait_until("d")
            self.play(FadeIn(temp, shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(chip))
        self.clear_scene()

    def residue(self):
        h = load("helmholtz")
        bar = stage_bar([(r"nerve, inward", 30, NERVE), (r"the brain", h["brain_time_ms"], KANT),
                         (r"nerve and muscle, outward", 45, NERVE)], unit=0.062, height=1.2, font_size=30,
                        show_ms=False)
        bar.move_to([0, 0.5, 0])
        q = MathTex(r"?", font_size=96, color=WHITE).move_to(bar.cells[1])
        tenth = label(r"about a tenth of a second, \ for ``perceiving and willing''", font_size=38, color=KANT)
        tenth.next_to(bar, DOWN, buff=0.7)
        head = heading(r"One reaction, from shock to movement")
        sch = schematic_tag(DR)
        src = historical_tag(r"Helmholtz (1850), in Schmidgen (2002)")
        with self.voiceover(
            "The experiments on people left something behind. <bookmark mark='a'/> Take one reaction, from the "
            "shock on the skin to the movement of the hand. Subtract the time the signal spends travelling in "
            "along the nerve, and the time for the command to travel out. <bookmark mark='b'/> Helmholtz was "
            "left with about a tenth of a second that the brain itself was taking, for what he called the "
            "processes of perceiving and willing. <bookmark mark='c'/> A tenth of a second is a long time. "
            "At sixty metres a second a signal could cross the whole body three times over. So what is the "
            "brain doing with it?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(sch), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowFromEdge(bar.cells[0], LEFT), FadeIn(bar.names[0]))
            self.play(FadeIn(bar.cells[1]), GrowFromEdge(bar.cells[2], LEFT), FadeIn(bar.names[2]))
            vo.wait_until("b")
            self.play(FadeIn(bar.names[1]), FadeIn(tenth, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(q, scale=1.4))
        self.clear_scene()
