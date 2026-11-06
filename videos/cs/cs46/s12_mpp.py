from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs46.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, bar_chart, code_block, load,
                                   module_box, mono, tag_box, trace)

# columnar.skew's defaults (explainer/cs/data/columnar.py): one key holds a fifth of the rows; salting splits it eight
# ways
HOT_SHARE, SALT = 0.2, 8
STORE = {"L": ("Leeds", DATA), "Y": ("York", LAM), "H": ("Hull", KERN)}


def cell(text, color, w=0.6, h=0.42, size=17, fill=0.15):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=fill)
    return VGroup(r, label(text, font_size=size, color=WHITE).move_to(r))


class Mpp(VoiceoverScene):
    def construct(self):
        self.card()
        self.partitioned()
        self.joins()
        self.joincost()
        self.skew()
        self.vectorized()

    def card(self):
        card = chapter_card(11, r"Queries on a thousand machines", r"How does one query use a thousand machines "
                            r"at once?", lit=(1986, 2005), extra=((1986, r"DeWitt et al.: \ Gamma"),
                                                                 (2005, r"Boncz et al.: \ MonetDB/X100")), part=PART)
        with self.voiceover("Chapter eleven. Queries on a thousand machines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def partitioned(self):
        head = label(r"Partitioned execution", font_size=36).to_edge(UP, buff=0.3)
        q = mono("SELECT store, COUNT(*) FROM sales GROUP BY store", size=16, color=HEAD).move_to([-2.9, 2.62, 0])
        wx = [-5.8, -4.0, -2.2, -0.4]
        ys = {"scan": 1.4, "partial": 0.3, "final": -1.15, "gather": -2.4}
        parts = ["LYLHLY", "YYHLHY", "LHHLYL", "HYLLYH"]       # the rows each worker holds (illustrative)
        workers = VGroup()
        for k, (x, p) in enumerate(zip(wx, parts)):
            box = Rectangle(width=1.5, height=0.85, stroke_color=GREY_B, stroke_width=1.5).move_to([x, ys["scan"], 0])
            sq = VGroup(*[Square(0.2, stroke_width=0, fill_color=STORE[s][1], fill_opacity=0.9) for s in p])
            sq.arrange_in_grid(rows=2, cols=3, buff=0.12).move_to(box)
            t = label(rf"worker {k + 1}", font_size=16, color=GREY_A).next_to(box, UP, buff=0.08)
            workers.add(VGroup(box, sq, t))
        partials = VGroup()
        for x, p in zip(wx, parts):
            g = VGroup(*[mono(f"{s}{p.count(s)}", size=17, color=STORE[s][1]) for s in "LYH" if s in p])
            partials.add(g.arrange(RIGHT, buff=0.14).move_to([x, ys["partial"], 0]))
        owner = {"Y": 0, "L": 2, "H": 3}                          # hash(store) mod 4, illustrative
        finals = {}
        for s, w in owner.items():
            total = sum(p.count(s) for p in parts)
            finals[s] = tag_box(f"{STORE[s][0]} {total}", STORE[s][1], size=16).move_to([wx[w], ys["final"], 0])
        moves = VGroup()
        for g, p in zip(partials, parts):
            for piece, s in zip(g, [s for s in "LYH" if s in p]):
                moves.add(Arrow(piece.get_bottom(), finals[s].get_top(), buff=0.06, stroke_width=1.6,
                                color=STORE[s][1], max_tip_length_to_length_ratio=0.08))
        down = VGroup(*[Arrow(w[0].get_bottom(), g.get_top(), buff=0.08, stroke_width=1.6, color=GREY_B,
                              max_tip_length_to_length_ratio=0.25) for w, g in zip(workers, partials)])
        coord = module_box(r"coordinator", HEAD, w=2.4, h=0.55).move_to([-3.1, ys["gather"], 0])
        up = VGroup(*[Arrow(f.get_bottom(), coord.get_top(), buff=0.06, stroke_width=1.6, color=HEAD,
                            max_tip_length_to_length_ratio=0.12) for f in finals.values()])
        stages = VGroup(*[label(t, font_size=17, color=GREY_B).move_to([0, y, 0]) for t, y in (
            (r"scan", ys["scan"]), (r"partial count", ys["partial"]), (r"exchange", (ys["partial"] + ys["final"]) / 2),
            (r"final count", ys["final"]), (r"gather", ys["gather"]))])
        for s in stages:
            s.align_to([0.55, 0, 0], LEFT)
        illus = note(r"illustrative", font_size=16).next_to(coord, RIGHT, buff=0.4)
        notes = VGroup(
            wrapped_label(r"the coordinator cuts the plan into fragments; \ every worker runs them on its own share "
                          r"of the files", 4.3, font_size=19, color=WHITE),
            wrapped_label(r"partial counts first: \ each worker sends three numbers, \ not its rows", 4.3,
                          font_size=19, color=YES),
            wrapped_label(r"an \textbf{exchange} sends each key to the one worker its hash names: \ Part 39's "
                          r"MapReduce shuffle, \ inside a query", 4.3, font_size=19, color=HEAD),
            wrapped_label(r"Gamma \ (DeWitt et al., \ 1986) \ had this shape; \ so do Redshift, \ BigQuery, \ "
                          r"Snowflake and Trino", 4.3, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([4.6, 0.0, 0])
        with self.voiceover(
            "A warehouse query is too big for one machine, so it runs on many. <bookmark mark='a'/> The table's "
            "files are spread over the workers, and the coordinator cuts the plan into fragments that every worker "
            "runs on its own share. <bookmark mark='b'/> Each worker first counts its own rows per store, a partial "
            "aggregate, and so sends three numbers instead of its rows. <bookmark mark='c'/> An exchange operator "
            "then hashes each store to one worker, which adds up that store's partial counts: Part 39's MapReduce "
            "shuffle, inside a query. <bookmark mark='d'/> The coordinator gathers the answers. DeWitt's Gamma "
            "machine had this shape in 1986; Redshift, BigQuery, Snowflake and Trino have it today."
        ) as vo:
            self.play(FadeIn(head), FadeIn(q))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(w) for w in workers], lag_ratio=0.2), FadeIn(stages[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(down), FadeIn(partials), FadeIn(stages[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowArrow(m) for m in moves], lag_ratio=0.08), FadeIn(stages[2]), run_time=2)
            self.play(*[FadeIn(f) for f in finals.values()], FadeIn(stages[3]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(coord), Create(up), FadeIn(stages[4]), FadeIn(illus), FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def joins(self):
        head = label(r"Broadcast or shuffle", font_size=36).to_edge(UP, buff=0.3)
        lx = [-5.6, -4.15, -2.7, -1.25]
        rx = [1.6, 3.05, 4.5, 5.95]
        t_l = label(r"broadcast join", font_size=24, color=LAM).move_to([-3.4, 2.6, 0])
        t_r = label(r"shuffle hash join", font_size=24, color=DATA).move_to([3.75, 2.6, 0])
        s_box = cell(r"$S$", LAM, w=0.9, h=0.36, fill=0.4).move_to([-3.4, 1.85, 0])
        b_parts = VGroup(*[cell(rf"$B_{k + 1}$", DATA, w=0.9, h=1.1, fill=0.3).move_to([x, -0.05, 0])
                           for k, x in enumerate(lx)])
        copies = VGroup(*[cell(r"$S$", LAM, w=0.9, h=0.3, fill=0.4).next_to(b, UP, buff=0.06) for b in b_parts])
        bc_arr = VGroup(*[Arrow(s_box.get_bottom(), c.get_top(), buff=0.06, stroke_width=1.8, color=LAM,
                                max_tip_length_to_length_ratio=0.15) for c in copies])
        cost_l = label(r"moves $S \times N$ rows", font_size=22, color=LAM).move_to([-3.4, -1.2, 0])
        top = VGroup(*[VGroup(cell(rf"$B_{k + 1}$", DATA, w=0.9, h=0.5, fill=0.3),
                              cell(rf"$S_{k + 1}$", LAM, w=0.9, h=0.3, fill=0.4)).arrange(DOWN, buff=0.04).move_to(
            [x, 1.6, 0]) for k, x in enumerate(rx)])
        bottom = VGroup(*[VGroup(cell(rf"$B'_{k + 1}$", DATA, w=0.9, h=0.5, fill=0.3),
                                 cell(rf"$S'_{k + 1}$", LAM, w=0.9, h=0.3, fill=0.4)).arrange(DOWN, buff=0.04).move_to(
            [x, -0.45, 0]) for k, x in enumerate(rx)])
        wires = VGroup(*[Line(a.get_bottom(), b.get_top(), color=GREY_C, stroke_width=1.2)
                         for a in top for b in bottom])
        dots = VGroup(*[Dot(w.get_start(), radius=0.05, color=HEAD) for w in wires])
        cost_r = label(r"moves $(B + S)\left(1 - \frac{1}{N}\right)$ rows", font_size=22, color=DATA).move_to(
            [3.75, -1.2, 0])
        lines = VGroup(
            wrapped_label(r"broadcast: \ the big table never moves; \ each worker joins its share of $B$ against a "
                          r"whole copy of $S$, \ by Part 35's hash join", 12.4, font_size=20, color=LAM),
            wrapped_label(r"shuffle: \ both tables are repartitioned by the join key, \ so matching rows meet on one "
                          r"worker; \ a row stays put only if it already sits on its key's worker, \ one time in $N$",
                          12.4, font_size=20, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Joins are where the network bill comes from: a big table, B, meets a small one, S, on N workers. "
            "<bookmark mark='a'/> A broadcast join sends a whole copy of S to every worker. B never moves; each "
            "worker joins its share of B against the copy, with Part 35's hash join. The cost is S rows, N times "
            "over. <bookmark mark='b'/> A shuffle hash join repartitions both tables by the join key, so matching "
            "rows meet on one worker. A row stays put only if it already sits on the right worker, one time in N, so "
            "the cost is B plus S, times one minus one over N."
        ) as vo:
            self.play(FadeIn(head), FadeIn(t_l), FadeIn(t_r), FadeIn(b_parts), FadeIn(s_box), FadeIn(top))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in bc_arr], lag_ratio=0.2),
                      LaggedStart(*[TransformFromCopy(s_box, c) for c in copies], lag_ratio=0.2), run_time=1.8)
            self.play(FadeIn(cost_l), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Create(wires), run_time=1.2)
            self.add(dots)
            self.play(*[MoveAlongPath(d, w) for d, w in zip(dots, wires)], run_time=1.6)
            self.remove(dots)
            self.play(FadeIn(bottom), FadeIn(cost_r), FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def joincost(self):
        rows = load("joins")["rows"]
        n = rows[0]["workers"]
        rb = rows[0]["broadcast_bytes"] / (rows[0]["small_rows"] * n)          # bytes per row
        big = rows[0]["big_rows"]                                               # the instrument's B
        cross = rows[0]["crossover_small_rows"]                                 # B (N - 1) / (N^2 - N + 1)
        head = label(r"Which costs less?", font_size=36).to_edge(UP, buff=0.3)
        ylab = {8: r"100 MB", 9: r"1 GB", 10: r"10 GB", 11: r"100 GB", 12: r"1 TB"}
        ch = axes([4, 8, 1], [8, 12, 1], x_length=5.8, y_length=3.7, x_label=r"rows in the small table $S$",
                  y_label=r"bytes sent over the network", xticks=[4, 5, 6, 7, 8], yticks=[8, 9, 10, 11, 12],
                  fx=lambda v: rf"$10^{{{int(v)}}}$", fy=lambda v: ylab[int(v)])
        ch.move_to([-2.75, 0.35, 0])
        ax = ch.ax
        pb = [(math.log10(r["small_rows"]), math.log10(r["broadcast_bytes"])) for r in rows]
        ps = [(math.log10(r["small_rows"]), math.log10(r["shuffle_bytes"])) for r in rows]
        l_b = VGroup(trace(ax, pb, LAM, width=3), *[Dot(ax.c2p(*p), radius=0.06, color=LAM) for p in pb])
        l_s = VGroup(trace(ax, ps, DATA, width=3), *[Dot(ax.c2p(*p), radius=0.06, color=DATA) for p in ps])
        n_b = label(r"broadcast", font_size=19, color=LAM).next_to(ax.c2p(*pb[2]), RIGHT, buff=0.15).shift(DOWN * 0.15)
        n_s = label(r"shuffle", font_size=19, color=DATA).next_to(ax.c2p(*ps[0]), UP, buff=0.12).shift(RIGHT * 0.5)
        xc = math.log10(cross)
        vline = DashedLine(ax.c2p(xc, 8), ax.c2p(xc, 12), color=HEAD, stroke_width=2, dash_length=0.08)
        c_l = label(rf"$S^* \approx$ {cross / 1e6:.0f} million", font_size=19, color=HEAD).next_to(
            vline, UP, buff=0.08)
        deriv = VGroup(
            label(r"broadcast: \ $S N$ \qquad shuffle: \ $(B + S)\left(1 - \frac{1}{N}\right)$", font_size=21),
            label(r"broadcast wins while", font_size=21, color=GREY_A),
            label(r"$S \;<\; \dfrac{B\,(N - 1)}{N^2 - N + 1} \;\approx\; \dfrac{B}{N}$", font_size=26, color=HEAD),
            label(rf"$B$: \ {big / 1e9:g} billion rows of {rb:g} bytes; \ $N = {n}$", font_size=21),
            label(rf"$S^* \approx$ {cross / 1e6:.1f} million rows, \ {cross / big * 100:.0f}\% of $B$", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.95, 0.6, 0])
        foot = wrapped_label(r"optimizers choose from estimated sizes; \ every worker must hold the copy in memory, \ "
                             r"so Spark broadcasts only a table it estimates under 10 MB by default; \ a wrong "
                             r"estimate \ (Part 35's guessed sizes) \ makes either choice a disaster", 12.4,
                             font_size=20, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Which is cheaper? <bookmark mark='a'/> In our cost model B has a billion rows of a hundred bytes, there "
            "are a hundred workers, and S grows from ten thousand rows to a hundred million. <bookmark mark='b'/> "
            "Broadcasting grows tenfold with S. Shuffling costs about a hundred gigabytes whatever S is, because B "
            "dominates. <bookmark mark='c'/> Set the costs equal: broadcast wins while S is below about B over N, "
            "here ten million rows, one percent of B. <bookmark mark='d'/> Optimizers choose from estimated sizes, "
            "and cautiously, since every worker must hold the copy in memory: Spark broadcasts only tables it "
            "estimates under ten megabytes, by default. A wrong estimate, Part 35's guessing of sizes, makes either "
            "choice a disaster."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch))
            vo.wait_until("a")
            self.play(FadeIn(deriv[3]))
            vo.wait_until("b")
            self.play(Create(l_b[0]), FadeIn(l_b[1:]), FadeIn(n_b), run_time=1.5)
            self.play(Create(l_s[0]), FadeIn(l_s[1:]), FadeIn(n_s), run_time=1.5)
            self.play(FadeIn(deriv[0]))
            vo.wait_until("c")
            self.play(FadeIn(deriv[1]), FadeIn(deriv[2]))
            self.play(Create(vline), FadeIn(c_l), FadeIn(deriv[4]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def skew(self):
        s = load("skew")
        w, ideal = s["workers"], s["ideal"]
        rows = round(ideal * w)
        head = label(r"One hot key", font_size=36).to_edge(UP, buff=0.3)
        xs = [-5.9, -4.6, -3.3, -2.0]
        src = VGroup(*[cell(rf"scan {k + 1}", GREY_B, w=1.05, h=0.45, size=16) for k in range(4)])
        for c, x in zip(src, xs):
            c.move_to([x, 2.2, 0])
        base_y, unit = -0.95, 0.16
        baseline = Line([xs[0] - 0.6, base_y, 0], [xs[-1] + 0.6, base_y, 0], color=GREY_C, stroke_width=1.5)
        names = VGroup(*[label(rf"worker {k + 1}", font_size=16, color=GREY_A).next_to([x, base_y, 0], DOWN, buff=0.12)
                         for k, x in enumerate(xs)])
        hot_to = 2
        # illustrative traffic: each scan sends three ordinary rows, spread round, and two rows of the hot key
        traffic = [(i, (i + j) % 4, False) for i in range(4) for j in range(3)] + [(i, hot_to, True) for i in range(4)
                                                                                    for _ in range(2)]
        load_plain = [sum(1 for _, d, _ in traffic if d == k) for k in range(4)]
        n_hot = sum(1 for *_, h in traffic if h)
        load_salt = [sum(1 for _, d, h in traffic if d == k and not h) + n_hot // 4 for k in range(4)]

        def bars(loads, hot_rows):
            g = VGroup()
            for k, (x, n) in enumerate(zip(xs, loads)):
                hot = hot_rows[k]
                cold = Rectangle(width=0.8, height=(n - hot) * unit, stroke_width=0, fill_color=DATA,
                                 fill_opacity=0.8).move_to([x, base_y + (n - hot) * unit / 2, 0])
                hr = Rectangle(width=0.8, height=max(hot, 0.01) * unit, stroke_width=0, fill_color=NO,
                               fill_opacity=0.85 if hot else 0).move_to([x, base_y + (n - hot / 2) * unit, 0])
                g.add(VGroup(cold, hr))
            return g
        b_plain = bars(load_plain, [n_hot if k == hot_to else 0 for k in range(4)])
        b_salt = bars(load_salt, [n_hot // 4] * 4)
        dots = VGroup()
        targets = []
        for i, d, h in traffic:
            dots.add(Dot(src[i].get_bottom() + DOWN * 0.15, radius=0.06, color=NO if h else DATA))
            targets.append([xs[d], base_y + 0.2, 0])
        mid = label(r"rows sent by $\mathrm{hash}(\mathit{key}) \bmod 4$", font_size=18, color=GREY_A).move_to(
            [-3.95, 1.35, 0])
        salt_l = label(r"salted: \ hot\#0 \dots \ hot\#3", font_size=18, color=YES).move_to([-3.95, 1.35, 0])
        illus = note(r"illustrative", font_size=16).next_to(baseline, RIGHT, buff=0.25)
        ch = bar_chart([ideal, s["max_plain"], s["max_salted"]], [r"ideal\\share", r"slowest,\\plain",
                                                                    r"slowest,\\salted"],
                       [GREY_B, NO, YES], height=3.0, bar_w=1.0, gap=0.8, fmt_=lambda v: f"{v:,.0f}", font_size=18)
        ch.move_to([3.85, 0.4, 0])
        facts = VGroup(*[label(rf"${f:.2f}\times$", font_size=18, color=BLACK).move_to(b.get_top() + DOWN * 0.22)
                         for f, b in zip((1.0, s["slowdown_plain"], s["slowdown_salted"]), ch.bars)])
        cap = label(rf"measured: \ {rows:,} rows, \ {w} workers, \ one key with a fifth of them", font_size=18,
                    color=GREY_A).next_to(ch, UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"a query ends when its slowest worker does \ (Part 39's tail); \ backup tasks cannot help: "
                          r"\ the worker is not slow, \ its share is large", 12.4, font_size=20, color=NO),
            wrapped_label(rf"\textbf{{salting}}: \ split the hot key into {SALT} sub-keys on the big side, \ copy its "
                          r"matches on the small side to each; \ heavy-hitter sketches find hot keys \ (Chapter 6)",
                          12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Hashing spreads keys evenly, not rows. <bookmark mark='a'/> If one key is hot, all its rows go to one "
            "worker. <bookmark mark='b'/> We measured it: two hundred thousand rows on sixteen workers, one key "
            "holding a fifth. The busiest worker gets almost four times its fair share, and a query finishes only "
            "when its slowest worker does. Part 39's backup tasks cannot help: that worker is not slow, its share is "
            "large. <bookmark mark='c'/> The fix is salting: split the hot key into eight random sub-keys, and copy "
            "its matches on the small side eight times. The slowest worker now carries "
            f"{s['slowdown_salted']:.1f} times the ideal. <bookmark mark='d'/> Chapter 6's heavy-hitter sketches find hot keys cheaply, and Spark's "
            "adaptive execution splits skewed partitions as the query runs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(baseline), FadeIn(names), FadeIn(mid), FadeIn(illus))
            vo.wait_until("a")
            self.add(dots)
            self.play(LaggedStart(*[d.animate.move_to(t) for d, t in zip(dots, targets)], lag_ratio=0.06),
                      run_time=2.5)
            self.play(FadeOut(dots), *[GrowFromEdge(b, DOWN) for b in b_plain])
            vo.wait_until("b")
            self.play(FadeIn(cap), FadeIn(ch.names), *[FadeIn(x) for x in ch[0:1]])
            self.play(GrowFromEdge(ch.bars[0], DOWN), FadeIn(ch.vals[0]), FadeIn(facts[0]))
            self.play(GrowFromEdge(ch.bars[1], DOWN), FadeIn(ch.vals[1]), FadeIn(facts[1]))
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(Transform(b_plain, b_salt), FadeTransform(mid, salt_l))
            self.play(GrowFromEdge(ch.bars[2], DOWN), FadeIn(ch.vals[2]), FadeIn(facts[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def vectorized(self):
        head = label(r"A batch at a time", font_size=36).to_edge(UP, buff=0.3)
        left = code_block(["while row := child.next():", "    if row.price > 100:", "        total += row.amount"],
                          size=16)
        right = code_block(["while batch := child.next_batch():", "    sel = select_gt(batch.price, 100)",
                            "    total += sum_at(batch.amount, sel)"], size=16)
        t_l = label(r"one row per call: \ Volcano \ (Graefe, \ 1994)", font_size=19, color=NO)
        t_r = label(r"a batch per call: \ MonetDB/X100 \ (Boncz et al., \ 2005)", font_size=19, color=YES)
        g_l = VGroup(t_l, left).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-4.0, 1.85, 0])
        g_r = VGroup(t_r, right).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.2, 1.85, 0])
        g_l.align_to([-6.6, 0, 0], LEFT)
        price = [40, 120, 90, 300, 150, 20, 110, 60]
        amount = [3, 5, 2, 7, 4, 1, 6, 2]
        sel = [i for i, p in enumerate(price) if p > 100]
        x0, cw = -1.6, 0.66
        ys = (0.0, -0.75, -1.5)
        p_cells = VGroup(*[cell(f"{v}", DATA, w=cw).move_to([x0 + i * cw, ys[0], 0]) for i, v in enumerate(price)])
        a_cells = VGroup(*[cell(f"{v}", LAM, w=cw).move_to([x0 + i * cw, ys[1], 0]) for i, v in enumerate(amount)])
        s_cells = VGroup(*[cell(f"{v}", YES, w=cw).move_to([x0 + k * cw, ys[2], 0]) for k, v in enumerate(sel)])
        rn = VGroup(*[label(t, font_size=18, color=c).move_to([0, y, 0]) for t, c, y in (
            (r"price", DATA, ys[0]), (r"amount", LAM, ys[1]), (r"selection vector", YES, ys[2]))])
        for r in rn:
            r.align_to([x0 - cw / 2 - 0.25, 0, 0], RIGHT)
        sweep = Rectangle(width=cw, height=0.5, stroke_color=HEAD, stroke_width=3).move_to(p_cells[0])
        total = label(rf"sum $=$ {sum(amount[i] for i in sel)}", font_size=22, color=YES).next_to(
            a_cells, RIGHT, buff=0.5)
        illus = note(r"illustrative batch of 8", font_size=16).next_to(p_cells, RIGHT, buff=0.5)
        lines = VGroup(
            wrapped_label(r"the call's overhead is paid once per batch of about a thousand values \ (DuckDB: \ "
                          r"2{,}048); \ loops with no calls inside become SIMD \ (Part 24), \ often run on Chapter "
                          r"8's dictionary codes without decoding", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"or compile each query to machine code \ (HyPer, \ Neumann, \ 2011); \ either way, \ "
                          r"exchanges pass whole batches between machines", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Inside each worker, how operators pass data matters as much as the network. <bookmark mark='a'/> Part "
            "35's iterator model, Volcano's, passes one row per call: a function call and a branch for every row and "
            "every operator. <bookmark mark='b'/> Vectorized execution, from MonetDB X100 in 2005, passes a batch: "
            "about a thousand values of each column, two thousand and forty-eight in DuckDB. <bookmark mark='c'/> A "
            "filter runs one tight loop over the price column and writes a selection vector, the positions that "
            "passed; the sum reads only those positions of the amount column. <bookmark mark='d'/> Loops without "
            "calls become Part 24's SIMD instructions, often on chapter eight's dictionary codes. The other answer, "
            "HyPer's, compiles each query to machine code."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g_l))
            vo.wait_until("b")
            self.play(FadeIn(g_r), FadeIn(p_cells), FadeIn(a_cells), FadeIn(rn[:2]), FadeIn(illus))
            vo.wait_until("c")
            self.play(Create(sweep), FadeIn(rn[2]))
            k = 0
            for i, p in enumerate(price):
                anims = [sweep.animate.move_to(p_cells[i])] if i else []
                if anims:
                    self.play(*anims, run_time=0.25)
                if p > 100:
                    self.play(p_cells[i][0].animate.set_stroke(YES, width=3), FadeIn(s_cells[k], shift=DOWN * 0.2),
                              run_time=0.35)
                    k += 1
                else:
                    self.play(p_cells[i].animate.set_opacity(0.35), run_time=0.25)
            self.play(FadeOut(sweep))
            self.play(*[a_cells[i][0].animate.set_stroke(YES, width=3).set_fill(YES, opacity=0.3) for i in sel],
                      *[a_cells[i].animate.set_opacity(0.35) for i in range(len(amount)) if i not in sel])
            self.play(FadeIn(total))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]))
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, HOT_SHARE, mono)
