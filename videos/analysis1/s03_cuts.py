from __future__ import annotations

from fractions import Fraction

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import SQRT2, Window, pin


def cut_split(c):
    """Split for the rational cut c*: True (upper set) where p/q >= c, exactly."""
    c = Fraction(c)

    def f(v, p, q):
        return np.array([Fraction(int(a), int(b)) >= c for a, b in zip(p, q)], bool)

    return f


def sqrt2_split(v, p, q):
    """Upper set of the sqrt 2 cut: p/q >= 0 and p^2 > 2 q^2."""
    return np.array([int(a) >= 0 and int(a) * int(a) > 2 * int(b) * int(b) for a, b in zip(p, q)], bool)


class Cuts(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.order()
        self.sup()
        self.arithmetic()
        self.cauchy()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"Filling the holes: Dedekind cuts", r"How do you build a number out of fractions?",
                            lit=(1872,), part=1)
        with self.voiceover(
            "Chapter two. How do you fill a hole, using nothing but the things around it? <bookmark mark='d'/> In 1872, "
            "Richard Dedekind had the idea: describe a number by the set of all the fractions below it."
        ) as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
            vo.wait_until("d")
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def definition(self):
        win = Window(1.0, 4.2, y=-2.3)
        self.win = win
        axis, labs = win.axis(), win.labels()
        half = win.dust(height=0.85, split=cut_split(Fraction(1, 2)), color=C.CUT_LOW, color_hi=C.CUT_HIGH,
                        nonneg=False)
        title = label(r"A \textbf{cut} is a set $\alpha \subset \Q$ such that", font_size=32).to_edge(UP, buff=0.45)
        conds = VGroup(
            label(r"(I) \ $\alpha$ is not empty, and $\alpha \neq \Q$;", font_size=30),
            label(r"(II) \ if $p \in \alpha$ and $q < p$, then $q \in \alpha$;", font_size=30),
            label(r"(III) \ $\alpha$ has no largest element.", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(title, DOWN, buff=0.3).align_to(title, LEFT).shift(RIGHT * 0.3)
        ref = note(r"Rudin, \textit{Principles}, appendix to chapter 1").next_to(conds, DOWN, buff=0.18).align_to(conds, LEFT)
        ex = MathTex(r"\big(\tfrac12\big)^{*} = \{\, q \in \Q : q < \tfrac12 \,\}", font_size=36, color=C.CUT_LOW)
        ex.move_to([3.2, 0.2, 0])
        with self.voiceover(
            "Here's his definition, as Rudin gives it. <bookmark mark='a'/> A cut is a set of fractions, call it alpha, "
            "with three properties. <bookmark mark='i'/> First, it isn't empty, and it isn't everything. "
            "<bookmark mark='j'/> Second, it's closed downward: if p is in alpha, so is every fraction smaller than p. "
            "<bookmark mark='k'/> Third, it has no largest element."
        ) as vo:
            self.play(Create(axis), FadeIn(labs), FadeIn(half))
            vo.wait_until("a")
            self.play(FadeIn(title))
            for mk, c in zip("ijk", conds):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=RIGHT * 0.2))
            self.play(FadeIn(ref))
        p_val = -0.2
        p_dot = pin(Dot(radius=0.08, color=C.CUT_LOW), win, p_val)
        down_arrow = always_redraw(lambda: Arrow(win.P(p_val, 1.75), [win.L - 0.1, win.y + 1.75, 0], buff=0,
                                                 color=C.CUT_LOW, stroke_width=4, max_tip_length_to_length_ratio=0.06))
        p_l = pin(MathTex(r"p", font_size=32, color=C.CUT_LOW), win, p_val, dy=2.1)
        with self.voiceover(
            "Picture it as a way of coloring the fractions: blue for the ones in the cut, orange for the rest. "
            "<bookmark mark='e'/> This one is the cut of one half: every fraction strictly below one half. "
            "<bookmark mark='d'/> Condition two says the blue part is a ray: once a fraction is blue, everything to its "
            "left is blue too."
        ) as vo:
            vo.wait_until("e")
            self.play(Write(ex))
            vo.wait_until("d")
            self.play(FadeIn(p_dot, scale=2), FadeIn(p_l), GrowArrow(down_arrow))
        self.wait(0.3)
        for m in (p_dot, p_l, down_arrow):
            m.clear_updaters()
        self.play(FadeOut(VGroup(p_dot, p_l, down_arrow)))
        hl = pin(Circle(radius=0.12, color=C.CUT_HIGH, stroke_width=3), win, 0.5)
        hl_l = pin(MathTex(r"\tfrac12 \notin \big(\tfrac12\big)^*", font_size=30, color=C.CUT_HIGH), win, 0.5, dy=-0.85)
        with self.voiceover(
            "Condition three is bookkeeping. <bookmark mark='z'/> Zoom in at one half. The fraction one half itself is "
            "orange, left out, and blue fractions crowd up to it from below with no last one. Without condition three, "
            "one half would have two cuts, with and without the endpoint; this way every fraction gets exactly one."
        ) as vo:
            vo.wait_until("z")
            self.play(FadeOut(VGroup(title, conds[0], conds[1], ref)), conds[2].animate.to_edge(UP, buff=0.5))
            self.play(*win.zoom_to(0.5, 0.06), run_time=2)
            self.play(FadeIn(hl, scale=2), FadeIn(hl_l))
        hl.clear_updaters()
        hl_l.clear_updaters()
        self.play(FadeOut(VGroup(hl, hl_l, ex)))
        self.play(*win.zoom_to(1.0, 4.2), run_time=1.5)

        root = win.dust(height=0.85, split=sqrt2_split, color=C.CUT_LOW, color_hi=C.CUT_HIGH, nonneg=False)
        ex2 = MathTex(r"\alpha = \{\, q \in \Q : q < 0 \ \text{ or } \ q^2 < 2 \,\}", font_size=40, color=C.CUT_LOW)
        ex2.next_to(conds[2], DOWN, buff=0.45)
        note3 = label(r"(III) holds: that is exactly Rudin 1.1 from chapter 1.", font_size=28, color=GREY_A)
        note3.next_to(ex2, DOWN, buff=0.3)
        with self.voiceover(
            "Now the interesting one. <bookmark mark='r'/> Color blue every fraction that's negative or squares to less "
            "than two. <bookmark mark='c'/> Is this a cut? It's clearly not empty, not everything, and closed "
            "downward. And it has no largest element: <bookmark mark='t'/> that's exactly the theorem from chapter one, "
            "the hop that always finds a bigger element. This cut sits precisely where the hole was. "
            "<bookmark mark='n'/> Dedekind's move is to declare that this set is a number."
        ) as vo:
            vo.wait_until("r")
            self.play(FadeOut(half), FadeIn(root), run_time=1.5)
            vo.wait_until("c")
            self.play(Write(ex2))
            vo.wait_until("t")
            self.play(FadeIn(note3))
            vo.wait_until("n")
            self.play(*win.zoom_to(SQRT2, 0.002), run_time=2.5)
        self.play(FadeOut(VGroup(conds[2], ex2, note3)))
        self.play(*win.zoom_to(1.0, 4.2), run_time=1.2)
        self.axis, self.labs, self.root = axis, labs, root
        half.clear_updaters()

    # ------------------------------------------------------------------
    def order(self):
        win = self.win
        defs = VGroup(
            MathTex(r"\R = \{\text{all cuts}\}", font_size=44),
            MathTex(r"\alpha < \beta \quad\text{means}\quad \alpha \subsetneq \beta", font_size=40),
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.45)

        def bar(c, y, color=C.CUT_LOW):
            g = VGroup(Line([win.L - 0.1, y, 0], [win.X(c), y, 0], color=color, stroke_width=8),
                       Circle(radius=0.08, color=color, stroke_width=3).set_fill(BACKGROUND, 1).move_to([win.X(c), y, 0]))
            return g

        b1 = bar(0.5, -0.5)
        b2 = bar(SQRT2, -1.0)
        l1 = MathTex(r"\big(\tfrac12\big)^*", font_size=30, color=C.CUT_LOW).next_to(b1, RIGHT, buff=0.2)
        l2 = MathTex(r"\alpha_{\sqrt2}", font_size=30, color=C.CUT_LOW).next_to(b2, RIGHT, buff=0.2)
        with self.voiceover(
            "So: <bookmark mark='r'/> a real number is a cut, and the real line is the set of all cuts. "
            "<bookmark mark='o'/> To compare two of them, compare the sets: alpha is less than beta when alpha is a "
            "proper subset of beta. <bookmark mark='b'/> Drawn as blue rays, the cut of one half sits inside the cut of "
            "root two, so one half is smaller."
        ) as vo:
            vo.wait_until("r")
            self.play(Write(defs[0]))
            vo.wait_until("o")
            self.play(Write(defs[1]))
            vo.wait_until("b")
            self.play(Create(b1[0]), FadeIn(b1[1]), FadeIn(l1))
            self.play(Create(b2[0]), FadeIn(b2[1]), FadeIn(l2))
        rows = [
            MathTex(r"p \in \alpha,\; p \notin \beta", font_size=34),
            MathTex(r"q \in \beta \;\Rightarrow\; q < p", font_size=34),
            MathTex(r"q \in \beta \;\Rightarrow\; q \in \alpha", font_size=34),
        ]
        whys = [why(r"suppose $\alpha \not\subset \beta$"), why(r"if $q \ge p$, (II) would put $p$ in $\beta$"),
                why(r"by (II) for $\alpha$; so $\beta \subset \alpha$")]
        grp = VGroup(*rows)
        step = ladder(self, rows, whys, keep=3, top=1.4, buff=0.25, x=-2.4, align_index=None)
        with self.voiceover(
            "For this to be an order, any two cuts must be comparable: one must contain the other. The proof takes "
            "three lines. <bookmark mark='a'/> Suppose alpha is not inside beta, so some p is in alpha but not in beta. "
            "<bookmark mark='b'/> Then every q in beta is less than p, because if q were at least p, condition two "
            "would put p in beta. <bookmark mark='c'/> And then, by condition two for alpha, every q in beta is in "
            "alpha: beta is inside alpha."
        ) as vo:
            self.play(FadeOut(VGroup(b1, b2, l1, l2)))
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                step(i, run_time=0.9)
        self.wait(0.3)
        self.play(FadeOut(VGroup(grp, *whys)), FadeOut(defs[1]), defs[0].animate.to_corner(UL, buff=0.45))
        self.defs0 = defs[0]

    # ------------------------------------------------------------------
    def sup(self):
        win = self.win
        vals = [Fraction(1), Fraction(14, 10), Fraction(141, 100), Fraction(1414, 1000), Fraction(14142, 10000)]
        ys = [1.4, 0.95, 0.5, 0.05, -0.4]

        def bar(c, y, color=C.CUT_LOW, sw=8):
            return VGroup(Line([win.L - 0.1, y, 0], [win.X(float(c)), y, 0], color=color, stroke_width=sw),
                          Circle(radius=0.08, color=color, stroke_width=3).set_fill(BACKGROUND, 1)
                          .move_to([win.X(float(c)), y, 0]))

        self.play(*win.zoom_to(1.0, 1.4), run_time=1.0)
        bars = VGroup(*[bar(v, y) for v, y in zip(vals, ys)])
        labs = VGroup(*[MathTex(rf"{float(v):g}^*", font_size=28, color=C.CUT_LOW).next_to(b, RIGHT, buff=0.15)
                        for v, b in zip(vals, bars)])
        A_l = MathTex(r"\mathcal{A} = \{\, 1^*,\ 1.4^*,\ 1.41^*,\ 1.414^*,\ \ldots \}", font_size=36).to_edge(UP, buff=0.45)
        A_l.shift(RIGHT * 1.0)
        with self.voiceover(
            "Now the payoff: the least-upper-bound property. <bookmark mark='a'/> Take any collection of cuts that is "
            "bounded above, like the cuts of one, one point four, one point four one, and so on. Each one is a blue ray, "
            "and each contains the one before."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A_l))
            self.play(LaggedStart(*[AnimationGroup(Create(b[0]), FadeIn(b[1]), FadeIn(l)) for b, l in zip(bars, labs)],
                                  lag_ratio=0.35), run_time=3)
        union = bar(SQRT2, -1.05, color=C.EPS, sw=10)
        union_l = MathTex(r"\gamma = \bigcup_{\alpha \in \mathcal{A}} \alpha", font_size=34, color=C.EPS)
        union_l.next_to(union, RIGHT, buff=0.2)
        with self.voiceover(
            "Dedekind's answer for the supremum is almost embarrassingly simple: <bookmark mark='u'/> take the union of "
            "all of them. Every fraction that is in at least one of the cuts. <bookmark mark='r'/> Here, that union is "
            "every fraction that is negative or squares to less than two: the cut of root two. The hole has been "
            "filled by the union of the cuts approaching it."
        ) as vo:
            vo.wait_until("u")
            self.play(TransformFromCopy(bars, VGroup(union)), FadeIn(union_l), run_time=1.6)
            vo.wait_until("r")
            self.play(Indicate(union_l, color=C.EPS))
        self.wait(0.3)
        self.play(FadeOut(VGroup(bars, labs, union, union_l, A_l)))

        rows = [
            label(r"$\gamma \ne \emptyset$; \ $\gamma \subset \beta$, so $\gamma \ne \Q$", font_size=30),
            label(r"$p \in \gamma,\ q < p$: \ $p$ is in some $\alpha$, so $q \in \alpha \subset \gamma$", font_size=30),
            label(r"$p \in \gamma$: \ $p \in$ some $\alpha$, which has $r > p$; \ $r \in \gamma$", font_size=30),
            label(r"every $\alpha \subset \gamma$: \ $\gamma$ is an upper bound", font_size=30),
            label(r"$\delta < \gamma$: some $p \in \gamma \setminus \delta$, \ $p \in$ some $\alpha \not\subset \delta$",
                  font_size=30),
        ]
        tags = [r"(I)", r"(II)", r"(III)", r"upper bound", r"least"]
        tag_m = [label(t, font_size=28, color=C.EPS) for t in tags]
        lines = VGroup(*[VGroup(t, r).arrange(RIGHT, buff=0.35) for t, r in zip(tag_m, rows)])
        for ln in lines:
            ln[1].shift(RIGHT * (2.3 - ln[0].width - 0.35))
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.8).shift(DOWN * 0.4)
        head = label(r"Claim: for $\mathcal{A}$ nonempty and bounded above by a cut $\beta$, \ "
                     r"$\gamma = \bigcup \mathcal{A}$ is a cut, and $\gamma = \sup \mathcal{A}$.", font_size=30)
        head.to_edge(UP, buff=0.5)
        self.play(*win.zoom_to(1.0, 4.2), FadeOut(self.root), FadeOut(self.axis), FadeOut(self.labs),
                  FadeOut(self.defs0), run_time=1)
        with self.voiceover(
            "In general, let script A be any nonempty set of cuts, bounded above by some cut beta, and let gamma be "
            "their union. <bookmark mark='a'/> Gamma isn't empty, and it sits inside beta, so it isn't everything. "
            "<bookmark mark='b'/> It's closed downward, because each of the cuts is. <bookmark mark='c'/> It has no "
            "largest element, because any p in gamma lies in some cut, which has something bigger. So gamma is a cut."
        ) as vo:
            self.play(FadeIn(head))
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(lines[i], shift=RIGHT * 0.2))
        with self.voiceover(
            "<bookmark mark='u'/> It contains every cut in the collection, so it's an upper bound. <bookmark mark='l'/> "
            "And it's the least one: if delta is smaller than gamma, some p in gamma is missing from delta, and that p "
            "came from a cut alpha, which therefore isn't inside delta. So delta is not an upper bound. "
            "<bookmark mark='q'/> The whole difficulty of the real numbers dissolves into one line of set theory: the "
            "supremum is the union."
        ) as vo:
            vo.wait_until("u")
            self.play(FadeIn(lines[3], shift=RIGHT * 0.2))
            vo.wait_until("l")
            self.play(FadeIn(lines[4], shift=RIGHT * 0.2))
            vo.wait_until("q")
            box = MathTex(r"\sup \mathcal{A} = \bigcup_{\alpha \in \mathcal{A}} \alpha", font_size=46, color=C.EPS)
            box = boxed(box, color=C.EPS).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.4)
            self.play(FadeIn(box, scale=1.1))
        self.wait(0.5)
        for m in (self.axis, self.labs, self.root):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def arithmetic(self):
        rows = VGroup(
            MathTex(r"\alpha + \beta = \{\, r + s : r \in \alpha,\ s \in \beta \,\}", font_size=40),
            MathTex(r"0^* = \{\, q \in \Q : q < 0 \,\}", font_size=40),
            MathTex(r"\alpha\beta = \{\, p : p \le rs,\ r \in \alpha,\ s \in \beta,\ r, s > 0 \,\}"
                    r"\quad (\alpha, \beta > 0^*)", font_size=36),
        ).arrange(DOWN, buff=0.45).to_edge(UP, buff=0.7)
        rows[2].set_color(GREY_A)
        emb = VGroup(
            MathTex(r"r \;\longmapsto\; r^* = \{\, q \in \Q : q < r \,\}", font_size=40),
            MathTex(r"(r + s)^* = r^* + s^*,\quad (rs)^* = r^* s^*,\quad r < s \iff r^* < s^*", font_size=34),
        ).arrange(DOWN, buff=0.3).next_to(rows, DOWN, buff=0.6)
        with self.voiceover(
            "Then comes arithmetic, and it's mostly routine. <bookmark mark='a'/> To add two cuts, add their elements in "
            "every possible way. <bookmark mark='z'/> Zero is the cut of the negative fractions, and you can check that "
            "adding it changes nothing. <bookmark mark='m'/> Multiplication is defined first for positive cuts, then "
            "extended by cases of sign. Rudin checks the field rules one by one; it's tedious and teaches nothing "
            "new, so we'll trust it. <bookmark mark='e'/> And the rationals sit inside, each fraction r becoming "
            "the cut of fractions below it, in a way that respects sums, products and order."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("z")
            self.play(Write(rows[1]))
            vo.wait_until("m")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(Write(emb[0]))
            self.play(FadeIn(emb[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cauchy(self):
        thm = VGroup(
            label(r"\textbf{Theorem} (Rudin 1.19) \ There is an ordered field $\R$ with the least-upper-bound property", font_size=28),
            label(r"that contains $\Q$; \ it is unique: any two such fields are isomorphic.", font_size=28),
        ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.5)
        h_ = [Fraction(1), Fraction(4, 3), Fraction(7, 5), Fraction(24, 17), Fraction(41, 29), Fraction(140, 99)]
        d_ = [Fraction(1), Fraction(14, 10), Fraction(141, 100), Fraction(1414, 1000), Fraction(14142, 10000),
              Fraction(141421, 100000)]
        a_row = MathTex(*[rf"{float(v):.5f}".rstrip("0").rstrip(".") + "," for v in d_], r"\ldots", font_size=32, color=C.SEQ)
        b_row = MathTex(*[(rf"\tfrac{{{v.numerator}}}{{{v.denominator}}}" if v.denominator > 1 else "1") + "," for v in h_],
                        r"\ldots", font_size=34, color=C.APPROX)
        diff = [abs(float(a - b)) for a, b in zip(d_, h_)]
        d_row = MathTex(*[f"{x:.5f}," for x in diff], r"\ldots \to 0", font_size=32, color=C.EPS)
        lab = VGroup(label(r"decimals", font_size=26, color=C.SEQ), label(r"hops", font_size=26, color=C.APPROX),
                     label(r"difference", font_size=26, color=C.EPS))
        grid = VGroup(*[VGroup(l, r).arrange(RIGHT, buff=0.5) for l, r in zip(lab, (a_row, b_row, d_row))])
        for g in grid:
            g[1].align_to(a_row, LEFT)
        grid.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.3)
        for g in grid:
            g[1].shift(RIGHT * (2.2 - g[0].width))
        assert diff[-1] < 1e-4
        who = label(r"Cantor and M\'eray, also 1872: \ a real number is a Cauchy sequence of fractions,", font_size=28)
        who2 = label(r"two sequences counting as the same number when their difference tends to $0$.", font_size=28,
                     color=GREY_A)
        txt = VGroup(who, who2).arrange(DOWN, buff=0.12).next_to(grid, DOWN, buff=0.6)
        with self.voiceover(
            "That's Rudin's theorem: <bookmark mark='t'/> there is an ordered field with the least-upper-bound property, "
            "containing the rationals, and it's unique: any two such fields are the same up to renaming. "
            "<bookmark mark='c'/> There's a second classic construction, by Cantor and Méray, in the same year. A real "
            "number is a sequence of fractions that bunches up, a Cauchy sequence, <bookmark mark='d'/> with two "
            "sequences counting as the same number when their difference goes to zero, like the decimals and the hops "
            "for root two."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm))
            vo.wait_until("c")
            self.play(FadeIn(grid[0]), FadeIn(grid[1]), FadeIn(who))
            vo.wait_until("d")
            self.play(FadeIn(grid[2]), FadeIn(who2))
        reuse = label(r"Whenever a space has holes, we will fill them with its own Cauchy sequences.", font_size=30,
                      color=C.EPS).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "That second construction is the one this series will reuse. <bookmark mark='r'/> Whenever a space has holes, "
            "and the spaces of functions we meet later will, we fill them with the space's own Cauchy sequences. "
            "From here on, though, we can forget how the reals were built. Everything we need follows from one fact: "
            "every set that is bounded above has a least upper bound."
        ) as vo:
            vo.wait_until("r")
            self.play(FadeIn(reuse, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()
