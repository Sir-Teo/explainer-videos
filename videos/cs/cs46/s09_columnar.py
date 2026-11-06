from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs46.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono, tag_box)

# the pushdown experiment's table and filter (explainer/cs/data/columnar.py, pushdown's defaults): a million rows,
# row groups of 100,000, and the filter 420,000 <= x < 430,000
N_ROWS, GROUP, LO, HI = 1_000_000, 100_000, 420_000, 430_000


def cell(text, color, w=0.78, h=0.42, size=16):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=0.18)
    return VGroup(r, label(text, font_size=size, color=WHITE).move_to(r))


def segment(text, color, w, h=0.55, size=18, code=False):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.15)
    t = mono(text, size=size - 2, color=color) if code else label(text, font_size=size, color=WHITE)
    if t.width > w - 0.1:
        t.width = w - 0.1
    return VGroup(r, t.move_to(r))


def zoom(a, b):
    """Two dashed lines from the bottom corners of ``a`` to the top corners of ``b``: b is a's inside."""
    return VGroup(DashedLine(a.get_corner(DL), b.get_corner(UL), color=GREY_C, stroke_width=1.2),
                  DashedLine(a.get_corner(DR), b.get_corner(UR), color=GREY_C, stroke_width=1.2))


def mb(x):
    return f"{x / 1e6:.2f}"


