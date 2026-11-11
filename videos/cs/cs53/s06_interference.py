from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono

S2 = 1 / math.sqrt(2)


def amp_row(values, width=0.32, gap=0.12, scale=2.4):
    """Signed amplitude bars on one baseline (y = 0), coloured by sign: blue for +, red for -.  Every bar exists even
    when its amplitude is zero, so that one row can be transformed into the next."""
    bars = VGroup()
    for i, a in enumerate(values):
        h = max(abs(a) * scale, 0.002)
        col = DATA if a >= 0 else NO
        r = Rectangle(width=width, height=h, stroke_width=0, fill_color=col,
                      fill_opacity=0.85 if abs(a) > 1e-6 else 0.0)
        r.move_to([i * (width + gap), 0, 0], aligned_edge=DOWN if a >= 0 else UP)
        bars.add(r)
    n = len(values)
    base = Line([-width, 0, 0], [(n - 1) * (width + gap) + width, 0, 0], color=GREY_C, stroke_width=1.5)
    return VGroup(base, bars)


def gate_box(tex, x, y, color=HEAD, side=0.55, size=28):
    sq = Square(side_length=side, stroke_color=color, stroke_width=2.2, fill_color=BG, fill_opacity=1).move_to([x, y, 0])
    return VGroup(sq, MathTex(tex, font_size=size, color=color).move_to(sq))


def oracle_box(x, y_top, y_bot, color=KERN, w=1.0, tex=r"U_f"):
    r = Rectangle(width=w, height=y_top - y_bot + 0.6, stroke_color=color, stroke_width=2.2, fill_color=BG,
                  fill_opacity=1).move_to([x, (y_top + y_bot) / 2, 0])
    return VGroup(r, MathTex(tex, font_size=32, color=color).move_to(r))


def meter(x, y, color=KERN, size=0.55):
    r = Rectangle(width=size + 0.1, height=size, stroke_color=color, stroke_width=2, fill_color=BG,
                  fill_opacity=1).move_to([x, y, 0])
    arc = Arc(radius=0.17, start_angle=PI / 6, angle=2 * PI / 3, color=color, stroke_width=2).move_to([x, y - 0.03, 0])
    return VGroup(r, arc, Line([x, y - 0.12, 0], [x + 0.15, y + 0.13, 0], color=color, stroke_width=2))


def wires(ys, x0, x1):
    return VGroup(*[Line([x0, y, 0], [x1, y, 0], color=GREY_B, stroke_width=2) for y in ys])


