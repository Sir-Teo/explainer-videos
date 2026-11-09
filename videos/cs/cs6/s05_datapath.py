from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, USES, WIRE, YES, box, fmt,
                                  load)
from videos.cs.cs6.common import Datapath as DatapathFigure


def caption(text, color=GREY_A, font_size=24):
    return label(text, font_size=font_size, color=color).to_edge(DOWN, buff=0.18)


def instr_tag(src, color=CODE):
    t = Text(src, font="DejaVu Sans Mono", font_size=24, color=color)
    b = SurroundingRectangle(t, buff=0.12, color=color, corner_radius=0.08, stroke_width=2)
    return VGroup(b, t).to_corner(UL, buff=0.25)


class Datapath(VoiceoverScene):
    def construct(self):
        self.card()
        dp = DatapathFigure().scale(0.9).shift(DOWN * 0.3)
        self.dp = dp
        self.fetch()
        self.rtype()
        self.itype()
        self.memory()
        self.branches()
        self.summary()
        self.one_cycle()

    def card(self):
        card = chapter_card(4, r"The datapath, \ one instruction at a time", r"Where do the bits go?", part=PART)
        with self.voiceover("Chapter four. The datapath, one instruction at a time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def show(self, keys):
        return [FadeIn(self.dp.blocks[k]) for k in keys]

    # ------------------------------------------------------------------
    def fetch(self):
        dp = self.dp
        cap = caption(r"every cycle: \ fetch the word at \texttt{pc}, \ and compute \texttt{pc} $+ 4$")
        with self.voiceover(
            "Now we build the machine that runs this loop, one piece at a time, and send instructions through it. "
            "<bookmark mark='a'/> It starts with the program counter, a thirty-two-bit register from Part 5, and the "
            "instruction memory, which takes an address and returns the word stored there. <bookmark mark='b'/> In "
            "the same cycle, a small adder computes the program counter plus four, the address of the next "
            "instruction, ready to be loaded at the next clock edge. <bookmark mark='c'/> That is the whole of fetch: "
            "a register, a memory, an adder, and a wire looping back."
        ) as vo:
            self.play(*self.show(["pc", "imem"]), Create(dp.wires["pc_imem"]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(dp.blocks["add4"]), Create(dp.wires["pc_add4"]), FadeIn(cap))
            vo.wait_until("c")
            self.play(FadeIn(dp.blocks["mux_pc"]), Create(dp.wires["add4_pc"]), Create(dp.wires["pc_next"]),
                      FadeIn(dp.dots[6]))
            dp.flow(self, ["pc_imem", "pc_add4"], color=YES)
            dp.flow(self, ["add4_pc"], color=YES, run_time=1.0)
            dp.flow(self, ["pc_next"], color=YES, run_time=1.2)
        self.play(FadeOut(cap))

    # ------------------------------------------------------------------
    def rtype(self):
        dp = self.dp
        tag = instr_tag("add  a2, a0, a1")
        vals = VGroup(MathTex(r"a_0 = 5", font_size=26, color=DATA).next_to(dp.wires["rf_a"], UP, buff=0.08),
                      MathTex(r"a_1 = 7", font_size=26, color=DATA).next_to(dp.blocks["mux_b"], DOWN, buff=0.15)
                      .shift(LEFT * 0.4), MathTex(r"12", font_size=30, color=HEAD).next_to(dp.blocks["alu"], DOWN,
                                                                                           buff=0.2))
        cap = caption(r"R format: \ read two registers, \ add in the ALU, \ write the third")
        with self.voiceover(
            "Next, an instruction that adds two registers. <bookmark mark='a'/> The instruction's bits fan out. Two "
            "four-bit fields go to the register file's read ports, which is Part 5's register file exactly. <bookmark "
            "mark='b'/> The two values flow into Part 4's ALU, and a few bits from the control unit tell it to add. "
            "<bookmark mark='c'/> The sum flows back around to the register file's write port, addressed by the third "
            "field, and is written at the next clock edge, at the same moment as the program counter moves on. In this"
            " synchronous model, combinational signals settle between edges; state is captured at the edges."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(*self.show(["rf", "ctrl"]), Create(dp.wires["instr_rf"]), Create(dp.wires["instr_ctl"]),
                      FadeIn(dp.dots[0]))
            vo.wait_until("b")
            self.play(*self.show(["alu", "mux_b"]), Create(dp.wires["rf_a"]), Create(dp.wires["rf_b"]),
                      Create(dp.wires["mux_alu"]), Create(dp.ctl[1]), Create(dp.ctl[2]), FadeIn(dp.dots[4]))
            vo.wait_until("c")
            self.play(*self.show(["mux_wb"]), Create(dp.wires["alu_wb"]), Create(dp.wires["wb_rf"]),
                      Create(dp.ctl[0]), FadeIn(dp.dots[3]), FadeIn(cap))
            self.play(*dp.lit(USES["R"]))
            dp.flow(self, ["pc_imem"], run_time=0.6)
            dp.flow(self, ["instr_rf", "instr_ctl"], run_time=0.8)
            self.play(FadeIn(vals[0]), FadeIn(vals[1]))
            dp.flow(self, ["rf_a", "rf_b"], run_time=0.6)
            dp.flow(self, ["mux_alu"], run_time=0.4)
            self.play(FadeIn(vals[2]))
            dp.flow(self, ["alu_wb"], run_time=0.8)
            dp.flow(self, ["wb_rf"], run_time=1.0)
        self.play(*dp.unlit(), FadeOut(tag), FadeOut(vals), FadeOut(cap))

    # ------------------------------------------------------------------
    def itype(self):
        dp = self.dp
        tag = instr_tag("addi a0, a0, -1")
        cap = caption(r"I format: \ the immediate, \ sign-extended to 32 bits, \ takes the place of the second "
                      r"register")
        ext = MathTex(r"\underbrace{1\cdots1}_{14}\,\underbrace{11\,1111\,1111\,1111\,1111}_{18 \text{ bits of } -1}",
                      font_size=24, color=HEAD).next_to(dp.blocks["imm"], DOWN, buff=0.15)
        with self.voiceover(
            "To add a constant instead, the instruction's low eighteen bits go to the immediate unit. "
            "<bookmark mark='a'/> It sign-extends them: copies the top bit into the fourteen bits above, so minus one "
            "in eighteen bits becomes minus one in thirty-two. No gates at all, just wires. <bookmark mark='b'/> A "
            "multiplexer in front of the ALU chooses the second operand: the register, for an R-format instruction, or "
            "the immediate. Which one is chosen is another bit from the control unit."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(*self.show(["imm"]), Create(dp.wires["instr_imm"]), FadeIn(dp.dots[1]), FadeIn(ext))
            vo.wait_until("b")
            self.play(Create(dp.wires["imm_b"]), FadeIn(cap))
            self.play(*dp.lit(USES["I"]))
            dp.flow(self, ["instr_imm"], run_time=0.8)
            dp.flow(self, ["imm_b"], run_time=0.8)
            dp.flow(self, ["mux_alu"], run_time=0.4)
        self.play(*dp.unlit(), FadeOut(tag), FadeOut(cap), FadeOut(ext))

    # ------------------------------------------------------------------
    def memory(self):
        dp = self.dp
        tag = instr_tag("lw   t0, 8(sp)")
        cap = caption(r"load: \ the ALU adds base and offset; \ the word read from memory is written back")
        cap2 = caption(r"store: \ the second register's value goes to memory, \ nothing is written back")
        with self.voiceover(
            "Loads and stores need the second memory, for data. <bookmark mark='a'/> For a load, the ALU adds the base "
            "register and the offset, and the sum is an address. The data memory reads the word there, and a second "
            "multiplexer, at the end, chooses what is written back: the ALU's result or the loaded word. "
            "<bookmark mark='b'/> A store uses the same address calculation, but sends the second register's value to "
            "the memory's data input, and tells the register file not to write. <bookmark mark='c'/> The load is the "
            "longest journey any instruction makes in this machine: through the instruction memory, the register file, "
            "the ALU, the data memory and the write-back multiplexer, all within one clock cycle. That path sets the "
            "clock for every instruction."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(*self.show(["dmem"]), Create(dp.wires["alu_dmem"]), Create(dp.wires["dmem_wb"]),
                      Create(dp.ctl[3]), FadeIn(cap))
            self.play(*dp.lit(USES["load"]))
            dp.flow(self, ["rf_a", "imm_b"], run_time=0.7)
            dp.flow(self, ["mux_alu"], run_time=0.4)
            dp.flow(self, ["alu_dmem"], run_time=0.6)
            dp.flow(self, ["dmem_wb"], run_time=0.6)
            dp.flow(self, ["wb_rf"], run_time=1.0)
            vo.wait_until("b")
            self.play(*dp.unlit(), Transform(tag, instr_tag("sw   t0, 8(sp)")), FadeOut(cap))
            self.play(Create(dp.wires["b_dmem"]), FadeIn(cap2))
            self.play(*dp.lit(USES["store"]))
            dp.flow(self, ["b_dmem", "alu_dmem"], run_time=1.0)
            vo.wait_until("c")
            self.play(*dp.unlit(), FadeOut(cap2))
            path = ["pc_imem", "instr_rf", "rf_a", "mux_alu", "alu_dmem", "dmem_wb", "wb_rf"]
            self.play(*dp.lit(path, color=NO, width=6))
        self.play(*dp.unlit(), FadeOut(tag))

    # ------------------------------------------------------------------
    def branches(self):
        dp = self.dp
        tag = instr_tag("bne  a0, zero, loop")
        cap = caption(r"branch: \ the ALU compares; \ a second adder computes \texttt{pc} $+ 4 \times$ offset; \ "
                      r"a multiplexer picks the next \texttt{pc}")
        cap2 = caption(r"\texttt{jal}: \ jump, \ and write \texttt{pc} $+ 4$ \ (the return address) \ to a register")
        with self.voiceover(
            "Last, the instructions that change the flow. <bookmark mark='a'/> A branch compares two registers in the "
            "ALU, by subtracting them and testing for zero, or comparing signs. <bookmark mark='b'/> Meanwhile a "
            "second adder computes the target: the program counter plus four times the offset in the instruction. "
            "<bookmark mark='c'/> If the condition holds, the multiplexer in front of the program counter takes the "
            "target instead of pc plus four. <bookmark mark='d'/> A jump-and-link always takes its target, and writes "
            "pc plus four into a register on the way, so that the code it jumps to can return: EDSAC's Wheeler jump, "
            "in hardware. Jump-and-link-register takes its target from the ALU instead, which is how a function "
            "returns."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(*dp.lit(["rf_a", "rf_b", "mux_alu"]))
            vo.wait_until("b")
            self.play(*self.show(["addt"]), Create(dp.wires["imm_t"]), Create(dp.wires["pc_t"]), FadeIn(dp.dots[2]))
            self.play(*dp.lit(["imm_t", "pc_t"]))
            dp.flow(self, ["imm_t", "pc_t"], run_time=1.2)
            vo.wait_until("c")
            self.play(Create(dp.wires["t_pc"]), FadeIn(cap))
            self.play(*dp.lit(USES["branch"]))
            dp.flow(self, ["t_pc"], run_time=0.6)
            dp.flow(self, ["pc_next"], run_time=1.2)
            vo.wait_until("d")
            self.play(*dp.unlit(), Transform(tag, instr_tag("jal  ra, f")), FadeOut(cap))
            self.play(Create(dp.wires["link_wb"]), Create(dp.wires["alu_pc"]), FadeIn(dp.dots[5]), FadeIn(cap2))
            self.play(*dp.lit(USES["jal"]))
            dp.flow(self, ["link_wb", "t_pc"], run_time=1.0)
            dp.flow(self, ["wb_rf", "pc_next"], run_time=1.2)
        self.play(*dp.unlit(), FadeOut(tag), FadeOut(cap2))

    # ------------------------------------------------------------------
    def summary(self):
        dp = self.dp
        cp = load("cpu")
        cap = caption(rf"all of it: \ {fmt(cp['gates'])} gates and {cp['flip_flops']} flip-flops, \ one instruction "
                      r"per clock cycle", color=HEAD, font_size=26)
        with self.voiceover(
            "That is the whole datapath: about a dozen blocks, every one of them a circuit from an earlier part, with "
            "the control unit's dashed lines steering the multiplexers and the ALU. <bookmark mark='a'/> Built as a "
            "netlist in this series' library, it comes to a little over eight thousand gates and five hundred and "
            "twelve flip-flops: the program counter and fifteen registers of thirty-two bits. One instruction "
            "finishes in every clock cycle."
        ) as vo:
            self.play(*[Indicate(b, color=HEAD, scale_factor=1.04) for b in dp.blocks.values()], run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()


    # ------------------------------------------------------------------
    def one_cycle(self):
        head = label(r"Inside one clock cycle", font_size=38).to_edge(UP, buff=0.35)
        x0, x1 = -4.0, 5.6
        e0, e1 = -3.2, 4.8
        rows = [(r"\text{clk}", None, CLOCK), (r"\text{pc}", 0.15, YES), (r"\text{instruction}", 1.6, DATA),
                (r"\text{registers read}", 2.5, YES), (r"\text{ALU result}", 4.6, FUNC),
                (r"\text{memory data}", 6.4, DATA), (r"\text{value to write}", 6.9, HEAD)]
        g = VGroup()
        for k, (name, settle, c) in enumerate(rows):
            y = 2.0 - 0.62 * k
            nm = MathTex(name, font_size=24, color=c).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
            if settle is None:
                pts = [[x0, y - 0.18, 0], [e0, y - 0.18, 0], [e0, y + 0.18, 0], [(e0 + e1) / 2, y + 0.18, 0],
                       [(e0 + e1) / 2, y - 0.18, 0], [e1, y - 0.18, 0], [e1, y + 0.18, 0], [x1, y + 0.18, 0]]
                wv = VMobject(color=c, stroke_width=3).set_points_as_corners([np.array(p_, float) for p_ in pts])
                g.add(VGroup(nm, wv))
                continue
            xs = e0 + settle
            busy = Polygon([e0, y, 0], [e0 + 0.1, y + 0.18, 0], [xs, y + 0.18, 0], [xs + 0.1, y, 0],
                           [xs, y - 0.18, 0], [e0 + 0.1, y - 0.18, 0], stroke_width=0, fill_color=GREY_D,
                           fill_opacity=0.6)
            good = Polygon([xs + 0.1, y, 0], [xs + 0.2, y + 0.18, 0], [e1, y + 0.18, 0], [e1 + 0.1, y, 0],
                           [e1, y - 0.18, 0], [xs + 0.2, y - 0.18, 0], stroke_color=c, stroke_width=2, fill_color=c,
                           fill_opacity=0.25)
            g.add(VGroup(nm, busy, good))
        edges = VGroup(*[DashedLine([x, 2.4, 0], [x, -2.1, 0], color=GREY_C, stroke_width=1.5) for x in (e0, e1)])
        el = VGroup(label(r"rising edge: \\ \texttt{pc} and registers load", font_size=18, color=GREY_A).next_to(
            edges[0], DOWN, buff=0.1), label(r"next edge: \\ the result is written", font_size=18, color=GREY_A).next_to(
            edges[1], DOWN, buff=0.1))
        foot = label(r"grey: \ still settling; \ coloured: \ correct. \ The cycle must outlast the slowest row.",
                     font_size=22, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "It helps to watch one cycle in time. <bookmark mark='a'/> At the rising edge, the program counter and the"
            " registers load their new values, and everything downstream starts to change. <bookmark mark='b'/> The "
            "instruction word comes out of memory first, then the register file's outputs settle, then the ALU's "
            "result, then, for a load, the data from memory, and last of all the value to be written back. Before each"
            " one settles, the wires may carry glitches and unfinished values; synchronous registers must sample only "
            "after their timing requirements are met. <bookmark mark='c'/> At the next rising edge, the register file "
            "and the program counter capture what is on their inputs, and the cycle starts again. Part 5's timing "
            "rules still apply: values must settle before the next edge with setup margin, and remain stable for the "
            "required hold window. This drawing illustrates the settling order, not a measured physical waveform. The "
            "next chapter opens the one block we have treated as a black box: the control unit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(edges), *[FadeIn(r[0]) for r in g])
            self.play(Create(g[0][1]))
            vo.wait_until("a")
            self.play(FadeIn(el[0]))
            vo.wait_until("b")
            for r in g[1:]:
                self.play(FadeIn(r[1]), run_time=0.3)
                self.play(GrowFromEdge(r[2], LEFT), run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(el[1]), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

