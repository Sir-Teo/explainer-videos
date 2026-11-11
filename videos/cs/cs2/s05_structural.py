from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, live_int


def layout(t, x=0.0, y=0.0, dx=2.0, dy=0.9, out=None, edges=None, parent=None):
    """Positions for a binary tree given as nested [left, right] lists (None is a leaf)."""
    if out is None:
        out, edges = [], []
    me = len(out)
    out.append((np.array([x, y, 0.0]), t is None))
    if parent is not None:
        edges.append((parent, me))
    if t is not None:
        layout(t[0], x - dx, y - dy, dx / 2, dy, out, edges, me)
        layout(t[1], x + dx, y - dy, dx / 2, dy, out, edges, me)
    return out, edges


def tree_mob(t, dx=2.0, dy=0.9, r=0.16) -> VGroup:
    pts, edges = layout(t, dx=dx, dy=dy)
    g = VGroup()
    g.edges = VGroup(*[Line(pts[a][0], pts[b][0], color=GREY_C, stroke_width=2.5) for a, b in edges])
    g.nodes = VGroup()
    for p, leaf in pts:
        if leaf:
            g.nodes.add(Square(r * 1.7, stroke_width=0, fill_color=YES, fill_opacity=1).move_to(p))
        else:
            g.nodes.add(Circle(r, stroke_width=0, fill_color=CTRL, fill_opacity=1).move_to(p))
    g.add(g.edges, g.nodes)
    g.leaves = sum(1 for _, leaf in pts if leaf)
    g.internal = len(pts) - g.leaves
    return g


