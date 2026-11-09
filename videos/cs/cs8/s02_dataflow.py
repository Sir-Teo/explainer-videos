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
        card = chapter_card(1, r"The dataflow limit", "What do explicit dependencies and resources permit?", lit=(1966, 1974),
                            extra=((1966, r"Graham's bound"), (1974, r"Dennis's dataflow machine")), part=PART)
        with self.voiceover("Chapter one. The dataflow limit."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def loop(self):
        head = label(r"The loop where the Job spends its time", font_size=36).to_edge(UP, buff=0.35)
        code = VGroup(*[mono(s, 20) for s in SCAN]).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(UP * 0.6)
        facts = VGroup(
            label("six instructions: \\ the mismatched-length fast path", font_size=24, color=GREY_A),
            label("pipeline: \\ 7 steady-state cycles; \\ warm correct prediction", font_size=24, color=NO),
            label("question: how fast under the stated oracle model?", font_size=26, color=HEAD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "This is the Job's table-scan fast path when an entry's length differs from the word being searched. "
            "Matching lengths need additional letter comparisons, and reaching the insertion point follows another "
            "path. <bookmark mark='a'/> The displayed path has six instructions: table-end test, length load, "
            "comparison, two increments and a jump. <bookmark mark='b'/> With warm correct direction and target "
            "prediction, Part 7's pipeline takes seven steady-state cycles per such trip, including a load-use "
            "bubble. <bookmark mark='c'/> Now hold this known path fixed. Give its instructions explicit latencies "
            "and ask how overlapping their true dependencies changes the schedule. This idealization assumes the "
            "future path and relevant memory information are already known."
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
        jumps = note("(four register-independent jumps; \\ path supplied by the oracle)", font_size=18)
        foot = VGroup(leg, jumps).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.15)
        trips = VGroup()
        for k in range(4):
            trips.add(VGroup(*[g.nodes[i] for i in range(6 * k, 6 * k + 6) if i in g.nodes]))
        cp = d["critical"]
        cp_len = d["asap"][cp[-1]] + d["nodes"][cp[-1]]["lat"]
        crit = label(rf"the critical path: \ {cp_len} cycles, \ through \texttt{{addi t0, t0, 12}}", font_size=26,
                     color=HEAD).next_to(head, DOWN, buff=0.12)
        with self.voiceover(
            "Each node is an instruction. An arrow connects a value's producer to an instruction that uses it. "
            "These arrows describe register data dependencies for this fixed path; real execution also has memory, "
            "control, resource and exception constraints. <bookmark mark='a'/> Place four trips at their earliest "
            "starts with unlimited resources. Loads take two cycles and the other displayed operations take one. "
            "The jumps have no register predecessors in this oracle graph. <bookmark mark='b'/> A length load needs "
            "its entry address, and the comparison waits for that load. <bookmark mark='c'/> The next entry address "
            "comes from a one-cycle increment of the previous address. <bookmark mark='d'/> The highlighted longest "
            "weighted chain, ending at the last comparison, spans six cycles. Under these dependencies and "
            "latencies, no valid schedule finishes the four trips sooner. The corresponding single-start, in-order "
            "schedule takes twenty-eight cycles; this is a scoped schedule comparison."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            self.play(FadeIn(axis), LaggedStart(*[FadeIn(t) for t in trips], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("a")
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
            "In this ideal scheduler, width W limits how many operations may start each cycle. It does not limit "
            "how many earlier operations remain in flight, and execution units are otherwise unlimited. <bookmark "
            "mark='a'/> One start slot gives twenty-four cycles for twenty-four instructions, including jumps. "
            "<bookmark mark='b'/> Two slots give twelve cycles. <bookmark mark='c'/> Four give seven. <bookmark "
            "mark='d'/> Eight give six, reaching this graph's weighted critical path. These are the computed "
            "schedules for four fixed fast-path trips. <bookmark mark='e'/> Two immediate lower bounds apply: at "
            "least the instruction count divided by start width, rounded up, and at least the longest dependency "
            "chain. Real cores need additional front-end, unit, ordering and retirement constraints."
        ) as vo:
            self.play(FadeIn(head))
            prev = None
            for mk, key, row in (("a", "1", 0), ("b", "2", 1), ("c", "4", 2), ("d", "8", 3)):
                if mk != "a":
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
                if mk == "a":
                    vo.wait_until(mk)
            vo.wait_until("e")
            self.play(FadeIn(table[4]), FadeIn(table[5]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bounds(self):
        d = load("dataflow")
        head = label(r"Work, \ span, \ and width", font_size=38).to_edge(UP, buff=0.35)
        law = MathTex(r"\max\!\left(\left\lceil\frac{N}{W}\right\rceil,\; L\right) \le T_W",
                      font_size=42, color=FUNC).move_to(UP * 1.85)
        graham = MathTex(r"T_G \le \frac{A}{W}+\left(1-\frac{1}{W}\right)L",
                         font_size=40, color=CTRL).move_to(UP * 0.2)
        keys = VGroup(
            label(r"start-slot model: $N=24$ instructions, $L=6$ cycles; $W$ starts/cycle",
                  font_size=22, color=GREY_A).next_to(law, DOWN, buff=0.22),
            label(r"Graham: nonpreemptive jobs on $W$ processors; $A=28$ processing cycles",
                  font_size=22, color=GREY_A).next_to(graham, DOWN, buff=0.22),
        )
        check = VGroup(*[MathTex(rf"W={w}:\quad {max((24+w-1)//w,6)}\le {d['widths'][str(w)]['cycles']}",
                                  font_size=26, color=c)
                         for w, c in ((1, GREY_B), (2, GREY_B), (4, HEAD), (8, GREY_B))]).arrange(RIGHT, buff=0.45)
        check.move_to(DOWN * 1.6)
        loop = label(r"fixed fast path, unlimited resources and known path: \\ one trip/cycle after startup; not whole-program IPC",
                     font_size=23, color=YES).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Keep the resource model explicit. N counts instructions, L is the longest latency-weighted path, and W "
            "is the number of starts permitted each cycle. <bookmark mark='a'/> Every schedule in this start-slot "
            "model needs at least the larger of ceiling N over W and L. <bookmark mark='b'/> Graham's classic "
            "list-scheduling result concerns nonpreemptive jobs occupying W processors. Its work is A, the sum of "
            "processing times, and a greedy schedule takes at most A over W plus one minus one over W times L. With "
            "two-cycle loads, A and the instruction count N differ. Do not substitute one for the other when "
            "changing resource models. <bookmark mark='c'/> Our four-trip schedules satisfy the displayed "
            "start-slot lower bounds; they have twenty-four instructions and a six-cycle span. <bookmark mark='d'/> "
            "Across many fixed fast-path trips, the address recurrence permits one trip per cycle in the "
            "unlimited-resource, perfect-path idealization: six instructions per cycle after startup. This is a "
            "model opportunity, not a guarantee for the whole table search."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(law), FadeIn(keys[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(graham), FadeIn(keys[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in check], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(loop))
        self.wait(0.3)
        self.clear_scene()
