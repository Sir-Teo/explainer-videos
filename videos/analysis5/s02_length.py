from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import interval_band, load, plain_axes
from videos.analysis5.compute import cantor_intervals


class Length(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.rationals()
        self.cantor()
        self.fat()
        self.interval()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"A length for every set", r"How long is the set of rationals? \ The Cantor set?",
                            lit=(1902,), part=5)
        with self.voiceover("Chapter one: how to give a length to sets that are not intervals."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def line(self, y=0.0):
        return NumberLine(x_range=[0, 1, 0.25], length=11.0, include_numbers=True, font_size=22,
                          decimal_number_config={"num_decimal_places": 2}).move_to([0, y, 0])

    # ------------------------------------------------------------------
    def definition(self):
        nl = self.line(-0.3)
        ax = plain_axes([0, 1, 1], [0, 1, 1], 11.0, 1.0).move_to(nl.get_center())
        ax.set_opacity(0)
        E = [(0.08, 0.22), (0.31, 0.36), (0.52, 0.71), (0.83, 0.86)]
        pts = [0.42, 0.47, 0.93]
        Eb = interval_band(ax, E, nl.get_y(), C.FUNC, height=0.16)
        Ep = VGroup(*[Dot(nl.n2p(p), radius=0.06, color=C.FUNC) for p in pts])
        covers = [
            [(0.0, 0.5), (0.45, 1.0)],
            [(0.05, 0.4), (0.4, 0.5), (0.5, 0.74), (0.8, 0.95)],
            [(0.07, 0.23), (0.30, 0.37), (0.41, 0.43), (0.46, 0.48), (0.51, 0.72), (0.82, 0.87), (0.92, 0.94)],
        ]
        bands, totals = [], []
        for k, cv in enumerate(covers):
            bands.append(interval_band(ax, cv, nl.get_y() + 0.55 + 0.0 * k, C.MEASURE, height=0.22, opacity=0.5))
            totals.append(MathTex(rf"\sum \ell(I_k) = {sum(b - a for a, b in cv):.2f}", font_size=30, color=C.MEASURE)
                          .next_to(nl, DOWN, buff=0.7))
        lenE = sum(b - a for a, b in E)
        assert all(sum(b - a for a, b in cv) >= lenE for cv in covers)
        head = VGroup(label(r"\textbf{Outer measure} \ (Lebesgue, 1902)", font_size=32),
                      MathTex(r"m^*(E) = \inf\Big\{ \sum_k \ell(I_k) : E \subset \bigcup_k I_k,\ I_k \text{ intervals}\Big\}",
                              font_size=36, color=C.MEASURE)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        props = VGroup(label(r"monotone: \ $A \subset B \Rightarrow m^*(A) \le m^*(B)$", font_size=26),
                       label(r"countably subadditive: \ $m^*(\bigcup E_k) \le \sum m^*(E_k)$", font_size=26),
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.3)
        el = MathTex("E", font_size=32, color=C.FUNC).next_to(nl.n2p(0.15), DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Lebesgue's idea, from his thesis of 1902: cover a set by countably many intervals, "
            "add up their lengths, and take the smallest total you can get. That's the outer measure. "
            "<bookmark mark='b'/> Here's a set made of a few intervals and points. A crude cover has total length "
            "one. <bookmark mark='c'/> Tighter covers do better, <bookmark mark='d'/> and the infimum over all "
            "countable covers is the outer measure. Two properties are immediate: bigger sets have bigger outer "
            "measure, and the outer measure of a countable union is at most the sum of the outer measures."
        ) as vo:
            self.play(FadeIn(head[0]), Create(nl))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.play(FadeIn(Eb), FadeIn(Ep), FadeIn(el))
            self.play(FadeIn(bands[0]), FadeIn(totals[0]))
            vo.wait_until("c")
            self.play(ReplacementTransform(bands[0], bands[1]), FadeTransform(totals[0], totals[1]))
            vo.wait_until("d")
            self.play(ReplacementTransform(bands[1], bands[2]), FadeTransform(totals[1], totals[2]))
            self.play(FadeIn(props))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rationals(self):
        d = load("cantor")
        rats, cover, eps = d["rats"], d["cover"], float(d["eps"])
        nl = self.line(-0.8)
        ax = plain_axes([0, 1, 1], [0, 1, 1], 11.0, 1.0).move_to(nl.get_center())
        ax.set_opacity(0)
        K = 40
        dots = VGroup(*[Dot(nl.n2p(float(q)), radius=0.035, color=C.RATIONAL) for q in rats[:400]])
        boxes = VGroup()
        for k in range(K):
            q, w = float(rats[k]), float(cover[k])
            pa, pb = nl.n2p(q - w / 2)[0], nl.n2p(q + w / 2)[0]
            boxes.add(Rectangle(width=max(pb - pa, 0.01), height=0.5, stroke_color=C.MEASURE, stroke_width=1.5,
                                fill_color=C.MEASURE, fill_opacity=0.35).move_to([(pa + pb) / 2, nl.get_y() + 0.45, 0]))
        kT = ValueTracker(0)
        total = always_redraw(lambda: MathTex(
            rf"\text{{first {int(kT.get_value())} rationals: total }} = \varepsilon\,(1 - 2^{{-{int(kT.get_value())}}}) "
            rf"< \varepsilon = {eps}", font_size=30, color=C.MEASURE).next_to(nl, DOWN, buff=0.7))
        head = VGroup(label(r"The rationals have outer measure $0$", font_size=32),
                      MathTex(r"q_1, q_2, q_3, \dots \text{ listed (Part 1)}; \quad \text{cover } q_k \text{ by an interval "
                              r"of length } \varepsilon / 2^k", font_size=30)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        out = label(r"total $\le \varepsilon$, \ for every $\varepsilon > 0$: \ $m^*(\mathbb Q \cap [0, 1]) = 0$",
                    font_size=28, color=C.EPS).to_edge(DOWN, buff=0.35)
        assert cover[:K].sum() < eps
        with self.voiceover(
            "<bookmark mark='a'/> The rationals between zero and one are dense, but they can be listed, as Part 1 "
            "showed. <bookmark mark='b'/> Cover the first by an interval of length epsilon over two, the second by "
            "epsilon over four, the k-th by epsilon over two to the k. <bookmark mark='c'/> Together the intervals "
            "have total length less than epsilon, and every rational is covered. Since epsilon was arbitrary, the "
            "rationals have outer measure zero: dense, but no length at all."
        ) as vo:
            self.play(FadeIn(head[0]), Create(nl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.003), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(head[1]), FadeIn(total))
            self.play(LaggedStart(*[FadeIn(b_) for b_ in boxes], lag_ratio=0.15), kT.animate.set_value(K),
                      run_time=5.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(out))
        total.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cantor(self):
        d = load("cantor")
        depths, tot = d["depths"], d["tot"]
        ax = plain_axes([0, 1, 1], [0, 1, 1], 9.3, 1.0).move_to([-2.15, 0, 0])
        ax.set_opacity(0)
        rows = VGroup()
        labs = VGroup()
        for k in range(7):
            y = 1.9 - 0.62 * k
            rows.add(interval_band(ax, cantor_intervals(k), y, C.CLOSED_SET, height=0.2, min_width=0.008))
            labs.add(MathTex(rf"2^{{{k}}} \text{{ intervals, total }} (\tfrac23)^{{{k}}} = {tot[k]:.4f}", font_size=24,
                             color=C.MEASURE).next_to([2.95, y, 0], RIGHT, buff=0.0))
        head = label(r"The Cantor set: \ uncountable, \ and outer measure $0$", font_size=32).to_edge(UP, buff=0.3)
        out = label(r"its stage-$n$ intervals cover it with total $(2/3)^n \to 0$", font_size=26,
                    color=C.EPS).to_edge(DOWN, buff=0.35)
        assert np.allclose(tot, (2 / 3) ** depths)
        with self.voiceover(
            "<bookmark mark='a'/> Part 1's Cantor set is uncountable, as big as the whole interval by counting. "
            "<bookmark mark='b'/> But its stages cover it: two to the n intervals with total length two thirds to the "
            "n, which goes to zero. <bookmark mark='c'/> So the Cantor set has outer measure zero. Counting and "
            "measuring are different kinds of size."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(labs[0]))
            vo.wait_until("b")
            for k in range(1, 7):
                self.play(TransformFromCopy(rows[k - 1], rows[k]), FadeIn(labs[k]), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(out))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fat(self):
        d = load("cantor")
        meas = d["stage_meas"]
        ax = plain_axes([0, 1, 1], [0, 1, 1], 9.3, 1.0).move_to([-2.15, 0, 0])
        ax.set_opacity(0)
        rows, labs = VGroup(), VGroup()
        for k in range(6):
            y = 1.7 - 0.62 * k
            rows.add(interval_band(ax, d[f"fat{k}"], y, C.CONNECTED_SET, height=0.2, min_width=0.008))
            labs.add(MathTex(rf"\text{{measure }} {meas[k]:.6f}", font_size=24, color=C.MEASURE).next_to([2.95, y, 0], RIGHT,
                                                                                                       buff=0))
        head = VGroup(label(r"A fat Cantor set: \ remove middle intervals of length $4^{-n}$ at stage $n$", font_size=30),
                      ).to_edge(UP, buff=0.3)
        out = VGroup(MathTex(rf"\text{{measure }} = 1 - \sum_{{n \ge 1}} 2^{{n-1}} 4^{{-n}} = \tfrac12", font_size=32,
                             color=C.EPS),
                     label(r"yet it contains no interval \ (its pieces shrink to $0$): \ thin, but not small",
                           font_size=26, color=C.PATHOLOGY)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        assert abs(float(d["fat_measure"]) - 0.5) < 1e-3
        # the first piece after stage 5, magnified: the depth-12 set inside it (stages 6..12, 128 pieces)
        keep12 = d["fat_keep"]
        a5 = float(d["fat5"][0][1])
        zin = keep12[keep12[:, 1] <= a5 + 1e-12] / a5
        assert len(zin) == 2**7 and abs(zin.max() - 1) < 1e-9 and zin.min() == 0
        lens = [float(np.diff(d[f"fat{k}"], axis=1).max()) for k in range(1, 6)]
        assert all(a > 2 * b for a, b in zip(lens, lens[1:]))  # each stage more than halves the longest piece
        y5, zy = 1.2, -0.2
        zbar = interval_band(ax, zin, zy, C.CONNECTED_SET, height=0.3, min_width=0.004)
        xa, xb = ax.c2p(0, 0)[0], ax.c2p(a5, 0)[0]
        win = Rectangle(width=xb - xa + 0.08, height=0.34, stroke_color=C.EPS, stroke_width=2.5).move_to(
            [(xa + xb) / 2, y5, 0])
        conn = VGroup(DashedLine(win.get_corner(DL), [ax.c2p(0, 0)[0], zy + 0.17, 0], color=C.EPS, stroke_width=1.5),
                      DashedLine(win.get_corner(DR), [ax.c2p(1, 0)[0], zy + 0.17, 0], color=C.EPS, stroke_width=1.5))
        zlab = MathTex(rf"\times {1 / a5:.0f}: \ \text{{stages }} 6\text{{--}}12", font_size=24, color=C.EPS
                       ).next_to([2.95, zy, 0], RIGHT, buff=0)
        plab = label(r"longest piece after stage $n$: \ " + r", \ ".join(f"{v:.3f}" for v in lens) + r", \ \dots \ $\to 0$",
                     font_size=24, color=GREY_A).move_to([ax.get_center()[0], -0.95, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now change the recipe. At stage n, remove from the middle of each piece an interval "
            "of length only four to the minus n. <bookmark mark='b'/> The removed lengths add up to one half, so what "
            "remains has measure one half. <bookmark mark='c'/> Yet the remaining pieces shrink to nothing: "
            "each stage more than halves the longest one. <bookmark mark='z'/> Magnify a piece sixty times and the "
            "same pattern of holes is there again. So the set contains no interval at all. It's nowhere dense, full of holes everywhere, and still has half the "
            "length of the line. Being thin and having measure zero are different things."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(labs[0]))
            for k in range(1, 6):
                self.play(TransformFromCopy(rows[k - 1], rows[k]), FadeIn(labs[k]), run_time=0.7)
            vo.wait_until("b")
            self.play(FadeIn(out[0]))
            vo.wait_until("c")
            self.play(FadeOut(rows[:5]), FadeOut(labs[:5]), VGroup(rows[5], labs[5]).animate.shift(UP * (y5 - rows[5].get_y())))
            self.play(FadeIn(plab))
            vo.wait_until("z")
            self.play(Create(win))
            self.play(Create(conn), GrowFromEdge(zbar, LEFT), FadeIn(zlab), run_time=1.6)
            self.play(FadeIn(out[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def interval(self):
        rng = np.random.default_rng(6)
        # a finite chain of open intervals covering [0, 1] (as a finite subcover would be), each overlapping the next
        ends, pos = [], -0.05
        while pos < 1:
            w = rng.uniform(0.12, 0.3)
            a = pos - rng.uniform(0.02, 0.06)
            ends.append((a, a + w))
            pos = a + w
        ends = np.array(ends)
        total = float(np.sum(ends[:, 1] - ends[:, 0]))
        assert ends[0, 0] < 0 and ends[-1, 1] > 1 and all(ends[i + 1, 0] < ends[i, 1] for i in range(len(ends) - 1))
        assert total >= 1
        nl = self.line(-0.6)
        bars = VGroup()
        for k, (a, b) in enumerate(ends):
            pa, pb = nl.n2p(max(a, -0.08))[0], nl.n2p(min(b, 1.08))[0]
            bars.add(Rectangle(width=pb - pa, height=0.22, stroke_color=C.MEASURE, stroke_width=1.5, fill_color=C.MEASURE,
                               fill_opacity=0.4).move_to([(pa + pb) / 2, nl.get_y() + 0.45 + 0.28 * (k % 2), 0]))
        seg = Line(nl.n2p(0), nl.n2p(1), color=C.FUNC, stroke_width=8)
        head = VGroup(label(r"Is the outer measure of $[a, b]$ really $b - a$?", font_size=32),
                      label(r"$\le$ is clear; \ $\ge$ needs compactness \ (Heine--Borel, Part 1)", font_size=26,
                            color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        rows = VGroup(
            label(r"widen each $I_k$ a little to an open interval: \ total grows by at most $\varepsilon$", font_size=24),
            label(r"compactness: \ finitely many already cover $[a, b]$", font_size=24),
            label(r"finitely many overlapping intervals that span $[a, b]$ have total length $\ge b - a$", font_size=24),
            MathTex(rf"\text{{here: }} {len(ends)} \text{{ intervals, total }} {total:.3f} \ge 1", font_size=30,
                    color=C.MEASURE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> A sanity check: does an interval get its usual length? Covering it by itself shows "
            "the outer measure is at most b minus a. The other direction is where compactness enters. "
            "<bookmark mark='b'/> Widen each interval of a countable cover slightly to an open one, at a total cost "
            "of epsilon. By Heine–Borel, finitely many of them already cover the closed interval, <bookmark mark='c'/> "
            "and finitely many intervals that chain across it must have total length at least its length. So the "
            "outer measure of an interval is its length, as it should be."
        ) as vo:
            self.play(FadeIn(head), Create(nl), Create(seg))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()
