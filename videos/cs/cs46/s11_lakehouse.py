from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs46.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, code_block, grid_table, load,
                                   module_box, mono, tag_box, trace)


def link(a, b, color=GREY_B, width=2.0):
    """An arrow from the bottom of ``a`` to the top of ``b`` (a pointer in the table's tree)."""
    return Arrow(a.get_bottom(), b.get_top(), buff=0.05, stroke_width=width, color=color,
                 max_tip_length_to_length_ratio=0.2)


class Lakehouse(WatchScene):
    def construct(self):
        self.card()
        self.lake()
        self.snapshots()
        self.optimistic()
        self.timetravel()

    def card(self):
        self.chapter(10, r"Tables on object storage", r"Can a pile of files behave like a database table?", lit=(2018, 2020), extra=((2018, r"Apache Iceberg"),
                                                     (2020, r"Armbrust et al.: \ Delta Lake")), part=PART, said="Chapter ten. Tables on object storage.")

    def lake(self):
        head = label(r"A folder is not a table", font_size=36).to_edge(UP, buff=0.3)
        folder = RoundedRectangle(width=4.0, height=2.9, corner_radius=0.12, stroke_color=GREY_B,
                                  stroke_width=2).move_to([-4.4, 0.45, 0])
        path = mono("s3://lake/sales/", size=16, color=GREY_A).next_to(folder, UP, buff=0.12).align_to(folder, LEFT)
        files = VGroup(*[tag_box(f"part-{i}.parquet", DATA, size=16) for i in range(3)]).arrange(
            DOWN, buff=0.3).move_to(folder)
        writer = module_box(r"a job, \ writing", KERN, w=2.6, h=0.6).move_to([0.2, 1.45, 0])
        w_arr = Arrow(writer.get_left(), folder.get_right() + UP * 1.0, buff=0.1, stroke_width=2, color=KERN,
                      max_tip_length_to_length_ratio=0.12)
        reader = module_box(r"a reader: \ list, \ then read", LAM, w=2.6, h=0.6).move_to([0.2, -0.55, 0])
        r_arr = Arrow(folder.get_right() + DOWN * 1.0, reader.get_left(), buff=0.1, stroke_width=2, color=LAM,
                      max_tip_length_to_length_ratio=0.12)
        seen = VGroup(label(r"sees part-0 and part-1", font_size=19, color=NO),
                      label(r"two files of three: \ half a result, \ silently", font_size=19, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(reader, RIGHT, buff=0.35)
        lines = VGroup(
            wrapped_label(r"a job that crashes leaves its files behind; \ overwriting a partition means deleting, "
                          r"\ then writing, \ with a gap between", 12.4, font_size=20, color=NO),
            wrapped_label(r"each object is atomic, \ but nothing spans two objects \ (Part 45); \ and listing a "
                          r"million files takes a thousand requests, \ one page after another", 12.4, font_size=20,
                          color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A data lake is a folder of chapter eight's files in object storage. Is that a table? <bookmark "
            "mark='a'/> A job writes its output as three files. <bookmark mark='b'/> A reader that lists the folder "
            "halfway through sees two, and silently computes half an answer. <bookmark mark='c'/> A crashed job "
            "leaves its files behind, and overwriting means deleting, then writing. Part 45's object store makes "
            "each object atomic, but nothing spans two. And listing a million files takes a thousand requests, one "
            "after another."
        ) as vo:
            self.play(FadeIn(head), Create(folder), FadeIn(path))
            vo.wait_until("a")
            self.play(FadeIn(writer), GrowArrow(w_arr))
            self.play(FadeIn(files[0], shift=RIGHT * 0.2))
            self.play(FadeIn(files[1], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(reader), GrowArrow(r_arr))
            self.play(FadeIn(seen))
            self.play(FadeIn(files[2], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def snapshots(self):
        head = label(r"Snapshots and manifests", font_size=36).to_edge(UP, buff=0.3)
        xa, xb = -5.0, -1.8
        ys = [2.3, 1.3, 0.3, -0.7, -1.7]
        cat = tag_box("catalog: sales", HEAD, size=16).move_to([(xa + xb) / 2, ys[0], 0])
        meta1 = tag_box("v1.metadata.json", KERN, size=15).move_to([xa, ys[1], 0])
        meta2 = tag_box("v2.metadata.json", KERN, size=15).move_to([xb, ys[1], 0])
        list1 = tag_box("snap-1.avro", LAM, size=15).move_to([xa, ys[2], 0])
        list2 = tag_box("snap-2.avro", LAM, size=15).move_to([xb, ys[2], 0])
        man1 = tag_box("m1.avro", LAM, size=15).move_to([xa, ys[3], 0])
        man2 = tag_box("m2.avro", LAM, size=15).move_to([xb, ys[3], 0])
        d1 = tag_box("a.parquet", DATA, size=15).move_to([xa - 0.8, ys[4], 0])
        d2 = tag_box("b.parquet", DATA, size=15).move_to([xa + 0.8, ys[4], 0])
        d3 = tag_box("c.parquet", DATA, size=15).move_to([xb, ys[4], 0])
        levels = VGroup(*[label(t, font_size=16, color=GREY_B).move_to([0, y, 0]) for t, y in zip(
            (r"pointer", r"table metadata", r"manifest list", r"manifests", r"data files"), ys)])
        for lv in levels:
            lv.align_to([-0.45, 0, 0], LEFT)
        p_old = link(cat, meta1, color=HEAD, width=3)
        p_new = link(cat, meta2, color=HEAD, width=3)
        old = VGroup(link(meta1, list1), link(list1, man1), link(man1, d1), link(man1, d2))
        new = VGroup(link(man2, d3), link(list2, man2), link(list2, man1, color=YES), link(meta2, list2))
        hist = DashedLine(meta2.get_left(), meta1.get_right(), buff=0.06, color=GREY_C, stroke_width=1.5,
                          dash_length=0.07)
        hist_l = label(r"history", font_size=16, color=GREY_C).next_to(hist, UP, buff=0.06)
        notes = VGroup(
            wrapped_label(r"files never change: \ a commit writes new ones from the bottom up \ --- \ data, \ "
                          r"manifest, \ manifest list, \ metadata", 5.3, font_size=19, color=WHITE),
            wrapped_label(r"then swaps the catalog's pointer in one atomic step: \ readers see the whole commit "
                          r"or none of it \ (Part 35's commit record)", 5.3, font_size=19, color=YES),
            wrapped_label(r"snapshot 2 reuses manifest m1: \ a commit costs a few small files, \ never a copy of "
                          r"the table", 5.3, font_size=19, color=HEAD),
            wrapped_label(r"manifests give each file's partition and its columns' min and max: \ planning prunes "
                          r"files without listing a folder \ (Chapter 8)", 5.3, font_size=19, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([4.15, 0.2, 0])
        with self.voiceover(
            "Apache Iceberg, begun at Netflix, and Delta Lake, from Databricks, give the same answer: keep the list "
            "of files in files. <bookmark mark='a'/> In Iceberg a table is a tree: data files; manifests listing "
            "them; a manifest list for each snapshot; and a metadata file with the schema and history. A commit "
            "writes new files, bottom up, and changes none. <bookmark mark='b'/> Then it swaps one pointer in a "
            "catalog, from the old metadata file to the new. That one atomic step is the commit: readers see all of "
            "it or none. <bookmark mark='c'/> The new snapshot reuses the old manifest, so a commit costs a few "
            "small files. <bookmark mark='d'/> Manifests also record column ranges, so planners prune files without "
            "listing anything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(levels), FadeIn(cat), FadeIn(meta1), FadeIn(list1), FadeIn(man1),
                      FadeIn(d1), FadeIn(d2), Create(old), GrowArrow(p_old))
            vo.wait_until("a")
            for box, arr in ((d3, None), (man2, new[0]), (list2, VGroup(new[1], new[2])), (meta2, new[3])):
                self.play(FadeIn(box, shift=UP * 0.15), *([Create(arr)] if arr is not None else []), run_time=0.7)
            self.play(Create(hist), FadeIn(hist_l), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(ReplacementTransform(p_old, p_new), run_time=1.2)
            self.play(Indicate(meta2, color=YES, scale_factor=1.08), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Indicate(man1, color=YES, scale_factor=1.1), Indicate(new[2], color=YES), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(Indicate(VGroup(man1, man2), color=DATA, scale_factor=1.08), FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


    def optimistic(self):
        self.ask(r"Two jobs both read version 41 \\ and commit at once. Both succeed?", [r"yes",
                 r"one wins, one retries"], 1,
                 say="Two jobs read version forty-one of a table and try to commit at the same moment. Do both succeed?",
                 reveal="One wins version forty-two. The other checks for conflicts and retries.")
        head = label(r"Optimistic commits", font_size=36).to_edge(UP, buff=0.3)
        ya, yb = 1.7, 0.3
        lanes = VGroup(Line([-5.6, ya, 0], [6.6, ya, 0], color=GREY_D), Line([-5.6, yb, 0], [6.6, yb, 0],
                                                                           color=GREY_D))
        who = VGroup(label(r"job A", font_size=20, color=DATA).next_to([-5.6, ya, 0], LEFT, buff=0.15),
                     label(r"job B", font_size=20, color=LAM).next_to([-5.6, yb, 0], LEFT, buff=0.15))
        ra = tag_box("read v41", DATA, size=16).move_to([-4.6, ya, 0])
        rb = tag_box("read v41", LAM, size=16).move_to([-3.9, yb, 0])
        wa = Rectangle(width=2.4, height=0.3, stroke_width=0, fill_color=DATA, fill_opacity=0.5).next_to(
            ra, RIGHT, buff=0.15)
        wb = Rectangle(width=2.9, height=0.3, stroke_width=0, fill_color=LAM, fill_opacity=0.5).next_to(
            rb, RIGHT, buff=0.15)
        wl = VGroup(label(r"work", font_size=16, color=WHITE).move_to(wa),
                    label(r"work", font_size=16, color=WHITE).move_to(wb))
        ca = tag_box("create v42", YES, size=16).next_to(wa, RIGHT, buff=0.15)
        ok_a = label(r"wins", font_size=18, color=YES).next_to(ca, UP, buff=0.1)
        cb = tag_box("create v42", NO, size=16).next_to(wb, RIGHT, buff=0.15)
        taken = label(r"taken", font_size=18, color=NO).next_to(cb, DOWN, buff=0.1)
        check = tag_box("check v42", HEAD, size=16).next_to(cb, RIGHT, buff=0.2)
        cb2 = tag_box("create v43", YES, size=16).next_to(check, RIGHT, buff=0.2)
        ok_b = label(r"appends only: \ no conflict", font_size=18, color=YES).next_to(VGroup(check, cb2), DOWN,
                                                                                       buff=0.1)
        lines = VGroup(
            wrapped_label(r"no locks: \ each writer assumes it is alone and checks at commit, \ Kung and "
                          r"Robinson's optimistic control \ (Part 35)", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"the loser reads what the winner changed: \ if it touched nothing the loser read or "
                          r"rewrote, \ the loser retries with the next number, \ writing only a new log entry", 12.4,
                          font_size=20, color=YES),
            wrapped_label(r"if the winner rewrote files the loser read, \ the loser's work is stale and must be "
                          r"redone", 12.4, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Two jobs commit to the same table at once. <bookmark mark='a'/> Both read version forty-one and work "
            "without locks, checking only at commit: Kung and Robinson's optimistic control, from Part 35. <bookmark "
            "mark='b'/> Job A finishes first and creates version forty-two. Job B tries forty-two as well, and "
            "fails: the name is taken. <bookmark mark='c'/> B reads what A committed. If A touched nothing B read or "
            "rewrote, as when both only append, B retries as forty-three, writing just a new log entry. <bookmark "
            "mark='d'/> If A rewrote files that B read, B's work is stale and must be redone."
        ) as vo:
            self.play(FadeIn(head), Create(lanes), FadeIn(who))
            vo.wait_until("a")
            self.play(FadeIn(ra), FadeIn(rb))
            self.play(GrowFromEdge(wa, LEFT), GrowFromEdge(wb, LEFT), FadeIn(wl), run_time=1.5)
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(ca), FadeIn(ok_a))
            self.play(FadeIn(cb), FadeIn(taken))
            vo.wait_until("c")
            self.play(FadeIn(check))
            self.play(FadeIn(cb2), FadeIn(ok_b), FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()


    def timetravel(self):
        head = label(r"Time travel", font_size=36).to_edge(UP, buff=0.3)
        y = 0.55
        xs = [-5.0 + 2.0 * k for k in range(5)]
        strip = Line([-6.0, y, 0], [6.4, y, 0], color=GREY_D, stroke_width=2)
        dots = VGroup(*[Dot([x, y, 0], radius=0.12, color=DATA) for x in xs])
        names = VGroup(*[label(f"v{38 + k}", font_size=18, color=GREY_A).next_to(d, DOWN, buff=0.15)
                         for k, d in enumerate(dots)])
        cur = label(r"current", font_size=18, color=HEAD)
        cur_arr = Arrow(UP * 0.55, ORIGIN, buff=0, stroke_width=3, color=HEAD, max_tip_length_to_length_ratio=0.35)
        pointer = VGroup(cur, cur_arr).arrange(DOWN, buff=0.05).next_to(dots[4], UP, buff=0.08)
        q = code_block(["SELECT * FROM sales VERSION AS OF 40",
                        "SELECT * FROM sales TIMESTAMP AS OF '2025-03-01'"], size=16, color=LAM)
        q.move_to([-1.5, 2.3, 0])
        q_arr = Arrow(q.get_bottom() + LEFT * 0.3, dots[2].get_top(), buff=0.12, stroke_width=2, color=LAM,
                      max_tip_length_to_length_ratio=0.12)
        hit = Circle(radius=0.25, color=LAM, stroke_width=3).move_to(dots[2])
        v43 = Dot([6.0, y, 0], radius=0.12, color=YES)
        v43_l = label(r"v43", font_size=18, color=GREY_A).next_to(v43, DOWN, buff=0.15)
        rest = mono("RESTORE TABLE sales TO VERSION AS OF 40", size=16, color=YES)
        rest.move_to([(xs[2] + 6.0) / 2, y - 1.55, 0])
        rest_arr = CurvedArrow(dots[2].get_bottom() + DOWN * 0.45, v43.get_bottom() + DOWN * 0.45, angle=0.4,
                               color=YES, stroke_width=2, tip_length=0.15)
        ret = Brace(VGroup(dots[0], dots[1]), DOWN, buff=0.55, color=GREY_B)
        ret_l = label(r"past the retention period: \ vacuum deletes files only these need", font_size=18,
                      color=GREY_B).next_to(ret, DOWN, buff=0.1).align_to(ret, LEFT)
        lines = VGroup(
            wrapped_label(r"audits, \ reproducible training sets, \ debugging: \ what did the table say then? \ "
                          r"(Chapter 7's type-2 history, \ for a whole table)", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"Armbrust et al. \ (2021): \ the \textbf{lakehouse}, \ a warehouse's guarantees over "
                          r"open files on cheap object storage", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Because commits never change old files, every old version is still there. <bookmark mark='a'/> In Spark "
            "SQL, either format can be read as of a version or a timestamp, starting from an older snapshot. "
            "<bookmark mark='b'/> A bad write is undone by restoring an earlier version, itself a new commit. Audits "
            "can ask what a report saw last March, and models can retrain on the data they first saw. <bookmark "
            "mark='c'/> A vacuum later deletes the files that no recent snapshot needs. <bookmark mark='d'/> "
            "Armbrust and colleagues named the result in 2021: a lakehouse, a warehouse's guarantees over open files "
            "on cheap storage."
        ) as vo:
            self.play(FadeIn(head), Create(strip), FadeIn(dots), FadeIn(names), FadeIn(pointer))
            vo.wait_until("a")
            self.play(FadeIn(q))
            self.play(GrowArrow(q_arr), Create(hit))
            vo.wait_until("b")
            self.play(FadeIn(rest), Create(rest_arr))
            self.play(FadeIn(v43), FadeIn(v43_l), pointer.animate.next_to(v43, UP, buff=0.08))
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeOut(rest), FadeOut(rest_arr))
            self.play(GrowFromCenter(ret), FadeIn(ret_l), dots[0].animate.set_color(GREY_D),
                      dots[1].animate.set_color(GREY_D))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM)
