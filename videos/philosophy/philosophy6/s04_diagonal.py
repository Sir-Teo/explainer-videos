from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


class Diagonal(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"The diagonal", r"Are some infinities larger than others?", lit=(1891,), part=PART)
        with self.voiceover("Chapter three. The diagonal."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.sweep()
        self.theorem()
        self.check()
        self.ladder()

    def sweep(self):
        d = load("diagonal")
        rows = d["rows"]
        n = len(rows)
        tab = bit_table(rows, cell=0.5, font_size=26).move_to([-3.0, 0.4, 0])
        names = VGroup(*[MathTex(rf"r_{{{i + 1}}}", font_size=26, color=GREY_B).next_to(tab.cell[i][0], LEFT,
                                                                                         buff=0.3) for i in range(n)])
        dots = VGroup(*[MathTex(r"\cdots", font_size=26, color=GREY_B).next_to(tab.cell[i][-1], RIGHT, buff=0.2)
                        for i in range(n)])
        hc = history_card(1891, r"Georg Cantor", r"`On an elementary question of the theory of manifolds'", width=6.4,
                          color=HIST).to_corner(UR, buff=0.3)
        rule = VGroup(MathTex(r"d(i) = 1 - r_i(i)", font_size=36, color=GOAL),
                      MathTex(r"d(i) \neq r_i(i) \ \Rightarrow\ d \neq r_i \quad \text{for every } i", font_size=32)).arrange(
            DOWN, buff=0.4).move_to([3.4, 0.0, 0])
        new = bit_table([d["diagonal"]], cell=0.5, font_size=26).next_to(tab, DOWN, buff=0.6)
        nl = MathTex(r"d", font_size=28, color=GOAL).next_to(new, LEFT, buff=0.3)
        marks = VGroup()
        for i in range(n):
            marks.add(SurroundingRectangle(tab.cell[i][i], buff=0.0, color=GOAL, stroke_width=3.5))
        cap = label(r"$d$ differs from $r_i$ in place $i$: \ it is in no row of the list", font_size=24,
                    color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Cantor's second proof, from 1891, is one of the most famous arguments in mathematics. "
            "<bookmark mark='a'/>Suppose someone claims to have listed every infinite sequence of zeros and ones: "
            "row one, row two, row three, and so on forever. <bookmark mark='b'/>Walk down the diagonal: the first "
            "digit of row one, the second of row two, the third of row three. <bookmark mark='c'/>Flip each one. "
            "<bookmark mark='d'/>The new sequence differs from row one in the first place, from row two in the "
            "second, from every row somewhere. So it is not in the list, and the list was not complete after all. "
            "No list of such sequences can be complete, and since each sequence is the binary expansion of a real "
            "number, the real numbers are uncountable."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(names), FadeIn(dots))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.25), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(nl), LaggedStart(*[FadeIn(new.cell[0][i], shift=DOWN * 0.3) for i in range(n)],
                                              lag_ratio=0.2), FadeIn(rule[0]), run_time=2.5)
            vo.wait_until("d")
            for i in range(n):
                self.play(Indicate(tab.cell[i][i], color=BAD), Indicate(new.cell[0][i], color=GOAL), run_time=0.45)
            self.play(FadeIn(rule[1]), FadeIn(cap))
        self.clear_scene()

    def theorem(self):
        thm = theorem_card(r"Cantor's theorem", r"for every set $X$, \ $|X| < |\mathcal{P}(X)|$: \ no function from $X$ "
                           r"onto its power set exists", width=9.0, font_size=26).to_edge(UP, buff=0.5)
        X = VGroup(*[VGroup(Dot(radius=0.08, color=SETC), MathTex(n, font_size=28)).arrange(RIGHT, buff=0.12)
                     for n in ("a", "b", "c")]).arrange(DOWN, buff=0.6).move_to([-5.2, -0.6, 0])
        imgs = [r"\{a, b\}", r"\{a\}", r"\varnothing"]
        F = VGroup(*[MathTex(t, font_size=30, color=SETC) for t in imgs]).arrange(DOWN, buff=0.6).move_to(
            [-2.6, -0.6, 0])
        arrows = VGroup(*[Arrow(x.get_right(), f.get_left(), buff=0.15, color=CONN, stroke_width=3) for x, f in
                          zip(X, F)])
        checks = VGroup(label(r"$a \in f(a)$", font_size=24, color=GREY_A), label(r"$b \notin f(b)$", font_size=24,
                                                                                  color=GOAL),
                        label(r"$c \notin f(c)$", font_size=24, color=GOAL))
        for c, f in zip(checks, F):
            c.next_to(f, RIGHT, buff=0.6)
        D = MathTex(r"D = \{x \in X : x \notin f(x)\} = \{b, c\}", font_size=34, color=GOAL).move_to([3.4, 0.6, 0])
        proof = VGroup(MathTex(r"\text{if } D = f(d):\quad d \in D \iff d \notin f(d) \iff d \notin D", font_size=30),
                       label(r"contradiction: \ $D$ is no one's image", font_size=26, color=BAD)).arrange(
            DOWN, buff=0.25).move_to([3.4, -1.0, 0])
        with self.voiceover(
            "The diagonal works for any set, not just the natural numbers. <bookmark mark='a'/>Cantor's theorem: "
            "every set has fewer members than it has subsets. <bookmark mark='b'/>Take any function f from a set X "
            "to its subsets: here, a goes to a and b, b goes to a, c to the empty set. <bookmark mark='c'/>Ask of "
            "each element whether it belongs to its own image. a does; b and c do not. <bookmark mark='d'/>Collect "
            "the ones that do not: the diagonal set D. <bookmark mark='e'/>D cannot be the image of anything. If D "
            "were f of d, then d would belong to D exactly when it does not. So f misses D, and no function from X "
            "covers all its subsets."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(X), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(F))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in checks], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(Write(D))
            vo.wait_until("e")
            self.play(FadeIn(proof))
        self.clear_scene()

    def check(self):
        d = load("cantor")
        head = label(r"The Reasoner tries every function", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        hd = [label(r"$|X|$", font_size=24, color=P.CLAIM), label(r"subsets", font_size=24, color=P.CLAIM),
              label(r"functions $X \to \mathcal{P}(X)$", font_size=24, color=P.CLAIM),
              label(r"that miss $D$", font_size=24, color=P.CLAIM)]
        rows = [[MathTex(str(c["n"]), font_size=30), MathTex(str(c["subsets"]), font_size=30),
                 MathTex(f"{c['functions']:,}".replace(",", "{,}"), font_size=30),
                 MathTex(r"\text{all}\ \checkmark", font_size=30, color=OK)] for c in d["checks"]]
        grid = ValueGrid(hd, rows, col_w=[1.4, 1.8, 3.6, 2.4], cell_h=0.7, font_size=28).move_to([0, 0.2, 0])
        f = MathTex(r"(2^n)^n \text{ functions}, \ \text{none onto}", font_size=34, color=GOAL).to_edge(DOWN, buff=0.8)
        assert all(c["all_miss"] for c in d["checks"])
        with self.voiceover(
            "A proof covers every set at once, but the Reasoner can check the small cases by brute force. "
            "<bookmark mark='a'/>For a set of n elements there are two to the n subsets, and two to the n, to the "
            "power n, functions from the set to its subsets. <bookmark mark='b'/>For n equal to four, that is "
            "sixty-five thousand, five hundred and thirty-six functions. For every one of them, the diagonal set is "
            "missed. No function is onto."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(grid.cell[r][c]) for r in range(len(rows)) for c in range(3)], FadeIn(f))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][3], scale=0.6) for r in range(len(rows))], lag_ratio=0.3))
        self.clear_scene()

    def ladder(self):
        steps = [r"\mathbb{N}", r"\mathcal{P}(\mathbb{N})", r"\mathcal{P}(\mathcal{P}(\mathbb{N}))",
                 r"\mathcal{P}(\mathcal{P}(\mathcal{P}(\mathbb{N})))", r"\cdots"]
        lad = VGroup()
        for i, s_ in enumerate(steps):
            m = MathTex(s_, font_size=38 - 2 * i, color=interpolate_color(ManimColor(SETC), ManimColor(CARD), i / 4))
            lad.add(m)
        lad.arrange(RIGHT, buff=0.9).move_to([0, 1.0, 0])
        lts = VGroup(*[MathTex(r"<", font_size=40, color=GREY_B).move_to((lad[i].get_right() + lad[i + 1].get_left()) / 2)
                       for i in range(len(lad) - 1)])
        cap = label(r"an endless ladder of ever larger infinities", font_size=30, color=GOAL).next_to(lad, DOWN,
                                                                                                buff=0.6)
        same = VGroup(label(r"the same diagonal returns:", font_size=26, color=GREY_A),
                      label(r"Russell's paradox \ (Chapter 5); \ the halting problem \ (Part 3); \ Gödel \ (Part 7)",
                            font_size=26)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Cantor's theorem never stops. <bookmark mark='a'/>The natural numbers are smaller than their power "
            "set, which has the size of the real numbers. That is smaller than its own power set, and so on, without "
            "end. <bookmark mark='b'/>There is no largest infinity. <bookmark mark='c'/>And the diagonal trick "
            "itself will keep returning: in Russell's paradox, in a moment; in the halting problem of Part 3; and in "
            "Gödel's theorems of Part 7."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(x) for x in lad], lag_ratio=0.4), FadeIn(lts), run_time=3)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(cap))
            vo.wait_until("c")
            self.play(FadeIn(same))
        self.clear_scene()