class Structural(VoiceoverScene):
    def construct(self):
        self.card()
        self.strings()
        self.proof_strings()
        self.trees()
        self.expressions()

    def card(self):
        card = chapter_card(4, r"Induction on structures", r"How do you prove something about every string, every tree?",
                            part=PART)
        with self.voiceover("Chapter four. Induction on structures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def strings(self):
        head = label(r"A set defined by rules", font_size=38).to_edge(UP, buff=0.4)
        rules = VGroup(
            label(r"rule 1: \ the empty string $\varepsilon$ is balanced", font_size=30, color=YES),
            label(r"rule 2: \ if $s$ and $t$ are balanced, \ so is \ \texttt{(}$\,s\,$\texttt{)}$\,t$", font_size=30,
                  color=CTRL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.45)
        gen = [[r"\varepsilon"], [r"\texttt{()}"], [r"\texttt{()()}", r"\texttt{(())}"],
               [r"\texttt{()()()}", r"\texttt{()(())}", r"\texttt{(())()}", r"\texttt{(()())}", r"\texttt{((()))}"]]
        rows = VGroup()
        for k, g in enumerate(gen):
            r = VGroup(*[MathTex(s, font_size=44, color=DATA) for s in g]).arrange(RIGHT, buff=0.7)
            rows.add(VGroup(MathTex(rf"{k}\ \text{{pairs:}}", font_size=28, color=GREY_B), r).arrange(RIGHT, buff=0.5))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(rules, DOWN, buff=0.55)
        cnt = note(r"1, \ 1, \ 2, \ 5, \ \dots \ \ (chapter 11 counts them)", font_size=24).next_to(rows, DOWN, buff=0.3)
        with self.voiceover(
            "Computer science is full of sets defined by rules rather than by formulas: strings a grammar allows, "
            "trees, expressions, lists, programs. <bookmark mark='a'/> Here is a small one: balanced parentheses. The "
            "empty string is balanced. And if s and t are balanced, then an open bracket, s, a close bracket, then t, "
            "is balanced. Nothing else is. <bookmark mark='b'/> Apply the rules, and the set grows: the empty string; "
            "one pair; two ways with two pairs; five with three. <bookmark mark='c'/> These are the Catalan numbers, "
            "and chapter eleven counts them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rules, lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rows], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(cnt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof_strings(self):
        head = label(r"Structural induction", font_size=38).to_edge(UP, buff=0.4)
        claim = label(r"claim: \ every balanced string, \ read left to right, \\ never has more closes than opens, \ "
                      r"and ends at zero", font_size=30, color=DATA).next_to(head, DOWN, buff=0.4)
        steps = VGroup(*[label(t, font_size=25, color=c) for t, c in (
            (r"rule 1: \ $\varepsilon$: \ the count starts and ends at $0$", YES),
            (r"rule 2: \ \texttt{(}$\,s\,$\texttt{)}$\,t$: \ assume the claim for $s$ and $t$", GREY_A),
            (r"the \texttt{(} lifts $s$'s whole walk by one: \ never below $1$, \ back to $1$", CTRL),
            (r"the \texttt{)} returns to $0$; \ then $t$'s walk, \ from $0$ to $0$", CTRL),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(claim, DOWN, buff=0.45).to_edge(LEFT, buff=0.5)
        # the walk of (()())(): +1 for (, -1 for )
        w = "(()())()"
        h = np.cumsum([0] + [1 if c == "(" else -1 for c in w])
        ax = Axes(x_range=[0, len(w), 1], y_range=[0, 3, 1], x_length=5.0, y_length=2.0, tips=False,
                  axis_config={"color": GREY_C}).move_to(RIGHT * 3.9 + DOWN * 1.0)
        path = VMobject(color=HEAD, stroke_width=4).set_points_as_corners([ax.c2p(i, v) for i, v in enumerate(h)])
        chars = VGroup(*[Text(c, font="DejaVu Sans Mono", font_size=24, color=DATA).move_to(ax.c2p(i + 0.5, -0.55))
                         for i, c in enumerate(w)])
        wl = note(r"the count of opens minus closes", font_size=20).next_to(ax, UP, buff=0.1)
        rule = label(r"prove the claim for the base rule, \ and show each rule preserves it", font_size=28,
                     color=HEAD).to_edge(DOWN, buff=0.25).to_edge(LEFT, buff=0.6)
        with self.voiceover(
            "To prove something about every member of such a set, follow the rules that build it. "
            "<bookmark mark='a'/> Claim: in a balanced string, reading left to right, the count of opens minus closes "
            "never goes negative, and ends at zero. Here is that count for one string, as a walk. "
            "<bookmark mark='b'/> Rule one: the empty string's walk starts and ends at zero. <bookmark mark='c'/> Rule "
            "two: assume the claim for s and t, and look at open, s, close, t. The open bracket lifts the whole of s's "
            "walk up by one, so it never drops below one and comes back to one. The close bracket brings it to zero, "
            "and t's walk goes from zero to zero. <bookmark mark='d'/> That is structural induction: prove the claim for "
            "what the base rules make, and show that every rule preserves it. Ordinary induction is the special case "
            "where the only rules are zero, and plus one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(claim), Create(ax), FadeIn(chars), FadeIn(wl))
            self.play(Create(path), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(steps[0]))
            vo.wait_until("c")
            self.play(FadeIn(steps[1]))
            self.play(FadeIn(steps[2]))
            self.play(FadeIn(steps[3]))
            vo.wait_until("d")
            self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trees(self):
        head = label(r"Full binary trees: \ leaves $=$ internal nodes $+ 1$", font_size=38).to_edge(UP, buff=0.35)
        rules = VGroup(label(r"a leaf \ \ is a tree", font_size=28, color=YES),
                       label(r"a node with two trees below \ is a tree", font_size=28, color=CTRL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UL, buff=0.5).shift(DOWN * 0.8)
        seq = [None, [None, None], [[None, None], None], [[None, None], [None, None]],
               [[None, [None, None]], [None, None]], [[None, [None, None]], [[None, None], [None, [None, None]]]]]
        trees = [tree_mob(t, dx=1.6, dy=0.68) for t in seq]
        for t in trees:
            t.move_to(RIGHT * 2.2 + UP * 0.2)
        L = live_int(1, 34, YES)
        I = live_int(0, 34, CTRL)
        counts = VGroup(VGroup(label(r"leaves:", font_size=28, color=GREY_A), L).arrange(RIGHT, buff=0.2),
                        VGroup(label(r"internal:", font_size=28, color=GREY_A), I).arrange(RIGHT, buff=0.2)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).next_to(rules, DOWN, buff=0.6).align_to(rules, LEFT)
        L.add_updater(lambda m: m.next_to(counts[0][0], RIGHT, buff=0.2))
        I.add_updater(lambda m: m.next_to(counts[1][0], RIGHT, buff=0.2))
        proof = VGroup(MathTex(r"\text{leaf: } 1 = 0 + 1", font_size=32, color=YES),
                       MathTex(r"\text{node: } L_1 + L_2 = (I_1 + 1) + (I_2 + 1) = (I_1 + I_2 + 1) + 1", font_size=32,
                               color=CTRL)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4)
        use = note(r"every expression tree, \ every tournament bracket, \ every merge of a sort (Part 16)",
                   font_size=22).next_to(proof, UP, buff=0.25)
        cur = trees[0]
        with self.voiceover(
            "Trees are the other great recursive structure. <bookmark mark='a'/> Here we use full binary trees: either a leaf, "
            "or a node with exactly two full binary subtrees. <bookmark mark='b'/> Build some and count. One leaf, no internal nodes. "
            "Grow it: two leaves, one node. Three and two. Four and three. Whatever shape, the leaves outnumber the "
            "internal nodes by exactly one. <bookmark mark='c'/> The proof follows the definition. A leaf: one leaf, "
            "zero nodes. A node: its leaves are the leaves of its two subtrees; by the hypothesis each has one more leaf "
            "than nodes; add the new node, and the difference is still one. A knockout tournament with sixty-four teams "
            "therefore plays exactly sixty-three games, whatever the bracket looks like."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rules, lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(cur), FadeIn(counts))
            for t in trees[1:]:
                self.play(ReplacementTransform(cur, t), L.tracker.animate.set_value(t.leaves),
                          I.tracker.animate.set_value(t.internal), run_time=1.0)
                cur = t
                self.wait(0.4)
            vo.wait_until("c")
            self.play(FadeIn(proof, lag_ratio=0.3), FadeIn(use))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def expressions(self):
        head = label(r"Expressions are trees, \ and meaning is defined by recursion", font_size=36).to_edge(UP, buff=0.35)
        # (2 + 3) * (7 - 1)
        pos = {"*": UP * 1.6, "+": LEFT * 2.0 + UP * 0.4, "-": RIGHT * 2.0 + UP * 0.4, "2": LEFT * 3.0 + DOWN * 0.8,
               "3": LEFT * 1.0 + DOWN * 0.8, "7": RIGHT * 1.0 + DOWN * 0.8, "1": RIGHT * 3.0 + DOWN * 0.8}
        shift = LEFT * 2.4 + DOWN * 0.4
        nodes = {k: VGroup(Circle(0.34, stroke_color=CTRL if k in "*+-" else DATA, stroke_width=2.5,
                                  fill_color="#121722", fill_opacity=1),
                           MathTex(r"\times" if k == "*" else k, font_size=36, color=CTRL if k in "*+-" else DATA)
                           ).move_to(p + shift) for k, p in pos.items()}
        edges = VGroup(*[Line(nodes[a].get_center(), nodes[b].get_center(), buff=0.36, color=GREY_C) for a, b in (
            ("*", "+"), ("*", "-"), ("+", "2"), ("+", "3"), ("-", "7"), ("-", "1"))])
        vals = {"+": 5, "-": 6, "*": 30}
        vtags = {k: MathTex(str(v), font_size=30, color=YES).next_to(nodes[k], UP if k == "*" else LEFT, buff=0.12)
                 for k, v in vals.items()}
        vtags["-"].next_to(nodes["-"], RIGHT, buff=0.12)
        src = MathTex(r"(2 + 3) \times (7 - 1)", font_size=40, color=CODE).next_to(head, DOWN, buff=0.4).shift(LEFT * 2.4)
        defn = VGroup(*[MathTex(t, font_size=32) for t in (
            r"\mathrm{val}(n) = n",
            r"\mathrm{val}(e_1 + e_2) = \mathrm{val}(e_1) + \mathrm{val}(e_2)",
            r"\mathrm{val}(e_1 - e_2) = \mathrm{val}(e_1) - \mathrm{val}(e_2)",
            r"\mathrm{val}(e_1 \times e_2) = \mathrm{val}(e_1) \times \mathrm{val}(e_2)",
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.3 + UP * 0.6)
        later = VGroup(note(r"parse trees and evaluators: \ Part 12", font_size=24),
                       note(r"type derivations and type safety: \ Part 14", font_size=24)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).next_to(defn, DOWN, buff=0.6).align_to(defn, LEFT)
        with self.voiceover(
            "The structure that matters most to us is the expression. <bookmark mark='a'/> Two plus three, times seven "
            "minus one, is a tree: operators at the nodes, numbers at the leaves. <bookmark mark='b'/> Its meaning is "
            "defined by recursion on the same structure. The value of a number is itself. The value of a sum is the "
            "sum of the values of its parts, and similarly for a difference and a product. <bookmark mark='c'/> Evaluate bottom up: five, "
            "six, thirty. <bookmark mark='d'/> Every interpreter is this definition, written as a program, and every "
            "fact about such programs, that evaluation always finishes, that a well-typed program never goes wrong, is "
            "proved by structural induction on this tree. Part 12 builds the parser that makes the tree; Part 14 "
            "proves the type system safe."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src), FadeIn(edges), LaggedStart(*[FadeIn(n_) for n_ in nodes.values()], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(defn, lag_ratio=0.3))
            vo.wait_until("c")
            for k in ("+", "-", "*"):
                self.play(Circumscribe(nodes[k], color=HEAD, buff=0.04), FadeIn(vtags[k], scale=1.3), run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(later))
        self.wait(0.3)
        self.clear_scene()
