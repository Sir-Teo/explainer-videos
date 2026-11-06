from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, code_block, grid_table, load,
                                   mono, tag_box)


def mini_call(kind, w=2.0, h=1.9):
    """A tiny sequence diagram of one gRPC call shape: client on the left, server on the right, time downwards."""
    xl, xr, top = -w / 2, w / 2, h / 2

    def y(t):
        return top - t * h
    shapes = {
        "unary": [(0.05, 0.3, True), (0.6, 0.85, False)],
        "server": [(0.0, 0.2, True), (0.3, 0.45, False), (0.45, 0.6, False), (0.6, 0.75, False),
                   (0.75, 0.9, False)],
        "client": [(0.0, 0.15, True), (0.15, 0.3, True), (0.3, 0.45, True), (0.45, 0.6, True),
                   (0.72, 0.92, False)],
        "bidi": [(0.0, 0.2, True), (0.12, 0.32, False), (0.3, 0.5, True), (0.42, 0.62, False), (0.6, 0.8, True),
                 (0.72, 0.92, False)],
    }
    g = VGroup(Line([xl, top + 0.05, 0], [xl, -top - 0.05, 0], color=GREY_C, stroke_width=2),
               Line([xr, top + 0.05, 0], [xr, -top - 0.05, 0], color=GREY_C, stroke_width=2))
    g.add(label(r"client", font_size=16, color=GREY_A).next_to(g[0], UP, buff=0.08),
          label(r"server", font_size=16, color=GREY_A).next_to(g[1], UP, buff=0.08))
    arrows = VGroup()
    for t0, t1, right in shapes[kind]:
        a, b = ([xl, y(t0), 0], [xr, y(t1), 0]) if right else ([xr, y(t0), 0], [xl, y(t1), 0])
        arrows.add(Arrow(a, b, buff=0.02, color=DATA if right else YES, stroke_width=2.2, tip_length=0.12,
                         max_tip_length_to_length_ratio=0.12))
    g.add(arrows)
    g.arrows = arrows
    return g


