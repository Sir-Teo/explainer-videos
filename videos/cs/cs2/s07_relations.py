from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import CLOCK, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES

DIVS = [d for d in range(1, 61) if 60 % d == 0]


def omega(n: int) -> int:
    k, p = 0, 2
    while n > 1:
        while n % p == 0:
            n //= p
            k += 1
        p += 1
    return k


def arrow_diagram(n_left, n_right, pairs, color=FUNC, gap=0.62, width=3.2) -> VGroup:
    L = VGroup(*[Dot(radius=0.1, color=DATA) for _ in range(n_left)]).arrange(DOWN, buff=gap - 0.2)
    R = VGroup(*[Dot(radius=0.1, color=CTRL) for _ in range(n_right)]).arrange(DOWN, buff=gap - 0.2)
    R.next_to(L, RIGHT, buff=width)
    R.match_y(L)
    eL = Ellipse(width=0.9, height=L.height + 0.8, stroke_color=GREY_C).move_to(L)
    eR = Ellipse(width=0.9, height=R.height + 0.8, stroke_color=GREY_C).move_to(R)
    arr = VGroup(*[Arrow(L[a].get_center(), R[b].get_center(), buff=0.14, stroke_width=3, color=color,
                         max_tip_length_to_length_ratio=0.1) for a, b in pairs])
    g = VGroup(eL, eR, L, R, arr)
    g.L, g.R, g.arr = L, R, arr
    return g


