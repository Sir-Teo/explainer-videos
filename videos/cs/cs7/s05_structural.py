from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, STAGE_COLOR, STAGES,
                                  YES, PipeChart, PipeFigure, box, fmt, load, mono)


class Structural(VoiceoverScene):
    def construct(self):
        self.card()
        self.hazards()
        self.memory()
        self.divider()

    def card(self):
        card = chapter_card(4, r"Structural hazards", r"What if two instructions need the same part at once?",
                            part=PART)
        with self.voiceover("Chapter four. Structural hazards."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def hazards(self):
        head = label(r"Three kinds of hazard", font_size=38).to_edge(UP, buff=0.35)
        kinds = VGroup(*[VGroup(label(a, font_size=30, color=c), label(b, font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.15) for a, b, c in (
            (r"structural", r"two instructions need \\ the same hardware", INF),
            (r"data", r"an instruction needs a value \\ an earlier one has not produced", FUNC),
            (r"control", r"the next instruction depends \\ on a branch not yet decided", NO))]).arrange(RIGHT, buff=1.0)
        kinds.move_to(UP * 0.4)
        fix = label(r"the cure is always the same in the last resort: \ \textit{stall}, \ and insert a bubble; \\ the art "
                    r"is to stall as rarely as possible", font_size=24, color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The ideal chart, one instruction per cycle, breaks whenever an instruction cannot proceed. These "
            "situations are called hazards, and they come in three kinds. <bookmark mark='a'/> Structural hazards: two "
            "instructions need the same piece of hardware in the same cycle. Data hazards: an instruction needs a value "
            "that an earlier instruction has not produced yet. Control hazards: the machine needs to fetch the next "
            "instruction before it knows where the program is going. <bookmark mark='b'/> The last-resort cure is "
            "always the same: hold the instruction back, and let an empty slot, a bubble, travel down the pipeline in "
            "its place. Every cycle lost this way raises the CPI above one. The art of pipeline design is stalling as "
            "rarely as possible."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.2) for k in kinds], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(fix))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def memory(self):
        hz = load("hazards")["structural"]
        frac = hz["one memory port, the Job"]["memory_fraction"]
        head = label(r"One memory, \ two stages", font_size=38).to_edge(UP, buff=0.35)
        fig = PipeFigure(width=11.0, stage_w=1.6, h=1.1).move_to(UP * 1.4)
        mem = box(3.0, 0.9, r"\text{one memory}", INF, 26).move_to(DOWN * 0.6)
        a1 = Arrow(fig.stage["IF"].get_bottom(), mem.get_left() + UP * 0.2, buff=0.1, color=DATA, stroke_width=3)
        a2 = Arrow(fig.stage["MEM"].get_bottom(), mem.get_right() + UP * 0.2, buff=0.1, color=INF, stroke_width=3)
        clash = label(r"a load in MEM \ and a fetch in IF, \ in the same cycle", font_size=24, color=NO).next_to(
            mem, DOWN, buff=0.3)
        res = VGroup(
            label(rf"in the Job, \ {100 * frac:.0f}\% of instructions are loads or stores: \ with one port, \ "
                  rf"CPI $+\,{frac:.2f}$", font_size=24, color=GREY_A),
            label(r"the cure: \ separate instruction and data memories \ (in practice, \ two caches: \ Part 9)",
                  font_size=24, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The commonest structural hazard is memory. <bookmark mark='a'/> The fetch stage reads an instruction from "
            "memory in every cycle, and the memory stage reads or writes data whenever a load or store reaches it. "
            "With a single memory that serves one request per cycle, the two collide, and the fetch must wait. "
            "<bookmark mark='b'/> In the Job, about a fifth of all instructions are loads or stores, so one shared "
            "memory port would add about a fifth of a cycle to every instruction. <bookmark mark='c'/> The cure is to "
            "duplicate the hardware: separate memories for instructions and data. Real processors keep one main memory "
            "but give each stage its own cache in front of it, which is part of Part 9's story."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fig))
            vo.wait_until("a")
            self.play(FadeIn(mem), GrowArrow(a1), GrowArrow(a2))
            self.play(FadeIn(clash), Indicate(mem, color=NO))
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            vo.wait_until("c")
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def divider(self):
        d = load("charts")["divide"]
        st = load("stages")
        hz = load("hazards")["structural"]
        head = label(r"A unit that is busy for many cycles", font_size=36).to_edge(UP, buff=0.3)
        pc = PipeChart(d, cycles=min(d["cycles"], 26), cw=0.36, ch=0.42, font_size=12, label_size=15,
                       label_width=2.6).move_to(UP * 0.6)
        notes = VGroup(
            label(r"Part 4's SRT divider: \ two quotient bits per cycle, \ 16 cycles, \ not pipelined", font_size=22,
                  color=FUNC),
            label(r"while it works, \ EX is occupied, \ and everything behind waits", font_size=22, color=NO),
            label(rf"Part 4's multiplier, \ in contrast, \ settles in {st['mul_gates']} gate delays: \ it fits in EX "
                  r"\ (the memories set the cycle)", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part 7 also gives Pebble multiply and divide instructions, from Part 4's circuits, and the divider brings "
            "a structural hazard of its own. <bookmark mark='a'/> Part 4's SRT divider produces two quotient bits per "
            "cycle, so a thirty-two-bit division occupies the execute stage for sixteen cycles. It is not pipelined: "
            "while it works, the instruction behind it cannot enter EX, and the whole front of the pipeline waits. "
            "Here the add after the divide sits in decode for fifteen extra cycles. <bookmark mark='b'/> The "
            "multiplier is different. Part 4's Dadda tree settles in a few dozen gate delays, comfortably inside a "
            "cycle set by the memories, so a multiply costs no more than an add. Designers pipeline or duplicate the "
            "units that are used often, and let the rare ones stall."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pc.heads), FadeIn(VGroup(*pc.rows.values())))
            vo.wait_until("a")
            for c in range(pc.ncycles):
                if c in pc.columns:
                    self.play(FadeIn(pc.columns[c]), run_time=0.18)
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()
