from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, WIRE, YES, axis_plot, gate, load,
                                  wire)


def fa_box(label_tex=r"\text{FA}", w=1.0, h=1.0):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=CTRL, stroke_width=2.5, fill_color=BG,
                           fill_opacity=1)
    t = MathTex(label_tex, font_size=26, color=CTRL).move_to(box)
    g = VGroup(box, t)
    g.a = lambda: box.get_top() + LEFT * w * 0.22
    g.b = lambda: box.get_top() + RIGHT * w * 0.22
    g.cin = lambda: box.get_right()
    g.cout = lambda: box.get_left()
    g.s = lambda: box.get_bottom()
    return g


def tt_table(header, rows, font_size=26, col_colors=None):
    cols = len(header)
    g = VGroup()
    hdr = VGroup(*[MathTex(h, font_size=font_size, color=GREY_B) for h in header])
    g.add(hdr)
    for r in rows:
        g.add(VGroup(*[MathTex(str(v), font_size=font_size, color=(col_colors[j] if col_colors else GREY_A))
                       for j, v in enumerate(r)]))
    for i, row in enumerate(g):
        for j, m in enumerate(row):
            m.move_to([0.62 * j, -0.4 * i, 0])
    line = Line([-0.3, -0.2, 0], [0.62 * (cols - 1) + 0.3, -0.2, 0], color=GREY_D, stroke_width=1.5)
    return VGroup(g, line)


