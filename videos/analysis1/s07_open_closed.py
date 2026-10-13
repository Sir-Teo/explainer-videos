from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import endpoint


def blob_pts(center, scale=1.0, n=400):
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = scale * (1.55 + 0.28 * np.cos(3 * th) + 0.16 * np.sin(2 * th + 0.4))
    return np.stack([center[0] + r * np.cos(th), center[1] + r * np.sin(th), np.zeros(n)], 1)


def nbhd(p, r, color=C.OPEN_SET, fill=0.12, width=2.5, dashes=36):
    c = Circle(radius=r).move_to(p).set_fill(color, fill).set_stroke(width=0)
    e = DashedVMobject(Circle(radius=r, color=color, stroke_width=width).move_to(p), num_dashes=dashes)
    return VGroup(c, e)


class OpenClosed(VoiceoverScene):
    def construct(self):
        self.card()
        self.definitions()
        self.balls_open()
        self.complements()
        self.unions()
        self.table()
        self.closure()
        self.relative()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"Open and closed sets", r"Which points have wiggle room?", part=1)
        with self.voiceover(
            "Chapter six. With a distance in hand, we can describe the shape of a set in terms of which points have "
            "wiggle room."
        ) as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def definitions(self):
        c0 = np.array([-3.6, -0.3, 0])
        pts = blob_pts(c0)
        E = Polygon(*pts, stroke_width=0, fill_color=C.SEQ, fill_opacity=0.28)
        edge = Polygon(*pts, color=C.SEQ, stroke_width=2.5)
        iso = Dot(c0 + np.array([2.55, 1.85, 0]), radius=0.07, color=C.SEQ)
        El = MathTex(r"E", font_size=40, color=C.SEQ).move_to(c0 + np.array([0.75, -0.45, 0]))
        defs = VGroup(
            MathTex(r"N_r(p) = \{\, q : d(p,q) < r \,\}", font_size=32, color=C.OPEN_SET),
            label(r"$p$ is an \textbf{interior point} of $E$: \ some $N_r(p) \subset E$", font_size=26),
            label(r"$E$ is \textbf{open}: \ every point of $E$ is interior", font_size=26, color=C.OPEN_SET),
            label(r"$p$ is a \textbf{limit point} of $E$: \ every $N_r(p)$ contains", font_size=26),
            label(r"\qquad some $q \in E$ with $q \neq p$", font_size=26),
            label(r"$E$ is \textbf{closed}: \ it contains all its limit points", font_size=26, color=C.CLOSED_SET),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.35, 0.3, 0])
        ref = note(r"Rudin 2.18").next_to(defs, DOWN, buff=0.2).align_to(defs, RIGHT)
        with self.voiceover(
            "Here's a set E in the plane, <bookmark mark='n'/> and here's the basic tool: the neighborhood of radius r "
            "around a point p, all the points at distance less than r. A disk, with its edge left out, which is why it's "
            "dashed."
        ) as vo:
            self.play(FadeIn(E), Create(edge), FadeIn(iso), FadeIn(El))
            vo.wait_until("n")
            self.play(FadeIn(defs[0]))
        p_in = c0 + np.array([-0.35, 0.45, 0])
        n_in = nbhd(p_in, 0.55)
        d_in = Dot(p_in, radius=0.06)
        ok = label(r"interior", font_size=26, color=C.CONNECTED_SET).next_to(n_in, DOWN, buff=0.1)
        b_idx = 300  # the bottom of the blob
        p_b = pts[b_idx]
        d_b = Dot(p_b, radius=0.07, color=C.CLOSED_SET)
        n_bs = [nbhd(p_b, r) for r in (0.6, 0.35, 0.18)]
        bl = label(r"boundary: every disk pokes out", font_size=24, color=C.CLOSED_SET).next_to(p_b, DOWN, buff=0.75)
        with self.voiceover(
            "A point is interior if some neighborhood of it fits entirely inside E: <bookmark mark='i'/> this one does, "
            "with room to spare. <bookmark mark='o'/> A set is open if every one of its points is interior. "
            "<bookmark mark='b'/> A point on the edge fails the test: however small the disk, it pokes outside."
        ) as vo:
            vo.wait_until("i")
            self.play(FadeIn(d_in), FadeIn(n_in, scale=0.5), FadeIn(defs[1]))
            self.play(FadeIn(ok))
            vo.wait_until("o")
            self.play(FadeIn(defs[2]))
            vo.wait_until("b")
            self.play(FadeIn(d_b, scale=2), FadeIn(n_bs[0]), FadeIn(bl))
            self.play(Transform(n_bs[0], n_bs[1]))
            self.play(Transform(n_bs[0], n_bs[2]))
        with self.voiceover(
            "<bookmark mark='l'/> The edge point is, however, a limit point of E: every disk around it, however small, "
            "catches points of E other than itself. <bookmark mark='c'/> A set is closed if it contains all of its limit "
            "points. <bookmark mark='s'/> This isolated point, by contrast, belongs to E but isn't a limit point: a "
            "small enough disk around it contains no other point of E."
        ) as vo:
            vo.wait_until("l")
            self.play(FadeIn(defs[3:5]))
            vo.wait_until("c")
            self.play(FadeIn(defs[5]), FadeIn(ref))
            vo.wait_until("s")
            n_iso = nbhd(iso.get_center(), 0.3, color=C.SEQ)
            self.play(FadeIn(n_iso, scale=0.5), Indicate(iso, color=C.SEQ))
        q_ = label(r"Is $E$ open? Closed? \ Neither: it contains some edge points and misses others.", font_size=26,
                   color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Notice that open and closed are not opposites. <bookmark mark='q'/> If E contains some of its edge points but "
            "not others, it's neither. And some sets are both, like the whole plane."
        ) as vo:
            vo.wait_until("q")
            self.play(FadeIn(q_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def balls_open(self):
        p = np.array([-3.4, -0.4, 0])
        R = 2.2
        big = nbhd(p, R, dashes=60)
        pd = Dot(p, radius=0.07)
        pl = MathTex(r"p", font_size=34).next_to(pd, DL, buff=0.08)
        q = p + np.array([1.05, 0.65, 0])
        dq = np.linalg.norm(q - p)
        h = R - dq
        qd = Dot(q, radius=0.07, color=C.SEQ)
        ql = MathTex(r"q", font_size=34, color=C.SEQ).next_to(qd, DOWN, buff=0.12)
        small = nbhd(q, h, color=C.EPS, fill=0.15, dashes=30)
        s = q + h * 0.7 * np.array([np.cos(0.4), np.sin(0.4), 0])
        sd = Dot(s, radius=0.06, color=C.EPS)
        sl = MathTex(r"s", font_size=32, color=C.EPS).next_to(sd, UR, buff=0.05)
        pq = Line(p, q, color=GREY_B, stroke_width=2)
        qs = Line(q, s, color=C.EPS, stroke_width=2)
        stmt = VGroup(label(r"\textbf{Theorem} (Rudin 2.19)", font_size=28, color=GREY_A),
                      label(r"Every neighborhood is an open set.", font_size=32)).arrange(DOWN, buff=0.15)
        stmt.move_to([3.4, 2.4, 0])
        rows = VGroup(
            MathTex(r"h = r - d(p, q) > 0", font_size=34),
            MathTex(r"d(p, s) \le d(p, q) + d(q, s)", font_size=34),
            MathTex(r"< d(p, q) + h = r", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75).move_to([3.4, 0.0, 0])
        rows[2].shift(RIGHT * 1.25)
        whys = VGroup(why(r"room left before the edge"), why(r"triangle inequality"), why(r"so $s \in N_r(p)$"))
        for r_, w_ in zip(rows, whys):
            w_.next_to(r_, DOWN, buff=0.08).align_to(r_, LEFT)
        with self.voiceover(
            "Our first theorem has a one-picture proof. <bookmark mark='s'/> Every neighborhood is itself an open set. "
            "<bookmark mark='q'/> Take any point q inside the disk of radius r around p. <bookmark mark='h'/> Its "
            "distance to p is less than r, so there's room to spare: call it h. <bookmark mark='t'/> Any point s within "
            "h of q is within r of p, by the triangle inequality. So the small disk around q sits inside the big one, and "
            "q is interior."
        ) as vo:
            self.play(FadeIn(big), FadeIn(pd), FadeIn(pl))
            vo.wait_until("s")
            self.play(FadeIn(stmt))
            vo.wait_until("q")
            self.play(FadeIn(qd, scale=2), FadeIn(ql), Create(pq))
            vo.wait_until("h")
            self.play(FadeIn(small, scale=0.5), FadeIn(rows[0]), FadeIn(whys[0]))
            vo.wait_until("t")
            self.play(FadeIn(sd), FadeIn(sl), Create(qs))
            self.play(FadeIn(rows[1:]), FadeIn(whys[1:]))
        self.wait(0.3)
        self.clear_scene()

        lim = VGroup(label(r"\textbf{Theorem} (Rudin 2.20) \ If $p$ is a limit point of $E$, every neighborhood", font_size=28),
                     label(r"of $p$ contains \emph{infinitely many} points of $E$. \ So finite sets have no limit points.",
                           font_size=28)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.5)
        p = np.array([0, -0.8, 0])
        pd = Dot(p, radius=0.07)
        pts = [p + 1.9 * np.array([np.cos(a), np.sin(a), 0]) * s for a, s in ((0.3, 0.8), (2.0, 0.55), (4.2, 0.7), (5.4, 0.4))]
        qs_ = VGroup(*[Dot(x, radius=0.07, color=C.SEQ) for x in pts])
        dmin = min(np.linalg.norm(x - p) for x in pts)
        n1 = nbhd(p, 1.85)
        n2 = nbhd(p, dmin * 0.92, color=C.PATHOLOGY)
        txt = label(r"only finitely many? \ shrink the radius below the nearest one: \ none left", font_size=26,
                    color=C.PATHOLOGY).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "One more consequence of the triangle inequality. <bookmark mark='a'/> If p is a limit point of E, every "
            "neighborhood of p contains infinitely many points of E. <bookmark mark='b'/> Because if some neighborhood "
            "held only finitely many, shrink the radius below the nearest of them, and you'd have a neighborhood with "
            "none at all. <bookmark mark='c'/> In particular, a finite set has no limit points."
        ) as vo:
            self.play(FadeIn(lim), FadeIn(pd), FadeIn(n1), FadeIn(qs_))
            vo.wait_until("b")
            self.play(Transform(n1, n2), FadeIn(txt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def complements(self):
        stmt = VGroup(label(r"\textbf{Theorem} (Rudin 2.23)", font_size=28, color=GREY_A),
                      label(r"$E$ is open \ $\iff$ \ its complement $E^c$ is closed.", font_size=34))
        stmt.arrange(DOWN, buff=0.15).to_edge(UP, buff=0.5)
        frame = Rectangle(width=12.0, height=5.4, color=GREY_C, stroke_width=1.5).shift(DOWN * 0.75)
        frame.set_fill(C.CLOSED_SET, 0.12)
        pts = blob_pts(np.array([-0.8, -0.75, 0]), scale=1.05)
        E = Polygon(*pts, stroke_width=0, fill_color=BACKGROUND, fill_opacity=1)
        Ef = Polygon(*pts, stroke_width=0, fill_color=C.OPEN_SET, fill_opacity=0.25)
        Ee = DashedVMobject(Polygon(*pts, color=C.OPEN_SET, stroke_width=2.5), num_dashes=70)
        El = MathTex(r"E", font_size=40, color=C.OPEN_SET).move_to([-0.8, -0.6, 0])
        Ecl = MathTex(r"E^c", font_size=40, color=C.CLOSED_SET).move_to([4.5, 0.9, 0])
        x = np.array([0.3, -1.3, 0])
        xd = Dot(x, radius=0.07)
        nx = nbhd(x, 0.45)
        txt = label(r"$x \in E$: a disk around $x$ misses $E^c$, so $x$ is not a limit point of $E^c$", font_size=26)
        txt.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Open and closed are related through complements. <bookmark mark='s'/> E is open exactly when everything "
            "outside it, its complement, is closed. <bookmark mark='p'/> If E is open, every x in E has a disk around it "
            "inside E, a disk that misses the complement entirely, so x is not a limit point of the complement. So every "
            "limit point of the complement lies in the complement: it's closed. The converse runs the same argument "
            "backwards."
        ) as vo:
            self.play(FadeIn(frame), FadeIn(E), FadeIn(Ef), Create(Ee), FadeIn(El), FadeIn(Ecl))
            vo.wait_until("s")
            self.play(FadeIn(stmt))
            vo.wait_until("p")
            self.play(FadeIn(xd), FadeIn(nx, scale=0.5), FadeIn(txt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unions(self):
        stmt = VGroup(
            label(r"\textbf{Rudin 2.24} \ Any union of open sets is open. \ A \emph{finite} intersection of open sets is open.",
                  font_size=28),
        ).to_edge(UP, buff=0.5)
        cs = [np.array([-4.3, 0.1, 0]), np.array([-3.2, 0.35, 0]), np.array([-3.8, -0.75, 0])]
        rs = [1.35, 1.25, 1.2]
        disks = VGroup(*[nbhd(c, r, color=C.OPEN_SET, fill=0.12) for c, r in zip(cs, rs)])
        x = np.array([-3.75, -0.1, 0])
        xd = Dot(x, radius=0.06)
        radii = [r - np.linalg.norm(x - c) for c, r in zip(cs, rs)]
        rm = min(radii)
        small = nbhd(x, rm, color=C.EPS, fill=0.25, dashes=24)
        sl = label(r"radius $= \min(r_1, r_2, r_3)$", font_size=26, color=C.EPS).next_to(disks, DOWN, buff=0.3)
        with self.voiceover(
            "How do open sets combine? <bookmark mark='u'/> Any union of open sets is open: a point in the union is in "
            "one of them, and that one already gives it room. <bookmark mark='i'/> The intersection of finitely many "
            "open sets is also open: <bookmark mark='m'/> a point in all of them has a disk inside each, and the "
            "smallest of those finitely many disks fits inside all of them."
        ) as vo:
            self.play(FadeIn(stmt))
            vo.wait_until("i")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in disks], lag_ratio=0.3), FadeIn(xd))
            vo.wait_until("m")
            self.play(FadeIn(small, scale=0.5), FadeIn(sl))

        X = lambda v: 2.5 + v * 3.5  # noqa: E731
        line = Line([X(-1.15), -0.4, 0], [X(1.15), -0.4, 0], color=GREY_C, stroke_width=2)
        zero = VGroup(Line([X(0), -0.5, 0], [X(0), -0.3, 0], color=GREY_B), Text("0", font_size=22, color=GREY_B)
                      .move_to([X(0), -0.75, 0]))
        bars = []
        for n in (1, 2, 3, 5, 10, 30):
            bars.append(VGroup(Line([X(-1 / n), 0.1, 0], [X(1 / n), 0.1, 0], color=C.OPEN_SET, stroke_width=7),
                               endpoint([X(-1 / n), 0.1, 0], False, C.OPEN_SET), endpoint([X(1 / n), 0.1, 0], False, C.OPEN_SET)))
        lab = MathTex(r"\bigcap_{n=1}^{\infty} \Big(-\frac1n, \frac1n\Big) = \{0\}", font_size=38).move_to([X(0), 1.6, 0])
        notopen = label(r"not open", font_size=30, color=C.PATHOLOGY).next_to(lab, DOWN, buff=0.15)
        dot0 = Dot([X(0), 0.1, 0], radius=0.08, color=C.PATHOLOGY)
        with self.voiceover(
            "But only finitely many. <bookmark mark='a'/> The intervals from minus one over n to one over n are all open, "
            "and they shrink down onto a single point, zero. <bookmark mark='b'/> Their intersection is just zero, which "
            "is not open. With infinitely many sets, the minimum radius can be zero. That one word, finite, is the seed "
            "of compactness, in the next chapter."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(line), FadeIn(zero), FadeIn(bars[0]))
            for b in bars[1:]:
                self.play(Transform(bars[0], b), run_time=0.5)
            vo.wait_until("b")
            self.play(Write(lab), FadeIn(dot0, scale=2), FadeIn(notopen))
        dual = label(r"Dually: any intersection of closed sets is closed; finite unions of closed sets are closed;"
                     r" \ $\bigcup [\tfrac1n, 1] = (0, 1]$ is not.", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(dual))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        heads = [r"", r"closed", r"open", r"perfect", r"bounded"]
        rows = [
            (r"(a) \ $|z| < 1$", ["no", "yes", "no", "yes"]),
            (r"(b) \ $|z| \le 1$", ["yes", "no", "yes", "yes"]),
            (r"(c) \ a finite set", ["yes", "no", "no", "yes"]),
            (r"(d) \ the integers", ["yes", "no", "no", "no"]),
            (r"(e) \ $\{1, \tfrac12, \tfrac13, \ldots\}$", ["no", "no", "no", "yes"]),
            (r"(f) \ the whole plane", ["yes", "yes", "yes", "no"]),
            (r"(g) \ a segment $(a, b)$", ["no", "no", "no", "yes"]),
        ]
        xs = [-3.6, -0.6, 0.9, 2.4, 3.9]
        y0 = 2.2
        g = VGroup()
        hd = VGroup(*[label(h, font_size=26, color=GREY_A).move_to([x, y0, 0]) for h, x in zip(heads, xs)])
        g.add(hd)
        body = VGroup()
        for i, (name, vals) in enumerate(rows):
            y = y0 - 0.62 * (i + 1)
            r = VGroup(label(name, font_size=26).move_to([xs[0], y, 0]))
            for v, x in zip(vals, xs[1:]):
                r.add(label(v, font_size=26, color=C.CONNECTED_SET if v == "yes" else GREY_C).move_to([x, y, 0]))
            r[0].align_to([-5.4, 0, 0], LEFT)
            r.add(self.icon(i).move_to([-6.25, y, 0]))  # a thumbnail of the set, last in the row
            body.add(r)
        g.add(body)
        rule = Line([-5.5, y0 - 0.3, 0], [4.6, y0 - 0.3, 0], color=GREY_C, stroke_width=1.5)
        title = label(r"Subsets of the plane \ (Rudin 2.21--2.22)", font_size=32).to_edge(UP, buff=0.4)
        perfect = label(r"\textbf{perfect} = closed, and every point is a limit point", font_size=26, color=GREY_A)
        perfect.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Rudin collects the standard examples in a table, here in the plane. <bookmark mark='a'/> The open disk is "
            "open but not closed; the closed disk, closed but not open. <bookmark mark='e'/> The points one, a half, a "
            "third, and so on, are neither: zero is a limit point the set doesn't contain. <bookmark mark='f'/> The whole "
            "plane is both. <bookmark mark='p'/> The new column is perfect: closed, with every point a limit point, no "
            "isolated points. Perfect sets will give us the Cantor set. <bookmark mark='g'/> And look at the last row: a "
            "segment of the x-axis is not open in the plane."
        ) as vo:
            self.play(FadeIn(title), FadeIn(hd), Create(rule))
            vo.wait_until("a")
            self.play(FadeIn(body[0]), FadeIn(body[1]))
            self.play(FadeIn(body[2]), FadeIn(body[3]))
            vo.wait_until("e")
            self.play(FadeIn(body[4]))
            vo.wait_until("f")
            self.play(FadeIn(body[5]))
            vo.wait_until("p")
            self.play(FadeIn(perfect), Indicate(hd[3], color=C.EPS))
            vo.wait_until("g")
            self.play(FadeIn(body[6]))
            self.play(Indicate(body[6][2], color=C.PATHOLOGY))
        self.wait(0.3)
        self.clear_scene()

    @staticmethod
    def icon(i):
        """Thumbnails for the rows of the table (a)..(g), about 0.5 across."""
        frame = Square(side_length=0.5, stroke_color=GREY_D, stroke_width=1)
        c = frame.get_center()
        if i == 0:
            body = nbhd(c, 0.2, color=C.OPEN_SET, fill=0.3, width=1.5, dashes=14)
        elif i == 1:
            body = Circle(radius=0.2, stroke_color=C.CLOSED_SET, stroke_width=2).set_fill(C.CLOSED_SET, 0.3)
        elif i == 2:
            body = VGroup(*[Dot(c + np.array(v), radius=0.035, color=C.SEQ)
                            for v in ((-0.12, 0.1, 0), (0.1, 0.13, 0), (0.0, -0.05, 0), (0.14, -0.14, 0))])
        elif i == 3:
            body = VGroup(*[Dot(c + np.array([x, y, 0]), radius=0.025, color=C.SEQ)
                            for x in (-0.18, -0.06, 0.06, 0.18) for y in (-0.18, -0.06, 0.06, 0.18)])
        elif i == 4:
            body = VGroup(*[Dot(c + np.array([-0.2 + 0.4 / n, 0, 0]), radius=0.025, color=C.SEQ) for n in range(1, 13)],
                          Circle(radius=0.03, color=C.PATHOLOGY, stroke_width=1.5).move_to(c + np.array([-0.2, 0, 0])))
        elif i == 5:
            body = Square(side_length=0.5, stroke_width=0).set_fill(C.OPEN_SET, 0.3)
        else:
            body = VGroup(Line(c + np.array([-0.17, 0, 0]), c + np.array([0.17, 0, 0]), color=C.SEQ, stroke_width=2.5),
                          *[Circle(radius=0.035, color=C.SEQ, stroke_width=1.5).set_fill(BACKGROUND, 1).move_to(
                              c + np.array([x, 0, 0])) for x in (-0.17, 0.17)])
        return VGroup(frame, body)

    # ------------------------------------------------------------------
    def closure(self):
        defs = VGroup(
            MathTex(r"\overline{E} = E \cup \{\text{limit points of } E\}", font_size=40, color=C.CLOSED_SET),
            label(r"the \textbf{closure}: closed, and the smallest closed set containing $E$ \ (Rudin 2.27)", font_size=28),
        ).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.5)
        ex = VGroup(
            MathTex(r"\overline{\Q} = \R", font_size=40, color=C.RATIONAL),
            label(r"every real number is a limit of fractions: $\Q$ is \textbf{dense}", font_size=28),
            MathTex(r"\text{yet the interior of } \Q \text{ is empty}", font_size=34, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(defs, DOWN, buff=0.6)
        ex.next_to(defs, DOWN, buff=0.35)
        # E = {1/n} together with the open interval (1.3, 2): the closure adds 0, 1.3 and 2
        X = lambda v: -5.0 + 4.6 * v  # noqa: E731
        y1, y2 = -0.95, -2.05
        l1 = Line([X(-0.08), y1, 0], [X(2.1), y1, 0], color=GREY_C, stroke_width=1.5)
        E_pts = VGroup(*[Dot([X(1 / n), y1, 0], radius=0.045, color=C.SEQ) for n in range(1, 31)],
                       Line([X(1.3), y1, 0], [X(2.0), y1, 0], color=C.SEQ, stroke_width=6),
                       *[endpoint([X(v), y1, 0], False, C.SEQ, radius=0.06) for v in (1.3, 2.0)])
        E_l = MathTex(r"E = \{1, \tfrac12, \tfrac13, \ldots\} \cup (1.3,\, 2)", font_size=26, color=C.SEQ).next_to(
            [X(1.0), y1, 0], UP, buff=0.25)
        added = VGroup(*[Dot([X(v), y1, 0], radius=0.07, color=C.CLOSED_SET) for v in (0.0, 1.3, 2.0)])
        added_l = label(r"$\overline{E}$ adds $0$, \ $1.3$, \ $2$", font_size=24, color=C.CLOSED_SET).next_to(
            [X(0.0), y1, 0], DOWN, buff=0.2).shift(RIGHT * 0.9)
        l2 = Line([X(-0.08), y2, 0], [X(2.1), y2, 0], color=GREY_C, stroke_width=1.5)
        dust = rational_dust(0.0, 2.1, X(0.0), X(2.1), y=y2, height=0.45, target=900)
        Qbar = VGroup(Line([X(0.0), y2 - 0.12, 0], [X(2.1), y2 - 0.12, 0], color=C.CLOSED_SET, stroke_width=4),
                      MathTex(r"\Q \ \to \ \overline{\Q} = \R", font_size=26, color=C.CLOSED_SET).next_to(
                          [X(2.1), y2, 0], RIGHT, buff=0.15))
        sup = VGroup(label(r"\textbf{Rudin 2.28} \ If $E \subset \R$ is nonempty and bounded above, $\sup E \in \overline{E}$.",
                           font_size=28),
                     label(r"(If $\sup E$ were not a limit point, a slightly smaller number would be an upper bound.)",
                           font_size=24, color=GREY_B)).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Adding the limit points to a set gives its closure, <bookmark mark='c'/> the smallest closed set containing "
            "it. <bookmark mark='q'/> The closure of the rationals is the whole real line: every real number is a limit "
            "of fractions. That's what dense means. <bookmark mark='i'/> And yet the rationals contain no interval at "
            "all, so their interior is empty. Big and small at once, a theme that will come back in Part 8 as Baire's "
            "theorem. <bookmark mark='s'/> And one fact that ties back to chapter one: the supremum of a set of reals "
            "always lies in its closure."
        ) as vo:
            self.play(FadeIn(defs[0]), Create(l1), FadeIn(E_pts), FadeIn(E_l))
            self.play(LaggedStart(*[FadeIn(a_, scale=2) for a_ in added], lag_ratio=0.3), FadeIn(added_l))
            vo.wait_until("c")
            self.play(FadeIn(defs[1]))
            vo.wait_until("q")
            self.play(FadeIn(ex[0]), FadeIn(ex[1]), Create(l2), FadeIn(dust))
            self.play(Create(Qbar[0]), FadeIn(Qbar[1]))
            vo.wait_until("i")
            self.play(FadeIn(ex[2]))
            vo.wait_until("s")
            self.play(FadeIn(sup))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def relative(self):
        plane_box = Rectangle(width=12, height=4.6, color=GREY_D, stroke_width=1.5).shift(DOWN * 0.6)
        axis = Line([-6, -0.6, 0], [6, -0.6, 0], color=GREY_C, stroke_width=2)
        seg = VGroup(Line([-3.0, -0.6, 0], [3.0, -0.6, 0], color=C.OPEN_SET, stroke_width=8),
                     endpoint([-3.0, -0.6, 0], False, C.OPEN_SET), endpoint([3.0, -0.6, 0], False, C.OPEN_SET))
        p = np.array([1.0, -0.6, 0])
        pd = Dot(p, radius=0.07)
        in_line = VGroup(Line(p + LEFT * 0.7, p + RIGHT * 0.7, color=C.EPS, stroke_width=10))
        disk = nbhd(p, 0.7, color=C.PATHOLOGY, fill=0.15)
        l1 = label(r"in $\R$: an interval around the point fits inside: \textbf{open}", font_size=28, color=C.EPS)
        l2 = label(r"in $\R^2$: every disk pokes above and below: \textbf{not open}", font_size=28, color=C.PATHOLOGY)
        VGroup(l1, l2).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.5)
        coda = label(r"Open depends on the surrounding space. \ Compact, it turns out, does not.", font_size=30,
                     color=C.COMPACT_SET).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "That last example deserves a closer look. <bookmark mark='a'/> The interval from a to b, on the real line, "
            "is open: around each of its points there's a little interval inside it. <bookmark mark='b'/> But put the "
            "same segment inside the plane, and every disk around a point pokes above and below it. As a subset of the "
            "plane, it's not open. <bookmark mark='c'/> Being open is not a property of a set alone: it depends on the "
            "space around it. Rudin calls this being open relative to a space. The next property we meet, compactness, "
            "is different: it belongs to the set itself."
        ) as vo:
            self.play(FadeIn(plane_box), Create(axis), FadeIn(seg))
            vo.wait_until("a")
            self.play(FadeIn(pd), Create(in_line), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeOut(in_line), FadeIn(disk, scale=0.5), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(coda))
        self.wait(0.5)
        self.clear_scene()
