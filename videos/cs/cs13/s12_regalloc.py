from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, FUNC, HEAD, NO, PALETTE, PART, YES, bar_chart, code, graph,
                                   grid_table, load, mono)


def demo_graph(colors=None, radius=2.55, at=LEFT * 3.0):
    d = load("regalloc")["demo"]
    nodes = [n for n in d["nodes"]]
    g = graph(nodes, [tuple(e) for e in d["edges"]], colors=colors, radius=radius, node_r=0.3, font_size=13)
    g.shift(at + DOWN * 0.25)
    return g


class RegAlloc(VoiceoverScene):
    def construct(self):
        self.card()
        self.interference()
        self.colouring()
        self.chaitin()
        self.hard()
        self.chordal()
        self.hole()
        self.sweep()

    def card(self):
        card = chapter_card(11, r"Register allocation", r"Thirteen registers: \ which value goes where?",
                            lit=(1981,), extra=((1981, r"Chaitin: \ allocation by colouring"),), part=PART)
        with self.voiceover("Chapter eleven. Register allocation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def interference(self):
        d = load("regalloc")["demo"]
        head = label(r"Who may share a register?", font_size=34).to_edge(UP, buff=0.3)
        body = next(b for b in d["func"]["blocks"] if b["label"] == "body1")
        src = code([b["label"] + ":" for b in d["func"]["blocks"][:1]] +
                   ["  " + l for l in d["func"]["blocks"][0]["ins"]] +
                   [x for b in d["func"]["blocks"][1:] for x in [b["label"] + ":"] + ["  " + l for l in b["ins"]]],
                   size=12, color=CODE).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.3)
        g = demo_graph()
        rule = VGroup(
            label(r"two values \textbf{interfere} if both are live at the same point", font_size=21, color=GREY_A),
            label(r"interfering values need different registers", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(head, DOWN, buff=0.3).to_edge(LEFT, buff=0.5)
        stats = label(rf"\texttt{{total}}, \ optimized, \ in SSA: \ {len(d['nodes'])} values, \ "
                      rf"{len(d['edges'])} interferences", font_size=20, color=YES).to_edge(DOWN, buff=0.3).to_edge(
            LEFT, buff=0.5)
        e = ("%s.2", "%t10")
        both = VGroup(g.nodes[e[0]], g.nodes[e[1]])
        with self.voiceover("After selection, total uses seventeen virtual registers. Pebble has thirteen it may allocate, and bigger functions use hundreds. Which values may share a register? <bookmark mark='a'/> Two values interfere if both are live at the same point: both still needed. Then they need different registers. Values that never live at the same time can share one. <bookmark mark='b'/> Here is total after optimization, in SSA form. Notice the strength-reduced pointer i v two, stepping by four. <bookmark mark='c'/> Draw a node for each value and an edge for each pair that interferes, and you have the interference graph: seventeen nodes, forty-one edges. <bookmark mark='d'/> For instance, s dot two, the running sum, is still live when t ten is loaded, so they interfere.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(rule), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(src))
            vo.wait_until('c')
            self.play(Create(g.edges), *[FadeIn(n) for n in g.nodes.values()], run_time=2.5)
            self.play(FadeIn(stats))
            vo.wait_until('d')
            idx = [k for k, ed in enumerate(load('regalloc')['demo']['edges']) if tuple(ed) == e][0]
            self.play(Indicate(both, color=HEAD), g.edges[idx].animate.set_color(HEAD).set_stroke(width=4))
        self.wait(0.3)
        self.clear_scene()

    def colouring(self):
        d = load("regalloc")["demo"]
        head = label(r"Register allocation is graph colouring", font_size=34).to_edge(UP, buff=0.3)
        g = demo_graph()
        side = VGroup(
            label(r"registers $=$ colours", font_size=22, color=GREY_A),
            label(r"adjacent nodes get different colours", font_size=22, color=GREY_A),
            label(rf"this graph: \ {max(d['colors'].values()) + 1} colours", font_size=24, color=YES),
            label(rf"and no fewer will do: \ it contains {d['omega']} values all live at once", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.6)
        order = sorted(d["nodes"], key=lambda n: (d["colors"][n], n))
        with self.voiceover(
            "So the problem becomes a famous one. <bookmark mark='a'/> Give each register a colour. Assign every "
            "node a colour so that no edge joins two nodes of the same colour, and you have assigned every value a "
            "register so that no two values needed at once share one. <bookmark mark='b'/> Our allocator colours "
            "this graph with five colours. <bookmark mark='c'/> And five is the minimum, because the graph contains "
            "a clique of five: five values all live at the same moment, each adjacent to all the others."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(side[:2]))
            vo.wait_until("b")
            # Overlap the color fades and fit them before the actual next spoken cue.
            budget = vo.start + vo.mark_time("c") - self.renderer.time
            reveal_time = min(2.4, max(0.4, budget - 0.6))
            colors = []
            for n in order:
                c = PALETTE[d["colors"][n] % len(PALETTE)]
                colors.append(g.nodes[n][0].animate.set_fill(c, 0.6).set_stroke(c))
            self.play(LaggedStart(*colors, lag_ratio=0.12), run_time=reveal_time)
            self.play(FadeIn(side[2]), run_time=0.4)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def chaitin(self):
        head = label(r"Chaitin's allocator \ (IBM, 1981)", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"\textbf{simplify}: \ a node with fewer than $k$ neighbours can always be coloured last;",
                  font_size=21, color=GREY_A),
            label(r"remove it, \ push it on a stack, \ repeat \ (Kempe's trick, \ 1879)", font_size=21, color=GREY_A),
            label(r"\textbf{spill}: \ if every node has $\ge k$ neighbours, \ pick one to live in memory:", font_size=21,
                  color=NO),
            label(r"cheapest: \ few uses, \ many neighbours, \ not in a loop", font_size=21, color=NO),
            label(r"\textbf{select}: \ pop the stack, \ give each node a colour its neighbours lack", font_size=21,
                  color=YES),
            label(r"\textbf{coalesce}: \ merge the two ends of a copy, \ if it stays colourable \ (Briggs, \ George)",
                  font_size=21, color=CTRL),
            label(r"\textbf{rematerialize}: \ a constant or an address is recomputed, \ not stored", font_size=21,
                  color=FUNC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        spill = code(["sw   t1, 8(sp)    # after the definition", "...", "lw   t1, 8(sp)    # before each use"],
                     size=16, color=NO).to_edge(DOWN, buff=0.4).to_edge(RIGHT, buff=0.8)
        with self.voiceover("Gregory Chaitin and his colleagues at IBM built the first allocator of this kind in 1981. <bookmark mark='a'/> Simplify: suppose a node has fewer neighbours than there are registers. However its neighbours are coloured, one colour is left for it. So remove it, push it on a stack, and repeat on the smaller graph. Kempe used the same trick in 1879, in a flawed proof of the four colour theorem. <bookmark mark='b'/> If every remaining node has too many neighbours, pick one to spill: it lives in memory, stored after each definition and loaded before each use. Choose the cheapest, a value used rarely, with many neighbours, outside any loop. <bookmark mark='c'/> Select: pop the nodes back off the stack and give each a colour its neighbours do not have. <bookmark mark='d'/> Two refinements matter a great deal. Coalescing merges the two ends of a copy into one node, so the copy disappears; this is how the copies left by phis vanish. Briggs and George gave tests for when merging is safe. <bookmark mark='e'/> And rematerialization: a value that is a constant or an address need not be stored at all, only recomputed where it is needed.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(steps[:2]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(steps[2:4]), FadeIn(spill))
            vo.wait_until('c')
            self.play(FadeIn(steps[4]))
            vo.wait_until('d')
            self.play(FadeIn(steps[5]))
            vo.wait_until('e')
            self.play(FadeIn(steps[6]))
        self.wait(0.3)
        self.clear_scene()

    def hard(self):
        head = label(r"In general: \ NP-hard", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"can a graph be coloured with $k$ colours? \ NP-complete \ (Karp, \ 1972), \ even for $k = 3$",
                  font_size=22, color=GREY_A),
            label(r"Chaitin: \ \textit{every} graph is the interference graph of some program", font_size=22,
                  color=GREY_A),
            label(r"so optimal register allocation, \ in general, \ is NP-hard", font_size=24, color=NO),
            label(r"what NP-hard means, \ and why it is believed to be truly hard: \ Part 26", font_size=21,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.6)
        prog = code(["a = ...;  b = ...;", "use(a, b);        // edge a-b", "c = ...;", "use(b, c);        // edge b-c",
                     "..."], size=18).next_to(pts, DOWN, buff=0.5)
        with self.voiceover("Why use allocation heuristics? <bookmark mark='a'/> General graph k-colorability is NP-complete when k is part of the input, and remains NP-complete for each fixed k of at least three. One and two colors have easier tests. <bookmark mark='b'/> Chaitin's register-allocation work connects sufficiently general programs to arbitrary interference graphs. The code sketch suggests pairwise conflicts; it is not the full reduction, which must also control every unintended live overlap. <bookmark mark='c'/> Thus the general uniform-register allocation problem contains hard instances. Particular program forms and register models can be easier, as strict SSA will show. Spilling, physical-register constraints and copy costs add further objectives. <bookmark mark='d'/> Part 26 explains these complexity claims and why polynomial special cases do not contradict general NP-hardness.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(pts[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts[1]), FadeIn(prog))
            vo.wait_until('c')
            self.play(FadeIn(pts[2]))
            vo.wait_until('d')
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def chordal(self):
        ra = load("regalloc")
        head = label(r"But on SSA programs: \ easy", font_size=34).to_edge(UP, buff=0.3)
        defs = VGroup(
            label(r"a graph is \textbf{chordal} if every cycle of 4 or more nodes has a shortcut, \ a chord",
                  font_size=21, color=GREY_A),
            label("\\textbf{strict SSA}: dominating definitions, phi-edge uses, interchangeable registers", font_size=21, color=HEAD),
            label(r"why: \ each SSA value is live on a subtree of the dominator tree, \ and subtrees of a tree "
                  r"intersect chordally \ (Gavril 1974)", font_size=20, color=GREY_A),
            label("perfect elimination order + reverse greedy coloring: optimal in the explicit graph model", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        rows = [[r["func"], str(r["ssa_nodes"]), "yes" if r["ssa_chordal"] else "no", str(r["omega"]),
                 str(r["after_nodes"]), "yes" if r["after_chordal"] else "no"] for r in ra["chordal"]]
        cols = [[WHITE, WHITE, YES if r["ssa_chordal"] else NO, WHITE, WHITE, YES if r["after_chordal"] else NO]
                for r in ra["chordal"]]
        tab = grid_table([r"function", r"SSA values", r"chordal?", r"colours", r"after SSA", r"chordal?"], rows,
                         widths=[1.8, 1.7, 1.4, 1.3, 1.7, 1.4], row_h=0.42, font_size=18, colors=cols,
                         mono_cols=(0,)).next_to(defs, DOWN, buff=0.45).set_x(0)
        cap = label(r"every function of the list Job, \ checked by our compiler", font_size=19,
                    color=GREY_B).next_to(tab, DOWN, buff=0.15)
        with self.voiceover("Strict SSA reveals a useful special case. <bookmark mark='a'/> A graph is chordal when every cycle of at least four vertices has a chord between nonconsecutive vertices. <bookmark mark='b'/> The SSA allocation results of Hack and colleagues, and related independent work, show chordality for the interference model with each definition dominating its uses and phi operands treated on incoming edges. <bookmark mark='c'/> A value's live region can then be represented as a subtree of the suitably detailed dominator tree. Intersecting such subtrees produces a chordal graph. <bookmark mark='d'/> A perfect elimination order followed by greedy coloring in reverse uses exactly the clique number. Suitable algorithms run in the explicit graph's vertices plus edges. This assumes interchangeable registers and excludes extra physical-register constraints, spilling and coalescing costs. <bookmark mark='e'/> The recorded tables compare our SSA graphs with the graphs after phi copies are inserted. Leaving SSA can destroy chordality, even though the program still computes the same result.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(defs[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(defs[1]))
            vo.wait_until('c')
            self.play(FadeIn(defs[2]))
            vo.wait_until('d')
            self.play(FadeIn(defs[3]))
            vo.wait_until('e')
            self.play(FadeIn(tab), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def hole(self):
        ra = load("regalloc")
        head = label(r"What leaving SSA breaks", font_size=34).to_edge(UP, buff=0.3)
        cyc = [c.replace("%", "") for c in ra["hole"]["cycle"]]
        pos = {cyc[0]: (-1.6, 1.4), cyc[1]: (1.6, 1.4), cyc[2]: (1.6, -1.4), cyc[3]: (-1.6, -1.4)}
        nodes = {}
        for n, (x, y) in pos.items():
            c = Circle(radius=0.55, stroke_color=NO, fill_color=NO, fill_opacity=0.2).move_to([x - 2.5, y - 0.3, 0])
            nodes[n] = VGroup(c, mono(n, 18, WHITE).move_to(c))
        es = VGroup(*[Line(nodes[a][0].get_center(), nodes[b][0].get_center(), buff=0.55, color=NO, stroke_width=3)
                      for a, b in zip(cyc, cyc[1:] + cyc[:1])])
        miss = VGroup(DashedLine(nodes[cyc[0]][0].get_center(), nodes[cyc[2]][0].get_center(), buff=0.55,
                                 color=GREY_D),
                      DashedLine(nodes[cyc[1]][0].get_center(), nodes[cyc[3]][0].get_center(), buff=0.55,
                                 color=GREY_D))
        txt = VGroup(
            label(rf"in \texttt{{{ra['hole']['func']}}}, \ after the $\phi$s become copies:", font_size=21,
                  color=GREY_A),
            label(r"a 4-cycle with no chord: \ a hole", font_size=22, color=NO),
            label(r"the primed values are the copies, \ placed on the loop's back edge", font_size=20,
                  color=GREY_A),
            label(r"so allocate \textit{before} leaving SSA, \ and coalesce the copies afterwards", font_size=21,
                  color=YES),
            label(r"allocators built this way: \ libFirm \ (Hack's own compiler)", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.5)
        with self.voiceover("Here is what goes wrong. <bookmark mark='a'/> In the function same, after the phis become copies on the loop's back edge, these four values form a cycle: each interferes with the next. <bookmark mark='b'/> But neither diagonal is an edge. A cycle of four with no chord is a hole, and the graph is no longer chordal. The primed values are the copies, which overlap the originals they copy. <bookmark mark='c'/> The lesson for compiler writers is to colour while the program is still in SSA form, where it is easy, and deal with the copies afterwards, by coalescing. The libFirm compiler, Hack's own, is built this way; LLVM and GCC leave SSA first and rely on heuristics.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(*[FadeIn(n) for n in nodes.values()], FadeIn(txt[0]), run_time=0.6)
            vo.wait_until('a')
            self.play(Create(es), run_time=1.5)
            vo.wait_until('b')
            self.play(Create(miss), FadeIn(txt[1:3]))
            vo.wait_until('c')
            self.play(FadeIn(txt[3:]))
        self.wait(0.3)
        self.clear_scene()

    def sweep(self):
        ra = load("regalloc")
        sw = ra["sweep"]
        head = label(r"Fewer registers, \ more work", font_size=34).to_edge(UP, buff=0.3)
        ch = bar_chart([r["steps"] / 1e6 for r in sw], [rf"$k = {r['k']}$" for r in sw],
                       [YES, YES, CTRL, CTRL, NO, NO], height=3.6, bar_w=0.7, gap=0.35,
                       fmt_=lambda v: f"{v:.2f}M", font_size=18).move_to(LEFT * 3.6 + DOWN * 0.4)
        yl = label(r"instructions, \ list Job, \ chapter 1", font_size=18, color=GREY_B).next_to(ch, UP, buff=0.25)
        sp = VGroup(*[label(rf"{r['spills']} spilled", font_size=15, color=NO if r["spills"] else GREY_B).next_to(
            ch.names[k], DOWN, buff=0.12) for k, r in enumerate(sw)])
        side = VGroup(
            label(r"fewer registers: \ more copies survive, \ more values saved around calls", font_size=19,
                  color=GREY_A),
            label(r"at 5 and 4, \ values spill to memory", font_size=19, color=NO),
            label(r"heuristics are not monotone: \ the one spill at 13 vanishes at 6", font_size=19, color=GREY_A),
            label(r"\textbf{linear scan} \ (Poletto and Sarkar, \ 1999): \ live ranges as intervals, \ one pass;",
                  font_size=19, color=FUNC),
            label("compile-time and code-quality tradeoffs depend on the allocator and workload", font_size=19, color=FUNC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        if side.width > 6.0:
            side.scale_to_fit_width(6.0)
        side.to_edge(RIGHT, buff=0.35).shift(UP * 0.2)
        with self.voiceover("The register sweep recompiles the same list Job with different register budgets. <bookmark mark='a'/> Read executed instructions and spill counts separately. Fewer registers can leave more copies, require more saves around calls, or force loads and stores. The plotted totals belong to this first-chapter input. <bookmark mark='b'/> The heuristic's choices are not monotone: a spill can disappear when a smaller budget changes ordering and coalescing decisions. That observation is about this allocator, not an optimality theorem. <bookmark mark='c'/> Linear scan, associated with Poletto and Sarkar's 1999 work, trades different analysis and allocation costs by processing live intervals. It is widely used in just-in-time settings, with many refinements. Relative compile time and generated-code quality depend on the algorithms and workload; one is not uniformly faster or worse than every graph-coloring allocator.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(ch), FadeIn(yl), FadeIn(sp), FadeIn(side[:2]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(side[2]))
            vo.wait_until('c')
            self.play(FadeIn(side[3:]))
        self.wait(0.3)
        self.clear_scene()
