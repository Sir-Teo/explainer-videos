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
        with self.voiceover(
            "After selection, total uses seventeen virtual registers. Pebble has thirteen it may allocate, and "
            "bigger functions use hundreds. Which values may share a register? <bookmark mark='a'/> Two values "
            "interfere if both are live at the same point: both still needed. Then they need different registers. "
            "Values that never live at the same time can share one. <bookmark mark='b'/> Here is total after "
            "optimization, in SSA form. Notice the strength-reduced pointer i v two, stepping by four. <bookmark "
            "mark='c'/> Draw a node for each value and an edge for each pair that interferes, and you have the "
            "interference graph: seventeen nodes, forty-one edges. <bookmark mark='d'/> For instance, s dot two, "
            "the running sum, is still live when t ten is loaded, so they interfere."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rule))
            vo.wait_until("b")
            self.play(FadeIn(src))
            vo.wait_until("c")
            self.play(Create(g.edges), *[FadeIn(n) for n in g.nodes.values()], run_time=2.5)
            self.play(FadeIn(stats))
            vo.wait_until("d")
            idx = [k for k, ed in enumerate(load("regalloc")["demo"]["edges"]) if tuple(ed) == e][0]
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
            for n in order:
                c = PALETTE[d["colors"][n] % len(PALETTE)]
                self.play(g.nodes[n][0].animate.set_fill(c, 0.6).set_stroke(c), run_time=0.25)
            self.play(FadeIn(side[2]))
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
        with self.voiceover(
            "Gregory Chaitin and his colleagues at IBM built the first allocator of this kind in 1981. <bookmark "
            "mark='a'/> Simplify: suppose a node has fewer neighbours than there are registers. However its "
            "neighbours are coloured, one colour is left for it. So remove it, push it on a stack, and repeat on "
            "the smaller graph. Kempe used the same trick in 1879, in a flawed proof of the four colour theorem. "
            "<bookmark mark='b'/> If every remaining node has too many neighbours, pick one to spill: it lives "
            "in memory, stored after each definition and loaded before each use. Choose the cheapest, a value used "
            "rarely, with many neighbours, outside any loop. <bookmark mark='c'/> Select: pop the nodes back off "
            "the stack and give each a colour its neighbours do not have. <bookmark mark='d'/> Two refinements "
            "matter a great deal. Coalescing merges the two ends of a copy into one node, so the copy disappears; "
            "this is how the copies left by phis vanish. Briggs and George gave tests for when merging is safe. "
            "<bookmark mark='e'/> And rematerialization: a value that is a constant or an address need not be "
            "stored at all, only recomputed where it is needed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[:2]))
            vo.wait_until("b")
            self.play(FadeIn(steps[2:4]), FadeIn(spill))
            vo.wait_until("c")
            self.play(FadeIn(steps[4]))
            vo.wait_until("d")
            self.play(FadeIn(steps[5]))
            vo.wait_until("e")
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
        with self.voiceover(
            "How good can an allocator be? <bookmark mark='a'/> Deciding whether a graph can be coloured with a given "
            "number of colours is NP-complete, one of Karp's twenty-one problems of 1972, and it stays hard even for "
            "three colours. <bookmark mark='b'/> And Chaitin showed that "
            "every graph is the interference graph of some program. Given any graph, write a program that defines "
            "a value per node and uses each pair of neighbours together. <bookmark mark='c'/> So finding the "
            "fewest registers for an arbitrary program is NP-hard, and allocators settle for heuristics. <bookmark "
            "mark='d'/> What NP-hard means, and why most people believe it really is hard, is Part 26."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]), FadeIn(prog))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def chordal(self):
        ra = load("regalloc")
        head = label(r"But on SSA programs: \ easy", font_size=34).to_edge(UP, buff=0.3)
        defs = VGroup(
            label(r"a graph is \textbf{chordal} if every cycle of 4 or more nodes has a shortcut, \ a chord",
                  font_size=21, color=GREY_A),
            label(r"\textbf{theorem} \ (Hack, Grund, Goos 2006; \ Bouchez; \ Brisk): \ the interference graph of a "
                  r"program in SSA form is chordal", font_size=21, color=HEAD),
            label(r"why: \ each SSA value is live on a subtree of the dominator tree, \ and subtrees of a tree "
                  r"intersect chordally \ (Gavril 1974)", font_size=20, color=GREY_A),
            label(r"chordal graphs colour optimally in linear time: \ eliminate in a perfect order; \ colours "
                  r"$=$ largest clique", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        rows = [[r["func"], str(r["ssa_nodes"]), "yes" if r["ssa_chordal"] else "no", str(r["omega"]),
                 str(r["after_nodes"]), "yes" if r["after_chordal"] else "no"] for r in ra["chordal"]]
        cols = [[WHITE, WHITE, YES if r["ssa_chordal"] else NO, WHITE, WHITE, YES if r["after_chordal"] else NO]
                for r in ra["chordal"]]
        tab = grid_table([r"function", r"SSA values", r"chordal?", r"colours", r"after SSA", r"chordal?"], rows,
                         widths=[1.8, 1.7, 1.4, 1.3, 1.7, 1.4], row_h=0.42, font_size=18, colors=cols,
                         mono_cols=(0,)).next_to(defs, DOWN, buff=0.45)
        cap = label(r"every function of the list Job, \ checked by our compiler", font_size=19,
                    color=GREY_B).next_to(tab, DOWN, buff=0.15)
        with self.voiceover(
            "Then, in 2006, came a surprise. <bookmark mark='a'/> A graph is chordal if every cycle of four or "
            "more nodes has a chord, an edge cutting across it. <bookmark mark='b'/> Sebastian Hack and his "
            "colleagues proved, and Bouchez and Brisk independently, that the interference graph of any program "
            "in SSA form is chordal. <bookmark mark='c'/> The reason is the dominator tree again. In SSA, each "
            "value is defined once, and it is live only on a connected region below its definition: a subtree of "
            "the dominator tree. And graphs made of overlapping subtrees of a tree are always chordal. <bookmark "
            "mark='d'/> Chordal graphs are easy. Order the nodes by maximum cardinality search, colour them "
            "greedily in that order, and you use exactly as many colours as the largest clique, which is the "
            "minimum possible. In linear time. <bookmark mark='e'/> Our compiler checks it on every function of the "
            "Job. In SSA form all five graphs are chordal, and colour optimally. After the phis are turned into "
            "copies, four of the five are no longer chordal."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defs[0]))
            vo.wait_until("b")
            self.play(FadeIn(defs[1]))
            vo.wait_until("c")
            self.play(FadeIn(defs[2]))
            vo.wait_until("d")
            self.play(FadeIn(defs[3]))
            vo.wait_until("e")
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
        with self.voiceover(
            "Here is what goes wrong. <bookmark mark='a'/> In the function same, after the phis become copies on "
            "the loop's back edge, these four values form a cycle: each interferes with the next. <bookmark "
            "mark='b'/> But neither diagonal is an edge. A cycle of four with no chord is a hole, and the graph "
            "is no longer chordal. The primed values are the copies, which overlap the originals they copy. "
            "<bookmark mark='c'/> The lesson for compiler writers is to colour while the program is still in SSA "
            "form, where it is easy, and deal with the copies afterwards, by coalescing. The libFirm compiler, Hack's own, "
            "is built this way; LLVM and GCC leave SSA first and rely on heuristics."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(*[FadeIn(n) for n in nodes.values()], FadeIn(txt[0]))
            self.play(Create(es), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(miss), FadeIn(txt[1:3]))
            vo.wait_until("c")
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
            label(r"a little worse, \ much faster: \ the choice of JIT compilers", font_size=19, color=FUNC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        if side.width > 6.0:
            side.scale_to_fit_width(6.0)
        side.to_edge(RIGHT, buff=0.35).shift(UP * 0.2)
        with self.voiceover(
            "How much do registers matter? We compiled the list Job with fewer and fewer registers available. "
            "<bookmark mark='a'/> With all thirteen it executes seven hundred and sixty-seven thousand "
            "instructions on the first chapter. With ten, eight, then six, the count climbs, because more copies "
            "survive and more values must be saved around calls. At five and four, values begin to spill into "
            "memory, and the count reaches one point one five million, half as much again. <bookmark mark='b'/> "
            "Notice one oddity: the single spill with thirteen registers disappears with six. The heuristics are "
            "not monotone, and real allocators show the same quirks. <bookmark mark='c'/> Just-in-time compilers, "
            "which must compile in milliseconds, often use linear scan instead, from Poletto and Sarkar in 1999. "
            "It treats each live range as an interval, sorts the intervals, and assigns registers in one pass: a "
            "little worse than colouring, and much faster."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(yl), FadeIn(sp), FadeIn(side[:2]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3:]))
        self.wait(0.3)
        self.clear_scene()
