from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (CODE, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, load, mono, num)

COLS = [DATA, HEAD, LAM, KERN, YES, NO]


class Columns(VoiceoverScene):
    def construct(self):
        self.card()
        self.layouts()
        self.measured()
        self.compression()

    def card(self):
        card = chapter_card(14, r"Column stores", r"Why store a table sideways?", lit=(2005,),
                            extra=((2005, r"C-Store; \ MonetDB/X100"),), part=PART)
        with self.voiceover("Chapter fourteen. Column stores."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def layouts(self):
        head = label(r"Rows or columns, \ in the same pages", font_size=36).to_edge(UP, buff=0.3)
        W, H = 0.34, 0.3
        grid = VGroup(*[VGroup(*[Rectangle(width=W, height=H, stroke_width=0.8, stroke_color=GREY_D,
                                           fill_color=COLS[c], fill_opacity=0.55) for c in range(6)]).arrange(
            RIGHT, buff=0) for _ in range(6)]).arrange(DOWN, buff=0).move_to([-4.6, 0.6, 0])
        gl = label(r"a table: \ 6 rows, \ 6 columns", font_size=18, color=GREY_A).next_to(grid, UP, buff=0.15)
        row_store = VGroup(*[grid[r][c].copy() for r in range(6) for c in range(6)]).arrange(RIGHT, buff=0)
        col_store = VGroup(*[grid[r][c].copy() for c in range(6) for r in range(6)]).arrange(RIGHT, buff=0)
        row_store.width = 8.4
        col_store.width = 8.4
        row_store.move_to([2.3, 1.4, 0])
        col_store.move_to([2.3, -0.2, 0])
        rl = label(r"\textbf{row store}: \ each row together \ (good for fetching one order)", font_size=18,
                   color=WHITE).next_to(row_store, UP, buff=0.12)
        cl = label(r"\textbf{column store}: \ each column together \ (good for scanning one attribute)", font_size=18,
                   color=WHITE).next_to(col_store, UP, buff=0.12)
        q = mono("SELECT SUM(c3) FROM t WHERE c7 < 100", 18, YES).move_to([0, -1.5, 0])
        lines = VGroup(
            label(r"analytics read a few columns of many rows: \ a row store drags every column through memory",
                  font_size=19, color=NO),
            label(r"a column store reads only the two it needs, \ contiguously: \ $2/16$ of the bytes",
                  font_size=19, color=YES),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Everything so far has stored a table row by row, every attribute of a row together on a page. "
            "<bookmark mark='a'/> That suits transactions, which fetch or change a whole row: one order, one account. "
            "<bookmark mark='b'/> But turn the table sideways and store each column on its own pages. "
            "<bookmark mark='c'/> An analytic query, adding up one column over the rows that pass a test on "
            "another, touches two attributes of millions of rows. <bookmark mark='d'/> A row store must carry all "
            "sixteen columns through the memory hierarchy to get at two. <bookmark mark='e'/> A column store reads "
            "only those two, each a contiguous array: an eighth of the bytes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(gl))
            vo.wait_until("a")
            self.play(FadeIn(rl), TransformFromCopy(grid, row_store), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(cl), TransformFromCopy(grid, col_store), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]), *[row_store[k].animate.set_fill(opacity=0.9) for k in range(36)])
            vo.wait_until("e")
            self.play(FadeIn(lines[1]), *[col_store[k].animate.set_fill(opacity=0.12) for k in range(36)
                                          if k // 6 not in (3, 1)])
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        c = load("columns")
        head = label(rf"{num(c['n'])} rows, \ {c['cols']} columns, \ measured", font_size=36).to_edge(UP, buff=0.3)
        vals = [c["tuple_s"] * 1000, c["row_s"] * 1000, c["col_s"] * 1000]
        ch = bar_chart(vals, [r"tuple at a time\\(an interpreter)", r"vectorized,\\row store",
                              r"vectorized,\\column store"], [NO, HEAD, YES], height=3.2, bar_w=1.2, gap=1.2,
                       fmt_=lambda v: rf"{v:.1f} ms", font_size=20)
        ch.move_to([-2.8, -0.2, 0])
        lines = VGroup(
            label(r"tuple at a time: \ an interpreted loop, \\ one row per call, \ as Volcano's \texttt{next()} does",
                  font_size=20, color=NO),
            label(r"\textbf{vectorized}: \ each operator takes a column \\ of a thousand values at once \ "
                  r"(MonetDB/X100, \\ Boncz et al., 2005): \ tight loops, \ SIMD, \ few calls", font_size=20,
                  color=HEAD),
            label(rf"the column store also reads \\ {c['bytes_col'] // 10**6} MB instead of {c['bytes_row'] // 10**6} MB",
                  font_size=20, color=YES),
            label(r"or \textbf{compile} each query to machine code \\ (HyPer, \ Neumann, 2011): \ Part 13 at run time",
                  font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ch, RIGHT, buff=0.7)
        with self.voiceover(
            "We measured this, on a million rows of sixteen columns: add one column where another is under a hundred. "
            "<bookmark mark='a'/> Processing one tuple at a time, as an interpreter running the iterator model does, "
            "takes seventy-four milliseconds. <bookmark mark='b'/> Processing whole arrays of values per operation, "
            "which is called vectorized execution, on the row layout: fourteen milliseconds, because the loops are "
            "tight and the per-call overhead is paid once per thousand values, not once per row. "
            "<bookmark mark='c'/> And vectorized on the column layout: four milliseconds, because it moves sixteen "
            "megabytes instead of a hundred and twenty-eight. <bookmark mark='d'/> The other modern answer is to "
            "compile each query into machine code, as HyPer does: the compiler of Part 13, invoked for every query."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch.names))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(GrowFromEdge(ch.bars[k], DOWN), FadeIn(ch.vals[k]), FadeIn(lines[k]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def compression(self):
        c = load("columns")
        head = label(r"Columns compress", font_size=36).to_edge(UP, buff=0.3)
        runs = VGroup(*[Rectangle(width=w, height=0.45, stroke_width=0.8, stroke_color=GREY_D,
                                  fill_color=COLS[k % 6], fill_opacity=0.7)
                        for k, w in enumerate([0.9, 0.5, 0.7, 1.1, 0.4, 0.6, 0.8, 0.5, 0.9, 0.6, 0.7, 0.5,
                                               0.8, 0.6, 0.9])]).arrange(RIGHT, buff=0)
        runs.next_to(head, DOWN, buff=0.7)
        rl = label(r"\texttt{book\_id} of each of the Job's words, \ in table order: \ long runs", font_size=19,
                   color=WHITE).next_to(runs, UP, buff=0.15)
        lines = VGroup(
            label(rf"\textbf{{run-length}}: \ {num(c['book_rows'])} values are {c['book_runs']} runs: \ "
                  rf"{num(c['plain_bytes'] / 1e6)} MB become {c['rle_bytes']} bytes", font_size=20, color=YES),
            label(rf"\textbf{{dictionary}}: \ {num(c['vocab'])} distinct words, \ so each is a {c['dict_bits']}-bit "
                  rf"code: \ {c['raw_word_bytes'] / 1e6:.1f} MB become {c['dict_word_bytes'] / 1e6:.1f} MB",
                  font_size=20, color=HEAD),
            label(r"a column holds one type, \ often sorted or repetitive: \ it compresses far better than rows "
                  r"\ (Part 21's compression at work)", font_size=20, color=WHITE),
            label(r"and operators can run \textit{on the compressed data}: \ a sum over a run is value $\times$ length",
                  font_size=20, color=LAM),
            label(r"C-Store \ (Stonebraker et al., 2005) \ became Vertica; \ today: \ Parquet files, \ BigQuery, \ "
                  r"Snowflake, \ ClickHouse, \ DuckDB", font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(runs, DOWN, buff=0.6).set_x(0)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "Storing columns apart has a second payoff. <bookmark mark='a'/> The Job's words table records, for each "
            "word, which book it came from, and the rows are in book order, so that column is thirty long runs. "
            "Stored run by run, four point six million values, thirty-seven megabytes, become four hundred and eighty "
            "bytes. <bookmark mark='b'/> The word column has fifty-eight thousand distinct values, so each can be "
            "replaced by a sixteen-bit code into a dictionary, and twenty-four megabytes become under ten. "
            "<bookmark mark='c'/> A column holds values of one type, often sorted, often repeated, and so it has far "
            "less entropy than a row of mixed fields. <bookmark mark='d'/> Better still, operators can work on the "
            "compressed form directly: the sum of a run is its value times its length. <bookmark mark='e'/> Michael "
            "Stonebraker's C-Store showed all of this in 2005. Today almost every analytic system stores columns: "
            "Parquet files, BigQuery, Snowflake, ClickHouse, and DuckDB, which runs inside a program the way sqlite "
            "does."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(runs), FadeIn(rl), FadeIn(lines[0]))
            for mk, ln in zip("bcde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()


_ = (CODE,)
