from __future__ import annotations

from fractions import Fraction

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import SQRT2, Window, endpoint, pin


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
        # the window does not move here: a dot p, a dashed riser from it, and the arrow "everything to the left"
        ad = 1.15  # just above the ticks (dust height 0.85)
        p_dot = Dot(win.P(p_val), radius=0.08, color=C.CUT_LOW)
        riser = DashedLine(win.P(p_val, 0.12), win.P(p_val, ad), color=GREY_B, stroke_width=2)
        down_arrow = Arrow(win.P(p_val, ad), [win.L - 0.1, win.y + ad, 0], buff=0, color=C.CUT_LOW, stroke_width=4,
                           max_tip_length_to_length_ratio=0.06)
        p_l = MathTex(r"p", font_size=32, color=C.CUT_LOW).next_to(win.P(p_val, ad), UP, buff=0.12)
        with self.voiceover(
            "Picture it as a way of coloring the fractions: blue for the ones in the cut, orange for the rest. "
            "<bookmark mark='e'/> This one is the cut of one half: every fraction strictly below one half. "
            "<bookmark mark='d'/> Condition two says the blue part runs all the way to the left: once a fraction is "
            "blue, everything to its left is blue too."
        ) as vo:
            vo.wait_until("e")
            self.play(Write(ex))
            vo.wait_until("d")
            self.play(FadeIn(p_dot, scale=2), FadeIn(p_l), Create(riser))
            self.play(GrowArrow(down_arrow))
        self.wait(0.3)
        self.play(FadeOut(VGroup(p_dot, p_l, riser, down_arrow)))
        hl = pin(endpoint(ORIGIN, False, C.CUT_HIGH, radius=0.12), win, 0.5)  # hollow: 1/2 is left out
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
            seam = endpoint(win.P(SQRT2), False, C.HOLE, radius=0.12)
            seam_l = MathTex(r"\sqrt2", font_size=32, color=C.HOLE).move_to(win.P(SQRT2, -0.85))
            self.play(FadeIn(seam, scale=2), FadeIn(seam_l))
        self.play(FadeOut(VGroup(conds[2], ex2, note3, seam, seam_l)))
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
        step = ladder(self, rows, whys, keep=3, top=1.95, buff=0.2, x=-2.4, align_index=None)
        # the proof on the two rays: alpha = the cut of root 2 (lower ray), beta = the cut of 1/2 (upper ray)
        la = MathTex(r"\alpha = \alpha_{\sqrt2}", font_size=30, color=C.CUT_LOW).next_to(b2, RIGHT, buff=0.2)
        lb = MathTex(r"\beta = \big(\tfrac12\big)^*", font_size=30, color=C.CUT_LOW).next_to(b1, RIGHT, buff=0.2)
        pv, qv = 1.0, 0.1
        assert 0.5 < pv < SQRT2 and qv < 0.5  # p is in alpha but not in beta; q is in beta
        pd = Dot([win.X(pv), -1.0, 0], radius=0.08, color=WHITE)
        p_l = MathTex(r"p", font_size=30).next_to(pd, DOWN, buff=0.15)
        p_up = DashedLine([win.X(pv), -0.88, 0], [win.X(pv), -0.15, 0], color=GREY_B, stroke_width=2)
        qd = Dot([win.X(qv), -0.5, 0], radius=0.08, color=WHITE)
        q_l = MathTex(r"q", font_size=30).next_to(qd, UP, buff=0.12)
        q_ar = Arrow([win.X(qv), -0.75, 0], [win.X(pv) - 0.05, -0.75, 0], buff=0, color=GREY_B, stroke_width=3,
                     max_tip_length_to_length_ratio=0.08)  # q lies left of p
        inside = Line([win.L - 0.1, -1.0, 0], [win.X(0.5), -1.0, 0], color=C.EPS, stroke_width=8)
        with self.voiceover(
            "For this to be an order, any two cuts must be comparable: one must contain the other. The proof takes "
            "three lines. <bookmark mark='a'/> Suppose alpha is not inside beta, so some p is in alpha but not in beta. "
            "<bookmark mark='b'/> Then every q in beta is less than p, because if q were at least p, condition two "
            "would put p in beta. <bookmark mark='c'/> And then, by condition two for alpha, every q in beta is in "
            "alpha: beta is inside alpha."
        ) as vo:
            self.play(FadeTransform(l1, lb), FadeTransform(l2, la))
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                step(i, run_time=0.9)
                if mk == "a":
                    self.play(FadeIn(pd, scale=2), FadeIn(p_l), Create(p_up))
                elif mk == "b":
                    self.play(FadeIn(qd, scale=2), FadeIn(q_l), GrowArrow(q_ar))
                else:
                    self.play(TransformFromCopy(b1[0], inside), run_time=1.0)
        self.wait(0.3)
        self.play(FadeOut(VGroup(grp, *whys, b1, b2, la, lb, pd, p_l, p_up, qd, q_l, q_ar, inside)),
                  FadeOut(defs[1]), defs[0].animate.to_corner(UL, buff=0.45))
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
            label(r"$\gamma \ne \emptyset$; \ $\gamma \subset \beta$, so $\gamma \ne \Q$", font_size=26),
            label(r"$p \in \gamma,\ q < p$: \ $p$ is in some $\alpha$, so $q \in \alpha \subset \gamma$", font_size=26),
            label(r"$p \in \gamma$: \ $p \in$ some $\alpha$, which has $r > p$; \ $r \in \gamma$", font_size=26),
            label(r"every $\alpha \subset \gamma$: \ $\gamma$ is an upper bound", font_size=26),
            label(r"$\delta < \gamma$: some $p \in \gamma \setminus \delta$, \ $p \in$ some $\alpha \not\subset \delta$",
                  font_size=26),
        ]
        tags = [r"(I)", r"(II)", r"(III)", r"upper bound", r"least"]
        tag_m = [label(t, font_size=26, color=C.EPS) for t in tags]
        lines = VGroup(*[VGroup(t, r).arrange(RIGHT, buff=0.35) for t, r in zip(tag_m, rows)])
        for ln in lines:
            ln[1].shift(RIGHT * (2.0 - ln[0].width - 0.35))
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.6).set_y(-0.1)
        # the proof, drawn: cuts as rays on the right (values 0.9 .. 1.8), filling the right half
        X = lambda v: 2.2 + (float(v) - 0.9) * 4.3 / 0.9  # noqa: E731
        x0 = 1.9  # the rays come in from the left (toward minus infinity)

        def ray(v, y, color, sw=6):
            return VGroup(Line([x0, y, 0], [X(v), y, 0], color=color, stroke_width=sw),
                          Circle(radius=0.07, color=color, stroke_width=2.5).set_fill(BACKGROUND, 1).move_to([X(v), y, 0]))

        a_vals, a_ys = (1.0, 1.4, 1.41), (2.2, 1.8, 1.4)
        r_al = VGroup(*[ray(v, y, C.CUT_LOW) for v, y in zip(a_vals, a_ys)])
        r_al_l = MathTex(r"\alpha \in \mathcal{A}", font_size=28, color=C.CUT_LOW).next_to([X(1.0), 2.2, 0], RIGHT,
                                                                                         buff=0.2)
        y_ga, y_de, y_be, y_nl = 0.75, 0.2, -0.35, -1.0
        r_ga = ray(SQRT2, y_ga, C.EPS, sw=8)
        r_ga_l = MathTex(r"\gamma", font_size=32, color=C.EPS).next_to(r_ga, RIGHT, buff=0.12)
        r_be = ray(1.7, y_be, GREY_A)
        r_be_l = MathTex(r"\beta", font_size=32, color=GREY_A).next_to(r_be, RIGHT, buff=0.12)
        nl = VGroup(Line([x0, y_nl, 0], [6.85, y_nl, 0], color=GREY_C, stroke_width=2),
                    *[VGroup(Line([X(v), y_nl - 0.07, 0], [X(v), y_nl + 0.07, 0], color=GREY_C, stroke_width=2),
                             MathTex(f"{v:g}", font_size=22, color=GREY_B).next_to([X(v), y_nl - 0.07, 0], DOWN, buff=0.1))
                      for v in (1.0, 1.5)])
        fade = Rectangle(width=0.5, height=3.4, stroke_width=0, fill_color=BACKGROUND, fill_opacity=1.0).move_to(
            [x0 - 0.1, (a_ys[0] + y_be) / 2, 0])  # the rays run off to the left, toward minus infinity
        pq = VGroup(Dot([X(1.2), y_ga, 0], radius=0.07, color=WHITE),
                    MathTex(r"p", font_size=26).next_to([X(1.2), y_ga, 0], UP, buff=0.12),
                    Arrow([X(1.2), y_ga - 0.25, 0], [X(1.02), y_ga - 0.25, 0], buff=0, color=C.CUT_LOW, stroke_width=3,
                          tip_length=0.12),
                    MathTex(r"q", font_size=26, color=C.CUT_LOW).next_to([X(1.0), y_ga - 0.25, 0], LEFT, buff=0.06))
        pr = VGroup(Dot([X(1.2), a_ys[2], 0], radius=0.07, color=WHITE),
                    Arrow([X(1.2), a_ys[2] + 0.2, 0], [X(1.33), a_ys[2] + 0.2, 0], buff=0, color=C.EPS, stroke_width=3,
                          tip_length=0.12),
                    MathTex(r"r", font_size=26, color=C.EPS).next_to([X(1.35), a_ys[2] + 0.2, 0], RIGHT, buff=0.06))
        de_v, p_v = 1.36, 1.375
        r_de = ray(de_v, y_de, C.PATHOLOGY)
        r_de_l = MathTex(r"\delta", font_size=30, color=C.PATHOLOGY).next_to([X(de_v), y_de, 0], RIGHT, buff=0.18)
        pl_ = VGroup(Dot([X(p_v), y_ga, 0], radius=0.07, color=WHITE),
                     MathTex(r"p", font_size=26).next_to([X(p_v), y_ga, 0], UP, buff=0.12))
        assert de_v < p_v < 1.41 < SQRT2 < 1.7  # p is in gamma (via the cut of 1.41) but not in delta
        assert lines.get_right()[0] < fade.get_left()[0]
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
            self.play(FadeIn(head), Create(nl), FadeIn(r_al), FadeIn(r_al_l), FadeIn(fade))
            self.play(TransformFromCopy(r_al, VGroup(r_ga)), FadeIn(r_ga_l), FadeIn(fade))
            extra = [lambda: (Create(r_be), FadeIn(r_be_l), FadeIn(fade)),
                     lambda: (FadeIn(pq),),
                     lambda: (FadeIn(pr),)]
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(lines[i], shift=RIGHT * 0.2), *extra[i]())
        with self.voiceover(
            "<bookmark mark='u'/> It contains every cut in the collection, so it's an upper bound. <bookmark mark='l'/> "
            "And it's the least one: if delta is smaller than gamma, some p in gamma is missing from delta, and that p "
            "came from a cut alpha, which therefore isn't inside delta. So delta is not an upper bound. "
            "<bookmark mark='q'/> The whole difficulty of the real numbers dissolves into one line of set theory: the "
            "supremum is the union."
        ) as vo:
            vo.wait_until("u")
            self.play(FadeIn(lines[3], shift=RIGHT * 0.2), FadeOut(pq), FadeOut(pr))
            self.play(*[Indicate(r_[0], color=C.CUT_LOW, scale_factor=1.0) for r_ in r_al], run_time=1.0)
            vo.wait_until("l")
            self.play(FadeIn(lines[4], shift=RIGHT * 0.2), Create(r_de), FadeIn(r_de_l), FadeIn(fade))
            self.play(FadeIn(pl_), Indicate(r_al[2][0], color=C.CUT_LOW, scale_factor=1.0))
            vo.wait_until("q")
            box = MathTex(r"\sup \mathcal{A} = \bigcup_{\alpha \in \mathcal{A}} \alpha", font_size=42, color=C.EPS)
            box = boxed(box, color=C.EPS).move_to([4.4, -2.55, 0])
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
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.7)
        rows[2].set_color(GREY_A)
        emb = VGroup(
            MathTex(r"r \;\longmapsto\; r^* = \{\, q \in \Q : q < r \,\}", font_size=40),
            MathTex(r"(r + s)^* = r^* + s^*,\quad (rs)^* = r^* s^*,\quad r < s \iff r^* < s^*", font_size=34),
        ).arrange(DOWN, buff=0.3).next_to(rows, DOWN, buff=0.6)
        rows.to_edge(UP, buff=0.4)
        emb.next_to(rows, DOWN, buff=0.4)
        Xa = lambda v: -0.4 + float(v) * 2.4  # noqa: E731

        def aray(v, y, color, sw=6):
            return VGroup(Line([-6.6, y, 0], [Xa(v), y, 0], color=color, stroke_width=sw),
                          Circle(radius=0.07, color=color, stroke_width=3).set_fill(BACKGROUND, 1).move_to([Xa(v), y, 0]))

        a_, b_ = SQRT2, 0.5
        ys_ = (-0.95, -1.3, -1.65, -2.1)  # the rays fill the middle band, the axis under them
        rays = VGroup(aray(a_, ys_[0], C.CUT_LOW), aray(b_, ys_[1], C.DELTA), aray(a_ + b_, ys_[2], C.EPS, sw=7),
                      aray(0, ys_[3], GREY_B))
        rlabs = VGroup(MathTex(r"\alpha = (\sqrt2)^*", font_size=26, color=C.CUT_LOW),
                       MathTex(r"\beta = (\tfrac12)^*", font_size=26, color=C.DELTA),
                       MathTex(r"\alpha + \beta", font_size=26, color=C.EPS),
                       MathTex(r"0^*", font_size=26, color=GREY_B))
        for l_, r_ in zip(rlabs, rays):
            l_.next_to(r_, RIGHT, buff=0.15)
        ya = -2.55
        axis_ = VGroup(Line([-6.6, ya, 0], [6.6, ya, 0], color=GREY_C, stroke_width=2),
                       *[VGroup(Line([Xa(v), ya - 0.07, 0], [Xa(v), ya + 0.07, 0], color=GREY_C, stroke_width=2),
                                MathTex(f"{v}", font_size=22, color=GREY_B).next_to([Xa(v), ya - 0.07, 0], DOWN, buff=0.1))
                         for v in (-2, -1, 0, 1, 2)])
        r_, s_ = 1.1, 0.3
        assert r_ < a_ and s_ < b_
        sample = VGroup(Dot([Xa(r_), ys_[0], 0], radius=0.06, color=WHITE), Dot([Xa(s_), ys_[1], 0], radius=0.06, color=WHITE),
                        Dot([Xa(r_ + s_), ys_[2], 0], radius=0.07, color=WHITE),
                        MathTex(r"r", font_size=24).next_to([Xa(r_), ys_[0], 0], UP, buff=0.08),
                        MathTex(r"s", font_size=24).next_to([Xa(s_), ys_[1], 0], UP, buff=0.08),
                        MathTex(r"r + s", font_size=24).next_to([Xa(r_ + s_), ys_[2], 0], DOWN, buff=0.08))
        with self.voiceover(
            "Then comes arithmetic, and it's mostly routine. <bookmark mark='a'/> To add two cuts, add their elements in "
            "every possible way. <bookmark mark='z'/> Zero is the cut of the negative fractions, and you can check that "
            "adding it changes nothing. <bookmark mark='m'/> Multiplication is defined first for positive cuts, then "
            "extended by cases of sign. Rudin checks the field rules one by one; it's tedious and teaches nothing "
            "new, so we'll trust it. <bookmark mark='e'/> And the rationals sit inside, each fraction r becoming "
            "the cut of fractions below it, in a way that respects sums, products and order."
        ) as vo:
            self.play(Write(rows[0]), Create(axis_), FadeIn(rays[:2]), FadeIn(rlabs[:2]))
            self.play(FadeIn(sample[:2]), FadeIn(sample[3:5]))
            self.play(Create(rays[2]), FadeIn(rlabs[2]), TransformFromCopy(sample[:2], sample[2]), FadeIn(sample[5]))
            vo.wait_until("z")
            self.play(Write(rows[1]), Create(rays[3]), FadeIn(rlabs[3]))
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
            label(r"\textbf{Theorem} (Rudin 1.19)", font_size=28, color=GREY_A),
            label(r"There is an ordered field $\R$ with the least-upper-bound property that contains $\Q$.",
                  font_size=28),
            label(r"(And it is unique: any two such fields are isomorphic.)", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.4)
        h_ = [Fraction(1), Fraction(4, 3), Fraction(7, 5), Fraction(24, 17), Fraction(41, 29), Fraction(140, 99)]
        d_ = [Fraction(1), Fraction(14, 10), Fraction(141, 100), Fraction(1414, 1000), Fraction(14142, 10000),
              Fraction(141421, 100000)]
        diff = [abs(float(a - b)) for a, b in zip(d_, h_)]
        assert diff[-1] < 1e-4 and all(abs(float(v) - SQRT2) < 0.5 for v in d_ + h_)

        def dec_s(v):
            return f"{float(v):.5f}".rstrip("0").rstrip(".")

        def frac_s(v):
            return rf"\tfrac{{{v.numerator}}}{{{v.denominator}}}" if v.denominator > 1 else "1"

        def diff_s(x):
            return "0" if x == 0 else f"{x:.4f}"

        # both sequences on one line, closing in on the same spot
        X = lambda v: -4.3 + (float(v) - 0.95) / 0.55 * 10.4  # noqa: E731
        yl = 1.2
        nl = VGroup(Line([X(0.95), yl, 0], [X(1.5), yl, 0], color=GREY_C, stroke_width=2))
        for v in (1.0, 1.1, 1.2, 1.3, 1.4, 1.5):
            nl.add(Line([X(v), yl - 0.06, 0], [X(v), yl + 0.06, 0], color=GREY_C, stroke_width=2),
                   MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to([X(v), yl - 0.06, 0], DOWN, buff=0.32))
        ring = endpoint([X(SQRT2), yl, 0], False, C.HOLE, radius=0.1)
        ring_l = MathTex(r"\sqrt2", font_size=26, color=C.HOLE).next_to(ring, UP, buff=0.45)
        dots_d = VGroup(*[Dot([X(v), yl + 0.22, 0], radius=0.06, color=C.SEQ) for v in d_])
        dots_h = VGroup(*[Dot([X(v), yl - 0.22, 0], radius=0.06, color=C.APPROX) for v in h_])
        names = VGroup(label(r"decimals", font_size=24, color=C.SEQ).next_to([X(0.95), yl + 0.22, 0], LEFT, buff=0.3),
                       label(r"hops", font_size=24, color=C.APPROX).next_to([X(0.95), yl - 0.22, 0], LEFT, buff=0.3))
        joins = VGroup(*[Line(dd.get_center(), hd.get_center(), color=C.EPS, stroke_width=3)
                         for dd, hd in zip(dots_d, dots_h)])
        # the numbers, on a real grid (one MathTex part per entry)
        tab = VGroup(
            MathTex(r"\text{decimals}", *[dec_s(v) + "," for v in d_], r"\ldots", font_size=30, color=C.SEQ),
            MathTex(r"\text{hops}", *[frac_s(v) + "," for v in h_], r"\ldots", font_size=30, color=C.APPROX),
            MathTex(r"\text{difference}", *[diff_s(x) + "," for x in diff], r"\ldots \to 0", font_size=30, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([0, -0.55, 0])
        regrid(tab, gap=0.35, center=True, max_width=12.6)
        who = label(r"M\'eray (1869) and Cantor (1872): \ a real number is a Cauchy sequence of fractions,", font_size=28)
        who2 = label(r"two sequences counting as the same number when their difference tends to $0$.", font_size=28,
                     color=GREY_A)
        txt = VGroup(who, who2).arrange(DOWN, buff=0.12).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "That's Rudin's theorem: <bookmark mark='t'/> there is an ordered field with the least-upper-bound property, "
            "containing the rationals. And, as Rudin remarks, it's unique: any two such fields are the same up to "
            "renaming. "
            "<bookmark mark='c'/> There's a second classic construction, by Méray and Cantor, from the same years. A real "
            "number is a sequence of fractions that bunches up, a Cauchy sequence, <bookmark mark='d'/> with two "
            "sequences counting as the same number when their difference goes to zero, like the decimals and the hops "
            "for root two."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("c")
            self.play(Create(nl), FadeIn(ring), FadeIn(ring_l), FadeIn(names), FadeIn(who))
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots_d], lag_ratio=0.25),
                      LaggedStart(*[FadeIn(h, scale=2) for h in dots_h], lag_ratio=0.25),
                      FadeIn(tab[0]), FadeIn(tab[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(j) for j in joins], lag_ratio=0.2), FadeIn(tab[2]), FadeIn(who2),
                      run_time=1.6)
        reuse = label(r"Whenever a space has holes, we will fill them with its own Cauchy sequences.", font_size=30,
                      color=C.EPS).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "That second construction is the one this series will reuse. <bookmark mark='r'/> Whenever a space has holes, "
            "and the spaces of functions we meet later will, we fill them with the space's own Cauchy sequences. "
            "From here on, though, we can forget how the reals were built. Everything we need follows from one fact: "
            "every nonempty set that is bounded above has a least upper bound."
        ) as vo:
            vo.wait_until("r")
            self.play(FadeIn(reuse, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()
