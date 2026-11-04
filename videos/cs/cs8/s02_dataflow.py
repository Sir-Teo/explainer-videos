from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, KIND_COLOR, NO, PART, YES, dag_figure,
                                  fmt, load, mono, slot_grid)

SCAN = ["scan:  beq  a2, s1, insert   # every entry looked at?",
        "       lw   t1, 4(t0)        # this entry's length",
        "       bne  t1, a1, next     # not the word's length: skip it",
        "next:  addi t0, t0, 12       # the next entry",
        "       addi a2, a2, 1",
        "       j    scan"]


class Dataflow(VoiceoverScene):
    def construct(self):
        self.card()
        self.loop()
        self.graph()
        self.widths()
        self.bounds()

    def card(self):
        card = chapter_card(1, r"The dataflow limit", r"How fast could a program possibly run?", lit=(1966, 1974),
                            extra=((1966, r"Graham's bound"), (1974, r"Dennis's dataflow machine")), part=PART)
        with self.voiceover("Chapter one. The dataflow limit."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def loop(self):
        head = label(r"The loop where the Job spends its time", font_size=36).to_edge(UP, buff=0.35)
        code = VGroup(*[mono(s, 20) for s in SCAN]).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(UP * 0.6)
        facts = VGroup(
            label(r"six instructions per table entry, \ for every word read", font_size=24, color=GREY_A),
            label(r"Part 7's pipeline: \ 7 cycles a trip \ (a load-use bubble)", font_size=24, color=NO),
            label(r"question: \ how few cycles could \textit{any} machine take?", font_size=26, color=HEAD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In Part 7 we found where the Job spends its time: in one small loop, the scan of the word table. For "
            "every word it reads, the Job walks the table entry by entry, skipping each entry whose length differs "
            "from the word's. <bookmark mark='a'/> Six instructions a trip: test whether the table is finished, load "
            "this entry's length, compare it, step to the next entry, count, and jump back. <bookmark mark='b'/> On "
            "the pipeline a trip took seven cycles. <bookmark mark='c'/> So here is this chapter's question. Forget "
            "pipelines and forget hardware. If a machine could start any instruction the moment its inputs exist, "
            "how fast could this loop go?"
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c) for c in code], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def graph(self):
        d = load("dataflow")
        head = label(r"Four trips as a dataflow graph", font_size=36).to_edge(UP, buff=0.3)
        g = dag_figure(d, dx=1.55, dy=0.62, font_size=15).move_to(DOWN * 0.1)
        T = max(d["asap"][i] for i in g.nodes) + 1
        x0 = min(n.get_x() for n in g.nodes.values())
        axis = VGroup(*[label(rf"cycle {t}", font_size=18, color=GREY_B).move_to([x0 + t * 1.55, -2.75, 0])
                        for t in range(T)])
        leg = VGroup(*[VGroup(Square(side_length=0.2, stroke_width=0, fill_color=c, fill_opacity=0.8),
                              label(t, font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.1)
                       for t, c in ((r"load", KIND_COLOR["load"]), (r"branch", KIND_COLOR["branch"]),
                                    (r"arithmetic", KIND_COLOR["alu"]))]).arrange(RIGHT, buff=0.4)
        jumps = note(r"(and four jumps, \ which depend on nothing)", font_size=18)
        foot = VGroup(leg, jumps).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.15)
        trips = VGroup()
        for k in range(4):
            trips.add(VGroup(*[g.nodes[i] for i in range(6 * k, 6 * k + 6) if i in g.nodes]))
        cp = d["critical"]
        cp_len = d["asap"][cp[-1]] + d["nodes"][cp[-1]]["lat"]
        crit = label(rf"the critical path: \ {cp_len} cycles, \ through \texttt{{addi t0, t0, 12}}", font_size=26,
                     color=HEAD).next_to(head, DOWN, buff=0.12)
        with self.voiceover(
            "Draw each instruction as a node, and an arrow from the instruction that produces a value to each one "
            "that uses it. This is the program's dataflow graph: the only order that really matters. <bookmark "
            "mark='a'/> Here are four trips round the loop, each instruction placed in the earliest cycle it could "
            "start. Loads take two cycles, everything else one. The four jumps depend on nothing at all, so they are "
            "left out of the picture. <bookmark mark='b'/> The load of an entry's length needs only the entry's "
            "address, and the branch needs only the load. <bookmark mark='c'/> And the address of the next entry "
            "needs only the address of this one. That is the chain that runs through all four trips: one add per "
            "trip, each waiting for the last. <bookmark mark='d'/> The longest chain of dependences through the graph "
            "is called the critical path. Here it is six cycles long, so no machine, however wide, can do these four "
            "trips in fewer than six cycles. The pipeline took twenty-eight."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(axis), LaggedStart(*[FadeIn(t) for t in trips], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(g.edge_group), run_time=2.0)
            vo.wait_until("c")
            chain = VGroup(*[g.nodes[6 * k + 3] for k in range(4)])
            self.play(LaggedStart(*[Indicate(n, color=HEAD, scale_factor=1.15) for n in chain], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(Create(g.critical), run_time=1.5)
            self.play(FadeIn(crit))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def widths(self):
        d = load("dataflow")
        head = label(r"A machine of width $W$: \ $W$ slots a cycle", font_size=36).to_edge(UP, buff=0.3)
        rows = [("1", d["widths"]["1"]["cycles"]), ("2", d["widths"]["2"]["cycles"]),
                ("4", d["widths"]["4"]["cycles"]), ("8", d["widths"]["8"]["cycles"]),
                (r"$\infty$", d["widths"]["inf"]["cycles"]), (r"in order, \ 1 wide", d["in_order"]["cycles"])]
        table = VGroup()
        for w, c in rows:
            table.add(VGroup(label(rf"width {w}" if "order" not in w else w, font_size=22, color=GREY_A),
                             label(rf"{c} cycles", font_size=22, color=HEAD)).arrange(RIGHT, buff=0.4))
        table.arrange(DOWN, aligned_edge=RIGHT, buff=0.12).to_corner(DR, buff=0.4)
        grids = {}
        for key in ("1", "2", "4", "8"):
            w = int(key)
            cw = 0.5 if w == 1 else 0.8
            gr = slot_grid(d, d["widths"][key]["start"], w, cw=cw, ch=0.5, font_size=14)
            gr.move_to(UP * 0.3).to_edge(LEFT, buff=0.5)
            grids[key] = gr
        cap = {k: label(rf"width {k}: \ {d['widths'][k]['cycles']} cycles", font_size=26, color=HEAD) for k in grids}
        for k, c in cap.items():
            c.next_to(grids[k], DOWN, buff=0.3).align_to(grids[k], LEFT)
        with self.voiceover(
            "The critical path assumes a machine that can start as many instructions in a cycle as it likes. Real "
            "machines have a width: so many instructions a cycle, and no more. Picture the machine as a grid, one "
            "row for each slot, one column for each cycle. <bookmark mark='a'/> One wide, the twenty-four "
            "instructions, jumps included, need twenty-four cycles. <bookmark mark='b'/> Two wide: twelve. <bookmark "
            "mark='c'/> Four wide: seven, one more than the critical path. <bookmark mark='d'/> Eight wide: six, and "
            "now most slots are empty; the width no longer matters, only the chain does. <bookmark mark='e'/> Two "
            "things bound the time, then: the work divided by the width, and the length of the longest chain."
        ) as vo:
            self.play(FadeIn(head))
            prev = None
            for mk, key, row in (("a", "1", 0), ("b", "2", 1), ("c", "4", 2), ("d", "8", 3)):
                vo.wait_until(mk)
                gr = grids[key]
                if prev is None:
                    self.play(FadeIn(gr.frame), LaggedStart(*[FadeIn(gr.cells[i]) for i in range(24)],
                                                            lag_ratio=0.05), FadeIn(cap[key]), FadeIn(table[row]))
                else:
                    p = grids[prev]
                    self.play(FadeOut(p.frame), FadeIn(gr.frame), *[Transform(p.cells[i], gr.cells[i])
                                                                    for i in range(24)],
                              Transform(cap[prev], cap[key]), FadeIn(table[row]), run_time=1.6)
                    grids[key] = p
                    p.frame = gr.frame
                    cap[key] = cap[prev]
                prev = key
            vo.wait_until("e")
            self.play(FadeIn(table[4]), FadeIn(table[5]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bounds(self):
        d = load("dataflow")
        head = label(r"Work, \ span, \ and width", font_size=38).to_edge(UP, buff=0.35)
        law = MathTex(r"\max\!\left(\frac{N}{W},\; L\right)", r"\;\le\;", r"T_W", r"\;\le\;", r"\frac{N}{W} + L",
                      font_size=52).move_to(UP * 1.4)
        law[0].set_color(FUNC)
        law[4].set_color(CTRL)
        keys = VGroup(
            label(r"$N$: \ instructions \ (the work) \qquad $L$: \ the critical path \ (the span) \qquad $W$: \ "
                  r"the width", font_size=24, color=GREY_A),
            label(r"left: \ no machine can do better \qquad right: \ any greedy machine does at least this well",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(law, DOWN, buff=0.4)
        check = VGroup(*[label(rf"$W = {w}$: \ ${max(24 / w, 6):g} \le {d['widths'][str(w)]['cycles']} \le "
                               rf"{24 / w + 6:g}$", font_size=24, color=c)
                         for w, c in ((1, GREY_B), (2, GREY_B), (4, HEAD), (8, GREY_B))]).arrange(DOWN, buff=0.12)
        check.next_to(keys, DOWN, buff=0.35)
        loop = label(r"in a loop, \ the chain sets a rate: \ one trip per cycle \ $\Rightarrow$ \ 6 instructions per "
                     r"cycle, \ against the pipeline's 0.86", font_size=24, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Those two bounds have names. The number of instructions is the work, N. The critical path is the span, "
            "L. With a width W, <bookmark mark='a'/> no schedule can take fewer cycles than the work divided by the "
            "width, and none can beat the span. <bookmark mark='b'/> And there is a matching upper bound, proved by "
            "Ronald Graham in 1966 for scheduling jobs on machines: any greedy schedule, one that never leaves a "
            "slot idle while some instruction is ready, finishes within N over W plus L. The greedy schedule is never "
            "worse than twice the best. <bookmark mark='c'/> Our four trips obey both, at every width. <bookmark "
            "mark='d'/> And in a loop the span becomes a rate. The longest chain gains one add per trip, so in the "
            "steady state the loop could run one trip per cycle, six instructions a cycle. The pipeline manages zero "
            "point eight six. Between those numbers lies everything this part is about."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(law[0]), FadeIn(law[1]), FadeIn(law[2]), FadeIn(keys[0]))
            vo.wait_until("b")
            self.play(FadeIn(law[3]), FadeIn(law[4]), FadeIn(keys[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in check], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(loop))
        self.wait(0.3)
        self.clear_scene()
