from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import (COST, CTRL, DATA, HEAD, HIST, NO, ONE, PART, VDD_COLOR, WIRE, YES, ZERO, ground,
                                  load, nmos, pmos, rail)


class Transistors(VoiceoverScene):
    def construct(self):
        self.card()
        self.speed()
        self.mosfet()
        self.inverter()
        self.curve()
        self.restore()

    def card(self):
        card = chapter_card(3, r"The transistor", r"How do you make a switch with no moving parts?", lit=(1947, 1958),
                            part=PART)
        with self.voiceover("Chapter three. The transistor."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def speed(self):
        head = label(r"Faster switches", font_size=38).to_edge(UP, buff=0.35)
        rows = [
            (r"relay", r"1930s", r"$\sim 10^{-2}$ s", r"a moving metal contact; \ clicks, \ wears out"),
            (r"vacuum tube", r"1940s", r"$\sim 10^{-6}$ s", r"electrons through a vacuum; \ hot, \ burns out \\ "
                                                             r"(ENIAC: 17{,}468 tubes)"),
            (r"transistor", r"1947 $\to$", r"$\sim 10^{-11}$ s", r"electrons through silicon; \ nothing moves"),
        ]
        tab = VGroup()
        for i, (a, b, c, d) in enumerate(rows):
            r = VGroup(label(a, font_size=30, color=[CTRL, HEAD, YES][i]), label(b, font_size=26, color=GREY_B),
                       label(c, font_size=30, color=COST), label(d, font_size=23, color=GREY_A))
            r[0].move_to([-5.4, 1.2 - 1.1 * i, 0], aligned_edge=LEFT)
            r[1].move_to([-2.6, 1.2 - 1.1 * i, 0], aligned_edge=LEFT)
            r[2].move_to([-0.9, 1.2 - 1.1 * i, 0], aligned_edge=LEFT)
            r[3].move_to([0.9, 1.2 - 1.1 * i, 0], aligned_edge=LEFT)
            tab.add(r)
        hdr = VGroup(note(r"switch", font_size=22).move_to([-5.4, 2.0, 0], aligned_edge=LEFT),
                     note(r"switching time", font_size=22).move_to([-0.9, 2.0, 0], aligned_edge=LEFT))
        hc = note(r"1947: \ Bardeen, Brattain and Shockley, Bell Labs; \ 1959: \ the MOSFET (Atalla and Kahng); \ "
                  r"1958--59: \ the integrated circuit (Kilby, Noyce)", font_size=21).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Shannon's algebra does not care what the switches are made of, which is lucky, because relays are slow. "
            "<bookmark mark='a'/> A relay moves a piece of metal, and takes about a hundredth of a second. "
            "<bookmark mark='b'/> A vacuum tube steers electrons through a vacuum and switches a thousand times faster, "
            "but it is hot and it burns out; ENIAC, in 1945, had seventeen and a half thousand of them. "
            "<bookmark mark='c'/> The transistor, invented at Bell Labs in 1947, switches electrons in a solid crystal "
            "with nothing moving at all, and today's switch in a few picoseconds. The kind in every chip is the "
            "MOSFET, from 1959, and from 1958 they were built many at a time on one slice of silicon: the integrated "
            "circuit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(Circumscribe(tab[0], color=HEAD))
            for mk, r in zip("bc", tab[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            self.play(FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mosfet(self):
        head = label(r"A transistor is a switch worked by a voltage", font_size=36).to_edge(UP, buff=0.35)
        n = nmos(scale=1.6).move_to(LEFT * 3.2 + DOWN * 0.2)
        p = pmos(scale=1.6).move_to(RIGHT * 2.6 + DOWN * 0.2)
        ln = VGroup(label(r"nMOS", font_size=32, color=CTRL),
                    label(r"gate high: \ drain and source connected", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.15).next_to(n, DOWN, buff=0.5)
        lp = VGroup(label(r"pMOS", font_size=32, color=CTRL),
                    label(r"gate low: \ connected \ (the bubble: \ not)", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.15).next_to(p, DOWN, buff=0.5)
        gn = MathTex(r"0", font_size=36, color=GREY_B).next_to(n.gate_pin(), LEFT, buff=0.15)
        gp = MathTex(r"0", font_size=36, color=GREY_B).next_to(p.gate_pin(), LEFT, buff=0.15)
        names = VGroup(note(r"drain", font_size=20).next_to(n.drain(), RIGHT, buff=0.1),
                       note(r"source", font_size=20).next_to(n.source(), RIGHT, buff=0.1),
                       note(r"gate", font_size=20).next_to(n.gate_pin(), DOWN, buff=0.15))
        with self.voiceover(
            "For logic, a MOSFET is just a switch with three wires. <bookmark mark='a'/> In an n-type transistor, a "
            "high voltage on the gate connects the drain to the source; a low voltage disconnects them. The gate itself "
            "draws almost no current: it works like the coil of a relay, through an electric field instead of a magnet. "
            "<bookmark mark='b'/> A p-type transistor is the mirror image: it conducts when its gate is low. The little "
            "bubble on the symbol means not, as on a gate. <bookmark mark='c'/> Two kinds of switch, one that closes on "
            "one and one that closes on zero. Put them together and something remarkable happens."
        ) as vo:
            self.play(FadeIn(head), FadeIn(n), FadeIn(names), FadeIn(gn))
            vo.wait_until("a")
            self.play(Transform(gn, MathTex(r"1", font_size=36, color=YES).move_to(gn)), n.conduct(True), FadeIn(ln))
            self.play(Transform(gn, MathTex(r"0", font_size=36, color=GREY_B).move_to(gn)), n.conduct(False))
            vo.wait_until("b")
            self.play(FadeIn(p), FadeIn(gp), FadeIn(lp), p.conduct(True))
            self.play(Transform(gp, MathTex(r"1", font_size=36, color=YES).move_to(gp)), p.conduct(False))
            vo.wait_until("c")
            self.play(Transform(gp, MathTex(r"0", font_size=36, color=GREY_B).move_to(gp)), p.conduct(True))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inverter_mob(self, center=ORIGIN, scale=1.3):
        p = pmos(scale=scale).move_to(center + UP * 0.95 * scale)
        n = nmos(scale=scale).move_to(center + DOWN * 0.95 * scale)
        # the pMOS source goes to VDD (drawn on top), its drain to the output
        top = p.drain()
        bot = n.source()
        out_pt = (p.source() + n.drain()) / 2
        rail_top = Line(top + LEFT * 0.6, top + RIGHT * 0.6, color=VDD_COLOR, stroke_width=4)
        gnd = ground(bot)
        mid = Line(p.source(), n.drain(), color=WIRE, stroke_width=3)
        out = Line(out_pt, out_pt + RIGHT * 1.4, color=WIRE, stroke_width=3)
        gate_wire = VGroup(Line(p.gate_pin(), p.gate_pin() + LEFT * 0.5, color=WIRE, stroke_width=3),
                           Line(n.gate_pin(), n.gate_pin() + LEFT * 0.5, color=WIRE, stroke_width=3),
                           Line(p.gate_pin() + LEFT * 0.5, n.gate_pin() + LEFT * 0.5, color=WIRE, stroke_width=3))
        inp = Line(out_pt * np.array([0, 1, 0]) + np.array([gate_wire.get_left()[0], 0, 0]),
                   out_pt * np.array([0, 1, 0]) + np.array([gate_wire.get_left()[0] - 1.0, 0, 0]), color=WIRE,
                   stroke_width=3)
        vl = MathTex(r"V_{DD}", font_size=30, color=VDD_COLOR).next_to(rail_top, UP, buff=0.1)
        g = VGroup(rail_top, vl, p, n, mid, out, gate_wire, inp, gnd)
        g.p, g.n, g.out, g.inp, g.mid = p, n, out, inp, mid
        return g

    def inverter(self):
        head = label(r"The CMOS inverter", font_size=38).to_edge(UP, buff=0.35)
        inv = self.inverter_mob(LEFT * 3.0 + DOWN * 0.3)
        in_v = MathTex(r"\text{in} = 0", font_size=34, color=GREY_B).next_to(inv.inp, LEFT, buff=0.15)
        out_v = MathTex(r"\text{out} = 1", font_size=34, color=YES).next_to(inv.out, RIGHT, buff=0.15)
        txt = VGroup(*[label(t, font_size=27, color=c) for t, c in (
            (r"in $= 0$: \ the pMOS conducts, \ the nMOS does not: \\ out is pulled up to $V_{DD}$ \ $= 1$", GREY_A),
            (r"in $= 1$: \ the nMOS conducts, \ the pMOS does not: \\ out is pulled down to ground \ $= 0$", GREY_A),
            (r"at a stable 0 or 1: \\ no ideal DC path; \ real devices still leak", HEAD),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(RIGHT * 3.5 + DOWN * 0.2)
        with self.voiceover(
            "Stack a p-type transistor on an n-type one, the p on top connected to the supply voltage, the n below "
            "connected to ground, and join their gates as the input and their middle as the output. This is the CMOS "
            "inverter, the C standing for complementary. <bookmark mark='a'/> Input zero: the p transistor conducts and "
            "the n does not, so the output is connected to the supply: one. <bookmark mark='b'/> Input one: the n "
            "conducts and the p does not, so the output is connected to ground: zero. It computes not. "
            "<bookmark mark='c'/> At a stable zero or one, one transistor is off, so the ideal circuit has no path from the "
            "supply to ground. Real transistors still leak, and switching consumes energy. That is why static CMOS is "
            "so efficient."
        ) as vo:
            self.play(FadeIn(head), FadeIn(inv), FadeIn(in_v))
            vo.wait_until("a")
            self.play(inv.p.conduct(True), inv.out.animate.set_stroke(ONE), FadeIn(out_v), FadeIn(txt[0]))
            vo.wait_until("b")
            self.play(Transform(in_v, MathTex(r"\text{in} = 1", font_size=34, color=YES).move_to(in_v)),
                      inv.p.conduct(False), inv.n.conduct(True), inv.out.animate.set_stroke(ZERO),
                      Transform(out_v, MathTex(r"\text{out} = 0", font_size=34, color=GREY_B).move_to(out_v)),
                      FadeIn(txt[1]))
            vo.wait_until("c")
            self.play(FadeIn(txt[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        d = load("cmos")
        vin, vout = np.asarray(d["vin"]), np.asarray(d["vout"])
        head = label(r"Between 0 and 1: \ the transfer curve", font_size=38).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1, 0.25], x_length=5.6, y_length=5.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 20},
                  x_axis_config={"numbers_to_include": [0, 0.25, 0.5, 0.75, 1]},
                  y_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1]}).move_to(LEFT * 2.8 + DOWN * 0.4)
        xl = MathTex(r"V_{\text{in}} / V_{DD}", font_size=26, color=GREY_B).next_to(ax, DOWN, buff=0.15)
        yl = MathTex(r"V_{\text{out}}", font_size=26, color=GREY_B).next_to(ax, LEFT, buff=0.1).shift(UP * 2.0)
        path = VMobject(color=CTRL, stroke_width=4).set_points_as_corners([ax.c2p(x, y) for x, y in zip(vin, vout)])
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_D, stroke_width=1.5)
        vm = Dot(ax.c2p(d["vm"], d["vm"]), color=HEAD, radius=0.07)
        lo_band = Rectangle(width=ax.x_length * d["vil"], height=ax.y_length, stroke_width=0, fill_color=YES,
                            fill_opacity=0.08).move_to(ax.c2p(d["vil"] / 2, 0.5))
        hi_band = Rectangle(width=ax.x_length * (1 - d["vih"]), height=ax.y_length, stroke_width=0, fill_color=YES,
                            fill_opacity=0.08).move_to(ax.c2p((1 + d["vih"]) / 2, 0.5))
        txt = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (rf"switching threshold: \ $V_M = {d['vm']:.2f}\,V_{{DD}}$", HEAD),
            (rf"steepest slope: \ gain $\approx {d['max_gain']:.0f}$", COST),
            (rf"noise margins: \ $NM_L = NM_H \approx {d['nml']:.2f}\,V_{{DD}}$", YES),
            (r"any input below $V_{IL}$ counts as 0; \\ any above $V_{IH}$ counts as 1", GREY_A),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(RIGHT * 3.4 + DOWN * 0.2)
        model = note(r"computed: \ square-law transistors, \ $V_T = 0.3\,V_{DD}$, \ matched sizes", font_size=20)
        model.to_corner(DR, buff=0.25)
        with self.voiceover(
            "Real voltages are not exactly zero and one, so look at everything in between. <bookmark mark='a'/> Sweep "
            "the input from ground to the supply, and plot the output, computed here from a standard model of the two "
            "transistors. It stays high, then plunges, then stays low. <bookmark mark='b'/> It crosses the diagonal at "
            "half the supply: the switching threshold. And in the middle it is very steep: a small change in the input "
            "makes a change in the output more than a hundred times bigger. <bookmark mark='c'/> The flat parts are the "
            "point. Anything below about forty-five percent of the supply is read as a clean zero, and anything above "
            "about fifty-five percent as a clean one. The gaps between what a gate guarantees to produce and what the "
            "next gate needs to see are the noise margins."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), Create(diag))
            vo.wait_until("a")
            self.play(Create(path), run_time=2.2)
            self.play(FadeIn(model))
            vo.wait_until("b")
            self.play(FadeIn(vm), FadeIn(txt[0]))
            self.play(FadeIn(txt[1]))
            vo.wait_until("c")
            self.play(FadeIn(lo_band), FadeIn(hi_band), FadeIn(txt[2]), FadeIn(txt[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def restore(self):
        d = load("cmos")
        vin, vout = np.asarray(d["vin"]), np.asarray(d["vout"])

        def f(v):
            return float(np.interp(v, vin, vout))

        head = label(r"Every gate cleans up its input", font_size=38).to_edge(UP, buff=0.35)
        vals = [0.38]
        for _ in range(4):
            vals.append(f(vals[-1]))
        bars = VGroup()
        for k, v in enumerate(vals):
            frame = Rectangle(width=0.8, height=3.0, stroke_color=GREY_D, stroke_width=1.5).move_to(
                [-4.8 + 2.4 * k, -0.4, 0])
            fill = Rectangle(width=0.8, height=max(3.0 * v, 0.02), stroke_width=0,
                             fill_color=YES if v > 0.5 else DATA, fill_opacity=0.8).move_to(frame.get_bottom(),
                                                                                             aligned_edge=DOWN)
            tv = MathTex(f"{v:.2f}", font_size=30, color=WHITE).next_to(frame, DOWN, buff=0.2)
            bars.add(VGroup(frame, fill, tv))
        arrows = VGroup(*[label(r"$\rightarrow$ \textsc{not} $\rightarrow$", font_size=22, color=CTRL).move_to(
            (bars[k].get_center() + bars[k + 1].get_center()) / 2 + DOWN * 0.4) for k in range(4)])
        cap = label(r"a sloppy zero ($0.38\,V_{DD}$) \ becomes a clean one, \ then a cleaner zero", font_size=28,
                    color=HEAD).to_edge(DOWN, buff=0.5)
        why = note(r"this is what makes a circuit \textit{digital}: \ errors shrink at every stage \ instead of adding up",
                   font_size=22).next_to(cap, DOWN, buff=0.12)
        with self.voiceover(
            "That steep curve does something wonderful. <bookmark mark='a'/> Feed a chain of inverters a sloppy zero, "
            "at thirty-eight percent of the supply, almost in the middle. <bookmark mark='b'/> After one inverter it is "
            "a confident one. After two, an almost perfect zero, and it stays perfect. Each gate restores the signal "
            "towards the rails. <bookmark mark='c'/> This is what digital means. In an analog circuit, noise accumulates "
            "with every stage. In a digital one, every gate throws it away, so a signal can pass through billions of "
            "gates and arrive intact. Everything from here on counts in zeros and ones, and it is allowed to because of "
            "this curve."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars[0]))
            vo.wait_until("a")
            self.play(Circumscribe(bars[0], color=HEAD))
            vo.wait_until("b")
            for k in range(1, len(bars)):
                self.play(FadeIn(arrows[k - 1]), FadeIn(bars[k], shift=RIGHT * 0.2), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(cap), FadeIn(why))
        self.wait(0.3)
        self.clear_scene()
