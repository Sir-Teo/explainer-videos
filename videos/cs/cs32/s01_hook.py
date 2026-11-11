from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (BG, DATA, HEAD, PART, YES, hx, load, mono)


def proc_box(name, color, pos, lines):
    r = RoundedRectangle(width=4.4, height=2.5, corner_radius=0.15, stroke_color=color, stroke_width=2.5,
                         fill_color=BG, fill_opacity=1).move_to(pos)
    t = label(name, font_size=24, color=color).next_to(r.get_top(), DOWN, buff=0.2)
    body = VGroup(*[mono(s, 18, c) for s, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(
        t, DOWN, buff=0.25)
    return VGroup(r, t, body)


class Hook(VoiceoverScene):
    def construct(self):
        self.same()
        self.plan()

    def same(self):
        d = load("sameva")
        va = d["va"]
        w1, w2 = d["walks"]
        head = label(r"Two programs, \ one address", font_size=36).to_edge(UP, buff=0.3)
        a = proc_box(r"process 1", DATA, [-3.4, 1.2, 0], [(f"store 1 -> {hx(va)}", WHITE), ("yield", GREY_B),
                                                          (f"load  {hx(va)} -> {w1['value']}", YES)])
        b = proc_box(r"process 2", HEAD, [3.4, 1.2, 0], [(f"store 2 -> {hx(va)}", WHITE), ("yield", GREY_B),
                                                         (f"load  {hx(va)} -> {w2['value']}", YES)])
        ram = Rectangle(width=11.0, height=0.6, stroke_color=GREY_B, fill_color=BG, fill_opacity=1).move_to([0, -1.6, 0])
        rl = label(r"physical memory, \ 1 MiB to 1.125 MiB \ (where the frames are)", font_size=18,
                   color=GREY_B).next_to(ram, DOWN, buff=0.1)
        x0 = ram.get_left()[0]
        lo, span = 0x100000, 0x20000

        def mark(pa, color):
            x = x0 + 11.0 * (pa - lo) / span
            return VGroup(Rectangle(width=0.12, height=0.6, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to(
                [x, -1.6, 0]), mono(hx(pa), 16, color).move_to([x, -1.05, 0]))
        m1, m2 = mark(w1["pa"], DATA), mark(w2["pa"], HEAD)
        ar1 = Arrow(a.get_bottom(), m1[1].get_top(), buff=0.1, color=DATA, stroke_width=2.5)
        ar2 = Arrow(b.get_bottom(), m2[1].get_top(), buff=0.1, color=HEAD, stroke_width=2.5)
        lines = VGroup(
            label(rf"the same program, \ the same address {hx(va)}: \ each reads back \textbf{{its own}} number",
                  font_size=22, color=WHITE),
            label(r"every address a program uses is \textbf{virtual}: \ the hardware translates it, \ through a table "
                  r"the kernel keeps for that process", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Two copies of the same program run on our machine. <bookmark mark='a'/> Each stores its process number "
            "at the same address, hexadecimal four oh five, oh oh four. Then each steps aside, so "
            "the other can store its number at that very address. <bookmark mark='b'/> Then each reads the address "
            "back. Process one finds one, and process two finds two. <bookmark mark='c'/> They used the same address, "
            "and two different bytes of memory. <bookmark mark='d'/> Every address a program uses is virtual. The "
            "hardware translates it, on every load, store and instruction fetch, through a table the kernel keeps for "
            "that process. This part builds that translation into Pebble, and asks what it costs and what it buys."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a[:2]), FadeIn(b[:2]))
            vo.wait_until("a")
            self.play(FadeIn(a[2][:2]), FadeIn(b[2][:2]))
            vo.wait_until("b")
            self.play(FadeIn(a[2][2]), FadeIn(b[2][2]))
            vo.wait_until("c")
            self.play(FadeIn(ram), FadeIn(rl), GrowArrow(ar1), GrowArrow(ar2), FadeIn(m1), FadeIn(m2))
            vo.wait_until("d")
            self.play(FadeIn(lines))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Virtual Memory", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"relocation and protection: \ from base and bounds to pages",
            r"page tables as a tree walked by hardware, \ and the TLB that caches it, \ measured here",
            r"page faults and demand paging: \ what a miss to disk costs",
            r"which page to evict: \ Belady's optimum, \ his anomaly, \ LRU, \ CLOCK, \ ARC, \ LIRS",
            r"copy-on-write, \ the kernel's mapping and Meltdown, \ buddy and slab allocators",
            r"virtual machines and containers: \ PebbleOS on our own hypervisor",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 32 of Computer Science, Built: Virtual Memory. <bookmark mark='a'/> In this part: why programs need "
            "relocation and protection, and why pages won; page tables, the tree the hardware walks on every access, "
            "and the cache that makes it fast, measured on this machine; page faults, and what a trip to the disk "
            "costs; which page to throw out when memory is full, with the optimum, a famous anomaly, and the policies "
            "in real systems; copy-on-write, the kernel's own mapping and Meltdown, and the kernel's allocators; and "
            "virtual machines and containers, with our own operating system running on a hypervisor we write."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
