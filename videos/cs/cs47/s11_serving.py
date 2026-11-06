from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, load, mono, module_box,
                                   tag_box)

# the stems drawn as rows of the term-by-passage picture; the dots in it are illustrative
ROWS = ["whale", "sea", "captain", "ahab", "love", "darci", "holm", "moor"]
SHARD_COLORS = [DATA, LAM, YES, KERN]


class Serving(VoiceoverScene):
    def construct(self):
        self.card()
        self.cuts()
        self.query()
        self.tail()
        self.replicas()
        self.caches()

    def card(self):
        card = chapter_card(10, r"Serving at scale", r"How do a thousand machines answer one query?",
                            lit=(2003, 2013), extra=((2003, r"Barroso, \ Dean and H\"olzle: \ a cluster for search"),
                                                     (2013, r"Dean and Barroso: \ the tail at scale")), part=PART)
        with self.voiceover("Chapter ten. Serving at scale."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cuts(self):
        ix = load("index")
        head = label(r"Two ways to cut an index", font_size=36).to_edge(UP, buff=0.3)
        cell, rh = 0.36, 0.48
        ncol = 16
        x0, y0 = -5.4, 2.2
        rng = random.Random(7)
        frame = Rectangle(width=ncol * cell, height=len(ROWS) * rh, stroke_color=GREY_C, stroke_width=1.5)
        frame.move_to([x0 + ncol * cell / 2, y0 - len(ROWS) * rh / 2, 0])
        dots = VGroup(*[Dot([x0 + (j + 0.5) * cell, y0 - (i + 0.5) * rh, 0], radius=0.07, color=GREY_A)
                        for i in range(len(ROWS)) for j in range(ncol) if rng.random() < 0.38])
        names = VGroup(*[mono(t, size=17, color=GREY_A).move_to([x0 - 0.1, y0 - (i + 0.5) * rh, 0], aligned_edge=RIGHT)
                         for i, t in enumerate(ROWS)])
        top = label(r"passages $\rightarrow$", font_size=17, color=GREY_B).next_to(frame, UP, buff=0.1)
        ill = label(r"illustrative pattern", font_size=16, color=GREY_B).next_to(frame, DOWN, buff=0.15)
        bands_d = VGroup()
        for k in range(4):
            r = Rectangle(width=4 * cell, height=len(ROWS) * rh, stroke_width=0, fill_color=SHARD_COLORS[k],
                          fill_opacity=0.28).move_to([x0 + (4 * k + 2) * cell, frame.get_y(), 0])
            t = label(rf"shard {k + 1}", font_size=16, color=SHARD_COLORS[k]).next_to(r, DOWN, buff=0.55)
            bands_d.add(VGroup(r, t))
        bands_t = VGroup()
        for k in range(4):
            r = Rectangle(width=ncol * cell, height=2 * rh, stroke_width=0, fill_color=SHARD_COLORS[k],
                          fill_opacity=0.28).move_to([frame.get_x(), y0 - (2 * k + 1) * rh, 0])
            t = label(rf"server {k + 1}", font_size=16, color=SHARD_COLORS[k]).next_to(r, RIGHT, buff=0.12)
            bands_t.add(VGroup(r, t))
        notes = VGroup(
            wrapped_label(rf"our index is a sparse matrix: \ {ix['terms']:,} terms by {ix['docs']:,} passages, \ "
                          rf"with {ix['postings']:,} postings", 4.8, font_size=19, color=WHITE),
            wrapped_label(r"\textbf{document-partitioned}: \ each shard indexes a slice of the passages, \ with "
                          r"every term", 4.8, font_size=19, color=DATA),
            wrapped_label(r"\textbf{term-partitioned}: \ each server holds whole postings lists, \ for a slice of "
                          r"the vocabulary", 4.8, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.35, 0.3, 0])
        with self.voiceover(
            "One machine cannot hold the web's index, or answer the world's queries, so the index must be cut "
            "into pieces. <bookmark mark='a'/> Picture it as a matrix: a row for each term, a column for each "
            f"passage, a dot for each posting. Ours has {ix['terms']:,} rows and {ix['docs']:,} columns, and "
            "it is almost empty. <bookmark mark='b'/> Cut it by columns and each shard is a complete little index "
            "for a slice of the passages: document partitioning. <bookmark mark='c'/> Cut it by rows and each "
            "server holds the whole postings list of some terms: term partitioning. The matrix is the same; what "
            "differs is the work a query causes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(frame), FadeIn(names), FadeIn(top), FadeIn(ill),
                      LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01), FadeIn(notes[0]), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bands_d], lag_ratio=0.3), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeOut(bands_d))
            self.play(LaggedStart(*[FadeIn(b) for b in bands_t], lag_ratio=0.3), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def query(self):
        row = next(r for r in load("intersect")["rows"] if r["terms"] == ["whale", "sea"])
        n_whale, n_sea = row["sizes"]
        head = label(r"One query, \ two layouts", font_size=36).to_edge(UP, buff=0.3)
        div = DashedLine([0, 2.7, 0], [0, -3.6, 0], color=GREY_D)
        # left: document-partitioned
        lt = label(r"document-partitioned", font_size=22, color=DATA).move_to([-3.45, 2.65, 0])
        broker = module_box(r"broker", HEAD, w=2.2, h=0.55).move_to([-3.45, 1.85, 0])
        shards = VGroup(*[module_box(rf"shard {k + 1}", SHARD_COLORS[k], w=1.35, h=0.55)
                          for k in range(4)]).arrange(RIGHT, buff=0.22).move_to([-3.45, 0.15, 0])
        down = VGroup(*[Line(broker.get_bottom(), s.get_top(), color=GREY_C, stroke_width=1.5) for s in shards])
        qdots = VGroup(*[Dot(broker.get_bottom(), radius=0.07, color=HEAD) for _ in shards])
        tens = VGroup(*[tag_box(r"top 10", color=SHARD_COLORS[k], size=13, h=0.34).move_to(s.get_top() + UP * 0.25)
                        for k, s in enumerate(shards)])
        merged = label(r"merge: \ $4 \times 10 \rightarrow 10$", font_size=18, color=HEAD)
        merged.next_to(broker, RIGHT, buff=0.15)
        lnote = wrapped_label(r"every shard works on every query, \ but on a quarter of the data; \ the scores need "
                              r"global statistics \ (the idf of Chapter 5), \ shared among the shards", 6.2,
                              font_size=19, color=WHITE).move_to([-3.45, -1.75, 0])
        # right: term-partitioned
        rt = label(r"term-partitioned", font_size=22, color=LAM).move_to([3.45, 2.65, 0])
        broker2 = module_box(r"broker", HEAD, w=2.2, h=0.55).move_to([3.45, 1.85, 0])
        sw = module_box(rf"\texttt{{whale}}: \ {n_whale} postings", LAM, w=2.7, h=0.6).move_to([1.95, 0.15, 0])
        ss = module_box(rf"\texttt{{sea}}: \ {n_sea} postings", KERN, w=2.7, h=0.6).move_to([4.95, 0.15, 0])
        down2 = VGroup(Line(broker2.get_bottom(), sw.get_top(), color=GREY_C, stroke_width=1.5),
                       Line(broker2.get_bottom(), ss.get_top(), color=GREY_C, stroke_width=1.5))
        packets = VGroup(*[Rectangle(width=0.06, height=0.3, stroke_width=0, fill_color=LAM, fill_opacity=0.9)
                           for _ in range(14)]).arrange(RIGHT, buff=0.04).next_to(sw, DOWN, buff=0.2)
        hits = label(rf"{row['hits']} passages contain both", font_size=18, color=YES).next_to(ss, DOWN, buff=0.25)
        rnote = wrapped_label(rf"only the servers of the query's terms work, \ but a whole list of {n_whale} postings "
                              r"crosses the network, \ and the servers of common terms become hot spots", 6.2,
                              font_size=19, color=WHITE).move_to([3.45, -1.75, 0])
        foot = wrapped_label(r"web engines partition by document \ (Barroso, \ Dean and H\"olzle, \ 2003): \ "
                             r"balanced load, \ and a lost shard loses a few pages, \ not a word", 12.4, font_size=19,
                             color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Follow the query whale sea through each layout. <bookmark mark='a'/> With documents partitioned, the "
            "broker sends the whole query to every shard. Each computes its own top ten over its quarter of the "
            "passages, and the broker merges four short lists. The scores need collection-wide statistics, such "
            "as idf, shared among the shards. <bookmark mark='b'/> With terms "
            "partitioned, only the two servers holding those terms work, but one must ship its entire list, "
            f"{n_whale} postings, to the other, which intersects them and finds {row['hits']} passages. "
            "<bookmark mark='c'/> Web engines chose documents: Google's cluster, "
            "described by Barroso, Dean and Hoelzle in 2003, cut its index into shards of documents."
        ) as vo:
            self.play(FadeIn(head), Create(div), FadeIn(lt), FadeIn(rt), FadeIn(broker), FadeIn(shards),
                      FadeIn(broker2), FadeIn(sw), FadeIn(ss))
            vo.wait_until("a")
            self.play(Create(down), FadeIn(qdots))
            self.play(*[d.animate.move_to(s.get_top()) for d, s in zip(qdots, shards)], run_time=1.0)
            self.play(FadeOut(qdots), FadeIn(tens))
            self.play(*[t.animate.move_to(broker.get_bottom() + DOWN * 0.3 + RIGHT * (k - 1.5) * 0.25).set_opacity(0)
                        for k, t in enumerate(tens)], run_time=1.2)
            self.play(FadeIn(merged), FadeIn(lnote))
            vo.wait_until("b")
            self.play(Create(down2))
            self.play(FadeIn(packets))
            self.play(packets.animate.next_to(ss, DOWN, buff=0.2).set_x(ss.get_x()), run_time=1.5)
            self.play(FadeOut(packets), FadeIn(hits), FadeIn(rnote))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def tail(self):
        head = label(r"Fan-out and the tail", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 100, 20], [0, 1, 0.25], x_length=6.0, y_length=3.8, xticks=[0, 20, 40, 60, 80, 100],
                 yticks=[0, 0.25, 0.5, 0.75, 1.0], fy=lambda v: f"{100 * v:.0f}\\%",
                 x_label=r"servers a query must wait for",
                 y_label=r"share of queries slower than one second")
        g.move_to([-3.1, -0.35, 0])
        ax = g.ax
        curve = ax.plot(lambda n: 1 - 0.99 ** n, x_range=[0, 100], color=NO, stroke_width=3)
        n = ValueTracker(1)
        dot = always_redraw(lambda: Dot(ax.c2p(n.get_value(), 1 - 0.99 ** n.get_value()), radius=0.08, color=HEAD))
        read = always_redraw(lambda: label(rf"{n.get_value():.0f} servers: \ "
                                           rf"{100 * (1 - 0.99 ** n.get_value()):.0f}\% slow", font_size=20,
                                           color=HEAD).move_to(ax.c2p(4, 0.92), aligned_edge=LEFT))
        notes = VGroup(
            wrapped_label(r"each server is slow once in a hundred requests; \ a query is as slow as its slowest "
                          r"shard: \ $1 - 0.99^{n}$", 5.0, font_size=19, color=WHITE),
            wrapped_label(r"\textbf{hedged requests}: \ after a short delay, \ send a second copy to another "
                          r"replica and take the first answer; \ in Dean and Barroso's BigTable test the 99.9th "
                          r"percentile fell from 1{,}800 ms to 74 ms, \ for 2\% more requests", 5.0, font_size=19,
                          color=YES),
            wrapped_label(r"or answer without the stragglers: \ a slightly worse page now beats a perfect one "
                          r"late", 5.0, font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.15, -0.2, 0])
        with self.voiceover(
            "Document partitioning has a price, which Part 39 called the tail at scale. <bookmark mark='a'/> A "
            "query waits for its slowest shard. Suppose, as Dean and Barroso did in 2013, that each server is slow "
            "on one request in a hundred. A query that touches one server is slow one time in a hundred; a query "
            "that must wait for a hundred servers is slow sixty-three times in a hundred. "
            "<bookmark mark='b'/> One remedy is the hedged request: "
            "after a short delay, send a second copy to another replica and keep whichever answers first. In their "
            "test it cut the ninety-nine point nine percentile from one thousand eight hundred milliseconds to "
            "seventy-four, for two percent more requests. <bookmark mark='c'/> Another is to answer without the "
            "stragglers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(notes[0]), run_time=1.5)
            self.add(dot, read)
            self.play(n.animate.set_value(100), run_time=4, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def replicas(self):
        head = label(r"Shards and replicas", font_size=36).to_edge(UP, buff=0.3)
        w, h, gx, gy = 1.45, 0.55, 0.22, 0.3
        x0, y0 = -5.6, 0.9

        def box(r, c, color=None):
            return module_box(rf"{c + 1}.{r + 1}", color or SHARD_COLORS[c % 4], w=w, h=h, font=17).move_to(
                [x0 + c * (w + gx), y0 - r * (h + gy), 0])
        grid = VGroup(*[box(r, c) for r in range(3) for c in range(4)])
        cols = VGroup(*[label(rf"shard {c + 1}", font_size=17, color=SHARD_COLORS[c]).move_to(
            [x0 + c * (w + gx), y0 + 0.55, 0]) for c in range(4)])
        broker = module_box(r"broker", HEAD, w=2.4, h=0.5).move_to([x0 + 1.5 * (w + gx), 2.35, 0])
        pick = [0, 2, 1, 0]
        rings = VGroup(*[SurroundingRectangle(grid[pick[c] * 4 + c], color=HEAD, buff=0.05, stroke_width=3)
                         for c in range(4)])
        dead = grid[2 * 4 + 1]
        cross = Cross(dead, stroke_color=NO, stroke_width=4)
        new_ring = SurroundingRectangle(grid[0 * 4 + 1], color=HEAD, buff=0.05, stroke_width=3)
        extra_row = VGroup(*[box(3, c) for c in range(4)])
        extra_col = VGroup(*[box(r, 4, color=GREY_B) for r in range(4)])
        extra_col_l = label(r"shard 5", font_size=17, color=GREY_B).move_to([x0 + 4 * (w + gx), y0 + 0.55, 0])
        notes = VGroup(
            wrapped_label(r"a query visits one replica of each shard", 4.4, font_size=19, color=HEAD),
            wrapped_label(r"a machine fails: \ the broker uses another copy of the same shard", 4.4, font_size=19,
                          color=NO),
            wrapped_label(r"more queries per second: \ add a row of replicas", 4.4, font_size=19, color=YES),
            wrapped_label(r"a bigger index: \ add a column of shards, \ each smaller and faster", 4.4,
                          font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.6, -0.2, 0])
        with self.voiceover(
            "A real deployment is a grid. <bookmark mark='a'/> The columns are shards, each holding a slice of the "
            "index; the rows are replicas, identical copies. A query visits one replica of every shard, chosen by "
            "load. <bookmark mark='b'/> When a machine fails, as one in a big cluster always is, the broker sends "
            "that shard's work to another copy, and the user notices nothing. <bookmark mark='c'/> The grid grows "
            "in two directions. More queries per second? Add a row of replicas. <bookmark mark='d'/> A bigger "
            "index? Add a column of shards, each smaller, so each answers faster. Capacity and size are separate "
            "dials."
        ) as vo:
            self.play(FadeIn(head), FadeIn(broker), FadeIn(grid), FadeIn(cols))
            vo.wait_until("a")
            self.play(Indicate(broker, color=HEAD))
            self.play(Create(rings), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(cross), FadeIn(notes[1]))
            self.play(ReplacementTransform(rings[1], new_ring))
            vo.wait_until("c")
            self.play(FadeIn(extra_row, shift=DOWN * 0.2), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(extra_col, shift=RIGHT * 0.2), FadeIn(extra_col_l), FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def caches(self):
        z = load("zipf")
        head = label(r"Caching the head", font_size=36).to_edge(UP, buff=0.3)
        specs = [(r"query", WHITE, 1.5), (r"result cache", YES, 2.1), (r"broker", HEAD, 1.6),
                 (r"shards: \ postings cache", DATA, 2.7), (r"disk", GREY_B, 1.3)]
        boxes = VGroup(*[module_box(t, c, w=w, h=0.7) for t, c, w in specs]).arrange(RIGHT, buff=0.42)
        boxes.next_to(head, DOWN, buff=0.7)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.05, color=GREY_B,
                                stroke_width=2, max_tip_length_to_length_ratio=0.3) for i in range(4)])
        q1 = tag_box(r"white whale", color=WHITE, size=15, h=0.38).next_to(boxes[0], DOWN, buff=0.3)
        q2 = tag_box(r"monster creator", color=WHITE, size=15, h=0.38).next_to(boxes[0], DOWN, buff=0.3)
        hit = label(r"hit: \ the stored page goes straight back", font_size=18, color=YES)
        miss = label(r"miss: \ the full path, \ where the tail lives", font_size=18, color=NO)
        lines = VGroup(
            wrapped_label(rf"queries are skewed like words: \ the novels' word counts fall as rank to the power "
                          rf"{z['zipf_slope']:.2f} \ (Chapter 1), \ and a small head of popular queries recurs "
                          r"all day", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"a \textbf{result cache} keeps whole answer pages for the head; \ entries expire, \ "
                          r"because the index changes under them", 12.4, font_size=20, color=YES),
            wrapped_label(r"a \textbf{postings cache} keeps the lists of popular terms in memory; \ Baeza-Yates "
                          r"et al. \ (2007): \ rank terms by how often queries use them, \ divided by the length of "
                          r"their lists", 12.4, font_size=20, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(boxes, DOWN, buff=1.9)
        with self.voiceover(
            "The cheapest query is one you have already answered. <bookmark mark='a'/> Queries are skewed the way "
            "words are: as Chapter 1 found for the novels, a few are enormously common and most are rare, so a "
            "small head of popular queries recurs all day. <bookmark mark='b'/> A result cache in front of the "
            "broker stores whole answer pages for that head. A hit goes straight back without touching a shard. "
            "Entries must expire, because the index keeps changing underneath them. <bookmark mark='c'/> A miss "
            "takes the full path, and that is where the tail lives. Inside each shard a second cache keeps the "
            "postings of popular terms in memory. Baeza-Yates and colleagues showed in 2007 that the best terms "
            "to keep are those queries use often relative to the length of their lists."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes), *[GrowArrow(a) for a in arrows])
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(q1))
            self.play(q1.animate.next_to(boxes[1], DOWN, buff=0.3), run_time=1.0)
            hit.next_to(q1, DOWN, buff=0.15).align_to(boxes[1], LEFT)
            self.play(Indicate(boxes[1], color=YES), FadeIn(hit), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeOut(q1), FadeOut(hit), FadeIn(q2))
            for k in (1, 2, 3):
                self.play(q2.animate.next_to(boxes[k], DOWN, buff=0.3), run_time=0.7)
            miss.next_to(q2, DOWN, buff=0.15)
            self.play(FadeIn(miss), Indicate(boxes[3], color=DATA), FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG,)
