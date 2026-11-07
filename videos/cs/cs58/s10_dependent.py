from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs58.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, mono


def fit(m, w):
    """Scale a mobject down to width w if it is wider."""
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def keep_in(m, x0=-6.85, x1=6.85):
    """Shift a mobject sideways so that it lies inside [x0, x1]."""
    if m.get_right()[0] > x1:
        m.shift(LEFT * (m.get_right()[0] - x1))
    if m.get_left()[0] < x0:
        m.shift(RIGHT * (x0 - m.get_left()[0]))
    return m


def cells(values, color=WHITE, w=0.6, h=0.46, fs=26):
    """A vector drawn as a row of boxes."""
    g = VGroup()
    for v in values:
        r = Rectangle(width=w, height=h, stroke_color=GREY_C, stroke_width=1.6, fill_color=BG, fill_opacity=1)
        g.add(VGroup(r, MathTex(str(v), font_size=fs, color=color).move_to(r)))
    return g.arrange(RIGHT, buff=0.05)


def box(body, col, pad=0.3, w=None, h=None):
    """A rounded frame around a mobject."""
    fr = RoundedRectangle(width=w or body.width + 2 * pad, height=h or body.height + 2 * pad, corner_radius=0.14,
                          stroke_color=col, stroke_width=2, fill_color=BG, fill_opacity=1).move_to(body)
    return VGroup(fr, body)


VEC = r"\mathsf{Vec}"


