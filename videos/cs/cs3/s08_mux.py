from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, NO, ONE, PART, WIRE, YES, ZERO, gate, load,
                                  wire)


def mux_symbol(h=1.0, w=0.55, color=CTRL):
    """A 2-to-1 multiplexer: a trapezoid, inputs on the left (0 on top), output on the right, select below."""
    t = Polygon([-w / 2, h / 2, 0], [-w / 2, -h / 2, 0], [w / 2, -h / 3, 0], [w / 2, h / 3, 0], stroke_color=color,
                stroke_width=3, fill_color="#151B26", fill_opacity=1)
    z = MathTex("0", font_size=18, color=GREY_B).move_to(t.get_left() + RIGHT * 0.12 + UP * h * 0.25)
    o = MathTex("1", font_size=18, color=GREY_B).move_to(t.get_left() + RIGHT * 0.12 + DOWN * h * 0.25)
    g = VGroup(t, z, o)
    g.i0 = lambda: t.get_left() + UP * h * 0.25
    g.i1 = lambda: t.get_left() + DOWN * h * 0.25
    g.out = lambda: t.get_right()
    g.sel = lambda: (t.get_vertices()[1] + t.get_vertices()[2]) / 2
    return g


class Mux(VoiceoverScene):
    def construct(self):
        self.card()
        self.mux2()
        self.universal()
        self.expansion()
        self.lut()
        self.decoder()

    def card(self):
        card = chapter_card(7, r"Choosing with gates", r"Can a circuit look up an answer?", part=PART)
        with self.voiceover("Chapter seven. Choosing with gates."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def mux2(self):
        head = label(r"The multiplexer: \ a switch controlled by a bit", font_size=36).to_edge(UP, buff=0.35)
        m = mux_symbol(h=1.8, w=1.0).scale(1.0).move_to(LEFT * 2.6 + DOWN * 0.2)
        a = np.array([-5.4, m.i0()[1], 0])
        b = np.array([-5.4, m.i1()[1], 0])
        s = np.array([m.sel()[0], -2.4, 0])
        wa, wb = Line(a, m.i0(), color=WIRE, stroke_width=3), Line(b, m.i1(), color=WIRE, stroke_width=3)
        ws = Line(s, m.sel(), color=WIRE, stroke_width=3)
        wo = Line(m.out(), m.out() + RIGHT * 1.4, color=WIRE, stroke_width=3)
        la = MathTex("a", font_size=34, color=DATA).next_to(a, LEFT, buff=0.1)
        lb = MathTex("b", font_size=34, color=DATA).next_to(b, LEFT, buff=0.1)
        ls = MathTex("s", font_size=34, color=HEAD).next_to(s, DOWN, buff=0.1)
        lo = MathTex("y", font_size=34, color=YES).next_to(wo, RIGHT, buff=0.1)
        eq = MathTex(r"y = \bar s\, a + s\, b", font_size=42, color=YES).move_to(RIGHT * 3.4 + UP * 1.4)
        txt = VGroup(label(r"$s = 0$: \ $y = a$", font_size=30, color=GREY_A),
                     label(r"$s = 1$: \ $y = b$", font_size=30, color=GREY_A),
                     note(r"two ANDs, \ an OR, \ a NOT: \ four gates", font_size=24)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).next_to(eq, DOWN, buff=0.45)
        with self.voiceover(
            "A circuit can choose. <bookmark mark='a'/> A multiplexer has two data inputs, a and b, and a select input s. "
            "When s is zero, the output is a; when s is one, it is b. <bookmark mark='b'/> In gates: not s and a, or s "
            "and b. Four gates. <bookmark mark='c'/> Watch it route one input or the other to the output as the select "
            "bit flips. It is the electrical version of an if statement, and it is about to turn out to be universal "
            "too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(m), Create(VGroup(wa, wb, ws, wo)), FadeIn(VGroup(la, lb, ls, lo)))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(txt))
            vo.wait_until("c")
            for sv in (0, 1, 0, 1):
                self.play(ws.animate.set_stroke(ONE if sv else ZERO), wa.animate.set_stroke(ONE if not sv else WIRE),
                          wb.animate.set_stroke(ONE if sv else WIRE), wo.animate.set_stroke(ONE), run_time=0.6)
                self.wait(0.3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def universal(self):
        head = label(r"A multiplexer, \ with constants, \ is complete", font_size=36).to_edge(UP, buff=0.35)
        items = [(r"\bar x", "1", "0", "x"), (r"x\,y", "0", "y", "x"), (r"x + y", "y", "1", "x")]
        groups = VGroup()
        for name, a0, a1, sel in items:
            m = mux_symbol(h=1.3, w=0.7)
            i0 = MathTex(a0, font_size=32, color=YES if a0 in "01" else DATA).next_to(m.i0(), LEFT, buff=0.35)
            i1 = MathTex(a1, font_size=32, color=YES if a1 in "01" else DATA).next_to(m.i1(), LEFT, buff=0.35)
            w0 = Line(i0.get_right() + RIGHT * 0.05, m.i0(), color=WIRE, stroke_width=3)
            w1 = Line(i1.get_right() + RIGHT * 0.05, m.i1(), color=WIRE, stroke_width=3)
            ws = Line(m.sel() + DOWN * 0.6, m.sel(), color=WIRE, stroke_width=3)
            sl = MathTex(sel, font_size=30, color=HEAD).next_to(ws, DOWN, buff=0.08)
            out = Line(m.out(), m.out() + RIGHT * 0.5, color=WIRE, stroke_width=3)
            ol = MathTex(name, font_size=32, color=CTRL).next_to(out, RIGHT, buff=0.1)
            groups.add(VGroup(m, i0, i1, w0, w1, ws, sl, out, ol))
        groups.arrange(RIGHT, buff=1.2).move_to(UP * 0.3)
        lab = VGroup(*[note(t, font_size=22).next_to(g_, DOWN, buff=0.6) for t, g_ in zip(
            (r"$x$ ? 0 : 1", r"$x$ ? $y$ : 0", r"$x$ ? 1 : $y$"), groups)])
        why = label(r"NOT, AND, OR \ $\Rightarrow$ \ everything; \ Post's test agrees, \ once the constants are "
                    r"allowed", font_size=26, color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A multiplexer can imitate the basic gates. <bookmark mark='a'/> Select with x, and feed in one and zero: "
            "if x then zero else one, which is not x. <bookmark mark='b'/> Feed in zero and y: if x then y else zero, "
            "which is x and y. <bookmark mark='c'/> Feed in y and one: if x then one else y, which is x or y. So a "
            "multiplexer, given the constants zero and one, is complete on its own, and Post's test agrees. This is why "
            "some chip families were built entirely from multiplexers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(groups[0]), FadeIn(lab[0]))
            vo.wait_until("a")
            self.play(Circumscribe(groups[0], color=HEAD))
            for mk, g_, l_ in zip("bc", groups[1:], lab[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(g_), FadeIn(l_))
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def expansion(self):
        head = label(r"Shannon expansion", font_size=38).to_edge(UP, buff=0.35)
        f = MathTex(r"f(x, y, z) = \bar x\, f(0, y, z) + x\, f(1, y, z)", font_size=40, color=YES).next_to(head, DOWN,
                                                                                                    buff=0.4)
        expl = label(r"a function of $n$ inputs \ $=$ \ a multiplexer choosing between two functions of $n - 1$",
                     font_size=26, color=GREY_A).next_to(f, DOWN, buff=0.3)
        tree = self.tree([1, 0, 0, 1, 0, 1, 1, 0], LEFT * 0.5 + DOWN * 1.15)
        tl = note(r"keep expanding: \ a tree of multiplexers \ whose leaves are the truth table", font_size=22).next_to(
            tree, DOWN, buff=0.2)
        with self.voiceover(
            "Shannon also noticed this identity. <bookmark mark='a'/> Any function of x and other inputs equals: if x "
            "is zero, the function with x set to zero; if x is one, the function with x set to one. That is a "
            "multiplexer, choosing between two simpler functions. <bookmark mark='b'/> Expand those the same way, and "
            "again, until no inputs are left. What remains at the leaves are constants, zeros and ones: the truth "
            "table itself, read off by a tree of multiplexers driven by the inputs."
        ) as vo:
            self.play(FadeIn(head), Write(f), FadeIn(expl), FadeIn(tree, lag_ratio=0.05), FadeIn(tl), run_time=2.4)
            vo.wait_until("a")
            self.play(Circumscribe(f, color=HEAD))
            vo.wait_until("b")
            self.play(Circumscribe(tree, color=HEAD))
        self.wait(0.3)
        self.clear_scene()

    def tree(self, bits, origin, h=0.62, dx=1.6):
        """A three-level tree of 2-to-1 muxes reading eight leaf bits (index = 4x + 2y + z)."""
        o = np.asarray(origin, float)
        g = VGroup()
        levels = []
        # level 0 (leaves side): 4 muxes selected by z
        xs = [o[0] - 2 * dx, o[0] - dx, o[0]]
        prev_outs = []
        leaves = VGroup()
        muxes = []
        for lvl, n in enumerate((4, 2, 1)):
            row = []
            for i in range(n):
                y = o[1] - (i - (n - 1) / 2) * (h * 2 ** (lvl + 1)) * 0.95
                m = mux_symbol(h=h, w=0.42).move_to([xs[lvl], y, 0])
                row.append(m)
                g.add(m)
            muxes.append(row)
        for i, m in enumerate(muxes[0]):
            for j, pin in enumerate((m.i0, m.i1)):
                v = bits[2 * i + j]
                t = MathTex(str(v), font_size=26, color=YES if v else GREY_B).move_to(pin() + LEFT * 0.55)
                leaves.add(t)
                g.add(Line(t.get_right() + RIGHT * 0.05, pin(), color=WIRE, stroke_width=2.5))
        for lvl in (1, 2):
            for i, m in enumerate(muxes[lvl]):
                g.add(wire(muxes[lvl - 1][2 * i].out(), m.i0()), wire(muxes[lvl - 1][2 * i + 1].out(), m.i1()))
        out = Line(muxes[2][0].out(), muxes[2][0].out() + RIGHT * 0.6, color=WIRE, stroke_width=3)
        g.add(out, leaves)
        for lvl, var in enumerate(("z", "y", "x")):
            g.add(MathTex(var, font_size=28, color=HEAD).next_to(muxes[lvl][0], DOWN, buff=0.35))
        g.leaves = leaves
        g.muxes = muxes
        return g

    # ------------------------------------------------------------------
    def lut(self):
        head = label(r"A lookup table: \ how an FPGA computes", font_size=38).to_edge(UP, buff=0.35)
        maj = [1 if bin(k).count("1") >= 2 else 0 for k in range(8)]
        par = [bin(k).count("1") % 2 for k in range(8)]
        # leaf order in the tree is index 4x + 2y + z read top to bottom
        tree = self.tree(maj, LEFT * 1.5 + DOWN * 0.4)
        cfg = label(r"8 memory bits \ $=$ \ any function of 3 inputs", font_size=28, color=CTRL).move_to(
            RIGHT * 0.6 + UP * 1.6, aligned_edge=LEFT)
        n1 = label(r"store majority's truth table: \ it computes majority", font_size=24, color=GREY_A).next_to(
            cfg, DOWN, buff=0.4).align_to(cfg, LEFT)
        n2 = label(r"rewrite the bits: \ now it computes parity", font_size=24, color=GREY_A).next_to(
            n1, DOWN, buff=0.3).align_to(cfg, LEFT)
        fp = VGroup(label(r"an FPGA: \ hundreds of thousands of 6-input LUTs \\ ($2^6 = 64$ bits each), \ and "
                          r"programmable wires between them", font_size=23, color=HEAD),
                    note(r"hardware you can rewrite in seconds: \\ prototypes, \ networking, \ the cloud's accelerators",
                         font_size=21)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(n2, DOWN, buff=0.5).align_to(
            cfg, LEFT)
        with self.voiceover(
            "Now turn that around. <bookmark mark='a'/> Build the tree of multiplexers in hardware, and instead of "
            "constants at the leaves, put eight bits of memory. Whatever eight bits you store, the circuit computes "
            "that truth table. <bookmark mark='b'/> Store majority's table, and it is a majority gate. "
            "<bookmark mark='c'/> Rewrite the bits, and the same circuit computes parity. <bookmark mark='d'/> This is "
            "a lookup table, and it is how a field-programmable gate array works: hundreds of thousands of six-input "
            "lookup tables, sixty-four bits each, with programmable wiring between them. Hardware you can change in a "
            "few seconds, used for prototyping chips, for network equipment, and for accelerators in data centres."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tree, lag_ratio=0.03), FadeIn(cfg), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(n1), *[Indicate(t, color=HEAD) for t in tree.leaves])
            vo.wait_until("c")
            self.play(*[Transform(t, MathTex(str(v), font_size=26, color=YES if v else GREY_B).move_to(t))
                        for t, v in zip(tree.leaves, par)], FadeIn(n2))
            vo.wait_until("d")
            self.play(FadeIn(fp))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decoder(self):
        d = load("blocks")
        rows = {r["name"]: r for r in d["rows"]}
        head = label(r"Decoders: \ a number in, \ one wire out", font_size=38).to_edge(UP, buff=0.35)
        outs = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.9, color=WIRE, stroke_width=3),
                               MathTex(rf"y_{k}", font_size=26, color=GREY_B)).arrange(RIGHT, buff=0.1)
                        for k in range(8)]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(LEFT * 1.4)
        box = RoundedRectangle(width=1.6, height=outs.height + 0.4, corner_radius=0.12, stroke_color=CTRL,
                               stroke_width=3, fill_color="#151B26", fill_opacity=1).next_to(outs, LEFT, buff=0.0)
        bl = label(r"3-to-8", font_size=24, color=CTRL).move_to(box)
        ins = VGroup(*[MathTex(rf"a_{k}", font_size=28, color=DATA) for k in (2, 1, 0)]).arrange(DOWN, buff=0.5).next_to(
            box, LEFT, buff=0.5)
        bits = VGroup(*[MathTex("0", font_size=28, color=GREY_B).next_to(ins[k], LEFT, buff=0.25) for k in range(3)])
        r = rows["3-to-8 decoder"]
        txt = VGroup(label(r"output $k$ is 1 \ exactly when the input is the number $k$", font_size=26, color=GREY_A),
                     label(rf"{r['gates']} gates, \ depth {r['depth']} \ (built and verified)", font_size=26, color=COST),
                     label(r"Pebble uses one to pick which register to write \ (Part 6)", font_size=26, color=HEAD),
                     label(r"the reverse, \ an \textit{encoder}, \ turns one hot wire back into a number: \ chapter 11",
                           font_size=24, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        txt.scale_to_fit_width(6.2).move_to(RIGHT * 3.7 + DOWN * 0.2)
        with self.voiceover(
            "One more choosing circuit, which every memory needs. <bookmark mark='a'/> A decoder takes a number in "
            "binary, here three bits, and lights exactly one of eight output wires: the one with that number. "
            "<bookmark mark='b'/> Count through the inputs and the lit wire walks down. Each output is an and of the "
            "inputs, plain or negated, which is chapter five's normal form, one term per wire. "
            "<bookmark mark='c'/> Pebble uses one to decide which of its sixteen registers to write, and every memory "
            "chip uses one to find the row you asked for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(box), FadeIn(bl), FadeIn(outs), FadeIn(ins), FadeIn(bits))
            vo.wait_until("a")
            self.play(FadeIn(txt[0]))
            vo.wait_until("b")
            for k in range(8):
                new_bits = [MathTex(str((k >> s) & 1), font_size=28, color=YES if (k >> s) & 1 else GREY_B).move_to(
                    bits[i]) for i, s in enumerate((2, 1, 0))]
                self.play(*[Transform(bits[i], new_bits[i]) for i in range(3)],
                          *[outs[j][0].animate.set_stroke(ONE if j == k else WIRE) for j in range(8)], run_time=0.45)
            self.play(FadeIn(txt[1]))
            vo.wait_until("c")
            self.play(FadeIn(txt[2]), FadeIn(txt[3]))
        self.wait(0.3)
        self.clear_scene()
