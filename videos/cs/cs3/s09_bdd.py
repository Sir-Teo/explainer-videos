from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, load


def draw_bdd(nodes, order, root, width=5.0, height=4.6, origin=ORIGIN, names=None, r=0.24, font_size=24):
    """nodes: [id, var, lo, hi]; order: variables top to bottom.  lo edges dashed, hi edges solid."""
    names = names or {v: f"x_{{{v + 1}}}" for v in order}
    level = {v: i for i, v in enumerate(order)}
    by_level = {}
    for nid, v, lo, hi in nodes:
        by_level.setdefault(level[v], []).append(nid)
    L = len(order) + 1
    pos = {}
    o = np.asarray(origin, float)
    for lv, ids in by_level.items():
        ids.sort()
        for i, nid in enumerate(ids):
            x = (i - (len(ids) - 1) / 2) * min(width / max(len(ids), 1), 1.3)
            pos[nid] = o + np.array([x, height / 2 - lv * height / (L - 1), 0])
    pos[0] = o + np.array([-0.8, -height / 2, 0])
    pos[1] = o + np.array([0.8, -height / 2, 0])
    g = VGroup()
    edges = VGroup()
    for nid, v, lo, hi in nodes:
        for tgt, dashed in ((lo, True), (hi, False)):
            a, b = pos[nid], pos[tgt]
            d = (b - a) / max(np.linalg.norm(b - a), 1e-6)
            seg = (DashedLine if dashed else Line)(a + d * r, b - d * (r if tgt > 1 else 0.22),
                                                   color=GREY_C if dashed else GREY_A, stroke_width=2.5)
            edges.add(seg)
    circ = VGroup()
    for nid, v, lo, hi in nodes:
        circ.add(VGroup(Circle(r, stroke_color=DATA, stroke_width=2.5, fill_color="#121722", fill_opacity=1),
                        MathTex(names[v], font_size=font_size, color=DATA)).move_to(pos[nid]))
    terms = VGroup(*[VGroup(Square(0.4, stroke_color=YES if t else GREY_B, stroke_width=2.5, fill_color="#121722",
                                   fill_opacity=1), MathTex(str(t), font_size=26)).move_to(pos[t]) for t in (0, 1)])
    g.add(edges, circ, terms)
    g.n_nodes = len(nodes) + 2
    return g


