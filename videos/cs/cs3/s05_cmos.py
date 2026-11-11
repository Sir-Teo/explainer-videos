from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import (COST, CTRL, DATA, HEAD, NO, ONE, PART, VDD_COLOR, WIRE, YES, ZERO, ground, load,
                                  nmos, pmos)
from videos.cs.cs2.common import truth_table


def W(a, b):
    return Line(np.asarray(a, float), np.asarray(b, float), color=WIRE, stroke_width=3)


def cmos_gate(kind="NAND", center=ORIGIN, s=1.05):
    """A two-input CMOS NAND or NOR, drawn transistor by transistor.  Returns the group with .pa, .pb (pMOS),
    .na, .nb (nMOS), .out (output wire), .ga, .gb (input labels)."""
    c = np.asarray(center, float)
    g = VGroup()
    top_y, out_y, mid_y, bot_y = 2.3, 0.35, -0.75, -2.0
    if kind == "NAND":  # pMOS in parallel on top, nMOS in series below
        pa = pmos(s).move_to(c + np.array([-1.0, (top_y + out_y) / 2, 0]))
        pb = pmos(s).move_to(c + np.array([1.0, (top_y + out_y) / 2, 0]))
        na = nmos(s).move_to(c + np.array([0.0, (out_y + mid_y) / 2 - 0.05, 0]))
        nb = nmos(s).move_to(c + np.array([0.0, (mid_y + bot_y) / 2 - 0.05, 0]))
        rail = Line(c + np.array([-1.8, top_y, 0]), c + np.array([1.8, top_y, 0]), color=VDD_COLOR, stroke_width=4)
        g.add(rail, pa, pb, na, nb,
              W(pa.drain(), [pa.drain()[0], c[1] + top_y, 0]), W(pb.drain(), [pb.drain()[0], c[1] + top_y, 0]),
              W(pa.source(), [pa.source()[0], c[1] + out_y, 0]), W(pb.source(), [pb.source()[0], c[1] + out_y, 0]),
              W([pa.source()[0], c[1] + out_y, 0], [pb.source()[0], c[1] + out_y, 0]),
              W([na.drain()[0], c[1] + out_y, 0], na.drain()), W(na.source(), nb.drain()),
              W(nb.source(), [nb.source()[0], c[1] + bot_y, 0]))
        gnd = ground(c + np.array([nb.source()[0] - c[0], bot_y, 0]))
        pull_up = VGroup(pa, pb)
        pull_dn = VGroup(na, nb)
    else:  # NOR: pMOS in series on top, nMOS in parallel below
        pa = pmos(s).move_to(c + np.array([0.0, top_y - 0.55, 0]))
        pb = pmos(s).move_to(c + np.array([0.0, top_y - 1.55, 0]))
        na = nmos(s).move_to(c + np.array([-1.0, (out_y + bot_y) / 2 - 0.2, 0]))
        nb = nmos(s).move_to(c + np.array([1.0, (out_y + bot_y) / 2 - 0.2, 0]))
        rail = Line(c + np.array([-1.8, top_y + 0.2, 0]), c + np.array([1.8, top_y + 0.2, 0]), color=VDD_COLOR,
                    stroke_width=4)
        g.add(rail, pa, pb, na, nb,
              W(pa.drain(), [pa.drain()[0], c[1] + top_y + 0.2, 0]), W(pa.source(), pb.drain()),
              W(pb.source(), [pb.source()[0], c[1] + out_y - 0.45, 0]),
              W([na.drain()[0], c[1] + out_y - 0.45, 0], [nb.drain()[0], c[1] + out_y - 0.45, 0]),
              W([na.drain()[0], c[1] + out_y - 0.45, 0], na.drain()),
              W([nb.drain()[0], c[1] + out_y - 0.45, 0], nb.drain()),
              W(na.source(), [na.source()[0], c[1] + bot_y, 0]), W(nb.source(), [nb.source()[0], c[1] + bot_y, 0]),
              W([na.source()[0], c[1] + bot_y, 0], [nb.source()[0], c[1] + bot_y, 0]))
        gnd = ground(c + np.array([0, bot_y, 0]))
        out_y = out_y - 0.45
        pull_up = VGroup(pa, pb)
        pull_dn = VGroup(na, nb)
    out_start = c + np.array([1.2 if kind == "NOR" else 1.4, out_y, 0])
    out_x0 = pb.source()[0] if kind == "NAND" else nb.drain()[0]
    out = W([out_x0, c[1] + out_y, 0], c + np.array([2.4, out_y, 0]))
    vl = MathTex(r"V_{DD}", font_size=26, color=VDD_COLOR).next_to(rail, UP, buff=0.08)
    ol = MathTex(r"\text{out}", font_size=28, color=GREY_A).next_to(out, RIGHT, buff=0.1)
    labs = VGroup()
    for t, nm in ((pa, "A"), (pb, "B"), (na, "A"), (nb, "B")):
        labs.add(MathTex(nm, font_size=28, color=DATA).next_to(t.gate_pin(), LEFT, buff=0.08))
    g.add(gnd, out, vl, ol, labs)
    g.pa, g.pb, g.na, g.nb, g.out = pa, pb, na, nb, out
    g.pull_up, g.pull_dn = pull_up, pull_dn
    return g


