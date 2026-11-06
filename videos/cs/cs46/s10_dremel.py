from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs46.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load,
                                   module_box, mono, tag_box)

Y_BOOK, Y_CH, Y_LEAF, Y_R, Y_D = 2.3, 1.3, 0.3, -0.5, -1.1
R_COL = {0: YES, 1: LAM, 2: KERN}           # repetition: a new record, a new chapter, the same chapter
D_COL = {0: NO, 1: HEAD, 2: YES}            # definition: nothing, a chapter without keywords, a keyword


def node(text, color, size=18):
    t = label(text, font_size=size, color=WHITE)
    r = RoundedRectangle(width=t.width + 0.3, height=0.45, corner_radius=0.08, stroke_color=color, stroke_width=2,
                         fill_color=BG, fill_opacity=1)
    return VGroup(r, t.move_to(r))


def null_slot():
    r = DashedVMobject(RoundedRectangle(width=0.9, height=0.45, corner_radius=0.08, stroke_color=GREY_B,
                                        stroke_width=1.5), num_dashes=24)
    return VGroup(r, label(r"null", font_size=16, color=GREY_B).move_to(r))


def slots_of(records):
    """The column's slots in order, one per (value, r, d) triple: a keyword, an empty chapter, or an empty book."""
    out = []
    for b, rec in enumerate(records):
        if not rec["chapters"]:
            out.append(("book", b, None, None))
            continue
        for c, ch in enumerate(rec["chapters"]):
            if not ch["keywords"]:
                out.append(("chapter", b, c, None))
            for kw in ch["keywords"]:
                out.append(("kw", b, c, kw))
    return out


def book_tree(records, nulls=True):
    """The three books drawn as a tree whose bottom row is the column's slots, left to right in column order."""
    slots = slots_of(records)
    n = len(slots)
    xs = [-5.0 + k * 10.0 / (n - 1) for k in range(n)]
    ch_x, bk_x = {}, {}
    for k, (kind, b, c, _) in enumerate(slots):
        if kind == "book":
            bk_x.setdefault(b, []).append(xs[k])
        else:
            ch_x.setdefault((b, c), []).append(xs[k])
    for (b, c), v in ch_x.items():
        bk_x.setdefault(b, []).append(sum(v) / len(v))
    books = {b: node(records[b]["title"], GREY_A).move_to([sum(v) / len(v), Y_BOOK, 0]) for b, v in bk_x.items()}
    chs = {(b, c): node(records[b]["chapters"][c]["name"], LAM).move_to([sum(v) / len(v), Y_CH, 0])
           for (b, c), v in ch_x.items()}
    leaves = VGroup()
    edges, null_edges, null_edge_of = VGroup(), VGroup(), {}
    for (b, c), m in chs.items():
        edges.add(Line(books[b].get_bottom(), m.get_top(), color=GREY_C, stroke_width=1.5))
    for k, (kind, b, c, kw) in enumerate(slots):
        if kind == "kw":
            leaf = tag_box(kw, DATA, size=16).move_to([xs[k], Y_LEAF, 0])
            edges.add(Line(chs[(b, c)].get_bottom(), leaf.get_top(), color=GREY_C, stroke_width=1.5))
        else:
            leaf = null_slot().move_to([xs[k], Y_LEAF, 0])
            top = (books[b] if kind == "book" else chs[(b, c)]).get_bottom()
            null_edge_of[k] = DashedLine(top, leaf.get_top(), color=GREY_B, stroke_width=1.2)
            null_edges.add(null_edge_of[k])
        leaves.add(leaf)
    g = VGroup(VGroup(*books.values()), VGroup(*chs.values()), edges, leaves, null_edges)
    g.books, g.chs, g.edges, g.leaves, g.null_edges, g.xs, g.slots = books, chs, edges, leaves, null_edges, xs, slots
    g.null_edge_of = null_edge_of
    g.kw = VGroup(*[leaves[k] for k, s in enumerate(slots) if s[0] == "kw"])
    g.nulls = VGroup(*[leaves[k] for k, s in enumerate(slots) if s[0] != "kw"])
    return g


def level_row(tr, levels, which, cmap, y):
    return VGroup(*[label(f"{t[which]}", font_size=26, color=cmap[t[which]]).move_to([tr.xs[k], y, 0])
                    for k, t in enumerate(levels)])


