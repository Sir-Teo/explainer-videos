from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, mono, tag_box,
                                   trace)


def eq_fn(v: dict) -> bool:
    """x1 = y1 and x2 = y2: the function whose diagrams are drawn."""
    return v["x1"] == v["y1"] and v["x2"] == v["y2"]


def robdd(order):
    """The reduced ordered BDD of eq_fn under ``order``: nodes {id: (level, low, high)}, root id; 0 and 1 are the
    terminals.  Built by Shannon expansion with a unique table, as in Part 3."""
    nodes, unique = {}, {}

    def build(level, env):
        if level == len(order):
            return 1 if eq_fn(env) else 0
        lo = build(level + 1, {**env, order[level]: False})
        hi = build(level + 1, {**env, order[level]: True})
        if lo == hi:
            return lo
        key = (level, lo, hi)
        if key not in unique:
            unique[key] = len(nodes) + 2
            nodes[unique[key]] = key
        return unique[key]
    root = build(0, {})
    return nodes, root


def var_tex(name: str) -> str:
    return f"{name[0]}_{name[1]}"


def draw_bdd(order, x0, x1, ytop, dy, r=0.2, font=20):
    """Lay out and draw a ROBDD: levels top to bottom, each level's nodes ordered by their parents' positions."""
    nodes, root = robdd(order)
    levels = {}
    for u, (lev, _, _) in nodes.items():
        levels.setdefault(lev, []).append(u)
    pos = {}
    parents = {}
    for u, (_, lo, hi) in nodes.items():
        parents.setdefault(lo, []).append(u)
        parents.setdefault(hi, []).append(u)
    for lev in range(len(order)):
        us = levels.get(lev, [])
        us.sort(key=lambda u: (np.mean([pos[p][0] + (0.01 if nodes[p][2] == u else -0.01)
                                        for p in parents.get(u, [])]) if u != root else 0))
        for q, u in enumerate(us):
            pos[u] = [x0 + (x1 - x0) * (q + 0.5) / len(us), ytop - lev * dy, 0]
    yb = ytop - len(order) * dy
    pos[0] = [x0 + (x1 - x0) * 0.3, yb, 0]
    pos[1] = [x0 + (x1 - x0) * 0.7, yb, 0]
    g = VGroup()
    edges = VGroup()
    for u, (_, lo, hi) in nodes.items():
        edges.add(DashedLine(pos[u], pos[lo], buff=r, color=GREY_C, stroke_width=1.6, dash_length=0.07))
        edges.add(Line(pos[u], pos[hi], buff=r, color=GREY_A, stroke_width=1.8))
    circles = VGroup()
    for u, (lev, _, _) in nodes.items():
        c = Circle(radius=r, color=DATA if order[lev][0] == "x" else LAM, stroke_width=2, fill_color=BG,
                   fill_opacity=1).move_to(pos[u])
        circles.add(VGroup(c, MathTex(var_tex(order[lev]), font_size=font).move_to(c)))
    terms = VGroup(*[VGroup(Square(side_length=2 * r, color=NO if t == 0 else YES, stroke_width=2, fill_color=BG,
                                   fill_opacity=1), MathTex(str(t), font_size=font)).move_to(pos[t]) for t in (0, 1)])
    g.add(edges, circles, terms)
    g.n = len(nodes)
    return g


