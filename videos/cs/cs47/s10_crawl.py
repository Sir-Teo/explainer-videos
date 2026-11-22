from __future__ import annotations

import hashlib
import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono, module_box,
                                   tag_box, timeline_bar)


def h64(s: str) -> int:
    """The 64-bit shingle hash of the instrument (explainer/cs/search/links.py)."""
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), "big")


class Crawl(WatchScene):
    def construct(self):
        self.card()
        self.loop()
        self.frontier()
        self.simhash()
        self.scale()

    def card(self):
        self.chapter(9, r"Crawling the web", r"How do you keep a copy of the web, \ and keep it fresh?", lit=(1994, 2002), extra=((1994, r"Koster: \ robots.txt"), (1999, r"Heydon and Najork: \ Mercator"),
                                   (2002, r"Charikar: \ SimHash")), part=PART, said="Chapter nine. Crawling the web.")

    def loop(self):
        head = label(r"The crawl loop", font_size=36).to_edge(UP, buff=0.3)
        w, h = 2.7, 0.75
        spec = {"frontier": (r"frontier", HEAD, -4.9, 1.4), "fetch": (r"fetch: \ DNS, robots.txt", KERN, -1.6, 1.4),
                "parse": (r"parse", DATA, 1.7, 1.4), "dup": (r"content seen? \ (fingerprint)", LAM, 4.9, 1.4),
                "index": (r"to the indexer", YES, 4.9, -0.4), "norm": (r"normalise links", DATA, 1.7, -0.4),
                "seen": (r"URL seen? \ (hash set)", LAM, -1.6, -0.4)}
        box = {k: module_box(t, c, w=w, h=h, font=17).move_to([x, y, 0]) for k, (t, c, x, y) in spec.items()}

        def arr(a, b, sa=RIGHT, sb=LEFT):
            return Arrow(box[a].get_edge_center(sa), box[b].get_edge_center(sb), buff=0.08, stroke_width=2.5,
                         color=GREY_B, max_tip_length_to_length_ratio=0.15)
        arrows = VGroup(arr("frontier", "fetch"), arr("fetch", "parse"), arr("parse", "dup"),
                        arr("dup", "index", DOWN, UP), arr("parse", "norm", DOWN, UP), arr("norm", "seen", LEFT, RIGHT),
                        Arrow(box["seen"].get_edge_center(LEFT), box["frontier"].get_edge_center(DOWN), buff=0.08,
                              stroke_width=2.5, color=YES, max_tip_length_to_length_ratio=0.1))
        newl = label(r"new", font_size=16, color=YES).next_to(arrows[-1].get_center(), DOWN + LEFT, buff=0.05)
        tok = tag_box(r"novels.example/ch1", color=HEAD, size=14).next_to(box["frontier"], UP, buff=0.15)
        path = [box["frontier"], box["fetch"], box["parse"], box["norm"], box["seen"]]
        lines = VGroup(
            wrapped_label(r"\textbf{normalise}: \ lower-case the host, \ drop the default port and the "
                          r"\texttt{\#fragment}, \ resolve relative paths, \ so that one page has one address", 12.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"the seen-URL test is a hash set of fingerprints \ (Part 17); \ the content test keeps "
                          r"copies out of the index", 12.4, font_size=19, color=LAM),
            wrapped_label(r"Heydon and Najork's \textbf{Mercator} \ (1999) \ set this design out in modules; \ "
                          r"crawlers must also escape traps, \ like a calendar linking to the next day forever", 12.4,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Before anything can be indexed, it must be fetched. <bookmark mark='a'/> A crawler starts from seed "
            "addresses in a frontier. It takes one, looks up the host, checks the site's robots dot t x t, downloads "
            "the page and parses it. <bookmark mark='b'/> Each link found is normalised, so that one page has one "
            "address, and tested against the addresses already seen, a hash set of fingerprints as in Part 17. New "
            "ones join the frontier. <bookmark mark='c'/> The text is fingerprinted too, so copies are not indexed "
            "twice. Heydon and Najork's Mercator set this design out in 1999. Crawlers must also escape traps, like a"
            " calendar linking to the next day, forever."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(b) for b in box.values()])
            vo.wait_until("a")
            self.play(Create(arrows[0]), Create(arrows[1]), FadeIn(tok))
            for b in path[1:3]:
                self.play(tok.animate.next_to(b, UP, buff=0.15), run_time=0.8)
            vo.wait_until("b")
            self.play(Create(arrows[4]), Create(arrows[5]), Create(arrows[6]), FadeIn(newl), FadeIn(lines[0]))
            self.play(tok.animate.next_to(box["norm"], DOWN, buff=0.2), run_time=0.7)
            self.play(tok.animate.next_to(box["seen"], DOWN, buff=0.2), run_time=0.7)
            self.play(tok.animate.next_to(box["frontier"], UP, buff=0.15), FadeIn(lines[1]), run_time=0.8)
            vo.wait_until("c")
            self.play(Create(arrows[2]), Create(arrows[3]), Indicate(box["dup"], color=LAM))
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def frontier(self):
        head = label(r"The frontier: \ priority and politeness", font_size=36).to_edge(UP, buff=0.3)
        hosts = {"a": DATA, "b": LAM, "c": KERN}
        front = [["a/4", "c/9", "b/2"], ["b/7", "a/1"], ["c/3", "a/8"]]
        ys = [1.75, 1.05, 0.35]
        fq, fl, toks = VGroup(), VGroup(), {}
        for k, (row, y) in enumerate(zip(front, ys)):
            r = Rectangle(width=3.0, height=0.5, stroke_color=GREY_C, stroke_width=1.5).move_to([-4.0, y, 0])
            fq.add(r)
            fl.add(label(rf"priority {k + 1}", font_size=16, color=GREY_A).next_to(r, LEFT, buff=0.12))
            for j, u in enumerate(row):
                toks[u] = tag_box(u, color=hosts[u[0]], size=14, w=0.8, h=0.36).move_to(
                    [r.get_left()[0] + 0.5 + j * 0.95, y, 0])
        ftitle = label(r"front queues: \ what matters most", font_size=18, color=HEAD).next_to(fq, UP, buff=0.18)
        bq, bl = VGroup(), VGroup()
        for k, (hname, c) in enumerate(hosts.items()):
            r = Rectangle(width=3.0, height=0.5, stroke_color=c, stroke_width=1.5).move_to([1.0, ys[k], 0])
            bq.add(r)
            bl.add(label(rf"\texttt{{{hname}.example}}", font_size=16, color=c).next_to(r, LEFT, buff=0.12))
        btitle = label(r"back queues: \ one per host", font_size=18, color=YES).next_to(bq, UP, buff=0.18)
        heap_rows = [["c.example", "0.2 s"], ["a.example", "0.5 s"], ["b.example", "1.4 s"]]
        heap = grid_table([r"host", r"may fetch at"], heap_rows, widths=[1.9, 1.6], row_h=0.42, font_size=17,
                          mono_cols=(0,))
        heap.move_to([5.0, 1.0, 0])
        heap2 = grid_table([r"host", r"may fetch at"], heap_rows[1:] + [["c.example", "2.2 s"]], widths=[1.9, 1.6],
                           row_h=0.42, font_size=17, mono_cols=(0,)).move_to(heap)
        htitle = label(r"a heap of hosts, \ earliest first", font_size=18, color=KERN).next_to(heap, UP, buff=0.18)
        ill = label(r"illustrative", font_size=16, color=GREY_B).next_to(heap, DOWN, buff=0.15)
        lines = VGroup(
            wrapped_label(r"\textbf{priority}: \ important and fast-changing pages first \ (Mercator's front "
                          r"queues)", 12.4, font_size=19, color=HEAD),
            wrapped_label(r"\textbf{politeness}: \ one connection per host, \ and a pause before the next; \ a "
                          r"common rule waits about ten times as long as the last fetch from that host took \ "
                          r"(Manning, Raghavan and Sch\"utze)", 12.4, font_size=19, color=YES),
            wrapped_label(r"\texttt{robots.txt} \ (Koster, 1994; \ RFC 9309, 2022) \ lists the paths a site asks "
                          r"crawlers not to fetch", 12.4, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        order = ["a/4", "c/9", "b/2", "b/7", "a/1", "c/3", "a/8"]
        slot = {"a": 0, "b": 0, "c": 0}
        moves = []
        for u in order:
            k = list(hosts).index(u[0])
            moves.append(toks[u].animate.move_to([bq[k].get_left()[0] + 0.5 + slot[u[0]] * 0.95, ys[k], 0]))
            slot[u[0]] += 1
        with self.voiceover(
            "The frontier decides what to fetch next, and it serves two masters. <bookmark mark='a'/> Priority: "
            "important and fast-changing pages first, held in Mercator's front queues. <bookmark mark='b'/> And "
            "politeness: never hammer one server. Back queues hold one host each, and a heap records when each host "
            "may next be contacted. A common rule, in Manning, Raghavan and Schütze's textbook, waits about ten times"
            " as long as the last fetch from that host took. <bookmark mark='c'/> Sites also state their wishes. "
            "Martijn Koster's robots exclusion convention of 1994 lists paths a crawler should leave alone; in 2022 "
            "it became an internet standard, RFC nine three oh nine. A polite crawler fetches from thousands of hosts"
            " at once, and from each one slowly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fq), FadeIn(fl), FadeIn(ftitle), *[FadeIn(t) for t in toks.values()])
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), Indicate(fq[0], color=HEAD))
            vo.wait_until("b")
            self.play(FadeIn(bq), FadeIn(bl), FadeIn(btitle))
            self.play(LaggedStart(*moves, lag_ratio=0.25), run_time=2.5)
            self.play(FadeIn(heap), FadeIn(htitle), FadeIn(ill), FadeIn(lines[1]))
            self.play(Indicate(heap.cells[1][0], color=KERN), toks["c/9"].animate.shift(RIGHT * 3.6).set_opacity(0),
                      run_time=1.0)
            self.play(Transform(heap, heap2), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()


    def simhash(self):
        self.ask(r"Change a few words of a passage. \\ Its SimHash fingerprint changes...", [r"completely",
                 r"in a few bits"], 1,
                 say="Change a few words of a passage. How much does its SimHash fingerprint change?",
                 reveal="In a few bits. Near-duplicates have nearby fingerprints.")
        head = label(r"SimHash: \ a fingerprint that bends", font_size=36).to_edge(UP, buff=0.3)
        words = "call me ishmael some years ago never".split()
        sh = [" ".join(words[i:i + 3]) for i in range(len(words) - 2)]
        nb, cell = 12, 0.42
        x0, y0 = -0.6, 2.1
        bits = [[h64(s) >> b & 1 for b in range(nb)] for s in sh]
        grid, names = VGroup(), VGroup()
        for i, (s, row) in enumerate(zip(sh, bits)):
            y = y0 - i * 0.5
            names.add(mono(s, size=14, color=DATA).next_to([x0 - 0.2, y, 0], LEFT, buff=0))
            for b, v in enumerate(row):
                sq = Square(cell * 0.92, stroke_color=GREY_C, stroke_width=1, fill_color=YES if v else NO,
                            fill_opacity=0.5).move_to([x0 + (b + 0.5) * cell, y, 0])
                grid.add(VGroup(sq, mono(str(v), size=13, color=WHITE).move_to(sq)))
        sums = [sum(1 if r[b] else -1 for r in bits) for b in range(nb)]
        ys = y0 - len(sh) * 0.5 - 0.15
        srow = VGroup(*[label(f"{s:+d}", font_size=17, color=HEAD).move_to([x0 + (b + 0.5) * cell, ys, 0])
                        for b, s in enumerate(sums)])
        sl = label(r"sum of $\pm 1$", font_size=17, color=HEAD).next_to([x0 - 0.2, ys, 0], LEFT, buff=0)
        yf = ys - 0.55
        frow = VGroup(*[VGroup(Square(cell * 0.92, stroke_color=YES, stroke_width=2, fill_color=YES if s > 0 else BG,
                                      fill_opacity=0.8 if s > 0 else 1),
                               mono("1" if s > 0 else "0", size=13, color=BLACK if s > 0 else WHITE)).move_to(
            [x0 + (b + 0.5) * cell, yf, 0]) for b, s in enumerate(sums)])
        for g in frow:
            g[1].move_to(g[0])
        fl = label(r"fingerprint: \ the signs", font_size=17, color=YES).next_to([x0 - 0.2, yf, 0], LEFT, buff=0)
        cap = label(rf"three-word shingles; \ the first {nb} of 64 bits of each hash", font_size=16,
                    color=GREY_B).next_to(grid, UP, buff=0.15).align_to(grid, LEFT)
        lines = VGroup(
            wrapped_label(r"a small edit changes a few shingles, \ which rarely flips the sign of a sum", 12.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"Charikar \ (2002): \ each bit says on which side of a random hyperplane the document's "
                          r"vector of shingles lies \ (Part 20)", 12.4, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Much of the web is copied: mirrors, syndicated articles, pages that differ only in an advertisement. "
            "<bookmark mark='a'/> Moses Charikar's SimHash, of 2002, makes a fingerprint that changes a little when "
            "the text does. Cut the text into overlapping three-word shingles, and hash each one to sixty-four bits. "
            "<bookmark mark='b'/> For each bit position, add one for every shingle with a one there, and subtract one"
            " for every zero. <bookmark mark='c'/> The fingerprint keeps the signs. A small edit changes a few "
            "shingles, which rarely flips a sign. <bookmark mark='d'/> It is Part 20's random-hyperplane sketch: each"
            " bit says on which side of a random hyperplane the document's vector of shingles lies."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(names), FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(sl), LaggedStart(*[FadeIn(s) for s in srow], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(fl), LaggedStart(*[FadeIn(f) for f in frow], lag_ratio=0.1), FadeIn(lines[0]),
                      run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def scale(self):
        s = load("simhash")
        head = label(r"Near-duplicates at scale", font_size=36).to_edge(UP, buff=0.3)
        rows = [[f"{r['edits']}", f"{r['mean_bits']:.1f}", f"{r['max_bits']}"] for r in s["rows"]]
        rows.append([r"unrelated", f"{s['unrelated_mean']:.1f}", rf"min {s['unrelated_min']}"])
        tab = grid_table([r"words replaced", r"mean bits", r"max bits"], rows, widths=[2.4, 1.6, 1.6], row_h=0.42,
                         font_size=19, mono_cols=())
        tab.move_to([-4.0, 0.7, 0])
        for c in tab.cells[-1]:
            c.set_color(NO)
        tcap = wrapped_label(r"bits that differ between 64-bit fingerprints of a 400-word passage and a copy "
                             r"with words replaced at random; \ 200 passages", 5.4, font_size=16,
                             color=GREY_B).next_to(tab, UP, buff=0.2).align_to(tab, LEFT)
        # the pigeonhole: two fingerprints that differ in three bits, cut into four blocks of sixteen
        cw = 0.088
        x0, ya, yb = 0.9, 1.15, 0.6
        diff = {5, 40, 57}
        cells = VGroup()
        for y in (ya, yb):
            for b in range(64):
                bad = b in diff and y == yb
                cells.add(Rectangle(width=cw * 0.8, height=0.42, stroke_width=0, fill_color=NO if bad else GREY_C,
                                    fill_opacity=0.9 if bad else 0.5).move_to([x0 + (b + 0.5) * cw, y, 0]))
        blocks = VGroup(*[Rectangle(width=16 * cw, height=1.05, stroke_color=YES if k == 1 else GREY_B,
                                    stroke_width=3 if k == 1 else 1.2).move_to([x0 + (k * 16 + 8) * cw,
                                                                               (ya + yb) / 2, 0])
                          for k in range(4)])
        pl = label(r"two fingerprints, \ 3 bits apart \ (illustrative)", font_size=16, color=GREY_A).next_to(
            blocks, UP, buff=0.15).align_to(blocks, LEFT)
        spoilt = {b // 16 for b in diff}
        verdict = VGroup(*[label(r"differs" if k in spoilt else r"agrees", font_size=17,
                                 color=NO if k in spoilt else YES).next_to(blocks[k], DOWN, buff=0.15)
                           for k in range(4)])
        ok = label(r"one block of 16 bits matches exactly", font_size=18, color=YES).next_to(verdict, DOWN,
                                                                                           buff=0.2)
        lines = VGroup(
            wrapped_label(rf"unrelated passages differ in about half of 64 bits; \ the closest of the unrelated "
                          rf"pairs differed in {s['unrelated_min']}", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"Manku, Jain and Das Sarma \ (Google, 2007): \ 64 bits, \ near-duplicates within "
                          r"\textbf{3 bits}, \ 8 billion pages", 12.4, font_size=19, color=HEAD),
            wrapped_label(r"3 differing bits spoil at most 3 of 4 blocks: \ one block agrees exactly, \ so one "
                          r"exact lookup per block, \ in 4 sorted tables, \ finds every candidate", 12.4,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How well does it work on the novels? <bookmark mark='a'/> We fingerprinted two hundred passages and "
            "replaced words at random. One replaced word moves two point four bits on average; eighty words, a fifth "
            "of the passage, about twenty. Unrelated passages differ in about thirty-two bits, half of sixty-four, "
            "and the closest unrelated pair in twenty-two. <bookmark mark='b'/> Manku, Jain and Das Sarma, at Google "
            "in 2007, found three bits a good threshold for eight billion pages. To search quickly, cut the "
            "fingerprints into four blocks of sixteen bits. <bookmark mark='c'/> Three differing bits spoil at most "
            "three blocks, so one block agrees exactly, and an exact lookup per block, in four sorted tables, finds "
            "every candidate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tcap), FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]),
                      FadeIn(tab.cells[0][2]), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=2.5)
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(cells), FadeIn(pl), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(Create(blocks))
            self.play(FadeIn(verdict), FadeIn(ok), FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, math)
