from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import FAIL, FCOL, GCOST, HEUR, HIST, LEARN, PART, PATH, SYMBOL, load

NAMES = "abcde"
# an illustrative formula: clauses as tuples of (variable index, sign)
FORMULA = [((0, 1), (1, 1)), ((0, 0), (2, 1)), ((0, 0), (2, 0), (3, 1)), ((3, 0), (4, 1)), ((3, 0), (4, 0)),
           ((1, 1), (2, 0)), ((1, 0), (2, 1), (4, 1))]


def lit_tex(v, s):
    return ("" if s else r"\lnot ") + NAMES[v]


def small_dpll(clauses, n):
    """DPLL on a tiny formula, recording its tree: each node has the decision, the unit propagations it caused and
    how it ended ('conflict', 'sat' or 'split')."""
    nodes = []

    def propagate(assign):
        forced = []
        while True:
            changed = False
            for c in clauses:
                if any(assign.get(v) == bool(s) for v, s in c):
                    continue
                open_ = [(v, s) for v, s in c if v not in assign]
                if not open_:
                    return forced, False
                if len(open_) == 1:
                    v, s = open_[0]
                    assign[v] = bool(s)
                    forced.append((v, s))
                    changed = True
            if not changed:
                return forced, True

    def go(assign, parent, decision):
        a = dict(assign)
        if decision is not None:
            a[decision[0]] = bool(decision[1])
        forced, ok = propagate(a)
        k = len(nodes)
        nodes.append({"parent": parent, "decision": decision, "forced": forced, "end": None, "children": []})
        if parent is not None:
            nodes[parent]["children"].append(k)
        if not ok:
            nodes[k]["end"] = "conflict"
            return False
        if all(any(a.get(v) == bool(s) for v, s in c) for c in clauses):
            nodes[k]["end"] = "sat"
            return True
        v = min(i for i in range(n) if i not in a)
        nodes[k]["end"] = "split"
        for val in (1, 0):
            if go(a, k, (v, val)):
                return True
        return False

    go({}, None, None)
    return nodes


def _names(lits):
    out = [("not " if not s else "") + NAMES[v] for v, s in lits]
    return out[0] if len(out) == 1 else ", ".join(out[:-1]) + " and " + out[-1]


def describe(nodes) -> str:
    """The run of small_dpll in words, node by node, in the order it happened."""
    out = []
    for nd in nodes:
        if nd["decision"] is None:
            continue
        v, s = nd["decision"]
        t = f"try {NAMES[v]} {'true' if s else 'false'}"
        if nd["forced"]:
            t += f", which forces {_names(nd['forced'])}"
        if nd["end"] == "conflict":
            t += ", and a clause fails: back up."
        elif nd["end"] == "sat":
            t += ", and every clause holds."
        else:
            t += "."
        out.append(t[0].upper() + t[1:])
    return " ".join(out)