class Styles(VoiceoverScene):
    def construct(self):
        self.card()
        self.rest()
        self.methods()
        self.paging()
        self.grpc()
        self.graphql()

    def card(self):
        card = chapter_card(4, r"API styles", r"What shape should a remote interface take?",
                            lit=(2000, 2015, 2022), extra=((2000, r"Fielding: \ REST"), (2015, r"gRPC, \ GraphQL"),
                                                           (2022, r"RFC 9110")), part=PART)
        with self.voiceover("Chapter four. API styles."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rest(self):
        head = label(r"REST: \ resources and representations", font_size=36).to_edge(UP, buff=0.3)
        req = code_block(["GET /books/42 HTTP/1.1", "Host: api.example.com", "Accept: application/json"], size=19)
        res = code_block(["HTTP/1.1 200 OK", "Content-Type: application/json", "Cache-Control: max-age=60", "",
                          '{"id": 42,', ' "title": "Moby-Dick",', ' "author": "/authors/7"}'], size=19)
        rl = label(r"request", font_size=20, color=DATA)
        sl = label(r"response", font_size=20, color=YES)
        left = VGroup(rl, req, sl, res).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        left.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        ill = label(r"an illustrative exchange", font_size=16, color=GREY_B).next_to(left, DOWN, buff=0.25).align_to(
            left, LEFT)
        ideas = [(r"resources", HEAD, r"everything the server knows about has a name, \ a URL"),
                 (r"representations", DATA, (r"a client receives a representation \ (JSON, \ HTML), \ never the thing "
                                             r"itself, \ and it links to other resources")),
                 (r"uniform interface", LAM, (r"the same few methods on every resource, \ so caches and proxies "
                                              r"understand any request")),
                 (r"stateless", YES, (r"each request carries all it needs; \ any replica can answer, \ and a "
                                      r"response can be cached"))]
        rows = VGroup()
        for name, col, text in ideas:
            rows.add(VGroup(label(rf"\textbf{{{name}}}", font_size=23, color=col),
                            wrapped_label(text, 6.0, font_size=21, color=WHITE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                        buff=0.12))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.5).align_to(left, UP)
        VGroup(left, ill, rows).shift(DOWN * 0.55)
        with self.voiceover(
            "Roy Fielding, one of the authors of HTTP's specification, named the web's architecture in his doctoral "
            "dissertation of 2000: representational state transfer, or REST. <bookmark mark='a'/> Everything the "
            "server knows about is a resource with a name, a URL, like book forty-two. <bookmark mark='b'/> A "
            "client receives only a representation of it, here in JSON, which links to other resources, like the "
            "book's author. <bookmark mark='c'/> Every resource answers the same few methods, so a cache or a proxy "
            "can understand any request. <bookmark mark='d'/> And each request is stateless: it carries everything "
            "needed to answer it, so any replica can reply."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rl), FadeIn(req), FadeIn(ill))
            vo.wait_until("a")
            self.play(req[0].animate.set_color(HEAD), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(sl), FadeIn(res), FadeIn(rows[1]))
            self.play(res[6].animate.set_color(HEAD))
            vo.wait_until("c")
            self.play(Indicate(req[0], color=LAM), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Indicate(res[2], color=YES), FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()

    def methods(self):
        head = label(r"Safe and idempotent methods", font_size=36).to_edge(UP, buff=0.3)
        data = [(r"GET", "yes", "yes", r"read a resource"), (r"HEAD", "yes", "yes", r"read only its headers"),
                (r"OPTIONS", "yes", "yes", r"ask what is allowed"),
                (r"PUT", "no", "yes", r"replace it with this representation"),
                (r"DELETE", "no", "yes", r"remove it"), (r"POST", "no", "no", r"create, \ or anything else"),
                (r"PATCH", "no", r"not necessarily", r"apply a partial change")]
        cmap = {"yes": YES, "no": NO, r"not necessarily": HEAD}
        rows = [[rf"\texttt{{{m}}}", s, i, u] for m, s, i, u in data]
        colors = [[WHITE, cmap[s], cmap[i], GREY_A] for _, s, i, _ in data]
        tab = grid_table([r"method", r"safe", r"idempotent", r"typical use"], rows, widths=[2.4, 1.6, 2.9, 5.6],
                         row_h=0.46, font_size=22, colors=colors, mono_cols=())
        tab.next_to(head, DOWN, buff=0.35).set_x(0)
        put = mono('PUT /cart/7  {"qty": 2}', size=19, color=DATA)
        post = mono('POST /orders  {"item": 42}', size=19, color=DATA)
        twice1 = label(r"sent twice $\to$", font_size=20, color=GREY_A)
        twice2 = label(r"sent twice $\to$", font_size=20, color=GREY_A)
        cart = tag_box("cart 7: qty 2", YES, size=19)
        o1, o2 = tag_box("order 1001", NO, size=19), tag_box("order 1002", NO, size=19)
        r1 = VGroup(put, twice1, cart).arrange(RIGHT, buff=0.3)
        r2 = VGroup(post, twice2, o1, o2).arrange(RIGHT, buff=0.3)
        demo = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, DOWN, buff=0.45)
        demo.set_x(-1.0)
        twice1.align_to(twice2, LEFT)
        cart.next_to(twice1, RIGHT, buff=0.3)
        ill = label(r"illustrative", font_size=16, color=GREY_B).next_to(demo, RIGHT, buff=0.5)
        foot = wrapped_label(r"safe: \ the client asks for no change; \ idempotent: \ $n$ identical requests have the "
                             r"intended effect of one; \ every safe method is idempotent \ (RFC 9110, \ 2022; \ "
                             r"PATCH is RFC 5789)", 12.6, font_size=19, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "RFC 9110, the definition of HTTP's semantics published in 2022, sorts its methods by two properties. "
            "<bookmark mark='a'/> A safe method asks for no change at all: GET, HEAD and OPTIONS only "
            "read. <bookmark mark='b'/> An idempotent method may change things, but sending it twice has the same "
            "intended effect as sending it once: PUT replaces a resource, DELETE removes it, "
            "however often you repeat them. POST is neither, and PATCH need not be. <bookmark mark='c'/> This is "
            "what makes retries safe. A client whose request timed out cannot know whether it was applied. "
            "Repeating the PUT leaves the cart as intended. <bookmark mark='d'/> Repeating the POST may place a "
            "second order: the next chapter's problem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r][:2], tab.cells[r][3])) for r in (1, 2, 3)],
                                  lag_ratio=0.3))
            self.play(LaggedStart(*[FadeIn(tab.cells[r][2]) for r in (1, 2, 3)], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r])) for r in range(4, 8)], lag_ratio=0.35),
                      run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(put), FadeIn(ill))
            self.play(Indicate(put, color=HEAD), run_time=0.6)
            self.play(Indicate(put, color=HEAD), FadeIn(twice1), run_time=0.6)
            self.play(FadeIn(cart, shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(post), FadeIn(twice2))
            self.play(FadeIn(o1, shift=RIGHT * 0.2))
            self.play(FadeIn(o2, shift=RIGHT * 0.2), Flash(o2, color=NO))
        self.wait(0.4)
        self.clear_scene()

    def paging(self):
        rows = load("pagination")["rows"]
        r0, r3, r10 = rows[0], rows[2], rows[3]
        head = label(r"Offsets against cursors", font_size=36).to_edge(UP, buff=0.3)
        step, x0, y = 0.9, -5.85, 1.6

        def cell(i, color=GREY_B):
            r = RoundedRectangle(width=0.78, height=0.5, corner_radius=0.06, stroke_color=color, stroke_width=1.6,
                                 fill_color=BG, fill_opacity=1)
            return VGroup(r, mono(str(i), size=18, color=color).move_to(r))
        ids = list(range(20, 8, -1))
        cells = {i: cell(i).move_to([x0 + k * step, y, 0]) for k, i in enumerate(ids)}
        new = {i: cell(i, KERN).move_to([x0 + k * step, y, 0]) for k, i in enumerate((22, 21))}
        order = [22, 21] + ids

        def span(a, b):
            return VGroup(*[(new | cells)[i] for i in order[a:b]])
        nf = label(r"newest first", font_size=16, color=GREY_B).next_to(cells[20], DOWN, buff=0.15).align_to(
            cells[20], LEFT)
        ill = label(r"illustrative: \ pages of four", font_size=16, color=GREY_B).move_to([4.6, y + 0.75, 0])
        p1 = VGroup(*[cells[i] for i in (20, 19, 18, 17)])
        b1 = Brace(p1, UP, buff=0.08, color=DATA)
        l1 = label(r"page 1: \ offset 0", font_size=18, color=DATA).next_to(b1, UP, buff=0.06)
        b2 = Brace(span(4, 8), UP, buff=0.08, color=NO)
        l2 = label(r"page 2: \ offset 4 \ --- \ 18 and 17 again", font_size=18, color=NO).next_to(b2, UP, buff=0.06)
        b3 = Brace(span(6, 10), DOWN, buff=0.08, color=YES)
        l3 = label(r"cursor: \ older than 17 \ --- \ no repeats", font_size=18, color=YES).next_to(b3, DOWN,
                                                                                                 buff=0.06)
        trows = [[f"{r['inserts_per_page']}", f"{r['offset']['duplicates']}", f"{r['offset']['rows_scanned']:,}",
                  f"{r['cursor']['duplicates']}", f"{r['cursor']['rows_scanned']:,}"] for r in rows]
        tcol = [[WHITE, NO if r["offset"]["duplicates"] else WHITE, KERN, YES, YES] for r in rows]
        tab = grid_table([r"new rows per page", r"offset: \ repeats", r"offset: \ rows scanned", r"cursor: \ repeats",
                          r"cursor: \ rows scanned"], trows, widths=[2.7, 2.3, 2.8, 2.3, 2.8], row_h=0.4,
                         font_size=19, colors=tcol, mono_cols=())
        tab.move_to([0, -1.05, 0])
        foot = wrapped_label(rf"{r0['n']:,} rows, \ newest first, \ pages of {r0['page']}; \ an offset makes the "
                             r"database step past every skipped row, \ so a full pass is quadratic; \ a cursor "
                             r"\ (\texttt{WHERE id < last}) \ follows an index; \ deletions would make offsets skip "
                             r"rows instead", 12.6, font_size=18, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Long lists come in pages, and there are two ways to ask for the next one. <bookmark mark='a'/> With an "
            "offset, the client says: skip the rows I have, give me four more. Page one of this feed is rows twenty "
            "to seventeen. <bookmark mark='b'/> Now two new rows arrive at the top, everything shifts down, and "
            "skipping four lands on rows already seen. "
            "<bookmark mark='c'/> A cursor says instead: rows older than the last one I saw. It cannot repeat. "
            "<bookmark mark='d'/> We measured both on a thousand rows in pages of fifty. With three new rows per "
            f"page, offsets repeat {r3['offset']['duplicates']} rows; with ten, {r10['offset']['duplicates']}. "
            "Cursors repeat none. <bookmark mark='e'/> And since the database steps past every skipped row, offsets "
            "scan ten and a half thousand rows even with no inserts; a cursor reads only the thousand it returns."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c) for c in cells.values()], lag_ratio=0.05), FadeIn(nf),
                      FadeIn(ill))
            vo.wait_until("a")
            self.play(GrowFromCenter(b1), FadeIn(l1), *[c[0].animate.set_stroke(DATA) for c in p1],
                      *[c[1].animate.set_color(DATA) for c in p1])
            vo.wait_until("b")
            self.play(FadeOut(b1), FadeOut(l1), FadeOut(nf))
            self.play(*[c.animate.shift(RIGHT * 2 * step) for c in cells.values()],
                      *[FadeIn(c, shift=RIGHT * 0.4) for c in new.values()], run_time=1.5)
            seen = VGroup(cells[18], cells[17])
            self.play(GrowFromCenter(b2), FadeIn(l2), *[c[0].animate.set_stroke(NO) for c in seen],
                      *[c[1].animate.set_color(NO) for c in seen])
            vo.wait_until("c")
            fresh = VGroup(*[cells[i] for i in (16, 15, 14, 13)])
            self.play(GrowFromCenter(b3), FadeIn(l3), *[c[0].animate.set_stroke(YES) for c in fresh],
                      *[c[1].animate.set_color(YES) for c in fresh])
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r][:2], tab.cells[r][3])) for r in range(1, 5)],
                                  lag_ratio=0.3), run_time=2)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(VGroup(tab.cells[r][2], tab.cells[r][4])) for r in range(1, 5)],
                                  lag_ratio=0.3), FadeIn(foot), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def grpc(self):
        head = label(r"gRPC: \ typed calls and streams", font_size=36).to_edge(UP, buff=0.3)
        proto = code_block(["service Library {", "  rpc Get(BookId) returns (Book);",
                            "  rpc List(Query) returns (stream Book);", "  rpc Upload(stream Chunk) returns (Receipt);",
                            "  rpc Chat(stream Note) returns (stream Note);", "}"], size=18)
        proto.next_to(head, DOWN, buff=0.7).to_edge(LEFT, buff=0.5)
        pl = label(r"a \texttt{.proto} service \ (illustrative)", font_size=17, color=GREY_B).next_to(
            proto, UP, buff=0.15).align_to(proto, LEFT)
        shapes = VGroup()
        for kind, name in (("unary", r"unary"), ("server", r"server streaming"), ("client", r"client streaming"),
                           ("bidi", r"bidirectional")):
            d = mini_call(kind)
            shapes.add(VGroup(d, label(name, font_size=20, color=WHITE).next_to(d, DOWN, buff=0.15)))
        shapes.arrange_in_grid(rows=2, cols=2, buff=(0.7, 0.45)).next_to(head, DOWN, buff=0.5).to_edge(RIGHT,
                                                                                                       buff=0.5)
        notes = VGroup(
            wrapped_label(r"messages in protocol buffers \ (chapter 2), \ stubs generated for each language \ "
                          r"(chapter 1)", 6.2, font_size=21, color=DATA),
            wrapped_label(r"carried by HTTP/2: \ many calls at once on one connection \ (Part 37), \ each with a "
                          r"deadline", 6.2, font_size=21, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(proto, DOWN, buff=0.6).align_to(proto, LEFT)
        with self.voiceover(
            "Google's gRPC, open-sourced in 2015 from its internal system Stubby, sees an API as a set of typed "
            "procedures. <bookmark mark='a'/> Services are declared in a protocol buffers file, so messages travel "
            "in chapter two's compact binary, and stubs are generated for every language. <bookmark mark='b'/> "
            "Calls ride on HTTP/2, many at once on one connection, each with a deadline. <bookmark mark='c'/> And a "
            "call need not be one request and one reply: a server can stream replies, a client can stream "
            "requests, and both can stream at once."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pl), LaggedStart(*[FadeIn(ln) for ln in proto], lag_ratio=0.2), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            for k, s in enumerate(shapes):
                self.play(FadeIn(s[0][:4]), FadeIn(s[1]), Indicate(proto[k + 1], color=HEAD), run_time=0.5)
                self.play(LaggedStart(*[GrowArrow(a) for a in s[0].arrows], lag_ratio=0.3), run_time=1.0)
        self.wait(0.4)
        self.clear_scene()

    def graphql(self):
        n = load("nplus1")
        books = n["nested_naive"] - n["naive"]
        head = label(r"GraphQL, \ and the N + 1 problem", font_size=36).to_edge(UP, buff=0.3)
        query = code_block(["{", f"  authors(first: {n['authors']}) {{", "    name", "    books {", "      title",
                            "    }", "  }", "}"], size=19)
        ql = label(r"query", font_size=20, color=DATA)
        qg = VGroup(ql, query).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(head, DOWN, buff=0.45).to_edge(
            LEFT, buff=0.6)
        resp = code_block(['{"authors": [', '  {"name": "Melville",', '   "books": [{"title": "Moby-Dick"},',
                           '             {"title": "Typee"}]},', '  {"name": "Austen", ...},', '  ...]}'], size=18)
        rlab = label(r"response: \ the same shape \ (illustrative)", font_size=20, color=YES)
        rg = VGroup(rlab, resp).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(qg, RIGHT, buff=1.0).align_to(
            qg, UP)
        arr = Arrow(qg.get_right(), rg.get_left(), buff=0.2, color=GREY_B, stroke_width=2)
        big = Square(0.55, stroke_color=DATA, fill_color=DATA, fill_opacity=0.6)
        smalls = VGroup(*[Square(0.24, stroke_width=0, fill_color=KERN, fill_opacity=0.85)
                          for _ in range(n["authors"])]).arrange_in_grid(rows=5, cols=10, buff=0.08)
        VGroup(big, smalls).arrange(DOWN, buff=0.35).next_to(qg, RIGHT, buff=0.7).align_to(qg, UP).shift(
            DOWN * 0.4)
        bl = label(r"1 query: \ the authors", font_size=19, color=DATA).next_to(big, RIGHT, buff=0.15)
        sl = label(rf"+ {n['authors']}: \ one per author's books", font_size=19, color=KERN).next_to(smalls, DOWN,
                                                                                                buff=0.15)
        batch = RoundedRectangle(width=smalls.width, height=0.5, corner_radius=0.06, stroke_width=0, fill_color=YES,
                                 fill_opacity=0.85).move_to(smalls)
        batl = label(rf"+ 1: \ books of all {n['authors']} authors", font_size=19, color=YES).move_to(sl)
        chart = bar_chart([n["naive"], n["batched"], n["nested_naive"], n["nested_batched"]],
                          [r"naive", r"batched", r"naive", r"batched"], [KERN, YES, KERN, YES], height=2.6,
                          bar_w=0.6, gap=0.45, fmt_=lambda v: f"{v}", font_size=20)
        chart.to_edge(RIGHT, buff=0.5)
        chart.shift(UP * (-1.0 - chart.bars[0].get_bottom()[1]))
        cap = VGroup(label(r"books", font_size=17, color=GREY_B).next_to(chart.names[:2], DOWN, buff=0.12),
                     label(r"+ reviews", font_size=17, color=GREY_B).next_to(chart.names[2:], DOWN, buff=0.12))
        ctitle = label(rf"queries \ ({n['authors']} authors, \ {books} books)", font_size=18,
                       color=GREY_A).next_to(chart, UP, buff=0.25)
        notes = VGroup(
            wrapped_label(r"\textbf{persisted queries}: \ clients send only the hash of a query registered in "
                          r"advance, \ and the server runs nothing else", 12.4, font_size=20, color=LAM),
            wrapped_label(r"\textbf{cost limits}: \ estimate a query's work from its depth and list sizes before "
                          r"running it, \ and refuse it above a budget", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "GraphQL, released by Facebook in 2015, puts the client in charge of the shape. <bookmark mark='a'/> A "
            "query names the fields it wants, nested as deeply as it likes, and the response has exactly that "
            "shape, with no second round trip for the books. <bookmark mark='b'/> The server fills it in with a "
            "resolver per field, and the obvious resolvers hide a trap. One query fetches fifty authors; then each "
            f"author's books resolver runs its own query. That is {n['naive']} queries, the N plus one problem; "
            f"with each book's reviews, {n['nested_naive']}. <bookmark mark='c'/> The fix is batching, in the style "
            "of Facebook's DataLoader: collect every key requested in one tick, and fetch them together. "
            f"{n['naive']} queries become {n['batched']}, and {n['nested_naive']} become {n['nested_batched']}. "
            "<bookmark mark='d'/> And since clients can write any query, public servers defend themselves with "
            "persisted queries and cost limits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(qg))
            vo.wait_until("a")
            self.play(GrowArrow(arr), FadeIn(rg))
            vo.wait_until("b")
            self.play(FadeOut(arr), FadeOut(rg))
            self.play(FadeIn(big), FadeIn(bl), Indicate(query[1], color=DATA))
            self.play(Indicate(query[3], color=KERN),
                      LaggedStart(*[FadeIn(s, scale=0.5) for s in smalls], lag_ratio=0.04), FadeIn(sl), run_time=2.5)
            self.play(FadeIn(ctitle), FadeIn(chart[0]), GrowFromEdge(chart.bars[0], DOWN), FadeIn(chart.vals[0]),
                      FadeIn(chart.names[0]), GrowFromEdge(chart.bars[2], DOWN), FadeIn(chart.vals[2]),
                      FadeIn(chart.names[2]), FadeIn(cap))
            vo.wait_until("c")
            self.play(ReplacementTransform(smalls, batch), ReplacementTransform(sl, batl))
            self.play(GrowFromEdge(chart.bars[1], DOWN), FadeIn(chart.vals[1]), FadeIn(chart.names[1]),
                      GrowFromEdge(chart.bars[3], DOWN), FadeIn(chart.vals[3]), FadeIn(chart.names[3]))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM, NO)
