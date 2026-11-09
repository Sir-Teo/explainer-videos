from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, DEMO_POS_SMALL, FUNC, HEAD, NO, PART, YES, cfg_view, grid_table,
                                   load, mono)

ORDER = ["entry", "while1", "body2", "then5", "else7", "endif6", "endwhile3"]


def dom_sets(idom):
    out = {}
    for b in idom:
        s, x = [b], b
        while idom[x] != x:
            x = idom[x]
            s.append(x)
        out[b] = s
    return out


def small_cfg(at=LEFT * 4.2, colors=None):
    return cfg_view(load("ir")["func"], DEMO_POS_SMALL, size=14, lines=False, colors=colors, at=at + DOWN * 0.2)


class Dominators(VoiceoverScene):
    def construct(self):
        self.card()
        self.define()
        self.iterate()
        self.tree()
        self.frontier()

    def card(self):
        card = chapter_card(4, r"Dominators", r"Which blocks must run before this one?", lit=(1979,),
                            extra=((1979, r"Lengauer--Tarjan dominators"),), part=PART)
        with self.voiceover("Chapter four. Dominators."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def define(self):
        head = label(r"$d$ dominates $n$: \ every path from entry to $n$ passes through $d$", font_size=30).to_edge(
            UP, buff=0.3)
        cfg = small_cfg(at=LEFT * 4.7)
        B = cfg.blocks
        paths = [["entry", "while1", "body2", "then5", "endif6"], ["entry", "while1", "body2", "else7", "endif6"],
                 ["entry", "while1", "body2", "then5", "endif6", "while1", "body2", "else7", "endif6"]]
        right = VGroup(
            label(r"paths from entry to \texttt{endif6}:", font_size=22, color=GREY_A),
            *[mono(" → ".join(p), 13, CODE) for p in paths],
            label(r"every one passes \texttt{entry}, \ \texttt{while1}, \ \texttt{body2}", font_size=22,
                  color=YES),
            label(r"\texttt{then5} \ does not dominate \texttt{endif6}: \ go round by \texttt{else7}", font_size=22,
                  color=NO),
            label(r"a test: \ delete $d$; \ is $n$ still reachable? \ If not, \ $d$ dominates $n$", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        right[1:4].shift(RIGHT * 0.3)
        if right.width > 8.6:
            right.scale_to_fit_width(8.6)
        right.move_to([-1.6, -0.2, 0], aligned_edge=LEFT)
        with self.voiceover(
            "The first thing the middle end computes about the graph is who dominates whom. A block d dominates a "
            "block n if every path from the entry to n passes through d. Whenever n runs, d has already run. "
            "<bookmark mark='a'/> Take endif. <bookmark mark='b'/> Control can reach it through then, or through "
            "else, or around the loop any number of times first. <bookmark mark='c'/> Every one of these paths "
            "passes through entry, the loop test while one, and body two. Those three dominate endif, and so does "
            "endif itself. <bookmark mark='d'/> Then five does not: there is a path round it, by else. <bookmark "
            "mark='e'/> An equivalent test: delete d from the graph. If n can no longer be reached from the entry, "
            "d dominates n. Our test suite checks the compiler's answer against exactly this definition, for every "
            "pair of blocks in the Job."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cfg))
            vo.wait_until("a")
            self.play(B["endif6"].box.animate.set_fill(HEAD, 0.5))
            vo.wait_until("b")
            self.play(FadeIn(right[0]))
            for k, p in enumerate(paths):
                edges = [cfg.edges[(p[j], p[j + 1])] for j in range(len(p) - 1)]
                self.play(FadeIn(right[1 + k]), *[e.animate.set_color(YES) for e in edges], run_time=0.8)
                self.play(*[e.animate.set_color(GREY_B) for e in edges], run_time=0.4)
            vo.wait_until("c")
            self.play(FadeIn(right[4]), *[B[k].box.animate.set_fill(YES, 0.45) for k in ("entry", "while1",
                                                                                         "body2")])
            vo.wait_until("d")
            self.play(FadeIn(right[5]), B["then5"].box.animate.set_stroke(NO, 3))
            vo.wait_until("e")
            self.play(FadeIn(right[6]))
            self.play(B["body2"].animate.set_opacity(0.15))
            self.play(B["body2"].animate.set_opacity(1))
        self.wait(0.3)
        self.clear_scene()

    def iterate(self):
        d = load("dom")
        head = label(r"Computing them: \ a fixed point", font_size=34).to_edge(UP, buff=0.3)
        eq = MathTex(r"\mathrm{Dom}(\text{entry}) = \{\text{entry}\}, \qquad \mathrm{Dom}(n) = \{n\} \;\cup "
                     r"\bigcap_{p \,\in\, \mathrm{pred}(n)} \mathrm{Dom}(p)", font_size=34).next_to(head, DOWN,
                                                                                                buff=0.35)
        cfg = small_cfg(at=LEFT * 4.6 + DOWN * 0.4)
        sets = dom_sets(d["idom"])
        preds = {b: [] for b in ORDER}
        for (a, b) in cfg.edges:
            preds[b].append(a)
        rows = [[b, ", ".join(preds[b]) or "--", "{" + ", ".join(sets[b][::-1]) + "}"] for b in ORDER]
        tab = grid_table(["block", "predecessors", "dominators"], rows, widths=[1.7, 2.4, 3.6], row_h=0.42,
                         font_size=15, mono_cols=(0, 1, 2)).move_to([2.6, -0.6, 0])
        rpo = label("reverse postorder helps; irreducible graphs need additional care",
                    font_size=19, color=GREY_A).next_to(tab, DOWN, buff=0.25)
        note = label(rf"passes until nothing changes: \ {d['passes']} \ (one to settle, \ one to confirm)",
                     font_size=20, color=YES).next_to(rpo, DOWN, buff=0.15)
        job = label(r"every function of the Job: \ " + ", ".join(rf"\texttt{{{r['func']}}} {r['passes']}"
                                                                 for r in d["job"]), font_size=18,
                    color=GREY_B).next_to(note, DOWN, buff=0.12)
        with self.voiceover("Dominance has a useful set equation. <bookmark mark='a'/> The reachable entry is dominated only by itself. For another reachable block n, intersect the dominator sets of its reachable predecessors, then add n. <bookmark mark='b'/> A loop makes those equations circular. Initialize the entry to itself and the other sets to all reachable blocks, then repeatedly intersect until no set changes. This is a descending finite iteration. <bookmark mark='c'/> Reverse postorder is a useful visiting order. In reducible graphs it respects the forward structure apart from loop back edges; an arbitrary irreducible graph needs more care. The displayed example stabilizes quickly. <bookmark mark='d'/> Our implementation uses the related Cooper, Harvey and Kennedy method: intersect immediate-dominator tree paths, rather than explicitly storing every dominator set. Its measured rounds are observations about these graphs. They are not a size-independent bound for every program. Lengauer and Tarjan provide a different, nearly linear theoretical approach. <bookmark mark='e'/> The recurring pattern is an equation solved by iteration to a fixed point.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Write(eq), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(cfg), FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]])
            for r in tab.cells[1:]:
                self.play(*[FadeIn(c) for c in r[:2]], run_time=0.3)
            vo.wait_until('c')
            self.play(FadeIn(rpo))
            for k, r in enumerate(tab.cells[1:]):
                self.play(FadeIn(r[2]), Indicate(cfg.blocks[ORDER[k]].box, color=HEAD), run_time=0.6)
            vo.wait_until('d')
            self.play(FadeIn(note), FadeIn(job))
        self.wait(0.4)
        self.clear_scene()

    def tree(self):
        d = load("dom")
        head = label(r"The dominator tree", font_size=34).to_edge(UP, buff=0.3)
        cfg = small_cfg(at=LEFT * 4.4)
        kids = d["tree"]
        pos = {"entry": (2.6, 2.3), "while1": (2.6, 1.1), "endwhile3": (4.4, 0.0), "body2": (1.2, 0.0),
               "then5": (-0.2, -1.2), "else7": (1.2, -1.2), "endif6": (2.6, -1.2)}
        nodes = {}
        for b, (x, y) in pos.items():
            t = mono(b, 15, WHITE)
            r = RoundedRectangle(width=t.width + 0.35, height=t.height + 0.3, corner_radius=0.08, stroke_color=YES,
                                 stroke_width=1.8, fill_color=YES, fill_opacity=0.15).move_to([x, y, 0])
            nodes[b] = VGroup(r, t.move_to(r))
        lines = VGroup(*[Line(nodes[a][0].get_bottom(), nodes[c][0].get_top(), color=YES, stroke_width=2)
                         for a, cs in kids.items() for c in cs])
        cap = VGroup(
            label("reachable non-entry block: parent is its nearest strict dominator", font_size=21,
                  color=GREY_A),
            label(r"\texttt{endif6} hangs from \texttt{body2}: \ neither branch dominates it", font_size=21,
                  color=GREY_A),
            label(r"$d$ dominates $n$ \ $\iff$ \ $d$ is an ancestor of $n$ in the tree", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.35).shift(RIGHT * 1.3)
        with self.voiceover(
            (
            "For a block reachable from entry, its dominators form a chain under domination. <bookmark mark='a'/> "
            "Every reachable block except entry therefore has a closest strict dominator, its immediate "
            "dominator. Drawing an edge from that parent to the block gives the dominator tree, rooted at entry. "
            "<bookmark mark='b'/> Notice where endif hangs: from body two, rather than then or else, because "
            "neither branch dominates the join. <bookmark mark='c'/> Now d dominates n exactly when d is n or an "
            "ancestor of n in this tree. A table of dominator sets has become one parent pointer per non-root "
            "block. The compiler uses this structure to place phis and to track which definitions are available "
            "along every incoming path."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(cfg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(nodes[b]) for b in ORDER], lag_ratio=0.2), Create(lines), run_time=2.5)
            self.play(FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(Indicate(nodes["endif6"], color=HEAD), FadeIn(cap[1]))
            vo.wait_until("c")
            self.play(FadeIn(cap[2]))
        self.wait(0.3)
        self.clear_scene()

    def frontier(self):
        d = load("dom")
        head = label(r"Where dominance ends: \ the dominance frontier", font_size=34).to_edge(UP, buff=0.3)
        cfg = small_cfg(at=LEFT * 4.2)
        B = cfg.blocks
        defn = VGroup(
            label(r"$\mathrm{DF}(d)$: \ the blocks $n$ where $d$ dominates a predecessor of $n$,", font_size=22,
                  color=GREY_A),
            label(r"but does not strictly dominate $n$ itself", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([2.6, 2.0, 0])
        rows = [[b, "{" + ", ".join(d["frontiers"][b]) + "}"] for b in ORDER]
        tab = grid_table(["block d", "DF(d)"], rows, widths=[2.0, 2.4], row_h=0.4, font_size=15,
                         mono_cols=(0, 1)).move_to([2.6, -0.5, 0])
        why = label(r"the first place where another path joins: \ a value from $d$ meets a value from elsewhere",
                    font_size=20, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            "One more idea, and it is the one SSA needs. <bookmark mark='a'/> The dominance frontier of d "
            "contains blocks n where d dominates a predecessor of n, but does not strictly dominate n. Strictly "
            "matters: a block dominates itself, yet a loop header can belong to its own frontier. <bookmark "
            "mark='b'/> Then five's frontier is endif. Then five dominates itself, a predecessor of endif, but a "
            "path through else reaches endif without visiting then. <bookmark mark='c'/> Body two's frontier "
            "contains the loop test, while one, reached around the back edge. While one is also in its own "
            "frontier: it dominates the back-edge predecessor, without strictly dominating itself. <bookmark "
            "mark='d'/> These are join points where definitions from different incoming paths may meet. Taking "
            "the frontier again for newly inserted definitions tells SSA where further phi functions may be "
            "needed."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(cfg))
            vo.wait_until("a")
            self.play(FadeIn(defn))
            self.play(FadeIn(tab.rule), *[FadeIn(c) for r in tab.cells for c in r])
            vo.wait_until("b")
            self.play(B["then5"].box.animate.set_fill(YES, 0.5), B["endif6"].box.animate.set_stroke(HEAD, 4),
                      Indicate(tab.cells[ORDER.index("then5") + 1][1], color=HEAD))
            vo.wait_until("c")
            self.play(B["then5"].box.animate.set_fill(DATA, 0.15), B["endif6"].box.animate.set_stroke(DATA, 1.8))
            self.play(*[B[k].box.animate.set_fill(YES, 0.5) for k in ("body2", "then5", "else7", "endif6")],
                      B["while1"].box.animate.set_stroke(HEAD, 4),
                      Indicate(tab.cells[ORDER.index("body2") + 1][1], color=HEAD))
            self.play(Indicate(tab.cells[ORDER.index("while1") + 1][1], color=HEAD))
            vo.wait_until("d")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()