def show(recs):
    """A partial record as the reader holds it: lists of chapters, each a list of keywords."""
    return "[" + ", ".join("[" + ", ".join(ch) + "]" for ch in recs) + "]"


class Dremel(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.repetition()
        self.definition()
        self.assembly()
        self.payoff()

    def card(self):
        card = chapter_card(9, r"Nested data in columns", r"How can a tree be stored as flat columns, \ and come back?",
                            lit=(2010, 2013), extra=((2010, r"Melnik et al.: \ Dremel"),
                                                     (2013, r"Parquet")), part=PART)
        with self.voiceover("Chapter nine. Nested data in columns."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def problem(self):
        d = load("dremel")
        head = label(r"A tree in a column?", font_size=36).to_edge(UP, buff=0.3)
        tr = book_tree(d["records"])
        schema = code_block(["message Book {", "  required string title;", "  repeated group chapters {",
                             "    required string name;", "    repeated string keywords;", "  }", "}"], size=16)
        schema.to_edge(LEFT, buff=0.4).shift(UP * (-0.75 - schema.get_top()[1]))
        cap = label(r"the column \texttt{chapters.keywords}, \ flattened:", font_size=20, color=GREY_A)
        cap.move_to([2.0, -0.95, 0])
        flat = VGroup(*[tag_box(t[0], DATA, size=16) for t in d["levels"] if t[0] is not None]).arrange(
            RIGHT, buff=0.15).next_to(cap, DOWN, buff=0.25)
        qs = wrapped_label(r"which keywords shared a chapter? \ which chapter was in which book? \ and where did the "
                           r"empty chapter and the empty book go?", 7.2, font_size=20, color=NO).next_to(
            flat, DOWN, buff=0.3)
        with self.voiceover(
            "Real data is rarely flat: logs and documents are records nested inside records. Dremel, Google's "
            "interactive query engine, described by Sergey Melnik and colleagues in 2010, stored them in columns "
            "anyway. <bookmark mark='a'/> Here are three books, with repeated chapters, each with repeated keywords. "
            "One chapter has no keywords; one book has no chapters. <bookmark mark='b'/> The schema says which fields "
            "are required and which repeat. <bookmark mark='c'/> Take one column, chapters dot keywords, and write "
            "out its values: sea, whale, inn, Highbury. The structure is gone. Which keywords shared a chapter, or a "
            "book? And the empty chapter and the empty book have vanished. Two small numbers beside each value bring "
            "it all back."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tr[0]))
            vo.wait_until("a")
            self.play(Create(tr.edges), FadeIn(tr[1]), FadeIn(tr.kw))
            vo.wait_until("b")
            self.play(FadeIn(schema))
            vo.wait_until("c")
            self.play(FadeIn(cap), *[TransformFromCopy(a, b) for a, b in zip(tr.kw, flat)], run_time=1.5)
            self.play(FadeIn(qs))
        self.wait(0.4)
        self.clear_scene()

    def _frame(self, d):
        tr = book_tree(d["records"])
        names = VGroup(label(r"$r$", font_size=28, color=WHITE).move_to([-6.4, Y_R, 0]),
                       label(r"$d$", font_size=28, color=WHITE).move_to([-6.4, Y_D, 0]))
        return tr, names

    def repetition(self):
        d = load("dremel")
        lv = d["levels"]
        head = label(r"Repetition level: \ where does the value repeat?", font_size=36).to_edge(UP, buff=0.3)
        tr, names = self._frame(d)
        rr = level_row(tr, lv, 1, R_COL, Y_R)
        defs = VGroup(*[label(t, font_size=20, color=R_COL[k]) for k, t in (
            (0, r"$r = 0$: \ a new record"), (1, r"$r = 1$: \ a new chapter, \ same book"),
            (2, r"$r = 2$: \ another keyword, \ same chapter"))]).arrange(RIGHT, buff=0.6).move_to([0, -1.95, 0])
        mx = wrapped_label(rf"the path \texttt{{chapters.keywords}} has {d['max_r']} repeated fields, \ so $r$ runs "
                           rf"from 0 to {d['max_r']}; \ an empty list still takes a slot, \ as a null", 12.4,
                           font_size=20, color=GREY_A).to_edge(DOWN, buff=0.45)
        ring = SurroundingRectangle(tr.leaves[0], color=WHITE, buff=0.08)
        with self.voiceover(
            "The first number is the repetition level. <bookmark mark='a'/> For each value, in order, it says at "
            "which repeated field along the path this value repeats. Zero means a new record has begun. One means a "
            "new chapter, in the same book. Two means another keyword, in the same chapter. "
            "<bookmark mark='b'/> Walk the column. Sea starts the first book: zero. Whale follows it in the same "
            "chapter: two. Inn starts a new chapter: one. <bookmark mark='c'/> The empty chapter still needs a slot, "
            "a null with level one, and so does the book with no chapters, a null with level zero. Highbury starts a "
            "new book: zero. The path has two repeated fields, so the levels run from zero to two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tr[0]), FadeIn(tr[1]), Create(tr.edges), FadeIn(tr.kw), FadeIn(names[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in defs], lag_ratio=0.4), run_time=2)
            vo.wait_until("b")
            self.play(Create(ring))
            for k in range(3):
                self.play(Transform(ring, SurroundingRectangle(tr.leaves[k], color=WHITE, buff=0.08)), run_time=0.5)
                self.play(FadeIn(rr[k], shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("c")
            for k in range(3, len(lv)):
                if tr.slots[k][0] != "kw":
                    self.play(FadeIn(tr.leaves[k]), Create(tr.null_edge_of[k]), run_time=0.6)
                self.play(Transform(ring, SurroundingRectangle(tr.leaves[k], color=WHITE, buff=0.08)), run_time=0.5)
                self.play(FadeIn(rr[k], shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeOut(ring), FadeIn(mx))
        self.wait(0.4)
        self.clear_scene()

    def definition(self):
        d = load("dremel")
        lv = d["levels"]
        head = label(r"Definition level: \ how much of the path exists?", font_size=36).to_edge(UP, buff=0.3)
        tr, names = self._frame(d)
        rr = level_row(tr, lv, 1, R_COL, Y_R)
        dd = level_row(tr, lv, 2, D_COL, Y_D)
        defs = VGroup(*[label(t, font_size=20, color=D_COL[k]) for k, t in (
            (2, r"$d = 2$: \ chapter and keyword present"), (1, r"$d = 1$: \ a chapter, \ no keyword"),
            (0, r"$d = 0$: \ no chapter at all"))]).arrange(RIGHT, buff=0.6).move_to([0, -1.85, 0])
        tail = wrapped_label(r"a null is never stored as a value, \ only as a level below the maximum; \ a column of "
                             r"required fields needs no definition levels, \ and one outside any repeated field no "
                             r"repetition levels: \ flat tables pay nothing", 12.4, font_size=20,
                             color=GREY_A).to_edge(DOWN, buff=0.3)
        full = [k for k, t in enumerate(lv) if t[2] == d["max_d"]]
        part = [k for k in range(len(lv)) if k not in full]
        with self.voiceover(
            "The second number, the definition level, says how much of the path exists. <bookmark mark='a'/> Count "
            "the fields along chapters dot keywords, optional or repeated, that are really present. <bookmark "
            "mark='b'/> A real keyword has its chapter and itself: two, the maximum. <bookmark mark='c'/> The empty "
            "chapter exists but holds no keyword: one. The book without chapters has neither: zero. <bookmark "
            "mark='d'/> So a null is never stored as a value, only as a level below the maximum, which says exactly "
            "where the missing part begins. A column of required fields needs no definition levels, and one outside "
            "any repeated field no repetition levels, so flat tables pay nothing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tr), FadeIn(names), FadeIn(rr))
            vo.wait_until("a")
            self.play(FadeIn(defs))
            vo.wait_until("b")
            self.play(*[Indicate(tr.leaves[k], color=YES) for k in full])
            self.play(LaggedStart(*[FadeIn(dd[k], shift=DOWN * 0.15) for k in full], lag_ratio=0.2))
            vo.wait_until("c")
            for k in part:
                self.play(Indicate(tr.leaves[k], color=D_COL[lv[k][2]]), run_time=0.6)
                self.play(FadeIn(dd[k], shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("d")
            self.play(FadeIn(tail))
        self.wait(0.4)
        self.clear_scene()

    def assembly(self):
        d = load("dremel")
        lv = d["levels"]
        head = label(r"Rebuilding the records from the levels", font_size=36).to_edge(UP, buff=0.3)
        rows = [[t[0] if t[0] is not None else "null", f"{t[1]}", f"{t[2]}"] for t in lv]
        colors = [[DATA if t[0] is not None else GREY_B, R_COL[t[1]], D_COL[t[2]]] for t in lv]
        tab = grid_table([r"value", r"$r$", r"$d$"], rows, widths=[2.2, 1.0, 1.0], row_h=0.54, font_size=24,
                         colors=colors, mono_cols=())
        tab.to_edge(LEFT, buff=0.5).shift(UP * (2.35 - tab.get_top()[1]))
        # the reader's side, step by step (the same rule as explainer/cs/data/columnar.py's reassemble)
        states, recs = [], []
        for v, r, dl in lv:
            if r == 0:
                recs.append([])
            if dl > 0:
                if r <= 1:
                    recs[-1].append([])
                if dl == d["max_d"]:
                    recs[-1][-1].append(v)
            states.append([[list(ch) for ch in rec] for rec in recs])
        assert states[-1] == d["rebuilt"]
        n_rec = len(d["rebuilt"])
        ys = [1.9 - 0.9 * i for i in range(n_rec)]
        tags = VGroup(*[label(rf"record {i + 1}:", font_size=22, color=GREY_A).move_to([-1.4, y, 0])
                        for i, y in enumerate(ys)])

        def lines(st):
            return VGroup(*[mono(show(rec), size=20, color=WHITE).next_to(tags[i], RIGHT, buff=0.3)
                            for i, rec in enumerate(st)])
        rules = VGroup(*[label(t, font_size=21, color=c) for t, c in (
            (r"$r = 0$: \ start a new record", R_COL[0]),
            (r"$d = 0$: \ it has no chapters; \ next pair", D_COL[0]),
            (r"$r \le 1$: \ start a new chapter", R_COL[1]),
            (rf"$d = {d['max_d']}$: \ append the keyword", D_COL[2]))]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rules.move_to([2.6, -2.0, 0]).align_to(tags, LEFT)
        rbox = SurroundingRectangle(rules, color=GREY_C, buff=0.2, corner_radius=0.08)
        ok = wrapped_label(r"the three books, \ exactly as they were", 3.8, font_size=21, color=YES).next_to(
            tab, DOWN, buff=0.4).align_to(tab, LEFT)
        ptr = Rectangle(width=4.2, height=0.54, stroke_color=WHITE, stroke_width=2.5).move_to(
            [tab.rule.get_center()[0], tab.cells[1][0].get_y(), 0])
        shown = VGroup()
        with self.voiceover(
            "A reader rebuilds the records from the levels alone, without ever seeing the tree. "
            "<bookmark mark='a'/> Read the pairs in order. A repetition level of zero starts a new record. A "
            "definition level of zero means that record has no chapters, and we move on. Otherwise, a repetition "
            "level of one or less opens a new chapter, and a definition level of two appends a keyword to it. "
            "<bookmark mark='b'/> Six pairs later the three books are back, exactly: two keywords and then one in "
            "the first two chapters, an empty third chapter, an empty book, and Highbury. "
            "<bookmark mark='c'/> And because every column carries its own levels, a query can rebuild just the "
            "parts of the records it reads, and never touch the rest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(rbox), LaggedStart(*[FadeIn(x) for x in rules], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(Create(ptr))
            for k, st in enumerate(states):
                if k:
                    self.play(ptr.animate.move_to([ptr.get_x(), tab.cells[k + 1][0].get_y(), 0]), run_time=0.4)
                new = lines(st)
                anims = [FadeIn(tags[i]) for i in range(len(shown), len(new))]
                anims += [Transform(shown[i], new[i]) for i in range(len(shown))]
                anims += [FadeIn(new[i]) for i in range(len(shown), len(new))]
                self.play(*anims, run_time=0.6)
                shown.add(*[new[i] for i in range(len(shown), len(new))])
            self.play(FadeOut(ptr), FadeIn(ok), *[Indicate(x, color=YES) for x in shown])
            vo.wait_until("c")
            self.play(Indicate(tab, color=WHITE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def payoff(self):
        d = load("dremel")
        lv = d["levels"]
        head = label(r"Why it pays", font_size=36).to_edge(UP, buff=0.3)
        width = max(d["max_r"], d["max_d"]).bit_length()
        xs = [-2.6 + 0.85 * k for k in range(len(lv))]
        names = VGroup(*[label(t, font_size=19, color=c) for t, c in (
            (r"repetition levels", KERN), (r"definition levels", HEAD), (r"values", DATA))])
        ys = [2.1, 1.35, 0.6]
        for n, y in zip(names, ys):
            n.move_to([0, y, 0]).align_to([-6.6, 0, 0], LEFT)
        rbits = VGroup(*[tag_box(f"{t[1]:0{width}b}", KERN, size=16, w=0.7).move_to([x, ys[0], 0])
                         for t, x in zip(lv, xs)])
        dbits = VGroup(*[tag_box(f"{t[2]:0{width}b}", HEAD, size=16, w=0.7).move_to([x, ys[1], 0])
                         for t, x in zip(lv, xs)])
        vals = VGroup(*[tag_box(t[0], DATA, size=16) for t in lv if t[0] is not None]).arrange(RIGHT, buff=0.12)
        vals.move_to([0, ys[2], 0]).align_to(rbits, LEFT)
        page = SurroundingRectangle(VGroup(names, rbits, dbits, vals), color=GREY_C, buff=0.2, corner_radius=0.08)
        pcap = label(r"one data page of the column", font_size=16, color=GREY_B).next_to(page, DOWN, buff=0.08).align_to(
            page, LEFT)
        nvals = sum(1 for t in lv if t[0] is not None)
        notes = VGroup(
            wrapped_label(rf"levels are small integers, \ {width} bits each here, \ bit-packed and run-length coded "
                          r"like any column", 3.5, font_size=19, color=KERN),
            wrapped_label(rf"{len(lv)} slots, \ {nvals} values stored: \ a null costs only its levels", 3.5,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(page, RIGHT, buff=0.3)
        sys_ = VGroup(module_box(r"Dremel \ (2010)", KERN, w=3.4, h=0.6), module_box(r"Parquet \ (2013)", DATA, w=3.4,
                                                                                    h=0.6),
                      module_box(r"Apache Arrow, \ in memory", LAM, w=3.4, h=0.6)).arrange(RIGHT, buff=0.6)
        sys_.move_to([0, -1.55, 0])
        caps = VGroup(
            wrapped_label(r"aggregations over trillion-row tables in seconds \ (Melnik et al.); \ the engine behind "
                          r"BigQuery", 3.5, font_size=18, color=KERN),
            wrapped_label(r"the same repetition and definition levels, \ in every data page", 3.5, font_size=18,
                          color=DATA),
            wrapped_label(r"the same trees as offsets into child arrays, \ with bitmaps marking nulls", 3.5,
                          font_size=18, color=LAM))
        for c, b in zip(caps, sys_):
            c.next_to(b, DOWN, buff=0.2)
        with self.voiceover(
            "Why is this worth the trouble? <bookmark mark='a'/> The levels are tiny integers, two bits each here, "
            "bit-packed and run-length coded like any other column; in regular data they are nearly constant, and "
            "almost free. A missing value costs only its levels. In return, nested records get every benefit of "
            "columns: a query about keywords reads keywords and their levels, and nothing else. <bookmark mark='b'/> "
            "Dremel's paper reported aggregations over trillion-row tables in seconds, and the system became the "
            "engine behind Google's BigQuery. <bookmark mark='c'/> Parquet adopted the same levels, in every data "
            "page. In memory, Apache Arrow stores the same trees another way, as offsets into child arrays with "
            "bitmaps that mark the nulls."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(page), FadeIn(pcap), FadeIn(names), LaggedStart(*[FadeIn(b) for b in rbits],
                                                                                lag_ratio=0.1),
                      LaggedStart(*[FadeIn(b) for b in dbits], lag_ratio=0.1), FadeIn(vals), run_time=2)
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(sys_[0]), FadeIn(caps[0]))
            vo.wait_until("c")
            self.play(FadeIn(sys_[1]), FadeIn(caps[1]))
            self.play(FadeIn(sys_[2]), FadeIn(caps[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM, mono, YES)