class Ripple(VoiceoverScene):
    def construct(self):
        self.card()
        self.by_hand()
        self.half_full()
        self.chain()
        self.induction()
        self.slow()

    def card(self):
        card = chapter_card(3, r"Adding, one bit at a time", r"How do gates add two numbers?", lit=(1937,), part=PART)
        with self.voiceover("Chapter three. Adding, one bit at a time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def by_hand(self):
        head = label(r"Binary addition, \ by hand", font_size=38).to_edge(UP, buff=0.4)
        a, b = "1011", "0110"
        s = format(int(a, 2) + int(b, 2), "05b")
        carries = []
        c = 0
        for i in range(3, -1, -1):
            t = int(a[i]) + int(b[i]) + c
            c = t >> 1
            carries.append(c)
        carries = carries[::-1]  # carry out of column i (string order)
        x0, dx = -1.2, 0.75
        rowa = VGroup(*[MathTex(ch, font_size=48, color=DATA).move_to([x0 + dx * (i + 1), 1.0, 0]) for i, ch in enumerate(a)])
        rowb = VGroup(*[MathTex(ch, font_size=48, color=DATA).move_to([x0 + dx * (i + 1), 0.2, 0]) for i, ch in enumerate(b)])
        plus = MathTex("+", font_size=48, color=GREY_B).move_to([x0, 0.2, 0])
        bar = Line([x0 - 0.3, -0.25, 0], [x0 + dx * 4.4, -0.25, 0], color=GREY_B)
        rows_ = VGroup(*[MathTex(ch, font_size=48, color=YES).move_to([x0 + dx * i, -0.75, 0]) for i, ch in enumerate(s)])
        cmark = {i: MathTex("1", font_size=28, color=HEAD).move_to([x0 + dx * i, 1.75, 0]) for i in range(1, 4)
                 if carries[i]}  # the carry out of column i, written above column i - 1
        dec = MathTex(r"11 + 6 = 17", font_size=36, color=GREY_A).move_to(RIGHT * 4.0 + UP * 0.2)
        rule = label(r"each column: \ three bits in \ (two digits and a carry), \\ two bits out \ (a sum and a carry)",
                     font_size=26, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Adding binary numbers works exactly like the method from school, with fewer facts to remember. "
            "<bookmark mark='a'/> Eleven plus six: start at the right. One plus zero is one. One plus one is two, "
            "which in binary is one zero: write zero, carry one. Zero plus one plus the carry is two again: write zero, "
            "carry one. One plus zero plus the carry: zero, carry one, and that last carry becomes a new top digit. "
            "Seventeen. <bookmark mark='b'/> Every column does the same small job: three bits come in, the two digits "
            "and the carry, and two bits go out, a sum and a carry for the next column. Build that job once in gates, "
            "copy it n times, and you can add."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rowa), FadeIn(rowb), FadeIn(plus), Create(bar), FadeIn(dec))
            vo.wait_until("a")
            for i in range(3, -1, -1):
                self.play(FadeIn(rows_[i + 1], shift=DOWN * 0.1), run_time=0.5)
                if i in cmark:
                    self.play(FadeIn(cmark[i], shift=UP * 0.1), run_time=0.4)
            if carries[0]:
                self.play(FadeIn(rows_[0], shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def half_full(self):
        head = label(r"The half adder \ and the full adder", font_size=38).to_edge(UP, buff=0.35)
        ht = tt_table([r"a", r"b", r"c", r"s"], [(a, b, a & b, a ^ b) for a in (0, 1) for b in (0, 1)],
                      col_colors=[DATA, DATA, HEAD, YES]).move_to(LEFT * 5.0 + UP * 0.9)
        hx = MathTex(r"s = a \oplus b \qquad c = a\,b", font_size=32, color=CODE).next_to(ht, DOWN, buff=0.35)
        ft = tt_table([r"a", r"b", r"c_{in}", r"c_{out}", r"s"],
                      [(a, b, c, (a + b + c) >> 1, (a + b + c) & 1) for a in (0, 1) for b in (0, 1) for c in (0, 1)],
                      font_size=24, col_colors=[DATA, DATA, HEAD, HEAD, YES]).move_to(LEFT * 0.6 + UP * 0.6)
        fx = VGroup(MathTex(r"s = a \oplus b \oplus c_{in}", font_size=32, color=CODE),
                    MathTex(r"c_{out} = a\,b + (a \oplus b)\,c_{in} = \mathrm{maj}(a, b, c_{in})", font_size=30,
                            color=CODE)).arrange(DOWN, buff=0.15).next_to(ft, DOWN, buff=0.3)
        # the full adder in five gates
        g1 = gate("XOR", size=0.7).move_to([3.6, 1.6, 0])
        g2 = gate("XOR", size=0.7).move_to([5.4, 1.2, 0])
        g3 = gate("AND", size=0.7).move_to([3.6, 0.0, 0])
        g4 = gate("AND", size=0.7).move_to([5.0, -0.3, 0])
        g5 = gate("OR", size=0.7).move_to([6.2, -0.7, 0])
        ins = VGroup(MathTex("a", font_size=26, color=DATA).move_to([2.3, 1.75, 0]),
                     MathTex("b", font_size=26, color=DATA).move_to([2.3, 1.45, 0]),
                     MathTex("c_{in}", font_size=26, color=HEAD).move_to([2.3, 0.9, 0]))
        ws = VGroup(
            Line([2.5, 1.75, 0], g1.inp[0](), color=WIRE, stroke_width=2),
            Line([2.5, 1.45, 0], g1.inp[1](), color=WIRE, stroke_width=2),
            wire([2.85, 1.75, 0], g3.inp[0](), via="v", stroke_width=2),
            wire([3.0, 1.45, 0], g3.inp[1](), via="v", stroke_width=2),
            wire(g1.out(), g2.inp[0](), stroke_width=2),
            wire([2.6, 0.9, 0], g2.inp[1](), stroke_width=2),
            wire([4.55, 1.6, 0], g4.inp[0](), via="v", stroke_width=2),
            wire([4.75, 0.9, 0], g4.inp[1](), via="v", stroke_width=2),
            wire(g3.out(), g5.inp[1](), stroke_width=2),
            wire(g4.out(), g5.inp[0](), stroke_width=2),
        )
        outs = VGroup(MathTex("s", font_size=26, color=YES).next_to(g2.out(), RIGHT, buff=0.1),
                      MathTex("c_{out}", font_size=26, color=HEAD).next_to(g5.out(), RIGHT, buff=0.1))
        fa = VGroup(g1, g2, g3, g4, g5, ins, ws, outs)
        fa.scale(0.9).shift(LEFT * 0.3)
        fl = note(r"five gates: \ two half adders and an OR", font_size=22).next_to(fa, DOWN, buff=0.3)
        with self.voiceover(
            "Start with two bits. <bookmark mark='a'/> Their sum is a two-bit number: the low bit is one when exactly "
            "one input is one, an exclusive-or; the high bit, the carry, is one when both are, an and. That is a half "
            "adder. <bookmark mark='b'/> A column in the middle of a sum has three inputs, the two digits and the "
            "carry from the right. The sum bit is the exclusive-or of all three: it is one when an odd number of them "
            "are. The carry out is one when at least two of them are: the majority function from Part 3. "
            "<bookmark mark='c'/> In gates: one half adder adds a and b, a second adds the carry in, and an or "
            "combines the two possible carries, which can never both be one. Five gates. This is the full adder, and "
            "it is the atom of computer arithmetic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ht))
            vo.wait_until("a")
            self.play(Indicate(ht, scale_factor=1.03), FadeIn(hx))
            vo.wait_until("b")
            self.play(FadeIn(ft), FadeIn(fx))
            vo.wait_until("c")
            self.play(FadeIn(fa, lag_ratio=0.05), FadeIn(fl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chain_mobs(self, n=8, y=0.4):
        boxes = VGroup(*[fa_box() for _ in range(n)]).arrange(LEFT, buff=0.55).move_to([0, y, 0])
        cw = VGroup(*[Line(boxes[i].cout(), boxes[i + 1].cin(), color=WIRE, stroke_width=3) for i in range(n - 1)])
        cin = Line(boxes[0].cin() + RIGHT * 0.45, boxes[0].cin(), color=WIRE, stroke_width=3)
        cout = Line(boxes[-1].cout(), boxes[-1].cout() + LEFT * 0.45, color=WIRE, stroke_width=3)
        return boxes, cw, cin, cout

    def chain(self):
        head = label(r"The ripple-carry adder", font_size=38).to_edge(UP, buff=0.35)
        n = 8
        boxes, cw, cin, cout = self.chain_mobs(n)
        ab = VGroup()
        for i, bx in enumerate(boxes):
            ab.add(MathTex(rf"a_{i}", font_size=24, color=DATA).next_to(bx.a(), UP, buff=0.12),
                   MathTex(rf"b_{i}", font_size=24, color=DATA).next_to(bx.b(), UP, buff=0.12),
                   MathTex(rf"s_{i}", font_size=24, color=YES).next_to(bx.s(), DOWN, buff=0.12))
        ends = VGroup(MathTex(r"c_{in}", font_size=24, color=HEAD).next_to(cin, RIGHT, buff=0.08),
                      MathTex(r"c_{out}", font_size=24, color=HEAD).next_to(cout, LEFT, buff=0.08))
        cost = label(r"$n$ full adders: \ $5n$ gates", font_size=28, color=COST).to_edge(DOWN, buff=1.2)
        sub = MathTex(r"a - b = a + \bar b + 1: \quad \text{invert } b, \ \text{set } c_{in} = 1", font_size=32,
                      color=CODE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Now copy the full adder, once per bit, and chain them. <bookmark mark='a'/> Bit zero on the right takes "
            "a carry in; each adder's carry out becomes the next one's carry in; the last carry out is the top bit of "
            "the answer, or, in a register of fixed width, unsigned overflow. <bookmark mark='b'/> This is the ripple-carry "
            "adder: n full adders, five n gates. <bookmark mark='c'/> And the same carry chain can subtract. Since minus b is not b "
            "plus one, a minus b is a plus not b plus one: put an exclusive-or on each b input to invert it, and feed "
            "a one into the carry. One circuit, two operations, signed or unsigned."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(boxes, cw, cin, cout, ab, ends)))
            vo.wait_until("a")
            self.play(Indicate(cw, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(cost))
            vo.wait_until("c")
            self.play(FadeIn(sub))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def induction(self):
        head = label(r"Why it is right: \ induction on the bits", font_size=38).to_edge(UP, buff=0.35)
        claim = MathTex(r"\sum_{i<k} s_i\, 2^i \; + \; c_k\, 2^k \;=\; \sum_{i<k} (a_i + b_i)\, 2^i \; + \; c_{in}",
                        font_size=40, color=CODE).move_to(UP * 1.6)
        cap = label(r"the claim, \ for the first $k$ adders", font_size=26, color=GREY_A).next_to(claim, DOWN, buff=0.25)
        base = MathTex(r"k = 0: \quad c_0 = c_{in}", font_size=34, color=GREY_A).move_to(LEFT * 3.4 + DOWN * 0.4)
        step = VGroup(MathTex(r"k \to k + 1:", font_size=34, color=GREY_A),
                      MathTex(r"a_k + b_k + c_k = s_k + 2\, c_{k+1}", font_size=34, color=HEAD),
                      label(r"(what one full adder does)", font_size=22, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 2.2 + DOWN * 0.6)
        mult = MathTex(r"\times\, 2^k \ \text{and add to the claim for } k", font_size=28, color=GREY_A).next_to(
            step, DOWN, buff=0.3).align_to(step, LEFT)
        done = label(r"at $k = n$: \ the $n$ sum bits and $c_{out}$ are exactly $a + b + c_{in}$", font_size=28,
                     color=YES).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Why is the chain right? By induction, as in Part 2. <bookmark mark='a'/> The claim: after the first k "
            "adders, the k sum bits plus the carry coming out of them, worth two to the k, equal the sum of the low k "
            "bits of a and b, plus the carry in. <bookmark mark='b'/> For k equal to zero there are no bits, and the "
            "carry is the carry in. <bookmark mark='c'/> For the step, one more full adder does exactly what its truth "
            "table says: its three inputs add up to its sum bit plus twice its carry out. Multiply that by two to the k "
            "and add it to the claim for k: the old carry term cancels, and the claim for k plus one appears. "
            "<bookmark mark='d'/> At k equal to n, it says the adder's outputs are exactly a plus b plus the carry in. "
            "Correct for every one of the two to the two n plus one inputs, and we never had to try them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(claim))
            vo.wait_until("a")
            self.play(Indicate(claim, scale_factor=1.02), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(base))
            vo.wait_until("c")
            self.play(FadeIn(step, lag_ratio=0.2))
            self.play(FadeIn(mult))
            vo.wait_until("d")
            self.play(FadeIn(done))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def slow(self):
        d = load("adders")
        ex = d["ripple_example"]
        times = ex["carry_times"]
        head = label(r"But the carry has to ripple", font_size=38).to_edge(UP, buff=0.35)
        n = 8
        boxes, cw, cin, cout = self.chain_mobs(n, y=1.3)
        a, b = format(ex["a"], "08b")[::-1], format(ex["b"], "08b")[::-1]
        s = format(ex["a"] + ex["b"], "09b")[::-1]
        ab = VGroup()
        for i, bx in enumerate(boxes):
            ab.add(MathTex(a[i], font_size=24, color=DATA).next_to(bx.a(), UP, buff=0.12),
                   MathTex(b[i], font_size=24, color=DATA).next_to(bx.b(), UP, buff=0.12))
        sums = VGroup(*[MathTex(s[i], font_size=28, color=YES).next_to(bx.s(), DOWN, buff=0.15)
                        for i, bx in enumerate(boxes)])
        tlab = VGroup(*[MathTex(rf"t = {times[i]}", font_size=20, color=HEAD).next_to(sums[i], DOWN, buff=0.1)
                        for i in range(n)])
        ex_t = MathTex(r"01111111 + 00000001", font_size=30, color=GREY_A).next_to(boxes, UP, buff=0.75)
        # depth against n
        rows = [r for r in d["rows"] if r["kind"] == "ripple"]
        ax = Axes(x_range=[0, 64, 16], y_range=[0, 130, 32], x_length=4.6, y_length=2.5, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).move_to(LEFT * 2.6 + DOWN * 2.1)
        pts = VGroup(*[Dot(ax.c2p(r["n"], r["settle"]), radius=0.06, color=NO) for r in rows])
        ln = axis_plot([r["n"] for r in rows], [r["settle"] for r in rows], ax, NO, 2.5)
        axl = note(r"bits $n$ \ against \ gate delays", font_size=20).next_to(ax, UP, buff=0.1)
        txt = VGroup(label(r"delay $\approx 2n + 1$ gates: \ $\Theta(n)$", font_size=28, color=NO),
                     label(r"64 bits: \ 129 gate delays \\ (a 4 GHz cycle has about 25)", font_size=24, color=GREY_A)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.4 + DOWN * 2.0)
        with self.voiceover(
            "There is a catch, and it is time. <bookmark mark='a'/> Add one to zero, one, one, one, one, one, one, one. "
            "Bit zero produces a carry; bit one cannot know its sum until that carry arrives; then it produces a carry "
            "for bit two, and so on. <bookmark mark='b'/> Simulated gate by gate, with every gate taking one unit of "
            "time, the sum bits settle one after another, two gate delays apart, from the right to the left. "
            "<bookmark mark='c'/> The worst case grows in step with the width: two n plus one gate delays. For "
            "sixty-four bits that is a hundred and twenty-nine, when Part 3's clock budget allowed a processor about "
            "twenty-five per cycle. A ripple-carry adder is correct, small and far too slow. The next chapter is about "
            "breaking the chain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes), Create(cw), Create(cin), Create(cout), FadeIn(ab), FadeIn(ex_t))
            vo.wait_until("a")
            self.play(Indicate(boxes[0], color=HEAD))
            vo.wait_until("b")
            order = sorted(range(n), key=lambda i: times[i])
            for i in order:
                anims = [FadeIn(sums[i]), FadeIn(tlab[i]), boxes[i][0].animate.set_stroke(HEAD)]
                if i < n - 1:
                    anims.append(cw[i].animate.set_stroke(HEAD))
                self.play(*anims, run_time=0.45)
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(axl), Create(ln), FadeIn(pts), FadeIn(txt))
        self.wait(0.3)
        self.clear_scene()
