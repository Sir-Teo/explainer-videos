from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, mono, region)

MEM = {"lw", "lbu", "sw", "sb"}


def mi_text(ins):
    op, *args = ins
    args = [a.rstrip(",") for a in args]
    if op in MEM and len(args) == 3:
        return f"{op:<5}{args[0]}, {args[2]}({args[1]})"
    if op == "ret":
        return "ret"
    return f"{op:<5}" + ", ".join(args)


class ISel(VoiceoverScene):
    def construct(self):
        self.card()
        self.tiles()
        self.munch()
        self.dp()
        self.fusion()

    def card(self):
        card = chapter_card(10, r"Instruction selection", r"Which machine instructions say this?", lit=(1976,),
                            extra=((1976, r"Aho--Johnson: \ optimal tree tiling"),), part=PART)
        with self.voiceover("Chapter ten. Instruction selection."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def node(self, txt, c=GREY_A):
        t = mono(txt, 17, WHITE)
        r = RoundedRectangle(width=max(0.8, t.width + 0.3), height=0.48, corner_radius=0.1, stroke_color=c,
                             stroke_width=1.6, fill_color=c, fill_opacity=0.12)
        return VGroup(r, t.move_to(r))

    def tree(self, at):
        n = {"load": self.node("load"), "add": self.node("+"), "shl": self.node("<<"), "a": self.node("%a", CODE),
             "i": self.node("%i", CODE), "2": self.node("2", CODE)}
        n["load"].move_to(at + UP * 1.5)
        n["add"].move_to(at + UP * 0.5)
        n["a"].move_to(at + LEFT * 1.0 + DOWN * 0.5)
        n["shl"].move_to(at + RIGHT * 1.0 + DOWN * 0.5)
        n["i"].move_to(at + RIGHT * 0.4 + DOWN * 1.5)
        n["2"].move_to(at + RIGHT * 1.6 + DOWN * 1.5)
        es = VGroup(*[Line(n[a][0].get_bottom(), n[b][0].get_top(), color=GREY_D, stroke_width=1.5) for a, b in
                      (("load", "add"), ("add", "a"), ("add", "shl"), ("shl", "i"), ("shl", "2"))])
        g = VGroup(es, *n.values())
        g.n = n
        return g

    def tiles(self):
        head = label(r"Covering the IR with machine instructions", font_size=34).to_edge(UP, buff=0.3)
        expr = mono("a[i]   →   load [%a + (%i << 2)]", 20, CODE).next_to(head, DOWN, buff=0.35)
        t = self.tree(LEFT * 3.2 + DOWN * 0.4)
        pats = VGroup(
            VGroup(mono("slli rd, rs, k", 17, YES), label(r"covers \ $\ll$ by a constant", font_size=18,
                                                           color=GREY_A)),
            VGroup(mono("add  rd, rs, rt", 17, CTRL), label(r"covers \ $+$", font_size=18, color=GREY_A)),
            VGroup(mono("lw   rd, k(rs)", 17, FUNC), label(r"covers \ load of $(\cdot + k)$, \ or a plain load",
                                                          font_size=18, color=GREY_A)),
        )
        for p in pats:
            p.arrange(RIGHT, buff=0.4)
        pats.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.0 + UP * 0.4)
        pl = label(r"Pebble's instructions as \textbf{tiles}", font_size=20, color=HEAD).next_to(pats, UP, buff=0.25)
        pl.align_to(pats, LEFT)
        n = t.n
        tile_s = SurroundingRectangle(VGroup(n["shl"], n["2"], n["i"]), color=YES, buff=0.1, corner_radius=0.15)
        tile_a = SurroundingRectangle(n["add"], color=CTRL, buff=0.1, corner_radius=0.15)
        tile_l = SurroundingRectangle(n["load"], color=FUNC, buff=0.1, corner_radius=0.15)
        out = code(["slli t1, %i, 2", "add  t2, %a, t1", "lw   t3, 0(t2)"], size=18, color=WHITE).next_to(
            pats, DOWN, buff=0.7).align_to(pats, LEFT)
        alt = label(r"and \texttt{p.count}, \ a load of $p + 12$, \ is one tile: \ \texttt{lw t, 12(p)}", font_size=20,
                    color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The back end begins by choosing machine instructions. <bookmark mark='a'/> Think of the IR for a of i "
            "as a small tree: a load, of a plus i shifted left by two. <bookmark mark='b'/> Each Pebble instruction "
            "covers a pattern in such trees, a tile. A shift by a constant. An addition. And a load, which on "
            "Pebble can also add a constant offset to its address for free. <bookmark mark='c'/> Instruction "
            "selection covers the tree with tiles, every node exactly once. Here three tiles: shift, add, load. "
            "<bookmark mark='d'/> Each tile becomes one instruction. <bookmark mark='e'/> A field access like p "
            "dot count, a load of p plus twelve, fits a single tile, because the load's offset absorbs the "
            "addition."
        ) as vo:
            self.play(FadeIn(head), FadeIn(expr))
            vo.wait_until("a")
            self.play(FadeIn(t))
            vo.wait_until("b")
            self.play(FadeIn(pl), LaggedStart(*[FadeIn(p) for p in pats], lag_ratio=0.4), run_time=2)
            vo.wait_until("c")
            self.play(Create(tile_s))
            self.play(Create(tile_a))
            self.play(Create(tile_l))
            vo.wait_until("d")
            self.play(FadeIn(out))
            vo.wait_until("e")
            self.play(FadeIn(alt))
        self.wait(0.3)
        self.clear_scene()

    def munch(self):
        head = label(r"Maximal munch", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"start at the root", font_size=22, color=GREY_A),
            label(r"choose the \textbf{largest} tile that matches there", font_size=22, color=GREY_A),
            label(r"recurse on the subtrees left uncovered at its leaves", font_size=22, color=GREY_A),
            label(r"emit the instructions in reverse: \ operands before the operation", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        ex = VGroup(
            label(r"\texttt{load [\%p + 12]}:", font_size=21, color=CODE),
            label(r"\texttt{lw t, 12(p)} \ beats \ \texttt{addi u, p, 12; \ lw t, 0(u)}", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(steps, DOWN, buff=0.5).align_to(steps, LEFT)
        note = label(r"greedy, \ linear time, \ and what our compiler does", font_size=22, color=HEAD).to_edge(
            DOWN, buff=0.6)
        with self.voiceover("How should the tiles be chosen? The simplest method is called maximal munch. <bookmark mark='a'/> Start at the root of the tree, choose the largest tile that matches there, and recurse on whatever subtrees hang below the tile's leaves. Then emit the instructions in reverse, so that operands are computed before the operations that use them. <bookmark mark='b'/> For a load from p plus twelve, the largest tile is the load with an offset, one instruction, rather than an add followed by a load. <bookmark mark='c'/> It is greedy and takes linear time, and it is what our compiler does.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.5), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(ex))
            vo.wait_until('c')
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def dp(self):
        head = label(r"Optimal tiling, \ by dynamic programming", font_size=34).to_edge(UP, buff=0.3)
        eq = MathTex(r"\mathrm{cost}(v) \;=\; \min_{\text{tile } T \text{ matching at } v} \Big( c(T) + "
                     r"\sum_{u \,\in\, \mathrm{leaves}(T)} \mathrm{cost}(u) \Big)", font_size=36).next_to(
            head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"bottom-up: \ every subtree's best cost, \ once", font_size=22, color=GREY_A),
            label(r"optimal for the given tile costs, \ in linear time for a fixed set of tiles", font_size=22,
                  color=GREY_A),
            label(r"Aho and Johnson, \ 1976; \ generated from a grammar of tiles: \ BURS, \ iburg \ (1992)",
                  font_size=22, color=GREY_A),
            label("greedy matching need not minimize cost for arbitrary tile sets", font_size=21, color=YES),
            label(r"real IRs are DAGs, \ not trees: \ optimal DAG tiling is NP-hard", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(eq, DOWN, buff=0.5)
        with self.voiceover("The largest matching tile need not have the lowest total cost. <bookmark mark='a'/> For a tree and a specified set of legal tiles, dynamic programming records the cheapest way to produce each required result form at a node: the tile's cost plus the best costs of its uncovered subtrees. <bookmark mark='b'/> Compute those states bottom-up. With fixed patterns and bounded matching work, this takes linear time in the tree size. Aho and Johnson developed optimal expression-tree selection, and tools such as iburg generate selectors from rules. <bookmark mark='c'/> Maximal munch uses a simpler greedy choice. Its quality depends on the tiles and costs; it does not establish minimum cost for arbitrary instruction sets. <bookmark mark='d'/> Shared subexpressions turn a tree into a DAG. General optimal DAG covering is NP-hard under the relevant selection models, so practical compilers combine decomposition and heuristics. That hardness claim does not make every restricted DAG case hard.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Write(eq), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts[:3]))
            vo.wait_until('c')
            self.play(FadeIn(pts[3]))
            vo.wait_until('d')
            self.play(FadeIn(pts[4]))
        self.wait(0.3)
        self.clear_scene()

    def fusion(self):
        d = load("isel")
        head = label(r"The function \texttt{same}, \ selected", font_size=34).to_edge(UP, buff=0.3)
        rows = []
        for p in d["pairs"]:
            n = max(len(p["ir"]), len(p["mi"]))
            irs = p["ir"] + [""] * (n - len(p["ir"]))
            mis = [mi_text(m) for m in p["mi"]] + [""] * (n - len(p["mi"]))
            for k in range(n):
                rows.append([p["label"] if k == 0 else "", irs[k], mis[k]])
        tab = grid_table([r"block", r"IR", r"Pebble, \ virtual registers"], rows, widths=[1.6, 4.6, 4.2],
                         row_h=0.3, font_size=15, mono_cols=(0, 1, 2)).next_to(head, DOWN, buff=0.35)
        fuse = [k for k, r in enumerate(rows) if r[0] == "while1"][0]
        hl = SurroundingRectangle(VGroup(*tab.cells[fuse + 1], *tab.cells[fuse + 2]), color=HEAD, buff=0.04)
        notes = VGroup(
            label(r"compare and branch fused: \ \texttt{<} then \texttt{if} \ becomes one \texttt{bge}, \ "
                  r"condition inverted to fall into the loop", font_size=19, color=HEAD),
            label(r"the calling convention appears: \ arguments arrive in \texttt{a0}--\texttt{a2}", font_size=19,
                  color=GREY_A),
            label(r"still on \textit{virtual} registers: \ fitting them into 13 real ones is next", font_size=19,
                  color=FUNC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Here is the whole of same, the letter comparison, on the left as IR and on the right as selected "
            "Pebble instructions. <bookmark mark='a'/> Most IR instructions become one instruction each. But the "
            "loop test is two IR instructions, a comparison producing a truth value and a branch on it, and "
            "Pebble can do both at once: branch if greater or equal. The selector fuses them, and inverts the "
            "condition so that the common case falls through into the loop body. <bookmark mark='b'/> The calling "
            "convention appears too: the three arguments arrive in registers a zero to a two, and are moved into "
            "the function's own names. <bookmark mark='c'/> But the code still uses virtual registers, as many as "
            "it likes. Pebble has thirteen that the compiler may allocate. Fitting the one into the other is the "
            "next chapter, and the deepest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(Create(hl), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()
