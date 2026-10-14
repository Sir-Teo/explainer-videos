from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import endpoint
from videos.analysis1.s07_open_closed import blob_pts, nbhd


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
        tag = schematic_tag(corner=UL).to_corner(UL, buff=0.45)
        # "some open cover": a 5 x 5 grid of open disks, each a little bigger than its grid cell
        cov_c = [((i + 0.5) / 5, (j + 0.5) / 5) for i in range(5) for j in range(5)]
        cov_r = 0.8 / 5
        samp = np.random.default_rng(0).uniform(0, 1, (4000, 2))
        assert all(any(np.hypot(*(q - np.array(c))) < cov_r for c in cov_c) for q in samp)  # it covers the square
        cover = VGroup(*[nbhd(P(*c), cov_r * S, color=C.OPEN_SET, fill=0.06, width=2, dashes=24) for c in cov_c])
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
            self.play(FadeIn(steps[0]), LaggedStart(*[FadeIn(d_) for d_ in cover], lag_ratio=0.04), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(steps[1:3]), cover.animate.set_opacity(0.3))
        lo, hi = np.array([0.0, 0.0]), np.array([1.0, 1.0])
        cells = VGroup()
        bad = None
        # after the fourth cut the cell is too small to follow: an inset magnifies it (x 8) in the empty upper half
        mag, K_IN = 8, 3
        in_c = np.array([-3.6, 1.1, 0])
        inset = None
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
                anims = [Create(lines)]
                if inset is not None:
                    # the same cut, magnified
                    def M(u, v):
                        return in_c + (np.array([u, v, 0]) - np.array([*w_mid, 0])) * S * mag
                    anims.append(Create(VGroup(Line(M(mid[0], lo[1]), M(mid[0], hi[1]), color=GREY_B, stroke_width=2),
                                               Line(M(lo[0], mid[1]), M(hi[0], mid[1]), color=GREY_B, stroke_width=2))))
                self.play(*anims, run_time=0.35 if k > 2 else 0.6)
                if bad is None:
                    bad = sq
                    self.play(FadeIn(bad), run_time=0.4)
                else:
                    anims = [Transform(bad, sq)]
                    if inset is not None:
                        anims.append(Transform(in_bad, Polygon(M(nlo[0], nlo[1]), M(nhi[0], nlo[1]), M(nhi[0], nhi[1]),
                                                               M(nlo[0], nhi[1]), stroke_color=C.PATHOLOGY, stroke_width=3,
                                                               fill_color=C.PATHOLOGY, fill_opacity=0.18)))
                    self.play(*anims, run_time=0.4)
                cells.add(lines)
                lo, hi = nlo, nhi
                if k == K_IN:
                    w_lo, w_hi = lo.copy(), hi.copy()
                    w_mid = (w_lo + w_hi) / 2
                    side_in = (w_hi[0] - w_lo[0]) * S * mag
                    assert abs(side_in - S / 16 * mag) < 1e-9 and abs(side_in - 2.8) < 1e-9
                    src = Square(side_length=(w_hi[0] - w_lo[0]) * S, color=GREY_B, stroke_width=2).move_to(P(*w_mid))
                    frame = Square(side_length=side_in, color=GREY_B, stroke_width=2).move_to(in_c)
                    frame.set_fill(BACKGROUND, 1)
                    links = VGroup(Line(src.get_corner(UL), frame.get_corner(UL), color=GREY_B, stroke_width=1.5),
                                   Line(src.get_corner(UR), frame.get_corner(UR), color=GREY_B, stroke_width=1.5))
                    in_bad = Square(side_length=side_in, stroke_color=C.PATHOLOGY, stroke_width=3,
                                    fill_color=C.PATHOLOGY, fill_opacity=0.18).move_to(in_c)
                    in_tag = MathTex(rf"\times {mag}", font_size=24, color=GREY_B).next_to(frame, UP, buff=0.08)
                    in_tag.align_to(frame, RIGHT)
                    inset = VGroup(links, frame, in_bad, in_tag)
                    self.play(Create(src), FadeIn(frame), Create(links), FadeIn(in_bad), FadeIn(in_tag), run_time=0.8)
            vo.wait_until("p")
            self.play(FadeIn(steps[3:]))
        xs = Dot(P(*target), radius=0.07, color=WHITE)
        xsl = MathTex(r"x^*", font_size=34).next_to(xs, DR, buff=0.05)
        xs_in = Dot(in_c + (np.array([*target, 0]) - np.array([*w_mid, 0])) * S * mag, radius=0.07, color=WHITE)
        assert np.all(np.abs(xs_in.get_center() - in_c)[:2] < side_in / 2)  # x* is inside the magnified cell
        disk = nbhd(P(*target), 0.55, color=C.OPEN_SET, fill=0.2, width=3)
        dl = MathTex(r"G_\alpha \supset N_r(x^*)", font_size=30, color=C.OPEN_SET).next_to(disk, DOWN, buff=0.12)
        fin = label(r"once $\delta / 2^n < r$, the $n$-th cell lies in the single set $G_\alpha$: \ contradiction",
                    font_size=26, color=C.PATHOLOGY).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "<bookmark mark='x'/> x star is in the square, so it's in one of the open sets of the cover, call it G "
            "alpha, <bookmark mark='g'/> and since G alpha is open, it contains a whole disk around x star. <bookmark mark='f'/> "
            "But the nested squares get as small as we like, so eventually one of them fits inside that disk, and a "
            "single open set covers it. That's a finite subcover of a square that supposedly had none. Contradiction."
        ) as vo:
            vo.wait_until("x")
            self.play(FadeIn(xs, scale=2), FadeIn(xsl), FadeIn(xs_in, scale=2))
            vo.wait_until("g")
            self.play(FadeIn(disk, scale=0.3), FadeIn(dl), FadeOut(cover))
            vo.wait_until("f")
            self.play(Indicate(in_bad, color=C.PATHOLOGY, scale_factor=1.15), FadeIn(fin))
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
            right = VGroup(Line([X(mid), y, 0], [X(hi), y, 0], color=C.COMPACT_SET, stroke_width=6))
            rows.add(VGroup(left, right))
            hi = mid
        notes = VGroup(label(r"right half: finitely many $(\tfrac1n, 2)$ cover it", font_size=26, color=C.COMPACT_SET),
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
        head = VGroup(label(r"\textbf{Heine--Borel} (Rudin 2.41)", font_size=28, color=GREY_A),
                      label(r"For $E \subset \R^k$, these are equivalent:", font_size=32)).arrange(DOWN, buff=0.12)
        head.to_edge(UP, buff=0.4)
        a = label(r"(a) \ $E$ is closed and bounded", font_size=30)
        b = label(r"(b) \ $E$ is compact", font_size=30, color=C.COMPACT_SET)
        c = VGroup(label(r"(c) \ every infinite subset of $E$", font_size=30),
                   label(r"has a limit point in $E$", font_size=30)).arrange(DOWN, buff=0.1)
        a.move_to([-3.8, 1.75, 0])
        b.move_to([3.8, 1.75, 0])
        c.move_to([0, -0.85, 0])
        ta, tb, tc = self.thumb("a").move_to([-3.8, 0.62, 0]), self.thumb("b").move_to([3.8, 0.62, 0]), \
            self.thumb("c").move_to([0, -2.05, 0])
        ab = Arrow(a.get_right(), b.get_left(), buff=0.25, color=GREY_B)
        bc = Arrow(tb.get_bottom(), c.get_top() + RIGHT * 2.0, buff=0.15, color=GREY_B)
        ca = Arrow(c.get_top() + LEFT * 2.0, ta.get_bottom(), buff=0.15, color=GREY_B)
        ab_l = VGroup(label(r"inside a $k$-cell;", font_size=22, color=GREY_A),
                      label(r"closed subset of compact (2.35)", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.06)
        ab_l.next_to(ab, UP, buff=0.1)
        bc_l = label(r"2.37", font_size=24, color=GREY_A).next_to(bc, RIGHT, buff=0.1)
        # (c) forces (a): the two ways a set can fail it, drawn small beside their captions
        esc = VGroup(*[Dot([0.08 * 1.6 ** k, 0, 0], radius=0.04, color=C.SEQ) for k in range(5)])
        esc.add(Arrow(esc[-1].get_center(), esc[-1].get_center() + RIGHT * 0.3, buff=0.06, color=C.SEQ,
                      stroke_width=2.5, tip_length=0.1))
        crowd_ring = endpoint(ORIGIN, False, C.HOLE, radius=0.06)
        crowd = VGroup(*[Dot(LEFT * 0.75 * 0.55 ** k, radius=0.035, color=C.SEQ) for k in range(6)], crowd_ring)
        cap1 = label(r"not bounded: they escape", font_size=22, color=GREY_A)
        cap2 = label(r"not closed: $x_n \to x_0 \notin E$", font_size=22, color=GREY_A)
        ca_l = VGroup(VGroup(esc, cap1).arrange(RIGHT, buff=0.25), VGroup(crowd, cap2).arrange(RIGHT, buff=0.25))
        ca_l.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ca_l.move_to([0, -1.95, 0]).align_to([-2.45, 0, 0], RIGHT)
        assert ca_l.get_left()[0] > -6.7
        with self.voiceover(
            "Now we can say exactly which subsets of k-dimensional space are compact. <bookmark mark='h'/> The "
            "Heine–Borel theorem says three properties are equivalent. <bookmark mark='a'/> Closed and bounded; "
            "<bookmark mark='b'/> compact; <bookmark mark='c'/> and every infinite subset has a limit point inside the set."
        ) as vo:
            self.play(FadeIn(head))
            for mk, m, t in zip("abc", (a, b, c), (ta, tb, tc)):
                vo.wait_until(mk)
                self.play(FadeIn(m), FadeIn(t, shift=UP * 0.15))
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
            self.play(GrowArrow(ca), FadeIn(ca_l[0]))
            self.play(FadeIn(ca_l[1]))
        warn = VGroup(label(r"(b) $\iff$ (c) holds in every metric space.", font_size=28, color=GREY_A),
                      label(r"(a) $\Rightarrow$ (b) is special to $\R^k$: \ chapter 11 breaks it.", font_size=28,
                            color=C.PATHOLOGY)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "One warning, which will matter at the end of this video. <bookmark mark='w'/> Compact and the limit-point "
            "property are equivalent in every metric space. But closed and bounded implies compact only in k-dimensional "
            "space, because the proof needed boxes, and bisection, and finitely many coordinates."
        ) as vo:
            vo.wait_until("w")
            self.play(FadeIn(warn))
        self.wait(0.4)
        self.clear_scene()

    @staticmethod
    def thumb(kind: str) -> VGroup:
        """1.8 x 1.1 pictures of (a) closed and bounded, (b) compact (covered by finitely many disks),
        (c) an infinite subset piling up at a point of the set."""
        pts = blob_pts(ORIGIN, scale=0.27, n=200)
        if kind == "a":
            blob = Polygon(*pts, stroke_color=C.CLOSED_SET, stroke_width=2.5, fill_color=C.CLOSED_SET, fill_opacity=0.2)
            frame = DashedVMobject(SurroundingRectangle(blob, buff=0.12, stroke_width=2, color=GREY_B), num_dashes=30)
            return VGroup(blob, frame)
        blob = Polygon(*pts, stroke_color=C.COMPACT_SET, stroke_width=2.5, fill_color=C.COMPACT_SET, fill_opacity=0.2)
        if kind == "b":
            cs = [np.array([np.cos(t), np.sin(t), 0]) * 0.3 for t in np.linspace(0, 2 * np.pi, 5, endpoint=False)]
            r = 0.32
            fill = np.array([t * p for p in pts for t in np.linspace(0, 1, 8)])
            assert all(any(np.linalg.norm(q - c) < r for c in cs) for q in fill)  # five disks cover the blob
            disks = VGroup(*[DashedVMobject(Circle(radius=r, color=C.OPEN_SET, stroke_width=2).move_to(c), num_dashes=16)
                             for c in cs])
            return VGroup(blob, disks)
        lim = np.array([0.12, -0.05, 0])
        dots = VGroup(*[Dot(lim + 0.4 * 0.75 ** k * np.array([np.cos(2.3 * k), np.sin(2.3 * k), 0]), radius=0.03,
                            color=C.SEQ) for k in range(14)])
        return VGroup(blob, dots, Dot(lim, radius=0.05, color=WHITE))

    # ------------------------------------------------------------------
    def weierstrass(self):
        n = np.arange(1, 100001)
        pts = np.stack([np.cos(n), np.sin(np.sqrt(2) * n)], 1)
        side = 5.3
        o = np.array([-3.4, -0.1, 0])

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
        # a locator: where the current view sits in the original square
        loc_s, loc_c = 1.1, np.array([6.0, -0.6, 0])
        loc = Square(side_length=loc_s, color=GREY_B, stroke_width=2).move_to(loc_c)

        def loc_box(lo_, hi_):
            c_ = loc_c + np.array([((lo_ + hi_) / 2 + 1)[0] / 2 - 0.5, ((lo_ + hi_) / 2 + 1)[1] / 2 - 0.5, 0]) * loc_s
            return Square(side_length=(hi_ - lo_)[0] / 2 * loc_s, color=C.EPS, stroke_width=2).move_to(c_)
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
                      Create(loc), run_time=2)
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
                          FadeTransform(zl, zl2), Create(loc_box(nlo, nhi)), run_time=0.8)
                count, zl = count2, zl2
                dots = nd
                assert cnt > 0
            # where the quarters close in: keep halving (with a million points) and mark the point they pin down
            many = np.stack([np.cos(np.arange(1, 1000001)), np.sin(np.sqrt(2) * np.arange(1, 1000001))], 1)
            plo, phi = lo.copy(), hi.copy()
            for _ in range(5):
                pm = (plo + phi) / 2
                cand = []
                for qx in (0, 1):
                    for qy in (0, 1):
                        nlo_ = np.array([plo[0] if qx == 0 else pm[0], plo[1] if qy == 0 else pm[1]])
                        nhi_ = np.array([pm[0] if qx == 0 else phi[0], pm[1] if qy == 0 else phi[1]])
                        cand.append((np.all((many >= nlo_) & (many <= nhi_), axis=1).sum(), nlo_, nhi_))
                cnt_, plo, phi = max(cand, key=lambda t: t[0])
                assert cnt_ > 0
            lp = (plo + phi) / 2
            u_ = (lp - lo) / (hi - lo)
            assert np.all((u_ > 0) & (u_ < 1))  # the point lies inside the current view
            lp_s = o + np.array([(u_[0] - 0.5) * side, (u_[1] - 0.5) * side, 0])
            lp_d = Dot(lp_s, radius=0.07, color=WHITE)
            lp_disk = DashedVMobject(Circle(radius=0.45, color=WHITE, stroke_width=2.5).move_to(lp_s), num_dashes=28)
            lp_l = label(r"limit point", font_size=26).next_to(lp_disk, UP if u_[1] < 0.7 else DOWN, buff=0.08)
            lp_l.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.05)
            self.play(FadeIn(lp_d, scale=2), Create(lp_disk), FadeIn(lp_l))
            vo.wait_until("c")
            cor = label(r"Every bounded sequence in $\R^k$ has a convergent subsequence.", font_size=28, color=C.EPS)
            cor.to_edge(DOWN, buff=0.4)
            self.play(FadeIn(cor))
        self.wait(0.5)
        self.clear_scene()
