from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (BG, DATA, HEAD, LAM, NO, PART, YES, curve, fit_right, load)


def strip(blocks, unit=0.42, y=0.0, x0=-6.72):
    """A row of 16 pages drawn as blocks (start, size, colour, text)."""
    g = VGroup()
    for a, n, c, t in blocks:
        r = Rectangle(width=n * unit, height=0.62, stroke_color=c, stroke_width=1.6, fill_color=c,
                      fill_opacity=0.3 if t else 0.06)
        r.move_to([x0 + (a + n / 2) * unit, y, 0])
        g.add(VGroup(r, label(t, font_size=17, color=WHITE).move_to(r)))
    return g


class Alloc(VoiceoverScene):
    def construct(self):
        self.card()
        self.buddy()
        self.traffic()
        self.machine()
        self.slab()

    def card(self):
        card = chapter_card(11, r"Kernel allocators", r"How does the kernel hand out its own memory?",
                            lit=(1965, 1994), extra=((1965, r"Knowlton: \ buddy system"), (1994, r"Bonwick: \ slab")),
                            part=PART)
        with self.voiceover("Chapter eleven. How the kernel allocates memory for itself."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def buddy(self):
        d = load("alloc")
        sd = d["split_demo"]
        head = label(r"The buddy system: \ split in halves, \ merge with your buddy", font_size=34).to_edge(UP, buff=0.3)
        u = 0.72
        x0 = -5.1
        rows = [
            strip([(0, 16, YES, "free: \\ 16")], u, 1.9, x0),
            strip([(0, 8, GREY_B, ""), (8, 8, YES, "free: \\ 8")], u, 0.9, x0),
            strip([(0, 4, GREY_B, ""), (4, 4, YES, "free: \\ 4"), (8, 8, YES, "free: \\ 8")], u, -0.1, x0),
            strip([(0, 4, DATA, "3 pages \\ (+1 wasted)"), (4, 4, YES, "free: \\ 4"), (8, 8, YES, "free: \\ 8")], u,
                  -1.1, x0),
        ]
        tags = VGroup(*[label(t, font_size=17, color=GREY_A).next_to(r, LEFT, buff=0.15) for t, r in zip(
            (r"16", r"split", r"split", r"take"), rows)])
        for t in tags:
            fit_right(t)
        fl = ", \\ ".join(rf"order {k}: \ {v or '--'}" for k, v in sd.items() if int(k) >= 2)
        lines = VGroup(
            label(rf"a request for 3 pages rounds up to 4; \ free lists afterwards: \ {fl}", font_size=20, color=WHITE),
            label(r"a block at address $a$ of size $2^k$ has its buddy at $a \oplus 2^k$: \ one XOR finds it", font_size=20,
                  color=LAM),
            label(r"freeing the 4: \ its buddy at 4 is free, \ merge to 8; \ that one's buddy at 8 is free, \ merge to 16",
                  font_size=20, color=YES),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The kernel needs memory too: for page tables, process control blocks, network buffers. It takes it in "
            "physical frames, and the classic allocator for frames is the buddy system, from Knowlton in 1965. "
            "<bookmark mark='a'/> Memory is kept in blocks whose sizes are powers of two. A request for three pages "
            "rounds up to four. <bookmark mark='b'/> There is no free block of four, so the sixteen splits into two "
            "eights, and one eight into two fours. The first four is handed out; its halves' partners stay on the "
            "free lists. <bookmark mark='c'/> Each block's partner, its buddy, is found by flipping one bit of its "
            "address. <bookmark mark='d'/> So freeing is quick: if the buddy is free too, merge, and try again one "
            "size up. Fragmentation can never leave two free buddies side by side."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(tags[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            for r, t in zip(rows[1:], tags[1:]):
                self.play(FadeIn(r, shift=DOWN * 0.1), FadeIn(t), run_time=0.8)
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def traffic(self):
        d = load("alloc")
        s = load("segments")
        ser = d["series"]
        head = label(r"Buddy under random traffic", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 3000, 500], y_range=[0, 1024, 256], x_length=6.2, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.1).shift(DOWN * 0.3)
        xt = VGroup(*[label(f"{x:,}".replace(",", "{,}"), font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN,
                                                                                              buff=0.08)
                      for x in (0, 1000, 2000, 3000)])
        yt = VGroup(*[label(f"{y:,}".replace(",", "{,}"), font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT,
                                                                                              buff=0.08)
                      for y in (0, 512, 1024)])
        xl = label(r"step: \ allocate 1--30 pages, \ or free one", font_size=17, color=GREY_A).next_to(xt, DOWN,
                                                                                                    buff=0.1)
        fr = curve(ax, [p["step"] for p in ser], [p["free"] for p in ser], YES, dots=False)
        lg = curve(ax, [p["step"] for p in ser], [p["largest"] for p in ser], HEAD, dots=False)
        k1 = label(r"free pages", font_size=17, color=YES).next_to(ax.c2p(2600, 960), UP, buff=0.05)
        k2 = label(r"largest free block", font_size=17, color=HEAD).next_to(ax.c2p(900, 512), UP, buff=0.05)
        notes = VGroup(
            label(rf"1{{,}}024 pages, \ 3{{,}}000 steps: \\ {d['splits']} splits, \ {d['merges']} merges", font_size=20,
                  color=WHITE),
            label(rf"requests refused: \ \textbf{{{d['fails']}}}; \\ a free block of {min(p['largest'] for p in ser)}+ pages "
                  r"at every step", font_size=20, color=YES),
            label(rf"chapter 2's segments, \ same pool: \\ {s['fails']} refused, \ largest hole {s['largest']}",
                  font_size=20, color=NO),
            label(r"the price is \textbf{internal} fragmentation: \\ 5 pages take a block of 8", font_size=20,
                  color=HEAD),
            label(r"Linux keeps orders 0--10: \\ \texttt{/proc/buddyinfo} lists them", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "Run it under random traffic: a thousand and twenty-four pages, three thousand steps, each one allocating "
            "between one and thirty pages or freeing an earlier block. <bookmark mark='a'/> Blocks split five hundred "
            "and eighty-three times and merged five hundred and seventeen times. <bookmark mark='b'/> Not one request "
            "was refused: there was always a free block of at least a quarter of the pool, usually half. <bookmark mark='c'/> Chapter two's "
            "segments, in the same size of pool, refused two hundred and forty-seven. <bookmark mark='d'/> The price "
            "is waste inside the blocks: five pages occupy a block of eight. <bookmark mark='e'/> Linux uses exactly "
            "this for physical frames, with eleven sizes, from one page to a thousand and twenty-four, and you can "
            "read the free lists in proc buddy-info."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl))
            self.play(Create(fr), Create(lg), FadeIn(k1), FadeIn(k2), run_time=2.0)
            for mk, n_ in zip("abcde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def machine(self):
        d = load("buddyinfo")
        counts, mib = d["counts"], d["free_mib"]
        head = label(r"This machine's free lists, \ right now", font_size=36).to_edge(UP, buff=0.3)
        mx = max(mib)
        bars = VGroup()
        for k, (c, m) in enumerate(zip(counts, mib)):
            h = max(0.03, 3.6 * m / mx)
            r = Rectangle(width=0.62, height=h, stroke_width=0, fill_color=YES if k == len(counts) - 1 else DATA,
                          fill_opacity=0.85)
            bars.add(r)
        bars.arrange(RIGHT, buff=0.18, aligned_edge=DOWN).move_to([-2.0, -0.2, 0])
        size = lambda k: (f"{4 << k} KiB" if (4 << k) < 1024 else f"{(4 << k) // 1024} MiB")
        xl = VGroup(*[label(rf"{k}", font_size=17, color=GREY_A).next_to(b, DOWN, buff=0.1) for k, b in
                      enumerate(bars)])
        sl = VGroup(*[label(size(k), font_size=13, color=GREY_B).next_to(x, DOWN, buff=0.06) for k, x in
                      enumerate(xl)])
        cl = VGroup(*[label(f"{c:,}".replace(",", "{,}"), font_size=14, color=WHITE).next_to(b, UP, buff=0.06)
                      for c, b in zip(counts, bars)])
        ol = label(r"order $k$: \ blocks of $2^k$ pages", font_size=17, color=GREY_A).next_to(sl, DOWN, buff=0.12)
        yl = label(r"free memory in blocks of each order \ (bars); \ number of blocks \ (above)", font_size=17,
                   color=GREY_A).next_to(bars, UP, buff=0.5)
        tot = sum(mib) / 1024
        notes = VGroup(
            label(rf"zone {d['zone']}: \ {tot:.1f} GiB free", font_size=21, color=WHITE),
            label(rf"{mib[-1] / sum(mib):.0%} of it in 4 MiB blocks, \\ the largest order".replace("%", r"\%"),
                  font_size=21, color=YES),
            label(rf"only {counts[0]} single pages: \\ freed pages merge with their buddies", font_size=21, color=HEAD),
            label(r"a busy machine runs low on high orders: \\ then huge pages need \textbf{compaction}, \\ moving pages "
                  r"to rebuild free blocks", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(bars, RIGHT, buff=0.8).align_to(bars, UP)
        fit_right(notes)
        with self.voiceover(
            "And here are this machine's own free lists, read just now from proc buddy-info. <bookmark mark='a'/> "
            "Each bar is one order: single pages on the left, four-mebibyte blocks on the right. <bookmark mark='b'/> "
            "There are almost six gibibytes free. <bookmark mark='c'/> Nearly half of it is in the largest blocks, "
            "ready to be split for any request, or to become huge pages. <bookmark mark='d'/> And there are only eight "
            "free single pages: freed pages almost always find their buddy and merge. <bookmark mark='e'/> On a busy "
            "machine that has run for weeks, the high orders run dry. Then a request for a huge page has to wait for "
            "compaction: the kernel moves pages around, updating their mappings, to rebuild large free blocks."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(yl), FadeIn(xl), FadeIn(sl), FadeIn(ol),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), run_time=2.0)
            self.play(FadeIn(cl))
            for mk, n_ in zip("bcde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def slab(self):
        d = load("alloc")
        head = label(r"Small objects: \ the slab allocator", font_size=36).to_edge(UP, buff=0.3)
        page = VGroup()
        per = d["per_slab"]
        for i in range(per):
            c = DATA if i % 3 != 2 else BG
            page.add(Rectangle(width=0.36, height=0.36, stroke_color=DATA, stroke_width=1, fill_color=c,
                               fill_opacity=0.45 if c is DATA else 1))
        page.arrange_in_grid(rows=4, cols=14, buff=0.04)
        frame = SurroundingRectangle(page, color=GREY_B, buff=0.08)
        pl = label(rf"one 4 KiB slab: \ {per} objects of {d['obj']} bytes \ (a cache per type: \ inodes, \ "
                   rf"PCBs, \ sockets)", font_size=19, color=GREY_A).next_to(frame, UP, buff=0.12)
        g = VGroup(pl, frame, page).next_to(head, DOWN, buff=0.4)
        mb = lambda b: f"{b / 1e6:.2f}"
        bars = VGroup()
        for t, v, c in ((r"a page each \ (buddy)", d["buddy_bytes"], NO), (r"slabs", d["slab_bytes"], YES)):
            w = max(0.08, 6.0 * v / d["buddy_bytes"])
            r = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=c, fill_opacity=0.8)
            tl = label(t, font_size=19, color=c)
            vl = label(rf"{mb(v)} MB", font_size=19, color=WHITE)
            bars.add(VGroup(tl, r, vl).arrange(RIGHT, buff=0.2))
        bars.arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(g, DOWN, buff=0.35)
        bl = label(rf"{d['n']:,} objects of {d['obj']} bytes".replace(",", "{,}"), font_size=19,
                   color=GREY_A).next_to(bars, UP, buff=0.1).align_to(bars, LEFT)
        lines = VGroup(
            label(r"a freed object goes back on its slab's list, \ \textit{still constructed}: \ the next allocation "
                  r"skips the set-up", font_size=20, color=HEAD),
            label(r"Bonwick, \ SunOS 1994; \ Linux's SLUB today; \ \texttt{/proc/slabinfo}, \ \texttt{slabtop}",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "But most of what a kernel allocates is small: a socket, an open file, a process control block of a "
            "hundred bytes or so. A page each would be absurd. <bookmark mark='a'/> Jeff Bonwick's slab allocator, "
            "written for SunOS in 1994, keeps a cache for each kind of object. Each cache carves pages into slots of "
            "exactly that size: fifty-six objects of seventy-two bytes in one page. <bookmark mark='b'/> Ten thousand "
            "such objects take forty-one megabytes at a page each, and under three quarters of a megabyte in slabs. "
            "<bookmark mark='c'/> And Bonwick's second idea: a freed object goes back to its slab still initialised, "
            "so the next allocation of that type can skip setting it up. <bookmark mark='d'/> Linux's allocator, "
            "called SLUB, descends from it; slab-top shows its caches on any Linux machine."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pl), Create(frame), LaggedStart(*[FadeIn(c) for c in page], lag_ratio=0.02),
                      run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(bl), *[FadeIn(b[0]) for b in bars])
            self.play(*[GrowFromEdge(b[1], LEFT) for b in bars], *[FadeIn(b[2]) for b in bars])
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()
