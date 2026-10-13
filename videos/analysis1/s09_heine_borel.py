from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import endpoint
from videos.analysis1.s07_open_closed import nbhd


class HeineBorel(VoiceoverScene):
    def construct(self):
        self.card()
        self.cells()
        self.hunt()
        self.theorem()
        self.weierstrass()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Heine--Borel, by bisection", r"Which subsets of $\R^k$ are compact?", lit=(1895,), part=1)
        with self.voiceover(
            "Chapter eight. Which subsets of the line, or of k-dimensional space, are compact? The proof uses the "
            "bisection engine from chapter three."
        ) as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cells(self):
        S = 5.6
        o = np.array([-6.3, -3.1, 0])

        def P(u, v):
            return o + np.array([u * S, v * S, 0])

        box = Square(side_length=S, color=C.COMPACT_SET, stroke_width=3).move_to(P(0.5, 0.5))
        stmt = VGroup(label(r"\textbf{Theorem} (Rudin 2.40)", font_size=28, color=GREY_A),
                      label(r"Every $k$-cell", font_size=32),
                      MathTex(r"I = [a_1, b_1] \times \cdots \times [a_k, b_k]", font_size=34),
                      label(r"is compact.", font_size=32)).arrange(DOWN, buff=0.15)
        stmt.move_to([3.6, 2.2, 0])
        target = np.array([0.6234, 0.3711])
        steps = VGroup(
            label(r"suppose some open cover of $I$ has no finite subcover", font_size=25),
            label(r"cut $I$ into $2^k$ pieces: if each had a finite subcover,", font_size=25),
            label(r"so would $I$; so one of them has none", font_size=25),
            label(r"repeat: nested cells, diameters $\delta / 2^n$,", font_size=25),
            label(r"shrinking to a single point $x^*$", font_size=25),
        )
        for s_ in steps:
            s_.set_max_width(6.0)
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.75, -0.6, 0])
        tag = schematic_tag(corner=DL)
        with self.voiceover(
            "The basic compact set is a box: a product of closed intervals, which Rudin calls a k-cell. <bookmark mark='t'/> "
            "Every k-cell is compact. Here's the square, with k equal to two. <bookmark mark='s'/> Suppose, to get a "
            "contradiction, that some open cover of it has no finite subcover. <bookmark mark='c'/> Cut the square into "
            "four quarters. If each quarter could be covered by finitely many of the open sets, so could the whole square. "
            "So at least one quarter can't."
        ) as vo:
            self.play(Create(box), FadeIn(tag))
            vo.wait_until("t")
            self.play(FadeIn(stmt))
            vo.wait_until("s")
            self.play(FadeIn(steps[0]))
            vo.wait_until("c")
            self.play(FadeIn(steps[1:3]))
        lo, hi = np.array([0.0, 0.0]), np.array([1.0, 1.0])
        cells = VGroup()
        bad = None
        with self.voiceover(
            "<bookmark mark='a'/> Keep that bad quarter, and cut it into four again. One of those has no finite "
            "subcover either. And so on. <bookmark mark='p'/> We get nested squares, each half the width of the last, "
            "and by the nested-cell version of chapter three's theorem, they close in on a single point, call it x star."
        ) as vo:
            vo.wait_until("a")
            for k in range(7):
                mid = (lo + hi) / 2
                lines = VGroup(Line(P(mid[0], lo[1]), P(mid[0], hi[1]), color=GREY_B, stroke_width=1.5),
                               Line(P(lo[0], mid[1]), P(hi[0], mid[1]), color=GREY_B, stroke_width=1.5))
                q = (target >= mid).astype(int)
                nlo = np.where(q, mid, lo)
                nhi = np.where(q, hi, mid)
                sq = Polygon(P(nlo[0], nlo[1]), P(nhi[0], nlo[1]), P(nhi[0], nhi[1]), P(nlo[0], nhi[1]),
                             stroke_color=C.PATHOLOGY, stroke_width=3, fill_color=C.PATHOLOGY, fill_opacity=0.18)
                self.play(Create(lines), run_time=0.35 if k > 2 else 0.6)
                if bad is None:
                    bad = sq
                    self.play(FadeIn(bad), run_time=0.4)
                else:
                    self.play(Transform(bad, sq), run_time=0.4)
                cells.add(lines)
                lo, hi = nlo, nhi
            vo.wait_until("p")
            self.play(FadeIn(steps[3:]))
        xs = Dot(P(*target), radius=0.07, color=WHITE)
        xsl = MathTex(r"x^*", font_size=34).next_to(xs, UR, buff=0.05)
        disk = nbhd(P(*target), 0.55, color=C.OPEN_SET, fill=0.2, width=3)
        dl = MathTex(r"G_\alpha \supset N_r(x^*)", font_size=30, color=C.OPEN_SET).next_to(disk, DOWN, buff=0.12)
        fin = label(r"once $\delta / 2^n < r$, the $n$-th cell lies in the single set $G_\alpha$: \ contradiction",
                    font_size=26, color=C.PATHOLOGY).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "<bookmark mark='x'/> x star is in the square, so it's in one of the open sets of the cover, call it G "
            "alpha, <bookmark mark='g'/> and since G alpha is open, it contains a whole disk around x star. <bookmark mark='f'/> "
            "But the nested squares get as small as we like, so eventually one of them fits inside that disk, and a "
            "single open set covers it. That's a finite subcover of a square that supposedly had none. Contradiction."
        ) as vo:
            vo.wait_until("x")
            self.play(FadeIn(xs, scale=2), FadeIn(xsl))
            vo.wait_until("g")
            self.play(FadeIn(disk, scale=0.3), FadeIn(dl))
            vo.wait_until("f")
            self.play(Indicate(bad, color=C.PATHOLOGY, scale_factor=1.8), FadeIn(fin))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hunt(self):
        X = lambda v: -5.6 + v * 11.2  # noqa: E731
        y0 = -1.6
        seg = VGroup(Line([X(0), y0, 0], [X(1), y0, 0], color=GREY_A, stroke_width=7),
                     endpoint([X(0), y0, 0], False, GREY_A), Dot([X(1), y0, 0], radius=0.075, color=GREY_A))
        lab = MathTex(r"(0, 1], \text{ covered by } \Big(\frac1n,\ 2\Big)", font_size=36).to_edge(UP, buff=0.6)
        expl = label(r"Run the same hunt on a set that is \emph{not} closed:", font_size=30, color=GREY_A)
        expl.next_to(lab, DOWN, buff=0.3)
        bars = VGroup()
        lo, hi = 0.0, 1.0
        rows = VGroup()
        for k in range(7):
            mid = (lo + hi) / 2
            y = y0 + 0.55 + 0.38 * k
            left = VGroup(Line([X(lo), y, 0], [X(mid), y, 0], color=C.PATHOLOGY, stroke_width=6))
            right = VGroup(Line([X(mid), y, 0], [X(hi), y, 0], color=C.CONNECTED_SET, stroke_width=6))
            rows.add(VGroup(left, right))
            hi = mid
        notes = VGroup(label(r"right half: finitely many $(\tfrac1n, 2)$ cover it", font_size=26, color=C.CONNECTED_SET),
                       label(r"left half: no finite subcover \ $\Rightarrow$ keep hunting", font_size=26, color=C.PATHOLOGY)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35).shift(RIGHT * 2.5)
        zero = VGroup(Circle(radius=0.14, color=C.HOLE, stroke_width=4).move_to([X(0), y0, 0]),
                      label(r"the hunt ends at $0$, \\ which is not in the set", font_size=26, color=C.HOLE)
                      .move_to([X(0) + 1.6, y0 - 1.0, 0]))
        with self.voiceover(
            "To see what the proof really used, <bookmark mark='r'/> run the same hunt on the half-open interval from zero "
            "to one, with the cover from chapter seven. <bookmark mark='h'/> Split it in half. The right half is covered "
            "by finitely many of the sets, but the left half isn't. Split the left half again, and again: <bookmark mark='z'/> "
            "the hunt for the place where the cover fails closes in on zero. <bookmark mark='m'/> And zero is not in the "
            "set. That's the only step that breaks: in a closed box, the point the hunt finds belongs to the box, and an "
            "open set swallows everything near it."
        ) as vo:
            self.play(FadeIn(seg), Write(lab))
            vo.wait_until("r")
            self.play(FadeIn(expl))
            vo.wait_until("h")
            self.play(FadeIn(rows[0]), FadeIn(notes))
            vo.wait_until("z")
            for r_ in rows[1:]:
                self.play(FadeIn(r_), run_time=0.45)
            vo.wait_until("m")
            self.play(Create(zero[0]), FadeIn(zero[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        head = VGroup(label(r"\textbf{Heine--Borel} (Rudin 2.41) \ For $E \subset \R^k$, these are equivalent:", font_size=30))
        head.to_edge(UP, buff=0.45)
        a = label(r"(a) \ $E$ is closed and bounded", font_size=30)
        b = label(r"(b) \ $E$ is compact", font_size=30, color=C.COMPACT_SET)
        c = label(r"(c) \ every infinite subset of $E$ has a limit point in $E$", font_size=30)
        a.move_to([-3.8, 1.2, 0])
        b.move_to([3.8, 1.2, 0])
        c.move_to([0, -1.2, 0])
        ab = Arrow(a.get_right(), b.get_left(), buff=0.25, color=GREY_B)
        bc = Arrow(b.get_bottom(), c.get_top() + RIGHT * 2.0, buff=0.25, color=GREY_B)
        ca = Arrow(c.get_top() + LEFT * 2.0, a.get_bottom(), buff=0.25, color=GREY_B)
        ab_l = label(r"inside a $k$-cell; closed subset of compact (2.35)", font_size=22, color=GREY_A).next_to(ab, UP, buff=0.1)
        bc_l = label(r"2.37", font_size=24, color=GREY_A).next_to(bc, RIGHT, buff=0.1)
        ca_l = VGroup(label(r"not bounded: $|x_n| > n$ escapes", font_size=22, color=GREY_A),
                      label(r"not closed: $x_n \to x_0 \notin E$", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.08)
        ca_l.next_to(ca, LEFT, buff=0.1)
        with self.voiceover(
            "Now we can say exactly which subsets of k-dimensional space are compact. <bookmark mark='h'/> The "
            "Heine–Borel theorem says three properties are equivalent. <bookmark mark='a'/> Closed and bounded; "
            "<bookmark mark='b'/> compact; <bookmark mark='c'/> and every infinite subset has a limit point inside the set."
        ) as vo:
            self.play(FadeIn(head))
            for mk, m in zip("abc", (a, b, c)):
                vo.wait_until(mk)
                self.play(FadeIn(m))
        with self.voiceover(
            "<bookmark mark='x'/> Closed and bounded gives compact: a bounded set sits inside some box, which is compact, "
            "and a closed subset of a compact set is compact. <bookmark mark='y'/> Compact gives the limit-point property, "
            "as we saw last chapter. <bookmark mark='z'/> And if a set is not bounded, points marching off to infinity "
            "form an infinite subset with no limit point; if it's not closed, points crowding toward a missing limit "
            "point form an infinite subset whose only limit point is outside the set. So the third property forces the "
            "first."
        ) as vo:
            vo.wait_until("x")
            self.play(GrowArrow(ab), FadeIn(ab_l))
            vo.wait_until("y")
            self.play(GrowArrow(bc), FadeIn(bc_l))
            vo.wait_until("z")
            self.play(GrowArrow(ca), FadeIn(ca_l))
        warn = VGroup(label(r"(b) $\iff$ (c) holds in every metric space.", font_size=28, color=GREY_A),
                      label(r"(a) $\Rightarrow$ (b) is special to $\R^k$: \ chapter 11 breaks it.", font_size=28,
                            color=C.PATHOLOGY)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "One warning, which will matter at the end of this video. <bookmark mark='w'/> Compact and the limit-point "
            "property are equivalent in every metric space. But closed and bounded implies compact only in k-dimensional "
            "space, because the proof needed boxes, and bisection, and finitely many coordinates."
        ) as vo:
            vo.wait_until("w")
            self.play(FadeIn(warn))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def weierstrass(self):
        n = np.arange(1, 100001)
        pts = np.stack([np.cos(n), np.sin(np.sqrt(2) * n)], 1)
        side = 5.6
        o = np.array([-3.4, -0.4, 0])

        def make_view(lo, hi, cnt=100000):
            sel = np.all((pts[:cnt] >= lo) & (pts[:cnt] <= hi), axis=1)
            P = pts[:cnt][sel]
            u = (P - lo) / (hi - lo)
            dots = VGroup(*[Dot(o + np.array([(x - 0.5) * side, (y - 0.5) * side, 0]), radius=0.022, color=C.SEQ)
                            for x, y in u[:1500]])
            return dots, sel.sum()

        frame = Square(side_length=side, color=C.COMPACT_SET, stroke_width=3).move_to(o)
        stmt = VGroup(label(r"\textbf{Bolzano--Weierstrass} (Rudin 2.42)", font_size=28, color=GREY_A),
                      label(r"Every bounded infinite subset of $\R^k$", font_size=30),
                      label(r"has a limit point in $\R^k$.", font_size=30)).arrange(DOWN, buff=0.12)
        stmt.move_to([3.6, 2.2, 0])
        seqn = MathTex(r"x_n = (\cos n,\ \sin \sqrt2\, n)", font_size=34, color=C.SEQ).move_to([3.6, 0.6, 0])
        lo, hi = np.array([-1.0, -1.0]), np.array([1.0, 1.0])
        dots, cnt = make_view(lo, hi)
        count = MathTex(rf"\text{{in view: }} {fmt_int(cnt)}", font_size=30).move_to([3.6, -0.3, 0])
        of = label(r"(of the first $100{,}000$ points; at most $1{,}500$ drawn)", font_size=22, color=GREY_B)
        of.move_to([3.6, -1.5, 0])
        zl = MathTex(r"\text{zoom } \times 1", font_size=30, color=GREY_A).move_to([3.6, -0.9, 0])
        with self.voiceover(
            "A corollary that we'll use constantly in Part 2. <bookmark mark='s'/> Every bounded infinite set in "
            "k-dimensional space has a limit point. <bookmark mark='e'/> Here are points of the sequence cosine "
            "of n, sine of root two times n, all inside a square: up to fifteen hundred of the first hundred "
            "thousand."
        ) as vo:
            self.play(Create(frame))
            vo.wait_until("s")
            self.play(FadeIn(stmt))
            vo.wait_until("e")
            self.play(FadeIn(seqn), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.0005), FadeIn(count), FadeIn(zl), FadeIn(of),
                      run_time=2)
        with self.voiceover(
            "The proof is bisection once more. <bookmark mark='q'/> Cut the square into quarters; at least one contains "
            "infinitely many of the points. Zoom into it, and repeat. The quarters shrink to a point, and every disk "
            "around that point contains infinitely many points of the set: a limit point. <bookmark mark='c'/> In "
            "sequence language: every bounded sequence has a convergent subsequence."
        ) as vo:
            vo.wait_until("q")
            for k in range(4):
                mid = (lo + hi) / 2
                best = None
                for qx in (0, 1):
                    for qy in (0, 1):
                        nlo = np.array([lo[0] if qx == 0 else mid[0], lo[1] if qy == 0 else mid[1]])
                        nhi = np.array([mid[0] if qx == 0 else hi[0], mid[1] if qy == 0 else hi[1]])
                        c_ = np.all((pts >= nlo) & (pts <= nhi), axis=1).sum()
                        if best is None or c_ > best[0]:
                            best = (c_, nlo, nhi, qx, qy)
                _, nlo, nhi, qx, qy = best
                quarter = Square(side_length=side / 2, color=C.EPS, stroke_width=4).move_to(
                    o + np.array([(qx - 0.5) * side / 2, (qy - 0.5) * side / 2, 0]))
                self.play(Create(quarter), run_time=0.5)
                lo, hi = nlo, nhi
                nd, cnt = make_view(lo, hi)
                count2 = MathTex(rf"\text{{in view: }} {fmt_int(cnt)}", font_size=30).move_to([3.6, -0.3, 0])
                zl2 = MathTex(rf"\text{{zoom }} \times {2 ** (k + 1)}", font_size=30, color=GREY_A).move_to([3.6, -0.9, 0])
                self.play(FadeOut(quarter), FadeOut(dots), FadeIn(nd), FadeTransform(count, count2),
                          FadeTransform(zl, zl2), run_time=0.8)
                count, zl = count2, zl2
                dots = nd
                assert cnt > 0
            vo.wait_until("c")
            cor = label(r"Every bounded sequence in $\R^k$ has a convergent subsequence.", font_size=28, color=C.EPS)
            cor.to_edge(DOWN, buff=0.45)
            self.play(FadeIn(cor))
        self.wait(0.5)
        self.clear_scene()
