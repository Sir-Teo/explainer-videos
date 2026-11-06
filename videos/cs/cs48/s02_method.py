from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs48.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load,
                                   module_box, tag_box)

PER_SERVER = 1000          # illustrative: requests a second one application server can handle
TARGET_UTIL = 0.5          # kept half busy (Part 31: latency explodes near full)


def servers_needed(n):
    return math.ceil(n["peak_qps"] / (PER_SERVER * TARGET_UTIL))


class Method(VoiceoverScene):
    def construct(self):
        self.card()
        self.steps()
        self.requirements()
        self.capacity()
        self.data_api()
        self.high_level()
        self.tradeoffs()

    def card(self):
        card = chapter_card(1, r"How a design is made", r"What do you decide, \ and in what order?",
                            lit=(2017, 2020), extra=((2017, r"Kleppmann: \ \textit{Designing Data-Intensive "
                                                            r"Applications}"),
                                                     (2020, r"Xu: \ \textit{System Design Interview}")), part=PART)
        with self.voiceover("Chapter one. How a design is made."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def steps(self):
        head = label(r"Eight decisions, \ in order", font_size=36).to_edge(UP, buff=0.3)
        names = [r"requirements", r"capacity model", r"data model", r"API", r"high-level design", r"deep dives",
                 r"trade-offs", r"design doc"]
        cols = [DATA, DATA, LAM, LAM, HEAD, HEAD, KERN, YES]
        boxes = []
        xs = [-4.8, -1.6, 1.6, 4.8]
        for i, (n, c) in enumerate(zip(names, cols)):
            b = module_box(rf"{i + 1}. \ {n}", c, w=2.7, h=0.75, font=20)
            r, k = divmod(i, 4)
            b.move_to([xs[k] if r == 0 else xs[3 - k], 1.3 if r == 0 else -0.6, 0])
            boxes.append(b)
        arrows = []
        for i in range(7):
            a, b = boxes[i], boxes[i + 1]
            if i < 3:
                s, e = a.get_right(), b.get_left()
            elif i == 3:
                s, e = a.get_bottom(), b.get_top()
            else:
                s, e = a.get_left(), b.get_right()
            arrows.append(Arrow(s, e, buff=0.06, stroke_width=2.5, color=GREY_B, max_tip_length_to_length_ratio=0.25))
        back = DashedLine(boxes[5][0].get_top() + LEFT * 0.5, boxes[1][0].get_bottom() + RIGHT * 0.5, color=NO,
                          dash_length=0.12).add_tip(tip_length=0.18)
        back_l = label(r"revise", font_size=18, color=NO).next_to(back.get_center(), RIGHT, buff=0.15)
        notes = VGroup(
            wrapped_label(r"not a waterfall: \ a deep dive that breaks an estimate sends you back to the model", 12.4,
                          font_size=21, color=WHITE),
            wrapped_label(r"running example \ (illustrative): \ the hook's napkin service as a \textbf{pastebin} "
                          r"--- store a text, \ get a link, \ read it later", 12.4, font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A design is a sequence of decisions, made in order. <bookmark mark='a'/> First the requirements: what "
            "the system must do, and how well. Then a capacity model, the data, and the interface. "
            "<bookmark mark='b'/> Only then a high-level design, deep dives into its riskiest parts, the trade-offs, "
            "and a written document. <bookmark mark='c'/> It is not a waterfall: a deep dive that breaks an estimate "
            "sends you back. We will follow one small service through it, a pastebin: store a text, get a link."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for p in zip(boxes[:4], arrows[:4]) for x in p], lag_ratio=0.4),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for p in zip(boxes[4:], arrows[4:] + [VGroup()]) for x in p],
                                  lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(back), FadeIn(back_l), FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    def requirements(self):
        head = label(r"Requirements, \ then objectives", font_size=36).to_edge(UP, buff=0.3)

        def column(title, items, color, x):
            t = label(title, font_size=24, color=color)
            body = VGroup(*[wrapped_label(s, 5.6, font_size=21, color=c) for s, c in items])
            body.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            g = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            g.move_to([x, 0, 0]).align_to([0, 2.75, 0], UP)
            return g
        fun = column(r"functional: \ what it does", [(r"create a paste, \ get a link", WHITE),
                                                    (r"read a paste by its link", WHITE),
                                                    (r"pastes expire", WHITE),
                                                    (r"not: \ editing, \ search", GREY_B)], DATA, -3.4)
        nf = column(r"non-functional: \ how well", [(r"fast reads", WHITE), (r"always up", WHITE),
                                                   (r"never loses a paste", WHITE),
                                                   (r"10 million users a day", WHITE)], HEAD, 3.4)
        slo1 = wrapped_label(r"99\% of reads within 200 ms", 5.6, font_size=21, color=YES)
        slo2 = wrapped_label(r"99.9\% of requests succeed, \ over 30 days", 5.6, font_size=21, color=YES)
        slo1.move_to(nf[1][0], aligned_edge=LEFT)
        slo2.move_to(nf[1][1], aligned_edge=LEFT)
        days, w, gap = 30, 0.3, 0.06
        tiles = VGroup(*[Square(side_length=w, stroke_width=1, stroke_color=GREY_C, fill_color=GREY_D,
                                fill_opacity=0.6) for _ in range(days)]).arrange(RIGHT, buff=gap)
        tiles.move_to([0.5, -0.55, 0])
        tl = label(r"30 days", font_size=18, color=GREY_B).next_to(tiles, LEFT, buff=0.2)
        budget_min = 30 * 24 * 60 * (1 - 0.999)
        day = Rectangle(width=tiles.width, height=0.42, stroke_width=1, stroke_color=GREY_C, fill_color=GREY_D,
                        fill_opacity=0.6).move_to([0.5, -1.6, 0])
        sliver = Rectangle(width=day.width * budget_min / (24 * 60), height=0.42, stroke_width=0, fill_color=NO,
                           fill_opacity=0.95).align_to(day, RIGHT).set_y(day.get_y())
        dl = label(r"one day", font_size=18, color=GREY_B).next_to(day, LEFT, buff=0.2)
        cap = label(rf"the month's whole error budget: \ 0.1\% of 30 days $\approx$ {budget_min:.0f} minutes, \ "
                    rf"{100 * budget_min / 1440:.0f}\% of a single day", font_size=20, color=NO).next_to(
            day, DOWN, buff=0.25)
        foot = note(r"illustrative targets", font_size=16).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Requirements come in two kinds. <bookmark mark='a'/> Functional ones say what the system does: create "
            "a paste and get a link, read it, let it expire; and, as useful, what it will not do. "
            "<bookmark mark='b'/> Non-functional ones say how well: fast, available, durable, at a given scale. As "
            "words, they cannot be checked. <bookmark mark='c'/> So turn them into "
            "service-level objectives, numbers over a window: ninety-nine percent of reads within two hundred "
            "milliseconds; ninety-nine point nine percent of requests succeeding over thirty days. "
            "<bookmark mark='d'/> The second is an error budget, about forty-three minutes a month, to spend on "
            "failures. Part 50 lives within it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(fun[0]), LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in fun[1]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(nf[0]), LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in nf[1]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(Transform(nf[1][0], slo1), Transform(nf[1][1], slo2))
            vo.wait_until("d")
            self.play(FadeIn(tiles, lag_ratio=0.05), FadeIn(tl), FadeIn(foot))
            self.play(TransformFromCopy(tiles[-1], day), FadeIn(dl))
            self.play(GrowFromEdge(sliver, RIGHT), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def capacity(self):
        n = load("napkin")
        peak_factor = n["peak_qps"] / n["avg_qps"]
        reads_per_write = (n["requests_per_day"] - n["writes_per_day"]) / n["writes_per_day"]
        mbit = n["read_bandwidth_Bps"] * 8 / 1e6
        head = label(r"The capacity model", font_size=36).to_edge(UP, buff=0.3)
        rows = [
            [rf"{n['peak_qps']:,.0f} requests/s at the peak",
             rf"at {PER_SERVER:,}/s a server, \ kept half busy \ (Part 31): \ {servers_needed(n)} servers",
             r"balancer, \ ch.\ 2"],
            [rf"{n['write_qps']:.0f} writes/s, \ {n['write_qps'] * peak_factor:.0f} at the peak",
             r"one primary database, \ replicas to spread the reads", r"replicas, \ ch.\ 9"],
            [rf"{reads_per_write:.0f} reads per write", r"skewed, \ repeated reads: \ cache them",
             r"cache, \ ch.\ 3--4"],
            [rf"{n['storage_bytes'] / 1e12:.0f} TB: \ {n['years']} years, \ {n['replicas']} copies",
             r"beyond one machine: \ shard the records, \ texts to a blob store", r"ch.\ 8 and 11"],
            [rf"{n['read_bandwidth_Bps'] / 1e6:.1f} MB/s out",
             rf"{mbit:.0f} Mbit/s, \ a tenth of one 1 Gbit/s link", r"none needed"],
        ]
        colors = [[DATA, WHITE, HEAD], [YES, WHITE, HEAD], [LAM, WHITE, HEAD], [KERN, WHITE, HEAD],
                  [GREY_A, WHITE, GREY_B]]
        tab = grid_table([r"from the napkin", r"so", r"block"], rows, widths=[4.0, 6.4, 2.2], row_h=0.8,
                         font_size=21, colors=colors, mono_cols=())
        tab.next_to(head, DOWN, buff=0.55).set_x(0)
        foot = wrapped_label(rf"numbers from the hook's napkin \ (computed); \ {PER_SERVER:,} requests a second "
                             r"per server is an illustrative assumption", 12.4, font_size=18,
                             color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Next, the capacity model: the hook's napkin, turned into decisions. <bookmark mark='a'/> About seven "
            "thousand requests a second at the peak. If a server handles a thousand, kept half busy, as Part 31 "
            f"advises, that is {servers_needed(n)} servers behind a load balancer. <bookmark mark='b'/> About two "
            "hundred writes a second, six hundred at the peak: one primary database, with replicas for reads. Ten "
            "reads per write: a cache earns its place. "
            "<bookmark mark='c'/> Two hundred terabytes will not fit one machine: shard the records, and put the "
            "texts in a blob store. <bookmark mark='d'/> A dozen megabytes a second is a tenth of one gigabit link: "
            "not the problem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1]), shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[2]), shift=RIGHT * 0.15))
            self.play(FadeIn(VGroup(*tab.cells[3]), shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[4]), shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[5]), shift=RIGHT * 0.15))
        self.wait(0.4)
        self.clear_scene()

    def data_api(self):
        head = label(r"The data, \ then the interface", font_size=36).to_edge(UP, buff=0.3)
        fields = code_block(["id        primary key", "owner     user id", "created   time", "expires   time",
                             "size      bytes", "blob_key  where the text is"], size=16)
        ttl = label(r"a \textbf{paste}", font_size=22, color=LAM)
        inner = VGroup(ttl, fields).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        frame = RoundedRectangle(width=inner.width + 0.6, height=inner.height + 0.5, corner_radius=0.12,
                                 stroke_color=LAM, stroke_width=2, fill_color=BG, fill_opacity=1)
        frame.move_to(inner)
        entity = VGroup(frame, inner).move_to([-4.2, 0.9, 0])
        e_note = wrapped_label(r"always read by its \texttt{id}: \ a key--value store will do \ (chapter 7)", 4.8,
                               font_size=19, color=YES).next_to(entity, DOWN, buff=0.35)
        api = code_block(["POST /pastes  {text, ttl}", "  Idempotency-Key: 5c1e...", "  -> 201 {id}",
                          "GET /pastes/{id}", "  -> 200 text | 404 | 410 Gone",
                          "GET /users/{u}/pastes?cursor=...", "  -> 200 {ids, next_cursor}"], size=17)
        api.move_to([2.6, 1.0, 0])
        api_notes = VGroup(
            wrapped_label(r"an idempotency key \ (Part 43): \ a retried create makes one paste, \ not two", 6.6,
                          font_size=19, color=HEAD),
            wrapped_label(r"expired is \textit{gone} \ (410), \ not \textit{never existed} \ (404)", 6.6,
                          font_size=19, color=DATA),
            wrapped_label(r"a cursor, \ not a page number: \ the list stays correct while it changes", 6.6,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(api, DOWN, buff=0.4).align_to(api, LEFT)
        foot = note(r"illustrative", font_size=16).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Then the data model. <bookmark mark='a'/> A paste is a record: an identifier, an owner, when it was "
            "made and when it expires, its size, and where its text is kept. It is always read by its identifier, "
            "so a key-value store will do. "
            "<bookmark mark='b'/> Then the interface. Creating a paste carries an idempotency key, Part 43's device, "
            "so that a retried request does not make two. <bookmark mark='c'/> Reading an expired paste says gone, "
            "not missing. <bookmark mark='d'/> And listing a user's pastes returns a cursor rather than a page "
            "number, so the list stays correct while it changes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(frame), FadeIn(ttl), LaggedStart(*[FadeIn(f) for f in fields], lag_ratio=0.2))
            self.play(FadeIn(e_note))
            vo.wait_until("b")
            self.play(FadeIn(api[0:3]), FadeIn(api_notes[0]), api[1].animate.set_color(HEAD))
            vo.wait_until("c")
            self.play(FadeIn(api[3:5]), FadeIn(api_notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(api[5:7]), FadeIn(api_notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def high_level(self):
        n = load("napkin")
        head = label(r"High-level design, \ then deep dives", font_size=36).to_edge(UP, buff=0.3)
        client = module_box(r"clients", WHITE, w=1.5, h=0.75, font=19).move_to([-5.9, 0.7, 0])
        lb = module_box(r"load balancer", HEAD, w=2.0, h=0.75, font=19).move_to([-3.5, 0.7, 0])
        app = module_box(rf"{servers_needed(n)} app servers", DATA, w=2.1, h=0.75, font=19).move_to([-0.9, 0.7, 0])
        cache = module_box(r"cache", YES, w=2.3, h=0.75, font=19).move_to([2.2, 1.9, 0])
        meta = module_box(r"records: \ sharded key--value", LAM, w=2.3, h=0.75, font=17).move_to([2.2, 0.7, 0])
        blob = module_box(r"texts: \ blob store", KERN, w=2.3, h=0.75, font=19).move_to([2.2, -0.5, 0])
        boxes = VGroup(client, lb, app, cache, meta, blob)

        def arr(a, b):
            return Arrow(a[0].get_right(), b[0].get_left(), buff=0.06, stroke_width=2.2, color=GREY_B,
                         max_tip_length_to_length_ratio=0.15)
        arrows = VGroup(arr(client, lb), arr(lb, app), arr(app, cache), arr(app, meta), arr(app, blob))
        qs = [
            (lb, r"which server takes each request? \ (ch.\ 2)", DOWN),
            (app, r"how to mint unique ids without a central counter? \ (ch.\ 10)", DOWN),
            (cache, r"a hot entry expires: \ a stampede? \ (ch.\ 4)", RIGHT),
            (meta, r"which shard key? \ (ch.\ 8)", RIGHT),
            (blob, r"signed links, \ the edge \ (ch.\ 11)", RIGHT),
        ]
        qlabels = VGroup()
        for box, text, d in qs:
            q = wrapped_label(text, 2.4 if d is DOWN else 3.0, font_size=18, color=box[0].get_stroke_color())
            q.next_to(box, d, buff=0.25)
            if d is RIGHT:
                q.set_y(box.get_y())
            qlabels.add(q)
        foot = wrapped_label(r"a deep dive takes the riskiest box first: \ the busiest by the estimate, \ or the "
                             r"one whose failure costs most", 12.4, font_size=21, color=WHITE).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Only now, the high-level design. <bookmark mark='a'/> Clients reach a load balancer, which "
            "spreads requests over stateless application servers. They read through a cache, keep the records in "
            "a sharded key-value store, and put the texts in a blob store. <bookmark mark='b'/> Every box hides "
            "questions, and deep dives take the riskiest first. Which server takes each request? How are "
            "identifiers made without a central counter? What happens when a popular entry expires and a thousand "
            "requests miss at once? Which key spreads the shards? The rest of this part answers each in turn."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes[:3]], lag_ratio=0.3), Create(arrows[:2]))
            self.play(LaggedStart(*[FadeIn(b) for b in boxes[3:]], lag_ratio=0.3), Create(arrows[2:]))
            vo.wait_until("b")
            for (box, _, _), q in zip(qs, qlabels):
                self.play(Indicate(box, scale_factor=1.08, color=WHITE), FadeIn(q), run_time=0.9)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def tradeoffs(self):
        head = label(r"Trade-offs, \ written down", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"a cache", r"fast reads, \ less load", r"a paste can be stale while its entry lives"],
                [r"sharding", r"storage past one machine", r"cheap queries across shards"],
                [r"a blob store", r"cheap, \ durable bytes", r"each create writes two systems that must agree"]]
        colors = [[WHITE, YES, NO] for _ in rows]
        tab = grid_table([r"choice", r"gains", r"gives up"], rows, widths=[2.4, 4.0, 6.2], row_h=0.6,
                         font_size=21, colors=colors, mono_cols=())
        tab.next_to(head, DOWN, buff=0.55).set_x(0)
        doc_t = label(r"the design document", font_size=24, color=HEAD)
        secs = [r"context", r"goals, non-goals", r"design", r"alternatives", r"trade-offs", r"open questions"]
        tags = VGroup(*[tag_box(s, color=c, size=17) for s, c in zip(secs, [DATA, DATA, HEAD, LAM, NO, KERN])])
        tags.arrange(RIGHT, buff=0.2)
        doc = VGroup(doc_t, tags).arrange(DOWN, buff=0.3).next_to(tab, DOWN, buff=0.7)
        foot = wrapped_label(r"reviewers argue with the document, \ not with a whiteboard; \ Part 49 writes eight",
                             12.4, font_size=20, color=GREY_A).next_to(doc, DOWN, buff=0.45)
        with self.voiceover(
            "No design is free, and a good one says what it gives up. <bookmark mark='a'/> The cache makes reads "
            "fast, and a paste can be stale for as long as its entry lives. <bookmark mark='b'/> Sharding takes the "
            "data past one machine, and gives up cheap queries across shards. The blob store keeps bytes cheaply "
            "and durably, and every create now writes two systems that must agree. <bookmark mark='c'/> All of it "
            "goes into a design document: context, goals and non-goals, the design, the alternatives and why they "
            "lost, the trade-offs, and open questions. Reviewers argue with the document, and Part 49 writes eight."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1]), shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[2]), shift=RIGHT * 0.15))
            self.play(FadeIn(VGroup(*tab.cells[3]), shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(doc_t), LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tags], lag_ratio=0.25))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN,)
