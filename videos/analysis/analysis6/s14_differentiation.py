from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis6.common import left_y_axis, load, plain_axes, polyline
from videos.analysis.analysis6.compute import STEP_GAP, step_data


def window_average(jumps, vals, a, b):
    """The exact average of the step function over [a, b] (each step's overlap times its value)."""
    edges = np.concatenate([[0.0], jumps, [1.0]])
    a, b = max(a, 0.0), min(b, 1.0)
    ov = np.clip(np.minimum(edges[1:], b) - np.maximum(edges[:-1], a), 0, None)
    return float(ov @ vals / (b - a))


class Differentiation(VoiceoverScene):
    def construct(self):
        self.card()
        self.averages()
        self.maximal()
        self.vitali()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(13, r"Differentiating measures", r"Is a function the derivative of its integral?", lit=(),
                            part=6)
        with self.voiceover("Chapter thirteen: averages over shrinking intervals, and the Lebesgue differentiation "
                            "theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def averages(self):
        d = load("lebdiff")
        rs, good = d["rs"], d["good"]
        jumps, vals, _ = step_data()
        edges = np.concatenate([[0], jumps, [1]])
        assert np.diff(edges).min() >= STEP_GAP - 1e-12  # every step visible (>= 0.13 units wide)

        def f(t):
            return vals[np.searchsorted(jumps, t)]

        ax = plain_axes([0, 1, 0.25], [0, 1.1, 0.5], 7.2, 3.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-2.5, 0.2, 0])
        graph = VGroup(*[Line(ax.c2p(a, v), ax.c2p(b, v), color=C.FUNC, stroke_width=3.5)
                         for a, b, v in zip(edges[:-1], edges[1:], vals)])
        # a typical point inside a wide step, and a jump with wide steps on both sides, far apart
        k = 20
        x0 = float((jumps[k] + jumps[k + 1]) / 2 + 0.3 * (jumps[k + 1] - jumps[k]) / 2)
        jx = 3
        xj = float(jumps[jx])
        lo_v, hi_v = float(vals[jx]), float(vals[jx + 1])
        mid = 0.5 * (lo_v + hi_v)
        assert min(jumps[k + 1] - jumps[k], jumps[jx] - jumps[jx - 1], jumps[jx + 1] - jumps[jx]) > 0.04
        assert abs(hi_v - lo_v) > 0.4 and abs(x0 - xj) > 2 * 0.12 + 0.05  # the two windows never overlap
        rT = ValueTracker(0.12)

        def window(xc, col):
            def draw():
                r = rT.get_value()
                a, b = max(0.0, xc - r), min(1.0, xc + r)
                avg = window_average(jumps, vals, a, b)
                p0, p1 = ax.c2p(a, 0), ax.c2p(b, 1.1)
                return VGroup(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                                        fill_opacity=0.12).move_to((p0 + p1) / 2),
                              Line(ax.c2p(a, avg), ax.c2p(b, avg), color=col, stroke_width=5))
            return draw

        w1 = always_redraw(window(x0, C.EPS))
        w2 = always_redraw(window(xj, C.PATHOLOGY))
        fx0 = float(f(np.array([x0]))[0])
        d1 = Dot(ax.c2p(x0, fx0), radius=0.07, color=C.EPS)
        # the jump: its two values joined by a dashed red line, the midpoint marked
        jline = DashedLine(ax.c2p(xj, lo_v), ax.c2p(xj, hi_v), color=C.PATHOLOGY, stroke_width=2.5, dash_length=0.06)
        d2 = VGroup(jline, Dot(ax.c2p(xj, mid), radius=0.07, color=C.PATHOLOGY))
        # the readouts, checked: at the smallest r the typical point gives f(x) exactly, the jump its midpoint
        assert window_average(jumps, vals, x0 - 0.001, x0 + 0.001) == fx0
        assert abs(window_average(jumps, vals, xj - 0.001, xj + 0.001) - mid) < 1e-12

        def reads(keep):
            r = rT.get_value()
            g = VGroup(
                MathTex(rf"r = {r:.4f}", font_size=26),
                MathTex(rf"\text{{a typical point: average}} = {window_average(jumps, vals, x0 - r, x0 + r):.4f} \to "
                        rf"f(x) = {fx0:.4f}", font_size=26, color=C.EPS),
                MathTex(rf"\text{{a jump: average}} = {window_average(jumps, vals, xj - r, xj + r):.4f} \to "
                        rf"\text{{the midpoint}} = {mid:.4f}", font_size=26, color=C.PATHOLOGY),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax, DOWN, buff=0.2).align_to(ax, LEFT)
            return VGroup(*[g[i] for i in keep])

        rd = always_redraw(lambda: reads((0, 1)))
        rdj = always_redraw(lambda: reads((2,)))  # the jump's row comes in with the jump
        tab = VGroup(label(r"1000 random points:", font_size=24),
                     label(r"average $= f(x)$ exactly at", font_size=24))
        for r_, gv in zip(rs, good):
            tab.add(MathTex(rf"r = {sci(r_, 0)}: \ {100 * gv:.1f}\%", font_size=26, color=C.EPS))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.8, 0.6, 0])
        assert abs(good[-1] - 0.999) < 1e-12 and np.all(np.diff(good) >= 0)
        thm = VGroup(
            label(r"\textbf{RCA 7.7} \ for $f \in L^1(\R^k)$,", font_size=26),
            label(r"almost every $x$ is a Lebesgue point:", font_size=26),
            MathTex(r"\lim_{r \to 0} \frac{1}{m(B_r)} \int_{B_r(x)} |f - f(x)|\,dm = 0,", font_size=30, color=C.EPS),
            MathTex(r"\text{so} \quad \frac{d}{dx}\int_a^x f = f(x) \ \text{a.e.}", font_size=30, color=C.EPS),
        )
        for r_ in thm:
            if r_.width > 4.15:
                r_.width = 4.15
        thm.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to([2.4, -1.15, 0], DR, buff=0)  # right column, below the readouts
        assert thm.get_right()[0] <= 6.6
        head = label(r"Average $f$ over a shrinking interval: \ do you get $f(x)$ back?", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Average a function over a small interval around x. As the interval shrinks, do "
            "you get f of x back? <bookmark mark='b'/> Here's a step function with thirty random jumps. At a typical "
            "point, the yellow average becomes exactly f of x once the interval is inside one step. "
            "<bookmark mark='c'/> At a jump, the average tends to the midpoint of the jump instead. "
            "<bookmark mark='d'/> Over a thousand random points, the fraction that works climbs to 99.9 percent: the "
            "failures are the jumps, a set of measure zero. <bookmark mark='e'/> Lebesgue's theorem says this "
            "happens for every integrable function: almost every point is a Lebesgue point. In particular, the "
            "derivative of the integral is the function, almost everywhere."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), LaggedStart(*[Create(s_) for s_ in graph], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(d1), FadeIn(w1), FadeIn(rd))
            vo.wait_until("c")
            self.play(FadeIn(d2), FadeIn(w2), FadeIn(rdj))
            self.play(rT.animate.set_value(0.001), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(tab[:2]))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(thm))
        for m in (w1, w2, rd, rdj):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def maximal(self):
        d = load("maximal")
        xs, Mf, lams, level = d["xs"], d["Mf"], d["lams"], d["level"]
        ax = plain_axes([-1, 2, 0.5], [0, 1.15, 0.5], 7.4, 3.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"include_numbers": False}).move_to([-2.0, 0.0, 0])
        ynum = left_y_axis(ax, (0.5, 1.0), decimals=1)  # at x = -1: the level line never crosses a number
        f = VGroup(Line(ax.c2p(-1, 0), ax.c2p(0.4, 0), color=C.FUNC, stroke_width=3),
                   Line(ax.c2p(0.4, 1), ax.c2p(0.6, 1), color=C.FUNC, stroke_width=4),
                   Line(ax.c2p(0.6, 0), ax.c2p(2, 0), color=C.FUNC, stroke_width=3))
        fa = Rectangle(width=ax.c2p(0.6, 0)[0] - ax.c2p(0.4, 0)[0], height=ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1],
                       stroke_width=0, fill_color=C.FUNC, fill_opacity=0.3).move_to(ax.c2p(0.5, 0.5))
        f_l = MathTex(r"f = \mathbf 1_{[0.4,\, 0.6]}", font_size=26, color=C.FUNC).next_to(ax.c2p(0.6, 1), RIGHT, buff=0.15)
        gM = polyline(ax, xs, Mf, color=C.EPS, stroke_width=3.5)
        M_l = MathTex(r"Mf(x) = \sup_{r > 0} \frac{1}{2r}\int_{x - r}^{x + r} |f|", font_size=28, color=C.EPS).next_to(
            ax, UP, buff=0.1)
        lamT = ValueTracker(float(lams[0]))

        def lvl():
            lam = lamT.get_value()
            # {Mf > lam} = (b - (b - a) / (2 lam), a + (b - a) / (2 lam))
            lo, hi = 0.6 - (0.2 / (2 * lam)), 0.4 + 0.2 / (2 * lam)
            return VGroup(DashedLine(ax.c2p(-1, lam), ax.c2p(2, lam), color=C.APPROX, stroke_width=2),
                          Line(ax.c2p(max(lo, -1), 0.02), ax.c2p(min(hi, 2), 0.02), color=C.APPROX, stroke_width=8))

        lv = always_redraw(lvl)
        tab = VGroup(MathTex(r"\lambda", r"\quad m\{Mf > \lambda\}", r"\quad 3\|f\|_1/\lambda", font_size=26, color=GREY_A))
        for lam, lv_ in zip(lams, level):
            tab.add(MathTex(f"{lam}", rf"\quad {lv_:.2f}", rf"\quad {3 * 0.2 / lam:.2f}", font_size=26, color=C.APPROX))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        widths = [max(r_[j].width for r_ in tab) for j in range(3)]
        lefts = np.concatenate([[0], np.cumsum(np.array(widths) + 0.25)[:-1]])
        for r_ in tab:  # a real grid
            for j in range(3):
                r_[j].set_x(lefts[j] + r_[j].width / 2)
        tab.move_to([4.7, 0.4, 0])
        assert np.all(level <= 3 * 0.2 / lams)
        # check the level sets against the computed Mf
        for lam, lv_ in zip(lams, level):
            dx = xs[1] - xs[0]
            assert abs(np.sum(Mf > lam) * dx - lv_) < 0.02
        notes = VGroup(
            label(r"\textbf{RCA 7.4} \ (Hardy--Littlewood, 1930) \ $m\{Mf > \lambda\} \le 3^k \|f\|_1 / \lambda$",
                  font_size=24, color=C.EPS),
            label(r"$Mf \approx \frac{0.1}{|x|}$ far away: \ not integrable, \ but its level sets are controlled",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.4)
        head = label(r"The maximal function: \ the worst average at each point", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The proof needs a way to control all the averages at once. The maximal function "
            "takes, at each point, the largest average over all intervals centered there. "
            "<bookmark mark='b'/> For the indicator of a short interval, it's one on the interval, and outside it "
            "decays like one over the distance. It's not integrable. <bookmark mark='c'/> But the set where it "
            "exceeds lambda is small, at most three times the integral of f over lambda. That's the Hardy-Littlewood "
            "maximal inequality, and the three comes from a covering lemma."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(ynum), FadeIn(fa), Create(f), FadeIn(f_l))
            self.play(FadeIn(M_l))
            vo.wait_until("b")
            self.play(Create(gM), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(lv), FadeIn(tab[0]), FadeIn(tab[1]))
            for i in range(1, len(lams)):
                self.play(lamT.animate.set_value(float(lams[i])), FadeIn(tab[i + 1]), run_time=1.2)
            self.play(FadeIn(notes))
        lv.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vitali(self):
        d = load("lebdiff")
        c, L, chosen, m_union, m_chosen = d["c"], d["L"], d["chosen"], float(d["m_union"]), float(d["m_chosen"])
        runs_ = d["runs"]
        assert np.all(c - L / 2 >= 0) and np.all(c + L / 2 <= 1)  # every interval inside [0, 1]
        assert abs(float(np.sum(runs_[:, 1] - runs_[:, 0])) - m_union) < 1e-12 and m_union <= 3 * m_chosen
        x0, W = -5.4, 7.2  # room for the 3x enlargements (they reach -0.11 and 1.11) and the labels
        X = lambda t: x0 + W * t  # noqa: E731

        def stack(lo, hi, gap):
            """Rows for intervals [lo_i, hi_i]: each goes into the first row where it clears the last one by gap."""
            ends, row = [], {}
            for i in np.argsort(lo):
                for k, e in enumerate(ends):
                    if lo[i] > e + gap:
                        ends[k], row[i] = hi[i], k
                        break
                else:
                    ends.append(hi[i])
                    row[i] = len(ends) - 1
            return row, len(ends)

        row_of, nrows = stack(c - L / 2, c + L / 2, 0.012)
        top, dy = 2.25, min(0.22, 2.6 / nrows)
        segs = VGroup()
        for i in range(len(c)):
            y = top - dy * row_of[i]
            segs.add(Line([X(c[i] - L[i] / 2), y, 0], [X(c[i] + L[i] / 2), y, 0], color=GREY_B, stroke_width=4))
        hl = VGroup(*[segs[i].copy().set_color(C.EPS).set_stroke(width=6) for i in chosen])
        # the 3x enlargements of the chosen ones, on as few rows as keep them apart
        e_lo, e_hi = c[chosen] - 1.5 * L[chosen], c[chosen] + 1.5 * L[chosen]
        erow, nerow = stack(e_lo, e_hi, 0.01)
        ytop_e = top - dy * (nrows - 1) - 0.45
        enl = VGroup(*[Line([X(e_lo[j]), ytop_e - 0.2 * erow[j], 0], [X(e_hi[j]), ytop_e - 0.2 * erow[j], 0],
                            color=C.APPROX, stroke_width=6) for j in range(len(chosen))])
        yu = ytop_e - 0.2 * (nerow - 1) - 0.45
        ubar = VGroup(*[Line([X(a), yu, 0], [X(b), yu, 0], color=C.MEASURE, stroke_width=8) for a, b in runs_])
        lab = VGroup(label(r"all 60 intervals", font_size=22, color=GREY_B).next_to([X(1.13), top, 0], RIGHT, buff=0.2),
                     VGroup(label(r"chosen: \ greedy,", font_size=22, color=C.EPS),
                            label(r"longest first, \ disjoint", font_size=22, color=C.EPS)).arrange(
                         DOWN, aligned_edge=LEFT, buff=0.08),
                     label(r"chosen, \ enlarged $3\times$", font_size=22, color=C.APPROX).next_to(
                         [X(1.13), ytop_e - 0.1 * (nerow - 1), 0], RIGHT, buff=0.2),
                     label(r"their union", font_size=22, color=C.MEASURE).next_to([X(1.13), yu, 0], RIGHT, buff=0.2))
        lab[1].next_to(lab[0], DOWN, buff=0.1).align_to(lab[0], LEFT)
        nums = VGroup(
            MathTex(rf"m(\text{{union}}) = {m_union:.3f}", font_size=28, color=C.MEASURE),
            MathTex(rf"3 \sum_{{\text{{chosen}}}} m(I_j) = 3 \times {m_chosen:.3f} = {3 * m_chosen:.3f}", font_size=28,
                    color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.4).shift(LEFT * 2.0)
        why_ = label(r"each interval meets a chosen one at least as long, \ so it lies in that one's $3\times$ enlargement",
                     font_size=22, color=GREY_A).next_to(nums, UP, buff=0.12).align_to(nums, LEFT)
        rca = label(r"\textbf{RCA 7.3}", font_size=24, color=GREY_A).next_to(lab[0], UP, buff=0.2).align_to(lab[0], LEFT)
        pm = ProofMap([r"Vitali: \ $3\times$", r"$m\{Mf > \lambda\} \le 3\|f\|_1/\lambda$",
                       r"$f = g + (f - g)$, \ $g$ continuous", r"bad set: \ measure $\le 6\varepsilon/\lambda$, \ any $\varepsilon$"],
                      font_size=18, width=3.0, buff=0.3).to_edge(DOWN, buff=0.3)
        head = label(r"The Vitali covering lemma: \ a disjoint subfamily whose triples cover", font_size=34).to_edge(
            UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Here's the covering lemma, with sixty random intervals. <bookmark mark='b'/> Pick "
            "greedily: the longest interval, then the longest one disjoint from it, and so on. "
            "<bookmark mark='c'/> Every interval meets a chosen one at least as long, so it lies inside that one, "
            "enlarged three times. <bookmark mark='d'/> So the union, of measure 0.965, is at most three times the "
            "chosen total, 0.81. <bookmark mark='e'/> That gives the maximal inequality. Then approximate f by a "
            "continuous function, which has every point as a Lebesgue point. The error is small in L one, so by the "
            "maximal inequality, the set where things go wrong has measure as small as we like: zero."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), LaggedStart(*[Create(s_) for s_ in segs], lag_ratio=0.02), FadeIn(lab[0]),
                      FadeIn(rca), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(h_) for h_ in hl], lag_ratio=0.2), FadeIn(lab[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(e_) for e_ in enl], lag_ratio=0.1), FadeIn(lab[2]), FadeIn(why_),
                      run_time=2.0)
            vo.wait_until("d")
            self.play(Create(ubar), FadeIn(lab[3]))
            self.play(FadeIn(nums))
            vo.wait_until("e")
            self.play(FadeOut(nums), FadeOut(why_), FadeIn(pm))
            for k in range(4):
                self.play(*pm.light(k), run_time=0.6)
            self.play(*pm.done())
        self.wait(0.4)
        self.clear_scene()
