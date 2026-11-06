from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs48.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, load, module_box, tag_box, trace


def pct(x: float, d: int = 0) -> str:
    return f"{100 * x:.{d}f}"


class Caching(VoiceoverScene):
    def construct(self):
        self.card()
        self.where()
        self.patterns()
        self.evict()
        self.che()
        self.curve()

    def card(self):
        card = chapter_card(3, r"Caching: \ where, \ and what to keep", r"Which few answers deserve the fast memory?",
                            lit=(1966, 2017), extra=((1966, r"Belady: \ the optimal replacement"),
                                                     (2002, r"Che, \ Tung and Wang: \ the characteristic time"),
                                                     (2017, r"Einziger, \ Friedman and Manes: \ TinyLFU")),
                            part=PART)
        with self.voiceover("Chapter three. Caching: where, and what to keep."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def where(self):
        head = label(r"Where caches sit", font_size=36).to_edge(UP, buff=0.3)
        layers = [(r"browser", DATA, r"responses, \ as Cache-Control allows \ (Part 42)"),
                  (r"CDN edge", DATA, r"public responses, \ near the user"),
                  (r"reverse proxy", HEAD, r"whole responses, \ shared by many users"),
                  (r"application", YES, r"objects and query results: \ in process, \ Redis, \ Memcached"),
                  (r"database", LAM, r"pages of tables and indexes: \ the buffer pool"),
                  (r"storage", GREY_B, r"the data itself")]
        boxes = VGroup(*[module_box(n, c, w=1.85, h=0.7, font=19) for n, c, _ in layers]).arrange(RIGHT, buff=0.3)
        boxes.move_to([0, 0.6, 0])
        links = VGroup(*[Arrow(boxes[i][0].get_right(), boxes[i + 1][0].get_left(), buff=0.03, stroke_width=2,
                               color=GREY_B, max_tip_length_to_length_ratio=0.35) for i in range(5)])
        descs = VGroup(*[wrapped_label(d, 1.85, font_size=17, color=c).next_to(b, DOWN, buff=0.25)
                         for (_, c, d), b in zip(layers, boxes)])
        y = boxes.get_top()[1] + 0.35
        full = Dot([boxes[0].get_left()[0], y, 0], radius=0.09, color=GREY_A)
        hit = Dot([boxes[0].get_left()[0], y, 0], radius=0.09, color=YES)
        hl = label(r"a hit at the application: \ the rest of the trip is saved", font_size=19, color=YES).next_to(
            boxes, UP, buff=0.65)
        foot = wrapped_label(r"each hit ends the journey early; \ each layer is one more copy that can be stale \ "
                             r"(chapter 4)", 12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A cache keeps a copy of an answer closer to whoever asks, and there is room for one at every hop. "
            "<bookmark mark='a'/> The browser keeps responses, as Part 42's Cache-Control headers allow; a content "
            "delivery network keeps them at the edge, near the user. <bookmark mark='b'/> A reverse proxy keeps "
            "whole responses shared by many users. The application keeps objects and query results, in its own "
            "memory or in Redis or Memcached. <bookmark mark='c'/> And the database keeps pages of its tables and "
            "indexes in a buffer pool. <bookmark mark='d'/> Each hit ends the journey early; each layer is one "
            "more copy that can be stale."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.15), Create(links))
            self.play(FadeIn(full))
            self.play(full.animate.set_x(boxes[-1].get_x()), run_time=2.0, rate_func=linear)
            self.play(full.animate.set_x(boxes[0].get_left()[0]), run_time=1.5, rate_func=linear)
            self.play(FadeOut(full))
            vo.wait_until("a")
            self.play(FadeIn(descs[0]), FadeIn(descs[1]))
            vo.wait_until("b")
            self.play(FadeIn(descs[2]), FadeIn(descs[3]))
            vo.wait_until("c")
            self.play(FadeIn(descs[4]), FadeIn(descs[5]))
            vo.wait_until("d")
            self.play(FadeIn(hit))
            self.play(hit.animate.set_x(boxes[3].get_x()), run_time=1.0, rate_func=linear)
            self.play(hit.animate.set_x(boxes[0].get_left()[0]), FadeIn(hl), run_time=1.0, rate_func=linear)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def patterns(self):
        head = label(r"Four ways to wire a cache", font_size=36).to_edge(UP, buff=0.3)

        def mini(title, color, a1, a2, desc, at, curved=None, dashed=False):
            app = module_box(r"app", DATA, w=1.2, h=0.55, font=18).move_to([-2.4, 0, 0])
            cache = module_box(r"cache", YES, w=1.2, h=0.55, font=18).move_to([0, 0, 0])
            db = module_box(r"database", LAM, w=1.2, h=0.55, font=16).move_to([2.4, 0, 0])
            g = VGroup(app, cache, db)
            ar1 = Arrow(app[0].get_right(), cache[0].get_left(), buff=0.04, stroke_width=2.5, color=WHITE,
                        max_tip_length_to_length_ratio=0.25)
            g.add(ar1, label(a1, font_size=17, color=GREY_A).move_to([ar1.get_x(), 0.55, 0]))
            if a2 is not None:
                ar2 = Arrow(cache[0].get_right(), db[0].get_left(), buff=0.04, stroke_width=2.5, color=WHITE,
                            max_tip_length_to_length_ratio=0.25)
                if dashed:
                    ar2 = DashedLine(cache[0].get_right(), db[0].get_left(), buff=0.04, color=WHITE,
                                     dash_length=0.08).add_tip(tip_length=0.15)
                g.add(ar2, label(a2, font_size=17, color=GREY_A).move_to([ar2.get_x(), 0.55, 0]))
            if curved is not None:
                arc = CurvedArrow(app[0].get_bottom(), db[0].get_bottom(), angle=PI / 4, color=WHITE,
                                  stroke_width=2.5, tip_length=0.15)
                lc = label(curved, font_size=17, color=GREY_A).next_to(arc, DOWN, buff=0.06)
                g.add(arc, lc)
            t = label(title, font_size=23, color=color).move_to([0, 1.05, 0])
            d = wrapped_label(desc, 6.0, font_size=18, color=color).move_to([0, -1.3, 0])
            return VGroup(t, g, d).shift(at)
        aside = mini(r"cache-aside", DATA, r"1 get, \ 3 set", None,
                     r"writes: \ update the database, \ delete the cached copy", [-3.45, 1.15, 0],
                     curved=r"2 on a miss: \ read")
        through_r = mini(r"read-through", YES, r"1 get", r"2 miss: \ load",
                         r"the cache does the loading; \ the app sees one store", [3.45, 1.15, 0])
        through_w = mini(r"write-through", HEAD, r"1 write", r"2 write, \ then ack",
                         r"never stale; \ every write pays for both", [-3.45, -1.75, 0])
        back = mini(r"write-back", NO, r"1 write: \ ack at once", r"2 later, \ in batches",
                    r"fast writes; \ unwritten data is lost if the cache dies \ (Part 9)", [3.45, -1.75, 0],
                    dashed=True)
        grid = VGroup(aside, through_r, through_w, back)
        with self.voiceover(
            "There are four common ways to connect a cache to the data behind it. <bookmark mark='a'/> In "
            "cache-aside, the commonest, the application asks the cache, and on a miss reads the database and "
            "fills the cache itself; on a write it updates the database and deletes the cached copy. "
            "<bookmark mark='b'/> In read-through, the cache does the loading itself. <bookmark mark='c'/> "
            "Write-through sends each write through the cache to the database "
            "before acknowledging it: never stale, but every write is slower. <bookmark mark='d'/> Write-back "
            "acknowledges at once and writes the database later, as Part 9's processor caches do: fast, but what "
            "it has not yet written is lost if it fails."
        ) as vo:
            self.play(FadeIn(head))
            for mk, g in zip("abcd", grid):
                vo.wait_until(mk)
                self.play(FadeIn(g[0]), FadeIn(g[1]), FadeIn(g[2]))
        self.wait(0.4)
        self.clear_scene()

    def evict(self):
        s = load("scan")
        head = label(r"What to evict", font_size=36).to_edge(UP, buff=0.3)
        ill = note(r"illustrative entries", font_size=16).to_corner(UR, buff=0.35)
        # LRU: most recent on the left
        order = ["a", "b", "c", "d", "e"]
        lru = {k: tag_box(k, color=DATA, size=20, w=0.75, h=0.55) for k in order + ["f"]}
        lx0 = -6.2

        def place(seq):
            return [[lx0 + 0.375 + i * 0.95, 1.85, 0] for i in range(len(seq))]
        for k, p in zip(order, place(order)):
            lru[k].move_to(p)
        lt = label(r"\textbf{LRU}: \ most recent first", font_size=20, color=DATA).move_to([-3.85, 2.55, 0])
        lnote = wrapped_label(r"a hit moves an entry to the front; \ the back falls off; \ quick to adapt, \ but "
                              r"one pass over cold data flushes it", 5.8, font_size=18, color=WHITE).next_to(
            VGroup(*[lru[k] for k in order]), DOWN, buff=0.25).align_to([lx0, 0, 0], LEFT)
        counts = [9, 7, 4, 2, 1]
        lfu = VGroup(*[VGroup(tag_box(k, color=LAM, size=20, w=0.75, h=0.55),
                              label(f"{c}", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.08)
                       for k, c in zip("pqrst", counts)]).arrange(RIGHT, buff=0.2)
        lfu.move_to([3.5, 1.7, 0])
        ft = label(r"\textbf{LFU}: \ counts of use", font_size=20, color=LAM).move_to([3.5, 2.55, 0])
        fnote = wrapped_label(r"evict the least used; \ suits steady popularity, \ slow to forget yesterday's "
                              r"favourites", 5.8, font_size=18, color=WHITE).next_to(lfu, DOWN, buff=0.2).align_to(
            lfu, LEFT)
        # W-TinyLFU: window -> admission by the sketch -> main
        win = module_box(r"window LRU, \ 1\%", DATA, w=2.3, h=0.75, font=18).move_to([-5.2, -0.9, 0])
        gate = module_box(r"sketch: \ candidate used more than the victim?", HEAD, w=4.4, h=0.75,
                          font=18).move_to([-0.5, -0.9, 0])
        main = module_box(r"main LRU, \ 99\%", YES, w=2.3, h=0.75, font=18).move_to([4.6, -0.9, 0])
        a1 = Arrow(win[0].get_right(), gate[0].get_left(), buff=0.05, stroke_width=2.2, color=GREY_B)
        a2 = Arrow(gate[0].get_right(), main[0].get_left(), buff=0.05, stroke_width=2.2, color=YES)
        yes_l = label(r"yes: \ admit", font_size=16, color=YES).next_to(a2, UP, buff=0.08)
        no_l = label(r"no: \ drop the candidate", font_size=16, color=NO).next_to(gate, DOWN, buff=0.12).shift(
            RIGHT * 1.0)
        tt = label(r"\textbf{W-TinyLFU} \ (Einziger, \ Friedman and Manes)", font_size=20, color=HEAD).next_to(
            gate, UP, buff=0.3)
        cells = VGroup(*[Square(side_length=0.2, stroke_width=1, stroke_color=GREY_C) for _ in range(48)])
        cells.arrange_in_grid(rows=4, cols=12, buff=0.0).move_to([-5.2, -2.25, 0])
        lit = VGroup(*[cells[r * 12 + c].copy().set_fill(HEAD, 0.9) for r, c in ((0, 3), (1, 9), (2, 1), (3, 6))])
        ctext = wrapped_label(r"Count-Min sketch \ (Part 20): \ four counters per item, \ read the smallest; \ "
                              r"halved now and then, \ so it forgets", 4.6, font_size=17, color=GREY_A).next_to(
            cells, RIGHT, buff=0.3)
        scan = wrapped_label(rf"a one-off scan of 20,000 cold keys: \ LRU {pct(s['lru_clean'], 1)}\% $\to$ "
                             rf"{pct(s['lru'], 1)}\%, \ TinyLFU {pct(s['tinylfu_clean'], 1)}\% $\to$ "
                             rf"{pct(s['tinylfu'], 1)}\%; \ the scan's own misses explain nearly all of both drops "
                             r"\ (computed)", 12.4, font_size=18, color=GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "When the cache is full, something must go. <bookmark mark='a'/> LRU evicts the entry used least "
            "recently. It adapts quickly, but one pass over cold data flushes it. <bookmark mark='b'/> LFU evicts "
            "the entry used least often: good for steady popularity, slow to forget yesterday's favourites. "
            "<bookmark mark='c'/> W-TinyLFU, by Einziger, Friedman and Manes, combines them. New entries land in a "
            "small LRU window; one leaving it enters the main cache only if it has been used more than the main "
            "cache's victim, as counted by Part 20's Count-Min sketch, halved now and then so that it forgets. "
            "<bookmark mark='d'/> When we ran a one-off scan of cold keys, LRU's hot entries came straight back: "
            "nearly all the damage was the scan's own misses."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(lt), *[FadeIn(lru[k]) for k in order])
            new = ["d", "a", "b", "c", "e"]
            self.play(*[lru[k].animate.move_to(p) for k, p in zip(new, place(new))], run_time=0.8)
            lru["f"].move_to([lx0 + 0.375, 1.85, 0]).shift(UP * 0.4)
            new2 = ["f", "d", "a", "b", "c"]
            self.play(FadeOut(lru["e"], shift=RIGHT * 0.4),
                      *[lru[k].animate.move_to(p) for k, p in zip(new2[1:], place(new2)[1:])], run_time=0.8)
            self.play(lru["f"].animate.move_to(place(new2)[0]), FadeIn(lnote))
            vo.wait_until("b")
            self.play(FadeIn(ft), FadeIn(lfu))
            self.play(lfu[-1].animate.set_opacity(0.25), FadeIn(fnote))
            vo.wait_until("c")
            self.play(FadeIn(tt), FadeIn(win), Create(a1), FadeIn(gate))
            self.play(FadeIn(cells), FadeIn(ctext))
            self.play(LaggedStart(*[FadeIn(x) for x in lit], lag_ratio=0.2))
            self.play(Create(a2), FadeIn(yes_l), FadeIn(main), FadeIn(no_l))
            vo.wait_until("d")
            self.play(FadeIn(scan))
        self.wait(0.4)
        self.clear_scene()

    def che(self):
        c = load("caches")
        r1k = next(r for r in c["rows"] if r["size"] == 1000)
        head = label(r"Che's approximation", font_size=36).to_edge(UP, buff=0.3)
        seq = "abacadbaeabcafbaadabea"
        C = 4
        colors = {"a": DATA, "b": YES, "c": LAM, "d": KERN, "e": HEAD, "f": NO}
        boxes = VGroup(*[tag_box(ch, color=colors[ch], size=16, w=0.44, h=0.44) for ch in seq]).arrange(RIGHT,
                                                                                                    buff=0.08)
        boxes.move_to([0, 2.15, 0])
        # the longest recent span holding at most C distinct items: what an LRU of size C still holds
        seen, start = set(), len(seq)
        for i in range(len(seq) - 1, -1, -1):
            if seq[i] not in seen and len(seen) == C:
                break
            seen.add(seq[i])
            start = i
        span = boxes[start:]
        br = Brace(span, DOWN, buff=0.1, color=HEAD)
        bl = label(rf"the last $T$ requests: \ exactly $C = {C}$ distinct items, \ the cache's contents",
                   font_size=18, color=HEAD).next_to(br, DOWN, buff=0.08).align_to(span, RIGHT)
        tl = label(r"requests, \ oldest to newest \ (illustrative)", font_size=16, color=GREY_B).next_to(
            boxes, UP, buff=0.12).align_to(boxes, LEFT)
        eqs = VGroup(
            MathTex(r"P(i \text{ cached}) \approx 1 - (1 - p_i)^T \approx 1 - e^{-p_i T}", font_size=34),
            MathTex(r"\sum_i \left(1 - e^{-p_i T}\right) = C", font_size=34),
            MathTex(r"h = \sum_i p_i \left(1 - e^{-p_i T}\right)", font_size=34, color=YES),
        )
        whys = VGroup(
            wrapped_label(r"item $i$ is a fraction $p_i$ of requests: \ the chance it was asked for in the last $T$",
                          5.2, font_size=18, color=GREY_A),
            wrapped_label(r"the cache holds $C$ items: \ one equation that fixes $T$, \ the \textbf{characteristic "
                          r"time}, \ assumed nearly constant", 5.2, font_size=18, color=GREY_A),
            wrapped_label(r"a request for $i$ hits exactly when $i$ is cached", 5.2, font_size=18, color=GREY_A),
        )
        lines = VGroup(*[VGroup(e, w) for e, w in zip(eqs, whys)])
        for e, w in zip(eqs, whys):
            e.move_to([-2.7, 0, 0])
            w.move_to([4.1, 0, 0]).align_to([1.5, 0, 0], LEFT)
        for k, ln in enumerate(lines):
            ln.set_y(0.0 - k * 1.05)
        foot = wrapped_label(rf"at {r1k['size']:,} entries: \ simulated LRU {pct(r1k['lru'], 1)}\%, \ the formula "
                             rf"{pct(r1k['che'], 1)}\% \ (computed)", 12.4, font_size=20, color=YES).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "How large must a cache be? In 2002 Che, Tung and Wang gave LRU a formula. <bookmark mark='a'/> An LRU "
            "cache of C entries holds exactly the items of the most recent stretch of requests in which C "
            "different items appear. Call its length T, and assume that it hardly varies: that is the "
            "approximation. <bookmark mark='b'/> If item i is a fraction p i of requests, it was missed by all T "
            "with probability one minus p i to the T, about e to the minus p i T. <bookmark mark='c'/> The cache "
            "holds C items, so the chances of being cached add up to C, which fixes T. <bookmark mark='d'/> A "
            "request hits when its item is cached, so the hit rate is the sum of p i times that chance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tl), LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(GrowFromCenter(br), FadeIn(bl))
            vo.wait_until("b")
            self.play(Write(eqs[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(Write(eqs[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(Write(eqs[2]), FadeIn(whys[2]))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def curve(self):
        c = load("caches")
        rows = c["rows"]
        by = {r["size"]: r for r in rows}
        head = label(r"Hit rate against size", font_size=36).to_edge(UP, buff=0.3)
        g = axes([2, 4, 1], [0, 0.8, 0.2], x_length=7.0, y_length=4.4, x_label=r"cache size \ (entries, \ log scale)",
                 y_label=r"hit rate", xticks=[2, 3, 4], yticks=[0, 0.2, 0.4, 0.6, 0.8],
                 fx=lambda v: f"{10 ** v:,.0f}", fy=lambda v: rf"{100 * v:.0f}\%", font=16)
        g.move_to([-2.6, -0.35, 0])
        ax = g.ax

        def series(key, color, dots=True, dash=False, width=2.5):
            pts = [(math.log10(r["size"]), r[key]) for r in rows]
            ln = trace(ax, pts, color, width=width)
            if dash:
                ln = DashedVMobject(ln, num_dashes=40)
            ds = VGroup(*[Dot(ax.c2p(x, y), radius=0.07, color=color) for x, y in pts]) if dots else VGroup()
            return VGroup(ln, ds)
        lru = series("lru", DATA)
        che = series("che", WHITE, dots=False, width=2)
        lfu = series("lfu", LAM)
        tiny = series("tinylfu", YES)
        opt = series("optimal_static", HEAD, dots=False, dash=True)
        legend = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.45, color=cl, stroke_width=3),
                                 label(t, font_size=18, color=cl)).arrange(RIGHT, buff=0.15)
                          for t, cl in ((r"LRU, \ simulated", DATA), (r"Che's formula", WHITE),
                                        (r"LFU", LAM), (r"W-TinyLFU", YES),
                                        (r"best fixed set: \ the most popular items", HEAD))])
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        legend.move_to([0, 1.55, 0]).align_to([1.7, 0, 0], LEFT)
        err = max(abs(r["lru"] - r["che"]) for r in rows)
        notes = VGroup(
            wrapped_label(rf"{c['items']:,} items, \ Zipf popularity \ ($s = {c['zipf_s']}$), \ {c['requests']:,} "
                          r"requests; \ computed", 5.0, font_size=18, color=GREY_B),
            wrapped_label(rf"Che against simulation: \ within {100 * err:.1f} percentage points at every size", 5.0,
                          font_size=19, color=WHITE),
            wrapped_label(rf"1\% of the catalogue \ ({1000:,} entries) \ serves {pct(by[1000]['lru'])}\% "
                          rf"\ (LRU) \ to {pct(by[1000]['tinylfu'])}\% \ (TinyLFU) \ of requests", 5.0, font_size=19,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(legend, DOWN, buff=0.4).align_to(legend, LEFT)
        mark = DashedLine(ax.c2p(3, 0), ax.c2p(3, 0.8), color=GREY_B, dash_length=0.08)
        r1, r4 = by[rows[0]["size"]], by[rows[-1]["size"]]
        with self.voiceover(
            f"Now the measurement: a catalogue of {c['items']:,} items with Zipf popularity "
            f"and {c['requests']:,} requests. <bookmark mark='a'/> LRU's hit rate climbs steadily as the "
            f"cache grows tenfold, and tenfold again: {pct(r1['lru'])} percent at {r1['size']} entries, "
            f"{pct(by[1000]['lru'])} at a thousand, {pct(r4['lru'])} at ten thousand. <bookmark mark='b'/> Che's "
            "formula lies on top of it, within half a percentage point at every size. <bookmark mark='c'/> "
            f"Frequency does better: TinyLFU and LFU reach {pct(by[1000]['tinylfu'])} and "
            f"{pct(by[1000]['lfu'])} percent at a thousand entries, close to the best fixed set, the thousand most "
            f"popular items, at {pct(by[1000]['optimal_static'])}. <bookmark mark='d'/> So one percent of the "
            "catalogue serves over a third of the requests, and the formula gives the size before you buy the "
            "memory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(lru[0]), LaggedStart(*[FadeIn(d) for d in lru[1]], lag_ratio=0.3), FadeIn(legend[0]),
                      run_time=2)
            vo.wait_until("b")
            self.play(Create(che[0]), FadeIn(legend[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(lfu[0]), FadeIn(lfu[1]), Create(tiny[0]), FadeIn(tiny[1]), FadeIn(legend[2]),
                      FadeIn(legend[3]))
            self.play(Create(opt[0]), FadeIn(legend[4]))
            vo.wait_until("d")
            self.play(Create(mark), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, NO)
