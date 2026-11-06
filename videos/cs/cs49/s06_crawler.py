from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs49.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, module_box,
                                   mono, tag_box)


def _path(points):
    return VMobject().set_points_as_corners([[x, y, 0] for x, y in points])


class Crawler(VoiceoverScene):
    def construct(self):
        self.card()
        self.napkin()
        self.design()
        self.frontier()
        self.dedup()

    def card(self):
        card = chapter_card(5, r"A web crawler", r"How do you fetch a billion pages, \ politely, \ once each?",
                            lit=(1999, 2007), extra=((1999, r"Heydon and Najork: \ Mercator"),
                                                     (2007, r"Manku et al.: \ SimHash dedup")), part=PART)
        with self.voiceover("Chapter five. A web crawler."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def napkin(self):
        c = load("crawler")
        head = label(r"The napkin: \ a billion pages a month", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"pages", rf"{c['pages'] / 1e9:.0f} billion in {c['days']} days",
                 rf"{c['pages_per_second']:.0f} a second"],
                [r"fetches in flight", r"half a second per fetch", rf"{c['concurrent_fetches']:.0f} at once"],
                [r"bandwidth", r"100 kB a page", rf"{c['gbit_per_s']:.2f} Gbit/s"],
                [r"fetching machines", r"500 connections each", rf"{c['machines']:.2f} of one"],
                [r"politeness", rf"{c['polite_host_rate']:.0f} request a second per host",
                 rf"$\geq$ {c['hosts_needed_busy']:.0f} hosts busy at once"],
                [r"URLs seen", r"a Bloom filter, \ 1\% false positives",
                 rf"{c['bloom_bits_per_url']:.1f} bits a URL, \ {c['bloom_bytes_1pct'] / 1e9:.1f} GB"]]
        tab = grid_table([r"quantity", r"assumption", r"result"], rows, widths=[3.2, 5.0, 4.6], row_h=0.66,
                         font_size=22, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45)
        for r in range(1, len(rows) + 1):
            tab.cells[r][2].set_color(HEAD)
        for r in (5, 6):
            tab.cells[r][2].set_color(NO)
        foot = wrapped_label(r"the speed is easy; \ the manners and the memory are the design", 12.4, font_size=24,
                             color=WHITE).next_to(tab, DOWN, buff=0.5)
        note_ = note(r"assumptions illustrative; \ the arithmetic is the crawler instrument's", font_size=16).to_edge(
            DOWN, buff=0.3)
        with self.voiceover(
            "Requirements first. A search engine, like the one of Part 47, wants a billion pages fetched every month, "
            "politely, and never the same page twice. <bookmark mark='a'/> A billion pages in thirty days is about "
            "three hundred and eighty-six pages a second. <bookmark mark='b'/> If a fetch takes half a second, about "
            "a hundred and ninety-three are in flight at once; at a hundred kilobytes a page, that is about a third "
            "of a gigabit a second, and one machine could carry it. "
            "<bookmark mark='c'/> What makes the crawler hard is manners. A polite crawler asks any one host for at "
            "most one page a second, so to keep its rate it must be busy with at least three hundred and eighty-six "
            "different hosts at once. And it must remember every URL it has seen: a billion of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])), FadeIn(note_))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[2])), FadeIn(VGroup(*tab.cells[3])))
            self.play(FadeIn(VGroup(*tab.cells[4])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[5])))
            self.play(FadeIn(VGroup(*tab.cells[6])), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def design(self):
        head = label(r"The design: \ a loop", font_size=36).to_edge(UP, buff=0.3)
        yt = 1.1
        front = module_box(r"URL frontier", HEAD, w=2.4, h=0.75).move_to([-4.6, yt, 0])
        fetch = module_box(r"fetcher", KERN, w=2.2, h=0.75).move_to([-1.5, yt, 0])
        parse = module_box(r"parser", DATA, w=2.2, h=0.75).move_to([1.5, yt, 0])
        store = module_box(r"page store \ (blobs)", GREY_B, w=2.4, h=0.75).move_to([4.6, yt, 0])
        seeds = module_box(r"seed URLs", GREY_B, w=2.0, h=0.6).move_to([-4.6, 2.35, 0])
        dns = module_box(r"DNS cache", LAM, w=2.0, h=0.6).move_to([-1.5, 2.35, 0])
        seen = module_box(r"seen before?", NO, w=2.2, h=0.65).move_to([1.5, -0.25, 0])

        def arr(a, b):
            return Arrow(a, b, buff=0.06, color=GREY_C, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        arrows = VGroup(arr(seeds.get_bottom(), front.get_top()), arr(front.get_right(), fetch.get_left()),
                        arr(fetch.get_right(), parse.get_left()), arr(parse.get_right(), store.get_left()),
                        DoubleArrow(fetch.get_top(), dns.get_bottom(), buff=0.06, color=GREY_C, stroke_width=2,
                                    tip_length=0.15),
                        arr(parse.get_bottom(), seen.get_top()))
        back_pts = [(seen.get_left()[0], -0.25), (-4.6, -0.25), (-4.6, front.get_bottom()[1])]
        back = VGroup(_path(back_pts).set_stroke(YES, 2),
                      Arrow([-4.6, -0.05, 0], front.get_bottom(), buff=0.0, color=YES, stroke_width=2,
                            max_tip_length_to_length_ratio=0.4))
        back_l = label(r"new URLs only", font_size=17, color=YES).next_to([-2.6, -0.25, 0], DOWN, buff=0.1)
        # partitioning by host
        nodes = VGroup(*[module_box(rf"crawler {i}", GREY_A, w=2.1, h=0.55, font=17) for i in range(4)]).arrange(
            RIGHT, buff=0.55).move_to([0, -1.75, 0])
        hosts = [r"a.example", r"b.example", r"c.example", r"d.example"]
        hl = VGroup(*[mono(h, size=14, color=GREY_B).next_to(n, DOWN, buff=0.1) for h, n in zip(hosts, nodes)])
        pnote = wrapped_label(r"each host belongs to one machine, \ by a hash of its name \ (Part 39): \ its queue, "
                              r"\ its politeness clock and its DNS entry live in one place; \ a link to another host "
                              r"is forwarded to its owner", 12.4, font_size=19, color=WHITE).to_edge(DOWN, buff=0.3)
        ill = note(r"hosts illustrative", font_size=16).next_to(nodes, RIGHT, buff=0.15).shift(DOWN * 0.45)
        pkt = Dot(radius=0.11, color=HEAD)
        loop = _path([front.get_center()[:2], fetch.get_center()[:2], parse.get_center()[:2],
                      store.get_center()[:2]])
        with self.voiceover(
            "The design is a loop. <bookmark mark='a'/> Seed URLs enter the frontier, the list of pages still to "
            "fetch. A fetcher takes one, looks up its host name and downloads the page, and the parser "
            "stores it. <bookmark mark='b'/> Name lookups would dominate if done naively, so every fetcher "
            "keeps a DNS cache, Part 37's resolver; Mercator, the crawler Allan Heydon and Marc Najork described in "
            "1999, found lookups slow enough to write its own resolver. <bookmark mark='c'/> The parser also "
            "extracts the page's links. Each is checked against the set of URLs already seen, and only new ones go "
            "back to the frontier. <bookmark mark='d'/> Across machines the work is split by a hash of the host "
            "name, so everything about one host lives on one machine, and a link to another host is forwarded to "
            "the machine that owns it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in (seeds, front, fetch, parse, store)], lag_ratio=0.25),
                      *[GrowArrow(a) for a in arrows[:4]], run_time=2)
            pkt.move_to(front)
            self.play(FadeIn(pkt))
            self.play(MoveAlongPath(pkt, loop), run_time=2.2, rate_func=linear)
            self.play(FadeOut(pkt))
            vo.wait_until("b")
            self.play(FadeIn(dns), GrowFromCenter(arrows[4]))
            q = Dot(radius=0.09, color=LAM).move_to(fetch.get_top())
            self.play(q.animate.move_to(dns.get_bottom()), run_time=0.6)
            self.play(q.animate.move_to(fetch.get_top()), run_time=0.6)
            self.play(FadeOut(q))
            vo.wait_until("c")
            self.play(FadeIn(seen), GrowArrow(arrows[5]))
            links = VGroup(Dot(radius=0.09, color=YES), Dot(radius=0.09, color=NO)).move_to(parse)
            self.play(links.animate.move_to(seen), run_time=0.8)
            cross = Cross(links[1], stroke_color=NO, stroke_width=4).scale(1.6)
            self.play(Create(cross), Create(back[0]), FadeIn(back[1]), FadeIn(back_l))
            self.play(FadeOut(links[1]), FadeOut(cross), MoveAlongPath(links[0], _path(back_pts)), run_time=1.5)
            self.play(FadeOut(links[0]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.2), FadeIn(hl), FadeIn(ill))
            fwd = Dot(radius=0.09, color=HEAD).move_to(nodes[0])
            self.play(FadeIn(fwd))
            self.play(fwd.animate.move_to(nodes[2]), run_time=1.0)
            self.play(Indicate(nodes[2], color=HEAD), FadeOut(fwd), FadeIn(pnote))
        self.wait(0.4)
        self.clear_scene()

    def frontier(self):
        head = label(r"The frontier: \ priority in front, \ politeness behind", font_size=36).to_edge(UP, buff=0.3)
        # front queues by priority (left), back queues by host (middle), and a heap of next-allowed times (right)
        fq_names = [r"high", r"medium", r"low"]
        fq = VGroup()
        for i, n in enumerate(fq_names):
            slot = Rectangle(width=3.0, height=0.5, stroke_color=GREY_C, stroke_width=1.5).move_to(
                [-4.2, 1.5 - i * 0.75, 0])
            nm = label(n, font_size=16, color=GREY_A).next_to(slot, LEFT, buff=0.1)
            fq.add(VGroup(slot, nm))
        fq_t = label(r"front queues: \ priority", font_size=19, color=HEAD).next_to(fq, UP, buff=0.25)
        hosts = [r"a.example", r"b.example", r"c.example", r"d.example"]
        bq = VGroup()
        for i, h in enumerate(hosts):
            slot = Rectangle(width=2.6, height=0.5, stroke_color=GREY_C, stroke_width=1.5).move_to(
                [0.4, 1.7 - i * 0.7, 0])
            nm = mono(h, size=14, color=GREY_B).next_to(slot, LEFT, buff=0.1)
            bq.add(VGroup(slot, nm))
        bq_t = label(r"back queues: \ one host each", font_size=19, color=KERN).next_to(bq, UP, buff=0.25)
        times = [(r"c.example", 0.2), (r"a.example", 0.6), (r"d.example", 0.9), (r"b.example", 1.4)]

        def heap_rows(ts):
            g = VGroup()
            for k, (h, t) in enumerate(ts):
                row = VGroup(mono(h, size=14, color=YES if k == 0 else GREY_A),
                             mono(f"t = {t:.1f} s", size=14, color=YES if k == 0 else GREY_A)).arrange(RIGHT,
                                                                                                    buff=0.3)
                g.add(row)
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([5.0, 0.75, 0])
            return g
        heap = heap_rows(times)
        heap_box = SurroundingRectangle(heap, color=YES, buff=0.2, corner_radius=0.08, stroke_width=1.5)
        heap_t = label(r"a heap: \ when each host may be asked again", font_size=19, color=YES)
        heap_t.width = min(heap_t.width, 3.4)
        heap_t.next_to(heap_box, UP, buff=0.25)
        # tokens in the queues
        tok = {}
        for i, h in enumerate(hosts):
            tok[h] = VGroup(*[Square(side_length=0.32, stroke_width=0, fill_color=DATA, fill_opacity=0.8)
                              for _ in range(3 - i % 2)]).arrange(RIGHT, buff=0.08)
            tok[h].align_to(bq[i][0], LEFT).shift(RIGHT * 0.1).set_y(bq[i][0].get_y())
        ftok = VGroup()
        for i in range(3):
            g = VGroup(*[Square(side_length=0.32, stroke_width=0, fill_color=[HEAD, LAM, GREY_B][i],
                                fill_opacity=0.8) for _ in range(4 - i)]).arrange(RIGHT, buff=0.08)
            g.align_to(fq[i][0], LEFT).shift(RIGHT * 0.1).set_y(fq[i][0].get_y())
            ftok.add(g)
        new = tag_box(r"new URL", color=DATA, size=14).move_to([-4.2, 2.8, 0])
        notes = VGroup(
            wrapped_label(r"pop the host whose time has come, \ fetch the head of its queue, \ push the host back "
                          r"with a new time; \ an empty back queue is refilled from the front", 12.4, font_size=19,
                          color=WHITE),
            wrapped_label(r"the new time is the politeness rule: \ here one request a second; \ a common heuristic "
                          r"waits several times as long as the last fetch took, \ so a slow server is asked less "
                          r"often", 12.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        ill = note(r"times illustrative", font_size=16).next_to(heap_box, DOWN, buff=0.15)
        fetched = tag_box(r"fetch c.example/...", color=HEAD, size=14).next_to(heap_box, DOWN, buff=0.6)
        with self.voiceover(
            "The frontier is the heart of a crawler, and Mercator's design of it is still the textbook one. "
            "<bookmark mark='a'/> New URLs are first sorted by priority, by importance or how often a page changes, "
            "into a few front queues. <bookmark mark='b'/> Behind them sit back queues, one for each host, "
            "each holding only that host's URLs. <bookmark mark='c'/> A heap, the priority queue of Part 17, keyed "
            "by the earliest time each host may be visited again, decides what is fetched next. Pop the host whose "
            "time has come, fetch the URL at the head of its queue, and push the host back with a new time. "
            "<bookmark mark='d'/> The new time is the politeness rule: here one request a second; a common heuristic "
            "waits several times as long as the last fetch took, so a struggling server is asked less often."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(fq), FadeIn(fq_t), FadeIn(ftok))
            self.play(FadeIn(new))
            self.play(new.animate.scale(0.6).move_to(ftok[0].get_right() + RIGHT * 0.3), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(bq), FadeIn(bq_t), LaggedStart(*[FadeIn(tok[h]) for h in hosts], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(heap), Create(heap_box), FadeIn(heap_t), FadeIn(ill))
            self.play(Indicate(heap[0], color=YES), Indicate(bq[2], color=YES))
            out = tok[r"c.example"][0]
            self.play(out.animate.move_to(fetched), FadeIn(fetched), run_time=0.9)
            self.play(FadeOut(out), FadeIn(notes[0]))
            vo.wait_until("d")
            new_heap = heap_rows([times[1], times[2], (r"c.example", 1.2), times[3]])
            self.play(Transform(heap, new_heap), FadeIn(notes[1]))
            refill = ftok[1][-1]
            self.play(refill.animate.move_to(tok[r"c.example"][-1].get_right() + RIGHT * 0.4), run_time=0.9)
        self.wait(0.4)
        self.clear_scene()

    def dedup(self):
        b = load("bloom")
        c = load("crawler")
        head = label(r"Seen before? \ A Bloom filter", font_size=36).to_edge(UP, buff=0.3)
        m = 24
        cell = 0.46
        bits = VGroup(*[Square(side_length=cell, stroke_color=GREY_C, stroke_width=1.5, fill_color=BG,
                               fill_opacity=1) for _ in range(m)]).arrange(RIGHT, buff=0).move_to([0, 1.0, 0])
        vals = VGroup(*[mono("0", size=15, color=GREY_C).move_to(s) for s in bits])
        urls = [(r"a.example/1", [3, 9, 17], DATA, -4.0), (r"b.example/2", [6, 12, 20], LAM, 0.0),
                (r"c.example/3", [3, 12, 17], NO, 4.0)]
        tags = VGroup(*[tag_box(u, color=col, size=14).move_to([x, 2.35, 0]) for u, _, col, x in urls])

        def hits(k):
            _, idx, col, _ = urls[k]
            return VGroup(*[Arrow(tags[k].get_bottom(), bits[i].get_top(), buff=0.06, color=col, stroke_width=1.8,
                                  max_tip_length_to_length_ratio=0.08) for i in idx])
        ill = note(r"24 bits and 3 hashes, \ illustrative", font_size=16).next_to(bits, DOWN, buff=0.12)
        verdict = label(r"all three bits set: \ ``probably seen'' \ --- \ wrongly", font_size=19, color=NO)
        verdict.next_to(ill, DOWN, buff=0.15)
        rows = [[rf"{b['urls']:,} URLs, \ {b['bits_per_url']} bits each, \ {b['hashes']} hashes",
                 rf"{100 * b['false_positive']:.3f}\%", rf"{100 * b['theory']:.3f}\%"]]
        tab = grid_table([r"measured \ (our filter)", r"false positives", r"theory $(1 - e^{-kn/m})^k$"], rows,
                         widths=[5.6, 2.6, 3.6], row_h=0.5, font_size=19, mono_cols=())
        tab.cells[1][1].set_color(HEAD)
        tab.cells[1][2].set_color(YES)
        tab.next_to(verdict, DOWN, buff=0.35)
        lines = VGroup(
            wrapped_label(rf"a billion URLs: \ {c['bloom_bytes_1pct'] / 1e9:.1f} GB, \ in memory; \ a false positive "
                          r"is a page never fetched, \ and there are no false negatives, \ so none is fetched twice",
                          12.4, font_size=19, color=WHITE),
            wrapped_label(r"the same text at different URLs: \ SimHash \ (Charikar 2002, \ Part 20) \ gives similar "
                          r"pages fingerprints a few bits apart; \ Manku et al. \ (2007) \ used 64 bits, \ at most 3 "
                          r"differing, \ over 8 billion pages", 12.4, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(tab, DOWN, buff=0.3)
        with self.voiceover(
            "And the crawler must not fetch a page twice. <bookmark mark='a'/> The seen set is a Bloom filter, from "
            "Part 20: each URL sets a few bits, chosen by independent hashes. <bookmark mark='b'/> A new URL whose "
            "bits are all set is reported as seen, sometimes wrongly: these three were set by two other URLs. "
            "<bookmark mark='c'/> We measured our filter: two hundred thousand URLs at nine point six bits each and "
            "seven hashes gave one point zero zero five percent false positives, against zero point nine nine seven "
            "from the formula. <bookmark mark='d'/> For a billion URLs that is one point two gigabytes, in memory. A "
            "false positive costs a page never fetched; there are no false negatives, so nothing is fetched twice. "
            "<bookmark mark='e'/> Different URLs often serve the same text, so crawlers also fingerprint content. "
            "With Moses Charikar's SimHash, similar pages get fingerprints a few bits apart, and Gurmeet Manku and "
            "colleagues at Google reported in 2007 that sixty-four bits, at most three differing, worked across "
            "eight billion pages."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bits), FadeIn(vals), FadeIn(ill))
            vo.wait_until("a")
            for k in range(2):
                ar = hits(k)
                self.play(FadeIn(tags[k]), LaggedStart(*[GrowArrow(a) for a in ar], lag_ratio=0.2), run_time=1.0)
                idx, col = urls[k][1], urls[k][2]
                self.play(*[bits[i].animate.set_fill(col, opacity=0.6) for i in idx],
                          *[Transform(vals[i], mono("1", size=15, color=WHITE).move_to(bits[i])) for i in idx],
                          FadeOut(ar), run_time=0.7)
            vo.wait_until("b")
            ar = hits(2)
            self.play(FadeIn(tags[2]), LaggedStart(*[GrowArrow(a) for a in ar], lag_ratio=0.2), run_time=1.0)
            self.play(*[Indicate(bits[i], color=NO) for i in urls[2][1]], FadeIn(verdict))
            vo.wait_until("c")
            self.play(FadeOut(ar), FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]))
            vo.wait_until("e")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