class Bdd(VoiceoverScene):
    def construct(self):
        self.card()
        self.reduce()
        self.order()
        self.uses()

    def card(self):
        card = chapter_card(8, r"Decision diagrams", r"Is there a canonical form that is usually small?", part=PART)
        with self.voiceover("Chapter eight. Decision diagrams."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def reduce(self):
        head = label(r"From a decision tree to a diagram", font_size=38).to_edge(UP, buff=0.35)
        # majority of three: the full tree, 7 decision nodes, 8 leaves
        maj = [1 if bin(k).count("1") >= 2 else 0 for k in range(8)]
        pos, nodes, leaves = {}, VGroup(), VGroup()
        edges = VGroup()
        for lvl, name in enumerate(("a", "b", "c")):
            n = 2 ** lvl
            for i in range(n):
                p = np.array([(i - (n - 1) / 2) * (6.4 / n) - 3.0, 1.8 - lvl * 1.15, 0])
                pos[(lvl, i)] = p
                nodes.add(VGroup(Circle(0.24, stroke_color=DATA, stroke_width=2.5, fill_color="#121722",
                                        fill_opacity=1), MathTex(name, font_size=26, color=DATA)).move_to(p))
        for i, v in enumerate(maj):
            p = np.array([(i - 3.5) * 0.8 - 3.0, 1.8 - 3 * 1.15, 0])
            pos[(3, i)] = p
            leaves.add(VGroup(Square(0.38, stroke_color=YES if v else GREY_B, stroke_width=2.5, fill_color="#121722",
                                     fill_opacity=1), MathTex(str(v), font_size=24)).move_to(p))
        for lvl in range(3):
            for i in range(2 ** lvl):
                for j, dashed in ((2 * i, True), (2 * i + 1, False)):
                    a, b = pos[(lvl, i)], pos[(lvl + 1, j)]
                    edges.add((DashedLine if dashed else Line)(a + DOWN * 0.24, b + UP * 0.22,
                                                               color=GREY_C if dashed else GREY_A, stroke_width=2))
        key = note(r"dashed: \ the variable is 0; \ solid: \ it is 1", font_size=22).next_to(leaves, DOWN, buff=0.25)
        rules = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"1. \ share identical subgraphs", CTRL),
            (r"2. \ delete a test whose two branches agree", CTRL),
            (r"repeat until neither applies: \\ a \textit{reduced ordered BDD}", YES),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.7 + UP * 2.0)
        # the reduced diagram for majority (order a, b, c): 4 decision nodes
        red = [[2, 0, 3, 4], [3, 1, 0, 5], [4, 1, 5, 1], [5, 2, 0, 1]]
        bdd = draw_bdd(red, [0, 1, 2], 2, width=2.4, height=2.8, origin=RIGHT * 3.7 + DOWN * 1.0,
                       names={0: "a", 1: "b", 2: "c"}, r=0.22)
        cnt = label(r"15 nodes \ $\to$ \ 6", font_size=26, color=YES).next_to(bdd, DOWN, buff=0.3)
        with self.voiceover(
            "Truth tables and normal forms are either huge or not unique. In 1986 Randal Bryant made a data structure "
            "that is often small and always unique. <bookmark mark='a'/> Start with a decision tree. Here is majority: "
            "test a, then b, then c, and read the answer at a leaf. Dashed lines are zero, solid lines one. It is just "
            "the truth table, spread out. <bookmark mark='b'/> Now apply two rules. Share any two identical pieces, so "
            "all the zero leaves become one leaf and all the ones another. And delete any test whose two branches lead "
            "to the same place, because it does not matter. <bookmark mark='c'/> Repeat until neither rule applies. "
            "What remains is a reduced ordered binary decision diagram: for majority, four tests instead of seven."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(edges), FadeIn(nodes), FadeIn(leaves), FadeIn(key), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rules[0]), FadeIn(rules[1]))
            vo.wait_until("c")
            self.play(FadeIn(rules[2]), FadeIn(bdd), FadeIn(cnt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def order(self):
        d = load("bdd")
        k3 = d["k3"]
        head = label(r"The order of the variables matters, \ exponentially", font_size=36).to_edge(UP, buff=0.3)
        f = MathTex(r"f = x_1 x_2 + x_3 x_4 + x_5 x_6", font_size=36, color=CODE).next_to(head, DOWN, buff=0.25)
        good = draw_bdd(k3["good"], k3["good_order"], k3["root_good"], width=2.6, height=4.4,
                        origin=LEFT * 4.2 + DOWN * 1.0, r=0.22, font_size=20)
        bad = draw_bdd(k3["bad"], k3["bad_order"], k3["root_bad"], width=5.6, height=4.4,
                       origin=RIGHT * 0.1 + DOWN * 1.0, r=0.22, font_size=20)
        gl = label(rf"order $x_1, x_2, x_3, \dots$: \ {good.n_nodes} nodes", font_size=24, color=YES).next_to(
            good, UP, buff=0.15)
        bl = label(rf"order $x_1, x_3, x_5, x_2, \dots$: \ {bad.n_nodes} nodes", font_size=24, color=NO).next_to(
            bad, UP, buff=0.15)
        rows = d["rows"]
        tab = VGroup()
        for r in rows:
            row = VGroup(MathTex(str(2 * r['k']), font_size=28, color=GREY_A),
                         MathTex(str(r['good']), font_size=28, color=YES),
                         MathTex(fmt(r['bad']), font_size=28, color=NO))
            for j, m in enumerate(row):
                m.move_to([4.55 + 0.85 * j, 0, 0])
            tab.add(row)
        for i, row in enumerate(tab):
            row.shift(UP * (0.9 - 0.42 * i))
        tl = VGroup(*[note(t, font_size=20).move_to([4.55 + 0.85 * j, 1.45, 0])
                      for j, t in enumerate((r"vars", r"good", r"bad"))])
        with self.voiceover(
            "There is a catch. <bookmark mark='a'/> Take x one and x two, or x three and x four, or x five and x six. "
            "Test the variables in their natural order, and the diagram is a neat ladder: eight nodes. "
            "<bookmark mark='b'/> Test all the odd ones first, then the even ones, and the diagram has to remember "
            "which of the first three were one before it can see their partners: sixteen nodes. "
            "<bookmark mark='c'/> Computed for more pairs, the good order grows by two nodes per pair; the bad order "
            "doubles. With fourteen variables, sixteen nodes against two hundred and fifty-six. Finding the best order "
            "is itself NP-hard, so real tools reorder heuristically as they go."
        ) as vo:
            self.play(FadeIn(head), FadeIn(f))
            vo.wait_until("a")
            self.play(FadeIn(good), FadeIn(gl), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(bad), FadeIn(bl), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(tl), LaggedStart(*[FadeIn(t) for t in tab], lag_ratio=0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uses(self):
        head = label(r"Why canonical matters", font_size=38).to_edge(UP, buff=0.4)
        lines = VGroup(*[label(t, font_size=28, color=c) for t, c in (
            (r"fixed order $\Rightarrow$ every function has exactly one reduced diagram", YES),
            (r"so ``are these two circuits equivalent?'' \ becomes \ ``are these two pointers equal?''", HEAD),
            (r"and, or, not, \ and ``is there an input that makes $f = 1$?'' \ are fast on diagrams", GREY_A),
            (r"the cost moved into the size: \ some functions, \ like multiplication, \\ have exponential diagrams "
             r"under \textit{every} order \ (Bryant, 1991)", NO),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.75)
        for l in lines:
            l.scale(0.88, about_edge=LEFT)
        red = [[2, 0, 3, 4], [3, 1, 0, 5], [4, 1, 5, 1], [5, 2, 0, 1]]
        bdd = draw_bdd(red, [0, 1, 2], 2, width=2.0, height=2.6, origin=RIGHT * 2.4 + UP * 1.15,
                       names={0: "a", 1: "b", 2: "c"}, r=0.2, font_size=22)
        root = bdd[1][0]
        boxes = VGroup()
        for t, c in ((r"\text{spec: }\ ab + bc + ca", GREY_A), (r"\text{optimized: }\ ab + c\,(a \oplus b)", CTRL)):
            m = MathTex(t, font_size=30, color=c)
            boxes.add(VGroup(SurroundingRectangle(m, buff=0.15, color=GREY_D, corner_radius=0.08), m))
        boxes.arrange(DOWN, buff=0.7, aligned_edge=RIGHT).move_to(LEFT * 3.0 + UP * 1.6)
        ptrs = VGroup(*[Arrow(b.get_right(), root.get_left() + UP * 0.08 * (1 - 2 * k), buff=0.12, stroke_width=3,
                              color=HEAD, max_tip_length_to_length_ratio=0.06) for k, b in enumerate(boxes)])
        pq = VGroup(*[MathTex(n, font_size=28, color=HEAD).next_to(a.get_center(), UP if k == 0 else DOWN, buff=0.12)
                      for k, (n, a) in enumerate(zip("pq", ptrs))])
        eq = MathTex(r"p = q \ \checkmark", font_size=32, color=YES).next_to(bdd, RIGHT, buff=0.5).shift(UP * 0.9)
        later = note(r"hardware verification, \ model checking: \ Part 54; \ SAT solvers, \ the other approach: \ Part 26",
                     font_size=22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why go to this trouble? <bookmark mark='a'/> Because with the order fixed, every function has exactly one "
            "reduced diagram. <bookmark mark='b'/> So to check that a clever optimized circuit computes the same "
            "function as its simple specification, build both diagrams in one shared table and compare two pointers. "
            "<bookmark mark='c'/> And, or and not on diagrams, and asking whether any input makes the function true, "
            "are all fast, taking time proportional to the sizes of the diagrams involved. Counting how many inputs "
            "make a function true is fast too: one pass over the nodes. That made decision diagrams the workhorse of "
            "chip verification in the 1990s. "
            "<bookmark mark='d'/> The catch never goes away: Bryant also proved that the middle output bit of a "
            "multiplier has an exponentially large diagram under every possible order. Part 54 uses them anyway, where "
            "they work, and Part 26 meets the other great approach, satisfiability solvers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes))
            vo.wait_until("a")
            self.play(FadeIn(bdd), FadeIn(lines[0], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in ptrs], lag_ratio=0.4), FadeIn(lines[1], shift=RIGHT * 0.1))
            self.play(FadeIn(pq), FadeIn(eq), Indicate(root, color=HEAD))
            for mk, l in zip("cd", lines[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=RIGHT * 0.1))
            self.play(FadeIn(later))
        self.wait(0.3)
        self.clear_scene()


def fmt(n) -> str:
    return f"{int(n):,}".replace(",", "{,}")
