from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (CODE, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono, num)


class OurDb(VoiceoverScene):
    def construct(self):
        self.card()
        self.plans()
        self.sqlite()
        self.ledger()
        self.beyond()

    def card(self):
        card = chapter_card(15, r"Our database runs the Job", r"What did it choose, \ and was it right?",
                            lit=(2000,), extra=((2000, r"Hipp: \ SQLite"),), part=PART)
        with self.voiceover("Chapter fifteen. Our database runs the Job."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def plans(self):
        j = load("job")
        head = label(r"Two correct plans, \ costed", font_size=36).to_edge(UP, buff=0.3)
        sql = mono(j["sql"], 17, YES).next_to(head, DOWN, buff=0.35)
        groups = VGroup()
        for name, c in (("hash aggregate", YES), ("sort aggregate", NO)):
            p = j["plans"][name]
            ex = VGroup(*[mono(ln, 14, CODE) for ln in p["explain"].splitlines()]).arrange(DOWN, aligned_edge=LEFT,
                                                                                           buff=0.05)
            g = VGroup(label(rf"\textbf{{{name}}}: \ estimated {num(p['cost'])} page I/Os", font_size=20, color=c), ex)
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            groups.add(g)
        groups.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(sql, DOWN, buff=0.45).set_x(0)
        for g in groups:
            if g.width > 12.8:
                g.width = 12.8
        lines = VGroup(
            label(r"the hash table of 57{,}895 words fits in memory, \ so one pass over 46{,}100 pages suffices",
                  font_size=19, color=YES),
            label(r"sorting 4.6 million rows needs an external sort: \ read, \ write runs, \ merge: \ five times the "
                  r"I/O", font_size=19, color=NO),
            label(r"Parts 16 and 17 in one decision: \ the optimizer picked Part 17's hash table over Part 16's sort",
                  font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Back to the Job. Our database considered two ways to group the words. <bookmark mark='a'/> Hash "
            "aggregation: keep a hash table of counts, one entry per distinct word. Fifty-eight thousand entries fit in "
            "memory, so it reads the table once: forty-six thousand pages. <bookmark mark='b'/> Sort aggregation: sort "
            "all four point six million rows by word, so equal words are adjacent, and count the runs. The rows do "
            "not fit in memory, so the sort writes runs to disk and merges them: five times the page traffic. "
            "<bookmark mark='c'/> So it chose hashing. Part 16 sorted the words and Part 17 replaced the sort with a "
            "hash table and was six times faster. The optimizer made the same decision from its cost model, without "
            "being told."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sql))
            vo.wait_until("a")
            self.play(FadeIn(groups[0]), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(groups[1]), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def sqlite(self):
        j = load("job")
        head = label(r"Cross-checked against sqlite3", font_size=36).to_edge(UP, buff=0.3)
        pl = VGroup(label(r"sqlite's plan \ (\texttt{EXPLAIN QUERY PLAN})", font_size=19, color=HEAD),
                    *[mono(s, 16, CODE) for s in j["sqlite_plan"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        pi = VGroup(label(r"after \texttt{CREATE INDEX words\_word}", font_size=19, color=YES),
                    *[mono(s, 16, CODE) for s in j["sqlite_plan_indexed"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        VGroup(pl, pi).arrange(RIGHT, buff=0.9, aligned_edge=UP).next_to(head, DOWN, buff=0.45)
        rows = [[r"our engine \ (Python)", rf"{j['ours_seconds']:.1f} s", r"hash aggregate, \ top-20 heap"],
                [r"sqlite3 \ (C), \ no index", rf"{j['sqlite_seconds']:.2f} s", r"a temporary B-tree keyed by word"],
                [r"sqlite3, \ with the index", rf"{j['sqlite_indexed_seconds']:.2f} s",
                 r"read the index in order: \ groups are adjacent"],
                [r"loading 4.6 million rows into sqlite", rf"{j['load_seconds']:.1f} s", r"paid once"]]
        tab = grid_table([r"", r"time", r"how"], rows, widths=[4.4, 1.6, 5.6], row_h=0.44, font_size=19,
                         mono_cols=())
        tab.next_to(VGroup(pl, pi), DOWN, buff=0.5).set_x(0)
        for r in range(1, 5):
            tab.cells[r][1].set_color(YES)
        lines = VGroup(
            label(r"all three give exactly the twenty words and counts of Part 17's program", font_size=19,
                  color=WHITE),
            label(r"sqlite groups with a B-tree rather than a hash table, \ and with an index it needs no grouping "
                  r"structure at all: \ a covering index scan", font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "We check our database against sqlite, the most widely deployed database in the world, which ships "
            "inside every phone and every browser. <bookmark mark='a'/> Its plan: scan the words, and group them in "
            "a temporary B-tree, a sort by another name. <bookmark mark='b'/> Our engine, written in Python, takes "
            "seven seconds. Sqlite, in C, takes two and a quarter. <bookmark mark='c'/> Give sqlite an index on the "
            "word column and it changes plan by itself: the index holds the words already in order, so it reads the "
            "index alone, counting runs, in a quarter of a second. The query did not change. "
            "<bookmark mark='d'/> Every one of these gives the same twenty words with the same counts as Part 17's "
            "hand-written program."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]), FadeIn(tab.cells[0][2]), FadeIn(tab.rule),
                      *[FadeIn(c) for c in tab.cells[1] + tab.cells[2]])
            vo.wait_until("c")
            self.play(FadeIn(pi), *[FadeIn(c) for c in tab.cells[3] + tab.cells[4]], FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]))
        self.wait(0.3)
        self.clear_scene()

    def ledger(self):
        j = load("job")
        led = j["ledger"]
        row = led[-1]
        head = label(r"Ledger row 13", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=20, row_h=0.3,
                           label_width=4.8).scale(0.9).move_to(UP * 0.95)
        notes = VGroup(
            label(rf"one line of SQL, \ run by sqlite3 on this machine: \ {row['seconds']:.2f} s, \ with no "
                  r"instruction about how", font_size=20, color=HEAD),
            label(rf"row 11, \ Part 24's hand-engineered C: \ {led[10]['seconds'] * 1000:.0f} ms: \ thirty times "
                  r"faster, \ and it took a part to write", font_size=19, color=GREY_A),
            label(rf"with an index, \ {row['indexed_seconds']:.2f} s; \ and the same line answers questions the "
                  r"program never could", font_size=19, color=YES),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The ledger gets row thirteen. <bookmark mark='a'/> One line of SQL, answered by sqlite on this machine "
            "in two and a quarter seconds, and we never said how. <bookmark mark='b'/> That is slower than Part 24's "
            "engineered C, by about thirty times, and that program took a whole part to write. "
            "<bookmark mark='c'/> With an index it is a quarter of a second. And the same database answers the whale "
            "question, or any other, with one more line and no new program. That trade, some speed for never having "
            "to say how, is Codd's bargain, and the world took it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            vo.wait_until("a")
            self.play(FadeIn(tab.rows[-1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def beyond(self):
        head = label(r"Beyond relational", font_size=36).to_edge(UP, buff=0.3)
        kinds = [
            (r"key-value", r"get and put by key; \ Dynamo \ (2007), \ Redis, \ RocksDB", DATA),
            (r"document", r"nested records, \ JSON; \ MongoDB; \ now also a column type in PostgreSQL", HEAD),
            (r"graph", r"nodes and edges, \ queries by path; \ Neo4j; \ SQL:2023 added property graphs", LAM),
            (r"distributed SQL", r"transactions across machines: \ Spanner, \ CockroachDB \ (Part 39)", KERN),
        ]
        cards = VGroup()
        for t, d, c in kinds:
            g = VGroup(label(rf"\textbf{{{t}}}", font_size=22, color=c), label(d, font_size=18, color=WHITE)).arrange(
                DOWN, buff=0.12)
            fr = SurroundingRectangle(g, buff=0.2, color=c, stroke_width=1.5, corner_radius=0.08)
            fr.stretch_to_fit_width(6.1)
            fr.stretch_to_fit_height(1.4)
            fr.move_to(g)
            cards.add(VGroup(fr, g))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.3)).next_to(head, DOWN, buff=0.45)
        lines = VGroup(
            label(r"each began by giving up the relational model for speed or scale; \ most have since added SQL "
                  r"and transactions back", font_size=19, color=WHITE),
            label(r"Stonebraker and Pavlo \ (2024): \ ``what goes around comes around'': \ fifty years on, \ the "
                  r"relational model and SQL still win", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(cards, DOWN, buff=0.45)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        lines.set_x(0)
        with self.voiceover(
            "Not every store is relational. <bookmark mark='a'/> Key-value stores, like Amazon's Dynamo, give up "
            "queries for scale: get and put by key, and nothing else. <bookmark mark='b'/> Document stores keep nested "
            "records. <bookmark mark='c'/> Graph databases query by path. <bookmark mark='d'/> And distributed SQL "
            "systems, like Google's Spanner, keep transactions across many machines, which Part 39 explains. "
            "<bookmark mark='e'/> Each new kind began by dropping Codd's model for speed or scale, and most have "
            "since added SQL and transactions back. Michael Stonebraker and Andy Pavlo reviewed fifty years of this "
            "in 2024, and their title says it: what goes around comes around."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(lines))
        self.wait(0.3)
        self.clear_scene()


_ = (DATA, NO)