class Columnar(VoiceoverScene):
    def construct(self):
        self.card()
        self.rows_columns()
        self.anatomy()
        self.encodings()
        self.sizes()
        self.pushdown()

    def card(self):
        card = chapter_card(8, r"Columnar files", r"How small can a table be, \ and how much of it can a query skip?",
                            lit=(2005, 2013), extra=((2005, r"Stonebraker et al.: \ C-Store"),
                                                     (2013, r"Parquet")), part=PART)
        with self.voiceover("Chapter eight. Columnar files."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rows_columns(self):
        head = label(r"Rows or columns", font_size=36).to_edge(UP, buff=0.3)
        names = [r"date", r"store", r"product", r"amount"]
        cols = [DATA, LAM, KERN, YES]
        data = [["Mar 1", "Leeds", "tea", "4.20"], ["Mar 1", "York", "rice", "3.10"],
                ["Mar 2", "Leeds", "tea", "9.50"], ["Mar 2", "Hull", "soap", "6.20"]]
        grid = VGroup(*[VGroup(*[cell(v, cols[c], w=1.0) for c, v in enumerate(row)]).arrange(RIGHT, buff=0)
                        for row in data]).arrange(DOWN, buff=0)
        grid.to_edge(LEFT, buff=0.6).shift(UP * (2.15 - grid.get_top()[1]))
        hdr = VGroup(*[label(n, font_size=16, color=cols[c]).next_to(grid[0][c], UP, buff=0.1)
                       for c, n in enumerate(names)])
        illus = note(r"illustrative", font_size=16).next_to(grid, RIGHT, buff=0.2).align_to(grid, DOWN)
        row_order = [grid[r][c] for r in range(4) for c in range(4)]
        col_order = [grid[r][c] for c in range(4) for r in range(4)]
        ccol = {id(grid[r][c]): cols[c] for r in range(4) for c in range(4)}
        rib_r = VGroup(*[cell(m[1].tex_string, ccol[id(m)]).move_to([-5.85 + k * 0.78, -0.55, 0])
                         for k, m in enumerate(row_order)])
        rib_c = VGroup(*[cell(m[1].tex_string, ccol[id(m)]).move_to([-5.85 + k * 0.78, -1.95, 0])
                         for k, m in enumerate(col_order)])
        l_r = label(r"row layout, \ as an operational database writes it", font_size=19, color=GREY_A).move_to(
            [0, -0.08, 0]).align_to(rib_r, LEFT)
        l_c = label(r"column layout", font_size=19, color=GREY_A).move_to([0, -1.48, 0]).align_to(
            rib_c, LEFT)
        q = mono("SELECT SUM(amount) FROM sales", size=18, color=HEAD).move_to([2.6, 1.7, 0])
        read_r = Rectangle(width=16 * 0.78 + 0.1, height=0.56, stroke_color=NO, stroke_width=3).move_to(
            [-5.85 + 7.5 * 0.78, -0.55, 0])
        read_c = Rectangle(width=4 * 0.78 + 0.1, height=0.56, stroke_color=YES, stroke_width=3).move_to(
            [-5.85 + 13.5 * 0.78, -1.95, 0])
        n_r = label(r"reads every byte \ (all 16 values)", font_size=18, color=NO).next_to(q, DOWN, buff=0.3)
        n_c = label(r"reads 4 values, \ one contiguous run", font_size=18, color=YES).next_to(n_r, DOWN, buff=0.15)
        foot = wrapped_label(r"and one column's values share a type, \ and often a value: \ they compress far better "
                             r"than a mixed row \ (C-Store, \ Stonebraker et al., \ 2005)", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A warehouse query reads a few columns of many rows, so store the table by column. <bookmark mark='a'/> A "
            "small table of sales. <bookmark mark='b'/> Written row by row, as an operational database stores it, "
            "each row's values sit together. <bookmark mark='c'/> Written column by column, each column's values sit "
            "together instead. <bookmark mark='d'/> Now ask for the total amount. The row layout reads every byte of "
            "every row; the column layout reads one contiguous run, a quarter of the file, read sequentially, as Part "
            "34 showed disks prefer. <bookmark mark='e'/> And one column holds values of a single type, often "
            "repeating, which compress far better than a mixed row. C-Store made this argument in 2005."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(hdr), FadeIn(illus))
            vo.wait_until("b")
            self.play(FadeIn(l_r), LaggedStart(*[TransformFromCopy(a, b) for a, b in zip(row_order, rib_r)], lag_ratio=0.12), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(l_c), LaggedStart(*[TransformFromCopy(a, b) for a, b in zip(col_order, rib_c)], lag_ratio=0.12), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(q))
            self.play(Create(read_r), FadeIn(n_r))
            self.play(Create(read_c), FadeIn(n_c))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def anatomy(self):
        head = label(r"Inside a Parquet file", font_size=36).to_edge(UP, buff=0.3)
        parts = [("PAR1", GREY_A, 0.7, True), (r"row group 0", DATA, 3.0, False), (r"row group 1", DATA, 3.0, False),
                 (r"row group 2", DATA, 3.0, False), (r"footer", HEAD, 1.6, False), ("len", GREY_A, 0.6, True),
                 ("PAR1", GREY_A, 0.7, True)]
        bar = VGroup(*[segment(t, c, w, code=code) for t, c, w, code in parts]).arrange(RIGHT, buff=0)
        bar.move_to([0, 2.15, 0])
        rg = bar[2]
        cols = [(r"date", DATA), (r"store", LAM), (r"product", KERN), (r"amount", YES)]
        chunks = VGroup(*[segment(rf"{n} \ chunk", c, 2.0, h=0.5) for n, c in cols]).arrange(RIGHT, buff=0.1)
        chunks.move_to([-2.05, 0.85, 0])
        z1 = zoom(rg, chunks)
        ch = chunks[2]
        pages = VGroup(segment(r"dictionary page", LAM, 2.0, h=0.5),
                       *[segment(r"data page", KERN, 1.5, h=0.5) for _ in range(3)]).arrange(RIGHT, buff=0.1)
        pages.move_to([-3.2, -0.45, 0])
        z2 = zoom(ch, pages)
        page_n = wrapped_label(r"a data page: \ a small header \ (encoding, \ count, \ sizes), \ then the levels "
                               r"\ (Chapter 9), \ then the values; \ encoded and compressed as a unit", 6.6,
                               font_size=19, color=KERN).next_to(pages, DOWN, buff=0.3).align_to(pages, LEFT)
        foot_box = RoundedRectangle(width=4.6, height=2.0, corner_radius=0.1, stroke_color=HEAD, stroke_width=2,
                                    fill_color=BG, fill_opacity=1).move_to([4.5, -1.5, 0])
        foot_t = wrapped_label(r"the schema; \ for every row group and column chunk: \ its offset and size, \ its "
                               r"encodings, \ and statistics \ (min, \ max, \ null count)", 4.2, font_size=19,
                               color=HEAD).move_to(foot_box)
        z3 = zoom(bar[4], foot_box)
        read = wrapped_label(r"a reader fetches the footer first, \ then seeks to exactly the chunks a query needs",
                             12.4, font_size=21, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Parquet, created at Twitter and Cloudera in 2013, is the columnar file most warehouses and data lakes "
            "now share. <bookmark mark='a'/> A file begins and ends with four magic bytes, P A R one. In between, "
            "rows are cut into row groups, large horizontal slices that can be read in parallel. <bookmark mark='b'/> "
            "Within a row group, each column is one contiguous column chunk. <bookmark mark='c'/> A chunk is split "
            "into pages, the unit of encoding and compression: often a dictionary page, then data pages, each holding "
            "a small header, levels and values. <bookmark mark='d'/> The footer holds the schema and, for every "
            "chunk, its place, its encodings and its statistics. A reader fetches the footer first, then seeks to "
            "just the chunks it needs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in bar], lag_ratio=0.15), run_time=2)
            vo.wait_until("b")
            self.play(Indicate(rg, color=DATA, scale_factor=1.05))
            self.play(Create(z1), LaggedStart(*[FadeIn(c) for c in chunks], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("c")
            self.play(Indicate(ch, color=KERN, scale_factor=1.05))
            self.play(Create(z2), LaggedStart(*[FadeIn(p) for p in pages], lag_ratio=0.2), run_time=1.5)
            self.play(FadeIn(page_n))
            vo.wait_until("d")
            self.play(Create(z3), FadeIn(foot_box), FadeIn(foot_t))
            self.play(FadeIn(read))
        self.wait(0.4)
        self.clear_scene()

    def encodings(self):
        head = label(r"Dictionary, \ bit-packing, \ run lengths, \ deltas", font_size=36).to_edge(UP, buff=0.3)
        words = "the whale the sea the the whale sea".split()
        vocab = {"the": 0, "whale": 1, "sea": 2}
        xs = [-4.1 + 0.95 * k for k in range(len(words))]
        ys = [2.15, 1.15, 0.25, -0.75, -1.95]
        names = VGroup(*[label(t, font_size=20, color=GREY_A).move_to([-6.0, y, 0]) for t, y in zip(
            (r"plain", r"dictionary", r"bit-packed", r"sorted", r"delta"), ys)])
        for n in names:
            n.align_to([-6.7, 0, 0], LEFT)
        plain = VGroup(*[tag_box(w, DATA, size=16).move_to([x, ys[0], 0]) for w, x in zip(words, xs)])
        idx = VGroup(*[tag_box(str(vocab[w]), LAM, size=16, w=0.5).move_to([x, ys[1], 0]) for w, x in zip(words, xs)])
        dpage = VGroup(*[mono(f"{i}  {w}", size=16, color=LAM) for w, i in vocab.items()]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08)
        dbox = SurroundingRectangle(dpage, color=LAM, buff=0.15, corner_radius=0.08)
        dtitle = label(r"dictionary page", font_size=16, color=LAM).next_to(dbox, UP, buff=0.08)
        dict_g = VGroup(dbox, dpage, dtitle).move_to([4.6, 1.3, 0])
        bits = VGroup(*[mono(f"{vocab[w]:02b}", size=18, color=KERN).move_to([x, ys[2], 0])
                        for w, x in zip(words, xs)])
        n_bits = label(r"2 bits each: \ 8 values in 2 bytes", font_size=18, color=KERN).move_to([4.6, ys[2], 0])
        srt = sorted(vocab[w] for w in words)
        sidx = VGroup(*[tag_box(str(v), YES, size=16, w=0.5).move_to([x, ys[3], 0]) for v, x in zip(srt, xs)])
        runs = []
        for v in sorted(set(srt)):
            ks = [k for k, s in enumerate(srt) if s == v]
            runs.append((v, ks))
        braces = VGroup(*[Brace(VGroup(*[sidx[k] for k in ks]), DOWN, buff=0.06, color=YES) for _, ks in runs])
        rl = VGroup(*[label(rf"{len(ks)} $\times$ {v}", font_size=16, color=YES).next_to(b, DOWN, buff=0.04)
                      for (v, ks), b in zip(runs, braces)])
        n_runs = label(r"Part 21's run-length coding", font_size=18, color=YES).move_to([4.6, ys[3], 0])
        base = tag_box("1700000000000", HEAD, size=16).move_to([-3.4, ys[4], 0])
        deltas = VGroup(*[tag_box(t, HEAD, size=16) for t in ("+731", "+12", "+1904", "+40")]).arrange(
            RIGHT, buff=0.12).next_to(base, RIGHT, buff=0.2)
        n_delta = label(r"first value, \ then small differences", font_size=18, color=HEAD).next_to(
            deltas, RIGHT, buff=0.3)
        foot = note(r"illustrative values; \ Parquet's hybrid stores long runs as (count, \ value) \ and bit-packs "
                    r"the rest", font_size=18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Each chunk then picks its encodings. <bookmark mark='a'/> Here is a column of words, stored plainly, "
            "every string in full. <bookmark mark='b'/> Dictionary encoding stores each distinct word once, in a "
            "dictionary page, and replaces every value by its small integer index. <bookmark mark='c'/> The indices "
            "need only as many bits as the dictionary's size requires, here two, so they are bit-packed: eight values "
            "in two bytes. <bookmark mark='d'/> Sorted, equal indices sit together, and Part 21's run-length coding "
            "stores each run as a count and a value. <bookmark mark='e'/> And timestamps that creep forward store a "
            "first value and then small differences: delta encoding."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(names[0]), LaggedStart(*[FadeIn(p) for p in plain], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(dict_g), FadeIn(names[1]))
            self.play(LaggedStart(*[TransformFromCopy(p, i) for p, i in zip(plain, idx)], lag_ratio=0.1),
                      run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(names[2]), LaggedStart(*[TransformFromCopy(i, b) for i, b in zip(idx, bits)],
                                                    lag_ratio=0.1), FadeIn(n_bits), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(names[3]), FadeIn(sidx))
            self.play(LaggedStart(*[GrowFromCenter(b) for b in braces], lag_ratio=0.3), FadeIn(rl), FadeIn(n_runs))
            vo.wait_until("e")
            self.play(FadeIn(names[4]), FadeIn(base))
            self.play(LaggedStart(*[FadeIn(d, shift=RIGHT * 0.1) for d in deltas], lag_ratio=0.2), FadeIn(n_delta),
                      FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def sizes(self):
        e = load("encodings")
        ints = load("ints")
        head = label(r"Encodings on the novels' words", font_size=36).to_edge(UP, buff=0.3)
        idx_bytes = e["values"] * e["index_bits"] / 8          # the packed indices; the rest is the dictionary page
        sub = label(rf"{e['values']:,} words of the novels as one column: \ {e['distinct']:,} distinct, \ so "
                    rf"{e['index_bits']}-bit indices", font_size=20, color=GREY_A).next_to(head, DOWN, buff=0.3)
        scale = 5.0 / e["plain"]
        x0 = -2.0
        rows = [(r"plain, \ with lengths", [(e["plain"], DATA)], e["plain"]),
                (r"plain, \ then gzip", [(e["plain_gzip"], GREY_B)], e["plain_gzip"]),
                (r"dictionary page + indices", [(e["dictionary"] - idx_bytes, LAM), (idx_bytes, KERN)],
                 e["dictionary"]),
                (r"+ run lengths, \ reading order", [(e["dict_rle"], KERN)], e["dict_rle"]),
                (r"+ run lengths, \ sorted", [(e["dict_rle_sorted"], YES)], e["dict_rle_sorted"]),
                (None, None, None),
                (rf"{ints['values']:,} timestamps, \ plain", [(ints["plain"], DATA)], ints["plain"]),
                (r"delta-encoded", [(ints["delta"], HEAD)], ints["delta"])]
        bars = VGroup()
        y = 1.95
        for name, segs, total in rows:
            if name is None:
                y -= 0.45
                continue
            n = label(name, font_size=19, color=WHITE)
            n.move_to([x0 - 0.25 - n.width / 2, y, 0])
            parts = VGroup()
            x = x0
            for v, c in segs:
                w = max(0.03, v * scale)
                parts.add(Rectangle(width=w, height=0.36, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to(
                    [x + w / 2, y, 0]))
                x += w
            val = label(rf"{mb(total)} MB", font_size=19, color=segs[-1][1]).next_to(parts, RIGHT, buff=0.15)
            bars.add(VGroup(n, parts, val))
            y -= 0.55
        axis = Line([x0, 2.25, 0], [x0, y + 0.25, 0], color=GREY_C, stroke_width=1.5)
        key = VGroup(VGroup(Square(0.18, stroke_width=0, fill_color=LAM, fill_opacity=0.85),
                            label(rf"dictionary page {mb(e['dictionary'] - idx_bytes)} MB", font_size=16,
                                  color=LAM)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.18, stroke_width=0, fill_color=KERN, fill_opacity=0.85),
                            label(rf"indices {mb(idx_bytes)} MB", font_size=16, color=KERN)).arrange(RIGHT, buff=0.1)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(bars[2][2], RIGHT, buff=0.35)
        foot = wrapped_label(rf"in reading order a word almost never repeats 8 times running, \ so runs save nothing; "
                             rf"\ sorted, \ {e['dict_rle_sorted'] / e['plain'] * 100:.0f}\% of plain; \ timestamps: "
                             rf"{ints['plain'] // ints['values']} bytes each against "
                             rf"{round((ints['delta'] - 8) * 8 / (ints['values'] - 1))} bits", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "What do these save on real text? <bookmark mark='a'/> We took three hundred thousand words of the novels "
            "as one column. Plainly, with their lengths, it takes two point five eight megabytes. <bookmark "
            "mark='b'/> There are thirty thousand five hundred and fifteen distinct words, so indices need fifteen "
            "bits; with the dictionary page they come to zero point nine three megabytes, about a third. Gzip alone "
            "does a little better, zero point eight. <bookmark mark='c'/> In reading order a word almost never "
            "repeats eight times running, so run lengths add nothing. Sort the column, and they halve it, to zero "
            "point four seven, under a fifth of plain. <bookmark mark='d'/> A hundred thousand timestamps shrink from "
            "eight hundred kilobytes to a hundred and thirty-eight, eleven bits each. And both are undone by simple "
            "arithmetic, far cheaper to decode than gzip."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sub), Create(axis), FadeIn(bars[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[2]), FadeIn(key))
            self.play(FadeIn(bars[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars[3]))
            self.play(FadeIn(bars[4]))
            vo.wait_until("d")
            self.play(FadeIn(bars[5]), FadeIn(bars[6]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def pushdown(self):
        p = load("pushdown")
        head = label(r"Statistics and predicate pushdown", font_size=36).to_edge(UP, buff=0.3)
        q = mono(f"WHERE x >= {LO} AND x < {HI}", size=18, color=HEAD).next_to(head, DOWN, buff=0.3)
        n = p["sorted"]["groups"]
        w, gap = 1.12, 0.12
        x_first = -(n * w + (n - 1) * gap) / 2 + w / 2

        def row(y, spans, title, color):
            boxes = VGroup()
            for g, (lo, hi) in enumerate(spans):
                box = Rectangle(width=w, height=0.9, stroke_color=GREY_B, stroke_width=1.5).move_to(
                    [x_first + g * (w + gap), y, 0])
                track = Line(box.get_left() + RIGHT * 0.06 + DOWN * 0.18, box.get_right() + LEFT * 0.06 + DOWN * 0.18,
                             color=GREY_D, stroke_width=2)
                tw = track.get_length()
                rng = Line(track.get_start() + RIGHT * tw * lo / N_ROWS, track.get_start() + RIGHT * tw * hi / N_ROWS,
                           color=color, stroke_width=7)
                band = Rectangle(width=max(0.03, tw * (HI - LO) / N_ROWS), height=0.34, stroke_width=0,
                                 fill_color=HEAD, fill_opacity=0.9).move_to(
                    track.get_start() + RIGHT * tw * (LO + HI) / 2 / N_ROWS)
                gid = label(f"{g}", font_size=16, color=GREY_A).move_to(box.get_center() + UP * 0.22)
                boxes.add(VGroup(box, track, rng, band, gid))
            t = label(title, font_size=20, color=color).next_to(boxes, UP, buff=0.15).align_to(boxes, LEFT)
            return boxes, t
        legend = VGroup(Rectangle(width=0.1, height=0.3, stroke_width=0, fill_color=HEAD, fill_opacity=0.9),
                        label(r"the filter's range", font_size=18, color=HEAD),
                        Line(ORIGIN, RIGHT * 0.5, color=DATA, stroke_width=7),
                        label(r"a row group's min to max, \ from the footer", font_size=18, color=DATA)
                        ).arrange(RIGHT, buff=0.15).next_to(q, DOWN, buff=0.2)
        legend[2:].shift(RIGHT * 0.3)
        legend.set_x(0)
        srt = [(g * GROUP, (g + 1) * GROUP - 1) for g in range(n)]
        rnd = [(0, N_ROWS - 1)] * n
        b1, t1 = row(0.9, srt, r"sorted by x: \ each row group's min and max are narrow", DATA)
        b2, t2 = row(-1.55, rnd, r"random order: \ every row group spans nearly everything", LAM)
        mm = VGroup(*[VGroup(label(f"{lo:,}", font_size=16, color=GREY_B), label(f"{hi:,}", font_size=16,
                                                                                  color=GREY_B)).arrange(
            DOWN, buff=0.04).next_to(b, DOWN, buff=0.08) for (lo, hi), b in zip(srt, b1)])
        hit1 = [g for g, (lo, hi) in enumerate(srt) if lo < HI and hi >= LO]
        r1 = label(rf"read {p['sorted']['read']} of {n} row groups", font_size=21, color=YES).next_to(
            b1, RIGHT, buff=0.1)
        r1.next_to(t1, RIGHT, buff=0.5)
        r2 = label(rf"read {p['random']['read']} of {p['random']['groups']} row groups", font_size=21,
                   color=NO).next_to(t2, RIGHT, buff=0.5)
        foot = wrapped_label(r"it pays only when the table is sorted or clustered by the filtered column; \ the "
                             r"footer's statistics, \ page indexes and Bloom filters all let a reader decide without "
                             r"reading", 12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Statistics give the largest saving of all: not reading. <bookmark mark='a'/> Here are a million rows in "
            "ten row groups, and a query that wants x between four hundred and twenty thousand and four hundred and "
            "thirty thousand. <bookmark mark='b'/> If the table is sorted by x, each group's minimum and maximum are "
            "close together, and only one group overlaps the filter. The other nine are skipped unopened: the filter "
            "has been pushed down into the scan. <bookmark mark='c'/> In random order, every group spans nearly "
            "everything, and all ten must be read. <bookmark mark='d'/> So statistics pay only when data is sorted or "
            "clustered by the columns people filter on, which is why table layout matters so much."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q), FadeIn(legend))
            vo.wait_until("b")
            self.play(FadeIn(t1), FadeIn(b1), FadeIn(mm))
            self.play(*[b1[g][0].animate.set_stroke(GREY_D).set_fill(BG, opacity=0) for g in range(n)
                        if g not in hit1], *[b1[g][2].animate.set_opacity(0.3) for g in range(n) if g not in hit1],
                      *[b1[g][0].animate.set_stroke(YES, width=3) for g in hit1])
            self.play(FadeIn(r1))
            vo.wait_until("c")
            self.play(FadeIn(t2), FadeIn(b2))
            self.play(*[bx[0].animate.set_stroke(NO, width=3) for bx in b2], FadeIn(r2))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, NO)