class Relations(VoiceoverScene):
    def construct(self):
        self.card()
        self.functions()
        self.equivalence()
        self.orders()
        self.dilworth()

    def card(self):
        card = chapter_card(6, r"Sets, relations, functions", r"What shapes can mathematical data take?", part=PART)
        with self.voiceover("Chapter six. Sets, relations and functions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def functions(self):
        head = label(r"Functions, \ and three properties they can have", font_size=38).to_edge(UP, buff=0.35)
        inj = arrow_diagram(3, 4, [(0, 0), (1, 2), (2, 3)])
        sur = arrow_diagram(4, 3, [(0, 0), (1, 1), (2, 1), (3, 2)])
        bij = arrow_diagram(4, 4, [(0, 1), (1, 3), (2, 0), (3, 2)], color=YES)
        for g in (inj, sur, bij):
            g.scale(0.72)
        Group(inj, sur, bij).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.3)
        caps = VGroup(
            VGroup(label(r"one-to-one \ (injective)", font_size=26, color=FUNC),
                   note(r"no two arrows land together", font_size=21)),
            VGroup(label(r"onto \ (surjective)", font_size=26, color=FUNC),
                   note(r"every target is hit", font_size=21)),
            VGroup(label(r"a bijection", font_size=26, color=YES), note(r"both: \ a perfect pairing", font_size=21)),
        )
        for c, g in zip(caps, (inj, sur, bij)):
            c.arrange(DOWN, buff=0.1).next_to(g, DOWN, buff=0.35)
        defn = label(r"a function $f: A \to B$ \ sends every element of $A$ \ to exactly one element of $B$",
                     font_size=28, color=GREY_A).next_to(head, DOWN, buff=0.35)
        use = note(r"a bijection between two finite sets \ proves they have the same size: \ the heart of counting",
                   font_size=24, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Almost everything in mathematics, and in a program's data, is built from three things: sets, relations "
            "and functions. <bookmark mark='a'/> A function from A to B sends every element of A to exactly one "
            "element of B. Draw it as arrows. <bookmark mark='b'/> It is one-to-one, injective, if no two arrows land "
            "on the same element. A hash function that is one-to-one never has a collision. <bookmark mark='c'/> It is "
            "onto, surjective, if every element of B is hit. <bookmark mark='d'/> And it is a bijection if it is both: a "
            "perfect pairing. <bookmark mark='e'/> Bijections are how we count, and how Part 1 compared infinite sets. "
            "Two finite sets have the same size exactly when there is a bijection between them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defn))
            for mk, g, c in zip("bcd", (inj, sur, bij), caps):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*g[:4])), LaggedStart(*[GrowArrow(a) for a in g.arr], lag_ratio=0.2),
                          FadeIn(c), run_time=1.6)
            vo.wait_until("e")
            self.play(FadeIn(use))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def equivalence(self):
        head = label(r"Equivalence relations cut a set into classes", font_size=38).to_edge(UP, buff=0.35)
        props = VGroup(*[label(t, font_size=27, color=c) for t, c in (
            (r"reflexive: \ $x \sim x$", GREY_A),
            (r"symmetric: \ $x \sim y \Rightarrow y \sim x$", GREY_A),
            (r"transitive: \ $x \sim y,\ y \sim z \Rightarrow x \sim z$", GREY_A),
        )]).arrange(RIGHT, buff=0.6).next_to(head, DOWN, buff=0.35)
        ex = label(r"$x \sim y$ \ when \ $x - y$ is a multiple of $3$", font_size=30, color=CLOCK).next_to(
            props, DOWN, buff=0.35)
        cols = [DATA, CTRL, FUNC]
        nums = VGroup(*[VGroup(Circle(0.3, stroke_color=cols[k % 3], stroke_width=3, fill_color="#121722",
                                      fill_opacity=1),
                               MathTex(str(k), font_size=28)) for k in range(15)]).arrange(RIGHT, buff=0.18)
        nums.move_to(UP * 0.7)
        classes = VGroup()
        for r in range(3):
            g = VGroup(*[nums[k].copy() for k in range(r, 15, 3)]).arrange(RIGHT, buff=0.18)
            classes.add(g)
        classes.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.7 + LEFT * 1.0)
        tags = VGroup(*[MathTex(rf"[{r}]", font_size=34, color=cols[r]).next_to(classes[r], LEFT, buff=0.4)
                        for r in range(3)])
        side = VGroup(note(r"the puzzle's positions: \ two classes \ (reachable from each other)", font_size=22),
                      note(r"states a machine cannot tell apart: \ Part 5 (Myhill--Nerode)", font_size=22)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DR, buff=0.35)
        with self.voiceover(
            "A relation is just a set of pairs: which elements are related to which. One kind deserves a name. "
            "<bookmark mark='a'/> An equivalence relation is reflexive, symmetric and transitive: everything is related "
            "to itself, the relation goes both ways, and it chains. <bookmark mark='b'/> Example: call two integers "
            "related when their difference is a multiple of three. <bookmark mark='c'/> Then the integers fall apart "
            "into three classes, the numbers that leave remainder zero, one and two, and every integer is in exactly "
            "one. Every equivalence relation does this: it partitions its set into disjoint classes. "
            "<bookmark mark='d'/> The puzzle's positions under can reach each other form two classes, the hook's two "
            "halves. And in Part 5, the states of a machine that no input can tell apart form classes, and merging "
            "each class into one state gives the smallest machine possible."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(props, lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(ex), FadeIn(nums, lag_ratio=0.05))
            vo.wait_until("c")
            self.play(*[TransformFromCopy(nums[k], classes[k % 3][k // 3]) for k in range(15)], run_time=2.0)
            self.play(FadeIn(tags))
            vo.wait_until("d")
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hasse(self, scale=1.0):
        ranks = {}
        for d in DIVS:
            ranks.setdefault(omega(d), []).append(d)
        pos = {}
        for r, ds in ranks.items():
            for i, d in enumerate(ds):
                pos[d] = np.array([(i - (len(ds) - 1) / 2) * 1.5, (r - 2) * 1.15, 0]) * scale
        nodes = {d: VGroup(Circle(0.3 * scale, stroke_color=DATA, stroke_width=2.5, fill_color="#121722",
                                  fill_opacity=1),
                           MathTex(str(d), font_size=int(28 * scale))).move_to(pos[d]) for d in DIVS}
        edges = VGroup(*[Line(pos[a], pos[b], buff=0.3 * scale, color=GREY_C, stroke_width=2)
                         for a in DIVS for b in DIVS if b % a == 0 and omega(b) == omega(a) + 1])
        g = VGroup(edges, *nodes.values())
        g.nodes, g.edges, g.pos = nodes, edges, pos
        return g

    def orders(self):
        head = label(r"Partial orders: \ ``divides'' on the divisors of $60$", font_size=38).to_edge(UP, buff=0.35)
        h = self.hasse().move_to(LEFT * 2.6 + DOWN * 0.4)
        props = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"reflexive, \ transitive, \ and antisymmetric: \\ $a \mid b$ and $b \mid a$ \ only if $a = b$", GREY_A),
            (r"partial: \ $4$ and $6$ are incomparable", HEAD),
            (r"lines join $a$ to $b$ when $b / a$ is prime \\ (a Hasse diagram)", GREY_B),
            (r"any two have a greatest lower bound ($\gcd$) \\ and a least upper bound ($\mathrm{lcm}$): \ a lattice",
             YES),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.6 + DOWN * 0.2)
        uses = note(r"lattices: \ dataflow analysis (Part 13), \ CRDTs that merge without conflict (Part 39)",
                    font_size=22).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "A second kind of relation orders things. <bookmark mark='a'/> Take the divisors of sixty, related by "
            "divides. It is reflexive and transitive, and antisymmetric: if a divides b and b divides a, they are equal. "
            "That makes it a partial order. <bookmark mark='b'/> Partial, because some pairs are not comparable at all: "
            "four does not divide six, and six does not divide four. <bookmark mark='c'/> Draw only the steps that "
            "multiply by one prime, with bigger numbers higher, and the whole order is visible: a divides b exactly when "
            "there is an upward path. <bookmark mark='d'/> Any two elements here have a greatest common lower bound, "
            "their gcd, and a least common upper bound, their lcm. An order with that property is a lattice. Lattices "
            "come back twice: compilers use them to combine what they know about a program, and replicated databases "
            "use them to merge edits without conflicts."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*h.nodes.values()), lag_ratio=0.05), FadeIn(props[0]))
            vo.wait_until("b")
            self.play(Indicate(h.nodes[4], color=HEAD), Indicate(h.nodes[6], color=HEAD), FadeIn(props[1]))
            vo.wait_until("c")
            self.play(Create(h.edges), FadeIn(props[2]), run_time=1.6)
            vo.wait_until("d")
            for d in (4, 6):
                h.nodes[d][0].set_stroke(HEAD)
            self.play(h.nodes[2][0].animate.set_stroke(YES, 5), h.nodes[12][0].animate.set_stroke(YES, 5),
                      FadeIn(props[3]))
            self.play(FadeIn(uses))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dilworth(self):
        head = label(r"Chains and antichains", font_size=38).to_edge(UP, buff=0.35)
        h = self.hasse(scale=0.9).move_to(LEFT * 2.8 + DOWN * 0.4)
        chains = [[1, 2, 4, 12, 60], [3, 6, 30], [5, 10, 20], [15]]
        ccols = [HEAD, CTRL, FUNC, INF]
        anti = [4, 6, 10, 15]
        txt = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"chain: \ every two comparable", GREY_A),
            (r"antichain: \ no two comparable", GREY_A),
            (r"the largest antichain here: \ $\{4, 6, 10, 15\}$", NO),
            (r"the fewest chains that cover everything: \ $4$", YES),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.4 + UP * 0.5)
        thm = theorem_card(r"Dilworth (1950)", r"In any finite partial order, the largest antichain has exactly as many "
                           r"elements as the fewest chains that cover it.", width=5.7, font_size=22)
        thm.next_to(txt, DOWN, buff=0.4).align_to(txt, LEFT)
        lines = VGroup()
        for ch, col in zip(chains, ccols):
            for a, b in zip(ch, ch[1:]):
                lines.add(Line(h.nodes[a].get_center(), h.nodes[b].get_center(), buff=0.27, color=col,
                               stroke_width=7))
        rings = [h.nodes[d][0].animate.set_stroke(col, 5) for ch, col in zip(chains, ccols) for d in ch]
        with self.voiceover(
            "One theorem about orders, because it turns up in scheduling. <bookmark mark='a'/> A chain is a set in "
            "which every two elements are comparable, like one, two, four, twelve, sixty. An antichain is a set in "
            "which no two are. <bookmark mark='b'/> Here the largest antichain has four elements: four, six, ten and "
            "fifteen. <bookmark mark='c'/> And the whole order can be covered by four chains, and no fewer. "
            "<bookmark mark='d'/> Robert Dilworth proved in 1950 that those two numbers are always equal. Read the "
            "order as tasks that must come before others: an antichain is work that can run at the same time, and a "
            "chain is work one processor must do in sequence. Part 10, with its many cores, meets this trade-off "
            "head on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(h))
            vo.wait_until("a")
            self.play(FadeIn(txt[0]), FadeIn(txt[1]))
            vo.wait_until("b")
            self.play(*[h.nodes[d][0].animate.set_fill(NO, 0.6) for d in anti], FadeIn(txt[2]))
            vo.wait_until("c")
            self.play(Create(lines), *rings, FadeIn(txt[3]), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(thm))
        self.wait(0.3)
        self.clear_scene()
