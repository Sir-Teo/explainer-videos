from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, WIRE, YES, fmt, load, say


def unit(w, h, title, sub, color):
    b = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2.5, fill_color=BG,
                         fill_opacity=1)
    t = VGroup(label(title, font_size=24, color=color), label(sub, font_size=17, color=GREY_B)).arrange(DOWN, buff=0.08)
    if t.width > w - 0.2:
        t.scale_to_fit_width(w - 0.2)
    return VGroup(b, t.move_to(b))


class Alu(VoiceoverScene):
    def construct(self):
        self.card()
        self.diagram()
        self.compare_ops()
        self.verified()

    def card(self):
        card = chapter_card(8, r"Pebble's ALU", r"What does one arithmetic unit need to do?", part=PART)
        with self.voiceover("Chapter eight. Pebble's ALU."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def diagram(self):
        d = load("alu")
        head = label(r"Ten operations, \ one circuit", font_size=38).to_edge(UP, buff=0.3)
        add = unit(2.6, 1.1, r"adder", r"Kogge--Stone, \\ $b$ inverted for sub", YES).move_to(LEFT * 3.6 + UP * 1.0)
        logic = unit(2.6, 1.1, r"logic", r"AND, \ OR, \ XOR \\ per bit", CTRL).move_to(LEFT * 0.7 + UP * 1.0)
        shift = unit(2.6, 1.1, r"shifter", r"barrel: \ left, \ right, \\ arithmetic", FUNC).move_to(RIGHT * 2.2 + UP * 1.0)
        cmp_ = unit(2.6, 1.1, r"compare", r"from the adder's \\ sign, carry \ and overflow", HEAD).move_to(
            RIGHT * 5.1 + UP * 1.0)
        units = VGroup(add, logic, shift, cmp_)
        mux = RoundedRectangle(width=11.8, height=0.6, corner_radius=0.1, stroke_color=GREY_B, stroke_width=2.5,
                               fill_color=BG, fill_opacity=1).move_to(RIGHT * 0.75 + DOWN * 0.8)
        mt = label(r"select by \texttt{op}: \ an AND-OR multiplexer per output bit", font_size=22, color=GREY_A).move_to(mux)
        ins = VGroup(MathTex(r"a,\ b \ (32 \text{ bits each})", font_size=30, color=DATA).move_to(UP * 2.6 + RIGHT * 0.75))
        feeds = VGroup(*[Arrow(ins.get_bottom(), u.get_top(), buff=0.1, stroke_width=2.5, color=WIRE,
                               max_tip_length_to_length_ratio=0.12) for u in units])
        down = VGroup(*[Arrow(u.get_bottom(), [u.get_x(), mux.get_top()[1], 0], buff=0.05, stroke_width=2.5, color=WIRE,
                              max_tip_length_to_length_ratio=0.3) for u in units])
        op = MathTex(r"\texttt{op}\ (4 \text{ bits})", font_size=28, color=CTRL).next_to(mux, LEFT, buff=0.25).shift(
            DOWN * 0.5)
        out = MathTex(r"y\ (32 \text{ bits}), \quad \text{zero}, \quad \text{overflow}", font_size=30,
                      color=YES).next_to(mux, DOWN, buff=0.55)
        oarr = Arrow(mux.get_bottom(), out.get_top(), buff=0.05, stroke_width=2.5, color=WIRE,
                     max_tip_length_to_length_ratio=0.3)
        ops = label(r"add \ sub \ and \ or \ xor \ sll \ srl \ sra \ slt \ sltu", font_size=26, color=GREY_A).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Pebble's processor will need one unit that does all of its arithmetic and logic, the ALU. Here are the "
            "operations its instruction set asks for. <bookmark mark='a'/> An adder, which also "
            "subtracts by inverting b and setting the carry in. A logic unit, which is just one and, one or and one "
            "exclusive-or per bit. A barrel shifter, from Part 3, extended to shift right as well, filling with zeros "
            "or with copies of the sign bit. And comparisons, which need no new hardware at all, as we will see. "
            "<bookmark mark='b'/> All of them compute at once, on every instruction, and a four-bit operation code "
            "selects which answer leaves, through a multiplexer on every output bit. Two flags come out too: whether "
            "the result is zero, which branches will test, and whether a signed add overflowed. "
            "<bookmark mark='c'/> Ten operations in all, exactly the ones Pebble's emulator implements."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ins))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(u, shift=DOWN * 0.1) for u in units], lag_ratio=0.3), Create(feeds),
                      run_time=2.4)
            vo.wait_until("b")
            self.play(Create(down), FadeIn(mux), FadeIn(mt), FadeIn(op))
            self.play(GrowArrow(oarr), FadeIn(out))
            vo.wait_until("c")
            self.play(FadeIn(ops))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare_ops(self):
        head = label(r"Comparison is subtraction", font_size=38).to_edge(UP, buff=0.35)
        rows = VGroup(
            MathTex(r"\texttt{sltu}: \ a < b \text{ (unsigned)} \iff a - b \text{ borrows} \iff c_{out} = 0",
                    font_size=34, color=GREY_A),
            MathTex(r"\texttt{slt}: \ a < b \text{ (signed)} \iff \text{sign}(a - b) \oplus \text{overflow}",
                    font_size=34, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 1.7)
        ex = VGroup(
            label(r"4 bits: \ $a = -3$, \ $b = 2$:", font_size=28, color=DATA),
            MathTex(r"1101 - 0010 = 1011 \ (-5): \ \text{sign } 1, \ \text{no overflow} \Rightarrow -3 < 2 \ \checkmark",
                    font_size=32, color=YES),
            label(r"4 bits: \ $a = -8$, \ $b = 1$:", font_size=28, color=DATA),
            MathTex(r"1000 - 0001 = 0111 \ (+7): \ \text{sign } 0, \ \text{overflow} \Rightarrow -8 < 1 \ \checkmark",
                    font_size=32, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 0.7)
        foot = label(r"the sign alone would get the second one wrong: \ overflow flips it", font_size=26,
                     color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How does an adder compare? <bookmark mark='a'/> For unsigned numbers, a is less than b exactly when a "
            "minus b has to borrow, and in two's complement subtraction a borrow shows up as a carry out of zero. For "
            "signed numbers, look at the sign of a minus b, but correct it with the overflow bit. "
            "<bookmark mark='b'/> Minus three minus two is minus five: the sign is one, no overflow, so minus three is "
            "less. Minus eight minus one should be minus nine, which does not fit in four bits; it wraps round to plus "
            "seven, with a sign of zero, but the overflow flag is set, and flipping the sign gives the right answer. "
            "<bookmark mark='c'/> Getting this wrong is a classic bug in hand-written assembly: comparing by the sign "
            "of a difference works until the numbers get large."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verified(self):
        d = load("alu")
        rows = {r["adder"]: r for r in d["rows"]}
        ks, rp = rows["kogge-stone"], rows["ripple"]
        head = label(r"Built, \ verified, \ and measured", font_size=38).to_edge(UP, buff=0.35)
        checks = VGroup(
            label(rf"8-bit ALU: \ all {fmt(d['exhaustive8'])} cases \ ($2^8 \times 2^8 \times 10$ ops) \ $\checkmark$",
                  font_size=28, color=YES),
            label(r"32-bit ALU: \ 20{,}000 random and worst-case inputs, \\ against the semantics of Pebble's emulator "
                  r"\ $\checkmark$", font_size=28, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 1.6)
        hdr = VGroup(*[label(t, font_size=24, color=GREY_B) for t in (r"32-bit ALU with", r"gates", r"as NANDs",
                                                                      r"deepest path", r"measured delay")])
        tab = VGroup(hdr)
        for name, r in ((r"a ripple adder", rp), (r"Kogge--Stone", ks)):
            tab.add(VGroup(label(name, font_size=26, color=NO if r is rp else YES),
                           MathTex(fmt(r["gates"]), font_size=30, color=GREY_A),
                           MathTex(fmt(r["nands"]), font_size=30, color=GREY_A),
                           MathTex(str(r["depth"]), font_size=30, color=GREY_A),
                           MathTex(str(r["settle"]), font_size=30, color=NO if r is rp else YES)))
        for i, r in enumerate(tab):
            for j, m in enumerate(r):
                m.move_to([-4.6 + [0, 2.7, 4.6, 6.6, 8.8][j], -0.3 - 0.6 * i, 0])
        foot = VGroup(
            label(rf"the fast adder costs {ks['gates'] - rp['gates']} more gates \ and makes the whole ALU "
                  rf"{rp['settle'] / ks['settle']:.1f} times faster", font_size=26, color=HEAD),
            note(r"Part 5 gives Pebble registers to hold the operands; \ Part 6 wires this ALU into the processor",
                 font_size=22),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "This ALU exists, as a netlist in the series' library. <bookmark mark='a'/> The eight-bit version was "
            "checked on every one of its six hundred and fifty-five thousand cases: every pair of operands, for all "
            "ten operations. The thirty-two-bit version was checked on twenty thousand inputs, random ones and "
            "worst-case carries and borrows, against exactly what Pebble's emulator computes. "
            "<bookmark mark='b'/> With a ripple adder inside, the thirty-two-bit ALU has about sixteen hundred gates "
            "and takes seventy-eight gate delays. With Kogge-Stone, about three hundred gates more, and twenty-nine "
            "delays. <bookmark mark='c'/> The fast adder costs a fifth more gates and makes the whole unit almost "
            "three times faster, because addition was the slowest thing in it. Rewritten in NAND gates alone, it is "
            "about four and a half thousand of them. In Part 6 this circuit becomes the heart of Pebble."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(checks[0]))
            self.play(FadeIn(checks[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
