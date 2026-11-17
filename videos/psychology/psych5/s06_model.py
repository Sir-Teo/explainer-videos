from __future__ import annotations

import numpy as np

from videos.psychology.psych5.common import *  # noqa: F403


class Model(VoiceoverScene):
    def construct(self):
        self.card()
        self.particles()
        self.three_gates()
        self.equations()

    def card(self):
        card = chapter_card(5, r"Four equations", r"What is the least that will describe those three curves?",
                            lit={1952: r"Hodgkin and Huxley's model"}, part=PART, scale=("molecule", "neuron"),
                            marr=("how",))
        with self.voiceover(
            "Chapter five. Four equations."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def particles(self):
        d = load("clamp")
        head = heading(r"Why the potassium curve starts late")
        t = np.asarray(d["t"])
        gk = np.asarray(d["g_k_0"])
        n = (gk / 36.0) ** 0.25
        A = axes([0, 8], [0, 1.05], x_length=6.2, y_length=3.8, xticks=[0, 2, 4, 6, 8], yticks=[0, 0.5, 1.0],
                 xlabel=r"time after the step (ms)", ylabel=r"fraction", center=[-3.2, -0.5, 0])
        ax = A.ax
        one = curve(ax, t, n, GATE["n"], stroke_width=3)
        four = curve(ax, t, n ** 4, K, stroke_width=4)
        one_l = label(r"one exponential process: \ no delay", font_size=24, color=GATE["n"]).move_to(ax.c2p(5.2, 0.97))
        four_l = label(r"the potassium conductance", font_size=24, color=K).move_to(ax.c2p(5.9, 0.5))
        four_l2 = label(r"$n^4$: \ all four in place", font_size=24, color=K).move_to(ax.c2p(5.9, 0.5))
        one_l2 = label(r"$n$: \ one particle in place", font_size=24, color=GATE["n"]).move_to(ax.c2p(5.2, 0.97))
        gate = VGroup(*[Circle(radius=0.2, color=GATE["n"], stroke_width=3) for _ in range(4)]).arrange(RIGHT, buff=0.2)
        fills = VGroup(*[Circle(radius=0.2, stroke_width=0, fill_color=GATE["n"], fill_opacity=1).move_to(c_) for c_ in gate])
        gate_g = VGroup(gate, fills).move_to([3.9, 1.7, 0])
        gate_l = label(r"a potassium channel: \ open only if all four are in place", font_size=24, color=GREY_A)
        gate_l.next_to(gate_g, DOWN, buff=0.2)
        eqs = VGroup(
            MathTex(r"g_K \;=\; \bar g_K\, n^4", font_size=44),
            MathTex(r"\frac{dn}{dt} \;=\; \alpha_n(V)\,(1 - n) \;-\; \beta_n(V)\, n", font_size=38),
            wrapped_label(r"$\alpha$: \ the rate of moving into place; \ $\beta$: \ the rate of leaving. \ Both "
                          r"depend on the voltage, and were read off the clamp records.", 5.4, 25, WHITE),
        ).arrange(DOWN, buff=0.3).next_to(gate_l, DOWN, buff=0.45)
        keep_in_frame(VGroup(gate_g, gate_l, eqs))
        tag = psyche_tag()
        with self.voiceover(
            "Now the modelling, and watch how little they allowed themselves. Start with potassium. Its "
            "conductance rises along an S-shaped curve: nothing at first, then quickly, then levelling off. "
            "<bookmark mark='a'/> The simplest process that turns on is one that relaxes exponentially, like "
            "the charging curve of chapter three. But an exponential rises fastest at the very start. It has "
            "no delay. <bookmark mark='b'/> So Hodgkin and Huxley supposed that a potassium door opens only "
            "when several independent things have all happened. Imagine four particles, each of which has to "
            "move into place, each on its own exponential schedule. If the chance that one is in place is n, "
            "the chance that all four are is n to the fourth power. <bookmark mark='c'/> And n to the fourth "
            "starts flat. Raising to a power buys the delay, and the fourth power was enough to fit. "
            "<bookmark mark='d'/> So potassium needs one variable, n, with one equation: it moves toward "
            "open at a rate alpha and back at a rate beta, and both rates depend on the voltage. They "
            "measured those rates at each voltage from the clamp, and fitted smooth curves through them. They "
            "didn't know what the particles were, and they said so. It was more than forty years before the "
            "structure of a potassium channel was seen. It's built of four matching parts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            self.play(Create(four), FadeIn(four_l), run_time=5.0, rate_func=linear)
            vo.wait_until("a")
            self.play(Create(one), FadeIn(one_l), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(gate), FadeIn(gate_l))
            self.play(LaggedStart(*[FadeIn(f_) for f_ in fills], lag_ratio=0.6), run_time=3.0)
            vo.wait_until("c")
            self.play(ReplacementTransform(four_l, four_l2), ReplacementTransform(one_l, one_l2),
                      Indicate(four, color=WHITE, scale_factor=1.02), run_time=1.5)
            vo.wait_until("d")
            self.play(Write(eqs[0]))
            self.play(Write(eqs[1]), FadeIn(eqs[2]), run_time=2.0)
        self.clear_scene()

    def three_gates(self):
        d = load("gates")
        r = d["rest"]
        head = heading(r"Three gates: \ where each wants to be, and how fast it gets there")
        v = np.asarray(d["v"])
        A1 = axes([-100, 50], [0, 1.05], x_length=5.6, y_length=3.4, xticks=[-100, -50, 0, 50], yticks=[0, 0.5, 1.0],
                  xlabel=r"membrane potential (mV)", ylabel=r"steady value", center=[-3.5, -0.45, 0], font_size=20)
        A2 = axes([-100, 50], [0, 9.5], x_length=5.6, y_length=3.4, xticks=[-100, -50, 0, 50], yticks=[0, 2, 4, 6, 8],
                  xlabel=r"membrane potential (mV)", ylabel=r"time constant (ms)", center=[3.6, -0.45, 0], font_size=20)
        inf = {k: curve(A1.ax, v, d[k], GATE[k], stroke_width=4) for k in "mhn"}
        tau = {k: curve(A2.ax, v, d["tau_" + k], GATE[k], stroke_width=4) for k in "mhn"}
        names = {"m": r"$m$: \ sodium on", "h": r"$h$: \ sodium still available", "n": r"$n$: \ potassium on"}
        leg = VGroup(*[label(names[k], font_size=26, color=GATE[k]) for k in "mhn"]).arrange(RIGHT, buff=0.7)
        leg.next_to(VGroup(A1, A2), UP, buff=0.3)
        rest_line = VGroup(*[DashedLine(a.ax.c2p(-65, 0), a.ax.c2p(-65, top), color=GREY_B, stroke_width=2)
                             for a, top in ((A1, 1.05), (A2, 9.5))])
        rest_l = label(r"rest", font_size=20, color=GREY_B).next_to(rest_line[0], UP, buff=0.03)
        end = wrapped_label(rf"$m$ answers in {r['tau_m']:.1f} ms. \ $h$ and $n$ take {r['tau_n']:.0f} to "
                            rf"{r['tau_h']:.0f} ms. \ The whole signal lives in that difference.", 9.6, 26, P.ACCENT)
        end.to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        tag = psyche_tag()
        with self.voiceover(
            "Sodium needs two variables, because it does two things: it turns on, and then it turns off. "
            "<bookmark mark='a'/> Call them m and h. m is the turning on, and it behaves like n: low at rest, "
            "rising as the membrane is made more positive. <bookmark mark='b'/> h is the opposite. It's high "
            "at rest and falls when the membrane is made positive. Think of it as a second door on the same "
            "channel, which closes when the first one opens. The sodium conductance is m cubed times h: three "
            "particles to open, one to stay available. <bookmark mark='c'/> And potassium's n, rising. So at "
            "rest, on the dashed line, sodium's first door is nearly shut, its second door is mostly open, "
            "and potassium is slightly on. <bookmark mark='d'/> Now the right-hand picture, which is the "
            "important one. This is how quickly each gate moves. m is at the bottom: it responds within a "
            "fraction of a millisecond, everywhere. h and n are tens of times slower. "
            "<bookmark mark='e'/> So when the voltage rises, sodium turns on at once, and only later does "
            "sodium shut and potassium open. A fast process that pushes the voltage up, followed by two "
            "slow ones that bring it down. You can already see the shape of the signal in these curves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A1), FadeIn(A2), Create(rest_line), FadeIn(rest_l))
            vo.wait_until("a")
            self.play(Create(inf["m"]), FadeIn(leg[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(inf["h"]), FadeIn(leg[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(inf["n"]), FadeIn(leg[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(tau[k]) for k in "mhn"], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def equations(self):
        d = archive.HODGKIN_HUXLEY_1952.data
        head = heading(r"The model, whole")
        eq1 = MathTex(r"C\,\frac{dV}{dt}", r"\;=\;", r"I", r"\;-\;", r"\bar g_{Na}\, m^3 h\,(V - E_{Na})", r"\;-\;",
                      r"\bar g_K\, n^4\,(V - E_K)", r"\;-\;", r"g_L\,(V - E_L)", font_size=40)
        eq1[4].set_color(NA)
        eq1[6].set_color(K)
        eq1[8].set_color(LEAK)
        gates = VGroup(*[MathTex(rf"\frac{{d{x}}}{{dt}} \;=\; \alpha_{x}(V)\,(1 - {x}) \;-\; \beta_{x}(V)\,{x}",
                                 font_size=38, color=GATE[x]) for x in "mhn"]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        eq1.move_to([0, 1.95, 0])
        if eq1.width > 12.6:
            eq1.width = 12.6
        gates.move_to([-3.4, -0.55, 0])
        top, bot = eq1.get_top()[1] + 0.25, eq1.get_bottom()[1] - 0.25
        names = VGroup(*[label(t, font_size=22, color=c).move_to([eq1[i].get_center()[0], y, 0])
                         for t, c, i, y in ((r"sodium", NA, 4, top), (r"potassium", K, 6, top), (r"leak", LEAK, 8, top),
                                            (r"the capacitor", GREY_A, 0, top), (r"what you inject", GREY_A, 2, bot))])
        facts = VGroup(
            wrapped_label(rf"three conductances ({d['g_na']:.0f}, {d['g_k']:.0f} and {d['g_l']} mS/cm$^2$), three "
                          r"batteries, six rate curves", 5.8, 27, WHITE),
            wrapped_label(r"all of it fitted to the clamp, where the voltage was held still", 5.8, 27, DATA),
            wrapped_label(r"none of it fitted to a nerve signal", 5.8, 29, MODEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.5, -0.55, 0])
        code = code_block([r"hh = neuron.HH() \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \# the 1952 membrane",
                           r"r = hh.pulse(2 * hh.threshold()) \ \ \# stimulate it; r['v'] is the voltage"],
                          font_size=24).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Put it together. <bookmark mark='a'/> The top line is the circuit of chapter three with two "
            "branches added. The capacitor charges at a rate set by whatever current is left over after "
            "sodium, potassium and a small fixed leak have each taken theirs. Each current is a conductance "
            "times the distance from that ion's battery. <bookmark mark='b'/> Underneath, three small "
            "equations, one for each gate, all of the same form. That's four equations. "
            "<bookmark mark='c'/> And here is the point that makes it a test. Every number in these equations "
            "was measured with the voltage clamped still. <bookmark mark='d'/> Nobody had adjusted anything "
            "to make a nerve signal come out. They'd measured the parts. Whether the parts, put together and "
            "let go, would produce the signal that the squid produces was a real question, and the equations "
            "could have given the wrong answer. <bookmark mark='e'/> In Psyche's library the whole model is "
            "these two lines. Let's let it go."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq1), run_time=3.0)
            self.play(FadeIn(names, lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Write(g_) for g_ in gates], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(facts[0]), FadeIn(facts[1]))
            vo.wait_until("d")
            self.play(FadeIn(facts[2], scale=1.1))
            vo.wait_until("e")
            self.play(FadeIn(code, shift=UP * 0.15))
        self.clear_scene()