class SAT(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.dpll()
        self.transition()
        self.hardness()
        self.cdcl()
        self.learning_pays()

    def card(self):
        card = chapter_card(9, r"Satisfiability", r"Can these constraints all be true at once?", lit=(1962,), part=PART)
        with self.voiceover("Chapter nine. Satisfiability."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def problem(self):
        f = MathTex(r"(a \lor b)", r"\land", r"(\lnot a \lor c)", r"\land", r"(\lnot a \lor \lnot c \lor d)", r"\land",
                    r"(\lnot d \lor e)", r"\land", r"(\lnot d \lor \lnot e)", r"\land", r"(b \lor \lnot c)", r"\land",
                    r"(\lnot b \lor c \lor e)", font_size=34).move_to(UP * 2.2)
        if f.width > 13.2:
            f.width = 13.2
        tag = note(r"illustrative").next_to(f, DOWN, buff=0.15)
        dc = definition_card(r"SAT", r"given clauses (ors of variables and their negations), \ is there an "
                             r"assignment of true and false that makes every clause true?", width=6.0, font_size=22,
                             color=PATH).move_to([-3.4, -0.6, 0])
        hc = history_card(1971, r"Stephen Cook; \ Leonid Levin (1973)", r"SAT is NP-complete: \ every problem whose "
                          r"answers can be checked quickly can be rewritten as SAT", width=6.0, color=HIST,
                          font_size=21).move_to([3.4, -0.6, 0])
        uses = label(r"scheduling, \ chip verification, \ planning, \ puzzles, \ cryptanalysis, \ mathematics",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Strip logic down to its core and you get one problem. <bookmark mark='a'/> Given clauses, each an or of variables "
            "or their negations, can every variable be set true or false so that every clause holds? That is satisfiability, "
            "SAT. <bookmark mark='b'/> In 1971 Stephen Cook, and independently Leonid Levin, showed that any problem whose "
            "solutions can be checked quickly can be rewritten as SAT: the first NP-complete problem. <bookmark mark='c'/> And yet SAT solvers became one of "
            "AI's great practical successes."
        ) as vo:
            self.play(FadeIn(f), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(dc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(uses))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dpll(self):
        nodes = small_dpll(FORMULA, 5)

        def tree_of(k):
            return {"children": [tree_of(c) for c in nodes[k]["children"]]}

        tree = SearchTree(tree_of(0), width=6.0, level_height=1.5, radius=0.13, center=[-2.6, 0.35, 0])
        fm = MathTex(r"(a \lor b)", r"\land", r"(\lnot a \lor c)", r"\land", r"(\lnot a \lor \lnot c \lor d)", r"\land",
                     r"(\lnot d \lor e)", r"\land", r"(\lnot d \lor \lnot e)", r"\land", r"(b \lor \lnot c)", r"\land",
                     r"(\lnot b \lor c \lor e)", font_size=28, color=GREY_A).to_edge(UP, buff=0.3)
        if fm.width > 13.2:
            fm.width = 13.2
        # SearchTree numbers nodes breadth-first; map our depth-first ids onto them
        order = []
        q = [0]
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
                v, s_ = nd["decision"]
                parts.append(lit_tex(v, s_))
            if nd["forced"]:
                parts.append(r"\Rightarrow " + ",".join(lit_tex(v, s_) for v, s_ in nd["forced"]))
            if parts:
                labels[k] = MathTex(r"\ ".join(parts), font_size=24, color=FCOL).next_to(tree.nodes[i], RIGHT, buff=0.12)
            if nd["end"] in ("conflict", "sat"):
                ends[k] = MathTex(r"\times" if nd["end"] == "conflict" else r"\checkmark", font_size=34,
                                  color=FAIL if nd["end"] == "conflict" else PATH).next_to(tree.nodes[i], DOWN, buff=0.1)
        story = describe(nodes)
        steps = VGroup(
            label(r"1. \ unit propagation: \ a clause with one open literal forces it", font_size=22, color=FCOL),
            label(r"2. \ branch: \ pick a variable, try true, then false", font_size=22, color=GCOST),
            label(r"3. \ a clause with every literal false: \ conflict, \ back up", font_size=22, color=FAIL),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([3.6, 1.6, 0])
        if steps.width > 6.4:
            steps.width = 6.4
            steps.set_x(3.6)
        hcs = VGroup(history_card(1960, r"Davis \& Putnam", r"", width=3.0, color=HIST, font_size=18),
                     history_card(1962, r"Davis, Logemann \& Loveland", r"", width=3.4, color=HIST, font_size=18))
        hcs.arrange(RIGHT, buff=0.2).to_corner(DR, buff=0.25)
        tag = note(r"computed on the illustrative formula").to_corner(DL, buff=0.2)
        with self.voiceover(
            "The classic method is DPLL, from Martin Davis and Hilary Putnam in 1960, made practical with George Logemann and "
            "Donald Loveland in 1962. <bookmark mark='a'/> Propagate: a clause with one literal left open forces it. "
            "<bookmark mark='b'/> When nothing is forced, branch: pick a variable, try true, propagate. <bookmark mark='c'/> If "
            "a clause has every literal false, back up and try the other value. <bookmark mark='d'/> On our little formula: " +
            story
        ) as vo:
            steps.set_opacity(0.3)
            self.play(FadeIn(tag), FadeIn(hcs), FadeIn(fm), FadeIn(steps), FadeIn(tree.nodes[0]))
            for k_, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(steps[k_].animate.set_opacity(1.0))
            vo.wait_until("d")
            for k in range(len(nodes)):
                i = idx[k]
                anims = [Create(tree.edges[i]), FadeIn(tree.nodes[i])] if i > 0 else []
                anims += [FadeIn(labels[k])] if k in labels else []
                anims += [FadeIn(ends[k], scale=1.4)] if k in ends else []
                if anims:
                    self.play(*anims, run_time=0.9)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def transition(self):
        d = load("sat3")
        A = np.asarray(d["alphas"], float)
        ns = d["ns"]
        cols = [GREY_B, HEUR, FCOL, PATH][: len(ns)]
        g = axes([A[0], A[-1]], [0, 1], x_length=7.0, y_length=4.2, xlabel=r"clauses per variable, \ $m / n$",
                 ylabel=r"chance a random formula is satisfiable", xticks=[3, 4, 5],
                 yticks=[0, 0.5, 1], yfmt=lambda v: rf"{int(100 * v)}\%", center=[-2.0, -0.4, 0])
        lines = VGroup(*[curve(g.ax, A, d[f"psat_{n}"], c, 4) for n, c in zip(ns, cols)])
        lg = legend([(c, rf"$n = {n}$ variables") for n, c in zip(ns, cols)], font_size=20).move_to([4.6, 2.2, 0])
        thr = DashedLine(g.ax.c2p(4.267, 0), g.ax.c2p(4.267, 1), color=GREY_A, dash_length=0.08)
        tl = label(r"$4.267$", font_size=20, color=GREY_A).next_to(g.ax.c2p(4.267, 0.93), RIGHT, buff=0.08)
        cross = VGroup(*[label(rf"$n = {n}$: \ half at ${d[f'cross_{n}']:.2f}$, \ $90\%\to10\%$ over ${d[f'width_{n}']:.2f}$",
                               font_size=19, color=c) for n, c in zip(ns, cols)]).arrange(DOWN, buff=0.12,
                                                                                         aligned_edge=LEFT)
        cross.move_to([4.6, 0.0, 0])
        if cross.width > 4.6:
            cross.width = 4.6
            cross.set_x(4.6)
        cite_ = note(r"$4.267$: \ the cavity method of statistical physics \\ (M\'ezard, Parisi \& Zecchina 2002); "
                     r"\\ proved bounds: \ $3.52$ and $4.49$", font_size=18).next_to(cross, DOWN, buff=0.45)
        cite_.set_x(min(cite_.get_x(), 6.9 - cite_.width / 2))
        tag = note(rf"computed: \ DPLL on ${sum(d['per']) * len(A):,}$ random formulas".replace(",", "{,}"))
        tag.to_corner(DR, buff=0.2)
        n0, n1 = ns[0], ns[-1]
        w0, w1 = d[f"width_{n0}"], d[f"width_{n1}"]
        sharper = w1 < w0
        verdict = (f"The bigger the formulas, the sharper the step: for {n0} variables the chance falls from ninety "
                   f"to ten percent over a span of {w0:.2f} in the ratio; for {n1}, over {w1:.2f}." if sharper else
                   f"Here the step is about as wide for {n1} variables as for {n0}.")
        with self.voiceover(
            "In 1992 David Mitchell, Bart Selman and Hector Levesque asked what random formulas look like: n variables, m "
            "clauses of three random literals. <bookmark mark='a'/> With few clauses per variable, almost every formula is "
            "satisfiable; with many, almost none; in between, the chance drops off a cliff. <bookmark mark='b'/> " + verdict +
            " <bookmark mark='c'/> As n grows, the step becomes a jump, near a ratio of four point two seven. Physicists "
            "predicted 4.267 with a method from the theory of disordered magnets; mathematicians have proved the threshold lies "
            "between 3.52 and 4.49. A phase transition, like water freezing, in a logic problem."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(lg[0]), run_time=1.5)
            vo.wait_until("b")
            for i in range(1, len(ns)):
                self.play(Create(lines[i]), FadeIn(lg[i]), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(c) for c in cross], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(Create(thr), FadeIn(tl), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hardness(self):
        d = load("sat3")
        A = np.asarray(d["alphas"], float)
        ns = d["ns"]
        cols = [GREY_B, HEUR, FCOL, PATH][: len(ns)]
        top = np.ceil(np.log10(max(max(d[f"median_{n}"]) for n in ns))) + 0.3
        g = axes([A[0], A[-1]], [0, top], x_length=7.0, y_length=4.2, xlabel=r"clauses per variable, \ $m / n$",
                 ylabel=r"DPLL's decisions \ (median, log scale)", xticks=[3, 4, 5],
                 yticks=list(range(0, int(top) + 1)), yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.0, -0.4, 0])
        lines = VGroup(*[curve(g.ax, A, np.log10(np.maximum(d[f"median_{n}"], 1)), c, 4) for n, c in zip(ns, cols)])
        lg = legend([(c, rf"$n = {n}$") for n, c in zip(ns, cols)], font_size=20).move_to([4.6, 2.2, 0])
        n1 = ns[-1]
        pk = d[f"peak_{n1}"]
        med = np.asarray(d[f"median_{n1}"])
        lo_side, hi_side = med[0], med[-1]
        txt = VGroup(label(r"easy: \ satisfiable, \ solutions everywhere", font_size=20, color=PATH),
                     label(r"hard: \ near the threshold", font_size=20, color=FAIL),
                     label(r"easy again: \ contradictions are found fast", font_size=20, color=GCOST))
        txt.arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([4.6, 0.0, 0])
        if txt.width > 4.6:
            txt.width = 4.6
            txt.set_x(4.6)
        with self.voiceover(
            "The transition is also where the problems are hard. <bookmark mark='a'/> Count DPLL's decisions: far below the "
            "threshold a solution is found almost at once, far above, a contradiction. <bookmark mark='b'/> For "
            f"{n1} variables, the median peaks at a ratio of {pk:.1f}, at {med.max():,.0f} decisions, against {lo_side:,.0f} at "
            f"the left edge and {hi_side:,.0f} at the right. Easy, hard, easy."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.3), FadeIn(lg), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(txt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cdcl(self):
        d = load("cdcl")["example"]
        trail = d["trail"]
        learned = d["learned"]
        bj = d["backjump"]
        # place each assigned literal: decisions in a column by level, implied ones to the right in trail order
        pos, mobs = {}, VGroup()
        dec_y = {}
        imp_x = -1.0
        for lit, lvl, reason in trail:
            v = abs(lit)
            txt = rf"x_{{{v}}} = {1 if lit > 0 else 0} @ {lvl}"
            col = GCOST if reason is None else FCOL
            m = MathTex(txt, font_size=26, color=col)
            if reason is None:
                dec_y[lvl] = 2.4 - 1.05 * (lvl - 1)
                m.move_to([-5.4, dec_y[lvl], 0])
            else:
                m.move_to([imp_x, 0.0, 0])
            pos[v] = m
            mobs.add(m)
        # implied literals: spread them in order, two rows
        imp = [abs(l) for l, lv, r in trail if r is not None]
        for k, v in enumerate(imp):
            pos[v].move_to([-2.4 + 1.9 * (k // 2) + 0.95 * (k % 2), 1.2 - 2.2 * (k % 2), 0])
        kappa = MathTex(r"\kappa", font_size=40, color=FAIL).move_to([4.6, -0.2, 0])
        edges = VGroup()
        for lit, lvl, reason in trail:
            if reason is None:
                continue
            v = abs(lit)
            for q in reason:
                if abs(q) != v and abs(q) in pos:
                    edges.add(Arrow(pos[abs(q)].get_right(), pos[v].get_left(), buff=0.08, stroke_width=2,
                                    color=GREY_C, max_tip_length_to_length_ratio=0.12))
        for q in d["conflict"]:
            if abs(q) in pos:
                edges.add(Arrow(pos[abs(q)].get_right(), kappa.get_left(), buff=0.08, stroke_width=2, color=FAIL,
                                max_tip_length_to_length_ratio=0.12))
        uip = abs(learned[0])
        ring = SurroundingRectangle(pos[uip], color=LEARN, buff=0.08)
        lc = " \\lor ".join((r"\lnot " if l < 0 else "") + f"x_{{{abs(l)}}}" for l in learned)
        lt = MathTex(lc, font_size=36, color=LEARN)
        box = VGroup(label(r"learned clause:", font_size=24, color=LEARN), lt).arrange(RIGHT, buff=0.25)
        box.to_edge(DOWN, buff=1.15)
        jump = label(rf"jump back to level ${bj}$, \ where it forces $\lnot x_{{{uip}}}$ at once", font_size=22,
                     color=GREY_A).next_to(box, DOWN, buff=0.15)
        hcs = VGroup(history_card(1996, r"Marques-Silva \& Sakallah: \ GRASP", r"", width=3.6, color=HIST, font_size=18),
                     history_card(2001, r"Moskewicz et al.: \ Chaff", r"", width=3.6, color=HIST, font_size=18))
        hcs.arrange(DOWN, buff=0.15).to_corner(UR, buff=0.25)
        tag = note(r"computed: \ our CDCL solver, \ first conflict; \ illustrative clauses").to_corner(DL, buff=0.2)
        with self.voiceover(
            "Modern solvers add one idea: learn from every mistake. <bookmark mark='a'/> Here a solver has made four "
            "decisions, one per level, and propagation has implied a cascade, each arrow from the literals that forced it. "
            "<bookmark mark='b'/> It ends in a conflict. DPLL would just undo the last decision. <bookmark mark='c'/> "
            "Conflict-driven clause learning asks why: it traces the conflict back to the first point every path passes "
            f"through, here x {uip}. <bookmark mark='d'/> The reasons become a new clause, implied by the formula, that rules out "
            "this combination forever. <bookmark mark='e'/> Then the solver jumps back, past irrelevant decisions, to level "
            f"{bj}. With clever branching and cheap bookkeeping, from GRASP in 1996 and Chaff in 2001, every competitive solver "
            "works this way."
        ) as vo:
            self.play(FadeIn(hcs), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in mobs], lag_ratio=0.15))
            self.play(LaggedStart(*[GrowArrow(e) for e in edges if e.get_color() != ManimColor(FAIL)], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(kappa), *[GrowArrow(e) for e in edges if e.get_color() == ManimColor(FAIL)])
            vo.wait_until("c")
            self.play(Create(ring))
            vo.wait_until("d")
            self.play(FadeIn(box, shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(jump))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learning_pays(self):
        d = load("cdcl")
        W = np.asarray(d["adder_widths"])
        dp, cd = np.asarray(d["adder_dpll"], float), np.asarray(d["adder_cdcl"], float)
        top = np.ceil(np.log10(dp.max())) + 0.3
        g = axes([W[0] - 0.5, W[-1] + 0.5], [0, top], x_length=6.4, y_length=4.2,
                 xlabel=r"bits in each adder", ylabel=r"work \ (log scale)", xticks=list(W[::2]),
                 yticks=list(range(0, int(top) + 1, 2)), yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.6, -0.4, 0])
        l1 = curve(g.ax, W, np.log10(dp), GCOST, 4)
        l2 = curve(g.ax, W, np.log10(cd), LEARN, 4)
        p1 = VGroup(*[Dot(g.ax.c2p(x, np.log10(y)), radius=0.05, color=GCOST) for x, y in zip(W, dp)])
        p2 = VGroup(*[Dot(g.ax.c2p(x, np.log10(y)), radius=0.05, color=LEARN) for x, y in zip(W, cd)])
        lg = legend([(GCOST, r"DPLL: \ decisions"), (LEARN, r"CDCL: \ conflicts")], font_size=20).move_to([3.8, 2.2, 0])
        q = label(r"do two adders, \ ripple-carry and \\ Kogge--Stone, \ ever disagree?", font_size=22, color=GREY_A)
        q.move_to([3.8, 0.8, 0])
        growth = float(np.exp(np.mean(np.diff(np.log(dp[2:])))))  # the typical factor per extra bit
        txt = VGroup(label(rf"${int(W[-1])}$ bits: \ DPLL ${dp[-1]:,.0f}$".replace(",", "{,}"), font_size=21, color=GCOST),
                     label(rf"CDCL ${cd[-1]:,.0f}$".replace(",", "{,}"), font_size=21, color=LEARN))
        txt.arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([3.8, -0.6, 0])
        tag = note(r"computed: \ our solvers; \ the answer is no (the formulas are unsatisfiable)").to_corner(DR,
                                                                                                          buff=0.2)
        big = d["proved"]
        b64 = big[str(max(int(k) for k in big))]
        w64 = max(int(k) for k in big)
        with self.voiceover(
            "Learning is not a small improvement. Ask whether two circuits for adding binary numbers ever disagree, written "
            "as clauses that are satisfiable exactly when they do. <bookmark mark='a'/> DPLL, remembering nothing, needs about "
            f"{growth:.0f} times as many decisions for every extra bit: {dp[-1]:,.0f} for {int(W[-1])}-bit adders. "
            f"<bookmark mark='b'/> Our clause-learning solver needs {cd[-1]:,.0f} conflicts, up from {cd[0]:,.0f} at "
            f"{int(W[0])} bits, and proves two {w64}-bit adders equal on all two to the {2 * w64} inputs with "
            f"{b64['conflicts']:,} conflicts."
        ) as vo:
            self.play(FadeIn(g), FadeIn(q), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(l1), FadeIn(p1), FadeIn(lg[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(l2), FadeIn(p2), FadeIn(lg[1]), FadeIn(txt), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