class Interference(VoiceoverScene):
    def construct(self):
        self.card()
        self.twice()
        self.kickback()
        self.deutsch()
        self.jozsa()
        self.resource()

    def card(self):
        card = chapter_card(5, r"Interference as a resource", r"Where does a quantum speed-up come from?",
                            lit=(1985, 1992, 1998),
                            extra=((1985, r"Deutsch: \ one query for two values"),
                                   (1992, r"Deutsch and Jozsa: \ $n$ bits"),
                                   (1998, r"Cleve et al.: \ phase kickback")), part=PART)
        with self.voiceover("Chapter five. Interference as a resource. Where does a quantum speed-up come from?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ two paths
    def twice(self):
        head = label(r"A coin flipped twice, \ a Hadamard applied twice", font_size=36).to_edge(UP, buff=0.3)

        def tree(x0, root_tex, mid_tex, leaf_tex, edge_tex, edge_col, dx=1.75):
            ym = 0.55
            root = MathTex(root_tex, font_size=28, color=GREY_A).move_to([x0, ym, 0])
            mids = VGroup(*[MathTex(t, font_size=28, color=GREY_A).move_to([x0 + dx, ym + s * 0.95, 0])
                            for t, s in zip(mid_tex, (1, -1))])
            leaves = VGroup(*[MathTex(t, font_size=28, color=GREY_A).move_to([x0 + 2 * dx, ym + y, 0])
                              for t, y in zip(leaf_tex, (1.42, 0.48, -0.48, -1.42))])
            ends = [(root, mids[0]), (root, mids[1]), (mids[0], leaves[0]), (mids[0], leaves[1]),
                    (mids[1], leaves[2]), (mids[1], leaves[3])]
            edges, tags = VGroup(), VGroup()
            for (a, b), t, c in zip(ends, edge_tex, edge_col):
                ln = Line(a.get_right() + RIGHT * 0.08, b.get_left() + LEFT * 0.08, color=c, stroke_width=2.4)
                edges.add(ln)
                n = ln.copy().rotate(PI / 2).get_unit_vector()
                tags.add(MathTex(t, font_size=22, color=c).move_to(ln.get_center() + 0.2 * (n if n[1] > 0 else -n)))
            return VGroup(root, mids, leaves, edges, tags)

        half = r"\tfrac12"
        coin = tree(-6.3, r"0", [r"0", r"1"], [r"0", r"1", r"0", r"1"], [half] * 6, [GREY_B] * 6)
        amp = r"\tfrac{1}{\sqrt2}"
        had = tree(0.95, r"|0\rangle", [r"|0\rangle", r"|1\rangle"],
                   [r"+\tfrac12\,|0\rangle", r"+\tfrac12\,|1\rangle", r"+\tfrac12\,|0\rangle", r"-\tfrac12\,|1\rangle"],
                   [amp, amp, amp, amp, amp, r"-" + amp], [GREY_B] * 5 + [NO])
        had[2][3].set_color(NO)
        t1 = wrapped_label(r"a fair coin: \ probabilities multiply along a path \ and add across paths", 4.6,
                           font_size=19, color=GREY_A).move_to([-4.55, 2.6, 0])
        t2 = wrapped_label(r"a Hadamard: \ amplitudes multiply and add the same way, \ but they carry signs", 5.6,
                           font_size=19, color=GREY_A).move_to([2.7, 2.6, 0])
        s1 = label(r"$P(0) = \tfrac14 + \tfrac14 = \tfrac12$: \ still a coin flip", font_size=20,
                   color=GREY_A).move_to([-4.55, -1.55, 0])
        s2 = VGroup(label(r"$|0\rangle$: \ $\tfrac12 + \tfrac12 = 1$", font_size=21, color=YES),
                    label(r"$|1\rangle$: \ $\tfrac12 - \tfrac12 = 0$", font_size=21, color=NO)).arrange(
            RIGHT, buff=0.6).move_to([2.7, -1.55, 0])
        d = [MathTex(r"HH|0\rangle", r"=", r"H", r"\tfrac{1}{\sqrt2}(|0\rangle + |1\rangle)", font_size=34),
             MathTex(r"HH|0\rangle", r"=", r"\tfrac12(|0\rangle + |1\rangle)", r"+", r"\tfrac12(|0\rangle - |1\rangle)",
                     font_size=34),
             MathTex(r"HH|0\rangle", r"=", r"|0\rangle", font_size=34, color=YES)]
        for m in d:
            m.move_to([0, -2.45, 0])
        foot = wrapped_label(r"\textbf{interference}: \ the two paths to $|1\rangle$ cancel, \ the two paths to "
                             r"$|0\rangle$ reinforce; \ probabilities, \ never negative, \ cannot do this", 12.4,
                             font_size=19, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Flip a fair coin, then flip it again. "
            "Probabilities multiply along each path and add across paths, and after two flips the outcome is still "
            "a coin flip. <bookmark mark='b'/> Now apply a Hadamard to zero, twice. Amplitudes also multiply along "
            "paths and add across them, but they carry signs. One path to one picks up a minus sign. "
            "<bookmark mark='c'/> So the two paths to one cancel, and the two paths to zero reinforce: the result "
            "is zero, with certainty. <bookmark mark='d'/> The algebra says the same in two lines. That cancellation "
            "is interference, and a randomized algorithm, whose probabilities can only add, cannot do it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(coin[0]), Create(coin[3]), FadeIn(coin[4]), FadeIn(coin[1]), FadeIn(coin[2]),
                      run_time=1.5)
            self.play(FadeIn(s1))
            vo.wait_until("b")
            self.play(FadeIn(t2), FadeIn(had[0]), Create(had[3][:2]), FadeIn(had[4][:2]), FadeIn(had[1]))
            self.play(Create(had[3][2:]), FadeIn(had[4][2:]), FadeIn(had[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(Indicate(had[2][3], color=NO), Indicate(had[2][1], color=WHITE), FadeIn(s2))
            vo.wait_until("d")
            self.play(Write(d[0]))
            self.play(TransformMatchingTex(d[0], d[1]))
            self.play(TransformMatchingTex(d[1], d[2]))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ kickback
    def kickback(self):
        head = label(r"Phase kickback", font_size=36).to_edge(UP, buff=0.3)
        ys = (2.25, 1.35)
        w = wires(ys, -5.6, -2.3)
        box = oracle_box(-3.95, ys[0], ys[1])
        ins = VGroup(MathTex(r"|x\rangle", font_size=30, color=DATA), MathTex(r"|y\rangle", font_size=30, color=DATA))
        outs = VGroup(MathTex(r"|x\rangle", font_size=30, color=DATA),
                      MathTex(r"|y \oplus f(x)\rangle", font_size=30, color=DATA))
        ins2 = VGroup(MathTex(r"|x\rangle", font_size=30, color=DATA), MathTex(r"|-\rangle", font_size=30, color=LAM))
        outs2 = VGroup(MathTex(r"(-1)^{f(x)}|x\rangle", font_size=30, color=HEAD),
                       MathTex(r"|-\rangle", font_size=30, color=LAM))
        for grp, side in ((ins, LEFT), (outs, RIGHT), (ins2, LEFT), (outs2, RIGHT)):
            for m, y in zip(grp, ys):
                m.next_to([-5.6 if side is LEFT else -2.3, y, 0], side, buff=0.12)
        defn = wrapped_label(r"the oracle is reversible: \ it XORs $f(x)$ into a target, \ built by chapter 1's "
                             r"compute, \ copy, \ uncompute, \ so it leaves no garbage behind", 5.0, font_size=19,
                             color=GREY_A).move_to([4.1, 1.8, 0])
        rows = VGroup(
            MathTex(r"U_f|x\rangle|-\rangle", r"=", r"|x\rangle\,\tfrac{1}{\sqrt2}\big(|f(x)\rangle - |1 \oplus f(x)"
                    r"\rangle\big)", font_size=30),
            MathTex(r"f(x) = 0:", r"\quad", r"|x\rangle\,\tfrac{1}{\sqrt2}\big(|0\rangle - |1\rangle\big)", r"=",
                    r"+|x\rangle|-\rangle", font_size=30),
            MathTex(r"f(x) = 1:", r"\quad", r"|x\rangle\,\tfrac{1}{\sqrt2}\big(|1\rangle - |0\rangle\big)", r"=",
                    r"-|x\rangle|-\rangle", font_size=30),
            MathTex(r"U_f|x\rangle|-\rangle", r"=", r"(-1)^{f(x)}", r"|x\rangle|-\rangle", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([-1.6, -0.95, 0])
        rows[3][2].set_color(HEAD)
        whys = VGroup(label(r"$|-\rangle = \tfrac{1}{\sqrt2}(|0\rangle - |1\rangle)$", font_size=18, color=GREY_B),
                      label(r"nothing flips", font_size=18, color=GREY_B),
                      label(r"the two terms swap: \ a minus sign", font_size=18, color=GREY_B),
                      label(r"the target is unchanged", font_size=18, color=HEAD))
        wx0 = max(rows.get_right()[0] + 0.4, 2.3)
        for wl, r in zip(whys, rows):
            wl.move_to([wx0 + wl.width / 2, r.get_y(), 0])
        foot = wrapped_label(r"the answer has moved from the target into the \textbf{phase} of the input: \ invisible "
                             r"on one basis state, \ but a relative sign in a superposition, \ and signs interfere",
                             12.4, font_size=19, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "First we need the function as a gate. <bookmark mark='a'/> The "
            "oracle maps x and y to x and y exclusive-or f of x. It is reversible, and chapter one's compute, copy, "
            "uncompute builds it from any classical circuit without leaving garbage behind. "
            "<bookmark mark='b'/> Now feed the target the minus state. <bookmark mark='c'/> If f of x is zero, nothing "
            "flips. If f of x is one, the two terms of the minus state swap places, which is the same state times "
            "minus one. <bookmark mark='d'/> Either way the target comes out unchanged, and the input has picked up "
            "a sign, minus one to the f of x. The answer has been kicked back into the phase. On a single basis state "
            "a sign is invisible, but in a superposition it is a relative sign, and relative signs interfere."
        ) as vo:
            self.play(FadeIn(head), Create(w), FadeIn(box), FadeIn(ins))
            vo.wait_until("a")
            self.play(FadeIn(outs), FadeIn(defn))
            vo.wait_until("b")
            self.play(ReplacementTransform(ins, ins2), FadeOut(outs))
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[0].copy(), rows[3]), FadeIn(whys[3]), FadeIn(outs2))
            self.play(Circumscribe(rows[3][2], color=HEAD), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Deutsch
    def deutsch(self):
        head = label(r"Deutsch's problem: \ is $f(0) = f(1)$?", font_size=36).to_edge(UP, buff=0.3)
        ys = (2.25, 1.35)
        w = wires(ys, -6.0, -1.5)
        kets = VGroup(MathTex(r"|0\rangle", font_size=28, color=GREY_A).next_to([-6.0, ys[0], 0], LEFT, buff=0.1),
                      MathTex(r"|1\rangle", font_size=28, color=GREY_A).next_to([-6.0, ys[1], 0], LEFT, buff=0.1))
        gates = VGroup(gate_box(r"H", -5.25, ys[0]), gate_box(r"H", -5.25, ys[1]), oracle_box(-4.0, ys[0], ys[1]),
                       gate_box(r"H", -2.75, ys[0]), meter(-1.9, ys[0]))
        cap = label(r"one query", font_size=19, color=KERN).next_to(gates[2], DOWN, buff=0.12)
        marks = VGroup()
        for k, x in enumerate((-4.62, -3.38, -2.25)):
            marks.add(VGroup(DashedLine([x, ys[0] + 0.45, 0], [x, ys[1] - 0.45, 0], color=GREY_D, dash_length=0.06),
                             label(f"{k + 1}", font_size=18, color=GREY_A).move_to([x, ys[0] + 0.62, 0])))
        rows = VGroup(
            MathTex(r"\mathbf{1}\quad", r"\tfrac{1}{\sqrt2}\big(|0\rangle + |1\rangle\big)", r"|-\rangle",
                    font_size=28),
            MathTex(r"\mathbf{2}\quad",
                    r"\tfrac{1}{\sqrt2}\big((-1)^{f(0)}|0\rangle + (-1)^{f(1)}|1\rangle\big)", r"|-\rangle",
                    font_size=28),
            MathTex(r"=\pm", r"\tfrac{1}{\sqrt2}\big(|0\rangle + (-1)^{f(0) \oplus f(1)}|1\rangle\big)", r"|-\rangle",
                    font_size=28),
            MathTex(r"\mathbf{3}\quad", r"\pm\,|f(0) \oplus f(1)\rangle", r"|-\rangle", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        rows.move_to([0, 0.85, 0]).shift(RIGHT * (-0.55 - rows.get_left()[0]))
        rows[2].shift(RIGHT * 0.45)
        rows[3][1].set_color(HEAD)
        for r in (rows[0], rows[1], rows[3]):
            r[0].set_color(GREY_A)
        whys = VGroup(label(r"take out $(-1)^{f(0)}$", font_size=18, color=GREY_B),
                      label(r"$H$: \ $|{+}\rangle \to |0\rangle$, \ $|{-}\rangle \to |1\rangle$", font_size=18,
                            color=GREY_B))
        for wl, r in zip(whys, (rows[2], rows[3])):
            wl.next_to(r, RIGHT, buff=0.35)

        def tile(ftex, kind, col, amps):
            fr = RoundedRectangle(width=3.0, height=2.05, corner_radius=0.1, stroke_color=col, stroke_width=1.6)
            t = MathTex(ftex, font_size=28, color=col)
            k = label(kind, font_size=17, color=col)
            top = VGroup(t, k).arrange(RIGHT, buff=0.25).move_to(fr.get_top() + DOWN * 0.3)
            bars = VGroup()
            for i, a in enumerate(amps):
                h = max(abs(a) * 0.62, 0.002)
                r = Rectangle(width=0.42, height=h, stroke_width=0, fill_color=DATA if a >= 0 else NO,
                              fill_opacity=0.85 if a else 0)
                r.move_to([(i - 0.5) * 0.9, 0, 0], aligned_edge=DOWN if a >= 0 else UP)
                bars.add(r)
            base = Line([-0.9, 0, 0], [0.9, 0, 0], color=GREY_C, stroke_width=1.4)
            names = VGroup(*[MathTex(n, font_size=20, color=GREY_A).move_to([(i - 0.5) * 0.9, 0.2 if a < 0 else -0.2, 0])
                             for i, (n, a) in enumerate(zip((r"|0\rangle", r"|1\rangle"), amps))])
            body = VGroup(base, bars, names).shift(fr.get_center() + DOWN * 0.2)
            return VGroup(fr, top, body)
        tiles = VGroup(tile(r"f(x) = 0", r"constant", DATA, (1, 0)), tile(r"f(x) = 1", r"constant", DATA, (-1, 0)),
                       tile(r"f(x) = x", r"balanced", LAM, (0, 1)), tile(r"f(x) = 1 - x", r"balanced", LAM, (0, -1)))
        tiles.arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.35)
        note_t = label(r"the measured qubit after the circuit, \ for each of the four functions", font_size=18,
                       color=GREY_B).next_to(tiles, UP, buff=0.12)
        hist = wrapped_label(r"Deutsch \ (1985) \ posed the problem; \ this always-correct circuit is from Cleve, \ "
                             r"Ekert, \ Macchiavello and Mosca \ (1998)", 5.3, font_size=18, color=GREY_B)
        hist.next_to(cap, DOWN, buff=0.35).set_x(-3.75)
        with self.voiceover(
            "David Deutsch's problem of 1985 is the first in which interference wins. <bookmark mark='a'/> A function "
            "takes one bit to one bit. Are its two values equal? Classically you must evaluate it twice. "
            "<bookmark mark='b'/> Put the input qubit in an equal superposition and the target in the minus state. "
            "<bookmark mark='c'/> One query kicks both answers into the phases at once. Factor out the first sign, "
            "and what remains has a plus where the values agree and a minus where they differ. "
            "<bookmark mark='d'/> A final Hadamard turns plus into zero and minus into one. <bookmark mark='e'/> "
            "Constant functions always give zero, balanced ones always give one, from a single query. The circuit "
            "never learns either value of f, only the one fact we asked for."
        ) as vo:
            self.play(FadeIn(head), Create(w), FadeIn(kets))
            vo.wait_until("a")
            self.play(FadeIn(gates), FadeIn(cap), FadeIn(hist))
            vo.wait_until("b")
            self.play(FadeIn(marks[0]), Write(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(marks[1]), FadeIn(rows[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[0]))
            vo.wait_until("d")
            self.play(FadeIn(marks[2]), FadeIn(rows[3]), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(FadeIn(note_t), LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25),
                      run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Deutsch-Jozsa
    def jozsa(self):
        dj = load("dj")
        n = dj["n"]
        cases = dj["cases"]
        head = label(r"Deutsch--Jozsa: \ sixteen amplitudes, \ one query", font_size=36).to_edge(UP, buff=0.3)
        W, G = 0.3, 0.11
        anchor = np.array([-6.35, 0.15, 0])

        def row(vals):
            return amp_row(vals, width=W, gap=G, scale=2.2).shift(anchor)
        uni = cases["constant 0"]["uniform"]
        stages = [("constant 0", "after_oracle"), ("constant 0", "final"), ("balanced (top bit)", "after_oracle"),
                  ("balanced (top bit)", "final"), ("balanced (parity)", "after_oracle"),
                  ("balanced (parity)", "final")]
        rows_ = [row(uni)] + [row(cases[c][k]) for c, k in stages]
        b0 = rows_[0]
        xs = [b.get_x() for b in b0[1]]
        ends = VGroup(*[mono(format(i, "04b"), size=16, color=GREY_A).move_to([xs[i], -0.7, 0]) for i in (0, 8, 15)])
        names = {"constant 0": r"$f = 0$: \ constant", "balanced (top bit)": r"$f(x) =$ the top bit: \ balanced",
                 "balanced (parity)": r"$f(x) =$ the parity of $x$: \ balanced"}
        cy = -1.2
        caps = [label(r"$H$ on all four qubits: \ sixteen equal amplitudes", font_size=19, color=GREY_A)]
        for c, k in stages:
            what = r"after the oracle" if k == "after_oracle" else r"after $H$ again"
            caps.append(label(names[c] + r", \ " + what, font_size=19, color=DATA if c.startswith("c") else LAM))
        for c in caps:
            c.move_to([b0.get_x(), cy, 0])
        rows = VGroup(
            MathTex(r"H^{\otimes n}|x\rangle", r"=", r"\frac{1}{\sqrt N}\sum_z (-1)^{x \cdot z}|z\rangle", font_size=28),
            MathTex(r"\langle 0\cdots0|\,\psi\rangle", r"=", r"\frac{1}{N}\sum_x (-1)^{f(x)}", font_size=28),
            MathTex(r"=", r"\pm 1", r"\text{ (constant)}, \quad", r"0", r"\text{ (balanced)}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([4.0, 1.25, 0])
        rows.shift(RIGHT * (1.25 - rows.get_left()[0]))
        rows[2][1].set_color(DATA)
        rows[2][3].set_color(LAM)
        whys = VGroup(label(r"$x \cdot z$: \ bitwise AND, \ then parity", font_size=18, color=GREY_B),
                      label(r"the all-zeros amplitude is the average sign", font_size=18, color=GREY_B))
        whys[0].next_to(rows[0], DOWN, buff=0.08).align_to(rows[0], LEFT)
        whys[1].next_to(rows[1], DOWN, buff=0.08).align_to(rows[1], LEFT)
        rows[1].shift(DOWN * 0.15)
        whys[1].shift(DOWN * 0.15)
        rows[2].next_to(whys[1], DOWN, buff=0.25).align_to(rows[1], LEFT)
        p0 = cases["constant 0"]["p_zero"]
        pb = cases["balanced (top bit)"]["p_zero"]
        tab = grid_table([r"function", r"$P(0000)$"],
                         [[r"constant", f"{p0 + 0.0:.3f}"], [r"balanced", f"{abs(pb):.3f}"]],
                         widths=[2.2, 1.6], row_h=0.42, font_size=19, mono_cols=())
        tab.cells[1][1].set_color(DATA)
        tab.cells[2][1].set_color(LAM)
        tab.next_to(rows[2], DOWN, buff=0.4).align_to(rows, LEFT)
        src = note(r"our simulator, \ $n = 4$", font_size=16).next_to(tab, RIGHT, buff=0.3).align_to(tab, DOWN)
        foot = wrapped_label(rf"a deterministic classical algorithm must look at {dj['classical_worst_queries']} of "
                             rf"the {2 ** n} values in the worst case, \ $2^{{n-1}} + 1$, \ before it can be sure; \ "
                             r"the quantum circuit asks once \ (Deutsch and Jozsa, \ 1992)", 12.4, font_size=19,
                             color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 1992 Deutsch and Richard Jozsa scaled this up to n bits. The function is promised to be either "
            "constant, or balanced, zero on exactly half its inputs. <bookmark mark='a'/> Hadamards on four qubits "
            "give sixteen equal amplitudes. <bookmark mark='b'/> The oracle stamps a sign on each, and Hadamards "
            "again bring them together. For a constant function every sign agrees, and all the amplitude piles onto "
            "zero zero zero zero. <bookmark mark='c'/> For a balanced function, the signs cancel exactly there, and "
            "the amplitude lands somewhere else, a different place for each function. "
            "<bookmark mark='d'/> Why? The amplitude of all zeros after the last Hadamards is the average of the "
            "signs: plus or minus one if f is constant, zero if it is balanced. <bookmark mark='e'/> Our simulator "
            "measures all zeros with probability one or zero. A deterministic classical algorithm would need nine "
            "evaluations in the worst case; this needs one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ends))
            vo.wait_until("a")
            self.play(FadeIn(b0), FadeIn(caps[0]))
            cur, cap = b0, caps[0]
            vo.wait_until("b")
            for i in (1, 2):
                self.play(ReplacementTransform(cur, rows_[i]), ReplacementTransform(cap, caps[i]), run_time=1.2)
                cur, cap = rows_[i], caps[i]
                self.wait(0.6)
            vo.wait_until("c")
            for i in (3, 4, 5, 6):
                self.play(ReplacementTransform(cur, rows_[i]), ReplacementTransform(cap, caps[i]), run_time=1.0)
                cur, cap = rows_[i], caps[i]
                self.wait(0.4)
            vo.wait_until("d")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(tab), FadeIn(src))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the recipe, and its limits
    def resource(self):
        dj = load("dj")
        head = label(r"Interference, \ not parallelism", font_size=36).to_edge(UP, buff=0.3)

        def step(title, body, col):
            fr = RoundedRectangle(width=3.6, height=1.35, corner_radius=0.12, stroke_color=col, stroke_width=1.8)
            t = label(title, font_size=22, color=col)
            b = wrapped_label(body, 3.3, font_size=18, color=GREY_A)
            VGroup(t, b).arrange(DOWN, buff=0.12).move_to(fr)
            return VGroup(fr, t, b)
        steps = VGroup(step(r"1. \ spread", r"Hadamards: \ every input at once", DATA),
                       step(r"2. \ mark", r"the oracle writes answers into phases", KERN),
                       step(r"3. \ interfere", r"a transform makes wrong answers cancel", YES)).arrange(RIGHT, buff=0.7)
        steps.next_to(head, DOWN, buff=0.4)
        arrows = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.08, color=GREY_B,
                                stroke_width=2.5, max_tip_length_to_length_ratio=0.3) for i in range(2)])
        # left: measuring straight after the oracle
        vals = dj["cases"]["balanced (parity)"]["after_oracle"]
        bars = amp_row(vals, width=0.22, gap=0.08, scale=1.6)
        bars.move_to([-3.6, -0.45, 0])
        bt = label(r"after the oracle: \ a sign on each of sixteen inputs", font_size=18, color=GREY_B).next_to(
            bars, UP, buff=0.25)
        ill = note(r"the measured input: \ illustrative", font_size=16).next_to(bars, DOWN, buff=0.12)
        pick = 11
        ring = SurroundingRectangle(bars[1][pick], color=HEAD, buff=0.06, stroke_width=2.5)
        lt = wrapped_label(r"measure right after the oracle: \ one random $x$ and its $f(x)$, \ no better than one "
                           r"classical query", 5.6, font_size=19, color=WHITE).next_to(ill, DOWN, buff=0.3)
        lt.set_x(-3.6)
        # right: randomized classical
        rr = VGroup(
            label(r"a randomized classical test:", font_size=20, color=GREY_A),
            label(r"query $k$ random inputs; \ if they all agree, \ say constant", font_size=19, color=GREY_A),
            MathTex(r"P(\text{a balanced } f \text{ fools it})", r"\le", r"2 \cdot 2^{-k}", r"=", r"2^{1-k}",
                    font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, -0.5, 0])
        rr[2][4].set_color(NO)
        rt = wrapped_label(r"so Deutsch--Jozsa's advantage is only over \textit{certainty}: \ allow a small error and "
                           r"a few classical queries do; \ an exponential gap against randomized algorithms needs "
                           r"the next chapter", 5.8, font_size=19, color=HEAD).next_to(rr, DOWN, buff=0.35)
        rt.align_to(rr, LEFT)
        div = DashedLine([0.3, 0.6, 0], [0.3, -3.4, 0], color=GREY_D, dash_length=0.08)
        with self.voiceover(
            "This is the recipe for the next five chapters. <bookmark mark='a'/> Spread out over every input with "
            "Hadamards; mark each input's answer in its phase with the oracle; then apply a transform under which the "
            "wrong answers cancel. <bookmark mark='b'/> It is tempting to say a quantum computer tries every answer in "
            "parallel. But measure right after the oracle and you get one random input and its value, no better than "
            "one classical query. The gain is all in the third step. <bookmark mark='c'/> And we should be honest "
            "about Deutsch–Jozsa. Its advantage is over certainty. A randomized classical test that checks k random "
            "inputs is fooled by a balanced function with probability at most two to the one minus k. Ten queries, "
            "and it is almost never wrong. An exponential gap against randomized algorithms needs a harder problem, "
            "and Daniel Simon found one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(FadeIn(steps[0]), GrowArrow(arrows[0]), FadeIn(steps[1]), GrowArrow(arrows[1]),
                                  FadeIn(steps[2]), lag_ratio=0.35), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(bars), FadeIn(bt), Create(div))
            self.play(Create(ring), bars[1][pick].animate.set_fill(HEAD, opacity=1), FadeIn(lt), FadeIn(ill))
            vo.wait_until("c")
            self.play(FadeIn(rr[:2]))
            self.play(Write(rr[2]))
            self.play(FadeIn(rt))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM, NO, YES, BG, DATA, HEAD, mono)
