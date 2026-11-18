from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.compute import load as load34
from videos.cs.cs35.compute import load as load35
from videos.cs.cs48.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, mono,
                                   tag_box)


def cells(rows, cols, w=0.34, h=0.2, color=GREY_B, head=True):
    """A small table drawn as a grid of cells, the first row filled as a header."""
    g = VGroup(*[Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.2,
                           fill_color=color, fill_opacity=0.35 if (head and r == 0) else 0.0)
                 for r in range(rows) for _ in range(cols)])
    g.arrange_in_grid(rows=rows, cols=cols, buff=0)
    return g


class Storage(WatchScene):
    def construct(self):
        self.card()
        self.shapes()
        self.columns()
        self.engine()
        self.indexes()

    def card(self):
        self.chapter(7, r"Choosing storage", r"Which shape of database fits the questions you will ask?", lit=(1970, 2006), extra=((1970, r"Codd: \ the relational model"),
                                                     (2006, r"Chang et al.: \ Bigtable")), part=PART, said="Chapter seven. Choosing storage.")

    # ------------------------------------------------------------------ six shapes
    def shapes(self):
        head = label(r"Six shapes of data", font_size=36).to_edge(UP, buff=0.3)
        W, H = 4.25, 2.85

        def tile(title, color, drawing, use, examples):
            box = RoundedRectangle(width=W, height=H, corner_radius=0.12, stroke_color=GREY_D, stroke_width=1.5)
            t = label(title, font_size=23, color=color).next_to(box.get_top(), DOWN, buff=0.15)
            ex = label(examples, font_size=17, color=GREY_B).next_to(box.get_bottom(), UP, buff=0.14)
            u = wrapped_label(use, W - 0.3, font_size=18, color=WHITE).next_to(ex, UP, buff=0.12)
            room_top, room_bot = t.get_bottom()[1] - 0.12, u.get_top()[1] + 0.12
            if drawing.height > room_top - room_bot:
                drawing.scale_to_fit_height(room_top - room_bot)
            if drawing.width > W - 0.4:
                drawing.scale_to_fit_width(W - 0.4)
            drawing.move_to([box.get_x(), (room_top + room_bot) / 2, 0])
            return VGroup(box, t, drawing, u, ex)

        # relational: two tables and a foreign key
        users, pastes = cells(3, 2), cells(4, 3)
        rel = VGroup(users, pastes).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        fk = Line(users[2].get_right() + LEFT * 0.34, pastes[4].get_left(), color=HEAD, stroke_width=2.5)
        fk.put_start_and_end_on(users[2].get_center(), pastes[4].get_center())
        rel_d = VGroup(rel, fk)
        # key-value: a key and an opaque value
        k = tag_box("user:42", DATA, size=16)
        v = VGroup(Rectangle(width=1.5, height=0.5, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9),
                   label(r"opaque bytes", font_size=16, color=GREY_A))
        v[1].move_to(v[0])
        kv_d = VGroup(k, Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, color=WHITE, stroke_width=2.5,
                               max_tip_length_to_length_ratio=0.3), v).arrange(RIGHT, buff=0.15)
        # document: one nested record
        doc_d = code_block(['{"name": "Ada",', ' "pastes": [', '  {"title": "notes"},', '  {"title": "todo"}]}'],
                           size=16)
        # wide-column: sorted row keys, sparse columns
        wc_rows = VGroup()
        for name, n in (("ada", 4), ("bob", 2), ("cyd", 5)):
            wc_rows.add(VGroup(tag_box(name, KERN, size=16, w=0.8, h=0.36),
                               *[Square(side_length=0.3, stroke_width=0, fill_color=KERN, fill_opacity=0.55)
                                 for _ in range(n)]).arrange(RIGHT, buff=0.08))
        wc_d = wc_rows.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        # graph: nodes and edges
        P = [[-1.0, 0.3, 0], [-0.3, 0.6, 0], [0.4, 0.4, 0], [1.0, 0.0, 0], [-0.6, -0.4, 0], [0.3, -0.4, 0]]
        E = [(0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (5, 2), (1, 5)]
        gr_d = VGroup(*[Line(P[a], P[b], color=GREY_B, stroke_width=2) for a, b in E],
                      *[Dot(p, radius=0.09, color=YES) for p in P])
        # time-series: timestamped points, appended at the right
        vals = [0.2, 0.35, 0.3, 0.5, 0.45, 0.7, 0.55, 0.6, 0.8, 0.65]
        base = Line([-1.4, -0.4, 0], [1.2, -0.4, 0], color=GREY_C, stroke_width=1.5)
        pts = VGroup(*[Dot([-1.3 + 0.25 * i, -0.4 + y, 0], radius=0.05, color=LAM) for i, y in enumerate(vals)])
        ts_d = VGroup(base, pts, Arrow([1.15, 0.1, 0], [1.75, 0.1, 0], buff=0, color=LAM, stroke_width=2.5,
                                       max_tip_length_to_length_ratio=0.3))
        tiles = VGroup(
            tile(r"relational", DATA, rel_d, r"joins, \ transactions, \ any question", r"PostgreSQL, \ MySQL"),
            tile(r"key--value", HEAD, kv_d, r"one question, \ answered fast", r"Redis, \ DynamoDB"),
            tile(r"document", YES, doc_d, r"a whole nested record together", r"MongoDB"),
            tile(r"wide-column", KERN, wc_d, r"sorted rows of sparse columns; \ heavy writes",
                 r"Bigtable, \ Cassandra, \ HBase"),
            tile(r"graph", YES, gr_d, r"following edges, \ many hops", r"Neo4j"),
            tile(r"time-series", LAM, ts_d, r"append points, \ summarise windows", r"Prometheus, \ InfluxDB"),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.2, 0.2)).next_to(head, DOWN, buff=0.25)
        foot = note(r"schematic", font_size=16).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Every design needs somewhere to keep its data, and databases come in a handful of shapes. "
            "<bookmark mark='a'/> Relational databases keep tables of rows and join them when asked, with "
            "transactions, and a planner that answers questions nobody anticipated, as Part 35 showed. "
            "<bookmark mark='b'/> A key-value store answers one question, the value for this key, very fast, and "
            "scales by splitting the keys. A document store keeps a whole nested record together. "
            "<bookmark mark='c'/> Wide-column stores, after Google's Bigtable, keep sorted rows of sparse columns, "
            "built for heavy writes. Graph databases follow edges, hop after hop; and time-series databases append "
            "timestamped points and summarise them over windows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tiles[0]))
            self.play(Indicate(fk, color=HEAD))
            vo.wait_until("b")
            self.play(FadeIn(tiles[1]))
            self.play(FadeIn(tiles[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(t) for t in tiles[3:]], lag_ratio=0.5), run_time=2.5)
            self.play(LaggedStart(*[Indicate(p, color=WHITE, scale_factor=1.6) for p in pts[-3:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ rows against columns
    def columns(self):
        c = load35("columns")
        head = label(r"Access patterns decide", font_size=36).to_edge(UP, buff=0.3)
        cols, rows = c["cols"], 8

        def grid(title, color):
            g = cells(rows, cols, w=0.24, h=0.24, color=GREY_C, head=False)
            t = label(title, font_size=21, color=color).next_to(g, UP, buff=0.12).align_to(g, LEFT)
            return VGroup(t, g)
        rs = grid(r"row store: \ each row together", NO)
        cs = grid(r"column store: \ each column together", YES)
        grids = VGroup(rs, cs).arrange(DOWN, buff=0.55, aligned_edge=LEFT).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        hl = VGroup(*[label(rf"{j}", font_size=16, color=HEAD).next_to(cs[1][j], DOWN, buff=0.08) for j in (3, 7)])
        q = wrapped_label(rf"{c['n']:,} rows \ $\times$ \ {cols} columns: \\ add up column 3 where column 7 "
                          r"$<$ 100", 6.2, font_size=21, color=HEAD)
        q.move_to([3.4, 2.3, 0])
        tab = grid_table([r"", r"row store", r"column store"],
                         [[r"bytes read", rf"{c['bytes_row'] / 1e6:.0f} MB", rf"{c['bytes_col'] / 1e6:.0f} MB"],
                          [r"scan time", rf"{1000 * c['row_s']:.1f} ms", rf"{1000 * c['col_s']:.1f} ms"]],
                         widths=[2.0, 2.0, 2.3], row_h=0.6, font_size=21,
                         colors=[[WHITE, NO, YES], [WHITE, NO, YES]], mono_cols=())
        tab.next_to(q, DOWN, buff=0.5)
        notes = VGroup(
            wrapped_label(r"rows suit fetching and updating whole records \ (transactions); \ columns suit scanning "
                          r"a few fields of many \ (analytics, \ Part 46's warehouses)", 6.0, font_size=19,
                          color=WHITE),
            note(r"measured in Part 35; \ grids schematic", font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.45).align_to(tab, LEFT)
        row_cells, col_cells = rs[1], cs[1]
        with self.voiceover(
            "The shape that fits is the one that matches the questions you will ask, so list the access patterns "
            "first. <bookmark mark='a'/> Take one analytical question over a million rows of sixteen columns: add "
            "up column three wherever column seven is below a hundred. <bookmark mark='b'/> A row store keeps "
            "each row together, so the scan drags all sixteen columns through memory, a hundred and twenty-eight "
            "megabytes. <bookmark mark='c'/> A column store keeps each column together and reads only the two it "
            "needs, sixteen megabytes. In Part 35's measurement, the column scan took four milliseconds against "
            "fourteen. <bookmark mark='d'/> Rows suit fetching and updating whole records; columns suit scanning "
            "a few fields of very many."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grids))
            vo.wait_until("a")
            self.play(FadeIn(q), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            vo.wait_until("b")
            self.play(LaggedStart(*[VGroup(*row_cells[r * cols:(r + 1) * cols]).animate.set_fill(NO, 0.6)
                                    for r in range(rows)], lag_ratio=0.35), run_time=2.5)
            self.play(FadeIn(tab.cells[1][0]), FadeIn(tab.cells[1][1]))
            vo.wait_until("c")
            self.play(FadeIn(hl), LaggedStart(*[VGroup(col_cells[r * cols + 3], col_cells[r * cols + 7]).animate
                                                .set_fill(YES, 0.7) for r in range(rows)], lag_ratio=0.35),
                      run_time=2.0)
            self.play(FadeIn(tab.cells[1][2]))
            self.play(FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("d")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the engine underneath
    def engine(self):
        self.ask(r"A write-heavy workload. \\ Which engine suits it?", [r"a B-tree", r"an LSM tree"], 1,
                 say="A workload that writes far more than it reads. Which storage engine suits it?",
                 reveal="An LSM tree: appends and merges, instead of updates in place.")
        L = load34("lsm")
        head = label(r"The engine underneath", font_size=36).to_edge(UP, buff=0.3)
        bt = L["btree"]
        lsm = {(r["policy"], r["bloom_bits"]): r for r in L["rows"]}
        lev, tie = lsm[("leveled", 0)], lsm[("tiered", 0)]
        items = [(rf"B-tree, \ {100 * bt[0]['cache_fraction']:.0f}\% cached", bt[0]["write_amp"], NO),
                 (rf"B-tree, \ {100 * bt[-1]['cache_fraction']:.0f}\% cached", bt[-1]["write_amp"], NO),
                 (r"LSM, \ levelled", lev["write_amp"], KERN),
                 (r"LSM, \ tiered", tie["write_amp"], YES)]
        Hmax, bw, x0, y0 = 3.6, 1.0, -6.0, -2.3
        vmax = max(v for _, v, _ in items)
        bars, vals, names = VGroup(), VGroup(), VGroup()
        for i, (nm, v, col) in enumerate(items):
            x = x0 + i * 1.7 + bw / 2
            b = Rectangle(width=bw, height=Hmax * v / vmax, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([x, y0 + b.height / 2, 0])
            bars.add(b)
            vals.add(label(rf"{v:.1f}", font_size=20, color=col).next_to(b, UP, buff=0.08))
            names.add(wrapped_label(nm, 1.4, font_size=17, color=GREY_A).next_to([x, y0, 0], DOWN, buff=0.15))
        axis = Line([x0 - 0.2, y0, 0], [x0 + 3 * 1.7 + bw + 0.2, y0, 0], color=GREY_C, stroke_width=1.5)
        ttl = label(r"bytes written to disk per byte written", font_size=20, color=WHITE).next_to(
            bars, UP, buff=0.55).align_to(axis, LEFT)
        lev10, tie10 = lsm[("leveled", 10)], lsm[("tiered", 10)]
        tab = grid_table([r"runs probed", r"no filter", r"Bloom, \ 10 bits/key"],
                         [[r"levelled", f"{lev['read_miss']:.1f}", f"{lev10['read_miss']:.3f}"],
                          [r"tiered", f"{tie['read_miss']:.1f}", f"{tie10['read_miss']:.2f}"]],
                         widths=[1.9, 1.6, 2.6], row_h=0.55, font_size=20,
                         colors=[[KERN, WHITE, YES], [YES, NO, YES]], mono_cols=())
        tab.move_to([3.7, 0.9, 0])
        tl = label(r"looking up a key that is not there", font_size=19, color=GREY_A).next_to(tab, UP, buff=0.25)
        notes = VGroup(
            wrapped_label(r"a B-tree rewrites whole pages in place; \ an LSM tree buffers writes in memory and "
                          r"merges sorted runs on disk \ (Part 34)", 6.0, font_size=19, color=WHITE),
            wrapped_label(r"write-heavy stores \ (Cassandra, \ RocksDB) \ are LSM trees; \ most relational "
                          r"engines are B-trees", 6.0, font_size=19, color=HEAD),
            note(rf"Part 34's simulation: \ {L['n']:,} writes over {L['keys']:,} keys", font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.5).align_to(tab, LEFT)
        with self.voiceover(
            "Under the shape sits an engine, and it matters as much. <bookmark mark='a'/> A B-tree updates pages "
            "in place. In Part 34's simulation, with little of the tree cached, each byte the application wrote "
            "cost about forty bytes of disk writes, and still eighteen with over half the tree in memory. "
            "<bookmark mark='b'/> A log-structured merge tree buffers writes and merges sorted runs: about twelve "
            "with levelled compaction, about two with tiering. <bookmark mark='c'/> The price is paid on reads. "
            "Tiering leaves nineteen runs to probe for a key that is not there, until a Bloom filter of ten bits "
            "per key cuts that to a sixth of one. <bookmark mark='d'/> That is why write-heavy stores such as "
            "Cassandra and RocksDB are built on LSM trees."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(names), FadeIn(ttl), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(vals[0]))
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(vals[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[2], DOWN), FadeIn(vals[2]))
            self.play(GrowFromEdge(bars[3], DOWN), FadeIn(vals[3]))
            vo.wait_until("c")
            self.play(FadeIn(tl), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            self.play(FadeIn(VGroup(*tab.cells[1][:2])), FadeIn(VGroup(*tab.cells[2][:2])))
            self.play(FadeIn(tab.cells[1][2]), FadeIn(tab.cells[2][2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


    # ------------------------------------------------------------------ indexes
    def indexes(self):
        b = load35("btree")
        head = label(r"Every index is a bet", font_size=36).to_edge(UP, buff=0.3)
        # a small B-tree, a lookup's path lit
        node = lambda w=0.9: Rectangle(width=w, height=0.32, stroke_color=DATA, stroke_width=1.8)  # noqa: E731
        root = node().move_to([-4.3, 2.2, 0])
        mid = VGroup(*[node() for _ in range(3)]).arrange(RIGHT, buff=0.35).move_to([-4.3, 1.2, 0])
        leaves = VGroup(*[node(0.42) for _ in range(9)]).arrange(RIGHT, buff=0.08).move_to([-4.3, 0.2, 0])
        edges = VGroup(*[Line(root.get_bottom(), m.get_top(), color=GREY_C, stroke_width=1.5) for m in mid],
                       *[Line(mid[i // 3].get_bottom(), leaves[i].get_top(), color=GREY_C, stroke_width=1.2)
                         for i in range(9)])
        path = VGroup(root, mid[1], leaves[4])
        lv = {r["rows"]: r["levels"] for r in b["levels"]}
        tab = grid_table([r"rows", r"levels"], [[rf"$10^{{{k}}}$", f"{lv[10 ** k]}"] for k in (3, 6, 9, 12)],
                         widths=[1.4, 1.2], row_h=0.45, font_size=20, mono_cols=())
        tab.move_to([-0.9, 1.4, 0])
        tl = label(r"400 keys a node", font_size=18, color=GREY_B).next_to(tab, UP, buff=0.15)
        # pages of the word table: a range through a secondary index against one stored in index order
        n_pages = 36
        strip = VGroup(*[Square(side_length=0.3, stroke_color=GREY_C, stroke_width=1.2) for _ in range(n_pages)])
        strip.arrange(RIGHT, buff=0.05)
        strips = VGroup(strip, strip.copy()).arrange(DOWN, buff=0.75).move_to([0.3, -1.85, 0])
        lab_u = label(rf"secondary index: \ {b['hits']:,} rows on {b['pages_unclustered']} pages", font_size=20,
                      color=NO).next_to(strips[0], UP, buff=0.12).align_to(strips[0], LEFT)
        lab_c = label(rf"stored in index order: \ the same rows on {b['pages_clustered']} pages", font_size=20,
                      color=YES).next_to(strips[1], UP, buff=0.12).align_to(strips[1], LEFT)
        scattered = [1, 4, 6, 9, 12, 15, 17, 20, 23, 25, 28, 31, 33, 35]
        cost = wrapped_label(r"each index is one more structure to update on every insert, \ and more memory to "
                             r"keep warm: \ index the questions you will ask, \ and no others", 5.0, font_size=19,
                             color=HEAD).move_to([4.2, 1.3, 0])
        q = label(rf"WHERE word BETWEEN '{b['range'][0]}' AND '{b['range'][1]}'", font_size=18,
                  color=GREY_A).next_to(lab_u, UP, buff=0.3).align_to(lab_u, LEFT)
        foot = note(rf"Part 35: \ {b['rows']:,} rows of words, \ 100 rows a page; \ pages drawn illustrative",
                    font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Then index for the access patterns, with Part 35's B-trees. <bookmark mark='a'/> With four hundred "
            "keys to a node, a billion rows need only four levels, so a lookup is a handful of page reads. "
            "<bookmark mark='b'/> Where the rows sit matters too. In Part 35's word table, the range from whale "
            "to whales matched one thousand seven hundred and four rows. Through a secondary index they lay on "
            "nine hundred and sixty-six different pages; <bookmark mark='c'/> stored in index order, on eighteen. "
            "<bookmark mark='d'/> But every index is a bet. Each is one more structure to update on every insert, "
            "and more memory to keep warm. Index the questions you will ask, and no others."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot), Create(edges), FadeIn(root), FadeIn(mid), FadeIn(leaves))
            vo.wait_until("a")
            self.play(LaggedStart(*[p.animate.set_fill(HEAD, 0.8).set_stroke(HEAD) for p in path], lag_ratio=0.5))
            self.play(FadeIn(tl), FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(q), FadeIn(lab_u), FadeIn(strips[0]))
            self.play(LaggedStart(*[strips[0][i].animate.set_fill(NO, 0.8) for i in scattered], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(lab_c), FadeIn(strips[1]))
            self.play(strips[1][10].animate.set_fill(YES, 0.8), strips[1][11].animate.set_fill(YES, 0.8))
            vo.wait_until("d")
            self.play(FadeIn(cost))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, load)