class Cmos(VoiceoverScene):
    def construct(self):
        self.card()
        self.nand()
        self.nor()
        self.aoi()
        self.costs()
        self.power()

    def card(self):
        card = chapter_card(4, r"CMOS gates", r"How are gates built from transistors?", lit=(1958,), part=PART)
        with self.voiceover("Chapter four. CMOS gates."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def run(self, gte, fn, tt):
        for k, (a, b) in enumerate(((0, 0), (0, 1), (1, 0), (1, 1))):
            o = fn(a, b)
            self.play(gte.pa.conduct(not a), gte.pb.conduct(not b), gte.na.conduct(bool(a)), gte.nb.conduct(bool(b)),
                      gte.out.animate.set_stroke(ONE if o else ZERO), FadeIn(tt.rows[k]), run_time=0.8)
            self.wait(0.3)

    def nand(self):
        head = label(r"NAND, \ in four transistors", font_size=38).to_edge(UP, buff=0.3)
        g = cmos_gate("NAND", LEFT * 2.8 + DOWN * 0.4)
        tt = truth_table([r"A", r"B", r"\text{out}"], [[bool(a), bool(b), not (a and b)] for a, b in
                                                       ((0, 0), (0, 1), (1, 0), (1, 1))],
                         font_size=32, col_w=1.15, colors={0: DATA, 1: DATA, 2: HEAD}).move_to(RIGHT * 4.6 + UP * 1.2)
        txt = VGroup(label(r"pull-up: \ two pMOS in \textit{parallel}", font_size=26, color=CTRL),
                     label(r"pull-down: \ two nMOS in \textit{series}", font_size=26, color=CTRL),
                     label(r"out $= 0$ \ only when $A$ and $B$ are both $1$", font_size=26, color=HEAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).next_to(tt, DOWN, buff=0.5)
        with self.voiceover(
            "The inverter's trick extends to two inputs. <bookmark mark='a'/> To pull the output down to zero, put two "
            "n transistors in series between the output and ground: the path conducts only if A and B are both high. "
            "<bookmark mark='b'/> To pull it up, put two p transistors in parallel between the supply and the output: "
            "either one conducting, when A or B is low, connects the output to one. <bookmark mark='c'/> Run the four "
            "inputs. The output is zero only when both are one: not and, NAND. And as before, for every input exactly "
            "one of the two networks conducts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Indicate(g.pull_dn, color=HEAD), FadeIn(txt[1]))
            vo.wait_until("b")
            self.play(Indicate(g.pull_up, color=HEAD), FadeIn(txt[0]))
            vo.wait_until("c")
            self.play(FadeIn(tt.cells[0][0]), FadeIn(tt.cells[0][1]), FadeIn(tt.cells[0][2]), FadeIn(tt.rule))
            self.run(g, lambda a, b: not (a and b), tt)
            self.play(FadeIn(txt[2]))
        self.wait(0.3)
        self.clear_scene()

    def nor(self):
        head = label(r"NOR: \ the same parts, \ swapped", font_size=38).to_edge(UP, buff=0.3)
        g = cmos_gate("NOR", LEFT * 2.8 + DOWN * 0.4)
        tt = truth_table([r"A", r"B", r"\text{out}"], [[bool(a), bool(b), not (a or b)] for a, b in
                                                       ((0, 0), (0, 1), (1, 0), (1, 1))],
                         font_size=32, col_w=1.15, colors={0: DATA, 1: DATA, 2: HEAD}).move_to(RIGHT * 4.6 + UP * 1.2)
        txt = VGroup(label(r"series $\leftrightarrow$ parallel: \ the pull-up network \\ is the \textit{dual} of the "
                           r"pull-down", font_size=26, color=YES),
                     label(r"De Morgan, \ in silicon: \\ $\overline{A + B} = \bar A\,\bar B$", font_size=26,
                           color=HEAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(tt, DOWN, buff=0.5)
        with self.voiceover(
            "Swap the arrangement: n transistors in parallel below, p transistors in series above. "
            "<bookmark mark='a'/> Now either input high pulls the output down, and only both low pulls it up. NOR. "
            "<bookmark mark='b'/> The two networks of every CMOS gate are each other's duals: series in one is "
            "parallel in the other, exactly chapter one's duality, and the p network computes the De Morgan twin of "
            "the n network. Any expression built from and and or, with an inversion on the output, becomes one CMOS "
            "gate this way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(tt.cells[0][0]), FadeIn(tt.cells[0][1]), FadeIn(tt.cells[0][2]), FadeIn(tt.rule))
            self.run(g, lambda a, b: not (a or b), tt)
            vo.wait_until("b")
            self.play(FadeIn(txt, lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def aoi(self):
        from videos.cs.cs3.s03_relays import ladder
        head = label(r"Any expression, \ as one gate", font_size=38).to_edge(UP, buff=0.35)
        f = MathTex(r"\text{out} = \overline{A B + C}", font_size=42, color=YES).next_to(head, DOWN, buff=0.35)
        dn, _ = ladder([[r"A", r"B"], [r"C"]], x0=-5.6, x1=-2.2, y0=0.4, dy=1.0, length=0.75)
        up, _ = ladder([[r"A"], [r"B"]], x0=1.4, x1=3.4, y0=0.4, dy=1.0, length=0.75)
        c_up = VGroup(Line([3.4, -0.1, 0], [3.9, -0.1, 0], color=WIRE, stroke_width=3))
        from videos.cs.cs3.common import switch
        sc = switch(False, length=0.75).move_to([4.4, -0.1, 0])
        c_lab = MathTex(r"C", font_size=28, color=DATA).next_to(sc, UP, buff=0.1)
        c_up.add(sc, c_lab, Line(sc.right(), [5.4, -0.1, 0], color=WIRE, stroke_width=3))
        ldn = label(r"pull-down (nMOS): \ $AB$ in parallel with $C$", font_size=24, color=CTRL).next_to(dn, DOWN, buff=0.4)
        lup = label(r"pull-up (pMOS): \ the dual, \ ($A$ or $B$ low) in series with $C$ low", font_size=24,
                    color=CTRL).next_to(VGroup(up, c_up), DOWN, buff=0.4)
        cnt = label(r"6 transistors: \ one AND-OR-INVERT gate, \ instead of a NAND, a NOT and a NOR \ (10)",
                    font_size=26, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Duality does more than NAND and NOR. <bookmark mark='a'/> Take any expression built from and and or, "
            "say A and B, or C, and invert it. <bookmark mark='b'/> Build the expression itself as a network of n "
            "transistors pulling the output down: A and B in series, in parallel with C. <bookmark mark='c'/> Build "
            "its dual from p transistors pulling up: A and B in parallel, in series with C. The result is a single "
            "gate, an and-or-invert, in six transistors, where separate gates would need ten. "
            "<bookmark mark='d'/> Real cell libraries are full of these compound gates, and a synthesis tool chooses "
            "among them the way a chess program chooses moves."
        ) as vo:
            self.play(FadeIn(head), Write(f), Create(dn), FadeIn(ldn))
            vo.wait_until("a")
            self.play(Circumscribe(f, color=HEAD))
            vo.wait_until("b")
            self.play(Circumscribe(dn, color=HEAD))
            vo.wait_until("c")
            self.play(Create(up), Create(c_up), FadeIn(lup))
            vo.wait_until("d")
            self.play(FadeIn(cnt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def costs(self):
        head = label(r"Transistors per gate", font_size=38).to_edge(UP, buff=0.35)
        rows = [(r"NOT", 2, r""), (r"NAND, \ NOR", 4, r"the natural gates of CMOS"),
                (r"AND, \ OR", 6, r"a NAND or NOR, \ then an inverter"),
                (r"XOR", 8, r"or 12 in the plainest design")]
        tab = VGroup()
        for i, (n, k, why) in enumerate(rows):
            bar = Rectangle(width=k * 0.55, height=0.42, stroke_width=0, fill_color=COST, fill_opacity=0.85)
            r = VGroup(label(n, font_size=30, color=CTRL), bar, MathTex(str(k), font_size=32), note(why, font_size=22))
            r[0].move_to([-4.2, 1.3 - 0.9 * i, 0], aligned_edge=RIGHT)
            r[1].move_to([-3.8, 1.3 - 0.9 * i, 0], aligned_edge=LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.2)
            r[3].next_to(r[2], RIGHT, buff=0.4)
            tab.add(r)
        mob = label(r"electrons move 2--3 times faster than holes: \ nMOS in series (NAND) \\ beats pMOS in series "
                    r"(NOR), \ so real chips are mostly NAND and inverters", font_size=26, color=GREY_A).to_edge(
            DOWN, buff=0.6)
        with self.voiceover(
            "Count the transistors. <bookmark mark='a'/> An inverter takes two. NAND and NOR take four. And or or "
            "takes six, because CMOS naturally inverts: you build a NAND and then invert it. Exclusive-or takes eight or "
            "more. <bookmark mark='b'/> So the natural gates of CMOS are the inverting ones. And between those two, "
            "NAND wins: its series transistors are n-type, and electrons, which carry the current in n-type "
            "transistors, move two to three times faster than the holes in p-type ones. A modern chip is mostly NAND "
            "gates and inverters, which is why the next chapter asks whether NAND alone is enough."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in tab], lag_ratio=0.3), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(mob))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def power(self):
        d = load("cmos")
        vin, idd = np.asarray(d["vin"]), np.asarray(d["idd"])
        head = label(r"Switching power in CMOS", font_size=38).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, float(idd.max()) * 1.15, float(idd.max()) / 2], x_length=5.6,
                  y_length=3.4, tips=False, axis_config={"color": GREY_C, "font_size": 20},
                  x_axis_config={"numbers_to_include": [0, 0.5, 1]}).move_to(LEFT * 3.0 + DOWN * 0.3)
        path = VMobject(color=COST, stroke_width=4).set_points_as_corners([ax.c2p(x, y) for x, y in zip(vin, idd)])
        xl = MathTex(r"V_{\text{in}} / V_{DD}", font_size=26, color=GREY_B).next_to(ax, DOWN, buff=0.15)
        yl = label(r"model current: both transistors conduct", font_size=22, color=GREY_B).next_to(ax, UP, buff=0.15)
        txt = VGroup(label(r"stable 0 or 1: \ no ideal DC path; \ real devices leak", font_size=26, color=YES),
                     label(r"while switching: \ both briefly on, \\ and the next gate's input is charged", font_size=26,
                           color=COST),
                     MathTex(r"P \approx \alpha\, C\, V_{DD}^2\, f", font_size=42, color=HEAD),
                     note(r"$\alpha$: how often a wire switches; \ $C$: what it must charge; \ $f$: the clock", font_size=22),
                     label(r"lower $V_{DD}$, \ fewer switchings: \ Parts 7 and 10", font_size=26, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.3 + DOWN * 0.2)
        with self.voiceover(
            "One more property, and it is why CMOS won. <bookmark mark='a'/> The current the inverter draws from its "
            "supply, computed across the sweep, is zero at both ends and spikes only in the middle, while both "
            "transistors are partly on. <bookmark mark='b'/> In this ideal model, a stable CMOS gate draws no current; real gates still leak. Switching costs "
            "energy in two ways: overlap current while both transistors conduct, and the charge needed to flip the "
            "wires and gates it drives. <bookmark mark='c'/> The capacitive switching power is roughly the fraction of wires that switch, "
            "times their capacitance, times the supply voltage squared, times the clock frequency. That one formula "
            "explains why clocks stopped getting faster around 2005, and why chips grew many cores instead, which is "
            "Part 10."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(path), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(txt[0]), FadeIn(txt[1]))
            vo.wait_until("c")
            self.play(Write(txt[2]), FadeIn(txt[3]), FadeIn(txt[4]))
        self.wait(0.3)
        self.clear_scene()
