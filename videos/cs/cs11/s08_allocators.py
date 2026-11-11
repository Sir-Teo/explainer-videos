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
        cl = label("peak heap bytes $\\div$ peak requested live bytes \\\\ includes headers, alignment, rounding and holes", font_size=18, color=GREY_B).next_to(ch, UP,
                                                                                                         buff=0.2)
        y0 = ch.bars[0].get_bottom()[1]
        one = DashedLine([ch.get_left()[0], y0 + 1.5, 0], [ch.get_right()[0], y0 + 1.5, 0], color=GREY_B)
        ol = label("1: lower reference", font_size=16, color=GREY_B).next_to(one, RIGHT, buff=0.1)
        steps = VGroup(label(r"blocks examined \\ per \texttt{malloc}", font_size=18, color=GREY_B))
        for r in rows:
            steps.add(label(rf"{r['name']}: \ {r['steps']:.1f}", font_size=20, color=POL[r["name"]][0]))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.7).shift(DOWN * 0.3)
        best = rows[0]
        punch = label(rf"peak live {best['peak_live'] / 1e6:.2f} MB: \ first fit needs "
                      rf"{best['peak_heap'] / 1e6:.2f} MB, \ the buddy system {rows[-1]['peak_heap'] / 1e6:.2f} MB",
                      font_size=21, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover("These results describe one recorded trace and our simulator's rules. <bookmark mark='a'/> The ratio is peak heap size divided by peak requested live bytes. These peaks need not occur at the same instant. The ratio includes metadata, alignment, rounding and unused holes; it is not external fragmentation alone. <bookmark mark='b'/> First fit, best fit and segregated fits are near 1.13 here. Next fit is slightly larger, and buddy is about 1.82, or 82 percent above peak requested live bytes. The trace does not isolate how much each overhead contributes. A universal quarter-waste rule would require a request-size distribution. <bookmark mark='c'/> The other panel counts blocks examined per allocation. Next fit examines about eighteen, and segregated fits fewer than one on average because some requests extend the heap without a search. These are operation counts, not measured execution times. <bookmark mark='d'/> Size classes can reduce searching, but real performance also depends on synchronization, locality, metadata and workload. One trace does not rank every allocator for every program.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(ch[0]), FadeIn(ch.names), FadeIn(cl), Create(one), FadeIn(ol), *[GrowFromEdge(b, DOWN) for b in ch.bars], FadeIn(ch.vals), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Indicate(ch.bars[-1], color=HEAD), run_time=0.6)
            vo.wait_until('c')
            self.play(FadeIn(steps))
            vo.wait_until('d')
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
        rows = [[(0, 4, "free"), (4, 4, "free")], [(0, 2, ""), (2, 2, "free")], [(0, 1, "used: 16 B"),
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
            label("16-byte payload $+ 8$-byte header, aligned: a 32-byte block", font_size=21,
                  color=GREY_A),
            label("arena-relative buddy address $=$ block address $\\oplus$ block size", font_size=21,
                  color=HEAD),
            label("free: merge only with a free buddy of the same size; repeat upward", font_size=21,
                  color=GREY_A),
            label("25-byte payload $+ 8$-byte header needs 64 bytes here: internal waste", font_size=21,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "A binary buddy allocator splits power-of-two blocks. <bookmark mark='a'/> In our simulator a "
            "sixteen-byte payload needs an eight-byte header and alignment, so it occupies a thirty-two-byte "
            "block. Split 256 into 128, 64 and 32, leaving the other half free at each level. <bookmark "
            "mark='b'/> With addresses measured relative to an aligned arena, a block's buddy is its address "
            "exclusive-or its block size. This identifies its partner, not an arbitrary adjacent free block. "
            "<bookmark mark='c'/> Merge only when that partner is free and has the same size; repeat at the next "
            "level. <bookmark mark='d'/> The arithmetic is simple, but splitting, lookup and merging still have "
            "costs. A twenty-five-byte payload plus the header crosses the thirty-two-byte class and needs "
            "sixty-four bytes here. Waste within an allocated block is internal fragmentation; separated free "
            "holes contribute external fragmentation."
        )
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
            label("jemalloc, tcmalloc, mimalloc: size classes and local fast paths; ownership varies", font_size=21, color=YES),
            label("large requests may use separate OS mappings; thresholds depend on policy",
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
            (
            "Production allocators combine policies with concurrency and locality mechanisms. <bookmark "
            "mark='a'/> glibc's ptmalloc uses size-organized bins, coalescing and boundary metadata, with caches "
            "and multiple arenas. Details vary by release. <bookmark mark='b'/> jemalloc, tcmalloc and mimalloc "
            "use size classes and local fast paths. Their ownership differs: some configurations use thread "
            "caches, others CPU-local or page-local structures. They are not identical designs. <bookmark "
            "mark='c'/> Large requests may use separate operating-system mappings rather than extending a "
            "contiguous brk heap, depending on policy and thresholds. <bookmark mark='d'/> Local caches can "
            "reduce shared-list contention, at a cost in retained memory and cross-thread transfer complexity. "
            "Part 10's coherence lessons explain one part of that tradeoff. <bookmark mark='e'/> "
            "Garbage-collected runtimes decide when unreachable objects can be reclaimed, while still relying on "
            "allocation machinery. Part 15 builds those mechanisms."
        )
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
