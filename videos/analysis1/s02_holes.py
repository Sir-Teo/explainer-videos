from __future__ import annotations

from fractions import Fraction

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import SQRT2, Window, load, pin


def below_sqrt2(v, p, q):
    """True where p/q > sqrt 2 (exact: p^2 > 2 q^2)."""
    p = np.asarray(p, dtype=object)
    q = np.asarray(q, dtype=object)
    return np.array([int(a) * int(a) > 2 * int(b) * int(b) for a, b in zip(p, q)], bool)


class Holes(VoiceoverScene):
    def construct(self):
        self.card()
        self.field()
        self.density()
        self.irrational()
        self.rudin()
        self.bounds()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Holes in the rational line",
                            r"Why is $\sqrt2$ not a fraction, and why does that matter?", part=1)
        with self.voiceover("Chapter one. We start with what we have: the rational numbers.") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def field(self):
        win = Window(1.0, 4.4, y=-2.3)
        self.win = win
        axis, dust, labs = win.axis(), win.dust(height=1.3, nonneg=False), win.labels()
        q_def = MathTex(r"\Q = \Big\{ \tfrac{p}{q} \;:\; p, q \in \Z,\; q \neq 0 \Big\}", font_size=44).to_edge(UP, buff=0.5)
        rules = VGroup(
            label(r"\textbf{field:} $+,\ -,\ \times,\ \div$ (except by $0$), with the usual rules", font_size=28),
            label(r"\textbf{order:} $x < y \Rightarrow x + z < y + z$, \quad $x, y > 0 \Rightarrow xy > 0$", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(q_def, DOWN, buff=0.45)
        ref = note(r"Rudin, \textit{Principles} 1.12, 1.17").next_to(rules, DOWN, buff=0.2).align_to(rules, RIGHT)
        with self.voiceover(
            "The rational numbers are the fractions p over q, where p and q are whole numbers and q is not zero. "
            "<bookmark mark='f'/> You can add, subtract, multiply and divide them, except by zero, and the familiar rules "
            "hold. In Rudin's language, they form a field. <bookmark mark='o'/> You can also compare them, and the order "
            "plays well with the arithmetic: adding the same number to both sides of an inequality keeps it true, and "
            "a product of positive numbers is positive. <bookmark mark='q'/> An ordered field."
        ) as vo:
            self.play(Write(q_def))
            self.play(Create(axis), FadeIn(dust), FadeIn(labs))
            vo.wait_until("f")
            self.play(FadeIn(rules[0], shift=RIGHT * 0.2))
            vo.wait_until("o")
            self.play(FadeIn(rules[1], shift=RIGHT * 0.2), FadeIn(ref))
        self.wait(0.2)
        self.play(FadeOut(VGroup(q_def, rules, ref)))
        self.axis, self.dust, self.labs = axis, dust, labs

    # ------------------------------------------------------------------
    def density(self):
        win = self.win
        r, s = Fraction(5, 4), Fraction(3, 2)
        r_d = pin(Dot(radius=0.08, color=C.SEQ), win, float(r))
        s_d = pin(Dot(radius=0.08, color=C.SEQ), win, float(s))
        r_l = pin(MathTex(r"\tfrac54", font_size=34, color=C.SEQ), win, float(r), dy=2.05)
        s_l = pin(MathTex(r"\tfrac32", font_size=34, color=C.SEQ), win, float(s), dy=2.05)
        mids = []
        a, b = r, s
        for k in range(3):
            m = (a + b) / 2
            mids.append(m)
            b = m
        assert mids == [Fraction(11, 8), Fraction(21, 16), Fraction(41, 32)]
        mid_dots = [pin(Dot(radius=0.07, color=C.EPS), win, float(m)) for m in mids]
        mid_tex = [pin(MathTex(rf"\tfrac{{{m.numerator}}}{{{m.denominator}}}", font_size=30, color=C.EPS), win, float(m),
                       dy=2.05 - 0.0) for m in mids]
        avg = MathTex(r"r < \frac{r + s}{2} < s", font_size=40).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Between any two fractions there's another one: their average. <bookmark mark='a'/> Between five quarters "
            "and three halves sits eleven eighths; <bookmark mark='b'/> between five quarters and eleven eighths sits "
            "twenty-one sixteenths, and so on forever. So the fractions are dense: <bookmark mark='z'/> zoom in "
            "anywhere, and there are more of them."
        ) as vo:
            self.play(FadeIn(r_d), FadeIn(s_d), FadeIn(r_l), FadeIn(s_l), Write(avg))
            vo.wait_until("a")
            self.play(FadeIn(mid_dots[0], scale=2), FadeIn(mid_tex[0]))
            vo.wait_until("b")
            self.play(*win.zoom_to(1.33, 0.36), FadeOut(r_l), FadeOut(s_l), run_time=1.5)
            r_l2 = pin(MathTex(r"\tfrac54", font_size=30, color=C.SEQ), win, float(r), dy=2.05)
            self.play(FadeIn(r_l2), FadeIn(mid_dots[1], scale=2), FadeIn(mid_tex[1]))
            vo.wait_until("z")
            self.play(FadeOut(VGroup(mid_tex[0], mid_tex[1], r_l2)))
            self.play(*win.zoom_to(1.29, 0.05), run_time=2)
        for m in (r_d, s_d, *mid_dots, *mid_tex):
            m.clear_updaters()
        self.play(FadeOut(VGroup(r_d, s_d, *mid_dots, mid_tex[2], avg)))

        warn = VGroup(
            label(r"Careful: the line under the ticks is already the \emph{real} line.", font_size=30),
            label(r"$\Q$ is only the ticks. At every zoom they look gap-free.", font_size=30, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.6)
        with self.voiceover(
            "But be careful with this picture. <bookmark mark='w'/> The line I'm drawing the ticks on is already the "
            "real line, the thing we haven't built yet. The rationals are only the ticks. <bookmark mark='g'/> Is there a "
            "gap between them? You can't see one at any zoom, because there's always another tick nearby. A hole in "
            "the rationals only shows up when we ask about limits, or, as Rudin does at the very start of his book, "
            "about bounds."
        ) as vo:
            vo.wait_until("w")
            self.play(FadeIn(warn[0]))
            vo.wait_until("g")
            self.play(FadeIn(warn[1]), *win.zoom_to(1.2907, 0.004), run_time=2.5)
        self.play(FadeOut(warn))
        self.play(*win.zoom_to(1.5, 1.25), run_time=1.5)

    # ------------------------------------------------------------------
    def irrational(self):
        rows = [
            MathTex(r"\Big(\frac{p}{q}\Big)^2", r"=", r"2", font_size=42),
            MathTex(r"p^2", r"=", r"2q^2", font_size=42),
            MathTex(r"p", r"=", r"2r", font_size=42),
            MathTex(r"4r^2", r"=", r"2q^2", font_size=42),
            MathTex(r"q^2", r"=", r"2r^2", font_size=42),
        ]
        whys = [why(r"suppose so, with $p/q$ in lowest terms"), why(r"so $p^2$ is even, hence $p$ is even"),
                why(r"for some whole number $r$"), why(r"substitute"), why(r"so $q$ is even too: contradiction")]
        for r_ in rows:
            r_.set_color(WHITE)
        step = ladder(self, rows, whys, keep=5, top=3.3, buff=0.32, x=-2.6)
        bg = BackgroundRectangle(VGroup(*rows, *whys), color=BACKGROUND, fill_opacity=0.0)
        self.add(bg)
        with self.voiceover(
            "First, the oldest fact in the subject: no fraction squares to two. <bookmark mark='a'/> Suppose p over q, "
            "in lowest terms, did. <bookmark mark='b'/> Then p squared is twice q squared, so p squared is even, and "
            "therefore p is even: <bookmark mark='c'/> p is 2r for some whole number r. <bookmark mark='d'/> Then four "
            "r squared equals two q squared, <bookmark mark='e'/> so q squared is twice r squared, and q is even too. "
            "But we said the fraction was in lowest terms. So it can't exist."
        ) as vo:
            for i, mk in enumerate("abcde"):
                vo.wait_until(mk)
                step(i, run_time=0.9)
        box = SurroundingRectangle(VGroup(rows[-1], whys[-1]), color=C.HOLE, buff=0.15, corner_radius=0.1)
        self.play(Create(box))
        self.wait(0.4)
        self.play(FadeOut(VGroup(*rows, *whys, box)))

    # ------------------------------------------------------------------
    def rudin(self):
        win = self.win
        dust2 = win.dust(height=1.3, split=below_sqrt2, color=C.CUT_LOW, color_hi=C.CUT_HIGH)
        AB = VGroup(
            MathTex(r"A = \{\, p \in \Q : p > 0,\ p^2 < 2 \,\}", font_size=36, color=C.CUT_LOW),
            MathTex(r"B = \{\, p \in \Q : p > 0,\ p^2 > 2 \,\}", font_size=36, color=C.CUT_HIGH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UL, buff=0.45)
        thm = VGroup(label(r"\textbf{Theorem} (Rudin 1.1)", font_size=28, color=GREY_A),
                     label(r"$A$ has no largest element.", font_size=30),
                     label(r"$B$ has no smallest element.", font_size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        thm.to_corner(UR, buff=0.45)
        with self.voiceover(
            "Rudin makes this sharper. <bookmark mark='c'/> Color every positive fraction by which side of the missing "
            "square root it falls on. <bookmark mark='a'/> Let A be the positive fractions whose square is less than "
            "two, <bookmark mark='b'/> and B the ones whose square is more than two. <bookmark mark='t'/> The theorem: "
            "A has no largest element, and B has no smallest element."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeOut(self.dust), FadeIn(dust2), run_time=1.5)
            vo.wait_until("a")
            self.play(Write(AB[0]))
            vo.wait_until("b")
            self.play(Write(AB[1]))
            vo.wait_until("t")
            self.play(FadeIn(thm))
        self.play(FadeOut(thm))

        rows = [
            MathTex(r"q", r"=", r"p - \frac{p^2 - 2}{p + 2}", font_size=40),
            MathTex(r"q", r"=", r"\frac{2p + 2}{p + 2}", font_size=40),
            MathTex(r"q^2 - 2", r"=", r"\frac{2\,(p^2 - 2)}{(p + 2)^2}", font_size=40),
        ]
        whys = [why(r"nudge $p$ by an amount with the sign of $p^2 - 2$"), why(r"common denominator"),
                why(r"square it: the same sign as $p^2 - 2$")]
        step = ladder(self, rows, whys, keep=3, top=3.35, buff=0.25, x=-1.2)
        with self.voiceover(
            "The proof is a single clever formula. <bookmark mark='a'/> Given a positive fraction p, define q as p minus "
            "p squared minus two, over p plus two. <bookmark mark='b'/> Over a common denominator that's 2p plus 2, over "
            "p plus 2: another fraction. <bookmark mark='c'/> And if you square it and subtract two, you get two times p "
            "squared minus two, over p plus two squared. That has the same sign as p squared minus two."
        ) as vo:
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                if i == 0:
                    self.play(FadeOut(AB), run_time=0.4)
                step(i)
        cons = VGroup(
            label(r"if $p \in A$: \ $p^2 - 2 < 0$, so $q > p$ \ and \ $q^2 < 2$, so $q \in A$", font_size=30,
                  color=C.CUT_LOW),
            label(r"if $p \in B$: \ $p^2 - 2 > 0$, so $q < p$ \ and \ $q^2 > 2$, so $q \in B$", font_size=30,
                  color=C.CUT_HIGH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(rows[-1], DOWN, buff=0.35)
        with self.voiceover(
            "Now read it off. <bookmark mark='a'/> If p is in A, then p squared minus two is negative, so we subtracted "
            "a negative number: q is bigger than p. And q squared is still less than two, so q is in A. A bigger "
            "element of A, every time. <bookmark mark='b'/> If p is in B, everything flips: q is smaller than p, and "
            "still in B."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cons[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cons[1], shift=RIGHT * 0.2))
        self.wait(0.3)
        hop_formula = MathTex(r"p \;\longmapsto\; \frac{2p+2}{p+2}", font_size=36).to_corner(UL, buff=0.45)
        self.play(FadeOut(VGroup(*rows, *whys, cons)), FadeIn(hop_formula))
        self.hops(dust2)
        self.play(FadeOut(hop_formula))
        self.dust2 = dust2

    def hops(self, dust2):
        win = self.win
        h = load("hops")
        up = [Fraction(int(n), int(d)) for n, d in zip(h["up_n"], h["up_d"])]
        down = [Fraction(int(n), int(d)) for n, d in zip(h["down_n"], h["down_d"])]
        assert up[:5] == [1, Fraction(4, 3), Fraction(7, 5), Fraction(24, 17), Fraction(41, 29)]
        assert down[:5] == [2, Fraction(3, 2), Fraction(10, 7), Fraction(17, 12), Fraction(58, 41)]

        def frac(f):
            return rf"\tfrac{{{f.numerator}}}{{{f.denominator}}}" if f.denominator > 1 else str(f.numerator)

        def sq(f):
            return f"{float(f * f):.5f}".rstrip("0")

        marks, texts = VGroup(), VGroup()

        def show_point(f, color, dy):
            d = pin(Dot(radius=0.075, color=color), win, float(f))
            t = pin(MathTex(frac(f), font_size=30, color=color), win, float(f), dy=dy)
            marks.add(d)
            texts.add(t)
            return d, t

        def arc(f, g, color):
            a, b = win.P(float(f), 0.08), win.P(float(g), 0.08)
            return CurvedArrow(a, b, angle=-TAU / 5 if g > f else TAU / 5, color=color, stroke_width=3,
                               tip_length=0.18)

        sq_tab = VGroup().to_corner(UR, buff=0.45)
        with self.voiceover(
            "Watch it run. <bookmark mark='a'/> Start at one, in A. One hops to four thirds, <bookmark mark='b'/> four "
            "thirds hops to seven fifths, <bookmark mark='c'/> then twenty-four seventeenths, <bookmark mark='d'/> then "
            "forty-one twenty-ninths. Every hop lands in A again, a little higher, and the squares creep up toward two "
            "without ever reaching it."
        ) as vo:
            vo.wait_until("a")
            show_point(up[0], C.CUT_LOW, 2.0)
            self.play(FadeIn(marks[-1], scale=2), FadeIn(texts[-1]))
            schedule = [(None, None), ("b", (1.375, 0.24)), ("c", (1.406, 0.024)), ("d", (1.4128, 0.0032))]
            for k in range(1, 5):
                mk, zoom = schedule[min(k, 3)] if k < 4 else ("d", (1.41355, 0.0013))
                if k >= 2 and mk:
                    vo.wait_until(mk)
                if zoom and k >= 2:
                    self.play(*win.zoom_to(*zoom), run_time=1.2)
                ar = arc(up[k - 1], up[k], C.CUT_LOW)
                self.play(Create(ar), run_time=0.7)
                show_point(up[k], C.CUT_LOW, 2.0)
                row = MathTex(rf"\big({frac(up[k])}\big)^2 = {sq(up[k])}", font_size=28, color=C.CUT_LOW)
                sq_tab.add(row)
                sq_tab.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.45)
                self.play(FadeIn(marks[-1], scale=2), FadeIn(texts[-1]), FadeIn(row), FadeOut(ar), run_time=0.7)
                for t in texts[:-1]:
                    t.clear_updaters()
                if len(texts) > 1:
                    self.play(FadeOut(texts[-2]), run_time=0.3)
        self.play(FadeOut(sq_tab), FadeOut(texts[-1]))
        texts.remove(texts[-1])
        self.play(*win.zoom_to(1.6, 1.0), run_time=1.5)
        sq_tab2 = VGroup()
        with self.voiceover(
            "From above it's the mirror image. <bookmark mark='a'/> Two hops down to three halves, then ten sevenths, "
            "then seventeen twelfths: always in B, always smaller, never reaching the bottom."
        ) as vo:
            vo.wait_until("a")
            show_point(down[0], C.CUT_HIGH, 2.0)
            self.play(FadeIn(marks[-1], scale=2), FadeIn(texts[-1]))
            for k, zoom in ((1, None), (2, (1.47, 0.2)), (3, (1.43, 0.06))):
                if zoom:
                    self.play(*win.zoom_to(*zoom), run_time=1.0)
                ar = arc(down[k - 1], down[k], C.CUT_HIGH)
                self.play(Create(ar), run_time=0.6)
                show_point(down[k], C.CUT_HIGH, 2.0)
                row = MathTex(rf"\big({frac(down[k])}\big)^2 = {sq(down[k])}", font_size=28, color=C.CUT_HIGH)
                sq_tab2.add(row)
                sq_tab2.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.45)
                self.play(FadeIn(marks[-1], scale=2), FadeIn(texts[-1]), FadeIn(row), FadeOut(ar), run_time=0.6)
                if len(texts) > 1:
                    texts[-2].clear_updaters()
                    self.play(FadeOut(texts[-2]), run_time=0.3)
        self.play(FadeOut(sq_tab2), FadeOut(texts[-1]))
        for m in (*marks, *texts):
            m.clear_updaters()
        self.play(FadeOut(marks))
        self.play(*win.zoom_to(1.5, 1.25), run_time=1.5)

    # ------------------------------------------------------------------
    def bounds(self):
        win = self.win
        defs = VGroup(
            label(r"$\beta$ is an \textbf{upper bound} of $E$ \ if \ $x \le \beta$ for every $x \in E$.", font_size=30),
            label(r"$\alpha = \sup E$, the \textbf{least upper bound}, \ if", font_size=30),
            label(r"\quad (i) \ $\alpha$ is an upper bound of $E$, \ and", font_size=30),
            label(r"\quad (ii) \ no $\gamma < \alpha$ is an upper bound of $E$.", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(UP, buff=0.45)
        ref = note(r"Rudin 1.7, 1.8").next_to(defs, DOWN, buff=0.15).align_to(defs, RIGHT)
        with self.voiceover(
            "This is a statement about bounds. <bookmark mark='u'/> A number beta is an upper bound of a set E if "
            "everything in E is at most beta. <bookmark mark='s'/> And alpha is the least upper bound, the supremum, "
            "written sup E, if it's an upper bound, and nothing smaller is one."
        ) as vo:
            vo.wait_until("u")
            self.play(FadeIn(defs[0]))
            vo.wait_until("s")
            self.play(FadeIn(defs[1:]), FadeIn(ref))
        ex = VGroup(
            MathTex(r"\sup\{x \in \Q : x < 1\} = 1 \notin \text{the set}", font_size=32),
            MathTex(r"\sup\{1, \tfrac12, \tfrac13, \ldots\} = 1 \in \text{the set}", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ref, DOWN, buff=0.35)
        with self.voiceover(
            "A supremum doesn't have to belong to the set. <bookmark mark='a'/> The fractions below one have supremum "
            "one, which is not below one. <bookmark mark='b'/> The set one, a half, a third, and so on, has supremum "
            "one, which it contains."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(ex[0]))
            vo.wait_until("b")
            self.play(FadeIn(ex[1]))
        self.wait(0.3)
        self.play(FadeOut(VGroup(defs[0], defs[2:], ref, ex)), defs[1].animate.to_edge(UP, buff=0.5))

        ub = Brace(Line(win.P(SQRT2, -0.3), win.P(2.1, -0.3)), DOWN, color=C.CUT_HIGH)
        ub_l = label(r"every element of $B$ is an upper bound of $A$", font_size=28, color=C.CUT_HIGH)
        ub_l.next_to(ub, DOWN, buff=0.1)
        hole = pin(Circle(radius=0.11, color=C.HOLE, stroke_width=3), win, SQRT2)
        claim = VGroup(
            label(r"In $\Q$, the upper bounds of $A$ are exactly the elements of $B$,", font_size=30),
            label(r"and $B$ has no smallest element. \ So $\sup A$ does not exist in $\Q$.", font_size=30),
        ).arrange(DOWN, buff=0.15).next_to(defs[1], DOWN, buff=0.35)
        with self.voiceover(
            "Now apply this to A. <bookmark mark='a'/> Every element of B is an upper bound of A. And there are no "
            "others: an upper bound whose square was less than two would itself be in A, and A always has something "
            "bigger. <bookmark mark='b'/> So, in the rationals, the upper bounds of A are exactly the elements of B, "
            "and B has no smallest element. The set A is bounded above, and yet it has no least upper bound. "
            "<bookmark mark='h'/> That's the hole, stated without pictures."
        ) as vo:
            vo.wait_until("a")
            self.play(GrowFromCenter(ub), FadeIn(ub_l))
            vo.wait_until("b")
            self.play(FadeIn(claim))
            vo.wait_until("h")
            self.play(FadeIn(hole, scale=2))
        self.wait(0.3)
        hole.clear_updaters()
        self.play(FadeOut(VGroup(ub, ub_l, claim, defs[1], hole)))

        prop = VGroup(
            label(r"\textbf{Least-upper-bound property} (Rudin 1.10)", font_size=32, color=GREY_A),
            label(r"Every nonempty subset that is bounded above has a supremum.", font_size=32),
        ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.5)
        no_q = label(r"$\Q$ does \emph{not} have it.", font_size=34, color=C.HOLE).next_to(prop, DOWN, buff=0.35)
        thm = VGroup(
            label(r"\textbf{Theorem} (Rudin 1.19)", font_size=30, color=GREY_A),
            label(r"There is an ordered field $\R$ with the least-upper-bound property", font_size=30),
            label(r"that contains $\Q$.", font_size=30),
        ).arrange(DOWN, buff=0.15)
        thm_b = boxed(thm, color=C.EPS, buff=0.3).next_to(no_q, DOWN, buff=0.45)
        with self.voiceover(
            "So here's the property we want. <bookmark mark='p'/> An ordered set has the least-upper-bound property if "
            "every nonempty subset that is bounded above has a supremum. <bookmark mark='q'/> The rationals don't have "
            "it; that's the precise meaning of the rationals have holes. <bookmark mark='t'/> And the first big theorem "
            "of the subject says we can fix it: there is an ordered field, the real numbers, that has the "
            "least-upper-bound property and contains the rationals. Next, we build it out of nothing but fractions."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(prop))
            vo.wait_until("q")
            self.play(FadeIn(no_q))
            vo.wait_until("t")
            self.play(FadeIn(thm_b, shift=UP * 0.2))
        self.wait(0.6)
        for m in (self.axis, self.dust2, self.labs):
            m.clear_updaters()
        self.clear_scene()