def full_tree(order, x0, x1, ytop, dy, r=0.17, font=18):
    """The complete decision tree of eq_fn: 2^n - 1 tests and 2^n leaves."""
    n = len(order)
    g, edges, circles, leaves = VGroup(), VGroup(), VGroup(), VGroup()
    nl = 2 ** n

    def x_of(level, idx):
        span = (x1 - x0) / 2 ** level
        return x0 + span * (idx + 0.5)
    for lev in range(n):
        for idx in range(2 ** lev):
            p = [x_of(lev, idx), ytop - lev * dy, 0]
            for b in (0, 1):
                q = [x_of(lev + 1, 2 * idx + b), ytop - (lev + 1) * dy, 0]
                edges.add((DashedLine if b == 0 else Line)(p, q, buff=r, color=GREY_C if b == 0 else GREY_A,
                                                            stroke_width=1.4))
            c = Circle(radius=r, color=DATA if order[lev][0] == "x" else LAM, stroke_width=1.8, fill_color=BG,
                       fill_opacity=1).move_to(p)
            circles.add(VGroup(c, MathTex(var_tex(order[lev]), font_size=font).move_to(c)))
    for idx in range(nl):
        env = {order[k]: bool(idx >> (n - 1 - k) & 1) for k in range(n)}
        v = int(eq_fn(env))
        leaves.add(VGroup(Square(side_length=0.26, color=YES if v else NO, stroke_width=1.6, fill_color=BG,
                                 fill_opacity=1), MathTex(str(v), font_size=16)).move_to(
            [x_of(n, idx), ytop - n * dy, 0]))
    g.add(edges, circles, leaves)
    g.n = 2 ** n - 1
    return g


