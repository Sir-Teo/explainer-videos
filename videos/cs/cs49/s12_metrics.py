from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs49.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, bar_chart, grid_table, load,
                                   module_box, mono)


class Metrics(VoiceoverScene):
    def construct(self):
        self.card()
        self.pipeline()
        self.cardinality()
        self.napkin()
        self.downsample()
        self.tiers()

    def card(self):
        card = chapter_card(11, r"A metrics pipeline", r"How do you keep a number about everything, \ every ten "
                            r"seconds?", lit=(2012, 2015), extra=((2012, r"Prometheus begun at SoundCloud"),
                                                                 (2015, r"Pelkonen et al.: \ Gorilla")), part=PART)
        with self.voiceover("Chapter eleven. A metrics pipeline."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def pipeline(self):
        head = label(r"Requirements, \ and the pipeline", font_size=36).to_edge(UP, buff=0.3)
        sample = mono('requests_total{service="cart", status="200"}   12:00:10   1042', size=18, color=DATA)
        sample.next_to(head, DOWN, buff=0.45)
        parts = VGroup(label(r"name and labels", font_size=16, color=GREY_B),
                       label(r"time", font_size=16, color=GREY_B), label(r"value", font_size=16, color=GREY_B))
        n_chars = len('requests_total{service="cart", status="200"}   12:00:10   1042')
        cw = sample.width / n_chars
        x0 = sample.get_left()[0]
        for p, (a, b) in zip(parts, ((0, 44), (47, 55), (58, 62))):
            p.move_to([x0 + cw * (a + b) / 2, sample.get_bottom()[1] - 0.2, 0])
        specs = [(r"services", r"emit counters", DATA), (r"agents", r"scrape or push", DATA),
                 (r"log", r"absorbs bursts \ (Part 46)", LAM), (r"ingesters", r"shard by series", KERN),
                 (r"TSDB shards", r"recent data, \ hot", KERN), (r"queries", r"dashboards, \ alerts", YES)]
        boxes = VGroup(*[module_box(n, c, w=1.85, h=0.6) for n, _, c in specs]).arrange(RIGHT, buff=0.4)
        boxes.move_to([0, 0.75, 0])
        subs = VGroup(*[wrapped_label(s, 1.9, font_size=16, color=GREY_B).next_to(b, DOWN, buff=0.12)
                        for b, (_, s, _) in zip(boxes, specs)])
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.04, color=GREY_C,
                                stroke_width=2, max_tip_length_to_length_ratio=0.3) for i in range(5)])
        down = module_box(r"downsampler", LAM, w=1.85, h=0.55).move_to([boxes[4].get_x(), -1.15, 0])
        cold = module_box(r"object storage", GREY_B, w=2.1, h=0.55).next_to(down, LEFT, buff=0.7)
        cl = label(r"Part 45", font_size=16, color=GREY_B).next_to(cold, DOWN, buff=0.1)
        a_down = Arrow(subs[4].get_bottom(), down.get_top(), buff=0.06, color=GREY_C, stroke_width=2)
        a_cold = Arrow(down.get_left(), cold.get_right(), buff=0.06, color=GREY_C, stroke_width=2)
        reqs = wrapped_label(r"writes far outnumber reads; \ samples arrive in time order and are never updated; \ "
                             r"recent data is read most; \ queries aggregate over time and labels", 12.4,
                             font_size=20, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Every service in a large system reports numbers about itself: requests, errors, latencies, queue "
            "depths. <bookmark mark='a'/> Each sample is a metric's name, a set of labels, a time and a value. "
            "<bookmark mark='b'/> Agents scrape or receive the samples and push them into a log, Part 46's, which "
            "absorbs bursts. Ingesters shard them by a hash of the series and append them to a time-series store, "
            "and a downsampler moves older data to object storage. <bookmark mark='c'/> The workload is unusual. "
            "Writes far outnumber reads, samples arrive in time order and are never updated, recent data is read "
            "most, and queries aggregate across time and labels."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sample), FadeIn(parts))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(b, s)) for b, s in zip(boxes, subs)], lag_ratio=0.25),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25), run_time=2.5)
            dot = Dot(boxes[0].get_center(), radius=0.09, color=HEAD)
            self.add(dot)
            for b in boxes[1:]:
                self.play(dot.animate.move_to(b.get_center()), run_time=0.45)
            self.play(FadeOut(dot), GrowArrow(a_down), FadeIn(down), GrowArrow(a_cold), FadeIn(cold), FadeIn(cl))
            vo.wait_until("c")
            self.play(FadeIn(reqs))
        self.wait(0.4)
        self.clear_scene()

    def cardinality(self):
        c = load("cardinality")
        rows = c["rows"]
        head = label(r"Cardinality: \ every label multiplies", font_size=36).to_edge(UP, buff=0.3)
        ident = mono('requests_total{service, endpoint, status, region, pod, user_id}', size=18, color=DATA)
        ident.next_to(head, DOWN, buff=0.35)
        vals = [r["series"] for r in rows] + [c["with_user_id"]]
        users = c["with_user_id"] // rows[-1]["series"]
        u_tex = f"{users:,}".replace(",", "{,}")

        def fmt(v):
            if v >= 1e12:
                m, e = f"{v:.1e}".split("e")
                return rf"${m} \times 10^{{{int(e)}}}$"
            if v >= 1e6:
                return rf"{v / 1e6:.1f} million"
            return f"{v:,}".replace(",", "{,}")
        names = [rows[0]["label"]] + [rf"$+$ {r['label']}" for r in rows[1:]] + [r"$+$ user id"]
        mult = [rf"{rows[0]['values']} values"] + [rf"$\times$ {r['values']}" for r in rows[1:]] + \
            [rf"$\times$ {u_tex}"]
        cols = [DATA, DATA, DATA, DATA, HEAD, NO]
        chart = bar_chart(vals, [n.replace("_", r"\_") for n in names], cols, height=2.7, bar_w=0.95, gap=0.85,
                          log=True, fmt_=fmt)
        chart.move_to([0, -0.05, 0])
        chart.shift(UP * (1.95 - max(b.get_top()[1] for b in chart.bars)))
        ms = VGroup(*[label(m, font_size=16, color=GREY_B).next_to(n, DOWN, buff=0.08)
                      for m, n in zip(mult, chart.names)])
        scale = label(r"series, \ log scale", font_size=16, color=GREY_B).next_to(chart.bars[0], UP, buff=0.5)
        scale.align_to(chart.bars[0], LEFT)
        notes = VGroup(
            wrapped_label(r"a \textbf{series} is a metric's name plus one value per label: \ their number is the "
                          r"product of the labels' cardinalities", 12.4, font_size=19, color=WHITE),
            wrapped_label(rf"a label per user \ ({u_tex} users, \ illustrative) \ is beyond any time-series store: "
                          r"\ questions about one user belong in logs and traces \ (Parts 46 and 50)", 12.4,
                          font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        base = VGroup(*[m for m in chart if m not in (chart.bars, chart.vals, chart.names)])
        with self.voiceover(
            "The hard part of a metrics system is not the rate of samples but the number of series. "
            "<bookmark mark='a'/> A series is a metric's name plus one value for each of its labels, and every "
            "distinct combination is stored separately. <bookmark mark='b'/> Start with fifty services. Label each "
            "request with its endpoint, forty each, and there are two thousand series; with its status, twelve "
            "thousand; with its region, ninety-six thousand. <bookmark mark='c'/> Add the pod, two hundred of them, "
            "and one metric becomes nineteen point two million series. <bookmark mark='d'/> Add a user identifier, "
            "for a million users, and it is about nineteen trillion, which no time-series store can hold. Questions "
            "about one user belong in logs and traces."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ident))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), FadeIn(base), FadeIn(scale))

            def show(i):
                return [GrowFromEdge(chart.bars[i], DOWN), FadeIn(chart.vals[i]), FadeIn(chart.names[i]),
                        FadeIn(ms[i])]
            vo.wait_until("b")
            for i in range(4):
                self.play(*show(i), run_time=0.8)
            vo.wait_until("c")
            self.play(*show(4))
            vo.wait_until("d")
            self.play(*show(5))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def napkin(self):
        c = load("cardinality")
        series = c["rows"][-1]["series"]
        every_s, raw_b, gor_b = 10, 16, 1.37
        per_s = series / every_s
        per_day = per_s * 86_400
        raw_tb = per_day * raw_b / 1e12
        gor_gb = per_day * gor_b / 1e9
        head = label(r"The napkin, \ and Gorilla's compression", font_size=36).to_edge(UP, buff=0.3)
        m, e = f"{per_day:.2e}".split("e")
        rows = [[r"series", r"from the labels above", rf"{series / 1e6:.1f} million"],
                [r"samples", rf"one per series every {every_s} s", rf"{per_s / 1e6:.2f} million a second"],
                [r"a day", r"86{,}400 seconds", rf"${m} \times 10^{{{int(e)}}}$ samples"],
                [r"stored plainly", r"8 B time $+$ 8 B value", rf"{raw_tb:.2f} TB a day"],
                [r"Gorilla", rf"{gor_b} B a sample \ (Pelkonen et al., \ 2015)", rf"{gor_gb:.0f} GB a day"]]
        tab = grid_table([r"quantity", r"assumption", r"result"], rows, widths=[2.4, 5.0, 3.6], row_h=0.44,
                         font_size=18, mono_cols=())
        tab.next_to(head, DOWN, buff=0.3)
        for r in range(1, len(rows) + 1):
            tab.cells[r][2].set_color(HEAD)
        tab.cells[4][2].set_color(NO)
        tab.cells[5][2].set_color(YES)
        crow = [[r"time (s)", "1000", "1010", "1020", "1030", "1041"],
                [r"delta", "", "10", "10", "10", "11"],
                [r"delta of delta", "", "", "0", "0", "1"],
                [r"value", "42.0", "42.0", "42.0", "43.5", "43.5"],
                [r"XOR with previous", "", "0", "0", r"$\neq 0$", "0"]]
        ccol = []
        for r in crow:
            ccol.append([GREY_A] + [YES if v == "0" else (WHITE if v != r"$\neq 0$" else HEAD) for v in r[1:]])
        comp = grid_table([r"sample", "1", "2", "3", "4", "5"], crow, widths=[2.8, 1.0, 1.0, 1.0, 1.0, 1.0],
                          row_h=0.38, font_size=18, colors=ccol, mono_cols=())
        comp.to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        cnote = VGroup(
            wrapped_label(r"steady intervals: \ the delta of delta is usually 0, \ stored as a single bit", 4.6,
                          font_size=19, color=YES),
            wrapped_label(r"slow values: \ XOR with the previous is usually 0, \ again one bit", 4.6, font_size=19,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(comp, RIGHT, buff=0.45)
        ill = note(r"interval and samples illustrative", font_size=16).next_to(cnote, DOWN, buff=0.25).align_to(
            cnote, LEFT)
        with self.voiceover(
            "Now the napkin. <bookmark mark='a'/> Take those nineteen point two million series and sample each "
            "every ten seconds: about two million samples a second, a hundred and sixty-six billion a day. "
            "<bookmark mark='b'/> Stored plainly, eight bytes of time and eight of value, that is over two and a "
            "half terabytes a day. <bookmark mark='c'/> Facebook's Gorilla, described by Tuomas Pelkonen and "
            "colleagues in 2015, compressed samples to one point three seven bytes each on average. "
            "<bookmark mark='d'/> Timestamps arrive at a steady rhythm, so it stores the change in the gap, usually "
            "zero, in a single bit. <bookmark mark='e'/> Values change slowly, so it stores each value's exclusive or "
            "with the previous one, again usually zero. That brings our day down to about two hundred and "
            "twenty-seven gigabytes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            vo.wait_until("a")
            self.play(*[FadeIn(VGroup(*tab.cells[r])) for r in (1, 2, 3)])
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[4])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[5][:2])))
            vo.wait_until("d")
            self.play(FadeIn(comp.rule), FadeIn(VGroup(*comp.cells[0])), FadeIn(VGroup(*comp.cells[1])))
            self.play(FadeIn(VGroup(*comp.cells[2])))
            self.play(FadeIn(VGroup(*comp.cells[3])), FadeIn(cnote[0]))
            vo.wait_until("e")
            self.play(FadeIn(VGroup(*comp.cells[4])))
            self.play(FadeIn(VGroup(*comp.cells[5])), FadeIn(cnote[1]), FadeIn(ill))
            self.play(FadeIn(tab.cells[5][2]))
        self.wait(0.4)
        self.clear_scene()

    def downsample(self):
        head = label(r"Downsampling: \ keep the shape", font_size=36).to_edge(UP, buff=0.3)
        rng = np.random.default_rng(7)
        n, bucket = 360, 30                               # an hour at 10 s; five-minute buckets
        t = np.arange(n) / 6.0                            # minutes
        y = 38 + 8 * np.sin(t / 60 * 2 * PI * 1.5) + rng.normal(0, 2.5, n)
        y[222:225] += np.array([30.0, 44.0, 26.0])        # a short spike, about thirty seconds
        g = axes([0, 60, 10], [0, 100, 25], x_length=7.2, y_length=3.7, x_label=r"minutes",
                 y_label=r"latency, \ ms", xticks=range(0, 61, 10), yticks=(0, 50, 100))
        g.move_to([-2.7, -0.15, 0])
        ax = g.ax
        raw = VMobject(color=DATA, stroke_width=1.6).set_points_as_corners([ax.c2p(a, b) for a, b in zip(t, y)])
        bars, means = VGroup(), VGroup()
        for k in range(n // bucket):
            seg = y[k * bucket:(k + 1) * bucket]
            x0, x1 = k * 5 + 0.4, k * 5 + 4.6
            lo, hi = ax.c2p(x0, seg.min()), ax.c2p(x1, seg.max())
            bars.add(Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_color=LAM, stroke_width=1.5,
                               fill_color=LAM, fill_opacity=0.25).move_to((lo + hi) / 2))
            means.add(Line(ax.c2p(x0, seg.mean()), ax.c2p(x1, seg.mean()), color=HEAD, stroke_width=4))
        spike_k = 222 // bucket
        notes = VGroup(
            wrapped_label(r"an hour at 10 s: \ 360 points", 4.5, font_size=19, color=DATA),
            wrapped_label(r"five-minute buckets keep \textbf{min, \ max, \ sum and count}: \ 12 buckets of 4 "
                          r"numbers", 4.5, font_size=19, color=LAM),
            wrapped_label(r"the mean \ (yellow) \ hides the spike; \ the max keeps it; \ sums and "
                          r"counts give exact averages and rates", 4.5, font_size=19, color=WHITE),
            wrapped_label(r"percentiles cannot be averaged: \ keep a histogram or a mergeable sketch per bucket \ "
                          r"(Part 50)", 4.5, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.4, 0.0, 0])
        ill = note(r"illustrative series", font_size=16).next_to(g, DOWN, buff=0.2).align_to(g, RIGHT)
        with self.voiceover(
            "Old data is read less often, and less finely, so it is downsampled. <bookmark mark='a'/> Here is an "
            "hour of one series at ten-second resolution, three hundred and sixty points. <bookmark mark='b'/> Cut "
            "it into five-minute buckets, and keep four numbers for each: the minimum, the maximum, the sum and the "
            "count. <bookmark mark='c'/> The mean alone would have hidden this spike; the maximum keeps it. Sums "
            "and counts still give exact averages and rates over any longer window. <bookmark mark='d'/> But "
            "percentiles cannot be combined: the average of two ninety-ninth percentiles is not a ninety-ninth "
            "percentile. For latency, keep a histogram or a mergeable sketch in each bucket, which Part 50 builds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(raw), FadeIn(notes[0]), run_time=2)
            vo.wait_until("b")
            self.play(raw.animate.set_stroke(opacity=0.35), LaggedStart(*[FadeIn(b) for b in bars],
                                                                        lag_ratio=0.1), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(m) for m in means], lag_ratio=0.1), FadeIn(notes[2]))
            self.play(Indicate(bars[spike_k], color=YES), Indicate(means[spike_k], color=HEAD))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def tiers(self):
        head = label(r"Retention tiers, \ and the trade-off", font_size=36).to_edge(UP, buff=0.3)
        specs = [(r"10 s", 15, 10, 1, r"hot: \ memory and SSD", HEAD),
                 (r"1 minute", 90, 60, 4, r"warm: \ disk", LAM),
                 (r"1 hour", 730, 3600, 4, r"cold: \ object storage \ (Part 45)", DATA)]
        boxes = VGroup()
        total = 0
        for res, days, step, per, where, col in specs:
            pts = days * 86_400 // step
            total += pts * per
            frame = RoundedRectangle(width=3.5, height=1.75, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                     fill_color=BG, fill_opacity=1)
            keep = r"1 value" if per == 1 else r"min, \ max, \ sum, \ count"
            g = VGroup(label(rf"{res} \ for {days if days < 365 else days // 365} "
                             rf"{'days' if days < 365 else 'years'}", font_size=21, color=col),
                       label(where, font_size=17, color=GREY_A),
                       label(rf"{pts:,} $\times$ {keep}".replace(",", "{,}", 1), font_size=17, color=WHITE),
                       ).arrange(DOWN, buff=0.14).move_to(frame)
            for m in g:
                if m.width > 3.3:
                    m.width = 3.3
            boxes.add(VGroup(frame, g))
        boxes.arrange(RIGHT, buff=0.75).next_to(head, DOWN, buff=0.45)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.05, color=GREY_C,
                                stroke_width=2) for i in range(2)])
        flat = 730 * 86_400 // 10
        chart = bar_chart([flat, total], [r"10 s for 2 years", r"the three tiers"], [NO, YES], height=2.3,
                          bar_w=1.1, gap=1.6, fmt_=lambda v: f"{v:,}".replace(",", "{,}"))
        ct = label(r"numbers kept per series", font_size=18, color=GREY_A)
        left = VGroup(ct, chart).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45).to_edge(LEFT, buff=1.0)
        trade = VGroup(
            wrapped_label(rf"about {flat / total:.0f} times fewer numbers, \ every dashboard still drawable", 6.4,
                          font_size=19, color=YES),
            wrapped_label(r"the trade-off is detail against cost; \ the costliest knob is cardinality, \ so teams "
                          r"get a budget of series", 6.4, font_size=19, color=WHITE),
            wrapped_label(r"Part 50 builds service-level objectives and alerts on this pipeline", 6.4,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(left, RIGHT, buff=0.8)
        ill = note(r"tiers illustrative", font_size=16).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Put together, the store keeps tiers. <bookmark mark='a'/> The last fifteen days at full ten-second "
            "resolution, in memory and on fast disks. <bookmark mark='b'/> Ninety days of one-minute buckets on "
            "ordinary disks, <bookmark mark='c'/> and two years of hourly buckets in cheap object storage, Part "
            "45's blob store. <bookmark mark='d'/> For one series that is about seven hundred thousand numbers "
            "instead of six point three million: nearly nine times fewer, with every dashboard still drawable. "
            "<bookmark mark='e'/> The trade-off is detail against cost, and the costliest knob is cardinality, so "
            "teams are given a budget of series. Part 50 builds its service-level objectives and alerts on exactly "
            "this pipeline."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), FadeIn(boxes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[1]), FadeIn(boxes[2]))
            vo.wait_until("d")
            self.play(FadeIn(left), FadeIn(trade[0]))
            vo.wait_until("e")
            self.play(FadeIn(trade[1]))
            self.play(FadeIn(trade[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM)
