from __future__ import annotations

import numpy as np

from videos.psychology.psych6.common import *  # noqa: F403

MG = "#5BD18B"


class Remember(VoiceoverScene):
    def construct(self):
        self.card()
        self.ltp()
        self.nmda()
        self.timing()
        self.bcm()
        self.aplysia()

    def card(self):
        card = chapter_card(5, r"A synapse that remembers", r"Do real synapses follow Hebb's rule?",
                            lit={1973: r"long-term potentiation"}, part=PART, scale=("molecule", "neuron"),
                            marr=("how", "tissue"))
        with self.voiceover(
            "Chapter five. A synapse that remembers."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def ltp(self):
        head = heading(r"1973: \ a synapse is changed by use, and stays changed")
        # the preparation, drawn
        fibres = VGroup(*[Line([-6.3, 0.9 - 0.35 * i, 0], [-3.5, 0.35 - 0.12 * i, 0], color=EXC, stroke_width=4)
                          for i in range(3)])
        cells = VGroup(*[unit("", 0.26, VOLT).move_to([-3.1, 0.75 - 0.6 * i, 0]) for i in range(4)])
        stim = VGroup(Line([-5.9, 2.0, 0], [-5.6, 0.8, 0], color=THRESH, stroke_width=4),
                      label(r"stimulate", font_size=24, color=THRESH).move_to([-5.9, 2.25, 0]))
        rec = VGroup(Line([-2.0, 2.0, 0], [-2.85, 0.3, 0], color=GREY_A, stroke_width=3),
                     label(r"record", font_size=24, color=GREY_A).move_to([-2.0, 2.25, 0]))
        names = VGroup(label(r"perforant path", font_size=24, color=EXC).next_to(fibres, DOWN, buff=0.75).shift(
            LEFT * 0.4), label(r"dentate gyrus", font_size=24, color=VOLT).next_to(cells, DOWN, buff=0.2))
        where = label(r"the hippocampus of an anaesthetized rabbit", font_size=24, color=GREY_B).move_to(
            [-4.3, -2.0, 0])
        prep = VGroup(fibres, cells, stim, rec, names, where)
        A = axes([-10, 30], [0, 2.2], x_length=6.2, y_length=3.8, xticks=[], yticks=[], xlabel=r"time",
                 ylabel=r"response to one test pulse", center=[3.4, -0.2, 0])
        ax = A.ax
        g = np.random.default_rng(73)
        before = VGroup(*[Dot(ax.c2p(t, 1.0 + 0.04 * g.standard_normal()), radius=0.06, color=GREY_A)
                          for t in np.arange(-9, 0, 1.0)])
        after = VGroup(*[Dot(ax.c2p(t, 1.62 - 0.004 * t + 0.05 * g.standard_normal()), radius=0.06, color=EXC)
                         for t in np.arange(1, 30, 1.0)])
        base = DashedLine(ax.c2p(-10, 1.0), ax.c2p(30, 1.0), color=GREY_D, stroke_width=2)
        burst = VGroup(Line(ax.c2p(0, 0), ax.c2p(0, 2.1), color=THRESH, stroke_width=5))
        burst.add(label(r"a brief burst of fast stimulation", font_size=22, color=THRESH).next_to(
            ax.c2p(0, 2.1), UR, buff=0.05))
        name = wrapped_label(r"long-term potentiation, \ LTP: \ the response stays enlarged for hours", 12.4, 30,
                             P.ACCENT).to_edge(DOWN, buff=0.85)
        src = published_tag(archive.BLISS_LOMO_1973.cite)
        tag = note(r"schematic: the design, not the paper's data").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Hebb's rule sat for more than twenty years as a guess. Then, in Oslo, Terje Lømo and Tim Bliss "
            "were recording from the hippocampus of anaesthetized rabbits. <bookmark mark='a'/> They "
            "stimulated a bundle of fibres called the perforant path with single test pulses, and recorded how "
            "strongly the cells at the far end, in the dentate gyrus, responded. <bookmark mark='b'/> Pulse "
            "after pulse, the same response. <bookmark mark='c'/> Then they gave a brief burst of fast "
            "stimulation. <bookmark mark='d'/> And afterwards, the response to the very same test pulse was "
            "larger. Not for a moment. It stayed larger, for hours. <bookmark mark='e'/> They called it "
            "long-lasting potentiation, and it's now known as long-term potentiation, LTP. A synapse had been "
            "changed by use, and had held the change. The picture is a sketch of their design. I haven't "
            "drawn their data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag))
            self.play(FadeIn(VGroup(fibres, cells, names, where)))
            vo.wait_until("a")
            self.play(FadeIn(stim), FadeIn(rec), FadeIn(A), Create(base))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in before], lag_ratio=0.5), run_time=3.5)
            vo.wait_until("c")
            self.play(Create(burst[0]), FadeIn(burst[1]), Indicate(fibres, color=WHITE, scale_factor=1.03))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in after], lag_ratio=0.5), run_time=6.0)
            vo.wait_until("e")
            self.play(FadeIn(name, shift=UP * 0.1))
        self.clear_scene()

    def _spine(self, x, y, glu, dep):
        mem = Line([x - 1.6, y, 0], [x + 1.6, y, 0], color=THRESH if dep else GREY_C, stroke_width=7)
        g = VGroup(mem)
        for cx, kind in ((x - 0.8, "ampa"), (x + 0.8, "nmda")):
            gap = 0.3 if glu else 0.06
            hole = Rectangle(width=gap, height=0.3, stroke_width=0, fill_color=BACKGROUND, fill_opacity=1).move_to(
                [cx, y, 0])
            halves = VGroup(*[Rectangle(width=0.36, height=1.0, color=VOLT, stroke_width=3, fill_color="#1A2130",
                                        fill_opacity=1).move_to([cx + s * (0.18 + gap / 2), y, 0]) for s in (-1, 1)])
            g.add(hole, halves, label(r"AMPA" if kind == "ampa" else r"NMDA", font_size=20, color=GREY_B).next_to(
                halves, UP, buff=0.42))
            if glu:
                g.add(VGroup(*[Dot([cx + dx, y + 0.72, 0], radius=0.07, color=EXC) for dx in (-0.14, 0.14)]))
            if kind == "ampa" and glu:
                g.add(Arrow([cx, y + 0.35, 0], [cx, y - 0.95, 0], color=EXC, stroke_width=4, buff=0,
                            max_tip_length_to_length_ratio=0.18))
            if kind == "nmda":
                if dep:
                    plug = Dot([cx + 0.5, y + 0.75, 0], radius=0.12, color=MG)
                    g.add(plug, label(r"Mg$^{2+}$", font_size=18, color=MG).next_to(plug, UP, buff=0.06))
                    if glu:
                        g.add(Arrow([cx, y + 0.35, 0], [cx, y - 0.95, 0], color=DATA, stroke_width=6, buff=0,
                                    max_tip_length_to_length_ratio=0.18),
                              label(r"Ca$^{2+}$", font_size=22, color=DATA).move_to([cx + 0.55, y - 0.8, 0]))
                else:
                    plug = Dot([cx, y + 0.12, 0], radius=0.12, color=MG)
                    g.add(plug, label(r"Mg$^{2+}$ plug", font_size=18, color=MG).move_to([cx, y - 0.75, 0]))
        return g

    def nmda(self):
        head = heading(r"One protein that computes ``both at once''")
        y = 1.25
        cols = [(-4.5, True, False, r"input alone", r"an EPSP through AMPA; \ the NMDA pore is plugged", EXC),
                (0.0, False, True, r"the cell fires alone", r"the plug leaves, \ but nothing opens the channel",
                 THRESH),
                (4.5, True, True, r"both together", r"calcium enters, \ and more AMPA receptors are added", DATA)]
        panels = VGroup()
        for x, glu, dep, name, what, col in cols:
            s = self._spine(x, y, glu, dep).scale(1.3, about_point=[x, y, 0])
            state = label(r"cell depolarized" if dep else r"cell near rest", font_size=24,
                          color=THRESH if dep else GREY_B).move_to([x, y - 1.6, 0])
            txt = VGroup(label(name, font_size=34, color=col), wrapped_label(what, 4.2, 28, WHITE)).arrange(
                DOWN, buff=0.12).move_to([x, y - 2.65, 0])
            panels.add(VGroup(s, state, txt))
        end = label(r"input AND output: \ Hebb's product $x\,y$, in one molecule", font_size=32, color=P.ACCENT)
        end.to_edge(DOWN, buff=0.4)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "How could a synapse know that its own input was active and that its own cell fired, both at "
            "once? The answer turned out to be a single kind of molecule. Most excitatory synapses carry two "
            "kinds of receptor for glutamate. <bookmark mark='a'/> One, the AMPA receptor, is the ordinary "
            "kind. Glutamate binds, the channel opens, and you get an EPSP. The other, the NMDA receptor, is "
            "peculiar. Glutamate opens it too. But near the resting voltage its pore is plugged by a "
            "magnesium ion, held in by the negative charge inside the cell. So input alone gets nothing "
            "through this channel. <bookmark mark='b'/> If the cell is strongly depolarized, because it's "
            "firing, the plug is pushed out. But with no glutamate, the channel is shut anyway. "
            "<bookmark mark='c'/> Only when both happen together, glutamate from the input and a "
            "depolarized cell, is the channel open and clear. And what comes through it is calcium, which "
            "sets off the reactions that put more AMPA receptors into that synapse. <bookmark mark='d'/> "
            "Input and output. A logical AND, computed by one protein. It's Hebb's product, x times y, in "
            "molecular form. And remember the three numbers from chapter one. This changes the third: the "
            "response to one packet."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(FadeIn(panels[0][0]))
            vo.wait_until("a")
            self.play(FadeIn(panels[0][1:], shift=UP * 0.1))
            for k, mark_ in zip((1, 2), "bc"):
                vo.wait_until(mark_)
                self.play(FadeIn(panels[k], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def timing(self):
        p = load("plasticity")
        head = heading(r"The order matters: \ spike timing")
        A = axes([-100, 100], [-0.7, 1.15], x_length=6.8, y_length=4.2, xticks=[-100, -50, 0, 50, 100],
                 yticks=[-0.5, 0, 0.5, 1.0], yfmt=lambda v: f"{v:.1f}",
                 xlabel=r"cell's spike minus input's spike (ms)", ylabel=r"change in the synapse", center=[-3.2, -0.5, 0])
        ax = A.ax
        dt, w = p["dt"], p["stdp"]
        zero = DashedLine(ax.c2p(-100, 0), ax.c2p(100, 0), color=GREY_D, stroke_width=2)
        vert = DashedLine(ax.c2p(0, -0.7), ax.c2p(0, 1.15), color=GREY_D, stroke_width=2)
        pos = trace(ax, dt[dt > 0], w[dt > 0], EXC, 4)
        neg = trace(ax, dt[dt < 0], w[dt < 0], INH, 4)
        win = VGroup(*[DashedLine(ax.c2p(s * p["window"], -0.7), ax.c2p(s * p["window"], 1.15), color=THRESH,
                                  stroke_width=2) for s in (-1, 1)])
        win_l = label(rf"about {p['window']} ms either side", font_size=24, color=THRESH).move_to(ax.c2p(62, 0.8))
        phrase = label(r"``\,\dots takes part in firing it\,\dots''", font_size=34, color=WHITE)
        da, db = unit("", 0.3, EXC), unit("", 0.3, VOLT)
        VGroup(da, db).arrange(RIGHT, buff=1.6)
        dish = VGroup(Ellipse(width=4.6, height=1.7, color=GREY_C, stroke_width=2), da, db,
                      excite(da.get_right(), db.get_left(), buff=0.05),
                      Line(da.get_top() + UP * 0.9 + LEFT * 0.5, da.get_top(), color=GREY_A, stroke_width=3),
                      Line(db.get_top() + UP * 0.9 + RIGHT * 0.5, db.get_top(), color=GREY_A, stroke_width=3))
        dish_l = wrapped_label(r"two neurons grown in a dish, \ an electrode in each: \ the timing of single "
                               r"spikes is set by hand", 5.0, 26, GREY_A)
        intro = VGroup(phrase, dish, dish_l).arrange(DOWN, buff=0.4).move_to([3.9, 0.0, 0])

        def pair(first_input: bool, col):
            xs = (0.0, 0.7) if first_input else (0.7, 0.0)
            rows = VGroup()
            for name, x, c in ((r"input", xs[0], EXC), (r"cell", xs[1], VOLT)):
                base = Line([0, 0, 0], [2.0, 0, 0], color=GREY_D, stroke_width=2)
                tick = Line([0.5 + x, 0, 0], [0.5 + x, 0.4, 0], color=c, stroke_width=5)
                rows.add(VGroup(label(name, font_size=22, color=c).next_to(base, LEFT, buff=0.15), base, tick))
            rows.arrange(DOWN, buff=0.28, aligned_edge=RIGHT)
            return rows

        r1 = VGroup(pair(True, EXC), wrapped_label(r"input first: \ it helped to fire the cell. \ Stronger", 3.2, 26,
                                                   EXC)).arrange(RIGHT, buff=0.3)
        r2 = VGroup(pair(False, INH), wrapped_label(r"input late: \ it did not help. \ Weaker", 3.2, 26, INH)).arrange(
            RIGHT, buff=0.3)
        side = VGroup(r1, r2).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([3.9, 0.3, 0])
        end = wrapped_label(r"The synapse keeps the inputs that predicted the cell's firing.", 6.0, 28, P.ACCENT)
        end.next_to(side, DOWN, buff=0.5)
        keep_in_frame(VGroup(side, end))
        src = published_tag(archive.BI_POO_1998.cite)
        tag = psyche_tag(r"computed: Psyche's rule, shaped after the experiment")
        with self.voiceover(
            "Hebb wrote, takes part in firing it, and that phrase has an order in it. To take part in firing a "
            "cell, an input has to arrive before the cell fires. <bookmark mark='p'/> In 1998 Guo-qiang Bi and Mu-ming Poo tested "
            "exactly that, on pairs of neurons grown in a dish, where they could set the timing of single "
            "spikes. <bookmark mark='a'/> When the input arrived just before the cell's own spike, the "
            "synapse got stronger. <bookmark mark='b'/> When it arrived just after, the synapse got weaker. "
            f"<bookmark mark='c'/> And it mattered only within about {p['window']} milliseconds either side. "
            "The curve is Psyche's version of the rule, with that shape. <bookmark mark='d'/> So a synapse "
            "isn't only registering that two cells were active around the same time. It keeps the inputs that "
            "predicted the cell's firing, and drops the ones that came too late to have caused it. That's a "
            "rule about causes. Whether this exact rule is what operates in a living brain is still argued, "
            "and we'll come to that at the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(phrase))
            vo.wait_until("p")
            self.play(FadeIn(dish), FadeIn(dish_l), FadeIn(A), Create(zero), Create(vert))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.6)
            self.play(FadeIn(r1), Create(pos), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(r2), Create(neg), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(win), FadeIn(win_l))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def bcm(self):
        p = load("plasticity")
        head = heading(r"A threshold that slides: \ strengthening and weakening")
        A = axes([0, 3], [-1.7, 3.2], x_length=4.6, y_length=3.9, xticks=[0, 1, 2, 3], yticks=[0],
                 xlabel=r"the cell's response $y$", ylabel=r"change in an active synapse", center=[-4.2, -0.3, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(3, 0), color=GREY_D, stroke_width=2)
        th = ValueTracker(1.0)
        ys = np.linspace(0, 3, 80)

        def phi():
            t = th.get_value()
            v = ys * (ys - t)
            keep = v <= 3.2
            lo = curve(ax, ys[(ys <= t)], v[(ys <= t)], INH, stroke_width=4)
            hi = curve(ax, ys[(ys >= t) & keep], v[(ys >= t) & keep], EXC, stroke_width=4)
            mark = VGroup(Dot(ax.c2p(t, 0), radius=0.09, color=THRESH),
                          MathTex(r"\theta", font_size=34, color=THRESH).next_to(ax.c2p(t, 0), DOWN, buff=0.12))
            return VGroup(lo, hi, mark)

        fn = always_redraw(phi)
        words = VGroup(label(r"weaken", font_size=24, color=INH).move_to(ax.c2p(0.55, -1.4)),
                       label(r"strengthen", font_size=24, color=EXC).move_to(ax.c2p(1.2, 2.6)))
        B = axes([0, 20], [-0.4, 2.8], x_length=5.8, y_length=3.9, xticks=[0, 5, 10, 15, 20], yticks=[0, 1, 2],
                 xlabel=r"steps of learning (thousands)", ylabel=r"response", center=[3.3, -0.3, 0])
        bx = B.ax
        t = p["bcm_steps"] / 1000
        pref = trace(bx, t, p["bcm_pref"], EXC, 3.5)
        other = trace(bx, t, p["bcm_other"], INH, 3.5)
        k = 15  # the threshold is drawn as a moving average, and the legend says so
        smooth = np.convolve(np.pad(p["bcm_theta"], (k // 2, k // 2), mode="edge"), np.ones(k) / k, mode="valid")
        theta = trace(bx, t, smooth, THRESH, 2)
        lg = legend([(EXC, rf"pattern 1: \ ends at {p['bcm_late_pref']:.2f}"),
                     (INH, rf"pattern 2: \ ends at {abs(p['bcm_late_other']):.2f}"),
                     (THRESH, r"the threshold $\theta$ (smoothed)")], font_size=23)
        lg.next_to(bx.c2p(20, 0.9), LEFT, buff=0.15)
        end = wrapped_label(r"The cell began with no preference. \ Its own activity gave it one.", 12.4, 30, P.ACCENT)
        end.to_edge(DOWN, buff=0.72).shift(LEFT * 1.7)
        tag = psyche_tag()
        with self.voiceover(
            "One more piece. A rule that can only strengthen runs away, as we saw. Real synapses can also be "
            "weakened, and the theory that ties the two together is due to Bienenstock, Cooper and Munro, in "
            "1982. <bookmark mark='a'/> Their rule. When an input is active and the cell responds strongly, "
            "above a threshold, strengthen that synapse. When the cell responds weakly, below the threshold, "
            "weaken it. <bookmark mark='b'/> And the threshold isn't fixed. It slides up when the cell has "
            "been very active lately, and down when it's been quiet. That's the brake Hebb's rule lacked. "
            "<bookmark mark='c'/> Here's a model cell shown two patterns of input, by turns. At first it "
            "responds about equally to both. Then one pulls ahead. The threshold rises behind it, the other "
            "pattern drops below the threshold, and it's weakened away. <bookmark mark='d'/> The rule even "
            "says where this should stop. With two patterns shown equally often, the response to the winner "
            f"should settle at two. The simulation gives {p['bcm_late_pref']:.2f}, and "
            f"{abs(p['bcm_late_other']):.2f} for the loser. <bookmark mark='e'/> The cell has become "
            "selective. It began with no preference, and its own activity gave it one. Cells in the visual "
            "cortex acquire their preferences in much this way, and we'll meet them in the act on perception."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(fn), FadeIn(words))
            vo.wait_until("b")
            self.play(th.animate.set_value(2.0), run_time=2.5)
            self.play(th.animate.set_value(0.7), run_time=2.5)
            self.play(th.animate.set_value(1.0), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(B))
            self.play(Create(theta), Create(pref), Create(other), th.animate.set_value(2.0), FadeIn(lg[2]),
                      run_time=9.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(lg[0]), FadeIn(lg[1]))
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def aplysia(self):
        head = heading(r"A memory in a sea slug")
        # the circuit: siphon -> sensory neuron -> motor neuron -> gill; tail -> facilitating interneuron -> SN terminal
        siphon = label(r"siphon", font_size=20, color=GREY_A).move_to([-6.2, 1.6, 0])
        tail = label(r"tail", font_size=20, color=GREY_A).move_to([-6.2, -0.35, 0])
        gill = label(r"gill", font_size=20, color=GREY_A).move_to([-0.75, 1.6, 0])
        sn = unit(r"S", radius=0.36, color=DATA).move_to([-4.6, 1.6, 0])
        mn = unit(r"M", radius=0.36, color=MODEL).move_to([-2.35, 1.6, 0])
        fi = unit(r"F", radius=0.36, color=RULE).move_to([-4.6, -0.35, 0])
        wires = VGroup(excite(siphon, sn, color=DATA), excite(sn, mn, color=DATA), excite(mn, gill, color=MODEL),
                       excite(tail, fi, color=RULE))
        term = Dot([-3.05, 1.6, 0], radius=0.09, color=DATA)
        mod = Arrow(fi.get_top(), [-3.12, 1.48, 0], buff=0.08, color=RULE, stroke_width=4,
                    max_tip_length_to_length_ratio=0.18)
        mod_l = label(r"onto S's terminal", font_size=16, color=RULE).next_to(mod.get_center(), RIGHT, buff=0.15)
        names = VGroup(label(r"sensory neuron", font_size=17, color=DATA).next_to(sn, UP, buff=0.15),
                       label(r"motor neuron", font_size=17, color=MODEL).next_to(mn, UP, buff=0.15),
                       label(r"interneuron: \ serotonin", font_size=17, color=RULE).next_to(fi, DOWN, buff=0.15))
        # schematic: the reflex over trials, habituating, then restored by a shock to the tail
        A = axes([0, 16], [0, 1.05], x_length=5.4, y_length=2.6, xticks=[1, 8, 16], yticks=[0, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"touches to the siphon",
                 ylabel=r"gill withdrawal", center=[3.55, 0.85, 0], font_size=16)
        k = np.arange(1, 17)
        y = np.where(k <= 10, 0.25 + 0.75 * np.exp(-(k - 1) / 2.8), 0.25 + 0.75 * np.exp(-(k - 11) / 2.8))
        pts_h = VGroup(*[Dot(A.ax.c2p(a, b), radius=0.065, color=DATA) for a, b in zip(k[:10], y[:10])])
        pts_s = VGroup(*[Dot(A.ax.c2p(a, b), radius=0.065, color=RULE) for a, b in zip(k[10:], y[10:])])
        shock = DashedLine(A.ax.c2p(10.5, 0), A.ax.c2p(10.5, 1.05), color=RULE, stroke_width=2)
        shock_l = label(r"tail shock", font_size=16, color=RULE).next_to(shock, UP, buff=0.06)
        habit_l = label(r"habituation", font_size=17, color=DATA).move_to(A.ax.c2p(5.2, 0.85))
        sens_l = label(r"sensitization", font_size=17, color=RULE).move_to(A.ax.c2p(13.6, 0.95))
        sch = label(r"schematic", font_size=15, color=GREY_B).next_to(A, DOWN, buff=0.05).align_to(A, RIGHT)
        cards = point_cards([
            (r"Minutes: \ the same synapse, \ stronger or weaker",
             r"habituation: \ less transmitter from S onto M; \ sensitization: \ serotonin makes S release more", DATA),
            (r"Days: \ new proteins, \ new synapses",
             r"repeated training needs gene expression; \ S's synapses gain release sites after sensitization, \ "
             r"lose them after habituation \ (Bailey and Chen, \ 1983)", RULE),
        ], width=12.6, font_size=19)
        cards.move_to([0, -2.45, 0])
        tag = published_tag(r"Castellucci \& Kandel (1974); \ Brunelli, \ Castellucci \& Kandel (1976); \ Bailey \& "
                            r"Chen (1983)")
        with self.voiceover(
            "Everything so far has come from the hippocampus of mammals. The first memory traced all the way to a "
            "synapse was in a sea slug. <bookmark mark='a'/> Eric Kandel chose Aplysia because its neurons are few "
            "and large, some big enough to see, and because it has a simple reflex. Touch its siphon, and it pulls "
            "in its gill. A sensory neuron excites a motor neuron, which moves the gill. "
            "<bookmark mark='b'/> Touch the siphon again and again, gently, and the withdrawal shrinks: habituation, "
            "the simplest kind of learning. In 1974 Vincent Castellucci and Kandel found where it lives. The "
            "sensory neuron releases less transmitter onto the motor neuron with each touch. <bookmark mark='c'/> "
            "Now shock the tail. The reflex comes back bigger than before: sensitization. An interneuron releases "
            "serotonin onto the sensory neuron's terminals, and they release more transmitter. "
            "<bookmark mark='d'/> That much lasts minutes. With repeated training the change lasts days or weeks, "
            "and then it needs new proteins and new structure. In 1983 Craig Bailey and Mary Chen looked at the "
            "sensory neurons' synapses under the electron microscope: more release sites after long-term "
            "sensitization, fewer after long-term habituation. "
            "<bookmark mark='e'/> Kandel shared the Nobel Prize in 2000. A memory, in a slug as in a rabbit, is "
            "written as a change at a synapse: in its strength for minutes, and in its structure for longer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(siphon), FadeIn(gill), FadeIn(sn), FadeIn(mn), FadeIn(names[:2]),
                      LaggedStart(*[GrowArrow(w) for w in wires[:3]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(sch), LaggedStart(*[FadeIn(p_) for p_ in pts_h], lag_ratio=0.15),
                      FadeIn(habit_l), run_time=2.0)
            self.play(wires[1].animate.set_stroke(width=1.5), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(tail), FadeIn(fi), FadeIn(names[2]), GrowArrow(wires[3]), GrowArrow(mod), FadeIn(term),
                      FadeIn(mod_l),
                      Create(shock), FadeIn(shock_l))
            self.play(wires[1].animate.set_stroke(width=6), LaggedStart(*[FadeIn(p_) for p_ in pts_s],
                                                                         lag_ratio=0.15), FadeIn(sens_l),
                      run_time=1.8)
            vo.wait_until("d")
            self.play(FadeIn(cards.cards[0], shift=UP * 0.15))
            self.play(FadeIn(cards.cards[1], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(Indicate(wires[1], color=DATA))
        self.clear_scene()
