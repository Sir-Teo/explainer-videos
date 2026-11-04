from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import ADV, CTRL, DATA, FUNC, HEAD, INF, LIMIT, NO, PART, YES, load


class Cardinality(VoiceoverScene):
    def construct(self):
        self.card()
        self.rationals()
        self.pairing()
        self.bernstein()
        self.cantor()

    def card(self):
        card = chapter_card(7, r"Sizes of infinity", r"When are two infinite sets the same size?", lit=(1874, 1891),
                            part=PART)
        with self.voiceover("Chapter seven. Sizes of infinity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def rationals(self):
        d = load("rationals")
        cw = d["calkin_wilf"]
        head = label(r"Every positive fraction, \ exactly once", font_size=38).to_edge(UP, buff=0.3)
        rule = label(r"each $\tfrac{p}{q}$ has two children: \ $\tfrac{p}{p + q}$ \ and \ $\tfrac{p + q}{q}$",
                     font_size=30, color=CTRL).next_to(head, DOWN, buff=0.3)
        nodes = []
        levels = 4
        for k in range(2 ** levels - 1):
            lvl = int(np.floor(np.log2(k + 1)))
            i = k + 1 - 2 ** lvl
            n = 2 ** lvl
            x = (i - (n - 1) / 2) * (12.4 / n)
            y = 1.4 - lvl * 1.05
            p, q = cw[k]
            nodes.append(MathTex(rf"\tfrac{{{p}}}{{{q}}}", font_size=38 if lvl < 3 else 32,
                                 color=[HEAD, DATA, FUNC, INF][lvl]).move_to([x, y, 0]))
        edges = VGroup(*[Line(nodes[k].get_bottom(), nodes[c].get_top(), buff=0.08, color=GREY_D, stroke_width=1.5)
                         for k in range(2 ** (levels - 1) - 1) for c in (2 * k + 1, 2 * k + 2)])
        seq = MathTex(r",\ ".join(rf"\tfrac{{{p}}}{{{q}}}" for p, q in cw[:15]) + r",\ \dots", font_size=34,
                      color=GREY_A).to_edge(DOWN, buff=0.55)
        why = note(r"read the tree row by row: \ every positive rational appears once, \ in lowest terms \ "
                   r"(Calkin and Wilf, 2000)", font_size=22).next_to(seq, UP, buff=0.18)
        with self.voiceover(
            "Part 1 said the fractions can be listed. Here is a listing so neat it was only found in the year 2000. "
            "<bookmark mark='a'/> Start with one over one. Every fraction p over q has two children: p over p plus q, "
            "and p plus q over q. <bookmark mark='b'/> The tree grows: one half and two; one third, three halves, two "
            "thirds, three. <bookmark mark='c'/> Neil Calkin and Herbert Wilf proved that every positive fraction "
            "appears in this tree exactly once, already in lowest terms. So reading it row by row lists them all, with "
            "no repeats: a bijection between the natural numbers and the positive rationals. There are exactly as many "
            "fractions as whole numbers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rule), FadeIn(nodes[0]))
            vo.wait_until("b")
            for lvl in range(1, levels):
                ks = range(2 ** lvl - 1, 2 ** (lvl + 1) - 1)
                es = [edges[(k - 1)] for k in ks]
                self.play(*[Create(e) for e in es], *[FadeIn(nodes[k], shift=DOWN * 0.15) for k in ks], run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(why), Write(seq), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pairing(self):
        d = load("rationals")
        P = d["pairing"]
        head = label(r"Pairs of numbers, \ numbered by a formula", font_size=38).to_edge(UP, buff=0.35)
        n = 6
        cells = VGroup()
        for x in range(n):
            for y in range(n):
                v = P[x][y]
                diag = x + y
                cells.add(VGroup(Square(0.66, stroke_color=GREY_D, stroke_width=1,
                                        fill_color=interpolate_color(ManimColor(DATA), ManimColor(INF), diag / 10),
                                        fill_opacity=0.25),
                                 MathTex(str(v), font_size=28)).move_to([y * 0.66, -x * 0.66, 0]))
        cells.move_to(LEFT * 3.0 + DOWN * 0.5)
        xl = MathTex("x", font_size=32, color=DATA).next_to(cells, LEFT, buff=0.3)
        yl = MathTex("y", font_size=32, color=DATA).next_to(cells, UP, buff=0.2)
        f = MathTex(r"\pi(x, y) = \frac{(x + y)(x + y + 1)}{2} + y", font_size=42, color=FUNC).move_to(
            RIGHT * 3.2 + UP * 0.9)
        txt = VGroup(note(r"pairs on diagonal $s = x + y$ \ come after the $\tfrac{s(s+1)}{2}$ \ on earlier diagonals",
                          font_size=22),
                     note(r"a bijection $\mathbb{N} \times \mathbb{N} \to \mathbb{N}$, \ with an inverse you can compute",
                          font_size=22)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(f, DOWN, buff=0.4)
        use = label(r"so a program can encode any pair, \ list, \\ or program \ as one number", font_size=26,
                    color=HEAD).next_to(txt, DOWN, buff=0.5)
        with self.voiceover(
            "Part 1 walked the grid of pairs along its diagonals. That walk has a formula. <bookmark mark='a'/> Number "
            "the pair x, y by where it falls in the walk. <bookmark mark='b'/> The pairs on diagonal s come after all "
            "the earlier diagonals, which hold one plus two up to s pairs, the sum from chapter three. Add y, the "
            "position along the diagonal, and you have Cantor's pairing function. <bookmark mark='c'/> It is a bijection "
            "from pairs of numbers to numbers, and both directions are computable. Apply it again and again, and a "
            "single number can encode a list, a tree, or a whole program. That is how Gödel encoded statements as "
            "numbers, and how Part 25 will let programs talk about programs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(xl), FadeIn(yl),
                      LaggedStart(*[FadeIn(c) for c in sorted(cells, key=lambda m: int(m[1].tex_string))],
                                  lag_ratio=0.03), run_time=2.6)
            vo.wait_until("b")
            self.play(Write(f), FadeIn(txt[0]))
            vo.wait_until("c")
            self.play(FadeIn(txt[1]), FadeIn(use))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bernstein(self):
        head = label(r"Injections both ways are enough", font_size=38).to_edge(UP, buff=0.35)
        thm = theorem_card(r"Cantor--Schr\"oder--Bernstein", r"If $A$ injects into $B$ and $B$ injects into $A$, then "
                           r"there is a bijection between them.", width=8.0, font_size=26).next_to(head, DOWN, buff=0.4)
        a = NumberLine(x_range=[0, 1, 0.25], length=5.0, color=DATA, include_numbers=True, font_size=22).move_to(
            UP * -0.9 + LEFT * 3.2)
        b = NumberLine(x_range=[0, 1, 0.25], length=5.0, color=CTRL, include_numbers=True, font_size=22).move_to(
            UP * -0.9 + RIGHT * 3.2)
        la = MathTex(r"(0, 1)", font_size=32, color=DATA).next_to(a, UP, buff=0.3)
        lb = MathTex(r"[0, 1]", font_size=32, color=CTRL).next_to(b, UP, buff=0.3)
        open_ends = VGroup(Circle(0.08, color=DATA, stroke_width=3).move_to(a.n2p(0)),
                           Circle(0.08, color=DATA, stroke_width=3).move_to(a.n2p(1)))
        closed = VGroup(Dot(b.n2p(0), color=CTRL, radius=0.08), Dot(b.n2p(1), color=CTRL, radius=0.08))
        f = MathTex(r"f(x) = x", font_size=32, color=FUNC)
        g = MathTex(r"g(y) = \tfrac{y}{2} + \tfrac14", font_size=32, color=FUNC)
        VGroup(f, g).arrange(RIGHT, buff=2.0).to_edge(DOWN, buff=1.2)
        fn = note(r"$(0,1)$ into $[0,1]$", font_size=22).next_to(f, DOWN, buff=0.12)
        gn = note(r"$[0,1]$ into $[\tfrac14, \tfrac34] \subset (0,1)$", font_size=22).next_to(g, DOWN, buff=0.12)
        concl = label(r"so they are the same size, \ though no simple formula pairs them", font_size=26,
                      color=YES).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Finding an exact bijection can be hard. A theorem makes it unnecessary. <bookmark mark='a'/> If A fits "
            "one-to-one inside B, and B fits one-to-one inside A, then there is a bijection between them. "
            "<bookmark mark='b'/> Example: the open interval from zero to one, and the closed one, which also contains "
            "its two endpoints. <bookmark mark='c'/> The open one sits inside the closed one, unchanged. The closed one "
            "shrinks into the middle half of the open one. So they are the same size, even though writing down a "
            "pairing between them takes real ingenuity. The proof follows each element back and forth through the two "
            "maps and builds the pairing from those chains."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(Create(a), Create(b), FadeIn(la), FadeIn(lb), FadeIn(open_ends), FadeIn(closed))
            vo.wait_until("c")
            self.play(FadeIn(f), FadeIn(fn))
            self.play(FadeIn(g), FadeIn(gn))
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cantor(self):
        head = label(r"Cantor's theorem: \ every set is smaller than its set of subsets", font_size=36).to_edge(UP,
                                                                                                        buff=0.35)
        elems = ["a", "b", "c", "d"]
        imgs = [r"\{a, c\}", r"\{a\}", r"\{\,\}", r"\{a, b, c, d\}"]
        inside = [True, False, False, True]
        rows = VGroup()
        for e, s, ins in zip(elems, imgs, inside):
            rows.add(VGroup(MathTex(e, font_size=40, color=DATA), MathTex(r"\mapsto", font_size=36, color=GREY_B),
                            MathTex(s, font_size=40, color=FUNC),
                            label(r"contains it" if ins else r"does not", font_size=24, color=YES if ins else NO)))
        for r in rows:
            r[0].move_to(LEFT * 5.2)
            r[1].move_to(LEFT * 4.4)
            r[2].move_to(LEFT * 3.0)
            r[3].move_to(LEFT * 0.8, aligned_edge=LEFT)
        for i, r in enumerate(rows):
            r.shift(UP * (1.2 - 0.75 * i))
        D = MathTex(r"D = \{x : x \notin f(x)\} = \{b, c\}", font_size=40, color=ADV).move_to(RIGHT * 3.6 + UP * 0.6)
        miss = label(r"$D \ne f(x)$ for every $x$: \\ they disagree about $x$ itself", font_size=28, color=NO).next_to(
            D, DOWN, buff=0.4)
        chain = MathTex(r"|\mathbb{N}| < |\mathcal{P}(\mathbb{N})| < |\mathcal{P}(\mathcal{P}(\mathbb{N}))| < \cdots",
                        font_size=40, color=INF).to_edge(DOWN, buff=1.0)
        cl = note(r"no largest infinity; \ the same diagonal proves the halting problem undecidable \ (Part 1, Part 25)",
                  font_size=22).next_to(chain, DOWN, buff=0.2)
        with self.voiceover(
            "Part 1's diagonal argument proves something more general. <bookmark mark='a'/> Take any set, and any way of "
            "assigning to each element a subset. Here, a goes to a and c; b to a alone; c to the empty set; d to "
            "everything. <bookmark mark='b'/> Collect the elements that are not in their own subset: b and c. Call it D. "
            "<bookmark mark='c'/> Could D be anyone's subset? If D were f of x, then x would be in D exactly when it is "
            "not. So no assignment hits every subset: the subsets of any set always outnumber its elements. "
            "<bookmark mark='d'/> Apply it again and again, and there is a tower of ever larger infinities, with no top. "
            "The same move, the diagonal, is what proved the halting problem undecidable, and Part 25 uses it once more "
            "to prove that some problems need more time than others."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r[:3])) for r in rows], lag_ratio=0.25))
            self.play(LaggedStart(*[FadeIn(r[3]) for r in rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(Write(D))
            vo.wait_until("c")
            self.play(FadeIn(miss))
            vo.wait_until("d")
            self.play(FadeIn(chain), FadeIn(cl))
        self.wait(0.3)
        self.clear_scene()
