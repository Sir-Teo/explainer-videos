from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs48.compute import load as load48
from videos.cs.cs49.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, grid_table, load, mono

B62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def block(name, sub, color, w=2.1, h=0.95):
    """One building block: its name, and a small line saying where it comes from."""
    r = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2,
                         fill_color=BG, fill_opacity=1)
    t = label(name, font_size=19, color=WHITE)
    s = label(sub, font_size=15, color=color)
    for m in (t, s):
        if m.width > w - 0.15:
            m.width = w - 0.15
    VGroup(t, s).arrange(DOWN, buff=0.08).move_to(r)
    return VGroup(r, t, s)


def link(a, b, color=GREY_C):
    return Arrow(a, b, buff=0.08, stroke_width=2, color=color, max_tip_length_to_length_ratio=0.12)


def big(x):
    """An integer with thousands separators, for Tex."""
    return f"{x:,}".replace(",", "{,}")


class Shortener(VoiceoverScene):
    def construct(self):
        self.card()
        self.napkin()
        self.space()
        self.design()
        self.ids()
        self.traffic()

    def card(self):
        card = chapter_card(1, r"A URL shortener", r"How short can a link be, \ and how fast can it answer?",
                            lit=(2002, 2010), extra=((2002, r"TinyURL"), (2010, r"Snowflake IDs")), part=PART)
        with self.voiceover("Chapter one. A URL shortener."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def napkin(self):
        head = label(r"Requirements and the napkin", font_size=36).to_edge(UP, buff=0.3)
        api = VGroup(
            mono("POST /shorten   long URL  ->  code", size=18, color=DATA),
            mono("GET  /hBxM5A4   ->  redirect to the long URL", size=18, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(head, DOWN, buff=0.45)
        monthly = 100_000_000
        w = monthly / (30 * 86_400)
        r = 100 * w
        total = monthly * 12 * 5
        rows = [[r"new links", r"100 million a month", rf"{w:.0f} a second"],
                [r"redirects", r"100 per link", rf"{r:,.0f} a second".replace(",", "{,}")],
                [r"at a 3$\times$ peak", r"", rf"{3 * r:,.0f} a second".replace(",", "{,}")],
                [r"links in five years", r"", rf"{total / 1e9:.0f} billion"],
                [r"storage", r"500 bytes a link", rf"{total * 500 / 1e12:.0f} TB \ (before replicas)"]]
        tab = grid_table([r"quantity", r"assumption", r"result"], rows, widths=[3.6, 3.8, 4.4], row_h=0.5,
                         font_size=19, mono_cols=())
        tab.next_to(api, DOWN, buff=0.45)
        for k in range(1, len(rows) + 1):
            tab.cells[k][2].set_color(HEAD)
        foot = note(r"assumptions illustrative; \ arithmetic as in Part 48's worksheet", font_size=16).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "A URL shortener has two calls. <bookmark mark='a'/> One turns a long address into a short code; the "
            "other redirects from the code to the address. Links must last for years, and redirects must be fast. "
            "<bookmark mark='b'/> On the napkin, suppose a hundred million new links a month: about "
            f"{w:.0f} a second. <bookmark mark='c'/> If each is followed a hundred times, that is about {r:,.0f} "
            "redirects a second, three times that at the peak: overwhelmingly read-heavy. <bookmark mark='d'/> Five "
            "years make six billion links, and at five hundred bytes each, three terabytes, before replication."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(api[0]), FadeIn(api[1]))
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[2])), FadeIn(VGroup(*tab.cells[3])))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[4])), FadeIn(VGroup(*tab.cells[5])))
        self.wait(0.4)
        self.clear_scene()

    def space(self):
        s = load("shortener")
        ex = s["example"]
        head = label(r"The ID space: \ base 62", font_size=36).to_edge(UP, buff=0.3)
        form = label(r"length $L = \lceil \log_{62} N \rceil$ \ characters, \ each one of 0--9, \ a--z, \ A--Z",
                     font_size=22, color=WHITE).next_to(head, DOWN, buff=0.35)
        names = {1e6: r"a million", 1e9: r"a billion", 1e12: r"a trillion"}
        rows = [[names[r["links"]], f"{r['length']}", big(r["space"])] for r in s["rows"]]
        tab = grid_table([r"links $N$", r"length $L$", r"codes of that length, \ $62^L$"], rows,
                         widths=[1.7, 1.3, 3.2], row_h=0.7, font_size=20, mono_cols=())
        tab.next_to(form, DOWN, buff=0.6).to_edge(LEFT, buff=0.5)
        for k in range(1, 4):
            tab.cells[k][1].set_color(HEAD)
        # the trillionth link, converted by repeated division
        n, steps = ex["n"], []
        while True:
            q, r = divmod(n, 62)
            steps.append((n, q, r))
            n = q
            if n == 0:
                break
        lines = VGroup()
        for n0, q, r in steps:
            row = VGroup(label(rf"${big(n0)} = 62 \times {big(q)} + {r}$", font_size=20, color=GREY_A),
                         mono(B62[r], size=20, color=HEAD)).arrange(RIGHT, buff=0.3)
            lines.add(row)
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        lines.next_to(form, DOWN, buff=0.6).align_to([0.3, 0, 0], LEFT)
        right = max(row[0].get_right()[0] for row in lines)
        for row in lines:
            row[1].set_x(right + 0.45)
        code = VGroup(label(r"the trillionth link:", font_size=20, color=WHITE),
                      mono(ex["code"], size=26, color=HEAD)).arrange(RIGHT, buff=0.25)
        code.next_to(lines, DOWN, buff=0.4).align_to(lines, LEFT)
        rd = label(r"read the remainders upwards", font_size=17, color=GREY_B).next_to(code, DOWN, buff=0.15).align_to(
            code, LEFT)
        foot = wrapped_label(r"six characters cover the five years' six billion links; \ seven cover a trillion", 6.6,
                             font_size=19, color=YES).next_to(tab, DOWN, buff=0.5).align_to(tab, LEFT)
        with self.voiceover(
            "How short can the code be? <bookmark mark='a'/> Letters in both cases and digits make sixty-two "
            "symbols, so N links need the logarithm of N to base sixty-two characters, rounded up. "
            "<bookmark mark='b'/> A million links fit in four characters, a billion in six, a trillion in seven. "
            "<bookmark mark='c'/> Converting a number is Part 4's positional notation: divide by sixty-two again and "
            "again, and the remainders, read upwards, are the digits of the trillionth link. "
            "<bookmark mark='d'/> Our six billion links need only six characters. The length was never the "
            "problem. Choosing each link's number is."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(form))
            vo.wait_until("b")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.4), run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in lines], lag_ratio=0.3), run_time=3)
            self.play(TransformFromCopy(VGroup(*[r[1] for r in lines]), code[1]), FadeIn(code[0]), FadeIn(rd))
            vo.wait_until("d")
            self.play(FadeIn(foot), Indicate(VGroup(*tab.cells[2]), color=YES))
        self.wait(0.4)
        self.clear_scene()

    def design(self):
        head = label(r"The design, \ block by block", font_size=36).to_edge(UP, buff=0.3)
        y1, y2 = 1.1, -0.9
        client = block(r"browser", r"the click", WHITE, w=1.7).move_to([-5.75, y1, 0])
        lb = block(r"load balancer", r"Maglev, \ Part 48", GREY_B).move_to([-3.25, y1, 0])
        app = block(r"app servers", r"stateless", DATA).move_to([-0.65, y1, 0])
        cache = block(r"cache", r"W-TinyLFU, \ Part 48", YES).move_to([1.95, y1, 0])
        store = block(r"key-value store", r"code $\to$ URL, \ ch.\ 10", KERN, w=2.3).move_to([4.6, y1, 0])
        ids = block(r"ID ranges", r"a block of numbers each", HEAD, w=2.4).move_to([-0.65, y2, 0])
        logb = block(r"click log", r"Part 46", LAM).move_to([1.95, y2, 0])
        counts = block(r"click counts", r"a stream job", LAM, w=2.3).move_to([4.6, y2, 0])
        boxes = VGroup(client, lb, app, cache, store, ids, logb, counts)
        arrows = VGroup(link(client.get_right(), lb.get_left()), link(lb.get_right(), app.get_left()),
                        link(app.get_right(), cache.get_left()), link(cache.get_right(), store.get_left()),
                        link(app.get_bottom(), ids.get_top()), link(app.get_corner(DR), logb.get_corner(UL)),
                        link(logb.get_right(), counts.get_left()))
        read = wrapped_label(r"\textbf{read}: \ \texttt{GET /hBxM5A4} $\to$ any app server $\to$ the cache "
                             r"\ (almost always a hit) \ $\to$ \texttt{302}, \ Location: the long URL; \ the click "
                             r"goes onto the log", 12.6, font_size=19, color=YES)
        write = wrapped_label(r"\textbf{write}: \ the app server takes the next number from its own block, \ "
                              r"writes code $\to$ URL to the store, \ and returns the code", 12.6, font_size=19,
                              color=HEAD)
        VGroup(read, write).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45)
        pk = Dot(radius=0.11, color=YES).move_to(client.get_center())
        with self.voiceover(
            "The design uses Part 48's blocks. <bookmark mark='a'/> A click reaches a load balancer, Maglev hashing, "
            "which spreads requests over stateless app servers. Behind them sit a cache, and a key-value store "
            "mapping codes to addresses, the Dynamo-style store of chapter ten. <bookmark mark='b'/> Follow a read. "
            "An app server asks the cache, where a hot code almost always is, and answers with a redirect; a record "
            "of the click goes onto a log, Part 46's streams, where a job counts clicks per link. "
            "<bookmark mark='c'/> A write is rarer. The app server takes the next number from a block of a million "
            "that a coordinator handed it, stores the code and address, and returns the code."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes[:5]], lag_ratio=0.3), Create(arrows[:4]), run_time=3)
            self.play(FadeIn(boxes[5:]), Create(arrows[4:]))
            vo.wait_until("b")
            self.play(FadeIn(pk), FadeIn(read))
            for b in (lb, app, cache):
                self.play(pk.animate.move_to(b.get_center()), run_time=0.6)
            self.play(Indicate(cache, color=YES), run_time=0.6)
            ev = pk.copy().set_color(LAM)
            self.play(pk.animate.move_to(client.get_center()), ev.animate.move_to(logb.get_center()), run_time=1.2)
            self.play(ev.animate.move_to(counts.get_center()), FadeOut(pk), run_time=0.8)
            self.play(FadeOut(ev))
            vo.wait_until("c")
            wk = Dot(radius=0.11, color=HEAD).move_to(client.get_center())
            self.play(FadeIn(wk), FadeIn(write))
            for b in (lb, app, ids, app):
                self.play(wk.animate.move_to(b.get_center()), run_time=0.5)
            self.play(wk.animate.move_to(store.get_center()), run_time=0.9)
            self.play(wk.animate.move_to(client.get_center()), run_time=1.0)
            self.play(FadeOut(wk))
        self.wait(0.4)
        self.clear_scene()

    def ids(self):
        s = load("shortener")
        head = label(r"The hard part: \ which number?", font_size=36).to_edge(UP, buff=0.3)
        coll = {(c["chars"], c["links"]): c["expected_collisions"] for c in s["collisions"]}

        def fmt(v):
            return f"{v:,.0f}".replace(",", "{,}") if v >= 100 else (f"{v:.1f}" if v >= 1 else f"{v:.2g}")
        rows = [[f"{k}", fmt(coll[(k, 1e6)]), fmt(coll[(k, 1e8)])] for k in (6, 7, 8)]
        tab = grid_table([r"characters kept", r"1 million links", r"100 million links"], rows,
                         widths=[2.1, 2.2, 2.4], row_h=0.5, font_size=19, mono_cols=())
        for k in range(1, 4):
            tab.cells[k][1].set_color(HEAD if coll[(k + 5, 1e6)] < 1 else NO)
            tab.cells[k][2].set_color(NO)
        t1 = label(r"1. \ hash the URL, \ keep $k$ characters", font_size=22, color=NO)
        t2 = label(r"expected collisions $\approx m^2 / (2 \cdot 62^k)$", font_size=20, color=GREY_A)
        left = VGroup(t1, t2, tab).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        left.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.4)
        lnote = wrapped_label(r"the birthday bound of Part 17: \ every write must check the store, \ and retry with "
                              r"a salt on a clash", 6.6, font_size=18, color=GREY_B).next_to(left, DOWN, buff=0.3)
        lnote.align_to(left, LEFT)
        sf_chars = math.ceil(64 * math.log(2) / math.log(62))
        c2 = VGroup(label(r"2. \ a counter, \ handed out in blocks", font_size=22, color=HEAD),
                    wrapped_label(r"no collisions and no checks; \ the shortest codes; \ but consecutive codes are "
                                  r"guessable, \ so anyone can walk through every link", 5.6, font_size=18,
                                  color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        c3 = VGroup(label(r"3. \ Snowflake IDs \ (Part 48)", font_size=22, color=LAM),
                    wrapped_label(rf"41 bits of time, \ 10 of machine, \ 12 of sequence: \ no coordination at all, "
                                  rf"\ but 64 bits need {sf_chars} base-62 characters", 5.6, font_size=18,
                                  color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        right = VGroup(c2, c3).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.55)
        right.to_edge(RIGHT, buff=0.4)
        foot = wrapped_label(r"choice: \ the counter in blocks, \ with the number scrambled by a fixed bijection "
                             r"when codes must not be guessable", 12.4, font_size=19, color=YES).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "There are three ways to choose the number. <bookmark mark='a'/> The first hashes the address and keeps "
            "k characters. By Part 17's birthday bound, collisions come long before the space is full: with six "
            "characters, about nine among a million links, eighty-eight thousand among a hundred million. So every "
            "write must check the store and retry on a clash. <bookmark mark='b'/> The second is a counter, handed "
            "out in blocks: no checks, the shortest codes, but consecutive codes are guessable. "
            "<bookmark mark='c'/> The third is Part 48's Snowflake identifier: no coordination at all, but its "
            f"sixty-four bits take {sf_chars} characters. <bookmark mark='d'/> A common choice is the counter, passed "
            "through a fixed scrambling bijection when codes must not be guessable."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(t2))
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.4), run_time=2)
            self.play(FadeIn(lnote))
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(c3, shift=LEFT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def traffic(self):
        c48 = load48("caches")
        items = c48["items"]
        head = label(r"301 or 302, \ and Zipf's reads", font_size=36).to_edge(UP, buff=0.3)
        xs = (-5.9, -4.5, -3.1)
        names = (r"browser", r"CDN edge", r"shortener")

        def lanes(title, color, y0):
            g = VGroup(label(title, font_size=20, color=color).move_to([-4.5, y0, 0]))
            for x, n in zip(xs, names):
                g.add(label(n, font_size=16, color=GREY_A).move_to([x, y0 - 0.4, 0]))
                g.add(Line([x, y0 - 0.6, 0], [x, y0 - 2.0, 0], color=GREY_D, stroke_width=1.5))
            return g
        p1 = lanes(r"\texttt{301} permanent", NO, 2.75)
        p2 = lanes(r"\texttt{302} temporary", YES, 0.25)

        def hop(y, x_to, color):
            return Arrow([xs[0], y, 0], [x_to, y, 0], buff=0, stroke_width=2.5, color=color,
                         max_tip_length_to_length_ratio=0.08)
        a1 = VGroup(hop(2.05, xs[2], NO), label(r"click 1: \ reaches us, \ cached", font_size=15,
                                               color=GREY_B).move_to([-4.5, 1.8, 0]))
        a2 = VGroup(hop(1.35, xs[0] + 0.35, NO), label(r"click 2: \ never leaves the browser", font_size=15,
                                                       color=GREY_B).move_to([-4.5, 1.15, 0]))
        b1 = VGroup(hop(-0.45, xs[2], YES), label(r"click 1: \ reaches us", font_size=15,
                                                 color=GREY_B).move_to([-4.5, -0.65, 0]))
        b2 = VGroup(hop(-1.15, xs[2], YES), label(r"click 2: \ reaches us, \ counted", font_size=15,
                                                 color=GREY_B).move_to([-4.5, -1.35, 0]))
        for g in (a1, a2, b1, b2):
            g[1].add_background_rectangle(color=BG, opacity=1, buff=0.04)
        rows = c48["rows"]
        vals = [100 * r["tinylfu"] for r in rows]
        nm = [f"{100 * r['size'] / items:g}\\%" for r in rows]
        chart = bar_chart(vals, nm, [YES] * len(vals), height=2.6, bar_w=0.6, gap=0.35, vmax=100,
                          fmt_=lambda v: f"{v:.0f}\\%", font_size=17)
        ct = label(r"hit rate against cache size \ (share of links)", font_size=18, color=GREY_A)
        cg = VGroup(ct, chart).arrange(DOWN, buff=0.3).move_to([2.9, 1.0, 0])
        cnote = note(rf"Part 48's W-TinyLFU, \ Zipf traffic over {format(items, ',').replace(',', '{,}')} items",
                     font_size=16).next_to(cg, DOWN, buff=0.2)
        foot = wrapped_label(r"the trade-off: \ \texttt{301} lets browsers and CDNs absorb the load, \ but the "
                             r"service loses later clicks and cannot change the target; \ \texttt{302}, \ or a "
                             r"\texttt{301} with a short \texttt{Cache-Control} lifetime, \ keeps them", 12.4,
                             font_size=19,
                             color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The redirect itself is a choice, from Part 42's HTTP caching. <bookmark mark='a'/> A three-oh-one says "
            "the move is permanent. Browsers and edge caches remember it, and the second click never reaches us: "
            "cheap, but we lose the analytics and can never repoint the link. <bookmark mark='b'/> A three-oh-two "
            "says temporary, so every click comes back and is counted. <bookmark mark='c'/> Zipf's law makes that "
            "affordable: a few links get most clicks. On Part 48's Zipf traffic, a cache holding one percent of the "
            f"items catches {vals[2]:.0f} percent of requests, and ten percent catches {vals[4]:.0f}. "
            "<bookmark mark='d'/> The trade-off is our servers' load against the data and control we keep; a "
            "three-oh-one with a short cache lifetime sits in between."
        ) as vo:
            self.play(FadeIn(head), FadeIn(p1), FadeIn(p2))
            vo.wait_until("a")
            self.play(GrowArrow(a1[0]), FadeIn(a1[1]))
            self.play(GrowArrow(a2[0]), FadeIn(a2[1]))
            vo.wait_until("b")
            self.play(GrowArrow(b1[0]), FadeIn(b1[1]))
            self.play(GrowArrow(b2[0]), FadeIn(b2[1]))
            vo.wait_until("c")
            self.play(FadeIn(ct), FadeIn(chart[0]), FadeIn(chart.names), FadeIn(cnote))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in chart.bars], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(v) for v in chart.vals], lag_ratio=0.2), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN, LAM, NO, YES)
