from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import CLOCK, COST, CTRL, DATA, HEAD, NO, ONE, PART, WIRE, YES, ZERO, gate, load, wire


def waveform(values, x0, y0, dx=0.55, h=0.45, color=DATA, label_tex=""):
    """A digital waveform: one step of width dx per time unit."""
    pts = []
    for t, v in enumerate(values):
        y = y0 + (h if v else 0)
        pts += [np.array([x0 + t * dx, y, 0]), np.array([x0 + (t + 1) * dx, y, 0])]
    m = VMobject(color=color, stroke_width=3.5).set_points_as_corners(pts)
    lab = MathTex(label_tex, font_size=26, color=color).next_to(np.array([x0, y0 + h / 2, 0]), LEFT, buff=0.25)
    return VGroup(m, lab)


class Timing(VoiceoverScene):
    def construct(self):
        self.card()
        self.delay()
        self.hazard()
        self.fix()
        self.wires()

    def card(self):
        card = chapter_card(10, r"Gates take time", r"What happens between one answer and the next?", part=PART)
        with self.voiceover("Chapter ten. Gates take time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def delay(self):
        d = load("blocks")
        rows = {r["name"]: r for r in d["rows"]}
        head = label(r"Propagation delay, \ and the critical path", font_size=36).to_edge(UP, buff=0.35)
        gs = [gate(k, size=0.7) for k in ("NAND", "NAND", "NOT", "NAND", "NOR")]
        pos = [LEFT * 5.0 + UP * 0.9, LEFT * 5.0 + DOWN * 0.7, LEFT * 3.2 + UP * 0.9, LEFT * 1.4 + UP * 0.1,
               RIGHT * 0.4 + UP * 0.1]
        for g_, p in zip(gs, pos):
            g_.move_to(p)
        ws = VGroup(wire(gs[0].out(), gs[2].inp[0]()), wire(gs[2].out(), gs[3].inp[0]()),
                    wire(gs[1].out(), gs[3].inp[1]()), wire(gs[3].out(), gs[4].inp[0]()),
                    wire(gs[1].out() + RIGHT * 0.6, gs[4].inp[1]() + LEFT * 0.0, via="hv"))
        crit = VGroup(gs[0], gs[2], gs[3], gs[4], ws[0], ws[1], ws[3])
        txt = VGroup(label(r"each gate: \ a few picoseconds to change its output", font_size=26, color=GREY_A),
                     label(r"the slowest input-to-output path \ sets the speed: \ the \textit{critical path}",
                           font_size=26, color=COST),
                     label(rf"Pebble's 8-bit comparator: \ depth {rows['8-bit comparator']['nand_depth']} in NANDs",
                           font_size=26, color=HEAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        txt.scale_to_fit_width(6.6).to_edge(RIGHT, buff=0.4).shift(DOWN * 1.2)
        steps = VGroup(*[MathTex(rf"t = {k + 1}", font_size=22, color=HEAD).next_to(g_, UP, buff=0.12)
                         for k, g_ in enumerate((gs[0], gs[2], gs[3], gs[4]))])
        # the clock budget: a 250 ps cycle at 4 GHz, in 10 ps gate delays
        cells = VGroup(*[Rectangle(width=0.42, height=0.36, stroke_color=GREY_D, stroke_width=1.2, fill_color="#121722",
                                   fill_opacity=1) for _ in range(25)]).arrange(RIGHT, buff=0.04)
        cells.move_to(DOWN * 2.75)
        used = rows['8-bit comparator']['nand_depth']
        fills = VGroup(*[c.copy().set_fill(HEAD, 0.75) for c in cells[:used]])
        b1 = label(r"one cycle at 4 GHz: \ 250 ps \ $\approx$ 25 gate delays of 10 ps", font_size=24,
                   color=GREY_A).next_to(cells, UP, buff=0.15).align_to(cells, LEFT)
        b2 = label(rf"the 8-bit comparator alone: \ {used}", font_size=24, color=HEAD).next_to(cells, DOWN, buff=0.15
                                                                                                ).align_to(cells, LEFT)
        with self.voiceover(
            "So far a gate's output changed the instant its inputs did. Real gates take time: a few picoseconds to "
            "charge the wire they drive. <bookmark mark='a'/> In a circuit, a change at an input ripples forward gate "
            "by gate. <bookmark mark='b'/> The output is not settled until the change has travelled the longest path, "
            "here four gates deep. That path is the critical path, and it sets how fast the whole circuit can run. "
            "<bookmark mark='c'/> Every block in this part is counted in depth as well as size, because in Part 5 the "
            "critical path becomes the length of Pebble's clock cycle. For scale: a four gigahertz clock ticks every two "
            "hundred and fifty picoseconds, and a fast gate takes around ten, so a processor gets only a couple of "
            "dozen gate delays per cycle. Every design decision in act two is about living inside that budget."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(g_) for g_ in gs], Create(ws))
            vo.wait_until("a")
            for k, (g_, w) in enumerate(zip((gs[0], gs[2], gs[3], gs[4]), (ws[0], ws[1], ws[3], None))):
                self.play(g_.body.animate.set_stroke(HEAD), FadeIn(steps[k]),
                          *([w.animate.set_stroke(HEAD)] if w else []), run_time=0.5)
            vo.wait_until("b")
            self.play(FadeIn(txt[0]), FadeIn(txt[1]))
            vo.wait_until("c")
            self.play(FadeIn(txt[2]))
            self.play(FadeIn(cells), FadeIn(b1))
            self.play(LaggedStart(*[FadeIn(c) for c in fills], lag_ratio=0.08), FadeIn(b2), run_time=1.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hazard(self):
        d = load("glitch")
        b = d["before"]
        head = label(r"A glitch", font_size=38).to_edge(UP, buff=0.35)
        f = MathTex(r"f = a\,b + \bar a\, c, \qquad b = c = 1", font_size=36, color=GREY_A).next_to(head, DOWN, buff=0.3)
        should = note(r"with $b = c = 1$, \ $f = a + \bar a = 1$ \ whatever $a$ does", font_size=22).next_to(f, DOWN,
                                                                                                        buff=0.12)
        x0 = -4.4
        rows = [(b["a"], r"a", DATA), (b["not_a"], r"\bar a", CTRL), (b["ab"], r"a b", CTRL),
                (b["nac"], r"\bar a c", CTRL), (b["f"], r"f", HEAD)]
        waves = VGroup(*[waveform(v, x0, 1.35 - 0.95 * i - 0.6, color=c, label_tex=t) for i, (v, t, c) in
                         enumerate(rows)])
        tl = note(r"time, \ in gate delays \ (computed, unit delay per gate)", font_size=20).next_to(waves, DOWN, buff=0.42)
        dip = next(t for t in range(1, len(b["f"])) if b["f"][t] == 0)
        box = Rectangle(width=0.62, height=0.8, stroke_color=NO, stroke_width=3).move_to(
            [x0 + (dip + 0.5) * 0.55, waves[4][0].get_center()[1], 0])
        why = VGroup(label(r"$a$ falls: \ $ab$ drops at once, \\ but $\bar a$ rises one delay late", font_size=24,
                           color=GREY_A),
                     label(r"for one delay, \ both terms are 0: \\ $f$ glitches to 0", font_size=24, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 4.6 + DOWN * 0.8)
        with self.voiceover(
            "Delays cause stranger things than slowness. <bookmark mark='a'/> Take f equals a b plus not a c, with b "
            "and c held at one. Then f is a or not a, which is always one, whatever a does. <bookmark mark='b'/> Now "
            "simulate it with every gate taking one unit of time, and let a fall from one to zero. "
            "<bookmark mark='c'/> The a b term drops immediately. But the not-a term needs the inverter to react first, "
            "so it rises one delay late. For that one moment, both terms are zero, and the output, which should never "
            "change, flickers to zero. This is a glitch, from a static hazard. If anything downstream is watching at "
            "that moment, it sees a wrong answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(f))
            vo.wait_until("a")
            self.play(FadeIn(should))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.2), FadeIn(tl), run_time=2.6)
            vo.wait_until("c")
            self.play(Create(box), FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    def fix(self):
        d = load("glitch")
        a = d["after"]
        head = label(r"Fixing it: \ a redundant term", font_size=38).to_edge(UP, buff=0.35)
        f = MathTex(r"f = a\,b + \bar a\, c + b\,c", font_size=40, color=YES).next_to(head, DOWN, buff=0.35)
        why = note(r"the \textit{consensus} term $bc$: \ logically redundant, \ but it holds $f$ up while $a$ "
                   r"changes", font_size=22).next_to(f, DOWN, buff=0.15)
        x0 = -4.4
        rows = [(a["a"], r"a", DATA), (a["ab"], r"a b", CTRL), (a["nac"], r"\bar a c", CTRL), (a["bc"], r"b c", YES),
                (a["f"], r"f", HEAD)]
        waves = VGroup(*[waveform(v, x0, 0.8 - 0.9 * i - 0.6, color=c, label_tex=t) for i, (v, t, c) in
                         enumerate(rows)])
        lesson = VGroup(label(r"a K-map with every adjacent pair of 1s \\ covered by one loop \ has no static hazard",
                              font_size=24, color=GREY_A),
                        label(r"but the usual cure is the clock: \\ look at outputs only after everything settles "
                              r"\ (Part 5)", font_size=24, color=CLOCK)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        lesson.scale_to_fit_width(4.8).move_to(RIGHT * 4.5 + DOWN * 0.8)
        with self.voiceover(
            "One fix is surprising. <bookmark mark='a'/> Add the term b c, which the laws of chapter one say is "
            "redundant: it changes nothing about the function. <bookmark mark='b'/> But during the transition it holds "
            "the output up, and the glitch is gone. On a Karnaugh map, the rule is to cover every pair of neighbouring "
            "ones with a single loop. <bookmark mark='c'/> The more common cure is to stop caring: make every circuit "
            "settle before anybody looks at it, by reading outputs only at the tick of a clock. That is how Part 5 "
            "builds memory and time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(why))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.2), run_time=2.4)
            vo.wait_until("c")
            self.play(FadeIn(lesson))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wires(self):
        head = label(r"Why gates take time: \ wires are capacitors", font_size=36).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 1, 0.5], x_length=5.4, y_length=2.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(LEFT * 3.0 + DOWN * 0.4)
        curves = VGroup()
        for tau, col in ((0.5, YES), (1.0, HEAD), (2.0, NO)):
            curves.add(ax.plot(lambda t, tau=tau: 1 - np.exp(-t / tau), x_range=[0, 5], color=col, stroke_width=3))
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(5, 0.5), color=GREY_D, stroke_width=1.5)
        keys = VGroup(label(r"fan-out 1", font_size=22, color=YES), label(r"fan-out 2", font_size=22, color=HEAD),
                      label(r"fan-out 4", font_size=22, color=NO)).arrange(RIGHT, buff=0.4).next_to(ax, UP, buff=0.2)
        xl = note(r"time \ (in units of $RC$)", font_size=20).next_to(ax, DOWN, buff=0.1)
        txt = VGroup(MathTex(r"V(t) = V_{DD}\big(1 - e^{-t / RC}\big)", font_size=36, color=CTRL),
                     label(r"$R$: \ the driving transistor's resistance", font_size=24, color=GREY_A),
                     label(r"$C$: \ the wire, \ and every gate input it feeds", font_size=24, color=GREY_A),
                     label(r"more gates driven $\Rightarrow$ more $C$ $\Rightarrow$ slower", font_size=26, color=COST),
                     label(r"so designers limit fan-out, \ and insert buffers", font_size=24, color=HEAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28).move_to(RIGHT * 3.6 + DOWN * 0.3)
        with self.voiceover(
            "Where does the delay come from? <bookmark mark='a'/> A wire, and every gate input on it, is a small "
            "capacitor, and the transistor driving it is a resistor. Charging a capacitor through a resistor takes "
            "time: the voltage rises along an exponential, with a time constant R times C. <bookmark mark='b'/> A gate "
            "that drives four others has four times the load, and takes four times as long to reach the threshold. "
            "<bookmark mark='c'/> So fan-out, the number of inputs a gate drives, costs time, and chip designers limit "
            "it and insert buffers to drive long wires. Today, on the largest chips, the wires are slower than the "
            "gates."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), Create(half))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(keys[0]), FadeIn(txt[0]), FadeIn(txt[1]), FadeIn(txt[2]))
            vo.wait_until("b")
            self.play(Create(curves[1]), Create(curves[2]), FadeIn(keys[1:]), FadeIn(txt[3]))
            vo.wait_until("c")
            self.play(FadeIn(txt[4]))
        self.wait(0.3)
        self.clear_scene()
