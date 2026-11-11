from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.algo import optim as O
from fractions import Fraction
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
        self.near_integer()
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
                txt = f"{t['bound']:.0f}" if t["bound"] is not None else "x"
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
        head = label('Bounds, \\ cuts, \\ and finite search counts', font_size=34).to_edge(UP, buff=0.35)
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
            label('solver progress depends on the benchmark family and protocol; \\ no universal speedup claimed', font_size=21, color=YES),
            label(r"airline crews, \ power grids, \ kidney exchanges, \ chip placement", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.24).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            (
            "How well does branch and bound scale here? <bookmark mark='a'/> On these forty random knapsacks up "
            'to one hundred sixty items, tight fractional upper bounds prune most of the search. Independent '
            'capacity dynamic programming checks every integer optimum; this finite family gives no worst-case '
            "speed guarantee. <bookmark mark='b'/> Gomory cuts add inequalities valid for whole solutions but "
            "violated by a fractional candidate. <bookmark mark='c'/> Branch and cut combines these ideas with "
            "presolving and heuristics. <bookmark mark='d'/> Progress in solvers depends on problem family, "
            'benchmark protocol, algorithms and hardware. We make no single universal speedup claim from this '
            "experiment. <bookmark mark='e'/> The resulting models support crew scheduling, energy systems, "
            'kidney exchanges and placement problems, subject to their own constraints and validation.'
        )
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
        tab = grid_table([r"$\varepsilon$", r"guarantee $1 - \varepsilon$", r"achieved", '$nV$ work model', r"time"], rows,
                         widths=[1.2, 2.8, 1.8, 2.0, 1.6], row_h=0.42, font_size=21, mono_cols=(),
                         colors=[[WHITE, GREY_A, YES, LAM, GREY_A]] * len(rows))
        lines = VGroup(
            label(r"exact knapsack is pseudo-polynomial: \ $O(n \cdot \text{capacity})$ \ (Part 19)", font_size=22,
                  color=WHITE),
            label('teaching value scaling: \\ discard overweight items; \\ $K=\\varepsilon v_{\\max}/n$; \\ round down', font_size=22, color=LAM),
            label('loss $\\le nK\\le\\varepsilon\\,\\mathrm{OPT}$; \\ scaled sum $V=O(n^2/\\varepsilon)$; \\\\ displayed $nV$ counts work, \\ not allocated memory', font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.28).next_to(head, DOWN, buff=0.4)
        tab.next_to(lines, DOWN, buff=0.4).set_x(0)
        foot = label(rf"{d['fptas_n']} correlated items; \ minimum of 3 host trials; \ $nV$ is a work model", font_size=21, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "Knapsack also admits controlled approximation. <bookmark mark='a'/> Capacity dynamic programming is "
            'exact but pseudopolynomial: the numeric capacity may be exponential in its bit length. <bookmark '
            "mark='b'/> Our standard value-scaling teaching scheme first removes overweight items, then rounds "
            'feasible values down in units of epsilon times the largest feasible value divided by the item '
            "count. This is not the faster original Ibarra-Kim implementation. <bookmark mark='c'/> Total "
            'rounding loss is at most epsilon times that largest value, hence at most epsilon times OPT. The '
            "scaled sum is quadratic in n over epsilon; this code's reported n times that sum is a work model, "
            "not allocated table memory. <bookmark mark='d'/> The correlated twenty-item experiment checks each "
            'result against an independent exact optimum. High observed accuracy is welcome, but the promised '
            'guarantee remains one minus epsilon; the repeated host timings are observations, with generation '
            'and validation outside the clock.'
        )
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


    def near_integer(self):
        values, weights, capacity = [100,100], [10**12,1], 10**12-1
        bound, fractional = O.knapsack_lp_bound(values,weights,capacity,{})
        optimum, chosen, _, _ = O.branch_and_bound_knapsack(values,weights,capacity)
        assert fractional == {1:Fraction(1),0:Fraction(1)-Fraction(2,10**12)}
        assert bound == Fraction(200)-Fraction(2,10**10)
        assert optimum == 100 and sum(weights[i]*v for i,v in chosen.items())<=capacity
        head = label('Almost integral is not integral',font_size=34).to_edge(UP,buff=.35)
        items = VGroup(
            label('two items; each value 100',font_size=27,color=WHITE),
            MathTex(r'w=(10^{12},1),\quad C=10^{12}-1',font_size=35,color=DATA),
            MathTex(r'x=(1-2/10^{12},1)',font_size=37,color=LAM),
            MathTex(r'\hbox{LP bound}=200-2/10^{10}',font_size=35,color=LAM),
        ).arrange(DOWN,buff=.5).move_to(LEFT*3.5)
        if items.width>6.4:items.width=6.4;items.set_x(-3.5)
        rows=VGroup(
            label('round both items to one?',font_size=27,color=NO),
            MathTex(r'10^{12}+1=C+2>C',font_size=36,color=NO),
            label('weight exceeds capacity by 2',font_size=23,color=NO),
            MathTex(r'x_0=1:\ \hbox{infeasible};\qquad x_0=0:\ \mathrm{OPT}=100',font_size=30,color=YES),
            label('exact fractions preserve the necessary branch',font_size=23,color=YES),
        ).arrange(DOWN,buff=.4).move_to(RIGHT*3.1)
        if rows.width>6.6:rows.width=6.6;rows.set_x(3.1)
        with self.voiceover("An exact bound matters even when a fraction looks like an integer. Both items are worth one hundred; their weights are a trillion and one, and capacity is a trillion minus one. <bookmark mark='a'/> The relaxation takes the light item and one minus two trillionths of the heavy item. Its value is just below two hundred. <bookmark mark='b'/> Rounding that fraction to one would select both items and exceed capacity by two. A small coordinate error has become an invalid solution. <bookmark mark='c'/> Exact branching rejects the heavy-item branch as infeasible and keeps the light item, proving an integer optimum of one hundred. Closeness to an integer cannot replace feasibility and exact branch logic.") as vo:
            self.play(FadeIn(head),FadeIn(items[0]),FadeIn(items[1]))
            vo.wait_until('a');self.play(FadeIn(items[2]),FadeIn(items[3]))
            vo.wait_until('b');self.play(FadeIn(rows[0]),FadeIn(rows[1]),FadeIn(rows[2]))
            vo.wait_until('c');self.play(FadeIn(rows[3]),FadeIn(rows[4]))
        self.wait(.3);self.clear_scene()
