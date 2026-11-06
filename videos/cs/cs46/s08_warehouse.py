from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs46.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load,
                                   module_box, mono)


def table_card(title, fields, color, w=2.4):
    """A table drawn as a card: its name, then its columns (keys in the table's colour)."""
    t = label(title, font_size=20, color=color)
    fs = VGroup(*[mono(f, size=16, color=color if f.endswith("_key") else WHITE) for f in fields])
    fs.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    body = VGroup(t, fs).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    r = RoundedRectangle(width=max(w, body.width + 0.4), height=body.height + 0.32, corner_radius=0.1,
                         stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=1)
    body.move_to(r)
    g = VGroup(r, body)
    g.fields = fs
    return g


class Warehouse(VoiceoverScene):
    def construct(self):
        self.card()
        self.lambda_kappa()
        self.oltp_olap()
        self.star()
        self.star_join()
        self.scd()

    def card(self):
        card = chapter_card(7, r"The warehouse", r"How should data be laid out to answer questions about all of it?",
                            lit=(1993, 1996, 2014), extra=((1993, r"Codd: \ OLAP"),
                                                           (1996, r"Kimball: \ The Data Warehouse Toolkit"),
                                                           (2014, r"Kreps: \ Kappa")), part=PART)
        with self.voiceover("Chapter seven. The warehouse."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def lambda_kappa(self):
        head = label(r"Lambda against Kappa", font_size=36).to_edge(UP, buff=0.3)
        # Lambda: one log, two code paths, merged when queried
        t1 = label(r"Lambda \ (Marz, \ 2011)", font_size=22, color=HEAD).move_to([-5.0, 2.55, 0])
        log1 = module_box(r"the log", HEAD, w=1.6, h=0.6).move_to([-5.3, 1.5, 0])
        batch = module_box(r"batch job: \ recompute from all of it", DATA, w=3.9, h=0.55).move_to([-1.3, 2.0, 0])
        speed = module_box(r"stream job: \ only the recent part", LAM, w=3.9, h=0.55).move_to([-1.3, 1.0, 0])
        serve1 = module_box(r"merge at query time", YES, w=2.6, h=0.6).move_to([2.5, 1.5, 0])
        a1 = VGroup(*[Arrow(log1.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
                      for b in (batch, speed)],
                    *[Arrow(b.get_right(), serve1.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
                      for b in (batch, speed)])
        n1 = wrapped_label(r"every answer written twice, \ in two systems that must agree", 2.9, font_size=18,
                           color=NO).next_to(serve1, RIGHT, buff=0.25)
        # Kappa: one stream job; to change it, replay the log into a new version and switch
        t2 = label(r"Kappa \ (Kreps, \ 2014)", font_size=22, color=HEAD).move_to([-5.0, -0.45, 0])
        log2 = module_box(r"the log", HEAD, w=1.6, h=0.6).move_to([-5.3, -1.5, 0])
        v1 = module_box(r"stream job, \ version 1", DATA, w=3.9, h=0.55).move_to([-1.3, -1.0, 0])
        v2 = module_box(r"version 2, \ replaying from offset 0", YES, w=3.9, h=0.55).move_to([-1.3, -2.0, 0])
        serve2 = module_box(r"serving table", YES, w=2.6, h=0.6).move_to([2.5, -1.5, 0])
        a_in = VGroup(*[Arrow(log2.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
                        for b in (v1, v2)])
        a_old = Arrow(v1.get_right(), serve2.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
        a_new = Arrow(v2.get_right(), serve2.get_left(), buff=0.08, color=YES, stroke_width=3)
        n2 = wrapped_label(r"one code path; \ when version 2 catches up, \ readers switch to it", 2.9, font_size=18,
                           color=YES).next_to(serve2, RIGHT, buff=0.25)
        dot1 = Dot(log1.get_right(), radius=0.08, color=WHITE)
        dot2 = Dot(log2.get_right(), radius=0.08, color=WHITE)
        foot = wrapped_label(r"a batch is a bounded stream: \ with event-time windows and replay, \ streaming is a "
                             r"superset of batch \ (Akidau, \ 2015)", 12.4, font_size=21,
                             color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "First, an argument about architecture. <bookmark mark='a'/> In 2011 Nathan Marz "
            "proposed what became the Lambda architecture: recompute every answer from the whole log in a batch job, "
            "and, because the batch is hours behind, run a stream job alongside for the recent part, merging the two "
            "at query time. Every answer is written twice, in two systems that must agree. <bookmark mark='b'/> "
            "In 2014 Jay Kreps asked why not once. In his Kappa architecture there is only the stream job. To change "
            "it, start a second version reading the log from offset zero, let it catch up, and switch the readers "
            "over. <bookmark mark='c'/> A batch is just a bounded stream: with event-time windows and replay, as "
            "Tyler Akidau argued in 2015, streaming is a superset of batch."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(log1), FadeIn(batch), FadeIn(speed), FadeIn(serve1), GrowArrow(a1[0]),
                      GrowArrow(a1[1]), GrowArrow(a1[2]), GrowArrow(a1[3]))
            d1b = dot1.copy()
            self.add(dot1, d1b)
            self.play(MoveAlongPath(dot1, Line(log1.get_right(), batch.get_left())),
                      MoveAlongPath(d1b, Line(log1.get_right(), speed.get_left())), run_time=1)
            self.play(MoveAlongPath(dot1, Line(batch.get_right(), serve1.get_left())),
                      MoveAlongPath(d1b, Line(speed.get_right(), serve1.get_left())), run_time=1)
            self.play(FadeOut(dot1), FadeOut(d1b), FadeIn(n1))
            vo.wait_until("b")
            self.play(FadeIn(t2), FadeIn(log2), FadeIn(v1), GrowArrow(a_in[0]), FadeIn(serve2), GrowArrow(a_old))
            self.play(FadeIn(v2), GrowArrow(a_in[1]))
            self.add(dot2)
            self.play(MoveAlongPath(dot2, Line(log2.get_right(), v2.get_left())), run_time=1.5)
            self.play(FadeOut(dot2), FadeOut(a_old), GrowArrow(a_new), v1[0].animate.set_stroke(opacity=0.3).set_fill(opacity=0.03),
                      v1[1].animate.set_opacity(0.35), FadeIn(n2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def oltp_olap(self):
        head = label(r"OLTP against OLAP", font_size=36).to_edge(UP, buff=0.3)
        rows = [["1040", "Ann", "tea", "2", "4.20"], ["1041", "Bo", "rice", "1", "3.10"],
                ["1042", "Cy", "soap", "5", "9.50"], ["1043", "Ann", "rice", "2", "6.20"],
                ["1044", "Di", "tea", "1", "2.10"], ["1045", "Bo", "soap", "3", "5.70"],
                ["1046", "Cy", "tea", "4", "8.40"]]
        widths = [1.2, 1.4, 1.4, 1.0, 1.4]
        tab = grid_table([r"id", r"customer", r"product", r"qty", r"amount"], rows, widths=widths, row_h=0.42,
                         font_size=19, mono_cols=())
        tab.to_edge(LEFT, buff=0.5).shift(UP * (2.35 - tab.get_top()[1]))
        title = label(r"orders", font_size=20, color=GREY_A).next_to(tab, UP, buff=0.12).align_to(tab, LEFT)
        illus = note(r"illustrative", font_size=16).next_to(title, RIGHT, buff=0.3)
        x_mid = tab.rule.get_center()[0]
        r_hi = Rectangle(width=sum(widths), height=0.42, stroke_color=HEAD, stroke_width=3).move_to(
            [x_mid, tab.cells[3][0].get_y(), 0])
        top_y, bot_y = tab.cells[1][0].get_y() + 0.21, tab.cells[-1][0].get_y() - 0.21
        c_hi = VGroup(*[Rectangle(width=widths[c], height=top_y - bot_y, stroke_color=DATA, stroke_width=3,
                                  fill_color=DATA, fill_opacity=0.12).move_to([tab.cells[0][c].get_x(),
                                                                               (top_y + bot_y) / 2, 0])
                        for c in (2, 4)])
        q1 = mono("UPDATE orders SET qty = 3 WHERE id = 1042", size=16, color=HEAD)
        q2 = mono("SELECT product, SUM(amount) FROM orders", size=16, color=DATA)
        q2b = mono("GROUP BY product", size=16, color=DATA)
        qs = VGroup(q1, q2, q2b).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(tab, DOWN, buff=0.4)
        qs.align_to(tab, LEFT)
        notes = VGroup(
            wrapped_label(r"\textbf{OLTP}: \ many small transactions, \ each finding a few rows by key, \ reading "
                          r"and writing, \ in milliseconds", 5.2, font_size=20, color=HEAD),
            wrapped_label(r"\textbf{OLAP} \ (Codd, \ 1993): \ few large queries, \ each scanning a few columns of "
                          r"every row, \ reading only, \ in seconds", 5.2, font_size=20, color=DATA),
            wrapped_label(r"so the operational database keeps rows together \ (Part 35's B-trees), \ and a copy, "
                          r"\ loaded in batches or streamed from its change log \ (Chapter 3), \ goes to a warehouse "
                          r"built for scans", 5.2, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35).set_y(0.2)
        with self.voiceover(
            "A warehouse exists because two kinds of question want different machines. <bookmark mark='a'/> An "
            "operational database, built for online transaction processing, answers many small requests: fetch order "
            "ten forty-two, change its quantity, commit, in milliseconds, touching a few rows found by key. <bookmark "
            "mark='b'/> Analysis asks the opposite: total sales by product, over every order ever placed. Edgar Codd "
            "named it online analytical processing in 1993. Each query reads a couple of columns of every row, and "
            "writes nothing. <bookmark mark='c'/> On one database the long scans would starve the short transactions. "
            "So the operational system keeps its rows together, in Part 35's B-trees, and a copy of its data, loaded "
            "in batches or streamed from its change log, goes to a warehouse built for scans."
        ) as vo:
            self.play(FadeIn(head), FadeIn(title), FadeIn(illus), FadeIn(tab))
            vo.wait_until("a")
            self.play(Create(r_hi), FadeIn(q1), FadeIn(notes[0]))
            self.play(Indicate(tab.cells[3][3], color=HEAD, scale_factor=1.4))
            vo.wait_until("b")
            self.play(r_hi.animate.set_stroke(opacity=0.3), FadeIn(c_hi), FadeIn(q2), FadeIn(q2b), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def star(self):
        head = label(r"Facts and dimensions: \ the star schema", font_size=36).to_edge(UP, buff=0.3)
        fact = table_card(r"sales \ (fact)", ["date_key", "store_key", "product_key", "customer_key", "quantity",
                                               "amount"], HEAD, w=2.7).move_to([0, 0.05, 0])
        dims = {
            "date": table_card(r"date", ["date_key", "day", "month", "year"], DATA).move_to([-4.4, 1.25, 0]),
            "store": table_card(r"store", ["store_key", "city", "region", "size"], DATA).move_to([-4.4, -1.25, 0]),
            "product": table_card(r"product", ["product_key", "name", "category", "brand"], DATA).move_to(
                [4.4, 1.25, 0]),
            "customer": table_card(r"customer", ["customer_key", "name", "city", "segment"], DATA).move_to(
                [4.4, -1.25, 0]),
        }
        links = VGroup()
        for k, (name, d) in enumerate(dims.items()):
            f = fact.fields[k]
            left = d.get_x() < 0
            start = [fact.get_left()[0] if left else fact.get_right()[0], f.get_y(), 0]
            end = [d.get_right()[0] if left else d.get_left()[0], d.fields[0].get_y(), 0]
            links.add(Line(start, end, color=HEAD, stroke_width=2))
        notes = VGroup(
            wrapped_label(r"a \textbf{fact} is one business event: \ the numbers you add up, \ and keys; \ narrow, "
                          r"\ and billions of rows long", 12.4, font_size=20, color=HEAD),
            wrapped_label(r"a \textbf{dimension} describes who, \ what, \ where and when: \ wide, \ textual, \ and "
                          r"small \ (Kimball, \ \textit{The Data Warehouse Toolkit}, \ 1996)", 12.4, font_size=20,
                          color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Inside, the design Ralph Kimball set out in 1996 still dominates. <bookmark mark='a'/> At "
            "the centre is a fact table: one row per business event, here a sale, holding the numbers you add up, and "
            "keys. It is narrow, and billions of rows long. <bookmark mark='b'/> Around it are dimension tables, "
            "describing who, what, where and when: the date, the store, the product, the customer. They are wide and "
            "full of text, but small. <bookmark mark='c'/> Drawn out, the keys radiate from the centre like a star, "
            "which names the schema. Facts are what you measure; dimensions are what you filter and group by."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(fact), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in dims.values()], lag_ratio=0.3), FadeIn(notes[1]), run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(ln) for ln in links], lag_ratio=0.25), run_time=1.5)
            self.play(*[Indicate(f, color=HEAD) for f in fact.fields[:4]])
        self.wait(0.4)
        self.clear_scene()

    def star_join(self):
        head = label(r"Star joins, \ and snowflakes", font_size=36).to_edge(UP, buff=0.3)
        sql = code_block(["SELECT d.month, p.category,", "       SUM(s.amount)", "FROM sales s",
                          "JOIN date d ON s.date_key = d.date_key", "JOIN product p",
                          "  ON s.product_key = p.product_key", "WHERE d.year = 2025",
                          "GROUP BY d.month, p.category"], size=16)
        sql.to_edge(LEFT, buff=0.5).shift(UP * (2.6 - sql.get_top()[1]))
        # the plan: filter the small dimensions, hash them, stream the fact table past once
        hd = module_box(r"hash: \ date, \ year 2025", DATA, w=2.5, h=0.5).move_to([-5.2, -0.75, 0])
        hp = module_box(r"hash: \ product", DATA, w=2.5, h=0.5).move_to([-2.5, -0.75, 0])
        lane = Line([-6.4, -1.65, 0], [-0.6, -1.65, 0], color=HEAD, stroke_width=10, stroke_opacity=0.35)
        lane_l = label(r"sales: \ scanned once", font_size=18, color=HEAD).next_to(lane, DOWN, buff=0.12).align_to(
            lane, LEFT)
        probes = VGroup(*[DashedLine(b.get_bottom(), [b.get_x(), -1.55, 0], color=DATA, stroke_width=1.5)
                          for b in (hd, hp)])
        grp = module_box(r"group by", YES, w=1.3, h=0.5).next_to(lane, RIGHT, buff=0.1)
        dots = VGroup(*[Dot([-6.4 - 0.5 * i, -1.65, 0], radius=0.06, color=HEAD) for i in range(6)])
        plan_n = wrapped_label(r"Part 35's hash join; \ Chapter 11 spreads it over many machines", 6.0, font_size=18,
                               color=GREY_A).next_to(lane_l, DOWN, buff=0.2).align_to(lane, LEFT)
        illus = note(r"illustrative", font_size=16).next_to(sql, DOWN, buff=0.12).align_to(sql, LEFT)
        # the snowflake: the product dimension normalized into a chain
        sales = module_box(r"sales", HEAD, w=1.5, h=0.55).move_to([1.6, 0.6, 0])
        date = module_box(r"date", DATA, w=1.5, h=0.55).move_to([1.6, 2.0, 0])
        wide = module_box(r"product, \ category, \ department", DATA, w=3.6, h=0.55).move_to([4.6, 0.6, 0])
        prod = module_box(r"product", DATA, w=1.5, h=0.55).move_to([3.7, 0.6, 0])
        cat = module_box(r"category", LAM, w=1.5, h=0.55).move_to([5.8, 0.6, 0])
        dep = module_box(r"department", LAM, w=1.7, h=0.55).move_to([5.8, -0.7, 0])
        l_sd = Line(sales.get_top(), date.get_bottom(), color=GREY_B)
        l_sw = Line(sales.get_right(), wide.get_left(), color=GREY_B)
        l_sp = Line(sales.get_right(), prod.get_left(), color=GREY_B)
        l_pc = Line(prod.get_right(), cat.get_left(), color=LAM)
        l_cd = Line(cat.get_bottom(), dep.get_top(), color=LAM)
        snow_n = VGroup(
            wrapped_label(r"a \textbf{snowflake} normalizes the dimensions: \ less repetition, \ more joins", 5.6,
                          font_size=19, color=LAM),
            wrapped_label(r"dimensions are small, \ so the repetition rarely matters: \ most warehouses keep the "
                          r"simpler star", 5.6, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.95, -2.1, 0])
        with self.voiceover(
            "A typical question joins the facts to two dimensions: sales by month and category, for one year. "
            "<bookmark mark='a'/> The plan almost writes itself. Filter each small dimension and build a hash table "
            "from what survives, Part 35's hash join. Then stream the huge fact table past those tables once, keep "
            "the rows whose keys hit, and group them. Chapter 11 spreads exactly this over many machines. <bookmark "
            "mark='b'/> A snowflake schema normalizes the dimensions further: the product table points to a category "
            "table, which points to a department. Less repetition, more joins. <bookmark mark='c'/> But dimensions "
            "are small, so the repetition rarely matters, and most warehouses keep the simpler star."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sql), FadeIn(illus), FadeIn(sales), FadeIn(date), FadeIn(wide),
                      Create(l_sd), Create(l_sw))
            vo.wait_until("a")
            self.play(FadeIn(hd), FadeIn(hp), Create(lane), FadeIn(lane_l), FadeIn(grp))
            self.play(Create(probes), FadeIn(plan_n))
            self.add(dots)
            self.play(*[d.animate.shift(RIGHT * 6.5) for d in dots], run_time=2.5, rate_func=linear)
            self.remove(dots)
            vo.wait_until("b")
            self.play(FadeTransform(wide, VGroup(prod, cat)), ReplacementTransform(l_sw, l_sp))
            self.play(Create(l_pc), FadeIn(dep), Create(l_cd), FadeIn(snow_n[0]))
            vo.wait_until("c")
            self.play(FadeIn(snow_n[1]))
        self.wait(0.4)
        self.clear_scene()

    def scd(self):
        head = label(r"Slowly changing dimensions", font_size=36).to_edge(UP, buff=0.3)
        event = label(r"customer 17, \ Ann, \ moves from Leeds to York in 2024", font_size=22, color=HEAD)
        event.next_to(head, DOWN, buff=0.35)
        illus = note(r"illustrative", font_size=16).next_to(event, RIGHT, buff=0.3)
        t1 = grid_table([r"key", r"name", r"city"], [["17", "Ann", "Leeds"]], widths=[1.0, 1.2, 1.4], row_h=0.45,
                        font_size=20, mono_cols=())
        t2 = grid_table([r"key", r"name", r"city", r"from", r"to"],
                        [["17", "Ann", "Leeds", "2019", "2024"], ["42", "Ann", "York", "2024", ""]],
                        widths=[1.0, 1.1, 1.3, 1.1, 1.1], row_h=0.45, font_size=20, mono_cols=())
        t1.move_to([-4.4, 0.3, 0])
        t2.move_to([2.95, 0.55, 0]).align_to(t1, UP)
        h1 = label(r"type 1: \ overwrite", font_size=22, color=NO).next_to(t1, UP, buff=0.25)
        h2 = label(r"type 2: \ add a version", font_size=22, color=YES).next_to(t2, UP, buff=0.25)
        hidden = VGroup(t2.cells[1][4], *t2.cells[2])
        york = label(r"York", font_size=20, color=NO).move_to(t1.cells[1][2])
        f1 = wrapped_label(r"a 2021 sale, \ key 17: \ now reported in York; \ last year's report changes when "
                           r"run again", 5.0, font_size=19, color=NO).next_to(t1, DOWN, buff=0.45).align_to(t1, LEFT)
        f2 = VGroup(label(r"a 2021 sale, \ key 17: \ Leeds", font_size=19, color=YES),
                    label(r"a 2025 sale, \ key 42: \ York", font_size=19, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).next_to(t2, DOWN, buff=0.45).align_to(t2, LEFT)
        hi_old = Rectangle(width=5.6, height=0.45, stroke_color=YES, stroke_width=2).move_to(
            [t2.rule.get_center()[0], t2.cells[1][0].get_y(), 0])
        hi_new = hi_old.copy().move_to([t2.rule.get_center()[0], t2.cells[2][0].get_y(), 0])
        foot = wrapped_label(r"type 3 keeps a ``previous city'' column; \ type 2 turns the dimension into a log of "
                             r"versions, \ a table that can be asked what was true on any date \ (Chapter 10's time "
                             r"travel)", 12.4, font_size=20, color=WHITE)
        foot.next_to(VGroup(f1, f2), DOWN, buff=0.8).set_x(0)
        with self.voiceover(
            "Dimensions change, slowly. <bookmark mark='a'/> A customer, Ann, moves from Leeds to York. What should "
            "happen to her row? <bookmark mark='b'/> The simplest answer, Kimball's type one, overwrites the city. "
            "But then every sale she made in Leeds is now reported as a sale in York, and "
            "last year's report changes when it is run again. <bookmark mark='c'/> Type two keeps the history. The "
            "old row gets an end date, and a new row, with a new surrogate key, forty-two, begins. Each sale points "
            "to the version that was true when it happened. <bookmark mark='d'/> The dimension has become a log of "
            "versions, a table that can say what was true on any date, which is where Chapter 10's time travel "
            "begins."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(event), FadeIn(illus), FadeIn(h1), FadeIn(t1), FadeIn(h2),
                      FadeIn(VGroup(*[m for m in t2 if m not in hidden])))
            vo.wait_until("b")
            self.play(Transform(t1.cells[1][2], york))
            self.play(FadeIn(f1))
            vo.wait_until("c")
            self.play(FadeIn(t2.cells[1][4]))
            self.play(LaggedStart(*[FadeIn(c) for c in t2.cells[2]], lag_ratio=0.15))
            self.play(Create(hi_old), FadeIn(f2[0]))
            self.play(Create(hi_new), FadeIn(f2[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM, load)
