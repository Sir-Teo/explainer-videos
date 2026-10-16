from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis1.common import cantor_function, cantor_intervals, load, polyline, segments_points
from videos.analysis.analysis1.s07_open_closed import nbhd


def cantor_bars(depth: int, a: float, b: float, x_left: float, x_right: float, y: float, height=0.22,
                color=WHITE, min_w=0.004) -> VMobject:
    """The depth-n stage of the Cantor set restricted to the window [a, b], drawn as thick strokes on one VMobject."""
    iv = cantor_intervals(depth)
    sel = (iv[:, 1] >= a) & (iv[:, 0] <= b)
    iv = iv[sel]
    sx = (x_right - x_left) / (b - a)
    xa = x_left + (np.clip(iv[:, 0], a, b) - a) * sx
    xb = x_left + (np.clip(iv[:, 1], a, b) - a) * sx
    m = VGroup()
    for x0, x1 in zip(xa, xb):
        w = max(x1 - x0, min_w)
        m.add(Rectangle(width=w, height=height, stroke_width=0, fill_color=color, fill_opacity=1)
              .move_to([(x0 + x1) / 2, y, 0]))
    return m


class Cantor(VoiceoverScene):
    def construct(self):
        self.card()
        self.perfect()
        self.construction()
        self.properties()
        self.digits()
        self.staircase()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"The Cantor set", r"Can a set be uncountable and have length zero?", lit=(1883,), part=1)
        with self.voiceover(
            "Chapter nine. Compactness gives a second, completely different proof that the real numbers are "
            "uncountable, and it leads to the most famous strange set in analysis."
        ) as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def perfect(self):
        stmt = VGroup(label(r"\textbf{Theorem} (Rudin 2.43)", font_size=28, color=GREY_A),
                      label(r"A nonempty perfect set in $\R^k$ is uncountable.", font_size=32)).arrange(DOWN, buff=0.12)
        stmt.to_edge(UP, buff=0.45)
        steps = VGroup(
            label(r"suppose $P = \{x_1, x_2, x_3, \ldots\}$", font_size=28),
            label(r"choose nested closed disks $\overline{V}_1 \supset \overline{V}_2 \supset \cdots$, each meeting $P$,", font_size=28),
            label(r"with $x_n \notin \overline{V}_{n+1}$ \ (possible: every point of $P$ is a limit point)", font_size=28),
            label(r"$K_n = \overline{V}_n \cap P$: nested, nonempty, compact \ $\Rightarrow$ \ $\bigcap K_n \neq \emptyset$ (2.36)",
                  font_size=28),
            label(r"but no $x_n$ is in it: \ a point of $P$ missing from the list", font_size=28, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for s_ in steps:
            s_.set_max_width(8.6)
        steps.move_to([2.1, -1.25, 0])
        # P: a perfect set in the plane, the product of the Cantor set with itself (drawn to depth 4)
        o, S = np.array([-4.65, 0.2, 0]), 3.6

        def U(u, v):
            return o + np.array([(u - 0.5) * S, (v - 0.5) * S, 0])

        iv = cantor_intervals(4)
        # all 256 squares as one VMobject (one closed subpath each)
        sq_pts = []
        for a, b in iv:
            for c, d in iv:
                cs_ = [U(a, c), U(b, c), U(b, d), U(a, d), U(a, c)]
                for p0, p1 in zip(cs_, cs_[1:]):
                    sq_pts += [p0, p0 + (p1 - p0) / 3, p0 + 2 * (p1 - p0) / 3, p1]
        Pdust = VMobject(stroke_width=0, fill_color=C.SEQ, fill_opacity=0.85)
        Pdust.set_points(np.array(sq_pts))
        P_l = MathTex(r"P", font_size=32, color=C.SEQ).next_to(U(0, 1), UP, buff=0.1).align_to(U(0, 1), LEFT)
        # the nested disks and the listed points (endpoints of the depth-4 intervals, so points of P)
        ends = np.unique(iv.ravel())
        Ppts = np.array([(x, y) for x in ends for y in ends])
        cen = [np.array(c) for c in ((0.5, 0.5), (0.4226, 0.6166), (0.3355, 0.6637), (0.3759, 0.6932), (0.3765, 0.6724))]
        rad = [0.5, 0.32, 0.2, 0.127, 0.08]
        xs_u = [np.array([55, 18]) / 81, np.array([55, 55]) / 81, np.array([18, 63]) / 81, np.array([25, 62]) / 81]
        for i in range(4):
            assert any(np.allclose(xs_u[i], q) for q in Ppts)                          # x_i is a point of P
            assert np.linalg.norm(xs_u[i] - cen[i]) < rad[i]                          # inside V_i
            assert np.linalg.norm(xs_u[i] - cen[i + 1]) > rad[i + 1]                  # avoided by V_{i+1}
            assert np.linalg.norm(cen[i + 1] - cen[i]) + rad[i + 1] < rad[i]          # nested
        inner = Ppts[np.linalg.norm(Ppts - cen[4], axis=1) < rad[4]]
        assert len(inner) > 0                                                         # the last disk meets P
        xstar = inner[np.argmin(np.linalg.norm(inner - cen[4], axis=1))]
        disks = VGroup(*[Circle(radius=r * S, color=C.COMPACT_SET, stroke_width=3).move_to(U(*c)) for r, c in zip(rad, cen)])
        # each label where it is farthest from every ring and point (x_4, deep inside, goes unnamed: "and so on")
        lab_dir = [(3.665, 0.11), (4.189, 0.095), (4.363, 0.08), None]
        xd = VGroup()
        for i, (p, la) in enumerate(zip(xs_u, lab_dir)):
            g_ = VGroup(Dot(U(*p), radius=0.06, color=C.PATHOLOGY))
            if la is not None:
                a, rr = la
                t = MathTex(rf"x_{i + 1}", font_size=26, color=C.PATHOLOGY)
                t.add_background_rectangle(color=BACKGROUND, opacity=0.8, buff=0.03)
                g_.add(t.move_to(U(*p) + rr * S * np.array([np.cos(a), np.sin(a), 0])))
            xd.add(g_)
        star = Dot(U(*xstar), radius=0.06, color=WHITE)
        star_l = MathTex(r"x^* \notin \{x_1, x_2, \ldots\}", font_size=28).move_to([-0.9, 1.75, 0])
        star_lead = Line(star_l.get_left() + LEFT * 0.08, U(*xstar) + RIGHT * 0.08, color=GREY_B, stroke_width=1.5)
        perf = label(r"\textbf{perfect}: closed, and every point is a limit point (no isolated points)", font_size=30,
                     color=GREY_A).move_to(UP * 2.4)
        with self.voiceover(
            "Recall that a set is perfect if it's closed and every one of its points is a limit point: no isolated "
            "points. <bookmark mark='s'/> Every nonempty perfect set in k-dimensional space is uncountable. "
            "<bookmark mark='a'/> Suppose instead that a perfect set P could be listed: x one, x two, x three. "
            "<bookmark mark='b'/> Choose a closed disk that meets P, <bookmark mark='c'/> then a smaller closed disk inside "
            "it that still meets P but avoids x one. That's possible because every point of P is a limit point, so there "
            "are other points of P nearby to aim for. Then a smaller one avoiding x two, and so on."
        ) as vo:
            self.play(FadeIn(perf), FadeIn(Pdust), FadeIn(P_l), run_time=1.5)
            vo.wait_until("s")
            self.play(FadeIn(stmt), FadeOut(perf))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(Create(disks[0]), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            for i in range(4):
                self.play(FadeIn(xd[i]), Create(disks[i + 1]), run_time=0.7)
        with self.voiceover(
            "<bookmark mark='k'/> The pieces of P inside these disks are nested, nonempty and compact, so by theorem "
            "2.36, from the chapter on compactness, something lies in all of them. <bookmark mark='m'/> That something is a point of P, but "
            "it can't be x n for any n, because the n plus first disk avoids x n. So the list missed a point. The real "
            "line is perfect, so this is a second proof that it's uncountable, built from compactness instead of digits."
        ) as vo:
            vo.wait_until("k")
            self.play(FadeIn(steps[3]))
            vo.wait_until("m")
            self.play(FadeIn(steps[4]), FadeIn(star, scale=3), FadeIn(star_l), Create(star_lead))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def construction(self):
        L, R = -6.0, 2.0
        ys = [2.3 - 0.62 * k for k in range(8)]
        stages = VGroup(*[cantor_bars(k, 0, 1, L, R, ys[k], height=0.2) for k in range(8)])
        labs = VGroup(*[MathTex(rf"E_{k}", font_size=28, color=GREY_A).next_to([L, ys[k], 0], LEFT, buff=0.25)
                        for k in range(8)])
        info = VGroup(*[MathTex(rf"2^{{{k}}} \text{{ pieces, total length }} (2/3)^{{{k}}}", font_size=24, color=GREY_B)
                        .move_to([4.75, ys[k] - 0.0, 0]) for k in range(8)])
        title = label(r"Remove the open middle third, again and again", font_size=34).to_edge(UP, buff=0.3)
        ref = note(r"Rudin 2.44").to_corner(DR, buff=0.45)
        with self.voiceover(
            "The Cantor set, from 1883, is built by removing. <bookmark mark='a'/> Start with the interval from zero to "
            "one. <bookmark mark='b'/> Remove its open middle third, leaving two closed pieces. <bookmark mark='c'/> "
            "Remove the middle third of each of those, leaving four, then eight, then sixteen. <bookmark mark='p'/> The "
            "Cantor set is what survives every step: the intersection of all these stages."
        ) as vo:
            self.play(FadeIn(title), FadeIn(ref))
            vo.wait_until("a")
            self.play(FadeIn(stages[0]), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(TransformFromCopy(stages[0], stages[1]), FadeIn(labs[1]))
            vo.wait_until("c")
            for k in range(2, 8):
                self.play(TransformFromCopy(stages[k - 1], stages[k]), FadeIn(labs[k]), run_time=0.6)
            vo.wait_until("p")
            self.play(LaggedStart(*[FadeIn(i_) for i_ in info], lag_ratio=0.1))
        d = load("cantor")
        for k in range(8):
            iv = d[f"iv{k}"]
            assert len(iv) == 2**k and abs((iv[:, 1] - iv[:, 0]).sum() - (2 / 3) ** k) < 1e-12
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def properties(self):
        props = VGroup(
            label(r"\textbf{compact}: an intersection of closed sets inside $[0, 1]$", font_size=26, color=C.COMPACT_SET),
            label(r"\textbf{nonempty}: $0$, $1$, $\tfrac13$, $\tfrac23$, \ldots \ every endpoint survives", font_size=26),
            label(r"\textbf{no interval}: any $(\alpha, \beta)$ contains a removed middle third", font_size=26),
            label(r"\textbf{perfect}: endpoints of later stages crowd up to every point", font_size=26),
            label(r"so \textbf{uncountable} (2.43), \ \ yet the removed lengths add up to", font_size=26, color=C.EPS),
            MathTex(r"\frac13 + \frac29 + \frac4{27} + \cdots = \frac{1/3}{1 - 2/3} = 1", font_size=36, color=C.MEASURE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for p_ in props:
            p_.set_max_width(8.6)
        head = label(r"What survives?", font_size=34).to_edge(UP, buff=0.3)
        props.next_to(head, DOWN, buff=0.3).to_edge(LEFT, buff=0.6)
        props[-1].shift(RIGHT * 1.0)
        # one stage of the construction, under the list, illustrating each line in turn
        K = 5
        L, R, ys = -6.0, 6.0, -2.35
        X = lambda v: L + (R - L) * float(v)  # noqa: E731
        strip = cantor_bars(K, 0, 1, L, R, ys, height=0.32)
        strip_l = MathTex(rf"E_{K}", font_size=26, color=GREY_A).next_to([L, ys, 0], LEFT, buff=0.2)
        # nonempty: the endpoints 0, 1/3, 2/3, 1 are never removed
        e_vals = [(0, "0"), (1 / 3, r"\tfrac13"), (2 / 3, r"\tfrac23"), (1, "1")]
        e_pts = VGroup(*[Dot([X(v), ys, 0], radius=0.07, color=C.EPS) for v, _ in e_vals])
        e_lab = VGroup(*[MathTex(t, font_size=26, color=C.EPS).next_to([X(v), ys + 0.16, 0], UP, buff=0.12)
                         for v, t in e_vals])
        # no interval: (alpha, beta) = (0.24, 0.31) contains the removed third (7/27, 8/27)
        al, be = 0.24, 0.31
        gaps = [((2 * a + b) / 3, (a + 2 * b) / 3) for k in range(K) for a, b in cantor_intervals(k)]
        inside = [g for g in gaps if al < g[0] and g[1] < be]
        assert inside and abs(inside[0][0] - 7 / 27) < 1e-12 and abs(inside[0][1] - 8 / 27) < 1e-12
        g0 = inside[0]
        hole = Rectangle(width=X(g0[1]) - X(g0[0]), height=0.32, stroke_width=0, fill_color=C.HOLE,
                         fill_opacity=0.75).move_to([(X(g0[0]) + X(g0[1])) / 2, ys, 0])
        yb = ys - 0.42
        brk = VGroup(MathTex(r"(", font_size=40, color=WHITE).move_to([X(al), ys, 0]),
                     MathTex(r")", font_size=40, color=WHITE).move_to([X(be), ys, 0]),
                     MathTex(r"\alpha", font_size=26).next_to([X(al), yb, 0], DOWN, buff=0.05),
                     MathTex(r"\beta", font_size=26).next_to([X(be), yb, 0], DOWN, buff=0.05))
        # perfect: endpoints of E_1, E_2, ... nearest to 1/4 (a point of the set that is never an endpoint)
        near = []
        for k in range(1, 9):
            e = cantor_intervals(k).ravel()
            near.append(e[np.argmin(np.abs(e - 0.25))])
        dist = [abs(v - 0.25) for v in near]
        assert all(b_ < a_ for a_, b_ in zip(dist, dist[1:])) and dist[-1] < 1e-3  # they crowd up to 1/4
        crowd = VGroup(*[Dot([X(v), ys, 0], radius=0.045, color=C.DELTA) for v in near])
        q_ring = DashedVMobject(Circle(radius=0.42, color=C.DELTA, stroke_width=2.5).move_to([X(0.25), ys, 0]),
                                num_dashes=24)
        q_lab = MathTex(r"\tfrac14", font_size=26, color=C.DELTA).next_to(q_ring, UP, buff=0.08)
        # length: the removed thirds, stage by stage (1/3, then 2/9, then 4/27, ...)
        fills = VGroup()
        for k in range(K):
            row = VGroup()
            for a, b in cantor_intervals(k):
                ga, gb = (2 * a + b) / 3, (a + 2 * b) / 3
                row.add(Rectangle(width=X(gb) - X(ga), height=0.32, stroke_width=0, fill_color=C.MEASURE,
                                  fill_opacity=0.7).move_to([(X(ga) + X(gb)) / 2, ys, 0]))
            assert abs(sum((r_.width for r_ in row)) / (R - L) - 2 ** k / 3 ** (k + 1)) < 1e-9
            fills.add(row)
        with self.voiceover(
            "What survives? <bookmark mark='a'/> The Cantor set is compact, as an intersection of closed sets inside a "
            "compact interval. <bookmark mark='b'/> It's not empty: zero, one, and every endpoint of every stage is never "
            "removed. <bookmark mark='c'/> It contains no interval at all, since any interval, however short, contains "
            "some removed middle third. <bookmark mark='d'/> And it's perfect: near every point of the set, there are "
            "endpoints of later stages. <bookmark mark='e'/> So, by the theorem, it's uncountable. <bookmark mark='f'/> "
            "And yet, the lengths we removed add up to one third, plus two ninths, plus four twenty-sevenths, and so on: "
            "exactly one. Uncountably many points, total length zero."
        ) as vo:
            self.play(FadeIn(head), FadeIn(strip), FadeIn(strip_l))
            pics = {"a": lambda: [Indicate(strip, color=C.COMPACT_SET, scale_factor=1.0)],
                    "b": lambda: [FadeIn(e_pts, scale=2), FadeIn(e_lab)],
                    "c": lambda: [FadeOut(e_pts), FadeOut(e_lab), FadeIn(brk), FadeIn(hole)],
                    "d": lambda: [FadeOut(brk), FadeOut(hole), Create(q_ring), FadeIn(q_lab),
                                  LaggedStart(*[FadeIn(c_, scale=2) for c_ in crowd], lag_ratio=0.2)],
                    "e": lambda: [FadeOut(q_ring), FadeOut(q_lab), FadeOut(crowd)],
                    "f": lambda: [LaggedStart(*[FadeIn(r_) for r_ in fills], lag_ratio=0.5, run_time=2.4)]}
            for mk, p in zip("abcdef", props):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.15), *pics[mk]())
        card = museum_card(r"The Cantor set", r"Georg Cantor, 1883 (H.~J.~S.~Smith, 1875)",
                           r"``uncountable sets are big''", r"Rudin, \textit{Principles} 2.44").scale(0.9)
        card.to_edge(RIGHT, buff=0.4).set_y(props.get_center()[1])
        assert card.get_left()[0] > props.get_right()[0] + 0.2
        self.play(FadeIn(card, shift=LEFT * 0.2))
        self.wait(1.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def digits(self):
        d = load("cantor")
        dig = [int(x) for x in d["quarter_digits"]]
        L, R = -6.0, 6.0
        y = -0.4
        H = 0.5
        title = MathTex(r"\text{Cantor set} = \{\, x \in [0,1] : x \text{ has a base-3 expansion using only } 0 \text{ and } 2 \,\}",
                        font_size=32).to_edge(UP, buff=0.45)
        link = label(r"the zero--one sequences of chapter 4, with $1 \mapsto 2$", font_size=26, color=GREY_A)
        link.next_to(title, DOWN, buff=0.2)
        quarter = MathTex(r"\tfrac14 = 0.020202\ldots_{\,3}", font_size=40, color=C.EPS).next_to(link, DOWN, buff=0.35)
        a_, b_ = ValueTracker(0.0), ValueTracker(1.0)
        BELOW = 7  # every view is drawn 7 levels below its own scale, so each zoom shows the same picture

        def window_intervals(a, b):
            depth = int(math.floor(math.log(1 / (b - a), 3) + 1e-9)) + BELOW
            iv = np.array([[0.0, 1.0]])
            for _ in range(depth):  # split only the pieces that meet the window
                lo_, hi_ = iv[:, 0], iv[:, 1]
                t = (hi_ - lo_) / 3
                iv = np.stack([np.stack([lo_, lo_ + t], 1), np.stack([hi_ - t, hi_], 1)], 1).reshape(-1, 2)
                iv = iv[(iv[:, 1] >= a) & (iv[:, 0] <= b)]
            return iv

        def view():
            a, b = a_.get_value(), b_.get_value()
            iv = window_intervals(a, b)
            sx = (R - L) / (b - a)
            x0 = L + (np.clip(iv[:, 0], a, b) - a) * sx
            x1 = np.maximum(L + (np.clip(iv[:, 1], a, b) - a) * sx, x0 + 0.004)
            # all bars as one VMobject: each bar one closed subpath of four straight (cubic) edges
            corners = np.stack([np.stack([x0, x1, x1, x0, x0], 1), np.stack([np.full_like(x0, y - H / 2), np.full_like(x0, y - H / 2),
                                np.full_like(x0, y + H / 2), np.full_like(x0, y + H / 2), np.full_like(x0, y - H / 2)], 1)], 2)
            p0, p1 = corners[:, :-1], corners[:, 1:]
            seg = np.stack([p0, p0 + (p1 - p0) / 3, p0 + 2 * (p1 - p0) / 3, p1], 2).reshape(-1, 2)
            pts = np.concatenate([seg, np.zeros((len(seg), 1))], 1)
            m = VMobject(stroke_width=0, fill_color=WHITE, fill_opacity=1)
            m.set_points(pts)
            return m

        # the windows we zoom to are f^k([0, 1]) for f(x) = x/9 + 2/9, whose fixed point is 1/4: self-similar
        for k in range(1, 5):
            w = 9.0 ** (-k)
            lo, hi = 0.25 - 0.25 * w, 0.25 + 0.75 * w
            back = (window_intervals(lo, hi) - lo) / w
            back = back[(back[:, 1] > 1e-9) & (back[:, 0] < 1 - 1e-9)]
            ref_iv = cantor_intervals(BELOW)
            assert len(back) == len(ref_iv) and np.allclose(back, ref_iv, atol=1e-6)
        bars = always_redraw(view)
        mark = always_redraw(lambda: Triangle(color=C.EPS, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI)
                             .move_to([L + (0.25 - a_.get_value()) / (b_.get_value() - a_.get_value()) * (R - L), y + 0.55, 0]))
        zoom_l = always_redraw(lambda: Text(f"zoom ×{1 / (b_.get_value() - a_.get_value()):,.0f}", font_size=24,
                                            color=GREY_B).to_corner(DR, buff=0.45))
        dig_tx = ValueTracker(0)

        def digits_text():
            ds = "".join(str(x) for x in dig[: int(round(dig_tx.get_value()))])
            return Text("0." + ds + ("..." if ds else ""), font_size=34, color=C.EPS,
                        font="DejaVu Sans Mono").move_to([0, -2.2, 0])

        digits_m = always_redraw(digits_text)
        with self.voiceover(
            "There's a cleaner description in base three. <bookmark mark='t'/> The first removal throws out the numbers "
            "whose first base-three digit has to be a one; the second throws out those whose second digit has to be one; "
            "and so on. The Cantor set is exactly the numbers that can be written in base three using only zeros and "
            "twos. <bookmark mark='l'/> Those are chapter four's zero-one sequences, with ones written as twos. That's why "
            "the map we used there landed here."
        ) as vo:
            self.play(FadeIn(bars))
            vo.wait_until("t")
            self.play(FadeIn(title))
            vo.wait_until("l")
            self.play(FadeIn(link))
        with self.voiceover(
            "Here's a strange member. <bookmark mark='q'/> One quarter, in base three, is 0.0202 repeating: only zeros and "
            "twos, so it's in the Cantor set, but it's never an endpoint of any stage. <bookmark mark='z'/> Zoom in "
            "around it by a factor of nine, and the picture repeats exactly: the set is self-similar. "
            "<bookmark mark='d'/> Each zoom reads off two more digits."
        ) as vo:
            vo.wait_until("q")
            self.play(FadeIn(quarter), FadeIn(mark), FadeIn(digits_m))
            vo.wait_until("z")
            self.add(zoom_l)
            for k in range(1, 5):
                w = 9.0 ** (-k)
                lo, hi = 0.25 - 0.25 * w, 0.25 + 0.75 * w
                self.play(a_.animate.set_value(lo), b_.animate.set_value(hi), dig_tx.animate.set_value(2 * k), run_time=2.0)
        assert dig[:8] == [0, 2, 0, 2, 0, 2, 0, 2]
        self.wait(0.5)
        for m in (bars, mark, zoom_l, digits_m):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def staircase(self):
        d = load("cantor")
        ax = Axes(x_range=[0, 1, 1 / 3], y_range=[0, 1, 0.5], x_length=6.8, y_length=5.2, tips=False,
                  axis_config={"stroke_color": GREY_C}).shift(LEFT * 2.8 + DOWN * 0.4)
        xs = np.linspace(0, 1, 3001)
        xt = VGroup(*[MathTex(t, font_size=24, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.15)
                      for t, v in ((r"0", 0), (r"\tfrac13", 1 / 3), (r"\tfrac23", 2 / 3), (r"1", 1))])
        yt = VGroup(*[MathTex(t, font_size=24, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.15)
                      for t, v in ((r"\tfrac12", 0.5), (r"1", 1))])

        def stair(n):
            return polyline(ax, xs, cantor_function(xs, depth=n), color=C.SEQ, stroke_width=3.5)

        S = stair(1)
        head = label(r"The Cantor function: the devil's staircase", font_size=34).to_edge(UP, buff=0.3)
        rule = VGroup(label(r"read the base-3 digits of $x$ up to the first $1$;", font_size=26),
                      label(r"turn the $2$s into $1$s; read it in base $2$", font_size=26),
                      MathTex(r"\tfrac14 = 0.0202\ldots_3 \;\mapsto\; 0.0101\ldots_2 = \tfrac13", font_size=32, color=C.EPS)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.0, 1.4, 0])
        props = VGroup(label(r"continuous, nondecreasing,", font_size=26),
                       label(r"$F(0) = 0$, \ $F(1) = 1$,", font_size=26),
                       label(r"flat on every removed third:", font_size=26),
                       label(r"it climbs on a set of length $0$", font_size=26, color=C.PATHOLOGY)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        props.move_to([4.2, -1.2, 0])
        Fq = cantor_function(np.array([0.25]))[0]
        assert abs(Fq - 1 / 3) < 1e-12
        qp = ax.c2p(0.25, Fq)
        qdot = Dot(qp, radius=0.08, color=C.EPS)
        qdrop = VGroup(DashedLine(qp, ax.c2p(0.25, 0), color=C.EPS, stroke_width=2),
                       DashedLine(qp, ax.c2p(0, Fq), color=C.EPS, stroke_width=2))
        qlab = VGroup(MathTex(r"\tfrac14", font_size=24, color=C.EPS).next_to(ax.c2p(0.25, 0), DOWN, buff=0.15),
                      MathTex(r"\tfrac13", font_size=24, color=C.EPS).next_to(ax.c2p(0, Fq), LEFT, buff=0.15))
        with self.voiceover(
            "One more object to keep for later. <bookmark mark='r'/> Define a function on the Cantor set by reading a "
            "number's base-three digits, turning the twos into ones, and reading the result in base two. One quarter, "
            "0.0202 repeating, goes to 0.0101 repeating in binary, which is one third. <bookmark mark='f'/> Fill in each "
            "removed middle third with a flat step. As we add stages, the steps multiply."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), Create(S))
            vo.wait_until("r")
            self.play(FadeIn(rule))
            self.play(Create(qdrop), FadeIn(qdot, scale=2), FadeIn(qlab))
            vo.wait_until("f")
            for n in range(2, 9):
                self.play(Transform(S, stair(n)), run_time=0.6)
        with self.voiceover(
            "The limit is the devil's staircase. <bookmark mark='p'/> It's continuous and never decreases, it climbs "
            "from zero to one, and it's flat on every removed interval, which have total length one. All of the climbing "
            "happens on the Cantor set, a set of length zero. <bookmark mark='l'/> So its derivative is zero almost "
            "everywhere, and yet it rises. Keep it in mind: in Part 3 it will be an integrator, in Part 5 a measure, and "
            "in Part 6 the function for which the fundamental theorem of calculus fails."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(props))
            vo.wait_until("l")
            card = museum_card(r"The Cantor function", r"Cantor, 1884", r"``a function that rises has a positive slope''",
                               r"returns in Parts 3, 5, 6").scale(0.85).to_corner(DR, buff=0.25)
            self.play(FadeOut(props), FadeIn(card, shift=LEFT * 0.2))
        self.wait(0.6)
        self.clear_scene()
