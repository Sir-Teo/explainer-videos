from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy2.common import *  # noqa: F403

FN = "abcde"


def lt(l):
    return (r"\lnot " if l < 0 else "") + FN[abs(l) - 1]


def say(l):
    return ("not " if l < 0 else "") + FN[abs(l) - 1]


def names_list(ls):
    w = [say(l) for l in ls]
    return w[0] if len(w) == 1 else ", ".join(w[:-1]) + " and " + w[-1]


def describe(nodes) -> str:
    out = []
    for nd in nodes:
        if nd["decision"] is None:
            if nd["forced"]:
                out.append(f"First, propagation alone forces {names_list(nd['forced'])}.")
            continue
        l = nd["decision"]
        t = f"try {FN[abs(l) - 1]} as {'true' if l > 0 else 'false'}"
        if nd["forced"]:
            t += f", which forces {names_list(nd['forced'])}"
        if nd["end"] == "conflict":
            t += ", and a clause fails: back up."
        elif nd["end"] == "sat":
            t += ", and every clause holds."
        else:
            t += "."
        out.append(t[0].upper() + t[1:])
    return " ".join(out)


class DPLL(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Searching for a model", r"Can we find a satisfying valuation without trying "
                            r"them all?", lit=(1960,), part=PART)
        with self.voiceover("Chapter ten. Searching for a model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.idea()
        self.run()
        self.transition()

    def idea(self):
        hc = history_card(1962, r"Davis, Logemann \& Loveland", r"build one valuation step by step; back up on "
                          r"failure", width=5.6, color=HIST).to_corner(UL, buff=0.4)
        moves = VGroup(
            definition_card(r"Propagate", r"a clause with every literal false but one forces that one", width=6.0,
                            font_size=24, color=P.WORLD, kind=r"Move 1"),
            definition_card(r"Branch", r"nothing forced? \ pick an open atom; try true; if that fails, try false",
                            width=6.0, font_size=24, color=CONN, kind=r"Move 2"),
            definition_card(r"Back up", r"a clause with every literal false: undo the last choice", width=6.0,
                            font_size=24, color=BAD, kind=r"Move 3"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        ex = VGroup(MathTex(r"(\lnot a \lor c)", font_size=40),
                    MathTex(r"a = \mathrm{T}", font_size=34, color=ATOM),
                    MathTex(r"\Rightarrow\ c = \mathrm{T}", font_size=40, color=P.WORLD)).arrange(DOWN, buff=0.25)
        ex.next_to(hc, DOWN, buff=0.7).set_x(hc.get_x())
        with self.voiceover(
            "A truth table tries every valuation. A smarter search builds a single valuation one step at a time, and "
            "backs up when it gets into trouble. <bookmark mark='a'/>This is the method of Martin Davis, George "
            "Logemann and Donald Loveland, from 1962, now called DPLL. It has three moves. <bookmark mark='b'/>"
            "Propagate: if every literal of a clause is false but one, that one is forced. If a is true, the clause "
            "not a or c forces c. <bookmark mark='c'/>Branch: when nothing is forced, pick an open atom and try true. "
            "<bookmark mark='d'/>Back up: if some clause has every literal false, undo the last choice and try the "
            "other value."
        ) as vo:
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(moves[0]), FadeIn(ex))
            vo.wait_until("c")
            self.play(FadeIn(moves[1]))
            vo.wait_until("d")
            self.play(FadeIn(moves[2]))
        self.clear_scene()

    def run(self):
        d = load("dpll")
        nodes = d["nodes"]
        clauses = d["clauses"]
        fm = VGroup(*[MathTex(clause_tex(frozenset(c), list(FN)), font_size=30) for c in clauses]).arrange(
            RIGHT, buff=0.3)
        if fm.width > 13.2:
            fm.width = 13.2
        fm.to_edge(UP, buff=0.35)

        def tree_of(k):
            return {"children": [tree_of(c) for c in nodes[k]["children"]]}

        tree = SearchTree(tree_of(0), width=7.0, level_height=1.4, radius=0.14, center=[-1.4, -0.6, 0])
        order, q = [], [0]
        while q:
            k = q.pop(0)
            order.append(k)
            q.extend(nodes[k]["children"])
        idx = {k: i for i, k in enumerate(order)}
        labels, ends = {}, {}
        for k, nd in enumerate(nodes):
            i = idx[k]
            parts = []
            if nd["decision"] is not None:
                parts.append(lt(nd["decision"]))
            if nd["forced"]:
                parts.append(r"\Rightarrow " + ",".join(lt(l) for l in nd["forced"]))
            if parts:
                labels[k] = MathTex(r"\ ".join(parts), font_size=26, color=P.WORLD).next_to(tree.nodes[i], RIGHT,
                                                                                            buff=0.12)
            if nd["end"] in ("conflict", "sat"):
                ends[k] = MathTex(r"\times" if nd["end"] == "conflict" else r"\checkmark", font_size=36,
                                  color=BAD if nd["end"] == "conflict" else OK).next_to(tree.nodes[i], DOWN, buff=0.1)
        story = describe(nodes)
        model = d["model"]
        st = d["stats"]
        mod = MathTex(r",\ ".join(rf"{k}={'T' if v else 'F'}" for k, v in model.items()), font_size=32, color=OK)
        ml = VGroup(label(r"a model:", font_size=24, color=GREY_A), mod).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        ml.to_corner(UR, buff=0.4).shift(DOWN * 1.2)
        cnt = label(rf"{len(nodes)} nodes, \ not {2 ** 5} rows", font_size=28, color=GOAL).next_to(ml, UP, buff=0.4)
        cnt.align_to(ml, LEFT)
        tag = note(r"computed: the Reasoner's DPLL, recorded").to_corner(DL, buff=0.25)
        with self.voiceover(
            f"Here it is on a formula of {len(clauses)} clauses in five atoms, the Reasoner's own run, recorded. "
            "<bookmark mark='a'/>" + story
        ) as vo:
            self.play(FadeIn(fm), FadeIn(tag), FadeIn(tree.nodes[0]))
            vo.wait_until("a")
            for k in range(len(nodes)):
                i = idx[k]
                anims = [Create(tree.edges[i]), FadeIn(tree.nodes[i])] if i > 0 else []
                anims += [FadeIn(labels[k])] if k in labels else []
                anims += [FadeIn(ends[k], scale=1.4)] if k in ends else []
                if anims:
                    self.play(*anims, run_time=1.0)
                    self.wait(0.6)
        with self.voiceover(
            f"The search visited {len(nodes)} nodes, where the table would have filled {2 ** 5} rows. "
            "<bookmark mark='a'/>On real problems the difference is astronomical, because one forced value forces "
            "another, in long chains, and a single conflict prunes a whole subtree at once. <bookmark mark='b'/>It is "
            "also how a careful person reasons from a hypothesis: suppose, follow the consequences, and when they "
            "clash, withdraw the supposition. DPLL is reductio ad absurdum, done systematically."
        ) as vo:
            self.play(FadeIn(ml), FadeIn(cnt))
            vo.wait_until("a")
            self.play(Indicate(VGroup(*labels.values()), color=P.WORLD))
            vo.wait_until("b")
        self.clear_scene()

    def transition(self):
        t = load("transition")
        cols = {"20": GREY_B, "30": P.CLAIM, "40": P.CONCL}
        G1 = axes([2, 7], [0, 1], x_length=5.6, y_length=3.0, xticks=[2, 3, 4, 5, 6, 7], yticks=[0, 0.5, 1],
                  ylabel=r"chance a random formula is satisfiable", center=[-3.3, -0.4, 0])
        G2 = axes([2, 7], [0, 3.5], x_length=5.6, y_length=3.0, xticks=[2, 3, 4, 5, 6, 7], yticks=[0, 1, 2, 3],
                  yfmt=lambda v: f"10^{{{int(v)}}}", ylabel=r"DPLL decisions (median)", center=[3.3, -0.4, 0])
        xl = label(r"clauses per atom", font_size=22, color=GREY_A)
        xl1, xl2 = xl.copy().next_to(G1, DOWN, buff=0.1), xl.copy().next_to(G2, DOWN, buff=0.1)
        curves1, curves2 = VGroup(), VGroup()
        for n, rows in t["by_n"].items():
            rs = [r["ratio"] for r in rows]
            curves1.add(curve(G1.ax, rs, [r["p_sat"] for r in rows], cols[n], stroke_width=4, smooth=True))
            curves2.add(curve(G2.ax, rs, [np.log10(max(r["median_decisions"], 1)) for r in rows], cols[n],
                              stroke_width=4, smooth=True))
        th = 4.27
        v1 = DashedLine(G1.ax.c2p(th, 0), G1.ax.c2p(th, 1), color=BAD, stroke_width=2)
        v2 = DashedLine(G2.ax.c2p(th, 0), G2.ax.c2p(th, 3.5), color=BAD, stroke_width=2)
        thl = label(r"$\approx 4.27$", font_size=24, color=BAD).next_to(G1.ax.c2p(th, 0.85), RIGHT, buff=0.1)
        leg = legend([(cols[n], rf"{n} atoms") for n in t["by_n"]], font_size=22).to_corner(UR, buff=0.35)
        peak = {n: max(rows, key=lambda r: r["median_decisions"])["ratio"] for n, rows in t["by_n"].items()}
        head = label(r"random 3-SAT: \ " + rf"{t['seeds']} formulas at each point", font_size=26, color=GREY_A)
        head.to_edge(UP, buff=0.4)
        cites = note(r"Cheeseman, Kanefsky \& Taylor 1991; Mitchell, Selman \& Levesque 1992; Friedgut 1999; "
                     r"Ding, Sly \& Sun 2015", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "How hard is a random formula? <bookmark mark='a'/>Generate clauses of three random literals over n atoms, "
            "and turn one dial: the number of clauses per atom. With few clauses, almost every formula is "
            "satisfiable, and DPLL finds a model at once. With many, almost every formula is contradictory, and the "
            "conflicts come quickly. <bookmark mark='b'/>In between, near 4.27 clauses per atom, the chance of "
            "satisfiability falls from nearly one to nearly zero, more steeply as n grows. <bookmark mark='c'/>And "
            f"near it, DPLL's work peaks: for 40 atoms, at {peak['40']} clauses per atom; for small formulas the peak "
            "sits a little to the right of the threshold. The hardest formulas "
            "live on the knife edge between satisfiable and unsatisfiable, a phase transition, like water freezing. "
            "<bookmark mark='d'/>Ehud Friedgut proved in 1999 that the drop is sharp; exactly where it falls has been "
            "proved only for long clauses, by Jian Ding, Allan Sly and Nike Sun in 2015."
        ) as vo:
            self.play(FadeIn(head), FadeIn(G1), FadeIn(xl1), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(curves1[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(curves1[1]), Create(curves1[2]), Create(v1), FadeIn(thl), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(G2), FadeIn(xl2), Create(curves2), Create(v2), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(cites))
        self.clear_scene()
