from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.compute import load as load20
from videos.cs.cs46.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, mono, tag_box


class Sketches(VoiceoverScene):
    def construct(self):
        self.card()
        self.topk()
        self.distinct()
        self.quantiles()
        self.joins()
        self.merging()

    def card(self):
        card = chapter_card(6, r"Streaming algorithms in production", r"What can a stream remember in a few kilobytes?",
                            lit=(2007, 2016, 2019), extra=((2007, r"Flajolet et al.: \ HyperLogLog"),
                                                           (2016, r"Karnin, Lang and Liberty: \ KLL"),
                                                           (2019, r"Dunning and Ertl: \ t-digest")), part=PART)
        with self.voiceover("Chapter six. Streaming algorithms in production."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def topk(self):
        st = load20("stream")
        rows = st["mg"][:8]
        N, k, bound = st["N"], st["mg_k"], st["mg_bound"]
        head = label(r"Top-$k$ in one pass", font_size=36).to_edge(UP, buff=0.3)
        y0, H = -2.1, 3.9
        s = H / rows[0]["true"]
        bars, boxes, names = VGroup(), VGroup(), VGroup()
        for i, r in enumerate(rows):
            x = -6.0 + 0.92 * i
            t = Rectangle(width=0.32, height=r["true"] * s, stroke_width=0, fill_color=DATA, fill_opacity=0.85)
            t.move_to([x - 0.18, y0 + r["true"] * s / 2, 0])
            m = Rectangle(width=0.32, height=max(0.02, r["mg"] * s), stroke_width=0, fill_color=LAM,
                          fill_opacity=0.85)
            m.move_to([x + 0.18, y0 + r["mg"] * s / 2, 0])
            b = DashedVMobject(Rectangle(width=0.32, height=bound * s, stroke_color=LAM, stroke_width=1.5),
                               num_dashes=24).move_to([x + 0.18, y0 + (r["mg"] + bound / 2) * s, 0])
            bars.add(VGroup(t, m))
            boxes.add(b)
            names.add(mono(r["word"], size=16, color=GREY_A).move_to([x, y0 - 0.25, 0]))
        base = Line([-6.4, y0, 0], [0.9, y0, 0], color=GREY_C, stroke_width=1.5)
        legend = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=0.85),
                                 label(t, font_size=17, color=c)).arrange(RIGHT, buff=0.1)
                          for t, c in ((r"true count", DATA), (r"Misra--Gries", LAM))]).arrange(RIGHT, buff=0.4)
        legend.move_to([-2.75, 2.55, 0])
        mg0 = rows[0]
        notes = VGroup(
            wrapped_label(rf"Part 20's summary with {k - 1} counters, \ over the corpus's {N:,} words", 5.2,
                          font_size=20, color=WHITE),
            wrapped_label(rf"every count is low by at most $n/k$, \ about {bound:,.0f}: \ the true count lies in the "
                          r"dashed box above each estimate", 5.2, font_size=20, color=LAM),
            wrapped_label(rf"``{mg0['word']}'': \ true {mg0['true']:,}, \ estimate {mg0['mg']:,}; \ every word more "
                          r"frequent than the bound is certain to be kept", 5.2, font_size=20, color=HEAD),
            wrapped_label(r"in production: \ one summary per partition and per window, \ \textbf{merged} afterwards "
                          r"with the same guarantee \ (Agarwal et al., \ 2012)", 5.2, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.15, -0.1, 0])
        with self.voiceover(
            "The first question asked of a stream is often what is most frequent. <bookmark mark='a'/> Part 20's "
            f"Misra and Gries summary answers it in one pass, here with {k - 1} counters over {N / 1e6:.1f} million "
            "words. <bookmark mark='b'/> Every count it reports is low, but by at most the number of words divided "
            f"by {k}, about {bound / 1000:.0f} thousand, so the true count lies in the dashed box above each "
            "estimate, <bookmark mark='c'/> and any word more frequent than that is certain to be kept. "
            "<bookmark mark='d'/> In production what matters is that such summaries merge: each worker summarizes "
            "its own partition of each window, and the summaries combine with the same guarantee, as Pankaj Agarwal "
            "and his colleagues proved in 2012."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(names), FadeIn(legend))
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), LaggedStart(*[GrowFromEdge(b[1], DOWN) for b in bars], lag_ratio=0.1),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), Indicate(bars[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def distinct(self):
        h = load20("hll")
        rows = h["rows"]
        head = label(r"Distinct counts", font_size=36).to_edge(UP, buff=0.3)
        g = axes([1, 4.4, 1], [0, 2.0, 1], x_length=5.4, y_length=4.2,
                 x_label=r"memory \ (bytes, \ log scale)", y_label=r"relative error \ (root mean square)",
                 xticks=[1, 2, 3, 4], yticks=[0.4, 1.4],
                 fx=lambda v: f"{10 ** int(v):,}", fy=lambda v: r"1\%" if v < 1 else r"10\%")
        g.move_to([-3.5, -0.3, 0])
        ax = g.ax
        meas = [(math.log10(r["bytes"]), math.log10(r["rmse"]) + 2.4) for r in rows]      # 0.4 is 1%, 1.4 is 10%
        theo = [(math.log10(r["bytes"]), math.log10(r["theory"]) + 2.4) for r in rows]
        tl = DashedVMobject(VMobject().set_points_as_corners([ax.c2p(*p) for p in theo]), num_dashes=30).set_stroke(
            GREY_B, 1.5)
        ml = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in meas])
        md = VGroup(*[Dot(ax.c2p(*p), radius=0.06, color=YES) for p in meas])
        leg = VGroup(label(r"measured", font_size=16, color=YES),
                     label(r"$1.04/\sqrt{m}$", font_size=18, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                buff=0.12)
        leg.next_to(ax.c2p(2.7, 1.75), RIGHT, buff=0)
        A = [3, 1, 4, 2, 2, 5, 1, 3]
        B = [2, 4, 1, 2, 6, 1, 3, 3]

        def regs(vals, col, y):
            sq = VGroup(*[VGroup(Square(0.4, stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=0.15),
                                 mono(str(v), size=16, color=WHITE)) for v in vals]).arrange(RIGHT, buff=0.04)
            for s_ in sq:
                s_[1].move_to(s_[0])
            return sq.move_to([4.45, y, 0])
        ra, rb = regs(A, DATA, 2.4), regs(B, LAM, 1.9)
        rm = regs([max(a, b) for a, b in zip(A, B)], HEAD, 1.25)
        rlab = VGroup(label(r"sketch A", font_size=17, color=DATA).next_to(ra, LEFT, buff=0.2),
                      label(r"sketch B", font_size=17, color=LAM).next_to(rb, LEFT, buff=0.2),
                      label(r"A $\cup$ B: \ max", font_size=17, color=HEAD).next_to(rm, LEFT, buff=0.2))
        ill = note(r"illustrative registers", font_size=16).next_to(rm, DOWN, buff=0.1).align_to(rm, RIGHT)
        b12 = next(r for r in rows if r["b"] == 12)
        lo, hi = rows[0], rows[-1]
        notes = VGroup(
            wrapped_label(rf"HyperLogLog \ (Part 20), \ {h['distinct']:,} distinct words: \ "
                          rf"{100 * lo['rmse']:.0f}\% error with {lo['bytes']:.0f} bytes, \ {100 * hi['rmse']:.1f}\% "
                          rf"with {hi['bytes']:,.0f}", 5.2, font_size=19, color=WHITE),
            wrapped_label(rf"{b12['bytes']:,.0f} bytes: \ {h['est_corpus']:,.0f} estimated; \ and "
                          rf"{h['est_shingles']:,.0f} for {h['true_shingles']:,} distinct five-word phrases", 5.2,
                          font_size=19, color=YES),
            wrapped_label(r"merge: \ the larger register in each place; \ hours roll up into days, \ but never "
                          r"subtract", 5.2, font_size=19, color=HEAD),
            wrapped_label(r"BigQuery's \texttt{HLL\_COUNT} functions keep sketches in tables: \ HyperLogLog++ \ "
                          r"(Heule, \ Nunkesser and Hall, \ 2013)", 5.2, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ill, DOWN, buff=0.25).align_to(rlab, LEFT)
        with self.voiceover(
            "Counting distinct items exactly needs memory for every item. <bookmark mark='a'/> HyperLogLog, from "
            "Part 20, keeps only small registers, each holding the longest run of leading zeros among the hashes "
            f"that land in it. On the corpus's {h['distinct']:,} distinct words, its error falls from about a quarter "
            f"with {lo['bytes']:.0f} bytes to under one per cent with twelve kilobytes. <bookmark mark='b'/> Three "
            "kilobytes put the vocabulary within a fifth of a per cent, and count four and a half million distinct "
            "five-word phrases as well. <bookmark mark='c'/> Two sketches merge by keeping the larger register in "
            "each place, so hourly counts of distinct users roll up into daily ones. <bookmark mark='d'/> "
            "Warehouses store such sketches in tables, as BigQuery's HyperLogLog functions do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(tl), Create(ml), FadeIn(md), FadeIn(leg), FadeIn(notes[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), Indicate(md[[r["b"] for r in rows].index(12)], scale_factor=1.8))
            vo.wait_until("c")
            self.play(FadeIn(ra), FadeIn(rb), FadeIn(rlab[:2]), FadeIn(ill))
            self.play(TransformFromCopy(VGroup(ra, rb), rm), FadeIn(rlab[2]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def quantiles(self):
        q = load("quantiles")
        ex = q["exact"]
        qs = ["0.5", "0.99", "0.999"]
        head = label(r"Quantiles: \ KLL and t-digest", font_size=36).to_edge(UP, buff=0.3)
        lo, hi = 1.0, math.log10(500)

        def X(v):
            return -4.2 + (math.log10(v) - lo) / (hi - lo) * 9.6
        ys = [1.75, 1.2, 0.7, 0.2]
        names = [r"exact"] + [rf"KLL, \ {r['stored']:,} kept" for r in q["rows"]]
        rl = VGroup(*[label(t, font_size=17, color=WHITE if i == 0 else DATA).move_to([-4.6, y, 0],
                                                                                    aligned_edge=RIGHT)
                      for i, (t, y) in enumerate(zip(names, ys))])
        guides = VGroup(*[DashedLine([X(ex[k]), ys[0] + 0.25, 0], [X(ex[k]), ys[-1] - 0.25, 0], color=GREY_C,
                                     stroke_width=1.2) for k in qs])
        qn = VGroup(*[label(t, font_size=17, color=GREY_A).next_to(guides[i], UP, buff=0.08)
                      for i, t in enumerate((r"p50", r"p99", r"p99.9"))])
        exm = VGroup(*[Line([X(ex[k]), ys[0] - 0.15, 0], [X(ex[k]), ys[0] + 0.15, 0], color=WHITE, stroke_width=4)
                       for k in qs])
        exv = VGroup(*[label(f"{ex[k]:.0f}", font_size=16, color=WHITE).next_to(exm[i], RIGHT, buff=0.08)
                       for i, k in enumerate(qs)])
        est = VGroup()
        for r, y in zip(q["rows"], ys[1:]):
            est.add(VGroup(*[Dot([X(r["estimates"][k]), y, 0], radius=0.07, color=DATA) for k in qs]))
        estv = VGroup(*[label(f"{r['estimates']['0.999']:.0f}", font_size=16, color=DATA).next_to(
            est[i][2], LEFT, buff=0.25) for i, r in enumerate(q["rows"])])
        axis = Line([X(10), -0.15, 0], [X(500), -0.15, 0], color=GREY_C, stroke_width=1.5)
        tv = (10, 20, 50, 100, 200, 500)
        tks = VGroup(*[VGroup(Line([X(v), -0.2, 0], [X(v), -0.1, 0], color=GREY_C),
                              label(f"{v}", font_size=15, color=GREY_B).move_to([X(v), -0.38, 0])) for v in tv])
        axl = label(rf"{q['n']:,} simulated latencies \ (log scale)", font_size=16, color=GREY_B).next_to(
            tks, DOWN, buff=0.1).align_to(axis, RIGHT)
        r0 = q["rows"][0]
        ring = Circle(radius=0.17, color=NO, stroke_width=3).move_to(est[0][2])
        # t-digest: cluster boundaries from its scale function k1(q) = delta / (2 pi) asin(2q - 1), delta = 24
        delta = 24
        bnd = [(1 + math.sin(2 * math.pi * j / delta)) / 2 for j in range(-delta // 4, delta // 4 + 1)]
        x0, w = -4.2, 9.6
        td = VGroup(*[Rectangle(width=max(0.01, (b - a) * w - 0.02), height=0.36, stroke_width=0,
                                fill_color=YES if i % 2 else KERN, fill_opacity=0.75).move_to(
            [x0 + (a + b) / 2 * w, -1.6, 0]) for i, (a, b) in enumerate(zip(bnd, bnd[1:]))])
        tdl = label(r"t-digest's clusters, \ along the quantiles \ (schematic)", font_size=17, color=YES).next_to(
            td, UP, buff=0.12)
        ends = VGroup(label(r"$q = 0$", font_size=16, color=GREY_B).next_to(td, LEFT, buff=0.15),
                      label(r"$q = 1$", font_size=16, color=GREY_B).next_to(td, RIGHT, buff=0.15))
        lines = VGroup(
            wrapped_label(rf"KLL guarantees error in \textit{{rank}}: \ its p99.9 from {r0['stored']} items is off by "
                          rf"{100 * r0['rank_error']['0.999']:.1f}\% in rank, \ yet {r0['estimates']['0.999']:.0f} "
                          rf"against {ex['0.999']:.0f} in value, \ because the tail is where values spread out", 12.4,
                          font_size=19, color=NO),
            wrapped_label(r"t-digest \ (Dunning and Ertl, \ 2019) \ makes clusters small near the extremes and large "
                          r"near the median: \ accuracy where latency questions are asked, \ though without KLL's "
                          r"worst-case guarantee", 12.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Latency is judged by its median and its ninety-ninth percentile. <bookmark mark='a'/> A KLL sketch, by "
            "Zohar Karnin, Kevin Lang and Edo Liberty, keeps levels of samples, each level's items standing for "
            f"twice as many values as the level below. Over {q['n']:,} simulated latencies, keeping {r0['stored']} "
            "items, its median is close. <bookmark mark='b'/> But at the far tail its ninety-nine point nine "
            f"percentile is {r0['estimates']['0.999']:.0f} against a true {ex['0.999']:.0f}: less than one per cent wrong in "
            "rank, yet more than twice too low in value. <bookmark mark='c'/> Ted Dunning and Otmar Ertl's t-digest "
            "attacks the tail directly, with clusters that are large near the median and tiny near the extremes. "
            "KLL guarantees rank; t-digest is accurate where latency questions are asked."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(tks), FadeIn(axl), FadeIn(rl[0]), Create(guides),
                      FadeIn(qn), FadeIn(exm), FadeIn(exv))
            vo.wait_until("a")
            for i in range(3):
                self.play(FadeIn(rl[i + 1]), LaggedStart(*[FadeIn(d, scale=0.5) for d in est[i]], lag_ratio=0.2),
                          FadeIn(estv[i]), run_time=0.9)
            vo.wait_until("b")
            self.play(Create(ring), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(tdl), FadeIn(ends), LaggedStart(*[GrowFromCenter(r) for r in td], lag_ratio=0.05),
                      run_time=1.6)
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def joins(self):
        head = label(r"Windowed stream joins", font_size=36).to_edge(UP, buff=0.3)

        def X(t):
            return -5.2 + 0.47 * t
        yo, yp = 1.85, -0.25
        orders = [(1, 1), (2, 4), (3, 8), (4, 13)]          # (order number, minute)
        pays = [(1, 3), (2, 12), (4, 15), (3, 21)]
        win = 10
        lanes = VGroup(Line([X(0), yo, 0], [X(24), yo, 0], color=GREY_D, stroke_width=1.5),
                       Line([X(0), yp, 0], [X(24), yp, 0], color=GREY_D, stroke_width=1.5))
        ln = VGroup(label(r"orders", font_size=18, color=DATA).next_to(lanes[0], LEFT, buff=0.15),
                    label(r"payments", font_size=18, color=LAM).next_to(lanes[1], LEFT, buff=0.15))
        tks = VGroup(*[label(f"{t}", font_size=15, color=GREY_B).move_to([X(t), yp - 0.7, 0]) for t in (0, 5, 10, 15,
                                                                                                         20)])
        tu = label(r"event time \ (min)", font_size=15, color=GREY_B).move_to([X(23), yp - 0.7, 0])
        od = {o: VGroup(Dot([X(t), yo, 0], radius=0.09, color=DATA),
                        label(rf"\#{o}", font_size=16, color=DATA).next_to([X(t), yo, 0], UP, buff=0.14))
              for o, t in orders}
        pd = {o: VGroup(Dot([X(t), yp, 0], radius=0.09, color=LAM),
                        label(rf"\#{o}", font_size=16, color=LAM).next_to([X(t), yp, 0], DOWN, buff=0.14).shift(
                            RIGHT * 0.25))
              for o, t in pays}
        brk = VGroup()
        for i, (o, t) in enumerate(orders):
            y = 1.4 - 0.27 * i
            brk.add(VGroup(Line([X(t), y, 0], [X(t + win), y, 0], color=DATA, stroke_width=2, stroke_opacity=0.6),
                           Line([X(t + win), y - 0.08, 0], [X(t + win), y + 0.08, 0], color=DATA, stroke_width=2)))
        pt = dict(pays)
        ot = dict(orders)
        match = VGroup(*[Line([X(ot[o]), yo, 0], [X(pt[o]), yp, 0], color=YES, stroke_width=2.5)
                         for o in ot if pt[o] <= ot[o] + win])
        wm = ValueTracker(0.0)
        wline = always_redraw(lambda: DashedLine([X(wm.get_value()), yo + 0.55, 0], [X(wm.get_value()), yp - 0.05, 0],
                                                 color=HEAD, stroke_width=2))
        wlab = always_redraw(lambda: label(r"watermark", font_size=16, color=HEAD).next_to(
            [X(wm.get_value()), yo + 0.55, 0], UP, buff=0.05))
        sl = label(r"state: \ orders that may still match", font_size=18, color=GREY_A).move_to([-6.5, -1.5, 0],
                                                                                              aligned_edge=LEFT)
        chips = {o: tag_box(f"#{o}", color=DATA, size=16).next_to(sl, RIGHT, buff=0.3 + 0.95 * k)
                 for k, (o, _) in enumerate(orders)}
        lone = label(r"\#3 \ emitted alone, \ no payment", font_size=17, color=NO).next_to(
            chips[4], RIGHT, buff=0.4)
        late = Cross(pd[3][0], stroke_color=NO, stroke_width=4, scale_factor=1.6)
        ill = note(r"illustrative events", font_size=16).move_to([-6.6, 2.6, 0], aligned_edge=LEFT)
        lines = VGroup(
            wrapped_label(r"a payment matches an order with the same number in the 10 minutes after it; \ each order "
                          r"is held as state until the watermark passes the end of its interval", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"state is the event rate times the window: \ an hour-long join of a busy stream holds "
                          r"an hour of it; \ whether less can suffice is chapter 14's research problem", 12.4,
                          font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Joining two streams is harder than joining two tables, because neither side is ever complete. "
            "<bookmark mark='a'/> Here orders and payments are joined on the order number, and a payment counts if "
            "it comes within ten minutes of its order. <bookmark mark='b'/> Each order is kept as state while a "
            "payment could still arrive. Once the watermark passes ten minutes after it, the order leaves the "
            "state, joined, or in an outer join emitted alone. <bookmark mark='c'/> A payment that comes after "
            "that finds nothing. <bookmark mark='d'/> So the state is the event rate times the window. A join of a "
            "stream with a table, kept current from its change log as in chapter three, holds the table instead."
        ) as vo:
            self.play(FadeIn(head), Create(lanes), FadeIn(ln), FadeIn(tks), FadeIn(tu), FadeIn(ill))
            vo.wait_until("a")
            self.play(*[FadeIn(v) for v in od.values()], FadeIn(brk), FadeIn(lines[0]))
            self.play(*[FadeIn(pd[o]) for o in (1, 2, 4)], Create(match))
            vo.wait_until("b")
            self.play(FadeIn(sl), *[FadeIn(c) for c in chips.values()])
            self.add(wline, wlab)
            for o, t in orders:
                self.play(wm.animate.set_value(t + win + 0.2), run_time=1.0, rate_func=linear)
                if pt[o] <= t + win:
                    self.play(chips[o].animate.set_opacity(0.15), run_time=0.4)
                else:
                    self.play(chips[o].animate.set_opacity(0.15), FadeIn(lone), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(pd[3]))
            self.play(Create(late))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        wline.clear_updaters()
        wlab.clear_updaters()
        self.clear_scene()

    def merging(self):
        head = label(r"The property that matters: \ they merge", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"most frequent", r"Misra--Gries", r"$k$ counters", r"add, \ then shrink back to $k$"],
                [r"how many distinct", r"HyperLogLog", r"$m$ small registers", r"the larger of each register"],
                [r"how often each item", r"Count--Min", r"$d \times w$ counters", r"add cell by cell"],
                [r"quantiles", r"KLL, \ t-digest", r"weighted samples, \ clusters", r"combine, \ then compact"]]
        tab = grid_table([r"question", r"sketch \ (Part 20)", r"state", r"merge two by"], rows,
                         widths=[3.0, 2.7, 3.3, 3.8], row_h=0.55, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        parts = VGroup(*[tag_box(rf"partition {i}", color=DATA, size=15) for i in range(4)]).arrange(RIGHT, buff=0.3)
        parts.move_to([-3.0, -1.25, 0])
        mid = VGroup(*[tag_box(r"merged", color=LAM, size=15) for _ in range(2)])
        mid[0].move_to([(parts[0].get_x() + parts[1].get_x()) / 2, -2.15, 0])
        mid[1].move_to([(parts[2].get_x() + parts[3].get_x()) / 2, -2.15, 0])
        top = tag_box(r"the window's sketch", color=HEAD, size=15).move_to([-3.0, -3.05, 0])
        roll = VGroup(RoundedRectangle(width=3.6, height=0.5, corner_radius=0.08, stroke_color=YES, stroke_width=1.6,
                                       fill_color=BG, fill_opacity=1),
                      label(r"stored per hour, \ rolled up per day", font_size=17, color=YES)).move_to([3.2, -3.05, 0])
        roll[1].move_to(roll[0])
        ar = VGroup(*[Arrow(parts[i].get_bottom(), mid[i // 2].get_top(), buff=0.05, color=GREY_B, stroke_width=1.8,
                            max_tip_length_to_length_ratio=0.15) for i in range(4)],
                    *[Arrow(m.get_bottom(), top.get_top(), buff=0.05, color=GREY_B, stroke_width=1.8,
                            max_tip_length_to_length_ratio=0.15) for m in mid],
                    Arrow(top.get_right(), roll.get_left(), buff=0.1, color=GREY_B, stroke_width=1.8,
                          max_tip_length_to_length_ratio=0.1))
        side = wrapped_label(r"each worker sketches its share; \ a tree of merges gives the answer, \ with the same "
                             r"guarantee as one sketch of everything", 5.0, font_size=19, color=WHITE).move_to(
            [4.0, -1.6, 0])
        with self.voiceover(
            "These sketches share the property that matters most in production. <bookmark mark='a'/> Each can be "
            "built separately on every partition and every window, and two of them combine into one with the same "
            "guarantee: add the counters, keep the larger register, compact the combined samples. "
            "<bookmark mark='b'/> So a thousand workers each sketch their share, a tree of merges produces the "
            "answer, and the warehouse can store a sketch per hour and roll it up per day or per year. "
            "<bookmark mark='c'/> The warehouse is where chapter seven goes next."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[k])) for k in range(1, 5)], lag_ratio=0.4), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(parts), FadeIn(side))
            self.play(*[GrowArrow(a) for a in ar[:4]], FadeIn(mid))
            self.play(*[GrowArrow(a) for a in ar[4:6]], FadeIn(top))
            vo.wait_until("c")
            self.play(GrowArrow(ar[6]), FadeIn(roll))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN)