class Dependent(VoiceoverScene):
    def construct(self):
        self.card()
        self.pi_sigma()
        self.vectors()
        self.props()
        self.by_computation()
        self.termination()
        self.kernel()

    def card(self):
        card = chapter_card(9, r"Dependent types", r"What if types could mention values, \ and proofs were programs?",
                            lit=(1972, 1988), extra=((1972, r"Martin-L\"of: \ intuitionistic type theory"),
                                                     (1988, r"Coquand and Huet: \ the calculus of constructions")),
                            part=PART)
        with self.voiceover("Chapter nine. Dependent types. What if types could mention values, and proofs were "
                            "programs?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ Pi and Sigma
    def pi_sigma(self):
        head = label(r"Types that depend on values: \ $\Pi$ and $\Sigma$", font_size=36).to_edge(UP, buff=0.3)
        base_y = -2.55
        xs = [-5.9 + 1.1 * n for n in range(5)]
        base = Line([-6.4, base_y, 0], [-1.0, base_y, 0], color=GREY_B, stroke_width=2.5)
        ticks = VGroup(*[Dot([x, base_y, 0], radius=0.06, color=GREY_B) for x in xs])
        nums = VGroup(*[MathTex(str(n), font_size=24, color=GREY_B).next_to(t, DOWN, buff=0.12)
                        for n, t in enumerate(ticks)])
        alab = MathTex(r"x : A", font_size=24, color=GREY_B).next_to(base, RIGHT, buff=0.15).shift(DOWN * 0.3)
        heights = [0.8 + 0.6 * n for n in range(5)]
        fib = VGroup(*[RoundedRectangle(width=0.62, height=hh, corner_radius=0.1, stroke_color=DATA, stroke_width=1.8,
                                        fill_color=DATA, fill_opacity=0.1).move_to([x, base_y + 0.2 + hh / 2, 0])
                       for x, hh in zip(xs, heights)])
        flab = VGroup(*[MathTex(rf"B({n})", font_size=22, color=DATA).next_to(f, UP, buff=0.1)
                        for n, f in enumerate(fib)])
        fr = [0.5, 0.3, 0.7, 0.4, 0.62]
        sec_pts = [[x, f.get_bottom()[1] + q * f.height, 0] for x, f, q in zip(xs, fib, fr)]
        sec_dots = VGroup(*[Dot(p, radius=0.08, color=YES) for p in sec_pts])
        sec = VMobject(color=YES, stroke_width=3).set_points_as_corners(sec_pts)
        sig = Dot([xs[2], fib[2].get_bottom()[1] + 0.25 * fib[2].height, 0], radius=0.1, color=LAM)
        sigl = MathTex(r"(2,\ b)", font_size=19, color=LAM).next_to(sig, UP, buff=0.08).set_z_index(3)
        fs = 34
        pi0 = MathTex(r"\Pi(x{:}A).\ ", r"B(x)", font_size=fs, color=YES)
        pi1 = MathTex(r"\Pi(x{:}A).\ ", r"B", r"\ =\ ", r"A \to B", font_size=28, color=GREY_A)
        pie = MathTex(r"\mathsf{zeros} : \Pi(n{:}\N).\ " + VEC + r"\,\N\,n", font_size=28, color=WHITE)
        sg0 = MathTex(r"\Sigma(x{:}A).\ ", r"B(x)", font_size=fs, color=LAM)
        sg1 = MathTex(r"\Sigma(x{:}A).\ ", r"B", r"\ =\ ", r"A \times B", font_size=28, color=GREY_A)
        sge = MathTex(r"\Sigma(n{:}\N).\ " + VEC + r"\,\N\,n", font_size=28, color=WHITE)
        pl = label(r"dependent function: \ one element from every column", font_size=21, color=YES)
        sl = label(r"dependent pair: \ one point in one column", font_size=21, color=LAM)
        pe = label(r"a vector of zeros of every length", font_size=18, color=GREY_B)
        se = label(r"a vector of some length, \ paired with its length", font_size=18, color=GREY_B)
        right = VGroup(pl, pi0, pi1, VGroup(pie, pe).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
                       sl, sg0, sg1, VGroup(sge, se).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        right.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(head, DOWN, buff=0.4)
        right.align_to(np.array([0.0, 0, 0]), LEFT)
        right[4].shift(DOWN * 0.2)
        right[5:].shift(DOWN * 0.2)
        for r in (pi1, sg1):
            r.shift(RIGHT * 0.4)
        keep_in(right)
        foot = label(r"Martin-L\"of type theory \ (from 1972): \ built on $\Pi$ and $\Sigma$",
                     font_size=20, color=GREY_B).to_edge(DOWN, buff=0.25).align_to(right, LEFT)
        with self.voiceover(
            "Part 14 gave a first glimpse of types that mention values; here is how far the idea goes. <bookmark mark='a'/> Picture a family of types, one for "
            "each x in A, each a column above its point. <bookmark mark='b'/> A dependent function picks an element "
            "from every column, so its result type depends on its argument. Its type is a capital pi. <bookmark "
            "mark='c'/> When B does not mention x, every column is the same, and pi is the ordinary arrow. <bookmark "
            "mark='d'/> A dependent pair is one point in one column: a value x, and an element of B of x. Its type "
            "is a capital sigma, <bookmark mark='e'/> and when B is constant, the ordinary product. <bookmark "
            "mark='f'/> Per Martin-L\u00f6f's type theory, begun in nineteen seventy-two, is built on these two."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(ticks), FadeIn(nums), FadeIn(alab))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(f, DOWN) for f in fib], lag_ratio=0.2), FadeIn(flab))
            vo.wait_until("b")
            self.play(FadeIn(pl), Write(pi0))
            self.play(Create(sec), LaggedStart(*[GrowFromCenter(d) for d in sec_dots], lag_ratio=0.15))
            self.play(FadeIn(right[3]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(pi0.copy(), pi1), run_time=1.3)
            vo.wait_until("d")
            self.play(FadeIn(sl), Write(sg0), GrowFromCenter(sig), FadeIn(sigl))
            self.play(FadeIn(right[7]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(sg0.copy(), sg1), run_time=1.3)
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ length-indexed vectors
    def vectors(self):
        head = label(r"A vector that knows its length", font_size=36).to_edge(UP, buff=0.3)
        fs = 28
        defs = VGroup(
            MathTex(VEC + r"\,A : \N \to \mathsf{Type}", font_size=fs, color=DATA),
            MathTex(r"\mathsf{nil} : " + VEC + r"\,A\,0", font_size=fs),
            MathTex(r"\mathsf{cons} : A \to " + VEC + r"\,A\,n \to " + VEC + r"\,A\,(n+1)", font_size=fs),
            MathTex(r"\mathsf{head} : " + VEC + r"\,A\,(n+1) \to A", font_size=fs, color=HEAD),
            MathTex(r"\mathsf{append} : " + VEC + r"\,A\,m \to " + VEC + r"\,A\,n \to " + VEC + r"\,A\,(m+n)",
                    font_size=fs, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.7).to_edge(LEFT, buff=0.45)
        fit(defs, 6.9)
        xr = 3.6
        va = cells([7, 2], color=DATA).move_to([xr - 1.0, 1.7, 0])
        vb = cells([5], color=LAM).move_to([xr + 1.3, 1.7, 0])
        ta = MathTex(VEC + r"\,\N\,2", font_size=24, color=DATA).next_to(va, UP, buff=0.15)
        tb = MathTex(VEC + r"\,\N\,1", font_size=24, color=LAM).next_to(vb, UP, buff=0.15)
        vc = cells([7, 2, 5], color=WHITE).move_to([xr, -0.05, 0])
        for k, c in enumerate((DATA, DATA, LAM)):
            vc[k][1].set_color(c)
        arr = Arrow(VGroup(va, vb).get_bottom() + DOWN * 0.05, vc.get_top() + UP * 0.6, buff=0.05, color=GREY_B,
                    stroke_width=2.5, max_tip_length_to_length_ratio=0.2)
        al = label(r"\textsf{append}", font_size=19, color=GREY_B).next_to(arr, RIGHT, buff=0.1)
        t0 = MathTex(VEC + r"\,\N\,", r"(2+1)", font_size=28, color=WHITE).next_to(vc, UP, buff=0.15)
        t1 = MathTex(VEC + r"\,\N\,", r"3", font_size=28, color=YES).move_to(t0)
        t1[1].set_color(YES)
        bad = MathTex(r"\mathsf{head}\ \mathsf{nil}", font_size=32, color=NO).move_to([xr, -1.5, 0])
        badw = label(r"rejected: \ no $n$ has $n + 1 = 0$", font_size=20, color=NO).next_to(bad, DOWN, buff=0.32)
        cross = SurroundingRectangle(bad, buff=0.15, corner_radius=0.08, color=NO, stroke_width=2.5)
        foot = wrapped_label(r"a crash at run time \ (the head of an empty list) \ becomes an error before the program "
                             r"runs", 12.4, font_size=21, color=WHITE).to_edge(DOWN, buff=0.35)
        ill = note(r"illustrative values", font_size=16).next_to(vb, RIGHT, buff=0.3)
        keep_in(ill)
        with self.voiceover(
            "Part 14's example, now in full: a list that carries its length in its type. <bookmark mark='a'/> Vec A n is the "
            "type of lists of exactly n elements of A. <bookmark mark='b'/> nil has length zero, and cons, on a "
            "vector of length n, gives length n plus one. <bookmark mark='c'/> Now head can demand a vector of "
            "length n plus one, <bookmark mark='d'/> and append, given lengths m and n, returns length m plus n. "
            "<bookmark mark='e'/> Append seven and two to five. <bookmark mark='f'/> The checker computes the type: "
            "two plus one, which is three. <bookmark mark='g'/> And head of the empty vector is not a crash at run "
            "time, as in most languages; it is rejected before the program runs, because no n plus one equals zero."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(defs[0]))
            vo.wait_until("b")
            self.play(FadeIn(defs[1]))
            self.play(FadeIn(defs[2]))
            vo.wait_until("c")
            self.play(FadeIn(defs[3]))
            vo.wait_until("d")
            self.play(FadeIn(defs[4]))
            vo.wait_until("e")
            self.play(FadeIn(va), FadeIn(vb), FadeIn(ta), FadeIn(tb), FadeIn(ill))
            self.play(GrowArrow(arr), FadeIn(al))
            self.play(TransformFromCopy(va, vc[:2]), TransformFromCopy(vb, vc[2]), FadeIn(t0))
            vo.wait_until("f")
            self.play(TransformMatchingTex(t0, t1), run_time=1.2)
            self.play(Circumscribe(t1, color=YES))
            vo.wait_until("g")
            self.play(Write(bad))
            self.play(Create(cross), FadeIn(badw))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ propositions as types, extended
    def props(self):
        head = label(r"Propositions as types, \ extended", font_size=36).to_edge(UP, buff=0.3)
        old = [(r"A \wedge B", r"A \times B", r"a pair of proofs"), (r"A \vee B", r"A + B", r"a tagged proof"),
               (r"A \Rightarrow B", r"A \to B", r"a function on proofs"), (r"\bot", r"0", r"the empty type")]
        new = [(r"\forall x{:}A.\ P(x)", r"\Pi(x{:}A).\ P(x)", r"a proof for every $x$"),
               (r"\exists x{:}A.\ P(x)", r"\Sigma(x{:}A).\ P(x)", r"a witness, \ and a proof"),
               (r"a = b", r"\mathsf{Id}_A(a, b)", r"made by $\mathsf{refl} : \mathsf{Id}_A(a, a)$")]
        cx = [-5.3, -2.7]
        hdr = VGroup(label(r"logic", font_size=22, color=GREY_B).move_to([cx[0], 2.55, 0]),
                     label(r"type", font_size=22, color=GREY_B).move_to([cx[1], 2.55, 0]))
        rows = VGroup()
        for k, (lg, ty, wh) in enumerate(old + new):
            y = 2.0 - 0.58 * k - (0.25 if k >= len(old) else 0)
            col = GREY_A if k < len(old) else YES
            r = VGroup(MathTex(lg, font_size=28, color=col).move_to([cx[0], y, 0]),
                       MathTex(ty, font_size=28, color=col).move_to([cx[1], y, 0]),
                       label(wh, font_size=18, color=GREY_B))
            r[2].move_to([-1.4 + r[2].width / 2, y, 0])
            rows.add(r)
        rule = Line([-6.5, 0, 0], [1.5, 0, 0], color=GREY_D, stroke_width=1.5).move_to(
            [-2.5, (rows[3].get_y() + rows[4].get_y()) / 2, 0])
        tag14 = label(r"Part 14", font_size=18, color=GREY_B).next_to(rows[0], UP, buff=0.05).shift(RIGHT * 3.0)
        tagd = label(r"dependent", font_size=18, color=YES).next_to(rule, DOWN, buff=0.05).align_to(tag14, RIGHT)
        tag14.align_to(tagd, RIGHT)
        tag14.next_to(hdr, RIGHT, buff=0.3).align_to(tagd, RIGHT)
        ex = VGroup(
            label(r"for every $n$ there is a larger $m$:", font_size=21, color=WHITE),
            MathTex(r"\Pi(n{:}\N).\ \Sigma(m{:}\N).\ n < m", font_size=32, color=YES),
            label(r"proved by the program", font_size=21, color=WHITE),
            MathTex(r"\lambda n.\ (n+1,\ \mathsf{lt\_succ}\,n)", font_size=32, color=HEAD),
            label(r"$\mathsf{lt\_succ}\,n : n < n+1$, \ itself a program", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.3, 0.8, 0])
        keep_in(ex)
        cap = wrapped_label(r"a proof is a program; \ checking a proof is checking a type", 12.4, font_size=24,
                            color=YES).to_edge(DOWN, buff=0.45)
        ill = note(r"illustrative lemma name", font_size=16).next_to(ex, DOWN, buff=0.2).align_to(ex, LEFT)
        with self.voiceover(
            "Part 14 met the Curry\u2013Howard correspondence. <bookmark mark='a'/> A proof of A and B is a pair, a proof "
            "of A or B is a tagged proof of one, a proof that A implies B is a function, and falsehood is the empty "
            "type. <bookmark mark='b'/> For all x, P of x, is a dependent function: a proof for every x. <bookmark "
            "mark='c'/> There exists an x with P of x is a dependent pair: a witness, and a proof about it. "
            "<bookmark mark='d'/> And equality is a type, whose one constructor, refl, proves that a value equals "
            "itself. <bookmark mark='e'/> For every n there is a larger m: the proof is a function returning n plus "
            "one, with a proof that it is larger. <bookmark mark='f'/> A proof is a program, and checking it is type "
            "checking."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            vo.wait_until("a")
            self.play(FadeIn(tag14), LaggedStart(*[FadeIn(r) for r in rows[:4]], lag_ratio=0.3), run_time=2)
            vo.wait_until("b")
            self.play(Create(rule), FadeIn(tagd), FadeIn(rows[4], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(rows[5], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(rows[6], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(ex[:2]))
            self.play(FadeIn(ex[2:]), FadeIn(ill))
            vo.wait_until("f")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ a theorem proved by computing
    def by_computation(self):
        head = label(r"A theorem proved by computing", font_size=36).to_edge(UP, buff=0.3)
        plus = MathTex(r"0 + n = n", r"\qquad", r"\mathsf{S}\,m + n = \mathsf{S}(m + n)", font_size=32,
                       color=DATA).next_to(head, DOWN, buff=0.35)
        claim = MathTex(r"\mathsf{refl}", r":", r"2 + 2 = 4", font_size=32, color=HEAD).next_to(plus, DOWN, buff=0.3)
        fs = 32
        rows = VGroup(
            MathTex(r"2 + 2", font_size=fs),
            MathTex(r"=", r"\mathsf{S}(", r"1 + 2", r")", font_size=fs),
            MathTex(r"=", r"\mathsf{S}(", r"\mathsf{S}(", r"0 + 2", r")", r")", font_size=fs),
            MathTex(r"=", r"\mathsf{S}(", r"\mathsf{S}(", r"2", r")", r")", font_size=fs),
            MathTex(r"=", r"4", font_size=fs, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(claim, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
        for r in rows[1:]:
            r.shift(RIGHT * 0.45)
        whys = VGroup(
            label(r"the left side", font_size=19, color=GREY_B),
            label(r"$2 = \mathsf{S}\,1$; \ second equation", font_size=19, color=GREY_B),
            label(r"second equation again", font_size=19, color=GREY_B),
            label(r"first equation", font_size=19, color=GREY_B),
            label(r"the same normal form as $4$", font_size=19, color=YES),
        )
        wx = max(r.get_right()[0] for r in rows) + 0.45
        for w, r in zip(whys, rows):
            w.move_to([wx + w.width / 2, r.get_y(), 0])
        sep = DashedLine([0.85, 1.2, 0], [0.85, -2.9, 0], color=GREY_D, stroke_width=1.5, dash_length=0.1)
        stuck = VGroup(
            MathTex(r"n + 0 = n\ ?", font_size=32, color=NO),
            wrapped_label(r"does not compute: \ $+$ looks at its first argument, \ and $n$ is a variable", 5.2,
                          font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        ind = VGroup(
            MathTex(r"\mathsf{pz} : \Pi(n{:}\N).\ n + 0 = n", font_size=28, color=WHITE),
            MathTex(r"\mathsf{pz}\ 0 = \mathsf{refl}", font_size=28, color=HEAD),
            MathTex(r"\mathsf{pz}\ (\mathsf{S}\,n) = \mathsf{cong}\ \mathsf{S}\ (\mathsf{pz}\ n)", font_size=28,
                    color=HEAD),
            label(r"induction is recursion: \ the call is on a smaller $n$", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rightc = VGroup(stuck, ind).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.9, -0.85, 0])
        keep_in(rightc)
        with self.voiceover(
            "Some theorems are proved by computing. <bookmark mark='a'/> Define addition by recursion on its first "
            "argument: zero plus n is n, and the successor of m, plus n, is the successor of m plus n. <bookmark "
            "mark='b'/> Claim: two plus two equals four, and the proof is refl, which proves that a thing equals "
            "itself. <bookmark mark='c'/> Because the checker computes. Two plus two is the successor of one plus "
            "two, <bookmark mark='d'/> which is the successor of the successor of zero plus two, <bookmark "
            "mark='e'/> which is two with two successors, <bookmark mark='f'/> four. Both sides reach the same "
            "normal form. <bookmark mark='g'/> But n plus zero does not compute: addition looks at its first "
            "argument, and n is a variable. <bookmark mark='h'/> Its proof is a recursive function, whose second "
            "case calls itself on a smaller n. Induction is recursion."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(plus))
            vo.wait_until("b")
            self.play(FadeIn(claim))
            self.play(Write(rows[0]), FadeIn(whys[0]))
            for k, mk in enumerate("cdef", start=1):
                vo.wait_until(mk)
                self.play(TransformMatchingTex(rows[k - 1].copy(), rows[k]), FadeIn(whys[k]), run_time=1.2)
            self.play(Circumscribe(rows[4], color=YES), Indicate(claim[0], color=YES))
            vo.wait_until("g")
            self.play(Create(sep), FadeIn(stuck))
            vo.wait_until("h")
            self.play(FadeIn(ind[0]))
            self.play(FadeIn(ind[1]), FadeIn(ind[2]))
            self.play(FadeIn(ind[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ why checking must terminate
    def termination(self):
        head = label(r"Why every program must terminate", font_size=36).to_edge(UP, buff=0.3)
        fs = 28
        exp = MathTex(VEC + r"\,\N\,", r"3", font_size=fs, color=DATA)
        got = MathTex(VEC + r"\,\N\,", r"(2+1)", font_size=fs, color=LAM)
        ex_l = label(r"expected", font_size=18, color=GREY_B)
        got_l = label(r"given", font_size=18, color=GREY_B)
        left = VGroup(VGroup(ex_l, exp).arrange(DOWN, buff=0.1), VGroup(got_l, got).arrange(DOWN, buff=0.1))
        left.arrange(RIGHT, buff=0.9).move_to([-3.9, 2.1, 0])
        n1 = MathTex(VEC + r"\,\N\,", r"3", font_size=fs, color=DATA).next_to(left[0], DOWN, buff=0.9)
        n2 = MathTex(VEC + r"\,\N\,", r"3", font_size=fs, color=DATA).next_to(left[1], DOWN, buff=0.9)
        a1 = Arrow(left[0].get_bottom(), n1.get_top(), buff=0.1, color=GREY_B, stroke_width=2.5,
                   max_tip_length_to_length_ratio=0.2)
        a2 = Arrow(left[1].get_bottom(), n2.get_top(), buff=0.1, color=GREY_B, stroke_width=2.5,
                   max_tip_length_to_length_ratio=0.2)
        nl = label(r"normalize", font_size=18, color=GREY_B).move_to(VGroup(a1, a2))
        eq = MathTex(r"\equiv\ \checkmark", font_size=32, color=YES).move_to(VGroup(n1, n2))
        badc = VGroup(mono("bad : False", size=20, color=NO), mono("bad = bad", size=20, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1)
        badw = VGroup(wrapped_label(r"a proof of falsehood: \ the logic would prove everything", 5.4, font_size=19,
                                    color=NO),
                      wrapped_label(r"and normalizing it never stops", 5.4, font_size=19, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1)
        badg = VGroup(badc, badw).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.5, 1.7, 0])
        keep_in(badg)
        okr = VGroup(
            VGroup(MathTex(r"\mathsf{pz}\ (\mathsf{S}\,n) = \cdots\ \mathsf{pz}\ n", font_size=26, color=WHITE),
                   label(r"smaller argument: \ accepted", font_size=19, color=YES)).arrange(RIGHT, buff=0.4),
            VGroup(MathTex(r"\mathsf{bad} = \mathsf{bad}", font_size=26, color=WHITE),
                   label(r"no smaller argument: \ rejected", font_size=19, color=NO)).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        okr.move_to([0, -0.85, 0])
        thm = MathTex(r"\vdash t : T", r"\implies", r"t \text{ has a normal form}", font_size=32, color=YES)
        thl = label(r"Tait's method \ (chapter five), \ extended to polymorphism by Girard \ (1972)", font_size=19,
                    color=GREY_B)
        ext = label(r"intensional equality: \ type checking decidable \ \ $\cdot$ \ \ extensional \ (Martin-L\"of "
                    r"1984): \ undecidable", font_size=19, color=HEAD)
        VGroup(thm, thl, ext).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Type checking must decide when two types are equal. <bookmark mark='a'/> Meeting a vector of length two "
            "plus one where it expects length three, it normalizes both and compares. <bookmark mark='b'/> That "
            "works only if normalizing always stops. Allow one looping definition, bad equals bad, and it has any "
            "type, even falsehood: the logic would prove everything, and checking would run forever. <bookmark "
            "mark='c'/> So proof assistants accept only functions they can see terminate, such as recursion on a "
            "structurally smaller argument. <bookmark mark='d'/> That every well-typed term has a normal form is "
            "proved with chapter five's method, Tait's, which Jean-Yves Girard extended to polymorphism in nineteen "
            "seventy-two. <bookmark mark='e'/> Martin-L\u00f6f's nineteen eighty-four theory, with extensional equality, "
            "makes type checking undecidable; the intensional version keeps it decidable."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(nl))
            self.play(TransformMatchingTex(exp.copy(), n1), TransformMatchingTex(got.copy(), n2), run_time=1.2)
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(FadeIn(badc))
            self.play(FadeIn(badw))
            vo.wait_until("c")
            self.play(FadeIn(okr[0]))
            self.play(FadeIn(okr[1]))
            vo.wait_until("d")
            self.play(Write(thm), FadeIn(thl))
            vo.wait_until("e")
            self.play(FadeIn(ext))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ a proof assistant's kernel
    def kernel(self):
        head = label(r"A proof assistant's kernel", font_size=36).to_edge(UP, buff=0.3)
        big_t = VGroup(label(r"tactics, \ automation, \ the elaborator", font_size=22, color=GREY_A),
                       label(r"large, \ clever, \ untrusted", font_size=19, color=NO)).arrange(DOWN, buff=0.15)
        big = box(big_t, GREY_B, w=4.6, h=2.6).move_to([-4.2, 0.6, 0])
        ker_t = VGroup(label(r"kernel", font_size=24, color=YES),
                       label(r"a type checker", font_size=19, color=GREY_A),
                       label(r"small, \ trusted", font_size=19, color=YES)).arrange(DOWN, buff=0.12)
        ker = box(ker_t, YES, w=2.6, h=1.8).move_to([1.3, 0.6, 0])
        a1 = Arrow(big.get_right(), ker.get_left(), buff=0.1, color=HEAD, stroke_width=3,
                   max_tip_length_to_length_ratio=0.12)
        a1l = label(r"proof term", font_size=19, color=HEAD).next_to(a1, UP, buff=0.1)
        ok = VGroup(MathTex(r"\checkmark", font_size=48, color=YES), label(r"theorem", font_size=20, color=YES))
        ok.arrange(DOWN, buff=0.1).move_to([5.0, 0.6, 0])
        a2 = Arrow(ker.get_right(), ok.get_left(), buff=0.15, color=YES, stroke_width=3,
                   max_tip_length_to_length_ratio=0.15)
        user = VGroup(label(r"the user's statement and script", font_size=19, color=WHITE))
        user.next_to(big, UP, buff=0.35)
        ua = Arrow(user.get_bottom(), big.get_top(), buff=0.08, color=GREY_B, stroke_width=2.5,
                   max_tip_length_to_length_ratio=0.25)
        dot = Dot(a1.get_start(), radius=0.1, color=HEAD).set_z_index(5)
        hist = VGroup(
            wrapped_label(r"Coquand and Huet \ (1988): \ the calculus of constructions, \ the core of Coq, \ later "
                          r"extended with inductive types", 12.4, font_size=20, color=GREY_A),
            wrapped_label(r"trust only the kernel: \ Part 54's small trusted kernel again, \ the idea behind "
                          r"checked proofs such as CompCert's", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(big, DOWN, buff=0.8).set_x(0)
        with self.voiceover(
            "This is why a proof assistant can be trusted. <bookmark mark='a'/> Thierry Coquand and G\u00e9rard Huet's "
            "calculus of constructions, of nineteen eighty-eight, became the core of the Coq proof assistant, later "
            "extended with inductive types. <bookmark mark='b'/> Around the core sits a large, clever, untrusted "
            "layer: tactics, automation, and an elaborator that fills in what the user leaves out. Its only output "
            "is a proof term. <bookmark mark='c'/> The kernel, a small type checker, checks that term, and only the "
            "kernel has to be right. <bookmark mark='d'/> It is the idea of Part 54's small trusted kernel again, and "
            "a kernel like this one checks the proof of Part 54's verified compiler, CompCert."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hist[0]))
            vo.wait_until("b")
            self.play(FadeIn(user), GrowArrow(ua), FadeIn(big))
            self.play(GrowArrow(a1), FadeIn(a1l))
            vo.wait_until("c")
            self.play(FadeIn(ker))
            self.add(dot)
            self.play(dot.animate.move_to(ker.get_center()), run_time=0.9)
            self.play(FadeOut(dot), Flash(ker.get_center(), color=YES, flash_radius=0.9), GrowArrow(a2), FadeIn(ok))
            vo.wait_until("d")
            self.play(FadeIn(hist[1]), Circumscribe(ker, color=YES))
        self.wait(0.6)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
