from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import (
    Plot, fmt_int, fmt_ns, label, load, machine_tag, mtex, node, note, real_tag, schematic_tag, tagged,
)


def cell(text, color=GREY_B, w=1.0, h=0.5, font_size=20, fill=0.12):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=fill)
    t = label(text, font_size=font_size).move_to(r) if text else VGroup()
    g = VGroup(r, t)
    g.box, g.text = r, t
    return g


class BuildingTheBook(VoiceoverScene):
    def construct(self):
        self.structures()
        self.speed()

    # ------------------------------------------------------------------
    def structures(self):
        p = load("messages")["picks"]
        add, dele = p["A"]["fields"], p["D"]["fields"]
        # price levels: an array indexed by price in cents, each the head of a FIFO list
        prices = [18033, 18034, 18035, 18036, 18037]
        lv_cells = VGroup(*[cell(f"{x / 100:.2f}", C.BID if x <= 18035 else C.ASK, w=1.55, h=0.62, font_size=26)
                            for x in prices]).arrange(RIGHT, buff=0.06).move_to(UP * 1.9 + RIGHT * 2.3)
        arr_l = label(r"price levels: an array indexed by price", font_size=26, color=GREY_A).next_to(lv_cells, UP, buff=0.6)
        queues = {18033: [200, 100], 18034: [50, 300, 100], 18035: [100, 400], 18036: [100, 25], 18037: [300]}
        chains = {}
        for x, c in zip(prices, lv_cells):
            col = C.BID if x <= 18035 else C.ASK
            nodes = VGroup(*[cell(str(s), col, w=1.0, h=0.46, font_size=22, fill=0.35) for s in queues[x]])
            nodes.arrange(DOWN, buff=0.26).next_to(c, DOWN, buff=0.3)
            links = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.02, stroke_width=2, color=col,
                                   max_tip_length_to_length_ratio=0.4, tip_length=0.1) for a, b in zip(nodes[:-1], nodes[1:])])
            head = Arrow(c.get_bottom(), nodes[0].get_top(), buff=0.02, stroke_width=2, color=col, tip_length=0.1,
                         max_tip_length_to_length_ratio=0.4)
            chains[x] = VGroup(head, nodes, links)
            chains[x].nodes, chains[x].links = nodes, links
        fifo = label(r"each level: a first-in, first-out list of orders", font_size=22, color=GREY_A)
        fifo.next_to(VGroup(*[chains[x] for x in prices]), DOWN, buff=0.25)
        # the order map: a hash table from reference number to the order's node
        slots = VGroup(*[cell("", GREY_B, w=2.6, h=0.5) for _ in range(7)]).arrange(DOWN, buff=0.05)
        slots.move_to(LEFT * 4.6 + DOWN * 0.1)
        map_l = label(r"order map: reference \# $\to$ order", font_size=26, color=GREY_A).next_to(slots, UP, buff=0.15)
        filled = {1: "\\#53{,}998{,}112", 3: "\\#" + fmt_int(dele["order reference"]), 5: "\\#54{,}007{,}380"}
        for i, t in filled.items():
            slots[i].text = label(t, font_size=21).move_to(slots[i])
            slots[i].add(slots[i].text)
        tag = schematic_tag(corner=DR)
        head = label(r"rebuilding the order book", font_size=36).to_corner(UL, buff=0.4)
        self.play(FadeIn(head), run_time=0.6)
        with self.voiceover(
            "So a feed handler must remember every live order. How you store them decides how fast you are, so here is "
            "the design almost everyone converges on. <bookmark mark='a'/> First, an array of price levels, indexed "
            "directly by the price in cents: finding a price is just arithmetic, no searching. <bookmark mark='f'/> "
            "Each level holds its orders as a first-in, first-out list: the front of the list is the front of the "
            "queue. <bookmark mark='m'/> Second, a hash table from each order's reference number to where that order "
            "lives, because cancels and executions name only the number."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in lv_cells], lag_ratio=0.1), FadeIn(arr_l))
            vo.wait_until("f")
            self.play(LaggedStart(*[FadeIn(chains[x]) for x in prices], lag_ratio=0.15), FadeIn(fifo), run_time=1.5)
            vo.wait_until("m")
            self.play(FadeIn(slots), FadeIn(map_l))

        # an add: the real message from before
        msg = tagged(rf"Add \#{fmt_int(add['order reference'])}: buy 100 @ 180.35", font_size=26, color=C.MSG)
        msg.to_corner(DL, buff=0.4)
        h_lab = mtex(r"h(\#54{,}010{,}847) \bmod 7 = 6", font_size=26, color=GREY_A).next_to(slots, DOWN, buff=0.2)
        new_node = cell("100", C.BID, w=1.0, h=0.46, font_size=22, fill=0.35)
        c35 = chains[18035]
        new_node.next_to(c35.nodes[-1], DOWN, buff=0.26)
        new_link = Arrow(c35.nodes[-1].get_bottom(), new_node.get_top(), buff=0.02, stroke_width=2, color=C.BID,
                         tip_length=0.1, max_tip_length_to_length_ratio=0.4)
        best = VGroup(SurroundingRectangle(lv_cells[2], color=C.BID, buff=0.06, stroke_width=4),
                      label(r"best bid", font_size=24, color=C.BID).next_to(lv_cells[2], UP, buff=0.12))
        with self.voiceover(
            "<bookmark mark='a'/> Watch the real add order from before arrive. <bookmark mark='h'/> Hash its number "
            "to find a slot in the map. <bookmark mark='n'/> Take a pre-allocated order record, fill it in, and link it "
            "onto the back of the 180.35 list. <bookmark mark='u'/> Update the level's total, and if the price beats "
            "the best bid, move the best-bid marker. A handful of memory accesses, and no matter how many orders "
            "are in the book, it takes the same time."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(msg, shift=UP * 0.2))
            vo.wait_until("h")
            self.play(FadeIn(h_lab), Indicate(slots[6], color=C.MSG))
            slots[6].text = label(r"\#54{,}010{,}847", font_size=21, color=C.MSG).move_to(slots[6])
            self.play(FadeIn(slots[6].text))
            vo.wait_until("n")
            ptr = CurvedArrow(slots[6].get_right(), new_node.get_left(), angle=-0.4, color=C.MSG, stroke_width=2)
            self.play(FadeIn(new_node, shift=DOWN * 0.2), GrowArrow(new_link), Create(ptr))
            vo.wait_until("u")
            self.play(FadeIn(best))
        # a delete: hash, find, unlink
        dmsg = tagged(rf"Delete \#{fmt_int(dele['order reference'])}", font_size=26, color=C.CANCEL).to_corner(DL, buff=0.4)
        c34 = chains[18034]
        victim = c34.nodes[1]
        with self.voiceover(
            "<bookmark mark='d'/> A delete: hash the number, follow the pointer straight to the order, <bookmark "
            "mark='x'/> and unlink it: its neighbors now point at each other, and the record goes back on a free list "
            "for reuse. Nothing is searched, and nothing is allocated from the operating system while trading."
        ) as vo:
            vo.wait_until("d")
            self.play(FadeOut(msg), FadeOut(h_lab), FadeIn(dmsg, shift=UP * 0.2))
            ptr2 = CurvedArrow(slots[3].get_right(), victim.get_left(), angle=-0.3, color=C.CANCEL, stroke_width=2)
            self.play(Indicate(slots[3], color=C.CANCEL), Create(ptr2))
            vo.wait_until("x")
            below = VGroup(c34.nodes[2])
            relink = Arrow(c34.nodes[0].get_bottom(), c34.nodes[2].get_top() + UP * (victim.height + 0.22), buff=0.02,
                           stroke_width=2, color=C.BID, tip_length=0.1, max_tip_length_to_length_ratio=0.4)
            self.play(FadeOut(victim, shift=RIGHT * 0.5), FadeOut(c34.links), FadeOut(ptr2), FadeOut(slots[3].text))
            self.play(below.animate.shift(UP * (victim.height + 0.22)), FadeIn(relink))
        self.clear_scene()

    # ------------------------------------------------------------------
    def speed(self):
        b = load("bookbench")
        py, nat = b["python"], b["native"]
        n = b["messages"]
        v = nat["variants"]
        assert abs(n - 14_953_094) < 1 and 600 < py["ns_per_message"] < 1000 and 25 < v["prefaulted"]["ns_per_message"] < 45
        rows = [
            (r"Python, dictionaries", py["ns_per_message"], GREY_B),
            (r"C, memory faulted in on demand", v["cold"]["ns_per_message"], C.MSG),
            (r"C, memory touched in advance", v["prefaulted"]["ns_per_message"], C.MSG),
        ]
        ch = Plot((10, 1000), (0, 3), width=7.0, height=2.8, log_x=True, x_ticks=[10, 100, 1000],
                  x_fmt=lambda x: fmt_ns(x), grid=False, x_grid=True).move_to(RIGHT * 2.2 + UP * 0.6)
        ch.y_labels.set_opacity(0)
        ch.y_axis.set_opacity(0)
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        for i, (t, ns, col) in enumerate(rows):
            y = 2.5 - i
            p0, p1 = ch.c2p(10, y), ch.c2p(ns, y)
            bar = Rectangle(width=p1[0] - p0[0], height=0.55, stroke_width=0, fill_color=col, fill_opacity=0.85)
            bar.move_to((p0 + p1) / 2)
            bars.add(bar)
            labs.add(label(t, font_size=24, color=col).next_to(p0, LEFT, buff=0.2))
            vals.add(MathTex(fmt_ns(ns), font_size=28).next_to(bar, RIGHT, buff=0.12))
        ttl = label(rf"the whole day of SPY on Nasdaq: {fmt_int(n)} messages, through two order books", font_size=30)
        ttl.to_edge(UP, buff=0.35)
        tag = machine_tag(corner=DR)
        tot = VGroup(label(rf"Python: {py['total_s']:.1f} s for the day", font_size=26, color=GREY_B),
                     label(rf"C: {v['prefaulted']['total_ms'] / 1000:.2f} s for the day", font_size=26, color=C.MSG),
                     label(rf"(same algorithm; both end the day with identical books)", font_size=22, color=GREY_A)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DL, buff=0.5).shift(UP * 0.8)
        with self.voiceover(
            "How fast is it? Here is every message of SPY, the most traded ETF in the world, for the whole day on "
            "Nasdaq: almost fifteen million of them, through two implementations of exactly this design. <bookmark "
            "mark='p'/> In Python, about 780 nanoseconds a message. <bookmark mark='c'/> In C, about 38. <bookmark "
            "mark='f'/> And touching all the memory in advance, so the operating system never has to stop the program "
            f"to hand it a fresh page, removes {v['cold']['page_faults']:,} pauses and brings it to 35. <bookmark "
            "mark='t'/> The whole day of SPY, rebuilt in about half a second."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(tag), Create(ch.x_axis), FadeIn(ch.x_labels), FadeIn(ch.grid))
            for i, m in enumerate("pcf"):
                vo.wait_until(m)
                self.play(GrowFromEdge(bars[i], LEFT), FadeIn(labs[i]), FadeIn(vals[i]))
            vo.wait_until("t")
            self.play(FadeIn(tot))
        self.clear_scene()

        # per-message distribution: the tail
        h = np.array(nat["hist"], float)  # 20 bins per decade from 1 ns
        edges = 10 ** (np.arange(len(h) + 1) / 20)
        frac = h / h.sum()
        pc = nat["pct"]
        assert pc["99.99"] > 5000
        ch2 = Plot((10, 1e6), (0, frac.max() * 1.15), width=11, height=4.2, log_x=True,
                   x_ticks=[10, 100, 1e3, 1e4, 1e5, 1e6], x_fmt=lambda x: fmt_ns(x), y_ticks=[]).shift(DOWN * 0.3)
        hist = ch2.histogram(edges, frac, C.MSG, opacity=0.85)
        ttl2 = label(r"time for each single update, measured one at a time", font_size=32).to_edge(UP, buff=0.35)
        marks = VGroup()
        for q, txt in [("50", "median"), ("99", "99th pct"), ("99.99", "99.99th pct")]:
            x = pc[q]
            ln = ch2.vline(x, color=C.LATENCY if q != "99.99" else C.KERNEL, y1=frac.max() * 1.05)
            t = label(rf"{txt}\\{fmt_ns(x, tex=False).replace('us', r'$\mu$s')}", font_size=22,
                      color=C.LATENCY if q != "99.99" else C.KERNEL).next_to(ln, UP, buff=0.05)
            marks.add(VGroup(ln, t))
        with self.voiceover(
            "But averages hide the thing that matters most. <bookmark mark='h'/> Timing every update individually, "
            "the typical one takes well under a hundred nanoseconds, and ninety-nine in a hundred finish within a few "
            "hundred. <bookmark mark='t'/> But one in ten thousand takes more than ten microseconds, a hundred times "
            "longer, and the code had nothing to do with it: something else, the operating system or the virtual "
            "machine underneath it, interrupted the program. Those rare stalls tend to arrive exactly when the market "
            "is busiest. We'll come back to them."
        ) as vo:
            self.play(FadeIn(ttl2), Create(ch2), FadeIn(machine_tag(corner=DR)))
            vo.wait_until("h")
            self.play(FadeIn(hist), FadeIn(marks[0]), FadeIn(marks[1]))
            vo.wait_until("t")
            self.play(FadeIn(marks[2]), Indicate(hist[-12:], color=C.KERNEL))
        self.clear_scene()
