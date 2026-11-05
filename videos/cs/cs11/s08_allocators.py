from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bar_chart, grid_table, load)

POL = {"first fit": (DATA, r"the lowest-addressed free block that fits"),
       "next fit": (CTRL, r"the same, \ searching on from where the last search stopped"),
       "best fit": (YES, r"the smallest free block that fits"),
       "segregated fits": (FUNC, r"a free list per size class; \ search the request's class first"),
       "buddy": (NO, r"only power-of-two blocks: \ split in halves, \ merge with your ``buddy''")}


class Allocators(VoiceoverScene):
    def construct(self):
        self.card()
        self.policies()
        self.results()
        self.buddy()
        self.real()

    def card(self):
        card = chapter_card(7, r"Five allocators, \ one real trace", r"Which free block should a request get?",
                            part=PART)
        with self.voiceover("Chapter seven. Five allocators, one real trace."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def policies(self):
        head = label(r"Which free block?", font_size=36).to_edge(UP, buff=0.35)
        rows = VGroup(*[VGroup(label(n, font_size=24, color=c), label(d, font_size=21, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for n, (c, d) in POL.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        for r in rows:
            r[1].align_to([-1.6, 0, 0], LEFT)
            r[0].align_to([-5.8, 0, 0], LEFT)
        rows.move_to(DOWN * 1.15)
        # one request, five answers: a small heap with four holes
        items = [(None, 0.6), (96, 0), (None, 0.6), (48, 0), (None, 0.6), (32, 0), (None, 0.6), (160, 0),
                 (None, 0.6)]
        strip, holes = VGroup(), {}
        for sz, w in items:
            ww = w if sz is None else sz / 40
            r = Rectangle(width=ww, height=0.6, stroke_color=GREY_B, stroke_width=1.2,
                          fill_color=DATA if sz is None else GREY_E, fill_opacity=0.45 if sz is None else 0.2)
            strip.add(r)
            if sz:
                holes[sz] = r
        strip.arrange(RIGHT, buff=0).move_to(UP * 1.55)
        for sz, r in holes.items():
            strip.add(label(rf"{sz}", font_size=18, color=GREY_A).move_to(r))
        req = label(r"a request for 40 bytes:", font_size=21, color=HEAD).next_to(strip, UP, buff=0.55).align_to(
            strip, LEFT)
        rover = VGroup(Triangle(color=CTRL, fill_opacity=1).scale(0.08).rotate(PI),
                       label(r"last stop", font_size=15, color=CTRL)).arrange(UP, buff=0.05)
        rover.next_to(holes[160], UP, buff=0.05).align_to(holes[160], LEFT)
        picks = {"first fit": 96, "next fit": 160, "best fit": 48, "segregated fits": 48}
        marks = VGroup()
        for k, (name, sz) in enumerate(picks.items()):
            c = POL[name][0]
            under = [n for n, z in picks.items() if z == sz].index(name)
            marks.add(VGroup(Dot(radius=0.07, color=c), label(name, font_size=15, color=c)).arrange(RIGHT, buff=0.08)
                      .next_to(holes[sz], DOWN, buff=0.08 + 0.26 * under))
        bud = label(r"buddy: \ rounds 40 up to a 64-byte block", font_size=15, color=NO).next_to(strip, UP,
                                                                                               buff=0.55)
        bud.align_to(strip, RIGHT)
        marks.add(bud)
        rows.next_to(VGroup(strip, marks), DOWN, buff=0.45)
        sim = note(r"all five simulated in Python on the same heap rules: \ 8-byte headers, \ 16-byte alignment, \ "
                   r"immediate coalescing", font_size=17).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "When several free blocks would do, which should a request get? <bookmark mark='a'/> First fit takes "
            "the first one it finds, in address order. Next fit does the same but starts each search where the last "
            "one stopped, so it does not keep re-scanning the front. Best fit takes the smallest block that fits, "
            "leaving the biggest pieces intact. Segregated fits keeps a separate list for each size class and looks "
            "in the request's own class first. And the buddy system allows only blocks whose sizes are powers of "
            "two, which makes splitting and merging almost free. <bookmark mark='b'/> We implemented all five on the "
            "same simulated heap and replayed Perl's trace through each."
        ) as vo:
            self.play(FadeIn(head), FadeIn(req), FadeIn(strip), FadeIn(rover))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r, shift=RIGHT * 0.1), FadeIn(m)) for r, m in
                                    zip(rows, marks)], lag_ratio=0.5), run_time=6)
            vo.wait_until("b")
            self.play(FadeIn(sim))
        self.wait(0.3)
        self.clear_scene()

    def results(self):
        h = load("heap")
        rows = h["rows"]
        head = label(r"Perl's trace, \ replayed", font_size=34).to_edge(UP, buff=0.3)
        frag = [r["fragmentation"] for r in rows]
        ch = bar_chart(frag, [r["name"] for r in rows], [POL[r["name"]][0] for r in rows], height=3.0, bar_w=0.9,
                       gap=0.7, vmax=2.0, fmt_=lambda v: f"{v:.2f}", font_size=19).to_edge(LEFT, buff=0.8).shift(
            DOWN * 0.4)
        cl = label(r"heap needed \ $\div$ \ the most bytes ever live", font_size=18, color=GREY_B).next_to(ch, UP,
                                                                                                         buff=0.2)
        y0 = ch.bars[0].get_bottom()[1]
        one = DashedLine([ch.get_left()[0], y0 + 1.5, 0], [ch.get_right()[0], y0 + 1.5, 0], color=GREY_B)
        ol = label(r"1: \ perfect", font_size=16, color=GREY_B).next_to(one, RIGHT, buff=0.1)
        steps = VGroup(label(r"blocks examined \\ per \texttt{malloc}", font_size=18, color=GREY_B))
        for r in rows:
            steps.add(label(rf"{r['name']}: \ {r['steps']:.1f}", font_size=20, color=POL[r["name"]][0]))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.7).shift(DOWN * 0.3)
        best = rows[0]
        punch = label(rf"peak live {best['peak_live'] / 1e6:.2f} MB: \ first fit needs "
                      rf"{best['peak_heap'] / 1e6:.2f} MB, \ the buddy system {rows[-1]['peak_heap'] / 1e6:.2f} MB",
                      font_size=21, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here are the results. <bookmark mark='a'/> The measure is fragmentation: the heap each allocator "
            "needed, divided by the most bytes the program ever had live at once. One would be perfect. <bookmark "
            "mark='b'/> First fit, best fit and segregated fits all land at about one point one three: thirteen "
            "percent overhead, most of it headers and rounding on Perl's tiny blocks, not wasted holes. Next fit is "
            "a little worse. The buddy system needs nearly eighty percent more, because rounding every request up to "
            "a power of two wastes a quarter of each block on average. <bookmark mark='c'/> Speed is a different "
            "story. Next fit, meant to be fast, examines seventeen blocks per request on this trace; segregated "
            "fits examines fewer than one, because the right list is usually non-empty at its head. <bookmark "
            "mark='d'/> That combination, little waste and almost no searching, is why real allocators are built "
            "on size classes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch[0]), FadeIn(ch.names), FadeIn(cl), Create(one), FadeIn(ol))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(b, DOWN) for b in ch.bars], FadeIn(ch.vals))
            vo.wait_until("c")
            self.play(FadeIn(steps))
            vo.wait_until("d")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()

    def buddy(self):
        head = label(r"The buddy system \ (Knowlton, \ 1965)", font_size=34).to_edge(UP, buff=0.3)
        lv = VGroup()
        x0 = -5.0
        scale = 1.3
        r0 = Rectangle(width=8 * scale, height=0.5, stroke_color=GREY_B).move_to([x0 + 4 * scale, 1.6, 0])
        t0 = label(r"256 bytes", font_size=17, color=GREY_B).move_to(r0)
        rows = [[(0, 4, "free"), (4, 4, "free")], [(0, 2, ""), (2, 2, "free")], [(0, 1, "used: 30 B"),
                                                                                    (1, 1, "free")]]
        y = 0.9
        for row in rows:
            g = VGroup()
            for s, w, t in row:
                r = Rectangle(width=w * scale, height=0.5, stroke_color=GREY_B,
                              fill_color=DATA if "used" in t else GREY_E,
                              fill_opacity=0.4 if "used" in t else 0.2).move_to([x0 + (s + w / 2) * scale, y, 0])
                g.add(VGroup(r, label(t or rf"{int(32 * w)} B", font_size=15, color=WHITE).move_to(r)))
            lv.add(g)
            y -= 0.7
        pts = VGroup(
            label(r"a request for 30 bytes: \ split 256 into halves until a 32-byte block fits", font_size=21,
                  color=GREY_A),
            label(r"a block's buddy is at its address $\oplus$ its size: \ one XOR finds it", font_size=21,
                  color=HEAD),
            label(r"free: \ if the buddy is free too, \ merge, \ and try again one level up", font_size=21,
                  color=GREY_A),
            label(r"fast and simple, \ but a 33-byte request takes 64: \ internal fragmentation", font_size=21,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The buddy system, from Kenneth Knowlton in 1965, trades space for simplicity. <bookmark mark='a'/> "
            "Every block is a power of two. A request for thirty bytes splits a block in half, and in half again, "
            "until a thirty-two-byte block fits. <bookmark mark='b'/> Each half's partner, its buddy, sits at its "
            "own address with one bit flipped, the bit of the block's size, so a single exclusive-or finds it. "
            "<bookmark mark='c'/> When a block is freed and its buddy is free too, the two merge into their parent, "
            "and the check repeats one level up. <bookmark mark='d'/> All of this is fast. The cost is rounding: a "
            "request of thirty-three bytes gets sixty-four. Waste inside a block is internal fragmentation; waste "
            "between blocks, which first fit suffers from, is external."
        ) as vo:
            self.play(FadeIn(head), FadeIn(r0), FadeIn(t0))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            for g in lv:
                self.play(FadeIn(g, shift=DOWN * 0.1), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(pts[1]), Indicate(lv[2][1], color=HEAD))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def real(self):
        head = label(r"What real allocators do", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"glibc's \texttt{malloc} \ (ptmalloc, \ after Doug Lea's dlmalloc): \ size-class bins, \ boundary "
                  r"tags, \ coalescing", font_size=21, color=DATA),
            label(r"jemalloc, \ tcmalloc, \ mimalloc: \ size classes in pages of equal blocks, \ and a cache per "
                  r"thread", font_size=21, color=YES),
            label(r"big requests skip the heap: \ \texttt{mmap} straight from the operating system \ (Part 32)",
                  font_size=21, color=FUNC),
            label(r"why per-thread caches: \ Part 10's lesson, \ a shared free list is a contended line", font_size=21,
                  color=CTRL),
            label(r"and garbage collectors free memory for you: \ Part 15", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(head, DOWN, buff=0.4)
        # pages of one size class each, and a cache per thread
        import random
        rng = random.Random(4)
        pages = VGroup()
        for sz, n in ((16, 16), (32, 8), (64, 4)):
            cells = VGroup(*[Rectangle(width=4.8 / n, height=0.42, stroke_color=GREY_B, stroke_width=1,
                                       fill_color=YES, fill_opacity=0.55 if rng.random() < 0.6 else 0.06)
                             for _ in range(n)]).arrange(RIGHT, buff=0)
            pages.add(VGroup(label(rf"{sz}-byte page", font_size=16, color=GREY_B).next_to(cells, LEFT, buff=0.15),
                             cells))
        pages.arrange(DOWN, buff=0.15, aligned_edge=RIGHT).to_edge(DOWN, buff=0.45).shift(LEFT * 1.8)
        caches = VGroup(*[VGroup(RoundedRectangle(width=1.9, height=0.5, corner_radius=0.08, stroke_color=CTRL,
                                                  stroke_width=1.5, fill_opacity=0),
                                 label(rf"thread {t}'s cache", font_size=15, color=CTRL)) for t in (1, 2, 3)])
        for c in caches:
            c[1].move_to(c[0])
        caches.arrange(DOWN, buff=0.12).next_to(pages, RIGHT, buff=1.2)
        links = VGroup(*[Arrow(c.get_left(), pages[k][1].get_right(), buff=0.1, color=CTRL, stroke_width=2,
                               max_tip_length_to_length_ratio=0.1) for k, c in enumerate(caches)])
        with self.voiceover(
            "Real allocators combine these ideas. <bookmark mark='a'/> The C library on this machine uses ptmalloc, "
            "descended from Doug Lea's allocator: bins of free blocks by size, boundary tags and coalescing. "
            "<bookmark mark='b'/> Newer allocators, jemalloc, tcmalloc and mimalloc, carve pages into blocks of one "
            "size class each and give every thread its own cache of free blocks. <bookmark mark='c'/> Very large "
            "requests skip the heap entirely and get fresh pages from the operating system, which is Part 32's "
            "subject. <bookmark mark='d'/> The per-thread caches are Part 10's lesson again: a single shared free "
            "list would be a cache line every core fights over. <bookmark mark='e'/> And in languages with garbage "
            "collection, the runtime decides when to free, which Part 15 builds."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
                if mk == "b":
                    self.play(FadeIn(pages))
                if mk == "d":
                    self.play(FadeIn(caches), *[GrowArrow(a) for a in links])
        self.wait(0.3)
        self.clear_scene()