class Symbolic(VoiceoverScene):
    def construct(self):
        self.card()
        self.encode()
        self.diagrams()
        self.order()
        self.image()
        self.scaling()
        self.bmc()

    def card(self):
        card = chapter_card(7, r"Symbolic and bounded model checking", r"Can we check states we never list?",
                            lit=(1986, 1990, 1999),
                            extra=((1986, r"Bryant: \ BDDs"),
                                   (1990, r"Burch, \ Clarke, \ McMillan et al."),
                                   (1999, r"Biere et al.: \ bounded model checking")), part=PART)
        with self.voiceover("Chapter seven. Symbolic and bounded model checking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def encode(self):
        head = label(r"Sets of states as Boolean functions", font_size=36).to_edge(UP, buff=0.3)
        enc = grid_table([r"philosopher $i$", r"$h_i$", r"$e_i$"],
                         [[r"thinking", "0", "0"], [r"holds first fork", "1", "0"], [r"eating", "1", "1"]],
                         widths=[2.8, 0.8, 0.8], row_h=0.42, font_size=20, mono_cols=(1, 2))
        enc.move_to([-4.0, 1.75, 0])
        st = VGroup(*[VGroup(tag_box(b, color=DATA if k % 2 == 0 else LAM, size=20, w=0.45))
                      for k, b in enumerate("101100")]).arrange(RIGHT, buff=0.06)
        names = VGroup(*[MathTex(n, font_size=24, color=GREY_B) for n in
                         ("h_0", "e_0", "h_1", "e_1", "h_2", "e_2")])
        for nm, b in zip(names, st):
            nm.next_to(b, UP, buff=0.1)
        stg = VGroup(names, st).move_to([2.6, 2.0, 0])
        stl = label(r"one state of three philosophers: \ six bits", font_size=18, color=GREY_A).next_to(
            stg, DOWN, buff=0.15)
        chi = label(r"a set of states $S$ \ $\longleftrightarrow$ \ a formula $\chi_S$, \ true exactly on its "
                    r"members", font_size=20, color=HEAD).next_to(stl, DOWN, buff=0.3)
        steps = [
            MathTex(r"T_{\mathit{take1}_0}", r"=", r"\neg h_0 \wedge \neg e_2", font_size=32),
            MathTex(r"T_{\mathit{take1}_0}", r"=", r"\neg h_0 \wedge \neg e_2", r"\wedge h_0'", font_size=32),
            MathTex(r"T_{\mathit{take1}_0}", r"=", r"\neg h_0 \wedge \neg e_2", r"\wedge h_0'",
                    r"\wedge (e_0' \leftrightarrow e_0) \wedge \bigwedge_{i \ne 0} \big[(h_i' \leftrightarrow h_i) "
                    r"\wedge (e_i' \leftrightarrow e_i)\big]", font_size=32),
        ]
        for m in steps:
            if m.width > 12.6:
                m.width = 12.6
            m.move_to([0, -0.45, 0]).to_edge(LEFT, buff=0.5)
        whys = [label(r"the guard: \ not holding fork 0 already, \ and philosopher 2, \ who shares it, \ not eating",
                      font_size=18, color=GREY_A),
                label(r"the effect, \ on the primed \ (next-state) \ copy of the bits", font_size=18, color=GREY_A),
                label(r"the frame: \ every other bit unchanged", font_size=18, color=GREY_A)]
        for w in whys:
            w.next_to(steps[0], DOWN, buff=0.15).to_edge(LEFT, buff=0.5)
        total = MathTex(r"T(x, x')", r"=", r"\bigvee_a T_a(x, x')", font_size=36, color=YES).move_to([-2.6, -2.0, 0])
        tot_l = label(r"one relation for the whole system: \ every command's move, \ as a formula", font_size=18,
                      color=YES).next_to(total, RIGHT, buff=0.4)
        foot = wrapped_label(r"Part 3's Boolean functions, \ now describing sets of states and the moves between "
                             r"them; \ a formula can be small even when the set it describes is huge", 12.4,
                             font_size=19, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Explicit checking lists states one at a time; symbolic checking describes whole sets with formulas. "
            "<bookmark mark='a'/> Give each philosopher two bits: holding its first fork, and eating. <bookmark "
            "mark='b'/> A state of three philosophers is six bits, and a set of states is a Boolean function, true "
            "exactly on its members. <bookmark mark='c'/> Moves become formulas over the current bits and a primed "
            "copy for the next. Philosopher zero may take fork zero if it is not holding it and philosopher two, who "
            "shares it, is not eating. <bookmark mark='d'/> Afterwards it holds it. <bookmark mark='e'/> Every other "
            "bit stays put. <bookmark mark='f'/> The disjunction over all commands is the whole system."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(enc))
            vo.wait_until("b")
            self.play(FadeIn(stg), FadeIn(stl))
            self.play(FadeIn(chi))
            vo.wait_until("c")
            line, why = steps[0], whys[0]
            self.play(FadeIn(line), FadeIn(why))
            vo.wait_until("d")
            self.play(TransformMatchingTex(line, steps[1]), ReplacementTransform(why, whys[1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(steps[1], steps[2]), ReplacementTransform(whys[1], whys[2]))
            vo.wait_until("f")
            self.play(FadeIn(total), FadeIn(tot_l))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def diagrams(self):
        od = {r["n"]: r for r in load("bdd")["order"]}[2]
        head = label(r"Binary decision diagrams", font_size=36).to_edge(UP, buff=0.3)
        f = MathTex(r"f = (x_1 = y_1) \wedge (x_2 = y_2)", font_size=34).next_to(head, DOWN, buff=0.25)
        inter = ["x1", "y1", "x2", "y2"]
        sep = ["x1", "x2", "y1", "y2"]
        tree = full_tree(inter, -6.6, -0.6, 1.75, 0.62)
        tl = label(rf"the full decision tree: \ {tree.n} tests, \ {2 ** 4} leaves", font_size=18,
                   color=GREY_A).next_to(tree, DOWN, buff=0.2)
        bi = draw_bdd(inter, -5.6, -1.6, 1.75, 0.62)
        bs = draw_bdd(sep, 0.6, 6.6, 1.75, 0.62)
        assert bi.n == od["interleaved"] and bs.n == od["separated"]
        bil = label(rf"order $x_1, y_1, x_2, y_2$: \ {bi.n} nodes", font_size=19, color=YES).next_to(bi, DOWN,
                                                                                                      buff=0.2)
        bsl = label(rf"order $x_1, x_2, y_1, y_2$: \ {bs.n} nodes", font_size=19, color=NO).next_to(bs, DOWN,
                                                                                                     buff=0.2)
        key = label(r"solid: \ the variable is 1; \ dashed: \ it is 0", font_size=17, color=GREY_B).next_to(
            f, DOWN, buff=0.1)
        notes = VGroup(
            wrapped_label(r"\textbf{reduce}: \ merge identical subgraphs, \ skip a test whose two branches agree "
                          r"\ (Bryant, \ 1986)", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"\textbf{canonical}: \ for a fixed order each function has exactly one diagram, \ so two "
                          r"sets of states are equal exactly when their diagrams are the same node", 12.4,
                          font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part 3 built the data structure for such functions. <bookmark mark='a'/> This function of four bits says"
            " two pairs are equal. As a decision tree it needs fifteen tests. <bookmark mark='b'/> Randal Bryant's "
            "reduction, of 1986, merges identical subgraphs and skips tests whose branches agree: six nodes remain. "
            "<bookmark mark='c'/> The result is canonical: for a fixed order each function has one diagram, so "
            "comparing two sets of states is a single pointer comparison. <bookmark mark='d'/> But order matters. "
            "Read both x bits before either y bit, and the diagram must remember x one while reading x two: nine "
            "nodes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(f), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(tree), FadeIn(tl))
            vo.wait_until("b")
            self.play(ReplacementTransform(tree, bi), FadeOut(tl), FadeIn(notes[0]), run_time=2)
            self.play(FadeIn(bil))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(bs), FadeIn(bsl))
        self.wait(0.4)
        self.clear_scene()

    def order(self):
        od = load("bdd")["order"]
        head = label(r"Variable order matters", font_size=36).to_edge(UP, buff=0.3)
        ns = [r["n"] for r in od]
        g = axes([0, 12.5, 2], [0, 4.5, 1], x_length=6.0, y_length=3.9, x_label=r"pairs of bits $n$",
                 y_label=r"BDD nodes \ (log scale)", xticks=range(2, 13, 2), yticks=range(0, 5),
                 fy=lambda v: rf"$10^{{{int(v)}}}$")
        g.move_to([-3.2, -0.2, 0])
        ax = g.ax
        ti = trace(ax, [(r["n"], math.log10(r["interleaved"])) for r in od], YES)
        ts = trace(ax, [(r["n"], math.log10(r["separated"])) for r in od], NO)
        di = VGroup(*[Dot(ax.c2p(r["n"], math.log10(r["interleaved"])), radius=0.04, color=YES) for r in od])
        ds = VGroup(*[Dot(ax.c2p(r["n"], math.log10(r["separated"])), radius=0.04, color=NO) for r in od])
        last = od[-1]
        li = label(rf"interleaved: \ {last['interleaved']}", font_size=18, color=YES).next_to(
            ax.c2p(ns[-1], math.log10(last["interleaved"])), UP, buff=0.15).shift(LEFT * 0.8)
        ls = label(rf"separated: \ {last['separated']:,}", font_size=18, color=NO).next_to(
            ax.c2p(ns[-1], math.log10(last["separated"])), LEFT, buff=0.2)
        assert all(r["interleaved"] == r["interleaved_formula"] and r["separated"] == r["separated_formula"]
                   for r in od)
        rows = VGroup(
            MathTex(r"(2^n - 1)", r"+", r"\sum_{k=1}^{n} 2^{\,n-k+1}", font_size=32),
            MathTex(r"(2^n - 1)", r"+", r"(2^{n+1} - 2)", font_size=32),
            MathTex(r"3 \cdot 2^n - 3", font_size=34, color=NO),
        ).arrange(DOWN, buff=0.25).move_to([3.7, 1.35, 0])
        whys = VGroup(label(r"a full tree on the $x$ bits, \ then the $y$ checks still pending", font_size=17,
                            color=GREY_A),
                      label(r"a geometric sum", font_size=17, color=GREY_A),
                      label(r"separated; \ interleaved needs only $3n$", font_size=17, color=NO))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.06)
        VGroup(*[VGroup(r, w) for r, w in zip(rows, whys)]).arrange(DOWN, buff=0.18).move_to([3.7, 1.0, 0])
        notes = VGroup(
            wrapped_label(r"finding the best order is NP-hard \ (Bollig and Wegener, \ 1996); \ tools reorder "
                          r"heuristically as they run", 5.6, font_size=19, color=WHITE),
            wrapped_label(r"and some functions have no good order: \ the middle bit of a product needs exponentially "
                          r"many nodes under every order \ (Bryant, \ 1991)", 5.6, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.7, -2.3, 0])
        with self.voiceover(
            "How much does order matter? <bookmark mark='a'/> Our package builds the same equality for up to twelve "
            "pairs. Interleaved, each pair costs three nodes: thirty-six in all. Separated: twelve thousand two "
            "hundred and eighty-five. <bookmark mark='b'/> With the x bits first, the diagram is a full tree over "
            "them, and every branch must remember which y values it still expects. <bookmark mark='c'/> Summing the "
            "levels gives three times two to the n, minus three. <bookmark mark='d'/> Finding the best order is "
            "NP-hard. And Bryant proved in 1991 that multiplication has no good order at all, the wall our SAT solver"
            " hit in Chapter 4."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(ti), FadeIn(di), run_time=1.5)
            self.play(Create(ts), FadeIn(ds), run_time=2)
            self.play(FadeIn(li), FadeIn(ls))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def image(self):
        big = {(r["n"], r["ordered"]): r for r in load("bdd")["symbolic"]}[(16, False)]
        head = label(r"Reachability, \ one image at a time", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"\mathit{Img}(S)(x')", r"=", r"\exists x.\ S(x) \wedge T(x, x')", font_size=32),
            MathTex(r"\mathit{Img}(S)(x')", r"=", r"\bigvee_a \exists x.\ S(x) \wedge T_a(x, x')", font_size=32),
            MathTex(r"R_{k+1}", r"=", r"R_k \vee \mathit{Img}(R_k)[x' \mapsto x]", font_size=32),
            MathTex(r"R_{k+1}", r"=", r"R_k \;\Rightarrow\; R_k = \text{reachable}", font_size=32, color=YES),
        ).arrange(DOWN, buff=0.22)
        for r in rows:
            r.shift(RIGHT * (rows[0][1].get_x() - r[1].get_x()))
        whys = VGroup(label(r"the successors of a set: \ one relational product", font_size=17, color=GREY_A),
                      label(r"one small relation per command, \ never the whole $T$", font_size=17, color=GREY_A),
                      label(r"rename the primed bits back; \ add the new states", font_size=17, color=GREY_A),
                      label(r"a fixpoint: \ one pointer comparison, \ by canonicity", font_size=17, color=YES))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.05)
        VGroup(*[VGroup(r, w) for r, w in zip(rows, whys)]).arrange(DOWN, buff=0.16).move_to([3.0, 0.45, 0])
        rings = VGroup(*[Ellipse(width=0.6 + 0.62 * k, height=0.42 + 0.44 * k, color=interpolate_color(
            ManimColor(DATA), ManimColor(YES), k / 6), stroke_width=2, fill_opacity=0.05).move_to([-4.0, 0.2, 0])
            for k in range(7)])
        rl = VGroup(MathTex(r"R_0", font_size=24, color=DATA).move_to(rings[0]),
                    *[MathTex(rf"R_{k}", font_size=20, color=GREY_B).move_to(
                        (rings[k].get_right() if k % 2 else rings[k].get_left()) + (LEFT if k % 2 else RIGHT) * 0.17)
                      for k in range(1, 7)])
        dots = label(r"$\dots$ \ 16 images in all", font_size=18, color=GREY_B).next_to(rings, DOWN, buff=0.15)
        foot = wrapped_label(rf"16 philosophers: \ {big['iterations']} images, \ {big['states']:,} reachable states, "
                             rf"\ a final diagram of {big['nodes']} nodes, \ {big['seconds']:.2f} s \ (Burch, \ Clarke, "
                             r"\ McMillan, \ Dill and Hwang, \ 1990: \ ``$10^{20}$ states and beyond'')", 12.4,
                             font_size=19, color=HEAD).to_edge(DOWN, buff=0.35)
        assert big["iterations"] == 16
        with self.voiceover(
            "Reachability becomes a loop over formulas. <bookmark mark='a'/> The image of a set, its successors, is "
            "one relational product: conjoin with the transition relation, then quantify away the current bits. "
            "<bookmark mark='b'/> The relation is kept as one small piece per command. <bookmark mark='c'/> Start "
            "from the initial states, add the image, rename, repeat; each round reaches one step further. <bookmark "
            "mark='d'/> When a round adds nothing, we have every reachable state, and canonicity makes noticing that "
            "one comparison. <bookmark mark='e'/> Sixteen philosophers take sixteen images: one million three hundred"
            " and thirty-one thousand seven hundred and fourteen states, in under a second."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rings[0]), FadeIn(rl[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            self.play(LaggedStart(*[AnimationGroup(Create(rings[k]), FadeIn(rl[k])) for k in range(1, 7)],
                                  lag_ratio=0.5), run_time=3)
            self.play(FadeIn(dots))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def scaling(self):
        sy = [r for r in load("bdd")["symbolic"] if not r["ordered"]]
        head = label(r"Nodes against states", font_size=36).to_edge(UP, buff=0.3)
        g = axes([1, 16.5, 1], [0, 7, 1], x_length=7.4, y_length=4.4, x_label=r"philosophers $n$",
                 y_label=r"count \ (log scale)", xticks=range(2, 17, 2), yticks=range(0, 8),
                 fy=lambda v: rf"$10^{{{int(v)}}}$")
        g.move_to([-2.6, -0.3, 0])
        ax = g.ax
        assert all(r["explicit"] == r["states"] for r in sy if "explicit" in r)
        expl = [r for r in sy if "explicit" in r]
        ts = trace(ax, [(r["n"], math.log10(r["states"])) for r in sy], HEAD)
        tn = trace(ax, [(r["n"], math.log10(r["nodes"])) for r in sy], YES)
        ds = VGroup(*[Dot(ax.c2p(r["n"], math.log10(r["states"])), radius=0.045, color=HEAD) for r in sy])
        dn = VGroup(*[Dot(ax.c2p(r["n"], math.log10(r["nodes"])), radius=0.045, color=YES) for r in sy])
        de = VGroup(*[Circle(radius=0.09, color=WHITE, stroke_width=1.5).move_to(
            ax.c2p(r["n"], math.log10(r["explicit"]))) for r in expl])
        last = sy[-1]
        ls = label(rf"reachable states: \ {last['states']:,}", font_size=18, color=HEAD).next_to(
            ax.c2p(last["n"], math.log10(last["states"])), UP, buff=0.15).shift(LEFT * 1.4)
        ln = label(rf"BDD nodes: \ {last['nodes']}", font_size=18, color=YES).next_to(
            ax.c2p(last["n"], math.log10(last["nodes"])), UP, buff=0.2).shift(LEFT * 0.8)
        step = sy[-1]["nodes"] - sy[-2]["nodes"]
        assert all(b["nodes"] - a["nodes"] == step for a, b in zip(sy[4:], sy[5:]))
        notes = VGroup(
            wrapped_label(rf"states multiply by about {sy[-1]['states'] / sy[-2]['states']:.1f} per philosopher; "
                          rf"\ the diagram grows by {step} nodes", 4.4, font_size=19, color=WHITE),
            wrapped_label(rf"white rings: \ the explicit checker's counts, \ identical up to $n = {expl[-1]['n']}$",
                          4.4, font_size=19, color=GREY_A),
            wrapped_label(rf"the transition relation itself: \ {last['relation_nodes']:,} nodes for $n = "
                          rf"{last['n']}$; \ the deadlock is found in it too: \ {last['deadlock_states']} state",
                          4.4, font_size=19, color=NO),
            wrapped_label(r"structure, \ not size, \ decides: \ a ring of identical neighbours is BDD-friendly; \ a "
                          r"multiplier is not", 4.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.5, -0.2, 0])
        with self.voiceover(
            "Here is the pay-off. <bookmark mark='a'/> In yellow, the reachable states, past a million at sixteen "
            "philosophers. In green, the diagram that holds them: it grows by just eight nodes per philosopher, to "
            "one hundred and seventeen. <bookmark mark='b'/> Up to eight philosophers the explicit checker's counts "
            "agree exactly. <bookmark mark='c'/> And the deadlock is found symbolically too. <bookmark mark='d'/> The"
            " lesson: structure, not size, decides. A ring of identical neighbours suits a BDD; a multiplier does "
            "not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(ts), FadeIn(ds), run_time=2)
            self.play(FadeIn(ls))
            self.play(Create(tn), FadeIn(dn), run_time=2)
            self.play(FadeIn(ln), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(de), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def bmc(self):
        bd = load("bdd")
        run = next(b for b in bd["bmc"] if b["n"] == 7)
        good = next(b for b in bd["bmc_ordered"] if b["n"] == 5)
        dia = next(r for r in load("philosophers")["rows"] if r["n"] == 5 and r["ordered"])["diameter"]
        head = label(r"Bounded model checking", font_size=36).to_edge(UP, buff=0.3)
        fml = MathTex(r"I(s_0)", r"\wedge T(s_0, s_1)", r"\wedge \cdots", r"\wedge T(s_{k-1}, s_k)",
                      r"\wedge \mathit{Dead}(s_k)", font_size=36).next_to(head, DOWN, buff=0.3)
        fml[0].set_color(DATA)
        fml[4].set_color(NO)
        fl = label(r"satisfiable exactly when a deadlock is reachable in $k$ steps: \ one CNF for Part 26's solver",
                   font_size=18, color=GREY_A).next_to(fml, DOWN, buff=0.12)
        rows = [[f"{r['k']}", f"{r['vars']:,}", f"{r['clauses']:,}", r"SAT" if r["sat"] else r"UNSAT",
                 f"{r['conflicts']:,}"] for r in run["rows"]]
        colors = [[WHITE, GREY_A, GREY_A, NO if r["sat"] else YES, GREY_A] for r in run["rows"]]
        tab = grid_table([r"$k$", r"variables", r"clauses", r"answer", r"conflicts"], rows,
                         widths=[0.7, 1.45, 1.35, 1.3, 1.4], row_h=0.37, font_size=19, colors=colors, mono_cols=())
        tab.next_to(fl, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        tcap = label(r"seven philosophers, \ $k = 0, 1, 2, \dots$", font_size=18, color=GREY_B).next_to(
            tab, DOWN, buff=0.12).align_to(tab, LEFT)
        found = run["found"]
        chips = VGroup(*[tag_box(a, color=NO, size=15) for a in found["actions"]]).arrange_in_grid(
            rows=2, buff=(0.15, 0.15))
        cl = label(rf"the model at $k = {found['k']}$, \ decoded: \ every philosopher holds one fork", font_size=18,
                   color=NO)
        right = VGroup(cl, chips).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        notes = VGroup(
            wrapped_label(rf"forks in a global order, \ five philosophers: \ UNSAT for every $k \le {good['kmax']}$; \ "
                          rf"all reachable states lie within {dia} steps \ (the diameter), \ so this is a proof",
                          5.4, font_size=19, color=YES),
            wrapped_label(r"no diameter in sight? \ $k$-induction \ (Sheeran, \ Singh and St{\aa}lmarck, \ 2000) \ "
                          r"and IC3 \ (Bradley, \ 2011) \ prove properties of unbounded runs with the same solvers",
                          5.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(right, notes).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(tab, RIGHT, buff=0.5).align_to(
            tab, UP)
        assert not any(r["sat"] for r in good["rows"]) and good["kmax"] >= dia
        hard = max(run["rows"], key=lambda r: r["conflicts"])
        assert not hard["sat"]
        with self.voiceover(
            "SAT solvers attack the explosion from the other side. <bookmark mark='a'/> Bounded model checking, from "
            "Biere, Cimatti, Clarke and Zhu in 1999, unrolls the transitions k times: an initial state, k steps, and "
            "a deadlock at the end. A satisfying assignment is a counterexample. <bookmark mark='b'/> For seven "
            "philosophers we try k equals zero, one, two, and so on. The refutations get harder: k equals six costs "
            "two thousand five hundred and ninety-eight conflicts. <bookmark mark='c'/> At seven the formula is "
            "satisfiable, and the decoded model is the deadlock. <bookmark mark='d'/> With ordered forks, every bound"
            " up to seven is unsatisfiable, and every reachable state lies within five steps, so that is a proof. "
            "<bookmark mark='e'/> Without a known diameter, k-induction and IC3 prove unbounded properties with the "
            "same solvers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(fml), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0], tab.rule)), FadeIn(tcap))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:-1]], lag_ratio=0.3), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[-1])))
            self.play(FadeIn(cl), LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.2), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
        assert hard["k"] == 6 and hard["conflicts"] == 2598 and good["kmax"] == 7 and dia == 5
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, mono)
