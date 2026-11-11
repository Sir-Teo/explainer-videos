from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import DATA, HEAD, KERN, LAM, NO, PART, YES, axes, bar_chart, grid_table, load, mono, trace


def ms(v: float) -> str:
    """A latency in ms or s, as it would be read aloud."""
    if v >= 10_000:
        return rf"{v / 1000:.0f} s"
    if v >= 1000:
        return rf"{v / 1000:.1f} s"
    if v >= 100:
        return rf"{v:.0f} ms"
    return rf"{v:.1f} ms"


def err_col(e: float):
    return YES if e < 0.01 else (HEAD if e < 0.05 else NO)


class Metrics(VoiceoverScene):
    def construct(self):
        self.card()
        self.kinds()
        self.lies()
        self.fleet()
        self.ddsketch()
        self.compared()
        self.cardinality()

    def card(self):
        card = chapter_card(7, r"Metrics, and why averages lie", r"What number describes a latency?",
                            lit=(2012, 2019), extra=((2012, r"Prometheus, \ at SoundCloud"),
                                                     (2019, r"Masson, Rim and Lee: \ DDSketch")), part=PART)
        with self.voiceover("Chapter seven. Metrics, and why averages lie."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def kinds(self):
        head = label(r"Counters, \ gauges, \ histograms", font_size=36).to_edge(UP, buff=0.3)
        rng = np.random.default_rng(7)
        xs = (-4.45, 0.0, 4.45)
        panels = VGroup()
        # counter: only goes up, reset by a restart
        inc = rng.poisson(4, 40)
        c, vals = 0, []
        for k, d in enumerate(inc):
            c = 0 if k == 26 else c + int(d)
            vals.append(c)
        g1 = axes([0, 40, 10], [0, 120, 40], x_length=3.6, y_length=2.5)
        l1 = trace(g1.ax, list(enumerate(vals)), DATA, width=2.6)
        rst = label(r"restart", font_size=16, color=NO).move_to(g1.ax.c2p(27, 105), aligned_edge=LEFT)
        # gauge: up and down
        ar = [0.0]
        for _ in range(39):
            ar.append(0.8 * ar[-1] + rng.normal(0, 1.0))
        q = 10 + 2.5 * np.array(ar)
        g2 = axes([0, 40, 10], [0, 20, 5], x_length=3.6, y_length=2.5)
        l2 = trace(g2.ax, list(enumerate(q.tolist())), HEAD, width=2.6)
        # histogram: counts in buckets of "at most" bounds
        les = (r"10", r"25", r"50", r"100", r"250", r"500", r"$\infty$")
        cnt = (3, 9, 14, 8, 4, 2, 1)
        g3 = axes([0, 7, 1], [0, 15, 5], x_length=3.6, y_length=2.5)
        bars = VGroup()
        for k, v in enumerate(cnt):
            a, b = g3.ax.c2p(k + 0.12, 0), g3.ax.c2p(k + 0.88, v)
            bars.add(Rectangle(width=b[0] - a[0], height=b[1] - a[1], stroke_width=0, fill_color=LAM,
                               fill_opacity=0.85).move_to((a + b) / 2))
        blabs = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(g3.ax.c2p(k + 0.5, 0), DOWN, buff=0.08)
                         for k, t in enumerate(les)])
        bl = label(r"bucket: \ at most \ldots\ ms", font_size=15, color=GREY_B).next_to(blabs, DOWN, buff=0.08)
        specs = ((r"counter", DATA, g1, VGroup(l1, rst),
                  r"only goes up: \ requests, \ errors, \ bytes; \ chart its \textbf{rate}, \ which survives a missed "
                  r"reading and a reset"),
                 (r"gauge", HEAD, g2, VGroup(l2),
                  r"a reading that goes up and down: \ queue length, \ memory in use"),
                 (r"histogram", LAM, g3, VGroup(bars, blabs, bl),
                  r"counts of observations per bucket; \ buckets \textbf{add} across servers and across time"))
        for (name, col, g, plot, desc), x in zip(specs, xs):
            t = label(name, font_size=26, color=col)
            d = wrapped_label(desc, 3.9, font_size=19, color=WHITE)
            c0 = g.get_center()
            VGroup(t, g).arrange(DOWN, buff=0.3).move_to([x, 1.0, 0])
            plot.shift(g.get_center() - c0)
            d.next_to(g, DOWN, buff=0.75 if name == r"histogram" else 0.45).set_x(x)
            panels.add(VGroup(t, g, plot, d))
        for p in panels[:2]:
            p[3].align_to(panels[2][3], UP)
        ill = note(r"illustrative", font_size=16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Prometheus, begun at SoundCloud in 2012, stores three kinds of metric. <bookmark mark='a'/> A "
            "counter only goes up: requests, errors, bytes. You chart its rate, which survives a missed reading "
            "and a restart that resets it. <bookmark mark='b'/> A gauge goes up and down: queue length, memory in "
            "use. <bookmark mark='c'/> A histogram counts observations into buckets: under ten milliseconds, "
            "under twenty-five, under fifty. Buckets add, across servers and across time, and that turns out to "
            "matter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            for mk, p in zip("abc", panels):
                vo.wait_until(mk)
                self.play(FadeIn(p[0]), FadeIn(p[1]))
                self.play(Create(p[2]) if mk != "c" else LaggedStart(*[GrowFromEdge(b, DOWN) for b in p[2][0]],
                                                                      lag_ratio=0.15), run_time=1.5)
                if mk == "c":
                    self.play(FadeIn(p[2][1]), FadeIn(p[2][2]))
                self.play(FadeIn(p[3]))
        self.wait(0.4)
        self.clear_scene()

    def lies(self):
        s = load("sketches")
        a = load("averages")
        rows = {r["q"]: r for r in s["rows"]}
        counts, edges = s["hist"]["counts"], s["hist"]["log10_edges"]
        head = label(r"One distribution, \ five numbers", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0.2, 5.25, 1], [0, 6, 1], x_length=8.4, y_length=4.2, x_label=r"latency \ (log scale)",
                 xticks=(1, 2, 3, 4, 5), yticks=(0, 2, 4), fx=lambda v: (r"10 ms", r"100 ms", r"1 s", r"10 s",
                                                                         r"100 s")[int(v) - 1],
                 fy=lambda v: rf"$10^{{{v:g}}}$", font=16)
        g.move_to([-2.3, -0.35, 0])
        ax = g.ax
        ylab = label(r"requests \ (log scale)", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(
            ax, LEFT)
        bars = VGroup()
        for c, e0, e1 in zip(counts, edges[:-1], edges[1:]):
            if c <= 0:
                continue
            p0, p1 = ax.c2p(e0, 0), ax.c2p(e1, math.log10(c))
            bars.add(Rectangle(width=p1[0] - p0[0] - 0.01, height=max(0.02, p1[1] - p0[1]), stroke_width=0,
                               fill_color=GREY_B, fill_opacity=0.55).move_to((p0 + p1) / 2))
        marks = [(s["mean"], r"mean", NO), (rows[0.5]["true"], r"median", DATA), (rows[0.99]["true"], r"p99", HEAD),
                 (rows[0.999]["true"], r"p99.9", KERN), (s["max"], r"max", LAM)]
        lines = VGroup()
        for k, (v, name, col) in enumerate(marks):
            x = math.log10(v)
            ln = DashedLine(ax.c2p(x, 0), ax.c2p(x, (5.75, 5.0, 4.9, 5.3, 5.75)[k]), color=col, stroke_width=2.2)
            t = label(rf"{name}: \ {ms(v)}", font_size=17, color=col).next_to(ln, UP, buff=0.05)
            if name in (r"mean", r"median"):
                t.next_to(ln.get_end(), RIGHT if name == r"mean" else LEFT, buff=0.06).shift(UP * 0.12)
            lines.add(VGroup(ln, t))
        notes = VGroup(
            wrapped_label(rf"{s['n']:,} simulated requests: \ most near 20 ms, \ 5\% cache misses near 120 ms, \ "
                          r"0.5\% in a heavy tail", 3.6, font_size=18, color=GREY_A),
            wrapped_label(r"the mean describes almost no request", 3.6, font_size=19, color=NO),
            wrapped_label(rf"a page making 100 requests meets one slower than the p99 "
                          rf"{100 * a['users_seeing_p99_in_100_requests']:.0f}\% of the time: \ $1 - 0.99^{{100}}$",
                          3.6, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.75, -0.2, 0])
        with self.voiceover(
            "Here are two hundred thousand simulated latencies, on logarithmic axes. Most take about twenty "
            "milliseconds; one in twenty misses a cache; one in two hundred falls into a heavy tail. <bookmark "
            "mark='a'/> The mean is thirty milliseconds, a latency almost no request has. <bookmark mark='b'/> "
            "The median, twenty and a half, is what a typical request sees. <bookmark mark='c'/> The ninety-ninth "
            "percentile is a hundred and seventy-seven, the ninety-nine point ninth eight hundred and "
            "thirty-four, and the slowest took a hundred and four seconds. <bookmark mark='d'/> And the tail is "
            "not rare for users: a page making a hundred requests meets one beyond the ninety-ninth percentile "
            "sixty-three times in a hundred, as Dean and Barroso pointed out."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(ylab), FadeIn(notes[0]))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(lines[0][0]), FadeIn(lines[0][1]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(Create(lines[1][0]), FadeIn(lines[1][1]))
            vo.wait_until("c")
            for ln in lines[2:]:
                self.play(Create(ln[0]), FadeIn(ln[1]), run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def fleet(self):
        a = load("averages")
        p99s = a["p99s"]
        head = label(r"Percentiles do not average", font_size=36).to_edge(UP, buff=0.3)
        cols = [NO] + [DATA] * (len(p99s) - 1)
        ch = bar_chart(p99s, [rf"{k + 1}" for k in range(len(p99s))], cols, height=4.0, bar_w=0.5, gap=0.3,
                       vmax=800, fmt_=lambda v: rf"{v:.0f}", font_size=17)
        ch.move_to([-2.6, -0.35, 0])
        sx = label(r"server", font_size=17, color=GREY_A).next_to(ch.names, DOWN, buff=0.12)
        yl = label(r"each server's p99, \ ms", font_size=17, color=GREY_A).next_to(ch, UP, buff=0.15).align_to(
            ch, LEFT)
        base_y = ch[0].get_y()
        x0, x1 = ch[0].get_left()[0], ch[0].get_right()[0]

        def hline(v, col, dashed=True):
            y = base_y + 4.0 * v / 800
            ln = (DashedLine if dashed else Line)([x0, y, 0], [x1, y, 0], color=col, stroke_width=2.5)
            return ln
        l_avg = hline(a["mean_of_p99s"], NO)
        l_true = hline(a["p99"], YES, dashed=False)
        notes = VGroup(
            wrapped_label(r"server 1 is four times slower than the rest", 4.2, font_size=19, color=GREY_A),
            wrapped_label(rf"the average of the ten p99s: \ {a['mean_of_p99s']:.0f} ms", 4.2, font_size=20,
                          color=NO),
            wrapped_label(rf"the fleet's true p99: \ {a['p99']:.0f} ms", 4.2, font_size=20, color=YES),
            wrapped_label(rf"merge the ten servers' DDSketches bucket by bucket, \ then read the quantile: \ "
                          rf"{a['merged_sketch_p99']:.0f} ms", 4.2, font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.5, -0.1, 0])
        with self.voiceover(
            "Now ten servers, one of them four times slower than the rest. <bookmark mark='a'/> Each reports its "
            "ninety-ninth percentile: about a hundred and seventy-five milliseconds for nine, seven hundred and "
            "nineteen for the slow one. <bookmark mark='b'/> A dashboard that averages them shows two hundred and "
            "thirty. <bookmark mark='c'/> But the true ninety-ninth percentile of the fleet's requests is two "
            "hundred and seventy. Percentiles do not average. <bookmark mark='d'/> Distributions do combine: add "
            "the servers' histograms bucket by bucket, then read the quantile: two hundred and sixty-eight, "
            "within the sketch's one percent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch[0]), FadeIn(ch.names), FadeIn(sx), FadeIn(yl), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ch.bars], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(v) for v in ch.vals], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(l_avg), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(l_true), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def ddsketch(self):
        s = load("sketches")
        lo = 10 ** s["hist"]["log10_edges"][0]
        head = label(r"DDSketch: \ a guaranteed relative error", font_size=36).to_edge(UP, buff=0.3)
        # buckets drawn at alpha = 0.2 (gamma = 1.5) so that they are visible
        al = 0.2
        gm = (1 + al) / (1 - al)
        top = gm ** 7
        X0, W, Y = -6.0, 12.0, 1.75

        def xp(v):
            return X0 + W * math.log(v) / math.log(top)
        axis = Line([X0 - 0.2, Y, 0], [X0 + W + 0.2, Y, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[Line([xp(gm ** i), Y - 0.15, 0], [xp(gm ** i), Y + 0.15, 0], color=GREY_B, stroke_width=2)
                         for i in range(8)])
        tl = VGroup(*[MathTex(rf"\gamma^{{{i}}}", font_size=26, color=GREY_B).next_to(ticks[i], DOWN, buff=0.1)
                      for i in range(8)])
        i = 5
        x_val = 6.0
        est = 2 * gm ** i / (gm + 1)
        bk = Rectangle(width=xp(gm ** i) - xp(gm ** (i - 1)), height=0.5, stroke_width=0, fill_color=HEAD,
                       fill_opacity=0.25).move_to([(xp(gm ** i) + xp(gm ** (i - 1))) / 2, Y, 0])
        xd = Dot([xp(x_val), Y, 0], radius=0.09, color=DATA)
        xl = MathTex(r"x", font_size=30, color=DATA).next_to(xd, UP, buff=0.2)
        ed = Triangle(color=YES, fill_opacity=1).scale(0.1).rotate(PI).move_to([xp(est), Y + 0.36, 0])
        el = MathTex(r"\hat x", font_size=30, color=YES).next_to(ed, UP, buff=0.08)
        ill = note(r"drawn at $\alpha = 0.2$, \ $\gamma = 1.5$", font_size=16).next_to(axis, UP, buff=0.35).align_to(
            axis, LEFT)
        steps = VGroup(
            MathTex(r"\gamma = \frac{1+\alpha}{1-\alpha}", r"\qquad \text{bucket } i = \lceil \log_\gamma x \rceil:"
                    r"\ \ \gamma^{i-1} < x \le \gamma^{i}", font_size=32),
            MathTex(r"\hat x = \frac{2\gamma^{i}}{\gamma + 1}", font_size=32, color=YES),
            MathTex(r"\frac{2}{\gamma+1} \le \frac{\hat x}{x} < \frac{2\gamma}{\gamma+1}", r"\quad\Longrightarrow\quad",
                    r"1 - \alpha \le \frac{\hat x}{x} < 1 + \alpha", font_size=32),
            MathTex(r"|\hat x - x| \le \alpha\, x", font_size=36, color=HEAD),
        ).arrange(DOWN, buff=0.3).move_to([-1.6, -1.25, 0])
        steps[2][2].set_color(HEAD)
        side = VGroup(
            wrapped_label(rf"$\alpha = 1\%$: \ these latencies, \ {lo:.0f} ms to {s['max'] / 1000:.0f} s, \ fill "
                          rf"{s['size']['DDSketch']} buckets", 3.3, font_size=19, color=WHITE),
            wrapped_label(r"merge: \ add counts bucket by bucket, \ exactly", 3.3, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([5.0, -1.3, 0])
        with self.voiceover(
            "In 2019 Charles Masson, Jee Rim and Homin Lee, at Datadog, published a sketch with a guarantee, "
            "DDSketch. <bookmark mark='a'/> Choose a relative accuracy, alpha. Bucket boundaries are powers of "
            "gamma, one plus alpha over one minus alpha, so the buckets grow geometrically. <bookmark mark='b'/> "
            "To answer a quantile, find the bucket holding that rank and return two gamma to the i over gamma "
            "plus one. <bookmark mark='c'/> For any value in that bucket, the answer divided by the value lies "
            "between one minus alpha and one plus alpha. <bookmark mark='d'/> So the error is relative: one "
            "percent of a twenty-millisecond median, and one percent of a two-second tail. <bookmark mark='e'/> "
            "At one percent, these latencies fill three hundred and thirty-two buckets, and sketches merge by "
            "adding counts."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(tl), Write(steps[0]))
            self.play(FadeIn(xd), FadeIn(xl), FadeIn(bk))
            vo.wait_until("b")
            self.play(Write(steps[1]), FadeIn(ed), FadeIn(el))
            vo.wait_until("c")
            self.play(Write(steps[2]))
            vo.wait_until("d")
            self.play(Write(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[0]))
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def compared(self):
        s = load("sketches")
        names = ("DDSketch", "log-linear", "KLL", "sample of 1000")
        head = label(r"Four summaries against the true quantiles", font_size=36).to_edge(UP, buff=0.3)
        qn = {0.5: r"p50", 0.9: r"p90", 0.99: r"p99", 0.999: r"p99.9", 0.9999: r"p99.99"}
        body, colors = [], []
        for r in s["rows"]:
            body.append([qn[r["q"]], ms(r["true"])] + [rf"{100 * r['err ' + n]:.1f}\%" for n in names])
            colors.append([GREY_A, WHITE] + [err_col(r["err " + n]) for n in names])
        body.append([r"size", r""] + [rf"{s['size'][n]:,}" for n in names])
        colors.append([GREY_A, WHITE] + [GREY_A] * 4)
        tab = grid_table([r"quantile", r"true", r"DDSketch, \ 1\%", r"log-linear \ (HDR)", r"KLL \ (Part 46)",
                          r"sample of 1{,}000"], body, widths=[1.7, 1.6, 2.2, 2.3, 2.1, 2.3], row_h=0.6,
                         font_size=21, colors=colors, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45)
        sub = label(r"relative error of each estimate; \ size in buckets, \ or values kept", font_size=18,
                    color=GREY_A).next_to(tab, DOWN, buff=0.15)
        size_rule = Line(tab.cells[6][0].get_left() + UP * 0.25 + LEFT * 0.1,
                         [tab.get_right()[0], tab.cells[6][0].get_y() + 0.25, 0], color=GREY_D, stroke_width=1)
        cols = [VGroup(*[tab.cells[r][c] for r in range(len(tab.cells))]) for c in range(6)]
        notes = VGroup(
            wrapped_label(r"KLL bounds the error in \textbf{rank}: \ in a heavy tail, \ neighbouring ranks are far "
                          r"apart in value", 6.0, font_size=19, color=NO),
            wrapped_label(r"the log-linear layout of Tene's HdrHistogram: \ each power of two split into 128 parts",
                          6.0, font_size=19, color=WHITE),
        ).arrange(RIGHT, buff=0.4, aligned_edge=UP).next_to(sub, DOWN, buff=0.6)
        with self.voiceover(
            "Four summaries of the same latencies. <bookmark mark='a'/> DDSketch stays within its one percent "
            "everywhere. The log-linear layout of Gil Tene's HdrHistogram, each power of two split into a hundred "
            "and twenty-eight parts, does better still, with three times the buckets. <bookmark mark='b'/> Part "
            "46's KLL is accurate at the median, but off by almost half at the ninety-nine point ninth "
            "percentile: it bounds the error in rank, and in a heavy tail neighbouring ranks are far apart in "
            "value. <bookmark mark='c'/> A random sample of a thousand holds almost none of the tail."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols[0]), FadeIn(cols[1]), Create(tab.rule), Create(size_rule),
                      FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(cols[2]))
            self.play(FadeIn(cols[3]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(cols[4]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(cols[5]))
        self.wait(0.4)
        self.clear_scene()

    def cardinality(self):
        head = label(r"Cardinality: \ labels multiply", font_size=36).to_edge(UP, buff=0.3)
        parts = (("method", 5), ("status", 8), ("route", 40), ("instance", 200))
        name = mono("http_requests_total", size=24, color=WHITE)
        tags = VGroup(*[mono(p, size=22, color=DATA) for p, _ in parts])
        brace_o, brace_c = mono("{", size=24, color=WHITE), mono("}", size=24, color=WHITE)
        commas = [mono(",", size=22, color=GREY_B) for _ in range(len(parts) - 1)]
        seq = [name, brace_o]
        for k, t in enumerate(tags):
            seq.append(t)
            if k < len(tags) - 1:
                seq.append(commas[k])
        seq.append(brace_c)
        line = VGroup(*seq).arrange(RIGHT, buff=0.12).move_to([-0.6, 1.9, 0])
        for k, cm in enumerate(commas):
            cm.align_to(tags[k], DOWN).shift(DOWN * 0.06)
        counts = VGroup(*[label(rf"{n}", font_size=26, color=HEAD).next_to(t, DOWN, buff=0.35) for t, (_, n) in
                          zip(tags, parts)])
        times = VGroup(*[MathTex(r"\times", font_size=30, color=GREY_B).move_to(
            (counts[k].get_center() + counts[k + 1].get_center()) / 2) for k in range(len(parts) - 1)])
        total = 1
        for _, n in parts:
            total *= n
        res = label(rf"$=$ \ {total:,} time series", font_size=28, color=HEAD).next_to(counts, RIGHT, buff=0.35)
        uid = mono(", user_id", size=22, color=NO)
        uid_n = label(r"$\times$ \ 1{,}000{,}000 users", font_size=26, color=NO)
        boom = label(rf"$=$ \ {total * 1_000_000 / 1e11:.1f} $\times 10^{{11}}$ series", font_size=30, color=NO)
        VGroup(uid_n, boom).arrange(RIGHT, buff=0.35).next_to(counts, DOWN, buff=0.6).set_x(0)
        # a little grid of series that fills up
        grid = VGroup(*[Square(0.16, stroke_width=0, fill_color=HEAD, fill_opacity=0.7) for _ in range(160)])
        grid.arrange_in_grid(rows=4, cols=40, buff=0.05).next_to(boom, DOWN, buff=0.45)
        g_l = label(r"each series stored and indexed on its own", font_size=17, color=GREY_A).next_to(
            grid, DOWN, buff=0.12)
        ill = note(r"illustrative", font_size=16).next_to(line, UP, buff=0.2).align_to(line, LEFT)
        foot = wrapped_label(r"keep label values few and bounded \ (route templates, \ not paths); \ detail about "
                             r"single requests belongs in logs and traces", 12.4, font_size=20, color=YES)
        foot.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "One more cost. <bookmark mark='a'/> Every distinct combination of label values is a separate time "
            "series, stored and indexed on its own. <bookmark mark='b'/> Five methods, eight status codes, forty "
            "routes and two hundred instances make three hundred and twenty thousand series for one metric. "
            "<bookmark mark='c'/> Add a user identifier, for a million users, and it becomes three hundred and "
            "twenty billion. <bookmark mark='d'/> So keep label values few and bounded; detail about single "
            "requests belongs in logs and traces, the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(line), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(sq) for sq in grid[:40]], lag_ratio=0.02), FadeIn(g_l), run_time=1.2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in counts], lag_ratio=0.3), FadeIn(times))
            self.play(FadeIn(res), LaggedStart(*[FadeIn(sq) for sq in grid[40:]], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("c")
            uid.next_to(line[-2], RIGHT, buff=0.08).align_to(line[-2], UP)
            self.play(line[-1].animate.next_to(uid, RIGHT, buff=0.08))
            self.play(FadeIn(uid), FadeIn(uid_n))
            self.play(FadeIn(boom), grid.animate.set_fill(NO, 0.8))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
