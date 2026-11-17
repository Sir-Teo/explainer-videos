from __future__ import annotations

import numpy as np

from videos.psychology.psych6.common import *  # noqa: F403


def beating(h, origin, width=4.4, span=9.0, amp=0.5, rate=1.3):
    """Make the heart ``h`` beat at ``h.rate`` beats a second and return the trace it writes (newest at the right)."""
    h.rate, h.phase, h.clock, h.hist = rate, 0.0, 0.0, []
    base = h.height
    origin = np.asarray(origin, float)
    tr = VMobject(color=h.get_color(), stroke_width=3)

    def step(m, dt):
        m.clock += dt
        m.phase += dt * m.rate
        pulse = float(np.exp(-(((m.phase % 1.0) - 0.2) / 0.08) ** 2))
        m.scale_to_fit_height(base * (1 + 0.12 * pulse))
        m.hist.append((m.clock, pulse))
        m.hist = [p for p in m.hist if p[0] > m.clock - span]
        if len(m.hist) > 1:
            tr.set_points_as_corners(
                [origin + np.array([width * (1 - (m.clock - t) / span), amp * v, 0]) for t, v in m.hist])

    h.add_updater(step)
    return tr


class Hook(VoiceoverScene):
    def construct(self):
        self.question()
        self.two_hearts()
        self.adjustable()
        self.objectives()

    def question(self):
        head = heading(r"The signal reaches the end of the axon. \ Then what?")
        ya = 1.45
        axon = Line([-6.4, ya, 0], [-1.25, ya, 0], color=VOLT, stroke_width=9)
        bulb = Circle(radius=0.6, color=VOLT, stroke_width=4, fill_color="#111722", fill_opacity=1).move_to(
            [-0.7, ya, 0])
        nxt = RoundedRectangle(width=5.2, height=2.0, corner_radius=0.6, color=VOLT, stroke_width=4,
                               fill_color="#111722", fill_opacity=1).move_to([3.3, ya, 0])
        nxt_l = label(r"the next cell", font_size=30, color=GREY_A).move_to(nxt)
        axon_l = label(r"an axon", font_size=30, color=GREY_A).next_to(axon, UP, buff=0.2)
        gap = DoubleArrow([-0.1, ya - 0.85, 0], [0.7, ya - 0.85, 0], color=THRESH, stroke_width=4, buff=0,
                          tip_length=0.16)
        gap_l = label(r"a gap", font_size=30, color=THRESH).next_to(gap, DOWN, buff=0.1)
        pulse = Dot([-6.4, ya, 0], radius=0.16, color=THRESH)
        camps = VGroup(
            VGroup(label(r"the sparks", font_size=34, color=DATA),
                   wrapped_label(r"the current jumps across. \ It is fast, and nerves are electrical", 5.6, 29,
                                 WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"the soups", font_size=34, color=EXC),
                   wrapped_label(r"the ending releases a chemical, \ and the chemical acts on the other side", 5.6,
                                 29, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, -1.15, 0])
        slip = VGroup(Rectangle(width=2.6, height=1.0, color=GREY_B, stroke_width=2, fill_color="#1A2130",
                                fill_opacity=1))
        xs = np.linspace(-1.05, 1.05, 60)
        g = np.random.default_rng(6)
        slip.add(VMobject(color=GREY_A, stroke_width=2).set_points_smoothly(
            [np.array([x, 0.16 * np.sin(9 * x) + 0.1 * g.standard_normal(), 0]) for x in xs]))
        dream = VGroup(slip, wrapped_label(r"Graz, the night before Easter Sunday, 1921: \ a note he could not "
                                           r"read in the morning", 7.4, 28, GREY_A)).arrange(RIGHT, buff=0.4)
        dream.to_edge(DOWN, buff=0.55)
        tag = note(r"Loewi's own later account").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Part 5 ended with a signal racing down an axon, and stopping at a gap. Ramón y Cajal had shown that "
            "neurons are separate cells. So at the end of the axon the signal has to get across to the next cell "
            "somehow. For the first half of the twentieth century physiologists split into two camps over how, "
            "and they had names for each other. <bookmark mark='a'/> The sparks held that the electric current "
            "simply jumps the gap. It's fast, and nerve signals are electrical after all. <bookmark mark='b'/> "
            "The soups held that the nerve ending releases a chemical, and the chemical does the work on the "
            "other side. <bookmark mark='c'/> In 1921 the question got its first clean answer, and by the "
            "account of the man who gave it, the experiment came to him in his sleep. Otto Loewi, a "
            "pharmacologist in Graz, said that on the night before Easter Sunday he woke, scribbled an idea on "
            "a slip of paper, and fell asleep again. In the morning he couldn't read his own writing. The next "
            "night, at three o'clock, the idea came back, and this time he got up and went straight to the "
            "laboratory. That's his own telling, years afterwards, and historians aren't sure how much of it "
            "to believe. The experiment, though, is in the journal."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(axon, axon_l, bulb, nxt, nxt_l)))
            self.play(pulse.animate.move_to([-1.3, ya, 0]), run_time=2.0, rate_func=linear)
            self.play(FadeOut(pulse, scale=2.0), FadeIn(gap), FadeIn(gap_l))
            vo.wait_until("a")
            self.play(FadeIn(camps[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(camps[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(dream, shift=UP * 0.1), FadeIn(tag))
        self.clear_scene()

    def _vessel(self, x, y, w=2.4, h=2.3):
        pts = [[x - w / 2, y + h / 2, 0], [x - w / 2, y - h / 2, 0], [x + w / 2, y - h / 2, 0],
               [x + w / 2, y + h / 2, 0]]
        glass = VMobject(color=GREY_B, stroke_width=3).set_points_as_corners(pts)
        fluid = Rectangle(width=w - 0.06, height=h * 0.78, stroke_width=0, fill_color=INH, fill_opacity=0.16)
        fluid.move_to([x, y - h * 0.11, 0])
        return VGroup(fluid, glass)

    def two_hearts(self):
        head = heading(r"Two frog hearts, \ and one transfer of fluid")
        xa, xb, y = -3.6, 3.6, 0.9
        va, vb = self._vessel(xa, y), self._vessel(xb, y)
        ha, hb = heart(1.15, EXC).move_to([xa, y - 0.2, 0]), heart(1.15, DATA).move_to([xb, y - 0.2, 0])
        la = label(r"heart 1, \ with its vagus nerve", font_size=27, color=EXC).next_to(va, UP, buff=0.2)
        lb = label(r"heart 2, \ no nerve", font_size=27, color=DATA).next_to(vb, UP, buff=0.2)
        nerve = Line([xa - 2.5, y + 0.9, 0], [xa - 0.35, y + 0.0, 0], color=THRESH, stroke_width=5)
        stim = label(r"stimulate", font_size=24, color=THRESH).next_to(nerve.get_start(), UP, buff=0.1)
        ta = beating(ha, [xa - 2.2, -1.4, 0])
        tb = beating(hb, [xb - 2.2, -1.4, 0])
        base = VGroup(Line([xa - 2.2, -1.45, 0], [xa + 2.2, -1.45, 0], color=GREY_D, stroke_width=2),
                      Line([xb - 2.2, -1.45, 0], [xb + 2.2, -1.45, 0], color=GREY_D, stroke_width=2))
        tl = VGroup(label(r"its beats", font_size=22, color=GREY_B).next_to(base[0], DOWN, buff=0.1),
                    label(r"its beats", font_size=22, color=GREY_B).next_to(base[1], DOWN, buff=0.1))
        drops = VGroup(*[Dot([xa + 0.5 + 0.12 * i, y - 0.7, 0], radius=0.07, color=INH) for i in range(4)])
        path = Line([xa + 0.7, y - 0.7, 0], [xb - 0.7, y - 0.7, 0])
        arrow = Arrow([xa + 1.5, y + 0.2, 0], [xb - 1.5, y + 0.2, 0], color=INH, stroke_width=5, buff=0,
                      max_tip_length_to_length_ratio=0.06)
        arrow_l = label(r"fluid only", font_size=28, color=INH).next_to(arrow, UP, buff=0.12)
        end = wrapped_label(r"Nothing electrical joins the hearts. \ The nerve released a substance: \ "
                            r"\emph{Vagusstoff}, later identified as acetylcholine.", 12.6, 29, P.ACCENT)
        end.move_to([0, -2.75, 0])
        src = historical_tag(archive.LOEWI_1921.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Here it is. Two frog hearts, removed from the animals and kept beating in salt solution, each in "
            "its own vessel. <bookmark mark='a'/> The first still has its vagus nerve attached, the nerve that "
            "slows the heart. The second has no nerve at all. <bookmark mark='b'/> Loewi stimulates the nerve "
            "of the first heart, and it slows, as everyone knew it would. <bookmark mark='c'/> Then he takes "
            "some of the fluid that has been bathing the first heart and transfers it to the second. "
            "<bookmark mark='d'/> And the second heart slows too. Nothing electrical connects the two. Only "
            "the fluid crossed. <bookmark mark='e'/> So the nerve must have released a substance into it, and "
            "the substance is what tells a heart to slow. Loewi called it Vagusstoff: vagus stuff. It was "
            "later identified as acetylcholine, and in 1936 he shared a Nobel Prize for it with Henry Dale, "
            "who showed the same chemical at work where nerves meet muscles."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(VGroup(va, vb, ha, hb, base, tl)))
            self.add(ta, tb)
            vo.wait_until("a")
            self.play(Create(nerve), FadeIn(la), FadeIn(lb))
            vo.wait_until("b")
            self.play(FadeIn(stim), Indicate(nerve, color=WHITE, scale_factor=1.0), run_time=1.0)
            ha.rate = 0.5
            vo.wait_until("c")
            self.play(FadeIn(drops), GrowArrow(arrow), FadeIn(arrow_l))
            self.play(MoveAlongPath(drops, path), run_time=2.0)
            self.play(drops.animate.move_to([xb + 0.6, y - 0.7, 0]), run_time=0.8)
            vo.wait_until("d")
            hb.rate = 0.5
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def adjustable(self):
        head = heading(r"Why it matters which camp was right")
        # a wire on the left, a dial on the right
        wl = VGroup(unit("A"), unit("B")).arrange(RIGHT, buff=2.2).move_to([-3.6, 1.3, 0])
        wire = Line(wl[0].get_right(), wl[1].get_left(), color=DATA, stroke_width=6)
        w_txt = VGroup(label(r"a wire", font_size=32, color=DATA),
                       wrapped_label(r"the signal crosses or it does not: \ nothing to adjust", 5.2, 27,
                                     WHITE)).arrange(DOWN, buff=0.12).next_to(VGroup(wl, wire), DOWN, buff=0.4)
        cl = VGroup(unit("A"), unit("B")).arrange(RIGHT, buff=2.2).move_to([3.6, 1.3, 0])
        conn = excite(cl[0].get_right(), cl[1].get_left(), buff=0.05)
        w = ValueTracker(0.35)
        dial_c = conn.get_center() + UP * 0.75
        dial = VGroup(Arc(radius=0.42, start_angle=PI, angle=-PI, color=GREY_B, stroke_width=3).move_arc_center_to(
            dial_c))
        needle = always_redraw(lambda: Line(dial_c, dial_c + 0.4 * np.array(
            [-np.cos(PI * w.get_value()), np.sin(PI * w.get_value()), 0]), color=RULE, stroke_width=5))
        w_l = label(r"strength $w$", font_size=24, color=RULE).next_to(dial, UP, buff=0.08)
        c_txt = VGroup(label(r"a chemical step", font_size=32, color=EXC),
                       wrapped_label(r"how much is released, \ how many receptors wait, \ how fast it is cleared: "
                                     r"\ quantities, and quantities can change", 5.6, 27, WHITE)).arrange(
            DOWN, buff=0.12).next_to(VGroup(cl, conn), DOWN, buff=0.4)
        c_txt.align_to(w_txt, UP)
        lines = VGroup(
            label(r"a strength that can change can store what happened: \ learning and memory", font_size=30,
                  color=RULE),
            label(r"and it is where every drug that alters the mind does its work", font_size=30, color=P.ACCENT),
            label(r"the sparks' leader, John Eccles, gave up in 1951, \ on his own experiment", font_size=26,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Why does it matter which camp was right? <bookmark mark='a'/> If a connection between two neurons "
            "were a wire, there'd be nothing to adjust. The signal crosses, or it doesn't. <bookmark mark='b'/> "
            "A chemical step is different. How much is released. How many receptors are waiting for it. How "
            "quickly it's cleared away. Every one of those is a quantity, and quantities can change. So a "
            "chemical synapse has a strength. <bookmark mark='c'/> And a strength that can change is something "
            "that can store what has happened. That's the idea of this part. If learning and memory are "
            "anywhere in the machine, they're in the adjustment of these strengths. <bookmark mark='d'/> It's "
            "also where nearly every drug that alters the mind does its work, as we'll see. <bookmark mark='e'/> "
            "A footnote on the sparks. Their leader, John Eccles, held out until 1951, when an experiment in "
            "his own laboratory came out against his own theory, and he gave it up. And it turned out later "
            "that a minority of synapses really are electrical. So both camps were partly right, again. But "
            "most of the synapses in your brain are chemical, and those are the ones we'll build with."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(wl), Create(wire), FadeIn(w_txt))
            vo.wait_until("b")
            self.play(FadeIn(cl), GrowArrow(conn), FadeIn(dial), FadeIn(needle), FadeIn(w_l), FadeIn(c_txt))
            self.play(w.animate.set_value(0.8), run_time=1.5)
            self.play(w.animate.set_value(0.2), run_time=1.5)
            self.play(w.animate.set_value(0.6), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(lines[0], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(lines[1], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(lines[2], shift=UP * 0.1))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 6", font_size=34, color=GREY_B), label(r"Synapses and Circuits", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the chemical synapse, step by step, \ and the packets it releases",
            r"the transmitters, \ and the places a drug can act",
            r"how a neuron adds up its inputs, \ and how inhibition divides",
            r"Hebb's rule for learning: \ its flaw, the repair, \ and the synapse that obeys it",
            r"three small circuits: \ one sharpens edges, one holds a choice, one keeps time",
            r"populations and their rhythms, \ and the brain's volume knobs",
        ], color=P.ACCENT, font_size=32, width=13.2)
        with self.voiceover(
            "Part six: synapses and circuits. <bookmark mark='a'/> We'll take the chemical synapse apart, step "
            "by step, and find that it releases its transmitter in packets. <bookmark mark='b'/> We'll meet "
            "the transmitters, and the handful of places where a drug can interfere. <bookmark mark='c'/> "
            "We'll compute how a neuron adds up its inputs, and find a kind of inhibition that divides instead "
            "of subtracting. <bookmark mark='d'/> Then learning. Hebb's rule, why it can't work as stated, "
            "what repairs it, and the synapse that was found doing it. <bookmark mark='e'/> Then we wire "
            "neurons together, into three small circuits. One sharpens edges, and we'll test it on your own "
            "eyes. One holds a decision. One keeps time. <bookmark mark='f'/> And we'll finish with whole "
            "populations of neurons, the rhythms they fall into, and the chemicals that turn the whole thing "
            "up and down."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark_, r in zip("bcdef", obj.rows[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
