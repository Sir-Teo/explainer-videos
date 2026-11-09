from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, WIRE, YES, fmt, load, say


def box(w, h, text, color=CTRL, font_size=22):
    b = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=color, stroke_width=2.2, fill_color=BG,
                         fill_opacity=1)
    return VGroup(b, MathTex(text, font_size=font_size, color=color).move_to(b))


class RegFile(VoiceoverScene):
    def construct(self):
        self.card()
        self.structure()
        self.bypass()
        self.cost()

    def card(self):
        card = chapter_card(9, r"Pebble's register file", r"Where does a processor keep its working values?", part=PART)
        with self.voiceover("Chapter nine. Pebble's register file."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def structure(self):
        head = label(r"Sixteen registers, \ two read ports, \ one write port", font_size=34).to_edge(UP, buff=0.3)
        regs = VGroup(*[box(2.2, 0.28, rf"r_{{{i}}}" if i else r"r_0 = 0", YES if i else GREY_B, 18) for i in range(16)])
        regs.arrange(DOWN, buff=0.03).move_to(DOWN * 0.05)
        dec = box(1.3, 2.4, r"\text{decoder}", CTRL).next_to(regs, LEFT, buff=1.0)
        wa = MathTex(r"wa,\ we", font_size=26, color=DATA).next_to(dec, LEFT, buff=0.3)
        wd = MathTex(r"wd", font_size=26, color=DATA).next_to(regs, UP, buff=0.35)
        wlines = VGroup(*[Line(dec.get_right(), r.get_left(), color=CTRL, stroke_width=1.2) for r in regs[1:]])
        mA = box(1.0, 2.2, r"\text{mux}", HEAD).next_to(regs, RIGHT, buff=0.9).shift(UP * 1.2)
        mB = box(1.0, 2.2, r"\text{mux}", HEAD).next_to(regs, RIGHT, buff=0.9).shift(DOWN * 1.2)
        ra = MathTex(r"ra", font_size=24, color=DATA).next_to(mA, UP, buff=0.12)
        rb = MathTex(r"rb", font_size=24, color=DATA).next_to(mB, DOWN, buff=0.12)
        oa = Arrow(mA.get_right(), mA.get_right() + RIGHT * 1.0, buff=0, color=WIRE, stroke_width=3)
        ob = Arrow(mB.get_right(), mB.get_right() + RIGHT * 1.0, buff=0, color=WIRE, stroke_width=3)
        la = MathTex("a", font_size=28, color=YES).next_to(oa, RIGHT, buff=0.1)
        lb = MathTex("b", font_size=28, color=YES).next_to(ob, RIGHT, buff=0.1)
        rlines = VGroup(*[Line(r.get_right(), mA.get_left(), color=GREY_D, stroke_width=0.8) for r in regs],
                        *[Line(r.get_right(), mB.get_left(), color=GREY_D, stroke_width=0.8) for r in regs])
        note1 = label(r"write: \ the decoder enables one register; \ each of its bits loads $wd$ instead of keeping "
                      r"its value", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.55)
        note2 = label(r"read: \ two 16-to-1 multiplexer trees, \ 32 bits wide, \ pick any two registers at once",
                      font_size=22, color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Pebble's instructions name three registers at once: add r three, r one, r two reads two registers and "
            "writes a third. So its register file has two read ports and one write port. <bookmark mark='a'/> Sixteen "
            "registers of thirty-two flip-flops each, except register zero, which the instruction set defines to be "
            "zero and so needs no flip-flops at all. <bookmark mark='b'/> To write, Part 3's decoder turns the four-bit "
            "write address into one enable line per register; at the clock edge, the enabled register loads the "
            "write data, and every other register, through a multiplexer on each bit, loads its own value back. "
            "<bookmark mark='c'/> To read, two trees of multiplexers, each thirty-two bits wide, pick out the two "
            "registers named by the read addresses, both in the same cycle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(regs))
            vo.wait_until("a")
            self.play(Indicate(regs, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(dec), FadeIn(wa), FadeIn(wd), Create(wlines), FadeIn(note1))
            vo.wait_until("c")
            self.play(Create(rlines), FadeIn(mA), FadeIn(mB), FadeIn(ra), FadeIn(rb), GrowArrow(oa), GrowArrow(ob),
                      FadeIn(la), FadeIn(lb), FadeIn(note2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bypass(self):
        head = label(r"Reading a register \ in the cycle it is written", font_size=36).to_edge(UP, buff=0.35)
        prog = code_block(["add  r3, r1, r2     # cycle 1: writes r3 at the end", "sub  r4, r3, r5     # cycle 2: reads r3"],
                          font_size=24).move_to(UP * 1.7)
        opts = VGroup(
            label(r"the write happens at the clock edge; \ the read happens during the cycle", font_size=26,
                  color=GREY_A),
            label(r"one cycle apart: \ fine, \ the new value is already in the flip-flops", font_size=26, color=YES),
            label(r"in a pipelined processor the two overlap: \ write in the first half-cycle and read in the second, "
                  r"\\ or add a \textit{bypass}: \ a comparator and a multiplexer \ that route $wd$ straight to the "
                  r"output when $wa = ra$", font_size=24, color=HEAD),
            label(r"forwarding paths like this are a large part of Part 7", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.3)
        prog.move_to(UP * 2.25)
        rf = box(1.8, 1.0, r"\text{register file}", YES, 22).move_to(LEFT * 3.0 + UP * 0.45)
        mx = box(0.7, 1.0, r"\text{mux}", HEAD, 20).move_to(RIGHT * 0.6 + UP * 0.45)
        cmpb = box(1.5, 0.6, r"wa = ra\,?", CTRL, 22).move_to(RIGHT * 0.6 + DOWN * 0.65)
        wdin = MathTex(r"wd", font_size=26, color=DATA).move_to(LEFT * 5.6 + UP * 0.75)
        p1 = Arrow(rf.get_right() + DOWN * 0.15, mx.get_left() + DOWN * 0.15, buff=0.02, color=WIRE, stroke_width=3)
        w_into = Arrow(wdin.get_right(), [rf.get_left()[0], 0.75, 0], buff=0.1, color=DATA,
                       stroke_width=3)
        byp = VMobject(color=HEAD, stroke_width=3.5).set_points_as_corners(
            [[-4.6, 0.75, 0], [-4.6, 1.45, 0], [-0.4, 1.45, 0], [-0.4, 0.75, 0], mx.get_left() + UP * 0.3])
        sel = Arrow(cmpb.get_top(), mx.get_bottom(), buff=0.02, color=CTRL, stroke_width=3)
        outp = Arrow(mx.get_right(), mx.get_right() + RIGHT * 1.2, buff=0.02, color=YES, stroke_width=3)
        ol = MathTex(r"\text{read port } a", font_size=24, color=YES).next_to(outp, RIGHT, buff=0.1)
        bl_ = label(r"bypass", font_size=22, color=HEAD).next_to([-2.5, 1.45, 0], UP, buff=0.08)
        diag = VGroup(rf, mx, cmpb, wdin, p1, w_into, sel, outp, ol)
        with self.voiceover(
            "One subtlety matters as soon as the processor gets faster. <bookmark mark='a'/> The first instruction "
            "writes register three; the next one reads it. The register file writes at the clock edge and reads during "
            "the cycle, so as long as the second instruction reads in the next cycle, the new value is already sitting "
            "in the flip-flops. <bookmark mark='b'/> In the pipelined processors of Part 7, though, one instruction "
            "may be reading register three in the very cycle another is writing it. Designs solve this either by "
            "writing in the first half of the cycle and reading in the second, or with a bypass: a comparator notices "
            "that the read address equals the write address, and a multiplexer hands the new value straight to the "
            "output. Those forwarding paths, and when they are not enough, are a large part of Part 7."
        ) as vo:
            self.play(FadeIn(head), FadeIn(prog))
            vo.wait_until("a")
            self.play(FadeIn(opts[0]), FadeIn(opts[1]))
            self.play(FadeIn(diag))
            vo.wait_until("b")
            self.play(FadeIn(opts[2]))
            self.play(Create(byp), FadeIn(bl_), Indicate(cmpb, color=CTRL))
            dot = Dot(wdin.get_right(), radius=0.08, color=HEAD)
            self.add(dot)
            self.play(MoveAlongPath(dot, VMobject().set_points_as_corners(
                [wdin.get_right(), [-4.6, 0.75, 0], [-4.6, 1.45, 0], [-0.4, 1.45, 0], [-0.4, 0.75, 0],
                 mx.get_left() + UP * 0.3, mx.get_right(), outp.get_end()])), run_time=2.0, rate_func=linear)
            self.play(FadeOut(dot), FadeIn(opts[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cost(self):
        d = load("regfile")
        head = label(r"Built, \ verified, \ counted", font_size=38).to_edge(UP, buff=0.35)
        nums = VGroup(
            label(rf"{d['flip_flops']} flip-flops \ (15 registers $\times$ 32 bits)", font_size=30, color=YES),
            label(rf"{fmt(d['gates'])} gates of logic around them", font_size=30, color=COST),
            label(rf"verified: \ {d['copies']} copies run for {d['cycles']} cycles of random reads and writes, \\ "
                  r"against a Python model of sixteen variables", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.3).move_to(UP * 1.2)
        ports = VGroup(
            label(rf"each extra read port: \ another 32-bit 16-to-1 multiplexer tree, \ about {fmt(d['read_port_gates'])} "
                  r"gates", font_size=26, color=HEAD),
            label(r"each extra write port: \ another decoder, \ and a wider multiplexer on every one of the 480 bits",
                  font_size=26, color=HEAD),
            label(r"so wide superscalar processors, \ which read and write many registers per cycle, \\ spend a "
                  r"striking share of their area and power on the register file \ (Parts 7 and 8)", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.35)
        nums.move_to(UP * 1.85)
        rp = d['read_port_gates']
        parts = ((r"read port $a$", rp, HEAD), (r"read port $b$", rp, HEAD),
                 (r"write: \ decoder and hold muxes", d['gates'] - 2 * rp, CTRL))
        scale = 11.0 / d['gates']
        bar = VGroup()
        for t, n, c in parts:
            seg = Rectangle(width=n * scale, height=0.55, stroke_color=BG, stroke_width=2, fill_color=c,
                            fill_opacity=0.55)
            bar.add(VGroup(seg, label(t, font_size=20, color=WHITE).move_to(seg)))
        bar.arrange(RIGHT, buff=0).move_to(UP * 0.05)
        cnt = VGroup(*[label(fmt(n), font_size=20, color=GREY_B).next_to(b, DOWN, buff=0.1) for b, (_, n, _) in
                       zip(bar, parts)])
        bcap = note(rf"where the {fmt(d['gates'])} gates go", font_size=20).next_to(bar, UP, buff=0.12)
        with self.voiceover(
            "In the series' library this register file is a checked circuit model. These are counts in our chosen "
            "gate basis, not a transistor-area estimate. <bookmark mark='a'/> Four hundred and eighty flip-flops, "
            "and a little under six thousand gates of decoding and multiplexing around them. Two hundred and "
            "fifty-six copies were run for sixty-four cycles of random reads and writes, and every value read "
            "matched a Python model that simply keeps sixteen variables. <bookmark mark='b'/> Notice where the "
            "gates go. Every extra read port is another multiplexer tree, about two thousand gates; every extra "
            "write port is another decoder and wider multiplexers on all four hundred and eighty bits. Processors "
            "that execute several instructions per cycle need many ports, and their register files become some of "
            "the largest and hottest structures on the chip, as Parts 7 and 8 will show."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nums))
            vo.wait_until("a")
            self.play(Indicate(nums, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(bcap), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bar], lag_ratio=0.5), FadeIn(cnt),
                      run_time=2.0)
            self.play(LaggedStart(*[FadeIn(p) for p in ports], lag_ratio=0.4), run_time=2.4)
        self.wait(0.3)
        self.clear_scene()
