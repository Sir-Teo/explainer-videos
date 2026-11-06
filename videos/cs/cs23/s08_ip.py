from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


def tree_layout(tree):
    """Nodes keyed by their tuple of (item, value) decisions; parent = drop the last decision."""
    nodes = {}
    for t in tree:
        key = tuple((int(k), v) for k, v in t["fixed"].items())
        nodes[key] = t
    keys = set(nodes)
    for k in list(keys):
        while k:
            k = k[:-1]
            keys.add(k)
    children = {k: [] for k in keys}
    for k in keys:
        if k:
            children[k[:-1]].append(k)
    for k in children:
        children[k].sort(key=lambda c: -c[-1][1])          # "take it" (1) on the left
    pos, counter = {}, [0]

    def walk(k, depth):
        ch = children[k]
        if not ch:
            pos[k] = (counter[0], depth)
            counter[0] += 1
            return
        for c in ch:
            walk(c, depth + 1)
        pos[k] = (sum(pos[c][0] for c in ch) / len(ch), depth)
    walk((), 0)
    return nodes, children, pos


class IntegerPrograms(VoiceoverScene):
    def construct(self):
        self.card()
        self.bnb()
        self.scale()
        self.fptas()

    def card(self):
        card = chapter_card(7, r"Integer programming", r"What changes when the answer must be whole?", lit=(1958, 1960),
                            extra=((1958, r"Gomory cuts"), (1960, r"Land--Doig branch and bound")), part=PART)
        with self.voiceover("Chapter seven. Integer programming."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def bnb(self):
        d = load("ip")
        head = label(r"Branch and bound on a knapsack", font_size=34).to_edge(UP, buff=0.3)
        items = VGroup(*[mono(f"{i}: {v}/{w}", 15, GREY_A) for i, (v, w) in enumerate(zip(d["vals"], d["wts"]))])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        icap = label(rf"item: \ value/weight; \\ capacity {d['cap']}", font_size=17, color=GREY_B)
        ig = VGroup(icap, items).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.4).shift(DOWN * 0.8)
        nodes, children, pos = tree_layout(d["tree"])
        xs = [p[0] for p in pos.values()]
        depth = max(p[1] for p in pos.values())
        W, H = 9.0, 3.9
        sx = W / max(1, max(xs) - min(xs))
        sy = H / max(1, depth)

        def P(k):
            x, y = pos[k]
            return np.array([-2.4 + (x - min(xs)) * sx - W / 2 + 2.6, 2.4 - y * sy, 0])
        fate_col = {"branch": DATA, "pruned": NO, "integral": YES}
        dots, edges, labs = VGroup(), VGroup(), VGroup()
        order = sorted(pos, key=lambda k: (len(k), pos[k][0]))
        for k in order:
            t = nodes.get(k)
            col = fate_col[t["fate"]] if t else GREY_D
            dots.add(Dot(P(k), radius=0.08, color=col))
            if t:
                txt = f"{t['bound']:.0f}" if math.isfinite(t["bound"]) else "x"
                labs.add(mono(txt, 14, col).next_to(P(k), UP, buff=0.05))
            if k:
                edges.add(Line(P(k[:-1]), P(k), color=GREY_D, stroke_width=1.4))
        side = VGroup(
            label(r"relax: \ allow fractions; \ the LP bound is greedy by value per weight", font_size=20,
                  color=WHITE),
            label(rf"root bound {d['root']:.1f}; \ branch on the fractional item: \\ take it, \ or leave it",
                  font_size=20, color=DATA),
            label(r"prune any node whose bound can't beat the best whole answer so far", font_size=20, color=NO),
            label(rf"best: \ {d['best']}, \ after {d['nodes']} nodes \ (of $2^8 = 256$ choices)", font_size=20,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.3).shift(RIGHT * 1.6)
        if side.width > 9.6:
            side.width = 9.6
        with self.voiceover(
            "Insist that the answer be made of whole things, and linear programming becomes NP-hard. The standard "
            "attack keeps linear programming as a guide. <bookmark mark='a'/> Here is a knapsack: eight items with "
            "values and weights, and a capacity of eighty. Relax it: let items be taken fractionally. That linear "
            "program is easy, greedy by value per unit of weight, and its optimum bounds what any whole choice can "
            "reach. <bookmark mark='b'/> The root's bound is a hundred and eighty-four, with one item taken in part. "
            "Branch on that item: one subproblem takes it, the other leaves it out, and each has its own bound. "
            "<bookmark mark='c'/> Any node whose bound cannot beat the best whole answer found so far is pruned "
            "without being explored. <bookmark mark='d'/> Here the best answer, a hundred and seventy-four, is found "
            "and proved optimal after twenty-four nodes, instead of the two hundred and fifty-six possible choices. "
            "Ailsa Land and Alison Doig invented the method in 1960, at the London School of Economics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ig))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(dots[0]), FadeIn(labs[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), LaggedStart(*[Create(e) for e in edges], lag_ratio=0.05),
                      LaggedStart(*[FadeIn(x) for x in dots[1:]], lag_ratio=0.05),
                      LaggedStart(*[FadeIn(x) for x in labs[1:]], lag_ratio=0.05), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def scale(self):
        d = load("ip")
        head = label(r"Bounds, \ cuts, \ and decades of speedups", font_size=34).to_edge(UP, buff=0.35)
        rows = [[str(r["n"]), f"{r['nodes_mean']:.0f}", str(r["nodes_max"]), rf"$2^{{{r['n']}}}$",
                 f"{100 * r['gap']:.2f}\\%"] for r in d["rows"]]
        tab = grid_table([r"items", r"mean nodes", r"worst", r"choices", r"LP gap"], rows,
                         widths=[1.4, 2.0, 1.4, 1.6, 1.8], row_h=0.44, font_size=21, mono_cols=(),
                         colors=[[WHITE, YES, GREY_A, NO, LAM]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label(r"random knapsacks, \ 10 of each size: \ the LP bound is within a few percent, \ so most of the tree "
                  r"is pruned", font_size=21, color=WHITE),
            label(r"\textbf{Gomory cuts} \ (1958): \ add a valid inequality that slices off the fractional vertex, "
                  r"\ and re-solve", font_size=21, color=HEAD),
            label(r"branch and \textbf{cut}: \ both, \ plus presolve and heuristics: \ CPLEX, \ Gurobi, \ SCIP, \ "
                  r"HiGHS", font_size=21, color=LAM),
            label(r"Bixby: \ from 1991 to 2007 the algorithms alone sped up about 30,000-fold, \ on top of the "
                  r"hardware", font_size=21, color=YES),
            label(r"airline crews, \ power grids, \ kidney exchanges, \ chip placement", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.24).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "How well does it scale? <bookmark mark='a'/> On random knapsacks of up to a hundred and sixty items, "
            "where there are two to the hundred and sixty choices, branch and bound needed a few hundred nodes on "
            "average, because the linear bound was within a percent or two of the truth. Bad instances exist, but "
            "the bound does most of the work. <bookmark mark='b'/> Ralph Gomory showed in 1958 how to cut instead of "
            "branch: derive a new inequality that every whole solution satisfies but the fractional optimum violates, "
            "add it, and solve again. <bookmark mark='c'/> Modern solvers do both, branch and cut, with layers of "
            "presolving and heuristics. <bookmark mark='d'/> Robert Bixby measured their progress: between 1991 and "
            "2007 the algorithms alone became about thirty thousand times faster, on top of the hardware. <bookmark "
            "mark='e'/> They schedule airline crews, run power grids, match kidney donors and place components on "
            "chips."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
            for mk, n_ in zip("abcde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def fptas(self):
        d = load("ip")
        head = label(r"Knapsack, \ approximately, \ fast", font_size=34).to_edge(UP, buff=0.35)
        rows = [[f"{r['eps']:g}", f"{1 - r['eps']:.2f}", f"{r['ratio']:.4f}", words(r["table"]),
                 f"{r['seconds'] * 1000:.1f} ms"] for r in d["fptas"]]
        tab = grid_table([r"$\varepsilon$", r"guarantee $1 - \varepsilon$", r"achieved", r"table size", r"time"], rows,
                         widths=[1.2, 2.8, 1.8, 2.0, 1.6], row_h=0.42, font_size=21, mono_cols=(),
                         colors=[[WHITE, GREY_A, YES, LAM, GREY_A]] * len(rows))
        lines = VGroup(
            label(r"exact knapsack is pseudo-polynomial: \ $O(n \cdot \text{capacity})$ \ (Part 19)", font_size=22,
                  color=WHITE),
            label(r"Ibarra and Kim (1975): \ round every value down to a multiple of $K = \varepsilon v_{\max} / n$; \ "
                  r"solve the rounded problem exactly", font_size=22, color=LAM),
            label(r"rounding loses at most $K$ per item, \ $nK = \varepsilon v_{\max} \le \varepsilon\,\mathrm{OPT}$; \ "
                  r"the table has $O(n^2/\varepsilon)$ values", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.28).next_to(head, DOWN, buff=0.4)
        tab.next_to(lines, DOWN, buff=0.4).set_x(0)
        foot = label(rf"a strongly correlated instance, \ {d['fptas_n']} items: \ the guarantee is pessimistic; \ the "
                     r"cost grows only like $1/\varepsilon$", font_size=21, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Knapsack also shows a different kind of compromise. <bookmark mark='a'/> Part 19 solved it exactly by "
            "dynamic programming, in time proportional to the capacity, which can be astronomically large. "
            "<bookmark mark='b'/> Oscar Ibarra and Chul Kim rounded every value down to a multiple of epsilon times "
            "the largest value, divided by n, and solved the rounded problem exactly, by dynamic programming over "
            "values. <bookmark mark='c'/> Each item loses less than one rounding unit, so the whole answer loses at "
            "most epsilon times the best value, and the table has n squared over epsilon entries. Any accuracy you "
            "like, in time polynomial in n and one over epsilon: a fully polynomial-time approximation scheme. "
            "<bookmark mark='d'/> On a hard, strongly correlated instance, even epsilon of nine tenths, which "
            "promises only a tenth of the optimum, found ninety-nine point three percent; from a tenth down, it found "
            "the exact optimum, and the work grew only in proportion to one over epsilon."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
